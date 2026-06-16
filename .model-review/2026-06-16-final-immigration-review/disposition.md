# Final immigration review disposition

**Packet:** `.model-review/2026-06-16-final-immigration-review/`
**Date:** 2026-06-16

## Accepted and patched

1. **Mexico illustrative lifetime band invalid.**
   `research/immigration-mexico-npv-population-synthesis-2026-06-15.md` no longer exports `-$37k to +$28k`; the rows are non-additive layer checks until same-universe school, legal-status allocation, overlap, rate/horizon, and price-base choices are explicit.

2. **Fiscal/generator route labels stale.**
   `research/immigration-lifetime-fiscal-generators.md` now uses rounds A-S, scopes the `$1,519` row to narrow `mexico_origin`, and marks the interim `$771` school retrodiction withheld.

3. **Legacy synthesis routes stale.**
   `research/immigration-claims-evolution-ledger-2026-04-23.md`, `research/immigration-INDEX.md`, and `CYCLE.md` now route through the June delta/fixes and carry E-Verify CI/MDE and static-TWFE caveats.

4. **Loop ownership conflicted.**
   `research/immigration-knowledge-delta-agent-loop-2026-06-16.md` is now the canonical umbrella loop; `research/immigration-thesis-generator-audit-2026-06-16.md`, the cookbook, and the sweep protocol are sub-procedures.

5. **Provenance tags drifted.**
   `notes/provenance-tags.md` is now the local vocabulary reference, and loop docs point to it instead of re-listing divergent tag sets.

6. **Staged CSV mirror stale.**
   `infra/immigration-fiscal/derived/stage3_proto/three_layer_annual_2023.csv` was synced to the withheld-origin build output. Ignored local `sources/.../stage3_proto` mirrors were synced too.

## Deferred explicitly

1. **Generator lifecycle state.**
   Still manual. Do not automate yield-based parking/retirement until a sidecar or DuckDB table records fired/adopted/dry/parked/adoption_judge state.

2. **Full E-Verify robustness.**
   Static TWFE remains design-dependent. Heterogeneity-robust staggered-DiD is an unresolved analysis task, not a prose cleanup.
