"""Read-only original per-hop call/argument/return attribution; no bundle execution."""
from pathlib import Path
import collections
import hashlib
import json
import struct
import sys
import tarfile

ROOT = Path('/workspace/pumpfun-source-latest')
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
from pump_compare_function_bytes import body, normalize
from pump_quote_control_function_match import sections

ORIGINAL = ROOT / 'evidence/original/pump/deployed.so'
CURRENT = Path('/workspace/pump-current673-native-results/perhop-clock-40795474496/unstripped.so')
ARCHIVE = CURRENT.parent / 'compiled-source.tar.gz'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def cfg(raw):
    nodes, at = {}, 0
    while at < len(raw):
        op, regs, off, imm = struct.unpack_from('<BBhi', raw, at)
        width = 16 if op == 0x18 else 8
        nodes[at] = (op, regs & 15, regs >> 4, off, imm, width)
        at += width
    succ, pred = {}, collections.defaultdict(set)
    for at, (op, dst, src, off, imm, width) in nodes.items():
        edges = [] if op == 0x95 else [at + 8 + off * 8] if op == 0x05 else (
            [at + 8, at + 8 + off * 8]
            if op & 7 in [5, 6] and op not in [0x85, 0x8d] else [at + width])
        for edge in edges:
            assert edge in nodes
            pred[edge].add(at)
        succ[at] = edges
    return nodes, succ, pred


def reachable(succ, removed=None):
    seen, pending = set(), [0]
    while pending:
        at = pending.pop()
        if at == removed or at in seen:
            continue
        seen.add(at)
        pending.extend(succ[at])
    return seen


def reaching(nodes, succ, pred, writes):
    used = reachable(succ)
    incoming = {at: set() for at in used}
    outgoing = {at: set() for at in used}
    for iteration in range(100):
        changed = False
        for at in sorted(used):
            before = {-1} if at == 0 else set().union(
                *(outgoing[p] for p in pred[at] if p in used))
            after = {at} if writes(nodes[at]) else before
            if before != incoming[at] or after != outgoing[at]:
                incoming[at], outgoing[at], changed = before, after, True
        if not changed:
            return incoming, iteration
    raise ValueError('reaching definitions did not converge')


def main():
    original, current = ORIGINAL.read_bytes(), CURRENT.read_bytes()
    assert sha(original) == '7a19affaa2c6187e04a5fe0ea298cee81fa5eb8c24cfcc30d85f615e89f7b02d'
    assert sha(current) == '4f8f22984af1a35d9c6b0978e4d33b9e9bfe13a80188c6aabc41eb85fe3a0b14'
    raw = body(original, sections(original), 0x5b3b0, 18584)
    nodes, succ, pred = cfg(raw)

    def ins(at, expected):
        assert nodes[at][:5] == expected, (hex(at), nodes[at], expected)

    def call(at, target):
        op, dst, src, off, imm, width = nodes[at]
        assert (op, src, 0x5b3b0 + at + 8 + imm * 8) == (0x85, 1, target)

    def branch(at, target):
        assert target in succ[at], (hex(at), hex(target))

    call(0x17b0, 0xa08f8)
    call(0x1c08, 0x80488)
    call(0x1d68, 0x80488)
    call(0x1db0, 0xa0838)
    call(0x1838, 0xa0538)  # The unchanged actual sell_quote producer.
    ins(0x18, (0x7b, 10, 4, -0xa40, 0))  # Incoming CurveHop pointer.
    ins(0x20, (0x79, 9, 4, 0x10, 0))  # Incoming curve Account box.
    ins(0x6b0, (0x79, 6, 10, -0xa40, 0))
    ins(0x6d0, (0x79, 1, 6, 0, 0))
    ins(0x6d8, (0x7b, 10, 1, -0xaa8, 0))
    ins(0x12a0, (0x79, 9, 10, -0xaa8, 0))
    ins(0x1358, (0x79, 9, 10, -0xaa8, 0))
    ins(0x1748, (0x79, 6, 10, -0xab0, 0))
    ins(0x1750, (0x07, 6, 0, 0, 8))
    ins(0x17a0, (0xbf, 2, 6, 0, 0))
    ins(0x17a8, (0xbf, 3, 9, 0, 0))
    r9, iterations = reaching(nodes, succ, pred, lambda v:
        v[1] == 9 and (v[0] & 7 in [1, 4, 7] or v[0] == 0x18))
    assert r9[0x17a8] == {0x12a0, 0x1358}
    assert r9[0x1d50] == {0x19d0}
    stack_defs = {}
    for slot, use, expected in [(-0xaa8, 0x12a0, {0x6d8}),
                                (-0xaa8, 0x1358, {0x6d8}),
                                (-0xab0, 0x1748, {0x678, 0x688}),
                                (-0xa40, 0x6b0, {0x18}),
                                (-0xaf0, 0x1bf0, {0x1af0}),
                                (-0xab8, 0x1da0, {0x17d8})]:
        defs, count = reaching(nodes, succ, pred, lambda v:
            v[1] == 10 and v[3] == slot and v[0] & 7 in [2, 3])
        assert defs[use] == expected, (hex(slot), hex(use), defs[use])
        stack_defs[f'{slot:+#x}@{use:#x}'] = [hex(x) for x in sorted(expected)]
    assert r9[0x678] == r9[0x688] == {0x20}
    for at in [0x678, 0x688]:
        ins(at, (0x7b, 10, 9, -0xab0, 0))
    assert 0x17b0 not in reachable(succ, 0x6d8)
    assert 0x18e8 not in reachable(succ, 0x17b0)
    assert 0x1838 not in reachable(succ, 0x17b0)

    # Cap returns Result<u128>. Success is zero tag; both cap words are saved.
    ins(0x17b8, (0x79, 3, 10, -0x6c8, 0))
    ins(0x17c0, (0x79, 1, 10, -0x6d0, 0))
    ins(0x17c8, (0x55, 1, 0, 0x11, 0))
    branch(0x17c8, 0x1858)
    ins(0x17d0, (0x7b, 10, 3, -0xac8, 0))
    ins(0x17f0, (0x79, 6, 10, -0x6c0, 0))
    # Cap failure shares the actual unwrapped two-word Error forwarding block.
    for at, expected in [(0x1858, (0x79, 1, 10, -0x6c0, 0)),
                         (0x1860, (0x79, 2, 10, -0xa60, 0)),
                         (0x1868, (0x7b, 2, 1, 8, 0)),
                         (0x1870, (0x7b, 2, 3, 0, 0))]:
        ins(at, expected)

    # Sell gross is the low result of sell_quote after its zero-high-word check.
    ins(0x1830, (0x79, 3, 10, -0xa78, 0))
    ins(0x1840, (0x79, 3, 10, -0x6c8, 0))
    ins(0x1950, (0x79, 1, 10, -0x6c0, 0))
    branch(0x1958, 0x1ac8)
    ins(0x1af0, (0x7b, 10, 3, -0xaf0, 0))
    for at, expected in [(0x1bf0, (0x79, 2, 10, -0xaf0, 0)),
                         (0x1bf8, (0x79, 3, 10, -0xaf8, 0)),
                         (0x1c00, (0x79, 4, 10, -0xb00, 0))]:
        ins(at, expected)
    # Buy sub3 consumes the successful post_fee_amount value, not returned q.
    ins(0x1908, (0x79, 3, 10, -0x6c8, 0))
    ins(0x19d0, (0xbf, 9, 3, 0, 0))
    ins(0x1d50, (0xbf, 2, 9, 0, 0))
    ins(0x1d30, (0x79, 4, 10, -0x6b8, 0))
    ins(0x1d38, (0x79, 3, 10, -0x6c0, 0))
    # Both sub3 returns keep Error without remapping and use success tag 2.
    branch(0x1c50, 0x1c60)
    branch(0x1c58, 0x2710)
    branch(0x1d78, 0x1d88)
    branch(0x1d80, 0x2710)
    for at, expected in [(0x2710, (0x79, 2, 10, -0x6c8, 0)),
                         (0x2718, (0x79, 3, 10, -0xa60, 0)),
                         (0x2720, (0x7b, 3, 2, 8, 0)),
                         (0x2728, (0x7b, 3, 1, 0, 0))]:
        ins(at, expected)
    # The buy success is exactly the quote passed to tokens_for_quote.
    ins(0x1d88, (0x79, 3, 10, -0x6c8, 0))
    ins(0x1da0, (0x79, 2, 10, -0xab8, 0))
    ins(0x1da8, (0x7b, 10, 3, -0xaf0, 0))
    ins(0x1db8, (0x79, 1, 10, -0x6c8, 0))
    ins(0x1dc0, (0x7b, 10, 1, -0xb28, 0))
    branch(0x1dd0, 0x2190)  # Result<u128> zero-tag success.
    for at, expected in [(0x1dd8, (0x79, 1, 10, -0x6c0, 0)),
                         (0x1de0, (0x79, 2, 10, -0xa60, 0)),
                         (0x1de8, (0x7b, 2, 1, 8, 0)),
                         (0x1df0, (0x79, 1, 10, -0xb28, 0)),
                         (0x1df8, (0x7b, 2, 1, 0, 0))]:
        ins(at, expected)
    branch(0x2198, 0x2288)  # The unchanged u128->u64 high-word admission.
    branch(0x2290, 0x2748)  # The unchanged BuyZeroAmount cold block.

    # Exact helper/source identities are separately recorded, not inferred
    # from a callee address or just a same-length body.
    closure = json.loads((HERE / 'HELPER-CLOSURE.json').read_text())
    for helper in closure['helpers']:
        left = body(original, sections(original), int(helper['original'], 16), helper['bytes'])
        right = body(current, sections(current), int(helper['current'], 16), helper['bytes'])
        ln, _ = normalize(left, int(helper['original'], 16), sections(original))
        rn, _ = normalize(right, int(helper['current'], 16), sections(current))
        assert ln == rn and sha(ln) == helper['normalized_sha256']
    with tarfile.open(ARCHIVE) as archive:
        source = {p: archive.extractfile(p).read() for p in [
            'programs/pump/src/lib.rs', 'programs/pump/src/trade_v3.rs',
            'programs/pump/src/util/constant_product.rs',
            'programs/pump/src/multi_hop_curve_swap.rs']}
    assert sha(source['programs/pump/src/multi_hop_curve_swap.rs']) == closure['current_source_sha256']
    report = {
        'scope': 'One used arithmetic call-boundary proposal. Static original/current ELF and actual compiled source only; no build, VM, identity gain, or unique historical source claim.',
        'original': {'sha256': sha(original), 'start': '0x5b3b0', 'bytes': len(raw)},
        'current_symbols_sha256': sha(current),
        'archive_sha256': sha(ARCHIVE.read_bytes()),
        'actual_compiled_sources': {p: sha(b) for p, b in source.items()},
        'CFG': {'instructions': len(nodes), 'reachable': len(reachable(succ)),
                'r9_fixed_point_iterations': iterations,
                'conditional_edges': 'Both retained; no infeasible-path pruning.',
                'stack_reaching_definitions': stack_defs,
                'memory_scope': 'Explicit stores to these frame slots; all listed slots are scalar or immutable account pointers, outside the callee result buffers. This is not a general alias-analysis proof.'},
        'market_cap': {
            'call': '+0x17b0 -> 0xa08f8 (760B)',
            'r2_curve': 'Incoming h[0x10] box saved by +0x678/+0x688, reloaded +0x1748 and adjusted +8 at +0x1750; exact helper reads virtual tokens +0x40, virtual quote +0x48, Mayhem bit +0x9a, token_total_supply +0x60.',
            'r3_mint': 'Incoming h[0] box saved +0x6d8; either +0x12a0 or +0x1358 reload is the only reaching r9 definition. Exact helper reads Mint.supply at +0x28 on ordinary admitted hops.',
            'ordering': 'Call dominates both sell_quote +0x1838 and buy post_fee_amount +0x18e8. The proposed common cap binding belongs before trade_amount, not after it.',
            'success': 'Zero Result<u128> tag; low cap saved -0xac8 and high cap retained r6, then both passed to unchanged get_fees on either branch.',
            'failure': 'Nonzero tag -> +0x1858..+0x1870 copies both Error words unchanged to outer output; no caller source replacement.'},
        'sell_sub3': {
            'call': '+0x1c08 -> 0x80488 (576B)',
            'arguments': 'r2 gross_sell from successful sell_quote +0x1838: low word +0x1840 after high-word zero check +0x1958, stored -0xaf0 by +0x1af0. r3 protocol and r4 creator fees are selected/zeroed by the existing flag branches.',
            'success': 'Tag2 -> +0x1c60 reads net; original SellZeroAmount and outgoing quote transfer-fee operation remain after this boundary.',
            'failure': 'Other tag -> +0x2710..+0x2728 copies Error discriminant and pointer unchanged to outer output.'},
        'buy_sub3': {
            'call': '+0x1d68 -> 0x80488 (576B)',
            'arguments': 'r2 trade_amount has sole reaching r9 definition +0x19d0 from post_fee_amount successful low value; r3/r4 read actual net_quote_for_budget returned protocol/creator fee fields -0x6c0/-0x6b8. The returned net quote is deliberately recomputed, not substituted.',
            'success': 'Tag2 -> +0x1d88 supplies exactly its returned quote to tokens_for_quote and saves the same quote as -0xaf0.',
            'failure': 'Same unchanged Error forwarding at +0x2710..+0x2728 as sell.'},
        'tokens_for_quote': {
            'call': '+0x1db0 -> 0xa0838 (192B)',
            'arguments': 'r2 same cap curve pointer saved -0xab8; r3 successful buy sub3 quote.',
            'success': 'Zero Result<u128> tag -> +0x2190; high word admission +0x2198 precedes original u64 truncation and BuyZeroAmount +0x2290, then cap against real_token_reserves.',
            'failure': '+0x1dd8..+0x1df8 copies its two Error words unchanged to outer output.',
            'zero_quote': 'The actual helper performs checked_sub(1); zero converts PumpError::Overflow through the full matched From<PumpError> body, with no caller Source. It replaces the current explicit q!=0 require and effective=q-1 together.'},
        'helper_closure_sha256': sha((HERE / 'HELPER-CLOSURE.json').read_bytes()),
        'source_failures': closure['source_failures'],
        'limitations': 'Static attribution is not compiled caller identity or runtime qualification. Existing rejected Mayhem witness and closed constructor/CTA probes remain separate. Native compilation and replay may only follow one frozen proposal; no variants.'}
    (HERE / 'CALL-BOUNDARIES.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'passed': True, 'instructions': len(nodes), 'helper_bodies': len(closure['helpers']),
                      'market_cap_dominates_both_quote_producers': True,
                      'output': str(HERE / 'CALL-BOUNDARIES.json')}))


if __name__ == '__main__':
    main()
