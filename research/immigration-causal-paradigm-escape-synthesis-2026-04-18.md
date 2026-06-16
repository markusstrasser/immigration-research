# Paradigm-escape cycle synthesis (2026-04-18, evening)

**Cycle goal:** Run Paths A + B + C from the brainstorm — sharpen the prior cycle's findings (Saiz decomposition, Foged-Peri lag, mass-deportation simulation) AND escape the prior frame (open-borders calibration, domestic-vs-abroad mover comparison, sanctuary city DiD).

**Inputs to this synthesis:**
1. `immigration-causal-internal-vs-immigrant-newcomers.md` — IRS SOI × ACS comparison
2. `data/clemens/gpt54_calibration_review.md` — GPT-5.4 sensitivity + binding-constraint analysis (Clemens 2011 calibration)
3. `data/analysis/saiz_decomposition.parquet` + console output — regulatory vs topographic channel
4. `data/analysis/sanctuary_twfe_results.csv` — sanctuary state DiD on QWI
5. `data/analysis/mass_deportation_summary.json` — BEA I-O 11M removal simulation

## Bottom line — five updates to the repo's verdict

| Pre-cycle position | New evidence | Updated verdict |
|---|---|---|
| "Rent exposure ≠ welfare loss" was a strong adversarial caveat | Saiz decomposition: log(FB share) ~ unaval (β=0.12, n.s.) + WRLURI (β=0.33, t=6.29***); WRLURI is the stronger correlate | **Rent exposure is closer to welfare loss in inelastic destination markets, and zoning reform is a plausible policy hypothesis** — the descriptive channel is strong, but neither immigrant-specific rent causation nor zoning causation is identified without panel/IV evidence |
| Card-vs-Borjas "live debate"; prior cycle showed E-Verify null wage effect | Sanctuary state DiD on same QWI panel: pro-sanctuary E1 wages +0.5% (n.s.), anti-sanctuary E1 wages +0.8% (n.s.) — additional QWI policy-margin check | **For observed marginal enforcement variation, the Card-side pattern wins.** Native low-skill wages do not measurably respond to the E-Verify/sanctuary-style variation tested here; this does not settle surge or mass-shock regimes. |
| "Newcomer burden" treated as immigration-driven by default | IRS SOI `Total Migration-US` and ACS `Moved from abroad` still show an order-of-magnitude county gap, but the exact ratio is measurement-sensitive and not a clean burden ratio | **Most county newcomer pressure is not immigration-specific.** Treat this as a descriptive frame correction, not a precise causal burden split. |
| Mass-deportation hypothetical had no empirical analog | BEA I-O 2023 calibration: removing 7M unauthorized → $1.45T first-order output loss (5.3% GDP); $2.32T with multiplier (8.5%) as Type-II sensitivity; per-removed-worker loss $207K first-order and $332K under Type-II sensitivity | **Mass deportation would impose a large first-order output shock**, concentrated in Construction (-5.9%), Other Services / cleaning (-8.8%), Agriculture (-4.3%); multiplier amplification should be labeled as sensitivity |
| Repo verdict implicitly weights immigrant welfare at zero | GPT-5.4 calibration with project's findings as inputs: at w=0 negative by construction; at w≥0.25 positive under 25%-cost benchmark; housing/construction is modeled as binding in year 1 for every scenario S1+ | **Verdict is welfare-weight-sensitive under the current cost/capacity calibration.** Honest framing must name the welfare weight; empirical work can still move native-cost, fiscal, housing, and feasibility inputs. Feasibility constraint should be framed as a calibration warning: U.S. housing/construction may bind quickly at very large arrival scenarios, not as a validated national threshold. |

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
| 1 | E-Verify mandates do not raise native low-skill wages | STRONG against large Borjas-style wage gains in this enforcement margin | TWFE on QWI 2003-23, 9 states |
| 2 | E-Verify mandates reduce E1 employment in exposed industries ~6% (marginal) | MEDIUM | Same |
| 3 | Sanctuary policy variation produces null E1 wage effects (both directions) | STRONG null result for the tested policy variations | TWFE on QWI 2003-23, 12 sanctuary + 9 anti |
| 4 | Immigrants concentrate in inelastic-supply MSAs (top FB-share quintile median elasticity 1.51 vs bottom 3.40) | STRONG (descriptive) | Saiz × ACS 2022 5-yr, 237 MSAs |
| 5 | The inelastic-MSA concentration is more strongly associated with WRLURI than topographic unavailability | STRONG descriptive regression, not causal channel proof | Saiz decomposition regression |
| 6 | Domestic U.S.-origin mover flow is order-of-magnitude larger than moved-from-abroad flow at the median county | STRONG descriptive, not burden-causal | IRS SOI 2022-23 × ACS `B07001_081E` |
| 7 | Mass deportation of 7M unauthorized → ~$1.45T first-order output loss (~5% GDP), concentrated in Construction, Other Services, Agriculture; ~$2.32T / ~8% is Type-II sensitivity | MEDIUM (calibration, not estimate) | BEA Use Table 2023 partial-equilibrium sim |
| 8 | Open-borders welfare calculation depends heavily on weight assigned to immigrant welfare under the current native-cost benchmarks; housing capacity is a modeled early-binding constraint in very-large-arrival scenarios | MEDIUM (sensitivity analysis on Clemens parameters) | GPT-5.4 review of calibration |

### Three new policy-relevant statements

**Statement 1 — Card-side pattern wins for observed marginal wage variation.**
Two repo QWI policy-margin tests now (E-Verify + sanctuary state), read alongside Card/Foged-Peri literature, show no measurable native low-skill wage gains in the tested E-Verify/sanctuary-style range. The GPT-5.4 calibration belongs to the welfare-weight sensitivity frame, not the wage-evidence stack. The Borjas Mariel-restriction result does not generalize to this observed range. Future repo memos should treat the wage claim as **bounded to marginal policy variation**; surge and mass-shock regimes remain open.

**Statement 2 — The local-burden ledger is mostly domestic-mover driven; moved-from-abroad flow is a small visible component.**
At the median U.S. county, IRS `Total Migration-US` inflow is roughly an order of magnitude larger than ACS moved-from-abroad flow: the current corrected memo gives about **21.7x** for the ratio of medians and about **20.5x** for the median county-level ratio among counties with nonzero moved-from-abroad share. This is a descriptive frame correction, not a precise burden ratio, and the IRS series is not native-only. The Texas exurbs (Comal, Kaufman, Rockwall) experiencing 12-14% annual population replacement are doing so without moved-from-abroad flow as the primary driver. Where moved-from-abroad flow IS the dominant proximate driver (Miami-Dade, Hudson NJ, Santa Clara CA), it operates at much smaller scale than internal U.S. migration in equally-stressed Sun Belt counties.

**Statement 3 — The open-borders verdict mixes a value weight with empirical inputs.**
The headline arithmetic flips on the welfare weight assigned to immigrants. At w=0 (the repo's implicit framing), the verdict is negative by construction. At w=1.0 (full equal weight), the verdict is positive under the current 50%-of-gross-gains native-cost benchmark. The repo cannot empirically resolve the value weight itself, but empirical work can still move native-cost, fiscal, housing/capacity, and sending-country inputs. It must stop hiding the weight assumption without pretending the non-weight inputs are settled.

### Updated headline confidence ladder

Four entries to add (in addition to the three from morning cycle):

```
20. `Saiz elasticity-immigrant correlation is stronger for regulatory index than topographic unavailability`
Rating: STRONG descriptive regression
Reason: log(FB share) ~ WRLURI t=6.29*** vs unaval t=0.58. This makes zoning reform
a plausible policy hypothesis, not an identified causal lever for immigrant rent burden.
[SOURCE: research/immigration-causal-everify-card-vs-borjas.md, saiz_decomposition.py]

21. `Sanctuary policy variation does not change native low-skill wages either direction`
Rating: STRONG null result in this design (aligned with E-Verify margin)
Reason: TWFE on QWI 2003-23 with 12 pro-sanctuary + 9 anti-sanctuary states; all
E1 specifications |t|<1.0; another Card-side null for observed marginal policy variation
[SOURCE: scripts/analyze_sanctuary_wages.py]

22. `Domestic U.S.-origin mover flow is order-of-magnitude larger than moved-from-abroad flow at median county`
Rating: STRONG descriptive, not burden-causal
Reason: IRS SOI 2022-23 `Total Migration-US` and ACS `B07001_081E` imply about
21.7x for the ratio of medians and about 20.5x for the median county-level
ratio among counties with nonzero moved-from-abroad share. The IRS flow is not
native-only, so this reframes "newcomer burden" as predominantly domestic-
movement-driven outside specific gateways, but does not identify school,
shelter, or wage incidence directly.
[SOURCE: research/immigration-causal-internal-vs-immigrant-newcomers.md]

23. `Open-borders welfare verdict is welfare-weight-sensitive under current cost inputs`
Rating: STRONG (framing claim)
Reason: At w=0 negative by construction; at w≥0.25 positive under 25%-cost
benchmark; at w=1.0 positive under the current 50%-cost benchmark. Empirical
evidence cannot adjudicate the value weight, but can change native-cost,
fiscal, capacity, and sending-country inputs. Honest framing must name both.
[SOURCE: data/clemens/gpt54_calibration_review.md]

24. `Mass deportation of 7M unauthorized would impose ~$1.45T first-order output shock (~5% GDP); Type-II endpoint is sensitivity only`
Rating: MEDIUM (calibration not estimate)
Reason: BEA I-O 2023 partial-equilibrium with industry FB-share assumptions;
the ~$2.32T / ~8% Type-II endpoint is a labeled multiplier sensitivity, not
coequal headline estimate truth. Consistent with E-Verify -6% E1 employment
finding under 50% compliance.
[SOURCE: scripts/mass_deportation_sim.py]
```

## Methodological note

This cycle used **GPT-5.4 (high-then-medium reasoning effort) for the open-borders sensitivity analysis** because the question required parameter sensitivity reasoning across 5 sections that exceeds Claude's typical chain-of-thought depth. The first dispatch hit the max-tokens-includes-reasoning footgun (24K budget exhausted by reasoning, 0 visible output). The second dispatch with 48K budget and concatenated single context file produced a 16.5KB structured response. The result was integrated into the synthesis above.

This is the right division of labor: **Claude orchestrates and runs analyses on local data; GPT-5.4 handles parameter-sensitivity reasoning over a fixed framework.** Routing per `~/.claude/rules/llmx-routing.md`.

## What to do next (priority order)

1. **Mount SSD and re-run Saiz×PUMA + warehouse merges** — the Saiz finding is at MSA level; the existing warehouse has PUMA-level data that would sharpen everything. Same blocker as morning cycle.
2. **Fix SIPP donor library + run federal microsim** — same call from 2026-04-10. Highest-leverage single fix on the repo.
3. **Run DACA pre-post on ACS PUMS** — the design is documented, just needs execution. Free up disk first.
4. **Run Foged-Peri-style 6-yr lag analogue test** — also disk-constrained but smaller. Could explain Card-side wage finding via lag distribution.
5. **Sending-country welfare ledger** — natural extension of open-borders frame.
6. **Comparative international regimes** — Gulf Kafala / Canada points / Germany 2015 to test what's regime-specific.
7. **Diversity Visa lottery RCT** — true random assignment data for cleanest causal evidence.
8. **Immigration judge IV** — TRAC EOIR data for de facto policy.

Items 1-4 should be sequential; 5-8 can run independently in parallel cycles.

## Honest reflection

This was a productive cycle, but the *data* additions did not produce paradigm shifts — they sharpened existing positions. The two findings that genuinely change the repo's framing are:
- **Internal/domestic mover comparison** (corrected ~20–22x median-ratio range) — disrupts the "newcomer = immigrant" frame
- **Welfare-weight reframing of open-borders** — names the implicit zero-weight assumption that drives the verdict

The other findings (Saiz decomposition, sanctuary DiD, mass-deportation sim) are confirmatory or refining. Useful, not transformative.

The biggest *interpretation* lever remains the welfare-weight question, which is a values choice that no additional empirical work resolves by itself. But the empirical inputs still matter: native costs, capacity constraints, fiscal ledgers, and sending-country effects can move the break-even thresholds. The repo can either (a) make the implicit zero weight explicit and own it, (b) shift to a documented non-zero weight and re-grade everything, or (c) report multiple weighted scenarios as scenario analysis. Option (c) is honest; (a) and (b) are equally legitimate but should stop hiding the choice.

## Revisions

| Date | Change |
|------|--------|
| 2026-06-16 | Bounded short-form E-Verify/sanctuary confidence language: the findings reject large enforcement-channel wage gains within the tested policy margins, not every Borjas-style or enforcement-channel claim. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Bounded Saiz decomposition language: WRLURI is a stronger descriptive correlate than topographic unavailability, not proof that zoning drives immigrant concentration or that zoning reform is an identified causal lever. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Removed GPT-5.4 calibration from the wage-evidence stack; it is welfare-weight sensitivity/model reasoning, not an empirical wage test. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Reframed open-borders welfare-weight language: the value weight is normative, but native-cost, fiscal, capacity, and sending-country inputs remain empirical. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Replaced remaining sanctuary "replicates E-Verify margin" phrasing with alignment language; it is an additional QWI policy-margin check, not a direct replication. See `immigration-conclusion-audit-running-fixes.md`. |

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
