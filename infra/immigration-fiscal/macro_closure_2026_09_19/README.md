# National fiscal reconciliation and observed 2024 finance refresh

**Verdict:** The expanded account is partial. This lane reconciles explicit
national accounting boundaries, retains unallocated differences, updates the
available state/local inputs, and separates attribution from budget response.
See the [calculation memo](../../../research/immigration-macro-reconciliation-2026-09-19.md).

## Reproduce

```sh
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project \
  --with pandas --with numpy --with openpyxl \
  python3 infra/immigration-fiscal/macro_closure_2026_09_19/builder.py
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project \
  --with pandas --with numpy --with openpyxl \
  python3 -m unittest discover -s infra/immigration-fiscal/macro_closure_2026_09_19
```

Canonical ignored CPS/MEPS/profile inputs, the pinned BEA workbook and local
population file are prerequisites. `--source-root`, `--bea`, `--census-cache`
and `--out` override locations, not source versions. For an empty Census cache,
set the existing `CENSUS_API_KEY` and run `acquire_finance.py`; it writes public
URLs and hashes without credentials. Review any source revision before changing
the tracked `census_sources.json`; the builder fails on hash drift.

## Measurement contracts

- BEA tables 3.1/3.2/3.3, August 26, 2026 vintage, calendar 2024: header-selected
  year, millions converted to billions, federal/state grants netted once.
  Current saving differs from net borrowing by capital-account adjustments.
- BEA 3.18B exports its separate federal fiscal-year bridge. It has a different
  historical revision from the stored OMB FY2027 totals. BEA 3.19 currently ends
  at 2023; there is no substituted numeric cell pretending to be its 2024 year.
- Census `govslocalfin`, government type001, FY2022/2024, state/DC and US controls.
  Amounts are thousands of dollars. Repeated API predicate columns must agree.
  Omitted state cells become zero at published precision only when nonnegative
  reported cells exhaust the independent national control within $51,000.
  Flagged amounts fail. Original CV/flag fields remain archived; their uncertainty
  is not propagated into these point calculations.
- Census2024 G = LF0103 minus LF0107/0123/0129/0132/0159 minus fees LF0048–0056.
  P = LF0109 + LF0131 + LF0161 − LF0115. These retain the original service/capital
  definitions and overlap limitations. Denominators use POPESTIMATE2024, excluding
  separately reported Puerto Rico; all 51 jurisdictions must match finance.
- C and X retain original incidence, replacing their aggregate pools with federal
  receipts plus combined state/local LF0024 corporate tax and LF0012 selective
  sales tax. The earlier source covered states only. Other fiscal components
  and mapped federal grant deductions stay fixed.
- Census source refresh is a separate, versioned account. It does not silently
  change older age-profile, lifetime or benefit-threshold releases.

## Outputs and gates

`account_components/totals`, `national_bridge`, `receipt_diagnostics` and
`policy_arithmetic` reproduce the earlier release. `finance_vintage_effects`
and `finance_vintage_totals` identify each change. Corresponding `updated_*`
outputs carry refreshed gross fees, receipts, spending and the BEA differences.
`fiscal_year_comparators` keeps the Census general-finance/OMB comparator separate
from NIPA. `F_attribution` records an optional average-cost allocation, not savings.
`official_cells` preserves source line labels; `audit.json` fingerprints every
source and output and records accounting/conservation checks.

The policy grid computes `q * gross attributed spending − all attributed receipts`.
No estimated policy is assigned a value of q. In particular, fees are lost even
when q=0; symmetric fee netting is appropriate only for the static BEA presentation.

Regression gates cover the observed duplicate-header and Puerto Rico universe
failures, source year/units/missing cells, duplicate source lines, grant double
netting, current/capital confusion and the fee-loss endpoint. Full builds verify
the disjoint population partition and original canonical group/national totals.
The unresolved national residual is never mechanically allocated by ethnicity.
