**Verdict:** Candidate v2 `sept28_candidate_v2` (not adopted) is **$318.57–383.69bn**. That is **−$3.25bn at specification 48
and −$3.68bn at 11** from the September 27 case ($321.82–387.37bn), and −$5.11 / −$5.01bn from the first candidate.
Its end specifications stay 48 / 11. Each item alone, at 48 / 11:
- public housing's deficit keyed by its tenants, **−$1.69 / −$1.69bn** (the first candidate's population-key reading was
  +$0.22bn);
- production on the account's weights, **+$1.64 / +$1.11bn**, unchanged;
- the IRS-matched income-tax key, **−$3.20 / −$3.10bn**.

The items add exactly. Beside the range:
- public pay on the counterfactual workforce is **+$12.05–12.39 / +$7.85–8.09bn**, as on the first candidate;
- the fixed road stock is excluded by highway construction's across-state scaling (0.79, 95% CI 0.68–0.91);
- a stock scaled like construction adds **+$0.44–0.90bn at 48** (+$0.21–0.44bn net of congestion) and 0 at 11.

The outer range is **$255.29–432.47bn** account only and **$255.13–429.44bn** with every component read jointly with
congestion. The sign break-even is **3.55–13.95%** (September 27: 2.83–13.60%). All 96 gates pass (11 + 8 + 60 + 17),
and two runs through `scripts/rerun_lane.py` are byte-identical (18/18 files each).

## Result

Every comparison is at the fixed specifications 48 (low end: shared allocation, GDP normalization, general government
0.6000, 2%) and 11 (high end: personal, cash, 0.8504, 3%), with the two fill-in methods averaged. None is a difference
of band ends. [CALCULATION: `main_case.cjs` → `derived/fixed_specs.csv`, `derived/candidate_bands.csv`]

### Old → new at specifications 48 / 11 ($bn)

| Item | Spec 48 | Spec 11 | Placement |
|---|---|---|---|
| September 27 case | 321.8194 | 387.3701 | adopted |
| 1. Public housing's deficit at the tenant key; the $5.257811bn operating subsidy consolidated | 320.1281 (−1.6912) | 385.6788 (−1.6912) | in v2 |
| 1. The same without consolidating the subsidy | 320.1281 (−1.6912) | 385.6788 (−1.6912) | beside (moves nothing) |
| 1. The first candidate's reading: population key, subsidy consolidated | 322.0400 (+0.2207) | 387.5907 (+0.2207) | beside |
| 2. Production on the row-4 weights | 323.4621 (+1.6427) | 388.4774 (+1.1074) | in v2 |
| 3. Federal income-tax key matched to IRS 2023, raked with CBO's groups | 318.6188 (−3.2005) | 384.2735 (−3.0966) | in v2 |
| **Items 1–3 together: v2** | **318.5703 (−3.2490)** | **383.6896 (−3.6804)** | |
| First candidate (c313b53), for reference | 323.6827 (+1.8634) | 388.6981 (+1.3280) | |

The items add exactly: v2 less the September 27 case equals item 1 + item 2 + item 3 at every specification, within
1.1e-13bn. Each moves only its named lines:
- item 1 moves housing_subsidies, enterprise_surplus and the new housing_enterprise_surplus;
- item 2 moves P and F;
- item 3 moves the federal_income_tax receipt.

No other line moves, and no capital component moves by more than 1e-12. [CALCULATION: `main_case.cjs` gates]

### Item 1: public housing's deficit keyed by its tenants

- **The split.** NIPA Table 3.8 line 13 (housing and urban renewal, current surplus −$40.298bn in 2024) leaves the
  enterprise line, which goes from −$47.46bn to −$7.162bn. Every cell of that line is scaled, so its key (0.1172) and
  the enterprise capital key hold (1e-15 and 1e-12). The deficit becomes its own receipt line at the rental line's
  evaluated key (0.0740 / 0.0764 by fill-in method, mean 0.0752) and at the enterprise receipt's response (1).
  [DATA: `capital_return_services_2026_09_27/derived/enterprise_surplus_vs_return.csv` row l13, from NIPA Section 3
  T30800-A; `package.cjs` `splitHousing()`]
- **The consolidation.** The $5.257811bn operating subsidy leaves both legs. The rental line goes from 60.261 to
  55.003189, and the housing line from −40.298 to −45.555811. Under one key and one response this moves nothing: the
  difference is at most 1.1e-13bn at every specification, on the September 27 case and on v2.
- **The cost.** It moves by (ke − kh)·H = −(0.1172 − 0.0752) × $40.298bn = **−$1.6912bn at every specification**
  (−1.7403 / −1.6422 by method). That is the attack's §1 [E].
- **The choice, named.** The first candidate kept this deficit at the population key and consolidated only the
  subsidy (+$0.22bn, beside). v2 charges the deficit at the tenant key, because it finances public-housing tenants'
  below-cost rents, the same benefit the rental line's vouchers buy, which the account already charges at that key.
- **Controls.** [CALCULATION: `main_case.cjs`, internal-transfer controls]
  - Today, a synthetic $1bn on both legs moves the September 27 case by kh − ke. That is −$41.97m per $1bn, or −43.19 /
    −40.75 by method at spec 48 with capital off (the audit's positive control).
  - On v2, the same $1bn on the split legs moves the case by 0 (at most 1.1e-13) at every specification. This holds in
    the main profile, in long_run_non_school_fixed, in the proportional reference, and with v2's production and tax
    key.
  - That v2 control is not an identity. With the enterprise receipt, and so the housing line, at 0.37 and the rental
    line at 1, the $1bn moves the case by (r_h − r_x)·kh, +$47.38m per $1bn at spec 48.
  - The first candidate's after-gate is an identity. consolidate(withSyntheticTransfer(m, 1), T + 1) =
    consolidate(m, T) holds exactly on the population key too, where a transfer crosses at kh − ke. It is kept as a
    unit test of those two helpers, not as evidence about the keys.
- **Companion, not in v2.** Public housing's capital stays at the enterprise (population) key. Keying it by tenants
  too is the capital lane's variant `public_housing_at_rental_assistance_key`, already in the range's
  capital_definition component. It moves the case by −$0.3529 / −$0.5293bn, the same on v2 as on September 27, which
  gives $318.22–383.16bn. v2 keys the operating deficit only, so the enterprise's current account and its capital now
  sit at different keys. Taking both is a one-option change.

### Internal transfers that still cross differently keyed legs after item 1

A payment from a spending line into an enterprise's current surplus appears on both legs. NIPA's current surplus
includes "subsidies received from other levels of government" [SOURCE: BEA MP-5, "The current surplus of government
enterprises is equal to current operating revenues and subsidies received from other levels of government less
current operating expenses"]. The cost change per $1bn, at the evaluated keys and responses, both methods averaged:
[CALCULATION: `derived/crossings.csv`]

| Transfer | Paying leg | Receiving leg | Sept 27 ($m per $1bn, 48 / 11) | v2 |
|---|---|---|---|---|
| Public housing's operating subsidy ($5.258bn, FY2024) | housing_subsidies (rental key 0.0752, response 1) | enterprise_surplus (0.1172, 1) → housing line (0.0752, 1) | −41.97 / −41.97 | **0 / 0** |
| Other federal housing subsidies paid to housing authorities as landlords (Section 8 in NIPA 3.13 line 4; unpublished detail) | same | same | −41.97 / −41.97 | 0 / 0 where the money lands in NIPA 3.8 line 13 |
| Federal operating subsidies to state and local mass transit | other_subsidies (resources key 0.0806, response 0) | enterprise_surplus (0.1172, response 1) | −117.18 / −117.18 | **−117.18 / −117.18** |
| Federal subsidies to the Federal Crop Insurance Corporation | same | same | −117.18 / −117.18 | −117.18 / −117.18 [UNVERIFIED]: crosses only if the FCIC is an enterprise whose surplus holds the subsidy |

- **The transit amount.** NIPA 3.13 line 7 (federal "Other") was $24.627bn in 2024. Its footnote says it "consists
  largely of subsidies to railroads, mass transit systems, and the Federal Crop Insurance Corporation"
  [DATA: `sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx`, T31300-A]. The transit part is not
  published separately [UNVERIFIED]. If all of line 7 crossed, the case would fall by at most $2.89bn. That is a
  bound, not an estimate.
- **Other crossings.** Sales between agencies and enterprises, such as utilities selling to schools, also cross legs.
  They are purchases, not transfers, and are not listed.

### Item 2: production on the account's weights

This is the first candidate's item 2, unchanged: +$1.6427 / +$1.1074bn. It moves no line and no capital component, and
the cost moves by minus the change in P + F at every specification.
[CALCULATION: `main_case_candidate_2026_09_28/derived/production_row4.json`]

### Item 3: the federal income-tax key matched to IRS 2023

- **The edit.** `share_change.irs_2023_raked_with_cbo_groups` is 0.0014611 for personal and 0.0014841 for shared, of
  the $2,403.242bn line. It is applied as the tax lane's `ends.cjs` applies it: stack factor × national × share change,
  expanded to every incidence rule, with the stack factor of the tax-block case being run. The group's income tax rises
  by +$3.119 / +$3.236bn (hotdeck) and +$3.074 / +$3.165bn (matched), personal / shared.
- **The cost.** It falls by exactly that: **−$3.2005 / −$3.0966bn** at 48 / 11. That is the tax lane's own figure,
  matched per method within 6.1e-14 (`main_case_translation.json` `union_tax_change_bn`). Item 3 alone gives the tax
  lane's band, $318.62–384.27bn.
  [DATA: `tax_key_heldout_2026_09_28/derived/translation_inputs.json`; CALCULATION: `main_case.cjs`]
- **Approximation.** In the range, every income_tax variant (CBO 2018, 2019 or 2022 data, scaled or not) takes the
  same IRS share change on top of its own gradient. The tax block's variants carry their own stack factors, which
  widens that component by $0.10–0.11bn at each end.

### Public pay on the account's own workforce (beside the range)

The charge is the first candidate's, the public part of P + F at the reference cell. The counterfactual readings charge
it on the public workforce the account's own responses leave, charge × (1 − removal share). The approximation is a
uniform removal share across skill groups. Schools have more skilled staff and above-average removal, so the overlap is
more likely larger than smaller (attack §4d). [CALCULATION: `package.cjs` `publicPay()`; `main_case.cjs`]

| Reading | Removal share (48 / 11) | Spec 48 | Spec 11 |
|---|---|---|---|
| Unchanged workforce (the first candidate's reading) | — | +13.6085 | +8.9520 |
| Counterfactual workforce, all consumption lines | 8.96% / 9.63% | +12.3887 | +8.0899 |
| Counterfactual workforce, without defense and with the school rows | 11.43% / 12.27% | +12.0537 | +7.8533 |

Items 1–3 touch no consumption line, so every reading is the same on v2 as on the first candidate (1e-12). On the
first candidate the readings reproduce the attack's section 4: 12.05–12.39 and 7.85–8.09. With public pay the ends
move to 32 / 27, the normalization swapped at both ends, and the bands run from $330.50–391.63bn (high share) to
$331.52–393.30bn (unchanged workforce).

### The road arm (beside the range)

Each case is shown as a change from v2 at 48 / 11. The congestion item beside the account is priced at the same
specifications' lane cut. [CALCULATION: `derived/road_arm.csv`; `road_stock.py`, `road_congestion.py`]

| Case | Account | Congestion item | Net |
|---|---|---|---|
| Stationary network (v2's setting, as on September 27) | 0 / 0 | 13.99 / 12.02 | 0 / 0 |
| Replacement adjustment (lanes fixed) | −5.23 / −10.75 | 19.16 (+5.17 / +7.14) | −0.06 / −3.60 |
| Fixed stock (lanes fixed) | −10.51 / −17.97 | 19.16 (+5.17 / +7.14) | −5.34 / −10.83 |
| Upward: stock scaled like construction, year effects | +0.90 / 0 | 13.54 / 12.02 (−0.46 / 0) | +0.44 / 0 |
| Upward: stock scaled like construction, land control | +0.44 / 0 | 13.77 / 12.02 (−0.22 / 0) | +0.21 / 0 |

- **The fixed stock is excluded by data.** State and local nontoll highway construction (Census F44) scales with
  population across states at **0.792 (95% CI 0.675–0.908)** with year effects, and 0.758 (0.666–0.850) with a land
  control. A stock that did not respond, 0, lies outside both intervals.
  [CALCULATION: `road_stock.py`, running the attack's `probe_road_stock.py` unchanged; its rows reproduce]
- **The upward case.** Construction's slope replaces the operations slope where the case reads it, S&L highways at the
  low end: r 0.8022 / 0.7699 against 0.7392. The high end is capped at 1 either way, so the case moves nothing at 11.
  Its lanes follow the stock, and the deeper lane cut lowers the congestion item.
- **Independence from the items.** Each road case moves v2 exactly as it moves the September 27 case, within 1.1e-13
  at every specification. Replacement and the fixed stock reproduce the first candidate's per-specification moves.

### The outer range

"Account only" re-runs the September 27 components on each base at every specification. "Jointly" adds, to each
variant's account change, the change in the congestion item at its band ends' lane cut. That cut is taken at each
method's end specification, with the two methods' cuts averaged, as the bridge averages the key. This is the
dependent-pieces placement rule applied to every component. [CALCULATION: `derived/components.csv`, `summary.json`
`range`]

| Base | Band | Outer, account only | Outer, jointly | Quadrature (account / jointly) |
|---|---|---|---|---|
| September 27 | 321.82–387.37 | 258.65–436.05 | 258.49–433.02 | 290.90–408.23 / 290.87–406.01 |
| First candidate | 323.68–388.70 | 260.52–437.37 | 260.36–434.35 | 292.76–409.56 / 292.74–407.33 |
| **v2** | **318.57–383.69** | **255.29–432.47** | **255.13–429.44** | 287.63–404.57 / 287.60–402.35 |

Three of the 19 components have a dependent congestion piece:
- **long_run_response.** The highway responses move the cut. Read jointly, the low end goes from −0.3339 to −0.2429
  and the high end from +15.5402 to +12.3830. Uncapping within states nets to +12.3160. The held-at-zero-lines variant
  (+12.3830) does not move roads, so it becomes the extreme.
- **consumption_key.** Its variants move the economic-affairs (resources) key, and with it the cut, in the same
  direction as the account. This component therefore widens: from −3.5124 to −3.7543 at the low end, and from +0.9405
  to +1.0528 at the high end.
- **tax_block.** Each fill-in method has its own economic-affairs key: ±0.011 / ±0.016.

The attack's recipe, the long-run component alone at 48 / 11, reproduces its $260.6094–434.2178bn on the first
candidate. On v2 it gives $255.39–429.31bn. The all-component rule differs from it by the consumption-key and
tax-block pieces.

On v2 against the first candidate, only the tax block moves by more than $0.005bn: it widens by $0.10–0.11bn at each
end (item 3). The range therefore follows the centre.

### Specifications, ends and runner-ups

- **The specifications.** The 64 specifications are 32 distinct ones, each appearing twice. The pairs 48 ≡ 52 and
  11 ≡ 15 are identical in every field and in cost, in all 25 option sets. The ends, the runner-ups and `per_spec.csv`
  (32 × 2 methods) use the 32. [CALCULATION: `derived/ends.csv`]
- **The ends.** In both methods, v2's low end is 48: shared, GDP, school share 0.7153, general government 0.6000,
  uninsured care at low use, 2%. Its runner-up is 56 (school share 0.8652), +$0.79bn. The high end is 11: personal,
  cash, school share 0.8652, 0.8504, high use, 3%. Its runner-up is 3 (school share 0.7153), −$0.81bn.
- **Where they hold.** The same ends and runner-ups hold for the September 27 case, the first candidate, each item
  alone and every road case. Public pay alone moves them, to 32 / 27, with 48 / 11 the runner-ups at $0.09–0.66bn.

### The sign break-even, re-derived

This is the adopted definition (`main_case_2026_09_24/sign_reversal.cjs`, imported unchanged): the common share s of
ordinary service budgets at which the account changes sign. It adds the September 27 case's rental, enterprise and
capital terms, and v2's housing line responds with the enterprise receipt. Each cell below takes the lower of the two
allocations' low ends and the higher of their high ends. [CALCULATION: `sign_reversal.cjs` → `derived/sign_reversal.csv`]

| | Sept 27 | Item 1 | Item 2 | Item 3 | First candidate | **v2** |
|---|---|---|---|---|---|---|
| Enterprises respond at s | 2.83–13.60% | 2.93–13.75% | 2.70–12.99% | 3.58–14.41% | 2.79–13.07% | **3.55–13.95%** |
| Enterprises held at 1 | −2.87–9.65% | −2.44–10.10% | −3.01–9.01% | −2.08–10.50% | −3.07–8.95% | **−1.79–10.31%** |
| Frozen services, capital fixed, welfare $bn (enterprises at 1) | −53.49 to 57.77 | −51.80 to 59.47 | −54.01 to 53.93 | −50.39 to 60.97 | −54.23 to 53.71 | −49.22 to 58.82 |

The September 27 and first-candidate columns reproduce their committed files (1e-4). Each model gives its package's
band (1e-9). At s = 1 the wrapped definition is the proportional reference on v2 at every specification, and welfare
is linear in s.

### Adoption path (specified, not implemented)

v2 needs three payload extensions beyond the September 27 `corrections.json`. [CALCULATION: on the payload model,
`Engine.applyCorrections(model.json, corrections.json)`]

- **(A) The split.**
  - It adds a new receipt line, `housing_enterprise_surplus`, with national −$45.555811bn (NIPA 3.8 line 13, −40.298,
    less T). Its cells, in all 8 incidence rules, sit at the rental line's `housing_support` fraction (0.075207 in both
    allocations on the payload model, target −$3.426129bn), with `direct: false` and class `public_asset`.
  - `meta.responses.housing_enterprise_surplus` would be `{receipt: true, override:
    "receipt:housing_enterprise_surplus", low: 1, high: 1}`: it follows the enterprise receipt.
  - Two national totals change, with every cell scaled: enterprise_surplus −47.46 → −7.162 (factor 0.150906) and
    housing_subsidies 60.261 → 55.003189 (factor 0.912749).
  - `meta.capital_return` needs no change, because the enterprise key (receipt amount over national) holds.
  - `engine.js` `applyCorrections` cannot express this today. It adds only spending lines at national 0, and its edits
    keep national totals fixed. It needs a receipt-line field and a national-scale edit.
  - Expressing item 1 as an ordinary enterprise_surplus edit instead, by (kh − ke)·H, would move the enterprise capital
    key from 0.1172 to about 0.0815. Every consumer that computes the capital return from `meta` would then need a new
    key kind, so that form is no cheaper.
- **(B) Production.** The row-4 grid (`main_case_candidate_2026_09_28/derived/production_row4.json`, sha256
  69839e58a960…) replaces model.json's three production arrays. It is carried as a pointer with its hash, or embedded.
- **(C) The tax key.** These are ordinary receipt edits on federal_income_tax, the methods' mean: +3.096568 (personal)
  and +3.200535 (shared) in the reference rule. They are expanded to the 8 rules; federal_gap_high_agi gets 2.864970 /
  2.980487 and the others are equal. They compose with the existing −26.76 edit on that line.

The consumers that read the adopted payload, from `rg -l corrections.json infra/`, are below. The code was read by an
Explore agent, and three of its claims were spot-checked (band_variants 141–163, winners_losers 136–151,
sept24_specs 56–63).

| Consumer | (A) split | (B) production | (C) tax edits |
|---|---|---|---|
| `assumption_explorer_2026_09_21/engine.js` (the applier) | change: no receipt lines or national edits | only if the grid travels in the payload | none |
| `generation_account_2026_09_24/run_generations.cjs` | change: generation payloads and gates | change | change: gates require schools + 8 re-key edits |
| `late_arrival_account_line_2026_09_27/run_cells.cjs` (`--case sept27`) | change | change | change (same gates) |
| `debt_legacy_2026_09_23/debt_legacy.py` (its own Python engine copy) | change | change | change: gate on the exact edit set |
| `sept24_propagation_2026_09_24/band_variants.cjs` | change: rebuilds line responses by name | change | none |
| `uncertainty_propagation_2026_09_22/sept24_specs.cjs` | change: `lineTargets` throws on a new receipt line | change | none |
| `winners_losers_2026_09_24/specs.cjs` | change: requires exactly 4 line responses | change | none |
| `historical_backcast_2026_09_20/case_components.cjs` | change: fixed line list, "no other line moves" gate | change | change |
| `world_ledger_2026_09_27/split_residual.py` | change: gates reject a new line or a national change | none | none |
| `world_ledger_2026_09_27/generation_lines.cjs` (pinned generation payloads) | none once the engine carries (A); needs a new pin | none | none |
| `distribution_weights_2026_09_23/distribute.py` (`meta.responses` only) | none | change: assumes P and F never move | none |
| `sept24_propagation_2026_09_24/real_costs_totals.py` (congestion figure only) | none | none | none |

- **Case tables.** Every consumer that reaches the case through a table also needs a v2 entry: run_generations,
  run_cells, generation_lines, band_variants, sept24_specs, specs and case_components, plus
  `distribution_weights_2026_09_23/case_ends.cjs`.
- **Superseded consumers need nothing now.** These are the explorer UI (on Sept 26, lagging by design), figures,
  consumption_key, the older producers, the capital and response lanes that feed the adopted case, and the frozen
  first candidate and 09-27 audit probe.

### Flags

- **Transit's deficit.** Public transit's −$66.69bn deficit (NIPA 3.8 line 14) is still keyed by population. By item
  1's rule it belongs at its riders' key, which the account does not carry. The foreign-born commute by transit at a
  higher rate than the native-born [TRAINING-DATA], so the population key likely understates the group's share. It is
  not priced here.
- **The income_tax range variants** apply the same IRS share change on top of each CBO gradient. That is an
  approximation.

## Gates and reproducibility

All 96 gates pass, in four scripts:
- `road_stock.py`, 11 gates: the probe is the case's model, and the construction rows reproduce the attack's.
- `road_congestion.py`, 8 gates: the bridge's B1 and four rows are repriced, and the congestion item is monotone in the
  lane cut.
- `main_case.cjs`, 60 gates, as described above. They include:
  - the September 27 case at every specification, exactly, against its committed per_spec.csv;
  - the first candidate at every specification, exactly, against its committed per_spec.csv;
  - an independent path: engine, model.json, the September 27 corrections.json, H, T, the row-4 grid and the tax lane's
    own change, matching v2 at every specification within 2.3e-13;
  - the published ranges of September 27 and the first candidate, to 0.0;
  - the attack's joint range.
- `sign_reversal.cjs`, 17 gates.

The run order is `road_stock.py`, `road_congestion.py`, `main_case.cjs`, `sign_reversal.cjs`. After running them in
place, `uv run --no-project python3 scripts/rerun_lane.py
infra/immigration-fiscal/main_case_candidate_v2_2026_09_28 "uv run --no-project --with scipy python3
{lane}/road_stock.py" "uv run --no-project python3 {lane}/road_congestion.py" "node {lane}/main_case.cjs" "node
{lane}/sign_reversal.cjs" --allow-unrun infra/immigration-fiscal/main_case_candidate_v2_2026_09_28/package.cjs`
reported IDENTICAL, 18/18 files, on both runs. `summary.json` `inputs` records the sha256 of 14 inputs: for example the September 27
payload d3b10f144ebf…, the first candidate's package ed7f3dc5d8d9…, and this package 029cf65a0ec6….

## Files

- `package.cjs`: the definitions. It imports the first candidate's package unchanged: items 1–3, the road cases, public
  pay, the specification and range descriptors, and the congestion cuts.
- `road_stock.py`: construction's across-state slopes, from the attack's probe. It writes `derived/road_stock.json`.
- `road_congestion.py`: the congestion item at every lane cut the lane uses. It writes `derived/road_congestion.json`.
- `main_case.cjs`: the gates, then `derived/fixed_specs.csv`, `candidate_bands.csv`, `ends.csv`, `components.csv`,
  `per_spec.csv`, `road_arm.csv`, `crossings.csv` and `summary.json`.
- `sign_reversal.cjs`: writes `derived/sign_reversal.csv`.

## Log (append-only)

- 2026-09-28: stub written after reading `BRIEF.md` (08b1b7d). Case name `sept28_candidate_v2`; builds on the first
  candidate's package (`main_case_candidate_2026_09_28`, c313b53) and the adopted September 27 case, neither edited.
  Worker: mainbuild, model claude-opus-5-5.
- 2026-09-28: `road_stock.py` written and run (11 gates). `package.cjs` written. The first count of congestion cuts was
  61, because each method's key differs; cuts are now the two methods' mean at a band end, as the bridge reads k,
  which gives 35 cuts. `road_congestion.py` written and run (8 gates); it reprices the bridge's rows to 1e-9.
- 2026-09-28: `main_case.cjs` (60 gates) and `sign_reversal.cjs` (17 gates) written and run into a scratch directory,
  then in place; the outputs match byte for byte. Only three components (long-run response, consumption key, tax block)
  have a dependent congestion piece; the consumption key widens jointly. The adoption-path consumer list came from an
  Explore agent over the 85 files `rg` finds; three of its claims were checked against the code.
- 2026-09-28: `scripts/rerun_lane.py` over the four commands: IDENTICAL, 18/18. Verdict written.
- 2026-09-28: a runner-up margin corrected in the text ($0.09–0.66bn, not $0.13–0.66bn; ends.csv was right); second
  `scripts/rerun_lane.py` run: IDENTICAL, 18/18.
