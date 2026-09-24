# Lane brief: do legalized street vendors take business from licensed restaurants?

Date: 2026-09-24. Operator question: "california being flooded with dirt and crime and foodtrucks
from illegals not needing the same scrupels as normal business and driving other business that
are honest out of business?"

## What the repo already has (read first)

- `../informal_channel_2026_09_16/RESULT.md` §2 flags the gap: "[GAP] No paper models
  compliant-vs-noncompliant firm competition with immigrant labor". Its tax side (unpaid taxes on
  off-books work, $1.5–3.4k per unauthorized adult) is already inside the adopted account through
  the September 24 tax corrections (`../main_case_2026_09_24/RESULT.md`). Do not price lost taxes
  again; this lane prices the competition.
- `../../../research/immigration-enclave-neighborhood-quality-and-informality-2026-09-18.md`:
  Mission District storefronts 90.9% registered against 83.6% citywide; LA illegal dumping's link
  to Hispanic share falls from t 5.4 to 1.1 with income.
- `../consumer_price_benefit_2026_09_18/` and
  `../../../research/immigration-consumer-price-and-native-hours-2026-09-18.md`: cheaper services
  to consumers, which overlap the account's production term.

## Question

California legalized sidewalk vending statewide in 2018 (SB 946) and eased the health-code rules
for vendors in 2022 (SB 972). Los Angeles began issuing vending permits after that. Verify each
date and what each law changed from the statute text or the city's own pages before using them.
Did licensed restaurants lose establishments, jobs, payroll or taxable sales where vending grew
most?

## Design (write it into RESULT.md before the first outcome regression)

- **Exposure**, measured before 2018: the Mexican-origin, Hispanic or Mexico-born share of
  residents, and of food-preparation workers, by county and ZIP (ACS 2013–2017). Where it exists,
  a direct vending measure: permits by ZIP, or MyLA311 service requests for illegal vending by ZIP
  and year (LA open data; check availability and coverage years).
- **Outcomes:** County and ZIP Code Business Patterns, 2012–2023, for NAICS 722511 (full-service),
  722513 (limited-service) and 722330 (mobile food services): establishments, mid-March
  employment and annual payroll. QCEW county NAICS 7225 employment and wages. CDTFA taxable sales
  for food services and drinking places by county or city (California open data).
- **Comparisons:** (a) California counties against counties in other states with similar
  pre-2018 Hispanic share and restaurant trends, as an event study around 2019; (b) within LA
  County, ZIPs by vending intensity. COVID breaks the series. Report 2019 alone and 2022–2023
  separately, show pre-trends, and run placebos: grocery (NAICS 4451) in the same places, and
  restaurants in high-Hispanic counties of states without legalization.
- **Licensed food trucks:** does 722330 grow or shrink where unlicensed vending rises?
- **Size:** estimate vending sales. Any published count or sales estimate (for example, Economic
  Roundtable or UCLA reports on LA vendors) must be read and quoted, not recalled. Compare that
  with restaurant sales in the same places. It bounds the sales and margins that licensed
  restaurants could have lost.

## Literature

Search for and read studies of food-truck entry and restaurants, evaluations of street-vending
legalization, and formal-informal firm competition. The Mexican misallocation literature is one
example: informal firms surviving on a tax and regulatory advantage. Quote each number you use,
with page or table; cite nothing you have not read.

## Who wins and who loses

For each group, give the sign and a dollar range, or "unpriced" with the reason:

- licensed restaurant owners and their workers;
- vendors;
- vendors' customers;
- the budget (taxes are already inside the account, so say which correction carries them);
- residents near vending (litter or obstruction, only if measured, for example through 311
  complaints).

Write `derived/winners_losers_rows.csv` with the columns `group, channel, direction, bn_low,
bn_central, bn_high, population_m, per_person_usd, basis, relation_to_account, counterfactual,
source`. The columns work as follows:

- `direction` is `gain` or `loss`.
- `basis` is `measured`, `modelled`, `assumed` or `unpriced`.
- `relation_to_account` is `inside`, `beside` or `overlaps:<channel>`.

## Gates

- Row counts and expected keys of every fetched file.
- CBP national NAICS 722 establishments and employment match the published US totals within 0.5%
  for two years.
- The event-study pre-period coefficients are reported.
- Every computed specification appears in RESULT.md.

## Boundaries

- Write only inside this directory. Read anything. Do not edit shared files: memos, the FAQ,
  INDEX, the ladder, other lanes, `engine.js` or `package.cjs`. If one needs a change, stop and
  report the exact diff in RESULT.md. Do not commit; the parent re-runs and commits.
- Stub `RESULT.md` first with `**Verdict:** pending` and keep it current.
- Run Python as `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>`, with extra wheels
  as a literal `--with pkg`.
- Fetch with `subprocess.run(["curl", "-sS", "--fail", ...])`, because Python urllib fails TLS on
  this machine. Check content, never status or size: census.gov has returned truncated bodies
  under HTTP 200. bls.gov needs browser-like headers (`sec-ch-ua`, a user agent).
- Keys: `set -a; . ../acquire/config.local.env; set +a` sets `CENSUS_API_KEY` and
  `IPUMS_API_KEY`. Never print them. Redact `key=` in any logged URL. Never run `pgrep -f` or `ps`
  dumps.
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
