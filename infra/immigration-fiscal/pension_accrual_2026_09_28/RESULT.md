claude-opus-5-5

**Verdict:** On an accrual basis for Social Security (OASDI) and Medicare Part A, the September 27 case becomes
**$443.8bn / $503.7bn** at specifications 48 / 11 under the central arm. That is up $121.9bn / $116.3bn from
$321.8bn / $387.4bn. Changing one setting at a time moves it to $381–467bn at 48 and $444–526bn at 11. Every
combination of settings spans $348–527bn / $413–583bn. The figure sits beside the case, never in it; adoption is
the operator's call. [CALCULATION: `pension_accrual.py` → `derived/summary.json`, `derived/case_beside.csv`]

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
entitlement accrual". Its trigger for revisiting is "an independently validated pension accrual model". This lane
supplies one. Whether it meets that bar is the operator's call.

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
