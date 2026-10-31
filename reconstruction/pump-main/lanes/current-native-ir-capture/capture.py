"""One fixed-source diagnostic build; never a source/IR-edit or LLVM-variant oracle."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import sys

SOURCE_SHA256 = '29a8df2d7e12b379a9dc515d5a84eaaf051729da62350a54996a0077015f0c8a'
SOURCE_FILES = 141
SYMBOL = '_ZN14pump_recovered9admin_cto7execute17h3bd6d7f34f2e30d7E'
LLVM_ARGUMENTS = (
    '-filter-print-funcs=' + SYMBOL,
    '-print-after=finalize-isel',
    '-print-before=greedy',
    '-print-after=greedy',
    '-print-after=virtregrewriter',
    '-print-after=block-placement',
)
ROOT_ARGUMENTS = ('--emit=link,llvm-ir',) + tuple(
    item for value in LLVM_ARGUMENTS for item in ('-C', 'llvm-args=' + value))
STAGES = (('After', 'finalize-isel'), ('Before', 'greedy'), ('After', 'greedy'),
          ('After', 'virtregrewriter'), ('After', 'block-placement'))
ENVIRONMENT_KEYS = (
    'RUSTC', 'RUSTC_WRAPPER', 'CARGO_HOME', 'CARGO_TARGET_DIR', 'CARGO_BUILD_JOBS',
    'CARGO_TARGET_SBPF_SOLANA_SOLANA_RUSTFLAGS', 'CC', 'AR', 'OBJDUMP', 'OBJCOPY',
    'PUMP_RECON_HOME', 'PUMP_RECON_PYTHON', 'PUMP_LOGICAL_REGISTRY_SRC',
    'PUMP_LINK_NEXT_WRAPPER', 'PUMP_LINK_ROOT_CRATE', 'PUMP_LINK_SCRIPT',
    'PUMP_LINK_SCRIPT_SHA256', 'PUMP_LINK_LLD', 'PUMP_LINK_RECEIPT', 'PUMP_LINK_MAP',
    'PYTHONDONTWRITEBYTECODE')
OWNED_OUTPUTS = ('capture-result.json', 'llvm-ir', 'machine-dumps')
BUILD_OUTPUTS = ('build.log', 'unstripped.so', 'candidate.so', 'source-inputs.json',
                 'link-receipt.json', 'link.map')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def overlap(first, second):
    return first == second or first in second.parents or second in first.parents


def admit_paths(src, work, out, expected_source):
    """Read-only admission before creating any helper directory or receipt."""
    for path in (src, work, out):
        require(not path.is_symlink(), 'source/work/output must not be a symlink')
    src, work, out = (path.resolve() for path in (src, work, out))
    require(src == expected_source.resolve() and src.is_dir(), 'only frozen repository source is admitted')
    require(not overlap(src, work) and not overlap(src, out), 'source overlaps workspace/output')
    require(not overlap(work, out), 'diagnostic workspace/output must be separate')
    require(not out.exists() or out.is_dir(), 'output must be a directory')
    require(not work.exists() or work.is_dir(), 'workspace must be a directory')
    for name in OWNED_OUTPUTS + BUILD_OUTPUTS:
        destination = out / name
        require(not destination.exists() and not destination.is_symlink(),
                'diagnostic output already present: ' + name)
    require(not (work / 'target-identity').exists()
            and not (work / 'target-identity').is_symlink(), 'diagnostic target must start absent')
    return src, work, out


def rewrite_command(command):
    """Pure transformation; the hook separately requires the entire frozen argv."""
    require(isinstance(command, list) and len(command) >= 2
            and Path(command[0]).name == 'cargo' and command[1] == 'build'
            and command[-1] == '--offline' and '--release' in command
            and '--locked' in command and '--' not in command,
            'unexpected maintained cold Cargo command')
    result = list(command)
    result[1] = 'rustc'
    return result + ['--lib', '--', *ROOT_ARGUMENTS]


def collect(out, work):
    """Copy every available .ll and exact log slice, including on build failure."""
    ir_folder, dump_folder = out / 'llvm-ir', out / 'machine-dumps'
    ir_folder.mkdir()
    dump_folder.mkdir()
    modules = []
    deps = work / 'target-identity/sbpf-solana-solana/release/deps'
    for source in sorted(deps.glob('*.ll')):
        require(source.is_file() and not source.is_symlink(), 'unexpected emitted IR file type')
        destination = ir_folder / source.name
        with source.open('rb') as reader, destination.open('xb') as writer:
            shutil.copyfileobj(reader, writer)
        text = destination.read_text(encoding='utf-8')
        modules.append({'file': destination.relative_to(out).as_posix(),
                        'bytes': destination.stat().st_size, 'sha256': digest(destination),
                        'containsTargetDefinition': bool(re.search(
                            r'(?m)^define\b[^\n]*@"?' + re.escape(SYMBOL) + r'"?\(', text))})
    log = out / 'build.log'
    require(not log.is_symlink(), 'raw build log must not be a symlink')
    raw = log.read_bytes() if log.is_file() else b''
    starts = list(re.finditer(rb'(?m)^\*\*\* IR Dump [^\r\n]+', raw))
    dumps = []
    for i, start in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(raw)
        part = raw[start.start():end]
        destination = dump_folder / ('dump-%03d.txt' % (i + 1))
        with destination.open('xb') as writer:
            writer.write(part)
        # A heading or a truncated body alone cannot qualify a requested stage.
        complete = (b'# Machine code for function ' + SYMBOL.encode() + b':' in part
                    and b'# End machine code for function ' + SYMBOL.encode() + b'.' in part)
        dumps.append({'file': destination.relative_to(out).as_posix(),
                      'bytes': len(part), 'sha256': digest(destination),
                      'rawLogOffset': start.start(), 'rawLogEnd': end,
                      'heading': start.group().decode('utf-8', errors='replace'),
                      'containsTargetSymbol': SYMBOL.encode() in part,
                      'completeTargetMachineFunction': complete})
    observed = []
    for timing, stage in STAGES:
        matching = [d['file'] for d in dumps
                    if ('IR Dump ' + timing + ' ') in d['heading']
                    and ('(' + stage + ')') in d['heading'] and d['completeTargetMachineFunction']]
        observed.append({'timing': timing, 'pass': stage, 'files': matching})
    return {'llvmIr': modules, 'machineDumps': dumps, 'requestedStages': observed,
            'allRequestedStagesObserved': all(x['files'] for x in observed),
            'targetDefinitionRetained': any(x['containsTargetDefinition'] for x in modules),
            'rawBuildLogPresent': log.is_file(),
            'rawBuildLogSha256': hashlib.sha256(raw).hexdigest(),
            'rawBuildLogBytes': len(raw)}


def capture(fastbuild, src, work, out, expected_source):
    src, work, out = admit_paths(src, work, out, expected_source)
    source = fastbuild.snapshot(src)
    require(source['sha256'] == SOURCE_SHA256 and len(source['files']) == SOURCE_FILES,
            'selected source differs from frozen FAF source')
    # Source/path/output admission above precedes every helper write.
    out.mkdir(parents=True, exist_ok=True)
    calls = []
    original = fastbuild.run_compiler
    record = {'purpose': 'Diagnostic capture only; no source gain or IR editing.',
              'symbol': SYMBOL, 'sourceSha256': source['sha256'],
              'rootAdditionalArguments': list(ROOT_ARGUMENTS),
              'rootOnlyCargoRustcArguments': True, 'calls': calls,
              'environmentScope': 'Only explicit compiler/linker environment keys; inherited environment is not dumped.',
              'rustMirDump': 'Not requested: no scoped Rust-MIR dump option qualified.',
              'compilerCompleted': False, 'buildOk': False, 'captureComplete': False}
    def save():
        path = out / 'capture-result.json'
        require(not path.is_symlink() and (not path.exists() or
                (path.is_file() and path.stat().st_nlink == 1)), 'unsafe capture receipt output')
        with path.open('w' if path.exists() else 'x', encoding='utf-8') as stream:
            stream.write(json.dumps(record, indent=2) + '\n')
    def hook(command, *positional, **keywords):
        require(not calls, 'diagnostic permits exactly one compiler command')
        expected = [str(fastbuild.SDK / 'rust/bin/cargo'), 'build', '--manifest-path',
                    str(work / 'ws/programs/pump/Cargo.toml'), '--release',
                    '--target', 'sbpf-solana-solana', '--locked', '--offline']
        require(command == expected and keywords.get('cwd') == work / 'ws',
                'compiler command/cwd differs from frozen identity build')
        environment = keywords.get('env', {})
        require(environment.get('CARGO_TARGET_SBPF_SOLANA_SOLANA_RUSTFLAGS') == '-Zremap-cwd-prefix='
                and 'RUSTFLAGS' not in environment and 'CARGO_ENCODED_RUSTFLAGS' not in environment,
                'maintained identity compiler flags differ')
        require(environment.get('RUSTC') == str(fastbuild.RECIPES['identity']['rustc'])
                and environment.get('RUSTC_WRAPPER') == str(fastbuild.H / 'pump_link_rustc.sh')
                and environment.get('CARGO_TARGET_DIR') == str(work / 'target-identity'),
                'maintained identity compiler/wrapper/target path differs')
        fastbuild.assert_unchanged(src, source)
        transformed = rewrite_command(command)
        calls.append({'originalArgv': list(command), 'diagnosticArgv': transformed,
                      'argvDelta': {'replacedIndex': 1, 'from': 'build', 'to': 'rustc',
                                    'appended': ['--lib', '--', *ROOT_ARGUMENTS]},
                      'cwd': str(keywords['cwd']),
                      'compilerEnvironment': {key: environment.get(key) for key in ENVIRONMENT_KEYS},
                      'originalKeywordNames': sorted(keywords), 'timeout': keywords.get('timeout'),
                      'originalPositionalCount': len(positional)})
        save()
        # Preserve every original argument and keyword, including timeout and env.
        return original(transformed, *positional, **keywords)
    result, failure = None, None
    save()
    try:
        fastbuild.run_compiler = hook
        result = fastbuild.build(src, work, out, recipe='identity')
        record['compilerCompleted'] = True
        record['buildOk'] = result.get('ok', False)
        require(len(calls) == 1, 'actual compiler boundary count differs from one')
    except BaseException as error:
        failure = error
        record['error'] = {'type': type(error).__name__, 'message': str(error)}
    finally:
        fastbuild.run_compiler = original
        try:
            record.update(collect(out, work))
            fastbuild.assert_unchanged(src, source)
            record['sourceUnchanged'] = True
        except BaseException as error:
            record['collectionError'] = {'type': type(error).__name__, 'message': str(error)}
            if failure is None:
                failure = error
        record['captureComplete'] = bool(record['buildOk'] and record.get('sourceUnchanged')
                and record.get('rawBuildLogPresent') and record.get('targetDefinitionRetained')
                and record.get('allRequestedStagesObserved') and len(calls) == 1 and failure is None)
        save()
    if failure is not None:
        raise failure
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--src', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--recipe', choices=['identity'], required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[4]
    harness = root / 'reconstruction/harness'
    sys.path.insert(0, str(harness))
    try:
        spec = importlib.util.spec_from_file_location('diagnostic_fastbuild', harness / 'fastbuild.py')
        fastbuild = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fastbuild)
    finally:
        sys.path.pop(0)
    result = capture(fastbuild, args.src, args.work, args.out, root / 'programs/pump')
    print(json.dumps(result, indent=2))
    # Build success still reaches the official scorer even if capture is incomplete.
    # The controller separately rejects incomplete diagnostic attribution.
    return 0 if result.get('ok') else 1


if __name__ == '__main__':
    raise SystemExit(main())
