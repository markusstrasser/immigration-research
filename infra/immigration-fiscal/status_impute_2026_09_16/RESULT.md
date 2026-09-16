MODEL SELF-REPORT: Opus 5 (1M context) — claude-opus-5[1m]

# Splitting the Mexico-born ledger cell by imputed legal status

**Verdict:** **Unauthorized immigrants are in the ledger, but the ledger as published cannot see
them, and once their real eligibility rules are applied they are the worse half of the Mexico-born
cell — though not by nearly as much as the framing of the question implies.** The Borjas residual
puts **41.5% of the Mexico-born adults 25–64 in the ledger (3.92M of 9.45M) in the imputed-unauthorized
cell.** In the **raw** ledger the two halves are statistically indistinguishable: imputed-unauthorized
**−7,806 (se 472)** vs imputed-legal **−8,166 (se 378)** against third-plus non-Hispanic whites, a
difference of $360 on standard errors of ~600 — **no separation at all.** The split only opens once
the structurally wrong lines are corrected: zeroing status-ineligible transfers and applying the
informal-channel lane's 44% on-books share moves the imputed-unauthorized to **−9,720 (se 312)**
while the imputed-legal barely move to **−8,234 (se 378)**, a real $1,486 spread. On the extended
balance the corrected figures are **−14,151 (se 392)** vs **−11,725 (se 465)**. The
imputed-unauthorized carry **40.4% of the pooled Mexico-born gap raw, 45.5% corrected** — close to
their 41.5% population share, which is the substantive answer: **status is not what is driving the
Mexico-born gap.** Education and earnings are, and they are low on both sides of the status line.

`[UNVERIFIED]`

Provenance tags: `[DATA]` CPS ASEC 2025 public-use file, sha256 318845a2…, 160-replicate SDR.
`[INFERENCE]` for the corrected arm's eligibility construction and the licensed-occupation list.
`[SOURCE: …]` on every external benchmark.

Files: `status_ledger.py` (driver), `impute_status.py` (the imputation),
`status_imputed_ledger.csv` (every group × metric × arm × allocation with SDR se),
`status_result.txt` (the printed tables), `status_counts.csv`, `status_manifest.json`, `run.log`.

Verification, pasted verbatim from `run.log` (exit code 0):

```
==============================================================================================================
STEP A — reproduction of the published gen-ledger numbers
==============================================================================================================
   Mexican 2nd gen minus 3rd+ NH white, taxes minus selected transfers: -6,066 (se 353)   published -6,066 (se 353)   deviation +0.17
   same, EXTENDED balance:                                             -8,286 (se 443)   published -8,286 (se 443)   deviation -0.23
   [reproduction check] PASS (both within $50)
```

The `equal_adults_18plus` allocation independently reproduces the gen-ledger lane's second pair:
−7,625 (se 462) baseline and −10,633 (se 587) extended, matching
`gen_ledger_extension_2026_09_16/RESULT.md` exactly. **Verification result: PASS.**

---

## 1. The imputation rule list, quoted from the paper

George J. Borjas, "The Labor Supply of Undocumented Immigrants," NBER Working Paper 22102 (March
2016), published as *Labour Economics* 46 (2017) 1–13, pp. 10–11
[SOURCE: https://www.nber.org/system/files/working_papers/w22102/w22102.pdf]:

> "The algorithm I use to create a comparable undocumented status identifier in all the relevant
> ASEC files is as follows. A foreign-born person will be classified as a legal immigrant if:
> a. that person arrived before 1980; b. that person is a citizen; c. that person receives Social
> Security benefits, SSI, Medicaid, Medicare, or Military Insurance; d. that person is a veteran, is
> currently in the Armed Forces; e. that person works in the government sector; f. that person
> resides in public housing or receives rental subsidies, or that person is a spouse of someone who
> resides in public housing or receives rental subsidies; g. that person was born in Cuba (as
> practically all Cuban immigrants are granted refugee status); h. that person's occupation requires
> some form of licensing (such as physicians, registered nurses, air traffic controllers, and
> lawyers; i. that person's spouse is a legal immigrant or citizen. The residual group of all other
> foreign-born persons is then classified as undocumented."

Two corrections to the brief as written. **The paper's refugee rule is Cuba alone** — Vietnam, Laos,
Cambodia and Ukraine are the Pew list, not Borjas's, and they enter here only as the
`wide_refugee_list` sensitivity. And the paper prints **no occupation list**, only four examples, so
`LICENSED_OCC` in `impute_status.py` is this lane's 33-code list of 2018-vintage Census occupation
codes, flagged `[INFERENCE]`, with `no_occupation_rule` as the sensitivity. Rule (i) is recursive and
is iterated to a fixpoint. Country codes were taken from this repo's own
`secgen_selectivity_2026_09_16/country_crosswalk.csv` (Cuba = 327, not the 337 I first assumed).

Rule hit rates among the 11,283 foreign-born noncitizens (rules overlap):

| rule | n | weighted |
|---|---|---|
| a arrived pre-1980 | 347 | 0.79M |
| c benefits (SS/SSI/Medicaid/Medicare/military ins.) | 3,186 | 7.57M |
| d veteran or armed forces | 45 | 0.11M |
| e government sector | 388 | 0.83M |
| f subsidised housing | 459 | 1.13M |
| g born in Cuba | 366 | 0.91M |
| h licensed occupation | 137 | 0.33M |
| i spouse legal or citizen (marginal) | 1,168 | 2.65M |
| **→ imputed UNAUTHORIZED** | **5,973** | **14.90M** |
| → imputed legal noncitizen | 5,310 | 12.46M |

## 2. Counts against the published benchmarks

CPS ASEC 2025 (March 2025, income year 2024), person weights, **no undercount adjustment applied**:

| | all ages | 18+ | 25–64 |
|---|---|---|---|
| imputed unauthorized, national | 14.90M | 13.26M | 11.31M |
| imputed unauthorized, Mexico-born | 4.57M | 4.33M | 3.92M |

Sensitivities on the national all-ages total: dropping rule (h) 15.13M; the wide refugee list 14.32M;
**dropping the Medicaid clause 18.58M** — the Medicaid rule is by far the most load-bearing, which is
expected after ACA expansion and emergency Medicaid made receipt a much weaker legal-status signal
than it was in Borjas's 2012–13 sample.

Benchmarks, with one correction to the brief:

| source | year | total | Mexico-born |
|---|---|---|---|
| Pew Research Center, report of 21 Aug 2025 | mid-2023 | **14.0M** | **4.3M (30%)** |
| Pew, same report, **revised** | 2022 | **11.8M** (revised up from the 11.0M originally published) | — |
| DHS OHSS | 1 Jan 2022 | 11.0M | — |

[SOURCE: https://www.pewresearch.org/race-and-ethnicity/2025/08/21/u-s-unauthorized-immigrant-population-reached-a-record-14-million-in-2023/ and its methodology appendix; the 11.0M→11.8M revision for 2022 is stated in the report's own methodology, driven by the Census Bureau's Vintage 2024 net-international-migration revision]
[SOURCE: DHS OHSS, *Estimates of the Unauthorized Immigrant Population Residing in the United States: January 2018–January 2022*, 11.0M on 1 Jan 2022]

**The undercount adjustment is smaller than the brief assumed.** Pew's published figure is
**"coverage adjustments increase the estimate of the unauthorized immigrant population by 8% to 13%
for 2000-09 and by 5% to 7% for 2010-16"** [SOURCE: https://www.pewresearch.org/hispanic/2018/11/27/unauthorized-immigration-estimate-methodology/].
The 10–15% figure in the brief matches Pew's *1995–2000 CPS* era, not the current one. The 2025
report describes the adjustment only qualitatively ("we adjust our estimates to account for
immigrants… who are missed in the national surveys. We use Census Bureau studies of undercount").

**The unadjusted residual here (14.90M in March 2025) sits above Pew's undercount-adjusted 14.0M for
mid-2023, and the Mexico-born 4.57M above Pew's 4.3M.** Two years of growth plus the
Borjas method's known upward bias — he states plainly that his reconstruction does "not carry out
any kind of probabilistic sampling to account for the 'excess' number of undocumented immigrants
that this residual method yields" — make the agreement better than it looks, but the level should
not be read as validated.

## 3. The ledger, both allocations, adults 25–64, per adult per year

`equal_all_members`, person weights, differences from third-plus non-Hispanic white (SDR se):

| row | 3rd+ NH white | Mexico-born pooled | Mex. imputed **unauth** | Mex. imputed **legal** |
|---|---|---|---|---|
| **RAW ARM** | | | | |
| Modeled taxes | 14,383 | 4,874 · −9,509 (325) | 4,472 · −9,912 (467) | 5,160 · −9,224 (355) |
| Cash transfers | 2,453 | 860 · −1,593 (84) | 240 · −2,213 (67) | 1,299 · −1,154 (115) |
| Non-cash transfers | 145 | 246 · +101 (14) | 253 · +107 (29) | 241 · +96 (13) |
| = Taxes − transfers | 11,785 | 3,768 · **−8,016 (338)** | 3,979 · **−7,806 (472)** | 3,619 · **−8,166 (378)** |
| = Extended balance | 15,984 | 4,462 · **−11,522 (402)** | 4,611 · **−11,373 (563)** | 4,356 · **−11,628 (465)** |
| **CORRECTED ARM** | | | | |
| Modeled taxes | 14,377 | 3,985 · −10,392 (295) | 2,436 · −11,941 (302) | 5,083 · −9,295 (354) |
| Cash transfers | 2,453 | 848 · −1,605 (85) | 212 · −2,241 (66) | 1,298 · −1,155 (115) |
| Non-cash transfers | 145 | 209 · +63 (9) | 165 · +20 (11) | 239 · +94 (12) |
| = Taxes − transfers | 11,779 | 2,929 · **−8,850 (310)** | 2,059 · **−9,720 (312)** | 3,545 · **−8,234 (378)** |
| = Extended balance | 15,977 | 3,246 · **−12,731 (372)** | 1,827 · **−14,151 (392)** | 4,252 · **−11,725 (465)** |
| adults 25–64 (n / weighted) | 36,287 / 87.65M | 4,318 / 9.45M | 1,696 / 3.92M | 2,622 / 5.53M |

`equal_adults_18plus`, same construction, headline rows only:

| row | 3rd+ NH white | Mexico-born pooled | Mex. imputed unauth | Mex. imputed legal |
|---|---|---|---|---|
| RAW taxes − transfers | 14,409 | 4,023 · −10,386 (384) | 4,140 · −10,269 (503) | 3,939 · −10,470 (437) |
| RAW extended balance | 18,099 | 3,154 · −14,945 (475) | 3,319 · −14,781 (632) | 3,038 · −15,061 (573) |
| CORR. taxes − transfers | 14,403 | 3,161 · −11,242 (356) | 2,188 · −12,215 (347) | 3,850 · −10,553 (437) |
| CORR. extended balance | 18,092 | 1,835 · −16,257 (444) | 314 · −17,778 (468) | 2,912 · −15,180 (573) |

Share of the pooled Mexico-born gap carried by the imputed-unauthorized (their share of the cell's
adults is 41.5%): raw **40.4%** on the balance and **40.9%** on the extended balance; corrected
**45.5%** and **46.1%**. Every full metric, group, arm and allocation is in
`status_imputed_ledger.csv`.

## 4. Which ledger lines are structurally wrong for the unauthorized, and the corrected arm

| line | why the raw ledger is wrong | what the corrected arm does |
|---|---|---|
| Federal income tax (`FEDTAX_AC`) | Census's tax model assumes a filed return; 56% of unauthorized workers have no payroll record at all | scaled by the 44% on-books share |
| EITC (`EIT_CRED`) | requires a work-authorised SSN for filer and spouse; ITIN filers are categorically ineligible | **zeroed** for every imputed-unauthorized person |
| ACTC (`ACTC_CRD`) | available on an ITIN return when the child has an SSN, so eligibility survives — but a non-filer claims nothing | scaled by the same 44%, not zeroed |
| Payroll and state income tax | same filing/withholding assumption | scaled by 44% |
| Employer payroll tax | off-books wages generate no employer contribution either | scaled by 44% |
| SSI, Social Security, veterans' benefits | ineligible — but **already a no-op**, because rules (c) and (d) route any recipient to LEGAL by construction | zeroed anyway, for explicitness |
| TANF (`PAW_VAL`), unemployment insurance (`UC_VAL`) | both require qualified-alien status or work authorisation for the adult; these are the **live** cash corrections | zeroed for the imputed-unauthorized adult |
| SNAP (`SPM_SNAPSUB`), LIHEAP (`SPM_ENGVAL`) | the adult is ineligible, the citizen children are not; the CPS field is an SPM-unit total | prorated to the non-unauthorized share of unit members |
| WIC, school lunch, broadband subsidy | no immigration-status test; children qualify regardless | left whole |
| Sales/excise and property tax | paid on consumption and housing regardless of status | left whole |
| Medicaid | ineligible beyond emergency Medicaid — **but Medicaid is not in this ledger's balance at all**; it lives in the separate MEPS health module, which was not run here | not applicable; flagged as the single largest omitted correction |

The 44% on-books share is 3.1M of 7.0M unauthorized workers on payroll in 2010
[SOURCE: SSA OCACT Actuarial Note 151, Goss, Wade, Skirvin, Morris, Bye & Huston, April 2013,
https://www.ssa.gov/oact/NOTES/pdf_notes/note151.pdf], as established by
`infra/immigration-fiscal/informal_channel_2026_09_16/RESULT.md`.

## 5. Caveats

**The `all_imputed_unauthorized` group is not usable as a fiscal cell, and this is the probe's most
important negative finding.** The Borjas reconstruction assigns **2.03M India-born people to the
unauthorized cell — 95.8% of them hold a bachelor's degree or more and they average $101,165 in
earnings** (China: 0.58M, 87.7% BA+, $114,710). Pew's 2023 estimate for India is roughly 725,000.
These are H-1B, L-1 and F-1 holders, whom Pew explicitly assigns a "legal temporary migration
status" and Borjas's rules cannot. That is why `all_imputed_unauthorized` shows modeled taxes of
$9,895 and a gap of only −2,304 in the raw arm: it is a mixture of the actual unauthorized with the
high-skill temporary-visa population. **The Mexico-born split is far more trustworthy** — Mexico has
almost no temporary-visa population of that shape, and the Mexico-born imputed-unauthorized cell is
9.7% BA+ with mean earnings of $34,940, which is what the literature describes.

**Imputation error is one-directional and known.** Borjas does no probabilistic reweighting to DHS
counts, so the residual over-assigns. Rules (c) and (e) also make the imputation *mechanically
correlated with the ledger's own outcome variables*: anyone receiving Social Security, SSI, Medicare
or Medicaid, or working in government, is defined into the legal cell. That builds in part of the
transfer gap between the two halves and is a reason to read the raw arm's near-zero separation as
the more honest of the two numbers, not the corrected arm's spread.

**CPS coverage of recent arrivals.** The CPS measured a net increase of 3.94M immigrants from
January 2022 to October 2024 against a CBO estimate of 8.65M over the same window
[SOURCE: Alexander Bick, "The Recent Surge in Immigration and Its Impact on Unemployment," Federal
Reserve Bank of St. Louis, 3 January 2025,
https://www.stlouisfed.org/on-the-economy/2025/jan/recent-surge-immigration-impact-on-unemployment].
Recent arrivals are the most likely to be unauthorized and the most likely to be missed, so both the
counts and the per-adult means here are biased toward the settled, better-covered population. I did
not locate a Philadelphia Fed 2025 brief on this; the St. Louis Fed piece is the substitute and is
directly on point.

**The corrected arm is an accounting scenario, not a measurement.** The 44% share is a 2010 national
figure applied uniformly; it is not measured for Mexico-born adults in 2024, and IRS publishes no
tax-gap breakdown by nativity or status. Neither arm is actual tax collection.
