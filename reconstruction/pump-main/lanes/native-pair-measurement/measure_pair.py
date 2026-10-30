"""Measure exactly one frozen Pump control/candidate pair; no source proposals.

Derived from qualified control e7ed2474df380c81d55b822515055c953f0947117d28ef5bb783355d4f415c2e.
--preflight-only authenticates and stages inputs without SDK/bootstrap/Cargo calls.
"""
import argparse
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import urllib.request

ROOT = Path(__file__).resolve().parents[4]
CORE = ('reconstruction/harness', 'reconstruction/toolchain', 'reconstruction/base',
        'reconstruction/pump-main/baseline', 'evidence/original/pump')
ALLOWED = ('programs/pump/src/buy_v2.rs', 'programs/pump/src/creator/admin_cto.rs',
           'programs/pump/src/multi_hop_curve_swap.rs')
WORKFLOW = '.github/workflows/qualify-pump-macos-v144.yml'
OPERATIONAL = (WORKFLOW, 'reconstruction/pump-main/lanes/native-pair-measurement/README.md',
               'reconstruction/pump-main/lanes/native-pair-measurement/measure_pair.py')
SDKROOT = Path.home() / '.cache/solana'
SDK_ARCHIVES = {
    'v1.44': '66e20d135fddd70ff519baf7ff320d762957f9aedf93a50e23756db23ad79351',
    'v1.52': '1727dfb31e833ce777d01e70cb4b3cebd26b376bf09d80527f02457d4cf6fd00',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def commit_id(value):
    if not re.fullmatch('[0-9a-f]{40}', value):
        raise argparse.ArgumentTypeError('expected an exact lowercase 40-hex commit')
    return value


def git(*args):
    return subprocess.check_output(['git', *map(str, args)], cwd=ROOT)


def entries(commit, prefixes):
    result = []
    for row in git('ls-tree', '-rz', commit, '--', *prefixes).split(b'\0'):
        if not row:
            continue
        meta, name = row.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        require(kind == 'blob' and mode in ('100644', '100755', '120000'),
                'unsupported Git input kind/mode')
        path = name.decode('utf-8')
        require(not Path(path).is_absolute() and '..' not in Path(path).parts,
                'unsafe Git input path')
        data = git('cat-file', 'blob', oid)
        result.append({'path': path, 'mode': mode, 'gitBlob': oid,
                       'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    require(bool(result), 'empty Git input vector')
    return result


def verify_files(root, rows):
    for row in rows:
        path = root / row['path']
        if row['mode'] == '120000':
            require(path.is_symlink(), 'missing Git symlink: ' + row['path'])
            data = os.fsencode(os.readlink(path))
        else:
            require(path.is_file() and not path.is_symlink(), 'nonregular input: ' + row['path'])
            require(bool(path.stat().st_mode & 0o111) == (row['mode'] == '100755'),
                    'input executable mode differs: ' + row['path'])
            data = path.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        require(blob == row['gitBlob'] and len(data) == row['bytes']
                and hashlib.sha256(data).hexdigest() == row['sha256'],
                'input changed: ' + row['path'])


def verify_core(rows):
    verify_files(ROOT, rows)
    actual = {p.relative_to(ROOT).as_posix() for prefix in CORE
              for p in (ROOT / prefix).rglob('*') if p.is_file() or p.is_symlink()}
    require(actual == {x['path'] for x in rows}, 'maintained input file set differs from Git')


def file_vector(root):
    rows = {}
    for path in sorted(root.rglob('*')):
        require(not path.is_symlink(), 'unexpected staged symlink')
        if path.is_file():
            rows[path.relative_to(root).as_posix()] = {
                'bytes': path.stat().st_size, 'executable': bool(path.stat().st_mode & 0o111),
                'sha256': sha(path)}
    return rows


def archive(path, root, names):
    with tarfile.open(path, 'w:gz') as output:
        for name in names:
            output.add(root / name, arcname=name, recursive=False)


def registry_manifest():
    root = Path.home() / '.cargo/registry/src'
    return {p.relative_to(root).as_posix(): sha(p) for p in sorted(root.rglob('*')) if p.is_file()}


class Pair:
    def __init__(self, args):
        self.args = args
        self.work = args.work.resolve()
        self.output = args.output.resolve()
        self.core = []
        self.cohorts = []
        self.output_created = False

    def write(self, name, value):
        path = self.output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')

    def run(self, name, command, env, check=True):
        command = list(map(str, command))
        log = self.output / (name + '.log')
        log.parent.mkdir(parents=True, exist_ok=True)
        with log.open('wb') as stream:
            result = subprocess.run(command, cwd=ROOT, env=env, stdout=stream,
                                    stderr=subprocess.STDOUT)
        with (self.output / 'commands.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps({'name': name, 'command': command,
                                     'returncode': result.returncode}) + '\n')
        if check:
            if result.returncode:
                print(log.read_text(errors='replace')[-16000:], flush=True)
            result.check_returncode()
        return result.returncode

    def validate_pair(self):
        a = self.args
        require(a.source_base != a.candidate, 'control and candidate commits must differ')
        for commit in (a.source_base, a.candidate):
            require(git('cat-file', '-t', commit).strip() == b'commit', 'input must be a commit')
        # Raw commit headers retain parent identity even after a shallow fetch.
        headers = git('cat-file', '-p', a.candidate).split(b'\n\n', 1)[0].splitlines()
        parents = [x[7:].decode() for x in headers if x.startswith(b'parent ')]
        require(parents == [a.source_base], 'candidate must have exactly source-base as its parent')
        changed = git('diff', '--no-ext-diff', '--no-textconv', '--no-renames',
                      '--name-status', a.source_base, a.candidate).decode().splitlines()
        require(changed == ['M\t' + a.changed_source_path],
                'candidate must change only the selected existing Rust source')
        for commit in (a.source_base, a.candidate):
            data = git('show', commit + ':' + a.changed_source_path)
            data.decode('utf-8')
            require(b'\0' not in data, 'Rust source must be text')
            require(git('ls-tree', commit, '--', a.changed_source_path).startswith(b'100644 blob '),
                    'selected Rust source must retain regular nonexecutable mode')
        checkout = git('rev-parse', 'HEAD').decode().strip()
        checkout_changes = git('diff', '--no-ext-diff', '--no-textconv', '--no-renames',
                               '--name-only', a.source_base, checkout).decode().splitlines()
        require(set(checkout_changes) <= set(OPERATIONAL),
                'operational checkout must differ from source-base only in the three driver files')
        self.operational = entries(checkout, OPERATIONAL)
        require({x['path'] for x in self.operational} == set(OPERATIONAL),
                'all operational files must be committed in the checkout')
        verify_files(ROOT, self.operational)
        self.core = entries(a.source_base, CORE)
        verify_core(self.core)
        require((ROOT / 'reconstruction/pump-main/baseline/score.json').is_file(),
                'explicit historical baseline is required before staging or SDK setup')
        protected = [ROOT / 'programs/pump', *[ROOT / p for p in CORE]]
        for location in (self.work, self.output):
            require(not location.exists() and not location.is_symlink(),
                    'work and evidence paths must start absent')
            require(not any(location == p or location in p.parents or p in location.parents
                            for p in protected), 'work/output overlaps immutable inputs')
        require(not (self.work == self.output or self.work in self.output.parents
                     or self.output in self.work.parents), 'work and evidence paths must be separate')

    def prepare(self):
        self.validate_pair()
        self.work.mkdir(parents=True)
        self.output.mkdir(parents=True)
        self.output_created = True
        a = self.args
        self.write('pair-inputs.json', {'sourceBase': a.source_base, 'candidate': a.candidate,
                   'changedSourcePath': a.changed_source_path,
                   'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   'operationalCheckout': git('rev-parse', 'HEAD').decode().strip(),
                   'controllerSha256': sha(__file__), 'workflowSha256': sha(ROOT / WORKFLOW),
                   'recipe': 'identity', 'triple': 'sbpf-solana-solana',
                   'preflightOnly': a.preflight_only})
        self.write('maintained-inputs.json', {'base': a.source_base, 'files': self.core})
        self.write('operational-inputs.json', {'checkout': git('rev-parse', 'HEAD').decode().strip(),
                                             'files': self.operational})
        patch = git('diff', '--no-ext-diff', '--no-textconv', '--no-renames', '--binary',
                    a.source_base, a.candidate, '--', a.changed_source_path)
        (self.output / 'candidate.patch').write_bytes(patch)
        harness = ROOT / 'reconstruction/harness'
        sys.path.insert(0, str(harness))
        try:
            spec = importlib.util.spec_from_file_location('pair_fastbuild', harness / 'fastbuild.py')
            builder = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(builder)
        finally:
            sys.path.pop(0)
        for label, commit in [('control', a.source_base), ('candidate', a.candidate)]:
            rows = entries(commit, ('programs/pump',))
            source_root = self.work / 'sources' / label
            for row in rows:
                require(row['mode'] != '120000', 'program source symlinks are unsupported')
                target = source_root / row['path']
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(git('cat-file', 'blob', row['gitBlob']))
                target.chmod(0o755 if row['mode'] == '100755' else 0o644)
            verify_files(source_root, rows)
            source = source_root / 'programs/pump'
            expected = [{'path': x['path'].removeprefix('programs/pump/'), 'bytes': x['bytes'],
                         'executable': x['mode'] == '100755', 'sha256': x['sha256']} for x in rows]
            expected.sort(key=lambda x: x['path'])
            snapshot = builder.snapshot(source)
            require(snapshot['files'] == expected, 'builder snapshot omits or changes a Git source input')
            work = self.work / 'builds' / label
            require(not work.exists(), 'each cohort work tree must begin empty')
            builder.stage(source, work / 'ws')
            staged = file_vector(work / 'ws')
            require(len(staged) == len(rows) + 1, 'unexpected staged workspace file count')
            folder = self.output / label
            folder.mkdir()
            self.write(label + '/program-source-inputs.json', {'commit': commit, 'files': rows})
            self.write(label + '/preflight-builder-source-inputs.json', snapshot)
            self.write(label + '/compiled-workspace-inputs.json', staged)
            archive(folder / 'program-source.tar.gz', source_root, [x['path'] for x in rows])
            archive(folder / 'compiled-workspace.tar.gz', work / 'ws', staged)
            self.write(label + '/archives.json', {
                name: {'sha256': sha(folder / name), 'bytes': (folder / name).stat().st_size}
                for name in ('program-source.tar.gz', 'compiled-workspace.tar.gz')})
            self.cohorts.append({'label': label, 'commit': commit, 'sourceRoot': source_root,
                                 'source': source, 'rows': rows, 'snapshot': snapshot,
                                 'work': work, 'staged': staged, 'folder': folder,
                                 'linkInputs': self.link_preflight(builder.link_order, source, work, folder, rows)})
        before, after = [x['staged'] for x in self.cohorts]
        require(set(before) == set(after), 'staged workspace file set changed')
        require([p for p in before if before[p] != after[p]] == [a.changed_source_path],
                'staging changed inputs beyond the authorized Rust file')
        self.assert_sources()
        self.write('PREFLIGHT.json', {'sourceBase': a.source_base, 'candidate': a.candidate,
                   'changedSourcePath': a.changed_source_path,
                   'sourceFiles': [len(x['rows']) for x in self.cohorts],
                   'workspaceFiles': [len(x['staged']) for x in self.cohorts],
                   'sdkInstalledByPreflight': False, 'bootstrapRunByPreflight': False,
                   'cargoRunByPreflight': False, 'compilerRunByPreflight': False})

    def link_preflight(self, linker, source, work, folder, rows):
        # Pure admitted-script parsing only. configure() requires the real SDK and
        # is intentionally left exclusively to the maintained actual builder.
        script = source / 'link/ordered.ld'
        require(script.is_file() and not script.is_symlink(), 'frozen source requires ordered link script')
        counts = linker.check_script(script.read_text())
        program = next(x for x in rows if x['path'] == 'programs/pump/link/ordered.ld')
        files = {}
        retained = folder / 'pinned-link-inputs'
        retained.mkdir()
        shutil.copy2(script, retained / 'ordered.ld')
        for name in ('link_order.py', 'pump_link_rustc.py', 'pump_link_lld.py', 'sbf_default.ld'):
            relative = 'reconstruction/harness/' + name
            row = next(x for x in self.core if x['path'] == relative)
            files[name] = row
            shutil.copy2(ROOT / relative, retained / name)
            require(sha(retained / name) == row['sha256'], 'retained link input differs')
        record = {'programScript': program, 'maintainedInputs': files, 'selectors': counts,
                  'stagedScriptSha256': sha(work / 'ws/programs/pump/link/ordered.ld'),
                  'configureExecutedByPreflight': False}
        require(record['stagedScriptSha256'] == program['sha256'], 'staged linker script differs')
        self.write(folder.relative_to(self.output).as_posix() + '/link-inputs.json', record)
        return record

    def lld_input(self, env):
        sdk = SDKROOT / 'v1.44/platform-tools'
        paths = sorted((Path(env['PUMP_RECON_HOME']) / 'toolchains/hybrid144/rust').glob(
            'lib/rustlib/*/bin/rust-lld'))
        require(len(paths) == 1, 'expected exactly one native hybrid rust-lld')
        lld = paths[0]
        resolved = lld.resolve(strict=True)
        require(resolved.is_relative_to(sdk.resolve()), 'hybrid rust-lld is not from the authenticated native SDK')
        relative = resolved.relative_to(sdk.resolve()).as_posix()
        inventory = json.loads((ROOT / 'reconstruction/toolchain/v1.44-macos-inventory.json').read_text())['entries']
        expected = inventory[relative]
        require(expected['type'] == 'file' and sha(lld) == expected['sha256']
                and resolved.stat().st_size == expected['bytes']
                and stat.S_IMODE(resolved.stat().st_mode) == int(expected['mode'], 8),
                'native rust-lld bytes/mode differ from the full SDK inventory')
        return {'path': str(lld), 'resolvedPath': str(resolved), 'sdkRelativePath': relative,
                'sha256': sha(lld), 'bytes': resolved.stat().st_size,
                'mode': oct(stat.S_IMODE(resolved.stat().st_mode))}

    def verify_link_result(self, cohort, build, native_lld):
        folder, work, inputs = cohort['folder'], cohort['work'], cohort['linkInputs']
        expected = {'script': 'link/ordered.ld', 'script_sha256': inputs['programScript']['sha256'],
                    'selectors': inputs['selectors'], 'lld_sha256': native_lld['sha256']}
        require(build.get('link_order') == expected, 'actual builder link_order differs from frozen inputs')
        receipt = folder / 'link-receipt.json'
        link_map = folder / 'link.map'
        require(receipt.is_file() and link_map.is_file() and link_map.stat().st_size > 0,
                'actual link receipt/map missing')
        require(receipt.read_bytes() == (work / 'link-receipt.json').read_bytes()
                and link_map.read_bytes() == (work / 'link.map').read_bytes(),
                'builder copied another link receipt/map')
        actual = json.loads(receipt.read_text())
        script = (work / 'ws/programs/pump/link/ordered.ld').resolve()
        require(actual['script'] == str(script) and sha(script) == expected['script_sha256']
                and actual['script_sha256'] == expected['script_sha256']
                and actual['default_script_sha256'] == inputs['maintainedInputs']['sbf_default.ld']['sha256']
                and actual['lld'] == native_lld['path'] and actual['lld_sha256'] == native_lld['sha256'],
                'actual linker receipt source/default/native-LLD binding differs')
        argv = actual['forwarded']
        scripts = [argv[i+1] for i,v in enumerate(argv[:-1]) if v in ('-T','--script')]
        require(scripts == [str(script)] and argv.count('-Map=' + str(work / 'link.map')) == 1,
                'actual linker did not forward the single frozen script/map')
        self.write(cohort['label'] + '/link-order-admission.json', {
            'actualBuildLinkOrder': build['link_order'], 'receiptSha256': sha(receipt),
            'mapSha256': sha(link_map), 'mapBytes': link_map.stat().st_size,
            'nativeLld': native_lld, 'frozenProgramScript': inputs['programScript'],
            'frozenDefaultScript': inputs['maintainedInputs']['sbf_default.ld']})

    def assert_sources(self):
        verify_core(self.core)
        verify_files(ROOT, self.operational)
        for cohort in self.cohorts:
            verify_files(cohort['sourceRoot'], cohort['rows'])
            require(file_vector(cohort['work'] / 'ws') == cohort['staged'],
                    'compiled workspace inputs changed')

    def install_sdk(self, version):
        destination = SDKROOT / version / 'platform-tools'
        require(not destination.exists(), 'SDK installation must begin absent')
        path = self.work / ('platform-tools-' + version + '.tar.bz2')
        url = ('https://github.com/anza-xyz/platform-tools/releases/download/' + version
               + '/platform-tools-osx-aarch64.tar.bz2')
        with urllib.request.urlopen(url, timeout=180) as response, path.open('wb') as stream:
            shutil.copyfileobj(response, stream)
        require(sha(path) == SDK_ARCHIVES[version], 'official SDK archive differs')
        destination.mkdir(parents=True)
        with tarfile.open(path) as source:
            source.extractall(destination, filter='data')
        path.unlink()
        return {'version': version, 'url': url, 'archiveSha256': SDK_ARCHIVES[version],
                'sdk': str(destination), 'role': 'compiler' if version == 'v1.44' else 'analysis only'}

    def tool_inputs(self, env):
        sdk = SDKROOT / 'v1.44/platform-tools'
        paths = [sdk / 'rust/bin/rustc', sdk / 'rust/bin/cargo', sdk / 'llvm/bin/llvm-objcopy',
                 Path(env['PUMP_RECON_HOME']) / 'toolchains/hybrid144/rust/bin/rustc',
                 SDKROOT / 'v1.52/platform-tools/llvm/bin/llvm-objdump']
        paths.append(Path(self.lld_input(env)['path']))
        paths += sorted((sdk / 'rust/lib').glob('lib*.dylib'))
        return {str(p): sha(p) for p in paths}

    def measure(self):
        env = dict(os.environ)
        env.update(PUMP_RECON_HOME=str(self.work / 'identity-cache'), PUMP_BUILD_SLOTS='1',
                   CARGO_BUILD_JOBS='2', PUMP_OBJDUMP=str(SDKROOT / 'v1.52/platform-tools/llvm/bin/llvm-objdump'))
        cache = Path(env['PUMP_RECON_HOME'])
        require(not cache.exists(), 'shared pair cache must begin empty')
        require(all(not (SDKROOT / version / 'platform-tools').exists() for version in SDK_ARCHIVES),
                'both qualified SDK installations must begin absent')
        self.write('host.json', {'platform': platform.platform(), 'machine': platform.machine(),
                                'python': sys.version})
        downloads = []
        for version in SDK_ARCHIVES:
            downloads.append(self.install_sdk(version))
            self.write('sdk-downloads.json', downloads)
        self.write('documented-environment.json', {k: env[k] for k in
                   ['PUMP_RECON_HOME', 'PUMP_BUILD_SLOTS', 'CARGO_BUILD_JOBS', 'PUMP_OBJDUMP']})
        bootstrap = ROOT / 'reconstruction/toolchain/bootstrap.py'
        harness = ROOT / 'reconstruction/harness'
        self.run('bootstrap-before', [sys.executable, '-B', bootstrap, '--sdk-check', 'full'], env)
        native_lld = self.lld_input(env)
        self.write('native-lld-input-before.json', native_lld)
        tools = self.tool_inputs(env)
        self.write('tool-inputs-before.json', tools)
        baseline = ROOT / 'reconstruction/pump-main/baseline/score.json'
        require(baseline.is_file(), 'explicit historical baseline is required')
        self.write('historical-baseline-input.json', {'path': str(baseline.relative_to(ROOT)),
                   'sha256': sha(baseline), 'role': 'Control reporting only; candidate uses fresh control.'})
        sdk = SDKROOT / 'v1.44/platform-tools'
        fetch_env = dict(env, RUSTC=str(sdk / 'rust/bin/rustc'))
        fetch_env['PATH'] = str(sdk / 'rust/bin') + os.pathsep + env['PATH']
        self.run('fetch-locked', [sdk / 'rust/bin/cargo', 'fetch', '--locked', '--manifest-path',
                 self.cohorts[0]['work'] / 'ws/Cargo.toml'], fetch_env)
        registry = registry_manifest()
        self.write('registry-source-inputs-before.json', registry)
        self.assert_sources()
        for cohort in self.cohorts:
            label, folder, work = cohort['label'], cohort['folder'], cohort['work']
            require(not (work / 'target-identity').exists(), 'cohort target must be cold')
            require(not (cache / 'template-target-sbpf').exists()
                    and not (cache / 'template-target').exists(), 'warm targets are forbidden')
            self.write(label + '/cold-target-inputs.json', {
                'commit': cohort['commit'], 'sourceSha256': cohort['snapshot']['sha256'],
                'target': str(work / 'target-identity'), 'targetAbsentBeforeBuild': True,
                'dependencyTemplatesAbsent': True, 'toolInputs': tools})
            self.run(label + '/cold-build', [sys.executable, '-B', harness / 'fastbuild.py',
                     '--src', cohort['source'], '--work', work, '--out', folder,
                     '--recipe', 'identity'], env)
            text = (folder / 'cold-build.log').read_text()
            values = []
            for marker in re.finditer(r'(?m)^\{', text):
                try:
                    value, _ = json.JSONDecoder().raw_decode(text[marker.start():])
                except json.JSONDecodeError:
                    continue
                if isinstance(value, dict) and 'unstripped_sha256' in value:
                    values.append(value)
            require(len(values) == 1, 'expected one actual builder result')
            build = values[0]
            self.write(label + '/build.json', build)
            require(build['ok'] and build['runtime_valid'] and not build['stack_warnings'],
                    'runtime-invalid or failed build')
            require(build['recipe'] == 'identity' and build['triple'] == 'sbpf-solana-solana',
                    'compiler recipe changed')
            require(build['unstripped_sha256'] == sha(folder / 'unstripped.so')
                    and build['candidate_sha256'] == sha(folder / 'candidate.so'), 'ELF hash differs')
            self.verify_link_result(cohort, build, native_lld)
            receipt = json.loads((folder / 'source-inputs.json').read_text())
            require(receipt == cohort['snapshot'] and receipt['sha256'] == build['source_sha256'],
                    'Git and actual builder source receipts differ')
            log = (folder / 'build.log').read_text()
            for package in ('pump-recovered', 'pump-token-ext'):
                require(re.search(r'(?m)^\s*Compiling ' + package + r' v', log),
                        'missing fresh local compilation: ' + package)
            fingerprints = {}
            for package in ('pump-recovered', 'pump-token-ext'):
                paths = list((work / 'target-identity').glob(
                    'sbpf-solana-solana/release/.fingerprint/' + package + '-*/*.json'))
                require(bool(paths), 'target Cargo fingerprint receipt missing: ' + package)
                for path in paths:
                    value = json.loads(path.read_text())
                    require(value.get('rustflags') == ['-Zremap-cwd-prefix='],
                            'actual target compiler flags differ: ' + package)
                    fingerprints[path.relative_to(work).as_posix()] = value
            self.write(label + '/cargo-fingerprints.json', fingerprints)
            self.run('bootstrap-after-' + label,
                     [sys.executable, '-B', bootstrap, '--sdk-check', 'full'], env)
            self.assert_sources()
            require(registry_manifest() == registry, 'registry source changed')
            require(self.tool_inputs(env) == tools, 'compiler/tool files changed')
            require(self.lld_input(env) == native_lld, 'native rust-lld binding changed')
            self.write(label + '/native-lld-input-after.json', self.lld_input(env))
            self.write(label + '/tool-inputs-after.json', self.tool_inputs(env))
            self.write(label + '/registry-source-inputs-after.json', registry_manifest())
            score_baseline = baseline if label == 'control' else self.output / 'control/score.json'
            self.run(label + '/score', [sys.executable, '-B', harness / 'score.py',
                     folder / 'unstripped.so', '--baseline', score_baseline,
                     '--json', folder / 'score.json'], env)
            scored = json.loads((folder / 'score.json').read_text())
            require(scored['summary']['total'] == len(scored['windows']) == 1035,
                    'incomplete official census')
            require(scored['summary']['candidate_sha256'] == build['unstripped_sha256'],
                    'scorer used another ELF')
        code = self.run('compare-scores', [sys.executable, '-B', harness / 'compare_scores.py',
                        self.output / 'control/score.json', self.output / 'candidate/score.json',
                        '--json', self.output / 'comparison.json'], env, check=False)
        require(code in (0, 1), 'invalid full score comparison')
        comparison = json.loads((self.output / 'comparison.json').read_text())
        require(comparison['accepted'] == (code == 0), 'comparison exit/result mismatch')
        self.assert_sources()
        require(registry_manifest() == registry, 'registry source changed during scoring')
        require(self.tool_inputs(env) == tools, 'compiler/tool files changed during scoring')
        original = ROOT / 'evidence/original/pump/deployed.so'
        whole_files = {label: {name: {'sha256': sha(self.output / label / name),
                                      'bytes': (self.output / label / name).stat().st_size}
                               for name in ('unstripped.so', 'candidate.so')}
                       for label in ('control', 'candidate')}
        self.write('PAIR-RESULT.json', {'sourceBase': self.args.source_base, 'candidate': self.args.candidate,
                   'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   'changedSourcePath': self.args.changed_source_path, 'comparison': comparison,
                   'control': json.loads((self.output / 'control/score.json').read_text())['summary'],
                   'candidateScore': json.loads((self.output / 'candidate/score.json').read_text())['summary'],
                   'sourceUnchanged': True, 'registrySourceUnchanged': True, 'twoColdTargets': True,
                   'nativeLld': native_lld,
                   'linkOrderInputs': {x['label']: x['linkInputs'] for x in self.cohorts},
                   'originalFullCaptureSha256': sha(original),
                   'wholeFiles': whole_files,
                   'wholeFileEquality': {
                       'controlAndCandidateStripped': whole_files['control']['candidate.so']
                           == whole_files['candidate']['candidate.so'],
                       'controlStrippedAndOriginal': whole_files['control']['candidate.so']
                           == {'sha256': sha(original), 'bytes': original.stat().st_size},
                       'candidateStrippedAndOriginal': whole_files['candidate']['candidate.so']
                           == {'sha256': sha(original), 'bytes': original.stat().st_size}},
                   'limits': 'One measured pair; no VM, automatic promotion or whole-original-ELF equality claim.'})
        return code


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-base', required=True, type=commit_id)
    parser.add_argument('--candidate', required=True, type=commit_id)
    parser.add_argument('--changed-source-path', required=True, choices=ALLOWED)
    parser.add_argument('--preflight-only', action='store_true')
    parser.add_argument('--work', type=Path, default=Path(os.environ.get('RUNNER_TEMP', ROOT / 'work')) / 'pump-native-pair-work')
    parser.add_argument('--output', type=Path, default=ROOT / 'work/pump-native-pair/evidence')
    args = parser.parse_args()
    pair = Pair(args)
    try:
        if not args.preflight_only:
            require(platform.system() == 'Darwin' and platform.machine() == 'arm64'
                    and platform.mac_ver()[0].split('.')[0] == '26', 'native macOS 26 arm64 is required')
        pair.prepare()
        if args.preflight_only:
            print(json.dumps({'preflight_only': True, 'output': str(pair.output)}))
            return 0
        return pair.measure()
    except Exception as error:
        if pair.output_created:
            pair.write('FAILURE.json', {'type': type(error).__name__, 'message': str(error),
                       'sourceBase': args.source_base, 'candidate': args.candidate})
        raise


if __name__ == '__main__':
    raise SystemExit(main())
