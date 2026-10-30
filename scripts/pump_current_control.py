"""One cold build of the unchanged 1cacecfb Pump crate with the maintained identity recipe."""
from pathlib import Path
import datetime
import hashlib
import importlib.util
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import urllib.request

BASE = '1cacecfbf9a58b698f99d5e11d6723a254588b81'
ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'work/pump-current-identity/evidence'
WORK = Path(os.environ['RUNNER_TEMP']) / 'pump-current-identity-work'
SDKROOT = Path.home() / '.cache/solana'

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def write(name, value):
    (EVIDENCE / name).write_text(json.dumps(value, indent=2) + '\n')

def run(name, args, env=None):
    args = [str(x) for x in args]
    with (EVIDENCE / (name + '.log')).open('w') as stream:
        result = subprocess.run(args, cwd=ROOT, env=env, stdout=stream, stderr=subprocess.STDOUT)
    with (EVIDENCE / 'commands.jsonl').open('a') as stream:
        stream.write(json.dumps({'name': name, 'command': args, 'returncode': result.returncode}) + '\n')
    if result.returncode:
        print((EVIDENCE / (name + '.log')).read_text()[-16000:], flush=True)
    result.check_returncode()

def source_manifest(prefixes=('programs/pump',)):
    rows = subprocess.check_output(['git', 'ls-tree', '-rz', BASE, *prefixes], cwd=ROOT).split(b'\0')
    manifest = []
    for row in rows:
        if not row:
            continue
        meta, path = row.split(b'\t', 1)
        mode, kind, oid = meta.split()
        assert kind == b'blob'
        name = os.fsdecode(path)
        file = ROOT / name
        data = os.fsencode(os.readlink(file)) if mode == b'120000' else file.read_bytes()
        observed = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert observed == oid.decode(), name
        manifest.append({'path': name, 'mode': mode.decode(), 'gitBlob': observed, 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
    return manifest

def registry_manifest():
    root = Path.home() / '.cargo/registry/src'
    return {str(p.relative_to(root)): sha(p) for p in sorted(root.rglob('*')) if p.is_file()}

def install_sdk(version, expected_archive=None):
    archive = Path(os.environ['RUNNER_TEMP']) / ('platform-tools-' + version + '.tar.bz2')
    url = 'https://github.com/anza-xyz/platform-tools/releases/download/' + version + '/platform-tools-osx-aarch64.tar.bz2'
    with urllib.request.urlopen(url, timeout=180) as response, archive.open('wb') as stream:
        shutil.copyfileobj(response, stream)
    digest = sha(archive)
    if expected_archive:
        assert digest == expected_archive, version
    destination = SDKROOT / version / 'platform-tools'
    assert not destination.exists(), 'Cold SDK directory unexpectedly present'
    destination.mkdir(parents=True)
    with tarfile.open(archive) as source:
        source.extractall(destination, filter='data')
    archive.unlink()
    return {'version': version, 'url': url, 'archiveSha256': digest, 'expectedArchiveSha256': expected_archive, 'sdk': str(destination)}

def main():
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    assert platform.system() == 'Darwin' and platform.machine() == 'arm64', platform.platform()
    assert not WORK.exists(), 'Build target must begin empty'
    source = source_manifest()
    write('source-inputs.json', {'base': BASE, 'files': source})
    core_paths = ('reconstruction/harness', 'reconstruction/toolchain', 'reconstruction/base', 'reconstruction/pump-main/baseline', 'evidence/original/pump')
    core = source_manifest(core_paths)
    write('toolchain-source-inputs.json', {'base': BASE, 'files': core})
    baseline = ROOT / 'reconstruction/pump-main/baseline/score.json'
    assert baseline.is_file(), 'The explicit historical baseline is required'
    write('baseline-input.json', {'path': str(baseline.relative_to(ROOT)), 'sha256': sha(baseline), 'role': 'Historical comparison only; current counts come from a fresh full census.'})
    write('host.json', {'platform': platform.platform(), 'machine': platform.machine(), 'python': sys.version, 'base': BASE})
    downloads = [install_sdk('v1.44')]
    write('sdk-downloads.json', downloads)
    # The unchanged official scorer names this exact analysis-tool installation.
    downloads.append(install_sdk('v1.52', '1727dfb31e833ce777d01e70cb4b3cebd26b376bf09d80527f02457d4cf6fd00'))
    write('sdk-downloads.json', downloads)
    sdk = SDKROOT / 'v1.44/platform-tools'
    env = dict(os.environ)
    env['PUMP_RECON_HOME'] = str(Path(os.environ['RUNNER_TEMP']) / 'pump-current-identity-cache')
    env['PUMP_BUILD_SLOTS'] = '1'
    env['CARGO_BUILD_JOBS'] = '2'
    env['PUMP_OBJDUMP'] = str(SDKROOT / 'v1.52/platform-tools/llvm/bin/llvm-objdump')
    assert not Path(env['PUMP_RECON_HOME']).exists(), 'Identity cache must begin empty'
    write('controller-inputs.json', {'checkout': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(), 'runnerSha256': sha(__file__), 'workflowSha256': sha(ROOT / '.github/workflows/qualify-pump-macos-v144.yml'), 'recipe': 'identity', 'triple': 'sbpf-solana-solana', 'documentedEnvironment': {key: env[key] for key in ['PUMP_RECON_HOME', 'PUMP_BUILD_SLOTS', 'CARGO_BUILD_JOBS', 'PUMP_OBJDUMP']}})
    # Full inventory verification includes all compiler bytes, symlinks and Linux target-library hashes.
    run('bootstrap-before', [sys.executable, '-B', ROOT / 'reconstruction/toolchain/bootstrap.py', '--sdk-check', 'full'], env)
    harness = ROOT / 'reconstruction/harness'
    spec = importlib.util.spec_from_file_location('current_fastbuild', harness / 'fastbuild.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.stage(ROOT / 'programs/pump', WORK / 'ws')
    staged = {str(p.relative_to(WORK / 'ws')): {'sha256': sha(p), 'bytes': p.stat().st_size} for p in sorted((WORK / 'ws').rglob('*')) if p.is_file()}
    write('compiled-workspace-inputs.json', staged)
    with tarfile.open(EVIDENCE / 'compiled-workspace.tar.gz', 'w:gz') as archive:
        for name in staged:
            archive.add(WORK / 'ws' / name, arcname=name, recursive=False)
    fetch_env = dict(env, RUSTC=str(sdk / 'rust/bin/rustc'))
    fetch_env['PATH'] = str(sdk / 'rust/bin') + os.pathsep + env['PATH']
    run('fetch-locked', [sdk / 'rust/bin/cargo', 'fetch', '--locked', '--manifest-path', WORK / 'ws/Cargo.toml'], fetch_env)
    registry_before = registry_manifest()
    write('registry-source-inputs.json', registry_before)
    assert not (Path(env['PUMP_RECON_HOME']) / 'template-target-sbpf').exists(), 'Cold target cannot use a warm template'
    # The child process imports the maintained builder normally with only its documented cache/slot environment.
    run('cold-build', [sys.executable, '-B', harness / 'fastbuild.py', '--src', ROOT / 'programs/pump', '--work', WORK, '--out', EVIDENCE, '--recipe', 'identity'], env)
    build_text = (EVIDENCE / 'cold-build.log').read_text()
    build_results = []
    for marker in re.finditer(r'(?m)^\{', build_text):
        try:
            value, _ = json.JSONDecoder().raw_decode(build_text[marker.start():])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and 'runtime_valid' in value and 'unstripped_sha256' in value:
            build_results.append(value)
    assert len(build_results) == 1, 'Expected exactly one actual builder result'
    build = build_results[0]
    write('build.json', build)
    assert build['ok'] and build['runtime_valid'] and not build['stack_warnings'], 'Runtime-invalid stack build'
    assert build['recipe'] == 'identity' and build['triple'] == 'sbpf-solana-solana'
    assert build['unstripped_sha256'] == sha(EVIDENCE / 'unstripped.so') and build['candidate_sha256'] == sha(EVIDENCE / 'candidate.so')
    run('bootstrap-after', [sys.executable, '-B', ROOT / 'reconstruction/toolchain/bootstrap.py', '--sdk-check', 'full'], env)
    assert source_manifest() == source, 'Program source changed'
    assert source_manifest(core_paths) == core, 'Maintained harness, target libraries or original inputs changed'
    assert registry_manifest() == registry_before, 'Registry source changed'
    run('score', [sys.executable, '-B', harness / 'score.py', EVIDENCE / 'unstripped.so', '--baseline', baseline, '--json', EVIDENCE / 'score.json'], env)
    score = json.loads((EVIDENCE / 'score.json').read_text())['summary']
    tools = {str(p.relative_to(ROOT)): sha(p) for p in harness.glob('*') if p.is_file()}
    tools.update({str(p): sha(p) for p in [sdk / 'rust/bin/rustc', Path(env['PUMP_RECON_HOME']) / 'toolchains/hybrid144/rust/bin/rustc', sdk / 'rust/bin/cargo', sdk / 'llvm/bin/llvm-objcopy', SDKROOT / 'v1.52/platform-tools/llvm/bin/llvm-objdump']})
    write('tool-inputs.json', tools)
    with tarfile.open(EVIDENCE / 'program-source.tar.gz', 'w:gz') as archive:
        for row in source:
            archive.add(ROOT / row['path'], arcname=row['path'], recursive=False)
    assert score['total'] == 1035
    result = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'base': BASE, 'sourceUnchanged': True, 'registrySourceUnchanged': True, 'coldTarget': True, 'summary': score, 'unstrippedSha256': sha(EVIDENCE / 'unstripped.so'), 'candidateSha256': sha(EVIDENCE / 'candidate.so'), 'limits': 'One unchanged current-source identity control; no new source proposal, window gain, runtime behavior or whole-original-ELF equality claim.'}
    write('RESULT.json', result)
    print(json.dumps(result, indent=2), flush=True)

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        EVIDENCE.mkdir(parents=True, exist_ok=True)
        write('FAILURE.json', {'type': type(error).__name__, 'message': str(error), 'base': BASE})
        raise
