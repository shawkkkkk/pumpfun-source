# Byte-identity progress after the 26 October audit

The [full audit](RECONSTRUCTION-AUDIT.md) and its generated tables retain their
explicit `1463bd22` snapshot. This log records later research without silently
changing that baseline or promoting new selected artifacts.

## Mayhem: complete curve representation recovers four more windows

The [full curve recovery](../research/mayhem-full-curve-recovery/README.md)
reaches **345/441 normalized matches, including 59 raw-local matches**, preserving
all earlier bodies. Four newly matched windows total 1,640 original bytes;
96 windows / 348,576 text bytes remain unmatched. The boxed helpers now agree
with their immediate callees, but the lower account decoder remains unequal.
Two builds with explicit Anchor recompilation agree; all 6,636 trade comparisons,
1,032 admin cases and 12 Burn transactions pass, with 15,348 signatures verified.
Whole-file identity, remaining decoder bodies and transitive closure are open.

## Fees: V2 finishing helper advances the composed source to 573 matches

The [V2 finishing-helper recovery](../research/fees-v2-finish-source-recovery/README.md)
adds the complete 5,656-byte body at 225920 to the PR225 source. All 36 direct
callees and 27 direct data references match. Coverage reaches **573/585 normalized
windows, 143 raw-local matches, 171 equal Location observations and 12 unmatched
windows**, preserving every previous match and positive call observation. The
V2 caller remains unmatched and whole-ELF equality remains false.

Two recorded root builds agree. Review recomputed the body/call/data evidence,
checked all 17,331 saved non-log comparison results, and independently verified
18,520 transaction signatures. This review did not rerun the compiler or VM.
The packet separately retains the 119 arithmetic, eight quote-owner and 24
preprocessing cases; finite observations do not establish exhaustive semantics.

The [portable native reproduction](../research/fees-v2-transfer-ownership/README.md)
of PR222 independently reproduces its 570-window candidate and symbol artifacts.
Its five recorded compilations, source maps, SDK hashes and saved runtime
receipts are checked; seven mutation controls and 1,668 signature checks pass.
It adds no matches beyond PR222 and is not substituted for the newer 573-window
source. Neither packet promotes a canonical selected checkpoint.

## Fees: V2 transfer adapter recovered at 570 matches

The [V2 transfer recovery](../research/fees-v2-transfer-source-recovery/README.md)
adds the complete 3,096-byte adapter at 240088. The borrowed payer, owned program
account and account-initialization order reproduce the original calling
convention and cleanup. All thirteen direct callees and the System program ID
match. The result is **570/585 normalized original functions, 143 raw local
matches, 168 equal Location observations and 15 unmatched functions**, with no
prior match lost.

Repeated native Rust builds agree. Fresh execution passes 17,331 regression
cases, 119 native arithmetic cases, eight quote-owner cases and 24 preprocessing
cases. Whole-ELF/capture equality remains false; selected checkpoints are unchanged.

## Fees: current source recoveries composed at 569 matches

The [current-source union](../research/fees-current-569-union/README.md) preserves
the merged authorization, sharing-parser and native-payout recoveries, then adds
the full legacy transfer adapter and both generated transfer CPI bodies. The
result is **569/585 normalized original functions, 143 raw local matches, 168
equal Location observations and 16 unmatched functions**. All earlier matches
and positive direct-callee observations remain; the V2 outer transfer adapter
is still unmatched.

Two native Rust builds are byte-identical to each other. Fresh execution passes
17,331 regression cases, 119 arithmetic-boundary cases, eight quote-owner cases
and 24 preprocessing-boundary cases. The 119-case matrix preserves the merged
38 behavioral corrections. Whole-ELF/capture equality remains false and no
canonical selected checkpoint changes.

## Fees: shared authorization body recovered

The [authorization recovery](../research/fees-authorization-source-recovery/README.md)
adds the complete 1,208-byte function at 234096 on top of the composed563 source.
The signer-reference ABI, shared-module origin and explicit inequality guard
reproduce its full normalized body; all nine direct callees and eleven direct
data objects match. All prior matches remain. Fees now has **564/585 normalized
original functions, 143 raw local matches, 168 equal Location observations and
21 unmatched functions**. Repeated native Rust builds are identical and fresh
regression passes 17,331 cases in 18 suites. Whole-ELF/capture equality remains
false; the other incomplete helpers and selected-checkpoint boundary remain open.

## Fees: source frontiers composed, legacy payout adapter recovered

The [payout-context recovery](../research/fees-payout-context-recovery/README.md)
combines the latest 43-input Social/Crank/exotic source line with the independent
Fees558 preprocessing and distribution recoveries. It retains both sets of
normalized/raw matches, decoded source locations and positive direct-callee
observations, then adds the complete 1,688-byte adapter at 204080. The result is
**563/585 normalized original functions, 143 raw local matches, 167 equal
Location observations and 22 unmatched functions**. Its preparation callee at
199072 remains unequal; the caller match does not close that dependency.

Two native Rust builds reproduce identical outputs. Fresh regression passes
17,331 cases across 18 suites plus 24 preprocessing boundary cases. The packet
retains the two independently reproduced baselines, full source maps and scoped
checks. Whole-ELF/capture equality remains false; selected checkpoints are not
changed, and these counts are not completion percentages.

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

## Relay: independent artifact-backed 488-window settlement checkpoint

The [new artifact packet](../repro/donation-relay/settlement-artifact-recovery/README.md)
builds both exact 60-input source states from the settlement proposal with fresh
target directories. Both reproduce their expected hashes. The three new
settlement bodies (97, 98, 100) have all 99 direct callees matched, with no loss
relative to the combined 485-window baseline. The candidate retains 142 raw-local
matches, complete raw equality of the 19,863-byte read-only data section, and the
359-pointer / 507-nonpointer positional data audit. Fresh signed replay passes
536 records / 534 fixtures with the existing comparison exclusions.

The artifact-backed inventory now records 488/492 normalized matches and four
unmatched donation windows (92–95), totaling 17,680 original text bytes (2.3%).
This does not imply whole-program or arbitrary semantic identity. The compiler
ELF is 818,392 bytes versus 818,280 meaningful original bytes; no allocation
padding is added. Privileged successes and indirect/data semantics remain open.


## Relay donation cleanup controls — 27 October 2026

Two actual v1.48 root-crate builds on the accepted 488-window source tested
native event/close ordering and a borrowed-key argument constructor.
[The retained controls](../repro/donation-relay/donation-close-order-controls/README.md)
restore the original native cleanup-call sequence, but native bodies remain
40 bytes shorter and regular/payer bodies 16 bytes shorter. Both variants produce
identical binaries; full analysis remains 488 normalized / 142 raw-local windows,
with no gained or lost matches. No trial is promoted, and no runtime replay is
claimed for these rejected controls. The next source investigation must explain
the remaining caller construction differences rather than accept call topology
or artifact size as byte identity.


## Fees: isolated math ownership and authentic SyncNative pack, 545 windows — 27 October 2026

The [four-stage source-only study](../research/fees-math-pack-source-proposal/README.md)
isolates math compilation-unit ownership from authentic token instruction packing.
From the pinned PR178 544-window source, the local math crate/root reexports
preserve all 588 candidate shapes and restore seven contiguous original-order
windows without a normalized gain. The one-expression runtime-used
TokenInstruction::SyncNative.pack() recovers complete original 695672 (1,792 bytes),
reaching **545/585 normalized windows** with no losses and **118 raw local matches**.
The composition preserves both causes; it is not the latest moving global frontier.

Fresh static verification checks all 3,029 baseline/math direct edges and 3,033
pack/composition edges, retaining exactly 18 pre-existing callee-shape gaps.
All 161 Location-shaped uses remain value-equal. The new pack helper has four
matching actual callees and no direct data/external/indirect operands; its real
incoming Crank calls pass discriminant 17. The incoming Crank body, complete enum
extent, recursive semantics and all other data remain open.

The packet provides four exact 41/42-input source maps, ordinary overrides and
patches, nine tests, a pinned native recipe and optional independent ELF checks.
All 252 registry package records stay unchanged. No binaries, logs, runtime cases
or archived build/replay receipts are published; default runtime_verified=false.
Local finite suites are not downloadable replay proof and omit known Crank
application-log gaps. Pack's positional file differences worsen 461,447→468,043;
math+pack retains 466,077 differing common positions. Whole byte identity remains
false, and the four core programs' full-identical count is still 0/4.


## Relay Result/event construction controls — 27 October 2026

[Six additional ordinary-source controls](../repro/donation-relay/donation-result-shape-controls/README.md)
test explicit error propagation, result-field destructuring, event `Result::map`
and two event initializer orders. None recovers original windows 92–95. Explicit
matching produces 2,560-byte regular/payer wrappers against 2,568 original bytes,
but their complete normalized bodies still differ. `Result::map` adds function
windows and loses two raw-local matches. No trial is promoted; the accepted
inventory remains 488 normalized / 142 raw-local. One control has a fresh
all-dependency v1.48 rebuild; other retained controls contain actual root builds
with dependency-cache reuse. There is no new target execution claim.

## Relay event initializer controls — 26 October 2026

[Two further event initializer orders](../repro/donation-relay/donation-event-initializer-controls/README.md)
were compiled from the 488-window source after independently reproducing the
accepted stripped and unstripped baseline artifacts. Ordering expressions by
physical event layout or reversing the numeric field evaluation order recovers
no complete original body. Both retain 488 normalized / 142 raw-local matches;
92–95 and whole-file identity remain open. The retained receipts each contain
one actual root invocation. An initial cached-root observation was rejected and
rerun after refreshing input mtimes. No new runtime claim or candidate promotion
is made.

[All 24 owned AccountInfo construction orders were also rechecked](../repro/donation-relay/donation-context-488-controls/README.md)
on the recovered 488-window source, rather than relying only on the older
482-window controls. Every retained run compiled the root crate. All preserve
exactly the same 488 normalized and 142 raw-local matches; no missing donation
body is recovered and no existing match is lost. These controls remain rejected.

## Relay argument initializers and ELF layout — 26 October 2026

[Two DonationArgs initializer controls](../repro/donation-relay/donation-argument-initializer-controls/README.md)
compile to the exact same stripped and unstripped after-close artifacts. Moving
the message clone first inside its aggregate or following field declaration
order does not recover a body. This differs from the prior whole-argument-local
and Context-construction controls.

The [ELF layout audit](../repro/donation-relay/elf-layout-488-audit/README.md)
independently accounts for the112-byte text surplus using the four unmatched
body-size deltas. Other section sizes already agree, as do all2327 relocation
type/symbol records. Function permutations still prevent raw equality even if
the four sizes were repaired. The capture includes12168 zero bytes after its
last ELF structure; `capture.py` retained that exact ProgramData account suffix.
This is a deployment-allocation provenance question, not a compiler-padding fix.

[Three entrypoint/name/module controls](../repro/donation-relay/entrypoint-layout-controls/README.md)
retain488 normalized bodies but do not restore the original function order.
The ordinary Anchor entrypoint adds one raw-local match (142→143); the `contracts`
name and instruction-boundary controls have140 each. No variant is promoted.

The [deployment-allocation provenance packet](../repro/donation-relay/allocation-provenance/README.md)
now decodes all13 returned ProgramData transactions. Initial capacity546,944 plus
five explicit extensions (33,504,100,000,100,000,40,000,10,000) exactly explains
830,448 captured payload bytes. The last upgrade slot415422992 and later authority
change agree with captured metadata. This resolves the unexplained-size question;
it does not prove a matching Rust ELF or permit padding compiler output.


## Fees verified branch composition — 27 October 2026

The [new artifact-backed composition](../research/fees-composed-frontier188/README.md)
reproduces #188's exact binary hashes, then combines #176/#185 sharing contexts
and #172 social-PDA creation in four ordinary-source files. The result is
551/585 normalized counterparts, 404 unique pairs, 118 raw-local matches and
34 unmatched windows, with no lost matches. Six windows are gained over #188;
all 163 decoded Location-shaped uses agree. Fresh execution passes 17,331 suite
comparisons and 157 strict signed social-creation cases. The current inventory
is advanced to this composed artifact; selected checkpoints remain unchanged.
## Relay: all 492 normalized windows, but 18,623 bytes still differ — 27 October 2026

The [donation wrapper source proposal](../repro/donation-relay/donation-wrapper-source-proposal/README.md)
preserves two causal stages on the frozen public 488-window source. Ordinary
context declaration order and direct post-close event construction recover
native wrappers 92/93, reaching 490. Matching real context literal field order
then recovers token wrappers 94/95, reaching **492/492 normalized windows** with
no losses. Raw local matches rise **142→317**, including raw equality of all
four wrappers. Their 18 actual direct callees bind complete normalized bodies
and closed recursive direct-call shapes; the wrappers have no data or indirect
operands. This does not establish unique function correspondence or semantics.

All section lengths now match and candidate size 818,280 equals the original
meaningful ELF extent. **Whole byte identity is still false:** 18,623 common
positions differ (.text 18,453; .data.rel.ro 25; .dynsym 4; .rel.dyn 139; header 2),
and the capture has 12,168 allocation-tail bytes. The complete 19,863-byte .rodata
remains equal. Fresh static audit preserves all 359 data-pointer and 507
nonpointer-qword obligations, with five indirect-call-containing text targets.

Three exact 60-input source states, readable overrides/patches, nine tests and
independent optional full comparison are supplied without binaries, logs,
runtime cases or archived build/replay receipts. Local repeated builds and
finite signed replay are observations, not downloadable runtime proof. Default
compiler_executed=false and runtime_verified=false; protected relayer success
remains untested. Raw data semantics, addresses/order, indirect behavior and
whole-file identity remain open. Full identity of the four core programs is 0/4.


## Relay 492-window independent artifact verification — 27 October 2026

The [wrapper artifact](../repro/donation-relay/donation-wrapper-artifact-recovery/README.md)
independently reproduces #189's intermediate and final outputs. All 492 normalized
windows now match, including 317 raw-local bodies and all four donation wrappers.
The 18 actual wrapper callees, exact read-only data and positional data graph pass;
536 fresh signed replay records pass. The meaningful ELF still differs at 18,623
positions. The current inventory is advanced to the artifact-backed result,
without changing selected checkpoints or claiming whole-binary identity.
The fixed-order interleaving search was stopped after 29 completed negative
trials because #189 supplied the broader declaration/construction fix.

## Relay access-control layout recovery — 26 October 2026

The [ordinary-source access-control change](../repro/donation-relay/access-control-layout-source/README.md)
replaces six explicit first-body relayer checks with the equivalent upstream
Anchor attribute. It restores original windows194–204, including entrypoint,
allocator/panic routines and the five settlement entry functions, at their exact
addresses with full raw bodies equal. Their103 direct calls bind closed full
callee shapes. The full inventory stays492 normalized while raw-local matches
increase317→376 with59 gains and no losses. ELF/program/section headers and the
complete dynsym now match. Residual common-position bytes decrease18,623→9,398
(text9,324,data.rel.ro25,rel.dyn49); allocation-tail handling remains separate.

The [artifact packet](../repro/donation-relay/access-control-layout-artifact/README.md)
retains a reproduced492 baseline, two identical recovery builds from separate
source materializations and536 fresh signed offline replay records with no
mismatch. All359 positional data pointers and507 nonpointer qwords retain their
prior validation; five text targets containing indirect calls remain outside
semantic proof. This is a raw-layout gain, not whole-byte identity or selected
checkpoint promotion. Full captured-file equality remains false.

The [offline loader allocation recipe](../repro/donation-relay/offline-loader-allocation/README.md)
now executes real local signed buffer creation,910 writes and DeployWithMaxDataLen
using the historically derived830,448-byte capacity. It produces the unmodified
818,280-byte compiler ELF plus the12,168-byte loader-allocated zero tail, without
manual padding, add_program, set_account or RPC. Two fresh local runs reproduced
the same912-transaction receipt. Five static negative tests pass. This establishes
a loader-backed allocation route; original-payload equality remains false because
the ELF prefix still has9,398 differing positions.


## Relay raw-layout audit — 27 October 2026

Complete byte accounting attributes the 18,453 text differences to 15 normalized
body-permutation regions (17,991 bytes) and otherwise aligned direct-call operands
(462 bytes). Fourteen data pointers, two symbol values, 81 relocation-site values
and the entry address account for the other 170 differing bytes. Six compiled
source-identity controls preserve 492 normalized windows but do not reduce the
whole output difference; raw gains and losses are retained. The accepted artifact
and its 18,623-position residual remain unchanged.

## Relay: context naming recovers three raw bodies — 27 October 2026

The [context naming recovery](../repro/donation-relay/donate-context-raw-recovery/README.md)
continues the merged PR189 source with one ordinary Rust type definition and a
compatibility alias. `DonateContext` restores the context/BTreeSet cleanup order
and the shared worker's call displacements. Original windows 51, 52 and 112
(528, 488 and 10,248 bytes) become completely raw-equal at their original addresses.
Raw local matches rise **317 → 320**, all 492 normalized windows remain matched,
and no prior raw or normalized match is lost. All 60 direct-call sites in the
gained bodies retain closed normalized call shapes.

An independent baseline reproduces PR189 exactly. Root-clean and fresh
all-dependency candidate builds produce identical output pairs, and a fresh
local replay passes 536 signed records / 534 unique fixtures with zero differences.
The packet contains the one-file source patch, 60-input maps, isolated portable
build recipe, static remeasurement and six passing source/ELF tests, including a
changed-CALL negative control. Local receipt hashes are reported; full build and
runtime receipts remain local. Default verification does not compile or execute.

Only `.text` and `.rel.dyn` change from PR189. Whole-file common-position differences
fall 18,623 → 18,126; complete `.rodata` and the bounded positional data graph are
preserved. This is a reproducible naming/layout hypothesis, not proof of the
historical identifier, full data/indirect semantics or byte-identical completion.
Protected relayer settlement success remains untested. Prior evidence and selected
checkpoints are unchanged.

## Fees: boxed AdminCto ownership and typed self-program source — 27 October 2026

The [AdminCto source proposal](../research/fees-admin-cto-boxed-context-source-proposal/README.md)
changes exactly three declarations in one file on the pinned PR188 math+pack
combined source: box Global and SharingConfig and use a typed self-program field.
The handler and all other source inputs remain unchanged. Independent public
source hash checks, full 42-input materialization and thirteen source-only tests
pass; the readable patch reverses exactly to the pinned public parent.

Local development observed 545→547 normalized original windows with no losses:
parser 381352 (6,152 bytes) and generated wrapper 642848 (1,416 bytes), preserving
118 raw local matches. Local static audit checked 51/51 parser callees and 19
complete direct data objects; wrapper 8/9 callees and six direct data objects
hold, while the business callee remains unmatched. These native/static/runtime
observations are explicitly unpublished evidence, not claims established by the
packet's default source checks. The local root-clean repeat reused a verified
dependency/math cache, not a fresh all-dependency rebuild.

No binaries, logs, runtime cases, archived build/replay receipts or encoded
derivatives are included. Source tools report runtime_verified=false,
native_build_verified=false and whole_binary_identity_verified=false. The
business body and whole ELF/capture remain unequal; indirect/transitive data
and historical source provenance remain unproved. Prior checkpoints and sealed
evidence are not replaced.

## Exact Relay ELF and loader payload reproduction

The [explicit linker-layout packet](../repro/donation-relay/linked-elf-reproduction/README.md)
reproduces all 818,280 original meaningful ELF bytes and all 492 raw windows.
The layout is solved from complete normalized bodies, direct-call constraints
and code-pointer positions, then expressed through ordinary linker input-section
selectors. No original instructions, assembly, output patching or padding enter
the build. Both the first build and an isolated fresh dependency build produce
candidate `56d81ec64a0ba070d3d23f3c1547b31d659e85716dfa2198ec4b0ce6cd355333`
and symbols `07ab4ac487727385a3b5ec0d4bc1139e10f701c3fac2f95b88d89701a38ab9e1`.
Fresh bounded replay passes 536 records / 534 fixtures.

A fresh 912-transaction offline loader deployment writes this exact ELF and
allocates the history-derived capacity. Its full 830,448-byte payload equals
the capture (SHA-256 `367f07a62e3f74d358187d175cf3228848e81a56c781a9a75b9df7fed1268563`).
The extra 12,168 zeros come from the loader; compiler output remains 818,280 bytes.
ProgramData metadata/history and historical compiler/source provenance remain
unproved. Four core selected programs are still byte-unequal; no selection promotion
is made by this research packet.

PR #195 also independently reproduces the current Fees prefix correction:
552/585 normalized windows, 118 raw-local, 405 unique, 33 unmatched (205,216 bytes).
A fresh 17,331-case suite has zero mismatches. PR #196 preserves the separate
376-raw default-linker source result and supplies verified allocation history.


## Fees: pinned upstream union and Crank diagnostic source — 27 October 2026

The [source-only integration/diagnostic packet](../research/fees-upstream-crank-source-proposal/README.md)
preserves three exact 42-input stages: public PR188 math+pack 545, an independently
validated composition of PR169/172/176 at 550, and a three-expression Crank
correction retaining 550. All five integration gains belong to upstream authors;
this is not the latest frontier or a new discovery of those windows. Later
PR185/190/195 compositions, including the 552-window dataset, remain separate.

Fresh static remeasurement retains 118 raw counterparts throughout, preserves
all previously equal actual direct-callee shapes, and checks 161→163 equal
Location uses. The diagnostic adds the disabled/zero-amount messages and ordinary
overflow error conversion without changing dependencies. Its positional byte
distance regresses 456,100→466,083; whole identity remains false. Nine tests,
all exact materializations and independent three-output static comparisons pass.
Local two-build repetitions and finite runtime/application-log observations are
explicitly unpublished, not downloadable replay evidence. No artifacts, logs,
replay cases or archived receipt excerpts/derivatives are included; default
verification neither compiles nor executes and reports runtime_verified=false.
No selected checkpoint is replaced, and complete Crank semantics remain open.

## Fees public module visibility: 553 normalized windows

The [visibility packet](../research/fees-instruction-visibility/README.md) changes
a single declaration on the current 42-input source: `mod instructions;` becomes
`pub mod instructions;`. It restores original 650064's default-bump store and
complete 1,208-byte initialization wrapper, with all six callee bodies matching.
Two root builds reproduce candidate
`d85fe4eb037cd91b982eea55169faac1b342e6841ce440bee26c28b5f5617e36`.
The fresh 17,331-case suite passes. Coverage advances 552→553 normalized,
405→406 unique, 33→32 unmatched; raw-local remains 118, with no lost matches.
The visibility/source/branch controls for authorization at 234096 remain incomplete.
Whole-program equality and historical source visibility remain unproved.

## Relay: exact meaningful ELF from source plus inferred linker ordering — 27 October 2026

The [raw-ELF reconstruction](../repro/donation-relay/raw-elf-reconstruction/README.md)
compiles the exact public PR189 ordinary source with an explicitly nonhistorical,
object-qualified LLD input-section order. The unmodified stripped compiler ELF
has 818,280 bytes and SHA-256
`56d81ec64a0ba070d3d23f3c1547b31d659e85716dfa2198ec4b0ce6cd355333`:
**every byte equals the captured original's meaningful ELF extent**. Comparison
uses no address masks, normalization or binary patching. The ordering script
selects compiler-produced sections; it emits no machine bytes or integer addresses.
This is a reproducible reconstruction recipe, not the historical build recipe.

The full capture is 830,448 bytes with an additional 12,168 zero allocation bytes.
The compiler file is not claimed to equal that longer capture. A separate,
explicitly sized allocation-container helper leaves the ELF unchanged and can
reproduce the full captured image, checked independently by exact comparison.
Default verification checks only source packet integrity; explicit local inputs
are required to verify raw equality. No compiler, target or live service executes
in the verifier, and no binary/build/runtime receipt is published.

Local clean repeats, including an original-absent allowlisted filesystem build,
and finite offline replay are reported as unpublished observations. Source-only
negative tests cover metadata/mutation/symlink boundaries. All four core-program
identities remain unresolved (0/4); Relay is a separate dependency, not completion
of the entire repository. Prior evidence and selected checkpoints stay unchanged.


## Fees: included AdminCto business source recovery — 27 October 2026

The [included-handler source proposal](../research/fees-admin-cto-included-handler-source-proposal/README.md)
adds one complete normalized business body, original 127776 / 4,968 bytes, on the
exact public PR194 context-only source: pinned 547→548, no losses, raw 118.
Earlier boxed-account/typed-program gains belong to PR185/194 and are not claimed
again. Later public PR195's 552-window source is a separate baseline; this packet
does not claim a measured composition onto it.

Four ordinary source edits add the observed zero-admin guard, mutation/event
ordering and a real included block with authentic file/line spans. The local
event/include organization is inferred, not historical-source proof. Exact public
42-input provenance, reversible patch, full materialization and thirteen tests
pass independently. Local native audits report 20/20 business callees and eleven
complete direct objects; two root-clean outputs and finite offline regression
were verified locally, but their receipts are not included or downloadable proof.

No binaries, archives, runtime cases, logs or archived build/replay receipt
excerpts/derivatives are published. Default tools report native_build_verified,
runtime_verified and whole_binary_identity_verified all false. Indirect behavior,
transitive data and full raw ELF/capture identity remain unresolved. No selected
checkpoint or previous evidence is replaced.

## Current AdminCto integration: 554/585

[Independent integration of PR #200](../research/fees-admin-cto-current-integration/README.md)
recovers original 127776/4,968 bytes while preserving all prior current-source
matches. Two builds produce candidate
`ce8e040056b0645e59473306ad6b9fc8f1428461695d7fece8d0b276fc3f10d8`;
all 20 direct callee bodies and 17,331 fresh runtime cases pass. Current Fees
coverage is 554 normalized, 407 unique, 118 raw-local and 31 unmatched.

[CPI ownership controls](../research/fees-cpi-adapter-ownership-controls/README.md)
separately isolate four copy displacement bytes per legacy/V2 adapter. Thirteen
real controls add no complete matches; a local symbolic copy proof and 417
sharing-update cases support the limited observations. These artifacts remain
experimental and do not replace the current candidate.

## Fees: public module boundary restores the Buyback wrapper — 27 October 2026

The [one-line source proposal](../research/fees-buyback-module-source-proposal/README.md)
changes only `mod instructions;` to `pub mod instructions;` on public PR188's
exact 42-input math+pack source. This naturally retains the default bump store
at wrapper offset 104 and recovers original 650064 / 1,208 bytes: pinned
545→546 normalized windows, no losses, raw 118 unchanged. The later public552
source still leaves this wrapper unmatched; a combined frontier is not claimed.

Independent source checks preserve all other bytes and inputs, with thirteen
passing tests and exact full materialization. Local native audit binds six real
callee bodies and both complete direct objects. Two equal native builds and the
finite 17,331-case regression passed locally; their evidence remains unpublished.
The public source boundary is an inferred explanation, not historical provenance.

Only ordinary source, a reversible patch, public input hashes and source-only
tools are included. No binary, archive, log, runtime case or build/replay receipt
excerpt/derivative is published. Default native_build_verified, runtime_verified
and whole_binary_identity_verified remain false. Full raw ELF/capture identity,
indirect behavior and unrestricted transitive data remain open. No selected
checkpoint changes.

## Canonical exact Relay selected

The 60-input reconstructed Rust source is now installed at `programs/donation-relay`.
Independent review compiled it from that canonical path with a completely empty
target and no network: candidate and symbols match the exact ELF hashes. A fresh
real-loader run reproduces all captured payload bytes. The current 4,415-row
inventory now reflects this Relay selection, while the previous 23-input source
and metadata remain explicitly historical.

The successor guard preserves core107 and historical signature checks. Review
fixed a checkout-specific absolute-path check by validating one recorded source/
configuration root, read-only mounts and the same actual source hashes. Twelve
selection, portability and critical-code controls pass; the preserved signature
routes and exact Relay 536-record check pass. Historical source provenance,
ProgramData metadata/history and broader behavior remain outside byte equality.

## Fees: constant Pubkey boundary recovers the initializer parser — 27 October 2026

The [constant-admin source proposal](../research/fees-initialize-config-const-admin-source-proposal/README.md)
moves the unchanged admin Pubkey expression into a named constant, preserving
account types, error code, literal value, source line count and dependencies.
On exact public PR197's integrated550 source, this recovers original 295800 /
6,232 bytes: isolated 550→551 normalized, raw 118→142, no losses. The ordinary
constant boundary eliminates an unintended runtime base58-decoder call; its name
is not claimed historical. Newer combined frontiers remain separate experiments.

All 42 public input mappings and materialized bytes are independently verified;
thirteen source-only tests pass. Local static audit binds 42 actual callees,
14 complete direct objects and 163 decoded Location uses. Native outputs repeat
and finite 17,331-case regression passes locally, but authentic fixed-admin
initializer success is NOT exercised. These execution observations remain
unpublished, not evidence supplied by default source verification.

Positional byte differences worsen 456,100→466,938 despite raw-body gains; full
ELF/capture identity is false. No binary, archive, log, runtime case or archived
build/replay receipt derivative is included. Default native_build_verified,
runtime_verified and whole_binary_identity_verified are false. No selected
checkpoint or prior evidence changes.
## Fees: checked native Crank credit — 27 October 2026

The [Crank lamport-overflow proposal](../research/fees-crank-lamport-overflow/README.md)
replaces one native destination `+=` with Anchor's checked `add_lamports`.
Synthetic destination balances with insufficient `u64` headroom return the
original's `ArithmeticOverflow` instead of the reconstruction's panic and
`ProgramFailedToComplete`. This is an error-contract correction, not evidence
of economically reachable live balances, an exploit or fund loss.

The control preserves the current 553-window source, including the public
instruction-module recovery, and imports PR197's three diagnostic expressions
unchanged. Those prior recoveries are separately attributed. Fresh signed local
replay corrects 15 control mismatches across 76 cases, with matching donation
PDA/ATA rollback. The 17,331 existing suite comparisons and ten persistent
create/deposit/crank steps pass. A clean dependency rebuild repeats both output
hashes. Actual commands, source maps, compiler logs and runtime records are retained.

All 553 normalized/118 raw-local counterparts, 406 unique pairs, 163 equal
Location uses and 3,255 direct-edge observations remain. No new complete body
match is claimed; Crank and 31 other original windows remain unmatched.
Positional differing bytes increase 456,375→456,603 for the one-line fix, so
the observed behavior improvement is not a whole-binary-distance gain. Selected
checkpoints, original evidence, dependencies and existing harnesses are unchanged.
## Fees: complete legacy and V2 distribution helpers

The [distribution helper recovery](../repro/pump_fees/distribution-helper-recovery/README.md)
composes two reconstructed Rust helpers with the AdminCto-integrated source at
`3aa90d02`. The measured research candidate reaches **556/585 normalized windows,
409 unique structural pairs and 118 raw-local matches**, with 29 unmatched
windows. The selected checkpoint and pinned research inventory remain unchanged.

The complete 936-byte legacy and 1,224-byte V2 bodies match under the existing
call/relocation normalization. All 23 outgoing callee observations match, all
165 checked source locations remain equal, and no prior positive match is lost.
The changes follow original argument order and Rust ownership/evaluation order;
no emitted bytes are patched. Both original/candidate pairs pass all 417 fresh
sharing-update cases, exercising the legacy CPI in 90 cases and V2 CPI in 120.
Raw logs and compute are not fully equal, and whole-file identity remains open.
The packet retains all three builds, source snapshots, complete comparisons,
compressed receipts, and a verifier with mutation tests.

## Fees 556 inventory integration

The verified PR206 candidate is now the current Fees research inventory: 556/585
normalized windows, 409 unique structural pairs, 118 raw-local, and 29 unmatched
windows spanning 196,880 original instruction bytes. Fresh execution of all
17,331 suite comparisons passes. Call-graph refinement recomputes 69 additional
pairs for 478 attributed correspondences, leaving 78 duplicate windows unassigned.
The core selected checkpoint remains unchanged; this is a research inventory
update, not whole-program identity or historical-source proof.
## Fees: typed Relay donation encoder

The [Relay encoder recovery](../repro/pump_fees/relay-donation-encoder/README.md)
adds the complete 1,400-byte original function at 270136 through an ordinary
borrowed Anchor-serializable argument type and a public encoder. It has a real
incoming call from the reconstructed Crank handler. The measured research
candidate advances from 556 to **557/585 normalized windows**, 410 unique
structural pairs and 118 raw matches, with all prior matches and all 165 checked
source locations preserved. The original calling handler remains unmatched.

Both candidates pass 357 fresh donation-Crank cases, including 159 cases that
reach the captured Relay program. The verifier checks the retained 556 parent
source/artifact hashes directly, without requiring its Git object in a shallow
checkout. Whole-ELF equality, full raw logs/compute and the selected checkpoint
remain unchanged; this is an additional bounded research result.


## Fees: six-window source integration on pinned public552 — 27 October 2026

The [source-only integration](../research/fees-six-window-source-integration/README.md)
composes seven ordinary source changes on exact public PR195 `origins`, with 43
inputs and unchanged packages/lock/features. It retains all 552 normalized and
118 raw matches, reaching **558 normalized / 143 raw / 411 unique pairs**.
Six complete gains are 127776, 270136, 271536, 276672, 295800 and 650064. Attribution
is explicit: PR200 Admin body, SDK's three typed Relay CPI helpers, PR204
constant-admin parser and PR202 Buyback wrapper. PR197 diagnostics, independently
measured native privileges and checked lamport methods also compose here.
The typed and native-privilege controls were parallel, not a sequential chain;
the checked arithmetic correction fixes an independently discovered overflow
boundary also published by PR205, which is explicitly credited.

All 42 public parent input bytes were independently checked, exact 43-input
materialization and thirteen tests pass, and a fresh opt-in static reader checks
83 actual new direct callees plus all 3,233 previously equal obligations and 165
value-equal Location uses. Thirteen actual callee edges remain unequal. Raw
section inventories and all full output hashes are bound; 446,635 common bytes
still differ and the candidate meaningful ELF is 784 bytes too long. Whole
binary identity remains false.

Repeated native builds and finite runtime/application-log/boundary observations
passed locally but their receipts are not included. Authentic fixed-admin success,
exhaustive semantics and full runtime log/CU equality are not claimed. Later
PR201 native-only lifetime work and PR206 distribution-helper recovery are
explicitly not in this pinned source. Only
ordinary source, public provenance, readable patches and freshly remeasured
static metadata are published; no binary/archive, log, runtime fixture or
archived build/replay receipt derivative. Default native/runtime/whole identity
verification stays false. No selected checkpoint changes.

## Pump AMM: buyback split helper and recorded source locations

The [buyback helper recovery](../repro/pump_amm/buyback-helper-recovery/README.md)
extracts the complete 328-byte original function at 412888 through ordinary
Rust method ownership, public visibility and an early return. The measured
candidate reaches **489 complete normalized windows**, including 93 raw matches,
with 296 unmatched windows and no previous match lost. Both referenced panic
messages and source-location triples match; all 51 prior location positives
remain, giving 53. Raw pointer-bearing records and the full ELF still differ.

Baseline and final candidate each pass 1,011 legacy-buy cases and 575 legacy-sell
cases, with 3,172 signed transactions per build. The source layout and root-only
path remap are documented reconstructed build inputs, not historical provenance.
The retained materializer restores its builder's transitive Python imports, and
the verifier checks ordered complete callees, source, artifacts and signatures.
The selected checkpoint remains unchanged.

## Independently compiled current558 source

The [558 integration](../research/fees-current-558-integration/README.md) closes
encoder 270136 and parser 295800 on the 556 base and preserves every previous
match. It adds 24 raw-local counterparts:558 normalized,142 raw-local,411 unique,
27 unmatched;189,248 original instruction bytes remain unmatched. Two builds
agree. All 165 Locations and 3,284 prior positive direct-call observations survive,
with 3,336 equal observations in the new build. All 17,331 suite and 76 boundary
cases pass. Strict304-case Crank observations agree except explicit compute
lines in every case; raw runtime equivalence is not claimed.
## Mayhem: shared error namespace and typed Sell CPI

The [shared-error and typed-CPI recovery](../repro/mayhem/shared-errors-typed-cpi/README.md)
reconstructs six complete normalized helpers from Rust: three error helpers and
three generated Sell CPI helpers. A fourth newly examined dependency already
matched the baseline and is recorded as an admission result, not a source gain.
All 177 prior admitted matches are retained. The expanded examined scope is
191 admitted functions, 184 matching and seven still unmatched, with 250
semantically opaque windows. All 58 literal raw windows remain equal; that
includes 46 admitted and 12 still-opaque windows.

Original data tables and bounded dispatch prove the twenty error names, numbers
and messages. The typed CPI retains fourteen core accounts and two remaining
accounts, with independently checked ordering and flags. Legacy Sell passes
396 cases / 792 signed transactions, and the Burn regression adds 12 signed
transactions. Four panic/overflow log differences remain. Full handlers and the
whole ELF are still unequal, and no canonical source is promoted by this packet.

## Fees: complete exotic-fee body on the pinned 558 union — 27 October 2026

The [source-only exotic integration](../research/fees-exotic-body-source-integration/README.md)
changes only `lib.rs` on exact PR209: borrowed resize-helper inputs and ordinary
non-cloned event emission recover the complete 5,520-byte body at original 88552.
The frozen result reaches **559 normalized / 143 raw / 412 unique pairs**, with
no prior loss; 26 original windows remain unmatched. All 43 input hashes and the
reversible one-file source patch are checked, with unchanged dependencies/features.

Fresh optional static remeasurement checks all 21 actual direct callees, abort,
incoming wrapper binding and all four complete direct object values. It preserves
3,319 earlier equal callee obligations and 165 Locations, reaching 166 matched
Location uses; 12 actual edges remain unequal. No transitive/indirect/runtime
closure is inferred. Raw positional differences worsen 446,635 to 448,155,
despite the complete-window gain; meaningful ELF size remains 640 bytes too long.

Default verification, thirteen source tests and full materialization pass. Two
exact native builds and finite 17,331-case/18-suite plus boundary checks passed
locally, but no build/replay receipts, fixtures, logs, binaries or derivatives are
published. Source/static verification alone reports runtime/build/whole identity
false. Authentic fixed-admin success and exhaustive runtime log/CU identity remain
unproven. All four core whole identities remain unresolved; no checkpoint changes.
## Fees: complete remaining-account preprocessing

The [preprocessing recovery](../repro/pump_fees/remaining-preprocess-recovery/README.md)
reconstructs the complete 2,520-byte original function at 231576 using the
observed public module, owned key value and borrowed-result lifetime. The
cumulative research candidate reaches **558/585 normalized windows**, 411
unique pairs and 118 raw matches. Every previous match is retained; 166 checked
source locations agree, with 17 additional matching callee observations.

The ordinary 417-case regression passes. Another 24 cases explicitly exercise
the completed-curve branch with boundary account lengths and ownership/key
variants. All compared outcomes and state pass; two incomplete-curve controls
retain old downstream diagnostic differences. Whole-ELF equality remains open.
No selected checkpoint is changed.

## Mayhem: typed GlobalParams layout and complete codecs

The [GlobalParams recovery](../repro/mayhem/global-params-layout-recovery/README.md)
replaces opaque byte groups with transport-proven fields. The original serializer
independently maps all 254 serialized bytes and 26 native fields. The shared
trade-validation method and all three GlobalParams codecs now have complete
normalized matches, preserving the six preceding helper gains and all 58 raw
windows. Including the explicitly examined but unmatched quote-aware validator,
the admitted scope is 196 functions, 188 matching and eight unmatched, with
245 still semantically opaque. This does not turn opaque raw equality into a
claim of analyzed behavior.

The candidate passes 2,868 independently verified signed transactions: 1,032
admin transport/update/reset cases (initializers excluded), 396 Sell cases and
the three-family Burn regression. Independent checks reconstruct complete
expected account bytes for 624 successful admin cases. Four Sell log differences
remain, and no full-handler or whole-ELF equality is claimed.

## Mayhem priority and quote-validator controls

A private source build independently reproduces the latest GlobalParams artifact and symbols. Seven ordinary Rust variants preserve 188 examined matches and 58 raw-local windows, but the 1,296-byte O0095 body remains unmatched. Loading expiry before Clock recovers the original register/spill prefix; threshold and error block order remain open. These negative controls and their complete source/build evidence are retained in [the control packet](../research/mayhem-quote-validator-controls/README.md). The [Mayhem plan](MAYHEM-RECONSTRUCTION-PLAN.md) is now the active reconstruction priority.

## Fees: legacy social-claim semantics on the pinned 559 source — 27 October 2026

The [source-only Social proposal](../research/fees-social-claim-semantics-source-proposal/README.md)
changes only the legacy `social.rs` body and its root module visibility on exact
PR212's 43-input source. It restores saturated-deadline admission, four complete
diagnostics, ordinary error conversion, saturating transfers and observed borrow/
event ownership. The V2 handler, account declarations and other 41 inputs stay
unchanged. Historical source topology is inferred, not proven.

This is semantic progress, **not a complete-window gain**: all 559 normalized /
143 raw counterparts and 166 Location uses remain, but original 132744's
4,536-byte body is still unequal because of diagnostic block/branch placement.
All 26 ordered actual callees and eight complete direct objects were checked
locally without masking differing offsets. Positional differences worsen from
448,155 to 453,541; the candidate is 80 bytes shorter than the meaningful original.

Fresh local comparison on BOTH actual559 control and proposal covers 348 cases,
fixing one state/event mismatch and 144 application-log mismatches. Two exact
native builds, 17,331-case/18-suite regression and existing arithmetic boundaries
also pass locally. No execution receipts, fixture/log data or derivatives are
published; these observations are not downloadable runtime proof. Finite coverage
is not exhaustive semantics, full log/CU equality or authentic fixed-admin success.

Default source verification, thirteen tests and exact 43-input materialization
pass. The nine plain-text files contain only ordinary source, reversible patch,
public provenance and source-only tools; runtime/native/whole identity flags stay
false. All four core whole identities remain unresolved; no checkpoint changes.

## Mayhem interval-overflow location recovered

[Compiled source-location recovery](../research/mayhem-interval-location-recovery/README.md) corrects exactly one ELF data byte: candidate offset 578012 changes from 27 to 32, matching original state.rs 562:32. All code bytes remain identical. Two clean root builds agree; all 396 Sell comparisons and 792 signed transactions verify. Known non-compute log differences decrease from four to three. Five [further validator controls](../research/mayhem-quote-validator-followups/README.md) preserve all 188 matches but do not close O0095.

## Mayhem Sell arithmetic and source-origin recovery

The [new source composition](../research/mayhem-sell-origin-recovery/README.md) restores the Result-based arithmetic failure and original state.rs locations. Two root builds agree. All 396 Sell cases match on the checked fields and every log line except explicit compute consumption; all 1,032 admin cases and three sequential Burn families pass. Independent verification covers 2,868 signatures and complete expected account bytes for 624 admin successes. No complete-function gain is counted: the current research remains 188/196 examined matches, eight admitted gaps and 245 opaque windows.


## Fees: two sharing parsers and attributed CPI helper integration — 27 October 2026

The [source-only sharing integration](../research/fees-sharing-parser-source-integration/README.md)
changes one ordinary file on exact PR215's 43-input Social-corrected source.
It recovers complete legacy/V2 account parsers at 484816 / 16,112 bytes and
502096 / 16,880 bytes through the native ATA constants and explicit quote-mint
owner constraint. Upstream PR206 owns the composed 235304 / 936-byte and
236240 / 1,224-byte distribution helpers; they are not claimed as new discoveries.
Later PR213 preprocessing is explicitly not included in this frozen source.
Concurrent PR216 reaches the same 563 total with different coverage (preprocessing
and new adapter204080 rather than these parsers); its overlapping PR206 helpers
are credited, not claimed as fresh discoveries. Its new adapter is not included.

Fresh measurement reaches **563 normalized / 143 raw / 416 unique pairs**, with
no loss from actual559. All 252 actual direct callees from the four bodies match;
all 3,341 prior equal obligations and 166 Location uses survive. Ten actual edges
still target unequal complete bodies. Local semantic-extent audits also confirm
47 and 45 parser objects plus the helpers' no-direct-object boundary, without
claiming transitive data or exhaustive behavior.

Raw positional differences worsen 453,541 to 464,073; the meaningful ELF remains
1,432 bytes too long. Default verification, thirteen tests, exact materialization
and fresh opt-in static comparison pass. Two exact root-clean builds and fresh local 17,331-case/18-suite regression pass,
as do 348 Social checks, 357 covered Crank log cases and both native boundaries.
Eight quote-owner matrix cases repair four failures in the actual parent. No runtime/build receipts,
fixtures, logs, binaries or derivatives are included; default execution/identity
flags remain false. All four core whole identities remain unresolved and no
selected checkpoint changes.

## Fees: V2 native social and buyback payout arithmetic — 27 October 2026

The [native payout correction](../research/fees-native-payout-arithmetic/README.md)
changes three expressions on exact PR215's 43-input source. Legacy social claim
stays byte-identical to that merged work. V2 native credit now saturates like the
original; overflowing transactions still fail `UnbalancedInstruction` and roll
back, retaining the original clamped event/return value. Buyback returns
`ArithmeticOverflow` instead of panicking. V2's executable-before-zero no-op
order and both diagnostics are restored.

Fresh normally signed comparison corrects 38 mismatches in 119 focused cases:
30 overflow and eight native no-op cases. Legacy cases are preservation controls.
The fresh proposal passes 17,331 existing comparisons across 18 suites. The
all-dependency-clean baseline reproduces both published PR215 hashes, and a
separate all-dependency-clean proposal rebuild reproduces both new hashes.
Commands, logs, artifacts and full comparisons are retained in the packet.

All 559 normalized/143 raw-local counterparts, 412 unique pairs, 166 equal
Location uses and 3,353 direct-edge observations remain. No complete original
body is newly matched; 26 windows remain unmatched. Positional differences
worsen 453,541→466,189 and whole-binary equality remains false. Synthetic extreme
balances do not establish mainnet reachability or an exploit; failed events are
not successful payments. Originals, prior evidence and selected sources remain
unchanged. Earlier 554-based experiments were superseded after PR215 merged and
are excluded from these acceptance counts.

## Mayhem deployed trade-wrapper attribution

The [new audit and source controls](../research/mayhem-trade-wrapper-attribution/README.md)
map all six trade bodies from actual wrapper log literals and direct calls.
O0092/O0093 belong to PumpSwap Buy/Sell rather than legacy Buy/Sell. Two actual
15-input builds preserve all 188 examined normalized matches and 58 raw-local
matches; neither quote helper is a full counterpart. The branch/error control
passes 1,257 fresh BuyPumpSwap comparisons across three quote families with
2,514 verified signatures. Token-2022 fixtures all reject. Full handlers, eight
admitted body gaps, opaque scope and whole-file equality remain unresolved.

## Mayhem AMM source origins and expanded audit scope

[Shared state/origin recovery](../research/mayhem-amm-source-origins/README.md)
restores AMM validation/risk diagnostics and the balance-delta adapter's original
source sites. All 1,653 fresh trade comparisons have exact logs after removing
only compute-consumption lines. The full packet verifies 5,382 signatures,
1,032 admin cases with 624 independently reconstructed account results, and three
Burn families. Two root builds reproduce the 625,488-byte candidate.

No new whole-body match is claimed. Explicitly admitting O0090 and O0092 expands
the ledger to 198 examined / 188 matched / ten unmatched / 243 opaque, retaining
all 58 all-inventory raw-local counterparts. The ten examined extents total
101,480 bytes; opaque code and whole-ELF obligations are additional work.

## Full Mayhem window accounting

The [complete static scan](../research/mayhem-full-window-audit/README.md) now
reports every original window rather than restricting its headline to the
source-interpreted subset. Existing artifacts have 58 raw-local matches,
269 normalized-only matches and 114 unmatched windows (495,936 bytes). The
139 additional structural matches were previously classified as opaque, not
newly reconstructed. All 441 windows cover text without gaps; 93 counterpart
mappings remain ambiguous. Three retained root MIR controls fail to improve the
accounting or quote helper and do not replace the existing candidate.

## Shallow-checkout Relay source verification repair

The linked-ELF verifier now reconstructs the same three exact 60-input maps from checked-in public source files authenticated by the unchanged historical source manifest. It no longer requires old Git commit objects merely to read those files. A tiny local depth-one clone reproduces the missing-history failure; ten source-only regression tests pass, including changed/missing input, immutable manifest, unsafe path and symlink rejection. No Git/network fallback is permitted.

The historical wrapper package, compiler source hashes, original and reconstructed ELF bytes, linker recipe, archived builds and runtime evidence remain unchanged. Only the linked verifier and its explicit canonical/status dependency pins change. This fixes CI source retrieval, not a new binary or runtime claim; the complete archived-ELF/portable CI route is checked separately. See `repro/donation-relay/linked-elf-reproduction/SOURCE-CHECKOUT.md`.

## Mayhem native Program parser recovery: fourteen full bodies

[Native Program recovery](../research/mayhem-native-program-recovery/README.md)
adds 14 strict normalized matches and preserves the preceding 327. Restoring the
unconditional program-ID check in an authenticated Anchor source copy permits
standard Program account syntax and reproduces the original generated parser
layout. All six trade account parsers and Burn's parser now match; their business
handlers remain separate work. Five new bodies retain a differing direct-callee
shape. No raw-local gain or whole-ELF equality is claimed.

The two builds reproduce the same 625,904-byte candidate. All 6,636 trade cases,
1,032 admin cases and three Burn families pass; the verifier checks 15,348
signatures and 624 complete admin account results. The full static remainder is
100 windows / 350,216 bytes, versus 114 / 495,936 before this source recovery.

## SweepBuyback source-coordinate and arithmetic-order proposal

A separately measured three-file Rust delta on the exact PR212 559-window source restores original admission diagnostics, a real state claim method/source locations, borrowed balance access, transfer-before-counter ordering and source-free counter errors. PR219 independently published the same destination `add_lamports` correction and is explicitly credited; the other changes and all reported comparisons remain scoped to the pinned PR212 parent, not incremental claims over current upstream.

The default source-only verifier and 13 tests pass; all 43 materialized input hashes match the frozen native-tested source. Independent local static remeasurement retains 559/585 normalized windows, 143 raw local counterparts and 166 equal Locations. The actual unmatched body is 6,984 versus original 6,960 bytes; its matched-wrapper binding, multiset of 37 actual callee shapes and 17 direct used operands/descriptors were checked, not a whole-body/CFG proof. Common-position differences worsen 448,155 → 455,540.

Two identical local native builds and the finite 17,331-case regression passed; the exact candidate repairs 275 prior application-log mismatches among 1,249 Buyback cases plus separately checked arithmetic boundaries. These are explicitly unpublished local observations, not downloadable execution proof. The packet contains only ordinary source, reversible patch, full provenance/maps and static source tools; no artifact or build/runtime receipt. See `research/fees-sweep-buyback-source-proposal/README.md`. Whole core identity remains unresolved and no selected checkpoint changes.
## Mayhem: restore BuyV2's shared trade-validator call — 27 October 2026

The [BuyV2 shared-validation proposal](../research/mayhem-buy-v2-shared-validation/README.md)
replaces one duplicated pause/Clock/rate block with the existing O0094 validator.
Only BuyV2 source changes on the pinned 15-input Sell-origin baseline. The fully
matched O0189 wrapper binds original O0083 to the actual candidate handler. The
original calls O0094 once, the control does not, and the proposal restores that
edge. The validator's complete 1,192-byte body and nine ordered immediate callee
bodies match under unchanged normalization. No new complete body match is claimed.

Fresh focused replay corrects 12 non-compute log differences in 24 signed cases.
Both actual Linux control and proposal also pass 613 existing BuyV2 cases for
each of native, legacy-token and Token-2022 quotes: 1,839 comparisons per build.
Independent verification checks 7,356 signature entries, successful state/event/CPI
results and failed-transaction rollback. The broader non-compute log differences
decrease 130→118; raw compute differences and all remaining diagnostics stay explicit.

All 188 prior examined matches and the Linux control's 63 raw-local windows remain.
The latter already includes five platform-related raw matches beyond the Darwin
parent and is not credited to this source delta. Linux does not reproduce the
Darwin parent's whole hash. A separate all-dependency-clean build and the portable
builder reproduce both proposal ELF hashes. BuyV2's complete body, full call/data
closure, whole-ELF identity and later 16-input AMM composition remain unresolved.
Originals, existing evidence and selected sources/checkpoints remain unchanged.

## Native Program + BuyV2 shared-validator composition

The [new composition](../research/mayhem-native-buy-v2-validation/README.md)
verifies PR226's call restoration on the newer native Program source. Its two
root builds are identical and preserve all 341 full-window matches. All 1,839
fresh BuyV2 comparisons pass; 3,678 new signatures and 3,678 parent signature
entries verify. Non-compute log differences decrease from 130 to 118. This is a
restored call edge and diagnostic improvement, not a new complete body or ELF
match; other parent runtime observations are not rebound to the new artifact.


## Current-public Social V2 admission and Source-coordinate proposal

Two ordinary source overrides on the exact 43-input public PR222 source restore V2 feature/deadline/executable admission, zero-amount diagnostics, saturating operators and four actual associated-token helper Source coordinates. PR219's native saturation/messages and PR220/222's existing recoveries are preserved and credited. Legacy Social code and prior helper bodies/physical ranges are unchanged. This isolated source retains 570 normalized / 143 raw local counterparts and 168 equal Locations; both V2 business and ATA helper bodies remain unmatched. Later finish-helper/Sweep integrations are not composed here.

All 43 public compressed source blobs and expanded hashes were authenticated; exact materialization, default verification and 15 tests pass. Two exact-public source builds repeat both full ELF hashes and match the separately executed source-order control byte-for-byte. The finite 640-case current-parent comparison repairs three outcomes and 283 application-log mismatches; 17,331 regression cases pass their defined predicates. This is explicitly full-byte-linked execution evidence, not a new source-path replay. Eight executable-recipient snapshots omit executable-account bytes, and 78 known sharing application-log mismatches remain. All receipts/case data stay local.

Fresh static checks bind the real wrapper, three early callees, four diagnostics/four Source records, plus 729 decoded deadline and 343 saturation combinations—not whole CFG/behavior closure. Raw differing positions worsen 462,922 → 470,275. The nine-file source-only packet has no binary/archive or build/runtime receipt derivative; default native/runtime/whole identity claims remain false. See `research/fees-social-v2-current-source-proposal/README.md`.


## Source-only legacy preparation recovery on exact public PR227

The 44-input public PR227 source plus two ordinary source changes recovers the complete 5,008-byte preparation body at original 199072: actually measured 573 → 574 / 585 normalized counterparts, zero losses, 143 raw local counterparts unchanged and 427 unique pairs. This is a pinned-source result, not a sum added to the moving main frontier. PR225/PR227 finishing bodies are preserved and credited; later PR229 Sweep, PR231 V2 semantics and PR232 Social likelihood changes are not composed here.

`research/fees-legacy-preparation-source-proposal/` contains only ordinary source overrides, exact public-source hashes, a reversible patch and source/static tools. All 44 public stored/source hashes are authenticated. Sixteen source tests and exact full materialization pass. The optional pinned-parser reader freshly checks full inventories, 15 actual complete callee shapes, all 13 explicitly bounded direct operands/inferred tables, the actual incoming payout edge and six in-memory rejection controls. All 3,765 prior positive callee obligations and 171 Locations survive; 174 Locations now match. Nine actual edges still target unequal bodies; no recursive/all-data/whole-identity claim is made.

Two native root-clean outputs repeat exactly and finite local 17,331-case regressions pass for parent and candidate. Current-parent sharing logs repair six mismatches, but 27 inherited sharing-log mismatches remain. Eight filtered-holder fixtures check seven downstream distribution events and the all-filtered CPI skip. The separate 640-case V2 scope still has three outcome and 283 application-log differences because PR231 is not composed. Those executions and receipts remain local, not downloadable proof; default build/runtime verification remains false.

Raw positional differences worsen 462,972 → 463,015; the compiler ELF remains 5,104 bytes too long. No binary/archive, build/runtime receipt, transaction/log fixture or derivative is published. Whole Fees ELF/capture identity and canonical selected checkpoints remain unchanged.
