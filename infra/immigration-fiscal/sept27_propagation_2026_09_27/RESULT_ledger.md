**Verdict:** The real-costs totals and the winners ledger now run the September 27 case, and every earlier
case still reproduces byte for byte. Fiscal and social costs together are **$363–438bn a year** at central
values [2026-09-28, later: $371–446bn with fear, security and schools, rows `social_items_2026_09_28`; [decision](../../../decisions/2026-09-28-social-items-fear-security-schools.md). Later still: $486.8–561.4bn with PM2.5 and road crashes, rows `social_item_*`; [decision](../../../decisions/2026-09-28-social-items-pollution-crashes.md). With the scale benefits (the scale lane's net and restaurant market size, as negative costs): $466.1–540.6bn, full span $270–763bn; [decision](../../../decisions/2026-09-28-social-items-scale-benefits.md). With the crash item on California's measured non-fatal culpability ($42.3bn): $462.6–537.2bn. With volunteering, consumer-side scale and trade ties as further benefits: **$447.5–522.0bn**, $10.9–12.8k per member, full span $224–755bn; [decision](../../../decisions/2026-09-28-social-items-more-benefits.md)] (schools case: $305–350bn), or $8.9–10.7k per group member. About one other resident in six comes out
ahead: 17.8% pooled under tax-share financing and 17.0% under per-person cuts (was 20.5% and 19.0%). The
fiscal channel now has three financing parts. Taxpayers carry $349.3bn at central values, of which $44.7bn is
the return on public capital. The capped programs, $5.1bn, fall on eligible households that go without the
aid. The preferences row is now an attribution under a stated replacement rule. Carrying the rule's gain to
other recipients raises the preferences term in "with proposed" from $0.58bn to $1.55bn. That moves the
with-proposed share ahead by 0.1 point.

# W4 `ledger`, round 2: real-costs totals and the winners ledger on the September 27 case

Date 2026-09-28. Work order: `BRIEF.md` §"Round 2, W4 `ledger`", the parent's message of 2026-09-28 (items
1–4, pins below) and its add-on of the same day (the channel name, capital lines). I stayed in the shared
checkout, as the peer-session hook asked me to state. I made no git writes: no add, commit, stash, checkout
or reset. Everything below is uncommitted for the parent.

## What changed

1. **`sept24_propagation_2026_09_24/`.**
   - `band_variants.cjs`, `real_costs_totals.py` and `constant_choices.py` default to `sept27` and write to
     `sept27_propagation_2026_09_27/derived/`.
   - The congestion item is the long-run re-derivation: $13.99bn at the low band end and $12.02bn at the
     high end, against B1's $19.16bn.
   - Two labelled variants sit outside the central total: the capital return at the reported 7%, and option A
     (no enterprise capital, the enterprise receipt at 0).
   - `constant_choices.py` selects the run's main profile (`summary.json` `case.main_profile`). Both
     constants are cash, so it compares cash to cash and never compounds the capital or displaced columns.
   - `RESULT.md` line 6 and its line-133 twin carry a dated bracket: the joint CPS SE is not a floor (audit
     ffcce20 §A; withdrawn in 796f057).
2. **`winners_losers_2026_09_24/`.** `sept27` is the default. The pins sit beside the old ones:
   `BASE27_COMMIT` 78766c2, `DEBT27_COMMIT` e03450b and `GEN27_COMMIT` 8654a0c. The back-cast (de468f2) is not
   read, since nothing here uses it.
   - **Evaluation.** `specs.cjs` evaluates the case with `evaluateFull`. The capital return, enterprise
     capital included, is part of A. The enterprise surplus receipt is a cash line. Both sit in the fiscal
     channel.
   - **Financing parts.** The fiscal channel is split into the debt lane's three parts, each gated to its own
     columns:
     - `fiscal_cash`, with `future_taxpayers` as its borrowed part;
     - `fiscal_resource`, the capital return, never borrowed;
     - `displaced_beneficiaries`.
     The registry's `fiscal` row is now the taxpayers' channel, A − D + F. Its parts add to it, and
     `fiscal` + `displaced_beneficiaries` + `wages` = `main_case` (gated).
   - **Capped programs (brief item 6).** Rental assistance ($4.53bn) and LIHEAP ($0.56bn) fall on eligible
     non-recipients under both conventions. Keys and amounts come from the distribution lane's `capped_keys()`
     and `case_ends_sept27.json` at 78766c2. The proxies:
     - renter households below 50% of their state's median household income that are not in public or
       subsidized housing (10.27m), after HUD's very-low-income limit (24 CFR 5.603, 982.201(b));
     - households below 150% of the HHS 2024 poverty guideline without energy assistance (17.95m), after 42
       U.S.C. 8624(b)(2)(B) and 89 FR 2961. The statute's 60%-of-state-median alternative is not used.

     TANF-type aid is a block grant and stays in the cash part under the financing conventions.
   - **Congestion.** The channel is re-derived by state from the long-run lane's own arm (its `setup()` and
     `time_cost_arm`, read-only). With no lane cut it reproduces B1's state totals, and it reproduces both
     band ends. The levels are:
     - low: the low end's factorial minimum, $2.01bn;
     - central: the mean of the band ends, $13.01bn;
     - high: the high end's maximum, $30.83bn.

     A uniform lane cut offsets delay where the group is thin. Other residents therefore gain in 18–27 of the
     50 states and DC; at central values that is 22, worth $0.9bn.
   - **Compliance and vending.** Not rerun. Their rows are on other counterfactuals (workers paid on the
     books; California before SB 946), sit in the role table only and do not depend on the case. Neither lane
     has a commit after 2026-09-26 (1d14b54, 1c9b6fe), so `SISTER26_COMMITS` stand.
3. **Preferences (adversarial audit 61b4eac §3).**
   - **Relabel.** The row is now an attribution. The label and note state that a beneficiary share supplies
     neither the policy response nor the replacement allocation.
   - **The stated rule: proportional replacement.** A program's preferred placements scale with its
     eligible pool. Without the group, its seats, jobs and contracts go to the non-preferred pool in the
     producer's own race-neutral proportions, and no other eligible group takes them.
   - **Gains to other included recipients.** The rule's gain to the pool's other members is carried as
     `preferences_group_part_others`. It is the white natives' part × (1 − s) / s, where s is their share of
     the pool. The admissions share is rebuilt from the producer's `calc.py` constants and `ipeds_tiers.csv`;
     it is gated to the logged crossings (1,093 and 4,151) and per-worker losses ($21,887 and $3,018). The
     seven CPS shares are recomputed on this frame and gated to the producer's log. Other members get the same
     loss per worker as white natives [INFERENCE].
   - **DBE premium.** It is reconciled before `with_proposed` adds the row. Since September 27 the fiscal
     channel removes the group's key share of highway spending times its response: 0.0806 × 0.733 at the low
     end and 0.0806 × 1 at the high end, 6.98% at the mean. That part of the Mexican-origin premium is already
     in the account, $2.59m of $37.07m, and is netted. The remaining $34.48m sits on the premium removed with
     the group's firms from the spending that remains, which the account does not see.
     - The premium is paid in construction. The account sees it through consumption of fixed capital and the
       capital return, which in steady state annualize the same price [INFERENCE].
     - Transit and airport contracts are matched at the highway share, not the enterprise key [INFERENCE].
   - **Bound.** Under a fixed-target rule, other eligible groups take the placements and white natives
     recover nothing, so 0 is the white natives' lower bound. Those groups' gain is not computed.
4. **`sept26_propagation_2026_09_26/old_new_lanes.py`.** It reads its pinned commits' files with `git show`
   (table 90c4b23; sept26 e62fccb/f697514; schools 90c4b23/39b854b) instead of the working tree. Its CSV (97
   rows) is byte-identical to the committed one.

**Add-on (parent, 2026-09-28).**
- The capped-program channel is named `displaced_beneficiaries` everywhere: the channel, the registry row, the
  page row and `inputs.json` `capped_programs`.
- `fiscal_lines_band_ends.csv` writes each capital component as a line `capital_<id>` on side
  `capital_return`, with 24 lines at each band end.
  - A gate requires the ids to be the payload's `meta.capital_return.components`, in order.
  - A second gate requires the lines, capital included, to sum to `fiscal_specs.csv` A_bn at every
    specification of each band end (1e-6; observed ≤ 5.7e-14).
  - No total line is written, because the file never had one. The totals stay in `fiscal_specs.csv`
    (`capital_total_bn`, by level and by part). A total line would double count in any line sum and stop the
    world ledger's line classifier.
  - `winners_losers.py` maps `capital_<id>` to the debt lane's `<id>` for the federal split.
- A probe of the world ledger found nothing that stops it:
  - `valuation.py`'s `LINE_CLASS` classifies all 48 capital lines;
  - the lines reproduce A_bn to 3.4e-13;
  - `world_ledger.py`'s gate `fiscal_channel_is_A_less_displaced_plus_F` holds, with gaps of 4.9e-5 and
    3.4e-5 (the fiscal_totals rounding).
  - Its `pins.json` still has `sept27` winners null. After the parent's commit it needs that commit and model
    `adopted_2026_09_27`.

## Old → new: numbers the research record quotes

Old is the schools case. The real-costs memo §7 table keeps its September 23 figures, which the lane still
reproduces exactly (the `sept23` column), so it has no row here.

**Real-costs memo, 2026-09-26 update block.** $bn a year unless noted.
[CALCULATION: `sept27_propagation_2026_09_27/derived/real_costs_totals.csv` against
`sept26_propagation_2026_09_26/derived/real_costs_totals.csv` at HEAD (4e66adb)]

| Quoted | Schools case | Sept 27 | Row (section 7 / 7b) |
|---|---:|---:|---|
| Fiscal and social, the pairing | 305–350 | **363–438** | `hispanic_mixed_group` total (low); `custody` total (high) |
| Full span | 268–383 | **325–474** | `full_span` |
| Per group member ($k) | 7.5–8.6 | **8.9–10.7** | per group member, same rows |
| Low end with the memo's $28.9bn victims | 303 | **361** | `hispanic` total (low) |
| Fiscal row's change since Sept 24 | +57.6 / +45.6 | +120.9 / +141.1 | `custody` fiscal minus the `sept24` column |
| Social items beside the account | 52.5–57.7, "do not depend on the case" | **47.3–50.6**, move with congestion | 7b `costs_only` social items |
| Costs and benefits together | 310–349 | **369–437** | 7b `with_care_and_mobility` |
| … adding the scale net | 296–335 | **355–423** | 7b `adding_scale_net` |
| Costs alone | 315–354 | **373–442** | 7b `costs_only` |
| Variant: capital at 7%, the pairing | — | 448–512 ($10.9–12.5k) | `capital_at_7pct`, outside the central total |
| Variant: option A, the pairing | — | 346–415 ($8.5–10.1k) | `enterprises_out_option_a`, outside the central total |
| Income split: fiscal channel; central total | 276.7; 311.4 | 351.0; 390.8 | not this lane: W1, distribution lane at 78766c2 |
| First-year budget response: total; full span | 248–303; 210–336 | unchanged | the one-year scenario is its own case (`derived/sept26/`, reproduced) |

**Winners memo** (update block, §6, §7). [CALCULATION: `winners_losers_2026_09_24/derived/` against the same
files at fa1bd3a; every value is a row of `sept27_propagation_2026_09_27/derived/old_new_ledger.csv`, or
a ratio of two rows (the state and local share: `fiscal_state_local` over `fiscal`)]

| Quoted | Schools case | Sept 27 | File |
|---|---:|---:|---|
| Share ahead, pooled, (a) / (b) | 20.5% / 19.0% | **17.8% / 17.0%** | `net_shares.csv` |
| Every choice least / most costly, pooled (a) | 27% / 12% | **24% / 11%** | `net_shares.csv` |
| Person count, (a) / (b) | 18.4% / 18.3% | **16.9% / 16.9%** | `net_shares.csv` |
| Fiscal channel, central | $275.0bn, 83% state and local | **$349.3bn** (taxpayers), 85%; plus $5.1bn capped programs | `channels.csv` `fiscal`, `displaced_beneficiaries` |
| Social net on today's residents | −$314.4bn; −$1,063 per other resident | **−$386.6bn; −$1,307** | `net_shares.csv` |
| Behind: California and Texas | 96–98% | **97–99%** | `person_nets_by_cut.csv`, pooled |
| Behind: US-born adults, high school or less | 97–99% | **98–99%** | same |
| Behind: renters | 88–91% | **90–92%** | same |
| Behind: bottom-half deciles | 81% to over 99% | **83% to over 99%** | same |
| Ahead: top decile, (a) / (b) | 36% / 57% | **31% / 55%** | same |
| Ahead: landlords | 43–47% | **37–42%** | same |
| Landlords' pooled net, (a) | −$227 | **−$701** | same |
| §6 Preferences, the group's part | −$0.6bn | **−$0.58bn** white natives; −$0.97bn other recipients | `channels.csv` |
| §7 Debt legacy interest | $30.1–37.9bn | **$30.9–41.6bn** | `inputs.json` `debt` |
| §7 Published fiscal and social: range; equal footing; custody footing | $305–350bn; 305.3–344.0; 311.0–349.7 | **$363–438bn; 363.4–432.2; 369.2–438.0** | `inputs.json` `published_totals` |

**FAQ.**
- Entry 2 quotes nothing from these lanes.
- Entry 4 quotes the omitted benefits: $0.65bn, or $14.6bn with the scale net. Both are unchanged (0.655 /
  14.582, `real_costs_totals.csv` 7b). Their share of the main case falls from 0.22–5.6% to 0.17–4.5%.
- Entry 4 also says "with road budgets fixed … about $19bn ($8–35bn)". That is B1. On the September 27 case
  the congestion item beside the account is $14.0bn at the low end and $12.0bn at the high end. The ranges
  are $2.0–32.0bn and −$0.9–30.8bn, and the ledger's central is $13.0bn.

**Preferences (item 3).**
[CALCULATION: `channels.csv`, `inputs.json` `preferences_attribution`, `_cache/person_frame.parquet`]

| Quantity | Before | Now |
|---|---:|---:|
| Label | "the part the counterfactual removes" | attribution under proportional replacement |
| White natives' part, central (low / high), $bn | −0.58 (−0.01 / −3.76) | −0.5774 (−0.0100 / −3.7432) |
| DBE premium inside it, central | $37.07m | $34.48m ($2.59m netted) |
| Other included recipients' part, central (low / high), $bn | none | −0.9686 (−0.0167 / −6.2794) |
| Preferences in "with proposed", central, $bn | −0.58 | −1.546 |
| "With proposed" on Sept 27: total; pooled share ahead (a) / (b) | −373.28; 18.73% / 17.94% without the others' part | −374.25; 18.62% / 17.82% |

The others' part comes mostly from admissions ($0.90bn of $0.97bn). White natives take 28.6% of the freed
seats' value. At the elite boundary most freed seats go to Asian applicants. Espenshade–Chung and AKR's Harvard
put 9.1% and 10.8% outside the four groups the sources report, and those seats stay with the pool. The white
natives' shares of the other three pools are 0.811 (hiring), 0.670 (lost profits) and 0.634 (the premium).

**Band variants and constant choices (item 1).** $bn, low–high.
[CALCULATION: `band_variants.csv`, `constant_choices_stock.csv`]

| Variant | Schools case | Sept 27 |
|---|---:|---:|
| Adopted | 258.4885–291.9548 | 321.8194–387.3701 |
| Justice raw coding | 254.2151–287.6814 | 317.4802–382.9980 |
| Justice grid low / high | 251.5167–284.9830 / 261.1910–294.6573 | 314.7402–380.2372 / 324.5634–390.1350 |
| CBP fixed | 255.3810–288.8473 | 318.6640–384.1908 |
| Uncompensated care at 0.7 of use | 256.9550–289.7124 | 320.2858–385.1277 |
| Grid low and 0.7 | 249.9832–282.7406 | 313.2067–377.9948 |
| Uncorrected | 265.5903–298.6797 | 332.7493–398.3079 |
| Capital at 7% (variant) | — | 406.3122–461.6229 |
| Option A, enterprises out (variant) | — | 304.6335–364.3718 |

The constant choices are unchanged to 1e-6.
- Row 8: federal −$0.027bn, stock −$0.353bn, interest −$0.011bn.
- Row 10: stock +$2.029bn, interest +$0.066bn.

## Gates and determinism

- **`specs.cjs --case sept27`.** Every gate passes:
  - both bands reproduce `main_case_bands.csv`: adopted and `schools_case`, plus the uncorrected row
    332.7493–398.3079, all to 1e-4;
  - every specification matches `cost()` to 1e-9;
  - the specifications match `per_spec.csv`'s method mean to 2.3e-13;
  - the capital components are the payload's 24;
  - the lines add to A_bn.
- **`winners_losers.py`.** 494 gates pass. The new ones cover:
  - the capital return against `case_ends_sept27.json` (1e-9), which must equal its 78766c2 blob;
  - the resource and displaced parts of the federal split, recomputed at every end and convention (1e-5);
  - the displaced total against the debt lane (1e-6), and fiscal = cash + resource per person (4.4e-11);
  - congestion against B1 by state (8e-15) and against both band ends (1e-9);
  - the seven CPS shares, the admissions crossings and the per-worker losses;
  - the registry's inside rows against `main_case`.
- **Two runs are byte-identical.** `specs.cjs` then `winners_losers.py`, in place, twice: 28 files in
  `derived/`, `gates.json` included. The three item-1 scripts give the same result in place, twice.
- **Earlier cases.**
  - `--case sept26_schools` in place leaves every tracked `derived/` file byte-identical to fa1bd3a.
  - `sept24` into scratch matches 8a762fe in 22 of 23 files; `sept26` matches round 1's run in 22 of 23.
  - The item-1 scripts on `sept24`, `sept26` and `sept26_schools` match in 5 of 6 files each.
  - The one file that differs in each case (`sources_manifest.csv`; `real_costs_totals.json`) differs only in
    out-dir path cells; the hashes are equal.
- **Old → new files.**
  - `old_new.py --round 1` rewrites round 1's `old_new_ledger.csv` (643 rows) byte for byte (d27dcb1).
  - The default `--round 2` writes `sept27_propagation_2026_09_27/derived/old_new_ledger.csv` (718 rows), the
    same on rerun.
- **Tests.** `pytest winners_losers_2026_09_24/`: 16 passed. The default is `sept27`, sept27's configure has
  its own pins and inputs, and the page rows follow the case.

## Flags for the parent (outside my boundary)

1. The real-costs memo's 2026-09-26 block says the social items do not depend on the case. From September 27
   congestion does: −$5.2bn at the low end and −$7.1bn at the high end.
2. FAQ entry 4's congestion sentence describes B1 with road budgets fixed. The case now prices $12.0–14.0bn.
3. The winners memo's "one in five" becomes about one in six (17.0–17.8% pooled).
4. The world ledger needs the winners commit and model pinned for `sept27` (`pins.json`).

## Files (uncommitted)

- `sept24_propagation_2026_09_24/`: `band_variants.cjs`, `real_costs_totals.py`, `constant_choices.py`,
  `RESULT.md`.
- `sept26_propagation_2026_09_26/old_new_lanes.py`.
- `winners_losers_2026_09_24/`: `specs.cjs`, `winners_losers.py`, `test_winners_losers.py`, `old_new.py`,
  `RESULT.md` (dated bracket), and `derived/`. In `derived/`, 16 files are modified, and
  `quintiles_vs_base_sept27.csv` and `regression_sept27.csv` are new.
- `sept27_propagation_2026_09_27/`: this file and `derived/` (`band_variants.csv/.json`,
  `real_costs_totals.csv/.json`, `constant_choices.csv`, `constant_choices_stock.csv`, `old_new_ledger.csv`).

Run, from the repository root:
```
F=infra/immigration-fiscal
node $F/sept24_propagation_2026_09_24/band_variants.cjs
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $F/sept24_propagation_2026_09_24/real_costs_totals.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $F/sept24_propagation_2026_09_24/constant_choices.py
node $F/winners_losers_2026_09_24/specs.cjs
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $F/winners_losers_2026_09_24/winners_losers.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $F/winners_losers_2026_09_24/old_new.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $F/sept26_propagation_2026_09_26/old_new_lanes.py
```

Model self-report: claude-opus-5-5 (Opus 5.5), W4 `ledger`.
