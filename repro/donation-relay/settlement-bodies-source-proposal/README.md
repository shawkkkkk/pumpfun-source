# Relay: three complete settlement bodies from ordinary source

This source-only continuation of [PR181](https://github.com/lalalune/pumpfun-source/pull/181)
recovers original normalized windows **97, 98 and 100** without losing any prior
window: **485 → 488/492**, with **142 raw local matches** unchanged. Only original
windows 92–95 remain unmatched. These three are normalized-body gains, not raw
body equality or whole-program identity.

| Original ordinal | Body | Complete bytes | Checked direct callees |
| --- | --- | ---: | ---: |
| 97 | distribute_after_just_swapping | 5216 | 36 |
| 98 | distribute_non_swap_output_mint | 5696 | 38 |
| 100 | swap_then_distribute | 5328 | 25 |

All **99 actual direct-callee sites** bind complete normalized bodies and closed
recursive direct-call shapes. These callers have no indirect instructions;
that does not prove arbitrary runtime behavior or all transitive semantics.
Total recursively direct-call-shape-closed pairs rise 650 → 659. The recovered
callers have 68 direct data references; a full object-type/extent proof for each
is not asserted.

## Minimal ordinary-source boundary

Exactly three source files change across two exact 60-input maps:

- Use a generic iterator of basis points in the source-attributed checks helper,
  preserving checked arithmetic and the diagnostic error constructor.
- Use a normal `DistributionArgs::new` constructor that accepts a borrowed
  program key and copies it inside the constructor, instead of eager caller
  field construction.
- Restore the measured declaration order of the existing argument fields.

The actual helper is called by all three settlement paths. No dead helper,
assembly template, copied target instruction sequence, custom linker-order file,
output patch, or padding is used. This establishes a reproducible ordinary-source
candidate, not unique historical source or struct-layout provenance.

The baseline map points to immutable public ordinary source blobs in PR175 and
PR181. It does not read program bytes as compiler inputs. The packet supplies
three readable overrides, their exact unified patch, full before/after hashes,
portable recipe reference and static verifier/tests. Prior selected checkpoints,
source programs and sealed evidence are not overwritten.

## Preserved data result and remaining raw gap

The complete `.rodata` remains **19,863 bytes raw-equal**, SHA-256
`353454bb0f6cd671503726c5427817c16f7c9c0054d8568ddd9d0cf8be11f2df`.
The optional checker freshly audits all 359 positional `.data.rel.ro` pointers
and 507 nonpointer qwords: 282 read-only-data offsets into the identical section,
74 closed direct-call-shape text targets, and three same-relative data targets.
Five text targets contain indirect calls; this is relocation-aware data shape,
not semantic/indirect closure. The complete recomputed address ledger is bound
by a digest, rather than republishing another long address table.

The `.text` excess shrinks 120 → 112 bytes. `.data.rel.ro` common-position
mismatches shrink 473 → 462 and `.rel.dyn` mismatches 3235 → 3170. Nevertheless,
whole-file common differences remain **383,718 positions**. The candidate is
818,392 bytes versus 818,280 meaningful original ELF bytes and 830,448 captured
bytes; the original-only tail is 12,056 bytes. Neither full capture nor meaningful
ELF equals this candidate. These positional counts and size gaps are not a
completion percentage or a measure of missing source. Full core identity remains
0/4.

## Verification and reproducibility

Local independent root-clean builds reproduced both outputs and finite offline
replay passed. These are **local observations, not downloadable runtime proof**.
Protected relayer settlement success is not dynamically covered. No ELF,
compressed/encoded program payload, replay cases, archived build/runtime receipts
or their excerpts are published. Static reports below were freshly recomputed
from original/compiler outputs without reading archived receipts.

With Python 3.11+ and a Git clone containing the pinned public source commits:

```sh
P=repro/donation-relay/settlement-bodies-source-proposal
python3 -I -B "$P/verify.py"
python3 -I -B "$P/test_verify.py"
python3 -I -B "$P/verify.py" --materialize work/relay-settlement488-source
python3 -I -B "$P/verify.py" --variant baseline --materialize work/relay-settlement485-source
```

Default verification checks source integrity and recorded static metadata, not
ELF bytes or execution. It reports `compiler_executed=false` and
`runtime_verified=false`. Nine stdlib tests cover full materialization, mutation,
patches, unsafe paths/symlinks and the default no-ELF/no-receipt read boundary.

Build each materialized source using the reviewed [official native v1.48 recipe
pinned by PR175](https://github.com/lalalune/pumpfun-source/blob/a56a22f32fce7dfe4e05c47d48e7b18651438779/repro/donation-relay/module-layout-facade-source-proposal/README.md#portable-local-compilation-recipe).
Preserve its 253 checksum-pinned public packages, locked/default features,
release profile, explicit clean environment, remapped source paths and strip
command. Authenticate official tools and registry inputs before executing native
build scripts/procedural macros. This verifier does not install tools or sandbox
a build. Local results used root-clean dependency-cache reuse; a fresh relocated
all-dependency build must be independently compared, not assumed identical.

Supply the two local output directories, each containing `candidate.so` and
`symbols.so`, for an optional full remeasurement:

```sh
python3 -I -B "$P/verify.py" \
  --baseline-build /path/to/baseline-build \
  --candidate-build /path/to/recovered-build
```

The checker rehashes/reanalyzes both pairs, recomputes all gains/losses and
section inventories, checks every recovered actual callee, and independently
recomputes the data graph. No mode executes a compiler or target VM. Final hashes:

- Stripped: `e98ef5d4453ea93ab8189b35d7183a0777b2bf3ee46f87497a11700c263f55a3`
- Symbols: `fa862881aae3ced649f3db972b1ba4ec80af9d7dcf8d8f5a54fc32011c1a1d45`
