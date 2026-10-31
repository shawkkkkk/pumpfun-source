# Exact measured-negative C1 compiler capture

This operational branch requests one diagnostic build of source commit
`0fc50efbc599fa1e025169c8db06fceb25c9c192`, whose parent is frozen
`39eb377aa6c6ce4aacff273aa13732abb0c0078a`. It changes no program, CORE,
compiler recipe, optimization threshold or IR. The measured source implements
the non-leaf `validate -> Result<Option<Pubkey>>` carrier previously suggested
in w13a42, while preserving the existing fee-edge volatile read.

The original normal C1 run
[41162533835](https://github.com/shawkkkkk/pumpfun-source/actions/runs/41162533835)
failed its no-loss guard: 1,034 normalized / 347 raw matches, with 687 raw losses
against the admitted 39eb control. Its target grew from 27,400 to 27,616 bytes.
That failure and all original receipts remain preserved. This diagnostic keeps
the same official scorer, exact 39eb score baseline and unchanged no-loss guard.
Successful trace collection cannot make the source candidate pass.

The second reference is the exact 45-member normal C1 artifact `13027638017`,
ZIP SHA256 `081b9de25c3c6ed446b3b3d610d08f8d58a0a6e88f7fea16b9aab0a3fc341477`.
It is used only to admit the diagnostic trace against the already measured C1
code. The controller separately authenticates the original 43-member 39eb
control from run `41159607118`, artifact `13026402898`. Every extracted member
size/hash is pinned; hosted `download-artifact` supplies extracted members,
so the original transport ZIP hashes are recorded rather than rehashed there.

The unchanged-source guards admit all 141 program files, 236 CORE files and the
maintained 142-file standalone-to-workspace projection. The selected source
SHA256 is `0a6f3cd63c65df63915d912d09e69b3d163628d3cb70b1212aeca021ea32d3f2`.
The four OPS files must be a direct child of C1. The controller retains the full
SDK/archive/inventory/target-library/native-LLD checks, locked fetch, cold target,
local-crate fingerprints, registry/tool/source before-and-after checks, private
link-script/map admission and complete 1,035-window official score.

The helper changes only the maintained single root Cargo command from `build`
to `rustc --lib -- --emit=link,llvm-ir`, with the same fixed target-function
filter and print arguments previously used for 39eb:

```
-filter-print-funcs=_ZN14pump_recovered9admin_cto7execute17h3bd6d7f34f2e30d7E
-print-before=jump-threading
-print-after=jump-threading
-print-after=finalize-isel
-print-before=greedy
-print-after=greedy
-print-after=virtregrewriter
-print-after=block-placement
```

These request two ordered before/after JumpThreading pairs and five complete
machine-function stages, plus optimized LLVM IR. The parser narrowly accepts
the actual retained 39eb heading `; *** IR Dump Before JumpThreadingPass on
<exact target symbol> ***` and its `After` partner, as well as the already
admitted registered pass-ID forms. The original strict 39eb diagnostic failure
is untouched. No pass/flag search, `opt`, `llc`, source or IR edit is performed.

The raw build log, every available root `.ll`, raw dump sections and exact target
IR extents are retained even on a false build return or exception. Source/work/
output admission runs before helper writes. The hook checks the full frozen
Cargo argv, cwd, compiler/wrapper/target/flags, forwards every original positional
and keyword argument, and restores the original function in `finally`.

`DIAGNOSTIC-COMPARISON.json` independently requires complete stripped ELF bytes
equal to the normal C1 strip
`ce58f0f14b30ef758f97904a5ceb7d6f0e47c41b9068c5d85764846cbbe364b3`, all
non-symbol section payloads, semantic function symbols and symbol numeric fields
equal, and every saved official score row equal to normal C1. Only local OBJECT
symbol names may differ; full unstripped hashes and name differences are recorded
separately. All requested complete stages and one actual compiler call are also
required. This report is written before the unchanged source no-loss guard;
the expected negative guard still raises and the workflow uploads with `always()`.

If an earlier source, SDK, compiler, link, fingerprint or scoring guard fails,
the workflow stops there and retains available evidence; a partial trace is not
qualified. There is one authorized native capture, with no retry or fallback.
Preparation includes genuine no-SDK source/stage/both-reference admission and
read-only replay of the actual 39eb raw heading formats. Pure hook/path checks
are identified separately and do not prove native C1 IR or code equality.

This is a historical causal trace for the measured C1 negative, intended to
locate the early payload copies and PHIs relative to Result projection and
caller mutation. It is not another source candidate, source progress, latest-main
qualification, runtime/VM result or whole-original equivalence claim. Main had
advanced to `95a64ba7524555bf24927f85852073dde085ae5a` at the last packet intake;
neither that source nor later sources are qualified by this frozen measurement.
