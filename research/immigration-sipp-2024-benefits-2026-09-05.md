**Verdict:** In calendar 2024, SIPP foreign-born adults aged 25–64 averaged **$250 in allocated SNAP, TANF and individual SSI**, versus **$456 for all native adults**. The foreign-born-minus-native difference is **−$205 per adult, with a design-based 95% interval of −$284 to −$126**. This is a descriptive estimate for three benefits, with explicit allocation assumptions; it does not establish which population has a larger net fiscal contribution. The broad recent-entry group averages $153, but its 154 sampled adults cannot support a precise recent-cohort ranking.

As of 2026-09-05. [CALCULATION: official 2025 SIPP person records, covering 2024, and 240 Census replicate weights; generator and artifacts below.] The comparison was defined before inspecting these benefits: December adults aged 25–64, all native versus all foreign-born, with the dictionary's latest entry bin as a supplementary domain. There is no income, employment or benefit-recipient filter.

| December adult population | Sample adults | Weighted adults | SNAP $/adult | TANF $/adult | SSI $/adult | Three benefits $/adult (95% interval) | Any of the three during 2024 |
|---|---:|---:|---:|---:|---:|---:|---:|
| All native | 12,211 | 140.258 million | 171.13 | 3.96 | 280.46 | **455.55 (414.13–496.96)** | 11.28% |
| All foreign-born | 2,576 | 29.719 million | 123.90 | 1.13 | 125.34 | **250.37 (183.72–317.03)** | 7.64% |
| Foreign-born, entry code covering 2022–25 | 154 | 1.699 million | 78.46 | 0 observed | 74.62 | **153.08 (19.80–286.37)** | 5.77% |
| Foreign-born, entry codes through 2021 | 2,422 | 28.020 million | 126.66 | 1.20 | 128.41 | **256.27 (185.97–326.57)** | 7.75% |

All amounts are nominal **2024 dollars per selected adult over the observed calendar year**, including adults with no benefits. Program amounts are gross receipts allocated to beneficiaries, not expenditure net of their taxes. All-race native includes US/island-area birth and birth abroad to US-citizen parents; this is broader than the earlier non-Hispanic-white comparator. The denominator is SIPP's December-weighted population, not the ACS recipient population in the earlier microsimulation. [CALCULATION: `benefit_profiles_2024.csv`; SOURCE: [2025 data files](https://www2.census.gov/programs-surveys/sipp/data/datasets/2025/), dictionary fields `EBORNUS`, `ENATCIT`.]

The recent-entry-minus-earlier-entry difference is **−$103**, with a **−$254 to +$48** 95% interval. The data therefore do not resolve that ranking. Only 11 recent-entry adults had any of these benefits; ten had SNAP, two had SSI and none had TANF, with overlapping program participation. The zero TANF estimate and its mechanical zero replicate standard error do **not** establish population zero. Both profiles and contrasts flag zero-observation domains. Normal intervals can extend below zero for rare nonnegative outcomes; they are sampling approximations, not negative benefit predictions or reliable rare-event bounds. [CALCULATION: `benefit_profiles_2024.csv`, `benefit_contrasts_2024.csv`.]

The year code needs care. In the **2025** dictionary, `TYRENTRY=2025` pools **2022–25**. It cannot separate 2022, 2023 and 2024 arrivals, measure a policy-specific admitted cohort, or identify precise time since arrival. `TIMSTAT` describes first-entry Permanent/Other status; it is not used to infer current legal status or work authorization. A reported entry code is also not a record of all border arrivals. [SOURCE: [2025 SIPP dictionary](https://www2.census.gov/programs-surveys/sipp/tech-documentation/data-dictionaries/2025/2025_SIPP_Data_Dictionary.pdf), pp. 916–917.]

The allocation and survey design were checked against the **2025** definitions, rather than assumed from the old release. `TSNAP_AMT` and `TTANF_AMT` are monthly owner-record amounts; coverage and owner pointers identify the beneficiaries. The established allocator divides each total equally among its covered people in that sample-unit/owner/month, before selecting age or nativity. A benefit owner need not be a beneficiary. Child shares stay with children. `TSSI_AMT` stays with its individual recipient. This preserves reported dollars once per benefit unit, while equal shares remain an accounting assumption about incidence. These fields do not isolate federal from state funding. [SOURCE: 2025 dictionary, pp. 2930–2931, 3002–3009, 3094, 3158–3160; field-by-field extracts in `verified_2025_field_definitions.json`.]

The real-data allocation check covered **379,215 person-month rows from 32,052 distinct people**. Unweighted allocated sample totals were $5,552,082 SNAP, $261,204 TANF and $8,357,754 SSI. Selected adults received $2,469,887.39, $58,875.13 and $4,017,807 respectively; the residual stays with children and other people outside the selected adult population. These are **sample conservation checks, not national spending totals**. No selected adult's three-program benefits occurred in months marked outside the survey frame. [CALCULATION: `manifest.json`; each program's all-person total equals selected-adult plus outside-selected total.]

Each selected person contributes the **positive December `WPFINWGT` once** to annual sums. Census recommends this weight for calendar-year estimates; there is no separate annual weight. Monthly values are summed without scaling short exposure to twelve months. Every selected person had twelve monthly records, but some months were outside the survey frame. Weighted mean in-frame months were **11.981 native, 11.968 foreign-born and 11.692 in the latest entry bin**; partial-frame-year shares were **0.29%, 0.64% and 5.69%**. Limiting each nativity group to twelve in-frame months yields **$454.04 native and $251.96 foreign-born**. This selected sensitivity leaves the stock comparison nearly unchanged; it does not solve entrant undercoverage or make the recent-entry population comparable to established residents. [SOURCE: [2025 SIPP Users' Guide](https://www2.census.gov/programs-surveys/sipp/tech-documentation/methodology/2025_SIPP_Users_Guide.pdf), §7.3.4, p. 159; CALCULATION: profiles.]

Uncertainty uses all **240 December replicate weights**, joined on the documented person/month identifiers. Every one of the **14,787 selected adults** matched, and each replicate file's full-sample `REPWGT0` agreed with that person's December weight. The full person and replicate files have different row counts; selected-domain coverage was checked directly. Each replicate recomputes the weighted ratio, and each contrast uses the difference within that same replicate:

\[
\widehat\mu_g=\frac{\sum_{i\in g}w_i y_i}{\sum_{i\in g}w_i},\qquad
\widehat{\mathrm{Var}}(\widehat\theta)=\frac{1}{240(0.5)^2}\sum_{r=1}^{240}(\widehat\theta_r-\widehat\theta)^2.
\]

This preserves survey and within-wave group covariance. Intervals use ±1.96 standard errors. Replication does not capture the full uncertainty from nonresponse, underreporting, imputation or equal-beneficiary allocation; Census explicitly cautions about variance with imputed data. SIPP targets the civilian, noninstitutionalized US population, but civilian status is determined at interview. Its population and observation clock are consequently not identical to an ACS survey-year restriction or a current administrative admissions register. [SOURCE: Users' Guide §§2.1.1, 7.2.3–7.2.4, pp. 16, 154–156.]

Reported earnings and person income are included only as auxiliary descriptive outputs. Zero earnings and business losses are retained. Their annual sums include reported out-of-frame months: the latter contribute **$32.99 per native adult, $68.67 per foreign-born adult and $715.75 per latest-entry-bin adult** to reported earnings. They are therefore not an exclusively US earnings or taxable-income measure and are not used here to calculate taxes. Person income must not be added to these benefit amounts as though the components were disjoint. [CALCULATION: annual person output and independent verification; SOURCE: dictionary `TPEARN`, `TPTOTINC`.]

The substantive residual is large. These comparisons combine age, disability, resources, family structure, program eligibility, take-up, reporting and migration selection. They omit other transfers, health, education, taxes, retirement costs and public goods. Neither the native–foreign-born gap nor the broad entry-bin contrast identifies an effect of immigration or of a presidential administration. A lower amount on this three-program ledger supports only that narrower conclusion. [INFERENCE from the measured scope; no causal adjustment or policy instrument is estimated.]

Reproduction uses [the generator](../infra/immigration-fiscal/build/analyze_sipp_2025.py) and the shared owner-to-beneficiary allocator in [public_mvp_io.py](../infra/immigration-fiscal/build/public_mvp_io.py). The only shared-reader change is accepting one validated `puYYYY.csv` member; malformed or ambiguous archives fail. Run from the repository root:

```sh
uv run --with numpy python3 infra/immigration-fiscal/build/analyze_sipp_2025.py \
  --schema .scratch/clarity-next-20260905/admission/pu2025_schema.json \
  --zip /Volumes/2TBPNY/research-data/immigration-fiscal/data/external/stage3/census/sipp_2025/pu2025_csv.zip \
  --replicate-schema /Volumes/2TBPNY/research-data/immigration-fiscal/data/external/stage3/census/sipp_2025/rw2025_schema.json \
  --replicate-zip /Volumes/2TBPNY/research-data/immigration-fiscal/data/external/stage3/census/sipp_2025/rw2025_csv.zip \
  --out-dir .scratch/clarity-next-20260905/sipp/results
uv run --with duckdb,pandas,numpy python3 -m unittest discover \
  -s infra/immigration-fiscal/tests -p 'test_sipp*.py'
uv run python3 .scratch/clarity-next-20260905/sipp/verify_outputs.py
```

**Validation:** 29 SIPP tests passed, including unchanged 2024 behavior, different monthly/December weights, mixed-nativity adults with child beneficiaries, zero and negative earnings, partial exposure, invalid entry codes, exact expected Fay variance/covariance, missing/mismatched replicate weights, the official lower-case replicate header, and propagation of zero-event warnings. A separate standard-library calculation rechecked **all 90 weighted profiles and all 45 replicate contrasts**, plus selected-person coverage and sample-dollar conservation. No canonical database was written.

The ignored artifact directory `.scratch/clarity-next-20260905/sipp/` contains the verified dictionary definitions, acquisition manifest, independent verification script/result and `results/` with person allocations, profiles, contrasts, replicate estimates and manifest. Raw ZIPs remain on the SSD. Official replicate data were probed first and downloaded with a 600 MB cap; the replicate ZIP, schema and guide total **538,956,342 bytes**. The following SHA-256 values pin the actual source versions:

| Source | SHA-256 |
|---|---|
| `pu2025_csv.zip` | `570798a6f512c8f82af311ee01a1668d178063c9076c18a05bc3a5a0039b67ed` |
| `pu2025_schema.json` | `6cdc23c537ba1431540e62994f0c05e05e62920e785384872bf5b7c23fe8c241` |
| `rw2025_csv.zip` | `3bf35c17723de10697d581d1122fda4d7cdecb34c6f9e9dfcb18ddc561c7c6b6` |
| `rw2025_schema.json` | `9a7c9ddfa1344f96a65425590a4efc34919a131a34b669f0fa89a075dd85c6e9` |
| 2025 dictionary PDF | `571e53b4ec3ebb11bebddbb7190fc1084f5364b8a1ec5fbd7ca8e2f69e7cc752` |
| 2025 Users' Guide PDF | `0f0bfbc9bbd0de97d8cfd07ec3128925159c9696d259893e04aa1e6f5d17ba41` |
