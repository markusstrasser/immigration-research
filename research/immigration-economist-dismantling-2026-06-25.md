# Dismantling the Pro-Immigration Economists — Smith, Decker, CATO (2026-06-25)

**Commission.** A step-by-step, fundamental dismantling of the immigration arguments of **Noah Smith**,
**Nicholas Decker**, and the **CATO Institute**. Built by three parallel teammates (one per target),
synthesized here.

**The frame — and why the FAIR version is the devastating one. [FRAMING-SENSITIVE]**
These three are pro-immigration optimists. This repo's *own* evidence agrees with them on several
empirics — so a one-sided hit job would be both dishonest and self-contradictory (it would have to deny
our own confidence ladder). The dismantling that actually lands grants what is empirically solid and then
surgically kills the **overclaims and rhetorical moves**. Instrument-bias note (`notes/llm-bias-caveat.md`):
the LLM tilt runs *toward* these authors' conclusions, so where this memo grants them, that grant is
load-bearing (verified at primary, ladder 44-50); where it kills them, the kill is a *specific analytical
error*, not a vibe.

**What we GRANT up front (their valid core — do not relitigate):**
- Immigrant crime is *lower* than native-born — robust across our Light-TX arrests, BJS-SPI incarceration, the 188-spec curve, and (CATO's own) TX convictions. Ladder 42/48.
- The realized 2021-26 surge is fiscally **positive at the FEDERAL level** (CBO −$0.9T). Ladder 46.
- Average native wage effects of observed immigration are **small** — the Borjas-Mariel "10-30% harm" is a ~17-obs/yr artifact (Clemens-Hunt). Ladder 44.
- The lump-of-labor fallacy is real; immigrants are not a fixed-pie subtraction.
- Legalization *reduces* crime via the jobs channel. Ladder 49.

## The analytical spine — the 6 recurring moves (from `immigration-economist-rhetorical-failures-2026-04-22.md`)

Every overclaim below reduces to one of these. The memo's force is in naming the move precisely each time.
1. **Coordinate-switching / ledger-switching** — answering "average/aggregate GDP" when the question is "marginal, low-skill, distributional, local, or fiscal-at-which-level." *The central error.*
2. **Upper-bound laundering** — citing the most-optimistic estimate as if it were the consensus.
3. **Marginal-to-mass extrapolation** — projecting effects of a small *selected* inflow onto a mass/surge/open-borders inflow.
4. **Capacity erasure** — assuming infinite absorption (housing, schools, institutions) — now *measured*: immigrants concentrate in high-rent, inelastic metros (`msa_fb_rent_panel`, corr +0.74 in inelastic tercile).
5. **Denominator masking** — per-capita vs total, federal vs all-government, gross vs net.
6. **Political-economy underspecification** — "keyhole solutions" that are politically infeasible; ignoring distribution/backlash/institutional erosion.

## Cross-cutting: the data-capture is itself biased (the classification confound) [FRAMING-SENSITIVE]

Operator-raised, 2026-06-25 — an instrument-level critique (the *coding*, not the analysis) that cuts
the pro-immigration crime claim harder than any analytic point. It applies to ALL three targets, who
cite "immigrants don't raise crime" without it.

**(a) Hispanic→"white" miscoding.** UCR + many state systems fold Hispanics into "white," inflating the
native/white comparator. Bites our *race-matched* comparison (already deflated — ladder 42, matching to
NH-white natives ~halves the gap), less the *status* comparison (Light-TX keys on status, not race).

**(b) 2nd-generation coded as "native" — structural (birthright citizenship), and DIRECTION-DEPENDENT:**
- **Crime:** 2nd-gen converge toward / exceed 3rd+-gen rates (generational decay — RTI 2024, El Paso
  acculturation). Filing them under "native" **inflates the native baseline → overstates the 1st-gen
  advantage**, which is **first-generation-specific and does not persist** to the US-born children.
- **Fiscal:** the 2nd-gen are the upside (out-earn/out-pay — Abramitzky mobility). Crediting that to
  "native" **understates** the immigrant *dynastic* contribution.
- **THE KILL:** the pro-immigration case uses **inconsistent generational accounting** — first-gen-only
  for crime (foreign-born look best), dynastic for fiscal (descendants look best). They pick the
  classification that flatters each claim. Coordinate-switching at the *generational* level.

**Honest bound:** these deflate MAGNITUDE and restrict the advantage to the 1st generation; they likely
do NOT reverse direction (selection + deportation-deterrence; homicide *convictions* are detection-
resistant and still show foreign-born below native). Light-TX has no generation variable → the confound
is real and largely **unaddressable in current crime data**; the pending CPS 2nd-gen-by-origin test
(`load_cps_second_gen.py`, keyed on *parental* birthplace) is what would settle it. → also belongs in the
crime ladder (sharpen entry 48).

## The central thesis (the one error under all three)
There is **no single "effect of immigration."** The pro-immigration case wins on the coordinates it
chooses (aggregate GDP, average, federal, national-average crime, steady-state selected inflow) and goes
quiet on the coordinates where the cost concentrates (marginal low-skill, distributional, state/local
education, housing incidence, surge/absorption, political economy). The dismantling is not "they're wrong"
— it's **"they answered a different, easier question than the one that matters, and presented the answer
as if it settled the hard one."**

---

## 1. Noah Smith — *ledger-switching at corpus scale (self-sourced)*
Full: `immigration-dismantle-noah-smith-2026-06-25.md`.

**The master key: Smith has TWO registers and never reconciles them.** *Register A* (the reassuring
"evidence" essays — *Why immigration doesn't reduce wages*, *Mass deportation would accomplish nothing*)
deploys steady-state / average / national-aggregate machinery: "the total effect on wages is…not much,"
cost-of-living "relatively small." *Register B* (*America, please be reasonable*, 2024-01) concedes the
exact opposite in his own words: the surge is **"a massive problem… a long-term fiscal problem, because
these people will require heavy government support for their health care, housing, and education; this
will end up coming from city and state governments,"** and low-skill mass inflow is "an altruistic luxury."
He has the federalism split *exactly right in Register B* — then writes Register A as if he didn't. The
dismantling is not "Smith is wrong" (mostly he isn't); it's **"his reassuring essays answer the
national-average question and let the reader believe they answered the local-incidence question — which
his own honest essay concedes they don't."**

| # | Claim | Empirics | Move that kills the overclaim |
|---|---|---|---|
| 1 | No native-wage cut | **SOLID on average** | (3) marginal→mass + (5) avg masks distribution |
| 2 | Cost-of-living small | **OVERCLAIM** | (4)+(5) netting masks regressive renter-incidence — *now measured* (+1.4% rents; fb-share↔rent +0.74 in inelastic tercile) |
| 3 | Unrelated to inflation | **SOLID (claim he defends)** | (1) minor headline→shelter-CPI switch |
| 4 | Net fiscal positive | **SOLID federally** | (1) federal→state/local switch he makes correctly in Register B then drops |
| 5 | Lower crime | **SOLID, repo-confirmed** | quotes inflated non-race-matched magnitude; omits first-gen-decay (weak hit) |
| 6 | Deportation accomplishes nothing | **MOSTLY SOLID** | (3) "nothing" is an absolute his own Register B + the BEA sim contradict |

## 2. Nicholas Decker — *right about the mechanisms, wrong about the welfare conclusion*
Full: `immigration-dismantle-decker-2026-06-25.md`.

Decker's move is methodological: the anti-immigration ledgers assume constant returns to scale (CRS),
which is "obvious nonsense" given increasing returns (specialization/ideas/fixed costs); therefore
immigrants "**must** make us richer." **Grant the CRS critique** — the repo's Colas-Sachs vindication
(+$750/yr indirect benefit via complementarity, ladder 45) is exactly the hole in the static ledger he
points at. **Kill the word "must":** it silently swaps *aggregate output* (where IRS operates) for
*incumbent per-capita welfare*. The counterexample he says can't exist is the official scorekeeper's
own projection — **CBO 2024: real GDP per person ~0.8% LOWER by 2034 even as aggregate GDP rises**
([VERIFIED at primary, conf 0.95]). His "double world GDP" headline is upper-bound laundering **caught
in his own text** — two paragraphs later he writes the structural estimates "are likely high… if labor
is not identical, this breaks down… the most skilled people [move] first" — and uses the doubling figure
anyway (the honest number is single-digit-% of world GDP at policy-plausible volumes — Docquier ~4%).
And "the only coherent objection is voting" is flatly false: CBO 2025 scored the coherent *economic*
(state/local fiscal-incidence) objection at −$9.2B. **Granted hard:** high-skill immigration is strongly
net-positive (Claim 4 — conceded, not quibbled). Self-flagged GAP: the 23%/36% immigrant-inventor figures
are direction-granted but not primary-verified.

## 3. CATO Institute — *solid empirical floor (partly against-interest), overreaching macro ceiling*
Full: `immigration-dismantle-cato-2026-06-25.md`.

The honest split a one-sided memo can't make: **GRANT CATO's floor** — the TX homicide-conviction series
(Nowrasteh PA977: illegal −26% vs native; primary admin data, detection-resistant margin, *against the
libertarian's own interest*, **adopted at our ladder entry 48**); the federal fiscal positive (CBO); the
"21% less welfare/capita" datum (Nowrasteh's own scope caveat: "not a net-fiscal analysis"); the
legal-backlog facts (Bier: 9-decade Indian EB waits — near-pure deadweight). **Kill the ceiling** — the
flagship **"$14.5T net positive, +$6.6T at state/local"** dies on two allocation choices: (a) assigning
immigrants **zero** public-goods cost — a NAS scenario NAS *itself* flags as "less tenable" for sustained
mass inflow, and the swing is a documented sign-flip (NAS: average-cost drops the 1st-gen deficit share to
"<4%"; +$25B→−$16B in the canonical replication); (b) **counting US-born children as "natives" and
assigning their K-12 cost to the child, not the immigrant** — moving the largest state/local
immigrant-origin cost off the ledger. **(b) is the operator's 2nd-gen-as-native confound, fiscal
direction — independently re-derived here:** you cannot bank the descendants' future taxes as the
benefit while billing their education cost to "a native." Strip either assumption → state/local moves to
the NAS/CBO net-cost-in-education finding (ladder 46). "Wall around the welfare state" (keyhole) can't
touch the binding costs (education/*Plyler*, shelter) and is circular with the low-welfare-use claim.

---

## What survives — the honest close (be specific; the memo's credibility lives here)

All three are pro-immigration optimists, and a large fraction of what they say is **correct and
repo-confirmed**. State it plainly:
1. **Immigrants (1st-gen) have lower crime than natives** — direction robust (Light, SPI, the 188-spec curve, CATO's own convictions). Ladder 42/48. *Granted by all three; it's our finding too.*
2. **The realized federal surge is fiscally positive** — CBO −$0.9T, +$8.9T GDP, + Colas-Sachs's +$750/yr indirect channel. Ladder 45-46.
3. **Average native-wage effects of observed inflows are small** — the Mariel "10-30% harm" is a ~17-obs/yr artifact (Clemens-Hunt). The lump-of-labor fallacy is real. Ladder 44.
4. **High-skill immigration is strongly net-positive**; the global/origin gains are directionally large; brain-drain doom is overstated.
5. **Immigration did NOT drive the recent rent spike or the 2023 disinflation** — our growth-margin rent null (−0.17) + JCHS/Yale-Budget-Lab back Smith and Decker on the *national-aggregate-causation* question.

**What does NOT survive is the impression their corpora leave:** that the **local-incidence,
distributional, state/local-fiscal, capacity, and composition** questions are settled-small. They are
real, measured (rent incidence +1.4% and concentrated in the inelastic metros where immigrants actually
live; school-age-children intensity; state/local education cost), and they fall on renters, competing
low-skill workers, and receiving cities.

**The one error under all three (the central thesis, now evidenced):** they win on the coordinates they
pick — *aggregate* GDP, *average* native, *federal* ledger, *national-average* crime, *steady-state
selected* inflow — and present that win as settling the coordinates where the cost concentrates —
*marginal low-skill*, *distributional*, *state/local*, *surge-absorption*, *composition*. It is
**coordinate-switching**, and — per the operator's instrument critique — it runs down to the **generational
accounting**: first-gen framing where it flatters crime, dynastic framing where it flatters fiscal. CATO's
$14.5T claim and Smith's two registers are the same move at different scales. The dismantling is devastating
precisely because it grants their valid empirics and then shows the reassurance is an artifact of which
question got answered.

**Pre-publication caveat (mandatory before any external use):** every *direct quote* in the three sub-memos
was fetched by a teammate and tagged verbatim, but quotes are the weapon — **re-verify each at primary
before publishing.** The one load-bearing external *fact* checked here (CBO GDP-per-person −0.8%) verified
at 0.95; the inventor-share figures (Decker §4) are flagged unverified.

## Integration log
- [x] dismantle-smith — integrated (two-registers / ledger-switching at corpus scale)
- [x] dismantle-decker — integrated ("must" quantifier error; double-world-GDP self-refutation; CBO per-person verified)
- [x] dismantle-cato — integrated (floor granted incl. crime; $14.5T ceiling killed on public-goods + 2nd-gen-as-native)
