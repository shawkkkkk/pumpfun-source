# AMM union4 + recovered mint scanner (769 → 770 / 785)

Composes the already-recovered [`supported_mint_data`](../amm-mint-scanner-raw-20261028/README.md) body into the [union4](../claude-amm-union4-20261028/README.md) program and measures the linked ELF. That packet had the exact 1,192-byte function and said it was not yet composed. This build does that composition.

| Linux v1.44 `sbpf-solana-solana` | normalized | raw |
| --- | ---: | ---: |
| union4 symbols `576eb629…` | 769 / 785 | 160 |
| **this candidate** (`562bfa9e…`) | **770 / 785** | **163** |

- Normalized gain: `0xf28b8` (1,192 bytes). It is raw-equal as well. Normalized losses: none.
- Raw gains, no raw losses: `0xf28b8`, plus `0xf28a8` (16 bytes) and `0x111360` (32 bytes), which were already normalized matches.
- Unmatched AMM windows: 16 → 15.
- Five-program total against current `main`: **3,278 / 3,338 (98.20%)**. Pump stays at the published L32 count of 990 / 1,035.

## Source

`crates/native-transfer-fee/src/lib.rs` is byte-identical to [`sources/recovered.rs`](../amm-mint-scanner-raw-20261028/sources/recovered.rs). Every other file is the union4 archive `sources/candidate.tar.gz`. A Linux v1.44 compile of that crate alone reproduces all 1,192 original bytes (`cd1639db…`) before linking; the linked program keeps that body.

The maintained `programs/` tree is not changed. Whole-ELF identity is still false. The union4 incentive stack-frame diagnostic is still present and does not fail the build.

## Build

Official Linux platform-tools v1.44, target `sbpf-solana-solana`, union4 release profile (`panic = abort`, `overflow-checks = true`, `lto = false`, `codegen-units = 1`), `CARGO_TARGET_SBPF_SOLANA_SOLANA_RUSTFLAGS=-Zremap-cwd-prefix=`, `--locked --offline`. `builds/unstripped.so.gz` is the linked artifact (1,802,960 bytes, SHA-256 `562bfa9e87b47713b0fa60d061c17e4612eea621aca930023914d3c3d84a79e4`).

```sh
python3 research/amm-mint-scanner-union4-20261028/verify.py
```
