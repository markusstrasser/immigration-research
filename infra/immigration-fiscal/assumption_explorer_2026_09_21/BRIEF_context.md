# Brief: refresh the explorer's objection cards after the September 23 adoption

`context.json` (49 objection cards, built by `build_context.py` from an agent-made inventory that
is no longer on disk) was verified on 2026-09-21 against the September 20 account. Two things are
now wrong:

1. Five cards quote the September 20 account: `headline_cbo_informed_net_cost`,
   `e2_fixed_functions_and_cbo_inputs`, `e4_offset_threshold_is_conditional`,
   `e11_not_a_policy_saving`, `e12_no_group_crime_cost_in_headline` (it says police, courts and
   prisons are "charged per capita"). The adopted main case is $203.2–249.6bn
   (`main_case_2026_09_23/RESULT.md`, `derived/main_case_bands.csv`); FAQ entries 2, 4, 11, 12
   in `research/immigration-objections-faq-2026-09-21.md` now carry the adopted text.
2. The FAQ, the INDEX and other memos were edited today, so many cards' `file_line` citations
   point at shifted lines.

## Do

- Write `_cache/inventory_2026_09_23.json` in the format `build_context.py` reads (derive it from
  the current `context.json` items; read `build_context.py` for the schema).
- Re-anchor every citation whose value no longer verifies at its cited line: search the same file
  for the window where `confirmed()` passes, closest to the old line; if none exists, report it
  (the value may have been corrected; do not guess).
- Rewrite the five stale cards from the current FAQ and main-case text: adopted band first, the
  September 20 figure named as such; e12 must say justice is charged by use (+$5.9bn) and victim
  harm sits outside the fiscal account.
- Run `build_context.py _cache/inventory_2026_09_23.json`, then `build_ui.py` and
  `node test_engine.js`. No card may be dropped silently: list every item that failed
  verification and why.
- Headless look (agent-browser; see the explorer memory's traps) at the objections section.

Write only in `assumption_explorer_2026_09_21/` (`context.json`, `_cache/`). Do not commit.
Report files changed, cards changed, citations re-anchored, anything dropped, gate output, in at
most 10 lines.
