# Pump CTO borrowing and used CPI flow

This historical673 research overlay restores original-backed token-account
borrows, the used holder payout boundary, and program-first CPI construction.
Final source: [`used-flow/source/admin_cto.rs`](used-flow/source/admin_cto.rs),
SHA256 `5203d20c2e63be7337204491588e0ec69808f8ddd39d96b8b5fa1964d6ec201d`.

The final native image passes380 existing case records with777 actual signed
executions and1,550 verified signature fields. Full ordered logs, including Source
diagnostics, and structured outcomes agree with the original. Only exact standard
compute-consumption lines are excluded.

**No window gain or canonical promotion:** the complete1,035-window census
remains1,019 normalized /188 raw, with zero gains/losses. The original27,400B
caller still differs from the final18,464B caller. This packet changes no
maintained program source, selected executable or global count.

## Historical cohort

The source/control input is immutable revision
`1285b5e9e3a29c1e2cf32246d6046035e5d66fad`, also unchanged at publication base
`a18e1e89b59bf9d734955550c92f321c97c95e62`. Its native673 control is `199fd737…`
(symbols `49df399b…`), and its CTO source is `6353b1f7…`.

Main subsequently advanced to `f57bbf0dd856b101acd02c242cb5c4a56bf276b1`, selecting
the separate per-hop734 composition (`c0e29…` / `dd73…`). These retained builds
and runtime receipts do **not** qualify that newer composition with this overlay.
A future combination needs its own actual build, complete census and runtime.

## Recovered used operations

Five original token-reader arguments directly borrow the context `AccountInfo`.
The historical673 source instead cloned them into temporaries. Stage1 restores
those borrows and removes two outer emptiness checks already performed by
`token_frozen`. Exact original/selected instruction witnesses remain in
[borrow-proof.json](evidence/borrow-proof.json).

The final stage restores the genuine holder payout in the caller: create its ATA,
then transfer the existing amount using the existing creator-vault authority and
three-element signer seed slice. The historical source introduced a `pay_token`
boundary and copied its owner once in the caller and again in the helper. The
overlay uses the same context owner directly, with one copy, and deletes the
obsolete helper. It does not flip an inlining attribute or add a forced-inline
replacement; the removed whole declaration carried its old `inline(never)`.

Original sharing, pool and collect-coin sequences clone the outer CPI program
before their account fields. The final source creates a genuine used
`cpi_program` first in those three contexts. Account values, field order, business
guards, owner/signer validation, amount/seeds and CPI/error ordering are preserved
as documented in the exact operand evidence.

| Measurement | Original | Historical673 | Stage1 `f4a2bb7d` | Final `5203d20c` |
| --- | ---: | ---: | ---: | ---: |
| CTO body bytes | 27,400 | 19,632 | 18,104 | 18,464 |
| Defined direct calls | 154 | 177 | 170 | 178 |
| Direct caller `AccountInfo::clone` calls | 33 | 53 | 48 | 54 |
| Inline AccountInfo copies in this flow | 21 | 7 in `pay_token` | 7 in `pay_token` | 0 |
| Total static AccountInfo copy sites | 54 | 60 | 55 | 54 |
| Outer caller `data_is_empty` calls | 6 | 8 | 6 | 6 |

Each caller also has three relocated external calls. The148 shared attributed
callee occurrences in the initial ledger were never the selected177-call total.
Original inline Rc-overflow `abort` paths are not missing business guards.

The final54 copies remain direct calls; the original has33 direct plus21 inline.
That distribution is an explicit residual. `memcmp` remains15 calls versus14
original; final `memcpy`8 includes the moved holder-ATA account array copy versus6
original. Counts alone establish no semantic equivalence.

## Actual compiler, source and static bindings

| Stage | Actual stripped ELF SHA256 | Actual symbol ELF SHA256 |
| --- | --- | --- |
| Stage1 | `d537faf5907c594eeef6f3706d87e300e6f01509243b5dcf28b018f3c90a64c6` | `daa2772d4745d8488b357c6c1c088fadc77bf31d341c59f5b50c4706d7b54c78` |
| Final | `df40382896c913ba02f064a993424daec707abe7ea95895cc821061cc7a82684` | `388fa73431d68cb0a89e9c939f1645510abd844652f4272ef1a841a0ec60bbe0` |

The unchanged [control40791064153](https://github.com/shawkkkkk/pumpfun-source/actions/runs/40791064153)
passed before [stage1 run40792775552](https://github.com/shawkkkkk/pumpfun-source/actions/runs/40792775552)
and the single final [run40794982049](https://github.com/shawkkkkk/pumpfun-source/actions/runs/40794982049).
Both use the historical673 empty-target native macOS v1.44 recipe and authenticated
Linux SBPF target libraries. Both local crates actually compile. All65 primary
inputs differ from historical canonical in this one file; each archive verifies
all66 actual workspace compiler inputs. No flag, SDK or layout sweep was used.

The [canonical-to-final patch](used-flow/source/canonical-to-proposal.patch) and
[immediate stage1-to-final patch](used-flow/source/proposal.patch) are distinct.
All stage1 source/artifacts/18-case receipts remain unchanged at their original
paths; [F4-STAGE.md](F4-STAGE.md) preserves that stage's narrative and limits.

The [independent actual audit](used-flow/independent-audit/SUMMARY.json) matches
all108 Rc source-pointer expressions for54 original/final copies after only
constant pointer-add folding. It confirms the single holder-owner copy and all
three program-first groups. Following actual paired call edges through depth2
matches21 payout pairs and12 raw-helper pairs. This bounded audit does not close
every caller edge, pointee, data or opaque contract.

## Source positions and finite runtime

The source inherits explicitly disclosed engineered blank-line positioning from
earlier reconstruction. This work adds no padding. All17 explicit error/require/
unwrap token positions remain fixed. Removing the obsolete helper naturally moves
`token_raw_amount` from775 to772. Its actual448B body is byte-identical to stage1
except four real CALL displacements, has zero relocations, and its sole observed
direct-callee Location remains `src/lib.rs:102:19`. No emitted775→772 Location
change was found. The independent parent recognizer's16 Source records are a
heuristic check, not exhaustive Source proof.

| Final actual suite | Case records | Signed executions | Verified signature fields |
| --- | ---: | ---: | ---: |
| Existing broad admin CTO | 363 | 726 | 1,448 |
| Existing strict Source records | 5 | 15 | 30 |
| Existing shared holder | 12 | 36 | 72 |
| Total | 380 | 777 | 1,550 |

These are case records, with overlapping inputs, not380 unique independent
branches. The original broad corpus reaches169 successful cases,162 sharing CPI
occurrences,177 pool CPIs,10 collect-coin CPIs,9 creator-fee transfer CPIs and two
genuine `TransferChecked`/ATA initialization flows. Source/shared suites retain
their original negative witnesses. Actual captured dependencies execute with
signed outer transactions and nonsigner pool authorities at the transaction
boundary. No privileged signer or owner bypass is added.

Executed controllers, unchanged input/tool hashes, explicit historical path
adaptations and raw reports remain under [used-flow](used-flow/). The shared
suite preserves its existing transparent holder-key fixture input adapter; it
does not bypass validation. Broad JSON is archived losslessly as gzip with its
exact original output hash. No filename, line, Source or message substitution is
used. Stage1's18 fresh common-wallet cases remain separate prior-stage evidence;
their results were not transferred to the final ELF.

## Verification and limits

From a complete checkout with the repository's Python dependencies:

```sh
python3 -B scripts/verify_evidence.py
python3 -B scripts/test_tooling.py
python3 -B research/pump-cto-direct-borrows-20261029/verify_measurement.py
python3 -B research/pump-cto-direct-borrows-20261029/used-flow/verify.py
python3 -B research/pump-cto-direct-borrows-20261029/used-flow/test_runtime_controls.py
```

The offline verifiers check actual source/archive/image bindings, complete native
manifests, call counts, official full-window census, real signatures, captured
loader observations and strict outputs. They do not invoke a compiler or VM.
Exact executed replay scripts retain physical paths; rebuilding that environment
requires the recorded filesystem path adaptations, unchanged tools/captures and
explicitly selected actual images.

Common capture9/9 and comparator6/6 pass. Both measurement verifiers pass normally
and under `-O`; original source/witness3 controls and final strict runtime4 controls
pass. Commands and outputs remain under the corresponding `validation/` folders.

Full44-suite replay, full caller byte/CFG identity, whole meaningful ELF identity,
all runtime branches, unique original source/private build provenance and security
acceptance remain unresolved. Stopped incentive domains remain excluded. No global
completion count changes.

Attribution: creation-worker initial callee evidence was independently decoded
before the borrow correction. The CI worker performed genuine control/candidate
builds; root produced official complete-window deltas. The AMM worker independently
audited actual copy operands, call edges and Locations. Their evidence and limits
are preserved; those independent contributions are not claimed as solely this
worker's work.
