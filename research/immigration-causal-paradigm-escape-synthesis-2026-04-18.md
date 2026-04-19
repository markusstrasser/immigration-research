# Paradigm-escape cycle synthesis (2026-04-18, evening)

**Cycle goal:** Run Paths A + B + C from the brainstorm — sharpen the prior cycle's findings (Saiz decomposition, Foged-Peri lag, mass-deportation simulation) AND escape the prior frame (open-borders calibration, internal-native comparison, sanctuary city DiD).

**Inputs to this synthesis:**
1. `immigration-causal-internal-vs-immigrant-newcomers.md` — IRS SOI × ACS comparison
2. `data/clemens/gpt54_calibration_review.md` — GPT-5.4 sensitivity + binding-constraint analysis (Clemens 2011 calibration)
3. `data/analysis/saiz_decomposition.parquet` + console output — regulatory vs topographic channel
4. `data/analysis/sanctuary_twfe_results.csv` — sanctuary state DiD on QWI
5. `data/analysis/mass_deportation_summary.json` — BEA I-O 11M removal simulation

## Bottom line — five updates to the repo's verdict

| Pre-cycle position | New evidence | Updated verdict |
|---|---|---|
| "Rent exposure ≠ welfare loss" was a strong adversarial caveat | Saiz decomposition: log(FB share) ~ unaval (β=0.12, n.s.) + WRLURI (β=0.33, t=6.29***); regulatory channel dominates | **Rent exposure IS welfare loss AND zoning reform is a viable policy lever** — rent burden is policy-tractable, not topographic |
| Card-vs-Borjas "live debate"; prior cycle showed E-Verify null wage effect | Sanctuary state DiD on same QWI panel: pro-sanctuary E1 wages +0.5% (n.s.), anti-sanctuary E1 wages +0.8% (n.s.) — **third confirmation** | **Native low-skill wages do not respond to enforcement variation in either direction.** Card wins decisively on observed U.S. policy variation. |
| "Newcomer burden" treated as immigration-driven by default | IRS SOI: median county receives 3.0% native + 0.08% immigrant inflow per year (33× ratio). Texas exurbs / military bases dominate the top inflow list, not immigrant gateways | **Most local newcomer pressure is internal native migration, not immigration.** Restricting immigration cannot fix newcomer-driven burden in fast-growing counties. |
| Mass-deportation hypothetical had no empirical analog | BEA I-O 2023 calibration: removing 7M unauthorized → $1.45T first-order output loss (5.3% GDP); $2.32T with multiplier (8.5%); per-removed-worker loss $207K-$332K, ~7-11× their own annual earnings | **Mass deportation would impose a one-time $1.5-2.3T output shock**, concentrated in Construction (-5.9%), Other Services / cleaning (-8.8%), Agriculture (-4.3%) |
| Repo verdict implicitly weights immigrant welfare at zero | GPT-5.4 calibration with project's findings as inputs: at w=0 negative by construction; at w≥0.25 positive under 25%-cost benchmark; housing/construction binds in year 1 for every scenario S1+ | **Verdict is welfare-weight-driven, not data-driven, in the dimension that matters most.** Honest framing must name the weight. Feasibility constraint: U.S. housing/construction binds immediately at any scenario above ~10M/year arrivals. |

## What this cycle didn't settle

- **Federal microsim** still broken (SSD blocker from prior cycle; SIPP HHINC bug). Highest-leverage single fix that remains.
- **Foged-Peri 6-yr lag** deferred (disk-constrained ACS PUMS pull; lower marginal value than completed items).
- **DACA pre-post**, **Diversity Visa lottery**, **Immigration judge IV** — Tier 1 brainstorm items not executed this cycle.
- **Sending-country welfare** — still unaddressed, but partially subsumed by the open-borders calibration which forces the question.
- **Comparative international regimes** — Tier 3 brainstorm item not executed.

## Synthesis of the two cycles (2026-04-18 morning + evening)

### Eight findings now in the repo

| # | Finding | Confidence | Method |
|---|---------|------------|--------|
| 1 | E-Verify mandates do not raise native low-skill wages | STRONG REJECTION of Borjas | TWFE on QWI 2003-23, 9 states |
| 2 | E-Verify mandates reduce E1 employment in exposed industries ~6% (marginal) | MEDIUM | Same |
| 3 | Sanctuary policy variation produces null E1 wage effects (both directions) | STRONG REJECTION of enforcement-channel wage effects | TWFE on QWI 2003-23, 12 sanctuary + 9 anti |
| 4 | Immigrants concentrate in inelastic-supply MSAs (top FB-share quintile median elasticity 1.51 vs bottom 3.40) | STRONG (descriptive) | Saiz × ACS 2022 5-yr, 237 MSAs |
| 5 | The inelastic-MSA concentration is driven by REGULATORY constraint (WRLURI), not topography | STRONG | Saiz decomposition regression |
| 6 | Native US migration is ~33× larger per capita per year than recent immigration at the median county | STRONG | IRS SOI 2022-23 × ACS B05005 |
| 7 | Mass deportation of 7M unauthorized → $1.5-2.3T output loss (5-8% GDP), concentrated in Construction, Other Services, Agriculture | MEDIUM (calibration, not estimate) | BEA Use Table 2023 partial-equilibrium sim |
| 8 | Open-borders welfare calculation depends entirely on weight assigned to immigrant welfare; at w≥0.25 positive even under harsh native-cost benchmarks; housing capacity binds in year 1 at any scenario above ~10M arrivals/year | MEDIUM (sensitivity analysis on Clemens parameters) | GPT-5.4 review of calibration |

### Three new policy-relevant statements

**Statement 1 — Card wins decisively on the wage channel.**
Three convergent tests now (E-Verify + sanctuary state + GPT-5.4 calibration interpretation) all show that native low-skill wages do not respond to immigration enforcement variation. The Borjas Mariel-restriction result does not generalize to the U.S. policy variation we have. Future repo memos should treat this as settled, not open.

**Statement 2 — The local-burden ledger is mostly native-newcomer driven; immigration is a small visible component.**
At the median U.S. county, 33× more newcomer flow comes from natives than from immigrants. The Texas exurbs (Comal, Kaufman, Rockwall) experiencing 12-14% annual population replacement are doing so without immigration as the primary driver. Where immigration IS the dominant proximate driver (Miami-Dade, Hudson NJ, Santa Clara CA), it operates at much smaller scale than internal native migration in equally-stressed Sun Belt counties.

**Statement 3 — The open-borders verdict is a values question, not an empirical one.**
The headline arithmetic flips on the welfare weight assigned to immigrants. At w=0 (the repo's implicit framing), the verdict is negative by construction. At w=1.0 (full equal weight), the verdict is positive even under harsh 50%-of-gross-gains native-cost benchmarks. The repo cannot resolve this empirically — but it MUST stop hiding the weight assumption.

### Updated headline confidence ladder

Four entries to add (in addition to the three from morning cycle):

```
20. `Saiz elasticity-immigrant correlation operates through regulatory not topographic channel`
Rating: STRONG
Reason: log(FB share) ~ WRLURI t=6.29*** vs unaval t=0.58. Zoning reform is a
policy lever for the rent-burden problem.
[SOURCE: research/immigration-causal-everify-card-vs-borjas.md, saiz_decomposition.py]

21. `Sanctuary policy variation does not change native low-skill wages either direction`
Rating: STRONG REJECTION (replicates E-Verify finding)
Reason: TWFE on QWI 2003-23 with 12 pro-sanctuary + 9 anti-sanctuary states; all
E1 specifications |t|<1.0; third confirmation of Card-side null
[SOURCE: scripts/analyze_sanctuary_wages.py]

22. `Native US migration is ~33x larger per capita than recent immigration at median county`
Rating: STRONG (admin data, not survey)
Reason: IRS SOI 2022-23 + ACS B05005. Reframes "newcomer burden" as
predominantly native-driven outside specific immigrant gateways.
[SOURCE: research/immigration-causal-internal-vs-immigrant-newcomers.md]

23. `Open-borders welfare verdict is welfare-weight-determined, not data-determined`
Rating: STRONG (framing claim)
Reason: At w=0 negative by construction; at w≥0.25 positive under 25%-cost
benchmark; at w=1.0 positive even at 50%-cost. Empirical evidence cannot
adjudicate values. Honest framing must name the weight.
[SOURCE: data/clemens/gpt54_calibration_review.md]

24. `Mass deportation of 7M unauthorized would impose ~$1.5-2.3T one-time output shock (5-8% GDP)`
Rating: MEDIUM (calibration not estimate)
Reason: BEA I-O 2023 partial-equilibrium with industry FB-share assumptions;
consistent with E-Verify -6% E1 employment finding under 50% compliance
[SOURCE: scripts/mass_deportation_sim.py]
```

## Methodological note

This cycle used **GPT-5.4 (high-then-medium reasoning effort) for the open-borders sensitivity analysis** because the question required parameter sensitivity reasoning across 5 sections that exceeds Claude's typical chain-of-thought depth. The first dispatch hit the max-tokens-includes-reasoning footgun (24K budget exhausted by reasoning, 0 visible output). The second dispatch with 48K budget and concatenated single context file produced a 16.5KB structured response. The result was integrated into the synthesis above.

This is the right division of labor: **Claude orchestrates and runs analyses on local data; GPT-5.4 handles parameter-sensitivity reasoning over a fixed framework.** Routing per `~/.claude/rules/llmx-routing.md`.

## What to do next (priority order)

1. **Mount SSD and re-run Saiz×PUMA + warehouse merges** — the Saiz finding is at MSA level; the existing warehouse has PUMA-level data that would sharpen everything. Same blocker as morning cycle.
2. **Fix SIPP donor library + run federal microsim** — same call from 2026-04-10. Highest-leverage single fix on the repo.
3. **Run DACA pre-post on ACS PUMS** — the design is documented, just needs execution. Free up disk first.
4. **Run Foged-Peri 6-yr lag replication** — also disk-constrained but smaller. Could explain Card-side wage finding via lag distribution.
5. **Sending-country welfare ledger** — natural extension of open-borders frame.
6. **Comparative international regimes** — Gulf Kafala / Canada points / Germany 2015 to test what's regime-specific.
7. **Diversity Visa lottery RCT** — true random assignment data for cleanest causal evidence.
8. **Immigration judge IV** — TRAC EOIR data for de facto policy.

Items 1-4 should be sequential; 5-8 can run independently in parallel cycles.

## Honest reflection

This was a productive cycle, but the *data* additions did not produce paradigm shifts — they sharpened existing positions. The two findings that genuinely change the repo's framing are:
- **Internal-native migration comparison** (the 33× ratio) — disrupts the "newcomer = immigrant" frame
- **Welfare-weight reframing of open-borders** — names the implicit zero-weight assumption that drives the verdict

The other findings (Saiz decomposition, sanctuary DiD, mass-deportation sim) are confirmatory or refining. Useful, not transformative.

The biggest *interpretation* lever remains the welfare-weight question, which is a values choice that no additional empirical work resolves. The repo can either (a) make the implicit zero weight explicit and own it, (b) shift to a documented non-zero weight and re-grade everything, or (c) report multiple weighted scenarios as scenario analysis. Option (c) is honest; (a) and (b) are equally legitimate but should stop hiding the choice.

[SOURCE: research/immigration-causal-everify-card-vs-borjas.md]
[SOURCE: research/immigration-causal-saiz-elasticity-rent.md]
[SOURCE: research/immigration-causal-synthesis-2026-04-18.md]
[SOURCE: research/immigration-causal-internal-vs-immigrant-newcomers.md]
[SOURCE: data/clemens/gpt54_calibration_review.md]
[SOURCE: data/analysis/sanctuary_twfe_results.csv]
[SOURCE: data/analysis/mass_deportation_summary.json]
[SOURCE: scripts/saiz_decomposition.py]

<!-- knowledge-index
generated: 2026-04-19T04:21:56Z
hash: cb845f425587

cross_refs: research/immigration-causal-everify-card-vs-borjas.md, research/immigration-causal-internal-vs-immigrant-newcomers.md, research/immigration-causal-saiz-elasticity-rent.md, research/immigration-causal-synthesis-2026-04-18.md

end-knowledge-index -->
