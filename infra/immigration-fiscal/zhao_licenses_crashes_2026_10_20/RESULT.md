**Verdict:** The cleaned-panel port recovers Zhao's roughly 5% headline: coefficient **0.04922**, state-clustered SE **0.02417**, on `log(1 + fatal crashes)`. The abstract's **0.46 additional crashes per county-year** and **nearly 60% risky-driving attribution** are **not reproduced**. The repo's categorical licensing premise needs correction; this result supplies **no incremental fiscal or social crash charge**. [CALCULATION: `derived/regressions.csv`, `derived/abstract_comparison.csv`, `derived/integration_delta.csv`] [INFERENCE: matching and double-counting assessment below]

**[DEGRADED]** This is an offline NumPy specification port, independently checked by a second fixed-effects implementation. It is not a pyfixest run, full Stata replication, or verification of the unavailable paper's tables. The supplied abstract targets are taken from the worker brief; they were not independently retrieved here. The author package's README and all supplied do-files were read. [SOURCE: `_cache/osf/README.pdf`, `master.do`, `main_results.do`, `appendix.do`, `figures.do`; hashes in `derived/input_hashes.csv`]

## What was reproduced

The main-results specification is unweighted county-year OLS with county effects, year effects, `log(pop)`, unemployment, `log(fuel)`, `log(regularhighway)` and `log(police)`. Errors cluster by the supplied encoded state. Outcomes are fatal-crash counts, not fatalities, all police-reported crashes, convictions, or crashes identified as caused by undocumented immigrants. The outcome transform is `log(1 + count)`. [SOURCE: `main_results.do:10–77`; package README describes the DOT FIRST crash-query source]

The main estimation sample covers **2007–2018**, **34,251 county-years**, **3,121 counties**, and **50 jurisdictions** (the states other than Vermont, plus DC). This is a multi-jurisdiction licensing-policy contrast for crashes involving all drivers. It does not identify the immigration status or Mexican origin of the drivers responsible. [DATA: `derived/regressions.csv`, `derived/sample_states.csv`] [INFERENCE: outcome/population distinction]

| Outcome, main sample | Coefficient | State-cluster SE | 95% interval |
|---|---:|---:|---:|
| Total fatal crashes | 0.049219 | 0.024174 | [0.000639, 0.097800] |
| Non-hit-and-run fatal crashes | 0.046182 | 0.022536 | [0.000894, 0.091470] |
| Hit-and-run fatal crashes | 0.048997 | 0.026444 | [−0.004145, 0.102139] |

[CALCULATION: `derived/regressions.csv`, `sample=main`; CR1 convention and t intervals described in README. No Stata SE parity claim.]

The split is a partition of the underlying counts, verified row by row. The log coefficients do **not** add to the total coefficient, and the hit-and-run interval includes zero. The total estimate's lower interval endpoint is close to zero; it should not be presented as strong precision. [CALCULATION: `reproduce.py` partition guard; table above] [INFERENCE]

Treatment dates are copied literally from `main_results.do`; encoded `state2` is not a FIPS code:

| First treated year | Jurisdictions present in primary panel | Source state2 codes |
|---|---|---|
| 2014 | DC, Illinois, Maryland, Nevada | 9, 14, 21, 29 |
| 2015 | California, Colorado, Connecticut, Delaware | 5, 6, 7, 8 |
| 2016 | Hawaii | 12 |

Vermont (46) is assigned treatment beginning in 2014 by the source but absent from the primary panel. It appears in the separately loaded full-sample robustness. Other jurisdictions are untreated under this code; that is the author's coding, not an independently audited history of eligibility laws. [SOURCE: `main_results.do:16–19,203–225`] [DATA: `derived/sample_states.csv`, `derived/regressions.csv`]

The package's primary file contains **34,265 rows** and **3,122 counties**, versus **37,464** possible county-year cells in that set of counties over its year window: **3,199 cells are absent**, and only **one observed row has zero total crashes**. **14 rows** have missing controls and are excluded from the main estimation. The file is unbalanced. We have not established why county-years are absent; they must not silently be filled with zeros or treated as a complete universe of counties. This task reproduces the cleaned panel, not the raw FARS/FIRST construction. [DATA: `derived/sample_audit.csv`; CALCULATION: balanced capacity minus observed rows]

## Abstract comparison and level conversion

The coefficient-times-100 approximation is **4.92194%**, **0.07806 percentage points below 5%**. Exponentiating gives **5.04508%** on the multiplicative scale of **one plus the crash count**. Because the outcome includes an added one, neither expression is an exact uniform percentage change in crash counts. The percentage headline is nevertheless closely recovered on its apparent log approximation. [CALCULATION: `derived/abstract_comparison.csv`] [INFERENCE]

The estimation sample's mean is **11.35266 fatal crashes per county-year**. Multiplying that mean by the coefficient gives **0.55877**, **0.09877 above 0.46**. A conversion respecting the added one, `(exp(beta)−1) * (mean+1)`, instead gives **0.62320**. These are descriptive plug-ins, not a retransformed causal level ATT; neither reproduces 0.46. The inspected code supplies no level conversion or baseline tying its headline coefficient to the abstract's level number. That discrepancy remains unresolved without the paper's calculation. [CALCULATION: `derived/regressions.csv`, `derived/abstract_comparison.csv`] [SOURCE: inspected do-files]

## Risky driving and the attribution claim

The code estimates separate effects on speeding-, drowsiness- and distraction-involved fatal crashes. It then drops Delaware, DC, Hawaii, Washington and Indiana for a subset described as high coverage, without restoring them before the later event studies and IHS robustness. The dropped jurisdictions are **state2 8, 9, 12, 48 and 15**. The subset uses **32,646 estimation rows** and **45 state clusters**. The labels describe the author's intention; this run does not independently verify reporting coverage. [SOURCE: `main_results.do:95–103,107–179`] [DATA: `derived/regressions.csv`]

| Outcome | Full main sample coefficient (SE) | High-coverage subset coefficient (SE) |
|---|---:|---:|
| Speeding | 0.103257 (0.051221) | 0.120301 (0.051382) |
| Drowsiness | 0.009836 (0.029571) | 0.013943 (0.030420) |
| Distraction | 0.020470 (0.075506) | 0.025744 (0.077478) |

[CALCULATION: `derived/regressions.csv`, `mechanism_all` and `mechanism_high_coverage`; coefficients on `log(1 + category count)`.]

The speeding outcome increases under both samples. The drowsiness and distraction estimates are imprecise. These regressions do not identify a mediated share of the total effect: the categories are not supplied as mutually exclusive cells, their log coefficients cannot be added, and a crash recorded with speeding is not a causal attribution to licensing-induced risky behavior. **No code in the supplied do-files computes a 60% risky-driving fraction.** [SOURCE: `main_results.do:93–103`; all four do-files inspected] [INFERENCE]

There is a different **mediation analysis** in `appendix.do:460–550` and `master.do:838–930`. It regresses state-level log fatal crashes on treatment and mediators for vehicles, carpooling, commuting and transit time, then calculates product-of-coefficient indirect effects. It requires **`mediation_analysis.dta` and `mediation_clean.dta`**, both absent from the supplied cache. The README calls the mechanism dataset `mediation_mechanism.dta`, another unresolved naming mismatch; that file is absent too. Even with those files, a residual after travel mediators would not on its own establish risky driving as the mechanism. The published 60% claim remains **unreproduced**, not falsified. [SOURCE: the cited mediation blocks and README.pdf] [DATA: `derived/do_file_inputs.csv`] [INFERENCE]

The omitted `usa_00008.dta` ACS extract is needed for the likely-undocumented/native-proxy migration checks and for vehicle ownership, carpooling, commuting and travel-time regressions. Those analyses cannot be reconstructed here. The missing mediation files are an independent obstacle: the provided do-files do not supply a complete raw-ACS-to-mediation build. None of these missing files is needed for the headline, hit/non-hit or risky-outcome regressions reproduced above. [SOURCE: `appendix.do:329–362,423–550`; `master.do:702–735,796–930`] [DATA: `derived/do_file_inputs.csv`]

## Staggered adoption and disconfirmation

`main_results.do:142–156` runs TWFE event studies and **Sun–Abraham interaction-weighted event studies** (`eventstudyinteract`), not csdid or did_imputation. The port fits the supplied cohort interactions and uses observed cohort shares at each event time. The control cohort is never-treated. The exact finite event list is retained; periods outside it remain in the omitted category alongside the nominal reference period. The state drops above remain in force, removing DC, Delaware and Hawaii from the treated cohorts. [SOURCE: `main_results.do:100,110–156`] [CALCULATION: `reproduce.py`, `derived/sa_cohort_weights.csv`]

| Event time, total fatal crashes | TWFE coefficient (SE) | Interaction-weighted coefficient (conditional SE) |
|---|---:|---:|
| 0 | 0.008070 (0.037145) | 0.006950 (0.026543) |
| +1 | 0.049113 (0.030797) | 0.048670 (0.019703) |
| +2 | 0.061143 (0.027718) | 0.060043 (0.017741) |
| +3 | 0.064536 (0.038450) | 0.065191 (0.024185) |

[CALCULATION: `derived/event_studies.csv`; all leads and all three main outcomes are retained there.]

The later post-treatment points remain positive with the interaction-weighted estimator. **[DEGRADED]** Its covariance conditions on estimated cohort shares and omits eventstudyinteract's additional estimated-share uncertainty; these SEs and intervals cannot be called exact Sun–Abraham/Stata inference. There is no single aggregate robust ATT in the supplied commands or this output. The pre-treatment estimates do not by themselves prove parallel trends, and all these estimates inherit the source panel's coverage and model assumptions. [CALCULATION: `derived/event_studies.csv`] [INFERENCE]

The full-sample robustness including Vermont gives **0.042463**, SE **0.023856**, interval **[−0.005452, 0.090379]**, on **34,408 estimation rows**. The point remains positive but its interval includes zero. IHS total-crash robustness on the persistently reduced sample gives **0.054761**, SE **0.027823**, interval **[−0.001313, 0.110835]**. This changes both the transform and sample relative to the headline; it is not a pure transform test. These are material checks against treating the headline's near-zero lower bound as a decisive result. [CALCULATION: `derived/regressions.csv`] [INFERENCE]

Pedestrian and time-of-day specifications were also reproduced and retained, rather than selected by significance. PPML, conditional negative binomial with bootstrap, the source's trend-adjustment procedure, state VMT/licensed-driver outcomes, other appendix estimates and randomized placebos were not ported. Several placebo inputs and base-year state-characteristic files are absent; generated placebo intermediates are not evidence of missing raw inputs. The reference inventory records the distinction to investigate. [SOURCE: all four do-files] [DATA: `derived/regressions.csv`, `derived/do_file_inputs.csv`]

## Relevance to the repo's crash charge

The live declaration is **oct16 / main_case_2026_10_16**, adopted **2026-10-20**. Its fiscal corrections payload contains no crash item: crashes are a social-cost companion. The active social consumer, `sept24_propagation_2026_09_24/real_costs_totals.py`, loads `road_crash_externality_2026_09_28/derived/items.csv` through `SOCIAL_ITEMS`, then applies the selected capacity adjustment; its oct16 route calls `v9_transport.crash_at_new_capacity`. That function uses the existing crash capacity items and a VMT-inclusive traffic share, not a new licensing-policy effect. No complete oct16 social output directory was present when inspected, so this memo does not invent a current dollar crash level. [SOURCE: `../live_case.json`; `../main_case_2026_10_16/derived/corrections.json`; `../sept24_propagation_2026_09_24/real_costs_totals.py:144–169,819–848`; `../sept24_propagation_2026_09_24/v9_transport.py:53–76`]

The source crash model's fatal involvement is **`m = (1+r_c)/2`**, with `r_c` taken from observed FARS culpability odds; its split evaluator uses separately observed CCRS non-fatal inputs. Its traffic share takes the group's VMT key. These observations are made with licensing policies already in force. They are proxies and model inputs, not a measured causal effect of licensing; nevertheless, replacing them with themselves times Zhao's policy coefficient would add a policy increment to observed risks that already reflect actual policy conditions. [SOURCE: `../road_crash_externality_2026_09_28/crash_model.py` docstring, lines 76–81,145–174,219–267] [INFERENCE]

Zhao's policy effect covers all-origin undocumented eligibility and county-wide fatal crashes over the study window. The repo's removal calculation covers Mexican-immigrant lineage driving, harms to others, fatal and non-fatal components and an existing-policy baseline. The county-year coefficient supplies neither a Mexican-lineage per-mile involvement update nor a coefficient for every crash component. Under the FAQ's population/horizon/outcome matching rule, the incremental charge applied here is **$0bn fiscal and $0bn social crash**. That is the consequence of retaining the existing inputs, not a finding that licensing has zero effect. A different policy counterfactual would need matched exposure, affected-population and component-specific causal estimates. [SOURCE: FAQ, “Before combining numbers,” matching rule] [CALCULATION: `derived/integration_delta.csv`] [INFERENCE]

What does change is the confidence in the old blanket premise. The existing crash lane cites **Lueders, Hainmueller and Lawrence (2017)** on California AB60's initial **2015** experience, reporting no detected total- or fatal-crash increase and fewer hit-and-runs. Zhao instead pools several jurisdictions and follows later post-adoption years, measuring fatal crashes only. Those scopes can yield different results without either estimate directly refuting the other's specific estimand. **“Licensing therefore moves compensation, not crash frequency” is too categorical.** The Lueders effect size and uncertainty remain a repo GAP: this task has not obtained or estimated them, and a null finding is not proof of a precisely zero effect. [SOURCE: `../road_crash_externality_2026_09_28/RESULT.md:209–212`, existing abstract/introduction record; Zhao code above] [INFERENCE]

## Draft correction — do not apply from this lane

> [2026-10-20] The California AB60 study by Lueders, Hainmueller and Lawrence (2017) reports no detected increase in total or fatal crashes in its initial 2015 setting and fewer hit-and-runs; its effect size and uncertainty remain a GAP here. That does not establish that licensing never changes crash frequency. Zhao (2025), using a multi-jurisdiction county panel, reports an increase in fatal crashes: the public-package port recovers 0.04922 on log(1 + fatal crashes), state-clustered SE 0.02417, over 2007–2018. The abstract's 0.46-crash conversion and nearly 60% risky-driving attribution are not reproduced. The studies differ in geography, follow-up and outcome, so their causal conclusions remain unreconciled. This corrects the premise without adding a licensing multiplier to m: the model's FARS and CCRS involvement inputs already describe driving under policies in force, and the new estimate is not matched to the lineage's per-mile involvement or all crash components. [CALCULATION: `../zhao_licenses_crashes_2026_10_20/derived/regressions.csv`] [SOURCE: Zhao replication code; existing Lueders abstract/introduction record] [INFERENCE]

## Verification and epistemic limits

All input hashes, panel uniqueness, count partition and numerical-rank/convergence checks pass. Every regression and event model is checked against a separately constructed county-within/year-dummy OLS calculation, including its CR0 cluster covariance. This verifies the implementation algebra, not identification, raw-data construction or published-table parity. The source does not identify individual immigration status in the crash outcomes. [CALCULATION: `reproduce.py`; successful run and byte-rerun receipt recorded in the worker result]

This memo uses the repo's other-residents removal frame for integration; it does not evaluate licensing's full welfare balance. The LLM is a fallible and potentially politically biased research instrument. Directional safeguards here are reporting the positive headline, its weaker robustness intervals, the unavailable attribution, and the older California null under the same scope/uncertainty standard. [FRAMING-SENSITIVE] [INFERENCE]
