# Healthcare donor sensitivity, September 19, 2026

This lane compares the existing age × US-birth medical donor model with adult-only age × birth, adult age × birth × education, and age × birth × insurance models. It uses staged CPS ASEC 2025 and MEPS HC-256 (2024). Outputs describe transported healthcare costs for current adult residents. **MEPS birth information here is US/not-US: none of the detailed-origin cost estimates is observed origin-specific spending.**

The public medical cost is positive. `raw` is the same six-payer sum used upstream. `calibrated` is raw plus `(Medicaid ratio−1) × Medicaid + (Medicare ratio−1) × Medicare`, reproducing the annual base-health-plus-M account. Compare these jointly; adding raw and calibrated sensitivity deltas would count the raw change twice. The inherited multipliers (1.5432 and 1.2804) are historical 2012 reconciliation assumptions, not fitted 2024 totals.

## Run

```sh
UV_CACHE_DIR=/private/tmp/immigration-uv-cache OPENBLAS_NUM_THREADS=1 \
  uv run --no-project python3 \
  infra/immigration-fiscal/health_transport_sensitivity_2026_09_19/builder.py \
  --root /Users/alien/Projects/immigration-research

UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project python3 -m pytest -q \
  infra/immigration-fiscal/health_transport_sensitivity_2026_09_19/test_builder.py
```

`--root` supplies read-only canonical code/raw files/parameters. `--out` defaults to this lane's ignored `derived/`. No raw files are changed. `load_outputs(out)` verifies all recorded input and output hashes before reading. Full-data generation checks both the canonical donor assignments/means and its entire raw-outcome covariance against the existing implementation.

## Coding and support

| Target education | CPS A_HGA | MEPS crosswalk |
|---|---|---|
| `lt_hs` | 31–38 | HIDEG=1; EDUCYR=0–12 |
| `hs_only` | 39 | HIDEG=2 (GED) or 3; EDUCYR=0–12 |
| `some_college` | 40–42 | HIDEG=1/2/3; EDUCYR=13–17 |
| `ba_plus` | 43–46 | HIDEG=4/5/6; degree dominates reported years |
| `unknown` | other | HIDEG=7 (other degree), missing or otherwise unmapped |

This is a conservative modeling crosswalk, not a claim of exact questionnaire equivalence. MEPS attainment is measured when entering the panel and is minimally cleaned; CPS attainment is current. HIDEG=7 is not identified as an associate/professional degree. All such records remain in the survey design, but are excluded from education-domain means. Their weighted mass is reported in `audit.json`. [Sources: staged HC-256 codebook pp.114–115 and documentation C-29; CPS ASEC 2025 dictionary 6C-3; official [MEPS HC-256 release](https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-256).]

MEPS BORNUSA=1/2 corresponds to US/not-US; the existing CPS transport uses PENATVTY=57 versus elsewhere, preserving the canonical convention. Origin targets use foreign-born PRCITSHP=4/5 and the explicit birthplace sets in `builder.ORIGIN_CODES`. `all_native` and `third_plus_nh_white` retain the existing CPS definitions. Country sets match the education-account lane's full CPS manual Appendix J.

For under-65 insurance matching, MEPS INSURC24=1/2/3 means any private/public only/uninsured. The canonical CPS match treats PRIV or MIL or CHAMPVA as private-equivalent, then PUB, then uninsured. The MEPS documentation includes TRICARE/CHAMPVA in that summary's private category. All 65+ insurance categories are pooled to preserve the current match. This is annual coverage matching, not insurance at the March interview. [Sources: HC-256 codebook p.472 and insurance-summary documentation; CPS dictionary PUB/PRIV/MIL/CHAMPVA.]

Donor ages retain the canonical bands 0–17/18–34/35–49/50–64/65+. Education donors are restricted to age25+; `adult_age_birth` uses the same age restriction without education, separating the restriction's effect from the education split. CPS results use age25–64 and six adult bands: `0`=25–34, `1`=35–44, `2`=45–54, `3`=55–64, `4`=65–74, `5`=75+.

The prespecified support screen is at least 30 donor records, Kish effective n≥20, and two contributing PSUs. These are analyst screening thresholds, **not AHRQ reliability guarantees**. Cell cost RSEs are reported and can remain large. Direct education/insurance estimates use their supported target subset; comparisons to canonical use exactly that same subset. Named `education_backoff` and `insurance_backoff` scenarios use the richer donor only when supported, otherwise adult-age-birth and canonical donors respectively. Backoff mass is explicit in `target_support.csv`. No unreported fallback is allowed.

## Uncertainty interface

`domain_means_covariance(data, keys, outcomes, valid)` is reusable. Pass the **complete** MEPS frame and a separate domain mask. It returns `cells`, `means[cell,outcome]`, `covariance`, `influence[full_record,j]`, `keys`, `outcomes`. Covariance ordering is cell-major, so `means.reshape(-1)` aligns: cell0/raw, cell0/calibrated, cell1/raw, cell1/calibrated. Any additional outcome such as TRICARE is supported.

Every positive-weight MEPS stratum/PSU is retained, with zero influences outside each domain. The joint matrix includes covariance across raw/calibrated outcomes and across all matching models. CPS uncertainty uses all 160 person SDR replicates and each replicate's own denominator. Reported joint SEs add independent CPS and MEPS sampling variances; transport validity, historical scaling and crosswalk uncertainty are not sampling errors. [AHRQ full-design subgroup guidance](https://meps.ahrq.gov/survey_comp/standard_errors.jsp).

| Artifact | Contract |
|---|---|
| `estimates.csv` | `row`, origin, education, band, model, scope, outcome; population/records; cost and CPS/MEPS/joint SE; delta versus canonical and adult control on the identical target domain |
| `donor_cells.csv` | Model/cell keys, n, Kish ESS, contributing PSUs/strata, support flag, raw/calibrated means/SE/RSE |
| `target_support.csv` | Target population/records, unsupported mass and explicit-backoff status |
| `native_contrasts.csv` | Same-education, same-age healthcare-cost differences versus all-native and third-plus NH-white; correlated sampling SE |
| `covariance_index.csv` | Joint donor parameter index `j` → model, cell, outcome |
| `age_deltas.csv` | Six adult bands; `row`, `estimate_row`, `baseline_row`, model/baseline, group keys, identical CPS count/population, healthcare-cost delta and SE |
| `medical_uncertainty.npz` | `covariance[J,J]`; `donor_means[J]`; `point_gradients[R,J]`; `cps_per_person_replicates[R,161]`; `age_delta_gradients[D,J]`; `age_delta_cps_replicates[D,161]` |

Here R is `len(estimates)`, D is `len(age_deltas)`, and J is `len(covariance_index)`. `row` gives the zero-based array row. CPS column0 is the full-weight estimate. `point_gradients @ donor_means` reconstructs per-person costs. For age weights `w`, form `g = w @ age_delta_gradients[rows]` and `r = w @ age_delta_cps_replicates[rows]`; MEPS variance is `g @ covariance @ g`, CPS variance is `4/160 * sum((r[1:]−r[0])**2)`. Use conditional survival/discount person-years as age weights for a period-profile NPV. **Additional healthcare cost means the fiscal balance changes by its negative.** Do not sum age-specific variances independently.

## Institutional overlap check

The actual M multipliers target **adjusted** NHEA. Bernard et al. Table4 subtracts nursing-home and institutional acute-care expenditure before the Table6 Medicaid/Medicare gap is calculated. Consequently these multipliers do not inherently price institutional N; that add still requires a defensible institutional population/type/payer model. Its removal from the primary account cannot be justified by claiming these particular multipliers are full institutional-inclusive NHEA ratios. [Primary reconciliation, Tables4–6](https://meps.ahrq.gov/data_files/publications/workingpapers/wp_17003.pdf).
