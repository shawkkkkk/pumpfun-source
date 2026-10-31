# S3 full-settings Result measurement against actual 13fe control

This operational proposal measures source commit
65f0162a3dcd381df0f831082dd6732c9af4ab78, tree
f36a4e0b3c02822750ce5c41529b7a75e16f79c0, sole parent
13fe4536be64d8c5c10f8905e9d2236f423ac4f4. Only
programs/pump/src/creator/admin_cto.rs changes: Gitblob
74827621b1bc966466a0d39d88ca76aa5e5c91e9, SHA256
32d4d71065f96e0d24f65ead880974a4e4cc95919ec2ef0bc113a0d536e3d7b9,
21896 bytes and 772 lines. The candidate is a genuine Git checkout. No source
archive or parent overlay supplies its program files.

S3 changes the private validator's actual success aggregate. It accepts the
already computed shared boolean and returns
Result<(bool,bool,Pubkey,Option<Option<Pubkey>>,bool,bool)> for holder, cashback,
target, sharing_update, collect_old and skip. Creator and fee checks remain
inside that helper. After validating a nonholder new key, shared selects the
owned creator snapshot before fee checks; otherwise the target is the new key.
The post-fee flags tree is inside the helper before its combined Ok. The caller
projects the combined settings once through validate(...)?; the existing outer
Ok carry remains. Sharing payload uses the original new option, not the selected
creator target. The public execute signature, creator/fee error coordinates,
both volatile reads at334/338, prepare339 suffix and later source are preserved.

The source proposal manifest is
42a11e20671e4c354813f0b45de7f0f5521b8948cd8c683919d3ff0c1b1ad0a5;
independent semantic review is
d38a892b1ec4785fca34a4a62f7d33bfba7f398e1449be6b4b287dcf413e6753.
These are static source reviews. A larger private Result aggregate is a real
source change, not an inert wrapper. Its emitted ABI, register/copy shape,
inlining, cold error placement, sweep behavior and score are unmeasured. No
native outcome or gain is promised, and no inline attribute, size knob or flag
variant is included. Historical S1/S2 negative builds remain separate evidence.

## Frozen source and reference

All141 Git/selected source files bind selected SHA256
9fc3fd3c8e68d85e5bf4fcb2309694974aab3c5aaacab9741a1e0ea25c72a622.
All236 CORE leaves equal actual13fe source. The unchanged maintained staging
helper produces142 workspace files, canonical vector SHA256
8ecb6144b71aee05d37cb1bebd4f2b0b3343c7eb88f0a3366d17c4dc0381e9db.
The unchanged link script has555 text selectors. Git modes/blobs/bytes and
source/stage identities are checked before/after; Python bytecode is disabled.

The reference is actual normal run41170683278, artifact13031166975, operational
commit1f061a9adb2217b1cf37c26dacfab66fe7e2205b, source13fe4536be64d8c5c10f8905e9d2236f423ac4f4.
Its43-member ZIP is2539578 bytes, SHA256
875edcd6e9ebb7e5b8fb2495d0008e723762b1f0251a02e038881fb56749fa92.
Unstripped SHA256
cec841bd60cc002213829e3149e7c170dbb7f5bbc47a9887cef1ab7e0193319e;
stripped SHA256
fe099633c59f1a409f66d7b7bd6ce702580116c92ac24cb26842a351f3ee459e.
Reference selected source SHA256 is
ba203d5c8b0cda5ab3bb6eec65266a992331b7a8a361b9977a3d2ab474b11fe2.
Root admitted actual source/archive/cold/build/link bindings and independently
ran the full official1035-row score once:1034 normalized and1034 raw matches.
Its separate actual signed363 comparison passed, with all726 saved transactions
independently signature/nonsigner checked. That finite reference result does
not qualify S3 and does not establish whole-program byte identity.

Every actual reference member's bytes/size/hash is pinned. The hosted workflow
downloads that exact artifact; the controller authenticates the43-member
domain, source/cold/CORE and complete score before SDK work. The outer ZIP
digest was separately verified during acquisition and is recorded, not
purportedly rehashed by the hosted job. Reference archives are retained
evidence only and are never candidate source transplants.

## One normal native candidate, released separately

The operational Git commit must be one direct child of S3 and change only:

- .github/workflows/qualify-pump-macos-v144.yml
- reconstruction/pump-main/lanes/current-native-control/pump_current_control.py
- reconstruction/pump-main/lanes/current-native-control/README.md

The candidate framework's14 helpers, LinkAudit class and full comparison
function are unchanged from the prior normal candidate framework. Only
candidate/reference pins and descriptive labels are adapted. Full mode requires
native macOS26 arm64 and preserves pinned SDK archives/inventories/target
libraries, authenticated native LLD, fresh cache/work/target, locked acquisition,
identity recipe/flags, registry/tool/source/CORE/stage guards, linker/map
admission and actual ELF hashes. There are no IR dumps, optimizer runs, source
overlays or automatic repairs. Root alone publishes and dispatches after review.

The actual13fe score.json is the baseline. The official scorer retains all1035
candidate rows; CANDIDATE-COMPARISON.json saves every changed row and complete
gains/losses before any raw or normalized loss rejection. Failures retain full
score/comparison/ELFs/source/compiler/provenance and FAILURE.json. Build success
does not accept source. A useful no-loss result still needs raw-target review
and an actual separately released signed363 comparison before a source PR.

The real preflight-only call authenticates source/CORE, actual reference43 and
full baseline, candidate selected-source pin, maintained stage142 and pure link
admission, then returns before SDK/bootstrap/Cargo/compiler/scorer/VM work.
Local path binding does not exercise hosted direct-parent operational-file
admission or native SDK/output checks. Its actual receipt is retained separately;
this document alone does not claim execution.
