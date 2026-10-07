**2026-09-30 source-verification correction:** The historical calculations below are conditional financing attributions. The convention called cash replaces Social Security and Medicare accrual with benefits paid, but still compounds NIPA consumption containing accrued public-employee compensation. It has not been fully reconciled to Treasury cash borrowing. The accrual alternative capitalizes promises as if borrowed. Do not add either to the public-employee pension legacy without a common financing bridge. The verified comparator results, 2005 reporting window and scope ruling are in the [comparison lane](../legacy_comparators_2026_09_30/RESULT.md), [source verification](../legacy_comparators_2026_09_30/verification-2026-09-30.md) and [decision](../../../decisions/2026-09-30-legacy-comparisons-separate.md). Earlier dated results below remain preserved.

**Verdict:** [2026-09-27: the script now defaults to the main case of that day (`--case sept27`) and compounds cash flows only. 2024 interest is **$30.9–41.6bn** ($756–1,018 per member) on a stock of $0.96–1.29tn; the federal part of the 2024 cash gap is $37.3–62.2bn (13.2–19.1%). Two columns sit beside it and are never compounded: the return on public capital ($33.8–55.7bn, federal $0.83–1.74bn), an imputed resource cost, and the capped programs ($5.09bn, rental assistance and LIHEAP), which displace eligible households rather than cost a budget. `--case sept26_schools` reproduces 90c4b23. See "The September 27 case" below.] [2026-09-26, later: the script now defaults to the main case with schools at full cost (`--case sept26_schools`). The stock is $0.93–1.17tn, 2024 interest **$30.1–37.9bn** ($737–926 per member), and the federal share of the 2024 gap 14.1–19.0%. The school step is 8.2% federal under the central convention (1.0% low, 12.9% high); `derived/sept26_schools_bridge_2024.csv` walks it. `--case sept26` gives the one-year scenario, $28.2–36.3bn.] [2026-09-25: the script now defaults to the main case adopted September 24: stock $0.88–1.13tn, 2024 interest **$28.3–36.4bn** ($693–891 per member), federal share of the 2024 gap 15.9–21.1%; the programme back-cast gives $1.95–2.33tn over 2015–2024. `debt_legacy.py --case sept23 --out-dir DIR` reproduces the September 23 run this text describes, byte for byte (`test_debt_legacy.py`); per-correction federal parts are in `derived/corrections_federal_split_2024.csv`. See `../sept24_propagation_2026_09_24/RESULT.md`.] If the federal part of the group's 2005–2023 fiscal gaps was borrowed, the debt it left
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
  [2026-09-25: not as the interest row's response. The main case compares 2024 with and without
  the group, and removing the group in 2024 does not remove debt borrowed in 2005–2023; the line
  answers the historical question and, if adopted, enters as its own line. See Revisions.]

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
   adopted $203.2–249.6bn. If adopted, it is the response of the account's interest row
   [2026-09-25: withdrawn as the route in; see Revisions]. That row
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

## The September 27 case (2026-09-27)

`debt_legacy.py` defaults to `--case sept27`, the main case of 2026-09-27 (`../main_case_long_run_2026_09_27/`,
$321.82–387.37bn). `--case sept26_schools`, `sept26`, `sept24` and `sept23` rebuild 90c4b23, e62fccb, ed1b623
and 96a5c3b byte for byte (`test_debt_legacy.py`, 5 tests pass). Two default runs are byte-identical.

**The engine port.** The case adds four things to the schools case, and the Python port now sets both override
kinds engine.js has: a line's response (`economic_affairs_services`, `recreation_culture`, `housing_subsidies`)
and a receipt's (`receipt:enterprise_surplus`), from the payload's `meta.responses`. `capital_rows()` adds the
return on public capital from `meta.capital_return`, 24 components, each stock × rate × key × response, with keys
and responses read on the corner's own evaluation, as `main_case.cjs` `independentCosts()` does. The case's
profiles are its own (`long_run_non_school_full`, `long_run_non_school_fixed`, `proportional_reference`).
`per_spec_gates()` checks the port at all 64 specifications against the methods' mean of `per_spec.csv`:

| Check | Largest difference | Tolerance |
|---|---:|---:|
| cost and engine cost | 2.3e-13 | 1e-6 |
| capital return in total, by level, by part and by component | 1.4e-14 | 1e-9 |
| enterprise receipt's response, group amount and cost; the three lines' responses and group amounts | 7.1e-15 | 1e-9 |
| the receipt alone at 1 (no other override, no capital) moves the cost by `enterprise_surplus_receipt_cost_bn` | 1.9e-14 | 1e-9 |
| federal plus state and local, over cash, displaced beneficiaries and the capital return, equals cost + P (every specification and payer convention) | 2.3e-13 | 1e-6 |
| capital's federal and state-local parts equal the by-level columns | 1.4e-14 | 1e-9 |
| `main_case_bands.csv` `adopted` and `uncorrected_at_adopted_responses`, all three profiles | 4.9e-5 | 1e-4 (the file's rounding) |

The corners reproduce `summary.json`'s `main_case` and `uncorrected_at_adopted_responses` bands for every profile
(1e-6), and the main profile's corners are the case's end specifications (48 low, 11 high). The payload gate now
admits the enterprise receipt's 8 re-key edits after the September 26 edits; they are the component
`enterprise_rekey`. [CALCULATION: `derived/summary.json` `case.per_spec_gates`]

**Three columns (audit §1; brief correction of 2026-09-27).** Only cash is compounded into debt.

| 2024, main profile, central convention, $bn | Low end | High end | Federal part, low / high |
|---|---:|---:|---:|
| Cash financing: the engine's lines less the capped programs | 282.69 | 326.43 | 37.26 / 62.21 |
| of which the enterprise surplus receipt (its own row) | 5.56 | 5.56 | 0.21 / 0.21 |
| Resource cost: the return on public capital, never compounded | 33.80 | 55.69 | 0.83 / 1.74 |
| Displaced beneficiaries: rental assistance and LIHEAP, never compounded | 5.09 | 5.09 | 5.05 / 5.05 |
| Sum: net cost + P | 321.58 | 387.21 | |

Under the low convention the displaced federal part is $4.53bn (LIHEAP's grant counts as state-local), and the
cash federal part is $10.49 / 35.40bn; under the high convention $49.47 / 80.55bn. [CALCULATION:
`derived/federal_split_2024.csv`, `derived/federal_split_2024_lines.csv` (column `financing`; the capital
components are rows with side `capital_return`)]

**Federal shares of the new lines.**
- *Long-run roads and parks*: each subfunction in `responses.json` takes its level. Federal subfunctions are
  federal. State-local ones are federal only through grants, at the function's grant share of state-local
  consumption and benefits (the lines' central rule), and 0 under the low convention. The subfunctions blend
  to the line's response at every corner (1e-12), and their national amounts are NIPA 3.17's federal and
  state-local consumption (180.2 and 271.7; 5.4 and 48.9). At the low reading the federal subfunctions are held
  fixed, so economic affairs is $1.00bn federal of $13.99bn; at the high reading $6.35bn of $23.27bn. A gate
  checks the levels against NIPA 3.17 (1e-6).
- *Enterprise surplus*: t32(23) / t31(19), −$1.822bn of −$47.46bn in 2024, 3.84%. The programme rule carries each
  level with its own series (NIPA 3.2 line 23, 3.3 line 22). The federal enterprises had a surplus in 2005–2009
  and 2016–2022, so the federal part changes sign in those years. The receipt follows population, so the income
  rule does not scale it, as in the back-cast.
- *Rental assistance*: federal (NIPA 3.13 line 4). *LIHEAP*: the existing energy-assistance share (92.1% in
  2024; 0 under the low convention).

**Bridge from the schools case** (`derived/sept27_bridge_2024.csv`, central convention, $bn, low / high end):

| Step | Cash | Federal cash | Resource cost (federal) | Displaced (federal) |
|---|---:|---:|---:|---:|
| Schools case | 258.25 / 291.80 | 36.49 / 55.44 | | |
| LIHEAP leaves the cash gap | −0.56 / −0.56 | −0.52 / −0.52 | | +0.56 (0.52) |
| Long-run road and park responses | +19.44 / +29.63 | +1.08 / +7.07 | | |
| Rental assistance at 1 | | | | +4.53 (4.53) |
| Capital return, core | | | +15.99 / +25.78 (0.63 / 1.08) | |
| Capital return, roads and parks | | | +6.18 / +12.47 (0 / 0.36) | |
| Enterprise surplus receipt at 1 | +5.56 / +5.56 | +0.21 / +0.21 | | |
| Capital return, enterprises | | | +11.62 / +17.44 (0.20 / 0.30) | |
| Constant line's federal share | | +0.001 / +0.0002 | | |
| September 27 case | 282.69 / 326.43 | 37.26 / 62.21 | 33.80 / 55.69 (0.83 / 1.74) | 5.09 (5.05) |

Gates: each step moves only its own lines (1e-9); each step's total is the case lane's
`change_at_fixed_specifications` part (1e-6); the steps add to the new split in every column (1e-9); the whole
moves by the lane's `change` (1e-6); the range ends do not move (both cases end at specifications 48 and 11).

**Annual flows.** The programme rules carry the cash lines only. The whole-budget rules take the back-cast's
concept less its capital return and rental assistance, each by its own series
(`../historical_backcast_2026_09_20/derived/case_parts_annual.csv`, new), and less LIHEAP, which sits in the base
and follows it at its 2024 share of the base's fiscal gap; the parts' 2024 values are this split's (1e-3, the
file's rounding). `summary.json` `case.whole_budget_rules` has the window sums of the two excluded columns.

**One input to flag.** NIPA 3.17 line 61, federal grants for economic affairs, is $160.8bn in 2020 and $258.0bn in
2021, against $9.7–22.0bn in every other year; probably the pandemic relief grants [INFERENCE]. The state-local
grant share of economic affairs is therefore 0.75 in 2020 and 1.0 in 2021 (1.12, capped), so the long-run lines'
state-local part counts as federal in those years. The case raises the 2020 and 2021 federal flows by $7.3bn and
$10.6bn at the low end (about 0 in 2019 and 2022) and by $14.2bn and $19.0bn at the high end ($4.3bn and $5.0bn in
2019 and 2022). With those two years at the 2019/2022 average increase, the 2024 interest is $30.3–40.8bn, $0.6 /
0.8bn lower
[CALCULATION: scratch, from `derived/federal_gap_annual.csv` and `derived/rates.csv`]. The ex-pandemic rules
(`programme_income_ex_pandemic`: $22.2–32.8bn) replace both years.

**A pre-existing gap, named and not repaired.** The engine compounds each year's current gap, whose spending
includes consumption of fixed capital; it does not compound gross investment or capital transfers. The 2024
federal bridge from current saving (−$1,874.5bn) to net lending (−$2,106.2bn) is −$231.8bn: gross investment
$450.9bn and capital transfers paid $211.0bn, less consumption of fixed capital $393.4bn, capital transfers
received $36.4bn and net sales of nonproduced assets $0.4bn (NIPA 3.2 lines 37, 42 and 45–49, gated to add up). It is a national diagnostic, not a group
correction, and no part of it is charged to the group here. [DATA: `derived/summary.json` `case.pre_existing_gap`]

Old (schools case, 90c4b23) → new; the full table is in `../sept27_propagation_2026_09_27/RESULT_lanes.md`:

| Quantity (central rule, central convention) | Schools case | Sept 27 | File |
|---|---:|---:|---|
| legacy interest, 2024, $bn | 30.14 to 37.87 | 30.93 to 41.63 | `derived/stocks.csv` |
| interest per group member, $ | 737 to 926 | 756 to 1,018 | `derived/stocks.csv` |
| legacy stock entering 2024, $bn | 932.4 to 1,171.4 | 956.8 to 1,287.7 | `derived/stocks.csv` |
| federal part of the 2024 (cash) gap, $bn | 36.49 to 55.44 | 37.26 to 62.21 | `derived/federal_split_2024.csv` |
| federal share of the 2024 (cash) gap, % | 14.1 to 19.0 | 13.2 to 19.1 | `derived/federal_split_2024.csv` |
| legacy interest across back-cast rules, $bn | 8.03 to 38.69 | 8.20 to 42.45 | `derived/stocks.csv` |
| legacy interest, every specification, $bn | −4.24 to 61.24 | −4.25 to 66.29 | `derived/stocks.csv` |
| legacy interest, proportional benchmark, $bn | 38.77 to 46.50 | 38.59 to 46.32 | `derived/stocks.csv` |

The proportional benchmark falls slightly: its roads and parks already responded at 1, and LIHEAP's federal part
leaving the cash gap outweighs the enterprise receipt's.

Files: `debt_legacy.py`, `test_debt_legacy.py`, 10 changed derived files and `derived/sept27_bridge_2024.csv`
(new); `rates.csv`, `benefit_sensitivity.csv` and the two earlier bridges are unchanged. For consumers: from
September 27 `federal_split_2024.csv` names the case's profiles (main `long_run_non_school_full`) and its
`fiscal_gap_bn` and `federal_bn` are the cash part; four columns hold the resource cost and the displaced
beneficiaries. The lines and per-correction files add a `financing` column.

## Revisions

- 2026-09-25 (weekly conceptual audit §8): the line stays beside the main case. Its proposed route,
  the interest row's response, puts a historical counterfactual (the 2005–2023 gaps never
  borrowed) inside a static one (2024 with and without the group), and removing the group in 2024
  leaves past debt in place. If the operator chooses the historical question (ladder 207's
  changelog), the line enters as its own history line. The audit's second objection, that domestic
  interest is a transfer among other residents, does not shrink the figure: if the debt displaced
  private capital, other residents lose the return on that capital, which is at least the interest;
  if foreigners hold it, the interest leaves the country. The size of either effect is not
  modelled. [INFERENCE] [Decision](../../../decisions/2026-09-25-weekly-audit-corrections.md).

## v4 case (sept29), 2026-09-29

claude-opus-5-5 (fork A of the v4 consumer lane "v4-debt-lane"). The case runs on the adopted lane
(`../main_case_2026_09_29/`, 40c4ba75): the set is its `derived/corrections.json`, and the cash set is the candidate's
`../main_case_candidate_v4_2026_09_29/derived/corrections_v4_cash.json`, which the adopted lane reads too (it writes no
cash payload). `SEPT29` in `debt_legacy.py` names the lane, the payloads, whether the lane writes the September 27
contract, the payload consumer, the headcount file and the printed bands in one place. Phase 1 ran on the candidate
lane; phase 2, below, switched to the adopted one and moved no number.

`debt_legacy.py --case sept29` writes `derived/sept29/` (16 files: the default run's 15 names for this case, plus
`sept29_bridge_2024.csv`). The default run (`--case sept27`, `derived/`) is unchanged, and so are the four earlier cases.
The sept27, sept26_schools and sept26 bridges in `derived/sept29/` are byte-identical to those in `derived/`.
[CALCULATION: `debt_legacy.py --case sept29` → `derived/sept29/`]

**Headline (central rule `programme_income_pandemic_per_head`, central payer convention, effective rate, 2005 window,
all borrowed; cash set compounded; low / high end, $bn).**

| Quantity | Sept 27 | Sept 29 | File |
|---|---:|---:|---|
| legacy interest, 2024 | 30.93 / 41.63 | **30.75 / 41.48** | `derived/sept29/stocks.csv` |
| interest per group member, $ | 756 / 1,018 (40.90m) | **774 / 1,044** (39.71m); 752 / 1,014 at 40.90m | same |
| legacy stock entering 2024 | 956.8 / 1,287.7 | **951.1 / 1,283.0** | same |
| federal part of the 2024 cash gap | 37.26 / 62.21 | **36.28 / 61.27** | `derived/sept29/federal_split_2024.csv` |
| federal share of the 2024 cash gap | 13.2% / 19.1% | **14.4% / 20.7%** | same |
| pension accrual beside, 2024, all federal, never compounded | — | **76.71 / 73.02** | same |
| legacy interest across the programme rules | 8.20 to 42.45 | 7.77 to 42.30 | `derived/sept29/stocks.csv` |
| legacy interest, every specification (programme rules) | −4.25 to 66.29 | −5.15 to 65.73 | same |
| legacy interest, proportional benchmark | 38.59 / 46.32 | 38.48 / 46.16 | same |

The 2024 cash gap falls by $31.2 / 30.4bn, mostly state-local: the long-run property taxes (−27.19) and public
housing's deficit leaving the cash gap (−4.72). The federal part falls $0.98 / 0.94bn: the IRS-matched income-tax key
(−2.91 / −2.71, with payroll compliance on the same line) outweighs production on the account's weights (+1.05 / +0.71)
and state pricing (+0.81). Per member rises because the divisor is now the headcount the account prices. [CALCULATION:
`derived/sept29/summary.json` `case.v4.headline_2024`; the Sept 27 column is `derived/stocks.csv` and
`derived/federal_split_2024.csv`]

**The engine port against engine.js (gate 2).** `engine_parity()` runs the candidate's `consumer.cjs` `evaluateAll`
(node; engine.js, model.json and the payload only) on each payload and compares every one of the 64 specifications:

| Payload | Band at 48 / 11, $bn | Largest difference: cost, engine cost | capital by component, P and F, every line's amount and response | Tolerance |
|---|---:|---:|---:|---:|
| set (with the pension accrual) | 371.414600 / 434.840959 | 1.1e-13 | 0 | 1e-9 |
| cash set | 294.701076 / 361.817482 | 2.8e-13 | 0 | 1e-9 |

Both bands equal the printed $371.4146 / 434.8410bn and $294.7011 / 361.8175bn at specifications 48 / 11 (5e-5, the
printing's rounding). The port applies engine.js's three optional parts as it does (receipt lines, the national-scale
edits in payload order, the production grid; its dimensions compared as JSON.stringify compares them, since
JavaScript writes 1.0 as 1), sets every `meta.responses` entry as `consumer.cjs` `lineResponses` does, and reads the
`part_rekeyed` capital key. The adopted lane's own files gate the port as well (phase 2, below). [CALCULATION:
`derived/sept29/summary.json` `case.v4.engine_parity`]

**Four columns (only cash is compounded).** The corners are the set's end specifications (48 and 11 on the main profile);
the cash set is split at the same corners (a gate: its own ends are the same specifications, every profile).

| 2024, main profile, central convention, $bn | Low end | High end | Federal part, low / high |
|---|---:|---:|---:|
| Cash financing: the cash set's lines less the capped programs | 251.46 | 296.07 | 36.28 / 61.27 |
| Resource cost: the return on public capital, never compounded | 34.42 | 57.17 | 0.83 / 1.76 |
| Displaced beneficiaries: rental assistance, LIHEAP and public housing, never compounded | 8.13 | 8.13 | 5.05 / 5.05 |
| Pension accrual: the set less the cash set, never compounded | 76.71 | 73.02 | 76.71 / 73.02 |
| Sum: the set's net cost + P | 370.72 | 434.38 | |

Under the low convention the cash federal part is $9.06 / 33.95bn (displaced $4.53bn), under the high one $47.73 /
78.86bn. The accrual is on three lines, all federal: social security +53.15 / +49.73, Medicare +21.47 / +21.47 (the
Part A accrual is fixed) and the tax on benefits +2.09 / +1.82. [CALCULATION: `derived/sept29/federal_split_2024.csv`,
`derived/sept29/federal_split_2024_lines.csv`, side `pension_accrual`]

**Rules designed for this case, each with its alternative.**

1. *Cash against accrual (the directive's choice, made here).* The pension switch values social security and Medicare
   Part A at the benefits the group's 2024 payroll taxes earn, payable later, instead of the benefits paid in 2024.
   That is a liability accruing in 2024, not a 2024 cash flow, so nothing of it is borrowed in 2024. **Rule:** the split,
   the annual flows and the stocks run on the cash set; the accrual (set less cash set, line by line) is a fourth
   column beside, never compounded. Identity gate: cash + resource cost + displaced + accrual = the set's net cost + P
   (1e-6), at every corner and convention. **Alternative** (benchmark `main_with_accrual`, programme rules only): the set
   compounded, the accrual carried back with its lines' own series as if it had been borrowed each year. It gives
   **$61.27 / 70.53bn** of 2024 interest on a stock of **$1,895.1 / 2,181.4bn** ($1,543 / 1,776 per member): the accrual
   adds $30.52 / 29.05bn of interest and $943.9 / 898.4bn of stock. [FRAMING-SENSITIVE] Compounding the accrual counts
   benefits not yet paid as if the Treasury had borrowed for them each year since 2005.
2. *Public housing's enterprise deficit* (receipt line `housing_enterprise_surplus`, at the rental line's key, response
   1). **Rule:** a capped program like rental assistance: its units go to eligible households without the group, so
   there is no budget response and nothing is borrowed (displaced beneficiaries, $3.43bn, $0.40bn of it federal).
   **Alternative** (benchmark `main_housing_as_cash`): the line in the cash gap, carried with NIPA 3.13 line 4 and 3.8
   line 13, not scaled by income: 2024 interest $30.92 / 41.64bn (+$0.16 / 0.16bn), stock $956.2 / 1,288.0bn.
3. *Federal shares of the lines the case adds or re-scales* (`v4_shares`, in every convention unless noted; 2024):
   - `modeled_owner_property`, `tenant_occupied_property`, `personal_property_tax`: 0, state-local property taxes (NIPA
     3.3 line 9, 3.4 line 11). The first and third respond for the first time (0.763 and 1); the second is new (0.708).
   - `housing_enterprise_surplus`: 11.5%, the $5.258bn operating subsidy that left rental assistance (federal, NIPA
     3.13 line 4) over the line's −$45.556bn; the $40.298bn deficit that left the enterprise surplus is state-local (NIPA
     3.8 line 13, gated). Alternative: the enterprise surplus's September 27 share, 3.84% (−$0.26bn on the displaced
     federal part; nothing compounded either way).
   - `enterprise_surplus`: the line's key times the federal enterprises' surplus, t32(23) = −$1.822bn, which the split
     leaves in the line: 25.4% of the line after the split (−$7.162bn), 3.84% before it. The re-key edits move the key
     at the share before the split; the national-scale edit, which removes a state-local deficit, moves no federal
     dollars (so item 1 moves the federal cash part by 0, in the bridge and in the corrections file alike). Alternative:
     the September 27 share 3.84% on the split line, $0.18bn less federal a year.
   - `housing_subsidies` (re-scaled to $55.003bn): federal, as before.
   - `roads_vmt_fed`: 1 (federal highways). `roads_vmt_sl`: state-local highways, federal only through grants at
     economic affairs' state-local grant share, 7.1% (0 under the low convention), as `long_run_fraction` splits the
     state-local subfunctions.
   - `state_price_<line>`: the state-price gaps are state-local spending, federal only through the grants each
     convention gives state-local consumption of the function: public order 0.8%, recreation 1.6% (0 under the low
     convention), health 41.9% (29.0% low; 0 high, because the high convention puts every health grant on Medicaid).
   The programme rule carries each synthetic line with its parent's national series (`SYNTHETIC_CARRY`) at its own
   federal share by year; the property taxes with the state-local property-tax series; the enterprise surplus with NIPA
   3.2 line 23 (federal) and 3.8 lines 8–12, 14 and 15 (state-local without housing, gated to add to 3.3 line 22 less
   line 13). NIPA 3.17 line 61's 2020–2021 economic-affairs grants (flagged in the September 27 section) also raise
   `roads_vmt_sl`'s federal share in those two years.
4. *Per member.* The headcount the account prices, audit row 4's union, 39,712,493 (the adopted case's divisor,
   `main_case_candidate_2026_09_28/derived/production_row4.json`, gated to the account's 40.9m target). Per-head shares
   (OMB net interest, the debt increase, the pandemic credits) stay at the account's population key, 40.9m / 340.1m,
   as its population-keyed lines and the back-cast's group series do.

**Bridge from September 27** (`derived/sept29/sept29_bridge_2024.csv`, central convention, $bn, low / high end). Each
line's move is assigned to the items that move it (`meta.candidate_v4.items_by_line`); a line two items move is one
step named for both.

| Step | Cash | Federal cash | Resource cost (federal) | Displaced (federal) | Accrual |
|---|---:|---:|---:|---:|---:|
| September 27 case | 282.69 / 326.43 | 37.26 / 62.21 | 33.80 / 55.69 (0.83 / 1.74) | 5.09 (5.05) | |
| 1: public housing's deficit at the rental key | −4.72 | 0 | | +3.03 (0) | |
| 2: production on the account's weights (F) | +1.18 / +0.81 | +1.05 / +0.71 | | | |
| 3 + 6a: IRS-matched income-tax key, payroll compliance (federal income tax) | −2.91 / −2.71 | −2.91 / −2.71 | | | |
| 4: public housing's capital at the rental key | | | −0.35 / −0.53 (0) | | |
| 5: long-run property taxes | −27.19 | 0 | | | |
| 6a: payroll compliance (payroll taxes) | +0.56 / +0.60 | +0.64 / +0.66 | | | |
| 6a + roads (excise) | −1.58 / −1.58 | −0.43 / −0.42 | | | |
| 6a + state (general sales tax) | −5.96 | 0 | | | |
| 7: workers' compensation, pooled | −0.95 / −0.73 | −0.30 / −0.24 | | | |
| roads keyed by miles | +2.24 / +3.06 | +0.16 / +0.24 | +0.98 / +2.01 (0 / 0.02) | | |
| state pricing | +8.58 / +8.64 | +0.81 / +0.81 | | | |
| state + roads (motor-vehicle licences) | −0.49 / −0.59 | 0 | | | |
| constant line's federal share | | −0.001 | | | |
| pension accrual | | | | | +76.71 / +73.02 |
| September 29 case | 251.46 / 296.07 | 36.28 / 61.27 | 34.42 / 57.17 (0.83 / 1.76) | 8.13 (5.05) | 76.71 / 73.02 |

Gates: the September 27 corner reproduces its split (1e-9); every line that moves has an item, and none changes
financing; at the matched specification the steps add to its split in every column (1e-9); the whole moves by the set's
band change plus the change in P (1e-6); the range ends do not move (both cases end at 48 and 11). Items 1, 4, 5 and 7
match the candidate's alone-columns exactly (−1.691, −0.353 / −0.529, −27.186, −0.948 / −0.732); item 2's total with P
is its +1.643 / +1.107. `derived/sept29/corrections_federal_by_component_2024.csv` splits the payload's edits the same
way, at the case's responses (items `v4_<items>`; the production grid's change in F is item 2's row); property taxes
that already existed but did not respond enter there through `before`, so item 5 is −7.73 there and −27.19 here.

**Consumers.** `derived/sept29/federal_split_2024_lines.csv` lists every line of the case, the new ones included
(`roads_vmt_fed` responds at 0 at the low end and is absent there, as other zero-response lines are), the capital
components (side `capital_return`) and the accrual (side and financing `pension_accrual`, federal = gap). The production
row is −F at the induced-receipt share. `winners_losers_2026_09_24` stops on the financing value `pension_accrual`
until it maps it (or drops those rows when it evaluates the cash set).

**[DEGRADED] Not run for sept29: the whole-budget rules** (whole_flat, whole_ratio, whole_income and their
federal-series variants). They take the back-cast's concept less the parts that are not cash. The back-cast's sept29
concept is the set, the pension accrual included, being written to `../historical_backcast_2026_09_20/derived/sept29/`
on 2026-09-29 by another lane; the rules need its parts by financing column (the capital return, rental assistance,
public housing and the accrual). For sept27 the whole-budget rules lay inside the programme rules' range (8.20 to
42.45), so the headline and the ranges above do not depend on them. [DATA: `derived/sept29/summary.json`
`case.whole_budget_rules.not_run`] [Resolved later the same day: the back-cast's sept29 parts landed at c4dd711 and
the rules now run on this case; see "Whole-budget rules on sept29" below. `not_run` has left `summary.json`.]

### Phase 2: the adopted lane (2026-09-29)

`SEPT29` now points at `main_case_2026_09_29` (40c4ba75) and reads its September 27 contract. The payloads:
- **the set:** `main_case_2026_09_29/derived/corrections.json`. A gate in `case_payload` checks that it is the
  candidate's `corrections_v4.json` in everything but the adoption's five meta stamps (source, adopted, decision, case,
  status), and that `adopted` is set. A positive control, pointing the gate at the cash payload, stops it.
- **the cash set:** the candidate's `corrections_v4_cash.json`. The adopted lane writes no cash payload: its
  `main_case.cjs:78` reads the same file and gates it against its package's pension4 "cash" option.

The adopted lane's files gate the port as they gate sept27 (`per_spec_gates`, `v4_anchors`, `case_split`):

| Check against `main_case_2026_09_29/derived/` | Largest difference | Tolerance |
|---|---:|---:|
| `per_spec.csv`, methods' mean, 64 specifications: cost and engine cost | 2.8e-13 | 1e-6 |
| capital return in total, by level, by part and by component | 1.4e-14 | 1e-9 |
| enterprise receipt's response, amount and cost; the three lines' responses and amounts | 7.1e-15 | 1e-9 |
| the receipt alone at 1 | 1.1e-15 | 1e-9 |
| federal plus state and local equals cost + P (every specification and convention) | 1.7e-13 | 1e-6 |
| capital's federal and state-local parts | 7.1e-15 | 1e-9 |
| `main_case_bands.csv`: `adopted` and `uncorrected_at_adopted_responses` (three profiles), `cash_set` (main profile) | 4.1e-5 | 1e-4 (the file's rounding) |
| `summary.json`: `main_case`, `uncorrected_at_adopted_responses` and `other_profiles`; `cash_set` band | within 1e-6 | 1e-6 |
| `summary.json` `end_specifications` (both methods) and `cash_set` ends | 48 / 11 | exact |

The uncorrected model here is model.json. The adopted package adds the payload's two receipt lines and eight
correction lines to it at zero, which adds nothing to a cost or a capital key, and the uncorrected bands match. Every
CSV in `derived/sept29/` is byte-identical to phase 1; only `summary.json` changed (the lane, the payload files and
hashes, `bands_source` and the new `per_spec_gates`). [CALCULATION: `derived/sept29/summary.json`
`case.per_spec_gates`, `case.v4.payloads`]

### Whole-budget rules on sept29 (2026-09-29, later)

The back-cast's concept for this case and its parts by line landed at c4dd711
(`../historical_backcast_2026_09_20/derived/sept29/`). The whole-budget rules now run on sept29 for the main and
proportional benchmarks, as on September 27. `backcast_case()` reads the concept's tag and directory from the
back-cast's own case table. A gate checks that the group and income series there are the ones `History` reads, so
only the concepts come from the new directory.

**Designed rule: the cash part of the set's concept.** The back-cast carries the set, the pension accrual included,
with v4's change line by line. `cash_whole()` takes out each part that is not cash, on the series the back-cast
carries it with:
- the capital return (resource cost), as on September 27;
- the displaced beneficiaries: rental assistance with its v4 change (`v4_housing_subsidies`), public housing's
  deficit (`v4_housing_enterprise_surplus`), and LIHEAP, which follows the base at its 2024 share of the base's fiscal
  gap. The base carries September 27's P, so that share uses P less the production grid's change;
- the pension accrual, line by line as `accrual_rows` splits it:
  - social security's and Medicare Part A's accrual parts, less the benefits they no longer charge;
  - the tax on benefits ($2.09 / 1.82bn in 2024), which has no part of its own. It sits inside
    `v4_federal_income_tax`, so it leaves at its 2024 amount on that part's series. A gate checks that the part follows
    one series at both band ends.

What is left is the cash set carried back line by line. The series the set's concept gives the tax on benefits does
not matter: taking the tax out on the same series leaves only the cash set's own lines. Splitting the tax into a part
of its own (the back-cast's README names that option) would leave the cash part unchanged. Gates (1e-3, the file's
rounding): the parts add to the concept, and in 2024 the cash part, the resource cost, the displaced beneficiaries and
the accrual (in total and on each of its three lines) are this split's. A case with two payloads whose whole-budget
rules do not run now stops the run, where it wrote `not_run` before.

Alternative, named and not run: the whole-budget rules on the set, with the accrual compounded as if borrowed. That is
the whole-budget form of the benchmark `main_with_accrual`, whose programme rules give $61.27 / 70.53bn of 2024
interest (above).

**Results** (central convention, effective rate, 2005 window, all borrowed; $bn, low / high end):

| Rule | Sept 27 interest | Sept 29 interest | Sept 29 stock entering 2024 |
|---|---:|---:|---:|
| programme_income_pandemic_per_head (central, unchanged) | 30.93 / 41.63 | 30.75 / 41.48 | 951.1 / 1,283.0 |
| whole_flat | 18.73 / 31.27 | 18.24 / 30.80 | 564.0 / 952.6 |
| whole_ratio | 15.52 / 26.11 | 14.92 / 25.48 | 461.3 / 788.0 |
| whole_income | 18.76 / 30.79 | 18.46 / 30.56 | 570.9 / 945.2 |
| whole_ratio_federal_series | 10.90 / 21.33 | 10.45 / 20.91 | 323.3 / 646.6 |
| whole_income_federal_series | 26.55 / 36.98 | 26.21 / 36.67 | 810.8 / 1,134.2 |
| **all 11 back-cast rules, both ends** | **8.20 to 42.45** | **7.77 to 42.30** | |
| the five whole-budget rules alone | 10.90 to 36.98 | 10.45 to 36.67 | |
| every specification, main benchmark | −4.25 to 66.29 | −5.15 to 65.73 | |
| the whole-budget rules, proportional benchmark | 17.48 to 41.05 | 17.07 to 40.74 | |

As on September 27, the whole-budget rules lie inside the programme rules' range. The range across rules is therefore
the programme rules' range, **$7.8–42.3bn**; the INDEX printed $8.2–42.5bn for September 27. Each whole-budget rule
falls $0.23–0.63bn against September 27. The rules hold the 2024 federal share of the cash gap, and the federal part of
that gap falls $0.98 / 0.94bn (above). [CALCULATION: `debt_legacy.py --case sept29` → `derived/sept29/stocks.csv`, rows
`benchmark` main and proportional; the September 27 column from `derived/stocks.csv`]

Files: in `derived/sept29/`, `stocks.csv` gains 1,440 rows, `federal_gap_annual.csv` 1,200 and
`adopted_backcast_windows.csv` 36, all whole-budget rules; every committed row is unchanged and in place.
`summary.json` changes in 17 key paths, all under `case.whole_budget_rules` (the rule, the window sums with the
accrual beside, `not_run` gone), `case.lane_sha256` (the back-cast's sept29 `backcast_annual.csv` and
`case_parts_annual.csv`) and `case.v4.backcast_concept` (sept29). The other 12 files are byte-identical. The headline
does not move.

Reproduce (from the repository root; `test_debt_legacy.py` `test_sept29_rebuilds_its_directory` rebuilds it byte for
byte):

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/debt_legacy_2026_09_23/debt_legacy.py --case sept29
```

Log (append-only; times from `date`):
- 2026-09-29 15:33 JST: stub written. Phase 1 points the case at the candidate lane
  (`main_case_candidate_v4_2026_09_29`, payloads `corrections_v4.json` and `corrections_v4_cash.json`); phase 2 switches
  to `main_case_2026_09_29`. The default run (`--case sept27`, `derived/`) must stay byte-identical.
- 2026-09-29 17:00 JST: phase 1 done on the candidate lane. Gate 1: the default rerun (before `derived/sept29/`
  existed) is identical but for one line of `derived/summary.json`, the provenance hash of
  `main_case_long_run_2026_09_27/derived/main_case_bands.csv`, which b3f4d849 edited after this lane's last build; the
  same line differed before this change. pytest: 6 passed (with that line refreshed). Gate 2: parity with engine.js on
  both payloads, 64 specifications, largest difference 2.8e-13; the printed bands at 48 / 11. Gate 3: the lane's own
  gates pass on sept29. Gate 4: two `rerun_lane.py` passes with both commands, IDENTICAL, 36/36 files.
- 2026-09-29 17:12 JST: phase 2 done on the adopted lane (40c4ba75). The set is its `derived/corrections.json`, gated
  equal to the candidate's `corrections_v4.json` but for five meta stamps; the cash set is still the candidate's
  `corrections_v4_cash.json`. The adopted lane's `per_spec.csv`, `summary.json` and `main_case_bands.csv` gates pass
  (largest 4.1e-5 on the bands file, tolerance 1e-4; everything else ≤ 2.8e-13). No number moved: every CSV in
  `derived/sept29/` is byte-identical to phase 1. Gate 1: the default rerun is identical but for the same
  `derived/summary.json` provenance line as at 17:00. pytest: 6 passed with that line refreshed. Gate 4: two passes with
  both commands, IDENTICAL, 36/36. `derived/summary.json` is back to its committed bytes; the refreshed copy is in the
  session's scratchpad (`forkA/summary_default_refreshed.json`).
- 2026-09-29 20:43 JST (the lane, after the lead's revive): `derived/summary.json` now carries the refreshed copy. Its
  one changed line is the build-time hash of `main_case_long_run_2026_09_27/derived/main_case_bands.csv`, 6e550bd3… →
  46443c0c…, which is that file's sha256 since b3f4d849 (checked). Every CSV of the default run is unchanged. Gates after
  the refresh (20:32–20:42): two `rerun_lane.py` passes with both commands and `--allow-unrun` for the test file,
  IDENTICAL 36/36, rc 0 each; pytest 6 passed.
- 2026-09-29 21:09 JST (the lane, resumed after the machine rebooted at about 20:51; the gate logs above were lost
  with `/private/tmp`, so every gate was rerun and printed): the 16 pre-reboot files in `derived/sept29/` and
  `derived/summary.json` all parse. A fresh `--case sept29` run (21:04) wrote all 16 byte-identical to the pre-reboot
  files, so none was truncated. Gate 2 ran inside it: parity with engine.js on both payloads, 64 specifications,
  largest difference 1.1e-13 (the set) and 2.8e-13 (the cash set), tolerance 1e-9. Gate 3: the bands at 48 / 11 are
  $371.4146 / 434.8410bn and $294.7011 / 361.8175bn. Gates 1 and 4: two `rerun_lane.py` passes with both commands
  and `--allow-unrun` for the test file, IDENTICAL 36/36, rc 0 each (21:04–21:07). The default run's `derived/`
  differs from HEAD only in `summary.json`'s provenance line above. pytest: 6 passed.
- 2026-09-29 23:04 JST (the lane, after the lead's commit 7e1b500): the whole-budget rules run on sept29 (section
  above), from the back-cast's `derived/sept29/` at c4dd711. The new gates in `cash_whole` pass at both ends, every
  rule and both benchmarks: parts add to the concept; in 2024 the cash part, the resource cost, the displaced
  beneficiaries and the accrual on each of its three lines match the split; the benefit tax's part follows one
  series. Against HEAD, `derived/sept29/` changes in four files: three CSVs gain whole-budget rows only, with every
  committed row unchanged and in place, and `summary.json` in 17 key paths. The other 12 files are byte-identical,
  and the scratch and in-place runs agree 16/16.
  - Gate 1: pytest 6 passed. That covers the four earlier cases against their commits, the default run against
    `derived/` and sept29 against its directory. The default `derived/` equals HEAD.
  - `constant_choices.py` imports this script. The sept24_propagation pass is IDENTICAL 23/23, and its sept26,
    sept26_schools and sept27 files are identical to the tracked ones.
  - Gate 4: two `rerun_lane.py` passes with both commands, IDENTICAL 36/36, rc 0 each (22:55–23:04). Two earlier
    passes (22:33–22:35) flagged only this RESULT.md, which I was editing while they ran; every output was
    unchanged, 35/36.

## v5 case (oct05), 2026-10-05

claude-opus-5-5 (teammate v5consB of the v5 consumer lanes). [2026-10-05: on main case v5 (`oct05`), the 2024 legacy
interest on the central rule is **$30.63 / 42.62bn** on a stock of **$947.4 / 1,318.4bn**, **$716 / 997 per member** at
the lineage's 42.75m, against $30.75 / 41.48bn, $951.1 / 1,283.0bn and $774 / 1,044 at 39.71m for sept29. Across the
11 back-cast rules it is $5.76 to 43.42bn (sept29: 7.77 to 42.30).] The case is `../main_case_2026_10_05/` (`OCT05` in
`debt_legacy.py`): the September 29 case plus 3.04M descendants of Mexican immigrants who no longer report Mexican
origin, counted whole (`../main_case_lineage_2026_10_05/`, arm b). Both payloads are the lane's own
(`derived/corrections.json`, `derived/corrections_cash.json`). `debt_legacy.py --case oct05` writes `derived/oct05/`:
sept29's 16 file names plus `oct05_bridge_2024.csv`. Its four earlier bridges are byte-identical to those in
`derived/sept29/`. [CALCULATION: `debt_legacy.py --case oct05` → `derived/oct05/`]

**Headline** (central rule `programme_income_pandemic_per_head`, central payer convention, effective rate, 2005 window,
all borrowed; cash set compounded; low / high end, $bn):

| Quantity | Sept 29 | v5 (oct05) | File |
|---|---:|---:|---|
| legacy interest, 2024 | 30.75 / 41.48 | **30.63 / 42.62** | `derived/oct05/stocks.csv` |
| interest per group member, $ | 774 / 1,044 (39.71m) | **716 / 997** (42.75m) | same |
| legacy stock entering 2024 | 951.1 / 1,283.0 | **947.4 / 1,318.4** | same |
| federal part of the 2024 cash gap | 36.28 / 61.27 | **32.40 / 61.18** | `derived/oct05/federal_split_2024.csv` |
| federal share of the 2024 cash gap | 14.4% / 20.7% | **12.4% / 19.6%** | same |
| 2024 cash gap (all governments) | 251.46 / 296.07 | 260.71 / 312.28 | same |
| resource cost (federal) | 34.42 / 57.17 (0.83 / 1.76) | 37.15 / 61.86 (0.89 / 1.90) | same |
| displaced beneficiaries (federal) | 8.13 (5.05) | 8.81 (5.48) | same |
| pension accrual beside, all federal | 76.71 / 73.02 | 82.92 / 77.83 | same |
| legacy interest across the 11 back-cast rules | 7.77 to 42.30 | 5.76 to 43.42 | `derived/oct05/stocks.csv` |
| the five whole-budget rules alone | 10.45 to 36.67 | 8.33 to 37.80 | same |
| every specification, main benchmark (programme rules) | −5.15 to 65.73 | −8.90 to 67.78 | same |
| proportional benchmark | 38.48 / 46.16 | 38.96 / 47.68 | same |
| alternative: the set compounded (`main_with_accrual`) | 61.27 / 70.53 | 63.33 / 73.36 | same |
| alternative: public housing as cash | 30.92 / 41.64 | 30.81 / 42.80 | same |

The lineage adds $9.56 / 16.53bn to the 2024 cash gap, but it lowers the federal part by $3.89bn at the low end and
by $0.11bn at the high end (central convention). The added people pay more in federal taxes than they draw in federal
spending, so their net cost falls on state and local budgets: schools, Medicaid's state share and the long-run lines.
The legacy interest therefore barely moves at the low end and rises $1.14bn at the high end. Per member falls because
the divisor grows by 3.04m and the federal legacy does not. [CALCULATION: `derived/oct05/oct05_bridge_2024.csv`]

Whole-budget rules (central, low / high, interest $bn): whole_flat 16.22 / 30.56 (sept29 18.24 / 30.80); whole_ratio
13.32 / 25.38 (14.92 / 25.48); whole_income 16.37 / 30.19 (18.46 / 30.56); whole_ratio_federal_series 8.33 / 20.36
(10.45 / 20.91); whole_income_federal_series 25.76 / 37.80 (26.21 / 36.67). They lie inside the programme rules' range,
as before.

**Bridge from September 29** (`derived/oct05/oct05_bridge_2024.csv`, central convention, $bn, low / high end):

| Step | Cash | Federal cash | Resource cost (federal) | Displaced (federal) | Accrual |
|---|---:|---:|---:|---:|---:|
| September 29 case | 251.46 / 296.07 | 36.28 / 61.27 | 34.42 / 57.17 (0.83 / 1.76) | 8.13 (5.05) | 76.71 / 73.02 |
| the union's response move (group-size responses, row 8) | −0.31 / −0.32 | +0.005 / +0.010 | +0.01 / +0.003 | 0 | 0 |
| the lineage: the added people | +9.56 / +16.53 | −3.89 / −0.11 | +2.71 / +4.68 (0.06 / 0.13) | +0.69 (0.43) | +6.20 / +4.81 |
| v5 case | 260.71 / 312.28 | 32.40 / 61.18 | 37.15 / 61.86 (0.89 / 1.90) | 8.81 (5.48) | 82.92 / 77.83 |

Under the low convention the lineage's federal cash step is −5.98 / −2.27; under the high one −3.18 / +1.16.

**Rules this case needed** (each tagged; the Consumers row of `../main_case_2026_10_05/RESULT.md` asks for the case,
42.75m per member and the moved `meta.responses`):
1. *Shares at the case's own group size.* General government's low-end federal fraction follows the finite-removal
   responses at v5's s (0.1292 against 0.1202): 0.11434 against 0.11431 in 2024 (central). The earlier cases a run
   rebuilds for its bridges, September 29 included, keep September 29's shares (`later_state`), so their bridges are
   unchanged.
2. *The lineage's path* [ASSUMPTION]. The programme rules carry the union on its own series and the lineage (the case
   less its twin, the union at the case, every line, the induced receipts F and the constant line) on the identified
   third-plus generation's path. They use its population share where the union's lines use the union's, and its count
   where they use the group's size. This is the back-cast's choice (`../historical_backcast_2026_09_20/README.md`, v5
   case; `inputs/cps_g3plus_path.csv`). The path's share index is 0.655 in 2005 against the union's 0.789. The rule is
   linear in the lines' amounts, so the lineage's part is the rule on that path at the case less at the twin
   (`lineage_programme`; gate: the 2024 values are the case's, 1e-9). Carried on the union's own path instead, the
   central interest is $30.57 / 42.73bn (−0.06 / +0.11); the choice barely matters. The income rule scales the lineage's
   receipts by the union's relative income [ASSUMPTION: its own is not measured].
3. *The constant line.* Audit row 8's change at the larger group (−$0.008bn) splits and carries as row 8 (a
   `row8_finite` part, component `v5_union_response`). The added people's part of the line (−$0.19bn) is the union's
   parts in proportion, each with its part's share and series [APPROX: the generation account splits the line by one
   ratio per generation, not part by part]. The parts keep their names, so the ledger lane's choices in
   `../sept24_propagation_2026_09_24/constant_choices.py` reach them too.
4. *Per member and per head.* Per member is the lineage, 42,752,212.9 (`meta.lineage.counts.lineage_population`;
   gate: its union is audit row 4's). Per-head shares are taken at the case's population key,
   `meta.responses.general_government.s` = 0.12918 (40.90m + 3.04m over 340.11m; gate 1e-8): OMB net interest per head
   is $113.66bn (sept29 105.80), and the pandemic credits' per-head part gets the lineage's own share.
5. *Whole-budget rules.* The back-cast's oct05 concept, the set, carries the lineage's parts (`v5_`) on the same path.
   `cash_whole` takes them out as it takes out v4's. The lineage's rental assistance, public housing and LIHEAP go with
   the displaced beneficiaries; the base's LIHEAP share leaves out the lineage's own part. Its accrual parts go with
   the accrual. Its tax on benefits (the case's accrual on the income tax less the twin's) goes on
   `v5_federal_income_tax`'s series. [APPROX] P is added back on the union's group path for the whole case, as on
   September 29 for v4's change in P.
6. *The enterprise surplus.* The lineage's cell edits on the enterprise surplus follow the national-scale edit, so they
   move the key at the line's share after public housing's split (25.4%), not before (`post_scale`). Before this fix the
   corrections split missed the federal move by $0.014bn, and the gate stopped the run.

**Gates** (all pass; the run stops on any failure):
- `v5_parts`: September 29's payload comes first, unchanged, in both payloads; there are 336 lineage cell edits, two on
  the constant line, row 8's last at `row8_edit_bn`; production is on v4's dimensions; meta moves only the adoption
  stamps, responses, capital return and lineage; the responses are the lane's `summary.json`'s; the counts are the
  lineage lane's arm b.
- `v5_components`: September 29's model plus the lineage's edits rebuilds the case, cell by cell (1e-9).
- Parity with engine.js through the payload consumer, 64 specifications, both payloads: largest difference 1.7e-13
  (set) and 1.1e-13 (cash). Bands $390.2940 / 461.2431bn and $307.3764 / 383.4093bn at 48 / 11.
- The lane's `per_spec.csv`, `main_case_bands.csv` (largest 5.0e-5, tolerance 1e-4) and `summary.json` gates, as on
  September 29.
- `lineage_bridge`: the union step equals the lane's `union_response_move` (−0.298 / −0.315), and the lineage step its
  `g3plus_members + whites` plus the added people's P (1e-6). The whole moves by the set's band change plus P (1e-6).
- `cash_whole`: in 2024 the cash part, resource cost, displaced and accrual (each line and the total) are this split's
  (1e-3); `v5_federal_income_tax` follows one series at both ends.
- `derived/sept29/` and the default `derived/` rebuild byte for byte with the changed script; so does
  `constant_choices.py --case sept29` (its two CSVs).

Reproduce (from the repository root; `test_debt_legacy.py` `test_oct05_rebuilds_its_directory` rebuilds it byte for
byte):

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/debt_legacy_2026_09_23/debt_legacy.py --case oct05
```

Log (append-only; times from `date`):
- 2026-10-06 00:05 JST: `--case oct05` written to `derived/oct05/` (17 files; a scratch run gives the same bytes).
  `--case sept29` into a scratch directory is byte-identical to `derived/sept29/` (16/16), and so is the default run to
  `derived/` (15/15). pytest: 7 passed (the four old cases against their commits, the default, sept29, oct05).
  `rerun_lane.py` over the default, sept29 and oct05 commands, with `--allow-unrun` for the test file: IDENTICAL 53/53,
  exit 0. Not committed (the lead's brief).

## v6 case (oct07), 2026-10-07

claude-opus-5-5 (teammate prop-b of the v6 consumer lanes). [2026-10-07: on main case v6 (`oct07`), the 2024 legacy
interest on the central rule is **$31.82 / 44.17bn** on a stock of **$984.3 / 1,366.2bn**, **$744 / 1,033 per member**
of the lineage's 42.75m, against $30.63 / 42.62bn, $947.4 / 1,318.4bn and $716 / 997 for oct05. Across the 11
back-cast rules it is $6.84 to 44.95bn (oct05: 5.76 to 43.42).] The case is `../main_case_2026_10_07/` (`OCT07` in
`debt_legacy.py`), adopted 2026-10-07: the October 5 case plus four items from its registry (`meta.items`):
- `pension_tr2026`, the pension accrual on the 2026 Trustees' separate OASI and DI funds (set only);
- `retiree_health`, retiree health on accrual;
- `added_age_mix`, the 3.04M added people at their measured age mix;
- `user_fees`, user fees and the education keys, on the union only.

Both payloads are the case lane's (`derived/corrections.json`, `derived/corrections_cash.json`). `debt_legacy.py --case
oct07` writes `derived/oct07/`: oct05's 17 file names plus `oct07_bridge_2024.csv`. Its five earlier bridges are
byte-identical to those in `derived/oct05/`. [CALCULATION: `debt_legacy.py --case oct07` → `derived/oct07/`]

**Headline** (central rule `programme_income_pandemic_per_head`, central payer convention, effective rate, 2005 window,
all borrowed; cash set compounded; low / high end, $bn):

| Quantity | v5 (oct05) | v6 (oct07) | File |
|---|---:|---:|---|
| legacy interest, 2024 | 30.63 / 42.62 | **31.82 / 44.17** | `derived/oct07/stocks.csv` |
| interest per group member, $ | 716 / 997 | **744 / 1,033** | same |
| legacy stock entering 2024 | 947.4 / 1,318.4 | **984.3 / 1,366.2** | same |
| federal part of the 2024 cash gap | 32.40 / 61.18 | **34.04 / 63.83** | `derived/oct07/federal_split_2024.csv` |
| federal share of the 2024 cash gap | 12.4% / 19.6% | **13.0% / 20.3%** | same |
| 2024 cash gap (all governments) | 260.71 / 312.28 | 261.30 / 315.03 | same |
| resource cost (federal) | 37.15 / 61.86 (0.89 / 1.90) | 36.58 / 61.06 (0.89 / 1.90) | same |
| displaced beneficiaries (federal) | 8.81 (5.48) | 8.81 (5.47) | same |
| pension accrual beside, all federal | 82.92 / 77.83 | 81.68 / 76.12 | same |
| legacy interest across the 11 back-cast rules | 5.76 to 43.42 | 6.84 to 44.95 | `derived/oct07/stocks.csv` |
| the five whole-budget rules alone | 8.33 to 37.80 | 9.02 to 38.88 | same |
| every specification, main benchmark (programme rules) | −8.90 to 67.78 | −7.41 to 69.79 | same |
| proportional benchmark | 38.96 / 47.68 | 40.17 / 49.23 | same |
| alternative: the set compounded (`main_with_accrual`) | 63.33 / 73.36 | 63.97 / 74.19 | same |
| alternative: public housing as cash | 30.81 / 42.80 | 32.00 / 44.35 | same |

The items add $0.59 / 2.75bn to the 2024 cash gap and $1.64 / 2.65bn to its federal part (central convention).

- **User fees** move the most federal money, +4.01 / +4.10. Pell, keyed by the group's share of Pell grants, adds
  $3.87 / 3.97bn to federal spending. The federal parts of the health and education keys add +0.14 / +0.13. State and
  local budgets fall by 3.68 / 3.82, almost all of it from the education keys and the tuition credit.
- **The added people's measured ages** move federal cash down by $1.68 / 0.88bn and state and local cash up by
  $1.36 / 2.59bn. The later losses are younger: they draw less Social Security and Medicare (−$2.39 / 2.48bn), pay less
  federal income tax (+$0.51 / 1.13bn) and use more schooling (state and local +$1.13 / 2.31bn).
- **Retiree health on accrual** moves the federal part down by $0.69 / 0.57bn: the federal pay-go premiums in other
  federal benefits leave (−$0.97 / 0.90bn). The state and local part rises by $1.27 / 1.33bn, mostly the schools'
  normal cost.
- **The pension item** is set only. It moves the accrual beside (−2.85 / −2.66) and nothing the central rule
  compounds.

The legacy interest therefore rises by $1.19 / 1.55bn, and per member by $28 / 36, on the same 42.75m. [CALCULATION:
`derived/oct07/oct07_bridge_2024.csv`; by line, `derived/oct07/corrections_federal_split_2024.csv`, components
`v6_user_fees`, `v6_retiree_health:scale` and `v5_lineage` less oct05's]

Whole-budget rules (central, low / high, interest $bn): whole_flat 17.04 / 31.86 (oct05 16.22 / 30.56); whole_ratio
14.05 / 26.55 (13.32 / 25.38); whole_income 17.25 / 31.53 (16.37 / 30.19); whole_ratio_federal_series 9.02 / 21.48
(8.33 / 20.36); whole_income_federal_series 26.42 / 38.88 (25.76 / 37.80). They lie inside the programme rules' range,
as before.

**Bridge from October 5** (`derived/oct07/oct07_bridge_2024.csv`, central convention, $bn, low / high end; each item
taken after the ones before it, in the payload's order):

| Step | Cash | Federal cash | Resource cost (federal) | Displaced (federal) | Accrual |
|---|---:|---:|---:|---:|---:|
| October 5 case | 260.71 / 312.28 | 32.40 / 61.18 | 37.15 / 61.86 (0.89 / 1.90) | 8.81 (5.48) | 82.92 / 77.83 |
| `added_age_mix`: the added people's measured ages | −0.32 / +1.71 | −1.68 / −0.88 | +0.06 / +0.21 (0.00) | 0.00 (−0.01) | +1.61 / +0.95 |
| `pension_tr2026`: the 2026 Trustees, separate funds | 0 | 0 | 0 | 0 | −2.85 / −2.66 |
| `retiree_health`: retiree health on accrual | +0.58 / +0.76 | −0.69 / −0.57 | 0 | 0 | 0 |
| `user_fees`: user fees and the education keys | +0.33 / +0.28 | +4.01 / +4.10 | −0.63 / −1.01 | 0 | 0 |
| v6 case | 261.30 / 315.03 | 34.04 / 63.83 | 36.58 / 61.06 (0.89 / 1.90) | 8.81 (5.47) | 81.68 / 76.12 |

The steps are rounded so that they add to the printed totals (largest remainder). Unrounded, the added people's
federal step is −1.6873 / −0.8798, retiree health's cash +0.5845 / +0.7654 and user fees' resource cost
−0.6279 / −1.0025 (`derived/oct07/oct07_bridge_2024.csv`). The case's end specifications are October 5's (48 / 11),
so the bridge's range-ends step is zero. Under the low convention, the items' federal cash step is +1.71 / +2.68, of
which user fees are +4.28 / +4.38. Under the high convention it is +1.49 / +2.55, of which user fees are
+3.76 / +3.81.

**Rules this case needed** (each tagged; the Consumers row of `../main_case_2026_10_07/RESULT.md` asks for the union
twin to take item 1's union parts, item 2's edits and item 4 whole, and the lineage step item 1's lineage parts and
item 3):
1. *The payload, by its registry.* `v6_parts` locates every block by `meta.items`, never by counts. It gates five
   things. September 29's payload comes first. The lineage follows at v5's cells, in v5's order (item 3's values,
   row 8 last at 751). The applied edit sets follow in registry order and close the payload. Each item's parts add to
   its edits. The receipt lines are September 29's two plus the user-fee item's three carriers. meta moves only in the
   stamps, the items' blocks and the capital return, whose components are v5's plus the item's four offsets.
2. *The union twin* [ASSUMPTION, the Consumers rule]. September 29's model plus row 8 plus the union's part of every
   item: the `union_` parts of item 1's cell edits, item 2's ten national-scale edits as they are, item 4 whole and its
   carriers. Gate: the twin's lines and national totals are the case's (1e-9). The items' lineage parts (item 1's
   `lineage_` parts and item 2's share of the added people's cells) and item 3 are then the case less the twin, on the
   lineage's path as in v5 (rule 2 of the v5 section).
3. *Components per item.* A cell edit is a `v6_<item>` component of its line. A national-scale edit is each cell's
   (f − 1) × its amount before the edit (`:scale`). A carrier is a receipt component over its cells. The lineage's
   edits keep v5's component names (`v5_lineage`, `v5_union_response`) at item 3's values. So
   `../winners_losers_2026_09_24/` and `../sept24_propagation_2026_09_24/constant_choices.py` still find them.
4. *The user-fee offsets.* Each offset is keyed by its carrier's amount over the national total
   (`receipt_amount_over_national`). On a model without the item, such as an earlier case or a twin before item 4, the
   carrier is absent and the key is 0 (`capital_rows`).
5. *The bridge, item by item.* Each step is the package's prefix payload: the lineage item, then each edit set with
   the carriers so far. Gate: the last step is the payload. Each step's total equals the case lane's
   `change_at_fixed_specifications` for that item alone plus its pairs with the earlier items, plus the added people's
   P (1e-6 plus the printed remainder). The whole moves by the set's band change plus P (1e-6).
6. *Whole-budget rules.* `cash_whole` classifies the back-cast's `v6_<item>_<path>_<line>` parts by name. The
   production parts are added back with P. Energy assistance, rental assistance and public housing go with the
   displaced beneficiaries. The Social Security and Part A accrual rests go with the accrual. The tax on benefits
   follows `v5_federal_income_tax`'s series, gated at both ends. Any v6 part without a rule stops the run.
7. *Shares and per member.* The responses and counts are v5's (gated), so the shares are October 5's: the case's
   population key 0.12918 and 42,752,212.9 per member. Runs rebuild October 5 for its bridge on October 5's state and
   earlier cases on September 29's, so every earlier bridge is unchanged.
8. *The carriers in the receipts sensitivity.* The three carrier lines carry $1e-9bn each and no key of their own, so
   the receipts sensitivity leaves them out.

**Gates** (all pass; the run stops on any failure):
- `v6_parts` (rule 1) on both payloads. The adoption stamp is 2026-10-07, and the statuses open "adopted 2026-10-07"
  and "the cash set of the case adopted 2026-10-07". The responses are the lane's `summary.json`'s.
- `v5_components` with the items' components: September 29's model plus the lineage's and the items' edits rebuilds
  the case, cell by cell (1e-9).
- Parity with engine.js through the payload consumer, 64 specifications, both payloads: largest difference 3.4e-13
  (set) and 2.8e-13 (cash). Bands $389.082553 / 461.479709bn and $307.399411 / 385.364123bn at 48 / 11, the adoption's
  bands to 6 decimals, gated at 1e-6 (`OCT07` oracle; earlier cases keep their 4-decimal oracles at 5e-5).
- `items_bridge` (rule 5), and the union twin's lines and national totals against the case's (rule 2).
- `cash_whole`: in 2024 the cash part, resource cost, displaced and accrual (each line and the total) are this split's
  (1e-3).
- `derived/oct05/`, `derived/sept29/` and the default `derived/` rebuild byte for byte with the changed script; so
  does `../sept24_propagation_2026_09_24/constant_choices.py --case oct05` (its two CSVs, against its committed
  `derived/oct05/`, 2026-10-07 15:07:32–15:08:39 JST).

Reproduce (from the repository root, after `historical_backcast_2026_09_20/backcast.py --case oct07`;
`test_debt_legacy.py` `test_oct07_rebuilds_its_directory` rebuilds it byte for byte):

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/debt_legacy_2026_09_23/debt_legacy.py --case oct07
```

Log (append-only; times from `date`):
- 2026-10-07 15:01:01–15:02:03 JST: `--case oct07` written to `derived/oct07/` on the adopted payload (case lane
  218a2fb2; corrections.json f8d346aa…, corrections_cash.json e9033bff…), after the back-cast's final oct07 files. Its 17
  CSVs are byte-identical to the 14:12 scratch run on the payload of 14:01, and summary.json differs only in input
  hashes and the oracle. The default run, `--case sept29` and `--case oct05` rebuild their directories byte for byte.
- 15:02:17–15:03:34: `rerun_lane.py` over the default, sept29, oct05 and oct07 commands, with `--allow-unrun` for the
  test file: IDENTICAL 71/71, exit 0. 15:04:06–15:05:31: pytest, 8 passed (the four old cases against their commits,
  the default, sept29, oct05, oct07). Not committed (the lead's brief).
- 15:13:19–15:14:28: the case-lane hashes recorded in `derived/oct07/summary.json` (corrections.json f8d346aa…, corrections_cash.json
  e9033bff…, main_case_bands.csv 35116620…, per_spec.csv 9244bcb5…) are the committed files' (218a2fb2), so no file
  was read mid-write; no rerun needed.
