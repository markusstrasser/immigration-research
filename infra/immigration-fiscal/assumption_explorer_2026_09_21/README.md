# Fiscal assumption explorer

**Verdict:** One self-contained page (`derived/explorer.html`) evaluates the adopted main case,
v6 of 2026-10-07 ([decision](../../../decisions/2026-10-07-main-case-v6.md);
[lane](../main_case_2026_10_07/RESULT.md)), under any set of assumptions, live. As loaded, its
central preset gives **389.0826–461.4797 bn** a year, the case lane's band at full precision. The
cash set (benefits counted when paid) gives 307.3994–385.3641 bn, and every other reading the lane
ran that the page can set reproduces too. The page shows the first-year budget response
(288.9–336.5 bn, 207.3–260.3 bn counting benefits when paid) and schools at the within-district rate
(361.3–434.9 bn) beside the presets, read from the lane files, because the page cannot compute them.
[CALCULATION: test_engine.js against main_case_2026_10_07/derived/summary.json and main_case_bands.csv;
break_conditions_2026_09_29/derived/c1_arms_oct07.csv]

The evaluator is two files. `engine.js` is the complete annual account's own formula,
`welfare = P + weight * (direct + F)`, over executed allocations and the 3,888 executed production
scenarios. `case.js` applies the case's two payloads and adds what the case lane computes after
the engine: the line and receipt responses in `meta.responses` and the return on public capital in
`meta.capital_return`. `test_engine.js` gates `engine.js` against 2,629 rows of the 497,664-row grid,
all 60 service-response cases, all 32 accounting cases, the four published September 20 headline
bounds and the bands of the main-case lanes of September 23, 24 and 26. It gates `case.js` against
the v6 lane. Worst gap 4.3e-9 bn. [CALCULATION: test_engine.js]

The page has a pinned result bar (the live number, the span of the account's open choices, the
distance from the main case, and the last-touched setting beside its central value and its effect
alone). It has convention columns, an exact Shapley split of the distance from the main case, a
bridge from taxes paid to the result, a sensitivity ranking and the full receipt and spending ledger,
with the allocation rule and response of every line and a table of the return on public capital.
Below the ledger come whose welfare the ledger counts, what four commentators argue (text, no number
under any name), the FAQ-routed objection cards, the whole confidence ladder (298 entries, searchable
and linked to ledger lines) and a Sources section. Every assumption, card, convention and author
statement carries short source labels that open the paper, report, dataset or repo document directly.

## Reproduce

```sh
cd infra/immigration-fiscal/assumption_explorer_2026_09_21
uv run --no-project --with duckdb --with pandas --with numpy python3 build_model.py   # hash-guards upstream
OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl --with numpy python3 scaling_check.py
node test_engine.js
uv run --no-project python3 build_ui.py && open derived/explorer.html
uv run --no-project python3 check_sources.py        # optional: re-fetch every link, rewrite sources_check.json
```

The case's inputs are the case lane's tracked outputs: `main_case_2026_10_07/derived/corrections.json`
(the case, 769 cell edits), `corrections_cash.json` (the cash set, 765), `summary.json` and
`main_case_bands.csv`. When that lane's inputs change, rerun it with `scripts/rerun_lane.py`, then
rerun the gate and the build here. `test_engine.js` also reads the September 23, 24 and 26 main-case
lanes' bands and payloads, which stay in git as the engine's regression record.

## The main case on the page

- **Payloads.** `build_ui.py` inlines both payloads as `window.CASE_PAYLOADS`, and `ui.js` calls
  `Case.create(MODEL, CASE_PAYLOADS)` once. `case.js` refuses a pair that is not one adopted case: a
  payload without capital components, responses or lineage counts; two adoption stamps; or a cash set
  that differs from the case in more than its edits, the pension switch and the lineage meta.
  `test_engine.js` tampers with each and expects the refusal.
- **State.** Beside the engine's fields a case state has `benefits` (`accrual`, the case, or `cash`,
  the cash set), `long_run` (roads, transport and parks and the lines that follow them: the case's
  long-run responses, 0 or 1), `capital` (the case's 2% and 3% return, none, or the 7% private return),
  `enterprises` (`D`, every enterprise responds, or `A`, held out) and `reading` (`low` or `high`). The
  central preset spans both readings, each paired with its end of the general-government band
  (0.6005 and 0.8511 of average cost), as the lane pairs them.
- **Cost.** `cost = −(engine welfare) + fiscal weight × capital return`. The case's service responses
  scale with the public-services slider and rental assistance with the benefits slider, as the engine
  scales the lines it answers itself, so the page's sliders keep their meaning. Shares typed into the
  ledger win over the case's. Per-member figures divide by the 42.75 million people of the lineage,
  and per other resident by the rest of the 340.1 million residents.
- **Presets.** `main_case` is central; every other preset `extends` it and lists only what it
  changes, and a setting of `null` removes a band. Numbers are read, never typed: `value_from:
  responses.<path>` reads `meta.responses`, and preset text carries tokens that `build_ui.py`
  resolves from the payload: `{response:<id>}`, `{share:<id>}`, `{elasticity:<id>}`,
  `{people:<field>}` and `{rate:<name>}`. `{assigned:<name>}` is filled from the ledger when the page
  draws.

| Preset | Cost, bn a year |
|---|---|
| Main case | 389.1–461.5 |
| Benefits counted when paid (the cash set) | 307.4–385.4 |
| All services at average cost (the proportional benchmark) | 418.1–475.8 |
| Taxes paid minus benefits received | −118.7 to −101.6 |
| No public services charged | −44.3 to −28.7 |
| Everything at average cost | 703.9–744.1 |
| Production side only | 0.5–0.7 |

  [CALCULATION: case.js on presets.json; a negative cost is a net gain to other residents]

- **Lane readings.** `presets.json` `lane_readings` lists the states the case lane ran too, each the
  central preset with stated changes; `test_engine.js` checks each against its field of `summary.json`
  at 1e-6 bn or its row of `main_case_bands.csv` at the CSV's printed precision, and the status line
  names them when the reader lands on one. The cash set 307.3994–385.3641; every service proportional
  418.1016–475.8387; college and other education budgets fixed too 328.3312–428.2095; no return on
  public capital 352.5010–400.4155; capital at the private 7% 480.5364–542.8987; enterprises held out
  372.3212–438.6484; rental assistance at 0 384.5937–456.9909; general government held fixed
  356.3820–413.5857 (CSV).
- **Readouts.** Two figures of the case sit beside the presets, read by `build_ui.py` from the file
  each names, because the page cannot compute them. The first-year budget response keys roads by
  household resources, which changes the case's own data, and the CSV it comes from must carry this
  case's band in its `adopted` row (the build checks it at the CSV's precision). Schools at the
  within-district rate need the group's share of pupils, which the case lane holds.
- **Ledger.** Amounts are the case's: the data corrections and the 3.04 million added descendants
  are in every line. The case's own lines (schools priced where the group enrolls, colleges keyed by
  use, care and shelter constants, roads by vehicle miles, three state price levels) form the last
  spending group under plain names; `build_ui.py` refuses a payload line or receipt line that `ui.js`
  does not name. The capital table groups the 28 components by the line whose response they follow;
  the four user-fee offsets sit with the component they adjust, and the eleven enterprises form one row.
- **Printed sums.** The bridge, the Shapley split, the ledger groups and the capital table round their
  parts by largest remainder, so printed parts add to the printed totals, and the bridge prints its
  changes against the main case in a column that adds to the printed difference. A rendered-page
  probe checked 20 to 23 sums at the main case, at every preset, in all three views and after
  stacked changes on 2026-10-08, with no mismatch.

## Gates

`test_engine.js` ends `PASS: 2629 grid rows, 60 service cases, 32 accounting cases, 4 headline bounds,
22 lane bands (...); main case as loaded 389.0826 to 461.4797 bn, cash set 307.3994 to 385.3641 bn,
9 lane readings, 7 presets, 2 readouts, per-member figures, attribution closure, 3 case guards, 1692
corrected shares on their base; worst gap 4.28e-9 bn`. Three negative controls fail it (2026-10-08): the
central preset's general government a hair off the case's response, a lane reading given the wrong
change, and one payload edit moved by 0.01 bn.

The share-base check found one cell where the case's payload gives the group part of a national
amount of zero: the added descendants' edit carries +0.4474 bn of corporate tax borne by labor to the
all-capital incidence rule, under which that line is zero nationally. The reference rule is unaffected,
and the page counts that line only when a reader picks that rule and moves the corporate-tax response
off 0. The test names the cell, reported to the case lane on 2026-10-08, and fails on any other.

`build_ui.py` refuses to build when the payloads are missing or malformed, a preset sets a path the
case cannot honour (an unknown field, a case option outside its values, a band without its point
value), a lane reading names no band, a readout's file is not on this case, a token does not resolve,
an `{assigned:...}` name is undefined, or a source names a place that is not on the page.

## Objection cards

`context.json` is rebuilt with `build_context.py <inventory.json>`. A value is kept only when every
number in it equals, at its printed precision, a number within two lines of the cited file:line. Since
2026-10-08 the build fails loud: a value or card that does not verify stops it (exit 1, context.json
unwritten) unless `--allow-drop <id>` names the card. On the cards of 2026-09-26 it refused 133
failures (114 of 250 values; 19 of 57 cards would have lost every value).

The cards were rebuilt on 2026-10-08 on the current documents by `cards/build_inventory.py`
(inventory `_cache/inventory_2026_10_08.json`, from `context.json` at cb3c2e6c): 61 cards and 251
values, all verified, with no `--allow-drop`. Each card's objection is its FAQ entry's heading or
steel-man, checked sentence by sentence, and every number token in an objection, finding, combining
rule or value label equals a value of the card or a number at a line it cites. 46 cards were
rewritten to main case v6 and the current documents (the generation-ledger cards carry item T),
eight kept their text with refreshed rules or citations, and seven were added: one per FAQ entry 18,
20 and 21, two for entry 19, the legacy financing comparisons beside entry 2 and the main case's own
generation split. Three were dropped because no living document carries their figures any more: the
September 20 account's 356.84 bn stress test, the financing projection on the superseded
complete-account balance and the ledger's arms grid before item T. No card adds to the main case.
`sources.json` follows the cards: a repo document a card cites supports that card, the earlier
cases' main-case lanes support none and left the registry, and so did three external sources that
only the dropped cards used.

The numeric gate confirms that a number is printed at its cited line, not that the source still
stands behind it. A value a source marks stale, or that the FAQ has since corrected, passes it and has
to be replaced by hand.

## Ladder

`ladder.py` parses `research/immigration-confidence-ladder.md` at build time, so the page carries the
ladder's own sentences: 298 entries on 2026-10-08, 128 current, 119 qualified and 51 historical.
Status is mechanical: entries 1-51 are the dated earlier layers; an entry is `qualified` when it opens
with a bracketed correction, is named in the file's opening correction notes, or is named by a later
entry as replaced, superseded, qualified or narrowed. Topics and ledger links are keyword rules, and
the page says so. Only current entries show by default.

## Sources and links

`sources.json` is the registry: 102 external sources, each with authors, year, title, venue, link, a
short label, the places on the page it supports (`control:<id>`, `card:<id>`, `preset:<id>`,
`readout:<id>`, `argue:<author>:<n>`, `ledger`, `capital`, `production`, `standing`) and where this
repo cites it (`repo_ref`, file:line), and 33 documents of this repo (`kind: repo`, with the file's
`path`): the v6 decision and lane, the decisions the case builds on, and the lanes behind its parts.
The page opens repo documents locally and lists them after the external sources. The links were mined
from citations already in the repo; 16 are marked `resolved`, built from an identifier the repo
records. Bibliographic details were checked against Crossref or the publisher's `citation_*` tags
where the repo's note and the record disagreed. [SOURCE: sources.json]

`check_sources.py` fetches each link once and writes `sources_check.json`, a dated receipt. On
2026-10-08 every link was fetched again and 88 of 102 answered, five more than at the checks of
September (the Marginal Revolution posts). The rest return 403 to a script (five CBO pages, DHS, CGD,
PNAS, SSRN and four journal articles, three of them reached through doi.org) or are not fetched by rule (x.com); the
page marks each "open it by hand". A file named in a reference becomes a local link only when it
exists in this checkout.

The places that carry no outside source are printed by the build: three author summaries, three
conventions and the assumptions the account sets itself (among them labor share, labor-supply
response, capital adjustment, fiscal weight and the interest and transfer responses). The page labels
those "No outside source: the account sets this itself".

## Evidence for general government

The published account held defense **and** general government at zero response. The engine separates
the two (`general_government_response`). `scaling_check.py` gives the evidence for treating them
differently [CALCULATION: scaling_check.py -> derived/scaling_check.json]:

- BEA Table 3.16, 2024: general public service outside interest is 475.8 bn, 63% of it state and
  local. Federal tax collection and financial management is 36.6 bn; federal executive and
  legislative 137.9 bn. [DATA: bea_nipa/Section3All_xls.xlsx, T31600-A lines 3, 4, 6, 44, 45, 47]
- Across the 50 states (FY2022), log spending on log population: governmental administration
  0.842 (se 0.039), financial administration 0.789, judicial 0.951; for comparison police 1.041,
  correction 0.975, K-12 0.983. [DATA: _cache/slf2022.xlsx, Census State and Local Government
  Finance Table 1, sha256 4dd123c5...643b9b; census_popest_2024/NST-EST2024-ALLDATA.csv]
- Marginal rates 0.59 (federal executive and legislative fixed, federal tax collection at 0.789,
  state and local at 0.842) to 0.84 (everything at 0.842). The case reads them over a removal of the
  group's size, 12.9% of residents, under a power-law cost: 0.6005 to 0.8511 of average cost
  ([decision](../../../decisions/2026-09-26-main-case-finite-removal-and-consumption-key.md)).
  [INFERENCE: a cross-section shows long-run scale, not a measured response to this group]
- Federal police, courts and prisons (82.8 bn, FBI included) are charged inside
  `public_order_safety`, by use; this is not an added cost. Defense and interest on debt already
  issued stay at zero.

## Wording

A separate-context editing pass (`/de-slop`, 45 findings) found the page speaking the build's
language. Options, allocation rules (named from the two upstream builders and guarded at build time),
statuses and card labels use reader words. The payloads' own line labels are the builders' and never
reach the page.

## Limits [FRAMING-SENSITIVE]

- Number columns are accounting conventions, never people: no commentator produced a number for this
  population. The authors section is text with audit references, the object each claim is about, and
  the closest convention where one exists. Caplan has none.
- The ledger counts other US residents only. The group's own gains (the place premium) and Mexico's
  side are computed in the world ledger (`world_ledger_2026_09_27`), which sets the main case against
  the group living in Mexico and states the weight at which the sum changes sign. The page points to
  it and does not net it.
- The case's 9 lane readings are reproduced exactly. Any other setting is an exact evaluation of the
  same formula; the status line says whether the case lane ran the state, the page computes a
  convention or a combination with the case's formula, or a setting is one the case never uses.
- Two figures of the case cannot be set on the page and are read from lane files (the readouts).
  Moving an assumption does not move them.
- One income year of the resident lineage. No generation split, lifetime value or policy effect; the
  cards say which outside results overlap. Crime victims' harm, free hospital care absorbed outside
  government budgets, rent transfers and mobility insurance are priced beside the account
  (`research/immigration-real-fiscal-and-social-costs-2026-09-23.md`), never inside it.
- The production block is CES; increasing-returns arguments are outside it.
- Compiled through an LLM (`notes/llm-bias-caveat.md`): the ledger numbers are gated; the readings of
  authors and the ladder's keyword links are not.
- One light theme, set as a printed handout after Tufte: off-white paper, one serif, rules only where
  a table needs them, native form controls, colour on data marks only. The mark outlines (#5c97d2,
  #ca7a5e) pass the palette validator on the paper colour; the pastel fills do not reach 3:1 against
  it, so every bar carries its value and the ledger tables repeat the chart.
- Checked at 1400 px and 390 px with no horizontal overflow and no page errors. The template must
  open with `<!doctype html>` (the build refuses otherwise): without it browsers use quirks mode and
  the ledger tables stop inheriting the text colour.

The page's earlier cases (September 20 to 26) and how it carried them are in this file's history
(at d434f272 and before) and in the decisions.
