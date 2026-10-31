# Frozen FAF CTO diagnostic capture

This job makes one diagnostic build of unchanged Pump source at
`faf99624250b4e60107790f7edabf6609f709885` on macOS 26 ARM64 using the maintained
v1.44 identity recipe. It captures optimized LLVM IR and target-filtered LLVM
machine-function dumps for the actual ELF symbol
`_ZN14pump_recovered9admin_cto7execute17h3bd6d7f34f2e30d7E`.
The selected source is 141 files, aggregate SHA256
`29a8df2d7e12b379a9dc515d5a84eaaf051729da62350a54996a0077015f0c8a`;
maintained staging has 142 files and the complete CORE vector has 236 files.
No program source, CORE, scorer or build recipe is changed.

The operational commit must be one direct child of that frozen source and may
change only these four paths:

- `.github/workflows/qualify-pump-macos-v144.yml`
- `reconstruction/pump-main/lanes/current-native-ir-capture/pump_ir_control.py`
- `reconstruction/pump-main/lanes/current-native-ir-capture/capture.py`
- `reconstruction/pump-main/lanes/current-native-ir-capture/README.md`

The controller derives source/CORE vectors from Git and uses unchanged maintained
snapshot/staging helpers. It retains full SDK archive/inventory and Linux target
library checks, authenticated native LLD, locked dependency acquisition, empty
target/cache admission, local-crate fingerprints and target flags, before/after
source/CORE/stage/registry/tool checks, private linker-script and map receipts,
both full ELFs, and the official complete 1,035-window score. Python cache writes
are disabled rather than excluded from those checks.

The capture helper admits source/path/output inputs before creating a directory
or receipt. It hooks only `fastbuild.run_compiler` and requires the single exact
maintained Cargo argv, manifest, target, cwd, compiler/wrapper/target paths and
identity flags. It changes `cargo build` to `cargo rustc`, then appends exactly
`--lib -- --emit=link,llvm-ir` and these root-only LLVM diagnostics:

- `-filter-print-funcs=` followed by the exact symbol above
- `-print-after=finalize-isel`
- `-print-before=greedy`
- `-print-after=greedy`
- `-print-after=virtregrewriter`
- `-print-after=block-placement`

Each LLVM option is passed as its own `-C llvm-args=...` pair. This follows the
published `w12a02-cto-iroracle/scripts/capture.py` Cargo boundary and the prior
`exact-sol-reconstruction/capture_backend.py` LLVM dump mechanism. Every original
positional argument and keyword, including cwd, environment and timeout, reaches
the original compiler function unchanged. The hook is restored in `finally`.
The receipt records original/actual argv, the exact delta and an explicit list of
compiler/linker environment values; it does not dump the inherited environment.
No Rust MIR option, second build, fallback flag or pass-name search is permitted.

The raw `build.log` stays intact. Every available `deps/*.ll` is copied verbatim
into `llvm-ir/`, and every LLVM dump is retained as an exact byte slice in
`machine-dumps/`, with offsets and hashes. Available partial outputs are copied
on build failure or exceptions too. A stage qualifies only when its exact heading
and complete target machine-function delimiters are present; optimized IR must
contain the target definition. `buildOk` and `captureComplete` are separate.
A successful build with incomplete capture still reaches official scoring, but
cannot produce qualified attribution. Failed/partial evidence is retained and
must not trigger a retry or a changed diagnostic configuration.

The reference is actual successful native control run **41146593117**, artifact
**13020993188**, operational commit
`50ebec8188201e8e8bf8f484f2b6b44e3387e121`. The workflow uses pinned official
`actions/download-artifact` to retrieve that artifact by run and artifact ID.
The controller authenticates all 43 extracted member sizes/hashes, exact source,
CORE, selected/staged vectors, and the full score census before SDK acquisition.
The prior transport ZIP SHA256 is
`ac71b05401e38551fcd30aca8a310773adad5eb3355a8f5d5faa940c4cababb0`;
the workflow does not claim to redownload or rehash that transport ZIP.

Qualified attribution requires both complete ELF hashes to equal that actual
control (unstripped
`8febf467fc61fbf17ff11045ed9d7b0d3aba0eeedbcadf5060abb2552212b02a`,
stripped `d5cee214ba29be1a1ccbb96d036f3dd7dfbd683d61046d76b66103507d3ef750`),
all 1,035 official score rows and the full summary to equal its report, the
optimized target definition, and all five requested complete dump stages.
A mismatch preserves actual output and fails attribution. The existing
1,034/1,035 raw and normalized result and unresolved 27,400-byte CTO window
remain baseline observations, not a predicted gain.

`--preflight-only` runs real staging, pure link-script admission and reference
hash/vector checks without SDK acquisition, bootstrap, Cargo, compiler or linker.
An explicitly bound local loader may select the actual frozen checkout and owned
RAM paths for that check; full hosted operational-parent checks are still pending.
Pure fake-boundary checks can verify argument forwarding and restoration, but
cannot prove native pass availability, ELF equality or diagnostic completeness.
Only a real uploaded native result can establish those facts. The capture is
compiler attribution evidence only: it makes no source gain, VM/runtime,
latest-main, whole-original equality, or security-acceptance claim. Uploads retain
partial failures and expire after 30 days.
