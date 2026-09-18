**Verdict:** The native-sorting channel is real in California, roughly two orders of magnitude too small to matter against the state's Mexican-origin fiscal gap, and not attributable to that gap — high-income out-migration tracks the effective tax rate on top earners, not immigrant shares, and the metro-level "displacement" coefficient is a normalisation artefact that reverses sign when the regressor stops carrying the native population in its denominator.

Model: claude-opus-5[1m]

## Headline numbers

| quantity | value | source |
|---|---|---|
| California net AGI outflow, mean 2012-2023 | **+$7.09bn/yr** | `derived/revenue_arithmetic.csv` |
| California net AGI outflow, 2021 / 2023 | **+$20.6bn / +$17.2bn** | same |
| California revenue effect at ITEP top-1% rate 12.1%, 2023 | **−$2.08bn** | same |
| share of California's $189.3bn Mexican-origin gap | **1.1%** (2.2% against the $111.7bn all-native version) | `ledger_stress_2026_09_17/derived/state_matched.csv` |
| Texas net AGI flow, mean | **−$6.44bn/yr (net inflow)** | `derived/revenue_arithmetic.csv` |
| Mexican-origin share, CA vs TX | 31.8-32.5% vs 33.5-31.7% | `derived/state_panel.csv` |
| net out-migration of $200k+ filers, per SD: tax rate vs Mexican share | **+0.51 [+0.20, +0.82]** vs −0.20 [−0.53, +0.14] | `derived/horse_race.csv` |
| metro native population response, Δ Mexican-origin **share** | −0.013 [−0.024, −0.003] | `derived/metro_estimates.csv` |
| same, both sides scaled by fixed 2010 population | **+1.69 [+1.26, +2.12]** | same |
| shift-share IV first-stage F | **0.3 to 9.0** (gate was 10) → all IV rows uninformative | same |

## Memo

`research/immigration-native-sorting-tiebout-2026-09-18.md` (498 lines): verdict, what is and
is not identified, data with two API traps recorded, metro analysis with the normalisation
test and the failed IV gate, state analysis with the CA/TX contrast, the revenue arithmetic,
four disconfirmation checks (three fail the hypothesis), the steel-man of the mobility null,
instrument-bias note, sources with URLs and fetch dates.

## Verification

```bash
cd /Users/alien/Projects/immigration-research
set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
L=infra/immigration-fiscal/tiebout_sorting_2026_09_18
UV='uv run --no-project --with pandas>=2 --with numpy>=2 --with statsmodels --with linearmodels python3'

# 1. re-fetch the IRS CSVs (idempotent; validates each header, needs --http1.1)
$L/fetch_soi.sh

# 2. rebuild the SOI panel; expect the 1415 incompleteness warning
uv run --no-project --with "pandas>=2" python3 $L/build_soi_panel.py

# 3. the three analyses (metro_estimates.csv, state_estimates.csv, horse_race.csv,
#    revenue_arithmetic.csv all regenerate identically)
$UV $L/analyze_metro.py
$UV $L/analyze_state.py
$UV $L/horse_race.py
uv run --no-project --with "pandas>=2" python3 $L/revenue_arithmetic.py

# 4. spot-check the headline ratio
uv run --no-project --with "pandas>=2" python3 - <<'PY'
import pandas as pd
r = pd.read_csv('infra/immigration-fiscal/tiebout_sorting_2026_09_18/derived/revenue_arithmetic.csv')
ca = r[(r.state=='California') & (r.bracket=='all filers') & (r.year==2023)]
print('CA 2023 revenue effect $bn', round(float(ca.revenue_at_top1_rate_bn), 2))
g = pd.read_csv('infra/immigration-fiscal/ledger_stress_2026_09_17/derived/state_matched.csv')
gap = g[(g.target=='mexican_observed_total') & (g.metric=='gap_total') &
        (g.scenario=='all_age_shared') & (g.cells=='CA_age') &
        (g.reference=='third_plus_nh_white')].estimate.iloc[0]
print('share of CA gap %', round(float(ca.revenue_at_top1_rate_bn)*1e9/abs(gap)*100, 2))
PY

# 5. the PUMS predicate trap: the range form returns foreign codes and drops own-state movers
python3 - <<'PY'
print("wrong:  MIGSP=1:56          -> includes 303 (Mexico), 207, 210; no 006")
print("right:  MIGSP=001&...&056   -> 50 codes incl. 006; CA 2023 domestic in = 423,980")
PY
```

Re-running `analyze_metro.py` and `revenue_arithmetic.py` reproduced their stored outputs
byte-identically when the parent session checked them. `analyze_state.py` filled the
`net_out_hi_acs` rows once `_cache/mobility_B07010.csv` and `_cache/mobility_B07410.csv`
finished downloading; those rows are in the stored `state_estimates.csv` and in
`horse_race.csv`.

## Files

Scripts, all under `infra/immigration-fiscal/tiebout_sorting_2026_09_18/`:
`fetch_soi.sh`, `build_soi_panel.py`, `pull_state_covariates.py`, `pull_metro_covariates.py`,
`pull_metro_acs5.py`, `pull_mobility_tables.py`, `pull_pums_migration.py` (validation only),
`analyze_metro.py`, `analyze_state.py`, `horse_race.py`, `revenue_arithmetic.py`.

Derived: `soi_state_agi.csv`, `soi_state_totals.csv`, `state_panel.csv`,
`state_estimates.csv`, `horse_race.csv`, `metro_panel.csv`, `metro_estimates.csv`,
`revenue_arithmetic.csv`. `_cache/` holds the raw pulls and is gitignored by the tree's
existing rules; nothing was committed.

## Covered

State panel 51 states x 12 tax-year pairs on IRS SOI by AGI bracket; ACS state migration by
nativity (B07007/B07407) and by income (B07010/B07410) 2010-2024; metro panel 846 metro and
micro areas on ACS 5-year 2010 and 2023 endpoints; OLS in share and population-scaled form
with size, age, college, rent and region controls; 2000-base shift-share IV with first-stage
F reported; rent mediator arm; 250k population floor arm; state and region fixed-effects arms;
the Asian and Cuban placebo groups at both levels; the tax-versus-share horse race on six
outcomes; the California and Texas revenue arithmetic against the stress lane's state gaps.

## Skipped, with reasons

* **Income crossed with nativity.** The published ACS tables do not cross them and the PUMS
  pull that would have was abandoned: the Census API served roughly 2.5 minutes per large
  state-year, about 90 minutes per year of data. The pull script is kept and works; it was
  used to validate the flow definition. The consequence is that the "high-income" arm is
  $200k-plus **filers** (SOI, all nativities) and $75k-plus **movers** (ACS, all
  nativities), not high-income natives specifically.
* **County and within-metro sorting.** The Tiebout mechanism is usually argued to work
  across school districts and neighbourhoods. IRS county-to-county files were downloaded but
  not analysed; no arm here can see sub-metro sorting, and that is the main thing this lane
  cannot rule out.
* **IRS 2014-15 AGI brackets.** The IRS's own `1415inmigall.csv` covers 14 states (Alaska
  through Illinois), so that pair is dropped from every bracket series. California is inside
  the covered set, so its revenue series has no hole; Texas is not.
* **Kleibergen-Paap and the JRS multi-instrument correction.** Not run: the single-instrument
  first stage already fails at F 0.3 to 9.0, so the brief's stop rule applied.
* **A within-metro housing design.** Separating the housing channel from common demand shocks
  needs an instrumented within-metro design, which is a different lane.
