**Verdict:** On the evidence available, race- and ethnicity-based preferences cost non-Hispanic
white natives about **$4.0bn a year in 2024 (scenario range $0.2–18.7bn)**, which is **$41 per
white native worker ($2–192)** or 0.05% of their earnings. The level before 2023 was the same
within rounding: $3.8bn ($0.15–17.5bn). About **28% of the central cost ($1.1bn) corresponds to
seats, jobs and contracts that went to Hispanic beneficiaries**, and about 15% ($0.6bn) to
Mexican-origin beneficiaries. Two channels carry most of the total, and both rest on
weak evidence:
- **Elite admissions.** The earnings value of a lost seat is contested: zero in Dale–Krueger and
  in Bleemer's Berkeley discontinuity, large in Chetty–Deming–Friedman.
- **Federal-contractor hiring.** Nobody has measured the wage loss of a displaced white worker.

Four channels are not priced: graduate and professional admissions, state and local minority
set-asides, public-sector hiring decrees and corporate hiring after 2020. The result is a transfer
among residents, not a fiscal cost of immigration. It sits beside ladder entry 194 and adds to
neither that entry nor the $203–250bn account.
[CALCULATION: `calc.py` → `derived/calc_output.txt`]

## What was estimated

The object is the annual earnings and business-income loss to non-Hispanic white natives from
preferences based on race or ethnicity, net of any gain whites received from the same regime,
such as the penalty on Asian applicants. Sex-based preferences are excluded. So is the white-women
share of the Department of Transportation's disadvantaged-business program (DBE), because that
share moves money among whites.

Each row multiplies a measured count by published effect sizes:
- IPEDS fall 2023 first-year enrollment;
- USAspending contract obligations for FY2022 and FY2024;
- CPS ASEC 2025 earnings, taxes, nativity and Hispanic origin.

The effect sizes are page-cited in `calc.py`. Values tagged [INFERENCE] are assumptions; the
table below lists them. "Low", "central" and "high" are scenarios, and the high case sets every
input high at once. They are not confidence intervals.

**Periods.** The 2024 column uses the 2024 working population and FY2024 contracting. The
pre-2023 column uses the 2022 working population and FY2022 contracting.

## Result by channel

$bn a year. Hispanic and Mexican-origin shares are of the central 2024 cost. Grade: B = causal
estimate in a comparable setting; C = causal estimates combined with at least one assumed input;
D = assumption-dominated.

| Channel | 2024 low / central / high | pre-2023 low / central / high | Hispanic | Mexican-origin | Grade |
|---|---|---|---|---|---|
| 1 Undergraduate admissions (earnings of the working population) | 0.00 / 1.58 / 7.92 | 0.00 / 1.52 / 7.58 | 44.7% | 22.9% | C |
| 2 Federal-contractor hiring (EO 11246) | 0.00 / 1.37 / 5.48 | 0.00 / 1.37 / 5.48 | 20% (0–50%) | 11.7% | C−/D |
| 3a 8(a) contracts, profit lost by other firms | 0.15 / 0.46 / 2.46 | 0.12 / 0.37 / 2.14 | 9.0% | 4.2% | C |
| 3b DOT DBE, profit lost by other firms (minority-owned part) | 0.02 / 0.07 / 0.25 | 0.02 / 0.07 / 0.18 | 16.9% | 7.8% | C− |
| 3c DOT DBE, price premium paid by taxpayers | 0.00 / 0.48 / 1.29 | 0.00 / 0.48 / 0.95 | 16.9% | 7.8% | B−/C |
| 3d 8(a), price premium paid by taxpayers | 0.00 / 0.00 / 1.30 | 0.00 / 0.00 / 1.13 | 9.0% | 4.2% | D |
| 4 Other channels (see Gaps) | not priced | not priced | | | |
| **Total priced** | **0.18 / 3.96 / 18.70** | **0.15 / 3.80 / 17.46** | **28.2%** | **14.8%** | |
| Career loss (rows 1, 2, 3a, 3b) | 0.18 / 3.48 / 16.11 | 0.15 / 3.32 / 15.37 | | | |
| Taxpayer premium (rows 3c, 3d) | 0.00 / 0.48 / 2.59 | 0.00 / 0.48 / 2.08 | | | |

[CALCULATION: `derived/channels.csv`]

**Per worker.** There are 97.5 million non-Hispanic white native workers with 2024 earnings, and
their mean earnings are $77,004. The cost per worker is $2, $41 or $192 a year across the three
scenarios. [CALCULATION: CPS ASEC 2025, MARSUPWT/100, PEARNVAL > 0]

**Hispanic part in 2024.** The central Hispanic part is $1.11bn:

| Channel | Hispanic part, central |
|---|---|
| Admissions | $0.71bn |
| Contractor hiring | $0.27bn |
| Contracting | $0.13bn |

Across the scenarios the Hispanic part runs from $0.02bn to $7.03bn. Two narrower parts, low /
central / high:
- **Mexican-origin:** $0.01 / 0.58 / 3.76bn.
- **Immigrants and their children:** $0.01 / 0.78 / 4.92bn. These are Hispanic beneficiaries who
  were born abroad or have a foreign-born parent, which is the part most directly tied to
  immigration since 1965.

[CALCULATION: Mexican and generation shares from CPS ASEC 2025, as proxies for each channel's
beneficiaries. Hispanic graduates aged 22–40: 51.2% Mexican, 67.0% first or second generation.
Hispanic workers: 58.4% and 72.2%. Hispanic owners of incorporated businesses: 46.4% and 79.5%.]

## Channel 1: undergraduate admissions before the SFFA ruling

**Measured seats.** The first input is the number of first-year students at selective colleges,
from IPEDS fall 2023. This was the last class admitted before the ruling. Two tiers:
- **Elite:** admission rate under 15%. This tier has 53 institutions, 94% of them private, and
  68,607 first-year students. Of these, 5,235 are Black and 9,626 Hispanic.
- **Selective:** admission rate of 15–50% and an SAT median of at least 1200 (or an ACT median
  of at least 26). This tier has 80 institutions and 135,483 first-year students, of whom 7,782
  are Black and 16,761 Hispanic.

Public universities in the nine states that banned preferences before 2023 are excluded. Only
the high scenario adds a broader tier: 79 institutions with admission rates of 50–70%.
[CALCULATION: `derived/ipeds_tiers.csv`]

**Seats that preferences moved.**
- **Elite tier.** Removing race from admissions cuts Black admits by 64–72% and Hispanic admits
  by about 51%. Whites fill 12–34% of the freed seats.
  [SOURCE: Espenshade & Chung 2005, *Social Science Quarterly* 86(2), Table 2 p. 299: Black 899
  → 326, Hispanic 792 → 381, white 5,134 → 5,256, Asian 2,369 → 3,141. Arcidiacono, Kinsler &
  Ransom 2023, Table 11 p. 62, Harvard classes 2014–19: Black 1,163 → 324, Hispanic 1,188 → 581,
  white 2,704 → 3,195, Asian 2,013 → 2,812.]
- **Selective sector.** The loss is 20–36% of Black and 18–28% of Hispanic enrollment, and whites
  fill 69–93% of the freed seats.
  [SOURCE: Hinrichs 2012, *REStat* 94(3), Table 5 and text p. 717: at public US News top-50
  universities, bans cut Black enrollment 1.74 points and Hispanic 2.03 points, and raised white
  enrollment 2.93 points. AKR Table 11 p. 62, UNC: in-state Black −35.5%, Hispanic −17.6%, white
  +1,024; out-of-state white +1,924.]

These parameters produce 8,720 upward moves by white natives per entering cohort (5,714 to
21,489): white natives who move up one tier. [CALCULATION]

**Value of a lost seat.**
- **Elite boundary.** The loss is 0% (low), 11.5% (central) or 23% (high) of $211k, the
  2024-dollar mean earnings of graduates of the College and Beyond colleges. Central is $21,887
  per affected worker-year.
  - Low: Dale & Krueger find a return of about zero once they adjust for where students applied.
    [SOURCE: NBER w17159 p. 25]
  - High: Chetty, Deming & Friedman find that Ivy-Plus attendance, compared with the average
    flagship, raises income by 23% on average across income quantiles. [SOURCE: w31492 p. 37]
    They also find $101k higher mean income at age 33 on a $143k counterfactual (p. 4), with no
    significant effect on mean income rank (p. 30).
  - Central: half of 23%, because a rejected applicant's next choice is usually better than a
    flagship. [INFERENCE]
  - Earnings base: [SOURCE: Dale–Krueger Table 1 p. 29: $139,698 in 2007 dollars, converted with
    CPI-U, TRAINING-DATA]
- **Selective boundary.** The loss is 0%, 3% or 10% of $111,719, the mean earnings of
  non-Hispanic white native graduates aged 25–64 (CPS). Central is $3,018 per affected
  worker-year.
  - Low: Bleemer's Berkeley discontinuity for marginal non-minority applicants finds a log-wage
    effect of −0.10 (s.e. 0.11). [SOURCE: *QJE* advance-access Fig. VIII p. 36; "Prop 209 provided
    minimal benefits to non-URM students", p. 37]
  - High: Hoekstra finds a +20% flagship effect for white men and none for white women, as cited
    in Dale–Krueger p. 2; 10% is the average.
  - Central: half of Dale–Krueger's unadjusted 6% per 100 points of school SAT (p. 25).
    [INFERENCE]

**From cohorts to a yearly cost.** Workers aged 22–61 in 2024 entered college between 1981 and
2020. Earlier cohorts are scaled down by their lower minority enrollment shares: 0.874 for Black
and 0.486 for Hispanic students, relative to 2023. [CALCULATION: NCES Digest 2024 Table 306.10;
the Hispanic share rose from 4.0% in 1980 to 22.2% in 2023]

About two-thirds of the central cost ($1.06bn of $1.58bn) sits at the elite boundary. Two more
figures:
- **Present value.** One pre-SFFA entering cohort's lifetime loss is worth $1.30bn (range
  $0–6.58bn) at 3%, 59% of it Hispanic-driven.
- **2024 compared with before 2023.** The 2024 figure matches the pre-2023 one because everyone
  working in 2024 was admitted before the ruling. SFFA changes the flow of new cohorts, not the
  2024 working population.

**Evidence for a large cost.**
- **Preferences were large.** At Harvard, a typical Black applicant's admission chance was over
  four times what it would have been if treated as white, and a Hispanic applicant's 2.4 times.
  [SOURCE: AKR 2023 abstract p. 1]
- **Most minority admits would not have been admitted without them.** Without preferences, 70%
  of Black and 54% of Hispanic Harvard admits, and 91% and 71% of UNC out-of-state admits, would
  not have been admitted. [SOURCE: AKR Table 10 p. 61]
- **The Dale–Krueger null has a challenger.** Chetty–Deming–Friedman reproduce Dale–Krueger's
  matched-application design and still find large effects in the upper tail. [SOURCE: w31492 p. 4]
- **Graduate schools are excluded, and preferences there were larger.** In 1990–91 law school
  data, only 687 of 3,435 Black applicants admitted somewhere would have been admitted on test
  scores and grades alone. [SOURCE: Wightman 1997, via Espenshade & Chung p. 302]

**Evidence for a small cost.**
- **Whites gain little from race-blind admission at elite privates.** Their acceptance rate would
  rise from 23.8% to 24.3%, and Asians would fill nearly four of every five freed places.
  [SOURCE: Espenshade & Chung p. 298]
- **For whites, a more selective school adds about nothing.** The adjusted return to selectivity
  is about zero for the mostly white samples. Black and Hispanic students, by contrast, gain.
  [SOURCE: Dale–Krueger p. 25]
- **Minority applicants lose more than whites gain.** After Prop 209, minority applicants' wages
  fell about 5%, while marginal non-minority applicants gained nothing measurable.
  [SOURCE: Bleemer p. 4, p. 37]
- **Bans moved students without changing overall attainment.** Bans shifted students between
  colleges but had no effect on the typical student's enrollment or degree attainment.
  [SOURCE: Hinrichs abstract p. 712]

## Channel 2: federal-contractor hiring under EO 11246

**Size.** Contractors employ about a quarter of the workforce. [SOURCE: Miller 2017, *AEJ:
Applied* 9(3) p. 153, citing OFCCP 2013] The shift from whites to preferred groups is:
- **Low:** 0.03 points of contractor employment. Kurtulus's coefficients for 1973–2003 are white
  women −0.122 and white men +0.090. [SOURCE: Kurtulus 2016, *JPAM* 35(1) Table 4 p. 53]
- **Central:** 1.0 point. The Black share rises 0.8 points five years after an establishment
  becomes a contractor [SOURCE: Miller p. 153], plus 0.2 points for Hispanics [INFERENCE].
- **High:** 2.0 points, adding Miller's further 0.8 points after deregulation and 0.4 for
  Hispanics [INFERENCE].

Whites are 85.4% of the earners who are neither Hispanic nor Black, so that share of each moved
job is counted as white. Central, this displaces 355,668 white native workers (11,381 to
711,336). [CALCULATION]

**Wage loss.** A displaced worker loses 0%, 5% or 10% of $77,004. The low case is pure
reshuffling: displaced whites take equivalent jobs elsewhere. Leonard and Smith–Welch describe
that mechanism (as summarized by Holzer–Neumark w7323 p. 37), but zero loss is an assumption.
Holzer and Neumark expect some loss, because wage levels differ between contractors and other
employers; no cited study measures it. [INFERENCE]

**Hispanic share.** Central 20% (range 0–50%). Kurtulus finds that contractor status lowered the
share of Hispanic men (−0.058, s.e. 0.022). Miller says only that Hispanic results are
"qualitatively similar" to Black results (fn. 1, p. 153).

**Periods.** The order was in force through January 2025, so the 2024 figure equals the pre-2023
figure.

**Evidence for a large cost.**
- **The policy worked like a tax on white male hiring.** Leonard models it as "a tax on white
  male employment in contractor firms". In 1974–80 Black male employment grew 0.62% a year faster
  at contractors and white male employment 0.2% a year slower. [SOURCE: Leonard 1990, *JEP*
  4(4), pp. 48, 50]
- **White men had fewer jobs at firms practicing affirmative action.** Holzer and Neumark find
  white male employment 10–15% lower at such firms. [SOURCE: w7323 p. 37]
- **Miller's effects persist.** Black shares keep rising after an employer stops being a
  contractor. [SOURCE: Miller p. 153]

**Evidence for a small cost.**
- **Leonard says the program largely lapsed after 1980.** It "virtually ceased to exist in all
  but name after 1980", and Black employment then grew more slowly at contractors.
  [SOURCE: Leonard 1990, section "Charades for the 1980s"]
- **Enforcement was weak.** Reviews reached about 1% of covered establishments a year, and only
  43 firms were ever debarred through 2001. [SOURCE: Miller pp. 157–158]
- **Hispanic men lost share.** Kurtulus finds contractor status lowered their share, so this
  channel probably transfers nothing to Hispanics.
- **Hiring still favours whites on net.** Whites receive 24% more callbacks than equally
  qualified Latinos (95% CI 15–33%), down from 30% in 1990 to 15% in 2010. [SOURCE: Quillian et
  al. 2017, *PNAS* 114(41), Results] Federal contractors show *smaller* Black–white contact gaps
  than other large employers. [SOURCE: Kline, Rose & Walters, w29053 p. 25]

## Channel 3: contracting

**Federal 8(a).** In FY2024, awards restricted to 8(a) firms (competed and sole-source set-asides)
totalled **$15.13bn**, up from $12.18bn in FY2022. Of the FY2024 total:
- Hispanic-owned firms took 9.0%.
- Native American-owned firms, mostly Alaska Native corporations and tribes, took 56%.

All obligations to 8(a) participants were $36.70bn, which the high case uses.
[DATA: USAspending `spending_over_time`, award types A–D, set-aside codes 8A and 8AN,
`_cache/usaspending/`]

**Most disadvantaged-business dollars are not reserved.** Self-certified small disadvantaged
businesses received $77.29bn, or 10.4% of all contract obligations. This matches the 12.27% SBA
scorecard figure on a smaller base. Only about 20% of those dollars came through race-restricted
8(a) awards; the rest carry no set-aside. [CALCULATION]

**Profit lost by other firms.** The formula is:

restricted dollars × share that other firms would otherwise win (50/75/100%) × margin
(3/6/10%) × 67.0%

- Share won and margin are assumptions. [INFERENCE]
- 67.0% is the white native share of incorporated self-employed earnings, used as a proxy for
  who owns the losing firms. [CALCULATION: CPS]

**What changed in 2024.** The Ultima ruling ended the presumption of social disadvantage in
July 2023. [SOURCE: CRS R48190 pp. 12–13] Even so, restricted dollars rose in FY2024, so the
2024 figure exceeds the pre-2023 figure.

**DOT DBE.** DBE awards and commitments were about $6.2bn in FY2020. [SOURCE: CRS IF12055 v3]
- **Minority-owned share:** 54.7%, from the 1993–99 split of 7.0% to minority-owned firms and
  5.8% to women-owned firms. [SOURCE: Marion 2007 working paper p. 12; dated]
- **Share caused by the goals:** 34%, 50% or 80%. Raising a state's goal by 10 points raises DBE
  use by 4.3 points once state trends are controlled, against 12.6% average participation; without
  trends the response is "nearly one-for-one". [SOURCE: Marion 2007 working paper pp. 4, 11;
  the 50% and 80% are INFERENCE]
- **Price premium:** after Prop 209, California's state-funded highway contracts became 5.6%
  cheaper than federally funded ones that kept the goals. [SOURCE: Marion 2009, *REStat* 91(3),
  abstract p. 503; the body text is paywalled and was not verified]

The premium is applied at 0%, 2.8% or 5.6%. It falls on the $49bn of DOT-assisted contracts that
the 12.6% participation rate implies. Only the minority-owned share of it is counted, and white
natives pay 63.4% of that through income, payroll and state income taxes. [CALCULATION: CPS
ASEC]

The central 2.8% is half the abstract's figure, and the halving is an assumption. A 2008 summary
quotes Marion as finding that winning bids fell "by between 3.1 and 5.6 percent relative to
similar federal-aid contracts". [SOURCE: Geshekter, National Association of Scholars, 25 Sep
2008, quoting Marion; secondary and UNVERIFIED, because the paper's body could not be reached
through fetch_paper, the MIT Press PDF, the DOI page, Unpaywall (no open copy) or CiteSeerX] If
that range is right, the central sits below the paper's lowest estimate. At 3.1% the central DBE
premium row would be $0.53bn instead of $0.48bn. At the range's midpoint, 4.35%, it would be
$0.74bn, and the 2024 central total would rise from $3.96bn to $4.22bn. [CALCULATION: linear
rescaling of row 3c, $0.4773bn × p / 2.8%]

**Periods.** The DBE presumption lasted until 3 October 2025 [SOURCE: 90 FR 47969], so the 2024
figure equals the pre-2023 figure. The high 2024 case scales the dollars by 1.35 for the
infrastructure law. [INFERENCE]

**Hispanic share of DBE dollars.** The DBE rows use 16.9%, the Hispanic-owned share of
minority-owned federal contract dollars. [DATA: USAspending; used as a proxy]

**Evidence for a large cost.**
- **Every restricted dollar is closed to other firms.** For 8(a) awards under $4.5m, the sole-source
  route involves no competition at all. [SOURCE: CRS R48190 Table 1]
- **Marion's 5.6% is the only causal price estimate, and it is sizeable.** [SOURCE: Marion 2009
  abstract p. 503]
- **State and local minority set-asides are missing.** No national total exists, so the priced
  rows understate the contracting channel by an unknown amount. [INFERENCE]

**Evidence for a small cost.**
- **The loss to other firms is the margin, not the award.** Contract dollars buy goods and
  services, so the losing firms forgo only their profit.
- **Many firms would have won anyway.** Many 8(a) firms would win open or small-business
  set-aside competitions. [INFERENCE; the low case assumes half would]
- **The Hispanic link is thin.** Only 9% of restricted 8(a) dollars go to Hispanic-owned firms.
- **The premium is a single estimate.** It comes from one state in the 1990s. Most of it came from
  the mix of subcontractors, which Marion traces to the higher costs of firms in high-minority
  areas rather than to minority-owned firms being less productive than their neighbours.
  [SOURCE: Marion 2009 abstract, as quoted on the UCOP Prop 209 research page]

## Where this sits against the account

**Outside the fiscal ledger.** Rows 1, 2, 3a and 3b are transfers of earnings and profit among
residents. Most beneficiaries are US-born Black and Hispanic Americans. [INFERENCE: CPS
generation shares; second-generation Hispanics are US-born] The premium in rows 3c
and 3d is already inside observed government spending. So nothing here adds to the $203–250bn
complete account. The FAQ rule applies: offsets and side channels do not add unless an entry says
so.

**Beside ladder entry 194.** That entry splits the costs of immigration outside the budget by
income: the bottom four fifths lose $80.7bn and the top fifth gains $46.0bn. This lane's figure
belongs next to it as a second distributional item, with two differences:
- It is about 20 times smaller than the bottom four fifths' loss.
- It is caused by a policy, not by immigration. Immigration enters only because Hispanic arrivals
  and their descendants became eligible.

The most immigration-linked part is $0.78bn central ($0.01–4.92bn): Hispanic beneficiaries who
are immigrants or the children of immigrants. It should be quoted as its own line and not merged
into the entry 194 totals. [INFERENCE]

**Framing** [FRAMING-SENSITIVE]. Whether these amounts count as a "cost" depends on the
counterfactual:
- **Race-blind admission.** AKR and Espenshade–Chung remove race and hold everything else fixed.
- **A ban with institutional responses.** Hinrichs measures actual bans, after universities
  adjusted in other ways.
- **Discrimination.** If contractor affirmative action only offset discrimination, as the
  callback studies suggest it partly did, then part of row 2 is a lost discriminatory advantage.
  Someone else would call it a lost job.

The table follows the counterfactual that each cited source uses.

## 2024, before 2023 and after

The 2024 total ($3.96bn) is not lower than the pre-2023 total ($3.80bn):
- **Admissions.** Everyone working in 2024 was admitted before the SFFA ruling.
- **Contractor hiring.** EO 11246 remained in force.
- **8(a).** Restricted dollars rose after Ultima.
- **DBE.** The presumption stood until October 2025.

The regime changed after 2024: SFFA applies from the fall 2024 class, EO 14173 revoked EO 11246
in January 2025, and the DBE interim rule took effect in October 2025. Those changes shrink future
flows. None of them is priced here, because post-SFFA enrollment by race is not yet published: the
IPEDS EF2024A file returned 404 on 2026-09-24. [DATA]

## Gaps

- **Graduate and professional admissions are not priced.** Wightman's law school counts show
  large preferences. Medicine is the likely largest case, because a displaced applicant can lose
  a physician's career unless they enter an osteopathic school or reapply. [INFERENCE] The AAMC table of acceptances by test score, grades and race
  (FACTS A-23) would price it.
- **State and local minority set-asides.** No national total exists. Nothing is priced.
- **Public-sector hiring decrees.** Court-ordered quotas raised the Black share of new police
  hires by 14 points in litigated departments. [SOURCE: McCrary w12368 abstract] They were mostly
  Black-focused and most have expired, so the channel is not priced.
- **Corporate hiring after 2020.** No credible causal estimate of a net shift exists. The
  channel is not priced.
- **Grants to minority-serving institutions.** These are grants to institutions, not a career
  channel. They are not priced.
- **Wage loss of a displaced contractor worker.** This input is assumed. It drives row 2
  linearly.
- **The selective tier is 78% private, but its preference sizes come from public universities.**
  Hinrichs and UNC in-state are public-sector estimates. UNC out-of-state shows much larger
  effects in competitive pools, so the central may understate this tier.
- **DBE inputs are old.** The dollars are from FY2020, the minority/women split from 1993–99, and
  Marion's price premium was checked in the abstract only.
- **Mexican-origin and generation shares are population proxies.** They are not measured among
  actual beneficiaries. Elite colleges' Hispanic students are likely less Mexican than Hispanic
  graduates in general.
- **No sampling error is reported.** The table shows scenario ranges only, and the
  admissions-to-cohort step assumes constant preference sizes and sector capacity since 1981.
  [INFERENCE]

## Instrument note

The research instrument is an LLM, and its post-training may lean in one direction on this topic
(`notes/llm-bias-caveat.md`). To check for that, each channel lists the strongest evidence on
both sides, and the assumed central values sit between published bounds rather than at either
end.

Conflicts of interest were treated alike on both sides:
- Arcidiacono served as SFFA's expert witness, and Kinsler consulted for SFFA.
- Bleemer worked for the University of California while its Regents backed repealing Prop 209.

Both sets of results are used, and both disclosures are noted.

The central answer depends mostly on three inputs:
- the elite-seat return: 11.5% central;
- the contractor wage loss: 5% central;
- the share of 8(a) dollars that other firms would win: 75% central.

Each moves its row linearly. The low and high totals ($0.2bn and $18.7bn) set every input to its
bound at once, so they are wider than any single input would make them.

## Reproduction

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project --with lxml python3 \
    infra/immigration-fiscal/affirmative_action_cost_2026_09_24/calc.py
```

The inputs are cached under `_cache/`, which is ignored by git. They are:
- the IPEDS 2023 files;
- NCES Digest Table 306.10;
- the USAspending JSON pulls of 2026-09-24;
- the source PDFs and text excerpts.

The CPS ASEC 2025 file is read from `../gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip`.

The script was run twice on 2026-09-24, and the two outputs are byte-identical:

| File | sha256 |
|---|---|
| `derived/calc_output.txt` | `ee522e5381ad9e06610dd3c765477deb7ad47c5e70439420754a77ed8a04cc99` |
| `derived/channels.csv` | `b43f30233454e3bb71c6658699bac2c5322188d92006e3584ceeefe1b8ed3786` |
| `derived/ipeds_tiers.csv` | `cc88946d76346f6d2cd345fa75716ba6b29cb5decf0137790f11b0462e29c173` |

The source log, with page numbers, is `WORKLOG.md`.

## Sources

- Arcidiacono, Kinsler & Ransom (2023), "What the Students for Fair Admissions Cases Reveal
  About Racial Preferences", Duke version of 17 March 2023 (NBER w29964; *JPE Micro*). Cited:
  Tables 10–11, pp. 61–62.
- Espenshade & Chung (2005), *Social Science Quarterly* 86(2): 293–305. Cited: pp. 298–302.
- Hinrichs (2012), *REStat* 94(3): 712–722. Cited: Tables 4–5, p. 717.
- Bleemer (2022), *QJE* 137(1): 115–160. Pages cited are from the advance-access version:
  pp. 4 and 34–37.
- Chetty, Deming & Friedman (2023, revised 2025), NBER w31492. Cited: pp. 4, 30, 37.
- Dale & Krueger (2011), NBER w17159 (*JHR* 2014). Cited: pp. 2, 25, Table 1.
- Miller (2017), *AEJ: Applied* 9(3): 152–190.
- Kurtulus (2016), *JPAM* 35(1): 34–66.
- Leonard (1990), *JEP* 4(4): 47–63.
- Holzer & Neumark (1999), NBER w7323 (*JEL* 2000).
- McCrary (2006), NBER w12368 (*AER* 2007).
- Kline, Rose & Walters (2021), NBER w29053 (*QJE* 2022).
- Quillian et al. (2017), *PNAS* 114(41).
- Marion (2007 working paper), "The Effectiveness of Affirmative Action in Highway Procurement".
- Marion (2009), *REStat* 91(3): 503–522. Abstract only.
- CRS IF12055 (version 3) and CRS R48190 (19 September 2024).
- DOT interim final rule, 90 FR 47969 (3 October 2025).
- USAspending API.
- IPEDS 2023.
- NCES Digest 2024, Table 306.10.
- CPS ASEC 2025.
