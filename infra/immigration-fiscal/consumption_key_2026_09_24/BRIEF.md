# Lane brief: test the account's consumption key for remittances and saving

Date: 2026-09-24. The outside checks left this key untested (ladder 216: "the consumption, state-local
income and property tax keys remain untested").

## The key

`../full_account_receipts_2026_09_20/builder.py` keys four receipt lines on positive SPM
resources per person (`consumption = SPM_RESOURCES.clip(lower=0)/size`):

- general sales taxes (BEA 3.5 line 20);
- selective excises (3.5 lines 4 and 23);
- customs duties (3.5 line 15);
- personal current transfers (3.1 line 17).

The group's share is 8.104% (`derived/allocation_keys.csv`, row `consumption`). Two known errors
pull in opposite directions:

- **Remittances.** Money sent abroad is not spent in the United States. Banxico received $64.745bn
  in 2024 (verified in `../remit_leak_2026_09_16/RESULT.md`, which also shows that CEMLA's 16.7%
  is an accounting quotient, not a measured sending rate). If the group's resources include the
  earnings it sends, its consumption share is overstated, its sales taxes are overstated, and the
  net cost is understated.
- **Saving.** Higher-income households consume a smaller share of their resources. Other
  residents are richer, so resources overstate their consumption relative to the group's. The
  group's sales taxes are then understated and the net cost overstated.

## Tasks

1. **Remittances.** Find the US share of Mexico's receipts and the share sent by the group's
   members, from primary sources: BEA personal transfers by country, Banxico by country of
   origin, and survey sender rates (ENADID or the Mexican Migration Project), read and quoted.
   Model person-level outflows for the group's senders, calibrated to the national flow. Keep
   the first generation and US-born senders apart, and follow `remit_leak`'s correction on the
   circularity of any first-generation rate.
2. **Saving.** Apply BLS Consumer Expenditure Survey expenditure-to-income ratios by income
   position (quintile or decile tables, spread within bins by the microdata) to every person's
   resources. Check the result directly against CEX tables by Hispanic origin of the reference
   person. Hispanic is not Mexican-origin, so state that transport.
3. **Outside checks.** Compare the corrected key's distribution by income with:
   - CBO's federal excise distribution (ladder 216 found the current key within $2.1bn of it;
     keep or explain that match);
   - ITEP *Who Pays?* sales and excise incidence by income.
4. **Engine run (proposed, not adopted).** Express each corrected key as receipt edits in the
   payload shape of `../main_case_2026_09_24/derived/corrections.json` (`side: "receipt"`, line,
   scenario, `by: {personal, shared}`). Apply them on top of the adopted corrections: evaluate
   `Engine.applyCorrections` on the adopted payload's result, or compose the two payloads, using
   `../assumption_explorer_2026_09_21/engine.js`. Report the main case (low / high) with:
   - remittances alone;
   - saving alone;
   - both.

   Every incidence scenario and both allocations must be covered. Follow `package.cjs`
   `expand()` for how a receipt shift is carried across scenarios.
5. **Symmetry.** Name any other line keyed on resources and treat it the same way.

## Gates

- The current key reproduces 8.104% from the CPS archive before any change.
- The CEX tables used are quoted with table ids and years.
- The engine run with no edits reproduces the adopted band $200.875–246.318bn.
- Every computed specification appears in RESULT.md.

## Boundaries

- Write only inside this directory. Read anything. Do not edit shared files: memos, the FAQ,
  INDEX, the ladder, other lanes, `engine.js` or `package.cjs`. If one needs a change, stop and
  report the exact diff in RESULT.md. Do not commit; the parent re-runs and commits. Main-case
  changes are the operator's to adopt.
- Stub `RESULT.md` first with `**Verdict:** pending` and keep it current.
- Run Python as `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>`, with extra wheels
  as a literal `--with pkg`. Run Node with `node`.
- Fetch with `subprocess.run(["curl", "-sS", "--fail", ...])`, because Python urllib fails TLS on
  this machine. Check content, never status or size. bls.gov needs browser-like headers
  (`sec-ch-ua`, a user agent).
- Keys: `set -a; . ../acquire/config.local.env; set +a` sets `CENSUS_API_KEY`. Never print it.
  Redact `key=` in any logged URL. Never run `pgrep -f` or `ps` dumps.
- Evidence: tag claims `[SOURCE: url, page/table]`, `[DATA: file]`, `[CALCULATION: script →
  output]` or `[INFERENCE]`. Apply the evidence-symmetry rules in
  `../../../notes/quant-bias-checklist.md`.
- RESULT.md style: lead with the outcome in plain words; short paragraphs; tables with units; a
  "Would change it" line; a model self-report line with the exact model id from your environment.
- Final message: the RESULT.md path and at most ten lines.
