# Pump curve unchecked deserializer plus line-997 closure (990 → 992 / 1035)

Measured against published [L32](../claude-pump-integration-20261027/r37-layout-32/README.md). Upstream L32 is 990 / 1,035. This ELF is 992 / 1,035.

| Linux v1.44 `sbpf-solana-solana` | normalized | raw |
| --- | ---: | ---: |
| L32 | 990 / 1,035 | 166 |
| **this candidate** (`de4e5dfc…`) | **992 / 1,035** | **164** |

Normalized gains, no losses:

- `0x9b430` (624 bytes), `BondingCurve::try_deserialize_unchecked`. Call-normalized Hamming distance 0.
- `0x857a8` (520 bytes), the `trade_v3.rs:997` `Truncation` closure from the third `tokens_for_quote` narrowing.

`0x9b148`, the checked entry, is still unmatched on this branch. It is 736 bytes here and 744 in the original. The unchecked body matches; the checked prologue does not.

Raw stays 164 versus L32's 166. Gains `0x199af0` and `0x199b18`. Losses `0x1891d8`, `0x189340`, `0x18de90`, `0x18e568`, which remain normalized matches.

## What the search tried

A standalone `anchor-lang` crate compiled each dispatcher shape in about 0.2s and scored it against the original windows. Seventeen shapes: separate `if` returns, `else if`, nested pairs, `>=` chains, `core::intrinsics::likely`, a `#[cold]` error helper, `match` guards, range `match`, shared `Ok`, split helpers, block separators, inverted fused arms, and named `const` thresholds.

`likely` and the named constants both reproduced all 624 unchecked bytes in the standalone crate (call immediates masked). Only the named-constant chain, duplicated inside both `AccountDeserialize` entries instead of a shared helper, reproduced `0x9b430` in the full Pump program. The checked entry reached 736 bytes and did not match.

## Patches

- `trade_types.patch` duplicates the length chain in `try_deserialize` and `try_deserialize_unchecked`.
- `trade_v3.patch` is the line-997 closure. Both are in this ELF; dropping either one was not remeasured.

`builds/unstripped.so.gz` is 2,764,360 bytes, SHA-256 `de4e5dfce4e136708b1451e2e19bc3ea2f4fe455de7a6d3c6bbc224b407e2019`.

```sh
python3 research/pump-curve-unchecked-20261028/verify.py
```
