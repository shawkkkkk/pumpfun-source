# Frozen39eb377a native identity control

One unchanged Pump source commit,
`39eb377aa6c6ce4aacff273aa13732abb0c0078a`, tree
`cfebeb4e9117b764f251a7ed7727a3dca192b298`, measured with the maintained
macOS26 ARM64 v1.44 identity recipe. This is the narrowly adapted faithful
controller SHA256 `f951a055235298250c6a46df95bf06994cccf3bcd0233a9abafeec4958a5e018`
that produced the actual FAF control run41146593117. That older run and its
hashes remain historical; they are not expected output bytes for this source.

Only the registered `.github/workflows/qualify-pump-macos-v144.yml`, this README
and `pump_current_control.py` may differ in the operational checkout, which
must be one direct child of the frozen source. The controller changes only its
frozen BASE and descriptive source label. There is no Rust proposal, paired
candidate, diagnostic/IR flag, compiler variant, historical hash floor or
latest-main claim in this job.

Current physical inputs were selected through a real detached sparse Git
checkout. Program and complete CORE vectors are derived from the frozen tree.
The maintained source selector admits141 files with aggregate SHA256
`a0cbf5b4a9adf2aaefd9a54d19ee2167032fb31a62a197dc871da71b53705642`;
real maintained staging yields142 workspace files. The complete CORE vector
has236 files and is unchanged from the reviewed FAF inputs. Source/CORE checks
include exact sets, modes, Git blobs and SHA256 hashes. An inherited
`PYTHONDONTWRITEBYTECODE=1` prevents helper cache files rather than excluding
them from admission.

`--preflight-only` executes actual Git/input admission, maintained source
selection and staging with real rsync, and pure linker-script validation.
It returns before SDK acquisition, bootstrap, Cargo, compiler or linker work.
An explicitly bound local loader may choose the actual frozen checkout and
owned RAM evidence/work paths for that check. Such a preflight does not exercise
the full hosted operational-parent, SDK or native output qualification.

Full mode retains the existing guards: macOS26 ARM64, fresh work/SDK/cache/target
locations; exact pinned v1.44 and analysis-only v1.52 archives; complete native
SDK and Linux target-library checks; authenticated native LLD; locked acquisition
then one offline cold compilation; local-crate fingerprints and unchanged target
flags; before/after source, CORE, stage, registry and tool checks. The maintained
linker validates the program/default scripts, writes a private checked copy,
forwards it to the real native LLD and removes it after linking. The controller
retains frozen script/helper bytes, link receipt/map and native LLD identity;
it does not claim that removed temporary bytes are separately retained.

Both raw ELF outputs, full logs, source/workspace archives, provenance receipts
and all1,035 official score rows are uploaded, including unresolved rows and
partial failures. The explicit historical scorer baseline remains a comparison
input; current counts and bytes come only from this actual new source build.
No score is assumed from an upstream description or from the old FAF result.

This operational preparation has not run natively. Root owns publication and
one control dispatch after independent review. Only after its actual successful
control is admitted may a separate, same-source filtered LLVM capture be
prepared/authorized. That diagnostic must preserve its own outcome and qualify
complete stripped-code/section/score identity against this exact control;
full unstripped hash equality is recorded separately, not assumed from emitting
IR. No current IR, candidate, source gain, runtime result or whole-original
identity follows from this preflight.
