# S5 borrowed selected-key diagnostic

One normal cold build of genuine source `bb4a6fcaca179a8a49882a6acac3b503a1206882`, a direct child of frozen D421 `d4219123cf0fbbefcfc7e77450efeda6684b812b`. The sole program delta is five lines of admin_cto.rs: validate returns a borrowed selected K/C/N key, selecting C only after the required incoming-N guards and before the unchanged fee checks; the caller copies the validated key and preserves distinct incoming N for sharing.

This is a bounded mechanism hypothesis, not an inferred original private Rust ABI or recovered lifetime. Standard v1.44/macOS26 source recipe, unchanged current CORE279, full SDK guards and cold target. Controller executable AST differs only in BASE from the qualified D421 control. No flag/layout search, original-byte transplant, padding, IR edit or ownership/signature bypass. Public authorization/account/CPI code unchanged.

All raw and normalized rows must retain D421's 1034/1035 before target measurement; losses reject the source without metric or VM. No-loss must improve the same sealed normalized metric above M2248 before affected runtime validation or a source PR. This diagnostic is frozen to D421; promotion requires a fresh current-main build. The root source/preparation reviews are not independent agent reviews. Prior failed S1-S4/H1 and feephi results remain retained.
