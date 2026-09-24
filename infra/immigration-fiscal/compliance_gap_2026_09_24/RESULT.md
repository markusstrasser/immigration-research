**Verdict:** Breaking labor and tax rules gives an employer a real cost edge, but its measured total is a few billion dollars a year, and nothing here shows it driving honest firms out of business. Paying a worker off the books saves 11–12% of the wage in legally required costs, and 11–24% once the worker's own payroll tax and typical underpayment are counted; construction's 12–23% matches the construction payroll-fraud studies. Across states, wage work that the ACS sees but unemployment-insurance payrolls miss rises by about 0.6 of a worker (range 0.3–0.9) for each imputed-unauthorized worker in construction, landscaping and janitorial services; restaurants show no such gap across states. At 2024 pay that is $30–64bn of off-books pay and an edge of up to $14.8bn a year in those four industries (central $6.4bn). Of the central edge, $4.5bn is payroll tax that the adopted account already counts. A national level check calibrated on low-immigrant industries cannot confirm the off-books count and allows as little as zero. Covered establishments and employment grew no slower where the group's share grew (2012–2023, state-year and industry-year fixed effects), the one negative association (specialty-trade establishments) disappears once state-wide shocks are removed, and the pre-registered E-Verify test fails its pre-trend check. The literature points the same way: in Georgia, rivals' undocumented hiring did not significantly raise exit in construction, agriculture or hospitality, and police-based removals of unauthorized immigrants lowered local business counts instead of letting compliant firms take over.

Lane: compliance edge and competition, 2026-09-24/25, answering the operator's question whether illegal immigrants' businesses, "not needing the same scrupels", drive honest businesses out ([BRIEF](BRIEF.md)). Model self-report: `claude-opus-5-5[1m]`. Nothing was committed; nothing outside this directory was edited.

## Answers in one table

| Question | Answer | Evidence level |
|---|---|---|
| Edge per dollar of off-books wages | 11–12% in employer legal costs (construction 12.2%, restaurants 11.2%); 11–24% with the employee's payroll tax kept and underpayment | measured costs (BLS ECEC), modelled capture |
| Share of the group's wage workers off UI payrolls | construction 0.60 (SE 0.10; variants 0.54–0.88), landscaping 0.59 (0.29–0.59), janitorial 0.74 (0.31–0.74), restaurants 0.01 (0–0.59) | association across states |
| Off-books pay and workers, 2024, four industries | $30–64bn (central $37bn); 0.74–1.72m workers (central 0.96m); level check: $0 | modelled from the slope; the level check disagrees |
| Edge in dollars, 2024 | $0–14.8bn (central $6.4bn): payroll taxes $4.5bn (inside the account), workers' compensation $1.3bn, underpayment $0.6bn | modelled |
| What enforcement finds | WHD back wages 0.001–0.017% of covered payroll; OSHA penalties at most 0.026% | measured, targeted |
| Do compliant firms lose ground? | No association in establishments or employment; wage association not robust; E-Verify test not identified | associations; one failed design |
| Who gains | noncompliant employers (the edge); customers if it is passed on | modelled / assumed |
| Who loses | the budget (inside the account); off-books workers (underpayment, no workers' compensation) | modelled / assumed |

## Gates

| Gate | Result |
|---|---|
| Row counts, keys and hashes of every fetched file | PASS. IPUMS extracts match IPUMS's published sha256. QCEW has 20 years × 52 areas. The DOL files have identical headers across chunks and unique case ids. See the data table. |
| QCEW national 2-digit totals equal BLS published annual averages, two years | PASS. 2019 and 2023: 20 of 20 sectors equal the rows behind BLS's published Table 2. Private totals are 126.359m employees and 9.932m establishments (2019), against the printed 126.4m and 9.9m, and 131.290m and 11.561m (2023), against the printed 131.3m and 11.6m. The lane's industry cells sum to the national private total in all 20 years (ratio 1.00000). |
| WHD case count and back wages for one fiscal year match a DOL published figure | **FAIL**, see below |
| Every computed specification appears here | PASS. All 68 slope specifications, all 30 E-Verify summaries with their event-time coefficients and trend breaks, all 174 panel rows (as 58 table rows, three outcomes each) and the composition check are below. |
| Quotes re-found in the cached source texts | PASS. `quote_check.py` finds all 33 quotes in the "Quotes used" table and 272 of the 295 quoted strings in the reading notes (details in `derived/quote_check.csv`). The other 23 are not source quotes: titles, search queries, tool error text, the operator's words, table-parsing fragments, and one shortened paraphrase (LIT_COMPLIANCE_COSTS.md line 378) of a quote that appears verbatim at line 243. |

**WHD gate, failed.** DOL publishes, for FY 2023, 20,215 concluded compliance actions, $212,325,391 in back wages and 163,768 employees ([SOURCE: dol.gov WHD "All Acts" table, cached `_cache/papers/whd_all_acts.txt`]). The portal file carries no case-closing date. Dated by the fiscal year of the findings end date, it holds the following shares of the published figures:

| FY | cases | back wages | employees |
|---|---|---|---|
| 2013 | 0.72 | 1.09 | 1.17 |
| 2014 | 0.71 | 1.02 | 0.94 |
| 2015 | 0.66 | 0.97 | 0.97 |
| 2016 | 0.57 | 0.74 | 0.71 |
| 2017 | 0.58 | 0.92 | 0.95 |
| 2018 | 0.65 | 0.86 | 0.88 |
| 2019 | 0.60 | 0.81 | 0.64 |
| 2020 | 0.55 | 0.80 | 0.78 |
| 2021 | 0.55 | 0.80 | 0.81 |
| 2022 | 0.57 | 0.99 | 0.96 |
| 2023 | 0.52 | 0.85 | 1.03 |
| 2024 | 0.49 | 0.73 | 0.65 |
| 2025 | 0.41 | 0.41 | 0.40 |

Dated by load date, back wages match in FY 2021 (1.0001) and employees nearly so (0.99), but cases do not (0.63).

No year matches within 2% on both cases and back wages. The file's metadata says it "contains all concluded WHD compliance actions since FY 2005", yet it holds about half the published action count. It does include 161,253 actions with no back wages, so dropping zero-dollar actions does not explain the gap. The cause is unresolved [UNVERIFIED].

Consequence: the WHD figures below are floors. The file's back wages run 0.73–1.09 of the published totals in FY 2013–2024. Scaled to the published totals, WHD recoveries remain under 0.02% of covered payroll, so the conclusion does not depend on the gate.

## Data

| Source | File (ignored `_cache/`) | Rows | Check |
|---|---|---|---|
| IPUMS USA ACS 1-year 2012–2024, employed (extract 16) | `_cache/ipums/workers.csv.gz` | 19,103,402 | sha256 equals IPUMS's published value; 13 years; person key unique |
| IPUMS USA ACS 1-year 2005–2011, employed (extract 17) | `_cache/ipums/workers_pre.csv.gz` | 9,683,631 | same; 7 years |
| QCEW annual singlefiles 2005–2024, state and national rows | `_cache/qcew/qcew_state_<year>.csv.gz` | 137–144k kept of 3.56–3.66m a year | the gates above |
| QCEW API national files 2019 and 2023 | `_cache/qcew/api_US000_{2019,2023}.csv` | 4,560 and 4,531 | gate source; UI contributions |
| DOL WHD compliance actions (portal bulk file, loaded 2026-09-21) | `_cache/dol/whd_cases.csv.gz` | 367,890, unique case ids | gate failed, above |
| DOL OSHA inspections (loaded 2026-09-24) | `_cache/dol/osha_inspections.csv.gz` | 1,930,996 opened since FY 2005, of 5,201,660 | columns present |
| DOL OSHA violations | `_cache/dol/osha_violations.csv.gz` | 4,059,361 issued since FY 2005 and not deleted, of 13,272,520 | columns present |
| BLS ECEC Table 4, June 2026 | `_cache/papers/ecec_t04_2026q2.txt` | industry rows | edges.py checks the release label and 16 values per row |

Per-file row counts, headers and hashes are in `derived/fetch_manifest_{ipums,qcew,dol}.json`, and the QCEW gates are in `derived/gates_qcew.csv`. The literature texts are under `_cache/papers/`; the reading notes (`reads/`) give each one's URL.

**Groups.** Mexico-born noncitizen means BPL 200 with CITIZEN 3. The imputed-unauthorized flag applies the Borjas (2017) residual rules the ACS supports; `../status_impute_2026_09_16` ports the same rules to the CPS. The ACS lacks two of the rules (public housing, licensed occupations), so the flag over-counts slightly. It also takes in temporary visa holders, so a variant restricted to workers without a bachelor's degree is reported. Insurance items start in 2008. In 2008–2024 the flag counts 6.8–8.7m employed people in the lane's industries: 6.8m in 2020, the pandemic year with experimental ACS weights, and 8.7m in 2024.

## Test A. The edge

### What enforcement finds

| Industry | WHD cases/yr | back wages $m/yr | per case $ | per employee found $ | per employee-year, % of covered pay | per covered worker $ | % of covered payroll | WHD penalties $m/yr | OSHA inspections/yr | OSHA penalty per inspection $ | per covered worker $ | % of covered payroll | programmed % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Construction | 2,255 | 37.2 | 31,380 | 1,683 | 1.5 | 5.71 | 0.0098 | 1.43 | 36,474 | 3,124 | 15.70 | 0.0256 | 65 |
| Landscaping services | 208 | 3.0 | 26,048 | 1,266 | 1.7 | 4.13 | 0.0120 | 0.47 | 865 | 2,434 | 2.72 | 0.0074 | 31 |
| Services to buildings except landscaping (janitorial) | 340 | 4.6 | 25,498 | 1,104 | 2.2 | 3.59 | 0.0136 | 0.36 | 538 | 2,758 | 1.04 | 0.0039 | 29 |
| Restaurants and other food services | 3,272 | 32.8 | 16,637 | 970 | 2.5 | 3.15 | 0.0168 | 5.16 | 1,106 | 1,721 | 0.17 | 0.0008 | 28 |
| Private households | 16 | 0.1 | 12,397 | 6,296 | 16.2 | 0.38 | 0.0015 | 0.00 | 11 | 2,070 | 0.04 | 0.0001 | 36 |
| Crop production | 654 | 2.8 | 18,251 | 619 | 1.4 | 5.18 | 0.0158 | 3.04 | 872 | 2,093 | 3.09 | 0.0090 | 38 |
| Animal production | 66 | 0.7 | 27,647 | 1,263 | 1.7 | 2.96 | 0.0084 | 0.35 | 268 | 2,506 | 2.51 | 0.0065 | 44 |
| Support activities for agriculture | 372 | 1.7 | 17,800 | 508 | 1.6 | 4.46 | 0.0135 | 2.08 | 576 | 2,361 | 3.37 | 0.0102 | 25 |
| Professional and technical services | 438 | 12.7 | 50,547 | 2,521 | 1.3 | 1.43 | 0.0016 | 0.33 | 701 | 1,950 | 0.14 | 0.0001 | 28 |
| Finance and insurance | 141 | 2.1 | 28,807 | 1,009 | 0.5 | 0.36 | 0.0004 | 0.05 | 101 | 1,221 | 0.02 | 0.0000 | 11 |

WHD dollars come from the portal file, dated by findings end. The depth column is back wages per employee-year of the findings period, divided by the industry's average covered pay. OSHA figures are for private establishments; penalties are current penalties, after settlement.

**How targeting biases each figure:**

- **WHD per case overstates the typical employer.** About a third of FLSA cases are directed, aimed at low-wage, high-violation industries, and investigators found violations in 80% of FY 2019 FLSA cases (GAO-21-13, excerpt).
- **WHD per covered worker understates prevalence.** About two-thirds of cases start from a complaint, and GAO names these industries' workers as unlikely to complain, so the group in question is under-sampled.
- **WHD depth (1.4–2.5% of pay outside private households) is a floor** on what underpaid workers lose. Recoveries cover a two-year look-back and only the violations investigators computed. The 2008 three-city survey found low-wage workers losing 15% of earnings (Bernhardt et al. 2009, p. 9).
- **OSHA penalties describe targeted high-hazard sites.** 65% of construction inspections are programmed, against 25–44% in the other focus industries; OSHA overall was 49.6% programmed in FY 2024. Per covered worker they understate hazard, because most sites are never inspected.

### IRS tax gap (Publication 1415, Table 5; tax years 2014–2016, the newest audit-based estimate)

| Income category | Net misreporting percentage | Tax gap, $bn a year |
|---|---|---|
| Wages, salaries, tips (withheld and reported) | 1% | 7 |
| Substantial information reporting, no withholding | 6% | 15 |
| Some information reporting | 15% | 43 |
| Little or no information reporting | 55% | 126 |
| of which nonfarm proprietor income | **57%** | 80 |
| Employer FICA and FUTA underreporting (Pub 1415 p. 24; Pub 5869 Table 3) | – | 29 (TY 2014–16); 40 projected (TY 2022) |

The net misreporting percentage is net misreported income over the sum of absolute correct amounts. The IRS derives it from random National Research Program audits with detection-controlled estimation. The audits are random, so this figure carries no targeting bias; its weaknesses are age and method.

The employer FICA/FUTA estimate rests on the Employment Tax Study of 2008–2010. It excludes agricultural and household employers, the two industries where the lane cannot price the edge, so the IRS calls it an underestimate (Pub 1415 p. 23).

No IRS publication splits any of these by nativity or status [SOURCE: reads/LIT_COMPLIANCE_COSTS.md §1]. The self-employed's side, 57% of proprietor income unreported, is the tax edge of the group's own businesses (see Test B). It is inside the adopted account through the September 24 tax correction and is not priced here.

### Edge per dollar of off-books wages

| Industry | E1 employer legally required, % of wages | of which state UI (QCEW 2023) % | E2 employee FICA kept, % (low/central/high) | E3 underpayment, % | edge, % of off-books wages | off-books share of the group's wage workers (slope) |
|---|---|---|---|---|---|---|
| Construction | 12.2 | 0.70 | 0 / 3.8 / 7.65 | 0 / 1.5 / 3.0 | 12.2 / 17.5 / 22.9 | 0.54 / 0.60 / 0.88 |
| Landscaping services | 10.7 | 0.97 | 0 / 3.8 / 7.65 | 0 / 1.7 / 3.3 | 10.7 / 16.2 / 21.7 | 0.29 / 0.59 / 0.59 |
| Services to buildings except landscaping (janitorial) | 10.7 | 0.80 | 0 / 3.8 / 7.65 | 0 / 2.2 / 4.4 | 10.7 / 16.7 / 22.8 | 0.31 / 0.74 / 0.74 |
| Restaurants and other food services | 11.2 | 0.75 | 0 / 3.8 / 7.65 | 0 / 2.5 / 5.0 | 11.2 / 17.6 / 23.9 | 0.00 / 0.01 / 0.59 |
| Crop production | 10.1 (8.6-11.6) | 0.99 | 0 / 3.8 / 7.65 | 0 / 1.4 / 2.8 | 8.6 / 15.4 / 22.1 | not identified |
| Animal production | 9.5 (8.0-11.0) | 0.35 | 0 / 3.8 / 7.65 | 0 / 1.7 / 3.5 | 8.0 / 15.1 / 22.1 | not identified |
| Support activities for agriculture | 10.7 (9.2-12.2) | 1.52 | 0 / 3.8 / 7.65 | 0 / 1.6 / 3.3 | 9.2 / 16.1 / 23.1 | not identified |
| Private households | 9.8 (8.3-11.3) | 0.66 | 0 / 3.8 / 7.65 | 0 / 16.2 / 32.4 | 8.3 / 29.8 / 51.3 | not identified |

**How the edge is built:**

- **E1** is legally required benefits per hour over wages per hour, from BLS ECEC Table 4 for June 2026:
  - construction $4.42 / $36.13, which is 12.2%;
  - administrative and waste services $2.80 / $26.07, 10.7%;
  - accommodation and food services $1.82 / $16.18, 11.2%;
  - all private industry $3.40 / $32.82, 10.4%.

  ECEC excludes farms and private households. For those, E1 is statutory FICA of 7.65% (IRS Pub 15, 2024) plus the industry's measured QCEW UI rate, plus an assumed 0–3% for workers' compensation.
- **E2** is the employee's 7.65%, which the employer keeps only by cutting the cash wage: none, half or all.
- **E3** is underpayment: none, the WHD depth, or twice it.

The construction edge of 12–23% of the off-books wage matches two construction studies, neither immigrant-specific:

- Ormiston–Belman–Erlich (2020) put payroll-fraud savings at 12.5–23.5% of legal labor cost [CALCULATION on their Table A, p. 5, in reads/LIT_COMPLIANCE_COSTS.md §3b].
- Belman et al. (ICERES 2025) put workers' compensation plus employer FICA at 16.1% of labor cost on one Michigan project (p. 3).

If off-books workers lost 15% of earnings, as in the 2008 survey, underpayment alone would be $5.6bn on the central 2024 off-books pay rather than $0.6bn [CALCULATION: 0.15 × $37.08bn]. That survey covered low-wage workers in Chicago, Los Angeles and New York, so it is a sensitivity, not the central case.

### Edge in dollars (each year computed on its own; 2024 is the account year)

| Industry | group's wage bill $bn | group's wage workers m | off-books pay $bn (low/central/high) | off-books workers m | edge $bn |
|---|---|---|---|---|---|
| Construction | 49.2 | 1.15 | 26.6 / 29.5 / 43.5 | 0.62 / 0.69 / 1.02 | 3.26 / 5.18 / 9.94 |
| Landscaping services | 5.9 | 0.18 | 1.7 / 3.5 / 3.5 | 0.05 / 0.11 / 0.11 | 0.19 / 0.57 / 0.76 |
| Services to buildings except landscaping (janitorial) | 5.3 | 0.21 | 1.7 / 3.9 / 3.9 | 0.07 / 0.15 / 0.15 | 0.18 / 0.66 / 0.89 |
| Restaurants and other food services | 23.1 | 0.75 | 0.0 / 0.2 / 13.6 | 0.00 / 0.01 / 0.44 | 0.00 / 0.03 / 3.24 |

| Item | 2024 low | 2024 central | 2024 high | 2012-23 mean low | central | high |
|---|---|---|---|---|---|---|
| off-books pay, $bn | 30.05 | 37.08 | 64.46 | 21.16 | 26.42 | 46.77 |
| off-books workers, m | 0.74 | 0.96 | 1.72 | 0.66 | 0.86 | 1.62 |
| edge, $bn | 3.63 | 6.43 | 14.83 | 2.55 | 4.58 | 10.77 |
| of which payroll taxes, $bn | 2.52 | 4.53 | 10.33 | 1.77 | 3.23 | 7.50 |
| of which workers' comp (and FUTA), $bn | 1.11 | 1.31 | 2.24 | 0.78 | 0.93 | 1.61 |
| of which underpayment, $bn | 0.00 | 0.59 | 2.26 | 0.00 | 0.42 | 1.66 |
| employee FICA kept by the worker, $bn | 2.30 | 1.42 | 0.00 | 1.62 | 1.01 | 0.00 |

Off-books pay is the slope times the group's ACS wage bill for that year. The slope is the central across-state estimate; low and high are the smallest and largest of its four variants. This assumes off-books workers earn the group's average pay, which likely overstates their pay. The 2012–2023 columns are in nominal dollars of each year. The priced industries are construction, landscaping, janitorial and restaurants. Agriculture and private households are not priced; `derived/edges_by_industry.csv` gives the reasons.

| Item | 2024 | 2012-23 mean | 2012-23 min | 2012-23 max |
|---|---|---|---|---|
| off-books workers, m | 0.00 | 0.26 | 0.00 | 0.55 |
| off-books pay, $bn | 0.00 | 7.61 | 0.00 | 19.65 |
| edge at the central rate, $bn | 0.00 | 1.32 | 0.00 | 3.44 |

The level check disagrees with the slope. In 2024, 13.6% of construction's ACS wage workers are imputed unauthorized, so the central slope says 8.1% of the industry's wage workers are the group off the books. Yet construction's national uncovered share, calibrated on the six low-exposure industries, averaged 3.0% in 2012–2023 and was −2.2% in 2024.

Either the calibration misstates construction's definitional gap, or the cross-state slope picks up something else that rises with the group's share. The calibration set includes management of companies, where QCEW counts 13 times the ACS. The slope could reflect other informal workers, or ACS–QCEW differences that vary by state. These data cannot settle it. The winners-and-losers rows therefore take their low end from the level check and their central and high ends from the slope.

## Test B. Uncovered employment

### Levels

| Industry | set | ACS private wage and salary workers m | QCEW jobs m | U raw (min to max over years) | U calibrated | U with incorporated self-employed | Mexico-born noncitizen % | imputed unauthorized % |
|---|---|---|---|---|---|---|---|---|
| Crop production | focus | 0.74 | 0.55 | 0.254 (0.191 to 0.319) | 0.224 | 0.334 | 34.2 | 26.6 |
| Support activities for agriculture | focus | 0.11 | 0.37 | -2.296 (-2.910 to -1.755) | -2.427 | -1.986 | 29.7 | 20.7 |
| Landscaping services | focus | 0.81 | 0.76 | 0.054 (-0.087 to 0.180) | 0.016 | 0.167 | 21.5 | 24.2 |
| Animal production | focus | 0.31 | 0.26 | 0.151 (-0.031 to 0.287) | 0.117 | 0.272 | 20.3 | 18.5 |
| Services to buildings except landscaping (janitorial) | focus | 1.04 | 1.30 | -0.259 (-0.359 to -0.202) | -0.309 | -0.145 | 13.5 | 18.9 |
| Construction | focus | 7.36 | 6.88 | 0.067 (0.042 to 0.091) | 0.030 | 0.162 | 11.1 | 13.6 |
| Private households | focus | 0.31 | 0.30 | 0.049 (-0.829 to 0.314) | 0.012 | 0.126 | 8.0 | 17.1 |
| Restaurants and other food services | focus | 8.77 | 10.70 | -0.220 (-0.347 to -0.154) | -0.269 | -0.188 | 6.7 | 9.3 |
| Accommodation |  | 1.43 | 1.83 | -0.287 (-0.485 to -0.166) | -0.339 | -0.265 | 6.3 | 10.1 |
| Forestry, logging, fishing |  | 0.09 | 0.06 | 0.294 (0.245 to 0.349) | 0.266 | 0.396 | 4.6 | 5.5 |
| Manufacturing |  | 14.88 | 12.37 | 0.168 (0.154 to 0.182) | 0.135 | 0.184 | 4.0 | 6.4 |
| Wholesale trade |  | 3.50 | 5.83 | -0.677 (-1.027 to -0.561) | -0.744 | -0.591 | 3.7 | 5.5 |
| Mining |  | 0.73 | 0.67 | 0.085 (0.021 to 0.132) | 0.049 | 0.106 | 3.4 | 4.1 |
| Repair, personal and membership services |  | 5.16 | 4.05 | 0.215 (0.195 to 0.263) | 0.184 | 0.271 | 3.3 | 5.6 |
| Other administrative, support and waste services |  | 3.26 | 6.82 | -1.096 (-1.257 to -0.970) | -1.180 | -1.014 | 2.7 | 4.7 |
| Transportation and warehousing |  | 5.30 | 5.18 | 0.024 (-0.027 to 0.069) | -0.015 | 0.073 | 2.6 | 4.8 |
| Drinking places |  | 0.20 | 0.37 | -0.904 (-1.218 to -0.569) | -0.981 | -0.796 | 2.4 | 4.0 |
| Real estate and rental |  | 2.06 | 2.17 | -0.053 (-0.165 to 0.008) | -0.095 | 0.087 | 2.1 | 3.7 |
| Retail trade |  | 15.91 | 15.43 | 0.030 (0.012 to 0.067) | -0.008 | 0.061 | 2.0 | 3.9 |
| Arts, entertainment and recreation |  | 2.39 | 2.17 | 0.093 (0.037 to 0.205) | 0.057 | 0.142 | 1.8 | 3.5 |
| Utilities | low exposure | 0.93 | 0.55 | 0.407 (0.375 to 0.460) | 0.384 | 0.413 | 1.1 | 2.2 |
| Health care and social assistance (private) |  | 18.21 | 19.15 | -0.051 (-0.085 to -0.010) | -0.093 | -0.021 | 1.0 | 2.9 |
| Management of companies | low exposure | 0.17 | 2.29 | -13.588 (-21.050 to -8.197) | -14.150 | -13.319 | 0.9 | 3.8 |
| Information | low exposure | 2.62 | 2.81 | -0.073 (-0.165 to 0.028) | -0.116 | -0.035 | 0.8 | 4.6 |
| Educational services (private) | low exposure | 5.04 | 2.81 | 0.442 (0.388 to 0.486) | 0.420 | 0.451 | 0.7 | 4.5 |
| Professional and technical services | low exposure | 9.05 | 9.19 | -0.022 (-0.087 to 0.049) | -0.062 | 0.074 | 0.6 | 6.5 |
| Finance and insurance | low exposure | 6.69 | 5.92 | 0.114 (0.099 to 0.141) | 0.079 | 0.142 | 0.6 | 3.2 |

U is one minus QCEW employment over ACS private wage and salary workers, counted at the place of work. The calibrated version divides each industry's QCEW/ACS ratio by that of the six low-exposure industries: professional services, finance, private education, management of companies, utilities and information, the third with the lowest 2005–07 Mexico-born noncitizen share.

Definitional gaps dominate the levels: management of companies −13.6, private education +0.44, utilities +0.41, farm support −2.3. The ACS codes farm labour contractors' workers to crop production, while QCEW puts them in 115. National levels alone therefore identify little.

### Slopes (every specification)

| Specification | sample | regressor | slope (SE) | n | clusters |
|---|---|---|---|---|---|
| raw U on Mexico-born noncitizen share | all cells 2012-2023 | m_mexnc | +0.096 (0.186) | 12216 | 51 |
| raw U on imputed unauthorized share | all cells 2012-2023 | m_unauth | +0.273 (0.147) | 12216 | 51 |
| raw U on imputed unauthorized share without a bachelor's degree | all cells 2012-2023 | m_unauth_noba | +0.197 (0.162) | 12216 | 51 |
| raw U on foreign-born noncitizen share | all cells 2012-2023 | m_fbnc | +0.218 (0.119) | 12216 | 51 |
| U with incorporated self-employed on Mexico-born noncitizen share | all cells 2012-2023 | m_mexnc | -0.054 (0.174) | 12216 | 51 |
| split-sample U on Mexico-born noncitizen share | all cells 2012-2023 | m_mexnc_split | +0.075 (0.183) | 24432 | 51 |
| split-sample U on imputed unauthorized share | all cells 2012-2023 | m_unauth_split | +0.188 (0.131) | 24432 | 51 |
| Construction: U on m_mexnc, across states | c23 | m_mexnc | +0.371 (0.109) | 610 | 51 |
| Construction: U on m_mexnc, within state over time | c23 | m_mexnc | +0.608 (0.240) | 610 | 51 |
| Construction: U on m_mexnc, across states, without California and Texas | c23 | m_mexnc | +0.280 (0.184) | 586 | 49 |
| Construction: U on m_mexnc, across states, unweighted | c23 | m_mexnc | +0.324 (0.162) | 610 | 51 |
| Construction: U on m_unauth, across states | c23 | m_unauth | +0.600 (0.099) | 610 | 51 |
| Construction: U on m_unauth, within state over time | c23 | m_unauth | +0.884 (0.154) | 610 | 51 |
| Construction: U on m_unauth, across states, without California and Texas | c23 | m_unauth | +0.542 (0.158) | 586 | 49 |
| Construction: U on m_unauth, across states, unweighted | c23 | m_unauth | +0.847 (0.221) | 610 | 51 |
| Landscaping services: U on m_mexnc, across states | c56173 | m_mexnc | +0.532 (0.086) | 372 | 36 |
| Landscaping services: U on m_mexnc, within state over time | c56173 | m_mexnc | +0.168 (0.151) | 370 | 36 |
| Landscaping services: U on m_mexnc, across states, without California and Texas | c56173 | m_mexnc | +0.381 (0.199) | 348 | 34 |
| Landscaping services: U on m_mexnc, across states, unweighted | c56173 | m_mexnc | +0.348 (0.173) | 372 | 36 |
| Landscaping services: U on m_unauth, across states | c56173 | m_unauth | +0.589 (0.154) | 372 | 36 |
| Landscaping services: U on m_unauth, within state over time | c56173 | m_unauth | +0.432 (0.136) | 370 | 36 |
| Landscaping services: U on m_unauth, across states, without California and Texas | c56173 | m_unauth | +0.304 (0.196) | 348 | 34 |
| Landscaping services: U on m_unauth, across states, unweighted | c56173 | m_unauth | +0.293 (0.193) | 372 | 36 |
| Services to buildings except landscaping (janitorial): U on m_mexnc, across states | c5617z | m_mexnc | +0.823 (0.213) | 419 | 39 |
| Services to buildings except landscaping (janitorial): U on m_mexnc, within state over time | c5617z | m_mexnc | +0.486 (0.258) | 417 | 39 |
| Services to buildings except landscaping (janitorial): U on m_mexnc, across states, without California and Texas | c5617z | m_mexnc | +0.442 (0.358) | 395 | 37 |
| Services to buildings except landscaping (janitorial): U on m_mexnc, across states, unweighted | c5617z | m_mexnc | +0.748 (0.254) | 419 | 39 |
| Services to buildings except landscaping (janitorial): U on m_unauth, across states | c5617z | m_unauth | +0.739 (0.269) | 419 | 39 |
| Services to buildings except landscaping (janitorial): U on m_unauth, within state over time | c5617z | m_unauth | +0.487 (0.182) | 417 | 39 |
| Services to buildings except landscaping (janitorial): U on m_unauth, across states, without California and Texas | c5617z | m_unauth | +0.315 (0.229) | 395 | 37 |
| Services to buildings except landscaping (janitorial): U on m_unauth, across states, unweighted | c5617z | m_unauth | +0.623 (0.231) | 419 | 39 |
| Restaurants and other food services: U on m_mexnc, across states | c722z | m_mexnc | +0.160 (0.134) | 609 | 51 |
| Restaurants and other food services: U on m_mexnc, within state over time | c722z | m_mexnc | +0.548 (0.204) | 609 | 51 |
| Restaurants and other food services: U on m_mexnc, across states, without California and Texas | c722z | m_mexnc | +0.308 (0.236) | 585 | 49 |
| Restaurants and other food services: U on m_mexnc, across states, unweighted | c722z | m_mexnc | +0.494 (0.144) | 609 | 51 |
| Restaurants and other food services: U on m_unauth, across states | c722z | m_unauth | +0.008 (0.169) | 609 | 51 |
| Restaurants and other food services: U on m_unauth, within state over time | c722z | m_unauth | +0.587 (0.231) | 609 | 51 |
| Restaurants and other food services: U on m_unauth, across states, without California and Texas | c722z | m_unauth | -0.040 (0.235) | 585 | 49 |
| Restaurants and other food services: U on m_unauth, across states, unweighted | c722z | m_unauth | -0.141 (0.358) | 609 | 51 |
| Private households: U on m_mexnc, across states | c814 | m_mexnc | -0.156 (0.716) | 192 | 22 |
| Private households: U on m_mexnc, within state over time | c814 | m_mexnc | +2.033 (1.133) | 190 | 22 |
| Private households: U on m_mexnc, across states, without California and Texas | c814 | m_mexnc | +2.031 (0.980) | 168 | 20 |
| Private households: U on m_mexnc, across states, unweighted | c814 | m_mexnc | +0.810 (0.717) | 192 | 22 |
| Private households: U on m_unauth, across states | c814 | m_unauth | +0.344 (0.814) | 192 | 22 |
| Private households: U on m_unauth, within state over time | c814 | m_unauth | +1.258 (0.748) | 190 | 22 |
| Private households: U on m_unauth, across states, without California and Texas | c814 | m_unauth | +0.816 (0.717) | 168 | 20 |
| Private households: U on m_unauth, across states, unweighted | c814 | m_unauth | +0.486 (0.663) | 192 | 22 |
| Crop production: U on m_mexnc, across states | c111 | m_mexnc | -0.350 (0.286) | 395 | 39 |
| Crop production: U on m_mexnc, within state over time | c111 | m_mexnc | +0.448 (0.101) | 394 | 39 |
| Crop production: U on m_mexnc, across states, without California and Texas | c111 | m_mexnc | -1.127 (0.195) | 371 | 37 |
| Crop production: U on m_mexnc, across states, unweighted | c111 | m_mexnc | -0.699 (0.244) | 395 | 39 |
| Crop production: U on m_unauth, across states | c111 | m_unauth | -0.716 (0.328) | 395 | 39 |
| Crop production: U on m_unauth, within state over time | c111 | m_unauth | +0.559 (0.136) | 394 | 39 |
| Crop production: U on m_unauth, across states, without California and Texas | c111 | m_unauth | -1.142 (0.253) | 371 | 37 |
| Crop production: U on m_unauth, across states, unweighted | c111 | m_unauth | -0.870 (0.244) | 395 | 39 |
| Animal production: U on m_mexnc, across states | c112 | m_mexnc | -0.078 (0.223) | 292 | 31 |
| Animal production: U on m_mexnc, within state over time | c112 | m_mexnc | -0.132 (0.173) | 290 | 31 |
| Animal production: U on m_mexnc, across states, without California and Texas | c112 | m_mexnc | -0.522 (0.247) | 268 | 29 |
| Animal production: U on m_mexnc, across states, unweighted | c112 | m_mexnc | -0.306 (0.249) | 292 | 31 |
| Animal production: U on m_unauth, across states | c112 | m_unauth | -0.217 (0.284) | 292 | 31 |
| Animal production: U on m_unauth, within state over time | c112 | m_unauth | +0.060 (0.147) | 290 | 31 |
| Animal production: U on m_unauth, across states, without California and Texas | c112 | m_unauth | -0.461 (0.292) | 268 | 29 |
| Animal production: U on m_unauth, across states, unweighted | c112 | m_unauth | -0.343 (0.307) | 292 | 31 |
| placebo: low-exposure cells only | low-exposure cells 2012-2023 | m_mexnc | -2.241 (2.649) | 2970 | 51 |
| raw U on imputed unauthorized share, agriculture excluded (own UI coverage rules) | all cells except agriculture 2012-2023 | m_unauth | +0.616 (0.153) | 11446 | 51 |
| raw U on Mexico-born noncitizen share, agriculture excluded | all cells except agriculture 2012-2023 | m_mexnc | +0.473 (0.175) | 11446 | 51 |
| raw U on imputed unauthorized share without a bachelor's degree, agriculture excluded | all cells except agriculture 2012-2023 | m_unauth_noba | +0.562 (0.166) | 11446 | 51 |
| check: U of other admin and support (temp help) on construction's unauthorized share | c56r | m_unauth of c23 | -0.177 (0.506) | 553 | 48 |

**Reading the slopes:**

- In construction, landscaping and janitorial services, the uncovered share rises by 0.3–0.9 per unit of the imputed-unauthorized share, and every variant is positive. Construction is 0.60 (SE 0.10) across states, 0.54 (0.16) without California and Texas, and 0.88 (0.15) within states over time.
- Restaurants show nothing across states (0.01, SE 0.17) but 0.59 (0.23) within states over time.
- Crop production is negative across states. State UI law exempts small farms to different degrees, so QCEW farm coverage differs by state.
- Private households have only 22 usable states and are imprecise.
- The Mexico-born noncitizen share gives smaller slopes (construction 0.37, SE 0.11) than the imputed-unauthorized share. That is expected: most Mexico-born noncitizens with papers work on the books.
- Across all industries the pooled slope is 0.27 (SE 0.15). Without agriculture it is 0.62 (0.15), and 0.56 (0.17) for workers without a bachelor's degree; the agriculture-excluded specification was added after the agriculture slopes were seen.
- The split-sample version, which removes the sampling error shared between U and the share, is lower (0.19 vs 0.27, all industries), so part of the raw pooled slope may be shared error.
- Temp help (other administrative services) shows no rise with construction's group share (−0.18, SE 0.51), so the construction slope is not workers placed by temp agencies being coded to construction.

Consistency with the account's on-books share:

- The pooled agriculture-excluded slope implies about 0.38 of the group's wage workers on the books, by head count.
- SSA's 2010 actuarial count had 44% of unauthorized workers paying payroll tax [SOURCE: SSA Actuarial Note 151, pp. 3–4, as read in `../onbooks_share_2026_09_23/RESULT.md`].
- The adopted account uses 0.52 by dollars, range 0.42–0.63 (`../onbooks_share_2026_09_23`).

The slope sits at the low edge of that range and the level check far above it. Test B brackets the account's assumption; it does not give grounds to move it.

### The group's own businesses

| Industry | unincorporated self-employed 2024, thousand | of whom imputed unauthorized, thousand | share 2024 % | share 2012-23 mean % | Mexico-born noncitizen, thousand | incorporated self-employed, thousand | QCEW establishments 2024, thousand |
|---|---|---|---|---|---|---|---|
| Construction | 1,594 | 239 | 15.0 | 11.8 | 191 | 961 | 938 |
| Landscaping services | 322 | 49 | 15.3 | 15.8 | 62 | 128 | 123 |
| Services to buildings except landscaping (janitorial) | 433 | 84 | 19.5 | 16.5 | 65 | 136 | 129 |
| Restaurants and other food services | 250 | 31 | 12.4 | 11.9 | 24 | 301 | 671 |
| Private households | 289 | 55 | 19.2 | 22.6 | 38 | 29 | 191 |
| Crop production | 232 | 7 | 3.1 | 1.8 | 8 | 92 | 52 |
| Animal production | 141 | 3 | 2.0 | 1.1 | 2 | 46 | 29 |
| Support activities for agriculture | 24 | 1 | 2.3 | 2.7 | 0 | 12 | 22 |

In the operator's sense, the group's own businesses are these self-employed operators. In 2024 the ACS counts 239,000 imputed-unauthorized unincorporated self-employed in construction, 15.0% of the industry's 1.59m. The shares in landscaping, janitorial, restaurants and private households are 12–20%. The ACS does not say whether they employ anyone. Their income falls in the IRS category where 57% of nonfarm proprietor income goes unreported. That tax loss is inside the account, as noted under the IRS table.

Workers misclassified as contractors who report themselves as self-employed are outside U, so the edge above excludes 1099 misclassification. The construction studies above include it: 12.4–20.5% of construction workers were misclassified or off the books in 2017, with no split by nativity (Ormiston–Belman–Erlich 2020, p. 3).

## Test C. Do compliant firms lose ground?

### Pre-registration (written before any outcome regression was run; unchanged)

#### P1. E-Verify mandates, stacked triple-difference event study

A state mandate widens the cost gap between compliant and noncompliant employers: an on-books
employer can no longer hire on a borrowed or false Social Security number, while an employer who
pays off the books is unaffected. If noncompliance drives out compliant firms, the gap's widening
should shift work out of UI coverage and shrink covered establishments and employment in the
industries where unauthorized workers concentrate. The design identifies the effect of widening
the gap, not the effect of the gap's level.

- **Treated states and event years** (first calendar year of a mandate with no alternative to
  E-Verify, covering most private hires; dates from the statute table in
  `reads/LIT_FIRMS_EVERIFY.md`): Arizona 2008, Mississippi 2008 (phase-in complete 2011),
  South Carolina 2012, Alabama 2012, Georgia 2012 (phase-in to 2013), North Carolina 2013.
  Secondary set adds Utah 2010. Tennessee 2023 and Florida 2023 have at most two post years and
  enter only a descriptive check. Louisiana (E-Verify or kept documents) is not a mandate.
- **Controls:** states with no private-employer mandate or option law through 2024 (all states
  except the ten named above).
- **Units:** state (of work) × industry cell × year, 2005–2024.
- **Exposure groups:** high = the brief's cells (construction c23, landscaping c56173, other
  services to buildings c5617z, restaurants c722z, private households c814, crop c111, animal
  c112, farm support c115); low = the third of the other cells with the lowest 2005–2007 national
  Mexico-born noncitizen share of private wage and salary workers.
- **Outcomes:** (O1) uncovered share U = 1 − QCEW employment / ACS private wage and salary
  workers; (O2) ln QCEW establishments; (O3) ln QCEW employment; (O4) ln QCEW average weekly wage;
  (O5) Mexico-born noncitizen share of ACS private wage and salary workers; (O6) unincorporated
  self-employment of Mexico-born noncitizens per ACS private wage and salary worker.
- **Estimator:** one stack per treated state (the state plus all control states, event time
  −4…+5, reference −1); regression of each outcome on event-time × treated × high-exposure, with
  stack × state × cell, stack × cell × year and stack × state × year fixed effects. Cells are
  weighted by their pre-period (event time −1) ACS unweighted sample count. Standard errors are
  clustered by state. Reported: each event-time coefficient, the post average (0…+5), and a joint
  test of the pre coefficients (−4…−2).
- **Support for the operator's mechanism:** O1 > 0 and O2, O3 < 0 in the post average, with flat
  pre-trends. O5 < 0 alone means departure of workers rather than informalization.
- **Robustness (all reported):** Mississippi event year 2011 and Georgia 2013; secondary set with
  Utah; unweighted; QCEW outcomes on the focus 4- and 6-digit series (specialty trades 2381–2389,
  janitorial 561720, restaurants 7225 / 7221+7222) against low-exposure cells.

#### P2. Panel associations (brief test C), no design

State × cell × year, 2012–2023. Annual first differences of ln QCEW establishments, ln QCEW
employment and ln QCEW average weekly wage on the change in U, with state × year and cell × year
fixed effects, clustered by state; the same on the ACS-only Mexico-born noncitizen share (O5),
which does not contain QCEW employment. Specifications: (a) focus cells, (b) low-exposure placebo
cells, (c) all cells with a focus interaction; contemporaneous and one-year-lagged regressors;
long differences 2012–13 to 2022–23. U contains QCEW employment in its numerator, so the
contemporaneous U-on-employment regression is mechanical and is shown only for completeness.
These are associations.

### P1 results: the design does not identify an effect

| Variant | cells | outcome | post average (SE) | pre-trend p | n | states |
|---|---|---|---|---|---|---|
| main | focus vs low-exposure cells | U | +0.0005 (0.0138) | 0.0931 | 22474 | 47 |
| main | focus vs low-exposure cells | ln_estabs | -0.0179 (0.0153) | 0.0000 | 22474 | 47 |
| main | focus vs low-exposure cells | ln_emp | -0.0604 (0.0342) | 0.0005 | 22474 | 47 |
| main | focus vs low-exposure cells | ln_wkwage | -0.0090 (0.0067) | 0.0111 | 22474 | 47 |
| main | focus vs low-exposure cells | m_mexnc | -0.0275 (0.0149) | 0.0142 | 22474 | 47 |
| main | focus vs low-exposure cells | se_mexnc_per_ws | +0.0017 (0.0024) | 0.5279 | 22474 | 47 |
| MS 2011, GA 2013 | focus vs low-exposure cells | U | +0.0096 (0.0169) | 0.9020 | 22853 | 47 |
| MS 2011, GA 2013 | focus vs low-exposure cells | ln_estabs | -0.0149 (0.0173) | 0.0070 | 22853 | 47 |
| MS 2011, GA 2013 | focus vs low-exposure cells | ln_emp | -0.0552 (0.0372) | 0.0000 | 22853 | 47 |
| MS 2011, GA 2013 | focus vs low-exposure cells | ln_wkwage | -0.0102 (0.0060) | 0.3605 | 22853 | 47 |
| MS 2011, GA 2013 | focus vs low-exposure cells | m_mexnc | -0.0266 (0.0149) | 0.0752 | 22853 | 47 |
| MS 2011, GA 2013 | focus vs low-exposure cells | se_mexnc_per_ws | +0.0034 (0.0022) | 0.8385 | 22853 | 47 |
| with Utah 2010 | focus vs low-exposure cells | U | -0.0009 (0.0127) | 0.3937 | 26330 | 48 |
| with Utah 2010 | focus vs low-exposure cells | ln_estabs | -0.0218 (0.0152) | 0.0000 | 26330 | 48 |
| with Utah 2010 | focus vs low-exposure cells | ln_emp | -0.0587 (0.0319) | 0.0008 | 26330 | 48 |
| with Utah 2010 | focus vs low-exposure cells | ln_wkwage | -0.0079 (0.0069) | 0.0117 | 26330 | 48 |
| with Utah 2010 | focus vs low-exposure cells | m_mexnc | -0.0237 (0.0145) | 0.0767 | 26330 | 48 |
| with Utah 2010 | focus vs low-exposure cells | se_mexnc_per_ws | +0.0018 (0.0023) | 0.5048 | 26330 | 48 |
| unweighted | focus vs low-exposure cells | U | -0.0684 (0.0335) | 0.0012 | 22474 | 47 |
| unweighted | focus vs low-exposure cells | ln_estabs | -0.0183 (0.0231) | 0.0147 | 22474 | 47 |
| unweighted | focus vs low-exposure cells | ln_emp | -0.0523 (0.0306) | 0.0807 | 22474 | 47 |
| unweighted | focus vs low-exposure cells | ln_wkwage | -0.0158 (0.0087) | 0.1904 | 22474 | 47 |
| unweighted | focus vs low-exposure cells | m_mexnc | -0.0456 (0.0137) | 0.0008 | 22474 | 47 |
| unweighted | focus vs low-exposure cells | se_mexnc_per_ws | +0.0120 (0.0093) | 0.5442 | 22474 | 47 |
| main | detail series vs low-exposure cells | ln_estabs | -0.0477 (0.0108) | 0.0000 | 27708 | 47 |
| main | detail series vs low-exposure cells | ln_emp | -0.1222 (0.0512) | 0.0000 | 27708 | 47 |
| main | detail series vs low-exposure cells | ln_wkwage | +0.0109 (0.0105) | 0.0084 | 27708 | 47 |
| unweighted | detail series vs low-exposure cells | ln_estabs | -0.0318 (0.0110) | 0.0001 | 27846 | 47 |
| unweighted | detail series vs low-exposure cells | ln_emp | -0.0785 (0.0434) | 0.0000 | 27846 | 47 |
| unweighted | detail series vs low-exposure cells | ln_wkwage | +0.0030 (0.0073) | 0.0000 | 27846 | 47 |

| Outcome | −4 | −3 | −2 | 0 | +1 | +2 | +3 | +4 | +5 |
|---|---|---|---|---|---|---|---|---|---|
| U | -0.028 (0.016) | -0.014 (0.021) | -0.003 (0.023) | +0.002 (0.019) | +0.011 (0.023) | -0.013 (0.016) | -0.017 (0.011) | -0.017 (0.028) | +0.037 (0.025) |
| ln_estabs | +0.069 (0.014) | +0.028 (0.013) | +0.009 (0.005) | -0.004 (0.006) | -0.008 (0.014) | -0.015 (0.015) | -0.023 (0.018) | -0.029 (0.020) | -0.029 (0.025) |
| ln_emp | +0.036 (0.024) | +0.028 (0.008) | +0.019 (0.006) | -0.020 (0.014) | -0.050 (0.032) | -0.070 (0.039) | -0.071 (0.042) | -0.074 (0.042) | -0.078 (0.041) |
| ln_wkwage | -0.014 (0.011) | -0.023 (0.008) | -0.003 (0.005) | -0.001 (0.006) | -0.008 (0.006) | -0.002 (0.008) | -0.010 (0.007) | -0.016 (0.009) | -0.017 (0.010) |
| m_mexnc | -0.028 (0.013) | -0.018 (0.005) | -0.010 (0.005) | -0.014 (0.007) | -0.019 (0.016) | -0.028 (0.016) | -0.033 (0.017) | -0.034 (0.017) | -0.036 (0.018) |
| se_mexnc_per_ws | -0.002 (0.002) | -0.002 (0.001) | -0.000 (0.001) | +0.000 (0.003) | +0.004 (0.002) | +0.000 (0.002) | -0.001 (0.004) | +0.004 (0.002) | +0.002 (0.004) |
| detail: ln_estabs | +0.111 (0.017) | +0.041 (0.022) | +0.015 (0.010) | -0.019 (0.009) | -0.034 (0.010) | -0.045 (0.010) | -0.055 (0.016) | -0.062 (0.018) | -0.071 (0.019) |
| detail: ln_emp | +0.085 (0.036) | +0.059 (0.014) | +0.049 (0.010) | -0.050 (0.021) | -0.107 (0.047) | -0.136 (0.059) | -0.147 (0.067) | -0.145 (0.059) | -0.148 (0.059) |
| detail: ln_wkwage | -0.011 (0.012) | -0.022 (0.009) | +0.004 (0.006) | -0.002 (0.006) | -0.000 (0.009) | +0.011 (0.013) | +0.016 (0.012) | +0.022 (0.012) | +0.019 (0.015) |

The support criterion is not met. U does not move: +0.0005 (SE 0.014). Establishments and employment fall after the mandates, −1.8% (1.5) and −6.0% (3.4), but they were already falling beforehand, with pre-trend p-values below 0.001 and 0.0005.

The event-time rows show the problem. Establishment counts in the exposed industries of mandate states slid relative to controls from +6.9% four years before the mandate, and kept sliding at about the same pace to −2.9% five years after. This is the housing bust in Arizona and the Southeast running through the window, not a break at the mandate. The establishment pre-test fails in every variant. The employment pre-test fails in every variant except the unweighted one (p = 0.08), where the post average is not significant (−5.2%, SE 3.1) and U falls (−0.068, SE 0.034) instead of rising. No variant shows U rising.

The Mexico-born noncitizen share fell after the mandates (−2.8 points, SE 1.5), which the pre-registration reads as departure rather than informalization, but its pre-trend fails too (p = 0.014).

| Cells | outcome | pre-trend per year | level shift at 0 | slope change after 0 | n |
|---|---|---|---|---|---|
| focus vs low-exposure cells | U | +0.0092 (0.0045) | -0.0178 (0.0147) | -0.0067 (0.0092) | 22474 |
| focus vs low-exposure cells | ln_estabs | -0.0217 (0.0055) | +0.0246 (0.0068) | +0.0162 (0.0075) | 22474 |
| focus vs low-exposure cells | ln_emp | -0.0120 (0.0070) | -0.0254 (0.0345) | +0.0015 (0.0121) | 22474 |
| focus vs low-exposure cells | ln_wkwage | +0.0068 (0.0039) | -0.0078 (0.0033) | -0.0098 (0.0040) | 22474 |
| focus vs low-exposure cells | m_mexnc | +0.0091 (0.0038) | -0.0246 (0.0148) | -0.0138 (0.0049) | 22474 |
| focus vs low-exposure cells | se_mexnc_per_ws | +0.0008 (0.0008) | +0.0002 (0.0030) | -0.0006 (0.0010) | 22474 |
| detail series vs low-exposure cells | ln_estabs | -0.0341 (0.0071) | +0.0228 (0.0097) | +0.0239 (0.0111) | 27708 |
| detail series vs low-exposure cells | ln_emp | -0.0270 (0.0110) | -0.0594 (0.0522) | +0.0095 (0.0185) | 27708 |
| detail series vs low-exposure cells | ln_wkwage | +0.0065 (0.0045) | -0.0100 (0.0057) | -0.0015 (0.0047) | 27708 |

The trend break was not pre-registered; it was added after the pre-trend tests failed. Against the pre-existing slide of −2.2% a year, establishment counts shifted up 2.5% (SE 0.7) at the mandate, and the slide slowed by 1.6 points a year (0.75). At the same time the Mexico-born noncitizen share turned down by 1.4 points a year (0.5), and U did not move.

Read at face value, the group's workers left rather than going off the books, and covered establishments did not shrink relative to trend. The mechanism predicted they would shrink. The reading depends on extending a linear trend through the housing bust, so it identifies nothing and carries no weight in the verdict.

### P2 results: no displacement of covered firms

| Design | sample | regressor | ln establishments | ln employment | ln weekly wage | n |
|---|---|---|---|---|---|---|
| first differences | focus cells | d_U | -0.253 (0.081) | -0.235 (0.069)‡ | +0.081 (0.028) | 2799 |
| first differences | focus cells | d_U_lag | +0.047 (0.038) | +0.038 (0.034) | -0.013 (0.011) | 2499 |
| first differences | focus cells | d_m_mexnc | -0.019 (0.022) | -0.032 (0.024) | +0.004 (0.011) | 2799 |
| first differences | focus cells | d_m_mexnc_lag | +0.047 (0.045) | +0.058 (0.037) | -0.032 (0.017) | 2499 |
| first differences | focus cells | d_m_unauth | +0.005 (0.021) | -0.008 (0.017) | +0.010 (0.013) | 2799 |
| first differences | focus cells | d_m_unauth_lag | +0.092 (0.070) | +0.090 (0.056) | -0.041 (0.025) | 2499 |
| first differences | low-exposure placebo cells | d_U | -0.002 (0.001) | -0.008 (0.002)‡ | -0.001 (0.001) | 2906 |
| first differences | low-exposure placebo cells | d_U_lag | +0.001 (0.002) | -0.001 (0.001) | -0.000 (0.002) | 2638 |
| first differences | low-exposure placebo cells | d_m_mexnc | -0.055 (0.076) | +0.097 (0.079) | +0.171 (0.147) | 2906 |
| first differences | low-exposure placebo cells | d_m_mexnc_lag | +0.074 (0.097) | +0.134 (0.081) | -0.049 (0.085) | 2638 |
| first differences | low-exposure placebo cells | d_m_unauth | -0.035 (0.028) | +0.015 (0.024) | +0.027 (0.041) | 2906 |
| first differences | low-exposure placebo cells | d_m_unauth_lag | -0.010 (0.027) | +0.032 (0.034) | +0.045 (0.053) | 2638 |
| first differences | all cells | d_U | -0.078 (0.040) | -0.059 (0.021)‡ | +0.014 (0.010) | 11922 |
| first differences | all cells | d_U_lag | +0.012 (0.006) | +0.005 (0.006) | -0.003 (0.003) | 10787 |
| first differences | all cells | d_m_mexnc | +0.011 (0.038) | -0.027 (0.015) | -0.010 (0.010) | 11922 |
| first differences | all cells | d_m_mexnc_lag | +0.005 (0.022) | +0.057 (0.023) | -0.001 (0.013) | 10787 |
| first differences | all cells | d_m_unauth | -0.029 (0.045) | -0.021 (0.018) | +0.012 (0.015) | 11922 |
| first differences | all cells | d_m_unauth_lag | +0.043 (0.062) | +0.047 (0.026) | -0.014 (0.017) | 10787 |
| first differences, focus interaction | all cells | x_focus [d_U_lag] | +0.050 (0.040) | +0.038 (0.032) | -0.010 (0.011) | 10787 |
| first differences, focus interaction | all cells | x_focus [d_m_mexnc_lag] | +0.242 (0.217) | +0.027 (0.055) | -0.093 (0.057) | 10787 |
| first differences, focus interaction | all cells | x_focus [d_m_unauth_lag] | +0.096 (0.067) | +0.048 (0.050) | -0.072 (0.036) | 10787 |
| long difference 2012-13 to 2022-23 | focus cells | dU | -0.678 (0.147) | -0.581 (0.090)‡ | +0.208 (0.060) | 220 |
| long difference 2012-13 to 2022-23 | focus cells | dm_mexnc | +0.239 (0.380) | +0.614 (0.311) | -0.580 (0.134) | 220 |
| long difference 2012-13 to 2022-23 | focus cells | dm_unauth | +0.370 (0.437) | +0.461 (0.376) | -0.291 (0.101) | 220 |
| long difference 2012-13 to 2022-23 | low-exposure placebo cells | dU | -0.058 (0.040) | -0.106 (0.047)‡ | -0.018 (0.011) | 238 |
| long difference 2012-13 to 2022-23 | low-exposure placebo cells | dm_mexnc | +0.513 (1.787) | -0.856 (2.393) | -1.556 (1.260) | 238 |
| long difference 2012-13 to 2022-23 | low-exposure placebo cells | dm_unauth | +0.068 (0.956) | +2.414 (0.989) | +0.663 (0.277) | 238 |
| long difference 2012-13 to 2022-23 | all cells | dU | -0.373 (0.169) | -0.378 (0.091)‡ | +0.087 (0.059) | 969 |
| long difference 2012-13 to 2022-23 | all cells | dm_mexnc | +0.242 (0.660) | +0.756 (0.184) | -0.639 (0.244) | 969 |
| long difference 2012-13 to 2022-23 | all cells | dm_unauth | +0.262 (0.359) | +0.635 (0.128) | -0.150 (0.092) | 969 |
| first differences, detail series (year FE only) | q238 | d_U_lag | -0.015 (0.013) | -0.014 (0.018) | -0.011 (0.007) | 557 |
| first differences, detail series net of the state's low-exposure cells | q238 | d_U_lag | -0.004 (0.010) | -0.015 (0.017) | +0.010 (0.013) | 557 |
| first differences, detail series (year FE only) | q238 | d_m_mexnc_lag | -0.189 (0.056) | -0.069 (0.068) | -0.045 (0.036) | 557 |
| first differences, detail series net of the state's low-exposure cells | q238 | d_m_mexnc_lag | -0.024 (0.037) | +0.083 (0.070) | -0.022 (0.043) | 557 |
| first differences, detail series (year FE only) | q2381 | d_U_lag | -0.007 (0.016) | -0.015 (0.030) | -0.002 (0.013) | 557 |
| first differences, detail series net of the state's low-exposure cells | q2381 | d_U_lag | +0.004 (0.014) | -0.016 (0.030) | +0.020 (0.020) | 557 |
| first differences, detail series (year FE only) | q2381 | d_m_mexnc_lag | -0.258 (0.085) | -0.161 (0.084) | -0.029 (0.075) | 557 |
| first differences, detail series net of the state's low-exposure cells | q2381 | d_m_mexnc_lag | -0.093 (0.076) | -0.010 (0.076) | -0.006 (0.076) | 557 |
| first differences, detail series (year FE only) | q2382 | d_U_lag | -0.013 (0.013) | -0.015 (0.020) | -0.024 (0.009) | 557 |
| first differences, detail series net of the state's low-exposure cells | q2382 | d_U_lag | -0.002 (0.013) | -0.017 (0.019) | -0.003 (0.014) | 557 |
| first differences, detail series (year FE only) | q2382 | d_m_mexnc_lag | -0.168 (0.056) | -0.062 (0.070) | -0.048 (0.033) | 557 |
| first differences, detail series net of the state's low-exposure cells | q2382 | d_m_mexnc_lag | -0.003 (0.047) | +0.089 (0.071) | -0.025 (0.043) | 557 |
| first differences, detail series (year FE only) | q2383 | d_U_lag | -0.023 (0.016) | +0.019 (0.034) | -0.010 (0.010) | 557 |
| first differences, detail series net of the state's low-exposure cells | q2383 | d_U_lag | -0.012 (0.013) | +0.017 (0.033) | +0.011 (0.015) | 557 |
| first differences, detail series (year FE only) | q2383 | d_m_mexnc_lag | -0.236 (0.074) | +0.023 (0.113) | -0.003 (0.048) | 557 |
| first differences, detail series net of the state's low-exposure cells | q2383 | d_m_mexnc_lag | -0.071 (0.052) | +0.174 (0.124) | +0.019 (0.051) | 557 |
| first differences, detail series (year FE only) | q2389 | d_U_lag | -0.004 (0.016) | -0.025 (0.023) | +0.022 (0.012) | 557 |
| first differences, detail series net of the state's low-exposure cells | q2389 | d_U_lag | +0.007 (0.013) | -0.027 (0.023) | +0.043 (0.017) | 557 |
| first differences, detail series (year FE only) | q2389 | d_m_mexnc_lag | -0.053 (0.069) | -0.016 (0.067) | -0.106 (0.061) | 557 |
| first differences, detail series net of the state's low-exposure cells | q2389 | d_m_mexnc_lag | +0.112 (0.060) | +0.136 (0.073) | -0.083 (0.067) | 557 |
| first differences, detail series (year FE only) | q561720 | d_U_lag | -0.006 (0.011) | -0.003 (0.004) | -0.001 (0.003) | 368 |
| first differences, detail series net of the state's low-exposure cells | q561720 | d_U_lag | +0.001 (0.008) | -0.002 (0.004) | -0.004 (0.005) | 368 |
| first differences, detail series (year FE only) | q561720 | d_m_mexnc_lag | -0.062 (0.030) | -0.017 (0.026) | -0.021 (0.012) | 368 |
| first differences, detail series net of the state's low-exposure cells | q561720 | d_m_mexnc_lag | -0.024 (0.025) | -0.009 (0.027) | -0.000 (0.014) | 368 |
| first differences, detail series (year FE only) | q7225 | d_U_lag | +0.003 (0.010) | -0.009 (0.013) | +0.012 (0.006) | 552 |
| first differences, detail series net of the state's low-exposure cells | q7225 | d_U_lag | -0.008 (0.009) | -0.001 (0.014) | -0.005 (0.012) | 552 |
| first differences, detail series (year FE only) | q7225 | d_m_mexnc_lag | -0.120 (0.103) | -0.110 (0.075) | +0.007 (0.059) | 552 |
| first differences, detail series net of the state's low-exposure cells | q7225 | d_m_mexnc_lag | -0.041 (0.072) | -0.003 (0.051) | +0.011 (0.065) | 552 |

‡ mechanical: U contains QCEW employment.

**What P2 shows:**

- **Regressors that exclude QCEW show no displacement.** With the ACS-only shares, covered establishments and employment in the focus industries show no negative association:
  - lagged imputed-unauthorized share: +0.09 (SE 0.07) for establishments, +0.09 (0.06) for employment;
  - long differences: +0.37 (0.44) and +0.46 (0.38);
  - across all industries, long-difference employment rises with the group's share (+0.64, SE 0.13), as expected when workers move toward growing industries and places;
  - the placebo industries are null except in the long differences on the imputed-unauthorized share (employment +2.4, SE 1.0; wages +0.66, SE 0.28), where the flag picks up temporary-visa professionals in growing industries.
- **The U regressors are close to mechanical.** U contains QCEW employment, and establishments move with employment, so the contemporaneous negative coefficients on U reflect that construction. Lagged U: +0.05 (0.04).
- **The specialty-trades association does not survive.** Specialty-trade establishments fell with the lagged Mexico-born noncitizen share when only year effects are used: −0.17 to −0.26 in 2381, 2382 and 2383. That specification cannot remove state-wide cycles. Net of the same state's low-exposure industries, the coefficients are −0.09 to +0.11 and none is significant. That check was added after the year-effects results were seen.
- **Wages lean negative in the pooled specifications:**
  - long difference: −0.29 (0.10) on the imputed-unauthorized share, −0.58 (0.13) on the Mexico-born noncitizen share;
  - first differences, lagged: −0.04 (0.025);
  - focus interaction: −0.07 (0.036).

### Is the wage association composition?

| Industry | group share % | group pay / others' pay | off-books share used | composition-only slope | long difference net of low-exposure cells (SE) | states |
|---|---|---|---|---|---|---|
| Crop production | 26.6 | 0.68 | 0.00 | -0.356 | +0.04 (0.21) | 30 |
| Animal production | 18.5 | 0.90 | 0.00 | -0.106 | +0.03 (0.16) | 20 |
| Construction | 13.6 | 0.64 | 0.60 | -0.175 | +0.41 (0.45) | 51 |
| Landscaping services | 24.2 | 0.84 | 0.59 | -0.091 | -0.01 (0.10) | 28 |
| Services to buildings except landscaping (janitorial) | 18.9 | 0.75 | 0.74 | -0.090 | +0.37 (0.20) | 31 |
| Restaurants and other food services | 9.3 | 1.13 | 0.01 | +0.131 | +0.27 (0.14) | 48 |
| Private households | 17.1 | 0.83 | 0.34 | -0.127 |  | 12 |
| all focus cells | 13.0 | 0.89 |  | -0.033 |  |  |

Composition means that the group's on-books workers are counted in QCEW's average and are paid differently, not that anyone's wage falls. It predicts −0.03 for the focus industries together: −0.17 in construction, and +0.13 in restaurants, where the group works longer hours than the industry's many part-timers. So composition does not explain the pooled −0.29.

But the pooled estimate compares industries within a state. Compared across states within an industry, net of the state's low-exposure industries, the wage association is zero or positive:

| Industry | Coefficient (SE) |
|---|---|
| Construction | +0.41 (0.45) |
| Janitorial | +0.37 (0.20) |
| Restaurants | +0.27 (0.14) |
| Landscaping | −0.01 (0.10) |

The per-industry version was added after the pooled result was seen. The wage association therefore depends on the comparison and is not robust. It is not evidence that compliant firms' workers lose pay.

## Test D. Literature

Every number below is quoted in the reading notes with its page or table and re-found in the cached text by `quote_check.py`. The notes are [LIT_FIRMS_EVERIFY](reads/LIT_FIRMS_EVERIFY.md) and [LIT_COMPLIANCE_COSTS](reads/LIT_COMPLIANCE_COSTS.md).

| Source | Population | Finding | Where | Weight |
|---|---|---|---|---|
| Brown, Hotchkiss & Quispe-Agnoli, IZA DP 3936 (2009) | Georgia UI records, firms 1995–2005; undocumented workers identified by invalid SSNs on the payroll | Own undocumented hiring lowers quarterly exit by 0.76 points in construction (base about 2%). Rivals' hiring raises exit in 4 of 12 sectors, but not significantly in construction (0.492, SE 0.516), agriculture (−0.638, 0.666) or leisure and hospitality (0.045, 0.501). | p. 22; Table 3 | The only firm-level test of the mechanism. Observational, with no instrument. Covers only on-books employers, not cash firms. |
| Hotchkiss, Quispe-Agnoli & Rios-Avila (2012 WP; 2013 draft) | Georgia UI records, documented workers | +0.44% wage per point of the county-industry undocumented share (SE 0.0002 per point). At the firm level the sign depends on the fixed effects, and every estimate is under 1% per point. | 2013 draft Table 4 col. 7; WP 2012-4 p. 23 | The coworker wage channel is small. |
| Bohn & Lofstrom, IZA DP 6598 (2012) | Arizona, CPS, likely-unauthorized men (non-citizen Hispanic, high school or less) | After the 2008 mandate, wage and salary employment fell about 11 points; self-employment rose 8.3 points (significant at 5% by permutation), "roughly a doubling". | pp. 19–25 | Synthetic control on one state. Enforcement pushed work toward the least compliant segment. |
| Bohn, Lofstrom & Raphael (2014 WP) | Arizona, low-skilled natives | Employment of low-skilled white native men fell 4.4 points; the mandate "does not appear to have improved labor market outcomes of competing legal low-skilled workers". | results pp. 18–26 | One state, during the recession |
| Orrenius & Zavodny (IZA 2014, SEJ 2015) | CPS, likely-unauthorized Mexican immigrants in mandate states | Men's hourly earnings −0.075 (0.019); employment 0.006 (0.016); self-employment −0.008 (0.015). | Table 2 | Fewer than 4% of the sample live in mandate states. |
| Amuedo-Dorantes & Bansak, IZA DP 7419 (2013) | CPS | Likely-unauthorized employment −4.6 points; natives +2 points (SEs in a table not extracted) | pp. 13–16 | Disagrees with the two studies above on natives |
| Ayromloo, Feigenberg & Lubotsky, NBER w26676 | QWI and County Business Patterns (CBP) counties, 2004–2015 | Hispanic employment −8.7%. Establishments of big firms −0.027 (0.013). All establishments −0.004 (0.014), "small and statistically insignificant". Mandates covered 12.3% of private hires by 2015. | Table 6; p. 9 | Compliance fell on large firms; activity shifted to small ones. |
| Shrestha & Sant'Anna (2026 WP) | Secure Communities rollout, county-sector Census data | Firms −3.4%, establishments −2.9% (both significant at 1%); entry −9.5%; exit not significant | introduction | Police enforcement, not E-Verify. SEs are in tables not read. |
| Shrestha & Kostandini (2024), JAAE | 287(g) counties | Businesses per 1,000 residents −6% | results | The authors report significant pre-trends in two panels. |
| Bernhardt et al. (2009) | Low-wage workers in three cities, 2008 | Minimum-wage violations: U.S.-born 15.6%, authorized immigrants 21.3%, unauthorized 37.1%. Lost pay 15% of earnings. The report says "Nor are these abuses limited to unauthorized immigrants". | Table 5.1 p. 46; p. 9; p. 13 | A survey, not enforcement data. Three large metros. |
| Ormiston, Belman & Erlich (2020) | U.S. construction, 2017, the same ACS–payroll residual method | 12.4–20.5% of construction workers misclassified or off the books; savings 12.5–23.5% of legal labor cost | p. 3; p. 36; Table A p. 5 | Union-commissioned, which carries no weight either way (symmetry rule 3). Not split by nativity. |
| Belman, Bilginsoy, Ormiston & Wenz (ICERES 2025) | One 67-unit Michigan project | Misclassifying all workers saves 4.9% of project cost, 16.1% of labor cost (workers' compensation plus employer FICA only) | p. 3 | One project, not peer reviewed |

Not obtained: the published versions of Brown–Hotchkiss–Quispe-Agnoli (JRS 2013) and Hotchkiss et al. (SEJ 2015); Orrenius–Zavodny (2026, abstract only); Bohn & Owens (2012), "Immigration and Informal Labor", the closest academic analogue to Test B. See the notes' "not obtained" lists.

No U.S. study was found that compares compliant and noncompliant firms competing in the same market after an enforcement change [GAP, both notes].

## Who wins and who loses

`derived/winners_losers_rows.csv` holds the brief's columns. The group names carry NAICS codes, so the ledger's key map can place them.

| Who | channel | sign | $bn low / central / high | $ per person | basis | relation to the account |
|---|---|---|---|---|---|---|
| noncompliant employers | payroll taxes not paid on off-books wages | gain | 0.00 / 4.53 / 10.33 |  | modelled | overlaps:tax_corrections_2026_09_24 |
| noncompliant employers | workers' compensation premiums (with federal unemployment tax, which ECEC Table 4 does not split out) not paid | gain | 0.00 / 1.31 / 2.24 |  | modelled | beside |
| noncompliant employers | wage-and-hour underpayment of their off-books workers | gain | 0.00 / 0.59 / 2.26 |  | modelled | beside |
| informal and unauthorized workers paid off the books | wage-and-hour underpayment | loss | 0.00 / 0.59 / 2.26 | 614 | modelled | beside |
| informal and unauthorized workers paid off the books | employee Social Security and Medicare not withheld and kept in cash | gain | 0.00 / 1.42 / 2.30 | 1,483 | modelled | overlaps:tax_corrections_2026_09_24 |
| informal and unauthorized workers paid off the books | no workers' compensation coverage | loss | 0.00 / 1.31 / 2.24 | 1,374 | assumed | overlaps:uncompensated_care |
| the budget: Social Security and Medicare trust funds and state unemployment-insurance funds | payroll taxes not collected on off-books wages (employer and employee Social Security and Medicare, state UI; income tax not included here) | loss | 0.00 / 5.95 / 10.33 | 20 | modelled | inside |
| customers of the four industries | lower prices where noncompliant firms' cost edge is competed away | gain | 0.00 / 3.21 / 14.83 | 11 | assumed | overlaps:production_term |
| compliant owners | jobs or margin lost to noncompliant rivals | loss | unpriced |  | unpriced | beside |
| workers of compliant firms | wages | loss | unpriced |  | unpriced | overlaps:wage_split |
| noncompliant employers in agriculture (NAICS 111, 112, 115) and private households (NAICS 814) | the same edge | gain | unpriced |  | unpriced | beside |

**How to read the rows:**

- **Noncompliant employers** gain the edge. The ledger cannot identify them; its key map says so. They include native contractors as well as the group's own businesses. [FRAMING-SENSITIVE] Their payroll-tax gain is the same money as the budget's loss, a transfer from taxpayers that the account already carries; it is marked as overlapping and is not added.
- **The budget** loses employer and employee Social Security and Medicare and state UI on off-books pay: $0–10.3bn (central $5.9bn) in 2024. The adopted account carries this inside through the September 24 correction "Tax records: the Census tax model's status and compliance, CPS fill-ins, Mexico-born recount, state-aware status flag (audit rows 2, 13, 4)", +$19.91/+21.21bn alone (`../main_case_2026_09_24/RESULT.md`). It is not priced again. Income tax is not included in the row.
- **Off-books workers** lose underpayment and workers' compensation coverage. They keep some of their own payroll tax. Most are the group, so these are within-group items. The coverage loss is valued at the premium, an upper bound. Its public part (injury care) is inside the account's uncompensated-care line.
- **Customers** gain only if the edge is passed on. The share is unmeasured, and a share of the employers' gain is not additional to it. The row overlaps the production term and the consumer-price lane.
- **Compliant owners and their workers** are unpriced because no loss is measured. Covered establishments and employment show no negative association, and the wage association is not robust. The workers' row also overlaps the account's wage split.
- **Symmetry rule 5 (costs and benefits alike):**
  - The customers' gain is priced only as a bounded share of the measured edge.
  - The compliant owners' loss has no measured basis, so it stays unpriced, and nothing bounds it in these data.
  - Neither enters the ledger's nets: one overlaps, the other is unpriced.

## What this means for the adopted account

- **No new cost channel.** No displacement of compliant firms is measured. The edge's tax part is already inside the account, and its private parts (workers' compensation premiums, underpayment) are transfers between employers and workers beside it.
- **The on-books share stays.** Test B brackets the account's 0.52 without moving it.
- **Beside the account:** workers' compensation premiums avoided of $0–2.2bn (central $1.3bn) and underpayment of $0–2.3bn (central $0.6bn) in 2024. These are private transfers from off-books workers and insurance pools to their employers, within the group where both sides are group members. No change to `engine.js` or any shared file is proposed.

## Steel-man, disconfirmation and bias

**The strongest case for the operator's claim:**

- The edge per dollar is large relative to construction margins: 12–23% of the off-books wage, 3.5–7% of a project's cost when labor is about 30% of it [CALCULATION with ICERES's labor share, p. 3].
- It is concentrated in a few trades.
- The one firm-level study finds that firms hiring undocumented workers survive better. It also finds that rivals' undocumented hiring raises exit in manufacturing, finance, professional services and education and health.
- Enforcement shifts activity to the least compliant segment: Arizona's self-employment doubled, and large establishments lost ground under mandates.
- Enforcement data cannot see the cash economy. The IRS gap on employment tax omits agriculture and households. Our slope places over half of the group's construction wage workers off the books.

**The case against, which prevails on the evidence here:**

- Covered establishments and employment show null or positive associations with the group's share, never the negative one the claim needs.
- The one supportive association disappears with state-wide controls.
- The E-Verify design is not identified.
- The Georgia rival effect is not significant in the three industries the claim is about.
- Removing unauthorized workers lowered business counts.
- Violation rates among U.S.-born low-wage workers (15.6% minimum wage) show the edge is taken wherever low-wage labor is, not only by immigrant firms.

**Framing and bias:**

- [FRAMING-SENSITIVE] "Driving out" can also mean compliant firms losing share of jobs they would otherwise do, with no change in their count. These data measure counts, employment and pay, not market shares of the same jobs.
- This analysis runs through an LLM with post-training dispositions that lean against findings of harm on this topic (`../../../notes/llm-bias-caveat.md`).
- Countermeasures:
  - P1 and P2 were pre-registered;
  - every specification is reported;
  - every post-hoc check is labeled.
- Of the post-hoc checks, three weakened results on the operator's side: the specialty-trade control, the per-industry wage comparison and the level check. One strengthened one: excluding agriculture raised the pooled slope. That imbalance is the direction the instrument's lean would produce, so the unadjusted results stay in the tables beside the checks.

## Would change it

- **An employer–employee test of rival exit in construction with cash firms visible**, for example LEHD with SSA no-match flags by NAICS, showing that rivals' noncompliant hiring raises compliant firms' exit.
- **Florida's 2023 mandate with more post years**, or another mandate outside the housing cycle with flat pre-trends, showing covered establishments grow after a mandate.
- **An independent count of off-books workers by industry and state** that settles the slope versus the level check. It would move the edge anywhere in $0–15bn.
- **Evidence that the ACS undercount of the group varies across states with its share**, which would bias the slope.

## Disclosures

**Post-hoc additions**, each labeled where it appears:

- the agriculture-excluded pooled slopes;
- the E-Verify trend break;
- the specialty-trade check net of low-exposure industries;
- the per-industry wage long differences;
- the level check.

The bachelor's-degree variant was planned, because of H-1B holders in the imputed flag.

**Pricing assumptions:**

- Off-books workers are priced at the group's average pay.
- ECEC's workers'-compensation residual includes federal unemployment tax.
- The customers' pass-through is assumed.

**Coverage gaps:**

- 1099 misclassification is outside U.
- Agriculture and private households are unpriced.

**Recomputation.** Every per-year figure (enforcement, uncovered levels, edges) is computed one year at a time and then averaged; none is a pooled ratio.

## Reproduce

Run from the repository root. The first step needs `IPUMS_API_KEY` (`set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a`; never print it). Downloads: IPUMS 804 MB; QCEW 20 singlefiles, filtered on arrival; DOL 3.7 GB of zips.

```sh
L=infra/immigration-fiscal/compliance_gap_2026_09_24
uv run --no-project python3 $L/ipums_extract.py submit workers workers_pre   # then: wait, download
OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb python3 $L/acs_prepare.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb python3 $L/acs_cells.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/fetch_qcew.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb python3 $L/qcew_cells.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/fetch_dol.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pyfixest --with duckdb python3 $L/uncovered.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb python3 $L/enforcement.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pyfixest --with duckdb python3 $L/panel_c.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pyfixest --with duckdb python3 $L/everify.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb python3 $L/edges.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb python3 $L/composition.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb python3 $L/winners_losers.py
uv run --no-project python3 $L/report_tables.py > /tmp/tables.md   # every table above
uv run --no-project python3 $L/quote_check.py                        # exit 1 if a quote is not found
```

## Quotes used

| Quote | File (`_cache/papers/`) | Where |
|---|---|---|
| "Nonfarm proprietor income $80 16% 29% 57%" | irs_p1415.txt | Pub 1415 Table 5, p. 20 |
| "Wages, salaries, tips $7 1% 2% 1%" | irs_p1415.txt | Pub 1415 Table 5, p. 20 |
| "2016 is a combined $29 billion, with $28 billion from underreported FICA taxes and $1 billion from" | irs_p1415.txt | Pub 1415 p. 24 |
| "workers are also excluded from the estimates due to lack of compliance data. Therefore, the estimate of the" | irs_p1415.txt | Pub 1415 p. 23 |
| "FICA and FUTA Tax $34 6% $37 5% $40 6%" | irs_p5869.txt | Pub 5869 Table 3 |
| "\| Concluded Compliance Actions \| 16,924 \| 17,300 \| 20,215 \| 20,422 \| 24,746 \|" | whd_all_acts.txt | DOL WHD All Acts, FY 2025 to FY 2021 |
| "\| Back Wages \| $259,294,764 \| $202,676,115 \| $212,325,391 \| $213,161,638 \| $234,362,486 \|" | whd_all_acts.txt | same |
| "The dataset contains all concluded WHD compliance actions since FY 2005." | dol_whd_enforcement_metadata.txt | DOL API dataset 10362 |
| "Findings Start Date and Findings End Date are not equal to Case Open Date and Case Close Date, which are not included in the dataset." | dol_whd_enforcement_metadata.txt | same |
| "In fiscal year 2019, according to WHD data, 64 percent of FLSA cases were initiated in response to complaints and 36 percent were initiated by WHD." | gao_21_13_excerpt.txt | GAO-21-13 (excerpt) |
| "WHD found minimum wage and/or overtime pay violations in 80 percent of FLSA cases concluded in fiscal year 2019." | gao_21_13_excerpt.txt | GAO-21-13 (excerpt) |
| "In FY 2024, OSHA conducted 34,625 inspections comprising 17,455 unprogrammed and 17,170 programmed inspections." | osha_enforcement_summaries.txt | OSHA FY 2024 summary |
| "UI and UCFE programs covered 153.1 million jobs. The estimated 147.3 million workers in these jobs (after adjustment for multiple jobholders) represented 97.4 percent of civilian wage and salary employment." | bls_ewaa_2023.txt | BLS Employment and Wages, Annual Averages 2023 |
| "social security tax on taxable wages is 6.2% each for the" | irs_p15_2024.txt | IRS Pub 15 (2024) |
| "The Medicare tax rate is 1.45% each for the employee" | irs_p15_2024.txt | IRS Pub 15 (2024) |
| "workers compensation insurance and the employer share of Social Security and Medicare." | iceres_2025_misclassification_brief.txt | p. 3 |
| "In an average month of 2017, between 12.4% and 20.5% of the construction industry" | obe_2020_payroll_fraud_methodology.txt | p. 3 |
| "translates into wage theft of 15 percent of earnings." | bernhardt_2009_broken_laws.txt | p. 9 |
| "All respondents 25.9 15.6 31.1" | bernhardt_2009_broken_laws.txt | Table 5.1, p. 46 (all / U.S.-born / foreign-born) |
| "Nor are these abuses limited to unauthorized immigrants or other especially vulnerable workers." | bernhardt_2009_broken_laws.txt | p. 13 |
| "Employing undocumented workers reduces a firm's probability of exiting by 0.8 of a percentage point in construction and professional and business services" | bhq_iza3936.txt | p. 22 |
| "Technically, what equation (3) is describing is the probability of the joint decision by the firm to employ and report the employment of undocumented workers." | bhq_iza3936.txt | text |
| "A one-percentage point increase in the share of undocumented workers in a documented worker's county/industry results in an average wage boost of 0.44 percent." | hqr_solejole_2013.txt | 2013 draft, abstract |
| "the self-employment rate for likely unauthorized men in Arizona rose 8.3 percentage points higher relative to the synthetic control group." | bohn_lofstrom_iza6598.txt | results |
| "Among men, E-Verify mandates appear to reduce hourly earnings by about 8 percent." | orrenius_zavodny_impact_iza2014.txt | results |
| "identify a small and statistically insignificant 0.4 percent decline in the total number of establishments." | ayromloo_nber_w26676.txt | results |
| "The coverage rate rises from zero in 2007 to 12.3 percent in 2015." | ayromloo_nber_w26676.txt | p. 9 |
| "The number of firms falls by 3.4%. Both estimates are significant at the 1% level." | sc_business_dynamics_samyam.txt | introduction |
| "counties with 287(g) agreements experienced a 6 percent decrease in the total number of businesses per 1000 county population" | business_creation_287g_jaae2024.txt | results |
| "A. After December 31, 2007, every employer, after hiring an employee, shall verify the employment eligibility of the employee through the e-verify program" | statute_az_ars_23-214.txt | A.R.S. 23-214 |
| "All employers shall meet verification requirements not later than July 1, 2011." | statute_ms_71-11-3.txt | Miss. Code 71-11-3 |
| "(b) Effective April 1, 2012, every business entity or employer in this state shall enroll in E-Verify" | statute_al_31-13-15.txt | Ala. Code 31-13-15 |
| "2011 Act No. 69, SECTION 9, eff January 1, 2012." | statute_sc_code_t41c008.txt | S.C. Code 41-8-20 |

## Files

- Scripts, in run order: `ipums_extract.py`, `acs_prepare.py`, `acs_cells.py`, `cells.py` (industry partition), `fetch_qcew.py`, `qcew_cells.py`, `fetch_dol.py`, `uncovered.py`, `enforcement.py`, `panel_c.py`, `everify.py`, `edges.py`, `composition.py`, `winners_losers.py`, `report_tables.py`, `quote_check.py`.
- Derived outputs (`derived/`):
  - `uncovered_*.csv`, `low_exposure_cells.csv`;
  - `enforcement_by_cell*.csv`, `whd_gate.csv`;
  - `edges_*.csv`;
  - `panel_c.csv`, `composition_check.csv`;
  - `everify_*.csv`;
  - `winners_losers_rows.csv`;
  - `quote_check.csv`;
  - `gates_qcew.csv`, `qcew_national_sectors.csv`;
  - `fetch_manifest_*.json`.
- Reading notes: `reads/LIT_COMPLIANCE_COSTS.md` and `reads/LIT_FIRMS_EVERIFY.md`.

Model self-report: `claude-opus-5-5[1m]` (Opus 5.5, 1M context), lane worker, 2026-09-25.
