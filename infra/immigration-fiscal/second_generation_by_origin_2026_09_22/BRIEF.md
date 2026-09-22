# Brief — second generation by parental origin, IPUMS-CPS ASEC 1994–2025 (cluster-V V02)

Owner: the build agent. Files owned: this directory only (except BRIEF.md). No commits. No edits outside it.
Data (read-only): `sources/immigration-fiscal/data/external/cps/cps_2ndgen.csv.gz` (5,721,633 persons, 32 ASECs 1994–2025), its DDI `cps_2ndgen.xml` (variable codes: read it for EDUC, EMPSTAT, LABFORCE, HISPAN, RACE, CITIZEN, NATIVITY, BPL code lists) and `cps_2ndgen.manifest.json` (sha256; verify before reading).
Prior art to reuse, not repeat: `infra/immigration-fiscal/build/load_cps_second_gen.py` (region map; note CPS BPL codes are 5-digit, general code = code // 100), `research/immigration-gated-data-specs-2026-06-25.md` §1 (design and caveats: NCHILD/YNGCH are coresident children, not completed fertility; EDUC is a code), `research/immigration-mexican-origin-by-generation-2026-09-16.md` and `infra/immigration-fiscal/gen_ledger_extension_2026_09_16/` (the repo's G1/G2/G3+ definitions on ASEC 2025 and its white reference).

## Question
Do origin-group gaps in adult outcomes persist into the US-born second generation, and by how much do they close, by parental origin and over 1994–2025? Descriptive, with sampling error. No causal claim.

## Definitions (must match the repo's conventions)
- Universe: civilian adults 25–64 (`AGE`), ASEC person weight `ASECWT`. Drop `ASECFLAG`/`HFLAG` duplicates only if the DDI says the 2014 redesign sample would otherwise double count; document the choice.
- Generations from `NATIVITY`: 5 = first generation (own `BPL` gives origin); 2, 3, 4 = second generation (origin = `FBPL` when foreign, else `MBPL`; report the both-foreign subset separately); 1 = third-plus.
- Reference group: third-plus, non-Hispanic white (`NATIVITY` 1, `HISPAN` 0, `RACE` white per DDI), the ledger's white reference. Also report the all-native-parentage baseline the loader uses.
- Mexican-origin third-plus by self-identification: `NATIVITY` 1 and `HISPAN` Mexican code, as `mexican_third_plus_selfid` in the ledger extension. Report it as its own row.
- Origins: nine regions from the loader map plus the ten largest single parental birthplaces by weighted second-generation count (Mexico will be first). Country codes come from the DDI, never from memory.
- Outcomes: employed (`EMPSTAT` employed codes per DDI), in labor force, female LFP, log `INCTOT` for positive values (NIU = 999999999), positive `INCWAGE` share and log wage, college-or-more and less-than-high-school shares from `EDUC` codes per DDI, coresident own children for women 40–49 (`NCHILD`), citizenship for the first generation.
- Periods: 1994–2004, 2005–2014, 2015–2025.

## Estimates
1. Weighted means by generation × origin × period (all cells with n ≥ 100 unweighted).
2. Age- and sex-adjusted gaps to the white reference: weighted least squares of each outcome on origin × generation indicators with age-band × sex × survey-year fixed effects; report gaps, not coefficients on controls.
3. Closing ratio per origin: 1 − (second-generation adjusted gap / first-generation adjusted gap), for education, employment and log income; report the raw ratio too.
4. Standard errors: no replicate weights in this extract. Use a household-cluster bootstrap (resample `SERIAL` within `YEAR`, 200 draws) for every reported mean, gap and ratio; write the draw count and seed into audit.json. State that this ignores the CPS PSU design and is a lower bound on the true SE.

## Gates (fail loud; a failure is the verdict)
- G1 manifest sha256 of the CSV matches before any read.
- G2 reproduce the loader: rebuilding `cps_second_gen_by_origin` from this lane's code must equal `sources/immigration-fiscal/derived/lifetime/cps_second_gen_by_origin.csv` (all 37 rows, all columns, to 1e-9 after the same rounding).
- G3 population anchor: for ASEC 2025 the weighted count of `BPL` = Mexico persons (all ages) and of second-generation persons with a Mexican-born parent must match the `gen_ledger_extension_2026_09_16` derived populations for `mexico_born` and `mexican_second_gen` within 0.5% (find the file; if the lane stores civilian-only counts, apply the same civilian filter and say so). If no such file exists, say so and anchor instead on the Census-published CPS ASEC 2025 foreign-born total if it is in the repo; never invent an anchor.
- G4 code sanity from the DDI: the employed, in-labor-force, college and Mexico/white/Hispanic codes used are printed with their DDI labels in audit.json.
- G5 every cell has n ≥ 100 unweighted; every SE is finite.

## Outputs
`derived/cells.csv`, `derived/adjusted_gaps.csv`, `derived/closing_ratios.csv`, `derived/period_trends.csv`, `derived/audit.json` (hashes, gates, codes with labels, bootstrap spec, limitations), `analysis.py`, `test_analysis.py` (synthetic-data tests of the estimators plus the DDI code assertions), `README.md`, `RESULT.md` (opens with `**Verdict:**`; the Mexico rows first; tables; gates; files covered/skipped; limits copied without softening). Every number in RESULT.md is tagged `[CALCULATION: derived/<file>]`. No number from memory.

Verification commands (run all, paste tails into RESULT.md):
```sh
cd /Users/alien/Projects/immigration-research
uv run --no-project python3 -m pytest infra/immigration-fiscal/second_generation_by_origin_2026_09_22/ -q
OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb python3 infra/immigration-fiscal/second_generation_by_origin_2026_09_22/analysis.py
```
Use DuckDB or pandas over the gz CSV; 5.7M rows fit in memory. If a full run exceeds 4 minutes wall, run it with `~/Projects/skills/bin/bgrun v02-build -- <command>` and poll the `.done` marker; never pipe a background command through `tail`.
Return: the RESULT.md path and at most 10 lines (verdict; Mexico closing ratios for education, employment, income with SEs; gate summary; files; anything skipped and why).
