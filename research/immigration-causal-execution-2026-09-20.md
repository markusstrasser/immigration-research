# Executed causal checks: Mexican inflows and school budgets

**Finding, September20,2026:** Two public-data routes produced useful results.
The Mexican-inflow crime model gives mixed offense effects and exposes a count/rate
labeling issue. The Mariel reconstruction consistently estimates higher school
spending, with weaker inference and substantial donor sensitivity. Neither identifies
a national annual cost for Mexican-origin residents and their descendants.
[EXECUTED ESTIMATES/INFERENCE; reproducible lane](../infra/immigration-fiscal/causal_execution_2026_09_20/README.md)

## Four steps completed

| Step | Executed work | Remaining identification boundary |
|---|---|---|
| Define intervention and comparison | Historical Mexican-born share variation across MSAs;1980 Mariel shock versus synthetic Miami-Dade schools | Neither is removal of the present ethnic-origin population |
| Obtain external variation | Original Mexican birth-cohort/network IV package; public historical school-finance panel around Mariel | Prepared IV lacks upstream cohort build; arrival timing does not rule out concurrent local shocks |
| Measure matched outcomes | Seven recorded offenses;21 school expenditure/revenue/tax/transfer models across three donor specifications | Crime geography unresolved; school finance does not contain native-child attainment |
| Try to break the result |644 MSA exclusions, weaker-control and reconstructed-rate specifications, AR sets; fiscal holdouts, placebo ranks and donor deletion | Asymptotic inference/transport assumptions remain; no national extrapolation |

The separate [school-capacity review](immigration-school-capacity-harms-2026-09-20.md)
adds conditional learning-loss calculations and withdraws the old categorical
zero for incumbent quality harms. Evidence and calculations are preserved; essay
narrative remains operator-owned.

## Mexican-inflow crime: actual archived-model execution

The already-downloaded [Chalfin2015 package](https://doi.org/10.3886/E113382V1)
contains276 observations,92 MSAs and1980/1990/2000 levels. Python translation uses
the supplied instrument, population weights, demographic controls and region×period
effects. A separate full-matrix implementation checks every baseline coefficient,
cluster covariance and AR boundary. This is not native Stata execution; exact
published-table matching and Stata's omission conventions remain unverified.

Each coefficient is per one unit of `dmexfb_alt`, numerically **one percentage point
of change in `mexfba`**. The precise age universe needs upstream documentation.
These outcomes are **changes in log recorded counts**:

| Offense | IV coefficient | Cluster SE | Marginal95% cluster-AR set |
|---|---:|---:|---|
| Murder |−.0197|.0970|[−.2987,+.1509]|
| Rape |−.1328|.0618|[−.3706,−.0371]|
| Robbery |+.0520|.0968|[−.2130,+.2322]|
| Aggravated assault |+.1964|.0763|[+.0499,+.3986]|
| Burglary |−.0922|.0577|[−.2758,+.00002]|
| Larceny |−.1036|.0478|[−.2417,−.0195]|
| Motor theft |−.1470|.0820|[−.3888,−.0055]|

[EXECUTED: `derived/chalfin/chalfin_replay.json`; individual, not seven-outcome
simultaneous intervals.] Cluster CR0 matches `ivreg2` without `small`;
[the estimator's author documents that convention](https://www.stata.com/statalist/archive/2012-01/msg01113.html).
AR tests address weak relevance, conditional on validity, and still use an
asymptotic cluster reference. They do not repair shared-origin-shock dependence.

The main first-stage conventional clustered F is13.28; removing Chicago reduces
it to9.17. About9–11 effective clusters by residual-instrument-energy concentration
carry the adjusted variation. Assault, rape and property-effect signs survive
single-MSA deletion, but individual significance does not: assault without Chicago
has z1.88. Region×period controls alone give assault+.0668, versus+.1964 with the
full demographic changes. Some demographic controls may be mediators; dropping
them can instead expose confounding. Neither specification automatically identifies
the total effect. [EXECUTED/INFERENCE]

All **1,282** available supplied `dlogpc_*` observations match changes in log raw
counts within stored precision; they do not match changes in their `logpc_*`
rate levels. Reconstructing those rate differences yields assault+.1677(SE.0786),
larceny−.1323(.0471), murder−.0475(.0958). This is a separate estimand, not evidence
that the count estimate itself is meaningless. Census population/crime-population
ratios span0.52–2.35, so stable incident geography cannot be assumed. [EXECUTED]

**Dollar bridge remains unresolved:** identify compatible crime reporting geography,
exposure age/count units and a beneficiary population, then estimate one victim-harm
index on a common sample or preserve its joint covariance. A changing population
share is not a count of new admissions. No immigration-only violation receives an
automatic harm price; real resources and distinct victim losses are counted once.
[INFERENCE; operator's accounting rule]

## Mariel school spending: independent reconstruction

Acquired and validated the **85,277,958-byte** publisher GFD supplement; streamed
268,798 historical school-year rows covering17,259 units,1967–92. The old held
all-government ZIP was truncated and was not used. Source values are nominal
thousands; current operating spending is distinct from total-minus-capital.
[SOURCE: [Pierson–Hand–Thompson2015](https://doi.org/10.1371/journal.pone.0130119),
[source lock and reproduction](../infra/immigration-fiscal/causal_execution_2026_09_20/mariel/README.md)]

Fit ordinary nonnegative, sum-to-one synthetic controls on1970–79; omit1980 from
fit/effect averages; measure1981–90 mean log gaps. This differs from the author's
`allsynth` bias correction. The source's survey/fiscal-year ambiguity is addressed
in the primary sensitivity by keeping districts whose observed fiscal endings
are allJune30; missing dates still require calendar stability. Full-pool runs are
explicit timing diagnostics. [METHOD; [Census year convention](https://www.census.gov/programs-surveys/gov-finances/information.html)]

| Donor specification | Current operating log gap | Geometric difference | Two-sided placebo rank | Total-spending log gap |
|---|---:|---:|---:|---:|
|28 donors, observedJune30 calendars|.1606|+17.4%|.138|.1696|
|43 published donor identities, timing diagnostic|.1942|+21.4%|.091|.2489|
|44 donors, timing diagnostic|.1942|+21.4%|.133|.2489|

[EXECUTED] This is a **specification spread, not a confidence interval**. Pretreatment
1977–79 holdout gaps are−.0004 for June30 operating spending and−.0425 for the full
pool. Los Angeles supplies43–46% of operating weights; deleting it raises operating
log gaps to.326–.381. Point estimates remain positive while magnitude and placebo
inference depend materially on the comparison set. Placebo ranks are conditional
diagnostics, not exact probabilities from randomized city assignment.

The author's August2024 TableA3 already gives operating expenditure+.20 with
**one-sided p=.09**; total+.25/p=.045 also uses a one-sided test. The earlier memo
omitted that qualification. Neither our reconstruction nor those tables establishes
an exact variable-cost percentage for all public services.
[SOURCE: [author manuscript](https://wagner.nyu.edu/files/faculty/publications/Mariel%20Boatlift_5.pdf), §§3–4/TableA3]

Revenue/own-tax/state-transfer endpoints were also run. Their separately fitted
counterfactuals do not form an additive balanced ledger. Federal-transfer estimates
are unstable to donor deletion. Intergovernmental grants cannot be charged at both
levels. No class-size, native-attainment, national tax or Mexican-descendant effect
is inferred from these local Cuban-refugee budget results. [EXECUTED/INFERENCE]

## Fruitfulness and checks

The fruitful work was raw reproduction, unit reconstruction and capacity-versus-peer
separation. Further abstract-level literature expansion has lower immediate value.
The H-2B lottery remains evidence of employer gains, but no new assignment microdata
were acquired here; restricted Mexican local-fiscal data also remain unavailable.
Published revenue effects cannot be promoted to national consumer surplus.
[Coverage; [earlier policy audit](immigration-policy-causal-evidence-2026-09-20.md)]

Independent review caught two implementation defects: the baseline checker accepted
incorrect saved interval labels/summary statistics, and fiscal placebo fits included
treated Dade as a donor. Both were fixed; corrupted-result probes fail under
`python -O`, and all21 fiscal models were rerun with Dade excluded from placebo
donors. Source hashes/CRC, direct path/rank checks and source-specific definitions
are retained. Favorable/adverse/null findings remain together; model selection of
research questions can still bias emphasis. No national fiscal or crime total is
revised by these exercises.
