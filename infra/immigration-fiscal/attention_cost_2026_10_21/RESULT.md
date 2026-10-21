claude-opus-5-5

# Attention, legal and agenda cost of immigration as a political issue (2024)

**Verdict:** What each component measures, its size, and what it holds fixed. $bn per year, 2024. [CALCULATION: attention_cost.py → derived/attention_cost.csv; displacement.py → derived/displacement.csv]

| Component | What it measures | Size | Holds fixed / leaves out | Mexican-attributable (6% / **30%** / 44%) |
|---|---|---|---|---|
| A. Private dollars | I-9 and E-Verify paperwork hours at the ICR loaded wage; immigration legal-services revenue; advocacy spending | **11.1** gross: paperwork 1.53, legal ≈9.3 [UNVERIFIED industry model], advocacy ≈0.30; fight-specific part (paperwork + advocacy) ≈1.8 | Gross resource use. It does not net out screening employers would do anyway or donors' alternative causes. Lobbying is not separable by issue. Public enforcement is excluded (already in the main case) | 0.6 / **3.3** / 4.9 |
| B. Attention | Adult news-hours × immigration's cable mention-clip share × value of time | **1.5–5.3bn hours**; 31.7–111.6 at $21.10/h (USDOT non-work value); 52.7–185.4 at $35.06/h (wage) | The hours would otherwise go to something non-news; no consumption or information value. Social-media argument and rumination are left out. The net of substitution between issues is **not identified** | central share, mid reading: 20.1–33.4 (all-arm span 1.8–81.2) |
| C. Agenda | Immigration's share of bills and laws; displacement of housing and family shares | 3.5% of 118th-Congress bills (565/16,213), 1.1% of laws (3/269). Displacement beyond share arithmetic: none detected in 16 US regressions (excess t within ±1.5); NL family +0.14 (SE 0.055), not robust to lag | Topic shares only, not priced; quadratic trend; NW(2) | — |
| D. Policy-quality channel | Identified link from immigration or its salience to policy and then to output | not priced; no 2023–2026 study identifies it | — | — |

[INFERENCE] A counts resources spent; most of it (legal services) is the cost of running admissions, and the cost tied to the political fight is about $1.8bn. B is a gross time count. Its welfare value depends on a substitution rule that no source here identifies; the measured evidence (stable total news time, a shifting topic mix) is consistent with substitution between topics. C measures agenda shares. Its displacement test can rule out large crowding-out of housing in US hearings but cannot resolve small effects. [FRAMING-SENSITIVE: value of time, substitution rule, attribution rule]

## Load-bearing inputs: exact source passages

- **Allen et al. 2020 (63.7 min/day)**, Sci. Adv. 6:eaay3539. The text reads: "Overall, the ratio of TV to online news—including both desktop and mobile devices—is more than five to one (54 min versus 9.7 min)". The 54 + 9.7 = 63.7 used here is that sentence's two figures. Context passage: "Of the 460 min per person per day of total media consumption, approximately 400 min (86%) is not related to news of any kind". The two passages do not reconcile exactly (460 − 400 = 60 vs 63.7, "approximately"). [SOURCE: https://www.science.org/doi/10.1126/sciadv.aay3539]
- **GDELT mention shares.** GDELT's definition: "The total monitored airtime of each station in a given day/hour is broken into 15 second intervals and the timeline reports the percent of those 15 second clips that matched your search. A single mention of your keyword in a given 15 second interval will count as the entire 15 second interval". Example cell, `inputs/gdelt_tv_immigration_narrow_2024.csv`: `2024-01-03,CNN,4.0858`. The shares used are daily means over 2024-01-01..2024-10-10 per station (narrow: CNN 1.02, Fox 2.25, MSNBC 1.07%), computed in attention_cost.py. [SOURCE: https://api.gdeltproject.org/api/v2/summary/summary?d=iatv] [DATA: inputs/gdelt_tv_*.csv]
- **IBISWorld legal services.** Research and Markets' listing of the IBISWorld report: "revenue for immigration lawyers and attorneys is expected to soar at a CAGR of 5.3% during the current period, reaching $8.7 billion in 2023". IBISWorld's own page: "The market size of the Immigration Lawyers & Attorneys industry in the United States is $10.6bn in 2026." The $9.29bn for 2024 is the geometric interpolation between the two. Both are vendor estimates of an unpublished model. [SOURCE: https://www.researchandmarkets.com/reports/2764260/immigration_lawyers_and_attorneys_in_the_us] [SOURCE: https://www.ibisworld.com/united-states/industry/immigration-lawyers-attorneys/4808/]

Instrument note: this analysis was produced by an LLM, and its framing of a politically charged issue may lean the way post-training leans (notes/llm-bias-caveat.md). Every number is anchored to a cited primary table, and the choices that move the result are shown as ranges.

Lane: `infra/immigration-fiscal/attention_cost_2026_10_21/`. Scripts:
- `fetch_gdelt_tv.py`: GDELT TV pulls → `inputs/`
- `count_bills.py`: GovInfo BILLSTATUS → `derived/bills_policy_area_118.csv`
- `displacement.py`: CAP downloads → `_cache/`, output `derived/displacement.csv`
- `attention_cost.py`: arithmetic → `derived/attention_cost.csv`

**EOL flag:** `inputs/cbp_sbo_encounters_fy23_fy26_aug.csv` is CBP's raw CRLF download and needs a `-text` line in `.gitattributes` before commit.

## Order of work and pre-registration status

The no-anchor instruction (operator 14:37 JST, relayed after the first pass had finished) asked for each method to be pre-registered before its magnitude was looked up. That held for one test only:
- **C-displacement** was pre-registered in Append 2 (14:55 JST), before any CAP data was fetched. Its results are in Append 3.
- **A, B, C-shares and E** were fixed and run in the first pass (14:37–14:52 JST), so their magnitudes were seen before this instruction arrived. Their method notes below record the methods as run; they are not blind pre-registrations.
- The first pass also scaled every figure against a benchmark. That framing and the benchmark rows were removed at 14:57 JST (see Log). No component's method or input was changed when the framing was removed.

## Methods (as run; C-displacement as pre-registered)

- **A, private dollars.**
  - Sources: OIRA paperwork estimates for the I-9 and E-Verify forms, valued at the ICR's own loaded wage; IBISWorld legal-services revenue (graded low); NCRP/Candid foundation grants to the pro-immigrant movement; restrictionist groups' 990 expenses.
  - Public enforcement is excluded because the main case already charges it per head (FAQ 12).
  - Substitution rule: report gross, and name what each item replaces where a source says so.
- **B, attention.**
  - Hours = adults (ACS 2024) × news minutes per day (Allen et al. 2020) × immigration's share of news.
  - The share is GDELT's cable mention-clip share for 2024 (narrow terms; terms with "border"; Fox with "border"). Gallup MIP measures salience, not airtime, and is not used for hours.
  - Value of time: USDOT non-work value as central, the average wage as an alternative.
  - Substitution rule: the gross figure assumes the hours would otherwise go to something other than news. The net needs evidence on total news time, and is reported as unidentified if none is found.
- **C-shares.** Congress.gov policy area of every H.R. and S. bill in the 118th Congress, counted for introduced bills and enacted laws.
- **C-displacement.** Pre-registered in Append 2: CAP topic shares by year; immigration = major 9, housing = major 14, family = subtopics 1302/1308/1208; quadratic trend; Newey–West(2); three robustness checks; mechanical benchmark −mean(share_k)/(1 − mean(imm)).
- **D.** Bounded search of 2023–2026 work for an identified link from immigration or its salience to policy and then to output; Brexit as a calibration case.
- **E.** Attribute by the Mexican share of the unauthorized population: low = share of the 2021–23 increase, central = 2023 stock (Pew), high = 2022 stock (DHS), with CBP FY2024 encounters as a check. Lineage size is rejected as a key because the fight is about the unauthorized and the border, not settled citizens.

## A. Private dollars: findings

- Paperwork: I-9 33,207,976 h/yr (ICR 202401-1615-009) × $43.45 = **$1.44bn**; E-Verify 1,966,051 h × $43.45 + $1.887M = **$0.09bn**. The I-9 covers every hire in the country. *Large-burden reading:* OIRA hour estimates are notoriously low for small employers, and E-Verify's tentative non-confirmations cost workers time that is not counted. *Small-burden reading:* the hours include identity-document checks that payroll (W-4/SSN) and background screening would partly do anyway, so the incremental burden is below $1.5bn. Neither adjustment is measured.
- Legal services: **≈$9.3bn** (IBISWorld $8.7bn 2023 → $10.6bn 2026, geometric interpolation; proprietary model, method unpublished). Most of it is visa, green-card, naturalization and employer-petition casework, the transaction cost of running an admissions system. Only the removal-defense and litigation part is tied to the political fight. [GAP: EOIR representation counts × fees would split it]
- Advocacy: pro-immigrant foundation grants **$0.28bn/yr** (2016–20 average, NCRP from Candid); FAIR + NumbersUSA (both entities) + CIS functional expenses **$18.6M** (TY2023, ProPublica 990 API). Donors' alternative is mostly other causes, so the net social cost of advocacy spending is the difference in value between causes, which is unidentified and could be either sign.
- Lobbying: LDA dollars cannot be split by issue, and OpenSecrets' client count renders by JS. [GAP]

## B. Attention: findings

- 267.18M adults × 63.7 min/day (Nielsen 2016–18: TV news 54 + online 9.7) = **103.5bn news-hours/yr**.
- Immigration's mention-clip share of cable airtime, 1 Jan–10 Oct 2024: **1.45%** (narrow, three-station mean), **3.07%** (with "border"), **5.11%** (Fox with "border") → **1.50 / 3.18 / 5.29bn hours**. [DATA: inputs/gdelt_tv_*.csv]
- Valued at $21.10/h: **$31.7 / 67.0 / 111.6bn**; at $35.06/h: **$52.7 / 111.4 / 185.4bn** (gross).
- Measurement direction:
  - Applying a cable share to all news (network, local, online) probably overstates it.
  - A one-word clip match marks the whole 15-second clip, which inflates the count; unmatched clips inside an immigration segment deflate it. The net direction is unknown.
  - The definition of news is broad (morning shows, entertainment news), which inflates the hours.
  - Social-media posting, conversation and rumination are outside Allen's measure, which deflates the hours.
- **The case for a large hidden burden.**
  - Salience was extreme: immigration was Gallup's top problem for three straight months, at 20–28% of adults (Jan–Apr 2024).
  - The Migration Fear Index ran 1.7–2.4× its 1995–2011 mean through 2024 (and 3.6× in 2025 Q2).
  - Pew: 62% were worn out by campaign coverage (April 2024).
  - For high-opportunity-cost people, an hour of political attention can displace work or study worth far more than $35. The average-wage value does not capture that tail.
  - Distress and polarization are costs of the content itself, beyond the time.
- **The case that the net is near zero.**
  - Total media and news time was "relatively stable" over 36 months in Allen et al. Cable airtime is fixed by construction, and from 2022 to 2024 immigration's share rose while inflation/prices and Ukraine fell (Append 1). Topics substitute within a fixed news budget.
  - People choose news as consumption, partly for its value as information on a real policy question. Valuing chosen leisure at the full value of time counts it as a pure loss, and immigration coverage may displace lower-value content. The net can be negative.
- **Net reading: not identified.** A design that would identify it (total news minutes around an issue-salience shock, e.g. Nielsen around the 2019 and 2024 border surges) was not found. [GAP]

## C. Agenda: findings

- Shares: 565 of 16,213 H.R./S. bills (3.5%, 12th of 33 policy areas) and 3 of 269 enacted bills (1.1%), 118th Congress. [DATA: derived/bills_policy_area_118.csv] Immigration provisions also ride in appropriations and NDAA bills (CRS R47901), so this is a floor.
- Displacement: results in Append 3, the specification in Append 2. In brief:
  - **US hearings and US laws, 1946–2022:** no coefficient on housing or family differs from the mechanical benchmark (|excess t| ≤ 1.5 in all 16 regressions). The US-hearings precision rules out large displacement. A 1-SD rise in immigration's hearing share (0.45 pp) lowers housing's share by at most ~0.19 pp (95% bound), about 10% of housing's 1.9% mean. It cannot tell arithmetic-scale displacement (−0.009 pp per SD) from zero.
  - **Netherlands parliamentary questions, 1945–2024:** family policy rises with immigration (levels b = +0.14, SE 0.055; first differences +0.21, SE 0.052). That is crowding-in, the opposite of displacement. It vanishes with a one-year lag (−0.02, SE 0.057), and family questions average under one a year, so it is fragile. Housing shows nothing (|t| < 1).
  - **UK:** excluded by the pre-registered rule; the PMQs series covers only 1997–2008 (12 years).

## D. Policy-quality channel: literature refresh 2023–2026

Nothing new clears the bar of an identified estimate linking immigration (or its salience) to policy outcomes and then to output in the US. Ladder 102's withdrawal stands, and the withdrawn chain is not recomposed.

- Basso, Mathur & Peri 2026 (NBER w35523): immigration from non-OECD countries predicts faster GDP-per-worker growth, through investment (OECD local projections 1990–2024). This is the direct channel, with no political link. [SOURCE: https://www.nber.org/papers/w35523]
- Böhmelt & Ezrow 2023 (JEPP): when populist governments make immigration salient, they enact fewer immigration policies. [SOURCE: https://doi.org/10.1080/13501763.2023.2255658]
- Berger 2025: radical-right parties' indirect effect on immigration legislation is "not a pivotal element" (11 West European countries, 1985–2017). [SOURCE: https://doi.org/10.3389/fpos.2025.1529840]
- Alrababa'h, Beerli, Hangartner & Ward 2024: the Swiss border opening raised anti-immigrant votes by 6 pp (29%) with no economic or perceived-threat effect, which they attribute to elite framing. The vote effect is identified; any output effect is not estimated. [SOURCE: https://doi.org/10.31235/osf.io/hgczq]
- Docquier & Rapoport 2025 is a theory paper with no output estimate. Hangartner & Spirig 2024 say the political channel could exceed the direct channels, but that the evidence is scarce.
- **Brexit calibration.** The UK case shows how large such a channel can be, and why it does not transfer.
  - Bloom et al. (NBER w34459, rev. June 2026): UK GDP 6–8% lower by end-2025. One named mechanism is management time diverted to Brexit preparation, which is attention diversion measured at firms.
  - CER synthetic control: −5.2% by 2021 Q4.
  - Ashcroft poll: 33% of Leave voters gave immigration control as their main reason.
  - Becker, Fetzer & Novy 2017: EU-immigration exposure explains little of the district vote.
  - Immigration's share of Brexit's cost is therefore unidentified.
- [FRAMING-SENSITIVE] The 2025 enforcement drive's output costs are a policy response. Whether to charge them to the immigrants or to the policy is a framing choice, so they are not priced.

## E. Attribution: findings

- Shares of the unauthorized population: Pew 2023 30% (4.3M of 14.0M); DHS OHSS Jan 2022 43.8% (4.81M of 10.99M); Mexico's share of the 2021–23 increase 5.7% (Pew: non-Mexican 6.4M → 9.7M on a +3.5M total).
- CBP FY2024 southwest-border encounters: 30.6% Mexican (653,684 of 2,135,005), consistent with the central.
- The 2024 salience peak followed a surge that was about 94% non-Mexican, which argues for the low arm in any counterfactual where the Mexican-origin lineage is absent but the surge is not.
- Disconfirmation of population-scaled keys: salience is partisan, not proportional to exposure (Gallup April 2024: 48% of Republicans vs 8% of Democrats). The repo's county panel finds the within-state county gradient of Mexican-origin share on the vote is −0.02 pp per point (95% CI −0.31 to +0.27). [SOURCE: research/immigration-political-trajectory-county-panel-2026-09-19.md]

## Sources

I-9: reginfo.gov ICR 202401-1615-009; supporting statement omb.report/icr/202307-1615-002. E-Verify: 88 FR 42091. Legal: IBISWorld 4808 / Research&Markets 2764260 (low grade). Advocacy: NCRP "A Ripple, Not a Wave" (2022); ProPublica Nonprofit Explorer API, EINs 521136126, 470865418, 470865426, 521449368. Salience: Gallup 2024-02-27, 2024-03-29, 2024-04-30; Chicago Council 2024; Pew 2024-05-28 and 2024-10-10; FRED USEPUFEARINDX. Airtime: GDELT TV API v2. News time: Allen et al. 2020, Sci. Adv. 6:eaay3539. Adults: ACS 2024 S0101. Value of time: USDOT BCA Guidance 2025, Table A-2 (quoted via two grant BCAs; [GAP] primary PDF). Wage: BLS CES0500000003. Attribution: DHS OHSS 2024 report, Table 2; Pew 2025-08-21; CBP sbo-encounters-fy23-fy26-aug.csv. Agenda: GovInfo BILLSTATUS 118 hr/s; CRS R47901; CAP US Hearings 21.7, US Public Laws 20.1, NL questions 3QS03102024 (minio.la.utexas.edu/compagendas). D: as cited inline.

## Remaining gaps and next queries

- [GAP] Topic-time share across network, local and online news (Media Cloud; GDELT segment windows).
- [GAP] Net-of-substitution identification (Nielsen total news minutes around border surges).
- [GAP] Split of legal services into removal defense vs admissions (EOIR representation × fee schedules).
- [GAP] LDA immigration client count (Senate LDA API, issue code IMM).
- [GAP] H-2A/H-2B employer program costs (DOL ICRs).
- [GAP] DOT Table A-2 personal-only value, from the primary PDF.
- [GAP] A second European CAP agenda series (Denmark's page linked no files; Spain's oral questions are untested).
- D sweep was bounded (Exa, 8 hits screened). A scite forward-citation pass from Funke–Schularick–Trebesch 2023 would close it.

## Log
- 2026-10-21 14:37 JST stub.
- 2026-10-21 14:52 JST first pass: components A–F complete; verdict written.
- 2026-10-21 14:55 JST operator correction received (no anchor, estimate blind, pre-register; C adds displacement). C-displacement pre-registration written (Append 2) before CAP data was fetched.
- 2026-10-21 14:57 JST **removed**: component F, the GDP benchmark and the comparison with another lane's result. Removed from attention_cost.py (constants and `F`/`pct_gdp` rows), from derived/attention_cost.csv (rerun), from the verdict table, and from Append 1 (its first bullet). The first-pass message to the team lead used that framing and is superseded by this file. No other number changed.
- 2026-10-21 14:58 JST displacement.py run; results appended (Append 3); RESULT rewritten in this order.
- 2026-10-21 15:00 JST Verdict and [INFERENCE] line rewritten as descriptive only (what each component measures, size, what it holds fixed). Exact source passages added for Allen et al., GDELT and IBISWorld. `-text` added to .gitattributes for the CBP CSV. Component F and every benchmark reference confirmed absent from RESULT, code and CSV.

## Append 1: first-pass anchors (14:37–14:52 JST; benchmark bullet removed 14:57)

- **I-9 burden** (OMB 1615-0047, ICR 202401-1615-009, approved 2024-05-14): **33,207,976 hours/yr**, cost burden $0. The prior ICR's supporting statement values hours at $43.45 (May 2022 BLS all-occupation mean $29.76 × 1.46 benefits). [SOURCE: https://www.reginfo.gov/public/do/PRAViewICR?ref_nbr=202401-1615-009] [SOURCE: https://omb.report/icr/202307-1615-002/doc/133853301.pdf]
- **Immigration legal services**: IBISWorld $8.7bn revenue 2023, $10.6bn 2026, 18,417 businesses. Grade: proprietary model, [UNVERIFIED] order of magnitude only. [SOURCE: https://www.researchandmarkets.com/reports/2764260 ; https://www.ibisworld.com/united-states/industry/immigration-lawyers-attorneys/4808/]
- **Public enforcement already in the account** (FAQ 12, per head inside public order and safety).
- **Salience**: Gallup MIP immigration 20 / 28 / 28 / 27% Jan–Apr 2024; 48% R vs 8% D (April). [SOURCE: https://news.gallup.com/poll/644570/immigration-named-top-problem-third-straight-month.aspx] Chicago Council: 21% follow immigration news very closely vs 29% economy. [SOURCE: https://globalaffairs.org/research/public-opinion-survey/domestic-issues-overshadow-foreign-conflicts-2024-voting-decisions]
- **Cable airtime mention share** (GDELT TV, CNN/Fox/MSNBC, 1 Jan–10 Oct 2024):
  - Immigration, narrow terms: 1.02 / 2.25 / 1.07%; with "border": 2.17 / 5.09 / 1.91%.
  - 2024 comparators: inflation/prices 0.73 / 1.28 / 0.55; abortion 0.70 / 0.37 / 1.30; Ukraine 1.21 / 0.69 / 1.05; Mexico 0.33 / 0.43 / 0.18.
  - 2022 narrow immigration: 0.57 / 1.59 / 0.47; inflation/prices: 1.60 / 3.24 / 1.27; Ukraine (CNN): 5.19.
  - [DATA: inputs/gdelt_tv_*.csv]
- **Migration Fear Index (US newspapers)**: 2024 quarters 182.8 / 172.7 / 212.5 / 236.2 (1995–2011 mean = 100); 2025 Q2 359.0. [SOURCE: https://fred.stlouisfed.org/data/USEPUFEARINDX]
- **Mexican share of unauthorized** (DHS OHSS, Jan 2022): 4.81M of 10.99M = 43.8%. [SOURCE: OHSS 2024 report, Table 2]
- **Value of time**: USDOT BCA Guidance 2025, Table A-2, all purposes $21.10 per person-hour (2023 $). [SOURCE: quoted in two grant BCAs]

## Append 2 — 2026-10-21 14:55 JST: pre-registration of C-displacement (written before any CAP data was fetched or viewed)

Question: in years where immigration takes a larger share of the legislative agenda, do housing and family-policy shares fall by more than share arithmetic alone implies, beyond trend?
- Data: Comparative Agendas Project (CAP) US Congressional Hearings, calendar-year counts by major/subtopic; robustness on CAP US Public Laws if available. Europe: the first one or two CAP country datasets with a parliamentary-agenda series (bills, questions or hearings) and an immigration code covering at least 30 years.
- Topic codes (CAP master codebook): immigration = major 9; housing = major 14; family policy = subtopics 1302 (low-income family assistance), 1308 (child care) and 1208 (family issues).
- Outcome: share_k(t) = items in topic k / all items in year t. Regressor: immigration share(t).
- Main specification: share_k(t) = a + b·imm(t) + c1·t + c2·t² + e, OLS, Newey–West SE with 2 lags.
- Robustness: (i) first differences, Δshare_k on Δimm, NW(2); (ii) the regressor lagged one year, imm(t−1); (iii) adding log total items.
- Mechanical benchmark: shares sum to 1, so if immigration displaced every other topic in proportion, b_k = −mean(share_k)/(1 − mean(imm)). Report b, its SE, the benchmark and the excess (b − benchmark). Displacement beyond arithmetic means the excess is negative.
- Power rule: with fewer than ~40 annual observations, or an immigration share with little variation, say so and treat the result as uninformative.
- Report every coefficient, whatever its sign.

## Append 3 — 2026-10-21 14:59 JST: C-displacement results (spec exactly as Append 2)

[DATA: derived/displacement.csv] b = coefficient on immigration share; benchmark = proportional-displacement arithmetic; excess = b − benchmark (negative = displacement beyond arithmetic). NW(2) SE.

| dataset | topic | spec | n | b | SE | benchmark | excess t |
|---|---|---|---|---|---|---|---|
| us_hearings | housing | levels_quadtrend | 75 | -0.1415 | 0.1405 | -0.0192 | -0.87 |
| us_hearings | housing | first_diff | 74 | -0.0029 | 0.2880 | -0.0192 | 0.06 |
| us_hearings | housing | lag1_quadtrend | 74 | -0.0403 | 0.3252 | -0.0192 | -0.06 |
| us_hearings | housing | levels_quadtrend_logtotal | 75 | -0.2113 | 0.1551 | -0.0192 | -1.24 |
| us_hearings | family | levels_quadtrend | 75 | 0.0387 | 0.1190 | -0.0060 | 0.38 |
| us_hearings | family | first_diff | 74 | 0.0724 | 0.1176 | -0.0060 | 0.67 |
| us_hearings | family | lag1_quadtrend | 74 | -0.0133 | 0.0879 | -0.0060 | -0.08 |
| us_hearings | family | levels_quadtrend_logtotal | 75 | 0.0231 | 0.1221 | -0.0060 | 0.24 |
| us_public_laws | housing | levels_quadtrend | 75 | -0.1098 | 0.0908 | -0.0122 | -1.07 |
| us_public_laws | housing | first_diff | 74 | -0.1749 | 0.1408 | -0.0122 | -1.16 |
| us_public_laws | housing | lag1_quadtrend | 74 | 0.1105 | 0.1252 | -0.0122 | 0.98 |
| us_public_laws | housing | levels_quadtrend_logtotal | 75 | -0.1186 | 0.0916 | -0.0122 | -1.16 |
| us_public_laws | family | levels_quadtrend | 75 | -0.0260 | 0.1040 | -0.0069 | -0.18 |
| us_public_laws | family | first_diff | 74 | 0.1264 | 0.0897 | -0.0069 | 1.49 |
| us_public_laws | family | lag1_quadtrend | 74 | -0.0377 | 0.1107 | -0.0069 | -0.28 |
| us_public_laws | family | levels_quadtrend_logtotal | 75 | -0.0277 | 0.1035 | -0.0069 | -0.20 |
| nl_questions | housing | levels_quadtrend | 80 | 0.0148 | 0.1178 | -0.0384 | 0.45 |
| nl_questions | housing | first_diff | 79 | -0.0241 | 0.1331 | -0.0384 | 0.11 |
| nl_questions | housing | lag1_quadtrend | 79 | 0.0403 | 0.1507 | -0.0384 | 0.52 |
| nl_questions | housing | levels_quadtrend_logtotal | 80 | 0.0728 | 0.1283 | -0.0384 | 0.87 |
| nl_questions | family | levels_quadtrend | 80 | 0.1373 | 0.0553 | -0.0065 | 2.60 |
| nl_questions | family | first_diff | 79 | 0.2131 | 0.0520 | -0.0065 | 4.22 |
| nl_questions | family | lag1_quadtrend | 79 | -0.0236 | 0.0566 | -0.0065 | -0.30 |
| nl_questions | family | levels_quadtrend_logtotal | 80 | 0.1202 | 0.0592 | -0.0065 | 2.14 |

Power: 74–80 annual observations each (above the 40 floor), but immigration's share moves little (SD 0.45 pp US hearings, 0.77 pp US laws, 1.97 pp NL questions), so the SEs (0.05–0.33) are 3–20× the mechanical benchmarks. The test can rule out large displacement, not arithmetic-scale displacement. Family-policy counts are small (US laws ≈2/yr, NL questions <1/yr).

## Reproduce

`fetch_gdelt_tv.py` re-downloads the GDELT TV inputs (network; pinned copies are in `inputs/`). `count_bills.py` and
`displacement.py` read the Congress.gov BILLSTATUS and Comparative Agendas downloads in the ignored `_cache/`.

```sh
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/attention_cost_2026_10_21 \
  "uv run --no-project python3 {lane}/count_bills.py" "uv run --no-project python3 {lane}/displacement.py" \
  "uv run --no-project python3 {lane}/attention_cost.py" --allow-unrun infra/immigration-fiscal/attention_cost_2026_10_21/fetch_gdelt_tv.py
```
