# Fiscal assumption explorer

**Verdict:** One self-contained page (`derived/explorer.html`) evaluates the complete annual
account of `full_account_2026_09_20` under any set of assumptions, live. Its evaluator
(`engine.js`) is the account's own formula, `welfare = P + weight * (direct + F)`, over executed
allocations and the 3,888 executed production scenarios. `test_engine.js` gates it against
2,629 rows of the 497,664-row grid (every level of every dimension), all 60 category
service-response cases, all 32 complete accounting cases and the four published headline
bounds (165.1-197.4 and 269.8-288.7 bn); worst gap 4e-9 bn. [CALCULATION: test_engine.js]
Since 2026-09-23 the page's central case is the adopted main case (see "Adopted 2026-09-23"
below). The same gate checks the adopted presets against the main-case lane: central
203.2-249.6 bn, with non-school education fixed 158.9-212.6 bn, and proportional 307.9-341.0 bn.
[CALCULATION: test_engine.js against main_case_2026_09_23/derived/main_case_bands.csv]

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
node ../main_case_2026_09_23/main_case.js           # reads model.json; its tracked outputs must not change
node test_engine.js
uv run --no-project python3 build_ui.py && open derived/explorer.html
uv run --no-project python3 check_sources.py        # optional: re-fetch every link, rewrite sources_check.json
```

`build_model.py` also reads the two use lanes' `derived/summary.json` and adds six allocation
rules (`spending.added_keys` in `model.json` records each rule's base, change and source field).
`test_engine.js` reads `main_case_2026_09_23/derived/main_case_bands.csv` and `inputs.json`. The
CSV prints four decimals, so the gate checks it to half a unit of the last digit and checks the
lane's own identity (published band plus the three changes, from `inputs.json`) to 1e-6 bn.

`context.json` is rebuilt with `build_context.py <inventory.json>`; it keeps a value only when every
number in it equals, at its printed precision, a number within two lines of the cited file:line
(49 of 50 items and all 255 values on 2026-09-21, the dropped item a caveat with no number;
49 cards and 211 values on 2026-09-23 after the adoption).
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

Since 2026-09-23 the registry also lists four documents of this repo (`kind: repo`, with the
`path` of the file instead of a link): the adoption decision, the main-case lane and the justice
and uncompensated-care lanes. The page opens them locally and lists them after the external
sources; `check_sources.py` skips them.

`build_ui.py` refuses to build when a source lacks a link or a repo reference (for a repo
document, when its file is missing from this checkout), or names a place that is not on the page,
and prints the places that carry no outside source. 21 do (2026-09-23): three author summaries,
three conventions (taxes minus benefits, everything at average cost, production only) and fifteen
assumptions the account sets itself (among them labor share, labor-supply response, capital
adjustment, fiscal weight and the service, interest and transfer responses). The page labels those
"No outside source: the account sets this itself" rather than borrowing authority.

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

## Adopted 2026-09-23: general government grows, justice and uncompensated care by use

The operator adopted three changes to the main case on 2026-09-23
([decision](../../../decisions/2026-09-23-main-case-general-government-and-use-keys.md);
[main-case lane](../main_case_2026_09_23/RESULT.md)). The page's central case
(`repo_central_gg`, marked `central` in `presets.json`) carries all three; the proportional
benchmark carries them too, and the September 20 central case stays as a convention
(`repo_central`, general government fixed, justice per head).

1. **General government** responds at 0.59-0.84 instead of zero, read from
   `derived/scaling_check.json` (`composite_low`, `composite_high`). Both values enter the range
   (`general_government_response_band`). The evidence is set out below.
2. **Public order and safety by use.** `build_model.py` adds the rule `use`: the per-head
   allocation with the group's part raised by the justice lane's central change,
   `cj_use_allocation_2026_09_23/derived/summary.json` `central.change_bn` (+5.94 bn, target
   68.37 bn), national total unchanged. `use_raw_coding` applies the lane's raw ethnicity coding
   (`one_at_a_time_change_bn.scaling_raw`, +1.67 bn).
3. **Uncompensated hospital care.** `uninsured_use_low` and `uninsured_use_high` raise the
   group's Medicaid allocation by the part of government uncompensated-care payments that the
   account's keys under-charge, at equal use:
   `uncompensated_care_2026_09_23/derived/summary.json` `inside_undercharged_bn_use_1.0`
   (3.65-5.75 bn). Both ends enter the range (`key_band`). `uninsured_use_07_low` and
   `uninsured_use_07_high` are the 0.7x-use arm (2.12-3.51 bn), selectable in the ledger.

Both added rules sit on lines that count in full in every published profile, so they move the
result one for one. The result is 203.2-249.6 bn for the central case, 158.9-212.6 bn with
non-school education fixed and 307.9-341.0 bn for the proportional benchmark (September 20:
165.1-197.4, 120.8-160.3 and 269.8-288.7 bn). [CALCULATION: main_case_2026_09_23/main_case.js;
test_engine.js reproduces it]

The engine reports a band as a range: `unresolvedRange` evaluates the cartesian product of the
account's open choices, `school_response_band`, `general_government_response_band` and every
`key_band` entry, and returns the minimum and maximum. A preset sets the point value to one end
of each band, as the school band did; moving that control, or choosing another rule for that
line, drops the band.

### Evidence for general government

The published account held defense **and** general government at zero response. The engine
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
- Federal police, courts and prisons (82.8 bn, FBI included) are already charged inside
  `public_order_safety` (per head in the September 20 account, by use since 2026-09-23); this is
  not an added cost. Defense and interest on debt already issued stay at zero.

Adopting this changed the analysis protocol, so it waited for the operator; he adopted it on
2026-09-23 (decision above).

## Limits [FRAMING-SENSITIVE]

- Number cards (`presets.json`) are accounting conventions, never people: no commentator
  produced a number for this population. The authors section is text with audit references, the
  object each claim is about, and the closest convention where one exists. Caplan has none: his
  gains accrue mainly to migrants and his keyhole remedy applies to future entrants, so switching
  benefits off here would only stop counting 364 bn of costs.
- The ledger counts other US residents only. Gains to the group's own members (the place premium,
  where most of any world-GDP gain sits) and origin-country effects are not computed in this repo;
  the page says so rather than netting them.
- Settings off the executed grid are exact evaluations of the same linear formula. The page says
  whether the account ran the exact case, only its formula applies (any mix of executed rules per
  line, since 2026-09-23), or a setting is one the account never uses (the reader's own).
- One income year of a resident stock. No generation split, lifetime value or policy effect; the
  cards say which outside results overlap and none may be added. Since 2026-09-23 police, courts
  and prisons are charged by use. Crime victims' harm, free hospital care absorbed outside
  government budgets and rent transfers are priced beside the account
  (research/immigration-real-fiscal-and-social-costs-2026-09-23.md), never inside it.
- The objection cards (`context.json`) were rebuilt on 2026-09-23 from a fresh inventory: 49
  cards, 211 values, none dropped. Cards lead with the adopted main case and name September 20
  values as such. The numeric gate confirms that a number is printed at its cited line, not that
  the source still stands behind it: values a source stamps STALE, or that the FAQ has since
  corrected, pass it and must be replaced by hand. FAQ 15, FAQ 16 and entry 14's executed nest
  have no cards yet. The id `e12_no_group_crime_cost_in_headline` is kept because `sources.json`
  keys on it, although the card now describes justice charged by use.
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
