**Verdict:** The comparator mixed-unit adjustments are computed with the frozen source survivor kernels and exact comparator masks. The lineage control reproduces every part, paired SE and replicate before admitting comparators. [CALCULATION: `adapter.py`; `derived/positive_control.json`]

Income-year 2024, current oct15 comparator ends, personal allocation. Positive adjustments raise the comparator's modeled net cost to other residents and reduce the lineage-minus-comparator gap. These are conditional simulations, not observed removals. [FRAMING-SENSITIVE] [ASSUMPTION]

| Comparator, own count | Bounded low, $bn | Bounded high, $bn | SE low / high, $bn |
|---|---:|---:|---:|
| white | -35.394141 | -17.804446 | 12.075098 / 11.996529 |
| black | -2.333671 | +0.646664 | 2.208058 / 2.237184 |
| white_children | +16.376557 | +26.858428 | 12.016522 / 11.988385 |
| black_children | +5.915975 | +7.956662 | 2.279604 / 2.302179 |

All table numbers: [CALCULATION: `derived/{white,black}_summary.json` `results`]. Set and cash use the same current-year survivor terms; no spousal-pension model is added. Both readings at each endpoint and all component/diagnostic stacks appear in the JSON/CSV outputs. [ASSUMPTION]

## Definitions and populations

A1 whites: civilian (`PRPERTYP==2` or age under 15), non-Hispanic (`PEHSPNON==2`), white alone (`PRDTRACE==1`), native (`PRCITSHP` 1/2/3), with both parents born in US areas (57/60/66/69/73/78). All ages, third-plus definition, own age mix. [DATA: `../white_replacement_2026_09_28/rekey_white.py:68-79`; `rekey_sept29.py:1299`]

Black: civilian, non-Hispanic (`PEHSPNON==2`), Black alone (`PRDTRACE==2`); all ages, generations and birthplaces, own count. [DATA: `../black_comparator_rough_2026_09_28/rekey.py:41-48`; `../white_replacement_2026_09_28/rekey_white.py:76`]

The original union is used to construct row-4 national weights before swapping the group mask. Comparators never inherit the Mexican union's completion, added residual or Hispanic coverage construction. Paired uncertainty retains all signed SDR columns. Ownership is stored in the third source row as a computational slot; no Black generation classification is inferred. [CALCULATION: `adapter.py` `frame`, `membership`]

| Comparator | Own members, records / weighted | Mixed members, records / weighted | Staying civilian nonmembers, records / weighted | Outside biological children, records / weighted |
|---|---:|---:|---:|---:|
| white | 73,873 / 173,053,897.030000 | 9,485 / 19,676,554.770000 | 10,691 / 23,428,384.589073 | 2,866 / 6,120,363.264739 |
| black | 15,057 / 41,954,493.920000 | 1,195 / 3,178,044.430000 | 1,723 / 4,470,165.241207 | 407 / 1,209,135.360000 |
| white_children | 76,731 / 179,163,067.000000 | 11,111 / 23,374,259.600000 | 7,833 / 17,319,214.619073 | 8 / 11,193.294739 |
| black_children | 15,462 / 43,159,582.340000 | 1,504 / 4,049,168.040000 | 1,318 / 3,265,076.821207 | 3 / 5,528.900000 |

Counts: [DATA / CALCULATION: `derived/{white,black}_summary.json` `counts`]. Weighted counts and record counts refer to these civilian masks; noncivilian co-residents are disclosed separately in the JSON.

M6: a biological child outside the comparator definition stays. Biological links (`PEPAR1TYP`/`PEPAR2TYP==1`, under-18 native civilian child outside the mask) are counted with the source's keyed roster function, but do not expand departures. Their taxes/benefits therefore already enter the ordinary survivor solve. The incremental M6 membership change and membership-benefit interaction are exactly zero because both masks are identical. D is zero by the requested no-added-residual rule. [DATA: `../mixed_unit_removal_2026_10_14/membership.py:43-62`] [CALCULATION: `adapter.py` `counts`, `tax`] [ASSUMPTION]

2026-10-15, round 3 (C3 fix 2): `white_children` and `black_children` take one membership rule for all three groups. Members' biological minor children outside the group depart with them and count as members at their own costs: the same source roster rule, now expanding the departure and the own-count population. The survivor solve, health, SNAP and resource kernels run unchanged on the expanded mask. The groups' own-count line targets come from the white lane's rough engine on the same expanded masks (`../white_replacement_2026_09_28/derived/children_targets_oct15.json`, sha256 in `derived/children_targets_source.json`); their lineage side adds the lineage's own 0.336M outside children, outside its latent subset, as a block at their own costs. The rule's change in item 11 is the children group's amount less the current group's. The lineage's item 11 stays the source's; its all-biological federal-tax arm is the source's `M6_all_biological_federal_tax_arm`. Splitting the change by household type would need three more solves per group, because the national pools are not separable by unit; it is not computed. [CALCULATION: `adapter.py` `membership`, `prepare`] [ASSUMPTION]

## Gap changes

| Group / set / population | Current one-sided rough gap, low / high $bn | Both-sided rough gap, low / high $bn | Change, low / high $bn |
|---|---:|---:|---:|
| white / set / own_count | +1121.329632 / +781.412084 | +1156.723773 / +799.216530 | +35.394141 / +17.804446 |
| white / set / lineage_count | +547.478999 / +523.777254 | +556.729754 / +528.430696 | +9.250755 / +4.653442 |
| white / cash / own_count | +703.203691 / +363.286143 | +738.597832 / +381.090589 | +35.394141 / +17.804446 |
| white / cash / lineage_count | +380.581117 / +356.879372 | +389.831872 / +361.532814 | +9.250755 / +4.653442 |
| black / set / own_count | -87.440301 / -75.111983 | -85.106630 / -75.758647 | +2.333671 / -0.646664 |
| black / set / lineage_count | -121.157792 / -114.752340 | -118.641921 / -115.449492 | +2.515871 / -0.697152 |
| black / cash / own_count | -152.322073 / -139.993755 | -149.988402 / -140.640419 | +2.333671 / -0.646664 |
| black / cash / lineage_count | -185.015241 / -178.609789 | -182.499370 / -179.306941 | +2.515871 / -0.697152 |
| white_children / set / own_count | +1020.021915 / +674.256936 | +1003.645359 / +647.398509 | -16.376557 / -26.858428 |
| white_children / set / lineage_count | +521.998710 / +500.068918 | +517.833741 / +493.238145 | -4.164970 / -6.830773 |
| white_children / cash / own_count | +601.761233 / +255.996254 | +585.384676 / +229.137826 | -16.376557 / -26.858428 |
| white_children / cash / lineage_count | +357.458560 / +335.528768 | +353.293591 / +328.697995 | -4.164970 / -6.830773 |
| black_children / set / own_count | -101.166277 / -89.720283 | -107.082252 / -97.676945 | -5.915975 / -7.956662 |
| black_children / set / lineage_count | -126.437414 / -119.288168 | -132.683196 / -127.688403 | -6.245782 / -8.400234 |
| black_children / cash / own_count | -165.838453 / -154.392459 | -171.754427 / -162.349121 | -5.915975 / -7.956662 |
| black_children / cash / lineage_count | -190.366335 / -183.217089 | -196.612116 / -191.617323 | -6.245782 / -8.400234 |

Gap table: [CALCULATION: `derived/gaps.csv`]. These are the base route's gaps: the evaluator's default settings (whole-population mortality, the original status and production rules, no comparator coverage). They are this lane's record of the survivor term, not the comparison central, which is round 3's table in the white lane (`../white_replacement_2026_09_28/RESULT.md`, R3C3: children rule, own coverage, own mortality). Each gap is rough lineage against rough comparator, not the exact case lineage against rough comparator. Both comparisons are supplied in the CSV with explicit names. Population standardization is linear at fixed per-person amounts; it is not a fresh removal of a smaller universe. `item11_paired_se_bn` uses lineage-minus-comparator signed replicate vectors, not SE quadrature. The SE for changing the already one-sided gap is the comparator correction's SE. [CALCULATION: `finalize.py`] [ASSUMPTION]

## Calibration and limitations

Source federal/state/refund kernels retain their national calibration, own-survivor filing status, own IRS cell, actual person flags, residual rules and paired weights. The comparator has no previously booked item 5b, so its subtraction vector is zero. The national source IRS/refund calibration remains conditioned. Unobserved deductions, QBI and care attribution remain source assumptions. [CALCULATION: `adapter.py` `tax`; source `removal.py:273-393`; source `state_tax.py:166-354`] [ASSUMPTION]

M5 uses each comparator's own-count amount from the live comparator evaluator, including state sales/excise pricing and the actual owner-property response. Its relative change uses the source's saving/remittance-adjusted SPM consumption and state-rate/owner-tenure property allocator. The rough comparator baseline uses an income-power household consumption proxy and a property-value proxy; transporting source allocator relative movements to those amounts is an explicit calibration bridge, not equality of raw keys. SNAP/housing retain their reported unit pools. Source model-share declarations are rederived for each mask without changing national totals. [DATA: `../white_replacement_2026_09_28/rekey_white.py:97-119,266-284`; `rekey_sept29.py:973-1068`] [CALCULATION: `derived/comparator_targets.json`; `adapter.py` `declaration_model`] [ASSUMPTION]

Health/takeup/shelter models and prices are the frozen source's. Membership-benefit terms are solved on the comparator departure mask, while M5 SNAP and its baseline interaction cancel exactly. Conditional SDR SEs omit policy, takeup, cost-vintage and calibration uncertainty; the bounded-low/high readings are model scenarios, not confidence limits. Current consumption resources are held rather than responding behaviorally to new taxes or benefits. Source spousal-pension alternatives stay beside the unified reading. [ASSUMPTION]

The LLM-assisted analysis can inherit political framing bias. Executable controls verify implementation and accounting, not the removal counterfactual's causal premises. [INFERENCE]

## Reproduce

From the repository root:
```sh
sh infra/immigration-fiscal/mixed_unit_comparators_2026_10_15/run_all.sh
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/mixed_unit_comparators_2026_10_15 "sh {lane}/run_all.sh"
```

Every process gates its own peak physical footprint through the existing memory-budget helper. Python perf_counter/getrusage receipts append only in ignored `_cache/timing.jsonl`. Source bytes are checked before and after execution; no source/comparator producer lane or Git metadata is edited. [CALCULATION: `adapter.py`; `derived/source_fingerprints.json`]

## Adapter conventions

The child-count table includes every under-18 civilian outside the group with a type-1 biological member parent, regardless of citizenship. The source-native subset is also reported separately in the JSON. Both subsets stay; neither changes departure membership. [CALCULATION: `adapter.py` `counts`] [DATA: `derived/{white,black}_summary.json`]

The comparator full weight is MARSUPWT/100 with its exact live row-4 factors; national federal/refund denominators are recomputed on that column. Source signed SDR columns are unchanged. The source control retains its own pwwgt0 full weight. These conventions keep the comparator own-count gate exact rather than loosening it. [DATA: `derived/comparator_weight_rule.json`] [CALCULATION: `adapter.py` `comparator_weights`, `tax`]

For a new nonfiler claimant, the state adapter aligns a zero-income/dependent before-return, gated to zero booked CPS state tax, with the actual after-return. The added row creates no original income or tax calibration mass; income, dependents, weights and ownership enter only after removal. [CALCULATION: `adapter.py` `state_registry`; `test_adapter.py`]

The white own-count baseline is a linear standardization of the published A1 per-person prices. A fresh natural unscaled MEPS universe uses different prices, recorded separately as `natural_unscaled_universe_cost_bn`; it does not replace that baseline. The comparator M5 amounts are CPS-keyed and are computed at own count before standardizing the adjustment. [DATA: `derived/comparator_targets.json`] [CALCULATION: `adapter.py` `prepare`] [ASSUMPTION]

The exact case-side totals and complete denominator gate against the live JSON at 1e-9; the adopted/cash_set CSV rows gate at their four-decimal rounding tolerance. [CALCULATION: `finalize.py`]
