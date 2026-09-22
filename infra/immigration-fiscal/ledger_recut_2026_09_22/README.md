# Practitioner recut of the ledger arms grid — September 22, 2026

Takes the pinned September 19 build of
[`ledger_absolute_2026_09_17`](../ledger_absolute_2026_09_17/README.md) and asks which of
its switch combinations a budget modeler would run, prices the switches the grid does
not hold, and reports the resulting hulls next to the full design hull. Everything is a
linear combination of that lane's published per-item replicate vectors; no microdata is
touched and no fingerprinted upstream script is edited.

Object: Mexican-origin union (40.9m civilian household residents), income-year 2024,
household-shared allocation, expanded partial account, items D and P on. Not the
September 20 complete account, not the generation-vs-white gaps, not the later
finance-refresh or enrollment-correction vintages.

## Reproduce

From the repository root:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
  infra/immigration-fiscal/ledger_recut_2026_09_22/recut.py
uv run --no-project python3 -m pytest infra/immigration-fiscal/ledger_recut_2026_09_22/ -q
```

Inputs, all hashed into `derived/audit.json` and re-checked by the tests:

- `ledger_absolute_2026_09_17/derived/`: `replicates.npz` (ignored, present after a ledger
  build), `arms_matrix.csv`, `marginality_curve.csv`, `items_by_group.csv`, `audit.json`,
  `age_profiles.csv`, `age_profile_components.csv`; `params/params.json` for the OMB
  function amounts behind item F.
- `scaling_test_2026_09_20/derived/state/estimates.csv` (cross-state function
  elasticities, year effects, all years) and `derived/school_estimates.csv`
  (within-district school elasticities).
- `ledger_residual_agg_2026_09_16/_cache/22slsstab1.xlsx` (ignored): the 2022 Census of
  Governments table the ledger's item G is built from, read here for G's national
  composition by function.

`--out-dir DIR` writes elsewhere so a rerun cannot clobber the published output.

## What it computes

1. **Reproduction gates.** All 63 admissible `arms_matrix.csv` cells and their standard
   errors, the 21-point marginality curve and its break-even m\*, rebuilt from the
   replicate vectors to 1e-6 $bn. The grid has 63 cells, not 144, because the builder
   skips E ≠ zero unless R = all zero (the enforcement appropriation sits inside OMB
   function 750, which R charges per capita).
2. **Switch moves** (`derived/switch_moves.csv`): each arm against the central cell, with
   the replicate SE of the difference, its source, the class of modeler that runs it, the
   side it moves the balance to, and whether it enters the practitioner set. Grid arms are
   differences of grid cells. Added here, on the published vectors:
   - enforcement charged to Mexico-born noncitizens *and* removed from the per-capita
     justice charge (netted, so it does not double count);
   - item F split into defense net of TRICARE, net interest and general government by the
     OMB function amounts, and general government at the cross-state administration
     elasticity;
   - item G at cross-state function elasticities (police, fire, highways, parks,
     libraries, administration; other functions held at 1), using G's national
     composition from Census lines 76–112; and state-local interest on general debt at
     zero, the convention item F already applies to federal interest;
   - K and D at the within-district school elasticity;
   - corporate tax borne by consumers (C national × the union's consumption share from
     item X's consumption-proxy arm).
3. **Named cells and hulls** (`derived/named_cells.csv`, `derived/hulls.csv`): central,
   practitioner pessimistic and optimistic, the disclosed stretches, the dropped corners,
   and the second object (F per capita). `derived/gross_flows.csv` carries the receipts
   and outlays behind the net and what 20% of each would be.

Standard errors follow the ledger's rule, 4/160 × Σ(replicate − full)², on the same 160
replicate weights, so cell and difference SEs are exact for the survey part. They say
nothing about the conventions.

## What this does not settle

- The hulls are convention hulls, not confidence intervals. The practitioner set is a
  judgment about which arms a named class of modeler runs; the memo states each.
- The cross-state elasticities are descriptive size gradients that the
  [scaling decision](../../../decisions/2026-09-20-service-scaling-calibration.md) holds as
  sensitivities, not identified responses. G's composition is national, not the union's
  state mix.
- Base school current spending (−$115.8bn for the union) is not on the ledger's dial, so a
  CBO-type school response cannot be applied to it here; the point-only stretch cell shows
  what it would add. Per-function responses on the whole account live in
  `full_account_2026_09_20`.
- The enforcement-netted cell and the F split are computed on published vectors; the
  builder's admissibility rule and item definitions are unchanged.
