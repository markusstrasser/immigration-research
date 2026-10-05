**Verdict:** The September 27 case ($321.8–387.4bn a year) splits into four additive parts at its two ends (low / high, Shapley means). The **shared** part is $163.8 / 212.5bn: what the account's own 39.71M-person group would cost other residents at national per-capita taxes and service use. **Age structure** is −$76.9 / −42.5bn, **taxes at given ages** +$294.9 / 287.0bn and **service use at given ages** −$59.9 / −69.6bn. As shares of the case they are 51% / 55%, −24% / −11%, 92% / 74% and −19% / −18%. The group costs more than average residents only because it pays less tax at the same ages: income taxes $204 / 196bn, payroll $65 / 60bn and consumption taxes $39bn, less a production gain of $14 / 9bn. Two parts lower its cost. Its young age structure saves more on retirees than it adds in pupils. At given ages it also draws less from Social Security, Medicare, veterans' and other health programs than it draws extra from schools, cash, food and housing aid. The parts add to the case within 3e-13bn in all six orders, but the order moves the age part by up to $55bn at the low end and $86bn at the high end. A separate finding: since September 24 the corrected account is an account of 39.71M members, after audit row 4 reweighted the Mexico-born to the ACS, while the record's per-member figures for the union divide by 40.90M. Those figures run 2.9% low: the case is $8,104 / 9,754 per account member, not $7,869 / 9,472. The whole gap sits in the first generation and outside California and Texas. The generation account's first-generation figures run 9.7% low: $8,496 / 7,096 per member, not $7,673 / 6,408. [CALCULATION: `decompose.cjs` → `derived/decomposition.csv`] [FRAMING-SENSITIVE]
claude-opus-5-5

Status: proposed; the parent commits. No total changes; no other lane's file was edited.

[2026-10-05: on main case v5 (`oct05`: $390.29–461.24bn, 42.75M members), part 1 is $109.8 / 163.8bn (September 29:
$102.5 / 152.8bn). Taxes at given ages are +$255.3 / 248.3bn (+$247.7 / 242.4bn), age structure +$17.1 / 59.4bn
(+$12.9 / 48.6bn) and service use at given ages +$8.1 / −10.3bn (+$8.3 / −9.0bn), printed so that the parts add. Lower taxes at the same ages are 91% /
83% of the excess over part 1, against 92% / 86% on September 29. The 3.04M people v5 adds are placed at the identified
G3+'s ages (section "v5 case (oct05)" at the end). [CALCULATION: `decompose.cjs --case oct05|oct05_cash` →
`derived/decomposition_oct05.csv`, `derived/decomposition_oct05_cash.csv`]]

## The parts

Shapley means at the case's end specifications: 48 (shared allocation, low end) and 11 (personal allocation, high end).
Per member uses the case's denominator, 40,896,574. Per account member uses the 39,712,493 people the corrected
account charges per-head lines for (see the finding on the per-member denominator below).

| Part | $bn, low / high | $ per member | $ per account member | Share of the case |
|---|---|---|---|---|
| 1. Shared: the group's headcount at national per-capita amounts | 163.75 / 212.50 | 4,004 / 5,196 | 4,124 / 5,351 | 51% / 55% |
| 2. Age structure | −76.87 / −42.53 | −1,880 / −1,040 | −1,936 / −1,071 | −24% / −11% |
| 3. Taxes at given ages (with the production term) | +294.85 / +286.98 | 7,210 / 7,017 | 7,425 / 7,227 | 92% / 74% |
| 4. Service use at given ages | −59.92 / −69.59 | −1,465 / −1,701 | −1,509 / −1,752 | −19% / −18% |
| **The case** | **321.82 / 387.37** | **7,869 / 9,472** | **8,104 / 9,754** | 100% |

[CALCULATION: `decompose.cjs` → `derived/decomposition.csv`, `derived/summary.json` → `parts`]

The CSV's `share_of_total` is each part's share of the case's midpoint: (low + high) over
($321.82bn + $387.37bn). `share_low` and `share_high` give the share at each end.

**The order matters for parts 2 and 4.** Age interacts with both profiles. The group's elderly draw far less Social
Security and Medicare than average elderly people do. Removing retirees therefore saves more when national per-age
use is the benchmark than when the group's own use is. Taxes and use never interact, because they act on different
lines. The range over the six orders:

| Part | Low end, $bn | High end, $bn |
|---|---|---|
| Age structure | −104.6 to −49.1 | −85.4 to +0.3 |
| Taxes at given ages | 291.1 to 298.6 | 268.5 to 305.5 |
| Service use at given ages | −83.9 to −35.9 | −93.9 to −45.2 |

The age part is largest in magnitude when it is taken first, and smallest when taken last or after use. All six
orders are rows of `decomposition.csv`.

### By line

Shapley means, $bn, low / high. Each line's amount of the capital return sits with it: the K-12 return with
schools, the college return with colleges, and so on. The production term is shown on its own.

| Line group | 1. Shared | 2. Age | 3. Taxes at given ages | 4. Use at given ages | In the case |
|---|---|---|---|---|---|
| Income taxes (federal, state, other personal) | −349.0 / −349.0 | +7.4 / +26.9 | **+203.9 / +196.5** | — | −137.7 / −125.7 |
| Payroll taxes and contributions | −227.6 / −227.6 | +0.4 / +15.1 | **+65.1 / +60.1** | — | −162.1 / −152.4 |
| Consumption taxes | −141.8 / −141.8 | +5.0 / +5.0 | +39.3 / +39.3 | — | −97.5 / −97.5 |
| Production term (P + F) | 0 / 0 | +0.2 / +0.1 | −13.5 / −8.9 | — | −13.3 / −8.8 |
| Schools (with K-12 capital) | +139.5 / +142.8 | **+29.6 / +54.2** | — | +21.0 / +4.0 | +190.1 / +201.0 |
| Colleges, other education, education benefits | +20.4 / +21.6 | +0.4 / +1.3 | — | +2.9 / +2.7 | +23.7 / +25.7 |
| Medicaid (with uncompensated care) | +111.8 / +111.9 | +5.9 / +6.4 | — | −0.0 / +1.5 | +117.7 / +119.7 |
| Justice (with its capital) | +61.8 / +62.2 | +3.5 / +3.5 | — | +5.5 / +5.5 | +70.7 / +71.3 |
| Refundable tax credits | +26.8 / +26.8 | +6.0 / +0.9 | — | +3.5 / +4.9 | +36.3 / +32.6 |
| Social Security and Medicare | +300.6 / +300.6 | **−120.5 / −133.4** | — | **−70.9 / −61.2** | +109.3 / +106.0 |
| Health services and veterans | +64.8 / +65.4 | −13.0 / −14.7 | — | −19.9 / −20.8 | +31.9 / +29.8 |
| Cash, food and housing benefits | +73.9 / +73.9 | −1.1 / −6.4 | — | +12.7 / +14.6 | +85.6 / +82.1 |
| Roads and other economic affairs | +27.9 / +49.6 | −1.0 / −1.8 | — | −7.7 / −13.7 | +19.2 / +34.1 |
| Per-head government and enterprises | +55.9 / +77.4 | 0 | — | 0 | +55.9 / +77.4 |
| Care, shelter and audit constants | +1.9 / +1.9 | 0 | — | −7.1 / −7.1 | −5.2 / −5.2 |
| Other receipts | −3.1 / −3.1 | +0.2 / +0.3 | +0.1 / 0.0 | — | −2.8 / −2.8 |

[CALCULATION: `decompose.cjs` → `derived/decomposition_lines.csv`; the groups add to each part within 1e-9bn]

What the parts say, line by line:

- **Taxes at given ages are the whole excess over average residents.** The group's $158.1 / 174.9bn excess over
  part 1 is smaller than part 3. At its own ages the group pays 41% of the average resident's income taxes, 71% /
  72% of payroll taxes and 72% of consumption taxes. At national ages the figures are 41% / 40%, 72% / 73% and 71%
  (`summary.json` → `receipt_ratios`). The case's corrections contribute +$34.1 / 35.0bn of part 3: income taxes
  +$25.8 / 26.3bn, payroll +$11.0 / 11.4bn and consumption −$2.7bn. They cut the group's federal income tax by
  17.5% / 18.5% (kappa 0.825 / 0.815). The production gain offsets $13.5 / 8.9bn.
- **The young age structure lowers the cost.** At national per-age amounts, the group's few retirees save
  $120.5 / 133.4bn of Social Security and Medicare and $13.0 / 14.7bn of health and veterans' spending. Its many
  pupils add $29.6 / 54.2bn of schooling, and its age mix costs $13.0 / 47.3bn of taxes. The two ends differ because
  the shared allocation (low end) splits each household unit's taxes and costs equally among its members, so a child
  carries part of its parents' taxes and parents carry part of its schooling. The personal allocation (high end)
  leaves them with the child and the earner.
- **At given ages the group uses less, not more.** Its elderly draw far less Social Security and Medicare than
  average elderly people (−$70.9 / 61.2bn). It also draws less from veterans' and other health programs
  (−$19.9 / 20.8bn) and from roads and economic affairs, which the account keys by household resources
  (−$7.7 / 13.7bn). The case's care, shelter and audit corrections are −$7.1bn. It draws more from schools
  (+$21.0 / 4.0bn), cash, food and housing aid (+$12.7 / 14.6bn), justice (+$5.5bn), credits (+$3.5 / 4.9bn) and
  colleges (+$2.9 / 2.7bn). The school figure is large at the low end because, under the shared allocation, family
  size shows up as use at given ages. The case's corrections contribute −$48.6 / 52.2bn of part 4:
  - Social Security and Medicare −$21.9 / 23.0bn;
  - refundable credits −$16.3 / 16.6bn;
  - health and veterans −$8.0 / 7.8bn;
  - the care, shelter and audit constants −$7.1bn;
  - against justice +$2.0bn and schools +$3.9 / 0.9bn.

  [CALCULATION: `summary.json` → `sensitivities.corrections_off.*.corrections_contribution_by_group`]
- **Medicaid's excess is age, not use at given ages.** The group's Medicaid is $5.9 / 7.9bn above average residents.
  Age accounts for $5.9 / 6.4bn and use at given ages for −$0.0 / +1.5bn. The account's Medicaid key is MEPS spending by
  age band and US birth, for people with any coverage, plus the uncompensated-care arm. It has no income or
  enrollment gradient within those cells (see "Would change it").

### Part 1

Part 1 is $163.75 / 212.50bn. At national per-capita shares (11.835% of receipts, 11.718% of spending on the row-4
frame), the group would pay $716.0bn of taxes the case counts. It would draw $846.3 / 872.5bn of operating spending
at the case's responses and carry $33.4 / 56.0bn of the return on public capital. [CALCULATION: `summary.json` →
`part1_composition`]

The zero-response conventions nearly cancel in part 1. At average residents' shares, the lines held at zero response
would carry $226.1bn of receipts: corporate, property, production taxes, asset income and business transfers. They
would also carry $235.2bn of spending: defense $100.2bn, interest $131.1bn and subsidies $4.0bn. Letting both sides
respond at 1 would raise part 1 by only $9.1bn. [CALCULATION: `summary.json` → `zero_response_at_average_residents`]

## Method

**Target.** The adopted September 27 case: `corrections.json` applied to `model.json`, evaluated through
`main_case_long_run_2026_09_27/package.cjs` `evaluateFull()`. That is the engine at the specification's responses
plus the return on public capital. The ends are specification 48 (shared allocation, GDP normalization, school share
0.715, general government 0.6000, the low long-run readings, 2%) and specification 11 (personal, cash, 0.865, 0.8504,
the high readings, 3%). The case averages the two fill-in methods. Its payload is their average and the engine is
linear, so one evaluation of the payload model is the case.

**Eight states.** Each factor is either national (N) or the group's (G):
- A: the age distribution;
- R: the receipts profile by age;
- U: the service-use profile by age.

Each state is a copy of the corrected union model, with the group's amount replaced on every line the specification
evaluates. It is evaluated through `evaluateFull()`, so every capital-return component keys off the state's own line
amounts. State NNN is part 1 and state GGG is the case. Parts 2–4 are the marginal effects of switching A, R and U
from N to G, in each of the six orders and averaged (Shapley). [CALCULATION: `derived/states.csv` has all eight
states at both ends]

**Frame.** Everything is on the row-4 frame, the weights the case's stack uses. `combine_onbooks_lane.weight_arms`
arm "row4" scales Mexico-born persons outside CA+TX to their ACS 2024 cells, with factors 0.855626 (naturalized) and
0.778127 (noncitizen). The union is 39,712,493 people in a civilian household frame of 335,543,722. On this frame the
general-public-services population cell reproduces the case's corrected cell (kappa 1.0000000). Part 1 at the
published count (40.90M) is in the finding on the per-member denominator below.

**Age profiles** (`profiles.py` → `derived/age_bins.csv`). Every per-person key vector the account allocates by is
summed in 38 age bins, over the union and over the national frame, under both weight sets. The vectors are the
account's own: `generation_account_2026_09_24/frame.py` and `keys.py`, imported read-only, and through them
`cps_imputation_keys_2026_09_23/common.py`. That covers the CPS receipt and spending keys, the MEPS payer keys and the
school keys. The bins are single years 0–24, five-year bins 25–79, and the top codes 80 (80–84) and 85 (85+). For a
key with national per-person value n(b) and group per-person value g(b) in bin b:

- T_GG is the union total;
- T_GN = sum over b of n_G(b) × n(b);
- T_NG = sum over b of N_G × pi_nat(b) × g(b);
- T_NN = N_G × national per-person value.

A state's uncorrected amount is the model's uncorrected cell times the state's key share over the published share.
Every standardized line's published share reproduces model.json's stored share to its nine decimals (45 checks per
end).

**Which lines are age-standardized, and which are held.**

- *Standardized with the group's own per-age profile* (47 lines at each end). The 42 profile lines are:
  - federal and state income, other personal and motor-vehicle taxes;
  - the payroll taxes and contributions and Medicare premiums;
  - sales, excise, customs and personal transfers;
  - economic affairs, health services, education, income security, Social Security, Medicare, unemployment,
    railroad retirement, pension guaranty, veterans (four lines), workers' compensation, temporary disability and
    black lung;
  - military medical, SNAP, SSI, refundable credits, other federal benefits, family assistance, energy, WIC-keyed
    welfare, education benefits, employment and training, and rental assistance.

  Five more use special keys: justice, Medicaid and the three correction lines. The reason is the same for all
  47: each is allocated by a per-person key, so its per-age profile exists for the nation and the group alike.
- *Held at the case's corrected amount in every state* (9 per-head lines): general public services, defense,
  housing and community, recreation and culture, other state benefits, domestic interest, source rounding, asset
  income, and the enterprise surplus. Reason: a per-head key gives every person the same amount at every age, so
  these lines belong wholly to part 1. Holding them fixed also keeps the enterprise re-key consistent. The
  receipt's key is `general_public_services`' population cell (`populationShare()`, package.cjs:170-174), and
  that cell is the same in every state.
- *Held because they carry no cost* (10 lines at zero response): corporate and property taxes, production
  taxes, business transfers, and the three subsidies. Defense and interest are also zero response by the case's
  assumption. Separately, 6 external lines are zero in every state.

**Special keys.**

- *Justice* (`public_order_safety`, key `use`). The justice lane's central split is the base. Its per-head parts
  ($243.4bn national) are per head. The police-arrest half, the criminal courts, prisons and ICE interior custody
  ($275.7bn) follow the national arrest profile by age (FBI CIUS 2024 Table 38, all offenses, 6.62M arrests,
  spread within its bands by population). A group relative risk θ = 1.101 is calibrated to the case's
  administrative keyed amount, which the stack holds fixed across weight sets. This is indirect standardization.
  [DATA: `nibrs_arrests_2026_09_16/_cache/x/pa2024/CIUS_Table_38_Arrests_by_Age_2024.xlsx`]
- *Medicaid* (`uninsured_use_low` at the low end, `_high` at the high end). The key is the MEPS Medicaid key plus
  the uncompensated-care arm g × (s − k) × n (`keys.py`). The arm that sets the key is picked on the published
  union: 2013 offsets, per-head state-local, $42.67bn for the low key; 2017 offsets, health-other, $51.20bn for the
  high key. It reproduces model.json's cells to 1e-6. Each state's s and k come from that state's own key totals.
- *Correction lines* (package.cjs:250-257 keys the K-12 and college capital off them).
  - `school_reprice` scales with the group's school-key profile across ages and is 0 at national use.
  - `college_rekey` scales with the group's education-mix profile and is 0 at national use.
  - `lane_constants` splits in two. Audit row 8 ($1.90bn: unallocable state-local spending, a per-head
    response correction to general public services) is in every state, so it sits in part 1. The rest (care
    work, shelter, audit rows 9–10, small items: −$7.06 / −7.10bn) is the group's own and is 0 at national use.

**Corrections.** The case's 278 edits are measurements of the group's own amounts, so they enter only where a line's
profile is the group's. At a state with the group's profile, a line's corrected amount is kappa × the uncorrected
amount, with kappa = corrected / uncorrected at GG. In other words, each correction scales with the group's own
per-age profile. At national profile the line is uncorrected. The kappas are in `summary.json` → `lines`, and
"Would change it" gives the fixed-dollar alternative.

**Production (P + F)** goes with the receipts factor, and is 0 at national per-age earnings. That rests on an
assumption, constant returns with capital adjusting, which the case already makes; this lane adds nothing to it.

The source chain:
- The engine's P and F come from the two-skill CES model in `matched_benefits_2026_09_19/model.py`, replayed into
  the 3,888 production scenarios by `full_account_benefits_2026_09_20/builder.py` `expand_ownership`.
- The case evaluates them at the explorer's reference. `assumption_explorer_2026_09_21/build_model.py:52-54` sets
  `capital_adjustment=1.0, labor_supply_elasticity=0.0`. `engine.js:23` takes the reference, and
  `main_case_2026_09_24/package.cjs:81` changes only the normalization.
- In the model, `model.py:28` sets `power = labor_share + adjustment * (1 - labor_share)`. At adjustment 1,
  power is 1: domestic output has constant returns in labor and capital together.

So removing the same fraction of both skills' labor changes no wage and leaves no capital gain.

`production_check.py` runs the model three ways [CALCULATION: → `derived/production_check.json`]:
- A slice at the row-4 union share (0.118353 of both skills) gives exactly P = F = 0, and the transfer saving is
  also 0. Wages are unchanged, at 1.0 / 1.0.
- The positive control, the group's own skill fractions, reproduces the engine's P = −$0.236bn and F = $13.559bn at
  specification 48.
- In the failure case, with capital only half adjusting, the same slice would give P = +$73.0bn and F = −$61.0bn.

At the group's profile but national ages, the term scales with the group's earnings (wage key, ×1.032). The group's
P + F is $13.32 / 8.79bn.

## Controls

- **(a) Closure.** Part 1 plus parts 2–4 equals the case at both ends in all six orders and in the Shapley mean.
  The worst gap is 2.3e-13bn; the brief's tolerance is $0.1bn. [CALCULATION: `decompose.cjs` gate (a)]
- **(b) Reproduction.** Before any counterfactual, the corrected union reproduces $321.8194 / 387.3701bn at
  specifications 48 / 11. `corrections.json` deep-equals the package's `correctionsPayload()`. State GGG equals the
  union line by line and in cost.
- **(c) Linearity.** Twice the average residents cost exactly twice part 1: $327.5098 / 425.0040bn, to 1e-9. At
  fixed responses, nothing in the engine is non-linear. The return on public capital is linear in its key lines.
  The production term is 0 at any multiple under constant returns.

  What breaks linearity in substance is the set of responses the case computes at the group's own share
  s = 0.1202. That covers the finite-removal response of general government (r = [1 − (1 − s)^b] / s), the long-run
  road and park readings, and row 8's finite factor. At 2s:
  - general government would respond at 0.6268 instead of 0.6000 at the low end, and 0.8597 instead of 0.8504 at
    the high end, adding $2.51 / 0.88bn to the doubled part 1;
  - the long-run lines would add $0.77 / 0.14bn.

  The capital return's long-run subfunction responses and row 8's factor are not re-read [GAP].
  [CALCULATION: `summary.json` → `linearity`]

## Finding: the per-member denominator is not the account's count

**The corrected account counts 39,712,493 members; the record divides by 40,896,574.** The record's per-member
figures for the union divide totals by 40,896,574, the CPS count. Since September 24 the case's stack has included
audit row 4 ([decision](../../../decisions/2026-09-24-main-case-audit-and-outside-checks.md), decision 1). Row 4
scales the Mexico-born outside CA+TX down to their ACS 2024 cells; ladder 209 found the CPS 9–13% above the ACS every
year since 2019. That removes 1,184,081 people from the union and from the national frame. So the corrected
account, on its per-head lines and on every other key, is an account of 39,712,493 people. **The denominator that
matches the account's own count is 39,712,493.** Per-member figures on 40,896,574 run 2.9% low: multiply by 1.0298
for any total from the engine account since September 24.

| Figure | $bn a year, low / high | Per member at 40,896,574 (the record) | Per member at 39,712,493 (the account's count) |
|---|---|---|---|
| The September 27 case | 321.82 / 387.37 | $7,869 / 9,472 | $8,104 / 9,754 |
| Part 1, shared | 163.75 / 212.50 | $4,004 / 5,196 | $4,124 / 5,351 |
| Part 2, age structure | −76.87 / −42.53 | −$1,880 / −1,040 | −$1,936 / −1,071 |
| Part 3, taxes at given ages | +294.85 / +286.98 | $7,210 / 7,017 | $7,425 / 7,227 |
| Part 4, use at given ages | −59.92 / −69.59 | −$1,465 / −1,701 | −$1,509 / −1,752 |
| The INDEX's latest pairing (case plus social rows) | 416 / 491 | $10.2k / 12.0k | $10.5k / 12.4k if every row were on the account's count |

The pairing's last column is an upper reading. Only its engine part ($321.8–387.4bn) is on the row-4 count. The
social rows were built by their own lanes, whose counts this lane did not check [GAP].

**The gap sits in the first generation and outside California and Texas.** Row 4 reweights only Mexico-born people
outside those two states:

| Group | Published count | Account's count (row 4) | Multiply per-member figures by |
|---|---|---|---|
| The union | 40,896,574 | 39,712,493 | 1.0298 |
| First generation, convention (a) | 12,220,782 | 11,036,701 | 1.1073 |
| First generation, convention (b), minors with parents | 16,855,802 | 15,672,846 | 1.0755 |
| Second and third-plus generations | unchanged under (a); under (b) −602 and −522 | | 1.0000 |
| California, Texas | 13,082,782 and 9,761,462 | unchanged | 1.0000 |
| Outside California and Texas | 18,052,330 | 16,868,249 | 1.0702 |

[CALCULATION: `profiles.py` → `derived/headcount.csv`, with 2 gates; generations by the generation lane's
`frame.assignments`]

The generation account (`generation_account_2026_09_24/derived/generation_results.csv`, ladder 224) divides each
generation's corrected total by its published count. Its first-generation figures therefore run 9.7% low under
convention (a) and 7.0% low under (b):
- (a): $7,673 / 6,408 per member become $8,496 / 7,096;
- (b): $9,434 / 11,320 become $10,146 / 12,174.

The second and third-plus generations' figures stand. No ordering among the generations changes. At the low end
of (a), the first generation's shortfall against the second narrows from $1,228 to $405 per member. Regional
figures outside California and Texas run 6.6% low if their totals are on the account.

**How many record figures it touches.** `rg "per (group )?member"` finds 32 lines in 11 files of `research/` and
`decisions/`. Once lane RESULTs are counted, it finds 112 lines in 34 files; those were not classified. Read one by
one, the 32 lines fall into six kinds:

| Kind | Lines | Effect of the account's count |
|---|---|---|
| The union's cost per member on the September 24 case or a later one, or on a pairing built on one | 19 | 2.9% low on the engine part |
| The generation table (`immigration-adopted-account-by-generation-2026-09-25.md:108`) | 1, plus its rows | First generation 9.7% low; the others stand |
| Per member of other lanes' own totals: victimisation $707, skill production $341, PM2.5 $1,704, disease $7 | 4 | Depends on each lane's count [GAP] |
| Per member within households (ladder entry 268) | 1 | Depends on the distribution lane's weights [GAP] |
| The September 20 figure, from before row 4 (`immigration-real-fiscal-and-social-costs-2026-09-23.md:393`) | 1 | None: that case used the published weights |
| Prose, percentages, a California figure, the Black comparator | 6 | None, except a per-member comparison with the union |

The 19 lines:
- `immigration-INDEX.md` 221 and 223;
- `immigration-real-fiscal-and-social-costs-2026-09-23.md` 31, 39, 48, 67, 94, 109 and 387;
- `immigration-confidence-ladder.md` 317 (entry 219's figure), 321, 345 and 441;
- the decision records `2026-09-28-social-items-more-benefits.md:61`, `2026-09-28-social-items-scale-benefits.md:63`
  and `:69`, `2026-09-28-social-items-pollution-crashes.md:86`, `2026-09-28-social-items-fear-security-schools.md:59`
  and `2026-09-29-crash-item-with-against-without.md:65`.

The Black comparator's "1.5–1.7×" stands as a ratio of totals. Read per member, it becomes 1.46–1.62×.
[INFERENCE: each line read against the date of its case]

**Arithmetic, with the lines it is read from.** This corrects one figure from the lane's first message to the lead:
0.11718 is not 39.712M / 335.54M. The published cell (`assumption_explorer_2026_09_21/derived/model.json`, `general_public_services`
→ `keys.population.personal`) stores `"share": 0.121452918`. That is 40,896,574 / 336,727,803, the union over the
CPS civilian household frame. Its `"target_bn": 48.291269414` of `national_bn` 401.608 is 0.120245 of the line. A
spending cell's target is national × household fraction × share:

```
full_account_spending_2026_09_20/builder.py:267-270:  household=amount*household_fraction ... target=... household*share
cps_imputation_keys_2026_09_23/translate.py:162-166:  household_fraction(d): W[civ].sum(axis=0) / c.RESIDENT
cps_imputation_keys_2026_09_23/translate.py:203:      hf = household_fraction(c.load_frame())   (published weights, held under row 4)
```

- The household fraction is hf = 336,727,803 / 340,110,988 = 0.990053. The stack keeps it at its published value.
- In the corrected cell (`corrections.json` applied), `share` is 0.118352664 = 39,712,493 / 335,543,722. That is
  the key share, the lead's 0.11835. The cell's target is 47.058568, which is **0.117175 of the line**
  = hf × 0.118353.
- So 0.11718 is the cell's share of the national line, after the household fraction. The frame that turns it into
  39.712M is **338,915,010** = 335,543,722 / 0.990053. That is the 340,110,988 US residents less the 1,184,081
  removed people grossed up by 1 / hf (1,195,978).
- The first message paired 0.11718 with 335.54M, which was wrong: 0.11718 × 335.54M = 39.32M. The RESULT uses
  0.117175 only as the share of each spending line and 0.118353 for receipts, which carry no household fraction.

[DATA: `model.json` and the corrected union, read in `decompose.cjs`; CALCULATION: `derived/summary.json` → `frame`]

**Part 1 and the count.** Part 1 uses the account's own count, so parts 2–4 carry no headcount term. At the
published count, 40.90M average residents on the published frame, part 1 would be **$168.0 / 218.0bn**
(+$4.24 / 5.52bn), and that difference would otherwise surface as false age, tax and use effects.
[CALCULATION: `summary.json` → `sensitivities.part1_at_published_count`] [FRAMING-SENSITIVE]

## Would change it (disconfirmation)

What would make a part mislabelled, and how far each measured alternative moves it:

- **Corrections as fixed dollars instead of scaling with the profile.** Age moves to −$83.7 / −49.9bn, use to
  −$52.8 / −60.7bn and taxes to +$294.6 / 285.5bn. About $7bn moves between parts 2 and 4 at each end. If a
  correction is concentrated at certain ages (the credits' SSN rule hits working-age parents), neither rule is
  exact. [CALCULATION: `summary.json` → `sensitivities.corrections_fixed_dollars`]
- **The case's corrections by part.** They contribute +$6.9 / 7.5bn to part 2, +$34.1 / 35.0bn to part 3 and
  −$48.6 / 52.2bn to part 4. Without them part 4 would be −$11.3 / 17.4bn.

  The national per-age profiles are the raw CPS and MEPS keys; national totals are fixed. The CBO income gradient,
  for example, corrects the group's share, not the national age gradient. If the CPS misstates how taxes rise with
  age nationally, part of part 3 is age structure. [CALCULATION: `sensitivities.corrections_off`]
- **The justice age profile.** A flat 18–64 profile, the key's own base, instead of arrests moves age to
  −$79.1 / −44.8bn and use to −$57.6 / −67.3bn, a $2.3bn shift. The arrest profile also stands in for custody, which
  peaks later (25–44). [CALCULATION: `sensitivities.justice_flat_18_64`]
- **The allocation convention.** The parts mean different things at the two ends. Under the shared allocation (low
  end), family size shows up as taxes and use at given ages. Schools' age part is $29.6bn there against $54.2bn
  under the personal allocation, and their use part $21.0bn against $4.0bn. Compare parts across ends only with
  this in mind. [FRAMING-SENSITIVE]
- **Medicaid's key.** The case's Medicaid key is MEPS spending by age band and US birth, times any coverage, plus
  the uncompensated-care arm. The pooled medical-ethnicity correction is the only adjustment within cells. The
  group is 19.6% of CPS Medicaid enrollees (model.json `medicaid_covered`) but carries 12.3–12.5% of the line's
  dollars. A key with an income or enrollment gradient within age would move dollars into part 4 and raise the
  total. [INFERENCE; the account's key choice, not this lane's]
- **Roads keyed by household resources.** Economic affairs is keyed by SPM resources, which charges the group 8.06%
  of the line against 11.72% of residents, 31% less per head. The crash lane measured that the group drives 11%
  fewer miles per person than the average resident (`road_crash_externality_2026_09_28/RESULT.md`). A mileage key
  for the road part would make part 4 less negative by a few $bn. [INFERENCE; not computed]
- **Capital-income and property taxes at zero response.** If they responded, part 1 would fall by $226.1bn. Parts 2
  and 3 would rise by $128.0 / 135.7bn, the gap between average residents' amounts and the group's. Defense and
  interest at average cost would add $235.2bn to part 1 and nothing to parts 2–4, since they are per head.
  [CALCULATION: `zero_response_at_average_residents`; the parts split is [INFERENCE]]
- **The production term.** Attaching it to receipts puts $13.5 / 8.9bn in part 3. If the production gain came from
  the group's age rather than its skills, some would belong in part 2. Its Shapley age share here is only
  +$0.2 / 0.1bn.
- **Sampling.** The profiles use the full-sample weight only. No replicate standard errors [GAP]. The group's 85+
  bin is thin, and the part-4 Social Security and Medicare line rests on the group's per-capita values at 65+.

## Files

Written (this lane only):
- `profiles.py` builds the age profiles and the headcount by generation and region, with 5 gates.
- `decompose.cjs` builds the states, orders, Shapley means and controls, with 28 gates.
- `production_check.py` runs the CES model on a proportional slice, with 3 gates. It writes
  `derived/production_check.json`.
- `derived/age_bins.csv` (6,764 rows), `derived/arrest_profile.csv` and `derived/headcount.csv`.
- `derived/decomposition.csv`, the brief's columns plus `share_low` and `share_high`.
- `derived/decomposition_lines.csv`, `derived/states.csv` and `derived/summary.json`.

Read, not edited:
- `main_case_long_run_2026_09_27`: `package.cjs` (and the chain it imports), `corrections.json` and `summary.json`.
- `assumption_explorer_2026_09_21/engine.js` and `model.json`.
- `generation_account_2026_09_24`: `frame.py`, `keys.py` and `generation_keys.csv` (gate).
- `cps_imputation_keys_2026_09_23`: `common.py` and `combine_onbooks_lane.py` (the row-4 weights).
- `cj_use_allocation_2026_09_23/derived/central_split.csv` and `summary.json`.
- `uncompensated_care_2026_09_23/derived/summary.json`.
- `finite_response_2026_09_26/derived/r_values.json` and `service_response_long_run_2026_09_27/derived/responses.json`.
- The CIUS 2024 Table 38 workbook, and `road_crash_externality_2026_09_28/RESULT.md` (one figure).
- `matched_benefits_2026_09_19`: `model.py`, and in `derived/`, `skill_composition.csv` and `audit.json` (the
  production check).
- `full_account_spending_2026_09_20/builder.py:264-270` and `cps_imputation_keys_2026_09_23/translate.py:162-166, 203`
  (the household fraction).
- `generation_account_2026_09_24`: `frame.py` `assignments()` (the generations) and
  `derived/generation_results.csv` (its per-member figures).
- Record counts: `research/` and `decisions/`, read with `rg`; each of the 32 lines read in context, and
  `decisions/2026-09-24-main-case-audit-and-outside-checks.md` for the date row 4 entered the case.

Skipped, with the reason:
- Replicate-weight SEs: not asked for; about 1M more bin rows [GAP].
- The generation lane's per-generation correction rules (`correction_rules.py`, `run_generations.cjs`): this split is
  by age and profile, not generation. Its key machinery is reused and its splits are not needed.
- A re-read of the capital return's long-run subfunctions and of row 8 at 2s for control (c) [GAP; about $0.1–0.5bn].

## Reproduce

```sh
# from the repository root
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/main_case_decomposition_2026_09_29/profiles.py
node infra/immigration-fiscal/main_case_decomposition_2026_09_29/decompose.cjs   # --out-dir DIR to write elsewhere
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/main_case_decomposition_2026_09_29/production_check.py
```

`profiles.py` needs the pinned ASEC zip (via the generation lane's cached frame), the MEPS 2024 file, the IPUMS and
PUMS extracts that row 4 reads, and the CIUS workbook. All are local and ignored. All three scripts exit 1 on a
failed gate. Two runs gave byte-identical outputs (`diff -r` over `derived/`).

## Log

- 2026-09-29 00:21 JST — stub written; reading main case, engine and generation lane.
- 2026-09-29 00:36 JST — profiles.py passes: 86 key totals reproduce generation_keys.csv (2.2e-16); row-4 union 39.712493M of a 335.543722M frame (published 40.896574M / 336.727803M). Finding to carry: the corrected account charges per-head lines for 39.71M people, the per-member convention divides by 40.90M.
- 2026-09-29 00:49 JST — decompose.cjs passes all gates (a, b, c, key-share reproduction, GGG = union, group sums); rerun of profiles.py and decompose.cjs byte-identical (diff -r). Drafting RESULT.
- 2026-09-29 00:56 JST — added receipt ratios and the corrections' split by line group; final rerun of both scripts byte-identical (diff -r), 28 + 3 gates pass. RESULT final.
- 2026-09-29 01:12 JST — the lead's three additions: the per-member finding (both denominators, record lines classified, first generation 9.7% low via the new `derived/headcount.csv`), the arithmetic corrected with its source lines (0.117175 is the cell share after hf; the key share is 0.118353; frame 338,915,010), and the production term stated as an assumption with its source and `production_check.py` (3 gates). All three scripts rerun: rc 0, 36 gates pass, `derived/` byte-identical (diff -r); earlier outputs unchanged.

## Lead verification (2026-09-29 00:59 JST)

- Reran both scripts in place with `scripts/rerun_lane.py`: rc 0, 9 of 9 files byte-identical.
- The per-head share divides the union by the US resident population, not the household frame: 39,712,493 / 0.117176 = 338.91M and 40,896,574 / 0.120245 = 340.11M. The second matches Census's July 2024 resident population (340,110,988). The lane's early message quoting a 335.54M denominator was loose wording; the code reproduces the case's cell exactly.
- Part 1's composition checks by hand: 846.3 + 33.4 − 716.0 = 163.7 at the low end; 872.5 + 56.0 − 716.0 = 212.5 at the high end.


claude-opus-5-5

## v4 case (sept29), 2026-09-29

**Verdict:** On the adopted v4 case ($371.4146–434.8410bn at specifications 48 / 11), 39.71M average residents would
cost other residents **$102.49 / 152.76bn** under the case's own rules, pension accrual included. The group's excess
over them is **$268.92 / 282.08bn**. It splits into taxes at given ages **+$247.68 / 242.43bn**, age structure
**+$12.96 / 48.62bn** and service use at given ages **+$8.28 / −8.97bn** (Shapley means, low / high end).

"All of the excess comes from lower taxes at the same ages" no longer holds on the accrual central. Those taxes are 92% /
86% of the excess, and the group's young age mix now adds to its cost instead of lowering it. The statement still holds
in the cash set ($294.70–361.82bn), where taxes at given ages are 171% / 150% of a $175.16 / 193.54bn excess.

The accrual lands on both ages and rates. Against the cash set, the pension switch adds $86.0 / 87.3bn to the age part
and $59.2 / 49.7bn to use at given ages. It takes $51.5 / 48.5bn from taxes at given ages and $17.0 / 15.5bn from part 1.
The reason is how accrual charges pensions. Social Security and Part A are charged as the pensions this year's work
earns, so they follow the payroll taxes of people of working age, not the benefits of retirees. The group's few retirees
therefore stop lowering its cost, and its lower payroll taxes at given ages now also earn smaller pensions.
[CALCULATION: `decompose.cjs --case sept29` and `--case sept29_cash` → `derived/*_sept29.*`, `derived/*_sept29_cash.*`]
[FRAMING-SENSITIVE]

Status: proposed; the lead commits. The run was resumed after the reboot at about 20:51 JST, and every gate below was
rerun after it.

### The parts

Shapley means at the case's end specifications 48 (low) and 11 (high). Per account member divides by the 39,712,493
people the account prices (the row-4 union; this lane's finding above, which the v4 decision adopts). The September 27
files keep the record's 40,896,574, as written.

| Part | $bn, low / high | $ per account member | Share of the case | Cash set, $bn | September 27, $bn |
|---|---|---|---|---|---|
| 1. Shared | 102.49 / 152.76 | 2,581 / 3,847 | 28% / 35% | 119.54 / 168.28 | 163.76 / 212.50 |
| 2. Age structure | 12.96 / 48.62 | 326 / 1,224 | 3% / 11% | −73.08 / −38.66 | −76.87 / −42.53 |
| 3. Taxes at given ages (with the production term) | 247.68 / 242.43 | 6,237 / 6,105 | 67% / 56% | 299.21 / 290.88 | 294.85 / 286.98 |
| 4. Service use at given ages | 8.28 / −8.97 | 209 / −226 | 2% / −2% | −50.97 / −58.68 | −59.92 / −69.58 |
| **The case** | **371.41 / 434.84** | **9,353 / 10,950** | 100% | 294.70 / 361.82 | 321.82 / 387.37 |

[CALCULATION: `derived/decomposition_sept29.csv`, `decomposition_sept29_cash.csv`, `decomposition.csv`; printed by
largest remainder so each column adds. The September 27 column prints 163.76 and −69.58 where the section above
prints 163.75 and −69.59. Those parts add to 321.81 / 387.36, not to the case.]

**Part 1 on v4.** At national per-capita shares, the group would pay $749.2bn of the taxes the case counts, draw
$818.3 / 846.0bn of operating spending and carry $33.4 / 56.0bn of the return on public capital (`summary_sept29.json`
→ `part1_composition`). Part 1 is $44.2bn below September 27's even in the cash set. Item 5 now counts the property
taxes that average residents would pay: property taxes are $44.2bn of part 1 (table below). The pension switch lowers
part 1 by a further $17.0 / 15.5bn. At national ages, Social Security accrues $149.3bn for 39.7M people, against the
$169.7bn of benefits they would draw. The same people's Medicare Part A accrual is $7.1 / 5.6bn below their Part A
benefits. The tax on current benefits, which the accrual's net ratio already counts, leaves the receipts: +$10.4bn.

**The lines held at zero response** would now carry $167.9bn of receipts at average residents' shares, against
$226.1bn on September 27, because item 5 makes property taxes respond. The spending side is unchanged at $235.2bn.
Letting both respond at 1 would raise part 1 by $67.3bn (September 27: $9.1bn). [CALCULATION: `summary_sept29.json`
→ `zero_response_at_average_residents`]

**The order matters**, as on September 27 (six orders, `decomposition_sept29.csv`):

| Part | Low end, $bn | High end, $bn |
|---|---|---|
| Age structure | 2.9 to 23.1 | 26.3 to 70.9 |
| Taxes at given ages | 242.8 to 252.6 | 226.4 to 258.5 |
| Service use at given ages | 3.1 to 13.5 | −15.2 to −2.7 |

The age part is positive in every order at both ends. So is the conclusion below: in every order, taxes at given ages
fall short of the excess.

### Where the pension accrual lands

The pension switch by part is the v4 case less its cash set. The two differ in this one option only, and no other line
moves (largest other change 9.1e-10bn). Figures are $bn, low / high:

| Line | 1. Shared | 2. Age | 3. Taxes at given ages | 4. Use at given ages | Change |
|---|---|---|---|---|---|
| Social Security (accrual for benefits) | −20.3 / −20.3 | 65.6 / 69.1 | −44.7 / −42.1 | 52.5 / 43.0 | 53.1 / 49.7 |
| Medicare (Part A accrual for Part A benefits) | −7.1 / −5.6 | 23.6 / 21.9 | −1.7 / −1.5 | 6.7 / 6.7 | 21.5 / 21.5 |
| Federal income tax (less the tax on current benefits) | 10.4 / 10.4 | −3.2 / −3.7 | −5.1 / −4.9 | 0.0 / 0.0 | 2.1 / 1.8 |
| **The pension switch** | **−17.0 / −15.5** | **86.0 / 87.3** | **−51.5 / −48.5** | **59.2 / 49.7** | **76.7 / 73.0** |

[CALCULATION: `summary_sept29.json` and `summary_sept29_cash.json` → `v4.line_parts`; one decimal, controlled rounding
so that rows and columns add]

Why each line moves as it does:

- **Social Security.** In the cash set, the group's few retirees save $60.8 / 73.6bn (age). Its retirees also draw less
  than average retirees, which saves another $52.6 / 43.1bn (use). On accrual, the line is the payload's own rule, 0.974
  (`ratio_net`) × the OASDI taxes the members pay, read at each state's ages and tax profile.
  - Its age part is +$4.8 / −4.4bn. The group's age mix holds about as many payroll taxpayers per member as the nation's:
    it has more children than the nation and fewer retirees, and neither group pays payroll tax.
  - Its tax part is −$44.7 / 42.1bn. The group pays 70% / 72% of average OASDI taxes at given ages, so it also accrues
    70% / 72% of average pensions.
  - Nothing is left for use at given ages.
- **Medicare.** The line keeps −$35.4 / 37.1bn of age and −$11.1bn of use in the accrual case, from Parts B and D, which
  stay on cash. The Part A accrual follows covered workers, so its tax part is only −$1.7 / 1.5bn.
- **Federal income tax.** The case drops the tax on current benefits from receipts, because the accrual's net ratio
  already counts the tax on future benefits. That removes $10.4bn at average residents and $8.3 / 8.6bn less for the
  group, which pays less of that tax at its ages and rates.

Read on its own, the accrual sits in part 1 and in taxes at given ages, with almost nothing on ages. Social Security's
accrual is $149.3bn in part 1, +$4.8 / −4.4bn in age and −$44.7 / 42.1bn in taxes at given ages (`v4.line_parts`). The
switch from cash moves the age and use parts because it removes the benefits that the cash view charges to retirees.

### Does all the excess still come from lower taxes at the same ages?

| Case | Excess over part 1, $bn | Taxes at given ages | Age structure | Use at given ages |
|---|---|---|---|---|
| v4 (accrual) | 268.92 / 282.08 | 247.68 / 242.43 (92% / 86%) | 12.96 / 48.62 (5% / 17%) | 8.28 / −8.97 (3% / −3%) |
| Cash set | 175.16 / 193.54 | 299.21 / 290.88 (171% / 150%) | −73.08 / −38.66 (−42% / −20%) | −50.97 / −58.68 (−29% / −30%) |
| September 27 | 158.06 / 174.87 | 294.85 / 286.98 (187% / 164%) | −76.87 / −42.53 (−49% / −24%) | −59.92 / −69.58 (−38% / −40%) |

**No, not on the accrual central.** Most of the excess, 86–92%, still comes from lower taxes at the same ages, and they
remain the largest part at both ends. The age mix now adds $13.0 / 48.6bn (5% / 17%): schools add $29.6 / 54.2bn, and
Social Security's age saving is gone. Use at given ages adds 3% / −3%. The result holds under every alternative rule
below: taxes at given ages are 85–93% of the excess in each. In the cash set, the September 27 reading stands. There,
taxes at given ages exceed the whole excess, because the age mix and use at given ages lower the cost.

### By line

Shapley means, $bn, low / high:

| Line group | 1. Shared | 2. Age | 3. Taxes at given ages | 4. Use at given ages | In the case |
|---|---|---|---|---|---|
| Income taxes (federal, state, other personal) | −338.6 / −338.7 | 4.3 / 23.3 | 195.8 / 188.8 | — | −138.5 / −126.6 |
| Payroll taxes and contributions | −227.6 / −227.6 | 0.3 / 15.0 | 65.9 / 60.9 | — | −161.4 / −151.7 |
| Consumption taxes | −141.8 / −141.8 | 5.2 / 5.2 | 31.5 / 31.5 | — | −105.1 / −105.1 |
| Property taxes (item 5's three lines) | −44.2 / −44.2 | 3.8 / 3.8 | 13.2 / 13.2 | — | −27.2 / −27.2 |
| Production term (P + F) | — | 0.2 / 0.1 | −11.9 / −7.8 | — | −11.7 / −7.7 |
| Other receipts | −3.1 / −3.1 | 0.2 / 0.4 | −0.4 / −0.6 | — | −3.3 / −3.3 |
| Schools (with K-12 capital) | 139.5 / 142.8 | 29.6 / 54.2 | — | 21.0 / 4.0 | 190.1 / 201.0 |
| Colleges, other education, education benefits | 20.4 / 21.6 | 0.4 / 1.3 | — | 2.9 / 2.7 | 23.7 / 25.6 |
| Medicaid (with uncompensated care) | 111.8 / 111.8 | 5.9 / 6.4 | — | 0.0 / 1.5 | 117.7 / 119.7 |
| Justice (with its capital and state price) | 61.7 / 62.2 | 3.6 / 3.7 | — | 11.8 / 11.8 | 77.1 / 77.7 |
| Refundable tax credits | 26.8 / 26.8 | 6.0 / 0.9 | — | 3.5 / 4.9 | 36.3 / 32.6 |
| Social Security and Medicare | 273.2 / 274.7 | −31.3 / −42.4 | −46.4 / −43.6 | −11.6 / −11.5 | 183.9 / 177.2 |
| Health services and veterans (with state price) | 64.8 / 65.4 | −13.3 / −15.1 | — | −17.8 / −18.7 | 33.7 / 31.6 |
| Cash, food and housing benefits (with public housing's deficit) | 78.6 / 78.7 | −1.0 / −6.4 | — | 10.1 / 12.1 | 87.7 / 84.4 |
| Roads and other economic affairs (with the miles lines) | 27.9 / 49.6 | −1.0 / −1.8 | — | −4.5 / −8.6 | 22.4 / 39.2 |
| Per-head government and enterprises | 51.2 / 72.7 | 0.0 / 0.0 | — | 0.0 / −0.1 | 51.2 / 72.6 |
| Care, shelter and audit constants | 1.9 / 1.9 | — | — | −7.1 / −7.1 | −5.2 / −5.2 |
| **Total** | **102.5 / 152.8** | **12.9 / 48.6** | **247.7 / 242.4** | **8.3 / −9.0** | **371.4 / 434.8** |

[CALCULATION: `derived/decomposition_lines_sept29.csv`. The groups add to each part within 2.6e-13bn. The table is
printed at one decimal with controlled rounding: the totals row is the parts rounded by largest remainder, and 5 / 8
cells sit 0.1 off their nearest rounding, so that every row and column adds. The age total prints 12.9 for 12.96.]

v4's new lines sit with their parents: the state-price lines with justice, health and recreation, the miles lines with
roads, public housing's deficit with housing benefits. The cash set's table (`decomposition_lines_sept29_cash.csv`)
differs only in the Social Security and Medicare row and in income taxes, by the amounts in the pension table above.
Against September 27, three v4 items change the parts line by line:
- **State prices** add $8.7 / 8.8bn to use at given ages (justice +$6.3bn, health +$2.1bn, recreation +$0.4bn), plus
  small age terms. The group lives where public services cost more, and at national use the price index is 1.
- **Roads.** Their use part is −$4.5 / 8.6bn against −$7.7 / 13.7bn on September 27; the miles lines add $2.3 / 3.1bn
  of the change. The September 27 section expected a mileage key to move it this way.
- **Receipts' rate parts.** Income taxes' part moves from +$203.9 / 196.5bn to +$200.9 / 193.6bn in the cash set (item
  3's IRS key raises the group's federal income tax). Consumption taxes' part moves from +$39.3bn to +$31.5bn. Several
  items touch those lines (state prices on sales taxes, miles on fuel taxes, 6a's sales rule), and this lane does not
  split them.

### Rules designed for v4

Every rule applies only to v4's payload. A September 27 payload has no receipt lines, national scales, accrual or new
correction lines, and its outputs are unchanged (gate 1).

| Line(s) | Rule used | Why | Alternative beside | Its effect, $bn low / high |
|---|---|---|---|---|
| `social_security` (accrual) | 0.974 (`ratio_net`) × the OASDI receipts at the state's ages and tax profile (factors A and R, never U) | the payload's own rule, read at every state: the accrual is earned by the tax paid | the national money's worth at national per-age taxes, 0.901 [INFERENCE: a bridge from the group's gross 1.018 by the pension lane's national-to-group ratio on scheduled benefits at trust-fund rates, 1.237 / 1.281, net of the national 8.4% of future benefits taxed, against the group's 4.4%] | part 1 −11.2 / −11.2; taxes +11.4 / +11.0; taxes are then 92.5% / 86.4% of the excess |
| `medicare` | Parts B and D (1 − the Part A share) on the Medicare key at (A, U), with the line's correction ratio; the Part A accrual ($41.1bn) × covered workers (`positive_fica_worker` key) at (A, R) over GG | Part A turns on insured status (40 covered quarters), not on the tax paid | the Part A accrual scaled by the group's HI receipts | part 1 +19.4 / +22.4; taxes −19.7 / −20.4; age +0.3 / −2.0 |
| `federal_income_tax` | its key at (A, R), corrected on the cash amount (the case + the benefit tax), less the tax on current benefits on the Social Security benefit key: the payload's $2.09 / 1.82bn at R = G, the pension lane's national rate (`current_rate_nation`) on the national line at R = N | the payload removes the tax on current benefits because the net ratio counts the tax on future benefits | the group's rate at every state | at most the line's move in the pension table, $10.4bn between part 1 and parts 2–3 |
| `modeled_owner_property` | the account's CPS key (`keys.py` `owner_property`) under both weight sets (`profiles_sept29.py`) | the line's own key, which reproduces model.json's cell (1e-6) | none needed | see the finding below |
| `tenant_occupied_property`, `personal_property_tax` | ACS 2024 contract rent and household vehicles per person by age: household amounts shared per member, the group as HISP 02 or POBP 303, as the receipt-side lane builds its shares. Each is times the CPS frame's headcount by age, and a correction ratio (0.980, 0.980) carries the measured share over the standardized one | the CPS has neither rent nor vehicles; the receipt-side lane keys both on the ACS | per head, all in part 1 | their age and rate parts are −0.2 / +0.5 and +0.1 / +0.1: any rule moves under $0.5bn |
| `housing_enterprise_surplus` | its national over `housing_subsidies`' × that line's amount at (A, U) | item 1 keys public housing's deficit at the tenant key, the rental line's | per head | its age and use parts, −0.1 and −1.9, would move to part 1 |
| `state_price_*` (3 lines) | the parent line's amount at (A, U = G) × the line's ratio to its parent at GG; 0 at U = N | the price where the group lives is the group's own; at national use the index is 1 | none computed | +8.7 / +8.8 in use; −0.1 / −0.1 in age |
| `roads_vmt_sl`, `roads_vmt_fed` | the case's amount × the group's persons aged 5+ at national ages over its own at A = N; 0 at U = N | the roads lane prices miles per person aged 5+ and has no age profile of miles | none computed | +2.3 / +3.1 in use; −0.03 / −0.04 in age |
| National-scale edits (3 lines) | a scaled line's uncorrected cell is model.json's × the payload's national over model.json's | national per-age amounts must add to the national line the case uses | none: the only consistent reading | exact (the key-share gates pass on every line) |
| Per member | 39,712,493 (row-4 union) | the account's count (the finding above) | 40,896,574 | × 0.971 |
| Sensitivities | no corrections-off run on v4; the accrual's two alternatives instead | v4's edits carry the items and the accrual, which reads the corrected receipts, and not only dataset corrections. The cash set is decomposed as its own case | — | — |

### Would change it

| Rule | 1. Shared | 2. Age | 3. Taxes | 4. Use | The case |
|---|---|---|---|---|---|
| Central (this section) | 102.5 / 152.8 | 12.9 / 48.6 | 247.7 / 242.4 | 8.3 / −9.0 | 371.4 / 434.8 |
| National money's worth at national per-age taxes (0.901 for 0.974) | 91.3 / 141.6 | 12.7 / 48.8 | 259.1 / 253.4 | 8.3 / −9.0 | 371.4 / 434.8 |
| Part A accrual scaled by HI receipts instead of covered workers | 121.9 / 175.1 | 13.3 / 46.7 | 227.9 / 222.0 | 8.3 / −9.0 | 371.4 / 434.8 |
| Justice profile flat over 18–64 | 102.5 / 152.8 | 10.6 / 46.2 | 247.7 / 242.4 | 10.6 / −6.6 | 371.4 / 434.8 |
| Corrections as fixed dollars | 102.5 / 152.8 | 9.6 / 45.3 | 247.6 / 241.4 | 11.7 / −4.7 | 371.4 / 434.8 |

[CALCULATION: `summary_sept29.json` → `sensitivities`; each row printed by largest remainder so that it adds]

- **The money's-worth ratio at national profile** decides how much of the ratio gap sits in part 1. The central gives
  average residents the group's 0.974. The bridge gives them 0.901. The national ratio on the central's basis (payable
  benefits) is not measured. The bridge assumes the payable cut falls alike on the nation and on the younger group,
  which probably understates the nation's ratio. On a like-for-like basis the nation's ratio is 3.5% below the group's,
  and more of its future benefits are taxed. If the nation's ratio lies between the two rules, part 1 lies at
  $91.3–102.5bn at the low end [INFERENCE]. The pension lane measured ratios by generation (G1 1.041, G2 0.919, G3+
  0.962; the generation lane uses them), not for the nation.
- **The accrual's age profile.** Every state's accrual is its OASDI receipts × one ratio, so a tax dollar earns the
  same pension at every age. A ratio by age would move dollars between parts 2 and 3 [GAP: no per-age ratio in the
  pension lane's outputs].
- **Part 1 at the published count** (40.90M on the published frame) would be $103.97 / 155.17bn (+$1.47 / 2.41bn;
  September 27: +$4.24 / 5.52bn).
- **Finding: item 5's owner-occupied property tax is on the published weights, not the row-4 frame.** The case's group
  amount for `modeled_owner_property`, $24.970bn, is model.json's published cell (share 0.063237). On the row-4 frame
  that the rest of the account uses, the key gives 0.062121 of the same national line (correction ratio 1.01798). The
  line was at zero response on September 27, so row 4 never needed to move it. Item 5 now makes it respond at 0.763. Put
  on row 4, the case rises by $0.34bn at both ends ($371.75 / 435.18bn). [CALCULATION: engine run, `summary_sept29.json`
  → `v4.kappas`] The fix belongs to the adopted lane's payload and was not made here.

### Controls and gates

`decompose.cjs` gates (exit 1 on any failure): sept29 35 PASS, sept29_cash 29 PASS, sept27 28 PASS (unchanged).
- (b) the oracle: the corrected union reproduces $371.4146 / 434.8410bn (relative 1e-12, the lane's tolerance), and the
  cash set $294.7011 / 361.8175bn. The ends are specifications 48 / 11. The payload equals the package's
  `correctionsPayload()`.
- Pension inputs:
  - `pension_accrual_2026_09_28/derived/summary.json` has the payload's pinned sha256 (9ea1beb).
  - `ratio_net` is the central's gross ratio × (1 − the group's future share taxed), to 1e-12.
- The accrual rules reproduce the case's Social Security, Medicare and federal income tax at GGG (1e-9). Public
  housing's deficit reproduces too (1e-9).
- Key shares reproduce model.json's uncorrected cells: 50 checks per end, 47 in the cash set.
- State GGG is the union line by line; per-head lines' correction ratios are 1; the line groups add (2.6e-13).
- (a) Parts 1–4 add to the case in all six orders and the Shapley mean (worst 1.7e-13).
- (c) Twice the average residents cost exactly twice part 1 ($204.99 / 305.51bn).

The brief's gates:
1. **Old case unchanged:** `scripts/rerun_lane.py --allow-unrun profiles_sept29.py` with the September 27 commands
   (`profiles.py`, `decompose.cjs`, `production_check.py`) gave IDENTICAL, 23/23 files, rc 0 (21:03 JST). `git diff
   --quiet` on `derived/` gave rc 0: the tracked outputs are HEAD's bytes.
2. **sept29 outputs:** the ten new files exist (eight decomposition outputs, two profile files), and the lane's gates
   pass on both cases (35 and 29).
3. **Oracle:** gate (b), above.
4. **Two passes** of `rerun_lane.py` with all six commands, after the sept29 run, gave IDENTICAL, 23/23 files, rc 0
   (21:03 and 21:03 JST).

### Files

Written (this lane only):
- `decompose.cjs` (modified): `--case sept29 | sept29_cash`. The September 27 default and its four outputs are
  unchanged.
- `profiles_sept29.py` (new, 5 gates): the three property keys by age → `derived/age_bins_sept29.csv`,
  `derived/acs_rates_sept29.csv`.
- New outputs: `derived/decomposition_sept29.csv`, `decomposition_lines_sept29.csv`, `states_sept29.csv`,
  `summary_sept29.json`, and the same four with `_sept29_cash`.

Read, not edited:
- `main_case_2026_09_29`: `package.cjs`, `corrections.json` and `summary.json`.
- `main_case_candidate_v4_2026_09_29/derived/corrections_v4_cash.json`: the cash payload, read through `forPayload`.
- `pension_accrual_2026_09_28/derived/`: `summary.json` (hash-pinned), `national_prediction.json` and `oasdi_arms.csv`.
- `receipt_side_long_run_2026_09_28/derived/housing.json`.
- The ACS 2024 1-year PUMS housing and person files, at the receipt-side lane's pinned hashes.

### Reproduce

```sh
# from the repository root, after profiles.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/main_case_decomposition_2026_09_29/profiles_sept29.py
node infra/immigration-fiscal/main_case_decomposition_2026_09_29/decompose.cjs --case sept29
node infra/immigration-fiscal/main_case_decomposition_2026_09_29/decompose.cjs --case sept29_cash
```

### Log

- 2026-09-29 20:14 JST: resumed after the usage-limit stop at 17:24 JST. Only this stub existed; no code or derived file of the lane had been changed. Design read: the adopted package (40c4ba7), its payload (8 correction lines, 2 receipt lines, 3 national-scale edits, row-4 production grid, pension accrual meta), candidate v4 package options (pension4 cash|payable_net, property none|long_run, property_reading low|central|high).
- 2026-09-29 21:02 JST: resumed after the machine reboot of about 20:51 JST (the run had stopped mid-work). The code (decompose.cjs, profiles_sept29.py) and the sept29 outputs were in the working tree, complete (written 20:30–20:33 JST, before the reboot). Rerun here to a scratch directory: all three cases (sept27, sept29, sept29_cash) reproduce the working-tree files byte for byte, rc 0, 28 / 35 / 29 gates PASS. The gate logs were lost with /private/tmp, so every brief gate is rerun below.
- 2026-09-29 21:03 JST: the brief's gates rerun (the logs of 20:30 were lost): gate 1 IDENTICAL 23/23 rc 0 and the tracked `derived/` equal to HEAD; gate 4 passes 1 and 2 IDENTICAL 23/23 rc 0.
- 2026-09-29 21:23 JST: tables rebuilt (the helper was lost with /private/tmp) with printed parts that add, read back and checked; the owner-property frame probe rerun (+$0.34bn); this section written. No code or output changed after the gates.

## v5 case (oct05), 2026-10-05

**Verdict:** On the adopted v5 case ($390.2940–461.2431bn at specifications 48 / 11), 42.75M average residents would
cost other residents **$109.8 / 163.8bn**. The group's excess over them is **$280.5 / 297.4bn**: taxes at given ages
**+$255.3 / 248.3bn**, age structure **+$17.1 / 59.4bn** and service use at given ages **+$8.1 / −10.3bn** (Shapley
means, low / high end). The September 29 reading holds. Lower taxes at the same ages are 91% / 83% of the excess
(September 29: 92% / 86%), and the young age mix adds to the cost in every order. In the cash set ($307.38–383.41bn),
taxes at given ages are 172% / 147% of a $179.4 / 203.0bn excess (September 29: 171% / 150%).

v5 adds 3.04M people and moves the larger group's responses: +$18.88 / 26.40bn on the case. Part 1 takes $7.28 /
11.04bn of it, age structure $4.15 / 10.78bn, taxes at given ages $7.65 / 5.88bn and use −$0.20 / −1.30bn. The added
people are placed at the identified G3+'s ages, where 43% are children. [CALCULATION: `decompose.cjs --case oct05` and
`--case oct05_cash` → `derived/*_oct05.*`, `derived/*_oct05_cash.*`] [FRAMING-SENSITIVE]

Status: proposed; the lead commits. Model self-report: claude-opus-5-5.

### The parts

Shapley means at the case's end specifications 48 (low) and 11 (high). Per member divides by the 42,752,213 people v5
prices: the row-4 union plus the added people.

| Part | $bn, low / high | $ per member | Share of the case | Cash set, $bn | September 29, $bn | Change, $bn |
|---|---|---|---|---|---|---|
| 1. Shared | 109.77 / 163.80 | 2,568 / 3,832 | 28.1% / 35.5% | 128.00 / 180.45 | 102.49 / 152.76 | +7.28 / +11.04 |
| 2. Age structure | 17.11 / 59.40 | 400 / 1,389 | 4.4% / 12.9% | −76.44 / −33.61 | 12.96 / 48.62 | +4.15 / +10.78 |
| 3. Taxes at given ages (with the production term) | 255.33 / 248.31 | 5,972 / 5,808 | 65.4% / 53.8% | 308.71 / 297.77 | 247.68 / 242.43 | +7.65 / +5.88 |
| 4. Service use at given ages | 8.08 / −10.27 | 189 / −240 | 2.1% / −2.2% | −52.89 / −61.20 | 8.28 / −8.97 | −0.20 / −1.30 |
| **The case** | **390.29 / 461.24** | **9,129 / 10,789** | 100% | 307.38 / 383.41 | 371.41 / 434.84 | +18.88 / +26.40 |

[CALCULATION: `derived/decomposition_oct05.csv`, `decomposition_oct05_cash.csv`, `decomposition_sept29.csv`. Each
column is printed by largest remainder so that it adds: part 1 prints 109.77 for 109.777, $3,832 for $3,831.4, and the
cash set's 128.00 for 127.993.] September 29 was $9,353 / 10,950 per member on 39.71M.

The change holds the 3.04M added people and the larger group's responses, which move the identified union by −$0.30 /
−0.32bn (the lineage lane's arm b). The order matters as before (six orders, `decomposition_oct05.csv`):

| Part | Low end, $bn | High end, $bn |
|---|---|---|
| Age structure | 6.2 to 28.1 | 34.5 to 84.2 |
| Taxes at given ages | 249.6 to 261.1 | 229.7 to 266.9 |
| Service use at given ages | 2.9 to 13.3 | −16.5 to −4.0 |

The age part is positive in every order at both ends, and in every order taxes at given ages fall short of the excess.

### Where the change lands

The change from September 29 by line group, Shapley means, $bn, low / high:

| Line group | 1. Shared | 2. Age | 3. Taxes at given ages | 4. Use at given ages | Change in the case |
|---|---|---|---|---|---|
| Income taxes (federal, state, other personal) | −25.9 / −25.9 | 1.7 / 5.8 | 6.4 / 4.9 | — | −17.8 / −15.2 |
| Payroll taxes and contributions | −17.4 / −17.5 | 0.8 / 4.1 | 2.3 / 1.2 | — | −14.3 / −12.2 |
| Consumption taxes | −10.9 / −10.9 | 0.9 / 0.9 | 0.3 / 0.3 | — | −9.7 / −9.7 |
| Property taxes (item 5's three lines) | −4.0 / −4.0 | 0.5 / 0.5 | 0.7 / 0.7 | — | −2.8 / −2.8 |
| Production term (P + F) | — | 0.1 / 0.0 | −0.4 / −0.2 | — | −0.3 / −0.2 |
| Other receipts | −0.2 / −0.2 | 0.0 / 0.1 | 0.0 / −0.1 | — | −0.2 / −0.2 |
| Schools (with K-12 capital) | 10.7 / 10.9 | 3.7 / 8.4 | — | 1.3 / −0.6 | 15.7 / 18.7 |
| Colleges, other education, education benefits | 1.5 / 1.6 | 0.1 / 0.2 | — | 0.2 / 0.1 | 1.8 / 1.9 |
| Medicaid (with uncompensated care) | 8.6 / 8.6 | 0.8 / 0.8 | — | −1.0 / −1.0 | 8.4 / 8.4 |
| Justice (with its capital and state price) | 4.7 / 4.8 | −0.1 / −0.1 | — | 0.4 / 0.4 | 5.0 / 5.1 |
| Refundable tax credits | 2.0 / 2.1 | 0.8 / −0.4 | — | −0.4 / 0.2 | 2.4 / 1.9 |
| Social Security and Medicare | 21.1 / 21.1 | −3.6 / −6.4 | −1.7 / −0.9 | −0.5 / −0.5 | 15.3 / 13.3 |
| Health services and veterans (with state price) | 5.0 / 5.0 | −1.5 / −1.8 | — | −0.3 / −0.2 | 3.2 / 3.0 |
| Cash, food and housing benefits (with public housing's deficit) | 6.0 / 6.0 | 0.2 / −1.0 | — | 0.5 / 0.9 | 6.7 / 5.9 |
| Roads and other economic affairs (with the miles lines) | 2.2 / 3.8 | −0.2 / −0.3 | — | −0.2 / −0.4 | 1.8 / 3.1 |
| Per-head government and enterprises | 3.9 / 5.6 | 0.0 / 0.0 | — | 0.0 / 0.0 | 3.9 / 5.6 |
| Care, shelter and audit constants | 0.0 / 0.0 | — | — | −0.2 / −0.2 | −0.2 / −0.2 |
| **Total** | **7.3 / 11.0** | **4.2 / 10.8** | **7.6 / 5.9** | **−0.2 / −1.3** | **18.9 / 26.4** |

[CALCULATION: `decomposition_lines_oct05.csv` less `decomposition_lines_sept29.csv`. One decimal, controlled rounding
so that every row and column adds: 7 / 4 cells sit 0.1 off their nearest rounding.]

- **Part 1** takes $7.3 / 11.0bn: 3.04M more people at national per-capita taxes and use.
- **Age structure** takes $4.2 / 10.8bn. The added people's children add $3.7 / 8.4bn of schools. Their working-age share
  is lower than the nation's, which adds $2.5 / 9.9bn of income and payroll taxes not paid. Social Security and Medicare
  take $3.6 / 6.4bn off. Medicare gives $3.4 / 4.0bn of it: Parts B and D follow their few retirees, and the Part A
  accrual their smaller share of covered workers. Social Security's accrual gives $0.1 / 2.3bn, since children accrue no
  pensions (`summary_oct05.json` → `v4.line_parts`).
- **Taxes at given ages** take $7.6 / 5.9bn, $2.5k / 1.9k per added person against the union's $6.2k / 6.1k: the added
  people fall short of national per-age taxes by less than the union does [INFERENCE: the rule below spreads their
  amounts over the group's profile].
- **Use at given ages** gives −$0.2 / 1.3bn: Medicaid −$1.0bn, as the added people draw less of it than the union does
  at the same ages.

In the cash set the change is +$12.68 / 21.59bn: part 1 +$8.46 / 12.16bn, age −$3.36 / +5.06bn, taxes at given ages
+$9.50 / 6.89bn and use −$1.92 / 2.52bn. Its age part differs from the set's mainly in Social Security and Medicare.
Charged as benefits, the added people's few retirees save $11.4 / 12.5bn there, against $3.6 / 6.4bn in the set, so the
age part falls at the low end. [CALCULATION: `decomposition_lines_oct05_cash.csv` less
`decomposition_lines_sept29_cash.csv`]

### Rules designed for v5

v4's rules (section above) apply to v5's payload. The rules below apply only to v5's payload, and the September 27 and 29
outputs are unchanged (gates below).

| Line(s) | Rule used | Why | Alternative beside | Its effect, $bn low / high |
|---|---|---|---|---|
| The added people, every line | Placed at the identified G3+'s ages (`profiles_oct05.py`: convention a, the ASEC person weights, this lane's bins). Every row-4 union key vector is scaled by (union + added) / union in each bin, so each added person carries the union's per-person key at their age. Their own amounts (the lineage's edits) enter through each line's kappa, as the corrections do. [ASSUMPTION] | The Consumers row of `main_case_2026_10_05`: they are priced at G3+'s ages. This lane has no per-age keys for G3+ members or third-plus whites | each added person at G3+ members' or whites' own per-age keys | not computed [GAP]. It moves dollars among parts 2–4 only: part 1 and the case stay |
| `public_order_safety` (justice) | the added people's keyed parts at the union's relative risk, theta 1.101 | the same indirect standardization as the union's | none | — |
| `social_security` (accrual) | one ratio for the whole group: the case's amount over its OASDI receipts, 0.9724 / 0.9722 (the union's ratio_net 0.9737, the lineage's own 0.958 / 0.953) [ASSUMPTION] | the payload's rule, read at every state, at the group's ratio | two ratios, the union's and the lineage's | not computed: it needs the lineage's receipts by age |
| `medicare` | the Part A accrual is $44.45 / 44.00bn: the union's $41.14bn plus the lineage's $3.31 / 2.86bn (its set Medicare less 0.625 × its cash Medicare) | the lineage's Parts B and D are its cash ones, as the union's are | none | — |
| `federal_income_tax` | the tax on current benefits is $2.38 / 2.07bn: the union's $2.09 / 1.82bn plus the lineage's $0.29 / 0.25bn (its cash less its set income tax) | the payload's rule | none | — |
| `lane_constants` | the lineage's edit (−$0.19bn) is the added people's own, 0 at U = N; at U = N row 8 is c × v5's factor, $1.890bn | it is their share of the line | split out the $0.07bn of the edit that is G3+'s per-member share of row 8 | part 1 +0.07, use −0.07 |
| Per member | 42,752,213 | the count v5 prices | 39,712,493 | per-member figures × 1.077 |
| Part 1 at the published count | not computed | the added people are counted on the account's frame only | — | — |
| Linearity note | doubles v5's group share, 0.1292 | the note doubles the case's own group | — | — |

[CALCULATION: `summary_oct05.json` → `v5`; the printed accrual amounts are rounded so that they add (the lineage's
Part A accrual prints 3.31 for 3.317, its benefit tax 0.29 for 0.285).]

### Would change it

| Rule | 1. Shared | 2. Age | 3. Taxes | 4. Use | The case |
|---|---|---|---|---|---|
| Central (this section) | 109.8 / 163.8 | 17.1 / 59.4 | 255.3 / 248.3 | 8.1 / −10.3 | 390.3 / 461.2 |
| National money's worth at national per-age taxes (0.901 for the group's 0.972) | 97.9 / 152.0 | 16.9 / 59.7 | 267.4 / 259.8 | 8.1 / −10.3 | 390.3 / 461.2 |
| Part A accrual scaled by HI receipts instead of covered workers | 129.6 / 186.6 | 17.4 / 57.1 | 235.2 / 227.8 | 8.1 / −10.3 | 390.3 / 461.2 |
| Justice profile flat over 18–64 | 109.8 / 163.8 | 14.4 / 56.6 | 255.3 / 248.3 | 10.8 / −7.5 | 390.3 / 461.2 |
| Corrections, the lineage's amounts with them, as fixed dollars | 109.8 / 163.8 | 13.8 / 55.9 | 255.4 / 247.6 | 11.3 / −6.1 | 390.3 / 461.2 |

[CALCULATION: `summary_oct05.json` → `sensitivities`; each row printed by largest remainder so that it adds]

Under every rule, taxes at given ages are 90–92% of the excess at the low end and 83–84% at the high end. Each rule moves
the parts by about what it moved them on September 29.

### Controls and gates

`decompose.cjs` gates (exit 1 on any failure): oct05 41 PASS, oct05_cash 35 PASS. sept29 (35), sept29_cash (29) and
sept27 (28) are unchanged. The new gates:
- The age file's G3+ is the payload's identified_g3plus, 14,342,574.6. The row-4 frame held the account's 39,712,493.3
  and now holds the lineage's 42,752,212.9 (1e-3 persons).
- The payload's last 336 edits are the package's lineage edits (`meta.lineage.edits`), row 8's last.
- The set's and the cash set's lineage edits are the same cells and differ on Social Security, Medicare and federal
  income tax only.
- The lineage's v4 group share is the finite-removal memo's s.
- Row 8 is v4's $1.898bn plus the lineage's row-8 edit (−$0.0080bn), c × v5's factor (1e-12).
- The per-member count is the lineage's 42,752,213. This gate replaces v4's.
- Two checks per end join the key-share checks (52 per end in the set, 47 in the cash set). The September 29 union's
  Social Security is ratio_net × its OASDI receipts (1e-9), and the lineage's Part A accrual and benefit tax are
  positive.

The other gates pass as before:
- (b) the corrected union reproduces $390.2940 / 461.2431bn and the cash set $307.3764 / 383.4093bn (relative 1e-12).
- Per-head lines' kappa is 1.0000000 on v5's frame: the lineage prices per-head lines at the union's per-capita amounts.
- (a) the parts add in all six orders (worst 1.1e-13).
- (c) twice part 1 holds (1e-9).

`profiles_oct05.py` has 4 gates:
- G3+ (convention a) is the generation lane's 14,342,574.606276 (1e-3 persons).
- The bins add.
- Every bin holds members (the smallest holds 64,752).
- The five-year shares reproduce `white_lines.json`'s g3plus structure (worst 1.4e-8).

`scripts/rerun_lane.py` ran nine commands: the six of September 29, plus `profiles_oct05.py`, `decompose.cjs --case oct05`
and `--case oct05_cash`. Result: IDENTICAL, 33/33 files, rc 0 (23:52:29–23:52:52 JST, offline). `git diff --quiet` on
`derived/` gave rc 0: the tracked September 27 and 29 outputs are HEAD's bytes.

### Files

Written (this lane only):
- `decompose.cjs` (modified): `--case oct05 | oct05_cash`. The September 27 and 29 outputs are unchanged.
- `profiles_oct05.py` (new, 4 gates) → `derived/g3plus_ages_oct05.csv`.
- New outputs: `derived/decomposition_oct05.csv`, `decomposition_lines_oct05.csv`, `states_oct05.csv`,
  `summary_oct05.json`, and the same four with `_oct05_cash`. `summary_oct05*.json` → `v5` holds the rules, the added
  people by bin, the lineage's accrual amounts and row 8's part in its lane-constants edit.

Read, not edited:
- `main_case_2026_10_05`: `package.cjs`, `corrections.json`, `corrections_cash.json` and `summary.json`.
- `main_case_lineage_2026_10_05/derived/white_lines.json`.
- The generation lane's `frame.py`, a read-only import through `profiles.py`.

### Reproduce

```sh
# from the repository root, after the September 29 commands
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/main_case_decomposition_2026_09_29/profiles_oct05.py
node infra/immigration-fiscal/main_case_decomposition_2026_09_29/decompose.cjs --case oct05
node infra/immigration-fiscal/main_case_decomposition_2026_09_29/decompose.cjs --case oct05_cash
```

### Log (times from `date`, JST)

- 2026-10-05 23:46:56: `profiles_oct05.py` run, 4 gates passing.
- 23:51:28: first `--case oct05` run to scratch, all gates passing; then oct05_cash; both written to `derived/`, byte-equal
  to the scratch runs.
- 23:52:29–23:52:52: `rerun_lane.py` IDENTICAL 33/33, rc 0.
- 2026-10-06 00:00:30: tables computed from the derived files; this section written after.
