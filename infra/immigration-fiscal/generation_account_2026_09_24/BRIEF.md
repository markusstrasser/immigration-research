# Lane brief: split the adopted complete account by generation

Date: 2026-09-24. The operator approved this as the large structural build.

## Why

The adopted main case ($200.9–246.3bn a year, `../main_case_2026_09_24/RESULT.md`) has no
generation dimension. The only generation split is the September 19 ledger
(`../ledger_absolute_2026_09_17/`): the same-age gap against third-plus non-Hispanic whites is
−$7,584 for the Mexico-born, −$7,521 for the second generation and −$6,195 for the third-plus,
per person. That ledger is a different object and carries none of the later corrections
(ladder 161). The objection "their children pay it back" is answered only on it. Read the FAQ
section "Before combining numbers from different entries"
(`../../../research/immigration-objections-faq-2026-09-21.md`) before writing any comparison.

## Target

The adopted main case, split into three generations on the account's own frame (CPS ASEC 2025
civilian household persons, income year 2024; the 40.896574m canonical target):

- the first generation, born in Mexico;
- the second generation, US-born with at least one Mexico-born parent;
- the third-plus generation, US-born of US-born parents, identifying as Mexican-origin.

Use the canonical masks (`../generation_split_2026_09_20/analyze_cps.py`;
`../full_account_spending_2026_09_20/builder.py` `canonical_target`). Check how the CPS records
parents' birthplaces for people who do not live with their parents, and document it.

## Method

1. **Keys by generation.** The explorer's model (`../assumption_explorer_2026_09_21/build_model.py`)
   is built from these files:
   - `../full_account_receipts_2026_09_20/derived/category_allocations.csv`;
   - `../full_account_spending_2026_09_20/derived/allocations.csv` and its proxy alternatives;
   - `../full_account_benefits_2026_09_20/derived/benefit_scenarios.csv`;
   - the complete-account lane's scenario files;
   - the justice and uncompensated-care summaries.

   For every allocation key, compute the target key total restricted to each generation's
   persons, under both allocations (`personal`; `shared`, equal within the SPM unit, where a
   mixed-generation unit splits by person). Gate: the three generations sum to the group's key
   total for every key, to 1e-9 relative.
2. **Models by generation.** Write your own builder in this lane. It reads or imports the shared
   builders and writes `derived/model_G1.json`, `model_G2.json` and `model_G3plus.json`. Do not
   edit the shared builders. Gate: the three models' target amounts, summed line by line,
   reproduce `model.json`.
3. **Production term.** Attribute the account's production block (the `production` section of
   `model.json`; engine terms P and F) to the generations by each generation's share of the
   group's labor in each skill cell. This is a first-order attribution; state it. Gate: the
   three sum to the group's.
4. **Corrections.** The adopted corrections are 270 edits in
   `../main_case_2026_09_24/derived/corrections.json`, assembled in `package.cjs` from named
   lanes. Split each by generation with a written rule per source lane:
   - **status-based corrections** (tax compliance, the SSN rule on credits, state programs for
     unauthorized residents): the first generation, or its unauthorized subset;
   - **schools priced where enrolled:** by the pupils' own generation;
   - **pooled medical (MEPS):** by the generation make-up of the age × US-birth cells;
   - **long-term care:** by the users' generation;
   - **shelter:** recent arrivals, the first generation;
   - **care work:** by the workers' generation;
   - **Census fill-ins for missing income:** by the generation make-up of the imputed records
     (ASEC allocation flags);
   - **the income-tax key from the outside checks:** by each generation's income position.

   Where no rule is defensible, split in proportion to the line's uncorrected generation split,
   flag it, and report the band that the alternative assignments produce.
5. **Run the engine per generation** over the main case's specifications (`package.cjs`
   `MAIN_SPECS`, both allocations and normalizations). Report each generation's net cost to other
   residents ($bn a year, low and high), per member, and per adult:
   - (a) with children counted in their own generation;
   - (b) with minor children counted in their parents' generation, the convention the National
     Academies' 2017 report uses for school costs (verify its wording and page).

   Both are shown; the choice is `[FRAMING-SENSITIVE]`.
6. **Compare with the September 19 ledger's gaps.** Explain the differences (reference group,
   corrections, object) without scaling one onto the other.

## Gates

- Closure: the three generations sum to the adopted main case for every specification, to
  $0.01bn.
- `node ../main_case_2026_09_24/main_case.cjs` still passes; you do not change it.
- The engine is linear, so the per-generation runs add exactly; test that.
- Unit tests for the masks: counts by generation match `../generation_split_2026_09_20/` outputs.

## Boundaries

- Write only inside this directory. Read anything. Never edit `engine.js`, `package.cjs`,
  `main_case.cjs`, `corrections.json`, any other lane's builder, memos, the FAQ, INDEX or the
  ladder. If a shared module must change, stop and report the exact diff in RESULT.md. Do not
  commit; the parent re-runs and commits.
- Consumers of `ledger_absolute_2026_09_17` verify stored source hashes. Never edit a hash, and
  read that lane only through its own loaders.
- Stub `RESULT.md` first with `**Verdict:** pending` and keep it current.
- Run Python as `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>` and Node with
  `node`.
- Keys: `set -a; . ../acquire/config.local.env; set +a` if you need the Census API. Never print
  keys. Never run `pgrep -f` or `ps` dumps.
- Evidence: tag claims `[SOURCE: …]`, `[DATA: …]`, `[CALCULATION: script → output]` or
  `[INFERENCE]`. Apply the evidence-symmetry rules in `../../../notes/quant-bias-checklist.md`.
- RESULT.md style: lead with the outcome in plain words; short paragraphs; tables with units; a
  "Would change it" line; a model self-report line with the exact model id from your environment.
- Final message: the RESULT.md path and at most ten lines.
