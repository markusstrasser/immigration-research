# Brief: which Mexico-born count is right for early 2025 (audit row 4)

Owner: `mexborn-count` agent. Write only inside `infra/immigration-fiscal/mexborn_count_2026_09_23/`.
Do not commit; the parent grades and commits. Result file: `RESULT.md`, first line
`**Verdict:** …`.

## Why

Every CPS-based number in the main case reads one file: CPS ASEC 2025 public use
(`gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip`). It counts **12.231M Mexico-born** (SE
0.248). The other two counts are lower:
- ACS 2024 1-year: 11.005M in households, 11.154M with group quarters;
- CPS ASEC 2026 (`ledger_asec2026_2026_09_16`): 11.109M.

The instruments agree in California and Texas (6.30 vs 6.31). The whole excess is in the other
states (5.93M, against 4.70M in the ACS and 5.09M in ASEC 2026) and among noncitizens (8.13M,
against 7.20M and 6.77M). The CPS weights to national Hispanic controls by age and sex, not by
origin. See `dataset_integrity_2026_09_23/cps.md` §3, `derived/cps_vs_acs_origin.csv` and
`derived/cps_mexico_born_gap.csv`.

The audit prices the gap at −$6.0bn to −$8.3bn on the main case ($203.2–249.6bn) if the ACS is
right: the excess share × the first generation's 33.3% share of the union net (ledger waterfall step
14) × the main case. The population lane (`mexican_origin_population_total_2026_09_19`) assumed the
CPS under-covers the Mexico-born. The unauthorized lane's 4.567M Mexico-born unauthorized
(`unauthorized_population_size_2026_09_19`) is a residual from CPS 2025.

## Question

For February–April 2025, the ASEC reference months, which level is right: about 12.2M or about
11.1M? What is the resulting effect on the main case and on the unauthorized count?

## Method

1. **CPS basic monthly files, January 2024 to the latest held or available month.**
   - Source: census.gov/data/datasets/time-series/demo/cps/cps-basic.html.
   - Variables: `PENATVTY`, `PRCITSHP`, `GESTFIPS`, `PWCMPWGT` or `PWSSWGT`.
   - Build the monthly Mexico-born series, total and outside CA+TX. Does the count jump in the ASEC
     months, or is the ASEC sample alone high?
   - Before downloading, check the size of each file (`curl -sI`) and the free disk space; the
     monthly zips are about 15–20 MB each.
2. **ACS 2025 1-year.** It was not on the Census API on 2026-09-23 (404). Re-check once; if it has
   been released, tabulate the same cuts.
3. **Official and independent benchmarks.** Read the primary sources and quote each number with
   its page:
   - DHS OHSS LPR population estimates for Mexico (January 2024 or the latest), and naturalizations;
   - Pew, CMS (Center for Migration Studies) and MPI estimates of Mexican unauthorized residents for
     2022–2024;
   - the Census Vintage 2024 and 2025 net international migration, and the control change the CPS
     documentation flags (cpsmar25 footnote 9);
   - Mexico's INEGI/CONAPO or Mexican consular statistics, if they help.
4. **Decide**, weighting by instrument quality: ACS sample size and mode, CPS nonresponse among
   noncitizens, and whether the 2025→2026 drop (−1.12M) is plausible as real outflow. Price row 4 at
   the chosen level with the audit's formula; give low / central / high. Report the implied change to
   the unauthorized lane's 4.567M.

## Output

`RESULT.md` should open with the verdict: the level, the $bn effect, and the unauthorized-count
implication. Follow it with:
- the monthly series table;
- the benchmark table graded by evidence level;
- disconfirmation: what would make the CPS level right.

Put scripts in the lane directory and outputs in `derived/`. Tag claims `[SOURCE: …]`, `[DATA: …]`,
`[CALCULATION: …]` or `[INFERENCE]`.

## Validation

- Reproduce the audit's 12.231M and 11.109M from the held ASEC files as a gate before anything
  else.
- Rerun every script and show that the `derived/` outputs are byte-identical.
- Every published number used in a calculation is parsed from the primary document.

## Constraints

- Run Python as `OPENBLAS_NUM_THREADS=1 uv run --no-project [--with pkg] python3 <script>` from
  the repository root.
- Never print API keys (`infra/immigration-fiscal/acquire/config.local.env`); redact Census URLs
  with `sed -E 's/key=[A-Za-z0-9]+/key=<KEY>/g'`.
- Microdata goes in `_cache/` (ignored).
- No edits outside this directory.
- Stop after about 12 turns of source search and report what you have.
