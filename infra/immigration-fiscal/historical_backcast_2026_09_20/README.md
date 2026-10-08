# Historical back-cast of the 2024 fiscal concepts, 2005–2024

No year before income-year 2024 has Mexican-origin taxes, benefits or services
measured in this repository. This lane combines **measured national and population
series by year** with the **2024 relative position** from the
[complete annual account](../full_account_2026_09_20/README.md). It is a model
back-cast, not a historical account.

```sh
# inputs/acs_mexican_origin.csv (needs CENSUS_API_KEY in the environment; ~2 min)
uv run --no-project python3 infra/immigration-fiscal/historical_backcast_2026_09_20/pull_acs.py
# derived/backcast_annual.csv and derived/backcast_windows.csv
uv run --no-project python3 infra/immigration-fiscal/historical_backcast_2026_09_20/backcast.py
```

```sh
# programme-by-programme version; run backcast.py first
cd infra/immigration-fiscal/historical_backcast_2026_09_20 && uv run --no-project python3 backcast_categories.py
```

`backcast_categories.py` carries each 2024 benefit, function and household receipt line back with its
own BEA series (the source cells in `full_account_spending_2026_09_20/derived/categories.csv`; Table 3.1
lines 3, 4, 8 and 17 for direct receipts), keeps each response case's 2024 coefficients, and fails unless
every anchor reconstructs the account's 2024 value. It writes `backcast_categories_annual.csv`,
`backcast_categories_windows.csv` (with a variant setting 2020–2021 to the 2019/2022 mean) and
`national_programme_index.csv`.

## Measured by year

| Series | Source | Pin |
|---|---|---|
| Government current receipts and expenditures | BEA Table 3.1, `sources/.../bea_nipa/Section3All_xls.xlsx` | SHA256 `69b5c7ae…615e`, published 2026-08-26 |
| GDP implicit price deflator | BEA Table 1.1.9, `Section1All_xls.xlsx` | SHA256 `238ba851…1a19` |
| Midperiod population | BEA Table 7.1, [Section7All_xls.xlsx](https://apps.bea.gov/national/Release/XLS/Survey/Section7All_xls.xlsx) in `_cache/` (ignored) | SHA256 `ce107c8c…b9ef`, 1,003,641 bytes |
| Mexican-origin count | ACS 1-year `B03001_004E`, 2005–2024 except 2020 (interpolated) | `inputs/acs_mexican_origin.csv` |
| Per-capita income and median age, Mexican group and total | ACS 1-year Selected Population Profile S0201, 2008–2024 except 2010 and 2020 | same file |

`backcast.py` refuses any BEA workbook whose hash differs and checks that the 2024
totals equal the complete account's $8,008.290bn and $10,061.458bn. Since 2026-09-23 it also
carries back the adopted main case (`*_adopted_*` concepts, read from
`main_case_2026_09_23/derived/main_case_bands.csv`). Since 2026-09-24 it also carries back that case
with the data corrections (`*_corrected_*` concepts, read from
`main_case_2026_09_24/derived/main_case_bands.csv`), split on the corrected receipts in that lane's
`summary.json` (`group_receipts_bn`); a guard stops the run if that file's starting receipts differ
from the complete account's. Since 2026-09-26 the default run (`--case sept26`) also carries back the
case adopted that day (`*_sept26_*` concepts, read from `main_case_2026_09_26/derived/main_case_bands.csv`
and split on that lane's `summary.json` receipts, $492.5bn shared). Guards stop the run unless that
case starts from the band and receipts the `*_corrected_*` concepts carry. The earlier concepts do not
change value by value, and `backcast.py --case sept24 --out-dir DIR` writes the September 24 files byte
for byte. The whole-budget rules give $1.7316–2.4271tn over 2015–2024 (September 24:
$1.7317–2.4307tn), still $1.7–2.4tn. `backcast_categories.py` still covers the September 20 anchors
only.

Since the second decision of 2026-09-26 the default run (`--case sept26_schools`) also carries back the
main case with schools at full average cost (`*_schools_full_*` concepts, from
`main_case_schools_full_2026_09_26/`, gated to start from the `*_sept26_*` band and receipts). Each case
is one entry in `LATER_CASES`. `--case sept26` and `--case sept24` with `--out-dir DIR` reproduce
9d34d09 and 68f93d6 byte for byte (`test_backcast.py`). The whole-budget rules give $2.2432–2.8382tn over 2015–2024 on the schools case, against $1.7316–2.4271tn in the one-year scenario.

Since 2026-09-27 the default run (`--case sept27`) also carries back the main case of that day
(`*_sept27_*` concepts, from `main_case_long_run_2026_09_27/`). Run `node case_components.cjs` first. It
writes `derived/case_components_sept27.json`: at each profile's end specifications, the schools case's cost
there (the base) and each addition. `backcast.py` carries the base with the rules above, on the schools
case's receipts. Each addition follows its own national series times the group's population-share path:

- the long-run road and park responses, NIPA 3.17 lines 5 and 8;
- rental assistance, NIPA 3.13 line 4;
- the enterprise surplus, NIPA 3.1 line 19;
- the return on public capital, each component's net stock in FA Table 7.1 (the average of two yearends,
  at a constant real rate). The enterprise components follow line 79 together.

The flat rule holds every part per person. `derived/case_parts_windows.csv` gives each part's window sums,
`derived/case_parts_annual.csv` each part by year (read by `debt_legacy_2026_09_23`, which compounds the
cash part only).
The capital return is an imputed resource cost, not a payment. `--case sept26_schools` reproduces c1fcb27.

## v4 case (sept29), 2026-09-29

`--case sept29` carries back the adopted v4 main case (`main_case_2026_09_29/`, commit dd3a37e) as the
`*_sept29_*` concepts. It writes `derived/sept29/`: `backcast_annual.csv`, `backcast_windows.csv`,
`case_parts_annual.csv` and `case_parts_windows.csv`, with the default's names. The default stays `--case sept27`,
and its files did not move. Run `node case_components.cjs --case sept29` first; it writes
`derived/case_components_sept29.json`. Run and gated 17:17–17:21 JST (log file times). Code: `case_components.cjs`,
`backcast.py`, `test_backcast.py`.

**The rule designed here: v4's change is carried back line by line.** The base and September 27's four additions
are carried back as above, at September 27's values at the case's end specifications. The capital return takes the
case's values. The change from September 27 is split by engine line: `v4_<line>` is the line's effect less
September 27's, 32 parts with the split ones. Each part follows its own national series times the group's population-share path
(`V4_RECEIPT_CELLS`, `v4_series()`):

- A receipt line follows its NIPA cells. Personal current taxes: 3.4 lines 3 and 9–12. Social contributions: 3.6 lines 5–7,
  12–17 and 24–31. Sales taxes and customs: 3.5 lines 4, 15, 20 and 23. Property taxes: 3.3 line 9; the three
  property lines are parts of that cell. Corporate taxes: 3.1 line 5. Personal current transfers: 3.1 line 17.
- A spending line follows its category's source cells in `full_account_spending_2026_09_20/derived/categories.csv`.
  The synthetic lines, roads by miles and state pricing, follow their parent's cells.
- The pension switch is split in two:
  - The accrual it charges follows the contributions that earn it. `v4_social_security_accrual` is ratio_net × the
    group's OASDI receipts; it follows NIPA 3.6 lines 24 and 5, plus the self-employed at se_oasdi_share of line 26.
    `v4_medicare_part_a_accrual` follows lines 25 and 6, plus the rest of line 26.
  - The benefits it no longer charges (`v4_*_cash`) follow the benefit lines' own cells.
- The production grid's change, `v4_production_private` (−dP) and `v4_production_receipts` (−dF), follows nominal
  GDP, NIPA 1.1.5 line 1.
- The enterprise surplus's change is public housing's deficit moving to its own line, so it follows that deficit,
  NIPA 3.8 line 13. The national move of $40.298bn equals that line.
- `v4_housing_enterprise_surplus` follows the deficit plus the consolidated operating subsidy, as a fixed part of
  federal housing subsidies (NIPA 3.13 line 4).

Each series must equal its line's national total in 2024 (1e-3), or the run stops.

Alternative: carry v4's change back as one block with the whole-budget rules. That would carry the pension accrual,
which moves with payroll contributions, and the property-tax receipts, which move with NIPA 3.3 line 9, on national
current expenditure and receipts. The accrual parts are the largest carried item. Over 2015–2024 at the low end
(flat rule), the two accrual parts carry +$1.44tn and the benefits no longer charged −$0.72tn.

**Headline.** The 10-year total for 2015–2024, `net_cost_cbo_informed_sept29`, low / high end, 2024 dollars:

| Rule | sept29 | September 27 |
|---|---:|---:|
| flat | $3.54tn / $4.15tn | $3.07tn / $3.69tn |
| ratio | $3.21tn / $3.77tn | $2.77tn / $3.35tn |
| income | $3.50tn / $4.07tn | $3.07tn / $3.65tn |

The 15-year totals (2010–2024) are $5.16tn / $6.05tn and the 20-year totals $6.56tn / $7.68tn, flat. v4's
line-by-line change carries $0.47tn / $0.44tn of the 10-year flat total. The proportional reference,
`net_cost_full_proportional_sept29`, gives $3.80tn / $4.27tn. The cash set is not carried back as a concept of its
own. Its pension difference includes the federal income tax on benefits, and that tax sits inside
`v4_federal_income_tax` with the line's other changes. Splitting it out would need a new part and series (about
$2.1bn in 2024, at the low end).
[CALCULATION: `backcast.py --case sept29` → `derived/sept29/backcast_windows.csv`, `case_parts_windows.csv`]

**Gates.**

| Gate | Result |
|---|---|
| 1. Existing outputs reproduce | `rerun_lane.py` with the five commands below: IDENTICAL, 20 of 20 files (15 tracked, 5 new); the tracked files equal HEAD |
| 2. sept29 outputs exist and the lane's gates pass | `derived/case_components_sept29.json` (17 gates) and `derived/sept29/` (4 files). `backcast.py`'s guards stop on any failure. `pytest` 7 passed, including the rebuild of both case_components files and of `derived/sept29/` |
| 3. Oracle | Year 2024 of `net_cost_cbo_informed_sept29` is 371.4146 / 434.8410 under every rule, equal to the oracle at the file's 4-decimal rounding (tolerance 1e-4). `case_components.cjs` gates the parts' sum to the case's cost at 1e-9. The cash set, 294.7011 / 361.8175, is not a concept here (above) |
| 4. Two passes after the sept29 run | both IDENTICAL, 20 of 20 |

```sh
node infra/immigration-fiscal/historical_backcast_2026_09_20/case_components.cjs --case sept29
uv run --no-project python3 infra/immigration-fiscal/historical_backcast_2026_09_20/backcast.py --case sept29
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/historical_backcast_2026_09_20 \
  "node {lane}/case_components.cjs" "node {lane}/case_components.cjs --case sept29" \
  "uv run --no-project python3 {lane}/backcast.py" "uv run --no-project python3 {lane}/backcast.py --case sept29" \
  "cd {lane} && uv run --no-project python3 backcast_categories.py" \
  --allow-unrun infra/immigration-fiscal/historical_backcast_2026_09_20/test_backcast.py
```

## v5 case (oct05), 2026-10-05

[2026-10-05: on main case v5 (`oct05`), the 10-year total for 2015–2024, `net_cost_cbo_informed_oct05`, is
$3.71tn / $4.38tn flat, $3.37tn / $3.99tn ratio and $3.66tn / $4.28tn income, against $3.54tn / $4.15tn, $3.21tn /
$3.77tn and $3.50tn / $4.07tn for sept29. The lineage adds $0.17tn / $0.23tn under the flat rule.]

`--case oct05` carries back the adopted v5 main case (`main_case_2026_10_05/`): September 29 plus the 3.04M descendants of
Mexican immigrants who no longer report Mexican origin, counted whole. It writes the `*_oct05_*` concepts to
`derived/oct05/` (the four files of sept29) and `derived/case_components_oct05.json`. The default and `derived/sept29/`
did not move.

**The rule: the lineage at the identified third-plus generation's path.** Every September 29 part is carried back as
`--case sept29` carries it, at September 29's values at the case's end specifications (48 / 11, as on September 29).
The lineage line, v5 less September 29 at the same specifications, is added line by line (`case_components.cjs --case
oct05`):

- `v5_<line>` is the line's effect less September 29's: 67 parts. Each follows its line's national series under
  September 29's rules (`v4_series(..., "v5")`). The lineage's change in the capital return (`v5_capital_bn`) sits
  inside the three capital parts and follows each component's stock.
- Every lineage part takes the identified third-plus generation's population-share path instead of the group's.
  The Consumers row of the case lane asks for exactly this: the lineage's own count by year (the third-plus by year times
  the attrition rate) is not measured, so its 2024 ratio to the identified third-plus (3.04M to 14.34M) is held
  [ASSUMPTION]. Under the flat rule the lineage keeps its 2024 value per identified third-plus person.
- The third-plus by year is the CPS ASEC weighted count of self-identified Mexican-origin people born in the United
  States to two parents born there, survey year t + 1 for year t, as the account's 2024 is ASEC 2025
  (`cps_g3plus_path.py` → `inputs/cps_g3plus_path.csv`; IPUMS-CPS extract 4 of `g3_identity_pooled_2026_10_05`, 0.32%
  below the population lane's 14.38M on the Census file). It runs from 8.17M in 2005 to 14.34M in 2024, ×1.75, against
  ×1.46 for the group's ACS count. So the lineage weighs less in the early years than it would on the group's path.
  - The 2024 value is 9.6% above 2023's (13.08M), a larger step than the series takes in any other year.
    Every earlier year is read against it, so a smoother anchor would raise the lineage's back years.
- The pension lines are split three ways. Social security and Medicare each have the accrual the set charges (on the
  OASDI or HI contributions), the benefits the cash set charges, and minus the benefits the set does not charge (on the
  benefit lines' cells). Their sum is the set's change. The split keeps the set less the cash set separable for
  `debt_legacy_2026_09_23`.
- Two series rules are the lineage's own:
  - its enterprise surplus part follows NIPA 3.1 line 19 less 3.8 line 13, the line after public housing's deficit left
    it;
  - `lane_constants`, whose parts the back-cast does not see, is held per person.
- A cell BEA leaves blank counts as zero, as `backcast_categories.py` counts it. `veterans_other` (NIPA 3.12 line 20)
  starts in 2015.
- [APPROX] The union's own response move (−$0.30bn / −0.32bn in 2024) is inside the line-by-line change, so it rides the
  third-plus path too.

| Rule, 2015–2024 ($tn, low / high) | oct05 | sept29 | Lineage |
|---|---:|---:|---:|
| flat | 3.71 / 4.38 | 3.54 / 4.15 | +0.17 / +0.23 |
| ratio | 3.37 / 3.99 | 3.21 / 3.77 | +0.16 / +0.22 |
| income | 3.66 / 4.28 | 3.50 / 4.07 | +0.16 / +0.21 |

The lineage column is the difference of the printed totals (unrounded, flat: +0.1659 / +0.2320). Over 2010–2024 the
flat rule gives $5.40tn / $6.38tn and over 2005–2024 $6.86tn / $8.10tn (lineage +0.24 / +0.33 and +0.30 / +0.42). The
proportional reference, `net_cost_full_proportional_oct05`, gives $3.98tn / $4.51tn flat over 2015–2024.
[CALCULATION: `backcast.py --case oct05` → `derived/oct05/backcast_windows.csv`, `case_parts_windows.csv`]

**Gates.**
- `case_components.cjs --case oct05` passes 29 gates. September 29's parts and capital return equal September 29's cost at
  every end specification (1e-9). The case less the lineage is the case lane's `sept29_case` row, 371.4146 / 434.8410, and
  September 29's proportional band, 398.1491 / 448.0053 (1e-4). The lineage's parts and capital change equal
  `change_at_fixed_specifications.total`, 18.8794 / 26.4022 (1e-9). The set and the cash set differ only on federal
  income tax, social security and Medicare.
- `backcast.py` gives 2024 = 390.2940 / 461.2431 under every rule, and 419.2813 / 475.5823 for the proportional
  reference. Each lineage series equals its line's national total in 2024 (1e-3).
- `cps_g3plus_path.py` checks the extract's hash and that ASEC 2025 is within 0.5% of the population lane's count.
- `test_backcast.py` rebuilds both new files. `rerun_lane.py` over the commands below is IDENTICAL, exit 0.

```sh
uv run --no-project python3 infra/immigration-fiscal/historical_backcast_2026_09_20/cps_g3plus_path.py
node infra/immigration-fiscal/historical_backcast_2026_09_20/case_components.cjs --case oct05
uv run --no-project python3 infra/immigration-fiscal/historical_backcast_2026_09_20/backcast.py --case oct05
```

## v6 case (oct07), 2026-10-07

[2026-10-07: on main case v6 (`oct07`), the 10-year total for 2015–2024, `net_cost_cbo_informed_oct07`, is
$3,694.5bn / $4,377.9bn flat, $3,362.5bn / $3,994.0bn ratio and $3,660.2bn / $4,291.7bn income, against $3,707.0bn /
$4,377.8bn, $3,365.4bn / $3,985.7bn and $3,663.1bn / $4,283.3bn for oct05. The four items move it by −$12.5bn /
+$0.1bn under the flat rule.]

`--case oct07` carries back main case v6 (`main_case_2026_10_07/`, adopted 2026-10-07). v6 is October 5 plus four
items from the case's registry (`meta.items`):
- the pension accrual on the 2026 Trustees' separate OASI and DI funds;
- retiree health on accrual;
- the added people at their measured age mix;
- user fees and the education keys, on the union only.

It writes the `*_oct07_*` concepts to `derived/oct07/` (the four files of oct05) and `derived/case_components_oct07.json`.
The default, `derived/sept29/` and `derived/oct05/` did not move.

**The rule: each item part on its line's series, on the path of the people it prices.** Every October 5 part is carried
back as `--case oct05` carries it, at October 5's values at the case's end specifications (48 / 11, as on October 5).
The items are then added one at a time in the payload's order, the lineage item first (`case_components.cjs --case
oct07`). Step k is the case lane's `caseOf(v5, the first k items)`, so an item's change is step k less step k − 1 at
the same specification, and the last step is the case (gate, 1e-9).

- `v6_<item>_<path>_<line>` is the item's change on the line. There are 94 parts: 67 for the age mix, 4 for the
  pension item, 18 for retiree health and 5 for user fees. Each follows its line's national series under October 5's
  rules (`v4_series(..., "v6")`).
- The path follows the case lane's Consumers rules (R1–R4) [ASSUMPTION]:
  - `added_age_mix` re-values the added people's edits in place, so all of it is theirs (path lineage).
  - `pension_tr2026` and `retiree_health` split by a union twin: September 29's model plus audit row 8's change plus
    the union's part of every item so far. A cell edit takes its `union_` parts. A national-scale edit takes the line's
    national total after the step, so it scales the twin's cells as it scales the case's. The twin's change is the
    union's (path union) and the rest the added people's (path lineage).
  - `user_fees` is priced on the union only (the item's rule), so all of it is the union's.
- Path union rides the group's population-share path and path lineage the identified third-plus generation's, as v5's
  lineage does.
- Social Security and Medicare split three ways, as v5's do: the accrual the set charges, the benefits the cash set
  charges and minus the benefits the set does not charge. The pension item is set only, so its parts are accrual only.
- The capital return's change splits by component and path (`v6_capital_bn`) and sits inside the three capital
  parts. An item's offset component, the user-fee item's K-12, college and health keys, follows the stock of the
  component it offsets (`of_component`).
- [APPROX] Retiree health has no series of its own. Its parts ride their lines' NIPA series, so the history of the
  OPEB normal cost relative to each line is not measured.

| Rule, 2015–2024 ($bn, low / high) | oct07 | oct05 | Items |
|---|---:|---:|---:|
| flat | 3,694.5 / 4,377.9 | 3,707.0 / 4,377.8 | −12.5 / +0.1 |
| ratio | 3,362.5 / 3,994.0 | 3,365.4 / 3,985.7 | −2.9 / +8.3 |
| income | 3,660.2 / 4,291.7 | 3,663.1 / 4,283.3 | −2.9 / +8.4 |

The item column is the difference of the printed totals. In 2024 the items are, in order:
- `added_age_mix` +1.3466 / +2.8570;
- `pension_tr2026` −2.8463 / −2.6599 (−2.659951, rounded so the four add to the total);
- `retiree_health` +0.5844 / +0.7656;
- `user_fees` −0.2961 / −0.7261.

They add to −1.2114 / +0.2366, the case less October 5's band. Over 2010–2024 the flat rule gives $5,384.0bn /
$6,378.7bn (items −18.3 / −0.3), and over 2005–2024 $6,835.2bn / $8,096.4bn (items −23.6 / −1.3). The proportional
reference, `net_cost_full_proportional_oct07`, gives $3,969.5bn / $4,514.0bn flat over 2015–2024 (oct05 3,981.6 /
4,513.6). [CALCULATION: `backcast.py --case oct07` → `derived/oct07/backcast_windows.csv`, `case_parts_windows.csv`]

At the low end the window's change is close to ten times the 2024 change (−12.5 against 10 × −1.21). At the high end it
is well below that (+0.1 against 10 × +0.24). The largest positive item, the age mix, rides the third-plus path, which
lies below the group's path before 2024 (×1.75 from 2005 against ×1.46). So the age mix counts for less in the early
years than the pension item, most of which rides the group's path.

**Per member of the lineage (2026-10-08).** v6's per-member figures divide by the lineage the case counts, 42.75M in
2024. `derived/oct07/backcast_annual.csv` therefore also carries two kinds of column (`per_lineage_member()`):
- `lineage_millions`, the lineage's count by year. It is the union on the group's path, put on the account's frame
  (`group_millions` × the case's union, 39,712,493, over the group's 2024 count), plus the 3.04M added descendants on
  the identified third-plus path (`g3plus_millions_cps`, 2024 = 1), the lineage rule above [ASSUMPTION]. Both counts
  are read from the case lane's `summary.json` (`v5.lineage.counts`, which v6 keeps). The third-plus path grows faster
  than the group's (×1.26 against ×1.09 from 2015), so the lineage is 38.86M in 2015.
- `net_cost_cbo_informed_oct07_{low,high}__{ratio,income}__per_lineage_member_usd`, those concepts per lineage member
  in 2024 dollars.

The frame is a constant factor, so a change against 2024, or a figure at today's size, is the same on the group's frame.
Divided by the group's count path instead, the typical year's fall would read about 0.6 points larger, because the added
people's cost rides the faster path while that denominator does not. FAQ entry 18 and the INDEX read the typical-year
replay from these columns (the average of 2015–2019 and 2022–2023 against 2024): 9.8% / 10.0% less per member under the
income rule and 19.7% / 18.4% under the ratio rule. The other cases' files do not change.

**Gates.**
- `case_components.cjs --case oct07` passes 54 gates, among them:
  - the case's specifications and profiles are October 5's;
  - the last step is the case, as payloads and in cost at every end specification (1e-9);
  - the set at the case's end specifications is `summary.json` `main_case`, 389.082553 / 461.479709 (1e-9). That is
    the adopted band to within 1e-6, and `main_case_bands.csv` prints it to 4 decimals;
  - each item's parts and capital change add to its step's change (1e-9), and the edit sets move neither P nor F;
  - the case less the items is October 5's band, 390.2940 / 461.2431, and October 5's proportional band, 419.2813 /
    475.5823 (1e-4);
  - on the main profile, the items' parts and capital change equal `change_at_fixed_specifications.total`,
    −1.2114 / +0.2366 (1e-9). Each item, taken after those before it, is its change alone plus its pairs with them
    (1e-9 plus the printed remainder);
  - each edit set's union parts are its `.union` (a union-only item's with its capital change);
  - the cash set's last step is `cash_set.band_bn`, 307.3994 / 385.3641, and the 28 capital components equal
    `capital_at_end_specifications` (1e-9).
- `backcast.py` gives 2024 = 389.0826 / 461.4797 under every rule, the bands file's print, and 418.1016 / 475.8387 for
  the proportional reference. Every item part has a path, union or lineage.
- `backcast.py --case oct07` also gates the per-member columns. The case lane's union and added people must make its
  per-member population (1e-9 million). 2024 per member must be `v6.per_member_usd.set`, 9,100.88 / 10,794.29, under
  both rules ($0.01).
- `test_backcast.py` rebuilds every case_components file and `derived/sept29/`, `derived/oct05/` and `derived/oct07/`:
  12 passed. `rerun_lane.py` over the commands below: IDENTICAL, 32 of 32 files, exit 0. The tracked files equal HEAD.
- `case_components.cjs` now also counts a union-only item's capital change in its union, as the case's summary counts
  it (the user-fee item's union is its whole change, −0.2961 / −0.7261).

```sh
node infra/immigration-fiscal/historical_backcast_2026_09_20/case_components.cjs --case oct07
uv run --no-project python3 infra/immigration-fiscal/historical_backcast_2026_09_20/backcast.py --case oct07
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/historical_backcast_2026_09_20 \
  "node {lane}/case_components.cjs" "node {lane}/case_components.cjs --case sept29" \
  "node {lane}/case_components.cjs --case oct05" "node {lane}/case_components.cjs --case oct07" \
  "uv run --no-project python3 {lane}/cps_g3plus_path.py" \
  "uv run --no-project python3 {lane}/backcast.py" "uv run --no-project python3 {lane}/backcast.py --case sept29" \
  "uv run --no-project python3 {lane}/backcast.py --case oct05" "uv run --no-project python3 {lane}/backcast.py --case oct07" \
  "cd {lane} && uv run --no-project python3 backcast_categories.py" \
  --allow-unrun infra/immigration-fiscal/historical_backcast_2026_09_20/test_backcast.py
```

Log (append-only; times from `date`; claude-opus-5-5, teammate prop-b of the v6 consumer lanes):
- 2026-10-07 14:59:58–15:01:01 JST: `case_components.cjs --case oct07` (54 gates) and `backcast.py --case oct07`
  written on the adopted payload (case lane 65b05e33; corrections.json f8d346aa…, summary.json 54709259…).
  `derived/oct07/` is byte-identical to the development run on the candidate payload, whose edits and bands were the
  same.
- 15:01:01: pytest started, 12 passed in 58 s. 15:05:40–15:06:10: `rerun_lane.py` over the ten commands, IDENTICAL
  32/32, exit 0. Not committed (the lead's brief).
- 15:13:19–15:14:28: the eight case-lane hashes recorded in `derived/case_components_oct07.json` (corrections.json f8d346aa…,
  corrections_cash.json e9033bff…, summary.json 54709259…, main_case_bands.csv, package.cjs, item_age_mix.cjs and both
  lineage payloads) are the committed files' (65b05e33); no rerun needed.
- 2026-10-08 02:07:12–02:14:41 JST (claude-opus-5-5, teammate prop-a, the lead's brief): `per_lineage_member()` for
  `--case oct07`. A scratch build at 02:09:55 kept `backcast_windows.csv` and both parts files byte-identical. Its
  `backcast_annual.csv` kept all 117 columns as they were and added the five above.
  - 02:10:36–02:11:09: `rerun_lane.py` over the ten commands, every command exit 0. 31/32 files unchanged; the one
    CHANGED is `derived/oct07/backcast_annual.csv`, the columns added (its backup equals HEAD).
  - 02:13:46–02:14:13: rerun again, IDENTICAL 32/32, exit 0. 02:14:13–02:14:41: pytest, 12 passed. Not committed.

## Rules

The ACS self-identified count is scaled by 40.897m / 38.990m to the account's
own/parent-birthplace-plus-identification definition, held constant. Amounts are
2024 dollars by the GDP deflator; sums carry no interest.

- `flat`: the 2024 per-person cost is constant in real terms.
- `ratio`: the group's receipts per person stay 0.566 of national receipts per
  capita, and the spending charged to it under each response case keeps its 2024
  ratio to national current expenditure per capita.
- `income`: as `ratio`, with the receipts ratio multiplied by the group's measured
  relative per-capita income (0.519 in 2008, 0.611 in 2024; unit elasticity;
  2005–2007 held at the 2008 value, gaps interpolated).

The gap against the average resident uses a receipts shortfall less a spending
shortfall, so a deficit shared by everyone cancels. The net-cost concepts do not
cancel it: they rise in 2009–2012 and 2020–2021 with national spending.

## Limits

The spending side is never re-measured. A younger past population had more pupils
and fewer retirees per head; Medicaid expanded after 2014; pandemic business support
is inside national expenditure but was not paid in proportion to population. Total
current expenditure is a coarse scaler for the benefits and services actually charged
in the net-cost cases. Receipts need not move one for one with income. A measured
series requires rebuilding the account on each CPS ASEC file from 2005.
