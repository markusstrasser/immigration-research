# Source-Incentive Re-Grade — what survives when you discount advocacy and reward against-interest findings

**Date:** 2026-06-23
**Trigger:** operator critique — economists left-lean + single-channel overreach → journalist selection → LLM pretraining inherits the tilt. This pass turns that critique into a scoring rule the corpus runs.
**Lens:** `G-LIF-U01` (source-incentive / against-interest audit). **Table:** `source_incentive_grades` (in the unified release). **Builder:** `build_source_incentive_grades.py`.

## The rule (symmetric by construction)

A finding is more credible when it cuts **against** its source's own prior, and less credible when it's advocacy **confirming** that prior — *on both sides*. A version that only deflated the other team's advocacy would be the bias it audits.

```
base_weight  : govt_nonpartisan 1.0 | academic 0.8 | think_tank 0.6 | advocacy 0.4
against_interest      : restrictionist source → benefit finding,  OR  expansionist → cost finding
with_interest_advocacy: advocacy outlet whose finding confirms its own prior
adj_weight = min(1.0, base × (1.5 if against_interest else 0.7 if with_interest_advocacy else 1.0))
```

## Result (20 load-bearing sources)

| adj | source | finding | why |
|----:|--------|---------|-----|
| **1.0** | NAS 2016/17 panel | mixed | establishment panel publishing the <HS cost *and* the 2nd-gen benefit |
| **1.0** | CBO federal (surge cut deficit) | benefit | nonpartisan |
| **1.0** | CBO state-local cost | cost | nonpartisan |
| **1.0** | **Borjas — immigration surplus +** | benefit | **against-interest**: the field's skeptic deriving a positive aggregate |
| **1.0** | NAS — 2nd-gen contribution | benefit | nonpartisan panel |
| 0.8 | Borjas — low-skill wage harm | cost | academic, with-interest (standard weight) |
| 0.8 | Razin-Wahba — fiscal leakage | cost | academic, with-interest |
| 0.8 | Card/Peri, Clemens, Colas-Sachs, Cortes, AJKM, Ottaviano-Peri | benefit | academic, with-interest |
| **0.28** | **ITEP** — immigrants pay $X tax | benefit | expansionist advocacy confirming its prior |
| **0.28** | **Cato** — immigration benefits | benefit | expansionist advocacy |
| **0.28** | **FAIR** — high fiscal cost | cost | restrictionist advocacy confirming its prior |
| **0.28** | **CIS/Camarota** — welfare-use cost | cost | restrictionist advocacy |

## What shifts (this is the point)

- **The benefit headline weakens where it leans on advocacy.** "Immigrants are net contributors" rests heavily on ITEP/Cato/CAP — deflated to 0.28. Your media-critique is *correct here*: that specific meme is advocacy-inflated.
- **…but the aggregate-positive does NOT collapse**, because it doesn't depend on advocacy. It rests on **Borjas's own surplus identity** (up-weighted to 1.0 *because* it's against his prior) and the **nonpartisan CBO federal** number. The most pro-immigration-sounding result survives precisely because its source had every incentive to find the opposite.
- **The restrictionist headline also weakens.** The scary "huge fiscal cost / −$200k" numbers lean on FAIR/CIS — also deflated to 0.28. The rule does not flatter your prior; that's the integrity test, and it passes.
- **The real cost finding survives.** The <HS lifetime fiscal negative is NAS (1.0) and the state-local cost is CBO (1.0) — nonpartisan, not advocacy. The cost is real; it just isn't FAIR's number.

**Net:** discounting advocacy on both ends and rewarding against-interest findings leaves the **multi-ledger picture** standing — NAS <HS cost (real), CBO federal-positive (real), CBO state-local cost (real), Borjas aggregate surplus (real, against-interest), Borjas distributional wage hit (real). The advocacy noise on both sides — the part most amplified by journalists into pretraining — is exactly what drops out.

## Honest residual

The symmetry check: mean `adj_weight` is **0.63 (cost) vs 0.76 (benefit)** — close, and the *rubric* is direction-blind (the multipliers never see cost/benefit). The 0.13 gap comes from **source-set composition**: more mid-credibility *academic* benefit papers (Card, Clemens, Colas-Sachs, Cortes, AJKM, Ottaviano-Peri) than academic cost papers (Borjas-wage, Razin) entered the list. That is itself partly your point — the academy *produces* more benefit-framed papers — but it's a composition fact, not a tilted rule, and it may also reflect my source selection. Flagged as a thing to check: is the academic benefit:cost paper ratio real, or did I under-list the rigorous cost-side work (e.g., more Borjas, Camarota's peer-reviewed pieces, Huddle)? The grade table is append-only — add sources and re-run.

## Reproduce

```bash
duckdb warehouse/immigration.duckdb "SELECT label, finding_direction, adj_weight FROM source_incentive_grades ORDER BY adj_weight DESC"
```
