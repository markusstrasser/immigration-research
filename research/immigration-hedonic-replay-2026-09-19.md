# Housing comparison: original specification and modern sensitivity checks

**Verdict:** **The historical result reproduces on the authors' data.** A Python translation of the archived commands recovers all six Table 1 coefficients and standard errors at published precision, plus the column 5/6 first-stage and overidentification diagnostics. The modern ACS exercise remains a materially different specification and cannot establish that the historical relationship disappeared. On identical historical rows, mean and median house values both give negative estimates. [SOURCE: [original archive](https://doi.org/10.3886/E114757V1), author code and computed comparisons below]

## Source contract

| Component | Original source | Existing modern lane |
|---|---|---|
| Outcome and window | Log **average** value change,1980–1990/1990–2000 | ACS median values, five-year windows ending2013/2018/2023 |
| Baseline controls | Paper describes44; archived command actually has43, omitting HS-dropout share |12; different attributes and timing |
| Sample rule | Archived code requires foreign-born stock increase **>5%** of initial metro population per decade | Cutoff chosen to capture76.5% of positive growth; the paper's76.5% is an outcome of its threshold, not its rule |
| Inference | Tract clusters | CBSA clusters |
| Gravity | β=1.6; Euclidean longitude–latitude degree distances; other tracts in metro | β=1 main; haversine miles and quarter-mile floor; neighbors filtered by outcome/control validity |
| IV columns | Column5 excludes Pull and two interactions, controlling initial FB share; column6 includes Pull and excludes the interactions | Column5 form omitted from the original modern run |

All original value regressions use initial owner-unit weights and metro×period fixed effects. The [published targets](../infra/immigration-fiscal/hedonic_replay_2026_09_19/table1_targets.json) are preserved separately from the computed results. Gravity is supplied precomputed in the archive; its upstream construction is not replayed here. [SOURCE: main paper pp172–179,Table1,A1; [online appendix](https://www.aeaweb.org/articles/materials/1124) §3 and Table3; archived `.do` and `.dta`]

## Completed original-data reproduction

Archive V1 was acquired September 19:102,766 tract-period rows,248 fields. Source bytes, licensing, variable definitions and hashes are in the [acquisition record](../infra/immigration-fiscal/hedonic_replay_2026_09_19/ACQUIRED.md). These are translations of the authors' prepared-data commands, independently checked with explicit fixed-effect regressions; no native Stata executable or upstream Geolytics construction was run. [SOURCE; CALCULATION]

| Table 1 column | Published β (SE) | Recomputed β (SE) | Recomputed N |
|---|---:|---:|---:|
|1, basic WLS|−0.418 (0.016)|−0.417939 (0.015764)|34,835|
|2, baseline controls|−0.246 (0.015)|−0.246241 (0.014720)|34,833|
|3, land use and lagged trends|−0.244 (0.015)|−0.244211 (0.015481)|30,947|
|4, Pull IV|−0.323 (0.136)|−0.322738 (0.136414)|34,833|
|5, three excluded instruments|−0.211 (0.050)|−0.210950 (0.050218)|34,833|
|6, two excluded interactions|−0.214 (0.054)|−0.214420 (0.053538)|34,833|

Columns 1–3 also reproduce R²0.79/0.85/0.86. Columns 5/6 first-stage F are **362.2333/337.6318**, matching362.23/337.632. Their Hansen J p-values are **0.949689/0.796062**, matching0.95/0.80. The J calculation uses efficient two-step GMM with full fixed-effect instrument moments and agrees between an explicit matrix calculation and `linearmodels.IVGMM`; the ordinary point estimates remain2SLS. Passing J does not prove exclusion restrictions. [CALCULATION: `original_results.csv`, `original_verification.json`; [ivreg2 authors,§4.3](https://www.stata.com/meeting/2nasug/wp545.pdf)]

**Outcome-only historical check:** on the identical21,681 observations for1990–2000, the mean-value coefficient is **−0.309733 (SE0.018609)** and median-value coefficient is **−0.278154 (SE0.057098)**. The latter recovers appendix Table2 col4. Thus a negative historical gradient survives replacing means with medians while holding rows, controls and weights fixed. This does not rule out every shared survey-measurement concern or establish modern transportability. [CALCULATION; INFERENCE]

Bounded reporting discrepancies:

- Column1's code uses34,835 observations, two more than the printed table; both extra rows lack initial log income, which is only required from column2 onward. Other main-table Ns match.
- The archived baseline has43 controls. Adding the HS-dropout variable described in the paper gives−0.239796(SE0.014654), preserving the conclusion. Column3 also includes water and commercial/industrial/mining land shares; dropping those simultaneously changes rows, so that sensitivity is not a pure control effect.
- Column4's tract-cluster first-stage F is **30.7062**, not the printed76.01. Independent clustered, HC1 and classical calculations do not resolve that entry. Columns5/6 diagnostics match, so this is not a general failure of the IV reproduction.
- Literal appendix first stages use35,120 rows, because their commands do not restrict the sample to observed house-value changes; the appendix prints34,833. Their coefficients reproduce, while SEs differ slightly with finite-sample conventions. The historical Stata/ado versions were not supplied.

These source discrepancies are retained; they do not overturn the matching coefficients. [SOURCE: main `.do` lines17–48; supplemental `.do` lines100–107; CALCULATION: `original_first_stages.csv`]

## Completed modern comparisons

All coefficients below are changes in log owner value per unit change in foreign-born share. Multiplyβ by0.1 for log-value change per ten-percentage-point share increase; these are conditional statistical estimates, not welfare dollars. Owner-unit weighting and modern12-control matrix are held fixed within each comparison. [CALCULATION: `src/modern_bridge.py`, `derived/modern_bridge.csv` in the replay lane]

| Comparison | Coefficient | Cluster SE | N / metro clusters |
|---|---:|---:|---:|
| Existing pooled coverage sample |+0.04589|0.01987|45,369 /133|
| Identical rows, tract clustering |+0.04589|0.01435|45,369 /30,825 **tract** clusters|
| Native-boundary periodA,2013→2018 |−0.02430|0.02712|21,765 /85|
| Ten-year2013→2023, all valid metros |−0.04393|0.02514|56,071 /377|
| Same ten-year construction, coverage cutoff |+0.02136|0.03412|25,300 /88|
| Same ten-year construction, fixed5% cutoff |+0.13612|0.07641|5,441 /13|

Clustering changes uncertainty, exactly as expected; the coefficient is invariant. The ten-year cutoff changes sample and point estimate, but does not restore the historical negative slope. With only13 clusters, the last row is a descriptive sensitivity check, not a precise causal estimate. PeriodA versus pooled differences change the era as well as crosswalk exposure; they do not isolate the crosswalk. [INFERENCE]

The gravity comparisons freeze the same21,765 periodA outcome rows. Neighbor expansion is57,348 price-valid tracts→60,414 cached tracts with usable geography and initial FB share. Each successive row below changes one instrument-construction choice; controls, treatment, outcomes, weights and clustering remain fixed. Column6-style IV includes Pull directly; only its interactions are excluded.

| Gravity construction, column6 form | β̂ | SE | Excluded-instrument F |
|---|---:|---:|---:|
| Existing neighbors, exponent1, haversine |+5.537|3.694|3.03|
| All available neighbors, exponent1 |+3.238|2.016|5.93|
| All neighbors, exponent1.6 |+2.835|1.784|7.16|
| Same, remove quarter-mile floor |+2.736|1.697|7.66|
| Same, degree-plane distance |+2.586|1.507|9.82|

These imprecise, weak-first-stage results do not yield a defensible causal valuation. The separately added **column5 form** hasβ=+0.511(SE0.373),F62.14 under the final gravity convention. Therefore “gravity has no first stage” is not a specification-general conclusion. Column5 excludes Pull itself and makes a stronger exclusion assumption than column6; a higher F does not establish that assumption. This check supplies no verified overidentification verdict. [CALCULATION; INFERENCE]

## What survives and what remains open

- **Survives:** the modern lane does not supply an identified composition-amenity dollar price. Its matched-row ACS-versus-Zillow results remain evidence of outcome sensitivity.
- **Withdraw:** “exact reproduction,” an established era change, and the explanation that declining aggregate Mexican-born counts prove local diffusion stopped. Aggregate decline alone does not rule out local redistribution. The original authors' contemporaneous mean/median and transaction-data checks also preclude dismissing their result solely with the modern ACS measurement concern. [SOURCE: main paper p172 footnote3; appendix Table2; INFERENCE]
- **Original-data gate completed:** historical coefficients, uncertainty and the stronger IV diagnostics reproduce; the matched mean/median check rejects a means-only explanation. A fully harmonized cross-era comparison remains unavailable: the modern12-control set and ACS windows are not equivalent to the archived43-control specification. Neither the original upstream harmonization nor gravity-construction code is in the package.
- **Older modern J statistics are unverified:** its estimator evaluated a clustered moment quadratic at the2SLS estimate rather than the corresponding efficient-GMM estimate. That is not the documented ivreg2 Hansen J. The generator now returns missing J with an explicit unavailability status, covered by regression checks. Historical outputs remain preserved for audit, but their overidentification rejection labels should not be reused. This replay verifies historical J separately; it does not certify or regenerate the older modern J series. [SOURCE: [ivreg2 authors,§4.3](https://www.stata.com/meeting/2nasug/wp545.pdf); old `estim.py`; INFERENCE]
- **Identification limit:** preferences, schools, crime, housing quality and sorting can be bundled in relative prices. Neither an unstable slope nor its absence proves zero amenity value, and relative price redistribution does not by itself settle welfare. [FRAMING-SENSITIVE]

Verification: all six original columns and matched mean/median checked against independent statsmodels WLS/linearmodels2SLS with explicit fixed-effect dummies; original first-stage F independently checked; original Hansen J checked against full-instrument two-step GMM. The earlier modern bridge retains its separate coefficient/SE/first-stage checks. Inputs and row/matrix hashes remain in ignored derived outputs. [Reproduction instructions](../infra/immigration-fiscal/hedonic_replay_2026_09_19/README.md)

Instrument: LLM-assisted source audit, subject to the project's [bias caveat](../notes/llm-bias-caveat.md); deterministic checks verify calculation, not causal interpretation. No inference about individual preferences follows from these aggregate regressions.

## Revisions

- **2026-09-19, before acquisition:** [Specification-equivalence decision](../decisions/2026-09-19-require-housing-specification-equivalence.md) withdrew the earlier exact-reproduction rating while preserving its estimates. Archive acquisition was then pending terms acceptance, not evidence of a failed replication.
- **2026-09-19, after authorized acquisition:** The same decision's follow-through now recovers the historical result and matched-row mean/median robustness. Code resolves43 versus44 controls; reporting discrepancies remain explicit. The earlier modern J implementation is excluded from verified evidence. This strengthens the correction to the failed-replication claim without establishing contemporary causal effects or welfare prices.
