claude-opus-5[1m]

# Who is hurt by non-fatal violent crime, by ethnicity of victim and offender

Lane `infra/immigration-fiscal/ncvs_victim_offender_2026_09_18/`. September 18, 2026.
Model self-report: claude-opus-5[1m] (Opus 5, 1M context).

**Verdict:** Off the murder margin the victim–offender matrix looks nothing like the
homicide one. Pooling the National Crime Victimization Survey's published 2022–2024 tables,
the share of each offender group's violent incidents falling on a victim of the same group
is **0.760 for white offenders, 0.404 for Hispanic offenders and 0.345 for Black
offenders**, against **0.809 / 0.717 / 0.813** on cleared homicide. Every diagonal cell is
lower for non-fatal violence and the two minority diagonals are **roughly half** their
homicide values; the corresponding white-victim cells are two to three and a half times
their homicide values. Lethal violence really is far more intra-group than non-lethal
violence, and the gap is widest exactly where the homicide lane's numbers are weakest. The
second headline is on the offender side: **violent incidents per 1,000 residents age 12 or
older run 36.7 where the perceived offender is Black, 14.9 where white and 13.9 where
Hispanic** — the Hispanic rate is *below* the white rate, and age-standardising widens
rather than closes that gap, because Hispanic residents are younger and their age structure
alone predicts a rate **18% above** white. Pricing simple assault at the central figure
this lane derives, **$25,526** in 2024 dollars, the inter-group cost a Hispanic offender
population imposes is **$91 per Hispanic resident-year** in criminal-justice dollars,
against **$263** for Black and **$40** for white. [FRAMING-SENSITIVE] on every line: offender ethnicity here is the *victim's
perception*, and 18.3% of incidents carry no offender ethnicity at all.

**Correction, 2026-09-19.** Every per-resident-year cost transfer in the first version of
this file was **three times too high**. The pooled incident matrix was divided by pooled
person-years, which already yields a per-resident-year figure, and then multiplied by the
number of pooled years a second time. The figures below are the corrected ones; the
published Hispanic inter-group criminal-justice transfer of $195 to $385 per resident-year
should have read $65 to $128, Black $563 to $1,119 should have read $188 to $373, and white
$88 to $169 should have read $29 to $56. Ratios between groups are unaffected, and no other
quantity in the lane used that path: the victimisation rates and the cost-per-1,000 tables
divide the same pooled counts by the same pooled person-years and were always annual.
`analysis.py` now reassembles the transfer one year at a time and gates the pooled figure
against it exactly, so the same slip cannot recur silently.

**Route 1 — ICPSR microdata — was blocked by a login wall, so the lane is built entirely on
published tables**, with BJS's own generalized-variance standard errors rather than any this
lane computed. Three of the brief's requested arms (single-offender restriction,
reported-to-police only, injury only) exist only for 2012–15, where BJS published them.

---

## Phase 1: the three data routes

**Route 1 — ICPSR/NACJD NCVS Concatenated File 1992–2023 (ICPSR 38963): BLOCKED by a login
wall.** The study exists and the landing page renders under a browser User-Agent
(`https://www.icpsr.umich.edu/web/NACJD/studies/38963`, title "National Crime Victimization
Survey, Concatenated File, [United States], 1992-2023", DOI 10.3886/ICPSR38963.v1). Every
download path redirects to authentication:
`https://www.icpsr.umich.edu/cgi-bin/bob/zipcart2?path=NACJD&study=38963&bundle=all&ds=1&dups=yes`
returns **HTTP 302 → `https://www.icpsr.umich.edu/rpxlogin`**. No "download without login"
route is offered on the study page or the data-documentation page (both of which are
client-rendered shells). Per the brief the lane stopped there and **did not create an
account**; the probe results are in `derived/icpsr_route_probe.csv`.

Consequences, stated once and true of everything below: no record-level restriction is
possible, so **single-offender, reported-to-police-only and injury-only arms exist only
where BJS has already published them (2012–15)**; all standard errors are BJS's published
generalized-variance figures; and the unit of the matrix is the **incident**, not the
victimisation, because that is the unit BJS publishes the cross-tab in.

**Route 2 — BJS N-DASH: live, and it carries no offender characteristic at all.** The
dashboard at `https://ncvs.bjs.ojp.gov/` is a Vue application that reads static CSVs from
`/data/custom-graphics/<victimizationType>/<charA>_<charB>.csv`. The complete characteristic
list in its bundle (`/js/app.c7ab787c.js`, fetched 2026-09-18) is victim-side and
incident-side only: victim age, sex, race/Hispanic origin, marital status, household income,
household size, MSA status, population size, region, victim services use, victim–offender
relationship, weapon category, injury, reporting to police, location of incident, reason for
(not) reporting. **There is no offender race or Hispanic origin characteristic**, so N-DASH
cannot produce the matrix the brief asks for. It is used here for what it does carry:
victimisation rate, count, standard error and unweighted sample size by victim race/Hispanic
origin and crime type, 1993–2024 (`derived/ndash_rate_by_victim_race.csv`).

**Route 3 — the published BJS tables: this is where the matrix actually lives.** Two
families:

1. The **annual *Criminal Victimization* data tables**. Table 13 of the 2021–2024 editions
   ("Number of violent incidents, by race or Hispanic origin of victims and offenders") is
   the matrix, with appendix table 14 carrying its standard errors. The 2018 and 2019
   editions publish the same cross-tab under different numbering and different conventions.
   2017 publishes only marginals and **2020 has no such table** — the COVID-year report was
   cut back. This was not in the brief's route list and is the lane's main find.
2. **NCJ 250747, *Race and Hispanic Origin of Victims and Offenders, 2012-15*** (October
   2017, Rachel E. Morgan), `https://bjs.ojp.gov/content/pub/pdf/rhovo1215.pdf`, 476,937
   bytes. Its tables 1, 2, 3, 6 and 8 are transcribed into `derived/rhovo_t*.csv` and every
   transcribed number is gated against the `pdftotext` extraction of the PDF (133 values, 0
   missing).

### The window is set by definitional breaks, not by preference

The brief asked for 2017–2023. The comparable window is **2022–2024**, for reasons the
tables themselves state:

| Edition | Victim rows | Offender columns | Hispanic offender rule | Unknown offender |
|---|---|---|---|---|
| CV 2018 | White, Black, Hispanic, Asian | White, Black, Hispanic, Asian, Other, multiple-various | not stated | **excluded**, 11% of incidents |
| CV 2019 | White, Black, Hispanic | White, Black, Hispanic, Other | **any** offender perceived Hispanic | **excluded**, 16% |
| CV 2020 | — | — | — | table not published |
| CV 2021 | White, Black, Hispanic | White, Black, Hispanic, Other, Unknown | **all** offenders perceived Hispanic | own column |
| CV 2022–2024 | White, Black, Hispanic, **Other** | White, Black, Hispanic, Other, Unknown | **all** offenders perceived Hispanic | own column |

[SOURCE: cv18t14, cv19t15, cv21t13, cv22t13, cv23t13, cv24t13 and their footnotes]

Two breaks matter. The **2019 Hispanic-offender rule is "any offender perceived to be of
Hispanic origin"** in a multiple-offender group, while 2021 onward requires **all** of them;
that inflates the 2019 Hispanic column relative to later years. And **2021 publishes no
"Other" victim row**, so its rows cover only 3,995,290 of 4,403,570 incidents (90.7%), which
biases any column share computed on it. 2022–2024 is the widest window with a complete
victim universe and one convention throughout; 2021 is reported as a longer-window arm and
2018/2019 as their own arms.

---

## Phase 2: the matrix

### (a) Victim × offender, pooled 2022–2024, violent incidents

Counts, rows victim, columns perceived offender. Sum over three years; 18,240,550 incidents.

| victim ↓ / offender → | White | Black | Hispanic | Other | Unknown |
|---|---|---|---|---|---|
| White | 5,801,890 | 1,465,000 | 874,490 | 746,850 | 1,932,960 |
| Black | 271,820 | 1,323,160 | 208,860 | 103,930 | 455,300 |
| Hispanic | 957,770 | 640,870 | 880,760 | 183,630 | 608,350 |
| Other | 603,120 | 402,940 | 213,600 | 227,110 | 338,140 |

Standard errors (BJS generalized variance functions, summed in quadrature across years):

| victim ↓ / offender → | White | Black | Hispanic | Other | Unknown |
|---|---|---|---|---|---|
| White | 306,619 | 106,268 | 95,283 | 99,293 | 131,592 |
| Black | 40,007 | 132,603 | 76,536 | 33,479 | 74,047 |
| Hispanic | 144,327 | 130,010 | 97,710 | 30,651 | 84,279 |
| Other | 119,871 | 55,588 | 83,057 | 67,022 | 48,054 |

**The pooled standard errors are understated** and the memo should say so where it uses
them. NCVS runs a rotating panel in which a household stays in sample for three and a half
years, so adjacent annual estimates are positively correlated and the variance of a sum is
above the sum of variances. Quadrature is the right arithmetic only under independence.

**Offender ethnicity is unknown in 18.3%** of pooled incidents (3,334,750 of 18,240,550) —
the direct analogue of the SHR's missing-ethnicity problem, but a third of its size. CV2024
puts the 2024 figure at 19% in the footnote to table 11.

**Row shares, the arm with the unknown cell kept** (what fraction of each victim group's
violent incidents was committed by each offender group):

| victim | White | Black | Hispanic | Other | Unknown |
|---|---|---|---|---|---|
| White | 0.536 | 0.135 | 0.081 | 0.069 | 0.179 |
| Black | 0.115 | 0.560 | 0.088 | 0.044 | 0.193 |
| Hispanic | 0.293 | 0.196 | 0.269 | 0.056 | 0.186 |
| Other | 0.338 | 0.226 | 0.120 | 0.127 | 0.189 |

**Row shares, the arm with it dropped** (offender ethnicity known):

| victim | White | Black | Hispanic | Other |
|---|---|---|---|---|
| White | 0.653 | 0.165 | 0.098 | 0.084 |
| Black | 0.142 | 0.694 | 0.109 | 0.054 |
| Hispanic | 0.360 | 0.241 | **0.331** | 0.069 |
| Other | 0.417 | 0.279 | 0.148 | 0.157 |

A Hispanic victim's assailant is more likely to be white (0.360) than Hispanic (0.331).
That is a population-composition fact before it is anything else — non-Hispanic whites are
60.2% of the NCVS population age 12 or older and Hispanics 18.3% — but it is the number the
row-normalised table produces and it is the opposite of the homicide picture.

**Column shares — the victim distribution of each offender group.** This is the quantity
the homicide memo tabulates, so it is the one to compare:

| victim ↓ / offender → | White | Black | Hispanic | Other |
|---|---|---|---|---|
| White | **0.760** | 0.382 | 0.402 | 0.592 |
| Black | 0.036 | **0.345** | 0.096 | 0.082 |
| Hispanic | 0.125 | 0.167 | **0.404** | 0.146 |
| Other | 0.079 | 0.105 | 0.098 | **0.180** |

### Every cell against the cleared-homicide matrix

Homicide figures are SHR universe A, 2019–2023, ethnicity known on both sides, from
`research/immigration-homicide-victim-offender-and-treasury-cost-2026-09-18.md` §2.1.

| offender | victim | cleared homicide | non-fatal violent | difference | ratio |
|---|---|---|---|---|---|
| White | White | 0.809 | 0.760 | −0.049 | 0.94 |
| White | Black | 0.092 | 0.036 | −0.056 | 0.39 |
| White | Hispanic | 0.081 | 0.125 | +0.044 | 1.55 |
| White | Other | 0.018 | 0.079 | +0.061 | 4.39 |
| Black | White | 0.112 | 0.382 | **+0.270** | 3.41 |
| Black | Black | 0.813 | 0.345 | **−0.468** | 0.43 |
| Black | Hispanic | 0.064 | 0.167 | +0.103 | 2.61 |
| Black | Other | 0.011 | 0.105 | +0.094 | 9.56 |
| Hispanic | White | 0.156 | 0.402 | **+0.246** | 2.57 |
| Hispanic | Black | 0.110 | 0.096 | −0.014 | 0.87 |
| Hispanic | Hispanic | 0.717 | 0.404 | **−0.313** | 0.56 |
| Hispanic | Other | 0.016 | 0.098 | +0.082 | 6.13 |
| Other | White | 0.165 | 0.592 | +0.427 | 3.59 |
| Other | Black | 0.095 | 0.082 | −0.013 | 0.87 |
| Other | Hispanic | 0.077 | 0.146 | +0.069 | 1.89 |
| Other | Other | 0.663 | 0.180 | −0.483 | 0.27 |

**Every diagonal is lower off the murder margin**, and three of the four off-diagonal
white-victim cells are two to three and a half times higher. The white diagonal barely moves
(0.809 → 0.760); the Hispanic diagonal nearly halves and the Black diagonal more than
halves. Some of that is real — homicide concentrates in the dense intra-group networks where
disputes escalate — and some is the clearance selection the homicide lane already flagged:
cleared homicides over-represent domestic and acquaintance killings, which are
overwhelmingly intra-group. The two mechanisms cannot be separated from these data.

**Intra-group share against the victim group's own population share** normalises away the
composition effect:

| group | intra-group share | population share 12+ | concentration ratio |
|---|---|---|---|
| White | 0.760 | 0.602 | **1.26** |
| Black | 0.345 | 0.122 | **2.83** |
| Hispanic | 0.404 | 0.183 | **2.21** |
| Other | 0.180 | 0.092 | 1.95 |

Every group's violence is more intra-group than random targeting would give, and white
offenders are the *least* assortative of the four on this measure. The homicide diagonals
divided by these same NCVS population shares give 1.34 for white, 6.65 for Black and 3.91
for Hispanic offenders — a crosswalk, since the homicide lane's own denominator is the
all-age population — so the ordering (white least assortative) survives the move off the murder margin, while
the magnitudes collapse.

### (a2) Serious violent and simple assault separately

2019 is the only year with both an all-violent and an excluding-simple-assault matrix, so
simple assault comes out by subtraction (`derived/matrix_by_crime_type_2019.csv`; the
residual is non-negative in every cell, minimum 7,600). Column shares, 2019, three victim
rows, 2019's own conventions:

| scope | white→white | Black→Black | Hispanic→Hispanic |
|---|---|---|---|
| all violent | 0.868 | 0.324 | 0.397 |
| serious violent | 0.860 | 0.387 | **0.460** |
| simple assault | 0.873 | 0.291 | 0.350 |

The intra-group share **rises with severity for Black and Hispanic offenders** (by 6 and 6
points from simple assault to serious violence) and is flat for white offenders. That is the
same gradient as the homicide comparison, one notch down, and it is the single best piece of
evidence that the homicide–NCVS gap is partly real severity gradient rather than purely
clearance selection. 2018 shows the same direction (`derived/disconfirmation_arms.csv`).

### (b) The single-offender restriction

The SHR homicide universe is single-victim/single-offender. NCVS cannot be restricted that
way from published tables after 2015, but NCJ 250747 table 2 gives the split for 2012–15:

| offender | share of all violent victimisations | share of **single**-offender | share of multiple-offender | single minus all |
|---|---|---|---|---|
| White | 43.8% | 49.2% | 30.4% | **+5.4 pp** |
| Black | 22.7% | 23.2% | 24.7% | +0.5 pp |
| Hispanic | 14.4% | **12.5%** | **24.2%** | **−1.9 pp** |
| Other | 2.2% | 2.7% | 0.6% | +0.5 pp |

[SOURCE: BJS NCJ 250747 table 2]

**Hispanic offenders are concentrated in multiple-offender incidents**: 24.2% of
multiple-offender violence against 12.5% of single-offender violence, a factor of 1.9.
Restricting to the single-offender universe the SHR uses therefore removes a
disproportionate slice of Hispanic-attributed violence. Any comparison that takes the SHR's
single-offender matrix as representative of Hispanic offending in general is biased
downward on volume, and the direction of the bias on the *matrix* is unknown, because BJS
does not publish the victim × offender cross-tab separately by number of offenders.

### (c) Rates per 1,000

Pooled 2022–2024 incidents over pooled person-years age 12 or older:

| group | as victim | as offender |
|---|---|---|
| White | 21.05 | 14.85 |
| Black | 22.66 | **36.75** |
| Hispanic | 20.90 | **13.91** |
| Other | 22.69 | 16.03 |

Victimisation rates are close to flat across groups. **Offending rates are not**, and the
Hispanic rate is the lowest of the four, 6% below white. Two things this is not: it is not
an offender count (an incident with several same-group offenders counts once), and it is not
adjusted for the 18.3% of incidents with no offender ethnicity, which are excluded from the
numerator but not from anyone's denominator — so every rate here is a *lower bound* on the
group's true rate, understated by roughly the same proportion for all groups only if the
unknowns are distributed like the knowns.

Cross-check against N-DASH, built from the same survey but counting victimisations rather
than incidents: 22.87 white, 24.04 Black, 22.47 Hispanic, 24.61 Other, i.e. 1.06–1.09
victimisations per incident. That ratio is the multiple-victim factor and it is the same
across groups, which is the consistency check that matters here.

### (d) The cross-group cells the brief names

| | value |
|---|---|
| Hispanic offender → white victim | 0.402 |
| Hispanic offender → Hispanic victim | 0.404 |
| white offender → Hispanic victim | 0.125 |
| white offender → white victim | 0.760 |
| Black offender → Black victim | 0.345 |

A Hispanic offender's victim is as likely to be white as Hispanic. In cleared homicide the
same two numbers are 0.156 and 0.717.

### (e) Offence-mix cost weighting

Offence mix from N-DASH victimisations pooled 2022–2024:

| victim group | rape/sexual assault | robbery | aggravated assault | simple assault |
|---|---|---|---|---|
| White | 0.077 | 0.091 | 0.218 | 0.614 |
| Black | 0.073 | 0.137 | 0.240 | 0.549 |
| Hispanic | 0.071 | 0.139 | 0.194 | 0.596 |
| Other | 0.122 | 0.086 | 0.157 | 0.636 |

Unit costs, McCollister, French & Fang (2010) tables 3–5, 2008 dollars inflated by CPI-U
annual averages (215.303 → 313.689, factor 1.45697), the same table and the same
reconstruction gate `crime_cost_2026_09_16` uses, plus a central price for simple assault
derived in section 3 below:

| offence | social cost 2024$ | criminal-justice component 2024$ |
|---|---|---|
| rape/sexual assault | 350,802 | 38,579 |
| robbery | 61,644 | 20,145 |
| aggravated assault | 155,924 | 12,590 |
| **simple assault (central, derived)** | **25,526** | **5,120** |

Simple assault is 55–64% of every group's violent victimisations, and the first version of
this lane carried it at $0 and at the aggravated-assault price because McCollister publishes
no such offence. That was a factor of 2.4 on the majority of the volume and it is now
replaced by the central figure above. The derivation is section 3; the old two arms are kept
below so the reader can see where the central figure sits.

Cost of violent victimisation per 1,000 residents per year, 2024 dollars:

| arm | White | Black | Hispanic | Other |
|---|---|---|---|---|
| **social, simple central** | **1,732,724** | **1,942,298** | **1,649,080** | **2,012,016** |
| social, simple low (Miller 1996) | 1,538,496 | 1,755,328 | 1,461,775 | 1,795,285 |
| social, simple high (Miller 2021 reweighted) | 1,850,880 | 2,056,038 | 1,763,024 | 2,143,860 |
| social, simple at zero (legacy arm) | 1,402,926 | 1,624,825 | 1,331,038 | 1,644,008 |
| social, simple at aggravated (legacy arm) | 3,417,481 | 3,564,091 | 3,273,783 | 3,891,962 |
| **criminal-justice, simple central** | **225,104** | **259,180** | **230,392** | **264,464** |
| criminal-justice, simple at zero (legacy arm) | 158,952 | 195,501 | 166,598 | 190,649 |
| criminal-justice, simple at aggravated (legacy arm) | 321,611 | 352,081 | 323,459 | 372,153 |

**Inter-group cost transfer: what each offender group's violence costs victims outside the
group, per resident-year of the offender group**, 2024 dollars:

| arm | White | Black | Hispanic | Other |
|---|---|---|---|---|
| **social, simple central** | **296** | **1,984** | **695** | **1,079** |
| social, simple low | 264 | 1,762 | 620 | 959 |
| social, simple high | 316 | 2,119 | 741 | 1,151 |
| social, simple at zero (legacy) | 242 | 1,608 | 567 | 876 |
| social, simple at aggravated (legacy) | 576 | 3,907 | 1,351 | 2,114 |
| **criminal-justice, simple central** | **40** | **263** | **91** | **142** |
| criminal-justice, simple low | 40 | 263 | 91 | 142 |
| criminal-justice, simple high | 56 | 373 | 128 | 202 |
| criminal-justice, simple at zero (legacy) | 29 | 188 | 65 | 102 |
| criminal-justice, simple at aggravated (legacy) | 56 | 373 | 128 | 202 |

Totals including the intra-group cost, central arm: $161 / $408 / $153 / $176 per
resident-year at criminal-justice pricing and $1,225 / $3,072 / $1,139 / $1,335 at social
pricing, for white, Black, Hispanic and Other offenders respectively. The full grid over
five arms and two pricings is `derived/inter_group_cost_transfer.csv`.

**Two pairs of rows in that table are identical, by construction and not by mistake.** The
five arms carry five distinct social prices for a simple assault but only three distinct
criminal-justice prices, because the criminal-justice component of a simple assault has its
own bracket and does not depend on which quality-of-life valuation an arm picks. The central
and low arms share a criminal-justice component of **$5,120**, so their criminal-justice rows
coincide; the high arm's criminal-justice ceiling of **$12,590** is McCollister's
aggravated-assault figure, which is exactly what the legacy aggravated arm uses, so those two
coincide as well. Both cost CSVs now carry a `simple_assault_price_used` column naming the
price behind every row, and `analysis.py` gates the pattern: five distinct social prices and
three distinct criminal-justice prices. If the pricing ever stopped being switched per arm
the social column would collapse too and the gate would fire.

**The central price narrows the band that matters.** Across the three substantive
simple-assault routes the Hispanic inter-group criminal-justice transfer moves only between
$91 and $128 per resident-year, against $65 to $128 under the old zero-to-aggravated arms,
and the ordering across groups is identical in every arm. The old range was never
decision-relevant on ordering; it was decision-relevant on level, and the level is now
pinned to within about ±20%.

**Set beside the homicide lane, the picture inverts on volume and holds on ranking.** One
cleared homicide costs the treasury $1.5–1.8m, 91–97% of it prison. Non-fatal violence never
reaches those per-event numbers — $10,693 to $11,658 of criminal-justice cost per incident on
the central arm — but there are roughly six million violent incidents a year (6,075,830 in
2024) against roughly 23,000 homicide deaths a year (117,427 in 2019-2023 on the homicide
lane's CDC WONDER count). The **per-capita** inter-group transfer from non-fatal violence,
$40 to $263 per resident-year across groups on the central arm, is small against most lines
in the repo's fiscal ledger, and it is **larger for Black
offenders than for Hispanic by a factor of about 2.9 at every pricing and every arm**, and
larger for Hispanic than for white by 2.2 to 2.4.

---

## Phase 3: pricing a simple assault

The team lead's brief named three routes to a simple-assault price. Running them turned up a
fact that changes the shape of the answer, so it is stated first.

### Miller et al. (2021) does not publish a simple-assault cost

The paper is **paywalled**, not open access: the Cambridge page is an `/article/abs/` stub
offering "Get access" and "Purchase", OpenAlex reports `oa_status: closed` with no repository
full text, Semantic Scholar reports `isOpenAccess: false`, and the SSRN preprint
(abstract 3514296) sits behind a Cloudflare challenge. The PDF used here was retrieved
through the repo's research MCP by DOI and is pinned in `fetch.py` by sha256
`cccb174d…86103` rather than re-downloaded. The three PMC identifiers in the brief are
three different papers: PMC10421786 is a forensic genetic-genealogy cost-benefit analysis,
PMC10460458 is a dementia study in South Carolina prisons, PMC10712089 is alcohol costs in
Thailand.

Having read it: **table 5 prices "Assault" as a single category, $29,326 per crime in 2017
dollars** ($8,745 tangible, $20,581 quality of life; table 8 gives a 95% interval of
$24,975–$33,681, coefficient of variation 0.076). There is no simple-assault row, with or
without injury, in table 5, 6, 7, 8 or 9. A gate in `simple_assault_price.py` asserts this
rather than trusting the reading: of the two lines in the extracted text that mention simple
assault, neither carries a dollar figure. Table 4 does split the **incidence**: 7,492,068
simple and 1,417,526 aggravated assaults, so the priced category is **84.1% simple assault by
count** and its price is an arithmetic upper bound on simple assault. In 2024 dollars that
bound is **$37,530**, already 4.2 times below the $155,924 the old upper arm used.

### The other two routes

**Route 2, Miller, Cohen & Wiersema (1996), NIJ NCJ 155282.** The two-page document at
`ojp.gov/pdffiles/victcost.pdf` reports as 2 pages to `file` because of a damaged page tree,
but `pdftotext` recovers all 1,689 lines of the full research report, table 2 included. That
table gives "Other Assault or Attempt" split by injury, in 1993 dollars: **with injury
$24,000** (tangible $4,800, quality of life $19,300) and **no injury $2,000** (tangible $200,
quality of life $1,700).

**Route 3, derivation.** NCVS gives the injury share directly, from the N-DASH injury file
pooled 2022–2024: **12.88% of simple assaults and 24.26% of aggravated assaults** injure the
victim. The tangible victim cost is Miller 2021's medical, mental-health and productivity
columns scaled by that injury ratio, $3,481. The criminal-justice channel is Miller's own
public-services and adjudication columns scaled by simple assault's own arrest probability
(14.18% against 16.29% for the pooled category), $5,120, with McCollister's aggravated-assault
criminal-justice cost of $12,590 as the ceiling. Tangible bracket, no quality of life:
**$8,601 to $16,071**.

### One parameter governs the answer

Every route reduces to the same thing. If aggravated assault costs *k* times a simple assault,
then simple assault costs Miller's pooled price divided by (0.841 + 0.159*k*). The two
substantive routes are two values of *k* and they disagree because they import *k* from
incompatible costing methods:

| *k* | simple assault, 2024$ | where *k* comes from |
|---|---|---|
| 1.52 | 34,671 | the 1996 injured-to-uninjured relativity applied inside Miller's 2021 total |
| **3.96** | **25,526** | **the geometric mean of the two anchors** |
| 10.31 | 15,129 | Miller's pooled total minus McCollister's aggravated-assault price at Miller's own counts |

Route 1's *k* of 1.52 is **below what the survey alone requires**: aggravated assault injures
the victim 1.88 times as often as simple assault and leads to an arrest 1.93 times as often,
and it is more severe conditional on each of those. Route 4's *k* of 10.3 carries a
jury-award intangible cost into a QALY-based total, two methods that do not mix. The
geometric mean is the transparent compromise, it clears both survey floors, and
`derived/simple_assault_sensitivity_to_k.csv` gives the price at *k* from 1.5 to 13 so any
reader can move it.

### The central figure

**A simple assault costs $25,526 in 2024 dollars**: tangible **$8,601**, of which the
criminal-justice component is **$5,120**, plus **$16,925** of lost quality of life. The
tangible side is built from Miller's own cost columns and falls inside the independent
$8,601–$16,071 bracket of route 3; the quality-of-life figure is the residual under the
*k*-anchored total. Every route is in `derived/simple_assault_unit_cost.csv`:

| route | tangible | quality of life | criminal-justice | total |
|---|---|---|---|---|
| **central, *k*-anchored** | **8,601** | **16,925** | **5,120** | **25,526** |
| Miller 2021 reweighted to the simple-assault injury mix | 10,127 | 24,379 | 5,120 | 34,671 |
| Miller 1996 applied directly | 1,720 | 8,611 | — | 10,493 |
| derived tangible bracket, low | 8,601 | 0 | 5,120 | 8,601 |
| derived tangible bracket, high | 16,071 | 0 | 12,590 | 16,071 |
| residual against McCollister | — | — | — | 15,129 |
| Miller 2021 pooled assault (upper bound) | 11,191 | 26,338 | 5,882 | 37,530 |
| McCollister aggravated assault (old upper arm) | 17,479 | 138,445 | 12,590 | 155,924 |
| zero (old lower arm) | 0 | 0 | 0 | 0 |

Miller 1996 comes out lowest for two reasons worth naming: its quality-of-life valuation
predates the QALY methods Miller himself adopted later, and its cost columns contain no
adjudication or sanctioning line at all, so it omits the entire $5,120 criminal-justice
channel. Adding that channel back puts it at about $15,600, next to the McCollister residual
of $15,129 and inside route 3's bracket.

A complete Miller-2021 price set for all four NCVS offence categories is also written, to
`derived/miller2021_price_set.csv`, for anyone who wants the cost model run inside one
costing framework rather than McCollister's: rape/sexual assault $211,613, robbery $35,478,
aggravated assault $100,972, simple assault $25,526, all 2024 dollars. The lane's headline
tables keep McCollister for the three offences it prices, because the rest of the repo's
crime-cost work is built on it.

---

---

## Disconfirmation arms

Every arm reports the intra-group column share, the headline quantity.

| arm | white | Black | Hispanic | other |
|---|---|---|---|---|
| **C1a** unknown-offender column dropped (headline) | 0.760 | 0.345 | 0.404 | 0.180 |
| **C1b** unknowns allocated in proportion to each victim row's known offenders | 0.758 | 0.348 | 0.405 | 0.181 |
| **C1c** every unknown is an out-group offender (extreme) | 0.673 | 0.290 | 0.272 | 0.124 |
| **C1d** every unknown is an in-group offender (extreme) | 0.808 | 0.415 | **0.534** | 0.353 |
| **C2** 2012–15 baseline, three groups | 0.888 | 0.430 | 0.425 | — |
| **C2** reported-to-police incidents only | 0.884 | 0.442 | 0.440 | — |
| **C3** injury incidents only | 0.911 | 0.526 | **0.380** | — |
| **C3b** 2022–2024 restricted to three groups (baseline for C2–C5) | 0.825 | 0.386 | 0.448 | — |
| **C4** 2018, its own conventions | 0.877 | 0.358 | 0.441 | — |
| **C4** 2019, its own conventions | 0.868 | 0.324 | 0.397 | — |
| **C5** serious violent only, 2019 | 0.860 | 0.387 | **0.460** | — |
| **C5** simple assault only, 2019 | 0.873 | 0.291 | 0.350 | — |

**C1 is the arm that could overturn the headline and it does not.** The proportional
allocation moves nothing (0.404 → 0.405 for Hispanic offenders). Only the absurd bound in
which *every* unknown-ethnicity offender is in-group gets the Hispanic figure to 0.534, and
that is still 0.18 below the homicide figure of 0.717 and 0.13 below its imputed 0.667. The
conclusion that non-fatal violence is far less intra-group than homicide survives every
allocation of the unknown cell.

**C3 is the arm that moves the Hispanic number the wrong way.** Restricting to incidents
where the victim was injured raises the white intra-group share 2.3 points and the Black
share 9.6 points, but **lowers the Hispanic share 4.5 points**, from 0.425 to 0.380. On the
2012–15 data, violence against a Hispanic victim by a white or Black offender injures the
victim at 26.2% and 26.3% against 24.7% by a Hispanic offender — the only victim group whose
intra-group violence is the *least* injurious. So conditioning on severity pushes the
Hispanic diagonal down while pushing the others up, which is the opposite of the C5 crime-type
result on 2019 data. These two arms disagree and the lane cannot resolve them: C3 is 2012–15
and injury-defined, C5 is 2019 and offence-defined.

**C4 and C5 confirm the window choice.** The 2018 and 2019 vintages, on their own
conventions and restricted to three groups, give Hispanic diagonals of 0.441 and 0.397
against the 2022–2024 three-group baseline of 0.448 — a spread of five points across seven
years and three different offender-coding rules. The headline is not an artefact of the
window.

### The age arm

The homicide lane found that age-standardising closed 62% of the Hispanic–white
offender-age gap, so age is the obvious candidate for explaining the offender-rate ranking.
NCVS publishes perceived-offender age only as a national marginal in three bands, never
crossed with ethnicity, so a direct standardisation is not identified. Two bounds:

- On the **published offender bands** (12–17, 18–29, 30 or older) the implied national rates
  are 17.01, 16.58 and 15.90 per 1,000 — a 1.07 ratio end to end. The 30-or-older band is so
  wide that the age–crime curve is invisible inside it. This arm returns nothing, and that is
  a fact about the instrument, not about age.
- On the **fine grid** CV2024 table 3 publishes a victimisation rate for (12–17, 18–24,
  25–34, 35–49, 50–64, 65+; 29.3 / 34.8 / 31.7 / 27.1 / 20.4 / 7.5, a 4.6× gradient), applied
  to each group's ACS 2023 age structure, age composition alone predicts an index of
  **1.000 white, 1.110 Black, 1.181 Hispanic**. Observed is **1.000 / 2.474 / 0.937**.

So **age composition runs against the Hispanic result, not for it.** The Hispanic 12+
population is younger — 12.9% aged 12–17 and 14.1% aged 18–24, against 7.3% and 9.1% for
whites — and on the age curve alone it should show 18% *more* violence per resident than the
white population. It shows 6% less. Age-adjusting the ratio gives 0.937 / 1.181 = **0.79**.
Using the victim-age curve as a stand-in for the offender-age curve is the weak step here;
in violent crime victims and offenders are close in age, but not identical.

---

## Limits, stated plainly

1. **Offender ethnicity is the victim's perception**, not a record. NCJ 250747's own
   methodology note argues victims can usually identify it, citing Van Koppen & Lochun
   (1997) on the validity of offender descriptions, but this is a different measurement from
   the SHR's police-recorded ethnicity and the two are not interchangeable. Any systematic
   misperception — for instance, toward "Hispanic" for a Spanish-speaking stranger — lands
   directly on these cells.
2. **Multiple-offender incidents are coded by the group, not the individual.** From 2021
   onward an incident counts as Hispanic-offender only if *all* offenders were perceived
   Hispanic; mixed groups go to "Other". In 2019 the rule was the opposite for Hispanic. The
   "Other" offender column absorbs 222,030 mixed-group incidents in 2024 alone.
3. **Mexican origin is not in the NCVS.** Hispanic origin is a single yes/no. Nothing in
   this lane is a Mexican-origin figure, and the homicide lane's ACS bridge (53% to 75% of
   Hispanic prisoners Mexican-origin) is the only available crosswalk.
4. **The 2016 redesign is a series break.** The NCVS sample was redesigned and the
   victimisation rate series has a documented discontinuity; BJS published *Criminal
   Victimization, 2016: Revised* for that reason. This lane's window starts in 2018 and the
   matrix window in 2022, both after the break.
5. **Incidents, not victimisations.** The matrix is in incidents; the offence mix and the
   N-DASH cross-check are in victimisations. The ratio is 1.06–1.09 and uniform across
   groups, so the mix shares transfer, but the levels do not.
6. **The pooled standard errors assume between-year independence** and therefore understate
   the true sampling error, as above.
7. **Simple assault has no published unit cost in either costing framework the repo
   uses**, and it is most of the volume. Phase 3 derives one, but it rests on an
   aggravated-to-simple cost ratio that no source publishes and that the two available
   anchors put at 1.5 and 10.3. That ratio, not the survey, is now the largest single
   uncertainty in the cost section.
8. **These are resident groups, not admission categories.** The repo measures residents. The
   sign convention on the absolute account is a convention; the gap against same-age whites
   is not. No policy conclusion follows from any number here.

---

## Verification that was run and passed

```sh
cd /Users/alien/Projects/immigration-research/infra/immigration-fiscal/ncvs_victim_offender_2026_09_18
UV='uv run --no-project --with "pandas>=2" --with "numpy>=2" python3'
PYTHONUNBUFFERED=1 $UV fetch.py && PYTHONUNBUFFERED=1 $UV build.py \
  && PYTHONUNBUFFERED=1 $UV simple_assault_price.py \
  && PYTHONUNBUFFERED=1 $UV analysis.py && PYTHONUNBUFFERED=1 $UV age_standardise.py
```

- **Column sums reproduce BJS's own offender marginal.** For 2022, 2023 and 2024 the column
  totals of table 13 equal the offender-incident column of table 11 to within 10 incidents:
  white 2,316,030 / 2,316,030, Black 1,371,630 / 1,371,630, Hispanic 795,760 / 795,750,
  Other-plus-Asian-plus-mixed 459,720 / 459,720 in 2024. Row totals likewise reproduce the
  victim marginal. These are two independently published tables in the same report and they
  agree, which is the strongest available check that the parse is right.
- **NCJ 250747 transcription gate.** All 133 transcribed values from tables 1, 2, 3, 6 and 8
  appear verbatim in the `pdftotext` extraction of the PDF.
- **Population vintages agree exactly.** White, Black and Hispanic population age 12+ is
  identical across the CV2018, CV2019, CV2021 and CV2024 appendix tables on all 21
  overlapping cells. Asian and Other differ by up to 16.6% because CV2021 moved Native
  Hawaiian and Other Pacific Islander from "Other" into the Asian category; neither group
  carries a headline here.
- **McCollister components reconstruct the published totals**, the same gate
  `crime_cost_2026_09_16` runs; the removed risk-of-homicide slice is $113 / $1,663 / $7,470
  (2008$) for the three priced offences.
- **Simple assault by subtraction is non-negative** in every 2019 cell, minimum 7,600.
- **Miller 2021 and Miller 1996 transcription gates.** All 33 transcribed values from Miller
  et al. (2021) tables 4, 5 and 8 and all 9 from Miller, Cohen & Wiersema (1996) table 2
  appear verbatim in the `pdftotext` extractions. Cambridge drops the thousands separator in
  four-digit figures, so the gate accepts either rendering.
- **Miller 2021's published components close.** Its seven tangible columns for assault sum
  to $8,745, the published tangible subtotal; tangible plus quality of life equals the
  published $29,326 total; and its simple and aggravated counts sum to the assault total.
- **Miller 2021 carries no simple-assault price**, asserted by gate rather than by reading:
  of the two lines in the extracted text mentioning simple assault, neither carries a dollar
  figure.
- **The central decomposition reconstructs the published pooled cost.** Splitting Miller's
  assault category into simple and aggravated at the chosen ratio and reweighting by his own
  counts returns $29,326, the published figure, to the dollar.
- **The chosen aggravated-to-simple ratio clears both NCVS floors**, the 1.88 injury ratio
  and the 1.93 arrest ratio, and the resulting quality-of-life residual is positive.
- **The simple-assault arms are ordered** $10,493 < $25,526 < $34,671 < $155,924.
- **The cost transfer is per resident-year, checked two ways.** The pooled figure is
  reassembled one year at a time, each year's own matrix over its own population, and the
  two agree to within a part in a billion for all four groups. Separately, the Hispanic
  offender-side total of $110.02 per resident-year at criminal-justice pricing with simple
  assault at zero matches the $110.90 implied by the Hispanic victim-side cost per person
  and the ratio of the Hispanic offending rate to the Hispanic victimisation rate, a gap of
  0.8%. The same approximation reads +2.1% for white, −6.3% for Black and −6.5% for Other,
  and those gaps are the cost-weighted victim mix: a Black offender's victims are 38.2%
  white, whose incidents are cheaper than a Black victim's, so the approximation is not
  exact for that group and is reported as a diagnostic rather than a gate.
- **Victimisations per incident** are 1.06–1.09 across all four victim groups, i.e. the
  N-DASH and *Criminal Victimization* series are mutually consistent.
- **Reproducibility, warm:** re-running all five scripts with `_cache/` intact leaves
  `derived/` byte-identical (`diff -rq` clean, 35 files).
- **Reproducibility, cold:** with `_cache/` deleted and every source re-fetched from BJS,
  the Census API and BLS, all 26 files produced by `fetch.py`, `build.py` and `analysis.py`
  were byte-identical (`diff -rq`, zero differing files), and the four `age_standardise.py`
  outputs reproduced byte-identically against a fresh ACS API call. That cold run predates
  phase 3; the Miller 2021 PDF cannot be re-fetched by URL, so `fetch.py` verifies the
  cached copy by sha256 (`cccb174d…86103`) and fails loudly if it is missing.

## Files

Scripts: `fetch.py`, `build.py`, `analysis.py`, `age_standardise.py`,
`simple_assault_price.py`, `README.md`. `derived/` holds the CSVs plus `analysis_log.txt`
and `simple_assault_price_log.txt` (the full gated console transcripts).
Everything downloaded is under `_cache/` with sha256 in `derived/source_manifest.csv`.

## Skipped, with reasons

- **ICPSR 38963 microdata.** Login wall, documented above. Nothing was worked around.
- **CV 2017 and CV 2020.** 2017 publishes offender demographics only as marginals (table
  10), not crossed with victim ethnicity; 2020's report was cut back and publishes no
  victim × offender table and no data-table zip.
- **Generalized-variance standard errors computed by this lane.** Not possible without
  microdata; BJS's published SEs are used instead and are better than anything this lane
  would have produced from a public-use file.
- **Single-offender, reported-to-police and injury arms on the 2022–2024 window.** BJS
  publishes those cross-tabs only for 2012–15. The arms run there and are labelled.
- **A published simple-assault unit cost.** There is none. Miller et al. (2021) is
  paywalled and prices assault as one category; Miller, Cohen & Wiersema (1996) is free and
  splits assault by injury but not by degree. Phase 3 derives a central figure instead.
- **Mexican-origin split.** Not in the NCVS at all.

## The one thing to carry forward

The homicide lane's intra-group shares and this lane's cannot both be read as "how much
violence stays inside the group" — they differ by a factor of two on the Hispanic and Black
diagonals, and the 2019 severity gradient says at least part of that is real. Any repo claim
about assortative victimisation has to name the margin it is measured on. The quantity that
travels across margins is the **concentration ratio** against population share, where the
ordering (white least assortative) is the same on both.

The second thing to carry forward is narrower and concerns the cost model the whole repo
shares: **no crime-cost source in use prices a simple assault**, and simple assault is the
majority of all violent victimisation. This lane's $25,526 is a derivation, not a citation,
and it turns on an aggravated-to-simple ratio the literature does not report. Any repo figure
that weights offences by cost inherits that gap.
