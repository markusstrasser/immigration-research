# Brief: the main case with the return on public capital, long-run road and park responses, and rental assistance

Date 2026-09-27. Parent session immigration-research-1c. Operator, 13:26 JST (figures session): "why wouldn't
you add capital returns to main case? it's the honest value of the thing ... why would you ignore it?";
14:40 JST: "we can maybe add that in if you think the financial intuition checks out and most reasonable world
models would include it". The parent judged that it does, for both the capital return and the roads and parks.
Rental assistance is the same kind of zero, set by classification (parent's call under the 13:22 delegation;
the operator can veto, so it is one switch).

## What changes

The schools case (`main_case_schools_full_2026_09_26`, $258.4885–291.9548bn, end specifications 48 / 11 in
both fill-in methods) gains three things. Nothing else changes.

1. **Long-run responses** for `economic_affairs_services` and `recreation_culture`, from
   `service_response_long_run_2026_09_27/derived/responses.json` (committed bccf478): the low readings at the
   low end, the high readings at the high end. The main case holds both at 0 today (CBO's category lag).
2. **The return on public capital** for every responsive tax-financed line, from the capital lane's
   `capital_return_services_2026_09_27/derived/engine_components.json`. Wait for the parent's message that the
   lane is committed; it is being finished now. It covers roads, transit, parks and public housing, at 2% at
   the low end and 3% at the high end. 7% is reported only, as the social-cost upper bound beside the account.
3. **Rental assistance** (`housing_subsidies`, $60.26bn, key `housing_support`, $7.54bn for the group) at
   response 1, like the account's other capped means-tested transfers (TANF-type assistance and energy
   assistance are household transfers at 1). It is held at 0 today only because NIPA files it as a subsidy
   (`dataset_integrity_2026_09_23/spending.md` item 6). Public housing's capital return takes this line's
   response.
   - **Overlap check first.** Two questions, from primary NIPA texts and tables (3.13, the Handbook ch. 9):
     does this line include federal payments to state and local public housing agencies, and does the
     account's `enterprise_surplus` receipt (−$47.46bn, population key) exclude subsidies received? If both
     hold, that part is charged twice once the line responds. Net it out, or bound it and report the bound.

## Architecture (required)

- **Lane.** New directory `infra/immigration-fiscal/main_case_long_run_2026_09_27/`:
  - `package.cjs` imports `main_case_schools_full_2026_09_26/package.cjs` unchanged and exports the same
    names with the same shapes (`MAIN_SPECS`, `MAIN_PROFILE`, `cost`, `central`, `band`, `RESPONSES`,
    `responsesFor`, `correctionsPayload`, …), plus `stateFor`, `evaluateFull` and `capitalReturn`;
  - `main_case.cjs` runs the gates and writes `derived/`.
  Consumers will add it as case key `sept27`.
- **One state definition.** Add `stateFor(m, spec, profile)` to `main_case_2026_09_24/package.cjs` and have
  its `cost()` call it. When `spec.line_responses` is present it overrides the profile's responses for those
  line ids. This must be backward compatible: rerun `main_case.cjs` in `main_case_2026_09_24`,
  `main_case_2026_09_26` and `main_case_schools_full_2026_09_26`. Each must end "all gates passed", and
  `git status --short` on each of those directories must be empty afterwards. Edit nothing else in them.
- **Specifications.** The schools case's 64 `MAIN_SPECS`, in the same order and indices, each extended with:
  - `reading`: "low" where `gg` is general government's low response, "high" otherwise;
  - `rate`: 0.02 at low, 0.03 at high;
  - `line_responses`: the two lines' blended responses at that reading, and `housing_subsidies: 1`.
  - **Gate:** this tied set gives the same band as the crossed one, which takes the minimum over all 64 at
    every low setting and the maximum over all 64 at every high setting.
- **Profiles.**
  - Give the new main profile an honest name, since the CBO lag no longer applies to roads and parks, and
    export it as `MAIN_PROFILE`.
  - The line responses apply under that profile and its non-school-fixed variant.
  - The proportional reference keeps every service at 1.
  - Report the old main profile, with the capital return on, as a variant row.
- **Capital return.**
  - `capitalReturn(evaluation, spec)` reads `engine_components.json`. It takes every key share from the
    evaluation passed in, so a re-keyed evaluation (for example by generation) splits it. It takes every
    response from that evaluation, or from the long-run subfunction response at `spec.reading`.
  - `cost()` = engine cost + capital total.
  - `evaluateFull(m, spec, profile)` returns `{evaluation, capital: {components, total_bn}, cost_bn}`.
  - If the capital lane's K-12 key (fixed pupil share) differs from the account's own K-12 key from the
    evaluation, use the evaluation's and report the difference at the end specifications.
- **Payload.** `derived/corrections.json` keeps the schools case's `lines` and `edits`; gate that they are
  deep-equal. `meta` adds:
  - `responses.economic_affairs_services`, `responses.recreation_culture` and `responses.housing_subsidies`,
    each with its readings, subfunctions and source;
  - `capital_return`: the rule, rates `{low, high, reported}`, the components and the source with sha256;
  - `previous`, and `decision: decisions/2026-09-27-main-case-capital-return-and-long-run-responses.md`
    (the parent writes the decision file);
  - `beside_the_account.congestion`: the response lane's re-derived congestion, $13.99bn / $12.02bn against
    $19.16bn, from its `net_change.json`.
- **Per-specification table.** `derived/per_spec.csv`, one row per method × specification:
  - cost, engine cost and capital total;
  - capital by component and by level (state and local, federal);
  - the three lines' responses and group amounts.
  Python consumers (`debt_legacy.py`, `propagate.py`) will gate against it.

## Gates (exit 1 and write nothing on failure)

- **Old settings.** With the two lines at 0, rental assistance at 0 and no capital, the package reproduces the
  schools case: every per-spec cost exactly, and the band to 1e-6.
- **Each addition alone** reproduces its lane:
  - long-run responses alone: $277.93–321.59bn (`candidate_band.json`), ends 48 / 11, to 1e-6;
  - capital alone on the schools case: the capital lane's core band (`bands.csv`), to 1e-6, or the stated
    K-12 key difference;
  - long-run responses plus capital: the capital lane's combined headline (`combined_bands.csv`, option B).
- **Rental assistance** adds the `housing_subsidies` amount at every specification, less any overlap you net.
- **An independent path.** Apply the payload with `Engine.applyCorrections` and take responses and capital
  from `meta` alone, importing only the engine and `model.json`. It must give the same cost at every
  specification and method (1e-9).
- **Receipts.** The group's receipts do not move; all three additions are spending.
- **Determinism.** Two runs are byte-identical.

## Range

Carry the schools case's components onto the new case, as its `main_case.cjs` does, and add three more:
- `long_run_response`: the response lane's sensitivities (r = b; within-state uncapped; federal fixed at the
  high end; across-state at the high end; held-at-zero lines at 1);
- `capital_rate`: 2% at both ends, and 3% at both ends;
- `capital_definition`: the capital lane's variants.

Report these beside the range, not in it:
- 7%;
- land per 10% of land-to-structure value [GAP];
- rental assistance at 0;
- the congestion change.

## Outputs (inside the new directory)

`derived/`:
- `main_case_bands.csv`: the schools case's columns; variants for the first-year response, the schools case,
  each addition alone, the adopted candidate, 7%, rental assistance at 0, and the other profiles;
- `components.csv`;
- `summary.json`: main case; change from the schools case at fixed specifications and as band move; end
  specifications per method; capital by component and level at the ends; responses; range; other profiles;
  beside-the-account items;
- `corrections.json`;
- `per_spec.csv`.

`RESULT.md` opens with `**Verdict:**`. It gives the candidate band, the move by addition at fixed
specifications, the overlap finding, every judgment call, and the files covered and skipped.

## Validation (from the repository root; report each)

```sh
node infra/immigration-fiscal/main_case_long_run_2026_09_27/main_case.cjs | tail -3        # twice; shasum derived/*
for L in main_case_2026_09_24 main_case_2026_09_26 main_case_schools_full_2026_09_26; do
  node infra/immigration-fiscal/$L/main_case.cjs | tail -1; git status --short infra/immigration-fiscal/$L; done
node infra/immigration-fiscal/service_response_long_run_2026_09_27/engine.cjs | tail -1   # still passes
node infra/immigration-fiscal/capital_return_services_2026_09_27/spec_lines.cjs > /dev/null && echo ok
```

## Rules

- Do not commit, stage or stash. The checkout is shared with the figures session, which owns
  `figures_2026_09_22/`, `main_case_schools_full_2026_09_26/` and `school_capital_return_2026_09_26/`.
  Only run that main case's `main_case.cjs` as the byte-identity check.
- Touch only the new directory and the `stateFor` edit in `main_case_2026_09_24/package.cjs`.
- Take numbers from committed lane outputs. For NIPA facts, use primary texts: tag them `[SOURCE]` and quote
  them. No personal identifier in any request header or payload; use a generic User-Agent.
- Write `RESULT.md` early and update it as you go.
