claude-opus-5[1m]

# Canon Citation Audit — Most-Cited Low-Skill Immigration Economics Papers

**Verdict:** Neither canon is mostly wrong. One paper per side has a defective *result* (Borjas 2017 on the con side, a ~17-observations-per-year artifact; Longhi et al. 2005 on the pro side, but only as an estimate rather than as a description of its literature). The dominant failure on both sides is **over-citation** — a correct result quoted for a claim it does not support — and it is about twice as common on the pro side by count, while the con side's single result-level error is more severe. The deeper problem is structural: the pro canon rests largely on one identification strategy (the past-settlement shift-share instrument) that Jaeger, Ruist & Stuhler show is biased against detecting short-run effects, and the con canon rests largely on one author's national skill-cell calibrations with capital held fixed, which is biased the other way. The two cleanest exogenous shocks in the audit land between them and say the durable cost is an entry-cohort and employment-entry effect that neither camp's headline estimand measures.

Purpose: rank the most-cited economics papers on low-skill immigration's wage/employment/fiscal/welfare effects by Semantic Scholar `citationCount`, split pro-side vs con-side, and audit each for (i) whether the result is wrong and (ii) whether the result is right but routinely over-cited for a claim it does not support.

Model self-report: `claude-opus-5[1m]` (verbatim from environment-info block).

## Status log

- 2026-09-17 — citation pull complete (S2 keyed + OpenAlex cross-check), 26 papers audited, full text read for 3. Memo COMPLETE; open gaps listed in §5.

---

## 1. How the counts were obtained, and why one column is [DEGRADED]

Counts are Semantic Scholar `citationCount`, fetched **2026-09-17** with an API key via the `/graph/v1/paper/batch`, `/paper/search` and `/author/{id}/papers` endpoints. Full per-paper rows with S2 paper IDs are in [`notes/canon-citation-counts-2026-09-17.csv`](../notes/canon-citation-counts-2026-09-17.csv).

**S2 fragments this literature badly, and the fragmentation is not random.** Economics canon circulates as NBER working paper, discussion paper, journal article and reprinted book chapter; S2 sometimes consolidates these and sometimes does not. Concretely:

- **Borjas (2003), the single most-cited con-side paper, has no consolidated S2 record.** The only S2 hits for its exact title are stubs at **3** and **1** citations. OpenAlex carries it at **1,889**. Ranking the con side on S2 alone would have ranked the field's most influential adverse-effects paper below its own comment. [SOURCE: S2 `/paper/search` for "Reexamining the Impact of Immigration on the Labor Market", 2026-09-17]
- **Card (1990) is the mirror image:** S2 **1,885**, OpenAlex **4**. Each index drops a different paper.
- Peri & Sparber (2009), Longhi et al. (2005), Friedberg & Hunt (1995), Clemens & Hunt (2019) and Hunt & Gauthier-Loiselle (2010) have no consolidated S2 record at the published DOI; the count shown is the working-paper or SSRN record.
- Manacorda, Manning & Wadsworth (2012) reads 116 on S2 and 568 on OpenAlex.

Every affected row is tagged `[DEGRADED]` in the CSV with the substitute record named. **Ranks below are S2-primary with an OpenAlex column; where S2 has no usable record, the OpenAlex count sets the rank and this is stated in-line.** No rank in this memo should be treated as precise to better than roughly ±3 positions. [INFERENCE]

**Verified negative — the advocacy con side is absent from the citation record.** S2 searches for Camarota / Center for Immigration Studies and Rector & Richwine / Heritage return no item with a scholarly citation footprint; the highest hit is an 18-citation CIS backgrounder, and the Heritage query returns nothing. The consequence for this audit is structural: on the con side, "most-cited" means **Borjas**, six of the top eight slots. The pro side is split across Card, Peri, Clemens, Dustmann and Cortes. A reader should not infer that con-side arguments are rarer than pro-side ones — only that the ones carrying citations are one research program. [SOURCE: S2 `/paper/search`, 2026-09-17] [INFERENCE]

## 2. Summary table

Rank is within side. `S2` = Semantic Scholar citationCount, 2026-09-17. `OA` = OpenAlex `cited_by_count`, same date, shown because of the fragmentation above.

### Pro side — small or positive native effects, large aggregate gains

| # | Paper | S2 | OA | Verdict | One-line reason |
|---|---|---:|---:|---|---|
| 1 | Card 2001, *Immigrant Inflows, Native Outflows* (JOLE) | 2349 | 1796 | HOLDS-NARROWLY | The past-settlement instrument it popularised is shown by Jaeger–Ruist–Stuhler to conflate short- and long-run responses; its own low-skill results are negative, not null. |
| 2 | Card 1990, Mariel (ILRR) | 1885 | 4 | HOLDS | Repo-confirmed for the episode (ladder 44); the contrary magnitude is the artifact. Over-cited as a general proof. |
| 3 | Ottaviano & Peri 2012 (JEEA) | 1367 | 1368 | HOLDS-NARROWLY | +0.6% average native is a model output that works by reallocating the loss onto prior immigrants (−6.7%); the elasticity producing it is sample-fragile. |
| 4 | Card 2005, *Is the New Immigration Really So Bad?* (EJ) | 1100 | 844 | UNRESOLVED | Turns on whether dropouts and high-school graduates are near-perfect substitutes — the exact parameter the profession has not settled. |
| 5 | Card 2009, *Immigration and Inequality* (AER P&P) | 868 | 785 | HOLDS | Small contribution to measured inequality is right; routinely over-cited past its own bottom-decile result. |
| 6 | Peri & Sparber 2009 (AEJ: Applied) `[DEGRADED]` | 806 | 896 | HOLDS-NARROWLY | Task specialisation is real; measuring it from education cells is undercut by immigrant downgrading (Dustmann–Frattini–Preston). |
| 7 | Friedberg & Hunt 1995 (JEP) `[DEGRADED]` | 770 | 1129 | HOLDS-NARROWLY | An accurate 1995 summary of a literature whose shared identification strategy was later shown to be biased. |
| 8 | Dustmann, Frattini & Preston 2013 (REStud) | 744 | 771 | HOLDS | Cited as pro; it reports wage *declines* in the bottom decile. |
| 9 | Clemens 2011, *Trillion-Dollar Bills* (JEP) | 598 | 153 | HOLDS | The paper is explicit that its large numbers are model outputs; the over-citation is not its defect. |
| 10 | Cortes 2008 (JPE) | 570 | 518 | HOLDS | The price channel is real and identified; it is cited past its own low-skill wage result. |
| 11 | Peri 2012, productivity (REStat) | 529 | 591 | UNRESOLVED | Same past-settlement instrument, same Jaeger–Ruist–Stuhler problem, applied to a TFP outcome. |
| 12 | Manacorda, Manning & Wadsworth 2012 (JEEA) `[DEGRADED]` | 116 | 568 | HOLDS-NARROWLY | Independent UK confirmation that incidence falls on earlier immigrants, not natives. |
| — | Longhi, Nijkamp & Poot 2005 meta `[DEGRADED]` | 441 | 392 | WRONG-AS-USED | A meta-analysis cannot average away an identification defect common to its inputs. |

### Con side — adverse native wage/employment effects, fiscal costs

| # | Paper | S2 | OA | Verdict | One-line reason |
|---|---|---:|---:|---|---|
| 1 | Borjas 2003, *The Labor Demand Curve Is Downward Sloping* (QJE) | n/a `[DEGRADED]` | 1889 | HOLDS-NARROWLY | The headline −3.2% / −8.9% are short-run, capital-fixed simulation outputs; the paper says so in its own footnote 28 and conclusion. |
| 2 | Borjas, Freeman & Katz 1997 (BPEA) | 977 | 896 | HOLDS-NARROWLY | A factor-proportions accounting decomposition conditional on assumed elasticities, not a causal estimate. |
| 3 | Borjas 1994, *The Economics of Immigration* (JEL) | 910 | — | HOLDS-NARROWLY | Survey; its cohort-quality-decline thesis is contested by later assimilation work. |
| 4 | Borjas 1999, *Immigration and Welfare Magnets* (JOLE) | 848 | 539 | UNRESOLVED | Post-1996 replications do not reproduce the welfare-generosity location effect. |
| 5 | Borjas 2006, *Native Internal Migration* (JHR) | 613 | 447 | HOLDS-NARROWLY | Direction granted by this repo; the 40–60% magnitude is specification-sensitive and is not a correction factor for any other study. |
| 6 | Borjas 1996, *Searching for the Effect* (NBER w5454) | 545 | — | HOLDS-NARROWLY | Precursor to 2003; same closed-economy, fixed-capital frame. |
| 7 | Jaeger, Ruist & Stuhler 2018 (NBER w24285) | 374 | — | HOLDS | The most consequential live methodological finding on either side, and the most under-cited relative to its implications. |
| 8 | Dustmann, Schönberg & Stuhler 2017 (QJE) | 302 | 276 | HOLDS | Clean design; the adverse margin is native employment, not wages. |
| 9 | National Academies 2016 (fiscal chapters) | 252 | 291 | HOLDS-NARROWLY | Assumption-sensitive on public goods and descendants; over-cited by both sides from different scenarios of the same report. |
| 10 | Borjas 2017, Mariel reappraisal (ILRR) | 168 | 160 | WRONG | ~17 observations/year after a four-way sample cut, riding a 55pp black-share jump and a CPS frame change (ladder 44). |
| 11 | Monras 2020, peso crisis (JPE) | 142 | 193 | HOLDS | Not really a con paper: it shows a short-run negative effect that dissipates, which reconciles both sides. |
| 12 | Borjas, Grogger & Hanson 2012, comment (JEEA) | 110 | 96 | HOLDS-NARROWLY | Shows the OP elasticity is sample-fragile; does not establish perfect substitution. |
| — | Storesletten 2000 (JPE) | 632 | 539 | HOLDS-NARROWLY | Cited by both sides; the result is explicitly conditional on admitting *skilled* working-age immigrants. |


## 3. Per-paper audit

Each entry: **(a)** claim, **(b)** identification, **(c)** strongest published rebuttal or replication, **(d)** what this repo's own evidence says, **(e)** verdict, **(f)** falsification condition. Steel-man precedes verdict throughout. Where this repo has already adjudicated a paper, the ladder entry is cited rather than re-derived.

### 3.1 Pro side

---

#### P1. Card (2001), *Immigrant Inflows, Native Outflows, and the Local Labor Market Impacts of Higher Immigration*, JOLE — S2 2349 / OA 1796

**Steel-man.** This is the paper that made area studies defensible. It builds the occupation-specific past-settlement instrument, tests the native-flight objection directly rather than assuming it away, and finds it empirically small. Its design became the workhorse for two decades.

**(a) Claim.** Verbatim from the abstract: "intercity mobility rates of natives and earlier immigrants are insensitive to immigrant inflows. However, occupation-specific wages and employment rates are systematically lower in cities with higher relative supplies of workers in a given occupation. The results imply that immigrant inflows over the 1980s reduced wages and employment rates of low-skilled natives in traditional gateway cities like Miami and Los Angeles by **1–3 percentage points**." [SOURCE: 10.1086/209979, S2 abstract, fetched 2026-09-17]

**(b) Identification.** 1990 Census, 175 cities; occupation-specific immigrant supply instrumented by the interaction of national origin-group inflows with each city's 1980 origin-group distribution (the "past settlement" or shift-share instrument, with Altonji & Card 1991).

**(c) Strongest rebuttal.** Jaeger, Ruist & Stuhler (2018), NBER w24285 [SOURCE: full text, fetched 2026-09-17]. Verbatim: "If the spatial distribution of immigrant inflows is stable over time, the instrument is likely to be correlated with ongoing responses to previous supply shocks. Estimates based on the conventional shift-share instrument are therefore unlikely to identify the short-run causal effect." Their multiple-instrumentation correction finds the short-run effect "substantially more negative," and greater "for natives with a high school degree or less" and for young workers. Goldsmith-Pinkham, Sorkin & Swift (2020), AER, S2 2056 [SOURCE: 10.1257/aer.20181047] adds that the identifying assumption sits on the *shares*, not the national shifts, so exogeneity has to be argued origin-group by origin-group.

**(d) Repo evidence.** Ladder 19 rates the Card-side bounded-wage-impact reading "medium-strong" and explicitly calls it "a cross-design external-validity pattern, not one pooled U.S. estimate." Ladder 29 bounds it further to marginal-policy variation. Ladder 53 removed the QWI component from 19 because that series has no nativity field.

**(e) Verdict: HOLDS-NARROWLY.** Two separable parts. The **native-mobility null** holds and is independently supported by Peri & Sparber (2011), below. The **wage/employment magnitudes** are not identified as short-run causal effects under the instrument as used, per Jaeger–Ruist–Stuhler. Scope: a long-run, partly-adjusted association across cities.

**(f) Falsification.** Re-estimate Card's own 1985–1990 sample with the multiple-instrumentation procedure. If the corrected short-run coefficients are close to the published ones, the Jaeger–Ruist–Stuhler critique does not bind here.

**Over-citation.** This is the clearest case in the pro canon. Card (2001) is cited as the definitive demonstration that immigration does not hurt native workers, while the paper's own abstract reports a **1–3 percentage point** reduction in wages and employment rates for low-skilled natives in gateway cities. The citable finding is "no native flight," not "no effect."

---

#### P2. Card (1990), *The Impact of the Mariel Boatlift on the Miami Labor Market*, ILRR — S2 1885 / OA 4 `[index-fragmented]`

**Steel-man.** A 7% overnight labor-force shock concentrated in exactly the competing skill segment is the closest thing labor economics has to a controlled supply experiment, and the wage and unemployment paths of less-skilled Miami workers tracked the comparison cities.

**(a)–(b)** Difference-in-differences, Miami versus four comparison cities, CPS.

**(c) Rebuttal chain.** Borjas (2017) reappraisal → Clemens & Hunt (2019) → Peri & Yasenov (2019) → Borjas (2019) "The Role of Race." Adjudicated below at C10.

**(d) Repo evidence.** Ladder 44: Borjas's contrary magnitude is the artifact, not Card's null. Ladder 44 also declines to call the question closed, keeping Borjas (2019) as a live counter.

**(e) Verdict: HOLDS** for the episode. Its published limits are the paper's own: Card discusses endogenous location choice on his first page and warns that Miami's prior immigration and industry mix limit generalisation [SOURCE: `immigration-dismantle-card-peri-2026-06-25.md`, current section, citing Card 1990 pp. 245, 255–257].

**(f) Falsification.** A design that recovers a large Miami wage effect on a sample that is not knife-cut, and that passes a schooling-as-outcome placebo.

**Over-citation.** Cited as a general proof that labor-supply shocks do not move wages. It is one city, one episode, with a documented escape valve (reduced in-migration) that a nationwide inflow does not have. The repo's own kill A.

---

#### P3. Ottaviano & Peri (2012), *Rethinking the Effect of Immigration on Wages*, JEEA — S2 1367 / OA 1368

**(a) Claim.** Published headline: immigration over 1990–2006 raised average native wages about **+0.6%** and lowered prior immigrants' wages about **−6.7%** in the long run, under the preferred nested-CES specification. [SOURCE: ladder 59; publisher abstract]

**(b) Identification.** Structural nested-CES general equilibrium with an *estimated* immigrant–native substitution elasticity within education-experience cells, plus long-run capital adjustment.

**(c) Rebuttal.** Borjas, Grogger & Hanson (2012) JEEA comment, S2 110 [SOURCE: 10.1111/j.1542-4774.2011.01055.x], and the earlier NBER w13887: the imperfect-substitution finding is sample-fragile and "evaporates simply by removing high school students from the data."

**(d) Repo evidence.** Ladder 59 corrects the version error directly: the **−19%** figure circulating in critiques is from the NBER w12497 draft, not the published paper. The dismantle memo's current section grants the mechanism and the average and kills only the "no one is hurt" reading.

**(e) Verdict: HOLDS-NARROWLY.** Scope: a model output for 1990–2006 under a specific elasticity, not an observed wage change. The average is positive *because* the model reallocates incidence onto prior immigrants; that is a property of the model, and it is in the paper.

**(f) Falsification.** An estimate of the within-cell immigrant–native elasticity that is robust to the high-school-student sample choice and is indistinguishable from infinity.

**Over-citation.** "+0.6% for natives" is quoted as the effect of immigration on workers, dropping the −6.7% for prior immigrants that appears in the same table. The critique side's mirror-image error is quoting −19%/−24% from the superseded draft as if they were the published result — a failure this repo committed and corrected on 2026-09-05.

---

#### P4. Card (2005), *Is the New Immigration Really So Bad?*, EJ — S2 1100 / OA 844

**(a) Claim.** The relative supply of dropout labor is not meaningfully raised by immigration because dropouts and high-school graduates are close to perfect substitutes; therefore the skill-cell channel through which Borjas finds large dropout losses is largely absent.

**(b) Identification.** Cross-city relative supply/relative wage regressions plus direct estimation of the dropout / high-school-graduate elasticity.

**(c) Rebuttal.** Borjas (2003) and Borjas, Grogger & Hanson (2012) treat dropouts as a distinct skill group; Borjas's own 2003 simulation delivers −8.9% for dropouts precisely because they are not pooled.

**(d) Repo evidence.** The repo logs the low-skill distributional question as unresolved (dismantle memo, Claim 2).

**(e) Verdict: UNRESOLVED.** This is the single pivot parameter of the whole wage debate. Card (2009) states the assumption explicitly: "workers with below high school education are perfect substitutes for those with a high school education" [SOURCE: 10.1257/aer.99.2.1, abstract, fetched 2026-09-17]. Borjas denies it. Both headline results follow mechanically from that one choice, and neither side has produced an estimate the other accepts.

**(f) Falsification.** A design that identifies the dropout / high-school-graduate elasticity off variation other than the immigrant inflow itself — for example a compulsory-schooling or GED-policy shock — and that both camps pre-commit to.

---

#### P5. Card (2009), *Immigration and Inequality*, AER P&P — S2 868 / OA 785

**(a) Claim.** Verbatim: "immigration accounts for a small share (5%) of the increase in U.S. wage inequality." The effects on *overall* inequality are larger than on native relative wages, "reflecting the concentration of immigrants in the tails of the skill distribution and higher residual inequality among immigrants than natives." [SOURCE: 10.1257/aer.99.2.1, abstract]

**(e) Verdict: HOLDS.** The decomposition is sound on its own terms.

**Over-citation.** Two distinct claims in one abstract get merged. "5% of the rise in inequality" is a statement about *native relative wages under the perfect-substitutes assumption*; the paper separately says overall inequality effects "are larger." Citing the 5% as the paper's finding about inequality generally drops the second sentence and the assumption in conclusion (1).

---

#### P6. Peri & Sparber (2009), *Task Specialization, Immigration, and Wages*, AEJ: Applied — S2 806 `[DEGRADED: CReAM DP record]` / OA 896

**(a) Claim.** Immigrants specialise in manual/physical tasks, pushing natives toward communication-intensive tasks, which limits head-to-head wage competition within an education cell.

**(c) Rebuttal.** Dustmann, Frattini & Preston (2013), REStud, S2 744, verbatim: "we demonstrate that immigrants downgrade considerably upon arrival" [SOURCE: 10.1093/restud/rds019, abstract]. If immigrants work below their measured education, task shares measured off education cells mis-locate who actually competes with whom, and the same evidence that supports task reallocation also implies the competition is with lower-paid natives than the cells suggest.

**(d) Repo evidence.** The dismantle memo flags this paper as `[GAP]` — granted on the strength of Ottaviano–Peri's account rather than a primary fetch. That gap is not closed here either.

**(e) Verdict: HOLDS-NARROWLY.** The mechanism is real; the magnitude of protection it confers depends on a task measure built from occupation averages within education cells that downgrading undermines.

**(f) Falsification.** Task-share estimates built from observed job content rather than education cells that show no native reallocation after an inflow.

---

#### P7. Friedberg & Hunt (1995), JEP — S2 770 `[DEGRADED]` / OA 1129

**(a) Claim.** The empirical literature shows small native wage and employment effects of immigration.

**(e) Verdict: HOLDS-NARROWLY.** It is an accurate 1995 summary of the area-study literature. It is not an independent estimate, and the identification strategy common to nearly all of its inputs was later shown to be biased (Jaeger–Ruist–Stuhler). A survey inherits its inputs' defects.

**Over-citation.** Still quoted in policy writing as the settled state of knowledge, thirty years and one identification revolution later.

---

#### P8. Dustmann, Frattini & Preston (2013), *The Effect of Immigration along the Distribution of Wages*, REStud — S2 744 / OA 771

**(a) Claim.** Verbatim: "immigration depresses wages below the 20th percentile of the wage distribution but leads to slight wage increases in the upper part of the wage distribution." [SOURCE: 10.1093/restud/rds019, abstract]

**(e) Verdict: HOLDS.** Strong design; it deliberately avoids pre-allocating immigrants to skill cells, which sidesteps the Card-versus-Borjas cell dispute.

**Over-citation, both directions.** Cited on the pro side for "slightly positive overall effect on native wages" and on the con side for "immigration lowers wages at the bottom." Both halves are in the abstract. The paper's actual contribution is that *the two are simultaneously true*, and it names the mechanism (downgrading).

---

#### P9. Clemens (2011), *Economics and Emigration: Trillion-Dollar Bills on the Sidewalk?*, JEP — S2 598 / OA 153

**(a)–(b)** A survey of model-based estimates of global gains from labor mobility, plus the place-premium literature on wage gaps for observationally identical workers.

**(d) Repo evidence.** `immigration-dismantle-clemens-2026-06-25.md` (current section): the place premium is well identified for observed or marginal movers; the large global numbers are model outputs conditional on assumptions about capital, institutions and housing after mass relocation. The repo's own calibration at $7,500 per migrant per year and $110T world GDP gives 3B additional migrants ≈ **20.45%** of world GDP, not a doubling. The repo also withdrew its earlier "4% ceiling" kill: the published Docquier, Machado & Sekkat (2015) benchmark is **11.5–12.5%** medium-term, robustness **7.0–17.9%** [SOURCE: 10.1111/sjoe.12097].

**(e) Verdict: HOLDS.** The paper is explicit that it reports model estimates and distinguishes partial from complete liberalisation.

**Over-citation — the largest gap between paper and usage in this audit.** "Open borders would double world GDP" is presented as an economic estimate. Clemens's paper is a survey of what a class of models produces under stated assumptions. The repo's arithmetic shows the headline is not reachable from conservative per-mover gains at any plausible migration volume.

---

#### P10. Cortes (2008), *The Effect of Low-Skilled Immigration on U.S. Prices*, JPE — S2 570 / OA 518

**(a) Claim.** Verbatim: "a 10 percent increase in the share of low-skilled immigrants in the labor force decreases the price of immigrant-intensive services, such as housekeeping and gardening, by 2 percent. Wage equations suggest that lower wages are a likely channel through which these effects take place. However, wage effects are significantly larger for low-skilled immigrants than for low-skilled natives." [SOURCE: 10.1086/589756, abstract]

**(b) Identification.** Shift-share IV across cities and time on CPI microdata — same instrument class, same Jaeger–Ruist–Stuhler exposure.

**(e) Verdict: HOLDS** on the price channel, which is a genuine consumer-surplus benefit that restrictionist ledgers omit.

**Over-citation.** Used as "immigration makes everyone better off." The paper states the price fall *runs through lower wages*, and that the wage incidence lands mostly on earlier low-skilled immigrants. It is a transfer-plus-surplus result, not a free lunch, and the gain accrues to purchasers of those services.

---

#### P11. Peri (2012), *The Effect of Immigration on Productivity: Evidence from U.S. States*, REStat — S2 529 / OA 591

**(a) Claim.** Immigration raises total factor productivity at the state level through efficient task specialisation, with no effect on capital intensity or skill bias.

**(b) Identification.** Past-settlement shift-share instrument across states.

**(e) Verdict: UNRESOLVED.** The outcome variable changed; the instrument did not. Jaeger–Ruist–Stuhler's argument applies whatever is on the left-hand side: if the instrument correlates with ongoing adjustment to prior inflows, a TFP coefficient conflates the same horizons.

**(f) Falsification.** A TFP estimate using the composition-change instrument that reproduces the published magnitude.

---

#### P12. Manacorda, Manning & Wadsworth (2012), JEEA — S2 116 `[DEGRADED]` / OA 568

**(a) Claim.** In Britain, immigrants and natives are imperfect substitutes within education-experience cells; the wage incidence of immigration falls on **earlier immigrants**, not natives.

**(e) Verdict: HOLDS-NARROWLY.** A genuinely independent confirmation of the Ottaviano–Peri structural result in a different country and dataset, which raises the pro side's credibility on incidence. Its scope limit is the same: the loser group is real, and the headline "natives unaffected" is true only because that group is not native.

---

#### P13. Longhi, Nijkamp & Poot (2005), meta-analysis, JES — S2 441 `[DEGRADED: SSRN record]` / OA 392

**(a) Claim.** Across 348 estimates from 18 studies, the mean wage effect of a 1 percentage point increase in the immigrant share is about −0.1%.

**(e) Verdict: WRONG-AS-USED.** The estimate of the literature's central tendency is correct. Using it as an estimate of the causal effect is not: the inputs are overwhelmingly area studies sharing the past-settlement instrument, so the meta-mean averages over correlated, same-signed bias rather than independent draws. Meta-analysis corrects sampling noise, not a common identification defect.

**(f) Falsification.** A meta-analysis restricted to designs that do not use the past-settlement instrument, recovering the same mean.

---

### 3.2 Con side

---

#### C1. Borjas (2003), *The Labor Demand Curve Is Downward Sloping*, QJE — S2 record unavailable `[DEGRADED]` / OA 1889

**Steel-man.** This is the strongest paper in the adverse-effects literature and the only one that reframed the field. Its argument is that area studies cannot see a national effect because labor and capital arbitrage across cities, so the right unit is the national education-experience cell, where immigration's supply shift genuinely varies. That is a correct diagnosis of a real problem, and the resulting correlation is negative and robust across cells and decades.

**(a) Claim.** Verbatim from the abstract: "immigration lowers the wage of competing workers: a 10 percent increase in supply reduces wages by 3 to 4 percent." Simulation for 1980–2000, verbatim: "the immigrant influx reduced the wage of the average native worker by **3.2 percent**. The wage impact differed dramatically across education groups, with the wage falling by **8.9 percent** for high school dropouts, **4.9 percent** for college graduates, **2.6 percent** for high school graduates, and barely changing for workers with some college." Own factor-price elasticities "cluster between −0.3 and −0.4." [SOURCE: NBER w9755 full text, fetched 2026-09-17]

**(b) Identification.** 1960–2000 Census/CPS; 32 national education-experience cells; wage regressed on the immigrant share of the cell with education, experience and period fixed effects. The simulation is a nested-CES calibration, **not** a regression output.

**(c) Strongest rebuttal.** Ottaviano & Peri (2012) reverse the sign of the average effect by estimating rather than assuming the immigrant–native elasticity and letting capital adjust. Card (2009) removes most of the dropout result by rejecting the dropout / high-school-graduate distinction. Card (2012) JEEA comment presses the same point.

**(d) Repo evidence.** Ladder 53 withdrew the repo's own QWI-based test of Borjas-style magnitudes, so the repo has no independent wage estimate to set against this paper. Ladder 29 forbids extrapolating any of it to the 2021–2024 surge.

**(e) Verdict: HOLDS-NARROWLY.** The negative national skill-cell correlation is a real empirical fact and survives. The famous numbers are not estimates of the effect of immigration; they are outputs of a calibration with **capital held fixed**, and the paper says so. Footnote 28, verbatim: "The assumption of a constant capital stock implies that the resulting wage consequences should be interpreted as **short-run** impacts. Over time, the changes in factor prices will fuel adjustments in the capital stock that attenuate the wage effects." The conclusion adds, verbatim: "my analysis ignored the long-run capital adjustments induced by immigration, the role played by capital-skill complementarities."

**(f) Falsification.** A skill-cell estimate on a specification that permits within-cell imperfect substitution and long-run capital adjustment, still yielding an average native effect near −3%.

**Over-citation — the most consequential in this audit.** "Immigration cut the wages of high-school dropouts by 8.9%" circulates as *the* measured cost of immigration. It is a short-run, capital-fixed simulation, disclaimed by its own author in a footnote on the page it appears. Anyone citing it as a long-run or realised effect is contradicted by the paper.

---

#### C2. Borjas, Freeman & Katz (1997), *How Much Do Immigration and Trade Affect Labor Market Outcomes?*, BPEA — S2 977 / OA 896

**(a) Claim.** Verbatim: "The impact of post-1979 immigrants on relative skill supplies can explain a 0.030 to 0.060 log point decline (**27 to 55 percent** of the actual decline) in the relative wages of high school dropouts over 1980–95, depending on the wage elasticity chosen." And, in the same conclusion, verbatim: "the impact of increased immigration and LDC trade on the labor market **does not explain much** of the increase in the college wage premium or overall wage inequality in the United States." [SOURCE: BPEA 1997:1 full text, fetched 2026-09-17]

**(b) Identification.** Factor-proportions accounting: national supply shifts combined with assumed wage elasticities. Not a causal design.

**(e) Verdict: HOLDS-NARROWLY.** As an accounting decomposition conditional on the elasticity, it is sound and honestly bounded (the range is stated).

**Over-citation, both directions, from one paper.** The con side quotes a point figure near 44% for the dropout share; the paper gives **27 to 55 percent**, explicitly elasticity-dependent. The pro side quotes the same paper's "does not explain much of overall wage inequality." Both are accurate quotations of different sentences. Neither camp usually reports that the dropout result and the aggregate-inequality result come from the same analysis.

---

#### C3. Borjas (1994), *The Economics of Immigration*, JEL — S2 910

**(a) Claim.** Survey; the load-bearing thesis is declining immigrant cohort quality and slower assimilation across arrival cohorts.

**(c) Rebuttal.** Card (2005) disputes the cohort-quality reading; Abramitzky & Boustan (2017) JEL, S2 275, re-examines assimilation with linked historical data.

**(e) Verdict: HOLDS-NARROWLY** as a survey of its era. The cohort-quality thesis is contested and is sensitive to whether return migration is modelled, since less successful arrivals leave.

---

#### C4. Borjas (1999), *Immigration and Welfare Magnets*, JOLE — S2 848 / OA 539

**(a) Claim.** Immigrant welfare recipients are more geographically clustered in high-benefit states than other immigrants, consistent with welfare-induced location choice.

**(b) Identification.** Cross-state clustering comparison, pre-1996.

**(c) Rebuttal.** Kaushal (2005), *New Immigrants' Location Choices: Magnets without Welfare*, JOLE, S2 135 [SOURCE: 10.1086/425433]. Verbatim: she uses the PRWORA state-restoration variation and finds "safety-net programs have little effect on the location choices of newly arrived low-skilled unmarried immigrant women."

**(e) Verdict: UNRESOLVED, leaning against the magnet reading.** Borjas's clustering result is descriptive and pre-PRWORA; Kaushal's is a policy-variation design that post-dates it and finds no effect. The two are not testing the same regime, so neither refutes the other outright — but the design quality runs against the magnet claim.

**(f) Falsification.** A post-2000 policy-variation design that recovers a benefit-generosity location elasticity for low-skilled arrivals.

---

#### C5. Borjas (2006), *Native Internal Migration and the Labor Market Impact of Immigration*, JHR — S2 613 / OA 447

**(a) Claim.** Native internal migration responds to immigrant inflows; roughly three natives are displaced per ten immigrants at the city level, and this "can account for between 40 to 60 percent of the difference in the measured wage impact of immigration between the national and local labor market level" [SOURCE: NBER w11610, verbatim, via `immigration-dismantle-card-peri-2026-06-25.md`].

**(c) Strongest rebuttal.** Peri & Sparber (2011), *Assessing Inherent Model Bias*, JUE 69(1):82–91 [SOURCE: 10.1016/j.jue.2010.08.005]. Verbatim from the paper's body: "Borjas (2006) specifications are biased toward identifying displacement, and this bias grows larger as the variance of native flows rises in proportion to the variance of immigrant flows independently of their correlation," and "Of the models we explore, only the Borjas (2006) specifications reveal a significantly negative correlation. Given the bias uncovered in Section 3, we suspect that this finding for native displacement is spurious." Card (2001)'s own abstract independently reports mobility rates "insensitive to immigrant inflows." **[FRAMING-SENSITIVE]** Peri is an interested party in this dispute; the microsimulation logic is checkable independently of that, but the paper is not a neutral referee.

**(d) Repo evidence.** The dismantle memo's current section explicitly **withdraws** the repo's earlier use of the 40–60% figure as a correction factor for Card's Mariel coefficient: "Borjas's w11610 estimate … concerns that study's setting. It is not an estimated correction factor for Card's Mariel coefficient."

**(e) Verdict: HOLDS-NARROWLY.** The *existence* of a native-mobility channel is a valid methodological point that this repo grants. The *magnitude* is specification-dependent, and the one specification that produces it is the one Peri & Sparber show is mechanically biased toward it.

**(f) Falsification.** A displacement estimate from a specification that passes the microsimulation placebo — recovering zero when the data-generating process has zero — and still finds three-for-ten.

---

#### C6. Borjas (1996), *Searching for the Effect of Immigration on the Labor Market*, NBER w5454 — S2 545

Precursor to C1; same closed-economy, fixed-capital frame. **Verdict: HOLDS-NARROWLY**, subsumed by C1.

---

#### C7. Jaeger, Ruist & Stuhler (2018), *Shift-Share Instruments and the Impact of Immigration*, NBER w24285 — S2 374

**(a) Claim.** Verbatim from the abstract: "estimates based on this 'shift-share' instrument conflate the short- and long-run responses to immigration shocks … Estimates based on the conventional shift-share instrument are therefore unlikely to identify the short-run causal effect. … Our results are a cautionary tale for a large body of empirical work, not just on immigration." [SOURCE: NBER w24285 full text, fetched 2026-09-17]

**(b) Identification.** Multiple instrumentation isolating spatial variation arising from *changes in origin-country composition* at the national level, separating short- from long-run effects.

**(c) Rebuttal / complement.** Goldsmith-Pinkham, Sorkin & Swift (2020), AER, S2 2056, and Borusyak, Hull & Jaravel (2022), REStud [SOURCE: 10.1093/restud/rdab030] develop the shares-versus-shifts exogeneity conditions. These refine rather than reject the critique.

**(e) Verdict: HOLDS.** This is the most consequential live methodological finding on either side of the debate. It does not decide the sign of the effect; it says a large fraction of the published estimates on both sides do not measure what they claim to measure.

**Under-citation, not over-citation.** At 374 S2 citations it sits below Card (2001)'s 2349, Peri (2012)'s 529 and Cortes (2008)'s 570 — three papers it directly implicates. A field that had internalised it would cite it alongside every shift-share immigration estimate. This is the one paper in the audit whose problem is that it is cited **too little**.

---

#### C8. Dustmann, Schönberg & Stuhler (2017), *Labor Supply Shocks, Native Wages, and the Adjustment of Local Employment*, QJE — S2 302 / OA 276

**(a) Claim.** Verbatim: "the supply shock leads to a moderate decline in local native wages and a sharp decline in local native employment … the employment response is almost entirely driven by diminished inflows of natives into work rather than outflows into other areas or nonemployment, suggesting that 'outsiders' shield 'insiders' from the increased competition." [SOURCE: 10.1093/qje/qjw032, abstract, fetched 2026-09-17]

**(b) Identification.** A commuting-policy change producing a sharp, unexpected inflow of Czech workers to the German border region. One of the cleanest exogenous shocks in the literature.

**(e) Verdict: HOLDS.** Clean design, precisely stated.

**What it changes.** It relocates the whole argument. The adverse margin is **employment entry**, not the wage, and it falls on labor-market outsiders. A literature that argues about wage elasticities is measuring the wrong outcome if wage rigidity pushes the incidence onto hiring. Neither camp's headline captures this.

---

#### C9. National Academies (2016), *The Economic and Fiscal Consequences of Immigration* — S2 252 / OA 291

**(d) Repo evidence.** `immigration-nas-scope-and-bias-update-2026-04-10.md`: NAS is "not junk and not obviously unusable" but "highly assumption-sensitive, especially on public-goods assignment and descendant treatment." The largest sensitivity is whether immigrants are assigned *average* or *marginal* cost of public goods such as defence and debt interest [SOURCE: Orrenius 2017, 10.24149/wp1704]. Descendants are already a separate component of the totals, so the large negative figures are not adult-only.

**(e) Verdict: HOLDS-NARROWLY.** A transparent lifetime fiscal scaffold, not "the one true lifetime number."

**Over-citation by both sides from the same book.** The restrictionist side quotes the state-and-local net cost; the pro side quotes the second generation as the strongest fiscal contributor and the long-run federal surplus. Both appear in the report under different scenarios. Neither camp reports which public-goods assumption generated the figure it quotes, which is the variable that moves the sign.

---

#### C10. Borjas (2017), *The Wage Impact of the Marielitos: A Reappraisal*, ILRR — S2 168 / OA 160

**(a) Claim.** The Mariel boatlift reduced wages of Miami high-school dropouts by 10–30%.

**(d) Repo evidence — this is a repo-adjudicated WRONG.** Ladder 44: the result "survives only under a 4-way knife-cut (non-Hispanic men 25–59, dropouts) that discards **91%** of low-skill Miami workers, leaving **~17 obs/yr**, and rides a **55pp black-share jump** (1980 Haitian-refugee arrival plus a March-1981 CPS sampling-frame change); a schooling-as-outcome falsification (the boatlift spuriously 'causes' −0.444 years of schooling) confirms compositional contamination. Broadened sample → effect ≈ zero; Peri–Yasenov synthetic control agrees (~null)." [SOURCE: 10.3386/w23433; 10.3368/jhr.54.2.0217.8561R1]

**(e) Verdict: WRONG.** Defect: the estimate is not robust to sample definition and fails a placebo whose outcome cannot have been caused by the treatment. Ladder 44 keeps Borjas (2019) "The Role of Race" as a live counter and declines to call the question formally closed, so this is a strong artifact finding rather than a settled retraction.

**(f) Falsification.** A Mariel estimate on the full low-skill Miami sample, passing the schooling placebo, that recovers a double-digit wage decline.

---

#### C11. Monras (2020), *Immigration and Wage Dynamics: Evidence from the Mexican Peso Crisis*, JPE — S2 142 / OA 193

**(a) Claim.** Verbatim: "In the short run, high-immigration locations see their low-skilled labor force increase, native low-skilled wages decrease, and the relative price of rentals increase. Internal relocation dissipates this shock spatially. In the long run, the only lasting consequences are (a) worse labor market conditions for low-skilled natives who entered the labor force in high-immigration years, and (b) lower housing prices in high-immigrant locations." [SOURCE: 10.1086/707764, abstract, fetched 2026-09-17]

**(e) Verdict: HOLDS**, and it is misfiled as a con paper. It is a reconciliation: both camps are right about different horizons, and the durable cost is a **cohort** effect on natives who entered the labor market during the inflow — a group neither side's headline estimand isolates.

---

#### C12. Borjas, Grogger & Hanson (2012), *Comment: On Estimating Elasticities of Substitution*, JEEA — S2 110 / OA 96

**(a) Claim.** The Ottaviano–Peri imperfect-substitution finding is fragile to sample construction; perfect substitution cannot be rejected using standard methods.

**(e) Verdict: HOLDS-NARROWLY.** Demonstrating fragility is not demonstrating perfect substitution. Failing to reject a null is not evidence for it, a point this repo has had to enforce against itself repeatedly (ladder 53: "Non-significance is not equivalence").

**Provenance note.** The dismantle memo records that the widely quoted "evaporates" wording comes from NBER w13887 (2008), not from this published comment, and that the repo re-attributed it on quote-verification. A citation audit that did not check would have mis-sourced it.

---

#### C13. Storesletten (2000), *Sustaining Fiscal Policy through Immigration*, JPE — S2 632 / OA 539

**(a) Claim.** A calibrated overlapping-generations model in which admitting a large annual inflow of **high- and medium-skilled working-age** immigrants can close the US fiscal gap.

**(e) Verdict: HOLDS-NARROWLY.** Its conclusion is explicitly conditional on skill and age selection, which makes it evidence *against* treating low-skill inflows as fiscally equivalent.

**Over-citation.** Quoted as "immigration fixes the entitlement shortfall." The model's answer for low-skilled arrivals is the opposite sign, and the required volumes are large.


## 4. Which side is more often wrong, and how

### Counts

Thirteen papers audited per side.

| Verdict | Pro side | Con side |
|---|---:|---:|
| HOLDS | 5 | 3 |
| HOLDS-NARROWLY | 5 | 8 |
| UNRESOLVED | 2 | 1 |
| WRONG (result is wrong) | 0 | 1 |
| WRONG-AS-USED (result right, usage wrong) | 1 | 0 |

**Result-level wrongness is a near-tie at one paper each, and both are Mariel-adjacent or usage-level.** On the con side, Borjas (2017) is a genuine defective result: ~17 observations per year after a four-way sample cut, failing a placebo. On the pro side, no audited paper's result is wrong; the one WRONG verdict is Longhi et al. (2005), and it is wrong only as an estimate of the causal effect, because meta-analysis cannot average away an identification defect shared by its inputs.

### The dominant failure mode is over-citation, and it is more common on the pro side

Over-citation flagged in **8 of 13** pro papers versus **4 of 13** con papers, plus one con paper that is *under*-cited.

| Paper | Cited for | What it actually says |
|---|---|---|
| Card 2001 | "Immigration does not hurt native workers" | Its own abstract: inflows "reduced wages and employment rates of low-skilled natives in traditional gateway cities like Miami and Los Angeles by 1–3 percentage points" |
| Card 1990 | A general proof that supply shocks do not move wages | One city, one episode; Card warns on pp. 245, 255–257 that Miami's prior immigration and industry mix limit generalisation |
| Ottaviano–Peri 2012 | "+0.6% for workers" | +0.6% for **natives**, −6.7% for **prior immigrants**, in the same specification |
| Card 2009 | "Immigration explains only 5% of rising inequality" | 5% is the native-relative-wage share under an assumed perfect dropout/high-school substitutability; the paper separately says overall inequality effects "are larger" |
| Cortes 2008 | "Immigration lowers prices, everyone gains" | The price fall runs *through lower wages*, with incidence concentrated on earlier low-skilled immigrants |
| Clemens 2011 | "Open borders would double world GDP" | A survey of model outputs under stated assumptions; the repo's own calibration gives ~20% of world GDP at 3B movers, not 100% |
| Dustmann–Frattini–Preston 2013 | "Immigration slightly raises native wages" | And "depresses wages below the 20th percentile" — both halves are in the abstract |
| Friedberg & Hunt 1995 | The settled state of knowledge | A 1995 survey of a literature whose shared instrument was later shown to be biased |
| **Borjas 2003** | "Immigration cut dropout wages 8.9%" | A **short-run, capital-fixed** simulation; footnote 28 says capital adjustment attenuates it and the conclusion lists the omissions |
| **Borjas–Freeman–Katz 1997** | A point figure near 44% of the dropout wage decline | **27 to 55 percent**, "depending on the wage elasticity chosen" — and the same conclusion says immigration "does not explain much" of overall inequality |
| **National Academies 2016** | Either the state-local cost or the second-generation surplus | Both, under different public-goods and descendant assumptions; the assumption that moves the sign is almost never reported with the number |
| **Storesletten 2000** | "Immigration fixes the fiscal gap" | Conditional on admitting high- and medium-skilled working-age immigrants; the sign reverses for low-skill inflows |
| Jaeger–Ruist–Stuhler 2018 | *Under-cited*: 374 citations against the 2349, 570 and 529 of three papers it directly implicates | A cautionary tale "for a large body of empirical work" that the body has largely not absorbed |

### The structural finding: both sides are one-design-deep, and each design has a named live defect

This matters more than the verdict counts. The pro side has many authors but few designs: Card (2001), Cortes (2008), Peri (2012), and the inputs to both Friedberg–Hunt and Longhi et al. rest on the **past-settlement shift-share instrument**, which Jaeger–Ruist–Stuhler show conflates short- and long-run responses and biases estimates *toward zero on the short-run effect*. The con side is even narrower: six of its top eight slots are one author, and the headline results rest on the **national skill-cell frame** with fixed capital and within-cell perfect substitution — assumptions the paper itself flags.

So the two canons fail in opposite directions from a common cause. The pro side's designs are biased against finding a short-run effect; the con side's calibrations are biased toward finding a large one because capital cannot respond. Dustmann, Schönberg & Stuhler (2017) and Monras (2020) — the two cleanest exogenous shocks in the audit, both nominally con-side — land in between and say the durable cost is an **entry-cohort** and **employment-entry** effect, not a wage effect on incumbents. Neither camp's headline estimand captures that.

### Instrument-bias check `[FRAMING-SENSITIVE]`

This repo documents that the LLM instrument tilts toward the pro-immigration side (`notes/llm-bias-caveat.md`; ladder 44's mandatory flag). This audit's counts run **against** that tilt: it found more over-citation on the pro side and gave the pro side no clean WRONG only because its one candidate is a usage failure. Two counterweights before that is read as a finding. First, the con side has fewer distinct papers in circulation, so a raw count of over-citation instances is not a severity measure. Second, the con side's single WRONG (Borjas 2017) is a **result** defect, which is worse than any pro-side entry. A reader who weights by severity rather than count gets a tie, not a pro-side loss.

## 5. Gaps

- `[GAP]` Full text read this pass: Borjas (2003) NBER w9755, Jaeger–Ruist–Stuhler NBER w24285, Borjas–Freeman–Katz BPEA 1997. Everything else rests on publisher abstracts fetched from S2/OpenAlex on 2026-09-17 plus this repo's prior primary verification. Verdicts that turn on a table rather than an abstract — Card (2005)'s elasticity estimates, Peri (2012)'s first stage, Manacorda et al.'s incidence split — are abstract-level and should be hardened before load-bearing use.
- `[GAP]` Peri & Sparber (2009) full text still not fetched, carrying forward the same gap flagged in `immigration-dismantle-card-peri-2026-06-25.md`.
- `[GAP]` Borjas & Katz (2007)'s long-run capital-adjusted dropout figure, which is the natural companion to C1's short-run −8.9%, was not verified and is therefore not quoted.
- `[GAP]` Dustmann & Frattini (2014) was not re-fetched; the repo's corrected reading (recent 2001–2011 arrivals positive for both EEA and non-EEA; the negative non-EEA balance is the all-cohort comparison) is cited from `immigration-economics-disconfirmers-2026-06-25.md` rather than re-derived.
- `[GAP]` Over-citation examples name the *type* of citer (policy writing, advocacy, opposing camp) rather than specific citing documents. Naming specific articles that cite Borjas 2003's 8.9% as a long-run effect, or Clemens 2011 for a doubling estimate, would harden §4; S2's citation-context endpoint is the route.
- Suggested next queries if re-dispatched: `S2 /paper/{id}/citations?fields=contexts` on Borjas 2003 and Clemens 2011 to extract actual citation sentences; Borjas & Katz 2007 NBER w11281 full text; Peri & Sparber 2009 AEJ:Applied full text.

## 6. Sources

**Citation data.** Semantic Scholar Graph API `/paper/batch`, `/paper/search`, `/paper/search/match`, `/author/{id}/papers`, keyed, fetched 2026-09-17. OpenAlex `/works/doi:` cross-check, same date. Per-paper rows: [`notes/canon-citation-counts-2026-09-17.csv`](../notes/canon-citation-counts-2026-09-17.csv).

**Full text read this pass.** Borjas, NBER w9755 (2003). Jaeger, Ruist & Stuhler, NBER w24285 (2018). Borjas, Freeman & Katz, BPEA 1997:1.

**Abstracts verified at source 2026-09-17.** 10.1086/209979 (Card 2001) · 10.1086/589756 (Cortes 2008) · 10.1093/restud/rds019 (Dustmann, Frattini & Preston 2013) · 10.1257/aer.99.2.1 (Card 2009) · 10.1093/qje/qjw032 (Dustmann, Schönberg & Stuhler 2017) · 10.1086/707764 (Monras 2020) · 10.1086/425433 (Kaushal 2005) · 10.1257/aer.20170765 (Clemens, Lewis & Postel 2018) · 10.1257/app.20150114 (Foged & Peri 2016) · 10.1016/j.jue.2010.08.005 (Peri & Sparber 2011, body text via publisher page).

**Repo evidence cited, not re-derived.** `research/immigration-confidence-ladder.md` entries 17, 19, 29, 44, 45, 53, 59 · `research/immigration-dismantle-card-peri-2026-06-25.md` (current section) · `research/immigration-dismantle-clemens-2026-06-25.md` (current section) · `research/immigration-economist-dismantling-2026-06-25.md` · `research/immigration-redteam-2026-06-25.md` · `research/immigration-nas-scope-and-bias-update-2026-04-10.md` · `research/immigration-economics-disconfirmers-2026-06-25.md` · `notes/llm-bias-caveat.md`.

**Other DOIs cited.** 10.1111/j.1542-4774.2011.01052.x · 10.1111/j.1542-4774.2011.01055.x · 10.1111/j.1542-4774.2011.01057.x · 10.1111/j.1542-4774.2011.01049.x · 10.3386/w23433 · 10.3386/w13887 · 10.3386/w11610 · 10.3368/jhr.54.2.0217.8561R1 · 10.1257/aer.20181047 · 10.1093/restud/rdab030 · 10.17226/23550 · 10.24149/wp1704 · 10.1111/sjoe.12097 · 10.1257/pol.20220176 · 10.1177/0019793917692945 · 10.1086/262120 · 10.1111/ecoj.12181 · 10.1257/jep.25.3.83 · 10.1257/jel.20151189 · 10.1111/joes.12300.
