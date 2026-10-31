"""Fixed settings-Result S3 trace; native SUCCESS and source rejection remain separate."""
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

BASE = '65f0162a3dcd381df0f831082dd6732c9af4ab78'
EXPECTED_SOURCE_SHA256 = '9fc3fd3c8e68d85e5bf4fcb2309694974aab3c5aaacab9741a1e0ea25c72a622'
EXPECTED_PROGRAM_FILES = 141
EXPECTED_CHANGED_PATHS = ('programs/pump/src/creator/admin_cto.rs',)
REFERENCE_BASE = '13fe4536be64d8c5c10f8905e9d2236f423ac4f4'
REFERENCE_SOURCE_SHA256 = 'ba203d5c8b0cda5ab3bb6eec65266a992331b7a8a361b9977a3d2ab474b11fe2'
ROOT = Path(__file__).resolve().parents[4]
EVIDENCE = ROOT / 'work/pump-s3-diagnostic/evidence'
WORK = Path(os.environ['RUNNER_TEMP']) / 'pump-s3-diagnostic-work'
SDKROOT = Path.home() / '.cache/solana'
REFERENCE = ROOT / 'work/current13fe-reference'
REFERENCE_RUN = 41170683278
REFERENCE_ARTIFACT = 13031166975
REFERENCE_ZIP_SHA256 = '875edcd6e9ebb7e5b8fb2495d0008e723762b1f0251a02e038881fb56749fa92'
REFERENCE_FILES = {'unstripped.so': {'bytes': 2665688, 'sha256': 'cec841bd60cc002213829e3149e7c170dbb7f5bbc47a9887cef1ab7e0193319e'}, 'toolchain-source-inputs.json': {'bytes': 65119, 'sha256': 'f33d580fb0cbffa6bec6a6fad0ca8b70f0d201ccaccd86c2238ea3270e5785f1'}, 'tool-inputs-before.json': {'bytes': 1256, 'sha256': 'b158b9c883509967665704fc3a43ecc2ac608f6de1480397a1a6de7c6ead1e5e'}, 'tool-inputs-after.json': {'bytes': 1256, 'sha256': 'b158b9c883509967665704fc3a43ecc2ac608f6de1480397a1a6de7c6ead1e5e'}, 'source-selection.json': {'bytes': 544, 'sha256': 'ae0f280872b655d7e87960f0e744f9d2f61ffc7bd36a0abda7e1727d86292fe4'}, 'source-inputs.json': {'bytes': 26909, 'sha256': 'f0a11d2661e90b8c816c1e557037b923741ceff035ccde874451f4b05382ee09'}, 'sdk-downloads.json': {'bytes': 797, 'sha256': '6f379e6d35ee86b3239c86127424565bf003081a4d2d0df9b5f4ee9e32ba621b'}, 'score.log': {'bytes': 11769, 'sha256': 'aade9491298fd604ef4b2a89c1a9e587bd864d5d39915e123b244184d24c33cc'}, 'score.json': {'bytes': 336314, 'sha256': '0738b134e00c601bfdbbbd06491094873a545e138346e2e17526af529684303c'}, 'registry-source-inputs.json': {'bytes': 1258468, 'sha256': '8edb1e4e5d38fdc18f1965226b7025feeb03cf587ff82c40f35f9d764d3d3a6a'}, 'registry-source-inputs-after.json': {'bytes': 1258468, 'sha256': '8edb1e4e5d38fdc18f1965226b7025feeb03cf587ff82c40f35f9d764d3d3a6a'}, 'program-source.tar.gz': {'bytes': 218974, 'sha256': '8272f499363e919dbae1c27eed15807de05973cc32fa8b44c51e4280d285e83b'}, 'program-source-inputs.json': {'bytes': 36998, 'sha256': 'a5c10774d700d578748747efccd27a239043bf027a4878e8d355f1441bab77b5'}, 'preflight-builder-source-inputs.json': {'bytes': 26909, 'sha256': 'f0a11d2661e90b8c816c1e557037b923741ceff035ccde874451f4b05382ee09'}, 'native-lld-input-before.json': {'bytes': 457, 'sha256': '60b7eb107ee81d60ffd0d1efe66af50fc9f797caf139fb120bf7eabf1cec9d0f'}, 'operational-inputs.json': {'bytes': 924, 'sha256': '81ef0586039e1888ae4b5441e409f190b81f2abbbcfc7abd92f5ea1bf8c8de19'}, 'native-lld-input-after.json': {'bytes': 457, 'sha256': '60b7eb107ee81d60ffd0d1efe66af50fc9f797caf139fb120bf7eabf1cec9d0f'}, 'link.map': {'bytes': 2196461, 'sha256': '7e690907462a02ef149e39055a7ca60a9a7bf8dfe5db64045818f8614665fc4d'}, 'link-receipt.json': {'bytes': 19580, 'sha256': 'b4ecbf44bdd13f9f8d28da831003f0d556ba3da480f5b9f228d03a0061bfd254'}, 'link-order-admission.json': {'bytes': 1848, 'sha256': '92799edd5e09972109585edab34f419fcd8ca58ca5f686c0d84ff22311d84e17'}, 'link-inputs.json': {'bytes': 1604, 'sha256': 'daeadd69673d2527d96af991f53ca5b64bfff4759933d1ee3aaf90063c40a801'}, 'host.json': {'bytes': 230, 'sha256': '172775f407b8961d5a8fb810111b949444ffc02945f5671e6cfab7c905fb1320'}, 'fetch-locked.log': {'bytes': 9003, 'sha256': '485da67a6bb0f01d2538c74c64e9fd742b4438b8dcee505d85bbb50f1f01191c'}, 'controller-inputs.json': {'bytes': 695, 'sha256': '367b2c16e90a79f0258867ff8e85b18d125610e81a504849efd484e5a7cb2e93'}, 'compiled-workspace.tar.gz': {'bytes': 218080, 'sha256': '1bfef0daec3e3ba2069ed29c00be968538357127c9476c6dd444e87d0fbd9de4'}, 'compiled-workspace-inputs.json': {'bytes': 25498, 'sha256': '3dc3dbb927c2cb7594746cf751d11c99b8b251d93223f1225a25a5bfe051857d'}, 'commands.jsonl': {'bytes': 1718, 'sha256': '2c95d154e246560dc30ffaa9d088c0f74cb76a4a77ab99f7e886900a4ba8960f'}, 'cold-target-inputs.json': {'bytes': 1589, 'sha256': '6625c375aab50ee4543cfcf169fd05ce2e221045372f922395cece8e32233b6b'}, 'cold-build.log': {'bytes': 849, 'sha256': 'fbe1d6d294112ade9bac50ecda4ce629139be441e35f764dfb1df9c1d68ca093'}, 'cargo-fingerprints.json': {'bytes': 1859, 'sha256': 'd9daf85e10aa01fb4499961c7ed25256fad08fd6eb499c2eeee524dd4eb7e136'}, 'candidate.so': {'bytes': 1934832, 'sha256': 'fe099633c59f1a409f66d7b7bd6ce702580116c92ac24cb26842a351f3ee459e'}, 'build.log': {'bytes': 31075, 'sha256': '2c0eb6154cade74ecac9034ebc7a926e86773d99f8052c9037a773e35edf7777'}, 'build.json': {'bytes': 849, 'sha256': 'fbe1d6d294112ade9bac50ecda4ce629139be441e35f764dfb1df9c1d68ca093'}, 'bootstrap-before.log': {'bytes': 404, 'sha256': 'df8ee5f0b3f033130a22cbb9bb23da70b9fe1522c9abb4bbbe8ed9f0e89decd2'}, 'PREFLIGHT.json': {'bytes': 2154, 'sha256': '68449a68c148e98de3cfbb44e0fe0220be30681c1b9c5680fdf1226812a55c56'}, 'bootstrap-after.log': {'bytes': 199, 'sha256': '326aec33bf8b06d4426cbbaeaa72f4ccd9e708ac1ca243655f5da91aee3e0e69'}, 'baseline-input.json': {'bytes': 241, 'sha256': '0ae11a0ad853ee38dff47f8c47ecf74df45d386746fc1b418e1f10a4e3669969'}, 'RESULT.json': {'bytes': 16919, 'sha256': '1328a8b4ec33e0cc146d4c74f53c912b35e2b5c535829c836c80de0c0299426b'}, 'pinned-link-inputs/sbf_default.ld': {'bytes': 452, 'sha256': '5e8370b9380f55411d827721e2e43c8cfd1eac71d1383e20b938397bc0bd82c3'}, 'pinned-link-inputs/pump_link_rustc.py': {'bytes': 218, 'sha256': '94ab1290caee5bb9152fb4e49974960e53c4a5e1f9833c20cd6060ec514a360d'}, 'pinned-link-inputs/pump_link_lld.py': {'bytes': 236, 'sha256': '03b61b39cf5e85512086c87298ac302cec78378b00c09c594715d18c0aa86e5b'}, 'pinned-link-inputs/ordered.ld': {'bytes': 73681, 'sha256': '6954d9901b005312be6e7f980cb5e74a1440c174547c2040a881acf2e5c25b45'}, 'pinned-link-inputs/link_order.py': {'bytes': 8618, 'sha256': '0e10badcc2cb860c0b77a2d32e1a1086885f9f59d4ab163e77678eed42760462'}}
CORE = ('reconstruction/harness', 'reconstruction/toolchain', 'reconstruction/base', 'reconstruction/pump-main/baseline', 'evidence/original/pump')
OPS = ('.github/workflows/qualify-pump-macos-v144.yml', 'reconstruction/pump-main/lanes/current-native-ir-capture/pump_ir_control.py', 'reconstruction/pump-main/lanes/current-native-ir-capture/capture.py', 'reconstruction/pump-main/lanes/current-native-ir-capture/README.md')

TRACE_REFERENCE = ROOT / 'work/s3-normal-reference'
TRACE_RUN = 41172052790
TRACE_ARTIFACT = 13031054922
TRACE_ZIP_SHA256 = '0f1a82695dd41525fffbebe667c3067062a9a1fd1fd3fb4b70cbdb054965bdda'
TRACE_FILES = {'unstripped.so': {'bytes': 2665792, 'sha256': '100d222047a2281a4409d8f732266955368504479d3d4076b4f6e3af08ef37e4'}, 'toolchain-source-inputs.json': {'bytes': 65119, 'sha256': 'e5c4053c17d4f6a162bc36c8f926750b0b8e04015cb75059221a371110786c13'}, 'tool-inputs-before.json': {'bytes': 1260, 'sha256': 'ae2ba564cbcdf589b56e31f608a2e7285ac6aa2fd09f2133de7112953912c1e1'}, 'tool-inputs-after.json': {'bytes': 1260, 'sha256': 'ae2ba564cbcdf589b56e31f608a2e7285ac6aa2fd09f2133de7112953912c1e1'}, 'source-selection.json': {'bytes': 544, 'sha256': '3c4cc1e1b40ceca78fad5d801aa3d54ad754ea44d0719063f41e61e3f0946980'}, 'source-inputs.json': {'bytes': 26909, 'sha256': '9766730afe0bdabbf6e397f0fec7107b5e4fc4c7ed80eee3cd1d6a875c0e62d7'}, 'sdk-downloads.json': {'bytes': 797, 'sha256': '6f379e6d35ee86b3239c86127424565bf003081a4d2d0df9b5f4ee9e32ba621b'}, 'score.log': {'bytes': 241, 'sha256': '8cbcd2d0d2250968f4715659d616451f45107bde5aaffa1e0a23b4e62815aa81'}, 'score.json': {'bytes': 323923, 'sha256': 'e2e71e1af269d2fdaead4252f20730fa3310fbc6d89b26eaf7f1cb8fc15903d6'}, 'registry-source-inputs.json': {'bytes': 1258468, 'sha256': '8edb1e4e5d38fdc18f1965226b7025feeb03cf587ff82c40f35f9d764d3d3a6a'}, 'registry-source-inputs-after.json': {'bytes': 1258468, 'sha256': '8edb1e4e5d38fdc18f1965226b7025feeb03cf587ff82c40f35f9d764d3d3a6a'}, 'reference-admission.json': {'bytes': 6581, 'sha256': '52a2614b6fafe8d56e9e74e1beff9fc26139b094f4a19d9a428a88703fcc514b'}, 'program-source.tar.gz': {'bytes': 218910, 'sha256': 'd7950eb16766876d19b455967e1eb6846d0aad64977ff266a72c4b826ebf63b6'}, 'program-source-inputs.json': {'bytes': 36998, 'sha256': '610f3c469b7fddeb33cc5a1f754bd495a7ec5db58b446170c35313ac21073615'}, 'preflight-builder-source-inputs.json': {'bytes': 26909, 'sha256': '9766730afe0bdabbf6e397f0fec7107b5e4fc4c7ed80eee3cd1d6a875c0e62d7'}, 'operational-inputs.json': {'bytes': 924, 'sha256': '2a72935394ca07851a4f94757004b909f9e72523064608d269de2ebacaeb9cc7'}, 'native-lld-input-before.json': {'bytes': 459, 'sha256': '9dd609f9bde9027b70203e24acbef2c31aa86ace45dee2966e5cbb32f98ddd32'}, 'native-lld-input-after.json': {'bytes': 459, 'sha256': '9dd609f9bde9027b70203e24acbef2c31aa86ace45dee2966e5cbb32f98ddd32'}, 'link.map': {'bytes': 2201511, 'sha256': '6494611554d7c88810c80ac06a294aa5e1e57441068f648654a5bb75dc02e0be'}, 'link-receipt.json': {'bytes': 19838, 'sha256': 'e36fde6ee0af6890b24fcc313c36fe8c2f48f8689f1afdf576d24f53c1fe727a'}, 'link-order-admission.json': {'bytes': 1850, 'sha256': 'b6d9cda1103a33698cd3e6ad54bc6bda069b4e03653579371da250091decc0cb'}, 'link-inputs.json': {'bytes': 1604, 'sha256': 'daeadd69673d2527d96af991f53ca5b64bfff4759933d1ee3aaf90063c40a801'}, 'host.json': {'bytes': 230, 'sha256': '6045c6d9033961e7006ca3ffeb23f18880434bcd7cb7b892aa3ce6777f06d9d8'}, 'fetch-locked.log': {'bytes': 9003, 'sha256': '35ba0b3c23389d274487a39e85858a0e5fff9598bb411e43afaa472de17bdd1d'}, 'controller-inputs.json': {'bytes': 697, 'sha256': '0eed435c7a940b67d1df4fe13a168a04583e580557e28ca9679debb38ee85a5b'}, 'compiled-workspace.tar.gz': {'bytes': 218061, 'sha256': 'a05505dae1b990f288bf6c01d44b0427fb4808b14156731ca64501be40bd9c41'}, 'compiled-workspace-inputs.json': {'bytes': 25498, 'sha256': '1a9bbc3870a3e62fb041effa26d10e9a2ef2ad0e86f9c4a3d85cfce52cd4984d'}, 'commands.jsonl': {'bytes': 1722, 'sha256': '54c43cc7fb28a81d83d6f07b09b11d815739df691a1544b9b9e8cc980e656347'}, 'cold-target-inputs.json': {'bytes': 1595, 'sha256': 'b92ce1ec580d44ed15a630398a7ce71e2720a913b45ba27a22a35295c178d845'}, 'cold-build.log': {'bytes': 852, 'sha256': 'bc684dfa5d3d7d4c75a7e4c2b17caee4e901a17e2ffa0b271cb8f338f541b480'}, 'cargo-fingerprints.json': {'bytes': 1859, 'sha256': 'd9daf85e10aa01fb4499961c7ed25256fad08fd6eb499c2eeee524dd4eb7e136'}, 'candidate.so': {'bytes': 1934832, 'sha256': '31ece96dc7eee70c8c7cc16ba401d63e668c3725a8d1c411834fd9494d8e01d0'}, 'build.log': {'bytes': 31079, 'sha256': '8198f3fb86a01cb89ad62f752d73aa1749fe17b5efc10b0ac21e8450f9c19273'}, 'build.json': {'bytes': 852, 'sha256': 'bc684dfa5d3d7d4c75a7e4c2b17caee4e901a17e2ffa0b271cb8f338f541b480'}, 'bootstrap-before.log': {'bytes': 408, 'sha256': '6e2d95241fb44011da5e7767c9c437a7cf78d21ae94a646b69dbf1f401db7b97'}, 'bootstrap-after.log': {'bytes': 201, 'sha256': '489f947142962456a9755e59998ec49b9eb925fd621bea0a2b2e59fda82edb25'}, 'baseline-input.json': {'bytes': 299, 'sha256': 'ea9809b4ae9f4b917d29871d3bb8657b2fddec7426e3222ab0994ba3f9fdb638'}, 'CANDIDATE-COMPARISON.json': {'bytes': 886, 'sha256': 'ea4ec35fb16f20a250f23b204446b3816a64f1d733d593c45258644c623524b6'}, 'RESULT.json': {'bytes': 2145, 'sha256': '159bc5192ce00fe14a399d6d6e41b0efb153c1e86ccad67420a7fec857b7264b'}, 'PREFLIGHT.json': {'bytes': 2154, 'sha256': 'ed132d36ba13afb69c27310bfbf09018aa10700046f5e958a46b3c6ef44fdb6b'}, 'pinned-link-inputs/sbf_default.ld': {'bytes': 452, 'sha256': '5e8370b9380f55411d827721e2e43c8cfd1eac71d1383e20b938397bc0bd82c3'}, 'pinned-link-inputs/pump_link_rustc.py': {'bytes': 218, 'sha256': '94ab1290caee5bb9152fb4e49974960e53c4a5e1f9833c20cd6060ec514a360d'}, 'pinned-link-inputs/pump_link_lld.py': {'bytes': 236, 'sha256': '03b61b39cf5e85512086c87298ac302cec78378b00c09c594715d18c0aa86e5b'}, 'pinned-link-inputs/ordered.ld': {'bytes': 73681, 'sha256': '6954d9901b005312be6e7f980cb5e74a1440c174547c2040a881acf2e5c25b45'}, 'pinned-link-inputs/link_order.py': {'bytes': 8618, 'sha256': '0e10badcc2cb860c0b77a2d32e1a1086885f9f59d4ab163e77678eed42760462'}}
TARGET_SYMBOL = '_ZN14pump_recovered9admin_cto7execute17h3bd6d7f34f2e30d7E'
TRACE_TARGET_EXTENT = (141840, 27400)

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
          'limits': 'Every extracted current control member is authenticated. Candidate source is independently bound to S3; it is not transplanted from a reference tar. Outer transport ZIP is not rehashed by this hosted job.'})
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

def verify_trace_reference(source, core, snapshot, staged):
    actual = {p.relative_to(TRACE_REFERENCE).as_posix() for p in TRACE_REFERENCE.rglob('*') if p.is_file() or p.is_symlink()}
    require(actual == set(TRACE_FILES), 'reference artifact member set differs')
    for name, expected in TRACE_FILES.items():
        path = TRACE_REFERENCE / name
        require(path.is_file() and not path.is_symlink() and path.stat().st_size == expected['bytes']
                and sha(path) == expected['sha256'], 'reference artifact bytes differ: ' + name)
    normal_result = json.loads((TRACE_REFERENCE / 'RESULT.json').read_text())
    require(normal_result['base'] == BASE and normal_result['sourceUnchanged']
            and normal_result['registrySourceUnchanged'] and normal_result['toolInputsUnchanged']
            and normal_result['coldTarget'] and normal_result['noNormalizedLosses']
            and normal_result['noRawLosses'] and 'FAILURE.json' not in TRACE_FILES,
            'actual normal S3 success admission differs; source-metric rejection is separate')
    comparison = json.loads((TRACE_REFERENCE / 'CANDIDATE-COMPARISON.json').read_text())
    require(comparison['sourceCommit'] == BASE and comparison['sourceSha256'] == EXPECTED_SOURCE_SHA256
            and comparison['referenceBase'] == REFERENCE_BASE and comparison['referenceRun'] == REFERENCE_RUN
            and comparison['referenceArtifactId'] == REFERENCE_ARTIFACT and comparison['fullRowsCompared'] == 1035
            and comparison['noNormalizedLosses'] and comparison['noRawLosses'], 'actual normal S3 no-loss comparison differs')
    require(json.loads((TRACE_REFERENCE / 'program-source-inputs.json').read_text()) == {'base': BASE, 'files': source},
            'diagnostic program source differs from actual reference')
    require(json.loads((TRACE_REFERENCE / 'toolchain-source-inputs.json').read_text()) == {'base': BASE, 'files': core},
            'diagnostic CORE differs from actual reference')
    require(json.loads((TRACE_REFERENCE / 'source-inputs.json').read_text()) == snapshot
            and json.loads((TRACE_REFERENCE / 'compiled-workspace-inputs.json').read_text()) == staged,
            'diagnostic selected/staged bytes differ from actual reference')
    score = json.loads((TRACE_REFERENCE / 'score.json').read_text())
    require(score['summary']['total'] == len(score['windows']) == 1035, 'reference full census missing')
    _, _, symbols = elf_semantics(TRACE_REFERENCE / 'unstripped.so')
    target = [x for x in symbols if x[0] == TARGET_SYMBOL and x[1] & 15 == 2]
    require(len(target) == 1 and target[0][-2:] == TRACE_TARGET_EXTENT,
            'actual reference target symbol/extent differs')
    write('s3-reference-target-symbol.json', {'run': TRACE_RUN, 'artifactId': TRACE_ARTIFACT, 'symbol': target[0]})
    write('s3-reference-admission.json', {'run': TRACE_RUN, 'artifactId': TRACE_ARTIFACT,
          'originalZipSha256': TRACE_ZIP_SHA256, 'files': TRACE_FILES,
          'sourceAndCoreAndStageEqual': True,
          'limits': 'Official download-artifact supplies extracted files; every admitted member size and byte hash is checked. Original transport ZIP is not redownloaded/rehashed here.'})
    return score

def diagnostic_comparison(score, build, reference_score):
    reference_build = json.loads((TRACE_REFERENCE / 'build.json').read_text())
    capture = json.loads((EVIDENCE / 'capture-result.json').read_text())
    actual, sections, symbols = elf_semantics(EVIDENCE / 'unstripped.so')
    reference, reference_sections, reference_symbols = elf_semantics(TRACE_REFERENCE / 'unstripped.so')
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
    stripped_equal = ((EVIDENCE / 'candidate.so').read_bytes() == (TRACE_REFERENCE / 'candidate.so').read_bytes())
    equality = {name: build[field] == reference_build[field] for name, field in
                [('unstripped', 'unstripped_sha256'), ('stripped', 'candidate_sha256')]}
    summary_differences = {key: {'actual': score['summary'].get(key), 'reference': reference_score['summary'].get(key)}
        for key in score['summary'].keys() | reference_score['summary'].keys()
        if score['summary'].get(key) != reference_score['summary'].get(key)}
    code_qualified = (stripped_equal and section_payloads_equal and functions == reference_functions
                      and numeric_symbols_equal and local_names_only)
    report = {'purpose': 'One fixed-S3 compiler trace; native no-loss success and internal source-metric rejection remain separate.',
              'identityScope': 'Complete stripped ELF, all non-symbol section payloads and semantic function symbols equal the actual already-measured normal S3 artifact. Full unstripped identity is separately reported, not required.',
              'referenceRun': TRACE_RUN, 'referenceArtifactId': TRACE_ARTIFACT,
              'referenceSourceSha256': reference_build['source_sha256'], 'targetSymbol': TARGET_SYMBOL,
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
            and capture.get('sourceSha256') == build['source_sha256'] == EXPECTED_SOURCE_SHA256
            and report['targetDefinitionRetained'] and report['allRequestedStagesObserved']
            and report['allMachineStagesObserved'] and report['jumpThreadingPairingValid']
            and report['jumpThreadingPairCount'] >= 2 and report['captureComplete']
            and report['compilerCompleted'] and report['buildOk'] and len(capture['calls']) == 1)
    write('DIAGNOSTIC-COMPARISON.json', report)
    return report

def main(preflight_only=False):
    # This guard precedes every output write, Git source read or build operation.
    require(isinstance(BASE, str) and re.fullmatch(r'[0-9a-f]{40}', BASE)
            and isinstance(EXPECTED_SOURCE_SHA256, str)
            and re.fullmatch(r'[0-9a-f]{64}', EXPECTED_SOURCE_SHA256)
            and type(EXPECTED_PROGRAM_FILES) is int and EXPECTED_PROGRAM_FILES > 0
            and isinstance(EXPECTED_CHANGED_PATHS, (list, tuple)) and bool(EXPECTED_CHANGED_PATHS)
            and all(isinstance(p, str) and p.startswith('programs/pump/') for p in EXPECTED_CHANGED_PATHS),
            'candidate template is unbound; root-reviewed S3/source pins are required')
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
        require({r['path'] for r in operational} == set(OPS), 'all four diagnostic operational files must be committed')
        verify_files(ROOT, operational)
        write('operational-inputs.json', {'checkout': checkout, 'files': operational})
    write('program-source-inputs.json', {'base': BASE, 'files': source})
    write('toolchain-source-inputs.json', {'base': BASE, 'files': core})
    reference_score = verify_current_reference(core)
    baseline = REFERENCE / 'score.json'
    write('baseline-input.json', {'path': baseline.relative_to(ROOT).as_posix(), 'sha256': sha(baseline),
          'run': REFERENCE_RUN, 'artifactId': REFERENCE_ARTIFACT,
          'role': 'Actual admitted current13fe control; complete candidate gains/losses are relative to these exact1035 rows.'})
    harness = ROOT / 'reconstruction/harness'
    sys.path.insert(0, str(harness))
    try:
        spec = importlib.util.spec_from_file_location('current_fastbuild', harness / 'fastbuild.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    snapshot = module.snapshot(ROOT / 'programs/pump')
    require(snapshot['sha256'] == EXPECTED_SOURCE_SHA256, 'candidate selected source differs from frozen S3 pin')
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
    trace_score = verify_trace_reference(source, core, snapshot, staged)
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
    env = dict(os.environ, PUMP_RECON_HOME=str(Path(os.environ['RUNNER_TEMP']) / 'pump-s3-diagnostic-cache'),
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
    comparison = compare_candidate(score, reference_score)
    # Save exact-S3 trace identity before the unchanged native no-loss guard.
    # Internal source-metric rejection remains separate from native success.
    try:
        trace = diagnostic_comparison(score, build, trace_score)
    except Exception as error:
        trace = {'attributionQualified': False, 'error': {'type': type(error).__name__, 'message': str(error)}}
        write('DIAGNOSTIC-COMPARISON-ERROR.json', trace)
    require(comparison['noNormalizedLosses'] and comparison['noRawLosses'],
            'candidate has raw or normalized losses against the exact current control; full score/comparison retained')
    require(trace['attributionQualified'], 'diagnostic code identity or complete IR/machine capture is not qualified')
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
          'limits': 'One exact S3 candidate identity-recipe measurement against current13fe control. No automatic source acceptance, causal IR proof, runtime/latest-main/whole-original result or source gain is implied.'}
    write('RESULT.json', result); print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--preflight-only', action='store_true')
    args=parser.parse_args()
    try: main(args.preflight_only)
    except Exception as error:
        if EVIDENCE.is_dir(): write('FAILURE.json', {'type':type(error).__name__, 'message':str(error), 'base':BASE})
        raise
