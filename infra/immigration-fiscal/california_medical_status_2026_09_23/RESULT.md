**Verdict:** The status imputation's Medicaid clause hides California's unauthorized Medi-Cal
enrollees. Correcting it in California adds 0.47–0.59M people to the Mexican-origin union's
4.567M unauthorized.
Under the paper rules every Medicaid reporter counts as legal, so both surveys show zero
imputed-unauthorized Medi-Cal enrollees. DHCS counts 1.53M enrolled in its status-blind full-scope
programs (2024 monthly average). Without the clause, CPS ASEC 2025 finds 1.11M such Californians
(se 0.08), 72% of the DHCS count. ACS 2024 finds 1.29M (se 0.02), 84%. Each survey's reporting
rate for all Medi-Cal enrollees (63% and 74%) predicts 0.97M and 1.13M. On the CPS the clause
misclassifies 0.75–1.11M Californians, 0.47–0.59M of them Mexico-born. Nationally the figure is
1.1–1.5M at the state-ages where coverage ignored status in 2024. The ceiling is 3.68M, if no
Medicaid report carried status information. California's state and local governments spent
$183.8bn on public welfare in FY2023-24 (Census; first among states; 16.8% of the US total;
$4,662 per resident). That is the data definition matching "more than $180 billion … for the poor",
and $104.5bn of it arrived as federal grants.

Tags: `[DATA]` local microdata and DHCS/Census files; `[CALCULATION]` this lane's scripts, every
figure traceable to a `derived/` table; `[SOURCE: …]` external documents, fetched to `_cache/` and
hashed in `derived/sources.json`; `[INFERENCE]` where a step goes beyond the data. The instrument
is an LLM working on a politically charged question (`notes/llm-bias-caveat.md`). The counts
below are mechanical, and the interpretive steps are tagged.

## 1. Gate

`cps_ca_status.py` imports `status_impute_2026_09_16/impute_status.py` unmodified and reproduces
every published count to 1e-6 M. With the paper rules it gets 14.8964M national, 4.5671M
Mexico-born and 4.5671M union, the target of `dataset_integrity_2026_09_23/cps_status_keys.py`.
Mexico-born 25–64 comes to 3.9171M. With `no_medicaid_rule` it gets 18.5813M national, 5.7096M
Mexico-born and parent_status's 4.7781M Mexico-born 25–64 [CALCULATION: `derived/cps_gate.csv`].
`acs_ca_status.py` imports `unauthorized_population_size_2026_09_19/acs_residual.py` unmodified. It
reproduces that lane's ACS residual, 12,973,901 national and 3,963,961 Mexico-born, exactly
[CALCULATION: `derived/acs_gate.csv`]. **PASS.** The union's unauthorized are exactly the
Mexico-born unauthorized, because G2 and G3+ are US-born.

## 2. Counts under each rule set (CPS ASEC 2025, millions, SDR se)

| Rule set | California | Rest of US | US | Union (= Mexico-born), US | Union, California |
|---|---:|---:|---:|---:|---:|
| Paper rules | 2.220 (0.117) | 12.676 (0.292) | 14.896 (0.316) | 4.567 (0.165) | 0.809 (0.070) |
| Medicaid ignored in California only | 3.328 (0.148) | 12.676 (0.292) | 16.005 (0.331) | 5.159 (0.171) | 1.401 (0.085) |
| Medicaid ignored at all listed state-ages (§5) | 3.328 (0.148) | 13.050 (0.296) | 16.378 (0.335) | 5.227 (0.174) | 1.401 (0.085) |
| `no_medicaid_rule` (Medicaid ignored everywhere) | 3.328 (0.148) | 15.253 (0.330) | 18.581 (0.365) | 5.710 (0.184) | 1.401 (0.085) |

[CALCULATION: `derived/cps_counts_by_rules.csv`]. The two state-aware variants run the paper rules
on a copy of the frame with MCAID set to "No" at the listed state-ages; the imported code is
unchanged. In California they coincide with `no_medicaid_rule`, because Medi-Cal covered every age
regardless of status in 2024.

## 3. Medi-Cal coverage among California's `no_medicaid_rule` unauthorized, by age

**CPS ASEC 2025.** MCAID is "Medicaid, PCHIP or other means-tested coverage last year", covering
calendar 2024, as the status lane reads it [SOURCE: ASEC 2025 data dictionary, `ddl25.txt`
lines 5288–5294]. The unlisted-states column is the same population in states that ran no
status-blind program in 2024 (§5).

| Age | Unauthorized, no clause (M) | With Medi-Cal in 2024 (M) | Share | Same share, unlisted states | n |
|---|---:|---:|---:|---:|---:|
| 0–18 | 0.363 (0.041) | 0.209 (0.030) | 57% (6) | 28% (2) | 143 |
| 19–25 | 0.352 (0.041) | 0.092 (0.019) | 26% (5) | 11% (2) | 118 |
| 26–49 | 1.846 (0.099) | 0.498 (0.044) | 27% (2) | 8.5% (0.8) | 689 |
| 50–64 | 0.731 (0.057) | 0.310 (0.035) | 42% (4) | 8.4% (1.1) | 282 |
| 65+ | 0.036 (0.011) | 0 | 0 | 0 | 15 |
| **All** | **3.328 (0.148)** | **1.108 (0.078)** | **33% (2)** | **12% (0.8)** | 1,247 |

[CALCULATION: `derived/cps_coverage_by_age.csv`]. Mexico-born Californians number 1.401M, of whom
0.592M (se 0.049), or 42%, report Medi-Cal. By age that is 75% at 0–18, 34% at 19–25, 42% at 26–49
and 38% at 50–64. Current coverage (NOW_MCAID, February–April 2025) gives 1.102M, and
Medicaid-only (CAID) gives a 33.0% share, so the choice of item barely matters. Of these Medicaid
reports, 17% are donor-imputed (I_MCAID 1 or 3). Survey-wide, about 23% of persons have a
donor-imputed coverage item (`cps_imputation_keys_2026_09_23` step 2). In unlisted states the rate is 38%, so there the clause
often rests on a value the respondent never gave.

**ACS 2024 1-year PUMS.** HINS4 is Medicaid or other means-tested coverage at interview, 2024. The
table covers all persons, group quarters included.

| Age | Unauthorized, no clause | With Medicaid at interview | Share |
|---|---:|---:|---:|
| 0–18 | 381,518 (11,192) | 229,921 (9,529) | 60% (1.3) |
| 19–25 | 321,395 (8,064) | 103,960 (4,631) | 32% (1.1) |
| 26–49 | 1,892,233 (21,576) | 641,699 (13,370) | 34% (0.6) |
| 50–64 | 736,427 (10,255) | 309,759 (8,196) | 42% (0.9) |
| 65+ | 52,511 (2,748) | 0 | 0 |
| **All** | **3,384,084 (33,809)** | **1,285,339 (21,606)** | **38% (0.5)** |

[CALCULATION: `derived/acs_ca_counts_by_age.csv`]. The paper rules give 2,045,143 (se 23,950).
The clause moves 1,338,941 (se 21,765): 1,285,339 on their own report and 53,602 through the
spouse link. Among the Mexico-born, the count rises from 860,815 to 1,637,721, and 740,607 of them
(45%) have Medicaid. The household population alone gives 2,005,142 under the paper rules,
3,326,374 without the clause and 1,267,630 with Medicaid.

Three rules cannot be applied as written on the ACS. The mapping and its reasons come from
`acs_residual.py`:
- **(f) Public housing or rent subsidy.** The PUMS has no such item, so the rule is dropped. This
  raises the ACS residual.
- **(i) Spouse legal.** The ACS has no spouse pointer. Only the reference person and a single
  spouse record are linked, so spouses in subfamilies go unlinked.
- **(c) Benefits.** Coverage is read at the interview (HINS3/HINS4/HINS5), where the CPS asks about
  any time last year. Social Security and SSI are income in the past 12 months.

**No rule set finds unauthorized seniors on Medi-Cal.** Every noncitizen aged 65+ who reports
Medicaid also carries Medicare, in both surveys. On the CPS that is 0.119M Californians (n = 51),
all with MCARE = 1; Census logically imputed 74% of those Medicare values and hot-decked 6%
[CALCULATION: `derived/cps_65plus_medicare_edit.csv`]. On the ACS it is 231,898 (n = 2,330), all
with HINS3 [CALCULATION: `derived/acs_65plus_medicare.csv`]. So rule (c)'s Medicare clause, which
`no_medicaid_rule` keeps, calls them legal. DHCS's 50+ count includes unauthorized-status seniors
that neither survey can separate.

## 4. Benchmark: DHCS's published enrollment

DHCS publishes monthly counts, from its eligibility system (MEDS), of full-scope enrollees in each
status-blind expansion, on the CalHHS open-data portal
[SOURCE: https://data.chhs.ca.gov/dataset/medi-cal-adult-expansion and
…/sb-75-full-scope-medi-cal-for-all-children-enrollment, June 2026 files, fetched 2026-09-23;
`fetch_sources.py`]. The four programs are:
- SB 75, children under 19, since May 2016;
- the Young Adult Expansion, 19–25, since January 2020;
- the Older Adult Expansion, 50+, since May 2022;
- the Adult Expansion, 26–49, since January 2024.

DHCS's dataset notes say the adult counts are not UIS-only: "Lawfully present individuals 26-49
years of age are included in this count", with the same sentence for 50+ and for 21–25. They are
therefore an upper bound on UIS enrollment in these programs.
The Medi-Cal Local Assistance Estimates (May 2025, November 2025) report UIS costs but no UIS
caseload total [SOURCE: `_cache/M25-…txt`, `N25-…txt`; searched].

| Age | DHCS, 2024 monthly average | CPS, any time 2024 | CPS capture | ACS, at interview | ACS capture |
|---|---:|---:|---:|---:|---:|
| 0–18 | 197,375 | 0.209M | 106% (15) | 0.230M | 116% (5) |
| 19–25 | 140,187 | 0.092M | 65% (13) | 0.104M | 74% (3) |
| 26–49 | 802,798 | 0.498M | 62% (5) | 0.642M | 80% (2) |
| 50+ | 392,522 | 0.310M | 79% (9) | 0.310M | 79% (2) |
| **All** | **1,532,882** | **1.108M** | **72% (5)** | **1.285M** | **84% (1)** |
| Paper rules, every age | — | 0 | 0% | 0 | 0% |

[DATA: `derived/dhcs_uis_windows.csv`; CALCULATION: `derived/benchmark_survey_vs_dhcs.csv`].
Other windows give the same picture:
- The CPS 1.108M is 68% of the December 2024 count (1,624,296).
- CPS current coverage (1.102M) is 67% (se 5) of the February–April 2025 average (1,655,112).

DHCS enrollment peaked at 1,670,306 in June 2025 and fell to 1,275,056 by June 2026 after the adult
enrollment freeze.

The paper rules move 1.108M Californians into the legal column on the CPS, all on their own
Medi-Cal report and none through the spouse link. On the ACS they move 1.339M
[CALCULATION: `derived/cps_moved_decomposition.csv`, `acs_ca_counts_by_age.csv`].

**The surveys' reporting rate is the yardstick.** The CPS records 9.47M Californians with Medicaid
at some point in 2024, against DHCS's 14.98M average certified eligibles: 63%. The rate is 66% for
children, 61% at 19–44, 72% at 45–64 and 49% at 65+. The ACS records 11.05M, or 74%
[CALCULATION: `derived/benchmark_all_medi_cal_reporting.csv`; DATA: DHCS certified eligibles by
age, CalHHS]. If expansion enrollees reported coverage like other enrollees, the CPS would show
0.97M of them and the ACS 1.13M. The observed counts exceed that by 0.14M and 0.15M.

The excess sits in children (CPS 0.21M against 0.12M expected) and at 50–64, while at 19–49 the
CPS count and the expected count are about 1% apart (0.589M against 0.596M). That pattern fits lawfully present children and
older adults with regular Medi-Cal sitting in the no-clause pool [INFERENCE].

## 5. How many the Medicaid clause misclassifies

**California.** The CPS gives three readings of the same quantity, and the ACS gives two
[CALCULATION: `derived/ca_misclassification_band.csv`]:

| Reading | All foreign-born | Mexico-born (union) |
|---|---:|---:|
| Lower: California's Medi-Cal reports above unlisted states' rates for the same age band (CPS) | 0.749M (0.071) | 0.467M (0.048) |
| Calibrated: DHCS 2024 count × CPS reporting rate [INFERENCE] | 0.968M (0.026) | 0.517M (0.014) |
| Upper: everyone the clause moves (CPS) | 1.108M (0.078) | 0.592M (0.049) |
| Calibrated, ACS [INFERENCE] | 1.131M (0.006) | 0.656M (0.003) |
| Upper, ACS | 1.339M (0.022) | 0.777M (0.015) |

The lower reading is conservative. The unlisted-state rate it subtracts already contains
emergency and perinatal coverage, imputed values and lawful recipients.

**States whose programs ignored status in 2024**, the MCAID reference year. These are the states
listed in `STATUS_BLIND_2024`:
- **California**, every age: DHCS dataset notes, dates as in §4.
- **Oregon**, every age: "As of July 1, 2023, people of all ages who meet income and other criteria
  qualify for full OHP benefits … no matter their immigration status" [SOURCE:
  https://www.oregon.gov/oha/hsd/ohp/pages/healthier-oregon.aspx].
- **New York**, 65+: "expansion of health insurance coverage for undocumented non-citizens who are
  at age 65 or older. This change is effective January 1, 2024" [SOURCE: NY DOH 23 OHIP/INF-2,
  p. 1]. New York's children are listed below.
- **District of Columbia**, 21+ through the "longstanding locally funded Healthcare Alliance
  program", plus children.
- **Illinois**, 42–64 through the Health Benefits for Immigrant Adults program ("2022 … ended HBIA
  coverage on July 2025") and 65+ through the Health Benefits for Immigrant Seniors program
  ("December 2020 but new enrollment has been paused since 2023"), plus children.
  [SOURCE for the District of Columbia and Illinois: KFF, "State Health Coverage for Immigrants and
  Implications for Health Coverage and Care", 19 May 2026.]
- **Children, 0–18**, in California, Connecticut, Illinois, Maine, Massachusetts, New Jersey,
  New York, Oregon, Rhode Island, Utah, Vermont, Washington and the District of Columbia. KFF's
  March 2024 list: "12 states and Washington D.C. provide fully state-funded coverage for
  income-eligible children regardless of immigration status" [SOURCE: KFF news release,
  1 May 2024].

Some states are left out:
- Colorado: adult coverage runs through Marketplace plans, and child coverage started in 2025.
- Minnesota: coverage ran from January 2025 to January 2026.
- Washington adults: the Apple Health Expansion started July 2024 with an enrollment cap.

The rule set treats children as 0–18 in every state. Some state programs use other age limits,
and Rhode Island's started in October 2024 [UNVERIFIED for exact age limits outside California,
Oregon and New York].

**National (CPS).**

| Where | Moved by the clause | Of which at a listed state-age | Moved with a donor-imputed Medicaid value |
|---|---:|---:|---:|
| California | 1.108M (0.078) | 1.108M | 0.191M |
| Other listed states | 1.290M (0.098) | 0.373M (0.044) | 0.318M |
| Unlisted states | 1.287M (0.092) | — | 0.484M (0.065) |
| **US** | **3.685M (0.161)** | **1.482M (0.089)** | **0.992M (0.086)** |

[CALCULATION: `derived/cps_counts_by_rules.csv`, `cps_moved_decomposition.csv`,
`cps_moved_by_state.csv`]. The misclassification built into state policy is 1.1–1.5M:
California's 0.75–1.11M plus 0.37M elsewhere at program ages.

The other 2.2M the clause moves are a mixture. Some are lawful immigrants on regular Medicaid. The
rest are unauthorized people whose Medicaid report comes from emergency or perinatal (CHIP
unborn-child) coverage, misreporting, or a hot-deck value; 27% of the national total rests on a
donor-imputed value. The data cannot split that mixture.

New York stands out. The clause moves 0.587M there, a 44% Medicaid share in its pool. New York
funds coverage for PRUCOL immigrants, a court-ordered category that includes groups published
residual estimates count as unauthorized. The listed-state count therefore probably understates
New York [INFERENCE].

**The union's 4.567M.** California alone adds 0.47–0.59M, to 5.03–5.16M (+10% to +13%). Adding the
other listed state-ages (+0.068M, se 0.016) gives 5.10–5.23M. The ceiling, with Medicaid ignored
everywhere, is 5.71M (+1.142M, of which 0.274M rests on imputed values). The status lane feeds the
audit's on-books rows, so this lane reports the count only.

A separate correction runs the other way. The CPS carries more Mexico-born noncitizens than the ACS
outside California and Texas (`dataset_integrity_2026_09_23/cps.md` row 3), and
`mexborn_count_2026_09_23` puts the 4.567M nearer 4.07M. The two corrections are independent and
are not combined here.

## 6. California's public spending (Census finance files)

The source is the Census Annual Survey of State and Local Government Finances, public-use
state-by-level files. The 2024 survey covers fiscal years ending July 2023 to June 2024, so for
California it is FY 2023-24. Figures are direct expenditure: current operations plus construction.
Per-resident figures use ACS 2024 population (California 39.43M; US 340.11M).
[CALCULATION: `finance.py` → `derived/census_finance_ca.csv`, `census_finance_2024_states.csv`]

| Function, 2024 survey | California | State / local | US | California share | Rank | Per resident, CA / US |
|---|---:|---:|---:|---:|---:|---:|
| Public welfare | **$183.8bn** | $156.7bn / $27.1bn | $1,094.2bn | 16.8% | 1 | $4,662 / $3,217 (rank 6) |
| Health | $44.7bn | $3.8bn / $40.9bn | $159.1bn | 28.1% | 1 | $1,133 / $468 (rank 1) |
| Hospitals | $49.3bn | $25.2bn / $24.1bn | $312.3bn | 15.8% | 1 | $1,250 / $918 (rank 11) |
| All three | $277.8bn | | $1,565.7bn | 17.7% | | |
| Federal aid received for public welfare (B79) | $104.5bn | | $698.7bn | 15.0% | 1 | |

Public welfare grew over four surveys: $151.4bn in 2021, $152.4bn in 2022, $169.2bn in 2023 and
$183.8bn in 2024. The 2022–2024 public-use releases, reissued July 2026, merge vendor payments and
cash assistance into code E79, so the split the brief asks for exists only through 2021. That
year it was:
- vendor payments for medical care (Medi-Cal) $119.4bn (79%);
- cash assistance $8.1bn;
- other vendor payments $0.5bn;
- welfare institutions $0.4bn;
- other public welfare $22.9bn.

Census public welfare is the definition that matches "more than $180 billion … to food, health
care, and other programs for the poor". Medi-Cal alone is close in size: "DHCS estimates Medi-Cal
spending to be $179 billion total funds ($37.4 billion General Fund) in Fiscal Year (FY) 2024-25
and $194.5 billion total funds ($44.6 billion General Fund) in FY 2025-26" [SOURCE: DHCS May 2025
Medi-Cal Local Assistance Estimate, Management Summary]. The sister lane
`california_program_costs_2026_09_23` traces which figure the article used.

The $183.8bn is total funds. Federal public-welfare grants to California were $104.5bn in the same
survey year, 57% of the total. Food is largely outside it: Census codes federal aid for "food stamp
administration" to public welfare, so SNAP benefits themselves do not appear as state spending
[SOURCE: Census 2006 Classification Manual, code B79; INFERENCE for the benefits].
**[FRAMING-SENSITIVE]** "California devotes" fits all funds that pass through its budget; "the
California taxpayer devotes" fits roughly 43% of it.

## 7. Disconfirmation and limits

- **The no-clause pool is not all unauthorized.** Children and 50–64-year-olds with Medi-Cal
  exceed what DHCS's expansion counts allow (§4). The Borjas residual also admits temporary-visa
  holders (status lane §5). The upper readings therefore overstate misclassification, and the
  lower reading bounds it from below.
- **UIS is not the same as unauthorized.** DHCS's UIS includes pending and some lawfully present
  statuses. Published residual estimates (Pew, DHS, CMS) also count many of these people
  (`research/immigration-unauthorized-population-size-2026-09-19.md` §1), so the two concepts are
  close but not identical.
- **Reporting.** Both surveys under-report Medi-Cal: the CPS at 63% and the ACS at 74% of DHCS's
  average. The calibrated reading assumes expansion enrollees report like everyone else, and that
  cannot be tested here. Seventeen percent of the California Medicaid reports in question are
  hot-deck values.
- **Timing.** DHCS counts are monthly stocks. CPS MCAID is any coverage during 2024, which should
  run above a monthly average, so the capture shares are, if anything, flattering.
- **Seniors.** The Medicare edit (§3) hides unauthorized-status seniors under every rule set. That
  adds an unmeasured amount to the misclassification.
- **The CPS residual itself.** The CPS has sparse coverage of 2022–2025 arrivals and the
  Mexico-born excess over the ACS noted in §5. Both change the 4.567M independently of the Medicaid
  clause.

## Files and reproduction

Scripts:
- `fetch_sources.py`: DHCS/CalHHS tables, DHCS estimates via the Internet Archive (DHCS's site
  returns an Incapsula 403 to curl), KFF, Oregon, New York and the Census manual. It writes
  `derived/sources.json` with SHA-256 hashes.
- `dhcs_uis.py`: DHCS monthly and window totals.
- `cps_ca_status.py`: CPS gate, counts, coverage, moved counts, state-aware rules, the
  excess-over-unlisted table and the Medicare edit.
- `acs_ca_status.py`: ACS gate and California tables.
- `finance.py`: Census finance.
- `benchmark.py`: survey against DHCS, reporting rates and the misclassification band.

Inputs, read in place:
- CPS: `gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip` (sha256 318845a2…).
- ACS: `unauthorized_population_size_2026_09_19/_cache/acs2024_person_subset.parquet`, built by
  that lane's `extract_pums.py`.
- Census, 2024: `detention_reconciliation_2026_09_20/_cache/census_2024_units.zip` (0967c4d3…).
- Census, 2021–2023: `local_spending_composition_2026_09_18/_cache/indunit_2021.zip` to
  `indunit_2023.zip`.

```sh
# from the repository root
L=infra/immigration-fiscal/california_medical_status_2026_09_23
for s in fetch_sources dhcs_uis cps_ca_status acs_ca_status finance benchmark; do
  OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3 $L/$s.py || break
done
```

Nothing was committed, and no file outside this directory was edited.

Model self-report: claude-opus-5-5[1m]. Lane `ca-medical-status`, 2026-09-23. Parent rerun: 22/22
`derived/` files byte-identical; DHCS, KFF, Oregon and New York quotes found in `_cache/`.
