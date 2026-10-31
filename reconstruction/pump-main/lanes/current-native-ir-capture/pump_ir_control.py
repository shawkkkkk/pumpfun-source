"""One fixed-source diagnostic IR capture; output equality with actual current39eb baseline is required."""
from pathlib import Path
import argparse
import stat
import struct
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

BASE = '39eb377aa6c6ce4aacff273aa13732abb0c0078a'
ROOT = Path(__file__).resolve().parents[4]
EVIDENCE = ROOT / 'work/pump-current39eb-ir/evidence'
WORK = Path(os.environ['RUNNER_TEMP']) / 'pump-current39eb-ir-work'
SDKROOT = Path.home() / '.cache/solana'
REFERENCE = ROOT / 'work/current39eb-reference'
REFERENCE_RUN = 41159607118
REFERENCE_ARTIFACT = 13026402898
REFERENCE_ZIP_SHA256 = '94d7f23a92e0cae60b186ae589bffa7767e2c18f63b93dfb8e97f6c7e4a912c6'
TARGET_SYMBOL = '_ZN14pump_recovered9admin_cto7execute17h3bd6d7f34f2e30d7E'
REFERENCE_TARGET_EXTENT = (141840, 27400)
REFERENCE_FILES = {'PREFLIGHT.json': {'bytes': 2154, 'sha256': '862437e4ea41b5a693b17e338fcf9327e52dda033636d3fd65727b038fc46013'}, 'RESULT.json': {'bytes': 16919, 'sha256': '0cce0ac644ffa0fa5b4bb18991ac49a557b99ff200f443ff7b020c693e917026'}, 'baseline-input.json': {'bytes': 241, 'sha256': '0ae11a0ad853ee38dff47f8c47ecf74df45d386746fc1b418e1f10a4e3669969'}, 'bootstrap-after.log': {'bytes': 199, 'sha256': '326aec33bf8b06d4426cbbaeaa72f4ccd9e708ac1ca243655f5da91aee3e0e69'}, 'bootstrap-before.log': {'bytes': 404, 'sha256': 'df8ee5f0b3f033130a22cbb9bb23da70b9fe1522c9abb4bbbe8ed9f0e89decd2'}, 'build.json': {'bytes': 850, 'sha256': '141c3f2ae1f90b89dc3e2f79218031d40252dcaff0e80957a0fe278b32b545ee'}, 'build.log': {'bytes': 31075, 'sha256': 'f56ddd67f910c80c9025a8f217317807017f727114afd5a43dbb88ea9e91ebaf'}, 'candidate.so': {'bytes': 1934832, 'sha256': '5dff5613d7b329e6662eb10ad88b05cafa400da0620b1ba21da4c6f339823d16'}, 'cargo-fingerprints.json': {'bytes': 1859, 'sha256': 'd9daf85e10aa01fb4499961c7ed25256fad08fd6eb499c2eeee524dd4eb7e136'}, 'cold-build.log': {'bytes': 850, 'sha256': '141c3f2ae1f90b89dc3e2f79218031d40252dcaff0e80957a0fe278b32b545ee'}, 'cold-target-inputs.json': {'bytes': 1589, 'sha256': '6296f5d9486fada599f9864ee05da911954c72eb367d510d90716417dd04e0c6'}, 'commands.jsonl': {'bytes': 1718, 'sha256': '2c95d154e246560dc30ffaa9d088c0f74cb76a4a77ab99f7e886900a4ba8960f'}, 'compiled-workspace-inputs.json': {'bytes': 25498, 'sha256': 'dad65b2319cc29688c95957c1dd49f9dda73d95cca9a5fb394d52d5ef1c59665'}, 'compiled-workspace.tar.gz': {'bytes': 218050, 'sha256': '26ae55ece79ecbb15eaef41c7eab5a679b198e46f7aefae609015c524a911b1d'}, 'controller-inputs.json': {'bytes': 695, 'sha256': '324558fbabc0776c6eb67f64be581afe95b2a7448fc7a783c052efdefee98b8c'}, 'fetch-locked.log': {'bytes': 9003, 'sha256': 'deb5bef7ee3da0829feb19ff6868c097e19b1f5b50aa36e0852686c560351624'}, 'host.json': {'bytes': 230, 'sha256': 'd657d9b90a7db0c7355ad432f12372b4e11f6562da6320f394ee0d765486b47d'}, 'link-inputs.json': {'bytes': 1604, 'sha256': 'daeadd69673d2527d96af991f53ca5b64bfff4759933d1ee3aaf90063c40a801'}, 'link-order-admission.json': {'bytes': 1848, 'sha256': '1bab45857b2fafd7344b9235c3619c1dabf7b4957a353afca6f70ce737c64f11'}, 'link-receipt.json': {'bytes': 19580, 'sha256': '178fb7d67f253b161347b6510d095dd4fd09b845c32d276d1fd0aa013339f6b7'}, 'link.map': {'bytes': 2196463, 'sha256': 'e5b03e5dda5786fe7400f41eb889eb55217ec7fd5a9a9e2dab643b6568ca884e'}, 'native-lld-input-after.json': {'bytes': 457, 'sha256': '60b7eb107ee81d60ffd0d1efe66af50fc9f797caf139fb120bf7eabf1cec9d0f'}, 'native-lld-input-before.json': {'bytes': 457, 'sha256': '60b7eb107ee81d60ffd0d1efe66af50fc9f797caf139fb120bf7eabf1cec9d0f'}, 'operational-inputs.json': {'bytes': 924, 'sha256': 'ed4ffa93762fb75d2a8e815549ec5ae558e9e6cdef4fa365678d0b3674c44956'}, 'pinned-link-inputs/link_order.py': {'bytes': 8618, 'sha256': '0e10badcc2cb860c0b77a2d32e1a1086885f9f59d4ab163e77678eed42760462'}, 'pinned-link-inputs/ordered.ld': {'bytes': 73681, 'sha256': '6954d9901b005312be6e7f980cb5e74a1440c174547c2040a881acf2e5c25b45'}, 'pinned-link-inputs/pump_link_lld.py': {'bytes': 236, 'sha256': '03b61b39cf5e85512086c87298ac302cec78378b00c09c594715d18c0aa86e5b'}, 'pinned-link-inputs/pump_link_rustc.py': {'bytes': 218, 'sha256': '94ab1290caee5bb9152fb4e49974960e53c4a5e1f9833c20cd6060ec514a360d'}, 'pinned-link-inputs/sbf_default.ld': {'bytes': 452, 'sha256': '5e8370b9380f55411d827721e2e43c8cfd1eac71d1383e20b938397bc0bd82c3'}, 'preflight-builder-source-inputs.json': {'bytes': 26909, 'sha256': '34b2d76b4f1597e1de5494db5e3687984e58ef773426a8dba8ac03ebab2868f4'}, 'program-source-inputs.json': {'bytes': 36998, 'sha256': '3d8591d2bcd941722a046d47a3fdddaa301261de53f6413ea259ca9c8ce270da'}, 'program-source.tar.gz': {'bytes': 218941, 'sha256': 'aa46a981f7381148bd3fa140c63c2a423f1c7279070a851183c7310cb2d30db1'}, 'registry-source-inputs-after.json': {'bytes': 1258468, 'sha256': '8edb1e4e5d38fdc18f1965226b7025feeb03cf587ff82c40f35f9d764d3d3a6a'}, 'registry-source-inputs.json': {'bytes': 1258468, 'sha256': '8edb1e4e5d38fdc18f1965226b7025feeb03cf587ff82c40f35f9d764d3d3a6a'}, 'score.json': {'bytes': 336314, 'sha256': '775f7c765dc21e87851245da2fc939b127d85b944acaff34a75e7162fd3b38df'}, 'score.log': {'bytes': 11769, 'sha256': '62c13dc5fd76bb0348e33a7d7ea86fda0f6d64a13c062f7b64a3c1ea33724c70'}, 'sdk-downloads.json': {'bytes': 797, 'sha256': '6f379e6d35ee86b3239c86127424565bf003081a4d2d0df9b5f4ee9e32ba621b'}, 'source-inputs.json': {'bytes': 26909, 'sha256': '34b2d76b4f1597e1de5494db5e3687984e58ef773426a8dba8ac03ebab2868f4'}, 'source-selection.json': {'bytes': 544, 'sha256': '94c0362a3119e03432b0c828b9b5e5b0cd3ab48b9f4bdc2dcf6ff665c0d0f53c'}, 'tool-inputs-after.json': {'bytes': 1256, 'sha256': 'b158b9c883509967665704fc3a43ecc2ac608f6de1480397a1a6de7c6ead1e5e'}, 'tool-inputs-before.json': {'bytes': 1256, 'sha256': 'b158b9c883509967665704fc3a43ecc2ac608f6de1480397a1a6de7c6ead1e5e'}, 'toolchain-source-inputs.json': {'bytes': 65119, 'sha256': 'ec736a701fd42b3a6e84a490b9ef1d5e57399f9ada1ddc63f04486392f514698'}, 'unstripped.so': {'bytes': 2665688, 'sha256': '289b7d63122fb1f8a64213df1b781b49aa596448e2f33256fa85365d9f7ed4f4'}}
CORE = ('reconstruction/harness', 'reconstruction/toolchain', 'reconstruction/base', 'reconstruction/pump-main/baseline', 'evidence/original/pump')
OPS = ('.github/workflows/qualify-pump-macos-v144.yml', 'reconstruction/pump-main/lanes/current-native-ir-capture/pump_ir_control.py', 'reconstruction/pump-main/lanes/current-native-ir-capture/capture.py', 'reconstruction/pump-main/lanes/current-native-ir-capture/README.md')
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



def verify_reference(source, core, snapshot, staged):
    actual = {p.relative_to(REFERENCE).as_posix() for p in REFERENCE.rglob('*') if p.is_file() or p.is_symlink()}
    require(actual == set(REFERENCE_FILES), 'reference artifact member set differs')
    for name, expected in REFERENCE_FILES.items():
        path = REFERENCE / name
        require(path.is_file() and not path.is_symlink() and path.stat().st_size == expected['bytes']
                and sha(path) == expected['sha256'], 'reference artifact bytes differ: ' + name)
    result = json.loads((REFERENCE / 'RESULT.json').read_text())
    require(result['base'] == BASE and result['sourceUnchanged'] and result['coldTarget'], 'reference control binding differs')
    require(json.loads((REFERENCE / 'program-source-inputs.json').read_text()) == {'base': BASE, 'files': source},
            'diagnostic program source differs from actual reference')
    require(json.loads((REFERENCE / 'toolchain-source-inputs.json').read_text()) == {'base': BASE, 'files': core},
            'diagnostic CORE differs from actual reference')
    require(json.loads((REFERENCE / 'source-inputs.json').read_text()) == snapshot
            and json.loads((REFERENCE / 'compiled-workspace-inputs.json').read_text()) == staged,
            'diagnostic selected/staged bytes differ from actual reference')
    score = json.loads((REFERENCE / 'score.json').read_text())
    require(score['summary']['total'] == len(score['windows']) == 1035, 'reference full census missing')
    _, _, symbols = elf_semantics(REFERENCE / 'unstripped.so')
    target = [x for x in symbols if x[0] == TARGET_SYMBOL and x[1] & 15 == 2]
    require(len(target) == 1 and target[0][-2:] == REFERENCE_TARGET_EXTENT,
            'actual reference target symbol/extent differs')
    write('reference-target-symbol.json', {'run': REFERENCE_RUN, 'artifactId': REFERENCE_ARTIFACT, 'symbol': target[0]})
    write('reference-admission.json', {'run': REFERENCE_RUN, 'artifactId': REFERENCE_ARTIFACT,
          'originalZipSha256': REFERENCE_ZIP_SHA256, 'files': REFERENCE_FILES,
          'sourceAndCoreAndStageEqual': True,
          'limits': 'Official download-artifact supplies extracted files; every admitted member size and byte hash is checked. Original transport ZIP is not redownloaded/rehashed here.'})
    return score


def elf_semantics(path):
    raw = path.read_bytes()
    require(raw[:6] == b'\x7fELF\x02\x01', 'expected 64-bit little-endian ELF')
    header = struct.unpack_from('<16sHHIQQQIHHHHHH', raw)
    offset, width, count, strings_index = header[6], header[11], header[12], header[13]
    require(width == 64 and count > 0 and strings_index < count
            and offset + width * count <= len(raw), 'unsupported section table')
    rows = [struct.unpack_from('<IIQQQQIIQQ', raw, offset + i * width) for i in range(count)]
    strings = rows[strings_index]
    names = raw[strings[4]:strings[4] + strings[5]]
    sections = {}
    for row in rows:
        end = names.find(b'\0', row[0])
        require(end >= row[0] and row[4] + row[5] <= len(raw), 'invalid section extent')
        name = names[row[0]:end].decode('utf-8')
        require(name not in sections, 'duplicate section name')
        sections[name] = raw[row[4]:row[4] + row[5]]
    symbols, strings = sections['.symtab'], sections['.strtab']
    require(len(symbols) % 24 == 0, 'invalid symbol table')
    result = []
    for position in range(0, len(symbols), 24):
        name, info, other, section, value, size = struct.unpack_from('<IBBHQQ', symbols, position)
        end = strings.find(b'\0', name)
        require(end >= name, 'invalid symbol name')
        result.append((strings[name:end].decode('utf-8'), info, other, section, value, size))
    return raw, sections, result


def diagnostic_comparison(score, build, reference_score):
    reference_build = json.loads((REFERENCE / 'build.json').read_text())
    capture = json.loads((EVIDENCE / 'capture-result.json').read_text())
    actual, sections, symbols = elf_semantics(EVIDENCE / 'unstripped.so')
    reference, reference_sections, reference_symbols = elf_semantics(REFERENCE / 'unstripped.so')
    same_sections = set(sections) == set(reference_sections)
    section_rows = {name: {'equal': sections.get(name) == reference_sections.get(name),
                         'actualSha256': hashlib.sha256(sections[name]).hexdigest() if name in sections else None,
                         'referenceSha256': hashlib.sha256(reference_sections[name]).hexdigest() if name in reference_sections else None}
                    for name in sorted(sections.keys() | reference_sections.keys())}
    section_payloads_equal = same_sections and all(row['equal'] for name, row in section_rows.items()
                                                   if name not in ('.symtab', '.strtab'))
    functions = sorted(x for x in symbols if x[1] & 15 == 2)
    reference_functions = sorted(x for x in reference_symbols if x[1] & 15 == 2)
    numeric_symbols_equal = (len(symbols) == len(reference_symbols)
                            and all(a[1:] == b[1:] for a, b in zip(symbols, reference_symbols)))
    changes = [{'index': i, 'actual': a, 'reference': b}
               for i, (a, b) in enumerate(zip(symbols, reference_symbols)) if a != b]
    local_names_only = numeric_symbols_equal and all(
        x['actual'][0] != x['reference'][0] and x['actual'][1] >> 4 == 0
        and x['reference'][1] >> 4 == 0 and x['actual'][1] & 15 == 1 for x in changes)
    write('local-symbol-name-differences.json', changes)
    stripped_equal = ((EVIDENCE / 'candidate.so').read_bytes() == (REFERENCE / 'candidate.so').read_bytes())
    equality = {name: build[field] == reference_build[field] for name, field in
                [('unstripped', 'unstripped_sha256'), ('stripped', 'candidate_sha256')]}
    summary_differences = {key: {'actual': score['summary'].get(key), 'reference': reference_score['summary'].get(key)}
        for key in score['summary'].keys() | reference_score['summary'].keys()
        if score['summary'].get(key) != reference_score['summary'].get(key)}
    code_qualified = (stripped_equal and section_payloads_equal and functions == reference_functions
                      and numeric_symbols_equal and local_names_only)
    report = {'purpose': 'One fixed-source compiler measurement; no source gain or IR editing.',
              'identityScope': 'Complete stripped ELF, all non-symbol section payloads and semantic function symbols equal the actual current39eb control. Full unstripped identity is separately reported, not required.',
              'referenceRun': REFERENCE_RUN, 'referenceArtifactId': REFERENCE_ARTIFACT,
              'referenceSourceSha256': build['source_sha256'], 'targetSymbol': TARGET_SYMBOL,
              'referenceUnstrippedSha256': reference_build['unstripped_sha256'],
              'actualUnstrippedSha256': build['unstripped_sha256'],
              'referenceStrippedSha256': reference_build['candidate_sha256'],
              'actualStrippedSha256': build['candidate_sha256'], 'fullElfHashesEqual': equality,
              'completeStrippedBytesEqual': stripped_equal, 'sectionPayloads': section_rows,
              'nonSymbolSectionPayloadsEqual': section_payloads_equal,
              'semanticFunctionSymbolsEqual': functions == reference_functions,
              'symbolNumericFieldsEqual': numeric_symbols_equal, 'localSymbolDifferencesNamesOnly': local_names_only,
              'symbolNameDifferenceCount': len(changes), 'codeIdentityQualified': code_qualified,
              'full1035RowsEqual': score['windows'] == reference_score['windows'],
              'fullScoreSummaryEqual': score['summary'] == reference_score['summary'],
              'scoreSummaryDifferences': summary_differences,
              'captureMethodSha256': sha(ROOT / OPS[2]), 'actualCompilerCommands': capture['calls'],
              'targetDefinitionRetained': capture.get('targetDefinitionRetained', False),
              'allMachineStagesObserved': capture.get('allMachineStagesObserved', False),
              'jumpThreadingPairingValid': capture.get('jumpThreadingPairingValid', False),
              'jumpThreadingPairCount': len(capture.get('jumpThreadingPairs', [])),
              'allRequestedStagesObserved': capture.get('allRequestedStagesObserved', False),
              'captureComplete': capture.get('captureComplete', False),
              'compilerCompleted': capture.get('compilerCompleted', False), 'buildOk': capture.get('buildOk', False),
              'captureResultSha256': sha(EVIDENCE / 'capture-result.json')}
    report['attributionQualified'] = (code_qualified and report['full1035RowsEqual']
            and set(summary_differences) <= {'candidate_sha256'} and capture.get('symbol') == TARGET_SYMBOL
            and report['targetDefinitionRetained'] and report['allRequestedStagesObserved']
            and report['allMachineStagesObserved'] and report['jumpThreadingPairingValid']
            and report['jumpThreadingPairCount'] >= 2 and report['captureComplete']
            and report['compilerCompleted'] and report['buildOk'] and len(capture['calls']) == 1)
    write('DIAGNOSTIC-COMPARISON.json', report)
    require(report['attributionQualified'], 'diagnostic code identity or complete IR/machine capture is not qualified')
    return report


def main(preflight_only=False):
    require(isinstance(REFERENCE_ARTIFACT, int) and bool(REFERENCE_FILES)
            and isinstance(REFERENCE_ZIP_SHA256, str) and TARGET_SYMBOL.startswith('_ZN'),
            'actual current control reference/symbol not frozen')
    require(not EVIDENCE.exists() and not WORK.exists(), 'evidence and cold work must start absent')
    EVIDENCE.mkdir(parents=True)
    require(preflight_only or (platform.system() == 'Darwin' and platform.machine() == 'arm64'
            and platform.mac_ver()[0].split('.')[0] == '26'), 'native macOS 26 arm64 required')
    source = entries(BASE, ('programs/pump',))
    core = entries(BASE, CORE)
    verify_input_set(('programs/pump',), source, 'initial:program')
    verify_input_set(CORE, core, 'initial:core')
    checkout = git('rev-parse', 'HEAD').decode().strip()
    changed = git('diff', '--no-ext-diff', '--no-textconv', '--no-renames', '--name-only', BASE, checkout).decode().splitlines()
    require(set(changed) <= set(OPS), 'operational checkout changes source/core inputs')
    if not preflight_only:
        headers = git('cat-file', '-p', checkout).split(b'\n\n', 1)[0].splitlines()
        require([x[7:].decode() for x in headers if x.startswith(b'parent ')] == [BASE], 'control ops must be a direct child of frozen source')
        operational = entries(checkout, OPS)
        require({r['path'] for r in operational} == set(OPS), 'all four diagnostic operational files must be committed')
        verify_files(ROOT, operational)
        write('operational-inputs.json', {'checkout': checkout, 'files': operational})
    write('program-source-inputs.json', {'base': BASE, 'files': source})
    write('toolchain-source-inputs.json', {'base': BASE, 'files': core})
    baseline = ROOT / 'reconstruction/pump-main/baseline/score.json'
    require(baseline.is_file(), 'explicit historical baseline required')
    write('baseline-input.json', {'path': baseline.relative_to(ROOT).as_posix(), 'sha256': sha(baseline),
          'role': 'Historical comparison only; current counts come from this actual unchanged-source ELF.'})
    harness = ROOT / 'reconstruction/harness'
    sys.path.insert(0, str(harness))
    try:
        spec = importlib.util.spec_from_file_location('current_fastbuild', harness / 'fastbuild.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    snapshot = module.snapshot(ROOT / 'programs/pump')
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
    reference_score = verify_reference(source, core, snapshot, staged)
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
    env = dict(os.environ, PUMP_RECON_HOME=str(Path(os.environ['RUNNER_TEMP']) / 'pump-current39eb-ir-cache'),
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
    run('cold-build', [sys.executable, '-B', ROOT / OPS[2], '--src', ROOT / 'programs/pump',
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
    comparison = diagnostic_comparison(score, build, reference_score)
    result = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'base': BASE,
          'sourceUnchanged': True, 'registrySourceUnchanged': True, 'toolInputsUnchanged': True,
          'coldTarget': True, 'gitSourceManifest': 'program-source-inputs.json', 'builderSourceManifest': 'source-inputs.json',
          'builderSourceSha256': builder_source['sha256'], 'summary': score['summary'],
          'programGitFiles': len(source), 'selectedSourceFiles': len(selected), 'workspaceFiles': len(staged), 'coreFiles': len(core),
          'unstrippedSha256': sha(EVIDENCE / 'unstripped.so'), 'candidateSha256': sha(EVIDENCE / 'candidate.so'),
          'nativeLld': native, 'linkOrder': build['link_order'],
          'diagnosticAttributionQualified': comparison['attributionQualified'],
          'limits': 'One fixed-source diagnostic with fixed pass printing; complete stripped ELF/non-symbol sections/function symbols and all1035 rows equal the actual current39eb control. Full unstripped identity is separately reported. At least two paired before/after JumpThreading snapshots and five complete machine stages retained. No source gain, IR edits, opt/llc, threshold/variant search, VM/runtime or whole-original claim.'}
    write('RESULT.json', result); print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--preflight-only', action='store_true')
    args=parser.parse_args()
    try: main(args.preflight_only)
    except Exception as error:
        if EVIDENCE.is_dir(): write('FAILURE.json', {'type':type(error).__name__, 'message':str(error), 'base':BASE})
        raise
