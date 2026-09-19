# Hedonic composition lane — result

**Verdict:** Saiz and Wachter's within-metro composition discount does **not** reproduce on
2013–2023 data, and the lane cannot put a defensible dollar figure on the compositional
amenity. Three independent checks break the naive reproduction. (1) The negative gradient
appears only when the price measure and the composition measure are drawn from the *same*
ACS sample: on identical ZCTA rows, identical controls and identical fixed effects, a
10-point rise in Hispanic share is worth **−0.96% in ACS median value and +0.84% in Zillow's
ZHVI** (t = −2.4 and +2.8). (2) The placebo fails: earlier price growth predicts *later*
composition change with the same negative sign (Hispanic share on value, −0.066, t = −4.5),
so sorting on pre-existing price trends is present. (3) The paper's own geographic-diffusion
instrument does not transfer: across the gravity arms the first-stage F runs 0.003 to 8.9
in the calibrated sample, against 76 to 362 in the paper, and the Hansen overidentification
test rejects at p < 0.001 in the specifications matching the paper's column 6, where the
paper's own test did not reject. Separately, ACS margins of error imply
that **about 80% of the within-metro variance in measured 5-year tract share changes is
sampling noise** (reliability 0.19–0.23), so the small raw coefficients are not evidence of
a small effect either. The honest output is a sign-ambiguous bound, not a price.

The metro-level demand effect reproduces cleanly and positively, confirming the two channels
operate at different levels: a foreign-born inflow equal to 1% of a metro's initial
population raises that metro's rents 1.32% (se 0.42) and values 3.43% (se 0.69).

---

## 1. What the paper actually says

Obtained as full text from the open-access Penn repository copy
(`_cache/saiz_wachter_2011.pdf`, 19 pp.). **The lane brief's citation was wrong**: the brief
gives *Review of Economics and Statistics* 93(1):169–188, DOI `10.1162/REST_a_00052`; that
DOI resolves to Cohen-Cole, "Credit Card Redlining." The paper is Albert Saiz and Susan
Wachter, "Immigration and the Neighborhood," *American Economic Journal: Economic Policy*
3(2), May 2011, 169–188, DOI `10.1257/pol.3.2.169`.

Their estimating equation, quoted verbatim from p. 173:

> "Δln ​P​i,M,T​ = ​α​M,T​ + λ ⋅ Δ​(IS​H​i,M,T​)​ + Δ​Z​i,M,T​ ⋅ A + ​X​i,M,T−10​ ⋅ B + ​ξ​i,M,T."

with, on the same page:

> "The regressions are weighted using the initial number of owner-occupied housing units in
> the neighborhood as weights, and standard errors are clustered at the tract level."

Headline magnitude, quoted from p. 175:

> "The results suggest that a change of one percentage point in the share of immigrants in a
> neighborhood is associated with a relative decrease of roughly 0.25 log points in the
> neighborhood's average housing value."

[SOURCE: Saiz and Wachter 2011, pp. 173–175.] The coefficient is in share units, so the
sentence's "0.25 log points" per percentage point reads as 0.25 **percent** per point, i.e.
about −2.5% per 10 points. Table 1 coefficients on Δ(foreign born/population):

| Column | 1 (FE only) | 2 (baseline) | 3 (+ mean reversion, pre-trends) | 4 (IV) | 5 (IV) | 6 (IV) |
|---|---|---|---|---|---|---|
| λ | −0.418 | **−0.246** | −0.244 | −0.323 | −0.211 | −0.214 |
| se | 0.016 | 0.015 | 0.015 | 0.136 | 0.050 | 0.054 |

Sample: 34,833 tract observations in 122 MSA-year groups, 1980–1990 and 1990–2000, in MSAs
where the decennial foreign-born increase was at least 5% of prior MSA population (67 MSAs
in 2000, holding 76.5% of metro immigration inflows). The instrument is a "gravity pull"
term, quoted from p. 178:

> "Our measure of gravity is a weighted average of lagged immigrant densities in neighboring
> communities, where the weights are directly proportional to the area of neighboring tracts
> and inversely proportional to their distance from the relevant neighborhood."

Two further points from the paper matter for reading this lane. First, they lead with OLS
after Table 1: "Hansen overidentification tests fail to reject exogeneity. Hausman tests fail
to reject that the IV and OLS parameters are equivalent and hence we deploy the latter in the
regressions below" (p. 179). Second, their own conclusion attributes the effect to ethnicity
and status rather than nativity (p. 187):

> "the negative association between immigration and local price growth may be driven more by
> the fact that immigrants tend to be of low socioeconomic status and to belong to minority
> groups, than by foreignness per se."

## 2. Coefficients, all arms

Tract long differences on fixed 2010 tract definitions, CBSA × period fixed effects, weighted
by initial owner-occupied units (values) or renter-occupied units (rents), clustered on CBSA.
Period A = ACS 2013 → 2018, period B = 2018 → 2023. Coefficients are per unit of share;
the percentage column is the effect of a **+10 percentage point** share change,
100 × (exp(0.10 λ) − 1). "Calibrated sample" keeps the CBSA-periods holding ≥76.5% of metro
foreign-born growth, the paper's coverage target (cutoff 1.08% of initial population over
five years; 169 of 758 CBSA-periods). The paper's own 5%-of-population threshold, halved to
2.5% for a five-year window, keeps only 35 CBSA-periods in this era and was abandoned.

**OLS, pooled, calibrated sample** (n = 43,659 rent / 45,369 value, 133 CBSA clusters):

| Treatment | Outcome | Baseline λ (se) | per +10 pts | + mean reversion λ (se) | per +10 pts |
|---|---|---|---|---|---|
| Hispanic share | rent | −0.0565 (0.0163) | −0.56% | −0.0304 (0.0154) | −0.30% |
| Hispanic share | value | −0.0413 (0.0212) | −0.41% | −0.0802 (0.0208) | −0.80% |
| Mexican-origin share | rent | −0.0826 (0.0173) | −0.82% | −0.0519 (0.0162) | −0.52% |
| Mexican-origin share | value | −0.1056 (0.0241) | −1.05% | −0.1401 (0.0257) | −1.39% |
| Foreign-born share | rent | +0.0046 (0.0157) | +0.05% | +0.0241 (0.0156) | +0.24% |
| Foreign-born share | value | +0.0459 (0.0199) | +0.46% | +0.0213 (0.0178) | +0.21% |

Full metro sample (n = 110,145 / 113,571, 381 clusters) gives the same picture: Hispanic
rent −0.0530, value −0.0501; Mexican rent −0.0626, value −0.0846; foreign-born −0.0066 and
+0.0117, both insignificant.

So the one part of Saiz and Wachter that survives contemporaneously is the part they
themselves emphasised: **the gradient attaches to ethnic composition, not to nativity.**
Foreign-born share has no relationship with either price in this period. But the
Hispanic-share gradient is 3–6× smaller than their −0.246, and sections 3 and 4 show it does
not survive its own robustness checks.

**IV arms.** Every instrument is weak, rejected, or both:

| Arm | Treatment | Outcome | λ (se) | first-stage F | Hansen J p |
|---|---|---|---|---|---|
| Gravity, paper col. 6 form | foreign-born | rent | −0.372 (1.013) | 7.1 | 0.000005 |
| Gravity, paper col. 6 form | Hispanic | value | +2.104 (2.630) | 0.90 | 0.119 |
| Gravity, paper col. 4 form | Hispanic | value | −2.154 (1.571) | 7.2 | — |
| Shift-share, 9 origin regions | foreign-born | value | +0.428 (0.304) | 38.4 | — |
| Shift-share | Hispanic | value | +0.108 (2.917) | 1.1 | — |

The gravity instrument depends on enclaves expanding into adjacent neighbourhoods. Mexican-born
counts summed over the sample tracts *fell* 3.0–3.4% over these windows (computed from the
same tract files; a metro-sample aggregate, not a national total),
so the diffusion process the instrument models is not running in this period. The shift-share
for Mexican origin is reported but is **not an instrument**: with one origin group it reduces
to the initial Mexican-born share times a scalar and carries no shift variation.

## 3. The disconfirming arms

**(a) Independent price measure reverses the sign.** The strongest test. On the ZCTA panel,
restricted to rows where both measures exist, the only thing that changes across a pair of
rows is where the price comes from:

| Treatment | Outcome pair | ACS median (same survey as regressor) | Zillow (independent) | n |
|---|---|---|---|---|
| Hispanic share | home value | −0.0964 (0.0394), t = −2.4 | **+0.0838 (0.0295), t = +2.8** | 27,654 |
| Mexican-origin share | home value | −0.1680 (0.0463), t = −3.6 | **+0.0732 (0.0362), t = +2.0** | 27,654 |
| Foreign-born share | home value | +0.0708 (0.0394) | +0.1292 (0.0389) | 27,654 |
| Hispanic share | rent | −0.3514 (0.0829), t = −4.2 | **+0.1625 (0.0518), t = +3.1** | 1,205 |
| Mexican-origin share | rent | −0.3428 (0.1114), t = −3.1 | +0.0810 (0.0746) | 1,205 |

The ACS-measured gradient is 0.18 to 0.51 log points more negative than the
independently-measured one, in both periods and both outcomes. Two mechanisms produce
exactly this, and both are properties of the measure rather than of the housing market.
*Correlated sampling error*: tract composition and tract median rent come from the same
drawn households, so a draw that over-represents a lower-rent group moves both series
together. *Reporting composition*: ACS median home value is the median of owner
self-assessments and median gross rent is the median over occupied units, so a change in who
occupies a neighbourhood moves the statistic even when no unit's market price has changed.
Zillow's ZHVI is constructed to hold the housing tier fixed and does not have either
property. Period A is the partial exception for values: ACS −0.225 against Zillow −0.077
(t = −1.1), same sign but a third the size and not significant.

**(b) The placebo fails.** Regressing period-A price growth on period-B composition change,
with period-A controls, on the tracts observed in both periods:

| Treatment | Outcome | placebo λ (se) | reading |
|---|---|---|---|
| Hispanic share | value | −0.0655 (0.0145), t = −4.5 | fails |
| Mexican-origin share | value | −0.0502 (0.0132), t = −3.8 | fails |
| Hispanic share | rent | −0.0216 (0.0094), t = −2.3 | fails |
| Foreign-born share | rent | −0.0188 (0.0139), t = −1.4 | passes |

Groups move into neighbourhoods whose relative prices were *already* falling. The
contemporaneous coefficient therefore mixes capitalisation with sorting on pre-existing
trends, which is the "reverse causality" channel Saiz and Wachter named as one of their three
candidate explanations and used the gravity instrument to address.

**(c) The forward arm flips sign.** Using period-A composition change to predict period-B
price growth puts treatment and outcome in non-overlapping ACS samples, so their sampling
errors are independent by construction. Hispanic share on value: **+0.0669 (0.0129),
t = +5.2**; Mexican-origin share on value: **+0.0683 (0.0162), t = +4.2**. Rents are small
and insignificant (−0.016 and −0.018). Once the mechanical link between the two series is
cut, the value gradient is positive, matching the Zillow arm in direction.

**(d) The effect is not stable across periods.** On one fixed tract set, the Hispanic-share
value coefficient is −0.098 (t = −4.9) in 2013–2018 and −0.009 (t = −0.7) in 2018–2023;
rents, −0.071 and −0.037.

## 4. Measurement error in the regressor

Using published ACS margins of error and the handbook derived-proportion formula, the
sampling variance of the five-year change in tract share is large relative to its
within-CBSA variance after controls:

| Treatment | Outcome | var(residualised Δshare) | var(sampling error) | reliability λ | raw coef | implied corrected |
|---|---|---|---|---|---|---|
| Hispanic | rent | 0.00399 | 0.00323 | 0.192 | −0.0487 | −0.254 |
| Hispanic | value | 0.00277 | 0.00218 | 0.211 | −0.0538 | −0.254 |
| Mexican | rent | 0.00276 | 0.00223 | 0.189 | −0.0568 | −0.300 |
| Mexican | value | 0.00188 | 0.00151 | 0.200 | −0.0849 | −0.425 |
| Foreign-born | value | 0.00188 | 0.00146 | 0.225 | +0.0014 | +0.006 |

About four-fifths of the usable variation is noise. **This correction cuts against the
headline, and it is stated because it does.** If the error were classical, the true
Hispanic-share value coefficient would be −0.254, almost exactly the paper's −0.246. But the
Zillow arm shows the error is *not* classical — it is correlated with the outcome — and
dividing a contaminated coefficient by its reliability magnifies the contamination along with
the signal. The right reading is that neither the small raw magnitude nor the large corrected
one is a credible estimate: the ACS route cannot answer this question at tract level in this
period, in either direction.

## 5. Heterogeneity

Saiz and Wachter's Table 2 interacts the composition change with initial share non-Hispanic
white and with the initial house-value quartile, finding the discount concentrated in
initially white, initially expensive tracts (−0.285 and −0.075 on the interactions).
Reproduced on Hispanic share:

| Interaction | Outcome | main (se) | interaction (se) | vs paper |
|---|---|---|---|---|
| × initial non-Hispanic white share | value | +0.009 (0.038) | −0.110 (0.055) | same sign, 2.6× smaller |
| × initial non-Hispanic white share | rent | −0.088 (0.016) | **+0.084 (0.027)** | opposite sign |
| × initial value quartile | value | +0.052 (0.023) | −0.076 (0.010) | same sign, same size |
| × initial value quartile | rent | +0.058 (0.027) | −0.095 (0.013) | same sign |
| × initial group share (tipping) | rent | +0.011 (0.012) | −0.213 (0.036) | paper found no non-linearity |

The value-quartile interaction is the one result that lines up with the paper in sign and
magnitude, but it is also the one most exposed to mechanical mean reversion, since the
interacting variable is the initial price itself. Supply-response split (a realized
quantity-response proxy, **not** Saiz's 2010 land-and-regulation elasticity, which was not
obtainable): the value gradient is −0.088 in low-response metros against −0.026 in
high-response metros, the expected direction if the gradient is a price response to a demand
shift.

## 6. Metro level, for contrast

Aggregating the same tracts to CBSA and regressing metro price growth on the foreign-born
inflow as a share of initial metro population, with period fixed effects, clustered on CBSA
(758 metro-periods):

| Outcome | per 1% population inflow, foreign-born | per 1% population inflow, Hispanic |
|---|---|---|
| Rent | +1.32% (0.42) | +0.68% (0.18) |
| Home value | +3.43% (0.69) | +2.68% (0.37) |

Positive, large, and stable across both periods. The rent figure sits close to the +1.4% per
1% employment inflow the repo carries from Wilson and Zhou 2026; values come in higher than
their +2.2%, but the treatments differ (population inflow here, employment inflow there) and
the comparison is indicative only. The point for this lane is structural: the metro-level
demand effect is unambiguous and positive, while the within-metro neighbourhood gradient is
small, sign-unstable, and measurement-driven. Netting the metro effect out through CBSA ×
period fixed effects, as the design does, is therefore essential and was done throughout.

## 7. Dollars

Stated as a range across arms, per the brief. Base quantities are weighted means over the
estimation universe at end of period: annual gross rent $15,716 per renter household, home
value $336,390 per owner-occupied unit, 5,921 residents, 1,068 renter households and 1,584
owner-occupied units per tract.

Aggregation, stated explicitly: a +10 point share change in a tract of 5,921 people means
592 additional group residents. The rent channel costs 1,068 renter households
$15,716 × (exp(0.10λ) − 1) each per year; dividing that tract total by 592 gives dollars per
additional group resident-year. The value channel is a one-time capitalised amount per
owner-occupied unit, annualised at 4% and 6% cap rates before the same division.

| Treatment | ACS-measured arms | Independent-measure arms |
|---|---|---|
| Hispanic share | **−$979 to −$86** per resident-year | **+$303 to +$464** |
| Mexican-origin share | −$955 to −$107 | +$231 to +$396 |
| Foreign-born share | −$492 to +$384 | +$249 to +$702 |

**The range spans zero and its sign is determined by which price series is used, so this lane
does not deliver a dollar figure for the compositional amenity.** The defensible statement is
a bound: whatever natives pay within a metro to live away from Hispanic or immigrant
neighbours, it is under roughly $1,000 per group resident-year in the most adverse
construction available, and the better-measured constructions put it at or above zero.

Three further cautions on any use of these numbers. They are **within-metro relative prices**:
a receiving neighbourhood's relative decline is another neighbourhood's relative gain, so
they are transfers across locations inside a metro, not resource costs, and they very nearly
net to zero across a metro by construction. They are **a price for a bundle** — schools,
crime, income mix, housing vintage — that moves with composition; nothing here isolates a
taste for ethnicity. And within a receiving tract they are a **transfer between tenures**:
lower relative rents benefit renters exactly as much as they cost landlords.

## 8. Against the repo's other numbers

[UNVERIFIED — taken from the lane brief, the paper was not fetched] Card, Dustmann and
Preston (2012, JEEA 10(1):78–119) report that compositional concerns explain 2–5× the
attitude variation that wage and tax concerns do. If the compositional channel really carried
2–5× the weight of the fiscal channel *in dollar terms*, this lane should have found a
housing price of several thousand dollars per resident-year against the repo's complete
common-age fiscal gap of −$7,224 per person-year versus third-plus non-Hispanic whites
(confidence ladder entry **130** as amended 2026-09-18 — the brief attributes this figure to
entry 123, which carries the aggregate account, not the per-person gap). It did not. The most
adverse housing construction reaches about 13% of that fiscal gap, and the better-measured
constructions have the wrong sign for a cost at all.

The reconciliation is that attitude weights and revealed-preference prices are different
quantities. Card–Dustmann–Preston measure how much *stated* concern loads on composition;
housing capitalisation measures what the marginal mover actually pays within a metro. A large
attitude weight with a small revealed price is coherent: most natives are inframarginal to
neighbourhood composition, a point Saiz and Wachter make themselves ("the majority of the
native population is inframarginal", p. 187). This lane does not license converting
compositional attitudes into a fiscal-comparable dollar amount.

## 9. What was skipped, and why

- **Saiz (2010) housing supply elasticities**: not obtained. The published table is not in a
  machine-readable source reachable from here, and the Census Building Permits metro files
  404 at the documented path. Substituted a realized quantity-response proxy built from the
  same ACS panel (CBSA housing-unit growth over population growth), labelled as a proxy in
  section 5. It is endogenous to demand and should not be read as a supply elasticity.
- **Goldsmith-Pinkham–Sorkin–Swift exposure diagnostics**: not run. The shift-share
  instrument failed at the first hurdle (first-stage F of 0.09–1.1 for Hispanic share, and
  the Mexican-origin version is degenerate), so Rotemberg weights would decompose an
  instrument with no usable first stage. Reported as a failure rather than diagnosed.
- **HUD Small Area Fair Market Rents**: not fetched. Listed as optional in the brief; the
  Zillow arm already supplies an independent rent measure and answered the question the
  SAFMR check was there to answer.
- **ZCTA-level margins of error**: the three national API calls did not complete within four
  attempts each at a 600-second timeout. The attenuation correction therefore runs at tract
  level only; the ZCTA and Zillow regressions are uncorrected, which understates their
  magnitudes but cannot change their signs.
- **Rent results from the paper's own online appendix**: not consulted. Saiz and Wachter
  report rent results "in a separate online Appendix" (p. 174) and describe them as "highly
  consistent" with the value results, but the appendix was not fetched, so this lane compares
  its rent estimates only to their published value coefficients.

## 10. Draft memo section

> **Housing does not price the compositional amenity in 2013–2023.**
> Saiz and Wachter (2011, AEJ:EP 3(2):169–188) found that within a metropolitan area, house
> values grew relatively more slowly in neighbourhoods whose foreign-born share was rising:
> −0.246 log points per unit of share in their baseline, about −2.5% for a ten-point
> increase, on 34,833 tract observations across 1980–1990 and 1990–2000. Reproducing their
> first-differences specification on ACS five-year data for 2013–2018 and 2018–2023 — same
> equation, same weighting by initial owner-occupied units, CBSA-by-period fixed effects,
> 110,000 tract-period observations in 381 metros — recovers a gradient of the same sign but
> three to six times smaller, and only for ethnic composition: a ten-point rise in Hispanic
> share is associated with 0.3–0.8% lower relative values and 0.3–0.6% lower relative rents,
> while foreign-born share shows nothing at all. That split is what the original authors
> themselves predicted, attributing their result "more to the fact that immigrants tend to be
> of low socioeconomic status and to belong to minority groups, than to foreignness per se."
>
> The surviving gradient does not withstand its own checks. It fails a placebo: price growth
> in 2013–2018 predicts composition change in 2018–2023 with the same negative sign
> (−0.066, t = −4.5 for Hispanic share on values), so part of the contemporaneous
> relationship is groups moving into neighbourhoods already declining in relative price.
> It reverses when treatment and outcome are measured in non-overlapping survey samples
> (+0.067, t = +5.2). And it reverses when the price comes from outside the survey
> altogether: on identical ZIP-level rows with identical controls, a ten-point rise in
> Hispanic share is worth −0.96% in ACS median value and +0.84% in Zillow's home value index.
> The most likely reason is mechanical. ACS median home value is the median of owner
> self-assessments and median gross rent is a median over occupied units, so both move when a
> neighbourhood's occupants change even if no unit's market price does; and because
> composition and price are drawn from the same sampled households, their sampling errors are
> correlated. The published margins of error imply that four-fifths of the within-metro
> variance in measured five-year share changes is sampling noise.
>
> The metro-level effect, by contrast, is robust and runs the other way: a foreign-born
> inflow equal to 1% of a metro's population raises its rents 1.3% and its values 3.4%.
> Immigration raises housing costs where it lands; what it does to relative prices *within*
> a metro is below this data's resolution. Translating the neighbourhood estimates into
> dollars gives −$979 to +$464 per additional group resident-year depending on which price
> series is used — a range whose sign is set by a measurement choice. The compositional
> amenity channel therefore stays in this repo as narrative, not as a priced line. Against
> the complete common-age fiscal gap of −$7,224 per person-year (ladder 130), the most
> adverse housing construction reaches about an eighth, and the better-measured ones have the
> wrong sign for a cost at all.

## 11. Verification

- `src/test_estim.py` — the weighted within-group WLS reproduces `statsmodels` WLS with a
  full fixed-effect dummy set to machine precision on both coefficients and cluster-robust
  standard errors; hand-written 2SLS matches the closed-form just-identified IV exactly,
  recovers a known coefficient of 2.0 from simulated endogeneity where OLS returns 2.56,
  and its Hansen J passes a valid instrument set (p = 0.80) while rejecting a deliberately
  invalid one (p < 0.0001). Prints `ALL ESTIMATOR CONTROLS PASSED`.
- `src/verify_repro.sh` — deletes `derived/` and rebuilds every output from the cached raw
  inputs, then compares the SHA-256 of the whole tree. Result recorded below.

**Reproducibility gate, run 2026-09-19:**

```
[repro] before: 19 files, tree sha256 2502d7add7a38ae9254c509b9ca0012bfdf62742e53affd7be437e02d4611b44
[repro] after:  19 files, tree sha256 2502d7add7a38ae9254c509b9ca0012bfdf62742e53affd7be437e02d4611b44
[repro] PASS: derived/ is byte-identical after a from-scratch rebuild
```

`derived/` was deleted and every computation step re-run from the cached raw inputs; all 19
files returned identical to the byte. The network steps are idempotent by construction: each
fetch script skips any cache file that parses, so a second run makes zero API calls.
