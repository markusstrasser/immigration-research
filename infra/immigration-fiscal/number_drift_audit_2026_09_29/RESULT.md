**Verdict:** The evidence map takes its numbers from files at build time, and every reader-facing number in scope audits clean. At HEAD 856bd5a plus this lane's uncommitted changes, 684 of 824 numbers are checked (the rest are years and non-quantities): all 684 MATCH, with 0 STALE, MISMATCH, CONTEXT-SHIFT or UNSOURCEABLE. Every map number flagged at 263def3 (45 audit rows and 2 ledger cells) is now a placeholder or table row bound to a record in `overview_2026_09_28/quantity_registry.csv` (79 records). build.py lints and tests all 66 bindings and refuses the page on any failure. It also refuses the page when a printed sum does not add up as printed. That covers the ledger tables, at one decimal with the lines fitted to their totals, and the prose sum of the main estimate and the costs outside the budget. That sum now states the pairing's low-end offending assumption, $4bn less, so 322 − 4 + 96 = 414 and 387 + 101 = 488. General administration held fixed reads the engine arm from b3f4d84, −30.27 / −44.34, against my interim −30.3 / −44.3. The five PM2.5 and crash values the page marked approximate now come from `social_spans_priced_count_2026_09_29`, which reruns the air and crash lanes on the 39.7M the account prices. Two print differently, $45bn → $46bn and $40bn → $41bn, and no number on the page is approximate now. The INDEX paragraph where 869c7aa put the scale net on the priced count is now an audited span, and its 16 numbers MATCH. `memo_sweep.py` extends the check to the living topic memos. On HEAD 8aaf046 it flagged 11 quotes of a record's raw-count or other-arm value, on 9 lines in 4 memos, with no false positive on a hand check of all 11 (2 borderline). The lead fixed nine in 869c7aa. The borderline two are in the outside-checks memo, whose header keeps its figures as computed on the September 23 case; the sweep now exempts it while that sentence stands. On HEAD 856bd5a the sweep reads 178 memos and flags 0. The 48 registry records that carried the default treatment "cash; capital return in" now state their own basis; 11 keep the default, where it is true. The page, the audit's findings and the registry check are byte-identical before and after that edit.

Model: claude-opus-5-5

# Reader-facing number drift audit, 2026-09-29

This lane first audited the numbers on the evidence map and in the routing documents. It then built the map's
build-time sourcing and applied every map fix through it. Nothing is committed; the team lead reviews and commits.
The map audit last read HEAD 856bd5a and the working tree at 2026-09-29 11:48 JST. That working tree included the
peer's uncommitted CLAUDE.md edit, which this lane only read. `derived/inputs.json` holds the sha256 of every file
read. The memo sweep's derived files read the memos at HEAD 856bd5a at 11:49 JST.

Since the 263def3 run (05:24), these changes landed:
- ebf8808 applied the document fixes this lane sent. All 13 document bindings now test FIXED.
- b3f4d84 added the `general_government_fixed` row to main_case_bands.csv, which the map now reads. c8ded0e
  refreshed the winners-losers pin that the row's hash moved.
- f40e47e and 923dfbd ran the pending bundle as one set (candidate v4) and restated the INDEX on it. I re-anchored the
  INDEX anchors those edits moved and mapped the new v4 numbers.
- eceab11 rewrote the dataset register, which is outside the audit's spans.
- This lane moved the registry into the map's build and applied the fixes, below. The lead committed them as
  2ae6675 (the map) and b0bf4c2 (this lane), then the printed-sum gate as ea3369a. The prose sum and the capital
  label followed as f058b8a (the map) and 0a4d9dc (this lane).
- `social_spans_priced_count_2026_09_29` recomputed the five approximate values on the priced count, and their records
  now read it (8bdf62a, db03667, 5ccf86d).
- The lead fixed the documents' lane-count crash and PM2.5 figures by hand in 8aaf046. `memo_sweep.py` then extended
  the audit to the topic memos (uncommitted; see "Memo sweep, 2026-09-29"), and the lead fixed its flags in 869c7aa.
- 8aaf046 rewrote three audited INDEX and FAQ lines, which stopped the audit. I re-anchored them (see "Document
  numbers").
- Each registry record that carried the default treatment now states its own basis (uncommitted; see "Registry
  treatments, 2026-09-29").
- 869c7aa also put the scale net on the priced count in an INDEX paragraph that no span covered. It is now the ninth
  INDEX span (see "Document numbers"). The sweep exempts the outside-checks memo (see "Memo sweep, 2026-09-29").
- db5840f and 856bd5a (candidate v4's engine and payload) changed no file the build, the audit or the sweep reads.

## Result

| File | Tokens | Audited | of which bound | MATCH |
|---|---:|---:|---:|---:|
| overview_2026_09_28/groups.py | 267 | 251 | 46 | 251 |
| overview_2026_09_28/build.py (hand-typed text and rows) | 14 | 10 | 1 | 10 |
| overview_2026_09_28/template.html | 59 | 50 | 24 | 50 |
| research/immigration-INDEX.md (current-result spans) | 268 | 232 | 0 | 232 |
| research/immigration-objections-faq-2026-09-21.md | 202 | 127 | 0 | 127 |
| CLAUDE.md (main-case paragraph) | 14 | 14 | 0 | 14 |
| Total | 824 | 684 | 71 | 684 |

[CALCULATION: `audit_numbers.py` → `derived/number_audit.csv`, `derived/extracted_numbers.csv`]

A bound number is the rendering of a `{{q:<id>|<view>}}` placeholder. The audit checks it against its record and lints
the sentence around it, as the build does. The other 613 audited numbers are typed and checked through
`source_map.csv`, as before. Of the 140 numbers not audited, 86 are marked `skip` in `source_map.csv` (the reason is on
each row) and 54 are years in the routing files.

## Build-time sourcing as built

All files sit in `overview_2026_09_28/`:
- [`quantities.py`](../overview_2026_09_28/quantities.py): the only resolver, renderer, lint and binding test. build.py,
  audit_numbers.py and registry_check.py import it; there is no second copy.
- [`quantity_registry.csv`](../overview_2026_09_28/quantity_registry.csv): 79 records. By status: 71 file, 3
  file+text, 3 text and 2 inference. No page site quotes the two inference records.
- [`quantity_bindings.csv`](../overview_2026_09_28/quantity_bindings.csv): 66 map bindings, 38 in groups.py, 19 in
  template.html and 9 in build.py. The `replaced` column keeps what each site showed before.
- [`test_quantities.py`](../overview_2026_09_28/test_quantities.py): 13 tests of the rendering, binding and allocation
  rules; [`test_build_sums.py`](../overview_2026_09_28/test_build_sums.py): 6 tests of the printed-sum gates.

On every run, build.py does the following:
1. It reads each table value through `q(<id>)` from the registry, or through `d(<variant>)` from
   main_case_bands.csv as before. Every hand-typed table value is gone.
2. `check_quantities` lints every sentence that quotes a record against the record's `must_name` and `forbid`. The
   sentences come from groups.py fields, template lines and ledger notes. It then checks that each text binding
   still holds its placeholder. Finally, each table-row binding must carry the record's unrounded values (to 1e-9),
   and the row's label must pass the lint.
3. It fills every placeholder. A value with status `inference` or `needs_file` is wrapped as
   `<span class="approx" title="Approximate. …">`, and its `reader_note`, itself filled, becomes the tooltip. Such a
   record without a `reader_note` stops the build. The page's how-to-read section explains the dotted underline
   only when some number carries it (`APPROX_NOTE` in build.py); none does now.
4. It prints the ledger and the running sums so that the printed lines add to the printed totals, and reads the
   arithmetic back from the rendered tables (`displayed_sum_errors`). See "Printed sums" below.
5. On any failure it exits 1 and writes no page, as it already did for an unfilled `{{`.

Its existing gates still run: the waterfall and its subtotals against summary.json, and the ledger's sum. Four are
new. The September 26 split must match run I, the pairing's high-end fiscal case must be the main case, and the
pairing less its fiscal case must equal `social.items`. The fourth is the printed-sum gate.

### Printed sums

The operator's rule: in a ledger block, the printed lines must add to the printed total. Where whole-billion rounding
breaks a sum, the block prints one decimal ($8.6bn − $6.4bn = $2.2bn). With each line rounded on its own, both
tables broke that rule: the ledger in 6 sums and "Other ways to count" in 4. For example, 295 + 77 was printed as
371, and 317 + 96 as 414.

One decimal alone does not settle it. Rounded on its own at one decimal, the ledger still breaks 5 sums and the
costs outside public budgets 2: 317.5 + 96.3 is printed as 413.7. Two decimals still break 4.

The build therefore does the following for each table:
- It prints whole billions if every line's own rounding adds up. Otherwise it prints one decimal: both tables do now.
- In the ledger, it rounds the main estimate, allocates the category subtotals to it and each category's lines to
  its subtotal. The allocation is `Q.allocate`, largest remainder: the lines nearest a rounding boundary are rounded
  the other way, each by less than 0.1. A line whose two ends round alike keeps its own rounding when another line
  can move instead, so "Sales and excise taxes" prints −4.1 at both ends.
- In the running sums, it rounds every total, and prints each step as the difference of the printed totals around
  it. The build stops if that moves a step by more than 0.1.
- The caption under each table says how many lines are rounded the other way: 6 in the ledger, 2 in the running
  sums (the costs outside public budgets, 96.2 / 100.6 for 96.26 / 100.68).

`displayed_sum_errors` parses the rendered tables. Rows carry `data-sum` marks: subtotal, part and total, or start,
step and running. It checks each sum on the printed numbers, and a table with no marked sums is an error.
`build.py --round-each` rounds every number on its own. That is the positive control: it fails with the 7 broken
sums above. `test_build_sums.py` runs the gate on the operator's example and on the built tables, both allocated and
rounded each on its own. The assumptions table has no sums and still prints whole billions.

Sums stated in prose have a gate of their own, `PROSE_SUMS` in build.py, because the table gate cannot read them. The
one sum now listed is the main estimate, less `pairing.footing_reduction`, plus `social.items`, which must equal
`pairing.total`. The gate checks it at each end, on the values the page prints (`Q.printed_value`). Stated as
"$355bn (322–387)" plus "$100bn (96–101)" against "$450bn (414–488)", the low end read 322 + 96 = 414. The
missing $4bn is the pairing's low-end fiscal case, which prices offending at the Hispanic average. Three sentences
now say so: template 147 and 213, and the social group's why. They quote `pairing.footing_reduction` (4.34 at the
low end, 0 at the high end), and bindings keep each one in place. The central values stay "about", rounded to 5.
The main estimate at template 143 is now a placeholder too, so every part of the sum is bound.

### Record format

| Column | Meaning | Example: `fill_in.effect` |
|---|---|---|
| id | stable key, never reused; the page names this, not a file | `fill_in.effect` |
| label | what the number is, in plain words | the Census income fill-in correction: change to the main case |
| source_path | the file the selectors read | `main_case_long_run_2026_09_27/derived/summary.json` |
| field | selectors, `;;`-separated (the module docstring lists them); `q:<id>` reuses another record | `a=json:main_case ;; b=json:no_fill_in_correction` |
| expr | combines the bound names (`SAFE_BUILTINS` only) | `(a[0]-b[0], a[1]-b[1])` |
| unit | `$bn`, `$tn`, `$k`, `$`, `%`, `x` (a ratio or count), `year`, `M` | `$bn` |
| shape | `scalar`; `ends` (low end, high end); `interval` (min, max); `central_interval` (central, min, max) | `ends` |
| mid_round, ends_round | display rounding: decimals `0`–`2`, or a step `n5`, `n10`, `n100` | `1`, `1`: "$7.0bn (6.7–7.3)" |
| case, period, population, comparison, treatment | what the number measures | September 27 main case; income year 2024; the union, priced 39.71M; none: the group removed; cash; capital return in |
| status | `file`, `file+text` (plus a constant stated only in prose), `text`, `inference` (combined here under a stated assumption), `needs_file` (no file measures it in the page's frame; the value is interim) | `file` |
| must_name, forbid | case-insensitive regular expressions the quoting sentence (or a table row's label) must match, or must not match | `white` for the `gap_vs_white.*` records |
| supersedes, note | the value the record replaced and where it came from; caveats | ladder 208's estimate before adoption, $9–15bn |
| reader_note | the page's tooltip for an approximate record; may hold placeholders | empty: the record is not approximate |

In `treatment`, "cash" means Social Security and Part A on their 2024 cash flows, not accrued (candidate v4's pension
switch). The production term's cash and GDP measures are named as such. "Capital return in" means the 2–3% return on
public capital that the September 27 case added. A record that is not a fiscal figure says what it measures.

The views are:
- one number: `mid`, `value`, `min`, `max`, `at_low_end`, `at_high_end`;
- `range` ("49–62"), `range_unit` ("$49–62bn"), `mid_range` ("$55bn (49–62)");
- `pair` ("$77.3 / $73.6bn", in end order).

The central of an `ends` record is the midpoint of the unrounded ends, and rounding happens once, at rendering. A range
below zero keeps one sign ("−$3.1–3.2bn"), and a range across zero gives each end its sign ("−55 to +71").
Thousands take a comma in every unit but `year`.

The audit reads placeholders the same way. `audit_numbers.py` renders each unit with `Q.fill`. It checks a number
inside a rendering against its record and lint (MATCH, CONTEXT-SHIFT or MISMATCH), and a number outside one through
`source_map.csv`. A drift guard, `check_sites`, stops the audit when its groups.py locators differ from
`Q.groups_sites`, the build's. The audit no longer reads the rendered overview.html, because the substitutions it
covered are now placeholders in the sources.

## The map fixes, before and after

| Site | Before | After | Record |
|---|---|---|---|
| account/f123 | "Against third-generation whites of the same ages, the gap is about $240bn a year (190–290)" | "… about $291bn a year, and $358bn with every item of the ledger priced" | `gap_vs_white.age_matched_partial`, `…_complete` (must name whites) |
| account/f161 | $7,049; $4,093 in a sentence with no comparison group | the same numbers; the sentence names third-generation whites | `gap_vs_white.per_person_*` |
| account/f268 | (20–24); 53–61% | (21–24); 52–61% | `household.net_contributor_share`, `household.top10_cost_share` (derived/row4/) |
| services/f230 why | $52bn (46–58) | the same number; the sentence sets the school capital return aside | `schools.first_year_effect` |
| services/f211; ledger note | 0.60–0.85% per 1% more residents | 0.59–0.84% | `gg.growth_elasticity` |
| conventions/f253 why | (47–72) | (48–72) | `defense.bound` |
| data/f208 | $12bn (9–15) | $7.0bn (6.7–7.3) | `fill_in.effect` |
| data/f225 why | $1.8bn (1.3–2.3) | $3.3bn, or $0.9bn at surveyed amounts | `remittance.sales_tax_effect` |
| social claim and range; template lines 147 and 185 | {{SOCIAL_ADD}}: $95bn (92–101) | $100bn (96–101) | `social.items`: each footing net of its own fiscal case |
| social/f260 | 4,900 deaths; $70bn; (32–123) | 4,800 (approximate); $68bn; (31–120) (approximate) | `pm25.deaths_priced`, `pm25.cost`, `pm25.span_priced` |
| social/f260 why | $47bn | $45bn (approximate) | `pm25.normalized_priced` |
| social/f264 | (−58 to +74); why $42bn (24–73) | (−55 to +71); $40bn (23–70), both approximate | `crash.span_priced`, `crash.fault_based_priced` |
| social/f189; crime range | $29bn | $31bn (30–32); $31bn | `victims.harm` |
| social/f190 | "Rents rise about 1% per 1% more people" | "In the long run rents rise 0.25–0.60% per 1% more people" | `housing.rent_elasticity_long_run` |
| work/f53 why | after 2000 | after 2005 | `instrument.power_lost_year` |
| time range, time/f162, template "Model of past gaps" | $3.3tn | $3.2tn | `backcast.10y` |
| time/f240 | "costs $237k–274k" | "entering at 55–65 costs $235–288k" | `ir5.lifetime_cost_55_65` |
| template "Public services decide the sign" | $65bn (60–70) | $55bn (49–62) | `tally.corrected` |
| template "Assumptions matter more than data noise" | "Single assumptions move the total by $25–85bn" | "The larger single assumptions …" | `assumptions.move_range_above_noise` |
| template "Two accounting choices" | about $323bn (290–356) | about $327bn (295–360), property taxes alone | `property_tax.alone_case` |
| template "Against as many whites" | (315–330) | (317–325) | `comparators.us_whites` |
| ledger | Sales and excise taxes 0 / −1; schools +145 / +160; general administration +28 / +41 | −4 / −4; +148 / +163; +29 / +41 | `consumption_key.effect`, `finite_removal.schools`, gated remainder |
| assumptions | General administration held fixed, −28.5 / −40.6, "approximate" | −30.27 / −44.34 | `gg.fixed_change` (engine arm) |
| alternatives | v3's hand sums: 290.5 / 355.8, then 368.0 / 429.0 | v4's run: 294.70 / 361.82, then 371.41 / 434.84 | `candidate_v4.set_cash`, `…set_accrual_payable` |
| alternatives, beside | Costs outside public budgets +92 / +101 | Offending at the Hispanic average, low end −4 / 0; then costs outside public budgets +96 / +101 | `pairing.fiscal_footing`, `pairing.total` |
| template 147 and 213, social why | the total with the costs outside the budget, $450bn (414–488), with no word on its footing; 213 printed "The $450bn figure adds them" | each adds "Its low end also prices offending at the Hispanic average, $4bn less."; 213 prints "The $414–488bn figure adds them" | `pairing.footing_reduction`, `pairing.total` |
| template 183 | "Return on public capital: about $45bn (34–56)", the ledger line's name for a larger total | "Return on public capital, government enterprises' included: about $45bn (34–56)" | `capital_return.total` (must name enterprises) |
| social/f260 and f264, the five values marked approximate above | 4,800; (31–120); $45bn; (−55 to +71); $40bn (23–70), each with a dotted underline | the same without the mark, except **$46bn** and **$41bn** (23–70) | `pm25.*_priced`, `crash.*_priced`, now reading `social_spans_priced_count_2026_09_29` |

The other bound sites kept their values and are now placeholders or read rows. They are the headcount (39.7M), the
per-member figure ($8.9k, 8.1–9.8), f268's 22%, 11%, 44% and 30%, f211's 0.7 and f253's $60bn. The rest are f264's
$11bn, the back-cast's 2.8–3.7, template's $320bn and the pairing's $450bn (414–488). Three table rows complete the
list: the noise row (20.8), ε = 3 (−13.8 / −9.1) and the pairing's 414 / 488.

### General administration held fixed

The row reads `long_run_non_school_full, general_government_fixed` less `adopted` in main_case_bands.csv, which gives
291.55 − 321.82 = **−30.27** and 343.03 − 387.37 = **−44.34** [DATA: main_case_bands.csv at b3f4d84]. My interim was
−30.3 / −44.3. It added the line's operating effect, 28.24 / 40.02, to its capital return, 2.03 / 4.32
[INFERENCE, now tested]. The engine arm agrees to the interim's rounding. The subagent that built the arm found
that it equals that sum to about 2e-14, because the arm keeps the end specifications 48 / 11
(`scratchpad/gg_variant/RESULT_gg_variant.md`).

The subagent also produced the proof that the bands producer leaves the existing rows unchanged:
- **Baseline:** `node main_case.cjs --out-dir …/before` gave rc 0, and all five outputs were `cmp`-identical to derived/.
- **Variant:** after the edit it gave rc 0 with 63 gates passing. With the new line removed, the bands file is
  `cmp`-identical to the original.
- **Rerun:** `scripts/rerun_lane.py` on the lane reported "IDENTICAL: 11/11 files unchanged".
- **Commit:** the lead committed the row in b3f4d84 ("Gates 63 pass; a rerun reproduces all five outputs and the
  adopted ones are unchanged"). It rebuilt the two hash-pinned consumers, and c8ded0e refreshed the winners-losers pin.

The row leaves out audit row 8, unallocable state and local spending ($1.9bn at the finite factor), which the payload
carries as a constant. Reading row 8 as general government would lower both ends by about another $1.9bn.

### The ledger's September 26 step

The ledger showed the whole September 26 step, +0.04 / −0.62, as "Sales and excise taxes". build.py now splits it
into three parts [DATA: finite_response_2026_09_26/derived/runs.json]:
- the consumption key, run L, −4.05 / −4.05, which the label names;
- the schools' finite-removal response, run F, +3.72 / +3.04, which goes into "Schools, full cost per pupil";
- the remainder, +0.37 / +0.39, which goes into "General administration".

The build stops if the remainder differs from run I (general government with row 8) by more than 1e-3. The total does
not change.

### Other ways to count: candidate v4 (committed in 2ae6675)

At the lead's commit 923dfbd the INDEX restates the pending revision on candidate v4's one-set run, so the map's two
alternative rows now read it [DATA: main_case_candidate_v4_2026_09_29/derived/bands.csv, method mean]:
- **Cash set:** the total becomes 294.70 / 361.82, shown as −27 / −26 = 295 / 362. Before, it was v3's summed items,
  290.5 / 355.8, shown as −31 / −32 = 290 / 356.
- **With pensions counted when earned:** 371.41 / 434.84, shown as +77 / +73 = 371 / 435. Before, it was v3's hand
  sum, 368.0 / 429.0.

The label changes from "with smaller tax fixes" to "with smaller corrections". Several items in the set are not taxes:
public housing's keys (items 1 and 4), the production weights (item 2), workers' compensation (item 7), state
pricing and roads keyed by miles [DATA: v4 attribution.csv].

### The pairing's footing (committed in 2ae6675)

The pairing's low end, $413.7bn, assumes Mexican-origin offending equals the Hispanic average. That puts its fiscal
case at $317.5bn, not the adopted $321.8bn [DATA: real_costs_totals.csv §7, `hispanic` fiscal main case (low);
band_variants.csv sept27 `justice_raw_coding`]. The FAQ and INDEX say so, but the map's table did not. It showed
"Costs outside public budgets +92 / +101", and 92 is the social items' 96.3 less the 4.3 footing change. After the
prose moved to the social items alone, $100bn (96–101), the table disagreed with it.

The beside block now reads:
- main estimate 322 / 387;
- offending at the Hispanic average, low end, −4 / 0, for a total of 317 / 387;
- costs outside public budgets, +96 / +101, for a total of 414 / 488.

Two gates hold this together: the high end's fiscal case must be the main case, and the social step must equal
`social.items`.

### Priced-count values, formerly approximate

Until this round the page marked five values approximate. Each was the air or crash lane's figure on the raw 40.90M,
scaled by its row's central factor, because ladder 274 restated only the central values. The lane
[`social_spans_priced_count_2026_09_29`](../social_spans_priced_count_2026_09_29/RESULT.md) now reruns both lanes' own
functions over their full grids on the 39.71M the account prices. The crash figures also use the NHTS ratios per
person aged 5+, as the pairing does. The five records read its `derived/priced_spans.csv` with status `file`.

| Record | Scaled approximation | On the priced count | The page |
|---|---|---|---|
| `pm25.deaths_priced` | 4,825.46 | 4,825.46 | 4,800 |
| `pm25.span_priced` | 30.78–119.69 | 30.78–119.71 | (31–120) |
| `pm25.normalized_priced` | 45.45 | 45.53 | $45bn → **$46bn** |
| `crash.span_priced` | −55.14 to +71.06 | −55.07 to +70.84 | (−55 to +71) |
| `crash.fault_based_priced` | 40.47 (22.75–70.02) | 40.63 (22.96–69.84) | $40bn → **$41bn** (23–70) |

[DATA: social_spans_priced_count_2026_09_29/derived/priced_spans.csv; the approximations as registry_values.csv
printed them at 0a4d9dc]

Each end moves by its own factor, because the group's share enters both lanes nonlinearly. That lane's RESULT gives
the reasons, and its `derived/end_factors.csv` splits each factor into its parts. The page now carries no approximate
number. The how-to-read sentence on the dotted underline is filled only when a number carries the mark, so it has left
the page too. A positive control, a template copy with one marked number, brings it back.

## Document numbers

All 13 document bindings (`doc_bindings.csv`) test "FIXED: passes now" at 856bd5a, and the audit finds no flagged
number in the INDEX, the FAQ or the CLAUDE.md paragraph. **No document fix is pending.** Since ebf8808, the INDEX
edits for candidate v4 (f40e47e, 923dfbd) rewrote the lines that six INDEX anchors picked. I re-anchored them, dropped
the rows whose text is gone, and mapped the new v4 numbers to the v4 lane's bands.csv and attribution.csv. All
of them MATCH.

8aaf046 put the PM2.5 and crash ranges and the fault-based crash figure on the priced 39.71M in the INDEX and the
FAQ. Its rewrite broke three anchors, two in the INDEX and one in the FAQ, and the audit stopped with `[BLOCKED]`
from then on. I re-anchored two rows, re-pointed five to
`social_spans_priced_count_2026_09_29/derived/priced_spans.csv` (the crash range and the $40.6bn), and mapped the
three new numbers: the PM2.5 range in both files and the INDEX's "39.71M". 869c7aa moved INDEX lines without
changing an audited number. On 869c7aa all 668 audited numbers MATCH, and the 13 bindings still test FIXED.
[CALCULATION: scratch `reanchor_8aaf046.py` → `source_map.csv`; `audit_numbers.py` → `derived/`]

869c7aa also changed a paragraph outside the spans, "Benefits are priced to the same standard as the costs"
(INDEX:233–247). It now gives the scale net on the account's count, +$13.7bn, beside the lane's +$13.9bn. The
paragraph is now the INDEX's ninth span (`INDEX_SPANS`). Its 19 tokens are one year (1970–2000), two skips (the
rule number 5 and the interval's 95%) and 16 numbers, all MATCH:

| Printed | Source | Value |
|---|---|---:|
| $4.1bn ($2.6–13.3bn) | care lane, summary.csv: the additive channels' total | 4.1476 (2.5965–13.3496) |
| $2.7bn; $1.5bn | the same file: native women's hours taxes; the elder-care Medicaid saving, net | 2.69; 1.49 |
| $21.8bn | the care lane's partA_side_view_union_frame.csv: the gross consumer gain | 21.84 |
| 0.75%; $34bn to $30bn | construction lane, supply_headline.csv, case A central: the cost fall; other renters' extra rent without and with the supply response, metro-local | 0.751; 33.86 → 30.42 |
| $38.6bn; $24.9bn; +$13.9bn | scale lane, summary.csv, CZ 1990: the scale arm, the composition arm, the joint net | 38.65; −24.93; 13.93 |
| $0.2bn | the joint net less the parts' difference, 13.927 − (38.647 − 24.929) | 0.21 |
| −$56.6bn to +$84.4bn | the joint net's 95% interval | −56.57 to +84.42 |
| +$13.7bn; 39.7M | restated_pairing.csv, the scale net on the priced count (`scale.net`); audit row 4's headcount | 13.67; 39.71M |
| $109–677bn | scale lane, net_grid.csv: the central scale gain with the Moretti and the Iranzo–Peri college-share estimates | 109.3–676.9 |
| $0.65bn | mobility lane, insurance_summary.json | 0.65 |

[CALCULATION: scratch `map_benefits_span.py` → `source_map.csv`; `audit_numbers.py` → `derived/number_audit.csv`]

"$34bn to $30bn" holds only as the metro-local pair. Its start is ladder 190's $34bn, the housing lane's long-run
central, which is metro-local (33.86 in housing_transfer's arms_headline.csv). The construction lane's headline,
which ladder 200 and real-costs:393 print, is the national-uniform pair, $33.5bn → $29.9bn, and 33.47 rounds to
$33bn. The commit that wrote the INDEX pair, 66e098f, gives $33.5bn → $29.9bn in its body. Neither document names
its geography.

Against HEAD's `source_map.csv`, no row was dropped unaccounted for:
- **6 keys went.** Two were re-anchored with the same number ($68.1bn and $10.6bn). Four held numbers that 8aaf046
  replaced: the lane's crash range and $42.3bn, in the INDEX and the FAQ. Each replacement has its own row now.
- **27 keys came in:** the two re-anchored rows, 7 for 8aaf046's new numbers and 18 for the benefits span.
- **1 row changed:** the FAQ's $42.3bn under "Figures normalized" became $40.6bn, re-pointed to priced_spans.csv.

Every scanned token has a row and every row a token: the audit prints no unused rows, and no token is UNMAPPED.
`doc_bindings.csv` needed no change; no binding's anchor broke.

The audit used to stop at the first broken anchor, and which one it named changed from run to run with set order. It
now lists every broken anchor, sorted. Run on the source_map before the re-anchoring, it names all three, the same
way twice.

## Memo sweep, 2026-09-29

The audit above reads the map and the INDEX and FAQ spans. The topic memos drift the same way, so `memo_sweep.py`
reads every `research/immigration-*.md` except the confidence ladder, the 19 dated audits (a name holding "audit"
and a date) and one memo exempt by its header (see "Exemption" below). Within a memo it skips fenced code, HTML
comments, `Revisions` sections, bracketed record notes and source tags. It resolves the registry through
`quantities.py`.

A record's other values are the numbers a memo may still quote after the record moved on:
- the sibling on the lane's own count (`X_lane` beside `X_priced`);
- each number its `supersedes` names, tagged by what it differs by: the count (the raw 40.90M), an arm (road budgets
  fixed, before the mixed-group correction) or a vintage;
- the current value of a record that `supersedes` names by id (`case.main` names `case.schools_sept26`).

27 records have 74 other values. A memo number quotes one when it rounds to it as printed, does not round to the
current value, carries the record's unit and sits in a sentence naming the item. The item test keeps "Colombia 46.5%"
and "Colombia's output grew by $46.5bn" off the PM2.5 records. The sweep flags a quote in two cases:
- **Unlabelled.** Nothing near it names its basis in a label of its kind. A count takes the lane's `must_name` or a
  count phrase ("on the CPS's 40.9M", "the lanes' own figure"), an arm takes its arm, and any kind takes a date, a past
  tense or "from" just before it. In a table, a caption clause labels only the columns whose header shares a word with
  it.
- **Presented as current.** "Now" or "the adopted main case" stands just before it, or it is a range in the parenthesis
  after a number that reads as the item's current value: "$10.6bn (−$57.7bn to +$74.3bn in the lane)". A label does
  not clear this case.

`derived/memo_sweep.csv` gives per quote: file, line, quoted value, record, current value, class, suggested wording,
the other value with its origin, the label found and the sentence. `derived/memo_sweep_meta.json` records the
revision, the memos read and skipped, the other values per record and the registry's sha256.

### Result on HEAD 8aaf046

Of 35 quotes of an other value, 11 are flagged, on 9 lines in 4 memos, and 24 pass as labelled (count 11, arm 10,
vintage 3). [CALCULATION: memo_sweep.py → derived/memo_sweep.csv]

| Class | Quotes | Where |
|---|---:|---|
| count_unlabelled | 9 | INDEX:243 +$13.9bn; outside-checks:256 and 281 $30.9bn; real-costs:148 14.0 / 12.0, :217 −46.5, :393 +13.9; winners:246 $32.34bn and $30.93bn |
| arm_unlabelled | 2 | real-costs:145 28.9 (before the mixed-group correction); real-costs:156 $19.2bn (road budgets fixed) |

The memos are `immigration-INDEX.md`, `immigration-outside-checks-2026-09-24.md`,
`immigration-real-fiscal-and-social-costs-2026-09-23.md` and `immigration-winners-and-losers-2026-09-25.md`.

**Hand check of all 11.** No false positives; two are borderline.
- INDEX:243: "+$13.9bn … which counts in the fiscal-plus-social total". The total carries $13.7bn (real-costs:27).
- real-costs:145: "28.9 full" in §3's table. The memo's summary table (line 19) prints 30.5 / 31.9.
- real-costs:148: "14.0 / 12.0 … once roads respond". The summary table (line 23) prints 13.6 / 11.6.
- real-costs:156: "The central … $19.2bn". Since September 27 the central lets roads respond (13.6 / 11.6), and
  $19.2bn holds road budgets fixed.
- real-costs:217: the column "Normalized, beside" prints the lane's −46.5. The caption's count label speaks to the
  lane column only, and the sentence under the table gives −$45.5bn.
- real-costs:393: "+13.9 … in the social rows since September 28". The social rows carry 13.7.
- winners:246: "$32.34bn, not $30.93bn" are the lanes' raw-count values. The shares in that row were computed from
  them, so the fix is to name the basis, not to swap the numbers.
- outside-checks:256 and 281, $30.9bn: borderline. The sentences name no count, but the memo's header says "The
  proposals below are kept as computed on the September 23 case". The sweep never reads a document header as a label.

**Against the lead's list,** on 5ccf86d, before the 8aaf046 hand fix: 17 flagged. They include 7 of the 9 values the
lead listed: $42.3bn at INDEX:185, FAQ:49, FAQ:168 and real-costs:226; the lane range after "$10.6bn" at INDEX:185 and
FAQ:168 (count_as_current); and real-costs:217's −46.5. The other two, 217's 31.5 to 122.5 and 218's −57.7 to 74.3,
sit in the column "Lane central (range)" under a caption naming "the lanes' own central and range on the CPS's
40.9M". They pass as labelled, and 8aaf046 kept them. The remaining 10 flags at 5ccf86d are still open on HEAD, as is
the −46.5, which 8aaf046 left.

**After the fixes.** 869c7aa fixed six sites in three memos. On it the sweep finds 34 quotes, and flags only
outside-checks:256 and 281, the borderline pair. [CALCULATION: memo_sweep.py --rev 869c7aa, to scratch]

**Exemption.** The outside-checks memo is a dated audit whose name lacks "audit", so the name rule reads it. Its
header says "The proposals below are kept as computed on the September 23 case.", so its figures are that case's by
declaration, and the lead keeps them unedited. `EXEMPT` in memo_sweep.py maps the memo's path to that sentence and
the reason, which memo_sweep_meta.json lists among the skipped memos. The exemption lasts only while the sentence
stands. If the memo loses it, or the file is gone, the sweep stops with `[BLOCKED]`, so a memo rewritten to current
values is swept again. `test_memo_sweep.py` tests both the skip and the stop.

**Result on HEAD 856bd5a.** Of the 199 topic memos, the sweep reads 178 and skips 21: the 19 dated audits, the ladder
and the exempt memo. It finds 31 quotes of an other value, all labelled (count 17, arm 11, vintage 3), and flags 0.
Without the exemption it reads 179 memos and finds 34 quotes, 2 flagged: the exempt memo holds the two borderline
$30.9bn quotes and one labelled $28.9bn. `derived/` holds the exempt pass. [CALCULATION: memo_sweep.py →
derived/memo_sweep.csv, derived/memo_sweep_meta.json; scratch `sweep_noex.py` for the pass without it]

**The lead's hand fixes, checked.** The sweep reads only other values, so I checked the numbers 8aaf046 and 869c7aa
wrote into the real-costs memo against their sources. All 20 resolve:

| Line | Printed | Source | Value |
|---|---|---|---:|
| 145 | 30.5 / 31.9 on the 39.7M | `victims.harm`; `headcount.priced` | 30.48 / 31.87; 39.71 |
| 148, 167 | 13.6 / 11.6 | `congestion.item` | 13.63 / 11.64 |
| 227 | $30.8–119.7bn (normalized −$45.5bn) | `pm25.span_priced`; priced_spans.csv's normalized central, whose magnitude is `pm25.normalized_priced` | 30.78–119.71; −45.53 |
| 228 | −$55.1bn to +$70.8bn | `crash.span_priced` | −55.07 to +70.84 |
| 228 | $40.6bn ($23.0–69.8bn); $42.3bn on the lane's count | `crash.fault_based_priced`; `crash.fault_based_lane` | 40.63 (22.96–69.84); 42.34 |
| 394 | +13.7 | `scale.net` | 13.67 |
| 395, 545 | +21.7; $22.0bn on the lanes' counts | restated_pairing.csv: restaurant variety 6.79, volunteering 5.98, consumer-side scale 2.13 and trade ties 6.78, restated; the published column | 21.69; 21.96 |

[CALCULATION: scratch `verify_memo_changes.py` on HEAD 856bd5a]

No registry record covers the four smaller benefits, so the sweep cannot see their sum drift (open item 7).

**Limits.**
- It sees only numbers the registry records as another value. Raw-count figures without a record pass: real-costs:145's
  sensitivities (23.5–34.0, 15.4–45.3, 43.1), real-costs:148's "full span 2.0–30.8", and the scale lane's interval
  (−56.6 to +84.4), printed beside the scale net at INDEX:244 (audited as a document number) and real-costs:394.
  `scale.span_lane` has no priced sibling, so its value is a current one.
- A statement of vintage or count at the head of a memo does not label its sentences. `EXEMPT` names the one memo
  where such a statement covers the whole memo.
- Pairing a caption clause with a column by a shared word is a heuristic. A clause that shares no word with any header
  labels the whole table.
- A number whose unit is written only on its partner ("$14.0 / 12.0bn") needs "bn" or "billion" as a word in its
  clause. Real-costs:450's "$14.0" is not read; its partner is, and passes on the row's commit.
- The controls pin current registry values, such as crashes by fault at $40.6bn. A registry change that moves one
  stops the run with `[BLOCKED]` until the control is updated. `test_memo_sweep.py` runs the controls.

**Validation,** 2026-09-29 11:21:30–11:23:01 JST on HEAD 8aaf046, which last changed the INDEX (after 5ccf86d), with
the scratch script `memo_sweep_validate.sh`:
- all 19 positive controls pass on every run. A failed control stops the run with `[BLOCKED]` and writes nothing;
- two passes on HEAD give `cmp`-identical memo_sweep.csv and memo_sweep_meta.json, with `registry_equals_rev: true`;
- a `--worktree` pass gives an identical CSV;
- the pass on 5ccf86d is the comparison above;
- pytest passes 5 tests (test_pairing.py 4, test_memo_sweep.py 1), and `ruff check --select F,E9` passes.

A first run at 11:17:37–11:19:11 gave the same outputs; only the docstring changed between the two runs.

The controls:
- an unlabelled lane-count value is flagged, and the same value "on the CPS's 40.90M" is not;
- another arm's value is flagged, a count label does not clear it, and its arm does;
- an earlier case is flagged unless dated;
- "from" marks only the number after it;
- another unit, another item and the current value match nothing;
- a lane range after the current central is flagged, on one line and across a line break, but not in a clause of its
  own;
- a dated case after "now" is flagged;
- a caption's count label reaches only its column;
- a Revisions section and a bracketed note are skipped.

## Registry treatments, 2026-09-29

48 of the registry's 79 records carried the default treatment "cash; capital return in", whatever they measured.
Each now states its own basis. 11 keep the default because it is true for them: the September 27 case and the changes
measured on it, both candidates' cash sets, the per-member figure and the tornado's spread.

| Treatment now | Records |
|---|---|
| cash; no capital return (added September 27) | 8: the September 26 cases (`case.schools_sept26`, `case.first_year_response`, `schools.first_year_effect`) and the five runs measured on the September 24 case (`consumption_key.effect`, `finite_removal.*`) |
| accrual at payable benefits, net of income tax on benefits (current law); capital return in | 3: `candidate_v3.revised_set_accrual_payable`, `candidate_v3.items_1_7_accrual_payable`, `candidate_v4.set_accrual_payable` |
| a share of members, or of the net cost, from household balances on the September 27 case | 5: `household.*` |
| a social cost beside the fiscal account (in deaths for one) | 4: the air and crash lanes' own-count records |
| not a fiscal figure: a head count, a year, or a count or rate of calibration cases | 6: `headcount.*`, `instrument.power_lost_year`, `review.*` |
| a basis of its own | 11: `capital_return.total` (an imputed resource cost, never a debt flow), `balance.absolute_hull` (the practitioner hull, no capital return), `scale.span_lane`, `scale.induced_receipts_lane`, `care.total`, `care.named_items`, `nest.direct_low_skill_change`, `comparators.us_whites` (A1 accrual or A3 cash, capital return in), `congestion.range`, `backcast.typical_year_change`, `ir5.lifetime_cost_55_65` |

The same default was untrue in other columns of six records, and 14 fields changed with the treatments:
- `review.*` (3): case "not a case: the reviewer calibration lane", period "the lane's run, 2026-09-29",
  comparison "none";
- `instrument.power_lost_year`: case "not a case: ladder 136's instrument test", period "the inflow window
  2005–2023", comparison "none";
- `backcast.typical_year_change`: case "complete account, September 20". The back-cast anchors its gap against the
  average resident on the September 20 complete account (`backcast.py`, `anchors("shared")`), not on the September
  27 case. The FAQ's "falls 4% or rises 11%" already calls it a gap against average residents.
- `ir5.lifetime_cost_55_65`: case "IR-5 lifetime lanes (ladder 247)".

Each record's basis was read from its source: the September 27 summary.json (its schools and first-year cases carry
no capital return), the September 24 runs, the within-group, white-replacement, back-cast, scale and care lanes, the
ladder, and v3's and v4's pension switch. The edit script refuses to write unless the 48 default records are exactly
the 37 it changes plus the 11 it keeps, and each other field holds its expected old value. It writes through the csv
module, which round-trips the file byte for byte. [CALCULATION: scratch `set_treatments.py` →
`overview_2026_09_28/quantity_registry.csv`, 51 fields]

No code reads `treatment`. With the committed registry swapped back in, the page, `number_audit.csv`,
`extracted_numbers.csv`, `registry_values.csv` and `binding_tests.csv` come out byte-identical. The only difference is
the registry's sha256 in `inputs.json` (see Validation).

## Validation

Run at 2026-09-29 06:49:03–06:49:32 JST on HEAD 923dfbd, from the repository root, with
`PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1`. `PY` is `uv run --no-project --offline python3`, `OV` is
`infra/immigration-fiscal/overview_2026_09_28`, `AU` is this lane and `$V` is a scratch directory. One script in the
session scratchpad ran every step below in order.

| Step | Command | rc | Output |
|---|---|---:|---|
| build | `$PY $OV/build.py` | 0 | wrote derived/overview.html: 274 entries, 82 findings, 72 retired, 75 sources; 60 bindings pass |
| second build | `$PY $OV/build.py --out $V/overview_2.html` | 0 | the same |
| builds identical | `cmp $OV/derived/overview.html $V/overview_2.html` | 0 | |
| audit | `$PY $AU/audit_numbers.py` | 0 | audited 662 numbers (799 tokens): MATCH 662 |
| second audit | `$PY $AU/audit_numbers.py --out $V/audit_2` | 0 | the same |
| audits identical | `cmp` of number_audit.csv, extracted_numbers.csv, inputs.json | 0, 0, 0 | |
| registry check | `$PY $AU/registry_check.py` | 0 | 78 records resolved; 13 bindings: FIXED: passes now 13 |
| second check | `$PY $AU/registry_check.py --out $V/rc_2`; `cmp` of both outputs | 0; 0, 0 | |
| tests | `$PY -m pytest -p no:cacheprovider -q $OV/test_quantities.py $AU/` | 0 | 13 passed |
| lint | `ruff check --select F,E9` on build.py, quantities.py, test_quantities.py, groups.py and this lane's three scripts | 0 | All checks passed |

Positive controls. Each changes one bound value or label in a copy, or in place and then restored. Every control
must make the build fail.

| Control | Command | rc | Result |
|---|---|---:|---|
| a typed "$29bn" where f189 quotes `victims.harm` (groups copy) | `$PY $OV/build.py --groups pc/groups_typed.py --out $V/pc_typed.html` | 1 | "{{q:victims.harm\|mid_range}} is not at its site"; no page written (`test ! -e` rc 0) |
| f123 without "whites" (groups copy) | `… --groups pc/groups_nowhite.py --out $V/pc_nowhite.html` | 1 | 2 lint errors, "names none of /white/"; no page written |
| the general-administration row typed as −30.3, −44.3 (build.py in place) | `$PY $OV/build.py --out $V/pc_row.html` | 1 | "row shows (-30.3, -44.3), record gg.fixed_change is (-30.2695…, -44.3384…) (a typed number?)", digits shortened; build.py restored, `cmp` rc 0 |
| `social.items` moved by 0.5 (registry in place) | `$PY $OV/build.py --out $V/pc_registry.html` | 1 | "the pairing less its fiscal case is not social.items"; registry restored, `cmp` rc 0 |
| audit on the typed copy | `$PY $AU/audit_numbers.py --groups pc/groups_typed.py --out …` | 0 | MATCH 660, UNSOURCEABLE 1 (the typed number) |
| audit on the no-whites copy | `$PY $AU/audit_numbers.py --groups pc/groups_nowhite.py --out …` | 0 | MATCH 660, CONTEXT-SHIFT 2 |
| page after the controls | `cmp $OV/derived/overview.html $V/overview_2.html` | 0 | unchanged |

The audit reports and exits 0 when it flags a number. The build is the gate.

The printed-sum gate was validated at 2026-09-29 07:18:41–07:18:52 JST on HEAD b0bf4c2 plus its working-tree change,
with the same commands:
- two builds are `cmp`-identical;
- two audits are `cmp`-identical, and all 662 still MATCH;
- two registry checks are `cmp`-identical;
- pytest passes 21 tests (`test_build_sums.py` adds 4, `test_quantities.py` 4 more);
- ruff passes.

`build.py --round-each --out …` exits 1 with "7 printed sum(s) do not add up" and writes no page. The two groups-copy
controls above still exit 1.

Against b0bf4c2's outputs, the audit's `number_audit.csv` differs only in the line column. The same holds for
`extracted_numbers.csv`, plus five template locators that moved down one line. The captions, the two summed tables
and the new caption line are the only changes on the page. The assumptions table is byte-identical.

The prose sum and the capital label were validated at 2026-09-29 07:28:04–07:28:13 JST on HEAD ea3369a plus the
working tree, with the same commands:
- the builds are `cmp`-identical, with 66 bindings passing;
- the audits are `cmp`-identical, 665 of 665 MATCH;
- the registry checks are `cmp`-identical (79 records, 13 FIXED);
- pytest passes 23 tests, and ruff passes.

Three controls each exit 1 and write no page:
- **Footing record at 0** (registry in place, restored, `cmp` rc 0): "the parts print as 418, pairing.total as
  414".
- **Template copy without the footing sentence at 147** (`--template`): "{{q:pairing.footing_reduction|at_low_end}}
  is not at its site".
- **Template copy whose line 183 drops "government enterprises' included"**: "names none of /enterprise/", and
  its anchor picks 0 lines.

On the page, only the four sentences changed; line 143 renders as before.

The priced-count rebinding was validated at 2026-09-29 10:21:40–10:23:51 JST on HEAD 0a4d9dc plus the working tree,
with the same commands and one scratch script:
- two runs of `social_spans_priced_count_2026_09_29/priced_spans.py` pass all 22 gates, and their three CSVs are
  `cmp`-identical;
- the builds are `cmp`-identical, with 66 bindings passing and no `class="approx"` on the page;
- the audits are `cmp`-identical, 665 of 665 MATCH;
- the registry checks are `cmp`-identical (79 records, 13 FIXED);
- pytest passes 23 tests, and ruff passes on priced_spans.py, build.py and quantities.py;
- no file changed in the lanes that priced_spans.py imports.

A positive control builds from a template copy that carries one marked number (`--template`, `--out` to scratch). It
exits 0, and the how-to-read sentence on the dotted underline is back on that page. On the real page, only the
sentences holding the five values changed: they lost their marks, and two print $46bn and $41bn. The how-to-read
paragraph also lost its last two sentences.

The registry treatments and the re-anchored audit were validated at 2026-09-29 11:38:42–11:39:29 JST on HEAD 869c7aa
plus the working tree, with the scratch script `treatment_validate2.sh`. It first swapped the committed registry
back in and wrote a build, an audit and a registry check to scratch, then restored the edited registry (`cmp` rc 0):
- two builds with the edited registry are `cmp`-identical, and identical to the build with the committed one (66
  bindings pass);
- two audits are `cmp`-identical, 668 of 668 MATCH. Against the committed registry, `number_audit.csv` and
  `extracted_numbers.csv` are identical, and `inputs.json` differs in one line, the registry's sha256;
- two registry checks are `cmp`-identical and identical to the committed registry's (79 records, 13 FIXED);
- pytest passes 24 tests on the overview and this lane, and `ruff check --select F,E9` passes on audit_numbers.py;
- the memo sweep's CSV on 8aaf046 is unchanged, and on 869c7aa it flags 2.

Against the committed derived files, line numbers aside, `number_audit.csv` changes only at the lines 8aaf046
rewrote (8 rows out, 11 in). `extracted_numbers.csv` changes there too, and at four year tokens whose locator moved
with their lines (12 rows out, 15 in). `inputs.json` records the new HEAD and the new hashes of the registry, the
INDEX, the FAQ, the ladder and source_map.csv.

The final state was validated at 2026-09-29 11:48:26–11:49:13 JST on HEAD 856bd5a plus the working tree, with the
scratch script `final_validate.sh`. It first swapped the committed registry in and wrote a build, an audit, a registry
check and a sweep to scratch, then restored the edited registry (`cmp` rc 0). Every step below exited 0:
- two builds are `cmp`-identical, and identical to the build on the committed registry (66 bindings pass);
- two audits are `cmp`-identical: "audited 684 numbers (824 tokens): MATCH 684". On the committed registry,
  `number_audit.csv` and `extracted_numbers.csv` are identical, and `inputs.json` differs in one line, the registry's
  sha256;
- two registry checks are `cmp`-identical and identical to the committed registry's (79 records, 13 FIXED);
- two sweeps are `cmp`-identical: "swept 178 memos at 856bd5a (21 skipped): 31 quotes of other values, 0 flagged".
  On the committed registry `memo_sweep.csv` is identical, and `memo_sweep_meta.json` differs in the registry's
  sha256 and `registry_equals_rev`;
- pytest passes 25 tests on both runs: the overview's `test_quantities.py` (13) and `test_build_sums.py` (6), and
  this lane's `test_pairing.py` (4) and `test_memo_sweep.py` (2);
- `ruff check --select F,E9` passes on audit_numbers.py, memo_sweep.py and test_memo_sweep.py.

The control for the anchor check ran HEAD's `source_map.csv` against the current INDEX and FAQ. It stops with
"[BLOCKED] 3 anchor(s): …" and names all three broken anchors.

## Open items

1. **Done:** the lead committed both table changes (the v4 alternatives and the pairing's footing row) in 2ae6675.
2. **Done:** the five approximate values read `social_spans_priced_count_2026_09_29` on the priced count (see
   "Priced-count values, formerly approximate").
3. **Typed numbers remain.** 205 groups.py numbers, 9 build.py tokens and 30 template numbers are still typed. They
   MATCH through `source_map.csv`, but the build does not test them. One of them, services/why's "$55bn … (49–62)",
   equals `tally.corrected`, which template line 143 already quotes. Converting any of them means a placeholder, a
   binding, and removing its `source_map.csv` row.
4. **Dead text.** `RELABEL["gg"]` in build.py holds the ledger note too, but only its label reaches the page.
5. **evidence_class.py.** Its known-bias lines (28%, 36%, 62%) are unchanged, because no registry record covers them.
6. **Unquoted records.** 21 records resolve on every run, but no placeholder, `q()` call, binding or other record's
   `q:` selector reads them:
   - alternative readings: `balance.absolute_hull`, `gg.removal_response`;
   - superseded or off-page rows: `candidate_v3.*` (3), `pension.accrual_payable_net`, `property_tax.long_run_change`,
     `tax_key.irs_change`;
   - former document bindings: `backcast.typical_year_change`, `care.total`, `congestion.range`,
     `pairing.per_member_priced`;
   - parts of the case: `case.schools_sept26`, `case.first_year_response`, `finite_removal.effect`,
     `finite_removal.general_government`;
   - the air and crash lanes' own-count figures, which the priced records no longer read: `pm25.deaths_lane`,
     `pm25.span_lane`, `pm25.normalized_lane`, `crash.span_lane`, `crash.fault_based_lane`.

   `case.main` and `capital_return.total` left this list when template 143 and 183 began quoting them (f058b8a). The
   earlier list missed `pension.accrual_payable_net`. `congestion.range` was labelled as on the priced count, but it
   holds the congestion lane's readings on the raw 40.90M. Its population now says so, and its `must_name` requires
   that a quoting sentence says so too.

   They can stay, since ids are never reused, or be pruned.
7. **The four smaller benefits have no record.** Real-costs:395 prints their sum on the priced count, +21.7 (21.69;
   21.96 on the lanes' counts). Until 869c7aa it printed +21.9, which neither rounds to. A record reading the four
   rows of restated_pairing.csv, with the lanes' counts as its other value, would let the sweep see that sum drift.

## Coverage

**Covered:**
- groups.py: every claim, range, why, term and finding text and why in GROUPS, 266 tokens.
- build.py: the hand-typed text that reaches the page (LEDGER labels and notes, table labels), 14 tokens. Its table
  values are now all read from files and tested by the build's value bindings.
- template.html: the body, lines 123–237, 57 tokens.
- INDEX: 9 current-result spans, 268 tokens.
- FAQ: 8 spans, 202 tokens.
- CLAUDE.md: the main-case paragraph, 14 tokens, read only.
- Topic memos: 178 of the 199 `research/immigration-*.md` files, through memo_sweep.py, for the other values of 27
  records only.

**Not audited, with reasons:**
- 86 tokens mapped as `skip`; `source_map.csv` gives the reason for each. They include ladder and entry references,
  chosen elasticities, interval labels, "per 1%" definitions and FAQ offsets outside the brief's scope.
- 54 years in the routing files.
- The outside-checks memo, exempt from the sweep while its header keeps its figures on the September 23 case.
- evidence_class.py's known-bias lines, 8 number tokens, outside the assigned scope.
- The INDEX's bracketed history, per-lane table rows and sections after the back-cast.
- Numbers inside the ladder text itself. A ladder entry that is stale against its own lane would pass.

**Limits:**
- Which source a free number refers to is my judgment, recorded per row in `source_map.csv`.
- A free number's CONTEXT-SHIFT comes from a fixed note in `source_map.csv`. A bound number's comes from the lint,
  which reads the sentence as it stands.
- Centrals on the map are checked to the nearest 5, the map's "$355bn" convention.

**Adjacent observations (outside the audited spans):**
- The winners memo (research/immigration-winners-and-losers-2026-09-25.md) and its lane RESULT still print
  13.0% / 12.7% for state and local cost charged nationally. The current file gives 7.68% / 7.48%, and the INDEX
  prints 7.7%.
- The FAQ calls the 0.47 panel "the only within-state test". gg_response_county_iv_2026_09_23 is a later county IV
  with state fixed effects that cannot test 0.59–0.84.
- The INDEX's "$34bn to $30bn" is the construction lane's metro-local pair; real-costs:393's "$33.5bn → $29.9bn" is
  its national-uniform headline. Both are the lane's numbers, and neither sentence names its geography (see
  "Document numbers").

## How to rerun

```
OPENBLAS_NUM_THREADS=1 uv run --no-project --offline python3 infra/immigration-fiscal/overview_2026_09_28/build.py
uv run --no-project --offline python3 infra/immigration-fiscal/number_drift_audit_2026_09_29/audit_numbers.py
uv run --no-project --offline python3 infra/immigration-fiscal/number_drift_audit_2026_09_29/registry_check.py
uv run --no-project --offline python3 infra/immigration-fiscal/number_drift_audit_2026_09_29/memo_sweep.py
uv run --no-project --offline python3 -m pytest -p no:cacheprovider -q infra/immigration-fiscal/overview_2026_09_28/ \
  infra/immigration-fiscal/number_drift_audit_2026_09_29/
```

- **Quoting a record on the map.** Write `{{q:<id>|<view>}}` in groups.py, template.html or a LEDGER note, and add a
  binding row if the site must keep quoting it. A table row reads `q("<id>")` and gets a `…/value` binding.
- **Build options.** `build.py --groups <copy>` builds from another groups.py, `--out <path>` writes elsewhere, and
  `--round-each` rounds every table number on its own. All three exist for controls.
- **The audit's map.** `source_map.csv` holds one row per free token, keyed by (file, locator, ordinal). The locator
  is structural for groups.py and build.py. For the markdown and HTML files it is an anchor phrase that must pick one
  scanned line; a leading "^" requires the line to start with the anchor.
- **Where the audit stops.** An anchor that no longer picks exactly one line stops the run with `[BLOCKED]`, as does a
  span anchor that is gone. So does a groups.py locator set that differs from the build's.
- **Numbers that move within a unit.** Numbers inserted or deleted since mapping do not shift their neighbours. A
  unit's numbers and rows are aligned by the number as shown (`_align`, `pair_tokens`; `test_pairing.py`).
- **Document bindings.** registry_check.py tests the INDEX and FAQ numbers that should equal a record. It exits 1 when
  a record fails to resolve or a verdict is WRONG.
- **The memo sweep.** `memo_sweep.py` reads the memos at `--rev` (default HEAD) or on disk (`--worktree`) and writes
  to `derived/` or `--out DIR`. It exits 0 with flags; the flags are the output. A failed control, or a record with
  other values but no entry in `ITEM`, stops it with `[BLOCKED]`.
- **Exempting a memo.** Add its path to `EXEMPT` with a sentence the memo must keep and the reason. The sweep stops
  with `[BLOCKED]` if the sentence or the file goes.
- **Editing the CSVs.** The registry, the bindings and `source_map.csv` are the source of truth. Edit them directly;
  the scratch generators that first wrote them are not kept.

## Log

- 2026-09-29 00:43:31 JST: read the mechanisms trace, groups.py (511 lines), template.html 120–229, build.py (374 lines).
  build.py has shifted since the trace: the manual alternative rows are now at 179–186, the manual
  tornado rows at 198, 203–204, 208, 213. [DATA: overview_2026_09_28/build.py]
- 2026-09-29 00:43:31 JST: build.py's social pairing reads sept27_propagation_2026_09_27/derived/real_costs_totals.csv
  §7 (hispanic_mixed_group low 416.19, custody high 490.74), which already carries the Sept 29 crash
  switch (road_crash_externality central 11.05). [DATA: real_costs_totals.csv]
- 2026-09-29 00:47:33 JST: first confirmed defect, groups.py:62–63 (section account, finding refs 123…): "Against
  third-generation whites of the same ages, the gap is about $240bn a year (190–290)". The 190–290
  is the practitioner hull of the union's complete *absolute balance* (ledger_recut_2026_09_22
  derived/hulls.csv practitioner −290.48 / −190.12, central −217.32), not a gap against whites. The
  age-matched gap against third-plus NH whites is −$358.1bn complete (−$290.6bn partial)
  [DATA: ledger_absolute_2026_09_17/derived/complete_gaps.csv, mexican_observed_total]. The $240bn
  central is the range midpoint; the source central is −$217.3bn. History: 102712d printed "about
  $190–290bn a year around $217bn"; 1fbedf1 recast it as "$240bn (190–290)". [DATA: git log -S]
- 2026-09-29 01:02:20 JST: extractor built (audit_numbers.py): AST + tokenize for groups.py and build.py, tag-stripped lines
  for template.html, the rendered page's {{SOCIAL_*}} substitutions, anchored spans for INDEX, FAQ and
  CLAUDE.md. First pass finds about 580 number tokens. The peer committed ladder 267–269 and two new map
  findings (2f82fa4, ca25fc4, 3f92ed6) while this ran; the audit reads the working tree at run time and
  records every input's sha256 in derived/inputs.json.
- 2026-09-29 01:02:20 JST: second confirmed defect, groups.py services/why and template.html summary line 2: "about $65bn
  more in taxes than it gets in benefits (60–70)" equals the figures page's staircase row "tally"
  (−70.08 / −60.25) [DATA: figures_2026_09_22/src/generated/figures.json], which is the September 24
  staircase before data corrections. The untracked peer lane break_conditions_2026_09_29 computes the
  adopted-case tally at $62.0 / $49.4bn (derived/c2_tally.csv) [UNVERIFIED: peer lane, not committed].
- 2026-09-29 02:03:38 JST: the peer fixed groups.py services/why ($55bn, 49–62) and data/claim (44–57) in 0a592dd
  and moved the per-member figure to a build-time placeholder ({{PER_MEMBER}}, b3e9305); 648a3e8 committed
  break_conditions, so c2_tally.csv is now committed. template.html's summary line 2 still says "$65bn … (60–70)".
  Extractor fixes: masked spans keep their line breaks (FAQ lines had shifted by one), every numeric build
  placeholder is audited with a stable locator, "−$43–77bn" reads as two negatives, five new INDEX
  current-result paragraphs (ladder 267–271) are in scope. 604 tokens before mapping.
- 2026-09-29 02:42:05 JST: the peer replaced the map's charts with tables in 6f4b04f (build.py LEDGER, "Other ways to
  count", assumption_rows). The extractor now reads those; RELABEL and the step rows' notes no longer reach the page.
  New findings since the last entry (f250 why, f272 careers, f273 road miles; f271 left the map in 9157343) and the
  INDEX's ladder 273 line are mapped. First full run: 602 tokens, 554 audited: MATCH 513, STALE 16, CONTEXT-SHIFT 17,
  MISMATCH 6, UNSOURCEABLE 2. [CALCULATION: audit_numbers.py → derived/number_audit.csv]
- 2026-09-29 02:55:26 JST: final state. Four rows moved to machine files (the owner response from probe.json, the
  justice use key from main_case_2026_09_23 inputs.json, and the two f161 gaps from age_normalizations.csv). Four rows moved
  after re-reading their sources:
  - INDEX housing "$30bn" matches ladder 200's 29.9.
  - "after 2000" is a MISMATCH against ladder 136 and ladder 140.
  - FAQ "4–7%" is a MISMATCH against the back-cast's average-resident columns.
  - "Rents rise 1%" is a CONTEXT-SHIFT: it is ladder 79's elasticity beside ladder 190's long-run $34bn.

  I added the INDEX lines on the two use keys now inside the case (justice +$5.9bn, uncompensated care +$3.7–5.7bn).
  Final run: 605 tokens, 557 audited. The two runs and the positive control are above.
  [CALCULATION: audit_numbers.py → derived/]
- 2026-09-29 02:57:51 JST: the peer committed 69a7efa and 15b1036 during validation. I reran twice at 15b1036 and the
  outputs were byte-identical. `number_audit.csv` is unchanged from the 02:55 run.
- 2026-09-29 03:35:32 JST: brief update from the team lead: the map's owner will implement build-time sourcing from this
  lane's mismatch list and record format. groups.py, build.py and template.html are unchanged since b408183 (HEAD
  b170585). Wrote `quantity_registry.csv` (47 records), `quantity_bindings.csv` (56) and `registry_check.py`, and
  moved the audit's expression builtins to one constant (`SAFE_BUILTINS`) that both scripts use. The six tornado values
  the owner listed resolve to files; three have been off the page since 6f4b04f. The general-administration row has no
  source on the September 27 case (interim −30.3 / −44.3 [INFERENCE]). New: the ledger's "Sales and excise taxes" row
  shows the whole September 26 step, not the consumption key alone (runs.json K = J + L). The FAQ and INDEX
  rewrites (1a28dd0, 928d659) fixed 7 of the 9 flagged document numbers and broke the audit's anchors for those two
  files. [CALCULATION: registry_check.py → derived/registry_values.csv, derived/binding_tests.csv]
- 2026-09-29 03:51:08 JST: resumed after a context compaction. b7f14e7 had landed at 03:39: population_basis_2026_09_29
  (ladder 274) restates the pairing on the 39.71M the account prices, $413.74–488.05bn and $10,419–12,290 per member,
  and adds rows `pairing_on_priced_count` to real_costs_totals.csv. The peer was editing the INDEX and FAQ to match.
- 2026-09-29 03:56:12 JST: the peer committed 52ca964 (INDEX, FAQ, ladder, a ladder ref in groups.py) and ff60589 (build.py reads
  `pairing_on_priced_count`; groups.py's comparators on 39.7M). The FAQ rewrite had also rephrased the
  general-government sentence that three map rows read as a text source, which stopped the audit. I re-anchored the
  FAQ's third span on a stable phrase and re-pointed 46 map rows: the social rows to restated_pairing.csv, the white
  comparisons to white_count.csv, and the {{SOCIAL_TOTAL}} and {{SOCIAL_ADD}} rows to `pairing_on_priced_count`.
- 2026-09-29 04:36:08 JST: a subagent returned selectors for 47 new document tokens (46 MATCH, 1 MISMATCH at FAQ:95).
  I ran each selector and checked its five substantive claims in the files (see Coverage).
- 2026-09-29 04:55:49 JST: every token is mapped. 202 document rows are by hand, 10 of them replacing carried rows, and
  189 carried rows passed review. HEAD bb1e0ba; no audited file changed since ff60589. Registry rebuilt: 62 records,
  71 bindings.
- 2026-09-29 04:56:01 JST: final runs. audit_numbers.py twice: 669 audited, outputs byte-identical. registry_check.py
  twice: byte-identical, 58 bindings fail now and pass after. The positive control and six spot-checks are above.
  [CALCULATION: audit_numbers.py → derived/; registry_check.py → derived/]
- 2026-09-29 05:01:12 JST: rewrote this RESULT to the bb1e0ba state. The 03:35 entry's broken anchors are repaired;
  its 7-of-9 count stands, and the two it left open are now INDEX:97, still wrong, and the per-member figure, which
  52ca964 fixed.
- 2026-09-29 05:13:50 JST: checked the rewritten RESULT against the outputs and git. Corrected three statements: the
  rewrites fixed 8 of the 9 first-run document numbers, not 7 (52ca964 fixed the per-member figure); the carried-row
  count; and the `alt` line in build.py (188). Added the RELABEL note. Meanwhile the peer committed 3e1ae94 and
  263def3, which put the household split on the priced 39.71M and changed INDEX:112 and ladder 268. The rerun turned
  INDEX:112 into 9 MISMATCH and 1 UNSOURCEABLE: the line gained "39.71M" before nine mapped numbers, and the map
  paired numbers by position, so each number met its neighbour's source.
- 2026-09-29 05:22:51 JST: fixed the pairing. When numbers are inserted or deleted, a unit's numbers now align with its
  rows by the number as shown (`_align`, `pair_tokens`), and registry_check.py finds sites the same way. Added
  `test_pairing.py` (4 tests). With the old map, every row outside INDEX:112 was unchanged. Re-pointed INDEX:112 and the
  map's f268 to within_group_distribution_2026_09_29/derived/row4/, kept the published run as the superseded value,
  and mapped "39.71M". Two map numbers are STALE on the priced count: "(20–24)" and "53–61%". Added
  `household.net_contributor_share`, `household.top10_cost_share` and their two bindings. Final runs at HEAD 263def3,
  each twice and byte-identical: 670 audited; 64 records; 60 of 73 bindings fail now and pass after. I reran the
  positive control. [CALCULATION: audit_numbers.py, registry_check.py → derived/; pytest]
- 2026-09-29 05:24:44 JST: rewrote the header, tables and validation to the 263def3 run. The 05:01 entry describes the
  bb1e0ba state.
- 2026-09-29 06:39 JST: state at the start of the final validation, after the lead's brief to own the map's numbers.
  - The registry, its bindings and one module, `quantities.py`, now sit in overview_2026_09_28/. build.py,
    audit_numbers.py and registry_check.py import the module; the resolver copy in audit_numbers.py is gone.
  - build.py fills `{{q:<id>|<view>}}`, lints every quoting sentence, tests 59 bindings and marks approximate values.
  - Every flagged map number is fixed through a record. The table values are read from the registry, and the ledger
    splits the September 26 step, gated against run I.
  - General administration held fixed reads b3f4d84's engine arm, −30.27 / −44.34, against the interim −30.3 / −44.3.
    The subagent's run behind it has baseline and final checks at 05:34 and 05:49 JST (its own `date` calls).
  - The alternatives read candidate v4's one-set run after 923dfbd.
  - The INDEX anchors moved by f40e47e and 923dfbd are re-anchored. 662 numbers audit as MATCH, and the 13 document
    bindings are FIXED.
  - Builds and audits reproduce byte for byte. Three positive controls fail the build: a typed number, a missing
    "whites" and a typed table row. The audit flags the first two.
  [CALCULATION: build.py → derived/overview.html; audit_numbers.py, registry_check.py → derived/]
- 2026-09-29 06:42:02 JST: resumed after a context compaction. HEAD was still 923dfbd, and the working tree was as left.
- 2026-09-29 06:49:03 JST: the alternatives table's beside row showed "Costs outside public budgets +92 / +101". The
  92 is the social items' 96.3 less 4.3, because the pairing's low end prices offending at the Hispanic average
  (fiscal $317.5bn) [DATA: real_costs_totals.csv §7]. After the {{SOCIAL_ADD}} fix the prose says 96–101, so the table
  and prose disagreed.
  - Added the record `pairing.fiscal_footing` and a row for it, "Offending at the Hispanic average, low end" (−4 / 0).
    The social step now reads +96 / +101.
  - Added two gates: the high-end fiscal case must be the main case, and the pairing less its fiscal case must be
    `social.items`. The header of the beside block now prints once.
  - Reran every check from 06:49:03 to 06:49:32, and all passed with 60 bindings. A fifth positive control, moving
    `social.items` by 0.5, fails the build. [CALCULATION: see Validation]
- 2026-09-29 06:55:49 JST: rewrote this RESULT to the 923dfbd state. Every section above the log is new. The 05:24
  entry describes the 263def3 state.
- 2026-09-29 07:20:05 JST: the lead reported the operator's rule: printed lines must add to the printed total, and
  a block prints one decimal where whole billions break a sum. Rounded on its own, the ledger broke 6 sums at whole
  billions and the running sums 4. At one decimal they still broke 5 and 2, and at two decimals 4. [CALCULATION:
  scratch ledger_sums.py on build.py's rows]
  - The build now prints one decimal when whole billions break, and allocates by largest remainder (`Q.allocate`).
    6 ledger lines and 2 steps are rounded the other way, each by less than 0.1, and the captions say so.
  - `displayed_sum_errors` reads the printed tables back and refuses the page on a broken sum.
  - `--round-each` is the positive control: it fails with 7 broken sums. Validation ran at 07:18:41–07:18:52 (see
    Validation).
- 2026-09-29 07:29:45 JST: the lead approved both same-class fixes.
  - **Prose sum.** Added `pairing.footing_reduction` (4.34 at the low end, from `case.main` less
    `pairing.fiscal_footing`) and the sentence "Its low end also prices offending at the Hispanic average, $4bn less."
    It sits at template 147, template 213 (which now prints the range, $414–488bn) and the social group's why.
    `PROSE_SUMS` checks 322 − 4 + 96 = 414 and 387 + 101 = 488 on the printed values. Template 143's "$355bn a year
    (322–387)" became placeholders, and its two source_map rows went.
  - **Capital label.** Template 183 now reads "Return on public capital, government enterprises' included: about
    $45bn (34–56)", bound to `capital_return.total`, which must name the enterprises. Its two source_map rows went too.
  - **Validation.** Everything was validated at 07:28:04–07:28:13, with three controls (see Validation). Template 186
    states no sum ("Beside the total"), so it takes no footing sentence. My earlier report listed it by mistake.
- 2026-09-29 10:26:09 JST: the lead's last task: replace the five approximate values with file-backed ones on audit
  row 4's 39,712,493 people.
  - A new lane, `social_spans_priced_count_2026_09_29`, reruns air_items.py's `pm_grid` and crash_model.py's
    `evaluate_split` over their full grids on row 4. The crash figures use the NHTS ratios per person aged 5+. All 22
    gates pass: the positive controls, reeval.csv's centrals and restated_pairing.csv's factors.
  - The five records now read its `derived/priced_spans.csv` with status `file`, and their reader_notes are gone. PM2.5
    against average residents prints $46bn (was $45bn) and crashes by fault $41bn (was $40bn). The other three print
    as before.
  - `congestion.range` held the raw-count readings under a priced-count label. It now says raw, and quoting it must say
    so.
  - The how-to-read sentence is conditional on a marked number (`APPROX_NOTE`). Validation ran at 10:21:40–10:23:51
    (see Validation).
- 2026-09-29 11:20:48 JST: the lead's task: extend the audit to the living topic memos, which it did not reach. The lead
  committed the priced-count work (8bdf62a, db03667, 5ccf86d) and fixed the listed document sites in 8aaf046.
  - Wrote `memo_sweep.py` and `test_memo_sweep.py`. Built on 5ccf86d, the revision the lead's list describes, then run
    on HEAD 8aaf046.
  - Fixes while building: "ladder N" is not a vintage label; a caption labels only its own column; "from" marks only
    the number after it; a bare "$" is not a unit, which dropped a "+$464" per-household match; signed memo numbers
    match the registry's magnitude records; the presented-as-current test covers a range on the next line.
  - Result, hand check and validation (11:17:37–11:19:11) are in "Memo sweep, 2026-09-29".
- 2026-09-29 11:23:38 JST: corrected memo_sweep.py's docstring on units and caption scope and reran the validation at
  11:21:30–11:23:01. The outputs are byte-identical to the 11:17 run.
- 2026-09-29 11:39:38 JST: the lead's added task: give each registry record carrying the default treatment its own
  basis, then show that the outputs do not move. Meanwhile the lead committed 869c7aa, which fixed the sweep's flags.
  - A first validation at 11:30:34 found the audit `[BLOCKED]` before and after the edit, on two different anchors.
    8aaf046 had broken three (2 INDEX, 1 FAQ), and the audit named whichever its set order met first. I re-anchored
    them, re-pointed five rows to priced_spans.csv and mapped three new numbers. The audit now lists every broken
    anchor, sorted.
  - 48 records carried the default: 37 changed, 11 kept, plus 14 adjacent fields (see "Registry treatments,
    2026-09-29"). Validation ran at 11:38:42–11:39:29.
- 2026-09-29 11:58:51 JST: the lead's task on HEAD 869c7aa or later: repair the anchors for the new text, exempt the
  outside-checks memo, refresh derived/ on HEAD and validate everything twice. HEAD is 856bd5a; db5840f and 856bd5a
  touch no input of this lane.
  - The 8aaf046 anchors were already repaired. 869c7aa's scale net sits in the INDEX's benefits paragraph, which no
    span covered. It is now a ninth span, with 18 rows mapped: 16 MATCH, 2 skips. "$34bn to $30bn" matched only as
    the construction lane's metro-local pair; the lane's headline pair is national-uniform (see "Document numbers").
  - The sweep exempts the outside-checks memo under its header sentence and stops if the sentence goes; a second
    test covers it. The 20 numbers the lead's commits wrote into the real-costs memo resolve to their sources.
  - Validation ran at 11:48:26–11:49:13: 684 of 684 MATCH, 0 flagged in 178 memos, 25 tests, every output
    identical on its second run.
