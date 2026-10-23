**Verdict:** The school-level data support a within-state correction of about **1.03** on the
state-priced key, not the national 1.059. The group's pupils attend schools that spend 5.9% more
than the national average and 12.4% more than white pupils' schools in the SLFS measure, but that is
mostly a between-state and between-district composition gap. The group-weighted **within-district**
factor is **1.005** (1.037 excluding single-school districts and New York City), not zero: the
unweighted median 1.001 was misleading because 4,531 of 15,949 districts are single-school and have
k = 1 by construction. The state-level cross-school gradient (0.75–0.92) is a **size gradient, not
the response elasticity**; the 0.836 panel response remains the relevant one for the case.
[CALCULATION: `build.py`, `state_elasticity.py`; CCD SCH_052_2122 membership × SLFS FY2022 school
spending; 91,955 schools, 47.9M members, 13.4M Hispanic]

## What was built

The `school_cost_where_enrolled_2026_09_24` lane priced each group pupil at its **state's** average
spending per pupil and proposed a within-state correction k = 1.034 (its own build: R_state 1.0284 ×
within-district 1.0057). This lane goes one level finer: the **school the pupil attends**, using the
two files already in that lane's cache.

- **CCD SCH_052_2122**: school membership by race/ethnicity, 2021–22.
- **SLFS FY2022**: school-level current expenditures (`TCURELSCS`) and membership (`MEMBER`).
- Merge on `NCESSCH`; 91,955 schools with both, 47.9M members, 13.4M Hispanic (28.1%).

The CCD reports **Hispanic**, not Mexican origin. In the high-Mexican-share states the Hispanic
reading is close to the group; elsewhere it is a broader Hispanic proxy. SLFS is a voluntary state
collection, not a sample; it covers about 97% of pupils. FY2022 current expenditures carry COVID
relief and exclude capital and district-level costs.

## The price ladder

Per-pupil current expenditures, SLFS sample, FY2022 dollars:

| Population | Per-pupil spending | Ratio to national |
|---|---:|---:|
| National (all pupils) | $12,863 | 1.000 |
| Hispanic-weighted | **$13,624** | **1.059** |
| White-weighted | **$12,116** | **0.942** |
| Hispanic vs white | — | **1.124** |

So the group's pupils are in schools that spend 5.9% more than the national average, and white pupils
in schools that spend 5.8% less. The relative gap is 12.4%. **Both are composition gaps**, not a
within-school transfer; the locale and wage splits are not yet computed.

## The group-weighted chain

The medians hide the weighting. The chain is exact:

| Level | Group-weighted spending per pupil | Factor |
|---|---:|---:|
| P0 national | $12,863 | — |
| P1 state | $13,268 | **between states 1.031** |
| P2 district | $13,552 | **between districts 1.021** |
| P3 school | $13,624 | **within districts 1.005** |

The product is 1.031 × 1.021 × 1.005 = **1.059**. The **within-district factor is 1.005 (0.5%)**,
not 0.1%; excluding single-school districts and New York City it is **1.037 (3.7%)**. The unweighted
median 1.001 was misleading: 4,531 of 15,949 districts are single-school, and a single-school
district has k = 1 by construction.

## The within-district gap is small but not zero

- **LAUSD** is 74.1% Hispanic with k = 1.017. That implies non-Hispanic pupils sit at
  `(1 − 0.741 × 1.017) / 0.259 = 0.951`, so the group's schools spend about **6.9% more than other
  LAUSD pupils' schools**. The ratio to the district average is the right number for the key; it
  does not support "not in systematically better-funded schools within their districts."
- **Houston** 1.009, **Dallas** 0.990, **Fresno** 1.004, **Miami-Dade** 0.970, **Chicago** 0.965.
- **New York City's geographic districts** are 1.09–1.16 **within each sub-district**, so the cause
  is not "higher-spending sub-districts." It is unresolved; likely grade span, special-education and
  transfer-school composition inside the geographic districts, and how the citywide special-education
  and alternative districts (D75/D79) are coded.
- The interpretation should use the **group-vs-everyone-else** ratio, not the ratio to the district
  average alone.

## The shares: Hispanic, not Mexican-origin

| Place | Hispanic share of pupils |
|---|---:|
| National | 28.1% |
| Texas | 52.7% |
| California | 56.1% |
| Houston ISD | 61.8% |
| Dallas ISD | 70.0% |
| Miami-Dade | 73.3% |
| Los Angeles Unified | 74.1% |

The Mexican-origin share of Texans **under 30** was **38.0%** in 2023 (41.1% in 2010) — a plurality,
not a majority. The shares are Hispanic, and Mexican origin is about 80–85% of Hispanics in Texas and
California; LAUSD and Houston also have large Central American enrollment.

The share does **not** set the marginal response. With a constant elasticity, the group's average
cost relative to average spending per pupil is `[1 − (1 − s)^β] / s`. At β = 0.836 that is **0.88 at
s = 0.5** and **0.91 at s = 0.74**. A high share pushes the finite-removal response toward 1 but does
not reach it. The 1.0 central is a policy choice, not a share implication.

## The cross-school size gradient by state (not a response)

| State | Within-district gradient | 95% CI |
|---|---:|---|
| CA | 0.919 | [0.884, 0.954] |
| TX | 0.922 | [0.907, 0.937] |
| AZ | 0.903 | [0.868, 0.939] |
| NY | 0.868 | [0.838, 0.897] |
| IL | 0.913 | [0.848, 0.978] |
| FL | 0.807 | [0.781, 0.833] |
| GA | 0.781 | [0.761, 0.801] |
| NC | 0.748 | [0.719, 0.777] |
| National pooled | 0.895 | [0.885, 0.905] |
| Hispanic-weighted state average | 0.899 | — |

This is a **cross-sectional size gradient** with district fixed effects, not a response to an added
pupil. It holds the district budget fixed and leaves out central overhead, which is exactly the fixed
cost behind the 0.836 reading. The 0.836 is a panel response; 0.836 → 0.895 is the quantity change,
and 0.895 → 0.92 is state variation. The group variation is 0.899 vs 0.895, a difference of 0.004.
**Do not use the 0.92 as the case's response.** If state differences in the response matter, run the
F-33 panel by state with district and year fixed effects.

## Does this change the bottom line?

No. The within-state correction is **1.027** (1.031 × 1.021 × 1.005), against the proposed 1.034.
The lane's 1.034 already includes the within-district factor (1.0284 × 1.0057), and my 1.0053 matches
that 1.0057, so the two are consistent. The dollar correction is **+$2.8–3.7bn on the September 24
base** (0.76–0.85% of that case); on v9 the K-12 line is not separately exported, so the correction is
roughly **+$2–4bn, under 1%**. The headline stays **$368.0–436.6bn**; adopting k = 1.034 would put it
at roughly **$371–440bn**. The sign and order of magnitude do not change.

## Confounders and measure

- **District-level costs:** SLFS excludes them. Its $12,863 per pupil compares with about $15.6k
  Census total current spending, so roughly 18% is not allocated to schools. Applying a school-level
  ratio to ASSF totals assumes the overhead follows the same within-state pattern; the R = 0.954
  across states does not test that.
- **COVID relief (ESSER):** it followed Title I shares into high-poverty districts, pushing
  between-district k up. Much was spent centrally, which SLFS excludes, so the within-district factor
  is less affected.
- **Enrollment drops:** FY2022 enrollment fell under hold-harmless budgets (CA, TX), inflating
  per-pupil spending in the big urban districts where the group concentrates, also pushing k up.
- **Categorical funding:** k includes Title I/III, Texas bilingual and compensatory allotments, and
  California's LCFF supplemental and concentration grants. If the case prices ELL or poverty costs
  separately, k double-counts them.
- **Capital:** excluded from both measures; construction driven by enrollment is a real marginal cost
  neither measure captures.
- **Hispanic proxy:** between states it overweights NY, VA, MA, NJ and FL (non-Mexican Hispanic), which
  biases k up for the group; within TX, CA and AZ the direction is unclear. If the group means
  immigrant generations, the all-generation proxy probably understates k.

## Limits

- CCD has **Hispanic**, not Mexican origin; the group is a proxy.
- SLFS is a **voluntary state collection**, not a sample; coverage is about 97% of pupils, and Arizona
  looks low (408,910 Hispanic pupils matched against roughly 0.5M in CCD). Missing charters are a
  likely cause and would bias the group's k up.
- FY2022 current expenditures carry **COVID relief** and exclude capital and district-level costs.
- The `k` is a price, not a response. The elasticity question (1.0 vs 0.836) is separate and is
  answered in `scaling_test_2026_09_20`.

## Reproduce

```sh
uv run --no-project python3 infra/immigration-fiscal/school_level_price_2026_10_23/build.py
uv run --no-project python3 infra/immigration-fiscal/school_level_price_2026_10_23/state_elasticity.py
uv run --no-project python3 -m pytest infra/immigration-fiscal/school_level_price_2026_10_23/ -q
```

Inputs are unzipped from `school_cost_where_enrolled_2026_09_24/_cache/` into this lane's ignored
`_cache/`. Outputs are `derived/state_k.csv`, `derived/district_k.csv`, `derived/state_elasticity.csv`,
`derived/state_elasticity_summary.json` and `derived/summary.json`; the three intermediate tables
(`ccd_school_2122.csv`, `slfs_school_2122.csv`, `school_merge.csv`) stay in the ignored `_cache/`.
