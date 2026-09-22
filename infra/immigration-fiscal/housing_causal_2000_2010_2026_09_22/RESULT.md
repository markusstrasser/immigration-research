# Rents and house values against the 2000–2010 inflow, instrumented — result

**Verdict:** On the 334 metros of the displacement lane's 2000–2010 panel, a 1 percentage-point
rise in the foreign-born share of population over the decade raises **house values by about
6 to 12%** and **rents by 0 to 4%** when instrumented with the ancestry push-pull prediction
(ladder 182): values **+11.6% (SE 2.9)**, +5.7% (2.8) with the 2000 level controlled; rents
**+1.4% (1.4)**, a null whose interval [−1.5, +4.2] contains both zero and Saiz's one-for-one.
The settlement shift-share gives figures two to five times larger (values +29%, rents +7.8%)
and Hansen J rejects the instrument pair on both outcomes (p 0.00001 and 0.0006), the same
pattern as the transfers outcomes: the settlement instrument loads on where prices were
already high and rising. No amplification in supply-inelastic metros is detectable: on the
223 metros with a Saiz elasticity the extra effect below the median elasticity is −2.3% (3.9)
for rents and +0.9% (6.2) for values. Monras's long-run negative price effect is not what this
decade shows, and this is not his design (his is the 1995 push shock over 1990–2000). The
decade straddles the 2006–2010 bust; the 2010 endpoint is a five-year ACS average. 2026-09-22.
Treatment is the all-foreign-born share; the memo's Mexican-born version is not estimable at
the 2000 endpoint (n = 25), and native migration by education was not built.

## Data

- **2000:** Census SF3 county medians, 1999 dollars: median gross rent (H063001), median
  value (H085001), owner- and renter-occupied units (H007002, H007003). SF3 has no
  county aggregate-dollar rent or value table, so medians are used at both endpoints.
- **2010:** ACS 2006–2010 five-year county medians, 2010 dollars: B25064, B25077, tenure
  B25003. Suppressed medians (negative sentinels) dropped; 3,137 counties in both years.
- **Metro index:** renter-weighted mean of county median rents and owner-weighted mean of
  county median values inside each February-2013 CBSA (hedonic lane crosswalk), built
  identically in both years; outcomes are the log change 2000→2010. Population-weighted
  means: rents +0.337 log points, values +0.554, foreign-born share +2.17 points.
- **Treatment, instruments, weights, sample:** exactly the displacement lane's 2000–2010
  rows (published-ACS foreign-born share change, pre-1990 settlement shift-share Z,
  population weights, metros of 100k+), plus the ancestry prediction Z2 from
  `ancestry_instrument_2026_09_22`. First stages reproduce: Z 0.153 (0.028), F 29.1; Z2
  0.315 (0.039), F 63.9.
- **Supply elasticity:** Saiz (2010) MSA elasticities matched to CBSAs by first city and
  state, 223 of 334 matched; inelastic = below the matched sample's population-weighted
  median. [DATA: `derived/metro_housing_panel.csv`; `fetch.py` cache under `_cache/`]

## Estimates

Per 1 percentage-point rise in the foreign-born share, 2000–2010; HC1 robust SE, population
weights, n = 334 unless stated. [CALCULATION: `derived/estimates.csv`]

| outcome | estimator | coefficient | SE | 95% interval | Hansen p |
|---|---|---:|---:|---|---:|
| log rent | OLS | +0.019 | 0.006 | [0.006, 0.031] | |
| | reduced form on Z2 | +0.004 | 0.005 | [−0.005, 0.014] | |
| | IV with Z (settlement) | +0.078 | 0.019 | [0.040, 0.116] | |
| | **IV with Z2 (ancestry)** | **+0.014** | 0.014 | [−0.015, 0.042] | |
| | IV with Z2 + 2000 log level | +0.004 | 0.029 | [−0.053, 0.061] | |
| | IV with Z and Z2 | +0.011 | 0.015 | [−0.018, 0.040] | **0.0006** |
| | IV with Z2, elastic metros (n 223) | +0.015 | 0.018 | [−0.020, 0.051] | |
| | IV with Z2, extra in inelastic metros | −0.023 | 0.039 | [−0.099, 0.053] | |
| log value | OLS | +0.074 | 0.016 | [0.043, 0.104] | |
| | reduced form on Z2 | +0.036 | 0.009 | [0.018, 0.055] | |
| | IV with Z (settlement) | +0.290 | 0.052 | [0.189, 0.391] | |
| | **IV with Z2 (ancestry)** | **+0.116** | 0.029 | [0.060, 0.172] | |
| | IV with Z2 + 2000 log level | +0.057 | 0.028 | [0.002, 0.112] | |
| | IV with Z and Z2 | +0.109 | 0.029 | [0.052, 0.165] | **0.00001** |
| | IV with Z2, elastic metros (n 223) | +0.092 | 0.034 | [0.024, 0.159] | |
| | IV with Z2, extra in inelastic metros | +0.009 | 0.062 | [−0.113, 0.131] | |

The settlement-instrument rows with the 2000 level as a control are in the CSV and are
uninformative (rent −2.7 ± 25.9): once the 2000 level is held fixed the settlement instrument
has no first stage left, which is the exogeneity failure of ladder 182 seen from the other
side. The interaction spec's first stage (the interacted instrument on the interacted
treatment) is 0.258 (0.070), F about 13.5.

## Reading, against the published numbers

| source | horizon and shock | rents | values |
|---|---|---|---|
| this lane, ancestry IV | 2000–2010, +1 pt foreign-born share | +1.4% (−1.5 to +4.2) | +11.6% (6.0 to 17.2); +5.7% with the 2000 level |
| Saiz 2007 (memo §3) | annual, +1% of population | about +1% | about +1% |
| Wilson–Zhou 2026 (ladder 181 reading) | 2021–24, +1% of employment, unauthorized | +1.4% (0.3) | +2.2% (0.7) |
| Monras 2020, long run | 1990–2000, peso-crisis push | −0.5 to −1.2 | −0.8 to −1.4 |
| Piyapromdee 2020, model | +1% population | +0.8 to +1.2 | |

The rent estimate is consistent with every published figure and cannot separate them. The
value estimate is larger than the short-run and modelled figures and carries the 2000s cycle:
the metros that received immigrants in the 2000s were disproportionately the boom-bust
sunbelt metros, and a five-year 2006–2010 average still sits above the 2000 level there. The
2000-level control halves it. The absent inelastic-metro amplification is the one place this
lane speaks against the California–Texas memo's mechanical-response arithmetic (ladder 180),
which assumed the Saiz elasticity governs the pass-through; over a decade with the interaction
identified at F 13.5 and n 223, an extra effect of the size that arithmetic implies (about
two to three times the elastic-metro effect) is outside the rent interval and inside the value
interval, so the test has power for rents only.

## Limits

1. **Not Mexican-origin.** All foreign-born; the 2000 SF3 panel has no usable Mexico-born
   count at the metro level (25 metros).
2. **Nominal decade, one cycle.** 1999 to 2006–2010 dollars; a common deflator cancels in
   the cross-section but the bust does not.
3. **Medians of counties, not units.** A renter-weighted mean of county medians moves with
   composition within counties; the tract-level hedonic lane is the composition-controlled
   design for later periods.
4. **The instrument is the Burchardi–Chaney–Hassan prediction, whose exclusion restriction
   is that historical push-pull interactions affect 2000s housing only through 2000s
   arrivals; it predicts 2010 ancestry stocks, and ancestry itself can move housing demand
   through channels other than the decade's inflow.** The baseline-level check (ladder 182)
   is the only exogeneity evidence here.

## Reproduce

```sh
cd /Users/alien/Projects/immigration-research
set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
uv run --no-project python3 infra/immigration-fiscal/housing_causal_2000_2010_2026_09_22/fetch.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with statsmodels --with scipy \
  python3 infra/immigration-fiscal/housing_causal_2000_2010_2026_09_22/estimate.py
```

Fetch about two minutes (102 API calls, cached); estimate under a minute. Needs the
displacement, ancestry-instrument and hedonic lanes' derived files and the Saiz `.dta` under
`sources/`.

## Files

| file | tracked | what |
|---|---|---|
| `fetch.py` | yes | county endpoints from the Census API; key redacted in errors |
| `estimate.py` | yes | metro index, panel join, OLS/IV/interaction; imports the ancestry lane's estimators |
| `derived/county_housing_2000_2010.csv` | yes | 3,147 county rows, both endpoints |
| `derived/metro_housing_panel.csv` | yes | 334 metros: outcomes, treatment, both instruments, Saiz elasticity where matched |
| `derived/estimates.csv`, `derived/summary.json` | yes | every estimate; means and match counts |
