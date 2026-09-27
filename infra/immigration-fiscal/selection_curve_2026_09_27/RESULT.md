claude-opus-5-5

**Verdict:** For India-born and Indian G2, the high-skill advantage is a shift of the whole
upper three-quarters of the distribution. It is not a top-1% effect. Capping everyone's wage
earnings at the white p99 keeps 92% of the India-born earnings gap, and dropping everyone above
the white p99 keeps 94% of the partial fiscal gap (+$10,086 of +$10,732). China-born is the
exception: its advantage lives above the white p90, and its median sits below the white median.
Across 78 parental origins, the G1→G2 rank slope is **0.52** on education percentile (95%
interval over origins 0.29–0.59) and **0.55** on earnings (0.19–0.68). About half of a first
generation's distance from the white mean carries to its children, on top of a common uplift of
about 5 points at the white median. Mexico is the high-leverage point: without it the slopes are
0.36 and 0.30. Mexico's G2 sits 8 points below the line that the other 77 origins draw (5 on
earnings). The operator's "how selected" axis is the G1's percentile within its origin country,
measured on immigrants who arrived at 25 or older, whose schooling was not acquired in the US. It
predicts where those adult arrivals land in the US (R² 0.28 without Mexico; slope 1.19,
interval 0.45–1.75). It adds little to G2 outcomes once the G1's US position is known: without
Mexico, 0.12 (−0.22 to 0.38) on G2 education and 0.00 on G2 earnings. So selection works
through where the parents land. The earlier pooled R² of 0.10 was diluted by child arrivals
(R² 0.00 in that arm). The G2→G3 link is the weak one:
GSS gives 0.72 on education (0.23–1.06, 20 mostly European origins, 0.56 without Mexico), and
the literature gives 0.46–0.53 (Borjas 1994). India sits at origin percentile 95 → US 73 → G2 73
→ G3 about 67 [MODEL]. Mexico sits at 58 → 16 → 36 → about 40 [MODEL]. Mexico's observed G3
stalls near its G2, so the model overstates its convergence.

Model self-report: claude-opus-5-5. 2026-09-27. All gates pass (`verify.py`, exit 0).
Descriptive only: generation means observed in the same years are synthetic cohorts, not the
same families. [FRAMING-SENSITIVE: the reference is the third-plus-generation non-Hispanic white
distribution; "percentile" means a weighted mid-rank in that reference's year × five-year-age
cell, so the reference mean is 50 by construction]

## Gates

| gate | result |
|---|---|
| CPS extract sha256 = manifest (`a510e7a9…`) | PASS |
| Ladder 178: Mexican G2 no-HS gap, recomputed with the V02 lane's own `wls_gaps` | PASS, 0.11836 vs 0.1184 |
| Indian ledger: India-born gap raw / top-1% (SPM resources) excluded | PASS, +10,732 / +10,488 |
| Reference mean percentile = 50 (CPS edu, earn, ×sex; GSS edu, income) | PASS, all 50.000000 |
| Main slopes re-derive from `origin_curve.csv`; projection rows match observed | PASS |
| Barro-Lee v3 `618732c5…`, WIC v3 SSP2 `ddbdac12…`, GSS 7224 R3a `a7622e03…` hashes | PASS |

## 1. Top tail or whole distribution? (task 1)

The CPS ASEC 2015–2025 are pooled. The universe is civilian adults 25–64 (V02 lane rules), with
weights reweighted to the white reference's age-band mix. Earnings are IPUMS `INCWAGE`, zeros
included, in 2024 dollars (FRED CPIAUCSL annual; the ASEC year's income year).
`[CALCULATION: derived/percentile_distribution.csv, derived/tail_share.csv]`

| group | outcome | n | mean pct (se) | p10 | p25 | p50 | p75 | p90 | above white p90 / p95 / p99 |
|---|---|---|---|---|---|---|---|---|---|
| White reference G3+ | earnings incl. 0 | 496,750 | 50.0 | 11 | 22 | 50 | 75 | 90 | 0.100 / 0.050 / 0.010 |
| White reference G3+ | education | 496,750 | 50.0 | 15 | 21 | 49 | 73 | 90 | 0.102 / 0.035 / 0.009 |
| India G1 | earnings incl. 0 | 12,525 | 59.5 (0.4) | 10 | 22 | 70 | 91 | 96 | 0.260 / 0.141 / 0.023 |
| India G1 | education | 12,525 | 73.5 (0.3) | 21 | 68 | 77 | 91 | 94 | 0.323 / 0.091 / 0.030 |
| India G1 | earnings > 0 | 9,764 | 65.9 (0.4) | 14 | 43 | 78 | 91 | 96 | 0.279 / 0.144 / 0.021 |
| India G2 | earnings incl. 0 | 1,498 | 61.4 (1.3) | 13 | 29 | 71 | 91 | 97 | 0.259 / 0.159 / 0.035 |
| India G2 | education | 1,498 | 72.3 (1.1) | 22 | 67 | 76 | 92 | 99 | 0.322 / 0.200 / 0.046 |
| China G1 | earnings incl. 0 | 7,750 | 48.4 (0.4) | 9 | 20 | 43 | 81 | 94 | 0.155 / 0.087 / 0.015 |
| China G1 | education | 7,750 | 59.1 (0.4) | 3 | 20 | 71 | 91 | 99 | 0.293 / 0.138 / 0.051 |
| China G2 | earnings incl. 0 | 1,747 | 58.0 (0.9) | 11 | 24 | 65 | 88 | 96 | 0.216 / 0.127 / 0.032 |
| China G2 | education | 1,747 | 66.6 (0.7) | 20 | 63 | 72 | 89 | 94 | 0.210 / 0.094 / 0.019 |
| Philippines G1 | earnings incl. 0 | 8,753 | 49.8 (0.4) | 11 | 26 | 49 | 73 | 88 | 0.080 / 0.034 / 0.004 |
| Philippines G1 | education | 8,753 | 55.8 (0.3) | 17 | 37 | 67 | 73 | 78 | 0.074 / 0.032 / 0.009 |
| Philippines G2 | earnings incl. 0 | 3,459 | 54.9 (0.7) | 11 | 28 | 57 | 81 | 93 | 0.131 / 0.064 / 0.008 |
| Philippines G2 | education | 3,459 | 57.7 (0.6) | 17 | 37 | 67 | 74 | 91 | 0.117 / 0.042 / 0.008 |
| Mexico G1 | earnings incl. 0 | 59,003 | 35.1 (0.1) | 9 | 15 | 32 | 49 | 66 | 0.017 / 0.009 / 0.002 |
| Mexico G1 | education | 59,003 | 18.5 (0.1) | 0 | 1 | 15 | 21 | 62 | 0.017 / 0.006 / 0.001 |
| Mexico G2 | earnings incl. 0 | 23,990 | 42.9 (0.2) | 10 | 21 | 40 | 63 | 82 | 0.046 / 0.018 / 0.004 |
| Mexico G2 | education | 23,990 | 36.3 (0.2) | 3 | 16 | 33 | 54 | 75 | 0.043 / 0.012 / 0.003 |
| All foreign-born G1 | earnings incl. 0 | 197,161 | 43.0 (0.1) | 9 | 20 | 38 | 64 | 87 | 0.080 / 0.042 / 0.008 |
| All G2 | earnings incl. 0 | 74,316 | 49.5 (0.1) | 10 | 22 | 48 | 75 | 91 | 0.109 / 0.056 / 0.012 |

Positive-earner rows for every group, and the China-plus-Hong-Kong-Taiwan row, are in the CSV.
The India-born distribution matches the white one at the bottom quarter (p25 22 vs 22), where
the non-earners sit; about a fifth of India-born adults (22% unweighted) have no wage income. From the median
up it is displaced by 20 points: p50 70 vs 50, p75 91 vs 75. On education, the whole distribution
above p10 is shifted (p25 68 vs 21). About 2.3% are above the white p99, against 1%. That is a
2.3× over-representation of a tail that carries little of the dollar gap.

**Earnings gap and the tail** (2024 $, age-standardised) `[CALCULATION: derived/tail_share.csv]`.
The "winsorised" column caps every person, group and white, at the white threshold of their cell.
The "excluding" column drops persons above the threshold from both groups.

| group | gap | cap at white p99 (kept) | cap at p95 | cap at p90 | exclude above p99 | exclude above p90 |
|---|---|---|---|---|---|---|
| India G1 | +34,195 | +31,363 (92%) | +24,403 (71%) | +18,805 (55%) | +28,167 | +5,886 |
| India G2 | +43,786 | +40,679 (93%) | +27,751 (63%) | +21,495 (49%) | +33,305 | +8,179 |
| China G1 | +3,281 | +3,429 (105%) | +1,043 | −881 | +2,537 | −6,634 |
| China G2 | +32,072 | +25,968 (81%) | +19,057 | +14,722 | +20,043 | +5,676 |
| Philippines G1 | −4,863 | −3,209 | −1,180 | −294 | −1,290 | +1,578 |
| Philippines G2 | +8,040 | +9,957 | +9,693 | +8,538 | +10,548 | +6,567 |
| Mexico G1 | −31,949 | −30,076 (94%) | −26,591 | −23,816 | −27,876 | −16,815 |
| Mexico G2 | −16,941 | −15,545 (92%) | −12,888 | −10,971 | −13,924 | −6,558 |

**Partial fiscal gap and the tail.** This uses the Indian ledger's person-level net after
health: CPS ASEC 2025 public file, `equal_all_members`, 160-replicate SDR. Thresholds are the
white p90/p95/p99 of own earnings (`PEARNVAL`) by ten-year age band. The ledger is re-run
unchanged through `ledger_dump.py`. `[CALCULATION: derived/tail_share_fiscal.csv]`

| group | gap (se) | above white p99: group vs white share | gap from persons above p99 | gap excluding persons above p99 (se) | excluding above p95 | excluding above p90 |
|---|---|---|---|---|---|---|
| India-born | +10,732 (1,351) | 0.021 vs 0.009 | +998 (9%) | **+10,086 (1,113)** | +7,857 (950) | +6,529 (936) |
| Indian G2 | +20,572 (3,872) | 0.029 vs 0.009 | +4,164 (20%) | +17,140 (2,786) | +13,472 (2,591) | +12,692 (2,756) |
| China-born | +8,446 (2,523) | 0.028 vs 0.009 | +2,083 (25%) | +6,778 (1,946) | +4,092 (1,483) | +1,480 (1,267) |
| Mexico-born | −10,794 (405) | 0.002 vs 0.009 | −1,157 (11%) | −9,741 (319) | −8,496 (295) | −7,338 (295) |
| Mexican G2 | −7,923 (448) | 0.003 vs 0.009 | −1,148 (14%) | −6,866 (396) | −5,696 (372) | −4,946 (356) |
| All foreign-born | −3,209 (440) | 0.009 vs 0.009 | −158 (5%) | −3,075 (326) | −3,058 (309) | −2,938 (326) |

The India-born fiscal advantage survives every cut. It is still +$6.5k among people below the
white p90, where 75% of India-born adults sit. China-born loses significance below the white p90
(+1,480, se 1,267). The Mexico-born deficit is also a whole-distribution effect: 90% of it
remains among people below the white p99.

**What "without the top 1%" can mean in CPS.** The public ASEC files for 2011 onward apply rank
proximity swapping to earnings at or above a threshold. For the ASEC 2025 longest-job earnings
field (`ERN_VAL`) the threshold is **$458,000**. Swapped values are rounded to two significant
digits, and the procedure "preserves the distribution of values above the topcode"
[SOURCE: CPS ASEC 2025 technical documentation, Data Disclosure Avoidance Techniques pp. 8-5 to
8-7, `indian_ledger_2026_09_18/_cache/cpsmar25.txt` lines 8013–8069]. The maximum `INCWAGE` on the
IPUMS file for 2015–2025 runs from $1.26M to $2.10M. The white p99 threshold by year × age cell
has a median of $300k (range $150–600k). It lies below the 2025 swap threshold in most cells, so
"above the white p99" is observed; in the oldest bands it falls in the swap zone, where values
are swapped but the distribution is kept. What the
survey cannot see is the extreme tail: CPS under-covers top incomes against tax data
[TRAINING-DATA]. Individual values above $458k are swapped, and pre-2011 files (used in task 2
only through ranks) replace them with cell means. "Excluding the top 1%" here means the top 1% of
CPS respondents, not the tax-data top 1%. The answer to the operator's question does not depend on
that tail, because 92–94% of the India gap sits below the white p99 in both the earnings and the
fiscal measure.

## 2. The origin-level curve, G1 → G2 (task 2)

IPUMS-CPS ASEC 1994–2025, 2.87M adults, 78 parental birthplaces with ≥150 G2 adults and ≥100
G1 adults. Codes are merged where IPUMS splits a country (Korea/South Korea, UK parts, USSR, Czech
and Slovak, Azores to Portugal), and n.s. or residual codes are dropped. A G2 adult's origin is
the father's birthplace if he was foreign-born, else the mother's (V02 rule). G1 and G2 origin
means are age-standardised to the reference. The fit is a WLS across origins, weighted by G2 n as
the brief specifies. Intervals are the 2.5th–97.5th percentiles of 2,000 resamples of origins.
Mean reliability of the G1 origin means is 0.96–0.999, so attenuation is negligible.
`[CALCULATION: derived/origin_curve.csv, derived/slopes.csv, derived/focus_origins.csv]`

Every computed spec:

| spec | origins | slope | 95% interval | intercept | R² (wtd) |
|---|---|---|---|---|---|
| G1->G2 education, main | 78 | 0.52 | 0.29 – 0.59 | 28.7 | 0.87 |
| G1->G2 earnings, main | 78 | 0.55 | 0.19 – 0.68 | 25.7 | 0.72 |
| G1->G2 education, age x sex x year cells | 78 | 0.52 | 0.28 – 0.60 | 28.6 | 0.86 |
| G1->G2 earnings, age x sex x year cells | 78 | 0.52 | 0.18 – 0.63 | 27.4 | 0.74 |
| G1->G2 total income | 78 | 0.57 | 0.23 – 0.68 | 25.6 | 0.78 |
| G1 education -> G2 earnings | 78 | 0.23 | 0.11 – 0.27 | 40.3 | 0.78 |
| G1->G2 education, unweighted | 78 | 0.45 | 0.37 – 0.52 | 34.3 | 0.62 |
| G1->G2 earnings, unweighted | 78 | 0.47 | 0.32 – 0.61 | 30.7 | 0.38 |
| G1->G2 education, sqrt(n) weights | 78 | 0.48 | 0.35 – 0.55 | 32.1 | 0.74 |
| G1->G2 earnings, sqrt(n) weights | 78 | 0.48 | 0.28 – 0.61 | 29.7 | 0.49 |
| G1->G2 education, not age-standardised | 78 | 0.53 | 0.30 – 0.60 | 28.5 | 0.86 |
| G1->G2 education, G1 1994–2004 vs G2 2015–2025 | 68 | 0.54 | 0.32 – 0.60 | 29.7 | 0.88 |
| G1->G2 earnings, G1 1994–2004 vs G2 2015–2025 | 68 | 0.68 | 0.24 – 0.83 | 20.9 | 0.66 |
| G1->G2 education, G2 both parents foreign | 76 | 0.64 | 0.46 – 0.70 | 24.8 | 0.92 |
| G1->G2 earnings, G2 both parents foreign | 76 | 0.71 | 0.41 – 0.81 | 19.4 | 0.79 |
| G1->G2 education, G2 2015–2025 | 78 | 0.55 | 0.35 – 0.61 | 28.2 | 0.88 |
| G1->G2 earnings, G2 2015–2025 | 78 | 0.65 | 0.26 – 0.79 | 21.4 | 0.68 |
| origin selection -> G1 US education | 77 | 1.51 | 0.07 – 1.70 | −67.6 | 0.68 |
| origin selection -> G2 US education | 77 | 0.87 | 0.07 – 1.00 | −12.9 | 0.72 |
| origin selection -> G2 US earnings | 77 | 0.38 | −0.03 – 0.44 | 22.4 | 0.62 |
| origin selection -> G1 US education, without Mexico | 76 | 0.62 | −0.02 – 1.35 | 4.4 | 0.10 |
| origin selection -> G2 US education, without Mexico | 76 | 0.33 | −0.01 – 0.63 | 31.3 | 0.12 |
| origin selection (Barro-Lee only) -> G2 US education | 74 | 0.87 | 0.07 – 0.99 | −12.9 | 0.72 |
| origin selection (WIC 2020 only) -> G2 US education | 77 | 0.48 | −0.09 – 0.79 | 22.2 | 0.30 |
| origin selection (WIC 2020 only) -> G1 US education | 77 | 0.62 | −0.46 – 1.23 | 5.9 | 0.16 |
| G1->G2 education, origins with G1 below white median | 34 | 0.68 | 0.43 – 0.78 | 25.1 | 0.94 |
| G1->G2 education, origins with G1 at/above white median | 44 | 0.31 | −0.13 – 0.68 | 40.7 | 0.10 |
| G1->G2 education, below white median, without Mexico | 33 | 0.49 | 0.42 – 0.67 | 33.3 | 0.76 |
| G1->G2 education, low origin-selection half | 38 | 0.54 | 0.27 – 0.65 | 28.2 | 0.89 |
| G1->G2 education, high origin-selection half | 39 | 0.37 | 0.16 – 0.58 | 37.4 | 0.31 |
| G1->G2 education, without Mexico | 77 | 0.36 | 0.26 – 0.47 | 38.2 | 0.52 |
| G1->G2 education, without Mexico, India, China, Philippines | 74 | 0.32 | 0.24 – 0.42 | 39.5 | 0.54 |
| G1->G2 earnings, origins with G1 below white median | 55 | 0.74 | 0.37 – 0.91 | 18.5 | 0.80 |
| G1->G2 earnings, origins with G1 at/above white median | 23 | 0.27 | −0.52 – 1.06 | 39.1 | 0.05 |
| G1->G2 earnings, below white median, without Mexico | 54 | 0.51 | 0.31 – 0.76 | 29.6 | 0.40 |
| G1->G2 earnings, low origin-selection half | 38 | 0.59 | 0.18 – 0.78 | 24.1 | 0.77 |
| G1->G2 earnings, high origin-selection half | 39 | 0.25 | −0.06 – 0.58 | 40.8 | 0.13 |
| G1->G2 earnings, without Mexico | 77 | 0.30 | 0.14 – 0.49 | 38.4 | 0.26 |
| G1->G2 earnings, without Mexico, India, China, Philippines | 74 | 0.27 | 0.11 – 0.46 | 39.6 | 0.25 |

The named origins relative to the line, on education percentile. The leave-one-out residual
measures each origin against the line fitted on the other 77.

| origin | n G1 | n G2 | origin selection pct | G1 US pct | G2 US pct | residual | LOO residual | G1 earn | G2 earn | LOO residual (earn) |
|---|---|---|---|---|---|---|---|---|---|---|
| India | 25,134 | 2,608 | 94.5 | 73.1 | 72.6 | +5.7 | +6.0 | 57.9 | 60.6 | +3.1 |
| Mexico | 161,785 | 50,183 | 58.5 | 16.4 | 35.7 | −1.6 | **−8.4** | 34.4 | 43.4 | −5.4 |
| China | 17,885 | 4,051 | 86.4 | 57.2 | 68.1 | +9.5 | +9.9 | 47.9 | 58.2 | +6.2 |
| Philippines | 24,845 | 7,725 | 84.8 | 58.2 | 56.7 | −2.4 | −2.6 | 51.1 | 53.7 | −0.1 |
| Vietnam | 13,640 | 2,027 | 86.6 | 38.9 | 55.6 | +6.5 | +6.6 | 42.6 | 51.7 | +2.5 |
| Nigeria | 2,627 | 451 | 89.5 (WIC) | 66.7 | 64.6 | +1.0 | +1.0 | 50.4 | 56.4 | +2.9 |
| Korea | 11,729 | 2,403 | 70.0 | 60.1 | 64.9 | +4.8 | +4.9 | 43.6 | 56.7 | +7.0 |
| Cuba | 13,694 | 4,430 | 72.7 | 40.0 | 56.0 | +6.4 | +6.6 | 40.5 | 53.0 | +5.1 |
| El Salvador | 18,525 | 2,988 | 69.1 | 18.8 | 43.6 | +5.1 | +5.3 | 37.1 | 46.7 | +0.6 |

Reading:

- **About half carries over, with a common uplift.** The G2 line is roughly 28.7 + 0.52 × G1.
  An origin whose G1 sits at the white median has children at about 55, and the line's fixed
  point is about 60. The slope reproduces the published cross-origin estimates: Borjas 1993 gets
  0.45 on log earnings, and 0.36 without Mexico, R² dropping from .69 to .18. Card–DiNardo–Estes
  2000 get 0.41–0.43 on schooling and 0.44–0.62 on sons' wages
  [SOURCE: `literature_reads.md` §2a, §3; tables read from NBER working papers].
- **Mexico carries the weighted slope.** It holds 29% of the G2 weight at the far left of the
  distribution. The unweighted and square-root-weighted slopes (0.45–0.48) are the more robust
  central values.
- **Mexico is below the line; the other Hispanic-Caribbean and Central American origins are
  above it.** Guatemala, El Salvador and Honduras have G1 at 18–21, like Mexico's 16. Their G2
  reach 42–48; Mexico's reaches 36. This holds with G2 restricted to 2015–2025 (36.1), so the
  gap is not an older-cohort artifact.
- **Split slopes: point estimates differ; the data cannot distinguish them from linear.** The
  slope is 0.68 below the white median and 0.31 above it. The paired origin bootstrap puts the
  difference at 0.37, with an interval of −0.12 to 0.83 (§6). India shows no regression at all
  from G1 to G2 (73.1 → 72.6) and sits 6 points above the line.

## 3. Selection relative to origin (task 3)

Each G1 adult's schooling is placed in the origin country's distribution for the same birth
cohort. The main source is Barro-Lee v3, the 5-year census point where the cohort is aged about
30–39 (ten-year bands, seven attainment levels; CPS some college and associate degrees count as
"tertiary incomplete"). Where Barro-Lee lacks the country (Nigeria, Lebanon, Samoa), the source
is the Wittgenstein Centre v3 2020 reconstruction (six completed levels)
[SOURCE: github.com/barrolee/BarroLeeDataSet BLData/BL_v3_MF.csv; github.com/guyabel/wcde-data
wcde-v3-batch/2/pop-age-edattain.rds; both pinned by sha256 in `cps_curve.py`]. Of 535,983 G1
adults with schooling, 477,911 are placed.

- Almost every immigrant stream is positively selected on schooling relative to its origin.
  Origin means range from 58.5 (Mexico) and 64.9 (Armenia) to 94.5 (India), 95.8 (Indonesia) and
  96.4 (Uganda). Mexico is the least selected large stream. Its immigrants sit near their own
  country's median: 58.5 in Barro-Lee, 48.2 in WIC 2020.
- **Arrival age matters for the measure.** 28% of pooled G1 (weighted) arrived before 18, and
  their schooling may be US-acquired; for Mexico the share is 31%. 41% arrived at 25 or older,
  classified conservatively over the grouped YRIMMIG intervals; the ones in between belong to
  neither arm. For adult arrivals the within-origin axis predicts their own US position, and it
  predicts G2 only through that position. `[CALCULATION: derived/selection_arms.csv; cps_audit.json arrival_arms]`

| G1 arm | Mexico | origins | selection → G1 US edu, slope (95%), R² | selection → G2 edu, R² | selection → G2 earn, R² | G2 edu ~ G1 US + selection: b_G1US / b_sel | G2 earn ~ same: b_G1US / b_sel |
|---|---|---|---|---|---|---|---|
| all G1 | with | 77 | 1.51 (0.13–1.70), 0.68 | 0.87, 0.72 | 0.38, 0.62 | 0.40 (0.27–0.52) / 0.27 (−0.14 to 0.40) | 0.20 (0.11–0.26) / 0.09 (−0.13 to 0.17) |
| all G1 | without | 76 | 0.62 (−0.02 to 1.36), 0.10 | 0.33, 0.12 | 0.10, 0.03 | 0.34 (0.25–0.45) / 0.12 (−0.19 to 0.35) | 0.16 (0.10–0.23) / −0.00 (−0.19 to 0.12) |
| arrived 25+ | with | 77 | 1.63 (0.67–1.80), 0.75 | 0.84, 0.76 | 0.37, 0.67 | 0.28 (0.16–0.39) / 0.38 (−0.15 to 0.54) | 0.15 (0.09–0.21) / 0.12 (−0.14 to 0.21) |
| arrived 25+ | without | 76 | **1.19 (0.45–1.75), 0.28** | 0.39 (0.08–0.66), 0.18 | 0.15 (0.01–0.29), 0.09 | 0.23 (0.14–0.34) / **0.12 (−0.22 to 0.38)** | 0.13 (0.07–0.20) / −0.00 (−0.17 to 0.14) |
| arrived <18 | with | 74 | 1.33 (−0.21 to 1.65), 0.54 | 0.90, 0.59 | 0.39, 0.50 | 0.56 (0.44–0.66) / 0.16 (−0.08 to 0.32) | 0.26 (0.16–0.32) / 0.05 (−0.12 to 0.14) |
| arrived <18 | without | 73 | 0.08 (−0.27 to 0.68), 0.00 | 0.15, 0.03 | 0.02, 0.00 | 0.50 (0.41–0.61) / 0.11 (−0.15 to 0.30) | 0.21 (0.13–0.29) / 0.01 (−0.15 to 0.11) |

  Origins need ≥50 G1 in the arm. Arm means are age-standardised like the pooled ones; the G2
  side is unchanged.
- **Conclusion after the arrival-age split.** Selection within origin is a real predictor of
  where adult arrivals land in the US. Once that landing point is known, it adds nothing
  distinguishable from zero to G2 outcomes in any arm without Mexico. The pooled-G1 conclusion
  holds for G2. What changes is the G1 link: it was understated because child arrivals, whose
  origin-country rank is not pre-migration schooling, carry no signal.
- The two origin sources disagree most for rich European origins: Germany is 83 in Barro-Lee and
  52 in WIC, Canada 73 and 45. That is a definitional difference: Barro-Lee counts some tertiary
  as attained and WIC counts completed levels. Their disagreement is the size of the measurement
  problem. Feliciano–Lanuza 2017 find the same weak individual-level signal: 0.008 years per
  origin-percentile point with parental years held constant (Table 3, p.226)
  [SOURCE: `literature_reads.md` §5a].

So "how selected" in the operator's sense, meaning how far up the origin country's ladder the
migrants came from, matters through where the adult arrivals land on the US ladder, and that
landing point is what carries to G2. The curve below uses the adult-arrival arm for its first
link.

## 4. G2 → G3 (task 4)

GSS 1977–2024 (46,658 adults 25–64). Generations come from BORN × PARBORN × GRANBORN, origin from
ETHNIC. The reference is white with US-born parents, non-Hispanic, in year × ten-year age cells.
`[CALCULATION: derived/gss_origin_generations.csv, derived/gss_slopes.csv]`

| G3 definition | outcome | link | origins | slope | 95% interval | intercept | reliability of x | without Mexico |
|---|---|---|---|---|---|---|---|---|
| ≥1 grandparent foreign | education | G2→G3 | 20 | **0.72** | 0.23 – 1.06 | 14.6 | 0.72 | 0.56 |
| ≥1 grandparent foreign | education | G1→G2 | 15 | 0.53 | 0.04 – 0.65 | 26.6 | 0.97 | 0.20 |
| ≥1 grandparent foreign | education | G1→G3 | 13 | 0.40 | 0.15 – 0.60 | 34.3 | 0.92 | 0.28 |
| ≥1 grandparent foreign | education | G3→G4+ | 18 | 0.79 | 0.39 – 1.02 | 7.7 | 0.88 | 0.82 |
| ≥1 grandparent foreign | income | G2→G3 | 14 | 0.49 | −0.15 – 0.91 | 26.3 | 0.33 | 0.12 |
| ≥1 grandparent foreign | income | G1→G2 | 11 | 0.54 | 0.15 – 0.65 | 24.6 | 0.89 | 0.39 |
| ≥1 grandparent foreign | income | G1→G3 | 10 | 0.32 | −0.22 – 0.52 | 35.2 | 0.61 | 0.01 |
| ≥1 grandparent foreign | income | G3→G4+ | 17 | 0.62 | 0.07 – 0.96 | 18.4 | 0.19 | 0.42 |
| ≥2 grandparents foreign | education | G2→G3 | 20 | 0.81 | 0.20 – 1.10 | 10.0 | 0.73 | 0.60 |
| ≥2 grandparents foreign | education | G1→G3 | 12 | 0.42 | 0.08 – 0.72 | 33.6 | 0.92 | 0.25 |
| ≥2 grandparents foreign | education | G3→G4+ | 18 | 0.73 | 0.32 – 1.01 | 11.6 | 0.84 | 0.76 |
| ≥2 grandparents foreign | income | G2→G3 | 13 | 0.75 | −0.05 – 1.09 | 13.2 | 0.36 | 0.32 |
| ≥2 grandparents foreign | income | G1→G3 | 10 | 0.45 | −0.35 – 0.73 | 29.0 | 0.63 | 0.09 |
| ≥2 grandparents foreign | income | G3→G4+ | 17 | 0.36 | −0.11 – 0.70 | 32.0 | 0.33 | 0.15 |

The GSS G2 means of the European origins span only 43–65, so the fit leans on Mexico (G2 34, G3
37). The income link is noise: the reliability of the x means is 0.19–0.36. Published
cross-origin figures, read from the papers' tables [SOURCE: `literature_reads.md`]:

| source | link | coefficient |
|---|---|---|
| Borjas 1994 (GSS, Table 8) | G2→G3 mean convergence | log wage ≈ 0.46, education ≈ 0.53 |
| Borjas 1992 (Table V) | G2+→G3+ | education 0.47, NLSY log wage 0.55 |
| Borjas 1994 (Census, Table 6/5) | implied G2→G3 | education 0.47, wages 0.33–0.40 |
| Ward 2020 (App. Table A1) | G2 1910→G3 1940, linked | log occupational score 0.57–0.74 |
| Borjas 1994 / Ward 2020 | G1→G3 direct | 0.20–0.27 wages / 0.25–0.55 |

This lane's GSS G1→G3 education slope of 0.40 (0.15–0.60) sits inside that published range. The
G2→G3 central value to carry forward is **about 0.5**, with a range of 0.46–0.72. Two
origin-specific facts: the sister lane finds that Mexican G2→G3+ carries 85–92% of the gap on
standard data, with no G3→G4+ gain (`generation_carryover_2026_09_27/RESULT.md`). The Indian G3
cell (n 49) is +$11,806 (se 8,150) against a G2 of +$23,692
(`research/immigration-indian-origin-fiscal-coordination-politics-2026-09-18.md`, revision
2026-09-21).

## 5. The curve (task 5)

`[CALCULATION: derived/curve_projection.csv, derived/curve_links.csv; figure derived/selection_curve.png]`

| link | status | slope (95%) | intercept |
|---|---|---|---|
| origin selection → G1 US education, G1 arrived 25+ | measured (R² 0.75; 0.28 without Mexico) | 1.63 (0.74–1.80) | −75.3 |
| G1 → G2 education | measured | 0.52 (0.28–0.59) | 28.7 |
| G1 → G2 earnings | measured | 0.55 (0.17–0.68) | 25.7 |
| G2 → G3 education | [MODEL] GSS cross-origin | 0.72 (0.24–1.01) | 14.6 |
| G2 → G3 education | [MODEL] Borjas rule, 50 + β(p − 50) | 0.46–0.53 | — |

| origin | selection pct | G1 | G2 observed | G2 on the line | G3 [MODEL] GSS (95%) | G3 [MODEL] Borjas |
|---|---|---|---|---|---|---|
| India, education | 94.5 | 73.1 | 72.6 | 66.9 | 67.2 (59.0–72.8) | 60.4–62.0 |
| India, earnings | 94.5 | 57.9 | 60.6 | 57.6 | 55.7 (51.9–60.0) | 54.9–55.6 |
| Mexico, education | 57.9 | 16.4 | 35.7 | 37.3 | 40.4 (35.1–50.2) | 42.4–43.4 |
| Mexico, earnings | 57.9 | 34.4 | 43.4 | 44.7 | 47.4 (43.3–54.5) | 46.5–47.0 |

Rows for China, the Philippines, Vietnam, Nigeria, Korea, Cuba and El Salvador, and the generic
curve at origin-selection 60–95, are in `curve_projection.csv`. G3 is projected from each group's
observed G2. The earnings G3 row applies the noisy GSS income link to CPS wage percentiles.

**Measured:** G1 and G2 positions (CPS) and the cross-origin G1→G2 slope. **Assumed:** that the
cross-origin G2→G3 slope (GSS, mostly European origins observed 1977–2024, plus the literature)
applies to today's Indian and Mexican G2; that ETHNIC identifies G3 origin; and that the relation
is linear in percentile units. The Borjas coefficients are on log wages and years, and applying
them to percentiles is a further assumption. For Mexico the model's G3 of about 40–43 lies above
the observed Mexican G3 (GSS 36.9; CPS third-plus self-identified ≈ G2 in the V02 lane). Ethnic
attrition biases that observed figure down, but the sister lane's attrition bounds do not reach
the modelled convergence. For India there is no observed G3 beyond n = 49.

## 6. Disconfirmation (task 6)

- **Nonlinearity: point estimates differ; the data cannot distinguish them from linear.** The
  test is a paired origin bootstrap with 10,000 draws. Each draw resamples all origins, splits
  them at G1 = 50, and differences the two n-weighted slopes.
  `[CALCULATION: derived/nonlinearity.csv]`

| outcome | Mexico | origins below / above | slope below | slope above | difference (95%) | share of draws ≤ 0 |
|---|---|---|---|---|---|---|
| education | with | 34 / 44 | 0.685 | 0.310 | 0.374 (−0.116 to 0.825) | 0.073 |
| education | without | 33 / 44 | 0.494 | 0.310 | 0.184 (−0.187 to 0.697) | 0.161 |
| earnings | with | 55 / 23 | 0.741 | 0.275 | 0.466 (−0.411 to 1.260) | 0.162 |
| earnings | without | 54 / 23 | 0.506 | 0.275 | 0.231 (−0.519 to 1.097) | 0.272 |

  This reproduces the audit (0.374 [−0.114, 0.829], 0.466 [−0.419, 1.269]); the interval ends
  differ only through the random draws. The low- and high-selection halves (0.54/0.59 vs
  0.37/0.25) were not tested and carry the same caveat.
- **Leave-one-out:** dropping Mexico moves the slope from 0.52 to 0.36 (education) and from 0.55
  to 0.30 (earnings). No other single origin moves it by more than 0.05 (the largest is Canada, to 0.55 and
  0.59; `cps_audit.json` leave_one_out). Dropping Mexico, India, China and the Philippines gives
  0.32 and 0.27.
- **G2 advantage of high-selected groups as a top-tail effect: no for India, partly for China.**
  Capping at the white p99 keeps 93% of India G2's earnings gap and 81% of China G2's. The
  Indian G2 fiscal gap is still +$17,140 excluding persons above the white p99, and +$12,692
  below the white p90 (§1).
- **Cohort mismatch** (today's G1 are not the G2's parents): pairing G1 observed 1994–2004 with G2
  observed 2015–2025 leaves education at 0.54 and raises earnings to 0.68.
- **Mixed parentage:** G2 with both parents foreign-born carry more, 0.64 and 0.71, as expected
  when one parent is a native.

## Files and sources

Covered: IPUMS-CPS ASEC 1994–2025 extract (`cps_2ndgen.csv.gz`, V02 loader rules and estimator
imported unchanged for the gate); the Indian ledger (`indian_ledger_2026_09_18/ledger_india.py`,
imported unchanged via `ledger_dump.py`; CPS ASEC 2025 public zip `318845a2…`, MEPS 2024); GSS
7224 R3a; Barro-Lee v3; WIC v3 SSP2 2020; FRED CPIAUCSL. The literature reads were done by a
researcher sub-agent (claude-opus-5-5), and every number is quoted with its table and page in
`literature_reads.md`: Borjas 1992/1993/1994, Card–DiNardo–Estes 2000, ABJP 2021,
Feliciano–Lanuza 2017, Ward 2020. The sister lane `generation_carryover_2026_09_27` was read for
the Mexican consistency check only.

Skipped, with reasons:
- Feliciano 2005 (fetch failed) and Borjas 2006 (not reached).
- ABJP's origin-level table (Appendix A4, not read); ABJP report individual rank-rank slopes, a
  different object from the group slope.
- The CPS grandparent linkage in `generation_split_2026_09_20`: it is Mexican-only and co-resident
  only, and is covered by the sister lane.
- ACS: not needed, since the CPS cells meet the n rules.

Run from the repository root, in order: `OPENBLAS_NUM_THREADS=1 uv run --no-project --with pyreadr --with matplotlib python3 infra/immigration-fiscal/selection_curve_2026_09_27/<script>.py` for `load`, `cps_curve`, `ledger_dump`, `ledger_tail`, `gss_g3`, `curve`, then `verify` (parent rerun 2026-09-27: every file in `derived/` byte-identical; `cps_curve` needs `pyreadr` and `curve` needs `matplotlib`).

Scripts: `load.py` (frame and sha check) · `cps_curve.py` (tasks 1–3, 6; ~5 min) · `ledger_dump.py`
+ `ledger_tail.py` (fiscal tail) · `gss_g3.py` (task 4) · `curve.py` (task 5 and the PNG) ·
`verify.py` (gates). Outputs are in `derived/`. `_cache/` holds the frame, the ledger dump and the
pinned origin-education files, and is ignored.

Limits: the SEs of origin means ignore household clustering (they are Kish-effective-n
approximations), and the origin-resampling intervals carry the cross-origin uncertainty that
matters for the curve. Earnings are wage and salary only; self-employment is not in the extract,
which understates Korean and other high-self-employment groups. IPUMS counts people born abroad
to American parents as foreign-born, which inflates the G1 counts for Germany and similar origins
slightly.

## Revisions

**2026-09-27 (audit, same day).** Two findings from the team lead, both confirmed in the code and
fixed.

1. The within-origin selection percentile ranked the current schooling of every G1, including
   child arrivals whose schooling may be US-acquired. `yrimmig` was loaded but unused. There are
   now two arrival-age arms, conservative at the grouped YRIMMIG edges: arrived 25+ (41% of
   weighted G1) and arrived before 18 (28%; Mexico 31%). All "how selected" regressions are
   re-fitted on both arms, with and without Mexico (§3 table; `derived/selection_arms.csv`). The
   verdict changes in one respect. Selection predicts adult arrivals' own US position (R² 0.28
   without Mexico, against 0.10 pooled), and it still adds nothing distinguishable from zero to G2
   beyond that position. The curve's first link now uses the 25+ arm (1.63; Mexico 57.9, India
   94.5).
2. "Nonlinearity: yes" was never tested. A 10,000-draw paired origin bootstrap of the
   below-minus-above-median slope difference gives education 0.374 (−0.116 to 0.825) and
   earnings 0.466 (−0.411 to 1.260). Both intervals include zero, so §2 and §6 now read "point
   estimates differ; the data cannot distinguish them from linear" (`derived/nonlinearity.csv`).

`verify.py` adds gate G7 (arms, YRIMMIG parsing, bootstrap draws, audit point estimates). Re-run
exit codes: `cps_curve.py` 0, `curve.py` 0, `gss_g3.py` 0, `verify.py` 0 (ALL PASS; it re-runs
`ledger_tail.py`).

