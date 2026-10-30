# Frozen faf99624 native identity control (operational preparation)

One unchanged source commit `faf99624250b4e60107790f7edabf6609f709885`, measured
with the maintained macOS ARM64 v1.44 identity recipe. No Rust proposal,
paired build, latest-main claim, expected historical ELF hash or score floor is
part of this job. Only this README, the controller and the registered
`.github/workflows/qualify-pump-macos-v144.yml` may differ in the operational
checkout, which must be one direct child of the frozen source commit.

This is the minimal BASE/label adaptation of the reviewed 6ff controller
SHA256 `09128658accc91777e204df45dd766b683b6bb440f56013ec9eee032b5823cbc`,
which produced actual run41120816818. That run's source, outputs and receipts
remain historical; no previous ELF or match count is an expected current result.
The current fastbuild, source_inputs and link_order APIs have unchanged bytes.
Program and complete CORE vectors are freshly derived from the frozen Git tree,
the unchanged maintained selector and actual staging. No source count is assumed.

`--preflight-only` executes real maintained staging and pure script validation;
it does not install/run an SDK, Cargo, compiler or linker. An explicitly bound
local loader may select the actual frozen checkout and owned evidence/work paths
for that preflight; the full hosted operational-parent checks are not thereby run.
Full mode requires macOS 26 ARM64, fresh work/SDK/cache/target locations, the exact
v1.44/v1.52 archives previously authenticated in run41120816818, complete SDK and
Linux-target-library checks, locked acquisition, and one offline cold compilation.
The v1.52 SDK is analysis-only. Compiler/profile/target flags are unchanged.

The controller passes the admitted snapshot into stage(expected_inputs=...).
The frozen maintained linker checks source/default bytes, writes a private
ordered.ld copy, forwards it to authenticated native LLD and removes it after
linking. The controller retains receipt, map, frozen helpers/scripts and native
LLD identities. Removed temporary bytes are not claimed independently retained.

Before/after source, CORE, registry, tools, SDK and native-LLD checks stay strict;
inherited PYTHONDONTWRITEBYTECODE=1 prevents unrecorded hook cache files rather
than excluding them. Full build logs, cold-target proof, local crate compiler
fingerprints, both raw ELFs and the unchanged full1035 scorer report are uploaded,
including unmatched rows. Gains/losses in that report refer to the explicit
retained historical baseline, not a new source improvement. Artifacts expire
after30days and are not permanent hosted availability guarantees.

This operational adaptation has not yet run natively. Only an actual uploaded
result can qualify output bytes. Failed runs and old preparation evidence stay
separate. Coordinator review precedes publication/dispatch; no compiler launch
is authorized by a source/preflight result alone. No diagnostic/IR flags are
added to this faithful baseline.
