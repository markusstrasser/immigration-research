# Immigration Costs — Causal Check, DAG, and Robustness on a Measurable Long-Tail Channel

**Question:** If we stop presupposing a headline NPV and instead run the named causal skills honestly, what can we actually identify about the long-tail costs of unauthorized immigration from the local source set?  
**Date:** 2026-03-13  
**Tier:** Deep  
**Primary domain:** Economics / policy  
**Secondary domain:** Investigative social science  
**Instrument caveat:** Immigration is framing-sensitive. This memo leans on official budget documents and reproducible local data assembly. Narrative claims about cohesion, identity, or civilizational decline are not treated as identified causal quantities here. [SOURCE: `notes/llm-bias-caveat.md`]

## Scope and Ground Truth

This memo does **not** estimate the "true total cost" of immigration. That question mixes budgets, congestion, housing, labor-market redistribution, political backlash, and social capital, which cannot be identified from the current local files in one regression. [INFERENCE]

It instead isolates one channel that is actually measurable with the available data:

- **Treatment candidate:** state exposure to the 2021-2023 immigration surge, proxied by weighted ACS 2023 counts of foreign-born noncitizens with `YOEP` in `2021-2023`. [SOURCE: `sources/immigration-fiscal/data/census/acs_pums_2023_person.zip`] [SOURCE: `sources/immigration-fiscal/data/derived/build_state_response_cost_dataset.py`] [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_dataset.csv`]
- **Outcome:** explicit 2023 state/local response spending identified by CBO for eight states, normalized per 100,000 residents. This includes shelter-related spending in `NY`, `MA`, `IL`, `CO` and border-security/transport spending in `TX`, `AZ`, `FL`, `CA`. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf] [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_dataset.csv`]
- **Pre-treatment confounders available in minimal form:** `border_state` and `right_to_shelter`. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf] [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_dataset.csv`]

### Local inventory

1. `CBO 61256` for state/local costs, state concentration, and footnoted mechanisms. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
2. `ACS 2023 PUMS` person microdata for recent noncitizen exposure proxies. [SOURCE: `sources/immigration-fiscal/data/census/acs_pums_2023_person.zip`]
3. `ITEP 2024` state/local tax table for descriptive context only, not as a surge-specific offset. [SOURCE: https://itep.org/undocumented-immigrants-taxes-2024/] [SOURCE: `sources/immigration-fiscal/data/itep/itep_table_2.tsv`]
4. Derived reproducible dataset and model outputs produced in this session. [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_dataset.csv`] [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_models.json`] [SOURCE: `sources/immigration-fiscal/data/derived/exposure_response_dag_result.json`] [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_sensemakr_recent_exposure.json`] [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_sensemakr_right_to_shelter.json`]

## Researcher Axes

Selected search/analysis axes after local ground truth review:

1. **Mechanism axis:** does measured state/local response cost scale with realized surge exposure? [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf] [SOURCE: `sources/immigration-fiscal/data/census/acs_pums_2023_person.zip`]
2. **Adversarial axis:** is the visible cost concentration mostly an accounting artifact rather than a real causal pattern? [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
3. **Adjacent/practitioner axis:** do shelter-law and border-response institutions convert similar exposure into radically different budget footprints? [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]

## Causal Check

### Phase 0 — Observation

**Observation:** In the eight states for which CBO gives explicit 2023 response-spending fragments, `NY` and `TX` account for about `84.5%` of the identified spending (`$5.1B` of `$6.035B` midpoint), while CBO's own state-of-residence table says those two states held only `22%` of the surge population (`NY 7%`, `TX 15%`). By contrast, `FL` and `CA` together held `33%` of the surge population (`FL 22%`, `CA 11%`) but only about `0.6%` of the identified spending in this eight-state breakdown (`$36M` of `$6.035B`). [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf] [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_dataset.csv`]

**Null:** If response costs were driven mainly by the number of recent migrants resident in a state, spending should scale roughly with surge exposure after adjusting for population size. [INFERENCE]

**Residual after null:** It does not. Florida has the highest ACS recent-noncitizen exposure in this eight-state set (`2,638.3` per `100k` residents) and almost no explicit response spending (`0.0929` per `100k` residents), while New York has lower exposure (`1,742.2` per `100k`) and extremely high explicit response spending (`13.2848` per `100k`). [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_dataset.csv`]

**Geometry:** Isolated cluster, not smooth dose-response. The high-cost states are concentrated in two institutional buckets: right-to-shelter jurisdictions (`NY`, `MA`) and exceptional border-response jurisdictions led by Texas. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf] [INFERENCE]

**Magnitude:** The simple exposure-only model has `R^2 = 0.012`; the residuals are largest for `NY (+9.28)` and `TX (+4.01)`, and most negative for `FL (-4.77)` and `CA (-3.83)`. That is far outside a "costs scale with heads" story in this sample. [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_models.json`]

**Lag window:** Pre-2021 legal and institutional settings matter. New York's and Massachusetts's shelter regimes predate the surge, and Texas's Operation Lone Star began in `2021`, with spending visible in `2023`. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]

### Phase 1 — Shape-Constrained Hypotheses

| Hypothesis | Prior | Why it fits the geometry |
|---|---:|---|
| `H1` Institutional-response regime: preexisting shelter mandates plus discretionary border-security responses convert exposure into very different spending totals | 0.45 | Predicts clustered outliers rather than smooth scaling |
| `H2` Measurement / accounting artifact: CBO found public data only for a few states and categories, so apparent concentration overstates real concentration | 0.25 | Predicts missing-cost asymmetry across states |
| `H3` Destination/housing concentration: asylum seekers disproportionately entered metros with high shelter use and housing scarcity | 0.20 | Predicts `NYC/Boston/Chicago/Denver` concentration |
| `H4` Raw exposure volume: more recent migrants simply caused more spending | 0.10 | Predicts smooth positive slope with exposure |

Priors sum to `1.00`. [INFERENCE]

### Phase 2 — Natural-Experiment Style Checks

1. **Cross-sectional variation:** Florida has the highest recent-exposure proxy and almost no explicit spending. That is direct disconfirmation of `H4` as a standalone explanation. [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_dataset.csv`]
2. **Institutional variation:** CBO explicitly attributes large shelter spending to `NYC` and `MA`, both right-to-shelter settings, and attributes `TX` spending to extraordinary border-security operations. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
3. **Adjacent-domain concentration:** CBO cites Meyer, Wyse, and Williams for the finding that `NYC`, suburban Boston, Chicago, and metro Denver accounted for about `90%` of the national increase in asylum seekers in shelters from `2022` to `2024`. That is much more consistent with `H1/H3` than with `H4`. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]

No clean quasi-experiment exists in the local data because the sample is tiny, the outcome is partially hand-collected from public budgets, and institutional variables are heavily clustered. [INFERENCE]

### Phase 3 — Specificity Ranking

| Hypothesis | Temporal | Magnitude | Scope | Mechanism | New prediction | Total |
|---|---:|---:|---:|---:|---:|---:|
| `H1` Institutional-response regime | 3 | 3 | 3 | 3 | 3 | 15 |
| `H3` Destination/housing concentration | 2 | 2 | 2 | 2 | 2 | 10 |
| `H2` Measurement / accounting artifact | 2 | 2 | 2 | 3 | 1 | 10 |
| `H4` Raw exposure volume | 3 | 0 | 1 | 2 | 0 | 6 |

**New prediction checked for `H1`:** once `border_state` and `right_to_shelter` are added, the exposure slope should collapse toward zero because the visible spending variation is mostly sitting in those institutional buckets. That prediction holds: the exposure coefficient moves to `-0.000493` with a `p`-value of `0.889`. [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_models.json`]

### Phase 3b — Recursive Causal Audit

`H1` chain: `Institutional regime -> destination / response rules -> category-specific spending -> observed 2023 cost concentration` [INFERENCE]

RCA for `H1`:

- `Right-to-shelter / border regime -> response obligations or operational latitude`  
  directional: yes  
  necessary: no  
  proportional: partial  
  confounder risk: medium  
- `Response obligations / operational latitude -> observed 2023 spending`  
  directional: yes  
  necessary: partial  
  proportional: yes  
  confounder risk: medium  
- `Recent exposure -> spending`  
  directional: yes  
  necessary: partial  
  proportional: weak in this sample  
  confounder risk: high

**Weakest link:** `Recent exposure -> spending` as a smooth proportional relationship. The measured data do not support that shape once institutional variables are present. [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_models.json`]

**Bad controls to avoid:** `Shelter_Use` and `State_Response_Intensity`. Both are descendants of exposure and mediators on the path to spending. Conditioning on either would over-control the total effect of exposure. [INFERENCE]

### Phase 4 — Commit

**Most likely cause (0.60):** institutional-response regime, not raw exposure volume, is the leading explanation for the visible 2023 spending concentration. The strongest observed outliers are jurisdictions with preexisting shelter mandates or extraordinary border-response policy. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf] [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_dataset.csv`] [INFERENCE]

**Top alternative (0.20):** accounting artifact. CBO states that it could not find public data on shelter costs in other states and treated the explicit states as accounting for "most" of such spending. That weakens any claim that the observed concentration is the full national picture. This is less specific than `H1` because it does not explain why the identified spending maps so closely onto institutional buckets. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]

**Falsifier:** if a larger state-year panel with consistent budget coding shows response spending scales smoothly with recent-exposure proxies and the `right_to_shelter` / border-policy variables no longer matter, `H1` should be downgraded sharply. [INFERENCE]

**Decision impact:** if `H1` is right, the measured long-tail fiscal burden is driven less by immigrant headcount alone than by where migrants land and how state institutions are structured to respond. That pushes analysis toward heterogeneous local cost channels, not universal per-person negative NPV claims. [INFERENCE]

## Causal DAG

### Phase 1 — Variable Classification

| Variable | Classification | Temporal order | Justification |
|---|---|---|---|
| `Recent_Exposure` | Treatment (`X`) | 2021-2023 before 2023 spending ledger closes | Weighted ACS proxy for recent noncitizen arrivals exposed to state systems |
| `Response_Spending` | Outcome (`Y`) | 2023 | Explicit CBO-identified state/local response spending |
| `Border_State` | Pre-treatment confounder (`C`) | Before surge | Geography affects both exposure and border-security spending |
| `Right_To_Shelter` | Pre-treatment confounder (`C`) | Before surge | Preexisting shelter obligation affects destination and shelter spending |
| `Shelter_Use` | Mediator (`M`) | After exposure, before spending | Exposure raises shelter use, which raises spending |
| `State_Response_Intensity` | Mediator (`M`) | After exposure, before spending | Exposure can trigger emergency appropriations / transport / enforcement operations |

### Phase 2 — DAG in Text Notation

```text
Recent_Exposure -> Response_Spending
Right_To_Shelter -> Recent_Exposure
Right_To_Shelter -> Response_Spending
Border_State -> Recent_Exposure
Border_State -> Response_Spending
Recent_Exposure -> Shelter_Use -> Response_Spending
Recent_Exposure -> State_Response_Intensity -> Response_Spending
Border_State -> State_Response_Intensity -> Response_Spending
```

Validated machine-readable DAG result: `adjustment_set = {Border_State, Right_To_Shelter}` with no bad-control problems in the proposed control set. [SOURCE: `sources/immigration-fiscal/data/derived/exposure_response_dag_spec.json`] [SOURCE: `sources/immigration-fiscal/data/derived/exposure_response_dag_result.json`]

### Phase 3 — Adjustment Set

**Valid adjustment set:** `{Border_State, Right_To_Shelter}`. [SOURCE: `sources/immigration-fiscal/data/derived/exposure_response_dag_result.json`]

**Excluded and why:**

- `Shelter_Use`: mediator; conditioning would block part of the causal path. [INFERENCE]
- `State_Response_Intensity`: mediator / descendant of treatment; conditioning would over-control the total effect and may open collider problems if other unmeasured parents exist. [INFERENCE]

**Remaining open back-door paths:** none in the minimal DAG. [SOURCE: `sources/immigration-fiscal/data/derived/exposure_response_dag_result.json`]

**Unobserved threats:** preexisting immigrant networks, local housing scarcity, and general state policy posture could still confound the treatment-outcome relationship in a larger and better measured design. The current DAG validates the minimal observable control set, not the truth of the no-unmeasured-confounding assumption. [INFERENCE]

### Phase 4 — Bad-Control Audit

| Variable | In DAG? | Classification | In valid adjustment set? | Problem? |
|---|---|---|---|---|
| `Recent_Exposure` | Yes | Treatment | n/a | None |
| `Response_Spending` | Yes | Outcome | n/a | None |
| `Border_State` | Yes | Confounder | Yes | None |
| `Right_To_Shelter` | Yes | Confounder | Yes | None |
| `Shelter_Use` | Yes | Mediator | No | `OVER-CONTROL` if included |
| `State_Response_Intensity` | Yes | Mediator / descendant of treatment | No | `OVER-CONTROL / COLLIDER RISK` if included |

### Phase 5 — Clean Specification

```text
Model:      response_spending_per_100k_residents_mid
            ~ recent_noncit_per_100k_residents + border_state + right_to_shelter
Treatment:  recent_noncit_per_100k_residents
Controls:   border_state, right_to_shelter
Excluded:   shelter_use, state_response_intensity
Estimand:   Total effect of measured recent exposure on explicit 2023 response spending
            within the eight-state sample, conditional on the minimal observed confounders
```

**Assumptions:**

1. No material unmeasured confounding after conditioning on `border_state` and `right_to_shelter`. [INFERENCE]
2. The ACS recent-noncitizen proxy is a reasonable ranking of state exposure. [INFERENCE]
3. CBO's explicit spending fragments are comparable enough across states to treat as a common outcome family. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf] [INFERENCE]
4. Linear additivity is tolerable in a tiny illustrative sample. [INFERENCE]

**Threats:** tiny `n`, interval-censored Colorado outcome, omitted housing/political confounders, and incomplete national budget coding. [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_dataset.json`] [INFERENCE]

## OLS and Robustness

### Main exposure model

Formula:

```text
response_spending_per_100k_residents_mid
~ recent_noncit_per_100k_residents + border_state + right_to_shelter
```

Results:

- `n = 8`, `R^2 = 0.4624`, adjusted `R^2 = 0.0592`. [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_models.json`]
- Coefficient on `recent_noncit_per_100k_residents = -0.000493`, `p = 0.889`. [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_models.json`]
- Confidence interval includes both moderate negative and moderate positive slopes (`-0.009735` to `0.008750`). [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_models.json`]
- The sign is not meaningful here; the substantive result is that the slope is effectively indistinguishable from zero once the two institutional controls are included. [INFERENCE]

Sensitivity:

- `Robustness Value = 0.0713`. [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_sensemakr_recent_exposure.json`]
- Interpretation from the sensitivity tool: **fragile**. An omitted confounder as strong as an observed covariate could explain away the effect. [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_sensemakr_recent_exposure.json`]

**Takeaway:** this small-sample model does **not** support the claim that per-capita recent exposure by itself explains the measured spending concentration. [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_models.json`] [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_sensemakr_recent_exposure.json`] [INFERENCE]

### Structural check on `right_to_shelter`

Swapping the treatment to `right_to_shelter` in the same regression yields a coefficient of `7.69134` with `RV = 0.586`, which looks much more stable numerically. [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_sensemakr_right_to_shelter.json`]

That is **not** a headline causal estimate for the total effect of shelter law. It is a direct-effect style diagnostic inside a mis-specified total-effect model, because recent exposure plausibly sits downstream of `right_to_shelter`. Controlling for exposure while treating `right_to_shelter` as the treatment would condition on a descendant of treatment. [INFERENCE]

**Useful interpretation:** institutional variables are where the visible action lives in this sample. **Not useful interpretation:** "`right_to_shelter` causally adds exactly `7.69` spending units per `100k` residents." [INFERENCE]

## Best Current Judgment

1. The measurable long-tail channel here is **real but highly heterogeneous** across states. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
2. The observed 2023 spending concentration is **better explained by institutional response and category-specific state policy** than by immigrant counts alone. [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_dataset.csv`] [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_models.json`] [INFERENCE]
3. That does **not** imply the broader full-spectrum cost question is small. It implies the costs are **conditional and locally state-dependent**, which is different from saying there is one nationally stable per-person number. [INFERENCE]
4. The present data do **not** justify a clean causal estimate of "the real long-tail total cost" and do **not** rescue a `-$200k` claim by identification alone. To get there, you still need a stack of partially measured or unmeasured channels. [SOURCE: `research/immigration-path-to-minus-200k-scenario-audit.md`] [INFERENCE]

## What Would Actually Improve This

1. A `50-state x multi-year` panel with consistent coding of shelter, emergency aid, transport, border-security, education, and hospital uncompensated-care responses. [INFERENCE]
2. A pre-surge baseline for the same spending categories, not just post-surge point estimates. [INFERENCE]
3. Better pre-treatment controls for immigrant-network strength, local housing scarcity, and state policy posture. [INFERENCE]
4. A model that estimates **interaction effects** between exposure and institutional regime, because the present results strongly suggest heterogeneity rather than a common slope. [INFERENCE]

## Bottom Line

Running the named causal skills honestly narrows the claim rather than inflating it. The best-supported conclusion from this measurable sub-analysis is:

> explicit 2023 state/local response costs are concentrated where exposure interacted with specific institutions and discretionary policy responses; they do not scale cleanly with recent immigrant headcount alone. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf] [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_dataset.csv`] [SOURCE: `sources/immigration-fiscal/data/derived/state_response_cost_models.json`] [INFERENCE]

That makes the full-spectrum cost story **more local and more nonlinear** than either side's clean national talking number. [INFERENCE]
