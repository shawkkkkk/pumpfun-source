# Pump `v3_buy_costs` narrowed toward `0x80df8`

Research note on L33 (`research/claude-pump-integration-20261027/r37-layout-33`). The maintained `programs/` tree is unchanged. `0x80df8` is still unmatched.

`0x80df8` (2,120 bytes, 249 instructions) is `trade::v3_buy_costs`, not `constant_product::output`. Both bodies call `__multi3`, `__udivti3`, `trade::add` twice, `pre_fee_amount`, and the `gross_up_quote` error closure, and both contain `buyback fee is at most protocol_fee`. L33's `v3_buy_costs` is 1,160 bytes because `add3` and `sub` are separate calls. The original inlines those checked adds and the following subtract, and it masks the mayhem flag with `and r3, 255`.

`trade_v3.patch` is the line-count-preserving edit against the L33 `trade_v3.rs`:

- `is_mayhem` is a `u8`, compared with `!= 0`, so the prologue emits `and r3, 255`.
- `quote + protocol_fee + creator_fee`, the post-complete sum, and the final subtract are written inline. The two `add(buyback, post_buyback)` and `add(first, second)` calls stay outlined, matching the original's two `trade::add` calls.

Workspace-layout rebuild with the v1.44 SBPF SDK (`-Zremap-cwd-prefix=`, release profile from L33):

| | L33 | this patch |
| --- | ---: | ---: |
| normalized windows | 1,010 / 1,035 | 1,010 / 1,035 |
| losses against L33 | | none |
| `v3_buy_costs` size | 1,160 | 1,816 |
| opcode ratio vs `0x80df8` | 0.488 | 0.711 |

The window is still 304 bytes short of 2,120. Replacing `try_from(...).expect` with `assert!(product >> 64 <= 9999)` grew the body to 1,904 and dropped the ratio to 0.668, so that form is not in the patch.
