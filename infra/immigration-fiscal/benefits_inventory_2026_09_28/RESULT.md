**Verdict:** The account already carries the large benefit channels: every direct tax, the long-run production term with its induced taxes, care, elder care and housing, and an implicit credit worth about $271bn a year, because defense and existing interest are never charged to the group. The capital owners' gain (the "immigration surplus") is in the code, but only in its long-run form, where it is exactly zero. The short-run version, with capital fixed, would add $13.8–26.1bn a year (central $20.4bn, −$499 per member on the cost convention). That rests on a frame the case rejects for public capital, and it turns into a net loss to US residents once more than 5.7% of the capital income goes to owners abroad (foreigners hold about 40% of US corporate equity). Among the new candidates, only formal volunteering (a gain of about $6.2bn, speculative) and the corporate tax on foreign-owned capital serving the group's jobs ($0–21bn, retention unmeasured) have any size. Military service, giving, culture and fertility add nothing measurable. Recommendation: add nothing new to the headline, and keep the three priced items beside it as arms. [FRAMING-SENSITIVE]
claude-opus-5-5

**2026-10-14 P7 update:** The September 28 inventory and verdict are historical; v7 now carries job-capital taxes. The P7 volunteering and city-tax checks below preserve the outgoing volunteering central. Food receipt is measured; incoming volunteer labour and displacement remain conditional. The city-size benefit already includes induced taxes, so the proposed additional city tax credit is **zero**.

# Benefits inventory: channels through which the Mexican-origin union's presence benefits other US residents

Lane `infra/immigration-fiscal/benefits_inventory_2026_09_28/`, dispatched 2026-09-28 by team-lead. Frame: the adopted September 27 main case, 2024 with and without the 40.9m CPS 2025 union, effects on all other residents. Money is $bn a year at 2024 prices. In `items.csv` a benefit is a negative cost. In the tables below, sizes read as gains to other residents unless a line says "cost".

## Inventory

The full list, with 33 rows, is in `derived/inventory.csv`.

| Channel | In the account? | Where | Size (gain to others) | Recommendation |
|---|---|---|---|---|
| Direct taxes (income, payroll, sales, excise, customs) | inside, response 1 | `assumption_explorer_2026_09_21/engine.js:41-44,152-157`; `model.json` receipt cells with `direct=True` | federal income $128.2bn, payroll $150.6bn, sales $48.8bn | nothing |
| **Public-good cost sharing (defense, existing interest)** | inside, as an implicit credit | `engine.js` `defaultState`: `public_goods_response 0`, `interest_response 0`, `subsidy_response 0`; `main_case_long_run_2026_09_27/derived/corrections.json` `meta.responses` overrides none of them | ≈$270.8bn at the population share [CALCULATION: (854.8+1,397.7)×0.1202] | nothing: already credited |
| Production term P+F (two skill cells, induced taxes) | inside | `matched_benefits_2026_09_19/model.py:7-106`; `engine.js:176-183` | $8.8 cash / $13.3bn GDP | nothing |
| Native–immigrant nest (ε 3) | beside, proposed | ladder 176, 181; winners_losers channel table | $6.7bn (5.3–8.0) | beside |
| **Capital owners' surplus, capital fixed** | not inside (grid cell exists but is unadopted) | this lane | $13.8–26.1bn; $22.8bn less than as many average residents | beside, as an arm only |
| Capital owners' surplus, half adjusted | not inside | this lane | $3.4–6.4bn | beside |
| Capital owners' surplus, capital adjusted | inside, at 0 | `model.py:50-56`; `model.json` reference `capital_adjustment 1.0` | 0 by construction | nothing |
| Corporate and business-property tax on capital serving the group's jobs (Clemens) | beside, response 0 | `full_account_2026_09_20/welfare.py:28-31`; `receipt_side_long_run_2026_09_28` item 4 | lane 253: $81/87bn if lost outright; foreign-owned corporate part $0–21.3bn | beside; measure retention first |
| The group's own capital and businesses | its personal taxes are inside; capital-keyed taxes at 0 | `model.json` receipts; production model `excluded_owner_share 0` | capital key 3.11% vs 12.1% of population | nothing |
| Property taxes (owner, tenant, personal) | candidate (253) | `receipt_side_long_run_2026_09_28` | $19.05 + $6.81 + $1.33bn | in progress |
| Cheaper services (Cortés prices) | inside P, side view | care lane `summary.csv`; ladder 198 | $21.8bn gross, $11.9bn net | never add |
| Cheaper construction | inside P | ladder 200 | 0.75% lower costs; $0 added | nothing |
| Care: taxes on native women's hours | inside (fiscal) | ladder 198 | $2.69bn | nothing |
| Family elder care | inside (fiscal) | care lane `summary.csv`, row 3 | $1.49bn (1.20–7.62) | nothing |
| Housing net | beside (social item) | ladder 190 | $3.5bn (−0.4 to 9.4) | adopted |
| City size and schooling mix | being adopted | `scale_spillovers_2026_09_23` | $13.9bn | add (in adoption) |
| Restaurants, market size | being adopted | `disease_food_2026_09_28` | $6.8bn; $1.2bn less than average residents | add (in adoption) |
| Restaurants, cuisine composition | beside | same | $0.6bn, sign uncertain | beside |
| Mobility insurance | beside | ladder 203 | $0.65bn | beside |
| Innovation, idea production (Jones) | not added | ladder 201 | patent term $37–57bn inside a ±$490bn interval | nothing |
| Fertility, future population | outside the annual frame | 2024 is the only measured year; generation account ladder 224 | n/a | nothing |
| Trade networks | **in progress** | `trade_networks_2026_09_28` | not priced here | await the lane |
| Consumer scale: variety prices, network utilities, media variety | **in progress** | `consumer_scale_2026_09_28` | not priced here | await the lane |
| Cultural output | no dollar line; its variety goes to consumer_scale | ladder 156 | creative labour 0.72–0.74 of whites' per head | nothing |
| Military service | outside the frame | the union is the CPS civilian universe, so active-duty members are not removed | 0 | nothing |
| Charitable giving | not priced | CE 2024: $911 per Hispanic consumer unit vs $2,292 for all; CEV 2023 giving rate 30.9% vs 52.4% for non-Hispanics | beneficiaries unmeasured; charity received is a counter-flow | nothing |
| Formal volunteering | beside (priced here) | CEV 2023 | $6.2bn (4.5–7.9); $4.2bn less than average residents | beside |
| Pay-as-you-go payroll, never-claimed payroll | inside; the accrual arm and 254 carry the rest | ladder 254, 257 | payroll receipts $150.6bn | nothing |
| Government enterprises, public purchases, remittances | inside, or neither cost nor benefit | main case option D; ladder 200; memo §8 | $5.56bn enterprises | nothing |

## Pricing

**Is the return to capital in the production term?** Yes. `model.py` nests two CES skill cells under Cobb-Douglas capital. The capital owners' gain `domestic_capital_gain = (1−s)(1−output)` is netted against the released capital's opportunity income `(1−s)(1−capital)` (lines 50–56). The engine's reference cell sets `capital_adjustment 1.0`, which makes the net capital gain exactly zero: capital adjusts. The fixed and half cells were computed on 2026-09-19 but never adopted. The script reproduces the adopted P+F of $8.79 cash / $13.32bn GDP with a capital gain of 0 (gated). [CALCULATION: `price_capital_surplus.py`]

**Efficiency units.** The union supplies $1,049.6bn of the $12,565.6bn CPS ASEC 2025 positive-earnings pool, **8.35%** of labour input in efficiency units (17.83% of the HS-or-less pool, 5.75% of some-college-plus). As many average residents would supply 12.15% of every pool. [DATA: `matched_benefits_2026_09_19/derived/skill_composition.csv`; `target_population_cps2025.csv`]

**Factor-price elasticity.** NAS (2017, ch. 4), verbatim: "65 percent of total national income is paid as employee compensation; it is therefore reasonable to assume that the elasticity of the own factor price for labor is −0.35". Its formula ½·s·|e|·m²·Y reproduces its own "$54.2 billion" for 16.5% of hours (54.19 here). [SOURCE: [NAS ch. 4](https://nap.nationalacademies.org/read/23550/chapter/8); excerpts in `reads/nas2017_ch4_surplus_excerpts.txt`]

| Capital owners' surplus, beyond the adopted term | Cash | GDP | Grid (s .60–.70, σ 1.5–2.5, both normalizations) | Normalized vs average residents |
|---|---:|---:|---:|---:|
| Short run, capital fixed (NAS convention: natives own all capital) | +16.22 | +24.59 | +13.84 to +26.12 | union gives 15.4–29.1 less (central 22.8) |
| Half adjusted | +3.98 | +6.03 | +3.39 to +6.40 | 3.7–7.0 less |
| Long run, capital adjusted | 0 | 0 | 0 | 0 |
| Check: NAS homogeneous formula, m = 8.35%, s .65 | +15.34 | +23.25 | 13.2–24.5 (s .70–.60) | average residents 32.4 / 49.2 |

- **The redistribution behind the short-run gain** [CALCULATION: `derived/capital_surplus_summary.json`]:
  - capital owners gain $376 / $570bn;
  - outside workers lose $351 / $532bn;
  - taxes fall by $48.8 / $73.9bn, because labour taxes shrink faster than capital taxes grow.
- **Foreign owners** [CALCULATION: `build_tables.py`]:
  - Once owners outside the beneficiary set are excluded (the model's `excluded_owner_share`), the short-run increment reaches zero at a **5.7%** foreign share of the capital income.
  - At 10%, 20% and 40% it becomes a cost of $15.3bn, $50.9bn and $122.3bn. Normalized against average residents at the same share, the gap is +$6.7bn, −$9.5bn and −$41.7bn.
  - Foreigners hold "about 40 percent of total US equity" (2019) [SOURCE: [Rosenthal–Burke](https://www.law.nyu.edu/sites/default/files/Who%E2%80%99s%20Left%20to%20Tax%3F%20US%20Taxation%20of%20Corporations%20and%20Their%20Shareholders-%20Rosenthal%20and%20Burke.pdf)], and 42% at the end of 2022 [SOURCE: Rosenthal–Mucciolo, Tax Notes 2024]. The economy-wide share of the model's capital income is lower and is not measured here.
- **Corporate tax on foreign-owned capital serving the group's jobs.** This is corporate receipts ($663.69bn) × the wage key (8.02% / 7.48%) × 0.40 × (1 − retention): $0 at the account's retention of 1, $10.3bn at 0.5, $21.3bn at 0. Normalized, the union carries $5.8bn less than average residents at 0.5. Lane 253's all-owner figure, lost outright, is $81/87bn; that lane ruled it not a candidate. [CALCULATION: `build_tables.py`]
- **Formal volunteering.** The union has 30.25m people aged 16+ [ASSUMPTION: 16–17 is a third of 12–17]. At a 16.9% formal rate [SOURCE: AmeriCorps CEV 2023, `bhmf-84dy`], 65.9 hours per volunteer and $33.51 an hour [SOURCE: americorps.gov: 4.99bn hours, 75.7m volunteers, $167.2bn], output is $11.29bn gross. A non-group beneficiary share of 0.4 / 0.55 / 0.7 [ASSUMPTION] gives a gain of **$4.5 / $6.2 / $7.9bn**. Average residents volunteer at 28.3%, so normalized the union gives $4.2bn less.
- **Charitable giving is not priced.** Hispanic consumer units report $911 of cash contributions against $2,292 for all units [SOURCE: FRED CXUCASHCONTLB1002M, CXUCASHCONTLB0101M, BLS CE 2024]. That category also includes alimony and support of students. Beneficiaries are unmeasured.

## Disconfirmation

1. **Capital surplus "missing".** The code search came first. The channel is in the model, and the adopted case chose its long-run form. NAS itself says "Once the capital-labor ratio is restored, the adverse wage effect of immigration and the immigration surplus disappear", and warns that the static method is "problematic" for "the entire population of immigrants, which has grown over the course of decades". The main case charges the group a 2–3% return on public capital, which assumes public capital scales with population. Pairing that with fixed private capital would be inconsistent: a short-run arm must also drop the public-capital charge ($33.8–55.7bn). [FRAMING-SENSITIVE]
2. **NAS convention against the data.** The surplus assumes natives own the capital. Foreign equity ownership of 40% of corporate equity puts the relevant share plausibly above the 5.7% break-even, which can flip the short-run arm's sign.
3. **Public goods.** Checked in the engine: the group's receipts are credited in full, while defense, interest and subsidies respond at 0. The channel is present, and in the group's favour.
4. **Corporate tax.** `receipt_side_long_run_2026_09_28` had already priced the all-owner version beside the case. P+F is $13.32bn at every retention while owners are included, so only foreign or excluded owners can make it a net gain.
5. **Charity and volunteering.** The group's rates are below average: 16.9% vs 28.3% formal volunteering, $911 vs $2,292 per unit. Normalized, both are relative costs. The absolute gains are speculative.
6. **Care and elder care, cultural output, innovation.** All of these were already carried or ruled on (ladder 156, 198 and 201). Nothing was re-priced.

## Files covered and skipped

- **Covered:**
  - The main case: `main_case_long_run_2026_09_27` (RESULT; `package.cjs`; `corrections.json` `meta.responses`) and `main_case_2026_09_24/package.cjs:81-82` (`count_production`).
  - The engine and production model: `assumption_explorer_2026_09_21/engine.js` and `derived/model.json`; `matched_benefits_2026_09_19` (`model.py`, `builder.py`, `skill_composition.csv`, memo).
  - The research record: the real-costs memo §3, 5, 7, 7b and 8; the winners_losers channel table; ladder rows 156, 176, 181, 194, 198, 200, 201, 203 and 244–263.
  - Other lanes: care `summary.csv`, disease_food `items.csv`, scale `summary.csv`, `receipt_side_long_run_2026_09_28`, `receipt_long_run_probe_2026_09_28` and `full_account_2026_09_20/welfare.py:21-31`.
  - External: NAS ch. 4 (primary), FRED/BLS CE, the AmeriCorps CEV data and Rosenthal–Burke.
- **Skipped:**
  - `decisions/2026-09-23-evidence-symmetry-rules.md` was not opened; the rules came from memo §7b. [GAP]
  - Borjas (1995) primary: NAS restates and cites it, and the formula is verified on NAS's own number. [GAP]
  - The internals of `main_case_schools_full_2026_09_26` (the production flag comes from the 09-24 package it builds on).
  - `consumer_price_benefit_2026_09_18` and `cultural_output_2026_09_19` (read through memo §7b and ladder 156).
  - `trade_networks_2026_09_28` and `consumer_scale_2026_09_28`, deliberately.
- **Outputs:**
  - `derived/items.csv` (12 rows);
  - `derived/inventory.csv` (33 rows);
  - `derived/capital_surplus_grid.csv` and `derived/capital_surplus_summary.json`;
  - `reads/nas2017_ch4_surplus_excerpts.txt`.
- **Scripts:** `price_capital_surplus.py`, then `build_tables.py`, run from the repo root.

## Log
- 2026-09-28 23:00 JST — Stub written; read the production term. `matched_benefits_2026_09_19/model.py:7-57` carries the return to capital net of the released capital's opportunity income. The engine reference is `capital_adjustment 1.0`, so the adopted P+F holds a net capital gain of zero. The fixed-capital cell exists but is unadopted.
- 2026-09-28 23:07 JST — Ran `price_capital_surplus.py`. The production term reproduces ($8.79 / $13.32bn). Fixed capital adds +$16.22 / +$24.59bn, half adjustment +$3.98 / +$6.03bn. The NAS formula reproduces $54.2bn and gives $15.3 / $23.3bn for m = 8.35%.
- 2026-09-28 23:17 JST — Ran `build_tables.py`: foreign-owner break-even 5.7%; corporate tax on foreign-owned capital $0–21.3bn; volunteering $6.2bn; inventory of 33 rows. Remaining [GAP]s: the retention share for relocated capital; the economy-wide foreign share of capital income; the evidence-symmetry decision file not read.

## P7, 2026-10-14: volunteering both ways and city-size taxes

**Verdict:** Keep the outgoing central. The CPS Food Security files measure household food-aid use, which supports a bounded allocation exercise; they do not identify the volunteer hours the group receives or the amount that would reach outsiders without it. On 2024 receipt shares, the conditional reverse-food proxy is **$2.49–5.35bn** for the identified union or **$2.68–5.76bn** on the lineage extrapolation if all that labour is redirected to outsiders. At half displacement the changes are **$1.24–2.67bn** and **$1.34–2.88bn**. Zero displacement preserves the existing central. These are alternative proxy scenarios, not an identified interval or a measured net volunteering balance. The broad proxy at full displacement clears the $5bn review bar; the narrower and half-displacement scenarios do not. [CALCULATION: `social_receipts.py` → `derived/volunteering_flows.csv`] [ASSUMPTION: task-person shares stand for hours; national mean hours; beneficiary allocation; displacement]

The city tax proposal rests on a false premise: the adopted city-size-and-schooling earnings gain already includes induced receipts. The source's $13.927467bn on its original count is $7.967732bn of after-tax private earnings plus $5.959735bn of receipts. Recomputing the joint specification on the priced union gives $13.674355944bn = $7.824098462bn + **$5.850257483bn**. Under the consumer's headcount extrapolation, the lineage decomposition is $14.721034312bn = $8.422979655bn + **$6.298054657bn**. **Additional credit: $0 at both ends.** [CALCULATION: `social_receipts.py` → `derived/city_tax_decomposition.csv`; producer `scale_spillovers_2026_09_23/arms.py:235–252`, `:431–443`; consumer `sept24_propagation_2026_09_24/real_costs_totals.py:360–369`]

### Measured receipt and supply

| Survey year | Pantry recipient households, national | Free-meal recipient households, national | Union share of pantry recipients | Union share of free-meal recipients | Union share receiving either |
|---|---:|---:|---:|---:|---:|
| 2023 | 9.315M | 2.962M | 15.21% (SE 1.00pp) | 9.89% (SE 1.24pp) | 14.17% (SE 0.89pp) |
| 2024 | 9.616M | 3.284M | 14.86% (SE 1.05pp) | 13.58% (SE 1.75pp) | 14.43% (SE 1.04pp) |

[DATA: December 2023/2024 CPS Food Security public-use files, `HESC3`, `HESC4`, `HRSUPINT`, `HHSUPWGT`, origin and parental birthplace fields; `derived/food_receipt.csv`]

These are positive reported household uses, not food-insecurity estimates. Each household enters once. Mixed households split a household service by member-person fraction; this is an allocation assumption, not a measured household-specific quantity of food or labour. `any_member_recipient_hh` and member persons in recipient households are retained beside that allocation. Unknown/refused responses are reported separately (2024: 1.017M weighted households for pantry, 1.162M for meals); screened-out households are not recoded as observed no-use responses. The union includes Mexico birth, either parent's Mexico birth, or Mexican self-origin. It is identifiable in these monthly files; the added lineage people are not. [DATA: `derived/food_receipt.csv`] [ASSUMPTION: fractional-household beneficiary allocation]

The 2023 volunteering file yields 75.763M formal volunteers (28.330% of people aged 16+) and 70.667M outside the identified union. The union's own measured rate is 17.195% (SE 0.831pp), beside the inherited Hispanic-rate proxy of 16.9%; this exercise does not change that outgoing proxy. All household and person CSV weights retain four implied decimals. Full weights match replicate zero exactly; 160 successive-difference replicates give SE = sqrt(4/160 × sum of squared deviations). [DATA: `derived/volunteering_supply.csv`; Census codebooks in `inputs/pins.json`]

The **2023 CEV has no organization-type item**: its `PES16F` is in-person versus online volunteering. We therefore parse organization types from the detailed September **2015** supplement, `PTS4M1`; its `PES85` records any food collection/preparation/distribution/service, and `PES8A` the main activity. Outside-union volunteers reporting food as their main activity (including food as their sole activity) are 11.437%; those reporting any food activity are 24.581%. Both shares are volunteer-person shares; neither is an observed food-hour share. The organization table includes religious, school, social/community and other types separately, with unknown types retained. Food service includes school events and fundraising, so it does not match emergency food aid exactly. Transporting this composition into 2023 is an explicit sensitivity. [SOURCE: https://www2.census.gov/programs-surveys/cps/techdocs/cpssept15.pdf] [DATA: `derived/volunteering_organization_types.csv`]

### Dollar scenarios and comparator

The unchanged lane unit is $33.507014/hour, read from `build_tables.py`'s existing valuation constants ($167.2bn / 4.99bn hours); its 65.918098 hours per volunteer is also inherited. Incoming proxy = outside-union formal volunteers × national mean hours × unit value × 2015 food-task person share × 2024 recipient share, standardized to the 39.712493M priced union. That last standardization scales the union fractional-household count per member to the case population while holding observed outside receipt fixed, giving a 13.9358% share (conditional SE 1.011pp). No food/commodity value is added. [CALCULATION: `social_receipts.py` → `derived/volunteering_flows.csv`] [ASSUMPTION: equal service per recipient household, transported composition and hours]

| 2024, $bn/year; positive = presence raises others' cost | Identified union | Lineage extrapolation |
|---|---:|---:|
| Gross formal production by group, before beneficiary allocation | 10.8741 | 11.5505 |
| Gross outgoing labour reaching outsiders, inherited central | 5.9808 | 6.3528 |
| Gross incoming proxy, primary-food task / any-food task | 2.4877 / 5.3468 | 2.6781 / 5.7560 |
| Net cost with displacement 0, either proxy | −5.9808 | −6.3528 |
| Net cost with displacement 0.5, primary / any | −4.7369 / −3.3074 | −5.0137 / −3.4748 |
| Net cost with displacement 1, primary / any | −3.4930 / −0.6340 | −3.6746 / −0.5967 |

Gross receipt is not the removal effect. The displacement parameter is the share of outside volunteers' labour serving members that would otherwise benefit other residents: 0 if it is dedicated or disappears, 1 if fully redirected; 0.5 is a scenario midpoint. **Neither survey identifies it.** They also do not identify the food-labour fraction, donated service quality, matching from donor origin to beneficiary origin, capacity constraints, or charity beyond food. Consequently the table cannot establish that incoming labour is zero, that total net volunteering is a benefit, or that the broad proxy is an upper bound on all received services. It supports no newly measured central. [INFERENCE] [GAP]

For lineage, outgoing uses the case's adults multiplier (+6.2198%); incoming uses its headcount multiplier (+7.6543%). The latter holds measured outside-union volunteering supply fixed and assumes the unseen added people receive food services at the identified union's rate. These are key extrapolations, not observations of the added people. The gross-out reference predates the separate P7 lineage-boundary correction being made in the consumer: **use the delta columns on a consumer with that correction**, not the pre-P7 net level. The reverse row's `low_end_delta_bn` and `high_end_delta_bn` equal displacement × gross incoming; they are identical on both personal endpoints and on set/cash readings of the fiscal-plus-social account. The fiscal main case itself changes by zero. [ASSUMPTION] [DATA: `sept24_propagation_2026_09_24/derived/oct14/band_variants.json`, `lineage_social_keys`; `derived/social_integration.json`]

### City-tax overlap, integration and gates

City receipts use the case's marginal labour rates: 0.384 for high school or less, 0.426 for some college or more, applied separately to each skill cell's earnings change. The source computes private earnings as gross earnings less these receipts. The consumer reads gross `gain_bn`, so the tax credit is already present. The production module's receipts are `tau × result.labor_gain` from its two-skill CES equilibrium, with its capital term at zero under retention 1; it does not compute the separate CRY city productivity change. The city specification subtracts its modelled CES composition gradient before estimating the remaining schooling effect, but that is a modelling overlap treatment, not proof that every empirical channel is disjoint. Adding the city taxes to either gross city gain or production receipts again is unjustified. [DATA: `matched_benefits_2026_09_19/model.py:79–107`, `builder.py:132`; `assumption_explorer_2026_09_21/engine.js:221–229`; `scale_spillovers_2026_09_23/arms.py:447–465`]

Producer integration files:

- `derived/volunteering_flows.csv`: keys `year=2024`, `frame=identified_union_row4|lineage_key_extrapolation`, `food_task_proxy=primary_food|any_food`, `displacement=0|0.5|1`. Gross out, gross in, displaced in, net cost and both endpoint deltas are numeric. Do not reapply population factors.
- `derived/social_items.csv`: existing item columns plus frame, comparator, beneficiary, valuation and overlap. `formal_volunteering_reverse_food_proxy` is a conditional add-on; `formal_volunteering_net_food_proxy` is the alternative pre-P7 net reference. Never add both.
- `derived/city_tax_decomposition.csv`: receipts and private/gross earnings by published union, priced union and lineage. Incremental tax delta is zero.
- `derived/social_integration.json`: declarations, source hashes, population keys, conditional delta route and unresolved identification gaps.

The gates verify primary source hashes; unweighted pantry/meal/interview tallies in both food-security codebooks; 2015 food/interview/volunteer tallies; unique field layouts; one household record and one-to-one replicate joins; full-weight/replicate-zero equality; proper weight units; recipient-weight conservation to 1e-6bn; national volunteering-rate positive control; donor-count conservation; organization-count closure; original outgoing central and adopted rounding; case endpoint keys; the city source's earnings and receipts positive controls; adopted row4 city earnings at 1e-9bn; and private-plus-receipt closure at 1e-12bn. SEs are supplied for measured receipt shares and 2023 supply, plus a receipt-share-only conditional dollar SE. No joint SE is asserted across surveys or for transported 2015 task composition, displacement or the added population. [CALCULATION: `derived/social_gates.json`]

Reproduce from repo root (acquisition uses the network only for missing files and fails closed on changed pins):

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/benefits_inventory_2026_09_28/acquire_social.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with statsmodels python3 infra/immigration-fiscal/benefits_inventory_2026_09_28/social_receipts.py
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/benefits_inventory_2026_09_28 \
  "uv run --no-project python3 {lane}/price_capital_surplus.py" \
  "uv run --no-project python3 {lane}/build_tables.py" \
  "uv run --no-project python3 {lane}/acquire_social.py" \
  "uv run --no-project --with statsmodels python3 {lane}/social_receipts.py"
```

Files covered: this inventory producer; primary 2023/2024 food and 2023 CEV microdata/replicates and codebooks; 2015 volunteering microdata/codebook; scale producer and adopted population re-evaluation; v7 personal endpoint and lineage keys; consumer gross-income row; production receipt partition. Files skipped: other social/environment producers and fiscal case edits, owned by peers. No external publication or git mutation performed.

P7 log:

- 2026-10-14 21:57 JST — Acquired primary CPS food microdata, weights and docs; existing CEV local files copied with source pins. Acquisition 51.09 seconds.
- 2026-10-14 22:05 JST — Parsed receipts and 2015 organization/activity fields; rejected 2023 organization-type premise from its actual questionnaire.
- 2026-10-14 22:07 JST — First complete run: 80 gates, 10.15 seconds, peak RSS 911.8MB measured by Python `resource.getrusage`; timing by `time.perf_counter`. Added exact inherited controlled-rounding gate afterwards. Final rerun receipt below.
- 2026-10-14 22:11 JST — Complete check: **81 gates PASS**, 7.33 seconds, peak RSS 922.2MB; both Python scripts compile. Full original-plus-P7 lane rerun: **IDENTICAL: 19/19, exit 0**, all four commands exit 0, no `--allow-unrun`. Existing `items.csv`, inventory and capital outputs remain byte-identical. No git writes.
