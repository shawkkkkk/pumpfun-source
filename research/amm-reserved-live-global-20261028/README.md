# AMM `0x19138`: bind `global_config` before the key allocation

Partial follow-up to [`research/claude-amm-union7-20261028`](../claude-amm-union7-20261028/README.md) (780/785). The maintained `programs/` tree is unchanged. Apply `handler.patch` to that packet's `programs/pump-amm/src/instructions/admin/set_reserved_fee_recipients.rs` (the patched file is also saved here). `require_gte!` stays on line 40, `require_keys_neq!` on line 60, and the executable / rent-exempt `Error::from` sites stay on lines 66 and 70.

Pump `set_reserved_fee_recipients` (`0x6fef8`) improved when the global account was borrowed before the recipient-key `Vec` allocation, so the accounts pointer stayed live across the allocator. Union7 already collects the eight keys before the checks and already hoists `Rent::get`. This edit only moves

```rust
let global_config = &mut ctx.accounts.global_config;
```

to that same point, before `collect::<Vec<_>>()`. Taking the first key with `recipients[0]` and the other seven with `recipients[1..].try_into()` compiled to the same body, so the slice pattern is unchanged.

Linux platform-tools v1.44, target `sbpf-solana-solana`, same release profile and `-Zremap-cwd-prefix=` as union7. One root-crate rebuild.

| | normalized | raw | `0x19138` size | opcode alignment | hunks |
|---|---:|---:|---:|---:|---:|
| union7 | 780/785 | 220 | 9,136 (orig 9,176) | 0.982 | 22 |
| this edit | 780/785 | 220 | 9,128 | 0.987 | 12 |

No normalized or raw losses. The window is still unmatched. The halfword+byte versus word copy of the first pubkey is still there (`ldxh`/`ldxb` in the original, `ldxw` in the candidate). The size moved 8 bytes further from 9,176. The spill alignment is what improved.

## `jeq`+`ja` is not a global build lever

The original program and the union7 candidate both contain this unfused pattern (conditional branch with offset `+1` whose next instruction is `ja`): **1,619 sites** in `evidence/original/pump_amm/deployed.so`, **1,617** in the union7 image. `0x4c750` (`sell::cashback`) is the near miss: same 9,024 bytes, same 80 calls in the same order, **14** unfused sites versus **13**. The missing one is a `jeqx` at offset `0xd00` (the `try_borrow_data()?` check), which this compiler folds to `jne`.

The original text embeds the platform-tools standard-library path `/home/runner/work/platform-tools/platform-tools/out/rust/library/alloc/...`. That is the official v1.44 archive (`platform-tools-linux-x86_64.tar.bz2`, sha256 `6719b889…`), not a second LLVM.

Flags passed only to the `pump-amm-recovered` crate with `cargo rustc -- -C llvm-args=…`:

| lever | normalized | `0x4c750` |
|---|---:|---|
| `--disable-branch-fold` | 427/785 | still open |
| `--simplifycfg-branch-fold-threshold=0` | 762/785 | still open |

Folding is required for the windows that already match. The one extra fused `jne` in `0x4c750` is local to that check. Reordering `AppliedFees` (the union7 store-order lever) lost 13 windows and gained none.
