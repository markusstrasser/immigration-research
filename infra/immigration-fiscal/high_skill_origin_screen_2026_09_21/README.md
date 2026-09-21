# High-education origin screen

**Verdict:** see [`RESULT.md`](RESULT.md). No high-education birthplace group is clearly negative;
the Philippines-born sit at zero for an age reason, and degree holders from Venezuela, Pakistan
and Bangladesh pay far less than native degree holders.

## Contents

- `screen.py`: runs `education_origin_fiscal_2026_09_19/builder.py` unchanged with 19 birthplace
  groups (codes from `cpsmar25.pdf` Appendix J) and summarises adults 25+, 25–64 and 65+ with the
  builder's own CPS-replicate and MEPS uncertainty. `mexico_born` stays in the list because the
  builder validates its legacy anchor on it. Raw builder tables go to the ignored
  `_cache/builder/`; `derived/origin_screen.csv` is tracked.
- `acs_screen.py`: ACS 2024 one-year PUMS tabulations by birthplace (foreign-born only): degree
  share, age, employment, poverty, SSI, Medicaid, public assistance, Social Security receipt and
  high earners, for the 68 birthplaces with at least 100,000 residents. Reuses `fetch` and
  `cells` from `mr_leads_papers_2026_09_21/pull_acs_care.py`. Output:
  `derived/acs_origin_screen.csv`.

## Reproduce

```sh
# from the repository root; about three minutes
OPENBLAS_NUM_THREADS=1 uv run --no-project --with numpy --with pandas --with openpyxl \
  python3 infra/immigration-fiscal/high_skill_origin_screen_2026_09_21/screen.py
# re-summarise without rebuilding: add --summarise-only
set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a   # key is never printed
uv run --no-project python3 infra/immigration-fiscal/high_skill_origin_screen_2026_09_21/acs_screen.py
```

The builder verifies the September 19 ledger's input hashes before it runs and records every
source hash, including this lane's origin codes, in `_cache/builder/manifest.json`.

## Census API notes

`row+POBP` returns all 222 birthplace codes in one call; value labels come from
`…/acs/acs1/pums/variables/POBP.json` (no key needed). Range filters work on dollar variables
(`SSIP=1:99999`, `PINCP=100000:9999999`) as they do on `AGEP`. ACS `POBP` and CPS `PENATVTY`
share the Census country list, but check each code against its own codebook: 217 is Korea and
218 Kazakhstan in both.
