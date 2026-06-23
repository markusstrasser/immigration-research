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
| Fiscal — lifetime NPV, <HS cell | **−** (assumption-dependent; can flip **+**) | NAS −$109k; flips to +$128k under capital-tax GE (Clemens) | A01, A02 |
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

`lifetime_generators` (112 lenses, 20 clusters A–T, in `immigration_lifetime_evidence.duckdb` + the unified release). Each is a reusable audit that surfaces an omitted ledger or unnamed assumption:

- **Cost / incidence side (A–S, 104):** NPV accounting (A), labor market (B), local capacity (C), composition/descendants (D), housing (E), high-skill (F), legal status (G), … and the 14-lens restrictionist steelman (S).
- **Benefit side (T, 8 — added 2026-06-23):** the mirror of S — `T01` additive-output, `T02` place premium, `T03` consumer surplus, `T04` entrepreneurship, `T05` PAYG solvency, `T06` GE capital adjustment, `T07` positive selection, `T08` fiscal-externality-≠-exclusion. Their `source_rel_paths` point at papers **not yet in the corpus** — so cluster T doubles as the **benefit-side acquisition list** that balances the former "net-negative dataset frontier."

## Honest residual

The *reasoning* is symmetric now (S ↔ T). The *evidence base* is not yet: the warehouse was built richer on cost-measurement (schools, local fiscal, Medicaid) than on benefit-measurement (consumer-price effects, firm formation, place premium). Closing that — acquiring the cluster-T sources — is the next move if the goal is a ledger that isn't asymmetric by construction. See `immigration-net-negative-dataset-frontier-2026-06-15.md` (the cost frontier) for the shape to mirror.
