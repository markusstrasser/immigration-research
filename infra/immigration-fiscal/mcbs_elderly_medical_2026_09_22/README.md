# MCBS 2023 Cost Supplement PUF — public medical spending at 65+, Hispanic vs non-Hispanic white

One bounded check on the fiscal ledger's **public medical transport**, which assigns MEPS
public-payer costs by age and US birth with **no ethnicity dimension**. The ledger's 65+ cells
for the Mexican-origin union rest on few observations, and the re-aged balance moves −$80bn
through public medical. This lane asks whether an ethnicity adjustment is indicated at 65+,
using a second, independent, Medicare-specific survey.

**Hispanic is not Mexican-origin.** `CSP_RACE=3` covers "persons of Mexican, Puerto Rican,
Cuban, Central and South American, or Spanish origin", of any race
[DATA: `_cache/methodology/2023MCBSSummaryofChangesCSPUF.pdf`, footnote 4]. The file carries
**no country of birth, no nativity and no generation**
[DATA: `fiscal_access_2026_09_20/derived/mcbs_validation.json`, `origin_field_review`].

Results: [RESULT.md](RESULT.md).

## Reproduce

From the repository root:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/mcbs_elderly_medical_2026_09_22/mcbs_elderly.py
uv run --no-project python3 -m pytest infra/immigration-fiscal/mcbs_elderly_medical_2026_09_22/ -q
```

No download. The script reads the CSV member straight out of the pinned zip acquired by
`fiscal_access_2026_09_20` on 2026-09-20 and verifies both hashes before parsing. Only
`numpy` and `pandas` are needed, so the main checkout's `.venv` suffices; in a worktree drop
`--no-project`.

## Inputs

| File | Role | SHA256 |
|---|---|---|
| `../fiscal_access_2026_09_20/_cache/CSPUF2023_Data.zip` | data archive | `56937f1a623b77a85d5b401c1fdc00791098772c240073f70cbbbdff9db86d41` |
| member `cspuf2023.csv` | 6,920 × 134 microdata | `3407a9a76e8ddb71d9b8e840c4c14c94ddd25648c2cc60bf7eeb1d537c96b188` |
| `../fiscal_access_2026_09_20/_cache/CSPUF2023_Codebook.txt` | variable map | `865624a99f0cdbdca5c6903bc88c93e738046710ab1ade803abea9ca88712fed` |
| `../fiscal_access_2026_09_20/_cache/methodology/MCBSMicrodataPUFDataUsersGuide.pdf` | variance method, scope | read, not hashed by this lane |
| `../fiscal_access_2026_09_20/_cache/methodology/2023MCBSSummaryofChangesCSPUF.pdf` | published anchors, top-coding | read, not hashed by this lane |
| `../fiscal_access_2026_09_20/derived/mcbs_validation.json` | row/column/race gate targets | upstream receipt |

## Variable map

Read from `CSPUF2023_Codebook.txt`. Frequencies are the codebook's own unweighted counts over
all 6,920 records; this lane's gates require the file to reproduce them exactly.

### Classifiers

| Variable | Label in codebook | Categories (code: label, codebook frequency) |
|---|---|---|
| `CSP_AGE` | "Age Group" (format `AGE2GRP`) | `1` "1:Age Group <65" (1,058); `2` "2:Age Group [65,75)" (2,463); `3` "3:Age Group >=75" (3,399) |
| `CSP_RACE` | "Race" (format `RACE`) | `1` "1:Non-Hispanic white" (5,091); `2` "2:Non-Hispanic black" (732); `3` "3:Hispanic" (753); `4` "4:Other" (344) |
| `CSP_SEX` | "Sex code(Admin)" | `1` "1:Male" (3,103); `2` "2:Female" (3,817) |
| `CSP_INCOME` | "Household income" (format `INCOM25F`) | `1` "1:<$25,000" (2,137); `2` "2:>=$25,000" (4,783) |
| `CSP_NCHRNCND` | "Number of chronic conditions" | `1` "0-1" (851); `2` "2-3" (2,443); `3` "4+" (3,626) |

**65+ is `CSP_AGE ∈ {2, 3}`** — the codebook gives only these three age groups, with no
finer age detail and no continuous age.

**There is no dual-eligibility or Medicaid-enrolment variable.** All 34 non-replicate labels
were reviewed upstream and again here; the file carries payer *amounts* only. This lane uses
`PAMTCAID > 0` (any Medicaid payment in 2023) as a **proxy**, which undercounts partial-benefit
duals whose Medicaid coverage pays premiums or cost-sharing without generating a service
payment on this file.

### Payer amounts (all "Amount as $$$$$$.CC", all 6,920 non-missing)

| Variable | Label in codebook | Used as |
|---|---|---|
| `PAMTTOT` | "Adj. sum: total payments, all sources" | all-source total |
| `PAMTCARE` | "Adj. sum: Medicare payments" | public |
| `PAMTMADV` | "Adj. sum: Medicare MCO/HMO payments" | public (Medicare Advantage) |
| `PAMTCAID` | "Adj. sum: Medicaid payments" | public |
| `PAMTOOP` | "Adj. sum: out-of-pocket payments" | private |
| `PAMTALPR` | "Adj. sum: all priv ins. payments" (note: "Sum of Cost Supplement variables PAMTHMOP, PAMTPRVE, PAMTPRVI, and PAMTPRVU") | private |
| `PAMTOTH` | "Adj. sum: other payments (includes VA)" | other; the only bottom-coded variable |
| `PAMTDISC` | "Adj. sum: uncollected liability" | not used; keeps components below `PAMTTOT` |

`PUBLIC` is this lane's construction: `PAMTCARE + PAMTMADV + PAMTCAID`
[CALCULATION: `mcbs_elderly.py`, `build_rows`]. Eight service-type amounts (`PAMTIP`,
`PAMTMP`, `PAMTOP`, `PAMTPM`, `PAMTHH`, `PAMTDU`, `PAMTVU`, `PAMTHU`) and their event counts
exist on the file but are not used here.

### Weights

| Variable | Label | Use |
|---|---|---|
| `CSPUFWGT` | "CS PUF full sample weight" | point estimates; strictly positive on every record |
| `CSPUF001`–`CSPUF100` | "CS PUF replicate weight 1…100" | variance |

## Variance formula — what the acquired documents actually say

The **method** is prescribed, in the acquired user guide, §7.1
[DATA: `MCBSMicrodataPUFDataUsersGuide.pdf` §7.1, p.15]:

> When using the replicate weight approach to variance estimation, the variance estimation
> method of balanced repeated replication (BRR) using Fay's adjustment of 0.3 is recommended.

Appendix B gives the matching software specifications for the Cost Supplement weights
[DATA: same PDF, Appendix B, pp.21–22]:

```
SAS    proc surveymeans data=<...> VARMETHOD = brr (fay=.30); weight CSPUFWGT; repweight CSPUF001 - CSPUF100;
Stata  svyset _n [pweight= CSPUFWGT ], brrweight(CSPUF001 - CSPUF100) fay(.3) vce(brr) singleunit(missing)
R      svrepdesign(weights = ~CSPUFWGT, repweights = "CSPUF[001-100]+", type = "Fay", rho = 0.3,
                   data = <...>, combined.weights = TRUE)
```

The **algebra is not written out anywhere in the acquired codebook, user guide or summary of
changes.** This lane therefore uses the standard definition of exactly those three software
options, and labels it as such rather than as a quotation:

```
V(theta) = 1 / (R * (1 - rho)^2) * sum_{r=1..R} (theta_r - theta_0)^2
R = 100, rho = 0.3  ->  scale = 1/49
```

`combined.weights = TRUE` means the replicate columns are finished weights, not multipliers,
so each replicate estimate is formed by substituting the replicate column for `CSPUFWGT`.

Two honest caveats on that formula:

1. **Centering.** SAS and Stata centre the deviations on the full-sample estimate `theta_0`;
   R's survey package defaults to centring on the mean of the replicates. The acquired
   documents do not say which. This lane centres on `theta_0` and records the alternative in
   `derived/audit.json` under `variance.centering_sensitivity`. For the headline public-cost
   ratio the two differ by about 3% of the standard error, which changes nothing.
2. **Subsetting.** §7.1 warns that "restricting the sample to the subgroup and then performing
   an analysis would lead to slightly biased point estimates and estimates of variance", but
   §7.3 states specifically for BRR that it "allows the researcher to subset data to a
   subgroup of interest and still produce unbiased standard error estimates". §7.3 governs
   here. A domain mean is a ratio estimator computed inside each replicate, so subsetting
   per replicate is arithmetically identical to the domain estimator under BRR.

Ratio standard errors use the same formula applied to the 100 replicate **ratios**, so the
Hispanic and white estimates stay correlated through the shared replicate structure. A test
asserts the result differs from the independence-assuming delta-method value.

## Gates (fail loud, exit 2)

Every gate below must pass before any estimate is written
[CALCULATION: `mcbs_elderly.py`, `load_frame` and `run_gates`]:

- zip and CSV SHA256 equal the values pinned by `fiscal_access_2026_09_20`
- 6,920 rows, 134 columns, `PUF_ID` unique, `SURVEYYR` uniformly 2023
- `CSP_RACE` frequencies equal `mcbs_validation.json` exactly (`{1: 5091, 2: 732, 3: 753, 4: 344}`)
- `CSPUFWGT` strictly positive on every record; all 100 replicate columns present and finite
- no missing payer amounts
- **published-anchor gates**: the weighted total, the four race totals and the full age ×
  Hispanic panel must reproduce the published exhibits to the dollar (see below)

## Published anchor

`2023MCBSSummaryofChangesCSPUF.pdf` publishes weighted counts computed from this same file, so
the weighting can be checked against CMS's own arithmetic rather than asserted.

- Exhibit 3.2.3, overall and by race/ethnicity [DATA: same PDF, p.4]
- Exhibit 3.3, sample size and weighted count by age × Hispanic/non-Hispanic [DATA: same PDF, p.5]

All eighteen published cells reproduce exactly; `derived/anchor_reproduction.csv` shows
published against computed side by side. This anchors the weights and the age and ethnicity
classifiers. It does **not** anchor any cost figure: no published mean or total cost appears in
the acquired documents, so the spending estimates here are unanchored reproductions.

## Outputs

| File | Contents |
|---|---|
| `derived/elderly_cost_by_race.csv` | 200 rows: weighted mean per beneficiary with Fay SE, 95% CI, CV, unweighted n and weighted n, for each measure × race × domain |
| `derived/ratios.csv` | 50 rows: Hispanic / non-Hispanic white ratio and difference per measure × domain, each with a replicate SE and 95% CI |
| `derived/anchor_reproduction.csv` | published vs computed, Exhibit 3.3 |
| `derived/audit.json` | input hashes, every gate, the variance quotes and formula status, the centering sensitivity, caveats |

Domains: `65+`, `65-74`, `75+`, `65+ income <$25,000`, `65+ income >=$25,000`.
Measures: the seven payer amounts, the constructed `PUBLIC`, plus two shares —
`ANY_MEDICAID` (`PAMTCAID > 0`, dual proxy) and `ANY_MADV` (`PAMTMADV > 0`, MA-enrolment proxy).

## Scope limits carried into RESULT.md

- **Community-dwelling, full year.** "The MCBS Cost Supplement File Microdata PUF includes only
  beneficiaries living in the community the entire year. The file excludes beneficiaries who
  had a Facility interview during the year or who incurred any facility, hospice, or
  institutional events or costs during the year."
  [DATA: `MCBSMicrodataPUFDataUsersGuide.pdf` §3.3, p.4]
- **Top-coding.** "All of the service- and payer-specific costs and events variables are
  top-coded at the 99.5 percent level… Their values are then replaced by the mean value of the
  top 0.5 percent." [DATA: same PDF §3.4, p.6]
- **Medicare Advantage accounting.** `PAMTMADV` is what the MCO/HMO paid for events, not the
  capitation CMS paid the plan. Where MA enrolment differs by group, `PUBLIC` is a
  payments-for-services measure, not a government-outlay measure.
- 2023 calendar year; no country of birth; ever-enrolled population.
