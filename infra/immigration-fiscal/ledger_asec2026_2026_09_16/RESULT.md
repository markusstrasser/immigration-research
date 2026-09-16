Model self-report: Opus 5 (1M context) — claude-opus-5[1m]

**Verdict:** STABLE. The Mexican-second-generation fiscal gap reproduces on CPS ASEC 2026
(income year 2025) and moves by less than one standard error on both headline measures.
Taxes minus selected transfers goes from −6,066 (se 353) to −6,499 (se 489), a change of
−434 against a 603 standard error of the change (0.72 se). The extended balance goes from
−8,286 (se 443) to −8,727 (se 594), a change of −441 against 741 (0.60 se). Pooled two-year
estimates: **−6,282 (se 301)** and **−8,507 (se 371)**.

[DATA] [INFERENCE] [SOURCE: https://www2.census.gov/programs-surveys/cps/datasets/2026/march/asecpub26csv.zip]

---

## 1. Step-1 gate — PASS

Re-ran the published ledger on the ASEC 2025 file before touching 2026. Both headline
numbers reproduce to the dollar.

| quantity | this run | published | deviation |
|---|---|---|---|
| taxes minus selected transfers, Mexican 2nd gen − 3rd+ NH white | −6,066 (se 353) | −6,066 (se 353) | +0.17 |
| extended balance, same contrast | −8,286 (se 443) | −8,286 (se 443) | −0.23 |

Cut: `equal_all_members` allocation, person weights, adults 25–64, civilian household
members, 160-replicate SDR. Published in `research/immigration-mexican-origin-by-generation-2026-09-16.md`
§5 and the peer lane `gen_ledger_extension_2026_09_16/`.

## 2. Layout changes found on ASEC 2026

**One ledger input was removed.** `SPM_BBSUBVAL` (SPM broadband subsidy resource, the
Affordable Connectivity Program) is not on the 2026 public-use file. The program lapsed
2024-06-01. Thirteen person-file columns were dropped in total; the other twelve are the
`M5G*` one-year-ago migration block, which this ledger does not use. No columns were added.

I did not substitute a value. Instead both years were re-run on a four-item non-cash set
(SNAP, energy, WIC, school lunch) so the year contrast is clean, and the 2025 five-item
run is retained as the published gate. The item is negligible: broadband contributes
**$1–2 per adult per year** in every one of the six groups, so dropping it moves the
2025 gap by about a dollar.

**`PEINUSYR` was recoded and this is a trap for other callers.** ASEC 2025 top code 28
means "2022–2024". ASEC 2026 splits it: 28 = "2022–2023" and a new code 29 = "2024–2026".
Empirically, code 28 holds 7.04M weighted persons on the 2025 file, and on the 2026 file
28 holds 4.90M with another 3.19M in code 29. `analyze_cps_fiscal_2025.py` defines its
`foreign_born_entry_2022_2024` group as `PEINUSYR.eq(28)`; pointed at ASEC 2026 that
expression silently drops 3.19M recent arrivals and must become `PEINUSYR.isin([28, 29])`.
**No number in this lane is affected** — that group is not one of the six extended-ledger
groups.

Everything else the ledger depends on is unchanged: `PRCITSHP`, `PRDTHSP` (1 = Mexican),
`PEHSPNON`, `PRDTRACE`, `PRPERTYP`, and every tax-model field. Birthplace country codes
are unchanged, verified empirically rather than from the dictionary, which carries no
inline country list: `PENATVTY == 303` gives 12.6M Mexico-born in 2025 and 11.5M in 2026,
and the both-parents-US-born population is 240.2M in both years. Details in
`layout_check.txt`.

All of the generator's identity gates pass on the 2026 file: the federal refundable-credit
identity, constant SPM unit fields, exactly one head per unit, unit size agreement, the
SPM weight matching the head's full weight, and person tax sums reproducing `SPM_FEDTAX`
and `SPM_FICA`. The 2026 sample is 5.2% smaller (134,729 person records and 55,401 SPM
units, against 142,125 and 58,147), which is why the 2026 standard errors are wider.

## 3. Side by side, six groups

Annual dollars per adult 25–64. Left column is the 2025 file (income year 2024), right is
the 2026 file (income year 2025). Both on the four-item non-cash basis at 2024 parameters.

| group | taxes | cash transfers | non-cash | taxes − transfers | extended balance |
|---|---|---|---|---|---|
| 3rd+ NH white | 14,383 → 14,864 | 2,453 → 2,367 | 144 → 136 | 11,786 → 12,361 | 15,986 → 16,816 |
| all native | 13,110 → 13,487 | 2,451 → 2,437 | 186 → 175 | 10,473 → 10,875 | 14,267 → 14,898 |
| all 2nd gen | 13,653 → 14,250 | 1,823 → 1,875 | 166 → 150 | 11,664 → 12,225 | 15,659 → 16,632 |
| Mexican 2nd gen | 7,419 → 7,738 | 1,460 → 1,648 | 239 → 228 | 5,720 → 5,862 | 7,700 → 8,089 |
| Mexican 3rd+ self-id | 9,149 → 8,899 | 2,049 → 2,130 | 230 → 231 | 6,870 → 6,538 | 9,707 → 9,273 |
| Mexico-born | 4,874 → 5,514 | 860 → 949 | 245 → 213 | 3,770 → 4,353 | 4,463 → 5,518 |

Standard errors for every cell are in `ledger_2025_vs_2026_result.txt` and
`ledger_2025_vs_2026.csv`.

## 4. Differences from 3rd+ NH white, and the pooled estimate

Taxes minus selected transfers:

| group | ASEC 2025 | ASEC 2026 | change / se | pooled |
|---|---|---|---|---|
| all native | −1,313 (106) | −1,486 (120) | 1.09 | −1,399 (80) |
| all 2nd gen | −122 (413) | −136 (455) | 0.02 | −129 (307) |
| Mexican 2nd gen | −6,066 (353) | −6,499 (489) | 0.72 | −6,282 (301) |
| Mexican 3rd+ self-id | −4,916 (456) | −5,823 (563) | 1.25 | −5,370 (362) |
| Mexico-born | −8,016 (338) | −8,008 (393) | 0.02 | −8,012 (259) |

Extended balance:

| group | ASEC 2025 | ASEC 2026 | change / se | pooled |
|---|---|---|---|---|
| all native | −1,718 (124) | −1,919 (142) | 1.06 | −1,819 (94) |
| all 2nd gen | −327 (488) | −184 (540) | 0.20 | −255 (364) |
| Mexican 2nd gen | −8,286 (443) | −8,727 (594) | 0.60 | −8,507 (371) |
| Mexican 3rd+ self-id | −6,279 (546) | −7,543 (661) | 1.47 | −6,911 (429) |
| Mexico-born | −11,522 (402) | −11,298 (489) | 0.35 | −11,410 (317) |

Pooled estimates are the simple average of the two years with
se = sqrt(se₂₀₂₅² + se₂₀₂₆²)/2, as the brief specifies.

**The independence assumption is optimistic.** Consecutive March ASEC samples share roughly
half their households through the CPS 4-8-4 rotation. Real correlation between the two
years is positive, which means the pooled standard errors above are too small and the
standard errors of the year-to-year change are too large. The "within 1 se" stability test
therefore runs in the conservative direction — it is easier to pass than it should be.
Treat the pooled se as a lower bound. [INFERENCE]

## 5. Two component contrasts that did move

Out of 45 group-by-metric year comparisons, three exceeded two standard errors of the
change. With that many comparisons roughly two are expected by chance, so I do not read
these as established shifts, but they are where the instability sits:

- Employer payroll tax gap for Mexican 3rd+ self-identified: −637 → −852, 2.27 se.
- K-12 charged for all second generation: +204 → +19, 2.64 se. The second-generation
  child load fell sharply on the 2026 file.
- K-12 charged for Mexico-born: +660 → +453, 2.15 se, the same direction.

Falling K-12 child load among the foreign-born and second generation is the one pattern
that repeats across groups and would be worth a direct look at children-per-adult rather
than the dollar aggregate. [INFERENCE]

## 6. Parameters

The 2026 run keeps the 2024 parameter set exactly as the 2025 run uses it: state combined
sales tax rates, effective property tax rates, ACS 2023 median gross rent, FY2024 per-pupil
current spending, ITEP quintile rates, and the ACS 2024 pupil ratio. Nominal income grew
between the income years while per-pupil cost and rent are held fixed, so the K-12 and
renter items are understated in real terms on the 2026 file.

One parameter was updated as a reported sensitivity rather than in the headline: the
employer OASDI wage base, $168,600 for 2024 and $176,100 for 2025.
[SOURCE: https://www.irs.gov/pub/irs-prior/p15--2024.pdf]
[SOURCE: https://www.irs.gov/pub/irs-prior/p15--2025.pdf — "The social security wage base
limit is $176,100."] The effect is immaterial: it raises employer payroll tax by $23 per
adult for 3rd+ NH white and $8 for Mexican second generation, moving the extended-balance
gap by about $15. Both values are in the CSV as `estimate_asec2026_oasdi2025cap`.

## 7. Method

`ledger_asec2026.py` calls the existing code rather than re-implementing it. It imports
`analyze_cps_fiscal_2025.prepare/allocate/estimate/summarize` and `extend_ledger.build`,
and switches income years by remapping the zip member names those modules open
(`pppub25.csv` → `pppub26.csv`, `hhpub25.csv` → `hhpub26.csv`,
`asec_csv_repwgt_2025.csv` → `asec_csv_repwgt_2026.csv`). No analytic code is copied. The
peer lane's output directory is left untouched; `extend_ledger.HERE` is repointed here and
`state_parameters.csv` is copied in.

## 8. Sources and artifacts

- CPS ASEC 2026 public-use CSV, sha256 `fe819d0d2fc4470c282e76c247b8aa8b6054811619730307e9f2fe6186707d93`,
  139,103,894 bytes, members `hhpub26.csv ffpub26.csv pppub26.csv asec_csv_repwgt_2026.csv`.
  The replicate weights ship inside the same zip, as in 2025.
  [SOURCE: https://www2.census.gov/programs-surveys/cps/datasets/2026/march/asecpub26csv.zip]
- CPS ASEC 2025 public-use CSV, sha256 `318845a2b5e0034eb2973898de1738f4df0025727de38499e7669cb9c0deef0b`,
  read from the existing SSD stage.
- ASEC 2026 data dictionary.
  [SOURCE: https://www2.census.gov/programs-surveys/cps/datasets/2026/march/asec2026_ddl_pub_full.pdf]
- `ledger_2025_vs_2026.csv` — 54 rows, six groups by nine metrics, both years, the OASDI
  sensitivity, differences from 3rd+ NH white with SDR standard errors, and pooled values.
- `ledger_2025_vs_2026_result.txt` — full printed tables.
- `layout_check.txt` — the empirical code positive control and dictionary comparison.

## 9. Verification

```
cd /Users/alien/Projects/immigration-research && uv run python3 \
  infra/immigration-fiscal/ledger_asec2026_2026_09_16/ledger_asec2026.py
```

Exit code 0. Console excerpt:

```
Person-file columns dropped 2025 -> 2026 (13): ['I_M5G1', 'I_M5G2', 'I_M5G3', 'M5GSAME',
 'M5G_CBST', 'M5G_DIV', 'M5G_DSCP', 'M5G_MTR1', 'M5G_MTR3', 'M5G_MTR4', 'M5G_REG',
 'M5G_ST', 'SPM_BBSUBVAL']
Person-file columns added   2025 -> 2026 (0): []
Ledger fields absent from the 2026 person file: ['SPM_BBSUBVAL']

  Mexican 2nd gen minus 3rd+ NH white, taxes minus selected transfers: -6,066 (se 353)
    published: -6,066   deviation: +0.17
  Mexican 2nd gen minus 3rd+ NH white, extended balance: -8,286 (se 443)
    published: -8,286   deviation: -0.23
  GATE PASS --- both headline numbers within $50 of the published values.

[run]   validation: {"person_rows": 134729, "replicate_rows": 134729, "spm_units": 55401,
 "max_full_weight_difference": 0.005049899999903573, "negative_replicate_weights": 0,
 "federal_credit_identity": true, "unit_fields_constant": true,
 "source_tax_sums_match_unit_fields": true}

  taxes minus selected transfers
    ASEC 2025 (IY2024): -6,066 (se 353)
    ASEC 2026 (IY2025): -6,499 (se 489)
    change: -434   se of change (independent): 603   |change|/se = 0.72   -> WITHIN 1 se
    pooled two-year: -6,282 (se 301)
  extended balance
    ASEC 2025 (IY2024): -8,286 (se 443)
    ASEC 2026 (IY2025): -8,727 (se 594)
    change: -441   se of change (independent): 741   |change|/se = 0.60   -> WITHIN 1 se
    pooled two-year: -8,507 (se 371)
```

Nothing was committed. No file outside this directory was modified.
