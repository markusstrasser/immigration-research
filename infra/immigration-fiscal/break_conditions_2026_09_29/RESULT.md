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
