#!/usr/bin/env python3
"""Verify the retained hosted control and its actual65-to66 compiler projection."""
import gzip
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import tarfile
import tomllib
import zipfile

HERE = Path(__file__).resolve().parent
digest = lambda data: hashlib.sha256(data).hexdigest()


def bound_manifest(actual, relative):
    """Check an exact relative file map despite the recorded runner root prefix."""
    first = next(iter(relative))
    prefixes = [name[:-len(first)] for name in actual if name.endswith(first)]
    assert sum(actual == {prefix + key: value for key, value in relative.items()}
               for prefix in prefixes) == 1, 'Compiler input membership/hash mismatch'


def candidate_measurements(expected, projected, frozen_builder):
    rows = json.loads((HERE / 'evidence/candidate-receipts.json').read_text())['measurements']
    terminal = b";assert record['qualified_image_hashes_equal']\n"
    assert frozen_builder.endswith(terminal)
    for row in rows:
        assert row['candidate'] in ['cto', 'sweep', 'perhop', 'sell-event', 'constructor', 'cto-used-flow', 'perhop-clock', 'sweep-read-timing']
        assert row['zip'] == row['candidate'] + '-' + str(int(row['run_id'])) + '.zip'
        archive = (HERE / 'evidence' / row['zip']).read_bytes()
        assert digest(archive) == row['zip_sha256']
        with zipfile.ZipFile(io.BytesIO(archive)) as zipped:
            names = zipped.namelist()
            assert len(names) == len(set(names))
            assert all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in names)
            files = {name: zipped.read(name) for name in names}
        manifest = json.loads(files['MANIFEST.json'])
        assert set(files) == set(manifest) | {'MANIFEST.json'}
        assert all(digest(files[name]) == value for name, value in manifest.items())
        result = json.loads(files['RESULT.json'])
        assert result == row['result'] and result['control_run'] == 40791064153
        assert result['status'] == 'compiled-measurement-only' and result['both_local_crates_compiled']
        proposal = json.loads(files['proposal.json'])
        assert proposal == result['proposal']
        assert proposal['before_sha256'] == expected['source_inputs'][proposal['source_path']]
        assert digest(files['proposed-source.rs']) == proposal['after_sha256']
        inputs = dict(expected['source_inputs'], **{proposal['source_path']: proposal['after_sha256']})
        compiler_inputs = dict(projected, **{'programs/pump/' + proposal['source_path']: proposal['after_sha256']})
        assert files['executed-builder.py'] == frozen_builder[:-len(terminal)] + b'\n'
        candidate_expected = json.loads(files['candidate-build-inputs.json'])
        assert candidate_expected == dict(expected, source_inputs=inputs)
        record = json.loads(files['build-attempt.json'])
        assert record['returncode'] == 0 and record['cold_empty_target'] and not record['target_existed_before']
        assert all(record[key] for key in ['source_unchanged', 'tools_unchanged', 'sdk_rust_libraries_unchanged',
            'registry_sources_unchanged', 'target_libraries_unchanged'])
        assert record['builder_sha256'] == digest(files['executed-builder.py'])
        assert record['tool_sha256'] == expected['tool_sha256']
        assert record['target_libraries_sha256'] == expected['target_libraries_sha256']
        assert record['source_wrapper_sha256'] == expected['source_wrapper_sha256']
        assert record['command'][1:] == ['build', '--manifest-path', record['source_directory'] + '/Cargo.toml',
                    '--locked', '--offline', '--release', '--target', 'sbpf-solana-solana', '-vv']
        assert record['environment']['CARGO_TARGET_SBPF_SOLANA_SOLANA_RUSTFLAGS'] == '-Zremap-cwd-prefix='
        bound_manifest(record['primary_source_sha256'], inputs)
        bound_manifest(record['source_sha256'], compiler_inputs)
        assert record['source_sha256'] == record['source_after_sha256']
        assert record['primary_source_sha256'] == record['primary_source_after_sha256']
        with tarfile.open(fileobj=io.BytesIO(files['compiled-source.tar.gz']), mode='r:gz') as tar:
            members = tar.getmembers()
            assert all(member.isfile() for member in members)
            assert len(members) == len(set(member.name for member in members))
            assert {member.name: digest(tar.extractfile(member).read()) for member in members} == compiler_inputs
        for key, filename in [('candidate_sha256', 'candidate.so'), ('unstripped_sha256', 'unstripped.so')]:
            assert digest(files[filename]) == result[key]
        assert record['unstripped_sha256'] == result['unstripped_sha256']
        assert record['comparison']['candidate_sha256'] == result['candidate_sha256']
        assert record['qualified_image_hashes_equal'] == result['control_hashes_equal']
        assert result['control_hashes_equal'] == (result['candidate_sha256'] == expected['comparison']['candidate_sha256']
                and result['unstripped_sha256'] == expected['unstripped_sha256'])
        log = gzip.decompress(files['build.log.gz'])
        assert digest(log) == record['build_log_sha256']
        assert b'--crate-name pump_recovered ' in log and b'--crate-name pump_token_ext ' in log
    return len(rows)


def retained_census():
    directory = HERE / 'evidence/census'
    baseline = json.loads(gzip.decompress((directory / 'baseline-inventory.json.gz').read_bytes()))
    assert baseline['candidate_sha256'] == '49df399b8a36a0a60de03e8d55f1417261dc451e44845ca9d17a94040968c680'
    measurements = json.loads((HERE / 'evidence/candidate-receipts.json').read_text())['measurements']
    checked = 0
    for measurement in measurements:
        path = directory / (measurement['candidate'] + '-' + str(measurement['run_id']))
        if not path.is_dir():
            continue
        compressed = (path / 'inventory.json.gz').read_bytes()
        candidate = json.loads(gzip.decompress(compressed))
        delta = json.loads((path / 'delta.json').read_text())
        assert delta['inventory_sha256'] == digest(compressed)
        assert candidate['candidate_sha256'] == delta['candidate_symbols_sha256'] == measurement['result']['unstripped_sha256']
        assert len(baseline['windows']) == len(candidate['windows']) == 1035
        for inventory in [baseline, candidate]:
            windows = inventory['windows']
            normalized = sum(bool(row['normalized_matches']) for row in windows)
            assert inventory['counts'] == {'total': len(windows), 'normalized': normalized,
                'raw': sum(row['raw_match'] for row in windows), 'unmatched': len(windows) - normalized,
                'matched_text_bytes': sum(row['bytes'] for row in windows if row['normalized_matches'])}
        changes = []
        for before, after in zip(baseline['windows'], candidate['windows']):
            assert all(before[key] == after[key] for key in ['start', 'end', 'bytes', 'raw_sha256'])
            states = lambda row: {'normalized': bool(row['normalized_matches']), 'raw': row['raw_match']}
            old, new = states(before), states(after)
            if old != new:
                changes.append({'original_start': before['start'], 'original_start_hex': hex(before['start']),
                    'bytes': before['bytes'], 'before': old, 'after': new})
        assert changes == delta['all_match_changes']
        assert delta['gained'] == [r for r in changes if any(not r['before'][k] and r['after'][k] for k in ['normalized', 'raw'])]
        assert delta['lost'] == [r for r in changes if any(r['before'][k] and not r['after'][k] for k in ['normalized', 'raw'])]
        assert delta['no_window_regressions'] == (not delta['lost'])
        assert delta['baseline_counts'] == baseline['counts'] and delta['candidate_counts'] == candidate['counts']
        checked += 1
    return checked


def main():
    assert __debug__, 'Optimized Python is unsupported'
    packet_manifest = json.loads((HERE / 'MANIFEST.json').read_text())
    packet_files = {p.relative_to(HERE).as_posix(): p for p in HERE.rglob('*')
                    if p.is_file() and p != HERE / 'MANIFEST.json'}
    assert all(not p.is_symlink() and p.resolve().is_relative_to(HERE) for p in packet_files.values())
    assert set(packet_files) == set(packet_manifest)
    assert all(digest(packet_files[name].read_bytes()) == value for name, value in packet_manifest.items())
    spec = json.loads((HERE / 'inputs.json').read_text())
    archive = (HERE / 'evidence/control-40791064153.zip').read_bytes()
    assert digest(archive) == 'b3e31aeb7512b6cec0e1aede4efbb16e72edf047451065a1e5b476223230a6ce'
    with zipfile.ZipFile(io.BytesIO(archive)) as zipped:
        names = zipped.namelist()
        assert len(names) == len(set(names))
        assert all(not PurePosixPath(name).is_absolute() and '..' not in PurePosixPath(name).parts for name in names)
        files = {name: zipped.read(name) for name in names}
    manifest = json.loads(files['MANIFEST.json'])
    assert set(files) == set(manifest) | {'MANIFEST.json'}
    assert all(digest(files[name]) == expected for name, expected in manifest.items())
    assert digest(files['build-inputs.json']) == spec['build_inputs_sha256']
    assert digest(files['executed-builder.py']) == spec['builder_sha256']
    expected = json.loads(files['build-inputs.json'])
    result, record = [json.loads(files[name]) for name in ['RESULT.json', 'build-attempt.json']]
    run = json.loads((HERE / 'evidence/control-run.json').read_text())
    host = json.loads(files['host.json'])
    assert run['id'] == 40791064153 and run['event'] == 'workflow_dispatch' and run['conclusion'] == 'success'
    assert run['head_sha'] == host['revision'] == 'c6ae78c36ef59de4f1b2a057b54e57b6c9f3dce7'
    assert host['system'] == 'Darwin' and host['machine'] == 'arm64'
    assert result['base_commit'] == spec['base_commit'] and result['status'] == 'reproduced'
    for key, name in [('candidate_sha256', 'candidate.so'), ('unstripped_sha256', 'unstripped.so')]:
        assert digest(files[name]) == spec['expected'][key] == result[key]
    assert record['returncode'] == 0 and not record['target_existed_before']
    assert all(record[key] for key in ['cold_empty_target', 'source_unchanged', 'tools_unchanged',
        'sdk_rust_libraries_unchanged', 'registry_sources_unchanged', 'target_libraries_unchanged', 'qualified_image_hashes_equal'])
    assert record['builder_sha256'] == spec['builder_sha256']
    assert record['source_wrapper_sha256'] == expected['source_wrapper_sha256']
    assert record['tool_sha256'] == expected['tool_sha256']
    assert record['target_libraries_sha256'] == expected['target_libraries_sha256']
    assert record['command'][1:] == ['build', '--manifest-path', record['source_directory'] + '/Cargo.toml',
                                   '--locked', '--offline', '--release', '--target', 'sbpf-solana-solana', '-vv']
    assert record['environment']['CARGO_TARGET_SBPF_SOLANA_SOLANA_RUSTFLAGS'] == '-Zremap-cwd-prefix='
    assert record['source_sha256'] == record['source_after_sha256']
    assert record['primary_source_sha256'] == record['primary_source_after_sha256']
    bound_manifest(record['primary_source_sha256'], expected['source_inputs'])
    # Derive the exact compiler projection independently from the frozen primary
    # Cargo input, rather than treating the builder's own manifest as the oracle.
    primary = (HERE / 'evidence/source-input-Cargo.toml').read_bytes()
    assert digest(primary) == expected['source_inputs']['Cargo.toml']
    text = primary.decode(); start = text.index('[profile.release]'); end = text.index('[workspace]')
    projected = {'programs/pump/' + key: value for key, value in expected['source_inputs'].items()
                 if key not in ['Cargo.toml', 'Cargo.lock']}
    projected['Cargo.lock'] = expected['source_inputs']['Cargo.lock']
    projected['programs/pump/Cargo.toml'] = digest((text[:start].rstrip() + '\n').encode())
    projected['Cargo.toml'] = digest(('[workspace]\nmembers = ["programs/pump"]\nresolver = "2"\n\n' + text[start:end].strip() + '\n').encode())
    with tarfile.open(fileobj=io.BytesIO(files['compiled-source.tar.gz']), mode='r:gz') as tar:
        members = tar.getmembers()
        assert len(members) == len(set(member.name for member in members))
        assert all(member.isfile() and not PurePosixPath(member.name).is_absolute()
                   and '..' not in PurePosixPath(member.name).parts for member in members)
        actual_source = {member.name: tar.extractfile(member).read() for member in members}
    assert {name: digest(data) for name, data in actual_source.items()} == projected
    assert len(expected['source_inputs']) == 65 and len(projected) == 66
    bound_manifest(record['source_sha256'], projected)
    registry = json.loads(files['registry-authentication.json'])
    assert digest(files['registry-authentication.json']) == record['registry_authentication_sha256']
    locked = {package['name'] + '-' + package['version']: package['checksum']
              for package in tomllib.loads(actual_source['Cargo.lock'].decode())['package']
              if package.get('source', '').startswith('registry+')}
    assert {name: item['sha256'] for name, item in registry['locked_registry_archives'].items()} == locked
    assert sum(len(entries) for entries in registry['actual_registry_source_files'].values()) == registry['files_checked']
    log = gzip.decompress(files['build.log.gz'])
    assert digest(log) == record['build_log_sha256']
    assert b'--crate-name pump_recovered ' in log and b'--crate-name pump_token_ext ' in log
    measurements = candidate_measurements(expected, projected, files['executed-builder.py'])
    censuses = retained_census()
    print(json.dumps({'control_run': run['id'], **spec['expected'], 'primary_source_files': 65,
        'compiled_source_files': 66, 'locked_registry_packages': len(locked), 'independent_candidate_measurements': measurements,
        'retained_census_deltas': censuses,
        'limits': 'Actual hosted build/source bindings and retained delta arithmetic; no fresh normalizer/runtime/original identity claim.'}, indent=2))


if __name__ == '__main__':
    main()
