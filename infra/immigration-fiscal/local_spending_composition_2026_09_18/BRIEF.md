# Lane: does local spending shift from education toward police and corrections where the Hispanic or foreign-born share rises? (2026-09-18)

## Goal
Extend ladder 141 (school flight lane: within state-year, a 10-point rise in a district Hispanic share lowers local school revenue, state aid offsets most of it) from revenue to the composition of local spending. Tabarrok endorsed a paper on 2023-12-02 stating that unauthorized inflows "reduce local public spending, and shift it away from education towards law-and-order"; the archived post with its link is in `infra/immigration-fiscal/mr_archive_2026_09_18/derived/mr_posts.jsonl` (url contains `2023/12/immigration-backlash`). Identify the paper, read its design, and test its composition claim on US local government finance.

## Inputs
- Census Annual Survey of State and Local Government Finances / Census of Governments individual unit files (counties and municipalities), 2007, 2012, 2017, 2022 census years plus the annual survey years between; the "Fin_GID" unit files or the Data Base on Historical Finances (Willamette/GovFin) if faster. Cache; use Modal for anything over 100 MB.
- County population by Hispanic origin and nativity: ACS 5-year via the Census API (B03003, B05006, B05002), 2009 onward; 2000 Census SF3 for the pre-period.
- Reuse the school lane design and caveats: `infra/immigration-fiscal/school_flight_2026_09_18/RESULT.md`, `estimate_districts.py`, `derived/metro_school_panel.csv`.

## Estimation
County-level (aggregate all local units inside a county, including the county government, municipalities and school districts, so composition is total-local). Outcomes: shares of total local direct expenditure on education, police, corrections, public welfare, health and hospitals, highways; and per-capita real levels. Regressor: change in Hispanic share and in foreign-born share (and Mexico-born where B05006 supports it). Within state-year, long differences 2007→2022 and 2012→2022, population-weighted and unweighted, with and without the school-lane covariates. Report the composition shift per 10-point share change with clustered SEs. Arms that could reverse it: dropping the largest metros; per-capita levels instead of shares (a denominator-masking check); the pre-period placebo (2000→2007 share change on the 2007→2022 outcome). Do not use the post-2008 shift-share instrument; ladder 136 shows it is dead. Label every estimate descriptive.

## Limits to state
Composition can shift because education spending is state-financed (the school lane finding) rather than because law-and-order rose; separate the two by reporting levels.

## Rules (all lanes)
- Repo root `/Users/alien/Projects/immigration-research`. Own only your lane directory; `_cache/` is gitignored repo-wide; write outputs to `derived/`. Never edit anything under `research/`. Do not commit. Analysis agents do not commit.
- `uv run --no-project --with "pandas>=2" --with "numpy>=2" [--with requests --with lxml --with statsmodels] python3 <script>`; scripts over 10 lines in files; line-based progress; `PYTHONUNBUFFERED=1` for logs. Never use bare `python3` after `&&`.
- Census API key: `CENSUS_API_KEY` in `infra/immigration-fiscal/acquire/config.local.env` (source it; never print it). PUMS API pattern: `https://api.census.gov/data/<year>/acs/acs1/pums?tabulate=weight(PWGTP)&col+<VAR>&ucgid=0400000US<ST>&<VAR>=<a:b>&key=...`. Raw data under `~/research-data` is read-only.
- If census.gov or another host fails under curl (HTTP/2 PROTOCOL_ERROR seen on 2026-09-18), use `curl --http1.1 -C -`; a Modal container is authorized for downloads over 100 MB.
- Every number in your memo carries [SOURCE]/[CALCULATION]/[INFERENCE]/[UNVERIFIED]/[TRAINING-DATA]. Read `CLAUDE.md` and `notes/quant-bias-checklist.md` first. Disconfirmation is mandatory: run at least two arms that could reverse the headline and report them.
- Deliverables: `README.md` (run commands, inputs, outputs), `RESULT.md` opening `**Verdict:**` with counts, arms, what was skipped and why, then a draft memo section the parent can lift (verbatim quotes only from fetched sources). Update RESULT.md after each phase so partial progress survives.
- Verification you must run and report: every script re-run from scratch reproduces `derived/` byte-identically (`git diff --stat -- derived/` empty after the second run, or `cmp`).
- The repo measures resident groups, not admission; the absolute sign is a convention and the gap against same-age whites is not. Do not write policy advice.
