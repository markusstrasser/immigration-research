# Political backlash externality — can it be priced?

**Superseded verdict, 2026-09-17:** [audit §6](../../../research/immigration-new-conclusions-audit-2026-09-17.md) withdraws $1,300–$43,000 as a defensible bound. Both endpoints depend on unsupported policy attribution, exposure and transport assumptions; dividing discounted lifetime cost by forty is not a comparable annual equivalent. The mechanism remains unpriced, with no identified positive lower bound. Original scenario and reasoning remain below for provenance.

**Verdict:** The chain can be *bounded* but not *priced*. Links 1 and 3 have strong primary
estimates; the middle link (vote share -> populist government) is estimated by nobody, and the
local-to-national aggregation step breaks the arithmetic. Defensible range: **~$1,300 to
~$43,000 per low-skill immigrant-year** (factor ~33), which straddles the repo's measured
second-generation fiscal gap of -$8,300 to -$8,900. **Do not book a point estimate.** Full
reasoning under THE JOIN below.

Model self-report: claude-opus-5[1m] (Opus 5, 1M context), researcher subagent lane.

Lane: `infra/immigration-fiscal/backlash_cost_2026_09_17/`
Scope: (1) immigration → far-right vote coefficients; (2) populist government → GDP cost;
(3) [INFERENCE] the join, with range and weakest link; (4) US specificity + 2024 Hispanic swing.

## Findings

All four deliverables completed across appends 1-4 below. Remaining gaps are listed inline and
at the end of append 4; none blocks the verdict.

---

## Append 1 (turn 5) — Link 1 and Link 2 anchors verified

### 1a. Konstantinou & Roumanias 2024 — the headline elasticity
"From the Fringe to the front-stage. European immigration and the Far-Right vote: An IV approach",
*Quarterly Review of Economics and Finance* 98 (2024) 101925. DOI 10.1016/j.qref.2024.101925
[SOURCE: https://doi.org/10.1016/j.qref.2024.101925]

Design: NUTS3 regional panel, 4,500+ electoral outcomes, Western Europe, 2000-2017.
Immigration in *neighbouring countries* instruments domestic immigration stock (2SLS).
Abstract, verbatim: "a 1% increase in immigration stocks leads to a between 1.78% and 2.97%
in Far-Right voting"; at NUTS2 the effect is "between 3% and 5.32%".
IV estimates are larger than OLS/FE — the authors read this as negative feedback from
Far-Right strength back onto immigration policy (reverse causation biases OLS down).

**UNITS WARNING — this is a RELATIVE effect, not percentage points.** Both sides of the
sentence are in %, and the NUTS2 figures (3-5.32%) are implausible as pp on a far-right base
of ~10%. Read as an elasticity: +1% of immigration stock (i.e. stock from 10.0% to 10.1% of
population, not +1pp) raises far-right vote share by ~2-3% *of itself* (10% -> ~10.2-10.3%).
[UNVERIFIED — exact table number and units confirmation still pending; flagged as the single
biggest arithmetic trap in this chain]

### 1b. Mayda, Peri & Steingress 2022 (AEJ:Applied 14(1):358-89) — the US sign flip
DOI 10.1257/app.20190081 [SOURCE: https://www.aeaweb.org/articles?id=10.1257%2Fapp.20190081]
NBER WP version w24510 free: https://www.nber.org/system/files/working_papers/w24510/w24510.pdf

Design: US county panel 1990-2016, Republican vote share (presidential/House/Senate pooled),
shift-share IV from 1980 settlement by origin x skill-specific national inflows; county, year
and election FE; commuting-zone controls incl. Bartik shifter and Autor-Dorn-Hanson import
exposure; SEs clustered by commuting zone.

**Table 5, col. 1 (preferred spec), 2SLS:**
| Regressor (share of adult population) | Effect on Republican vote share |
|---|---|
| Low-skilled immigrants, +1 percentage point | **+4.563 pp*** |
| High-skilled immigrants, +1 percentage point | **-1.522 pp*** |

These ARE percentage points, and both are per 1pp of the adult population — a genuinely large
effect. Robustness table A5 gives low-skilled 3.16 to 4.76 and high-skilled -1.38 to -2.39.
The earlier NBER 1990-2010 version had a much smaller +1.3 / -0.78, so the published estimate
roughly tripled the low-skill coefficient when 2012-16 was added. [FRAMING-SENSITIVE: which
vintage you quote changes the answer by 3.5x — quote the published 4.563, note the w24510 1.3.]
Heterogeneity (Table 7): in the most low-skill county the low-skill effect is +3.22pp, in the
most high-skill county +0.28pp and insignificant.
Counterfactual in the paper: halving 1990-2016 immigrant growth flips WI, PA, FL, NC, AZ, GA
and TX to the Democrats in 2016. Net effect in the average county was *pro-Democrat*, because
US immigration over the period was on net high-skilled.

### 2a. Funke, Schularick & Trebesch 2023 — the populist-government cost
"Populist Leaders and the Economy", *AER* 113(12):3249-88, Dec 2023. DOI 10.1257/aer.20202045
[SOURCE: https://www.aeaweb.org/articles?id=10.1257%2Faer.20202045]
Free: https://sciencespo.hal.science/hal-04211174v1

51 populist presidents/PMs, 1900-2020. Main estimator: partially pooled synthetic control with
staggered adoption (Abadie-L'Hour; Ben-Michael-Feller-Rothstein), plus event-study local
projections and inverse-propensity-weighted LPs as cross-checks.
**Point estimate: real GDP per capita 10% lower than the synthetic non-populist counterfactual
after 15 years.** Channels named: economic disintegration (trade and financial integration
fall), macro instability (debt and inflation rise), erosion of institutions (checks and
balances, judicial and press freedom).
Decomposition that matters for us: **"The GDP decline is primarily driven by left-wing
populists"**, though it is "also observable for right-wing populists". Populists stay in power
~8 years vs 4 for non-populists.
[GAP] Confidence interval not yet pulled — abstract and intro give only the 10%. Cattaneo et al.
simulation-based CIs are in the paper; need the figure/table number and the band.
[GAP] Right-wing-only subsample magnitude not yet quoted. This is load-bearing: the immigration
channel produces *right*-wing populists, and FST's headline is driven by the *left* wing.

### 1c. Schröder, Rehm & Röcke 2026 — the disconfirmer, sized
PLoS One 21(7): e0350403, 21 July 2026. DOI 10.1371/journal.pone.0350403
[SOURCE: https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0350403]
SOEP 2014-2024, 11 waves, 110,194 observations from 31,985 individuals, incl. individual FE.
**Effect size as the authors state it: immigration concern alone accounts for ~75% of
explicable variation in AfD support and ~90% of explicable variation in actual AfD voting.**
Adding the full deprivation block (income, education, life satisfaction, own-finances concern,
general-economy concern) raises explained variation by ~2 percentage points over the
immigration-concern-only model. Individual FE: the same person supports the AfD more when they
become more concerned about immigration; becoming more deprived has hardly any effect.
Their measure is *perceived* concern, and Schröder is explicit: "It is not about the actual
number of migrants in a person's immediate surroundings, but about their personal perception".
That is exactly why it does not rescue the dose-response chain — see Gaps.

## Gaps after append 1

- [GAP] Konstantinou table number and pp-vs-relative confirmation.
- [GAP] FST confidence interval + right-wing-populist subsample estimate.
- [GAP] Halla/Wagner/Zweimuller, Dustmann/Vasiljeva/Damm, Edo, Tabellini — not yet pulled.
- [GAP] Far-right-in-coalition fiscal/institutional cost — nothing yet.
- [GAP] Jones 2017; Alesina-Baqir-Easterly; Luttmer; 2024 Hispanic swing.
- [GAP] The join (deliverable 3) — not yet written.

---

## Append 2 (turn 7) — the rest of link 1, plus Jones and the 2024 swing

### 1d. Halla, Wagner & Zweimüller 2017 (JEEA 15(6):1341-85) — Austria, FPÖ
DOI 10.1093/jeea/jvx003 [SOURCE: https://ideas.repec.org/a/oup/jeurec/v15y2017i6p1341-1385..html]
Ungated WP: https://doi.org/10.5167/uzh-63504
Design: Austrian community panel; identification from the 1960s guest-worker inflow, whose
settlement pattern is argued exogenous to later local politics; FPÖ vote share 1979-2013.
Headline as the *published* abstract states it: immigrant inflow into a community "has a
significant impact on the increase in the community's voting share for the FPÖ, **explaining
roughly a tenth of the regional variation in vote changes**".
[TRAP] The 2015 working-paper abstract says "roughly a **quarter** of the cross-community
variance". Published = a tenth of the variance *in changes*; WP = a quarter of the variance in
*levels*. Quote the published figure. Mechanism they favour: labour-market competition plus
degraded "compositional amenities" — longer school commutes for Austrian children, fewer
daycare places. No native out-migration (so this is not white flight).
[GAP] The pp-per-pp elasticity itself is in their Table, not in the abstract; not pulled.

### 1e. Dustmann, Vasiljeva & Damm 2019 (REStud 86(5):2035-91) — Denmark, the sign reversal
DOI 10.1093/restud/rdy047 [SOURCE: https://ideas.repec.org/a/oup/restud/v86y2019i5p2035-2091..html]
Ungated WP: RFBerlin DP 1619, https://ideas.repec.org/p/crm/wpaper/1619.html
**Best identification in the whole chain**: Denmark's dispersal policy assigned refugees to
municipalities on a quasi-random basis, so this is not a shift-share design and does not rest
on the exclusion restriction that historical settlement affects politics only through current
immigration.
Result: in all but the most urban municipalities, a larger allocated refugee share raises the
vote share of right-leaning anti-immigration parties (WP version: and of centre-right parties,
while centre-left falls). **In the largest, most urban municipalities the effect on
anti-immigration vote share is, if anything, the opposite sign.** Heterogeneity: stronger in
less-urban municipalities with high pre-policy immigrant *and* affluent shares; pre-policy
crime rates predict a larger pro-anti-immigration response in both urban and non-urban places.
Refugee allocation also changes *where anti-immigration parties choose to stand* for municipal
election — a supply-side response that is itself part of the mechanism.
[This is the paper that makes the German "AfD strongest where immigration is lowest"
disconfirmer tractable: the sign of the local dose-response is not constant across place type.]

### 1f. Edo, Giesing, Öztunc & Poutvaara 2019 (European Economic Review 115:99-143) — France
[SOURCE: https://www.ifo.de/en/econpol/publications/2019/working-paper/immigration-and-electoral-support-far-left-and-far-right]
Panel of French presidential elections 1988-2017; recent flows instrumented by 1968 settlement.
Immigration raises far-right support; **the effect is driven by low-educated immigrants from
non-Western countries**. Weak negative (or no robust) effect on the far left, which the authors
read as reduced demand for redistribution. Same skill-composition asymmetry as Mayda-Peri-
Steingress, on a different continent and a different party system.
[GAP] Point coefficients not pulled (working-paper PDF not fetched).

### 1g. Tabellini 2020 (REStud 87(1):454-86) — the cleanest statement of the whole thesis
DOI 10.1093/restud/rdz027 [SOURCE: https://www.hbs.edu/ris/Publication%20Files/19-005_a4261e39-175c-4b3f-969a-8e1ce818a3d8.pdf]
US cities 1910-30; immigration instrumented by WWI and the 1921/1924 Acts interacted with
pre-existing settlement by origin.
| Outcome | 2SLS effect of +5 pp immigrant share |
|---|---|
| Democrat (pro-immigrant party) vote share | **-2 pp** (= -5% of its 1910 mean) |
| Democrat-Republican margin | **-2.9 pp** (= -15% of 1910 mean) |
| P(House member votes for 1924 National Origins Act) | **+10 pp** |
| Natives' employment | **+1.4 pp** (+1.6% of 1910 level) |
| City tax rates and public spending | both cut |
Spending cuts concentrated in education, sewerage and garbage collection. And the decisive
test: **Protestant and non-Protestant immigrants had the same effect on natives' employment
but only Catholic and Jewish immigrants produced the political backlash.** Economic gain,
political loss, and the loss tracks cultural distance rather than labour-market exposure.
Tabellini's own summary: "even when diversity is economically beneficial, it may nonetheless
be socially hard to manage."
Follow-up worth reading: Alesina & Tabellini 2024, "The Political Effects of Immigration:
Culture or Economics?", *Journal of Economic Literature* 62(1):5-46 — the survey of this whole
link. [GAP] not read.

### 2b. Jones 2017 — the argument, and its honesty about what it is
Garett Jones, "The Populist Revolts of 2016: A Hidden Cost of Immigration?",
*The Independent Review* 22(3), Winter 2017/18.
[SOURCE: https://www.independent.org/wp-content/uploads/tir/2017/12/tir_22_3_03_jones.pdf]
Verbatim thesis: "The populist backlash against immigration is strong evidence that a mass
influx of lower-skilled workers can lower the quality of political institutions."
Chain he builds: diversity lowers social trust (Putnam 2007) -> low trust raises demand for
government regulation (Aghion et al. 2010) -> diversity lowers public-goods provision
(Alesina, Baqir & Easterly 1999; Easterly & Levine 1997) -> institutional quality falls.
He explicitly brackets the moral question: "the question here isn't whether immigrants are
morally responsible for an anti-immigration backlash."
**He offers no quantification.** His own complaint is that nobody has costed it: "This is the
kind of risk that should definitely be included in any kind of serious cost-benefit analysis of
rising diversity, yet I have seen nothing of the kind in the academic literature." That is
still true in 2026 — see the join. He also flags the Easterly 2001 defeater: diversity does not
lower growth or worsen policy in countries with sufficiently good institutions.

### 4a. The 2024 Hispanic swing — three independent instruments, one direction
| Source | Dem share of Hispanic vote 2020 | 2024 | Dem margin swing |
|---|---|---|---|
| Catalist voter file (`whathappened2024`) | 63% | **54%** | -9 pts in support |
| Pew validated voters | 61% | **51%** (Trump 48%, up from 36%) | D+25 to D+3, ~22 pts |
| Edison/NEP exit poll | ~65% | ~52% | D+33 to D+5, ~28 pts |
| Cygnal n=9,000 exit poll | D+33 | D+9 | 24 pts |
[SOURCE: https://catalist.us/whathappened2024/ ;
https://www.pewresearch.org/politics/2025/06/26/voting-patterns-in-the-2024-election/ ;
https://centerforpolitics.org/crystalball/how-the-new-catalist-report-on-2024-compares-to-the-exit-polls/]
Catalist subgroup detail that matters most: **Latino men fell below a majority for the
Democrats for the first time, 47%**; among young Latino men, support fell 63% -> 47%. Rural
Latinos: 50% (2016) -> 46% (2020) -> **38% (2024)**. Urban-rural gap 19 pts in 2016.
Pew's mechanism finding: the shift is mostly *differential turnout*, not conversion. 86% of
Trump's 2020 Hispanic voters turned out in 2024 vs only 77% of Biden's; Hispanic 2020-only
voters had favoured Biden 69-31, Hispanic 2024-only voters favoured Trump 60-37.
**Naturalized citizens** (Pew, 9% of the electorate): D+21 in 2020 -> **D+4 in 2024**; Shor/Blue
Rose put the same group at D+27 -> R+1.
Contested read: the BSP Research / African American Research Collaborative American Electorate
Voter Poll (n=3,750 Latinos) puts Harris at 62-37 among Latinos and rejects the exit-poll
Latino-men figure; their precinct-level ecological regressions in Maricopa, Pima, Philadelphia
and Lehigh show a 5-7 point decline, not 20-30.
[SOURCE: https://2024electionpoll.us/wp-content/uploads/2024/11/AEP-Latino-Deck-Final.pdf]
Their other point survives regardless of magnitude: "Latino voters were not instrumental in the
Trump victory. If no Latino had cast a ballot, the outcome would be unchanged."
[FRAMING-SENSITIVE: the exit poll and the voter file disagree by ~2x on the size of the swing.
Use Catalist/Pew (voter-file and validated) as the primary and note the exit-poll overstatement;
BSP is a partisan-commissioned poll but its ecological-regression check is a real method.]

## Gaps after append 2
- [GAP] Konstantinou exact table + units; FST CI + right-wing subsample; far-right-in-coalition
  cost; Alesina-Baqir-Easterly and Luttmer coefficients; the join.

---

## Append 3 (turn 9) — link 2 beyond Funke et al., and the US public-goods literature

### 2c. Far-right in COALITION, not merely in parliament — and this is where the cost thins out
The operator asked specifically for governing rather than seat-winning. Four findings, and they
do not agree.

**Elsässer & Röth 2024, "Fiscal implications of the populist radical right in power",
*Journal of European Public Policy*.** DOI 10.1080/13501763.2024.2314248
[SOURCE: https://doi.org/10.1080/13501763.2024.2314248 ; plain-language:
https://blogs.lse.ac.uk/europpblog/2024/02/26/does-the-populist-radical-right-run-higher-deficits-in-government/]
35 countries, 1980-2019; mixed-effects models with entropy-balanced weights matching on
socio-economic starting conditions. Populist-radical-right participation in government produces
"significantly and substantially higher public deficits" than comparable governments without
them. Mechanism is the signature combination: tax cuts plus protected pension spending, driven
by "native producerist deservingness". **Reverses in Eastern Europe**, where PRRP governments
run comparatively *lower* deficits despite the same announced policy mix (Fidesz case study).
[GAP] deficit magnitude in pp of GDP not pulled.

**Disconfirmer — Stankov 2025, "Frugal populists: fiscal management under populist rule in
Europe and the OECD", *Frontiers in Political Science*.** DOI 10.3389/fpos.2025.1565020
1950-2022, Europe + OECD: **no sufficient evidence of a debt increase attributable to populist
governance.** Three reasons he gives, all of which bear directly on transporting Funke et al. to
Western Europe: fiscal rules and electoral accountability punish bad management; **most European
populists have so far held junior coalition roles, limiting policy damage**; and parliamentary
systems differ from the presidential regimes that dominate the existing evidence base.
[This is the single most important caveat on the whole cost chain and it must be in the essay.]

**Bond-market price of coalition — "So Right It's Wrong? Right Governments, Far Right Populism,
and Investment Risk", *Comparative Political Studies*.** DOI 10.1177/00104140231223742
Quarterly bond spreads, 23 OECD advanced economies, 2000-2019, plus a paired case study of
Rutte I (Netherlands, supported by the PVV) against Reinfeldt II (Sweden, which refused to
partner with the Sweden Democrats). **Right-wing executives enjoy bond spreads over 100 basis
points lower than left-wing ones on average during their tenure — but only when they govern
without the far right.** Partnering with the far right erases the mainstream right's borrowing
advantage. This is the cleanest *priced* estimate of a far-right coalition anywhere in the set.

**Balduzzi, Brancati, Brianti & Schiantarelli, "Populism, Political Risk and the Economy:
Lessons from Italy"** (Boston College WP 989, 2019). [SOURCE: https://ideas.repec.org/p/boc/bocoec/989.html]
Local-projections IV using CDS-spread changes around Italian political events 2013-2019 as the
instrument for political-risk shocks. Populist-rise shocks have adverse and sizable effects on
financial markets and a negative real effect, **moderated by European institutions and domestic
constitutional constraints**, with international spillovers to other eurozone spreads.
Same lesson as Stankov: binding institutions truncate the damage.

Policy-output channel, for completeness: Akkerman (Migration Policy Institute, Netherlands)
notes PRRPs have a weak bargaining position in coalition precisely because their immigration
stance leaves them few coalition partners; Röth, Afonso & Spies find PRRP cabinet participation
raises market-liberal economic policy (+11.82 on their economy index) while its effect on
deregulation is insignificant (+0.65).

### 4b. US: does Hispanic/ethnic composition move policy outcomes? Yes, but through DIVERSITY
**Alesina, Baqir & Easterly 1999, "Public Goods and Ethnic Divisions", *QJE* 114(4):1243-84.**
DOI 10.1162/003355399556269
[SOURCE: https://dash.harvard.edu/server/api/core/bitstreams/7312037c-5be4-6bd4-e053-0100007fdf3b/content]
Three cross-sections: US cities, metro areas, urban counties. ETHNIC = probability two random
residents differ by race. The coefficient is scaled so it reads as the change from ETHNIC=0 to
ETHNIC=1.
| Outcome | Effect of moving from full homogeneity to full heterogeneity |
|---|---|
| Share of city spending on **roads** | **-0.09 (nine percentage points)**, t = -4.7 to -8.7 |
| Shares on education, roads, sewerage/trash | all negative and significant across all 3 samples |
| Share of spending on **welfare** (metro, county) | negative; **1 SD of ETHNIC = -0.2 SD of the welfare share** |
| Share on **police** | **positive** in all three samples |
Their own scaling caution: with five race groups ETHNIC maxes at .8, so the 0-to-1 reading is
heuristic. One SD of ETHNIC moves the roads share by a quarter of an SD.
**Crucial for the essay's framing**: "The results are mainly driven by observations in which
majority whites are reacting to varying sizes of minority groups." The mechanism is the
*majority's* response to diversity, not the minority's preferences. That is the same asymmetry
as Tabellini's Catholic/Jewish-but-not-Protestant result.

**Luttmer 2001, "Group Loyalty and the Taste for Redistribution", *JPE* 109(3):500-528.**
DOI 10.1086/321019
GSS self-reported welfare-spending preference, validated against voting on welfare cuts.
Two interpersonal preferences: a **negative exposure effect** (support for welfare falls as the
local welfare recipiency rate rises) and **racial group loyalty** (support rises with the share
of local recipients who share the respondent's race). Robust at state, metro and census-tract
definitions. His stated implication: this is why welfare benefit levels are low in racially
heterogeneous states.
[GAP] Luttmer's point elasticities not pulled; only the signs and the validated direction.

Alesina & Glaeser 2004 (*Fighting Poverty in the US and Europe*) is the book-length version of
the same claim: roughly half the US-Europe gap in redistribution is attributable to racial
fragmentation and the political institutions that translate it. [GAP] not verified from primary;
do not quote a number from it without checking.

### 2a supplement — what is still missing from Funke et al.
[GAP, ATTEMPTED AND BLOCKED] The confidence interval on the -10% and the right-wing-only
subsample estimate. The Sciences Po HAL mirror is behind an Anubis bot wall; the Kiel WP path
404s; the AEA PDF needs a subscription. Next dispatch should try
`https://www.nber.org/` mirrors, the CEPR DP, or an institutional copy, or read the AER
via the corpus `fetch_paper` with the DOI 10.1257/aer.20202045 through Sci-Hub.
What is already known from the abstract and introduction and is enough for the join: the -10%
headline, the 15-year horizon, and the authors' own statement that the decline is **primarily
driven by left-wing populists**.

---

## Append 4 (turn 11) — Funke et al. inference details, then THE JOIN

### 2a completed — CI and the left/right cut
[SOURCE: AER full text mirror https://iacmr.org/wp-content/uploads/sites/26/2024/05/6.populist-leaders-and-economies_aer23.pdf ;
online appendix https://assets.aeaweb.org/asset-server/files/19727.pdf ;
book-chapter restatement DOI 10.1515/9783839474877-012]
Inference: **90% simulation-based confidence intervals** following Cattaneo, Feng & Titiunik
(2021) and Cattaneo, Feng, Palomba & Titiunik (2022), separating in-sample uncertainty (200
simulations) from out-of-sample uncertainty (sub-Gaussian bounds). Plus time and country placebo
tests and Hahn-Shi end-of-sample instability tests. Appendix figures plot left-wing and
right-wing gap paths separately and the authors state the result "is robust ... when we cut the
sample along the left-wing versus right-wing populist dimension".
Sample composition, which is decisive for transportability: 1,482 leaders screened, **51
populists, 72 spells, split almost evenly 37 right-wing / 35 left-wing**, from 28 countries;
core estimation sample 28 cases (balanced, ±15 years of GDP data, which is why **Trump is
excluded**). "Latin America and Europe clearly dominate the sample", with left-wing populists
the main story in Latin America and right-wing populists in Europe. The cumulative gap
"exceed[s] ten percentage points after 15 years" and "the economy does not recover".
[GAP, still] The numeric width of the 90% band at t=15 is read off a figure, not tabulated;
I did not extract it. Treat -10% as a central estimate whose band is visibly wide and, on the
published figures, not obviously excluding zero at every horizon.

---

# THE JOIN [INFERENCE — every number below is my construction, not any author's]

## The chain, with the three transfer functions written out

Let L = low-skilled immigrants as a share of the adult population.

**Link A (immigration -> far-right/populist vote).** Best-identified US estimate:
dV/dL = **+4.563 pp of Republican vote share per +1 pp of L** (Mayda, Peri & Steingress 2022,
Table 5 col. 1). European analogue as an elasticity: **+1.78% to +2.97% of far-right vote per
+1% of immigration stock** (Konstantinou & Roumanias 2024). Denmark's quasi-random allocation
(Dustmann et al. 2019) confirms the sign outside the shift-share family, but with a **sign
reversal in the most urban municipalities**.

**Link B (vote share -> populist government).** *No paper estimates this.* I use a linear
approximation over the competitive band: US presidential outcomes turn inside roughly ±5 pp of
two-party vote, so dP/dV ≈ **0.1 per pp**, i.e. a 10-point swing moves the probability from 0
to 1. Nothing in the literature licenses this number. It is the weakest link and I say so
below.

**Link C (populist government -> GDP).** Funke et al. 2023: **-10% of GDP per capita at 15
years**, path diverging from entry and not recovering. Present value, gap growing roughly
linearly 0 -> 10% over 15 years, discounted at 3%: average gap ≈5% of GDP over a 15-year
annuity factor ≈11.9, so **PV ≈ 0.6 x annual GDP**. On US GDP of ~$29T that is **~$17T per
populist episode**.

## Naive composition, and why it detonates

US adult population ≈262M, so +1 pp of L = 2.62M low-skill immigrants.
Link A: 2.62M immigrants -> +4.563 pp Republican vote.
Link B: +4.563 pp -> ΔP ≈ +0.46.
Link C: 0.46 x $17T = **$7.8T expected cost, from 2.62M immigrants = ~$3.0M per immigrant.**

**That is roughly 300x the entire measured lifetime fiscal gap and it is therefore wrong.**
A channel that priced at $3M per person would dominate every other consideration in the
immigration debate by two orders of magnitude, and it does not. The arithmetic is a reductio,
and the informative part is *which* link breaks.

**The link that breaks is A, and it breaks on aggregation.** Mayda-Peri-Steingress,
Halla et al., Dustmann et al., Edo et al. and Tabellini are all **cross-sectional within
country**: counties or municipalities that received *relatively more* immigrants shifted
*relatively more* to the right. None of them identifies the national-level effect of national
immigration, because the national inflow is absorbed into the year fixed effect by
construction. Treating a within-country relative coefficient as a national dose-response is the
central error available in this literature, and it is exactly the error the essay would make.
The German disconfirmer is the visible symptom: AfD support is highest where immigration is
lowest, which is impossible under a uniform positive local dose-response and unsurprising once
you accept that the national salience channel and the local contact channel have different
signs. Schröder, Rehm & Röcke 2026 say the same thing from the individual side: what predicts
AfD support is **perceived** immigration concern (75% of explicable variation in support, 90%
in voting), and Schröder states outright that it is "not about the actual number of migrants in
a person's immediate surroundings". A cost that runs through perception rather than local stock
cannot be divided by a local stock.

## The defensible range: use the authors' own national counterfactual instead

The one place a paper in this literature makes a *national* claim is MPS's own counterfactual:
halving 1990-2016 immigrant growth flips WI, PA, FL, NC, AZ, GA and TX in 2016. The US received
on the order of 20M low-skill immigrants over that window, so the marginal ~10M are, on the
authors' own arithmetic, what bought one populist presidency. Assign the whole of it to them,
which is maximally generous to the restrictionist reading.

Cost of one populist term, bracketed rather than assumed:
| Bound | Basis | PV |
|---|---|---|
| Low | Measured US trade-war output cost, ~0.3-0.5% of GDP sustained over a term | ~$0.5T |
| High | Funke et al. -10% at 15 years applied unmodified | ~$17T |

Divide by 10M immigrants, then spread over ~40 adult years in the US:

| | per immigrant, lifetime | **per immigrant-year** |
|---|---|---|
| Low bound | $50,000 | **~$1,300** |
| High bound | $1,700,000 | **~$43,000** |

**Range: roughly $1,300 to $43,000 per low-skill immigrant-year, an interval spanning a factor
of ~33.** For scale, the repo's measured second-generation fiscal gap is -$8,300 to -$8,900 per
adult-year. So the political channel's *low* bound is a fifth of the fiscal gap and its *high*
bound is five times it. **No point estimate should be reported. The honest statement is that
the channel is plausibly the same order of magnitude as the entire fiscal ledger and cannot be
signed more precisely than that.** This is the same verdict the automation channel got
(memo §16) and for structurally the same reason: a real mechanism, an unidentified magnitude.

## Which link is weakest, ranked

1. **Link B, vote share -> populist government. Not estimated by anyone.** It is a threshold
   function of the whole party system: Denmark's anti-immigration parties have held vote share
   for decades with limited governing power; the AfD is at record vote share and in no
   government; the FPÖ has entered coalition three times. Between vote share and policy sits
   the cordon sanitaire, the electoral system, and coalition arithmetic — none of it a function
   of immigration.
2. **Link A's external validity, i.e. local-to-national aggregation.** See above.
3. **Link C's transportability.** Funke et al.'s sample is dominated by Latin America and
   interwar Europe, the GDP decline is "primarily driven by left-wing populists", and Trump is
   excluded from the core sample for lack of ±15 years of data. Two papers say institutions
   truncate the damage in exactly the countries the essay is about: **Stankov 2025 finds no
   sufficient evidence of a populism-attributable debt increase in Europe and the OECD**, giving
   as one reason that European populists mostly hold junior coalition roles; **Balduzzi et al.**
   find Italian populist-risk shocks were "moderated by European institutions and domestic
   constitutional constraints". Against that, **Elsässer & Röth 2024** do find significantly
   higher deficits under radical-right government participation in Western Europe, and the
   **CPS bond-spread paper** finds the mainstream right's ~100bp spread advantage disappears
   when it partners with the far right. The literature on *governing* far-right parties is
   genuinely split; the literature on *populist leaders* globally is not. The essay must not
   quote -10% as if it applied to a European coalition.
4. Link C's horizon and discounting — my own PV construction, defensible but arbitrary.

## The objection the readers will make, and the answer both sides give

**Objection: the cost is caused by the political reaction, not by the immigrants. Booking it
against immigration charges newcomers for their neighbours' xenophobia.**

*The restrictionist answer* is Garett Jones's, and it concedes the moral point explicitly while
denying that it settles the accounting: "the question here isn't whether immigrants are morally
responsible for an anti-immigration backlash". His claim is causal, not moral — if a policy
predictably produces an outcome, the outcome belongs in the cost-benefit analysis of the policy
regardless of who is blameworthy. A dam that predictably floods a village is costed at the
flood, not at the rain. He notes nobody has done it: "I have seen nothing of the kind in the
academic literature." Still true.

*The pro-immigration answer* is the heckler's-veto structure: pricing backlash into the policy
makes the size of the cost a function of how much hostility the receiving population chooses to
express, which hands a veto to the most hostile and creates an incentive to be more hostile.
Applied to any other group the accounting is obviously unacceptable.

*What the evidence actually adds, and it cuts for the restrictionist side on the facts and for
the pro-immigration side on the framing:* Tabellini 2020 is the decisive case. Immigration
raised natives' employment (+1.4 pp per +5 pp immigrant share) and industrial production, yet
cities cut taxes and public goods and the House voted for the 1924 Act. And **Protestant and
non-Protestant immigrants had identical employment effects but only Catholic and Jewish
immigrants triggered the backlash.** So the reaction is not tracking an economic injury, which
destroys the "natives are responding to a real harm" defence of the cost — and simultaneously
confirms that the reaction is real, predictable and expensive. Tabellini's own line is the one
for the essay: "even when diversity is economically beneficial, it may nonetheless be socially
hard to manage." The cost is real *and* the objection is right. Both.

**My recommendation for the essay: report the channel as a named, sized-but-unbookable
externality with the range above, cite Tabellini as the mechanism and the moral hinge, cite
Stankov as the reason the European transfer fails, and refuse the point estimate.** Booking a
number here would be the mirror image of the automation-channel error the repo already caught.

---

# 4. US specificity: does Hispanic share move policy, and is the bloc reliable?

**Does Hispanic/ethnic composition move US policy outcomes? Yes — but the literature measures
DIVERSITY, not Hispanic share, and it measures the MAJORITY's reaction.**
Alesina, Baqir & Easterly 1999: the productive-public-goods share (education, roads, sewerage
and trash) falls with ethnic fractionalisation in cities, metro areas and urban counties; the
roads share falls by ~9 pp across the full 0-to-1 ETHNIC range (t = -4.7 to -8.7); one SD of
ETHNIC costs a fifth of an SD of the welfare share; police share *rises*. Their own attribution:
"The results are mainly driven by observations in which majority whites are reacting to varying
sizes of minority groups." Luttmer 2001: support for welfare falls with the local recipiency
rate and rises with the own-race share of local recipients, at state, metro and tract level.
Both are about the *reaction to* diversity. **Neither is evidence that Hispanic voters
themselves demand less public spending — and the repo's own GSS result says the opposite.**

**Reconciling §15 with the 2024 swing.** They are not in conflict, because they measure
different objects over different windows.
- §15 (GSS 2000-2024, adjusted): Democratic party ID is **+.14 over third-plus-generation
  whites in every generation and does not converge**; redistribution preference stays high
  (+0.63 unadjusted -> +0.50 adjusted on the 7-point item); but the *immigration* items converge
  monotonically and by the third generation the "immigrants increase crime" gap is -.02 (se .04),
  statistically indistinguishable from whites. Strength of partisanship is 5-6 points *below*
  whites in every generation.
- 2024: Democratic Hispanic vote share fell 63% -> 54% (Catalist) or 61% -> 51% (Pew), with
  Latino men at 47% and rural Latinos at 38%. Naturalized citizens went D+21 -> D+4 (Pew).
- **The reconciliation is in §15's own numbers.** Stable party *identification* plus
  *weak partisan intensity* plus *converged immigration attitudes* is precisely the profile of a
  bloc whose vote is loosely attached to its label. Pew's mechanism finding closes it: the 2024
  shift was mostly **differential turnout, not conversion** (86% of Trump's 2020 Hispanic voters
  returned vs 77% of Biden's; 2020-only Hispanic voters had been Biden 69-31, 2024-only Hispanic
  voters were Trump 60-37). Identification held; turnout and the marginal voter moved.
- **So the "reliable Democratic bloc" premise is undercut, and §15 explains why it was always
  weaker than it looked.** But so is the mirror-image restrictionist premise that immigration
  mechanically imports a permanent left-of-centre electorate: the group with the largest single
  swing was **naturalized citizens**, the immigrants themselves.
- **And note the direction this cuts for Link A.** MPS's mechanism is explicitly *indirect* —
  the effect runs through existing citizens' votes, not immigrants' own. 2024 is a second
  reason the direct-bloc story is the wrong model: the political effect of immigration in the
  US is a native reaction, which is what makes it a backlash externality rather than a
  franchise-composition effect, and which is also what makes the moral objection above bite.

[GAP] Alesina & Glaeser 2004 not verified from primary; do not quote a number from it.
[GAP] Edo et al. 2019 and Halla et al. 2017 point coefficients (only shares-of-variance and
signs pulled). [GAP] Alesina & Tabellini 2024 JEL survey unread — that is the first thing a
re-dispatch should read, since it is the field's own reconciliation of this exact chain.
