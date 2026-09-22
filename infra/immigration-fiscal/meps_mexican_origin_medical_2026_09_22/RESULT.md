**Verdict:** In the very MEPS file the fiscal ledger transports medical costs from, Mexican-origin people draw **less** public medical money per person than the all-donor average the transport assigns them, not more. At 65+ the Mexican-origin/all-donor public ratio is **0.893 (SE 0.145, 95% CI 0.610-1.177)**; across all ages it is **0.757 (SE 0.211, CI 0.344-1.171)**; among 18-64-year-olds it is **0.688 (SE 0.095, CI 0.502-0.873)**, the only one of the three whose interval excludes parity [DATA: `derived/ratios.csv`; CALCULATION: `meps_mexican.py`]. Against non-Hispanic whites the same figures are 0.886, 0.659 and 0.625. Medicaid runs the other way and is the whole of the payer story: **25.8% of Mexican-origin 65+ have any Medicaid coverage against 7.1% of non-Hispanic whites and 12.4% of all donors** (ratios 3.61, SE 0.48, and 2.08, SE 0.23), Medicaid dollars at 65+ are 3.33x white (CI 1.368-5.284, excludes 1), and out-of-pocket and private payments are roughly 0.4x white at every age [DATA: `derived/cells.csv`, `derived/ratios.csv`]. Coverage composition is what holds the public ratio as high as it is: standardizing the Medicaid-coverage mix to the all-donor mix drops the 65+ public ratio from 0.893 to **0.796 (SE 0.143)** and the 18-64 ratio from 0.688 to **0.554 (SE 0.070)** [DATA: `derived/ratios.csv`, rows `subgroup=coverage_standardized`]. Translated onto the union's own ledger cells, the 65+ bands imply **+$2.74bn** (SE $6.69bn, i.e. a $2.7bn *smaller* cost) and the all-bands total **−$26.57bn** (SE $29.66bn, a larger cost) [DATA: `derived/ledger_translation.csv`]. **The all-bands total is not usable.** Its sign is set by a single record: one 4-year-old with $1,242,405 in Medicaid payments and a weight of 25,339 supplies **68.3%** of the Mexican-origin 0-17 public mean; remove that one observation and the 0-17 ratio falls from 2.425 to 1.090 and the all-bands medical translation flips from −$16.06bn to **+$20.19bn** [DATA: `derived/audit.json` `leave_one_out`; `derived/ledger_translation.csv` column `delta_medical_bn_drop_top1`]. The defensible reading is the adult and elderly bands, where every ratio sits at or below 1 and the transport, if anything, over-charges the Mexican-origin population for public medical care.

Method, variable map with codebook quotes, gates and the estimator: [README.md](README.md).
Hashes, reproduced anchors and the standard-error validation: `derived/audit.json`.

## Gates: every published anchor reproduces exactly

All eight `HISPNCAT` codebook categories reproduce unweighted and weighted, including the
Mexican-origin cell at **2,679 / 42,446,768**; the transport's two nativity anchors reproduce
to the dollar (**285,498,519** US-born, **52,835,316** born elsewhere); `nh_white` defined as
`HISPANX == 2 & RACEV1X == 1` reproduces `RACETHX == 2` at **10,766 / 191,692,001**; and
`MCDEV24 == 1` reproduces **4,941 / 78,147,553** [DATA: `h256cb.pdf` pp.107-109, 121, 469;
CALCULATION: `derived/audit.json` `gates`]. The design carries 105 strata and 264 PSUs among
positive-weight records with a minimum of 2 PSUs per stratum, so no variance fallback is used.

**Standard errors are validated.** The 65+ public ratio's linearized SE is **0.1446**; a
Rao-Wu(n_h − 1) rescaling bootstrap over PSUs within strata, 2,000 replicates, gives
**0.1473**, 1.9% apart [CALCULATION: `derived/audit.json` `se_validation`].

## Weighted payments per person, 2024 dollars

Public = `TOTMCR24 + TOTMCD24 + TOTVA24 + TOTTRI24 + TOTOFD24 + TOTSTL24`, the transport's own
list. `all_donors` is the transport's valid set [DATA: `derived/cells.csv`].

| Domain | Group | n | Public | SE | Medicare | Medicaid | Out of pocket | Private | All sources | Share ever Medicaid |
|---|---|---|---|---|---|---|---|---|---|---|
| All ages | Mexican-origin | 2,576 | **2,640** | 818 | 743 | 1,672 | 530 | 1,506 | 4,744 | 0.368 |
| All ages | NH white | 10,438 | **4,006** | 186 | 2,851 | 789 | 1,469 | 4,627 | 10,208 | 0.151 |
| All ages | All donors | 18,476 | **3,485** | 171 | 2,138 | 1,041 | 1,119 | 3,605 | 8,305 | 0.230 |
| 65+ | Mexican-origin | 280 | **9,794** | 1,650 | 8,386 | 974 | 921 | 1,112 | 11,939 | 0.258 |
| 65+ | NH white | 3,502 | **11,057** | 409 | 9,927 | 293 | 2,300 | 2,967 | 16,473 | 0.071 |
| 65+ | All donors | 4,839 | **10,963** | 389 | 9,594 | 531 | 1,963 | 2,696 | 15,757 | 0.124 |
| 18-64 | Mexican-origin | 1,567 | **1,314** | 170 | 199 | 883 | 621 | 1,908 | 3,931 | 0.258 |
| 18-64 | All donors | 10,092 | **1,911** | 141 | 619 | 1,066 | 1,084 | 4,635 | 7,739 | 0.189 |
| 0-17 | Mexican-origin | 729 | **3,620** | 2,407 | 0 | 3,462 | 247 | 777 | 4,662 | 0.619 |
| 0-17 | All donors | 3,545 | **1,489** | 446 | 4 | 1,408 | 494 | 1,510 | 3,522 | 0.436 |

The 0-17 Mexican-origin row has a standard error two-thirds the size of its mean. That is the
outlier, discussed below, not noise that averages away.

## The transport's own cells: Mexican-origin / all-donor public ratio

These are exactly the donor cells `donor_model` matches on, age band x US birth
[DATA: `derived/ratios.csv`, `scheme=transport`].

| Band | Nativity | n Mexican | Ratio | SE | 95% CI | Excludes 1 |
|---|---|---|---|---|---|---|
| 0-17 | US-born | 691 | 2.436 | 0.946 | 0.582 - 4.289 | no |
| 0-17 | foreign-born | 38 | 1.364 | 0.487 | 0.409 - 2.319 | no |
| 18-34 | US-born | 507 | 0.895 | 0.214 | 0.477 - 1.314 | no |
| 18-34 | foreign-born | 134 | **1.998** | 0.416 | 1.183 - 2.814 | **yes** |
| 35-49 | US-born | 209 | **0.616** | 0.186 | 0.251 - 0.980 | **yes** |
| 35-49 | foreign-born | 294 | 1.178 | 0.339 | 0.514 - 1.841 | no |
| 50-64 | US-born | 154 | 0.965 | 0.234 | 0.505 - 1.424 | no |
| 50-64 | foreign-born | 269 | 0.582 | 0.276 | 0.041 - 1.122 | no |
| 65+ | US-born | 125 | 0.971 | 0.218 | 0.543 - 1.398 | no |
| 65+ | foreign-born | 155 | 0.844 | 0.163 | 0.524 - 1.164 | no |

Ten cells, two of which exclude 1, in opposite directions. Nothing here supports a single
multiplicative ethnicity adjustment to the transport. The 18-34 foreign-born cell at 1.998 is
the one clear excess and it is a small-dollar cell: $1,606 against $804 per person.

## How much of the difference is Medicaid coverage

Two cuts. First, within coverage strata; second, direct standardization holding the coverage
mix at the all-donor mix [DATA: `derived/ratios.csv`].

| Domain | Denominator | Pooled public ratio | Within Medicaid-covered | Within not covered | Coverage-standardized | SE | Composition part |
|---|---|---|---|---|---|---|---|
| 65+ | all donors | 0.893 | 0.884 (n 106) | 0.773 (n 174) | **0.796** | 0.143 | +0.098 |
| 65+ | NH white | 0.886 | 0.843 | 0.738 | **0.759** | 0.143 | +0.126 |
| 18-64 | all donors | 0.688 | 0.520 (n 445) | 0.666 (n 1,122) | **0.554** | 0.070 | +0.134 |
| 18-64 | NH white | 0.625 | 0.378 | 0.555 | **0.415** | 0.065 | +0.211 |
| All ages | all donors | 0.757 | - | - | **0.582** | 0.129 | +0.176 |

In every domain the pooled ratio sits **above** both within-stratum ratios. Mexican-origin
people are likelier to be in the Medicaid-covered stratum, which spends more public money, and
that composition raises the pooled ratio by 0.10 to 0.21. Strip it out and the Mexican-origin
population's public medical spending is 20-45% below the donor cell it is matched to. This is
the same mechanism the MCBS lane found, with Medicaid coverage standing in for income.

## Translation onto the union's ledger cells

Each band's `medical` and `M` charge for `mexican_observed_total` multiplied by that band's
MEPS ratio, the two nativity cells combined with the union's own per-band foreign-born share
from `age_profiles.csv`. Positive means a smaller cost. `M` is rescaled with payer-specific
ratios because it is a fixed linear form in the Medicaid and Medicare donor means
[DATA: `derived/ledger_translation.csv`; `../ledger_absolute_2026_09_17/params/params.json`].

| Band | Union pop | FB share | n Mex | Ledger medical $bn | Ledger M $bn | Ratio | SE | Δ medical $bn | Δ M $bn | Δ total $bn | SE | Δ medical, leave-one-out |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0-17 | 12.12M | 0.045 | 729 | −17.77 | −9.14 | 2.425 | 0.939 | −25.31 | −13.24 | **−38.56** | 25.67 | **−1.60** |
| 18-24 | 5.02M | 0.115 | 283 | −5.25 | −2.46 | 0.882 | 0.224 | +0.62 | +0.12 | +0.74 | 1.77 | +1.32 |
| 25-34 | 6.30M | 0.269 | 358 | −6.32 | −2.92 | 1.241 | 0.307 | −1.52 | +0.19 | −1.33 | 2.80 | −0.02 |
| 35-44 | 5.69M | 0.454 | 342 | −7.58 | −3.18 | 0.731 | 0.194 | +2.04 | +1.45 | +3.49 | 1.75 | +3.95 |
| 45-54 | 4.92M | 0.583 | 301 | −10.47 | −3.81 | 0.731 | 0.202 | +2.81 | +0.40 | +3.22 | 3.09 | +5.45 |
| 55-64 | 3.67M | 0.625 | 283 | −11.58 | −3.94 | 0.748 | 0.254 | +2.92 | +0.21 | +3.13 | 4.06 | +4.04 |
| 65-74 | 2.05M | 0.543 | 172 | −21.96 | −6.30 | 0.984 | 0.217 | +0.35 | −0.19 | +0.16 | 6.14 | +4.79 |
| 75+ | 1.11M | 0.482 | 108 | −11.95 | −3.41 | 0.830 | 0.184 | +2.03 | +0.54 | +2.58 | 2.79 | +2.26 |
| **65+** | 3.16M | - | 280 | −33.91 | −9.71 | - | - | **+2.39** | +0.35 | **+2.74** | **6.69** | +7.04 |
| **All bands** | 40.90M | - | 2,576 | −92.88 | −35.15 | - | - | **−16.06** | −10.51 | **−26.57** | **29.66** | **+20.19** |

Read the last column against the ninth. Six of the eight bands imply a *smaller* medical cost
for the union. The all-bands total is negative only because band 0-17 carries a ratio of 2.425,
and that ratio is one record.

## The one record

| Field | Value |
|---|---|
| Age | 4 |
| `TOTMCD24` | $1,242,405 |
| `PERWT24F` | 25,338.68 |
| Share of the Mexican-origin 0-17 weighted public mean | **68.3%** |
| Same statistic for all 0-17 donors (n 3,545) | 29.2% |
| 0-17 Mexican/all-donor public ratio with it | 2.425 |
| 0-17 ratio without it | **1.090** |

[DATA: `derived/audit.json` `leave_one_out.bands.0`]. $1,242,405 is the top of the codebook's
`TOTEXP24` range, so this is a retained catastrophic case, not a coding error. The same record
is the largest contributor in both rows above; it carries 29.2% of the mean over all 3,545
under-18 donors and 68.3% over the 729 Mexican-origin ones, purely because the subsample is
smaller. No standard error is quoted for the leave-one-out: it is a one-observation
sensitivity, not a design-based estimate.

## Secondary: pooling 2023 with 2024 at 65+

HC-251 pooled with HC-256 at half weight each, 2023 dollars deflated by the CPI-U annual-average
ratio 313.698/304.703 = **1.0295** taken from the acquired FRED file, 2023 strata offset so the
two samples never share one [DATA: `external/fred/cpi_all_urban.csv`; `derived/audit.json`
`pooled_2023_2024_65plus`]. The pooled 65+ public ratio is **0.810 (SE 0.090)** against all
donors and **0.798 (SE 0.093)** against non-Hispanic whites, on 558 Mexican-origin records
against 280 in 2024 alone. It sits below the 2024 point estimate with a smaller interval and
does not touch 1. **2024 is primary** because it is the transport's year; the pooled figure is
a precision check, and it points the same way.

## How this sits against the MCBS 65+ lane

[`../mcbs_elderly_medical_2026_09_22/RESULT.md`](../mcbs_elderly_medical_2026_09_22/RESULT.md)
found Hispanic/non-Hispanic-white public payments at 65+ of **1.265 (CI 0.966-1.564)**. This
lane finds Mexican-origin/non-Hispanic-white at 65+ of **0.886 (CI 0.589-1.182)**. The intervals
overlap only on 0.97-1.18, and four differences explain the gap rather than either being wrong:
MCBS covers **Medicare beneficiaries living in the community all year** while MEPS 65+ covers
all non-institutional 65+ residents; MCBS `CSP_RACE=3` pools every Hispanic origin while this
lane isolates Mexican-origin; MCBS is 2023 and this is 2024; and MCBS counts Medicare Advantage
plan payments for services, not capitation. What both agree on is the mechanism: far higher
Medicaid coverage and dollars, far lower out-of-pocket and private payments, near-equal or lower
total spending, and a pooled public ratio held up by composition that falls once the composition
is held fixed. Neither lane licenses a flat ethnicity multiplier on the transport.

## Limits

- **MEPS excludes institutional residents.** The file is the civilian non-institutionalized
  population. Long-term institutional care is Medicaid's largest 65+ outlay and is absent here,
  so nothing in this lane bounds the institutional public-medical cell. The ledger prices that
  separately in item `N`.
- **Mexican-origin is self-reported origin, not birthplace and not generation.** `HISPNCAT == 1`
  is "MEXICAN/MEX AMER/CHICANO - NO OTHER HISP RPTD". `BORNUSA` splits nativity and `YRSINUS`
  gives duration, but MEPS carries no country of birth and no parental birthplace, so the
  US-born cell pools second and later generations exactly as the ledger's union does. A person
  of Mexican descent who reports multiple Hispanic origins falls in `HISPNCAT == 8`, not here.
- **The 65+ Mexican cell is 280 records** (125 US-born, 155 foreign-born), and the 75+ ledger
  band has 108. Every 65+ interval here is wide enough to contain both a 40% shortfall and
  parity. The 18-24 foreign-born cell has 28 records and the 0-17 foreign-born cell 38.
- **One income year.** 2024 only for the primary estimates; the 2023 pooling is a precision
  check on the 65+ cells alone and carries no trend claim.
- **No income dimension.** The MCBS lane showed income reversing the sign of the 65+ Hispanic
  public ratio. MEPS HC-256 carries income, and this lane does not use it. The
  coverage-standardized rows are the nearest available control and they are not a substitute:
  Medicaid coverage is downstream of income, so standardizing on coverage absorbs part of the
  income effect and part of the eligibility effect without separating them.
- **The translation's assumption.** Multiplying the union's charge by the MEPS ratio assumes the
  union's members in a band resemble MEPS Mexican-origin donors in that band. The union is
  defined on CPS ancestry and nativity; the MEPS group is defined on self-reported Hispanic
  origin. They are not the same population, and the translation does not re-run the ledger or
  change any committed number.
- **Top-coding cuts both ways.** MEPS retains catastrophic cases rather than trimming them, which
  is why one record can carry the 0-17 cell. A trimmed or winsorized estimate would be more
  stable and would no longer be the same estimand as the transport's untrimmed cell mean.
- **`M` rescaling is an approximation within band.** Item `M`'s two NHEA coefficients are fixed
  at 1.5432 and 1.2804 and are applied here to the band-level Medicaid and Medicare donor means.
  The ledger applies them record by record, so a band whose within-band payer mix differs
  between the union and MEPS donors will move slightly differently.
- **Instrument bias.** Per `notes/llm-bias-caveat.md`, this analysis was produced through an LLM
  on a politically charged topic. Every number above is reproducible from
  `meps_mexican.py` against a hashed input; the framing choices, especially which of the two
  translation totals to call unusable, are judgement and are stated as such.
