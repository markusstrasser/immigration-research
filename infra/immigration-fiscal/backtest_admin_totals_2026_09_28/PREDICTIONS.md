# Pre-registered predictions: do the account's keys put dollars in the right states?

Written 2026-09-28 in phase 1 of [`BRIEF.md`](BRIEF.md) (commit 78ca741), before any external figure for these
checks was opened. The parent's commit of this file with `derived/` and the scripts is the pre-registration.
Phase 2 fetches the administrative files, scores every check with the code frozen here (`estimators.py`), and
edits nothing in this file.

## The prediction: the adopted key, state by state

The account splits each national line by a key: the group's share of a CPS ASEC 2025 amount. A national total
cannot test a key, because every key splits 100% of its line. State totals can. The group is half of California's
credit dollars and a twentieth of Florida's [DATA: derived/predictions.csv], so a key that misstates the group's
use misplaces dollars across states in proportion to the group's share of each state's amount.

The prediction is the adopted key before its fill-in step: stack arm
`row4+status_state_aware|central|audit_rules_alone`, rebuilt with the CPS lane's own functions
(`cps_imputation_keys_2026_09_23/combine_onbooks_lane.py`) [CALCULATION: predict.py]:

- audit row 4's weights, which scale the Mexico-born naturalized and noncitizens outside CA+TX to the ACS 2024
  (factors 0.856 and 0.778) [DATA: derived/prediction_audit.json];
- the state-aware status flag. The flagged lose their EITC and keep 0.526 (Mexico-born) or 0.550 (other
  Latin-American-born) of their ACTC, the on-books lane's central shares.

Gates, all passed: the rebuilt shares reproduce the adopted package's stored cells for the credit, SSI, Social
Security and railroad lines with a gap of 0.0 bn (1e-9 required); the builder's published keys reproduce to
9.7e-17 and the paper rule's change to 1.4e-15 [DATA: derived/prediction_audit.json].

State totals cannot see the steps after this arm: the fill-in step (the union-matched hot deck) and the
package's national shifts on these lines. Those are CBO's income-group shift (SSI −0.08, Social Security −2.07 /
−2.00, railroad −0.02 $bn, shared / personal) [DATA: external_benchmarks_2026_09_24/derived/cbo_deltas.json],
Treasury's EITC split (−0.36 / −0.34) [DATA: external_benchmarks_2026_09_24/derived/ota_deltas.json] and the
premium-tax-credit re-key (−14.23, PTC part only) [DATA: dataset_integrity_2026_09_23/derived/
spending_mts_credits.json]. Phase 2 lists them beside any miss, because a national shift may already correct
what a state miss finds.

The secondary reading, "published", is the builder's keys on the published weights with the audit's paper flag
at a flat 0.60. It shows what the stack changed. Where the two readings differ, the one closer to the
administrative totals tells whether audit row 4 and the state-aware flag moved the key the right way.

## How every check is scored

Frozen in `estimators.py`; phase 2 imports it unchanged.

- **Misstatement δ (checks 1–2).** Suppose the group's true dollars on a key are (1 + δ) times the key's and
  everyone else's are right. Then a state's true share of the national total is
  A_s = P_s (1 + δ g_s) / (1 + δ ḡ). Here P_s is the key's predicted share, g_s the group's share of the
  state's predicted amount and ḡ the national share. `delta_fit` is weighted least squares of
  A_s / P_s − 1 on (g_s − ḡ) through the origin, weights P_s. Each end of the case gets its own δ with its own
  g_s: the shared allocation sets the low end (specification 48), the personal the high end (specification 11).
- **Standard error.** `delta_se` takes the larger of two estimates. The replicate term refits δ on each of the
  160 successive-difference replicates of P and g, holding A. It measures the frame's sampling error. The HC3
  term reads the residuals, which carry sampling error and the state model's misfit, and it corrects for the
  leverage of the largest states. Adding the two would count the sampling error twice.
- **Tolerance.** A key error is material when it moves the September 27 case by more than $2bn. For small δ the
  group's dollars move by G (1 − s) δ, so τ = 2 / (G (1 − s)). G = L × hf × s is the key's group dollars: L is
  the keyed national total and hf = 0.99005 the household fraction by which the engine scales spending lines
  [CALCULATION: predict.py, as in translate.household_fraction]. Every τ is in `derived/power.csv`.
- **Call** (`call`). Miss: |δ| > τ and |δ| > 1.96 SE. No power: not a miss, and 1.96 SE > 2τ. Otherwise hit.
  A check misses when either end misses. It hits when both ends hit, and otherwise has no power. A hit means no
  material error was found and the 95% interval is no wider than ±2τ. It does not certify the key to within τ.
- **Relative and absolute checks (check 3).** The same call, with error A / P − 1 (or A − P for a level) and the
  prediction's replicate SE. NVSS counts every birth, so the target carries no sampling error.
- **Distributions** (`distribution_call`). Dissimilarity D = ½ Σ |A_c − P_c| over the declared cells. Miss:
  D > τ and the Wald statistic, with the frame's replicate covariance, above the 95th percentile of χ² with
  (cells − 1) degrees of freedom. No power: not a miss, and the dissimilarity expected from sampling noise alone
  exceeds τ. Otherwise hit.
- **Baselines.** Each is scored like the prediction. The prediction beats a baseline when its error is smaller:
  dissimilarity for state distributions, absolute error for national figures.
- **Dollars regardless of the label.** Every δ is reported in dollars at its point estimate and at its 95%
  bounds, at both ends.

**Estimator check** [DATA: derived/estimator_check.csv; CALCULATION: estimator_check.py]. The check builds 160
synthetic truths from the frame's own replicates and scores them like the real data, with no state misfit.

| Key | Mean estimate at δ = 0 / +0.3 / −0.3 | 95% coverage | Calls at δ = 0 (miss / hit / no power) | Miss rate at δ = +0.3 / −0.3 |
|---|---|---|---|---|
| Credits (shared) | −0.001 / +0.299 / −0.300 | 0.97–0.98 | 0.03 / 0.64 / 0.33 | 0.59 / 0.88 |
| SSI (shared) | +0.008 / +0.307 / −0.292 | 0.96 | 0.04 / 0.84 / 0.12 | 0.07 / 0.16 |
| Social Security (shared) | +0.001 / +0.301 / −0.299 | 0.96 | 0.04 / 0.00 / 0.96 | 0.43 / 0.53 |

The estimator is unbiased at this noise, and its interval covers at the nominal rate. For SSI a δ of ±0.3 is
immaterial ($1.4bn) [CALCULATION: $5.26bn × (1 − 0.0816) × 0.3], so a hit there is the right call.

## Check 1: refundable credits by state (IRS SOI)

**Target.** SOI Historic Table 2, tax year 2023, all-states file `23in55cmcsv.csv`, rows with AGI_STUB = 0
(state totals) for the 50 states and DC. TY2023 is the latest year SOI publishes by state. The primary target
is A59660 + A11070: the earned income credit, refundable and non-refundable parts [SOURCE: SOI 2023 state data
guide, footnote 12], plus the additional child tax credit. This matches the microdata, whose EIT_CRED is the whole
credit. The secondary target is A59720 (the refundable EIC) + A11070. The components are A59660 against the
EITC series and A11070 against the ACTC series. The amounts are in $ thousands; each state is scored as its share
of the 51-area total.

**Prediction** (adopted reading). The group's share of the key is 20.29% (shared) and 18.43% (personal); without
the rule it would be 23.84% and 21.83%. In the published reading it is 21.66% and 20.06%.
[DATA: derived/prediction_scalars.csv]

| State | Share of credits, % (SE) | Baseline 1: no SSN rule | Baseline 2: population | Group's share of the state's credits, shared / personal | Group's share of residents |
|---|---|---|---|---|---|
| CA | 10.12 (0.52) | 11.07 | 11.73 | 52.0 / 49.6 | 33.2 |
| TX | 10.54 (0.62) | 11.32 | 9.23 | 44.0 / 41.7 | 31.5 |
| AZ | 2.41 (0.35) | 2.43 | 2.21 | 66.7 / 62.3 | 31.2 |
| NM | 0.76 (0.09) | 0.75 | 0.62 | 44.6 / 40.1 | 32.6 |
| NV | 0.97 (0.15) | 1.06 | 0.97 | 39.9 / 33.8 | 21.9 |
| CO | 1.06 (0.15) | 1.03 | 1.73 | 40.9 / 40.7 | 19.1 |
| IL | 3.40 (0.34) | 3.38 | 3.73 | 29.8 / 28.0 | 14.4 |

[DATA: derived/predictions.csv, frame asec2025_adopted]. The published reading puts California at 11.30%; the
state-aware flag removes more of California's credits.

The prediction is 0.025 in dissimilarity from baseline 1 and 0.074 from baseline 2.
[CALCULATION: derived/predictions.csv]

**Tolerance and power.** The key's group dollars are $22.19bn (shared) and $20.16bn (personal), so τ = 0.113
and 0.122. The sampling SE of δ is 0.103 and 0.106 [DATA: derived/power.csv]. That is powered by sampling
alone, but only just. Any misfit of the state model raises the SE through HC3, so "no power" is a likely
outcome unless δ is large.

If the prediction were exact, the no-rule microdata would score δ = −0.185 and −0.194. That is about 1.8
standard errors, so the test can only just tell the adopted rule from no rule.

**Named definitional gaps.**

1. Year. TY2023 claims, filed in calendar 2024, against ASEC 2025 incomes of 2024 and its 2024 credit rules.
   The ASEC 2024 secondary matches the year but carries only the published reading.
2. Take-up and error. CPS credits are simulated for every eligible unit; SOI counts claims. State differences in
   take-up and in erroneous claims enter δ. They belong in the key, because the account's line is actual outlays.
3. Address. SOI's state is the return's address, which "may differ from the taxpayer's actual residence"
   [SOURCE: SOI 2023 state data guide, §C].
4. Coverage. The key's national total, $110.46bn of line 25 without PTC, also holds about $24bn of other
   refundable credits beside the refundable EITC ($60.135bn) and ACTC ($26.287bn)
   [DATA: dataset_integrity_2026_09_23/derived/spending_mts_credits.json]. The test covers EITC and ACTC.

**What a miss means.** If δ > 0, the group claims more credit dollars than the key gives it, so
refundable_tax_credits/refundable_credits rises at the group. If δ < 0, the adopted SSN rule and on-books shares
still leave the group too much. The component fits show whether EITC or ACTC carries the miss. The published
reading and baseline 1 show whether the stack's rule moved the key the right way.

**Blindness: partly not blind.** No TY2023 state figure has been seen. From general knowledge I know the rough
ranking of states by EITC dollars: California, Texas and Florida lead, each with roughly a tenth of the national
amount [TRAINING-DATA]. SOI county files for TY2011–2022, which sum to state totals, are in the repo
(`causal_evidence_2026_09_20/raw/county_outcomes/raw/irs_soi/county/`), unopened. California FTB CalEITC reports
in `california_program_costs_2026_09_23/_cache/` are also unopened.

## Check 2: SSI and Social Security by state (SSA)

**Targets.**

- SSI: SSA's SSI Annual Statistical Report 2024, federally administered payments by state (federal SSI plus
  federally administered state supplementation), for the 50 states and DC. Calendar 2024 totals are used if SSA
  publishes them by state, otherwise December 2024. The secondary target is federal SSI alone, the part the
  budget line pays, if SSA splits it by state.
- OASDI: SSA's *OASDI Beneficiaries by State and County, 2024*: the total monthly benefits in current-payment
  status in December 2024, by state, for the 50 states and DC.

**Predictions** (adopted reading). The group's share of the key is 8.16% / 8.14% for SSI and 4.29% / 4.08% for
Social Security (shared / personal) [DATA: derived/prediction_scalars.csv].

| State | SSI share, % (SE) | Population | Age 65+ | Group's share of the state's SSI, shared / personal | Social Security share, % (SE) | Population | Age 65+ | Group's share of the state's Social Security, shared / personal |
|---|---|---|---|---|---|---|---|---|
| CA | 12.38 (1.20) | 11.73 | 10.68 | 27.4 / 27.1 | 9.48 (0.26) | 11.73 | 10.68 | 15.5 / 15.3 |
| TX | 6.92 (0.85) | 9.23 | 7.36 | 32.9 / 31.9 | 6.86 (0.21) | 9.23 | 7.36 | 18.6 / 17.8 |
| AZ | 1.34 (0.31) | 2.21 | 2.38 | 15.2 / 10.4 | 2.54 (0.17) | 2.21 | 2.38 | 13.2 / 11.7 |
| NM | 0.87 (0.17) | 0.62 | 0.70 | 28.8 / 32.1 | 0.66 (0.04) | 0.62 | 0.70 | 17.8 / 17.1 |
| NV | 0.89 (0.21) | 0.97 | 0.92 | 12.7 / 12.2 | 0.83 (0.07) | 0.97 | 0.92 | 7.6 / 6.0 |
| CO | 1.45 (0.48) | 1.73 | 1.67 | 28.7 / 29.3 | 1.78 (0.14) | 1.73 | 1.67 | 7.2 / 7.2 |
| IL | 3.20 (0.71) | 3.73 | 3.68 | 5.3 / 7.0 | 3.47 (0.18) | 3.73 | 3.68 | 4.5 / 3.9 |

[DATA: derived/predictions.csv, frame asec2025_adopted]

The SSI prediction is 0.111 in dissimilarity from both baselines. The Social Security prediction is 0.062 from
population and 0.028 from age 65+.

**Tolerance and power.**

- SSI: the key's group dollars are $5.26bn / $5.25bn, so τ = 0.414 / 0.415. The sampling SE is 0.331 / 0.335,
  powered by sampling [DATA: derived/power.csv]. At this resolution only an error well beyond $2bn can register
  as a miss: 1.96 × 0.363, the mean scored SE, is 0.71, or $3.4bn [CALCULATION: derived/estimator_check.csv].
- Social Security and railroad retirement: the key's group dollars are $62.12bn / $59.06bn, so τ = 0.034 / 0.035.
  The sampling SE is 0.136 / 0.140 [DATA: derived/power.csv]. This part is declared **no power**: the rule cannot
  return a hit, and a miss needs |δ| above about 0.27 (1.96 × 0.136).

**Named definitional gaps.**

1. The CPS under-reports SSI, and respondents confuse SSI with Social Security.
2. State-administered supplements are outside SSA's figures but may sit inside CPS reports.
3. SSI may be compared in December rather than over the calendar year. OASDI compares December benefits with
   annual 2024 CPS income.
4. OASDI beneficiaries abroad fall outside the state tables.
5. Benefits paid for children may be recorded on a parent's record. This moves g_s under the personal allocation
   only.

**What a miss means.**

- SSI: δ > 0 raises ssi/ssi at the group, and δ < 0 lowers it. If the federal-only secondary misses while the
  primary hits, the explanation is state supplementation. The candidate then becomes a supplement strip rather
  than δ: each state's CPS SSI is scaled by SSA's federal share of its payments.
- Social Security: δ moves social_security/social_security and railroad_retirement/social_security together.

**Blindness: partly not blind.** From general knowledge, California has the largest SSI caseload, and California,
Florida and Texas lead in Social Security beneficiaries [TRAINING-DATA]. No 2024 state figure has been seen, and
no SSA state file is in the repo.

## Check 3: births and who paid for them (NVSS 2024)

**Targets.** CDC WONDER, Natality 2016–2024 expanded, year 2024, by the mother's legal residence (50 states and
DC). Cells of 1–9 births are suppressed and count as 0.

- Births to mothers of Mexican origin (Maternal Hispanic Origin, expanded: Mexican), by state and in total.
- Births to mothers born in Mexico (Mother's Birth Country: Mexico).
- Source of Payment for Delivery, five categories. The Medicaid share is Medicaid over all births less "Unknown
  or Not Stated", for Mexican-origin mothers, Mexico-born mothers and all mothers. The group's share of
  Medicaid-paid births is the Mexican-origin mothers' Medicaid births over all Medicaid births.

[SOURCE: WONDER natality expanded help, saved in `_cache/`]

**Predictions** (adopted reading). The published reading differs only through the weights of Mexico-born women
outside CA+TX [DATA: derived/prediction_scalars.csv, derived/birth_cells.csv].

**3a. Births to Mexican-origin mothers.**

| Statistic | Prediction | Baseline 1: share of women 15–44 | Baseline 2: share of civilians | Tolerance | Role |
|---|---|---|---|---|---|
| Share of all births | 14.43% (SE 1.10pp) | 13.90% | 11.84% | ±10% relative | verdict |
| Count | 512.3k (SE 38.1k) | 493.5k | 420.3k | ±10% relative | secondary |

The frame holds 3.551m infants (SE 48.6k). The share cancels the CPS's overall coverage of infants; the count
does not.

Distribution over six cells, children 0–2 (verdict; tolerance 0.05; expected dissimilarity from sampling noise
alone 0.041):

| Reading | CA | TX | AZ | IL | NM+NV+CO | Rest |
|---|---|---|---|---|---|---|
| Prediction, % | 25.9 | 30.5 | 5.3 | 5.7 | 6.1 | 26.4 |
| SE, pp | 2.2 | 2.6 | 1.1 | 1.1 | 1.0 | 2.1 |
| Baseline 1: union women 15–44 | 31.3 | 24.6 | 6.0 | 5.0 | 6.7 | 26.3 |
| Baseline 2: union residents | 32.9 | 24.6 | 5.8 | 4.5 | 6.3 | 25.8 |
| Infants alone (secondary; noise 0.075) | 23.5 | 35.6 | 5.2 | 4.3 | 5.0 | 26.5 |

The prediction is 0.067 in dissimilarity from baseline 1 and 0.078 from baseline 2. NM, NV and CO are pooled,
and the other states are grouped as "rest", because they hold too few children in the frame to stand alone.

**3b. Births to Mexico-born mothers: no power.** The prediction is a 4.10% share of births (SE 0.69pp) and a
count of 145.4k (SE 24.2k); the baselines are 3.02% and 3.40%. The distribution over the six cells is 21.2,
25.1, 4.9, 8.2, 6.1 and 34.5%, with noise 0.075. None of these is powered.

**3c. Medicaid-paid births, Mexican-origin mothers.**

| Statistic | Prediction | Baselines | Tolerance | Role |
|---|---|---|---|---|
| Group's share of Medicaid-paid births | 18.93% (SE 0.64pp): the union's share of Medicaid-covered women 15–44 | 13.90% (share of women 15–44); 19.37% (share of Medicaid-covered persons of all ages) | ±10% relative | verdict |
| Medicaid share, group over all | 1.362 (SE 0.041) | 1 (no difference); 1.637 (all-age coverage ratio) | ±10% relative | secondary |
| Medicaid share, level (the brief's reading) | 26.77% (SE 0.92pp) | 19.66% (all women 15–44) | ±5pp | secondary; expected to miss low |

Two further readings are secondary. Mothers of infants covered in 2024: a 36.0% level (SE 4.8pp), a 1.316 ratio
and an 18.38% share. Infants' own coverage at interview: 45.4% (SE 4.8pp), 1.327 and 19.15%.

**Named definitional gaps.**

1. Cohort. Age 0 at a March 2025 interview is roughly the cohort born from March 2024 to March 2025, less infant
   deaths.
2. Identity. The frame uses the co-resident mother's Hispanic origin (the mother is present for 91% of the
   group's infants [DATA: derived/prediction_scalars.csv, 3_births_mother_present]) and otherwise the infant's
   own. NVSS records the mother's report on the birth certificate.
3. Coverage. The CPS may cover young children in immigrant households unevenly.
4. Medicaid level. Pregnancy widens Medicaid eligibility, so coverage among all women 15–44 understates the share
   of births Medicaid pays for. The CPS also under-reports Medicaid. This is why the ratio and share readings
   exist: both effects largely cancel in them.
5. Distribution. Children 0–2 cover three birth years, and some move between states.

**What a miss means.**

- 3a share or count: the frame has too few newborns in the group (A > P) or too many. That moves the group's
  population count at age 0. It is immaterial for a year's account, because infants are 1.3% of the group
  [CALCULATION: 512.3k of 39.71m, derived/prediction_audit.json], but it would flag how well the frame covers the
  group's young children.
- 3a distribution: no national key moves, because the school key's state mix is administrative
  (`school_cost_where_enrolled_2026_09_24`). It would mean the frame misplaces the group's children across states,
  which weakens g_s, the regressor of checks 1–2.
- 3c group share: coverage mis-sees the group's births. The adopted Medicaid key is MEPS spending by age band,
  with the medical-ethnicity ratios and the long-term-care carve-out, not a coverage count, so no adopted key
  moves on this check alone. Phase 2 sizes it as (A − P) × Medicaid-paid births (NVSS 2024) × Medicaid spending
  per birth (MACPAC's latest published figure). Above $2bn it opens a follow-up lane on the adopted key's
  maternity component.

**Blindness: not blind for the national figures.** From general knowledge [TRAINING-DATA]:

- about 3.6m US births a year;
- about a quarter to Hispanic mothers, and roughly half of those to mothers of Mexican origin;
- Medicaid pays for about 41% of all births and for about 60% of births to Hispanic mothers.

That recall puts the national share near the prediction and the Medicaid ratio near or somewhat above it. It is
also why the level reading is declared a likely miss. I have no recall of the state distribution or of the
Mexico-born figures. Memos and lanes that mention these births (`demo_momentum_2026_09_16`,
`ir5_fraud_and_cohorts_2026_09_27`, `external_benchmarks_2026_09_24`, the confidence ladder) are unopened.

## Diagnostics declared now

These are reported and never change a call.

1. Each δ refitted without California, and again without Texas.
2. δ with a second regressor: other foreign-born persons' share of the state's amount (`delta_fit_controlled`),
   to ask whether a miss follows the group or immigrants at large.
3. The components: EITC against A59660, ACTC against A11070. The alternative credit target: refundable EITC
   (A59720) + ACTC.
4. The published reading, and ASEC 2024 against tax year 2023 (the matched year).
5. SSI against federal SSI alone.
6. The brief's descriptive slope: A_s / P_s − 1 on the state's group share of residents, with intercept (HC1).
7. For each state named in the brief (CA, TX, AZ, NM, NV, CO, IL), the error A_s / P_s − 1 with the replicate SE
   of P_s.

## Phase 2, fixed now

1. Fetch the primary files:
   - IRS SOI `https://www.irs.gov/pub/irs-soi/23in55cmcsv.csv`;
   - SSA's SSI Annual Statistical Report 2024 state tables;
   - SSA's *OASDI Beneficiaries by State and County, 2024*;
   - CDC WONDER Natality 2016–2024 expanded, queried for 2024 by state of residence × Mexican origin, × mother's
     birth country Mexico, and × source of payment.

   Hash each into `derived/sources.json` and save the quoted definitions and totals in `reads/`.
2. `score.py` imports `estimators.py` and reads `derived/` as frozen. It writes scores for every statistic in
   `derived/power.csv`, the baselines and the diagnostics.
3. For each miss:
   - A δ miss becomes a key correction. At each end, ΔG = L × hf × (s' − s), where s is the adopted reading's key
     share at that end's allocation and s' = s (1 + δ) / (1 + δ s) (`implied_share`). It enters the September 27
     package unchanged as one more shift on that line and key at that allocation; national totals are held.
     Its effect is reported at specifications 48 and 11, with the package's two methods averaged as the package
     averages them. For Social Security, the shift splits between social_security ($1,447.965bn) and
     railroad_retirement ($14.493bn) by national total. Every correction is a candidate, not adopted.
   - Check 3 misses are sized as stated under that check.
4. RESULT.md then gets its verdict line and one line per check.

## Deviations from the brief

1. **Prediction.** The brief's "account's refundable-credit microdata, SSN rule included" is taken as the adopted
   stack before its fill-in step. The adopted case keys the credit line with that stack, not with the builder's
   published keys. The builder's keys, with the paper rule at 0.60, are the published secondary, and the gate
   covers both.
2. **The brief's slope.** It becomes δ, the slope of the error on the group's share of each state's predicted
   amount, with a stated model and a dollar tolerance. The brief's descriptive slope on the group's share of
   residents is still reported.
3. **Births.** Children 0–2 and six cells carry the state distribution, because infants alone lack power. A
   national share sits beside the count, because it cancels the CPS's coverage of infants.
4. **Medicaid.** The ratio and group-share readings sit beside the brief's level reading, because they cancel the
   pregnancy-eligibility gap and CPS under-reporting. The group share is the verdict because it is what dollars
   follow.
5. **Year.** ASEC 2024 against tax year 2023 is added as a matched-year secondary.

## Files

Run from the repository root; `line_amounts.cjs` first, then `predict.py`, then `estimator_check.py`.

| File | What it holds |
|---|---|
| `derived/predictions.csv` | reading × check × series × state: share, replicate SE, group shares under both allocations, other foreign-born share |
| `derived/prediction_scalars.csv` | national key shares, birth counts and shares, Medicaid readings, with replicate SEs |
| `derived/state_replicates.csv.gz` | the 161 replicate values behind every keyed state share and group share |
| `derived/birth_cells.csv` | the six birth cells with their 161 replicate shares |
| `derived/power.csv` | every scored statistic: role (verdict, baseline, secondary), rule, tolerance, sampling SE |
| `derived/estimator_check.csv` | the synthetic check of the δ estimator |
| `derived/line_amounts.json` | the September 27 case's amounts on these lines at specifications 48 and 11 |
| `derived/prediction_audit.json` | pins, gates, sample counts, row-4 factors, on-books shares |
