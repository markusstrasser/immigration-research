# Lane brief: price what the account leaves free in schools

Date: 2026-09-24. The operator asked what big channels remain unexamined; this one is on the list
the operator approved.

## The gap

The adopted account charges each of the group's pupils 63–66% of average spending per pupil: our
arithmetic on CBO's coefficients for how school spending responds to enrollment
(`../../../decisions/2026-09-20-service-scaling-calibration.md`, `../service_scaling_test_2026_09_20/`).
The other 34–37% is charged to no one. It is either:

1. **economies of scale**: administration, buildings and debt service do not grow with
   enrollment, and nobody loses; or
2. **dilution**: resources per pupil fall for every pupil in the district, including other
   residents' children.

The capacity memo withdrew the old "$0 harm" and left the channel unpriced
(`../../../research/immigration-school-capacity-harms-2026-09-20.md`;
`../../../decisions/2026-09-20-school-quality-unpriced.md`).

## What the repo already has (read first)

- The capacity memo:
  - Jackson–Mackevicius (2024) put the gain from $1,000 more per pupil sustained four years at
    +0.0316 SD, with a 90% range across contexts of −0.004 to +0.067;
  - Jackson–Wigger–Xiong (2021) find −0.0267 SD (SE 0.00566) in white pupils' NAEP scores per
    $1,000 cut;
  - within-school peer studies are small or positive (Figlio et al., ReStud 2024).
- `../school_peer_checks_2026_09_20/` and its memo: Texas and California enrollment and staffing;
  ECLS-K classroom associations.
- `../school_cost_where_enrolled_2026_09_24/` (ladder 215): the group's pupils sit in districts
  and schools that spend about 3.4% more than their states' averages. Compensatory money may
  follow them.

## Tasks

1. **Split the non-response by function.** Use district finance (Census Annual Survey of School
   System Finances, F-33, about 2000–2023) with enrollment and demographics (NCES CCD). Estimate
   how spending per pupil moves with enrollment within districts, by function:
   - instruction;
   - instructional support;
   - administration;
   - operations and maintenance;
   - capital outlay;
   - interest.

   Use district and state-year fixed effects. Use an instrument only if its first stage is
   strong, and report the F. Fixed categories are scale economies. A fall in instructional
   spending per pupil is dilution. Reconcile with the CBO-based 63–66%.
2. **Compensatory funding.** State formulas pay more for poor and English-learner pupils:
   California's LCFF supplemental and concentration grants, Texas compensatory and bilingual
   allotments, Title I and Title III. Measure whether district revenue per pupil rises with the
   English-learner or Hispanic share, and whether instructional resources per other pupil fall in
   the districts where the group's pupils are.
3. **Price the dilution.** Take the fall in instructional dollars per other pupil and apply
   Jackson–Mackevicius (central and 90% range) to get the test-score effect. Convert to lifetime
   earnings with a verified earnings-per-SD estimate, quoting the paper, table and page. Give the
   present value per pupil-year, then national dollars a year for other residents' pupils.
   Class size (pupil-teacher ratios) is an alternative measure of the same resource loss: show
   it, but never add it to the spending channel.
4. **Peer effects** are separate from resources. Summarize the capacity memo's table. Add a peer
   channel only if a measured negative effect exists, with its interval (symmetry rule 1).
5. **Symmetry (rule 5).** If compensatory money raises spending on other pupils in the group's
   districts, that is a benefit to them. Price it the same way and report it in the same table.

## Who wins and who loses

Cover other residents' pupils (by region and district income), the group's pupils and
taxpayers. Write `derived/winners_losers_rows.csv` with the columns `group, channel, direction,
bn_low, bn_central, bn_high, population_m, per_person_usd, basis, relation_to_account,
counterfactual, source`. The columns work as follows:

- `direction` is `gain` or `loss`.
- `basis` is `measured`, `modelled`, `assumed` or `unpriced`.
- `relation_to_account` is `inside`, `beside` or `overlaps:<channel>`.

This channel is beside the account: a human-capital loss, not a budget line. Its tax consequence
comes decades later; state it and do not add it to the annual account.

## Gates

- F-33 national current spending per pupil for two years matches the Census published figure
  within 0.5%.
- The enrollment panel's row counts and district coverage are reported by year.
- Every computed specification appears in RESULT.md, including null ones.
- The earnings-per-SD and Jackson–Mackevicius figures are quoted verbatim with page.

## Boundaries

- Write only inside this directory. Read anything. Do not edit shared files: memos, the FAQ,
  INDEX, the ladder, other lanes, `engine.js` or `package.cjs`. If one needs a change, stop and
  report the exact diff in RESULT.md. Do not commit; the parent re-runs and commits.
- Stub `RESULT.md` first with `**Verdict:** pending` and keep it current.
- Run Python as `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>`, with extra wheels
  as a literal `--with pkg`.
- Fetch with `subprocess.run(["curl", "-sS", "--fail", ...])`, because Python urllib fails TLS on
  this machine. Check content, never status or size: census.gov has returned truncated bodies
  under HTTP 200.
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
