**Verdict:** [2026-10-05: on main case v5 (`oct05`), C2 splits by end. Direct taxes exceed benefits counted on accrual by $6.5bn at the low end and fall $4.4bn short at the high end (sept29: −$3.4 / −12.6bn, broken at both ends), because the added people's own tally is +$9.9 / 8.2bn. C1 restates to a $425.8bn midpoint ($390.3–461.2bn; sept29 $403.1bn) and still breaks on the first-year horizon alone (−26.7%; sept29 −26.1%). Counting the lineage by ancestry share at the stated bound's low end also breaks it alone (−29.8%) [FRAMING-SENSITIVE]. The lineage's other alternatives (arms a and c, C3 ± 1 SE, the replacement child) each move C1 by less than 3%. The other conclusions hold as on v4; C8 and C5's winner share are not rerun here. See "v5 case (oct05)" below.] No premise, swapped for its best-supported alternative, overturns more than two of the nine conclusions. The survey frame carries all nine, but its credible alternatives move none by more than about 1%. The conclusions nearest to breaking are C8's $320bn (one reference choice moves it +28%), C2's "taxes cover benefits" (it flips when pensions are counted on accrual), C5's "one in six gains" and C4's ~$100bn social add. Each of these breaks on one convention or on one item's published range. C1's $355bn breaks on the first-year horizon alone; inside the long-run frame it takes three of the case's own alternatives, or two conventions priced beside the account. [CALCULATION: `engine_breaks.cjs`, `tables.py` → `derived/`]

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
| C6 generations | Clause 2 needs the literature's G2→G3 transmission (0.46–0.53) in place of the CPS 0.84 [2026-10-05: 0.86 with C3 from the CPS basic monthly frame (g3_identity_pooled_2026_10_05, monthly frame)]. Clause 1 needs a service response ≤ 27% for any generation. | 1 source swap / far |
| C9 crime | Clause 1 needs a 2.3–3.2× undercount of undocumented arrests. Legal non-naturalized immigrants already sit at 1.20 of the US-born on cost weights. Clause 2 is stable over 2019–2024. | unmeasured |
| C7 status | The status contrast is about $1.5k per adult (15% of the gap). "Little" would need about three times that. | far on size |

## Observations most worth making next

1. **How budgets respond to population outflows.** The 2008–12 net return to Mexico, the 2020–21 enrollment falls and declining-enrollment districts would show whether spending falls about 1:1 within 3–5 years. This decides P02/P03, the only premise whose swap breaks two conclusions (C1 and C4). The repo measured only the inflow side (0.836, ladder 230; "about half, and late", ladder 252).
2. **The on-books share of the Mexico-born.** SSA's Earnings Suspense File and ITIN filer counts by state for 2022–24 would measure it. It decides the tax side of C3 ($44–46bn) and the tax block in C1, C2 and C7. No 2022–25 measurement exists.
3. **Linked three-generation records** (restricted Census-linked data, PSID immigrant samples) would test C6's 0.84. The CPS grandparent test had no power (closing 0.78, SE 0.64; ladder 232). [2026-10-05: the CPS basic monthly frame 1994–2026 now gives 526 unique G3 non-identifiers at 25+, closing 0.57 (SE 0.26) and 0.56 (0.25) pooled with NLSY97, and C6's ratio becomes 0.86. It tests identity loss, not linkage. (g3_identity_pooled_2026_10_05, monthly frame)]
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

## v5 case (oct05), 2026-10-05

claude-opus-5-5 (v5 consumer lane B). **Verdict (v5).** Main case v5 (`../main_case_2026_10_05/`, $390.29–461.24bn) adds
3.04M descendants who no longer report Mexican origin, counted whole. One conclusion changes status: C2 now splits by
end. The added people's direct taxes exceed their household transfers by $9.9 / 8.2bn, which lifts the tally from
v4's −$3.4 / −12.6bn to +$6.5bn at the low end and −$4.4bn at the high end. The split holds under arms a and c, and one
tail decides each end. C1 restates to $390.3–461.2bn (+20.1% on September 27's $354.6bn midpoint, against v4's +13.7%).
The first-year horizon alone still breaks it (−26.7%), and so does the ancestry-share count at its stated bound's low
end (−29.8%) [FRAMING-SENSITIVE]. The lineage's own alternatives each move C1 by less than 3%: arms a and c, C3 ± 1 SE
and the replacement child. C3 is v4's to $0.01bn, and C4, C5 and C6 hold with v5's figures. C7 and C9 take no v5 input.
C8 and C5's winner share belong to other lanes' oct05 runs and are not rerun here [GAP]. [CALCULATION:
`engine_breaks_sept29.cjs --case oct05`, `tables_oct05.py` → `derived/*_oct05.csv`]

### The nine conclusions on v5

The claims are still the map's, on the September 27 case. Full cells are in `derived/conclusions_oct05.csv`, and the
premise matrix is in `derived/common_mode_oct05.csv`.

| | Claim (the map) | On v4 (sept29) | On v5 (oct05) | Status on v5 |
|---|---|---|---|---|
| C1 | about $355bn a year | $371.4–434.8bn, midpoint $403.1bn | $390.3–461.2bn, midpoint $425.8bn | holds, restated |
| C2 | taxes cover benefits; services decide the sign | tally −$3.4 / −12.6bn; break-even −11.0% to +3.3% | tally +$6.5 / −4.4bn; break-even −8.8% to +5.5% | **breaks at the high end**, holds at the low end |
| C3 | ~$50bn each, net ~$11bn | +$44.43 / 45.84bn, −$55.16 / 57.15bn, net −$10.73 / 11.31bn | the same | holds |
| C4 | the add, about $100bn | $96.3 / 100.7bn; pairing $462.9–535.5bn | $104.8 / 109.4bn; pairing $490.2–570.7bn | holds |
| C5 | most (85%); one in six gains | 67.9% / 67.5% state and local | 68.8% / 68.2% | holds on "most"; winners not rerun here |
| C6 | each generation costs others | each at least $87.1bn; break-evens at most 18.5% | at least $87.0bn; at most 21.6% | holds |
| C7 | status explains little | no v4 input | no v5 input | unchanged |
| C8 | $320–405bn more than as many whites | $351.2 / 350.5bn (lead verification) | not rerun here [GAP] | — |
| C9 | offending and custody | no v4 input | no v5 input | unchanged |

### C2 on v5

| $bn, ends 48 / 11 | Direct receipts | Household transfers | Tally |
|---|---:|---:|---:|
| v5 case: accrual at payable benefits | 450.5 / 424.0 | 444.0 / 428.4 | **+6.5 / −4.4** |
| cash set: pensions as 2024 cash | 452.8 / 426.0 | 363.4 / 352.6 | +89.4 / +73.4 |
| v5's items without the dataset corrections (the union's accrual rebuilt) | 495.1 / 470.2 | 484.0 / 469.8 | +11.1 / +0.4 |
| uncorrected, no v4 items, no lineage | 444.8 / 424.5 | 378.4 / 370.0 | +66.4 / +54.5 |

The cash set's high-end receipts (426.06) print as 426.0 and the uncorrected-items transfers (484.06) as 484.0, so the
rows add. The tally splits into the union alone at v5's responses, −$3.4 / −12.6bn, and the added people's own,
+$9.9 / +8.2bn. Arm a (1.81M added) gives +$4.6 / −5.3bn and arm c (4.27M) gives +$8.4 / −3.5bn. At scheduled benefits
the transfers rise another $37.2 / 34.9bn and the tally is −$30.7 / −39.3bn. [CALCULATION: `c2_tally_oct05.csv`]

One tail decides each end [INFERENCE: additive, `components.csv`]. At the high end, care's favorable tail alone restores
clause 1 (+$4.8bn). The tax block's favorable tail falls $0.15bn short alone and restores it with any one more tax or
transfer tail (+$1.0bn or more). At the low end, the MCBS 65+ bound on medical alone breaks it (−$2.0bn).

| Break-even service response | Personal, most / least adverse | Shared, most / least adverse |
|---|---:|---:|
| v5 case, enterprise surplus at 1 | −8.8% / −0.4% | −6.9% / +1.7% |
| v5 case, enterprise surplus at s | −3.4% / +3.4% | −1.5% / +5.5% |
| cash set, enterprise surplus at 1 | 9.0% / 17.9% | 12.3% / 21.5% |
| cash set, enterprise surplus at s | 13.5% / 21.0% | 16.7% / 24.5% |

Clause 2 survives only at the least adverse end: below a 1.7% response with the enterprise surplus at 1 (shared), or
3.4–5.5% with it at s. [CALCULATION: `c2_break_even_oct05.csv`; the case's rows reproduce
`main_case_2026_10_05/derived/sign_reversal.csv` (`oct05_low`, `oct05_high`) at 1e-4]

### What moved in the other conclusions

- **C1.** The cut is a quarter of the $425.8bn midpoint: below $319.3bn or above $532.2bn.
  - **Downward, one step.** The first-year horizon alone gives $289.1–335.3bn (−26.7%; −33.7% with item 5's long-run
    response kept, −45.5% with cash pensions as well). The ancestry-share count at its stated bound's low end alone gives
    $275.4–322.1bn (−29.8%) [FRAMING-SENSITIVE].
  - **Downward with whole people.** Cash pensions plus one alternative break it: no capital return (−30.5%), first-year
    roads and parks (−28.3%), or schools at 0.836 (−25.3%; new on v5). Without cash pensions it takes four. At the
    population lane's convention for ancestry share (−19.2% alone), one more alternative breaks it.
  - **Upward.** It takes two, both with 7% capital: + defense by GDP share (+34.7%), + scheduled benefits (+29.1%) or
    + property taxes at zero (+27.6%). Without 7% it takes three.
  - **The lineage's own alternatives.** Arms a and c move it −2.8% / +2.8%, C3 ± 1 SE ∓0.8%, the replacement child (r = 1)
    −2.1% [FRAMING-SENSITIVE], and the ancestry-share count −17.5% to −29.8% across its bound. Stacks: all 8 downward
    alternatives −50.8% (−74.7% with the ancestry share), all 6 upward +55.4% (+58.1% with arm c).
  - [CALCULATION: `c1_arms_oct05.csv`, `c1_min_cuts_oct05.csv`]
- **C3.** The corrections' split is v4's within $0.01bn: the lineage's edits are held in every run. Taxes move
  +$44.43 / 45.84bn, spending −$55.16 / 57.15bn and the net −$10.73 / 11.31bn. The tails findings are unchanged. [GAP]
  The added G3+ members are priced on the corrected G3+ model, so the split leaves out the corrections their amounts
  carry. [CALCULATION: `c3_correction_split_oct05.csv`]
- **C4.** The social rows rise to $104.8 / 109.4bn: the added people's own rows are $8.6 / 8.8bn, each restated row times
  their share of its key. The pairing rises to $490.2–570.7bn ($11,466–13,349 per member of 42.75M). One item at a range
  end still breaks the add. The pairing (below $397.8bn or above $663.1bn) needs crashes and scale net together
  (−26.2% / +25.2%); PM2.5 high plus crashes high reaches +21.9%. The first-year horizon moves the pairing about −21.4%,
  and the cash set pairs to $407.3–492.8bn (−15.2%). [DATA: `sept24_propagation_2026_09_24/derived/oct05/real_costs_totals.csv`;
  INFERENCE: additive]
- **C5.** State and local taxpayers pay 68.8% / 68.2%. The accrual ($82.9 / 77.8bn) is all federal; on the cash set the
  share is 87.4% / 82.1%. "Most" survives defense by GDP share, legacy interest ($30.6 / 42.6bn) and scheduled benefits
  together (51.8% / 52.5%). It fails with defense and old interest at average cost (40.6% / 43.0%). [CALCULATION:
  additive on `debt_legacy_2026_09_23/derived/oct05/federal_split_2024.csv`, central convention]
- **C6.** Every generation costs others at both ends under both conventions: at least $87.0bn, or $72.6bn on the cash
  set. G3+ carries the added people: $141.7 / 195.0bn under convention a, against v4's $122.6 / 168.4bn. Its largest
  break-even rises 3.5 / 3.2 points to 16.9% (a) and 21.6% (b), because 1.08M of the added people are priced as
  third-plus whites at G3+ ages. [CALCULATION: `c6_generation_break_even_oct05.csv`, from
  `generation_account_2026_09_24/derived/generation_corrections_oct05.json` and `generation_results_oct05.csv`]
- **C7 and C9** take no v5 input.
- **C8 and C5's winner share** are not rerun here: the comparators' and the winners lane's oct05 runs belong to other
  lanes [GAP].
  - An added person costs others $6,309–8,790 against $2,274–3,472 for a third-plus white at the same ages, so putting
    both sides on 42.75M widens C8's gap [INFERENCE: direction only].

### Premises on v5

| Rank | Premise | Conclusions | Swapped for its best-supported alternative |
|---|---|---|---|
| 1 | P01 survey frame, 39.71M identified | 9 | Not rerun on v5; on September 27, C1 −0.7%. Breaks none [INFERENCE]. |
| 2 | P02 one income year | 8 | First-year horizon: **C1 −26.7%, breaks**; the pairing, about −21%, holds. **Breaks one.** |
| 3 | P08 dataset corrections | 7 | Uncorrected, the union's accrual rebuilt: C1 +2.6%; C2 tally +$11.1 / 0.4bn, which holds at both ends. Breaks none. |
| 4 | P03 long-run responses, property levies included | 6 | Schools at 0.836: C1 −6.4% (property taxes at zero instead, +7.1%). Breaks none. |
| 5 | P05 pensions on accrual at payable benefits | 6 | Cash: **restores C2** (tally +$89.4 / 73.4bn), C1 −18.9%, C5 82–87%. Breaks none. Scheduled benefits instead: C1 +8.5%, tally −$30.7 / −39.3bn. |
| 7 | P20 the lineage count (new on v5) | 6 | Arms a and c: C1 −2.8% / +2.8%; C2's split holds. Breaks none. By ancestry share: C1 −17.5% to −29.8%, a break at the bound's low end [FRAMING-SENSITIVE]. |

P07 (keys) ties at 6 and ranks sixth, as before. P20 ranks seventh on the tie-break. [CALCULATION and INFERENCE as marked
in `common_mode_oct05.csv`]

### Rules for v5

1. **A case flag in `engine_breaks_sept29.cjs`, and a new `tables_oct05.py`.** `--case oct05` swaps the package path to
   `main_case_2026_10_05`, the oracle band, the cash payload and the generation files, and writes `*_oct05.csv`. The
   sept29 run is byte-identical (rerun gate). Justification: v5 has v4's package API, so the engine computations are
   v4's plus the lineage's handling; a copy would duplicate about 400 gated lines. This departs from v4's rule 1 (separate
   scripts), whose reason was new arms and gates for a new item set. The conclusions' prose is per case, so it gets its
   own script. Alternative: `engine_breaks_oct05.cjs` as a copy.
2. **Cash pensions run on the cash set's package.** v5's package blocks `pension4: "cash"` (its lineage is priced with
   the pension switch on), so the cash arm, its combinations and the first-year cash row run on `P.CASH` with the other
   options. Gate: `P.CASH`'s payload is `derived/corrections_cash.json`.
3. **The lineage's alternatives enter C1 as band changes.** Each is the change of its band from the central arm's in the
   lineage lane: on the set, or on the cash set when cash pensions are in the combination. Each is added to the engine
   part [APPROX: additive; the change at the case's options], at most one per combination, since they are alternative
   counts. Searched: arms a and c, C3 ± 1 SE (from the C3 line), the ancestry-share count at its bound's two ends and
   at the population lane's convention, and the replacement child at r = 1. The replacement child at r = 0.5 is listed,
   dominated. The ancestry-share and replacement rows are [FRAMING-SENSITIVE] readings, beside the whole-person central.
   Gates: the central arm is the case (5e-6) and its cash set (5e-5); the C3 line gives both at C3 (1e-6).
4. **Scheduled benefits raise the lineage's accrual in the union's proportion** [ASSUMPTION]. The union's rule applies
   to the union's OASDI receipts (the case's, less the lineage's). The lineage's Social Security accrual (k = 0.9534 /
   0.9582 of its OASDI receipts) is raised by 1.2406 / 0.9737, and its Part A accrual by 45.35 / 41.14. The result is
   +$37.17 / 34.90bn, against +$34.21 / 32.38bn on v4.
5. **C3 holds the lineage's edits in every run.** The union's pension switch is rebuilt on each subset, and the
   lineage keeps its own accrual. Social Security is ratio_net × (the model's OASDI receipts less the lineage's) plus
   the lineage's; Medicare is (1 − part_a_share) × the union's pre-switch amount plus the Part A accrual plus the
   lineage's edit. Gate: the rebuild moves nothing on the full payload (1e-9). [GAP] The lineage's amounts are not
   re-priced without the corrections.
6. **C2 at arms a and c from the lineage lane's per-line costs.** `lineage_lines.csv` (v5_bn: v4's line, the union's
   response move and the added people's parts, at each arm's responses and ends) is classed as the case's evaluation
   classes each line. Gate: arm b gives the case's receipts and transfers at both ends (1e-4, the file's six decimals).
   `union_at_case_responses` is v4's payload with row 8's move, at v5's specifications.
7. **The first-year rule's positive control runs on the September 29 package** (`P.BASE`). With the lineage on and every
   v4 item off, the September 27 row has no meaning.
8. **Inputs from other lanes' oct05 runs, uncommitted at this run.** C4 reads `sept24_propagation_2026_09_24/derived/oct05/`
   (consumer group C), and C5 reads `debt_legacy_2026_09_23/derived/oct05/` (this group). C6 reads the generation account's
   oct05 files (committed in e5ca5efe; sha256 in `c6_inputs_oct05.csv`). `tables_oct05.py` recomputes every quoted
   number, so a changed input stops the build. [2026-10-06, the lead: both were then committed, the debt legacy in
   604b09e1 and the pairing in 72f2e3bc; on them the two oct05 commands pass and rewrite every `*_oct05.csv` byte for
   byte.]

### Gates

1. `engine_breaks_sept29.cjs --case oct05`: 49 of 49 gates, including the oracle 390.2940 / 461.2431 and the cash set
   307.3764 / 383.4093 at 1e-4. The September 29 run passes 41 of 41, and its seven files are byte-identical.
2. `tables_oct05.py`: every check passes. Two text figures were wrong on the first build (52.6% for 52.5%, and 3.6 points
   for 3.5); the checks stopped the build, and both were fixed in the text.
3. `scripts/rerun_lane.py` with the six commands below: IDENTICAL 31/31 files, rc 0 (2026-10-06 00:41 JST). No tracked
   file in `derived/` differs from HEAD.

### Reproduce

```sh
node infra/immigration-fiscal/break_conditions_2026_09_29/engine_breaks_sept29.cjs --case oct05
uv run --no-project --offline python3 infra/immigration-fiscal/break_conditions_2026_09_29/tables_oct05.py
# the whole lane: engine_breaks.cjs, tables.py, engine_breaks_sept29.cjs, tables_sept29.py, then the two lines above
```

### Log (append-only; times from `date`)

- 2026-10-06, after 00:21 JST (the last `date` before this lane started): scripts read, and the September 29 run
  reproduced in a scratch copy (41 gates, seven files identical).
- 2026-10-06 00:41 JST: `--case oct05` passes 49 gates and `tables_oct05.py` builds; the rerun is IDENTICAL 31/31, rc 0.
- 2026-10-06 00:43 JST: this section written.

## v6 case (oct07), 2026-10-07

[Round 2, later on 2026-10-07: the comparators' income taxes moved to the case's own keys, and C8 now breaks upward at
both ends. This section's C8 figures use the CPS-dollar rule; the current ones are in "v6 round 2" below. C1's lineage
rows then moved from rule 5's v5 changes to the case lane's own v6 companions (below, "C1's lineage rows on v6's own
companions"): the ancestry-share count's low end now gives −30.0%, arms a and c −3.2% / +3.2%, and the minimal cuts
number 158; no status changes.]

[Round 3, 2026-10-08: C8 now tests the map's live claim, about $434bn against third-plus whites and $530bn against
local whites, and holds; at the central only C2 breaks ("v6 round 3" below).]

claude-opus-5-5 (v6 propagation, group D, prop-d). **Verdict (v6).** Main case v6 (`../main_case_2026_10_07/`,
$389.08–461.48bn) adds four items to v5: pensions on the 2026 Trustees' separate funds, state-local retiree health on
accrual, the added people at their measured ages, and user fees with education keyed by use. No conclusion changes
status. C2 still breaks at the high end and holds at the low end: the tally is +$6.2 / −5.3bn (v5 +$6.5 / −4.4bn), and
one tail still decides each end. C1 restates to $389.1–461.5bn (midpoint $425.3bn, −0.1% on v5). The first-year horizon
alone still breaks it (−26.5%), and so does the ancestry-share count at its stated bound's low end (−29.9%)
[FRAMING-SENSITIVE]. One downward pair from v5 no longer breaks it: schools at 0.836 with cash pensions falls 0.05
points short (−24.95%). The items' ten arms each move C1 by less than 2% and enter minimal cuts only as a third or later
step. C3 is within $0.26bn of v5's. C4, C5 and C6 hold with v6's figures, and C5's "one in six" now reads 17.5% / 16.8%
on the winners lane's oct07 run. C8 restates on the IPEDS keys at $380.3–433.1bn from US to local whites, with the
comparators' hospital term beside. C7 and C9 take no v6 input. [CALCULATION: `engine_breaks_sept29.cjs --case oct07`,
`tables_oct07.py` → `derived/*_oct07.csv`, written in place at "v6 final"]

### The nine conclusions on v6

The claims are still the map's, on the September 27 case. Full cells are in `derived/conclusions_oct07.csv`, and the
premise matrix is in `derived/common_mode_oct07.csv`.

| | Claim (the map) | On v5 (oct05) | On v6 (oct07) | Status on v6 |
|---|---|---|---|---|
| C1 | about $355bn a year | $390.3–461.2bn, midpoint $425.8bn | $389.1–461.5bn, midpoint $425.3bn | holds, restated |
| C2 | taxes cover benefits; services decide the sign | tally +$6.5 / −4.4bn; break-even −8.8% to +5.5% | tally +$6.2 / −5.3bn; break-even −9.05% to +5.38% | **breaks at the high end**, holds at the low end |
| C3 | ~$50bn each, net ~$11bn | +$44.43 / 45.84bn, −$55.16 / 57.15bn, net −$10.73 / 11.31bn | +$44.43 / 45.84bn, −$54.92 / 56.89bn, net −$10.49 / 11.05bn | holds |
| C4 | the add, about $100bn | $104.8 / 109.4bn; pairing $490.2–570.7bn | $104.7 / 109.2bn; pairing $489.0–570.7bn | holds |
| C5 | most (85%); one in six gains | 68.8% / 68.2%; 17.6% / 16.9% | 68.6% / 68.0%; 17.5% / 16.8% | holds |
| C6 | each generation costs others | at least $87.0bn; break-evens at most 21.6% | at least $86.7bn; at most 21.7% | holds |
| C7 | status explains little | no v5 input | no v6 input | unchanged |
| C8 | $320–405bn more than as many whites | A1 $373.9 / 376.8bn on the IPEDS keys (white lane) | A1 $380.3 / 384.7bn; local whites $430.3 / 433.1bn | holds, restated |
| C9 | offending and custody | no v5 input | no v6 input | unchanged |

C5's v5 winner shares are the winners lane's oct05 run (c1c259ef), which this lane's v5 section did not read. C8's v5
figure is the white lane's oct05 re-key rebuilt on the IPEDS keys in this propagation (it was $368.8 / 371.9bn on the
rough keys).

### C2 on v6

| $bn, ends 48 / 11 | Direct receipts | Household transfers | Tally |
|---|---:|---:|---:|
| v6 case: accrual at payable benefits (2026 Trustees' separate funds) | 449.5 / 421.5 | 443.3 / 426.8 | **+6.2 / −5.3** |
| cash set: pensions as 2024 cash | 451.9 / 423.5 | 364.0 / 352.7 | +87.9 / +70.8 |
| v4's and v6's items and the lineage without the dataset corrections (the union's accrual rebuilt) | 494.2 / 467.7 | 483.2 / 467.9 | +11.0 / −0.2 |
| uncorrected, no v4 items, no lineage | 444.8 / 424.5 | 378.4 / 370.0 | +66.4 / +54.5 |

The cash set's low-end receipts (451.85) print as 451.9 and the uncorrected-items low-end transfers (483.15) as 483.2,
so the rows add. The tally splits into the union alone at v6's responses, −$3.7 / −13.3bn, and the added people's own,
+$9.9 / +8.0bn (unrounded 7.93; it prints 8.0 so the parts add). Against v5 the tally falls $0.30 / 0.95bn. The items'
union parts raise the union's transfers by $0.35 / 0.65bn, with its receipts unchanged. The added people's own parts
(their measured ages and the items' lineage parts) lower their direct taxes by $0.93 / 2.49bn and their transfers by
$0.98 / 2.19bn. Arm a (1.81M added) gives +$4.3 / −6.3bn and arm c (4.27M) gives +$8.1 / −4.4bn [APPROX: rule 5]. At scheduled benefits on the 2026 inputs the transfers rise another
$43.3 / 40.5bn (v5 $37.2 / 34.9bn on the 2025 reports), and the tally is −$37.1 / −45.8bn. [CALCULATION:
`c2_tally_oct07.csv`, against `c2_tally_oct05.csv`]

One tail decides each end [INFERENCE: additive, `components.csv`]. At the high end, care's favorable tail alone restores
clause 1 (+$3.9bn). The tax block's favorable tail falls $1.09bn short alone (v5: $0.15bn), and with any one more tax or
transfer tail it restores clause 1, by $0.08bn or more (medical's the least). At the low end, the MCBS 65+ bound on
medical alone breaks it (−$2.3bn); the tax block's adverse tail leaves +$0.6bn.

| Break-even service response | Personal, most / least adverse | Shared, most / least adverse |
|---|---:|---:|
| v6 case, enterprise surplus at 1 | −9.05% / −0.66% | −7.03% / +1.58% |
| v6 case, enterprise surplus at s | −3.65% / +3.16% | −1.63% / +5.38% |
| cash set, enterprise surplus at 1 | 8.32% / 17.26% | 11.94% / 21.14% |
| cash set, enterprise surplus at s | 12.86% / 20.40% | 16.38% / 24.19% |

The table prints two decimals because the file's four (−0.0905) do not settle the first decimal of −9.05%. Clause 2
survives only at the least adverse end: below a 1.58% response with the enterprise surplus at 1 (shared), or
3.16–5.38% with it at s. [CALCULATION: `c2_break_even_oct07.csv`; the case's rows reproduce
`main_case_2026_10_07/derived/sign_reversal.csv` at 1e-4]

### What moved in the other conclusions

- **C1.** The cut is a quarter of the $425.3bn midpoint: below $319.0bn or above $531.6bn.
  - **Downward, one step.** The first-year horizon alone gives $288.9–336.5bn (−26.5%, clearing the cut by 1.5 points;
    −33.5% with item 5's long-run response kept, −45.0% with cash pensions as well, $207.3–260.3bn). The ancestry-share
    count at its stated bound's low end alone gives $274.2–322.4bn (−29.9%) [FRAMING-SENSITIVE].
  - **Downward with whole people.** Cash pensions (−18.6% alone) plus one alternative break it: no capital return
    ($270.8–324.3bn, −30.0%) or first-year roads and parks ($277.0–335.3bn, −28.0%). Schools at 0.836 with cash
    pensions, a pair on v5 (−25.3%), now falls 0.05 points short ($279.6–358.8bn, −24.95%) and takes a third: care low
    (−27.1%), the age mix by birth cohort (−26.3%) or retiree health at ρ = 1 (−25.3%). Without cash pensions it takes
    four (no capital return + schools at 0.836 + first-year roads and parks + care low, −26.3%). At the population
    lane's convention for the ancestry share (−19.3% alone), one more alternative breaks it: no capital return
    (−30.7%), cash pensions (−33.9%), first-year roads and parks (−28.7%) or schools at 0.836 (−25.7%).
  - **Upward.** It takes two, both with 7% capital (+20.3% alone): + defense by GDP share (+34.4%), + scheduled benefits
    (+30.2%) or + property taxes at zero (+27.4%). Without 7% it takes three: scheduled benefits + defense + property
    taxes at zero (+31.0%), + the largest long-run response (+27.1%) or + the MCBS 65+ bound (+26.0%).
  - **The lineage's own alternatives.** Arms a and c move it −2.8% / +2.8%, C3 ± 1 SE ∓0.8%, the replacement child
    (r = 1) −2.1% [FRAMING-SENSITIVE], and the ancestry-share count −17.5% to −29.9% across its bound.
  - **The items' arms** (new on v6). Each of the ten moves it by less than 2%: the age mix by birth cohort −1.8%, the
    age mix on rough keys +0.1%, retiree health's six −0.3% to +0.5%, the 2026 inputs on combined trust funds +0.3%. They
    enter 91 of the 165 minimal cuts, always as a third or later step [APPROX: additive].
  - **Stacks.** All 10 downward alternatives −51.9% (−75.9% with the ancestry share); all 9 upward +57.4% (+60.1% with
    arm c).
  - [CALCULATION: `c1_arms_oct07.csv`, `c1_min_cuts_oct07.csv`]
- **C3.** Taxes move +$44.43 / 45.84bn, as on v5, and spending −$54.92 / 56.89bn, so the net is −$10.49 / 11.05bn, with
  no interaction. The spending move includes the accrual following the corrected OASDI receipts, −$10.44 / 11.23bn,
  which is $0.22 / 0.24bn smaller than on v5 because the pension item lowers the accrual per OASDI tax dollar from
  0.9737 to 0.9535. With every increment held instead: −$55.27 / 56.89bn, net −$10.84 / 11.05bn. The tails findings
  hold: the net moves by more than a quarter on any one of six data-component tails (five at the low end), and the
  near-cancellation fails with care low + tax block low (−$25.2 / 24.5bn), or with care low alone counted by the edits'
  side (−$19.7 / 20.2bn). [GAP] The added G3+ members are priced on the corrected G3+ model, so the split leaves out
  the corrections their amounts carry. [CALCULATION: `c3_correction_split_oct07.csv`]
- **C4.** The social rows are $104.7 / 109.2bn; the added people's own rows are $8.4 / 8.5bn (v5 $8.6 / 8.8bn), their
  key shares read at their measured ages. The pairing is $489.0–570.7bn ($11,438–13,349 per member of
  42.75M). One item at a range end still breaks the add (a quarter ≈ $26.7bn): PM2.5 −$38.2 / +52.8bn, crashes
  −$68.7 / +63.3bn, scale net ∓$70.5bn. The pairing (below $397.4bn or above $662.3bn) needs crashes and scale net
  together (−26.3% / +25.2%); PM2.5 high plus crashes high reaches +21.9%. The first-year horizon moves the pairing
  about −21.2% with the social rows held, and the cash set pairs to $407.3–494.6bn (−14.9%). [DATA:
  `sept24_propagation_2026_09_24/derived/oct07/real_costs_totals.csv`; INFERENCE: additive]
- **C5.** State and local taxpayers pay 68.6% / 68.0%. The accrual ($81.7 / 76.1bn) is all federal; on the cash set the
  share is 86.8% / 81.5%. "Most" survives defense by GDP share (59.4% / 60.2%), plus legacy interest ($31.8 / 44.2bn,
  55.5% / 55.5%), plus scheduled benefits as well (50.9% / 51.8%). It fails with defense and old interest at average cost
  (40.4% / 42.9%). Pooled within SPM units, 17.5% of other residents come out ahead under tax-share financing and 16.8%
  per person (v5 17.6% / 16.9%), against 16.7% for "one in six". [CALCULATION: additive on
  `debt_legacy_2026_09_23/derived/oct07/federal_split_2024.csv`, central convention; DATA:
  `winners_losers_2026_09_24/derived/oct07/net_shares.csv`]
- **C6.** Every generation costs others at both ends under both conventions: at least $86.7bn, or $72.7bn on the cash
  set. G3+ carries the added people: $141.8 / 196.8bn under convention a (v5 $141.7 / 195.0bn). Its largest break-even
  is 16.8% (a) and 21.7% (b), 3.5 / 3.2 points above v4's; on the cash set at most 38.4% (a) and 42.2% (b). On the
  case, G1's break-evens under b stay negative at every end and allocation. [CALCULATION: `c6_generation_break_even_oct07.csv`,
  from `generation_account_2026_09_24/derived/generation_corrections_oct07.json` and `generation_results_oct07.csv`]
- **C8.** With both sides on the lineage's 42.75M, the union costs others $380.3 / 384.7bn a year more than as many
  third-plus non-Hispanic whites at national rates ($8,896 / 8,998 per member), and $430.3 / 433.1bn more than local
  whites state by state at union ages. That is +19.5% on the claim's $320bn and +6.6% on its $405bn, within a quarter at
  both ends.
  - **Up.** The two case conventions together (the CPS top tail of income tax spread in proportion, capital-side taxes
    responding) give $492.8 / 498.3bn (+29.6% on A1), which crosses a quarter; alone +10.7% and +18.8%.
  - **Down.** Cash at whites' own ages gives $212.2 / 218.6bn (−43.7%), the age artefact the accrual removes. White
    rates at the union's ages (A3) give $356.6 / 361.0bn (−6.2%).
  - **The keys.** Both sides take Pell by each group's IPEDS share and public higher education by measured use, and on
    v6 tuition by use (rule 7). The comparators' hospital term stays beside; with it A1 is $383.0 / 387.3bn. On the
    September 27 rough keys A1 is $373.8 / 378.2bn.
  - **Against an all-residents slice** on the same rough keys the union is $221.3 / 226.6bn above average on the
    case's accrual and $121.6 / 129.0bn on cash. The rough keys put the union 1.6% above the engine's at the low end and
    1.8% below it at the high end.
  - [CALCULATION: `white_replacement_2026_09_28` `headline_oct07.csv`, `rekey_summary_oct07.csv`,
    `ipeds_terms_oct07.csv`]
- **C7 and C9** take no v6 input.

### Premises on v6

| Rank | Premise | Conclusions | Swapped for its best-supported alternative |
|---|---|---|---|
| 1 | P01 survey frame, 39.71M identified | 9 | Not rerun on v6; on September 27, C1 −0.7%. Breaks none [INFERENCE]. |
| 2 | P02 one income year | 8 | First-year horizon: **C1 −26.5%, breaks** ($288.9–336.5bn); the pairing, about −21%, holds. **Breaks one.** |
| 3 | P08 dataset corrections | 7 | Uncorrected, the union's accrual rebuilt: C1 +2.5% ($399.6–472.5bn); C2 tally +$11.0 / −0.2bn, which holds at the low end only, as on the case (v5's swap held it at both). Breaks none. |
| 4 | P03 long-run responses, property levies included | 6 | Schools at 0.836: C1 −6.4% ($361.3–434.9bn; property taxes at zero instead, +7.0%); the pairing about −5%. Breaks none. |
| 5 | P05 pensions on accrual at payable benefits (2026 Trustees' separate funds), retiree health on accrual | 6 | Cash: **restores C2** (tally +$87.9 / 70.8bn), C1 −18.6%, C5 82–87%, C8 $364.9–371.2bn at the union's ages. Breaks none at the union's ages. Scheduled benefits instead: C1 +9.9%, tally −$37.1 / −45.8bn. |
| 7 | P20 the lineage count, the added people at their measured ages (v6's item 3) | 6 | Arms a and c: C1 −2.8% / +2.8%; C2's split holds. At the identified G3+'s ages (v5's rule): C1 −0.5%. By ancestry share: C1 −17.5% to −29.9%, a break at the bound's low end [FRAMING-SENSITIVE]. |

The ranking is v5's: P07 (keys) ties at 6 and ranks sixth, and P20 ranks seventh on the tie-break. [CALCULATION and
INFERENCE as marked in `common_mode_oct07.csv`]

### Rules for v6

1. **The same case flag, a new tables script.** `--case oct07` swaps the package path to `main_case_2026_10_07`, the
   oracle band (389.0826 / 461.4797), the cash payload (307.3994 / 385.3641) and the generation files, and writes
   `*_oct07.csv`. The sept29 and oct05 runs rewrite their 14 files byte for byte. v6's package has v5's API, so v5's
   rule 1 carries over; the conclusions' prose is per case, so it gets `tables_oct07.py`.
2. **The items' edits are held in every C3 run**, after the lineage's, as v5 holds the lineage's.
3. **The pension item's parts follow their owners.** Its cell shifts on Social Security and Medicare split into union
   parts, which join the union's rebuilt switch, and lineage parts, which join the lineage's own accrual. Gate: the
   rebuilt switch is the case on the full payload.
4. **Scheduled benefits on the 2026 inputs** [ASSUMPTION]. The case's scheduled-benefits arm stays on the 2025 reports
   (net 1.2406 per OASDI tax dollar), and the case's payable arm is on the 2026 reports (0.9535), so scheduled less
   payable would mix two years. `scheduled_tr2026.py` rebuilds the scheduled arm on the 2026 inputs the payable arm
   reads: net 1.2568, Part A $46.56bn against $40.78bn payable. Gates: on the 2025 inputs the same code gives the case's
   scheduled arm (1e-6) and the pension lane's scheduled Part A; on the 2026 inputs at payable benefits it gives the
   case's ratio_net and Part A (5e-9). The rule's positive control stays on the 2025 values, where it reproduces the
   pension lane's scheduled less payable ($34.36 / 32.54bn, 1e-6). The scheduled move is +$43.29 / 40.49bn (v5
   +$37.17 / 34.90bn).
5. **The lineage's alternatives are v5's changes** [APPROX: additive; ASSUMPTION: each moves v6 as it moves v5]. The
   lineage lane prices no v6 arm. C1 adds each one's change from v5's lineage central, and the tally's arms a and c are
   v5's lines moved by the case's change from v5.
6. **The items' arms enter C1.** `summary.json` `v6.arms` gives ten: the 2026 inputs on combined trust funds, retiree
   health's six, and the age mix at birth cohorts and on rough keys. Each is its band's change from the case, on the set
   or on the cash set when cash pensions are in the combination [APPROX: additive], at most one per item in a
   combination; the stacks take each item's largest arm in their direction. The union at the case's responses carries
   the items' union parts (`engine_lines.cjs`'s rule).
7. **C8 on the IPEDS keys** [ASSUMPTION] (the lead's decision of 2026-10-07, a named defect fix). Both sides of every
   comparison take Pell by each group's IPEDS share and public higher education by measured use, and on v6 item 4's
   tuition by use. The comparators' hospital term is beside the central (the lead's later decision of 2026-10-07): its
   fee side would take MEPS hospital use that the comparators' spending side never charges. The white lane's v6 section
   holds the rule, its parts and the hospital term beside.
8. **Inputs from other lanes' oct07 runs.** C4 reads the pairing (`sept24_propagation_2026_09_24/derived/oct07/`,
   committed in b0a2ccac), C5 the debt lane's split (0485e5a2) and the winners lane's oct07 run (f2d96008), C6 the
   generation account's oct07 files (3f583fb4; sha256 in `c6_inputs_oct07.csv`), and C8 the white lane's oct07 re-key
   (this propagation, final at 16:58:52). `tables_oct07.py` recomputes every quoted number, so a changed input stops the
   build.

### Gates

1. `engine_breaks_sept29.cjs --case oct07`: 61 of 61 gates, including the oracle and the cash set at 1e-4, the scheduled
   helper's payload check and the case's break-evens against `sign_reversal.csv` at 1e-4. The sept29 run (41 of 41) and
   the oct05 run (49 of 49) rewrite their 14 files byte for byte (scratch copy, 16:01).
2. `scheduled_tr2026.py`: its gates pass. Rerun on the committed payload (1548b396), its numbers are unchanged; only the
   payload's sha256 in `derived/scheduled_tr2026.json` moves (b07e2a34 → f8d346aa), since the file was written on the
   payload before its commit. The in-place run at "v6 final" rewrote it so.
3. `tables_oct07.py`: every check passes on the engine outputs in `derived/`, which equal the scratch run's byte for
   byte. Its first build after the winners lane's oct07 run appeared stopped on C5's "no oct07 run" guard; C5 now reads
   that run. Since the hospital term moved beside, C8's checks read the white lane's final files, and two more check A1
   with the hospital term and the smallest arm. `tables_oct05.py`, rerun in place, rewrites its two files byte for byte.
4. `scripts/rerun_lane.py` over the whole lane: see the log.

### Reproduce

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/break_conditions_2026_09_29/scheduled_tr2026.py
node infra/immigration-fiscal/break_conditions_2026_09_29/engine_breaks_sept29.cjs --case oct07
uv run --no-project --offline python3 infra/immigration-fiscal/break_conditions_2026_09_29/tables_oct07.py
# the whole lane: engine_breaks.cjs, tables.py, engine_breaks_sept29.cjs, tables_sept29.py, the oct05 pair, then the three lines above
```

### Log (append-only; times from `date` or the files' clock)

- 2026-10-07 13:23 JST (file time): `scheduled_tr2026.py` written; 13:42:46 its `derived/scheduled_tr2026.json`, on the
  payload before the case's commit.
- 2026-10-07 13:55:42 JST: the first `--case oct07` run in a scratch copy (45 gates); 15:23:10 the run with the items'
  arms and the committed generation files, 61 gates.
- 2026-10-07 15:28:46 JST: `tables_oct07.py` with C4–C6 builds on the scratch outputs.
- 2026-10-07 15:58:32 JST: the build stops on C5's guard (the winners lane wrote `derived/oct07/` at 15:41); C5 now reads
  it, and at 16:00:01 the build passes.
- 2026-10-07 16:01:10–16:01:21 JST: the sept29 and oct05 runs in scratch, 14 files byte-identical to `derived/`; 16:03:40
  the scheduled helper on the committed payload, numbers unchanged; 16:04:05 the oct07 run again, seven files identical
  to 15:23's.
- 2026-10-07 16:06 JST: this section written. Nothing in `derived/` carries oct07 output yet except
  `scheduled_tr2026.json`.
- After 16:06: the team lead declared v6 final and took the comparators' hospital term out of their central (beside).
  C8's checks and text in `tables_oct07.py` follow the white lane's final files (16:58:52).
- 2026-10-07 17:05:55–17:06:31 JST (by `date`): in place, `scheduled_tr2026.py` (payload sha256 f8d346aa),
  `engine_breaks_sept29.cjs --case oct07` (61 of 61 gates; its seven files equal the 16:04 scratch run's byte for byte)
  and `tables_oct07.py` (every check passes; C2 the only break). `conclusions_oct07.csv` differs from the scratch build
  only in C8's three text cells and `common_mode_oct07.csv` only in P05's swap cell.
- 2026-10-07 17:08:40–17:09:37 JST (by `date`): `rerun_lane.py` with all nine commands (`engine_breaks.cjs`,
  `tables.py`, the sept29 pair, the oct05 pair, `scheduled_tr2026.py` and the oct07 pair): **IDENTICAL 43/43, exit 0**.

## v6 round 2: C8 on the case's income-tax keys, 2026-10-07

claude-opus-5-5 (prop-d). **Verdict (round 2).** Every comparator's income taxes now take the case's own keys (the
white lane's section "v6 round 2"), and **C8 breaks upward at both ends**: the gap is larger than claimed.
- The union costs others $431.6 / 436.0bn a year more than as many third-plus non-Hispanic whites at national rates,
  $10,096 / 10,197 per member, and $528.6 / 531.5bn more than local whites state by state at union ages. That is +35.6%
  on the claim's $320bn and +30.9% on its $405bn.
- The deciding premise is P07, the keys. On the CPS-dollar rule, which charged a group only the income tax it reports
  to the CPS and, on the comparators' frame, charged $395.9bn of federal and $39.4bn of state income tax to no one, A1
  was $380.3 / 384.7bn, +19.5% on $320bn. [DATA: white lane `cps_tax_totals_oct07.csv`, frame row 4, the rough keys]
- [INFERENCE] The claim's figures came from that rule on the September 27 case, so the break is the key change, not new
  data.

Two conclusions now break at the central, C2 and C8. No other conclusion reads a comparator figure, and none moves.
[CALCULATION: `tables_oct07.py` → `derived/conclusions_oct07.csv`, `common_mode_oct07.csv`, on the white lane's round-2
`headline_oct07.csv`, `rekey_summary_oct07.csv`, `ipeds_terms_oct07.csv` and `income_tax_keys_oct07.csv`]

| | Claim (the map) | On v6, the CPS-dollar rule | On v6, round 2 | Status |
|---|---|---|---|---|
| C8 | $320–405bn more than as many whites | A1 $380.3 / 384.7bn; local whites $430.3 / 433.1bn | A1 $431.6 / 436.0bn; local whites $528.6 / 531.5bn | **breaks upward at both ends** |

- **Back inside a quarter.** Two arms bring it back:
  - The CPS-dollar rule: A1 $380.3 / 384.7bn, +19.5% on $320bn.
  - Cash at whites' own ages: $263.5 / 269.8bn, −38.5% on A1 and −16.7% on $320bn. This is the age artefact the
    accrual removes.
- **Still broken.**
  - CPS income-tax dollars spread over the national lines in proportion give $421.4 / 425.8bn (−2.3% on A1).
  - White rates at the union's ages (A3) give $411.4 / 415.7bn (−4.7%).
  - Capital-side taxes responding give $503.0 / 508.5bn (+16.6%). With the top tail inside the central, this is also
    the both-arms figure.
  - The comparators' hospital term gives $434.3 / 438.6bn, and the September 27 rough keys $425.1 / 429.5bn.
  - The ordering holds in every arm: the smallest is $263.5bn.
- **P05's swap on C8** (cash). A3 is $419.6–425.9bn (+4.4% on $405bn) and local whites $554.1–559.0bn (+37.4%). At
  whites' own ages it is $263.5–269.8bn (−16.7% on $320bn). Of C1–C6 the swap breaks none at the union's ages. C8,
  broken upward at the central, stays broken against local whites.
- **Against an all-residents slice** the union is $261.8 / 267.2bn above average on the case's accrual and $162.2 /
  169.5bn on cash.
- **The rough union and the engine's.** The rough keys put the union 2.3% below the engine's at the low end and 5.0% below
  at the high end, because on the same keys the engine's union pays less income tax. The case scales the union's income
  taxes by union-only corrections (the tax-records stack), which no comparator takes. At the high end it also gives each
  earner their own income tax, where the comparators share it over the household.
- **The allocation, beside the central.** At the personal allocation A1 is $448.7 / 453.1bn, so C8 breaks under either
  allocation. A3 falls to $364.1 / 368.4bn there (the white lane's round-2 section).

**Rule 9 (round 2): C8 on the case's income-tax keys** [ASSUMPTION]. This follows the lead's instruction of 2026-10-07,
which the operator approved at 19:44 JST.
- Every group takes federal income tax on v4 item 3's IRS-raked key, and state and other personal taxes on the
  state-liability key, at the shared allocation.
- No group takes a union-only correction.
- The CPS-dollar rule stays as an arm. `tables_oct07.py` checks each quoted number against the white lane's files.
- `tables_oct05.py` is unchanged: its C8 cites the September 29 headline, which round 2 leaves alone. Rerun in place,
  it rewrites its two files byte for byte.

**Gates.** `tables_oct07.py` exits 0 on the round-2 files, and every check passes, including the C8 arms, the CPS-dollar
rule, the rough union against the engine's and the smallest arm. Its tally reads: broken at the central, C2 and C8.
`engine_breaks_sept29.cjs` reads no comparator file, so its outputs are the v6 section's.

**Files.** Changed: `derived/conclusions_oct07.csv` (C8's row) and `derived/common_mode_oct07.csv` (P05's swap cell);
`tables_oct07.py` (C8's checks and text, and the P05 cell).

### Log (round 2; times from `date` or the files' clock)

- 2026-10-07 20:26:52 (log time): `tables_oct07.py` and `tables_oct05.py` ran in place on the white lane's round-2
  files, exit 0. oct07's two files changed and oct05's did not.
- 20:53:51 (by `date`): C8's text on the rough union against the engine's now names the tax-records stack;
  `tables_oct07.py` reran in place, exit 0. Only that cell of `conclusions_oct07.csv` changed.
- 21:15:48–21:16:46 (by `date`): `rerun_lane.py` with the v6 section's nine commands, after the four comparator lanes'
  round-2 reruns: **IDENTICAL 43/43, exit 0**.

### C1's lineage rows on v6's own companions (round 2, later on 2026-10-07)

claude-opus-5-5 (prop-d). The v6 section's rule 5 carried the lineage's alternatives to v6 as v5's changes, because the
lineage lane prices no v6 arm. The case lane does: `main_case_2026_10_07/derived/summary.json` `v6.companions` holds
the count's arms a and c, C3 ± 1 SE and the ancestry-share count at its stated bound, each on the set and the cash set,
with every item rebuilt on the option's lineage. C1 now reads them. **No status changes.** C1 holds, restated; the
first-year horizon and the ancestry-share count's low end each still break it alone; C2 and C8 are still the only
breaks at the central, and the top five premises are still P01, P02, P08, P03 and P05. [CALCULATION:
`engine_breaks_sept29.cjs --case oct07`, `tables_oct07.py` → `derived/c1_arms_oct07.csv`, `c1_min_cuts_oct07.csv`]

| C1 alternative, $bn | Rule 5 (v5's change) | v6's own | Move on the midpoint |
|---|---|---|---|
| Ancestry share, the stated bound's low end | 274.18–322.36 | 274.87–320.84 | −29.9% → −30.0% |
| Ancestry share, the stated bound's high end | 325.47–376.05 | 325.20–374.79 | −17.5% → −17.7% |
| Ancestry share at the population lane's convention | 319.23–367.48 | 319.01–366.27 | −19.3% → −19.4% |
| Arm a (1.81M added) | 379.16–447.79 | 378.00–445.25 | −2.8% → −3.2% |
| Arm c (4.27M added) | 398.99–475.16 | 400.16–477.70 | +2.8% → +3.2% |
| C3 + 1 SE | 386.09–457.53 | 386.25–457.59 | −0.8%, unchanged |
| C3 − 1 SE | 392.08–465.43 | 391.91–465.37 | +0.8%, unchanged |

- **The convention row** is the case lane's count on v6's generation costs (`ancestry_share.cjs` `rowsFor`, run
  read-only) at the population lane's shares, third-plus members at 0.6156. The case lane prints no convention row, so
  the same code is gated on the bound's two ends, which it does print.
- **The replacement child** (r = 1, −2.1%; r = 0.5, dominated) has no v6 counterpart, since it belongs to the frame the
  operator declined on 2026-10-05. Its rows stay v5's changes, and their source now says "v5 delta carried, not
  recomputed on v6".
- **Minimal cuts.** There are 158 (137 down, 21 up), against 165 (141, 24). The items' arms enter 81 of them, against 91,
  still always as a third or later step [APPROX: additive]. The larger moves of arms a and c and of the ancestry-share
  rows let smaller sets cross the cut, so 20 larger sets that contain one of them are no longer minimal; three
  downward sets with C3 + 1 SE, which now moves C1 slightly less, no longer cross it. With the ancestry share at the
  convention, one more alternative still breaks C1: no capital return −30.9% (was −30.7%), cash pensions −34.0%
  (−33.9%), first-year roads and parks −28.9% (−28.7%) or schools at 0.836 −25.8% (−25.7%).
- **Stacks.** All downward alternatives with the ancestry share give −76.0% (was −75.9%); all upward with arm c +60.6%
  (+60.1%). The stacks without the lineage's rows do not move (−51.9%, +57.4%).
- **Text.** C1's break condition, distance note ("3.2% at most"), rival reading ($275–375bn) and source, and P20's swap
  cell: arms a / c −3.2% / +3.2%, the ancestry share −17.7% to −30.0%, and per member $9,194–10,731 at the bound's low
  end against the case's $9,101–10,794 (`summary.json` `v6.companions`).
- **Still on rule 5.** C2's tally at arms a and c (+$4.3 / −6.3bn and +$8.1 / −4.4bn) is v5's lines moved by the case's
  change [APPROX]. The companions give each option's band, per-member cost and change from the case, not the direct-tax
  and transfer lines the tally needs.

**Gates.** `engine_breaks_sept29.cjs --case oct07` passes 69 of 69 (61 before):
- each of the four options is the case plus its change and `main_case_bands.csv`'s row, on the set and the cash set
  (1e-9; 5e-5);
- on each set, the ancestry-share count at the bound's two ends is `rowsFor`'s row (1e-9), `summary.json`'s (1e-6) and
  `main_case_bands.csv`'s (5e-5).

`tables_oct07.py` stopped on its first build after the engine run, on the old text (`[BLOCKED] ancestry_share_low low:
computed 274.8742, text says 274.18`), as its checks are meant to. After the text edits every check passes. The sept29
and oct05 runs do not take the new rows, and the rerun shows their files unchanged.

**Files.** Changed: `engine_breaks_sept29.cjs` (the oct07 lineage block and its header), `tables_oct07.py` (C1's and
P20's checks and text), and in `derived/`, `c1_arms_oct07.csv`, `c1_min_cuts_oct07.csv`, `conclusions_oct07.csv` (C1's
four text cells) and `common_mode_oct07.csv` (P20's swap cell).

**Log (times from `date` or the files' clock).**
- 21:50:12 (file time): `engine_breaks_sept29.cjs` edited. 21:50:27–21:50:48 (by `date`): `--case oct07` ran in place,
  69 of 69 gates, exit 0. Of its files, only `c1_arms_oct07.csv` and `c1_min_cuts_oct07.csv` changed.
- 21:51:24 (file time): `tables_oct07.py` stopped on the old text, as above. 21:53:48 (file time): after the text
  edits, exit 0, broken at the central C2 and C8, top five P01, P02, P08, P03, P05. `conclusions_oct07.csv` changed only
  in C1's four text cells, and `common_mode_oct07.csv` only in P20's swap cell.
- 22:00:54–22:01:48 (by `date`): `rerun_lane.py` with the nine commands: **IDENTICAL 43/43, exit 0**.

## v6 round 3: C8 on the map's live claim, 2026-10-08

claude-opus-5-5 (prop-d). **Verdict (round 3).** C8 now tests the evidence map's live sentence, and it **holds**.
Since 3834b1c8 the map prints C8 from its registry on v6: "Against as many third-generation whites, the group costs
others about $434bn (432–436) a year more. Against local whites, state by state, the gap is about $530bn (529–531)."
Its two records are this lane's A1 and local-whites centrals, so the central restates the claim.
- The break rule and the swaps are round 2's. A move of more than a quarter from the claim's figure for the same
  whites breaks it: $433.8bn (A1's midpoint) against third-plus whites, $530.1bn against local whites.
- Inside the accrual no arm reaches a quarter. The largest moves are capital-side taxes responding (+16.6%) and the
  CPS-dollar rule (−11.8%).
- Only P05's swap read at whites' own ages breaks it, downward: raw cash gives $263.5 / 269.8bn (−38.5%). That is
  the age artefact the accrual removes, and the map prints it beside the claim [FRAMING-SENSITIVE]. At the union's ages
  the cash swap holds: A3 −2.5% and local whites +5.0%.
- At the central the tally is C2 alone, which splits by end; the other eight hold.

[CALCULATION: `tables_oct07.py` → `derived/conclusions_oct07.csv`, `common_mode_oct07.csv`, on the white lane's
`headline_oct07.csv`, `rekey_summary_oct07.csv` and `ipeds_terms_oct07.csv`]

| C8 reading | $bn, specs 48 / 11 | Move on the claim's figure | Status |
|---|---|---:|---|
| central: third-plus whites (A1), accrual | 431.6 / 436.0 | 0 (the claim, $433.8bn) | holds |
| central: local whites state by state, union ages | 528.6 / 531.5 | 0 (the claim, $530.1bn) | holds |
| P07: each group charged only the income tax it reports to the CPS | 380.3 / 384.7 | −11.8% | holds |
| P07: CPS income-tax dollars spread over the national lines in proportion | 421.4 / 425.8 | −2.3% | holds |
| white rates at the union's ages (A3) | 411.4 / 415.7 | −4.7% | holds |
| capital-side taxes responding (with the top tail inside the central, also both arms) | 503.0 / 508.5 | +16.6% | holds |
| the comparators' hospital term (beside the central) | 434.3 / 438.6 | +0.6% | holds |
| the September 27 rough keys | 425.1 / 429.5 | −1.5% | holds |
| P05 on cash: A3 at the union's ages | 419.6 / 425.9 | −2.5% | holds |
| P05 on cash: local whites | 554.1 / 559.0 | +5.0% | holds |
| P05 on cash: at whites' own ages (raw cash) | 263.5 / 269.8 | −38.5% | **breaks downward** [FRAMING-SENSITIVE] |

The ordering holds in every arm: the smallest gap is $263.5bn. Against an all-residents slice the union is
$261.8 / 267.2bn above average. That is the rival reading, a different reference group, and is not tested against this
claim.

**Rule 10 (round 3): C8 follows the map's live claim** [ASSUMPTION]. This follows the lead's instruction of 2026-10-08
(only live cases).
- C8's claim is the map's `groups.py` sentence at `selection/f263/text`. `tables_oct07.py` fills it with the map's own
  `quantities.py`, imported read-only.
- The build stops if any of these happens:
  - the sentence no longer quotes `whites.gap_a1` and `whites.gap_local`;
  - the filled text is not the text the row quotes;
  - the why line beside it (`selection/f263/why`) no longer quotes `whites.gap_cash`, the raw-cash reading that
    breaks C8;
  - any of the three records (`whites.gap_a1`, `whites.gap_local`, `whites.gap_cash`) differs from its
    `headline_oct07.csv` row.
- The other eight rows keep the map's September 27 claims. `tables.py`, `tables_sept29.py` and `tables_oct05.py` and
  their files are untouched. The sept29 and oct05 claim sets still test "$320–405bn".

**Gates.** `tables_oct07.py` exits 0, and its tally reads: broken at the central, C2.
- New checks: the claim's two figures (433.78 and 530.05); the hospital term (+0.6%) and the September 27 rough keys
  (−1.5%) on the claim; P05's cash readings, A3 (−2.5%) and local whites (+5.0%), on the claim.
- Removed: the six checks against the September 27 figures ($320bn, $405bn), with the text that quoted them.
- Every other C8 check is unchanged.

**Files.**
- Changed: `tables_oct07.py` (its docstring, C8's checks, the C8 row and P05's swap cell).
- `derived/conclusions_oct07.csv`: 7 of the C8 row's 12 cells changed (the claim, status, deciding premise,
  reading, break condition, distance note and source).
- `derived/common_mode_oct07.csv`: only P05's swap cell changed.

### Log (round 3; times from `date`)

- 2026-10-08 02:04:41: `tables_oct07.py` ran in place, exit 0, broken at the central: C2. Against HEAD only C8's seven
  cells and P05's swap cell differ.
- 02:06:26–02:07:34: `rerun_lane.py` with the nine commands: **IDENTICAL 43/43, exit 0**.
- 02:08:15–02:10:11: this section written.
- 02:16:15: added the why-line guard and the `whites.gap_cash` record check. C8's distance note now quotes the map's
  own cash figure ($267bn, 263–270). `tables_oct07.py` ran in place, exit 0, broken at the central: C2. Against the
  02:04:41 outputs only C8's distance note differs.
- 02:16:46–02:17:42: `rerun_lane.py` with the nine commands: **IDENTICAL 43/43, exit 0**.
- 02:22:42–02:23:35: the docstring's date for the map's wording corrected (on v6 since 2026-10-07); `rerun_lane.py`
  with the nine commands: **IDENTICAL 43/43, exit 0**.
