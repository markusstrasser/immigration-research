# Brief: is each Mexican arrival cohort less crime-prone than the last? (Butcher–Piehl on our data)

Date: 2026-09-23. Operator question, verbatim: "Selection is the main explanation. Butcher & Piehl
found each recent cohort more positively selected than the last. Americans who move between states
show the same pattern. -- can we see that in our data?"

The quoted sentences are from our own earlier chat answer and are UNVERIFIED. Check them first.

## Deliverables (in this directory only; do not edit any other file; do not commit)

1. `RESULT.md` opening with `**Verdict:**` (plain prose, short, numbers with sources), then method,
   tables, limits, reproduce commands. Tags: `[SOURCE: …]`, `[DATA: …]`, `[CALCULATION: …]`,
   `[INFERENCE]`, `[UNVERIFIED]`.
2. Scripts plus `derived/*.csv` tables (aggregates only). Microdata and API pulls go in `_cache/`
   (ignored: add a `.gitignore` with `_cache/`). IPUMS microdata must never be committed.
3. Return the RESULT.md path and ≤10 lines.

## Part 1: primary-text check (do this first)

- Butcher & Piehl, "Why are Immigrants' Incarceration Rates so Low? Evidence on Selective
  Immigration, Deterrence, and Deportation", NBER w13229 (2007). Quote verbatim what they say about
  successive arrival cohorts ("increasingly positive selection"?) and whether they compare natives
  who move between states. If the interstate-migrant sentence is not in this paper, search their
  1998 papers (ILR Review; JPAM "Recent immigrants: unexpected implications for crime and
  incarceration") and report where, if anywhere, it is supported. Use the research MCP
  (`fetch_paper`, `read_paper`) or Exa. State plainly if our earlier sentence is unsupported.

## Part 2: institutionalization by arrival cohort, Mexico-born men

Estimand: share institutionalized among Mexico-born men aged 18–40 by arrival cohort, at fixed years
since migration (0–5, 6–10, 11–15), across survey years. Ratio to US-born men of the same ages:
all US-born, US-born non-Hispanic white, US-born Mexican-origin. Survey-weighted, with SEs (ACS:
80 replicate weights; census: design-based or binomial with the design-effect note).

Data:
- ACS 1-year PUMS 2006–2024 (skip 2020, experimental) via the Census API: `TYPEHUGQ` (2 =
  institutional group quarters), `POBP` (303 = Mexico), `YOEP`, `AGEP`, `SEX`, `HISP`, `RAC1P`,
  `PWGTP` + `PWGTP1..80`. Key: `set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a`.
  NEVER print the key; pipe any output that may echo a URL through
  `sed -E 's/key=[A-Za-z0-9]+/key=<KEY>/g'`. The API truncates large responses silently: pull by
  state or verify row counts against published totals.
- 1980/1990/2000 5% census: the held IPUMS panel (`immigration_microdata.duckdb`,
  `ipums_usa_borjas_panel`) has NO group-quarters variable. Submit a new IPUMS USA extract through
  the IPUMS API (`IPUMS_API_KEY` in the same config file; pattern:
  `infra/immigration-fiscal/acquire/ipums_cps_second_gen.py`) with YEAR, PERWT, GQ, GQTYPE,
  GQTYPED, AGE, SEX, BPL, BPLD, YRIMMIG, HISPAN, RACE, CITIZEN for samples us1980a, us1990a,
  us2000a (5%) and, if cheap, ACS 2006–2024. Men 18–40 only is fine if the API supports case
  selection; otherwise filter after download. If the extract is refused or queued for hours, do not
  block: finish the ACS part and say so.

Known traps (from this repo; respect them):
- Immigration detention: ICE detainees are counted in institutional GQ, which inflates
  foreign-born rows, most of all recent arrivals. Public ACS PUMS cannot separate them. Report the
  foreign-born rates as upper bounds for crime, and use the 1980–2000 GQTYPED detail to show the
  correctional-only share where available.
- Definitions change: the repo's 2000 figure counted correctional institutions only, while the later
  series counts every institution. Keep one definition across years (all institutions) and show the
  correctional-only series separately where the detail exists.
- Deportation removes offenders from the foreign-born stock (a channel Butcher and Piehl test), and
  census undercounts of the unauthorized differ by cohort. Both bias cohort comparisons; discuss them.
- Composition: report cohort ratios with age held within 18–40 and, if cell sizes allow, education
  at arrival held fixed.

## Part 3: US-born interstate movers vs stayers

US-born men 18–40, ACS 2019, 2023 and 2024: institutional share for those living outside their
state of birth vs in it, by race/ethnicity (NH white, NH Black, Hispanic). Caveat: prison location is
not pre-prison residence (federal prisoners are placed out of state), which pushes movers' rates up.
Say whether the data show movers less institutionalized.

## Existing work to build on (read before computing; do not redo)

- `research/immigration-mexican-origin-generation-incarceration-2026-09-16.md` and
  `infra/immigration-fiscal/acs_institutional_2026_09_16/` (generation series, API patterns)
- `research/immigration-detention-crime-and-fiscal-scope-2026-09-20.md` (custody/crime measurement rule)
- `research/immigration-mexican-arrival-cohorts-2026-09-18.md` (cohort definitions, entry quality)
- `research/immigration-crime-rates-unauthorized-vs-native-born.md` and ladder 144 (Texas arrest rates)

## Run conventions

`OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>` from the repo root. Scripts over 10
lines live in files here. Report every specification you computed, not only the favourable ones.
Before finishing, re-run every script from a clean `derived/` and confirm the tables reproduce.
