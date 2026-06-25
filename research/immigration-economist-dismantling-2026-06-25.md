# Dismantling the Pro-Immigration Canon — Commentators, Academic Foundations, Popular Books (2026-06-25)

**Commission.** A step-by-step, fundamental dismantling of the major pro-immigration canon, across three
tiers: **Commentators** (Noah Smith, Nicholas Decker, the CATO Institute), **Academic Foundations** (the
Card-Peri wage canon; Michael Clemens's open-borders / Place-Premium canon), and **Popular Books** (Zeke
Hernandez's *The Truth About Immigration*; Abramitzky-Boustan's *Streets of Gold*). Built by seven parallel
teammates (one per target, two dispatch waves), synthesized here. Each target has a full standalone sub-memo;
this document is the synthesis and entry point.

**The frame — and why the FAIR version is the devastating one. [FRAMING-SENSITIVE]**
These authors are pro-immigration optimists. This repo's *own* evidence agrees with them on a great deal —
so a one-sided hit job would be both dishonest and self-contradictory (it would have to deny our own
confidence ladder, which is *built on* the academic foundations dismantled in Tier 2). The dismantling that
actually lands grants what is empirically solid and then surgically kills the **overclaims and rhetorical
moves**. Instrument-bias note (`notes/llm-bias-caveat.md`): the LLM tilt runs *toward* these authors'
conclusions, so where this memo grants them, that grant is load-bearing (verified at primary, ladder 44-51);
where it kills them, the kill is a *specific analytical error*, not a vibe. The fairness keystone is external
and ideologically aligned: **Alexander Kustov**, a self-described cosmopolitan pro-immigration scholar,
independently levels the same select/omit/frame charge against pro-immigration "highbrow misinformation" —
proof the critique is not the instrument's tilt (see Tier 3, Hernandez).

**What we GRANT up front (their valid core — do not relitigate):**
- Immigrant crime is *lower* than native-born — robust across our Light-TX arrests, BJS-SPI incarceration, the 188-spec curve, and (CATO's own) TX convictions. Ladder 42/48.
- The realized 2021-26 surge is fiscally **positive at the FEDERAL level** (CBO −$0.9T). Ladder 46.
- Average native wage effects of observed immigration are **small** — the Borjas-Mariel "10-30% harm" is a ~17-obs/yr artifact (Clemens-Hunt). Ladder 44. *This is Card-Peri's finding, and we adopt it.*
- The lump-of-labor fallacy is real; immigrants are not a fixed-pie subtraction. Ladder 44.
- Legalization *reduces* crime via the jobs channel. Ladder 49.
- The **Place Premium** is real and not a selection artifact; **intergenerational mobility** of immigrants' children is real and large. *These are Clemens's and Abramitzky-Boustan's findings, and we adopt them.*

## The analytical spine — the 6 recurring moves (from `immigration-economist-rhetorical-failures-2026-04-22.md`)

Every overclaim below reduces to one of these. The memo's force is in naming the move precisely each time.
1. **Coordinate-switching / ledger-switching** — answering "average/aggregate GDP" when the question is "marginal, low-skill, distributional, local, or fiscal-at-which-level." *The central error.*
2. **Upper-bound laundering** — citing the most-optimistic estimate as if it were the consensus.
3. **Marginal-to-mass extrapolation** — projecting effects of a small *selected* inflow onto a mass/surge/open-borders inflow.
4. **Capacity erasure** — assuming infinite absorption (housing, schools, institutions) — now *measured*: immigrants concentrate in high-rent, inelastic metros (`msa_fb_rent_panel`, corr +0.74 in inelastic tercile).
5. **Denominator masking** — per-capita vs total, federal vs all-government, gross vs net, relative-rank vs absolute-level.
6. **Political-economy underspecification** — "keyhole solutions" that are politically infeasible; ignoring distribution/backlash/institutional erosion.

## Cross-cutting: the data-capture is itself biased (the classification confound) [FRAMING-SENSITIVE]

Operator-raised, 2026-06-25 — an instrument-level critique (the *coding*, not the analysis) that cuts
the pro-immigration crime claim harder than any analytic point. It applies to ALL seven targets, who
cite "immigrants don't raise crime" without it. Ladder entry 51.

**(a) Hispanic→"white" miscoding.** UCR + many state systems fold Hispanics into "white," inflating the
native/white comparator. Bites our *race-matched* comparison (already deflated — ladder 42, matching to
NH-white natives ~halves the gap), less the *status* comparison (Light-TX keys on status, not race).

**(b) 2nd-generation coded as "native" — structural (birthright citizenship), and DIRECTION-DEPENDENT:**
- **Crime:** 2nd-gen converge toward / exceed 3rd+-gen rates (generational decay — RTI 2024, El Paso
  acculturation). Filing them under "native" **inflates the native baseline → overstates the 1st-gen
  advantage**, which is **first-generation-specific and does not persist** to the US-born children.
- **Fiscal/mobility:** the 2nd-gen are the upside (out-earn/out-pay — Abramitzky-Boustan mobility).
  Crediting that to "native" **understates** the immigrant *dynastic* contribution.
- **THE KILL:** the pro-immigration case uses **inconsistent generational accounting** — first-gen-only
  for crime (foreign-born look best), dynastic for fiscal/mobility (descendants look best). They pick the
  classification that flatters each claim. Coordinate-switching at the *generational* level. Hernandez does
  this *between adjacent chapters of one book*; *Streets of Gold* sits on the dynastic side; CATO does it
  in the fiscal ledger (counting descendants' future taxes as benefit while billing their K-12 to "a native").

**Honest bound:** these deflate MAGNITUDE and restrict the advantage to the 1st generation; they likely
do NOT reverse direction (selection + deportation-deterrence; homicide *convictions* are detection-
resistant and still show foreign-born below native). Light-TX has no generation variable → the confound
is real and largely **unaddressable in current crime data**; the pending CPS 2nd-gen-by-origin test
(`load_cps_second_gen.py`, keyed on *parental* birthplace) is what would settle it. → also belongs in the
crime ladder (sharpens entry 48; recorded as entry 51).

## The central thesis (the one error under all seven)
There is **no single "effect of immigration."** The pro-immigration case wins on the coordinates it
chooses (aggregate GDP, average, federal, national-average crime, steady-state selected inflow,
relative-rank mobility) and goes quiet on the coordinates where the cost concentrates (marginal low-skill,
distributional, state/local education, housing incidence, surge/absorption, composition, political economy,
absolute-level convergence). The dismantling is not "they're wrong" — it's **"they answered a different,
easier question than the one that matters, and presented the answer as if it settled the hard one."**

**The tier structure is itself the finding.** The **Academic Foundations (Tier 2)** are *careful, primary,
and largely granted* — Card-Peri are right about the average native-wage effect; Clemens is right that the
Place Premium is real and mobility is high-leverage; Abramitzky-Boustan are right about rank-mobility. They
are the *rigorous source* of the valid empirics. The **Commentators (Tier 1)** and the **popularizer
(Hernandez, Tier 3)** then **over-deploy** those foundations past the coordinates on which they were
estimated. And the most devastating evidence is *against-interest, from the canon's own primary texts*:
Peri's own model names the losers (previous immigrants −19%); Clemens's own prose concedes the doubling
needs "epic movements"; Abramitzky-Boustan's own review concedes the racialized non-convergence tail and
that their modern data omit the undocumented. **We do not have to refute the foundations to dismantle the
canon — we quote them.**

---

# Tier 1 — Commentators

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

# Tier 2 — Academic Foundations (largely GRANTED; killed only at the over-deployment margin)

## 4. The Card-Peri wage canon — *right about the average, right about the mechanism; misused for "no one is hurt"*
Full: `immigration-dismantle-card-peri-2026-06-25.md`.

This is **the strongest empirical edifice in the corpus, and the repo's own ladder is built on it** — a hit
job here would contradict our own evidence. Card (1990) showed the Mariel 7% labor-force shock had ~no
effect on less-skilled wages; Ottaviano-Peri supplied the mechanism (imperfect substitution / task
complementarity) and the magnitude (average US-born wage **+0.7%**). The repo confirms every load-bearing
piece (Mariel-as-artifact ladder 44; E-Verify null ladder 17; Foged-Peri ladder 19). **GRANT the average
and the mechanism in full.** The canon fails only at three surgical scope-stretches:

- **KILL A (Move 3, on method).** The area-study *design* is read as a clean *general* proof. It isn't:
  native out-migration + capital mobility wash out **40-60%** of the local-vs-national wage gap (Borjas
  w11610, verbatim), so a single-city null under-identifies the national effect. *Borjas's method point is
  valid even though his Mariel magnitude is the ~17-obs artifact — the honest position holds both.*
- **KILL B (Move 5, the central one — exposed by Peri's OWN model).** The small AVERAGE is laundered into
  "no one is hurt." OP's model *reallocates* the loss, it doesn't erase it: verbatim, previous immigrants
  **"lost 19% of their real wages while some groups (i.e., college graduates) lost up to 24%"**; native
  high-school dropouts **−1.1%** long-run (−4.2% under the perfect-substitution methodology). A zero average
  is "the losers were averaged away," not "no losers" — and the elasticity generating the average is itself
  contested (Borjas-Grogger-Hanson: complementarity "evaporates" without HS students). *[parent re-verified
  the −19%/−24%/−1.1% figures against the w12497 PDF after an Exa proxy false-flagged them.]*
- **KILL C (Move 3, on regime).** Marginal/local results are stretched to the 2021-24 **surge** (8.7M above
  baseline, nationwide, concentrated) — exactly where the steady-state mechanism is least reliable and
  there is no comparison city and no 40-60% local escape valve. **Ladder 29 already forbids this
  extrapolation; surge wage estimates remain unrun.**

**Net:** Card-Peri are right that wage-doom is overstated. The kill is three scope-stretches on an
otherwise-granted, repo-confirmed canon — and the central one is quoted from Peri's own paper.

## 5. Michael Clemens — *Place Premium real, mobility high-leverage; "double world GDP" is an upper-bound slogan*
Full: `immigration-dismantle-clemens-2026-06-25.md`.

Clemens is the **most empirically careful** figure in this memo, and the **fairness anchor**: the repo
*adopts* his Mariel reconciliation (Clemens-Hunt 2019, ladder 44 — the work that established Borjas's
Mariel harm as a compositional artifact). **GRANT** the Place Premium (location explains most of the wage
gap for identical workers; selection modest 1.0-1.3 — kills the "ambitious self-select" objection, VERIFIED);
**GRANT** that migration gains are plausibly among the largest remaining global efficiency gains (World Bank:
100M movers → $1.4T/yr); **GRANT** that mobility is unusually high-leverage.

**The single most decisive kill is Clemens's OWN later model.** Clemens-Pritchett (2019, *JDE* 138:153-164)
formalizes an **interior optimum** migration rate (origin-TFP transmission × assimilation × congestion) and
concludes, verbatim, that "dynamically efficient policy would **NOT** imply open borders but would imply
**relaxations on current restrictions**." So the doubling slogan fails not merely against the friction-heavy
rival literature — **it fails against Clemens's own model**, and the repo's stance (direction yes,
mass-absorption no, optimum = relaxation) *is* Clemens's published 2019 position. The overclaim is the
*popularizers'* (Caplan, openborders.info), not Clemens's. [verified at primary, conf 1.0] Then **KILL** the
"open borders ≈ doubles world GDP" slogan as a central forecast on four further moves:

- **Move 2 (upper-bound laundering):** the 50-150% range is the *upper-bound model literature*; the omitted
  counterweight — Docquier-Machado-Sekkat — prices the frictions (moving costs, congestion, imperfect
  substitution, networks) and gets **~4% of world GDP** long-run.
- **Move 1 (ledger-switching):** the slogan compresses GDP, welfare-equivalent, and consumption-equivalent
  estimates into one literal-GDP object.
- **Move 3 (marginal-to-mass):** the doubling needs movements the modelers call unrealistic — Clemens's own
  "epic movements" (≥½ poor-country populations); Bradford's +75% needs **94-97% of the poor-region
  workforce** to move, which *he* calls "unrealistic."
- **Move 4 (capacity erasure):** repo calibration — +200M → 1.4%, +1B → 6.8%, **+3B for doubling territory**;
  housing **binds in year 1** (capacity ~3.5M/yr vs 10M+ arrivals); immigrants concentrate in the *least*
  elastic metros (corr −0.41).

The kill lands on the **popularized deployment** (openborders.info's literal "double world GDP"), **not** on
Clemens's hedged prose, which is more honest than the slogan that quotes him.

---

# Tier 3 — Popular Books

## 6. Zeke Hernandez, *The Truth About Immigration* (2024) — *four pillars granted; "The TRUTH" oversells a coordinate-restricted answer*
Full: `immigration-dismantle-hernandez-2026-06-25.md`.

**GRANT four of five pillars** (innovation/talent — the 1924 National Origins Act natural experiment is
clean; entrepreneurship; crime-direction with his own honest caveats; federal-fiscal magnitude; the
demographic argument). The danger here is *excess agreement* (the instrument's prior aligns with him), so
every grant is repo-tied and every kill is a coordinate/incidence charge on data:

- **The generational frame-switch (Move 1, sharpened by ladder 51) — the key kill.** Hernandez *does*
  address the generational fiscal ledger honestly (names the −$1,600 1st-gen state cost, the 2-to-1
  descendant ROI), so the naive "treats 1st-gen as permanent" charge *fails*. The real kill: he runs the
  **dynastic frame for fiscal** (count descendants → ledger flips positive) and the **first-gen frame for
  crime** (advantage that decays by 2nd gen) — opposite generational conventions on adjacent chapters, each
  chosen to come out positive.
- **"Newcomers Fill Public Coffers" (Move 1+6):** the chapter title erases the state-local cost his own
  −$1,600 number establishes, and the 2023 surge was state-local net-NEGATIVE (CBO 61256).
- **Housing-incidence omission (Move 4):** rents appear nowhere as a pillar or conceded catch; Wilson-Zhou
  (+1.4% rents, ladder 50) + the repo panel (fb↔rent +0.74 inelastic) are the omitted renter side.
- **Composition universalization (Move 3):** the sign is composition/skill/welfare-regime-dependent
  (Dustmann-Frattini ladder 47: UK EEA +34% vs non-EEA negative, *same country*).
- **The title meta-kill + fairness keystone:** "The TRUTH … overwhelmingly positive on EVERYTHING" sells a
  coordinate-dependent question as settled. **Kustov** (cosmopolitan pro-immigration scholar) independently
  calls this "highbrow [pro-immigration] misinformation" — *"misleads by how it selects, omits, and frames
  facts … technically defensible … yet a significant distortion"* — **proof the charge is not the
  instrument's tilt.** *[parent corrected the attribution: "highbrow misinformation" is Dan Williams' term
  that Kustov endorses and applies to immigration; the load-bearing keystone — a pro-immigration scholar
  leveling the select/omit/frame charge — is verified on-page and unaffected.]*

## 7. Abramitzky & Boustan, *Streets of Gold* (2022) — *rank-mobility granted; "immigrant SUCCESS" as a universal property over-reaches*
Full: `immigration-dismantle-streets-of-gold-2026-06-25.md`.

The repo *uses* their AER 2021 intergenerational-mobility paper as a landmark. **GRANT** the headline
(children of poor immigrants out-mobilize children of poor natives, then and now, on rank-rank, nearly all
sending countries); **GRANT** the myth-puncture (yesterday's feared groups assimilated) and the
lump-of-labor refutation (ladder 44). **KILL** the *generalization the title sells* — built substantially
from the authors' OWN against-interest admissions (PNAS Nexus 2024 review, re-verified at primary):

- **Metric masking (Move 5):** "out-mobilize" is *relative-rank* ascent from a low origin, not
  *absolute-level* parity; the book's "success" rhetoric invites the reader to hear level success.
- **External validity (Move 3/4):** "then and now" replicates one *statistic*, not the *absorption
  environment* — no 1900 welfare state, open frontier, or pre-civil-rights racial order. Authors concede the
  modern tax data **"do not contain undocumented immigrant parents"** — the present inflow most relevant to
  the fiscal/housing debate is invisible to their modern half.
- **Classification confound (ladder 51):** the success story rests on the 2nd-gen being coded "native"; the
  most-assimilated descendants *attrit out* (ethnic attrition, Duncan-Trejo) or get *recoded native*
  (birthright citizenship). Authors *acknowledge* (citing Villarreal-Tamborini) a Hispanic/Black 2nd-gen
  non-convergence tail and reframe it as "racial inequality" while pivoting to the relative-rank coordinate;
  their *own* AER data carries persistent-gap cases (Jamaican/Haitian/Mexican 2nd-gen). *[parent corrected:
  the non-convergence sentence is A&B citing V-T, not their own estimate; both verified at primary,
  SemScholar mirror of pgae344.]*
- **Selection-not-treatment (Move 3):** the advantage runs partly through *selection of who emigrates* +
  *geographic sorting* (the AER 2021 mechanism) — their own boundary condition on the universal claim; they
  concede they "lack household-level data to evaluate geography in the modern period."

---

## What survives — the honest close (be specific; the memo's credibility lives here)

All seven are pro-immigration optimists, and a large fraction of what they say is **correct and
repo-confirmed**. State it plainly:
1. **Immigrants (1st-gen) have lower crime than natives** — direction robust (Light, SPI, the 188-spec curve, CATO's own convictions). Ladder 42/48. *Granted by all; it's our finding too.*
2. **The realized federal surge is fiscally positive** — CBO −$0.9T, +$8.9T GDP, + Colas-Sachs's +$750/yr indirect channel. Ladder 45-46.
3. **Average native-wage effects of observed inflows are small** — Card-Peri's +0.7% average; the Mariel "10-30% harm" is a ~17-obs/yr artifact (Clemens-Hunt). The lump-of-labor fallacy is real. Ladder 44.
4. **High-skill immigration is strongly net-positive**; the **Place Premium** is real (Clemens, selection modest); the global/origin gains are directionally large; brain-drain doom is overstated. *And the open-borders optimum is a substantial relaxation, not open borders — which is Clemens's OWN 2019 model (Clemens-Pritchett), not a critique imposed on him.*
5. **Intergenerational mobility of immigrants' children is real and large** (Abramitzky-Boustan rank-mobility, repo-adopted); the "old good / new bad" nostalgia is empirically wrong.
6. **Immigration did NOT drive the recent rent spike or the 2023 disinflation** — our growth-margin rent null (−0.17) + JCHS/Yale-Budget-Lab back Smith and Decker on the *national-aggregate-causation* question.

**What does NOT survive is the impression their corpora leave:** that the **local-incidence,
distributional, state/local-fiscal, capacity, composition, and absolute-convergence** questions are
settled-small. They are real, measured (rent incidence +1.4% and concentrated in the inelastic metros where
immigrants actually live; school-age-children intensity; state/local education cost; the racialized
downward-mobility tail), and they fall on renters, competing low-skill workers, prior immigrants, and
receiving cities.

**The one error under all seven (the central thesis, now evidenced):** they win on the coordinates they
pick — *aggregate* GDP, *average* native, *federal* ledger, *national-average* crime, *steady-state
selected* inflow, *relative-rank* mobility — and present that win as settling the coordinates where the cost
concentrates — *marginal low-skill*, *distributional*, *state/local*, *surge-absorption*, *composition*,
*absolute-level*. It is **coordinate-switching**, and — per the operator's instrument critique — it runs down
to the **generational accounting**: first-gen framing where it flatters crime, dynastic framing where it
flatters fiscal/mobility. CATO's $14.5T claim, Smith's two registers, Hernandez's adjacent-chapter
frame-switch, and *Streets of Gold*'s relative-rank retreat are the **same move at different scales**. The
dismantling is devastating precisely because it grants their valid empirics — and shows the reassurance is an
artifact of which question got answered. **We dismantle the canon by quoting its own primary texts.**

**Pre-publication caveat (mandatory before any external use):** every *direct quote* in the seven sub-memos
was fetched by a teammate and tagged verbatim — quotes are the weapon, so **re-verify each at primary before
publishing.** Verification done this pass (intern-rule spot-checks on the four Tier-2/3 targets, all
load-bearing): **(i)** Card-Peri's −19%/−24%/−1.1% distributional figures — re-checked against the actual
w12497 PDF (an Exa proxy had false-flagged them as not-in-paper); **(ii)** *Streets of Gold*'s "do not
converge" sentence — verified verbatim at primary (SemScholar mirror of PNAS Nexus pgae344), attribution
corrected (A&B *citing* Villarreal-Tamborini); **(iii)** Hernandez's Kustov keystone — verified on-page,
attribution corrected (Williams' term, Kustov applies it) and one unverified verbatim quote downgraded to
paraphrase. The one load-bearing external *fact* checked in Tier 1 (CBO GDP-per-person −0.8%) verified at
0.95; the inventor-share figures (Decker §2; Hernandez pillar 2) are flagged direction-granted, not
primary-verified.

## Integration log
- [x] dismantle-smith — integrated (two-registers / ledger-switching at corpus scale)
- [x] dismantle-decker — integrated ("must" quantifier error; double-world-GDP self-refutation; CBO per-person verified)
- [x] dismantle-cato — integrated (floor granted incl. crime; $14.5T ceiling killed on public-goods + 2nd-gen-as-native)
- [x] dismantle-card-peri — integrated (average + mechanism granted; 3 scope-stretches killed; −19%/−24%/−1.1% re-verified at primary)
- [x] dismantle-clemens — integrated (Place Premium granted, Mariel rigor adopted; "double world GDP" killed by Clemens's OWN 2019 interior-optimum model; parent built the base from repo audit, then integrated 3 primary-verified teammate upgrades — the teammate raced-and-deferred, did not stall)
- [x] dismantle-hernandez — integrated (4 pillars granted; generational frame-switch + housing omission + title meta-kill; Kustov keystone verified+corrected)
- [x] dismantle-streets-of-gold — integrated (rank-mobility granted; metric/external-validity/classification/selection kills from authors' own admissions; pgae344 verified+corrected)
