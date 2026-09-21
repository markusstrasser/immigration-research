# Seven papers from the Marginal Revolution archive, read in full

**Verdict:** None of the seven changes the account's headline. Two identify benefits the account
omits: a nursing-home channel bounded at $2.3–14.9bn a year of Medicaid spending for the
Mexico-born, and native–immigrant complementarity, which the production term assumes away.
Memo: [`research/immigration-marginal-revolution-leads-read-2026-09-21.md`](../../../research/immigration-marginal-revolution-leads-read-2026-09-21.md).

## Contents

- `BRIEF.md`: the reading protocol every reader agent followed (primary PDF, `pdftotext -layout`,
  whole text, a page or table reference and verbatim quote for every number).
- `notes/<slug>.md`: one set of reading notes per paper: a model self-report line, then `**Verdict:**`.
  The parent session re-checked the decisive numbers of every note against the cached text.
- `pull_acs_care.py`: ACS 2024 one-year PUMS tabulations (direct-care workforce by birthplace and
  origin, the Butcher–Moran–Watson treatment population, elderly by housing type).
- `elder_care_bound.py`: applies the Butcher–Moran–Watson coefficients to the 2024 Mexico-born
  share and prices the result with CMS national health expenditure Table 15.
- `derived/acs_care_inputs.csv`, `derived/elder_care_bound.csv`: tracked outputs.
- `_cache/` (ignored): the seven PDFs and their text, CMS `nhe-tables.zip`, raw ACS responses.

## Reproduce

```sh
# from the repository root; the key is read from the environment and never printed
set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
uv run --no-project python3 infra/immigration-fiscal/mr_leads_papers_2026_09_21/pull_acs_care.py
curl -sL -o infra/immigration-fiscal/mr_leads_papers_2026_09_21/_cache/nhe-tables.zip \
  https://www.cms.gov/files/zip/nhe-tables.zip   # then unzip into _cache/nhe_tables/
uv run --no-project --with openpyxl python3 infra/immigration-fiscal/mr_leads_papers_2026_09_21/elder_care_bound.py
```

Pins: CMS `nhe-tables.zip` SHA256 `a09ef6d3e84e25d745047a47b6b08a0d96b303085b4c725b67ce67a0eb0c4420`
(1970–2024 tables; the script refuses another file). BEA compensation of employees comes from
`sources/immigration-fiscal/data/external/bea_nipa/Section1All_xls.xlsx`, Table 1.10, SHA256
`238ba851c9a4932d91a0dedb1b3f2e6c6d37574d154a54267da18b9cb0921a19`.

## Census API notes

National PUMS tabulations take no geography clause (`&for=us:1` returns HTTP 400). A variable used
only as a filter takes a comma list or a range (`ESR=1,2,3`, `AGEP=16:64`); several occupation
codes must be repeated (`&OCCP=3601&OCCP=3602`), and a filtered variable cannot also be a row.

## Limits

The elder-care figure is a bound, not an estimate: the coefficient comes from 1980–2000 variation
of 3.3 points and is applied to a 3.45-point share; it loses significance with year-by-state
effects; CMS nursing-facility totals include residents under 65; no offset is taken for Medicaid
home-care spending on people who stay at home. The papers were read by subagents; figures that
exist only as images were not used for any number.
