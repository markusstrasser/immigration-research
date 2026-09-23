**Verdict:** If the federal part of the group's 2005–2023 fiscal gaps was borrowed, the debt it left
entering FY2024 is **$0.94–1.20tn**, 3.6–4.6% of debt held by the public. On that debt, 2024
taxpayers pay **$30.5–38.9bn** in interest: **$745–950 per member** of the 40.9m Mexican-origin
union, and $102–130 per other resident. That is 3.5–4.4% of FY2024 federal net interest. These are
the central specification on the adopted low and high anchors.
[CALCULATION: `debt_legacy.py` → `derived/stocks.csv`]

- **Range.** Across the eleven back-cast rules on both anchors, the interest runs **$7.7–42.8bn**
  and the stock $0.24–1.32tn. Adding the low and high payer conventions widens this to
  −$1.9bn to +$48.2bn. Every specification together, including rates, windows and financing,
  spans −$2.7bn to +$64.7bn.
- **Federal share it rests on.** The federal government carries **19.0–23.4% of the 2024 gap**:
  $38.6bn of $203.0bn at the low anchor, $58.4bn of $249.5bn at the high anchor. Across payer
  conventions the share is 8.1–29.0%. It moves by year: −7% to +8% in 2005–2007, 42% in 2010, and
  50–57% in 2020–2021.
- **Why the federal side is a cost.** The group's payroll taxes exceed its Social Security and
  Medicare by $27–32bn, as the brief expected for a young group. But federal income tax
  ($128–138bn) falls short of federal Medicaid, refundable credits, SNAP and the federal part of
  state services.
- **How it relates to the annual account.** If adopted, the $30.5–38.9bn enters the main case as
  the response of its interest row, now held at zero. The stock is never added to an annual figure.

Rate used, as the lead asked: OMB **net interest** of $879.879bn (Historical Table 3.1) divided by
the average of end-FY2023 and end-FY2024 **debt held by the public** (Table 7.1: $26,235.6bn and
$28,193.9bn) gives **3.233%**. The BEA interest line, which includes imputed interest on government
pension liabilities, is not used for any rate. Interest paid on securities held outside the trust
funds (Table 3.2 subfunctions 901 + 902 + 903, $949.2bn) gives 3.488%; that is a sensitivity only.
[DATA: `derived/rates.csv`, `derived/summary.json`]

Date: 2026-09-23. Brief: [BRIEF.md](BRIEF.md). [FRAMING-SENSITIVE] The central rule is this lane's
choice; the brief named no central rule. The reasons are below, and every rule is reported.

## Central specification

| 2024, adopted anchor (low–high) | Value |
|---|---:|
| Federal part of the 2024 gap (the flow) | $38.6–58.4bn |
| Stock entering FY2024 (debt from 2005–2023 gaps) | $943–1,202bn |
| Share of end-FY2023 debt held by the public | 3.6–4.6% |
| Legacy interest paid in 2024 | $30.5–38.9bn |
| Per group member / per other resident | $745–950 / $102–130 |
| Share of FY2024 net interest ($879.9bn) | 3.5–4.4% |
| The 2024 gap's own part-year interest (belongs to the flow) | $0.6–0.9bn |
| The brief's D, stock at the end of FY2024 before the 2024 gap | $973–1,241bn |
| Nominal sum of the 2005–2023 federal gaps, without interest | $824–1,044bn |

Specification:
- **Rule:** the programme-by-programme back-cast, with receipts adjusted for relative income and
  the 2020–2022 refundable-credit surge assigned per head.
- **Payer convention:** central.
- **Rates:** OMB effective rates, year by year.
- **Window and financing:** 2005–2023 gaps, all borrowed.

Low anchor = shared allocation, GDP scaling, general government 0.59; high anchor = personal
allocation, cash scaling, 0.84, as in the
[adopted main case](../main_case_2026_09_23/RESULT.md).

Scale reference: debt held by the public rose $21.94tn from end-FY2004 to end-FY2023, and a
per-head share of each year's increase would be $2.52tn. The central stock is 37–48% of that.
[CALCULATION: `summary.json`] [INFERENCE] Most of the difference is spending the adopted account
does not charge the group: defense, existing interest and business subsidies at zero response.

## Method

**F_t**, the federal part of year t's fiscal gap:
- It is responsive spending minus responsive receipts minus the induced receipts F. Each line is
  split by the government that pays or collects it.
- The private production term P is excluded; it never touches the debt.
- Nominal dollars come from the back-cast's GDP deflator (BEA Table 1.1.9).

**Stock and interest:**
- Gaps are borrowed at the end of each calendar year:
  D_start = Σ_{t=start}^{2023} F_t Π_{s=t+1}^{2023} (1 + r_s).
- Legacy interest in 2024 = r_2024 × D_start.
- The brief's D, Σ F_t Π_{s=t+1}^{2024} (1 + r_s), equals D_start × (1 + r_2024). It is the stock
  at the end of FY2024. Multiplying it by r_2024 would charge 2024 interest on 2024's own interest,
  3.2% too much, so the interest uses D_start. Both are reported.
- The 2024 gap's own interest is F_2024 × r_2024 / 2. It is reported beside the flow and is not
  part of the legacy.

**Rates** pair fiscal year s with calendar-year gaps, an approximation. There are four paths:

| Rate path | Definition | 2005 | 2010 | 2015 | 2021 | 2024 |
|---|---|---:|---:|---:|---:|---:|
| Effective (central) | OMB net interest ÷ average debt held by the public | 4.14% | 2.37% | 1.72% | 1.63% | 3.23% |
| Constant | ladder 137's 3.22% | 3.22% | 3.22% | 3.22% | 3.22% | 3.22% |
| 10-year Treasury | FRED GS10, fiscal-year mean | 4.21% | 3.36% | 2.16% | 1.27% | 4.25% |
| Securities held outside trust funds | OMB 901 + 902 + 903 ÷ average debt | 4.31% | 2.76% | 2.01% | 1.91% | 3.49% |

**The 2024 federal split, line by line.** It is rebuilt at the corners that set the adopted band,
and each corner is gated to the published band to 5e-4bn.
[DATA: pinned BEA Section 3, CMS NHEA Table 3, OMB Table 12.3]
- **Federal benefit programmes** are federal: Social Security, Medicare, SNAP, refundable credits,
  unemployment insurance, veterans and SSI's federal part.
- **Receipts** go to the collecting government:
  - federal income and payroll taxes and customs are federal;
  - state-local income, sales and motor-vehicle taxes are state-local;
  - excise taxes, other social contributions and transfers from persons are split by
    BEA Tables 3.2–3.6.
- **State-local consumption and benefits** are federal in the proportion that federal
  grants-in-aid fund them, function by function (BEA Table 3.17).
- **The Medicaid line** takes CMS's federal share of Medicaid spending: 64.0% in 2024, 57.4% in
  2005 and 70.6% in 2022. The rest of BEA's health grants funds state-local health services.
- **Income-security grants** exclude LIHEAP, which goes to energy assistance, and are spread over
  state-local income-security consumption and welfare benefits.
- **General government** is 11.4% federal at the low end of its adopted response and 25.3% at the
  high end. The low end holds the federal executive and legislature fixed.
- **Justice.** The +$5.94bn use-keyed change is $0.81bn federal: prisons 8.4%, courts 12.2%,
  non-border police 16.5%, ICE interior 100%.
- **Uncompensated care.** The under-charged part is $1.9bn federal at both ends: Medicaid DSH at
  the Medicaid share, Medicare DSH federal, and state programmes federal only for their grants.
- **Induced receipts F** are labour taxes, 88.4% federal.

**Payer conventions:**
- *Low* treats block grants as state-local and keeps only open-ended matching grants federal.
  Income-security grants are 67.1% matching in 2024. The corrections increment and the state
  uncompensated-care programmes are state-local.
- *High* puts every BEA health grant on the Medicaid line, charges K-12 at the 12.9% federal share
  used by the incidence memo, uses the composite weights for general government (36.7% federal),
  and makes the corrections increment federal.

**Carrying the split back:**
- **Programme rules** carry each of the group's 2024 lines with its own national BEA series, as
  the September 20 programme rule does. Each line takes that year's federal share from Tables 3.17
  and 3.12 and NHEA. Receipts use their own federal or state-local series. The group's relative
  use of each programme stays at its 2024 value.
- The machinery reproduces the September 20 programme back-cast to 5.0e-5bn before any split is
  applied, and every rule reproduces its 2024 split exactly.
- **Whole-budget rules** (flat, ratio, income) use the back-cast's adopted annual net cost plus P
  and **hold the 2024 federal share**, the brief's fallback. A variant scales the federal part with
  federal receipts and expenditure per resident (BEA Table 3.2).

### Why this central rule

- **Programme rule.** It uses the measured national growth of each programme. Medicaid and
  Medicare were 42–47% smaller per resident in 2005. It also uses each year's measured federal
  funding share.
- **Income-adjusted receipts.** The group's measured per-capita income relative to the nation rose
  from 0.519 in 2008 to 0.611 in 2024. Holding receipts at the 2024 ratio contradicts that series,
  as the back-cast memo itself notes. Years 2005–2007 are held at the 2008 value by the back-cast.
- **Pandemic credits per head.** The group's 2024 key share of refundable credits is 22.8–24.2%,
  against 12.0% per head.
  - The 2020–2022 national excess over the 2019–2023 line is assigned per head. It was mainly the
    stimulus payments and the 2021 child-credit expansion [TRAINING-DATA].
  - The back-cast's own alternative sets 2020–2021 to the 2019/2022 mean. That removes pandemic
    payments the group did receive, so it is too low.
  - Pandemic payments were close to uniform per person, and the first round excluded households
    filing without Social Security numbers [TRAINING-DATA]. Per head may therefore still be
    slightly high.

The income adjustment is the largest single judgment: it adds $0.46–0.49tn to the stock
(compare the first and fourth rows of the rule table). Whole-budget income with federal series is
an independent method and gives $0.89–1.14tn, close to the central.

## The 2024 split of the adopted gap

| Payer convention | Low anchor ($203.0bn gap) | High anchor ($249.5bn gap) |
|---|---:|---:|
| Central | $38.6bn (19.0%) | $58.4bn (23.4%) |
| Low | $16.5bn (8.1%) | $35.6bn (14.3%) |
| High | $48.5bn (23.9%) | $72.4bn (29.0%) |

[CALCULATION: `derived/federal_split_2024.csv`; lines in `derived/federal_split_2024_lines.csv`]

Central convention, low–high anchor, $bn:

| Federal line | Low anchor | High anchor |
|---|---:|---:|
| Receipts, total | 329.1 | 311.0 |
| Federal income tax | 137.9 | 128.2 |
| Payroll taxes | 158.4 | 150.6 |
| Spending, total | 379.8 | 377.4 |
| Medicaid | 76.8 | 76.7 |
| Medicare | 64.0 | 64.0 |
| Social Security | 62.7 | 59.9 |
| Refundable credits | 55.4 | 52.1 |
| Income-security services | 21.4 | 20.2 |
| Health services | 17.9 | 17.9 |
| SNAP | 14.3 | 14.3 |
| Education | 10.8 | 12.4 |
| Public order and safety | 10.7 | 10.7 |
| General government | 3.3 | 10.2 |
| Induced receipts | 12.0 | 7.9 |

The federal part is a cost under every convention.

**The benchmarks.** The same split on the other published benchmarks:
- *every service proportional:* 19.7–23.2% federal, $60.5–79.2bn;
- *non-school education also fixed:* 22.1–26.1%.

**The superseded incidence memo** found 10.7% federal on the −$263bn absolute balance, with
defense, net interest and general government at zero. It found 50.9% when those were charged per
capita. The adopted gap is a different concept (net cost to other residents, with general
government responding at 0.59–0.84), so its shares are not comparable line for line. Its
correctional-payer sensitivity (corrections 0 or 1 federal) is kept here as the low and high
treatment of the justice increment. That increment is $0.59–3.22bn federal.

## Where the stock comes from

Central rule, central convention; federal part of each year's gap, nominal $bn, low–high anchor:

| Year | 2005 | 2007 | 2008 | 2010 | 2012 | 2015 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| F_t | −0.8–6.3 | −5.4–3.3 | 23–31 | 72–81 | 48–58 | 30–41 | 23–37 | 138–151 | 158–174 | 39–59 | 42–62 | 39–58 |
| Federal share | −1–8% | −7–3% | 20–23% | 42% | 32–33% | 21–24% | 15–20% | 51–52% | 55–57% | 23–27% | 22–27% | 19–23% |

The stock, with interest to 2023, comes from four periods:
- 2008–2012 recession: 33–36%;
- 2013–2019: 24–27%;
- 2020–2022 pandemic: 34–37%;
- 2005–2007 and 2023: the remainder, with 2005–2007 at −1.5% to +1.8%.

In recessions the group's federal receipts fall with the national series and its benefits rise.
In 2020–2021 two further things happen:
- federal grants paid for a larger share of state-local services: the measured federal share of
  income-security services rose from 68% to 84%, of education from 5% to 10%, and of Medicaid from
  63% to 70% (the match increase); the programmes behind them were mainly school relief and rental
  assistance [TRAINING-DATA];
- unemployment insurance and SNAP spiked.

[CALCULATION: `derived/federal_gap_annual.csv`, `derived/federal_shares_by_year.csv`]

## Every specification

Each table varies one choice from the central specification. The four columns are the stock
entering FY2024 ($bn), 2024 interest ($bn), interest per member and interest per other resident,
each as low–high anchor.

**Back-cast rules** (central convention, effective rates, 2005–, all borrowed):

| Rule | Stock | Interest | Per member | Per other resident |
|---|---:|---:|---:|---:|
| Programme, income-adjusted, pandemic credits per head (central) | 943–1,202 | 30.5–38.9 | $745–950 | $102–130 |
| Programme, income-adjusted | 1,081–1,324 | 35.0–42.8 | $855–1,047 | $117–143 |
| Programme, income-adjusted, 2020–21 at the 2019/2022 mean | 731–989 | 23.6–32.0 | $578–782 | $79–107 |
| Programme, pandemic credits per head | 451–737 | 14.6–23.8 | $357–583 | $49–80 |
| Programme (September 20 rule) | 590–860 | 19.1–27.8 | $467–680 | $64–93 |
| Programme, 2020–21 at the 2019/2022 mean | 237–522 | 7.7–16.9 | $187–413 | $26–56 |
| Whole budget, flat | 601–909 | 19.4–29.4 | $475–718 | $65–98 |
| Whole budget, ratio | 493–752 | 15.9–24.3 | $390–595 | $53–81 |
| Whole budget, income | 653–950 | 21.1–30.7 | $516–751 | $71–103 |
| Whole budget, ratio, federal series | 334–591 | 10.8–19.1 | $264–467 | $36–64 |
| Whole budget, income, federal series | 887–1,143 | 28.7–37.0 | $701–904 | $96–124 |

**Payer convention** (central rule):

| Convention | Stock | Interest | Per member | Per other resident |
|---|---:|---:|---:|---:|
| Central | 943–1,202 | 30.5–38.9 | $745–950 | $102–130 |
| Low | 642–895 | 20.8–28.9 | $508–707 | $69–97 |
| High | 1,059–1,369 | 34.2–44.3 | $837–1,083 | $114–148 |

**Window** (central rule):

| Gaps from | Stock | Interest | Per member | Per other resident |
|---|---:|---:|---:|---:|
| 2005 (central) | 943–1,202 | 30.5–38.9 | $745–950 | $102–130 |
| 2010 | 858–1,060 | 27.8–34.3 | $679–838 | $93–115 |
| 2015 | 545–687 | 17.6–22.2 | $431–543 | $59–74 |

**Rate path** (central rule):

| Rates | Stock | Interest | Per member | Per other resident |
|---|---:|---:|---:|---:|
| Effective (central) | 943–1,202 | 30.5–38.9 | $745–950 | $102–130 |
| Constant 3.22% | 1,024–1,307 | 33.0–42.1 | $806–1,029 | $110–141 |
| 10-year Treasury | 963–1,228 | 40.9–52.2 | $1,000–1,275 | $137–174 |
| Securities held outside trust funds | 960–1,226 | 33.5–42.7 | $819–1,045 | $112–143 |

Effective rates in 2009–2022 were below 3.22%, so the constant rate compounds a larger stock. The
10-year path gives a similar stock but charges 4.25% in 2024.

**Financing** (central rule):

| Financing | Stock | Interest | Per member | Per other resident |
|---|---:|---:|---:|---:|
| All borrowed (central) | 943–1,202 | 30.5–38.9 | $745–950 | $102–130 |
| Half borrowed, half offset | 471–601 | 15.2–19.4 | $373–475 | $51–65 |

Every rule × convention × rate × window × financing cell is in `derived/stocks.csv`. The full
central-rule span is $6.4–59.4bn.

### The programme rule on the adopted anchor, for the back-cast memo

The memo says the programme version "has not been re-run on that anchor". Here it is, in the memo's
own concept: net cost to other residents without interest, $tn in 2024 dollars, low–high anchor.
[CALCULATION: `derived/adopted_backcast_windows.csv`]

| Rule | 2015–2024 | 2010–2024 | 2005–2024 |
|---|---:|---:|---:|
| Programme | 2.02–2.42 | 2.82–3.39 | 3.31–4.04 |
| Programme, income-adjusted | 2.29–2.68 | 3.34–3.89 | 4.04–4.73 |
| Both with 2020–21 at the 2019/2022 mean | 1.63–2.31 | 2.43–3.53 | 2.93–4.37 |
| Both with pandemic credits per head | 1.87–2.54 | 2.67–3.76 | 3.16–4.60 |
| Whole budget: flat, ratio, income | 1.75–2.49 | 2.52–3.74 | 3.00–4.62 |

- The whole-budget row reproduces the memo's adopted figures.
- The September 20 method carries receipts by Table 3.1 group; this lane carries them by own-government
  series. The grouped method is $0.01–0.02tn higher over any window.
- On the every-service-proportional benchmark the programme rule gives $5.02–5.53tn over
  2005–2024.

## Overlap ruling

1. **Main case.** Existing interest responds at zero, so the legacy line overlaps nothing in the
   adopted $203.2–249.6bn. If adopted, it is the response of the account's interest row. That row
   holds BEA domestic interest of $1,118.87bn, allocated per head as $134.54bn to the group.
   - The legacy line equals a response of 0.23–0.29 on that allocation.
   - It is 29–37% of the group's per-head share of OMB net interest, $105.8bn.
2. **Every service proportional.** This benchmark does not allocate interest.
   - `full_account_2026_09_20/welfare.py:77-78` subtracts only services and
     `public_response × public_goods_bn` (defense plus general government, $151.07bn).
   - The `legacy_interest_bn` pool ($134.54bn) is built at line 51 and never subtracted.
   - The explorer evaluator also keeps the interest class at zero in every profile.

   A legacy line may therefore sit beside this benchmark, but it must be the benchmark's own:
   **$41.1–49.1bn** on the central rule, from a stock of $1.27–1.52tn. The main case's
   $30.5–38.9bn belongs with the main case only.
3. **Assigned balance and the gap against the average resident.** Both concepts charge domestic
   interest per head. The legacy line must not be added to either; it would count interest twice.
4. **Never added.** The stock and the 20-year sum never enter an annual figure. The 2024 flow's own
   part-year interest ($0.6–0.9bn) belongs to the flow.

## Symmetry (rule 5)

- **Inside F_t:**
  - Induced receipts reduce F_t every year: F is $13.6bn and $8.9bn in 2024, federal at 86.2–88.4%
    by year, scaled with the group.
  - Every receipt line inside the back-cast, as a past fiscal benefit, reduces F_t at its
    government's share.
- **Never touch the debt:** social benefits beside the account. These are the production gain P,
  the consumer surplus on cheaper services, the insurance value of mobility and the private income
  from scale.
- **Omitted fiscal benefits** would reduce F_t if adopted. Their federal part is $3.33bn a year:
  - the care lane's three additive channels, $4.15bn;
  - the mobility lane's tax on today's earnings change, $0.03bn.

  Carried back by group size, they cut the stock by **$52bn** and 2024 interest by **$1.7bn**
  ($41 per member).
- **Adding the scale lane's proposed induced receipts** ($5.96bn; not adopted, 95% interval of the
  net −$57bn to +$84bn) raises the federal part to $8.60bn a year: −$134bn and −$4.3bn.

[CALCULATION: `derived/benefit_sensitivity.csv`; lane inputs hashed in `summary.json`]

## Forward counterpart

This follows ladder 137: a constant nominal flow borrowed at year end at 3.22%. The formula
reproduces ladder 137's table. Adopted federal flow, central convention, all borrowed, low–high
anchor:

| Years | Federal flow $38.6–58.4bn: debt | Interest in the debt | Interest bill that year | Whole gap as ladder 137 treated it: debt | Ladder 137 (−$263.2bn): debt |
|---:|---:|---:|---:|---:|---:|
| 10 | $448–677bn | $61–92bn | $13–19bn | $2.35–2.89tn | $3.05tn |
| 20 | $1.06–1.61tn | $289–437bn | $32–48bn | $5.58–6.86tn | $7.23tn |
| 30 | $1.91–2.88tn | $746–1,129bn | $58–88bn | $10.0–12.3tn | $12.98tn |

The whole-gap column borrows the state-local part too, which the brief's framing excludes. Half
borrowed halves every federal figure. [CALCULATION: `derived/forward_path.csv`]

## Before 2005

The ACS group series starts in 2005, so earlier years are not computed.
- Under the programme rules the federal part in 2005–2007 is −$26bn to +$6bn a year. It is a
  surplus under the September 20 programme rule and near zero under the central rule.
- Before 2005 the group was smaller: 26.8m in the 2005 ACS.
- Federal programmes cost less per resident then, and the federal budget ran surpluses in
  FY1998–2001 [TRAINING-DATA].
- Effective rates were higher: 4.1–4.8% in FY2005–2008, and higher in the 1990s [TRAINING-DATA].
  Whatever balance existed would therefore compound faster.

[INFERENCE] The late-1990s federal part was probably small or negative, and 2002–2004 probably
positive. The sign of the pre-2005 legacy is not determined. It is most likely small next to the
2008–2023 contributions. Computing it needs a group series from the CPS or the 2000 census.

## Where the data contradict the framing

1. **State-local governments are not balanced in NIPA terms.** Their 2024 net saving was −$178.7bn
   and net lending −$260.1bn, mostly pension accrual and capital (BEA Table 3.3 lines 29, 32, 44).
   Balanced-budget rules bind operating budgets. The lead's no-legacy framing for state-local gaps
   is kept, but it is an assumption. State-local interest ($274.6bn) sits in the account's
   interest row.
2. **The federal side ran a surplus on the group in 2005–2007** under the September 20 programme
   rule: −$9.7bn to −$26.3bn a year.
3. **The federal share is not stable.** It ranges from −7% to 57% by year, so the whole-budget
   rules' fixed 2024 share is a real simplification. The programme rules avoid it.
4. **The brief's formula** multiplies r_2024 by a stock that already includes 2024 interest. This
   lane uses the stock entering 2024 (see Method).

## Limits

- **Relative use of each programme** is held at 2024 in every year. The group was younger (median
  age 25.7 in 2008 against 29.8 in 2024), so it had more pupils and fewer retirees per head than
  that implies. The bias direction is unknown.
- **Federal shares are national.** The group's own federal Medicaid share is lower where states
  fund coverage for undocumented residents alone. California's Legislative Analyst puts that
  spending at $10.8bn General Fund in 2025-26, about 1.7m enrollees.
  [SOURCE: `sources/immigration-fiscal/data/external/state_medicaid/lao_may.txt`, lines 236–245]
  [INFERENCE] This overstates the 2024 federal flow by a few $bn and earlier years by less, since
  the expansion phased in from 2016 [TRAINING-DATA].
- **Classification mismatches.**
  - BEA grants by function differ from OMB programme classifications. OMB Table 12.3 is used only
    to separate block grants from matching grants.
  - BEA's economic-affairs grants were $160.8bn in 2020 and $258.0bn in 2021, against $10.3bn in
    2019; [INFERENCE] these are the general fiscal-relief funds. They exceed state-local spending on that function, and its federal
    share clips at 100%. The main case holds economic affairs fixed (its responsive
    employment-training line is $0.17bn), so only the proportional benchmark is touched, by a few
    percent.
- **Mixed receipt lines** keep their 2024 federal share: excise, other social contributions and
  transfers from persons.
- **Timing.** Fiscal-year rates are paired with calendar-year gaps. Borrowing is at year end.
- **Unpropagated inputs.**
  - The account's own statistical error, about $12bn per case, is not propagated.
  - The dataset audit's −$29bn to +$3bn (ladder 204) is not adopted and not applied.
  - The group count before 2024 is the back-cast's ACS series.
- **What the result is.** These are conditional accounting attributions on a resident-stock
  account, not the effect of an admission policy.

## Reproduce

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/debt_legacy_2026_09_23/debt_legacy.py
```

Two consecutive runs exited 0 and wrote byte-identical outputs: all 10 files in `derived/`, compared
by SHA-256. The script stops with `[BLOCKED]` on any failed gate:
- **Input pins:** SHA-256 of the BEA, OMB (3.1, 3.2, 7.1, 12.3), NHEA and FRED files. The brief's
  cached OMB copies are byte-identical to those used here.
- **Anchors and splits:**
  - the adopted and published bands are rebuilt;
  - each fiscal gap equals cost + P;
  - justice and uncompensated care rebuild their adopted amounts.
- **Back-cast:**
  - the September 20 programme control reproduces to 5.0e-5bn;
  - every rule reproduces its 2024 split;
  - the per-head and grouped variants change only the years they should.
- **Forward formula:** ladder 137's table is reproduced to within $1bn.

Outputs in `derived/`:

| File | Contents |
|---|---|
| `federal_split_2024.csv`, `federal_split_2024_lines.csv` | the 2024 split |
| `federal_gap_annual.csv` | F_t by benchmark, rule, anchor, convention and year |
| `stocks.csv` | 3,168 specifications |
| `adopted_backcast_windows.csv` | net-cost windows |
| `benefit_sensitivity.csv` | the rule 5 sensitivity |
| `forward_path.csv` | the forward counterpart |
| `federal_shares_by_year.csv` | federal share by line and year |
| `rates.csv` | the four rate paths |
| `summary.json` | input hashes, gates and parameters |

Raw pulls in `_cache/` (ignored) are OMB Tables 3.2, 7.1 and 12.3 (FY2027 edition) and FRED GS10.

**Files read:**
- **Model and main case:** the explorer's `model.json` and `engine.js`, and the main case's
  `inputs.json` and bands.
- **Complete account:** `welfare.py` and `response_pools.csv`, the spending lane's
  `categories.csv`, and the back-cast lane's scripts and derived files.
- **Lanes feeding the split:** the justice and uncompensated-care lanes' summaries.
- **Benefit lanes:** care, scale and mobility summaries.
- **Earlier work:** the incidence and ladder 137 lanes.

**Not read:** the fingerprinted `ledger_absolute_2026_09_17` and `gen_ledger_extension_2026_09_16`
`.py` files, which were not needed.

[INSTRUMENT] This is LLM-assisted modelling on a politically charged topic. The central rule is a
choice. Every alternative is tabulated, and each input is inspectable.

claude-opus-5-5[1m], lane agent, 2026-09-23.
