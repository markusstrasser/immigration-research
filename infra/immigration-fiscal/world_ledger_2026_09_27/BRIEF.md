# Lane brief: the world ledger, with the second generation, recipients' valuations, the cost of raising the taxes, and weights

Date 2026-09-27. Parent session immigration-research-1c. The operator asked, after the chat answer on Caplan and
Yglesias ("global GDP goes up"):
- "If the tax is regressive ... then a dollar in a lower class person (dumber) is worth less than a competent person
  that had it stolen ... but idk if that was ever modelled well ... or is even true";
- "and how to model the 2nd gen ... that's a loss... they don't send remittance".

## What exists (read first; none of it is committed)

`/private/tmp/claude-501/-Users-alien-Projects-immigration-research/95a94bd8-dcdc-4501-bb8e-5f9906dddc53/scratchpad/placegain.md`
is the chat-level answer. Treat it as a lead to verify, not a result.
- It sums the first generation's place premium, $224.6bn (Clemens–Montenegro–Pritchett's Re 2.46 on the 12.22m
  Mexico-born members' $378.4bn of US earnings), with `winners_losers_2026_09_24/derived/group_frame.csv`.
- Equal weights give about +$150bn a year. The break-even weight on the group is w* ≈ 0.68, under
  W = N + wM (`research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md` line 21).
- It leaves out four things:
  - any place premium for the second and third-plus generations ("none computed");
  - recipients' valuation: services are counted at cost;
  - the cost of raising the taxes;
  - Mexico's side.

## Questions

1. **What is the second generation's place premium?** The counterfactual is the same person born and raised in
   Mexico by parents who stayed.
2. **What does the group value its services at, rather than their cost?** Avoid double counting: schooling's
   investment value shows up as the second generation's earnings.
3. **What does raising the revenue cost?** Take it under both of the account's payer conventions (ladder 194: tax
   shares, which are progressive, and per-person cuts, which are regressive).
4. **How does the sum depend on the weights?** Compare:
   - equal weights, with a marginal cost of public funds;
   - Hendren's efficiency weights;
   - log-income (inequality-averse) weights, with PPP incomes for people in Mexico;
   - the operator's moral weight w on the group, as a break-even table.
5. **What is Mexico's side?** Remittances by generation, and what the repo can and cannot say.

## Method

### A. Second-generation premium

- **US side.** The second generation's 2024 earnings, by age, sex and schooling, from the repo's CPS or ACS files. Use
  the same member count and definitions as the account's generation split
  (`generation_account_2026_09_24/derived/generation_results.csv`).
- **Mexico side.** Earnings in Mexico of adults whose parents had the schooling of the second generation's parents.
  - Sources to try, in order:
    - ESRU-EMOVI 2017 (parental schooling and the respondent's own income; check the access terms);
    - INEGI's ENOE or ENIGH 2024 (free), combined with an intergenerational schooling transition from EMOVI's
      published tables or from Mexican census co-resident children;
    - IPUMS-International's Mexico samples, if a key exists. Check the variable names in
      `acquire/config.local.env` only; never print values.
  - The parents' schooling distribution: the first generation of the right arrival cohorts (CPS 1994–2000
    Mexico-born parents of children now 25–54), or any repo source with parental schooling. The repo's ladder 178
    lane (IPUMS-CPS ASEC 1994–2025) is the nearest.
- **Selection.** Clemens–Montenegro–Pritchett place the average emigrant at the 56th percentile of residual wages.
  Bound how much of that the children inherit: none (children of stayers with the same schooling) and all.
- **PPP and employment.** Use the same PPP conversion as the first generation's premium. Report employment and hours
  in each place, not an assumed equality.
- **Third-plus generation.** Report only what can be bounded; the counterfactual is two moves removed. Say so.

### B. Valuation instead of cost

For each spending line the group draws on, take a willingness to pay per $1 of cost from primary sources. Hendren &
Sprung-Keyser (QJE 135(3), 2020) give, for example:
- adults' in-kind transfers 0.65–1.04, with food stamps $0.62 per $1;
- cash welfare and tax credits from below zero to 1.20;
- health insurance for adults 0.40–1.63.

For Medicaid for adults use Finkelstein, Hendren & Luttmer (JPE 2019); verify its figures.
- **Public goods and general services.** Value them at average cost as the convention, and say so.
- **K–12 schooling.** Count the resource cost on the payers' side. On the group's side, credit only its current
  consumption value, since the investment return is inside the second generation's earnings premium; state how you
  value it. A double count here is the main trap.

### C. Cost of raising the revenue

- **Marginal cost of public funds.** Sensitivity at λ ∈ {1.0, 1.16, 1.5}. The 1.16 is Hendren & Sprung-Keyser's
  lowest estimate for top-rate changes; source the others.
- **Hendren's efficiency weights (JPubE 187, 2020).**
  - Weights g(y) run from about 1.15 at the bottom to 0.65 at the top.
  - Taking $1 of revenue from people at income y costs them 1/g(y) of surplus, so their weighted loss equals the
    revenue raised.
  - Apply g(y) to every party's surplus, the group's included, at its US income.
- **Payer conventions.** Show both ladder-194 conventions (tax shares; per-person cuts), from
  `distribution_weights_2026_09_23`.

### D. Weights

The table has one row per party and one column per weighting. Parties:
- other US residents today;
- future taxpayers;
- the first, second and third-plus generations;
- residents of Mexico.

Columns:
- equal;
- equal with λ;
- Hendren;
- log income (ε = 1);
- the break-even w on the group.

Show which parties' weights come from measured incomes and which are assumed.

### E. Mexico's side

- **Remittances.** $62.8bn from the US to Mexico in 2024 (Banxico via the winners lane). US-born senders are capped
  at $3.7bn, under 1% of the second generation's wages (ladder 90). Remittances move money within the world, so
  they change the sum only under unequal weights.
- **Other effects.** Stayers' wages (sign only in the repo), lost taxpayers, and human capital. Mark each as
  measured, bounded or a gap.

## The case

The fiscal rows must come from the main case of 2026-09-27 (`main_case_long_run_2026_09_27`, case key `sept27`), once
the winners lane is re-run on it. Build everything that does not depend on the case first: A, B's ratios, C's
weights, E. Read the case through a flag defaulting to `sept26_schools`. **Do not report final numbers until the
parent sends the sept27 pins.** Then run on `sept27` and report both.

## Outputs (`infra/immigration-fiscal/world_ledger_2026_09_27/`)

- scripts;
- `derived/world_ledger.csv` (party × weighting), `derived/g2_premium.csv` and `derived/valuation.csv`;
- `reads/` with a quoted source excerpt for every number taken from a paper;
- `RESULT.md`, opening with `**Verdict:**`.
  - Say which of the operator's two claims the evidence supports: the transfer leaks, and a dollar is worth less
    to the poorer, less productive recipient. Steel-man each, and quote what would falsify it.
  - Give the files covered and skipped, and every judgment call.

Tag every number: [SOURCE], [DATA], [CALCULATION], [INFERENCE] or [TRAINING-DATA]. [FRAMING-SENSITIVE] applies to
every weighted total.

## Rules

- Do not commit, stage or stash. The checkout is shared. Edit only this directory.
- Raw downloads go in an ignored `_cache/`, with a `.gitignore` in the lane.
- Firecrawl is out of credits. Use Exa or direct HTTP with a generic User-Agent. No personal identifier in any
  request header or payload.
- Verify every paper figure against the primary text. The corpus is `~/Projects/corpus`; use the research MCP's
  `corpus_lookup` / `fetch_paper`.
- Run Python as `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>` from the repository root. Write CSVs
  with `lineterminator="\n"`. Two runs must be byte-identical.
- Stub `RESULT.md` with `**Verdict:** pending` first, and append as you go. Final message: the RESULT path and at most
  ten lines.
