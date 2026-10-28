# AMM `0x19138`: copy the first reserved pubkey as `u16`/`u8`/`u32`/`u64`s

Partial on top of [`research/claude-amm-union7-20261028`](../claude-amm-union7-20261028/README.md) (780/785). `programs/` is unchanged. `handler.patch` applies to that packet's `set_reserved_fee_recipients.rs`. `require_gte!` stays on line 40, `require_keys_neq!` on line 60, and the executable / rent-exempt sites stay on lines 66 and 70.

The original copies that first pubkey with a halfword at `+0`, a byte at `+2`, a word at `+3`, three doublewords at `+7`/`+15`/`+23`, and a byte at `+31`. A `#[repr(C, packed)]` aggregate `read_unaligned` of those fields is widened back to four `ldxdw`s by this LLVM. Separate `read_unaligned`/`write_unaligned` calls of `u16`, `u8`, `u32`, three `u64`s, and `u8` keep those widths. The copy reads `recipients[0]` in place. The other seven keys stay a `try_into` of the tail. `global_config` is borrowed before the `Vec` allocation.

Linux platform-tools v1.44, `sbpf-solana-solana`, union7 release profile.

| | normalized | raw | `0x19138` size | opcode alignment |
|---|---:|---:|---:|---:|
| union7 | 780/785 | 220 | 9,136 (original 9,176) | 0.982 |
| this edit | 780/785 | 220 | 9,184 | 0.989 |

No other window was lost. Word loads and stores now match the original (`ldxw` 1, `stxw` 1). Halfword loads and stores are 1 and 1; the original has 2 and 2. The window is still open.

Copying the event field the same way as well grew the handler to 9,216 bytes and dropped the alignment to 0.980.
