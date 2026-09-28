**Verdict:** The September 27 case ($321.8–387.4bn a year) splits into four additive parts at its two ends (low / high, Shapley means). The **shared** part is $163.8 / 212.5bn: what the account's own 39.71M-person group would cost other residents at national per-capita taxes and service use. **Age structure** is −$76.9 / −42.5bn, **taxes at given ages** +$294.9 / 287.0bn and **service use at given ages** −$59.9 / −69.6bn. As shares of the case they are 51% / 55%, −24% / −11%, 92% / 74% and −19% / −18%. The group costs more than average residents only because it pays less tax at the same ages: income taxes $204 / 196bn, payroll $65 / 60bn and consumption taxes $39bn, less a production gain of $14 / 9bn. Two parts lower its cost. Its young age structure saves more on retirees than it adds in pupils. At given ages it also draws less from Social Security, Medicare, veterans' and other health programs than it draws extra from schools, cash, food and housing aid. The parts add to the case within 3e-13bn in all six orders, but the order moves the age part by up to $55bn at the low end and $86bn at the high end. A separate finding: since September 24 the corrected account is an account of 39.71M members, after audit row 4 reweighted the Mexico-born to the ACS, while the record's per-member figures for the union divide by 40.90M. Those figures run 2.9% low: the case is $8,104 / 9,754 per account member, not $7,869 / 9,472. The whole gap sits in the first generation and outside California and Texas. The generation account's first-generation figures run 9.7% low: $8,496 / 7,096 per member, not $7,673 / 6,408. [CALCULATION: `decompose.cjs` → `derived/decomposition.csv`] [FRAMING-SENSITIVE]
claude-opus-5-5

Status: proposed; the parent commits. No total changes; no other lane's file was edited.

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
