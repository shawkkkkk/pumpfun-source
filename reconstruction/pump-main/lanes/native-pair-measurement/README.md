# One native control/candidate measurement

Operational fork-only driver derived from qualified single control
`e7ed2474df380c81d55b822515055c953f0947117d28ef5bb783355d4f415c2e`.
This directory does not propose a Rust change. No pair is selected or dispatched
by adding these files. Root review and two frozen commit IDs are required.

The operational checkout must retain the exact source-base harness, toolchain,
original and baseline files. Start it from the chosen source-base commit and
add only these operational files. The candidate must be a direct, single-parent
child of that base, modifying exactly one existing UTF-8 Rust file, selected
explicitly from `buy_v2.rs`, `creator/admin_cto.rs`, or `multi_hop_curve_swap.rs`.

Preflight, with real rsync available, uses new work/output directories:

```sh
python3 -B reconstruction/pump-main/lanes/native-pair-measurement/measure_pair.py \
  --source-base "$M" --candidate "$C" \
  --changed-source-path programs/pump/src/buy_v2.rs \
  --preflight-only --work /tmp/pump-pair-preflight-work \
  --output /tmp/pump-pair-preflight-evidence
```

`M` and `C` must already be the reviewed full lowercase 40-hex commit IDs.
Preflight authenticates the full Git delta, both source vectors and the base
tooling. It exports byte/mode-exact source trees, runs the unchanged real stager,
checks the builder's source inventory, and retains separate source/workspace
archives. It never installs an SDK, bootstraps a toolchain, runs Cargo, compiles,
scores or dispatches anything.

Full mode is for native macOS 26 arm64. The reviewed workflow installs the
qualified v1.44 compiler SDK once, authenticates the complete SDK and Linux
SBPF libraries, and reuses that unchanged installation for both builds. The
unchanged v1.52 analysis tool is installed once separately. Neither target is
seeded or reused: control and candidate have separate initially absent targets.
Only the locked registry source cache is shared, with complete before/after
hashes. Both local crates must visibly compile in each retained build log.

Each image has its own Git source receipt, actual builder receipt, compiled
workspace archive, build result/log, Cargo fingerprints, tool/registry hashes,
ELFs and full official 1035-window score. Candidate scoring uses the fresh
control score; the unchanged `compare_scores.py` then checks every normalized
and raw membership, inventory key and size. A loss retains both images and a
rejected comparison and exits nonzero. Existing output paths are never reused.

The fixed compiler recipe and scorer are not changed. SDK/compiler/profile
sweeps, multiple candidates, VM tests and automatic promotion are out of scope.
This is a driver, not a successful measurement, equivalence receipt or source
recovery. No M/C pair or native execution is claimed until actual artifacts exist.

## Current link-order input closure

This v2 uses the already registered fork workflow path
`.github/workflows/qualify-pump-macos-v144.yml`; the old three-file prototype
remains at `5dfb3427525d44db4ac5c7b266d5e1122142aac7`. Apply these operations
only on the exact reviewed M source tree. No M/C pair or build is fabricated by
this driver. The real direct-child C and single allowed Rust delta are required.

Input counts are derived from exact Git trees, never fixed to an older count.
For reviewed M `fb25fce02f4845dbf06c1639ec2144125845a0ef`, the current closure
is112 program files,113 staged workspace files,155 maintained core members.
Both M and C must preserve the same `link/ordered.ld` and all maintained hooks.
Pure preflight runs `check_script` only, retaining exact script/default/hook
bytes, modes, Git IDs and admitted selector counts; it never calls `configure`.

Full mode authenticates the one native hybrid host rust-lld against the full
native v1.44 SDK inventory, retaining its resolved path/hash/size/mode in both
tool profiles. Each actual build must supply its real `build.link_order`,
`link-receipt.json`, and nonempty `link.map`, bound to the frozen program script,
default script, selector counts and that exact native LLD. Raw receipts/maps
remain beside the two output ELFs; no linker, source, script or compiler flag
variant is attempted. Candidate acceptance is every normalized/raw window
against the fresh M census, including domain and lengths; no numeric match
floor from6a/2b is substituted.
