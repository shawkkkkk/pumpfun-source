# Frozen 6ff770f7 native identity control (operational preparation)

One unchanged source commit `6ff770f7a8a2a74ff3a631b644f1ffef59640582`, measured
with the maintained macOS ARM64 v1.44 identity recipe. No Rust proposal, candidate,
paired build, latest-main claim or expected historical ELF hash is part of this job.
Only this README, the controller and the registered
`.github/workflows/qualify-pump-macos-v144.yml` may differ in the operational
checkout, which must be one direct child of the frozen source commit.

The controller derives program and complete CORE vectors from Git, applies the
unchanged maintained source selector, and retains both full source and compiled
workspace archives. Current independent source admission is 141 selected files,
aggregate `46b623d7c8ded1dd6a09555eb26b38a80b8afda750d290371e69a84cb4bdfab6`;
these are corroboration, not a replacement for deriving the actual vectors.
The previous 1ddb control's 135-input aggregate and ELF hashes remain historical.

`--preflight-only` executes real maintained staging and pure script validation;
it does not install/run an SDK, Cargo, compiler or linker. An explicitly bound
local loader may select the actual frozen checkout and owned evidence/work paths
for that preflight; the full hosted operational-parent checks are not thereby run.
Full mode requires macOS 26 ARM64, fresh work/SDK/cache/target locations, the exact
v1.44/v1.52 archives previously authenticated in run41065537974, complete SDK and
Linux-target-library checks, locked acquisition, and one offline cold compilation.
The v1.52 SDK is analysis-only. Compiler/profile/target flags are unchanged.

Operational integration since the old49bf controller: pass the already admitted
snapshot into the maintained stage API; accept the CURRENT linker's checked
private `ordered.ld` pathname rather than the former mutable staged pathname.
The retained Git-bound link helper checks source/default bytes and writes the
private copy before invoking authenticated native LLD, then removes it. Receipt,
map, frozen helpers/scripts and native LLD are retained. The temporary bytes are
not independently available after cleanup and are not claimed retained.

Before/after source, CORE, registry, tools, SDK and native-LLD checks stay strict;
inherited `PYTHONDONTWRITEBYTECODE=1` prevents unrecorded hook cache files rather
than excluding them. Full build logs, cold-target proof, local crate compiler
fingerprints and both raw ELFs are uploaded with the unchanged full1035 scorer
report, including unmatched rows. Gains/losses refer to the explicit retained
historical baseline, not a new source improvement. Artifacts expire after30days.

This operational adaptation has not yet run natively. Only an actual uploaded
result can qualify output bytes. Failed runs and old preparation evidence stay
separate. Coordinator review precedes publication/dispatch; no compiler launch
is authorized by a source/preflight result alone.
