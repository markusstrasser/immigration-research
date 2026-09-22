# A second instrument for the 2000–2010 inflow: the ancestry push-pull prediction

**Verdict:** On the displacement lane's own 2000–2010 metro panel (334 metros of 100k+, all
foreign-born share, published ACS treatment, population weights), the public
Burchardi–Chaney–Hassan predicted 2000–2010 arrivals aggregated to 2013 CBSAs are a
**stronger and cleaner instrument than the pre-1990 settlement shift-share**: first-stage F
**63.9** against 29.1, it does **not** predict the 2000 level of the outcome (the settlement
instrument does, +0.132 ± 0.035 on SSI receipt), Mexico carries **33%** of its variance
(against 67% in Wilson–Zhou's 2021–24 use of the same file), and it keeps F 58.6 with the
Mexico component removed. With it, the household **SSI** response to a 1-point rise in the
foreign-born share is **−0.28 (SE 0.06)** instead of the settlement instrument's −0.44 (0.10),
and the **public-assistance** response is **−0.10 (0.19), a null**, instead of −0.99 (0.28).
The two instruments disagree formally (Hansen J p = 0.011 on SSI, 0.0002 on public
assistance), which is what the settlement instrument's failed exogeneity test predicts. The
lane's negative claim stands, and is now better founded: no native take-up of transfers is
visible on this margin; a negative SSI association survives a cleaner instrument at about
two thirds of its earlier size; the public-assistance association does not survive it.
Employment and participation outcomes are absent from the 2000 endpoint (SF3 does not carry
them) and were not tested. 2026-09-22. Lane script `second_instrument.py`; gates G1 and G2
reproduce the displacement lane's first stage and IV coefficient to 1e-9 before any new row.

## What the instrument is

`AncestryInstrument_County.dta` (immigrationshock.com; 3,141 counties × 195 origins) gives,
per county and origin, the predicted arrivals in each census wave from the interaction of an
origin's national outflow with a destination's pull from **other** origins, the construction
of Burchardi, Chaney and Hassan (2019). `PushPull_10` is the 2000–2010 wave; it sums to
10.45 million predicted arrivals nationally, 3.15 million from Mexico. County codes are 1990
FIPS × 10 (checked on Autauga, AL = 01001). Counties are mapped to February-2013 CBSAs with
the hedonic lane's crosswalk (`geo_county_cbsa_2013.csv`); the 1,335 counties outside any
CBSA drop, as the lane's metro panel has no rows for them. The instrument in percentage
points of 2000 population, matching the lane's units:

    Z2 = 100 × Σ_origins PushPull_10[county ∈ CBSA] × 1000 / pop_2000(CBSA)

`Z2_mex` uses the Mexico row only; `Z2_exmex` is the remainder; `Z2_1990s` uses the previous
wave (`PushPull_9`) as a check on whether the 1990s prediction also carries the 2000s change.
[DATA: `derived/cbsa_predicted_inflow.csv`; `sources/immigration-fiscal/data/external/stage3/immigrationshock/ancestry-instruments/ACQUIRED.md`]

## Estimates, 2000–2010, all foreign-born, n = 334

Units: change in the outcome (percentage points of households) per 1 percentage-point rise in
the foreign-born share of the metro population. HC1 robust standard errors, population
weights. `Z` is the lane's settlement instrument; `Z2` the ancestry prediction.
[CALCULATION: `derived/second_instrument.csv`]

### First stages and instrument checks

| quantity | estimate | SE | 95% interval | F |
|---|---:|---:|---|---:|
| corr(Z, Z2), weighted | 0.653 | | | |
| Mexico share of var(Z2) | 0.327 | | | |
| first stage on Z | 0.153 | 0.028 | [0.097, 0.209] | **29.1** |
| first stage on Z2 | 0.315 | 0.039 | [0.238, 0.392] | **63.9** |
| first stage on Z2 without Mexico | 0.442 | 0.058 | [0.329, 0.555] | 58.6 |
| first stage on Z2, Mexico only | 0.833 | 0.134 | [0.570, 1.096] | 38.5 |
| first stage on the 1990s prediction | 0.175 | 0.033 | [0.111, 0.239] | 28.5 |
| first stage on both, coefficient on Z | −0.016 | 0.102 | [−0.217, 0.184] | joint 37.0 |
| first stage on both, coefficient on Z2 | 0.328 | 0.104 | [0.124, 0.533] | partial F of Z2 given Z **9.9** |
| Z on the 2000 SSI level (exogeneity test) | **+0.132** | 0.035 | [0.064, 0.200] | |
| Z2 on the 2000 SSI level (exogeneity test) | −0.085 | 0.083 | [−0.247, 0.077] | |

Given Z2, the settlement instrument adds nothing to the first stage (its coefficient goes to
−0.02 ± 0.10). The settlement instrument predicts where SSI receipt was already high in 2000;
the ancestry prediction does not.

### Second stages

| outcome | estimator | coefficient | SE | 95% interval | Hansen p |
|---|---|---:|---:|---|---:|
| household SSI receipt | OLS | −0.144 | 0.032 | [−0.207, −0.080] | |
| | IV with Z (lane) | −0.442 | 0.098 | [−0.635, −0.250] | |
| | IV with Z + 2000 level (lane) | −0.424 | 0.088 | [−0.596, −0.252] | |
| | **IV with Z2** | **−0.280** | 0.065 | [−0.408, −0.153] | |
| | IV with Z2 + 2000 level | −0.279 | 0.069 | [−0.414, −0.144] | |
| | IV with Z2 without Mexico | −0.292 | 0.066 | [−0.421, −0.164] | |
| | IV with Z and Z2 | −0.274 | 0.064 | [−0.400, −0.148] | **0.011** |
| household public assistance | OLS | | | | |
| | IV with Z (lane) | −0.986 | 0.276 | [−1.528, −0.445] | |
| | IV with Z + 2000 level (lane) | −0.348 | 0.126 | [−0.595, −0.101] | |
| | **IV with Z2** | **−0.102** | 0.193 | [−0.481, 0.276] | |
| | IV with Z2 + 2000 level | −0.079 | 0.103 | [−0.281, 0.122] | |
| | IV with Z2 without Mexico | −0.184 | 0.182 | [−0.541, 0.173] | |
| | IV with Z and Z2 | −0.067 | 0.191 | [−0.441, 0.308] | **0.0002** |

The public-assistance OLS row is in the CSV; it is omitted here because the lane's memo does
not headline it. The lane's IV rows reproduce to 1e-9 (gate G2, both outcomes).

## Reading

1. **The lane's instrument was the weak link, and this one is better on every check the lane
   itself used.** Higher F, no correlation with the baseline level, less Mexico
   concentration, robust to dropping Mexico. It is also the instrument's intended decade:
   the file predicts 2010 ancestry from the 2000s wave, whereas Wilson–Zhou's rejected use
   pushed it onto 2021–24 flows.
2. **Sign held, size shrank, one result died.** SSI receipt still falls with inflow, at
   −0.28 instead of −0.44 per point. Public assistance receipt is null. The Hansen rejections
   say the two instruments identify different things, and the exogeneity test says which one
   is contaminated.
3. **Not a fiscal number.** These are household receipt rates across metros over a decade,
   with no dollar amounts and no native split at the 2000 endpoint; the lane's natives-only
   check used 2005–2008. They bear on the displacement objection (do natives move onto
   transfers when immigrants arrive: no sign of it), not on the account's benefit terms.
4. **What is still open.** Employment and participation at 2000–2010 need a 2000 endpoint
   the SF3 pull does not carry; the natives-only outcome at 2000–2010 needs the same. Both
   are a PUMS 2000 5% build, which the lane's `build_pums_panel.py` could be pointed at.

## Reproduce

```sh
cd /Users/alien/Projects/immigration-research
OPENBLAS_NUM_THREADS=1 uv run --no-project --with statsmodels --with scipy \
  python3 infra/immigration-fiscal/ancestry_instrument_2026_09_22/second_instrument.py
```

About 70 seconds, most of it reading the 131 MB Stata file. Needs the displacement lane's
`derived/` files, the hedonic lane's crosswalk and the ignored `.dta` under `sources/`.
Gates: G1 reproduces the lane's 2000–2010 settlement first stage (n 334, 0.15296841, SE
0.02836149); G2 reproduces its IV coefficients (−0.442459 SSI, −0.986354 public assistance).
[DATA: `derived/summary.json`]

## Files

| file | tracked | what |
|---|---|---|
| `second_instrument.py` | yes | build, gates, estimates; hand-written weighted 2SLS with HC1 sandwich and Hansen J |
| `derived/cbsa_predicted_inflow.csv` | yes | 2000s and 1990s predicted arrivals and 2010 predicted ancestry per CBSA, all origins and Mexico |
| `derived/second_instrument.csv` | yes | 34 estimate rows, two outcomes |
| `derived/summary.json` | yes | gate values and file counts |
