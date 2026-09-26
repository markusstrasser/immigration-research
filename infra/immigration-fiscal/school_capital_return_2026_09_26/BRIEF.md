# Lane brief: the return on school capital that the account leaves out

Date: 2026-09-26. Operator: "yeah" to measuring it (figures session f5e074c6).

## Question

The main case charges the Mexican-origin group's pupils at full average cost per pupil (school
response 1; `../main_case_schools_full_2026_09_26/`, decision
`../../../decisions/2026-09-26-main-case-schools-full-cost.md`). Its school line comes from BEA
government consumption (NIPA Tables 3.15.5/3.17, the explorer's `education_services` line). That line
includes consumption of fixed capital (depreciation), but no return on the capital itself: a
national-accounts convention, not an economic cost measure. A school system sized for the group's
pupils ties up buildings, equipment and land whose alternative use has value. **How large is the
annual opportunity cost of that capital for the group's pupils, beside the depreciation already
counted?**

## Facts to reuse (do not re-derive)

- Pupil share s = 0.17480600215120404 (8.487m of 48.551m public-school pupils):
  `../school_cost_where_enrolled_2026_09_24/derived/account_embedded_price.json`.
- School line at full cost: $167.0bn (band low end) / $143.4bn (high end):
  `../main_case_schools_full_2026_09_26/derived/summary.json` → `school.school_line_at_full_cost`.
- The school fraction of BEA education consumption is bounded at 71.5–86.5%
  (`../../../decisions/2026-09-20-category-service-response.md`).
- State and local consumption includes CFC of $312.559bn of $2,550.362bn (12.26%)
  (`../school_cost_where_enrolled_2026_09_24/RESULT.md`, around line 255, with its NIPA table cite).

## Deliverables

1. **National K–12 capital.** Current-cost net stock of state and local government fixed assets used
   for elementary and secondary education (structures, plus equipment and software if separable),
   latest year, with its current-cost depreciation. Use BEA's Fixed Assets Accounts (government fixed
   assets by type and function; detailed estimates if the published tables only give "educational"
   structures). If BEA does not split K–12 from higher education, split by a documented key (for
   example each sector's share of education CFC or capital outlays) and report the key's range.
2. **Land under schools.** Not a produced asset, so absent from BEA. Estimate it only from a
   defensible primary source (for example school-district property records or published land shares
   of institutional property). Otherwise mark it [GAP] with what would close it.
3. **Real return.** Annual opportunity cost = real rate × current-cost net stock. Report 2% (OMB
   Circular A-4, 2023) and 3% (A-4, 2003), plus the real yield on long municipal bonds if a primary
   series is at hand. State that the rate is a convention [FRAMING-SENSITIVE].
4. **The group's share.** Multiply by s. Say whether capital per pupil where the group enrols
   plausibly differs (newer or overcrowded buildings in CA and TX); describe it, don't model it.
5. **Compare** with the depreciation already inside the school line: education CFC × school fraction
   × s. Report the ratio of the missing return to that depreciation.
6. **Double-count check.** The main case holds interest on existing debt at zero response (engine
   response class `interest`). Check how `../assumption_explorer_2026_09_21/engine.js` treats interest
   and whether any lane (start with `../debt_legacy_2026_09_23/`) already charges interest on school
   debt to the group. State plainly whether adding the capital return double counts anything.
7. **Secondary, if BEA gives structures by function.** The same return for the other services the
   main case charges in full (public order and safety, health, income security, housing and
   community), as a separate table.

## Outputs, all inside this directory

- `RESULT.md`. The first line starts with `**Verdict:**` and gives $bn a year for the group at 2%
  and 3%. It then sets out the method, sources (URL, table ID, line), the double-count finding, gaps,
  and the files covered and skipped with reasons. Tag claims [SOURCE], [DATA], [CALCULATION],
  [INFERENCE] or [GAP].
- `capital_return.py`, reproducible with
  `uv run --no-project python3 infra/immigration-fiscal/school_capital_return_2026_09_26/capital_return.py`
  from the repo root. It prints the results and exits nonzero on a failed gate. Gates at minimum:
  - net stock over CFC lies in a plausible range for structures;
  - the FA-table CFC for state and local education is within a stated tolerance of NIPA's education
    CFC, where both exist.
- `derived/*.csv` (`csv` module with `lineterminator="\n"`). Raw downloads go in `_cache/`, with
  their URLs recorded.

## Rules

- Write only inside this directory. No commits. No edits to shared documents (CLAUDE.md, INDEX, FAQ,
  ladder, memos) or other lanes: a peer session is their single writer.
- Numbers used in a calculation come from primary tables (BEA, NCES, Census), never from web
  summaries or model-extracted PDF tables; parse the primary file.
- Never print API keys. If BEA's API needs a key you don't have, use its public download files.
- Write `RESULT.md` early and append as you go, so a killed run leaves its findings.
