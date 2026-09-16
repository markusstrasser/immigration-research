# Guard Labor vs Immigration/Diversity — US States, ACS 2019–2023 + Census Govt Finance 2022

**Verdict:** PARTIALLY SUPPORTED, THEN FRAGILE. Private guard employment does rise with foreign-born
share and ethnic fractionalization across states, and the foreign-born coefficient survives income,
poverty, urbanization, Black-share and violent-crime controls. But the fractionalization result is
carried almost entirely by Nevada, Hawaii and DC (casino surveillance and tourism, which sit in the
same occupation code); drop those three and the diversity coefficient collapses to zero. **Public**
police and corrections spending per capita shows no association with immigration or diversity once
controls are in — the raw correlation is an urbanization/income artefact. The strong form of the X
claim, that diversity forces society to buy more coercive infrastructure, is not supported by these
data for the public side, and is weakly and fragilely supported for the private side.

Model self-report: claude-opus-5[1m] (Opus 5, 1M context).

[UNVERIFIED] — cross-sectional, observational, n=51. No causal identification. See §5.

## 1. Validation gates

| Gate | Result | Status |
|---|---|---|
| (a) National OCCP 3930 employed (security guards + gaming surveillance), ACS 2019–2023 5-yr PUMS | **967,863** vs BLS OES 2023 SOC 33-9032 ≈ 1.16M → **−16.6%** | **PASS** (<20%) |
| (b) CA foreign-born share, PUMS NATIVITY=2 | **26.79%** vs ACS B05012 26.70% → 0.09 pt | **PASS** (<1 pt) |
| (b) TX foreign-born share | **17.20%** vs B05012 17.19% → 0.01 pt | **PASS** (<1 pt) |
| FBI Table 5 2019 spot-check | CA 441.2, TX 418.9, DC 1049.0 per 100k | matches published |
| Census govslocalfin 2022 spot-check | CA police protection total direct expenditure $26.14B | plausible |

The 16.6% PUMS shortfall against OES is expected: OES is an establishment survey of jobs, PUMS is
self-reported occupation of employed persons, and OES counts contract-guard jobs that respondents
often self-describe differently. Direction and magnitude are the known ones.
[SOURCE: https://api.census.gov/data/2023/acs/acs5/pums, https://www.bls.gov/oes/2023/may/oes339032.htm]

## 2. What was built

- `state_pums.csv` — 51 states. Employed civilians 16+ (ESR 1,2) as denominator; guard labor split
  into **private guards** (OCCP 3930) and **public police/corrections** (3870 police officers,
  3820 detectives/criminal investigators, 3801 bailiffs/correctional officers/jailers, 3900 private
  detectives). Foreign-born share (NATIVITY=2), Hispanic share (HISP≠01), Black share (HISP=01 &
  RAC1P=2), and a Herfindahl fractionalization index over {Hispanic-any-race} ∪ {non-Hispanic × RAC1P}.
- `state_finance.csv` — 2022 state+local direct expenditure on police protection and on correction,
  Census `timeseries/govslocalfin`. Per capita using the PUMS population.
- `state_crime_2019.csv` — FBI UCR 2019 Table 5 state violent crime rate per 100,000, all 51.
- `panel.csv` — merged analysis file. `regressions.txt` — full output. Scripts: `pull_pums.py`,
  `pull_finance.py`, `regress.py`. All API responses cached in `_cache/` (gitignored).

Descriptives: guard share of employment mean 0.556% (range 0.24% Vermont → 1.39% Nevada);
police/corrections share mean 0.625%; police $394.9/capita, corrections $268.3/capita.

## 3. Regressions (OLS, n=51, controls = log median HH income, poverty rate, urban share, Black share, 2019 violent crime rate)

| Outcome | Regressor | Bivariate b (se) | With controls b (se) |
|---|---|---|---|
| Guard share (pp) | Foreign-born share | **0.0231 (0.0043)** p<.001 | **0.0196 (0.0070)** p=.008 |
| Guard share | Hispanic share | 0.0089 (0.0031) p=.005 | −0.0004 (0.0037) p=.91 |
| Guard share | Fractionalization | **0.0119 (0.0015)** p<.001 | **0.0084 (0.0027)** p=.003 |
| Police/corr employment share | Foreign-born share | 0.0042 (0.0032) p=.19 | 0.0116 (0.0059) p=.054 |
| Police/corr employment share | Fractionalization | 0.0042 (0.0012) p=.001 | 0.0075 (0.0021) p=.001 |
| Police $/capita | Foreign-born share | 10.88 (2.45) p<.001 | 1.74 (3.22) p=.59 |
| Police $/capita | Fractionalization | 4.22 (1.04) p<.001 | **−2.48 (1.20) p=.045** |
| Police+corrections $/capita | Foreign-born share | 15.67 (3.99) p<.001 | 4.86 (5.70) p=.40 |
| Police+corrections $/capita | Hispanic share | 7.55 (2.58) p=.005 | 3.08 (2.74) p=.27 |
| Police+corrections $/capita | Fractionalization | 6.20 (1.67) p=.001 | −1.14 (2.23) p=.61 |

Dropping the Black-share control changes almost nothing here (full table in `regressions.txt`), so
the usual artefact warning applies less than expected: in these data foreign-born share and Black
share are essentially orthogonal (r = 0.07). The variable that does the damage is **urban share**,
which correlates 0.81 with foreign-born share.

Effect size on the surviving result: one standard deviation of foreign-born share (6.2 pp) predicts
+0.12 pp of guard share, about half a standard deviation of the outcome. Not trivial if causal.

## 4. The result that kills the strong reading

Nevada (1.39% guard share), Hawaii (1.21%) and DC (1.13%) are the top three. OCCP 3930 bundles
**gaming surveillance officers** with security guards, so Nevada is mechanically loaded; Hawaii and
DC are tourism and federal-facility economies. Dropping those three:

| Outcome | Regressor | Bivariate | With controls |
|---|---|---|---|
| Guard share | Foreign-born share | 0.0160 (0.0031) p<.001 | 0.0092 (0.0042) **p=.033** |
| Guard share | Hispanic share | 0.0070 (0.0021) p=.002 | 0.0003 (0.0020) p=.89 |
| Guard share | Fractionalization | 0.0088 (0.0010) p<.001 | **0.0026 (0.0023) p=.27** |

Fractionalization — the measure the trust literature actually theorizes about — goes to zero.
Foreign-born share halves but stays marginally significant. Hispanic share is null throughout.
A claim that survives only with three casino/tourism/capital outliers in the sample is not a claim.

## 5. Why none of this identifies anything [FRAMING-SENSITIVE]

Cross-sectional and confounded, by construction. Foreign-born share is 0.81 correlated with urban
share; guards are an urban occupation for reasons having nothing to do with trust (density of
retail, offices, transit, stadiums, casinos). Immigrants also *sort into* guard work — the estimate
partly measures labor supply into the occupation, not demand for coercion. Reverse causality and
state fixed characteristics (climate, tourism, federal presence) are unaddressed. The brief's own
warning about the Black-share control is correct in general but not binding here; the urbanization
confound is the live one.

Bowles & Jayadev's own measure is broader than mine (they include supervisors, the unemployed, and
the military as "guard labor"); this is a narrow security-occupation reading of it.
[SOURCE: Bowles & Jayadev 2006, J. Development Economics 82(2); Jayadev & Bowles, "Estimating Guard Labor", UMass WP 2007]

## 6. Literature: is there a credible design?

Yes, one, and it cuts *for* the claim on the public-spending margin — in Italy, not the US.

- **Bove, Elia & Ferraresi (2021), "Immigration, Fear of Crime, and Public Spending on Security,"
  Journal of Law, Economics & Organization, doi:10.1093/jleo/ewab021.** 7,000+ Italian municipalities,
  2003–2015. Shift-share instrument built on the EU enlargement shock, plus a historical-Fascist-era
  migration instrument. Quoted: *"We find that immigration increases spending on police protection,
  such as enhanced police presence and surveillance. On average, the amount of spending allocated to
  local security increases by 0.12-0.30 percentage points for one point increase in the share of
  immigrants... the higher the [genetic, linguistic or religious] distance the stronger the impact of
  immigration on law enforcement spending."* This is the single best-identified paper on the exact
  question, and it supports the mechanism — including the cultural-distance gradient. It measures
  *budget share* in a country with small municipal budgets, so it does not transfer cleanly to US
  per-capita dollars. My US null on public spending and their Italian positive are not directly
  comparable designs; theirs is the better one.
- **Brady & Fink, "Immigration and Preferences for Greater Law Enforcement Spending in Rich
  Democracies"** — the attitudinal analogue: immigration growth and preferences for punitive social
  control. Preferences, not expenditure.
- **Hines & Peri, "Immigrants' Deportations, Local Crime and Police Effectiveness"** (Secure
  Communities, PUMA-level) — runs the opposite direction: enforcement → crime and clearance rates.
  Relevant to the causal tree, not to guard-labor demand.
- **Jaeger, Ruist & Stuhler (NBER w24285), "Shift-Share Instruments and the Impact of Immigration"** —
  the standing methodological caution: the Card-style instrument conflates short- and long-run
  responses. It applies to Bove et al. too.
- I found **no** paper estimating immigrant share → *private* security employment with a credible
  design, in the US or elsewhere. That is the gap the X post asserts an answer to.
  Besley & Mueller (2018, AEJ Macro) model firm-level guard labor against predation across 144
  countries, but the regressor is predation, not diversity.

## 7. What was not done

- **PUMA/metro level: not attempted.** The state pass consumed the turn budget. The `tabulate`
  endpoint takes `&for=public%20use%20microdata%20area:*&in=state:XX`, so this is a mechanical
  extension of `pull_pums.py` and would give ~2,400 units and real within-state variation. That is
  the single highest-value next step and it would let an urban-fixed-effect specification separate
  density from diversity, which is exactly what the state-level design cannot do.
- `ST` is **not** a valid `tabulate` dimension on the 5-year PUMS API (error: `unknown dimension
  variable: 'ST'`). Geography must go through `&for=state:XX`, one call per state.
- FBI CDE API requires an api.data.gov key not present in `acquire/config.local.env`; DEMO_KEY is
  rate-limited and `ucr.fbi.gov` is Cloudflare-gated to plain curl. Table 5 was retrieved via
  Firecrawl and parsed; values spot-check against the published table.

Nothing was committed. Lane: `infra/immigration-fiscal/guard_labor_2026_09_16/`.
