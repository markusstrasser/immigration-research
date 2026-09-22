# MEPS Mexican-origin medical payments against the ledger's donor cells

What the fiscal ledger's health transport does, and what this lane measures against it.

`../build/meps_health_transport_2024.py::donor_model` gives every CPS record the mean
public-payer spending of MEPS donors matched on **age band x US birth** (x insurance status
when the under-65 variant is used). It carries no ethnicity, no income and no Medicaid
dimension. This lane computes, inside the same MEPS HC-256 file, the same-cell ratio of
Mexican-origin public payments to all-donor public payments. A ratio away from 1 is the
direct size of what that transport misses for the Mexican-origin population.

Findings: [RESULT.md](RESULT.md). Companion 65+ check on a Medicare-specific survey:
[`../mcbs_elderly_medical_2026_09_22/RESULT.md`](../mcbs_elderly_medical_2026_09_22/RESULT.md).

## Reproduce

```sh
# from the repository root
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
    infra/immigration-fiscal/meps_mexican_origin_medical_2026_09_22/meps_mexican.py
uv run --no-project python3 -m pytest \
    infra/immigration-fiscal/meps_mexican_origin_medical_2026_09_22/ -q
```

Runtime is about four minutes, most of it the 2,000-replicate bootstrap that validates the
linearized standard error. Nothing is downloaded; every input is already on disk and its
SHA-256 is recorded in `derived/audit.json`.

## Inputs

| File | Role |
|---|---|
| `~/research-data/…/ahrq/meps_2024/h256dat.zip` + `h256su.txt` | MEPS HC-256, 2024 full-year consolidated file and its SAS load statement. Primary; the transport's own year |
| `~/research-data/…/ahrq/meps_2024/h256cb.pdf` | codebook, read with `pdftotext -layout`; every quote below comes from it |
| `~/research-data/…/ahrq/meps/h251dat.zip` + `h251su.txt` | MEPS HC-251, 2023, for the secondary pooled 65+ check only |
| `~/research-data/…/fred/cpi_all_urban.csv` | CPI-U (CPIAUCSL) monthly, annual means, to deflate 2023 dollars in the pooled check |
| `../ledger_absolute_2026_09_17/derived/age_profile_components.csv` | the union's `medical` and `M` charges by band, `allocation=shared`, `account=expanded` |
| `../ledger_absolute_2026_09_17/derived/age_profiles.csv` | band populations for `mexican_observed_total`, `mexico_born`, `mexican_second_gen`, `mexican_third_plus_selfid` |
| `../ledger_absolute_2026_09_17/params/params.json` | `meps_coverage.nhea_to_meps_ratio_medicaid` 1.5432 and `…_medicare` 1.2804, the fixed coefficients inside item `M` |

## Variable map, with codebook quotes

Fixed-width positions come from `h256su.txt`; the parser is copied from
`../build/public_mvp_io.py::parse_meps_sas_fields`.

| Variable | Start | Codebook line |
|---|---|---|
| `AGE24X` | 192 | `AGE AS OF 12/31/24 (EDITED/IMPUTED)`; `-1 INAPPLICABLE 161 2,998,984` |
| `RACEV1X` | 203 | `RACE (EDITED/IMPUTED)`; `1 WHITE - NO OTHER RACE REPORTED 14,459 252,364,775` |
| `RACETHX` | 209 | `RACE/ETHNICITY (EDITED/IMPUTED)`; `2 NON-HISPANIC WHITE ONLY 10,766 191,692,001` |
| `HISPANX` | 210 | `HISPANIC ETHNICITY (EDITED/IMPUTED)`; `1 HISPANIC 4,116 68,605,583` / `2 NOT HISPANIC 15,024 271,192,047` |
| `HISPNCAT` | 211 | `1 MEXICAN/MEX AMER/CHICANO - NO OTHER HISP RPTD 2,679 42,446,768` … `9 NON-HISPANIC 15,024 271,192,047` |
| `BORNUSA` | 278 | `PERSON BORN IN THE US`; `1 YES 16,002 285,498,519` / `2 NO 3,050 52,835,316` |
| `YRSINUS` | 280 | `YEARS PERSON LIVED IN THE US`; `-1 INAPPLICABLE 16,090 286,962,313` … `5 15 YEARS OR MORE 2,001 33,246,175` |
| `MCREV24` | 2798 | `EVER HAVE MEDICARE DURING 2024 (ED)`; `1 YES 5,469 70,105,211` |
| `MCDEV24` | 2799 | `EVER HAVE MCAID/SCHIP DURING 2024 (ED)`; `1 YES 4,941 78,147,553` / `2 NO 14,199 261,650,077` |
| `INSURC24` | 2806 | `FULL YEAR INSURANCE COVERAGE STATUS 2024`; `1 <65 ANY PRIVATE` … `4 65+ EDITED MEDICARE ONLY` |
| `TOTEXP24` | 3195 | `TOTAL HEALTH CARE EXP 24` |
| `TOTSLF24` | 3202 | `TOTAL AMT PAID BY SELF/FAMILY 24` |
| `TOTMCR24` | 3208 | `TOTAL AMT PAID BY MEDICARE 24` |
| `TOTMCD24` | 3214 | `TOTAL AMT PAID BY MEDICAID 24` |
| `TOTPRV24` | 3221 | `TOTAL AMT PAID BY PRIVATE INS 24` |
| `TOTVA24` | 3227 | `TOTAL AMT PAID BY VA/CHAMPVA 24` |
| `TOTTRI24` | 3233 | `TOTAL AMT PAID BY TRICARE 24` |
| `TOTOFD24` | 3239 | `TOTAL AMT PAID BY OTHER FEDERAL 24` |
| `TOTSTL24` | 3244 | `TOTAL AMT PAID BY OTH ST/LOCAL 24` |
| `PERWT24F` | 4599 | `FINAL PERSON WEIGHT, 2024`; `0.000000 457` / `776.278855 - 91256.761356 18,683` |
| `VARSTR` | 4635 | `VARIANCE ESTIMATION STRATUM, 2024`; `2001 - 2117 19,140` |
| `VARPSU` | 4639 | `VARIANCE ESTIMATION PSU, 2024`; `1-7 19,140` |

**public** = `TOTMCR24 + TOTMCD24 + TOTVA24 + TOTTRI24 + TOTOFD24 + TOTSTL24`, the
transport's own `PUBLIC_PAYERS` list, unchanged.

## Groups

| Name | Definition |
|---|---|
| `mexican_origin` | `HISPNCAT == 1`, self-reported Mexican / Mexican American / Chicano with no other Hispanic origin reported |
| `nh_white` | `HISPANX == 2` and `RACEV1X == 1`. A gate checks this reproduces `RACETHX == 2` exactly, 10,766 records and 191,692,001 people |
| `all_donors` | the transport's valid set: `PERWT24F > 0`, `AGE24X >= 0`, `BORNUSA in (1, 2)` |

## Bands

Both formulas are copied verbatim and a test fails if either source file changes.

- **transport bands** `np.digitize(age, [18, 35, 50, 65])` → `0-17, 18-34, 35-49, 50-64, 65+`,
  from `../build/meps_health_transport_2024.py::age_band`. These are the donor cells.
- **ledger bands** `np.digitize(age, [18, 25, 35, 45, 55, 65, 75])` → eight bands, from
  `../ledger_absolute_2026_09_17/profile_export.py` line 80. These are the bands
  `age_profile_components.csv` is keyed on, so the translation runs on them.

## Gates, all fail-loud

1. 19,140 records; 18,683 with `PERWT24F > 0`.
2. All eight `HISPNCAT` categories reproduce the codebook exactly, unweighted and weighted.
3. The transport's two nativity anchors reproduce to the dollar: 285,498,519 and 52,835,316.
4. `nh_white` reproduces `RACETHX == 2` exactly.
5. `VARSTR` in 2001-2117 and `VARPSU` in 1-7 on every record, no missing, and no stratum
   with a single PSU among positive-weight records (105 strata, 264 PSUs, minimum 2).
6. No negative or reserved public-payer value; nothing is silently replaced by zero.
7. `MCDEV24` reproduces 4,941 / 78,147,553.

## Estimator

Weighted means, then the **with-replacement stratified-PSU Taylor linearization** the
transport already uses in `donor_model`:

```
z_i = w_i (y_i - theta) / W        for i in the domain, 0 outside
V   = sum_h  n_h/(n_h - 1)  sum_a (z_ha - zbar_h)^2
```

where `z_ha` sums the influence values of PSU `a` in stratum `h`. Ratios are formed as
`z_i^R = (z_i^num - R z_i^den) / theta_den`, so the numerator and denominator stay correlated
through the shared PSUs; the same composition handles the nativity-mixed and
coverage-standardized estimates. 95% intervals are `ratio +/- 1.96 x SE`.

**Validation.** The 65+ Mexican-origin/all-donor public ratio was recomputed with a
Rao-Wu(n_h - 1) rescaling bootstrap over PSUs within strata, 2,000 replicates: linearized SE
**0.1446**, bootstrap SE **0.1473**, 1.9% apart. Both are in `derived/audit.json` under
`se_validation`. The lane exits non-zero if they disagree by more than 20%.

## Outputs

| File | Contents |
|---|---|
| `derived/cells.csv` | 171 domain x group rows: transport cells, ledger bands, pooled age domains and Medicaid-coverage strata, each by nativity, with weighted means and SEs for public, Medicare, Medicaid, out-of-pocket, private and all-source payments, plus the share ever Medicaid-covered |
| `derived/ratios.csv` | 810 rows: Mexican-origin over `nh_white` and over `all_donors` for every domain and measure, with linearized SE, 95% interval, an excludes-one flag, the absolute difference, and the coverage-standardized rows carrying `pooled_ratio` and `coverage_composition_part` |
| `derived/ledger_translation.csv` | the eight ledger bands plus a 65+ and an all-bands row: the union's own charges, the nativity-mixed ratio, the implied change in $bn with a delta-method SE, and a leave-one-out column |
| `derived/audit.json` | input SHA-256s, every gate's reproduced value, all codebook quotes, the band-formula provenance, the SE validation, the leave-one-out record, the NHEA coefficients and the pooled two-year check |

## The translation, and what it assumes

`age_profile_components.csv` carries no nativity split for `mexican_observed_total`, so each
band's foreign-born share comes from `age_profiles.csv` as
`population(mexico_born) / population(mexican_observed_total)`. A gate checks that
`mexico_born + mexican_second_gen + mexican_third_plus_selfid` equals the union exactly in
every band, which it does. Each band's MEPS ratio is then the nativity-mixed Mexican-origin
mean over the nativity-mixed all-donor mean, and the band's charge is multiplied by it.

Item `M` is a fixed linear form in the Medicaid and Medicare donor means,
`mcd (r_mcd - 1) + mcr (r_mcr - 1)` with `r_mcd = 1.5432` and `r_mcr = 1.2804`, so it is
rescaled with the payer-specific ratios rather than the combined public one.

This is a **translation, not a re-estimate of the ledger**. It answers: if the union's members
in a band spend like MEPS Mexican-origin donors in that band rather than like all donors in
that band, how much does the charge move? It does not re-run the ledger, does not touch the
CPS side, and does not change any committed number.
