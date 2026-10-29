"""Freeze exactly one source proposal; not a compiler-variant generator."""
from pathlib import Path
import difflib
import hashlib
import json
import re
import tarfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
sha = lambda data: hashlib.sha256(data).hexdigest()
clock = (BASE / 'perhop-clock-snapshot/multi_hop_curve_swap.rs').read_bytes()
canonical = (BASE / 'accrual-proposal/multi_hop_curve_swap.rs').read_bytes()
assert sha(clock) == '5871a2cf35ebe0db502eb242db0f1652ef93e51e4971e56483016d900349ac2b'
assert sha(canonical) == '734bdae1189dd4e4f54a27fd215624611228f36b92d3877b63f00df19ccc9e44'
with tarfile.open('/workspace/pump-current673-native-results/perhop-clock-40795474496/compiled-source.tar.gz') as archive:
    trade = archive.extractfile('programs/pump/src/trade_v3.rs').read()
assert sha(trade) == '580b1e31173ca53ccd5cb547e04efde4ae178a0626fca966ca0034e4305b2ee5'
changes = [
    ('fn div(a: u128, b: u128) -> Result<u128> {\n    a.checked_div(b).ok_or(error!(PumpError::DivisionByZero))\n}', '\n\n'),
    ('        let c = &h.bonding_curve;\n        let trade_amount = if buy {',
     '        let c = &h.bonding_curve; let cap = crate::buy_fee_market_cap(c,&h.base_mint)?;\n        let trade_amount = if buy {'),
    ('        let cap = div(h.base_mint.supply as u128 * c.virtual_quote_reserves as u128,\n            c.virtual_token_reserves as u128)?;', '\n'),
    ('            let q = sub(sub(trade_amount,pf)?,cf)?;\n            require!(q != 0,PumpError::Overflow);\n            let effective = q - 1;',
     '            let q = crate::trade::sub3(trade_amount,pf,cf)?;\n\n'),
    ('            let base = u64::try_from(div(effective as u128 * c.virtual_token_reserves as u128, c.virtual_quote_reserves as u128 + effective as u128)?).map_err(|_| error!(PumpError::Truncation))?;',
     '            let base = u64::try_from(crate::constant_product::tokens_for_quote(c,q)?).map_err(|_| error!(PumpError::Truncation))?;'),
    ('            let net = sub(sub(gross_sell,pf)?,cf)?;',
     '            let net = crate::trade::sub3(gross_sell,pf,cf)?;'),
]
s = clock.decode()
for before, after in changes:
    assert s.count(before) == 1, before
    assert before.count('\n') == after.count('\n')
    s = s.replace(before, after)
after = s.encode()
old = 'fn sub3(a:u64,b:u64,c:u64)->Result<u64>{'
assert trade.decode().count(old) == 1
newtrade = trade.decode().replace(old, 'pub(crate) ' + old).encode()
assert len(after.splitlines()) == len(clock.splitlines())
assert len(newtrade.splitlines()) == len(trade.splitlines())
oldlines, newlines = clock.decode().splitlines(), after.decode().splitlines()
changed = [i + 1 for i, (a, b) in enumerate(zip(oldlines, newlines)) if a != b]
retained_sites = []
for line, (a, b) in enumerate(zip(oldlines, newlines), 1):
    if re.search(r'\b(?:error|require(?:_gt|_gte|_eq|_neq|_keys_eq|_keys_neq)?|err|panic)!', a):
        if a == b:
            retained_sites.append(line)
        else:
            assert line in [68, 581, 589], (line, a, b)

def save(name, data):
    path = HERE / name
    if path.exists():
        assert path.read_bytes() == data, f'Frozen file differs: {path}'
    else:
        path.write_bytes(data)

for name, data in [('source-before-clock.rs', clock), ('source-before-current.rs', canonical),
                   ('trade-before.rs', trade), ('multi_hop_curve_swap.rs', after),
                   ('trade_v3.rs', newtrade)]:
    save(name, data)

def diff(before, after, path):
    return ''.join(difflib.unified_diff(before.decode().splitlines(True), after.decode().splitlines(True),
                                      fromfile='a/' + path, tofile='b/' + path))

for label, before in [('current', canonical), ('clock', clock)]:
    patch = diff(before, after, 'programs/pump/src/multi_hop_curve_swap.rs')
    patch += diff(trade, newtrade, 'programs/pump/src/trade_v3.rs')
    save(f'{label}-to-arithmetic.patch', patch.encode())

proposal = {
    'state': 'one frozen uncompiled source proposal; no native queue, byte gain or runtime claim',
    'base_main': 'f57bbf0dd856b101acd02c242cb5c4a56bf276b1',
    'base_selection': sha(canonical), 'immediate_parent': sha(clock),
    'immediate_parent_PR': 'https://github.com/lalalune/pumpfun-source/pull/731',
    'files': [
        {'source_path': 'src/multi_hop_curve_swap.rs', 'frozen_file': 'multi_hop_curve_swap.rs',
         'before_sha256': sha(canonical), 'immediate_parent_sha256': sha(clock),
         'after_sha256': sha(after), 'immediate_changed_lines': changed},
        {'source_path': 'src/trade_v3.rs', 'frozen_file': 'trade_v3.rs',
         'before_sha256': sha(trade), 'immediate_parent_sha256': sha(trade),
         'after_sha256': sha(newtrade),
         'change': 'Only private sub3 -> pub(crate) sub3; unchanged consumed helper body and source lines.'}],
    'operation': 'Use matched buy_fee_market_cap before the buy transfer-fee operation, matched sub3 on both branches, matched tokens_for_quote for buy output; preserve fee snapshot/admission, accrual, common Clock, event/payment/guard order. Remove replaced current div helper and q!=0/effective operations; blank deleted operation lines preserve unrelated Source sites. No historical source-coordinate claim.',
    'retained_macro_source_lines': retained_sites,
    'affected_error_origins': {
        'division': 'Old multi_hop_curve_swap.rs:68 -> original-backed lib.rs:2481 cap or util/constant_product.rs:13/17/19 output.',
        'subtractions': 'Old multi_hop_curve_swap.rs:65 -> original-backed trade_v3.rs:294 for only these two compound subtractions; post-event standalone subtraction remains unchanged.',
        'zero_quote': 'Old explicit require multi_hop_curve_swap.rs:581 -> exact tokens_for_quote checked_sub(1), From<PumpError::Overflow> with no Source.',
        'truncation': 'Existing map_err at line589 retained as a macro at the same line; only its producing expression changes.'},
    'proof_files': {name: sha((HERE / name).read_bytes()) for name in [
        'CALL-BOUNDARIES.json', 'HELPER-CLOSURE.json', 'prove_call_boundaries.py']},
    'policy': 'No build until source/argument/failure/pointee proof accepted; exactly one subsequent fixed native recipe measurement, no variants; do not alter the locked CTO+Sweep+Clock composition.'}
save('proposal.json', (json.dumps(proposal, indent=2) + '\n').encode())
print(json.dumps({'files': proposal['files'], 'retained_macro_sites': len(retained_sites),
                  'changed_lines': changed, 'output': str(HERE)}, indent=2))
