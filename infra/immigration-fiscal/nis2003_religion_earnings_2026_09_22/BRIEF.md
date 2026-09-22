# Brief — religion and earnings among new legal permanent residents, NIS 2003 Round 1 (ICPSR 38031 v3)

Owner: the build agent. Files owned: this directory only (except BRIEF.md). No commits. No edits outside it.
Data (read-only): `sources/immigration-fiscal/data/external/icpsr_nis_2003/ICPSR_38031-V3.zip` (567,819,638 bytes; sha256 `61a6e3d58d79f652…`, full hash in `sources/immigration-fiscal/data/MANIFEST.md`). Unzip only what you need into `_cache/` (git-ignored; create `.gitignore` with `_cache/`). Adult sample datasets: DS0001 roster (8,573 respondents), DS0002 preload, DS0003 Section A demographics (3,461 variables), DS0004–05 Section B, DS0006–24 sections C–R. Religion is in Section J (DS0017: `J30_1MO` respondent's religion, `J31_1MO`, `J33_1MO` denomination, `J36_1MO`); income and earnings in Section H (DS0013 and DS0014). Use `pdftotext -layout` on the ICPSR codebooks in the zip to read code lists; never quote a code from memory. Sampling weights: `38031-Documentation-sampling_weights.pdf`.
Context: `research/immigration-muslim-origins-funding-outcomes-2026-09-21.md` §2 lists NIS 2003 as "not reached" for religion with earnings; this lane reaches it.

## Question
Among adults granted permanent residence in 2003, how do employment and earnings differ by religion, before and after conditioning on education, English, age, sex, origin region and class of admission? Descriptive; the sample is new legal immigrants only.

## Steps
1. Locate and print (into audit.json, with codebook labels) the variables for: religion (J30/J33), age, sex, country of birth, years of schooling or highest degree (Section A), English speaking/reading ability (Section A or B), class of admission (preload or Section A; the public file may hold an aggregated version), current employment status and hours (Section G or H), own earnings last year and current wage (Section H), and any means-tested program use if present (Section H or I). If a needed variable exists only in the restricted tier, say so and proceed without it.
2. Religion groups: Muslim, Christian (Catholic, Protestant/other Christian, Orthodox separately where n allows), Hindu, Buddhist, Jewish, no religion, other. Cell sizes unweighted and weighted.
3. Estimates with the documented sampling weight: employment rate, share with positive earnings, mean and median earnings, log-earnings gaps to the Christian group, unadjusted and adjusted (WLS with age band × sex, schooling, English, region of birth, class of admission). Standard errors: Taylor linearization with the design variables if the weights documentation provides strata/PSU; otherwise a 500-draw respondent bootstrap, stated as such.
4. Anchors (gates): reproduce at least three published counts from `38031-Documentation-overview.pdf` (for example respondents by class of admission or by region of birth) to the unit before any estimate is reported; the adult sample size 8,573 must reproduce in every dataset used.

## Gates
G1 zip sha256 matches the manifest. G2 8,573 respondents in each dataset joined on `PU_ID`, no duplicates. G3 three published counts reproduced. G4 every code used is printed with its codebook label. G5 every cell has n ≥ 50; every SE finite.

## Outputs
`derived/religion_cells.csv`, `derived/earnings_gaps.csv`, `derived/anchors.csv`, `derived/audit.json`, `analysis.py`, `test_analysis.py`, `README.md`, `RESULT.md` (opens with `**Verdict:**`; tables; gates; files covered/skipped; limits: new-LPR sample only, 2003 dollars, self-reported religion, small cells). Every number tagged `[CALCULATION: derived/<file>]`.

Verification commands (run all, paste tails into RESULT.md):
```sh
cd /Users/alien/Projects/immigration-research
uv run --no-project python3 -m pytest infra/immigration-fiscal/nis2003_religion_earnings_2026_09_22/ -q
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/nis2003_religion_earnings_2026_09_22/analysis.py
```
Return: the RESULT.md path and at most 10 lines (verdict; Muslim vs Christian employment and adjusted log-earnings gap with SEs; anchors; files; anything skipped and why).
