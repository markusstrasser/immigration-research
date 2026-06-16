Reviewed the packet as embedded (no file/tool access; line numbers refer to the packet text). The material is already heavily self-corrected via the running-fixes ledger, so I audited the **current live text** for statistical/econometric/causal overclaims that survive. Six confirmed.

## (1) Confirmed findings

**C1 — Nonsignificant employment decline reported as a real effect (asymmetric significance standard).**
`research/immigration-causal-everify-card-vs-borjas.md:11,80,87,110,111`; `CYCLE.md:29`
The E1-exposed employment estimate is β=−6.11%, **t=−1.40, p≈0.16** (line 80, 87) — not distinguishable from zero at conventional levels. Yet it is stated as fact ("stable W-2 employment … fell ~6%", line 11; "shows a ~6% drop", CYCLE:29) and carries the central mechanism inference ("QWI employment ↓ but wages flat = the large native wage-bidding channel is not observed", line 111). Meanwhile the equally-nonsignificant *wage* coefficient (t=0.63) is correctly reported as "no statistically significant effect." Same evidentiary situation, opposite verbal treatment.
*Why it matters:* the "employment fell but wages didn't rise" conclusion — the file's main result — rests on an employment estimate the data cannot distinguish from zero.
*Fix:* report −6% as a nonsignificant point estimate (t=−1.40); make the combined inference conditional, or anchor the employment claim on the external Bohn-Lofstrom-Raphael Arizona estimate (line 87) rather than on this coefficient. Apply the null-handling language symmetrically.

**C2 — The Borjas counterfactual (+5–15%) is asserted, not scaled to the estimated supply shock.**
`research/immigration-causal-everify-card-vs-borjas.md:9,50,122`
The memo tests against "a wage rise on the order of 5–15%" (line 50, 122). But Borjas's own elasticity, cited in the same file (line 104: 10% supply rise → 3–4% wage fall, i.e. ~0.3–0.4), applied to the estimated shock (≈6% E1 employment, line 80) implies a predicted native wage gain of only **~1.8–2.4%** — essentially the +2.1% upper CI bound (line 50). The +5–15% figure is a mass-removal-scale prediction applied to a marginal-enforcement-scale shock.
*Why it matters:* "the Borjas prediction is rejected" (line 9) is then a rejection of a magnitude Borjas would not predict for a shock this size. A correctly-scaled Borjas effect (~2%) sits at the edge of the CI and is *not* cleanly rejected — especially since the true supply contraction is likely smaller than 6% (unauthorized are a subset of E1; cash-economy substitution, line 130). The informative content of the rejection is much thinner than stated.
*Fix:* derive the benchmark as (estimated supply contraction × 0.3–0.4) and state the magnitude actually being rejected; note that smaller shocks are not excluded.

**C3 — Nine treated clusters: cluster-robust CIs likely too narrow for the rejection claim.**
`research/immigration-causal-everify-card-vs-borjas.md:5,26,50,122`
Inference uses Liang-Zeger clustered SEs (line 26) with only **9 treated states** (line 5). With few treated clusters, CR1 SEs are downward-biased and over-reject; the "95% CI excludes anything above +2.1%" / "reject Borjas" claims depend on precisely the narrow upper bound that few-treated-cluster correction would widen.
*Why it matters:* the *null* wage finding is robust (larger true SEs only reinforce fail-to-reject), but the *rejection* of Borjas is exactly the claim this inflation undercuts. The file addresses TWFE heterogeneity bias (Sun-Abraham/Goodman-Bacon, line 124) but not few-treated-cluster inference.
*Fix:* report wild-cluster-bootstrap or Conley-Taber CIs; treat +2.1% as tentative and soften "reject."

**C4 — "Cleaner predictor" ranking built on noise-level adj-R² differences.**
`research/immigration-capacity-frontier-2026-04-21.md:56,104-110,148-149,240`
Claim 3 (HIGH/VERIFIED, line 56) says wage growth "loads more cleanly on load-capacity than on stock or flow," from adj-R² **0.154 vs 0.147 vs 0.144** (lines 108–110) — a 0.007–0.010 spread among collinear constructs. Same for native sorting ("load_only has the best adjusted R²", line 148). These differences are within sampling noise.
*Why it matters:* the memo's headline reframe ("flow+capacity is where the traction is", line 240) partly rests on these sub-0.01 gaps. (The *politics* ranking, 0.415 vs 0.345, line 89–91, is genuinely separated and is fine.)
*Fix:* state that Δadj-R² is noise-level and the predictors are collinear; rank only where gaps are material, or use a formal non-nested/encompassing test.

**C5 — The load ratio puts permit issuance in its denominator — a probable confound for the very outcomes it "wins" on.**
`research/immigration-capacity-frontier-2026-04-21.md:36,40-43,104-135,240`
`load = recent immigrant persons / (permits/4 × 2.5)` (lines 36, 40–43). Low-permit counties get high load. But low permit issuance co-moves with weaker wage growth, weaker employment growth, and net out-migration for reasons unrelated to immigrant absorption (permits proxy local economic vitality). So load's apparent edge on wages/employment/native-migration (lines 104–135) may be **mechanical**, not informative about absorption capacity.
*Why it matters:* this is a problem even for the *descriptive* "most informative variable" claim (not just the causal reading the memo already disclaims). It offers an immigration-free explanation for why load "predicts" these three outcomes.
*Fix:* control for permit level directly (outside the ratio) and show load adds signal beyond a permits-only model before calling it "the cleaner stress object."

**C6 — Threshold grid: selective significance from a multi-cell search; "q90 weaker" is likely a power artifact.**
`research/immigration-capacity-frontier-2026-04-21.md:11,58,168-198`
The grid scans q70/q80/q90 × q25/q50 across wages, politics, and employment, reports the significant cells, then concludes the threshold is "the broad high-flow tail (q70–q80), not the extreme top-decile" (claim 5, line 58; lines 188–198). Selecting significant cells from many interaction tests is a multiple-comparison search, and the q90 tail contains far fewer counties (lower power), so "weaker and less stable" (line 188) need not mean a weaker effect.
*Why it matters:* the substantive "broad-tail, not extreme" reading may be a power gradient, not a real plateau.
*Fix:* report the number of cells tested and q90 cell counts; adjust for multiplicity; distinguish "weaker effect" from "less power."

## (2) Speculative concerns

- **S1 — Inflow/outflow pooling.** `…synthesis-2026-04-18.md:21-25` calls Card 1990, Foged-Peri (immigrant *inflow*) and E-Verify (enforcement-induced *outflow*) "three converging pieces" on the wage channel. Convergence assumes wage-response symmetry between inflow and supply contraction, which is asserted, not tested. (Mechanism-pooling is partly handled by the running fixes.)
- **S2 — Surge-regression collinearity.** `…surge-2021-2024.md:113-118`: `fb_share`, `recent_fb_annual_share`, `receiver_city` are mutually correlated; the negative `recent_fb` coefficient beside positive `fb_share`/`receiver_city` is a textbook collinearity sign pattern. Mechanism is correctly left unresolved (line 115), but the coefficient signs shouldn't be read individually.
- **S3 — Small-N correlations.** Receiver-node `corr≈0.93` vs `0.32` (`…capacity-frontier:60,225`) on n≈5–16 has wide CIs; the 0.93-vs-0.32 contrast may not be statistically distinguishable. Labeled MEDIUM/descriptive, so low-stakes.
- **S4 — Compliance scaling tension.** `…everify:128` notes that under ~50% compliance the MDE rises to 4–6%, which would reject only the *high end* of 5–15% — mild tension with the unqualified "rejected" at line 9. Interacts with C2.
- **S5 — Mass-deportation per-worker loss.** First-order $207K/removed worker (ladder entry 24) exceeds average US GDP-per-worker, high for a predominantly low-wage group; an I-O Type-I multiplier artifact. Labeled calibration, so minor.

## (3) No-action notes (checked, sound)

- **Arithmetic spot-checks pass:** race correction 50%→30% (613/1221, 626/891, crime:169-178); mass-dep $207K/$332K and the 1.6× multiplier; CHNV −57.5/−95.3/−96.2% (surge:39-44); E4 +4.13% (everify:85); CI upper +2.1% (everify:50, modulo C3's dof point).
- **ICE docket denominator** error correctly removed — now refuses the unauthorized-stock per-capita comparison (crime:124).
- **Ratio-of-medians (21.7×) vs median-of-ratios (20.5×)** correctly distinguished (ladder entry 22; surge:148) — good hygiene.
- **Wage null** stated as "no statistically significant positive effect," explicitly not an equivalence-tested zero (running fixes); robust to C3.
- **12-spec null + one significant E4 aggregate** (t=2.19) correctly dismissed as skill-upgrading, not causal (everify:89).
- **CHNV reversal** internally coherent: USBP↓ + OFO↑ + null total-CBP DiD (β=+0.45, t=1.29) → "substitution, not reduction" (surge:36-53).
- **Confidence-ladder append-only supersession** (entries 26/30 marked invalidated by 34) is sound provenance.
- **Crime directional finding** scoped to "observed justice-system rates," with residual confounds (age/sex/geography) named after the within-race correction (crime:178).

The two findings I'd prioritize for the executor: **C1** (asymmetric significance standard — cleanest and most consequential) and **C2** (un-scaled Borjas benchmark — reframes how much the "reject Borjas" headline can actually claim). Both are demonstrable from the packet's own numbers.
