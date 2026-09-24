**Verdict:** The operator's decisions of 2026-09-24 were built into the explorer engine and run once.
The main case is now **$200.9–246.3bn a year** of conditional net cost to other US residents, against
$203.2–249.6bn adopted on September 23: −$2.3bn at the low end and −$3.3bn at the high end.

The corrections are large and nearly cancel:
- **The group's taxes were overstated**, which moves the case **+$48.7 / +$50.3bn**.
- **Its keyed spending was overstated**, which moves it **−$51.0 / −$53.6bn**, together with the lane
  figures added (care, shelter and audit rows 8–10).

If every component sits at its extreme in the same direction, the range is **$172–276bn**. Combining
the components' spreads as independent gives about $189–260bn. No combination changes the sign.
[CALCULATION: `main_case.cjs` → `derived/main_case_bands.csv`, `derived/summary.json`; every gate
passes]

Date: 2026-09-24. Operator, on the six pending decisions: "1 ok 2 why hold? 3 ok 4 okk 5 ok 6 ok".
After the explanation of decision 2 he answered "ok". Decision record:
[`decisions/2026-09-24-main-case-audit-and-outside-checks.md`](../../../decisions/2026-09-24-main-case-audit-and-outside-checks.md).
Low end = shared allocation, high end = personal allocation, as in every published band.

## What is in it

Each change is shown alone on the September 23 case, as it enters the package; the gates first
reproduce each lane's own figure (below).

| Change | Decision | Alone, $bn (low / high) |
|---|---|---:|
| Tax records: the Census tax model's status and compliance, CPS fill-ins, Mexico-born recount, state-aware status flag (audit rows 2, 13, 4) | 1 | +19.91 / +21.21 |
| Income gradients from CBO 2022 without Medicaid, Medicare, SNAP, WIC and cash; replaces audit row 3 | 6 | +10.53 / +9.71 |
| Treasury's EITC shares, over the audit's SSN rule | 6 | −0.36 / −0.34 |
| Premium tax credits keyed as EITC (audit row 1) | 1 | −14.23 / −14.23 |
| Long-term care by use plus pooled-MEPS ethnicity ratios; replaces audit row 5 | 2 | −17.67 / −17.67 |
| Education: audit row 6 on the whole line, schools priced where the group enrolls | 1, 6 | +0.71 / −0.54 |
| Benefit keys from administrative records | 6 | +2.27 / +2.17 |
| Justice: 2024 arrests (audit row 7) and the booking correction on them | 1, 6 | +2.03 / +2.03 |
| Audit rows 8–10 and small items, shelter keying, care and household services | 1, 5, 3 | −5.06 / −5.10 |
| **Sum of the changes alone** | | **−1.87 / −2.76** |
| Interactions: the ratio corrections applied on top of the tax records | | −0.46 / −0.56 |
| **Main case** | | **200.88–246.32** |

The largest interaction is income tax. The tax records cut the group's federal income tax by 10–12%,
so CBO's gradients, which re-weight the same dollars, add $1.2bn / $1.3bn less on top of them
[DATA: `derived/components.csv`, variant `2022 unscaled`].
With the audit's own row 3 in place of CBO's gradient the case would be $196.2–243.1bn. CBO's
version adds $4.7bn / $3.2bn more [DATA: `derived/main_case_bands.csv`]. The audit's top alternative
treats the CPS fill-ins as carrying no group bias (audit row 13 at zero). On that reading the case is
$193.1–237.6bn [DATA: same file, `no_fill_in_correction`].

**The constants.** One synthetic line at response 1 carries the lane figures that share no line with
any other change:

| Item | $bn |
|---|---|
| Audit row 8: unallocable state and local spending at the all-spending elasticity | +2.0 |
| Audit row 9: MEPS donor filter | −0.8 |
| Audit row 10: foster care keyed by WIC | −1.5 |
| Audit small items | −0.1 |
| Shelter keying, mapping A at central outlays | −0.51 / −0.55 |
| Care: taxes on native women's extra hours and elder-care Medicaid savings | −4.15 |

Beside the account, not in these figures:
- the debt legacy, interest on past deficits ($30.5–38.9bn; decision 4);
- crime victims' harm ($28.9bn, $30.9bn with the crime check's mixed-group correction);
- audit rows 11 and 12, which are classification choices (0 to +7.5bn; −7.5 to −20bn);
- the social items and the scale net of the
  [real-costs memo](../../../research/immigration-real-fiscal-and-social-costs-2026-09-23.md).

## Range

Each component's spread is measured in the engine against the central package. The spreads are
summed as independent bounds at each band end, the way `dataset_integrity_2026_09_23/synthesis.py`
sums the audit's rows [DATA: `derived/components.csv`].

| Component | Variants | Low end, $bn | High end, $bn |
|---|---|---|---|
| Tax records | on-books share low/central/high × two fill-in methods | −5.9 to +6.0 | −4.9 to +5.1 |
| Income gradients | CBO 2018, 2019, 2022 data; scaled to the tax records or not | −1.9 to +2.7 | −1.9 to +2.7 |
| Medical ethnicity | six other specifications; MCBS 65+ ratio taken as the truth | −3.3 to +11.5 | −3.3 to +11.5 |
| Long-term care | extremes of the lane's 960 combinations | −1.4 to +3.0 | −1.4 to +3.0 |
| Education | row 6 weight 0.77/0.82 × school price low/high | −1.7 to +1.6 | −1.7 to +1.7 |
| Benefit keys | ±1.96 SE | −2.3 to +2.3 | −2.3 to +2.3 |
| Justice | 2023 arrests; booking in Texas only or Arizona only | −0.9 to +0.2 | −0.9 to +0.2 |
| Audit rows 9, 10, small items | their bounds | −1.7 to +1.8 | −1.7 to +1.8 |
| Shelter | outlays, served shares, mappings A–C | −0.3 to +0.1 | −0.3 to +0.1 |
| Care | envelope of the lane's specifications ($2.6–13.35bn) | −9.2 to +1.6 | −9.2 to +1.6 |
| **Main case** | | **172.3 to 231.6** | **218.8 to 276.1** |

- **Medical ethnicity is the widest spread upward.** If MCBS's 65+ ratio (1.265) is right and pooled
  MEPS (1.005 on MCBS's definitions) is wrong, the medical correction shrinks by $11.5bn. Weighting
  the two surveys by their precision moves it only $1.4bn [CALCULATION: `mcbs_bound.py` →
  `derived/mcbs_bound.json`].
- **Care is the widest spread downward.** Its lane's envelope reaches $13.35bn.

## How each change enters

- **Frame.** The adopted September 23 case is rebuilt as `outside_checks_combined_2026_09_24/combine.cjs`
  builds it: 64 specifications, justice on the `use` key, Medicaid on the two uninsured-use keys.
  With no change it reproduces $203.2070–249.6400bn to 1e-4.
- **Tax records.** These are the CPS imputation lane's stacks as line deltas, in
  `derived/stack_line_deltas.json`. That file is a vendored subset of the lane's ignored
  `_cache/onbooks_lane_line_deltas.json`, rewritten and drift-checked whenever the cache is present.
  - That lane translated on preferred keys plus the adopted justice and uncompensated-care shifts.
    Here, a shift on the Medicaid key also moves both uninsured-use keys. The stack's
    public-order population shift, which that lane scaled to the use key's per-head part, moves the
    use key.
  - Each of the six stacks alone reproduces that lane's published change to 2e-3.
- **Ratio corrections.** These rescale the group's key dollars on a line: CBO's gradients, the
  benefit keys, the medical-ethnicity ratios, and the school price and re-blend. On top of the tax
  records each is multiplied by its key's stack factor, the group's target after the stack over its
  target before.
- **Replacement corrections.** These set the group's charge on named dollars.
  - Long-term care is charged at its T-MSIS share. The stack's change on those dollars is removed,
    +$0.57bn / +$0.60bn.
  - Premium tax credits: the stack already leaves them alone.
  - Treasury's EITC share is measured against the audit's SSN rule.
- **Overlaps.** The more direct measurement wins each time:
  - CBO's income-tax gradient replaces audit row 3.
  - The administrative benefit keys replace CBO on SNAP, WIC and cash assistance (as in `combine.cjs`).
  - The pooled-MEPS ratios replace CBO's Medicare gradient (+$0.72bn dropped).
  - The booking factor multiplies audit row 7's 2024 arrest ratio (+$0.05bn).
  - Row 6's re-blended key applies to both education steps. The school price applies to the school
    step only.
- **Not resolved.** The benefits lane found up to $0.4bn of overlap with the CPS fill-ins on the
  SNAP, WIC and cash keys. The two fill-in methods run in opposite directions, and the central
  averages them.

**Gates** (exit 1 on any failure). With no change, the September 23 case reproduces. Each change
alone reproduces its lane's own figure:
- the six tax stacks;
- CBO's 2022 bundle (+10.560 / +9.444);
- Treasury's shares against the raw keys (−4.554 / −4.313);
- audit row 1 (−14.23);
- the joint medical figure at four specifications (−17.671, −13.176, −21.088, −8.648);
- audit row 6 on the whole line, and with the school price;
- the school price on the adopted key (+3.380 / +3.031);
- the benefit keys (+2.268 / +2.167);
- the booking factor (+0.869);
- audit row 7 (+1.12).

A unit synthetic line moves both ends by exactly 1, and the tax and spending sides add to the
package. The MCBS helper reproduces the pooled lane's p99.5 Medicare and Medicaid changes at k = 1.

## Limits

- **Interactions are first-order.** A ratio correction on top of the tax records is scaled by the
  group's target on that key. The exact version would re-run each lane on the stack's microdata. The
  scaling moves the package by −$0.5bn, and the unscaled income-tax row is inside the range.
- **Some audit rows are constants, not engine edits.** Rows 8, 9 and 10 come from the audit's own
  measurements or bounds, and so do care and shelter. None shares a line with another change, so
  in a linear engine they add exactly.
- **The range sums independent bounds.** It is wide by construction. The quadrature figure,
  $189–260bn, is context only.
- **Not re-run on the new case.** These were computed on September 23:
  - the service-response break-even (5.5–16.4%);
  - the back-cast;
  - the ten-year and lifetime anchors;
  - the uncertainty propagation;
  - the real-costs totals.

  The main case moved by about 1%.
- **Instrument.** An LLM assembled this (`notes/llm-bias-caveat.md`). The combining rules follow
  which measurement is more direct and were written into the script before its first run. Their
  effects run both ways:
  - scaling to the tax records, −$0.5bn net: the income-tax part −$1.2 / −1.3bn, the long-term-care
    part +$0.6bn;
  - dropping CBO's Medicare gradient, −$0.7bn;
  - dropping CBO's SNAP, WIC and cash gradients, +$0.7 / +1.0bn;
  - the booking factor on the 2024 ratio, +$0.05bn.

## Reproduce

From the repository root:

```sh
uv run --no-project python3 infra/immigration-fiscal/main_case_2026_09_24/mcbs_bound.py   # derived/mcbs_bound.json
node infra/immigration-fiscal/main_case_2026_09_24/main_case.cjs                         # all gates must pass
```

The script reads each lane's committed `derived/` files. It needs the CPS lane's ignored cache
only to refresh the vendored stacks.
