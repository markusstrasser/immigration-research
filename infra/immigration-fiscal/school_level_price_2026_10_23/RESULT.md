**Verdict:** The school-level data confirm the proposed district correction, not a larger one. The
group's pupils attend schools that spend **5.9% more than the national average** and **12.4% more than
the schools white pupils attend**, but almost all of that is *between* districts and states, not
*within* them. The within-district gap is **0.1%** (median k = 1.001). The Hispanic-weighted
*within-state* correction is **1.027**, against the proposed district k = 1.034; the national 1.059 is
mostly the state mix the case already prices. [CALCULATION: `build.py`; CCD SCH_052_2122 membership ×
SLFS FY2022 school spending; 91,955 schools, 47.9M members, 13.4M Hispanic]

## What was built

The `school_cost_where_enrolled_2026_09_24` lane priced each group pupil at its **state's** average
spending per pupil and proposed a district correction k = 1.034. This lane goes one level finer: the
**school the pupil attends**, using the two files already in that lane's cache.

- **CCD SCH_052_2122**: school membership by race/ethnicity, 2021–22.
- **SLFS FY2022**: school-level current expenditures (`TCURELSCS`) and membership (`MEMBER`).
- Merge on `NCESSCH`; 91,955 schools with both, 47.9M members, 13.4M Hispanic (28.1%).

The CCD reports **Hispanic**, not Mexican origin. In the high-Mexican-share states the Hispanic
reading is close to the group; elsewhere it is a broader Hispanic proxy. SLFS is a sample, not the
universe, and FY2022 current expenditures carry COVID relief.

## The price ladder

Per-pupil current expenditures, SLFS sample, FY2022 dollars:

| Population | Per-pupil spending | Ratio to national |
|---|---:|---:|
| National (all pupils) | $12,863 | 1.000 |
| Hispanic-weighted | **$13,624** | **1.059** |
| White-weighted | **$12,116** | **0.942** |
| Hispanic vs white | — | **1.124** |

So the group's pupils are in schools that spend 5.9% more than the national average, and white pupils
in schools that spend 5.8% less. The relative gap is 12.4%.

## The shares: the group is the base, not an add-on

The group is not a small minority being added to a fixed system. Hispanic pupils are **52.7% of
Texas pupils**, **56.1% of California's pupils**, **74.1% of Los Angeles Unified's pupils**, **61.8%
of Houston ISD's** and **70.0% of Dallas ISD's**. The Mexican-origin share of Texans under 30 was **38.0%** in
2023 (41.1% in 2010). In these places the school system is sized around the group, so the 0.836
"fixed overhead" reading is least applicable exactly where the group is largest; the 1.0 central is
the right reading there. The 12.4% national gap against whites is therefore a comparison between the
group's urban-majority districts and the rural/small-town districts where white pupils are
disproportionately concentrated, not a within-district transfer.

## The response by state: CA and TX are ~0.92, not 0.836

The scaling lane's 0.836 is a **national** within-district average. Run separately by state on the
SLFS/CCD school merge (log current expenditures on log membership, district fixed effects, pupil
weighted), the high-share states are closer to proportional:

| State | Within-district elasticity | 95% CI |
|---|---:|---|
| CA | **0.919** | [0.884, 0.954] |
| TX | **0.922** | [0.907, 0.937] |
| AZ | 0.903 | [0.868, 0.939] |
| NY | 0.868 | [0.838, 0.897] |
| IL | 0.913 | [0.848, 0.978] |
| FL | 0.807 | [0.781, 0.833] |
| GA | 0.781 | [0.761, 0.801] |
| NC | 0.748 | [0.719, 0.777] |
| National pooled | 0.895 | [0.885, 0.905] |
| Hispanic-weighted state average | **0.899** | — |

So the 0.836 low side is a national average that **understates** the response in CA and TX. The
differentiated ensemble is 0.75–0.95 by state, with the group's high-share states at **0.90–0.92**.
The national pooled SLFS estimate (0.895) is above the scaling lane's F-33 panel estimate (0.836);
the difference is the sample and measure (school-level FY2022 vs district F-33 2000–2019), not a
contradiction.

## Does this change the bottom line?

No. The share finding is **interpretation**: the group is the majority of pupils in the high-share
places, so the 1.0 central is the right reading there and the 0.836 low side is a small-district
average. The price finding (k = 1.034) is a **+$2.8–3.7bn** correction on the September 24 case
(about 1%), and the response finding (CA/TX ~0.92 vs 0.836) supports the central rather than the low
side. The headline stays **$368.0–436.6bn**; adopting k = 1.034 would put it at roughly
**$371–440bn**, a ~1% move. The sign and the order of magnitude do not change.

## The decomposition: between states, between districts, within districts

| Margin | Ratio | Reading |
|---|---:|---|
| National Hispanic / national average | 1.059 | raw national gap |
| Hispanic-weighted state k (within state) | **1.027** | the state mix is already in the case's key |
| Within-district k, median | **1.001** | IQR [0.996, 1.009] |
| State k, median | 1.013 | IQR [0.993, 1.036] |

The gap is almost entirely **between districts and states**:

- **Between states:** 1.059 / 1.027 ≈ 1.031. The group is concentrated in higher-spending states in
  this sample (NY, AZ, CO, IL).
- **Between districts within states:** 1.027 / 1.001 ≈ 1.026.
- **Within districts:** 1.001. The group's pupils attend schools that spend about the district average.

The case's state-priced key already carries the between-state part. The correction that belongs on
top is the within-state district/school part, **~1.03** — which is the proposed k = 1.034, not the
national 1.059.

## The states and districts

Hispanic-weighted k by state (selected):

| State | k Hispanic | k white | k relative |
|---|---:|---:|---:|
| NY | 1.082 | 0.913 | 1.186 |
| AZ | 1.047 | 0.917 | 1.143 |
| CO | 1.037 | 0.969 | 1.070 |
| TX | 1.035 | 0.954 | 1.086 |
| IL | 1.033 | 0.944 | 1.095 |
| NV | 1.019 | 0.993 | 1.026 |
| CA | 1.013 | 0.949 | 1.067 |
| FL | 1.013 | 0.954 | 1.061 |
| NM | 0.989 | 0.966 | 1.024 |

The bottom states are Alaska (0.901), New Hampshire (0.914), Montana (0.929), North Dakota (0.937) and
West Virginia (0.954) — small Hispanic populations, so noisy.

Within-district k for the large districts:

| District | k within |
|---|---:|
| Los Angeles Unified | 1.017 |
| Houston ISD | 1.009 |
| Dallas ISD | 0.990 |
| Fresno Unified | 1.004 |
| Miami-Dade | 0.970 |
| Chicago SD 299 | 0.965 |
| Clark County (NV) | 1.016 |
| San Antonio ISD | 0.996 |
| El Paso ISD | 1.005 |

New York City's geographic districts are the exception: 1.09–1.16, because the LEA is a geographic
sub-district and the group's pupils sit in higher-spending sub-districts. That is a between-district
effect inside the city, not within-school sorting.

## What it changes

- **The proposed k = 1.034 is confirmed.** The within-state correction is 1.027, and the within-district
  component is ~1.001. The school-level data do not justify a larger correction.
- **The national 1.059 is not the right correction** for a state-priced key, because it includes the
  between-state mix the key already carries. Applying 1.059 would double-count the state mix.
- **The relative gap vs whites is 12.4%**, but it is a between-district/state gap, not a within-school
  gap. That matters for the interpretation: the group's pupils are not in systematically better-funded
  schools *within* their districts; they are in higher-spending districts and states.
- **The big districts are at or near their district averages** (LA 1.017, Houston 1.009, Dallas 0.990,
  Fresno 1.004), so the "where inside the district" correction is small.

## Limits

- CCD has **Hispanic**, not Mexican origin; the group is a proxy.
- SLFS is a **sample** (91,955 of ~100k schools), not the universe.
- FY2022 current expenditures carry **COVID relief** and exclude capital; the `school_cost_where_enrolled`
  lane's ASSF FY2024 measure gives different levels (R = 0.954), so the levels are not comparable across
  the two lanes. The **ratios** within each measure are the object.
- The `k` is a price, not a response. The elasticity question (1.0 vs 0.836) is separate and is
  answered in `scaling_test_2026_09_20`.

## Reproduce

```sh
uv run --no-project python3 infra/immigration-fiscal/school_level_price_2026_10_23/build.py
uv run --no-project python3 -m pytest infra/immigration-fiscal/school_level_price_2026_10_23/ -q
```

Inputs are unzipped from `school_cost_where_enrolled_2026_09_24/_cache/` into this lane's ignored
`_cache/`. Outputs are `derived/state_k.csv`, `derived/district_k.csv` and `derived/summary.json`;
the three intermediate tables (`ccd_school_2122.csv`, `slfs_school_2122.csv`, `school_merge.csv`)
stay in the ignored `_cache/`.
