**Verdict:** P7's corrected crime rule gives **$440.05–537.45bn/year** at the current v7 personal endpoints: **+$0.615 / +$4.605bn**, below the review's $5bn bar at both ends under the stated recipient-exposure assumption. The arrest-footed high alternative clears it. These are modeled fiscal-plus-social removals for other US residents, 2024 dollars; the fiscal case remains frozen. [CALCULATION: `p7_crime.py` → `derived/p7_changes.csv`; `real_costs_totals.py --case oct14`] [ASSUMPTION]

## Per-fix changes and totals

Each isolated row changes the named rule from the executed pre-P7 control; stacked rows combine them. Security's isolated row also removes its forward spending from the fear budget, an inseparable overlap correction. Victims and fear are always paired on the selected incident/unit-price arm. The low fiscal footing is the existing raw-coded justice reading; the high is the existing custody reading, at personal specifications 16 / 11. No new pollution, crash or benefit producer rows join. [DATA: `inputs/baseline_totals_oct14.*`; `derived/payment_keys.json`]

| Rule | Δ union social, low/high | Δ lineage pairing, low/high | Lineage pairing | Lineage full span* | $5bn bar |
|---|---:|---:|---:|---:|---|
| `baseline` | +0.000 / +0.000 | +0.000 / +0.000 | 439.435 / 532.848 | 151.925 / 811.414 | below |
| `security_comparator` | -1.291 / -0.996 | -1.436 / -1.132 | 437.999 / 531.716 | 153.154 / 805.060 | below |
| `fear_active_arm` | +0.593 / +1.218 | +0.635 / +1.299 | 440.071 / 534.146 | 149.814 / 816.077 | below |
| `uniform_dot` | +2.977 / +3.884 | +3.187 / +4.140 | 442.622 / 536.988 | 151.597 / 816.077 | below |
| `life_years_crime_only` | +3.711 / +4.704 | +3.972 / +5.015 | 443.407 / 537.863 | 151.848 / 816.077 | clears |
| `mixed_both_ends` | -0.000 / +2.209 | -0.000 / +2.355 | 439.435 / 535.203 | 153.154 / 813.924 | below |
| `lineage_boundary` | -0.987 / -1.032 | -1.072 / -1.119 | 438.363 / 531.729 | 153.878 / 807.452 | below |
| `stacked_legacy` | -1.720 / +1.767 | -1.911 / +1.792 | 437.525 / 534.640 | 154.451 / 810.867 | below |
| `stacked_dot` | +0.639 / +4.405 | +0.615 / +4.605 | 440.050 / 537.452 | 156.215 / 810.867 | below |
| `stacked_dot_recipient_zero` | +1.686 / +5.536 | +1.750 / +5.829 | 441.186 / 538.676 | 154.319 / 814.927 | clears |
| `stacked_dot_recipient_twice` | -0.407 / +3.273 | -0.521 / +3.381 | 438.915 / 536.228 | 158.111 / 806.807 | below |
| `stacked_life_years_crime_only` | +1.366 / +5.217 | +1.392 / +5.470 | 440.827 / 538.318 | 156.463 / 810.867 | clears |
| `arrest_high_beside` | +0.639 / +16.159 | +0.615 / +17.137 | 440.050 / 549.984 | 156.215 / 810.867 | clears |

[CALCULATION: `derived/p7_changes.csv`] All table values are $bn/year. Union changes are the 39.71M union's social rows; lineage changes include the 3.04M added people on the existing justice sender keys and their own consumption payment key. The `union_social_only_*` CSV columns hold the full lineage fiscal row fixed and include only the union's social sender rows; they are **not a union-only fiscal counterfactual**. The complete-account union-only removal changes service responses and is not substituted here.

*Full spans are model envelopes, not confidence intervals. The first gate reproduces the published-union pre-P7 span byte-precision values; the displayed baseline then puts social rows on row4 and adds D. PM/crash endpoints use their already-executed priced-count grids. Other noncrime span ends retain their existing central population factors [APPROXIMATION], rather than a newly executed full nonlinear grid. Every noncrime source/union row is held unchanged across the fixes. The old printed span and this population-consistent baseline are distinct objects. The arrest high beside value changes the central arrest footing; it does not invent an arrest uncertainty envelope.

## Security, fear and the beneficiary boundary

`response()` is the one rule: household security attributable to offending against outsiders has no population subtraction. Businesses/nonprofits pass security costs through to purchasers; the net subtracts the group's payment toward security against other offenders. Government customer receipts remain in national closure but are excluded from the private response [ASSUMPTION: exact fiscal overlap not identified]. The Census customer split is measured; crime-driven shares, source-bridging the EC payer mix to SAS revenue, nonprofit pass-through, in-house coverage and equipment payer mix remain assumptions. [SOURCE: Census 2022 `ecnclcust` and `ecnnapcsind`, URLs/pins in `inputs/security_pins.json`; DATA: `derived/security_inputs.json`; see `security-inputs.md`.]

The current business payment key is extracted from v7's personal general-sales-tax cells, with the **on-case moved consumption lineage share** taking precedence over the old item-base share. An offender-footing change cannot change that payment share. Security and fear are evaluated again for U+D with the lineage's payment share and its separate justice sender multiplier; their net is not multiplied by a single key. [CALCULATION: `payment_keys.cjs`; `derived/payment_keys.json`; `derived/p7_payload.json` `response_parameters`.]

Fear uses WTP minus the active victim harm on the same outsider counts. Its residual removes **positive forward security spending before phi**, floors at zero, and never removes the reverse payment credit as if it were spending. This deliberately prevents security from being counted a second time inside fear; the overlap premise is conservative, not empirically identified. The original equal-population security and fixed-Miller fear figures are preserved beside in `inputs/baseline_social_items.csv` and historical `derived/items.csv`, never adopted as the live P7 crime rows. [CALCULATION: `crime_responses()`; `derived/p7_security_spending.csv`; ASSUMPTION.]

U→D and D→D harms **and benefits** leave the outsider side. The central assumes the added people have average former-outsider exposure in each recipient age range; school uses their measured age mix with uniform within-bin interpolation. It is not an observed geographic or victim-level allocation. Zero and twice the average exposure are reported as sensitivity endpoints, not statistical bounds; they cross the $5bn review threshold on the high side. [DATA: frozen v7 lineage age mix, `frame_counts.csv`; CALCULATION: `lineage_recipient_shares()`, `derived/p7_changes.csv`; ASSUMPTION.]

## Common mortality standard and matched victim/fear rows

Setting **`vsl_standard`**: `dot_uniform` = **$13.7m (2024 dollars)**. `dot_life_years` uses the same base at reference age **40**, **41.000209** undiscounted remaining life-years on the common NVSS 2024 period table; the 3% sensitivity base is **23.255233** years. Age calibration is an assumption. Shared API and values: `../crime_victim_cost_2026_09_23/vsl_standard.py` and `derived/vsl_standard.json` in that lane. [SOURCE: pinned DOT primary table and NVSS workbook, crime lane `inputs/pins.json`.]

The pollution worker can read the same setting/API. A common life-year total needs pollution's mortality age mix or an explicit remaining-year range; this lane does not invent it. The life-year pairing/span rows hold pollution/crashes at their existing DOT valuation and are explicitly **crime-only sensitivities, not uniform life-year totals**. The live P7 payload uses `dot_uniform`, matching existing PM2.5. [GAP: pollution age-specific mortality; ownership boundary.]

| Standard / end | Sender population and recipient boundary | Victims | Fear after security overlap | Victims + fear | Security |
|---|---|---:|---:|---:|---:|
| `dot_uniform` / low | 39.71M union → outside lineage | 34.889 | 6.161 | 41.050 | 0.494 |
| `dot_uniform` / low | 42.75M lineage → outsiders | 37.342 | 6.611 | 43.952 | 0.459 |
| `dot_uniform` / high | 39.71M union → outside lineage | 39.008 | 7.106 | 46.114 | 0.616 |
| `dot_uniform` / high | 42.75M lineage → outsiders | 41.585 | 7.592 | 49.177 | 0.568 |
| `dot_life_years` / low | 39.71M union → outside lineage | 36.341 | 5.435 | 41.776 | 0.494 |
| `dot_life_years` / low | 42.75M lineage → outsiders | 38.896 | 5.833 | 44.730 | 0.459 |
| `dot_life_years` / high | 39.71M union → outside lineage | 40.632 | 6.294 | 46.926 | 0.616 |
| `dot_life_years` / high | 42.75M lineage → outsiders | 43.317 | 6.726 | 50.043 | 0.568 |

[CALCULATION: `derived/p7_joint_valuation.csv`] Mortality earnings/QoL are replaced, not added on top of DOT. Crime ages come from primary SHR 2024 known-Hispanic-first-offender victims, with explicit selection/unknown-age sensitivities; see `../crime_victim_cost_2026_09_23/p7-victim-result.md`.

## Contract, gates and uncertainty

The consumer registry declares comparator, beneficiary population, valuation basis and overlap set for all 15 adopted social rows. Unknown sources/items, incompatible producer declarations, equal-population security, missing/stale payload sources and mismatched item/payload values stop before outputs are written. A historical mode exists solely to reconstruct the executed pre-P7 control; the live P7 rows are validated separately. The regression injects equal-population security through the actual consumer and stops it. [CALCULATION: `../sept24_propagation_2026_09_24/real_costs_totals.py`; `test_p7_contract.py`.]

National security totals close within 1e-6bn; customer fractions within 1e-12. Victim mixed-attribution changes conserve national victim-row incidents and matched cost/count/unit products. Baseline pairing and full-span positive controls pass; every noncrime union span row is byte-equivalent across scenarios. The output comparison permits only the priced pairing, full span and lineage-detail corrections. Old fear/security/aggregate item controls are explicitly relabeled historical, and twelve endpoint-specific fear/security rows are appended; every other exported row stays byte-identical. [CALCULATION: `derived/p7_gates.csv`; primary parser checks; test suites.]

No joint live-key replicate SE is identified. Available partial sampling information is reported separately:

| Component / footing | Population and conditioning | SE, $bn |
|---|---|---:|
| security+fear / mixed | published CPS union; other inputs held | 0.045865 |
| nonfatal_victims / mixed | row4 union | 2.008854 |
| security+fear / custody | published CPS union; other inputs held | 0.045760 |
| nonfatal_victims / custody | row4 union | 2.246060 |

[CALCULATION: `derived/p7_sampling.csv`] Security/fear SE is exact affine propagation of the existing payment key's 160-replicate CPS SDR SE on the **published union**, other inputs held; it is not the row4/lineage/joint crime SE. Victim SE is the existing understated independent-cell NCVS generalized-variance delta method on row4, not a replicate SE. Neither covers uncertainty in phi, offending measurement, demographic transport, mortality age selection, Census customer mix or the beneficiary boundary.

## Report-only checks and review

`report_checks.md` reports geography, state custody reallocation, ICE overlap and the arrest high. Geography already enters one NIBRS transfer and is not an omitted new adjustment; transporting the NCVS mixed-group theta is explicitly a sensitivity. State-by-state custody reassignment is below $5bn. Contract-only annual ICE/ACS overlap is unidentified; the reported stock stresses are not matched survey corrections. The high victim footing uses an ACS institutional multiplier, which cannot be called observed ordinary offending; the arrest alternative remains a charging proxy. [CALCULATION: `derived/report_checks_*`; SOURCE: custody/crime measurement rule and reused detention audit.]

`p7-code-review.md` records the independent source review and corrected findings: all-row contract coverage, principal moved payment key, shared API payment independence, and direct lineage security/fear evaluation. LLM instrument limitations remain: response/transport and welfare assumptions are labeled; modeled attribution is not a measured causal effect.

## Reproduction and fixed scope

```sh
node infra/immigration-fiscal/social_costs_unpriced_2026_09_28/payment_keys.cjs
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/social_costs_unpriced_2026_09_28/security_inputs.py --check
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/social_costs_unpriced_2026_09_28/p7_crime.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/sept24_propagation_2026_09_24/real_costs_totals.py --case oct14
uv run --no-project python3 infra/immigration-fiscal/social_costs_unpriced_2026_09_28/render_p7.py
```

The final validation receipts and every changed path are appended in the parent result file. Historical source outputs remain records; no frozen-case, research-document or independent producer edits. `social_spans_priced_count_2026_09_29` is read-only: it contains PM/crash grids, no crime-driven security producer; its original priced grid is pinned here. No git metadata writes. This result is ready for the parent's adoption/integration decision.

## Completed validation log

2026-10-14 21:58:31 JST (date): 18 targeted social/consumer tests and 8 victim/population tests pass. Social producer IDENTICAL: 65/65; eight commands rc=0; no allow-unrun; totals IDENTICAL: 42/42; two commands rc=0; no allow-unrun; victims IDENTICAL: 38/38; rc=0; no allow-unrun; population IDENTICAL: 27/27; rc=0; no allow-unrun. Warm P7 computation 1.275s / 107.9MB peak RSS; largest victim producer 1.720GB, below the lane limit. Python time.perf_counter and resource.getrusage, Darwin ru_maxrss bytes. Source/consumer regressions and independent review pass. [CALCULATION: `inputs/validation_receipt.json`.]

The captured lane validation receipt is the authority for this completed validation log.

## Historical September 28 result (superseded for the live crime rows)

**Verdict:** On one method per item applied to both groups, the four unpriced items add about **$8bn a year** for the 40.9m Mexican-origin union and about **$51bn a year** for the 42.0m non-Hispanic Black residents (central, 2024 $, cost to residents outside the group). The ranges are −$9bn to $30bn and $17–159bn. The Mexican-origin figure is fear of its violent offending ($10.5bn), less a small gain to other pupils ($1.9bn): Hispanic pupils are 29% of enrollment but 24% of out-of-school suspensions. Its security and property-value lines net to about zero, because its property offending and violent-cost share sit at or below its population share. The Black figure is fear ($25bn), private security ($14bn) and school disruption ($11bn). Property values add nothing to either central figure. A composition price discount is either a transfer between owners and buyers or a capitalisation of crime and schools, which are priced elsewhere. The only part that is neither is a taste for neighbours' race, and it appears only as a flagged high arm: $50bn for the Black group, from Bayer, Ferreira and McMillan, and $19bn for the Mexican-origin group, from a hedonic over-bound. Every central number rests on at least one assumed parameter: the fear share of the willingness-to-pay excess, the crime share of security spending, or the behaviour share of the suspension gap. The evidence level is **modelled**. The Black victim-cost inputs and population come from the comparator lane `black_comparator_rough_2026_09_28`. [CALCULATION: `items.py` → `derived/items.csv`] [FRAMING-SENSITIVE]

Model: claude-opus-5-5

Lane `infra/immigration-fiscal/social_costs_unpriced_2026_09_28/`, started 2026-09-28 18:38:31 JST (from `date`). Integrated by the lead at 19:30 JST: exact Black inputs from the comparator lane and CRDC's Hispanic figures from the primary PDF (see Log).

## Verdict table

$bn a year, 2024 dollars, cost to residents outside the group; low / central / high; negative = a gain to them.

| Item | Mexican-origin union (40.9m) | per member, central | Non-Hispanic Black (41.95m) | per member, central |
|---|---|---:|---|---:|
| 1. Fear and avoidance (non-victims) | 5.2 / **10.5** / 30.3 | $256 | 12.7 / **25.4** / 75.5 | $605 |
| 2. Private security | −2.9 / **−0.6** / 0.4 | −$15 | 3.8 / **14.1** / 25.0 | $337 |
| 3. Property values | 0 / **0** / 18.5 (hedonic over-bound, not added) | $0 | 0 / **0** / 50.2 (taste arm, not added) | $0 |
| 4. School disruption | −11.7 / **−1.9** / −0.5 | −$48 | 0 / **11.4** / 58.4 | $273 |
| **Addable: items 1 + 2 + 4** | −9.4 / **7.9** / 30.2 | **$194** | 16.5 / **51.0** / 158.8 | **$1,215** |

The low and high columns stack every low or every high choice. They form an envelope, not a confidence interval. Where a group's gap is negative (Mexican-origin schools), the high parameters give the lowest cost, so that item's envelope is taken over the corners. At the high end, fear and security overlap (see item 1), so the high sums overstate. For scale, the victim cost to others that this lane builds on is $28.9bn full for the Mexican-origin union and $72.9bn full for the Black group. Central fear is 0.36 and 0.35 of those figures.

## Inputs shared by all items

- The groups are the Mexican-origin union, 40,896,574 in CPS ASEC 2025 [DATA: `crime_victim_cost_2026_09_23/derived/target_population_cps2025.csv`], and non-Hispanic Black (Black alone), 41,954,494 in the same survey [DATA: `black_comparator_rough_2026_09_28/derived/cps_profile.csv`]. Population shares are 12.15% and 12.46% of the 336.7m civilian population.
- Victim cost to others comes from Miller et al. 2021 victim-only prices. The Mexican-origin offence split is read from the lane's `cost_by_victim_and_offence_central.csv`, which sums to its $28.92bn central. For the Black group, the comparator lane runs the same NCVS, SHR, WONDER and price inputs [DATA: `black_comparator_rough_2026_09_28/derived/victim_cost_by_offence.csv`, `victim_cost_summary.csv`]. Non-Black victims bear $72.9bn full:
  - rape and sexual assault, $21.9bn;
  - aggravated assault, $17.2bn;
  - homicide, $16.3bn (1,820 deaths × $8.96m);
  - simple assault, $15.2bn;
  - robbery, $2.3bn.

  The totals are $185.2bn on all victims, from 11,142 homicides, and $507.9bn nationally. The NCVS offender shares cover all violent crime rather than each offence. That likely understates robbery, where Black people account for 52.7% of 2019 arrests, against 33.2% for aggravated assault (FBI 2019 Table 43A).
- Exposure is measured at tract level in ACS 2020–24. The average outsider lives in a tract that is **8.04%** non-Hispanic Black and **7.58%** Mexican-origin, against national shares of 11.9% and 11.3%, across 84,401 tracts. [CALCULATION: `exposure.py` → `derived/exposure.csv`; B03001 from the victim-cost lane's cache, B03002 pulled here]
- CPI-U annual averages are 1990 130.7, 2000 172.2, 2022 292.655 and 2024 313.689 [TRAINING-DATA]. The present value of lifetime earnings is $750,886 in 2024 dollars, the dilution lane's conversion of Chetty–Friedman–Rockoff's $522,000 (2010 dollars) [DATA: `school_dilution_2026_09_24/RESULT.md` Table A].
- All constants and their tags are in `derived/inputs.csv`, and the intermediate values are in `derived/components.csv`.

## 1. Fear and avoidance

**Method.** Cohen, Rust, Steen & Tidd (2004) surveyed 1,300 US households and asked what each would pay for a program that prevented 1 in 10 crimes in their community. The implied willingness to pay per crime prevented, in 2000 dollars, is $9.7m for murder, $237k for rape or sexual assault, $70k for serious assault, $232k for armed robbery and $25k for burglary. The authors put these at "1.5 to 10 times higher than prior estimates of the cost of crime to victims" [SOURCE: https://www.ojp.gov/library/publications/willingness-pay-crime-control-programs; the NIJ executive summary (govinfo GOVPUB-J28-PURL-gpo6387) gives the pilot figures and the calculation: households × WTP ÷ crimes averted]. In 2024 dollars, each is set against the repo's Miller victim-only price. Willingness to pay exceeds the victim cost by **0.97× for murder, 1.05× for rape and sexual assault, 0.56× for aggravated assault**, and 8.1× for robbery (armed-robbery WTP × an assumed 45% armed share [UNVERIFIED]) [CALCULATION: `components.csv` `wtp_excess_*`].

That excess is everything the public values beyond the expected victim cost. It includes fear and avoidance, altruism toward other victims, expected tax savings on justice, and private precautions. The share φ that is non-victims' fear and avoidance is assumed at **0.25 / 0.5 / 1.0** [ASSUMPTION]. With φ below 1, altruism, justice spending and security spending, which are counted in the fiscal account or item 2, stay out of this item.

Robbery's excess is capped at 1.0 in the low and central cases. Cohen's item covers armed robbery only, and its WTP likely includes the risk of death, which is counted under murder. In the high case the cap is removed. Simple assault has no counterpart in Cohen, so it gets zero, except in the high case, which uses the aggravated-assault excess. Property crime gets no fear cost. Non-victims' mental wellbeing does not respond to property crime (next paragraph), and precautions against burglary belong to item 2.

The item is computed as fear_g = φ × Σ over offences of excess × the group's victim cost to others for that offence, and the same method is used for both groups.

**Disconfirmation.**
- **Upward.** Cornaglia, Feldman & Leigh (JHR 2014, 49(1)) use Australian panel data. They find that violent crime rates lower the mental wellbeing of non-victims, while property crime does not. They estimate that "society-wide impact of increasing the crime rate by one victim is about 80 times more than the direct impact on the victim" [SOURCE: https://jhr.uwpress.org/content/49/1/110; IZA DP 8014]. That ratio is measured in mental-wellbeing terms and implies a non-victim cost above even our high arm. Compensating-income methods run high because income coefficients are small, so this result is treated as evidence that the high arm is not absurd, not as a central value.
- **Downward.**
  - Contingent-valuation answers are hypothetical. Actual-payment experiments typically find them overstated by a factor of about 2–3 (List & Gallet 2001 meta-analysis) [TRAINING-DATA].
  - The per-crime values date from about 2000, when violent crime was higher.
  - Fear tracks media coverage and disorder more closely than measured crime. Cornaglia et al. find that local press coverage amplifies the effect, so fear may not fall one-for-one when one group's offending is removed.
  - Stereotype-driven fear exceeds actual offending: perceived neighbourhood crime rises with the share of young Black men beyond measured crime (Quillian & Pager 2001, AJS) [TRAINING-DATA]. That component is caused by others' beliefs, not by the group's offending, and is excluded by allocating on actual victim cost. [FRAMING-SENSITIVE]
- **Double counting.** If altruism is pure, adding altruistic WTP to victims' own losses counts the same loss twice (Jones-Lee 1992; Bergstrom 2006) [TRAINING-DATA]. The central φ of 0.5 is where this is handled.
- **Not located or not used.** Dolan & Peasgood (2007, BJC 47(1)) price the health losses from fear of crime, but only the abstract was reached, so it supplies no number [SOURCE: https://researchonline.lse.ac.uk/id/eprint/33043/]. Anderson 1999 and Ludwig & Cook 2001 were not fetched. Cullen & Levitt's crime-driven flight is a form of avoidance and belongs conceptually inside the WTP excess, so pricing it separately would count it twice.

## 2. Private security

**National crime-driven spend: $49.7 / 74.4 / 104.1bn** [CALCULATION: `components.csv`]. It is built from these lines, each in 2024 dollars:

| Line | Value | Source |
|---|---:|---|
| Contract guards (NAICS 561612), 2022 employer revenue $32.2bn | $34.5bn | Census SAS via FRED `REVEF561612ALLEST` |
| In-house private guards | $26.3bn | BLS OES May 2025 API (see below) |
| Security systems services (561621), 2022 $28.3bn | $30.3bn | Census SAS via FRED |
| Locksmiths (561622) | $2.9bn | Census SAS via FRED |
| Armored car (561613) | $4.5bn | Census SAS via FRED |
| Investigation (561611) | $8.4bn | Census SAS via FRED |
| Direct equipment purchases | $5 / 10 / 20bn | [UNVERIFIED: no primary total] |

The in-house guard line uses BLS OES May 2025. SOC 33-9032 has 1,283,470 jobs at a mean of $42,470, of which 768,900 at $41,380 are inside NAICS 5616. That leaves 514,570 guards outside the industry, earning $22.7bn in wages. The wages are multiplied by 1.40 for benefits [TRAINING-DATA: BLS ECEC], by 0.85 to keep private employers only, because government guards are already in the fiscal account [ASSUMPTION], and by 0.975 to move from 2025 to 2024 prices [ASSUMPTION]. [SOURCE: BLS OES May 2025 API, series OEUN000000000000033903201/04 and OEUN000000056160033903201/04]

The crime-driven share of each line is assumed [ASSUMPTION], low / central / high:
- guards: 0.5 / 0.7 / 0.9;
- alarm monitoring, which includes fire alarms: 0.4 / 0.6 / 0.8;
- locksmiths: 0.3 / 0.5 / 0.7;
- armored car: 0.5 / 0.75 / 1.0;
- investigation: 0 / 0.1 / 0.3;
- equipment: 0.8 in all cases.

**Allocation**, as the brief specifies: cost to others = crime-driven spend × (group's offending share − population share). Offending shares weight property crime 0.75 and violent crime 0.25 [ASSUMPTION], because most security spending is aimed at theft.

- **Black.** In the FBI's 2019 Table 43A, Black people account for 29.8% of property-crime arrests (burglary 28.8%, larceny 30.2%, motor vehicle theft 28.6%) [SOURCE: https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/tables/table-43]. Their share of violent victim cost is 36.5%, $185.2bn of $507.9bn. The weighted share is 31.5% against a 12.5% population share, an excess of **19.0 points**. The low case uses 17.3 points (property only) and the high case 24.0 (violent only).
- **Mexican-origin.** The property share comes from the lane's arrest-share proxy: 11.9% cost-weighted and 9.2% count-weighted. The violent share is 9.65% on the NCVS arm (the group's $49.0bn of violent cost on all victims, out of $507.9bn). On the lane's arrest-share arm it is 14.4%. The population share is 12.1%, so the excess is **−0.8 points** (−2.8 to +0.4). [CALCULATION: `components.csv`]

**Cross-check with the guard-labor lane's regression.** It is rerun unchanged on that lane's `panel.csv` [CALCULATION: `guard_black.py` → `derived/guard_share_coefficients.csv`], and the replication check reproduces the lane's foreign-born coefficient of 0.0196 (0.0070).

- In the lane's own specification, with income, poverty, urban share and violent crime controlled, the **Black-share control is +0.0026 percentage points of guard employment per point of Black share (SE 0.0027, p = 0.35)** across all 51 jurisdictions.
- Dropping Nevada, Hawaii and DC gives +0.0044 (0.0015, p = 0.005). The bivariate slope is +0.0092 (0.0030). Dropping the crime control changes little: +0.0015 (0.0029) and +0.0041 (0.0016).
- The Hispanic share is null throughout: −0.0004 (0.0037) with controls, +0.0003 (0.0020) without the three outliers.

At the population-weighted Black share of 12.0% and a mean guard share of 0.608%, these coefficients attribute **5.2%** (controlled, all 51), 8.7% (without the outliers) or 18% (bivariate) of guard employment to the Black population. Applied to central spend, the controlled figure gives $3.8bn, which becomes the Black low. The allocation's excess of 19% is close to the bivariate and two to four times the controlled estimates.

The controls (poverty, income, urban share) partly mediate offending, so the controlled coefficient answers a different question. Even so, the state regressions suggest that security spending responds less than proportionally to crime at the margin. For the Mexican-origin group both routes give about zero: the Hispanic coefficient implies −0.8% of guard employment, or −$0.6bn.

**Disconfirmation.**
- Much security spending is set by insurance, regulation, events, fire protection or density rather than by crime. In the guard lane, urban share is the dominant confounder. So average-cost allocation likely overstates the marginal response, which is why the low arm uses the regression.
- Arrest shares may overstate Black property offending if policing differs by race. The NCVS has no offender-race item for property crime to check this against. For violent crime, the victim-reported NCVS share of cost (36.5%) is close to the 2019 arrest share (36.4%).
- Pushing the other way, charging each group its population share of security costs understates the excess if the group's share of consumer spending, through which businesses pass security costs on, is below its population share. This is not applied.

## 3. Property values

**Decision: central 0 for both groups.** A composition-linked price discount breaks into five parts, and only the fifth is neither double-counted nor a transfer:

1. **Capitalised crime.** A price discount is the market's present value of the same crime disamenity that the victim cost and items 1–2 already count, so adding it would count the crime twice.
2. **Capitalised schools.** School quality and peers are item 4 and the school-dilution lane.
3. **Neighbours' socioeconomic status.** In Bayer, Ferreira & McMillan's hedonic regressions, once boundary fixed effects are added, "the magnitude of the coefficient on the fraction of black neighbors declines to zero". In the abstract's words, "neighborhood race is not capitalized directly into housing prices; instead, the negative correlation ... is due entirely to the fact that blacks live in unobservably lower quality neighborhoods" [SOURCE: NBER w13236, `_cache/bfm_w13236.pdf`, abstract and p. 5]. This is Harris's (1999, ASR) race-as-proxy result [TRAINING-DATA]. Saiz & Wachter attribute their historical immigrant discount to "low socioeconomic status and ... minority groups" rather than foreignness, and that discount reproduces on their own 1980–2000 data [DATA: `research/immigration-hedonic-replay-2026-09-19.md`]. What socioeconomic status proxies for (crime, schools, public goods) is either already priced or a transfer.
4. **The price change itself.** A capital loss to incumbent owners is a gain to buyers and renters, so it is a **transfer**. At national scale the group's presence raises housing demand: an inflow of 1% of population raises metro rents 1.32% and values 3.43% [DATA: `hedonic_composition_2026_09_19/RESULT.md`]. Removing the group would shift prices the other way, which is again a transfer.
5. **A residual taste for neighbours' race or ethnicity**, net of crime, schools and socioeconomic status. This is the only part that is neither a transfer nor a double count. It is priced only as a high arm and flagged.

**High arm, Black: $50.2bn.** Bayer, Ferreira & McMillan's sorting model controls for block-group income, education, school test scores and crime. Its mean marginal willingness to pay is −$10.50 a month (1990 dollars, SE 3.69) for 10 more percentage points of Black rather than white neighbours. Black households value the same change $98.34 a month more than white households (Table 7; Table 6 gives −104.8 per unit share, the same figure). BFM's block groups average 8% Black, which is used as the household share [ASSUMPTION]. On that basis, non-Black households' valuation is about −$18.4 a month, or **−$44.1 in 2024 dollars**. Multiplied by 117.9m outsider households (persons ÷ 2.5 [TRAINING-DATA]), by 12 months and by an exposure of 8.04/10, it comes to $50.2bn. [SOURCE: w13236 Tables 6–7; CALCULATION: `items.py`]

It stays out of the central figure for four reasons:
1. It is a preference over neighbours' race. Standard welfare accounting and fair-housing law do not count such preferences. [FRAMING-SENSITIVE]
2. It is reciprocal. Black households' own-race preference is about +$80 a month, so the same accounting would charge non-Black residents for Black households' tastes.
3. It comes from the 1990 San Francisco Bay Area and has not been tested nationally in 2024.
4. BFM's crime control is coarse, so perceived crime can load on race, which would overlap with item 1.

**High arm, Mexican-origin: $18.6bn, by a different method.** No sorting-model estimate for Hispanic or Mexican share was located. BFM include % Hispanic in the model but do not report its coefficient. [GAP] The figure applies the repo's modern within-metro ACS gradient, −0.96% per 10 points of Hispanic share, to $2.9tn of housing services (BEA PCE [TRAINING-DATA]) × the outsider share × an exposure of 7.58/10. This is an over-bound. The replay says the ACS gradient is not a price: Zillow values on the same rows give **+0.84%**, so the sign is ambiguous, and the gradient includes capitalised socioeconomic status, crime and schools. This is the one item where the one-method rule could not be met.

**Disconfirmation.**
- Perry, Rothwell & Harshbarger (Brookings 2018) estimate that homes in majority-Black neighbourhoods are devalued by about $48,000, or 23%, for comparable quality and amenities [TRAINING-DATA, not re-read]. That loss falls mainly on owners inside those neighbourhoods, who are largely group members, so it is not a cost to others.
- If stereotype-driven avoidance (Quillian & Pager) is priced into non-group owners' homes, it is a real loss to them. It is caused by beliefs rather than conduct, so it goes in the taste arm, not the central figure.

## 4. School disruption

**Method.** Carrell, Hoekstra & Kuka (AER 2018; NBER w22042) study peers from families linked to domestic violence. One such peer in a class of 25 lowers each classmate's adult earnings by 3.2–4.2% over elementary school, or 0.6–0.8% per year. Their footnote 16 works through the arithmetic: one year of exposure costs $87,696 across 24 classmates, and their range is "$81,000 to $105,000" in present value, at CFR's $522,000 and 3% real. The AER version gives about $80,000. [SOURCE: `_cache/chk_w22042.pdf` p. 22 fn 14–16; https://faculty.econ.ucdavis.edu/faculty/scarrell/DV_Long-run.pdf]

This becomes β, the earnings lost per unit of disruptive-peer share per year: **0.15 / 0.165 / 0.20**, where 0.165 is AER Table 5 column 4 (3.3% over 5 years × 25).

Disruption is proxied by pupils with one or more out-of-school suspensions. In CRDC 2021-22 that is 2.4m pupils, 5% of K-12. Black pupils are 15% of enrollment (boys 8%, girls 7%) and 35% of suspended pupils (22% and 13%). Hispanic pupils of any race are 29% of enrollment (boys 15%, girls 14%) and 24% of suspended pupils (16% and 8%). [SOURCE: CRDC 2021-22 First Look, p. 22 and Figure 12, https://www.ed.gov/media/document/2021-22-crdc-first-look-report-109194.pdf; ed.gov returns 403 to scripts, so the PDF was read from the Wayback Machine copy, `_cache/crdc_2021_22_first_look.pdf`, sha256 6a8296d8…]

The rate gap is **7.8 points** for Black pupils against others (11.7% vs 3.8%). For Hispanic pupils it is **−1.2 points** (4.1% vs 5.4%), with Mexican-origin pupils assumed to match Hispanic pupils of any race; the union's own rate is not published [GAP]. Each printed share is rounded to one point, so each boys-plus-girls sum is known to ±1 point. The low and high cases move both groups' shares by that much: 6.7–9.1 points for Black pupils and −1.7 to −0.7 for Hispanic pupils.

Other inputs:
- **Exposure.** Outsider pupils' exposure to group pupils is taken as tract exposure scaled by the ratio of pupil share to population share: 10.1% for Black pupils and 11.9% for Mexican-origin pupils [ASSUMPTION: schools are as segregated as tracts].
- **Pupils.** Outsider pupils number 42.0m non-Black and 39.45m non-Mexican-origin (from the dilution lane).
- **κ**, the share of the suspension gap that reflects behaviour rather than treatment, is 0.3 / 0.6 / 1.0 [ASSUMPTION].
- **Grades.** CHK's design covers elementary school only, so the low and central cases apply the effect to 6 of 13 grades; the high case extends it to K-12.

Cost = β × PV × outsider pupils × exposure × gap × κ × grade share. The same method is used for both groups. A negative gap makes the item a gain to other pupils: in a share-based peer model, removing a group that is suspended less often than others raises the disruptive share among those who remain. In a proportional peer model, removing a group whose suspension rate equals others' rate leaves others' exposure unchanged. That is why the rate gap against others, not the gross rate, carries the cost.

**Disconfirmation.**
- **Direct race-composition evidence points lower.**
  - Hanushek, Kain & Rivkin (Texas panel, NBER w8741): "racial and ethnic composition has considerably less influence on the achievement gains of whites or Hispanics" than on Black pupils, and "percentage black is largely uncorrelated with achievement for whites and Hispanics" [SOURCE: `_cache/hkr_w8741.pdf` pp. 1–2].
  - Angrist & Lang (2004, METCO) find little effect of Black transfer pupils on receiving-district pupils [TRAINING-DATA].
  - The repo's ECLS-K check uses white pupils, school fixed effects and the share of nonwhite classmates per 10 points. Kindergarten reading is −0.010 (0.008) and math −0.003 (0.009); spring 2000 reading is −0.007 (0.010) and math −0.027 (0.012). Three of the four are null. [DATA: `school_peer_checks_2026_09_20/derived/models.csv`]
  - The repo's NAEP lanes find a positive Hispanic-share slope on white scores and no saturation by baseline Black share [DATA: `naep_saturation_2026_09_28/RESULT.md`].

  On this evidence the **Black low is set to 0**.
- **Suspension is a contested proxy.** Part of the Black–white suspension gap may reflect how pupils are treated (Riddle & Sinclair 2019 PNAS; Owens & McLanahan 2020), while Wright et al. (2014) find prior behaviour accounts for it [TRAINING-DATA]. Hence the κ range.
- **Other reasons for overstatement:**
  - CHK's peers may be more disruptive than the average suspended pupil.
  - Suspension removes the pupil from class, which reduces classmates' exposure.
  - The high case extends the effect beyond elementary grades.
- **Mexican-origin.** The repo's NAEP English-learner slope is −0.038 (0.018) SD per 10 points on white scores. It is statewide and overlaps with the resource-dilution line (about $16bn beside the account). It is not added.

## What can be added to fiscal and victim costs without double counting

[2026-09-28, later: the operator adopted items 1, 2 and 4 into the social rows of the fiscal-plus-social total, from the September 27 case on; property values stay out ([decision](../../../decisions/2026-09-28-social-items-fear-security-schools.md)).]

- **Can be added (central): items 1, 2 and 4.** That is about **+$7.9bn** for the Mexican-origin union, on top of the $322–387bn budget cost, $28.9bn of violent victim cost and $1.3–1.4bn of property crime. For the Black group it is about **+$51.0bn**, on top of a budget cost of $549–595bn in the rough comparator re-key [DATA: `black_comparator_rough_2026_09_28/RESULT.md`] and $72.9bn of violent victim cost. No property-crime victim cost has been computed for the Black group [GAP].
  - Fear is net of the victim cost by construction. At central φ it is also meant to exclude justice spending, which the fiscal account charges by use, and private security (item 2).
  - Security excludes government guards.
  - School disruption is an earnings mechanism, separate from resource dilution. Where a school assault is also an NCVS victimisation, the violence part is already in the victim cost, and the learning part is not.
- **Cannot be added.**
  - Property-value capitalisation would count crime and schools a second time.
  - The taste arms are excluded as normative choices; they are shown for completeness.
  - Fear at φ = 1 overlaps with security.
  - The future tax on lost earnings from item 4 is a decades-later fiscal effect, not added, as in the dilution lane.
  - For the Mexican-origin group, the school-dilution line (about $16bn, beside the account) remains a separate option for the operator. It is not in the $7.9bn.

## Limits and instrument

- The central values are carried by assumed parameters: φ (fear share), the crime share of security, κ (behaviour share of the suspension gap), the armed-robbery share and the equipment spend. Each appears in its own row of `derived/inputs.csv`.
- The Black victim-cost inputs come from the comparator lane, whose NCVS offender shares cover all violent crime rather than each offence.
- The Mexican-origin school item uses Hispanic pupils of any race.
- Physical disorder (litter, dumping, graffiti) is not one of the four items, and this lane did not read the September 18 enclave lane. That lane measured disorder with city inspector audits, 311 data and AHS 2023. It found no Mexican-origin effect at equal income except slight litter, and street feces follow street homelessness [DATA: `enclave_quality_2026_09_18/RESULT.md`].
- This analysis was run by an LLM on a politically charged comparison; see `notes/llm-bias-caveat.md`. The choices that move the Black–Mexican gap most are the offending-share inputs, which come from the repo and FBI data, and κ.

## Files

- Covered, repo:
  - `guard_labor_2026_09_16` (RESULT, regressions, panel);
  - `hedonic_composition_2026_09_19` RESULT (verdict, §1–2);
  - `research/immigration-hedonic-replay-2026-09-19.md`;
  - `school_dilution_2026_09_24` RESULT (verdict and earnings conversion);
  - `naep_saturation_2026_09_28` RESULT;
  - `research/immigration-school-capacity-harms-2026-09-20.md` (head and update);
  - `research/immigration-school-peer-checks-2026-09-20.md` (head) and that lane's `derived/models.csv`;
  - `crime_victim_cost_2026_09_23` (verdict, derived CSVs, tract cache);
  - `black_comparator_rough_2026_09_28` (derived population and victim-cost CSVs).
- Covered, sources: Cohen et al. 2004 (abstract and NIJ summary), CHK (WP full text and AER abstract), HKR w8741, BFM w13236, Cornaglia et al., CRDC 2021-22 First Look (primary PDF, p. 22), FBI 2019 Table 43A, Census SAS via FRED, BLS OES API.
- Skipped:
  - hedonic §3 onward (not needed for the decision);
  - Dolan & Peasgood (paywalled; abstract only);
  - Anderson 1999, Ludwig & Cook 2001, Cullen & Levitt 1999, Hoxby 2000 and Billings–Deming–Rockoff (turn budget; the conclusions above do not rest on them);
  - the 2022 Economic Census API (HTTP 302 without a key; SAS via FRED used instead).

## Reproduce

`items.py` reads `black_comparator_rough_2026_09_28/derived/`; run that lane first (its RESULT has the commands).

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project --with statsmodels python3 infra/immigration-fiscal/social_costs_unpriced_2026_09_28/guard_black.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/social_costs_unpriced_2026_09_28/exposure.py   # reads the key, never prints it
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/social_costs_unpriced_2026_09_28/items.py
```

## Log

- 2026-09-28 18:38:31 JST: stub written; reading repo lanes (guard_labor, hedonic_composition, hedonic replay memo, school memos, school_dilution, naep_saturation, crime_victim_cost).
- 2026-09-28 18:54:28 JST: checkpoint 1 (inputs verified so far).
  - Guard lane Black-share control, rerun of its own OLS spec on its panel.csv (`guard_black.py` → `derived/guard_share_coefficients.csv`; replication check fb_share 0.0196 (0.0070) matches the lane): Black share **+0.0026 pp guard share per pp (SE 0.0027, p = 0.35), all 51**; **+0.0044 (0.0015, p = 0.005) dropping NV/HI/DC**; without the crime control +0.0015 (0.0029) / +0.0041 (0.0016). Hispanic share null throughout (−0.0004 (0.0037); +0.0003 (0.0020)). [CALCULATION]
  - Carrell, Hoekstra & Kuka: one disruptive peer-year costs the 24 classmates $81,000–105,000 PDV (2010 $, CFR $522k at age 12, 3% real; WP w22042 p.22 fn 14–16); AER 2018 version says ~$80,000; per classmate per year 0.6–0.8% of lifetime earnings. [SOURCE: _cache/chk_w22042.pdf; https://faculty.econ.ucdavis.edu/faculty/scarrell/DV_Long-run.pdf]
  - Cohen, Rust, Steen & Tidd 2004 (Criminology 42(1):89–109) WTP per crime, 2000 $: burglary $25k, serious assault $70k, armed robbery $232k, rape/sexual assault $237k, murder $9.7M; "1.5 to 10 times higher than prior estimates of the cost of crime to victims". [SOURCE: https://www.ojp.gov/library/publications/willingness-pay-crime-control-programs]
  - CRDC 2021-22 First Look: 2.4M K-12 pupils (5%) had 1+ out-of-school suspension; Black boys 8% of enrollment / 22% of OSS, Black girls 7% / 13%; Hispanic boys 15% / 16%. [SOURCE: https://www.ed.gov/media/document/2021-22-crdc-first-look-report]
  - Hanushek, Kain & Rivkin (NBER w8741): "racial and ethnic composition has considerably less influence on the achievement gains of whites or Hispanics" than of Black pupils. [SOURCE: _cache/hkr_w8741.pdf p.2]
  - [GAP] Census 2022 EC API for NAICS 5616 returned HTTP 302 without key; BLS OES page blocked to curl (Exa returned the index page only).
- 2026-09-28 19:07:08 JST: exposure (ACS 2020–24 tracts), FBI 2019 Table 43A, SAS revenues via FRED, BLS OES API and BFM Tables 6–7 in; `items.py` run (rc 0); security low set from the controlled guard regression; RESULT written.
- 2026-09-28 19:30:03 JST (lead): the Black population and victim-cost inputs are now read from `black_comparator_rough_2026_09_28/derived/` rather than hard-coded scratch totals. The by-offence split replaces the borrowed Mexican-origin mix. CRDC Figure 12 was read from the primary PDF (Wayback copy; ed.gov 403): Hispanic girls are 14% of enrollment and 8% of out-of-school suspensions. Hispanic shares are set to 29% / 24%, and both groups carry the ±1-point rounding bound. The school envelope is taken over corners. `items.py` rc 0. Central addable: Mexican-origin $9.9bn → $7.9bn (school 0 → −$1.9bn); Black $50.8bn → $51.0bn.
- 2026-09-28 20:20 JST (lead): the operator adopted items 1, 2 and 4 into the totals (decision 2026-09-28-social-items-fear-security-schools). Added a pointer to the enclave lane's disorder measurement, which this lane had missed.

## 2026-10-15 Round-2 corrections

[CALCULATION: mortality_oct15.py → derived/oct15/] The current P7 pairing already uses DOT's uniform $13.7M on every central death. Independently rebuilding its source-frame and boundary-adjusted victim rows gives $37.341853694137 / $41.585449347833bn, with round-2 uniform replacement delta zero at both ends (absolute residual <1e-9bn). The review's positive estimate describes an earlier correction, not a further change to the current P7 baseline.

The new keyed exporter applies the selected basis to every homicide, including unmixed high and envelope high. Both life-year rates use the lane's own primary SHR2024 victim-age distribution and common NVSS2024 period life table. At 0% the paired victim replacements are $38.896305481062 / $43.316551841520bn (deltas +$1.554451786925 / +$1.731102493687bn); at 3% they are $37.626186020798 / $41.902093713299bn (+$0.284332326661 / +$0.316644365466bn). Envelope and standalone rows expose the same basis/rate choices. Fear and private security remain on their existing source account.

The native receipt verifies six primary pins, 56 actual repository source reads/imports, all 27 footing/basis/rate cells, unchanged nonfatal prices, each uniform homicide at $13.7M, and row/age closure. The pairing verifies every native output hash, the frozen P7 source hashes, exact baseline reproduction, union-plus-added closure and the complete six-cell registry. Producers publish files with the receipt last; a partial publication fails hash validation. Gates are explicit failures, not asserts. Conditional scope: fixed v7 sender/offending and recipient exposure keys transported to oct15 fiscal; custody shares remain a modelled residence proxy. This does not reprice v8 crime membership. Root owns the joined environmental/crime registry and final pairing.

Validation: native producer normal run 7.534s, peak physical footprint 2.165GB; seven mortality tests and three pairing/source-contract tests pass. Native rerun IDENTICAL44/44 exit0 (11.431s); social rerun IDENTICAL71/71 exit0 (2.554s). Historical keyed outputs were preserved. No git writes or network calls.

Reproduce from repo root:
```
OPENBLAS_NUM_THREADS=1 GIT_OPTIONAL_LOCKS=0 uv run --no-project python3 infra/immigration-fiscal/crime_victim_cost_2026_09_23/mortality_oct15.py
OPENBLAS_NUM_THREADS=1 GIT_OPTIONAL_LOCKS=0 uv run --no-project python3 infra/immigration-fiscal/social_costs_unpriced_2026_09_28/mortality_oct15.py
uv run --no-project python3 -m pytest infra/immigration-fiscal/crime_victim_cost_2026_09_23/test_mortality_arms.py -q
uv run --no-project python3 -m pytest infra/immigration-fiscal/social_costs_unpriced_2026_09_28/test_mortality_oct15.py -q --import-mode=importlib
```

Log: 2026-10-15 06:01:26 JST (`date`, parent): rerun on corrected v8 (`d1a24d47`): crime IDENTICAL 44/44, social IDENTICAL 71/71, exit 0. The victim rows read no fiscal amount, so every figure above stands. The joint pairing they feed is in `sept24_propagation_2026_09_24/RESULT.md` ($462.163473 / 561.630823bn on the corrected case).
