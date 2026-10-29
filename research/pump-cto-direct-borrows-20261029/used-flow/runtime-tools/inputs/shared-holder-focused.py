"""Signed shared-holder validation/zero-balance/frozen-vault comparisons."""
from pathlib import Path
import argparse, base64, gzip, hashlib, inspect, json, sys
sys.path.insert(0, '/workspace/pump-admin-cto/runtime-control/repo/scripts')
import pump_admin_cto_differential as f
from solders.transaction import Transaction

# Change only an input which the stock fixture fixes to its expected PDA. Its
# ATA, account data and instruction metas continue to be constructed normally.
source = inspect.getsource(f.run)
needle = ' for key in [vault,holdervault,ammvault,'
assert source.count(needle) == 1
source = source.replace(needle, " holdervault=Pubkey.from_string(c.get('holder_vault',str(holdervault)))\n" + needle)
ns = dict(f.__dict__)
exec(compile(source, __file__ + ':fixture-key-input', 'exec'), ns)
run = ns['run']

p = argparse.ArgumentParser()
p.add_argument('--candidate', type=Path, required=True)
p.add_argument('--baseline', type=Path)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
stable = str(f.Pubkey.from_bytes(bytes([88]) * 32))
token22 = 'TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb'
cases = []
for label, quote in [('native', {}), ('token', {'quote': stable}),
                     ('token22', {'quote': stable, 'token_program': token22})]:
    cases.append({'name': 'empty-wrong-holder-' + label, 'holder': True, 'new_none': True,
                  'holder_vault': str(f.OTHER.pubkey()), **quote})
for token22_mode in [False, True]:
    for name in ['coin_creator_vault_ata', 'creator_vault_quote_token_account']:
        cases.append({'name': 'positive-frozen-' + name + ('-token22' if token22_mode else '-token'),
                      'holder': True, 'new_none': True, 'quote': stable,
                      **({'token_program': token22} if token22_mode else {}),
                      'accounts': {name: {'tokens': 1, 'patches': [[108, '02']]}}})
for name in ['coin_creator_vault_ata', 'creator_vault_quote_token_account']:
    cases.append({'name': 'wrong-holder-positive-frozen-' + name, 'holder': True, 'new_none': True,
                  'quote': stable, 'holder_vault': str(f.OTHER.pubkey()),
                  'accounts': {name: {'tokens': 1, 'patches': [[108, '02']]}}})
    cases.append({'name': 'zero-frozen-' + name, 'holder': True, 'new_none': True,
                  'quote': stable, 'accounts': {name: {'tokens': 0, 'patches': [[108, '02']]}}})
cases.append({'name': 'empty-valid-holder-token', 'holder': True, 'new_none': True, 'quote': stable})

sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
program_messages = lambda r: [s for s in r['logs'] if s.startswith(('Program log: ', 'Program data: '))]
paths = [('original', None)] + ([('baseline', a.baseline)] if a.baseline else []) + [('candidate', a.candidate)]
rows = []
for c in cases:
    rs = {k: run(c, b) for k, b in paths}
    for r in rs.values():
        Transaction.from_bytes(base64.b64decode(r['transaction_base64'])).verify()
        assert r['signatures_verified'] and not r['pool_authority_top_level_signer']
    fields = ['error', 'before', 'after', 'events', 'inner', 'return']
    diffs = {k: [v for v in fields if rs['original'][v] != r[v]] +
             ([] if program_messages(rs['original']) == program_messages(r) else ['ordered_program_messages'])
             for k, r in rs.items() if k != 'original'}
    expected_line = 648 if 'holder_vault' in c else (660 if 'positive-frozen-coin_creator' in c['name'] else
                                                  719 if 'positive-frozen-creator_vault' in c['name'] else None)
    if expected_line:
        assert any(f'admin_cto.rs:{expected_line}.' in s for s in rs['original']['logs']), (c, rs['original']['logs'])
    else:
        assert rs['original']['error'] is None, (c, rs['original']['error'])
    rows.append({'case': c, 'original_error_source_line': expected_line,
                 'differences': diffs, **rs})
report = {'scope': 'Twelve isolated signed captured-program comparisons. The holder-vault key is a fixture input with its matching ATA derived normally; no signer or account validation bypass. Finite behavioral evidence, not byte identity.',
          'original_sha256': sha(f.ROOT / 'evidence/original/pump/deployed.so'),
          'candidate_sha256': sha(a.candidate), 'baseline_sha256': sha(a.baseline) if a.baseline else None,
          'producer_sha256': sha(Path(__file__)), 'fixture_harness_sha256': sha(Path(f.__file__)),
          'fixture_input_adapter_source': source, 'fixture_input_adapter_sha256': hashlib.sha256(source.encode()).hexdigest(),
          'case_count': len(rows), 'signature_verifications': len(rows)*len(paths),
          'mismatches': [r['case']['name'] for r in rows if r['differences']['candidate']],
          'baseline_mismatches': [r['case']['name'] for r in rows if r['differences'].get('baseline')], 'cases': rows}
raw = (json.dumps(report, indent=2) + '\n').encode()
a.output.write_bytes(gzip.compress(raw, mtime=0) if a.output.suffix == '.gz' else raw)
print({k: report[k] for k in ['case_count', 'signature_verifications', 'mismatches', 'baseline_mismatches']})
assert not report['mismatches']
