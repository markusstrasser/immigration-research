claude-opus-5-5

**Verdict:** (written 2026-10-21 15:33:36 JST after all components; 2024 USD per year)
- **A private dollars ≈ $10–17bn deadweight-type (A1 + A2 + A3 allocated), central ≈ $12.7bn**, of which nearly all is running the legal
  system, not fighting over it:
  - A1 employer I-9/E-Verify compliance **$1.5–1.95bn** (37.6–41.2M h; reginfo ICR inventory; a floor).
  - A2 admissions/removal casework **$8–14bn, central $10bn** (private immigration bar ≈ $7bn [4.5–11] + applicant
    paperwork 64.7M h = $1.3–3.1bn). USCIS fees **$6.22bn** (FY2024) are reported beside, as a transfer that pays for a
    public service; with them, the outlay is $17–24bn.
  - A3 political fight: gross **$1.2–2.6bn** (TV ads mentioning immigration $0.9–1.3bn, whole lobbying filings ≤$0.94bn,
    advocacy $0.15–0.4bn), allocated **$0.6–1.1bn**, net of substitution **$0.15–0.4bn** (advocacy groups only).
  - Excluded and named: CBP, ICE, EOIR, USCIS above fees, state border operations.
- **B time:** gross **1.6–13.0bn person-hours, central 5.2bn (≈20 h per adult)**, valued at **$32–364bn, central
  $104bn (DOT non-work value $19.96/h) to $146bn (after-tax wage $28.05/h)**. The share inputs are GDELT 2024 cable
  keyword shares of 1.9% (narrow) and 3.9% (broad), scaled to topic time. Net of substitution: **≈ $0, with an
  unidentified upper bound of ~$30bn**. Total news time is stable and the news hole is fixed, so immigration minutes
  mostly displace other news.
- **E Mexican-origin (Mexican-born) share:** stock rule **23%**, unauthorized rule **37–45%**, caseload rule **13–15%**
  for casework and **4%** for I-9. Explicit on-air co-mention is **2–4%** (Venezuela/Haiti outrank Mexico in 2024
  immigration coverage). Central A ≈ $12.7bn → $2.9bn (R1); $2.4bn (R3 casework $2.0 + R3 I-9 $0.08 + R2 fight $0.35); $3.1bn (R2 on compliance, removal and fight + R3 benefits). Central B gross $104–146bn →
  $24–34bn (R1), $43–60bn (R2), $3–4bn (R3 explicit).
- Weakest inputs: total news minutes (2016–18 metered, not 2024), the clip-to-topic factor (×1.5–3, assumed),
  lobbying dollars (secondary aggregators; LDA API blocked), legal-services revenue (headcount × revenue per head).

# Blind estimate: annual US cost of immigration as a political and legal issue, 2024

Scope: (A) private dollars, (B) adult time on immigration news and debate, (E) Mexican-origin share.
Blinding: no file under the repo's attention_cost lane, world ledger, FAQ, INDEX, ladder, decisions/,
.brainstorm/ or memory/session notes was opened; no repo grep on these topics. I also did not open my own
agent-memory routing note on this topic (`immigration-attention-cost-routes-2026-10.md`), since it may carry
magnitudes. Web and published datasets only.

## 0. Pre-registration (written 2026-10-21 15:08:27 JST, before any magnitude was looked up)

### A. Private dollars
Three separated blocks; unit is 2024 USD/yr.

- **A1 Employer compliance (legal-regime cost, neither admissions nor political fight).** Sources: reginfo.gov
  ICR records for Form I-9 (OMB 1615-0047) and E-Verify (OMB 1615-0092): annual burden hours, annual cost
  burden, respondents. Value hours at (i) the wage the ICR itself uses, and (ii) BLS ECEC total compensation for
  the relevant occupation if the ICR uses something else. Include employee time on Section 1 if the ICR counts it.
- **A2 Running admissions (casework).** Sources: USCIS ICR burden for the high-volume forms (I-130, I-485, I-765,
  N-400, I-129/I-140, I-90, I-131, I-821D), USCIS fee receipts (CJ / fee rule), private immigration legal
  services (Census Economic Census/SAS has no immigration-law code, so use count of immigration lawyers × billings
  from BLS/AILA or an industry revenue figure, flagged secondary), and employer sponsorship costs (PERM/H-1B legal
  fees). Fees paid to USCIS are a private outlay that funds a public service: report them but mark them as a
  transfer that pays for admissions, not deadweight.
- **A3 Political fight.** Sources: Senate LDA API (filings listing issue code IMM, 2024), allocation rule:
  (low) report amount ÷ number of issue codes on the report, (high) full report amount; OpenSecrets issue totals
  as a cross-check. Advocacy nonprofits: IRS 990 expenses (ProPublica Nonprofit Explorer API) for the main
  immigration-focused organizations on both sides (restrictionist and expansionist), plus a NTEE-based aggregate
  if reachable. Political ads mentioning immigration in 2024 (AdImpact or Wesleyan Media Project tallies).
  Litigation by private parties against federal policy: counted inside the advocacy budgets.
- **Excluded and named:** public enforcement (CBP, ICE, EOIR, DOJ prosecutions, state border operations such as
  Operation Lone Star) and USCIS's own operating costs above fees.

### B. Time
- Unit: adult person-hours/yr, then USD/yr.
- Total news/political media time: ATUS (no news category; TV and reading only), Pew time-on-news estimates,
  Nielsen/Pew Research news-audience data; take a low and high per-adult minutes/day.
- Immigration's share of news: GDELT TV API (share of airtime on national cable/broadcast that mentions
  immigration terms in 2024), Media Cloud if reachable, Pew/Gallup issue salience (Gallup "most important
  problem" immigration share) as a demand-side cross-check.
- Adults: Census 2024 population 18+.
- **Time valuation, two rules:** (V1) USDOT value of travel time savings for personal travel (a published value
  of non-work time, 50% of median household hourly income), updated to 2024; (V2) the average after-tax hourly
  wage (BLS average hourly earnings, less an average tax rate).
- **Substitution:** gross = all immigration-news minutes. Net = minutes that would not have gone to other news or
  media in the absence of immigration as an issue. Evidence sought: whether total news time moves with immigration
  salience (agenda-setting crowd-out literature, fixed news hole). If no identification, net is reported as a bound
  with the point unidentified.
- Argue both: "large hidden burden" (gross, plus stress/attention costs) and "mostly substitution, near zero net".

### E. Mexican-origin share (rules fixed in advance)
- **R1 stock share:** Mexican-born share of the foreign-born population (ACS 2023/2024).
- **R2 unauthorized share:** Mexican share of the unauthorized population (Pew/MPI/CMS), applied to employer
  compliance (I-9/E-Verify exist to screen out unauthorized work) and to the political fight.
- **R3 caseload/attention share:** for admissions, Mexico's share of the relevant caseload (LPR admissions,
  naturalizations, H-2A/H-2B); for news time, the share of immigration coverage that mentions Mexico/the southern
  border (GDELT co-mention) or Mexican share of SW border encounters in FY2024.
- I report each rule; no rule is privileged as the headline.

## Findings log

### A1 Employer compliance — appended 2026-10-21 15:11:58 JST
Sources (parsed from reginfo.gov primary files, not a summary tool):
- Form I-9, ICR 202401-1615-009 (concluded 05/14/2024), inventory page: "Annual Number of Responses 151,327,900 …
  Annual Time Burden (Hours) 33,207,976 [previously approved 39,823,500] … Annual Cost Burden (Dollars) 0".
  Short statement: "decrease … due to the transfer of respondents from USCIS Form I-9 (OMB Control No. 1615-0047)
  to USCIS Form I-9NG (OMB Control No. 1615-NEW)". [SOURCE: https://www.reginfo.gov/public/do/PRAViewICR?ref_nbr=202401-1615-009]
- I-9 Supporting Statement A (docx, objectID 139141501), item 12 table: employers 62,063,950 responses × 0.35 h =
  21,722,383 h, $943,837,520; employees 62,063,950 × 0.15 h = 9,309,593 h, $404,501,794; record keepers 27,200,000 ×
  0.17 h = 4,624,000 h, $200,912,800; "Total … 35,655,976 … $1,549,252,114". Wage: "May 2022 Bureau of Labor
  Statistics average wage for All Occupations $29.76 times the wage rate benefit multiplier of 1.46 … equaling $43.45".
  Employer time includes "10 minutes – Completing audit with Immigration and Customs Enforcement agent".
  Item 14: federal cost $19,787,045 (132 ICE forensic auditors; public, excluded).
- E-Verify, ICR 202401-1615-010, Supporting Statement A (objectID 139154801): "Total … 13,470,505 … 1,966,051 [h] …
  $85,424,915" at the same $43.45; capital cost "$1,887,000" (2,550 firms × $740); "13,470,505 x $0.26 (estimated
  average cost per query), which equals $3,502,331".
- [GAP] I-9NG (1615-NEW) ICR not pulled; the transferred burden is bounded by the I-9 inventory drop (39.82M → 33.21M h)
  and the SS table total (35.66M h).

Computation [CALCULATION: hand, from the cells above]:
- Hours: I-9 35.66M (range 33.21–39.82M) + E-Verify 1.97M = **37.6M h (35.2–41.8M)**.
- Rule V-ICR (employer loaded wage, ICR's own rule, 2022 $): 37.6M × $43.45 = $1.63bn. Re-priced to 2024 by the BLS
  all-occupation mean wage growth 2022→2024 (≈+9.7%, see A1 note below) ≈ **$1.79bn**; plus E-Verify capital and
  query costs $5.4M. Range over the hour range: **$1.7–2.0bn**.
- Rule V-nonwork for the employee's 9.3M h only (DOT personal value ≈ $19/h, see B): employee share falls from
  $0.44bn to ≈$0.18bn, giving a low of ≈$1.5bn.
- Classification: this is the cost of the legal regime's work-authorization screening. It is neither admissions
  casework nor the political fight. It is a burden on every hire, citizens included (62M hires/yr).
- [INFERENCE] The ICR counts paperwork minutes only. It excludes I-9 software/vendor contracts, outside counsel for
  ICE Notice of Inspection audits, fines (transfers), and the hiring friction of tentative non-confirmations.
  Treat $1.7–2.0bn as a floor for A1.

#### A1 correction — 2026-10-21 15:16:53 JST
- Wage growth 2022→2024 is +8.7%, not ≈+9.7%: BLS CES average hourly earnings, total private (CES0500000003, BLS API v1),
  annual mean 2022 $32.26, 2024 $35.06 [CALCULATION: 35.06/32.26 = 1.087]. ICR loaded wage in 2024 $ = $43.45 × 1.087 = $47.22.
- The current PRA inventory (reginfo bulk XML `PRAXML?type=inventory`, RUNDATE 20 OCT 2026) shows the I-9 transfer
  landed in "1615-0160 E-Verify NextGen" (ICR 202401-1615-002): 5.96M h, 51.38M responses. A1 hours on the inventory:
  I-9 33.21M + NextGen 5.96M + E-Verify 1.97M + myE-Verify 0.05M = **41.2M h**. The SS-table route gives 37.6M h.
- A1 revised: 37.6–41.2M h × $47.22 = **$1.78–1.95bn** (rule V-ICR). With the employee's ~9.3M h at the DOT personal
  value ($20/h, see B), the low end is **$1.53bn**. Range **$1.5–1.95bn**, a floor (paperwork minutes only).

### A2 Running admissions (casework) — appended 2026-10-21 15:16:53 JST
Inputs:
- **USCIS fee revenue FY2024 $6.22bn.** IEFA Statement of Financial Condition FY2024: "Fiscal Year 2024 revenue
  collections were $6.22 billion ($4.96 billion in non-premium and $1.26 billion in premium)."
  [SOURCE: https://www.uscis.gov/sites/default/files/document/data/DHS%20SIGNED%20REPORT_%20USCIS%20IEFA%20FY2024%20Statement%20of%20Financial%20Condition.pdf]
  These fees pay for a public service; they are a transfer to the agency that runs admissions. Counting them and the
  agency's spending would count the same resources twice. Reported, not summed into the deadweight figure.
- **Applicant paperwork time and out-of-pocket costs (USCIS, DOL, EOIR ICRs).** Parsed from the PRA bulk inventory
  XML [CALCULATION: scratch `scripts/inv.py`]: USCIS (agency 1615) 93 ICRs, 131.3M h, cost burden $3.60bn. I remove
  A1's items (41.2M h) and ICRs created after 2024 (1615-0166 registration 4.41M h; 1615-0169/0170/0171 2025
  vetting clearances 23.2M h; 1615-0167 gold card) → **62.5M h for 2024-vintage benefit casework**. DOL immigration
  ICRs (LCA 0.84M h, PERM 0.34M, prevailing wage 0.15M, H-2A 0.23M, H-2B ~0.2M) ≈ **1.8M h**. EOIR 0.4M h, $0.05bn.
  Vintage caveat: several ICRs were renewed in 2025–26 with updated volumes, so this is the 2024 regime at
  ~2025 volumes.
- What the USCIS ICR "cost burden" contains: N-400 Supporting Statement item 13: "Costs may include payments for
  document translation and preparation services, attorney and legal fees, postage … average cost for these
  activities is $515 and approximately 90 percent … may incur this cost … $421,645,950." Filing fees excluded
  ("For informational purposes, there is a $760 paper filing fee"). So the $3.6bn is the agencies' own estimate of
  out-of-pocket preparation and legal costs, including medical exams (I-693 $329M).
- **Representation volume.** G-28 (attorney/accredited representative appearing before USCIS) ICR 202601-1615-002:
  4,677,172 responses/yr ("multiplying 4,677,172 (the estimated number of responses) x 0.333 hours"). EOIR-28
  (appearance before immigration court) 1125-0006: 1.54M responses/yr.
- **Private immigration bar.** AILA: "more than 18,000 attorneys who practice and teach immigration law"
  [SOURCE: https://www.aila.org/about]; 2024 media kit says "more than 16,000". IBISWorld via AILA: "over 52,000 people
  employed in the 'Immigration Lawyers & Attorneys industry' in 2023" [SOURCE: https://www.aila.org/library/think-immigration-what-s-changed-in-immigration-law-over-the-last-two-years-what-hasn-t]
  (secondary, IBISWorld's own figure not seen). AILA 2022 Marketplace Study: 2021 mean hourly rates $245–383;
  "87% of respondents report they work on a flat-fee basis"; mean personal income by practice area: asylum $104,167,
  business $209,923, family $105,099. 2025 media kit primary practice: business 28.7%, family 17.7%, asylum 10%,
  deportation 7.9%, multi-area 28.4%; 12.2% legal services/nonprofit.
- Lawyer time value used in USCIS's G-28 ICR: "May 2024 … Lawyers (23-1011) of $87.86 times … 1.46 … $128.28".

Estimate of private legal services [CALCULATION, hand; INFERENCE on revenue-per-head]:
- Route L1 (headcount): 52,000 industry employees × $100–200k revenue per employee = $5.2–10.4bn.
- Route L2 (attorneys): 18–25k practising attorneys × $250–450k firm revenue per attorney (mean attorney income
  $105–210k, revenue ≈ 2–2.5× attorney income) = $4.5–11bn.
- Route L3 (case volume): 4.68M G-28 appearances × $700–1,500 average fee = $3.3–7.0bn; plus 1.54M EOIR-28
  appearances × $1,000–3,000 = $1.5–4.6bn; sum $4.8–11.6bn. (A G-28 is often filed for each form in a package, so
  per-appearance fees are below per-case fees.)
- Agency floor: USCIS + EOIR ICR out-of-pocket $3.65bn (includes ~$0.33bn medical exams).
- **Private immigration legal services ≈ $7bn (range $4.5–11bn).** Of this, removal defense and asylum (court work) ≈
  20–30% by AILA practice shares, ≈ $1.5–2.5bn. That share is a private cost of enforcement adjudication, not
  of admissions.
- **Applicant and employer time:** 62.5M + 1.8M + 0.4M ≈ 64.7M h. At the DOT personal value $20/h: $1.3bn; at the ICR
  loaded wage $47.22: $3.1bn. **$1.3–3.1bn.** Part of this time is already counted in the attorney fees (the
  respondent hours are the agency's estimate of time "for the respondent", which includes preparers in some ICRs);
  overlap [UNVERIFIED], so I subtract nothing and flag it.
- **A2 total, deadweight-type (excluding USCIS fees): ≈ $8–14bn, central ≈ $10bn.** With fees, as an outlay figure:
  $14–20bn.
- [GAP] State Department visa forms (DS-160 21.0M h, immigrant visa DS-260 4.65M h, diversity visa 5.54M h) fall
  mostly on foreigners abroad and are excluded from a US-resident cost. Immigrant-visa petitioners in the US pay
  attorney fees that are inside route L1/L2. [GAP] Employer-side H-1B/PERM costs other than legal fees (recruitment
  advertising for PERM, ACWIA/fraud fees, which go to DOL/USCIS accounts and are transfers) not itemized.
- Named and excluded: USCIS spending above fees, EOIR's ~$0.8–1bn budget, CBP/ICE.

### A3 Political fight — appended 2026-10-21 15:27:23 JST
**Plan change (logged):** the Senate LDA API (lda.senate.gov and lda.gov) returns Akamai "Access Denied" (HTTP 403) to
direct requests from this machine. Through Exa's fetcher the API answers, but the issue-code filter
`lobbying_activity_general_issue_code=IMM` is ignored (count 96,955 = nearly all 2024 filings; the first hit is a 911
dispatch centre), while the text filter works: `filing_specific_lobbying_issues=immigration`, 2024 → **"count": 1523**
filings. Paging ~1,500 filings through Exa was not feasible, so the dollar split uses secondary LDA aggregators,
labelled as such. OpenSecrets pages are behind Cloudflare and Firecrawl's token is dead.

Lobbying:
- LegiList LDA tracker, issue IMM filings by year: "2024 | 2,059" [SOURCE: https://legilist.com/lda/issue/imm/] (secondary).
- OpenAmerica per-issue table (whole-filing amounts; "a filing that lobbied on three issues has its full spend counted
  under all three"): "16. Immigration $939,810,057 3,247 filings · 676 clients" [SOURCE: https://openamerica.io/lobbying/by-issue/]
  — year selector unclear in the fetched view; treat as the **gross upper bound** (whole budgets of filings that touched
  immigration). [UNVERIFIED year]
- PlainInfluence: "$120.7M in itemized Immigration lobbying disclosures across 597 filers … 2023-2024"
  [SOURCE: https://plaininfluence.com/issue/IMM] — allocation method not stated; read as an issue-allocated figure.
- OpenSecrets client list for IMM 2024 (fetched via Exa): top by report count "US Travel Assn 25, Microsoft 18, GEO
  Group 16, FWD.us 15, Business Roundtable 14 … NumbersUSA.com 9". Most immigration lobbying is business visa demand
  and contractors, not the restriction-vs-expansion fight.
- **Lobbying: allocated ≈ $0.12bn (rule 1/n issue codes), gross ≤ $0.94bn.**

Advocacy nonprofits (ProPublica Nonprofit Explorer API, IRS 990 total functional expenses, tax year 2023, latest filed):
- Restrictionist: FAIR $7,453,094; NumbersUSA Action $1,015,093 + NumbersUSA Education & Research $6,782,419; Center for
  Immigration Studies $3,315,911; Immigration Reform Law Institute $2,689,030 → **$21.3M** (America First Legal
  $10.3M is multi-issue; not added).
- Expansionist (national policy shops): American Immigration Council $12,404,600; National Immigration Law Center
  $18,164,437; FWD.us Education Fund $17,073,154; United We Dream Network $10,398,578; National Immigration Forum
  $6,483,852 → **$64.5M**; plus CLINIC $16.7M (mostly legal-capacity work) and the 501(c)(4) arms (FWD.us Inc,
  UWD Action, Forum Action Fund) not retrieved [GAP].
- State coalitions from the IRS BMF (NTEE R21, revenue field): ICIRR $56.3M, CHIRLA $24.5M, MIRA $7.8M; RAICES $39.2M and
  Tahirih $15.8M are mostly legal services (A2). NTEE P84/Q71 totals ($3.9bn, $2.0bn) are dominated by federally funded
  shelter, resettlement and legal-service contractors (Southwest Key $496M, Acacia $354M, IRC $1.3bn global) and are
  **not** political spending; not used.
- **Advocacy (both sides, political/policy share): $0.15–0.4bn** [INFERENCE: core national ≈ $0.09bn named above, ×1.5–4
  for unretrieved c4s, state/local coalitions, think-tank immigration programs (Heritage, Cato, MPI, Brookings), and the
  ACLU immigrants' rights project]. Restrictionist share of the named core ≈ 25%.

Campaign advertising (largest item):
- AdImpact via Washington Post: "More than $247 million was spent in the first six months of this year on television,
  streaming platform and digital ads that mention immigration … Over 90 percent of the ads supported Republican
  candidates" [SOURCE: https://www.washingtonpost.com/elections/interactive/2024/republican-campaign-ads-immigration-border-security/].
- America's Voice from AdImpact (11 Oct 2024): "Republican-aligned campaigns have spent $681 million on 1,615 unique TV ads
  that mention immigration so far this year" [SOURCE: https://americasvoice.org/blog/republicans-billion-dollar-bet-on-nativism/].
- Catalyze/Citizens memo from commissioned AdImpact data, 11 battleground states + Montana: "From January 2024 to October
  2024 … spent $680,452,236 on immigration-focused television ads … 84%, or $573,483,916 … GOP … $106,968,320, or 16% …
  Democratic"; "In October 2024, GOP … spent $249,502,818"; "more than $10 billion has been spent on political advertising
  in 2024" [SOURCE: https://catalyzecitizens.org/wp-content/uploads/2024/11/memo_-october-24-ad-spending-data-1-1.pdf].
  Both advocacy-side sources, but the numbers are AdImpact's.
- [CALCULATION] National full year, both parties: GOP $681M by 11 Oct + late October/November (GOP $249.5M in October in 12
  states alone, about half falling after 11 Oct) + Democrats ≈ $110–200M → **gross $0.9–1.3bn** of TV/CTV ads that mention
  immigration, ≈ 9–13% of $10bn total. Ads tagged "immigration" usually carry 2–3 issues (crime, inflation): allocated
  share **$0.35–0.6bn**.
- Net view: campaign budgets are set by fundraising, not by the issue mix; immigration ads displace ads about other
  issues one for one. The net resource cost of immigration being the topic is ≈ 0 [INFERENCE]; the gross figure is the
  share of the campaign that the issue absorbed.

**A3 total: gross ≈ $1.2–2.6bn (ads + whole lobbying filings + advocacy); allocated ≈ $0.6–1.1bn; net of substitution
≈ $0.15–0.4bn** (the advocacy organisations exist only because the issue does, so they are the non-substitutable part;
lobbying and ads would largely go to other issues).
[GAP] Private litigation costs (Texas v. US etc. are public; private plaintiffs are inside the advocacy budgets).
[GAP] Digital/social ads beyond TV/CTV, mailers, texts: not counted.

### B Time on immigration news and debate — appended 2026-10-21 15:32:16 JST
Inputs:
- **Adults:** 266,978,268 aged 18+ on 1 July 2024 [DATA: Census `nc-est2024-agesex-res.csv`, SEX=0, AGE 18–100+,
  POPESTIMATE2024; total 340,110,988].
- **Total news time per adult.** Allen, Howland, Mobius, Rothschild & Watts (2020), *Science Advances* 6:eaay3539, Nielsen
  TV panel (N≈100,000) + Comscore, Jan 2016–Dec 2018: "the ratio of TV to online news … is more than five to one (54 min
  versus 9.7 min)"; news is "at most 14.2% of Americans' daily media diets" of "over 7.5 hours (460 min)/day". TV news
  includes "roughly 400 programs … classified by Nielsen as 'news'", magazine news and late-night comedy.
  [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC7124954/]. Pew 2010 self-report: "increasing the total time spent with
  the news to 70 minutes" [SOURCE: https://www.pewresearch.org/politics/2010/09/12/americans-spending-more-time-following-the-news/].
  A 2024 SurveyMonkey poll (SmartNews, n=1,000) gives "around 2 hours" including 55 min social media; weak, used only to
  set the high end. **Range 50–80 min/day, central 64.** [GAP] No 2024 passive-metered figure found; TV news audiences have
  fallen since 2018, online/social risen.
- **Immigration's share of news airtime: GDELT TV 2.0 API** (`mode=timelinevol`, % of 15-second caption clips matching),
  1 Jan–11 Oct 2024 (archive's last 2024 day in the API is 20241011; 285 days) [CALCULATION: scratch `scripts/gdelt.py`,
  `scripts/gdelt2.py`]:

  | station | narrow terms (immigration, immigrant(s), migrant(s), deportation(s), asylum) | broad (+ border) |
  |---|---|---|
  | FOXNEWS | 2.397% | 5.194% |
  | MSNBC | 1.145% | 1.964% |
  | CNN | 1.115% | 2.227% |
  | KGO / KPIX / KNTV (SF ABC/CBS/NBC, all-day incl. non-news) | 0.42 / 0.67 / 0.57% | 0.84 / 1.14 / 1.03% |

  Audience-weighted cable (Fox 0.6, MSNBC 0.25, CNN 0.15, [ASSUMED] weights): **1.89% narrow, 3.94% broad.** A keyword
  hits only some clips of a segment about immigration, so topic time ≈ clip share × 1.5–3 [ASSUMED]. "Border" also picks up
  Ukraine/Gaza. Local affiliates' all-day shares, divided by a ~30% news share of their airtime, imply ~1.5–2.5% of news
  time, close to CNN/MSNBC.
  **Immigration share of news time: low 2%, central 5%, high 10%.**
- Demand side cross-check: Gallup, Feb 2024: "Significantly more Americans name immigration as the most important problem
  facing the U.S. (28%) than did a month ago (20%) … essentially ties the 27% reading from July 2019 as the highest in
  Gallup's trend" [SOURCE: https://news.gallup.com/poll/611135/immigration-surges-top-important-problem-list.aspx]. Salience
  was at a record in 2024, so 2024 is near the top of the attention distribution, not a typical year.
- **Valuation:** V1 = USDOT BCA Guidance (May 2025 update II), Table A-2: "Recommended Hourly Values of Travel Time Savings
  (2023 $ per person-hour) … Personal $19.40" [SOURCE: https://www.transportation.gov/sites/dot.gov/files/2025-05/Benefit%20Cost%20Analysis%20Guidance%202025%20Update%20II%20%28Final%29.pdf]
  × 1.029 CPI 2023→24 [ASSUMED] = **$19.96/h**. V2 = after-tax average wage: CES total private AHE 2024 mean $35.06 × (1 − 0.20
  average tax [ASSUMED]) = **$28.05/h**.

Gross [CALCULATION: scratch `scripts/calc.py`]:

| case | news min/day | immigration share | immigration hours/yr | h per adult | V1 | V2 |
|---|---|---|---|---|---|---|
| low | 50 | 2% | 1.62bn | 6.1 | $32bn | $46bn |
| central | 64 | 5% | 5.20bn | 19.5 | $104bn | $146bn |
| high | 80 | 10% | 12.99bn | 48.7 | $259bn | $364bn |

Excluded from B: conversation and social-media argument outside news (ATUS has no political-talk code) [GAP]; ad exposure
time (the ~$1bn of immigration ads bought ~20bn+ views per the Catalyze memo — "reaching over 20 billion views" — at
~30 s each that is ~0.17bn h, already inside TV time).

The case for a large hidden burden:
- 2024 was a record-salience year (Gallup 28%), and TV news is mostly watched by the old (Allen: 94 min/day at 55+ vs 9
  at 18–24), whose time has few market alternatives but real value; 5bn hours is ~20 h per adult per year, the same order
  as all I-9 paperwork in the country × 125.
- The keyword measure undercounts: much immigration coverage is framed as "the border", "crime", "Springfield" or
  "cities' shelters", and online/social debate (where outrage content travels) is not measured at all.
- Exposure is partly involuntary (ads, autoplay, ambient cable in public places); the time-value rule then measures a
  real cost, and stress and polarisation come on top [UNVERIFIED for immigration specifically; not priced].

The case for mostly substitution, near-zero net:
- Total news time is stable across years while topics swing. Pew 2008: "Americans … are spending about the same amount of
  time with news as they did a decade ago … 66 minutes"; Pew 2010: 57 minutes on traditional platforms "as was the case in
  2000"; Allen et al.: total media time "relatively stable over the 36-month period", with only seasonal and election
  peaks. Topic swings re-slice a roughly fixed daily budget.
- The news hole is fixed on the supply side: Eisensee & Strömberg (2007, QJE 122:693): disaster relief "depends on whether
  the disaster occurs at the same time as other newsworthy events … other newsworthy material crowds out this news
  coverage". When immigration fills airtime, other stories leave it; viewers do not watch more.
- News time is chosen; by revealed preference its value to the viewer is at least its time cost. Pricing gross minutes at a
  wage treats a consumption good as a pure loss. The cost of immigration being the topic is then only the difference in
  value between immigration news and the news it displaced, which may be either sign.
- **Net reading:** the counterfactual is the same news minutes about other topics, so net ≈ 0. A rough upper bound, if
  immigration salience raised total news time by 3–10% of the news day on the issue's share of 5–10%: 0.16–1.04bn h,
  **$3–29bn**. Neither bound is identified; I found no study that estimates how total news time responds to one topic's
  salience. **Net: point unidentified, bounded $0–30bn, most likely near the bottom.**
- Suggested next query if re-dispatched: Nielsen/Comscore total-day news minutes 2019 vs 2024 by month, regressed on
  GDELT immigration share (does total news time rise in immigration months?); Media Cloud online-news immigration share.

### E Mexican-origin share — appended 2026-10-21 15:32:16 JST
Inputs:
- R1 stock: MPI (ACS 2023): "Mexicans … accounting for about 23 percent of all 47.8 million foreign-born residents as of
  2023 … 10.9 million" [SOURCE: https://www.migrationpolicy.org/article/mexican-immigrants-united-states-2024]. **23%.**
- R2 unauthorized: OHSS Table 2, 2022: "Total 10,990,000 … Mexico 4,810,000" = 43.8%; "Forty-four percent of unauthorized
  immigrants in 2022 were from Mexico" [SOURCE: OHSS 2024_0418 estimates report]; Pew: "in 2022, Mexico accounted for 37% of
  the nation's unauthorized immigrants"; MPI 45% (mid-2022). Pew's Aug 2025 revision (14M in 2023) supersedes its 2022
  figure; its Mexican share not pulled [GAP]. **37–45%, central 41%.**
- R3 caseload/attention: MPI (DHS OHSS Table 10, FY2023): "approximately 180,500 Mexicans received lawful permanent residence,
  comprising 15 percent of the 1.2 million new LPRs"; naturalization "13 percent of the 878,500"; "the Mexican share of
  migrants crossing the U.S.-Mexico border irregularly … 29 percent in FY 2023" (CBP via MPI). GDELT co-mention, same
  15-second clip, 1 Jan–11 Oct 2024: immigration × (mexico OR mexican(s)) = 0.047% CNN, 0.067% Fox, 0.028% MSNBC, i.e.
  **4.2% / 2.8% / 2.4%** of immigration clips; immigration × (Venezuela/Haiti terms) = 0.051 / 0.091 / 0.061%, higher than
  Mexico on every channel. For employer compliance, R3 = Mexican-born share of the labour force: 10.9M × 68% LFP (MPI) ÷
  ~168M civilian labour force [TRAINING-DATA for 168M] ≈ **4.4%**.

Attribution (central dollars; ranges carry through proportionally):

| component (central) | R1 stock 23% | R2 unauthorized 41% | R3 caseload/attention |
|---|---|---|---|
| A1 compliance $1.8bn | $0.41bn | $0.74bn | 4.4% hires → $0.08bn |
| A2 casework $10bn | $2.3bn | n/a for benefits; removal-defense $2bn × 41% = $0.8bn | benefits $8bn × 15% + removal $0.8bn = $2.0bn |
| A3 fight, allocated $0.85bn | $0.20bn | $0.35bn | explicit co-mention 3% → $0.03bn; border-crosser 29% → $0.25bn |
| B time, gross V1–V2 $104–146bn | $24–34bn | $43–60bn | explicit 3% → $3–4bn; border-crosser 29% → $30–42bn |

Reading: by the people the system is about (R1/R2) the Mexican-born carry a quarter to two-fifths; by what the 2024 fight was
actually about on air (R3 explicit), Mexico is a minor topic, behind Venezuela/Haiti. In 2024 the debate was about recent
non-Mexican border arrivals more than about the settled Mexican population. [FRAMING-SENSITIVE]
Note on scope: these rules attribute to the Mexican-born. US-born Mexican-origin people (~37M total Mexican-origin
[TRAINING-DATA]) are not the object of the admissions system or the I-9 screen beyond family petitions; extending E to
them under a population-share rule (~11% of residents) would assign the general cost by headcount, which I did not
pre-register and do not report as a rule.
