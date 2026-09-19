<!-- fiscal-repair-2026-09-19 -->
**Current fiscal release (September 19):** [Repaired yearly and lifetime calculation index](../../../research/immigration-yearly-lifetime-cost-repair-2026-09-19.md) supersedes affected annual, household-financing and lifetime figures below. It reports both allocation conventions, actual-age survival NPVs and unresolved coverage. Earlier text and calculations remain historical evidence; unrelated findings are unchanged.

# Longevity and Social Security timing on the lifetime frame — 2026-09-18

Two objections to the repo's period account, priced on the repo's own profiles.

**A. Longevity.** The lifetime machinery in `pronatal_equivalence_2026_09_18` gives every
person exactly 83 years and then stops. Hispanic life expectancy at birth exceeds White
non-Hispanic by 2.9 years, so the 65+ bands should be drawn for longer. Phase A replaces the
constructed terminal age with NVSS 2024 life-table person-years `L(x)`.

**B. Social Security timing.** The account credits a worker with the OASDI tax paid in 2024
and charges a retiree with the benefit received in 2024, booking no liability for the benefit
the 2024 worker will claim later. Phase B prices that liability with SSA money's worth ratios.

## Run

```sh
cd /Users/alien/Projects/immigration-research
U='uv run --no-project --with pandas>=2 --with numpy>=2 --with openpyxl --with pyarrow python3'
D=infra/immigration-fiscal/lifetime_longevity_sstiming_2026_09_18
PYTHONUNBUFFERED=1 OPENBLAS_NUM_THREADS=1 $U $D/longevity.py     # phase A
PYTHONUNBUFFERED=1 OPENBLAS_NUM_THREADS=1 $U $D/ss_timing.py     # phase B
PYTHONUNBUFFERED=1 OPENBLAS_NUM_THREADS=1 $U $D/combine.py       # A and B on one footing
```

`ss_timing.py` builds the CPS ASEC 2025 state once (about 3 minutes) and caches the person
frame at `derived/cps_ss_stage.parquet`; later runs reuse it. Delete that file to rebuild.
`combine.py` reads `derived/ss_timing_by_band.csv`, so run `ss_timing.py` first.

## Prior work this lane does not redo

Longevity was priced once before on the **partial** ledger with the **CDC 2021** tables:
`research/immigration-mexican-origin-by-generation-2026-09-16.md` section 5.1, built by
`../cps_generation_welfare_2026_09_16/lifecycle_ledger_by_generation.py` (commit `1dc8b8e`,
output `lifecycle_ledger_result.txt`). It found the mortality-table swap worth about $20,000
undiscounted, roughly 5% of a $375,000 lifetime gap. This lane takes that as the prior result
and adds what was missing: the same swap on the **complete** all-age account (ladder 130) with
the pronatal-lane profiles at 3% and undiscounted from ages 0 and 25, the **nativity split**
that pass flagged as unresolved, **2024 and 2023** life tables in place of 2021, and Part B,
which had never been done. See "Relation to the 2026-09-16 pass" in `RESULT.md`.

## Inputs

| input | where |
|---|---|
| age-band balances by group, 8 bands | `../pronatal_equivalence_2026_09_18/derived/age_profiles_references.csv` |
| complete-minus-partial per-person-year shift | `../gap_interest_2026_09_18/derived/audit.json` (waterfall step 14) |
| band definitions, terminal age, profile loader | `../homicide_cost_2026_09_18/cost_model.py` (imported, not rewritten) |
| CPS ASEC 2025 | `sources/immigration-fiscal/data/external/stage3/census/cps_asec_2025/asecpub25csv.zip` |
| NVSS life tables 2024 and 2023 | `_cache/lt2024_Table*.xlsx`, `_cache/lt2023_Table*.xlsx` |
| SSA money's worth ratios | `_cache/ssa_an2025-7.pdf` and its `.txt` text layer |
| Trustees net-immigration sensitivity | `_cache/tr2025_vid.html`, `_cache/tr2026_vid.html` |
| SSA Actuarial Note 151 | `_cache/note151.pdf` |
| prior longevity pass, for comparison only | `../cps_generation_welfare_2026_09_16/lifecycle_ledger_result.txt` |
| average wage index, payroll tax receipts | `_cache/ssa_awi.html`, `_cache/ssa_tr2025_IVA.html` |

`ss_timing.py` extends `analyze_cps_fiscal_2025.PERSON` with `A_SEX`, `A_MARITL`, `A_SPOUSE`,
`A_LINENO`, `SEMP_VAL`, `FRSE_VAL` before calling `extend_ledger.build`, the same pattern
`extend_ledger` itself uses for `WSAL_VAL`.

## Outputs

| file | contents |
|---|---|
| `derived/survival_tables.csv` | `lx`, `Lx` by age 0-100 for every life table used |
| `derived/longevity_lifetime.csv` | lifetime balance by arm, account, rate, group, start age |
| `derived/longevity_gaps.csv` | gaps against the white reference and the longevity-only piece |
| `derived/longevity_audit.json` | life expectancies, gate residuals |
| `derived/mwr_table.csv` | Actuarial Note 2025.7 Table 1, parsed, 55 rows |
| `derived/ss_timing_arms.csv` | every timing arm by group |
| `derived/ss_timing_group.csv` | the central timing arm |
| `derived/ss_timing_by_band.csv` | the timing adjustment per person by age band |
| `derived/ss_timing_audit.json` | AWI, rates, gate residuals, coverage scale |
| `derived/combined_lifetime.csv` | both corrections together, every survival x timing arm |
| `derived/combined_summary.csv` | the Mexican-origin rows of the above |
| `derived/cps_ss_stage.parquet` | cached CPS person frame (regenerable) |

## Sign conventions

`longevity.py` reports `gap_vs_white` as **white minus group**, so a larger positive number is
a worse position for the group. `combine.py` reports `gap_vs_white` as **group minus white**,
matching the repo's `-7,224`, so a more negative number is worse. The two files are internally
consistent; read the column name, not the sign of a neighbouring table.

## Gates executed

1. `longevity.py` — the terminal-83 lifetime reproduces every row of the pronatal lane's
   `lifetime_equivalence.csv`, max absolute difference **$0.000000**.
2. `longevity.py` — the proportional-hazard life-table rebuild at HR = 1 reproduces the White
   non-Hispanic table, `|Δe0| = 0.0000` years.
3. `longevity.py` — each life table is checked for 101 single years of age, a radix of
   100,000, and monotone non-increasing `lx`.
4. `ss_timing.py` — the money's worth table parses to exactly 5 earnings levels x 11 cohorts
   and is monotone decreasing in earnings level within every cohort and family type.
5. `ss_timing.py` — the 40 group x band populations reproduce `age_profiles_references.csv`,
   max absolute difference **0.000000 people**.
6. External check, not a gate: the account's OASDI payroll tax on CPS civilian households is
   $1,347.8bn against published 2024 net payroll tax contributions of $1,293.3bn, a ratio of
   1.0422. A `coverage_scale` arm rescales to the published total.


## Revisions — fiscal repair, September 19, 2026

Grant/fee ownership, veterans and enforcement double counting, real discounting and age-profile propagation were corrected. The $263bn/$2,246/89% and flat-shift lifetime headlines are superseded; the birth-policy inference remains withdrawn. See [current results](../../../research/immigration-yearly-lifetime-cost-repair-2026-09-19.md) and its linked decision record.
