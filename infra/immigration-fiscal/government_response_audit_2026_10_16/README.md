# V9 general-government response audit

One link: population -> long-run general-public-services cost. Frozen candidate:
`a24d2468` (round-six v9). Population, accounting basis, other responses and the
capital-return rate stay fixed. The audit does not reopen the school result.

## Decision rule written before new estimates

The candidate link transports cross-state administration spending scale into a
national counterfactual. The existing within-state and county-IV estimates are
too imprecise to select zero or proportional response; their completed results
will be checked and retained, not rerun as a new discovery. Selection against
the remaining large candidates uses their current fiscal exposure and evidence.

Materiality: a defensible revision capable of moving either annual endpoint by
$5bn, or a demonstrated failure of the source-to-parameter bridge. Apply the
same standard to upward and downward revisions. A regression association alone
does not identify population removal; do not manufacture a finding.

Original-data checks:

1. Independently parse the original Census FY2022 state/local finance Table 1
   and population file. Reconstruct administration scale and the BEA component
   mix, including the distinction between the judicial-inclusive source basket
   and the destination's general-public-services functions. Check national sums,
   field labels, units and input hashes before interpreting estimates.
2. Use one independent staffing/payroll source, Census's public employment
   survey/census, if its function definitions permit a defensible match. Compare
   FTE scale, payroll scale and payroll per FTE to distinguish workforce from
   input-price composition. Do not equate FTE with output or service quality.
3. Keep equal-state and population-weighted fits, with and without Alaska/Hawaii;
   exclude DC in the primary comparison and disclose coverage. Heteroskedastic
   robust uncertainty is descriptive; it excludes causal/transport uncertainty.
4. Price the single response through the full frozen v9, including applicable
   post-engine and capital components. Reproduce the central case first. Price
   only interpretable alternatives and explicit bounds, not every fitted slope.

The memo follows the calculations. Original inputs are read-only; every computed
specification and failed source match is retained. A null audit is a valid result.

## Source-definition amendment, before staffing fits

The original employment methodology says FTE has been modeled since 2019.
Full-time employee counts and their March payroll therefore became primary;
FTE remains a disclosed secondary check. Buildings cannot be isolated in the
published employment functions, so the staffing baskets are finance alone and
finance plus other government administration. Neither is labeled the full BEA
general-public-services pool.

## Reproduction

Run from the main checkout; when executing this lane from a worktree, pass its
absolute script path and `--data-root /Users/alien/Projects/immigration-research`.

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl --with scipy python3 infra/immigration-fiscal/government_response_audit_2026_10_16/reproduce.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl --with scipy --with statsmodels --with pytest python3 -m pytest infra/immigration-fiscal/government_response_audit_2026_10_16/ -q
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/government_response_audit_2026_10_16 "uv run --no-project --with openpyxl --with scipy python3 {lane}/reproduce.py" "uv run --no-project --with openpyxl --with scipy --with statsmodels --with pytest python3 -m pytest {lane}/test_raw_finance.py {lane}/test_employment.py -q"
```

`reproduce.py` exports the committed case into a temporary checkout and copies
only hash-verified ignored principal inputs through the first audit's helper.
It reads older pinned Git objects through a read-only object-store alternate.
It changes no model source or scenario in the production case. The model's
declared vendored stack input is included in the fiscal source-hash receipt.

`raw_finance.py` independently parses original Census and BEA workbook cells,
population rows and labels. `employment.py` reads the original published Census
API extracts, validates duplicate fields and national aggregates, and uses the
same audited HC3 estimator. The source extracts and acquisition record are in
`sources/immigration-fiscal/data/external/stage3/census/aspep_2022/`.

`price.cjs` changes the response of general public services, its parent-linked
completion spending, and its capital return. It explicitly changes the active
completion capital selectors, then transports the current coverage and signed
count-item parts. Item20 revalues engine and reporter capital inside the full
evaluator; coverage/count capital is already at the current rate and receives
no second rate multiplier. The dataset-audit row8 residual and income-security
administration are different calibrations and remain fixed. Both accounting
bases and both methods reselect their endpoints.

All finance and staffing specifications are retained in CSVs. The fiscal table
prices only the primary 50-state basket/weight alternatives plus explicit zero,
half and proportional responses; half is an arithmetic check. Lower48, DC and
modeled FTE are robustness descriptions, not additional fiscal candidates.

## External checks and limits

Published national totals, workbook identities, an independent statsmodels
estimator and a clean frozen-case replay constrain the reconstruction. They do
not validate the causal counterfactual. The national-removal response remains
unidentified; the memo's null verdict means no defensible material correction
was established. See the linked memo for the full result and falsifier.

Validation on 2026-10-16: clean committed-case export passed all 777 fiscal
checks; ten source/estimator tests passed; the complete lane replay exited zero
with `IDENTICAL: 21/21 files unchanged`. A separate implementation review traced
native-child, reporter, capital/rate and coverage/count pathways and found no
material defect. Its verdict concerns calculation, not causal identification.

Result: [audit memo](../../../research/immigration-v9-government-response-audit-2026-10-16.md).
