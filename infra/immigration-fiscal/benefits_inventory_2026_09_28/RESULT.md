**Verdict:** The account already carries the large benefit channels: every direct tax, the long-run production term with its induced taxes, care, elder care and housing, and an implicit credit worth about $271bn a year, because defense and existing interest are never charged to the group. The capital owners' gain (the "immigration surplus") is in the code, but only in its long-run form, where it is exactly zero. The short-run version, with capital fixed, would add $13.8–26.1bn a year (central $20.4bn, −$499 per member on the cost convention). That rests on a frame the case rejects for public capital, and it turns into a net loss to US residents once more than 5.7% of the capital income goes to owners abroad (foreigners hold about 40% of US corporate equity). Among the new candidates, only formal volunteering (a gain of about $6.2bn, speculative) and the corporate tax on foreign-owned capital serving the group's jobs ($0–21bn, retention unmeasured) have any size. Military service, giving, culture and fertility add nothing measurable. Recommendation: add nothing new to the headline, and keep the three priced items beside it as arms. [FRAMING-SENSITIVE]
claude-opus-5-5

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
