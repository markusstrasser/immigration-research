# SSA, OASDI Beneficiaries by State and County, 2024: quoted title, notes and totals

File (hash in `derived/sources.json`): `_cache/ssa_oasdi_sc24.xlsx`, from
`https://www.ssa.gov/policy/docs/statcomps/oasdi_sc/2024/oasdi_sc24.xlsx`, downloaded 2026-09-28 through a
browser session because SSA refuses scripted requests.

Row numbers are 0-based worksheet rows as `openpyxl` reads them. Blank cells are dropped from the quoted rows.

> Table 3. Amount of benefits in current-payment status, by state or other area, type of benefit, and sex of
> beneficiaries aged 65 or older, December 2024 (in thousands of dollars)
>
> State or area | Total | Retirement | Survivors | Disability | Aged 65 or older
>
> Retired workers | Spouses | Children | Widow(er)s and parents | Children | Disabled workers | Spouses | Children |
> Men | Women
>
> All areas | 125577970 | 102268471 | 1732599 | 655088 | 6617163 | 2324891 | 11430894 | 37105 | 511758 | 54368713 |
> 53474772
>
> California | 11859914 | 9908872 | 223279 | 74601 | 610120 | 195523 | 809201 | 3701 | 34619 | 5334969 | 5141238
>
> Texas | 8561812 | 6852551 | 167625 | 46052 | 542492 | 191883 | 721909 | 2994 | 36305 | 3810959 | 3517600

(sheet `Table 3`, rows 0–3, 8 and 47)

> SOURCES: Social Security Administration, Master Beneficiary Record, 100 percent data; and U.S. Postal Service
> geographic data.

(row 65)

The target is the Total column for the 50 states and DC: $123,837,872k a month [DATA: derived/target_national.csv].
"All areas" also holds the outlying areas (rows 56–60), "Foreign countries" (row 61) and "Unknown" (row 62),
$1,740,098k together [CALCULATION: 125,577,970 − 123,837,872].
