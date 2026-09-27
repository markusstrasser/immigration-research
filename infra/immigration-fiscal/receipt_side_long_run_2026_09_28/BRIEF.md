# Lane brief: one long-run rule for the receipt side

Date 2026-09-28, 07:10 JST. Parent session immigration-research-1c. The operator asked where $30bn+ mistakes could
still hide in the adopted September 27 case ($321.82–387.37bn at specifications 48 / 11) and said "ok do" to this
lane. The probe `receipt_long_run_probe_2026_09_28` (3cd946e) found one asymmetry:
- the case scales public capital, roads and parks with population in the long run;
- `engine.js` credits every receipt marked `direct: false` at response 0 (`indirect_receipt_response: 0`),
  including the group's $24.97bn owner-occupied property tax.

Letting that tax leave with the group at 0.79 or 1 lowers the case by $19.73bn or $24.97bn at both ends. This
lane replaces the probe's two numbers with a derived response, adds the renters' share, and applies one long-run
rule to every line on both sides. Adoption is the operator's call. Build candidate items, never a new case.

## Read first

- `receipt_long_run_probe_2026_09_28/RESULT.md` and `probe.cjs`. Reuse its replica gate.
- `main_case_long_run_2026_09_27/` (`package.cjs`, `RESULT.md`, `derived/corrections.json`). Do not edit it.
- `assumption_explorer_2026_09_21/engine.js`: `evaluate` (receipt response at l.150–157), `applyCorrections`,
  `spendingResponse`. `derived/model.json` → `receipts.lines[].cells[scenario][allocation]` holds `direct`, `key`,
  `response_class`, `share`, `target_bn`.
- `research/immigration-complete-annual-account-2026-09-20.md` §"Benefits joined to an explicit fiscal response".
  Its rule 1 sets the zero: "Corporate/property incidence, other-business receipts and public-asset income receive
  zero direct response; the production model handles induced capital taxes."
- `full_account_receipts_2026_09_20/builder.py`: where each receipt key and `direct` flag come from.

## Items

1. **Trace the zero.** For every receipt line with `direct: false`, give its amount on the group at 48 and 11, its
   key, its response class and where the flag was set (commit and file). State exactly what the production term's
   induced receipts F contain. Does F already carry any property tax, production tax or business transfer on
   capital that leaves under capital adjustment? Nothing may be counted twice. The probe found P + F invariant to
   `capital_tax_retention` at the reference cell; say why.
2. **Owner-occupied property tax: derive the response, don't pick it.** Work it out under each regime, separating
   the short run (fixed stock) from the long run (stock follows households):
   - levy-set budgets, where the rate adjusts to raise the levy. Here the spending side already counts the budget's
     fall. Is the group's share then picked up by other residents at any horizon?
   - rate- or assessment-limited systems, where revenue follows assessed value. California's Proposition 13
     (1% rate, 2% assessment growth, reassessment on sale) is the group's largest case.
   - the benefit view, where property tax is the price of local services. The case charges schools at full
     average cost.
   - land versus structures. Land stays when the group leaves, but its price falls with demand. Use a
     county-level land share of residential value, such as Davis, Larson, Oliner and Shui (2021), weighted by where
     the group's owner-occupiers pay the tax. If no measured land-price response exists, state the assumed one.

   Weight the regimes by where the group pays property tax, using ACS 2024 owner property tax by state or the
   builder's own key by state, with a published classification of state levy, rate and assessment limits. Report
   a central response and a range, each with its reason. Cite the incidence literature you rely on (benefit view
   versus capital-tax view, and Saiz on immigration and rents) from primary sources, not memory.
3. **Renters' property tax, keyed by occupancy.** The case keys all business property tax
   (`remaining_production_property`, $357.3bn national, $13.28bn on the group, shared) by capital ownership.
   - Split out the tax on tenant-occupied housing with BEA's housing-sector accounts (NIPA table 7.4.5 splits taxes
     on production for owner- and tenant-occupied housing), or with another primary source.
   - Key it by the group's share of renter occupancy, weighted by rent or value (ACS 2024).
   - Apply item 2's response and report the result as a reallocation that holds the national total, the way
     `applyCorrections` does.
4. **Commercial and industrial property tax, other production taxes, business transfers.** Give the long-run
   key and response for each: whose jobs or purchases the capital serves, against who owns it. Do this only where
   item 1 shows F does not already carry it.
5. **One rule, both sides.** Tabulate every receipt and spending line whose response is set by convention (0, or
   a class default) rather than measured:
   - its base, and whether that base scales with population in the long run, with evidence;
   - the current response and the response the rule implies;
   - the effect at 48 and 11.

   On the spending side this covers:
   - defense ($102.78bn on the group at the population key; hold at 0 unless evidence says otherwise);
   - existing interest ($134.54bn);
   - agricultural, transport and other subsidies;
   - general public services, which already carry 0.60–0.85.

   For defense, report the GDP-share bound beside, never in, the case. The group earns 8.78% of wages (the
   `wages` key). GDP then falls about 5.4% with capital fixed (labor share 0.6, assumed) and 8.8% with full
   adjustment: $46–75bn at $854.8bn. Use the production module's own labor share if it carries one.
   Put the share history next to it: national defense was 6.0% of GDP in FY1986, 2.9% in 2000, 4.7% in 2010 and
   3.2% in 2024 ([DoD FY2025 Green Book, Table 7-7](https://comptroller.war.gov/Portals/45/Documents/defbudget/FY2025/fy25_Green_Book.pdf)).
   Keep defense to that bound and the history; do not estimate an elasticity.

## Probe

- Load the adopted package unchanged. Reproduce `evaluateFull` at 48 and 11 with both fill-in methods averaged
  (gate), then apply overrides or a payload.
- Report each item alone at 48 and 11, then all together. Report how the items interact if they do not add.
- Re-keys must hold national totals. Gate: the other residents' share moves by the same amount in the opposite
  direction.
- The 64 specifications hold 32 distinct ones (48 ≡ 52, 11 ≡ 15). Any statistic across specifications uses the 32.
- Give the sign break-even (`sign_reversal.cjs` in the September 27 lane) with the candidate items on.

## Rules

- Work only in this directory. Do not edit the adopted case, the engine, the probe or any other lane.
- Scripts write to `derived/`. Write `RESULT.md` first with `**Verdict:** pending` and append as you go.
- Two runs through `scripts/rerun_lane.py` must be byte-identical.
- Never print the Census API key. Load it with `set -a; . infra/immigration-fiscal/acquire/config.local.env;
  set +a` and pipe Census output through a redaction filter.
- Tag every claim `[SOURCE]`, `[DATA]`, `[CALCULATION]` or `[INFERENCE]`. No commits, staging or stash.
- Final message: the RESULT path and at most ten lines, giving old → new at 48 / 11 for every item.
