**Verdict:** The disability gradient survives three held ASEC years and a conservative bound allowing arbitrary cross-year covariance. Descendants' excess over whites remains unresolved. The trust gap survives including “depends,” NORC's preferred nonresponse-adjusted weights, and full available strata/PSU variance; these repairs do not overturn the headline. There is no precise adjusted generational trust trend. Neither result identifies an intergenerational causal trajectory or civilizational welfare effect.

All numerical results below are **[DATA]**, computed from held raw CPS/GSS files and integrated in this lane. Raw files were not changed. Date: 2026-09-17.

## Consequential disability findings

Adults 25–64, civilian household universe, valid PRDISFLG. Equal-weighted mean of the 2024, 2025 and 2026 ASEC estimates, standardized to the same fixed eight five-year age-band distribution of 2025 third-plus non-Hispanic whites:

| Group | Disability prevalence |
|---|---:|
| Mexico-born | 5.07% |
| US-native, at least one reported Mexico-born parent | 8.42% |
| US-native, US-native parents, Mexican self-ID | 11.15% |
| Third-plus non-Hispanic white comparison | 9.74% |

| Direct contrast | Difference, percentage points | Conservative approximate 95% interval |
|---|---:|---:|
| Second generation − Mexico-born | +3.35 | +1.47 to +5.23 |
| Third-plus self-ID − second generation | +2.73 | +0.36 to +5.10 |
| Second generation − white comparison | −1.32 | −3.06 to +0.42 |
| Third-plus self-ID − white comparison | +1.41 | −0.38 to +3.20 |

The older “advantage disappears by G2 and reverses by G3” formulation remains too strong. The first-to-second group difference is clear under the conservative variance bound; third-plus self-identifiers also exceed second generation in the pooled primary contrast. Neither descendant-white contrast establishes an excess or equivalence. These are contemporaneous selected groups, not observed successive generations of the same families. [INFERENCE grounded in the contrasts.]

**Meaningful alternative explanations tested.** The G2-minus-Mexico-born contrast survives separately for men (+3.54 pp, +0.79 to +6.29) and women (+3.16, +0.46 to +5.85). It is positive within the approximate 1965–84 and 1985–99 birth cohorts: +3.57 (+0.85 to +6.28) and +1.74 (+0.22 to +3.26), respectively. Cohorts are survey year minus reported age, with birthday uncertainty; their estimates are crude within the cohort bins, not the age-standardized headline or a panel effect. These tests weaken a pure age/sex-composition explanation without removing migration, family-history, reporting or identity selection.

**One-versus-two Mexico-born-parent split is informative but exploratory.** Age-standardized G2 prevalence is 10.52% with exactly one parent coded Mexico-born versus 6.92% with two, difference +3.60 pp (−0.11 to +7.30). The female split is larger at the point estimate, but subgroup exploration is not multiplicity-adjusted and no sex interaction is established. This is not a genetic-dose result: the comparison changes family formation, identity, resources and origin mix. “One” means one recorded Mexico-born parent, not a fully known family tree. Tables retain annual counts and events; the primary G2 cells contain 2,410/2,452/2,461 people across years.

**Annual stability.** Standardized G2 disability is 7.84%, 8.61%, 8.80%; Mexico-born 5.23%, 4.49%, 5.48%; third-plus self-ID 11.34%, 11.27%, 10.84%; white comparison 9.72%, 9.82%, 9.69%. No year-to-year change is labeled causal or significant. The old 2025 prevalence and SDR standard errors reproduce to numerical precision for all four main groups.

## Overlap and honest precision

Full files contain 144,265 / 142,125 / 134,729 records. Every person joins one-to-one to all 161 weights; MARSUPWT/100 matches PWWGT0 to within rounding (<0.006). PERIDNUM is read as a 22-character string, never a floating-point number. Adjacent files share 47,262 and 39,927 exact IDs; 45,910 and 38,796 also satisfy the broad same-sex/age-increment diagnostic. The 2024–26 pair shares none. These checks demonstrate overlap; they do not establish a valid longitudinal sample, explain every mismatch, or validate cross-year replicate-coordinate alignment.

Annual variance is the documented SDR formula, `4/160 × sum((replicate − full)^2)`. Direct contrasts are formed within each replicate, preserving within-year covariance. For pooled annual estimate `mean(theta_y)`, the unknown-covariance standard error is bounded above by `sum(SE_y)/3` (Cauchy–Schwarz). The report uses this upper bound, not the smaller independent-year SE. Every table saves the upper/lower possible SE and the independence calculation solely as a diagnostic. Exact cross-year design covariance was not verified. Consequently this is overlap-robust conservative precision, not an efficient longitudinal estimator. The age target is held fixed by estimand, not treated as an estimated nuisance population distribution.

Weights retain each release's population-control vintage. Pooling describes the arithmetic mean of these published-design annual populations, not a common-vintage population trend. Three years can repeat people and birth cohorts; they are not three independent replications.

## Disability prevalence is not disability expenditure

The same age-standardized equal-year estimates separate the prior income total:

| Annual dollars per adult, nominal income years 2023–25 averaged | Mexico-born | Second generation | White comparison |
|---|---:|---:|---:|
| Social Security with disability reported as a reason + SSI | $281 | $701 | $767 |
| Other payments explicitly coded government/military/railroad/state sickness | $36 | $110 | $82 |
| Company/union or accident/disability insurance | $35 | $26 | $72 |
| Workers compensation, black-lung, other/unknown source | $70 | $87 | $91 |
| Total of all these reported payments | $422 | $925 | $1,012 |

G2 minus white is −$66 (−$339 to +$208) for Social Security-with-disability-reason plus SSI, and −$87 (−$423 to +$249) for the total. This does not support higher G2 disability payments. No real-dollar growth is inferred from the nominal multi-year average. Social Security may report multiple receipt reasons, so the selected Social Security amount is not an administrative SSDI disbursement measure. The government-coded other category includes occupational entitlements; company/insurance income is not government cost. Workers compensation/black-lung/unknown are deliberately not silently assigned to public or private funding. The partition exactly reconciles to the old total person by person.

Primary definitions: archived 2025 dictionary at `infra/immigration-fiscal/ledger_asec2026_2026_09_16/_cache/ddl2025.txt`, DIS_SC1/2 lines 2909–2955 and PERIDNUM lines 1392–1395; [2024 source labels](https://api.census.gov/data/2024/cps/asec/mar/variables/DIS_SC1.json); [2026 dictionary](https://www2.census.gov/programs-surveys/cps/datasets/2026/march/asec2026_ddl_pub_full.pdf), pp.29 PRDISFLG, 49–50 RESNSS1, 55–56 DIS_SC1/2 and amounts. The 2026 API-variable route failed; the official dictionary supplied the primary definition instead. [SOURCE]

## GSS: denominator, weights and variance

The primary TRUST labels are 1 “most people can be trusted,” 2 “can't be too careful,” 3 “depends.” The full three-response distribution, using WTSSNRPS where available (2004 onward) and WTSSPS for 2000/2002:

| Group | Trust | Careful | Depends | Valid n |
|---|---:|---:|---:|---:|
| Hispanic G1 | 11.99% | 82.09% | 5.93% | 1,041 |
| Hispanic G2 | 16.61% | 79.40% | 4.00% | 513 |
| Hispanic G3+ | 21.07% | 74.98% | 3.95% | 623 |
| Third-plus non-Hispanic whites | 37.82% | 56.37% | 5.81% | 10,484 |

These crude differences include composition. The model matching the prior age, age-squared, education and survey-year controls produces these group-minus-white percentage-point contrasts:

| Group | Old definite-response/WTSSPS estimate | Three responses + preferred weights | New design SE |
|---|---:|---:|---:|
| Hispanic G1 | −11.15 | −11.81 | 1.55 |
| Hispanic G2 | −11.63 | −11.22 | 2.01 |
| Hispanic G3+ | −10.52 | −9.73 | 1.99 |

The measured deficit survives. The corrected G3+ minus G1 contrast is only +2.08 pp, SE 2.27 (approximate 95% −2.36 to +6.52); G2 minus G1 +0.59, SE 2.23; G3+ minus G2 +1.49, SE 2.58. Thus these adjusted data establish neither a precise convergence trend nor a precise absence of convergence. A conditional opinion difference is not immigration's total effect, a latent “collectivism” trait or measured institutional damage.

**Variance implementation.** Full available strata/PSU cells are retained, with zero influence outside each analysis domain. Variance sums each stratum's centered PSU influence squares with `n_h/(n_h−1)`. Every stratum has at least two PSUs; all strata are unique to a survey round, matching NORC's instruction. This handles the actual 2021 design rather than assuming every stratum always has exactly two PSUs. WLS influence vectors yield joint covariance for direct generation contrasts. The original unstratified cluster-regression estimates and SEs reproduce to stored rounding; correcting variance changes the relevant SEs only slightly. Independent validation checks the exact two-PSU identity as well as response partitions and the definite/full denominator identity.

**Missingness stays visible.** The residual table retains don't-know, no-answer, inapplicable, and unavailable-year codes separately. Much of the total-file exclusion is inapplicable/unavailable-by-year, so it must not be called respondent refusal or treated as distrust. Unknown generation remains outside named generations. This pool weights survey years by the source weights/sample composition and adjusts year in the conditional model; it is not a single contemporary population estimate.

Primary support: held R3a Stata value labels (`gss_labels.json`); held *GSS 2024 Codebook R3a*, extracted `gss_codebook.txt`, lines 1911–1925 on preferred weights and 2644–2688 on VSTRAT/VPSU/with-replacement design. [NORC design-variable guidance](https://gss.norc.org/content/dam/gss/get-documentation/pdf/other/GSS%20design%20variables.pdf) and [MR137 weighting guidance](https://gss.norc.org/content/dam/gss/get-documentation/pdf/reports/methodological-reports/GSS%20MR137%20Poststratification%20Weights.pdf) supply the same design contract. [SOURCE]

## Reproduction, validation and coverage

`probe.py --repo REPO --output-dir OUT` reads metadata and creates the selected GSS cache; `analyze_social.py --repo REPO --output-dir OUT --part all` runs both analyses (`cps`/`gss` can run separately); `validate.py --output-dir OUT` checks those products. The default output is `derived/social/` under this lane. Run with `UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run python3 ...`; no scipy dependency is required. GSS source labels require Latin-1, now explicit. Raw CPS sources are SHA-256 bound in `cps_audit.json`.

Products: `cps_annual.csv`, `cps_direct_contrasts.csv`, `cps_equal_year_pool.csv`, `cps_audit.json`; `gss_trust_distribution.csv`, `gss_trust_contrasts.csv`, `gss_trust_adjusted.csv`, `gss_trust_residuals.csv`, `gss_audit.json`, `gss_labels.json`; `validation.json`. Raw/selected respondent cache and source-document extracts are derived/local and should not be committed as research data.

**Checks passed:** 468 annual CPS rows, 390 direct contrasts, 286 pooled rows; old 2025 disability rate/SE gate; all person/replicate joins; identity precision/uniqueness; all-source income partition; old GSS coefficient/cluster-SE gate; full response partitions and denominator algebra; contrast variance bounds, pool arithmetic and two-PSU variance identity; scripts compile. Source inference limits survive these checks.

Covered: held CPS2024/25/26 person and replicate files, primary 2024/25/26 definitions, latest disability correction, prior disability estimator, GSS R3a labels/codebook, prior generation/trust estimators and full available GSS design fields. Skipped in this component: other attitudes, NLS crime/education (separate component), fiscal-ledger rebuilding, institutional-population disability and causal family health trajectories. The parent execution integrates these scripts and results in the repository.

Remaining useful gap: a harmonized population-control/longitudinal variance design could improve efficiency, but is not needed to obtain the conservative surviving disability contrast. A causal account of the parent-history pattern requires longitudinal/selection evidence; additional cross-sectional controls would not supply it. [INFERENCE]
