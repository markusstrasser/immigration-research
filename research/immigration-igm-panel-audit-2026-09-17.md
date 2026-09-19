claude-opus-5[1m]

# IGM / Clark Center expert-panel immigration polls — inventory and comment audit

**2026-09-19 interpretation correction:** Shimer's comment describes the incidence of
low-skill immigration on existing workers; the earlier claim that he reversed the fiscal
ranking of immigrant skill groups is withdrawn. Hart and Shimer both mention fiscal costs.
Shapiro's substitution argument can also fit a question about increased legal entry;
the poll does not stipulate that total entry must rise one-for-one.
The numerical fiscal comparisons below are historical: use the
[repaired calculation index](immigration-yearly-lifetime-cost-repair-2026-09-19.md).
Resident-stock accounting gaps do not establish the effect of additional legal admissions
on average citizen welfare. Comment ratings assess the public justification, not everything
a panelist knows or the panelist's general intelligence. [SOURCE: primary poll; INFERENCE]

**Verdict:** Thirteen immigration polls exist across the US and European panels, 22 statements
in all, every one of them about **legal** admission channels. **No IGM poll has ever asked
about unauthorized immigration, deportation, border enforcement, asylum policy, or the
2021-2024 US border surge.** On the one statement that matches the operator's framing — the
December 2013 low-skill poll — agreement is the weakest of any US immigration poll in the
series: 52.2% of the panel, 58.5% of respondents, 63% confidence-weighted, with 31.7% of
respondents uncertain. Of the 24 panelists who agreed, 17 left no reason at all. Of the 7 who
did, none cited a fiscal estimate or named a study. The short comments identify mechanisms,
but do not quantify a combined citizen-welfare effect. Shapiro's legal-for-unauthorized
substitution is a possible interpretation of greater legal admission; the poll leaves the
response of unauthorized entry unspecified. Shimer explicitly distinguished wage costs borne by low-skilled workers
from fiscal costs borne by high-skilled workers. The panel simultaneously agreed, 56.1% of respondents, that low-skilled American workers
would be substantially worse off — so the same body endorsed both a positive average and a
negative distributional effect in one sitting.

**Status:** COMPLETE. All 13 polls retrieved, all 986 panelist-responses parsed from the
Clark Center's own per-poll CSVs, both agree shares recomputed from the site's raw arrays and
reconciled against the published methodology.

Machine-readable output: `notes/igm-immigration-polls-2026-09-17.csv`
(986 rows: poll, date, panel, url, question, statement, panelist, institution, vote,
confidence, comment).

---

## 1. Method and retrieval [SOURCE]

`igmchicago.org` is Cloudflare-challenged. The live site is `https://kentclarkcenter.org/`
(the Clark Center Forum, formerly the IGM Forum). Retrieval facts, all verified this session:

- `www.kentclarkcenter.org` returns HTTP 301; `curl` must follow redirects.
- A short User-Agent trips Mod_Security (HTTP 406). A full desktop Chrome User-Agent string
  returns plain HTML.
- Every poll page carries a "Download Poll Data" link to a per-poll CSV under
  `/wp-content/uploads/`, containing each panelist's vote, confidence and verbatim comment.
  These CSVs are the authoritative record and are what this memo uses.
- Per-question vote distributions are embedded in each page as JavaScript arrays
  (`pollVals<id>_<n>` unweighted, `weightedPV<id>_<n>` confidence-weighted).
- Institutions are in the HTML response tables, not in the CSVs; they were merged by name.
- Full survey inventory: `https://kentclarkcenter.org/survey-sitemap.xml` (576 surveys).

**Completeness search.** Three independent routes, all run this session:
(1) slug scan of all 576 surveys in the sitemap for immigration/migration/refugee/border/
visa/deportation/asylum/citizen/labor/skill/surge/nation stems;
(2) the site's own search for `immigrant`, `migrant`, `refugee`, `H-1B`, `deportation`,
`asylum`, `border security`, `undocumented`;
(3) the site's own taxonomy pages `/tag/immigration/`, `/tag/migration/`, `/tag/refugees/`,
`/tag/immigrant-visas/`.
Routes 2 and 3 surfaced one poll the slug scan missed (`permanent-residency-rules`, June 2026).
Four further polls carry an immigration tag but contain no immigration statement and are
excluded: *Inequality, Populism, and Redistribution* (both panels, 2019), *Natural Experiments
in Labor Economics and Beyond* (2021, whose statement B mentions immigration only as an example
of a literature improved by the credibility revolution), *Hurricane Economics* (2022, where
"migrate" refers to economic activity), and *Scientists and Innovation* (2025).

**Verified negatives.** The site search returns **zero** surveys for `deportation`, `asylum`,
`border security` and `undocumented`. Scanning every survey modified on or after 2024-01-01
(149 polls) finds exactly two immigration polls in that window: *Immigration to Germany and
the EU* (European panel, 2025-02-20) and *Permanent Residency Rules* (US panel, 2026-06-03).
There is therefore **no poll on the 2021-2024 surge, on deportation policy, on the 2025-2026
enforcement expansion, or on H-1B since February 2017.**

### 1.1 How the two agree shares are built [SOURCE: methodology page, verbatim]

The Clark Center's methodology page states: "The unweighted graphs reflect the percentages of
all the members of a given panel, which means that those who do not answer are in the
denominator for that calculation, alongside those who vote… For the weighted graphs, each
response is weighted by the level of confidence in the topic that the panelist associates with
their answer (on a range from 1 to 10…), divided by the total level of confidence reported by
all responding panelists. In this case, those who do not answer are omitted from the
calculation."

The two published numbers therefore differ for **two** reasons, not one: a change of
denominator and a change of weight. The table below separates them. This matters: on
*Immigration and Government Budgets* (European, 2018) the published pair is 46% unweighted
versus 70% weighted, but 28% of that panel did not answer — re-basing alone moves 46% to 63.9%,
and confidence weighting adds the remaining 6 points. Quoting the weighted figure against the
unweighted one as evidence that "confident experts agree more" conflates the two effects.
[INFERENCE: arithmetic decomposition of the site's own published arrays]

---

## 2. Every immigration poll, both panels

Agree % = "strongly agree" + "agree". Columns 9-11 are the same votes under three conventions:
column 9 is the site's published unweighted number, column 11 is the site's published weighted
number, column 10 is the intermediate that isolates the re-basing effect.

**Polarity warning.** The agree column is not a "pro-immigration" column. Statements 7, 8, 9 and
12-13 are written so that *agreeing* is the restriction-favouring or immigration-sceptical answer
(7: free movement hurt low-skilled Europeans; 8-9: cutting H-1B raises revenue and employment),
or so that *disagreeing* is (12-13: reduced US appeal will hurt innovation). Statements 15-17 and
21-22 are written so that agreeing means a restriction does damage. Read each row against its
own wording. On the H-1B poll, the headline result is that **91.9% and 77.1% of respondents
disagreed** that cutting H-1B visas would raise tax revenue or American employment, with zero
agreement in either direction.

| # | Date | Panel | Poll | Q | Statement (verbatim) | n | No-answer % | Agree % (unweighted, all panel) | Agree % (of respondents) | Agree % (confidence-weighted) | Uncertain % (resp.) | Disagree % (resp.) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | February 12, 2013 | US | High-Skilled Immigrants | A | The average US citizen would be better off if a larger number of highly educated foreign workers were legally allowed to immigrate to the US each year. | 38 | 5.3 | 89.5 | 94.4 | 95 | 5.6 | 0.0 |
| 2 | December 10, 2013 | US | Low-Skilled Immigrants | A | The average US citizen would be better off if a larger number of low-skilled foreign workers were legally allowed to enter the US each year. | 46 | 10.9 | 52.2 | 58.5 | 63 | 31.7 | 9.8 |
| 3 | December 10, 2013 | US | Low-Skilled Immigrants | B | Unless they were compensated by others, many low-skilled American workers would be substantially worse off if a larger number of low-skilled foreign workers were legally allowed to enter the US each year. | 46 | 10.9 | 50.0 | 56.1 | 60 | 34.1 | 9.8 |
| 4 | September 20, 2016 | US | Science, Technology and Immigration | A | Allowing US-based employers to hire many more immigrants with advanced degrees in science or engineering would lower (at least temporarily) the premium earned by current American workers with similar degrees. | 42 | 9.5 | 71.4 | 78.9 | 80 | 18.4 | 2.6 |
| 5 | September 20, 2016 | US | Science, Technology and Immigration | B | Allowing US-based employers to hire many more immigrants with advanced degrees in science or engineering would raise per capita income in the US over time. | 42 | 9.5 | 85.7 | 94.7 | 94 | 5.3 | 0.0 |
| 6 | December 7, 2016 | European | Migration Within Europe | A | Freer movement of people to live and work across borders within Europe has made the average western European citizen better off since the 1980s. | 50 | 8.0 | 90.0 | 97.8 | 99 | 2.2 | 0.0 |
| 7 | December 7, 2016 | European | Migration Within Europe | B | Freer movement of people to live and work across borders within Europe has made many low-skilled western European citizens worse off since the 1980s. | 50 | 8.0 | 24.0 | 26.1 | 24 | 21.7 | 52.2 |
| 8 | February 14, 2017 | US | High-Skilled Immigrant Visas | A | If the US significantly lowers the number of H-1B visas now, expected US tax revenues will rise materially over the next four years. | 42 | 11.9 | 0.0 | 0.0 | 0 | 8.1 | 91.9 |
| 9 | February 14, 2017 | US | High-Skilled Immigrant Visas | B | If the US significantly lowers the number of H-1B visas now, employment for American workers will rise materially over the next four years. | 42 | 16.7 | 0.0 | 0.0 | 0 | 22.9 | 77.1 |
| 10 | July 12, 2017 | European | Refugees in Germany | A | The influx of refugees into Germany beginning in the summer of 2015 will generate net economic benefits for German citizens over the succeeding decade. | 50 | 22.0 | 34.0 | 43.6 | 47 | 48.7 | 7.7 |
| 11 | October 12, 2017 | US | Refugees in Germany | A | The influx of refugees into Germany beginning in the summer of 2015 will generate net economic benefits for German citizens over the succeeding decade. | 42 | 21.4 | 40.5 | 51.5 | 52 | 45.5 | 3.0 |
| 12 | January 17, 2018 | US | Immigration and Innovation | A | Over the past two years, all else equal, the appeal of the US as a destination for immigrants has changed in ways that will likely decrease innovation in the US economy. | 43 | 11.6 | 72.1 | 81.6 | 81 | 15.8 | 2.6 |
| 13 | January 25, 2018 | European | Immigration and Innovation | A | Over the past two years, all else equal, the appeal of the US as a destination for immigrants has changed in ways that will likely decrease innovation in the US economy. | 48 | 35.4 | 60.4 | 93.5 | 93 | 0.0 | 6.5 |
| 14 | November 7, 2018 | European | Immigration and Government Budgets | A | People who migrated to Europe between 2015 and 2018 are likely — over the next two decades — to contribute more in taxes paid than they receive in benefits and public services. | 50 | 28.0 | 46.0 | 63.9 | 70 | 25.0 | 11.1 |
| 15 | June 26, 2020 | US | New Visa Ban | A | Even if it is temporary, the ban on visas for skilled workers, including researchers, will weaken US leadership in STEM and R&D. | 43 | 0.0 | 97.7 | 97.7 | 99 | 2.3 | 0.0 |
| 16 | June 26, 2020 | US | New Visa Ban | B | Significantly fewer top foreign students will be attracted to US universities as a result of increased restrictions on visas for skilled workers. | 43 | 0.0 | 90.7 | 90.7 | 93 | 9.3 | 0.0 |
| 17 | June 26, 2020 | US | New Visa Ban | C | If increased restrictions on visas for skilled workers are made permanent, a noticeable share of research activities by US and foreign companies will move abroad. | 43 | 0.0 | 93.0 | 93.0 | 95 | 7.0 | 0.0 |
| 18 | February 20, 2025 | European | Immigration to Germany and the EU | A | The wave of immigration to Germany after 2015 (and up to the Russian invasion of Ukraine) has been a net positive for the country's economy. | 46 | 26.1 | 34.8 | 47.1 | 51 | 44.1 | 8.8 |
| 19 | February 20, 2025 | European | Immigration to Germany and the EU | B | Immigration to EU countries has been a net positive for government finances, adding substantially more in tax revenues than the increased costs associated with integration of immigrants. | 46 | 26.1 | 32.6 | 44.1 | 49 | 44.1 | 11.8 |
| 20 | February 20, 2025 | European | Immigration to Germany and the EU | C | Given Europe's low and falling fertility rates (from seven million births per year in 1960 to four million today), maintaining its position as a world economic power will require increased immigration over the medium term. | 46 | 23.9 | 52.2 | 68.6 | 72 | 14.3 | 17.1 |
| 21 | June 3, 2026 | US | Permanent Residency Rules | A | Requiring most green card applicants to apply for permanent residency from overseas would lead to a substantial reduction in the numbers of skilled immigrants in the US. | 44 | 15.9 | 75.0 | 89.2 | 94 | 8.1 | 2.7 |
| 22 | June 3, 2026 | US | Permanent Residency Rules | B | Requiring most green card applicants to apply for permanent residency from overseas would have a measurably adverse impact on a substantial number of US businesses. | 44 | 15.9 | 72.7 | 86.5 | 91 | 10.8 | 2.7 |

Two observations from the table, before any audit.

**The series is overwhelmingly about high-skilled and legal migration.** Of the 22 statements:
10 concern skilled workers, students, researchers, H-1B visas or green cards; 4 concern EU-wide
immigration or its effect on European government finances; 2 concern the German refugee inflow
(the same statement put to both panels); 2 concern intra-European free movement; 2 concern the
general appeal of the US as a destination and its effect on innovation (again the same statement
to both panels); and **2 concern low-skilled entry to the US**. The US panel has been asked about
low-skilled immigration exactly **once in thirteen years**, in December 2013.

**Agreement is far lower on the low-skill and fiscal statements than on the skilled ones.**
Confidence-weighted agreement runs 93-99% on the skilled-visa statements (High-Skilled
Immigrants 95%, New Visa Ban 93-99%, Permanent Residency Rules 91-94%, Science/Technology B
94%) but 63% on low-skill entry, 47-52% on the German refugee inflow, 70% on European migrant
fiscal contribution and 49% on EU immigration as a net positive for government finances. The
"economists agree immigration is good" summary is accurate for the skilled statements and is
not supported by the low-skill or fiscal statements. [INFERENCE: read off the table]

---

## 3. What the low-skill statement actually asked

Verbatim, December 10, 2013, US panel, Question A:

> "The average US citizen would be better off if a larger number of low-skilled foreign workers
> were legally allowed to enter the US each year."

And Question B, put to the same panel in the same sitting:

> "Unless they were compensated by others, many low-skilled American workers would be
> substantially worse off if a larger number of low-skilled foreign workers were legally allowed
> to enter the US each year."

Four features of the wording are load-bearing and the operator's framing should not be allowed
to stand in for them.

1. **It is about legal admission.** "Legally allowed to enter." The statement is a question
   about raising a visa quota, not about unauthorized entry, enforcement or amnesty. No IGM
   poll asks about unauthorized immigration.
2. **The welfare subject is "the average US citizen."** Not the median, not the low-skilled
   native, not the fiscal balance, and explicitly not immigrants themselves. See §6.
3. **There is no magnitude and no time horizon.** "A larger number" is unquantified; no period
   is named. Several panelists said in their comments that this made the statement unanswerable.
4. **Nothing is specified about status, family or duration.** Whether entrants get citizenship,
   whether they bring dependants, and whether they stay are all unspecified — and three
   panelists (Deaton, Hall, Hart) said these omissions determined their vote.

Question B is the decisive context. The panel was not asked to choose between "good" and "bad."
It was asked two separate questions and gave two answers that pull in opposite directions:
58.5% of respondents agreed the average citizen gains, and 56.1% of respondents agreed low-skilled
Americans would be substantially worse off. Twelve panelists — Baicker, Currie, Cutler, Duffie,
Edlin, Einav, Fair, Hart, Holmström, Hoynes, Maskin and Stokey — voted Agree on both. That combination
is coherent only under an aggregate-welfare criterion that permits uncompensated losers, which is
exactly the criterion §6 examines.

---

## 4. Low-skill poll, Question A — every panelist

| Panelist | Institution | Vote | Confidence | Verbatim comment |
|---|---|---|---|---|
| Christopher Udry | Northwestern | Strongly Agree | 4 | The evidence is that complementarities would make most Americans better off.  The data is not decisive, though. |
| Daron Acemoglu | MIT | Agree | 8 | — |
| David Autor | MIT | Agree | 8 | — |
| Katherine Baicker | University of Chicago | Agree | 4 | — |
| Abhijit Banerjee | MIT | Agree | 5 | The median US worker (which is how I interpret the word average) is high skill by global standards |
| Janet Currie | Princeton | Agree | 8 | — |
| David Cutler | Harvard | Agree | 5 | — |
| Darrell Duffie | Stanford | Agree | 4 | Labor is a valuable factor input. My answer presumes that many of these new workers would be employed. But I'm not confident of that. |
| Aaron Edlin | Berkeley | Agree | 6 | This would drive down the cost of a variety of services. |
| Liran Einav | Stanford | Agree | 6 | — |
| Ray Fair | Yale | Agree | 5 | — |
| Amy Finkelstein | MIT | Agree | 5 | — |
| Oliver Hart | Harvard | Agree | 8 | On average citizens would be better off--by classical gains from trade . A countervailing effect : welfare payments to unemployed immigrants |
| Bengt Holmström | MIT | Agree | 5 | — |
| Hilary Hoynes | Berkeley | Agree | 10 | — |
| Steven Kaplan | Chicago Booth | Agree | 6 | — |
| Anil Kashyap | Chicago Booth | Agree | 5 | — |
| Eric Maskin | Harvard | Agree | 7 | — |
| Maurice Obstfeld | Peterson Institute for International Economics | Agree | 8 | — |
| Emmanuel Saez | Berkeley | Agree | 3 | — |
| Carl Shapiro | Berkeley | Agree | 6 | Substituting legal immigration for illegal immigration would enhance efficiency and equity. |
| Robert Shimer | University of Chicago | Agree | 5 | For low skill workers, the main adverse effects are through wages. For high skill, through fiscal costs. Both costs could be small |
| Nancy Stokey | University of Chicago | Agree | 8 | — |
| Richard Thaler | Chicago Booth | Agree | 3 | — |
| Alan Auerbach | Berkeley | Uncertain | 3 | — |
| Marianne Bertrand | Chicago | Uncertain | 4 | — |
| Markus Brunnermeier | Princeton | Uncertain | 6 | It depends on whether one takes a long or short-term horizon. |
| Barry Eichengreen | Berkeley | Uncertain | 1 | "Average US citizen?" What does this mean.  Unskilled natives likely to be worse off, skilled native better off. Who's average? |
| Pinelopi Goldberg | Yale | Uncertain | 6 | — |
| Robert Hall | Stanford | Uncertain | 5 | If only workers are admitted, we come out ahead because of tax revenue. But it's not so obvious if they bring their families and relatives. |
| Caroline Hoxby | Stanford | Uncertain | 10 | I am sure that I am uncertain. A certain answer would require a knowledge of general eqm effects on which we've only a partial grasp. |
| Kenneth Judd | Stanford | Uncertain | 8 | Free trade is as good as migration for traded goods. The impact on nongraded goods is unclear, as are the burdens on social programs. |
| Pete Klenow | Stanford | Uncertain | 5 | But the gains to immigrants would be large. |
| Jonathan Levin | Stanford | Uncertain | 4 | Card's Ely lecture argues wage effects are small. Pro-immigration arguments partly about welfare of immigrants, rather than residents. |
| Larry Samuelson | Yale | Uncertain | 1 | There will be gains and losses of various types to various people; it is difficult to reduce these to a net effect on an average citizen. |
| José Scheinkman | Columbia University | Uncertain | 7 | — |
| Richard Schmalensee | MIT | Uncertain | 3 | Very unclear how to think about the "average" citizen when there would likely be winners and losers. |
| Alberto Alesina | Harvard | Disagree | 6 | — |
| Joseph Altonji | Yale | Disagree | 7 | Real income of avg the American would rise, but social strains and inequality would also increase. |
| Angus Deaton | Princeton | Disagree | 7 | I think it matters a lot whether or not they are granted citizenship which we are not told. |
| William Nordhaus | Yale | Disagree | 3 | This response is based on the idea that it will increase inequality, which is already too great. |
| Raj Chetty | Harvard | Did Not Answer | — | — |
| Judith Chevalier | Yale | Did Not Answer | — | — |
| Austan Goolsbee | Chicago | Did Not Answer | — | — |
| Michael Greenstone | University of Chicago | Did Not Answer | — | — |
| Hyun Song Shin | Princeton | Did Not Answer | — | — |

Mean confidence among the 24 agreers is 5.92 on the 1-10 scale; among all 41 respondents, 5.56.
Neither is a high-conviction number on a scale where the same panel routinely reports 8-10 on
questions it considers settled.


### Low-skill poll, Question B — every panelist

| Panelist | Institution | Vote | Confidence | Verbatim comment |
|---|---|---|---|---|
| David Cutler | Harvard | Strongly Agree | 7 | — |
| Liran Einav | Stanford | Strongly Agree | 8 | — |
| Alberto Alesina | Harvard | Agree | 4 | — |
| Alan Auerbach | Berkeley | Agree | 5 | — |
| Katherine Baicker | University of Chicago | Agree | 4 | — |
| Markus Brunnermeier | Princeton | Agree | 8 | — |
| Janet Currie | Princeton | Agree | 7 | — |
| Angus Deaton | Princeton | Agree | 7 | — |
| Darrell Duffie | Stanford | Agree | 1 | A higher number of workers of the same type seeking jobs would lower their average wages or employment rate, other things equal. |
| Aaron Edlin | Berkeley | Agree | 7 | Those who compete with low skill immigrants will be hurt by extra competition. |
| Barry Eichengreen | Berkeley | Agree | 5 | — |
| Ray Fair | Yale | Agree | 5 | "substantially" is probably too strong. |
| Pinelopi Goldberg | Yale | Agree | 6 | — |
| Oliver Hart | Harvard | Agree | 8 | There can be winners and losers. Similarly skilled workers will face greater competition for jobs and their wages may fall. |
| Bengt Holmström | MIT | Agree | 4 | — |
| Hilary Hoynes | Berkeley | Agree | 10 | — |
| Kenneth Judd | Stanford | Agree | 8 | It is hard to see how they would benefit, and they would lose from the competition in the labor market. |
| Eric Maskin | Harvard | Agree | 7 | — |
| William Nordhaus | Yale | Agree | 5 | "Substantially" is a vague term, but on the whole it would probably lower incomes at the bottom. |
| Larry Samuelson | Yale | Agree | 6 | These are the most likely candidates for people who will be adversely affected. |
| José Scheinkman | Columbia University | Agree | 8 | — |
| Richard Schmalensee | MIT | Agree | 3 | — |
| Nancy Stokey | University of Chicago | Agree | 8 | — |
| Daron Acemoglu | MIT | Uncertain | 6 | — |
| Abhijit Banerjee | MIT | Uncertain | 5 | It all turns on what fraction of low skilled US workers don't have an option that they clearly prefer to these mostly dead end low paid jobs |
| Marianne Bertrand | Chicago | Uncertain | 4 | — |
| Amy Finkelstein | MIT | Uncertain | 5 | — |
| Robert Hall | Stanford | Uncertain | 4 | My understanding is that the Mariel question is still up in the air in terms of serious research. |
| Caroline Hoxby | Stanford | Uncertain | 10 | Low-skilled workers would probably be worse off but positive gen eqm effects might offset negative direct effects. |
| Steven Kaplan | Chicago Booth | Uncertain | 6 | — |
| Anil Kashyap | Chicago Booth | Uncertain | 3 | I believe the evidence show that some low-skilled natives suffer, but whether many suffer substantially not clear given what I know on this |
| Jonathan Levin | Stanford | Uncertain | 1 | Again, Card's work suggests this is not obvious, although one might expect increased labor market competition. |
| Maurice Obstfeld | Peterson Institute for International Economics | Uncertain | 7 | — |
| Emmanuel Saez | Berkeley | Uncertain | 4 | — |
| Robert Shimer | University of Chicago | Uncertain | 5 | Evidence that immigration pushes down low skill wages is mixed |
| Richard Thaler | Chicago Booth | Uncertain | 1 | No way to answer this without knowing the definition of "many" and "substantially" plus some facts. |
| Christopher Udry | Northwestern | Uncertain | 7 | The "many" is the problem: some would certainly be hurt (unless compensated).   But "many"? |
| Joseph Altonji | Yale | Disagree | 7 | I agree that the effect would be negative, but believe that it would be modest, not substantial. |
| Pete Klenow | Stanford | Disagree | 5 | — |
| Carl Shapiro | Berkeley | Disagree | 6 | Substituting legal for illegal immigration could provide benefits to low-skilled workers generally, for both economic and political reasons. |
| David Autor | MIT | Strongly Disagree | 8 | — |
| Raj Chetty | Harvard | Did Not Answer | — | — |
| Judith Chevalier | Yale | Did Not Answer | — | — |
| Austan Goolsbee | Chicago | Did Not Answer | — | — |
| Michael Greenstone | University of Chicago | Did Not Answer | — | — |
| Hyun Song Shin | Princeton | Did Not Answer | — | — |

## 5. Audit of the stated justifications — low-skill Question A

**5.0 The silence is the largest single finding.** Of the 24 panelists who agreed, **17 left no
comment at all** (Acemoglu, Autor, Baicker, Currie, Cutler, Einav, Fair, Finkelstein, Holmström,
Hoynes, Kaplan, Kashyap, Maskin, Obstfeld, Saez, Stokey, Thaler). Comments are optional, so this
is not a defect in their answers; it is a limit on what the poll can be cited for. A vote with
no stated reason cannot be cited as expert endorsement of any particular mechanism — fiscal,
wage, complementarity or otherwise. Anyone invoking "economists agree" on this statement is
invoking 24 votes of which 17 carry no reasoning on the public record. Rating for those 17:
**NO REASON GIVEN** — not wrong, but not usable as evidence for a mechanism.

Below, each of the 7 reasoned agreements and all 4 disagreements is audited against this repo's
evidence base. Ratings: HOLDS · HOLDS-NARROWLY · UNSUPPORTED (the reason does not establish the
claim voted for) · WRONG (the reason is contradicted by evidence).

### Agreers who gave a reason

**Christopher Udry (Northwestern), Strongly Agree, confidence 4** — "The evidence is that
complementarities would make most Americans better off. The data is not decisive, though."
→ **HOLDS-NARROWLY.** The complementarity channel is real and this repo adopts a version of it:
Colas-Sachs 2024 (AEJ:Policy) finds one average low-skilled immigrant generates an indirect
fiscal benefit of roughly $750/yr by raising complementary native high-skill wages, of the same
order as the direct fiscal cost and opposite in sign [SOURCE: ladder 45, 10.1257/pol.20220176].
But the magnitude of the complementarity elasticity is contested: Borjas-Grogger-Hanson show the
Ottaviano-Peri imperfect-substitution result weakens sharply once high-school students are
removed from the sample [SOURCE: `immigration-economist-dismantling-2026-06-25.md` line 231,
parent-re-verified]. Udry's own hedge ("not decisive") is the accurate part; the rating is
narrow because "most Americans" is a distributional claim that complementarity alone does not
deliver — it delivers a gain to complements, not to most people.

**Abhijit Banerjee (MIT), Agree, confidence 5** — "The median US worker (which is how I
interpret the word average) is high skill by global standards."
→ **UNSUPPORTED as stated.** This is a re-reading of the statement, not evidence for it. Being
high-skill "by global standards" establishes that the median US worker is a complement rather
than a substitute for a low-skilled entrant in the labour market; it says nothing about the
fiscal transfer, which runs through the tax-and-transfer system rather than the wage. This
repo's measurement of that omitted term is large: the Mexican-origin population's age-band
fiscal gap against third-plus non-Hispanic whites is −$290.59bn/yr on an all-age expanded
account [SOURCE: `immigration-all-age-and-lineage-findings-2026-09-17.md`, ladder 123], widening
to −$411.81bn under within-state matching [SOURCE: ladder 125]. Banerjee's reasoning addresses
one of the two channels and treats the answer as settled by it.

**Darrell Duffie (Stanford), Agree, confidence 4** — "Labor is a valuable factor input. My
answer presumes that many of these new workers would be employed. But I'm not confident of that."
→ **UNSUPPORTED.** "Labor is a valuable factor input" is a statement about the production
function that is true of any labour, native or foreign, and does not distinguish the
counterfactual. The vote is explicitly conditional on an employment assumption the panelist
declines to endorse, at confidence 4. This is a self-flagged conditional, and it should be
read as one.

**Aaron Edlin (Berkeley), Agree, confidence 6** — "This would drive down the cost of a variety
of services."
→ **HOLDS-NARROWLY, welfare-of-whom problem.** Lower service prices are a real consumer-surplus
channel and accrue disproportionately to households that buy those services. The reason is
silent on the two offsetting terms: the wage incidence on competing workers, which Edlin himself
affirmed by voting Agree on Question B ("Those who compete with low skill immigrants will be
hurt by extra competition"), and the fiscal transfer. A price effect is not a welfare verdict
until netted against both.

**Oliver Hart (Harvard), Agree, confidence 8** — "On average citizens would be better off--by
classical gains from trade. A countervailing effect : welfare payments to unemployed immigrants"
→ **HOLDS-NARROWLY; Hart and Shimer both name the fiscal channel.** Hart
is correct that the classical gains-from-trade argument delivers a positive aggregate for
factor-owners in the receiving economy, and he explicitly names a
fiscal offset. The audit point is that he names the offset without sizing it, and its size is
what determines the sign. Under this repo's measurement the offset is not a rounding error:
the measured partial balance for the 40.90m Mexican-origin population is **+$50.24bn** in the
main arm, but the age-band gap against third-plus non-Hispanic whites is **−$290.59bn**
[SOURCE: ladder 123]. Hart's framing also understates the term by restricting it to "welfare
payments to unemployed immigrants" — the measured gap is primarily a **tax-side** gap, not a
transfer-side one, and it persists among the employed [SOURCE: ladder 76, 127].

**Carl Shapiro (Berkeley), Agree, confidence 6** — "Substituting legal immigration for illegal
immigration would enhance efficiency and equity."
→ **HOLDS-NARROWLY as a conditional status-substitution argument.** The statement asks about
more workers being legally allowed to enter. It does not require total entry to rise
one-for-one: greater legal admission might partly replace unauthorized entry. The previous
audit incorrectly treated the question as fixing that counterfactual. Shapiro's mechanism
therefore fits one reading of the question, although the comment supplies neither the
substitution rate nor a quantified net welfare effect. [INFERENCE from primary wording]
Shapiro gave the same reason on Question B. Notably, his is the only comment in the
entire IGM immigration series that engages unauthorized immigration at all — and it does so as
an aside on a poll about legal admission, which underlines §1's verified negative.

**Robert Shimer (University of Chicago), Agree, confidence 5** — "For low skill workers, the
main adverse effects are through wages. For high skill, through fiscal costs. Both costs could
be small."
→ **HOLDS-NARROWLY as an incidence distinction.** In the context of a question about
low-skilled entrants, the natural reading is that low-skilled existing workers face wage
competition while high-skilled existing workers face fiscal costs through taxation. He does
not claim that high-skilled immigrants generate greater fiscal costs than low-skilled
immigrants. The previous audit confused the people bearing a cost with the entrants whose
admission is being evaluated; its "PARTIALLY WRONG" rating is withdrawn. [INFERENCE from
the wording and question context; SOURCE: primary poll linked below]
The comment does not quantify either channel or establish that the combined welfare effect
is positive. Its statement that both costs could be small remains a possibility claim.
Shimer voted Uncertain on Question B, citing
mixed evidence on low-skill wages, which is consistent with this repo's position on Mariel
[SOURCE: ladder 44].

### Disagreers

**Alberto Alesina (Harvard), Disagree, confidence 6** — no comment. → **NO REASON GIVEN.**

**Joseph Altonji (Yale), Disagree, confidence 7** — "Real income of avg the American would rise,
but social strains and inequality would also increase."
→ **HOLDS, and it is the sharpest comment in the poll.** Altonji concedes the pecuniary
aggregate and votes No anyway, because he reads "better off" as including non-income components.
This is a disagreement about the welfare criterion, not about the economics, and it is stated
as such. It is the mirror image of the agreeing votes: same predicted income effect, different
definition of "better off." See §6.

**Angus Deaton (Princeton), Disagree, confidence 7** — "I think it matters a lot whether or not
they are granted citizenship which we are not told."
→ **HOLDS.** A statement-incompleteness objection, and a correct one. Citizenship determines
access to means-tested federal programs, and this repo's ledger work shows the fiscal balance
is sensitive to exactly that eligibility margin [SOURCE: `immigration-admission-work-access-2026-09-05.md`;
ladder 76 on the transfer and tax terms]. Deaton is objecting that the question is
under-specified, not asserting a sign.

**William Nordhaus (Yale), Disagree, confidence 3** — "This response is based on the idea that
it will increase inequality, which is already too great."
→ **HOLDS-NARROWLY, with a stated value premise.** The inequality prediction is well supported —
the panel itself endorsed it at 56.1% of respondents on Question B, and it is the standard
prediction of any model with imperfect substitution. The move from "increases inequality" to
"the average citizen is not better off" requires an inequality-averse social welfare function,
which Nordhaus states openly ("already too great"). Confidence 3 is appropriately low for a
vote that turns on a value judgment. [FRAMING-SENSITIVE]

### What no comment says

Across all 41 respondents on Question A, **not one comment cites a fiscal estimate, a number,
or a study by name on the fiscal channel.** Two comments name the fiscal channel qualitatively
(Hart, Hall). Two name the literature on wages (Levin and Hall, both citing Card — Levin on
Question A, Hall on Question B via Mariel). Zero cite NAS, CBO, Borjas's fiscal work, or any
quantitative estimate. The poll is a record of priors, not of a literature review, and its
weight as evidence should be set accordingly.

Two of those literature references deserve a note because they are load-bearing in this repo.
**Jonathan Levin (Stanford), Uncertain, confidence 4** — "Card's Ely lecture argues wage effects
are small. Pro-immigration arguments partly about welfare of immigrants, rather than residents."
→ **HOLDS**, and it is the only comment in the poll that names the welfare-of-whom problem
explicitly. This repo adopts the small-average-wage-effect reading [SOURCE: ladder 44; Ottaviano-Peri
2012 published native effect about +0.6%, per `immigration-economist-dismantling-2026-06-25.md`],
while flagging that the average conceals losers and that the generating elasticity is contested.
**Robert Hall (Stanford), Uncertain (Q B), confidence 4** — "My understanding is that the Mariel
question is still up in the air in terms of serious research." → **HOLDS** and matches this
repo's rating exactly: Clemens-Hunt 2019 shows the large-harm reading survives only under a
sample cut leaving roughly 17 observations per year, but Borjas 2019 remains a live counter and
the profession has not formally closed it [SOURCE: ladder 44, 10.3386/w23433].

Hall's Question A comment — "If only workers are admitted, we come out ahead because of tax
revenue. But it's not so obvious if they bring their families and relatives." → **HOLDS.** The
dependants margin is precisely where the measured fiscal gap sits: the second generation, not
the first, shows the widest per-adult gap once place is fixed (−$7,081 at metro×age)
[SOURCE: ladder 128].

### 5.1 There is no unauthorized-immigration or deportation poll to audit

The operator's task specified auditing "any unauthorized/deportation poll." **None exists.**
This is a verified negative established three ways in §1. The closest artefacts in the series
are Shapiro's one-line aside above, and the 2020 *New Visa Ban* poll, which concerns a
restriction on **skilled** visas and which the panel opposed near-unanimously (weighted
agreement 93-99% that the ban would do damage). The most recent US immigration poll,
*Permanent Residency Rules* (June 3, 2026), asks about a procedural restriction on green-card
applicants and again concerns skilled immigrants: 94% weighted agreement that it would
substantially reduce skilled-immigrant numbers, 91% that it would adversely affect a
substantial number of US businesses. No panelist has ever been asked to vote on removal,
enforcement, or the fiscal or wage effects of the unauthorized population.

---

## 6. What "better off" means, and why the answers turn on it

The statement fixes the welfare subject as **the average US citizen**. Three consequences.

**It is an average, so it is silent on distribution by construction.** Five panelists said so
in their comments, and this is the single most common substantive remark in the poll.
Eichengreen (Uncertain, confidence 1): "'Average US citizen?' What does this mean. Unskilled
natives likely to be worse off, skilled native better off. Who's average?" Schmalensee
(Uncertain, confidence 3): "Very unclear how to think about the 'average' citizen when there
would likely be winners and losers." Samuelson (Uncertain, confidence 1): "There will be gains
and losses of various types to various people; it is difficult to reduce these to a net effect
on an average citizen." Banerjee reinterpreted "average" as "median" before answering. Altonji
accepted that average real income rises and voted Disagree anyway. Confidence 1 from two
panelists is the lowest in the poll and is an objection to the question, not an estimate.

**"Citizen" excludes the immigrants themselves — and this is where most of the measured gain
in the migration literature sits.** Levin named it: "Pro-immigration arguments partly about
welfare of immigrants, rather than residents." Klenow, voting Uncertain, said only "But the
gains to immigrants would be large" — a remark that is true, is the largest single welfare
term in the global accounting, and is excluded from the statement by its own wording. This
repo's place-premium work rates that gain as the strongest single fact in the open-borders
corpus: for observably identical workers the US-versus-home wage ratio exceeds 2 in 38 of 42
countries even after a worst-case selection adjustment, the selection-bias correction itself
being only 1.0-1.3 (1.45 at its observed maximum, for Peru) [SOURCE:
`immigration-dismantle-clemens-2026-06-25.md` §Claim 1, verbatim from Clemens-Montenegro-Pritchett
2008 §3.9]. The same memo fences it: the premium is a marginal-mover fact under current
institutions, not a general-equilibrium open-borders warrant. A reader who cites this poll as showing
"economists say immigration is beneficial" is silently swapping a global-welfare criterion for
the citizen-welfare criterion the panel was actually asked about. The 52-63% agreement is on
the narrower question; the global gain is not in it.

**"Better off" is undefined over income versus everything else.** Altonji votes Disagree while
conceding income rises, on "social strains and inequality." Nordhaus votes Disagree on
inequality aversion. Brunnermeier is Uncertain because "it depends on whether one takes a long
or short-term horizon." Hoxby, at confidence 10 — the highest in the poll — votes Uncertain:
"I am sure that I am uncertain. A certain answer would require a knowledge of general eqm
effects on which we've only a partial grasp."

**The aggregation the poll performs is not the aggregation a fiscal or distributional question
needs.** A confidence-weighted share of expert votes on an unquantified statement about an
unspecified average is a measure of professional disposition. It is not an estimate of a
magnitude, it has no standard error, and it cannot be compared with a measured quantity such as
this repo's −$290.59bn age-band gap or +$50.24bn partial balance [SOURCE: ladder 123]. The poll
and the ledger answer different questions; neither refutes the other. [FRAMING-SENSITIVE]

A final note on the public-goods convention, because it is where the statement is most sensitive
and where no panelist commented. Whether immigration looks fiscally positive or negative depends
heavily on whether defence and debt interest are treated as pure public goods (marginal cost
zero) or allocated per capita. NAS 2016 varies only pure public goods across its scenarios and
generates a $160k lifetime NPV swing from that choice alone [SOURCE: ladder 80]. This repo finds
a fixed-national-budget allocation change narrows the white gap by $47.42bn [SOURCE: ladder 123].
No panelist's comment engages this, so the poll carries no information about which convention
the panel had in mind.

---

## 7. Panel composition [SOURCE: kentclarkcenter.org]

The Clark Center Forum runs three panels: the US Economic Experts Panel, the European Economic
Experts Panel, and a Finance Panel. Immigration polls have gone to the first two only.

The US panel on the December 2013 low-skill poll numbered 46. Institutional distribution, taken
directly from the site's response tables:

| Institution (as printed on the site) | Panelists |
|---|---|
| Chicago (University of Chicago 4 + Chicago Booth 3 + "Chicago" 2) | 9 |
| Stanford | 7 |
| MIT | 6 |
| Yale | 6 |
| Berkeley | 6 |
| Harvard | 5 |
| Princeton | 4 |
| Columbia University | 1 |
| Northwestern | 1 |
| Peterson Institute for International Economics | 1 |

Ten institutions account for all 46 seats, and seven of them account for 43. Only one panelist
sits outside a university. The 2026 US panel
(n=44) has the same shape. Panel sizes across the 13 immigration polls run 38 to 50.

The site publishes each panelist's institution but **not** a field label, so no field breakdown
can be given as [SOURCE]. What can be said from the roster is that the panel is a general
economics panel, not a panel of immigration or labour economists: on the 2013 low-skill poll
the roster includes macroeconomists, finance specialists, behavioural economists, public
finance specialists and development economists. Several panelists whose published work is
directly on immigration wage effects did not answer or answered Uncertain. This is a feature of
the panel's design — it is built to measure the profession's general view, not specialist
consensus — and it bears on how the results should be cited. [INFERENCE: from the roster and
the panel's stated purpose; no field data published]

Non-response is material and varies a great deal: 0% on the 2020 New Visa Ban, 10.9% on the
2013 low-skill poll, 23.9% on the 2025 Germany/EU poll, 26.1-28% on the 2018 European fiscal
poll, and 35.4% on the 2018 European innovation poll. On the polls with the highest
non-response — the two European fiscal and innovation polls — the published weighted agree
share is built on under two-thirds of the panel.

---

## 8. Summary of findings

1. **Thirteen immigration polls, 22 statements, 986 panelist-responses, 2013-2026.** All
   retrieved from the Clark Center's own per-poll CSVs; full data in
   `notes/igm-immigration-polls-2026-09-17.csv`.
2. **No poll on unauthorized immigration, deportation, border enforcement or asylum has ever
   been run**, on either panel, in any year. Three independent search routes agree. The most
   recent US immigration poll is June 3, 2026, on green-card procedure.
3. **The low-skill statement is about legal admission** — "legally allowed to enter the US each
   year" — and is the only time the US panel has been asked about low-skilled immigration.
4. **Agreement on it is the weakest in the US series**: 52.2% of the panel, 58.5% of respondents,
   63% confidence-weighted, mean confidence 5.92 among agreers, 31.7% of respondents uncertain.
   Compare 95% weighted on the high-skilled statement ten months earlier.
5. **Seventeen of the 24 agreers gave no reason.** Of the seven who did, none cited a fiscal
   estimate. Hart and Shimer named fiscal costs without sizing them; Shimer distinguished
   their incidence across existing workers. Shapiro offered a substitution-of-status argument
   whose sufficiency for the question about greater legal entry remains disputed.
6. **The same panel agreed, at 56.1% of respondents, that low-skilled Americans would be
   substantially worse off.** Twelve panelists voted Agree on both. The joint position requires
   an aggregate criterion that tolerates uncompensated losers.
7. **The published weighted-versus-unweighted gap is partly a denominator change, not a
   confidence effect.** The methodology page confirms non-respondents are in the unweighted
   denominator and out of the weighted one. On the 2018 European fiscal poll this accounts for
   about three-quarters of the 46%-to-70% gap.
8. **The panel is ten institutions deep and general rather than specialist**, and non-response
   runs from 0% to 35.4% across the series.

---

## Revisions

2026-09-17 — created. Inventory and audit built from primary retrieval of all 13 Clark Center
immigration polls and their per-poll response CSVs.

2026-09-19 — [Correct the Shimer incidence reading](../decisions/2026-09-19-igm-shimer-incidence-reading.md).
Withdraw the mistaken immigrant-skill interpretation in the verdict, detailed rating and
summary, correct the claim that only Hart mentioned fiscal costs, and recognize that Shapiro's
legal-for-unauthorized substitution can fit the poll's wording. Original response
text and vote data are unchanged; the prior interpretation remains in Git history.

---

## Sources

All retrieved 2026-09-17 by direct HTTP with a desktop Chrome User-Agent.

**Methodology and index**
- Methodology (weighting and denominator conventions, quoted verbatim in §1.1): https://kentclarkcenter.org/methodology/
- Full survey inventory (576 surveys): https://kentclarkcenter.org/survey-sitemap.xml
- Topic taxonomies used for completeness: https://kentclarkcenter.org/tag/immigration/ · https://kentclarkcenter.org/tag/migration/ · https://kentclarkcenter.org/tag/refugees/ · https://kentclarkcenter.org/tag/immigrant-visas/

**Poll pages (13)**
- High-Skilled Immigrants, US, 2013-02-12: https://kentclarkcenter.org/surveys/high-skilled-immigrants/
- Low-Skilled Immigrants, US, 2013-12-10: https://kentclarkcenter.org/surveys/low-skilled-immigrants/
- Science, Technology and Immigration, US, 2016-09-20: https://kentclarkcenter.org/surveys/science-technology-and-immigration/
- Migration Within Europe, European, 2016-12-07: https://kentclarkcenter.org/surveys/migration-within-europe/
- High-Skilled Immigrant Visas, US, 2017-02-14: https://kentclarkcenter.org/surveys/high-skilled-immigrant-visas/
- Refugees in Germany, European, 2017-07-12: https://kentclarkcenter.org/surveys/refugees-in-germany/
- Refugees in Germany, US, 2017-10-12: https://kentclarkcenter.org/surveys/refugees-in-germany-2/
- Immigration and Innovation, US, 2018-01-17: https://kentclarkcenter.org/surveys/immigration/
- Immigration and Innovation, European, 2018-01-25: https://kentclarkcenter.org/surveys/immigration-and-innovation/
- Immigration and Government Budgets, European, 2018-11-07: https://kentclarkcenter.org/surveys/immigration-and-government-budgets/
- New Visa Ban, US, 2020-06-26: https://kentclarkcenter.org/surveys/new-visa-ban/
- Immigration to Germany and the EU, European, 2025-02-20: https://kentclarkcenter.org/surveys/immigration-to-germany-and-the-eu/
- Permanent Residency Rules, US, 2026-06-03: https://kentclarkcenter.org/surveys/permanent-residency-rules/

**Per-poll response data (the authoritative vote/confidence/comment records)**
Each poll page links its own CSV under `https://kentclarkcenter.org/wp-content/uploads/`. The
low-skill poll's is `2020/12/2013-12-10-US-EEP-Low-skilled-Immigrants.csv`; all 13 are listed
with their polls in `notes/igm-immigration-polls-2026-09-17.csv`.

**Repo evidence used in the audit**
- `research/immigration-confidence-ladder.md` entries 44 (Mariel artifact-fragility), 45
  (Colas-Sachs complementarity, +$750/yr), 46 (CBO federal surge scoring), 76 (second-generation
  partial ledger), 80 (public-goods convention and prison capacity), 123 (−$290.59bn age-band
  gap, +$50.24bn partial balance), 125 (within-state matching, −$411.81bn), 127 (ACS earnings
  replication), 128 (metro matching, second generation worst at −$7,081).
- `research/immigration-all-age-and-lineage-findings-2026-09-17.md`
- `research/immigration-economist-dismantling-2026-06-25.md` (Ottaviano-Peri published +0.6%
  native effect; Borjas-Grogger-Hanson complementarity contest)
- `research/immigration-dismantle-clemens-2026-06-25.md` (place premium and its authors' own fence)
- `research/immigration-admission-work-access-2026-09-05.md` (eligibility margin)

**Instrument-bias flag (per repo constitution principle 7).** This audit was produced by an LLM
whose post-training disposition on immigration is documented as tilted toward the
"less costly/harmful" direction (`notes/llm-bias-caveat.md`; ladder §44 preamble). Two guards
were applied. First, every quantitative claim about the polls is recomputed from the site's own
raw arrays and CSVs rather than summarised, so the numbers are checkable. Second, the audit
ratings address the stated arguments rather than treating support or opposition as evidence
of correctness, and the finding that most agreers gave no reason is a
finding about the poll's evidentiary weight, not about the correctness of their votes. The
memo takes no position on whether more low-skilled immigration is desirable. [FRAMING-SENSITIVE]
