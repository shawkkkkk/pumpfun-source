#!/usr/bin/env python3
"""Challenge strict380 checks using retained genuinely signed outcomes."""
import base64
import copy
from pathlib import Path
import unittest

import verify

P = Path(__file__).resolve().parent
runtime = verify.load('executed_cto380_controller',P/'runtime-tools/replay.py')
runtime.P = P/'runtime-tools'
REPORT = verify.read(P/'runtime/broad.json.gz')
LOADER = verify.read(P/'runtime/broad-loader.json')
MANIFEST = verify.read(P/'runtime-tools/INPUTS.json')
IMAGE = verify.read(P/'MEASUREMENT.json')['candidate_sha256']


class Controls(unittest.TestCase):
    def check(self, report, loader=LOADER):
        return runtime.verify_report('broad',report,loader,IMAGE,MANIFEST)

    def test_actual_Source_filename_mutation_detected(self):
        report = copy.deepcopy(REPORT)
        row = next(row for row in report['cases'] if any('.rs:' in line for line in row['candidate']['logs']))
        index = next(index for index,line in enumerate(row['candidate']['logs']) if '.rs:' in line)
        row['candidate']['logs'][index] = row['candidate']['logs'][index].replace('.rs:','-changed.rs:')
        self.assertTrue(any('full_ordered_non_CU_logs' in row['different'] for row in self.check(report)['differences']))

    def test_invalid_actual_signature_rejected(self):
        report = copy.deepcopy(REPORT)
        raw = bytearray(base64.b64decode(report['cases'][0]['original']['transaction_base64']))
        raw[1] ^= 1
        for label in ['original','candidate']:
            report['cases'][0][label]['transaction_base64'] = base64.b64encode(raw).decode()
        with self.assertRaisesRegex(ValueError,'actual signature verification'):
            self.check(report)

    def test_changed_loader_prefix_rejected(self):
        loader = copy.deepcopy(LOADER)
        loader['loads'][0]['elf_prefix_unchanged'] = False
        with self.assertRaisesRegex(ValueError,'captured loader fidelity'):
            self.check(REPORT,loader)

    def test_only_exact_standard_compute_line_may_differ(self):
        report = copy.deepcopy(REPORT)
        lines = report['cases'][0]['candidate']['logs']
        index = next(index for index,line in enumerate(lines) if runtime.CU.fullmatch(line))
        lines[index] = 'Program 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P consumed 1 of 1400000 compute units'
        self.assertFalse(self.check(report)['differences'])


if __name__ == '__main__':
    unittest.main()
