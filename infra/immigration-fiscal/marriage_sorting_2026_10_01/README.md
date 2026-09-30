# Marital sorting after accounting for peer-group composition

Date: 2026-10-01. Mode: descriptive estimate and sensitivity analysis.

**Result:** Indian G2's opportunity-adjusted same-origin marriage odds index is
**4.05–5.38 times the native non-Hispanic white index**, across four full-period
age/education specifications with and without earnings and with married versus
all-adult pools. The corresponding native black range is **3.82–7.50**. Indian G2
versus black ranges **0.63–1.41**, so their ranking is not robust. These are ratios
of a descriptive sorting index, not measured psychological racism or identified
individual ethnic preferences. [CALCULATION: `derived/estimates.csv`]

## Principal result

The principal specification uses married people in the same survey year/state,
opposite sex, and the **actual spouse's** age, education and earnings categories.
Both members of the observed marriage must be 25–54. Categories are ages 25–39 /
40–54; less than BA / BA+; and annual earnings nonpositive / positive below
$75,000 / at least $75,000. Earnings are preceding-income-year nominal dollars,
and matching is within survey year. The coarse earnings bands are sensitivity
controls, not an inflation-adjusted earnings gradient. [METHOD]

| Respondent group | Person-year records | Same-group spouse, p | Expected share, q | Odds index K | K / native-white K |
|---|---:|---:|---:|---:|---:|
| Indian G2 | 333 | 65.9% | 9.6% | 18.22 | 4.05 |
| Native NH white | 70,604 | 90.8% | 68.6% | 4.50 | 1.00 |
| Native NH black | 5,497 | 83.5% | 15.0% | 28.51 | 6.34 |
| Mexican G2 | 3,478 | 72.3% | 32.3% | 5.47 | 1.22 |
| Mexican G3+ | 3,636 | 55.7% | 29.0% | 3.09 | 0.69 |
| Indian G1, descriptive context | 2,951 | 96.3% | 12.3% | 188.30 | 41.86 |
| NH white G2 | 2,754 | 85.7% | 64.0% | 3.36 | 0.75 |
| NH black G2 | 297 | 73.0% | 12.1% | 19.69 | 4.38 |

[CALCULATION: `estimates.csv`, `window=2022-2025`,
`spec=married_age_education_earnings`, `sex=both`.]

For each respondent i, q_i is the weighted same-group share in their comparison
cell. Then p = mean_w(same-group spouse), q = mean_w(q_i),
K = [p/(1-p)] / [q/(1-q)]. Ratios divide K by the comparator's K. A white-relative
value of 1 means the white level, **not random mixing**: the white K itself is
4.50. K is an aggregate odds-inflation index. With heterogeneous q_i, it is not
the common coefficient in a fitted individual offset-logit choice model. [ALGEBRA]

The saved alternatives p/q and (p-q)/(1-q) answer different questions. On the
latter (fraction of random-benchmark outmarriage absent), the principal values
are Indian G2 **0.623**, white **0.706**, black **0.805**. Thus the Indian-above-white
result is robust to these peer-pool choices **on the odds scale**, not a universal
ranking across sorting measures. The odds scale is selected for the user's
question about within-group versus outside-group matching relative to availability;
it does not make the psychological construct identified. [CALCULATION; FRAMING-SENSITIVE]

## Sensitivity and uncertainty

| Peer specification | Indian G2 / white | Native black / white | Mexican G2 / white | Mexican G3+ / white |
|---|---:|---:|---:|---:|
| Married, spouse age + education | 4.71 | 7.50 | 1.20 | 0.65 |
| Married, spouse age + education + earnings | 4.05 | 6.34 | 1.22 | 0.69 |
| All adults, spouse age + education | 5.38 | 3.82 | 1.03 | 0.55 |
| All adults, spouse age + education + earnings | 4.63 | 3.88 | 1.08 | 0.59 |

[CALCULATION: same CSV, full period/both sexes. The range is between specified
constructions; it is not a confidence interval and does not cover all conceivable
models or actual encounter networks.]

- Principal Indian/white ratio: **4.05**, approximate conservative 95% interval
  **2.37–6.92**. All four adjusted Indian/black intervals include 1. Mexican G2's
  all-adult white comparisons also have intervals including 1; do not claim a
  robust Mexican G2-above-white ranking. [CALCULATION]
- Indian G2/native-white ratios are **4.28 for men** and **3.80 for women** in the
  principal specification. This compares men with white men and women with white
  women. The two-period estimates are **2.87 in 2022–23** and **5.97 in 2024–25**.
  Small-sample variation and composition can explain a difference; this is not
  an identified time trend or independent replication. [CALCULATION; INFERENCE]
- Using **white G2 as the reference**, Indian G2 ranges **5.42–7.49** and black G2
  **3.38–6.29** across the four adjusted constructions. National-origin versus
  broad-race boundaries remain different. [CALCULATION]
- Unadjusted state-only ratios are Indian/white **7.13** with a married pool and
  **8.52** with all adults. The all-adult pool using the respondent's own age,
  education and earnings gives **4.88**. That last specification excludes actual
  spouses differing in these characteristics from their partner's candidate
  pool; it is a peer-exposure counterfactual, not the principal spouse-matched
  null. Its exclusions and spouse-ineligibility shares are in diagnostics.
  [CALCULATION; METHOD]
- Indian G1's very high index is context only: marriages may have formed before
  immigration, and current US availability does not reconstruct that market.
  The US opportunity objection is particularly consequential for this row.
  [IDENTIFICATION LIMIT]

All generated specifications, sexes and both two-year windows are retained in
`estimates.csv`; none are selected away. The four headline constructions vary
the two specific material choices: conditioning on earnings and conditioning
the peer pool on marriage. [METHOD]

**Uncertainty:** every q_i and p is recalculated under the 160 CPS replicate
weights. For each year, replace only that year's sufficient statistics with its
replicate version and hold other years at full weights. Calculate that year's
replicate SE contribution to the pooled statistic using 4/160 times squared
deviations, then sum the four SE contributions. This is a first-order
worst-covariance bound across years, accounting conservatively for unknown
overlap covariance. Comparator groups change jointly in each replicate, so
shared-reference covariance is retained. Intervals for K and ratios use the log
scale. These are conservative approximate intervals, not exact finite-sample
coverage guarantees for nonlinear statistics with estimated sparse-cell shares.
[METHOD; SOURCE: Census replicate guidance and IPUMS pooling warning below]

## Population, cells and limitations

The lane reuses the four hash-verified 2022–2025 ASEC archives, weight joins,
spouse links and origin definitions from the
[existing marriage analysis](../civic_trajectory_mexican_2026_09_27/RESULT.md#2-intermarriage-by-generation-cps-asec-20222025).
This window preserves the existing four-year series and increases the small
Indian G2 sample; the two half-windows test period sensitivity. No claim is made
about 2026 marriages. No new raw data are acquired or modified. [PROVENANCE]

- Indian origin = India-born, India-born parent, or Asian-Indian identification;
  Mexican origin = Mexico-born, Mexico-born parent, or Mexican Hispanic origin.
  Indian G2 excludes Mexico-parent overlap, following the existing code.
- Native = `PRCITSHP` 1–3, including US territories and people born abroad to US
  parents; **native is not strictly US-born**. G2 has a parent born in the named
  origin. White/black reference groups are native, non-Hispanic, single-race,
  and exclude Indian/Mexican-parent overlap. White/black G2 requires a reported
  parent birthplace code 100–899, excluding unknown/unspecified entries. These
  indicator boundaries are not an exhaustive common ancestry partition.
- The principal restriction keeps **333 of the prior 345 Indian G2 person-year
  records**: twelve have a spouse outside 25–54. No principal peer-cell drop
  occurs. Records are not independent people; spouses and repeated survey
  households contribute multiple observations. [DATA]
- In the main Indian G2 sample, the ego-weighted mean comparison-cell n is **72.3**
  (mean weight-effective n **65.9**); **10.3%** of weighted egos face cells with
  fewer than 20 records. **7.1%** face cells with no sampled Indian candidate.
  The actual spouse contributes to cell marginals; small cells can mechanically
  pull observed and expected composition together. No smoothing or clipping is
  used. The less-saturated age/education result is therefore load-bearing.
  All nonpositive replicate denominators or shares outside [0,1] fail loudly.
  [DATA; METHOD]
- `pool_diagnostics.csv` retains weighted cell-size/effective-size summaries,
  zero/one-share exposure, sample exclusions and actual-spouse-ineligibility for
  own-stratum pools for every group, sex, year and construction. Missing own-pool
  records are visibly marked `[DEGRADED]`; principal pools must exist. [METHOD]

This answers whether current marriage composition departs from an explicit
demographic random-draw benchmark. It does **not** observe actual school,
workplace, friendship or matchmaking encounters. Income, residence and marriage
are potentially jointly determined; adding earnings is not automatically a
better causal control. Restricting to married candidates conditions on marriage
selection, while all adults includes people not currently seeking a spouse.
Neither pool is the historical partner market. Person weights make this a
random-draw benchmark, not an exact one-to-one population permutation. [LIMITS]

Intentional ethnic introductions or family restrictions can contribute to total
sorting. The present data cannot allocate the observed outcome among the focal
person, their family, other groups' acceptance, or correlated religion/language.
To identify an individual ethnic preference would require actual exposed
alternatives and outgoing choices separately from reciprocation, with suitable
identifying variation. [IDENTIFICATION LIMIT]

## Reproduce and verify

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/marriage_sorting_2026_10_01/sorting.py
uv run --no-project python3 -m pytest infra/immigration-fiscal/marriage_sorting_2026_10_01/test_sorting.py -q
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/marriage_sorting_2026_10_01 \
  "uv run --no-project python3 {lane}/sorting.py" \
  "uv run --no-project python3 -m pytest {lane}/test_sorting.py -q"
```

Outputs are ignored and rederivable: `estimates.csv`, `pool_diagnostics.csv`,
`legacy_parity.csv`, `replicate_totals.csv`, `manifest.json`. The manifest pins
input and generator hashes. Legacy gates reproduce four original counts and
same-origin-spouse rates before applying the new both-spouse age restriction.
Tests cover the random-mixing null, reference covariance, within-replicate pool
recalculation, own-versus-spouse strata, and invalid denominators. [VERIFICATION]

Quantitative-bias checks: person-year denominator and conditional estimand are
explicit; the headline carries a construction range; periods and sexes are
retained; model output is not relabeled preference; thin cells, endogenous
earnings, marital selection, ancestry-boundary mismatch, and year overlap are
visible. The leading falsifier for the narrow descriptive result is disappearance
of the Indian/white excess under a defensible measured-exposure comparison; no
such exposure data were used here. LLM interpretation may be politically biased;
the numerical construction and caveats are applied symmetrically to groups.
[SELF-AUDIT; FRAMING-SENSITIVE]

Code-review disposition: Composer's repeated `PCOLS` append finding was fixed
by making configuration idempotent. Own-pool omissions are deliberate diagnostic
exclusions, now also printed as degraded; actual-spouse pools fail if missing.
Legacy unrestricted-age parity is deliberately separate from the new analysis
universe. Numeric formatting and scoped performance-warning suggestions do not
alter the estimates. [REVIEW]

## Primary sources and methodological references

- [Census ASEC datasets](https://www.census.gov/data/datasets/time-series/demo/cps/cps-asec.html)
  and [2025 codebook](https://www2.census.gov/programs-surveys/cps/datasets/2025/march/asec2025_ddl_pub_full.pdf):
  spouse pointer, race, parental nativity, education and person earnings fields.
- [2024 Census technical documentation](https://www2.census.gov/programs-surveys/cps/techdocs/cpsmar24.pdf):
  160 successive-difference replicates and the 4/160 variance factor.
- [IPUMS replicate-weight guidance](https://cps.ipums.org/cps/repwt.shtml) and
  [IPUMS pooled-ASEC warning](https://forum.ipums.org/t/weighting-asec-pooled-data-accounting-for-repeating-records/854/1):
  do not assume identically numbered annual replicates handle repeated households.
- [Currarini, Jackson and Pin, PNAS 2010](https://web.stanford.edu/~jacksonm/currarini-jackson-pin-PNAS-2010.pdf),
  DOI 10.1073/pnas.0911793107: method distinction between meeting and choice.
  Their high-school friendship estimates are not imported as Indian marriage
  estimates or as validation of this lane's index.
