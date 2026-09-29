**Verdict:** No premise, swapped for its best-supported alternative, overturns more than two of the nine conclusions. The survey frame carries all nine, but its credible alternatives move none by more than about 1%. The conclusions nearest to breaking are C8's $320bn (one reference choice moves it +28%), C2's "taxes cover benefits" (it flips when pensions are counted on accrual), C5's "one in six gains" and C4's ~$100bn social add. Each of these breaks on one convention or on one item's published range. C1's $355bn breaks on the first-year horizon alone; inside the long-run frame it takes three of the case's own alternatives, or two conventions priced beside the account. [CALCULATION: `engine_breaks.cjs`, `tables.py` → `derived/`]

claude-opus-5-5

# Break conditions for the evidence map's conclusions (2026-09-29)

Scope: the nine section claims C1–C9 in `overview_2026_09_28/groups.py`. "Overturn" means one of three things: the sign flips, the stated magnitude moves by more than a quarter, or the stated ordering reverses. "Credible" means an arm, band or alternative that the repo already computes or cites. Every arm below sits at the end of its own range. Full cells are in `derived/conclusions.csv`; the premise × conclusion matrix is in `derived/common_mode.csv`.

## Premises that carry the most conclusions

| Rank | Premise | Conclusions | Swapped for its best-supported alternative |
|---|---|---|---|
| 1 | P01 survey frame (CPS/ACS self-ID + parental birthplace, 40.9M) | 9 | ACS level for the Mexico-born and NVSS births for the split: C1 −$2.2–2.5bn (−0.7%). No conclusion breaks. [DATA: ladder 209, 255] |
| 2 | P02 removal over one income year, people alive in 2024 | 8 | First-year budget horizon: C1 −37% and C4's pairing ≈ −29%. **Breaks two.** C2 and C6 hold. [DATA: ladder 229; INFERENCE for C4] |
| 3 | P08 dataset corrections (on-books share 0.526 assumed) | 7 | Uncorrected: C1 +3%, C2 tally $66.4/54.5bn. Breaks none. [CALCULATION: `c2_tally.csv`] |
| 4 | P03 services at long-run average cost | 6 | Schools at the within-district 0.836: C1 −8%, C8 ≈ −3%. Breaks none. [CALCULATION; INFERENCE for C8] |
| 5 | P05 pensions on cash | 6 | Accrual at payable benefits: **C2 clause 1 flips** (−$15.3/−24.2bn); C1 +21%, C4 +17%, C5's state and local share 85% → ≈70%. Breaks one. |

P07 (CBO incidence and use keys) ties at 6 and ranks sixth on the tie-break. P04 (capital return) and P09 (imputed status) carry 5 each.

## Conclusions nearest to breaking

| Conclusion | What breaks it | Steps |
|---|---|---|
| C8 $320bn against whites | Local whites state by state give $412.3/406.2bn (+28%). With both convention arms on accrual it is $449.8/447.3bn (+41%). The ordering holds in every arm (at least +$155bn). | 0 |
| C2 "taxes cover benefits" | Social Security and Part A on accrual turn the tally from +$62.0/49.4bn to −$15.3/−24.2bn. | 1 convention |
| C5 "one in six gains" | The lane's own range is 11–24% (ladder 226). One σ end, or charging the state-local cost nationally, moves the share by more than a quarter [INFERENCE: swings measured on the Sept 24 case]. | 1 convention |
| C4 add ≈ $100bn | Any one of PM2.5 ($31.5–122.5bn), crashes (−$57.7 to +74.3bn) or scale net (−$84.4 to +56.6bn) at its range end. The pairing total needs two such items. | 1 item |
| C3 net ≈ $11bn | Any of six data-component tails moves the net by more than a quarter. The cancellation itself fails only with two tails (care low + tax block low ≈ −$26bn). | 1 / 2 tails |
| C1 $355bn | First-year horizon (−37%). Otherwise 3 long-run alternatives (e.g. no capital return + schools 0.836 + roads and parks at CBO's lag, −26%). Upward, any pair of 7% capital, accrual and defense by GDP share (+38 to +44%). | 1 / 3 / 2 |
| C6 generations | Clause 2 needs the literature's G2→G3 transmission (0.46–0.53) in place of the CPS 0.84. Clause 1 needs a service response ≤ 27% for any generation. | 1 source swap / far |
| C9 crime | Clause 1 needs a 2.3–3.2× undercount of undocumented arrests. Legal non-naturalized immigrants already sit at 1.20 of the US-born on cost weights. Clause 2 is stable over 2019–2024. | unmeasured |
| C7 status | The status contrast is about $1.5k per adult (15% of the gap). "Little" would need about three times that. | far on size |

## Observations most worth making next

1. **How budgets respond to population outflows.** The 2008–12 net return to Mexico, the 2020–21 enrollment falls and declining-enrollment districts would show whether spending falls about 1:1 within 3–5 years. This decides P02/P03, the only premise whose swap breaks two conclusions (C1 and C4). The repo measured only the inflow side (0.836, ladder 230; "about half, and late", ladder 252).
2. **The on-books share of the Mexico-born.** SSA's Earnings Suspense File and ITIN filer counts by state for 2022–24 would measure it. It decides the tax side of C3 ($44–46bn) and the tax block in C1, C2 and C7. No 2022–25 measurement exists.
3. **Linked three-generation records** (restricted Census-linked data, PSID immigrant samples) would test C6's 0.84. The CPS grandparent test had no power (closing 0.78, SE 0.64; ladder 232).
4. **Birthplace recorded at booking, independent of DHS matches.** County jail files would size the misfiling behind C9 clause 1.
5. **A person-level wage validation of the winner count** (LEHD by skill and region) would test C5 against the nest's assigned gains (audit §2).

## Per conclusion (short; full cells in `derived/conclusions.csv`)

| | Break condition | Rival reading | Discriminating observation, made? |
|---|---|---|---|
| C1 | First-year horizon −37%. Long-run minimal set of 3 (−26/−27%). Upward pairs (+26 to +44%). [CALCULATION: `c1_min_cuts.csv`] | Mostly a horizon and pricing convention; ~$200–250bn in the first year [FRAMING-SENSITIVE] | Budgets after outflows; inflow side only (230, 252) |
| C2 | Clause 1 flips on accrual. Clause 2 flips below a service response of 2.8–13.6% (the lowest arm is 4–20× that). | Payroll tax buys promises; on accrual the group is a net recipient before services [FRAMING-SENSITIVE] | Mostly values; the group's money's-worth ratio is unmeasured |
| C3 | Taxes +$44.2/45.6bn and spending −$55.1/56.5bn, net −$10.9bn. The net moves on 1 tail; the cancellation fails on 2. | Two assumed adjustments cancel, not two records | ESF/ITIN on-books share; spending side done (210, 255, 256) |
| C4 | One item at a range end breaks the add; the pairing needs two. | Against average residents the group is cleaner (PM2.5 −$46.5bn) [FRAMING-SENSITIVE] | Local volume × crash panel (PeMS × CCRS); partial (264, 266) |
| C5 | State-local share: >50% under three federal-side conventions (57%); below 50% only with defense and old interest at average cost (≈48%). Winners: 1 convention. | Winners are assigned, not identified (audit §2: 23.9% → 10.3% at the same aggregate) | LEHD wage effects; not made |
| C6 | Generation break-evens ≤ 21.5% (a) and ≤ 26.9% (b) [CALCULATION: `c6_generation_break_even.csv`]. Clause 2: one source swap. | G3+ is an older, less-selected stock. Partly fails: the young cohorts also carry 0.83–0.87 (232). | Linked lineages; underpowered attempt (232) |
| C7 | The contrast would need to be about three times larger. The status rule switches are unpriced [GAP]. | Status acts through the children (186) | DACA/IRCA timing on children's schooling; not made |
| C8 | Already crossed by local whites (+28%) and both convention arms (+41%) | Composition, not group-specific: the group is $85–87bn above an all-residents slice (263) | Framing; engine re-key not run |
| C9 | Clause 1: an undercount of 2.3–3.2× [GAP on its size]. Clause 2: needs 2010's 2.56. | Removal and matching hide offenders; custody carries sentencing, and NCVS gives 0.94× | Booking birthplace (not made). NIBRS 1.74–4.22× already matches custody better than NCVS (202). |

## Common mode: the two questions

**Which single weak premise, if wrong, takes down the most?** The long-run service response (P03), together with the horizon it defines (P02). If budgets adjust only as CBO's first-year rules say, C1 (−37%) and the C4 pairing (≈ −29%) fall together. C2, C5 and C6 survive, because their sign break-evens sit at 3–27% and the winner share moves less than 0.1 point. The pension convention (P05) is the only other single swap that breaks anything (C2 clause 1). The frame (P01) carries all nine conclusions, but no credible alternative moves any of them by more than about 1%. [CALCULATION; INFERENCE where marked in `common_mode.csv`]

**Apparently independent confirmations that share a premise:**
- C3's "Legal status does not drive the gap" and C7's section claim are the same evidence, ladder 85, counted in two sections. C7's own findings (157, 185–187, 242) describe counts and children, not the fiscal gap.
- "A second survey gives the same gaps within 4%" (127, 129): ACS and CPS share the self-ID question, Census hot-deck fill-ins (the source of ladder 208's bias) and one tax calculator.
- "IRS data confirm the direction" (249): IRS supplies only the national AGI bins. The group's share within each bin is still the CPS's (P01/P07).
- C6's split and C8's re-key are re-cuts of C1. They add no independent support for its sign or size.
- C9's NIBRS ratios and C4's $29bn victim cost use the same offender-ethnicity data (202; ladder 189 "police records confirm").
- C5's 85% state-local share and C2's "schools decide the sign" rest on the same line: schools at response 1, funded by states and localities.

## Stale numbers in the map (for the map's owner)

- C2's `why` text says "about $65bn (60–70)". That is the September 24 staircase before data corrections (`figures.json` "tally"). On the adopted case the tally is **$62.0 / $49.4bn** at ends 48 / 11 (uncorrected: $66.4 / $54.5bn). [CALCULATION: `c2_tally.csv`]
- C3's "about $50bn each" is now **$44.2–45.6bn** on taxes and **$55.1–56.5bn** on spending. The net is still −$10.9bn. [CALCULATION: `c3_correction_split.csv`]

## Computations

- `engine_breaks.cjs` runs on the adopted package (`main_case_long_run_2026_09_27/package.cjs`: `central`, `evaluateFull`, `capitalReturn`) and on `main_case_2026_09_24/sign_reversal.cjs`'s `breakEven`, whose definition runs unchanged. All 16 gates pass: the case, five published arm rows, both union break-evens and the six uncorrected generation models. Outputs: `c1_arms.csv`, `c1_min_cuts.csv`, `c2_tally.csv`, `c3_correction_split.csv`, `c6_generation_break_even.csv`.
- Additive items are ladder figures, not engine runs. They are marked "additive" in `c1_arms.csv`: accrual (257), property tax response (253), defense by GDP share (groups.py conventions), and the MCBS 65+ and care tails (components.csv).
- The C6 break-evens use the uncorrected generation models. Per-generation corrections run from −$8.4bn to +$2.6bn (`generation_results.csv`) and were not rerun [GAP].
- `tables.py` writes `conclusions.csv` and `common_mode.csv`. It stops if any quoted number drifts from the engine CSVs.
- Rerun: `scripts/rerun_lane.py` with both commands gives IDENTICAL, 10/10 files, rc 0.

## Coverage

- Covered: C1–C9 (groups.py sections account, services, data, social, whopays, generations, status, comparators, crime). Read: groups.py; ladder 65, 66, 70, 77, 82, 85, 144, 161, 185–189, 194, 196, 201, 202, 206, 208–210, 215, 217, 219, 220, 224, 226, 229, 230, 232, 236, 239, 248–250, 253–258, 260, 263–266; audit §1–§5 and the opening of §6; main_case_long_run RESULT, components.csv, sign_reversal.cjs/csv; generation_account RESULT and results; real_costs_totals.csv §7; figures.json staircase.
- Skipped, out of scope: groups.py sections conventions, work, time, civic, claims and method.
- Not computed [GAP]:
  - per-generation accrual;
  - C6 on the corrected generation models;
  - winners under σ on the September 27 base (the lane's σ plumbing needs its own run; the September 24 swings are transferred [INFERENCE]);
  - C7 under alternative status rules;
  - the size of the C9 undercount;
  - C8 through the engine.
- Not read in full: winners_losers.py and the crime-classification memos. Their figures are cited from ladder text only.

## Log

- 2026-09-29 00:37 JST lane created; stub written.
- 2026-09-29 00:46 JST read groups.py claims (C1–C9), the ladder entries listed under Coverage, audit §2–§4, sign_reversal.cjs/csv and components.csv.
- 2026-09-29 00:53 JST `engine_breaks.cjs` runs; all 16 gates pass.
- 2026-09-29 00:57 JST `tables.py` written. Rerun IDENTICAL 10/10.
- 2026-09-29 00:58 JST RESULT sections written; verdict set.

## Lead verification (2026-09-29 01:02 JST)

- Reran both scripts in place with `scripts/rerun_lane.py`: rc 0, 10 of 10 files byte-identical.
- Checked by hand: C2's tally 400.16 − 338.15 = 62.01 and 62.01 − 77.28 = −15.27 at the low end; C3's split 44.2 − 55.1 = −10.9; the first-year horizon 200.9 / 321.8 = 0.624 (−37.6%) and 245.7 / 387.4 = 0.634 (−36.6%).
- Note: the property-tax response in the minimal down-sets (ladder 253) is a candidate for the next revision, not yet an arm of the adopted case.


claude-opus-5-5

## v4 case (sept29), 2026-09-29

**Verdict (v4).** One of the nine conclusions breaks on v4's central itself: C2. With Social Security and Medicare Part A on accrual at payable benefits (P05, v4's central), the group's direct taxes fall short of its household transfers by $3.4 / 12.6bn at ends 48 / 11. At the most adverse end it costs others even if no service budget responds (service break-even −11.0% to −3.8%). C8's $320bn against US whites probably breaks for the same reason: September 27's accrual arm was +41% [INFERENCE; v4-dated-b reruns it]. The other seven hold. C1 restates to $403bn ($371–435bn) and is easier to break downward: the first-year horizon alone gives −26.1%, 1.1 points past the cut, and so do cash pensions plus no capital return (−29.9%). No premise swap breaks more than one conclusion. The horizon now breaks only C1 (the pairing falls about 21%), and pensions back on cash restore C2 and break nothing. [CALCULATION: `engine_breaks_sept29.cjs`, `tables_sept29.py` → `derived/*_sept29.csv`]

The run was resumed twice, after the usage-limit stop (17:24 JST) and after the machine reboot (about 20:51 JST), and this last segment also continued past a context compaction. Nothing but the stub existed before the reboot. Everything below was computed and gated after 21:47 JST.

### The nine conclusions on v4

The claims are the map's, still on the September 27 case (`overview_2026_09_28/groups.py` at HEAD). Full cells are in `derived/conclusions_sept29.csv`, the premise matrix in `derived/common_mode_sept29.csv`.

| | Claim (the map) | On v4 | Status | Decided by |
|---|---|---|---|---|
| C1 | about $355bn a year | $371.4–434.8bn, midpoint $403.1bn (+13.7%) | holds, restated | P02 alone breaks it |
| C2 | services decide the sign; taxes cover benefits | tally −$3.4 / −12.6bn; break-even −11.0% to +3.3% | **breaks at the central** | P05 |
| C3 | ~$50bn each (44–57), net ~$11bn | taxes +$44.43 / 45.84bn, spending −$55.16 / 57.15bn, net −$10.73 / 11.31bn | holds | P08 |
| C4 | the add, about $100bn | the same $96.3 / 100.7bn; pairing $462.9–535.5bn | holds | — |
| C5 | most (85%); one in six gains | 68% state and local; winners not rerun [GAP] | holds on "most" | P05 sets the share |
| C6 | each generation costs others | each at least $87.1bn; break-evens at most 18.5% | holds | — |
| C7 | status explains little | no v4 input (ladder 85, cash flows) | unchanged | — |
| C8 | $320–405bn more than as many whites | not rerun here | likely breaks [INFERENCE] | P05 |
| C9 | offending and custody | no v4 input | unchanged | — |

### "Taxes cover benefits" with the accrual as the central (C2)

| $bn, ends 48 / 11 | Direct receipts | Household transfers | Tally |
|---|---:|---:|---:|
| v4 case: accrual at payable benefits | 408.4 / 386.7 | 411.8 / 399.3 | **−3.4 / −12.6** |
| cash set: pensions as 2024 cash | 410.5 / 388.5 | 337.2 / 328.1 | +73.3 / +60.4 |
| v4's items without the dataset corrections (accrual rebuilt) | 453.1 / 432.9 | 451.9 / 440.7 | +1.2 / −7.8 |
| uncorrected, no v4 items | 444.8 / 424.5 | 378.4 / 370.0 | +66.4 / +54.5 |

At scheduled benefits the transfers rise another $34.2 / 32.4bn and the tally is −$37.6 / −45.0bn. The high-end transfers, 399.35, print as 399.3 so that the row adds. [CALCULATION: `c2_tally_sept29.csv`]

Clause 1 fails at both ends. At the low end the tax block's favorable tail alone brings it back (+$2.1bn); at the high end it takes all six tax and transfer tails at their favorable ends (+$6.9bn) [INFERENCE: additive, `components.csv`].

Clause 2 fails too. The service break-even is September 24's definition, run inside a copy of the v4 lane's `withCase`:

| Break-even service response | Personal, most / least adverse | Shared, most / least adverse |
|---|---:|---:|
| v4 case, enterprise surplus at 1 | −11.0% / −2.4% | −9.3% / −0.6% |
| v4 case, enterprise surplus at s | −5.5% / +1.5% | −3.8% / +3.3% |
| cash set, enterprise surplus at 1 | 7.0% / 16.2% | 9.8% / 19.1% |
| cash set, enterprise surplus at s | 11.7% / 19.4% | 14.3% / 22.2% |

A negative break-even means the group costs others at every service response from 0 to 1, so services no longer decide the sign. Only at the least adverse end, with the enterprise surplus at s, would a response below 1.5–3.3% flip it. On the cash set services still decide the sign. [CALCULATION: `c2_break_even_sept29.csv`; the case's rows reproduce `main_case_2026_09_29/derived/sign_reversal.csv` at 1e-4]

### What moved in the other conclusions

- **C1.** The first-year horizon alone gives $277.3–318.3bn (−26.1%). On v4 that horizon also fixes property levies (item 5 at zero) and keys roads on resources. With item 5's long-run response kept it is −32.9%; with cash pensions as well, −44.7%. Inside the long-run frame, cash pensions plus one alternative break it: no capital return (−29.9%) or roads and parks at CBO's first-year 0 (−27.8%). Without cash pensions it takes four. Upward it takes two, both with 7% capital: + defense by GDP share (+35.0%), + scheduled benefits (+28.4%) or + property taxes at zero (+26.9%); without 7% it takes three. [CALCULATION: `c1_arms_sept29.csv`, `c1_min_cuts_sept29.csv`]
- **C3.** By the lines that move, taxes move +$44.43 / 45.84bn and spending −$55.16 / 57.15bn, net −$10.73 / 11.31bn with no interaction. The spending move is the spending checks' −$44.50 / 45.68bn plus −$10.66 / 11.47bn of accrual: the checks lower the group's OASDI receipts by $10.95 / 11.78bn, and the accrual follows them. $10.79 / 11.23bn of Social Security and Part A benefit corrections drop out, because the accrual replaces current benefits. By the edits' side, the receipt checks move the cost +$33.77 / 34.37bn (44.43 − 10.66). With every tail increment held, the sides are +$44.43 / 45.84bn and −$55.29 / 56.91bn (−44.50 − 10.79), net −$10.86 / 11.07bn. One data tail moves the net by more than a quarter; the cancellation fails on two tails, or on one (care low) by the edits' side. [CALCULATION: `c3_correction_split_sept29.csv`; INFERENCE: additive for the tails]
- **C4.** The social rows do not move ($96.3 / 100.7bn); the pairing rises to $462.9–535.5bn. One item at a range end still breaks the add. The pairing needs two, and now only crashes and scale net together do it (−27.9% / +26.8%); PM2.5 high plus crashes high reaches +23.3%. The first-year horizon moves the pairing about −21% [INFERENCE: social rows held], so it no longer breaks it. [DATA: `sept24_propagation_2026_09_24/derived/sept29/real_costs_totals.csv`; INFERENCE: additive]
- **C5.** State and local taxpayers pay 67.9% / 67.5%, because the accrual ($76.7 / 73.0bn) is all federal; on the cash set it is 85.7% / 81.2%. "Most" survives defense by GDP share, legacy interest and scheduled benefits together (50.8% / 51.6%). It fails with defense and old interest at average cost (39.2% / 41.6%). [CALCULATION: additive on `debt_legacy_2026_09_23/derived/sept29/federal_split_2024.csv`, central convention] The winner share is not rerun, because the winners lane has no sept29 run [GAP].
- **C6.** Every generation costs others at both ends under both conventions: at least $87.1bn, or $66.8bn on the cash set. The largest service break-even is 18.5% (convention b, G3+, shared; 13.3% under a), and G1's are negative under b. These run on the generation account's corrected sept29 models; September 27's ran on uncorrected ones. [CALCULATION: `c6_generation_break_even_sept29.csv`]
- **C7 and C9** take no v4 input. C7 rests on ladder 85's cash flows and is not recomputed with the accrual [GAP].
- **C8** is not rerun here (v4-dated-b's lane). On September 27's rough re-key, the accrual arm gave $449.8 / 447.3bn, +41% on $320bn [INFERENCE for v4].

### Premises on v4

| Rank | Premise | Conclusions | Swapped for its best-supported alternative |
|---|---|---|---|
| 1 | P01 survey frame, 39.7M priced | 9 | Not rerun on v4; on September 27, C1 −0.7%. Breaks none [INFERENCE]. |
| 2 | P02 one income year | 8 | First-year horizon: **C1 −26.1%, breaks**; the pairing, about −21%, holds. **Breaks one.** |
| 3 | P08 dataset corrections | 7 | Uncorrected, accrual rebuilt: C1 +2.7%; C2 tally +$1.2 / −7.8bn. Breaks none. |
| 4 | P03 long-run responses, property levies included | 6 | Schools at 0.836: C1 −6.2% (property taxes at zero instead, +6.7%). Breaks none. |
| 5 | P05 pensions on accrual at payable benefits | 6 | Cash: **restores C2** (tally +$73.3 / 60.4bn), C1 −18.6%, C5 81–86%. Breaks none. Scheduled benefits instead: C1 +8.3%, tally −$37.6 / −45.0bn. |

P07 (keys) ties at 6 and ranks sixth, as on September 27. [CALCULATION and INFERENCE as marked in `common_mode_sept29.csv`]

### Rules designed for v4

1. **Separate scripts.** `engine_breaks_sept29.cjs` and `tables_sept29.py` write `derived/*_sept29.csv`; `engine_breaks.cjs`, `tables.py` and their seven files are unchanged. Justification: v4 needs other arms, gates and text, and the old scripts stay the record of what produced the September 27 files. Alternative: a `--case` flag in the old scripts, which would edit committed scripts for no gain.
2. **The arms that added item 5 and the accrual now remove them.** Cash pensions (`pension4: "cash"`, the cash set) is a downward engine arm; property taxes at zero (`property: "none"`, September 27's convention) is an upward one. Item 5's high reading (−$13.2bn) is a downward arm; its low reading (+$3.1bn) is listed, dominated by property at zero. Justification: an additive arm for an item the case already contains counts it twice. Alternative: none; the brief rules out the old additive arms.
3. **Scheduled benefits, priced beside the account.** The accrual's own rule at the scheduled net ratio (1.2406 for 0.9737) on the case's OASDI receipts, plus the scheduled Part A accrual (45.35 for 41.14): +$34.21 / 32.38bn. A positive control on the September 27 receipts reproduces the pension lane's scheduled less payable (34.3622 / 32.5441) at 1e-6. Justification: the accrual reads v4's OASDI receipts, not September 27's. Alternative: the pension lane's September 27 difference carried over, $0.15 / 0.16bn higher.
4. **The first-year horizon on v4.** September 27's rule (the long-run lines, rental assistance, the capital return and the enterprise receipt off; CBO's one-year school response), plus item 5 at zero and roads keyed on resources. Justification: levies are set a year ahead, so the first year has no property-tax response, and the package blocks first-year roads under the miles key (`[BLOCKED] roads by miles takes the subfunctions' long-run responses`). Gate: the rule with every v4 item off gives September 27's first-year row at 1e-9. Alternatives beside: item 5 kept (−32.9%), and cash pensions as well (−44.7%). The same key switch sits in the first-year roads and parks arm. On its own it is −$2.07 / 3.80bn of that arm's −$28.06 / 46.33bn.
5. **C3's split keeps v4's items and rebuilds the pension switch.** The dataset corrections are the payload's first 278 edits, gated identical to the September 27 payload's. The other 138 edits, the receipt lines and the production grid are in every run, in payload order. The pension switch is a level, so it is rebuilt on each subset: Social Security at ratio_net × that subset's OASDI receipts, and Part A's share of Medicare replaced by the Part A accrual. A gate checks that the rebuild moves nothing on the full payload. The other items stay at their increments, because each is proportional to a line amount or a share change and rebuilding them needs the builder. The sides are quoted by the lines that move, because the claim is about taxes and spending. Alternatives beside: the sides by the edits' side, and every increment held.
6. **C6 on the corrected generation models.** The generation account's sept29 payloads are applied to its generation models with the union's meta. They are gated to `generation_results_sept29*.csv` for each generation at 1e-6, and the three generations add up to the case. Their sha256 is in `c6_inputs_sept29.csv`. Justification: v4's items and the accrual live in those payloads. Alternative: the uncorrected models, as on September 27, which carry neither.
7. **C5 counts the accrual as a federal cost in 2024.** The share uses the debt lane's four columns and their federal parts. Justification: the accrual is a federal liability that the group's 2024 payroll taxes earn. Alternative: the winners lane's rule, which assigns the accrual to future taxpayers and gives the cash-set figure, 81–86%.
8. **C3's data tails** are `components.csv` less its response, capital and v4-item rows. This set reproduces September 27's six.
9. **A quote-aware CSV reader** that stops on a row with the wrong field count. The first run read `components.csv` with a naive split, and the arm gates caught the misread labels.

### Findings for files this lane does not own

- `derived/c6_generation_break_even.csv` (September 27) swaps two headers. `breakEven` returns [most adverse, least adverse], but the file labels them least, then most. Its text used only the maximum, so no conclusion changes. The file stays byte-identical; the sept29 file labels them correctly.
- The evidence map is still on September 27's case. On v4, C2's claim is false, and so are its range ("sign flips below a 3–14% service response") and the $55bn (49–62) in its text. C1's $355bn is $403bn, and C5's 85% is 68%. The method finding's "the budget horizon breaks two … about 37%" becomes "one … about 26%", and the accrual flip it forecasts for C2 has happened.
- A peer has uncommitted changes to `debt_legacy_2026_09_23/derived/sept29/summary.json` (the whole-budget rules). The `headline_2024` values this lane reads are identical to HEAD's.

### Gates (brief)

1. The September 27 commands rerun in place (`scripts/rerun_lane.py`, `--allow-unrun` for the two new scripts): IDENTICAL 21/21, rc 0. `git diff --quiet` on `derived/`: rc 0.
2. The sept29 outputs exist and the lane's gates pass: `engine_breaks_sept29.cjs` 41 of 41, and every check in `tables_sept29.py`. Four perturbed copies of the checks each stop the build.
3. Oracle: 371.4146 / 434.8410, and the cash set 294.7011 / 361.8175, at 1e-4 (rows `adopted` and `pension_cash` of `c1_arms_sept29.csv`; the engine gates at 1e-4, the C3 rebuild at 1e-9).
4. After the sept29 run, two passes with all four commands: IDENTICAL 21/21 each, rc 0.

### Reproduce

```sh
node infra/immigration-fiscal/break_conditions_2026_09_29/engine_breaks_sept29.cjs
uv run --no-project --offline python3 infra/immigration-fiscal/break_conditions_2026_09_29/tables_sept29.py
```

### Log (append-only; times from `date`)

- 2026-09-29 20:14 JST: resumed after the usage-limit stop at 17:24 JST. Only this stub existed; no code or derived file of the lane had been changed. Design read: the adopted package (40c4ba7), its payload (8 correction lines, 2 receipt lines, 3 national-scale edits, row-4 production grid, pension accrual meta), candidate v4 package options (pension4 cash|payable_net, property none|long_run, property_reading low|central|high).
- 2026-09-29 21:02 JST: resumed after the machine reboot of about 20:51 JST (the run had stopped mid-work). Nothing of this lane beyond the stub had been written before the reboot; the work starts here.
- 2026-09-29 21:47 JST: resumed after a context compaction and wrote `engine_breaks_sept29.cjs`. Every v4 computation (C1, C2, C3, C6), `tables_sept29.py` and all the gates were run in this segment; nothing had been computed before it. The first full run stopped on 4 of its gates (the naive CSV split, and the cash-set sum checked against a 4-decimal printed row at 1e-6); both were fixed before any output was written.
- 2026-09-29 22:35 JST: first gate run (22:35:37–22:36:43): gate 1 IDENTICAL 21/21, gate 3 pass, gate 4 IDENTICAL 21/21 twice.
- 2026-09-29 22:40 JST: section written; the PROBE line replaced.
- 2026-09-29 22:42 JST: gates rerun after the last text edits (controlled rounding in C2 and C3, the C4 footing note): gate 1 IDENTICAL 21/21 and `derived/` equal to HEAD; gate 3 pass; gate 4's first pass rewrote `conclusions_sept29.csv` (the C4 edit had not been run), its second was IDENTICAL.
- 2026-09-29 22:49 JST: two final gate-4 passes (22:47:09, 22:48:55) IDENTICAL 21/21, rc 0; `git diff --quiet` on `derived/` rc 0.

### Lead verification (2026-09-29 22:59 JST)

- **C8 holds on v4.** The white lane ran the v4 re-key after this section was written (6665297,
  `white_replacement_2026_09_28/derived/headline_sept29.csv`): against 39.7M third-plus whites the union costs
  $351.2 / 350.5bn more on the case's accrual basis, and $410.4 / 408.0bn against local whites state by state. That
  is inside the map's $320–405bn at its low end and $3–5bn above it at the high end, so the inference above that C8
  "likely breaks" does not stand. September 27's +41% arm was not v4's construction: on v4 the accrual already
  removes the cash age artefact that arm removed.
- **C5's winner share is in.** The winners lane's v4 run (858f77a) puts 17.9% (tax-share) and 17.1% (per person)
  of other residents ahead, against 17.8% / 17.0% on September 27: "one in six gains" holds.
- Checked: `sign_reversal.cjs:56-63` returns [most adverse, least adverse], confirming the swapped September 27
  header in `c6_generation_break_even.csv` (fixed separately; no figure in `conclusions.csv` reads the labels).
