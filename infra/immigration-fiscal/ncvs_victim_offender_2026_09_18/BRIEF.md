# Lane: who is hurt by violent crime, by group, beyond homicide (2026-09-18)

## Goal
Ladder 143 built the victim × offender ethnicity matrix for cleared homicides (Hispanic offender → Hispanic victim 0.72 on ethnicity-known cases, 0.67 under joint imputation; white → white 0.81; Black → Black 0.81) and found the inter-group cost transfer small next to prison cost. Extend it to all violent victimization with the National Crime Victimization Survey, which records the victim own Hispanic origin and the offender Hispanic origin as perceived by the victim (since 2012). Read `research/immigration-homicide-victim-offender-and-treasury-cost-2026-09-18.md` and `infra/immigration-fiscal/homicide_cost_2026_09_18/RESULT.md` first so the matrices are comparable.

## Data routes, in order
1. NCVS public-use concatenated incident file at NACJD/ICPSR (search "NCVS concatenated file 1992-2023", ICPSR 38963 or its successor). ICPSR downloads may require a free account; try the direct download and the "Download without login" route if offered; if a login wall blocks you, stop that route and say so (do not create accounts).
2. BJS NCVS Dashboard (N-DASH) CSV export with victim Hispanic origin × offender Hispanic origin for violent victimization, and the BJS "Criminal Victimization" annual report tables (victim-offender race and Hispanic origin), 2017–2023. Cache every file.
3. BJS special report "Race and Hispanic Origin of Victims and Offenders, 2012-15" (NCJ 250747) for the published matrix as a check.

## Outputs
Pooled 2017–2023 (or the widest available window): (a) victim ethnicity × offender ethnicity matrix for violent victimization, serious violent, and simple assault separately, with NCVS weights and, where the microdata route works, generalized-variance SEs; (b) the same restricted to single-offender incidents (comparable to the SHR restriction); (c) victimization rate per 1,000 by victim ethnicity and by offender ethnicity; (d) the share of Hispanic-offender victimizations with white victims and vice versa; (e) an offense-mix cost weighting with the McCollister unit costs from `infra/immigration-fiscal/crime_cost_2026_09_16/crime_cost.py` (the MCC table), giving cost of victimization per 1,000 by victim group and the inter-group cost transfer per capita. Compare every cell with the homicide matrix and state whether the intra-group share is higher or lower off the murder margin. Arms: with and without the "unknown offender ethnicity" cell (report its size), reported-to-police only, and injury-only incidents.

## Limits to state
Perceived offender ethnicity; multiple-offender incidents; Mexican origin is not in NCVS (Hispanic only); series break at 2016 redesign.

## Rules (all lanes)
- Repo root `/Users/alien/Projects/immigration-research`. Own only your lane directory; `_cache/` is gitignored repo-wide; write outputs to `derived/`. Never edit anything under `research/`. Do not commit. Analysis agents do not commit.
- `uv run --no-project --with "pandas>=2" --with "numpy>=2" [--with requests --with lxml --with statsmodels] python3 <script>`; scripts over 10 lines in files; line-based progress; `PYTHONUNBUFFERED=1` for logs. Never use bare `python3` after `&&`.
- Census API key: `CENSUS_API_KEY` in `infra/immigration-fiscal/acquire/config.local.env` (source it; never print it). PUMS API pattern: `https://api.census.gov/data/<year>/acs/acs1/pums?tabulate=weight(PWGTP)&col+<VAR>&ucgid=0400000US<ST>&<VAR>=<a:b>&key=...`. Raw data under `~/research-data` is read-only.
- If census.gov or another host fails under curl (HTTP/2 PROTOCOL_ERROR seen on 2026-09-18), use `curl --http1.1 -C -`; a Modal container is authorized for downloads over 100 MB.
- Every number in your memo carries [SOURCE]/[CALCULATION]/[INFERENCE]/[UNVERIFIED]/[TRAINING-DATA]. Read `CLAUDE.md` and `notes/quant-bias-checklist.md` first. Disconfirmation is mandatory: run at least two arms that could reverse the headline and report them.
- Deliverables: `README.md` (run commands, inputs, outputs), `RESULT.md` opening `**Verdict:**` with counts, arms, what was skipped and why, then a draft memo section the parent can lift (verbatim quotes only from fetched sources). Update RESULT.md after each phase so partial progress survives.
- Verification you must run and report: every script re-run from scratch reproduces `derived/` byte-identically (`git diff --stat -- derived/` empty after the second run, or `cmp`).
- The repo measures resident groups, not admission; the absolute sign is a convention and the gap against same-age whites is not. Do not write policy advice.
