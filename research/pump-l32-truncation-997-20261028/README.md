# Pump L32 + trade_v3 line 997 Truncation closure (990 → 991 / 1035)

Same closure recovery as the L31 packet, rebuilt on the published [L32](../claude-pump-integration-20261027/r37-layout-32/README.md) source. L32 did not move this site: `trade_v3.rs:997` is still the `transfer_from_user` closer, and `0x857a8` is still unmatched.

| Linux v1.44 `sbpf-solana-solana` | normalized | raw |
| --- | ---: | ---: |
| L32 `unstripped.so` | 990 / 1,035 | 166 |
| **this candidate** (`cd4d26c0…`) | **991 / 1,035** | **164** |

- Normalized gain: `0x857a8` (520 bytes), `error!(PumpError::Truncation)` at `programs/pump/src/trade_v3.rs:997`. Normalized losses: none.
- Raw 166 → 164. Gains `0x199af0` and `0x199b18`; losses `0x1891d8`, `0x189340`, `0x18de90`, `0x18e568`. Those four stay normalized matches; the new closure shifts later call displacements.
- Pump unmatched windows: 45 → 44.
- With the separate AMM mint-scanner composition (770 / 785), the five-program total is **3,279 / 3,338 (98.23%)**. This packet by itself, on current main's other rows, is **3,278 / 3,338 (98.20%)**.

`source.patch` closes `transfer_from_user` on the previous line and puts the third `tokens_for_quote` narrowing on line 997. The narrowed value is not consumed. A failure returns `Truncation`; the success path only adds the call. No other recorded `error!` / `require!` line moves.

`builds/unstripped.so.gz` is 2,763,056 bytes, SHA-256 `cd4d26c0baf6b7d0162c5c845e009dc68e91db15bbbf1c298d952d10360ab5ec`.

```sh
python3 research/pump-l32-truncation-997-20261028/verify.py
```
