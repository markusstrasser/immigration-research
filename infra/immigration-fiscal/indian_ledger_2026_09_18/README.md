# Lane: Indian-origin residents on the repo's fiscal ledger and ACS profile (2026-09-18)

Three scripts, three independent outputs. Nothing outside this directory is written or edited;
the upstream ledger lanes are imported, never modified.

## Run

```bash
cd infra/immigration-fiscal/indian_ledger_2026_09_18

# 1. CPS ASEC ledger (imports gen_ledger_extension_2026_09_16/extend_ledger.py and
#    build/analyze_cps_fiscal_2025.py; MEPS 2024 adds the public-paid health component)
uv run --no-project --with "pandas>=2" --with "numpy>=2" python3 ledger_india.py

# 2. Gate: the white reference must equal the upstream lane's figure (exit 0 = PASS)
uv run --no-project --with "pandas>=2" python3 gate_white_reference.py

# 3. ACS 2023 1-year PUMS profile
uv run --no-project --with "pandas>=2" --with "numpy>=2" python3 acs_profile.py

# 4. Entry class: DHS/OHSS Yearbook LPR Table 10 FY2020-FY2024 + nonimmigrant Tables 29/33
uv run --no-project --with "pandas>=2" --with "numpy>=2" --with openpyxl python3 entry_class.py
```

## Inputs

| Input | Where | Notes |
|---|---|---|
| CPS ASEC 2025 public-use zip | `../gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip` | sha256 `318845a2…`, the file the upstream lane used |
| MEPS 2024 full-year consolidated | `~/research-data/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip` + `h256su.txt` | read-only raw tree; drives the public-paid health component |
| CPS March 2025 data dictionary | `_cache/cpsmar25.pdf` | country codes verified here (Appendix J: India 210, China 207) |
| ACS 2023 1-year PUMS person | `~/research-data/immigration-fiscal/data/census/acs_pums_2023_person.zip` | the 2023 vintage names the state column `STATE`, the 2024 vintage `ST`; the loader handles both |
| ACS 2023 1-year PUMS household | `~/research-data/immigration-fiscal/data/census/acs_pums_2023_household.zip` | `HINCP`, `WGTP` for the household-level items |
| ACS PUMS data dictionary 2023 | `_cache/PUMS_Data_Dictionary_2023.csv` | occupation/industry labels; `VAL` rows put the label in field 6 |
| DHS/OHSS Yearbook workbooks | `_cache/yearbook_lpr_fy20*.xlsx`, `_cache/yearbook_nonimmigrants_fy2024.xlsx` | downloaded by `entry_class.py`, URLs + sha256 in `derived/entry_class_sources.json` |

`_cache/` is gitignored repo-wide. Raw data under `~/research-data` is read-only and is only read.

## Outputs (`derived/`)

| File | What |
|---|---|
| `india_ledger_long.csv` | universe × allocation × weighting × arm × group × metric, estimate, SDR se, difference from the white reference and its se |
| `india_ledger_result.txt` | printed ledger tables, arms, sensitivities, own-person descriptives |
| `acs_profile_2023.csv` / `acs_profile_2023_result.txt` | ACS profile, long form and printed |
| `entry_class.csv` / `entry_class_result.txt` / `entry_class_sources.json` | India's share of each admission class, and the cached-source manifest |

## Verification

* `gate_white_reference.py` compares nine white-reference metrics against
  `../gen_ledger_extension_2026_09_16/extended_ledger_by_generation.csv` at a $1.00 tolerance
  and checks the cell n. It exits non-zero on any mismatch.
* Every script is deterministic: a second run from scratch reproduces `derived/` byte-identically
  (checked with `cmp`; results in `RESULT.md`).

## Known limits

* The 2026 ASEC recodes `PEINUSYR`; this lane pools only ASEC 2025, the year the upstream ledger
  pools, so that trap is not hit here.
* `PEPAR1`/`PEPAR2` are parent *line numbers* (the `PPPOS = PEPAR + 40` pointer trap). This lane
  never needs them: `PEFNTVTY`/`PEMNTVTY` carry each person's own parents' birthplaces, so the
  second generation is identified without following a pointer.
* The MEPS donor model classifies birthplace only as US/not-US; India-specific medical cost is
  modeled, not measured.
