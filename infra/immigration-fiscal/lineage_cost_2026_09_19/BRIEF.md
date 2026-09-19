# Lane: the 100-year fiscal and crime cost of one Mexico-born arrival's lineage (2026-09-19)

## Goal
Land, as a reproducible lane, the operator's question: the fiscal balance of one Mexico-born arrival (unauthorized at arrival; and the Mexico-born average as a second arm) plus their descendants over 100 years, per year and in present value, against the same construction for one third-plus non-Hispanic white of the same age. A working scratch script exists and must be turned into a lane, not trusted: `/private/tmp/claude-501/-Users-alien-Projects-immigration-research/45fdf7bc-6c76-4a97-953b-e9d9ea0bf7a5/scratchpad/lineage_cost.py` (copy it in; its central result was −$1.22M per founder over 100 years undiscounted on the complete account, low fertility, half attribution, against −$661k for the white reference; check every input path and every constant it hard-codes against the cited lane outputs and replace hard-coded constants with reads).

## Inputs (read-only, all in `infra/immigration-fiscal/`)
- Period age profiles by generation: `all_age_ledger_2026_09_17/derived/age_profiles.csv` (scenario `all_age_shared`), complete-account add-on from `ledger_absolute_2026_09_17/derived/waterfall.csv`.
- Survival: `lifetime_longevity_sstiming_2026_09_18/derived/survival_tables.csv` (Hispanic and white 2024 tables; use the white table for the reference lineage).
- Fertility by generation: `native_fertility_2026_09_16/derived/` and `pronatal_equivalence_2026_09_18/derived/` (read what they give; state the TFR ratios used and their source; do not invent).
- Unauthorized penalty: ladder 85 corrected arm (`status_impute_2026_09_16` or the lane the ladder cites); crime cost per person-year: `crime_cost_firstgen_2026_09_18/derived/firstgen_cost_weighted.csv` (founder) and `crime_cost_2026_09_16/derived/` (US-born), tangible and social columns separately.
- Attrition: `mexican_origin_population_total_2026_09_19/derived/arm3_multiplier.csv` and `arm5_education_selectivity.csv` — third-plus descendants who attrite carry converged characteristics; run the lineage with and without that correction.

## Arms
1. Founder arrives at 25; generation length 29 (justify from ACS mean age at birth for Mexican-origin women, or state it as an assumption with a sensitivity at 26 and 32). Fertility low (repo ratios × white TFR) and high; attribution of children to the lineage half (intermarriage) and full. Horizon 100 years; discount 0% and 3%. Report per founder: lifetime fiscal balance, 100-year lineage total, per year, PV, crime tangible and social, number of persons generated, and the same for the white reference founder. The gap (lineage minus white lineage) is the headline.
2. **Disconfirmation arms:** (a) generation-specific convergence: replace the third-plus self-ID profile for G4+ with the attrition-corrected mixed profile; (b) unauthorized founder legalised at year 10 (switch to the legal Mexico-born profile); (c) fertility falling to white TFR in G2 (the native_fertility lane's finding, if that is what it says); report whether any arm brings the lineage gap inside the founder's own lifetime gap.
3. Growth: state that all profiles are 2024$ period profiles with no productivity growth; run one arm with 1% real growth in both taxes and outlays (neutral to the sign, changes the level) so the reader sees the sensitivity.

## Outputs
`derived/lineage_table.csv` (every arm × account × attribution × fertility × discount), `derived/generation_breakdown.csv`, `derived/white_reference.csv`, `derived/sensitivities.csv`. `RESULT.md` opening `**Verdict:**` with the central founder, lineage and per-year numbers, the white reference, the gap, and which arm moves it most.

## Limits to state
Period profiles are not cohort projections; no general equilibrium, no behavioural response, no wage growth by default; fertility and intermarriage are assumptions with sources; the crime social cost column is jury-award-derived (McCollister) and reported separately from the fiscal line.

## Rules (all lanes)
- Repo root `/Users/alien/Projects/immigration-research`. Own only your lane directory; `_cache/` is gitignored repo-wide; add a lane `.gitignore` with `logs/` and `__pycache__/`; write outputs to `derived/` (no file over 5 MB). Never edit anything under `research/`. Do not commit. Analysis agents do not commit.
- `uv run --no-project --with "pandas>=2" --with "numpy>=2" [--with requests --with pyarrow --with statsmodels --with duckdb] python3 <script>`; scripts over 10 lines in files; line-based progress; `PYTHONUNBUFFERED=1` for logs. Never bare `python3`.
- Census API key: `CENSUS_API_KEY` in `infra/immigration-fiscal/acquire/config.local.env` (source it with `set -a; . …; set +a`; never print it; never run `pgrep -f`/`ps` dumps; catch `requests` HTTPError and print only the status code, never the URL). Raw data under `~/research-data` is read-only. census.gov may truncate bodies under HTTP 200: validate every download by content (row count, magic bytes), `curl --http1.1` on failure.
- Every number in your RESULT.md carries [SOURCE]/[CALCULATION]/[INFERENCE]/[UNVERIFIED]/[TRAINING-DATA]. Read `CLAUDE.md` and `notes/quant-bias-checklist.md` first. Disconfirmation is mandatory: at least two arms that could reverse the headline, reported whether or not they do. Neutral language about named persons and groups.
- Deliverables: `README.md` (run commands, inputs, outputs), `RESULT.md` opening `**Verdict:**` then arms, what was skipped and why, then a draft memo section the parent can lift (verbatim quotes only from fetched primary sources). Update RESULT.md after each phase.
- Verification you must run and report: re-run every script over the existing cache and show `derived/` is byte-identical (`diff -rq` against a copy). The parent re-runs everything independently.
- The repo measures resident groups, not admission; the gap against same-age third-plus non-Hispanic whites is the meaningful number. No policy advice.
