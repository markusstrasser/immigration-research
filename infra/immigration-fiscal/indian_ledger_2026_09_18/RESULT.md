**Verdict:** On the repo's own ledger conventions, India-origin residents are the most fiscally positive group the repo has measured. Under the upstream lane's headline construction (`equal_all_members` allocation, person weights, adults 25–64) India-born adults run **+$24,163 per adult-year** after the employer-payroll, sales, property, K-12 and MEPS public-paid-health extensions, against **+$13,431** for the same-age third-plus non-Hispanic white reference — a gap of **+$10,732 (se 1,351)**, the mirror image of the Mexico-born **−$10,794 (se 405)**. Under the per-adult (`equal_adults_18plus`) allocation the same figures are **+$30,414** vs **+$14,954**, gap **+$15,460 (se 1,695)**. US-born adults with an India-born parent run **+$34,003**, gap **+$20,572 (se 3,872)** on 209 unweighted cases. No arm reverses the sign: age-standardising, household (resource-unit-head) weighting, dropping the top 1 percent of income, and excluding recent noncitizen entrants move the India-born gap only within **+$9,415 … +$12,587** on the extended balance. The one arm that moves it materially moves it *up*: excluding the temporary-visa proxy (noncitizens who entered 2018 or later) raises the India-born balance from +$24,163 to +$26,828, because that subgroup is the lowest-earning part of the India-born population, not the highest. [DATA: CPS ASEC 2025 public-use file, sha256 `318845a2…`, 160-replicate SDR; MEPS 2024 h256] [CALCULATION: this lane]

Model: `claude-opus-5[1m]`.

The absolute sign is a convention of this ledger (it omits public goods, defence, debt service and benefit accrual); the **gap against same-age whites is not**. This lane measures residents, not admissions, and writes no policy advice.

## Verification, run and pasted

```
$ uv run --no-project --with "pandas>=2" python3 gate_white_reference.py
metric                                    upstream         this lane       delta  result
cash_noncash_tax_balance               11,784.6617       11,784.6617     -0.0000  ✓ PASS
extended_balance_base                  15,984.4248       15,984.4248     -0.0000  ✓ PASS
modeled_tax_total                      14,383.3156       14,383.3156     -0.0000  ✓ PASS
selected_cash_total                     2,453.3194        2,453.3194      0.0000  ✓ PASS
selected_noncash_total                    145.3345          145.3345      0.0000  ✓ PASS
employer_payroll                        3,488.8234        3,488.8234      0.0000  ✓ PASS
sales_tax_share35                       1,049.7299        1,049.7299     -0.0000  ✓ PASS
property_tax_owner                      1,312.7558        1,312.7558      0.0000  ✓ PASS
k12_charged                             1,651.5460        1,651.5460      0.0000  ✓ PASS
white-reference cell n                      36,287            36,287           0  ✓ PASS
GATE: PASS   (exit 0)
```

Byte-identical second run of every script (`cmp` after a full re-run from scratch):

```
IDENTICAL india_ledger_long.csv
IDENTICAL india_ledger_result.txt
IDENTICAL entry_class.csv
IDENTICAL entry_class_result.txt
IDENTICAL entry_class_sources.json
IDENTICAL acs_profile_2023.csv
IDENTICAL acs_profile_2023_result.txt
```

The gate passes to four decimal places because `ledger_india.py` imports `extend_ledger.build()`
and the base generator's `prepare()`/`allocate()`/`estimate()` rather than re-implementing them;
all of the base script's integrity gates (federal refundable-credit identity, SPM-unit dollar
conservation, head-weight/person-weight agreement) run unchanged.

## 1. The ledger

CPS ASEC 2025 (income year 2024), SPM resource units, equal shares among all unit members,
person weights, adults 25–64, annual dollars per adult, SDR standard error in parentheses.
Transfer and cost rows are shown as positive outflows.

| | 3rd+ NH white | India-born | India 2nd gen | Asian Indian, native self-ID | China-born | Mexico-born | Mexican 2nd gen |
|---|---|---|---|---|---|---|---|
| unweighted n | 36,287 | 1,232 | 209 | 258 | 628 | 4,318 | 2,452 |
| weighted (millions) | 87.65 | 3.25 | 0.49 | 0.64 | 1.51 | 9.45 | 5.61 |
| Modeled taxes (payroll+fed+state) | 14,383 (238) | 20,580 (1,075) | 28,906 (3,312) | 25,828 (2,812) | 19,774 (2,116) | 4,874 (221) | 7,419 (268) |
| … federal income after refundable | 8,463 (180) | 12,605 (778) | 18,130 (2,545) | 16,042 (2,128) | 11,757 (1,426) | 2,134 (160) | 3,754 (191) |
| … personal payroll (FICA) | 3,816 (30) | 5,055 (167) | 5,778 (322) | 5,418 (300) | 4,487 (266) | 2,147 (41) | 2,712 (54) |
| … state income after credits | 2,105 (39) | 2,920 (212) | 4,998 (640) | 4,368 (521) | 3,530 (472) | 593 (37) | 953 (50) |
| State-local total (income+sales+property) | 4,467 (56) | 5,883 (284) | 9,332 (857) | 8,270 (737) | 6,760 (630) | 1,703 (54) | 2,502 (77) |
| Selected cash transfers | 2,453 (48) | 481 (97) | 1,016 (303) | 722 (249) | 815 (171) | 860 (63) | 1,460 (102) |
| Selected non-cash transfers | 145 (4) | 43 (5) | 25 (10) | 47 (13) | 166 (27) | 246 (13) | 240 (14) |
| **= Taxes minus selected transfers** | **11,785 (250)** | **20,056 (1,085)** | **27,865 (3,385)** | **25,059 (2,854)** | **18,793 (2,108)** | **3,768 (230)** | **5,719 (278)** |
| + Employer payroll tax | 3,489 (28) | 4,842 (163) | 5,469 (294) | 5,156 (274) | 4,187 (248) | 1,895 (37) | 2,542 (52) |
| + Sales/excise tax (0.35 share) | 1,050 (10) | 1,393 (55) | 1,668 (143) | 1,566 (123) | 1,296 (90) | 592 (12) | 784 (16) |
| + Property tax (owner-occupied) | 1,313 (16) | 1,569 (91) | 2,666 (321) | 2,336 (293) | 1,933 (137) | 518 (25) | 765 (29) |
| − K-12 public schooling | 1,652 (23) | 2,210 (128) | 1,562 (300) | 1,730 (270) | 2,464 (205) | 2,311 (62) | 2,112 (86) |
| **= EXTENDED BALANCE** | **15,984 (292)** | **25,650 (1,330)** | **36,105 (3,809)** | **32,387 (3,304)** | **23,746 (2,518)** | **4,462 (290)** | **7,698 (375)** |
| − MEPS public-paid health | 2,553 (12) | 1,487 (52) | 2,103 (116) | 2,044 (99) | 1,869 (74) | 1,825 (27) | 2,190 (39) |
| **= AFTER HEALTH** | **13,431 (295)** | **24,163 (1,332)** | **34,003 (3,824)** | **30,344 (3,320)** | **21,877 (2,510)** | **2,637 (291)** | **5,508 (378)** |

Gap from the white reference, after health: India-born **+10,732 (1,351)**, India second generation
**+20,572 (3,872)**, native self-identified Asian Indian **+16,913 (3,382)**, China-born
**+8,446 (2,523)**, Mexico-born **−10,794 (405)**, Mexican second generation **−7,923 (448)**.

Where the India-born advantage comes from: **+6,197** of it is modeled taxes (mostly federal
income tax, +4,142) and **+1,972** is cash transfers *not* received — India-born adults draw
$481 of selected cash transfers a year against $2,453 for white natives, a difference that is
mostly Social Security (the white reference is older) rather than means-tested aid. Their
Medicaid coverage rate is 4.2 percent against 11.2 percent for white natives and 21.0 percent
for Mexico-born adults. Against that, they carry **more** K-12 cost (+559) — their resource
units hold more school-age children per adult — and a smaller health charge (−1,066), which is
an age effect the MEPS donor model reproduces mechanically.

### Per-adult allocation (`equal_adults_18plus`), as the repo's quant-bias record requires

The table above uses `equal_all_members`, which spreads a unit's taxes, transfers and children's
schooling over every member including children, so its rows are per *person in an adult's unit*,
not per adult. The repo's 2026-09-16 self-audit requires that a per-adult claim come from the
adults-only allocation. Same file, same universe, person weights, adults 25–64:

| | white | India-born | India 2nd gen | India-born settled | India-born recent noncit. | China-born | Mexico-born |
|---|---|---|---|---|---|---|---|
| Taxes minus selected transfers | 14,409 | 26,141 | 35,349 | 29,756 | 17,717 | 23,527 | 4,023 |
| K-12 charged | 3,501 | 4,047 | 3,002 | 4,549 | 2,880 | 4,577 | 4,628 |
| Extended balance | 18,099 | 32,310 | 44,644 | 36,683 | 22,123 | 28,462 | 3,154 |
| After health | 14,954 (337) | **30,414 (1,669)** | **42,044 (5,281)** | 34,447 (2,098) | 21,018 (1,781) | 26,100 (2,939) | 778 (362) |
| Gap vs white (se) | — | **+15,460 (1,695)** | **+27,090 (5,317)** | +19,493 (2,139) | +6,064 (1,761) | +11,146 (2,955) | −14,176 (482) |
| Children 5–17 per adult | 0.253 | 0.264 | 0.185 | 0.298 | 0.183 | 0.271 | 0.334 |

The adults-only allocation roughly doubles the K-12 charge for every group and widens every gap,
including the India-born one (+15,460 against +10,732). The India-born carry slightly *more*
school-age children per adult than the white reference (0.264 vs 0.253) and settled India-born
adults carry clearly more (0.298); the temporary-visa proxy group carries the fewest (0.183).

All-age universe (every civilian resident, children included, `equal_all_members`): India-born
**+20,044 (1,137)** per person-year after health, India second generation **+23,647 (2,318)**,
white reference **+4,589 (202)**, Mexico-born **+644 (260)**. The all-age gaps are larger in
relative terms because the white reference carries the retirement years.

### Arms (extended balance after health, adults 25–64)

| Arm | white | India-born | gap (se) | India 2nd gen | gap (se) |
|---|---|---|---|---|---|
| raw (headline) | 13,431 | 24,163 | +10,732 (1,351) | 34,003 | +20,572 (3,872) |
| age-standardised to the white 25–64 distribution | 13,431 | 24,386 | +10,955 (1,449) | 37,123 | +23,692 (5,482) |
| household (resource-unit-head) weighted | 13,709 | 24,132 | +10,422 (1,338) | 34,057 | +20,348 (3,914) |
| excluding the top 1% of income | 11,488 | 21,976 | +10,488 (1,187) | 29,214 | +17,726 (2,934) |
| excluding recent noncitizen entrants (temporary-visa proxy) | 13,431 | 26,828 | +13,397 (1,618) | 34,003 | +20,572 (3,872) |

Sensitivity on the extension assumptions (extended balance before health): base 25,650, flat-0.90
pupil ratio 25,382, renter property-tax pass-through 26,107, ITEP sales-tax schedule 26,277. The
span is $895 on a $9,666 gap.

**The temporary-visa arm, stated with its direction.** CPS observes no visa class, so the proxy is
"noncitizen who entered in 2018 or later": 30.0 percent of India-born adults 25–64, n=362,
0.97M weighted. That subgroup runs **+17,956 (1,594)** after health against **+26,828 (1,588)**
for settled India-born adults. They pay $4,325 of personal payroll tax and generate $4,268 of
employer payroll tax per adult-year while drawing $158 of selected cash transfers. The ledger
credits them no future benefit and charges them none; if a share of them leave before claiming
Social Security, this annual snapshot *understates* their net contribution, and if they stay and
claim, it overstates it. Either way the headline does not turn on this arm — excluding them
raises the India-born figure. [FRAMING-SENSITIVE]

### What this does not measure

Public goods, defence, debt service, corporate tax and its incidence, institutional care, and
benefit accrual are all outside the ledger, exactly as in the upstream lane. The MEPS donor model
classifies birthplace only as US/not-US, so India-specific medical cost is modeled, not measured
[UNVERIFIED]. The sales, property and K-12 rows are accounting scenarios built from published
aggregate rates, not observed payments [UNVERIFIED]. Cell sizes for the second generation (n=209
adults) are small; the SDR standard errors carry sampling error only.

**A population discrepancy worth flagging.** CPS ASEC 2025 puts the India-born population at
4.28M all ages (3.25M aged 25–64). ACS 2023 1-year puts it at 2.94M all ages (2.23M aged 25–64).
Two years of growth cannot plausibly close a 45 percent gap; CPS ASEC is a small sample for a
1 percent origin group and is the weaker instrument for a level. The *gap* estimates above are
ratios within the same file and are far less exposed to this than any count would be. [SOURCE:
both files, this lane's own tabulations]

## 2. ACS 2023 1-year PUMS profile

| | India-born | China-born | China broad | Mexico-born | All foreign-born | US-born | US-born, Asian Indian ancestry |
|---|---|---|---|---|---|---|---|
| unweighted n, 25–64 | 20,976 | 16,128 | 21,327 | 69,152 | 287,286 | 1,403,154 | 2,937 |
| Population, all ages (M) | 2.94 | 2.28 | 2.95 | 11.30 | 47.81 | 287.11 | 1.12 |
| Median age | 41 | 46 | 48 | 46 | 46 | 37 | 15 |
| BA or higher, 25–64 | 84.4% | 59.0% | 62.8% | 10.4% | 36.8% | 38.3% | 83.6% |
| Graduate degree | 52.4% | 37.7% | 38.0% | 3.0% | 16.8% | 14.0% | 47.6% |
| Doctorate | 5.0% | 11.0% | 10.2% | 0.3% | 2.7% | 1.4% | 6.2% |
| High school or less | 9.2% | 30.2% | 25.8% | 74.9% | 44.9% | 31.7% | 5.4% |
| Employed 25–64 | 81.9% | 78.5% | 78.4% | 73.6% | 77.3% | 77.1% | 84.8% |
| Median household income (householder's group) | $165,193 | $91,757 | $100,219 | $65,147 | $78,911 | $77,483 | $142,733 |
| Mean household size | 2.95 | 2.62 | 2.57 | 3.62 | 3.03 | 2.35 | 2.39 |
| Computer/math occupations, employed | 31.1% | 14.6% | 14.1% | 1.0% | 6.0% | 3.9% | 11.6% |
| Physicians/surgeons, employed | 2.50% | 1.45% | 1.57% | 0.08% | 0.94% | 0.62% | 12.13% |
| Top-10 occupation concentration | 42.6% | 32.4% | 30.8% | 34.8% | 23.2% | 19.8% | 37.7% |
| Self-employed, employed | 7.3% | 11.6% | 11.4% | 14.2% | 13.2% | 9.3% | 9.1% |
| Traveler accommodation (NAICS 7211), share of the self-employed | 2.01% | 0.19% | 0.22% | 0.34% | 0.39% | 0.20% | 3.78% |
| Naturalised (foreign-born) | 47.8% | 52.3% | 58.4% | 34.7% | 52.3% | — | — |
| Median years in the US | 13 | 17 | 19 | 24 | 21 | — | — |
| English very well / only English | 79.3% | 42.1% | 45.2% | 34.9% | 53.2% | — | — |
| Top-10 PUMA concentration | 8.0% | 12.3% | 11.7% | 4.2% | 2.1% | 0.7% | 6.5% |
| Top-5 state concentration | 52.8% | 63.8% | 65.0% | 70.5% | 58.2% | 34.1% | 52.6% |
| **Group's share of all US employed 25–64** | **1.37%** | 0.88% | 1.14% | 4.82% | 19.51% | 80.49% | **0.19%** |
| … of all self-employed | 1.00% | 1.02% | 1.30% | 6.83% | 25.67% | 74.33% | 0.17% |
| … of self-employed in traveler accommodation | **8.14%** | 0.79% | 1.14% | 9.41% | 40.66% | 59.34% | **2.60%** |
| … of physicians and surgeons | **5.03%** | 1.88% | 2.63% | 0.58% | 26.85% | 73.15% | **3.35%** |
| … of computer/math occupations | **9.87%** | 2.98% | 3.72% | 1.17% | 27.29% | 72.71% | 0.50% |

Naturalisation by time in the US (India-born): 2.3% at 0–4 years, 15.9% at 5–9, 36.1% at 10–14,
55.6% at 15–19, 90.7% at 20+. The low early figures are the employment-based queue, not a
reluctance to naturalise: the 20-plus cohort naturalises at a higher rate than China-born (83.6%)
or Mexico-born (43.9%).

Top India-born occupations (employed 25–64): software developers 19.3%, other managers 5.3%,
other computer occupations 3.0%, computer and information systems managers 2.6%, physicians 2.4%,
management analysts 2.2%, other engineers 2.2%, registered nurses 1.9%, computer systems analysts
1.8%, postsecondary teachers 1.8%. One in five employed India-born adults is a software developer.

Self-employment is *lower* than the foreign-born average (7.3% vs 13.2%) and its industry mix is
professional, not retail: computer systems design 12.8%, truck transportation 8.3%, food services
5.9%, management consulting 5.4%, offices of physicians 4.7%. China-born self-employment is the
opposite profile (food services 19.0%, construction 6.3%, nail salons 6.2%).

**The motel claim, in both directions.** Read as a share of the group, it is small: 2.01% of
India-born self-employed people are in traveler accommodation (3.78% among US-born of Indian
ancestry), which is 0.15% of employed India-born adults. Read as a share of the industry — the
direction the claim is normally made in — it is large: India-born people are **1.37%** of all US
employed adults 25–64 but **8.14%** of the self-employed in traveler accommodation, and adding
US-born adults of Indian ancestry brings the two figures to 1.56% and **10.7%**, a roughly
seven-fold over-representation. The same two-directional reading applies to medicine (5.03% +
3.35% = 8.4% of physicians and surgeons, from 1.56% of employment) and to software (9.87% +
0.50% = 10.4% of computer and mathematical occupations). [CALCULATION: ACS 2023 1-year PUMS]

**Endogamy** (married, spouse present; couples where one partner is the household reference
person): India-born 88.4% have an India-born spouse (91.3% including a US-born spouse of Asian
Indian ancestry, n=18,718 couples); China-born 77.5%; Mexico-born 72.7%. US-born people of Asian
Indian ancestry marry an Indian-origin spouse 52.4% of the time (n=1,527) — a large drop between
generations, and still far above random matching.

Method notes: point estimates on `PWGTP` (households on `WGTP`); no replicate standard errors
(the 80 replicate columns would be ~2 GB for the national file; every cell above has an
unweighted n in the thousands except the US-born-ancestry group, whose n is printed). The
second generation cannot be identified in ACS — there is no parental birthplace — so "US-born,
Asian Indian ancestry" (ANC1P/ANC2P = 615) is a proxy that includes the third generation and
excludes anyone who does not report the ancestry. Its median age of 15 shows how young this
population still is; the 25–64 adults in it are a small, self-selected slice, which is the most
likely explanation for the striking 12.13% physician share (n=2,495 employed). [INFERENCE]

## 3. Entry class, FY2020–FY2024

India's share of persons obtaining lawful permanent resident status, by broad class of admission
(DHS/OHSS Yearbook Table 10; FY2020 and FY2021 come from the "tables 8–11 new adjustment"
workbooks, whose Table 10 splits each class into adjustments of status and new arrivals — this
lane sums the two halves back together):

| Class | FY2020 | FY2021 | FY2022 | FY2023 | FY2024 |
|---|---|---|---|---|---|
| Employment-based preferences | 16.7% | 39.0% | 35.6% | 14.5% | 11.0% |
| Family-sponsored preferences | 5.8% | 2.9% | 4.9% | 7.4% | 5.1% |
| Immediate relatives of US citizens | 4.0% | 3.9% | 4.8% | 5.8% | 5.1% |
| Diversity | 0.1% | 0.1% | 0.1% | 0.1% | 0.1% |
| Refugees and asylees | 1.8% | 1.8% | 2.2% | 1.8% | 1.7% |
| **All classes** | **6.6%** | **12.6%** | **12.5%** | **6.7%** | **4.9%** |

India persons, all classes: 46,363 (FY2020), 93,450, 127,012, 78,070, 66,800 (FY2024). The
FY2021–22 spike is the pandemic-era spillover of unused family visas into the employment-based
categories, not a change in Indian demand.

I-94 nonimmigrant admissions, FY2024 (Yearbook Table 33, by country of citizenship): India is
**55.9%** of admissions in specialty occupations (H-1B), 497,460 of 890,310; 32.6% of the spouses
and children of temporary workers, 265,400 of 814,530; 10.8% of intracompany transferees (L-1);
0.0% of seasonal agricultural workers (H-2A). India is 16.3% of all temporary-worker admissions
and 13.4% of students and exchange visitors, against 3.8% of all I-94 admissions.

**Not obtained:** the USCIS *Characteristics of H-1B Specialty Occupation Workers* report, which
gives H-1B *approvals* (petitions) by country of birth, was not fetched in this lane. Admissions
and approvals are different objects — an admission is a border crossing and one worker generates
several per year — so the 55.9% above should not be quoted as the approval share. [SKIPPED]

## Draft memo section the parent can lift

> **India-origin residents on the repo's ledger.** The repo has used India-born adults only as a
> positive-selection benchmark. Put on the same annual ledger as the Mexican-origin groups — CPS
> ASEC 2025, SPM resource units, equal shares among all members, person weights, adults 25–64,
> extended with employer payroll tax, sales and excise, owner-occupied property tax, K-12 at the
> measured public-pupil ratio, and MEPS public-paid health — India-born adults run **+$24,163 per
> adult-year** against **+$13,431** for same-age third-plus non-Hispanic whites, a gap of
> **+$10,732 (se 1,351)**. US-born adults with an India-born parent run **+$34,003**, gap
> **+$20,572 (se 3,872)** on 209 cases. Against the Mexico-born **−$10,794 (se 405)**, the two
> origin groups sit almost symmetrically either side of the white reference on this ledger.
> On the adults-only allocation, which charges each unit's schooling to its adults, the same
> comparison is +$30,414 against +$14,954, a gap of **+$15,460 (se 1,695)**.
>
> Roughly three-fifths of the India-born advantage is tax paid (+$6,197 of modeled taxes, mostly
> federal income tax) and two-fifths is cash transfers not received (−$1,972, mostly Social
> Security, an age effect). Their Medicaid coverage rate is 4.2% against 11.2% for white natives.
> They carry *more* K-12 cost than the white reference (+$559 per adult-year), not less.
>
> Four arms that could have reversed it do not: age-standardising to the white age distribution
> (+$10,955), household weighting (+$10,422), dropping the top 1% of income (+$10,488), and
> excluding the temporary-visa proxy (+$13,397 — recent noncitizen entrants are the *lowest*-net
> part of the India-born population, not the highest). The absolute sign remains a convention of a
> ledger that omits public goods and benefit accrual; the gap against same-age whites is not.
>
> The ACS 2023 profile behind those numbers: 84.4% of India-born adults 25–64 hold a BA or more
> and 52.4% a graduate degree (US-born: 38.3% and 14.0%); median household income $165,193 against
> $77,483; 31.1% of the employed are in computer and mathematical occupations and 19.3% are
> software developers. Self-employment is *below* the foreign-born average (7.3% vs 13.2%), though
> India-origin people are 1.56% of US employed adults 25–64 and 10.7% of the self-employed in
> traveler accommodation, 8.4% of physicians and surgeons and 10.4% of computer and mathematical
> occupations — the motel concentration is real read as a share of the industry, while describing
> only 0.15% of the group's own employment. Spousal endogamy is 88.4% for the India-born and
> 52.4% for US-born adults of Indian ancestry. Entry is employment-first: India took 11–39% of
> employment-based green cards over FY2020–24 but 0.1% of diversity visas, and is 55.9% of FY2024
> I-94 admissions in specialty occupations.

## Files

| File | What |
|---|---|
| `ledger_india.py` | The ledger run. Imports `extend_ledger.build()` and the base generator; adds groups, universes, arms and the MEPS health component. |
| `gate_white_reference.py` | The gate. Compares nine white-reference metrics with the upstream lane's CSV at $1.00 tolerance; exit 0 = PASS. |
| `acs_profile.py` | ACS 2023 1-year PUMS profile. |
| `entry_class.py` | DHS/OHSS Yearbook fetch and parse (LPR Table 10 FY2020–24, nonimmigrant Tables 29/33). |
| `derived/india_ledger_long.csv`, `derived/india_ledger_result.txt` | Ledger, long form and printed. |
| `derived/acs_profile_2023.csv`, `derived/acs_profile_2023_result.txt` | ACS profile. |
| `derived/entry_class.csv`, `derived/entry_class_result.txt`, `derived/entry_class_sources.json` | Entry class and its source manifest (URLs + sha256). |
| `README.md` | Run commands, inputs, outputs, known limits. |

Skipped, with reasons: the USCIS H-1B approvals-by-country report (not fetched; admissions used
instead and labelled as such); ACS replicate standard errors (2 GB of replicate weights for
estimates whose cells are in the thousands); multi-year ASEC pooling (the brief directs pooling
the same years the upstream lane pools, which is ASEC 2025 alone — and the 2026 file recodes
`PEINUSYR`, a trap the base generator fails loud on).
