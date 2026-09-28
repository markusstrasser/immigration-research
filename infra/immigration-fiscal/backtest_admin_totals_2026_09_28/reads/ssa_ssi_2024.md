# SSA, SSI payments by state, 2024: quoted titles, notes and totals

Files (hashes in `derived/sources.json`), downloaded 2026-09-28 through a browser session because SSA refuses
scripted requests:

- `_cache/ssa_supplement2025_7b.xlsx`, from `https://www.ssa.gov/policy/docs/statcomps/supplement/2025/7b.xlsx`
  (Annual Statistical Supplement 2025, SSI state tables);
- `_cache/ssa_ssi_asr24.xlsx`, from `https://www.ssa.gov/policy/docs/statcomps/ssi_asr/2024/ssi_asr24.xlsx`
  (SSI Annual Statistical Report 2024).

Row numbers are 0-based worksheet rows as `openpyxl` reads them. Blank cells are dropped from the quoted rows.

## Table 7.B7 (the primary target and the federal-only secondary)

> 7.B SSI: State Data
>
> Table 7.B7—Total federally administered payment amounts, by type of payment and state or other area, 2024 (in
> thousands of dollars)
>
> State or area | Total | Federal SSI | Federally administered state supplementation
>
> All areas | 63079493 | 59665127 | 3414366
>
> California | 10966403 | 7710463 | 3255939
>
> Texas | 4585186 | 4585186 | . . .

(sheet `7.B7`, rows 0–3, 8 and 47)

> SOURCE: Social Security Administration, Office of Financial Policy and Program Integrity; and Social Security
> Administration, Supplemental Security Record, 100 percent data.
>
> NOTES: Totals do not necessarily equal the sum of rounded components.
>
> SSI = Supplemental Security Income; . . . = not applicable.

(rows 59–61)

"All areas" also holds the one outlying area, "Northern Mariana Islands | 9933 | 9933 | . . ." (row 56). The
51-area sums are $63,069,561k in total, $59,655,194k federal
and $3,414,366k supplementation [DATA: derived/target_national.csv]. California holds $3,255,939k of the
supplementation, 95.4% [DATA: derived/targets.csv, ssa_ssi_supplement_2024].

## Tables 10 and 11 (the December secondary: recipients × average payment)

> Federally Administered Payments
>
> Table 10. Recipients, by state or other area, eligibility category, and age, December 2024
>
> All areas | 7423856 | 1190660 | 63747 | 6169449 | 1002887 | 3951866 | 2469103
>
> California | 1114706 | 347643 | 13857 | 753206 | 84110 | 440414 | 590182

(sheet `Table 10`, rows 0–1, 4 and 9; the first number is the total)

> Federally Administered Payments
>
> Table 11. Average monthly payment, by state or other area, eligibility category, and age, December 2024 (in
> dollars)
>
> All areas | 696.7 | 564.14 | 724.61 | 722.03 | 812.54 | 743.12 | 575.59
>
> California | 813.82 | 687.8 | 901.98 | 870.36 | 897.03 | 919.67 | 723.01

(sheet `Table 11`, rows 0–1, 4 and 9)

> SOURCE: Social Security Administration, Supplemental Security Record, 100 percent data.

(both sheets, row 60)
