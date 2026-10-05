**Verdict:** Split by generation, the main case adopted on 2026-09-29 ($371.4–434.8bn a year, with the pension
accrual) leaves all three Mexican-origin generations as net costs to other US residents at every one of its 64
specifications, under both ways of counting children. Counted in their own generation, the Mexico-born cost others
$97.2bn at the union's low end and $87.1bn at its high end ($8.8k / 7.9k per member). The second generation costs
$151.6 / 179.3bn ($10.6k / 12.5k) and the third-plus $122.6 / 168.4bn ($8.5k / 11.7k). Counted with their parents
they cost $169.4 / 197.4bn ($16.0k / 18.7k per adult), $110.6 / 121.8bn and $91.4 / 115.6bn. The change from
September 27 (+$49.6 / +47.5bn) falls mostly on the US-born generations under (a): +$24.0 / 26.4bn and
+$22.1 / 12.3bn, against +$3.5 / 8.8bn for the Mexico-born. The pension switch books the accrual on this year's
payroll taxes in place of this year's benefits. It adds $10.0bn to the Mexico-born at the low end and $33.9bn and
$32.8bn to the second and third-plus generations. The cash set (switch off, $294.7–361.8bn) gives $87.2 / 72.7bn,
$117.7 / 143.3bn and $89.8 / 145.8bn. [FRAMING-SENSITIVE] [CALCULATION: `run_generations_v4.cjs` →
`derived/generation_summary_sept29.json`, `generation_summary_sept29_cash.json`; section "v4 case (sept29)" below]

[2026-10-05: on main case v5 (`oct05`, $390.29–461.24bn), which adds 3.04M descendants who no longer report Mexican
origin to G3+, counted in their own generation the Mexico-born cost $97.15 / 87.02bn (September 29: 97.23 / 87.11), the
second generation $151.46 / 179.25bn (151.57 / 179.35) and the third-plus $141.68 / 194.97bn (122.61 / 168.38). G3+
costs $8,151 / 11,217 per member of 17.38M, against $8,549 / 11,740 of 14.34M. Counted with their parents: $169.27 /
197.30bn, $110.56 / 121.72bn and $110.46 / 142.22bn [ASSUMPTION: the added people stay in G3+ under (b)]. The cash set,
(a): $87.12 / 72.64bn, $117.62 / 143.22bn and $102.64 / 167.55bn. G1 and G2 move only by the larger group's responses
(−$0.09 to −0.11bn). [CALCULATION: `run_generations_v5.cjs` → `derived/generation_summary_oct05.json`,
`generation_summary_oct05_cash.json`; section "v5 case (oct05)" below]]

**September 27 case** (the default files, `derived/generation_results.csv`): Split by generation, the September 27
main case ($321.8–387.4bn a year) leaves all three
Mexican-origin generations as net costs to other US residents, at every one of its 64 specifications and
under both ways of counting children. Counted in their own generation, the Mexico-born cost others
$78–94bn a year ($6.4–7.7k per member), the second generation $128–153bn ($8.9–10.7k) and the third-plus
$100–156bn ($7.0–10.9k). Counted with their parents, as the National Academies count them, they cost
$159–191bn ($13.6–16.3k per adult), $87–95bn ($9.8–10.7k) and $75–102bn ($9.2–12.4k). The case's four
additions (long-run road and park responses, rental assistance, the return on public capital and the
government enterprises) add $63.3bn at the union's low end and $95.4bn at its high end. Under (a) the
second and third-plus generations carry 75–78% of that; under (b) the Mexico-born carry 37%. The return on
public capital, an imputed cost of the capital rather than a payment, is $8.7–11.5bn of the Mexico-born's
figure under (a) and $33.8–55.7bn of the union's. [FRAMING-SENSITIVE] [CALCULATION: `run_generations.cjs` →
`derived/generation_summary.json`, `change_from_sept26_schools`]

This paragraph's per-person figures divide by the CPS count (40.90m members, 28.77m adults). On the account's row-4
count (39.71m and 27.66m; ladder 274) the Mexico-born cost $7.1–8.5k per member and, counted with their parents,
$15.0–18.1k per adult. The US-born generations' figures do not change (section "v4 case (sept29)", 2026-09-29).

## v5 case (oct05), 2026-10-05

The operator adopted main case v5 on 2026-10-05 at 22:54 JST (`main_case_2026_10_05`, case key `oct05`;
decisions/2026-10-05-main-case-v5.md). It is the September 29 case plus the descendants of Mexican immigrants who no
longer report Mexican origin: 3,039,720 people on the account's frame (arm b), counted whole, a lineage of 42.75M. It
costs $390.2940–461.2431bn; the cash set beside it costs $307.3764–383.4093bn. Both keep specifications 48 and 11 as
their ends. Step 8 (`run_generations_v5.cjs`) splits both by generation into `*_oct05` and `*_oct05_cash` files. The
September 29 and September 27 files keep their names and bytes. Model self-report: claude-opus-5-5.

**How the split works.** The v5 payload is the September 29 payload of the same set, unchanged, plus 336 lineage edits,
the lineage's production grid and its meta. The meta carries the group-size responses at the larger group. Each
generation's payload is its September 29 payload (`generation_corrections_sept29*.json`) plus its v5 part
(`v5_split.cjs`, which the late-arrival lane shares):
- **The added people go on G3+.** G3+ takes the lineage's 335 cell edits and the production grid's change, as the case's
  `package.cjs` `withLineage()` adds them. The added people are priced as 1.96M identified G3+ members and 1.08M
  third-plus non-Hispanic whites at G3+ ages.
- **Row 8 is split.** The lineage's last edit is audit row 8's change at the larger group (−$0.0080bn on
  `lane_constants`), part of the union's response move. Each generation takes it times its share of the September 29
  union's `lane_constants` k cell, per allocation; this is the lineage lane's `generationCosts()` rule. The shares under
  (a) are G1 0.510, G2 0.221 and G3+ 0.269 (personal); under (b) they are 0.549, 0.217 and 0.234.
- **The responses need no rule.** Every generation is evaluated at the case's responses, which move with the group's
  size.

Costs come from candidate v4's `consumer.cjs` on the v5 payload. The v5 package's `evaluateFull` gives the same cost for
every model here (difference 0).

**Rules chosen here** [ASSUMPTION]:
- **Under (b) the added people stay in G3+.** Convention (b) counts minors with their parents, but the added people's
  parents' generation is not observed. Had their minors moved to G2 as the identified G3+'s do, about $4.89 / 8.38bn of
  their cost would move from G3+ to G2 (cash set $3.32 / 7.95bn). That figure is the added people's cost times the
  identified G3+'s fall from (a) to (b) at v5's responses: 25.5% / 31.3%. It is an indication, not a bound, and the union
  is unchanged (`summary` → `b_rule_indication`).
- **Adults among the added people.** They take the identified G3+'s adult share, 0.5706: 1,734,357 adults. The case
  prices them at the identified G3+'s age mix. Only per-adult figures use this.
- **Row 8 by `lane_constants` share** (the Consumers row's rule). The alternative puts the whole edit on G3+, as
  `withLineage()` does on the model it is given and as `main_case_2026_10_05` `api_check.json` pattern 3 prints. It moves
  G1 by +$0.0041bn, G2 by +$0.0018bn and G3+ by −$0.0058bn under (a); a gate reproduces pattern 3's print at its four
  decimals (`sensitivities.row8_on_g3plus`).

**Results, the set** ($bn a year; low and high are the union's ends: 48, shared allocation, and 11, personal). Each
cost and change column is rounded so the generations add to the printed union; the own range is rounded on its own.
[CALCULATION: `derived/generation_results_oct05.csv`, `generation_summary_oct05.json`]

| (a) Children in their own generation | $bn, low end | $bn, high end | Own range, $bn | $ per member, low / high | $ per adult, low / high | Change from September 29, $bn |
|---|---|---|---|---|---|---|
| G1, born in Mexico | 97.15 | 87.02 | 71.9–113.4 | 8,802 / 7,885 | 9,194 / 8,236 | −0.09 / −0.09 |
| G2, US-born, a parent born in Mexico | 151.46 | 179.25 | 151.5–179.2 | 10,568 / 12,506 | 16,990 / 20,106 | −0.10 / −0.11 |
| G3+, US-born of US-born parents, with the added people | 141.68 | 194.97 | 141.7–195.0 | 8,151 / 11,217 | 14,285 / 19,659 | +19.07 / +26.60 |
| All three (the case) | 390.29 | 461.24 | | 9,129 / 10,789 | 13,276 / 15,689 | +18.88 / +26.40 |

| (b) Minors with their parents (NAS 2017) | $bn, low end | $bn, high end | Own range, $bn | $ per member, low / high | $ per adult, low / high | Change from September 29, $bn |
|---|---|---|---|---|---|---|
| G1 | 169.27 | 197.30 | 169.3–197.3 | 10,800 / 12,589 | 16,019 / 18,672 | −0.11 / −0.12 |
| G2 | 110.56 | 121.72 | 106.5–125.9 | 9,057 / 9,970 | 12,402 / 13,653 | −0.09 / −0.10 |
| G3+ | 110.46 | 142.22 | 110.5–142.2 | 7,428 / 9,564 | 11,138 / 14,340 | +19.08 / +26.62 |

**Results, the cash set** (the pension switch off; [CALCULATION: `derived/generation_results_oct05_cash.csv`]):

| (a) | $bn, low end | $bn, high end | Own range, $bn | $ per member, low / high | $ per adult, low / high | Change from September 29, $bn |
|---|---|---|---|---|---|---|
| G1 | 87.12 | 72.64 | 57.5–103.3 | 7,894 / 6,582 | 8,245 / 6,875 | −0.08 / −0.09 |
| G2 | 117.62 | 143.22 | 117.6–143.2 | 8,206 / 9,992 | 13,193 / 16,065 | −0.10 / −0.11 |
| G3+ | 102.64 | 167.55 | 102.6–167.5 | 5,905 / 9,639 | 10,349 / 16,894 | +12.86 / +21.79 |
| All three | 307.38 | 383.41 | | 7,190 / 8,968 | 10,455 / 13,042 | +12.68 / +21.59 |

| (b) | $bn, low end | $bn, high end | Own range, $bn | $ per member, low / high | $ per adult, low / high | Change from September 29, $bn |
|---|---|---|---|---|---|---|
| G1 | 149.94 | 182.95 | 149.9–182.9 | 9,567 / 11,673 | 14,190 / 17,314 | −0.11 / −0.12 |
| G2 | 77.74 | 85.76 | 70.5–93.1 | 6,368 / 7,025 | 8,720 / 9,620 | −0.09 / −0.10 |
| G3+ | 79.70 | 114.70 | 79.7–114.7 | 5,359 / 7,713 | 8,036 / 11,565 | +12.88 / +21.81 |

Per-member figures add the 3,039,720 people to G3+ under both conventions: 17,382,294 members under (a), 14,871,214
under (b), and 42,752,213 for the union. The other generations keep the September 29 denominators. G3+'s cost per member
falls, because the added people cost less than an identified member: 1.08M of the 3.04M are priced as third-plus
whites. The
`uncorrected` columns are the identified generations' own models, so G3+'s `correction_bn` includes the added people.

**What moved from September 29, by part** ($bn, low / high end; the set, (a); [CALCULATION:
`generation_summary_oct05.json` → `change_from_sept29_by_part`]):

| Part | G1 | G2 | G3+ | Union |
|---|---:|---:|---:|---:|
| The responses at the larger group, with row 8's share | −0.09 / −0.09 | −0.10 / −0.11 | −0.11 / −0.12 | −0.30 / −0.32 |
| The added people | 0 | 0 | +19.18 / +26.72 | +19.18 / +26.72 |
| **Change** | −0.09 / −0.09 | −0.10 / −0.11 | +19.07 / +26.60 | +18.88 / +26.40 |

Row 8 is −$0.008bn of the union's response move. The union's parts are the lineage lane's arm b: the response move,
and the G3+ part (+16.72 / +22.96) plus the white part (+2.46 / +3.76) together, all to 1e-13bn. The response move is
the same in the cash set; there the added people add +12.97 / +21.91bn.

**Gates**, all passing (`run_generations_v5.cjs`: 28 in the set, 25 in the cash set):
- the September 29 generation models add to the union's September 29 model in all 335 cells (1.3e-12bn) and grid
  (5.7e-14bn), both conventions;
- the row-8 shares add to 1 (2.2e-16);
- each generation's v5 payload gives its September 29 model plus its part. G3+'s equals the package's `withLineage()`
  with row 8 moved to its share, exactly;
- the three v5 models add to the case's payload model in every cell (1.3e-12bn) and grid (5.7e-14bn);
- **oracle:** the union reproduces `main_case_2026_10_05/derived/main_case_bands.csv` (`adopted`, `cash_set`) at
  specifications 48 / 11 to 1e-4, and the set's `per_spec.csv` at all 64 specifications (1.7e-13bn). The uncorrected
  model reproduces `uncorrected_at_adopted_responses`, $313.0646–378.7098bn;
- the generations add to the union in all 64 specifications, corrected and uncorrected (1.6e-12bn), and so do their
  capital returns and enterprise receipts; the v5 package's `evaluateFull` gives every model's cost (difference 0);
- the parts start at the September 29 band (4.1e-5) and at `generation_results_sept29*.csv` (half its last digit), end
  at the v5 cost (exact), add across generations (1.5e-12bn), and equal the lineage lane's `v5_summary.json` and the
  case lane's `change_at_fixed_specifications` (2.0e-13bn);
- the alternative adds to the union (1.3e-12bn) and reproduces `api_check.json` pattern 3's print (4.5e-5bn).

`rerun_lane.py` over the lane's 18 commands (steps 0–8 of `run_all.sh`, the two modules and `run_all.sh` allowed
unrun): IDENTICAL, 56/56 files, exit 0 (23:09:56–23:10:51 JST). It needed `--online`. With uv offline, the first
attempt stopped at `tax_key_split.py`, because uv's cache cannot resolve `--with openpyxl --with xlrd`. That was a
transport failure, and no outputs were compared. The September 29 files are byte for byte unchanged.

**Files.**
- New scripts: `v5_split.cjs` (a module, for the late-arrival lane too) and `run_generations_v5.cjs`. `run_all.sh`
  gains step 8.
- New outputs: `derived/generation_{results,summary,corrections}_oct05{,_cash}.*`. Each file uses the sept29 file's
  layout. `generation_corrections_oct05*.json` applies to the same `model_*.json`; its `meta.union` is the v5 payload and
  `meta.builds_on` the sept29 file. The results CSV replaces the sept29 file's `sept27_cost_bn` and
  `change_from_sept27_bn` with `sept29_cost_bn` and `change_from_sept29_bn`, and adds `response_move_bn` and `lineage_bn`.

**Reproduce** (from the repository root; step 8 of `run_all.sh`, after step 7):
```
node infra/immigration-fiscal/generation_account_2026_09_24/run_generations_v5.cjs --case oct05
node infra/immigration-fiscal/generation_account_2026_09_24/run_generations_v5.cjs --case oct05_cash
```

Log (times from `date`, JST): 23:04 brief read; 23:07 first oct05 outputs (scratch), all gates passing; 23:08 written
to `derived/`; 23:08–23:09 rerun offline, stopped at `tax_key_split.py` (uv cache); 23:09:56–23:10:51 rerun
`--online` IDENTICAL 56/56, exit 0; 23:12 this section.

## v4 case (sept29), 2026-09-29

The operator adopted candidate v4 as the main case on 2026-09-29 at 15:12 JST (`main_case_2026_09_29`, case key
`sept29`). It costs $371.4146–434.8410bn with the pension accrual at payable benefits, net of the tax on benefits. The
cash set beside it, with the pension switch off, costs $294.7011–361.8175bn. Both have specifications 48 and 11 as
their ends. Step 7 splits both by generation into `*_sept29` and `*_sept29_cash` files. The September 27 files keep
their names and bytes (gate 1). Model self-report: claude-opus-5-5.

The split reads the adopted lane, landed at 40c4ba7 (`v4_split.cjs` `V4_LANE`). Until then it ran on candidate v4's
payload, which differs from the adopted `corrections.json` only in five meta stamps (`source`, `adopted`, `decision`,
`case`, `status`). The repointed run's results files are byte for byte the candidate run's.

**Resumed after the reboot.** The machine rebooted at about 20:51 JST, after this lane's gates had finished (20:35).
The gate logs were lost with the scratchpad; every output parsed complete. From 21:05 step 7 ran again directly, with
its gates printed, and `rerun_lane.py` gates 1 and 4 ran again (times below).

**How the split works.** The case's payload is the September 27 `corrections.json` unchanged, then v4's part. That
part is 2 receipt lines, 3 national-scale edits, 135 cell edits (133 in the cash set), 5 synthetic lines and the
row-4 production grid. Its cell edits are the two fill-in methods' mean change. Every v4 item is linear in the cells
it reads except the roads item's driver-mile share. The items applied once to the methods'-mean model (the September
27 payload on `model.json`), with that share read off the payload's `meta.roads_mileage_key`, reproduce v4's part:
every cell to 7.1e-15bn and the receipt lines to 4.4e-16bn.

Each generation's payload is built in three parts:
- its September 27 payload (`generation_corrections.json`);
- the case's three national scales;
- its own v4 tail.

The tail is candidate v4's own item functions applied to the generation's September 27 model in the package's order,
with each union input replaced by the generation's own (`v4_split.cjs`, which the late-arrival lane shares). The
production grid is the generation's row-4 attribution. Costs come from candidate v4's `consumer.cjs`: `engine.js`
with the payload's responses and capital rules, which also costs the item chain's part-built payloads. The adopted
lane's `package.cjs` `evaluateFull` gives the same cost for every model here (difference 0).

**Rules designed for this split.** Six items read a union input that needed a generation rule. The last column is the
alternative's move on the Mexico-born, (a), low / high end, in the set:

| Item | Rule used | Why | Alternative (key in `sensitivities`) | G1 move, $bn |
|---|---|---|---|---|
| 2 Production on the account's weights | `production.py`'s attribution re-run on the row-4 weights, all 3,888 scenarios (`v4_inputs.py`) | the union's grid is that attribution on the same weights; the generations add to it to 1.1e-13bn | none: exact | 0 |
| 3 IRS-matched income-tax key | each generation's own change in the raked CBO-group × AGI-bin cells (`tax_key_split.py` re-runs the tax lane's raking with each generation's dollars in each cell) times its own stack factor on the line; the remainder (at most $0.24bn) goes by the cells after the stack; per method, then the methods' mean | the lane's rule for the CBO gradient, a ratio-type change of the same kind; the raked change is exact by generation (adds to the union's to 1e-15) | the union's shift by the generations' September 27 amounts on the line (`fit_by_amount`) | +0.46 / +0.06 |
| 5 Tenant property tax | the group's contract-rent share by state (ACS group rent) split by the generations' persons in cash-rent homes in each state | the line is keyed on the rent the group pays where it lives | the same persons nationally (`tenant_national`) | −0.01 / −0.01 |
| 5 Personal property tax | the group's vehicle share × the generation's part of the licence line (its adults key), per allocation | vehicle ownership follows adults, as licences do | the population key (`vehicles_by_population`) | +0.04 / +0.14 |
| Roads keyed by miles | the union's methods'-mean driver-mile share × the generation's persons aged 5 and over over the union's (row-4 weights) | the union's formula puts every person aged 5+ at the group's miles; the split keeps that | the population key cells (`roads_by_population`) | −0.11 / −0.31 |
| Pension switch (the set only) | Social Security: the union's accrual split by each generation's accrual per OASDI tax dollar, net of its future benefit-tax share at its own rate (pension lane at 9ea1beb: G1 1.041, G2 0.919, G3+ 0.962), × its OASDI receipts in the account. Part A: likewise, its Part A accrual per HI tax dollar (1.439, 1.593, 1.348) × its HI receipts. Tax on current benefits: its 2024 benefit tax (census-income mapping, per allocation) | the accrual per tax dollar differs by generation with age and earnings (the benefit formula is progressive); the account's own receipts carry the allocation | the payload's literal rule, the union's ratios on every generation (`pension_union_rules`) | −1.77 / −1.88 |
| | | | the pension lane's Part A accruals as fixed shares (`part_a_lane_shares`) | +3.69 / +1.25 |

The other items need no new rule, because their functions read the generation's own model:
- item 1 puts the deficit at the generation's rental-key share;
- item 4's capital key reads its evaluation;
- the owner part of item 5 is a response;
- 6a, 7 and state pricing apply the union's ratios and indexes to its own amounts.

Convention (b) takes convention (a)'s pension ratios, which the pension lane measured by own generation.

The Part A rule first used the lane's accruals as fixed shares. It was replaced before any output was kept, because
fixed shares ignore the allocation. Under the shared allocation G1's HI receipts fall to 21.8% of the union's, yet
it would keep 30.6% of the accrual. Fixed shares also import the lane's own HI tax base (G1 31.1% of it) in place of
the account's (28.0%, personal). [CALCULATION: `v4_split.cjs` `split()`; the lane's `hi_arms.csv`, central row]

**Results, the set** ($bn a year; low and high are the union's ends: 48, shared allocation, and 11, personal).
Each column is rounded so the generations add to the printed union. [CALCULATION: `derived/generation_results_sept29.csv`]

| (a) Children in their own generation | $bn, low end | $bn, high end | Own range over the 64 specifications, $bn | $ per member, low / high | $ per adult, low / high | Change from September 27, $bn |
|---|---|---|---|---|---|---|
| G1, born in Mexico | 97.2 | 87.1 | 72.0–113.5 | 8,810 / 7,893 | 9,202 / 8,244 | +3.5 / +8.8 |
| G2, US-born, a parent born in Mexico | 151.6 | 179.3 | 151.6–179.3 | 10,575 / 12,513 | 17,002 / 20,118 | +24.0 / +26.4 |
| G3+, US-born of US-born parents | 122.6 | 168.4 | 122.6–168.4 | 8,549 / 11,740 | 14,983 / 20,575 | +22.1 / +12.3 |
| All three (the case) | 371.4 | 434.8 | | 9,353 / 10,950 | 13,426 / 15,718 | +49.6 / +47.5 |

| (b) Minors with their parents (NAS 2017) | $bn, low end | $bn, high end | Own range, $bn | $ per member, low / high | $ per adult, low / high | Change from September 27, $bn |
|---|---|---|---|---|---|---|
| G1 | 169.4 | 197.4 | 169.4–197.4 | 10,807 / 12,596 | 16,030 / 18,683 | +10.4 / +6.6 |
| G2 | 110.6 | 121.8 | 106.6–126.0 | 9,064 / 9,978 | 12,413 / 13,664 | +23.3 / +26.8 |
| G3+ | 91.4 | 115.6 | 91.4–115.6 | 7,724 / 9,771 | 11,167 / 14,127 | +15.9 / +14.1 |

**Results, the cash set** (the pension switch off):

| (a) | $bn, low end | $bn, high end | Own range, $bn | $ per member, low / high | $ per adult, low / high | Change from September 27, $bn |
|---|---|---|---|---|---|---|
| G1 | 87.2 | 72.7 | 57.6–103.4 | 7,901 / 6,590 | 8,253 / 6,883 | −6.6 / −5.6 |
| G2 | 117.7 | 143.3 | 117.7–143.3 | 8,213 / 10,000 | 13,205 / 16,077 | −9.8 / −9.6 |
| G3+ | 89.8 | 145.8 | 89.8–145.8 | 6,260 / 10,162 | 10,971 / 17,811 | −10.7 / −10.4 |
| All three | 294.7 | 361.8 | | 7,421 / 9,111 | 10,653 / 13,079 | −27.1 / −25.6 |

| (b) | $bn, low end | $bn, high end | Own range, $bn | $ per member, low / high | $ per adult, low / high | Change from September 27, $bn |
|---|---|---|---|---|---|---|
| G1 | 150.1 | 183.1 | 150.1–183.1 | 9,574 / 11,680 | 14,200 / 17,325 | −8.9 / −7.8 |
| G2 | 77.8 | 85.8 | 70.6–93.2 | 6,375 / 7,033 | 8,730 / 9,631 | −9.5 / −9.1 |
| G3+ | 66.8 | 92.9 | 66.8–92.9 | 5,648 / 7,852 | 8,165 / 11,352 | −8.7 / −8.7 |

Per-member figures use the row-4 headcounts (`v4_inputs.py`): 39.71m members and 27.66m adults, the case's basis. The
September 27 tables below use the corrected population key (40.90m and 28.77m), so per-member figures differ between
the two sections by the basis as well as the case.

The denominators, members / adults: (a) G1 11,036,701 / 10,566,525, G2 14,333,218 / 8,914,883, G3+ 14,342,575 /
8,183,369; (b) G1 15,672,846, G2 12,208,153, G3+ 11,831,494, with the same adults; all three 39,712,493 / 27,664,776
(ladder 274). Only the Mexico-born's count differs between the two bases: row 4 scales naturalized Mexico-born by
0.856 and noncitizens by 0.778, and G2 and G3+ keep their CPS weights (under (b) the minors who move with them shift
the counts by under 0.001m). The September 27 files (`generation_results.csv`, `generation_summary.json`) divide the
Mexico-born's account totals by the CPS count, 12.22m members and 11.67m adults. They stay byte for byte (gate 1). On
row 4 September 27's Mexico-born cost $8,496 / 7,096 per member under (a) and $15,049 / 18,057 per adult under (b);
the September 27 section prints $7,673 / 6,408 and $13,620 / 16,343.
[CALCULATION: `generation_results.csv` `cost_bn` ÷ `generation_results_sept29.csv` `population`, `adults`]

**What moved from September 27, by item** ($bn, low / high end; the items in candidate v4's order, each costed after
the ones before it, so they add to the change; [CALCULATION: `generation_summary_sept29.json` →
`change_from_sept27_by_item`]):

| Item | (a) G1 | (a) G2 | (a) G3+ | Union |
|---|---:|---:|---:|---:|
| 1 Public housing's deficit, tenant key | −0.75 / −0.74 | −0.76 / −0.77 | −0.18 / −0.18 | −1.69 / −1.69 |
| 2 Production on the account's weights | +1.40 / +0.94 | +0.13 / +0.09 | +0.11 / +0.08 | +1.64 / +1.11 |
| 3 IRS-matched income-tax key | −1.01 / −0.67 | −1.46 / −1.92 | −0.73 / −0.51 | −3.20 / −3.10 |
| 4 Public housing's capital, tenant key | −0.15 / −0.23 | −0.16 / −0.24 | −0.04 / −0.06 | −0.35 / −0.53 |
| 5 Long-run property taxes | −7.65 / −7.75 | −9.37 / −9.34 | −10.17 / −10.10 | −27.19 / −27.19 |
| 6a Payroll compliance | +0.16 / +0.34 | +0.11 / +0.11 | +0.13 / +0.09 | +0.40 / +0.54 |
| 7 Workers' compensation | −0.23 / −0.23 | −0.19 / −0.17 | −0.53 / −0.33 | −0.95 / −0.73 |
| Roads keyed by miles | +0.92 / +2.01 | +0.88 / +1.63 | +0.22 / +0.13 | +2.02 / +3.77 |
| State pricing | +0.74 / +0.75 | +0.96 / +0.99 | +0.51 / +0.53 | +2.21 / +2.27 |
| Pension switch (the set only) | +10.03 / +14.38 | +33.85 / +36.02 | +32.83 / +22.62 | +76.71 / +73.02 |
| **Change** | +3.46 / +8.80 | +23.99 / +26.40 | +22.15 / +12.27 | +49.60 / +47.47 |

Rounded so each column adds to its change and each row to the union; one cell in a few moves by 0.01. The union
column is candidate v4's attribution in this order (its marginals; its "alone" figures differ by the pairwise
interactions it reports). Under (b) the pension switch adds $19.3 / 14.4bn to the Mexico-born, $32.8 / 36.0bn to G2
and $24.6 / 22.7bn to G3+ (`change_from_sept27_by_item.b`).

The pension switch moves most. The accrual follows the payroll taxes a generation pays this year. The benefits it
replaces follow this year's beneficiaries. Under (a) the Mexico-born's Social Security and Medicare cost therefore
rises less than the US-born generations'. The property item (5) lowers every generation's cost, by $7.7–10.2bn
under (a).

**Gates**, all passing (`run_generations_v4.cjs`: 27 in the set, 26 in the cash set; logs in the session scratchpad):
- the union's items reproduce v4's part of the payload: 135 cells to 7.1e-15bn, receipt lines to 4.4e-16bn, with the
  same synthetic lines;
- the September 27 generation payloads add to its `corrections.json` in all 278 cells, and their models to the
  union's;
- item 3's generation shifts add to the union's in each method and in the mean (4.4e-16bn); the production grids add
  to the payload's in all 3,888 scenarios (5.7e-14bn);
- under each convention the generations' tails add to the union's (1.0e-12bn), and each payload gives the model its
  item chain built (exact);
- **oracle:** the union reproduces the adopted lane's band at specifications 48 / 11 (`main_case_bands.csv`, rows
  `adopted` and `cash_set`): $371.4146–434.8410bn and $294.7011–361.8175bn, as the mean of the two fill-in methods.
  The tolerance is 1e-4, the band's four decimals. The set also reproduces the lane's cost at all 64 specifications
  (`per_spec.csv`, 1.7e-13bn). In both sets the uncorrected model reproduces the row
  `uncorrected_at_adopted_responses`, $313.2581–378.9158bn (1e-4);
- the adopted lane's `package.cjs` `evaluateFull` (for the cash set, on `forPayload` of its payload) gives the cost of
  every model here, union and generations, corrected and uncorrected, at every specification (difference 0);
- the generations add to the union in all 64 specifications, corrected and uncorrected (1.6e-12bn), and so do their
  capital returns (total, by level, by part) and enterprise receipts;
- the change by item starts at the September 27 band (4.5e-5) and at each generation's row of
  `generation_results.csv` (half its last printed digit), ends at the case's cost (5.7e-14bn), and adds across
  generations item by item (1.5e-12bn);
- every alternative's split adds to the union's (1.0e-12bn).

`rerun_lane.py` gates after the repoint (times from `date`, JST):
- gate 1, the twelve September 27 commands: IDENTICAL, 48/48 files, exit 0 (20:16–20:18). The five v4 scripts were
  allowed unrun.
- gate 4, the twelve commands plus step 7's four: pass 1 IDENTICAL, 48/48, exit 0 (20:23–20:24); pass 2 IDENTICAL,
  48/48, exit 0 (20:31–20:35). `v4_split.cjs`, a module, and `run_all.sh`, whose steps the list names, were allowed
  unrun.

Rerun after the reboot, with the same command lists:
- step 7 directly (21:05): `v4_inputs.py` 20 gates and `tax_key_split.py` 9, all passing; `run_generations_v4.cjs` 27
  and 26 gates, all passing, oracle as above.
- gate 1: IDENTICAL, 48/48, exit 0 (21:05–21:09).
- gate 4: pass 1 IDENTICAL, 48/48, exit 0 (21:09–21:11); pass 2 IDENTICAL, 48/48, exit 0 (21:11–21:13). No script
  was reported NOT RUN. Of the tracked files, only `RESULT.md` and `run_all.sh` differ from HEAD.

**Files.**
- New scripts: `v4_inputs.py`, `tax_key_split.py`, `v4_split.cjs` (a module, shared with the late-arrival lane) and
  `run_generations_v4.cjs`. `run_all.sh` gains step 7.
- New outputs: `derived/v4_inputs.json` (`v4_inputs.py`), `derived/tax_key_by_generation.json` (`tax_key_split.py`),
  both read by `run_generations_v4.cjs` (the tax file for item 3), and
  `derived/generation_{results,summary,corrections}_sept29{,_cash}.*`.
- `generation_results.csv`, `generation_summary.json` and `generation_corrections.json` keep the September 27
  case.
- For consumers such as the world ledger's pins: each sept29 file is the default name with `_sept29`, in the same
  layout. `generation_corrections_sept29.json` applies to the same `model_*.json`. `generation_summary_sept29.json`
  carries `low_spec` and `high_spec` as the default does, plus `specifications`, `rules`, `sensitivities` and
  `change_from_sept27_by_item`. The results CSV adds three columns: `housing_enterprise_surplus_receipt_bn`,
  `sept27_cost_bn` and `change_from_sept27_bn`.
- Each sept29 corrections file names the case's lane in `meta.case_lane` (`main_case_2026_09_29`) and the union's
  payload in `meta.union`. The set's is the adopted lane's `derived/corrections.json`. The cash set's is candidate
  v4's `corrections_v4_cash.json`, which the adopted lane reads for its own `cash_set` row; that lane publishes no
  cash payload.

**Not computed.**
- State pricing by each generation's own state mix. The payload's rule applies the union's price indexes to each
  generation's keys; indexes by generation would need the state-pricing lane's inputs by generation.
- The ledger bridge (`compare_ledger.py`) stays on the September 27 run.

**Reproduce** (from the repository root; step 7 of `run_all.sh`):
```
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/generation_account_2026_09_24/v4_inputs.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl --with xlrd python3 infra/immigration-fiscal/generation_account_2026_09_24/tax_key_split.py
node infra/immigration-fiscal/generation_account_2026_09_24/run_generations_v4.cjs --case sept29
node infra/immigration-fiscal/generation_account_2026_09_24/run_generations_v4.cjs --case sept29_cash
```

Log (times from `date`, JST): 15:17 brief read; 16:43 inputs built and gated (`v4_inputs.py`, `tax_key_split.py`);
17:08 first sept29 outputs; 17:12 gate 1 IDENTICAL; 17:14 Part A rule replaced (per HI tax dollar); 17:21 outputs
rebuilt; 20:15 repointed to the adopted lane (40c4ba7), `meta.union` on its payload; 20:16 outputs rebuilt, results
unchanged; 20:16–20:35 `rerun_lane.py` gates 1 and 4; about 20:51 reboot; 21:05–21:13 step 7 and gates 1 and 4
rerun.

## September 27 case (2026-09-27)

The operator adopted the September 27 case (`main_case_long_run_2026_09_27`, $321.8194–387.3701bn; decision
`2026-09-27-main-case-capital-return-and-long-run-responses`). It is the schools case with four additions:
long-run responses for roads and parks (economic affairs and recreation), rental assistance at response 1,
the return on public capital at 2% at the low end and 3% at the high end, and the government enterprises
under option D. `derived/` holds this case (`--case sept27`, the default). `--case sept26_schools`,
`--case sept26` and `--case sept24` with `--out-dir DIR` reproduce the three sections below byte for byte.
Model self-report: claude-opus-5-5. Propagation report:
[RESULT_generation.md](../sept27_propagation_2026_09_27/RESULT_generation.md).

**How the split works.** Each generation's corrected model is its share of the schools-case payload (the
split below, unchanged), followed by `rekeyEdits()` on that model. The re-key moves the generation's
`enterprise_surplus` receipt to its own corrected population share, read from `general_public_services`'
population cell, as the package's `modelFor()` does for the union. The generations' re-key edits add to the
case's eight (gate). Every model is evaluated through the package's `evaluateFull()`: the engine at the
specification's line responses, plus the capital return. Each of the return's 24 components takes its key
from that evaluation, so a generation's own amounts split it. The 13 core, road and park components key
off their spending lines. The 11 enterprise components key off the generation's `enterprise_surplus`
receipt share.

The ends stay the schools case's: specification 48 (shared allocation, GDP normalization, school share
0.715, general government 0.6000, the low long-run readings with roads at 0.3840 and parks at 0.8562, 2%)
and specification 11 (personal, cash, 0.865, 0.8504, roads at 0.6386 and parks at 1, 3%). Rental
assistance and the enterprise receipt respond at 1 at both. As before, "low" and "high" are the union's
range ends, not each generation's own minimum and maximum.

| (a) Children in their own generation | $bn at the union's low end (shared) | $bn at the union's high end (personal) | Own range over the 64 specifications, $bn | $ per member, low / high | $ per adult, low / high |
|---|---|---|---|---|---|
| G1, born in Mexico | 93.8 | 78.3 | 63.5–109.6 | 7,673 / 6,408 | 8,032 / 6,708 |
| G2, US-born, a parent born in Mexico | 127.6 | 153.0 | 127.6–153.0 | 8,901 / 10,671 | 14,311 / 17,157 |
| G3+, US-born of US-born parents | 100.5 | 156.1 | 100.5–156.1 | 7,005 / 10,884 | 12,277 / 19,076 |
| All three (the case) | 321.8 | 387.4 | 321.8–387.4 | 7,869 / 9,472 | 11,185 / 13,463 |

| (b) Minors with their parents (NAS 2017) | $bn at the union's low end (shared) | $bn at the union's high end (personal) | Own range over the 64 specifications, $bn | $ per member, low / high | $ per adult, low / high |
|---|---|---|---|---|---|
| G1 | 159.0 | 190.8 | 159.0–190.8 | 9,434 / 11,320 | 13,620 / 16,343 |
| G2 | 87.3 | 95.0 | 80.2–102.2 | 7,152 / 7,781 | 9,794 / 10,656 |
| G3+ | 75.5 | 101.6 | 75.5–101.6 | 6,380 / 8,584 | 9,225 / 12,412 |

Members and adults do not change with the case: 40.90m and 28.77m in all. [CALCULATION:
`run_generations.cjs` → `derived/generation_results.csv`]

**From the schools case to this one.** The chain runs at the fixed end specifications and follows
`main_case.cjs`'s order and definitions for every generation (`generation_summary.json` →
`change_from_sept26_schools`):
- Roads and parks, and rental assistance, are each addition alone less the old settings on the re-keyed
  model.
- The three capital parts are the return's components on the case.
- The re-key is the old settings on the re-keyed model less the schools case. It is exactly 0 for every
  generation, because the receipt is still at response 0 when the re-key applies.
- The enterprise surplus is the receipt's cost at response 1.

The parts add to each generation's move within 3.6e-14bn. The union's parts equal the case's
`change_at_fixed_specifications` part by part, and its move equals the case's `change` (+63.33 / +95.42,
1.1e-13bn; gates).

| | Schools case | Roads and parks, long run | Rental assistance | Capital, core | Capital, roads and parks | Re-key | Enterprise surplus (receipt) | Capital, enterprises | **September 27** | Change |
|---|---|---|---|---|---|---|---|---|---|---|
| Union | 258.49 / 291.95 | +19.44 / +29.63 | +4.53 / +4.53 | +15.99 / +25.78 | +6.18 / +12.47 | 0.00 / 0.00 | +5.56 / +5.56 | +11.62 / +17.44 | **321.82 / 387.37** | +63.33 / +95.42 |
| (a) G1 | 77.65 / 56.91 | +4.98 / +7.53 | +0.85 / +0.85 | +3.96 / +3.49 | +1.56 / +3.14 | 0.00 / 0.00 | +1.55 / +1.55 | +3.23 / +4.85 | **93.77 / 78.31** | +16.13 / +21.40 |
| (a) G2 | 105.00 / 117.46 | +6.66 / +10.10 | +1.40 / +1.40 | +6.22 / +11.46 | +2.10 / +4.23 | 0.00 / 0.00 | +2.01 / +2.01 | +4.20 / +6.29 | **127.58 / 152.95** | +22.58 / +35.49 |
| (a) G3+ | 75.84 / 117.58 | +7.80 / +12.00 | +2.28 / +2.28 | +5.82 / +10.83 | +2.52 / +5.11 | 0.00 / 0.00 | +2.01 / +2.01 | +4.20 / +6.30 | **100.47 / 156.10** | +24.62 / +38.52 |
| (b) G1 | 135.56 / 155.38 | +6.67 / +10.03 | +1.27 / +1.27 | +6.66 / +10.90 | +2.06 / +4.15 | 0.00 / 0.00 | +2.19 / +2.19 | +4.59 / +6.88 | **159.01 / 190.80** | +23.45 / +35.42 |
| (b) G2 | 67.90 / 66.06 | +6.07 / +9.26 | +1.26 / +1.26 | +4.87 / +7.45 | +1.93 / +3.90 | 0.00 / 0.00 | +1.71 / +1.71 | +3.57 / +5.36 | **87.31 / 95.00** | +19.41 / +28.94 |
| (b) G3+ | 55.02 / 70.52 | +6.70 / +10.34 | +2.01 / +2.01 | +4.46 / +7.43 | +2.18 / +4.42 | 0.00 / 0.00 | +1.66 / +1.66 | +3.46 / +5.20 | **75.49 / 101.57** | +20.47 / +31.05 |

Share of the change by generation, low / high:

- (a) G1 25% / 22%; G2 36% / 37%; G3+ 39% / 40%
- (b) G1 37% / 37%; G2 31% / 30%; G3+ 32% / 33%

The additions fall less on the Mexico-born under (a): G1 takes 25% of the move at the low end and 22% at
the high end, the second and third-plus generations 75–78%. G1's share of every addition is below its 30%
of members:
- 19% of rental assistance, by the rental key;
- 25% of roads and parks;
- 28% of the enterprise surplus and the enterprise return, by its receipt share;
- 25% / 14% of the core capital return, whose school and college parts follow the pupils at the personal
  high end.

Under (b) the first generation takes 37% at both ends. [FRAMING-SENSITIVE]

**The capital return and the enterprise receipt.** The return is an imputed resource cost: the
opportunity cost of the capital at 2% / 3%, not a payment. It belongs in annual cost totals and never in a
borrowing flow. The enterprise surplus is a receipt: the group's share of the enterprises' operating loss
(−$47.46bn nationally, NIPA 3.1 line 19), at response 1. Its cost to others is minus its effect.

| | Capital return | of which core | roads and parks | enterprises | public housing (in enterprises) | state and local | federal | Enterprise surplus, group amount | its share of −$47.46bn | cost to others | re-key's move of the amount |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Union | +33.80 / +55.69 | +15.99 / +25.78 | +6.18 / +12.47 | +11.62 / +17.44 | +0.99 / +1.48 | +32.97 / +53.95 | +0.83 / +1.74 | −5.56 / −5.56 | 0.1172 | +5.56 / +5.56 | +0.15 / +0.15 |
| (a) G1 | +8.75 / +11.47 | +3.96 / +3.49 | +1.56 / +3.14 | +3.23 / +4.85 | +0.27 / +0.41 | +8.52 / +11.00 | +0.23 / +0.47 | −1.55 / −1.55 | 0.0326 | +1.55 / +1.55 | +0.16 / +0.16 |
| (a) G2 | +12.51 / +21.98 | +6.22 / +11.46 | +2.10 / +4.23 | +4.20 / +6.29 | +0.36 / +0.53 | +12.21 / +21.36 | +0.30 / +0.62 | −2.01 / −2.01 | 0.0423 | +2.01 / +2.01 | −0.01 / −0.01 |
| (a) G3+ | +12.54 / +22.24 | +5.82 / +10.83 | +2.52 / +5.11 | +4.20 / +6.30 | +0.36 / +0.53 | +12.24 / +21.59 | +0.30 / +0.65 | −2.01 / −2.01 | 0.0423 | +2.01 / +2.01 | −0.01 / −0.01 |
| (b) G1 | +13.32 / +21.93 | +6.66 / +10.90 | +2.06 / +4.15 | +4.59 / +6.88 | +0.39 / +0.58 | +13.02 / +21.30 | +0.29 / +0.62 | −2.19 / −2.19 | 0.0462 | +2.19 / +2.19 | +0.16 / +0.16 |
| (b) G2 | +10.38 / +16.72 | +4.87 / +7.45 | +1.93 / +3.90 | +3.57 / +5.36 | +0.30 / +0.45 | +10.11 / +16.16 | +0.27 / +0.56 | −1.71 / −1.71 | 0.0360 | +1.71 / +1.71 | −0.01 / −0.01 |
| (b) G3+ | +10.11 / +17.05 | +4.46 / +7.43 | +2.18 / +4.42 | +3.46 / +5.20 | +0.29 / +0.44 | +9.84 / +16.49 | +0.27 / +0.56 | −1.66 / −1.66 | 0.0349 | +1.66 / +1.66 | −0.01 / −0.01 |

The corrections lower the Mexico-born's population cell of `general_public_services` by $1.35bn (−9%;
the stack's reweighting to the ACS count) and raise the second and third-plus generations' by $0.06bn
each. The re-key therefore moves the first generation's receipt from −$1.71bn to −$1.55bn (share 0.0359 →
0.0326), and the other two by −$0.01bn each. Its effect on the case, −$0.45bn / −$0.60bn for the union, is
−$0.49bn / −$0.66bn for G1 and +$0.02bn / +$0.03bn for each of the others (the lane `enterprise_rekey`).

| | Economic affairs (roads, transit and the rest of the line) | Recreation and culture (parks) | Re-key's effect (case less the same case at model.json's share) |
|---|---|---|---|
| Union | +13.99 / +23.27 | +5.45 / +6.37 | −0.45 / −0.60 |
| (a) G1 | +3.46 / +5.76 | +1.51 / +1.77 | −0.49 / −0.66 |
| (a) G2 | +4.69 / +7.81 | +1.97 / +2.30 | +0.02 / +0.03 |
| (a) G3+ | +5.83 / +9.70 | +1.97 / +2.30 | +0.02 / +0.03 |
| (b) G1 | +4.52 / +7.52 | +2.15 / +2.51 | −0.49 / −0.65 |
| (b) G2 | +4.39 / +7.30 | +1.68 / +1.96 | +0.02 / +0.02 |
| (b) G3+ | +5.08 / +8.45 | +1.62 / +1.90 | +0.02 / +0.02 |

The union's line figures equal the case's `lines_at_end_specifications` (gate).

**What else moved.** Three lanes change because lines they edit now respond (`lanes`, union under (a), $bn
low / high):
- The benefits lane includes a −$2.45bn correction to rental assistance (before the stack factor), which
  had no effect while the line sat at 0. It moves from +2.15 / +2.02 to −0.02 / −0.16. Rental assistance's
  +$4.53bn in the chain is net of it.
- The consumption key edits cells of economic affairs, recreation and rental assistance. It moves from
  −4.05 / −4.05 to −3.00 / −2.19.
- The stack moves from +19.41 / +20.82 to +17.27 / +17.76.
The medical, education and justice lanes move by $0.25bn or less. They edit lines that key the capital
return. The new lane `enterprise_rekey` adds −0.45 / −0.60. The eight split sensitivities re-run with the
re-key; their largest move stays $3.71bn (`fill_ins_by_imputed_dollars`).

**Beside the account.** These rows stay outside the range, as in the case: without the capital return,
option A (enterprises out) and the return at 7% on every component. Each is taken at that variant's own
union ends, all 48 / 11. The union reproduces the case's `main_case_bands.csv` rows (gate), and the
generations add to it.

| | Without the capital return | Option A, enterprises out | Capital at 7% on every component |
|---|---|---|---|
| Union | 288.02 / 331.68 | 304.63 / 364.37 | 406.31 / 461.62 |
| (a) G1 | 85.02 / 66.84 | 89.00 / 71.92 | 115.64 / 93.61 |
| (a) G2 | 115.07 / 130.97 | 121.38 / 144.65 | 158.85 / 182.26 |
| (a) G3+ | 87.93 / 133.87 | 94.26 / 147.80 | 131.81 / 185.76 |
| (b) G1 | 145.70 / 168.88 | 152.23 / 181.72 | 192.30 / 220.04 |
| (b) G2 | 76.94 / 78.28 | 82.03 / 87.93 | 113.25 / 117.29 |
| (b) G3+ | 65.39 / 84.52 | 70.37 / 94.72 | 100.76 / 124.30 |

**Ledger bridge.** The bridge now evaluates through the package's `stateFor()`. The propagation brief
names this lane's own copy of the engine state, which would have missed the line responses. Under
`sept27` the capital return sits inside each fiscal column, as part of the direct fiscal response.
`ledger_comparison.csv` adds it on its own (`account_capital_return_*`). For G1 at the shared end that is
$716 of the $7,673 per member. The September 19 ledger has no capital return. [CALCULATION:
`compare_ledger.py`]

**Inherited, not repaired here.**
- The conceptual audit of 2026-09-27 (§7) finds that a federal housing subsidy is charged at the rental
  key and credited inside the enterprise surplus at the population key. That favours the group, by about
  $0.2bn for public housing's operating subsidies and at most $2.53bn. The split carries the mismatch into
  each generation: rental assistance by its housing key, the receipt by its population share.
- Rental assistance is a capped program. Without the group, other eligible households would take the
  slots. The $4.53bn is their loss, not a budget change. It counts at 1 in the account, and the chain
  keeps it as its own part.

**Gates.** A `sept27` run has 58 gates. Beyond the earlier cases' checks, they add:
- the specifications carry `meta.responses` and the rates;
- the payload is the schools payload plus the re-key;
- the generations' re-key edits add to the case's;
- the uncorrected generation models need no re-key (receipt share equals population share to 1.9e-12);
- each generation's payload gives the model `modelFor()` builds;
- the union reproduces `per_spec.csv` (576 values, 2.3e-13bn);
- the generations' capital return and receipt add to the union's at every specification;
- the chain gates above, and the rows beside the account.

A failed gate now writes nothing.

**Reproduce** (from the repository root; steps 0-6 took about a minute on 2026-09-27):
```
bash infra/immigration-fiscal/generation_account_2026_09_24/run_all.sh
node infra/immigration-fiscal/generation_account_2026_09_24/run_generations.cjs --case sept26_schools --out-dir DIR
```
The headline cell (a), G1, low end is 93.772592 (`generation_results.csv`).

## Schools at full average cost (2026-09-26; superseded as the default 2026-09-27)

[2026-09-27: `derived/` now holds the September 27 case. This section's numbers reproduce with
`--case sept26_schools --out-dir DIR`, byte for byte against 0f22f0c.]

Verdict of 2026-09-26: Split by generation, the main case with schools at full average cost ($258.5–292.0bn a
year) leaves all three Mexican-origin generations as net costs to other US residents, at every one of
its 64 specifications and under both ways of counting children. Counted in their own generation, the
Mexico-born cost others $57–78bn a year ($4.7–6.4k per member), the second generation $105–117bn
($7.3–8.2k) and the third-plus $76–118bn ($5.3–8.2k). Counted with their parents, as the National
Academies count them, they cost $136–155bn ($11.6–13.3k per adult), $66–68bn ($7.4–7.6k) and
$55–71bn ($6.7–8.6k). Against the one-year scenario, schools at full cost add $58.4bn at the union's
low end and $45.4bn at its high end, and where the children are counted decides who carries it.
Under (a) the second and third-plus generations carry 76–91% of it; under (b) the Mexico-born carry
43–44%. [FRAMING-SENSITIVE] [CALCULATION: `run_generations.cjs` → `derived/generation_summary.json`,
`change_from_sept26`]

At 22:39 JST the operator adopted schools at full average cost per pupil as the main case
(`main_case_schools_full_2026_09_26`, $258.4885–291.9548bn; decision
`2026-09-26-main-case-schools-full-cost`). It is the September 26 case (finite-removal responses, row 8
at 0.949, the consumption key) with the school response at 1. `derived/` held this case
(`--case sept26_schools`, then the default). `--case sept26 --out-dir DIR` reproduces the one-year scenario
below byte for byte, and `--case sept24 --out-dir DIR` reproduces the September 24 record. Model
self-report: claude-opus-5-5. Propagation report:
[RESULT_generation.md](../sept26_propagation_2026_09_26/RESULT_generation.md).

These figures are net costs to other US residents, $bn a year, 2024. "Low" and "high" are the union's
range ends, and every generation is evaluated at those two specifications. They are not each
generation's own minimum and maximum; the "Own range" column gives those. The low end is the shared
allocation with GDP normalization, school share 0.715 and general government at 0.6000
(specification 48). The high end is the personal allocation with cash normalization, school share
0.865 and general government at 0.8504 (specification 11). Schools respond at 1 at both ends.

| (a) Children in their own generation | $bn at the union's low end (shared) | $bn at the union's high end (personal) | Own range over the 64 specifications, $bn | $ per member, low / high | $ per adult, low / high |
|---|---|---|---|---|---|
| G1, born in Mexico | 77.6 | 56.9 | 49.3–85.4 | 6,354 / 4,657 | 6,651 / 4,875 |
| G2, US-born, a parent born in Mexico | 105.0 | 117.5 | 105.0–117.5 | 7,326 / 8,195 | 11,778 / 13,176 |
| G3+, US-born of US-born parents | 75.8 | 117.6 | 75.8–117.6 | 5,288 / 8,198 | 9,268 / 14,369 |
| All three (the case) | 258.5 | 292.0 | 258.5–292.0 | 6,321 / 7,139 | 8,984 / 10,147 |

| (b) Minors with their parents (NAS 2017) | $bn at the union's low end (shared) | $bn at the union's high end (personal) | Own range over the 64 specifications, $bn | $ per member, low / high | $ per adult, low / high |
|---|---|---|---|---|---|
| G1 | 135.6 | 155.4 | 135.6–155.4 | 8,043 / 9,218 | 11,612 / 13,309 |
| G2 | 67.9 | 66.1 | 60.9–73.0 | 5,562 / 5,411 | 7,617 / 7,410 |
| G3+ | 55.0 | 70.5 | 55.0–70.5 | 4,650 / 5,960 | 6,723 / 8,617 |

Members and adults do not change with the case: 40.90m and 28.77m in all. [CALCULATION:
`run_generations.cjs` → `derived/generation_results.csv`]

**From September 24, through the one-year scenario, to this case.** The move is a chain at matched
specifications,
and its parts add exactly, within 5.7e-14bn, for every generation and the union
(`generation_summary.json` → `change_from_sept24`, `change_from_sept26`):
- The finite-removal responses, row 8 and the consumption key reach the September 26 case at the
  September 24 ends. Those are specifications 56 and 7, which are also the September 26 ends.
- "Schools at full cost" raises the school response from 0.6522/0.6813 to 1 at the same
  specifications.
- "Band end moves" takes the schools case from those specifications to its own ends, 48 and 11. At a
  school response of 1 the school-share bound flips: 0.865 → 0.715 at the low end and 0.715 → 0.865
  at the high end.

The union's last two parts add to +$57.57bn / +$46.26bn. That is the schools lane's own change from
September 26, read from its `summary.json` (gate).

| $bn, low / high | Sept 24 | General government | Schools, finite removal | Row 8 at 0.949 | Consumption key | **Sept 26** | Schools at full cost | Band end moves | **Schools case** | Move |
|---|---|---|---|---|---|---|---|---|---|---|
| (a) G1 | 63.79 / 53.56 | +0.13 / +0.14 | +0.89 / +0.26 | −0.03 / −0.03 | −0.93 / −0.93 | **63.85 / 52.99** | +13.98 / +3.88 | −0.18 / +0.04 | **77.65 / 56.91** | +13.85 / +3.35 |
| (a) G2 | 81.74 / 95.12 | +0.17 / +0.18 | +1.48 / +1.44 | −0.04 / −0.04 | −1.23 / −1.23 | **82.12 / 95.47** | +23.20 / +21.58 | −0.32 / +0.41 | **105.00 / 117.46** | +23.26 / +22.34 |
| (a) G3+ | 55.34 / 97.64 | +0.17 / +0.18 | +1.35 / +1.34 | −0.04 / −0.04 | −1.89 / −1.89 | **54.95 / 97.23** | +21.18 / +19.98 | −0.29 / +0.37 | **75.84 / 117.58** | +20.50 / +19.95 |
| (b) G1 | 110.22 / 134.76 | +0.19 / +0.19 | +1.61 / +1.35 | −0.04 / −0.04 | −1.36 / −1.36 | **110.62 / 134.90** | +25.29 / +20.11 | −0.35 / +0.37 | **135.56 / 155.38** | +25.34 / +20.62 |
| (b) G2 | 50.18 / 52.96 | +0.15 / +0.15 | +1.12 / +0.85 | −0.03 / −0.03 | −0.77 / −0.77 | **50.64 / 53.16** | +17.50 / +12.68 | −0.24 / +0.22 | **67.90 / 66.06** | +17.72 / +13.10 |
| (b) G3+ | 40.47 / 58.60 | +0.14 / +0.15 | +0.99 / +0.85 | −0.03 / −0.03 | −1.92 / −1.92 | **39.66 / 57.64** | +15.57 / +12.65 | −0.20 / +0.22 | **55.02 / 70.52** | +14.55 / +11.92 |
| Union | 200.88 / 246.32 | +0.47 / +0.49 | +3.72 / +3.04 | −0.10 / −0.10 | −4.05 / −4.05 | **200.92 / 245.69** | +58.36 / +45.44 | −0.79 / +0.81 | **258.49 / 291.95** | +57.61 / +45.64 |

The responses are engine state, so each generation's model responds on its own lines. They come from
the package's `MAIN_SPECS`, gated against `corrections.json` → `meta.responses`. Row 8's change splits
as the lane splits row 8, by population.

**The school line by generation.** "School line in the case" is what the case charges each generation
for schools at the union's range end: its cost at a school response of 1 less its cost at 0
(`school_line_bn`). A generation's share of the line equals its share of "Schools at full cost",
because both scale the same school costs under the same allocation.

| $bn, low / high | Schools at full cost | Its share of the union's | School line in the case | Its share |
|---|---|---|---|---|
| (a) G1 | +13.98 / +3.88 | 24% / 9% | 33.22 / 14.74 | 24% / 9% |
| (a) G2 | +23.20 / +21.58 | 40% / 47% | 55.15 / 81.90 | 40% / 47% |
| (a) G3+ | +21.18 / +19.98 | 36% / 44% | 50.36 / 75.84 | 36% / 44% |
| (b) G1 | +25.29 / +20.11 | 43% / 44% | 60.13 / 76.34 | 43% / 44% |
| (b) G2 | +17.50 / +12.68 | 30% / 28% | 41.60 / 48.11 | 30% / 28% |
| (b) G3+ | +15.57 / +12.65 | 27% / 28% | 37.00 / 48.02 | 27% / 28% |
| Union | +58.36 / +45.44 | 100% / 100% | 138.73 / 172.47 | 100% / 100% |

Under (a) the line falls on the generations that hold the pupils, the second and third-plus. At the
shared low end, parents carry part of it through the SPM unit's equal split, so the Mexico-born take
24% there against 9% at the personal high end. Under (b) minors count with their parents, and the
first generation takes 43–44%. [FRAMING-SENSITIVE]

**Tied band ends.** At a school response of 1 the growth and decline specifications coincide. All 32
pairs are identical, and their costs are equal (`===`) for the union and every generation. The low end
is attained at specifications 48 and 52 and the high end at 11 and 15. `indexOf` takes the first of
each, 48 and 11, which carry the growth index (gate; `generation_summary.json` → `band_end_ties`).

**The consumption key, split exactly.** The consumption lane's CPS frame matches this one person for
person: the same records, all 161 weights and the generation masks (gate). `consumption_split.py`
recomputes each generation's key with the lane's saving ratio and corridor outflow. From the
generation totals it rebuilds the lane's 40 union edits with a maximum difference of 0.0. At the
union's stack factor, the group pays $9.30bn more from saving and $5.24bn less from remittances:

| $bn of receipts, at the union's stack factor | Saving | Remittances | Net | Key share: old → corrected |
|---|---|---|---|---|
| (a) G1 | +4.37 | −3.03 | +1.34 | 2.204% → 2.377% |
| (a) G2 | +2.91 | −1.87 | +1.04 | 2.654% → 2.798% |
| (a) G3+ | +2.02 | −0.34 | +1.67 | 3.246% → 3.423% |

The lane's rule for every ratio-type correction then applies. Each generation's saving part takes its
own stack factor on the consumption key (0.85, 0.98 and 0.99 under (a), against the union's 0.9497).
The corridor's dollars are not scaled, and the $0.31bn remainder goes to the generations in proportion
to their consumption-tax cells after the stack. Cells with no main-case weight take the union's edit
times the generation's share of the change in the key share. [CALCULATION: `consumption_split.py` →
`derived/consumption_key_by_generation.json`]

| Consumption key, $bn of cost | Own factor (central) | Union's factor | Old key's shares (brief's fallback) |
|---|---|---|---|
| (a) G1 / G2 / G3+ | −0.93 / −1.23 / −1.89 | −1.34 / −1.04 / −1.67 | −1.10 / −1.33 / −1.62 |
| (b) G1 / G2 / G3+ | −1.36 / −0.77 / −1.92 | −1.72 / −0.61 / −1.72 | −1.39 / −1.25 / −1.40 |

Both alternatives run as sensitivities: the union's factor inside `stack_scaling_by_union_factor`, and
the old key's shares as `consumption_key_by_old_key_shares`. The saving ratio comes from income rank
alone. CE has no parents' birthplace, so the ratio cannot differ by generation at the same income.

**Other figures, updated** (the one-year scenario in brackets):
- Moving minors to their parents' generation shifts $58–98bn onto the first generation ($47–82bn).
- Under (a), the household allocation rule shifts $28–36bn between the first and third-plus
  generations ($20–32bn).
- The eight alternative split rules (the seven in the September 24 record plus the old key's shares)
  move no generation by more than $3.7bn, and none turns a cost negative. The largest is still the
  literal fill-in rule.
- Under (b), a second-generation adult with their minor children costs others 56–66% of what a
  Mexico-born adult does (52–60%).
- Against the uncorrected model at the case's responses, the corrections move (a) G1 by +$4.8 / +4.1bn,
  G2 by −$5.9 / −7.5bn and G3+ by −$6.1 / −3.4bn. They move (b) G1 by −$2.0 / −2.3bn, G2 by
  −$3.5 / −3.6bn and G3+ by −$1.7 / −0.8bn.
- At the shared end the account gives −$6,354, −$7,326 and −$5,288 per person (−$5,225, −$5,729 and
  −$3,831), against the September 19 ledger's own balances of −$5,929, −$5,881 and −$4,223. With
  schools and other education at average cost, the main profile's marginal responses take off only
  the delayed services (economic affairs, recreation and culture at zero response), $967–1,172 per
  person. So the direct lines at the responses sit $751–2,025 below the ledger's balances; in the
  one-year scenario they differ from them by $175–400. At the low end the corrections add $396 per
  person to the first generation and take $411 and $422 from the second and third-plus ($414, $382
  and $423). Under the personal allocation, G3+ and G2 are within $3 per person of each other.
  [CALCULATION: `compare_ledger.py` → `derived/ledger_comparison.csv`]

**Gates.** Both full runs pass every gate (192 gate lines each), and the second run is byte-identical
to the first in all 20 derived files.
- The corrected union reproduces $258.4885–291.9548bn, and the uncorrected union reproduces
  $265.5903–298.6797bn. These are the rows `adopted` and `uncorrected_at_adopted_responses` of the
  schools lane's `main_case_bands.csv` (1e-4).
- The three generations add to the union in all 64 specifications under both conventions: 1.4e-12bn
  corrected, 1.1e-13bn uncorrected.
- The netted generation edits add to `corrections.json` in all 270 cells (1.4e-12bn). The payload is
  the package's (deep-equal), and its edits are the September 26 payload's.
- The specifications carry `meta.responses`: general government 0.6000/0.8504, schools 1/1.
- The chain's parts add to each move (5.7e-14bn), and the generations' parts add to the union's part by
  part (1.6e-12bn). The union's last two parts equal the schools lane's change (1.1e-13bn), and the
  band ends tie exactly.
- `--case sept26` reproduces the four outputs of its 2026-09-26 run byte for byte, and `--case sept24`
  those of ba12f3c.

**Reproduce.** `bash run_all.sh` runs every step and ends with `main_case_2026_09_26/main_case.cjs`
and `main_case_schools_full_2026_09_26/main_case.cjs`. For the other cases, run
`node run_generations.cjs --case sept26|sept24 --out-dir DIR`, then `compare_ledger.py --out-dir DIR`.
Headline cell: `derived/generation_results.csv`, row `a,G1,low`, `cost_bn` 77.645780.

## September 26 case (the one-year scenario since 22:39)

Earlier on 2026-09-26 the operator adopted the September 26 case (`main_case_2026_09_26`,
$200.9180–245.6949bn). It is the September 24 package with finite-removal responses and the
consumption key. Since the 22:39 adoption of schools at full cost it is the one-year scenario, which
answers how next year's budget would move. `node run_generations.cjs --case sept26 --out-dir DIR`
reproduces its four outputs byte for byte. Headline cell: row `a,G1,low`, `cost_bn` 63.851595.

The union's range ends are the September 24 specifications with the responses replaced. The low end
is the shared allocation with general government at 0.6000 and schools at 0.6522 (specification 56).
The high end is the personal allocation with 0.8504 and 0.6813 (specification 7).

| (a) Children in their own generation | $bn at the union's low end (shared) | $bn at the union's high end (personal) | Own range over the 64 specifications, $bn | $ per member, low / high | $ per adult, low / high |
|---|---|---|---|---|---|
| G1, born in Mexico | 63.9 | 53.0 | 44.2–74.6 | 5,225 / 4,336 | 5,469 / 4,539 |
| G2, US-born, a parent born in Mexico | 82.1 | 95.5 | 82.1–95.5 | 5,729 / 6,661 | 9,212 / 10,710 |
| G3+, US-born of US-born parents | 54.9 | 97.2 | 54.9–97.2 | 3,831 / 6,779 | 6,714 / 11,881 |
| All three (the case) | 200.9 | 245.7 | 200.9–245.7 | 4,913 / 6,008 | 6,983 / 8,539 |

| (b) Minors with their parents (NAS 2017) | $bn at the union's low end (shared) | $bn at the union's high end (personal) | Own range over the 64 specifications, $bn | $ per member, low / high | $ per adult, low / high |
|---|---|---|---|---|---|
| G1 | 110.6 | 134.9 | 110.6–134.9 | 6,563 / 8,003 | 9,475 / 11,555 |
| G2 | 50.6 | 53.2 | 44.4–59.6 | 4,148 / 4,354 | 5,681 / 5,963 |
| G3+ | 39.7 | 57.6 | 39.7–57.6 | 3,352 / 4,872 | 4,846 / 7,044 |

**What moved from September 24**, $bn a year at the low / high end (`change_from_sept24`; the parts add
within 5.7e-14bn):

| $bn, low / high | General government response | School response | Row 8 at 0.949 | Consumption key | Total move |
|---|---|---|---|---|---|
| (a) G1 | +0.13 / +0.14 | +0.89 / +0.26 | −0.03 / −0.03 | −0.93 / −0.93 | +0.06 / −0.57 |
| (a) G2 | +0.17 / +0.18 | +1.48 / +1.44 | −0.04 / −0.04 | −1.23 / −1.23 | +0.38 / +0.35 |
| (a) G3+ | +0.17 / +0.18 | +1.35 / +1.34 | −0.04 / −0.04 | −1.89 / −1.89 | −0.40 / −0.41 |
| (b) G1 | +0.19 / +0.19 | +1.61 / +1.35 | −0.04 / −0.04 | −1.36 / −1.36 | +0.40 / +0.14 |
| (b) G2 | +0.15 / +0.15 | +1.12 / +0.85 | −0.03 / −0.03 | −0.77 / −0.77 | +0.46 / +0.20 |
| (b) G3+ | +0.14 / +0.15 | +0.99 / +0.85 | −0.03 / −0.03 | −1.92 / −1.92 | −0.81 / −0.96 |
| Union | +0.47 / +0.49 | +3.72 / +3.04 | −0.10 / −0.10 | −4.05 / −4.05 | +0.04 / −0.62 |

The school response falls where the pupils are, as in the schools case. The consumption key splits
exactly as described above.

**Other figures in this case.**
- Moving minors to their parents' generation shifts $47–82bn onto the first generation.
- Under (a), the household allocation rule shifts $20–32bn between the first and third-plus
  generations.
- The eight alternative split rules move no generation by more than $3.7bn.
- Under (b), a second-generation adult costs others 52–60% of what a Mexico-born adult does.
- At the shared end, the case gives −$5,225, −$5,729 and −$3,831 per person against the ledger's own
  balances.
- The corrections add $414 per person to the first generation and take $382 and $423 from the second
  and third-plus.

## September 24 record (superseded 2026-09-26)

**September 24 verdict:** Split by generation, the adopted main case ($200.9–246.3bn a year) leaves all three
Mexican-origin generations as net costs to other US residents. That holds at every one of the main
case's 64 specifications and under both ways of counting children. Where children are counted
decides the order. Counted in their own generation, the Mexico-born cost others $54–64bn a year
($4.4–5.2k per member), the US-born second generation $82–95bn ($5.7–6.6k) and the third-plus
$55–98bn ($3.9–6.8k). Counted with their parents, as the
National Academies count them, the Mexico-born cost $110–135bn ($9.4–11.5k per adult), the second
generation $50–53bn ($5.6–5.9k per adult) and the third-plus $40–59bn ($4.9–7.2k per adult).
[FRAMING-SENSITIVE] [CALCULATION: `run_generations.cjs` → `derived/generation_summary.json`]

Moving minors to their parents' generation shifts $46–81bn onto the first generation. Under
convention (a), the household allocation rule shifts $19–32bn between the first and third-plus
generations. The alternative split rules for the 270 corrections, run at the two ends, move no
generation by more than $3.7bn, and none turns a generation's cost negative. Compared with the
September 19 ledger, its gaps (−$7,584, −$7,521 and −$6,195 per person) are measured against
third-plus non-Hispanic whites, who are net contributors at these ages. The groups' own balances in
that ledger (−$5,929, −$5,881 and −$4,223) are close to this account's −$5,220, −$5,703 and −$3,859
under the same allocation. They get there through offsetting differences, so the closeness validates
neither. This is one year's account of the people alive in 2024. It cannot say what today's children
will pay as adults.

Lane: `infra/immigration-fiscal/generation_account_2026_09_24/`, brief [BRIEF.md](BRIEF.md),
2026-09-24/25. Model self-report: `claude-opus-5-5[1m]`. Not committed (the parent re-runs and
commits). No shared module needed a change, and no other lane was written.

## Results

These figures are the net cost to other US residents in $bn a year for income year 2024, at the two
ends of the adopted main case:

- **Low end:** shared allocation, GDP normalization, school share 0.865 at response 0.63, general
  government 0.59 and low uncompensated care.
- **High end:** personal allocation, cash normalization, school share 0.715 at response 0.66,
  general government 0.84 and high uncompensated care.

They are model output: CPS allocations are measured, while service responses and the production term
are assumed. Per member divides by the people counted in the generation under the chosen convention.
Per adult divides by those aged 18 and over. The own range is the generation's lowest and highest
cost over the 64 specifications.

| (a) Children in their own generation | Members (m) | Adults (m) | $bn, low end | $bn, high end | Own range, $bn | $ per member, low / high | $ per adult, low / high |
|---|---|---|---|---|---|---|---|
| G1, born in Mexico | 12.22 | 11.67 | 63.8 | 53.6 | 44.7–74.8 | 5,220 / 4,383 | 5,464 / 4,588 |
| G2, US-born, a parent born in Mexico | 14.33 | 8.91 | 81.7 | 95.1 | 81.7–95.1 | 5,703 / 6,636 | 9,169 / 10,670 |
| G3+, US-born of US-born parents | 14.34 | 8.18 | 55.3 | 97.6 | 55.3–97.6 | 3,859 / 6,808 | 6,763 / 11,931 |
| All three (the adopted main case) | 40.90 | 28.77 | 200.9 | 246.3 | 200.9–246.3 | 4,912 / 6,023 | 6,981 / 8,561 |

| (b) Minors with their parents (NAS 2017) | Members (m) | Adults (m) | $bn, low end | $bn, high end | Own range, $bn | $ per member, low / high | $ per adult, low / high |
|---|---|---|---|---|---|---|---|
| G1 | 16.86 | 11.67 | 110.2 | 134.8 | 110.2–134.8 | 6,539 / 7,995 | 9,441 / 11,543 |
| G2 | 12.21 | 8.91 | 50.2 | 53.0 | 44.0–59.3 | 4,110 / 4,338 | 5,629 / 5,941 |
| G3+ | 11.83 | 8.18 | 40.5 | 58.6 | 40.5–58.6 | 3,420 / 4,952 | 4,945 / 7,160 |

[CALCULATION: `run_generations.cjs` → `derived/generation_results.csv`] At every specification and
under both conventions, the three generations add to the adopted main case to within $1.5e-12bn;
the brief's gate is $0.01bn.

Per adult under (a) is not a per-parent figure. It divides children's costs by the adults of another
generation: 5.4m of the second generation are minors, and 4.3m of them count with a Mexico-born
parent under (b). [DATA: `mixed_units.py` → `derived/minors_convention_b.csv`] Under (b),
a second-generation adult, with their minor children, costs others 51–60% of what a Mexico-born adult
does. The third-plus cost less than the second generation at the low end and more at the high end.
None of these figures is age-standardized. Second-generation adults average 34.7 years, against 40.8
for the third-plus and 48.2 for the Mexico-born. [DATA: `mixed_units.py` → `derived/mixed_units.csv`]

**The household allocation rule matters as much as the convention for the third-plus.** The shared
rule splits every key equally within the SPM unit (`cps_imputation_keys_2026_09_23/common.py`
`unit_equal`). Parents therefore carry part of their children's costs even under (a). Units that
include people outside the union also pass costs and taxes across its boundary. In the table below,
each end keeps its other settings and only the allocation changes. [FRAMING-SENSITIVE]

| $bn a year | Low end (shared) | Low end, personal instead | High end (personal) | High end, shared instead |
|---|---|---|---|---|
| (a) G1 | 63.8 | 44.7 | 53.6 | 74.8 |
| (a) G2 | 81.7 | 82.6 | 95.1 | 93.0 |
| (a) G3+ | 55.3 | 86.1 | 97.6 | 65.6 |
| (b) G1 | 110.2 | 119.2 | 134.8 | 125.5 |
| (b) G2 | 50.2 | 44.0 | 53.0 | 59.3 |
| (b) G3+ | 40.5 | 50.2 | 58.6 | 48.6 |

[CALCULATION: `run_generations.cjs` → `generation_summary.json` `allocation_swap`] Of third-plus
members, 36% live in an SPM unit with someone outside the union (41% of third-plus minors). The
figures are 18% for the second generation and 10% for the first. On average, 13% of a third-plus
member's unit lies outside the union. Under the shared rule these members take in part of those
people's taxes, and under the personal rule they carry their own costs in full.
[DATA: `mixed_units.py` → `derived/mixed_units.csv`]

**What the corrections do by generation.** Relative to the September 23 case at the same
specifications, under (a):

- The corrections raise the first generation's cost by $6.0bn (low end) and $4.3bn (high end).
- They lower the second generation's by $4.2bn and $6.1bn, and the third-plus's by $4.2bn and $1.6bn.

Under (b), they move the first generation by only +$0.4bn and −$0.7bn. The children's shares of the
premium-credit re-key and pooled medical join their parents' there, and the resulting −$9–10bn and
−$6.3bn offset the tax-records stack's +$16–18bn. [CALCULATION: `generation_summary.json` `lanes`]

## Plan and gate status

| Step | What | Gate | Status |
|---|---|---|---|
| 0 | Generation masks on the account's frame; how the CPS records parents' birthplaces | counts equal `generation_split_2026_09_20/derived/cps_generation_split.csv` | **passed** (`test_masks.py`, 3 tests) |
| 1 | Every allocation key restricted to each generation, both allocations | three generations sum to the group's key total, 1e-9 relative | **passed** (`keys.py`: 30 receipt and 52 spending keys, plus the education, owner-property, federal-gap, justice-use and uninsured-use keys) |
| 2 | `derived/model_G1.json`, `model_G2.json`, `model_G3plus.json`, plus `model_b_*` for (b) | summed line by line, they reproduce `model.json` | **passed** (`build_models.py`: every cell to 5.7e-14 bn and the production arrays to 1.1e-13 bn, both conventions) |
| 3 | Production term P and F by generation, as a first-order attribution | three sum to the group's in all 3,888 scenarios | **passed** (`production.py`: 1.1e-13 bn) |
| 4 | The 270 correction edits split by generation, one written rule per source lane | split edits sum to `corrections.json` | **passed** (`stack_split.py`, `external_split.py`, `correction_rules.py`; every lane's union figure is rebuilt from its own outputs, and the netted generation edits add to all 270 cells to 1.4e-12 bn under both conventions) |
| 5 | Engine per generation over `MAIN_SPECS`, conventions (a) and (b) | three sum to the main case at every specification, $0.01bn; linearity | **passed** (`run_generations.cjs`: the corrected union reproduces $200.8752–246.3184bn; the generations add to 1.5e-12 bn corrected and 1.4e-13 bn uncorrected, in all 64 specifications and both conventions) |
| 6 | Comparison with the September 19 ledger | ledger read through its own loader; same populations; eight-band gaps within 2% of the published ones | **passed** (`compare_ledger.py`) |
| — | `node ../main_case_2026_09_24/main_case.cjs` | still passes; lane unchanged | **passed** (last step of `run_all.sh`; `git status` on that lane is clean) |

A full rebuild with `run_all.sh` passed every gate and rewrote all 19 derived files byte for byte.

## Step 4: how each correction is split

The union column gives each source lane's contribution, including the package's stack-factor
interaction, so the rows add to the correction: −$2.33bn at the low end and −$3.32bn at the high end.
They differ from the package's "alone" figures, which leave that interaction out. "Exact" means the
lane's own computation was re-run for each generation.

| Source lane | Union, $bn low / high | Rule | Kind |
|---|---|---|---|
| Tax-records stack: status rules, the state-aware status flag, ACS row-4 weights, Census fill-ins | +19.9 / +21.2 | The CPS lane's own functions, with each generation's mask in place of the union's; ten hot-deck runs (five seeds, union-matched and pooled-donor), each reproducing the lane's stored shares to 3e-15 | exact |
| CBO incidence and category re-key | +9.3 / +8.4 | Each generation's share of the re-keyed receipt keys (the external lane's CBO arm) | exact |
| Treasury OTA income-tax key (outside checks) | −0.4 / −0.3 | The same with the OTA arm and the SSN rule, which splits by each generation's income position | exact |
| Premium credits keyed as EITC (audit row 1) | −14.2 / −14.2 | The audit's formula (credits × pool fraction × (Marketplace share − credit share)) per generation | exact |
| Pooled MEPS medical and long-term care | −16.8 / −16.8 | Medical: the lane's age × US-birth cell ratios on each generation's own cells. LTSS: by the users' generation | medical exact; LTSS users partly inferred |
| Schools priced where enrolled, college line (row 6) | +0.7 / −0.5 | Each generation's own pupils (school key) and students (postsecondary key) | the brief's rule |
| Administrative benefit keys | +2.2 / +2.0 | As each line's uncorrected key splits | flagged |
| Justice booking factor and audit row 7 | +2.0 / +2.0 | As the arrest-keyed parts of the use key split (like custody) | flagged |
| Lane constants: rows 8–10, small items, shelter, care work | −5.1 / −5.1 | Row 8 and small items by population; row 9 as the Medicaid and Medicare keys; row 10 as the WIC key; shelter by use to recent arrivals (G1) net of the keyed charge; care work by the workers' generation | shelter and care by the brief's rule; rows 9–10 and small items flagged |

[CALCULATION: `correction_rules.py` → `derived/correction_rules.json`; `stack_split.py` →
`derived/stack_by_generation.json`; `external_split.py` → `derived/external_by_generation.json`]

**Where the exact split departs from the brief's literal wording.** The brief assigns status-based
corrections to "the first generation, or its unauthorized subset". The exact re-run agrees on who
triggers them. It then spreads their effect as each allocation does: under the shared rule, a
Mexico-born worker's taxes are split with the unit's US-born children. The brief assigns Census
fill-ins "by the generation make-up of the imputed records". The exact re-run measures each
generation's change in key share under the fill-in method, where the literal rule would split by
imputed dollars. Both literal rules are run as sensitivities below.

Within the pooled medical correction, the long-term-care rule takes the Mexico-born share of users
from ACS 2024 proxy populations in each TAF age group. The US-born part is split as the union's
Medicaid enrollees are in the CPS. [INFERENCE: the ACS has no parents' birthplace.] The college part
of row 6 moves 18–23% of the education line onto the postsecondary key. Under the personal
allocation and (a), the first generation holds 29.0% of that key but only 5.6% of the school key.
That is why education adds $3.6bn to the first generation at the high end. [DATA:
`derived/generation_key_shares.json`]

**Sensitivities of the flagged and literal rules** ($bn a year; central, then the lowest and highest
of seven alternatives):

- benefits all to G1;
- benefits all to the US-born;
- justice per adult;
- foster care by children;
- the status rules all to G1;
- fill-ins by imputed dollars;
- stack scaling by the union's factor.

| | (a) low end | (a) high end | (b) low end | (b) high end |
|---|---|---|---|---|
| G1 | 63.8 (60.7–65.5) | 53.6 (50.3–54.9) | 110.2 (107.2–111.6) | 134.8 (131.8–135.9) |
| G2 | 81.7 (80.2–83.7) | 95.1 (94.4–98.8) | 50.2 (48.8–53.3) | 53.0 (52.3–56.5) |
| G3+ | 55.3 (54.5–56.5) | 97.6 (97.1–98.1) | 40.5 (39.9–40.9) | 58.6 (58.0–59.1) |

[CALCULATION: `generation_summary.json` `sensitivities`] The most influential alternative is the
literal fill-in rule. It lowers the first generation's cost by $2.9–3.3bn and raises the second's by
$2.0–3.7bn. I keep the exact split because it is the change the fill-in method actually makes to each
generation's key share. On the evidence-symmetry rule 4, the lean of the central rules is mixed.
Under (a), at the low end, five of the seven alternatives would raise the first generation's cost (by
up to $1.7bn) and two would lower it (by up to $3.1bn). At the high end the count is four and three.
Under (b) it is four and three at the low end and three and four at the high end. The central rules
sit inside every band.
The ratio-type lanes are scaled by each generation's own stack factor. That leaves a non-additive
remainder of at most $0.43bn, which is spread by the generations' cells after the stack.

**Lane contributions by generation**, $bn a year, low / high:

| Lane | (a) G1 | (a) G2 | (a) G3+ | (b) G1 | (b) G2 | (b) G3+ |
|---|---|---|---|---|---|---|
| Tax-records stack | +15.1 / +18.1 | +2.6 / −0.2 | +2.2 / +3.2 | +16.1 / +18.2 | +1.3 / −0.2 | +2.5 / +3.2 |
| CBO re-key | +1.1 / +1.0 | +5.1 / +3.9 | +3.0 / +3.5 | +1.6 / +0.7 | +3.9 / +4.0 | +3.9 / +3.6 |
| OTA re-key | −0.1 / −0.1 | −0.2 / −0.1 | −0.1 / −0.1 | −0.1 / −0.1 | −0.2 / −0.1 | −0.1 / −0.1 |
| Premium credits (row 1) | −4.0 / −11.4 | −6.5 / −2.2 | −3.7 / −0.6 | −8.9 / −10.3 | −3.5 / −2.9 | −1.8 / −1.0 |
| Pooled medical and LTSS | −5.5 / −5.5 | −5.3 / −5.3 | −6.1 / −6.1 | −6.3 / −6.3 | −5.1 / −5.1 | −5.4 / −5.4 |
| Schools and college | +1.0 / +3.6 | −0.6 / −2.6 | +0.3 / −1.5 | −0.5 / −1.3 | +0.3 / +0.4 | +0.9 / +0.4 |
| Benefit keys | +0.5 / +0.7 | +0.9 / +0.8 | +0.8 / +0.6 | +0.7 / +0.7 | +0.9 / +0.8 | +0.6 / +0.5 |
| Justice | +0.5 / +0.5 | +0.8 / +0.8 | +0.7 / +0.7 | +0.5 / +0.5 | +0.8 / +0.8 | +0.7 / +0.7 |
| Lane constants | −2.6 / −2.6 | −1.1 / −1.1 | −1.3 / −1.4 | −2.8 / −2.8 | −1.1 / −1.1 | −1.2 / −1.2 |
| Total correction | +6.0 / +4.3 | −4.2 / −6.1 | −4.2 / −1.6 | +0.4 / −0.7 | −2.7 / −3.4 | −0.0 / +0.7 |

The CPS lane prints `[DEGRADED] impute_status: Medicaid clause …` whenever its status function runs.
The warning describes the uncorrected status rule. The adopted stack's state-aware flag is its
repair, and this split carries that flag by generation.

## Step 6: the September 19 ledger beside the account

The ledger's groups keep children in their own generation, so they match convention (a). Their
populations equal this lane's to the person; the ledger and this lane use the same CPS ASEC 2025
frame. Every figure below is a net balance in $ per person a year (negative means the group costs
others). Each row is computed in its own object, and nothing is scaled from one object onto the other.
[CALCULATION: `compare_ledger.py` → `derived/ledger_comparison.csv`; the ledger is read through
`lifetime.load_age_profiles`, which verifies its hashes]

| $ per person a year | G1 shared | G2 shared | G3+ shared | G1 personal | G2 personal | G3+ personal |
|---|---|---|---|---|---|---|
| Ledger: published gap to third-plus NH whites, at the whites' ages | −7,584 | −7,521 | −6,195 | — | — | — |
| Ledger: the same gap from its eight age bands | −7,525 | −7,443 | −6,116 | −7,830 | −6,799 | −6,018 |
| Ledger: gap at the group's own ages | −9,806 | −9,820 | −6,685 | −12,394 | −6,166 | −4,598 |
| Ledger: the whites' own balance at the group's ages | +3,877 | +3,940 | +2,461 | +8,963 | −633 | −2,365 |
| Ledger: the group's own balance | −5,929 | −5,881 | −4,223 | −3,431 | −6,798 | −6,963 |
| Account: direct lines at average cost, before corrections | −7,635 | −8,882 | −7,015 | −5,751 | −9,804 | −9,689 |
| Account: the same lines at the adopted responses | −5,448 | −6,165 | −4,294 | −4,505 | −7,171 | −7,014 |
| Account: plus the production term (September 23 case) | −4,726 | −5,996 | −4,149 | −4,028 | −7,059 | −6,919 |
| Account: plus the corrections (adopted main case) | −5,220 | −5,703 | −3,859 | −4,383 | −6,636 | −6,808 |

The published gaps come from the shared allocation, and the eight-band recomputation lands within
0.8–1.3% of them.

- **Reference group.** The published figure is a gap to third-plus non-Hispanic whites, weighted to
  the whites' ages. At the Mexican-origin groups' own ages, those whites are net contributors under
  the shared allocation: +$2.5k to +$3.9k per person. A gap therefore exceeds the group's own
  balance. The groups' own balances are 22–32% smaller than the published gaps. Age weighting moves
  the gap too. Under the shared allocation it is larger at the groups' own ages than at the whites'.
- **Object.** The ledger charges services at average cost, charges pure public goods nothing and has
  no production term. The account differs in its line set, receipt rules and keys. At average
  cost (the package's proportional reference), it charges these people $1.7k to $3.0k per person more
  than the ledger. Pricing services at the adopted marginal responses then takes off $2.2k to $2.7k
  at the shared end ($1.2k to $2.7k at the personal end). That brings the direct lines to within
  $71–481 per person of the ledger's balance at the shared end. The first of these two differences
  is not decomposed here, so the near-agreement confirms neither object. The production term takes
  off a further $722, $169 and $144 per person at the low end.
- **Corrections.** The ledger carries none of the 270 corrections. At the low end they add $494 per
  person to the first generation and take $293 and $291 from the second and third-plus.
- **Order.** Both objects put the third-plus lowest under the shared allocation and the first
  generation lowest under the personal one. Under shared, the ledger has the first and second
  generations within $50 of each other, while the account puts the second $480 above the first.
  Under personal, both put G3+ about $170 above G2, with G1 well below.

The ledger answers how a group compares with third-plus whites of the same age. This split answers
what each generation alive in 2024 costs everyone else under the adopted account. Neither is a test
of "their children pay it back", which concerns future taxes and needs a cohort account with the
corrections carried into it. [INFERENCE] The FAQ rule holds here: the ledger's generation gaps must
not be scaled onto the $201–246bn, and this lane computes the split directly on the account.

## Sources and method notes

**National Academies convention (step 5b).** Verified in the local copy of the report
(`sources/immigration-fiscal/data/external/nas_2016/23550.pdf`), chapter 8, printed pages 387–388:
"The first group consists of first generation immigrants (the foreign-born) ages 18 and older, plus
their dependent first and second generation children (see Box 8-2). The second group consists of
independent individuals (those ages 18 and older) in the second generation plus their dependents
(who typically are third generation by nativity status)." Footnote 12: "For all three groups,
dependent children—identified at the individual level in the CPS data—are included in their
parents' generational group." Page 388: "Dependent children are assigned to the parental generation
if one or more independent parents are present in the household. If there are no parents in the
household, then the generational group of the oldest co-resident independent relative is assigned.
Defining generational groups in this way attributes the costs to governments associated with
dependent children—most notably, in terms of magnitude, public expenditures on education—to the
generation of a parent or relative responsible for raising the child." Footnote 13 assigns a child
whose parents are in different generations at random, half to the mother's generation and half to
the father's. Box 8-2 (printed page 377) defines dependents more widely than minors: anyone under 18,
18–21-year-olds in high school full time, 18–23-year-olds in school with income below half the
one-person poverty level, and some low-income single 18–23-year-olds living with a parent.
[SOURCE: National Academies of Sciences, Engineering, and Medicine (2017), *The Economic and Fiscal
Consequences of Immigration*, pp. 377, 387–388, doi:10.17226/23550]

Convention (b) here follows the brief's wording, minors only. A minor goes to the generation of the
co-resident parents in the union, split 50/50 if they are in two generations. Failing that, the
minor goes to the oldest union adult relative in the family, and otherwise stays in their own
generation. The split 50/50 replaces the NAS random draw with its expectation. Dependents aged 18–23
stay in their own generation, which leaves some college costs with the second generation that NAS
would move to the first. [INFERENCE]

**How the CPS records parents' birthplaces (step 0).** The household roster asks every member "What
is his/her mother's country of birth?" and "... father's country of birth?" (items MNTVT and FNTVT).
The questions are asked in the first month in sample and for members added later. The answers are
reported for the person, not copied from a linked parent record. [SOURCE: Census Bureau, *Current
Population Survey Design and Methodology*, Technical Paper 77 (2019), Table 3-2.5 part 2, p. 123;
ASEC 2025 data dictionary, PEMNTVTY/PEFNTVTY universe "All Persons"]

In the union, 54% of members (75% of adults) live without a linked parent, and their generation rests
on these reported items alone. The items are allocated for 4.8% of those members, against 2.7% of
members who live with a parent. Where a biological parent lives in the household, the member's report
agrees with that parent's own birthplace 96.4% of the time (G1 98.8%, G2 97.0%, G3+ 95.2%).
[CALCULATION: `parents_check.py` → `derived/parent_birthplace_check.csv`] A disagreement rate of at
least 3–5% therefore likely applies to the non-co-resident majority as well, whose answers cannot be
checked. The G2/G3+ boundary carries that error. [INFERENCE] The same mismatch shows under (b): 0.35m
third-plus minors live with a Mexico-born parent, so they count with the first generation.
[DATA: `derived/minors_convention_b.csv`] That parent is a step- or adoptive parent, or the minor's
reported parents' birthplaces disagree with the parent's own. [INFERENCE]

**Production term (step 3).** The account's CES production block is not linear in the union's
labor, so it has no unique generation split. I attribute it along the proportional removal path
(Aumann–Shapley: the path integral splits P and F exactly across the two skill cells). Within each
cell, the split follows each generation's share of the union's positive earnings there. **This is a
first-order attribution, not a counterfactual.** At the model's reference scenario:

| $bn a year, P + F | Union | G1 | G2 | G3+ |
|---|---|---|---|---|
| Attribution, cash normalization (high end), (a) | 8.79 | 5.82 | 1.60 | 1.37 |
| Attribution, GDP normalization (low end), (a) | 13.32 | 8.82 | 2.43 | 2.07 |
| Remove this generation alone, cash (does not add up) | — | 3.69 | 0.25 | 0.18 |
| Split by total labor income, cash | 8.79 | 3.17 | 2.82 | 2.80 |

[CALCULATION: `production.py` → `derived/production_by_generation.json` `reference`] The term is
almost entirely induced receipts: at the cash reference, F is +$8.95bn and P is −$0.16bn. Its positive
part comes from the high-school-or-less cell (+$12.7bn), while the other cell is −$3.9bn. The first
generation earns 53% of the union's labor income in the first cell and 22% in the second, so it
carries two thirds of the term. Removing one generation alone gives much less than its attribution,
because P + F rises faster than linearly in the removed share. Splitting by total labor income would
raise the first generation's cost by $2.7–4.0bn and lower the other two by $1.2–2.2bn each.

## Would change it

- **Flagged rules.** A measured generation split of the flagged corrections, meaning benefit receipt
  and justice use by parents' birthplace, would replace the proportional rules. Each moves a
  generation by $2bn or less.
- **Production term.** A counterfactual production model would replace the first-order attribution.
  The first generation's share runs from $3.2bn (labor-income split, cash) to $8.8bn (attribution,
  GDP).
- **Future taxes.** A cohort account of today's children would be needed to test "their children pay
  it back".
- **Main case.** A change to the main case itself (service responses, the production term) would move
  every generation. The convention and allocation choices stay framing.

## Reproduce

`bash infra/immigration-fiscal/generation_account_2026_09_24/run_all.sh` runs every step in
dependency order, stops at the first failed gate, and ends by re-running
`main_case_2026_09_24/main_case.cjs`. Headline cell: `derived/generation_results.csv`, row `a,G1,low`,
`cost_bn` 63.793787.

The steps can also be run one at a time from the repository root with
`OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>`, in this order: `test_masks.py`
(through `-m pytest … -p no:cacheprovider`), `parents_check.py`, `mixed_units.py`, `keys.py`,
`production.py`, `build_models.py`, `stack_split.py`, `external_split.py` (add `--with openpyxl`),
`correction_rules.py`, `node run_generations.cjs`, `compare_ledger.py`. The scripts set
`sys.dont_write_bytecode`, so they leave no bytecode beside the lanes they import. `_cache/` holds the
CPS frame parquet (ignored); `frame.load()` rebuilds it from the hash-checked ASEC zip.

Covered: every input the brief names, through `model.json`'s reproduction (step 2), and every lane in
`package.cjs` `packageShifts` (step 4). Skipped: none. Derived outputs total 3.7 MB, of which
`production_by_generation.json` (0.9 MB, all 3,888 scenarios) is the largest.
