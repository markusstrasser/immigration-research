**Verdict:** The operator adopted the two pending corrections together on 2026-09-26. The main case
is now **$200.9–245.7bn a year** of conditional net cost to other US residents, against
$200.9–246.3bn adopted on September 24: +$0.04bn at the low end and −$0.62bn at the high end. It
still rounds to $201–246bn.

The two corrections are each about $4bn and cancel:
- **Finite-removal responses** (ladder 227) move the case **+$4.09 / +$3.43bn**. Removing a group
  that is 12% of residents and 17.5% of pupils saves more than the marginal elasticities imply.
- **The consumption key** (ladder 225) moves it **−$4.05bn**. Richer residents save more of their
  income, so the group pays a larger share of consumption taxes than the old key gave it.

The outer range widens to **$164–277bn** (was $172–276bn), because both corrections bring their own
uncertainty. Under a fixed cost plus a constant marginal cost the removal saves only the
elasticity, which would undo the first correction (−$4.1 / −3.4bn). The consumption key's
specifications run from −$4.4bn to +$1.5bn around the adopted one. No combination changes the sign.
The service share at which the sign would turn rises by about one point, to 5.8–17.0%.
[CALCULATION: `main_case.cjs` → `derived/main_case_bands.csv`, `derived/summary.json`;
`sign_reversal.cjs` → `derived/sign_reversal.csv`; every gate passes]

Date: 2026-09-26. The operator was asked: "Adopt the two pending main-case corrections (ladders 225
and 227) together. Combined they leave the headline at $201–246bn." He answered "kk". Decision
record: [`decisions/2026-09-26-main-case-finite-removal-and-consumption-key.md`](../../../decisions/2026-09-26-main-case-finite-removal-and-consumption-key.md).
The low end is the shared allocation and the high end the personal allocation, as in every
published band.

## What changed

Each change is shown alone on the September 24 case. The gates first reproduce each lane's own run.

| Change | Lane | Alone, $bn (low / high) |
|---|---|---:|
| General government at the finite-removal response, with audit row 8's increment at 0.949 | `finite_response_2026_09_26` (runs I) | +0.37 / +0.39 |
| Schools at the finite-removal response | same (run F) | +3.72 / +3.04 |
| **Finite removal** | same (run J) | **+4.09 / +3.43** |
| **Consumption key**, saving and the Banxico corridor less H-2 pay (`both_corridor_net_h2`) | `consumption_key_2026_09_24` | **−4.05 / −4.05** |
| **Both, one engine run** | (run K) | **+0.04 / −0.62** |

The key's edits are receipt-side and the finite responses act on spending, so the two add exactly:
the interaction is zero to 1e-9 [DATA: `derived/summary.json`, `interaction_total`].

**The responses.** They are engine state, not cell edits. Every consumer must therefore set them,
from `corrections.json` → `meta.responses` (or `summary.json` → `responses`):

| Response | September 24 (elasticity used as response) | September 26 (finite removal) | Group share s |
|---|---:|---:|---:|
| General government, low | 0.59 | 0.6000 | 0.1202 of residents |
| General government, high | 0.84 | 0.8504 | same |
| Schools, growth coefficient | 0.63 | 0.6522 | 0.1748 of pupils |
| Schools, decline coefficient | 0.66 | 0.6813 | same |
| Audit row 8's increment | × 1 | × 0.949 | residents |

The general-government values are spending-weighted means of each component's r, with the fixed
federal executive and legislature staying at zero; r of the composite elasticity itself would be
0.605. [DATA: `finite_response_2026_09_26/derived/r_values.json`]

**By side.** Against the uncorrected model at the adopted responses ($207.4–253.2bn), the receipt
edits move the case +$44.7 / +46.2bn and the spending edits −$51.1 / −53.7bn. The group's receipts
on the reference incidence rule rise from $488.5bn to $492.5bn (shared) and from $458.9bn to $463.0bn
(personal) [DATA: `derived/summary.json`, `group_receipts_bn`].

## Range

Each component's spread is measured in the engine around the new central case and summed as
independent bounds at each band end, as on September 24 [DATA: `derived/components.csv`].

| Component | Variants | Low end, $bn | High end, $bn |
|---|---|---|---|
| Tax records | on-books share low/central/high × two fill-in methods | −5.9 to +6.0 | −4.9 to +5.1 |
| Income gradients | CBO 2018, 2019, 2022 data; scaled to the tax records or not | −1.9 to +2.7 | −1.9 to +2.7 |
| Medical ethnicity | six other specifications; MCBS 65+ ratio taken as the truth | −3.3 to +11.5 | −3.3 to +11.5 |
| Long-term care | extremes of the lane's 960 combinations | −1.4 to +3.0 | −1.4 to +3.0 |
| Education | row 6 weight 0.77/0.82 × school price low/high | −1.7 to +1.7 | −1.7 to +1.7 |
| Benefit keys | ±1.96 SE | −2.3 to +2.3 | −2.3 to +2.3 |
| Justice | 2023 arrests; booking in Texas only or Arizona only | −0.9 to +0.2 | −0.9 to +0.2 |
| Audit rows 9, 10, small items | their bounds | −1.7 to +1.8 | −1.7 to +1.8 |
| Shelter | outlays, served shares, mappings A–C | −0.3 to +0.1 | −0.3 to +0.1 |
| Care | envelope of the lane's specifications ($2.6–13.35bn) | −9.2 to +1.6 | −9.2 to +1.6 |
| **Finite removal (new)** | r = b; the engine key's population share; pupil share 0.16 or 0.18 | **−4.1 to +0.1** | **−3.4 to +0.1** |
| **Consumption key (new)** | the lane's twelve saving-and-remittance specifications | **−4.4 to +1.5** | **−4.4 to +1.5** |
| **Main case** | | **163.8 to 233.3** | **210.3 to 277.1** |

- **The removal's functional form is the new component's whole spread.** Under a power-law cost,
  which the log-log and log-change estimates imply, r > b. Under a fixed cost plus a constant
  marginal cost r = b, and the September 24 responses stand. Neither form is measured over a
  12–17% removal (finite_response_2026_09_26 RESULT, Limits). The share inputs move it by
  $0.3bn at most.
- **The consumption key's spread** is its lane's: survey or BEA remittance amounts instead of the
  corridor move it −$2.6 / −2.7bn, and CE ratios by income rank and household size with survey
  remittances −$4.4bn. Setting other residents' sending to zero moves it +$1.5bn.
- Combining the spreads as independent gives $187–259bn (context only).

The two other service profiles move with the package. With non-school education fixed as well, the
case is $156.5–210.8bn (was $157.1–210.8bn). With every service fully proportional it is
$301.3–334.8bn (was $303.0–336.4bn).

## Sign reversal

`sign_reversal.cjs` imports the September 24 definition and reproduces its columns first (gates,
1e-4). General government responds at 0.6000 and 0.8504, and services at the common share s
[CALCULATION: `derived/sign_reversal.csv`].

| Row | September 24 | September 26 |
|---|---:|---:|
| Break-even share of assigned service costs, personal allocation | 4.8–12.9% | **5.8–13.9%** |
| Break-even share, shared allocation | 7.8–16.0% | **8.8–17.0%** |
| Services fixed, capital fixed, CBO rules and preferred keys ($bn welfare) | −25.3 to +77.8 | −21.6 to +81.5 |

The corrections payload alone, at the September 24 responses, raises the break-even by 1.1 points:
the consumption key adds $4.05bn to the group's taxes, and with services frozen nothing offsets
it. The finite-removal responses act here only through general government, which responds at its
own share whatever s is. They lower the break-even by 0.13–0.14 points. [CALCULATION:
`derived/sign_reversal.csv`, rows `__corrections_only` and `__responses_only`]

## Limits

- **The consumption key's edits are dollars measured on the September 24 central tax stack** (stack
  factor 0.9497). The other five stacks put that factor at 0.9476–0.9518. The range keeps the
  central dollars, which moves the key's saving part by under $0.02bn. [CALCULATION: gate output]
- **The shelter constant stays keyed to 0.59/0.84.** At 0.60/0.85 it would move about −$0.002bn.
- **School dilution** (ladder 222, $16.1bn beside the account) prices the part of school cost left
  free at 0.63–0.66. At 0.652–0.681 that part is about 6% smaller. Not recomputed. [INFERENCE]
- **Instrument.** An LLM assembled this (`notes/llm-bias-caveat.md`). The two corrections were
  proposed on 2026-09-25/26, and the adoption rules were written before this run: both lanes' own
  central specifications, composed without new choices. One correction raises the cost and the
  other lowers it.

## For consumers

- `derived/corrections.json` is the payload for `Engine.applyCorrections`, as before. Its
  `meta.responses` holds the four responses above. A consumer that applies the payload but keeps
  0.59/0.84 and 0.63/0.66 computes the September 24 responses on September 26 data. That mixed case
  is $196.7–242.2bn, not the adopted one.
- `derived/main_case_bands.csv` keeps the September 24 variant names (`adopted`,
  `adopted_2026_09_23`) and adds `adopted_2026_09_24`, `uncorrected_at_adopted_responses`,
  `finite_removal_only` and `consumption_key_only`. Each consumer's "uncorrected" gate must use
  `uncorrected_at_adopted_responses` ($207.4046–253.1859bn), not the September 23 case.
- `derived/summary.json` keeps `main_case`, `adopted_2026_09_23`, `other_profiles`, `range` and
  `group_receipts_bn` (now with `adopted_2026_09_24`), and adds `responses`, `changes` and
  `uncorrected_at_adopted_responses`.

## Reproduce

From the repository root:

```sh
node infra/immigration-fiscal/main_case_2026_09_26/main_case.cjs       # all gates must pass
node infra/immigration-fiscal/main_case_2026_09_26/sign_reversal.cjs   # break-even on the new case
```

`package.cjs` imports `main_case_2026_09_24/package.cjs` unchanged and adds the two corrections.
The September 24 lane's scripts and outputs are unchanged. Its `sign_reversal.cjs` now exports its
definition when imported and writes byte-identical output when run.
