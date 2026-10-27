# Fees: recover the complete legacy preparation helper from ordinary source

Two source files on the exact 44-input
[public PR227 source](https://github.com/lalalune/pumpfun-source/blob/c5fb4efd18521f4c6aa6d5db3479e9d7b1b67ac2/research/fees-v2-finish-source-recovery/README.md)
recover the complete **5,008-byte original preparation body at 199072**.
The actually compiled comparison is **573 → 574 / 585 normalized counterparts**,
with no losses, **143 raw local counterparts** unchanged and 426 → 427 unique
pairs. This is a measured pinned-source result, not arithmetic added to a moving
main-branch count and not whole-file identity.

## Source cause and attribution

- Use `remaining.get(i).ok_or_else(|| error!(FeeError::NotEnoughRemainingAccounts))?`
  for the real account admission, instead of the separate guard/index sequence.
- Use `retained.len().saturating_sub(1)` for the retained maximum index.
- Move that real helper into the already existing
  `instructions/fee_sharing/update_fee_shares.rs` module and reexport its previous
  public path. Its actual error macros now occur at lines 186/188; the final
  indexed expression has the observed bounds Location 228:55.

The module's existing update/finish source and physical coordinates are preserved;
only one required import and the previously blank 177–231 span change there.
The other 42 source inputs, dependencies, lockfile and features remain exact.
No dead helper, assembly, executable payload, forged runtime Source object, new
normalization rule or binary rewriting is used. Names, ownership and whitespace
are sufficient reconstructed source, **not proof of historical source spelling**.

PR225/PR227 own the preserved legacy/V2 finishing recoveries. The later PR229
Sweep composition, PR231 V2 semantic correction and PR232 nonhistorical Social
likelihood recovery are not composed into this pinned source. Those separate
published results must not be counted as new work here. Eleven original windows
remain unmatched in this particular candidate.

## Recomputed static proof

`verify.py` defaults to source-only checks. With four explicitly supplied local
inputs it imports three hash-pinned public parser files and freshly recomputes
all inventories, direct edges, Locations, raw section differences and the new
body proof. It reads no archived result/build/runtime receipt and performs no
network, Git, compiler or target execution. The exact original, baseline and
candidate ELF hashes are pinned before optional measurement. Compiler outputs
are comparison inputs only, never materialized compiler source.

- All **15 same-offset actual direct callees** from the new complete body have
  matching complete normalized shapes. The actual `abort` import and absence of
  indirect calls in this body are checked.
- All **13 direct data operands** agree over explicit bounded extents: error
  discriminants, explicit strings, inferred Rust Location records and inferred
  formatter tables with their actual function-pointer targets. These are not
  claims that every backing allocation boundary is proven.
- The shape-ambiguous addition-overflow helper is independently bound through
  its actual descriptor, 28-byte message and complete panicking target.
- The actual existing payout at original 204080, call offset 80, now reaches the
  recovered body. This previously unequal edge closes; the helper is not dead.
- All **3,765 previously equal actual callee obligations** remain equal. Fifteen
  new-body call sites are checked; all 171 prior Location uses persist, with
  three newly matched uses (**174 total**). Nine actual edges still target unequal
  complete bodies.
- Six in-memory negative controls reject the old unmatched parent and altered
  Source path, Location line, formatter size, error discriminant and incoming
  payout target. These are static mutations, never executed programs.

This is bounded direct-call/data evidence, not recursive all-data closure,
indirect-call equivalence, complete semantics or raw identity. Normalization
masks relocated fields; matching shape is not raw byte equality.

| Measure | Exact PR227 parent | Recovered |
| --- | ---: | ---: |
| Normalized original counterparts | 573 | 574 |
| Raw local counterparts | 143 | 143 |
| Unique complete-body pairs | 426 | 427 |
| Equal Location uses | 171 | 174 |
| Compiler ELF bytes | 878,328 | 878,360 |
| `.text` bytes | 803,832 | 803,920 |
| `.rodata` bytes | 21,191 | 21,191 |
| `.data.rel.ro` bytes | 6,896 | 6,872 |
| `.rel.dyn` bytes | 44,592 | 44,560 |
| Common-position differences versus original | 462,972 | 463,015 |

Raw positional differences **worsen by 43 bytes**. The original meaningful ELF
is 873,256 bytes, so the candidate is still 5,104 bytes longer. The original
948,944-byte capture also includes a 75,688-byte allocation tail. Neither whole
ELF nor full capture matches; selected checkpoints are unchanged.

## Local compilation and finite execution scope

Two genuine root-clean native builds reproduce both entire candidate outputs:

- Stripped: `2f2613def4f89fb55e998c9581b48055760baf967b2bc7661f6b53eeaf68013d`
- Symbols: `c661a3a69b6197b14aa53b4601996cf198d539a8b2cb4f4b80e09372d1b24164`

Builds use official Linux platform-tools v1.44 and the locked registry/math
cache; the local stripping step is official v1.48 `llvm-objcopy --strip-all`.
A real root compiler invocation is checked. This is not an all-dependency-clean
build, complete host-library attestation or evidence of historical tool paths.

Fresh local executions of both the exact public parent and accepted candidate
pass the defined 17,331-case / 18-suite regression. On this current parent, the
417-case sharing scope repairs six application-log mismatches; **27 inherited
sharing-log mismatches remain** (not the obsolete older-parent 72). Forty actual
AMM transfer CPIs persist. Eight additional successful executable-holder
filtering cases check seven exact downstream distribution events and the
all-filtered CPI skip. The combined checks authenticate 1,704 transaction records
and 3,392 signatures; 348 legacy Social cases, eight owner cases and two native
arithmetic boundaries also pass their finite comparisons. The 201 pinned runtime
inputs remain unchanged.

The exact candidate still has the public parent's **three outcome and 283
application-log mismatches in the separate 640-case V2 Social scope**. PR231's
correction is not composed here. Finite passing suites are not exhaustive
semantics, all-log equality, arbitrary-state safety or live-chain reachability.

These are local observations only, **not downloadable execution proof**. The
source-only default and optional static reader always report
`runtime_verified=false` and `native_build_verified=false`; no build/runtime
receipt, case, transaction, log or derivative is published.

## Verify and materialize without executing the target

```sh
P=research/fees-legacy-preparation-source-proposal
python3 -B "$P/verify.py"
python3 -B "$P/test_scope.py"
python3 -B "$P/materialize.py" --parent-source /exact/pr227-expanded-source --output /fresh/source
```

Sixteen stdlib tests cover exact reversible patches, source membership,
provenance, altered inputs, unsafe/symlink paths and forbidden default claims.
Materialization requires the complete exact 44-file parent map. Public source
provenance records compressed storage hashes separately from actual UTF-8 source
hashes, including explicitly disclosed hash-identical source reuse from an older
public revision. No source is fetched automatically, and no hash fallback or
partial source set is accepted.

Optional local static comparison:

```sh
python3 -B "$P/verify.py" \
  --original /local/captured-pump-fees.so \
  --baseline-build /local/pr227-build \
  --candidate-build /local/preparation-build \
  --parser-root /local/repository
```

Each build directory must contain `candidate.so` and `symbols.so`; the parser
root must contain the three exact files declared in `parser-inputs.json`.
Python optimization (`-O`) is explicitly rejected because it would disable
assertion-based static checks. No ELF file is included in this packet.

For native reproduction follow the pinned public PR227 build recipe and parent
chain, using these 44 materialized inputs. Preserve its 252 registry packages,
default Anchor/SPL features, `sbpf-solana-solana`, `--release --locked --offline`,
overflow checks, panic-abort, codegen-units=1, no LTO and math source-path remaps.
Require a genuine root compiler invocation; authenticate any reused dependency
cache or genuinely rebuild its dependencies. Fresh-dependency and relocated-path
identity remain separate checks. Never replace or edit compiler output to repair
its hash. Ordinary source verification alone does not attest native builds,
runtime behavior or whole-binary identity.
