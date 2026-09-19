# Pupil exposure and Texas tax checks

Run from the canonical repository (or supply `--source-root`):

```sh
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project \
  --with numpy --with pandas python3 infra/immigration-fiscal/admin_school_checks_2026_09_19/builder.py
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project \
  --with numpy --with pandas python3 -m unittest discover -s infra/immigration-fiscal/admin_school_checks_2026_09_19
```

The canonical March2025 CPS child population and fixed public-enrollment factor
are compared with direct ACS2024 household child/enrollment cells. Both surveys'
replicate weights are retained for conditional count standard errors. The factor
was originally estimated from ACS native-adult household exposure, so this tests
its transport to unused child/state cells; it is not a new independent source.
ACS uses the 2024 `STATE` column, not the older `ST` schema; unexpected fields,
source hashes and row counts fail loudly. The school boundary regression excludes
private/home school, preschool and college; only public grades K–12 count.

The administrative grade bridge separately compares all-age ACS public K–12
with CDE/TEA fall membership after removing TK/EE/pre-K. Annual-average versus
fall timing, households versus group quarters, and TK classification remain
differences. No grade-based control is treated as exactly age5–17. Primary
transcribed cells, locators, dates and source links are in `sources.json`.

Two uniform-rate scenarios replace the fixed pupil share with the ACS all-child
or Hispanic-child share. They scale operating school costs, capital/interest and
district differentials together. These are transparent sensitivities, not a
Mexican-origin re-estimate; the original allocation and dollars stay unchanged.
Lunch reversal stays fixed because it prevents overlap with school expenditure.

Texas's no-individual-income-tax check verifies every current civilian record's
`STATETAX_A`, not only its aggregate. This passes for the held release; a future
failure would need investigation of migration, source coding and tax residency.
All outputs and caches are derived and ignored. No public API is changed.
