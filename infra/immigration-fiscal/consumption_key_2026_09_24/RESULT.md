**Verdict:** The consumption key understates the group's consumption taxes, and correcting it
lowers the adopted main case by about $4bn. The key treats every dollar of SPM resources as spent,
but richer residents save more of theirs, so the key hands other residents too large a share of the
four consumption-keyed lines. With the 2024 Consumer Expenditure Survey (CE) ratios of spending to
income by income position, the group's share rises from 8.104% to 8.894%. That alone lowers the
main case by $7.7bn.

Remittances pull the other way, and by less:
- calibrated to Banxico's US corridor less temporary workers' pay, they cut the share to 7.845%
  (+$3.3bn);
- at surveyed or BEA amounts, the effect is +$0.9bn.

Together the main case moves from $200.9–246.3bn to **$196.8–242.3bn (−$4.1bn)**. Across the
remittance calibrations and saving variants, the change runs from −$2.6bn to −$8.4bn.

Three outside checks support the saving correction and suggest it is, if anything, too small:
- CBO's excise distribution by income group;
- ITEP's incidence gradient, which gives −$10.3bn on the account's own base;
- CE's own Mexican-origin consumer units.

**This is a proposal. Nothing is adopted.** [2026-09-26: adopted together with finite-removal
responses in `main_case_2026_09_26` ($200.9–245.7bn; ladder 229; decision
`decisions/2026-09-26-main-case-finite-removal-and-consumption-key.md`).]

Model self-report: claude-opus-5-5[1m]. Lane `infra/immigration-fiscal/consumption_key_2026_09_24/`,
brief [BRIEF.md](BRIEF.md), run 2026-09-24/25. Effects are $bn a year of cost to other residents.
The low end is the shared allocation and the high end the personal allocation, as in the adopted
case. The four lines carry one target in both allocations, so both ends move by the same amount.

| Main case | Group share of the key | Share after the adopted corrections | Main case, $bn (low / high) | Change, $bn |
|---|---:|---:|---:|---:|
| Adopted (the current key) | 8.104% | 7.696% | 200.875 / 246.318 | — |
| Saving alone (CE central) | 8.894% | 8.446% | 193.176 / 238.620 | −7.699 |
| Remittances alone: Banxico corridor less H-2 pay | 7.845% | 7.428% | 204.146 / 249.589 | +3.271 |
| Remittances alone: survey (FDIC sender rates × CEMLA amount) | 8.024% | 7.620% | 201.801 / 247.245 | +0.926 |
| **Both, corridor** | 8.599% | 8.142% | **196.823 / 242.267** | **−4.052** |
| Both, survey | 8.803% | 8.360% | 194.214 / 239.657 | −6.662 |

[CALCULATION: `consumption_key.py` → `derived/key_specs.csv`; `engine_run.cjs` → `derived/engine_summary.json`]

**Would change it:**
- the Latino National Survey 2006 respondent file, which would give measured US-born sending
  amounts (ρ below) and needs an operator ICPSR login;
- any split of Banxico's corridor by the sender's residence or nativity, which would settle whether
  the corridor or the surveys describe the group's households;
- a CE-to-PCE reconciliation by income, which would size CE's shortfall at the top (the
  top-decile rows below);
- Mexico's FY2024 H-2A visa count;
- receiving-side totals for other countries' US corridors, which govern how other residents'
  sending is treated.

## Gates

| Gate | Result |
|---|---|
| The current key reproduces 8.104% from the CPS archive | **Pass.** 8.104060733729859%, stored 8.10406073372985%, SE 0.116 points. The group holds $998.5bn of $12,321.3bn [CALCULATION: `cps_frame.py` → stdout; stored value `../full_account_receipts_2026_09_20/derived/allocation_keys.csv`] |
| CE tables quoted with table ids and years | **Pass.** See [Sources](#sources) |
| Engine with no edits reproduces $200.875–246.318bn | **Pass.** 200.875 / 246.318 [CALCULATION: `engine_run.cjs` → stdout] |
| Every computed specification appears here | **Pass.** 42 specifications in the [full table](#every-specification); every CE check cell is in the check tables |
| Adopted payload rebuilt before composing | **Pass.** One stack factor, φ = 0.949694359, on all four lines. The selective-excise target 29.774743 = φ × (8.104% × $271.298bn non-federal + CBO's 9.369139% × $99.964bn federal) |
| Coverage | **Pass.** Every specification moves all eight receipt scenarios alike (maximum spread 8.5e-14 $bn). Spending edits on resource keys carry no main-case weight |
| Tests | **Pass.** 8 passed (`test_consumption_key.py`) |

## The key and how each specification replaces it

`../full_account_receipts_2026_09_20/builder.py` gives each person positive SPM resources divided
by unit size. The group's share of that key is applied to four lines:

| Line | National total, $bn |
|---|---:|
| General sales tax | 602.43 |
| Selective excise (of which $99.964bn federal) | 371.262 |
| Customs | 83.587 |
| Personal current transfers | 141.065 |
| **Total** | **1,198.3** |

One point of key share is worth about $12bn of receipts. Each specification replaces a person's
key with

    c(unit) × max(resources − M(unit), 0) / size

where:
- c is consumption per resource dollar at the unit's income rank (the saving correction; c = 1 for
  the current key);
- M is the unit's modelled remittance outflow (M = 0 without remittances).

**Composition with the adopted corrections.** The adopted payload does two things to these lines:
- it scales the group's share of every consumption line by φ = 0.949694 (dataset audit and count
  corrections);
- it re-keys the federal-excise part to CBO's group shares.

The specifications compose with it as follows:
- A ratio correction scales with φ. That covers saving, and the survey and BEA flows, which are
  built on CPS counts.
- The Banxico corridor is fixed in dollars, so its outflow is not scaled by φ.
- The federal-excise part keeps CBO's shares across income groups and takes each specification's
  group share inside each CBO group.
- Each line's edit is the specification's target less the adopted target.

**Scenarios and the one departure from `expand()`.** `package.cjs` `expand()` carries a receipt
shift to every scenario in proportion to the scenario's target. The four lines hold one target in
all eight scenarios, so every scenario gets the same dollar edit.

`remaining_production_property` is keyed on consumption only in `property_residual_consumption`,
where it is an indirect cell. There it takes the key's proportional change. Its other seven cells
are keyed on capital, so they are left alone. This is the one departure from `expand()`.

**Engine run.** The engine run composes `adopted.edits.concat(spec.edits)` through
`Engine.applyCorrections`. Its band functions are copied from `package.cjs` rather than imported,
because loading `package.cjs` rewrites `main_case_2026_09_24/derived/stack_line_deltas.json`.
[CALCULATION: `consumption_key.py` → `derived/payloads.json`; `engine_run.cjs` → `derived/engine_bands.csv`]

## Saving (task 2)

**Method.**
- **Ratios.** The CE 2024 decile table (Table 1110) gives mean spending and income before taxes by
  decile. "Consumption" is spending less personal insurance and pensions and less cash
  contributions.
- **Shape within deciles.** The 2024 Interview microdata give the shape of the ratio inside each
  decile, in 50 rank bins. Each decile is rescaled to its published ratio. Ranks are recomputed,
  because BLS's INC_RANK does not follow FINCBTXM. With recomputed ranks the microdata reproduce
  the deciles' incomes within 2.3% and their consumption within 6.4% (the top decile is the worst).
  [DATA: `derived/pumd_decile_control.csv`]
- **Ranking CPS units.** CPS SPM units are ranked the CE way: pre-tax money income plus SNAP, unit
  weights.
- **Conversion to resources.** The CE ratio to pre-tax income becomes a ratio to resources through
  the CPS's own ratio of pre-tax income to resources in the same rank bin.
- **Bottom decile.** Its bins are pooled at the decile's ratio, because incomes there are near zero.

The 2024 tables carry no after-tax income: "Beginning with 2024 publication, estimates developed by
TAXSIM models will no longer be published." [SOURCE: BLS CE Table 3214, 2023–2024, footnote b]

The steepness being carried over is in the published deciles. Consumption per dollar of pre-tax
income is:

| Decile | 1 | 4 | 6 | 10 | All units |
|---|---:|---:|---:|---:|---:|
| Consumption / pre-tax income | 3.18 | 0.98 | 0.73 | 0.40 | 0.64 |

[SOURCE: BLS CE Table 1110, 2024] [DATA: `derived/saving_curves.csv`]

**Results.** The central specification is `saving_central`: +0.790 points, to 8.894%. The change's
own sampling SE is $0.51bn on the CPS replicates. CE sampling error, from a 200-draw bootstrap of
consumer units, is 0.021 points.

| Saving variant | Key share | Main case change, $bn |
|---|---:|---:|
| Central: consumption, 50 bins, ratio transport | 8.894% | −7.699 |
| Published deciles only (step) | 8.835% | −7.082 |
| Level transport (CE dollars per unit ÷ CPS resources per unit) | 9.016% | −8.919 |
| Total spending instead of consumption | 8.732% | −6.099 |
| Taxable-type consumption (also less shelter, health, education) | 8.872% | −7.515 |
| Bottom decile capped at 1.0 | 8.873% | −7.669 |
| Rank × family size (20 × 5 cells) | 9.053% | −9.484 |
| Rank × size × age of head | 9.011% | −9.006 |
| Top decile's ratio × 1.25 (sensitivity to CE's shortfall at the top) | 8.693% | −5.646 |
| Top decile's ratio × 1.5 | 8.512% | −3.802 |
| Central × CE Mexican-origin residual on rank (1.036) | 9.186% | −11.019 |
| Rank × size × CE Mexican-origin residual on rank × size (0.984) | 8.918% | −7.954 |

### Check against CE by Hispanic origin

**Published tables.** Table 1110's Hispanic share of consumer units by decile predicts what
Hispanic units should earn and spend. Table 2200 gives the actual Hispanic column:

| Hispanic units | Actual / predicted |
|---|---:|
| Consumption over income (0.711 actual, 0.701 predicted) | 1.015 |
| Consumption, dollars | 0.995 |
| Income | 0.980 |
| Cash contributions ($911 actual, $2,042 predicted) | 0.45 |

Hispanic units consume 1.115 times the share of income that all units do.
[SOURCE: BLS CE Tables 1110 and 2200, 2024] [CALCULATION: `consumption_key.py` → `derived/ce_published_hispanic_check.csv`]

**Microdata.** In the 2024 Interview files, each group's actual spending is compared with the
national ratio in the same cell. Values are actual / predicted, with bootstrap SEs by consumer unit
in parentheses.

| Concept, cells | Mexican origin (1,739 interviews) | Mexican (975) | Mexican-American or Chicano (764) | Hispanic (3,378) | Not Hispanic (19,798) |
|---|---:|---:|---:|---:|---:|
| consumption, 20 income bins | 1.036 (0.020) | 1.069 (0.029) | 0.997 (0.025) | 1.027 (0.015) | 0.995 (0.003) |
| consumption, bins × size | 0.984 (0.020) | 1.005 (0.028) | 0.958 (0.025) | 0.986 (0.016) | 1.003 (0.003) |
| consumption, bins × size × age | 0.993 (0.024) | 1.013 (0.043) | 0.968 (0.024) | 0.994 (0.023) | 1.001 (0.004) |
| total spending, bins | 1.014 (0.017) | 1.042 (0.026) | 0.980 (0.022) | 1.007 (0.013) | 0.999 (0.002) |
| total spending, bins × size | 0.972 (0.017) | 0.991 (0.025) | 0.950 (0.022) | 0.974 (0.014) | 1.004 (0.002) |
| total spending, bins × size × age | 0.981 (0.021) | 0.999 (0.037) | 0.960 (0.021) | 0.982 (0.020) | 1.003 (0.003) |
| taxable-type, bins | 1.098 (0.026) | 1.135 (0.038) | 1.054 (0.036) | 1.056 (0.019) | 0.991 (0.003) |
| taxable-type, bins × size | 1.013 (0.025) | 1.031 (0.034) | 0.991 (0.035) | 0.991 (0.019) | 1.002 (0.003) |
| taxable-type, bins × size × age | 1.018 (0.029) | 1.031 (0.049) | 1.001 (0.033) | 0.995 (0.026) | 1.001 (0.005) |

[CALCULATION: `saving.py` `ce_check` → `derived/ce_microdata_check.csv`. Codes from the CE
dictionary: HORREF1 1 "Mexican", 2 "Mexican-American", 3 "Chicano"; HISP_REF 1 "Hispanic".]

What the check shows:
- **Income position alone.** Mexican-origin units consume 3.6% more than predicted (SE 2.0).
- **With family size.** They consume 1.6% less (SE 2.0).
- **With size and age.** They consume 0.7% less (SE 2.4).

The income-position model fits within two standard errors either way. Without size it
under-predicts the group, so the central correction errs on the small side.

On pre-tax income, CE's Mexican-origin units consume 0.739 against 0.627 for all units, a ratio of
1.179. The central curve predicts 0.694 against 0.621 for the group in the CPS, a ratio of 1.117.
[DATA: `derived/summary.json`]

**Transport, stated.** The check does not measure the account's group directly:
- CE classifies a consumer unit by its reference person's Hispanic origin. The account's group is
  persons: born in Mexico, US-born with a Mexico-born parent, and third-plus generation
  self-identified as Mexican.
- In the CPS, 98.6% of the group reports Hispanic origin. The group is 58.9% of Hispanic civilians:
  40.9m persons, of whom 12.2m first generation, 14.3m second and 14.3m third-plus.
  [CALCULATION: `cps_frame.frame()` arrays, stdout] Table 2200 therefore tests a population of
  which the group is about three fifths.
- The microdata codes 1–3 are closer to the group, but still assigned by reference person.
- CE records no nativity and no parents' birthplace; the MEMI file has country of Hispanic and of
  Asian origin only. So the check cannot separate the first generation.
  [DATA: `_cache/sources/ce-pumd-interview-diary-dictionary.xlsx`]

## Remittances (task 1)

### The corridor, from primary files

- **Banxico receipts.** 2024 receipts were $65,016.8mn (revised from 64,745). Of these,
  $62,794.3mn (96.58%) came from the United States; in 2023 the US share was 96.22%.
  [SOURCE: Banxico SIE table CE167 "País de origen de los ingresos por remesas", series SE43675
  and SE43738, four quarters, consulted 24/09/2026] [DATA:
  `_cache/sources/corridor/banxico_CE167_2022_2025.xlsx`, read back by `remittance.primary_flows()`]
- **What Banxico counts.** It records the remitter's country, not the remitter's residence or
  nativity. A remittance is money "originada por un Remitente para ser entregada en territorio
  nacional a un Beneficiario". [SOURCE: Banxico Circular 12/2012, Regla Segunda]
- **BEA personal transfers.** $72,407mn for 2024. [SOURCE: BEA, *U.S. International Transactions,
  1st Quarter 2025 and Annual Update*, Table 5 line 18,
  https://www.bea.gov/sites/default/files/2025-06/trans125.pdf]
- **What BEA counts.** A modelled flow from foreign-born senders only: "all current transfers from
  households in cash or in kind sent by the foreign-born population resident in the United States
  to households abroad". Transfers by the US-born are "included in other private transfer
  payments". [SOURCE: BEA, *U.S. International Economic Accounts: Concepts and Methods*, June 2026,
  ¶14.31, p. 147] The share of income remitted rests on the 2008 CPS migration supplement
  (¶14.32). H-2 and border workers are non-residents paid compensation (¶6.13, ¶13.57). BEA
  publishes no Mexico row.

### Senders, measured

The FDIC supplement to the June CPS asks whether "(you/ or someone else in your household) send
money to family or friends living outside of the US" in the last 12 months (item HES130). It asks
no amount. [SOURCE: Census CPS June 2015 and 2017 technical documentation,
`_cache/senders/techdoc_jun15.pdf`]

The positive control reproduces FDIC's published nonbank rates within 0.1 point: in 2019, 5.55% of
all households against FDIC's 5.5%. [SOURCE: FDIC, *How America Banks* 2019, Table 6.3]

Pooled 2015 and 2017 household rates by householder:

| Householder | Rate (SE) | Households |
|---|---:|---:|
| Mexico-born | 37.27% (1.24) | 1,984 |
| US-born, Mexico-born parent (G2) | 11.82% (1.16) | 967 |
| G2, a foreign-born member present | 26.28% (3.08) | 248 |
| G2, no foreign-born member | 6.52% (1.04) | 719 |
| US-born of US-born parents, Mexican origin (G3+) | 2.00% (0.47) | 1,190 |
| G3+, with / without a foreign-born member | 11.24% (4.49) / 1.45% (0.42) | 75 / 1,115 |
| Other foreign-born | 28.66% (0.67) | 5,331 |
| Other native, with / without a foreign-born member | 18.84% (1.17) / 1.28% (0.06) | 1,519 / 56,128 |

[CALCULATION: `sender_pull.py` → `_cache/senders/unbank_<year>.json`; `sender_rates.py` →
`derived/sender_rates_pooled.csv`; SEs from the Census generalized variance function]

### Amounts

- **CEMLA.** "la remesa mensual promedio es de 380 dólares" (the average monthly remittance is
  $380). The figure comes from a questionnaire of 6,803 Mexican emigrants visiting Mexico over the
  December 2015 holidays. It is a convenience sample of people able to travel, and it carries no
  SE. [SOURCE: CEMLA, *Migración mexicana, remesas e inclusión financiera*, March 2018, §5.4 and
  Cuadro 6, PDF p. 31, https://www.cemla.org/PDF/remesaseinclusion/2018-04-migracion-mexicana.pdf]
  At CPI-U 2015→2024 (237.017→313.689), that is **$6,035 a year**. [SOURCE: BLS API series
  CUUR0000SA0, annual averages]
- **NIS-2003.** Mexico-born new legal permanent residents who gave money gave a mean of $3,192
  (n = 113 givers), or $5,442 in 2024 dollars. [CALCULATION: `nis_transfers.py` → `derived/nis_transfers.csv`]

### The model

Each SPM unit's expected outflow is **M = θ × P × ρ × E**:
- **P** is the sender rate above for the unit head's type, split by whether a foreign-born member
  is present.
- **E** is the unit's positive earnings.
- **ρ** is what a US-born-only sending unit sends relative to other sending units. No source
  measures it: the central value is 0.5, run also at 0.25 and 1.
- **θ** is solved in each replicate so that a named set of units sends a named flow.

The key splits a unit's outflow per capita, as it splits the unit's resources.

The first generation's share comes out of measured sender counts and ρ; it is never put in. This
follows `remit_leak`'s correction of 2026-09-17, which found that CEMLA's 16.7% is an accounting
quotient, not a first-generation sending rate.

### Corridor against survey

**The survey and BEA agree.** At surveyed amounts, sending units send 8.6% of their earnings. That
gives the group's units $18.4bn and all civilians $83.2bn. Spreading BEA's modelled $72.4bn the same
way, and adding US-born senders, gives $77.7bn.

**The corridor needs far more than surveys find.** Banxico's corridor less H-2 pay is $58.8bn. To
reach it, each expected sending unit must send **$20,203 a year, 28% of its earnings**, 3.3 times
CEMLA's surveyed amount. Even if every one of the 5.83m Mexico-born-headed units sent CEMLA's
$6,035, the total would be $35.2bn.

So the corridor carries money that the group's households in the CPS do not generate at surveyed
amounts. Possible sources:
- unauthorized migrants the CPS misses;
- temporary workers outside the H-2 programs;
- business and illicit flows;
- under-reported sending.

Surveys of recipients miss most of the flow too. ENIGH 2024 captures 7.8% of Banxico's total
[SOURCE: CEMLA *Notas de Remesas* 2026-9, Gráfica 2, secondary on ENIGH]. CE records $295 a year of
gifts to people outside the unit for Mexican-origin units [DATA: `derived/ce_gifts_to_persons.csv`].

The corridor is therefore the upper bound on the group's outflow, and the survey the lower. The
brief asks for calibration to the national flow, which makes the corridor the central case.

| Remittance specification | Flow the group's units send | Group's key share | Main case change, $bn |
|---|---|---:|---:|
| Corridor less H-2 pay ($4.0bn; $2.5–5.5bn [INFERENCE]) | $58.794bn (57.3–60.3) | 7.845% (7.838–7.852) | +3.271 (+3.186 to +3.356) |
| Full corridor | $62.794bn | 7.827% | +3.499 |
| Corridor less H-2 and 7.5% illicit (Signos Vitales via Reuters, secondary) | $54.084bn | 7.866% | +3.004 |
| Corridor, others' sending at BEA's θ, not the corridor's | $58.794bn | 7.751% | +4.338 |
| Corridor, others send nothing | $58.794bn | 7.712% | +4.772 |
| Corridor, ρ = 0.25 / 1 | $58.794bn | 7.842% / 7.850% | +3.303 / +3.212 |
| Survey: FDIC × CEMLA $6,035 (ρ 0.25 / 0.5 / 1) | $18.4bn at ρ 0.5 | 8.025% / 8.024% / 8.022% | +0.912 / +0.926 / +0.955 |
| Survey: FDIC × NIS $5,442 | — | 8.032% | +0.835 |
| BEA: units with a foreign-born member send $72.407bn (ρ 0.25 / 0.5 / 1) | $17.2bn at ρ 0.5 | 8.031% / 8.029% / 8.027% | +0.851 / +0.864 / +0.891 |

**The H-2 allowance** rests on three pieces:
- Mexican H-2B visas, 90,457 in FY2024 [SOURCE: USCIS, *Characteristics of H-2B Nonagricultural
  Temporary Alien Workers FY2024*, Table 1];
- about 250–300 thousand Mexican H-2A workers [UNVERIFIED: State Dept Table XV(B) gives 315,328
  H-2A visas worldwide, read through a search highlight; Mexico's row was not read];
- an [INFERENCE] of about six months' work at the H-2A wage floor, with half to two thirds of pay
  sent home.

**Others' sending.** "Others" are units without a group member. At the corridor's θ they would send
$207bn, three times BEA's modelled total. The central case applies one θ to every unit
(symmetric). The two sensitivities above bound that choice at $1.1–1.5bn.

### First generation and US-born senders, kept apart

The corridor's $58.8bn split by sending unit, at ρ = 0.5:

| Sending unit (head) | $bn |
|---|---:|
| Mexico-born head | 41.86 (71%) |
| Other foreign-born head (group member in the unit) | 3.00 |
| US-born head with a foreign-born member: G2 / G3+ / other native | 7.62 / 0.88 / 2.42 |
| US-born only: G2 / G3+ / other native | 2.01 / 0.61 / 0.40 |
| **US-born-only share** | **5.1%** (2.6% at ρ = 0.25, 9.8% at ρ = 1) |

FDIC's own household counts point the same way. Of Mexican-origin sending households, 12.1% (2015)
and 19.6% (2017) have a US-born householder, and 5.2% and 9.0% have no foreign-born member at all.
[CALCULATION: weighted households × rates in `derived/sender_rates.csv`, any-channel item]

The key splits outflow per capita. US-born group members therefore bear $23.4bn of the group's
$52.9bn, mostly as the share that falls on US-born children of Mexico-born senders, not through
their own sending. [CALCULATION: `remittance.py` → `derived/remittance_flows.csv`]

## Both (task 4)

"Both" applies the consumption ratio to resources net of remittances, c × max(resources − M, 0).
A dollar-for-dollar variant, max(c × resources − M, 0), gives −4.096 instead of −4.052.

The two effects nearly add: −7.699 + 3.271 = −4.428, against −4.052 together. The small
interaction arises because the saving correction also scales the remitted dollars.

Per-line edits, $bn of the group's receipts:

| Specification | General sales | Selective excise | Customs | Personal current transfers | Total |
|---|---:|---:|---:|---:|---:|
| `saving_central` | +4.518 | +1.496 | +0.627 | +1.058 | +7.699 |
| `remit_corridor_net_h2` | −1.616 | −1.052 | −0.224 | −0.378 | −3.271 |
| `remit_survey_cemla` | −0.457 | −0.298 | −0.063 | −0.107 | −0.926 |
| `both_corridor_net_h2` | +2.685 | +0.366 | +0.372 | +0.629 | +4.052 |
| `outside_itep_gradient` | +5.885 | +2.266 | +0.817 | +1.378 | +10.346 |

The selective-excise edit under saving has two parts: +$2.035bn on the $271.3bn non-federal part
and −$0.538bn on the federal part. The federal part falls because of how the two income rankings
differ:
- CBO groups households by size-adjusted income;
- CE ranks by unadjusted income;
- inside each CBO group, the group's larger units rank higher on unadjusted income, where CE shows
  a lower consumption ratio.

So the group's share at CBO's shares falls from 9.369% to 8.802% (8.930% with size cells).

## Outside checks (task 3)

### CBO federal excise

The corrected key reproduces CBO's excise distribution group by group, within a point everywhere
except the top 1%. Each cell is the income group's share of the key, with the account group's share
inside that income group in parentheses:

| CBO group (2022) | CBO excise share | Current key | `saving_central` | `saving_rank_x_size` | `both_corridor_net_h2` |
|---|---:|---:|---:|---:|---:|
| Lowest fifth | 10.73% | 5.56% (18.36%) | 11.06% (16.55%) | 11.06% (16.65%) | 11.07% (16.00%) |
| Second | 14.34% | 10.22% (14.35%) | 14.52% (13.14%) | 14.78% (13.31%) | 14.52% (12.61%) |
| Middle | 18.05% | 15.27% (11.10%) | 17.59% (10.46%) | 17.75% (10.63%) | 17.62% (10.07%) |
| Fourth | 21.16% | 22.43% (7.90%) | 22.08% (7.67%) | 21.98% (7.81%) | 22.14% (7.41%) |
| 81st–90th | 13.14% | 16.07% (6.27%) | 13.79% (6.03%) | 13.85% (6.17%) | 13.78% (5.88%) |
| 91st–95th | 7.92% | 10.80% (4.11%) | 8.25% (4.08%) | 7.90% (4.13%) | 8.24% (4.02%) |
| 96th–99th | 8.22% | 12.66% (3.74%) | 8.42% (3.76%) | 8.21% (3.81%) | 8.38% (3.66%) |
| Top 1% | 6.42% | 7.00% (3.19%) | 4.28% (3.19%) | 4.46% (3.26%) | 4.26% (3.15%) |

On the $99.964bn federal part, the group's dollars at the key and at CBO's shares, $bn (SE of the
gap in parentheses):

| Specification | At the key | At CBO's shares | Gap |
|---|---:|---:|---:|
| Current key | 8.101 | 9.366 | −1.265 (0.050) |
| `saving_central` | 8.891 | 8.798 | +0.092 (0.033) |
| `saving_step_deciles` | 8.832 | 8.793 | +0.039 (0.031) |
| `saving_level_transport` | 9.013 | 8.743 | +0.270 (0.038) |
| `saving_total_expenditure` | 8.729 | 8.891 | −0.162 (0.033) |
| `saving_taxable_broad` | 8.869 | 8.841 | +0.028 (0.034) |
| `saving_rank_x_size` | 9.050 | 8.927 | +0.123 (0.033) |
| `saving_rank_x_size_x_age` | 9.008 | 8.883 | +0.125 (0.033) |
| `saving_top_decile_x1.25` | 8.690 | 8.843 | −0.154 (0.033) |
| `remit_corridor_net_h2` | 7.842 | 9.051 | −1.209 (0.048) |
| `remit_survey_cemla` | 8.021 | 9.269 | −1.247 (0.050) |
| `both_corridor_net_h2` | 8.595 | 8.503 | +0.092 (0.032) |

[SOURCE: CBO 61911 researcher Table 12, excise_taxes 2022, read through the outside-checks lane's
own functions] [CALCULATION: `outside.py` → `derived/cbo_check.csv`, `derived/cbo_check_summary.csv`;
the current key reproduces that lane's 9.369139409279738% exactly]

**Why ladder 216 found a match.**
- The current key sat $1.3bn from CBO on the federal part, inside ladder 216's $2.1bn line.
- The gap was the saving error on a $100bn line: at the bottom fifth, CBO has 10.7% and the key
  5.6%.
- The corrected key closes the gap to $0.1bn.
- The same error on all $1,198bn of consumption lines is the −$7.7bn above.

The match held only because the federal part is small.

CBO allocates excise by CE consumption patterns [INFERENCE]. This check therefore tests how the CE
gradient carries over to the CPS, not the CE gradient itself.

### ITEP *Who Pays?* 7th edition

ITEP's U.S. Average table (2024 law at 2023 incomes, non-senior families) gives sales and excise
taxes as a share of family income:

| | Lowest 20% | Second 20% | Middle 20% | Fourth 20% | Next 15% | Next 4% | Top 1% |
|---|---:|---:|---:|---:|---:|---:|---:|
| Tax share of family income | 7.0% | 5.7% | 4.8% | 3.9% | 3.0% | 1.9% | 1.0% |

[SOURCE: https://sfo2.digitaloceanspaces.com/itep/ITEP-Who-Pays-7th-edition.pdf, U.S. Average
table, PDF p. 205]

The report reads the average state's consumption taxes as "like an income tax with a 7 percent rate
for the poor, a 4.8 percent rate for the middle class, and a 1 percent rate for the wealthiest
taxpayers" (p. 33).

Distribution across ITEP's groups, % of each total. On the CPS side these are non-elderly units
ranked by money income.

| | Lowest 20% | Second | Middle | Fourth | Next 15% | Next 4% | Top 1% |
|---|---:|---:|---:|---:|---:|---:|---:|
| ITEP sales and excise tax dollars | 5.6 | 11.7 | 17.7 | 24.9 | 24.9 | 9.6 | 5.6 |
| Current key | 3.9 | 9.2 | 14.6 | 22.7 | 28.3 | 13.7 | 7.5 |
| `saving_central` | 9.1 | 13.7 | 17.2 | 22.7 | 23.5 | 9.1 | 4.7 |

Per dollar of money income, relative to the middle group:

| | Lowest 20% | Second | Middle | Fourth | Next 15% | Next 4% | Top 1% |
|---|---:|---:|---:|---:|---:|---:|---:|
| Corrected key | 2.61 | 1.36 | 1.00 | 0.82 | 0.66 | 0.51 | 0.44 |
| ITEP rates | 1.46 | 1.19 | 1.00 | 0.81 | 0.62 | 0.40 | 0.21 |
| Current key | 1.33 | 1.07 | 1.00 | 0.96 | 0.93 | 0.91 | 0.83 |

Above the middle, the corrected key tracks ITEP. Below it, the corrected key is steeper, for two
reasons: resources exceed money income at the bottom, and CE's bottom decile spends 3.2 times its
reported income.

**ITEP's gradient on the account's own base.** To isolate the gradient, ITEP's rates are applied to
the same base as the key:

| ITEP rate applied to resources | Group's share (SE) |
|---|---:|
| Sales and excise | **9.133% (0.098)** |
| General sales, individuals | 9.152% |
| Other sales and excise | 9.719% |
| For comparison: current key / corrected key | 8.104% / 8.894% |

On money income instead, the gradient takes the group from 7.711% (flat) to 8.708%. Run through the
engine as `outside_itep_gradient`, ITEP's gradient gives **−$10.3bn**, about 1.3 times the CE
central. [CALCULATION: `outside.py` → `derived/itep_check.csv`, `derived/itep_keyed_shares.csv`]

ITEP excludes seniors; here their units take the rate for their income group [INFERENCE]. Among
non-elderly persons alone, ITEP's gradient gives 10.753%, against 9.298% for the current key and
10.413% corrected.

## Symmetry (task 5)

Every other line keyed on resources carries the same 8.104% share.

**Receipts.** `remaining_production_property`, in `property_residual_consumption` only. It takes the
same proportional change (`saving_central`: +$2.305bn, personal). It is an indirect cell, so the
main case gives it no weight.

**Spending.** Seven lines have a resources cell:

| Resources is the | Lines |
|---|---|
| Preferred key | `economic_affairs_services` ($451.9bn), `transport_subsidies`, `other_subsidies` |
| Alternative key | `housing_community_services`, `recreation_culture`, `agricultural_subsidies`, `housing_subsidies` |

All seven take the key's proportional change on their resources cells, so benefits are priced like
receipts (rule 5). In the main case both economic affairs and subsidies have zero response, so
these edits move nothing (gate). In the proportional-reference profile, where those services
respond, they add +$3.356bn of cost under `saving_central`, offsetting 44% of the receipt gain in
that profile. `engine_summary.json` gives this for every specification.

**Generation ledger.** `gen_ledger_extension_2026_09_16/extend_ledger.py` (section D1) keys the
generation ledger's sales and excise tax on 0.9 × unit resources × a flat taxable share, with an
ITEP-quintile arm. The ledger is outside the main case and belongs to another lane. Its flat arm
carries the same saving error. It is named here, not edited.

**No shared file needs a change.** The payloads compose with the adopted corrections through the
existing `Engine.applyCorrections`.

## Evidence symmetry (rules 1–5)

1. **Intervals.** FDIC rates carry SEs, the CE check carries bootstrap SEs, and every key share
   carries CPS replicate SEs. CEMLA's amount (a convenience sample), BEA's model and the Signos
   Vitales share carry none, and are labelled that way.
2. **The same flaw on both sides.** Both corrections rest on surveys that under-measure one side:
   - surveys miss remittances, which would make the leak too small; the corridor calibration
     answers that;
   - CE misses spending at the top, which would make the saving correction too large; the
     top-decile rows answer that.

   Both flaws would lower the cost, and both are priced.
3. **Affiliation.** No weight is given to it. ITEP and CBO enter only as checks on a gradient, and
   Signos Vitales only as a labelled secondary sensitivity.
4. **Lean.** Saving lowers the cost and remittances raise it. The central case lowers it by $4.1bn.
5. **Costs and benefits alike.** The same key's spending cells (benefits) move with its receipt
   cells (see Symmetry).

## Limits

- **Sampling error only partly covered.** CE sampling enters only through the central curve's
  bootstrap (0.021 points). The CPS conversion from pre-tax income to resources is fixed at the
  point weights.
- **Dated rates on a different unit.** The FDIC rates are from 2015 and 2017; later years ask only
  about non-bank channels. They are household rates, applied here to SPM units.
- **Amounts per person, not per household.** CEMLA's amount is per sender and NIS's per giver, so
  the survey specification runs low.
- **An untested keying.** The account keys `personal_current_transfers` (fines, fees, donations) on
  consumption. The lane corrects it like the other lines and does not test that keying.

## Every specification

Key share, with its CPS replicate SE. The SE of the receipts change is computed replicate by
replicate against the current key. Main case in $bn, low (shared) / high (personal).

| Specification | Key share, % (SE) | Change, points | Adopted-basis share, % | Receipts change, $bn (SE) | Main case, $bn low / high | Change, $bn |
|---|---:|---:|---:|---:|---:|---:|
| `raw` | 8.104 (0.116) | +0.000 | 7.696 | 0.000 (0.000) | 200.875 / 246.318 | +0.000 |
| `saving_central` | 8.894 (0.098) | +0.790 | 8.446 | +7.699 (0.506) | 193.176 / 238.620 | −7.699 |
| `saving_step_deciles` | 8.835 (0.100) | +0.731 | 8.391 | +7.082 (0.480) | 193.793 / 239.236 | −7.082 |
| `saving_level_transport` | 9.016 (0.096) | +0.912 | 8.562 | +8.919 (0.603) | 191.956 / 237.399 | −8.919 |
| `saving_total_expenditure` | 8.732 (0.100) | +0.628 | 8.293 | +6.099 (0.408) | 194.776 / 240.220 | −6.099 |
| `saving_taxable_broad` | 8.872 (0.098) | +0.768 | 8.426 | +7.515 (0.495) | 193.360 / 238.803 | −7.515 |
| `saving_bottom_capped` | 8.873 (0.100) | +0.769 | 8.427 | +7.669 (0.468) | 193.206 / 238.649 | −7.669 |
| `saving_rank_x_size` | 9.053 (0.101) | +0.949 | 8.598 | +9.484 (0.466) | 191.391 / 236.834 | −9.484 |
| `saving_rank_x_size_x_age` | 9.011 (0.101) | +0.907 | 8.558 | +9.006 (0.491) | 191.869 / 237.313 | −9.006 |
| `saving_top_decile_x1.25` | 8.693 (0.101) | +0.589 | 8.256 | +5.646 (0.406) | 195.229 / 240.672 | −5.646 |
| `saving_top_decile_x1.5` | 8.512 (0.105) | +0.408 | 8.084 | +3.802 (0.352) | 197.073 / 242.516 | −3.802 |
| `outside_itep_gradient` | 9.133 (0.098) | +1.029 | 8.673 | +10.346 (0.636) | 190.529 / 235.972 | −10.346 |
| `saving_ce_mexican_rank` | 9.186 (0.100) | +1.082 | 8.724 | +11.019 (0.501) | 189.856 / 235.300 | −11.019 |
| `saving_ce_mexican_rank_x_size` | 8.918 (0.100) | +0.814 | 8.470 | +7.954 (0.468) | 192.921 / 238.364 | −7.954 |
| `remit_survey_cemla` | 8.024 (0.115) | −0.080 | 7.620 | −0.926 (0.029) | 201.801 / 247.245 | +0.926 |
| `remit_bea` | 8.029 (0.114) | −0.075 | 7.626 | −0.864 (0.030) | 201.740 / 247.183 | +0.864 |
| `remit_corridor_net_h2_low` | 7.838 (0.115) | −0.266 | 7.421 | −3.356 (0.050) | 204.231 / 249.675 | +3.356 |
| `remit_corridor_net_h2` | 7.845 (0.115) | −0.259 | 7.428 | −3.271 (0.049) | 204.146 / 249.589 | +3.271 |
| `remit_corridor_net_h2_high` | 7.852 (0.115) | −0.252 | 7.435 | −3.186 (0.048) | 204.061 / 249.504 | +3.186 |
| `remit_survey_cemla_rho0.25` | 8.025 (0.115) | −0.079 | 7.622 | −0.912 (0.029) | 201.787 / 247.230 | +0.912 |
| `remit_bea_rho0.25` | 8.031 (0.114) | −0.073 | 7.627 | −0.851 (0.030) | 201.726 / 247.169 | +0.851 |
| `remit_corridor_net_h2_rho0.25` | 7.842 (0.115) | −0.262 | 7.426 | −3.303 (0.050) | 204.178 / 249.621 | +3.303 |
| `remit_survey_cemla_rho1` | 8.022 (0.115) | −0.082 | 7.618 | −0.955 (0.029) | 201.830 / 247.274 | +0.955 |
| `remit_bea_rho1` | 8.027 (0.114) | −0.077 | 7.623 | −0.891 (0.030) | 201.767 / 247.210 | +0.891 |
| `remit_corridor_net_h2_rho1` | 7.850 (0.115) | −0.254 | 7.433 | −3.212 (0.046) | 204.087 / 249.530 | +3.212 |
| `remit_survey_nis` | 8.032 (0.115) | −0.072 | 7.628 | −0.835 (0.026) | 201.710 / 247.153 | +0.835 |
| `remit_corridor_full` | 7.827 (0.115) | −0.277 | 7.409 | −3.499 (0.052) | 204.374 / 249.817 | +3.499 |
| `remit_corridor_net_h2_illicit` | 7.866 (0.115) | −0.238 | 7.450 | −3.004 (0.045) | 203.879 / 249.322 | +3.004 |
| `remit_corridor_net_h2_others_bea` | 7.751 (0.116) | −0.353 | 7.339 | −4.338 (0.035) | 205.213 / 250.657 | +4.338 |
| `remit_corridor_net_h2_others_zero` | 7.712 (0.115) | −0.392 | 7.303 | −4.772 (0.037) | 205.647 / 251.090 | +4.772 |
| `both_corridor_net_h2` | 8.599 (0.098) | +0.495 | 8.142 | +4.052 (0.488) | 196.823 / 242.267 | −4.052 |
| `both_corridor_net_h2_dollar_for_dollar` | 8.607 (0.097) | +0.503 | 8.148 | +4.096 (0.521) | 196.779 / 242.222 | −4.096 |
| `both_survey_cemla` | 8.803 (0.097) | +0.699 | 8.360 | +6.662 (0.493) | 194.214 / 239.657 | −6.662 |
| `both_bea` | 8.809 (0.097) | +0.705 | 8.366 | +6.731 (0.507) | 194.144 / 239.588 | −6.731 |
| `both_corridor_full` | 8.578 (0.098) | +0.474 | 8.121 | +3.798 (0.487) | 197.077 / 242.520 | −3.798 |
| `both_corridor_net_h2_illicit` | 8.623 (0.098) | +0.519 | 8.167 | +4.349 (0.490) | 196.526 / 241.969 | −4.349 |
| `both_corridor_net_h2_others_bea` | 8.507 (0.099) | +0.403 | 8.055 | +3.019 (0.482) | 197.856 / 243.300 | −3.019 |
| `both_corridor_net_h2_others_zero` | 8.469 (0.099) | +0.365 | 8.020 | +2.599 (0.483) | 198.276 / 243.720 | −2.599 |
| `both_rank_x_size_corridor_net_h2` | 8.754 (0.102) | +0.650 | 8.289 | +5.785 (0.451) | 195.090 / 240.533 | −5.785 |
| `both_rank_x_size_survey_cemla` | 8.961 (0.101) | +0.857 | 8.510 | +8.433 (0.453) | 192.442 / 237.885 | −8.433 |
| `both_rank_x_size_x_age_corridor_net_h2` | 8.713 (0.101) | +0.608 | 8.250 | +5.314 (0.474) | 195.561 / 241.005 | −5.314 |
| `both_rank_x_size_x_age_survey_cemla` | 8.919 (0.101) | +0.815 | 8.470 | +7.957 (0.478) | 192.919 / 238.362 | −7.957 |

The remittance flows behind the `remit_` and `both_` rows:

| Flow specification | θ, share of sending units' earnings | Sent per expected sending group unit, $ | All civilians' outflow, $bn | Borne by the group in the key, $bn | First generation, $bn | US-born, $bn |
|---|---:|---:|---:|---:|---:|---:|
| `survey_cemla` | 0.0863 | 6,325 | 83.2 | 16.55 | 9.23 | 7.32 |
| `bea` | 0.0806 | 5,905 | 77.7 | 15.45 | 8.62 | 6.83 |
| `corridor_net_h2_low` | 0.2827 | 20,719 | 272.6 | 54.20 | 30.23 | 23.97 |
| `corridor_net_h2` | 0.2757 | 20,203 | 265.8 | 52.85 | 29.48 | 23.37 |
| `corridor_net_h2_high` | 0.2686 | 19,688 | 259.0 | 51.51 | 28.73 | 22.78 |
| `survey_cemla_rho0.25` | 0.0863 | 6,162 | 80.3 | 16.16 | 9.23 | 6.93 |
| `bea_rho0.25` | 0.0806 | 5,754 | 75.0 | 15.09 | 8.62 | 6.47 |
| `corridor_net_h2_rho0.25` | 0.2829 | 20,203 | 263.3 | 52.98 | 30.26 | 22.72 |
| `survey_cemla_rho1` | 0.0863 | 6,650 | 89.0 | 17.32 | 9.23 | 8.09 |
| `bea_rho1` | 0.0806 | 6,209 | 83.1 | 16.17 | 8.62 | 7.55 |
| `corridor_net_h2_rho1` | 0.2622 | 20,203 | 270.5 | 52.62 | 28.04 | 24.58 |
| `survey_nis` | 0.0778 | 5,703 | 75.0 | 14.92 | 8.32 | 6.60 |
| `corridor_full` | 0.2944 | 21,578 | 283.9 | 56.45 | 31.49 | 24.96 |
| `corridor_net_h2_illicit` | 0.2536 | 18,585 | 244.5 | 48.62 | 27.12 | 21.50 |
| `corridor_net_h2_others_bea` | 0.2757 | 20,203 | 119.3 | 52.85 | 29.48 | 23.37 |
| `corridor_net_h2_others_zero` | 0.2757 | 20,203 | 58.7 | 52.85 | 29.48 | 23.37 |

There are 16.08m units with a group member, 2.91m of them expected to send, and 5.83m
Mexico-born-headed units. [CALCULATION: `remittance.py` → `derived/remittance_flows.csv`]

## Sources

| Source | Table, year | Use |
|---|---|---|
| BLS CE, calendar-year tables | **Table 1110**, deciles of income before taxes, 2024 | ratios by income position (central) |
| BLS CE | **Table 2200**, Hispanic or Latino origin of reference person, 2024 | published Hispanic check |
| BLS CE | **Table 1101**, quintiles of income before taxes, 2024 | fetched; not used, since the deciles are finer |
| BLS CE, cross-tabs | **Tables 3203, 3214, 3224, 3234, 3244, 3254** (age of reference person by income, 2023–2024); **3404, 3424, 3434, 3444, 3454** (unit size by income, 2023–2024) | fetched; Table 3214's footnote b is quoted; the size and age cells come from the microdata instead |
| BLS CE Public Use Microdata | 2024 Interview files fmli241x–fmli251 and mtbi (cash-contribution UCCs), https://www.bls.gov/cex/pumd/data/csv/intrvw24.zip | within-decile shape, Mexican-origin check, gifts |
| CPS ASEC 2025 | `gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip` (hash-checked) | the key, ranks, replicates |
| CPS Unbanked/Underbanked supplement | June 2011–2019, Census API | sender rates |
| Banxico SIE CE167; Circular 12/2012 | 2023–2024 | corridor |
| BEA trans125; *Concepts and Methods* June 2026 | 2024 | personal transfers and their scope |
| CEMLA, *Migración mexicana, remesas e inclusión financiera* | March 2018 report of a December 2015 questionnaire | amount per sender |
| NIS-2003 | ICPSR 38031 v3, DS0002/0012/0015/0016 | amount per giver |
| ITEP *Who Pays?* | 7th edition (2024 law, 2023 incomes), U.S. Average | outside check |
| CBO | 61911 researcher Table 12, 2022 | outside check |
| BLS CPI-U | CUUR0000SA0, annual averages 2003, 2015, 2024 | deflating amounts |

`fetch.py` downloads and content-checks the BLS CE tables, PUMD, dictionary, ITEP, CEMLA, BEA and
CPI files. The corridor files in `_cache/sources/corridor/` came from a research subagent. The
Banxico and BEA totals used are read back from those files at run time.

## Files

**Scripts.**
- `consumption_key.py` is the driver.
- Its modules are `cps_frame.py`, `saving.py`, `remittance.py`, `outside.py`, `ce_tables.py` and
  `ce_pumd.py`.
- `engine_run.cjs` runs the engine.
- The data scripts are `sender_pull.py`, `sender_rates.py`, `nis_transfers.py` and `fetch.py`.
- `test_consumption_key.py` holds the tests.

**Outputs.**
- `derived/key_specs.csv` lists every specification.
- `derived/payloads.json` holds each specification's edits, composing with
  `main_case_2026_09_24/derived/corrections.json`.
- Engine: `derived/engine_summary.json`, `derived/engine_bands.csv`.
- Remittances: `derived/remittance_flows.csv`, `derived/sender_*.csv`, `derived/nis_transfers.csv`.
- Checks: `derived/cbo_check*.csv`, `derived/itep_*.csv`, `derived/ce_*.csv`,
  `derived/pumd_decile_control.csv`.
- Curves and summary: `derived/saving_curves.csv`, `derived/summary.json`.

**Rerun**, from the repository root:
1. `OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with openpyxl --with pyreadstat --with duckdb --with pyarrow python3 infra/immigration-fiscal/consumption_key_2026_09_24/consumption_key.py`
2. `node infra/immigration-fiscal/consumption_key_2026_09_24/engine_run.cjs`
3. `... --with pytest python3 -m pytest infra/immigration-fiscal/consumption_key_2026_09_24/ -q`
