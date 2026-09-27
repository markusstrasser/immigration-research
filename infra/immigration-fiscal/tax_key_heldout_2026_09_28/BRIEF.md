# Lane brief: score the final calibrated income-tax key on IRS data it was not fitted to

Date 2026-09-28, 03:40 JST. Parent session immigration-research-1c. Follows the validation memo
(`research/immigration-validation-and-backtesting-2026-09-28.md` §3). The released CPS tax construction misses
the IRS distribution across 19 AGI bins by 25.20pp of total variation, against 2.43pp for frozen IRS shares. The
memo says this is "not a score of the final calibrated key", and it lists "a policy-updated fiscal forecast
against genuinely reserved administrative outcomes" as open.

## Tasks

1. Find the income-tax key the September 27 main case uses. Start from `main_case_long_run_2026_09_27`, its
   `derived/corrections.json` and the lanes it names; the INDEX line with "too flat at the top"; and
   `same_year_tax_2026_09_20` and `admin_tax_checks_2026_09_19`. Record which IRS tax years it was fitted or
   calibrated to.
2. Score that final key on an IRS year it did not use: its AGI-bin distribution of tax after credits against
   the IRS SOI table.
   - Prefer TY2024 if SOI has published it; check for preliminary data first.
   - Otherwise use the nearest unused year, and say why it counts as held out.
   - Use the same score as the memo (total variation across the same 19 bins), with the frozen-IRS baseline.
3. Translate the error into the group's tax: how much would the group's federal income tax move if the key's
   bin distribution matched IRS? Give dollars at both ends of the case. State the assumption that links bins
   to the group.
4. Say whether this is a test of allocation or a forecast, and what it cannot identify.

## Rules

- A new lane in this directory; do not edit other lanes.
- Scripts write to `derived/`; raw pulls go in `_cache/`. Two runs must be byte-identical.
- Quote IRS table titles and cells in `reads/`.
- Write `RESULT.md` first with `**Verdict:** pending`, and append as you go. No commits, staging or stash.
- Never print the Census API key.
- Final message: the RESULT path and at most ten lines.
