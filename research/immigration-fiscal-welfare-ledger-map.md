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

## Honest residual

The *reasoning* now spans three poles — **S (short-run fiscal cost) ↔ T (benefit) ↔ V (long-run cultural/institutional skeptic)** — and the *evidence base* for T and V is acquired (12 papers, 2026-06-24), closing the asymmetry that previously made the bank cost-heavy. What remains is **build-out, not acquisition**: V01/V02/V04 want an ancestry/2nd-generation merge onto the IPUMS panel (parental BPL) to test the decay rate; V05 wants a state institutional-quality panel; V06 is deliberately not testable here and routes through `~/Projects/iq-sex-differences`. The benefit-side T03 still wants a local service-price index. See `immigration-acquisition-gaps-2026-06-24.md` for the full acquisition state and `immigration-net-negative-dataset-frontier-2026-06-15.md` (the cost frontier) for the original shape.
