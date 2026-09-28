claude-opus-5-5

**Verdict:** On an accrual basis for Social Security (OASDI) and Medicare Part A, the September 27 case becomes
**$437.8bn / $497.8bn** at specifications 48 / 11 under the central arm, up $116.0bn / $110.4bn from
$321.8bn / $387.4bn. The central is the ratio route, the route decision 2026-09-19 rejected: SSA's money's-worth
ratios applied to each year's taxes. The national check says those ratios, applied to the actual population
through the lane's frame, reproduce SSA's own aggregate. Against the Statement of Social Insurance at 1 January
2025 the OASDI 15–61 ratio comes out 4.6% high and the HI 15–64 ratio 1.7% high, with levels 3.8–8.0% low, all
within the declared tolerance. The check also cut the central by $5.9bn, because the Part A spouse credit counted
dependents twice (bec1cd7: $443.8bn / $503.7bn). One setting at a time gives $377–460bn at 48 and $439–519bn at 11;
every combination spans $348–519bn / $413–575bn. The lifetime model's own formula falls 20% short by construction and
decides nothing. Whether accrual can rest on SSA's ratios or needs an extended formula model goes to the operator
(recommended: SSA's ratios); until then the figure stays beside the case. [CALCULATION: `pension_accrual.py` →
`derived/summary.json`, `derived/case_beside.csv`; `national_check.py` → `derived/national_score.json`]

Lane `pension_accrual_2026_09_28` (worker W2, 2026-09-28): the September 27 case ($321.82–387.37bn at
specifications 48 / 11) with Social Security (OASDI) and Medicare Part A on an accrual basis, beside the case,
never in it. Model self-report: claude-opus-5-5. Brief: [BRIEF.md](BRIEF.md) (7609ed4).

## What changes

The case credits the group's OASDI and HI payroll taxes and charges the benefits paid in 2024. The switch keeps
every receipt and replaces two spending amounts:

- **Social Security.** The 2024 benefits ($56.26bn at 48, $53.02bn at 11) become the present value of the
  benefits the group's 2024 covered work earns.
- **Part A.** Medicare's Part A share of 2024 spending ($19.66bn) becomes the Part A value earned by the group's
  2024 covered worker-years.

What stays cash:

- **Parts B and D** ($32.76bn): general revenue and premiums finance them, so payroll work earns no entitlement
  to them.
- **Railroad retirement** ($0.56bn / $0.53bn).

Part A is the case's Medicare amount ($52.42bn) times the HI share of 2024 Medicare benefits, 416.3 / 1,109.8.
[CALCULATION: `derived/case_components.csv`; SOURCE: Medicare TR 2025 Table II.B1, `reads/quotes.json`
`mtr_benefits_2024_bn`]

**Central decomposition, $bn** (the two fill-in methods averaged) [CALCULATION: `derived/case_beside.csv`, arm
`central`]

| | Spec 48 | Spec 11 |
|---|---:|---:|
| The case | 321.82 | 387.37 |
| OASDI taxes credited (unchanged) | 112.94 | 106.13 |
| OASDI accrual (1.298 per tax dollar) | 146.58 | 137.74 |
| 2024 Social Security benefits removed | 56.26 | 53.02 |
| **Change, OASDI** | **+90.32** | **+84.72** |
| HI taxes credited (unchanged) | 31.28 | 29.15 |
| Part A accrual | 51.28 | 51.28 |
| 2024 Part A benefits removed | 19.66 | 19.66 |
| **Change, Part A** | **+31.62** | **+31.62** |
| **The case on accrual** | **443.76** | **503.71** |

The OASDI accrual is the group's accrual per dollar of on-books OASDI tax times the case's own OASDI receipts. The
Part A accrual counts covered workers, not tax dollars. The specifications change the tax allocation but not the
population, so the Part A accrual is the same at both ends.

## The central arm and why

| Setting | Central | Reason |
|---|---|---|
| Benefits | scheduled | The OASDI Trustees define cost with scheduled benefits. The Part A projections disregard the payment cuts that depletion would force. [SOURCE: `reads/quotes.json` `tr_cost_is_scheduled`, `mtr_projections_scheduled`] Payable is an arm. |
| Discount rate | the Trustees' rate on newly issued trust-fund securities (TR 2025 Table V.B2): 4.1% nominal / 1.7% real in 2026–34, 4.7% / 2.3% from 2045 | This is the government's projected marginal borrowing rate, the right rate for valuing a new obligation. Note 2025.7 instead uses the trust funds' effective portfolio yields (Table B: 0.1–0.8% real in 2025–30), which lag the market. For EAN the two paths differ by 1.3% (1.298 vs 1.281 per tax dollar). [SOURCE: `reads/quotes.json` `tr_new_issue_rates`, `note_mwr_effective_yields`; CALCULATION: `derived/oasdi_arms.csv`] |
| Attribution | entry-age normal (EAN): the lifetime money's-worth ratio times each year's tax | This is the brief's and the 09-18 lane's construction. At trust-fund rates it applies SSA's published ratios directly, and the choice of rate path barely moves it. Projected unit credit (PUC) is $10.8bn lower. PUC spreads the same lifetime benefit in wage-indexed units instead of discounted tax, which gives a young group less when the rate exceeds wage growth. |
| Earnings level | this year's covered earnings over the medium scaled worker's factor at the same age (Note 2025.3 Table 6) | The 09-18 lane's raw wage / AWI treats a 25-year-old's wage as a career average. That inflates young workers' ratios (+$14.9bn as an arm). |
| Career start | Mexico-born: US covered work from arrival (CPS year-of-entry midpoints) | SSA's scaled worker starts at 21. Late arrivals have fewer covered years and can fail the 10-year test. |
| Unauthorized | taxes on the books at 0.526, as in the case; 10% of their accrual credited | Note 151 projects that about 10% of "other immigrants" will be eligible for retired-worker benefits at the end of the 75-year projection, against 30% for those who were 62 in 2000. Suspense-file earnings have "only a relatively remote possibility" of being credited. [SOURCE: `reads/quotes.json` `note151_eligible_share`, `note151_suspense_file`; DATA: `onbooks_share_2026_09_23/derived/onbooks_split.csv`] |
| Mortality | NVSS 2024 period tables for the whole population, improved at the TR's 0.68% (65+) and 0.74% rates | This is the basis of the published ratios. The Hispanic advantage is contested (ethnicity misreporting on death certificates, return migration). Hispanic mortality is an arm (+$19.6bn). [SOURCE: `reads/quotes.json` `tr_mortality_decline_*`] |
| Part A, spouse | the non-working spouse of a one-earner couple qualifies on the worker's record | This matches OASDI's one-earner-couple ratios, which include the spouse's benefit. |

## Arms: one change from the central

$bn, methods averaged. OASDI arms leave Part A at the central, and the reverse; rate, payable, unauthorized and
mortality arms move both. [CALCULATION: `derived/case_beside.csv`]

| Arm | Per tax $ | ΔOASDI 48 / 11 | ΔPart A | Case 48 | Case 11 |
|---|---:|---:|---:|---:|---:|
| **central** | 1.298 | 90.3 / 84.7 | 31.6 | **443.8** | **503.7** |
| payable benefits (OASDI Note 2025.7 Table 3; HI 89% → 86% → 100%) | 1.018 | 58.7 / 55.0 | 26.8 | 407.3 | 469.2 |
| trust-fund effective rates (Note 2025.7's own) | 1.281 | 88.5 / 83.0 | 36.2 | 446.5 | 506.6 |
| real 2.3% flat (the Trustees' ultimate) | 1.093 | 67.2 / 63.0 | 26.9 | 415.9 | 477.2 |
| real 2% | 1.203 | 79.7 / 74.7 | 32.1 | 433.6 | 494.1 |
| real 3% | 0.872 | 42.3 / 39.6 | 17.0 | 381.1 | 443.9 |
| the case's rates, 2% at 48 and 3% at 11 | 1.203 / 0.872 | 79.7 / 39.6 | 32.1 / 17.0 | 433.6 | 443.9 |
| unauthorized credited nothing | 1.282 | 88.5 / 83.0 | 30.8 | 441.1 | 501.2 |
| unauthorized at 30% (Note 151, age 62 in 2000) | 1.330 | 93.9 / 88.1 | 33.2 | 449.0 | 508.7 |
| unauthorized credited in full | 1.441 | 106.6 / 100.0 | 38.9 | 467.3 | 526.3 |
| attribution PUC | 1.202 | 79.5 / 74.6 | 31.6 | 433.0 | 493.6 |
| attribution ABO (benefit formula on the record to date) | 1.405 | 102.4 / 96.1 | 31.6 | 455.9 | 515.1 |
| earnings level: raw wage / AWI (09-18) | 1.430 | 105.2 / 98.7 | 31.6 | 458.7 | 517.7 |
| earnings level: generation's career mean incl. zeros | 1.497 | 112.8 / 105.8 | 31.6 | 466.2 | 524.8 |
| every career from 21 | 1.272 | 87.4 / 82.0 | 31.6 | 440.9 | 501.0 |
| Hispanic mortality | 1.423 | 104.5 / 98.0 | 37.1 | 463.4 | 522.5 |
| Part A without the spouse | 1.298 | 90.3 / 84.7 | 25.7 | 437.8 | 497.8 |
| *bridge:* discounting at AWI growth (r = g) | 1.575 | 121.7 / 114.2 | 49.2 | 492.6 | 550.7 |
| *bridge:* 09-18 settings (raw level, trust-fund rates, careers from 21, unauthorized in full) | 1.516 | 115.0 / 107.9 | 44.2 | 481.0 | 539.4 |

The two bridges are neither candidates nor part of the range. The r = g arm serves the steady-state comparison.
The 09-18 arm shows the carry from that lane's 1.535 per tax dollar to this one.

The ends of the range:

- **Low:** real 3% at both ends.
- **High:** unauthorized workers credited in full.

**Every combination** of the non-bridge settings spans $348.4–527.0bn at 48 and $412.7–582.7bn at 11
(0.654–1.914 per tax dollar; Part A $28.6–64.9bn). MARG is left out because it does not add up. The corners
stack every extreme at once and are not plausible readings. [CALCULATION: `derived/summary.json`
`every_combination_bn`]

**By generation, central** (accrual per on-books tax dollar): G1 1.322, G2 1.276, G3+ 1.297. For the
Mexico-born, the arms mostly change how their unauthorized members are treated:

- 1.271 when the unauthorized are credited nothing;
- 1.783 when they are credited in full;
- 1.240 with careers from 21.

The US-born generations do not move with those arms. [CALCULATION: `derived/oasdi_by_generation.csv`]

**Marginal accrual.** The benefit that 2024's work adds, holding the rest of the career fixed, is only 0.224 per
tax dollar at the central settings. An extra year mostly displaces a lower year from the best 35. It does not
add up to lifetime benefits, so it is no accounting attribution. In the case's counterfactual the whole career
goes, not one year. [CALCULATION: `derived/oasdi_arms.csv`, method MARG]

## Part A

The accrual per covered worker-year is P(qualify) × PV at 2024 of Part A from 65 ÷ expected covered years:

- **Present value.** HI cost per beneficiary follows Table V.D1 through 2034 ($6,319 in 2024), then grows at the
  3.5% ultimate. It is discounted at the central rate, with NVSS 2024 survival by sex. [SOURCE: Medicare TR 2025
  Table V.D1, `reads/quotes.json` `mtr_hi_growth_ultimate`]

  | Age in 2024 | 25 | 45 | 64 |
  |---|---:|---:|---:|
  | Men | $79.0k | $96.9k | $122.2k |
  | Women | $93.1k | $113.6k | $138.2k |

  [CALCULATION: `derived/summary.json` `part_a.part_a_pv_at_2024`]
- **P(qualify).** The share of each generation's lawfully present 65+ with Medicare: G1 0.893, G2 0.937,
  G3+ 0.911. [DATA: CPS ASEC 2025 MCARE]
- **Expected covered years.** Summed covered shares by age from career start to 64: G1 32.9, G2 34.0, G3+ 34.7.
- **Counts.** The union has 20.53m HI-covered workers.
- **Spreading.** The value is spread evenly over covered years, like a service-based unit credit.
  - Front-loading it into the first 40 quarters would give a young group more.
  - Unauthorized worker-years count at the on-books share and at the legalization share of the arm.

  [CALCULATION: `derived/hi_arms.csv`]

The brief asked for a published Part A present value at 65. Neither Trustees report publishes one per person, so
this lane builds it from the Trustees' published per-beneficiary cost path. The cost carries no age gradient: a
cohort's survival-weighted mix over retirement resembles the cross-sectional mix of beneficiaries. [INFERENCE]

## Steady-state cross-check (item 3)

This route reweights the group's 2024 OASDI and Part A cash balance on the case's lines by age band, with no
money's-worth ratios. The change is benefits × (factor − 1) less taxes × (factor − 1). Part A scales with Medicare
coverage by band. [CALCULATION: `derived/steady_state.csv`, `derived/steady_state_case.csv`]

| Route | ΔOASDI 48 | ΔPart A 48 | Total 48 | Total 11 |
|---|---:|---:|---:|---:|
| Accrual, central | 90.3 | 31.6 | 121.9 | 116.3 |
| Accrual, Hispanic mortality | 104.5 | 37.1 | 141.6 | 135.1 |
| Accrual at r = g | 121.7 | 49.2 | 170.8 | 163.3 |
| Stationary population, NVSS 2024 Hispanic table | 93.1 | 35.7 | 128.8 | 123.3 |
| Stationary population, NVSS 2024 total table | 78.3 | 30.1 | 108.3 | 103.8 |
| White ages (FAQ entry 10's structure) | 85.7 | 33.4 | 119.1 | 114.2 |

At the stationary Hispanic ages the group's Social Security benefits scale by 2.539 and its OASDI taxes by 0.942.
Medicare coverage scales by 2.735. [CALCULATION: `derived/steady_state.csv`]

**How close.** The routes sit within 11% of each other when the mortality basis matches:

- whole-population tables: 108.3 against 121.9;
- Hispanic tables: 128.8 against 141.6.

The white-age route comes within 2–3% of the central accrual (119.1 against 121.9 at 48, 114.2 against 116.3 at
11).

**Why they differ, and why the closeness is partly coincidence.** [INFERENCE from the rows cited]

- **Where the routes should meet.** In a steady state, cash benefits equal the accrual plus (r − g) times the
  accrued liability. At r = g the two routes should therefore agree.
- **The gap at r = g.** The accrual at r = g is $170.8bn, $42–62bn above the stationary routes. The cash route
  inherits today's elderly, who collect far less than SSA's scaled workers promise today's workers:
  - 69.7% of the group's 65+ receive Social Security, against 83.5% of whites (G1 62.2%);
  - $17.3k per recipient, against $22.2k.

  [DATA: `derived/elderly_receipt.csv`, CPS ASEC 2025 through the 09-18 stage]

  Likely sources, not separated here:
  - earlier cohorts with shorter US careers and lower coverage;
  - people who worked off the books before legalizing;
  - benefits paid abroad to emigrants, which the CPS cannot see;
  - CPS underreporting.
- **At the Trustees' rates.** Discounting at r > g lowers the accrual by $49bn and leaves out the (r − g) term.
  That brings the two routes within 11%.
- **Which to prefer.** The accrual prices today's workers' own covered earnings. The steady-state route prices
  today's elderly. FAQ entry 10 names exactly this as what would change its composition result: "US-born cohorts
  reaching 65 with higher covered earnings" than those born before about 1960. The accrual is the measurement
  that caveat asks for. Its risk runs the other way: if future elderly look like today's, the accrual overstates.
  - The payable arm ($58.7bn OASDI) bounds part of that risk.
  - The unauthorized-credited-nothing arm ($88.5bn) bounds another part.

FAQ entry 10's figures (Social Security and other cash +$70bn, public medical +$80bn at white ages) come from the
September 19 ledger, a different object. They agree in direction and are not comparable to the dollar.

## The model, and decision 2026-09-19

Decision 2026-09-19 (program ownership) rejected "adding whole-career SSA money's-worth ratios as annual
entitlement accrual". Its trigger for revisiting is "an independently validated pension accrual model". The lane's
ratio route, the construction that decision rejected, passes the independent national check. The lifetime model's
own formula falls short of it by construction, as it falls short of the model-worker check below (see "National
check: score").

`lifetime_model.py` builds SSA's scaled workers from the benefit formula and the Trustees' 2025 assumptions:

- earnings: Note 2025.3 Table 6 and the AWI path in Table 7;
- the contribution base and COLAs: TR Table V.C1;
- tax rates: TR Table V.C6;
- the claiming reduction at 65: TR Table V.C3;
- NVSS 2024 survival, improved at the TR rates.

It is checked against SSA's own outputs [CALCULATION: `derived/model_check_v_c7.csv`, `derived/model_check_mwr.csv`]:

- **Benefit formula.** Replacement rates at 65 match TR 2025 Table V.C7 within 0.164 points in all 64 cells.
- **Payable haircut.** The payable-to-scheduled ratio matches Note 2025.7 Table 3 within 0.056.
- **Level.** The model reaches 0.667–0.825 of Note 2025.7 Table 1. It omits disability, child and young-survivor
  benefits, the family maximum and mortality by earnings. The lane therefore uses the model only for ratios to its
  own result on Note 2025.7's basis (trust-fund rates, careers from 21, EAN). On that basis the ratio is exactly 1,
  so the published table carries the level.
- **Adding up.** EAN, PUC and ABO each sum to the lifetime present value of benefits (worst error 2.2e-16).

## Conventions and limits

- **Interest on the group's existing pension liability is not charged.** The switch replaces cash with the normal
  cost. A full pension expense would add interest on the liability already accrued. In a steady state cash equals
  normal cost plus (r − g) times that liability, which is why the cash route runs above the accrual at r > g. The
  omission parallels the case's own convention of holding existing federal interest at zero response. It is
  flagged, not priced: pricing it needs the group's accrued liability, which includes past service of people
  with no 2024 tax. That would be a lane of its own.
- **Coverage.** The case's national OASDI receipts are $1,296.5bn, 1.0024 × the Trustees' $1,293.3bn of 2024
  net payroll tax contributions. The case is therefore already on the covered base, and the 09-18 lane's CPS
  coverage scale (0.9595) has no role in a ratio applied to the case's own OASDI taxes. [CALCULATION:
  `derived/summary.json` `coverage_check`; SOURCE: TR 2025 Table II.B1, `reads/quotes.json`]
- **Emigration** before retirement is ignored. It lowers the accrual if emigrants forfeit benefits and leaves it
  unchanged if they collect abroad.
- **Payroll base.** The accrual scales with the case's OASDI tax. A change to the on-books share (the peer lane
  `payroll_compliance_2026_09_28` works on this) moves the accrual in proportion.
- **The ratio applies across allocations.** The per-tax-dollar ratio is measured on the group's CPS on-books
  taxes ($113.7bn). It is applied to the case's allocation at each end ($112.9bn shared, $106.1bn personal).
- **Separate objects.** The 09-18 lane's −$136.9bn switch lives on the September 19 CPS ledger. It is reproduced
  here only as a gate. The figures above are computed on the adopted case's own lines and must not be added to
  that ledger's gaps.

## Gates and reproduction

1. **The 09-18 union row reproduced** with that lane's own `accruals()` and `parse_mwr()`: accrual −$188.1365bn,
   cash-to-accrual −$136.8799bn, 1.5347 per tax dollar. [DATA: `derived/gate_union_row.json`]
2. **The case reproduced through the unchanged package.**
   - `case_lines.cjs` runs `evaluateFull` at 48 and 11 for both methods.
   - The results equal `summary.json` to 0.0 ($321.8194 / $387.3701bn).
   - 48 and 11 are each method's ends.
   - The package chain, engine and model.json are identical to HEAD before and after.
   - `pension_accrual.py` re-checks every frozen hash and the per-method costs.

   [DATA: `derived/case.json`]
3. **Parser and quotes.** This lane's Note 2025.7 parser equals the 09-18 lane's `parse_mwr()`. Every fragment of
   the 29 quotes is found in its document (`reads/quotes.json`, PDF hashes in `derived/sources.json`).
4. **Model.** The factor is 1 on Note 2025.7's basis, and the attributions add up.
5. **Reruns.** Two consecutive runs of `scripts/rerun_lane.py` are byte-identical (22/22 files, rc 0).
   `lifetime_model.py` and `sources.py` are imported modules, passed with `--allow-unrun`.

```sh
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/pension_accrual_2026_09_28 \
  "node {lane}/case_lines.cjs" \
  "OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/pension_accrual.py" \
  --allow-unrun infra/immigration-fiscal/pension_accrual_2026_09_28/lifetime_model.py \
  --allow-unrun infra/immigration-fiscal/pension_accrual_2026_09_28/sources.py
```

Primary documents are cached in `_cache/` (ignored) and pinned by sha256 in `sources.py`:

- SSA Actuarial Notes 2025.7 and 151 (the 09-18 lane's copies);
- SSA Actuarial Note 2025.3 (Wayback 20260623);
- the 2025 OASDI Trustees Report (Wayback 20260919);
- the 2025 Medicare Trustees Report (cms.gov).

`sources.py` stops with `[BLOCKED]` if any document is missing or has changed.

## Files

- `case_lines.cjs` reads the case's pension lines through the unchanged package. It writes `derived/case_lines.csv`
  and `derived/case.json`.
- `sources.py` parses the primary tables and checks the quotes.
- `lifetime_model.py` is the scaled-worker model.
- `pension_accrual.py` runs the gates, the arms, Part A, the steady state and the case beside.
- `derived/`:
  - `case_beside.csv`: every arm at each end;
  - `summary.json`: the central, the ranges, the checks;
  - `oasdi_arms.csv`: the full OASDI factorial for the union;
  - `oasdi_by_generation.csv`;
  - `hi_arms.csv`;
  - `case_components.csv`;
  - `steady_state.csv` and `steady_state_case.csv`;
  - `elderly_receipt.csv`;
  - `model_check_v_c7.csv` and `model_check_mwr.csv`;
  - `gate_union_row.json`;
  - `sources.json`.

## National check: prediction

Frozen 2026-09-28 10:03 JST, before any Statement of Social Insurance (SOSI) figure was opened.
`derived/national_prediction.csv` has sha256 `b8b5c3f5ae9315a0a9a48ada1732d917c971df45edf51d68111bbfed469ed7d9`,
and `national_check.py` reproduces it. [CALCULATION: `national_check.py` → `derived/national_prediction.csv`,
`derived/national_prediction.json`, `derived/national_cells.csv`]

**Target.** The SOSI at 1 January 2025 closed-group rows: OASDI participants aged 15–61 and 62+, and HI participants
aged 15–64 and 65+. For each row it gives the present value (PV) of future expenditures and of future non-interest
income over 2025–2099, at the Trustees' rates with scheduled benefits.

**Not fully blind.** Before this check I had seen TR 2025 Table VI.F2's totals for all current participants
(OASDI cost $102.8tn, taxes $47.8tn, over an unlimited horizon). So the sum of the two OASDI rows is not blind. The
split by age and every HI figure are blind.

Two changes were made after the draft totals were visible and before the freeze. Both are disclosed because the
first moved the result toward that known total:

- **Per-age ratios.** The first draft priced each person's whole career at the ratio of their current five-year
  band ($73.5tn at a ratio of 1.714). It was replaced by the lane's per-year accrual summed over the career: each
  year's taxes earn the ratio that today's taxpayers of that age carry, re-evaluated at the person's birth
  cohort. The draft had priced a 22-year-old's career at the mix of 20–24-year-olds, who are mostly single; the
  lane's machinery never does that. The change raised the row by 2.3%.
- **Tax calibration.** Taxes now scale to 12.4% of the Trustees' 2024 taxable payroll ($10,124bn), not to 2024's
  payroll tax income ($1,293.3bn). That income is 12.77% of payroll in Table IV.B2 because it carries
  adjustments for prior years. Future years run at IV.B2's payroll-tax rate (12.23% in 2025, 12.38% from 2028).
  The change lowered both levels by 2.9%. [SOURCE: TR 2025 Tables VI.G6 and IV.B2, `reads/quotes.json`
  `tr_taxable_payroll_2024_bn`]

**Method.** The lane's machinery on the SOSI's basis: the trust funds' effective rates (the TR's own PV basis;
Table VI.G6's factor for 2024 is 0.9876, and this model's half-year roll gives 1/1.0124), 2025–2099, scheduled
benefits, the whole population aged 15+ in the CPS frame.

- **OASDI 15–61, the ratio route.**
  - *Taxes.* Lifetime taxes come from a pseudo-cohort: 2024 covered earnings by single year of age, sex and
    nativity (zeros included), moved along cohort lines with the AWI.
    - Past years are taxed at the year's OASDI rate and accumulated at the trust funds' rates.
    - Future years are weighted by NVSS 2024 survival from 2025 (improved at the TR's rates) and discounted.
    - The foreign-born count only from arrival.
  - *Ratio.* Each year's taxes earn the lane's per-tax-dollar ratio of today's taxpayers of that age: Note 2025.7
    Table 1 through the age-adjusted level and the observed family, with careers from arrival for every
    foreign-born worker. Unauthorized workers are on the books at the case's shares (0.526 Mexico-born, 0.550
    others) and credited at 10%.
  - *Window.* The lifetime model scales lifetime benefits to those paid in 2025–2099 to a person alive in 2025
    (factor 1.006, person-weighted).
  - *Formula route.* The same with the lifetime model's own ratio.
- **OASDI 62+.** CPS 2024 Social Security benefits are valued as annuities with COLAs, survival and the same rates,
  plus:
  - the survivor's step-up between linked spouses who both collect;
  - claims by those aged 62–69 not yet collecting, at the receipt share and benefit of 67–74-year-olds of the same
    sex and nativity, claimed at 67 (at 70 if already 67 or older).
- **Income.** Future payroll tax (the same pseudo-cohort) plus the taxation of benefits at Tables IV.B1/IV.B2's
  ratio of that income to cost, year by year. The ratio is 3.8% in 2025, 5.8% in 2050 and 6.1% in 2080. HI takes
  0.722 of the OASDI amount (the two 2024 amounts: $39.8bn over $55.1bn). OASDI cost is benefits × 1.0091 (2024
  cost over benefits, Table VI.A3).
- **HI 15–64: the lane's Part A machinery.** P(qualify) (Medicare coverage of lawfully present people 65+, by
  nativity and sex; unauthorized × 10%) × the PV of Part A from 65. That PV uses the average cost per beneficiary
  with no age gradient.
- **HI 65+.** Current enrollees' Part A cost from 2025. HI cost is benefits × 1.0149 (MTR Table II.B1).
- **Primary scaling.** Each 2024 flow is scaled to its Trustees total:
  - OASDI taxes × 0.949;
  - OASDI benefits × 1.200 (the CPS captures 83.3% of the Trustees' $1,471.4bn);
  - HI taxes × 1.113 (to $396.4bn, which includes the 0.9% additional tax);
  - Medicare enrollees 65+ × 1.036.

  The reason: the case's own lines are on the Trustees' base. The unscaled CPS frame is shown beside.

**Prediction, $tn at 1 January 2025** [CALCULATION: `derived/national_prediction.csv`]

| Row | Expenditures | Income | Net | Ratio (exp. / inc.) |
|---|---:|---:|---:|---:|
| OASDI 15–61, ratio route | **72.85** | **41.62** | −31.24 | **1.751** |
| OASDI 62+ | **21.04** | **2.00** | −19.04 | **10.54** |
| HI 15–64 | **22.49** | **15.27** | −7.22 | **1.473** |
| HI 65+ | **5.62** | **0.91** | −4.70 | **6.16** |
| *beside:* OASDI 15–61, formula route | 60.61 | 40.91 | −19.70 | 1.482 |
| *beside, CPS frame unscaled:* OASDI 15–61 / 62+ | 76.74 / 17.54 | 43.84 / 1.87 | | 1.751 / 9.40 |
| *beside, CPS frame unscaled:* HI 15–64 / 65+ | 21.70 / 5.42 | 14.19 / 0.77 | | 1.530 / 7.02 |

The OASDI rows sum to $93.9tn of expenditures and $43.6tn of income, a ratio of 2.15. For all current participants
over an unlimited horizon, TR Table VI.F2 gives $102.8tn and $47.8tn. The prediction therefore runs about 9% low on
both levels; the ratio is not blind. National per-tax-dollar flows at trust-fund rates, for all 2024 taxpayers
aged 15+: 1.237 on the ratio route and 1.027 on the formula route, against the group's 1.281.
[CALCULATION: `derived/national_prediction.json`]

**Tolerance (the parent's, adopted unchanged).** Each row's ratio must fall within ±10% of the published value, and
each level within ±15%.

- **OASDI.** The accrual route passes if the 15–61 row passes all three tests. That row carries the route's ratio
  and its past taxes.
- **HI.** The Part A machinery passes if the 15–64 row passes all three.
- **62+ and 65+ rows.** They are scored with the same tolerance and reported beside. They value current benefits
  and enrollees, which the case's accrual does not use.
- **What a miss implies for the central.** If the 15–61 income passes but the ratio misses, the lane's
  per-tax-dollar ratio (1.298) scales by the published ratio over 1.751. A Part A miss on the 15–64 expenditures
  scales the Part A accrual ($51.28bn) the same way.

**Named differences, fixed now with the expected direction of the published figure against this prediction:**

- **OASDI 15–61.**
  - Children under 15 who receive benefits on a current participant's record belong to the SOSI's future
    participants, but the route credits them to the worker. Published lower, by about 1–2%.
  - Disability benefits paid before 2025 sit inside lifetime ratios. Published lower, by about 1%.
  - Emigration of current participants. Published lower on both levels.
  - Rising participation at older ages. Published higher on income.
  - A pseudo-cohort freezes the 2024 age profile. Direction unknown.
- **OASDI 62+.**
  - Benefits that began partway through 2024 are understated in the CPS. Published higher.
  - CPS non-reporters are counted as future claimants and also scaled up. Published lower.
- **HI 15–64.**
  - Costs of disabled enrollees before 65 are left out: +$0.67tn for today's enrollees. The cost of those
    disabled in future before 65 is not computed. Published higher.
  - The 0.9% additional tax grows faster than the AWI. Published higher on income.
- **HI 65+.**
  - No age gradient in cost per beneficiary. Published higher, possibly by 10–25%.
  - Premiums of voluntary enrollees are left out. Published slightly higher on income.

## National check: score

The published rows were opened after the freeze and scored at 10:35 JST. They come from SSA's FY 2025 Agency
Financial Report (OASDI) and CMS's FY 2025 Financial Report (HI), both pinned by sha256 in `sources.py`.
`sosi_oasdi()` and `sosi_hi()` parse the 2025 columns and stop unless the rows add to the published totals.
`national_check.py` stops unless `derived/national_prediction.csv` is still the frozen file. [SOURCE: `sources.py`
DOCS `ssa_afr2025`, `cms_fr2025`; `reads/quotes.json` `afr_sosi_basis`, `cms_sosi_closed_group`; CALCULATION:
`national_check.py` → `derived/national_score.csv`, `derived/national_score.json`]

**Both checks pass.** Predicted against published, $tn at 1 January 2025:

| Row | Expenditures | Income | Ratio | Declared test |
|---|---:|---:|---:|---|
| **OASDI 15–61** (gates the OASDI accrual) | 72.85 / 75.71 (−3.8%) | 41.62 / 45.25 (−8.0%) | 1.751 / 1.673 (+4.6%) | **pass** |
| **HI 15–64** (gates Part A) | 22.49 / 23.96 (−6.2%) | 15.27 / 16.55 (−7.8%) | 1.473 / 1.448 (+1.7%) | **pass** |
| OASDI 62+ (beside) | 21.04 / 26.08 (−19.3%) | 2.00 / 2.52 (−20.8%) | 10.54 / 10.35 (+1.9%) | levels miss |
| HI 65+ (beside) | 5.62 / 8.05 (−30.2%) | 0.91 / 1.04 (−12.5%) | 6.16 / 7.72 (−20.2%) | expenditures and ratio miss |
| OASDI 15–61, formula route (beside) | 60.61 / 75.71 (−19.9%) | 40.91 / 45.25 (−9.6%) | 1.482 / 1.673 (−11.4%) | **fails** |

[SOURCE: SSA FY 2025 AFR, Statements of Social Insurance; CMS FY 2025 Financial Report, Statement of Social
Insurance; CALCULATION: `derived/national_score.csv`]

The two OASDI rows combined are **not blind** (TR Table VI.F2's $102.8tn / $47.8tn were seen before the freeze):
cost 93.90 against 101.78 (−7.7%), income 43.61 against 47.77 (−8.7%). The split by age and the HI rows are blind.

**The score leaves the central alone** under the declared rule, which scales only on a miss. Step d changes Part A
for a different reason (below). For reference [CALCULATION: `derived/national_score.json` `central_mapping`]:

- Scaling the OASDI accrual to the published 15–61 ratio would give 1.240 per tax dollar instead of 1.298
  (−$6.5bn at 48, −$6.1bn at 11).
- Scaling Part A to the published 15–64 expenditures would give $48.3bn instead of $45.4bn (+$3.0bn).

### The formula route: where its gap sits

The lifetime model leaves out disability, children's and young survivors' benefits, the family maximum and
mortality graded by earnings, so it misses the level by construction and decides nothing. It enters only the 15–61
row; on the 62+ row both routes value CPS benefits the same way. [CALCULATION: `derived/national_score.json`
`formula_gap`]

- **Age row.** The formula route is $15.1tn short on the 15–61 row. Of that, $12.2tn (81%) is its distance from
  the ratio route, the benefits the model leaves out; $2.9tn is common to both routes.
- **Age band.** The left-out benefits are about 18% of the ratio route's cost for participants aged 15–34 and 15%
  for those aged 45–61. Formula over ratio route: 0.820 (15–24), 0.819 (25–34), 0.830 (35–44), 0.845 (45–54),
  0.847 (55–61). The young have more years exposed to disability and to death with young children. [INFERENCE]
- **Benefit type.** The model-worker check, as model over Note 2025.7 Table 1 averaged over levels and cohorts:
  single men 0.785, single women 0.768, one-earner couples 0.750, two-earner couples 0.743. Note 2025.7 gives
  single workers no children, so their 21–23% is disability benefits with the mortality and disability incidence
  graded by earnings. Couples lose 2–4 points more: children's and young survivors' benefits, net of the family
  maximum. [SOURCE: `reads/quotes.json` `note_mwr_benefit_scope`; CALCULATION: `derived/model_check_mwr.csv`]

### Where the gaps come from

The parent's named differences for OASDI 15–61 (ratio 4.6% high, income 8.0% low):

- **DI and young-survivor benefits.** The ratio route has them; the formula route leaves them out, which fits its
  −20%. Disability benefits paid before 2025 sit inside lifetime ratios but outside the SOSI's future cost (frozen:
  published lower on the ratio, about 1%). Consistent in direction.
- **Auxiliaries.** Note 2025.1 sets a participant's age by the worker on whose account benefits are paid. The
  SOSI then books spouses', children's and survivors' benefits in the worker's row, as the ratio route does. The
  AFR does not state its convention; reading it as Note 2025.1's is an inference from the shared closed-group
  concept. On that reading my frozen item on children under 15 ("published lower by 1–2%") was wrong and is
  withdrawn. [SOURCE: `reads/quotes.json` `note2025_1_age_by_account`; INFERENCE]
  - The one piece that can overstate is the one-earner couple: a spouse with no 2024 wages may still collect on
    their own record. Pricing every one-earner couple as a two-earner couple removes the spousal benefit and gives
    1.624, 2.9% below the published ratio. The lane's 1.751 is 4.6% above it. [CALCULATION:
    `derived/national_probes.csv`]
  - The published ratio sits 39% of the way from that bound to the lane. The auxiliary assignment alone could
    account for the whole ratio gap; the check cannot separate it from the items below. Read the same way, the
    group's 1.298 (bound 1.186) would calibrate to about 1.23, close to the scaled 1.240. [INFERENCE]
- **The truncation.** The SOSI stops in 2099. The Trustees' unlimited-horizon cost for current participants is
  $102.8tn against the SOSI's $101.8tn, so about 1% of their cost falls later. The prediction cuts at 2099 too,
  through the window factor. [SOURCE: `reads/quotes.json` `tr_vi_f2_current_participants`; SOSI]
- **Income from taxing benefits.** Both sides include it. The prediction takes Tables IV.B1/IV.B2's ratio to cost
  year by year.
- **Non-covered state and local workers, and CPS earnings against SSA taxable payroll.** The CPS stage taxes every
  wage, including non-covered state and local pay. The CPS taxes run 5.3% above 12.4% of the Trustees' taxable
  payroll, and the prediction scales them down uniformly (0.949). [CALCULATION: `derived/national_prediction.json`
  `calibration.oasdi_tax`] If the excess sits at older ages, the scaling understates the young's future taxes and
  overstates older workers' past taxes. Both would push the predicted ratio up and income down, the observed
  pattern. Not quantified. [INFERENCE]
- **Level assignment.** Tested at the parent's request; it runs the other way (below).
- Of the other frozen items, rising participation at older ages (published higher on income) fits. Emigration
  (published lower on both levels) is outweighed by something larger.

The rows beside:

- **OASDI 62+, levels 19–21% low, ratio +1.9%.**
  - On the same reading, the SOSI's row holds every future benefit on the accounts of workers now 62+, including
    survivor benefits their younger spouses will draw. The prediction values only the step-up between linked
    spouses who both collect.
  - The Social Security Fairness Act (enacted 5 January 2025) raised benefits for people with non-covered pensions.
    It is in the valuation (the SOSI books −$1,048bn for changes in law, open group), and CPS 2024 benefits predate
    it. [SOURCE: `reads/quotes.json` `afr_ssfa_in_valuation`]
  - Frozen items: part-year 2024 awards (published higher) fits; non-reporters counted as claimants (published
    lower) is outweighed. The case's accrual does not use this row.
- **HI 65+, expenditures 30% low.** Every enrollee is priced at the average cost per beneficiary, but today's
  enrollees spend their remaining years at older, costlier ages. The frozen guess (10–25%) had the direction and too
  small a size. The case's accrual does not use this row.
- **HI 15–64.** Disabled enrollees' costs before 65 (frozen: published higher) add $0.67tn for today's enrollees
  and bring expenditures to 3.4% low. Future disability before 65 is not computed. Income is 7.8% low; the 0.9%
  additional tax grows faster than the AWI (frozen: published higher). [CALCULATION:
  `derived/national_prediction.json` `hi.disabled_under_65_scaled_tn`]

### Level assignment and convexity

The parent's premise holds for a person-weighted average of ratios. The accrual weights by tax dollars, and per tax
dollar the credit is lifetime benefits per unit of level. That is concave, like the benefit formula's 90/32/15%
brackets. Spread in the levels therefore lowers the tax-weighted ratio, and shrinking it raises the ratio.
[INFERENCE, checked by the probes]

| Probe | 15–61 ratio (published 1.673) | Group, per tax $ |
|---|---:|---:|
| The lane | 1.751 (+4.6%) | 1.298 |
| Levels shrunk, θ = 0.8 | 1.814 (+8.4%) | 1.345 (+3.6%) |
| Levels shrunk, θ = 0.6 | 1.885 (+12.7%) | 1.396 (+7.6%) |
| One-earner couples as two-earner | 1.624 (−2.9%) | 1.186 (−8.6%) |

θ is the share of each cell's variance in log level that is kept (cells: age × sex × nativity nationally, age ×
sex × generation for the group). [CALCULATION: `derived/national_probes.csv`]

No permanent-share estimate is needed to settle the sign. For the size of the spread, SSA publishes the target
itself: Note 2025.3 Table 1 gives the career-average earnings (AIME) of workers retiring in 2019–2024 against the
scaled workers' levels. The lane's levels for 2024 taxpayers aged 55–61 are not wider than that distribution. They
are thinner at the bottom.

| Share below | Very low | Low | Medium | High |
|---|---:|---:|---:|---:|
| Note 2025.3 Table 1, workers retiring 2019–2024 | 11.8% | 24.4% | 57.4% | 81.9% |
| The lane, taxpayers aged 55–61 | 8.5% | 20.9% | 57.7% | 80.2% |
| The lane, share of 15–61 OASDI tax | 1.1% | 5.1% | 31.0% | 58.8% |

[SOURCE: Note 2025.3 Table 1 via `sources.aime_distribution()`; CALCULATION: `derived/national_levels.csv`]

The level assignment does not explain the high ratio; correcting for transitory spread would widen the gap. The
convexity sits where the tax dollars are not: 1.1% of 15–61 OASDI tax falls below the very-low level.

### Part A: the spouse credit counted dependents twice

Step d asked for a check that the spouse credit does not double count. It does, and the central now leaves it out.
[CALCULATION: `derived/national_score.json` `part_a_spouse_check`]

- **In 2024.** Of the 2.29m covered workers the lane treats as one-earner couples (spouse with no wages), 0.31m
  (13.3%) have a spouse with covered self-employment earnings. That spouse accrues on their own record and was
  credited again on the worker's ($0.73bn).
- **Over a career, the whole credit.** P(qualify) is the share of the generation's 65+ with Medicare on any record,
  and expected covered years count every member's years, non-workers' zeros included. Summed over a generation's
  expected careers, the workers' own terms already give every member P(qualify) × the Part A value, dependents
  included. The spouse credit adds the dependents a second time: $5.93bn, 13.1% on top of the own term.
- **Revision.** The central Part A accrual falls from $51.28bn to $45.35bn, and the case on accrual from
  $443.76bn / $503.71bn to $437.83bn / $497.78bn. `derived/summary.json` keeps its keys. bec1cd7's central stays
  as the bridge `bridge_part_a_spouse_credit`, outside the ranges. [CALCULATION: `derived/summary.json`,
  `derived/case_beside.csv`]
  - Superseded above: the Part A rows of "What changes"; the "Part A, spouse" row of the central-arm table; the
    arms table's ΔPart A and case columns (every arm's Part A now leaves out the credit), including its "Part A
    without the spouse" arm, which is now the central; and the three accrual rows of the steady-state table, with
    the comparisons drawn from them. `derived/case_beside.csv` holds the new values.
  - Superseded ranges: one change at a time now gives $376.6–460.3bn at 48 and $439.4–519.2bn at 11. Every
    combination gives $348.4–519.2bn / $412.7–574.9bn, with Part A $28.6–57.1bn. [CALCULATION:
    `derived/summary.json` `range_across_arms_bn`, `every_combination_bn`]
- **Residual.** The own term values each worker-year at the worker's own sex, and women live longer and have fewer
  covered years. At the generation's sex mix the accrual would be $45.57bn (+$0.21bn, 0.5%). Left as is.

The national HI check tests the construction without the credit: its 15–64 row counts each person once.

### Accrued benefits at 1 January 2025 (step e, the stock only)

OCACT's maximum transition cost at 1 January 2025 is $54.1tn. It is the present value of accrued benefit
obligations less the reserves ($2.7tn) and the tax on those benefits. For a worker under 62 the accrued benefit is
a PIA computed as if disabled on the valuation date, wage-indexed to 62, times (age − 22) / 40. A worker who will be
disabled before normal retirement age accrues by service up to the date of disability. [SOURCE: `reads/quotes.json`
`note2025_1_transition_costs_2025`, `note2025_1_abo_disability_proration`]

- Take the 62+ row's published cost as its accrued obligations: $25.8tn after the cost loading. The MTC then
  implies $34.3tn accrued by today's 15–61-year-olds, 46% of that row's published benefits.
- The ratio route's entry-age attribution (past taxes × their ratio) gives $26.3tn, 36% of its own row, and 0.77 of
  the implied figure.
- The row totals nearly agree (−3.8%), so the difference is attribution. OCACT's measure puts more of the lifetime
  on service to date than entry-age normal does, most visibly for disability [INFERENCE from the definitions]. It
  is not a pass-or-fail test; the roll-forward stays skipped. [CALCULATION: `derived/national_score.json`
  `stock_check`]

### Adoption

Under the operator's 07:39 condition, the formula model had to pass both checks. It falls short of both, by
construction. The lead has since returned the question to the operator: can accrual rest on SSA's ratios now that
the ratio route passes nationally, or does it need an extended formula model? The model is not extended here.

**Recommendation: rest accrual on SSA's ratios, and put the ratio route into the next case revision with cash
beside.**

- The ratio route passed the one independent test that could have failed it, with the prediction frozen before the
  published rows were opened.
- An extended formula model would rebuild what Note 2025.7 already publishes: disability, children's and young
  survivors' benefits, the family maximum, and mortality and disability incidence graded by earnings. It would then
  need its own validation against the same tables.
- The lifetime model stays where the lane uses it now: for ratios to its own result (careers from arrival, the
  discount rate, the attribution).

The check leaves three things open:

- the group-specific settings (careers from arrival, the 10% unauthorized credit);
- the auxiliary assignment, which the check brackets but does not pin (1.24 against 1.30 per tax dollar);
- the attribution, where entry-age normal puts less on service to date than OCACT's accrued-benefit measure.

### Reproduction

```sh
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/pension_accrual_2026_09_28 \
  "node {lane}/case_lines.cjs" \
  "OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/pension_accrual.py" \
  "OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/national_check.py" \
  --allow-unrun infra/immigration-fiscal/pension_accrual_2026_09_28/lifetime_model.py \
  --allow-unrun infra/immigration-fiscal/pension_accrual_2026_09_28/sources.py
```

This supersedes the command under "Gates and reproduction". The quote count there is now 42 (all verified). New
files:

- `derived/national_score.csv`: every row and measure against the published figure, with the test;
- `derived/national_score.json`: the verdicts, the mapping to the central, the spouse check, the formula route's gap
  and the stock comparison;
- `derived/national_probes.csv`: the level and family probes;
- `derived/national_levels.csv`: the level distribution against Note 2025.3 Table 1.

## Progress (append-only)

- 2026-09-28. RESULT stubbed before any work.
- 2026-09-28. Objection sent to the parent: decision 2026-09-19 (program ownership) rejected "adding whole-career
  SSA money's-worth ratios as annual entitlement accrual" and 6a4b8b0 disabled `ss_timing.py` `main()`. Proposed:
  keep the money's-worth route as the brief's reproduction and one attribution (entry-age level, the pension
  accountant's normal cost), add a benefit-formula check validated against SSA's own tables, and report both.
  Working on the shared parts meanwhile.
- 2026-09-28. Primary sources fetched into `_cache/` (ignored; hashes and quotes go to `reads/`): SSA Actuarial
  Note 2025.3 (scaled factors; Wayback 20260623 snapshot, direct ssa.gov returns 403), the 2025 OASDI Trustees
  Report PDF (Wayback 20260919), the 2025 Medicare Trustees Report PDF (cms.gov). Note 2025.7 and Note 151 are
  the 09-18 lane's cached copies. Note 2025.7 has the payable scenario directly (its Tables 3 and 6).
- 2026-09-28. Gate 1 reproduced; the case read through the unchanged package (48 / 11 exact); the lifetime model
  validated against TR V.C7 and Note 2025.7 Tables 1 and 3.
- 2026-09-28. Central discount rate moved from Note 2025.7's effective portfolio yields to TR Table V.B2's
  new-issue path: a 2024 accrual is a new obligation, valued at the marginal rate. For EAN it changes little
  (1.281 → 1.298); for PUC it matters (1.295 → 1.202). Part A mortality moved to the whole-population tables, and
  Hispanic mortality became an arm. Unauthorized worker-years now count at the on-books share for Part A.
- 2026-09-28. Case beside, steady state, elderly receipt and coverage check written; two byte-identical reruns.
  Verdict filled.
- 2026-09-28. The stage cache is now keyed by the sha256 of the code that builds it (`ss_timing.py`, its
  extension builder, `cps_ca_status.py`). An edit to the case's status imputation rebuilds it instead of leaving
  stale flags. The rebuilt cache equals the old one, and the old one was removed. Two final reruns: 22/22
  identical, rc 0.
- 2026-09-28 10:03 JST. National check prediction frozen (section above) before any SOSI figure was opened:
  `derived/national_prediction.csv` sha256 `b8b5c3f5…d7d9`. Two changes preceded the freeze and are disclosed there
  (per-age ratios, +2.3%; tax calibration to taxable payroll, −2.9%). The OASDI sum is not blind (TR VI.F2 seen).
- 2026-09-28 10:35 JST. National check scored (section above): SOSI pinned from SSA's FY 2025 AFR (Wayback 20260316)
  and CMS's FY 2025 Financial Report; both gating rows pass, the formula route fails. The level probe runs the
  other way (shrinking raises the tax-weighted ratio). Step d found the Part A spouse credit double counting; the
  central drops it (Part A $51.28bn → $45.35bn; case $437.83bn / $497.78bn), with bec1cd7's central kept as a
  bridge. Step e (ABO against OCACT's maximum transition cost) skipped: the 62+ row, a large part of the accrued
  obligation, misses by 19%, so the comparison would test the annuity valuation rather than the attribution.
- 2026-09-28 10:50 JST. Two consecutive reruns with `national_check.py` in the command (see "Reproduction" above):
  30/30 files identical, rc 0. The prediction file kept its frozen sha256 through both.
- 2026-09-28 11:05 JST. Following the parent's settlement message (both routes frozen; the ratio route decides; the
  formula model decides nothing): the Verdict now labels the ratio route as the route decision 2026-09-19 rejected
  and says what the check shows; the formula route's gap is placed by age row, age band and benefit type; the
  combined OASDI rows are marked not blind; the adoption question is put as SSA's ratios against an extended formula
  model. The 1 January 2025 stock comparison against OCACT's maximum transition cost was cheap and is now run
  (lane 0.77 of the implied accrued obligations for 15–61); the roll-forward stays skipped. No model extension.
- 2026-09-28 11:15 JST. Two consecutive reruns after those edits: 30/30 files identical, rc 0; the prediction file
  kept its frozen sha256. 42 quotes verified.
