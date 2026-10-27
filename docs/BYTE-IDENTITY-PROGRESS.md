# Byte-identity progress after the 26 October audit

The [full audit](RECONSTRUCTION-AUDIT.md) and its generated tables retain their
explicit `1463bd22` snapshot. This log records later research without silently
changing that baseline or promoting new selected artifacts.

## Fees: social-PDA creation body recovered

The [creation-body recovery](../research/fees-social-creation-body/README.md)
reproduces the complete 3,296-byte original function at 190104, including feature
logging, existing-state precedence and its error location. All 18 direct callees
match, with no prior raw-local or normalized match lost. Fees advances to
**396 unique structural pairs and 42 unmatched windows**. A fresh control
reproduces the parent exactly; the proposal passes 17,331 existing comparisons
and 157 strict signed controls, fixing 12 instruction-outcome differences in
the added existing-PDA cases. Whole-file identity remains unachieved.

## Relay: original security metadata recovered from source

The [security declaration recovery](../repro/donation-relay/security-metadata-source-recovery/README.md)
adds the ordinary, checksum-pinned `solana-security-txt` macro and the saved
semantic fields. It recovers the original **510-byte payload**, the missing
`SECURITY_TXT` export/relocation, and the entire **247-byte `.dynstr` section**
byte-for-byte. It retains **482/492 normalized windows, 130 raw local matches,
and all 348 equal source-location pairs**, with no loss. Fresh offline replay
passes 536 records / 534 unique fixtures under the existing bounded comparator.

The independent native Linux control reproduces the previous candidate exactly.
The recovered compiler ELF is 818,664 bytes versus the original ELF extent of
818,280; the full captured allocation is 830,448 bytes including 12,168 trailing
zero bytes. No allocation padding or binary patch is added. Ten original bodies,
other section contents and whole-file identity remain unresolved.

## Relay: donation controls retain the 482-window frontier

The [donation source controls](../repro/donation-relay/donation-source-controls/README.md)
retain 59 builds and 173 targeted comparisons for the four donation wrappers
and shared worker. Construction order, argument handling, ownership timing,
CPI moves and result tuple layouts recover no new complete window. Some
ownership variants lose the matched context-drop helper and are rejected.
The unmodified control reproduces each compiler recipe's exact parent binary.
No new VM execution or source promotion is claimed; Relay remains 482/492 with
10 unmatched. These negative results are separate from the Fees gains below.

## Fees: authority body and refreshed duplicate attribution

The [authority-update study](../research/fees-authority-body-origin/README.md)
recovers the full 3,320-byte original body at 103,408 by preserving its tokens
and reproducing its diagnostic source location. It raises the frontier to
**354 unique structural pairs and 84 unmatched windows**, with no loss. Its
unpadded source-location control loses two later windows and is rejected.

The [fresh call-context analysis](../research/fees-refreshed-call-attribution/README.md)
then rederives 61 additional duplicate-body correspondences on that exact
candidate, for **415 attributed pairs**. Eight attributions are new, with no
previous one lost. It retains 86 unresolved duplicate windows, 2,485 consistent
bound call edges and 22 different-body frontier edges. No additional machine
body coverage or exhaustive semantic identity follows from the attribution.

## Relay: 11 → 10 unmatched normalized windows

The [burn/close ownership recovery](../repro/donation-relay/burn-mint-ownership-recovery/README.md)
recovers the complete 2,856-byte original window 109. The nonzero branch consumes
the mint instead of cloning it, and full context destructuring recovers the
conditional cleanup/return layout. All 24 direct-call sites bind to matched
callees. Both compiler recipes reach **482/492 normalized windows**, **130 raw
local matches**, and **10 unmatched**, with no losses. Each recovered binary
passes fresh 536-record / 534-unique-fixture replay; privileged-success coverage
limits remain. The same 348 source-location pairs remain equal.

The packet retains 36 negative epoch-close builds and eight negative ownership
variants alongside the recovered Darwin/Linux builds. These control results do
not constitute accepted epoch-close reconstruction. Whole-file identity remains
false; the full inventory and remaining-work report are updated.

## Relay: 12 → 11 unmatched normalized windows

The [Jupiter optional-seed recovery](../repro/donation-relay/jupiter-option-source-recovery/README.md)
recovers the complete 2,496-byte original window 90. The previous four-slot
residual concealed a pointer-versus-length distinction: the helper accepts an
optional seed slice, and Rust `match` reproduces its branch layout. `Some(&[])`
and `None` select different invocation wrappers. Both the Darwin/Linux-library
and full Linux builds reach **481/492 normalized windows**, **130 raw local
matches**, and **11 unmatched**, with no losses. Each passes 536 fresh replay
records; the existing privileged-success coverage limits remain.

All 11 direct-call sites bind to matched callees. The original 346 equal
source-location pairs are retained and two are added, for **348/348**. Relative
to the iterator-clone controls, each stripped binary changes at only ten byte
positions. Whole-file and exhaustive semantic identity remain unproved.
Nineteen metadata-source trials and the `if let` form are retained as negative
controls. The full function inventory and remaining-work report are refreshed.

## Fees: Darwin target-library substitution rejected

The [controlled library trial](../research/fees-target-library-control/README.md)
keeps all 33 source inputs and the Linux compiler unchanged while substituting
the official Darwin target libraries. It loses four original Type-ID windows:
352 unique pairs and 89 unmatched versus the retained 353/85 checkpoint. The
trial is not promoted. Its focused comparisons pass, which does not erase the
structural regression. An independent stored-artifact comparison also confirms
that all four selected core programs remain raw-byte unequal to their captures.

## Relay: narrowed Jupiter CPI residual, no match-count change

The [residual CPI source trials](../repro/donation-relay/residual-cpi-source-trials/README.md)
bank 53 builds. Iterator-based cloning reproduces 308/312 normalized instruction
slots of the 2,496-byte Jupiter builder; four stack load/store slots remain
unequal and are explicitly retained by the strict matcher. This is **not** a new
complete match: the candidate retains 480/492 windows, 130 raw local matches and
12 unmatched, with fresh 536-record replay. A separate source-only build confirms
the same artifact. The 32 burn/close trials recover no complete body; their
ownership, field-order and return-form variants are preserved as negative evidence.
No selected source or research checkpoint is promoted.

## Post-PR123 cross-program review

The [current reconstruction review](RECONSTRUCTION-STATUS.md) refreshes the full
4,415-row inventory and separates selected artifacts, current research, raw body
matches, normalized matches, opaque windows and behavior gaps. Relay's 12
unmatched windows span 57,968 original body bytes; Fees' 85 span 348,264. These
are whole-window extents, not counts of missing bytes or effort estimates.

## Fees: 87 → 85 unmatched normalized windows

The [Shareholder Copy study](../research/fees-shareholder-copy-clone/README.md)
recovers the complete 336-byte vector-clone window at 58,520 and independently
binds both encoded calls to raw-equal helpers. Its FeeTier-only negative control
adds no match. The [buyback initializer study](../research/fees-buyback-initializer-origin/README.md)
then recovers the complete 600-byte body at 120,216 by moving the unchanged
helper to the original diagnostic path/line. These studies add one unique pair
each with no losses: **353 unique structural pairs, 85 unmatched windows**.

The current candidate has 107 original windows with any raw-equal counterpart,
including ambiguous duplicates; 57 unique structural pairs are raw-equal. It
retains 17,331 suite cases and 1,542 exact outcome/log/compute comparisons. The
proposal replays are fresh; identical control receipts are explicitly reused.
Neither full capture nor meaningful ELF equality is achieved. Historical
duplicate-call attribution counts must be rederived before claiming them for
this candidate.

## Relay: 43 audited location differences → 0

The [compiled source-location study](../repro/donation-relay/source-location-recovery/README.md)
executes all four proposals from the independent location audit, separately and
combined. The same 346 recognized `(window, reference-offset)` pairs remain
present; all now agree in path, line and column. Instruction matching remains
**480/492**, with **12 unmatched** and no normalized losses. The combined build
has **130 raw local matches** and passes all 536 records / 534 unique fixtures.
An independent full Linux SDK build of the same 56 source inputs confirms all
those matches and location values, with its own fresh replay. This closes the
audited location-value differences, not all data or relocation equality.

## Relay: fully Linux build confirms 480-window frontier

The [Linux canonical reproduction](../repro/donation-relay/linux-canonical-reproduction/README.md)
uses the same recovered source with the official Linux v1.48 SDK. It independently
reaches **480/492 normalized windows**, **127 raw local matches**, and the same
**12 unmatched windows**, with 536 fresh replay records passing. A real root-crate
rebuild was required after two inconclusive Cargo cache-reuse attempts; those
attempts and the final compiler invocation are retained. The Linux and earlier
Darwin/Linux-library outputs differ at 9,469 file positions, so this confirms the
window frontier and finite runtime results, not host-independent ELF equality.

## Relay: 13 → 12 unmatched normalized windows

The [mint-fee predicate study](../repro/donation-relay/mint-fee-pair-recovery/README.md)
recovers the complete 3,440-byte mint-policy window 106 by expressing the same
zero-fee test as a tuple comparison. Only three register-operand bytes change in
the full stripped output. No previous match is lost. The current candidate has
**480/492 normalized windows**, **127 raw local matches**, and **12 unmatched**,
with all 536 records / 534 unique fixtures passing fresh replay. The separate
serial-condition trial is retained as a negative result.

## Relay: 22 → 13 unmatched normalized windows

The [framework/sysroot/share-error study](../repro/donation-relay/framework-sysroot-recovery/README.md)
recovers nine more original windows without losing any of the previous 470:
four framework/CPI/resize helpers, the Pubkey base58 writer, three raw-equal
`StringError` type-ID bodies, and the missing share-total `with_values` helper.

The best retained candidate has **479/492 normalized matches**, **127 raw local
matches**, and **13 unmatched windows**. It passes fresh replay of all 536 records
/ 534 unique fixtures. The share-total error now includes `(sum, 10000)`; its three
callers and complete captured helper are independently checked. The corpus does
not establish the protected rejection path end to end.

This is an explicit cross-host recipe: Darwin v1.48 compiler and linker with
official Linux v1.48 target libraries, Anchor Lang/SPL 0.32.1 and resolved macros
0.32.2. It is not a claim of a full Linux-host build or the unique historical
recipe. Whole-file identity and selected-artifact promotion remain open. All 13
remaining windows belong to donation/settlement bodies, mint policy, Jupiter CPI
construction, residual burn/close, and the shared donation worker.

## Relay: repeated type-ID attribution, no count change

The [StringError provenance study](../research/relay-string-error-provenance/README.md)
connects the candidate's three repeated type-ID bodies to `alloc`'s internal
boxed `StringError`, rather than `std::io::Error` itself. Seventeen successful
local compiler/target probes do not reproduce the captured constants; two
missing-library failures and six build-setting controls are retained. One
v1.48 canonical-target probe reproduces the latest candidate constants. Full linked-sysroot
provenance remains open. Relay stays at **470/492**, with **22 unmatched**.

## Relay: 26 → 22 unmatched normalized windows

The [Token-2022 dependency-path study](../repro/donation-relay/token-extension-version-recovery/README.md)
recovers full original windows 240, 242, 243 and 244: TLV data inspection, total
TLV sizing, required account extensions and token-instruction packing.

Latest research: **470/492 normalized windows**, **88 raw local body matches**,
**22 unmatched**, with no prior normalized window lost. All 536 records / 534
unique fixtures pass fresh original/candidate replay. The 812,864-byte output
still differs from the original; selection and exhaustive behavior are unresolved.

The direct Token-2022 v8 control had no normalized gain. The successful trial
also changes Anchor SPL's separately pinned token-interface dependency to v8,
using otherwise unchanged Anchor SPL Rust source. This identifies a matching
tested source/dependency arrangement, not the uploader's historical manifest.
The audit verifies 187 registry packages / 4,135 files; failed offline cache
preparations and the negative control are retained.

## Relay: 27 → 26 unmatched normalized windows

The [SwapReceipt coordinate study](../repro/donation-relay/swap-receipt-coordinate-recovery/README.md)
reproduced the retained 465-window build, tested the canonical target with fixed
source, and recovered the full 1,120-byte decoder at original window 167.
The observed attribute coordinate is line 5, not line 2. Moving the attribute by
three blank lines changes exactly two output bytes and loses no normalized match.

Latest research: **466/492 normalized windows**, **88 raw local body matches**,
**26 unmatched**. Fresh replay of 536 records / 534 unique fixtures gave zero
mismatches and reproduced the saved original observations. The output remains
813,968 bytes and is not equal to the 830,448-byte captured allocation.
These counts do not establish historical source text, all transitive data/calls,
successful privileged settlement or complete semantic equivalence.

The target-only control recovered no normalized window, so it is retained as a
negative result for the repeated `Error::type_id` hypothesis. The three type-ID
windows still need work. The current residual list is in the new package.

## Fees: 89 → 87 unmatched normalized windows

Merged [PR #120](https://github.com/lalalune/pumpfun-source/pull/120) restores the
source origin of two unchanged buyback helpers and recovers their complete
inlined program-body windows. The [buyback-origin packet](../research/fees-buyback-update-origins/README.md)
reaches **351 unique structural pairs**, with no loss and **87 unmatched** windows.
It retains 17,331 proposal suite cases, 1,542 focused comparisons, and a separate
1,249-case buyback suite. The initial missing-fixture attempt is preserved.
Selected artifacts and whole-file identity remain unchanged.

## Fees: 92 → 89 unmatched normalized windows

Merged [PR #117](https://github.com/lalalune/pumpfun-source/pull/117) recovers three
complete donation, sharing-config and social-creation account-parser windows.
The [creation-origin packet](../research/fees-creation-account-origins/README.md)
reaches **349 unique structural pairs**, with no loss and **89 unmatched** original
windows. It retains exact declaration/path/line evidence, 17,331 proposal suite
cases and 1,542 focused comparisons. Whole-file identity remains false.

## Fees: 94 → 92 unmatched normalized windows

Merged [PR #116](https://github.com/lalalune/pumpfun-source/pull/116) restores the
recorded source paths and derive lines for the two initializer account parsers.
It recovers complete 6,320-byte and 5,888-byte windows, reaching **346 unique
structural pairs** with no loss and **92 unmatched** original windows. The
[initializer-origin packet](../research/fees-initializer-account-origins/README.md)
verifies declaration preservation, exact path/line references, 17,331 proposal
suite cases and 1,542 focused comparisons. Selection and whole-file identity
remain unresolved.

## Fees: 95 → 94 unmatched normalized windows

Merged [PR #109](https://github.com/lalalune/pumpfun-source/pull/109) recovers the
complete 1,560-byte `get_fees` wrapper. Unique structural pairs rise from 343
to **344**, with no previous match lost and **94 unmatched** original windows.
The [optional-boolean study](../research/fees-optional-bool-query/README.md)
retains 17,331 passing full-suite comparisons and a separate 1,542-case focused
matrix covering every optional-byte value and absence. In the focused matrix,
proposal outcomes, raw logs and compute units agree; the retained control has
1,539 log/compute differences. These are finite cases, not whole-program proof.
Selected Fees source and artifacts are unchanged.

## Fees: 98 → 95 unmatched normalized windows

Merged [PR #96](https://github.com/lalalune/pumpfun-source/pull/96) recovers a
376-byte tier selector, a 656-byte quote selector and a 1,384-byte generated
quote-query wrapper. Its source separates helper boundaries, derives `Copy` for
Fees, and uses the observed Pubkey comparison order.

That research output has **343 unique structural pairs** (up from 340), **95
unmatched original windows**, and retains 17,331 finite passing comparisons.
The 393 call-attributed-pair count in the earlier audit belongs to the earlier
stable-sort build; it has not been automatically transferred to this candidate.
Selected Fees source and binary are unchanged. See the
[query-selector evidence](../research/fees-query-selectors/README.md).

## PR review and evidence maintenance

PRs #97–#99 clarify provenance, licensing and the distinction between executed
and post-hoc evidence. PR #95 now checks all pass-27 guard files before import;
its conflicts were resolved while preserving the newer audit and README pins.
These are evidence/guard changes, not byte-identity gains.

Whole-program status remains **0/4 selected core programs**, with selected Relay
also byte-unequal. The original byte-identity goal remains open.

## Shared-worker flow audit and mint-source controls

The [flow audit](../repro/donation-relay/shared-worker-flow-audit/README.md)
recomputes the original/current shared-worker instruction graphs. Every path
to an explicit return crosses the matched context-drop helper, including paths
from the transfer continuation. Calls are assumed to return; this is not a
semantic or runtime-success proof. Different linear cleanup offsets do not
establish different ownership stages. Five additional compiled mint-key and
whitelist-slice forms remain negative, with no lost matches. Relay remains at
482/492 with ten unmatched bodies and 130 raw local body matches.

## Complete partial-argument control family

All [32 subsets of donation argument fields](../repro/donation-relay/partial-argument-controls/README.md)
were compiled across the five source wrappers, yielding 128 negative comparisons
against original windows 92–95. The other source inputs, context field order and
compiler recipe remain fixed. Partial binding alone does not recover these
wrappers under this recipe. Every variant retains the 482/492 frontier and 130
raw local body matches, with no gained or lost matched window. No candidate is
promoted and no fresh runtime acceptance is claimed for these controls.

## Conditional regular/payer wrapper value flow

The [restricted caller diagnostic](../repro/donation-relay/wrapper-value-flow/README.md)
compares four modeled success/error traces. Both wrappers agree on 204 selected
context bytes, 68 argument bytes, and 153 success/24 error return bytes under
explicit callee summaries, nonwrapping guards and input-address assumptions.
Eight negative-control tests detect changed bumps, event discriminators, copy
lengths and unsupported model operations. These are conditional caller findings,
not fresh runtime acceptance, semantic equivalence, or new byte matches. Relay
remains at 482/492, with 130 exact local bodies and ten unmatched windows.

## Epoch-close field and error-result controls

Fourteen [compiled controls](../repro/donation-relay/epoch-source-controls/README.md)
test retaining debouncer fields across initialization and varying the checked-add
error/Result construction. None recovers the 4,000-byte original epoch-close
window. Every variant retains 482 normalized and 130 raw local matches with no
gained or lost window. No candidate is promoted or newly runtime-accepted.

A separate compiler-only control keeps the source, Cargo, linker and Linux target
libraries fixed while substituting the cached Darwin v1.50 Rust compiler. It
produces 226 normalized / 108 raw local matches, losing 256 normalized windows
and gaining none. The rejected 800,608-byte output and tool fingerprints are
retained in the same packet. This does not identify a historical compiler or
prove anything about other v1.50 recipes; no runtime acceptance is claimed.

## Root-profile and Result-helper controls

The [twelve-build packet](../repro/donation-relay/profile-result-controls/README.md)
reproduces the baseline exactly, then tests four root compiler overrides and seven
Result-helper source variants. No build gains a new original window. The compiler
overrides lose 100, 166, 168 and 110 matches; the source variants retain 482. A
unit-result helper duplicates original window 115, which was already matched by
an Error-returning helper. This is evidence against inferring a unique Rust return
type from local body shape, not additional recovery. The Relay frontier stays
482/492 with 130 raw local bodies and ten unmatched windows.

## Shared-worker arithmetic and tip-order controls

Six [compiled source forms](../repro/donation-relay/arithmetic-order-controls/README.md)
test in-place checked operations and naming the tip division before/after state
updates. All retain 482 normalized and 130 raw local matches without recovering
the worker. The two tip-only forms reproduce the candidate and symbol image
exactly. No candidate is promoted, and no new runtime acceptance is claimed.

## Swap caller layout and constructor order

The [six-build study](../repro/donation-relay/swap-caller-controls/README.md)
prints the current Rust account/context layouts without changing the baseline
binary. A reordered burn-context initializer removes `just_swap`'s extra memcpy
and passes fresh original/candidate replay of 536 records / 534 unique fixtures.
Its 4,408-byte body still differs from the original's 4,448 bytes. Four wire-arg
variants also remain unmatched. No matched window is gained or lost, and no
candidate is promoted. The original field-name mapping remains an inference.

## Settlement direct-call inventory

A [read-only ledger](../repro/donation-relay/settlement-call-audit/README.md)
checks all direct local calls in original windows 97–100 against both published
candidate forms. All callees have normalized-body counterparts; three baseline
caller multisets agree, and the constructor-order candidate agrees for all four.
No linear sequence or full caller body matches. The result narrows investigation
without asserting control-flow or semantic equivalence. Counts remain 482/492.

## Legacy Fees account ownership and total-check source probe

[PR #140](https://github.com/lalalune/pumpfun-source/pull/140) adds two complete
Fees body counterparts without losing a prior match: a 776-byte raw-equal
legacy cleanup and a 1,072-byte normalized dispatcher. Its standalone verifier
passes. The refreshed 585-window inventory now contains 108 raw, 395
normalized-only and 82 unmatched windows. There are 356 unique structural pairs
and 61 additional call-attributed pairs (417 total); 86 duplicates remain
unattributed. The newly recomputed call ledger has 2,493 bound-target edges and
23 different-body edges. Candidate size is 854,672 bytes; full ELF identity fails.

Separately, the [fee-total probe](../research/fees-total-predicate-probe/README.md)
reproduces a 192-byte predicate's instruction sequence using ordinary Rust. It
uses the Darwin v1.44 compiler and an isolated object; panic operands and full
Linux-candidate integration remain unresolved. It adds zero inventory matches.

## Fee-total predicate integrated and original diagnostic restored

The [full Linux packet](../research/fees-total-predicate-integration/README.md)
rebuilds PR #140's control exactly, then connects the predicate to the real fee
validator. Both variants gain original window 700568 (192 bytes), losing none:
357 unique structural pairs, 81 unmatched windows and 58 unique raw pairs. The
complete inventory partitions Fees into 108 raw, 396 normalized-only and 81
unmatched original windows. Call refinement yields 418 correspondences, 2,494
bound-target edges and 23 different-body edges; 86 duplicates stay unattributed.

The preferred method also reconstructs the observed `pump-fees-math/src/lib.rs`
line 28, column 9 and the overflow message. Both candidates pass fresh 17,331-case
suite and 1,542-case exact focused replays; all 15 applicable overflow diagnostic
cases match for the preferred candidate. Original helper callers remain open.
The failed missing-host-linker attempt and rejected stale-cache attempt are
retained explicitly. This updates research evidence, not selected program pins.

## Flat-fee setters and V2 sharing combined

The [new packet](../research/fees-config-setter-recovery/README.md) recovers the
two 624-byte flat/exotic setters, including their field writes, source origins
and all ten direct local callee bindings. The first edit lost two unrelated
matches by shifting source lines; restoring the blank line preserves both.
The rejected build is retained. The corrected setter candidate gains two and
loses none.

[PR #143](https://github.com/lalalune/pumpfun-source/pull/143) was also verified
and merged. Its V2 ownership change was compiled together with the setters:
all five gains survive in one actual binary, for 362 unique structural pairs,
59 unique raw pairs and 76 unmatched windows. Full window counts are 109 raw,
400 normalized-only and 76 unmatched. Call refinement gives 423 correspondences,
2,515 bound-target edges and 24 different-body edges; 86 duplicates stay
unattributed. Both the corrected setter and combined candidates pass fresh
17,331-case suites and 1,542-case exact matrices. Whole-file identity still fails.

## Complete normal and stable tier replacement/upsert bodies

The [six-variant packet](../research/fees-tier-splice-recovery/README.md) recovers
both 4,160-byte tier bodies and two helpers at 54864 and 784168. `FeeTier: Copy`,
an explicit usize limit, an aggregate validity predicate, and the correct stable
vector base/source positions explain the successive compiled differences.
No prior body is lost. [PR #145](https://github.com/lalalune/pumpfun-source/pull/145)
independently recovered the reserve helper and was verified/merged; that body is
counted only once in the combined candidate.

The final build has 366 unique structural pairs, 72 unmatched originals and 63
unique raw pairs. The full inventory records 116 raw, 397 normalized-only and 72
unmatched original windows. Call refinement gives 427 correspondences, 2,572
bound-target edges and 24 different-body edges; 86 duplicates remain unattributed.
All 57 direct calls in the four new bodies reach matching local callee bodies.
Fresh 17,331-case and 1,542-case exact replays pass. Whole-file identity still fails.

## Configuration-event borrowing and stored admin

The [two-build recovery](../research/fees-config-event-recovery/README.md) removes
four unnecessary event clones, then uses the configuration's stored admin value.
The unchanged `has_one = admin` constraints guard the instruction path. All four
caller bodies now match, with no existing match lost. Two callers add unique
pairs; the upserts form a duplicate-body group. Outgoing-callee checks identify
both upserts uniquely and agree with incoming-call attribution.

The final candidate has 368 unique structural pairs, 149 original windows in
ambiguous body groups and 68 unmatched windows. The full partition is 116 raw,
401 normalized-only and 68 unmatched. Call refinement gives 431 correspondences
(63 additional duplicate pairs), 2,625 bound-target edges and 20 different-body
edges; 86 duplicates remain unattributed. All 49 local calls in the four recovered
callers have matching callee bodies. Fresh 17,331-case and 1,542-case exact
replays pass. Whole-file identity still fails.

## Exotic-fee growth and rejection precedence

The [new 24-case matrix](../research/fees-exotic-growth-precedence/README.md)
finds four disagreements in the previous research candidate. The original can
fund/grow a short account before validating fees and uses realloc zero-init=false.
The minimal correction removes all four disagreements and passes fresh 17,331
broad cases plus 1,542 exact focused comparisons. Nine source trials are retained;
one matches the original caller's size but not its body. No full body is gained
or lost: 368 unique pairs, 68 unmatched. The current research candidate hash is
refreshed; selected sources and checkpoint pins are not promoted.

PR #148's Mayhem history package was merged and its offline checker passed. That
checker verifies hashes, account captures and a derived version chain, not an
independent raw transaction re-decode. The five field roles remain open and the
new history is linked as evidence for further checking.


## Post-PR #149 comprehensive review — 26 October 2026

Recomputed the [4,415-window inventory](../repro/reconstruction-status-2026-10-26/README.md)
and reconciled [all 150 handlers](../repro/reconstruction-status-2026-10-26/review.md)
against the immutable selected audit. No new body or behavior recovery is claimed.
The report separates selected/research builds, exact local bytes, normalized-only
matches, unmatched bodies, opaque windows and bounded/partial/unaccepted handlers.
It records unresolved text size per build and the largest remaining windows.
The current Fees call ledger has 2,625 bound-target edges and 20 different-body
frontier edges; the old overview's 24-edge value has been corrected.


## Optional AMM event-authority ownership — 26 October 2026

[The isolated source recovery](../research/fees-optional-account-ownership/README.md)
recovers original 10,232 (528-byte normalized parser) and 41,560 (160-byte raw
cleanup) through the real create-sharing account context. Only the optional
AMM event-authority field changes to owned `AccountInfo`. No matches are lost:
370 unique structural pairs, 66 unmatched, 117 raw-local windows. The new
candidate passes 17,331 suite cases, 1,542 exact focused comparisons, 24 growth
cases and 32 optional-account boundary cases. Its enclosing parser remains
unmatched; whole-file equality and selected-source promotion remain open.


## Social-claim signing-seed vector — 26 October 2026

[Copying the stored user-ID bytes before the V2 token CPI](../research/fees-social-seed-vector/README.md)
recovers the complete 296-byte original window at 51,608. Raw differences are
restricted to the two call immediates, whose callee bodies match. No matches are
lost: 371 unique pairs and 65 residuals. The larger claim caller remains
unmatched. Fresh regression and 20 user-ID byte-length/token-path cases pass;
whole-file identity and selection remain open.


## Extension-size logs and formatting — 26 October 2026

[Two restored no-resize log branches](../research/fees-extend-size-logs/README.md)
recover original formatting helper 52,568 (448 bytes), with three matched callee
bodies and no lost coverage. Fees reaches 372 unique pairs / 64 unmatched.
Eight signed cases have matching program logs after differing in all eight on
the parent. The enclosing resize body remains unmatched. A 24-byte previously
normalized body becomes raw-equal under the changed layout without new coverage.
All broad and focused regression suites pass; no selected checkpoint is promoted.


## Crank boxed interface-mint parser — 26 October 2026

[Changing the quote-mint context type](../research/fees-crank-interface-mint/README.md)
recovers original 9,880 (352 bytes), with all three callee bodies matched.
Two previously ambiguous originals become unique, giving 375 structural pairs,
147 ambiguous original windows and 63 unmatched. Only one new original body is
covered. Thirty owner/length cases correct ten parent/control discrepancies;
all broad and retained focused regressions pass. The enclosing crank parser,
whole ELF and selected-source promotion remain open.


## Common zero-quote predicate — 26 October 2026

[The Borsh helper expression](../research/fees-curve-zero-helper/README.md)
recovers original 75,880 (504 bytes), including four direct callee bodies and two
source-location records at `common/mod.rs:21`. The array and `TryFrom` controls
produce an identical 432-byte nonmatching body. Fees reaches 376 unique pairs
and 62 residuals with no lost normalized or raw coverage. Existing fee-sharing
callers remain unresolved; fresh broad and focused regressions pass.


## Current-frontier slice-location integration — 26 October 2026

[The four location corrections](../research/fees-slice-origin-integration/README.md)
are now integrated into the 376-pair Fees research source. A fresh build changes
exactly eight `.data.rel.ro` bytes and preserves the complete instruction
section. Actual location records, panic message pieces, formatter, callers and
panic target are checked. Counts remain 376 unique pairs / 62 unmatched; all
intervening body/runtime gains are preserved. Fresh broad/focused regressions
and three mutation tests pass. Whole-file identity remains open.


## Buyback initializer context ownership — 26 October 2026

[Boxed vault/token accounts and owned event/program infos](../research/fees-buyback-context-ownership/README.md)
recover the 7,184-byte parser, 5,512-byte initialization closure and 560-byte exit.
No normalized or raw coverage is lost: 379 unique pairs / 59 unmatched. The
adjoining 6,256-byte closure remains unresolved (the parser span is not 13,440
matched bytes). All 29 closure/exit callees and 57/58 parser callees match.
Previous location fixes survive; fresh broad and focused regressions pass.


## Buyback context source-origin closure — 26 October 2026

[Relocating the unchanged context declaration](../research/fees-buyback-context-origin/README.md)
to `instructions/buyback/mod.rs:12` recovers original closure 358,312 (6,256 bytes),
closing the parser's remaining direct-call mismatch. The four buyback context
components now bind 104/104 direct callee bodies. Counts reach 380 unique pairs
and 58 unmatched; one further duplicate attribution gives 442 total pairs.
The initializer function stays on line 94, previous location fixes survive,
and fresh broad/focused regressions pass. Whole-file identity remains open.

## Fees: crank event-account ownership recovers two bodies

The [event-account ownership study](../research/fees-crank-event-ownership/README.md)
recovers the complete crank exit (424,824; 952 bytes) and dispatch wrapper
(656,832; 840 bytes). Using an owned `AccountInfo` reproduces two original field
loads that were 40 bytes off. All 12 exit callees and the separately checked
owner/field-label bytes match. The parser and business handler called by the
wrapper remain unmatched. No previous raw or normalized match is lost.

The frontier is **382 unique structural pairs, 147 ambiguous original windows,
and 56 unmatched windows**, with 118 raw-local matches. Call refinement yields
444 correspondences (62 additional duplicates), 85 unattributed duplicate
windows, 2,768 bound-target edges and 21 different-body frontier edges. The
residual spans 296,712 original text bytes (37.1%). Fresh regression passes all
17,331 suite cases, 1,542 exact flag comparisons and the five focused matrices.
This remains a research build, with no whole-file or exhaustive behavior claim.

The separate [root compiler controls](../research/fees-wrapper-codegen-controls/README.md)
retain a fresh byte-equal one-unit control and four rejected unit-count variants.
None recovers the buyback wrapper or gains any body; all four lose prior matches.
They are static evidence only and are not promoted or replayed as candidates.

## Fees: sweep context recovery closes three bodies

The [sweep context study](../research/fees-sweep-context-ownership/README.md)
recovers the complete account parser (370,640; 9,280 bytes), exit (379,920;
944 bytes) and dispatch wrapper (651,272; 1,320 bytes). The source boxes three
accounts and owns the event/program account infos. Boxes alone, owned unchecked
accounts alone, and their broader combination each add no complete matches.
The final variant preserves every previous normalized and raw match.

All 77 parser and 12 exit callees match. The wrapper still calls the unmatched
sweep business body at 120,816. The prior crank wrapper retains its two explicit
frontiers. Exit owner/label data and prior panic-location contracts are checked
separately from instruction equality.

Fees now has **385 unique structural pairs, 147 ambiguous original windows,
and 53 unmatched windows**, partitioned as 118 raw-local and 414 normalized-only
matches. Call refinement gives 449 correspondences (64 additional duplicates),
83 unattributed duplicate windows, 2,875 bound-target and 21 different-body
frontier edges. Residual windows total 285,168 bytes (35.7% of original text).
Fresh full and focused regressions pass. No whole-file identity, exhaustive
behavior or selected-checkpoint promotion is claimed.

## Fees: shared buyback update context and wrappers recovered

The [buyback-update ownership study](../research/fees-buyback-update-ownership/README.md)
recovers the shared 5,856-byte parser at 331,936 and both update dispatch wrappers
at 652,592 (1,744 bytes) and 654,336 (1,568 bytes). Owning both event/program
account infos is sufficient; each single-field control adds no complete body.
All 61 direct callees match. No previous normalized or raw match is lost.

The frontier is **388 unique structural pairs, 147 ambiguous original windows
and 50 unmatched windows**: 118 raw-local plus 417 normalized-only matches.
Residual bodies span 276,000 bytes (34.5% of original text). Call refinement
yields 452 correspondences (64 additional duplicates), 83 unattributed duplicate
windows, 2,938 bound-target edges and 19 different-body frontier edges.

Twenty-five literal ranges, the earlier context/panic-location contracts and
fresh full/focused regressions pass. Nested panic/format metadata, transitive
identity and exhaustive behavior remain outside this result. The study does
not promote selected artifacts or establish whole-file equality.


## Relay: source-only shared-worker recovery proposal — 27 October 2026

The [ordinary Rust worker proposal](../repro/donation-relay/shared-worker-source-proposal/README.md)
recovers complete original window 112 (10,248 bytes), advancing its isolated
482-window baseline to **483/492 normalized windows and 130 raw local matches**,
with no losses. Cloning the mint account inside a borrowed admission helper,
direct context access and a checked increment helper recover the strict worker
shape; no register/stack masking or output patching is used.

The packet publishes only readable source, exact 56-input maps, a materializer,
static verifier/tests and a portable build recipe. Optional comparison of local
compiler outputs recomputes the complete inventory and all 51 worker direct
callee bindings. Local source builds and offline replay were performed, but the
archived replay receipt's publication is blocked: this is not downloadable or
self-contained replay proof. Default verification checks source only.

The research ELF remains unequal: 414,655 common byte positions differ and the
original has a further 12,432-byte tail. Windows 92–100 remain unmatched in this
isolated recipe. Normalized coverage is 98.17%, not overall byte identity;
complete data/indirect semantics and selected-checkpoint promotion remain open.

## Fees: three event contexts recover six complete bodies

The [event-context integration](../research/fees-event-context-ownership/README.md)
retains separate trials for six contexts. Social claim, withdrawal and social-PDA
creation each gain a complete parser and dispatch wrapper. Their combined build
preserves all six gains and every prior match. All 168 parser callees match;
each dispatch wrapper still has one unmatched business-body target.

The V2 sharing-update event conversion loses original 44,632 and 641,744, and
is rejected. Admin-reset and fee-sharing-creation conversions add no complete
body and are not integrated. The final candidate changes three source files.

Fees reaches **394 unique structural pairs, 147 ambiguous original windows,
and 44 unmatched windows**: 118 raw-local plus 423 normalized-only. Remaining
bodies span 250,048 bytes (31.3% of original text). Call refinement gives 459
correspondences (65 additional duplicates), 82 unattributed duplicate windows,
3,133 bound-target edges and 19 different-body frontier edges. Fresh full and
focused regressions, preserved data contracts and instruction-message checks
pass. This is a research result, not selected promotion or whole-file equality.

## Fees: unchecked full-buffer convention restored

The [prefix recovery](../research/fees-unchecked-prefix-recovery/README.md)
recovers original 18,384 (1,144 bytes) by consuming the eight-byte account prefix
before the payload decoder. It preserves checked parsing and the existing
2,648-byte payload body. All 11 direct helper callees and the real incoming
initializer closure match; no prior raw or normalized match is lost.

Fees now has **395 unique pairs, 147 ambiguous original windows and 43 unmatched
windows**, partitioned as 118 raw-local and 424 normalized-only matches. Residual
windows span 248,904 bytes (31.1% of original text). The graph has 460 attributed
pairs, 82 unattributed duplicate windows, 3,145 bound-target edges and 18
different-body frontier edges.

The parent fails the added native prefix regression; the correction passes 35
host contract cases. Fresh full and focused SBF regressions also pass, but their
17,331-case suite does not invoke the fixed-admin FeeConfig initializer. This
is not a claim of authorized initializer execution. Selected sources and
artifacts remain unchanged, and whole-file equality is still unachieved.


## Relay: source-only close-epoch recovery — 27 October 2026

The [close-epoch source proposal](../repro/donation-relay/epoch-close-source-proposal/README.md)
recovers original window 96 (4,000 bytes): **484/492 normalized windows (98.37%)**,
130 raw local matches, one gained window and no losses. Early epoch binding,
nested signer construction and a checked inherent increment method recover the
complete strict instruction window. All 11 direct-callee sites bind complete
normalized-matched bodies; whole-file/data/indirect equivalence remains open.

Only readable source, hashes, a materializer, eight source-only tests and a build
recipe are published. Both source states derive independently from the merged
public 482-window loader. Optional local ELF comparison recomputes the gain and
raw differences. Local builds/replay were performed, but blocked archive
publication means no downloadable replay proof is included. Protected relayer
success remains dynamically uncovered. The candidate remains unequal: 406,587
common positions differ plus a 12,440-byte original tail; no checkpoint promoted.
## Fees: isolated source-only native recipe and 27 Location corrections — 27 October 2026

The [core Fees source-only proposal](../research/fees-core-source-recovery/README.md)
reproduces an isolated PR162-derived research build with **529/585 normalized
windows, 382 unique pairs and 118 raw local matches**. Two complete windows
(291864 and 632080) are gained relative to that pinned 527-window baseline;
this is not a replacement for the newer global Fees frontier.

Ordinary event-module placement, math-module placement and the authentic published
solana-program-entrypoint 2.2.1 dependency close all 27 mismatches in a 160-use
Location-shaped-record cohort. Ninety-eight of 99 checked direct call targets
match complete normalized bodies; the extension wrapper's business callee remains
unmatched. The source-only packet supplies 36 public baseline mappings, 41 exact
recovered inputs, materializer, portable native build recipe, static verifier
and 15 passing tests. Independent local output comparison reproduces every claim.

Local independent builds and finite replay were performed, but no compiled
artifacts or runtime/build receipts are published; default verification reports
runtime_verified=false. Whole capture and meaningful ELF extent remain unequal,
with 469,722 common differing positions. Raw/data/indirect and exhaustive semantic
closure remain open; the four core programs' byte-identical count is still 0/4.
## Relay: source-only just-swap recovery — 27 October 2026

The [just-swap source proposal](../repro/donation-relay/just-swap-source-proposal/README.md)
recovers original window 99 (4,448 bytes): **485/492 normalized windows (98.58%)**,
130 raw local matches, one gained window and no losses. The existing wire-argument
wrapper, early total binding and nested scalar-bump signer construction reproduce
the strict window; all 26 direct-callee sites bind complete normalized bodies.
The prior worker and epoch source recoveries are preserved unchanged.

This is a source-only proposal with full 56-input maps, static verifier/eight tests,
materializer and build recipe. Optional local baseline/candidate comparison
recomputes the inventory and raw differences. Local builds/replay were performed,
but blocked receipt publication means this is not downloadable replay evidence.
Protected relayer success and complete data/indirect equivalence remain unproved.
The candidate is not byte-identical: 415,532 common positions differ and the
original has a further 12,448-byte tail. No selected checkpoint is promoted.
## Relay: ordinary module layout and Anchor facade — 27 October 2026

The [source-only module/facade proposal](../repro/donation-relay/module-layout-facade-source-proposal/README.md)
retains 483/492 normalized windows while improving complete raw local-window
matches **127 → 134 → 142**, with no losses. Ordinary instruction-module expansion
recovers seven raw windows; using Anchor's corresponding type reexports instead
of a redundant direct root dependency recovers eight more. All six intermediate
source states, including positional regressions, remain attributable.

Fresh optional local comparisons reproduce all six full inventories and section
comparisons. Final `.rodata` differing positions fall from 4,856 to 321 and
`.data.rel.ro` from 945 to 677; these counts do not measure missing semantics or
remaining effort. Non-instruction section lengths match, but the instruction
section remains 320 bytes longer. Whole-file identity is false.

Only readable sources/maps/diffs, static comparison counts and hashes, materializer,
portable recipe and seven tests are published. No ELF or archived build/replay
receipts are included or consumed. Default verification is source/static metadata
only and reports runtime_verified=false; local ELF remeasurement is explicit.
The later epoch/just-swap body gains are not silently included in this isolated
483-window series, and no selected checkpoint is promoted.
## Fees: pinned PR171 source integration preserves 544 windows and 161 Locations — 27 October 2026

The [pinned source integration](../research/fees-current-source-integration/README.md)
combines the previously published extension/source-coordinate recovery with the
independently reproduced PR171 revision fa8ef804. It retains **544/585 normalized
windows, 397 unique pairs and 118 raw local matches**, with no losses against that
542-window baseline. Only the same two earlier extension windows are added;
15 upstream gains and 27 earlier coordinate fixes are not new discoveries.
All **161 Location-shaped record uses** have equal decoded file/line/column
values, versus 134 on the pinned baseline. This is not a claim to the newest
moving upstream frontier or equal relocated pointer bytes.

The source-only packet provides 36 pinned public mappings, 41 exact recovered
inputs, the readable 18-path source patch, portable native recipe, materializer,
15 tests and optional local ELF comparison. Independent checks passed, including
542→544 with gains 291864/632080, no losses and the 98/99 direct-call ledger; one
known business callee remains unmatched. Local independent builds and finite
offline replay were performed, but no binary artifacts or archived build/runtime
receipts are published. Default verification reports runtime_verified=false.
Whole-capture and meaningful-ELF identity remain false: 461,447 common positions
differ, with a 4,272-byte meaningful-ELF length gap. Full core identity remains
0/4, and all-data, indirect and exhaustive semantic closure remain open.
## Relay shared worker: source-only result becomes artifact-backed — 26 October 2026

The [artifact-backed worker packet](../repro/donation-relay/shared-worker-artifact-recovery/README.md)
independently reproduces PR #167's source-only hashes with the official Linux
x86_64 v1.48 SDK. A fresh baseline matches the previous full-Linux artifact;
the recovered candidate gains only original worker window 112, loses no
normalized or raw match, and reaches **483/492 normalized / 130 raw-local**.
All **51/51** worker direct-call targets have complete normalized counterparts.

A fresh replay passes **536/536 signed records / 534 unique fixtures** with the
existing bounded comparator. The nine remaining windows are ordinals 92–100 and
span 42,368 original text bytes. The worker candidate remains whole-file unequal
and uses the source proposal's pre-security-metadata state; composition with the
separate security payload/dynamic-string-table gain and selected promotion stay
open.
## Relay: exact read-only data and tighter ordinary settlement source — 27 October 2026

The [settlement/data source proposal](../repro/donation-relay/settlement-data-source-proposal/README.md)
first composes the already recovered epoch/just-swap bodies with the published
module/facade source, then refines ordinary share-admission/recipient handling.
The frozen final candidate retains **485/492 normalized windows, 142 raw local
matches and 650 direct-call-shape-closed pairs**, with no lost windows. It adds
no new complete window beyond the previously published ordinals 96 and 99.

The entire **19,863-byte .rodata section is raw-equal**. Its .text length excess
is reduced from 304 to 120 bytes. A fresh static audit covers all 359 positional
.data.rel.ro pointers plus 507 nonpointer qwords: 282 read-only-data references
preserve offsets into the identical section, 74 text targets have closed direct
call shapes, and three data-to-data references preserve relative offsets.
Five text targets still contain indirect calls. This is not all-data semantics,
indirect behavior, historical provenance or whole-binary proof.

The compact source-only packet derives 60 exact inputs per stage from pinned
public PR175 sources, supplies six ordinary overrides/two patches and includes
nine passing tests. Independent optional comparison freshly reproduces all three
section/window inventories and the complete final positional data graph without
reading build/replay receipts. Local two-build/replay observations remain
unpublished evidence; default verification reports runtime_verified=false.
Protected relayer settlement success is not covered dynamically. No binary,
archive, encoded machine payload, runtime case or archived receipt is published.
Whole ELF remains unequal: final 818,400 versus meaningful 818,280 bytes, with
393,528 common differing positions. Seven original windows remain unmatched;
the four core programs' full byte-identical count remains 0/4.
## Fees: ordinary extension-admission diagnostic source — 27 October 2026

The [extension admission source proposal](../research/fees-extension-admission-source-proposal/README.md)
preserves a pinned 36-input public baseline and exactly reconstructs 37 proposed
source inputs with three ordinary overrides and a reversible patch. It owns the
raw account info, preserves diagnostic precedence/compared values and moves
admission checks to the captured source-attributed instruction coordinates,
without changing the parent resize/event tail or unrelated root line numbers.

Thirteen stdlib tests, exact public-source hash checks and independent complete
37-file materialization pass. The packet's successful checks attest source
integrity only: runtime_verified, native_build_verified and
whole_binary_identity_verified all remain false. Local development observed
99 corrected application-log comparisons, but that runtime evidence is
unpublished and cannot be independently verified from this source-only packet.
No logs, replay cases, binary/encoded artifacts or archived receipt excerpts
are included. The extension business body and whole original binary remain
unequal; this is diagnostic-source progress, not a new complete-body or global
frontier claim. Protected checkpoints and prior evidence remain unchanged.


## Relay: three complete settlement bodies, 488/492 normalized windows — 27 October 2026

The [settlement bodies source proposal](../repro/donation-relay/settlement-bodies-source-proposal/README.md)
recovers original windows **97, 98 and 100** (5,216, 5,696 and 5,328 bytes),
advancing 485→488 normalized windows without losses. Raw local matches stay 142;
these are not raw body or whole-program equality claims. All **99 actual direct
callee sites** bind complete normalized bodies and recursively closed direct-call
shapes. Only original windows 92–95 remain unmatched; closed pairs rise to 659.

Three ordinary source files add the actual generic basis-point iterator helper,
normal borrowed-key argument constructor and measured argument declaration order.
Two exact 60-input maps derive from pinned public PR175/PR181 source blobs. Nine
source-only tests and independent fresh local remeasurement pass. The complete
19,863-byte .rodata remains equal, and all 359 positional data pointers plus 507
nonpointer qwords retain the previously bounded relocation-aware shape result.
Five referenced text targets still contain indirect calls. .text excess falls
120→112 bytes; whole-file common differences remain 383,718 positions.

Local independent root-clean builds and finite signed replay were observed, but
no binaries, runtime cases or archived build/replay receipts/excerpts are
published. Default checks report compiler_executed=false and runtime_verified=false;
protected relayer settlement success remains untested. The 818,392-byte candidate
is not equal to the 818,280-byte meaningful original ELF or 830,448-byte capture.
All-data semantics, indirect behavior and unique historical source remain open;
whole identity across the four core programs remains 0/4.
