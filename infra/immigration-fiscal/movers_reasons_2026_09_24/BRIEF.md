# Lane brief: why natives leave California, and whether it tracks the Mexican-origin share where they lived

Date: 2026-09-24. Operator question: "the harm of just not wanting to live in a failed state with
32% hispanics that is rotten and moving? ... And people moving from CA to Austin etc?"

## What the repo already has (read first)

- `../housing_supply_ca_tx_2026_09_22/` and
  `../../../research/immigration-housing-supply-ca-tx-2026-09-22.md` (ladder 180):
  - native non-Hispanic white adults left California on net at 11.73 per 1,000 in ACS 2024,
    against +0.20 for Texas;
  - Texas permits 2.2–2.5 times as many units per resident;
  - California's stock outgrew its population over 2010–2024;
  - the interaction is not identified.
- `../displacement_transfers_2026_09_18/`: no displacement onto transfers; native employment null.
- `../tiebout_sorting_2026_09_18/`, `../school_flight_2026_09_18/` (white flight not reproduced)
  and `../hedonic_composition_2026_09_19/` (no house-price discount for composition that survives
  2013–2023; the sign flips with the price series).
- The ancestry instrument cannot move metro population for 2021–24 (ladders 182, 199).

## Data

- **IPUMS-CPS ASEC, 1999–2025.** Use `WHYMOVE` (main reason for moving, harmonized from 1999),
  `MIGRATE1`, `MIGSTA1`, the county and metro of residence one year earlier where IPUMS carries
  it, `STATEFIP`, `COUNTY`, `METFIPS`, `NATIVITY`, `BPL`, `HISPAN`, `RACE`, `AGE`, `SEX`, `EDUC`,
  `INCTOT`, `OWNERSHP`, `ASECWT` and replicate weights if offered. Submit through the IPUMS API
  (`IPUMS_API_KEY`) following `../acquire/ipums_cps_second_gen.py`, which pulled extract 1 on
  September 22. Check the variable names and availability against the IPUMS documentation.
- **Census public ASEC files, 2019–2025** (`NXTRES`, `MIG_ST`), as a check on the IPUMS coding.
- **IRS SOI state-to-state and county-to-county migration flows**, 2011–2022: returns, exemptions
  and AGI.
- **ACS**: county or PUMA housing costs and composition, for controls.

## Questions

1. Among US-born adults who moved from California to another state, what share gives each main
   reason? Cover housing (cheaper, better, own home), jobs, family, "better neighborhood/less
   crime", climate, retirement and other. Break it down by year, race and ethnicity, education and
   income. Compare with US-born leavers of other large states (New York, Illinois, New Jersey,
   Massachusetts, Washington) and with US-born movers into Texas. Pool years for precision and
   give standard errors.
2. Among leavers, does the neighborhood/crime share vary with the Mexican-origin or Hispanic share
   of the origin county or metro? Control for housing costs and income. This is descriptive; state
   the limits (CPS county identifiers cover large counties only; the reason is one self-reported
   main reason).
3. Who leaves? Compare the AGI per return of California-to-Texas flows with California stayers
   (IRS SOI). Give the state tax those leavers took with them: a transfer between states, not a
   national loss.
4. For the ledger: how many US-born leavers a year give neighborhood/crime as their main reason?
   Give a cost range for those moves from published moving-cost estimates, read and quoted. The
   category mixes crime, schools and neighborhood quality and cannot isolate ethnic composition,
   so the figure is an upper bound for composition-driven moves. Say so.

`[FRAMING-SENSITIVE]` This lane measures stated reasons and actual moves. It does not price
preferences over neighbors' ethnicity; whether to do that is the operator's decision. Report any
survey of why people leave California that you find (for example PPIC or Berkeley IGS polls) as
context, read and quoted.

## Who wins and who loses

Cover these groups, and prefer "unpriced" to a guess:

- US-born movers (moving costs);
- California's and Texas's budgets (tax base moved, a transfer);
- natives who stay (housing-cost relief, if measured).

Write `derived/winners_losers_rows.csv` with the columns `group, channel, direction, bn_low,
bn_central, bn_high, population_m, per_person_usd, basis, relation_to_account, counterfactual,
source`. The columns work as follows:

- `direction` is `gain` or `loss`.
- `basis` is `measured`, `modelled`, `assumed` or `unpriced`.
- `relation_to_account` is `inside`, `beside` or `overlaps:<channel>`.

## Gates

- The IPUMS extract's DDI matches its data (row count, variables).
- The weighted count of interstate movers out of California for one year matches a Census
  published CPS or ACS table within its margin, quoted.
- IRS SOI California outflow returns for one year match the published state file.
- Every computed specification appears in RESULT.md.

## Boundaries

- Write only inside this directory. Read anything. Do not edit shared files: memos, the FAQ,
  INDEX, the ladder, other lanes, `engine.js` or `package.cjs`. If one needs a change, stop and
  report the exact diff in RESULT.md. Do not commit; the parent re-runs and commits.
- Stub `RESULT.md` first with `**Verdict:** pending` and keep it current.
- Run Python as `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>`, with extra wheels
  as a literal `--with pkg`.
- Fetch with `subprocess.run(["curl", "-sS", "--fail", ...])`, because Python urllib fails TLS on
  this machine. Check content, never status or size.
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
