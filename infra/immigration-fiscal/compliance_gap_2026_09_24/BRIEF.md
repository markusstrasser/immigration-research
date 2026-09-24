# Lane brief: how big is the edge from breaking labor and tax rules, and do compliant firms lose ground?

Date: 2026-09-24. Operator question: illegal immigrants' businesses "not needing the same scrupels
as normal business and driving other business that are honest out of business".

## What the repo already has (read first)

- `../informal_channel_2026_09_16/RESULT.md`: off-books work costs $1.5–3.4k in unpaid taxes per
  unauthorized adult; one construction study puts the misclassification bid advantage at 4.9% of
  project cost (check whether it is immigrant-specific); coworker wage effects under 1%
  (Hotchkiss et al.; verify); §2 "[GAP] No paper models compliant-vs-noncompliant firm competition
  with immigrant labor". The tax side is already inside the adopted account through the September
  24 tax corrections (`../main_case_2026_09_24/RESULT.md`); do not price lost taxes again.
- `../status_impute_2026_09_16/` (unauthorized imputation on survey microdata) and
  `../construction_housing_supply_2026_09_23/` (ladder 200: the group holds 24.4% of
  construction-trades jobs; its construction gain is already inside the production term).
- A sister lane, `../vending_restaurants_2026_09_24/`, covers street vending; do not duplicate it.

## Tests

**A. Size the compliance edge by industry.** Use these sources:

- The DOL Wage and Hour Division compliance-action file (enforcedata.dol.gov bulk download) for
  2010–2024. Take back wages found, employees owed and civil penalties by NAICS, per case and per
  covered worker.
- OSHA inspections and penalties by NAICS.
- The IRS tax gap for income with little third-party reporting, such as the net misreporting rate
  for nonfarm proprietor income. Quote the IRS publication and table.

State each edge as a percent of payroll by industry. Enforcement records show violations found
where inspectors looked, not their prevalence; say how targeting biases each figure.

**B. Uncovered employment.** By state × industry (NAICS 2–3 digit) × year (2012–2023), compare
ACS workers (IPUMS USA or ACS PUMS) with QCEW covered employment (annual averages). The difference
is work outside unemployment-insurance coverage. There are known definitional gaps: QCEW counts
jobs at the workplace and ACS counts persons at residence, and multiple job holding and
self-employment differ. Calibrate the definitional gap on industries with few immigrant workers.
Relate the uncovered share to the Mexico-born noncitizen share of the industry's workers in that
state, and to an unauthorized share where `status_impute` supports one.

**C. Do compliant firms lose ground?** In state × industry cells, test whether growth in the
uncovered share predicts slower growth in QCEW establishments, employment or average weekly
wages. Cover:

- construction, especially specialty trades 2381–2389;
- landscaping (561730) and janitorial (561720);
- restaurants (7225);
- private households (814);
- agriculture (111–112, where QCEW coverage differs).

Use state-year and industry-year fixed effects and a placebo set of industries with low immigrant
shares. Identification is weak, so say so and report associations as associations. If a design
with a real source of variation exists, prefer it and pre-register it. E-Verify mandates are one
candidate: Arizona's 2008 law and later state mandates, with studies of their effects on firms and
employment (find and read them).

**D. Literature.** Construction misclassification, compliant-against-noncompliant competition,
E-Verify mandates and firm outcomes, and unauthorized coworkers' wage effects. Quote every number
you use, with page or table; cite nothing you have not read.

## Who wins and who loses

For each group, give the sign and a dollar range, or "unpriced" with the reason:

- compliant owners;
- their workers;
- noncompliant employers;
- informal and unauthorized workers (lower pay and no protections; they are mostly in the group,
  so this is a within-group item);
- customers (lower prices, which overlap the production term and the consumer-price lane);
- the budget (already inside the account; name the correction that carries it).

Write `derived/winners_losers_rows.csv` with the columns `group, channel, direction, bn_low,
bn_central, bn_high, population_m, per_person_usd, basis, relation_to_account, counterfactual,
source`. The columns work as follows:

- `direction` is `gain` or `loss`.
- `basis` is `measured`, `modelled`, `assumed` or `unpriced`.
- `relation_to_account` is `inside`, `beside` or `overlaps:<channel>`.

## Gates

- Row counts and expected keys of every fetched file.
- QCEW national totals by 2-digit NAICS match BLS published annual averages for two years.
- The WHD file's case count and back-wage total for one fiscal year match a DOL published
  figure, quoted.
- Every computed specification appears in RESULT.md.

## Boundaries

- Write only inside this directory. Read anything. Do not edit shared files: memos, the FAQ,
  INDEX, the ladder, other lanes, `engine.js` or `package.cjs`. If one needs a change, stop and
  report the exact diff in RESULT.md. Do not commit; the parent re-runs and commits.
- Stub `RESULT.md` first with `**Verdict:** pending` and keep it current.
- Run Python as `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>`, with extra wheels
  as a literal `--with pkg`.
- Fetch with `subprocess.run(["curl", "-sS", "--fail", ...])`, because Python urllib fails TLS on
  this machine. Check content, never status or size. bls.gov needs browser-like headers
  (`sec-ch-ua`, a user agent).
- Keys: `set -a; . ../acquire/config.local.env; set +a` sets `CENSUS_API_KEY` and
  `IPUMS_API_KEY`. Never print them. Redact `key=` in any logged URL. Never run `pgrep -f` or `ps`
  dumps. The IPUMS USA store (`../ipums_usa_store_2026_09_23/README.md`) may already hold what you
  need; check before submitting an extract.
- Before any download over 10 GB, run `df -h` and stop if free space is under 1.5 times the
  payload.
- Evidence: tag claims `[SOURCE: url, page/table]`, `[DATA: file]`, `[CALCULATION: script →
  output]` or `[INFERENCE]`. Steel-man before criticizing, search for disconfirming evidence and
  apply the evidence-symmetry rules in `../../../notes/quant-bias-checklist.md`. Mark value
  judgments `[FRAMING-SENSITIVE]`.
- Recompute any per-capita or per-year figure from pooled years one year at a time.
- RESULT.md style: lead with the outcome in plain words; short paragraphs; tables with units; a
  "Would change it" line; a model self-report line with the exact model id from your environment.
- Final message: the RESULT.md path and at most ten lines.
