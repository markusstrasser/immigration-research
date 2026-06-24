# Full-Spectrum Costs of Unauthorized Immigration — Bounded Scoring Model

**Question:** How should we score long-run cost channels without presupposing a conclusion or laundering weak claims into a single giant number?
**Date:** 2026-03-13
**Inputs:** [immigration-full-spectrum-costs-unauthorized-memo.md](/Users/alien/Projects/research/research/immigration-full-spectrum-costs-unauthorized-memo.md), [immigration-fiscal-impact-unauthorized-memo.md](/Users/alien/Projects/research/research/immigration-fiscal-impact-unauthorized-memo.md), CBO, ITEP, language-access reports, labor-enforcement reports, and political-economy literature.

---

## Purpose

This is a **neutral inclusion model**, not an answer. Its job is to prevent three common failures:

1. treating every plausible mechanism as if it were equally real,
2. monetizing weakly identified channels just because they feel important,
3. smuggling one-sided assumptions into a "full-spectrum" total.

The model scores channels on five axes and assigns them to one of three buckets:

- **Core bound**: safe to include in a bounded estimate.
- **Sensitivity band**: real enough to matter, but too weak for a single central estimate.
- **Narrative only**: discuss qualitatively unless better measurement appears.

---

## Scoring Rubric

Each channel gets five scores:

| Axis | Score | Meaning |
|---|---|---|
| Evidence (`E`) | 0-3 | 0 = mostly rhetoric, 3 = direct measurement or strong causal evidence |
| Attribution (`A`) | 0-3 | 0 = not specific to unauthorized immigration, 3 = closely tied |
| Monetizability (`M`) | 0-3 | 0 = no credible dollarization, 3 = already in budget or directly priceable |
| Persistence (`P`) | 0-3 | 0 = temporary, 3 = plausibly long-run / intergenerational |
| Double-count risk (`D`) | 0-3 | 0 = cleanly separable, 3 = easy to count twice |

**Composite score:** `E + A + M + P - D`

Action thresholds:

- **Core bound**: `7+` and no fatal attribution problem
- **Sensitivity band**: `4-6`
- **Narrative only**: `0-3`

This is deliberately conservative. A channel can be real and still stay out of the core bound if its attribution or monetization is weak.

---

## Channel Table

| Channel | Sign | E | A | M | P | D | Score | Bucket | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| State/local education, shelter, border response, incarceration, general services | Negative | 3 | 2 | 3 | 2 | 1 | 9 | Core bound | CBO directly measures direct and potential effects for the post-2021 surge. [SOURCE: https://www.cbo.gov/publication/61256] |
| Federal tax revenue and macro budget effects | Positive offset | 3 | 2 | 3 | 2 | 1 | 9 | Core bound | A full-spectrum account that omits this is one-sided. [SOURCE: https://www.cbo.gov/publication/60569] |
| Public-service crowding not fully booked as spending | Negative | 2 | 1 | 2 | 2 | 2 | 5 | Sensitivity band | CBO explicitly recognizes nonbudgetary crowding, but national per-person pricing is weak. [SOURCE: https://www.cbo.gov/publication/61256] |
| Language access and interpreter systems | Negative | 2 | 1 | 2 | 2 | 1 | 6 | Sensitivity band | Real overhead, but observed for LEP populations, not unauthorized immigrants specifically. [SOURCE: https://languageaccess.courts.ca.gov/system/files/2025-07/2025%20Language%20Need%20and%20Interpreter%20Use%20Study.pdf] [SOURCE: https://www.courts.wa.gov/content/Financial%20Services/documents/2025_2027/Biennial/BD%20Stabilize%20Interpreter%20Reimbursement%20Program.pdf] |
| Immigration court backlog and due-process friction | Negative | 2 | 2 | 2 | 2 | 1 | 7 | Core bound, if scoped to immigration-adjudication systems | Real system cost, but avoid importing the whole backlog as "cost of one migrant." [SOURCE: https://trac.syr.edu/immigration/reports/637/] [SOURCE: https://trac.syr.edu/immigration/reports/558/] |
| Health-system distortion via delayed care / ED substitution | Mixed-negative | 2 | 1 | 1 | 2 | 2 | 4 | Sensitivity band | Real channel, but overall immigrant health spending is lower than natives; do not price as a giant burden by default. [SOURCE: https://hia.berkeley.edu/wp-content/uploads/2014/03/2005_healthcare_exp.pdf] [SOURCE: https://scholars.duke.edu/publication/1476491] |
| Housing overcrowding, code enforcement, shelter spillover | Negative | 1 | 1 | 1 | 2 | 2 | 3 | Narrative only / local sensitivity | Likely real locally; weak status-specific attribution nationally. [SOURCE: https://www.cbo.gov/publication/61256] [SOURCE: https://www.montgomerycountymd.gov/OLO/Resources/Files/2025_reports/OLOReport2025-6.pdf] |
| Informal labor, wage theft, misclassification, payroll tax erosion | Negative | 2 | 1 | 2 | 3 | 2 | 6 | Sensitivity band | Strong mechanism, weak per-person attribution. Best handled as a separate employer-side distortion module. [SOURCE: https://www.umass.edu/labor/research/working-paper-series/social-and-economic-costs-illegal-misclassification-wage-theft-and-tax-fraud-residential/4-path-citizenship-immigrant-workers] [SOURCE: https://clje.law.harvard.edu/app/uploads/2019/06/misclassification_and_payroll_fraud.pdf] |
| Native wage displacement / tax-base effects | Mixed | 1 | 1 | 1 | 2 | 2 | 3 | Narrative only | Empirically unresolved; sign depends on methodology. [SOURCE: `research/immigration-fiscal-impact-unauthorized-memo.md`] |
| Redistribution backlash / policy churn | Negative | 2 | 0 | 0 | 3 | 2 | 3 | Narrative only | Real aggregate effect, but not credibly dollarized per immigrant. [SOURCE: https://www.hbs.edu/ris/download.aspx?name=Alesina+and+Tabellini_May2022.pdf] [SOURCE: https://economics.uci.edu/files/docs/micro/s11/Edmark.pdf] |
| Generalized trust / cohesion | Mixed / contested | 1 | 0 | 0 | 3 | 3 | 1 | Narrative only | Most vulnerable to framing bias and overclaiming. [SOURCE: https://www.ias.edu/sites/default/files/sss/BordersPortes-Diversity-Social-Capital.pdf] |
| Child costs without child lifetime contributions | Negative in short run, positive/mixed in long run | 2 | 2 | 2 | 3 | 2 | 7 | Core bound only if both sides are modeled | One-sided treatment of children is the single biggest distortion risk in fiscal accounting. [SOURCE: `research/immigration-fiscal-impact-unauthorized-memo.md`] |

---

## Inclusion Protocol

### Core bound

Include these in any bounded estimate:

- measured state/local service costs,
- measured or strongly inferred tax/revenue offsets,
- child-related channels only if both costs and later contributions are explicitly handled,
- immigration-adjudication system costs if scoped narrowly and not spread across unrelated court burdens.

### Sensitivity band

Add one at a time, not all at maximum:

- nonbudgetary crowding,
- language access,
- health-system substitution costs,
- informal-labor / tax-erosion channels.

These are the right place to widen the negative tail without pretending they are settled.

### Narrative only

Do not assign headline dollars absent new evidence:

- generalized trust / cohesion,
- redistribution backlash,
- broad housing-market and neighborhood effects without local causal identification,
- unresolved native wage effects.

They may matter, but the current state of evidence does not justify a clean NPV term.

---

## Neutral Use Cases

### If you want a cautious central estimate

Use only the **Core bound** channels and show both negative and positive components.

### If you want a pessimistic but still defensible estimate

Start with the core bound, then add **one or two Sensitivity band** modules with explicit caveats and no double counting.

### If you want a "worst case"

You can stack narrative channels too, but then it is a **scenario**, not an estimate. Label it that way.

---

## Anti-Bias Rules

1. **No pure-cost stack without offsets.** Federal revenues, macro gains, and child lifecycle contributions cannot be omitted merely because they are inconvenient.
2. **No cohesion arithmetic without mechanism.** If a claim cannot be decomposed into schools, courts, policing, housing, public-goods support, or compliance systems, keep it qualitative.
3. **No household-person unit switching.** Household and per-person estimates are not interchangeable.
4. **No gross-spending as net-cost substitution.** Spending lines and net-balance lines are different objects.
5. **No double counting across ledgers.** Budget outlays, queues, and downstream political effects are linked, not independent.

---

## Best Current Use

This model is best used as a gatekeeper before anyone tries to produce a headline NPV.

It does not tell you the answer. It tells you which channels deserve numeric inclusion, which belong in sensitivity analysis, and which should remain narrative unless better evidence arrives.
