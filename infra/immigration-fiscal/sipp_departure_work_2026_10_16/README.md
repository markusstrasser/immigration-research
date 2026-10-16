# SIPP remaining-adult work around a household departure

**Verdict:** Internally validated departures support a bounded descriptive
before/after analysis. No deportation identifier or causal identification is
supplied. See the [memo](../../../research/immigration-sipp-departure-work-2026-10-16.md)
for estimates and scope; [protocol](protocol.md) records choices before outcomes.

## Inputs and reproduction

From repository root:

```sh
sh infra/immigration-fiscal/sipp_departure_work_2026_10_16/run_all.sh
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/sipp_departure_work_2026_10_16 "sh {lane}/run_all.sh"
```

Requires the existing pandas, numpy, pyarrow and pytest environment; the figure
command explicitly supplies matplotlib through `uv --with`.
Original public inputs are the 2025 SIPP `pu2025_csv.zip`, `rw2025_csv.zip`, schema,
dictionary and guide; hashes, authoritative URLs and selected definitions are in
`derived/input_receipt.json`, `derived/replicate_receipt.json`,
`derived/schema.json`, `definitions.md` and the preceding audit's
`notes/v9-household-response-evidence-2026-10-16/data/source_receipts.json`.
The schema currently lives at the pinned original location
`.scratch/clarity-next-20260905/admission/pu2025_schema.json`; a missing or altered
source fails loudly. Raw records are never overwritten. The official schema
URL is https://www2.census.gov/programs-surveys/sipp/data/datasets/2025/pu2025_schema.json.

Microdata extracts, identified event keys, intermediate weights and receipts
stay in ignored `_cache/`. Tracked `derived/` files contain aggregate summaries
and variable definitions only. The PNG/PDF are generated, ignored standalone
artifacts; the existing fiscal figures page is untouched.

## Files and interpretation

- `extract.py`: verifies archive/schema hashes and writes selected person-months.
- `components.py`, `component_definitions.json`: streams the original archive
  to count visible component allocations; aggregate recode flag 9 is not a
  reported-value flag.
- `events.py`: reconciles identities, universe, residence spells and rosters;
  keeps the first eligible event per focal adult separately for each route.
- `measure.py`: source-defined zeros, balanced outcome-specific panels,
  cluster-bootstrap intervals and December Fay replicate calculations.
- `benchmark.py`: supported calendar/baseline-standardized descriptive
  comparisons; no causal claim. Original-sample-unit Poisson bootstrap handles
  repeated control anchors and shared event/control sample units.
- `artifacts.py`: full-sample influence diagnostics and trajectory figure.
- `test_measurement.py`: synthetic edge cases and missing/support failures.
- `definitions.md`, `event_validation.md`: independent original-source and
  event checks, with covered/skipped scope. `numerical_verification.md` records
  the independent reproduction of principal estimates.
- `review.md`: deterministic checks, code-review repairs and the complete
  Gemini/Astra claim-review dispositions.

Main windows are t−3…t−1 versus t…t+2; ages18–64 are defined before departure.
Both primary routes retain later returns and focal moves. A persistent subset
is a separate selected-cohort sensitivity. Type-2 identity is validated within
each focal's within-year roster only; no cross-focal departed-person total is
asserted, and routes are not pooled. Positive survey weights define the weighted
subset; 18 December records lacking replicate records have no positive full
weight, and every positive-weight record matches the replicate file.

Reported intervals omit event misclassification, unknown movers, retrospective
measurement error, incomplete lineage/relationship information and causal
confounding. Small subgroup bootstrap intervals can collapse when all observed
changes are equal; this is not evidence of population certainty. No multiple-
comparison-adjusted discovery claim is made. Every calculated specification is
retained in CSV, including a positive tracked-earnings benchmark contrast.
