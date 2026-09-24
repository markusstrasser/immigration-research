# Brief: outside numbers that corroborate or contradict the account's shares

Lane: `infra/immigration-fiscal/external_benchmarks_2026_09_24/` · dispatched 2026-09-24 13:55 CEST

## Question

The operator asked for outside numbers that can corroborate the complete annual account, "like the
$2tn deficit or expenses". The account already reconciles every dollar to BEA's 2024 consolidated
government account: receipts $8,008.290bn, current expenditure $10,061.458bn, balance
−$2,053.168bn (`research/immigration-complete-annual-account-2026-09-20.md`, section "Complete
accounting"). That closure holds by construction, so it cannot catch a keying error: a wrong key
moves dollars between the Mexican-origin group (40.9M, CPS ASEC 2025) and everyone else without
changing any total. The dataset audit found keying errors of $3–14bn each
(`dataset_integrity_2026_09_23/README.md`, rows 1, 5, 6); its tax corrections (about +$30bn
stacked) and spending corrections (about −$30bn) cancel. This lane tests the account's **shares**
against independently published distributions. Say in RESULT.md, in one paragraph, why the national
closure cannot test shares.

## Read first (build on these; do not redo them)

- Keys and allocations: `full_account_receipts_2026_09_20/derived/allocation_keys.csv`,
  `category_allocations.csv`; `full_account_spending_2026_09_20/derived/incidence_keys.csv`,
  `allocations.csv`, `categories.csv`; builders in those directories; `full_account_2026_09_20/`.
- National checks already done: `admin_tax_checks_2026_09_19` (CPS wages vs SSA W-2, +2.25%),
  `admin_transfer_checks_2026_09_19` (programme totals vs administrative totals),
  `health_admin_2026_09_20`, `national_coverage_2026_09_20`.
- Tax-side lanes: `onbooks_share_2026_09_23` (on-books share 0.52), `itin_credits_student_aid_2026_09_23`
  (National Taxpayer Advocate ITIN data), `cps_imputation_keys_2026_09_23`, `dataset_integrity_2026_09_23`
  (README table, `synthesis.py`, `cps.md`, `spending.md`).
- A parallel lane, `admin_benefit_keys_2026_09_24`, covers benefit programmes by ethnicity (Medicaid,
  SNAP, housing, WIC, TANF, UI). Do not duplicate it. This lane covers taxes, refundable credits, the
  all-household distribution, the unauthorized tax side and hospital status reports.

## Arms, in priority order

1. **All households against CBO.** CBO's "The Distribution of Household Income" series (use the
   latest year published; verify it) gives federal taxes by type (individual income, payroll,
   corporate, excise) and transfers (means-tested, social insurance) by income quintile and top
   percentiles. Run the account's receipt and transfer keys on all CPS ASEC 2025 households grouped
   into CBO-like quintiles. Document the differences in income definition, household-size
   adjustment and year; compare **shares** of each tax and transfer by quintile, not levels. A key
   that mis-assigns by income shows up as a quintile-share gap. Translate the largest gaps into the
   group's dollars through the group's own income distribution.
2. **Taxes and credits by ethnicity.** Treasury's Office of Tax Analysis may have published imputed
   race and Hispanic-ethnicity distributions of tax items (lead to verify: a 2023 working paper or
   note on tax expenditures by race and ethnicity using its BIFSG imputation). If it exists, take the
   Hispanic shares of income tax liability, EITC, CTC/ACTC and any other items and compare them with
   the account's Hispanic (any origin) shares under the same keys. Re-running the key construction
   with a Hispanic target is the clean route; document any other. Record other admin-based ethnicity
   distributions of tax items you find (IRS, JCT, TPC).
3. **The unauthorized tax side.** Compare the account's taxes for the imputed unauthorized
   Mexico-born with outside anchors: IRS data on ITIN filers (returns, income, tax), SSA Chief
   Actuary estimates of payroll taxes paid for unauthorized workers and the Earnings Suspense File,
   and ITEP's undocumented-tax estimate (verify the edition, year and figure; decompose per person by
   tax type). Reuse `onbooks_share_2026_09_23`; do not rebuild it.
4. **State hospital immigration-status reports.** Leads to verify: Florida's 2023 law requiring
   Medicaid-participating hospitals to ask immigration status (AHCA reports) and Texas executive
   order GA-46 of 2024 (HHSC reports). If published, compare their totals for unlawfully present
   patients with the account's uncompensated-care line for the unauthorized in those states (the
   line is keyed to uninsured use: `main_case_2026_09_23/`,
   `research/immigration-real-fiscal-and-social-costs-2026-09-23.md`). State the definitional gaps
   (charges vs costs, emergency Medicaid, who is counted).
5. **If time allows:** reconcile one published whole-group account component by component. The
   National Academies' 2017 chapter 8 cross-section for 2013 by generation is the natural one:
   compare per-person taxes and benefits by component for the first generation (all origins) with
   what the account's machinery gives for the first generation (all origins) in 2024, scaled by
   nominal per-capita GDP. Say where they differ and why.

## Deliverables

- `derived/benchmarks.csv`: benchmark, source, year, external value, account value, same
  definition (yes/partly/no), gap, implied $bn effect on the group, direction.
- Scripts, one `test_*.py` with a positive control (reproduce one existing target share from
  `allocation_keys.csv` or `incidence_keys.csv` from the microdata before any new computation).
- `RESULT.md`: which of the account's shares have outside corroboration, which are contradicted and
  by how much in main-case dollars, which remain uncorroborated.

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
  with the next arm.
- A lane adopts nothing. Express each finding as a proposed change to the adopted main case
  ($203.2–249.6bn, `main_case_2026_09_23/`) and, where different, to the proposed audit package
  ($202.9–251.1bn, `dataset_integrity_2026_09_23/synthesis.py`); say which.
- Finish: `RESULT.md` opens with `**Verdict:**` (2–5 sentences: the answer, direction, size, how
  sure), then method, results, what would change it, limits, reproduce commands. Return to the
  parent the RESULT.md path and at most 10 lines.
