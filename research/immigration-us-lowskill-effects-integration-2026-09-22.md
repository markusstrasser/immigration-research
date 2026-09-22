# Fourteen US low-skill effect papers: what joins the account and what stands on its own

Date: 2026-09-22. [SOURCE: fourteen primary texts in the local corpus, read in full by
one extraction agent each with every number re-found verbatim in the parsed text;
the parent spot-checked the rows quoted here against the source files. CALCULATION
rows reuse existing lane outputs. FRAMING-SENSITIVE in §5.] Reading record; narrative
authorship remains operator-owned.

**Verdict:** Four of the fourteen papers change something inside the fiscal account, and
they all act on the same object: the elasticity ε between natives and foreign-born workers
inside a skill cell, which the executed nest (ladder 176) left as the operator's call. Read
in the primary texts, the two numbers the 2026 removal model averages to ε = 3 are a
firm-level H-2B figure of **1.26 with a 95% interval of 0.12 to 2.39** backed out of an
insignificant employment coefficient (Clemens–Lewis), and a **calibrated** within-occupation
4.6 with no standard error whose own aggregate counterpart the authors put at **about 9**
(Burstein et al., footnote 42). The two papers that estimate the object directly for
low-skill workers put it at **8.7 to 17** nationally (Caiumi–Peri: 1/σ = 0.115 ± 0.031 for
no-diploma workers, 0.058 ± 0.025 pooled) and **17.9 ± 0.8** across cities (Piyapromdee).
That range brackets the account's own-file sketch of about 6 and sits far from 3. Computed
on the nest at those two elasticities (rows added the same evening), the production term is
**+$18.0bn (GDP scaling) / +$11.9bn (cash) at ε = 8.7 and +$15.6 / +$10.3bn at ε = 17.9**
against the published +13.3 / +8.8bn, so the adjustment to the $165–197bn headline is
**about $2 to 5bn, not the $9 to 14bn** that ε = 3 implied. Sign unchanged, size smaller,
still not applied. The other ten papers do not
touch the account's terms. They supply four sections that stand on their own: who bears the
wage cost (earlier immigrants and entering cohorts, locals briefly), whether removal hands
jobs to natives (three designs say no), housing (a demand shock now, a construction-cost
channel later), and who gains from selection. Two papers are method only. Nothing here is a
stationary fiscal object; every estimate is a marginal flow, a firm, a city or a season.
[CALCULATION: `production_nativity_nest_2026_09_22/derived/nest_headline.csv`, Option A
rows; reads in `us_lowskill_effects_2026_09_22/reads/`]

## 1. What each paper measured

The extraction files under
[`us_lowskill_effects_2026_09_22/reads/`](../infra/immigration-fiscal/us_lowskill_effects_2026_09_22/reads/)
hold the full tables with page anchors and verbatim quotes. This section keeps only what
the placement decision needs. Standard errors in parentheses.

| Paper | Design and unit | Result that matters here | Fiscal content |
|---|---|---|---|
| Caiumi–Peri, NBER w32389 (2024) | National 32 education × experience cells, 1960–2022, new skill shift-share + demographic IV, F 13–36 post-2000 | Own estimate is only σ_IMMI and the employment response: 1/σ 0.058 (0.025) pooled 2000–19, **0.115 (0.031) no diploma**, 0.017 (0.006) HS graduates; native emp/pop +0.075 (0.013) per log immigrant employment. The +1.7 to +2.6% wage gain for less-educated natives is a **simulation** whose cross-skill elasticities (1/σ_HL = 0.54) are imported from Ottaviano–Peri 2012 | none |
| Piyapromdee, RESTUD (2020) | Spatial equilibrium, 114 metros, Census 1980–2000 + ACS 2005–07, enclave IV, first-stage t 11–26 | σ between natives and immigrants: **17.87 (0.82) low skill**, 6.93 (0.15) high skill; σ high/low skill 2.19 (0.11); skill-selective policy (+46% high-skill immigrants): low-skill male natives +1.1% welfare, high-skill male natives −2.9%, incumbent high-skill immigrants −8.6% in gateway cities; national average −0.8% before rental income, +$94 a head after | none |
| Burstein–Hanson–Tian–Vogel, Econometrica (2020) | 722 commuting zones × 50 occupations, 1980–2012, Card shift-share, AP F 48–136 | Natives crowded out of immigrant-intensive **nontradable** occupations (−0.30 (0.10) low-ed, −0.37 (0.13) high-ed differential), precise zero in tradables (0.002 (0.089)); ρ = 4.6 is **calibrated** to those moments, no SE; "the aggregate substitution elasticity is not a structural parameter in our model. When we estimate it using model-generated data, it is roughly twice as high as our assumed value of ρ" (fn. 42); halving Latin American immigrants lowers low-education native real wages 1.3% in Los Angeles, 3.1% in Miami | none |
| Clemens–Lewis, NBER w30589 (2022, rev. 2024) | 472 firms in the 2021–22 H-2B lotteries, pre-registered; first stage 0.618 (0.112) | Revenue elasticity 0.20–0.22, investment 1.5–2.1, profit rate 0.15; US temporary employment +0.06 to +0.19, imprecise; rural +0.61 (AR p 0.05); **σ = 1.26, 95% CI (0.12, 2.39)**, solved from the US-employment coefficient 0.061 (0.125) under assumed η ≈ 8; landscaping 46%, forestry 16%, seafood 10% of firms; "US worker" includes permanent residents | none |
| Amuedo-Dorantes et al., IZA 16438 (2023) | ~3,300 H-2B applicants, Census LBD at an FSRDC, 2015–21, an unanticipated 2018 processing cutoff | Employment per approval 0.74 (0.13) to 0.80 (0.19), about one per hire; revenue elasticity ≈ 0.14 per hire; competitor spillovers 0.002–0.004, null; no nativity split in outcomes | none |
| Monras, JPE (2020) | Peso-crisis push × networks IV, states and metros, F 19–27; CPS 1990s; structural spatial model | Short-run native low-skill wage **−0.71 (0.31) state, −1.42 (0.33) metro** per 1% supply shock; high-skill null; low-skill population share +1.08 (0.29) in 1995 then −0.74 (0.41) in 1996; 1990→99 −0.26 / −0.38, not significant; entering cohorts long run: wage −0.53 (0.13), employment rate −0.57 (0.14); rental gap +0.68 / +0.56 short run, gone by 1998; 1990–2000 rents and house prices fall, −0.55 / −0.78 state and −1.17 / −1.43 metro, with native construction wages −0.45 / −0.77 | none |
| Llull, JHR (2018) | National skill cells, US + Canada, push × distance × cell IV, F 6–19 | Own-cell wage elasticity ≈ −1.1 to −1.2 by IV against −0.34 to −0.48 by OLS; compliers are low-education mid-career cells; perfect substitution within cell assumed | none |
| Lin–Weiss, Demography (2019) | State × year immigrant shares, RIF quantile regressions, 1980–2015, N 16.5m; **association**, IV only as a robustness check with no first stage reported | Low-skill immigrants: natives at p10–15 about −2% per 10 points, **earlier immigrants at p10 −11.5%**; high-skill immigrants: natives at p90 +15%, p95 +22% | none |
| Clemens–Hunt, ILR Review (2019) | Replication of Mariel and three refugee waves | Borjas's subsample is about 17 observations a year whose Black share moves 0.36 → 0.91; with a race indicator the 1984–86 coefficient goes from −0.37 / −0.45 to −0.14 (ns) / −0.23; what survives for dropouts is "roughly 2% to 8% ... but it is also compatible with ... zero"; the Borjas–Monras IV results for Israel, France and Europe reproduce with a white-noise instrument | none |
| Borjas–Cassidy, Labour Economics (2019) | ACS 2008–16, Pew residual imputation of status | Raw undocumented/legal log gap 0.413 (0.003) men; **0.061 (0.003) after observables**, 0.027 with occupation; men's penalty 6.7 → 4.1 by 2016; σ legal vs undocumented 17.0 men / 11.5 women | status classifier uses benefit receipt, so the imputed undocumented receive none by construction |
| Wilson–Zhou, Dallas Fed 2607 (2026) | 721 commuting zones / 348 metros, 2021–24, two-way leave-out shift-share on **restricted** immigration-court microdata, F 14–43 | Per unauthorized worker inflow of 1% of employment: employment 0.96 (0.27), weekly wages −0.93 (0.61), house prices +2.19 (0.74), rents +1.44 (0.34), permits −0.21 (0.21); native employment 0.18 (0.85), native hourly earnings −0.69 (0.38) with no skill gradient; **BEA transfer receipts −4.5 (1.4) over 2021–23 but −1.4 (0.7) over 2021–24**; the public ancestry instrument is their **rejected** alternative, F 6.80, Mexico carrying 0.67 of the identifying weight | transfers only, as a local receipts total; no taxes, services or schooling |
| Cox–East, NBER w35129 (2026) | 58 areas, ICE arrest surges Jan–Oct 2025, event study on monthly CPS | Likely-undocumented employment −1.3 pts (men −2.8 / −3.5); US-born employment null with **gains above +0.3 pts excluded**; US-born men **−0.6 pts**, significant; no wage rise; 7 immigrant men stop working per arrest | none |
| Clemens–Lewis–Postel, AER (2018) | Bracero exclusion 1964, state exposure from 1955 shares | Farm-wage semi-elasticity −0.083 (0.065), −0.075 (0.051) for 1960–70; the model's +0.4 (about +12% at exposure 0.3) rejected at 1%; upper 95% bound +0.02 to +0.07, so a high-exposure state rules out a wage rise above roughly 0.7 to 2.1% [CALCULATION, reader]; employment −0.31 (0.51); tomato harvester adoption jumps in California | none |
| Dee–Murphy, AERJ (2019) | 168 counties that applied for 287(g), 2000–11, county-year DD and DDD | Hispanic K–12 enrollment −0.076 (0.035) static, **−0.102 (0.047) two or more years after adoption**; non-Hispanic −0.005 (0.016); the effect sits in K–5 (−0.099); pupil–teacher ratio +0.27 (0.20), null; enrollment-weighted estimates are −0.199 Hispanic and −0.065 non-Hispanic, both significant, so the placebo fails under weighting | staffing follows enrollment; no dollars |

Borjas's "The Labor Supply of Undocumented Immigrants" has only a cover sheet in the corpus
and is not read. East et al. (Secure Communities), Christopher (undocumented rent premium)
and Mahajan (firm exit) did not download.

## 2. What joins the fiscal account

### 2.1 The production term's elasticity, now with its provenance

The removal model the account was compared with in FAQ 14 takes ε = 3 as "the midpoint of
two published estimates, 1.3 and 4.6"
([leads read, §3](immigration-marginal-revolution-leads-read-2026-09-21.md)). The two
primary texts say what those numbers are:

| Source | Object | Level and population | Value | Uncertainty |
|---|---|---|---|---:|
| Clemens–Lewis 2024, Table 7 | firm-level "effective" foreign–native elasticity inside the low-skill nest, monopsony included, between-firm reallocation excluded | 472 seasonal nonfarm H-2B firms, 2021–22 | 1.26 | 95% CI (0.12, 2.39); 0.8–2.2 across assumptions; solved from an employment coefficient of 0.061 (0.125) |
| Burstein et al. 2020, Table III | ρ, natives vs immigrants **within one occupation** | 722 CZs, calibrated to two 2SLS moments | 4.6 | none, calibrated; the authors' aggregate counterpart ≈ 9 (fn. 42); ρ = 13.8 breaks their tradable moment |
| Caiumi–Peri 2024, Tables 6–7 | σ_IMMI, natives vs immigrants within an education × experience cell | national, 2000–2019, 2SLS | 17 pooled; **8.7 no diploma**; 59 HS graduates; 22 used in the low-cell simulation | 1/σ 0.058 (0.025); 0.115 (0.031) |
| Piyapromdee 2020, Table 1 | σ_M,L, natives vs immigrants within a low-skill × gender cell | 114 metros, IV | **17.9** | (0.82) |
| Own file, ladder 176 sketch | two-cell nest ε consistent with occupation overlap 0.644 | CPS 2024, union vs outside | ≈ 6 | 4–9 |
| Removal model | ε | national | 3 | midpoint of the first two rows |

[SOURCE: reads `clemens_lewis_h2b.md`, `burstein_ecta_2020.md`, `caiumi_peri_nber_2024.md`,
`piyapromdee_restud_2020.md`; parent re-found the (0.12, 2.39) interval and the footnote 42
sentence in the parsed texts]

The three estimates of the low-cell object itself, 8.7, 17 and 17.9, and the own-file 6, all
lie above the removal model's 3. The nest grid was extended with 8.7, 9 and 17.9 on the
evening of 2026-09-22 (all nine gates pass, independent re-derivation to 5e-12bn)
[CALCULATION: `nest_headline.csv`, Option A, σ = 2, full capital adjustment]:

| ε | term, GDP scaling ($bn) | term, cash ($bn) | natives after tax | other foreign-born | change vs perfect substitution, GDP / cash |
|---:|---:|---:|---:|---:|---:|
| ∞ (published) | 13.32 | 8.79 | −0.6 | +0.4 | 0 / 0 |
| 20 | 15.35 | 10.13 | +7.4 | −6.4 | +2.0 / +1.3 |
| 17.9 (Piyapromdee) | 15.59 | 10.29 | +8.3 | −7.2 | +2.3 / +1.5 |
| 9 (Burstein aggregate, inferred) | 17.85 | 11.78 | +17.2 | −14.7 | +4.5 / +3.0 |
| 8.7 (Caiumi–Peri, no diploma) | 18.01 | 11.88 | +17.8 | −15.2 | +4.7 / +3.1 |
| 7 | 19.16 | 12.64 | +22.4 | −19.1 | +5.8 / +3.9 |
| 4.6 | 22.25 | 14.68 | +34.6 | −29.5 | +8.9 / +5.9 |
| 3 | 27.13 | 17.90 | +54.0 | −45.9 | +13.8 / +9.1 |
| 1.3 | 46.17 | 30.46 | +130.5 | −111.1 | +32.8 / +21.7 |

So at the published low-cell estimates the production term is **+$15.6 to 18.0bn GDP /
+$10.3 to 11.9bn cash**, the headline band would move by **$2 to 5bn**, and the transfer
inside the beneficiary set shrinks from ±$50bn at ε = 3 to ±$7–18bn. The comparison in FAQ 14 with the removal model's $38.6bn native loss
stands, with the added fact that its ε rests on one interval that includes 0.12 and one
calibrated number whose own authors double it. Whether to adopt an ε remains the operator's
call; the evidence now points to the upper half of the grid rather than the lower.

Two cautions carry over from the reads. Clemens–Lewis's σ is the right kind of object for
the removal margin the H-2B quota moves, seasonal firms with few substitutes, and a poor one
for a three-generation resident stock that holds 47% of the low cell's earnings in US-born
hands. Caiumi–Peri's 17 is a pooled figure; their no-diploma cell at 8.7 and their
high-school-graduate cell at 59 bracket the union's low cell, whose diploma split this memo
does not tabulate.

### 2.2 The "wage bound" does not run cleanly

The nest reports the low-cell native wage with the union present against absent: −5.6% at
perfect substitution, −4.4% at ε = 7, −2.9% at ε = 3, +1.0% at ε = 1.3
[CALCULATION: `nest_headline.csv`, `wage_pct_native_cell0`, sign reversed to "with union"].
Setting that beside the literature's elasticities (Monras −0.7 to −1.4 short run and −0.26
long run per 1% supply, Llull −1.1 per 1% of a cell, Caiumi–Peri +1.7 to +2.6% for a
twenty-year inflow that was mostly college-educated) does not produce a test, because the
account's number is the composition effect of removing 8.35% of national earnings
concentrated in one cell, a stock, while every published number is the marginal effect of a
flow whose skill mix differs from the union's. The bound proposed in the morning's chat is
therefore not executed; the elasticity table in §2.1 is the usable part.

### 2.3 Transfers: same sign as the displacement lane, same instrument problem

Wilson–Zhou's transfer result is the one fiscal object in the set. It is the BEA transfer
receipts component of county personal income, aggregated to commuting zones, for all
residents, with no program decomposition: −4.5% (1.4) per 1% inflow over 2021–23 and −1.4%
(0.7) over 2021–24, a gap the authors attribute to take-up rising with tenure. The sign
agrees with the account's displacement lane (SSI and public assistance receipt move down
with foreign-born inflow on 2000–2010, ladder 140). It is a local relative effect of recent
arrivals on a receipts total and cannot be carried into a per-person stationary account.

The downloaded ancestry-instrument files are the paper's rejected instrument: first-stage F
6.80 against 14–43 for their preferred two-way leave-out design, with Mexico carrying 0.674
of the identifying weight. The preferred design needs origin-by-destination flows from
restricted immigration-court records. The account's own finding that the settlement
instrument is dead for 2021–24 (F 0.002, ladder 140) is a different construction and is not
contradicted; it is not rescued either. The county file does serve the 2000–2010 window as a
second instrument, and that was executed the same evening: F 63.9 against the settlement
instrument's 29.1, no correlation with the 2000 baseline level (the settlement instrument
has one), a third of its variance from Mexico; the SSI response becomes −0.28 (0.06) instead
of −0.44 (0.10) and the public-assistance response a null (−0.10 ± 0.19) instead of −0.99
(0.28), with Hansen J rejecting the pair. The displacement lane's negative claim stands at a
smaller size (ladder 182, [lane](../infra/immigration-fiscal/ancestry_instrument_2026_09_22/RESULT.md)).

### 2.4 Two small pointers

**Legalization.** Borjas–Cassidy's adjusted male penalty of 4–6% is the wage change a
legalization scenario would carry for the union's unauthorized members. The account does
not split the union by legal status, so the number goes to the assumption explorer as a
sensitivity, not to a term; at any plausible unauthorized earnings base it is a few billion
of taxable earnings, not tens.

**School response.** Dee–Murphy find that when Hispanic enrollment falls 7–10% under local
enforcement, the pupil–teacher ratio does not move, so districts shed staff in step with
pupils within two years. That is a staffing response near one, above the 63–66% spending
response the account takes from CBO, on a different margin (a fall, local, two years) and
without dollars. It is a footnote for FAQ 2's sensitivity, not a replacement.

## 3. Sections that stand on their own

None of the following changes a line of the account. Each is a reading the essay can carry
as its own section, with the account's frame stated once: these are flows, firms, cities and
seasons, not a resident stock.

### 3.1 Who bears the wage cost

The reconciled picture across Monras, Llull, Lin–Weiss, Clemens–Hunt and Caiumi–Peri is
about incidence and horizon, not about whether a wage effect exists.

- **Locals, briefly.** An unexpected Mexican inflow of 1% of the local low-skill labor
  force lowers native low-skill wages 0.7% (states) to 1.4% (metros) on impact; the
  low-skill population share rises one for one in the first year and reverses the next; by
  1999 the 1990 cross-section shows −0.26 / −0.38, not significant. High-skill natives: null
  at every horizon. [SOURCE: Monras Tables 3, 7, 8]
- **Entering cohorts, lastingly.** Cohorts that entered the labor force in high-immigration
  years carry −0.53 (0.13) on wages and −0.57 (0.14) on the employment rate a decade later,
  the one long-run labor-market effect Monras finds. [SOURCE: Monras, cross-age IV]
- **Earlier immigrants, most.** Per 10 points of low-skill immigrant share, natives at the
  10th–15th percentile lose about 2% and immigrants at the 10th percentile lose 11.5%; the
  own-group effect is five times the cross-group effect, in an association design.
  [SOURCE: Lin–Weiss Fig. 2] Caiumi–Peri's simulation has the same shape: less-educated
  natives +1.7 to +2.6%, college-educated immigrants −6.7 to −10.9%.
- **The national cell number.** Llull's IV own-cell elasticity of about −1.1 is two to
  three times the OLS −0.4, with low-education mid-career cells as compliers; it assumes
  perfect substitution inside the cell and so is the Borjas object, not the Card one.
- **Mariel.** The large dropout loss is a racial-composition break in about 17 observations
  a year; what survives is −2 to −8% or zero.

The essay's use of this: the honest sentence is that the wage cost of a low-skill inflow is
real, short-lived where it lands, permanent for the cohort that arrives with it, and borne
mostly by the previous wave. That is also why the account's beneficiary set nets natives
against other foreign-born residents (§2.1).

### 3.2 Removal does not hand jobs to natives

Three designs at three scales, none of which finds native employment gains from removing or
withholding low-skill immigrant labor:

- **A historical exclusion.** Ending the Bracero program removed about half a million
  workers; the farm-wage semi-elasticity is −0.08 (0.07), the model's +0.4 is rejected at
  1%, and a high-exposure state can rule out a wage rise above roughly 0.7 to 2.1%. Domestic
  seasonal employment −0.31 (0.51). Growers mechanized tomatoes and abandoned crops that
  could not be mechanized. [SOURCE: Clemens–Lewis–Postel Tables 1–2]
- **A live enforcement surge.** In 2025, areas whose ICE arrests doubled saw
  likely-undocumented men's employment fall 2.8 to 3.5 points, US-born employment gains
  above 0.3 points excluded, US-born men −0.6 points, no wage rise; the US-born losses are
  largest in undocumented-intensive nontradable sectors. Nine months, area-relative, outflows
  not measured. [SOURCE: Cox–East Figures 3 and 5, Table A1]
- **A randomized quota.** Firms that win H-2B visas raise revenue (elasticity 0.20–0.22),
  investment (1.5–2.1) and profit rate (0.15); US employment +0.06 to +0.19, imprecise,
  +0.61 in rural firms; the administrative version on 3,300 firms finds about one job per
  hire and no competitor harm. Seasonal, firm-level, and "US worker" includes permanent
  residents. [SOURCE: Clemens–Lewis Tables 2–5; Amuedo-Dorantes et al.]
- **Where crowd-out is real.** Immigrant inflows push natives out of immigrant-intensive
  nontradable occupations (housekeeping against firefighting) and not out of tradable ones;
  this is reallocation across jobs inside a region, and the same model says halving Latin
  American immigration lowers low-education native real wages in every commuting zone.
  [SOURCE: Burstein et al. Table I, Fig. 2]

The account's FAQ 11 says the headline is not a removal saving. These four are the evidence
for the employment leg of that sentence. They are also the place to say plainly what the
account does not carry: the output lost when the workers go.

### 3.3 Housing: a demand shock now, a construction channel later

- 2021–24 unauthorized inflows of 1% of local employment raised house prices 2.2% (0.7) and
  rents 1.4% (0.3) with permits flat, on transaction indices; CoreLogic and Freddie Mac
  price effects are about 1% and insignificant and self-reported ACS values show nothing.
  [SOURCE: Wilson–Zhou Tables 6, B4, B5]
- The 1995 inflow raised the rental gap about 1% per 1% of population within a year and the
  effect was gone by 1998; over 1990–2000 rents and house prices in high-inflow places fell
  with elasticities near −1, through Mexican entry into construction and native construction
  wages −0.45 to −0.77. [SOURCE: Monras Tables 6, 7, 10, D10]
- Piyapromdee's model gives 0.84 to 1.24% rent per 1% population and a mean inverse housing
  supply elasticity of 0.68 across 114 metros, the same Saiz and Gyourko inputs the
  California–Texas memo used (ladder 180).

The two US papers disagree in sign because they measure different horizons: three years
against a decade. That is the frame for the housing section, and the reason the memo on
supply rates (ladder 180) needs a causal leg at the decade horizon before it can say
anything about rents. Monras's design, a push factor interacted with settlement networks over
1990–2000, is the template for his construction channel, and the IPUMS panel covers those
years; the peso crisis is the one identified Mexican push shock in the data and cannot be
reused for later decades. The 2000–2010 decade is now measured with the ancestry instrument
(ladder 183): rents +1.4% (SE 1.4) and values +11.6% (2.9) per point of foreign-born share,
with no extra effect in supply-inelastic metros, so at ten years the demand side dominates
and the construction-cost offset, if present, is not large enough to show.

### 3.4 Who gains from selection

Piyapromdee's skill-selective counterfactual is the cleanest distributional statement in the
set: adding 3.6 million high-skill immigrants raises low-skill natives' welfare about 1% and
lowers high-skill natives' about 3% in gateway cities, with incumbent high-skill immigrants
losing 8.6%; the national average is −0.8% until rental income is counted, then +$94 a
head, so the sign of "immigration helps natives" depends on who owns the housing. Lin–Weiss's
top-end gains (+15% at the 90th percentile per 10 points of high-skill immigrant share) are
the association-design version of the same split. Together with §3.1 they say the
distribution of gains and losses runs by skill, tenure and asset ownership more than by
nativity, which is the account's finding about the beneficiary set read from the other side.

### 3.5 The remedy's footprint on citizen children

Local 287(g) partnerships cut Hispanic K–12 enrollment 10% within two years, in grades K–5,
with no change for non-Hispanic pupils, and most of those children are US citizens (79% by
the authors' count). This belongs with §3.2 as a cost of enforcement that the account does
not price, with its weakness stated: under enrollment weighting the non-Hispanic placebo
also moves.

## 4. Method only

Clemens–Hunt (small-cell composition breaks) and Llull (OLS attenuation of two to three
times in cell designs) are instruments for reading other papers. The repo already applies
both cautions (the 2010→2011 BJS restatement trap, the CPS cell sizes in the second-generation
work); they add no result.

## 5. Limits and selection [FRAMING-SENSITIVE]

The fourteen were chosen by whoever built the acquisition list, and eleven of them find
native effects between benign and positive. The set lacks the papers that find otherwise
(Borjas 2003 and 2017, Dustmann–Schönberg–Stuhler on Germany, Edo on France, Amior–Manning
on monopsony), so §3 is a reading of what was read, not a survey. The account's own
disconfirmation for §2.1 is the Clemens–Lewis interval, which does include values near 1;
the reason it is given less weight is its object and population, stated in the table, not
its direction. Every estimate in §3 is short-horizon, local or firm-level, and none carries a
tax, service or schooling line; the account remains the only stationary object in the repo.

## 6. What the two data packages can do

- **Bracero replication package** (`harvard-dataverse/bracero-aer-2018/files/`, Stata data
  and do-file, 5.0 MB): reproduces Tables 1–2, which is where the confidence intervals in
  §3.2 come from. Worth running only if the essay quotes the exclusion bound; the reader's
  arithmetic on the printed standard errors already gives it.
- **Ancestry instruments** (`immigrationshock/ancestry-instruments/`, county 131 MB and DMA
  8.8 MB): Wilson–Zhou's rejected instrument (§2.3). Usable as a second instrument for the
  2000–2010 displacement window, not for 2021–24 and not to reproduce their headline.

## 7. Executions this reading proposes

1. Done the same evening: ε = 8.7, 9 and 17.9 rows added to `production_nativity_nest_2026_09_22`
   (its RESULT.md carries the rows and the gate record).
2. Done the same evening: `ancestry_instrument_2026_09_22`, §2.3.
3. Done the same evening, on 2000–2010 rather than 1990–2000 because ladder 182 gave that
   decade a clean instrument: `housing_causal_2000_2010_2026_09_22` (ladder 183), rents
   +1.4% (1.4) and values +11.6% (2.9) per point of foreign-born share, no inelastic-metro
   amplification. Monras's 1990–2000 design remains the way to test his construction channel.

## Revisions

- 2026-09-22 (evening): §2.1 and the verdict now quote computed nest rows at ε = 8.7, 9
  and 17.9 instead of interpolating between 7 and 20; the headline move is $2–5bn. Ladder
  181 and the nest memo carry the same revision. No claim changes direction.
- 2026-09-22 (evening): §2.3 now reports the executed second-instrument run (ladder 182)
  instead of proposing it; the displacement lane's public-assistance result is the one
  claim in the repo this reading changes, from a negative estimate to a null.
- 2026-09-22 (evening): §3.3 and §7 record the executed 2000–2010 housing leg (ladder 183).
