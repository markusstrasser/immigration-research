# Immigration fiscal and welfare ledgers — corrected map

**Current assessment: 2026-09-05.** The coordinates below remain useful. The former sign table, claim that fixing coordinates usually determines the sign, and “three empirically falsified theories” conclusion are superseded. A well-defined question can still lack sufficient evidence; leaving it vague does not make every answer defensible. [SOURCE: [repair decision](../decisions/2026-09-05-material-inference-repair.md)] [INFERENCE]

A scalar estimate is legitimate when it specifies the population, budget or welfare concept, cohort, counterfactual, horizon, discounting and aggregation weights. Its applicability is limited by those choices. A multidimensional table is useful for exposing heterogeneity, but does not itself make the entries measured or causally identified. [INFERENCE]

| Object | Defensible current interpretation |
|---|---|
| Federal budget | CBO projects a roughly $897B deficit reduction in 2024–2034 for its specified surge scenario, covering receipts, mandatory spending and interest. Discretionary appropriations are excluded; the report illustrates about $0.2T additional funding under population-proportional scaling. It is not a realized or lifetime balance. |
| State/local budget | CBO's 2023 estimate and the NAS literature support costs in the populations and accounting scenarios studied. Gross services, fiscal net, marginal costs and household-attribution choices are distinct. |
| Local payroll-minus-selected-benefits model | The old +$1,519 Mexico adult proxy and dependent totals are invalidated. The corrected person-level model remains a partial 2023 cash-flow proxy, not the federal budget. |
| Lifetime / dynasty | NAS education/arrival-age scenarios and descendant-inclusive scenarios are conditional projections. Cross-sectional generational annual balances cannot be added as a lifetime ROI. |
| Native wages | Published evidence includes small average effects and heterogeneous subgroup effects. A negative effect for every low-skill native is not established. QWI policy regressions cannot measure native-specific hourly wages. |
| Aggregate and migrant welfare | Several mechanisms and models support gains, especially for movers. Their magnitudes and transfer to different policies are conditional; there is no universal sign theorem for the full real-world ledger. |
| Consumer prices, profits, entrepreneurship, productivity | Potential mechanisms with overlapping incidence. They are not four separate quantities to sum on top of GDP. |
| PAYG pensions | Additional young contributors can improve near-term financing; future eligibility and contributions must be included to infer long-run solvency. |
| Remittances, rents and taxes | Transfers inside a specified welfare population, before real transaction, resource and distortion costs. Transfers across its boundary affect that population's income. Neither gross payment nor a fiscal deficit alone equals net global welfare loss. |
| Assimilation / crime | Repeated cohort cross-sections and repeated Texas justice outcomes describe their observed populations; they are not by themselves within-person, across-generation or causal institutional tests. |

[SOURCE: [CBO July 2024](https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf)] [SOURCE: [CBO state/local 2025](https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf)] [SOURCE: [current author synthesis](immigration-economist-dismantling-2026-06-25.md)] [SOURCE: [theory-check re-adjudication](immigration-theory-verdicts-2026-06-25.md)] [INFERENCE: accounting and identification boundaries]

Adding a lower-income newcomer can raise total output and lower the mean without making any incumbent poorer. That arithmetic does not hold other people's outcomes fixed in reality; identifying wage, capital, housing and fiscal responses is the empirical task. “Output is additive” therefore rejects a mechanical mean-to-incumbent inference, not every possible adverse externality. [INFERENCE]

The return-migration result formerly called a falsification simply assumed 25% fewer person-years. The innovation result inferred a counterfactual from a missing tag. Neither is empirical mechanism evidence. Do not impose an additional emigration discount or remove an innovation channel from NAS benchmarks on that basis. [SOURCE: [corrected checks](immigration-theory-verdicts-2026-06-25.md)]

The research question remains the fiscal and crime impact of immigration. Welfare weights and the choice of whose outcomes matter are explicit framing decisions; the signs and sizes of those outcomes remain empirical questions. [FRAMING-SENSITIVE]

## Revisions

- **2026-09-05:** Removed unconditional sign assignments, double-counting implications and unsupported falsification/assimilation conclusions under the [material inference repair](../decisions/2026-09-05-material-inference-repair.md).

<!-- historical-snapshot:start superseded=2026-09-05 -->
<details>
<summary>Superseded historical version — retained for provenance</summary>

# The Ledger Map — unifying "is low-skill immigration positive or negative?"

**Date:** 2026-06-23
**Status:** Synthesis / routing doc. Unifies the fiscal incidence tensor (`immigration-lifetime-unified-theory-2026-06-15.md`) with the benefit-side ledgers, and maps every generator cluster (A–T) onto them.
**Frame:** `[FRAMING-SENSITIVE]` — "positive vs negative" is **ill-posed** until you fix four coordinates.

---

## The question is under-specified

"Is low-skill immigration good/bad?" has no scalar answer because the sign depends on **four free coordinates**. Pin them and the sign is usually determinate; leave them free and any answer is defensible (which is why the public debate never resolves).

1. **Welfare boundary** — incumbent-natives-only · all-residents (incl. immigrants) · global. *(G-LIF-T02)*
2. **Ledger ℓ** — which of the books below.
3. **Cell** — education × experience × age-at-arrival × legal status × origin × destination elasticity. *(no scalar "Mexican NPV")*
4. **Cohort / horizon** — first-generation vs dynasty; static-annual vs 75-yr NPV; short-run (capital fixed) vs long-run (capital adjusted). *(G-LIF-A04, T06)*

The recurring debate error is **silently switching one coordinate mid-argument** — e.g. quoting a first-gen state-local fiscal number to rebut an aggregate long-run economic claim.

## The full ledger set, and the sign each tends to show (low-education entrant)

| Ledger ℓ | Typical sign | Why | Generator lens |
|----------|:---:|------|----------------|
| **Fiscal — first-gen, static, state-local** | **−** | Low earnings → low tax; K-12 + Medicaid concentrated locally | C, N, O, R |
| Fiscal — federal annual cash-flow | ~0 / **+** | Payroll incl. unclaimed unauthorized contributions | C01, G, T05 |
| Fiscal — lifetime NPV, <HS cell | **−** (assumption-dependent; can flip **+**) | NAS −$109k; flips to +$128k under Clemens's capital-tax correction (**partial-equilibrium, NOT GE** — see clemens-method-check; contested, AEI 2025) | A01, A02 |
| Fiscal — **dynasty** (incl. 2nd gen) | ~0 / **+** | US-born children are top net contributors | A06, D, C06 |
| Economic — aggregate native surplus | **+** (small) | Immigration surplus positive even in Borjas; complementarity | B02, B04, F02, T06 |
| Economic — **distributional** (low-skill natives) | **−** | The wage hit lands on competing natives (concentrated) | B06, S07–S09 |
| Consumer surplus — non-traded prices | **+** | Lower childcare/food/construction prices (Cortes) | **T03** |
| Labor demand — entrepreneurship/job creation | **+** | Immigrants are net firm founders (AJKM) | **T04**, F04 |
| PAYG dynamic — SS/Medicare solvency | **+** | Young contributors subsidize the existing old | M03, **T05** |
| **Migrant's own welfare** — place premium | **++** (large) | Same worker earns 2–15× more (Clemens-Pritchett) | **T02** |
| Welfare-economics — transfer vs deadweight | n/a (reframe) | A fiscal deficit is a financed transfer, not a net loss | **T08** |

**The shape of the answer:** **mildly positive in aggregate, strongly positive for the migrant and for native consumers/employers, negative on the first-gen state-local fiscal book and for competing low-skill native workers.** Costs are **concentrated** (low-skill natives, local taxpayers); benefits are **diffuse** (consumers, employers, the migrants themselves). That asymmetry — not a hidden aggregate negative — is why it *feels* negative to anyone standing in the cost. *(This is the steel-manned restrictionist position: G-LIF-S\*; it is a distributional and fiscal-incidence argument, not an aggregate-welfare one.)*

## Why "less educated than the average American → bad" is a category error

It chains three different ledgers and trips one fallacy *(G-LIF-T01)*: **output is additive, not averaged.** Adding a $35k worker to a $70k-mean economy lowers the *mean* while *raising total output* and making no incumbent mechanically poorer. The national average is a summary statistic, not a welfare target. The legitimate residue of the intuition is real and lives in exactly two cells above — first-gen state-local fiscal (−) and the distributional wage hit to low-skill natives (−) — **not** in an aggregate loss.

## Generator-bank structure (the lenses that populate this map)

`lifetime_generators` (122 lenses, 22 clusters A–V, in `immigration_lifetime_evidence.duckdb` + the unified release). Each is a reusable audit that surfaces an omitted ledger or unnamed assumption:

- **Cost / incidence side (A–S, 104):** NPV accounting (A), labor market (B), local capacity (C), composition/descendants (D), housing (E), high-skill (F), legal status (G), … and the 14-lens restrictionist steelman (S). These are the SHORT-to-MEDIUM-run, first-generation fiscal lenses.
- **Benefit side (T, 8 — added 2026-06-23):** the mirror of S — `T01` additive-output, `T02` place premium, `T03` consumer surplus, `T04` entrepreneurship, `T05` PAYG solvency, `T06` GE capital adjustment, `T07` positive selection, `T08` fiscal-externality-≠-exclusion. **Its 6 external papers were acquired to the corpus 2026-06-24** (Place Premium, Cortés, AJKM, Ottaviano-Peri, Chiswick, + Abramitzky-Boustan mobility anchor) — see `immigration-acquisition-gaps-2026-06-24.md`; cluster T is no longer a placeholder list.
- **Meta (U, 2):** `U_source_incentive_meta` — source-incentive grading lenses (not a cost/benefit axis).
- **Long-run skeptical side (V, 8 — added 2026-06-24):** `V_deep_roots_long_run_skeptic` — the LONG-RUN complement to S's short-run cost. The deepest skeptical channel no first-gen ledger sees: partial transmission of origin culture/trust/institutions/human-capital across generations. `V01` deep-roots/ancestry-adjusted development, `V02` cultural transmission (epidemiological), `V03` inherited trust, `V04` ethnic-capital/slow-assimilation, `V05` the new-economic-case-for-restrictions (institutional-quality externality), `V06` national cognitive capital (**CONTESTED — stress-test only; Lynn-Vanhanen data poor; routes to the IQ sister repo**), `V07` ancestral-distance diffusion barrier, `V08` **self-rebuttal: assimilation null** (carries its own disconfirmation). All 6 external papers acquired to corpus 2026-06-24; the V08 crime-null is verified against the in-repo Texas data (undocumented 0.41–0.48× native-born, no trend to parity).

## Empirically-failed predictions (2026-06-25 — the falsifier run)

Running the generator banks' own `duckdb_test`s (`immigration-theory-verdicts-2026-06-25.md`) **falsified three** of our predictions — live caveats on this map:
- **The annual federal proxy and the lifetime NPV have OPPOSITE signs** (M13): Mexico annual federal net **+$1,519** vs NAS <HS lifetime NPV **−$109k**. This is the "coordinate-switching" warning, now empirically proven — never read one ledger's sign as the other's.
- **Return migration is NOT fiscal-neutral** (I8): a base-case 25% early-exit cuts effective <HS person-years by ~25%, so any lifetime-NPV *stock* that ignores exit is over-counted. The <HS dynasty rows above should carry an exit discount.
- **High-skill positive NPV is not mechanism-decomposed** (F5): the +college NPV stands without the innovation-spillover conditioning the theory says drives it — treat the positive sign as observed-but-unexplained, not as evidence the spillover mechanism is doing the work.

## Honest residual

The *reasoning* now spans three poles — **S (short-run fiscal cost) ↔ T (benefit) ↔ V (long-run cultural/institutional skeptic)** — and the *evidence base* for T and V is acquired (12 papers, 2026-06-24), closing the asymmetry that previously made the bank cost-heavy. What remains is **build-out, not acquisition** — and the first slice is now built: **V04/V08's first-generation decay is measured** (`immigrant_assimilation_profile`, synthetic cohorts — the Mexican income gap to natives halves over ~30 years in the US, employment gap closes by 15–25 years; strong convergence, evidence against fixed-trait persistence). Still open: V02's true **cross-generational** 2nd-gen test needs an IPUMS-**CPS** extract (parental birthplace — IPUMS-USA dropped it after 1970, the current 44M-row extract lacks it; gated); V01 wants an ancestry-index merge; V05 wants a state institutional-quality panel; V06 routes through `~/Projects/iq-sex-differences`. The benefit-side T03 still wants a local service-price index. See `immigration-acquisition-gaps-2026-06-24.md` for the full acquisition state and `immigration-net-negative-dataset-frontier-2026-06-15.md` (the cost frontier) for the original shape.

</details>
