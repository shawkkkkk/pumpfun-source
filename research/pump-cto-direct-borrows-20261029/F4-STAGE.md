# Pump CTO direct-borrow source measurement

**Compiled research overlay; no window gain.** This packet restores five direct `AccountInfo`
borrows and removes two redundant outer emptiness checks in the used
`admin_cto::execute` path. It does not replace maintained program source, assign
an existing executable to new source. A fresh native build, full no-loss census
and the finite18 common-wallet replay are retained below; shared-holder runtime
qualification remains open.

The original `0x22a10` body is 27,400 bytes. The selected `0x2fd30` body is
19,632 bytes. They contain **154 versus 177 defined direct calls**, plus three
relocated external calls each. The 148 shared attributed callee occurrences are
not the selected body's total call count. External `call -1` instructions are
resolved through `.rel.dyn` and `.dynsym`, including the original inline Rc
overflow `abort`; they are not miscounted as self calls or missing business guards.

## Original instruction evidence and proposed source

The five original token-reader arguments come directly from their context's
`AccountInfo` field. The selected body instead clones each field to a temporary
before passing its address. Offsets below are relative to each body's start:

| Used operation | Original call | Selected call | Account field |
| --- | --- | --- | --- |
| Wallet quote frozen | `+0x2648` | `+0x1910` | `+0x40` |
| Shared AMM quote frozen | `+0x24d0` | `+0x3cf0` | `+0x88` |
| Shared AMM quote amount | `+0x2518` | `+0x3de8` | `+0x88` |
| Shared creator-vault quote amount | `+0x20c8` | `+0x4898` | `+0x48` |
| Shared creator-vault quote frozen | `+0x2110` | `+0x4980` | `+0x48` |

[The argument ledger](evidence/borrow-proof.json) retains exact instruction
contexts. The verifier compares their complete bytes to the two authenticated
ELFs. The source changes `&field.to_account_info()` to `field.as_ref()` at these
five used calls. Two other calls already use direct borrows and remain unchanged.

The wallet and shared-AMM frozen predicates also redundantly call
`data_is_empty()` before `token_frozen()`, whose first operation already returns
`Ok(false)` for empty data. Removing those two outer checks preserves that empty
account result and retains the helper's checked borrow/deserialization path.
All owner/signer checks, business guards, error operations and their order remain
in the proposal. The separate `pay_token` helper remains unchanged.

| Defined direct-callee count | Selected control | Measured overlay | Original |
| --- | ---: | ---: | ---: |
| `AccountInfo::clone` | 53 | 48 | 33 |
| `AccountInfo::data_is_empty` | 8 | 6 | 6 |
| `token_frozen` | 5 | 5 | 5 |
| `token_raw_amount` | 2 | 2 | 2 |

The predictions were confirmed by the actual new caller: 18,104B and170 defined
direct calls, down from19,632B and177. `pay_token` remains a used separate3,144B
helper. Other clone clusters and the `pay_token`
caller/callee boundary remain separate attribution work. No attribute, compiler
flag, dependency, SDK, binary, comparator or source-origin bypass is changed.

## Source and image bindings

The analysis input is maintained revision
`1285b5e9e3a29c1e2cf32246d6046035e5d66fad`. Live main
`a18e1e89b59bf9d734955550c92f321c97c95e62` still contains the identical source.
The research overlay is the only proposed program source change:

| Input | SHA-256 |
| --- | --- |
| [Unchanged before source](source/admin_cto.before.rs) | `6353b1f7b9e613bb8d819000c504d44410b04f7da7dfbdc7fb2e5132df100180` |
| [Proposed source](source/admin_cto.rs) | `f4a2bb7d33431e0fb4911e39d5e03c8bb9f45c6f7a184da21d1a6762f9127955` |
| Captured original allocation | `7a19affaa2c6187e04a5fe0ea298cee81fa5eb8c24cfcc30d85f615e89f7b02d` |
| Selected symbol ELF | `49df399b8a36a0a60de03e8d55f1417261dc451e44845ca9d17a94040968c680` |
| Actual overlay ELF | `d537faf5907c594eeef6f3706d87e300e6f01509243b5dcf28b018f3c90a64c6` |
| Actual overlay symbol ELF | `daa2772d4745d8488b357c6c1c088fadc77bf31d341c59f5b50c4706d7b54c78` |

The exact before-source Git blob is
`f8127a38285fa993c5fbdcb99304451bf8ccb4ee`. The selected symbol ELF is published
at `research/pump-final-composition-673-20261028/artifacts/unstripped.so`.
[The patch](proposal.patch) is an overlay for
`programs/pump/src/creator/admin_cto.rs`, not an applied maintained-source change.

The source inherits explicitly engineered blank-line positioning from earlier
qualified reconstruction. This proposal adds no padding and preserves all 775
newlines plus the explicit `error!`, `require!`, `panic!`, `unwrap` and `expect`
token line/column ledger. That finite token check does not prove every
compiler-generated `Location` remains equal; unexercised runtime sites remain open.

## Repeatable checks

From a complete repository checkout:

```sh
python3 -B scripts/verify_evidence.py
python3 -B scripts/test_tooling.py
python3 -B research/pump-cto-direct-borrows-20261029/verify.py \
  --original evidence/original/pump/deployed.so \
  --selected-symbols research/pump-final-composition-673-20261028/artifacts/unstripped.so
python3 -B research/pump-cto-direct-borrows-20261029/test_verify.py \
  --original evidence/original/pump/deployed.so \
  --selected-symbols research/pump-final-composition-673-20261028/artifacts/unstripped.so
python3 -B research/pump-cto-direct-borrows-20261029/verify_measurement.py
python3 -B research/pump-cto-direct-borrows-20261029/runtime-tools/test_replay_controls.py
```

All nine original/dependency captures and six comparator controls pass. The
proposal verifier passes normally and under `python3 -O`; its three negative
controls reject an undeclared source edit and mutations to each image's argument
witness. Exact commands, script/source/input hashes and outputs are retained in
[validation](validation/receipt.json). The static checks read ELF bytes.
`verify_measurement.py` independently checks retained actual compiler inputs,
outputs, census and genuine signed observations without rerunning a compiler or VM.

The authenticated native-673 control passed in
[run 40791064153](https://github.com/shawkkkkk/pumpfun-source/actions/runs/40791064153).
The exact `f4a2bb7d…` overlay was independently compiled in
[run40792775552](https://github.com/shawkkkkk/pumpfun-source/actions/runs/40792775552).
[Raw outputs and receipts](native-build/) retain the genuine empty-target native
macOS v1.44 recipe with authenticated Linux SBPF target libraries. Both local
crates actually compile. All65 source inputs differ from the frozen selection in
this one file; the archive verifies all66 workspace compiler inputs.

The [official complete census](census/delta.json) retains1,019/1,035 normalized
and188 raw windows, with zero membership gains or losses. Whole ELF equality
remains false. The [actual callee audit](evidence/f4-native-callee-audit.json)
confirms the five clone and two emptiness-call removals. No byte-coverage increase
is claimed from the shorter caller.

The unchanged18 common-wallet witnesses executed against the original allocation,
selected673 control and actual new overlay:54 fresh signed executions,108 verified
signature fields,54 captured-loader loads, and zero structured or full ordered
non-CU log differences. The verifier independently derives the pool-authority PDA
and checks it is not a top-level transaction signer; the genuine admin signs.
No Source filename or coordinate substitutions occur. Four additional controls
reject forged Source logs, altered CPI logs and invalid signatures, and permit
only the exact standard compute-consumption line difference.

These18 cases contain zero original Source-filename log records and exercise the
common-wallet flow. They do **not** close the runtime coverage gap for four shared
reader borrows, all holder/pool paths, the full44 suites or all compiler-generated
Location records. This is a bounded source/measurement contribution, not a
canonical selection or broad equivalence claim. Original selected-image receipts
were not transferred to the new image.

To rerun the same18 producer on a complete checkout, choose a fresh output path:

```sh
python3 -B research/pump-cto-direct-borrows-20261029/runtime-tools/replay.py \
  --candidate research/pump-cto-direct-borrows-20261029/native-build/candidate.so \
  --candidate-sha256 d537faf5907c594eeef6f3706d87e300e6f01509243b5dcf28b018f3c90a64c6 \
  --build-record research/pump-cto-direct-borrows-20261029/native-build/build-comparison.json \
  --output work/pump-cto-direct-borrows-fresh18
```

The portable controller changes only input-root selection/default paths from its
first executed local copy, which remains archived. It was rerun on the identical
actual image before publication. No fixtures, signers, comparison fields or logs
were changed. [MEASUREMENT.json](MEASUREMENT.json) binds both retained runs, tools,
images and receipts. Current global counts and selected artifacts remain unchanged.

Attribution: the original/candidate callee ledger supplied by the creation worker
was independently decoded from the authenticated images before this proposal;
the CI worker owns the independent control/candidate builds. This packet contains
the CTO-specific source correction and exact argument witnesses. It does not
claim original source spelling, private build provenance, security acceptance or
work from those independent build units.
