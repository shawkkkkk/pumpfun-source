# Multi-hop dispatcher: `require_gt!` on the amount check

Stacked on `cursor/pump-c-big-windows-567e`, which split `multi_hop_curve::execute` into a dispatcher plus `#[inline(never)] run_curve`.

`0x567d8` (5,216 bytes) calls `CurveHop::try_accounts` and then `0x5b3b0`, and its prologue is the hop-argument check (`amount`, `remaining_accounts.len() >= 5 && len % 5 == 0`, scan until a fee byte is `>= 4`). That is the dispatcher, not `run_curve`. The C agent's dispatcher was 4,024 bytes, opcode ratio 0.477 against `0x567d8`.

The original calls `Error::with_values` for that amount check. `require!(amount_in > 0, ...)` does not. `require_gt!(amount_in, 0, PumpError::BuyZeroAmount)` does, and the check stays on line 248, inside 208–262.

Workspace-layout rebuild, v1.44 SBPF SDK:

| dispatcher | size | opcode ratio vs `0x567d8` | normalized vs L33 |
| --- | ---: | ---: | --- |
| C agent split | 4,024 | 0.477 | 1,010, no losses |
| `require_gt!` | **4,080** | **0.590** | 1,010, no losses |

Still 1,136 bytes short of 5,216. Splitting the length check into `require_gte!(len, 5)` plus a separate modulo `require!` grew the body to 4,624 and dropped the ratio to 0.481, so that split is not included. `run_curve` in this build is 25,424 bytes and does not match `0x5b3b0` (18,584).

## Call and line order

Opcode-sequence LCS (immediates ignored) is 402/631 = 0.637 for both the `require_gt!` body and the line move below. Immediate-aware LCS, with call and `lddw` operands masked, is 357/631 = 0.566 before the line move and 360/631 = 0.571 after it. The earlier 0.590 figure was a different cut of the same `require_gt!` body.

Original `0x567d8`, in order:

| offset | what |
| ---: | --- |
| 208–840 | `PumpError::name`, `Display::fmt`, repeated three times, then `unwrap_failed` |
| 968 | `6020` BuyZeroAmount, line **208**, filename length 41, `From<AnchorError>`, `Error::with_values` |
| 1240 | `6027` NotEnoughRemainingAccounts, line **214**, 41, `From` (no `with_values`) |
| 1464 | `6106` MultiHopHopFeesMismatch, line **218**, 41, `From` (no `with_values`) |
| 2176 | `memcmp`, `name`, `ToString`, line **262**, `6098` MultiHopDiscontinuousPath, `From`, `Error::with_pubkeys`, `rust_begin_unwind` |
| 2800 | `CurveHop::try_accounts`, then `0x5b3b0`, `AccountsExit::exit`, `abort`, a syscall, `PreviousHop` drop, `FnOnce::call_once` |

There is one `with_values` in the window (the amount check). The length and hop-fee checks are plain `require!`. Adding `require_gte!` for a slippage test would insert a second `with_values` the original does not have.

Our dispatcher now stores lines 208, 214, and 218 at the same offsets as the original (984, 1256, 1480). The discontinuous-path `require_keys_eq!` is still line 805, and the compiler lays that cold block after the loop. Between the third `From` and `try_accounts` the original does not call `validate_trade` or `prepare_bonding_curve`; those stay in our dispatcher because they sit in the hop loop outside `run_curve`. Moving them into `run_curve` would shrink the dispatcher. `run_curve` stays on source line 483, and every `error!` / `require!` line outside 208/214/218 is unchanged.

## `trade::sell` lines 1126 / 1127 / 1148

`0x14a8a8` (6,032 bytes) is `trade::sell`, not a separate costs helper. Its `with_values` sites are:

| code | variant | line |
| ---: | --- | ---: |
| 6022 | SellZeroAmount | 1126 |
| 6023 | NotEnoughTokensToSell | 1127 |
| 6003 | TooLittleSolReceived | 1148 |

The balance check was on line 1129 and the slippage check on line 1155. Both now use `require_gte!` (`Error::with_values`) on 1127 and 1148. The slippage macro is an `#[inline(always)]` nested function so `line!()` is 1148 while `error!(Overflow)` stays on 1155 and the truncation closure stays on 1140. Outlining only that check (without `inline(always)`) left line 1148 in a 608-byte function outside the window.

| `trade::sell` | size | opcode LCS / 734 |
| --- | ---: | ---: |
| lines 1129 and 1155 | 8,160 | 0.826 |
| lines 1126, 1127, 1148 inside the body | **8,160** | **0.858** |

Normalized score stays 1,010 with no losses. The body is still 2,128 bytes above 6,032. Pulling 1126–1148 into an `#[inline(never)]` helper would move these three immediates out of the function that carries the 0.858 alignment, so that split is not in this build.
