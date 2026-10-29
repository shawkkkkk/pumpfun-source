#!/usr/bin/env python3
"""Measure one original-backed two-file helper boundary on the pinned current711 recipe."""
import argparse
import ast
import copy
import difflib
import importlib.util
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tarfile
import urllib.request

import pump_current673_macos_control as io

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / 'research/pump-current711-arithmetic-20261029'
ALLOWED = {'src/trade_v3.rs', 'src/multi_hop_curve_swap.rs'}


def bound_manifest(actual, expected):
    first = next(iter(expected))
    prefixes = [key[:-len(first)] for key in actual if key.endswith(first)]
    assert sum(actual == {prefix + key: value for key, value in expected.items()} for prefix in prefixes) == 1


def inspect():
    spec = json.loads((PACKET / 'inputs.json').read_text())
    assert spec['schema'] == 'PUMP_CURRENT711_TWO_FILE_BOUNDARIES_V1'
    assert io.sha(ROOT / spec['io_helper']['path']) == spec['io_helper']['sha256']
    base = ROOT / spec['base_package']
    assert io.sha(base / 'build.py') == spec['base_builder_sha256']
    assert io.sha(base / 'build-inputs.json') == spec['base_build_inputs_sha256']
    assert {p.name: io.sha(p) for p in (base / 'tools').iterdir() if p.is_file()} == spec['tools_sha256']
    expected = json.loads((base / 'build-inputs.json').read_text())
    assert expected['source_inputs'] == spec['source_inputs'] and len(spec['source_inputs']) == 65
    assert expected['comparison']['candidate_sha256'] == spec['base_expected']['candidate_sha256']
    assert expected['unstripped_sha256'] == spec['base_expected']['unstripped_sha256']
    source = base / 'source'
    assert not any(p.is_symlink() for p in source.rglob('*'))
    loader = importlib.util.spec_from_file_location('composition_source_manifest', base / 'tools/build_source_manifest.py')
    module = importlib.util.module_from_spec(loader); loader.loader.exec_module(module)
    actual = module.source_manifest(source, source, ROOT, cwd=source)
    assert {str((ROOT / name).relative_to(source)): value for name, value in actual.items()} == spec['source_inputs']
    assert set(spec['changes']) == ALLOWED
    composed = copy.deepcopy(expected)
    for name, change in spec['changes'].items():
        assert change['before_sha256'] == expected['source_inputs'][name]
        relative = Path(change['file'])
        assert relative.parent == Path('overlays') and relative.suffix == '.rs'
        assert not (PACKET / relative).is_symlink() and io.sha(PACKET / relative) == change['after_sha256']
        composed['source_inputs'][name] = change['after_sha256']
    assert composed['source_inputs'] == spec['composed_source_inputs']
    assert {key for key in spec['source_inputs'] if spec['source_inputs'][key] != composed['source_inputs'][key]} == ALLOWED
    for name, value in spec['baseline_files'].items():
        assert io.sha(ROOT / name) == value
    baseline = base / 'builds/cold-01'
    receipt = json.loads((baseline / 'build-attempt.json').read_text())
    assert receipt['builder_sha256'] == spec['base_builder_sha256'] and receipt['qualified_image_hashes_equal']
    assert receipt['tool_sha256'] == expected['tool_sha256'] and receipt['target_libraries_sha256'] == expected['target_libraries_sha256']
    assert receipt['source_wrapper_sha256'] == expected['source_wrapper_sha256']
    assert all(receipt[key] for key in ['cold_empty_target', 'source_unchanged', 'tools_unchanged',
        'sdk_rust_libraries_unchanged', 'registry_sources_unchanged', 'target_libraries_unchanged'])
    bound_manifest(receipt['primary_source_sha256'], expected['source_inputs'])
    assert io.sha(baseline / 'candidate.so') == spec['base_expected']['candidate_sha256']
    assert io.sha(baseline / 'unstripped.so') == spec['base_expected']['unstripped_sha256']
    assert io.sha(ROOT / 'evidence/original/pump/deployed.so') == spec['original_sha256']
    original = (base / 'build.py').read_text()
    terminal = ";assert record['qualified_image_hashes_equal']\n"
    assert original.endswith(terminal) and original.count(terminal) == 1
    derived = original[:-len(terminal)] + '\n'; ast.parse(derived)
    patch = ''.join(difflib.unified_diff(original.splitlines(True), derived.splitlines(True),
        fromfile='qualified-current711-build.py', tofile='two-file-boundary-measurement-build.py'))
    for name, value in spec.get('plan_files', {}).items():
        relative = Path(name)
        assert relative.parts[0] == 'plan' and not relative.is_absolute() and '..' not in relative.parts
        assert (PACKET / relative).resolve().is_relative_to(PACKET / 'plan') and not (PACKET / relative).is_symlink()
        assert io.sha(PACKET / relative) == value
    if spec.get('plan_files'):
        plan = json.loads((PACKET / 'plan/PLAN.json').read_text())
        maps = json.loads((PACKET / 'plan/MANIFESTS.json').read_text())
        assert io.sha(PACKET / 'plan/PLAN.json') == spec['plan_sha256']
        assert plan['current_main'] == spec['plan_current_main'] == maps['current_main']
        prefix = 'programs/pump/'
        assert {key.removeprefix(prefix): value for key, value in maps['current_standalone_sha256'].items()} == spec['source_inputs']
        assert {key.removeprefix(prefix): value for key, value in maps['composed_standalone_sha256'].items()} == composed['source_inputs']
        assert len(maps['composed_workspace_sha256']) == 66
        assert plan['current_recipe']['all5_tool_pins'] == expected['tool_sha256']
        assert plan['current_recipe']['entire_target_library_file_map'] == expected['target_libraries_sha256']
        assert plan['current_recipe']['empty_target_directories'] == ['self-contained']
        assert len(receipt['sdk_rust_libraries_sha256']) == plan['current_recipe']['recorded_sdk_rust_library_files'] == 1827
        assert {row['path'].removeprefix(prefix): (row['current_sha256'], row['composed_sha256'])
                for row in plan['only_authorized_source_changes']} == {
                    key: (value['before_sha256'], value['after_sha256']) for key, value in spec['changes'].items()}
    return spec, base, source, expected, composed, derived, patch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inspect', action='store_true')
    args = parser.parse_args(); assert __debug__
    spec, base, source, expected, composed, derived, patch = inspect()
    summary = {'base_commit': spec['base_commit'], 'base_expected': spec['base_expected'],
        'primary_files': 65, 'compiler_files': 66, 'changed_files': sorted(ALLOWED), 'other_inputs_fixed': 63,
        'builder_sha256': spec['base_builder_sha256'], 'adapter_patch': patch,
        'plan_files_bound': len(spec.get('plan_files', {})), 'composed_source_inputs': composed['source_inputs']}
    if args.inspect:
        print(json.dumps(summary, indent=2)); return
    assert spec.get('plan_files'), 'Root-reviewed sealed composition plan required before execution'
    assert platform.system() == 'Darwin' and platform.machine() == 'arm64' and sys.version_info >= (3, 12)
    io.WORK = ROOT / 'work/pump-current711-arithmetic'; io.EVIDENCE = io.WORK / 'evidence'
    work, evidence = io.WORK, io.EVIDENCE
    evidence.mkdir(parents=True, exist_ok=False)
    io.write(evidence / 'inputs.json', spec); io.write(evidence / 'inspection.json', summary)
    io.write(evidence / 'base-build-inputs.json', expected); io.write(evidence / 'composition-build-inputs.json', composed)
    io.write(evidence / 'host.json', {'system': platform.system(), 'machine': platform.machine(), 'python': sys.version,
        'revision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()})
    shutil.copyfile(Path(__file__), evidence / 'composition-controller.py')
    shutil.copyfile(Path(io.__file__), evidence / 'io-helper.py')
    shutil.copyfile(ROOT / '.github/workflows/qualify-pump-macos-v144.yml', evidence / 'workflow.yml')
    shutil.copyfile(base / 'build.py', evidence / 'qualified-current711-build.py')
    shutil.copyfile(base / 'builds/cold-01/build-attempt.json', evidence / 'base-build-attempt.json')
    shutil.copytree(PACKET / 'plan', evidence / 'sealed-plan')
    (evidence / 'measurement-adapter.patch').write_text(patch)
    repository = work / 'repository'; package = repository / 'research/composition-builder'
    staged = repository / 'source'; build = repository / 'build'
    try:
        package.mkdir(parents=True); (package / 'build.py').write_text(derived)
        io.write(package / 'build-inputs.json', composed)
        shutil.copytree(base / 'tools', package / 'tools', ignore=shutil.ignore_patterns('__pycache__'))
        for name, value in composed['source_inputs'].items():
            destination = staged / name; destination.parent.mkdir(parents=True, exist_ok=True)
            original = PACKET / spec['changes'][name]['file'] if name in ALLOWED else source / name
            shutil.copyfile(original, destination); assert io.sha(destination) == value
        with tarfile.open(evidence / 'primary-source.tar.gz', 'w:gz') as archive:
            for path in sorted(staged.rglob('*')):
                if path.is_file(): archive.add(path, arcname=path.relative_to(staged), recursive=False)
        original = repository / 'evidence/original/pump/deployed.so'; original.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / 'evidence/original/pump/deployed.so', original)
        downloads = {}
        for label, pin in spec['archives'].items():
            archive_path = work / (label + '.tar.bz2')
            with urllib.request.urlopen(pin['url'], timeout=120) as response, archive_path.open('wb') as output:
                shutil.copyfileobj(response, output)
            assert io.sha(archive_path) == pin['sha256']
            destination = work / label; destination.mkdir()
            with tarfile.open(archive_path) as archive: archive.extractall(destination, filter='data')
            downloads[label] = dict(pin, observed_sha256=io.sha(archive_path)); io.write(evidence / 'downloads.json', downloads)
        sdk = work / 'macos'; registry = work / 'cargo-home'
        libraries = work / 'linux/rust/lib/rustlib/sbpf-solana-solana/lib'
        env = dict(os.environ, CARGO_HOME=str(registry), RUSTC=str(sdk / 'rust/bin/rustc'),
            PATH=str(sdk / 'rust/bin') + os.pathsep + os.environ['PATH'])
        io.run('fetch', [sdk / 'rust/bin/cargo', 'fetch', '--locked', '--manifest-path', staged / 'Cargo.toml'], env)
        io.run('composition-build', [sys.executable, '-B', package / 'build.py', '--source-directory', staged,
            '--sdk', sdk, '--cargo-home', registry, '--target-library-profile', 'linux-v1.44-sbpf',
            '--target-libraries', libraries, '--wrapper', package / 'tools/pump_physical_source_wrapper.py', '--output', build])
        receipt = json.loads((build / 'build-attempt.json').read_text())
        assert all(receipt[key] for key in ['cold_empty_target', 'source_unchanged', 'tools_unchanged',
            'sdk_rust_libraries_unchanged', 'registry_sources_unchanged', 'target_libraries_unchanged'])
        bound_manifest(receipt['primary_source_sha256'], composed['source_inputs'])
        assert receipt['tool_sha256'] == expected['tool_sha256'] and receipt['target_libraries_sha256'] == expected['target_libraries_sha256']
        baseline_receipt = json.loads((base / 'builds/cold-01/build-attempt.json').read_text())
        assert receipt['sdk_rust_libraries_sha256'] == baseline_receipt['sdk_rust_libraries_sha256']
        plan_maps = json.loads((PACKET / 'plan/MANIFESTS.json').read_text())
        bound_manifest(receipt['source_sha256'], plan_maps['composed_workspace_sha256'])
        assert len(receipt['source_sha256']) == 66
        log = (build / 'build.log').read_text()
        assert '--crate-name pump_recovered ' in log and '--crate-name pump_token_ext ' in log
        assert inspect()[4] == composed
        io.write(evidence / 'RESULT.json', {'status': 'compiled-two-file-boundary-measurement-only', 'base_commit': spec['base_commit'],
            'base_expected': spec['base_expected'], 'changed_files': spec['changes'], 'other_inputs_fixed': 63,
            'primary_files': 65, 'compiler_files': len(receipt['source_sha256']), 'cold_empty_target': True,
            'both_local_crates_compiled': True, 'candidate_sha256': io.sha(build / 'candidate.so'),
            'unstripped_sha256': io.sha(build / 'unstripped.so'), 'base_hashes_equal': receipt['qualified_image_hashes_equal'],
            'limits': 'No current-source promotion, census gain, runtime acceptance or original whole-ELF identity claim.'})
        print((evidence / 'RESULT.json').read_text(), flush=True)
    finally:
        io.retain(build)


if __name__ == '__main__':
    main()
