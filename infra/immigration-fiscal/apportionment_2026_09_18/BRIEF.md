# Lane: House seats and electoral votes attributable to the Mexican-origin population (2026-09-18)

## Goal
An exact third-order political number: how many House seats and electoral votes moved between states in the 2020 (and 2010) apportionment because the Mexican-origin population is counted where it lives. No identification problem; it is arithmetic on public counts.

## Inputs
- 2020 and 2010 apportionment populations by state (Census apportionment tables; include overseas military as the Bureau does). Cache.
- Mexican-origin population by state: 2020 Census DHC (Hispanic origin: Mexican) via the Census API (`dec/dhc`, `P9`/`P10`-type tables; check the variable list) and the 2010 SF1 equivalent; foreign-born Mexico by state from ACS 2020 5-year (B05006) and ACS 2010 5-year; unauthorized by state from Pew (2021 or latest) and CMS estimates (cache the tables; cite).
- Method of equal proportions (Huntington–Hill); implement and verify that it reproduces the official 2020 and 2010 seat counts exactly before running counterfactuals.

## Counterfactuals (each a separate run, all reported)
1. Remove the Mexico-born from every state.
2. Remove all Mexican-origin persons (foreign-born and US-born).
3. Remove the estimated unauthorized population (all origins; Pew and CMS arms).
4. Remove the Mexico-born and their US-born children under 18 (ACS B05009 or PUMS: children with a Mexico-born parent), the "second-generation-in-the-house" arm.
For each: seats gained and lost by state, net electoral-vote shift, and which arms move the 2020 or 2024 presidential outcome in the Electoral College (report as arithmetic on the certified results, not as a claim about behaviour). Also report the 2030 projection using Census Vintage 2024 estimates as a rough arm, clearly labelled.

## Limits to state
Apportionment counts persons regardless of status by constitutional design; the counterfactual removes people from counts, not from the country; PUMS-based child linkage is an estimate.

## Rules (all lanes)
- Repo root `/Users/alien/Projects/immigration-research`. Own only your lane directory; `_cache/` is gitignored repo-wide; write outputs to `derived/`. Never edit anything under `research/`. Do not commit. Analysis agents do not commit.
- `uv run --no-project --with "pandas>=2" --with "numpy>=2" [--with requests --with lxml --with statsmodels] python3 <script>`; scripts over 10 lines in files; line-based progress; `PYTHONUNBUFFERED=1` for logs. Never use bare `python3` after `&&`.
- Census API key: `CENSUS_API_KEY` in `infra/immigration-fiscal/acquire/config.local.env` (source it; never print it). PUMS API pattern: `https://api.census.gov/data/<year>/acs/acs1/pums?tabulate=weight(PWGTP)&col+<VAR>&ucgid=0400000US<ST>&<VAR>=<a:b>&key=...`. Raw data under `~/research-data` is read-only.
- If census.gov or another host fails under curl (HTTP/2 PROTOCOL_ERROR seen on 2026-09-18), use `curl --http1.1 -C -`; a Modal container is authorized for downloads over 100 MB.
- Every number in your memo carries [SOURCE]/[CALCULATION]/[INFERENCE]/[UNVERIFIED]/[TRAINING-DATA]. Read `CLAUDE.md` and `notes/quant-bias-checklist.md` first. Disconfirmation is mandatory: run at least two arms that could reverse the headline and report them.
- Deliverables: `README.md` (run commands, inputs, outputs), `RESULT.md` opening `**Verdict:**` with counts, arms, what was skipped and why, then a draft memo section the parent can lift (verbatim quotes only from fetched sources). Update RESULT.md after each phase so partial progress survives.
- Verification you must run and report: every script re-run from scratch reproduces `derived/` byte-identically (`git diff --stat -- derived/` empty after the second run, or `cmp`).
- The repo measures resident groups, not admission; the absolute sign is a convention and the gap against same-age whites is not. Do not write policy advice.
