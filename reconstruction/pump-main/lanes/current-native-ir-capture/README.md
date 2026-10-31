# Frozen39eb377a JumpThreading and machine capture

This is one diagnostic build of unchanged Pump source at
`39eb377aa6c6ce4aacff273aa13732abb0c0078a`. Selected source141 has aggregate
SHA256 `a0cbf5b4a9adf2aaefd9a54d19ee2167032fb31a62a197dc871da71b53705642`;
complete CORE has236 files and maintained staging has142. No source, CORE,
scorer, threshold, optimization pipeline or link recipe is changed.

The actual reference is successful faithful native control
[run41159607118](https://github.com/shawkkkkk/pumpfun-source/actions/runs/41159607118),
artifact13026402898, operational commit
`d330ff55ca203ae8c733216770f16c3c56fbf033`. Its original ZIP is2,539,442 bytes,
SHA256 `94d7f23a92e0cae60b186ae589bffa7767e2c18f63b93dfb8e97f6c7e4a912c6`.
All43 extracted member sizes/hashes are frozen in the controller. The workflow
uses pinned official `actions/download-artifact` by exact run/artifact ID; the
controller authenticates every extracted member and exact source/CORE/selected/
staged vectors before SDK acquisition. It does not claim to rehash the outer
ZIP in the hosted diagnostic job.

The actual current reference ELF uniquely defines
`_ZN14pump_recovered9admin_cto7execute17h3bd6d7f34f2e30d7E`, VA `0x22a10`,
27,400 bytes. The filter was frozen from that actual artifact. The faithful
reference hashes are unstripped
`289b7d63122fb1f8a64213df1b781b49aa596448e2f33256fa85365d9f7ed4f4`
and stripped
`5dff5613d7b329e6662eb10ad88b05cafa400da0620b1ba21da4c6f339823d16`.
No FAF artifact or old output hash is reused as current evidence.

The operational commit must be one direct child of the frozen source and may
change exactly these four operational paths:

- `.github/workflows/qualify-pump-macos-v144.yml`
- `reconstruction/pump-main/lanes/current-native-ir-capture/pump_ir_control.py`
- `reconstruction/pump-main/lanes/current-native-ir-capture/capture.py`
- `reconstruction/pump-main/lanes/current-native-ir-capture/README.md`

## Fixed diagnostic measurement

Current source's
[w14a66 fee-edge notes](https://github.com/lalalune/pumpfun-source/blob/39eb377aa6c6ce4aacff273aa13732abb0c0078a/reconstruction/pump-main/lanes/w14a66-cto-feeedge/NOTES.md)
explicitly use `-print-after=jump-threading` and discuss JT1/JT2, the target's
7/9-byte copies, lifetime markers and duplication cost. This capture adds the
matching fixed before/after printing to measure actual current input/output of
that pass, alongside the previously captured machine boundaries. It does not
run the notes' IR-edit, opt/llc, variant or threshold experiments.

Only the single exact maintained `fastbuild.run_compiler` Cargo boundary is
hooked. `cargo build` becomes `cargo rustc`; the original manifest, target,
release/locked/offline arguments, cwd, compiler/wrapper/target paths and identity
flags must match. The helper appends `--lib -- --emit=link,llvm-ir`, followed by
one `-C llvm-args=...` pair for each fixed argument:

- `-filter-print-funcs=` plus the exact current target symbol above
- `-print-before=jump-threading`
- `-print-after=jump-threading`
- `-print-after=finalize-isel`
- `-print-before=greedy`
- `-print-after=greedy`
- `-print-after=virtregrewriter`
- `-print-after=block-placement`

Every original positional argument and keyword, including timeout, cwd and
environment, reaches the original compiler function unchanged. It is restored
in `finally`. Source/path/output admission precedes helper output creation.
The receipt records actual original/diagnostic argv, delta, call count and an
explicit compiler/linker environment subset; inherited credentials/environment
are not dumped. No Rust MIR option, second build, fallback flag, pass-name
search, threshold change, opt/llc invocation or IR modification is permitted.

The saved raw `build.log` remains intact. Every emitted root `.ll` is copied
verbatim. Every bare or comment-prefixed LLVM dump section is retained as an
exact byte slice, including unknown, incomplete and failed output. Complete
IR definitions are additionally retained as exact target-function byte slices
with original log offsets and hashes. No extracted IR is recompiled.

Machine qualification requires one complete target function in each of the
five requested timing/pass stages, with unique ordered opening/ending markers.
JumpThreading qualification requires at least two ordered, alternating complete
Before/After target-IR pairs, corresponding to observed JT1/JT2; all additional
observed pairs are retained. Both registered-ID and fixed legacy readable
Jump Threading headings are recognized, including trailing heading colons.
All sections and partial/unpaired snapshots remain visible when qualification
fails. Native flag acceptance, pair count and completeness are measured by this
one actual run; parser controls or prior machine logs do not prove them.

## Code identity and outcome

Build success and complete diagnostic attribution are separate. A successful
build with incomplete capture still reaches the official scorer, then fails
attribution while retaining its real output. SDK/build failures and partial
capture remain failures; no retry or changed configuration is implied.

Qualified current attribution requires complete stripped ELF byte equality,
all non-symbol section payloads equal, every semantic function symbol equal,
and every symbol's non-name numeric fields equal to the actual current control.
Only names of local `STT_OBJECT` symbols may differ; those differences and both
full ELF hashes are recorded separately. Full unstripped hash equality is not
assumed from emitting IR and is not the code-identity predicate. All1,035 actual
official score rows must equal the new control, and only the unstripped
`candidate_sha256` summary field may differ. The optimized target definition,
all five machine stages and complete JT1/JT2 pairs are also mandatory.

The faithful controller's existing full SDK archive/inventory/target-library,
native LLD, locked fetch, cold target/cache, local-crate fingerprint/flag,
source/CORE/stage/registry/tool before/after, private script/map and official
full-census guards remain intact. Python cache writes are disabled. Actual
source/workspace archives, link receipts, raw ELFs, compiler output and failure
receipts are uploaded for30 days.

`--preflight-only` performs real current source selection/staging/link-script
admission and all43 actual reference checks, then returns before SDK/bootstrap/
Cargo/compiler/linker operations. An explicitly bound local loader may select
the frozen checkout and owned RAM paths; it does not exercise native operational
parent/SDK/output admission. Pure hook and parser controls establish only their
bounded argument/format behavior.

This preparation is not a native current IR result or a source candidate.
One reviewed root-owned diagnostic dispatch supplies the actual trace needed
before proposing a source carrier. No source gain, new runtime coverage,
later-main equivalence, whole-original equality or security acceptance follows
from preparation or from code identity with this control.
