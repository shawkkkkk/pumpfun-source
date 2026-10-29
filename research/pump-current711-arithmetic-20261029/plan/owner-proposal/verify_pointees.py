"""Recompute all narrowly masked data bindings in the consumed helper bodies."""
from pathlib import Path
import hashlib
import json
import struct
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, '/workspace/pumpfun-source-latest/scripts')
from pump_compare_function_bytes import body, normalize
from pump_quote_control_function_match import sections

sha = lambda data: hashlib.sha256(data).hexdigest()


def main():
    closure = json.loads((HERE / 'HELPER-CLOSURE.json').read_bytes())
    images = {
        'original': Path('/workspace/pumpfun-source-latest/evidence/original/pump/deployed.so').read_bytes(),
        'current': Path('/workspace/pump-current673-native-results/perhop-clock-40795474496/unstripped.so').read_bytes(),
    }
    sec = {label: sections(image) for label, image in images.items()}

    def data(label, address, count):
        matches = [s for s in sec[label].values() if s['addr'] > 0 and s['addr'] <= address < address + count <= s['addr'] + s['size']]
        assert len(matches) == 1
        s = matches[0]
        at = s['offset'] + address - s['addr']
        return images[label][at:at + count]

    def matched(record):
        values = {}
        for label in images:
            at = int(record[label], 16)
            raw = body(images[label], sec[label], at, record['bytes'])
            normalized, ops = normalize(raw, at, sec[label])
            assert sha(normalized) == record['normalized_sha256']
            values[label] = {op['offset']: op for op in ops}
        return values

    total_pointers, total_edges, vtable_methods = 0, 0, set()
    for helper in closure['helpers']:
        operands = matched(helper)
        pointers = [{int(row['offset'], 16) for row in helper['masked_pointees']}]
        for label in images:
            assert {at for at, op in operands[label].items() if op['kind'] == 'elf-pointer'} == pointers[0]
        total_pointers += len(pointers[0])
        calls = {int(row['offset'], 16): row for row in helper['actual_direct_callees']}
        for label in images:
            assert {at for at, op in operands[label].items() if op['kind'] == 'direct-call'} == set(calls)
            assert all(operands[label][at]['target'] == int(row[label], 16) for at, row in calls.items())
        for row in calls.values():
            matched(row)
        total_edges += len(calls)
        for row in helper['masked_pointees']:
            at = int(row['offset'], 16)
            kind = row['kind']
            if kind in ['error_ordinal', 'Source_filename', 'unwrap_message']:
                for label in images:
                    address = operands[label][at]['value']
                    assert address == int(row[label], 16)
                    raw = data(label, address, row['bounded_bytes'])
                    assert sha(raw) == row['sha256']
                    if kind == 'error_ordinal':
                        assert struct.unpack('<I', raw)[0] == row['value']
                    else:
                        assert raw.decode() == row['value']
            elif kind == 'used_vtable':
                table = row['closure']
                for label in images:
                    address = operands[label][at]['value']
                    assert address == int(table[label], 16)
                    words = struct.unpack('<' + 'Q' * table['bounded_words'], data(label, address, 8 * table['bounded_words']))
                    assert words[1:3] == (table['size'], table['alignment'])
                    for method in table['methods']:
                        # Captured SBPF ELF relocatable data pointers occupy the high DWORD.
                        assert words[method['slot']] == int(method[label], 16) << 32
                        matched(method)
                        vtable_methods.add((method['normalized_sha256'], method['bytes']))
            elif kind == 'panic_Location':
                for label in images:
                    pointer, length, line, column = struct.unpack('<QQII', data(label, operands[label][at]['value'], row['bounded_bytes']))
                    assert pointer & 0xffffffff == 0
                    assert (length, line, column) == (row['filename_bytes'], row['line'], row['column'])
                    filename = data(label, pointer >> 32, length)
                    assert sha(filename) == row['filename_sha256'] and filename.decode() == row['filename']
            else:
                raise ValueError(kind)
    assert total_pointers == 33
    report = {'status': 'PASS', 'helper_bodies': len(closure['helpers']),
              'complete_direct_callee_edges_checked': total_edges,
              'masked_ELF_pointer_operands_closed': total_pointers,
              'unique_used_vtable_method_bodies_checked': len(vtable_methods),
              'actual_images_sha256': {label: sha(image) for label, image in images.items()},
              'HELPER_CLOSURE_sha256': sha((HERE / 'HELPER-CLOSURE.json').read_bytes()),
              'limits': 'All masked data operands of these five helper bodies and their listed used vtables are bounded and verified. Direct callee full normalized identities are checked; this does not claim blanket transitive stdlib pointee closure or unique historical source.'}
    (HERE / 'POINTEES-VERIFIED.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
