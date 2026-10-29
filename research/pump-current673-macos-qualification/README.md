# Frozen673 native macOS control

This is the historical673/1285 cohort. After its measurements, #711 promoted the
734 per-hop source and `c0e29e2d` / `dd73afe7` outputs to maintained main. The
historical199fd/49df control and its source pins below remain unchanged. Use the
frozen cohort ref/branch for these commands; a newer main with different sources
correctly fails the source guard. CTO/Sweep outputs here require an explicit new
main composition before promotion. Clock587 already includes734, but its exact
other64 input bindings must still be checked when relating it to the new main.

This controller runs the unchanged, hash-pinned
`pump-final-composition-cold-20261028/build.py` against the 65 maintained Pump
inputs at `1285b5e9e3a29c1e2cf32246d6046035e5d66fad`. It downloads authenticated
v1.44 native macOS tools and Linux **SBPF** libraries, fetches locked registry
packages, and lets the frozen builder authenticate every dependency source file
before compiling into an empty target. No historical executable supplies build
inputs. The physical source wrapper and frozen workspace projection are unchanged.

The control passes only when both complete outputs reproduce:

| Output | SHA-256 |
| --- | --- |
| Stripped | `199fd7379b6881adefd9e54803f75902176c17bded1718bfc1c59b1cf5bc8473` |
| Symbols | `49df399b8a36a0a60de03e8d55f1417261dc451e44845ca9d17a94040968c680` |

`python3 -B scripts/pump_current673_macos_control.py --inspect` authenticates
local inputs without downloading or compiling. Dispatch the registered fork
workflow `.github/workflows/qualify-pump-macos-v144.yml` on this branch. Its artifact
retains executed source, builder, tool/dependency bindings, compiler logs and raw
ELFs, with a hash ledger. `RESULT.json` exists only after the actual control passes;
preparing this workflow is not a successful build claim.

This replaces the old frontier798 workflow **on this branch only**. It does not
reuse or relabel that historical execution. No candidate, new window census,
runtime replay or original whole-ELF equality is claimed. Each grounded source
proposal must remain independently frozen and compared with this exact control
before any composition.

## Retained hosted proof

The unchanged [control run40791064153](https://github.com/shawkkkkk/pumpfun-source/actions/runs/40791064153)
passed on native Darwin arm64 and reproduced both complete hashes above from an
empty target. `evidence/control-40791064153.zip` is the exact uploaded artifact,
SHA-256 `b3e31aeb7512b6cec0e1aede4efbb16e72edf047451065a1e5b476223230a6ce`.
It includes raw ELFs, actual compiler source, commands, logs and authentication
receipts. No SDK or dependency target cache is included.

Run `python3 -B research/pump-current673-macos-qualification/verify.py` to check
the retained artifact hashes, actual65-to66 input projection, all254 locked
registry archive bindings, native tools/target libraries, source-preservation
receipts and genuine compilation of both local crates. The verifier also binds
the retained candidate artifacts to their sole source changes and explicit
measurement adapter. It executes no captured program or compiler.

| Independent compile | Hosted run | Stripped SHA-256 prefix |
| --- | --- | --- |
| CTO | [40792775552](https://github.com/shawkkkkk/pumpfun-source/actions/runs/40792775552) | `d537faf5907c594e` |
| Per-hop | [40792780769](https://github.com/shawkkkkk/pumpfun-source/actions/runs/40792780769) | `c0e29e2d41c30e85` |
| Sweep | [40793129553](https://github.com/shawkkkkk/pumpfun-source/actions/runs/40793129553) | `21b0de29ebc71c69` |
| SellV2 event order, compiler only | [40793772555](https://github.com/shawkkkkk/pumpfun-source/actions/runs/40793772555) | `844415f7d0615f0c` |
| Constructor array lifetime | [40794358580](https://github.com/shawkkkkk/pumpfun-source/actions/runs/40794358580) | `199fd7379b6881ad` |
| CTO used CPI flow | [40794982049](https://github.com/shawkkkkk/pumpfun-source/actions/runs/40794982049) | `df40382896c913ba` |
| Per-hop common timestamp | [40795474496](https://github.com/shawkkkkk/pumpfun-source/actions/runs/40795474496) | `0bc4a222f4040ad4` |
| Sweep native-read timing | [40796286687](https://github.com/shawkkkkk/pumpfun-source/actions/runs/40796286687) | `4e0e96a2b32b175c` |

All eight raw artifacts and exact measured hashes are retained under `evidence`.
The coordinator independently ran the unchanged official1035-window census for
the seven distinct changed images. `evidence/census` retains those full outputs and input bindings: all preserve
1019 normalized and188 raw memberships, with no original-start gains or losses.
The default verifier binds their symbol hashes and independently recomputes the
retained membership deltas; it does not rerun the normalizer. Runtime qualification
belongs to the separate source proposals and is not inferred here.
The constructor's genuinely compiled8cf source produces **both entire control
ELFs unchanged**. It recovers no bytes; no additional array/spelling variant or
runtime replay is justified by this result. This is control identity, not original
program identity.
The original Sweep attempt40792778116 failed before downloading SDKs or compiling:
the shared host's unauthenticated control-run API quota returned403. Its log and
metadata are preserved. The retry changed only control-proof retrieval to the
pinned official artifact action; the frozen Sweep source and compiler recipe
were unchanged.

## Independent candidate measurements

The `proposal` dispatch input selects `cto`, `sweep` or `perhop`. These are
separately authored, uncompiled source proposals by the CTO, lifecycle and
creation workers; storing them here supplies frozen CI inputs, not a new claim
to their recovery. `candidates/descriptors.json` records exact before/after
hashes. No proposal is composed with another.

Candidate execution requires the successful control run40791064153 at exact
head `c6ae78c36ef59de4f1b2a057b54e57b6c9f3dce7`. The pinned official artifact
download action retrieves that exact run's retained outputs using the standard
read-only Actions permission. The controller authenticates the actual ELF hashes,
RESULT, host revision, executed cold builder and complete artifact ledger before
compilation. No script reads or handles a token. A fresh isolated copy contains
the same65 source inputs with exactly one declared replacement. The unchanged
cold source is retained; its visibly derived measurement builder removes only
the final assertion demanding that the candidate output equal the control.
The original comparison and `qualified_image_hashes_equal` result remain in the
receipt. The exact adapter diff, candidate input descriptor, proposed source,
both compiler outputs and logs are retained. No candidate output hash is guessed
or supplied as an expected result. All SDK, dependency, profile, unchanged-input
and fresh-target checks remain active, with actual rustc commands required for
both local crates.

`python3 -B scripts/pump_current673_macos_candidate.py --candidate cto --inspect`
authenticates a proposal and prints the complete one-line adapter diff without
network access or compilation. A successful candidate job establishes a compiled
measurement only. The independent official census must still compare gained and
lost original starts for both normalized and raw membership, followed by the
relevant genuine signed runtime cases. Neither happens implicitly in this job.

The authored source proposals are [CTO#712](https://github.com/lalalune/pumpfun-source/pull/712),
[Sweep#713](https://github.com/lalalune/pumpfun-source/pull/713) and
[per-hop#711](https://github.com/lalalune/pumpfun-source/pull/711). Their individual
packets supply the source/call-data evidence and retain credit for that recovery.

The subsequent one-shot `sell-event` proposal (used SellV2 key/snapshot order)
compiled successfully after all three builds. The `constructor` proposal
(used six-account array lifetime) compiled after that fourth measurement and
reproduced the complete control outputs. The sixth `cto-used-flow` proposal was
dispatched as one separate measurement after the constructor: original used payout
body and three CPI constructor orders,
retaining the first CTO changes. It remains a canonical673-to-one-file comparison;
the immediate f4 source parent is additionally recorded. Its natural obsolete
helper deletion moves `token_raw_amount` from line775 to772; this is disclosed for
the actual Location audit, with all17 explicit Source sites unchanged. The SellV2
VM and old corrective/transfer-fee lanes remain stopped. These descriptors
authorize no variants or composition.

The seventh `perhop-clock` proposal is separately frozen after the sixth build:
original CFG/reaching-definition evidence selects one timestamp reused by all
three actual event constructors. It keeps the734 accrual source and changes only
three consumed statements, with no Source positions, event fields or ordering
changed. Both canonical679-to587 and immediate734-to587 source bindings are
recorded. This remains a separate one-file measurement, not a cross-file union.

The eighth `sweep-read-timing` proposal moves the one genuinely used native/quote
mint read after authorization, fee clear and zero exit as the original CFG shows.
Its canonical8735-to3d336 and immediate15db-to3d336 hashes are frozen separately.
All guards, state/helper operations, events and five bangmacro positions remain;
the vacated line27 stays blank and an existing blank is reused to preserve those
actual source positions, disclosed here. No missing predicate or byte gain is
inferred from this source-level timing evidence. The qualified15db proposal is
preserved unchanged.

## Hosted retention and a later cohort

Hosted artifacts expire after30 days. Their current download URLs and the
workflow's fixed control run are not an indefinite availability promise. The
checked-in exact ZIPs are permanent historical proof, and `verify.py` requires
no GitHub API, SDK download or network access.

To start a fresh cohort, preserve this packet and use the pinned1285 source65
with the same authenticated builder/tool/library inputs. Dispatch `proposal=control`
first and verify its actual RESULT, raw ELF hashes, host head and input manifest.
Only after both published control hashes reproduce may a new descriptor ledger
bind that **new** run ID and head, and the official download step bind its exact
artifact name/run ID. Freeze new candidate descriptors against the canonical
source, retaining each previous source/attempt separately. Never substitute an
unrun ID, reuse an expired HTTP URL as proof, relabel historical control outputs,
or overwrite this retained control ZIP. Changed maintained sources require their
own explicitly qualified frontier instead of inheriting this673 label.
