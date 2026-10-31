"""One faithful cold build of the exact reviewed S1 creator/fee boundary split."""
from pathlib import Path
import argparse
import stat
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

BASE = '66caa3e2de152190bab3d998e7f6df18243b8e1e'
EXPECTED_SOURCE_SHA256 = 'a1035b0d249859e09fd64c1598cef256c7ca337563d7408a4cf9189d9e0ceb2b'
EXPECTED_PROGRAM_FILES = 141
EXPECTED_CHANGED_PATHS = ('programs/pump/src/creator/admin_cto.rs',)
REFERENCE_BASE = 'ecea7021fcb6a09959901522c6a4edca150a1a1b'
REFERENCE_SOURCE_SHA256 = 'c182aa90dcbf0262ddb2354016f84500826b6013a36d5e4e122d350dd7262980'
ROOT = Path(__file__).resolve().parents[4]
EVIDENCE = ROOT / 'work/pump-candidate-identity/evidence'
WORK = Path(os.environ['RUNNER_TEMP']) / 'pump-candidate-identity-work'
SDKROOT = Path.home() / '.cache/solana'
REFERENCE = ROOT / 'work/current-ecea-reference'
REFERENCE_RUN = 41166161483
REFERENCE_ARTIFACT = 13029328269
REFERENCE_ZIP_SHA256 = 'e37113f971eb103ffa929a4c931f00d876bcdaef112f50ff0b6be451d788c48a'
REFERENCE_FILES = {'PREFLIGHT.json': {'bytes': 2154, 'sha256': '585f3361234d81224952f73b27132eae09f9dd4a8d01ae3002672fb962c20fa3'}, 'RESULT.json': {'bytes': 16919, 'sha256': '58a67842d7c9d260ffc89e28b2f45f4d42926a3294e451e2f3965d9ac6cd62ec'}, 'baseline-input.json': {'bytes': 241, 'sha256': '0ae11a0ad853ee38dff47f8c47ecf74df45d386746fc1b418e1f10a4e3669969'}, 'bootstrap-after.log': {'bytes': 199, 'sha256': '326aec33bf8b06d4426cbbaeaa72f4ccd9e708ac1ca243655f5da91aee3e0e69'}, 'bootstrap-before.log': {'bytes': 404, 'sha256': 'df8ee5f0b3f033130a22cbb9bb23da70b9fe1522c9abb4bbbe8ed9f0e89decd2'}, 'build.json': {'bytes': 850, 'sha256': '4320f8d1873b5d8a698d8d2ef1d4d56bcef2dfdc269dc3d47614cfdab3add658'}, 'build.log': {'bytes': 31075, 'sha256': 'b6de76388aaa73658c05039839bb9d057bf3d28cc8d7cad9e3203479567634cc'}, 'candidate.so': {'bytes': 1934832, 'sha256': '053452856e75b0995d4fe3a947fb66bffa3b49170c2537f4e198ee08da27ddb2'}, 'cargo-fingerprints.json': {'bytes': 1859, 'sha256': 'd9daf85e10aa01fb4499961c7ed25256fad08fd6eb499c2eeee524dd4eb7e136'}, 'cold-build.log': {'bytes': 850, 'sha256': '4320f8d1873b5d8a698d8d2ef1d4d56bcef2dfdc269dc3d47614cfdab3add658'}, 'cold-target-inputs.json': {'bytes': 1589, 'sha256': '8c1d4117d53de2b1fa4c971bfa73503ab5d3de30bd1c87726f8d3f883e21424c'}, 'commands.jsonl': {'bytes': 1718, 'sha256': '2c95d154e246560dc30ffaa9d088c0f74cb76a4a77ab99f7e886900a4ba8960f'}, 'compiled-workspace-inputs.json': {'bytes': 25498, 'sha256': 'ca64bd08fef60414bd8a18221a0511237fd984577970713f388a9950a8f7c11c'}, 'compiled-workspace.tar.gz': {'bytes': 218088, 'sha256': '1fc19238d21e868596a975a111a8f7e49fda19aa3040655761da328a9fa44035'}, 'controller-inputs.json': {'bytes': 695, 'sha256': '9eaeb3bb6a0e76f8d0223114edd1f8524e698a89b2ece92bb3f9b37f917cc1e6'}, 'fetch-locked.log': {'bytes': 9003, 'sha256': '13a0dcdeb46b78e8726afedb0a2ff97ad7649aa08bb4e78d34556cd7b63b968b'}, 'host.json': {'bytes': 230, 'sha256': '1aedc2c7b1b9c96bcfd770173339799bac771c83e3d2c0a383b3cfa4c0fc6e53'}, 'link-inputs.json': {'bytes': 1604, 'sha256': 'daeadd69673d2527d96af991f53ca5b64bfff4759933d1ee3aaf90063c40a801'}, 'link-order-admission.json': {'bytes': 1848, 'sha256': '94417058e1cab423b56fabb718605c4080e3a0743de534b004ec382aefdc5588'}, 'link-receipt.json': {'bytes': 19580, 'sha256': '9684d9141a2b669d816125bec6ba8ed806a762da233abb02dab38ea5e4fd6668'}, 'link.map': {'bytes': 2196461, 'sha256': '077b065748d3a37d8f87727b7b5743a93698d4c4bd3238ee7a13ae840b6dbf72'}, 'native-lld-input-after.json': {'bytes': 457, 'sha256': '60b7eb107ee81d60ffd0d1efe66af50fc9f797caf139fb120bf7eabf1cec9d0f'}, 'native-lld-input-before.json': {'bytes': 457, 'sha256': '60b7eb107ee81d60ffd0d1efe66af50fc9f797caf139fb120bf7eabf1cec9d0f'}, 'operational-inputs.json': {'bytes': 924, 'sha256': '7f328168c93f38c0283bdef9195ec6c65ea9a0ea1586bd507ebbd5eb20227c04'}, 'pinned-link-inputs/link_order.py': {'bytes': 8618, 'sha256': '0e10badcc2cb860c0b77a2d32e1a1086885f9f59d4ab163e77678eed42760462'}, 'pinned-link-inputs/ordered.ld': {'bytes': 73681, 'sha256': '6954d9901b005312be6e7f980cb5e74a1440c174547c2040a881acf2e5c25b45'}, 'pinned-link-inputs/pump_link_lld.py': {'bytes': 236, 'sha256': '03b61b39cf5e85512086c87298ac302cec78378b00c09c594715d18c0aa86e5b'}, 'pinned-link-inputs/pump_link_rustc.py': {'bytes': 218, 'sha256': '94ab1290caee5bb9152fb4e49974960e53c4a5e1f9833c20cd6060ec514a360d'}, 'pinned-link-inputs/sbf_default.ld': {'bytes': 452, 'sha256': '5e8370b9380f55411d827721e2e43c8cfd1eac71d1383e20b938397bc0bd82c3'}, 'preflight-builder-source-inputs.json': {'bytes': 26909, 'sha256': '0947ed17361dc199d7b49ff7dd77d3e351aa86cac536f2bc577209a83fa4bae7'}, 'program-source-inputs.json': {'bytes': 36998, 'sha256': '6a533746b7d15c7ab5b8df78ad765f2e9e9877ed1ed5a0853485dbe8b0c77989'}, 'program-source.tar.gz': {'bytes': 218940, 'sha256': '2f8eed039edb5c43623a42c723b3d06111ffff930a29d7156b60fd0920856ed1'}, 'registry-source-inputs-after.json': {'bytes': 1258468, 'sha256': '8edb1e4e5d38fdc18f1965226b7025feeb03cf587ff82c40f35f9d764d3d3a6a'}, 'registry-source-inputs.json': {'bytes': 1258468, 'sha256': '8edb1e4e5d38fdc18f1965226b7025feeb03cf587ff82c40f35f9d764d3d3a6a'}, 'score.json': {'bytes': 336314, 'sha256': '47b6afaa2216d608e2ee7f93384c6ff582f58a90a535cc2637b7363b23355b0a'}, 'score.log': {'bytes': 11769, 'sha256': 'e4a01d34fe3ac7b1ccdb74614efe5b432a4f96c4d72f0a72af0e1f852c1dab09'}, 'sdk-downloads.json': {'bytes': 797, 'sha256': '6f379e6d35ee86b3239c86127424565bf003081a4d2d0df9b5f4ee9e32ba621b'}, 'source-inputs.json': {'bytes': 26909, 'sha256': '0947ed17361dc199d7b49ff7dd77d3e351aa86cac536f2bc577209a83fa4bae7'}, 'source-selection.json': {'bytes': 544, 'sha256': '5d8c00a0595373faa29e9e75956dc39c19505e2e2e12fc3e7c39332bf14a3718'}, 'tool-inputs-after.json': {'bytes': 1256, 'sha256': 'b158b9c883509967665704fc3a43ecc2ac608f6de1480397a1a6de7c6ead1e5e'}, 'tool-inputs-before.json': {'bytes': 1256, 'sha256': 'b158b9c883509967665704fc3a43ecc2ac608f6de1480397a1a6de7c6ead1e5e'}, 'toolchain-source-inputs.json': {'bytes': 65119, 'sha256': 'b8e8521e3156ad47b0c790ff6fab4cb99d52b887c384c292d7143fdb2924e679'}, 'unstripped.so': {'bytes': 2665688, 'sha256': '8efdc872cdf169ae992c5efc193480c3cc4d9cc7b8808d956733e4f3ce713435'}}
CORE = ('reconstruction/harness', 'reconstruction/toolchain', 'reconstruction/base', 'reconstruction/pump-main/baseline', 'evidence/original/pump')
OPS = ('.github/workflows/qualify-pump-macos-v144.yml', 'reconstruction/pump-main/lanes/current-native-control/pump_current_control.py', 'reconstruction/pump-main/lanes/current-native-control/README.md')
# -B does not propagate to child shebang interpreters. Keep the exact input set.
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
sys.dont_write_bytecode = True

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
    env = dict(os.environ) if env is None else dict(env)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    with (EVIDENCE / (name + '.log')).open('w') as stream:
        result = subprocess.run(args, cwd=ROOT, env=env, stdout=stream, stderr=subprocess.STDOUT)
    with (EVIDENCE / 'commands.jsonl').open('a') as stream:
        stream.write(json.dumps({'name': name, 'command': args, 'returncode': result.returncode}) + '\n')
    if result.returncode:
        print((EVIDENCE / (name + '.log')).read_text()[-16000:], flush=True)
    result.check_returncode()


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

def require(condition, message):
    if not condition:
        raise ValueError(message)

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

def file_vector(root):
    rows = {}
    for path in sorted(root.rglob('*')):
        require(not path.is_symlink(), 'unexpected staged symlink')
        if path.is_file():
            rows[path.relative_to(root).as_posix()] = {
                'bytes': path.stat().st_size, 'executable': bool(path.stat().st_mode & 0o111),
                'sha256': sha(path)}
    return rows

class LinkAudit:
    def __init__(self, core):
        self.core = core
        self.output = EVIDENCE

    def write(self, name, value):
        write(name, value)

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
        # Current maintained lld_main forwards a checked private copy, then
        # removes it after the real linker exits. The frozen helper/default/
        # program digests above bind that source operation; do not demand the
        # old mutable staged pathname or claim a retained temporary-file hash.
        require(len(scripts) == 1, 'actual linker did not forward exactly one script')
        forwarded_script = Path(scripts[0])
        require(forwarded_script.is_absolute() and forwarded_script.name == 'ordered.ld'
                and forwarded_script.parent.name.startswith('pump-link-script-')
                and forwarded_script != script and not forwarded_script.exists()
                and argv.count('-Map=' + str(work / 'link.map')) == 1,
                'actual linker did not use the maintained private-script/map contract')
        self.write(cohort['label'] + '/link-order-admission.json', {
            'actualBuildLinkOrder': build['link_order'], 'receiptSha256': sha(receipt),
            'mapSha256': sha(link_map), 'mapBytes': link_map.stat().st_size,
            'nativeLld': native_lld, 'frozenProgramScript': inputs['programScript'],
            'frozenDefaultScript': inputs['maintainedInputs']['sbf_default.ld'],
            'forwardedScript': str(forwarded_script),
            'forwardedScriptBinding': 'Current frozen link_order.lld_main validates raw script bytes, writes the private copy, forwards it and removes it after linking; no retained private-copy bytes claimed.'})


def verify_input_set(prefixes, rows, phase):
    actual = {p.relative_to(ROOT).as_posix() for prefix in prefixes
              for p in (ROOT / prefix).rglob('*') if p.is_file() or p.is_symlink()}
    expected = {row['path'] for row in rows}
    if actual != expected:
        diagnostic = {'phase': phase, 'prefixes': prefixes,
                      'addedPaths': sorted(actual - expected), 'missingPaths': sorted(expected - actual)}
        write('input-set-failure.json', diagnostic)
        raise ValueError('input file set differs from Git: ' + json.dumps(diagnostic, sort_keys=True))
    verify_files(ROOT, rows)


def verify_inputs(source, core, staged, phase):
    verify_input_set(('programs/pump',), source, phase + ':program')
    verify_input_set(CORE, core, phase + ':core')
    require(file_vector(WORK / 'ws') == staged, 'compiled workspace inputs changed: ' + phase)


def tool_inputs(env, audit):
    sdk = SDKROOT / 'v1.44/platform-tools'
    paths = [sdk / 'rust/bin/rustc', sdk / 'rust/bin/cargo', sdk / 'llvm/bin/llvm-objcopy',
             Path(env['PUMP_RECON_HOME']) / 'toolchains/hybrid144/rust/bin/rustc',
             SDKROOT / 'v1.52/platform-tools/llvm/bin/llvm-objdump', Path(audit.lld_input(env)['path'])]
    paths += sorted((sdk / 'rust/lib').glob('lib*.dylib'))
    return {str(p): sha(p) for p in paths}


def verify_current_reference(core):
    actual = {p.relative_to(REFERENCE).as_posix() for p in REFERENCE.rglob('*') if p.is_file() or p.is_symlink()}
    require(actual == set(REFERENCE_FILES), 'current control reference member set differs')
    for name, expected in REFERENCE_FILES.items():
        path = REFERENCE / name
        require(path.is_file() and not path.is_symlink() and path.stat().st_size == expected['bytes']
                and sha(path) == expected['sha256'], 'current control reference member differs: ' + name)
    result = json.loads((REFERENCE / 'RESULT.json').read_text())
    require(result['base'] == REFERENCE_BASE and result['sourceUnchanged'] and result['coldTarget'],
            'current reference source/cold binding differs')
    require(json.loads((REFERENCE / 'toolchain-source-inputs.json').read_text())['files'] == core,
            'candidate changes the current control CORE')
    selected = json.loads((REFERENCE / 'source-inputs.json').read_text())
    require(selected['sha256'] == REFERENCE_SOURCE_SHA256, 'current reference selected source differs')
    score = json.loads((REFERENCE / 'score.json').read_text())
    require(score['summary']['total'] == len(score['windows']) == 1035
            and score['summary']['candidate_sha256'] == sha(REFERENCE / 'unstripped.so'),
            'current reference full score/ELF binding differs')
    write('reference-admission.json', {'base': REFERENCE_BASE, 'run': REFERENCE_RUN,
          'artifactId': REFERENCE_ARTIFACT, 'originalZipSha256': REFERENCE_ZIP_SHA256,
          'files': REFERENCE_FILES, 'coreEqual': True,
          'limits': 'Every extracted current control member is authenticated. Candidate source is independently bound to S1; it is not transplanted from a reference tar. Outer transport ZIP is not rehashed by this hosted job.'})
    return score


def compare_candidate(score, reference_score):
    require(set(score['windows']) == set(reference_score['windows'])
            and len(score['windows']) == 1035, 'candidate/current full score domain differs')
    changes = {key: {'reference': reference_score['windows'][key], 'candidate': row}
               for key, row in score['windows'].items() if row != reference_score['windows'][key]}
    report = {'sourceCommit': BASE, 'sourceSha256': EXPECTED_SOURCE_SHA256,
              'referenceBase': REFERENCE_BASE, 'referenceRun': REFERENCE_RUN,
              'referenceArtifactId': REFERENCE_ARTIFACT, 'fullRowsCompared': 1035,
              'allRowsEqual': not changes, 'changedRows': changes, 'summary': score['summary'],
              'noNormalizedLosses': not score['summary']['losses'],
              'noRawLosses': not score['summary']['raw_losses'],
              'limits': 'One exact-source candidate measurement against actual current control. No automatic source acceptance, causal IR proof, runtime result or source gain follows from build success.'}
    write('CANDIDATE-COMPARISON.json', report)
    return report


def main(preflight_only=False):
    # This guard precedes every output write, Git source read or build operation.
    require(isinstance(BASE, str) and re.fullmatch(r'[0-9a-f]{40}', BASE)
            and isinstance(EXPECTED_SOURCE_SHA256, str)
            and re.fullmatch(r'[0-9a-f]{64}', EXPECTED_SOURCE_SHA256)
            and type(EXPECTED_PROGRAM_FILES) is int and EXPECTED_PROGRAM_FILES > 0
            and isinstance(EXPECTED_CHANGED_PATHS, (list, tuple)) and bool(EXPECTED_CHANGED_PATHS)
            and all(isinstance(p, str) and p.startswith('programs/pump/') for p in EXPECTED_CHANGED_PATHS),
            'candidate template is unbound; root-reviewed S1/source pins are required')
    require(not EVIDENCE.exists() and not WORK.exists(), 'evidence and cold work must start absent')
    EVIDENCE.mkdir(parents=True)
    require(preflight_only or (platform.system() == 'Darwin' and platform.machine() == 'arm64'
            and platform.mac_ver()[0].split('.')[0] == '26'), 'native macOS 26 arm64 required')
    proposal_paths = git('diff', '--no-ext-diff', '--no-textconv', '--no-renames', '--name-only',
                         REFERENCE_BASE, BASE).decode().splitlines()
    require(set(proposal_paths) == set(EXPECTED_CHANGED_PATHS), 'candidate changes paths outside its frozen proposal')
    source = entries(BASE, ('programs/pump',))
    core = entries(BASE, CORE)
    require(len(source) == EXPECTED_PROGRAM_FILES, 'candidate program input census differs')
    verify_input_set(('programs/pump',), source, 'initial:program')
    verify_input_set(CORE, core, 'initial:core')
    checkout = git('rev-parse', 'HEAD').decode().strip()
    changed = git('diff', '--no-ext-diff', '--no-textconv', '--no-renames', '--name-only', BASE, checkout).decode().splitlines()
    require(set(changed) <= set(OPS), 'operational checkout changes source/core inputs')
    if not preflight_only:
        headers = git('cat-file', '-p', checkout).split(b'\n\n', 1)[0].splitlines()
        require([x[7:].decode() for x in headers if x.startswith(b'parent ')] == [BASE], 'control ops must be a direct child of frozen source')
        operational = entries(checkout, OPS)
        require({r['path'] for r in operational} == set(OPS), 'all three operational files must be committed')
        verify_files(ROOT, operational)
        write('operational-inputs.json', {'checkout': checkout, 'files': operational})
    write('program-source-inputs.json', {'base': BASE, 'files': source})
    write('toolchain-source-inputs.json', {'base': BASE, 'files': core})
    reference_score = verify_current_reference(core)
    baseline = REFERENCE / 'score.json'
    write('baseline-input.json', {'path': baseline.relative_to(ROOT).as_posix(), 'sha256': sha(baseline),
          'run': REFERENCE_RUN, 'artifactId': REFERENCE_ARTIFACT,
          'role': 'Actual admitted ECEA control; complete candidate gains/losses are relative to these exact1035 rows.'})
    harness = ROOT / 'reconstruction/harness'
    sys.path.insert(0, str(harness))
    try:
        spec = importlib.util.spec_from_file_location('current_fastbuild', harness / 'fastbuild.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    snapshot = module.snapshot(ROOT / 'programs/pump')
    require(snapshot['sha256'] == EXPECTED_SOURCE_SHA256, 'candidate selected source differs from frozen S1 pin')
    all_git = {r['path'].removeprefix('programs/pump/'): r for r in source}
    selected = {r['path']: r for r in snapshot['files']}
    require(len(selected) == len(snapshot['files']) and set(selected) <= set(all_git), 'selected source is not a unique Git subset')
    for name, row in selected.items():
        expected = {'path': name, 'bytes': all_git[name]['bytes'], 'executable': all_git[name]['mode'] == '100755', 'sha256': all_git[name]['sha256']}
        require(row == expected, 'maintained selected source differs from Git: ' + name)
    write('source-selection.json', {'helper': next(r for r in core if r['path'] == 'reconstruction/harness/source_inputs.py'),
          'rule': 'Execute unchanged maintained snapshot helper; excludes .git metadata and crate-root target directory only.',
          'allGitFiles': len(source), 'selectedSourceFiles': len(selected), 'excludedGitPaths': sorted(set(all_git) - set(selected)),
          'selectedSha256': snapshot['sha256']})
    write('preflight-builder-source-inputs.json', snapshot)
    module.stage(ROOT / 'programs/pump', WORK / 'ws', expected_inputs=snapshot)
    staged = file_vector(WORK / 'ws')
    require(len(staged) == len(selected) + 1, 'unexpected standalone-to-workspace projection')
    write('compiled-workspace-inputs.json', staged)
    for filename, folder, names in [('compiled-workspace.tar.gz', WORK / 'ws', staged),
            ('program-source.tar.gz', ROOT, [r['path'] for r in source])]:
        with tarfile.open(EVIDENCE / filename, 'w:gz') as archive:
            for name in names: archive.add(folder / name, arcname=name, recursive=False)
    audit = LinkAudit(core)
    link_inputs = audit.link_preflight(module.link_order, ROOT / 'programs/pump', WORK, EVIDENCE, source)
    verify_inputs(source, core, staged, 'after-stage')
    write('PREFLIGHT.json', {'base': BASE, 'preflightOnly': preflight_only,
          'programGitFiles': len(source), 'selectedSourceFiles': len(selected), 'workspaceFiles': len(staged), 'coreFiles': len(core),
          'sourceSha256': snapshot['sha256'], 'linkInputs': link_inputs,
          'pythonDontWriteBytecode': os.environ['PYTHONDONTWRITEBYTECODE'],
          'sdkInstalledByPreflight': False, 'bootstrapRunByPreflight': False,
          'cargoRunByPreflight': False, 'compilerRunByPreflight': False})
    if preflight_only:
        print(json.dumps({'preflightOnly': True, 'base': BASE, 'sourceSha256': snapshot['sha256'],
              'programGitFiles': len(source), 'selectedSourceFiles': len(selected), 'workspaceFiles': len(staged), 'coreFiles': len(core)})); return
    write('host.json', {'platform': platform.platform(), 'machine': platform.machine(), 'python': sys.version, 'base': BASE})
    downloads = [install_sdk('v1.44', '66e20d135fddd70ff519baf7ff320d762957f9aedf93a50e23756db23ad79351')]
    write('sdk-downloads.json', downloads)
    downloads.append(install_sdk('v1.52', '1727dfb31e833ce777d01e70cb4b3cebd26b376bf09d80527f02457d4cf6fd00'))
    write('sdk-downloads.json', downloads)
    sdk = SDKROOT / 'v1.44/platform-tools'
    env = dict(os.environ, PUMP_RECON_HOME=str(Path(os.environ['RUNNER_TEMP']) / 'pump-candidate-identity-cache'),
               PUMP_BUILD_SLOTS='1', CARGO_BUILD_JOBS='2', PYTHONDONTWRITEBYTECODE='1',
               PUMP_OBJDUMP=str(SDKROOT / 'v1.52/platform-tools/llvm/bin/llvm-objdump'))
    require(not Path(env['PUMP_RECON_HOME']).exists(), 'identity cache must start empty')
    write('controller-inputs.json', {'checkout': checkout, 'runnerSha256': sha(__file__),
          'workflowSha256': sha(ROOT / OPS[0]), 'recipe': 'identity', 'triple': 'sbpf-solana-solana',
          'gitSourceManifest': 'program-source-inputs.json', 'builderSourceManifest': 'source-inputs.json',
          'documentedEnvironment': {key: env[key] for key in ['PUMP_RECON_HOME','PUMP_BUILD_SLOTS','CARGO_BUILD_JOBS','PUMP_OBJDUMP','PYTHONDONTWRITEBYTECODE']}})
    run('bootstrap-before', [sys.executable, '-B', ROOT / 'reconstruction/toolchain/bootstrap.py', '--sdk-check', 'full'], env)
    native = audit.lld_input(env); tools = tool_inputs(env, audit)
    write('native-lld-input-before.json', native); write('tool-inputs-before.json', tools)
    fetch_env = dict(env, RUSTC=str(sdk / 'rust/bin/rustc'))
    fetch_env['PATH'] = str(sdk / 'rust/bin') + os.pathsep + env['PATH']
    run('fetch-locked', [sdk / 'rust/bin/cargo', 'fetch', '--locked', '--manifest-path', WORK / 'ws/Cargo.toml'], fetch_env)
    registry = registry_manifest(); write('registry-source-inputs.json', registry)
    verify_inputs(source, core, staged, 'before-build')
    cache = Path(env['PUMP_RECON_HOME'])
    require(not (WORK / 'target-identity').exists() and not (cache / 'template-target-sbpf').exists()
            and not (cache / 'template-target').exists(), 'cold build cannot use a warm target/template')
    write('cold-target-inputs.json', {'base': BASE, 'sourceSha256': snapshot['sha256'],
          'target': str(WORK / 'target-identity'), 'targetAbsentBeforeBuild': True,
          'dependencyTemplatesAbsent': True, 'toolInputs': tools})
    run('cold-build', [sys.executable, '-B', harness / 'fastbuild.py', '--src', ROOT / 'programs/pump',
         '--work', WORK, '--out', EVIDENCE, '--recipe', 'identity'], env)
    text = (EVIDENCE / 'cold-build.log').read_text(); values = []
    for marker in re.finditer(r'(?m)^\{', text):
        try: value, _ = json.JSONDecoder().raw_decode(text[marker.start():])
        except json.JSONDecodeError: continue
        if isinstance(value, dict) and 'runtime_valid' in value and 'unstripped_sha256' in value: values.append(value)
    require(len(values) == 1, 'expected exactly one actual cold result')
    build = values[0]; write('build.json', build)
    require(build['ok'] and build['runtime_valid'] and not build['stack_warnings'], 'runtime-invalid stack build')
    require(build['recipe'] == 'identity' and build['triple'] == 'sbpf-solana-solana', 'recipe/target changed')
    require(build['unstripped_sha256'] == sha(EVIDENCE / 'unstripped.so') and build['candidate_sha256'] == sha(EVIDENCE / 'candidate.so'), 'actual ELF differs')
    builder_source = json.loads((EVIDENCE / 'source-inputs.json').read_text())
    encoded = json.dumps(builder_source['files'], sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
    require(builder_source == snapshot and hashlib.sha256(encoded).hexdigest() == builder_source['sha256'] == build['source_sha256'], 'actual builder and Git source vectors differ')
    audit.verify_link_result({'label': '.', 'folder': EVIDENCE, 'work': WORK, 'linkInputs': link_inputs}, build, native)
    log = (EVIDENCE / 'build.log').read_text(); fingerprints = {}
    for package in ('pump-recovered','pump-token-ext'):
        require(re.search(r'(?m)^\s*Compiling ' + package + r' v', log), 'fresh local compilation missing: ' + package)
        paths = list((WORK / 'target-identity').glob('sbpf-solana-solana/release/.fingerprint/' + package + '-*/*.json'))
        require(paths, 'target compiler fingerprint absent: ' + package)
        for path in paths:
            value = json.loads(path.read_text()); require(value.get('rustflags') == ['-Zremap-cwd-prefix='], 'target compiler flags differ')
            fingerprints[path.relative_to(WORK).as_posix()] = value
    write('cargo-fingerprints.json', fingerprints)
    run('bootstrap-after', [sys.executable, '-B', ROOT / 'reconstruction/toolchain/bootstrap.py', '--sdk-check', 'full'], env)
    verify_inputs(source, core, staged, 'after-build')
    require(registry_manifest() == registry and tool_inputs(env,audit) == tools and audit.lld_input(env) == native, 'registry/tool/LLD changed')
    write('registry-source-inputs-after.json', registry_manifest()); write('tool-inputs-after.json', tool_inputs(env,audit))
    write('native-lld-input-after.json', audit.lld_input(env))
    run('score', [sys.executable, '-B', harness / 'score.py', EVIDENCE / 'unstripped.so', '--baseline', baseline, '--json', EVIDENCE / 'score.json'], env)
    score = json.loads((EVIDENCE / 'score.json').read_text())
    require(score['summary']['total'] == len(score['windows']) == 1035 and score['summary']['candidate_sha256'] == build['unstripped_sha256'], 'full official census absent/different ELF')
    verify_inputs(source, core, staged, 'after-score')
    require(registry_manifest() == registry and tool_inputs(env,audit) == tools and audit.lld_input(env) == native, 'registry/tool/LLD changed during scoring')
    verify_files(ROOT, operational)
    comparison = compare_candidate(score, reference_score)
    require(comparison['noNormalizedLosses'] and comparison['noRawLosses'],
            'candidate has raw or normalized losses against the exact current control; full score/comparison retained')
    result = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'base': BASE,
          'sourceUnchanged': True, 'registrySourceUnchanged': True, 'toolInputsUnchanged': True,
          'coldTarget': True, 'gitSourceManifest': 'program-source-inputs.json', 'builderSourceManifest': 'source-inputs.json',
          'builderSourceSha256': builder_source['sha256'], 'summary': score['summary'],
          'programGitFiles': len(source), 'selectedSourceFiles': len(selected), 'workspaceFiles': len(staged), 'coreFiles': len(core),
          'unstrippedSha256': sha(EVIDENCE / 'unstripped.so'), 'candidateSha256': sha(EVIDENCE / 'candidate.so'),
          'nativeLld': native, 'linkOrder': build['link_order'],
          'referenceRun': REFERENCE_RUN, 'referenceArtifactId': REFERENCE_ARTIFACT,
          'fullScoreRowsCompared': comparison['fullRowsCompared'],
          'noNormalizedLosses': comparison['noNormalizedLosses'], 'noRawLosses': comparison['noRawLosses'],
          'limits': 'One exact S1 candidate identity-recipe measurement against ECEA control. No automatic source acceptance, causal IR proof, runtime/latest-main/whole-original result or source gain is implied.'}
    write('RESULT.json', result); print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--preflight-only', action='store_true')
    args=parser.parse_args()
    try: main(args.preflight_only)
    except Exception as error:
        if EVIDENCE.is_dir(): write('FAILURE.json', {'type':type(error).__name__, 'message':str(error), 'base':BASE})
        raise
