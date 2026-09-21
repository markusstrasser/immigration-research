# Fiscal assumption explorer

**Verdict:** One self-contained page (`derived/explorer.html`) evaluates the complete annual
account of `full_account_2026_09_20` under any set of assumptions, live. Its evaluator
(`engine.js`) is the account's own formula, `welfare = P + weight * (direct + F)`, over executed
allocations and the 3,888 executed production scenarios. `test_engine.js` gates it against
2,629 rows of the 497,664-row grid (every level of every dimension), all 60 category
service-response cases, all 32 complete accounting cases and the four published headline
bounds (165.1-197.4 and 269.8-288.7 bn); worst gap 4e-9 bn. [CALCULATION: test_engine.js]

The page has a pinned result bar (the live number, its unresolved-convention span, the distance
from the central case, and the last-touched setting beside its central value and its effect
alone), convention cards, an exact Shapley split of the distance from the central case, a bridge
with uncounted-but-assigned amounts, a sensitivity ranking, and the full receipt and spending
ledger with per-line allocation rule and response. Below the ledger: whose welfare the ledger
counts, what four commentators argue (text, no number under any name), the 49 FAQ-routed
objection cards, the whole confidence ladder, searchable and linked to ledger lines, and a
Sources section. Every assumption, card, convention and author statement carries short source
labels that open the paper, report or dataset directly.

## Reproduce

```sh
cd infra/immigration-fiscal/assumption_explorer_2026_09_21
uv run --no-project --with duckdb --with pandas --with numpy python3 build_model.py   # hash-guards upstream
OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl --with numpy python3 scaling_check.py
node test_engine.js
uv run --no-project python3 build_ui.py && open derived/explorer.html
uv run --no-project python3 check_sources.py        # optional: re-fetch every link, rewrite sources_check.json
```

`context.json` is rebuilt with `build_context.py <inventory.json>`; it keeps a value only when every
number in it equals, at its printed precision, a number within two lines of the cited file:line
(49 of 50 items and all 255 values on 2026-09-21; the dropped item is a caveat with no number).
Fabricated numbers at real locations are rejected in memo and CSV files alike.

`ladder.py` parses `research/immigration-confidence-ladder.md` at build time, so the page carries
the ladder's own sentences (171 entries on 2026-09-21: 89 current, 31 qualified, 51 historical).
Status is mechanical: entries 1-51 are the dated earlier layers; an entry is `qualified` when it
opens with a bracketed correction, is named in the file's opening correction notes, or is named by
a later entry as replaced, superseded, qualified or narrowed. Topics and ledger links are keyword
rules and the page says so. Only current entries show by default.

## Sources and links

`sources.json` is the registry: 99 external sources (2026-09-21), each with authors, year, title,
venue, link, a short label, the places on the page it supports (`control:<id>`, `card:<id>`,
`preset:<id>`, `argue:<author>:<n>`, `ledger`, `production`, `standing`) and where this repo cites
it (`repo_ref`, file:line). The links were mined from citations already in the repo. 13 are marked
`resolved`: built on 2026-09-21 from an identifier the repo records (NBER number, DOI, SSRN id, a
Census API template instantiated for 2024, a corrected host). Bibliographic details were checked
against Crossref or the publisher's `citation_*` tags where the repo's note and the record
disagreed (Duncan and Trejo 2017 is ILR Review 70(5), not 71(5)). [SOURCE: sources.json]

`build_ui.py` refuses to build when a source lacks a link or a repo reference, or names a place
that is not on the page, and prints the places that carry no outside source. 22 do: three author
summaries and the assumptions the account sets itself (labor share, labor-supply response, capital
adjustment, fiscal weight, the service, defense, interest and general-government responses). The
page labels those "No outside source: the account sets this itself" rather than borrowing authority.

`check_sources.py` fetches each link once and writes `sources_check.json`, a dated receipt: 79 of
99 answered; 18 returned 403 to a script (CBO, PNAS, SSRN, SAGE, AEA, CGD, DHS, Marginal
Revolution, University of Chicago Press), one host is not fetched by rule (x.com) and Treasury
FiscalData failed certificate verification. The page marks each of them "open it by hand". Two
links the repo pins are dead: MEPS `h256dat.zip` returns 404 and `www.meps.ahrq.gov` no longer
resolves; the registry points at the HC-256 landing page and the host without `www`.

A file named in a reference becomes a local link only when it exists in this checkout (60 on
2026-09-21). Ladder entries keep the links their own markdown carries.

The citation pass corrected three statements, on the page and in `presets.json`: Yglesias's
"would cost taxpayers nothing" is an aside in a sentence about housing reform, with immigration as
the comparison, so the page now says he did not argue it; the 63-66% school response is this
repo's first-order arithmetic on CBO's two regression coefficients (0.37 and 0.34), not a figure
CBO states; and the 1.5-2.5 substitution range follows Colas and Sachs, not the National Academies.

## Wording

A separate-context editing pass (`/de-slop`, 45 findings) found the page speaking the build's
language. Options, allocation rules (47, named from the two upstream builders and guarded at build
time), statuses and card labels now use reader words; `context.json` prose was edited directly in
two passes that compare the multiset of numbers in every string before writing, so no value moved.

## General government: a proposal, not the published account

The published account holds defense **and** general government at zero response. The engine now
separates the two (`general_government_response`; the executed grid moves them together, and the
gate sets both from the grid's one column). `scaling_check.py` gives the evidence for treating
them differently [CALCULATION: scaling_check.py -> derived/scaling_check.json]:

- BEA Table 3.16, 2024: general public service outside interest is 475.8 bn, 63% of it state and
  local. Federal tax collection and financial management is 36.6 bn; federal executive and
  legislative 137.9 bn. [DATA: bea_nipa/Section3All_xls.xlsx, T31600-A lines 3, 4, 6, 44, 45, 47]
- Across the 50 states (FY2022), log spending on log population: governmental administration
  0.842 (se 0.039), financial administration 0.789, judicial 0.951; for comparison police 1.041,
  correction 0.975, K-12 0.983. [DATA: _cache/slf2022.xlsx, Census State and Local Government
  Finance Table 1, sha256 4dd123c5...643b9b; census_popest_2024/NST-EST2024-ALLDATA.csv]
- Implied response 0.59 (federal executive and legislative fixed, federal tax collection at 0.789,
  state and local at 0.842) to 0.84 (everything at 0.842). On the 48.3 bn assigned to the group
  that is 28.5-40.6 bn a year: the central span moves from 165-197 to 194-226 (low) or 206-238
  (high). [INFERENCE: a cross-section shows long-run scale, not a measured response to this group]
- Federal police, courts and prisons (82.8 bn, FBI included) are already charged per head inside
  `public_order_safety`; this is not an added cost. Defense and interest on debt already issued
  stay at zero.

Adopting this in the published account is a change of analysis protocol and needs the operator.

## Limits [FRAMING-SENSITIVE]

- Number cards (`presets.json`) are accounting conventions, never people: no commentator
  produced a number for this population. The authors section is text with audit references, the
  object each claim is about, and the closest convention where one exists. Caplan has none: his
  gains accrue mainly to migrants and his keyhole remedy applies to future entrants, so switching
  benefits off here would only stop counting 364 bn of costs.
- The ledger counts other US residents only. Gains to the group's own members (the place premium,
  where most of any world-GDP gain sits) and origin-country effects are not computed in this repo;
  the page says so rather than netting them.
- Settings off the executed grid are exact evaluations of the same linear formula, and are
  labelled as the reader's own assumptions.
- One income year of a resident stock. No generation split, lifetime value, crime-specific cost
  or policy effect; the cards say which outside results overlap and none may be added.
- The production block is CES; increasing-returns arguments are outside it.
- Compiled through an LLM (notes/llm-bias-caveat.md): the ledger numbers are gated, the readings
  of authors and the ladder's keyword links are not.
- One light theme, set as a printed handout after Tufte: off-white paper, one serif, rules only
  where a table needs them, native form controls, colour on data marks only. The mark outlines
  (#5c97d2, #ca7a5e) pass the palette validator on the paper colour; the pastel fills do not reach
  3:1 against it, so every bar carries its value and the ledger tables repeat the chart.
- Checked at 1400 px and 390 px: no horizontal overflow at either. The template must open with
  `<!doctype html>` (the build refuses otherwise): without it browsers use quirks mode and the
  ledger tables stop inheriting the text colour.
