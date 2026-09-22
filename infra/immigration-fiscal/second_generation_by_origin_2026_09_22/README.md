# Second generation by parental origin — IPUMS-CPS ASEC 1994–2025 (cluster-V V02)

Descriptive lane. It asks how much of the first-generation gap in adult outcomes is still there in
the US-born second generation, by parental origin and over three periods, and attaches a sampling
error to every number it prints.

Read [RESULT.md](RESULT.md) for the findings. This file covers how to run it and what the
estimator does.

## Run

```sh
cd /Users/alien/Projects/immigration-research
uv run --no-project python3 -m pytest infra/immigration-fiscal/second_generation_by_origin_2026_09_22/ -q
OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb python3 \
  infra/immigration-fiscal/second_generation_by_origin_2026_09_22/analysis.py
```

The full build takes about 40 seconds and writes everything under `derived/`. It needs no network
and no key. In a worktree or a fresh clone, drop `--no-project`.

## Input

One gated IPUMS-CPS extract, read only, never modified:

| file | what |
|---|---|
| `sources/immigration-fiscal/data/external/cps/cps_2ndgen.csv.gz` | 5,721,633 persons, ASEC 1994–2025 |
| `…/cps_2ndgen.xml` | DDI codebook — every code list this lane uses is parsed from it at run time |
| `…/cps_2ndgen.manifest.json` | sha256, checked before the first read (gate G1) |

Staging instructions for the extract are in
[`research/immigration-gated-data-specs-2026-06-25.md`](../../../research/immigration-gated-data-specs-2026-06-25.md)
section 1.

## Universe and definitions

Civilian adults 25–64, `ASECWT` weights, `NATIVITY` 1–5. Three sample decisions that the extract
forced and that change the numbers:

**The 2014 ASEC is in the file twice.** IPUMS ships both the 5/8 traditional sample and the 3/8
income-redesign sample, and each carries full-population weights: 313.4 million and 313.4 million
against 311.1 million in 2013 and 316.2 million in 2015. Keeping both doubles 2014. This lane keeps
`HFLAG = 0`, the traditional file, so the income questions stay comparable with 1994–2013. The
loader (`build/load_cps_second_gen.py`, whose table is a local derived file under `sources/`, not
tracked) kept both until 2026-09-22 and now applies the same rule; gate G2 rebuilds that table
from this lane's code. This lane's own cells still differ from the loader's because of the
civilian universe, the first-generation origin rule and the `US outlying` category below.

**Armed forces are dropped** (`EMPSTAT` = 1), which is the IPUMS analogue of the ledger's
`PRPERTYP = 2` civilian-adult universe. `NATIVITY = 0` (Unknown) is dropped, as the loader does.

**Origin.** The first generation takes its origin from its own birthplace; the second generation
takes the father's birthplace when he is foreign-born and the mother's otherwise. The committed
loader uses parental birthplace for everyone, including the first generation. Birthplaces in
general codes 100–120 (Puerto Rico, Guam, the US Virgin Islands, American Samoa, outlying n.s.) go
to a tenth category, `US outlying`; the loader's nine-region map leaves them unassigned. IPUMS
`NATIVITY` counts people born in US territories and people born abroad to American parents as
foreign-born, so that category sits inside the first generation here.

Two origin taxonomies are estimated separately, because a country is a subset of its region and the
two cannot go in one design:

- **region** — the loader's nine regions plus `US outlying`
- **country** — the ten largest single parental birthplaces by weighted second-generation count
  (Mexico, Canada, Italy, Germany, the Philippines, England, China, Cuba, Poland, Ireland), with
  everything else pooled as `Other origin`

The reference group is the third-plus generation, non-Hispanic white, the ledger's white reference.
`3rd+_Mexican_selfid` and `3rd+_other` are reported as their own rows; the three together are the
loader's `native_baseline`.

## Estimator

Each outcome is regressed by weighted least squares on group indicators plus a full set of
age-band × sex × survey-year indicators — 8 five-year bands × 2 sexes × 32 years = 512 cells. The
coefficient on a group indicator is its adjusted gap against the reference; no coefficient on a
control is reported. Because every regressor is an indicator and the groups partition the sample,
the normal equations have a diagonal fixed-effect block, and the group coefficients come out of its
Schur complement rather than a dense 2.9-million-row design matrix. `test_analysis.py` runs that
shortcut against a textbook dummy-variable regression on synthetic data and requires agreement to
1e-8.

The closing ratio for an origin is `1 − (second-generation gap ÷ first-generation gap)`: 1 means the
second generation has reached the reference, 0 means it has closed nothing. It is a ratio of two
estimates, so it is only interpretable where the first-generation gap is a clear deficit. For
origins whose first generation is already *ahead* of the reference the ratio is reported in
`closing_ratios.csv` as it comes out and should not be read as convergence.

## Standard errors

A household-cluster bootstrap: 200 draws, seed 20260922, resampling `SERIAL` with replacement
within each survey year, applied to every mean, gap, ratio and period change. The extract carries
no replicate weights, so the resample ignores the CPS stratified PSU design. The CPS rotation panel
also returns about half of each March sample the following March, and a within-year resample treats
those as independent clusters. **Every standard error here is a lower bound on the true sampling
error, for both reasons.**

## Gates

All five are asserted in `analysis.py` and recorded in `derived/audit.json`. A failure raises and
the build stops; no tolerance is relaxed to pass.

| gate | what it checks |
|---|---|
| G1 | sha256 of the CSV matches `cps_2ndgen.manifest.json` before any read |
| G2 | this lane rebuilds `sources/immigration-fiscal/derived/lifetime/cps_second_gen_by_origin.csv` — all 37 rows, all columns, to 1e-9 |
| G3 | ASEC 2025 weighted and unweighted counts match `gen_ledger_extension_2026_09_16` for `mexico_born`, `mexican_second_gen`, `third_plus_nh_white` and `mexican_third_plus_selfid` within 0.5% |
| G4 | every decision code is printed with the label the DDI gives it, and the label is asserted |
| G5 | no reported cell below 100 unweighted observations; every reported standard error finite |

G3 maps the ledger's `PRCITSHP` rule onto `CITIZEN` rather than `NATIVITY`, because `NATIVITY`
files territory-born and American-parent-born people as foreign. On the ledger's own universe —
civilian adults 25–64, person weights — the four groups agree to within 5e-8 relative.

## Outputs

| file | rows | what |
|---|---|---|
| `derived/cells.csv` | 3,296 | weighted mean and bootstrap SE by outcome × taxonomy × period × group |
| `derived/adjusted_gaps.csv` | 3,172 | adjusted and raw gap to the reference, with SEs |
| `derived/closing_ratios.csv` | 745 | closing ratio with bootstrap SE and 2.5/97.5 percentiles |
| `derived/period_trends.csv` | 834 | means and gaps by period, with the first-to-last change and its SE |
| `derived/audit.json` | — | gate results, DDI codes with labels, sample decisions, bootstrap spec, limitations |

344 cells fall below the 100-observation floor and are suppressed from all four CSVs.

## What this cannot show

The generation contrasts are cross-sectional. The first generation observed in a period is not the
parent generation of the second generation observed in the same period, so a closing ratio is a
synthetic-cohort quantity, not a family trajectory. Origin-group differences mix selection into
migration, arrival cohort, destination, legal status and period with anything transmitted inside
families. Age, sex and survey year are the only things adjusted for; education, state and legal
status are deliberately not controlled because they are outcomes of the same process. `NCHILD`
counts coresident own children, not completed fertility. Income is nominal as reported and
conditional on being positive. The full list is in `derived/audit.json` under `limitations`, and
RESULT.md repeats it without softening.
