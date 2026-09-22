# A practitioner range for the September 19 ledger: recut of the arms grid

Date: 2026-09-22. [MODEL / FRAMING-SENSITIVE] Calculation record on a published
accounting scenario; narrative authorship remains operator-owned.

**Verdict:** On the pinned September 19 ledger, the conventions a budget modeler would
run put the Mexican-origin union's annual expanded balance between **−$290bn and
−$190bn**, central **−$217bn**. The full switch design spans −$496bn to −$76bn over 63
admissible cells and reaches +$41bn only when every congestible service is free. The
range the lane's own RESULT.md still prints, −$548bn to −$87bn over 144 cells around
−$254bn, is the pre-repair September 17/18 build and is stale. Charging defense, net
interest and general government per capita is a second object, −$502bn to −$402bn around
−$429bn, and is reported beside the first, not inside it. None of these hulls is a
confidence interval; the survey standard error of any cell is $8–10bn.
[CALCULATION: [`ledger_recut_2026_09_22`](../infra/immigration-fiscal/ledger_recut_2026_09_22/RESULT.md)]

## 1. Object and vintage

The object is `ledger_absolute_2026_09_17` as rebuilt on September 19 (commit 6a4b8b0,
outputs byte-identical after the September 20 data-root refactor): the union of the three
Mexican-origin target groups, 40.9m civilian household residents, income-year 2024,
household-shared allocation, items D and P on, enforcement zero in the central because
its appropriation sits inside OMB function 750, which item R charges per capita. It is an
expanded partial account, not a marginal effect of immigration and not a lifetime value.
[SOURCE: [repaired calculation index](immigration-yearly-lifetime-cost-repair-2026-09-19.md)]

It is not the September 20 complete account ($165–197bn to other residents), not the
generation-vs-white gaps, and not the later annual vintages (−$234bn finance refresh,
−$259bn enrollment correction). The FAQ's
[combining rules](immigration-objections-faq-2026-09-21.md#before-combining-numbers-from-different-entries)
apply: one is not a decomposition of another.

A recut proposal reviewed on September 22 was built on the stale RESULT.md verdict. Its
logic survives; its numbers do not:

| Cell | Proposal (Sept 17/18 build) | Live grid (Sept 19 build) |
|---|---:|---:|
| Central | −254 | −217 |
| Practitioner pessimistic | −330 | −290 |
| School m 0.63 on every dialled item | −147 | −122 |
| Wishful corner (R zero, C per capita) | −87 | −76 |
| No congestible services (m = 0) | +35 | +41 |
| Public goods per capita on the central | −470 | −429 |
| Stacked corner | −548 | −496 |
| Practitioner optimistic | −210 to −254 | −190 (built here) |

The proposal's third question, whether to wait for the grant double-count repair, is
moot: that repair is the September 19 build. D and P are inside every live number.
[DATA: `ledger_absolute_2026_09_17/derived/arms_matrix.csv`, `waterfall.csv`, `audit.json`]

## 2. The switches, who runs them, and which enter the set

Each switch is priced one at a time against the central, with the replicate standard
error of the difference. Grid arms are differences of published grid cells; the rest are
linear combinations of the published per-item replicate vectors. Billions of 2024
dollars per year.

| Switch | Δ | SE | Side | In set | Who runs it |
|---|---:|---:|---|---|---|
| R: every netted federal function per capita | −58.5 | 1.8 | strict | yes | average-cost budget accounting that spreads non-entitlement federal functions per head |
| R: housing assistance by reported SPM subsidy | −0.4 | 0.8 | strict | yes | records-based refinement of the central |
| R: all functions zero | +92.2 | 1.7 | lenient | no | nobody: it zeroes veterans' cash, federal civilian pensions and justice, which are records-based outlays, not public goods |
| C: corporate tax 100% to capital | −8.8 | 0.4 | strict | yes | the older incidence convention [TRAINING-DATA: CBO's pre-2012 rule]; the central 25/75 is CBO's current rule (FAQ 2) |
| C: per capita | +49.0 | 1.2 | lenient | no | nobody: headcount is not an incidence theory |
| C: borne by consumers | +27.1 | 1.0 | lenient | no | a minority incidence view used in some state tax-incidence studies; disclosed, outside the set |
| E: charged to Mexico-born noncitizens, removed from the per-capita justice charge | −2.4 | 0.1 | strict | yes | the targeted-enforcement convention, netted; the builder admits the stacked version only with R all zero |
| F: federal general government at the administration elasticity 0.824 | −3.5 | 0.03 | strict | yes | the measured-response arm the repo proposes for the complete account; small here because state-local administration is inside G |
| F: defense, net interest, general government per capita | −211.7 | 2.0 | strict | second object | average-cost public goods [TRAINING-DATA: the National Academies' average-cost scenarios]; defense −101.6, interest −105.8, general government −4.2 |
| F: in proportion to federal taxes paid | −118.5 | 3.0 | strict | second object | benefit-principle variant of the same object |
| G: cross-state function elasticities | +9.5 | 0.1 | lenient | yes | police 1.037, fire 1.085, highways 0.727, parks 0.948, libraries 0.974, administration 0.824; the 72% of G without an estimate held at 1 |
| G: state-local interest on general debt at zero | +13.5 | 0.1 | lenient | yes | consistency: item F already fixes federal interest at zero; interest is 8.1% of G |
| K, D: within-district school elasticity 0.836 | +4.2 | 0.1 | lenient | yes | the CBO-type school response on the school items this ledger holds on its dial |
| K, D: same at 0.735 (unweighted) | +6.7 | 0.1 | lenient | no | lower bound of the same |

The grid's own restriction on E is right as far as it goes: charging ICE, EOIR and
appropriated USCIS to the unauthorized while also charging function 750 per capita
counts the same dollars twice. The netted cell removes the union's headcount slice of
those dollars first, which is why it costs $2.4bn rather than $2.7bn.
[CALCULATION: `ledger_recut_2026_09_22/derived/switch_moves.csv`; elasticities
[scaling test](immigration-service-scaling-test-2026-09-20.md), year-effects column and
within-district rows; G composition `derived/g_composition.csv` from the 2022 Census of
Governments functional lines 76–112]

## 3. Cells and hulls

| Hull | Low | Central | High |
|---|---:|---:|---:|
| Practitioner | −290.5 | −217.3 | −190.1 |
| Design grid, 63 cells | −496.2 | −217.3 | −76.1 |
| Design grid plus the dial | −496.2 | −217.3 | +40.9 |
| Second object, public goods per capita | −502.1 | −429.0 | −401.8 |

The strict bound stacks R all per capita, C all capital, enforcement targeted and general
government at 0.824. The lenient bound stacks the cross-state function elasticities on G,
interest treated alike at both levels, and the school elasticity on K and D. Disclosed
but outside the set: 0.63 on every dialled item (−121.8, the school coefficient applied
to police, fire, highways and federal functions), the same with 0.63 on base school
current spending (−79.0, point only, base school is not on the dial), the wishful corner
(−76.1) and m = 0 (+40.9, taxes and transfers only, the convention behind "they pay more
than they take"). The personal-source allocation of the same account is −239.2 and is a
different allocation, not a switch.
[CALCULATION: `derived/named_cells.csv`, `derived/hulls.csv`]

## 4. Why the range is a hull of named conventions

The account is linear in its items, so a range is a statement about which switch
settings are admitted, and it has three layers, each its own object:

1. **Conventions.** The practitioner hull, each arm tagged with the class of modeler that
   runs it; the design hull disclosed beside it; dropped cells listed with the reason.
   The complete account already reports this way ($165–197bn CBO-informed against
   $270–289bn full average cost).
2. **Parameters inside a convention.** One-at-a-time moves at source-given alternatives,
   which is what the table in §2 is, with the replicate SE beside each so the reader
   sees that conventions dominate sampling by an order of magnitude.
3. **Instrument bias.** A completeness audit of the arm list from both sides: for each
   side, which arm would its strongest expert insist on that is missing? Bias enters
   through which arms are built, which one is called central and which items are
   labelled congestible, so that is where it is checked.

| Side | Arm | Status |
|---|---|---|
| strict | enforcement charged to the enforced, netted | built here (−2.4) |
| strict | measured response on general government | built here (−3.5); the state-local part is already at average cost inside G |
| strict | defense and interest per capita | the second object, reported beside the first |
| strict | capital stock other than school capital | unpriced in the ledger (`audit.json` `unpriced`); not built |
| strict | crime victimization costs | outside a fiscal account by the [custody/crime rule](immigration-detention-crime-and-fiscal-scope-2026-09-20.md) |
| lenient | per-function response below one | built here on G, K, D; base school current spending is off the dial (+42.8 if 0.63 were applied there, disclosed) |
| lenient | interest treated alike at both levels | built here (+13.5) |
| lenient | consumption incidence of corporate tax | built here (+27.1), disclosed outside the set |
| lenient | personal-source allocation | published (−239.2), a different allocation |
| lenient | production and general-equilibrium offsets | outside this object; in the complete account and ladder 164–167 |

The scale behind the net, for reading the switch moves:

| Union, shared allocation | $bn |
|---|---:|
| Gross receipts | 417.0 |
| Gross outlays | −634.3 |
| Net | −217.3 |
| Replicate SE of the central | 8.7 |

The two objects' centrals sit on opposite sides for one item. This ledger charges
state-local general services at full average cost; the complete account holds general
public services at zero response. Reporting both centrals is the hedge that exists; the
open general-government proposal (0.59–0.84 response on the complete account) is the one
concrete correction pending on the lenient object.
[SOURCE: [complete account](immigration-complete-annual-account-2026-09-20.md);
[FAQ 2](immigration-objections-faq-2026-09-21.md); [scaling decision](../decisions/2026-09-20-service-scaling-calibration.md)]

## 5. What this could not do in this object

- The ledger's dial covers G, K, P, D, F and the per-capita part of R. Base school
  current spending (−$115.8bn for the union) and public medical are not on it, so a
  CBO-type school response cannot be applied to them here. Per-function responses on the
  whole account belong to `full_account_2026_09_20` (60 service cases).
- G's composition is the national 2022 Census of Governments mix, not the union's state
  mix; the state table exists but the union's population by state does not leave the
  microdata.
- The cross-state elasticities are descriptive size gradients; the September 20 decision
  holds them as sensitivities, not identified responses. Within-state estimates are too
  imprecise to use (every interval includes 1).
- The enforcement-netted cell and the F split are computed on published vectors. The
  builder's admissibility rule and item definitions are unchanged, so `arms_matrix.csv`
  still holds 63 cells; a builder-side version would need the fingerprint rebuild ritual.

## 6. Sources

[DATA: `infra/immigration-fiscal/ledger_absolute_2026_09_17/derived/` (replicates.npz,
arms_matrix.csv, marginality_curve.csv, items_by_group.csv, audit.json, age_profiles.csv,
age_profile_components.csv); `params/params.json` OMB Historical Table 3.2 functions 050,
800, 900] [DATA: `infra/immigration-fiscal/scaling_test_2026_09_20/derived/`
state/estimates.csv, school_estimates.csv] [DATA: 2022 Census of Governments Table 1,
`ledger_residual_agg_2026_09_16/_cache/22slsstab1.xlsx`, lines 66–112]
[CALCULATION: `infra/immigration-fiscal/ledger_recut_2026_09_22/recut.py`, nine gates in
`derived/audit.json`, `test_recut.py`]

## Revisions

- 2026-09-22: created. [Decision](../decisions/2026-09-22-practitioner-hull-as-ledger-range.md):
  the practitioner hull is the ledger's reported range; the design hull and the second
  object are disclosed beside it. No published ledger value changes.
