# Dismantling the Cato Institute's immigration case — step by step

**Date:** 2026-06-25 | **Tier:** Deep | **Section of:** consolidated dismantling memo
**Authors in scope:** Alex Nowrasteh (crime, fiscal), David Bier (legal immigration / backlogs), Bryan-Caplan-adjacent open-borders macro (Caplan's flagship is itself a *Cato Journal* article).

**Instrument caveat:** Immigration is politically charged and this LLM instrument has documented tilt toward the pro-immigration / "less costly" direction. [SOURCE: notes/llm-bias-caveat.md] Cato is a libertarian, pro-immigration ADVOCACY org (graded as such — base_weight 0.4, with-interest advocacy multiplier → 0.28). [SOURCE: research/immigration-source-incentive-regrade-2026-06-23.md]

**The central tension this memo must hold honestly:** Cato is advocacy, BUT its CRIME work is empirically solid and *this repo uses it* — Nowrasteh's TX conviction series anchors confidence-ladder entry 48 (illegal-immigrant homicide-conviction rate −26% vs native). You therefore CANNOT dismiss Cato wholesale without contradicting our own ladder. The honest, devastating split: **GRANT the crime empirics** (real, checkable, against the libertarian's own interest in showing a cost — which is *why* they're trustworthy), then **surgically kill the OVERCLAIMS** in the fiscal-macro and open-borders work. The fairness is the weapon.

**Method:** Builds on `research/immigration-economist-rhetorical-failures-2026-04-22.md` (the 6-move spine), `research/immigration-bryan-caplan-claims-audit-2026-04-21.md`, `research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md`, `research/immigration-open-borders-break-even-bounds-2026-04-22.md`, `research/immigration-source-incentive-regrade-2026-06-23.md`, and confidence-ladder entries 42-50. The 6 named moves: (1) ledger-switching/equivocation, (2) upper-bound laundering, (3) marginal-to-mass extrapolation, (4) capacity erasure, (5) denominator masking, (6) political-economy underspecification.

## STATUS: primary sources fetched + verified. Findings below.

The four load-bearing Cato briefs, all primary-fetched 2026-06-25:
1. **Nowrasteh, "Illegal Immigrant Murderers in Texas, 2013–2022"** (Policy Analysis 977, 2024) — TX DPS conviction data. [SOURCE: https://www.cato.org/policy-analysis/illegal-immigrant-murderers-texas-2013-2022]
2. **Nowrasteh & Famularo, "Immigrants' Recent Effects on Government Budgets: 1994–2023"** (White Paper, Feb 2026) — the NASEM–Cato static model. [SOURCE: https://www.cato.org/white-paper/immigrants-recent-effects-government-budgets-1994-2023]
3. **Nowrasteh & Famularo, welfare-consumption brief (2022 SIPP)** — immigrants consume 21% less welfare/capita. [SOURCE: https://www.cato.org/news-releases/immigrants-consume-less-welfare-entitlement-benefits-native-born-americans]
4. **Bier, "Immigration Wait Times from Quotas Have Doubled"** (Policy Analysis 873, 2019) + Senate Budget testimony (2023) — green-card backlog. [SOURCE: https://www.cato.org/publications/policy-analysis/immigration-wait-times-quotas-have-doubled-green-card-backlogs-are-long]

Plus Caplan's flagship *Cato Journal* piece "Why Should We Restrict Immigration?" (2012), already primary-audited. [SOURCE: research/immigration-bryan-caplan-claims-audit-2026-04-21.md]

---

## Cato's core immigration arguments by domain

| # | Domain | Cato claim (steelman, one sentence) | Verdict | Move (if overclaim) |
|---|--------|-------------------------------------|---------|---------------------|
| C1 | Crime | Illegal and legal immigrants are convicted of homicide at materially LOWER rates than native-born Americans (TX DPS, 2013-2022: 2.2 vs 3.0/100k, −26%). | **GRANT — solid, repo uses it** | — |
| C2 | Crime → policy | Therefore immigration enforcement aimed at "criminal aliens" is mis-targeted public safety policy. | **Mostly grant (scoped)** | mild (4) — first-gen/authorized-carried |
| C3 | Fiscal | Immigrants are net-positive for government budgets by **$14.5T over 1994-2023, at BOTH the federal AND the state/local level** (+$6.6T state/local surplus). | **OVERCLAIM — kill** | **(1) ledger-switching + unit-selection** |
| C4 | Fiscal | Immigrants consume **21% less** means-tested welfare/entitlements per capita than natives (2022 SIPP). | **Grant the datum, kill the inference** | (1) single-channel ledger presented as fiscal verdict |
| C5 | Fiscal → policy | "Build a wall around the welfare state" (keyhole: bar immigrant welfare access) is the free-market answer to any fiscal cost. | **OVERCLAIM — kill** | (6) political-economy / state-capacity erasure |
| C6 | Legal/macro | Green-card quotas are absurdly low: waits doubled, 4.7M+ backlog, 675k will die in line; the legal system "thwarts" willing workers. | **GRANT the descriptive backlog facts** | — |
| C7 | Legal/macro | Therefore the U.S. should massively expand legal immigration ("1% of population" ≈ 3.4M/yr) with the gains treated as near-free. | **OVERCLAIM — kill** | **(3) marginal-to-mass + (4) capacity erasure** |
| C8 | Open-borders | (Caplan, *Cato Journal* 2012) Free migration could roughly double world GDP; restriction needs a real excuse; keyhole solutions handle every objection. | **Sign survives, magnitude + closure killed** | **(2) upper-bound laundering + (3) + (6)** |

---

## Per-claim dismantling

### C1 + C2 — Crime: GRANT (this is the honest core; the repo USES it)

**Steelman:** Texas is the only state recording immigration status at arrest/conviction; over 2013-2022 the illegal-immigrant homicide-conviction rate was 2.2/100k vs 3.0/100k native-born (−26.2%), legal immigrants 1.2/100k (−61.4%); 472 illegal-immigrant vs 7,109 native-born homicide convictions; illegal immigrants were 7.1% of TX population but 5% of homicide convictions. [SOURCE: https://www.cato.org/policy-analysis/illegal-immigrant-murderers-texas-2013-2022]

**Verdict: GRANT.** This is not laundered. It is:
- **Primary administrative data**, not a model — TX DPS counts obtained by Public Information Act request, the same underlying data Light et al. (PNAS) use. [SOURCE: confidence-ladder entry 48]
- On the **homicide margin specifically**, which is near-fully-reported and detection-resistant — it closes the standard "arrests ≠ guilt / under-detection of unauthorized" objection that weakens softer crime claims. [SOURCE: confidence-ladder entry 48]
- **Against the libertarian's own interest** in the source-incentive sense: an advocacy shop motivated to show immigration's *benefits* has no incentive to publish a clean cost series — yet Nowrasteh publishes the non-homicide categories too (flagging their data quality is "suspect"), and reports the years where immigrant rates rise. That against-interest robustness is exactly why our regrade does NOT deflate this the way it deflates the fiscal claim. [SOURCE: research/immigration-source-incentive-regrade-2026-06-23.md]
- **Adopted into our own confidence ladder at entry 48** with `DIRECTION strong (now incl. convictions)`. To dismiss it would contradict the repo.

**The only scoping (not a kill, a bound):** entry 48's disconfirming caveats apply to Cato's framing too — the protective signal is (a) **first-generation** (decays toward native rates by the 2nd generation, RTI 2024) and (b) **authorship-status-heterogeneous** (NIJ/RTI 2024: the *unauthorized* share is a NULL ecological arrest predictor once controlled; the advantage is carried disproportionately by *authorized* immigrants). [SOURCE: confidence-ladder entry 48, SOURCE: NIJ 310356] Cato's headline ("illegal immigrants −26%") is real for TX homicide convictions but should not be read as "unauthorized status is protective everywhere" — it is "first-gen TX residents, homicide margin." Cato is careful here in the paper; the overreach is in how the number gets *cited*, not in Nowrasteh's text.

**[FRAMING-SENSITIVE]:** cite the TX DPS counts as the datum; attribute the *rate framing* to Cato.

### C3 — Fiscal "$14.5T, positive at federal AND state/local": KILL (the central overclaim)

**Steelman:** Nowrasteh & Famularo (Feb 2026) build a NASEM–Cato model on CPS-ASEC 1994-2023, validated to BEA/NIPA, and find immigrants generated $24.2T in taxes against $13.6T in costs = +$10.6T net, +$3.9T avoided-interest = **+$14.5T total**, with the state/local ledger *itself* a **+$6.6T surplus** ($9.6T taxes − $4.7T costs). [SOURCE: https://www.cato.org/white-paper/immigrants-recent-effects-government-budgets-1994-2023]

**Why this is the load-bearing overclaim:** it directly contradicts the nonpartisan authority our own ladder treats as decisive. **Confidence-ladder entry 46** (CBO 2024, the official scorekeeper): the surge is fiscally positive at the **FEDERAL** level but CBO explicitly **excludes state/local**, "where NAS finds the cost concentrates (education)." [SOURCE: confidence-ladder entry 46] And **NAS 2016/17** — the establishment panel, graded 1.0 in our regrade — finds the <HS immigrant a lifetime fiscal *cost*, concentrated at the state/local level via education. [SOURCE: research/immigration-source-incentive-regrade-2026-06-23.md] Cato's state/local-POSITIVE finding is the outlier; the question is *what assumption produces the flip*.

**The kill (verified at the methodology — two moves do all the work):**

1. **Public-goods exclusion — applying the small-flow assumption to the mass-flow regime NAS warns against (move 1, sharpened).** Cato assigns immigrants **zero** cost for "pure public goods — the single largest category of spending" (defense, interest, general government), arguing "defense spending is not tied to population growth." [SOURCE: cato.org white-paper, methodology, primary-fetched 2026-06-25] **Honest concession (verified at NAS primary):** this zero-marginal-cost allocation is NOT a fringe trick — it is one of NAS 2016's own eight sanctioned scenarios (scenarios 5-8), and NAS explicitly calls the *average-cost* alternative the assumption that "may overstate the net cost of an additional immigrant." [SOURCE: NAS 2016, ch. 7-8, https://www.nationalacademies.org/read/23550/chapter/13] So the move is defensible in isolation. **The kill is narrower and therefore sharper:** NAS states in the same breath that "for analyses estimating the fiscal impact of … large numbers of arrivals taking place over a multiyear period — the zero marginal cost assumption becomes **less tenable**," because sustained mass inflow *does* eventually require more defense/administration/infrastructure capacity. [SOURCE: NAS 2016, ch. 2, https://www.nationalacademies.org/read/23550/chapter/2] Cato's paper scores **30 years of sustained mass arrival (1994-2023)** — precisely the regime in which NAS says zero-marginal is the *wrong* choice — yet adopts it as the headline. And the magnitude of the swing is enormous and documented: NAS reports that flipping from average-cost to marginal-cost drops the first-generation's share of the deficit from a net cost to "**less than 4 percent**"; in the canonical Borjas vs. Passel-Fix replication, the SAME data go from **+$25B (zero-marginal) to −$16B (average-cost)** — a sign flip driven by nothing but this one assumption. [SOURCE: NAS 2016, ch. 12, https://www.nationalacademies.org/read/23550/chapter/12] Cato never reports the average-cost counterfactual sign in its headline. The honest statement is: "immigrants are net-positive **under the zero-public-goods-cost scenario that NAS flags as untenable for sustained mass inflow**; under NAS's own average-cost baseline the first generation is a net fiscal cost." That is not what "$14.5T surplus" communicates.

2. **Second-generation unit-selection = denominator/unit gerrymander.** Cato counts US-born children of immigrants as **natives** ("natural-born citizens… whatever benefit rules… apply to them") and assigns their K-12 education cost **to the child, not the immigrant parent.** [SOURCE: cato.org white-paper, methodology] This moves the single largest state/local immigrant-origin cost — educating the children of immigrants — **off the immigrant ledger entirely.** It is the mirror image of the favorable move our own ladder entry 45 grants (Colas-Sachs: count the immigrant's GE complementarity *benefit*). Cato takes the benefit-direction unit choice (drop the kid's cost) without the symmetric cost-direction one. NAS's higher fiscal estimates for immigrants come precisely from counting the *adult tax payments* of those same second-generation children; you do not get to bank the descendant's future taxes as a benefit while assigning the descendant's education cost to "a native." The static 30-year window (no NPV) compounds this: it captures the education *cost* years of recent arrivals' kids only partially while crediting the working-age tax years of earlier cohorts — a windowing that flatters whichever side has aged into its tax-paying years inside 1994-2023.

**Net verdict on C3:** the **federal-positive** half is real and matches CBO (grant it). The **"state/local positive / $6.6T surplus"** half is an artifact of (a) excluding public-goods cost and (b) reassigning second-generation education cost off the immigrant unit. Strip either assumption and the state/local ledger moves toward the NAS/CBO finding of net cost concentrated in education. Cato has not refuted NAS/CBO; it has re-run the model on the immigrant-favorable end of two contested allocation choices and reported the corner as the center. **[FRAMING-SENSITIVE]:** the federal/state-local split is the whole game — entry 46 names it explicitly.

---

### C4 — "Immigrants use 21% less welfare per capita": GRANT the datum, KILL the inference

**Steelman:** SIPP 2022 — all immigrants consumed 21% less means-tested welfare + entitlements per capita than natives; noncitizens 54% less; immigrants were 14.3% of population but 11.9% of benefits. [SOURCE: https://www.cato.org/news-releases/immigrants-consume-less-welfare-entitlement-benefits-native-born-americans]

**Verdict: grant the number, kill its use as a fiscal verdict.** Two honest points:
- The number is *real* and useful against the restrictionist "welfare magnet" meme — and Nowrasteh **says so himself**, explicitly: "This new brief is an analysis of the consumption of welfare benefits; it is **not a net-fiscal impact analysis** that considers the consumption of other government services or tax revenue." [SOURCE: alexnowrasteh.com, 2025-02-19] So Cato's *author* concedes the scope limit.
- **The overclaim is in the rhetorical deployment, not the brief.** Welfare/entitlements are ONE cost channel. The expensive immigrant-origin cost at the state/local level is **K-12 education** (NAS, CBO entry 46) — which is not means-tested welfare and is excluded from this 21% figure. Per-capita Medicare/Social Security *also* runs the other way for naturalized immigrants (Cato notes they consume *more* because they're older). Citing "21% less welfare" as if it settles the fiscal ledger is **single-channel ledger-switching (move 1)**: a true sub-ledger presented as the verdict on the whole. [SOURCE: confidence-ladder entry 46]

### C5 — "Build a wall around the welfare state" (keyhole): KILL (political-economy erasure)

**Steelman:** Rather than mass deportation, bar immigrants from means-tested welfare (the Grothman bill / Nowrasteh-Cole proposal); even low-skilled workers then become net taxpayers while the economy keeps their consumer-surplus contribution. [SOURCE: https://www.cato.org/white-paper/fiscal-impact-immigration-united-states, Figure 21]

**Verdict: KILL as a *closure*, grant as design imagination.** This is the Caplan keyhole move and it fails the same way (move 6, political-economy / state-capacity erasure):
- It does **nothing** for the binding state/local costs — K-12 education (constitutionally mandated for all children, *Plyler v. Doe*), shelter, policing. A welfare-access bar cannot touch the cost bucket that actually drives the state/local negative. [SOURCE: confidence-ladder entry 46, SOURCE: research/immigration-bryan-caplan-claims-audit-2026-04-21.md Claim 8]
- It assumes a **credible, durable** exclusion regime. Our rhetorical-failures memo names exactly this: "a keyhole solution that is politically impossible or institutionally non-credible is not a full answer." [SOURCE: research/immigration-bryan-caplan-claims-audit-2026-04-21.md] Means-tested exclusions erode (mixed-status households, emergency Medicaid, EITC mechanics, naturalization). Cato's own Figure 21 is a *counterfactual* ("does not show actual divergent net fiscal impacts") — it is an assumption, not an achieved policy.
- It is **circular with C3**: the fiscal optimism (C3) partly *already assumes* low immigrant welfare use; you cannot both bank "immigrants barely use welfare" as evidence of low cost AND propose walling them off from welfare as the fix for cost. If they barely use it, walling it off recovers little; if walling it off recovers a lot, they were using a lot. [INFERENCE]

### C6 + C7 — Bier on legal-immigration backlogs: GRANT the facts, KILL the macro leap

**Steelman (C6):** Quota waits doubled since 1991 (2y10m → 5y8m); 4.7M+ approved applicants stuck in backlog; 675k would die in line; Indian EB waits exceed a lifetime; the country-cap makes wait a function of birthplace, not merit. [SOURCE: https://www.cato.org/publications/policy-analysis/immigration-wait-times-quotas-have-doubled-green-card-backlogs-are-long]

**Verdict on C6: GRANT — clean descriptive work.** These are FOIA-obtained, primary administrative facts about the *legal* system's internal mechanics. The country-cap producing 9-decade Indian EB waits is a real, documentable absurdity. Like the crime work, this is Cato at its empirical best, and it cuts against the lazy "they should just get in line legally" trope. Nothing to kill in the description.

**Verdict on C7: KILL the macro inference.** Bier's testimony slides from "the legal system is absurdly restrictive" to "the U.S. should approach 1% of population/year (~3.4M green cards) and the skilled-worker gains are near-free." [SOURCE: https://www.cato.org/sites/cato.org/files/2023-09/Bier-Senate-Budget-Committee-Testimony-Final-1.pdf] The backlog facts establish *the current cap is too low*; they do **not** establish *the optimal level is ~1% of population* — that is **marginal-to-mass extrapolation (move 3)** plus **capacity erasure (move 4)**:
- "97% of immigrants who looked for work found jobs" and "immigrants out-work natives at every education level" are **marginal-mover, current-regime** facts. They do not survive automatic extrapolation to a 3× increase in annual flow under stressed housing/school/service capacity — the exact external-validity failure our rhetorical-failures memo flags. [SOURCE: research/immigration-economist-rhetorical-failures-2026-04-22.md, failure mode 3]
- The 1848-1914 "1% of population" benchmark erases that the absorptive machine was different (open frontier, no welfare state, no zoning, no *Plyler* education mandate). A historical ratio is not an absorption guarantee. [INFERENCE]
- **Honest scope:** the *skilled* (EB) backlog argument is the strongest part — high-wage Indian/Chinese workers (wage offers 2.5× US median) facing lifetime waits is close to pure deadweight loss with weak capacity objections. The kill lands on the *blanket* "1% of population" macro target, not on "raise the EB cap / scrap country-caps," which largely survives.

### C8 — Caplan's *Cato Journal* open-borders case: SIGN survives, MAGNITUDE + CLOSURE killed

This is fully audited in two prior memos; summarized here for the consolidated section. Caplan's "Why Should We Restrict Immigration?" (*Cato Journal* 2012) is Cato's house open-borders statement.

**Steelman:** A moral presumption favors free migration; the economic gains are "extremely strong" (place-premium / Clemens tradition, ~double world GDP in the strong literature); standard objections (workers, taxpayers, crime, culture) are overstated; keyhole solutions handle the rest. [SOURCE: research/immigration-bryan-caplan-claims-audit-2026-04-21.md]

**Verdict:**
- **Direction/sign survives** — large global gains from freer movement are real (Clemens, Place Premium, World Bank $1.4T/100M movers). [SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md]
- **"Double world GDP" magnitude — KILLED as a central forecast (move 2, upper-bound laundering).** Every strong paper requires implausible volumes (Clemens: half of poor-country populations move; Bradford: 94-97% of poor-region workforce, which Bradford himself calls "unrealistic"; Iregui: "far from realistic"); the friction-heavy Docquier-Machado-Sekkat model yields only **~4% of world GDP**. The repo's own conservative calibration: +200M migrants → ~1.36% of world GDP, and you need **+3B** to reach Clemens-extreme territory. [SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md]
- **Absorption closure — KILLED (move 4, capacity erasure).** +200M migrants ≈ 80M housing units ≈ 55% of current US housing stock, requiring ~1.9× current US annual housing starts for 30 straight years; housing binds in year 1 in every large-flow scenario. The gains are not fake, but they survive only if destination-capacity erosion stays below a very demanding physical absorption frontier — and the break-even incumbent loss that erases them is only ~$1,071/rich-country-resident/year, "moderate-to-large, not catastrophic." [SOURCE: research/immigration-open-borders-break-even-bounds-2026-04-22.md]
- **Taxpayer/political closure — KILLED (move 6).** Caplan's "restrictions unnecessary to protect taxpayers" fails once federal/state-local are split (same as C3); keyhole solutions don't close housing/school/shelter/credibility (same as C5). [SOURCE: research/immigration-bryan-caplan-claims-audit-2026-04-21.md]
- **Apartheid framing (the OpenBorders.info adjacent rhetoric):** moral analogy partly valid, institutional analogy overstated, "economic evidence: not evidence at all." [SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md]

---

## What survives (the honest concession — the crime work largely survives)

The source-incentive regrade deflates Cato to **0.28** as advocacy — but that weight is the *prior*, and against-interest robustness overrides it where it applies. Here is the honest split:

**SURVIVES (grant — do not contradict the repo's own ladder):**
1. **The TX crime convictions (C1).** Primary administrative data, homicide margin, against the libertarian's own incentive, adopted at confidence-ladder entry 48. This is the single most important concession: a critique that dismissed it would be *wrong* and would contradict our ladder. Scope it to first-gen / authorized-carried / homicide-margin; don't read it as "unauthorized status is protective everywhere."
2. **The federal-side fiscal positive (half of C3).** Matches CBO entry 46 (~+$0.9T over 2024-34, federal). Real.
3. **Immigrants use less means-tested welfare per capita (C4).** Real datum (Nowrasteh's own scope caveat included); kills the "welfare magnet" meme; just isn't a net-fiscal verdict.
4. **The legal-backlog facts (C6) and the skilled-worker / country-cap critique (part of C7).** FOIA-grade administrative facts; the 9-decade Indian EB wait is a real, near-pure-deadweight absurdity.
5. **The directional global-gains claim (part of C8).** Freer movement plausibly offers some of the largest remaining global welfare gains. Sign is right.

**KILLED (the overclaims):**
1. **"Net-positive at the state/local level / $14.5T surplus" (C3 core).** Artifact of (a) zero-public-goods-cost allocation NAS flags as *untenable for sustained mass inflow* and (b) reassigning second-generation education cost off the immigrant unit. Under NAS's own average-cost baseline the first generation is a net fiscal cost concentrated in state/local education — exactly what CBO entry 46 says. This is the headline number and it is the weakest claim.
2. **"Wall around the welfare state" as fiscal closure (C5).** Cannot touch the binding costs (education/shelter/policing); assumes a non-credible durable exclusion regime; circular with C4.
3. **"~1% of population / 3.4M-per-year" as a free-lunch macro target (C7).** Marginal-mover facts extrapolated to mass flow under erased capacity constraints.
4. **"Double world GDP" as a realistic central forecast (C8).** Upper-bound laundering; the honest number is single-digit-percent of world GDP under policy-plausible volumes, bottlenecked by a severe housing-absorption frontier.

**The one-line summary of the whole Cato dismantling:** *Cato's empirical floor (crime convictions, federal fiscal sign, welfare-use snapshot, legal-backlog facts) is solid and partly against-interest — grant it. Cato's macro ceiling (all-government fiscal surplus, open-borders doubling, keyhole closure, 1%-of-population target) is built by taking the immigrant-favorable end of every contested allocation, extrapolation, and political-feasibility choice and reporting the corner as the center.* The fiscal-macro overclaims die on our own CBO/NAS evidence (entries 45-46); the crime work survives on its own against-interest merits (entry 48).

---

*Method note: every Cato brief above was primary-fetched from cato.org on 2026-06-25; the NAS public-goods-allocation mechanism (the load-bearing kill on C3) was verified at the NAS 2016 report primary text (nationalacademies.org/read/23550), not from training memory. Prior-memo conclusions (Caplan audit, open-borders audits, break-even bounds, source-incentive regrade) are cross-referenced, not re-derived.*
