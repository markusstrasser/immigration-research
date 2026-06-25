# Red-Team of Our Own Synthesis — cross-model adversarial review

**Date:** 2026-06-25
**Method:** The conviction memo (`immigration-interpreted-insights-2026-06-24.md`), the ledger-map, and the confidence ladder were sent to **two non-Claude frontier models** (GPT-5.5 high, Gemini-3.5-flash) with an adversarial brief: find where this synthesis is overstated, tilted (either direction), or missing counter-evidence. Two different labs = genuine cross-lab pressure (Claude self-review would be same-family and is excluded). Raw outputs in scratchpad; this is the adjudication — **cosign / partial / reject, not wholesale adoption** (the models hallucinate too; every quote below was verified to exist in our docs first).

## Convergent findings (BOTH models flagged → highest confidence)

| # | Finding | Adjudication | Action |
|---|---|---|---|
| 1 | **2nd-gen crime convictionscore 0.88 is too high** — both note the memo itself admits the evidence is "broad generational literature, not unauthorized-specific or current-cohort." | **ACCEPT.** A node the memo calls "the weakest crime node" should not carry 0.88. | Downgraded to 0.65 with the scope spelled out. |
| 2 | **Federal "RAISED revenues and CUT the deficit" (0.95) is overstated** — GPT: it's a CBO *projection*, not an observed result; Gemini: CBO's baseline freezes downstream discretionary spending, inflating the "reduction" as an accounting artifact. | **ACCEPT.** The figures are verbatim-correct but the framing reads as observed fact and omits the baseline caveat. | Reframed to "CBO *projects*"; added the discretionary-baseline caveat. |
| 3 | **"Direction is bulletproof"** (crime) is advocacy language given the memo's own TX/race/detection caveats. | **ACCEPT.** | Softened to "robust across independent datasets." |
| 4 | **Enforcement "null-to-HARMFUL" is one-sided** — both note it isolates the reporting-suppression mechanism and omits the incapacitation/deterrence channel (deportation removes active offenders). | **ACCEPT.** A genuine omission, not just tone. | Added the incapacitation counter-mechanism; reframed as a trade-off. |
| 5 | **"Category error" framing of mean-vs-total is a value judgment dressed as math** — if a polity values per-capita public-service funding or cohesion, the per-capita mean *is* a legitimate target. | **PARTIAL.** The additive-output point is correct (a falling mean with rising total is not mechanically a loss), but the framing over-claims. The ledger-map already concedes "the legitimate residue lives in two cells." | Sharpened the concession; kept the additive-output logic. |
| 6 | **TX/Mexican-heavy crime data doesn't generalize to the 2021–26 surge cohort** (newly-arrived, shelter-bound, unstable-origin) — both. | **ACCEPT.** Already caveated but the headline should carry it harder. | Folded into the 2nd-gen downgrade + a surge-cohort caveat. |

## Single-model findings worth keeping

- **Gemini — asymmetric think-tank skepticism:** Heritage/FAIR deflated to 0.28 as "advocacy" while the equally-contested Clemens +$128k capital-tax flip rides at ~0.8. **PARTIAL-ACCEPT:** the memo *does* already disclose Clemens's with-interest discount (0.8, not 0.95), "no peer-reviewed rebuttal," and the AEI rebuttal that still finds ≤HS net-negative — so it's more balanced than the critique implies. But the *language* ("defensible" vs "advocacy") is asymmetric. Sharpened to treat both as contested endpoints of the same assumption-sensitivity fan. This is the instrument-tilt the operator flagged ("they're all woke"), caught in our own work — the most important catch.
- **Gemini — mass-deportation $1.45T is a static Leontief caricature** (freezes capital/automation/wage response). **ACCEPT as already-labeled:** the memo tags it "first-order / partial-equilibrium / Type-II is sensitivity only" — the caveat is present; no change, but noted.
- **GPT — "mildly positive in aggregate" outruns the integrated evidence:** no same-universe model was built that nets federal + state-local + housing + congestion + wage incidence for the actual low-skill cohort. **ACCEPT.** This is the honest ceiling of the whole stack and is now stated as such in the ledger-map residual.
- **Gemini — CHNV "substitution" term overstretched** (channel diversion ≠ same individuals; parolees still need local resources). **ACCEPT as caveat.**

## Missing entirely (both models) — the real gaps

Housing/rent incidence on low-skill natives (under-integrated); **ESL + emergency-Medicaid** state-local costs (omitted from the SIPP cash-flow proxy); per-capita vs aggregate native welfare; **brain-drain externality on sending countries** (the place-premium ledger counts only the gain); NCVS-style **victimization** data (detected crime ≠ crime); political-economy/institutional externalities (the V-cluster reasoning exists but isn't built into data).

## Net

The red-team did **not** overturn the headline — it tightened it. The honest synthesis after this pass: *best current evidence shows first-generation immigrants (incl. unauthorized) do not have higher detected crime than natives, and CBO projects the recent surge improves federal finances while imposing concentrated state-local and low-skill-native costs; net welfare depends on horizon and welfare weights, and no single same-population model has been built.* The most valuable catch was the **asymmetric-skepticism tilt** — confirming the instrument bias is real and lands in our own confidence scores, not just in the sources.
