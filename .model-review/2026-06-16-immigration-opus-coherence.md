## Reviewer C — internal-consistency / overclaim audit

Scope reminder: I checked the packet for (a) internal contradiction, (b) strength-of-conclusion exceeding the cited evidence, (c) unresolved uncertainty collapsed into a verdict. Findings are split into **Confirmed** (a demonstrable statistical/logical defect, sourced to the packet's own numbers) and **Optional** (scoping/consistency refinements, not style). One caveat up front: I cannot query the live DuckDB views, so where a finding rests on the warehouse I reason only from the arithmetic the packet itself prints.

---

## CONFIRMED

### C1 — The school-burden "correction" re-commits a denominator-universe mismatch and may invert its own headline sign *(highest severity; propagated widely)*

This is the load-bearing fix of the whole audit (the +$748/adult "Mexico federal-minus-school is positive" result), and the packet's own reconstruction shows the numerator and denominator come from different universes.

Evidence, all in `research/immigration-conclusion-audit-running-fixes.md`:
- Line 35 (scenario source table) labels the school inputs as **scenario-subset**: Mexico `scenario adults 436819`, `area-wtd per pupil 20907.09`, `school-age kids/HH 0.9718`, `HH weight 322540`.
- Line 39 derives the corrected school burden as `20907.09 * 0.9718 * 322540 / 8496334 = ~$771/adult`, and this reproduces the live view's `school_per_adult 771.285` (line 29) to 4 sig figs — so this *is* the computation, not an illustration.

The defect: the numerator `20907.09 × 0.9718 × 322540 ≈ $6.55B` is total school dollars for the **scenario subset's 322,540 households** (which contain ~436,819 adults). It is then divided by the **full-stock 8,496,334 adults**. Those are different populations. Spreading 322,540 households' school cost over 8.5M adults implies 26 adults/household — impossible — so the $771 is a scenario-scale numerator over a full-stock denominator.

Critically, the **federal layer was scaled to full stock but the school layer was not**:
- Federal: scenario subset $664M (436,819 × $1,519.28) → correctly rescaled to full-stock **$12.9B**/8.496M = $1,519/adult (lines 98, 137). ✔ consistent.
- School: scenario subset $6.55B → **not** rescaled; divided by full-stock adults → $771/adult. �’ mismatched.

A consistent full-stock school numerator (scaling 322,540 → the full Mexico-origin household count, ≈19.45× = 8,496,334/436,819) is ≈$127B, i.e. **~$15,000/adult**, giving net ≈ $1,519 − $15,000 = **−$13.5k** — which is exactly the "stale, wrong" number the correction claimed to kill (line 13/37: original −$13.5k = $1,519 − $15,002). In other words, the only thing that changed between the "wrong −$13.5k" and the "corrected +$748" is the **denominator** (436,819 → 8,496,334); the numerator stayed scenario-scale. Moving one side's universe and not the other is not a fix — it is the mirror-image of the original bug.

Internal red flag confirming this, line 204: Mexico-origin school burden `$771.29/adult` vs NH-white-US-born `$6,023.53/adult`. A younger, more child-heavy population showing **one-eighth** the per-adult K-12 burden of native whites is facially implausible and is the visible tell of the ~19× understatement. The "Remaining Risk" note (lines 67–68) gestures at this as a *cohort* issue ("may understate school incidence for … child-heavy subgroups") — but it is not a cohort nuance, it is a numerator/denominator universe error.

Why it matters beyond one row: the +$748 figure is propagated as a settled "current conclusion" at lines 62, 170, 180, and is the basis for the symmetry fix at line 922 ("Mexico-origin is +$748/adult and NH-white US-born is −$3,277/adult … Neither row is a welfare verdict"). The symmetry framing actively papers over the defect, because the two rows are not computed on the same footing if Mexico's school numerator is scenario-scale and the native row's is full-stock-scale.

Fix (not optional): recompute `school_per_adult` for Mexico-origin (and verify every group) with a **full-stock household/school-age-children numerator** over the full-stock adult denominator, *or* compute the whole `v_three_layer_annual` row on the scenario universe (federal included). Until then, the "+$748 federal-minus-school positive" headline and every downstream memo citing it should be marked **suspect / under recomputation**, not "corrected." Recommend an explicit invariant check: `school_total_dollars` and `adult_denominator` must reference the same population key.

### C2 — Statistical-significance discipline is applied to the wage null but not to the parallel employment estimate

The audit spent dozens of entries converting "wages did not rise" → "no statistically significant positive effect" (e.g. running-fixes lines 1846–1862, 2006–2022). The **employment** estimate of equal insignificance was never given the same treatment, and the central E-Verify interpretation leans on it.

- `research/immigration-causal-everify-card-vs-borjas.md:11` — "employment … **fell ~6%** post-treatment (t=−1.40, marginal). Combined picture: QWI **employment fell** but no statistically significant positive wage effect was observed." t=−1.40 is p≈0.16 — not significant — yet "fell" is asserted flatly while the wage side is carefully hedged.
- `:87` "**did fall** … (marginal, p≈0.16)"; `:110` "Stable W-2 employment … **did fall**"; `:111` "QWI employment ↓ but wages flat = the large native wage-bidding channel is not observed."
- `CYCLE.md:29` states it as a discovery: "E-Verify mandates **show a ~6% drop** in stable E1 W-2 employment."
- `research/immigration-confidence-ladder.md:120` then uses it as a "weak plausibility check" for the mass-deportation calibration.

The logical problem: the headline interpretive contrast — "employment margin moved, wage margin didn't, therefore Card-style adjustment" — requires one of the two effects to be real. Within this design, **neither** the wage point estimates nor the employment estimate is statistically distinguishable from zero, so the contrast as stated is an asymmetric-significance artifact. (The Borjas-rejection itself is fine — it rests on the wage 95% CI excluding ≥5%, line 50 — and is unaffected.)

Fix: render the employment estimate with the same discipline wherever it is stated as a conclusion — e.g. "a non-significant ~6% point estimate (t=−1.40, p≈0.16)" — and rest the "employment fell" claim on the external corroboration that actually supports it (Bohn-Lofstrom-Raphael 2014, line 87), not on this design's coefficient. Revise the "Combined picture" sentence (`:11`) and `CYCLE.md:29` accordingly.

### C3 — Receiver-city coefficient: the main-table value and the kill-test "before" value disagree

`research/immigration-causal-surge-2021-2024.md`:
- Line 113 specifies the multivariate model **without** a Hispanic-share term; line 116 reports `receiver_city: +0.024 (t=6.96***)`.
- Line 130 (and the bottom line, line 18) states the **without**-Hispanic-control coefficient is `+0.0256` and the **with**-control coefficient is `+0.0238`.
- Confidence ladder echoes both: entry 28 (`immigration-confidence-ladder.md:138`) gives the no-control multivariate β `+0.024`; entry 36 (`:174`) gives `+0.0256 → +0.0238`.

The line-116 regression contains no Hispanic control, so its `+0.024` should equal the kill-test's pre-control `+0.0256`, not the post-control `+0.0238`. As printed, the headline "+2.4pp **after** Hispanic-share control" (`surge:200`) is numerically the same as the main table's **uncontrolled** coefficient — which masks that the base regression never included the control. Either the two runs use different samples (e.g., the kill-test drops counties lacking the popest baseline) and the memo should say so and print each N, or one label is wrong. Right now a reader cannot tell whether the controlled estimate is +0.0238 or +0.024, nor whether the main table is controlled.

Fix: reconcile — print N for each run, label line-116 explicitly as the no-Hispanic-share spec, and state why its `+0.024` differs from the kill-test's `+0.0256` pre-control value (or correct the typo).

### C4 — Crime memo bottom line still asserts the Lott "error" that the audit downgraded to an unverified critique

`research/immigration-crime-rates-unauthorized-vs-native-born.md:13` (bottom line): "Lott 2018 … **has been criticized for a fundamental data classification error**." The phrasing presupposes the error exists.

This contradicts the corrected posture elsewhere in the same memo and the audit's stated intent:
- `:114` "**seriously challenged**"; `:207` claims-table row downgraded to "`SUPPORTED CRITIQUE — not independent reanalysis`."
- running-fixes lines 1366–1382: explicitly changed "shown to be unreliable" → "seriously challenged" because "multiple independent critiques … are not the same thing as an independent verification of the underlying classification error."

The bottom line is the most-quoted surface and still encodes the stronger claim the audit retracted. Fix: align `:13` to the table — "faces a serious, unresolved data-classification critique" — rather than asserting the error as established.

---

## OPTIONAL (substantive scoping/consistency, not style)

- **O1 — `everify:9` overstates the rejected Borjas range.** Line 9 says the "~5–15% rise … is rejected"; but line 122 ("cannot reject small sub-2% effects") plus line 128 (50% compliance doubles MDE to 4–6%) imply the **low** end (~5%) sits near the compliance-adjusted detection bound. Lines 128 and 138 already retreat to "high-end Borjas." Recommend `:9` say "rejects the mid-to-high Borjas range" for consistency with the memo's own power caveat.

- **O2 — Foged-Peri characterized two ways inside one memo.** `everify:98` calls it "see **no wage loss**" (a null); `everify:163` table and `synthesis:25` call it "native low-skill wages **↑**" (a positive gain, "Anti-Borjas"). Null and positive are different results. Pick one (the paper's finding is a positive effect) so the evidence isn't softened in one place and sharpened in another.

- **O3 — `synthesis:21` labels a Danish study as U.S. evidence.** "Three converging pieces of evidence **on the U.S. wage channel**" lists Card (US), this cycle's E-Verify (US), and **Foged-Peri (Denmark)**. This re-inflates the within-scope evidence count — the same move the audit guards against elsewhere (running-fixes 1186–1202, where GPT calibration was removed from the wage stack). Re-label as "one U.S. policy-margin test read alongside external (incl. Danish) literature."

- **O4 — `capacity-frontier:16` presupposes a causal channel it later disclaims.** Bottom line says "**the native exit channel** is not just ideology or partisan response," but line 159 says "whether incumbents sort away because of that load still needs counterfactual identification." Calling it "the native exit channel" hard-codes the causal reading the body withholds. Reword to "the native-migration association is not explained by partisanship alone."

---

## Could not verify (flagged, not asserted)
- Whether the live `v_three_layer_annual` view actually computes school cost as C1's arithmetic implies (the line-39 reconstruction matching line-29 to 4 sig figs is strong but not a query). **This is the one finding to confirm against the DB first — it is the highest-impact.**
- The "12 specifications" wage-null claim (`everify:9`, `CYCLE.md:28`): the table prints 6 wage rows; I cannot confirm the full 12 are all non-significant.

Net: C1 is the priority — it is an internal-consistency defect in the packet's flagship "correction" and, if the live view matches the printed arithmetic, it flips the sign of a conclusion now propagated across at least five memos. C2 is a genuine but contained methodological asymmetry. C3/C4 are small reconciliations.
