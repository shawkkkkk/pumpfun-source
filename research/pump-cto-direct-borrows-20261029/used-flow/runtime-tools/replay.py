#!/usr/bin/env python3
"""Existing CTO/shared/pool/collect witnesses for the sole5203 used-flow proposal."""
import argparse
import base64
import collections
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from solders.pubkey import Pubkey
from solders.transaction import VersionedTransaction

P = Path(__file__).resolve().parent
REPO = P.parent/'runtime-control/repo'
sha = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
CU = re.compile(r'^Program [1-9A-HJ-NP-Za-km-z]+ consumed [0-9]+ of [0-9]+ compute units$')
PID = Pubkey.from_string('6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P')


def require(ok, why):
    if not ok:
        raise ValueError(why)


def read(path):
    data = Path(path).read_bytes()
    return json.loads(gzip.decompress(data) if data.startswith(b'\x1f\x8b') else data)


def check_inputs():
    manifest = read(P/'INPUTS.json')
    for name, row in manifest['files'].items():
        require(sha(REPO/name) == row['sha256'], 'frozen tool/capture: '+name)
    for name, digest in manifest['additional_inputs'].items():
        require(sha(P/name) == digest, 'frozen inherited input: '+name)
    require(sha(sys.executable) == manifest['toolchain']['python_executable_sha256'], 'Python executable changed')
    import solders.solders as native
    require(sha(native.__file__) == manifest['toolchain']['solders_native_sha256'], 'native runtime changed')
    return manifest


def signed(row, labels):
    # All inherited fixtures use this fixed synthetic mint; wrong-mint negative
    # inputs intentionally change the meta, not the genuine pool-authority PDA.
    mint = Pubkey.from_bytes(bytes([61])*32)
    pool_authority = Pubkey.find_program_address([b'pool-authority', bytes(mint)], PID)[0]
    total = 0
    for label in labels:
        result = row[label]
        require(result['transaction_base64'] == row['original']['transaction_base64'], 'different transaction input')
        raw = base64.b64decode(result['transaction_base64'], validate=True)
        tx = VersionedTransaction.from_bytes(raw)
        checks = tx.verify_with_results()
        require(bytes(tx) == raw and checks and all(checks) and result['signatures_verified'], 'actual signature verification')
        required = tx.message.header.num_required_signatures
        require(required == len(tx.signatures), 'signature count/header')
        require(pool_authority not in tx.message.account_keys[:required] and not result['pool_authority_top_level_signer'], 'privileged outer PDA signer')
        instructions = [ix for ix in tx.message.instructions if tx.message.account_keys[ix.program_id_index] == PID]
        require(len(instructions) == 1 and bytes(instructions[0].data[:8]) == hashlib.sha256(b'global:admin_cto').digest()[:8], 'actual CTO outer instruction')
        total += len(tx.signatures)
    return total


def verify_report(kind, report, loader, candidate_sha, manifest):
    count = {'broad': 363, 'cto': 5, 'shared': 12}[kind]
    require(report['case_count'] == len(report['cases']) == count, 'exact inherited case count')
    require(report['candidate_sha256'] == candidate_sha and not report['mismatches'], 'actual candidate/structured result')
    labels = ['original', 'candidate'] if kind == 'broad' else ['original', 'baseline', 'candidate']
    if kind == 'broad':
        require([r['case'] for r in report['cases']] == read(P/'inputs/broad-cases.json'), 'unchanged363 definitions/order')
    signatures, differences = 0, []
    for row in report['cases']:
        signatures += signed(row, labels)
        a, b = row['original'], row['candidate']
        fields = [name for name in ['error', 'before', 'after', 'events', 'inner', 'return'] if a[name] != b[name]]
        logs = lambda result: [line for line in result['logs'] if not CU.fullmatch(line)]
        if logs(a) != logs(b):
            fields.append('full_ordered_non_CU_logs')
        if fields:
            differences.append({'case': row['case']['name'], 'different': fields})
    original_sha = manifest['files']['evidence/original/pump/deployed.so']['sha256']
    wanted = collections.Counter({original_sha: count})
    wanted.update({candidate_sha: count})
    if kind != 'broad':
        wanted.update({report['baseline_sha256']: count})
    require(collections.Counter(row['elf_sha256'] for row in loader['loads']) == wanted, 'all actual captured loads')
    for row in loader['loads']:
        require(row['elf_prefix_unchanged'] and row['zero_allocation_tail'] and row['program_bytes'] == 36 and row['programdata_bytes'] == 10485760, 'captured loader fidelity')
    return {'case_records': count, 'actual_signed_executions': count*len(labels),
            'signature_fields_verified': signatures, 'differences': differences,
            'Source_substitutions': None, 'pool_authority_outer_signer': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=Path)
    parser.add_argument('--candidate-sha256')
    parser.add_argument('--build-record', type=Path)
    parser.add_argument('--source', type=Path, default=P.parent/'candidates/used-cpi-flow/admin_cto.rs')
    parser.add_argument('--parent', type=Path, default=Path('/workspace/pump-current673-native-results/cto-40792775552/candidate.so'))
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check-inputs', action='store_true')
    args = parser.parse_args()
    require(__debug__, 'run without -O; unchanged original fixtures/loader use assertions')
    manifest = check_inputs()
    if args.check_inputs:
        print(json.dumps({'frozen_input_count': len(manifest['files'])+len(manifest['additional_inputs']), 'case_records': 380, 'new_VM_executions': 0}, indent=2))
        return
    require(args.candidate is not None and args.candidate_sha256 and args.build_record is not None and args.output is not None, 'actual candidate/hash/build receipt and fresh output required')
    candidate, parent, source, build, out = [item.resolve() for item in [args.candidate, args.parent, args.source, args.build_record, args.output]]
    require(sha(candidate) == args.candidate_sha256, 'actual candidate image')
    require(sha(parent) == manifest['parent_image_sha256'], 'actual f4 parent image')
    require(sha(source) == manifest['candidate_source_sha256'], 'exact5203 source')
    require(not out.exists(), 'preserve prior results; fresh output required')
    out.mkdir(parents=True)
    bound = {str(path): sha(path) for path in [candidate, parent, source, build, Path(__file__), P/'INPUTS.json']}
    commands = [('broad', REPO/'scripts/pump_admin_cto_differential.py', [], out/'broad.json'),
                ('cto', P/'inputs/cto-focused.py', [], out/'cto.json.gz'),
                ('shared', P/'inputs/shared-holder-focused.py', ['--baseline', str(parent)], out/'shared.json.gz')]
    results = []
    for kind, producer, extra, report in commands:
        loader = out/(kind+'-loader.json')
        command = [sys.executable, '-B', str(REPO/'scripts/pump_with_captured_loader.py'), '--receipt', str(loader), str(producer), '--candidate', str(candidate), *extra, '--output', str(report)]
        with (out/(kind+'.log')).open('w') as log:
            run = subprocess.run(command, cwd=REPO, stdout=log, stderr=subprocess.STDOUT)
        row = {'name': kind, 'command': command, 'returncode': run.returncode,
               'producer_sha256': sha(producer), 'report_sha256': sha(report) if report.exists() else None}
        if report.exists():
            row['verification'] = verify_report(kind, read(report), read(loader), args.candidate_sha256, manifest)
        results.append(row)
        (out/'execution.json').write_text(json.dumps({'input_sha256': bound, 'runs': results,
            'candidate_sha256': args.candidate_sha256, 'source_sha256': manifest['candidate_source_sha256'],
            'build_record_binding': 'provided actual bytes hash; independently authenticate compiler/source receipt',
            'Source_normalization': None}, indent=2)+'\n')
        check_inputs()
        require(all(sha(path) == digest for path, digest in bound.items()), 'input changed during actual replay')
        require(run.returncode == 0 and not row['verification']['differences'], 'actual strict difference; all raw results retained')
        print(kind, row['verification'], flush=True)


if __name__ == '__main__':
    main()
