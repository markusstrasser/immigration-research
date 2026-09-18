# Lane: longevity and Social Security timing on the lifetime frame (2026-09-18)

## Goal
Two objections a competent reader raises against the repo period account: (1) Hispanic life expectancy exceeds non-Hispanic white by about three years, so the 65+ bands draw Social Security and Medicare for longer than the constructed terminal age implies; (2) workers pay OASDI taxes now and claim later, so a snapshot over-credits the working ages. Quantify both on the repo own profiles.

## Inputs on disk
- Age profiles by group and reference: `infra/immigration-fiscal/pronatal_equivalence_2026_09_18/derived/age_profiles_references.csv` and `lifetime_equivalence.csv` (the 3% and undiscounted lifetime machinery; read that lane README and RESULT first). The homicide lane loader `infra/immigration-fiscal/homicide_cost_2026_09_18/cost_model.py` (`load_profiles`, TERMINAL = 83) shows how the profiles are consumed; reuse, do not rewrite.
- The complete-account items and conventions: `infra/immigration-fiscal/ledger_absolute_2026_09_17/RESULT.md`.

## Part A: longevity
Fetch CDC NVSS United States Life Tables (latest final year, 2022 or 2023) by Hispanic origin and race: Hispanic, non-Hispanic white, and if published Hispanic by sex. Source: cdc.gov NVSR life-table report or data.cdc.gov. Cache the file. Build survival curves l(x) and replace the constructed terminal age with survival-weighted lifetime sums for each group: lifetime balance at 3% and undiscounted, from age 0 and from age 25, for Mexican-origin by generation (Hispanic life table as proxy, labelled) and for the third-plus non-Hispanic white reference. Report the per-person change in the lifetime gap attributable to the longevity difference alone (hold profiles fixed, swap survival), on the partial and complete accounts. Arms: Hispanic table for all generations vs Hispanic for first generation only and white for descendants (the paradox fades by generation; cite the NVSS or a published source for that); mortality at ages 65+ only vs all ages.

## Part B: Social Security timing
Use SSA money-worth ratios by earnings level and cohort (SSA Office of the Chief Actuary, Actuarial Note series "Money Worth Ratios Under the OASDI Program for Hypothetical Workers", latest edition; cache the PDF or HTML) to convert each dollar of OASDI tax paid this year by working-age members of each group into the present value of benefits it accrues. Earnings level per group from the CPS-based profiles (use the profile tax line and the group wage distribution; the pronatal lane README says where the wage inputs live). Report: the accrued-liability adjustment per person-year and for the union population, the sign, and how it compares to the −$7,224 common-age complete gap. Cross-check with the 2025 OASDI Trustees Report immigration sensitivity (Section VI.D, net immigration alternatives) and the SSA Actuarial Note on unauthorized immigrants (Goss et al. 2013) as a second route; report both routes and their disagreement.

## Falsification
State the arm under which longevity plus timing together would close or reverse the common-age gap, and whether it is inside the published ranges.

## Rules (all lanes)
- Repo root `/Users/alien/Projects/immigration-research`. Own only your lane directory; `_cache/` is gitignored repo-wide; write outputs to `derived/`. Never edit anything under `research/`. Do not commit. Analysis agents do not commit.
- `uv run --no-project --with "pandas>=2" --with "numpy>=2" [--with requests --with lxml --with statsmodels] python3 <script>`; scripts over 10 lines in files; line-based progress; `PYTHONUNBUFFERED=1` for logs. Never use bare `python3` after `&&`.
- Census API key: `CENSUS_API_KEY` in `infra/immigration-fiscal/acquire/config.local.env` (source it; never print it). PUMS API pattern: `https://api.census.gov/data/<year>/acs/acs1/pums?tabulate=weight(PWGTP)&col+<VAR>&ucgid=0400000US<ST>&<VAR>=<a:b>&key=...`. Raw data under `~/research-data` is read-only.
- If census.gov or another host fails under curl (HTTP/2 PROTOCOL_ERROR seen on 2026-09-18), use `curl --http1.1 -C -`; a Modal container is authorized for downloads over 100 MB.
- Every number in your memo carries [SOURCE]/[CALCULATION]/[INFERENCE]/[UNVERIFIED]/[TRAINING-DATA]. Read `CLAUDE.md` and `notes/quant-bias-checklist.md` first. Disconfirmation is mandatory: run at least two arms that could reverse the headline and report them.
- Deliverables: `README.md` (run commands, inputs, outputs), `RESULT.md` opening `**Verdict:**` with counts, arms, what was skipped and why, then a draft memo section the parent can lift (verbatim quotes only from fetched sources). Update RESULT.md after each phase so partial progress survives.
- Verification you must run and report: every script re-run from scratch reproduces `derived/` byte-identically (`git diff --stat -- derived/` empty after the second run, or `cmp`).
- The repo measures resident groups, not admission; the absolute sign is a convention and the gap against same-age whites is not. Do not write policy advice.
