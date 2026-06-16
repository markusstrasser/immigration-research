**Reviewer B — causal / econometric / statistical lane.** Packet-only review (no tool, data, or DuckDB access this turn). I treat the printed DuckDB values as given; all arithmetic below is on the numbers as printed in the packet. Leading with confirmed findings, then preferences.

---

## CONFIRMED findings

### C1 — The "illustrative lifetime stack" mixes discount/horizon conventions and the band doesn't reconcile with its own rows
`research/immigration-mexico-npv-population-synthesis-2026-06-15.md:34,40-50`

The NAS benchmark is stated as **2012$, 3%, 75yr** (`:34`), whose annuity-immediate factor is ≈ **29.70**. But the recurring-cost rows present-value $657/yr → −$15,300 (`:46`) and $2,100/yr → −$49,000 (`:47`). Both imply factor ≈ **23.3** (15,300/657 = 23.3; 49,000/2,100 = 23.3), i.e. ~3%/40yr or ~4%/75yr — **not** the benchmark's 3%/75yr. You cannot net a ~40-yr cost stream against a 75-yr-from-age-25 benefit benchmark for the same people and sum them into a band.

Worse, the band **−$37k to +$28k** (`:48`) does not reconcile with the displayed rows under a single convention: with the printed row values (factor 23.3) and school = 0 the low end is only −$18.7k; reaching −$37k requires either ~$18k of additional annuitized school cost — which the same table marks **"unresolved"** (`:45`) and which the live view withholds — or re-pricing the flows at 29.7 (45,631 − 19,514 − 62,374 ≈ −$36k). So the pessimistic endpoint smuggles in either a withheld school layer or a second, inconsistent discount factor. This violates the repo's own unit-bridge generators (`research/immigration-lifetime-fiscal-generators.md` G-LIF-A04 `:34-41`, G-LIF-M01 `:562-568`). It survived the 2026-06-16 cleanup that updated the adjacent school row.

**Minimal fix:** Present-value all flow layers at the NAS 3%/75yr convention (→ surge −$19.5k, enforcement −$62.4k), or explicitly adopt a shorter remaining-life horizon for the current stock **and** bring the NAS benchmark to that same horizon. State the school assumption used at each band endpoint; do not print an endpoint that depends on the withheld school layer.

### C2 — Enforcement and state/local-surge layers use mismatched population universes (denominator/base-rate error)
`research/immigration-mexico-npv-population-synthesis-2026-06-15.md:46-47,33,76`

- **Enforcement:** the $2,100/yr figure is derived as total CBP/ICE ÷ **14M unauthorized** (`research/immigration-lifetime-fiscal-generators.md` G-LIF-R03 `:786`: "$29.5B / 14M ≈ $2.1k/yr"). It is then subtracted per **Mexico-origin adult** in an 8.5M *birthplace* stock that is mostly authorized (Mexico unauthorized ≈ 4.3M, `:33,76`; Mexico ≈ 30% of unauthorized, generators G-LIF-Q05 `:748`). Subtracting $2,100/adult × 8.5M implies ~$17.9B of national enforcement (60% of $29.5B) attributed to Mexico-origin adults — inconsistent with the repo's own stock figures. "Fully loaded" (`:50`) addresses fixed-vs-marginal, **not** this unauthorized-vs-birthplace denominator switch.
- **State/local surge:** $657/yr is a CBO **2021-26 surge** per-capita, applied to the **established** Mexico-origin stock (post-2021 unauthorized growth is "non-Mexico," `:33,76`; 53% of the stock is age 45-64, `:64`). This is the exact surge-cohort-vs-stock laundering the repo forbids (generators G-LIF-M05 `:594`, disconfirmation rows `:136-137`; budget-≠-per-migrant G-LIF-J01 `:438`).

**Minimal fix:** Scale enforcement to the unauthorized share of the stock (or compute a Mexico-origin-specific allocation) and tag the denominator; replace the surge per-capita with a stock-appropriate state/local figure or label that layer surge-cohort-only. Don't subtract per-unauthorized or per-surge rates from a per-all-Mexico-origin-adult NPV.

### C3 — "Cuts against large native wage gains" leans on absence-of-evidence without a reported CI or MDE
`research/immigration-knowledge-delta-agent-loop-2026-06-16.md:45-48,94,193`; `CYCLE.md:28`; running-fixes `:2422`

The conclusion states "large native wage gains are not observed" (`:45,94`) and CYCLE/running-fixes phrase it as the result "cuts against large native wage gains" (`CYCLE:28`, `rf:2422`). The repo's own significance frontier requires distinguishing "point estimate, CI, MDE" (`:193`), but the E-Verify conclusion reports **neither a confidence interval nor a minimum detectable effect**. A non-significant estimate only *cuts against* large effects if the upper CI bound actually excludes them (a precise null); otherwise it is merely underpowered (failure to detect). The memo is half-careful — it admits "small effects and scaled-shock Borjas benchmarks are not ruled out" (`:46`) — but "cuts against large gains" is the one phrase doing absence-of-evidence work.

**Minimal fix:** Report the wage-coefficient CI (or the design's MDE). Keep "cuts against large native wage gains" only if the upper bound sits below the margin-scaled Borjas benchmark; otherwise downgrade to "did not detect, and was not powered to detect, large gains." Note that in a *small* effective-shock margin neither Card nor a properly-scaled Borjas predicts large gains, so the informative content is power, not discrimination.

### C4 — Static TWFE under staggered E-Verify adoption is a *bias* risk, not just an unrun robustness check
`CYCLE.md:42,28-29,26`; `research/immigration-knowledge-delta-agent-loop-2026-06-16.md:48`

CYCLE notes "formal staggered-DiD robustness was not run" (`:42`) yet the point estimate and t-statistic are cited with precision (E1 ≈ −6%, t = −1.40, p ≈ 0.16, `:28-29`; `kd:48`). With 18 states adopting mandates at different times (queue `:26`), two-way fixed-effects uses already-treated units as controls, so the reported coefficient can be a negatively-weighted average of heterogeneous effects — the estimate and its t-stat may not be a clean ATT. The packet frames this only as a *missing* robustness check; it is also an interpretability/bias issue affecting the magnitude and sign, not only significance.

**Minimal fix:** One line stating that the static-TWFE estimate may carry heterogeneous-timing weighting bias and is not a clean ATT; flag a heterogeneity-robust estimator as the unresolved check. Keep numeric estimates labeled as design-dependent point estimates.

**Clean / correctly handled (credit, no action):** the significance-asymmetry fix is now consistent — wage non-significance and E1 employment are both treated as non-significant point estimates (`CYCLE:28-29`, `rf:2402-2422`); the capacity adjusted-R² catch (0.007–0.010 edge → "marginally best-fitting," q90 power/multiple-testing caveat, permit-denominator confounding, `rf:2446-2466`) is the right call; the crime estimand narrowing to observed justice-system rates with race-composition/aggregate-denominator caveats (`kd:66-72`, `rf:2426-2442`) is sound.

---

## Speculative / preferences

- **S1 — "+2.4pp ... upper-bound after controls"** (`rf:2561`) vs "survives the Hispanic-share kill-test at about +2.4pp" (`kd:55`). Calling a *controlled point estimate* an "upper bound" requires showing the coefficient *shrank* when the Hispanic-share control was added (Oster-style); "survives" implies it persisted, not that it fell. Either show the pre/post-control movement that licenses "upper bound" or relabel it a "controlled correlational point estimate." (Direction-of-label issue; low severity, but it's quoted in a high-reuse fix entry.)

- **S2 — receiver-node selection.** Picking Miami-Dade + NYC as "strongest survivors" out of nine nodes for multi-channel synchronization (`research/immigration-claims-evolution-ledger-2026-04-23.md:51-57`) is a selection/multiple-comparisons posture. It is already framed as case selection / hypothesis generation — keep that framing explicit and avoid letting synchronization read as confirmation.

- **S3 — retrodiction-as-quality-gate is in-sample fit.** Selecting generators because they "retrodict ≥2 prior findings" (`notes/immigration-lifetime-synthesis-diverge-cookbook.md:170`; `research/immigration-thesis-generator-audit-2026-06-16.md:42`) overfits to known results and will look better than it forecasts. The audit already prescribes "held-out retrodiction + novelty" (`:263`) — confirm that gate is the one implemented, not retrodiction alone.

- **S4 — mass-deportation calibration.** $1.5T–$2.3T ≈ 5–8% of GDP from removing 7M workers (`claims-evolution:97`) checks out against ~$29T GDP, but 7M ≈ 4.2% of employment, so a 5–8% output drop implies an output-elasticity >1 (multipliers/complementarities). Fine as a multiplier-inclusive bound; state the implied elasticity so it isn't read as a linear per-worker product.

- **Nit:** "annuitized ($657/yr)" (`mexico-npv:46-47`) describes converting a *flow to a present value*, which is capitalizing/present-valuing, not annuitizing (the reverse). Rename to avoid confusion in the unit-bridge.

**On "can the loop replace human search-space shaping" (stat-validity angle only):** the loop mechanizes denominator/estimand/significance checks well (the XDISC estimand-classifier and universe-twin gates, `thesis-generator-audit:95-96`, are exactly right), but C1–C4 are cases where automated guards that *exist as generators* (A04, M05, J01, R03, DS-01/02) did **not** fire on a live surface. Until a guard is executable and gated (not a prose prompt), the human is still doing the catching — so the honest answer is "loop assists, does not yet replace," which matches the memo's own deferral of a hook (`thesis-generator-audit:223`).
