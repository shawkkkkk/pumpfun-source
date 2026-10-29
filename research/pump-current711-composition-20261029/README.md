# Qualified three-file composition measurement

This is a separately named composition controller, based on the maintained711
source (`c0e29e2d` stripped / `dd73afe7` symbols). It does not change the historical
673 controls or their one-file candidate policy. The current65 source and archived
published65 both match the711 input JSON; only the per-hop734 file differs from
the earlier673 source. The portable builder remains byte-identical `c7d215a9`.

The root-reviewed plan is retained byte-for-byte under `plan`: PLAN SHA256
`56bdec77d01ddee5d74b78139979308e7626abff59410ad798bf8fad9c0646bd`,
SEAL `d8bf487dec6fcb60937e2f63f0f5b42a1e7b8068d151a4e85091b390b480da8c`,
and MANIFESTS `58429a8b4e17b81137a54d86daed5a571119ec8b135f9567260cf9c75d7b5d61`.
Its287 sealed files were checked before copying. The plan explicitly binds all65
standalone and66 compiler inputs. Current main563 and the publishedf57 source
have equal65 inputs. Exactly these three qualified source files change:

| File | Qualified after SHA-256 prefix | Source unit |
| --- | --- | --- |
| `src/creator/admin_cto.rs` | `5203d20c2e63be73` | #730 |
| `src/sweep_fees.rs` | `3d3363ddd7713999` | #737 |
| `src/multi_hop_curve_swap.rs` | `5871a2cf35ebe0db` | #731 |

All other62 inputs, Cargo files, SDK tools,25 target-library files plus the empty
`self-contained` directory, physical source wrapper and all1827 recorded SDK
Rust-library file hashes remain fixed. Each component's actual source/build
binding and finite qualification remain attributed to its owning source packet;
none is relabelled as a composed result.

Run `python3 -B scripts/pump_current711_composition_macos.py --inspect` to verify
the source maps, current control files, SDK pins and sealed plan without network
access or compilation. Native execution requires Darwin arm64 and creates a fresh
target. The derived cold builder changes only its terminal demand that composition
outputs equal current control: the equality remains recorded. No expected
composition output hash is supplied. Both local crates must actually compile.

The controller reuses the byte-identical I/O helper from #720; it does not call
its historical source inspector or relax its one-file policy. SDKs and locked
registry archives are downloaded and authenticated as in the qualified recipe.
All original compiler/profile/registry/source before-and-after checks remain.
The exact source65 archive, compiled66 archive, sealed plan, raw ELFs, SDK/registry
bindings, command logs and visible adapter diff are retained by the workflow.

Root released exactly one ordinary composition build after individual component
qualification and plan review. This packet is preparation until an actual RESULT
exists. No maintained-source promotion follows from compilation: the official
full1035 census, full44-suite and strict/affected signed cases, actual caller/data
and Location checks, and any required fresh repeat must qualify the measured
image first. No flags, layout, source variants or binary patching are permitted.
