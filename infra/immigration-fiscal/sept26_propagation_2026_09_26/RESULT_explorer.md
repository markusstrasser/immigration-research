claude-opus-5-5

# W3 `explorer`: the assumption explorer on the September 26 case

**Verdict:** The plumbing is done and passes its checks on the current tree; nothing is committed.
The explorer loads the September 26 payload, and its presets read the responses from
`meta.responses` through `value_from`. `test_engine.js` passes on all three September 26 bands:
**$200.9180–245.6949bn** central, both with the switch set explicitly and with the presets as loaded.
It also passes the uncorrected gate ($207.4046–253.1859bn) and still reproduces the September 23
and 24 cases.

At 23:24 two rebuilds were byte-identical to the page the headless check read (sha256
`9d19a39c…514b`). That page's central card reads "−246 to −201". The engine is unchanged.

The lead's scope trim arrived after the work below was finished. "Scope trim" says which changes
it covers and which go beyond it.

Since the 22:39 adoption of schools at full cost, the page's central case is the one-year scenario,
but its label still reads "adopted 2026-09-26". Relabelling is the lead's call (see "For the lead").

Model self-report: claude-opus-5-5. Lane: `../assumption_explorer_2026_09_21/`.

## Scope trim (received after the work was finished)

The trim asks for four things: plumbing only, note changes only where a note would be wrong, no
screenshot polish and no commit. Against it:

| Item | State |
|---|---|
| `build_ui.py` loads the September 26 payload | Done. It refuses a payload without `meta.responses`. |
| Presets take the responses from `meta.responses` (`value_from`) | Done: `responses.general_government.low/high`, `responses.school.growth/decline`. |
| `test_engine.js` gates the September 26 bands | Done. Exit 0 with the PASS line under "Gates", rerun at 23:24. |
| Rebuild and one headless check | Done. Two rebuilds at 23:24 exited 0 and match the checked page byte for byte. Central card "−246 to −201"; in-page engine 200.9180–245.6949. |

**Notes that had to change.** With the September 26 payload loaded, each of these would be wrong
about the value it describes:
- The central kind label read "adopted 2026-09-24". Its summary gave 63-66% and 0.59-0.84; both
  now print from `meta.responses` through the `{response:…}` token.
- The central scope note and the switch-off status called the switch-off state the September 23
  case. It is now the uncorrected model at the adopted responses, 207.4–253.2bn.
- The switch label and the ledger note named 2026-09-24 only.
- The September 20 preset's school note read "As in the central case". The central case no longer
  uses 63–66%.
- Each changed response note carries one sentence on why the response exceeds the rate. It cites
  `repo_finite_response_2026_09_26`, as the validator requires.

**Beyond the trim.** These were done before the trim arrived and are still in place. Nothing is
reverted, and each can be separated by file or hunk if the lead wants the smaller diff:
- Slider ticks at the adopted responses, and help text built from `meta.responses` (`ui.js`, plus
  one CSS rule in `template.html`).
- `cite` links under the preset notes (`ui.js`). The build-time check stays, because the validator
  requires it.
- Two sentences in the central preset beyond the minimum: "Both responses are what removing a group
  of this size saves…" in the summary, and the functional-form caveat in the scope note.
- The card pass (`context.json`, nine cards on the September 26 case) and the README sections.
- Eight screenshots (ignored files).

**Changed after the trim.** One README sentence was wrong from 22:39:
- Before: "the page's central case is the main case adopted that day".
- After: "the finite-removal case adopted that day".

A new sentence follows it: the schools decision makes this case the one-year scenario, and the page
stays on it until the operator asks.

## Regression gate (as it stood, September 24 case)

- `node test_engine.js` exited 0 with PASS; the central preset as loaded gave 200.8752 to 246.3184 bn.
- `build_ui.py` exited 0 twice, and the two builds were byte-identical (sha256 `86805c18…a833`).
  Nothing under `derived/` is tracked (`.gitignore: derived/`).
- Against the page built on 2026-09-25 (sha256 `257bf80e…1af2`), the rebuild differed in two inlined
  blocks only. Both are text inputs committed after that build:
  - `CONTEXT`: five `file_line` anchors re-pointed in ba12f3c; no value changed.
  - `LADDER`: the ladder file has grown since.

  The model, payload, presets, evidence, sources, engine, UI and template blocks were byte-identical.
- The main-case packages that W1 and W2 run import `model.json`, `scaling_check.json` and `engine.js`,
  so none of the three was rebuilt or edited. `package.cjs` still guards composite 0.59/0.84.

## Files changed (all in `assumption_explorer_2026_09_21/`)

| File | Change |
|---|---|
| `build_ui.py` | Loads `main_case_2026_09_26/derived/corrections.json` and refuses a payload without `meta.responses` (both ends of each band, `s`, the two elasticities). `value_from` also resolves dotted `responses.<path>` from `meta.responses`, and a path that names no number is refused. New `{response:<name>}` token prints the adopted band in preset text. New `cite` check: each key must be in `sources.json`, and that source must list the convention. The build line prints both adoption dates and the four responses. |
| `presets.json` | Central preset: school and general-government point values and bands via `value_from: responses.…`; notes, summary, scope note and kind label updated; `cite` added. Proportional: general government from `responses.…`, plus its note, summary and one miss. September 20 preset: school note and data-switch note. The other four presets: data-switch refs name both decisions. Top note documents the new paths, token and `cite`. |
| `test_engine.js` | Loads the September 26 payload as the page does, and a second corrected copy with the September 24 payload. It checks 14 bands in total (next section), and checks that the loaded presets carry exactly the payload's responses. |
| `ui.js` | The switch label, help and ledger note name both adoption dates, read from `meta`/`meta.builds_on`; the help says the responses stay when the switch is off. The school and general-government sliders show dark ticks at the adopted responses beside the grey marginal-rate ticks, with help text built from `meta.responses`. The switch-off status text is rewritten. Bands print their two ends to the same decimals ("0.60–0.85", not raw floats). The preset note renders `cite` links. |
| `template.html` | One CSS rule for the adopted-response tick (`.rng .am`, ink2). |
| `sources.json` | Four repo documents: the Sept 26 decision, `main_case_2026_09_26`, `finite_response_2026_09_26` and `consumption_key_2026_09_24` (127 sources, 22 of them repo documents). The main-case lane supports the nine refreshed cards. |
| `context.json` | Cards refreshed to the September 26 case. Every card and value was kept (57 cards, 250 values), and 29 drifted anchors were re-pointed (next section but one). |
| `README.md` | Verdict numbers, reproduce commands, new section "Adopted 2026-09-26", fifth card pass, source and card counts. The September 24 "Status" bullet is marked as superseded. |

Ignored outputs: `derived/explorer.html` (sha256 `9d19a39c…514b`), `derived/screenshots/sept26_*.png`
and `_cache/inventory_2026_09_26.json`. The two scripts that wrote the inventory are kept next to it
in `_cache/cards_2026_09_26/`. `build_inventory.py` starts from HEAD's cards and uses `reanchor.py`,
which maps each citation line from ba12f3c to the current files. Running `build_context.py` on the
inventory writes `context.json`.

## Gates

`node test_engine.js` exits 0:

> PASS: 2629 grid rows, 60 service cases, 32 accounting cases, 4 headline bounds, September 20 central
> preset, 14 adopted bands (central: September 23 203.2070 to 249.6400 bn; September 24 200.8752 to
> 246.3184 bn; September 26 200.9180 to 245.6949 bn, as loaded 200.9180 to 245.6949 bn; uncorrected at
> the adopted responses 207.4046 to 253.1859 bn), data switch on every preset as loaded (off only for
> repo_central), adopted responses as loaded, attribution closure, 532 corrected shares on their base;
> worst gap 4.28e-9 bn

The 14 band checks each hold to half a unit of the fourth printed decimal:
- the September 23 bands at the marginal rates, switch off, with the lane identity also held to 1e-6;
- the September 24 bands on that payload at the marginal rates;
- the September 26 bands, switch on;
- `uncorrected_at_adopted_responses`, switch off;

The first four run for the central case, non-school education fixed and the proportional profile. The
remaining two checks cover the central and proportional presets as loaded.

Negative controls (2026-09-26):
- **Old typed responses.** A scratch copy of the presets with 0.63/0.66 and `composite_low/high`
  fails 12 checks and exits 1. It computes the mixed case, 196.7218–242.1650 bn.
- **Build checks.** Eight malformed inputs are refused:
  - an unknown `cite` key;
  - a cited source that does not list the convention;
  - a `value_from` path that points to nothing;
  - a `value_from` path that points to an object;
  - an unknown `{response:…}` token;
  - a payload without responses;
  - a payload missing one end of a response band;
  - a point value that is neither end of its band.

  A point value at the band's other end is accepted, as it should be.

## Old → new, every number the page computes (cost to other residents, $bn a year)

Old is the page as built on 2026-09-25: HEAD presets with the September 24 payload. New is this
build. The page prints whole billions on cards and range lines. The one-decimal bands come from the
same engine: `test_engine.js`, or an eval inside the headless page.

| Item | Old | New | Where |
|---|---|---|---|
| Central preset band | 200.8752–246.3184 (card "−246 to −201") | **200.9180–245.6949** (card "−246 to −201") | `test_engine.js`; page card and range line |
| Central, non-school education fixed | 157.1268–210.8300 | **156.5248–210.8433** | `test_engine.js` |
| Proportional preset | 302.9720–336.4219 ("−336 to −303") | **301.2853–334.7516** ("−335 to −301") | `test_engine.js`; page card |
| Central with the switch off | 203.2070–249.6400 (the Sept 23 case) | **207.4046–253.1859** (uncorrected at the adopted responses) | `test_engine.js`; page range line |
| Switch off, non-school fixed / proportional | 158.8811–212.5633 / 307.8989–340.9715 | 162.4357–216.7469 / 308.3841–341.4735 | `test_engine.js` |
| Central point value (result bar) | −223.6 | **−223.1** | page bar |
| Central, per other resident / per member | −$747 / −$5,469 | −$746 / −$5,456 | page |
| Taxes minus benefits (gain) | 56.2–66.7 ("56 to 67") | 60.4–70.8 ("60 to 71") | page card |
| No public services (gain) | 65.0–80.0 ("65 to 80") | 69.2–84.1 ("69 to 84") | page card |
| Everything at average cost | 562.4–577.4 | 560.4–575.4 | page card |
| September 20 preset; production only | 165.1–197.4; 0.2 | unchanged | page cards |
| Responses in the central preset | general government 0.59/0.84, schools 0.63/0.66 | **0.6000/0.8504, 0.6522/0.6813** (from `meta.responses`) | `presets.json` → page |

The conventions with services off gain $4.15bn: the consumption key's +$4.05bn in receipts, and audit
row 8's −$0.10bn, which counts in full under every convention.

## What the page shows now (headless, agent-browser, 1400 and 390 px)

- The central card reads "This repo, adopted 2026-09-26, CBO-informed central case, −246 to −201".
  The result line reads "Across them the result runs from −246 to −201 bn", in standards mode with no
  console errors. The in-page engine gives 200.9180–245.6949 (on), 207.4046–253.1859 (off) and
  156.5248–210.8433 (non-school fixed).
- **Switch off:** the range becomes −253 to −207 and the Shapley split shows the switch alone at
  −7.2. The status line reads "The central case's assumptions on the data as the account published
  them". The ledger note reads "The data corrections adopted on 2026-09-24 and 2026-09-26 are off".
  Switching back and "Back to central case" restore −246 to −201.
- **Sliders:** school "central 0.652–0.681", with grey ticks at 0.63/0.66 and dark ticks at
  0.652/0.681; general government "central 0.60–0.85", with ticks at 0.59/0.84 and 0.600/0.850.
- No horizontal overflow at 390 px.
- **Screenshots** (in `assumption_explorer_2026_09_21/derived/screenshots/`):
  - `sept26_result_corrections_on.png`, the result area;
  - `sept26_result_corrections_off.png`;
  - `sept26_top_corrections_on.png`;
  - `sept26_rail_school_gg.png`, `sept26_rail_gg.png`;
  - `sept26_preset_note.png`, `sept26_preset_note_rows.png`;
  - `sept26_phone_top.png`.

  Element-crop screenshots of the sticky rail came out blank, so these are viewport shots taken after
  scrolling the element into view.

## Text changed (before → after)

- **Switch label:** "Apply the data corrections adopted on 2026-09-24" → "…adopted on 2026-09-24 and
  2026-09-26". The help adds the consumption key, and adds "The school and general-government
  responses are settings of their own, so switching the corrections off leaves them where they are."
- **Status with the switch off:** "The central case without the data corrections, as adopted on
  2026-09-23, …" → "The central case's assumptions on the data as the account published them, …".
- **Central preset.**
  - Kind label "adopted 2026-09-24" → "adopted 2026-09-26". Summary "School spending follows
    enrollment 63-66%" → "…65-68%", "…at 0.60-0.85 of average cost". Added: "Both responses are what
    removing a group of this size saves, a little more than the marginal rates they come from."
  - Scope note: "switch the corrections off to see the case of 2026-09-23" → "Switching the data
    corrections off keeps the responses, so it shows these conventions on the data as the account
    published them, a case no decision adopted". It also adds the functional-form caveat (−$4.1 /
    −$3.4bn if a removal saves only the marginal rate).
- **Why the response exceeds the rate.** One sentence per changed note, each citing
  `repo_finite_response_2026_09_26`:
  - school (central): "The group holds 17.5% of pupils, and when cost is a power of enrollment,
    removing a share that large saves more than the marginal rate: 65-68% of average cost."
  - general government (central and proportional): the same logic at 12% of residents, "0.60-0.85
    where the rates give 0.59-0.84".
  - September 20 preset, school: "As in the central case." → "CBO's marginal rate, 63-66%, used as
    the response, as the account published it. Since 2026-09-26 the central case uses the larger
    share that removing the group's 17.5% of pupils saves."
- **Proportional and average-cost misses:** the school evidence now names both 63-66% at the margin
  and 65-68% for a removal of the group's size.
- **Cards:** nine cards now lead with the September 26 case, and the September 24 figure stays beside
  each as such:
  - the headline;
  - `e2_fixed_functions_and_cbo_inputs`;
  - `e2_fixed_service_range_and_breakeven`: break-even 5.8–13.9% / 8.8–17.0%; frozen services −21.6
    to +81.5;
  - `e2_general_public_services_sensitivity`;
  - `e4_offset_threshold_is_conditional`;
  - `e11`;
  - `e16`;
  - `e17`: range $164–277bn;
  - `complete_account_assigned_balance`: receipts 488.5 → 492.5.

  Six cards' combining rules follow the FAQ's current wording. Values computed only on the September
  24 case keep that date: the back-cast, the scale net, the real-costs totals, e12's +2.03 and the
  356 bn endpoint.

## For the lead

- **Central label.** The card reads "This repo, adopted 2026-09-26, CBO-informed central case, −246
  to −201". Since 22:39 the main case adopted that day is $258.5–292.0bn.
  - A minimal fix, if wanted, has two parts. The kind label becomes "This repo, one-year scenario,
    2026-09-26". The scope note gains one sentence citing
    `decisions/2026-09-26-main-case-schools-full-cost.md`.
  - I have not made it, because it reframes the page and the operator deferred UI changes. The
    proportional preset is unaffected: it holds schools at 1.
- **Card anchors drifted after abf99ab.** That commit (22:58) added 1–11 lines to the FAQ and to the
  complete-account memo.
  - 29 of the 250 card values no longer re-verify at the line they cite. On HEAD's cards the count
    is 32 of 249.
  - Every one re-verifies after shifting its line by 1–11, so no value left the docs.
  - `build_ui.py` does not re-verify anchors; only `build_context.py` does. The page therefore
    builds over the drift.
  - The fix is mechanical: update the inventory's lines, then rerun `build_context.py`. A guard in
    `build_ui.py` would block builds until that is done. Neither is done, because both fall outside
    the trim.
  - Probes (read-only):
    `/private/tmp/claude-501/-Users-alien-Projects-immigration-research/95a94bd8-dcdc-4501-bb8e-5f9906dddc53/scratchpad/explorer/{recheck_cards,shift_cards}.py`.
- **Figures.** The figures session has pinned `figures_2026_09_22/account.cjs` to read the
  explorer's `presets.json` at d710a74 through `git show`.
  - The pin is uncommitted in the working tree, together with `proto/conventions.cjs`.
  - If this lane's `presets.json` is committed without that pin, the prototypes at HEAD will throw
    on `repo_central_gg` and `proportional`. The pin should land first or in the same commit.
- **Outside my boundary, still on the older wording:**
  - FAQ entry 2 (line 80) gives general government as "0.59–0.84".
  - FAQ entry 16 (line 418) says "the main case adopted September 24".
  - The explorer memory note (`immigration-assumption-explorer`) says the switch-off state is the
    09-23 case; that is now stale.

## Parent integration (2026-09-26, 23:30)

- **Relabel applied by the parent.** The central preset's kind label is now "This repo, one-year
  scenario, 2026-09-26". Its scope note opens with one sentence: the adopted main case charges
  schools at full average cost (decision `2026-09-26-main-case-schools-full-cost`), and this page
  shows the case adopted earlier that day, which the decision keeps as the one-year budget scenario.
  No number is typed. After the edit, `test_engine.js` gives PASS and `build_ui.py` exits 0; the
  built page carries the new label.
- **Beyond-trim items kept.** Slider ticks, cite links, the extra preset sentences, the card pass and
  the README sections were all in the original brief.
- **Card anchors deferred.** The drift is 29 of 250 values after abf99ab; 58b7596 shifts more. The
  memo edits of the consumer pass (generation, back-cast, real costs, winners and losers) will move
  them again, so the parent re-anchors once, after that pass.
- **Figures.** fef4d12 (figures session) pins the pages' explorer presets at d710a74. This commit
  therefore leaves `build_data.cjs` and `proto_data.cjs` unchanged; the figures session ran them
  against this presets.json.
