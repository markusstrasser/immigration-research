# Brief: benefit keys from administrative records by ethnicity

Lane: `infra/immigration-fiscal/admin_benefit_keys_2026_09_24/` · dispatched 2026-09-24 13:55 CEST

## Question

The account splits each programme's national dollars by survey keys: the shares of benefits people
report in CPS ASEC 2025 (SNAP, WIC, housing, cash assistance, SSI, unemployment; refundable credits
are imputed) and MEPS for medical spending. Survey-wide under-reporting washes out, because BEA
totals are split by shares. Differential under-reporting does not. People with immigration exposure
may under-report receipt (fear of public-charge or enforcement consequences); reporting can also
differ through language or household rosters. Nobody has tested the keys against administrative
participant data by ethnicity. Find a better key and say which way the account errs.

## Think first: two routes to a Mexican-origin administrative key

Administrative systems record Hispanic ethnicity and almost never Mexican origin.

- **Route A, states where Hispanic ≈ Mexican.** In Texas, Arizona, California, New Mexico and Nevada
  the Mexican share of Hispanics is high (verify with ACS). Where a programme publishes state-level
  Hispanic shares, compare the administrative Hispanic share with the survey's Hispanic share in
  those states. The ratio is a differential-reporting factor that applies almost directly to the
  Mexican-origin group.
- **Route B, national.** Administrative national Hispanic share × the survey's Mexican share within
  Hispanic recipients (assumes Mexicans report like other Hispanics).
- **Route C, independent check.** The linked survey–administrative literature on misreporting by
  ethnicity or citizenship (leads to verify: Meyer, Mittag and coauthors' linked CPS/ACS–SNAP work;
  Celhay, Meyer and Mittag on errors in reporting and imputation). Use it for direction and size.

Report A and B for every programme where data allow, and C where the literature covers it.

## Programmes, by dollars assigned to the group

- **Medicaid/CHIP:** enrollment and, if possible, spending by ethnicity from T-MSIS/TAF-based
  publications (CMS data briefs, DQ Atlas race/ethnicity completeness by state, MACPAC). The audit
  already used T-MSIS/TAF for long-term care (`dataset_integrity_2026_09_23` README row 5,
  `spending.md`); the medical key is MEPS-based, so say what an enrollment-share comparison can and
  cannot test.
- **SNAP:** USDA FNS SNAP Quality Control public-use microdata (FY2023 or latest: household and
  member ethnicity, citizenship, benefit amount) and the "Characteristics of SNAP Households" reports.
- **Housing assistance:** HUD Picture of Subsidized Households (2023 or 2024): share of Hispanic
  household heads by programme and subsidy dollars.
- **WIC:** FNS WIC Participant and Program Characteristics (2022 or latest).
- **TANF:** ACF Characteristics and Financial Circumstances of TANF Recipients (FY2022 or FY2023).
- **Unemployment insurance:** DOL ETA 203 claimant characteristics, which include ethnicity.
- **Optional:** school meals (CCD free/reduced-price eligibility × Hispanic membership by school).
  SSI: SSA publishes noncitizen counts, not ethnicity; note and skip unless you find a route.
- Refundable credits belong to the parallel `external_benchmarks_2026_09_24` lane; skip them.

For each programme report the account's current group share and dollars
(`full_account_spending_2026_09_20/derived/incidence_keys.csv`, `allocations.csv`;
`full_account_2026_09_20/derived/accounts.csv`), the survey's Hispanic share under the same
definitions (compute it, or say why you cannot), the administrative Hispanic share, the ratio and
the re-keyed group dollars under routes A and B. Flag keys that are not self-reports (imputed
credits, MEPS). Positive control first: reproduce the account's SNAP target share from the CPS
microdata before any comparison.

## Read first (build on these; do not redo them)

`admin_transfer_checks_2026_09_19` (programme totals against administrative totals; uniform gap
allocation moved the balance $5–7bn), `health_admin_2026_09_20`, `benefit_scale_2026_09_19`,
`dataset_integrity_2026_09_23` (README rows 1, 5, 9, 10, 12; `spending.md`; `cps_status_keys.py`),
`mexican_origin_population_total_2026_09_19` (coverage), `improper_payments_unauthorized_2026_09_23`
(context only).

## Deliverables

- `derived/program_keys.csv`: programme, year, administrative source, admin Hispanic share, survey
  Hispanic share, ratio, route, group $bn now, group $bn re-keyed, change.
- Scripts and one `test_*.py` with the positive control.
- `RESULT.md`: the net change to the main case and its direction; whether the fear-driven
  under-reporting hypothesis holds in administrative data, programme by programme.

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
  document you rely on to `_cache/` and cite page or table. Parse primary PDFs for any number used in
  a calculation; do not use scraped schema extraction for numbers.
- Report every specification you compute: list the spec column of each derived CSV in RESULT.md,
  including rows that go against your leading reading.
- Per-capita figures from pooled years: compute one year at a time or check against an independent
  annual rate.
- No single download over 10 GB without `df -h` first.
- Blocked data (login, data-use agreement, dead link): write `[BLOCKED] <what, where>` and continue
  with the next programme.
- A lane adopts nothing. Express each finding as a proposed change to the adopted main case
  ($203.2–249.6bn, `main_case_2026_09_23/`) and, where different, to the proposed audit package
  ($202.9–251.1bn, `dataset_integrity_2026_09_23/synthesis.py`); say which.
- Finish: `RESULT.md` opens with `**Verdict:**` (2–5 sentences: the answer, direction, size, how
  sure), then method, results, what would change it, limits, reproduce commands. Return to the
  parent the RESULT.md path and at most 10 lines.
