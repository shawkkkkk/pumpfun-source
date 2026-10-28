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
