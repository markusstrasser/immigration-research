claude-opus-5-5

**Verdict:** Under current law, the September 27 case with Social Security (OASDI) and Medicare Part A on an accrual
basis is **$399.1bn / $461.0bn** at specifications 48 / 11, $77.3bn / $73.6bn above the case's $321.8bn / $387.4bn.

- **2024 cash flows (from the case's lines).** At 48 the group paid $112.9bn of OASDI tax and $31.3bn of HI tax,
  and drew $56.3bn of Social Security and $19.7bn of Part A. Cash books the $68.3bn difference as income.
- **What accrual books instead (modelled).** It books the benefits that year's work earns, valued as current law
  will pay them. Each OASDI tax dollar earns $0.97 of benefits net of the income tax the group will pay on them.
  The year's covered work earns $41.1bn of Part A.

Current law here means two things. Benefits are cut to what the trust funds' income pays once their reserves are
depleted (OASDI in 2034, HI in 2033; SSA Note 2025.7 Table 3). The tax on benefits follows the 2025 tax law. The
operator moved the central to payable benefits on 2026-09-28 (see "Payable benefits: the central under current
law"). Scheduled benefits are the benefit formula paid in full, as CBO's baseline assumes by statute. They give
$433.5bn / $493.5bn, the arm `scheduled`, which was the central until then.

Ranges:

- one setting at a time: $365.3–433.5bn at 48 and $428.5–493.5bn at 11, from a 3% real rate to scheduled benefits;
- every combination: $350.8–513.0bn / $414.9–569.0bn.

The route is SSA's money's-worth ratios applied to each year's taxes, the construction that decision 2026-09-19
rejected. The national check says those ratios, applied to the actual population through the lane's frame,
reproduce SSA's own aggregate on the scheduled basis of the Statement of Social Insurance. At 1 January 2025 the
OASDI 15–61 ratio comes out 4.6% high and the HI 15–64 ratio 1.7% high, with levels 3.8–8.0% low, all within the
declared tolerance. The check also removed a Part A spouse credit that counted dependents twice. The lifetime
model's own formula falls 20% short by construction and decides nothing.

Whether accrual can rest on SSA's ratios or needs an extended formula model goes to the operator (recommended: SSA's
ratios). Until then the figure stays beside the case. [CALCULATION: `benefit_tax.py` → `derived/benefit_tax.json`;
`pension_accrual.py` → `derived/summary.json`, `derived/case_beside.csv`; `national_check.py` →
`derived/national_score.json`]

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
`central`]. These are bec1cd7's values. The national check removed the Part A spouse credit, so Part A is now
$45.35bn, its change +25.69, and the case on accrual $437.83bn / $497.78bn (see "Part A: the spouse credit counted
dependents twice"). All of these are on scheduled benefits. The current central's decomposition, on payable benefits
and net of the tax on them, is under "Payable benefits: the central under current law".

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
| Benefits | payable (since 2026-09-28; scheduled until then) | Once a trust fund's reserves are depleted, current law lets SSA pay only what the fund's income covers. Note 2025.7 publishes payable ratios (Table 3), and the Medicare Trustees give HI's payable share. The OASDI Trustees define cost with scheduled benefits, the Part A projections disregard the depletion cuts, and CBO's baseline pays scheduled benefits in full by statute. Scheduled is therefore the arm `scheduled`. [SOURCE: `reads/quotes.json` `tr_cost_is_scheduled`, `mtr_projections_scheduled`, `mtr_hi_payable_path`; CBO, under "Payable benefits: the central under current law"] |
| Discount rate | the Trustees' rate on newly issued trust-fund securities (TR 2025 Table V.B2): 4.1% nominal / 1.7% real in 2026–34, 4.7% / 2.3% from 2045 | This is the government's projected marginal borrowing rate, the right rate for valuing a new obligation. Note 2025.7 instead uses the trust funds' effective portfolio yields (Table B: 0.1–0.8% real in 2025–30), which lag the market. For EAN the two paths differ by 1.3% (1.298 vs 1.281 per tax dollar). [SOURCE: `reads/quotes.json` `tr_new_issue_rates`, `note_mwr_effective_yields`; CALCULATION: `derived/oasdi_arms.csv`] |
| Attribution | entry-age normal (EAN): the lifetime money's-worth ratio times each year's tax | This is the brief's and the 09-18 lane's construction. At trust-fund rates it applies SSA's published ratios directly, and the choice of rate path barely moves it. Projected unit credit (PUC) is $10.8bn lower. PUC spreads the same lifetime benefit in wage-indexed units instead of discounted tax, which gives a young group less when the rate exceeds wage growth. |
| Earnings level | this year's covered earnings over the medium scaled worker's factor at the same age (Note 2025.3 Table 6) | The 09-18 lane's raw wage / AWI treats a 25-year-old's wage as a career average. That inflates young workers' ratios (+$14.9bn as an arm). |
| Career start | Mexico-born: US covered work from arrival (CPS year-of-entry midpoints) | SSA's scaled worker starts at 21. Late arrivals have fewer covered years and can fail the 10-year test. |
| Unauthorized | taxes on the books at 0.526, as in the case; 10% of their accrual credited | Note 151 projects that about 10% of "other immigrants" will be eligible for retired-worker benefits at the end of the 75-year projection, against 30% for those who were 62 in 2000. Suspense-file earnings have "only a relatively remote possibility" of being credited. [SOURCE: `reads/quotes.json` `note151_eligible_share`, `note151_suspense_file`; DATA: `onbooks_share_2026_09_23/derived/onbooks_split.csv`] |
| Mortality | NVSS 2024 period tables for the whole population, improved at the TR's 0.68% (65+) and 0.74% rates | This is the basis of the published ratios. The Hispanic advantage is contested (ethnicity misreporting on death certificates, return migration). Hispanic mortality is an arm (+$19.6bn). [SOURCE: `reads/quotes.json` `tr_mortality_decline_*`] |
| Part A, spouse | the non-working spouse of a one-earner couple qualifies on the worker's record | This matches OASDI's one-earner-couple ratios, which include the spouse's benefit. |

## Arms: one change from the central

$bn, methods averaged. OASDI arms leave Part A at the central, and the reverse; rate, payable, unauthorized and
mortality arms move both. [CALCULATION: `derived/case_beside.csv`] The table holds bec1cd7's values, gross and on
scheduled benefits. Every Part A and case column predates the spouse correction, and the four constant-rate rows
predate the history fix. The current values, net and on payable benefits, are in `derived/case_beside.csv` and
under "Payable benefits: the central under current law".

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
  | Men, payable (the central since 2026-09-28) | $73.8k | $85.4k | $113.1k |
  | Women, payable | $87.1k | $100.3k | $127.2k |

  The payable rows cover HI costs at the Trustees' payable shares: 89% from 2033, falling to 86% in 2049, then
  rising to 100% in 2099. [CALCULATION: `derived/summary.json` `part_a.part_a_pv_at_2024`,
  `part_a_pv_at_2024_payable`; SOURCE: `reads/quotes.json` `mtr_hi_payable_path`]
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
coverage by band. [CALCULATION: `derived/steady_state.csv`, `derived/steady_state_case.csv`] Every 2024 benefit
is paid in full, so this route prices today's benefit rules and compares with the arm `scheduled`. The accrual
rows below are on scheduled benefits (bec1cd7).

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

The parent's premise holds for a person-weighted average of ratios. The accrual weights by tax dollars. With taxes
proportional to the level L, the tax-weighted ratio is ΣB(L) / ΣL, and lifetime benefits B(L) are concave in L, like
the benefit formula's 90/32/15% brackets. A spread in the levels that keeps ΣL therefore lowers the tax-weighted
ratio, and shrinking it raises the ratio. (Corrected after the cross-lab review: this sentence first called the
per-dollar credit B(L) / L concave; it is convex.) The probes shrink the variance of log levels, which also moves
ΣL, so they fix the sign for these transformations only. [INFERENCE, checked by the probes]

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

## Corrections after the cross-lab review

GPT-6 Astra (xhigh) reviewed a packet of this lane on 2026-09-28. The parent checked each finding against these
files and primary sources. What changed here, and what stays open:

**The constant-rate arms keep history.** `lifetime_model.py` `discount()` applied a constant real rate to every year,
so those arms also re-accumulated 1961–2024 taxes at that rate. Real new-issue rates were near zero or negative in
2009–2021, so the arms overstated how much the valuation rate matters. They now take the historical new-issue rates
through 2024, as the central does, and the constant rate from 2025. The central and every other arm are unchanged
(the national check's outputs are identical). [CALCULATION: `derived/case_beside.csv`; parent's finding, not the
reviewer's]

| Arm, case on accrual at 48 / 11 ($bn) | Per tax $, before → after | Before | After |
|---|---|---:|---:|
| real 2% | 1.203 → 1.322 | 427.7 / 488.3 | 441.2 / 501.0 |
| real 2.3% | 1.093 → 1.226 | 410.4 / 471.8 | 425.7 / 486.1 |
| real 3% | 0.872 → 1.031 | 376.6 / 439.4 | 394.9 / 456.7 |
| the case's rates, 2% at 48 and 3% at 11 | | 427.7 / 439.4 | 441.2 / 456.7 |

Gross of the tax on benefits, one setting at a time now spans $394.9–460.3bn at 48 and $456.7–519.2bn at 11 (net:
see "Net of income tax on benefits"). The 3% rate stays the low end; the
high end is the career-mean level mapping at 48 and full credit for unauthorized workers at 11. Every combination
spans $352.4–519.2bn / $416.5–574.9bn. [CALCULATION: `derived/summary.json` `range_across_arms_bn`,
`every_combination_bn`]

**Measured since, in "Net of income tax on benefits" below: the net central is $433.46bn / $493.52bn under current
law, −$4.37bn / −$4.26bn from gross; the estimate in this paragraph is superseded.** **Open (at the time):
benefits are valued before income tax on them.** SSA's ratios leave the tax out: "money's worth ratios
that ignore these transfers may arguably be overstated. Due to the difficulty of determining the level of income
tax on benefits, this factor is not addressed in this note." [SOURCE: SSA Actuarial Note 2025.7, footnote 2] The
accrual inherits the omission, and whatever income tax the case credits on 2024 benefits stays in receipts. A net accrual
subtracts the tax the group will pay on the benefits its 2024 work earns and drops today's tax on today's benefits.
Nationally the tax returns 10.1% of the future benefits of today's 15–61 (5.85% to OASDI; HI receives 0.722 times
OASDI's share). [CALCULATION: `derived/national_score.json` `stock_check.tob_share_15_61`,
`derived/national_prediction.json` `kappa_hi_over_oasdi_tob`] The group's lower incomes put its rate below that.
At 40–80% of the national rate, the net change is roughly −$4.5bn to −$9bn at 48; the national rate bounds it near
−$11bn. [INFERENCE; unmeasured, the group's relative rate is assumed] Part A benefits are not taxed.

**Open, already stated above:** the auxiliary assignment (the calibrated 1.24 against the central's 1.298, −$6.5bn /
−$6.1bn); future disability before 65 in Part A (left out, so Part A is low); the 10% unauthorized credit (a
population share at the end of Note 151's projection, not a measured probability for today's workers; the arms run
from nothing to full credit); entry-age attribution, which the national check cannot test (it checks lifetime
totals, not the split across years, and not the Part A divisor).

**Corrected wording:** "Level assignment and convexity" called the per-dollar credit concave; it is convex, and the
argument runs through the concavity of lifetime benefits in the level (fixed in place).

## Net of income tax on benefits

Brief: [BRIEF_net_of_tax.md](BRIEF_net_of_tax.md) (41e18c6). Worker model: claude-opus-5-5. This section measures
the item left open above ("benefits are valued before income tax on them"); its −$4.5bn to −$9bn estimate is
superseded.

**Net central: $433.46bn / $493.52bn** at specifications 48 / 11, $4.37bn / $4.26bn below the gross central. (That
central was on scheduled benefits and is now the arm `scheduled`. On payable benefits the net central is $399.10bn /
$460.98bn; see "Payable benefits: the central under current law".) Two things change. The OASDI accrual loses the income tax the group will pay on the benefits its 2024 work earns, 4.41%
of their value under current law. The case also stops crediting the tax on the group's 2024 benefits, because those
benefits leave the account. [CALCULATION: `derived/summary.json` `central_decomposition_net`]

**The central path moved at the parent's decision (2026-09-28).** The central now takes the tax-on-benefits path
after the 2025 tax law (see "The 2025 tax law" below). That path is current law, and the Chief Actuary's letter
that gives it uses the same TR 2025 intermediate assumptions as every other input here. This worker had first built
the central on the TR 2025 path, which assumes the TCJA rates expire after 2025. That path is now the arm
`benefit_tax_tr2025_path`: $432.26bn / $492.39bn, 5.23% taxed, −$5.57bn / −$5.38bn from the gross.
[CALCULATION: `summary.json` `benefit_tax.tr2025_path`]

| $bn | Spec 48 | Spec 11 |
|---|---:|---:|
| Gross central (arm `gross_of_benefit_tax`) | 437.83 | 497.78 |
| Income tax on the accrued benefits (4.41% of the OASDI accrual) | −6.46 | −6.07 |
| Tax on the 2024 benefits, dropped from receipts | +2.09 | +1.82 |
| **Net central** | **433.46** | **493.52** |
| Change from the case ($321.82bn / $387.37bn) | +111.64 | +106.15 |

Per dollar of OASDI tax the accrual falls from 1.298 to 1.241 (`ratio_net`; 1.230 on the TR 2025 path). Part A is
untouched, because Medicare benefits are not taxed. [CALCULATION: `derived/case_beside.csv`]

### Step 1: the tax on the 2024 benefits

`benefit_tax.py` runs every CPS ASEC 2025 tax unit (income year 2024) through Tax-Calculator 6.8.2 twice, with and
without its Social Security benefits. The tax units, income mapping and calculator call are the tax lane's
(`tax_rerun_acs_2026_09_17`), imported read-only; their hashes are recorded and checked. The benefit tax is the
difference in income tax, less the net investment income tax, and each return's amount goes to its filers in
proportion to their own benefits.

The central income mapping, `census_income`, adds four items to the tax lane's mapping: IRA distributions, capital
gains, and survivor and disability income. The Census tax model counts all four in AGI, and retirees hold much of
them. [CALCULATION: the checks below]

| 2024 | Benefits ($bn) | Benefit tax ($bn) | Share of benefits | Relative to the nation |
|---|---:|---:|---:|---:|
| Nation | 1,226.3 (8.3) | 74.37 (1.31) | 6.06% (0.09) | 1 |
| The group | 51.26 (1.81) | 1.627 (0.132) | 3.17% (0.22) | **0.523** (0.037) |
| G1, Mexico-born | 21.13 (1.12) | 0.522 (0.076) | 2.47% (0.32) | 0.407 (0.052) |
| G2 | 11.28 (0.96) | 0.446 (0.078) | 3.96% (0.55) | 0.652 (0.092) |
| G3+ | 18.84 (1.16) | 0.659 (0.074) | 3.50% (0.33) | 0.577 (0.055) |

Standard errors from the 160 replicate weights are in parentheses. The CPS captures 83% of the Trustees' $1,471.4bn
of 2024 benefits, and the rates are ratios within the survey. [CALCULATION: `derived/benefit_tax.json`,
`derived/benefit_tax.csv`; SOURCE: TR 2025 Table VI.A3]

Checks:

- **Census FEDTAX_BC (gate).** With benefits in, Tax-Calculator's tax before refundable credits is 1.093 times the
  Census model's FEDTAX_BC for the nation and 1.111 for the group. For units with benefits the ratios are 1.066 and
  1.144. All four sit inside the tax lane's 0.85–1.15 band. [CALCULATION: `benefit_tax.json`
  `results.census_income.gate`]
- **The benefit base.** The Census model files 11,742 of the sample returns with benefits. On those,
  Tax-Calculator's AGI is 1.001 times the Census model's. Its taxable benefits are 1.004 times the Census model's
  implied amount (the Census AGI less Tax-Calculator's AGI without benefits). [CALCULATION]
- **The Trustees.** The national rate is 6.06%. The Trustees' 2024 income from taxation of benefits ($55.1bn OASDI
  plus $39.8bn HI) is 6.39% of OASDI cost ($1,484.8bn). The gap is −5.1%, inside the brief's 25%. [SOURCE: TR 2025
  Table VI.A3; Medicare TR 2025 Table II.B1; CALCULATION]

The tax lane's mapping as it stands (`full`) fails where retirees matter:

- the national rate is 4.86%, −24.0% against the Trustees;
- FEDTAX_BC on units with benefits is 0.818, outside the band;
- taxable benefits are 0.445 of the Census model's on filed returns.

It stays only as a bridge arm. [CALCULATION]

**The receipt the switch drops.** The case keys its federal income tax line ($2,403.24bn nationally) by FEDTAX_BC:
at 48 shared over the SPM unit, at 11 on the person who carries the return. `case_lines.cjs` now stops if that key
changes. The group's benefit tax before refundable credits, allocated the same way, over the key's national Census
total, gives the part of the line that the group's 2024 benefits carry:

- **$2.091bn at 48**: $1.756bn of $2,018.4bn of key;
- **$1.817bn at 11**: $1.498bn of $1,981.1bn.

[CALCULATION: `summary.json` `benefit_tax.current_receipt_bn`] The difference is not rescaled to the Census level,
because the taxable benefits it taxes match the Census model's (1.004). Alternatives:

- over Tax-Calculator's own national total: $1.913bn / $1.663bn;
- the group's relative rate times the Trustees' 6.45% of benefits, times the case's Social Security line: $1.899bn /
  $1.790bn.

[CALCULATION: `benefit_tax.current_receipt_beside_bn`]

One gap remains. After the package's corrections, the case's federal income tax for the group is only 0.806 / 0.791
of this key share: $111.18bn against $137.94bn at 48 and $101.45bn against $128.21bn at 11, methods averaged.
[CALCULATION: `summary.json` `benefit_tax.case_line_over_key_share`] Two corrections account for all of it, to
1.4e-14:

- the CPS-imputation stack, −$12.8bn to −$16.0bn by method and end (on-books scaling of the unauthorized, the
  union-matched hot deck, audit rows 3 and 4, the state-aware status flag);
- CBO's income gradient, −$11.5bn to −$12.7bn.

[CALCULATION: a one-off rebuild from `main_case_2026_09_24/derived/stack_line_deltas.json` and
`external_benchmarks_2026_09_24/derived/cbo_deltas.json`, not written to `derived/`] The unauthorized draw almost no
benefits, so the on-books scaling should leave the benefits' part alone. The hot deck lowers imputed Social
Security, and row 3 and the CBO gradient move tax between income groups, so those should reach it [INFERENCE]. If
the benefits' part shrank in proportion to the whole line, the drop would be $1.685bn / $1.438bn, and the net case
would be $0.41bn / $0.38bn higher ($433.86bn / $493.90bn). [CALCULATION: `benefit_tax.current_receipt_beside_bn`
`scaled_to_case_line`] Pinning the drop down needs the difference computed inside those corrections, which this
lane does not do. The four measures of the drop span $1.69–2.09bn at 48 and $1.44–1.82bn at 11.

**State taxes on benefits.** No state line in the case plainly carries them, so none is netted. The case keys state
and local income tax ($536.2bn nationally) by STATETAX_A, "State income tax liability, after all credits", and the
data dictionary does not say whether that model taxes benefits. [SOURCE: CPS ASEC 2025 data dictionary; DATA:
`model.json`, key `state_liability`] Nine states taxed some benefits in 2024: Colorado, Connecticut, Minnesota,
Montana, New Mexico, Rhode Island, Utah, Vermont and West Virginia. Kansas, Missouri and Nebraska stopped from 2024.
[SOURCE: secondary summaries, URLs in `benefit_tax.json` `state_tax_bound.sources`] The group's benefits in those
states come to $3.52bn (SE 0.40), 6.9% of its benefits (nation 7.9%), and $0.53bn (SE 0.13) of that is federally
taxable. Each state starts from the federally taxable amount [INFERENCE from the same summaries]. At Minnesota's top
rate of 9.85%, the tax is therefore at most $0.05bn a year. [CALCULATION: `benefit_tax.json` `state_tax_bound`]

### Step 2: the tax on the benefits that 2024's work earns

**The national path.** Take income from taxation of OASDI benefits over OASDI cost (TR 2025 Tables IV.B1 and IV.B2,
intermediate, scheduled benefits) and multiply by 1 + κ for HI, where κ = $39.8bn / $55.1bn = 0.722 in 2024. The
TR 2025 path is 6.48% in 2025, 8.50% in 2030, 9.95% in 2050, 10.45% in 2080 and 10.51% in 2100. The central path
multiplies it by the 2025 tax law's factors (below): 6.14%, 7.09%, 8.42%, 8.81% and 8.92%. [SOURCE; CALCULATION:
`summary.json` `benefit_tax.national_path_oasdi_plus_hi`, `national_path_oasdi_plus_hi_after_obbba`]

The Trustees give the reasons the path rises. The thresholds "are specified in the Internal Revenue Code to be
constant in the future, and have never been changed, while income and benefit levels continue to rise". A
"permanent level shift upward" follows from 2026 "due to the expiration of the personal income tax provisions" of
the Tax Cuts and Jobs Act. [SOURCE: TR 2025, section V.C.7, pp. 155–156, `_cache/tr2025.txt`] The 2025 tax law
removed that shift; its deduction for people 65 and over lasts only through 2028, so the shift is most of the
long-run difference between the two paths [INFERENCE].

**Timing.** Each unit's accrued benefits are weighted by their present value in each year, at the central rate and
mortality, as `national_check.window_grid` weights them. The national check gates `tob_timing` against that grid on
22 cohorts (max gap 2.1e-17). At the group's accrual timing the central path gives 8.42%, and the TR 2025 path
9.99%. For comparison, the national check's TR 2025 figure for all of today's 15–61 is 10.1%. [CALCULATION]

**The group's share.** 8.42% × 0.523 = **4.41%** of the accrued value (`benefit_tax.future_share_group`); on the
TR 2025 path, 9.99% × 0.523 = 5.23%. [CALCULATION]

| Generation | Central path × the group's rate | × its own rate | TR 2025 path × the group's rate | × its own rate |
|---|---:|---:|---:|---:|
| G1 | 4.34% | 3.37% | 5.14% | 4.00% |
| G2 | 4.46% | 5.56% | 5.29% | 6.60% |
| G3+ | 4.42% | 4.87% | 5.24% | 5.77% |

With each generation's own rate the group's share is 4.63% on the central path (arm `benefit_tax_generation_rates`).
[CALCULATION: `summary.json` `benefit_tax.future_share_by_generation`, `future_share_by_generation_own_rate`,
`tr2025_path`]

### Step 3: every arm, net

The figures are in $bn, with the two fill-in methods averaged. "Change" is each arm's net figure minus its gross
one; Part A is as in the gross arms. [CALCULATION: `derived/case_beside.csv`] These values are a238f19's, with the
central on scheduled benefits. The current arms, one change from the payable central, are under "Payable benefits:
the central under current law".

Every arm below is on the central path unless it names another.

| Arm | Share taxed | Per tax $, net | Net 48 | Net 11 | Change 48 / 11 |
|---|---:|---:|---:|---:|---:|
| **central** | 4.41% | 1.241 | **433.46** | **493.52** | −4.37 / −4.26 |
| gross_of_benefit_tax (outside the ranges) | 0 | 1.298 | 437.83 | 497.78 | 0 / 0 |
| benefit tax: the TR 2025 path (`benefit_tax_tr2025_path`) | 5.23% | 1.230 | 432.26 | 492.39 | −5.57 / −5.38 |
| benefit tax: relative rate −1.96 SE (0.450) | 3.79% | 1.249 | 434.36 | 494.37 | −3.47 / −3.41 |
| benefit tax: relative rate +1.96 SE (0.597) | 5.03% | 1.233 | 432.55 | 492.67 | −5.27 / −5.10 |
| benefit tax: each generation's own rate | 4.63% | 1.238 | 433.13 | 493.22 | −4.70 / −4.56 |
| payable benefits | 4.39% | 0.974 | 399.08 | 460.96 | −2.96 / −2.93 |
| trust-fund effective rates | 4.42% | 1.225 | 435.70 | 495.87 | −4.30 / −4.19 |
| real 2.3% flat | 4.41% | 1.172 | 421.69 | 482.21 | −4.01 / −3.92 |
| real 2% | 4.41% | 1.264 | 436.70 | 496.60 | −4.50 / −4.38 |
| real 3% | 4.39% | 0.986 | 391.90 | 453.69 | −3.03 / −2.99 |
| the case's rates, 2% at 48 and 3% at 11 | | 1.264 / 0.986 | 436.70 | 453.69 | −4.50 / −2.99 |
| unauthorized credited nothing | 4.41% | 1.225 | 431.05 | 491.21 | −4.29 / −4.18 |
| unauthorized at 30% | 4.41% | 1.271 | 438.28 | 498.14 | −4.53 / −4.40 |
| unauthorized credited in full | 4.41% | 1.378 | 455.17 | 514.30 | −5.09 / −4.93 |
| attribution PUC | 4.40% | 1.149 | 423.15 | 483.84 | −3.88 / −3.79 |
| attribution ABO | 4.46% | 1.342 | 444.97 | 504.34 | −4.98 / −4.83 |
| earnings level: raw wage / AWI | 4.41% | 1.367 | 447.71 | 506.91 | −5.04 / −4.88 |
| earnings level: generation's career mean | 4.41% | 1.431 | 454.95 | 513.71 | −5.36 / −5.19 |
| every career from 21 | 4.41% | 1.216 | 430.71 | 490.93 | −4.25 / −4.14 |
| Hispanic mortality | 4.41% | 1.360 | 451.86 | 511.11 | −5.00 / −4.85 |
| *bridge:* national rate (relative rate 1) | 8.42% | 1.188 | 427.57 | 487.99 | −10.25 / −9.78 |
| *bridge:* the tax lane's mapping (`full`) | 4.95% | 1.234 | 432.45 | 492.58 | −5.38 / −5.19 |
| *bridge:* Part A spouse credit (bec1cd7) | 4.41% | 1.241 | 439.39 | 499.45 | −4.37 / −4.26 |
| *bridge:* r = g | 4.43% | 1.505 | 479.54 | 537.80 | −5.79 / −5.59 |
| *bridge:* 09-18 settings | 4.42% | 1.449 | 467.78 | 526.43 | −5.48 / −5.30 |

The arm `benefit_tax_after_obbba` stays in the CSVs by name and now equals the central. The tax lane's bridge also
drops a smaller receipt, $1.874bn / $1.623bn.

Real 3% is still the low end, at $391.90bn / $453.69bn. The high end is full credit for unauthorized workers at both
ends, at $455.17bn / $514.30bn. Every combination of the non-bridge settings spans $350.62–512.98bn /
$414.69–568.96bn. That envelope is on the central path and takes each of four benefit-tax rates: the group's, 1.96
SE either side, and each generation's own. The TR 2025 path is an arm inside the one-at-a-time range; it sets
neither end and is not in the envelope. [CALCULATION: `summary.json` `range_across_arms_net_bn`,
`every_combination_net_bn`]

**Gates.**

- With the share at 0 the switch reproduces the gross central exactly, and 8062db1's $437.828882bn / $497.775764bn
  to 1e-6.
- On each path, the central's timing computed through the spouse arm's machinery equals the arms' to 1e-12.
- Every existing key in `summary.json` and every existing row and column of the derived CSVs is unchanged; only the
  net values move with the central. `central_decomposition.low.accrual_per_tax_dollar`, which candidate v3 reads as
  its ratio, keeps its gross meaning, and `ratio_net` sits beside it.
- Against the outputs before the move, every gross column is identical, and the arm `benefit_tax_tr2025_path`
  reproduces the earlier central ($432.26bn / $492.39bn) exactly.
- The national check's outputs are unchanged, and `derived/national_prediction.csv` keeps its frozen sha256.

[DATA: `summary.json` `gate_net_with_no_tax`]

### The 2025 tax law

The TR 2025 path assumes that the TCJA rates expire after 2025. P.L. 119-21 (the OBBBA) made them permanent and
raised the deduction for people 65 and over for 2025–2028. SSA's Chief Actuary: "the trust funds will receive lower
levels of projected revenue from income taxation of Social Security benefits for all years beginning in 2025". The
75-year OASDI balance falls by 0.16% of taxable payroll, all of it through the income rate. [SOURCE: OCACT letter
to Senator Wyden, 5 August 2025, Wayback 20250809085421, sha256 `f402b44d…` pinned in `sources.py`]

Its Table 1 puts the OASDI path at 0.947 of the Trustees' in 2025, 0.783 in 2026, 0.833 in 2030 and about 0.85 from
2050 [CALCULATION: `summary.json` `benefit_tax.after_obbba.path_factor`]. The letter leaves HI out, and the central
path moves HI in proportion [INFERENCE]. The path taxes 4.41% against the TR 2025 path's 5.23%, which puts the net
case $1.20bn / $1.13bn higher.

**The central takes this path at the parent's decision of 2026-09-28**, as this section had recommended. It is
current law, and the letter uses the same TR 2025 intermediate assumptions as every other input here. [DATA:
`summary.json` `benefit_tax.central_path`, `central_path_basis`]

### Item 4: spouses' own records (time-boxed)

The central prices 2.52M workers as one-earner couples: married, with a spouse who has no 2024 wages. They pay 13.7%
of the group's OASDI tax. [CALCULATION: `summary.json` `spouse_own_record_arm`] The CPS ASEC shows the following
for their spouses, as shares of those workers' tax:

| Spouse | Share of tax | Records |
|---|---:|---:|
| self-employment income in 2024 | 12.7% | 173 |
| employed or on layoff in March 2025, or worked in the last 12 months | 4.8% | 59 |
| last worked more than 12 months ago | 4.8% | 61 |
| never worked | 0.4% | 4 |
| not known | 77.4% | 933 |

- **Self-employment is missed.** The family assignment counts only the spouse's wages, so a self-employed spouse is
  priced as having no record. Three of the 173 records fall below SECA's $400 floor, 3.8% of that row's tax.
  [CALCULATION: a one-off probe on the lane's frame, not written to `derived/`]
- **Most spouses are not known.** The CPS asks when-last-worked mainly in the fourth and eighth months in sample.
  Among adults outside the labor force it is answered for about 52% in those months and 2–6% in the others.
  [CALCULATION: a probe on the CPS ASEC 2025 person and household files by `H_MIS`; SOURCE: data dictionary]
- **"Worked" is not a record.** The work items count work abroad and do not show 40 covered quarters.

Moving the spouses with current work of their own (the first two rows, 17.5% of the tax) to two-earner pricing gives
1.277 per tax dollar, between the bounds of 1.298 and 1.186. On the central path the net case is then $431.26bn /
$491.45bn, $2.20bn / $2.07bn below the central; the two-earner bound gives $421.43bn / $482.21bn. (On the TR 2025
path: $430.08bn / $490.34bn and $420.33bn / $481.18bn.) The CPS cannot place the 77% whose
status is not known, so it supports a point just below the central, not the two-earner bound. ACS 2024 PUMS `WKL`
is asked of everyone and would narrow the unknown row [INFERENCE]; it was not tabulated. The central is unchanged.
[CALCULATION: `summary.json` `spouse_own_record_arm`]

### Limits

- **The relative rate is today's.** It is measured on today's beneficiaries and held for today's workers. The
  thresholds are fixed, so a growing share of everyone's benefits becomes taxable, and that should raise the group's
  rate toward the nation's [INFERENCE]. The national-rate bridge bounds this at 8.42% ($427.57bn / $487.99bn). The
  ±1.96 SE arms cover sampling error only.
- **Cost, not benefits.** The path divides by OASDI cost, as the national check does. Over benefits it would be about
  0.9% higher (2024: $1,484.8bn / $1,471.4bn), which is worth under $0.1bn. [CALCULATION]
- **κ is held at 2024.** HI takes the tax on benefits between the 50% and 85% inclusion tiers, which grow as the
  thresholds erode, so κ likely rises [INFERENCE]. The central path moves HI in proportion to OASDI.
- **Tax law can change again.** The central path is current law. The TR 2025 path shows what a return of the
  pre-2018 rates would do: 5.23%, −$1.20bn / −$1.13bn.
- **The timing unit** is the medium worker from 21. The level scales benefits, not their timing. The unit omits
  disability and young survivors' benefits, which are paid earlier, when the path is lower [INFERENCE]. The payable
  arm applies the scheduled path at its own timing.
- **Survey income.** The key and the difference are both model outputs on survey income. The rates assume the group
  reports as fully as the nation [INFERENCE].

### Files and reproduction

New:

- `benefit_tax.py` → `derived/benefit_tax.json` (every measure with its replicate SE, the gates, the Trustees check,
  the state bound, the hashes of the script and of the imported tax-lane files) and `derived/benefit_tax.csv`;
- `sources.py` pins the OCACT letter (`_cache/ocact_obbba_wyden_20250805.*`, ignored) and parses its Table 1 with
  gates: every year from 2025 to 2100 once, cost rates unchanged and equal to Table IV.B1's, and the 75-year −0.16%.

Changed (the derived files gain rows, columns and keys only):

- `case_lines.cjs`: the federal income tax line, gated on its key (4 rows in `case_lines.csv`);
- `pension_accrual.py`: the net switch on both paths, the arms, `summary.json`'s new keys (including
  `benefit_tax.central_path`, `tr2025_path` and `national_path_oasdi_plus_hi_after_obbba`) and the spouse arm;
- `national_check.py`: it reads the path from `pension_accrual` (one definition) and checks `tob_timing` against
  `window_grid`;
- `case_beside.csv`: net columns and the new arms;
- `oasdi_arms.csv`: `accrual_tob_bn` (the TR 2025 path) and `accrual_tob_obbba_bn` (the central path);
- `oasdi_by_generation.csv`: `national_path_share`, `national_path_share_after_obbba` and the new arms;
- `sources.json`: the letter.

This command supersedes the one under "Reproduction" (Tax-Calculator runs in an overlay environment):

```sh
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/pension_accrual_2026_09_28 \
  "node {lane}/case_lines.cjs" \
  "OPENBLAS_NUM_THREADS=1 uv run --no-project --with taxcalc==6.8.2 python3 {lane}/benefit_tax.py" \
  "OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/pension_accrual.py" \
  "OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/national_check.py" \
  --allow-unrun infra/immigration-fiscal/pension_accrual_2026_09_28/lifetime_model.py \
  --allow-unrun infra/immigration-fiscal/pension_accrual_2026_09_28/sources.py
```

## Payable benefits: the central under current law

The operator moved the central from scheduled to payable benefits on 2026-09-28. [DATA: `summary.json`
`central.scenario`, `central_scenario_basis`]

**The central, $bn** (the two fill-in methods averaged) [CALCULATION: `derived/summary.json` `central_decomposition`,
`central_decomposition_net`, `scheduled_arm`]

| | Spec 48 | Spec 11 |
|---|---:|---:|
| The case | 321.82 | 387.37 |
| OASDI taxes credited (unchanged) | 112.94 | 106.13 |
| OASDI accrual net of the income tax on it (0.974 per tax dollar: 1.018 gross, 4.39% taxed) | 109.97 | 103.34 |
| 2024 Social Security benefits removed | 56.26 | 53.02 |
| Tax on the 2024 benefits, dropped from receipts | +2.09 | +1.82 |
| **Change, OASDI** | **+55.80** | **+52.13** |
| HI taxes credited (unchanged) | 31.28 | 29.15 |
| Part A accrual, payable | 41.14 | 41.14 |
| 2024 Part A benefits removed | 19.66 | 19.66 |
| **Change, Part A** | **+21.47** | **+21.47** |
| **The case on accrual, current law** | **399.10** | **460.98** |
| Scheduled benefits (arm `scheduled`) | 433.46 | 493.52 |

**What is measured and what is modelled.** The 2024 flows are the case's own lines. At 48 the group paid $144.2bn
of OASDI and HI tax and drew $75.9bn of Social Security and Part A. Cash books the $68.3bn difference as income
($62.6bn at 11). That part of the change does not depend on the benefit level: at one dollar of claims per tax
dollar, accrual would replace the surplus exactly. The model decides the rest. [CALCULATION]

- **OASDI** earns 0.974 per tax dollar net, $3.0bn / $2.8bn below one-for-one.
- **Part A** earns $41.1bn against $31.3bn / $29.1bn of HI tax, $9.9bn / $12.0bn above it.
- **The receipt.** The switch drops $2.1bn / $1.8bn of receipts.

At scheduled benefits the OASDI claims run $27.2bn / $25.5bn above one-for-one and Part A $14.1bn / $16.2bn above
it. That is the extra $34.4bn / $32.5bn.

**Why payable is current law.**

- **The legal limit.** Once a trust fund's reserves are depleted, SSA may pay only what the fund's income covers:
  "Under current law, the Social Security Administration cannot pay benefits in excess of the available balances in
  a trust fund." [SOURCE: CBO, *OASI Baseline*, January 2025,
  https://www.cbo.gov/system/files/2025-01/51308-2025-01-socialsecurity.pdf] Beneficiaries "will remain legally
  entitled to full benefits", and "the method for reducing payments is not prescribed in current law". [SOURCE:
  CBO, *CBO's 2024 Long-Term Projections for Social Security*, https://www.cbo.gov/publication/60679]
- **Scheduled benefits are the budget convention.** "The rules that govern baseline construction require the
  Congressional Budget Office to assume that scheduled payments from federal trust funds will continue to be made
  in full even if a trust fund has been exhausted and there is no legal authority to make such payments." [SOURCE:
  CBO, January 2025, as above; the rule is section 257(b)(1) of the Balanced Budget and Emergency Deficit Control
  Act, per CBO 2024] The Trustees' cost and the Statement of Social Insurance use scheduled benefits too.
- **One reading throughout.** The central already took the tax on benefits from current law (see "The 2025 tax
  law"). Valuing the benefits at the schedule while taxing them under current law mixed two readings. The central
  now reads current law for both.
- **SSA publishes the payable ratios.** Note 2025.7 Table 3 pays 90.2% of scheduled benefits in 2034 and 80.7% in
  2035, falling to 71.9% in 2099. HI pays 89% from 2033. [SOURCE: `reads/quotes.json` `note_payable_*`,
  `mtr_hi_payable_path`]

**What the cut means for benefit levels.** The cut applies to a schedule that grows with wages, not to today's
benefits. TR 2025 Table V.C7 puts the scheduled benefit at 65 of the medium scaled worker at $25,172 for 2025 and
$41,553 for 2065, in CPI-indexed 2025 dollars. At Note 2025.7's payable share for 2065 (76.6%) that is $31.8k,
1.26 times today's benefit in real terms. Right after depletion (2035) it is 0.94 times today's, and it passes
today's level around 2045 (1.05). [SOURCE: TR 2025 Table V.C7 through `sources.benefit_amounts_v_c7`; CALCULATION:
the payable share on the lane's linear path]

**The model factor on payable benefits.** Before this move the payable arm took the model factor computed on
scheduled benefits. Each scenario now takes its factor from a model grid on the same scenario
(`model_grid(..., payable)`). That grid is gated like the scheduled one: the factor is 1 on Note 2025.7's basis, and
the attributions add up.

- Across the factorial the payable ratios move by −0.28% to +0.53%.
- The central moves +0.016%, +$0.02bn from the old payable arm's $399.08bn / $460.96bn.
- Part A needed no change, because its payable runs already used the HI payable path. A Hispanic-mortality Part A
  run on payable benefits was added, so that arm is one change from the central.

[CALCULATION: a comparison with the committed outputs (a238f19), not written to `derived/`]

**One change from the central, net, $bn** [CALCULATION: `derived/case_beside.csv`]

| Arm | Per tax $, net | ΔOASDI, net 48 / 11 | ΔPart A | Net 48 | Net 11 |
|---|---:|---:|---:|---:|---:|
| **central (payable benefits)** | 0.974 | 55.8 / 52.1 | 21.5 | **399.10** | **460.98** |
| scheduled benefits (`scheduled`; the central until 2026-09-28) | 1.241 | 85.9 / 80.5 | 25.7 | 433.46 | 493.52 |
| trust-fund effective rates | 0.959 | 54.1 / 50.6 | 25.1 | 401.05 | 463.03 |
| real 2.3% flat | 0.920 | 49.7 / 46.4 | 17.8 | 389.36 | 451.61 |
| real 2% | 0.990 | 57.6 / 53.8 | 22.1 | 401.52 | 463.29 |
| real 3% | 0.778 | 33.7 / 31.4 | 9.8 | 365.31 | 428.52 |
| the case's rates, 2% at 48 and 3% at 11 | 0.990 / 0.778 | 57.6 / 31.4 | 22.1 / 9.8 | 401.52 | 428.52 |
| unauthorized credited nothing | 0.962 | 54.4 / 50.8 | 20.9 | 397.11 | 459.07 |
| unauthorized at 30% | 0.998 | 58.5 / 54.7 | 22.7 | 403.07 | 464.79 |
| unauthorized credited in full | 1.083 | 68.2 / 63.7 | 27.0 | 416.99 | 478.13 |
| attribution PUC | 0.906 | 48.2 / 45.0 | 21.5 | 391.48 | 453.82 |
| attribution ABO | 1.027 | 61.8 / 57.8 | 21.5 | 405.11 | 466.63 |
| earnings level: raw wage / AWI | 1.072 | 66.9 / 62.6 | 21.5 | 410.24 | 471.45 |
| earnings level: generation's career mean | 1.129 | 73.4 / 68.7 | 21.5 | 416.69 | 477.50 |
| every career from 21 | 0.953 | 53.5 / 49.9 | 21.5 | 396.77 | 458.79 |
| Hispanic mortality | 1.066 | 66.2 / 61.9 | 26.0 | 413.99 | 475.25 |
| benefit tax: each generation's own rate | 0.972 | 55.6 / 51.9 | 21.5 | 398.87 | 460.76 |
| benefit tax: relative rate −1.96 SE | 0.980 | 56.5 / 52.8 | 21.5 | 399.80 | 461.64 |
| benefit tax: relative rate +1.96 SE | 0.967 | 55.1 / 51.5 | 21.5 | 398.39 | 460.31 |
| benefit tax: the TR 2025 path | 0.965 | 54.9 / 51.3 | 21.5 | 398.16 | 460.09 |
| gross of the benefit tax (outside the ranges) | 1.018 | 58.8 / 55.1 | 21.5 | 402.05 | 463.90 |
| *bridge:* national benefit-tax rate | 0.933 | 51.2 / 47.8 | 21.5 | 394.50 | 456.66 |
| *bridge:* the tax lane's mapping | 0.968 | 55.0 / 51.4 | 21.5 | 398.26 | 460.20 |
| *bridge:* Part A spouse credit (bec1cd7) | 0.974 | 55.8 / 52.1 | 26.8 | 404.41 | 466.29 |
| *bridge:* r = g | 1.171 | 78.1 / 73.1 | 36.4 | 436.36 | 496.90 |
| *bridge:* 09-18 settings | 1.133 | 73.8 / 69.0 | 31.2 | 426.76 | 487.56 |

The arms `payable` and `benefit_tax_after_obbba` stay in the CSVs by name and equal the central.

- **One setting at a time:** $365.31–433.46bn at 48 and $428.52–493.52bn at 11. The low end is a 3% real rate and
  the high end is scheduled benefits.
- **Every combination of the non-bridge settings:** $350.81–512.98bn / $414.87–568.96bn net ($352.58–519.18bn /
  $416.68–574.94bn gross). The envelope already covered both scenarios. Only its low corner moved, with the payable
  factor.

With spouses' own work priced as two-earner couples (item 4), the payable central is $397.36bn / $459.34bn; the
two-earner bound is $389.48bn / $451.94bn. [CALCULATION: `summary.json` `range_across_arms_net_bn`,
`every_combination_net_bn`, `spouse_own_record_arm`]

**Checks.**

- **The scheduled arm reproduces the earlier centrals.** It gives a238f19's net central ($433.458300bn /
  $493.520586bn) and 8062db1's gross central ($437.828882bn / $497.775764bn) to 1e-6, and `pension_accrual.py` stops
  otherwise. Every column of that arm equals the earlier central's exactly, and every scheduled row of
  `oasdi_arms.csv` and `hi_arms.csv` is unchanged. [DATA: `summary.json` `gate_net_with_no_tax`]
- **The national check stays on the Statement of Social Insurance's scheduled basis.** Its probe of the group's
  ratio and its Part A spouse check now compare with the arm `scheduled`, and their outputs are byte-identical. Only
  `national_score.json` `central_mapping` moves, because it maps the declared scaling rule onto the central; the
  rule does not apply. `derived/national_prediction.csv` keeps its frozen sha256.
- **The steady-state cross-check prices today's benefit rules.** It therefore compares with the arm `scheduled`:
  $111.6bn / $106.2bn against the stationary routes' $103.8–128.8bn. [CALCULATION: `derived/steady_state_case.csv`]

**Limits.**

- **The tax path is the Trustees' share of scheduled benefits.** The central applies it to payable benefits. Lower
  benefits leave some beneficiaries under the fixed thresholds, so the share taxed would be somewhat lower and the
  net accrual somewhat higher. The effect fades as the thresholds erode. [INFERENCE; unmeasured]
- **How benefits would be cut is not in the law.** The proportional cut is SSA's and CBO's modelling convention. A
  cut that spared low earners would put this lower-earning group nearer the scheduled value. [INFERENCE]
- **Legislation.** The 1983 amendments, the last major rebalancing, combined tax increases with benefit cuts. They
  advanced scheduled tax-rate increases, taxed benefits, delayed a COLA and raised the retirement age to 67.
  [SOURCE: SSA, Summary of P.L. 98-21, https://www.ssa.gov/history/1983amend.html] A fix through taxes alone would
  leave today's claims at the scheduled value and raise later taxes, which this year's account does not see. A mix
  lands between the two readings. The account prices current law, not a forecast of legislation. [INFERENCE]

**Reproduction.** The command under "Net of income tax on benefits", "Files and reproduction", is unchanged. Two
consecutive reruns: 34/34 files identical, rc 0 (passes started 16:59 and 17:01 JST).

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
- 2026-09-28 12:13 JST (parent). After the cross-lab review: `lifetime_model.py` `discount()` keeps the historical new-issue
  rates through 2024 in the constant-rate arms (probe first, then in place; the in-place `case_beside.csv` matched
  the probe byte for byte). Changed outputs: `case_beside.csv`, `oasdi_arms.csv`, `hi_arms.csv`,
  `oasdi_by_generation.csv`, `summary.json` (the rate arms and the ranges); the national check's outputs are
  unchanged. Verdict, the two stale tables' captions and the convexity sentence edited; new section "Corrections
  after the cross-lab review".
- 2026-09-28 13:27 JST (worker, BRIEF_net_of_tax.md). Net of income tax on benefits built (section above):
  `benefit_tax.py` (Tax-Calculator 6.8.2 on the tax lane's CPS tax units; the tax lane's own mapping misses retirees'
  income, so the central adds IRA distributions, capital gains, survivor and disability income), the net switch in
  `pension_accrual.py`, the federal income tax line and its key gate in `case_lines.cjs`, the path read by
  `national_check.py` from one definition. Gates pass: FEDTAX_BC 1.093 / 1.111; −5.1% against the Trustees; no tax
  reproduces 8062db1; the national check is unchanged. Net central $432.26bn / $492.39bn. Added after the first
  reruns: the state-tax bound, the receipt scaled to the case's corrected line, and the spouse category relabelled
  from "covered" self-employment to self-employment income. The OBBBA letter was pinned in `sources.py` as an arm.
- 2026-09-28 13:29 JST (worker). Two consecutive reruns of the final code with the new command ("Files and
  reproduction" in "Net of income tax on benefits"): 34/34 files identical both times, rc 0 (passes started 13:27
  and 13:28 JST). The prediction file kept its frozen sha256 `b8b5c3f5…d7d9`. Nothing committed, staged or stashed.
- 2026-09-28 13:42 JST (worker). At the parent's decision (current law), the central moved to the tax-on-benefits
  path after the 2025 tax law. The TR 2025 path became the arm `benefit_tax_tr2025_path`, and it reproduces the
  earlier central ($432.26bn / $492.39bn) exactly. Both paths now run at every setting (`accrual_tob_obbba_bn`), so every net arm,
  both envelopes and the spouse arm are on the new central. New central: $433.46bn / $493.52bn (−$4.37bn /
  −$4.26bn from the gross; 4.41% taxed). Every gross column is unchanged, and the no-tax gate reproduces 8062db1 to
  1e-6. Two consecutive reruns with the superseding command (passes started 13:40 and 13:41 JST): 34/34 identical,
  rc 0. The prediction file kept its frozen sha256. Nothing committed, staged or stashed.
- 2026-09-28 17:03 JST (parent). At the operator's decision (16:40 JST, "move the lane"), the central moved to payable
  benefits. The earlier central is the arm `scheduled`, gated to reproduce a238f19 net and 8062db1 gross to 1e-6.
  Payable now takes its own model factor (+$0.02bn on the central). A Hispanic-mortality Part A run on payable was
  added. `national_check.py` compares its probe and spouse check with the arm `scheduled`. New central $399.10bn /
  $460.98bn. Changed outputs: `case_beside.csv`, `oasdi_arms.csv` (payable rows only), `hi_arms.csv` (32 rows added),
  `oasdi_by_generation.csv` (the new arm), `summary.json`, and `national_score.json` (`central_mapping` only). The
  prediction file kept its frozen sha256. Verdict rewritten, new section "Payable benefits: the central under current
  law". Two consecutive reruns: 34/34 identical, rc 0.
