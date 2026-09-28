**Verdict:** Outside the mother role the sex gap in means-tested benefits is small. Adults aged 18–64 with no own child under 18 in the household: women receive about **1.09×** what men receive ($2,144 vs $1,960 a year). The gap is **1.79×** among parents, **1.18×** among childless adults living without a partner, and **1.27×** at 65+. Race differences are larger than sex differences: childless Black adults receive about 1.9× what childless white adults receive, at either sex.

Question (operator, 2026-09-29, prompted by a post about a welfare ad): how much more do women than men get in welfare, outside the mother role?

## Method

CPS ASEC 2025, income year 2024, person file (`pppub25.csv`, 142,125 persons, weighted 337.7M).
[DATA: sources/immigration-fiscal/data/external/stage3/census/cps_asec_2025/asecpub25csv.zip; hash in derived/audit.csv]

- **Welfare** = public assistance (TANF, general assistance) + SSI + an equal per-person share of the SPM unit's SNAP, housing subsidy, WIC, energy assistance and school lunch + Medicaid.
- **Medicaid** is valued at MACPAC FY2023 benefit spending per full-year-equivalent enrollee, national row: child $4,040; disabled (proxied by SSI receipt, 19–64) $27,361; other adult (proxied by parent) $5,757; expansion adult (non-parent) $8,021; aged $20,305. Covered all of 2024 counts one year; covered part of the year counts half (assumption).
[SOURCE: https://www.macpac.gov/wp-content/uploads/2026/01/EXHIBIT-22.-Medicaid-Benefit-Spending-Per-Full-Year-Equivalent-FYE-Enrollee-by-State-and-Eligibility-Group-FY-2023.pdf, "Total" row, parsed with pdftotext]
- **Refundable credits** (EITC, ACTC) are reported in their own column and are not in "welfare".
- **Mother role** = an own child under 18 in the household names the person as parent (PEPAR1/PEPAR2). Women whose children are grown or live elsewhere count as non-parents. Pregnancy is not observed.

## Results

$ a year per person, weighted. Full table: `derived/welfare_by_sex.csv`. [CALCULATION: welfare_by_sex.py]

| Cell | Women | Men | Women/men | Any receipt, W / M |
|---|---|---|---|---|
| 18–64, all | 2,086 | 1,724 | 1.21 | 41% / 36% |
| 18–64, parent of child <18 | 1,970 | 1,100 | 1.79 | 67% / 62% |
| **18–64, no own child <18** | **2,144** | **1,960** | **1.09** | 28% / 26% |
| 18–64, no own child, no partner | 3,057 | 2,589 | 1.18 | 37% / 32% |
| 18–34, no own child, no partner | 2,115 | 1,952 | 1.08 | 39% / 34% |
| 65+ | 1,998 | 1,578 | 1.27 | 19% / 15% |

Among childless adults the sex gap comes mostly from Medicaid (1.09×) and the household benefit share (1.23×). Cash (SSI, TANF) is equal (1.03×).

By race, 18–64 with no own child: white women 1,765 and men 1,663 (1.06×); Black women 3,417 and men 3,123 (1.09×); Hispanic women 2,458 and men 2,092 (1.17×); Asian women 1,326 and men 1,259 (1.05×).

Young (18–34), unpartnered, childless adults:
- White men: 12.05M people, $1,584 a year, 27% with any receipt, so about 3.3M recipients.
- Black women: 3.15M people, $2,977 a year, 47% with any receipt, so about 1.5M recipients.

Per head, the Black women receive 1.9× as much. By headcount, there are twice as many white male recipients in this cell. [CALCULATION: pop_m × any_share]

## Known biases

- **Under-reporting.** The survey's totals are SNAP $46bn, SSI $59bn and public assistance $7.6bn, with Medicaid valued at $456bn. Program records are roughly SNAP ~$100bn, SSI ~$65bn and Medicaid benefits ~$850bn. [TRAINING-DATA, not verified here] So dollar levels are too low, SNAP and Medicaid by about half. The women/men ratio is biased only if under-reporting differs by sex. No such evidence was checked.
- **Equal split within the unit.** SNAP and housing are split equally within the SPM unit. For couples this forces equal amounts, which pulls the sex ratio toward 1. The unpartnered cells avoid this: 1.18× at 18–64.
- **Medicaid priced by group, not by sex.** Each eligibility group gets the same cost for both sexes, so the Medicaid ratio reflects enrollment only.
- **Disability proxied by SSI.** Disabled Medicaid enrollees without SSI are priced as expansion adults, which undervalues them.
