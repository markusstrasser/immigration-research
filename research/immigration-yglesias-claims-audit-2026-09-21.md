# Matthew Yglesias on immigration: claims audit, 2026-09-21

**Verdict:** Yglesias is the least exposed of the commentators audited so far, because he has
already conceded in his own dated words most of what this repo measures for low-skill
immigration: less-educated immigrants are "less economically beneficial" (2021), the housing
argument is "factually accurate" (2025), large asylum inflows are "undesirable" (2023), Biden
"failed so badly" (2025), and assimilation needs work rather than reassurance (2026). Three
things remain unsupported. The 2020 book's universals ("immigrants of virtually all stripes …
make native-born Americans richer", immigration "would cost taxpayers nothing") were never
marked as withdrawn and do not hold for the low-education, Mexico-born stripe on our fiscal
account. His reading of Borjas as conceding gains "for native-born American workers" overstates
what Borjas wrote. And his fiscal remedy, "building a wall around the welfare state", targets
transfers, while our status split shows the gap is about the same for people already excluded
from most of them. He states no fiscal number in his own voice; the CBO material on Slow Boring
sits in guest posts. [INFERENCE from the graded rows below]

Scope: 40 claims and 15 concessions from 15 primary pieces (2020-08 to 2026-07) collected by
two reader agents under [`BRIEF.md`](../infra/immigration-fiscal/yglesias_claims_2026_09_21/BRIEF.md),
every quote checked against a cached copy of his own text:
[economic claims](../infra/immigration-fiscal/yglesias_claims_2026_09_21/notes/economic_claims.md) (rows E- and C-),
[crime, asylum and assimilation claims](../infra/immigration-fiscal/yglesias_claims_2026_09_21/notes/social_claims.md)
(rows S-; its concessions C-01 to C-09 are written SC- here to keep them apart). Five of the
pieces are paywalled and were read only as free previews.
Two pieces were already held ([media audit](immigration-media-perspectives-audit-2026-09-20.md), rows C1–C2).
Grading follows the [scorecard's September 19 rule](immigration-claim-scorecard-2026-09-18.md):
a measurement on a different population, horizon or outcome cannot refute a claim.

Grades: **AGREE** = the repo's evidence supports it as stated. **SCOPE** = true on the axis he
states, silent or false on the low-skill, descendant or state-and-local axis. **NOT SUPPORTED** =
contradicted by a repo measurement on a matched population. **LOOSE** = misstates its own source.
**OPEN** = checkable, not checked here. No tallies are given; rows differ too much in weight.

## 1. His case at its strongest

Yglesias's argument for more immigration is about scale, not budgets: a larger population gives
the United States more innovators, deeper markets and the weight to stay ahead of China (*One
Billion Americans*; E-20, 2025: "by far America's best chance to remain the number one power").
He holds that area wage studies miss "the outsized impact of super-achievers among immigrants,
and critically, among the children of immigrants" (E-07). A resident fiscal account prices none
of that. Nothing below tests the national-power case, and the innovation case applies mostly to
the high-skill inflow, where this repo agrees with him. [FRAMING-SENSITIVE]

## 2. Graded claims

### Fiscal

| Claim | Evidence here | Grade |
|---|---|---|
| E-01 (2020): "Immigrants of virtually all stripes … make native-born Americans richer" | On the education-by-origin account Mexico-born adults run −$2,282 per adult-year (−$3,483 to −$1,080) on the personal allocation and −$5,410 shared, before institutional costs and average public goods [CALCULATION: [`origin_screen.csv`](../infra/immigration-fiscal/high_skill_origin_screen_2026_09_21/derived/origin_screen.csv)]; below-high-school −$1,951, high-school-only +$522 [[education results](../infra/immigration-fiscal/education_origin_fiscal_2026_09_19/RESULT.md)]. For the whole Mexican-origin population the complete account puts the net cost to other residents at $165–197bn a year against a production gain of $8.8–13.3bn, positive only if under 18.5–25.8% of assigned service costs respond [[complete account](immigration-complete-annual-account-2026-09-20.md)]. The ledgers measure budgets and production, not innovation. | NOT SUPPORTED as a universal, on the fiscal axis, for the low-education stripe. He narrowed it himself in 2021 (E-08) without withdrawing it. |
| E-04 (2020): housing reform, "like immigration — would cost taxpayers nothing" | Federal, all origins: CBO's July 2024 report projects about $0.9tn lower federal deficits over 2024–2034 from the surge ([Smith audit](immigration-dismantle-noah-smith-2026-06-25.md)). State and local: CBO 2025 scores the incidence at −$9.2bn (scorecard row D3). Low-education residents: rows above. | SCOPE |
| SC-07 (2025): "'building a wall around the welfare state' to make sure that immigration is fiscally beneficial" | Imputed-unauthorized Mexico-born adults, already excluded from most transfers, run −$7,806 against third-plus whites; imputed-legal −$8,166 (ladder 85, imputed status, Medicaid outside that balance). If exclusion from transfers closed the gap, the excluded group would show a smaller one; it does not, so the gap sits mainly in lower taxes and in services no eligibility rule removes, such as schooling [INFERENCE]. | The remedy does not reach most of the measured gap. The concession that the fiscal benefit is conditional is AGREE. |
| Fiscal numbers attributed to him | None found in his own voice. "Higher immigration levels would boost GDP and reduce the federal budget deficit" is Jed Kolko's guest post (2024-09-12); the CBO/JCT dynamic score is Elmendorf and Williams's (2023-08-28). | Attribution note |

### Skill

| Claim | Evidence here | Grade |
|---|---|---|
| E-08 (2021): "less-educated immigrants are both less economically beneficial … than skilled ones" | Education gradient above; India-born adults +$29,174 (ladder 168; ladder 150 on the earlier account). | AGREE |
| E-15, E-17 (2025): H-1B workers earn well above average; pay rises two- to six-fold on moving | High-skill fiscal sign agreed (ladder 150; media audit C2, where the $100,000-fee job-loss certainty is overstated). The pay multiple is Clemens's, not checked here. | AGREE on sign; OPEN on the multiple |
| E-16 (2025): the legal system is "good enough", make it larger; the diversity lottery "admits a pool … with a higher skill profile than the population average" | Degrees do not convert equally: Venezuela-born degree holders pay $19,402 a year less than native degree holders and Pakistan/Bangladesh-born $12,947 less, India-born $7,545 more (ladder 168). The lottery claim is not in the repo. | OPEN; "larger" is not neutral to who comes |
| E-09 (2021): "the current flow … is already highly educated" | Not tabulated here for 2021; the 2021–2024 inflow differs in composition (CPS covers 3.9m of CBO's 8.7m arrivals, ladder 85). | OPEN |

### Wages and prices

| Claim | Evidence here | Grade |
|---|---|---|
| E-05, E-14, E-19: labour-market competition is a small problem; the working-class-harm perception is not true | Average native wage effects are small (scorecard S1; ladder 44). The canon audit notes bottom-decile declines in Dustmann–Frattini–Preston and negative low-skill results in Card 2001. He addresses wages, not local budgets; he concedes housing (C-04). | AGREE on average wages; SCOPE for "working class" |
| E-06 (2021): Borjas "concedes that immigration has net benefits for native-born American workers" | Borjas 1995, abstract: "Natives benefit from immigration mainly because of production complementarities between immigrant workers and other factors of production … small, on the order of $6 billion and almost certainly less than $20 billion annually" [SOURCE: https://www.aeaweb.org/articles?id=10.1257/jep.9.2.3]. The surplus goes to natives as owners of other factors, not to workers as a class; Yglesias's next sentence grants that "the distribution of the benefits is skewed". | LOOSE |
| E-11 to E-13 (2021): low-skill labour holds down grocery and service prices and frees high-wage native women to work more (Cortés–Tessada) | Both channels are real and identified. At face-value elasticities they come to about $22bn a year, 7.5% of the reference gap; the fiscal part is $8.7bn (ladder 132). | AGREE in sign; bounded in size |
| E-10 (2021): make-up visas "would greatly expand the country's productive capacity" | True of aggregate output. Says nothing per resident; CBO's per-person figure includes the newcomers and cannot settle incumbent gains either way (scorecard correction D1). | AGREE on the aggregate |

### Housing

| Claim | Evidence here | Grade |
|---|---|---|
| C-04 (2025): "The more immigrants we have, the more housing scarcity pinches" | Foreign-born share to rent +0.74 in the supply-inelastic tercile; +1.4% on the growth margin; incidence on renters (scorecard S2). | AGREE |
| C-05 (2025): skilled immigration is worse for housing than unskilled | The rent panel is not split by skill. | OPEN |

### Crime

| Claim | Evidence here | Grade |
|---|---|---|
| S-01 (2025): "immigrants commit crimes at lower rates than native-born Americans, which is true" | First generation: agreed on the conviction margin, a result carried by legal immigrants (ladder 48). He says nothing about descendants; our descendant contrasts carry the [September 20 measurement rule](immigration-detention-crime-and-fiscal-scope-2026-09-20.md) and do not identify offending. | AGREE as stated |
| S-02 (2025): a million arrivals will not commit zero crimes, "in that sense immigration makes crime worse" | Arithmetic. It is also the honest form of the argument: counts, victims and costs scale with population even at a lower rate. | AGREE |
| Hispanic incarceration statistics attributed to him | The one Slow Boring post carrying Hispanic-versus-white incarceration statistics (`/p/hispanic-prison`, 2021-08-28) is a guest post by Keith Humphreys [SOURCE: cached page, `<meta name="author" content="Keith Humphreys">`]. Nothing in it is Yglesias's claim; it remains usable as a source in its own right. | Attribution note |

### Assimilation

| Claim | Evidence here | Grade |
|---|---|---|
| SC-09 (2026): "immigrants to the United States do in fact assimilate very well" (Boustan), with the caveat that liberals must "make sure that it happens" | Conditional income mobility in *Streets of Gold* survives audit ([memo](immigration-dismantle-streets-of-gold-2026-06-25.md)). On our ledger the Mexican-origin second and third-plus generations still run −$7,521 and −$6,195 per person against third-plus non-Hispanic whites at common ages [DATA: `ledger_absolute_2026_09_17/derived/complete_gaps.csv`]. Per-capita income rose from 0.52 to 0.61 of the national figure, flat from 2008 to about 2016 and rising since; household income and earnings paused in 2024 (ladder 163). One cross-section is not a lineage forecast, and 11% of the third generation no longer identifies as Mexican (ladder 158). | SCOPE: mobility given parents' rank, yes; convergence to parity for this lineage, not observed |

### Outside our measurements

Asylum procedure, deterrence and enforcement (S-05, S-06, S-09 to S-15), public opinion (S-03,
S-17, S-18) and the 2024 election counterfactual (S-07) are not graded. S-19 (October 2025: "the
number of illegal immigrants in the country keeps going down") is a checkable forecast; ladder 157
gives the stock at 14.6–16.7m and no 2025 trend. [OPEN]

## 3. How his position moved

| Date | In his words |
|---|---|
| 2020-08 | "Immigrants of virtually all stripes … make native-born Americans richer"; costs named are traffic, rent, water, pollution |
| 2021-08 | "less-educated immigrants are both less economically beneficial and also provoke much more political backlash"; effective-altruism arguments moved him toward "Denmark's mix of generous foreign aid and stingy immigration" |
| 2023-07 | "Republicans are basically right and having large numbers of asylum claimants show up is undesirable" |
| 2025-01 | The housing-scarcity argument is "factually accurate" |
| 2025-03 | "strong borders … deporting people who actually do commit crimes … 'building a wall around the welfare state'" |
| 2025-10 | "elite liberals — including fairly moderate ones like me — are uncomfortable with the idea of being mean to sympathetic immigration cases" |
| 2025-11 | "in that sense immigration makes crime worse"; the left overstates "the substantive case that immigration is bad economics" |
| 2026-04 | "I'm not sure asylum has a future" (podcast preview) |
| 2026-05 | If robots replace unskilled work, "that would … make certain restrictionist ideas much more true" |
| 2026-07 | "it's not good enough for liberals to reassure voters that assimilation happens" |

The movement is toward conceding costs on housing, asylum, enforcement and low-skill economics
while holding the aggregate-benefit claim fixed. As with Smith (scorecard §1), concessions arrive
as new framing and the 2020 universal is never marked withdrawn. [INFERENCE]

## 4. Gaps

- Paywalled and read only as free previews. Five yielded a quote used here: "Hostility to
  immigration isn't about economics" (2023-09-06); parts one and three of the October–November
  2025 series (2025-10-15 and 2025-10-28); "Should we end asylum?" (2026-04-30); "The case for
  assimilation" (2026-07-02). Five yielded nothing: `/p/immigration-and-wages` (2021-01-04), his
  single dedicated wages post, 396 characters; "One Billion Americans — now more than ever"
  (2022-10-26), whose 10,511-character preview restates the national-power case of §1 and
  carries no fiscal, wage or skill claim; `/p/immigration-policy-should-prioritize`
  (2025-02-10); "Blame Trump for Trump-era immigration excesses" (2026-01-20); "Immigration
  enforcement's accountability gap" (2026-01-30). Part two of the 2025 series
  (`/p/democrats-cant-just-go-back-to-obamas`) was not fetched.
- *One Billion Americans* is represented by the New York magazine excerpt he bylined; the book's
  fiscal and wage chapters were not read. Vox (2016–2019) and Bloomberg columns were not fetched.
- Twelve on-topic Slow Boring posts named in the notes files were not fetched. The two readers'
  lists overlap, and two slugs on the social list (`immigration-openness`, the Kolko guest post)
  were fetched by the economic reader.
- `/p/immigration-can-power-american-energy` (2024-04-27) has an unresolved byline and was left
  unused.
- Negative results in the pieces read: no reference to the National Academies' 2016 fiscal
  report, no federal fiscal, Social Security or debt number in his own voice, and no claim about
  second-generation outcomes beyond E-07 and the Boustan citation in SC-09.
- OPEN rows name what would settle them.

[DISCONFIRMATION] The collection was weighted toward claims that could embarrass this repo's
account as much as toward his errors. The strongest is E-07: if super-achievers and the second
generation's top tail carry most of the gain, an average fiscal ledger understates it. Our ledger
measures the second generation's average and finds a gap; it does not price patents or firms.
That limit is stated in §1 and is not resolved here.

[INSTRUMENT] Graded by an LLM whose September 18 grades of four other commentators were
over-strong and corrected a day later; the matching rule above is that correction applied in
advance. See [`notes/llm-bias-caveat.md`](../notes/llm-bias-caveat.md).

## Revisions

- 2026-09-21 (later the same day): reconciled against the two readers' final reports. No grade
  changed. Added the Humphreys attribution note, the April 2026 asylum line and the readers'
  negative results; rewrote the preview list from the fetch inventory (it had named "parts 1–3"
  of the 2025 series where only parts one and three were fetched, and omitted four previews);
  corrected "seventeen" unfetched posts to twelve, since the first count added the two readers'
  lists without removing overlaps. Fetched one post neither reader listed, "One Billion
  Americans — now more than ever" (2022-10-26): its free preview holds no fiscal claim, so the
  statement that the 2020 universals were never marked withdrawn still rests on the pieces read,
  not on his full output. [INFERENCE]
