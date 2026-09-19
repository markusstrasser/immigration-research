# Medicaid administrative validation, 2026-09-20

**Verdict:** The executed CY2023 check does not validate the historical 1.5432 Medicaid expansion as a complete contemporary government account. Published institutional care is much smaller than the remaining national gap. The check identifies a denominator correction and substantial exposure/scope differences, but no defensible Mexican-origin spending correction. See [RESULT.md](RESULT.md).

This lane is independent of the canonical fiscal builder. It reconstructs its five age bands × US/not-US birth matching with **MEPS HC-251 (2023) and CPS ASEC 2024 (income/coverage 2023)**, including canonical civilian, infant reference-year exposure and origin-union rules. It does not relabel this as the main model's 2024 result. Medical spending remains a transported expectation: public MEPS has no detailed-origin/state administrative eligibility cells. Negative `AGE23X` records remain in the direct MEPS total and explicit residual age row; canonical donor matching excludes them. No `AGELAST` substitution is made.

## Reproduce

From a project checkout containing this lane. The commands provision the declared dependencies; `--root` points to the checkout holding the existing ignored MEPS/CPS inputs:

```sh
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project python3 \
  infra/immigration-fiscal/health_admin_2026_09_20/acquire.py
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project \
  --with numpy --with pandas --with openpyxl python3 \
  infra/immigration-fiscal/health_admin_2026_09_20/builder.py \
  --root /Users/alien/Projects/immigration-research
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project \
  --with numpy --with pandas --with openpyxl --with pytest python3 -m pytest -q \
  infra/immigration-fiscal/health_admin_2026_09_20/test_builder.py
```

Dependencies: Python 3.11+, numpy, pandas, openpyxl; pytest for tests. `--raw` and `--out` accept alternate locations. Local raw inputs: `sources/immigration-fiscal/data/external/stage3/ahrq/meps/{h251dat.zip,h251su.txt}` and `sources/immigration-fiscal/data/census/cps_asec_2024_march.zip`. Existing parameters and canonical parser are read only. `audit.json` records their hashes, builder hash and every output hash. A failed rebuild removes the prior receipt before writing outputs.

`source_pins.json` contains URLs, POST bodies, byte counts and SHA256 for nine newly staged CMS/Census files (8,224,811 bytes). Acquisition preserves existing raw files and fails on changed content. Raw and derived directories are ignored. This code does not alter a ledger, append institutions or distribute a residual by origin.

## Definitions and limits

- CMS EX.5: CY2023, Medicaid Title XIX, all residence settings, five administrative eligibility groups; member-years are member-months/12. It uses allocated CMS-64 cash payments, excludes CHIP, program administration and DSH, and includes Medicare premiums. [Methodology](https://www.medicaid.gov/state-overviews/scorecard/content/scorecard-rel/PerCapitaExpendDataMethod-2025.pdf).
- MEPS: civilian noninstitutionalized US population; edited `MCDJA23X`–`MCDDE23X` combine Medicaid/SCHIP. The builder retains all survey PSUs for domain variances. Unknown monthly responses are bounded, never zero-filled; none occur in this release. Source-of-payment costs and coverage are not edited to agree perfectly. Capitated services are imputed using service payments, not simply recorded as capitation checks. [HC-251 documentation](https://meps.ahrq.gov/data_files/pufs/h251doc.pdf).
- CPS: `MCAID_CYR` gives none/some/all, not months; some is bounded at 1–11 months. Coverage includes cases with CHIP/other means-tested coverage, as confirmed by the public records. These state intervals are exposure bounds, not sampling intervals. [2024 dictionary](https://www2.census.gov/programs-surveys/cps/datasets/2024/march/asec2024_ddl_pub_full.pdf).
- National CMS eligibility totals are visually transcribed from [2026 Beneficiary Profile, page 15](https://www.medicaid.gov/medicaid/quality-of-care/downloads/beneficiary-profile-2026.pdf). The figure is raster artwork, so text extraction misses its numeric values. It includes PR/Guam/USVI. Category values are rounded; component enrollment/expenditure sums need not equal separately rounded totals. National total per-member-year is calculated from rounded totals; the five category rates are published rates.
- LTSS tables are observed TAF claims/encounter spending, not CMS-64 cash allocations. Their quality ratings differ from EX.5. Subtracting all LTSS is deliberately excessive for a MEPS match because HCBS overlaps. It is neither a precise reconciliation nor a hard bound. The script removes mental-health DSH from its subtraction because EX.5 already excludes DSH.
- EX.2 is **federal fiscal year 2023**, retained solely as a managed-care/CHIP scale diagnostic. The displayed Medicaid categories are $2.506162bn short of its reported total; the discrepancy is saved, not forced into an invented category.

## Output contracts

`cms_state_eligibility_2022_2023.csv`: all 648 observations, including null/no-expansion and quality notes. `cms_national_2023.csv`: six observed/published national rows. `meps_national_2023.csv`: direct spending, coverage and full-design sampling errors; age rows, including unknown/out-of-scope, exhaust the national total. `cps_transport_2023.csv`: US/CA/TX and canonical Mexican-origin union, no group adjustment. `state_comparison_2023.csv`: explicitly unmatched state rate diagnostics. `ltss_2023_observed.csv`, `ltss_2023_ca_tx_quality.csv`, `scope_stresses_2023.csv`: observed state/national LTSS and scope tests. `cms_fy2023_service_spending.csv`, `cms_fy2023_category_closure.csv`: fiscal-year scale and closure checks.

## Acquisition issues resolved or retained

The stale `content/scorecard-release/` methodology URL returned HTTP404; the production app declares `content/scorecard-rel/`, which downloaded successfully. Production app `main-AU5ILMWJ.js` → `chunk-OIJEYANB.js` disclosed dataset IDs; the version endpoint identified ETL3.9.61/data20251205. EX.5 data came from the public production API, not methodology Table III.2 (explicitly contrived). Guessed full-workbook URLs returned404; no data were inferred from them. An unfiltered EX.2 request returned503; a national/year-filtered query succeeded, with returned count checked against actual rows. ZIP responses incorrectly advertise HTML MIME; their ZIP structure was opened and validated. No state eligibility numerator/member-month table was exposed by EX.5's returned schema. Exact state eligibility matching remains unavailable in this lane.
