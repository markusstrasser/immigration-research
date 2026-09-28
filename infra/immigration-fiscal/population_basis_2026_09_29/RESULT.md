**Verdict:** On the adopted account's own count, audit row 4's 39,712,493 people, the September 27 fiscal-plus-social pairing is **$414.03–488.34bn a year** and **$10,426–12,297 per member**. The record prints $416.19–490.74bn and $10,177–11,999, which divides by the published CPS union of 40,896,574. The fiscal case was already on the row-4 count. Of the 15 social rows, 13 were built on the published union; trade uses it only for the beneficiaries' share, and restaurant variety does not use it at all. Restated on the row-4 count, the social rows fall $2.16bn at the low end and $2.40bn at the high end. Most of the fall comes from PM2.5 (−$1.59bn), victims' harm (−$0.44 / −0.46bn) and congestion (−$0.39 / −0.40bn). Per-member figures rise 2.4–2.5%, less than the 3.0% that changing the denominator alone would give ($10,480–12,357). A second restatement also puts the NHTS traffic ratios on persons aged 5+ in the crash and congestion rows, as the roads lane flagged: **$413.74–488.05bn** and **$10,419–12,290 per member**. The crash row falls $0.31bn and congestion rises $0.03 / 0.02bn. Ladder 263's white replacement put 40,896,574 people on both sides. With both sides on 39,712,493 it is **$317–325bn** against US third-plus whites, against $315–330bn published, and **$402–407bn** against local whites, against $406–412bn. These changes are not proportional to the count, because the white lane already charged per-head, medical and justice lines at the engine's corrected shares. California's per-member figure moves from $14.1k to $14.3k, although the decomposition lane expected it to stay unchanged. In the generation table, the first generation's per-member figure rises 10.7%. The other lanes' per-member lines become $718 (victims), $344 (scale), $1,715 (PM2.5) and $7 (disease). The within-household figures (ladder 268) need their lane rerun on row-4 weights. [CALCULATION: `restate.py` → `derived/restated_pairing.csv`; `white_count.py` → `derived/white_count.csv`] [FRAMING-SENSITIVE: the choice of per-member denominator]

claude-opus-5-5

# Population basis of the fiscal-plus-social pairing

Task: find which population each row of the September 27 pairing was computed on, then restate the pairing and
its per-member figures on the account's 39,712,493-person basis (audit row 4). The lead later added four things:
- start the record's per-member figures from the decomposition lane's list and classify the lines it left to other
  lanes' counts;
- restate the generation table;
- price ladder 263's white replacement on the same count;
- restate the two traffic rows with the NHTS ratios on persons aged 5+, as a second restatement.

## The pairing on one population

| | Low end | High end |
|---|---|---|
| Published pairing (fiscal on 39.71M, social rows on 40.90M) | $416.19bn | $490.74bn |
| Every row on 39.71M | **$414.03bn** | **$488.34bn** |
| Change | −$2.16bn (−0.52%) | −$2.40bn (−0.49%) |
| Per member: published total ÷ 40,896,574 (the record) | $10,177 | $11,999 |
| Per member: published total ÷ 39,712,493 (denominator only) | $10,480 | $12,357 |
| Per member: restated total ÷ 39,712,493 | **$10,426** | **$12,297** |
| Second restatement: every row on 39.71M, traffic rows on persons aged 5+ | **$413.74bn** | **$488.05bn** |
| Per member: that total ÷ 39,712,493 | **$10,419** | **$12,290** |

[CALCULATION: `restate.py` → `derived/restated_pairing.csv`, sections `pairing`, `per_member`, `pairing_5plus` and
`per_member_5plus`]

The low end uses the Hispanic footing with decision 4's mixed-group victims; the high end uses the custody footing
(`sept24_propagation_2026_09_24/real_costs_totals.py:433`). The rows add to both published ends within the gate's 2e-6bn.
The decomposition lane's "$10.5k / 12.4k if every row were on the account's count"
(`main_case_decomposition_2026_09_29/RESULT.md`, headcount table) divides the published total by 39.71M. With the
social rows restated as well, the figure is $54 / $60 lower.

The social rows total $98.71bn / $103.37bn as published and $96.55bn / $100.97bn restated. Scaling every social row
by the plain headcount ratio 0.971048 would give $413.33–487.74bn ($10,408–12,282 per member). That is $0.6–0.7bn
too low, because most rows read a share or a subgroup count that moves less than the union does.
[CALCULATION: restated_pairing.csv]

## Which population each row was computed on

Figures are $bn a year, low end / high end, or one figure where the row enters both ends at its central value.
`basis.csv` gives the file and line where the population enters, and the method, for each row.

| Row | Published | Population it was computed on | Scales with headcount | Factor | Restated | Move |
|---|---|---|---|---|---|---|
| Fiscal case | 317.48 / 387.37 | 39.71M, row 4 (the case's stack) | already on the row-4 count | 1 | 317.48 / 387.37 | 0 |
| Victims' harm | 30.93 / 32.34 | 40.90M: union aged 12+ as a share of CPS Hispanics aged 12+ (s), applied to NCVS Hispanic-offender incidents | linear in s | 0.98563 | 30.48 / 31.87 | −0.44 / −0.46 |
| Property crime | 1.27 / 1.38 | the same s | linear in s | 0.98563 | 1.25 / 1.36 | −0.02 / −0.02 |
| Unreimbursed hospital care | 3.24 / 5.56 | 40.90M: the union's share of CPS uninsured person-years | linear | 0.95222 | 3.09 / 5.29 | −0.15 / −0.27 |
| Congestion | 13.99 / 12.02 | 40.90M: the ACS group (39.43M) scaled up to it in UMR urban areas | not linear; the lane cut stays at the corrected account's key share | 0.97210 / 0.96667 | 13.60 / 11.62 | −0.39 / −0.40 |
| Housing gain (subtracted) | −3.51 / −0.71 | 40.90M: the ACS group scaled up to it by CBSA (low end); 40.90M ÷ 340.11M everywhere (high end) | not linear | 0.96714 / 0.97096 | −3.39 / −0.69 | +0.12 / +0.02 |
| Fear and avoidance | 10.49 | the victim lane's s | linear in s | 0.98563 | 10.34 | −0.15 |
| Private security | −0.60 | offending shares (through s) less the population share 40.90M ÷ 336.73M | a difference of two shares | 0.81773 | −0.49 | +0.11 |
| School disruption | −1.95 | 8.487M pupils on the published weights; outsider exposure from ACS tracts | weakly, through pupils | 0.99419 | −1.94 | +0.01 |
| PM2.5 from consumption | 69.68 | 40.90M ÷ 336.73M CPS civilian frame | near-linear | 0.97720 | 68.09 | −1.59 |
| Road-crash externality | 11.05 | 40.90M ÷ 336.73M; q from the congestion lane's 40.90M exposures | near-linear | 0.98399 | 10.87 | −0.18 |
| Scale, net earnings (gain) | −13.93 | 40.90M: the ACS group scaled up to it, 1990 commuting zones | not linear | 0.98183 | −13.67 | +0.25 |
| Restaurant variety (gain) | −6.79 | none: an assumed share, ψ = 0.05 | no | 1 | −6.79 | 0 |
| Formal volunteering (gain) | −6.21 | 40.90M: union aged 16+ (30.25M) | linear | 0.96301 | −5.98 | +0.23 |
| Consumer-side scale (gain) | −2.19 | 40.90M: spending per person × count; CBSA shares from the scale lane | mostly linear | 0.97384 | −2.13 | +0.06 |
| Trade, travel and FDI (gain) | −6.77 | none: a literature elasticity applied to measured flows; the beneficiaries' share comes from the CPS consumption key | inversely, through the beneficiaries' share | 1.00230 | −6.78 | −0.02 |

[DATA: `derived/frame_counts.csv`; CALCULATION: `derived/reeval.csv`, `basis.csv`, `derived/restated_pairing.csv`]

Where the population enters (the full list is in `basis.csv`):
- Victims, property and fear: `crime_victim_cost_2026_09_23/victim_cost.py:432` (s), `:324,332,368` (incidents × s),
  `:571,652`; `social_costs_unpriced_2026_09_28/items.py:51,81`.
- Unreimbursed care: `uncompensated_care_2026_09_23/uncompensated.py:62,68,130,141`.
- Congestion and housing: `congestion_2026_09_23/arms.py:59,471`; `service_response_long_run_2026_09_27/congestion.py:63,139,145`;
  `housing_transfer_2026_09_23/arms.py:61,154-155,200`.
- PM2.5: `air_pollution_2026_09_28/air_items.py:29,31,107`.
- Crash: `road_crash_externality_2026_09_28/crash_model.py:91-92,109,160`.
- Scale: `scale_spillovers_2026_09_23/arms.py:45-47,121`.
- Volunteering: `benefits_inventory_2026_09_28/build_tables.py:18-19,112`.
- Consumer scale: `consumer_scale_2026_09_28/price_items.py:90,117,185`.
- Rows with no headcount: `disease_food_2026_09_28/price_items.py:163` (restaurant ψ);
  `trade_networks_2026_09_28/price_trade_networks.py:60,147` (trade).

The fiscal case needs no factor, because its stack applies row 4 (`band_variants.cjs:162`). Two things link it to
40.90M:
- The per-member division comes from downstream code. `band_variants.cjs:232` writes the uncorrected model's
  `target_population`, and `real_costs_totals.py:292,355` divides by it.
- The low end adds the justice raw-coding shift of −$4.339bn. It is identical on the uncorrected and corrected
  models by gate (`band_variants.cjs:214`).

## Why the factors differ from 0.9710

Row 4 removes 1,184,081 people, all Mexico-born naturalized citizens and noncitizens living outside California and
Texas. Of them, 98.8% are Hispanic and 93.6% are adults, and together they carry 530,435 uninsured person-years
(6.3% of the union's) [DATA: `derived/frame_counts.csv`]. Each row therefore moves with the count it actually reads:
- **The union's 12+ share of CPS Hispanics falls 1.44%, not 2.9%** (victims, property, fear). The same people leave
  the Hispanic denominator too: s goes from 0.59752 to 0.58894.
- **Its share of the civilian frame falls 2.55%** (PM2.5, crash, the population share in private security). The
  frame loses these people too. The result, 0.118353, is the account's own per-head share.
- **Its share of uninsured person-years falls 4.78%** (unreimbursed care).
- **Its 16+ count falls 3.70%** (volunteering), and its pupils about 0.7% (school disruption).

Where a lane's function is not linear in the count, the item moves by a different amount than the count does, so
each of these was re-evaluated:
- PM2.5 falls 2.3%, not 2.55%: a smaller group breathes less of its own pollution.
- Congestion falls less where the free-flow cap binds.
- The scale gain falls 1.8%: its size gain and its schooling-composition loss both shrink.
- The crash item falls 1.6%: q, the chance the other party is a group member, falls from 0.2988 to 0.2896, which
  raises the outsider share of each crash.
- Private security is a small difference of two shares, so it shrinks by 18%.

[CALCULATION: `derived/reeval.csv` method column]

## Rows not restated exactly, and what a rerun would need

Every row is restated here, and all but three exactly:
- **Trade, travel and FDI** (−$6.77bn → −6.78bn) is first order. The lane's beneficiaries' share uses the
  consumption lane's saving-corrected key share, 0.0889. I moved it by the raw key's row-4 change of −2.36%. An
  exact figure needs `consumption_key_2026_09_24` on row-4 weights; it would move the row by about ±$0.02bn.
- **School disruption** (−$1.95bn → −1.94bn) uses the lane's 8.487M pupils, which are a published-weight count
  (`school_cost_where_enrolled_2026_09_24/account_pupils.py:51,54`). I moved them with the union aged 5–17 (−0.7%).
  An exact figure needs that lane on row-4 weights; the effect is about ±$0.01bn.
- **The fiscal low end's raw-coding shift** (−$4.339bn) is left as it is. The stack holds the justice line's
  administrative keyed amount fixed across weight sets (decomposition RESULT.md:182). Restating the shift would
  change the fiscal case itself, which is outside this lane [INFERENCE].

The nine re-evaluated rows are restated only here: PM2.5, crash, congestion, housing, fear, security, school, scale
and consumer scale. Their lanes' `derived/` files stay on 40.90M, and so does every memo that quotes them. For each,
the lane needs a rerun with its union constant set to the row-4 count and its CPS civilian frame set to 335,543,722:
- `TARGET` in the congestion and housing lanes;
- `SCALE` in the scale lane;
- `n` and `POP_ALL` in the air lane;
- the `cps()` counts in the crash lane.

The victim lane (s) and the uncompensated-care lane (the uninsured share) need a rerun on row-4 weights as well,
though a factor restates them exactly. So does `crime_victim_cost_2026_09_23/derived/target_population_cps2025.csv`,
which six lanes read. Three more lanes copy its counts as constants, and a rerun must update those by hand:
`air_items.py:29,31`, `social_costs_unpriced_2026_09_28/items.py:34,37` and `price_trade_networks.py:47-52`.

## Second restatement: the traffic rows on persons aged 5+

The roads lane found that the NHTS ratio of the group's driving to others' is per person aged 5+, while the crash
lane applies it per resident (`roads_mileage_key_2026_09_29/RESULT.md:110`). On row-4 weights, 7.97% of the union is
under 5, against 5.18% of other residents [DATA: `main_case_decomposition_2026_09_29/derived/age_bins.csv`, equal to
the roads lane's `keys.csv`]. A per-resident ratio therefore overstates the group's share of driving. The second
restatement changes only the crash and congestion rows. Every other row is as in the first.

| | Row 4 alone | Row 4, traffic rows on persons 5+ | Move |
|---|---|---|---|
| Road-crash externality | 10.87 | 10.56 | −0.31 |
| Congestion, low end / high end | 13.60 / 11.62 | 13.63 / 11.64 | +0.03 / +0.02 |
| Pairing, $bn | 414.03 / 488.34 | **413.74 / 488.05** | −0.28 / −0.29 |
| Per member | $10,426 / $12,297 | **$10,419 / $12,290** | −$7 / −$7 |

[CALCULATION: `reeval.py` → `derived/reeval.csv` records `*_5plus`; `restate.py` → sections `row_5plus`,
`pairing_5plus`, `per_member_5plus`]

- **Crash.** The lane's traffic share is s = Pr / (Pr + 1 − P), with P the union's share of residents
  (`crash_model.py:160`). The arm sets P to the union's share of persons aged 5+,
  p(1 − u_g) / [p(1 − u_g) + (1 − p)(1 − u_o)], which goes from 0.118353 to 0.115272. At the lane's central ratio
  r = 0.874, s falls from 0.1050 to 0.1022, and the item falls 2.9%. q, the chance that the other party is a group
  member, comes from ACS commute minutes and stays at 0.2896. The group's miles relative to the average resident
  also change, but they enter only the normalized and fault-based figures (`crash_model.py:161,268,270`), which the
  pairing does not use.
- **Congestion.** The lead's formula does not carry over to this row. Its central share is the group's share of
  each urban area's population (`service_response_long_run_2026_09_27/congestion.py:146`, `e.s`), because the
  elasticity is one of travel time to city population. People of every age count in that share, so it stays
  [INFERENCE]. The NHTS ratios enter only the vehicle-hour terms: others' vehicle-occupant hours and the delay share
  that caps the fall (`congestion_2026_09_23/arms.py:356-364`). There the lane already counts only persons aged 5+,
  but with one national under-5 share, 5.40%, for both groups (`arms.py:80`). The arm gives each group its own. Others'
  hours rise 0.23% and the group's fall 2.7%, so others lose slightly more time to the group, and the item rises
  $0.03bn / $0.02bn.
- **Gates.**
  - At u_g = u_o = 0 the crash arm reproduces its row-4 figure (1e-12).
  - The congestion row's row-4 figures sit at u_g = u_o = 5.40%, the lane's own share, and the arm reproduces
    them there (1e-9). At zero the arm would drop the lane's existing correction, so zero is not its identity point.
  - u_g and u_o equal the roads lane's `keys.csv` (1e-6).
  - Each 5+ record starts from the pairing's value. Congestion matches to 1e-6bn. The crash row matches to 2 dp,
    because `real_costs_totals.csv` carries the lane's `items.csv` value as printed (11.05, against 11.053646).
- **The roads lane's 10.12%.** Its flag gives s = 10.12%, and this arm gives 10.22%. The difference is p. The roads
  lane uses the account's per-head cell, 0.117175 = 0.118353 × 0.990053. The household fraction 0.990053 puts the
  residents outside the CPS frame into the base, so the cell is the union's share of all residents, 338.9M on row 4
  (`main_case_decomposition_2026_09_29/RESULT.md:330-336`). The crash lane's P is the union's share
  of the CPS civilian frame, 0.118353 on row 4, and the arm keeps it. Given the roads lane's p and ratio, the arm's
  formula reproduces its 0.101232 (gate). On that p the crash item would be $0.12bn lower, $10.45bn
  [CALCULATION: `reeval.csv` record `road_crash_externality_5plus_account_p`, a sensitivity outside the pairing].
  I keep the crash lane's frame, because the NHTS samples households and most residents outside the CPS frame live
  in institutions [INFERENCE].

## The white replacement (ladder 263) on the account's count

**The white lane used 40,896,574 on both sides.** It scales every white slice to the engine meta's
`target_population`, 40,896,574. That count reaches `rekey_white.py:159,214` through
`white_replacement_2026_09_28/engine_lines.cjs:22`. The union side of each like-for-like delta is the lane's rough
re-key on the published CPS weights, 40,896,575 people. The state version scales each region's white piece to that
region's union on the same weights (`state_white.py:141,148-149`): California 13.08M, Texas 9.76M and the rest of
the US 18.05M.

Two kinds of line were already on the account's count, on both sides:
- Per-head lines charge a 40.90M group 0.117175 of each line. That is the engine's corrected per-head share, the
  share of 39.71M people (`rekey_white.py:202`, `pc_scale`).
- The union's medical and justice lines use the engine's corrected shares (`rekey_white.py:347`).

Only taxes, transfers, schools and the white slice's medical and justice keys were on 40.90M.

**Rerun with both sides on 39,712,493.** `white_count.py` imports the lane's modules read-only and uses audit row
4's weights, the engine's own factors from `combine_onbooks_lane.weight_arms`. It scales the whites to 39,712,493
and recomputes the frame totals the keys divide by. `white_accrual.py` recomputes the union's accrual per tax
dollar with the pension lane on row-4 weights: payable OASDI moves from 1.018378 to 1.020077, and Part A per HI
dollar from 1.460946 to 1.467447. The white group's ratios do not move.

| $bn a year, low / high | Published (both sides 40.90M) | Both sides 39.71M | × 0.971 (proportional) | Per member, published → restated |
|---|---|---|---|---|
| Against US third-plus whites, accrual (A1) | 317.6 / 315.1 | **318.9 / 316.6** | 308.4 / 305.9 | $7,766 / 7,704 → $8,031 / 7,973 |
| Against US third-plus whites, cash at the union's ages (A3) | 330.2 / 326.3 | **325.4 / 322.0** | 320.6 / 316.9 | $8,074 / 7,979 → $8,193 / 8,108 |
| The headline range | $315–330bn | **$317–325bn** | $306–321bn | |
| Raw cash at white ages (A1) | 157.2 / 154.6 | 164.5 / 162.1 | 152.6 / 150.1 | $3,843 / 3,781 → $4,141 / 4,083 |
| Against local whites state by state, sum | 412.3 / 406.2 | **407.5 / 401.9** | 400.3 / 394.4 | $10,081 / 9,931 → $10,261 / 10,119 |
| California | 184.9 / 181.9 | 186.9 / 184.0 | | $14,133 / 13,907 → $14,286 / 14,064 |
| Texas | 83.6 / 82.4 | 85.1 / 83.9 | | $8,567 / 8,440 → $8,720 / 8,597 |
| Rest of US | 143.8 / 141.8 | 135.5 / 134.0 | | $7,963 / 7,856 → $8,031 / 7,941 |
| Los Angeles metro (inside California) | 84.7 / 83.0 | 85.5 / 83.8 | | $18,816 / 18,441 → $18,977 / 18,605 |
| A1 against the engine's own union ($321.8 / 387.4bn) | 168.2 / 183.0 | 169.3 / 184.8 | | |

[CALCULATION: `white_count.py` → `derived/white_count.csv`; `white_accrual.py` → `derived/white_accrual_ratios.csv`]

**Why the change is not proportional.** The union's rough cost rises, from $310.8bn to $317.0bn at the low end. Its
income, payroll and sales taxes fall $11.9bn. Its charges for transfers, pensions, schools, capital and
earnings-keyed lines fall $5.6bn. The union's per-head, medical and justice charges do not change, because they already sit
on the account's count. The white slice at the union's ages (A3) shrinks 2.9%, and its taxes and its medical and justice
charges fall with it. So the A3 delta changes as follows:
- it falls $14.1bn on taxes and $0.4bn on welfare;
- it rises $6.3bn on Medicaid, Medicare, justice and veterans' lines;
- it rises $3.4bn on pensions, per-head lines, schools and capital.

The net is −$4.8bn, about half the proportional −$9.6bn. [CALCULATION: bucket moves from the lane's `run()` on both weight sets]

**California moves even though row 4 leaves its people alone.** Its delta rises $2.0bn, or 1.1% per member.
- $1.9bn of the rise is on Medicaid, Medicare and justice. The union's engine-share amounts for those lines are
  already on 39.71M. Split over a union without the removed people, they give California more: its share of the
  union's persons goes from 32.0% to 32.9%.
- The shrinking frame totals add $0.3bn.
- The production gain takes $0.2bn back.

The decomposition lane classed "a California figure" as unaffected; for this figure that is wrong. The rest of the
US, where every removed person lived, falls $8.3bn. [CALCULATION: California's union and white pieces by bucket on
both weight sets, from the lane's `priced()`]

Map text if the figures are adopted (the map holds "Against 40.9M whites"): "Against 39.7M whites, the group costs
others about $320bn a year more (317–325). Against local whites state by state, about $405bn (402–407)." On raw cash
the gap becomes $163bn (162–164). The comparators claim becomes "about $320–405bn". The headline figures are
midpoints: $321bn and $405bn.

## The record's per-member figures

The decomposition lane's list (`main_case_decomposition_2026_09_29/RESULT.md`, "How many record figures it
touches") is the starting point: 32 lines in `research/` and `decisions/`. It covers 19 of them with its rule,
×1.0298 on the engine part, and leaves five to other lanes' counts. Those five, the generation table and the lines the brief
named in the living documents are restated here. `restate.py` finds each line by its text and gates that the value it
computes renders as the record prints it. No text was missing (0 `[DEGRADED]`). Line numbers are from the 03:10 JST
run. Peers are editing these files, and each run of `restate.py` records the lines as it finds them.

**Living documents:**

| Where | Current | Restated | Basis |
|---|---|---|---|
| `research/immigration-INDEX.md:226`, latest pairing (ladder 266) | $10.2–12.0k | **$10.4–12.3k** | every row on 39.71M |
| INDEX:226, superseded ladder 265 ($447–522bn) | $10.9–12.8k | $11.3–13.1k | denominator only |
| INDEX:226, superseded ladder 264 ($463–537bn) | $11.3–13.1k | $11.7–13.5k | denominator only |
| INDEX:226, superseded fear, security and schools ($371–446bn) | $9.1–10.9k | $9.3–11.2k | denominator only |
| INDEX:228, superseded September 27 case ($363–438bn) | $8.9–10.7k | $9.1–11.0k | denominator only |
| INDEX:219 and `overview_2026_09_28/groups.py:470`, Black comparator | 1.5–1.7× per member | **1.5–1.6×** (1.454–1.615) | the case per member on 39.71M; the Black figure keeps its own 41.95M |
| INDEX:150, against US whites | $315–330bn | **$317–325bn** | both sides on 39.71M |
| INDEX:150, raw cash at white ages | $155–157bn | $162–164bn | both sides on 39.71M |
| INDEX:150, against local whites | $406–412bn | **$402–407bn** | both sides on 39.71M |
| INDEX:150, California per member | $14.1k | **$14.3k** | both sides on 39.71M |
| groups.py:456 claim; :457 range; :463 finding | $320–410bn; $320bn (315–330), $409bn (406–412); "40.9M whites" | $320–405bn; $321bn (317–325), $405bn (402–407); "39.7M whites" | both sides on 39.71M |
| groups.py:465, raw cash | $156bn | $163bn | both sides on 39.71M |
| INDEX:81 and FAQ:546, 10–20% less per member | 10–20% | unchanged | a ratio across years |

The decomposition gives the Black comparator as 1.46–1.62×, probably because it divides the rounded $13.1k /
$14.2k [INFERENCE]. From unrounded figures it is 1.454–1.615×, and both print as 1.5–1.6×. The superseded pairings are restated by the
denominator alone. Restating their social rows would probably lower them by about another 0.5%, as it lowers the
latest pairing [INFERENCE].

**The five lines left to other lanes' counts:**

| Line | Figure | Built on | Restated per member |
|---|---|---|---|
| `research/immigration-real-fiscal-and-social-costs-2026-09-23.md:237`, victims' harm | $707 per group member ($28.92bn) | 40.90M, through s (the victim lane's central) | **$718** (× 0.985635, ÷ 39.71M) |
| `research/immigration-confidence-ladder.md:333` (entry 201), scale net | $341 per member ($13.9bn) | 40.90M, the ACS group scaled up to it | **$344** (lane re-evaluated) |
| ladder:438 (entry 260), PM2.5 | $1,704 per member ($69.7bn) | 40.90M ÷ 336.73M | **$1,715** (lane re-evaluated) |
| ladder:439 (entry 261), disease and food safety | $7 per member ($0.30bn) | no headcount: CDC case counts and ACS kitchen shares; the share of US-born cases uses G2 and G3+, which row 4 leaves | $7 ($7.25 → $7.47; only the denominator moves) |
| ladder:446 (entry 268), within households | −$1,446 / +$1,093 (BA+ heads); median $8,716 / $10,139; childless about $4,400 | the row-4 totals spread over the published weights (`within_group_distribution_2026_09_29/households.py:116-118`; its RESULT.md:115 counts 40.90M members) | not restated |

The within-household lane gives each Mexico-born member outside CA and TX a share that is too small, and its union
mean per member runs 2.9% low. Its shares of net-contributor households and its medians need the lane rerun on row-4
weights, with the key-total gates re-pinned to that frame.

**The generation table** (`research/immigration-adopted-account-by-generation-2026-09-25.md:104-113`, the September
24 case). The factors come from the decomposition's `derived/headcount.csv`. First-generation adults come from this
lane's `frame_counts.csv`: row 4 removes 1.108M of the 11.67M.

| Row | Current, low / high | Restated | Factor |
|---|---|---|---|
| (a) G1 per member | $5,220 / 4,383 | **$5,780 / 4,853** | 1.107286 |
| (a) G2, G3+ per member | $5,703 / 6,636; $3,859 / 6,808 | unchanged | 1 |
| (a) All three per member | $4,912 / 6,023 | $5,058 / 6,203 | 1.029816 |
| (b) G1 per adult | $9,441 / 11,543 | **$10,431 / 12,754** | 1.104885 |
| (b) G2, G3+ per adult | $5,629 / 5,941; $4,945 / 7,160 | unchanged | 1 |

The decomposition already restated the current split (`generation_results.csv`, ladder 224, the September 27 case):
(a) $7,673 / 6,408 → $8,496 / 7,096; (b) $9,434 / 11,320 → $10,146 / 12,174.

By the repo's rule, records get a note, not an edit: the ladder, decisions and dated memos. Living documents take
the new figures: the INDEX, the FAQ and the map.

## What would change this (disconfirmation)

- **How row 4 is implemented.** The adopted arm drops the removed weight. The alternative arm, row4_other_hispanic
  (`combine_onbooks_lane.py:450-479`), moves it to other Hispanic residents. Under that arm the crime-linked rows
  would fall 3.4% instead of 1.4%: a further −$0.85bn at the low end and −$0.88bn at the high end
  [CALCULATION: victims, property and fear × (0.965657 − 0.985635)]. The share-based rows would keep the 336.73M
  frame. That arm also changes the fiscal case, so it is a different basis, not a restatement on the adopted one.
- **Whether row 4 is right.** If the CPS, not the ACS, counts the Mexico-born outside CA and TX correctly, the
  fiscal case belongs on 40.90M and the published per-member figures are the consistent ones. Ladder 209 found the
  CPS 9–13% above the ACS in every year since 2019 [SOURCE: main_case_decomposition_2026_09_29/RESULT.md:251,
  citing ladder 209].
- **The two proxies above:** trade ±$0.02bn, school ±$0.01bn.
- **The 5+ arm's p.** On the roads lane's p, the union's share of all residents rather than of the CPS frame, the
  crash row and both ends of the second pairing would be $0.12bn lower.
- **Restaurant variety's assumed ψ.** Scaled with the count, the row would move ×0.9710, adding about $0.20bn.
- **The white replacement's rough keys.** The white lane's own rating says its rough keys land 3–7% below the engine
  on the union. The restatement keeps that method and changes only the count. Its A1-against-engine row
  ($169.3 / 184.8bn) is the one comparison whose union side is the engine itself.
- **The choice of denominator** [FRAMING-SENSITIVE]. The account charges its lines for 39.71M people, so the
  per-member figure that matches it divides by 39.71M. A reader who takes the CPS count as the group's size would
  keep 40.90M; then the fiscal case, not the social rows, is on the wrong basis.

## Coverage

Covered:
- All 16 rows of the pairing (the fiscal case and 15 social rows) at both ends. That is 22 records in `basis.csv`;
  each of the six rows whose value differs by end has one record per end.
- Ladder 263's figures in the INDEX, the map and the ladder: A1 on accrual and on cash, A3, the state sum and its
  four regions, both ends.
- From the decomposition's list: its five other-lane lines, the generation table, and the living-document lines
  above.
- The second restatement's two traffic rows, crash and congestion. They are the only pairing rows whose lanes apply
  an NHTS ratio. Outside them, the only lane code that names the NHTS is the roads lane, the three main-case
  candidates of September 28, the ancestry-IV commute lane, winners-losers and the map. None of these feeds the
  adopted case or a pairing row [DATA: `rg -il nhts infra/immigration-fiscal`, `.py`/`.cjs`/`.js` files].

Skipped, with reasons:
- The roads lane's re-key of the fiscal case's road lines (ladder 273). It is outside the adopted case, so the fiscal
  case keeps its keys in both restatements.
- The decomposition's 19 union lines, other than the INDEX pairings above. Its rule (×1.0298 on the engine part)
  restates them, and they are records.
- The white lane's A2, A4, all-residents slice, "both arms" figures ($289 / $287bn cash, $450 / $447bn accrual) and
  the state version's convention-arm and own-age columns. None of them is in the INDEX's or the map's range.
- The full span ($142–757bn) and its package-range variant. They stack every item's low and high arms, each with
  its own basis, and they are not part of the pairing.
- The §7b columns, the capital-at-7% and option-A variants, and the footing totals other than the pairing's two
  ends. These are variants beside the pairing.
- The items' normalized figures and the crash lane's fault-based row. They are never added to the pairing.
- The fiscal case's own basis beyond the lead's verification, taken from decomposition RESULT.md:130-134,248-256.

## Method and reproduction

Run from the repository root, in order:

```
OPENBLAS_NUM_THREADS=1 uv run --no-project --offline python3 infra/immigration-fiscal/population_basis_2026_09_29/frame_counts.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --offline --with statsmodels python3 infra/immigration-fiscal/population_basis_2026_09_29/reeval.py
uv run --no-project --offline python3 infra/immigration-fiscal/population_basis_2026_09_29/basis.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --offline python3 infra/immigration-fiscal/population_basis_2026_09_29/white_accrual.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --offline python3 infra/immigration-fiscal/population_basis_2026_09_29/white_count.py
uv run --no-project --offline python3 infra/immigration-fiscal/population_basis_2026_09_29/restate.py
```

- **`frame_counts.py`** loads the account's CPS frame and audit row 4's weights. It imports
  `generation_account_2026_09_24/frame.py` and `combine_onbooks_lane.weight_arms` read-only, then tabulates 37
  counts under both weight sets. It has 15 gates. The published counts reproduce `target_population_cps2025.csv`
  (worst difference 0.05 persons), and the row-4 union, frame and uninsured person-years reproduce the
  decomposition lane's `age_bins.csv`.
- **`reeval.py`** re-evaluates nine rows with each lane's own functions. That is 11 records, with congestion and
  housing at both ends, plus the lanes-fixed B1 congestion figure as a reference. It adds the second restatement's
  three 5+ records and one sensitivity, the crash arm on the roads lane's p. It has 29 gates. Each lane's
  published figure is reproduced first: to 1e-9 where the lane stores full precision, to `items.csv`'s printed
  rounding otherwise. The consumer-scale `main()` rerun reproduces its `items.csv` byte for byte. The 5+ arm's
  gates are listed in its section.
- **`basis.py`** writes `basis.csv`. It has 15 gates: 4 rebuild the shares the lanes used from the frame counts,
  and 11 check that each re-evaluated record is in `reeval.csv`.
- **`white_accrual.py`** imports the pension lane and `accrual_white.py` read-only (neither `main()` runs) and
  writes `derived/white_accrual_ratios.csv`. It refuses to run if the pension lane's stage cache is missing, because
  building that cache would write into the pension lane. It has 8 gates. The published weights reproduce the white
  lane's union ratios and the pension lane's stored union, and row 4 removes the same 1,184,081 people. It runs in
  about 70 seconds.
- **`white_count.py`** imports `state_white.py`, and with it `rekey_white.py`, read-only; both module-level builds
  only read. It writes `derived/white_count.csv` and has 29 gates. The published run reproduces the white lane's
  `rekey_summary.csv`, `accrual_beside.csv` and `state_summary.csv` to 1e-3bn. The recomputed frame totals equal the
  module's own on the published weights, and the row-4 union matches the account's count (39,712,494.5 against
  39,712,493.3).
- **`restate.py`** writes `derived/restated_pairing.csv`. It has 51 gates:
  - 22 check that each factor is positive;
  - 2 check that the rows add up to the published pairing;
  - 1 checks that the totals CSV's per-member divisor is the account's row-4 count;
  - 2 check that the published per-member figures reproduce;
  - 3 check that each 5+ record starts from the pairing's value;
  - 21 check that each restated record figure's published value renders as the record prints it.

The chain was rerun: frame_counts, reeval, basis and restate at 01:30, and white_accrual, white_count and restate
at 02:41. Every output compared byte-identical (`cmp`). After the under-5 arm, `scripts/rerun_lane.py` ran all six
commands above at 03:02: every exit code was 0, 23 of 23 files were identical, and no script was left unrun. A second
run at 03:07 found one change: a peer's edit to the FAQ during the run moved a reader row's line from 552 to 546.
The values were unchanged. Two further runs of `restate.py` at 03:10 were byte-identical. Nothing was written
outside this lane. Every import sets
`sys.dont_write_bytecode`, the consumer-scale `main()` ran with its `OUT` pointed at
`derived/consumer_scale_rerun/`, and no other lane's `main()` runs.

## Log

- 2026-09-29 01:01 JST — lane created; reading real_costs_totals.py and the sept27 totals.
- 2026-09-29 01:15 JST — read every row's source lane; population enters through CPS counts in 13 of 16 social rows (victims, property, fear, security, care, pm25, crash, volunteering, consumer scale, congestion, housing, scale net) and not at all in restaurant variety and trade; writing frame_counts.py for the row-4 Hispanic and age counts.
- 2026-09-29 01:20 JST — correction to the 01:15 line: the population enters through CPS counts in 14 of the 16 social rows; restaurant variety and trade use no headcount (trade only through the beneficiaries' consumption share). frame_counts.py passes 15 gates (published counts reproduce target_population_cps2025.csv; row-4 counts reproduce the decomposition lane's age_bins.csv). reeval.py passes 17 positive controls and re-evaluates pm25, congestion (both ends), crash, housing (both ends), fear, security and school on the row-4 counts.
- 2026-09-29 01:20 JST — recount (supersedes the two lines above): the pairing has 16 rows, the fiscal case and 15 social rows. 13 social rows read a CPS count; trade reads one only through the beneficiaries' consumption share; restaurant variety reads none.
- 2026-09-29 01:23 JST — reeval.py extended: scale net (CZ joint central, x0.9818) and consumer scale (the lane's main() rerun with OUT redirected here; published control byte-identical, x0.9738). 23 gates pass. Next: basis.py and restate.py.
- 2026-09-29 01:30 JST — basis.py (4 share gates) and restate.py (sum and per-member gates) pass; the chain frame_counts -> reeval -> basis -> restate reruns byte-identical (cmp on all outputs, restate.py twice). Restated pairing $414.03-488.34bn, $10.43-12.30k per member on 39.71M.
- 2026-09-29 01:33 JST — the 01:20 line's "17 positive controls" was 18 gates at that point; the final reeval.py has 23. Evidence line for the decomposition finding updated to RESULT.md:248-256 after its follow-up commit fbd0db0. RESULT written; verdict final.
- 2026-09-29 01:44 JST — verification pass on the 01:33 RESULT. Corrected: the verdict's method count (nine rows re-evaluated with the lane's own code, school on a pupil proxy; four by an exact ratio of counts; trade by a first-order proxy; the fiscal case and restaurant variety need none); the heading over the non-linear rows (private security moves more than its count, not less); the gate counts (basis.py 15, restate.py 26, confirmed by a rerun; outputs byte-identical to the 01:31 run, restate.py twice); the row4_other_hispanic line reference (combine_onbooks_lane.py:450-479); the sum-gate tolerance (2e-6bn); six lanes read target_population_cps2025.csv and three more copy its counts as constants. Added [INFERENCE] and [SOURCE] tags. Checked for writes outside the lane since 01:00: all belong to peer lanes. The one near an import of mine, generation_account_2026_09_24/__pycache__/frame.cpython-313.pyc (01:32:50), was written when the career-trajectory lane created and ran cps_check.py at 01:32:49 (its transcript); frame_counts.py sets sys.dont_write_bytecode before importing frame.py and last ran at 01:30:02.
- 2026-09-29 02:07 JST — two follow-ups from the lead: start the record's per-member figures from the decomposition lane's list (classify its five other-lane lines and the social rows; add the generation table), and price ladder 263's white replacement on the account's count. white_count.py (first run 02:07:36 by date) reruns the white lane's rough re-key and state pieces on row-4 weights with the whites at 39,712,493; 26 gates pass, the published run reproducing rekey_summary, accrual_beside and state_summary. Sent the lead $316–325bn and $402–407bn, with the union's accrual ratio held (first order).
- 2026-09-29 02:25 JST — white_accrual.py recomputes the union's accrual per tax dollar with the pension lane on both weight sets (02:25:42–02:26:53 by date; 8 gates; nothing written outside the lane): payable OASDI 1.018378 -> 1.020077, Part A per HI dollar 1.460946 -> 1.467447. white_count.py now uses them (29 gates): the accrual delta is 318.9 / 316.6, so the range is $317–325bn, not $316–325bn; correction sent to the lead.
- 2026-09-29 02:41 JST — restate.py extended to the record's other per-member figures, lines found by text (47 gates, none degraded). Determinism: white_accrual.py, white_count.py and restate.py rerun from 02:41:38, outputs byte-identical to the previous run; outside the lane only peer files changed (.claude/checkpoint.md, number_drift_audit_2026_09_29).
- 2026-09-29 02:45 JST — RESULT rewritten: verdict, the white replacement section, the record's per-member figures from the decomposition's list (five other-lane lines, generation table, living documents), coverage and method. Correction: the 01:33 reader table called INDEX's California $14.1k per member unchanged; with both sides on 39.71M it is $14.3k ($14,133 -> $14,286).
- 2026-09-29 03:10 JST — the lead's under-5 arm for the two traffic rows, as a second restatement. reeval.py (29 gates; 02:54 first run, 03:01 with the sensitivity) adds three _5plus records and road_crash_externality_5plus_account_p; restate.py (50 gates, 0 degraded) adds row_5plus, pairing_5plus and per_member_5plus. Pairing $413.74–488.05bn, $10,419–12,290 per member, against $414.03–488.34bn and $10,426–12,297 for row 4 alone. The crash gate's first tolerance (1e-6) failed on the pairing's 2 dp value (11.05 against the lane's 11.053646); it now allows the printed rounding for social items. The congestion row's identity point is the lane's own under-5 share (5.40%), not zero; the crash row's is zero. The roads lane's s = 10.12% differs from this arm's 10.22% only through p (the account's per-head cell against the crash lane's CPS frame); its keys.csv value is reproduced by gate. rerun_lane.py with all six commands: 03:02 identical 23/23; 03:07 one reader line moved by a peer's FAQ edit (552 -> 546), values unchanged; restate.py twice at 03:10 byte-identical. Reader line numbers in the per-member section updated to the 03:10 run (the INDEX shifted by two lines). Nothing written outside the lane.
- 2026-09-29 03:39 JST — integration (the lead). `sept24_propagation_2026_09_24/real_costs_totals.py` now divides the
  adopted cases' per-member rows by the row-4 count (`main_case_decomposition_2026_09_29/derived/headcount.csv`) and
  adds column `pairing_on_priced_count` for the September 27 case from this lane's `pairing_5plus` and
  `per_member_5plus` sections, gated on this lane starting from its own pairing and dividing by the same count. The
  three cases' outputs differ from before only in 74 per-member cells, each ×1.0298163, and those four new rows.
  restate.py's per-member gate follows the CSV's divisor (`per_member_population_m` in the totals JSON), and one gate
  now ties that divisor to row 4 (51 gates). Reader rows now find their lines in the documents as committed at
  b170585, before the living documents take the restated figures, so reruns stay identical after they do; line
  numbers in `restated_pairing.csv` are at that commit. The INDEX rewrite at 928d659 removed the four superseded
  pairings' per-member line, so those rows name the INDEX as it read until then. rerun_lane.py with all six commands
  at 03:38: identical 23/23; restate.py again after the sept27 totals rerun: identical.
