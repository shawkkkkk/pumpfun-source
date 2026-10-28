# Pump `v3_buy_costs` narrowed toward `0x80df8`

Research note on L33 (`research/claude-pump-integration-20261027/r37-layout-33`). The maintained `programs/` tree is unchanged. `0x80df8` is still unmatched.

`0x80df8` (2,120 bytes) is `trade::v3_buy_costs`. Its two Anchor error sites are `PumpError::Overflow` (code 6024) at `trade_v3.rs` lines **371** and **375**. The stored `29` next to each line is the length of `programs/pump/src/trade_v3.rs`, not a column. The original calls `trade::add` twice, then `pre_fee_amount`, and builds those two errors in the function. It does not call `add3` or `sub`.

`trade_v3.patch` moves `v3_buy_costs` so those two `error!(PumpError::Overflow)` expressions sit on lines 371 and 375. `is_mayhem` is a `u8` compared with `!= 0` (`and r3, 255`). The post-complete leg is one outlined `add(quote_in, protocol_fee)`. The quote-fee sum and the later add-then-subtract are `match`/`return Err` on those two lines.

Workspace-layout rebuild, v1.44 SBPF SDK, `-Zremap-cwd-prefix=`:

| | L33 | this patch |
| --- | ---: | ---: |
| normalized windows | 1,010 / 1,035 | 1,010 / 1,035, no losses |
| `v3_buy_costs` | 1,160 bytes, opcode ratio 0.488 | **2,056 bytes, opcode ratio 0.722** |
| distance to 2,120 | 960 bytes short | **64 bytes short** |

The body contains line immediates 371 and 375 and two `6024` stores. Eager `ok_or(error!(...))` and inlining the remaining `add(first, second)` both grew past 2,120 and lowered the ratio, so they are not in the patch.
