One frozen arithmetic-boundary reconstruction is prepared here, not a family
of compiler probes. The canonical current711 source is 734bdae1; its qualified
Clock successor is 5871a2cf. The proposed per-hop source is d21edc80. The only
second-file change is `sub3` visibility in trade_v3.rs, 580b1e31→27ec6da2.
The helper body and its line294 Source remain unchanged. Trading owns no
overlapping shared edit and agreed to this actual used visibility change.

The complete original 0x5b3b0 caller, 18,584 bytes, contains these actual calls:

| Offset | Existing current helper | Used arguments and result |
| --- | --- | --- |
| +0x17b0 | buy_fee_market_cap | The same live curve and base Mint; Result<u128> cap feeds both fee-selection branches. |
| +0x1c08 | trade::sub3 | Admitted sell_quote low u64, flag-selected protocol fee, flag-selected creator fee; successful net feeds the sell zero check and output. |
| +0x1d68 | trade::sub3 | Successful post_fee_amount trade budget and the actual returned net_quote_for_budget fee fields; successful quote feeds tokens_for_quote. |
| +0x1db0 | constant_product::tokens_for_quote | The same curve and successful buy sub3 quote; Result<u128> feeds the existing u64 conversion, zero check and real-token cap. |

`prove_call_boundaries.py` validates those call targets, exact argument
instructions, result branches and unchanged Error forwarding against the
actual captured ELF. Its conservative whole-function CFG retains both edges
of every conditional: 2,287 instructions, three reaching-definition passes.
Both reaching r9 definitions for the market-cap Mint load the same base Mint
slot, whose defining h[0] store dominates the cap. The cap dominates the sell
quote and buy transfer-fee producers, so the proposed common cap binding is
before `trade_amount`. It is not placed merely at the old manual expression.

`HELPER-CLOSURE.json` identifies five complete normalized helper bodies:
marketcap760, sub3576, tokens_for_quote192, constant_product::output2136 and
From<PumpError>504. `verify_pointees.py` recomputes all 33 narrowly masked data
operands, all 30 direct-call identities, bounded filenames/ordinals/panic
Location, and the used String/fmt vtable methods. This does not claim blanket
transitive stdlib pointer closure or unique historical source.

The proposal restores actual helper error origins: cap DivisionByZero at
lib.rs2481, compound subtraction Overflow at trade_v3.rs294, and output
overflow/division at util/constant_product.rs13/17/19. A zero buy quote follows
the original tokens_for_quote checked_sub(1) conversion with no Source; the
current explicit q!=0 require is replaced together with effective=q−1.
The existing truncation, zero-output, completion, whitelist, admission,
payment, accrual and event operations remain. Deleted operation lines are
blank to preserve unrelated reconstructed Source lines; no historical source
coordinate is claimed and no new layout annotation is introduced.

`current-to-arithmetic.patch` is canonical734→proposed plus the minimal
visibility change. `clock-to-arithmetic.patch` is immediate587→proposed.
`freeze_source.py` refuses to overwrite any frozen file with different bytes.
`proposal.json` binds the exact two source files and original proof hashes.
Supplemental independent pointer verification is in POINTEES-VERIFIED.json.

Root released exactly one fixed current711 native measurement after the
separate composition20 run completed. The locked CTO+Sweep+Clock composition
is unchanged. No compiled caller identity, inventory gain or runtime claim is
made for this source until the actual new artifacts are qualified. No inline,
type, layout, flag or spelling alternatives are authorized. The rejected
Mayhem witness and closed constructor/CTA probes remain separate.
