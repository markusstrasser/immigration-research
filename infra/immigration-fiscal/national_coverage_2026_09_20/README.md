# National fiscal coverage decomposition

**Verdict:** The national residual is now separated into named receipt categories
and explicit spending conventions. This diagnoses coverage; it does not assign
the remainder to Mexican-origin residents or produce a complete welfare balance.

```sh
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project \
  --with pandas --with numpy --with openpyxl \
  python3 infra/immigration-fiscal/national_coverage_2026_09_20/builder.py
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project \
  --with pandas --with numpy --with openpyxl python3 -m unittest discover \
  -s infra/immigration-fiscal/national_coverage_2026_09_20
```

Requires the verified outputs of `macro_closure_2026_09_19` and
`admin_tax_checks_2026_09_19`, their original source dependencies, and the pinned
BEA section 3 workbook. `--source-root`, `--bea` and `--out` change locations.
An upstream output or dependency that differs from its audit fails rather than
silently loading a stale calculation. No download or calibration occurs here.

`receipt_crosswalk.csv` exhausts the current receipt boundary using BEA tables
3.1, 3.4, 3.5 and 3.6, August 26, 2026 vintage, calendar 2024, billions of dollars.
Every modeled receipt is owned once. Suppressed cells remain unavailable;
required unavailable cells fail. Published rounding has its own row.

`credit_presentation.csv` moves the exact modeled EITC/ACTC amount from negative
revenue to expenditure. Both sides increase equally; the deficit is unchanged.
This does not assert that these two credits exhaust BEA's refundable-credit
category or that all CPS liabilities equal recorded receipts.

`spending_conventions.csv` shows how much of the raw spending discrepancy comes
from the model's explicit zero allocation of F (defense, federal net interest and
general government). Seven other zeroed federal functions are exported separately
as **gross pools only**: their grants can finance state/local services already
counted in G/P, so they cannot reduce the residual before ownership is resolved.
Source pools remain FY2024 OMB amounts, with the existing household/resident ratio.
This waterfall is an attribution diagnostic, **not** a completed current-account
crosswalk. In particular, adding investment to NIPA current expenditure requires
subtracting consumption of fixed capital; the source capital identities are
checked, but not fabricated into a model correction.

The remaining differences retain their actual status: coverage, fiscal/calendar
timing, cash/accrual, survey population and incidence remain mixed. No ethnic
rescaling is performed. Source hashes and exported table hashes are in
`derived/audit.json`; raw and derived input data remain read-only.
