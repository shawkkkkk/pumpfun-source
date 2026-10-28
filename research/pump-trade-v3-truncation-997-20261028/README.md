# Pump trade_v3 line 997 Truncation closure (990 → 991 / 1035)

One normalized window over the published [L31](../claude-pump-integration-20261027/r37-layout-31/README.md) source-only build. Whole-ELF identity is still false.

| Linux v1.44 `sbpf-solana-solana` build | normalized | raw |
| --- | ---: | ---: |
| L31 `unstripped.so` (`ccb52f1f…`) | 990 / 1,035 | 166 |
| **this candidate** (`1e8660b5…`) | **991 / 1,035** | **164** |

- Gained normalized window: `0x857a8` (520 bytes), the `error!(PumpError::Truncation)` closure recorded at `programs/pump/src/trade_v3.rs:997`.
- Normalized losses: none.
- Raw: 166 → 164. Two raw windows appear (`0x199af0`, `0x199b18`) and four disappear (`0x1891d8`, `0x189340`, `0x18de90`, `0x18e568`). Those bodies stay normalized matches; the new 520-byte closure moves later call displacements.
- Unmatched Pump windows: 45 → 44. Across the five programs this is 3,272 / 3,338 (98.02%).

`0x857a8` is the same closure shape as the already-matched trade_v3 Truncation sites at lines 811, 904, 911 and 930 (error 6025, file `programs/pump/src/trade_v3.rs`). It differed by the line immediate only. L31 named this site as the missing third `tokens_for_quote` in `buy_exact_quote` and did not emit it.

## Source

`source.patch` is against L31 `source/programs/pump/src/trade_v3.rs`. The `transfer_from_user` call now closes on the previous line, and line 997 is:

```rust
let _ = u64::try_from(crate::constant_product::tokens_for_quote(curve, quote)?)
    .map_err(|_| error!(PumpError::Truncation))?;
```

The narrowed value is not yet fed into the handler. On the success path the call only adds work; a `tokens_for_quote` or `u64` narrowing failure now returns `Truncation` from `buy_exact_quote`. No other recorded `error!` / `require!` line moved. The 21,608-byte `buy_exact_quote` body was already unmatched and stays unmatched.

## Build

Official Linux platform-tools v1.44 (`6719b889…`), target `sbpf-solana-solana`, release profile from the L31 manifest (`panic = abort`, `overflow-checks = true`, `lto = false`, `codegen-units = 1`), `CARGO_TARGET_SBPF_SOLANA_SOLANA_RUSTFLAGS=-Zremap-cwd-prefix=`, `--locked --offline`. `builds/unstripped.so.gz` is that artifact (2,762,272 bytes, SHA-256 `1e8660b5bb24f549232c47476856d8db11ad79979d7c9b04bded654d2618395f`).

```sh
python3 research/pump-trade-v3-truncation-997-20261028/verify.py
```

`verify.py` rescores both ELFs against the L31 inventory and the captured `evidence/original/pump/deployed.so`.
