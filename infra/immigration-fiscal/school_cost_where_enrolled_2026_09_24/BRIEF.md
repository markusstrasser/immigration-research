# Brief: school cost per pupil where the group's children actually enroll

Lane: `infra/immigration-fiscal/school_cost_where_enrolled_2026_09_24/` · dispatched 2026-09-24 13:55 CEST

## Question

Schools are the line that turns the account's balance into a cost: $87.1–114.0bn a year in the
adopted main case (a 63–66% response × cost per pupil × the Mexican-origin group's pupils; see
`figures_2026_09_22/src/generated/figures.json`, staircase step `schools`). The account charges the
**national average** cost per pupil. A school-finance specialist would ask two things:

1. The group's pupils are concentrated in particular states and districts. Leads to verify: Texas
   and Arizona spend below the national average per pupil, California near or above it.
2. Most state formulas and federal programmes pay more for English learners and low-income pupils.
   The account says English-learner surcharges were "not imported"
   (`research/immigration-complete-annual-account-2026-09-20.md:195`).

Build the cost per pupil where the group's pupils actually enroll, and give the corrected school line.

## Read first (build on these; do not redo them)

- `school_enrollment_2026_09_20` (measured enrollment rates and the group's pupil counts; +$25bn
  correction), `admin_school_checks_2026_09_19` (CPS vs ACS pupils), `education_origin_fiscal_2026_09_19`,
  `school_peer_checks_2026_09_20`, `school_flight_2026_09_18`.
- `dataset_integrity_2026_09_23`: README row 6 (the education key puts 93% on K–12; BEA's split is
  77–82%), `acs_school_*.csv`, `acs.md`.
- How the account computes the line: `full_account_spending_2026_09_20` (keys `school_operating`,
  `age5_24`, `education_mix`), `full_account_2026_09_20/service_response.py`,
  `main_case_2026_09_23/inputs.json` and `main_case.js`. `figures_2026_09_22/build_data.cjs` shows how
  to evaluate the explorer engine with per-line response overrides.

## Method (preferred first, fallbacks after)

1. **District level.** NCES Common Core of Data LEA membership by race/ethnicity for 2023–24 (Hispanic
   counts), English-learner counts (CCD or EDFacts), and the Census Annual Survey of School System
   Finances for FY2023 or the latest year (current spending per pupil by LEA; NCES F-33 or Census
   "elsec" files). Link by NCES LEA ID; report the match rate.
2. **Group weighting.** The group is Mexican-origin (all generations), not all Hispanic. Get the
   Mexican share of Hispanic school-age children by state (ACS 2024) and, if feasible, by district or
   PUMA (ACS 5-year table B03001 by school district, or a PUMS PUMA-to-district crosswalk). Show three
   weightings: (i) Hispanic, (ii) Hispanic × the state's Mexican share, (iii) the finest
   Mexican-origin weighting you can build.
3. **Within districts.** If school-level ESSA per-pupil expenditure data exist in usable form
   (leads: Georgetown Edunomics NERD$, NCES School-Level Finance Survey; verify), add school-level
   weighting with CCD school membership by ethnicity and report how much within-district allocation
   (Title I schools) moves the district result.
4. **English learners.** District weighting already carries what formulas pay districts for English
   learners and poor pupils. As a check, estimate the revealed marginal spending per English learner
   within states: district spending per pupil on English-learner share and poverty share with state
   fixed effects.
5. **Result.** R = group-weighted current spending per pupil ÷ national current spending per pupil.
   Give the implied school line (R × the current line) for the adopted main case and for the audit
   package, whose row 6 changes the education split. Keep definitions aligned: BEA current consumption
   includes depreciation and excludes capital outlay; explain how Census current spending maps to it,
   and report capital outlay and interest separately. Check the group's pupil count against the
   administrative count as well (CCD Hispanic enrollment × Mexican share against the account's pupils).

Positive control first: reproduce the school step ($87.1–114.0bn) from the engine and inputs before
applying R.

## Deliverables

- `derived/per_pupil_weighting.csv` (spec, weighting, R, school line low/high $bn, change $bn),
  `derived/state_breakdown.csv` (state, group pupils, spending per pupil, contribution).
- Scripts and one `test_*.py` (the positive control plus one hand-checked state).
- `RESULT.md`: direction and size of the correction to the $87–114bn line and what drives it (state
  mix, within-state allocation, English-learner money).

## Rules (all lanes)

- Own only this lane directory. Do not edit anything else (memos, INDEX, ladder, FAQ, other lanes'
  code or outputs). Do not commit; the parent re-runs and integrates.
- First action: write `RESULT.md` opening `**Verdict:** (pending)`; update it as you go.
- Raw pulls go to `_cache/` (gitignored). Tracked outputs: scripts, `derived/*.csv` written with LF
  line endings (`lineterminator="\n"`), README/RESULT.
- Fetch with `subprocess.run(["curl", "-sS", "--fail", ...])`; Python urllib fails TLS on this
  machine. Validate content (row counts, expected columns and keys), never status or size alone;
  census.gov can return truncated bodies under HTTP 200.
- Census API key: `set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a` exports
  `CENSUS_API_KEY`. Never print it; redact URLs in logs and errors
  (`sed 's/key=[^&]*/key=REDACTED/'`); never run `ps` or `pgrep -f` dumps.
- Run Python from the repo root `/Users/alien/Projects/immigration-research` with
  `OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy python3 <script>` (add
  `--with` packages as needed; write each `--with pkg` literally).
- Tag every number in RESULT.md: [SOURCE: url + page/table], [DATA: local file],
  [CALCULATION: script/output], [INFERENCE] or [UNVERIFIED]. Never state an author, figure or
  publication from memory; the leads above are to verify and some may not exist. Save each primary
  document you rely on to `_cache/` and cite page or table.
- Report every specification you compute: list the spec column of each derived CSV in RESULT.md,
  including rows that go against your leading reading.
- Per-capita figures from pooled years: compute one year at a time or check against an independent
  annual rate.
- No single download over 10 GB without `df -h` first.
- Blocked data (login, data-use agreement, dead link): write `[BLOCKED] <what, where>` and continue
  with the next step.
- A lane adopts nothing. Express each finding as a proposed change to the adopted main case
  ($203.2–249.6bn, `main_case_2026_09_23/`) and, where different, to the proposed audit package
  ($202.9–251.1bn, `dataset_integrity_2026_09_23/synthesis.py`); say which.
- Finish: `RESULT.md` opens with `**Verdict:**` (2–5 sentences: the answer, direction, size, how
  sure), then method, results, what would change it, limits, reproduce commands. Return to the
  parent the RESULT.md path and at most 10 lines.
