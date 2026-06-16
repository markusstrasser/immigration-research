# Immigration causal analysis — synthesis (2026-04-18)

**Inputs from this autonomous cycle:**
1. `immigration-causal-saiz-elasticity-rent.md` — Saiz 2010 housing supply elasticity × ACS rent + foreign-born share, n=237 MSAs
2. `immigration-causal-everify-card-vs-borjas.md` — TWFE on QWI 2003-2023, 9 E-Verify states vs 42 controls, 151k observations

**Question revisited:** "On the immigration questions, can we find interpretations or datasets that would change the conclusions or something more descriptive and causal?"

## Bottom line — what the new evidence updates

| Repo claim (pre-cycle) | New evidence | Updated verdict |
|------------------------|--------------|-----------------|
| Rent exposure ≠ welfare loss (adversarial review §2) | Immigrants concentrate in inelastic MSAs (top FB-share quintile median elasticity 1.51 vs bottom 3.40); top 10 inelastic MSAs include all the major immigrant gateways | **Rent exposure is a stronger renter-incidence warning in inelastic destination markets** because supply response is weaker. Update: "rent exposure" should be tagged elasticity-conditional — higher incidence risk in inelastic destinations, lower in elastic. |
| Clark "agree" economists are scope-limited but not wrong on their narrow channel | E-Verify mandates produced no statistically significant positive QWI wage effect for native low-skill workers in any of 12 specifications | **The small-native-wage-effect channel in the Clark "agree" position is better supported** in the observed E-Verify policy variation. Large Borjas-style native wage gains are rejected at α=0.05 for this margin. |
| "Borjas vs Card" presented as live debate | Direct multi-state TWFE with 21-year panel finds Card-side pattern: no statistically significant positive QWI wage effect after E-Verify mandate variation | **For observed marginal enforcement variation, the Card-side pattern is favored.** Borjas's restricted-Mariel result does not generalize to the broader staggered enforcement shocks tested here; this does not settle surge or mass-shock regimes. |
| Federal-positive / local-negative split is plausible but unquantified | This cycle did not produce federal-side estimates (federal microsim still requires SIPP fix) | **Unchanged.** Federal side remains the weakest part of the repo. |
| Local-burden story is real but heterogeneous | Saiz merge sharpens the housing component; QWI supports a small/null wage response in the observed E-Verify margin | **Strengthened on the housing side, not on schooling.** School-burden findings are unchanged by this cycle. |

## E-Verify wage-channel verdict

Three converging pieces of evidence on the U.S. wage channel:

1. **Card (1990) Mariel:** zero wage effect on Miami HS dropouts.
2. **This cycle's E-Verify TWFE:** +0.5% (n.s.) wage effect on E1 workers in exposed industries across 9 mandate states 2003-2023.
3. **Foged-Peri (2016) Denmark:** native low-skill wages *rose* in a refugee dispersal-policy quasi-experiment.

Against:
- **Borjas (2017) Mariel reanalysis:** -10 to -30% on HS dropouts with restricted sample. **This finding does not generalize to the broader staggered designs tested here.**

**Verdict:** For the observed marginal U.S. policy variation in this file, large Borjas-style native wage gains from E-Verify-style labor-supply contraction are rejected at conventional significance levels. The remaining uncertainty is about surge regimes and hypothetical extreme shocks (mass deportation, border closure) that have no direct empirical analog. **The Clark Center "agree" small-native-wage-effect premise is supported for the narrow wage channel and observed-policy range, not for the all-in immigration question.**

This is a meaningful update to the repo's prior position. The verified-findings report (2026-04-10) said the Clark agree economists were "mostly right on a narrow question" but bracketed this carefully. The new evidence justifies elevating only the wage-channel premise: **small native wage effects are better supported within observed marginal policy variation.**

## Incidence — federal vs local — what this cycle changes

The Saiz finding sharpens the **local** side:
- Renter-incidence risk is structurally larger than the adversarial review allowed. In inelastic markets (where >40% of immigrants live), weaker supply response makes rent exposure more decision-relevant, but immigrant-specific rent causation still needs panel/IV identification.
- Owner-gain-to-renter-loss ratio differs by destination elasticity. The repo's existing PUMA rent table can be re-tagged elasticity-conditional once the SSD is remounted.

The E-Verify finding clarifies the **labor-market** side:
- Native low-skill wages do not rise under observed E-Verify mandate variation in the QWI panel.
- The evidence rejects large Borjas-style native wage gains from marginal enforcement, but does not directly measure the full wage effect of current inflow levels or surge regimes.
- Therefore the observed marginal-enforcement wage component of the local-burden ledger is small/null for natives; the broader labor-market ledger still includes employment composition, hours, occupational sorting, and unmeasured shock regimes.
- The total local burden is school-finance + housing-rent + service-capacity, NOT wage compression.

Combined effect on incidence narrative:
- Pre-cycle: native low-skill workers maybe lose wages (Borjas), bear school burden, face rent competition.
- Post-cycle: native low-skill wages do not measurably rise from E-Verify-style enforcement contractions; school burden and housing incidence remain separate local channels.

The political-economy reading: wage data alone are a weak justification for a native-low-skill restriction story in the observed marginal-enforcement range. School-finance exposure and renter exposure remain plausible incidence channels, but this cycle does not identify voter motivation or prove that those exposures justify the policy push; owner/renter status, local fiscal regime, and service geography still matter.

## What this cycle did NOT settle

1. **Federal microsimulation.** SIPP donor library is still broken (HHINC handled wrong). Same blocker as 2026-04-10. Not addressed this cycle.
2. **Causal IV for housing.** Saiz finding is descriptive cross-section. Card shift-share IV would be cleaner. Requires warehouse remount.
3. **DACA pre-post analysis.** Timeline + design coded but no execution this cycle (required ACS PUMS pull deferred for disk space).
4. **Spatial wage compression test.** State-level analysis may miss within-state heterogeneity. County-level QWI extension is feasible (data is there).
5. **Mass deportation counterfactual.** No data analog. The claim "tightening immigration won't help native workers" is supported for marginal enforcement, not for mass shocks.
6. **Indirect federal fiscal effects.** Colas-Sachs (2024) argument that low-skill immigration has positive indirect federal effects via consumer demand → tax base is not tested here.

## Reframing the original question

The user asked which interpretations or datasets could change conclusions. After this cycle:

- **Borjas vs Card debate:** Bounded to observed marginal U.S. policy variation. Card-side pattern there; surge and mass-shock regimes remain open.
- **Rent burden as renter-incidence risk:** Narrowed, not resolved. In inelastic destination markets it is a stronger renter-incidence warning; owner/renter incidence and causal identification caveats still apply.
- **Federal-positive / local-negative split:** Sharpened on local side, unchanged on federal side.
- **Race-stratified crime gap:** From earlier work — gap narrows from 50% to 30% but immigrants still lower than natives.
- **Place-premium / immigrant welfare weighting:** Untested this cycle. Remains the biggest single lever for flipping the verdict.
- **AGI-soon timing:** Untested empirically. Remains the biggest framing lever.

## Updated confidence ladder (additions)

Add to `immigration-confidence-ladder.md`:

```
17. `Borjas wage prediction for U.S. native low-skill workers from E-Verify`
Rating: strong against large Borjas-style gains in the E-Verify margin
Reason: TWFE on QWI 2003-2023 with 9 treated states finds +0.5% (n.s.) on E1 in
exposed industries. 95% CI excludes large Borjas magnitudes in this observed
mandate design. Surge and mass-shock regimes remain outside this result.
[SOURCE: research/immigration-causal-everify-card-vs-borjas.md]

18. `Immigrants concentrate in inelastic-supply MSAs`
Rating: STRONG (descriptive)
Reason: top FB-share quintile median Saiz elasticity 1.51, bottom 3.40. n=237 MSAs.
Implication: rent exposure in inelastic destination markets is a stronger renter-incidence warning than the adversarial review allowed.
[SOURCE: research/immigration-causal-saiz-elasticity-rent.md]

19. `Card-style labor-market complementarity for U.S. low-skill immigration`
Rating: MEDIUM-STRONG
Reason: convergent evidence from (a) Card 1990 Mariel, (b) this cycle's E-Verify
TWFE, and (c) Foged-Peri 2016 Denmark points against large native low-skill wage
losses/gains in these designs. Borjas 2017 restricted-Mariel reanalysis does not
generalize to the broader designs cited here.
[SOURCE: research/immigration-causal-everify-card-vs-borjas.md, multiple papers]
```

## What to do next

In priority order, given evidence value:

1. **Mount the SSD and rerun the Saiz×PUMA merge with the existing warehouse**, using `origin_puma_household_context_2023` × Saiz elasticity by MSA-PUMA crosswalk. This produces an *origin-conditional* renter-incidence screen, not a final welfare estimate. ~1 day with warehouse access.

2. **Fix the SIPP donor library.** This is the same call from 2026-04-10. The federal microsim remains the biggest gap. Highest-leverage single fix on the repo.

3. **County-level QWI extension** for E-Verify analysis, focused on border/non-border counties within mandate states. This would address the within-state heterogeneity caveat. Disk-cheap (similar to current pull).

4. **Card shift-share IV for housing.** Use 1990 origin-share × current national flow as instrument for current immigrant share by MSA. Rerun rent regressions with IV. Removes the cross-sectional endogeneity caveat. Requires warehouse remount.

5. **DACA pre-post on PUMS.** Implement the design already coded in `daca_timeline_and_design.md`. Tests labor-market spillovers from a clean shock. Requires ~2 GB ACS PUMS pull (defer until disk free or SSD).

6. **Continue chasing Foged-Peri analog in U.S. data.** Look for refugee resettlement quasi-random assignment (HUD voucher rollout, ORR placement quotas).

## Honest reflection

This cycle did what it set out to do: produced two original empirical findings using fresh datasets, both pointing in the Card direction. The findings are not novel relative to academic literature — they are consistent with well-known patterns rather than direct replications of those papers. The contribution is internal to this repo: **the prior epistemic posture ("Clark agree economists are scope-limited, but not false on the wage channel") understated the strength of the Card-side wage evidence**. The marginal-enforcement wage channel is bounded for the policy variation we have; surge and mass-shock regimes remain open.

The federal-fiscal side is still open. The political-economy and rent-exposure sides got sharper. The crime-rate side was already strong (separate memo earlier).

The *biggest* unresolved interpretation lever — Clemens place-premium, weighting immigrant welfare — remains untouched by this cycle. The welfare weight is a values choice; the place-premium, native-cost, fiscal, housing/capacity, and sending-country inputs are empirical and can still move the scenario break-evens.

[SOURCE: research/immigration-causal-saiz-elasticity-rent.md]
[SOURCE: research/immigration-causal-everify-card-vs-borjas.md]
[SOURCE: research/immigration-verified-findings-report-2026-04-10.md]
[SOURCE: research/immigration-confidence-ladder.md]
[SOURCE: research/immigration-adversarial-review.md]

## Revisions

| Date | Change |
|------|--------|
| 2026-06-16 | Scoped the Card-vs-Borjas section heading to the E-Verify wage-channel verdict rather than a broad theory verdict. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Replaced "E-Verify contracts unauthorized labor supply" synthesis exports with observed mandate-variation/QWI wage language; total unauthorized labor supply is not directly observed. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Replaced "Clark economists were right/correct" exports with support for the small-native-wage-effect premise within observed marginal policy variation. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Replaced residual "Card-side pattern wins" wording with "is favored" to avoid treating a bounded design comparison as debate closure. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Bounded the political-economy reading: wage evidence alone weakens the native-low-skill wage story, but school/rent exposure is only a plausible incidence channel, not identified voter motivation or policy justification. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Narrowed the embedded E-Verify confidence-ladder suggestion from global `STRONG REJECTION` to strong evidence against large Borjas-style gains in the E-Verify margin. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Replaced "QWI confirms wage channel is small" with margin-specific support for a small/null wage response in the observed E-Verify design. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Narrowed the explicit Card-vs-Borjas verdict sentence to large Borjas-style gains from E-Verify-style labor-supply contraction, not the full Borjas wage-prediction family. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Replaced "does not replicate in broader staggered designs" with "does not generalize" because E-Verify/Foged-Peri are adjacent external-validity tests, not direct Mariel replications. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Replaced "random refugee assignment" with "refugee dispersal-policy quasi-experiment"; Foged-Peri is exogenous/quasi-experimental, not a simple randomized trial. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Removed remaining "replicates well-known patterns" language; this cycle's findings are convergent/consistent evidence, not direct replications of Card, Foged-Peri, or Card-Peri. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Reframed the Clemens/welfare-weight lever: the weight is normative, but place-premium and cost/capacity inputs remain empirical. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Changed residual Saiz ladder implication from "closer to welfare loss" to a stronger renter-incidence warning in inelastic destination markets. See `immigration-conclusion-audit-running-fixes.md`. |

<!-- knowledge-index
generated: 2026-04-19T03:45:13Z
hash: 09b8c2f5eb8f

cross_refs: research/immigration-adversarial-review.md, research/immigration-causal-everify-card-vs-borjas.md, research/immigration-causal-saiz-elasticity-rent.md, research/immigration-confidence-ladder.md, research/immigration-verified-findings-report-2026-04-10.md
table_claims: 5

end-knowledge-index -->
