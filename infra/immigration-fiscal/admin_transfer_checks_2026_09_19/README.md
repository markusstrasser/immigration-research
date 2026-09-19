# 2024 administrative transfer checks

**Verdict:** Historical reporting multipliers do not close the current national totals. For three major programs the remaining comparator gaps run in the direction of additional transfers, not smaller transfers. Uniformly allocating those gaps changes the Mexican-origin annual balance by approximately $5–7bn across the tested conventions. That is a sensitivity, not an identified ethnic correction: geography, institutions, timing and survey allocation remain imperfectly matched.

This lane reconstructs the five U adjustments from the canonical CPS builder, checks all six U totals against current macro_closure (shared/personal × national/target/rest), and computes gaps before applying any new calibration. Values are nominal calendar2024 dollars. The loaded macro baseline is −$234.338818bn shared and −$256.263445bn personal. Source-root is explicit and raw inputs remain read-only.

## Executed national checks

Billions of dollars; shared allocation unless stated. Comparator gaps are not necessarily pure survey underreporting errors.

| Program | CPS before U | Current U multiplier | After U | Primary comparator | After-U gap |
|---|---:|---:|---:|---:|---:|
| SNAP | 46.103 | 1.8832 | 86.822 | 95.115 | −8.72% |
| Social Security | 1,254.671 | 1.0881 | 1,365.208 | 1,449.964 | −5.85% |
| SSI | 58.673 | 0.9814 | 57.582 | 63.079 | −8.72% |

The SNAP, OASDI, SSI and UI ratios derive from net reporting errors for **income2017**, not observations of2024. TANF's 2.0 factor comes from the **2000–2012 average**. Their source locators are retained in canonical `params.json`: NBERw35680 Table4 and w21399 Table1. Inversion is implemented correctly, including SSI's factor below one. Correct arithmetic does not establish transferability across seven years or sample/benefit definitions.

The original SNAP variable is the **SPM resource-unit subsidy**, repeated on member records. Canonical code takes one value per unit and allocates it once; there is no repeated-person SNAP double-count defect. The deliberately wrong repeated-person estimate is $150.181bn. Unique SPM-head weighting produces $44.425bn; current equal-member allocation with person weights produces $46.103bn. These are different survey estimators, not two benefits to add. Similarly, recipient-person weighting yields OASDI $1,226.322bn before U/$1,334.362bn after U, versus the shared figures above. Uniform rakes are therefore calculated separately by allocation.

## Primary-source definitions and unresolved boundaries

- **SNAP:** [USDA monthly national workbook](https://www.fns.usda.gov/sites/default/files/resource-files/snap-4fymonthly-9.xlsx), data as of September11,2026. Sum the twelve Jan–Dec2024 benefit-cost cells, not the FY2024 row: $95.115241680bn; FY2024 is $93.836369579bn. Includes territories and possibly disaster assistance; administrative costs are excluded. Territory subtraction was not identified from this national workbook. The current state snapshot has2025/2026 months and cannot supply2024 subtraction. No SNAP count-to-dollar imputation is used. A strict50-state/DC total therefore remains a small-scope unresolved item, not silently estimated.
- **OASDI:** [SSA2025 Annual Statistical Supplement Table5.J1](https://www.ssa.gov/policy/docs/statcomps/supplement/2025/5j.html): CY2024 all-areas annual estimated benefits $1,471.195bn. Explicitly subtract American Samoa$0.077bn, Guam$0.313bn, Northern Marianas$0.047bn, Puerto Rico$11.980bn, USVI$0.414bn, foreign countries$8.391bn and unknown$0.009bn, leaving **$1,449.964bn for50states/DC**. These records include institutional residents; CPS here does not. Unnegotiated checks are not deducted; lump-sum death payments are excluded. The current CPS population also excludes people who died before its2025 interview. We have not manufactured these missing adjustments.
- **SSI:** [SSA2024 Statistical Report Table2](https://www.ssa.gov/policy/docs/statcomps/ssi_asr/2024/sect01.html) reports $63.079493bn = federal$59.665127bn + federally administered state supplements$3.414366bn. It allocates payments by **month due**, nets overpayment recoveries, excludes state-administered supplements, and is broader than the CPS institutional/geographic domain. [SSA2025 Annual Report TableIV.C1](https://www.ssa.gov/oact/ssir/SSI25/IV_C_Payments.html) instead reports **federal-only payment-date** CY2024$63.080bn; it does not deduct certain overpayments remitted to Treasury. Their near equality does not make these the same measure. A complete cash/calendar/state-supplement/domain bridge is not available here, so no single SSI factor is promoted as corrected truth.
- **BEA cross-check:** The pinned [NIPA workbook](https://apps.bea.gov/national/Release/XLS/Survey/Section3All_xls.xlsx), Table3.12/T31200-A2024 column, has OASDI$1,447.965bn(line5), SNAP$97.391bn(line21), SSI$59.967bn federal(line23)+$5.167bn state(line36)=$65.134bn and UI$36.468bn(line7). These are calendar-year benefits-to-persons accounts, not identical program cash totals. The sheet publication date is September26,2025, in a workbook created August25,2026. The SNAP difference from the later USDA program table is left unallocated rather than assigned to a guessed cause. This workbook is already used by macro_closure; agreement is common-source national-account reconciliation, not independent evidence.

SSA raw HTML requests returned403, but primary pages were readable through the web tool. Exact transcribed cells, table locators, scope and retrieval date are versioned in `source_cells.json`; no claim of a raw SSA HTML archive is made. USDA raw bytes and the existing BEA workbook are SHA256-pinned. `acquire.py` refuses revised USDA bytes until reviewed. Census defines the SNAP unit directly in its [2025 variable catalog](https://api.census.gov/data/2025/cps/asec/mar/variables.html).

## Uniform-raking sensitivity, not an ethnic finding

For each program and allocation, set `new_ratio = administrative_total / model_national_baseline`. The change in target balance is `−target_baseline × (new_ratio − historical_ratio)`. This **replaces** the historical adjustment rather than adding the entire administrative payment again. Target/rest shares are retained; no assumption about ethnicity-specific reporting behavior is estimated. Institutional and other out-of-domain dollars are not identified as belonging to the target group.

| Sensitivity | Shared balance | Personal balance |
|---|---:|---:|
| Current macro baseline | −234.339 | −256.263 |
| SNAP + domestic OASDI only; SSI unchanged | −239.276 | −262.324 |
| Add SSA federally administered SSI/month-due target | −239.728 | −262.775 |
| Instead add broader BEA federal+state SSI target | −239.898 | −262.944 |
| All three targets from BEA | −240.147 | −263.197 |

No confidence interval or causal policy effect is implied. Holding all unobserved nonhousehold/domain adjustments at zero when raking broader admin totals onto CPS is a substantive scenario assumption. The strongest conclusion is that2017 multipliers cannot be represented as2024 national-total validation; these three tests do not overturn the rough fiscal magnitude.

The UI baseline is $25.061bn shared/$24.743bn personal; historical U raises it to $43.434bn/$42.881bn, versus BEA's $36.468bn calendar2024. This points the opposite way, but direct DOL program/domain matching was deferred under the parent's narrowed scope and **UI is not in the rakes**. TANF/other cash assistance is also excluded from new calibration: `PAW_VAL` is broader than TANF, and neither the total TANF block grant nor all TANF spending is a matched cash benefit target.

No canonical coding defect was confirmed. Recommend retaining old-ratio figures as explicitly historical scenarios until matched target construction is completed. A calibration that corrects current totals must retain pre-calibration errors, exclude nonhousehold payments where measurable, distinguish state supplements/timing, and not claim to identify missing Mexican-origin recipients.

## Reproduce and checks

From the canonical repository directory, with the code path set to this managed worktree or its integrated location:

```sh
OPENBLAS_NUM_THREADS=1 UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project --with pandas --with numpy --with openpyxl --with pyreadstat --with duckdb python3 /path/to/admin_transfer_checks_2026_09_19/builder.py --source-root /Users/alien/Projects/immigration-research
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project --with pandas --with numpy --with openpyxl python3 -m unittest discover -s /path/to/admin_transfer_checks_2026_09_19
```

Five tests cover real pinned workbook parsing, calendar rather than fiscal-year selection, duplicate/missing month rejection, resource-unit conservation and replacement-rake signs, plus declared-year selection. Runtime gates verify all six canonical U totals, unchanged macro balance anchors, source hashes, source units and national raking identities. Derived CSVs and manifests are ignored. No commits or canonical edits.
