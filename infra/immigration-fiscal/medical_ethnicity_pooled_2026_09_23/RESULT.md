**Verdict:** Pooling nine MEPS years (2016–2024, 37,213 Mexican-origin donor person-years) settles
what the 2024 file could not. In total, the ethnicity dimension does not add public medical cost to
the group. It moves cost from adults to children and from Medicare to Medicaid.

Inside the transport's own cells, weighted by the union's cost in each, Mexican-origin people draw:
- **1.38× the cell mean as children** (SE 0.27), or 1.16× (SE 0.06) winsorized at p99.5;
- **0.92× at 18–64** (SE 0.06);
- **0.88× at 65+** (SE 0.07);
- **1.00× over all ages** (SE 0.08), or 0.98× (SE 0.04) winsorized.

[CALCULATION: `translate.py`; DATA: `derived/translation_ledger.csv`, medical+M `implied_ratio`]

**The 2024 lane's 0.69 at 18–64 compares whole age domains, not transport cells.** Pooled, the
domain ratio is 0.671 (SE 0.039). Most of that gap comes from the group's younger age mix and
nativity mix inside 18–64, and the transport's cells already hold those fixed.
[CALCULATION: `derived/ratios.csv`]

**Ledger.** On the ledger's $128.0bn public medical charge (medical + M), the correction is
**+$0.15bn (SE 10.4) plain** and **−$2.7bn (SE 5.4) winsorized**. Across all seven specifications
it runs from −$5.5bn to +$3.5bn, and none differs from zero. [DATA: `derived/translation_ledger.csv`]

**Account.** In the complete account the same ratios move money between lines
[DATA: `derived/translation_account.csv`]:

| Line | Winsorized change $bn (SE) | Range across specifications $bn |
|---|---|---|
| Medicaid/CHIP/other medical ($116.91bn) | +13.6 (6.3) | +12.2 to +21.3 |
| Medicare ($63.96bn) | −9.9 (3.2) | |
| Health services | −5.7 | |
| All five medical lines ($207.43bn) | −3.0 (8.0) | |

**Nursing facilities.** Separately, the account's community key charges the group **$8.4bn of
nursing-facility Medicaid**. The group's share of institutional residents supports only
**$2.2–4.4bn**. With that corrected, the five medical lines fall **$8.0–10.2bn (SE 7.6)**
winsorized, and move between −$12.9bn and +$2.5bn across specifications.
[CALCULATION: `bounds.py`; DATA: `derived/bounds.csv`]

**The case that the group draws more fails at adult ages.** Every specification's 95% interval
rules out an excess above about 7% at 18–64 ($4bn) and 5% at 65+ ($2bn). [CALCULATION: section 8]
- At 65+, 30% of Mexican-origin people have Medicaid, against 12% of all donors. But over all
  ages, a covered Mexican-origin person draws 0.69 of the average covered person's Medicaid dollars.
- Uninsured Mexican-origin adults draw less public money than the average uninsured adult.
- The emergency Medicaid that MEPS does not record adds at most **$0.3–0.9bn** in FY2023. If every
  dollar of it were the group's, it would add $3.0bn.

[DATA: `derived/disconfirmation.csv`, `derived/coverage_vs_dollars.csv`, `derived/bounds.csv`]

The pooled data therefore contradict the +$68.7bn coverage-key stress test.

**One conflict stays open.** On MCBS's definitions, MEPS gives 1.005 pooled and 0.845 in 2023.
MCBS 2023 gives 1.265, so the gaps are z ≈ 1.6 and z ≈ 2.4. If MCBS is right, the 65+ ledger
change is about +$4.8bn rather than −$5.2bn. [INFERENCE: section 7]

## Estimand and sign convention

- **Ratio.** The ratio is a weighted mean payment for Mexican-origin donors (`HISPNCAT == 1`) divided
  by the weighted mean for all valid donors in the same cell.
  - Valid donors are the transport's own set: `PERWT > 0`, `AGE >= 0`, `BORNUSA` in {1, 2}.
  - Transport cells are 0–17, 18–34, 35–49, 50–64 and 65+, each split into US-born and born
    abroad. `donor_model(medical, d, False)` in `ledger_absolute_2026_09_17/absolute_ledger.py`
    matches on these.
  - Dollars are 2024 dollars, deflated by the BLS CPI-U Medical care index (CUUR0000SAM, US city
    average, not seasonally adjusted, annual average). Factors to 2024 run from 1.216 (2016) to
    1.027 (2023). [DATA: `derived/pool_audit.json` `deflators`]
- **Public payments.** Public = Medicare + Medicaid + VA + TRICARE + other federal + state/local,
  which is the transport's list.
  - In 2016–2018 it also includes `TOTOPU`: Medicaid payments for people who did not report
    Medicaid enrollment. MEPS kept these in a separate column until 2018 and inside `TOTMCD` from
    2019. [SOURCE: `h192doc.pdf` p. C-111; `h216doc.pdf` p. C-105]
  - Harmonized Medicaid = `TOTMCD + TOTOPU`. `TOTOPU` was 3.5%, 1.4% and 0.8% of Medicaid dollars
    in 2016, 2017 and 2018. [DATA: `derived/gates_by_year.csv`]
- **Weights and variance.**
  - Pooled weights are `PERWT / 9`.
  - Variance is with-replacement stratified-PSU Taylor linearization on HC-036's `STRA9624` and
    `PSU9624`, so people who appear in two or more years share their PSU.
  - Each estimate carries its PSU influence vector. Ratios, cell-weighted sums and dollar totals
    therefore get exact linearized SEs. [CALCULATION: `design.py`]
- **Dollar sign convention.** Changes are corrected cost minus current cost, so **positive means
  the ledger or account should charge the group more**. The ledger books costs as negatives, so
  +$1bn here is −$1bn in the ledger's net.

## 1. Inputs and gates

**Inputs.** Nine full-year consolidated files and HC-036 are pinned: HC-192, 201, 209, 216, 224,
233, 243, 251 and 256, plus the 1996–2024 pooled linkage file `h36u24`.
- 2016–2022 and HC-036 were fetched from the links on AHRQ's own download pages.
- HC-251 and HC-256 were hashed in place under `~/research-data/.../ahrq/meps{,_2024}/`.
- `derived/inputs_manifest.json` records the URL, size and SHA-256 of all 40 files. [DATA]

**Year gates** [DATA: `derived/gates_by_year.csv`, `derived/pool_audit.json` `years`]:
- In every year, every `HISPNCAT` codebook category (1–6, 8, 9) reproduces both unweighted and
  weighted.
- Code 1 reads "MEXICAN/MEX AMER/CHICANO" with no other Hispanic group reported. The wording varies
  in two versions.
- `BORNUSA` reproduces, and `RACETHX == 2` reproduces the codebook's non-Hispanic white count.
- `TOTEXP` equals the sum of its payer columns within $5 per person.

| Year | File | Records | Mexican-origin n | Weighted (M) | Max TOTEXP residual | OPU share of Medicaid | CPI medical factor |
|---|---|---|---|---|---|---|---|
| 2016 | HC-192 | 34,655 | 6,957 | 35.1 | $4 | 3.5% | 1.216 |
| 2017 | HC-201 | 31,880 | 5,644 | 35.2 | $4 | 1.4% | 1.186 |
| 2018 | HC-209 | 30,461 | 4,786 | 37.2 | $4 | 0.8% | 1.163 |
| 2019 | HC-216 | 28,512 | 4,230 | 37.0 | $5 | 0 | 1.131 |
| **2020** | HC-224 | 27,805 | 4,394 | 37.8 | $4 | 0 | 1.087 |
| **2021** | HC-233 | 28,336 | 4,325 | 37.8 | $4 | 0 | 1.073 |
| 2022 | HC-243 | 22,431 | 3,071 | 39.8 | $4 | 0 | 1.032 |
| 2023 | HC-251 | 18,919 | 2,766 | 42.0 | $4 | 0 | 1.027 |
| 2024 | HC-256 | 19,140 | 2,679 | 42.4 | $3 | 0 | 1.000 |

**HC-036 linkage** [DATA: `derived/pool_audit.json` `hc036_gates`, `pooled_design`]:
- All 242,139 person-years match on DUPERSID + PANEL.
- In-year flag counts equal the HC-036 codebook. Panel 22's 14,630 people carry an 8-character ID
  in 2017 and a 10-character ID in 2018; restricted to each year's ID format, the counts equal
  that year's records. Both IDs sit in the same (stratum, PSU) cell.
- The pooled design has 282 strata and 779 PSUs, with 2 to 8 PSUs per stratum.
- There are 144,756 unique people, 69,992 of them in more than one year.
- The pool holds 231,771 valid donor person-years, 37,213 of them Mexican-origin.

**Gate 1: the 2024 lane reproduces exactly.** From HC-256 alone, the code reproduces all 51
public-payment ratios and SEs that `meps_mexican_origin_medical_2026_09_22` published, with a
maximum absolute difference of 4.4e-16. That lane's figures are 0.688 (SE 0.095) at 18–64,
0.893 (0.145) at 65+ and 0.757 over all ages.
[CALCULATION: `pooled_ratios.py` `gate_2024`; DATA: `derived/ratios_audit.json`]

**Gate 2.** That lane's 2023+2024 pooled check at 65+ also reproduces: 0.810 (SE 0.090), with 558
Mexican-origin and 9,336 donor records. [DATA: `derived/ratios_audit.json` `gate_2023_2024`]

**Gate 3: the accounts' own charges reproduce before any ratio touches them.**
[CALCULATION: `translate.py`; DATA: `derived/translation_audit.json` `gates`]
- The CPS ASEC 2025 archive is SHA-pinned, and its canonical target population is gated at
  40,896,574.15.
- The ledger's union `medical` (−$92.878bn) and `M` (−$35.150bn) reproduce in all eight ledger
  bands. The worst residual is $0.00002.
- The account's five medical keys reproduce `incidence_keys.csv`, national and target, to 1e-9.
- The five line amounts equal `allocations.csv`, scenario `complete_preferred_F_per_capita`.

**Standard errors are validated.** A Rao-Wu (n_h − 1) PSU bootstrap on the HC-036 design, with
1,000 replicates and seed 20260923, gives these results. [CALCULATION: `validate_se.py`;
DATA: `derived/se_validation.csv`]

| Quantity | Estimate | Linearized SE | Bootstrap SE | Apart |
|---|---|---|---|---|
| 65+ public ratio, plain | 0.848 | 0.0668 | 0.0649 | 2.8% |
| Account Medicaid-line change $bn, p99.5 | +13.64 | 6.309 | 6.290 | 0.3% |
| Ledger medical+M change $bn, plain | +0.15 | 10.42 | 10.60 | 1.7% |

## 2. Ratios by transport cell

**Public payments, Mexican-origin / all donors, pooled 2016–2024, with SEs.**
- p99.5 and p99.9 winsorize every donor's payment at the weighted 99.5th or 99.9th percentile of
  all valid donors in the same cell, in 2024 dollars. [DATA: `derived/winsor_caps.csv`]
- The two-part log-normal ratio is (share with any payment) × (ratio of geometric means among
  payers), which is a common-smearing log-normal model that the tail cannot move.
- The two-part arithmetic version is identical to the plain ratio.

[CALCULATION: `pooled_ratios.py`; DATA: `derived/ratios.csv`, `derived/two_part.csv`]

| Band | Born | n Mexican-origin / all donors | Plain | p99.5 | p99.9 | Two-part log-normal | Excl. 2020–21 |
|---|---|---|---|---|---|---|---|
| 0–17 | US | 12,007 / 50,220 | 1.363 (0.265) | 1.151 (0.063) | 1.136 (0.074) | 1.234 (0.055) | 1.430 (0.315) |
| 0–17 | abroad | 384 / 2,083 | 1.359 (0.412) | 1.121 (0.261) | 1.171 (0.291) | 1.353 (0.328) | 1.203 (0.261) |
| 18–34 | US | 6,461 / 37,094 | 0.906 (0.120) | 0.996 (0.079) | 1.000 (0.094) | 0.956 (0.075) | 0.838 (0.087) |
| 18–34 | abroad | 2,483 / 7,593 | 1.251 (0.149) | 1.237 (0.130) | 1.256 (0.137) | 1.166 (0.149) | 1.271 (0.172) |
| 35–49 | US | 2,733 / 30,101 | 0.695 (0.080) | 0.773 (0.082) | 0.726 (0.081) | 0.728 (0.100) | 0.722 (0.091) |
| 35–49 | abroad | 4,825 / 12,703 | 1.071 (0.134) | 1.066 (0.091) | 1.100 (0.116) | 1.002 (0.092) | 0.928 (0.117) |
| 50–64 | US | 1,784 / 34,731 | 0.921 (0.152) | 0.898 (0.124) | 0.922 (0.142) | 0.852 (0.141) | 0.971 (0.171) |
| 50–64 | abroad | 3,503 / 10,607 | 0.929 (0.136) | 0.955 (0.116) | 0.975 (0.132) | 0.890 (0.110) | 0.986 (0.154) |
| 65+ | US | 1,351 / 39,404 | 0.914 (0.089) | 0.926 (0.087) | 0.922 (0.088) | 0.896 (0.082) | 0.978 (0.097) |
| 65+ | abroad | 1,682 / 7,235 | 0.847 (0.078) | 0.861 (0.078) | 0.853 (0.078) | 0.787 (0.082) | 0.857 (0.078) |

**What the cells show.**
- **US-born children** sit above 1 in every estimator. Their interval excludes 1 at p99.5 and in
  the two-part model.
- **US-born 35–49-year-olds** sit below 1 in every estimator, and their interval excludes 1 in
  all of them.
- **Both 65+ cells** sit below 1 in every estimator (0.79–0.98). The foreign-born 65+ interval
  excludes 1 only in the two-part model.
- **Foreign-born 18–34-year-olds** sit above 1 in every estimator (1.17–1.27), without
  significance.
- The remaining cells straddle 1.
- No flat multiplier fits the cells.

[DATA: `derived/ratios.csv` and `derived/two_part.csv`, column `excludes_one`]

Per-cell values for the CPI all-items and year-normalized samples are in `derived/ratios.csv`
(samples `pooled_cpi_all_items` and `pooled_year_normalized`). The eight ledger bands (18–24 …
75+), which the medical transport does not use, are there under `scheme == "ledger"`. [DATA]

**By payer: plain; p99.5.** [DATA: `derived/ratios.csv`]

| Band | Born | Medicare | Medicaid | Other public (VA, TRICARE, other federal, state/local) |
|---|---|---|---|---|
| 0–17 | US | 0.976 (0.453); 1.097 (0.180) | 1.406 (0.287); 1.178 (0.066) | 0.899 (0.269); 0.680 (0.151) |
| 0–17 | abroad | 1.274 (1.020); 1.274 (1.020) | 1.572 (0.480); 1.311 (0.316) | 0.143 (0.076); 0.184 (0.084) |
| 18–34 | US | 0.352 (0.129); 0.407 (0.117) | 0.972 (0.147); 1.065 (0.089) | 0.776 (0.155); 0.773 (0.117) |
| 18–34 | abroad | 0.532 (0.393); 0.521 (0.190) | 1.318 (0.177); 1.317 (0.152) | 0.939 (0.350); 0.756 (0.216) |
| 35–49 | US | 0.489 (0.104); 0.658 (0.128) | 0.773 (0.115); 0.886 (0.129) | 0.816 (0.269); 0.674 (0.130) |
| 35–49 | abroad | 0.290 (0.172); 0.358 (0.069) | 1.138 (0.160); 1.100 (0.101) | 1.272 (0.311); 1.056 (0.146) |
| 50–64 | US | 0.612 (0.120); 0.622 (0.103) | 1.368 (0.311); 1.255 (0.214) | 0.791 (0.234); 0.860 (0.208) |
| 50–64 | abroad | 1.074 (0.280); 0.994 (0.169) | 0.935 (0.152); 0.992 (0.126) | 0.487 (0.175); 0.534 (0.102) |
| 65+ | US | 0.860 (0.085); 0.867 (0.081) | 1.784 (0.568); 2.159 (0.635) | 1.055 (0.226); 1.151 (0.220) |
| 65+ | abroad | 0.846 (0.073); 0.871 (0.071) | 0.938 (0.182); 0.984 (0.189) | 0.380 (0.121); 0.429 (0.129) |

**Union-weighted cell ratio.** This is the ratio the dollars below actually use: each cell's ratio
weighted by the union's current charge in that cell, for medical + M.
[CALCULATION: `translate.py`; DATA: `derived/translation_ledger.csv` `implied_ratio`; SE =
`se_bn / ledger_cost_bn`]

| Age | Plain | p99.5 | p99.9 | Two-part | Excl. 2020–21 | CPI all items | Year-normalized |
|---|---|---|---|---|---|---|---|
| 0–17 | 1.378 (0.270) | 1.160 (0.062) | 1.144 (0.075) | 1.250 (0.055) | 1.445 (0.322) | 1.362 (0.257) | 1.334 (0.235) |
| 18–64 | 0.916 (0.061) | 0.955 (0.051) | 0.962 (0.056) | 0.903 (0.059) | 0.916 (0.067) | 0.914 (0.060) | 0.917 (0.060) |
| 65+ | 0.881 (0.070) | 0.899 (0.070) | 0.888 (0.070) | 0.849 (0.071) | 0.915 (0.069) | 0.881 (0.069) | 0.880 (0.068) |
| All ages | 1.001 (0.081) | 0.979 (0.042) | 0.975 (0.044) | 0.957 (0.045) | 1.027 (0.093) | 0.997 (0.078) | 0.992 (0.074) |
| All ages, US-born | 1.042 (0.110) | 1.000 (0.044) | 0.990 (0.047) | 1.001 (0.046) | 1.074 (0.129) | 1.035 (0.106) | 1.026 (0.098) |
| All ages, born abroad | 0.928 (0.069) | 0.940 (0.065) | 0.949 (0.069) | 0.879 (0.069) | 0.942 (0.073) | 0.928 (0.069) | 0.930 (0.068) |

**Age domains, all seven specifications.** This is the 2024 lane's estimand; it does not hold age
and nativity fixed within the domain. [DATA: `derived/ratios.csv`, `derived/two_part.csv`]

| Age | Plain | p99.5 | p99.9 | Two-part log-normal | Excl. 2020–21 | CPI all items | Year-normalized |
|---|---|---|---|---|---|---|---|
| 0–17 | 1.367 (0.262) | 1.154 (0.062) | 1.140 (0.074) | 1.240 (0.055) | 1.431 (0.312) | 1.352 (0.250) | 1.327 (0.231) |
| 18–64 | 0.671 (0.039) | 0.669 (0.034) | 0.688 (0.037) | 0.668 (0.041) | 0.678 (0.043) | 0.668 (0.038) | 0.667 (0.038) |
| 65+ | 0.848 (0.067) | 0.865 (0.067) | 0.856 (0.067) | 0.759 (0.064) | 0.885 (0.067) | 0.847 (0.066) | 0.846 (0.064) |
| All ages | 0.571 (0.050) | 0.530 (0.029) | 0.545 (0.029) | 0.498 (0.025) | 0.592 (0.059) | 0.569 (0.048) | 0.565 (0.046) |

**Why the domain and cell figures differ at 18–64 (0.671 against 0.916).**
- Mexican-origin adults are concentrated in the younger adult bands, where public spending is
  lowest.
- Foreign-born Mexican-origin adults are compared with all foreign-born donors, who draw little
  public money, and against that comparison they sit above 1.
- The domain ratio mixes both effects into one number; the transport's cells separate them.
  [CALCULATION]

**Age domains by payer: plain; p99.5.** The last column is the plain public ratio against
non-Hispanic whites. [DATA: `derived/ratios.csv`]

| Age | Medicare | Medicaid | Other public | Public, vs NH white |
|---|---|---|---|---|
| 0–17 | 0.983 (0.455); 1.101 (0.177) | 1.413 (0.285); 1.184 (0.066) | 0.877 (0.262); 0.656 (0.145) | 1.617 (0.411) |
| 18–64 | 0.378 (0.051); 0.337 (0.037) | 0.891 (0.067); 0.904 (0.054) | 0.558 (0.075); 0.494 (0.049) | 0.680 (0.044) |
| 65+ | 0.793 (0.055); 0.808 (0.055) | 1.895 (0.390); 2.190 (0.438) | 0.659 (0.130); 0.721 (0.130) | 0.843 (0.069) |
| All ages | 0.325 (0.028); 0.320 (0.028) | 1.149 (0.140); 1.088 (0.055) | 0.470 (0.052); 0.410 (0.035) | 0.505 (0.047) |

**Outside public payers, plain, all donors as reference** [DATA: `derived/ratios.csv`]:
- Out-of-pocket payments are 0.47–0.51× in each age domain (0.43× over all ages).
- Private insurance payments are 0.43–0.49× in each age domain.
- Spending from all sources is 0.76× under 18, 0.55× at 18–64 and 0.74× at 65+.
- At 65+, Medicaid dollars are 3.33× (SE 0.77) those of non-Hispanic whites and Medicaid coverage is
  4.7× theirs. That is the pattern the 2024 lane and MCBS both found.
- Other measures in the file: the transport's unharmonized public list (`public_transport`),
  Medicaid as reported (`TOTMCD` alone), VA, TRICARE, and other federal plus state/local.
  Harmonization (adding `TOTOPU`) moves the public ratio by at most 0.018 in any transport cell and
  0.004 in the three age domains.

## 3. Year-by-year stability, 2020–21 flagged

Each year is estimated alone with its own `VARSTR`/`VARPSU` design. The p99.5 rows apply the pooled
caps, in 2024 dollars. The last column is Cochran's Q across the nine years, with its p-value.
[CALCULATION: `pooled_ratios.py` `by_year`, `heterogeneity`; DATA: `derived/by_year.csv`,
`derived/year_heterogeneity.csv`]

| Age, estimator | 2016 | 2017 | 2018 | 2019 | **2020** | **2021** | 2022 | 2023 | 2024 | Q (df 8), p |
|---|---|---|---|---|---|---|---|---|---|---|
| 0–17 plain | 1.04 (0.15) | 0.99 (0.20) | 1.35 (0.15) | 1.16 (0.18) | 0.98 (0.14) | 1.17 (0.20) | 0.98 (0.14) | 1.39 (0.30) | 2.43 (0.94) | 7.7, 0.468 |
| 18–64 plain | 0.68 (0.09) | 0.80 (0.08) | 0.57 (0.07) | 0.52 (0.06) | 0.77 (0.14) | 0.53 (0.08) | 0.61 (0.08) | 0.84 (0.15) | 0.69 (0.09) | 13.6, 0.094 |
| 65+ plain | 0.95 (0.11) | 0.84 (0.12) | 1.03 (0.13) | 1.09 (0.15) | 0.78 (0.13) | 0.67 (0.09) | 0.74 (0.11) | 0.72 (0.11) | 0.89 (0.14) | 11.9, 0.157 |
| 0–17 p99.5 | 0.96 (0.09) | 1.16 (0.13) | 1.27 (0.10) | 1.18 (0.12) | 1.14 (0.13) | 1.16 (0.14) | 0.98 (0.14) | 1.21 (0.18) | 1.27 (0.19) | 7.7, 0.467 |
| 18–64 p99.5 | 0.66 (0.08) | 0.75 (0.07) | 0.62 (0.07) | 0.53 (0.06) | 0.64 (0.09) | 0.56 (0.07) | 0.66 (0.07) | 0.78 (0.11) | 0.77 (0.09) | 10.9, 0.209 |
| 65+ p99.5 | 0.93 (0.10) | 0.85 (0.12) | 1.03 (0.12) | 1.06 (0.12) | 0.80 (0.13) | 0.72 (0.09) | 0.77 (0.11) | 0.76 (0.11) | 0.93 (0.15) | 9.4, 0.310 |

**Heterogeneity p-values by payer (plain / p99.5)**:

| Age | Public | Medicare | Medicaid | Other public |
|---|---|---|---|---|
| 0–17 | 0.468 / 0.467 | 0.016 / 0.346 | 0.275 / 0.319 | 0.068 / 0.243 |
| 18–64 | 0.094 / 0.209 | 0.000 / 0.001 | 0.217 / 0.855 | 0.087 / 0.177 |
| 65+ | 0.157 / 0.310 | 0.078 / 0.171 | 0.711 / 0.987 | 0.070 / 0.071 |

**The public ratio is stable across years in every age domain.**
- The 2024 child figure of 2.43 is the outlier year. In that year one child record carried 68% of
  the Mexican-origin mean. [DATA: `meps_mexican_origin_medical_2026_09_22/derived/audit.json`
  `leave_one_out`] Winsorized, the child ratio holds between 0.96 and 1.27 in every year.
- Heterogeneity is significant at p < 0.01 in these places:
  - Medicare at 18–64 (Q 31.0, p 0.0001), with 2020 at 0.25 and 2021 at 0.14;
  - Medicare in the 50–64 cell (p 0.0001);
  - other public payers over all ages (p 0.001);
  - the 384-person foreign-born child cell, whose public ratio swings from 0.09 in 2020 to 2.94
    in 2021.

  [DATA: `derived/year_heterogeneity.csv`]
- **2020 and 2021** stand out only through Medicare. The 65+ ratio dips to 0.78 and 0.67 in those
  years, but it is also low in 2022–23, and Q does not reject stability.
- The pandemic years are not what drives the pooled result. Dropping 2020–21 moves 65+ from 0.848
  to 0.885, 18–64 from 0.671 to 0.678, and children from 1.37 to 1.43. [DATA: `derived/ratios.csv`]
- Consecutive years share panel members, so the year estimates are positively correlated. Q
  treats them as independent, which makes it conservative: real heterogeneity may be somewhat
  larger than these p-values suggest. [INFERENCE]

## 4. What drives the ratios

**Two-part decomposition, public payments, age domains** [DATA: `derived/two_part.csv`]:

| Age | Share with any public payment, Mexican-origin / all | Participation ratio | Conditional mean ratio | Conditional geometric ratio | Two-part log-normal |
|---|---|---|---|---|---|
| 0–17 | 0.529 / 0.386 | 1.370 (0.033) | 0.998 (0.189) | 0.905 (0.029) | 1.240 (0.055) |
| 18–64 | 0.238 / 0.243 | 0.977 (0.034) | 0.687 (0.033) | 0.684 (0.029) | 0.668 (0.041) |
| 65+ | 0.872 / 0.924 | 0.943 (0.011) | 0.899 (0.068) | 0.805 (0.064) | 0.759 (0.064) |
| All ages | 0.374 / 0.391 | 0.957 (0.022) | 0.597 (0.046) | 0.521 (0.019) | 0.498 (0.025) |

- **Children.** The child excess is participation. 53% of Mexican-origin children have any
  public payment against 39% of all children, and conditional on paying, their typical payment is
  lower (geometric ratio 0.905).
- **Adults and 65+.** Adults and older people participate at about the same rate as everyone else
  and draw less when they do.

**Direct standardization of the public ratio to the all-donor mix of Medicaid coverage, poverty
category (POVCAT 1–5) or both.** [CALCULATION: `pooled_ratios.py` `standardized`;
DATA: `derived/standardized.csv`]

| Age | Unstandardized | Medicaid coverage | Poverty category | Coverage × poverty |
|---|---|---|---|---|
| 0–17 | 1.367 | 0.962 (0.171) | 1.233 (0.272) | 1.011 (0.189) |
| 18–64 | 0.671 | 0.542 (0.030) | 0.542 (0.035) | 0.532 (0.030) |
| 65+ | 0.848 | 0.718 (0.052) | 0.787 (0.063) | 0.702 (0.057) |
| All ages | 0.571 | 0.439 (0.032) | 0.489 (0.044) | 0.428 (0.032) |

- **Coverage.** Medicaid coverage is what lifts the ratios. Ever-Medicaid shares are 66% against
  44% for children and 30% against 12% at 65+ [DATA: `derived/disconfirmation.csv`,
  `derived/mcbs_reconciliation.csv`]. Holding coverage at the all-donor mix removes the child
  excess entirely (0.96) and lowers the 65+ ratio to 0.72.
- **Poverty.** Poverty explains less than coverage for children and at 65+. At 18–64 the two
  explain the same amount.
- **Not a correction.** Standardization is descriptive, not a correction. The ledger's estimand is
  the unstandardized cell mean, because the group's coverage is a real feature of the group.
  [INFERENCE]

## 5. Dollars: the ledger

**How each current charge is scaled** [CALCULATION: `translate.py`; DATA:
`derived/translation_ledger.csv`, `derived/cps_cells.csv`]:
- The ledger charges each CPS record its transport cell's MEPS 2024 all-donor mean times
  `exposure`. Every record is exposed except infants that the CPS leaves out of universe.
- `medical` scales by the public ratio.
- `medical_transport_payers` repeats `medical` with the unharmonized six-payer list.
- `M` is (cell Medicaid mean × 0.5432) plus (cell Medicare mean × 0.2804), the NHEA-to-MEPS
  scaling. It scales by the Medicaid and Medicare ratios.
- SEs come from the PSU influence vectors of the ten cell ratios.

| Row | Current charge $bn | Plain | p99.5 | p99.9 | Two-part | Excl. 2020–21 | CPI all items | Year-normalized |
|---|---|---|---|---|---|---|---|---|
| medical, all ages | 92.88 | −1.92 (6.93) | −3.63 (3.84) | −3.93 (4.05) | −6.07 (4.19) | +0.73 (7.89) | −2.30 (6.68) | −2.75 (6.31) |
| medical, transport payers only | 92.88 | −2.12 (6.95) | −3.86 (3.87) | −4.15 (4.08) | −2.12 (6.95)¹ | +0.47 (7.91) | −2.51 (6.70) | −2.99 (6.32) |
| M, all ages | 35.15 | +2.07 (3.54) | +0.91 (1.58) | +0.78 (1.70) | +0.61 (1.70) | +2.72 (4.08) | +1.89 (3.41) | +1.71 (3.16) |
| **medical + M, all ages** | **128.03** | **+0.15 (10.42)** | **−2.71 (5.35)** | −3.16 (5.68) | −5.46 (5.79) | +3.45 (11.91) | −0.40 (10.04) | −1.03 (9.42) |
| medical + M, 0–17 | 26.90 | +10.16 (7.25) | +4.32 (1.68) | +3.87 (2.01) | +6.73 (1.48) | +11.97 (8.65) | +9.74 (6.92) | +8.97 (6.33) |
| medical + M, 18–64 | 57.51 | −4.83 (3.52) | −2.61 (2.93) | −2.16 (3.20) | −5.60 (3.39) | −4.80 (3.87) | −4.93 (3.47) | −4.76 (3.43) |
| medical + M, 65+ | 43.62 | −5.19 (3.04) | −4.42 (3.06) | −4.86 (3.05) | −6.59 (3.08) | −3.72 (3.01) | −5.21 (3.01) | −5.25 (2.95) |
| medical + M, US-born | 82.51 | +3.43 (9.08) | −0.00 (3.60) | −0.85 (3.85) | +0.07 (3.81) | +6.08 (10.67) | +2.88 (8.71) | +2.14 (8.09) |
| medical + M, born abroad | 45.51 | −3.28 (3.16) | −2.71 (2.95) | −2.31 (3.14) | −5.52 (3.12) | −2.63 (3.33) | −3.29 (3.13) | −3.17 (3.09) |

¹ The two-part model is fitted to harmonized public payments only; this row falls back to the
plain transport-payer ratios.

**What the table shows.** The ethnicity correction to the ledger's public medical charge is
indistinguishable from zero in every specification.
- **By age.** The child band gains cost: +$4.3bn winsorized, where the SE is small enough to
  exclude zero, and +$10.2bn plain. The 65+ band loses $3.7–6.6bn. 18–64 loses $2.2–5.6bn.
- **By nativity.** The born-abroad part of the charge falls ($2.3–5.5bn). The US-born part is flat
  once the child tail is capped.
- **Report the age split with the total.** Because the child band carries most of the positive
  side, a reader who wants a generation or age split should use the age rows, not the all-ages
  total. [CALCULATION]

## 6. Dollars: the complete account

The account allocates national BEA totals with expected-dollar keys built from MEPS 2024 cell
means on the CPS civilian population. Of each national total, 0.990 goes to households and the
remainder to people outside them. [SOURCE: `full_account_spending_2026_09_20/builder.py`;
DATA: `allocations.csv` `household_pool_fraction`]

**Payer-to-line mapping, as the builder's keys define it:**

| Account line (target $bn) | Key | MEPS 2024 column(s) in the key | Ratio applied |
|---|---|---|---|
| Medicaid/CHIP/other medical (116.91) | `medicaid` | `TOTMCD24` | harmonized Medicaid |
| Medicare (63.96) | `medicare` | `TOTMCR24` | Medicare |
| Health services (23.53) | `health_other` | `TOTVA24 + TOTTRI24 + TOTOFD24 + TOTSTL24` | other public |
| Military medical (0.65) | `tricare` | `TOTTRI24` | TRICARE |
| Veterans other (2.37) | `va_medical` | `TOTVA24` | VA |

**How the lines are translated** [CALCULATION: `translate.py`; DATA: `derived/translation_account.csv`]:
- The union's key in each cell is multiplied by that cell's ratio.
- The national key total is held fixed, because the cell mean is the donor average and people
  outside the union in the same cell absorb the complement.
- So each line changes by the line amount × (key-weighted ratio − 1).
- The renormalized variant instead leaves everyone else's key unchanged.

| Line | Target $bn | Plain | p99.5 | p99.9 | Two-part | Excl. 2020–21 | CPI all items | Year-normalized |
|---|---|---|---|---|---|---|---|---|
| **Medicaid/CHIP/other medical** | 116.91 | +20.09 (16.64) | **+13.64 (6.31)** | +12.16 (7.02) | +17.56 (7.02) | +21.27 (19.39) | +19.19 (15.97) | +18.09 (14.76) |
| **Medicare** | 63.96 | −10.67 (3.74) | **−9.91 (3.22)** | −9.03 (3.53) | −15.85 (3.34) | −8.38 (4.14) | −10.63 (3.68) | −10.41 (3.60) |
| Health services | 23.53 | −5.16 (2.01) | −5.67 (1.45) | −5.27 (1.85) | −6.03 (1.74) | −4.01 (2.36) | −5.27 (1.97) | −5.52 (1.89) |
| Military medical | 0.65 | −0.31 (0.08) | −0.33 (0.04) | −0.32 (0.06) | −0.31 (0.08)¹ | −0.29 (0.09) | −0.31 (0.08) | −0.30 (0.08) |
| Veterans other | 2.37 | −0.76 (0.30) | −0.73 (0.25) | −0.64 (0.29) | −0.76 (0.30)¹ | −0.57 (0.35) | −0.79 (0.29) | −0.87 (0.28) |
| **All five medical lines** | 207.43 | +3.18 (17.65) | **−3.00 (8.04)** | −3.11 (8.66) | −5.39 (8.78) | +8.02 (20.37) | +2.19 (16.97) | +0.98 (15.73) |
| Key-weighted Medicaid ratio | | 1.172 | 1.117 | 1.104 | 1.150 | 1.182 | 1.164 | 1.155 |
| Medicaid, renormalized | | +17.24 | +11.78 | +10.52 | +15.11 | +18.22 | +16.48 | +15.55 |
| Medicare, renormalized | | −10.15 | −9.42 | −8.57 | −15.14 | −7.95 | −10.11 | −9.90 |

¹ These rows use the plain TRICARE and VA ratios; the two-part model is fitted to public, Medicare,
Medicaid and other public only.

**The account's Medicaid line under-charges the group and its Medicare line over-charges it.**
- The Medicaid under-charge is $12–21bn and holds in every specification. Its interval excludes
  zero at p99.5 and in the two-part model.
- The Medicare over-charge is $8–16bn, and every specification excludes zero.
- They largely offset.
- Children drive the Medicaid excess. US-born children hold 39% of the union's Medicaid key, and
  their Medicaid ratio (1.41 plain, 1.18 winsorized) supplies most of the excess: 0.16 of the
  key-weighted 0.17 plain, and 0.07 of 0.12 winsorized. [CALCULATION: `derived/cps_cells.csv`
  `key_medicaid` × cell ratios from `derived/ratios.csv`]

**Cross-check against coverage and dollars.** In MEPS, Mexican-origin people are 11.6% of persons
and 13.5% of Medicaid dollars, a factor of 1.16. The account's CPS key gives the union 12.4% of the
Medicaid key against 12.1% of the population, a factor of 1.02. The implied correction, 1.14,
agrees with the key-weighted ratio. [DATA: `derived/bounds.csv` `coverage_key`]

**Year by year**, each year's own ratios and design, with the same translation
[DATA: `derived/translation_by_year.csv`]:

| Year | Ledger medical + M, plain | Same, p99.5 | Account Medicaid, plain | Same, p99.5 | Account Medicare, plain | Same, p99.5 |
|---|---|---|---|---|---|---|
| 2016 | +0.22 (10.65) | −2.35 (8.86) | +9.26 (9.77) | +7.80 (7.70) | −3.67 (9.72) | −6.55 (7.45) |
| 2017 | +3.25 (10.88) | +4.67 (9.32) | +9.69 (13.99) | +15.45 (9.94) | −1.38 (7.12) | −5.96 (6.71) |
| 2018 | +1.37 (9.52) | +4.14 (8.97) | +2.80 (10.64) | +9.32 (9.17) | +5.02 (7.18) | +2.56 (6.77) |
| 2019 | −6.14 (10.09) | −3.53 (9.02) | −4.25 (11.43) | +6.95 (10.75) | −1.30 (7.81) | −2.63 (6.03) |
| **2020** | +1.47 (14.23) | −2.79 (11.07) | +33.13 (20.78) | +19.02 (12.60) | −13.76 (7.99) | −10.13 (7.40) |
| **2021** | −24.35 (10.55) | −13.09 (9.60) | +1.96 (15.91) | +19.85 (13.06) | −24.49 (4.99) | −22.42 (4.66) |
| 2022 | −22.34 (9.22) | −14.33 (9.41) | −4.81 (12.42) | +6.94 (12.46) | −20.01 (4.92) | −18.52 (4.94) |
| 2023 | +10.00 (16.79) | +0.90 (9.93) | +40.21 (25.76) | +23.46 (13.18) | −13.09 (9.07) | −14.86 (7.11) |
| 2024 | +25.04 (30.03) | +1.51 (11.90) | +64.89 (49.71) | +14.34 (13.57) | −15.68 (8.75) | −9.90 (9.16) |

- **Medicaid.** Winsorized, the Medicaid line is positive in all nine years, between +$6.9bn and
  +$23.5bn.
- **Medicare.** Medicare is negative in eight of nine years, and at its most negative in 2021–22.
- **The 2024-only ledger figure.** A 2024-only translation gives +$25.0bn (SE 30.0). It is driven by
  the same child record [INFERENCE]. That is the number the 2024 lane called unusable, and pooling
  replaces it.

## 7. 65+: MCBS, nursing facilities and institutions

**Neither file includes people in institutions.**
- MEPS covers the civilian non-institutional population.
- The MCBS lane's 1.265 comes from the Cost Supplement PUF. That file "excludes beneficiaries who
  had a Facility interview during the year or who incurred any facility, hospice, or institutional
  events or costs during the year".
  [SOURCE: `MCBSMicrodataPUFDataUsersGuide.pdf` §3.3 p. 4, quoted in
  `mcbs_elderly_medical_2026_09_22/RESULT.md`]
- The brief's premise that MCBS "includes facility stays in its cost supplement design" does not
  hold for the file the lane used. The MCBS–MEPS gap is therefore not an institutions effect.

**Walk from the ledger's estimand to the MCBS lane's, one definition at a time**
[CALCULATION: `pooled_ratios.py` `mcbs_reconciliation`; DATA: `derived/mcbs_reconciliation.csv`]:

| Step | Pooled 2016–2024 | 2023 only |
|---|---|---|
| 1 Ledger estimand: Mexican-origin / all donors, all public payers | 0.848 (0.067) | 0.722 (0.106) |
| 2 Reference switched to non-Hispanic white | 0.843 (0.069) | 0.707 (0.109) |
| 3 Group widened to all Hispanic (MCBS `CSP_RACE = 3`) | 0.946 (0.052) | 0.806 (0.083) |
| 4 Restricted to Medicare-ever (the MCBS universe) | 0.977 (0.053) | 0.828 (0.086) |
| 5 Public = Medicare + Medicaid only (the MCBS payer set) | **1.005 (0.056)** | **0.845 (0.089)** |
| 6a Step 5, below 200% FPL | 0.937 (0.062) | 1.021 (0.126) |
| 6b Step 5, at or above 200% FPL | 0.939 (0.076) | 0.662 (0.106) |
| 7a Mexican-origin / all donors, below 200% FPL | 0.783 (0.077) | 0.806 (0.145) |
| 7b Mexican-origin / all donors, at or above 200% FPL | 0.821 (0.074) | 0.611 (0.101) |
| 8 Mexican-origin / all donors, Medicare-ever only | 0.870 (0.067) | 0.720 (0.110) |
| MCBS 2023, Hispanic / NH white, public | | 1.265 (0.152) |

**Where the definitions stand.** Aligning the definitions moves MEPS from 0.848 to 1.005 pooled.
- Most of the move comes from widening Mexican-origin to all Hispanic origins (+0.10).
- Restricting to Medicare-ever people and to the Medicare + Medicaid payer set adds +0.06.
- The pooled MEPS figure on MCBS's definitions differs from MCBS by 0.26 (z ≈ 1.6).
- The same-year 2023 figure differs by 0.42 (z ≈ 2.4). [CALCULATION: (1.265 − 1.005) /
  √(0.152² + 0.056²); (1.265 − 0.845) / √(0.152² + 0.089²)]
- MEPS 2023 is a low year, but the year test does not reject stability (p 0.157), so 2023 alone
  does not settle it.
- The remaining difference is between instruments. Candidate sources [INFERENCE; not tested here]:
  - household-reported MEPS payments against administrative fee-for-service claims in MCBS;
  - Medicare Advantage accounting;
  - MCBS's top-coding at the 99.5th percentile.

**The strongest reading against this lane.** Suppose MCBS's level is right and MEPS's shortfall
against it is a reporting error specific to Hispanics that carries over to the ledger's estimand.
- The union-weighted 65+ ratio would then be 0.881 × 1.265 / 1.005 ≈ 1.11.
- The 65+ ledger change would be about 43.62 × 0.11 ≈ **+$4.8bn instead of −$5.2bn**.
- The all-ages ledger total would then sit near +$10bn plain, or +$7bn winsorized.
- Nothing in either file shows the error is specific to Hispanics. The pooled MEPS reading stays
  the measured one, and this is its bound. [INFERENCE]

**At 65+, the Mexican-origin group differs from all donors on coverage and income**
[DATA: `derived/mcbs_reconciliation.csv`]:

| Share at 65+ | Mexican-origin | All Hispanic | NH white | All donors |
|---|---|---|---|---|
| Medicaid-ever | 30.3% | 32.1% | 6.4% | 11.7% |
| Medicare-ever | 95.1% | 95.3% | 98.8% | 98.2% |
| Uninsured all year | 2.2% | 2.0% | 0.1% | 0.3% |
| Below 200% FPL | 48.3% | 47.4% | 24.6% | 29.0% |

**How the ledger charges institutions (item N).** The ledger does not carry institutional care
through MEPS, so leaving institutions out of MEPS does not bias its medical charge.
- Item N charges institutional care separately. It uses each group's own ACS 2024 institutional
  group-quarters count, at $94,325 of public cost per institutionalized person aged 65+:
  (147e9 / 1.2e6) × (0.63 + 0.14).
- The group's low institutional rates therefore already enter through item N.

[SOURCE: `absolute_ledger.py` `institutional_cost_by_band`, lines 459–486, read only]

**How the complete account charges nursing-home Medicaid.** It charges it through the community
key.
- BEA's Medicaid line ($954.2bn) includes institutional long-term care, and the builder allocates
  the whole line by the MEPS community Medicaid key.
- The union's share of the line is 12.25%: its key share of 12.38% × 0.990.
- CMS reports 2023 Medicaid institutional LTSS of $82.7bn. Nursing facilities account for $68.8bn
  of it (83.2%), serving 1,294,881 users. [SOURCE: CMS/Mathematica, "Medicaid Long-Term Services
  and Supports Users and Expenditures by Service Category, 2023", medicaid.gov, bytes from Wayback
  snapshot 20260109200423; quotes in `derived/bounds_audit.json` `ltss_2023`]
- So the account charges the union **$8.43bn** of nursing-facility Medicaid.

**What use supports** [DATA: `institutional_bound_2026_09_17/derived/acs_cells.csv`;
CALCULATION: `bounds.py`]:
- ACS 2024 counts 43,447 union members aged 65+ in institutional group quarters.
- All natives plus the Mexico-born count 1,356,205. This denominator omits other foreign-born
  people, so the share it gives, **3.20%**, is a ceiling.
- Institutional rates:

  | Group | 65–74 | 75+ |
  |---|---|---|
  | Mexico-born | 0.58% | 1.97% |
  | US-born Mexican | 1.36% | 2.61% |
  | All natives | 1.38% | 4.22% |

- A use-based nursing-facility charge is therefore at most **$2.20bn**. Doubling the share to
  allow for under-65 residents gives **$4.41bn**.
- **The account over-charges the group $4.0–6.2bn here.**

**The Medicaid line with both corrections.** The MEPS ratio is applied to the line's
non-nursing-facility part, and nursing facilities are charged by use. The five-line SEs are
linearized through all five lines' influence vectors.
[CALCULATION: `bounds.py`; DATA: `derived/bounds.csv` `medicaid_line_combined`,
`medical_lines_combined`]

| Specification | Medicaid line, nursing-facility share at ceiling | Same, share doubled | All five lines, share at ceiling | Same, share doubled |
|---|---|---|---|---|
| Plain | +12.42 (15.44) | +14.62 (15.44) | −4.49 (16.49) | −2.29 (16.49) |
| p99.5 | +6.43 (5.85) | +8.63 (5.85) | **−10.21 (7.64)** | **−8.01 (7.64)** |
| p99.9 | +5.06 (6.51) | +7.26 (6.51) | −10.21 (8.22) | −8.01 (8.22) |
| Two-part | +10.07 (6.51) | +12.27 (6.51) | −12.88 (8.33) | −10.68 (8.33) |
| Excl. 2020–21 | +13.51 (17.99) | +15.71 (17.99) | +0.26 (19.02) | +2.47 (19.02) |
| CPI all items | +11.58 (14.82) | +13.79 (14.82) | −5.42 (15.86) | −3.22 (15.86) |
| Year-normalized | +10.56 (13.69) | +12.76 (13.69) | −6.55 (14.71) | −4.34 (14.71) |

## 8. Disconfirmation: the strongest case that the group draws more

**The case.**
- At 65+, Mexican-origin people are 2.6× as likely as all donors to have Medicaid (30% against
  12%) and 4.7× as likely as whites. Medicaid pays for the most expensive care.
- Uninsured people use emergency and uncompensated care that household surveys record poorly.
- Emergency Medicaid for the unauthorized is billed to Medicaid for people who do not report
  enrollment, so MEPS may miss it.
- Recent arrivals may be sicker, or may use more care, than the long-settled people who dominate
  the sample.

**What the pooled data say** [DATA: `derived/disconfirmation.csv`,
`derived/coverage_vs_dollars.csv`, `derived/bounds.csv`]:

| Check | Mexican-origin | All donors | NH white |
|---|---|---|---|
| Medicaid-ever, all ages | 38.3% | 22.8% | 15.2% |
| Share of Medicaid-covered people / share of Medicaid dollars (pooled) | 19.4% / 13.5% | 100% / 100% | |
| Uninsured all year, all ages (18–64) | 17.4% (26.0%) | 6.5% (9.6%) | 3.9% (5.9%) |
| Public $ per uninsured person, all ages (18–64) | $164 ($172) | $268 ($274) | $373 ($391) |
| Public $ per uninsured person, 65+ | $600 (SE 289, n 81) | $430 (SE 174, n 205) | $284 (n 38) |
| Medicaid $ paid for people not reporting enrollment, 2016–18 (`TOTOPU`), per person | $22.8 (SE 6.0) | $14.8 (2.1) | $11.5 (2.6) |
| Same, share of Medicaid dollars | 2.8% | 1.8% | 1.7% |
| Medicaid $ for people never reporting Medicaid, 2019–24, per person | $19.4 (SE 3.8) | $25.7 (3.0) | $29.1 (4.8) |
| Same, share of Medicaid dollars | 1.9% | 3.0% | 4.2% |

**Coverage.** Coverage does not carry into dollars.
- Mexican-origin people are 19.4% of those ever on Medicaid but 13.5% of Medicaid dollars. A
  covered Mexican-origin person therefore draws 0.69 of the average covered person's dollars.
- At 65+ the same calculation from the ratio table gives 1.895 / 2.584 = 0.73.
- The account's +$68.7bn stress test keys Medicaid by reported coverage, which assumes a covered
  person costs the average. MEPS contradicts that assumption for this group.
  [CALCULATION: `derived/coverage_vs_dollars.csv`, `derived/ratios.csv`]
- The CPS union's share of reported coverage (19.6%) matches MEPS's Mexican-origin share of the
  covered (19.4%), so the contradiction is not a difference between the two surveys.

**The uninsured.** Uninsured Mexican-origin children and adults draw less public money than other
uninsured people.
- The exception is 65+, where the point estimate is higher but rests on 81 people. At 2.2% of the
  group's elderly, it moves the 65+ mean by less than $5 per person.
- Uncompensated care that no one pays for is not a MEPS payment. The complete account charges it
  by use in its own line, which is outside this lane's lines.
  [SOURCE: `decisions/2026-09-23-main-case-general-government-and-use-keys.md`]

**Medicaid that respondents do not report.** MEPS records Medicaid payments for people who do not
report enrollment, through its provider follow-back.
- In 2016–18 that category was larger for the Mexican-origin group, and it is already inside the
  harmonized ratio.
- From 2019 it is smaller for the group.

**Recent arrivals** draw less than all foreign-born donors, not more. Public ratios by years in
the US, against all foreign-born donors [DATA: `derived/disconfirmation.csv`]:

| Age | Under 5 years in the US | 5–14 years | 15+ years |
|---|---|---|---|
| All ages | 0.26 (0.07) | 0.29 (0.04) | 0.87 (0.07) |
| 18–64 | 0.54 (0.23) | 0.60 (0.09) | 1.08 (0.11) |

**Emergency Medicaid.** CBO's Table 1 reports federal plus state emergency Medicaid for people
ineligible for full coverage by immigration status, from CMS-64 [SOURCE: CBO letter to Rep.
Arrington, 2 October 2024, Table 1; bytes from Wayback snapshot 20241003010917, because cbo.gov
serves a captcha to scripts; DATA: `derived/cbo_emergency_medicaid_table1.csv`]:

| FY2017 | FY2018 | FY2019 | FY2020 | FY2021 | FY2022 | FY2023 | Total |
|---|---|---|---|---|---|---|---|
| $1.54bn | $2.61bn | $3.11bn | $3.08bn | $7.05bn | $5.40bn | $3.78bn | $26.55bn |

- MEPS already records $19.38 per person (SE 3.82) of Medicaid for Mexican-origin people who never
  report Medicaid. For the union's 40.9M people that is **$0.79bn** (SE 0.16), or $1.22bn after
  the ledger's NHEA scaling.
- Take the unauthorized population's Mexico share as the group's share of emergency Medicaid:
  30% (Pew 2023) or 44% (OHSS, January 2022), from the ledger's `params.json`.
- The FY2023 dollars MEPS cannot see are then **$0.34–0.87bn**. In the FY2021 peak they are
  $1.32–2.31bn.
- If every dollar were the group's, which is an impossible ceiling, they would be $2.98bn in
  FY2023 and $6.26bn in FY2021. [CALCULATION: `bounds.py`; DATA: `derived/bounds.csv`
  `emergency_medicaid`]
- Even the ceiling is small beside the $12–21bn Medicaid-line correction, and it has the opposite
  sign to the nursing-facility over-charge.

**Conclusion.** The pooled data rule out a material excess at 18–64 and at 65+, within MEPS's
scope and on the ledger's estimand. They do not rule out parity.
- The union-weighted 18–64 ratio is 0.92 plain (CI 0.80–1.04) and 0.955 winsorized (0.86–1.05).
- The 65+ ratio is 0.88 plain (CI 0.74–1.02).
- Across all seven specifications, the upper 95% bounds reach 1.07 at 18–64 and 1.05 at 65+. An
  excess worth more than about $4bn at 18–64 or $2bn at 65+ is therefore excluded.
  [CALCULATION: union-weighted table, section 2]
- The case holds for children. Their cells run at 1.16× winsorized, a ratio driven by Medicaid
  coverage.
- The one open channel is the MCBS level at 65+ (section 7). The emergency Medicaid MEPS cannot
  see is bounded well below the size that would reverse the signs.

## 9. What this changes elsewhere (for the lead to route)

- **Ladder 175 and** `research/immigration-mexican-origin-medical-transport-check-2026-09-22.md`
  - "0.69 of their cell's public dollars at 18–64" is an age-domain figure. On the transport's
    cells, the pooled figure is 0.92 (plain) to 0.96 (p99.5).
  - At 65+, the "open, about −40% to +56%" range narrows. The ledger's estimand is 0.88
    union-weighted (CI 0.74–1.02). The MCBS-anchored alternative is about 1.11.
- **The +$68.7bn coverage-key stress test** in the complete-account memo rests on the equal-cost
  assumption that section 8 contradicts.
- **The account's line split.** The ratios move roughly +$12–21bn onto the Medicaid line and
  −$8–16bn off Medicare; the nursing-facility allocation over-charges $4–6bn.
  - Both are candidate corrections, and adopting them is the operator's call.
  - Net of both, the five medical lines fall $8–10bn winsorized (SE 7.6).
- **The ledger's public medical charge needs no ethnicity adjustment at the precision available.**
  The all-ages correction is −$2.7bn (SE 5.4) winsorized.

## 10. Limits

- **Population scope.** MEPS covers the civilian non-institutional population. Institutional care
  is handled by item N in the ledger and by the nursing-facility bound here. Three institutional or
  long-term-care items are not re-allocated:
  - ICF/IID ($10.6bn) and mental-health facilities ($3.2bn);
  - home and community-based services ($145.9bn), part of the $954.2bn line, which the account also
    allocates by the community key.

  The group is young, so both re-allocations would most likely lower its charge, but neither is
  computed. [INFERENCE]
- **The Medicaid key's age profile is flagged, not computed.**
  - MEPS captures about 1 / 1.5432 of adjusted NHEA Medicaid, and the missing part is plausibly
    concentrated in aged and disabled long-term care.
  - CMS data put children at 35.9% of 2023 beneficiary-years but 15.6% of spending.
    [SOURCE: CMS, as quoted in `research/immigration-complete-annual-account-2026-09-20.md`
    line 244]
  - If the missing dollars sit with the old and disabled, a key scaled uniformly from MEPS
    over-allocates Medicaid to a young population.
  - This is an ethnicity-independent issue, and a follow-up lane should size it from T-MSIS/TAF
    spending by age. [INFERENCE]
- **Group definitions differ.** `HISPNCAT == 1` is self-reported Mexican origin with no other
  Hispanic group; people reporting several groups fall outside it. The union is built from CPS
  birthplace, parentage and self-identification. Within each cell, the translation assumes the
  MEPS Mexican-origin donors represent the union's members, including their income and coverage
  mix; that mix is not re-weighted to the CPS union.
- **Reporting is assumed uniform across groups.** Item M's NHEA scaling and the account's national
  totals treat MEPS under-reporting as the same for every group. The walk to MCBS (section 7)
  leaves room for a reporting gap specific to Hispanics at 65+, of unknown size.
- **Winsorization trades bias for variance.** Applying a capped ratio to an uncapped all-donor mean
  assumes the group's tail scales with its body. The plain estimator is unbiased but carries a
  heavy child tail (SE 0.26), so both are reported.
- **Year normalization.** The year-normalized specification treats its normalization factors as
  fixed; its SEs ignore their sampling error.
- **The pool spans policy changes**, among them ACA expansions and continuous Medicaid enrollment
  from 2020 to 2023. The pooled ratio is an average over those regimes. The year table shows no
  trend in the public ratio, but the 2021–22 Medicare dip is not explained here.
- **Timing and units in the nursing-facility bound.**
  - Nursing-facility dollars are 2023 (CMS), applied to a 2024 BEA line.
  - The ACS denominator omits foreign-born people not from Mexico, so the share is a ceiling.
  - The "doubled" allowance for residents under 65 is a round assumption, not an estimate.
- **Emergency Medicaid.** The bound assumes the group's share of emergency Medicaid equals the
  Mexico share of the unauthorized population, which means equal use per person.
- **Instrument bias.** This analysis was conducted by an LLM with post-training dispositions on
  politically charged topics (`notes/llm-bias-caveat.md`).
  - Directional checks: one correction was computed that lowers the group's charge (nursing
    facilities) and one channel that raises it was bounded (emergency Medicaid).
  - Of the items not computed, the long-term-care allocations would most plausibly lower the
    charge and a Hispanic-specific reporting gap would raise it.
  - The verdict rests on neither.
  - The child band, where the data run against the group, is reported at full size.

## 11. Reproduction

Run from the repository root, in this order. Each step prints line-based progress and stops with
`[BLOCKED]` on a failed gate.

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/fetch_meps.py      # download + pin (skips pinned files)
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/meps_pool.py       # year gates, HC-036 link, pooled.parquet
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/pooled_ratios.py   # gates 1-2, all ratio specifications
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/translate.py       # gate 3, ledger and account dollars
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/bounds.py          # nursing facility, emergency Medicaid, coverage key
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/validate_se.py     # PSU bootstrap of three SEs
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/ -q
```

**Test suite.** `test_pooled.py` re-checks the derived files, 16 tests:
- input hashes;
- year and reproduction gates;
- ratios against cell means, and confidence intervals;
- the two-part identity and the headline ratios;
- the translation identities against `allocations.csv` and `incidence_keys.csv`;
- the bounds arithmetic and the SE validation.

**Files.**

| File | Contents |
|---|---|
| `design.py` | PSU-influence estimator, weighted quantiles, χ² tail |
| `fetch_meps.py` | Downloads and pins inputs |
| `meps_pool.py` | Year gates, HC-036 linkage, pooled frame |
| `pooled_ratios.py` | Every ratio specification, year-by-year runs, MCBS walk, standardization, disconfirmation |
| `translate.py` | Ledger and account dollars |
| `bounds.py` | Checks outside MEPS's scope |
| `validate_se.py` | Bootstrap SE check |
| `derived/` | Tracked aggregates |
| `_cache/` | Raw downloads, parsed text, pooled microdata and pickles; gitignored |
