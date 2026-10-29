#!/usr/bin/env python3
"""Offline exact-source/native/call/census and strict380 qualification checks."""
import argparse
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tarfile

P = Path(__file__).resolve().parent
sha = lambda data: hashlib.sha256(data).hexdigest()


def read(path):
    data = Path(path).read_bytes()
    return json.loads(gzip.decompress(data) if data.startswith(b'\x1f\x8b') else data)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V = load('cto_stage1_verifier', P.parent/'verify.py')
require = V.require


def symbols(elf):
    table, strings = elf.sections['.symtab'], elf.sections['.strtab']
    data = elf.data[strings[4]:strings[4]+strings[5]]
    result = []
    for offset in range(table[4], table[4]+table[5], table[9] or 24):
        name, info, other, section, value, size = struct.unpack_from('<IBBHQQ', elf.data, offset)
        if info & 15 == 2 and size:
            result.append((data[name:].split(b'\0',1)[0].decode(), value, size))
    return result


def exactly(rows, marker):
    found = [row for row in rows if marker in row[0]]
    require(len(found) == 1, 'unique actual symbol: '+marker)
    return found[0]


def without_call_immediates(data):
    result = bytearray(data)
    offset = 0
    while offset < len(result):
        if result[offset] == 0x85:
            result[offset+4:offset+8] = bytes(4)
        offset += 16 if result[offset] == 0x18 else 8
    return bytes(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=P.parents[2])
    args = parser.parse_args()
    root = args.repo.resolve()
    record = read(P/'MEASUREMENT.json')
    for name, digest in record['files'].items():
        require(sha((P/name).read_bytes()) == digest, 'stage2 artifact: '+name)
    for name, digest in read(P/'native-build/MANIFEST.json').items():
        require(sha((P/'native-build'/name).read_bytes()) == digest, 'complete native manifest: '+name)
    before, after = (P/'source/f4-before.rs').read_bytes(), (P/'source/admin_cto.rs').read_bytes()
    require(sha(before) == 'f4a2bb7d33431e0fb4911e39d5e03c8bb9f45c6f7a184da21d1a6762f9127955', 'exact f4 parent source')
    require(sha(after) == '5203d20c2e63be7337204491588e0ec69808f8ddd39d96b8b5fa1964d6ec201d', 'exact final source')
    require(V.source_sites(before.decode()) == V.source_sites(after.decode()), 'explicit Source/panic token positions')
    require(before.count(b'\n') == 775 and after.count(b'\n') == 772, 'honest natural helper deletion/line drift')
    build = read(P/'native-build/build-comparison.json')
    attempt = read(P/'native-build/build-attempt.json')
    canonical = read(P.parent/'native-build/canonical-SOURCE-FROZEN.json')['source_files']
    primary = {name.removeprefix('source/'): value for name, value in build['primary_source_sha256'].items()}
    require(set(primary) == set(canonical) and len(primary) == 65, 'same65 primary source inputs')
    require([name for name in primary if primary[name] != canonical[name]] == ['src/creator/admin_cto.rs'], 'one canonical source delta')
    require(primary['src/creator/admin_cto.rs'] == sha(after), 'actual native source')
    require(attempt['source_sha256'] == build['source_sha256'], 'actual attempt binding')
    with tarfile.open(P/'native-build/compiled-source.tar.gz') as archive:
        files = [member for member in archive.getmembers() if member.isfile()]
        actual = {'build/source/'+member.name: sha(archive.extractfile(member).read()) for member in files}
    require(len(actual) == 66 and actual == build['source_sha256'], 'all66 actual compiler inputs')
    require(build['cold_empty_target'] and not build['target_existed_before'], 'actual empty target')
    log = gzip.decompress((P/'native-build/build.log.gz').read_bytes()).decode()
    require(all('Compiling '+crate+' v0.1.0' in log for crate in ['pump-token-ext','pump-recovered']), 'both local crates actually compiled')
    image = (P/'native-build/candidate.so').read_bytes()
    elf = V.Elf(P/'native-build/unstripped.so')
    require(sha(image) == record['candidate_sha256'] == build['comparison']['candidate_sha256'], 'actual image binding')
    require(sha(elf.data) == record['unstripped_sha256'], 'actual symbol image')
    syms = symbols(elf)
    _, start, size = exactly(syms, 'admin_cto7execute')
    require((start,size) == (0x2fd30,18464), 'actual CTO body')
    calls, external = elf.calls(start,size)
    require(len(calls) == 178 and len(external) == 3, 'actual outgoing calls')
    counts = {}
    for label, marker, expected in [('clone','AccountInfo$u20$as$u20$core..clone..Clone$GT$5clone',54),
                                     ('ATA','associated_token17create_idempotent',2),
                                     ('transfer','collect_v221transfer_vault_tokens',1),
                                     ('raw','admin_cto16token_raw_amount',2),
                                     ('frozen','admin_cto12token_frozen',5)]:
        name, target, length = exactly(syms, marker)
        counts[label] = sum(value == target for _,value in calls)
        require(counts[label] == expected, 'actual used call count '+label)
    require(not [row for row in syms if 'admin_cto9pay_token' in row[0]], 'obsolete pay_token boundary absent')
    audit = read(P/'independent-audit/SUMMARY.json')
    require(sha((P/'independent-audit/SUMMARY.json').read_bytes()) == 'a33c849cac9a929795aa2e03f3dca55b5f4b2554a0181851f850985b7cd624d2', 'frozen independent actual audit')
    for name, row in audit['files'].items():
        require(sha((P/'independent-audit'/name).read_bytes()) == row['sha256'], 'exact independent producer/report: '+name)
    require(audit['images']['5203'] == sha(elf.data) and audit['source_sha256'] == sha(after), 'independent actual image/source binding')
    require(audit['holder_extra_copy_removed'] and audit['three_program_first_context_groups_reproduce_original_source_pointer_order'], 'actual original-backed copy/order observations')
    parent = V.Elf(P.parent/'native-build/unstripped.so')
    _, old_raw, old_size = exactly(symbols(parent),'admin_cto16token_raw_amount')
    _, new_raw, new_size = exactly(syms,'admin_cto16token_raw_amount')
    require(old_size == new_size == 448, 'same used raw helper')
    require(without_call_immediates(parent.body(old_raw,448)) == without_call_immediates(elf.body(new_raw,448)), 'all non-CALL helper bytes unchanged')
    for item, position in [(parent,old_raw),(elf,new_raw)]:
        row = item.sections['.rel.dyn']
        addresses = [struct.unpack_from('<QQ',item.data,offset)[0] for offset in range(row[4],row[4]+row[5],16)]
        require(not any(position <= value < position+448 for value in addresses), 'raw helper has no emitted data/Location relocation')
    delta, inventory = read(P/'census/delta.json'), read(P/'census/inventory.json.gz')
    require(sha((P/'census/inventory.json.gz').read_bytes()) == delta['inventory_sha256'], 'complete census bytes')
    require(delta['candidate_symbols_sha256'] == sha(elf.data) == inventory['candidate_sha256'], 'census exact image')
    require(len(inventory['windows']) == 1035 and delta['baseline_counts'] == delta['candidate_counts'] and not delta['gained'] and not delta['lost'] and not delta['all_match_changes'], 'zero gains/losses in complete1035')
    fixture = read(P/'runtime-tools/INPUTS.json')
    for name, row in fixture['files'].items():
        require(sha((root/name).read_bytes()) == row['sha256'], 'unchanged actual fixture tool/capture: '+name)
    runtime = load('cto_used_flow_executed_controller',P/'runtime-tools/replay.py')
    runtime.P, runtime.REPO = P/'runtime-tools', root
    execution = read(P/'runtime/execution.json')
    require(execution['candidate_sha256'] == sha(image) and execution['source_sha256'] == sha(after), 'fresh actual replay binding')
    require(len(execution['runs']) == 3, 'all3 affected suites')
    totals = {'case_records':0,'actual_signed_executions':0,'signature_fields_verified':0}
    for row in execution['runs']:
        kind = row['name']
        report = read(P/'runtime'/('broad.json.gz' if kind == 'broad' else kind+'.json.gz'))
        if kind == 'broad':
            archive = read(P/'runtime/broad-archive.json')
            require(sha(gzip.decompress((P/'runtime/broad.json.gz').read_bytes())) == row['report_sha256'] == archive['raw_sha256'], 'lossless unchanged broad report')
        else:
            require(sha((P/'runtime'/(kind+'.json.gz')).read_bytes()) == row['report_sha256'], 'actual raw report binding')
        result = runtime.verify_report(kind,report,read(P/'runtime'/(kind+'-loader.json')),sha(image),fixture)
        require(row['returncode'] == 0 and result == row['verification'] and not result['differences'], 'strict actual affected replay')
        for key in totals:
            totals[key] += result[key]
    require(totals == {'case_records':380,'actual_signed_executions':777,'signature_fields_verified':1550}, 'finite actual suite totals')
    print(json.dumps({'source_sha256':sha(after),'candidate_sha256':sha(image),'unstripped_sha256':sha(elf.data),
                      'native_compiler_input_files':66,'both_local_crates_compiled':True,
                      'defined_CTO_calls':178,'actual_call_counts':counts,'lexical_raw_helper_line_shift':'775→772; no non-CALL instruction or direct helper data/Location relocation change',
                      'normalized_windows':1019,'raw_windows':188,'gains':0,'losses':0,'runtime':totals,
                      'ordered_Source_or_structured_differences':0,'Source_substitutions':None,
                      'residual':'54direct/0inline copies vsoriginal33direct+21inline; fullcaller/wholeELF equality unresolved',
                      'canonical_selection_changed':False},indent=2))


if __name__ == '__main__':
    main()
