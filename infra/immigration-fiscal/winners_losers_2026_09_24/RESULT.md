**Verdict:** On adopted v9, stationary financing, the paired social stack and household pooling, 2.7939% / 4.7146% / 8.3071% of other residents are ahead under rules a/b/c; their central annual net is $-505.650039bn. Cohort financing is beside. [MODEL / FRAMING-SENSITIVE; CALCULATION: derived/oct16/p7_net_shares.csv]



# P7 fixes on the frozen adopted v7 account (2026-10-14)



The frozen hybrid reproduces **19.64694897% / 18.74420662%** pooled and **$-341.7338304bn** to today's residents. It remains a labelled calculation record in the original `net_shares.csv`; the new `p7_*` tables carry explicit financing, sharing, population and channel-set tags. [DATA: p7_positive_control.csv; source oracle at 2204a2bc]

The account and its personal specifications 16/11 are held fixed. `identified_union` and `lineage` name the **payer-pool** alternatives for the same live 42.75M fiscal case, not separately recomputed fiscal headlines. The complete social amounts are separately tabulated for the identified 39.71M union and the 42.75M lineage. No frozen main-case file changed. Adding the direct credit to non-member filers changes their resource net while the government's adopted account stays fixed. [ASSUMPTION / DATA: p7_inputs.json]

The social vintage is the adopted-v7 propagation at **c392d356**, copied verbatim to `inputs/social_oct14.json`, pinned by SHA-256. A concurrent unadopted peer refresh changed the working upstream JSON during a preliminary run; it is excluded. Every source pin is checked and within-run drift fails closed. [SOURCE: Git c392d356; DATA: inputs/pins.json]

## One fix at a time



Each dollar delta below compares to the live central hybrid at the **same end, rule and sharing**; the frozen government-account file stays unchanged. Pure financing reassignment has zero all-cohort resource delta, reported separately from its present-resident delta. Changes to the stated distributional claims are material independently. [CALCULATION: p7_net_shares.csv]



| arm | frame | population | financing | level | total_bn | winners_share | winners_share_conditional_se | delta_today_bn | delta_ahead_pp |
|---|---|---|---|---|---|---|---|---|---|
| financing_only | stationary | identified_union | a | low | -361.691 | 15.992% | 0.205pp | -80.068 | -7.393 |
| financing_only | stationary | identified_union | a | high | -494.889 | 4.474% | 0.108pp | -90.553 | -8.928 |
| financing_only | cohort30 | identified_union | a | low | -358.849 | 14.007% | 0.192pp | -77.226 | -9.378 |
| financing_only | cohort30 | identified_union | a | high | -491.206 | 3.292% | 0.098pp | -86.870 | -10.111 |
| financing_only | cohort10 | identified_union | a | low | -360.199 | 14.095% | 0.198pp | -78.576 | -9.290 |
| financing_only | cohort10 | identified_union | a | high | -493.168 | 3.268% | 0.098pp | -88.833 | -10.134 |
| social_coverage_only | hybrid | identified_union | a | low | -355.749 | 19.680% | 0.217pp | -74.125 | -3.705 |
| social_coverage_only | hybrid | identified_union | a | high | -433.773 | 7.257% | 0.132pp | -29.438 | -6.145 |
| crossing_credit_only | hybrid | identified_union | a | low | -276.625 | 23.632% | 0.244pp | 4.999 | 0.247 |
| crossing_credit_only | hybrid | identified_union | a | high | -399.337 | 13.645% | 0.168pp | 4.999 | 0.243 |
| state_wages_only | hybrid | identified_union | a | low | -281.624 | 5.445% | 0.130pp | 0.000 | -17.940 |
| state_wages_only | hybrid | identified_union | a | high | -404.336 | 2.887% | 0.094pp | -0.000 | -10.515 |
| capitalization_only | hybrid | identified_union | a | low | -281.624 | 22.718% | 0.228pp | 0.000 | -0.667 |
| capitalization_only | hybrid | identified_union | a | high | -404.336 | 13.929% | 0.175pp | -0.000 | 0.526 |
| owner_type_only | hybrid | identified_union | a | low | -281.624 | 25.920% | 0.255pp | 0.000 | 2.535 |
| owner_type_only | hybrid | identified_union | a | high | -404.336 | 17.534% | 0.191pp | 0.000 | 4.132 |
| owner_type_broad_only | hybrid | identified_union | a | low | -281.624 | 23.569% | 0.250pp | 0.000 | 0.184 |
| owner_type_broad_only | hybrid | identified_union | a | high | -404.336 | 13.666% | 0.165pp | 0.000 | 0.263 |
| financing_only | stationary | lineage | a | low | -361.691 | 16.054% | 0.204pp | -80.068 | -7.331 |
| financing_only | stationary | lineage | a | high | -494.889 | 4.513% | 0.108pp | -90.553 | -8.889 |
| financing_only | cohort30 | lineage | a | low | -358.704 | 14.061% | 0.194pp | -77.081 | -9.324 |
| financing_only | cohort30 | lineage | a | high | -491.014 | 3.303% | 0.100pp | -86.679 | -10.099 |
| financing_only | cohort10 | lineage | a | low | -360.121 | 14.150% | 0.198pp | -78.497 | -9.235 |
| financing_only | cohort10 | lineage | a | high | -493.073 | 3.293% | 0.099pp | -88.738 | -10.109 |
| social_coverage_only | hybrid | lineage | a | low | -364.140 | 19.147% | 0.216pp | -82.516 | -4.238 |
| social_coverage_only | hybrid | lineage | a | high | -442.294 | 7.046% | 0.132pp | -37.959 | -6.356 |
| crossing_credit_only | hybrid | lineage | a | low | -276.167 | 23.638% | 0.244pp | 5.456 | 0.253 |
| crossing_credit_only | hybrid | lineage | a | high | -398.880 | 13.714% | 0.165pp | 5.456 | 0.312 |
| state_wages_only | hybrid | lineage | a | low | -281.624 | 5.486% | 0.130pp | 0.000 | -17.899 |
| state_wages_only | hybrid | lineage | a | high | -404.336 | 2.932% | 0.095pp | 0.000 | -10.470 |
| capitalization_only | hybrid | lineage | a | low | -281.624 | 22.705% | 0.227pp | -0.000 | -0.680 |
| capitalization_only | hybrid | lineage | a | high | -404.336 | 13.955% | 0.176pp | -0.000 | 0.553 |
| owner_type_only | hybrid | lineage | a | low | -281.624 | 25.907% | 0.255pp | 0.000 | 2.522 |
| owner_type_only | hybrid | lineage | a | high | -404.336 | 17.542% | 0.188pp | -0.000 | 4.140 |
| owner_type_broad_only | hybrid | lineage | a | low | -281.624 | 23.592% | 0.250pp | 0.000 | 0.207 |
| owner_type_broad_only | hybrid | lineage | a | high | -404.336 | 13.715% | 0.165pp | -0.000 | 0.313 |
| payer_pool_only | hybrid | lineage | a | low | -281.624 | 23.387% | 0.244pp | 0.000 | 0.002 |
| payer_pool_only | hybrid | lineage | a | high | -404.336 | 13.458% | 0.163pp | -0.000 | 0.056 |
| financing_only | stationary | identified_union | b | low | -361.691 | 14.175% | 0.211pp | -80.068 | -7.912 |
| financing_only | stationary | identified_union | b | high | -494.889 | 6.904% | 0.137pp | -90.553 | -6.681 |
| financing_only | cohort30 | identified_union | b | low | -358.849 | 14.198% | 0.211pp | -77.226 | -7.889 |
| financing_only | cohort30 | identified_union | b | high | -491.206 | 6.821% | 0.140pp | -86.870 | -6.764 |
| financing_only | cohort10 | identified_union | b | low | -360.199 | 14.127% | 0.213pp | -78.576 | -7.960 |
| financing_only | cohort10 | identified_union | b | high | -493.168 | 6.626% | 0.137pp | -88.833 | -6.959 |
| social_coverage_only | hybrid | identified_union | b | low | -355.749 | 20.195% | 0.235pp | -74.125 | -1.892 |
| social_coverage_only | hybrid | identified_union | b | high | -433.773 | 9.687% | 0.174pp | -29.438 | -3.898 |
| crossing_credit_only | hybrid | identified_union | b | low | -276.625 | 22.314% | 0.237pp | 4.999 | 0.227 |
| crossing_credit_only | hybrid | identified_union | b | high | -399.337 | 13.793% | 0.193pp | 4.999 | 0.208 |
| state_wages_only | hybrid | identified_union | b | low | -281.624 | 9.629% | 0.169pp | 0.000 | -12.458 |
| state_wages_only | hybrid | identified_union | b | high | -404.336 | 3.930% | 0.107pp | 0.000 | -9.654 |
| capitalization_only | hybrid | identified_union | b | low | -281.624 | 21.992% | 0.231pp | 0.000 | -0.095 |
| capitalization_only | hybrid | identified_union | b | high | -404.336 | 12.716% | 0.184pp | 0.000 | -0.869 |
| owner_type_only | hybrid | identified_union | b | low | -281.624 | 24.578% | 0.245pp | 0.000 | 2.490 |
| owner_type_only | hybrid | identified_union | b | high | -404.336 | 17.040% | 0.208pp | 0.000 | 3.456 |
| owner_type_broad_only | hybrid | identified_union | b | low | -281.624 | 22.297% | 0.239pp | 0.000 | 0.209 |
| owner_type_broad_only | hybrid | identified_union | b | high | -404.336 | 13.962% | 0.197pp | 0.000 | 0.377 |
| financing_only | stationary | lineage | b | low | -361.691 | 14.203% | 0.212pp | -80.068 | -7.885 |
| financing_only | stationary | lineage | b | high | -494.889 | 6.911% | 0.137pp | -90.553 | -6.674 |
| financing_only | cohort30 | lineage | b | low | -358.704 | 14.241% | 0.209pp | -77.081 | -7.846 |
| financing_only | cohort30 | lineage | b | high | -491.014 | 6.838% | 0.141pp | -86.679 | -6.747 |
| financing_only | cohort10 | lineage | b | low | -360.121 | 14.117% | 0.214pp | -78.497 | -7.971 |
| financing_only | cohort10 | lineage | b | high | -493.073 | 6.648% | 0.137pp | -88.738 | -6.937 |
| social_coverage_only | hybrid | lineage | b | low | -364.140 | 19.842% | 0.232pp | -82.516 | -2.246 |
| social_coverage_only | hybrid | lineage | b | high | -442.294 | 9.496% | 0.168pp | -37.959 | -4.089 |
| crossing_credit_only | hybrid | lineage | b | low | -276.167 | 22.327% | 0.235pp | 5.456 | 0.239 |
| crossing_credit_only | hybrid | lineage | b | high | -398.880 | 13.827% | 0.193pp | 5.456 | 0.242 |
| state_wages_only | hybrid | lineage | b | low | -281.624 | 9.653% | 0.166pp | -0.000 | -12.435 |
| state_wages_only | hybrid | lineage | b | high | -404.336 | 3.931% | 0.107pp | 0.000 | -9.654 |
| capitalization_only | hybrid | lineage | b | low | -281.624 | 21.997% | 0.232pp | 0.000 | -0.090 |
| capitalization_only | hybrid | lineage | b | high | -404.336 | 12.736% | 0.183pp | 0.000 | -0.849 |
| owner_type_only | hybrid | lineage | b | low | -281.624 | 24.578% | 0.245pp | 0.000 | 2.491 |
| owner_type_only | hybrid | lineage | b | high | -404.336 | 17.074% | 0.209pp | 0.000 | 3.489 |
| owner_type_broad_only | hybrid | lineage | b | low | -281.624 | 22.300% | 0.239pp | 0.000 | 0.212 |
| owner_type_broad_only | hybrid | lineage | b | high | -404.336 | 13.982% | 0.198pp | 0.000 | 0.397 |
| payer_pool_only | hybrid | lineage | b | low | -281.624 | 22.089% | 0.236pp | 0.000 | 0.002 |
| payer_pool_only | hybrid | lineage | b | high | -404.336 | 13.606% | 0.194pp | 0.000 | 0.021 |



The added-descendant-only incidence arm removes precisely the payload's added count from US-born nonmembers whose two parents were born in US areas, proportionally within five-year age bands. Removed weights enter the surrogate member pool at the case's G3+ age records: no weight is discarded. The within-cell state, income and family assignment is unidentified. [ASSUMPTION; DATA: p7_payer_cells.csv]

Crossing credits go to the measured non-member tax-return carriers. The union's gross forward A+C is $4.998683bn (joint SDR SE $0.298167bn); reverse B+Cr is $-0.700138bn. The additional forward $0.457349bn uses item 5b's own G3+ per-member extrapolation, applied to the recovered G3+ gross forward vector; white-priced added people take zero. That additional filer location is an assumption, not observed microdata. [CALCULATION: p7_credits.py, p7_inputs.json; SOURCE: mixed_unit_credits/credits.py]

The identified union's direct filer gain is just below the review's $5bn bar; including the case's added-person extrapolation puts the full-lineage gain above it at both ends. This improves the combined other-resident resource account, not the government's unchanged net budget charge. `all_cohorts_resource_delta_bn` keeps that distinction visible; the parent decides whether to revise the broader headline interpretation. [CALCULATION: p7_net_shares.csv, p7_inputs.json]

## Financing and future cohorts



| population | frame | financing | sharing | total_bn | future_bn | winners_share |
|---|---|---|---|---|---|---|
| identified_union | hybrid | a | person | -341.734 | -85.310 | 17.888% |
| identified_union | hybrid | a | pooled | -341.734 | -85.310 | 19.647% |
| identified_union | stationary | a | person | -427.044 | -0.000 | 12.657% |
| identified_union | stationary | a | pooled | -427.044 | -0.000 | 8.700% |
| identified_union | cohort30 | a | person | -423.782 | -3.263 | 11.448% |
| identified_union | cohort30 | a | pooled | -423.782 | -3.263 | 7.065% |
| identified_union | cohort10 | a | person | -425.438 | -1.606 | 10.895% |
| identified_union | cohort10 | a | pooled | -425.438 | -1.606 | 7.005% |
| lineage | hybrid | a | person | -341.734 | -85.310 | 17.910% |
| lineage | hybrid | a | pooled | -341.734 | -85.310 | 19.657% |
| lineage | stationary | a | person | -427.044 | -0.000 | 12.672% |
| lineage | stationary | a | pooled | -427.044 | -0.000 | 8.740% |
| lineage | cohort30 | a | person | -423.613 | -3.431 | 11.478% |
| lineage | cohort30 | a | pooled | -423.613 | -3.431 | 7.129% |
| lineage | cohort10 | a | person | -425.351 | -1.693 | 10.912% |
| lineage | cohort10 | a | pooled | -425.351 | -1.693 | 7.061% |
| identified_union | hybrid | b | person | -341.734 | -85.310 | 18.044% |
| identified_union | hybrid | b | pooled | -341.734 | -85.310 | 18.744% |
| identified_union | stationary | b | person | -427.044 | -0.000 | 12.190% |
| identified_union | stationary | b | pooled | -427.044 | -0.000 | 10.131% |
| identified_union | cohort30 | b | person | -423.782 | -3.263 | 11.849% |
| identified_union | cohort30 | b | pooled | -423.782 | -3.263 | 10.069% |
| identified_union | cohort10 | b | person | -425.438 | -1.606 | 11.358% |
| identified_union | cohort10 | b | pooled | -425.438 | -1.606 | 9.905% |
| lineage | hybrid | b | person | -341.734 | -85.310 | 18.063% |
| lineage | hybrid | b | pooled | -341.734 | -85.310 | 18.758% |
| lineage | stationary | b | person | -427.044 | -0.000 | 12.196% |
| lineage | stationary | b | pooled | -427.044 | -0.000 | 10.134% |
| lineage | cohort30 | b | person | -423.613 | -3.431 | 11.859% |
| lineage | cohort30 | b | pooled | -423.613 | -3.431 | 10.094% |
| lineage | cohort10 | b | person | -425.351 | -1.693 | 11.375% |
| lineage | cohort10 | b | pooled | -425.351 | -1.693 | 9.909% |
| identified_union | hybrid | c | person | -341.734 | -85.310 | 22.989% |
| identified_union | hybrid | c | pooled | -341.734 | -85.310 | 24.019% |
| identified_union | stationary | c | person | -427.044 | -0.000 | 20.802% |
| identified_union | stationary | c | pooled | -427.044 | -0.000 | 18.483% |
| identified_union | cohort30 | c | person | -423.782 | -3.263 | 19.066% |
| identified_union | cohort30 | c | pooled | -423.782 | -3.263 | 16.734% |
| identified_union | cohort10 | c | person | -425.438 | -1.606 | 18.691% |
| identified_union | cohort10 | c | pooled | -425.438 | -1.606 | 16.691% |
| lineage | hybrid | c | person | -341.734 | -85.310 | 23.029% |
| lineage | hybrid | c | pooled | -341.734 | -85.310 | 24.000% |
| lineage | stationary | c | person | -427.044 | -0.000 | 20.846% |
| lineage | stationary | c | pooled | -427.044 | -0.000 | 18.471% |
| lineage | cohort30 | c | person | -423.613 | -3.431 | 19.114% |
| lineage | cohort30 | c | pooled | -423.613 | -3.431 | 16.762% |
| lineage | cohort10 | c | person | -425.351 | -1.693 | 18.740% |
| lineage | cohort10 | c | pooled | -425.351 | -1.693 | 16.719% |



Stationary assigns all accrual and borrowing to current keys. Cohort10/30 move the **whole trust block** together: current payroll receipts, current OASDI/Part A benefits and the net pension increment. The non-trust borrowing part uses projected federal-tax shares over the 10/30-year service windows. Each component is conserved between living and future cohorts. [CALCULATION: p7_inputs.cjs, p7_cohorts.py]

The cohort projection is **[DEGRADED]**, with these explicit proxies:



- [DEGRADED] SSA-area broad-age population growth applied to the other-resident CPS frame; future age/sex composition held at 2024 within broad bands.

- [DEGRADED] Future beneficiary cuts use SS retirement exposure from attained-age/sex cross-sectional benefits; no separate DI/child/survivor timing or specific legislative counterfactual.

- [DEGRADED] Worker payout timing uses medium single workers, entry 21, retirement 65; target FICA weights proxy accrual shares; HI fraction is explicit caller input (default 0.25).

- [DEGRADED] Living denominator is floored at closed-cohort exposure where coarse projected composition undershoots; every floor is recorded in year table.

- [ASSUMPTION] Borrowing service equal amounts in 2025–2034 / 2025–2054; federal income tax plus FICA age-sex profile proxies future federal taxes, with 2024 real profile fixed.

- [ASSUMPTION] NVSS 2024 sex survival with 2026 Trustees improvements; CPS topcoded ages treated as reported; age-profile means constant beyond last observed cell until age 100.

- [ASSUMPTION] Whole signed trust block uses one common payout-year incidence key; payroll/cash/accrual cannot be credited or charged to inconsistent cohorts.

- [DEGRADED] Payouts after 2100 are assigned wholly to future cohorts/arrivals; tail mass reported.



Rule (c) allocates cuts by receipt of the responding programmes, valued at their national budgets and responses. Cash and SPM noncash receipts are survey fields; health enrollment and school age/enrollment proxy their receipt. The education budget is split at the case's BEA K12 weight; college receipt uses A_ENRLW=1 and A_HSCOL=2 (CPS universe16–24), so older student receipt and public/private type are unidentified and this key is explicitly a proxy. Programmes without a CPS person receipt use a declared universal service key. It is an allocation assumption, not an observed policy experiment. [DATA: p7_programme_receipt_keys.csv; CALCULATION: p7_inputs.cjs → responding_programme_key]

## Sharing rules are sensitivities, never bounds



| financing | sharing | winners_share | total_bn |
|---|---|---|---|
| a | person | 9.829% | -483.072 |
| a | pooled | 4.633% | -483.072 |
| a | retains_0.5 | 5.822% | -483.072 |
| a | retains_0.8 | 8.192% | -483.072 |
| a | mixed_unit | 6.264% | -378.105 |
| b | person | 10.322% | -483.072 |
| b | pooled | 8.399% | -483.072 |
| b | retains_0.5 | 8.613% | -483.072 |
| b | retains_0.8 | 9.376% | -483.072 |
| b | mixed_unit | 9.986% | -376.701 |
| c | person | 17.690% | -483.072 |
| c | pooled | 14.741% | -483.072 |
| c | retains_0.5 | 14.756% | -483.072 |
| c | retains_0.8 | 14.790% | -483.072 |
| c | mixed_unit | 16.230% | -377.683 |



For s=0.5/0.8 the earner retains s of their own wage change and transfers the remainder to other unit members, conserving weighted dollars in each unit. All other net channels are pooled. Singletons retain everything. The two-person counterexample (wages 100/0, shared taxes 40/40) gives person 60/−40, pooled 10/10, and retaining 20% gives −20/40: an individual's sign can lie outside both endpoint signs. A separate aggregate control with two units, net wages (100,−1) and (8,−10), puts 50% ahead under both endpoints but 75% under s=0.8. Counts themselves also need not be bounded. [CALCULATION: test_p7_frames.py]

The mixed-unit arm includes members' personal cash income net of their own income taxes and FICA plus per-capita SPM noncash benefits. It shares those resources with the other residents of their units, conserving the combined total and reporting both sides of the boundary. It is a resources sensitivity; bargaining, refiling, wage adjustment and member departure behavior are unmeasured. The all-group units remain in the conservation check. [ASSUMPTION; DATA: p7_mixed_reconciliation.csv]

## Geography, ownership and claims



| arm | financing | cut | group | persons_m | mean_usd | winners_share |
|---|---|---|---|---|---|---|
| recommended | a | edu_nativity | ba_plus / other_foreign_born | 16.879 | -2198.7 | 7.423% |
| recommended | a | edu_nativity | ba_plus / us_born | 69.935 | -1790.4 | 8.269% |
| recommended | a | edu_nativity | below_high_school / other_foreign_born | 4.558 | -1935.5 | 0.675% |
| recommended | a | edu_nativity | below_high_school / us_born | 8.468 | -1424.8 | 1.200% |
| recommended | a | edu_nativity | high_school / other_foreign_born | 8.153 | -2295.6 | 1.335% |
| recommended | a | edu_nativity | high_school / us_born | 47.837 | -2016.4 | 1.570% |
| recommended | a | edu_nativity | some_college / other_foreign_born | 5.461 | -1665.2 | 4.675% |
| recommended | a | edu_nativity | some_college / us_born | 47.009 | -1345.3 | 4.737% |
| recommended | a | edu_nativity | under_25 | 84.491 | -1329.7 | 3.616% |
| recommended | a | tenure | landlord | 24.293 | -1160.4 | 25.653% |
| recommended | a | tenure | owner_no_rental_income | 182.667 | -1563.7 | 3.667% |
| recommended | a | tenure | renter | 85.831 | -1971.9 | 0.739% |
| recommended | a | state3 | CA | 26.104 | -4623.9 | 1.929% |
| recommended | a | state3 | TX | 21.008 | -4314.1 | 1.353% |
| recommended | a | state3 | rest | 245.679 | -1106.1 | 5.201% |
| recommended_state_wages | a | edu_nativity | ba_plus / other_foreign_born | 16.879 | -2175.6 | 3.051% |
| recommended_state_wages | a | edu_nativity | ba_plus / us_born | 69.935 | -1779.1 | 2.969% |
| recommended_state_wages | a | edu_nativity | below_high_school / other_foreign_born | 4.558 | -2039.7 | 0.917% |
| recommended_state_wages | a | edu_nativity | below_high_school / us_born | 8.468 | -1388.8 | 1.041% |
| recommended_state_wages | a | edu_nativity | high_school / other_foreign_born | 8.153 | -2321.7 | 1.512% |
| recommended_state_wages | a | edu_nativity | high_school / us_born | 47.837 | -2036.2 | 1.516% |
| recommended_state_wages | a | edu_nativity | some_college / other_foreign_born | 5.461 | -1661.3 | 1.941% |
| recommended_state_wages | a | edu_nativity | some_college / us_born | 47.009 | -1356.8 | 2.212% |
| recommended_state_wages | a | edu_nativity | under_25 | 84.491 | -1321.8 | 1.155% |
| recommended_state_wages | a | tenure | landlord | 24.293 | -1090.7 | 18.666% |
| recommended_state_wages | a | tenure | owner_no_rental_income | 182.667 | -1562.3 | 0.470% |
| recommended_state_wages | a | tenure | renter | 85.831 | -1994.6 | 0.346% |
| recommended_state_wages | a | state3 | CA | 26.104 | -4698.9 | 2.378% |
| recommended_state_wages | a | state3 | TX | 21.008 | -4321.2 | 1.720% |
| recommended_state_wages | a | state3 | rest | 245.679 | -1097.5 | 1.917% |
| recommended_capitalization | a | edu_nativity | ba_plus / other_foreign_born | 16.879 | -1948.5 | 7.909% |
| recommended_capitalization | a | edu_nativity | ba_plus / us_born | 69.935 | -1608.9 | 8.460% |
| recommended_capitalization | a | edu_nativity | below_high_school / other_foreign_born | 4.558 | -1995.5 | 0.626% |
| recommended_capitalization | a | edu_nativity | below_high_school / us_born | 8.468 | -1549.2 | 1.161% |
| recommended_capitalization | a | edu_nativity | high_school / other_foreign_born | 8.153 | -2307.9 | 1.089% |
| recommended_capitalization | a | edu_nativity | high_school / us_born | 47.837 | -2076.1 | 1.435% |
| recommended_capitalization | a | edu_nativity | some_college / other_foreign_born | 5.461 | -1683.2 | 4.035% |
| recommended_capitalization | a | edu_nativity | some_college / us_born | 47.009 | -1439.9 | 4.639% |
| recommended_capitalization | a | edu_nativity | under_25 | 84.491 | -1425.4 | 3.318% |
| recommended_capitalization | a | tenure | landlord | 24.293 | -1077.9 | 24.800% |
| recommended_capitalization | a | tenure | owner_no_rental_income | 182.667 | -1899.7 | 3.199% |
| recommended_capitalization | a | tenure | renter | 85.831 | -1280.0 | 1.736% |
| recommended_capitalization | a | state3 | CA | 26.104 | -4623.9 | 1.757% |
| recommended_capitalization | a | state3 | TX | 21.008 | -4314.1 | 1.130% |
| recommended_capitalization | a | state3 | rest | 245.679 | -1106.1 | 5.154% |
| stack | a | edu_nativity | ba_plus / other_foreign_born | 16.879 | -1937.9 | 3.536% |
| stack | a | edu_nativity | ba_plus / us_born | 69.935 | -1585.5 | 4.473% |
| stack | a | edu_nativity | below_high_school / other_foreign_born | 4.558 | -2097.9 | 0.816% |
| stack | a | edu_nativity | below_high_school / us_born | 8.468 | -1533.6 | 0.947% |
| stack | a | edu_nativity | high_school / other_foreign_born | 8.153 | -2344.4 | 1.065% |
| stack | a | edu_nativity | high_school / us_born | 47.837 | -2106.0 | 1.317% |
| stack | a | edu_nativity | some_college / other_foreign_born | 5.461 | -1713.6 | 2.169% |
| stack | a | edu_nativity | some_college / us_born | 47.009 | -1456.1 | 2.157% |
| stack | a | edu_nativity | under_25 | 84.491 | -1411.6 | 1.136% |
| stack | a | tenure | landlord | 24.293 | -1650.2 | 12.631% |
| stack | a | tenure | owner_no_rental_income | 182.667 | -1825.6 | 0.827% |
| stack | a | tenure | renter | 85.831 | -1275.9 | 2.414% |
| stack | a | state3 | CA | 26.104 | -4861.5 | 4.608% |
| stack | a | state3 | TX | 21.008 | -4399.5 | 3.144% |
| stack | a | state3 | rest | 245.679 | -1073.5 | 1.949% |
| recommended | b | edu_nativity | ba_plus / other_foreign_born | 16.879 | -1573.5 | 16.661% |
| recommended | b | edu_nativity | ba_plus / us_born | 69.935 | -1064.4 | 18.029% |
| recommended | b | edu_nativity | below_high_school / other_foreign_born | 4.558 | -2732.4 | 0.792% |
| recommended | b | edu_nativity | below_high_school / us_born | 8.468 | -1969.4 | 1.110% |
| recommended | b | edu_nativity | high_school / other_foreign_born | 8.153 | -2749.3 | 1.511% |
| recommended | b | edu_nativity | high_school / us_born | 47.837 | -2288.7 | 1.690% |
| recommended | b | edu_nativity | some_college / other_foreign_born | 5.461 | -1888.2 | 5.399% |
| recommended | b | edu_nativity | some_college / us_born | 47.009 | -1507.2 | 6.491% |
| recommended | b | edu_nativity | under_25 | 84.491 | -1655.6 | 5.638% |
| recommended | b | tenure | landlord | 24.293 | -0.5 | 32.881% |
| recommended | b | tenure | owner_no_rental_income | 182.667 | -1537.3 | 8.060% |
| recommended | b | tenure | renter | 85.831 | -2356.4 | 2.193% |
| recommended | b | state3 | CA | 26.104 | -4481.0 | 2.690% |
| recommended | b | state3 | TX | 21.008 | -4285.2 | 1.958% |
| recommended | b | state3 | rest | 245.679 | -1123.7 | 9.557% |
| recommended_state_wages | b | edu_nativity | ba_plus / other_foreign_born | 16.879 | -1550.4 | 6.463% |
| recommended_state_wages | b | edu_nativity | ba_plus / us_born | 69.935 | -1053.1 | 7.215% |
| recommended_state_wages | b | edu_nativity | below_high_school / other_foreign_born | 4.558 | -2836.6 | 0.745% |
| recommended_state_wages | b | edu_nativity | below_high_school / us_born | 8.468 | -1933.4 | 1.170% |
| recommended_state_wages | b | edu_nativity | high_school / other_foreign_born | 8.153 | -2775.4 | 1.310% |
| recommended_state_wages | b | edu_nativity | high_school / us_born | 47.837 | -2308.5 | 1.514% |
| recommended_state_wages | b | edu_nativity | some_college / other_foreign_born | 5.461 | -1884.3 | 2.489% |
| recommended_state_wages | b | edu_nativity | some_college / us_born | 47.009 | -1518.6 | 2.887% |
| recommended_state_wages | b | edu_nativity | under_25 | 84.491 | -1647.7 | 1.971% |
| recommended_state_wages | b | tenure | landlord | 24.293 | 69.2 | 26.263% |
| recommended_state_wages | b | tenure | owner_no_rental_income | 182.667 | -1535.9 | 1.799% |
| recommended_state_wages | b | tenure | renter | 85.831 | -2379.0 | 0.691% |
| recommended_state_wages | b | state3 | CA | 26.104 | -4556.0 | 6.688% |
| recommended_state_wages | b | state3 | TX | 21.008 | -4292.3 | 5.428% |
| recommended_state_wages | b | state3 | rest | 245.679 | -1115.1 | 3.001% |
| recommended_capitalization | b | edu_nativity | ba_plus / other_foreign_born | 16.879 | -1725.0 | 14.799% |
| recommended_capitalization | b | edu_nativity | ba_plus / us_born | 69.935 | -1318.0 | 15.693% |
| recommended_capitalization | b | edu_nativity | below_high_school / other_foreign_born | 4.558 | -2240.4 | 0.756% |
| recommended_capitalization | b | edu_nativity | below_high_school / us_born | 8.468 | -1791.3 | 1.179% |
| recommended_capitalization | b | edu_nativity | high_school / other_foreign_born | 8.153 | -2441.0 | 1.235% |
| recommended_capitalization | b | edu_nativity | high_school / us_born | 47.837 | -2199.5 | 1.582% |
| recommended_capitalization | b | edu_nativity | some_college / other_foreign_born | 5.461 | -1763.0 | 4.690% |
| recommended_capitalization | b | edu_nativity | some_college / us_born | 47.009 | -1516.5 | 5.689% |
| recommended_capitalization | b | edu_nativity | under_25 | 84.491 | -1542.9 | 4.634% |
| recommended_capitalization | b | tenure | landlord | 24.293 | -641.4 | 29.138% |
| recommended_capitalization | b | tenure | owner_no_rental_income | 182.667 | -1892.4 | 5.974% |
| recommended_capitalization | b | tenure | renter | 85.831 | -1419.3 | 3.867% |
| recommended_capitalization | b | state3 | CA | 26.104 | -4481.0 | 2.093% |
| recommended_capitalization | b | state3 | TX | 21.008 | -4285.2 | 1.445% |
| recommended_capitalization | b | state3 | rest | 245.679 | -1123.7 | 8.328% |
| stack | b | edu_nativity | ba_plus / other_foreign_born | 16.879 | -1714.4 | 6.142% |
| stack | b | edu_nativity | ba_plus / us_born | 69.935 | -1294.5 | 7.753% |
| stack | b | edu_nativity | below_high_school / other_foreign_born | 4.558 | -2342.8 | 0.677% |
| stack | b | edu_nativity | below_high_school / us_born | 8.468 | -1775.7 | 1.047% |
| stack | b | edu_nativity | high_school / other_foreign_born | 8.153 | -2477.5 | 1.160% |
| stack | b | edu_nativity | high_school / us_born | 47.837 | -2229.4 | 1.452% |
| stack | b | edu_nativity | some_college / other_foreign_born | 5.461 | -1793.3 | 2.355% |
| stack | b | edu_nativity | some_college / us_born | 47.009 | -1532.8 | 2.837% |
| stack | b | edu_nativity | under_25 | 84.491 | -1529.1 | 1.485% |
| stack | b | tenure | landlord | 24.293 | -1213.7 | 16.819% |
| stack | b | tenure | owner_no_rental_income | 182.667 | -1818.2 | 1.812% |
| stack | b | tenure | renter | 85.831 | -1415.2 | 3.134% |
| stack | b | state3 | CA | 26.104 | -4718.6 | 5.629% |
| stack | b | state3 | TX | 21.008 | -4370.5 | 3.491% |
| stack | b | state3 | rest | 245.679 | -1091.2 | 3.208% |



State wage incidence conserves every nativity/skill cell's national gross gain/loss at 1e-9bn; group skill-cell earnings locate the state shock, then other workers' own earnings allocate it. This is a geographic incidence arm, not a local-labor-market equilibrium solve. Capitalization puts the state/local burden on owners using ACS state × income property-value margins mapped to CPS owner cells. Renters bear no direct capitalization charge; the separate rent channel remains. [ASSUMPTION; CALCULATION: p7_state_wage_cells.csv, property_key]

Reported RHFS rental-unit owner shares proxy rent-receipt shares. Individuals are identified, corporation/REIT ownership is identified, and LLC/partnership/trust/other ownership remains unresolved. The two ownership arms assign that residual either through capital income or individual landlords; both preserve each matching geography's gross landlord dollars and the housing net. No interpretation makes an LLC automatically a corporate/REIT owner. [DATA: inputs_rhfs.csv; p7_owner_types_*.csv, p7_inputs.json]

## Complete social rows and exclusions



| item | low_bn | central_bn | high_bn | key |
|---|---|---|---|---|
| victims | -32.626396 | -33.302789 | -33.979181 | live total on existing crime_victims incidence |
| property_crime | -1.342564 | -1.394312 | -1.446059 | live total on existing property_crime incidence |
| unreimbursed_care | -3.310305 | -4.488684 | -5.667063 | live total on existing unreimbursed_care incidence |
| congestion | -14.663600 | -13.593610 | -12.523620 | live total on existing congestion incidence |
| housing_gain | 3.651977 | 2.196137 | 0.740298 | gross renter/landlord arrays, live central metro-local at low; national-uniform at high |
| fear_avoidance | -11.066272 | -11.044307 | -11.022342 | crime victim risk within group states |
| private_security | 0.525136 | 0.524094 | 0.523051 | crime victim risk within group states; signed net may be a benefit |
| school_disruption | 2.145917 | 2.145917 | 2.145917 | ages 5-17 in group states; school type unavailable |
| pm25_consumption | -74.182132 | -74.182132 | -74.182132 | 35% local group-state resident exposure, 65% national residents; assumed dispersion |
| road_crash_externality | -11.365389 | -11.365389 | -11.365389 | state group vehicle-minutes by urban area, receiving metro workers; driving proxy |
| scale_net_earnings | 14.721034 | 14.721034 | 14.721034 | earnings by scale-lane metro states plus induced receipts by financing rule |
| restaurant_variety_market_size | 6.793000 | 6.793000 | 6.793000 | SPM resources within group states, consumption proxy |
| formal_volunteering_outside_group | 6.352761 | 6.352761 | 6.352761 | all other residents nationally; beneficiary location unobserved |
| total_consumer_scale | 2.320176 | 2.320176 | 2.320176 | national SPM resources, consumption proxy |
| total_trade_travel_fdi | 7.391170 | 7.391170 | 7.391170 | national SPM resources, consumption proxy |
| source_rounding | -0.000000 | -0.000001 | -0.000001 | national persons; explicit serialized source-row rounding |



All 15 adopted live social rows are allocated, plus an explicit source-rounding row of at most $1,000 that reconciles the source's separately rounded aggregate. The legacy mobility row is supplemental and not in this adopted channel set. Fear/security use crime-risk keys; schools use group state pupil shares; pollution uses the source's local fraction plus national dispersion; crashes use urban vehicle exposure. Volunteering and trade/consumer-scale rows use national beneficiary/consumption keys where their location is unobserved. Every key is an incidence proxy. [DATA: p7_channel_coverage.csv; p7_excluded_channels.csv]

The low source social rows use the equal/raw-coded crime footing and the high use custody, while the frozen main-case fiscal band uses custody at both ends. These incidence sums are therefore explicit allocation scenarios, not a claim to reproduce the published paired total. Each source row and its population is preserved; the mismatch is not hidden by a total label. [DATA: inputs/social_oct14.json lineage_social_rows.keys]

## Dollar extrema and share extrema



| extreme | financing | level | wage_geography | capitalization | housing_level | sharing | persons_m | total_bn | winners_share | losers_share | mean_usd |
|---|---|---|---|---|---|---|---|---|---|---|---|
| share_minimum | a | high | state | False | central | person | 292.7915093 | -524.624 | 1.542% | 0.9845808576 | -1791.801709 |
| share_maximum | a | low | national | True | central | person | 292.7915093 | -438.896 | 14.937% | 0.8506326957 | -1499.004778 |
| dollar_minimum | a | high | national | True | low | person | 292.7915093 | -528.511 | 6.055% | 0.9394486006 | -1805.076768 |
| dollar_maximum | a | low | national | False | high | person | 292.7915093 | -433.000 | 14.527% | 0.8547339558 | -1478.866841 |
| share_minimum | a | high | state | False | central | pooled | 292.7915093 | -524.624 | 1.220% | 0.9877997344 | -1791.801709 |
| share_maximum | a | low | national | True | central | pooled | 292.7915093 | -438.896 | 12.186% | 0.8781386571 | -1499.004778 |
| dollar_minimum | a | high | national | True | low | pooled | 292.7915093 | -528.511 | 2.676% | 0.9732436025 | -1805.076768 |
| dollar_maximum | a | low | state | True | high | pooled | 292.7915093 | -433.000 | 2.839% | 0.9716081177 | -1478.866841 |
| share_minimum | b | high | state | True | central | person | 292.7915093 | -524.624 | 2.149% | 0.9785125873 | -1791.801709 |
| share_maximum | b | low | national | False | high | person | 292.7915093 | -433.000 | 14.549% | 0.8545096449 | -1478.866841 |
| dollar_minimum | b | high | national | False | low | person | 292.7915093 | -528.511 | 7.280% | 0.9272018564 | -1805.076768 |
| dollar_maximum | b | low | state | False | high | person | 292.7915093 | -433.000 | 5.717% | 0.9428347725 | -1478.866841 |
| share_minimum | b | high | state | True | central | pooled | 292.7915093 | -524.624 | 1.744% | 0.9825594825 | -1791.801709 |
| share_maximum | b | low | national | False | high | pooled | 292.7915093 | -433.000 | 13.078% | 0.8692215158 | -1478.866841 |
| dollar_minimum | b | high | national | False | low | pooled | 292.7915093 | -528.511 | 5.784% | 0.9421645158 | -1805.076768 |
| dollar_maximum | b | low | national | False | high | pooled | 292.7915093 | -433.000 | 13.078% | 0.8692215158 | -1478.866841 |
| share_minimum | c | high | state | True | central | person | 292.7915093 | -524.624 | 2.831% | 0.9716854412 | -1791.801709 |
| share_maximum | c | low | national | False | high | person | 292.7915093 | -433.000 | 20.553% | 0.7944749155 | -1478.866841 |
| dollar_minimum | c | high | national | False | low | person | 292.7915093 | -528.511 | 14.327% | 0.8567341744 | -1805.076768 |
| dollar_maximum | c | low | state | True | high | person | 292.7915093 | -433.000 | 6.116% | 0.9388352353 | -1478.866841 |
| share_minimum | c | high | state | True | central | pooled | 292.7915093 | -524.624 | 2.108% | 0.9789244023 | -1791.801709 |
| share_maximum | c | low | national | False | high | pooled | 292.7915093 | -433.000 | 18.899% | 0.8110121223 | -1478.866841 |
| dollar_minimum | c | high | national | False | low | pooled | 292.7915093 | -528.511 | 10.853% | 0.8914694884 | -1805.076768 |
| dollar_maximum | c | low | state | False | high | pooled | 292.7915093 | -433.000 | 8.696% | 0.9130385606 | -1478.866841 |



The enumerated grid has 2 fiscal ends × 2 wage incidences × 2 capitalization arms × 3 coherent housing levels, for each rule and person/pooled sharing. Nonhousing social rows follow the selected fiscal case end at their central model settings, including the matched source crime footing; credit rules are fixed. The reported share minimum/maximum are over this finite declared grid, not universal bounds on household outcomes or all uncertain social parameters. [CALCULATION: p7_enumerated_grid.csv]

## Literature within-cell substitution and skill split



| base_arm | epsilon | financing | level | total_bn | winners_share | winners_share_conditional_se | delta_vs_infinite_bn | delta_vs_infinite_ahead_pp |
|---|---|---|---|---|---|---|---|---|
| nest_recommended | infinite | a | low | -438.751473 | 11.082209% | 0.161789pp | 0.000000 | 0.000000 |
| nest_recommended | infinite | a | central | -483.071540 | 4.632925% | 0.103491pp | 0.000000 | 0.000000 |
| nest_recommended | infinite | a | high | -527.391608 | 2.329404% | 0.078289pp | 0.000000 | 0.000000 |
| nest_recommended | eps8.7 | a | low | -435.027003 | 11.505342% | 0.157620pp | 3.724470 | 0.423133 |
| nest_recommended | eps8.7 | a | central | -479.984293 | 4.846897% | 0.108995pp | 3.087247 | 0.213972 |
| nest_recommended | eps8.7 | a | high | -524.941583 | 2.386283% | 0.080381pp | 2.450025 | 0.056878 |
| nest_recommended | eps17.9 | a | low | -436.948189 | 11.280114% | 0.161305pp | 1.803284 | 0.197905 |
| nest_recommended | eps17.9 | a | central | -481.576781 | 4.751955% | 0.103711pp | 1.494759 | 0.119030 |
| nest_recommended | eps17.9 | a | high | -526.205374 | 2.348894% | 0.078839pp | 1.186234 | 0.019490 |
| nest_stack | infinite | a | low | -438.751473 | 2.976538% | 0.090955pp | 0.000000 | 0.000000 |
| nest_stack | infinite | a | central | -483.071540 | 2.271575% | 0.082740pp | 0.000000 | 0.000000 |
| nest_stack | infinite | a | high | -527.391608 | 1.907702% | 0.075126pp | 0.000000 | 0.000000 |
| nest_stack | eps8.7 | a | low | -435.027003 | 3.037720% | 0.091633pp | 3.724470 | 0.061182 |
| nest_stack | eps8.7 | a | central | -479.984293 | 2.318726% | 0.084492pp | 3.087247 | 0.047151 |
| nest_stack | eps8.7 | a | high | -524.941583 | 1.911666% | 0.076269pp | 2.450025 | 0.003964 |
| nest_stack | eps17.9 | a | low | -436.948189 | 3.022998% | 0.091321pp | 1.803284 | 0.046460 |
| nest_stack | eps17.9 | a | central | -481.576781 | 2.310516% | 0.084487pp | 1.494759 | 0.038941 |
| nest_stack | eps17.9 | a | high | -526.205374 | 1.907651% | 0.075133pp | 1.186234 | -0.000051 |
| nest_recommended | infinite | b | low | -438.751473 | 12.728445% | 0.191953pp | 0.000000 | 0.000000 |
| nest_recommended | infinite | b | central | -483.071540 | 8.399225% | 0.161376pp | 0.000000 | 0.000000 |
| nest_recommended | infinite | b | high | -527.391608 | 5.453652% | 0.123122pp | 0.000000 | 0.000000 |
| nest_recommended | eps8.7 | b | low | -435.027003 | 13.004636% | 0.198199pp | 3.724470 | 0.276191 |
| nest_recommended | eps8.7 | b | central | -479.984293 | 8.615776% | 0.164149pp | 3.087247 | 0.216552 |
| nest_recommended | eps8.7 | b | high | -524.941583 | 5.576079% | 0.120956pp | 2.450025 | 0.122427 |
| nest_recommended | eps17.9 | b | low | -436.948189 | 12.810510% | 0.194183pp | 1.803284 | 0.082065 |
| nest_recommended | eps17.9 | b | central | -481.576781 | 8.496720% | 0.162948pp | 1.494759 | 0.097495 |
| nest_recommended | eps17.9 | b | high | -526.205374 | 5.523616% | 0.123582pp | 1.186234 | 0.069963 |
| nest_stack | infinite | b | low | -438.751473 | 4.624418% | 0.110352pp | 0.000000 | 0.000000 |
| nest_stack | infinite | b | central | -483.071540 | 3.444365% | 0.099936pp | 0.000000 | 0.000000 |
| nest_stack | infinite | b | high | -527.391608 | 2.818167% | 0.088100pp | 0.000000 | 0.000000 |
| nest_stack | eps8.7 | b | low | -435.027003 | 4.702354% | 0.111721pp | 3.724470 | 0.077936 |
| nest_stack | eps8.7 | b | central | -479.984293 | 3.485513% | 0.101933pp | 3.087247 | 0.041148 |
| nest_stack | eps8.7 | b | high | -524.941583 | 2.867164% | 0.089086pp | 2.450025 | 0.048997 |
| nest_stack | eps17.9 | b | low | -436.948189 | 4.671696% | 0.110583pp | 1.803284 | 0.047278 |
| nest_stack | eps17.9 | b | central | -481.576781 | 3.465894% | 0.100561pp | 1.494759 | 0.021529 |
| nest_stack | eps17.9 | b | high | -526.205374 | 2.851616% | 0.089406pp | 1.186234 | 0.033448 |
| nest_recommended | infinite | c | low | -438.751473 | 18.809222% | 0.225405pp | 0.000000 | 0.000000 |
| nest_recommended | infinite | c | central | -483.071540 | 14.741259% | 0.209569pp | 0.000000 | 0.000000 |
| nest_recommended | infinite | c | high | -527.391608 | 10.760987% | 0.175469pp | 0.000000 | 0.000000 |
| nest_recommended | eps8.7 | c | low | -435.027003 | 19.019857% | 0.227606pp | 3.724470 | 0.210635 |
| nest_recommended | eps8.7 | c | central | -479.984293 | 14.922451% | 0.212845pp | 3.087247 | 0.181191 |
| nest_recommended | eps8.7 | c | high | -524.941583 | 10.922777% | 0.176081pp | 2.450025 | 0.161790 |
| nest_recommended | eps17.9 | c | low | -436.948189 | 18.890204% | 0.228498pp | 1.803284 | 0.080982 |
| nest_recommended | eps17.9 | c | central | -481.576781 | 14.838385% | 0.211878pp | 1.494759 | 0.097125 |
| nest_recommended | eps17.9 | c | high | -526.205374 | 10.842920% | 0.173567pp | 1.186234 | 0.081933 |
| nest_stack | infinite | c | low | -438.751473 | 5.811448% | 0.127753pp | 0.000000 | 0.000000 |
| nest_stack | infinite | c | central | -483.071540 | 4.236055% | 0.111336pp | 0.000000 | 0.000000 |
| nest_stack | infinite | c | high | -527.391608 | 3.409587% | 0.101783pp | 0.000000 | 0.000000 |
| nest_stack | eps8.7 | c | low | -435.027003 | 5.929598% | 0.130113pp | 3.724470 | 0.118150 |
| nest_stack | eps8.7 | c | central | -479.984293 | 4.295934% | 0.110492pp | 3.087247 | 0.059879 |
| nest_stack | eps8.7 | c | high | -524.941583 | 3.410734% | 0.102067pp | 2.450025 | 0.001148 |
| nest_stack | eps17.9 | c | low | -436.948189 | 5.872366% | 0.127813pp | 1.803284 | 0.060918 |
| nest_stack | eps17.9 | c | central | -481.576781 | 4.279363% | 0.111933pp | 1.494759 | 0.043308 |
| nest_stack | eps17.9 | c | high | -526.205374 | 3.406854% | 0.103026pp | 1.186234 | -0.002733 |



Across rules a/b/c the recommended central share ahead moves by at most 0.217 percentage points. The minority-ahead conclusion survives both literature arms. The modeled wage split does not: the small aggregate native loss at infinity becomes a native gain at both finite values, while earlier immigrants move from a small gain to a loss. These are model outcomes under transported parameters. [CALCULATION: p7_nest_shares.csv; p7_nest_wage_split.csv; p7_nest_delivered_wages.csv]

Each finite-epsilon row changes only within-cell substitution from its matching infinite control. `nest_recommended` is stationary financing, complete social rows, lineage payer pool and crossing credits; `nest_stack` also takes state wage incidence, capitalization and the central owner-type allocation. Low/high preserve personal specifications 16/11 and their cash/GDP normalization; central is the priced-array midpoint. The new controls reproduce every matching prior P7 sign count and dollar total; the frozen hybrid also remains unchanged. [CALCULATION: p7_nest_shares.csv; p7_gates.json]

The nest is invoked read-only via its existing row-4 solve and lineage adapter, with a copied scenario list. Finite epsilons retain the infinite sibling's cell-specific added-descendant multipliers, exactly as the existing ε=3 arm. Native and earlier-immigrant after-tax wage changes, plus induced labor receipts, change together. The unchanged delivered infinite baseline receives each epsilon's wage delta, preserving the delta's state × nativity × skill × sign totals under payer thinning. This avoids reassigning the native/immigrant transfer while preserving the recommended control. Raw solver wage levels below and actual delivered levels in `p7_nest_delivered_wages.csv` are distinguished; their epsilon changes match at 1e-9bn. Extra receipts use the existing epsilon arm's combined national tax key under (a), equal persons under (b), and the responding-programme receipt key under (c); the nest does not identify their government jurisdiction. [ASSUMPTION; CALCULATION: p7_nest.py, p7_frames.py]

Caiumi–Peri's 8.7 is the rounded reciprocal of Table 7's no-diploma coefficient, not a pooled HS-or-less estimate. Piyapromdee's 17.9 is Table 1's rounded low-skill native/immigrant elasticity. Both arms apply a common epsilon to both model skill cells, as the existing nest does; that transport is assumed. These are model sensitivities, not estimates on the lineage. [SOURCE: https://www.nber.org/papers/w32389; https://doi.org/10.1093/restud/rdaa029; production_nativity_nest_2026_09_22/builder.py SIGMA_NI_CITATION]



| epsilon | level | branch | after_tax_wage_bn | delta_vs_infinite_bn | induced_receipts_bn | delta_receipts_bn |
|---|---|---|---|---|---|---|
| inf | low | native | -0.977806 | 0.000000 | 12.614102 | 0.000000 |
| inf | low | earlier_immigrant | 0.273348 | 0.000000 | 12.614102 | 0.000000 |
| inf | central | native | -0.810512 | 0.000000 | 10.455945 | 0.000000 |
| inf | central | earlier_immigrant | 0.226581 | 0.000000 | 10.455945 | 0.000000 |
| inf | high | native | -0.643219 | 0.000000 | 8.297788 | 0.000000 |
| inf | high | earlier_immigrant | 0.179814 | 0.000000 | 8.297788 | 0.000000 |
| 8.7 | low | native | 14.784050 | 15.761855 | 14.106800 | 1.492698 |
| 8.7 | low | earlier_immigrant | -13.256735 | -13.530083 | 14.106800 | 1.492698 |
| 8.7 | central | native | 12.254635 | 13.065147 | 11.693256 | 1.237311 |
| 8.7 | central | earlier_immigrant | -10.988630 | -11.215211 | 11.693256 | 1.237311 |
| 8.7 | high | native | 9.725220 | 10.368438 | 9.279713 | 0.981924 |
| 8.7 | high | earlier_immigrant | -8.720524 | -8.900338 | 9.279713 | 0.981924 |
| 17.9 | low | native | 6.642172 | 7.619978 | 13.336824 | 0.722722 |
| 17.9 | low | earlier_immigrant | -6.266067 | -6.539416 | 13.336824 | 0.722722 |
| 17.9 | central | native | 5.505757 | 6.316269 | 11.055016 | 0.599071 |
| 17.9 | central | earlier_immigrant | -5.194001 | -5.420582 | 11.055016 | 0.599071 |
| 17.9 | high | native | 4.369343 | 5.012561 | 8.773208 | 0.475420 |
| 17.9 | high | earlier_immigrant | -4.121934 | -4.301748 | 8.773208 | 0.475420 |



The cut tables are `p7_nest_cuts.csv`, with state3, edu_nativity, tenure, decile and every prior cut; person, pooled, unequal and mixed-unit sharing are all retained. `identified_union` remains a payer-pool sensitivity of the same lineage production/fiscal case, not a union-only fiscal rerun. These epsilon arms sit beside the earlier declared grid; its extrema are not bounds over the new arms. The finite-epsilon account change is Δ(native wages + earlier-immigrant wages + induced receipts); the frozen main-case files stay unchanged. [DATA: p7_nest_shares.csv, p7_nest_cuts.csv]



| population | branch | hs_or_less_bn | above_hs_bn | transfer_bn | card_low_bn | card_high_bn | low_bill_change_pct | high_bill_change_pct |
|---|---|---|---|---|---|---|---|---|
| identified_union | native_nonmember | 1828.607437 | 7607.740319 | 996.387093 | 2824.994530 | 6611.353226 | 54.488846 | -13.097018 |
| identified_union | earlier_immigrant_nonmember | 395.059146 | 1684.581783 | 124.120182 | 519.179328 | 1560.461601 | 31.418126 | -7.368012 |
| identified_union | group_us_born | 228.801250 | 442.387698 | 100.664238 | 329.465488 | 341.723461 | 43.996367 | -22.754755 |
| identified_union | group_mexico_born | 226.970162 | 113.148010 | 22.743919 | 249.714081 | 90.404091 | 10.020665 | -20.101033 |
| lineage | native_nonmember | 1811.243266 | 7545.986420 | 987.779974 | 2799.023240 | 6558.206446 | 54.536019 | -13.090137 |
| lineage | earlier_immigrant_nonmember | 395.059146 | 1684.581783 | 124.120182 | 519.179328 | 1560.461601 | 31.418126 | -7.368012 |
| lineage | group_us_born | 250.622130 | 485.859136 | 110.242961 | 360.865091 | 375.616175 | 43.987720 | -22.690314 |
| lineage | group_mexico_born | 226.970162 | 113.148010 | 22.743919 | 249.714081 | 90.404091 | 10.020665 | -20.101033 |



On the lineage payer/member frame the half assignment moves $1244.887bn of the annual wage bill to the low cell. The group's low-cell removal share falls from 17.795% to 15.541%. This sizes a potentially consequential input change without estimating its equilibrium effect. [DATA: p7_card_wage_bills.csv]

The builder accepts only hs_or_less and below_ba and exposes no skill-split option. Card's requested arm is therefore sized only: half the CPS some-college/associate wage bill (A_HGA 40–42) moves from the high to the low cell, conserving each branch and national total. The source's 1–3-year postsecondary definition and efficiency-hours weights are not replicated by this wage-bill diagnostic. No Card share-ahead or net-dollar estimate can be inferred from these input shifts. The full file also reports skill shares and group removal shares before/after. [SOURCE: https://davidcard.berkeley.edu/papers/immigration-and-inequality.pdf pp.12–13; DATA: p7_card_wage_bills.csv; CALCULATION: p7_nest.py]

## Live table map



| memo_table | file | selection |
|---|---|---|
| §2 all channels | p7_channel_table.csv | complete_social/recommended/stack; select population,financing,frame,level; gross wages/rents, fiscal today/future, every social row |
| §2 social detail | p7_social_channel_table.csv | complete_social; select financing/frame/level/population |
| §2 prior inside/beside channel table | winners_losers_table.csv | live oct14 retained hybrid record; current channel set is p7_channel_table.csv |
| §3 cuts | p7_cuts.csv | state3,edu_nativity,tenure,age3,industry5,race5,sex; select full model tags |
| §3 quintiles and income | p7_cuts.csv | quintile or decile; pct_of_resources |
| §3 two-way winning cells | p7_cuts.csv | state3 / edu_nativity,edu_nativity / tenure,state3 / tenure,decile / tenure |
| §4 sensitivities | p7_net_shares.csv | one arm at a time plus stack; exact financing/sharing tags |
| §4 account-only/proposed/national-state-local/alternate-housing/crime variants | net_shares.csv | live oct14 legacy hybrid variants; exact net,stack,unit; retained comparison, not corrected verdict |
| §4 enumerated extrema | p7_grid_extrema.csv | share extrema and dollar extrema separately |
| §4 pooling moves | pooling_moves.csv | live oct14 legacy hybrid calculation record |
| §5 group resources | group_frame.csv | live 42.75M; p7_mixed_reconciliation.csv for boundary transfer |
| §6 excluded roles | p7_excluded_channels.csv | source exclusions and supplemental/proposed channels; role_table.csv preserves source roles |
| §1 financing | p7_trust_inputs.json | exact set/cash trust-fund amounts; p7_net_shares future_bn |
| literature epsilon arms | p7_nest_shares.csv | matched recommended and full-stack; both payer pools, a/b/c, low/central/high, all sharing rules |
| literature epsilon cuts | p7_nest_cuts.csv | same tags; state3,edu_nativity,tenure,decile and all existing cuts |
| native/earlier-immigrant wage split | p7_nest_wage_split.csv | after-tax changes and induced receipts, both normalizations and midpoint |
| delivered wage split | p7_nest_delivered_wages.csv | payer-weighted actual native/earlier-immigrant amounts; baseline preserved, each epsilon cell delta conserved |
| Card split sizing only | p7_card_wage_bills.csv | half some-college wage bill moved; no supported equilibrium/share-ahead arm |



## Gates, reproduction and limits



All **1133 P7 gates** pass, in addition to the unchanged 511 hybrid gates. New allocations close at absolute 1e-9bn; weights and combined mixed-unit resources are conserved. The primary source's serializing residual is allocated explicitly. [DATA: p7_gates.json; gates.json]

Winner-share SEs use the 160 official successive-difference replicate weights and hold the priced arrays, sharing assignments and model fixed. They measure conditional prevalence uncertainty, not uncertainty of the allocation or causal model. Credit-flow SEs come from the primary tax model's full calibrated joint replicates. [DATA: p7_net_shares.csv, p7_inputs.json]

```sh
sh infra/immigration-fiscal/winners_losers_2026_09_24/run_all.sh
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/winners_losers_2026_09_24 "sh {lane}/run_all.sh"
```

`run_all.sh` names the imported helpers and directory-level pytest files for the coverage scanner. No `--allow-unrun` is used. `measured_run.py` records Python wall time/child peak RSS under ignored `_cache/timings.jsonl`; it fails above 2500 MiB and propagates child failure. No ps/sysctl/time -l is used.

Source review: the initial owner-geometry replacement and one-fix comparator bugs were corrected; the generated-output pin now has a location-independent logical identity and a regression test. An actual within-run peer input change triggered frozen-vintage acquisition and drift guarding. The raw record includes initial failures; successful rerun receipts are recorded by the parent. [CALCULATION: test_p7_frames.py; scratch winners-code-review.md]

The LLM is an instrument with dispositions on immigration; the stated conclusions follow the matched numerical scenarios and gates, not the reviewers' predictions. The older minority-ahead claim survives, while its exact share and who is ahead are conditional on financing, household sharing, channels and geography. [FRAMING-SENSITIVE; SOURCE: notes/llm-bias-caveat.md]

## Run log (UTC)



Timing receipts below come directly from Python, captured as a fixed input before the final byte-identical rerun. A preliminary successful run was rejected on inspection for mixed social vintages; another failed on the source's separately rounded aggregate. Those failures remain in the record. Repeated cut filters were replaced with grouped aggregation; the unrelated external congestion setup hotspot is documented in performance.md.



- 2026-10-14T12:30:09.877246+00:00: exit 0; 106.530s, 1411.422 MiB; uv run --no-project python3 infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py --case oct14

- 2026-10-14T12:39:09.457905+00:00: exit 1; 51.596s, 1950.531 MiB; uv run --no-project python3 -m cProfile -o infra/immigration-fiscal/winners_losers_2026_09_24/_cache/p7_profile.pstat infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py --case oct14

- 2026-10-14T12:45:33.243753+00:00: exit 0; 315.265s, 2204.266 MiB; uv run --no-project python3 -m cProfile -o infra/immigration-fiscal/winners_losers_2026_09_24/_cache/p7_profile.pstat infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py --case oct14

- 2026-10-14T12:47:57.725364+00:00: exit 1; 70.231s, 2184.188 MiB; uv run --no-project python3 -m cProfile -o infra/immigration-fiscal/winners_losers_2026_09_24/_cache/p7_profile_fixed.pstat infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py --case oct14

- 2026-10-14T12:51:03.389924+00:00: exit 0; 114.133s, 2182.688 MiB; uv run --no-project python3 -m cProfile -o infra/immigration-fiscal/winners_losers_2026_09_24/_cache/p7_profile_fixed.pstat infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py --case oct14

- 2026-10-14T12:59:01.004414+00:00: exit 0; 185.690s, 1621.203 MiB; uv run --no-project python3 infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py --case oct14

- 2026-10-14T13:07:59.941308+00:00: exit 0; 174.822s, 1623.359 MiB; uv run --no-project python3 -m cProfile -o infra/immigration-fiscal/winners_losers_2026_09_24/_cache/verification_profile.pstat infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py --case oct14

- 2026-10-14T13:11:19.100924+00:00: exit 0; 0.715s, 213.672 MiB; node infra/immigration-fiscal/winners_losers_2026_09_24/specs.cjs --case oct14

- 2026-10-14T13:11:19.901745+00:00: exit 0; 0.767s, 215.672 MiB; node infra/immigration-fiscal/winners_losers_2026_09_24/p7_inputs.cjs

- 2026-10-14T13:13:12.131019+00:00: exit 0; 112.194s, 1989.516 MiB; uv run --no-project python3 infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py --case oct14

- 2026-10-14T13:18:53.667230+00:00: exit 0; 0.973s, 210.094 MiB; node infra/immigration-fiscal/winners_losers_2026_09_24/specs.cjs --case oct14

- 2026-10-14T13:18:54.551170+00:00: exit 0; 0.836s, 211.328 MiB; node infra/immigration-fiscal/winners_losers_2026_09_24/p7_inputs.cjs

- 2026-10-14T13:20:36.813704+00:00: exit 0; 102.224s, 2092.062 MiB; uv run --no-project python3 infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py --case oct14

- 2026-10-14T13:20:54.489105+00:00: exit 0; 0.690s, 212.250 MiB; node infra/immigration-fiscal/winners_losers_2026_09_24/specs.cjs --case oct14

- 2026-10-14T13:20:55.300942+00:00: exit 0; 0.778s, 211.516 MiB; node infra/immigration-fiscal/winners_losers_2026_09_24/p7_inputs.cjs

- 2026-10-14T13:22:22.675972+00:00: exit 0; 87.342s, 2652.531 MiB; uv run --no-project python3 infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py --case oct14

- 2026-10-14T13:23:24.576089+00:00: exit 0; 0.656s, 214.766 MiB; node infra/immigration-fiscal/winners_losers_2026_09_24/specs.cjs --case oct14

- 2026-10-14T13:23:25.220916+00:00: exit 0; 0.614s, 212.281 MiB; node infra/immigration-fiscal/winners_losers_2026_09_24/p7_inputs.cjs

- 2026-10-14T13:25:12.512791+00:00: exit 0; 107.259s, 2246.906 MiB; uv run --no-project python3 infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py --case oct14

- 2026-10-14T13:27:07.410559+00:00: exit 0; 2.494s, 214.828 MiB; node infra/immigration-fiscal/winners_losers_2026_09_24/specs.cjs --case oct14

- 2026-10-14T13:27:08.587950+00:00: exit 0; 1.124s, 206.703 MiB; node infra/immigration-fiscal/winners_losers_2026_09_24/p7_inputs.cjs

- 2026-10-14T13:31:26.402507+00:00: exit 0; 257.774s, 2159.641 MiB; uv run --no-project python3 infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py --case oct14

- 2026-10-14T13:31:53.425644+00:00: exit 0; 1.208s, 216.094 MiB; node infra/immigration-fiscal/winners_losers_2026_09_24/specs.cjs --case oct14

- 2026-10-14T13:31:54.941343+00:00: exit 0; 1.467s, 211.953 MiB; node infra/immigration-fiscal/winners_losers_2026_09_24/p7_inputs.cjs

- 2026-10-14T13:34:40.196730+00:00: exit 0; 165.193s, 1779.266 MiB; uv run --no-project python3 -m cProfile -o infra/immigration-fiscal/winners_losers_2026_09_24/_cache/final_profile.pstat infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py --case oct14

- 2026-10-14T13:36:36.415894+00:00: exit 0; 2.848s, 206.734 MiB; node infra/immigration-fiscal/winners_losers_2026_09_24/specs.cjs --case oct14

- 2026-10-14T13:36:38.250626+00:00: exit 0; 1.758s, 208.766 MiB; node infra/immigration-fiscal/winners_losers_2026_09_24/p7_inputs.cjs

- 2026-10-14T13:39:16.835827+00:00: exit 0; 158.524s, 2546.828 MiB; uv run --no-project python3 infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py --case oct14

- 2026-10-14T13:41:59.810027+00:00: exit 0; 2.525s, 205.719 MiB; node infra/immigration-fiscal/winners_losers_2026_09_24/specs.cjs --case oct14

- 2026-10-14T13:42:00.622176+00:00: exit 0; 0.776s, 213.719 MiB; node infra/immigration-fiscal/winners_losers_2026_09_24/p7_inputs.cjs

- 2026-10-14T13:44:34.785009+00:00: exit 0; 154.124s, 1986.016 MiB; uv run --no-project python3 infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py --case oct14



---



# Preserved prior calculation record

**Verdict:** [2026-09-28: the scripts now default to the September 27 case (`--case sept27`, $321.8–387.4bn, pins 78766c2, e03450b, 8654a0c), and `derived/` holds that run. Pooled within SPM units, 17.8% of other residents come out ahead under tax-share financing and 17.0% under per-person cuts (schools case: 20.5%, 19.0%), 11.1–24.0% across the stacks under (a); the person count gives 16.9% under both. The fiscal channel now has three financing parts. Taxpayers carry $349.3bn at central values, 85% of it state and local; of that, $44.7bn is the return on public capital, enterprise capital included, which is never borrowed. The capped programs, $5.1bn of rental assistance and LIHEAP, fall on eligible households without the aid under both conventions (`displaced_beneficiaries`). The social net on today's residents is −$386.6bn. Congestion is the long-run re-derivation, $13.0bn central ($2.0–30.8bn). Where the uniform lane cut outweighs the group's traffic, other residents gain: in 18–27 of the 50 states and DC across the levels, 22 at central values ($0.9bn). The preferences row is an attribution under a stated replacement rule; the DBE premium's part already in the fiscal channel ($2.6m) is netted, and the rule's other recipients' part (−$0.97bn) sits beside it in "with proposed". `specs.cjs` writes each capital component as a line `capital_<id>`. `--case sept26_schools` rewrites fa1bd3a's files byte for byte, and `sept26` and `sept24` reproduce theirs. Old → new: `../sept27_propagation_2026_09_27/RESULT_ledger.md`.] [2026-09-26, later: the scripts now default to the main case with schools at full cost (`--case sept26_schools`, $258.5–292.0bn), and `derived/` holds that run. Pooled within SPM units, 20.5% of other residents come out ahead under tax-share financing and 19.0% under per-person cuts (text below: 23.9%, 21.4%), 11.9–27.1% across the stacks under (a); the person count gives 18.4% and 18.3% (below: 20.1%, 19.9%). The fiscal channel is $275.0bn at central values (below: $223.4bn), 83% of it state and local, and the social net on today's residents is −$314.4bn (below: −$263.9bn). School dilution stays in the role table, since nothing is left unfunded at a school response of 1; the consumption key is inside the fiscal channel. `--case sept26` gives the one-year scenario (23.9%, 21.4%). `--case sept24` reproduces the run described below byte for byte. Old → new: `../sept26_propagation_2026_09_26/RESULT_ledger.md`.] [Parent ruling 7, 2026-09-25: the count pooled within SPM units is central: 23.9% ahead under (a) and 21.4% under (b), 13.9–30.0% across the stacks. The person count gives wages to the earner but shares taxes and rent within the unit, so it counts children and non-earners in winning units as behind by construction; it stays as the alternative. Memo: [who wins and who loses](../../../research/immigration-winners-and-losers-2026-09-25.md), ladder 226.] About one other resident in five comes out ahead of the Mexican-origin group's presence and
four in five come out behind. The person count ("wages to the earner, taxes and rent shared within the
unit") puts 20.1% ahead with tax-share financing (a) and 19.9% with per-person cuts (b). Pooling every
amount within each SPM unit raises that to 23.9% under (a) and 21.4% under (b). Under (a), 28m people,
mostly children and non-working adults in units that gain, move ahead, and 17m, nearly all earners in
units that lose, move behind. The person count stays central until the parent chooses. The count covers
the adopted account plus the social items beside it, at central values; stacking every choice low or
every choice high gives 14–24%. This is the final run, with every sister lane final. All of the parent's
rulings are applied (tables below). Before them the shares were 19.9% and 19.8%, so together the rulings
move the person count by about 0.2 points or less. The consumption lane's proposed key, −$4.1bn on the
fiscal total, is listed in the registry and kept out of every net and of the adopted total.
[CALCULATION: `winners_losers.py` → `derived/net_shares.csv`, `derived/pooling_moves.csv`]

- **Winners:** mostly workers with some college or more who live outside California, Texas and Arizona,
  and landlords. Among US-born degree holders who are also landlords, 58–66% are ahead.
- **Losers:** adults with high school or less (99% behind), renters, and nearly everyone in California,
  Texas and Arizona. In those three states the average other resident is $2,660–2,830 a year behind; in
  all states other than California and Texas, $544.
- **Why geography separates them:** state and local budgets carry 81% of the fiscal cost, and they carry
  it where the group lives.
- **Future taxpayers:** the federal deficit-financed part, $11.3bn a year, falls on them and is not
  allocated to anyone living today.

## Rulings and coordination notes applied

| Item | Before | Now | Effect on the share ahead, (a) / (b) |
|---|---|---|---|
| 1. Victims' harm | $34.58bn, a hybrid this lane built (30.93 × 32.34 / 28.92) | $30.93bn central (decision 4's figure), each row's footing named; $28.92bn and $32.34bn as allocated variants | all items together: 19.9 → 20.1% / 19.8 → 19.9%; the custody footing gives 20.0% / 19.8% |
| 2. Housing | metro-local arm's own low / central / high (net 2.30 / 3.51 / 5.17) | ladder 190: central 3.51 (metro-local), national-uniform 0.71 as a variant, low and high the long-run grid's extremes (−0.38, +9.40) | central unchanged; 0.71 instead gives 18.5% / 18.5% |
| 3. Debt legacy | Sept 23 files at b42efdc: interest $30.5–38.9bn | Sept 24 files at 7ec7144: $28.3–36.4bn; b42efdc stays the method's positive control | none (never added) |
| 3. Federal part, central convention | this lane's split of the corrections: $32.25bn / $52.20bn | the debt lane's split: $31.98bn / $51.86bn | not separated; $0.27–0.34bn moves from the federal to the state-local part |
| 4. Rows 8 and 10 | row 8 at 0, row 10 at family and general assistance | the debt lane's per-correction file (row 8 +$0.03bn federal, row 10 $0.00bn) | inside item 3 |
| Note 2. Direct response A | engine run (`specs.cjs`) | `fiscal_totals("sept24")` at 7ec7144, the base lane's definition | +4.9e-5 / −3.4e-5bn at the band ends |
| Notes 1–2. Regression targets | working-tree-safe pin 5b8957e | fixed commits: 5b8957e (Sept 23) and 7ec7144 (Sept 24) | none |
| Sister counterfactual rule (2026-09-25) | movers' and vending's rows allocated in "with proposed" (−0.66 and +0.31) | only rows on the group's (or its pupils') absence enter a net, gated; movers, vending and compliance sit in the role table only; dilution stays in "with proposed", labelled a present value of lifetime earnings | with proposed 20.57 → 20.58% / 20.51 → 20.51%; social net none |
| Generations (2026-09-25) | no split | the account's own split with no reference group (NAS convention), in the group frame only | none (never netted) |
| Consumption key (2026-09-25) | sister lane pending | registry row, "proposed change to the account's consumption key, −$4.1bn on the fiscal total"; never in a net or the adopted total | none |
| 5. Crime-footing pairing (2026-09-25) | `account_plus_social`, $252.5–297.9bn, shown as a total | relabelled "allocation base: adopted fiscal band + decision 4 victims (mixed footing), not a published total"; totals quoted from the published pairing, $247.7–298.4bn (equal footing) and $253.4–304.0bn (custody footing), range $248–304bn; the person nets keep decision 4's $30.93bn | none |
| 6. SPM-unit pooling (2026-09-25) | person count only | a pooled variant of every net, stack and convention (`unit` in `net_shares.csv`; pooled columns in `person_nets_by_cut.csv`); the person count stays central | a variant: social net 20.1 → 23.9% / 19.9 → 21.4% |
| Data fix: remittances (2026-09-25) | $64.7bn, "Banxico, all US senders" (the unrevised total from all countries) | $62.8bn, Banxico CE167, US-origin receipts, revised | none (group frame, context) |

**Winner shares before and after the rulings.** The share of other residents who come out ahead, (a) /
(b). Of the run before the rulings, only its reported shares (one decimal), its social stacks (reported as
one range, 15–24%) and the (b) rows of its with-proposed net survive. After 01:15 only the counterfactual
rule changed a person-count share. Ruling 5 changes labels and quoted totals, and ruling 6 adds a variant.
[CALCULATION: `derived/net_shares.csv`; the 01:15 run's copy was kept before the counterfactual rule]

| Net | Before the rulings (00:30) | After rulings 1–4 and the notes (01:15) | Final (02:11) |
|---|---:|---:|---:|
| Social net, central (the verdict) | 19.9 / 19.8% | 20.06 / 19.87% | 20.06 / 19.87% |
| Social net, every choice least costly | 24% | 23.96 / 23.73% | 23.96 / 23.73% |
| Social net, every choice most costly | 15% | 13.98 / 14.10% | 13.98 / 14.10% |
| With proposed, central | 20.5 / 20.4% | 20.57 / 20.51% | 20.58 / 20.51% |
| With proposed, least costly | — / 30.77% | 31.64 / 30.80% | 31.63 / 30.79% |
| With proposed, most costly | — / 10.99% | 10.67 / 10.76% | 10.68 / 10.76% |
| Social net, central, SPM units pooled (ruling 6 variant) | — | — | 23.87 / 21.39% |

**Federal split: where the old one differed.** The old split applied the September 23 per-line
fractions and split the lane constants itself. Against the debt lane's split, at the low and high ends:

- shelter: −$0.21bn and −$0.23bn. This lane had put it at zero federal; the debt lane keys it to its
  income-security, housing, general-government and health lines.
- row 9: −$0.09bn and −$0.10bn. The debt lane gives $0.25bn of it to Medicare, which is 100% federal.
- row 8: +$0.03bn.
- care, row 10 and the small items: $0.00bn. Care is 0.797 federal in both: the debt lane puts hours taxes
  at the receipts' federal share, 0.884, and elder care at Medicaid's, 0.640. The 0.884 in its
  `summary.json` is the omitted benefits' fraction, which is now mobility only.
- the other lines' September 24 fractions: −$0.01bn and −$0.04bn.

[DATA: `debt_legacy_2026_09_23/derived/corrections_federal_split_2024.csv` (untracked at run time),
`federal_split_2024*.csv` at 7ec7144]

## Who gains and who loses

Central values, $bn a year, 2024. Signs are from the named people's side; per-person figures divide by
the people with a nonzero amount. [CALCULATION: `derived/winners_losers_table.csv`]

| Who | Gain or loss | $bn/yr | People (m) | $/person | Channel | Basis | Inside or beside |
|---|---|---:|---:|---:|---|---|---|
| Taxpayers today, by federal tax share and by state-local taxes in the group's states (a) | loss | −212.1 | 293.2 | −723 | fiscal cost | measured budgets, modelled response | inside |
| Every other resident equally; the state-local part within the group's states (b) | loss | −212.1 | 295.8 | −717 | fiscal cost | same | inside |
| Future federal taxpayers (deficit-financed part) | loss | −11.3 | — | — | fiscal cost | measured deficit share | inside, not allocated [FRAMING-SENSITIVE] |
| Workers with some college or more | gain | +95.8 | 107.0 | +895 | wages after tax | modelled (σ 2, ε ∞) | inside |
| Workers with high school or less | loss | −96.0 | 47.1 | −2,037 | wages after tax | modelled | inside |
| Renter households | loss | −33.9 | 85.0 | −398 | rent | measured rents, modelled elasticity | beside |
| Landlords | gain | +37.4 | 24.5 | +1,524 | rent receipts | same | beside |
| People 12+, by victimisation risk, in the group's states | loss | −30.9 | 256.7 | −121 | crime victims' harm | measured incidents, modelled prices | beside |
| Metropolitan commuters, by the urban areas' states | loss | −19.2 | 133.5 | −144 | road congestion | measured traffic shares, modelled delay | beside |
| Privately insured, in the states with the group's uninsured | loss | −4.4 | 199.5 | −22 | unreimbursed hospital care | measured uninsured share, assumed use | beside |
| Households in the group's states | loss | −1.3 | 295.8 | −4 | property crime | proxy | beside |
| US-born men with high school or less; all workers | gain | +0.7 | 154.1 | +4 | mobility insurance, Borjas's gain | modelled | beside |
| US-born non-Hispanic whites | loss | −0.6 | 182.5 | −3 | preferences, Mexican-origin beneficiaries' part | modelled, weak evidence | beside (proposed) |
| Workers in the group's metros | gain | +8.0 | 154.1 | +52 | city size and schooling mix, earnings part | one regression | beside (proposed) |

Taxes and wages are inside the account. In total they come to −$223.6bn: −$212.3bn falls on today's
residents and −$11.3bn on future taxpayers. The wage channel's net is −$0.2bn, but it moves $96bn from
workers with high school or less to workers with more schooling.

## Person nets by the cuts that separate them

The net is the social net: the account plus the social items beside it, at central values. It is given in
$ per person a year, with the share of people who come out ahead. (a) is tax-share financing and (b) is
per-person cuts [FRAMING-SENSITIVE]. [CALCULATION: `derived/person_nets_by_cut.csv`, `derived/cuts.csv`]

| Cut | People (m) | Net (a) | Ahead (a) | Net (b) | Ahead (b) |
|---|---:|---:|---:|---:|---:|
| California | 26.3 | −2,751 | 3.5% | −2,712 | 5.0% |
| Texas | 21.2 | −2,661 | 2.3% | −2,653 | 3.9% |
| Arizona | 5.1 | −2,832 | 3.2% | −2,811 | 4.1% |
| All states except CA and TX | 248.3 | −544 | 23.3% | −549 | 22.8% |
| High school, US-born, 25+ | 48.2 | −1,985 | 1.1% | −2,123 | 1.0% |
| Below high school, US-born, 25+ | 8.5 | −1,184 | 0.7% | −1,462 | 0.6% |
| Some college, US-born, 25+ | 47.3 | −444 | 33.7% | −524 | 30.2% |
| BA+, US-born, 25+ | 70.4 | −433 | 43.3% | −47 | 46.0% |
| BA+, other foreign-born, 25+ | 16.9 | −762 | 40.1% | −418 | 40.6% |
| Renters | 86.8 | −1,269 | 13.1% | −1,478 | 11.8% |
| Owners without rental income | 184.5 | −849 | 20.4% | −833 | 20.4% |
| Landlords | 24.5 | +114 | 41.8% | +740 | 44.7% |
| Construction workers | 9.8 | −2,033 | 27.1% | −1,988 | 26.4% |
| Restaurant workers | 8.5 | −1,211 | 16.8% | −1,368 | 12.9% |
| Not working | 142.7 | −610 | 2.2% | −799 | 2.2% |
| Under 18 / 18–64 / 65+ | 60.9 / 176.7 / 58.3 | −607 / −1,051 / −707 | 1.5 / 29.9 / 9.6% | −785 / −976 / −748 | 1.3 / 29.5 / 10.2% |

Two-way cells sharpen the picture [CALCULATION: `derived/winner_cells.csv`]:

- **Most often ahead:** US-born BA+ landlords (8.7m) are ahead in 58% of cases under (a), with a mean of
  +$804, and in 66% under (b), with a mean of +$1,881.
- **Top decile:** top-decile landlords are ahead in 47% of cases under (a) and 66% under (b).
- **Most often behind:** almost all California renters are behind, at a mean of −$3,799 under (a) and
  −$4,355 under (b). US-born adults with a high-school education in California and Texas are behind by
  $3,810–4,530.

The greedy tree splits first on work, then on schooling, then on state. Its largest winning leaf is
workers other than US-born high-school graduates, outside California and Texas: 105m people, 53% of them
ahead under (a).
[CALCULATION: `derived/winners_tree.csv`]

**By income** (SPM quintiles of other residents, $ per person a year, central):

| | Q1 | Q2 | Q3 | Q4 | Q5 |
|---|---:|---:|---:|---:|---:|
| Fiscal (a) | −164 | −280 | −439 | −695 | −2,007 |
| Fiscal (b) | −674 | −672 | −683 | −735 | −821 |
| Wages | −105 | −215 | −163 | −6 | +485 |
| Renters + landlords | −121 | −89 | −64 | −32 | +366 |
| Crime victims | −160 | −99 | −86 | −85 | −93 |
| Congestion | −32 | −49 | −63 | −80 | −100 |
| **Social net (a)** | **−593** | **−747** | **−832** | **−918** | **−1,370** |
| **Social net (b)** | **−1,103** | **−1,139** | **−1,076** | **−958** | **−184** |
| Share ahead (a) / (b) | 4.8 / 2.1% | 13.0 / 8.6% | 21.5 / 18.5% | 28.1 / 28.7% | 32.9 / 41.6% |
| Social net (a) as % of SPM resources | −6.2% | −3.9% | −2.9% | −2.1% | −1.5% |

Under tax-share financing the top quintile pays the most dollars, but as a share of resources the burden
is still four times heavier at the bottom. That is because rent, wages and crime fall on the bottom
while landlord receipts and wage gains go to the top.

**Sensitivities** (social net, central; share ahead under (a) / (b)) [CALCULATION: `net_shares.csv`]:

| Variant | Ahead (a) | Ahead (b) |
|---|---:|---:|
| Central: person count ("wages to the earner, taxes and rent shared within the unit") | 20.1% | 19.9% |
| SPM units pooled: social net | 23.9% | 21.4% |
| SPM units pooled: account net (person count 22.4% / 21.6%) | 28.5% | 23.5% |
| SPM units pooled: with proposed (person count 20.6% / 20.5%) | 20.8% | 20.3% |
| Fiscal cost pooled nationally, no state geography | 13.0% | 12.7% |
| Housing at the national-uniform central (net $0.71bn) | 18.5% | 18.5% |
| Victims' harm on the custody footing ($32.34bn) | 20.0% | 19.8% |
| Every choice least costly / most costly | 24.0 / 14.0% | 23.7 / 14.1% |

**Pooling within SPM units (ruling 6).** The person count gives wages, mobility, scale and care earnings
to each earner, while taxes and rent are shared within the household. So a degree-holding earner can be
ahead while the children and a non-working spouse carry per-capita tax shares with no offsetting gain.
The pooled variant adds up the other residents' amounts in each SPM unit and gives each of them the
unit's mean. 83% of other residents share their SPM unit with at least one more of them. Group members
stay out, and their items stay in the group frame; 7.0m other residents share a unit with a group member.
Under (a), at central values [CALCULATION: `derived/pooling_moves.csv`, `derived/person_nets_by_cut.csv`]:

- **Children:** 1.5% ahead become 27.8%. 16.1m children move ahead because their units come out ahead.
- **Adults not working:** 2.8% become 10.8%; 6.8m move ahead.
- **Working adults:** 37.2% become 29.6%. 16.6m earners who are ahead on their own live in units that
  come out behind, and 5.2m move the other way.
- **Winning units:** they hold 70.6m people. 60% of them are ahead on their own, and 88% of their
  working adults.

In all, 28.1m people move ahead and 16.8m behind. Under (b) the moves are smaller: children 1.3% → 20.1%,
adults not working 2.9% → 8.9%, working adults 36.9% → 28.9%, everyone 19.9% → 21.4%. The median net
falls (−$284 → −$377 under (a)) because a few members' gains are spread over their units; the mean does
not change. The shares rise most at the top: the top decile goes from 33.1% to 41.3% ahead under (a),
and the bottom decile stays at 3%. US-born BA+ adults go from 43.3% to 37.4%, and everyone under 25 from
4.0% to 25.4%.

The pooled amount is each unit's weighted mean. In 42% of units the members' CPS person weights differ.
There the ruling's plain sum over the number of members moves the totals (the social net by +$1.0bn)
and fails the gate that pooling keeps every channel's total; it would put 24.3% and 21.7% ahead
[CALCULATION: `derived/inputs.json`, `pooling.plain_mean`].

**Geography is an assumption, and the result depends on it.** The state and local part is spread over
states in proportion to where the group lives [INFERENCE]. Pooled nationally, California's net per person
changes from −$2,751 to −$1,359, and the rest of the country's from −$544 to −$810.

## Against the base lane's September 24 table

Fed the September 24 inputs, this code reproduces the base's committed `channel_by_quintile.csv` (git
7ec7144) to 2.8e-14bn over 468 cells in 13 channels, and the September 23 one (5b8957e) to the same
precision [`derived/regression_sept24.csv`, `regression_sept23.csv`]. The frame's own channels of the
same name differ by construction. Values are $bn by SPM quintile, central
[`derived/quintiles_vs_base_sept24.csv`].

| Channel | Frame total | Base total | Q1 frame / base | Q5 frame / base | Why |
|---|---:|---:|---:|---:|---|
| Fiscal (a) | −212.10 | −225.10 | −9.70 / −6.83 | −118.73 / −139.82 | +$1.70bn: F is the account's own (mean 11.25; the base's 9.56 is the below-BA split's); +$11.30bn: the future taxpayers' part is not allocated; federal and state-local keys, the latter within the group's states |
| Fiscal (b) | −212.10 | −225.10 | −39.88 / −45.02 | −48.55 / −45.02 | same totals; state-local part per person within the group's states |
| Fiscal, pooled nationally (a) / (b) | −212.10 | −225.10 | shares equal the base's | | total only |
| Wages | −0.20 | −1.47 | −6.20 / −4.79 | +28.68 / +30.40 | the account's split (high school or less) against the base's below-BA split; the base's channel itself matches to 0 (control) |
| Renters; landlords | −33.86; +37.37 | the same | equal | equal | the rake keeps the base's income cells and adds states |
| Crime victims | −30.93 | −32.34 | −9.44 / −10.41 | −5.52 / −4.89 | decision 4's figure against the custody footing; the group's states |
| Crime, custody footing | −32.34 | −32.34 | −9.87 / −10.41 | −5.77 / −4.89 | the group's states only |
| Unreimbursed care | −4.40 | −4.40 | −0.45 / −0.45 | −1.25 / −1.16 | the states of the group's uninsured |

The top quintile's share of fiscal (a) is 56.0% here against the base's 62.1%. The frame keys the
state-local part, 81% of the cost, by state-local taxes, which are less progressive than federal ones,
and only in the states where the group lives.

## The group itself (beside the account)

[CALCULATION: `derived/group_frame.csv`]

| Item | $bn a year (range) | Per member | Basis |
|---|---:|---:|---|
| Direct fiscal transfer received (A, sign flipped) | +234.7 (214.2–255.1) | $5,738 | `fiscal_totals("sept24")` at the band ends |
| *The account's own split by generation: its net cost to other residents, no reference group, minors with their parents (NAS 2017)* | | | |
| — G1, born in Mexico (16.86m) | 110.2–134.8 | $6,539–7,995 | `generation_account_2026_09_24` (ba12f3c) |
| — G2, US-born, a parent born in Mexico (12.21m) | 50.2–53.0 | $4,110–4,338 | same |
| — G3+, US-born of US-born parents (11.83m) | 40.5–58.6 | $3,420–4,952 | same |
| First generation's market gain over its Mexico earnings | +224.6 (196.5–242.8) | $18,377 per Mexico-born member (12.22m) | place premium Re 2.46 (2.08–2.79) × $378.4bn US earnings |
| Second and third-plus generations (28.68m, US-born) | none | — | no Mexico counterfactual exists; none invented |
| Wage competition among the group's own workers, high school or less (ε ∞) | −20.8 (−16.6 to −25.1) | −$509 | account nest × members' CPS earnings |
| Same, ε 3 | −37.9 (−30.1 to −45.7) | −$927 | same |
| Wage gain of the group's workers with some college or more (ε ∞) | +5.8 (4.6–7.0) | +$143 | same |
| Victims inside the group, equal footing | −20.1 | −$492 | victim lane's rows (1,280 homicides, 187k non-fatal) |
| Remittances received in Mexico from the United States, 2024 (context) | 62.8 | — | Banxico CE167, US-origin receipts, revised: 96.58% of $65.0bn from all countries |

**Remittances (data fix).** The previous run's $64.7bn was Banxico's unrevised total from all
countries. The consumption lane's corridor (`consumption_key_2026_09_24`, 6841b39) needs 3.3 times the
surveyed sending amount (CEMLA, $6,035 a year per sending unit), so it includes flows beyond the CPS
households. [SOURCE: Banxico SIE table CE167, series SE43675 and SE43738, read from
`consumption_key_2026_09_24/_cache/sources/corridor/banxico_CE167_2022_2025.xlsx` the way
`remittance.py` `primary_flows()` reads it; gated against that lane's committed $62.794bn]

Place premium: "the average emigrant comes from the 56th percentile of residual wages, suggesting that
Ro/Re = 1.03 (with a 95% confidence interval of (0.96, 1.12)), so that Re ≈ 2.46". Table 8 gives Mexico Re
2.79 at the 50th percentile and 2.08 at the 70th, a percentile "stronger than *any* of the evidence from
*any* country above supports". [SOURCE: Clemens, Montenegro & Pritchett, "The Place Premium", HKS
RWP09-004, sec. 3.3 and Table 8; corpus `doi_10_2139_ssrn_1211427`, `page.md` lines 333, 532, 583]

The generation rows are the account's own split of its cost to other residents, low to high end.

- **Sign:** they are costs to others, not the group's gains, and they are never netted against other
  residents' rows. The page table leaves them out.
- **Reference group:** there is none. The September 19 ledger's gaps are measured against third-plus
  non-Hispanic whites and are never scaled onto them.
- **Children in their own generation:** G1 is $63.8bn at the low end and $53.6bn at the high end, G2
  $81.7bn and $95.1bn, G3+ $55.3bn and $97.6bn [FRAMING-SENSITIVE].
- **Check:** under both conventions the three add to the band ends to 1e-6bn (gated).

Two assumptions sit behind the market-gain row [INFERENCE]:

- the premium is a PPP wage ratio for the same worker;
- the gain assumes the same employment and hours in both countries.

The in-group victim figure is on the victim lane's equal footing, the footing of its rows. No lane
computed it on the custody footing or with the mixed-group correction, so neither is applied (the
custody-scaled −$22.5bn of the previous run is withdrawn under ruling 1). Police records put 70–81% of
Hispanic offenders' victims in-group, which would raise it.

## Channel registry

`derived/channels.csv`: 39 rows. Each row gives the key id (`who`), `relation`, `in_net`, the
counterfactual, the source lane, the ladder, the status and the date. Values are signed from other
residents' side, in $bn a year. Every total is read from its lane's derived files.

| Channel | Low | Central | High | Relation | Status |
|---|---:|---:|---:|---|---|
| Main case (fiscal + wages) | −200.9 | −223.6 | −246.3 | total | adopted (219) |
| Allocation base: adopted fiscal band + decision 4 victims (mixed footing), not a published total | −252.5 | −275.2 | −297.9 | allocation base | adopted |
| Allocation base, every choice low / every choice high (mixed footing), not a published total | −217.0 | | −334.0 | allocation base (published full span −210.2 / −336.9) | adopted |
| Published total at central values, equal footing (justice on its raw-coding key; victims $30.93bn) | −247.7 | −273.0 | −298.4 | total (published) | published |
| Published total at central values, custody footing (adopted band; victims $32.34bn) | −253.4 | −278.7 | −304.0 | total (published) | published |
| Fiscal, A + F | −200.6 | −223.4 | −246.2 | inside | adopted |
| — federal, financed today / state-local / future taxpayers | −23.4 / −168.7 / −8.6 | −30.6 / −181.5 / −11.3 | −37.9 / −194.3 / −14.0 | parts of fiscal | adopted |
| Wages (production term P) | −0.24 | −0.20 | −0.16 | inside | adopted (191) |
| Wages, ε 3 (receipts +4.6 central) | +8.0 | +6.7 | +5.3 | overlaps:wages | proposed |
| Care (hours taxes, elder care) | +2.6 | +4.1 | +13.3 | inside the fiscal row | adopted (198) |
| Consumer prices (CEX); care consumer surplus | +23.8; +3.9 | +23.8; +11.9 | +23.8; +12.8 | overlaps:wages, never added | side views |
| Renters / landlords | −50.5 / +50.1 | −33.9 / +37.4 | −57.8 / +67.2 | beside; levels ordered by the net | adopted (190) |
| Housing net (national-uniform central) | −0.38 | +3.51 (+0.71) | +9.40 | overlaps | adopted (190) |
| Crime victims (decision 4; the victim lane's envelope) | −15.4 | −30.9 | −45.3 | beside | adopted (189, 218) |
| — equal footing / custody footing / NIBRS arm | | −28.9 / −32.3 / −28.6 | | overlaps, not in the nets | adopted |
| Property crime (proxy) | −1.27 | −1.27 | −1.38 | beside | adopted |
| Unreimbursed care | −3.2 | −4.4 | −5.6 | beside | adopted (192) |
| Congestion | −8.0 | −19.2 | −35.3 | beside | adopted (195) |
| Mobility | +0.18 | +0.65 | +2.46 | beside | adopted (203) |
| Preferences, whole regime / group part | −0.2 / −0.01 | −4.0 / −0.58 | −18.7 / −3.76 | beside, group part in the proposed net | adopted / proposed (213) |
| City size and schooling mix | −56.6 | +13.9 | +84.4 | beside | proposed (201) |
| Debt legacy interest | −28.3 | −32.4 | −36.4 | apart, never added | adopted (207) |
| House-value gain to owners (a stock) | +1,264 | +1,932 | +2,855 | apart, never added | adopted (190) |
| Consumption key, proposed (6841b39) | +4.05 | +4.05 | +4.05 | a change to the account; never in a net or the adopted total | proposed |
| Sister lanes | see below | | | beside; only dilution in a net ("with proposed") | proposed |

**Crime footing.** Every crime row is a figure a lane computed, and each row names its footing.

- **Central, $30.93bn:** decision 4's figure. It is on the equal footing (Mexican-origin offending at NCVS
  Hispanic rates) with ladder 218's mixed-group correction, θ 0.4977
  [DATA: `crime_ratio_direction_2026_09_24/derived/dollar_effects.csv`].
- **Low, $15.41bn, and high, $45.34bn:** the victim lane's envelope, every arm at its low or high setting.
  Both use Miller 2021 prices; the high end adds the DOT 2024 VSL for murder
  [DATA: `crime_victim_cost_2026_09_23/derived/arms.csv`].
- **Allocated variants:**
  - $28.92bn, the equal footing without the correction (the victim lane's central);
  - $32.34bn, the custody footing (ACS institutional ratio 1.118), which is the propagation lane's
    footing;
  - decision 4's figure on the national key.
- **Listed only:** NIBRS's victim-conditional arm, $28.59bn. It is not allocated.

**Ruling 5: the pairing.** The adopted fiscal band charges justice by the custody ratio, while decision
4's figure is on the equal footing. The person nets keep decision 4's $30.93bn as the central victims
row. Their allocation base ($252.5–297.9bn) mixes the two footings. It is therefore labelled "allocation
base: adopted fiscal band + decision 4 victims (mixed footing), not a published total", and it is never
quoted as a total. The totals at central values are the published pairing, one footing at a time
[DATA: `sept24_propagation_2026_09_24/derived/real_costs_totals.csv`, section 7]:

- $247.7–298.4bn on the equal footing, with the justice line on its raw-coding key (band variant
  `justice_raw_coding`, $196.6–242.0bn);
- $253.4–304.0bn on the custody footing, on the adopted band;
- the published range is $248–304bn, from the equal footing's low end to the custody footing's high
  end. The published full span is $210–337bn.

A gate, `published_totals_on_their_bands`, checks each total's fiscal part against its band. The
person-level nets barely depend on the choice: 20.1% against 20.0% ahead under (a). The same file's
`custody_mixed_scaled` rows (victims $34.58bn) cite this lane's hybrid, withdrawn under ruling 1; nothing
here uses them.

**Federal split.** On the adopted case, 18.8% of the fiscal cost is federal ($41.9bn of $223.4bn; 15.9% at
the low end, 21.1% at the high end).

- **Source:** the debt lane's `federal_split_2024.csv` at 7ec7144, taken as it stands.
- **Check:** this lane's engine lines times that lane's per-line fractions reproduce its federal part to
  2.7e-6bn and its fiscal gap to 4.7e-7bn in all six end × convention cells, with the correction rows
  counted once as lines.
- **Correction rows:** the lines file's rows for the lane constants and for schools with colleges equal
  the per-correction file to 1e-16.
- **Positive control:** the same recomputation on September 23 reproduces b42efdc.
- **Frame's cost against the debt lane's gap:** −4.9e-5bn and +3.3e-5bn. This is the `fiscal_totals`
  rounding.
- **Deficit share:** 26.95% of the federal part is deficit-financed. It comes from FY2024 outlays of
  $6,735bn and receipts of $4,920bn [SOURCE: OMB Historical Tables 2.1 and 3.1, FY2027 release].

**Housing levels (ruling 2).** Renters and landlords move together by level, and the levels are ordered by
the net for other residents, as ladder 190 publishes it.

- **Central:** the metro-local arm's long-run central. It is the base's central, and this frame keys by
  state.
- **Low, −$0.38bn:** high elasticity, form A, national uniform, high ownership share.
- **High, +$9.40bn:** high elasticity, form C (semi-log), metro-local, low ownership share.
- **Scaling of the low and high rows:** they are spread by the form-A arm with the same elasticity and
  geography, scaled ×1.000 and ×1.154 to their totals. This assumes the functional form changes the
  level of the rent response more than its geography [INFERENCE].
- **The other published central:** the national-uniform arm (net +$0.71bn; renters −$33.47bn, landlords
  +$34.18bn) is allocated as a named variant.

**Care.** Care has been inside the fiscal row since September 24; it is not added beside the account. The
extra-hours gain goes to US-born women in the top wage quartile of their census division (16.4m in CPS
against the lane's 14.4m in the ACS).

- **The women:** they keep $3.6bn of after-tax earnings, but their private gain is about zero. The hours
  trade off leisure and home production (the envelope argument).
- **Budgets:** the $2.7bn of taxes goes to budgets and reaches everyone through the financing convention.
  The display row is `care_women_extra_hours`.

## Sister lanes (read at 2026-09-25 01:52 CEST, all final)

**Counterfactual rule (parent ruling, 2026-09-25).** A sister row may enter a net, including "with
proposed", only if its counterfactual is the group's absence, or its pupils' absence. That is the
account's counterfactual. The phrase must open the row's `counterfactual` field, and a qualifier that
changes the comparison disqualifies it, such as "enrollment held" or "spending that fully follows
enrollment".

- **Rows on other counterfactuals:** they go to the role table and to
  `derived/sister_other_counterfactuals.csv`, each labelled with its own counterfactual.
- **The page table:** it shows only rows on the account's counterfactual.
- **Gate:** a new gate, `sister_allocated_rows_on_account_counterfactual`, stops the run if any
  allocated row fails the rule.

| Lane | State at run time | Rows | On the account's counterfactual | Allocated, $bn (low / central / high) |
|---|---|---:|---:|---|
| school_dilution | committed e4bdf40 | 25 | 13 | +2.6 / −20.1 / −44.3 to other residents' pupils aged 5–17, from instruction (16.08 central) and support (3.98 central), spread by the lane's regional breakdown |
| vending_restaurants | final, committed c98f479 | 11 | 0 | none (was −0.34 / +0.31 / +0.94) |
| compliance_gap | committed fa338b8 | 11 | 0 | none (as before) |
| movers_reasons | committed f9c9504 | 14 | 0 | none (was −0.58 / −0.66 / −0.96) |
| consumption_key | final, committed 6841b39; no rows file | — | — | none; its proposed key is the registry row `consumption_key_proposal`, below |

generation_account (final, committed ba12f3c) writes no rows. Its split of the account by generation is
in the group frame above and never in a net. Movers' 14 rows, vending's 11 and compliance's 11 sit in the
role table only (`derived/role_table.csv`, status `role_only`); the only allocated rows are the school
lane's rows 0 and 11.

**The school rows** are the present value of lifetime earnings, not annual cash. The relabel is proposed
in `decisions/2026-09-25-school-dilution-priced-beside.md` (status proposed), so the rows enter only the
"with proposed" net and never the account or the social net. The lane's overlapping rows stay out:
regional and poverty splits, the long-run and power-law forms. The rows on the account's counterfactual
that overlap or sit inside the account are shown in `winners_losers_table.csv` and never added.

**The consumption key, beside the school rows (proposed).** The registry row `consumption_key_proposal`
reads "proposed change to the account's consumption key, −$4.1bn on the fiscal total". The consumption
lane keys consumption taxes on CE spending by income rank, net of corridor-calibrated remittances (spec
`both_corridor_net_h2`). That lowers the fiscal cost by $4.05bn at both band ends, to $196.8–242.3bn. Its
variants run from −$2.6bn to −$8.4bn, and surveyed remittances give −$6.7bn. It is a proposal and has
not been adopted, so it stays out of the central count, out of both conventions' nets and out of the
adopted total; the registry signs it +4.05 from other residents' side and allocates it to no one. Two
gates check it: the lane's adopted band equals the engine's to 5e-5bn, and its change equals its band
minus the adopted band. Every net is byte-identical to the run before the row was added.
[DATA: `consumption_key_2026_09_24/derived/engine_summary.json`]

**Before and after the rule.** Only the "with proposed" net changes. Its allocated sum moves from −$270.97bn to
−$270.62bn: out come vending's +$0.31bn and movers' −$0.66bn. The account and social nets do not change.

| Net, share ahead | Before (a) / (b) | After (a) / (b) |
|---|---:|---:|
| Social net, central (the verdict) | 20.1 / 19.9% | 20.1 / 19.9% |
| With proposed, central | 20.57 / 20.51% | 20.58 / 20.51% |
| With proposed, least costly | 31.64 / 30.80% | 31.63 / 30.79% |
| With proposed, most costly | 10.67 / 10.76% | 10.68 / 10.76% |

**Priced rows beside the account on other counterfactuals.** None of these rows is in any net. $bn a
year, central (low to high); every row, including the inside and overlapping ones, is in
`derived/sister_other_counterfactuals.csv`.

| Lane, row | Who | Channel | $bn | Counterfactual |
|---|---|---|---:|---|
| movers 3 | California state and local budgets | taxes on net income moved to all other states | −0.74 (−0.63 to −1.05) | the net movers stay; a transfer to other states |
| movers 5 | Texas state and local budgets | taxes on the net income moved from California | +0.10 (0.06 to 0.17) | the movers stay in California |
| movers 0 | US-born adults leaving California who cite conditions | moving costs | −0.03 (−0.01 to −0.09) | without the conditions they cite they stay; "an upper bound for moves driven by ethnic composition, which the category cannot isolate" |
| vending 0 | licensed restaurant owners | sales after legalization | +0.16 (−0.16 to +0.47) | California before SB 946 |
| vending 2 | restaurant workers | payroll after legalization | +0.17 (−0.17 to +0.50) | California before SB 946 |
| vending 1 | licensed restaurant owners | bound: every street-food dollar taken from restaurants | −0.41 (0 to −1.17) | no street-food vending at all |
| vending 4 | vendors | net income of street-food vendors | +0.04 (0.02 to 0.09) | no street-food vending at all |
| vending 8, 9 | budget | sales tax not remitted; City of LA program net of permits | −0.014; −0.004 | all vending sales taxed; no city vending program |
| compliance 1 | noncompliant employers in construction | workers' compensation premiums avoided | +1.31 (0 to 2.24) | the same workers paid on the books at the same gross wage |
| compliance 2, 3 | noncompliant employers; their off-books workers | wage-and-hour underpayment | +0.59; −0.59 (0 to ±2.26) | paid what wage-and-hour law requires |

The other allocation rules still apply:

- **Explicit key:** an explicit `key` column wins. Otherwise `key_map.csv` patterns decide, and a row with
  no defensible key stays in the role table.
- **Future taxpayers and bounds:** rows naming future taxpayers, and rows that are bounds, are never
  allocated.
- **Sign conventions:** two occur among the lanes, and both are read.
  - A central value of zero or more is an amount along the row's direction.
  - A loss row with a negative central is read as signed changes.
  - A gain row with a negative central is refused as ambiguous.
- **Templates:** `key_templates.csv` lists the templates with their CPS populations.
- **State words:** "City of LA" maps to California, not Louisiana.

## Method

- **Base.** `distribution_weights_2026_09_23` is loaded from git at 7ec7144, the commit that moved it to
  September 24, so later working-tree edits cannot change this lane. Its frame is reused unchanged:
  - 295.83m other residents in CPS ASEC 2025;
  - the SPM ranking, the tax key and the NCVS key;
  - the ACS and SCF housing cells.
- **Fiscal case.** `specs.cjs` evaluates the explorer engine on the 64 main-case specifications for the
  September 23 and September 24 models. It copies the specification grid of `package.cjs` without loading
  it, because loading it writes a file in another lane.
  - Per specification, fiscal = A + F and wages = P.
  - The frame's A at the band ends is the base's `fiscal_totals("sept24")`; F is the account's own.
- **Channel allocation.**
  - Fiscal: the debt lane's federal part. Today's share goes by federal tax share or per person; the
    state-local part goes by state, in proportion to where the group lives.
  - Wages: the account's own split (high school or less, cash, scaled ×1.5155 under GDP normalization).
  - Rent: renters, landlords and owners are raked to ACS income cells and state totals.
  - Crime, unreimbursed care and congestion: by the states where the group lives or drives, then by the
    base keys within each state.

## Gates

443 pass; the script stops on the first failure. Twelve pytest positive controls pass (synthetic frame,
sister ingestion, the counterfactual rule and its gate, SPM pooling, rake, fallbacks). Against the 434 of
the run before the counterfactual rule, seven fewer sister rows are allocated, each with three closure
gates (−21). These gates are new:

- the counterfactual gate (+1);
- four on the generation split (+4);
- two on the consumption proposal (+2);
- twenty on the pooling (+20): SPM units nest in households, pooling keeps every channel's total at every
  level (worst 3.1e-14bn), and the 18 pooled nets close;
- three on ruling 5 and the remittance fix (+3): the published totals sit on their bands, Banxico CE167
  matches the consumption lane's corridor, and the corridor needs over three times the surveyed amount.

- **Bands:** both bands reproduce `main_case_bands.csv`: 200.8752–246.3184 and 203.2070–249.6400.
- **Closure, headline:** CPS wages plus the engine's A + F equal the adopted cost in all 128 case ×
  specification pairs (max gap 2.4e-10bn).
- **Band ends with the shared A:** the frame's inside channels plus the future taxpayers' part equal the
  band ends to 4.9e-5bn. The difference is `fiscal_totals` rounding, and the tolerance is 1e-3.
- **Closure, persons:** persons sum to every channel's total at low, central and high, and to every
  sister row.
- **Regression:** both base tables reproduce to 2.8e-14bn: September 23 at 5b8957e and September 24 at
  7ec7144. Each gate first checks that the target file holds its case.
- **Shared inputs:**
  - the debt lane's September 24 band equals the engine's;
  - the interest is pinned at 28.3387 / 36.4297;
  - housing matches ladder 190's four values to 5e-6;
  - the crime figures are the lanes' own.
- **Cuts:** all eleven cuts sum to the frame [`derived/cut_reconciliation.csv`].

## Limits

- **State-local incidence:** it uses national ITEP rates by income group, not state rates (Texas taxes are
  more regressive).
- **Wages:** they are national; the account's nest has no local labour markets.
- **Missing CPS items:** CPS has no school type, no gross rents and few restaurant owners.
- **Landlords:** they are assumed to live in the state where the rent is paid.
- **Excluded from the nets:** the debt legacy, the owners' stock gain and the side views.
- **Unit of account:** the person count gives wages to the earner and shares taxes and rent within the
  household; the pooled variant shares everything within the SPM unit. Neither measures how families
  actually share income [FRAMING-SENSITIVE].

**Would change it:**

- State-specific tax incidence, or a state-level fiscal account, would change the geography of the fiscal
  row, and that geography drives the state gap.
- A local-labour-market wage model would concentrate the wage loss in the group's states.
- The parent's choices of financing convention and of the unit (person count or pooled SPM unit: 20.1%
  and 19.9% against 23.9% and 21.4% ahead) [FRAMING-SENSITIVE].
- The consumption lane's proposed key (6841b39, not adopted) would lower the main case by $4.05bn, to
  $196.8–242.3bn (variants −$2.6bn to −$8.4bn), and the fiscal channel with it. It is listed in the
  registry and is in no net.

## Files

- Run from the repository root:
  - `node infra/immigration-fiscal/winners_losers_2026_09_24/specs.cjs`
  - `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py`
  - `... -m pytest infra/immigration-fiscal/winners_losers_2026_09_24/ -q`
- [2026-09-26] Both scripts take `--case sept26_schools` (the default), `sept26` or `sept24`, and
  `--out-dir DIR` (default `derived/`); give both the same flags. The regression and quintile files
  are named by case: the schools run writes `regression_sept26.csv`, `regression_sept26_schools.csv`
  and `quintiles_vs_base_sept26_schools.csv`. `old_new.py` writes the three cases' old → new table to
  `../sept26_propagation_2026_09_26/derived/old_new_ledger.csv`.
- The September 24 run wrote these files. [2026-09-27, parent: `derived/` now holds the schools-case
  run of the same names plus its three case-named files. The September 24 run's `regression_sept23.csv`,
  `regression_sept24.csv` and `quintiles_vs_base_sept24.csv` stay, unchanged from 8a762fe, because the
  regression paragraph above cites them.]
  - `channels.csv`, `winners_losers_table.csv`, `person_nets_by_cut.csv`, `cuts.csv` (every channel at
    every level in every cut) and `cut_reconciliation.csv`;
  - `net_shares.csv` (`unit`: `person` or `spm_unit_pooled`), `pooling_moves.csv`, `winners_tree.csv`,
    `winner_cells.csv` and `group_frame.csv`;
  - `role_table.csv`, `sister_other_counterfactuals.csv`, `key_templates.csv` and
    `naics_census_industry.csv`;
  - `fiscal_specs.csv`, `fiscal_lines_band_ends.csv` and `fiscal_federal_split.csv`;
  - `regression_sept23.csv`, `regression_sept24.csv` and `quintiles_vs_base_sept24.csv`;
  - `inputs.json`, `gates.json` and `sources_manifest.csv`. The manifest pins every input by sha256,
    including the git blobs read at b42efdc, 7ec7144 and 5b8957e.
- `key_map.csv` holds the sister-row patterns.
- The person frame is `_cache/person_frame.parquet` (ignored). It carries `SPM_ID` and the pooled nets.
- Nothing outside this directory was edited, and nothing was committed.

Model self-report: claude-opus-5-5[1m], lane agent, 2026-09-24/25.

## v4 case (sept29), 2026-09-29

**Verdict:** On the v4 case ($371.4146 / $434.8410bn), pooled within SPM units, 17.9% of other residents come out ahead under tax-share financing (a) and 17.1% under per-person cuts (b), against 17.8% and 17.0% on September 27; the stacks give 11.1–24.4% under (a). The person count gives 16.9% under both, as on September 27. Taxpayers' fiscal channel is $394.4bn at central values (September 27: $349.3bn). Of it, $74.9bn is the pension accrual, which nothing finances in 2024. It sits with the future payers of Social Security and Medicare, beside the borrowed part ($13.1bn), and is not allocated to anyone living today. So the social net on today's residents falls in size, from −$386.6bn to −$360.6bn, while the case rises $48.5bn. The capped programs, now including public housing's deficit, fall on eligible households without the aid: $8.1bn (was $5.1bn). The group's own rows are now on the account's count, 39.71m members, with the CPS's 40.9m beside them. [CALCULATION: `specs.cjs --case sept29` and `winners_losers.py --case sept29`, pinned; `derived/sept29/`] [FRAMING-SENSITIVE: the accrual's payer]

claude-opus-5-5

**What runs.** `node specs.cjs --case sept29` evaluates the September 27 case (its band variant `sept27_case` in the adopted lane's `main_case_bands.csv`) and the adopted case with their own packages. `winners_losers.py --case sept29` allocates the adopted case and keeps September 27 as the positive control. Both write to `derived/sept29/`; `derived/` keeps the September 27 run. Pins in `CASES["sept29"]`:
- the distribution lane at 492bf32 (`derived/sept29/`, `case_ends_sept29.json`);
- the debt lane at 7e1b500 (`derived/sept29/`: `stocks.csv`, `summary.json` and the per-correction files);
- the generation account at aa1f53b (`generation_results_sept29.csv`);
- the propagation lane at 911afa6 (`sept24_propagation_2026_09_24/derived/sept29/`). As for every case, its real-costs totals and band variants are read from the working tree, which equals 911afa6 (`git diff 911afa6` empty; `sources_manifest.csv` holds their sha256);
- the debt lane's legacy interest (`SEPT29_INTEREST`): 30.7514 / 41.4794, gated at 5e-4 against `stocks.csv` at 7e1b500 (30.751354 / 41.479394);
- the ladder entry is 275 (d40e085), as the lead set; there is no new number.

`--dev-unpinned` is for dry runs before an upstream commit lands. It reads the missing pins' files from the working tree and stops unless `--out-dir` lies outside `derived/` (tested). The dry run used it; the final run does not.

Reproduce, from the repository root:
- `node infra/immigration-fiscal/winners_losers_2026_09_24/specs.cjs --case sept29`
- `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py --case sept29`

**Channels, central values, $bn a year** (`derived/sept29/channels.csv`):

| Channel | September 27 | September 29 |
|---|---:|---:|
| Adopted main case, other residents' net (fiscal + wages) | −354.6 | −403.1 |
| Fiscal channel (taxpayers) | −349.3 | −394.4 |
| — cash financed today | −291.2 | −260.6 |
| — return on public capital (never borrowed) | −44.7 | −45.8 |
| — federal part financed by borrowing (future taxpayers) | −13.4 | −13.1 |
| — pension accrual (future payers of Social Security and Medicare) | — | −74.9 |
| Displaced beneficiaries of the capped programs | −5.1 | −8.1 |
| Wages (production on row 4) | −0.2 | −0.6 |
| Social net on today's residents | −386.6 | −360.6 |
| Debt legacy interest (beside, never added) | 30.9–41.6 | 30.8–41.5 |

The channels outside the budget do not change: renters −33.9, landlords +37.4, victims −30.9, congestion −13.0, unreimbursed care −4.4 and the rest. Each is taken as its lane publishes it. Those lanes price the CPS's 40.9m, not the account's 39.71m: each pins the union at 40,896,574 (housing_transfer `arms.py` TARGET, which scales the ACS metro counts to it; congestion and its long-run re-derivation; care; scale spillovers; labor mobility; the victim lane's target population). This lane does not re-estimate them. Where a channel is linear in the count, the first-order correction is × 0.971 (39.712 / 40.897), about $1.3bn on the social net of today's residents. [INFERENCE; not computed]

**Share of other residents ahead** (`net_shares.csv`, the social net, central; stacks least to most costly in brackets):

| Count | (a) tax-share | (b) per person |
|---|---|---|
| Pooled within SPM units | 17.8 → **17.9** (11.1–24.4) | 17.0 → **17.1** (11.4–22.4) |
| Person | 16.9 → **16.9** (12.5–20.9) | 16.9 → **16.9** (12.5–20.8) |

The share barely moves. The accrual leaves today's persons, and the rest of the case's rise falls on the same payers in the same proportions.

**The group itself, on the account's count** (`group_frame.csv`; the CPS's published weights in `group_frame_cps_published.csv`):

| Item | Row 4 (39.71m) | CPS published (40.90m) |
|---|---|---|
| Direct fiscal transfer received (A, sign flipped), $bn | +412.8 (383.1–442.5) | the same |
| — per member | $10,395 | $10,094 |
| First generation's market gain over its Mexico earnings, $bn | +201.9 (176.6–218.2) on $340.1bn of US earnings, 11.04m members | +224.6 (196.5–242.8) on $378.4bn, 12.22m |
| — per Mexico-born member | $18,290 | $18,377 |
| Wage competition among the group's own workers, high school or less (ε ∞), $bn | −18.4 (−14.6 to −22.2) | −19.5 |
| Same, ε 3 | −31.6 | −34.7 |
| Wage gain of the group's workers with some college or more (ε ∞) | +5.3 | +5.5 |
| Victims inside the group, per member | −$506 | −$492 |
| The account's split by generation (minors with their parents), $bn | G1 169.4–197.4, G2 110.7–121.8, G3+ 91.4–115.6 | the same (the account's own rows, on row 4) |

[CALCULATION: `derived/sept29/group_frame.csv` against `group_frame_cps_published.csv`]

**Rules designed.**
- **The group frame's count** (the lead's question of 11:23). Every person-based group row is on the account's row-4 weights: A per member, the first generation's earnings and market gain, the group's own wage rows, the victims per member and the member counts. `row4_group_weights` uses the base lane's row-4 rule, the same mask and factors as `v4_inputs.py` (production_row4.json: the Mexico-born naturalized × 0.8556 and noncitizens × 0.7781 outside California and Texas; no other resident moves). It gates the grid file's sha256, each cell's records and CPS population, that only group records move, and the group's count, 39,712,493.33. The published 40.9m frame stays beside it in `group_frame_cps_published.csv`. The counterfactual label names 39.7m. The other residents, the payers, are the same persons on the same weights under both frames. Alternative: keep the published 40.9m frame; its per-member A would divide the 39.71m account's total by 40.90m, 2.9% too low. The one other place the group's weights enter, the cut of the ten states with the most members, keeps its set on row 4: CA, TX, AZ, IL, CO, WA, FL, NC, GA and NV (Nevada and Georgia swap ranks; the cut is membership, so it does not move).
- **The pension accrual** is a fourth financing part (the debt lane's `accrual_bn`, all federal). It goes to the future payers of Social Security and Medicare (`future_pension_accrual`) and is left out of today's persons. Alternative: allocate it today on the federal tax key, as if the trust funds' later outlays were prefunded now (registry note).
- **Production on row 4.** The case's wages and F come from the base lane's row-4 re-solve, gated there against the case's grid; the September 27 control keeps the published rows.
- **Public housing's deficit** is capped like rental assistance, on rental assistance's key (the base's `CAPPED_KEY_OF`).

**The two fiscal-channel centrals.** This lane's $394.4bn is the case's mid, $403.1bn, less −P ($0.6bn) and the capped programs ($8.1bn). The distribution lane's $395.7bn adds $1.3bn of F difference (its central scenario's F, 10.26 against the engine's 8.98 at 48 / 11). The bridge is in the distribution lane's RESULT.

**Gates.**
- Cross-check: at 48 / 11 the fiscal channel's A is −383.094429 / −442.524231 (the base's one definition), and the engine's is −383.094478 / −442.524197. That matches −383.0945 / −442.5242 at the oracle's rounding, 1e-4.
- `specs.cjs --case sept29`: 25 PASS. The band is 371.4146–434.8410 against `main_case_bands.csv` (adopted), the September 27 control gives 321.8194–387.3701 (`sept27_case`), and each has its payload's 13 and 4 line responses.
- `winners_losers.py --case sept29`: exit 0, 524 gates: the dry run's 523 and `debt_legacy_pinned_sept29`. Every figure equals the dry run's; only provenance strings differ (the pins' commits in place of the working tree in `channels.csv`, `group_frame*.csv`, `sources_manifest.csv` and `inputs.json`).
- `scripts/rerun_lane.py` over the four commands (`specs.cjs` and `winners_losers.py`, the default and `--case sept29`), twice: IDENTICAL, 59/59 files both times. The first pass exited 3 only because `test_winners_losers.py` is not a rerun command; the second passed `--allow-unrun` for it and exited 0.
- Old outputs unchanged: no file under `derived/` outside `derived/sept29/` differs from HEAD.
- pytest: 17 passed, including the dry-run test.

**Log (times from `date` calls).**
- 20:58 JST: resumed after the 20:51 reboot. `specs.cjs` and `winners_losers.py` carried the sept29 edits made before it.
- 22:05: `specs.cjs --case sept29` into scratch, 25 PASS.
- 22:05–22:08: `winners_losers.py --case sept29 --dev-unpinned`. The first run stopped on a merge bug in `inputs.json`'s production metadata (a duplicate `weights` key); after the fix, exit 0 with 523 gates.
- 22:17–22:18: rerun_lane on the default case, IDENTICAL 35/35. pytest 17 passed.
- 22:33: the pins landed (debt 7e1b500, generation aa1f53b, propagation 911afa6); `SEPT29_INTEREST` set from `stocks.csv` at 7e1b500. `specs.cjs --case sept29` (25 PASS; both files identical to the dry run's) and `winners_losers.py --case sept29` (exit 0, 524 gates) into `derived/sept29/`, finished before 22:35:40.
- 22:35:40–22:39:14: rerun_lane pass 1, IDENTICAL 59/59 (exit 3: the test file). 22:39:26–22:47:15: pass 2 with `--allow-unrun`, IDENTICAL 59/59, exit 0. 22:47:20: pytest 17 passed.

## v5 case (oct05), 2026-10-05

[2026-10-05: on main case v5 (`oct05`, `../main_case_2026_10_05/`, $390.2940–461.2431bn on the lineage's 42,752,213), pooled within SPM units, **17.6%** of other residents come out ahead under tax-share financing (a) and **16.9%** under per-person cuts (b), against 17.9% and 17.1% on sept29; the stacks give 10.8–24.3% under (a). The person count gives 16.7% and 16.8% (sept29 16.9% and 16.9%). Taxpayers' fiscal channel is **$416.4bn** at central values (sept29 $394.4bn). Of it, the pension accrual ($80.4bn; sept29 $74.9bn) and the borrowed part ($12.6bn; sept29 $13.1bn) go to future payers, so the social net on today's residents is **−$378.2bn** (sept29 −$360.6bn). The capped programs fall on eligible households without the aid: $8.8bn (sept29 $8.1bn). The group's own rows are on the lineage, 42.75m members, with the 3.04m added people placed at the identified third-plus generation's records [ASSUMPTION]; the direct transfer A is **$10,191 per member** (sept29 $10,395 on 39.71m). [CALCULATION: `specs.cjs --case oct05` and `winners_losers.py --case oct05`; `derived/oct05/`]]

claude-opus-5-5 (v5consC)

**What runs.** `node specs.cjs --case oct05` evaluates the September 29 case (band variant `sept29_case` in v5's `main_case_bands.csv`) and the adopted case with their own packages. `winners_losers.py --case oct05` allocates the adopted case and keeps September 29 as the positive control. Both write to `derived/oct05/`; `derived/` (September 27) and `derived/sept29/` are as they were. Pins in `CASES["oct05"]`:
- the distribution lane at fecaae7e (`derived/oct05/`, `case_ends_oct05.json`);
- the debt lane at 604b09e1 (`derived/oct05/`);
- the generation account at e5ca5efe (`generation_results_oct05.csv`);
- the propagation lane at 72f2e3bc (`sept24_propagation_2026_09_24/derived/oct05/`). As for every case, its real-costs totals and band variants are read from the working tree, which equals 72f2e3bc (`git diff 72f2e3bc` empty; `sources_manifest.csv` holds their sha256);
- the debt lane's legacy interest (`OCT05_INTEREST`): 30.6288 / 42.6236, gated at 5e-4 against `stocks.csv` at 604b09e1 (30.628803 / 42.623603);
- the ladder entry, 281.

**Channels, central values, $bn a year** (`derived/oct05/channels.csv`):

| Channel | September 29 | October 5 |
|---|---:|---:|
| Adopted main case, other residents' net (fiscal + wages) | −403.1 | −425.8 |
| Fiscal channel (taxpayers) | −394.4 | −416.4 |
| — cash financed today | −260.6 | −273.9 |
| — return on public capital (never borrowed) | −45.8 | −49.5 |
| — federal part financed by borrowing (future taxpayers) | −13.1 | −12.6 |
| — pension accrual (future payers of Social Security and Medicare) | −74.9 | −80.4 |
| Displaced beneficiaries of the capped programs | −8.1 | −8.8 |
| Wages (production on row 4, with the lineage's delta) | −0.6 | −0.6 |
| Social net on today's residents | −360.6 | −378.2 |
| Debt legacy interest (beside, never added) | 30.8–41.5 | 30.6–42.6 |

The channels outside the budget do not move: renters −33.9, landlords +37.4, victims −30.9, congestion −13.0, unreimbursed care −4.4 and the rest, together −$45.4bn in the social net. Their lanes price the CPS's 40.9m. Had they priced the lineage's 42.75m in proportion, the social net would carry about $2.1bn more (× 1.045) [INFERENCE; not computed: the added people resemble the G3+ and third-plus whites more than the union's average, so the proportional figure is rough].

**Share of other residents ahead** (`net_shares.csv`, the social net, central; stacks most to least costly in brackets):

| Count | (a) tax-share | (b) per person |
|---|---|---|
| Pooled within SPM units | 17.9 → **17.6** (10.8–24.3) | 17.1 → **16.9** (11.2–22.4) |
| Person | 16.9 → **16.7** (12.2–20.8) | 16.9 → **16.8** (12.3–20.8) |

The case rises $22.6bn at central values, and the rise falls on the same payers, so the share ahead slips by 0.1–0.3 points.

**The group itself, on the lineage** (`group_frame.csv`; the CPS's published weights in `group_frame_cps_published.csv`):

| Item | September 29, row 4 (39.71m) | October 5, lineage (42.75m) |
|---|---|---|
| Direct fiscal transfer received (A, sign flipped), $bn | +412.8 (383.1–442.5) | +435.7 (402.2–469.1) |
| — per member | $10,395 | $10,191 |
| First generation's market gain over its Mexico earnings, $bn | +201.9 (176.6–218.2), 11.04m members | the same: no first-generation member is added |
| Wage competition among the group's own workers, high school or less (ε ∞), $bn | −18.4 (−14.6 to −22.2) | −19.8 (−15.7 to −23.9) |
| Same, ε 3 | −31.6 | −32.8 |
| Wage gain of the group's workers with some college or more (ε ∞) | +5.3 | +5.9 |
| Victims inside the group, per member | −$506 | −$470 |
| The account's split by generation (minors with their parents), $bn | G1 169.4–197.4, G2 110.7–121.8, G3+ 91.4–115.6 | G1 169.3–197.3, G2 110.6–121.7, G3+ 110.5–142.2 |

The victims row is the victim lane's −$20.1bn for the identified members over the larger count; the added people's own victimisation is not priced [not computed]. The wage rows move by the lineage's production delta (each scenario's wage changes × λ, 1.022 for high school or less) and by the added people's earnings at the G3+ records. [CALCULATION: `derived/oct05/group_frame.csv`; the sept29 column from `derived/sept29/group_frame.csv`]

**Rules designed.**
- **The added people at the G3+ distribution** [ASSUMPTION; the Consumers row's second option]. The case prices 1.957m of them at identified G3+ members' amounts and 1.083m at third-plus non-Hispanic whites' amounts at the G3+'s ages (`meta.lineage.members`). The CPS cannot see them, so `lineage_group_weights` raises each identified G3+ member's row-4 weight by 1.211937 (= 1 + 3,039,719.6 / 14,342,574.6) over 6,351 records. All 3.04m then take the G3+ members' earnings, schooling and nativity. G3+ is the generation account's mask (`frame.py`: US-born, both parents born in US areas, PRDTHSP 1, inside the group). Gates (1e-9 relative):
  - the group on row 4 is the account's union, 39,712,493.33;
  - its G3+ is the identified G3+, 14,342,574.61;
  - the lineage is 42,752,212.92, and its G3+ is the generation split's 17,382,294.20;
  - only G3+ records move, and the counterfactual label's counts are the case's.

  This rule moves A per member, the group's own wage rows, the victims per member and the US-born count; the first generation's rows stay put. Alternative: leave the added people out of the group's rows and state the count. The rows stay on 39.71m, and A per member, $10,971, would put the 42.75m account's total over 39.71m, 7.7% too high.
- **The other residents keep the CPS frame** [ASSUMPTION], the distribution lane's rule 4. The added people sit among them unfound (about 3.04m of 295.83m, 1.03%), so the shares ahead count them among payers and winners, and under (b) they carry about 1% of today's fiscal channel [INFERENCE: their share of the frame].
- **The group's geography stays on the identified members' published weights**, as in every case [ASSUMPTION]. It decides where the state-local cost, victims' harm and uncompensated care arise. Alternative: the lineage weights would move $5.6bn of the $287.8bn central state-local cost between states (Texas +$3.5bn, California +$1.8bn, Illinois −$0.9bn). Row 4's reweighting alone moves $4.8bn (sept29 did not apply it either); the added people on top of row 4 move $2.4bn. [CALCULATION: scratch, state shares of `lineage_group_weights` and `row4_group_weights` against the published weights]
- **Both cases have production grids.** September 29's scenarios are now its own row-4 re-solve, not the published rows; its regression against 492bf32 passes (5.7e-14bn). The case's scenarios are the same re-solve plus the distribution lane's `lineage_rows` (`production_rows`). Gates: `account_production_term_case_grid` and `account_production_term_sept29_grid` (1e-6bn), and `production_rows_add_to_the_previous_case_s` (the same grid file, factors and GDP factor, with the lineage built on September 29's lane).
- **The debt lane's correction lines.** v5's lines carry the added people's part of each correction line, which the per-correction file holds as components of their own (`v5_lineage`, `v5_union_response`). `per_correction_check` takes those parts on the correction lines from the by-line file (`corrections_federal_split_2024.csv`), gated to rebuild the two components (3e-6bn); the check then closes at 2e-6bn (tolerance 1e-5).

**The two fiscal-channel centrals.** This lane's $416.4bn is the case's mid, $425.8bn, less −P ($0.6bn) and the capped programs ($8.8bn). The distribution lane's $417.6bn adds $1.2bn: the engine's F at 48 / 11 (mean 10.49) less its central scenario's (9.28). Unrounded, 416.3716 + 1.2069 = 417.5785.

**Gates.**
- Cross-check: at 48 / 11 the fiscal channel's A is −402.241371 / −469.102418 (the base's one definition), and the engine's is −402.241420 / −469.102384 (gate 1e-3).
- `specs.cjs --case oct05`: 25 PASS. The band is 390.2940–461.2431 (`adopted`); the September 29 control gives 371.4146–434.8410 (`sept29_case`).
- `winners_losers.py --case oct05`: exit 0, 538 gates (sept29: 524). Both regressions against the distribution lane pass, September 29 at 492bf32 and oct05 at fecaae7e: max |diff| 5.7e-14bn over 828 cells each.
- `scripts/rerun_lane.py` over six commands (`specs.cjs` and `winners_losers.py`: the default, `--case sept29` and `--case oct05`): **IDENTICAL 83/83, exit 0** (2026-10-06 00:58:33–00:59:45 JST).
- Old outputs unchanged: `git status` shows nothing under `derived/` outside the new `derived/oct05/`.
- pytest: 17 passed.

**Reproduce (oct05).**
- `node infra/immigration-fiscal/winners_losers_2026_09_24/specs.cjs --case oct05`
- `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py --case oct05`

**Log (2026-10-06 JST; times from `date` calls and the run files' timestamps).**
- 00:44:56: `specs.cjs --case oct05` into scratch, 25 PASS.
- 00:54:31–00:54:41: the first scratch run of `winners_losers.py --case oct05` stopped at `debt_lines_carry_per_correction_split` (0.199bn): v5's lines carry the added people's part of the correction lines. Fixed by reading those parts from the by-line file.
- 00:56:11–00:56:37: scratch run, exit 0, 538 gates.
- 00:57:41: `specs.cjs --case oct05` in place, identical to the scratch files. 00:57:46–00:58:11: `winners_losers.py --case oct05` in place, exit 0, 538 gates; every output equals the scratch run's except `sources_manifest.csv` (the specs path).
- 00:58:33–00:59:45: rerun_lane, IDENTICAL 83/83, exit 0. 00:59:51: pytest 17 passed.

## v6 case (oct07), 2026-10-07

[2026-10-07: on main case v6 (`oct07`, `../main_case_2026_10_07/`, $389.0826–461.4797bn on the lineage's 42,752,213), pooled within SPM units, **17.5%** of other residents come out ahead under tax-share financing (a) and **16.8%** under per-person cuts (b), against 17.6% and 16.9% on oct05; the stacks give 10.5–24.2% under (a). The person count gives 16.7% and 16.7% (oct05 16.7% and 16.8%). Taxpayers' fiscal channel is **$415.9bn** at central values (oct05 $416.4bn). Of it, the pension accrual ($78.9bn; oct05 $80.4bn) and the borrowed part ($13.2bn; oct05 $12.6bn) go to future payers, so the social net on today's residents is **−$378.6bn** (oct05 −$378.2bn). The capped programs fall on eligible households without the aid: $8.8bn (oct05 $8.8bn). The group's own rows stay on the lineage, 42.75m members, with the 3.04m added people now placed at the identified third-plus generation's records of their own five-year age band [ASSUMPTION]; the direct transfer A is **$10,178 per member** (oct05 $10,191). [CALCULATION: `specs.cjs --case oct07` and `winners_losers.py --case oct07`; `derived/oct07/`]]

claude-opus-5-5 (prop-c)

**What runs.** `node specs.cjs --case oct07` evaluates v5 (band variant `oct05_case` in v6's `main_case_bands.csv`, through `P.OCT05`) and v6 with their own packages. `winners_losers.py --case oct07` allocates v6 and keeps v5 as the positive control. Both write to `derived/oct07/`; `derived/` (September 27), `derived/sept29/` and `derived/oct05/` are as they were. Pins in `CASES["oct07"]`:
- the distribution lane at 498a6a71 (`derived/oct07/`, `case_ends_oct07.json`);
- the debt lane at 0485e5a2 (`derived/oct07/`);
- the generation account at 3f583fb4 (`generation_results_oct07.csv`);
- the propagation lane's `sept24_propagation_2026_09_24/derived/oct07/`, read from the working tree as every case's is. It was committed after the run, in b0a2ccac, unchanged: `sources_manifest.csv`'s sha256 of the two files read (`real_costs_totals.csv`, `band_variants.csv`) are the committed files';
- the debt lane's legacy interest (`OCT07_INTEREST`): 31.8233 / 44.1693, gated at 5e-4 against `stocks.csv` at 0485e5a2 (31.823258 / 44.169319);
- the ladder entry, 295.

**Channels, central values, $bn a year** (`derived/oct07/channels.csv`):

| Channel | October 5 | October 7 |
|---|---:|---:|
| Adopted main case, other residents' net (fiscal + wages) | −425.8 | −425.3 |
| Fiscal channel (taxpayers) | −416.4 | −415.9 |
| — cash financed today | −273.9 | −275.0 |
| — return on public capital (never borrowed) | −49.5 | −48.8 |
| — federal part financed by borrowing (future taxpayers) | −12.6 | −13.2 |
| — pension accrual (future payers of Social Security and Medicare) | −80.4 | −78.9 |
| Displaced beneficiaries of the capped programs | −8.8 | −8.8 |
| Wages (production on row 4, with the lineage's delta) | −0.6 | −0.6 |
| Social net on today's residents | −378.2 | −378.6 |
| Debt legacy interest (beside, never added) | 30.6–42.6 | 31.8–44.2 |

The channels outside the budget do not move: renters −33.9, landlords +37.4, victims −30.9, congestion −13.0, unreimbursed care −4.4 and the rest, together −$45.4bn in the social net. The federal part of the fiscal channel rises: $1.56bn more is financed by today's federal taxes and $0.58bn more by borrowing, while the state-local part falls $1.15bn.

**Share of other residents ahead** (`net_shares.csv`, the social net, central; stacks most to least costly in brackets):

| Count | (a) tax-share | (b) per person |
|---|---|---|
| Pooled within SPM units | 17.6 → **17.5** (10.5–24.2) | 16.9 → **16.8** (11.0–22.3) |
| Person | 16.7 → **16.7** (12.1–20.7) | 16.8 → **16.7** (12.2–20.7) |

The case falls $0.49bn at central values, but the pension accrual, which future payers carry, falls $1.48bn and the borrowed part rises $0.58bn. Today's residents therefore carry $0.41bn more, and the share ahead slips by 0.1–0.2 points.

**The group itself, on the lineage** (`group_frame.csv`; the CPS's published weights in `group_frame_cps_published.csv`):

| Item | October 5, lineage (42.75m) | October 7, lineage by age band (42.75m) |
|---|---|---|
| Direct fiscal transfer received (A, sign flipped), $bn | +435.7 (402.2–469.1) | +435.2 (401.0–469.3) |
| — per member | $10,191 | $10,178 |
| First generation's market gain over its Mexico earnings, $bn | +201.9 (176.6–218.2), 11.04m members | the same: the age rule moves only G3+ records |
| Wage competition among the group's own workers, high school or less (ε ∞), $bn | −19.8 (−15.7 to −23.9) | −19.7 (−15.6 to −23.8) |
| Same, ε 3 | −32.8 | −32.7 |
| Wage gain of the group's workers with some college or more (ε ∞) | +5.9 | +5.9 |
| Victims inside the group, per member | −$470 | −$470 |
| The account's split by generation (minors with their parents), $bn | G1 169.3–197.3, G2 110.6–121.7, G3+ 110.5–142.2 | G1 168.9–196.8, G2 109.5–120.6, G3+ 110.7–144.1 |
| The added people: under 20; earnings, $bn | 46.7%; 71.0 (one factor) | 51.2%; 65.3 (by age band) |

The wage rows move by the lineage's smaller production delta (λ 1.0191 for high school or less, v5 1.0222) and by the added people's earnings at the G3+ records, which the younger mix lowers. [CALCULATION: `derived/oct07/group_frame.csv`, `inputs.json` `group.lineage.age_bands`; the oct05 column from `derived/oct05/group_frame.csv`]

**Rules designed.**
- **The items reach this lane through its upstream files.** The engine run (`specs.cjs`) applies the whole payload, so every item's lines and capital components are in the band ends' lines, including the user-fee item's four offset components (28 components, 24 on v5) and its three carrier receipt lines (at zero response, no effect). The direct response A comes from the distribution lane's `fiscal_totals("oct07")`, the federal split and the pension accrual from the debt lane, and the group's split by generation from the generation account.
- **The added people at their measured ages** [ASSUMPTION]. v6 prices the 3.04m at the age mixes the age-mix lane measured (`meta.lineage.age_mix`): the 1.945m G3-rate persons at one mix and the 1.095m later losses at another. The group frame therefore raises each identified G3+ record by the added people of its five-year band over the identified G3+ of that band (`age_band_factors`, `LINEAGE_AGE_RULE`), not by one factor. All of them still take the G3+ members' records, band by band. The factors run from 1.141 (50 on) to 1.249 (20–24); v5's single factor, 1.211937, remains the G3+ total's. Gates (the age-mix gates, five new):
  - the bands are five years wide with an open top (17 bands, 80 on);
  - the two parts add to the added count, 3,039,719.6;
  - each band's added people are the case's (7.1e-16 relative);
  - every band they reach holds identified records;
  - the frame's identified mix is the case's (1.4e-8), a positive control that both read the same members.

  Their under-20 share is 51.2% (46.7% under one factor), and their earnings are $65.3bn ($71.0bn). The rule moves the group's own wage rows and age profile; the count and A are the case's. Alternative: keep v5's single factor, which gives the added people the identified G3+'s ages, an assumption the case no longer makes.
- **Both cases' production grids add to September 29's.** v5 and v6 each re-solve September 29's grid with their own added people (the base lane's `LATER_CASES`). The gate that ties the case's production rows to the case before's now compares the two additions' base (`production_rows_add_to_the_previous_case_s`: base and `previous_case_s_base` both `main_case_2026_09_29`); oct05's gate record is unchanged. `account_production_term_case_grid` and `account_production_term_oct05_grid` pass (1e-6bn).
- **The debt lane's correction lines carry the v6 items.** The per-correction file has two new components: `v6_retiree_health` (by line `v6_retiree_health:scale`, nine lines) and `v6_user_fees`. The pension item is set-only and has no cash component. `per_correction_check` takes their rows from the by-line file (`corrections_federal_split_2024.csv`) as it takes the lineage's. `v6_user_fees`' rows on `school_reprice` and `college_rekey` join the lineage's on the education check, and no item touches the lane constants. Gates: the by-line file rebuilds the components, the v6 items included, to 8.0e-6bn over 24 rows (tolerance 1e-5). The largest gap is `v5_lineage`'s, the six-decimal rounding of its 74 by-line rows; the v6 items rebuild to 2e-6bn. The check then closes at 2.0e-6bn over 12 rows (tolerance 1e-5).

**The two fiscal-channel centrals.** This lane's $415.9bn is the case's mid, $425.3bn, less −P ($0.6bn) and the capped programs ($8.8bn). The distribution lane's $417.1bn adds $1.2bn: the engine's F at 48 / 11 (mean 10.46) less its central scenario's (9.24). Unrounded, 415.8860 + 1.2170 = 417.1030, the level the distribution lane's bridge predicted.

**Gates.**
- Cross-check: at 48 / 11 the fiscal channel's A is −400.992149 / −469.314126 (the base's one definition), and the engine's is −400.992198 / −469.314093 (gate 1e-3).
- `specs.cjs --case oct07`: 25 PASS. The band is 389.0826–461.4797 (`adopted`); the oct05 control gives 390.2940–461.2431 (`oct05_case`).
- `winners_losers.py --case oct07`: exit 0, 543 gates (oct05: 538; the five new are the age-mix gates). Both regressions against the distribution lane pass, oct05 at fecaae7e (5.7e-14bn) and oct07 at 498a6a71 (1.4e-14bn), over 828 cells each. Peak RSS 2.07 GB.
- `scripts/rerun_lane.py` over nine commands (`specs.cjs` and `winners_losers.py` for the default, sept29, oct05 and oct07, and `pytest`): **IDENTICAL 107/107, exit 0** (2026-10-07 15:39:17–15:41:31 JST).
- Old outputs unchanged: `git status` shows nothing under `derived/` outside the new `derived/oct07/`.
- pytest: 18 passed, `test_age_band_factors_place_the_added_people_at_their_mixes` among them.

**Reproduce (oct07).**
- `node infra/immigration-fiscal/winners_losers_2026_09_24/specs.cjs --case oct07`
- `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py --case oct07`

**Log (2026-10-07 JST; times from `date` calls).**
- 13:20: `--case oct07` coded: a `specs.cjs` entry, `CASES["oct07"]` with empty pins, the production-rows gate generalized, the age-band frame and its test. `winners_losers.py --case oct05` rebuilt `derived/oct05/` byte for byte (538 gates).
- 13:32: a dry run (`--dev-unpinned`) in a mirror passed both regressions (oct05 5.7e-14bn, oct07 1.4e-14bn) and the one-definition A (+4.9e-5 / −3.4e-5bn), then stopped where the debt lane had no `oct07` files yet.
- 14:29: `per_correction_check` takes the debt lane's v6 components; `--case oct05` rebuilt byte for byte again.
- 15:29:47–15:29:48: `specs.cjs --case oct07` in place, 25 PASS.
- 15:37:34–15:38:07: `winners_losers.py --case oct07` in place on the pins: exit 0, 543 gates.
- 15:39:17–15:41:31: rerun_lane, IDENTICAL 107/107, exit 0. 15:41:42–15:41:43: pytest 18 passed.
- 16:12:35–16:28:16: `debt_by_line_file_rebuilds_lineage_components` now takes the six-decimal rounding bound as its tolerance, per component, in place of the fixed 1e-5 above: the rows summed in both files × 5e-7. On oct07 the largest gap is 8.0e-6bn (v5_lineage, 76 rows, bound 3.8e-5), and the closest to its bound is v6_user_fees low/high, 2.0e-6 against 3.0e-6bn. The run prints the bound. Moving one by-line row by 1e-4bn fails the gate on oct05 and on oct07. Outputs unchanged: rerun_lane over the nine commands on the final script, 16:26:14–16:28:16, IDENTICAL 107/107, exit 0.

## v7 case (oct14), 2026-10-14

**Verdict:** The lane now computes only oct14, beside the frozen oct07 files. The set band is $339.5520–423.6493bn at personal specifications 16 / 11. In the social net pooled within SPM units, 19.6% of other residents are ahead under tax-share financing (a), 18.7% under per-person financing (b); the central net allocated to today's residents is −$341.7338bn. The fiscal channel is −$372.2055bn centrally. These are this lane's allocation results, with future borrowing and pension-accrual payers kept beside today's persons under the existing financing rule. [CALCULATION: `derived/oct14/fiscal_specs.csv`, `net_shares.csv` (`net_social_a/b`, `central`, `spm_unit_pooled`), `channels.csv` (`fiscal`)]

**Rules and inputs.** R5 takes v7's 32 personal `MAIN_SPECS`; R6–R9 enter through the whole payload and the upstream split files. Receipt overrides in `specs.cjs` now take the specification's reading, including corporate 1 low / 0.37 high. Pins: distribution 17d3735a, debt 6b1250b9, generation 1a02fbbb. The propagation files are oct14's at c392d356, read from the working tree and hashed in `sources_manifest.csv`. The oct07 positive control loads its own frozen distribution module at 498a6a71, since the live distribution module computes only oct14; its outputs are not regenerated. The debt lane delivers v7 edit sets under its `v6_` component namespace, so the existing component check covers them unchanged. No gate tolerance changed.

**Checks.** `specs.cjs --case oct14`: 27 PASS, 96 rows (64 for the frozen v6 control, 32 personal for v7), 440 line rows. The package-cost gate is 1e-9, published-band gate 1e-4; the personal-grid and recorded end specifications are checked explicitly. The person run passes 511 gates. Both 828-cell distribution regressions close to at most 5.7e-14bn. Live A is −351.4616627 / −431.4836439bn, within 4.6e-13bn of the engine (existing tolerance 1e-3). The debt component rebuild closes within each unchanged six-decimal rounding bound, largest gap 9e-6bn. The existing generation split gates pass at their documented 1e-3 tolerance. Eighteen pytest controls pass; Python compile check passes. The final standalone person run took 29.77s, peak RSS 2,350,399,488 bytes, measured with Python `time.perf_counter` / `resource.getrusage`.

**Reproduce the live case.**
- `node infra/immigration-fiscal/winners_losers_2026_09_24/specs.cjs --case oct14`
- `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py --case oct14`
- `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/winners_losers_2026_09_24/test_winners_losers.py -q`

**Log (2026-10-14 JST, from `date`).**
- 19:31:51: first reproducibility pass, all three commands exit 0 and IDENTICAL 131/131; harness exits 3 because directory-level pytest does not name the changed test file to its coverage scanner. Repeating with the explicit test-file command above; `old_new.py` is excluded explicitly because its two historical propagation rounds are frozen and it writes outside this lane.
- 19:34: final reproducibility receipt read: **IDENTICAL 131/131, exit 0**, over the three live commands above and explicit `--allow-unrun old_new.py`. Python-measured elapsed 44.85s, child peak RSS 1,929,854,976 bytes. Old derived outputs unchanged; only `derived/oct14/` is new. No git writes.


## Round-2 Phase A on frozen v7 inputs, 2026-10-15

Phase A completed at 2026-10-14 16:49:45 UTC. These corrected scratch comparisons are beside the historical v7 tables above; oct15 production/readers await Phase B. Stationary financing remains the verdict, cohort frames beside. The frozen fiscal/social vintage is oct14; Phase B takes the live social producer vintage. All effects report the lineage's presence on other residents, negative for a cost. [CALCULATION: `/private/tmp/claude-501/-Users-alien-Projects-immigration-research/75b08f57-63cc-4e3d-96dc-60050327b5c1/scratchpad/prop8/winners/phase_a_validated/phase_a_fix_comparisons.csv`]

| frame | rule | ahead (%) | presence net ($bn) |
|---|---|---:|---:|
| stationary | a | 3.3392 | -483.071540 |
| cohort30 | a | 8.7499 | -452.035388 |
| cohort10 | a | 8.6929 | -452.659443 |
| stationary | b | 5.5002 | -483.071540 |
| cohort30 | b | 11.4392 | -452.035388 |
| cohort10 | b | 11.3728 | -452.659443 |
| stationary | c | 9.7212 | -483.071540 |
| cohort30 | c | 15.8972 | -452.035388 |
| cohort10 | c | 15.7826 | -452.659443 |

Fix 1 alone changes the mixed boundary from the one-way arm to -51.557272bn: forward member support 100.039383bn minus reverse non-member support 151.596655bn. Before pools all co-residents' own levels; after pools remaining residents' levels minus signed presence effects, on an equal per-person scale. This arm counts a non-member's support of member children in the same unit as a cost of the members' presence, which is why it stays beside the central. Neither pooling rule models re-partnering. Removal-level changes are labelled diagnostics only in the run log. [ASSUMPTION; CALCULATION: `/private/tmp/claude-501/-Users-alien-Projects-immigration-research/75b08f57-63cc-4e3d-96dc-60050327b5c1/scratchpad/prop8/winners/phase_a_validated/phase_a_mixed_levels.csv`; test_p7_frames.py]

All twelve isolated fixes, low/central/high shares under a/b/c and stationary/cohort10/cohort30, and channel-level changes are reported in `/private/tmp/claude-501/-Users-alien-Projects-immigration-research/75b08f57-63cc-4e3d-96dc-60050327b5c1/scratchpad/prop8/winners/phase_a_validated/phase_a_report.md`, `phase_a_fix_comparisons.csv`, `phase_a_fix_channels.csv`; every arm/sharing/epsilon is retained in the full shares/channels/cuts CSVs. State and landlord results require explicit frame/arm/rule selections; neither a general state winner-share ranking nor an unconditional landlord-benefit claim is supported. [MODEL / FRAMING-SENSITIVE]

Checks: 341,371 retained gates; 108 frozen control rows; 64 tests; Python compile check. Profile elapsed 239.512s; lifetime physical footprint 2.201GB, under 2.5GB. Two failed profiles are preserved in the scratch log; the cache mutation review defect is repaired with an actual-evaluate order regression. [CALCULATION: `/private/tmp/claude-501/-Users-alien-Projects-immigration-research/75b08f57-63cc-4e3d-96dc-60050327b5c1/scratchpad/prop8/winners/phase_a_validated/phase_a_gates.json`, `phase_a_timing.json`; test_p8_incidence.py]

[DEGRADED] School correction geography uses the preferred administrative/district spatial proxy at both ends; exact end-specific school/education-mixture state components need a producer export. Net state financing takes responded spending geography; receipt geography remains unidentified. FARS fatalities proxy injuries, and finite epsilon holds the case's first-order descendant P/F increment fixed while recomputing its multipliers. Item11, coverage payer exclusion, oct15 compressed readers and IDENTICAL rerun remain Phase B. No historical derived outputs were regenerated.


## Phase A final programme-source refresh, 2026-10-15

At 2026-10-14 17:00:20 UTC, completed the available ASEC disability-source mapping in fix2: railroad retirement also uses DIS_SC=6; Black Lung uses DIS_SC=8; state temporary sickness uses DIS_SC=9 and excludes private/federal disability. This supersedes the immediately preceding interim Phase-A exact shares. Other isolated fixes reproduce unchanged. The pooling presence boundary remains −$51.557272bn; the household-support and re-partnering limits stated above remain. [SOURCE: ASEC ddl25.txt; CALCULATION: test_p8_incidence.py; `/private/tmp/claude-501/-Users-alien-Projects-immigration-research/75b08f57-63cc-4e3d-96dc-60050327b5c1/scratchpad/prop8/winners/phase_a_complete/phase_a_shares.csv`]

| rule | stationary pooled ahead (%) | presence net ($bn) |
|---|---:|---:|
| a | 3.3392 | -483.071540 |
| b | 5.5002 | -483.071540 |
| c | 9.7373 | -483.071540 |

All frames, levels, isolated changes, channels and remaining universal programme proxies: `/private/tmp/claude-501/-Users-alien-Projects-immigration-research/75b08f57-63cc-4e3d-96dc-60050327b5c1/scratchpad/prop8/winners/phase_a_complete/phase_a_report.md`, `phase_a_fix_comparisons.csv`, `phase_a_fix_channels.csv`, `phase_a_unmapped_programmes.csv`. Checks: 65 tests; 341,371 retained gates; 108 original frozen-control rows; exported-ledger closure 1.79e-12bn; Python compile check. Profile 234.956s, physical footprint 2.199GB. School correction geography remains [DEGRADED] as documented above. No Git writes or tracked oct14 derived changes. Phase B remains held.

## Phase B verification receipt — 2026-10-15 01:14:56 UTC

[rerun] IDENTICAL: 221/221 files unchanged (backup removed), exit 0; all 44,167 gates pass. Complete harness 121.278s; pricing 107.346s, physical footprint 1.954728GB. All new derived artifacts are below 10MB, and prior oct14 derived files are unchanged. [CALCULATION: _cache/oct15_rerun.log; _cache/oct15_timings.jsonl]

Original public channel ids/columns and fiscal specification columns/ids remain stable. Added channel ids: p7_social_pm25_government_side, p7_social_pm25_respending, p7_social_scale_net_earnings, unlocated_fiscal. [DATA: derived/oct15/channels.csv; fiscal_specs.csv]

## v8 case (oct15) — 2026-10-15 01:11:35 UTC



On corrected v8, stationary financing, the current paired social stack and household pooling, 2.6140% / 4.4926% / 8.0294% of other residents are ahead under rules a/b/c; their central annual net is $-514.541916bn. Cohort financing is beside. [MODEL / FRAMING-SENSITIVE; CALCULATION: derived/oct15/p7_net_shares.csv]



All effects are presence minus removal; a positive amount means ahead from the lineage's presence. The stationary frame is the verdict. Cohort30 and cohort10 are beside. The low/high net rows pair the fiscal ends with the producer-range ratios transported to the live social rows; the central uses the central social rows at the fiscal midpoint. The paired-source ledger separately holds social parameters central at each fiscal end. [ASSUMPTION; DATA: p7_net_shares.csv; p8_channel_ledger.csv]



All accepted Phase-A fixes remain active; fix 8 now uses raw surviving-person item-11 changes. [CALCULATION: p8_incidence.ALL_FIXES; retained phase-A definitions]



| fix | finding IDs | source files | premise gates |
|---|---|---|---|
| 1 | R2E04/05/21/37; W1 | p7_frames.py, p8_incidence.py | mixed_before/after_levels_conserved; mixed_bidirectional_boundary |
| 2 | R2E07/09/33; W2 | p7_inputs.cjs, p8_incidence.py | programme_authority/exclusion |
| 3 | R2E10/19/26 | p7_cohorts.py, p8_incidence.py | trust_accrual_covered_earnings_only; cohort projection tests |
| 4 | R2E13/35; M1 | p8_recipient_keys.py, p8_incidence.py | air_old_recipient_death_share; fatal-victim conservation |
| 5 | R2E16/17/24/34; M4 | p8_incidence.py, p8_phase_a.py | social_producer_range; complete producer declarations |
| 6 | R2E01 | p8_incidence.py | matched coverage comparator; frozen control |
| 7 | R2E20 | p8_recipient_keys.py | rental capitalization only landlords; state stock preservation |
| 8 | R2E27; M3 | p8_incidence.py | credits_v7_legacy_only; replacement guard tests |
| 9 | R2E28/36/39 | p7_nest.py, inputs/p8_epsilon_sources.json | above_hs_perfect_substitutes; descendant_parts_close |
| 10 | R2E29/40/48/49; M2 | p8_recipient_keys.py, p8_incidence.py, p7_inputs.cjs | state_local_geography; end_pairing; prison producer; landlord states |
| 11 | R2E03/32/42/43 | p8_phase_a_document.py; RESULT.md | explicit frame failure; tagged cut tables |
| 12 | R2E15/44–47; M6 | p7_frames.py, winners_losers.py, p8_phase_a.py | resource rate; pins; repeated gates; fallback regression |



### Shares ahead under each financing rule



| frame | level | financing | persons_m | total_bn | future_bn | winners_share |
|---|---|---|---|---|---|---|
| stationary | central | a | 292.274073 | -514.541916 | -0.000000 | 2.6140% |
| stationary | central | b | 292.274073 | -514.541916 | -0.000000 | 4.4926% |
| stationary | central | c | 292.274073 | -514.541916 | -0.000000 | 8.0294% |
| stationary | high | a | 292.274073 | -844.313155 | -0.000000 | 2.7980% |
| stationary | high | b | 292.274073 | -844.313155 | -0.000000 | 3.0309% |
| stationary | high | c | 292.274073 | -844.313155 | -0.000000 | 3.5593% |
| stationary | low | a | 292.274073 | -186.443126 | -0.000000 | 41.8631% |
| stationary | low | b | 292.274073 | -186.443126 | -0.000000 | 39.4044% |
| stationary | low | c | 292.274073 | -186.443126 | -0.000000 | 41.4392% |
| cohort30 | central | a | 292.274073 | -479.700248 | -34.841668 | 7.3989% |
| cohort30 | central | b | 292.274073 | -479.700248 | -34.841668 | 10.2894% |
| cohort30 | central | c | 292.274073 | -479.700248 | -34.841668 | 14.7177% |
| cohort30 | high | a | 292.274073 | -809.020437 | -35.292718 | 2.9927% |
| cohort30 | high | b | 292.274073 | -809.020437 | -35.292718 | 3.8448% |
| cohort30 | high | c | 292.274073 | -809.020437 | -35.292718 | 4.7692% |
| cohort30 | low | a | 292.274073 | -152.052508 | -34.390618 | 38.7429% |
| cohort30 | low | b | 292.274073 | -152.052508 | -34.390618 | 37.8530% |
| cohort30 | low | c | 292.274073 | -152.052508 | -34.390618 | 41.7275% |
| cohort10 | central | a | 292.274073 | -480.386769 | -34.155147 | 7.2975% |
| cohort10 | central | b | 292.274073 | -480.386769 | -34.155147 | 10.2282% |
| cohort10 | central | c | 292.274073 | -480.386769 | -34.155147 | 14.5937% |
| cohort10 | high | a | 292.274073 | -810.033406 | -34.279749 | 2.9912% |
| cohort10 | high | b | 292.274073 | -810.033406 | -34.279749 | 3.8082% |
| cohort10 | high | c | 292.274073 | -810.033406 | -34.279749 | 4.7394% |
| cohort10 | low | a | 292.274073 | -152.412580 | -34.030546 | 38.7179% |
| cohort10 | low | b | 292.274073 | -152.412580 | -34.030546 | 37.7444% |
| cohort10 | low | c | 292.274073 | -152.412580 | -34.030546 | 41.6993% |



Rules a/b/c use tax shares, per-person financing, and responding-programme receipt, respectively. Federal and state-local programme keys remain separate; the trust accrual uses covered earnings under stationary financing and future payroll payers, including future births, under cohort financing. The FY2024 borrowing share is the central financing assumption. Public-capital return is a resource cost, and the unlocated financing block is explicitly per head with zero borrowing. [FRAMING-SENSITIVE; CALCULATION: p8_incidence.py]



### Case and channel closure



The corrected case is $365.791930–455.981785bn set and $281.752564–371.942418bn cash, over 45230062.300759 members including coverage. The ledger signs below are from other residents' side. [DATA: p8_channel_ledger.csv; p7_inputs.json population]



| basis | end | total_bn |
|---|---|---|
| cash | high | -371.942418 |
| cash | low | -281.752564 |
| set | high | -455.981785 |
| set | low | -365.791930 |



The payer pool changes from 292791509.254477 to 292274073.497283 people, exactly removing the completion records' 517435.757193 weight (gap -0.000000060). Coverage contributes 0 payer people. Actual completion members join the group; survey-absent coverage people have no fabricated payer/household records. [CALCULATION: p7_inputs.json membership; p8_membership.py]



| frame | level | channel | total_bn |
|---|---|---|---|
| stationary | low | trust_accrual | -84.051580 |
| stationary | low | general_federal | -22.542075 |
| stationary | low | current_trust_cash | 0.000000 |
| stationary | low | state_local | -246.257179 |
| stationary | low | unlocated_fiscal | -2.939947 |
| stationary | low | wages_positive | 109.866071 |
| stationary | low | wages_negative | -110.603366 |
| stationary | low | displaced_beneficiaries | -9.263855 |
| stationary | low | fiscal_source_rounding | 0.000000 |
| stationary | low | victims | -18.573432 |
| stationary | low | property_crime | -1.326445 |
| stationary | low | unreimbursed_care | -2.550811 |
| stationary | low | congestion | -2.124060 |
| stationary | low | housing_gain | -0.412728 |
| stationary | low | fear_avoidance | -3.296335 |
| stationary | low | private_security | -2.235128 |
| stationary | low | school_disruption | 13.094526 |
| stationary | low | pm25_consumption | -36.772442 |
| stationary | low | road_crash_externality | 65.234700 |
| stationary | low | scale_net_earnings | 93.272345 |
| stationary | low | restaurant_variety_market_size | 18.986077 |
| stationary | low | formal_volunteering_outside_group | 5.150195 |
| stationary | low | total_consumer_scale | 12.744518 |
| stationary | low | total_trade_travel_fdi | 26.203227 |
| stationary | low | pm25_government_side | -9.503085 |
| stationary | low | pm25_respending | 12.363712 |
| stationary | low | source_rounding | 0.000000 |
| stationary | low | item11_stayers_ACA | -0.493828 |
| stationary | low | item11_stayers_M1_federal | 8.498956 |
| stationary | low | item11_stayers_M2_state | 0.850817 |
| stationary | low | item11_stayers_M3_refunds | 1.723087 |
| stationary | low | item11_stayers_M6_biological_children | 1.928522 |
| stationary | low | item11_stayers_Medicaid | -1.071476 |
| stationary | low | item11_stayers_SNAP | -2.342106 |
| stationary | low | mixed_boundary | -56.010303 |
| stationary | low | future_cohorts | -0.000000 |
| stationary | central | trust_accrual | -84.051580 |
| stationary | central | general_federal | -42.668324 |
| stationary | central | current_trust_cash | 0.000000 |
| stationary | central | state_local | -269.375103 |
| stationary | central | unlocated_fiscal | -4.916845 |
| stationary | central | wages_positive | 91.068996 |
| stationary | central | wages_negative | -91.680146 |
| stationary | central | displaced_beneficiaries | -9.263855 |
| stationary | central | fiscal_source_rounding | -0.000000 |
| stationary | central | victims | -39.394626 |
| stationary | central | property_crime | -1.377571 |
| stationary | central | unreimbursed_care | -4.693120 |
| stationary | central | congestion | -12.266357 |
| stationary | central | housing_gain | 2.295526 |
| stationary | central | fear_avoidance | -7.088766 |
| stationary | central | private_security | -0.512160 |
| stationary | central | school_disruption | 2.180557 |
| stationary | central | pm25_consumption | -81.349333 |
| stationary | central | road_crash_externality | -12.615029 |
| stationary | central | scale_net_earnings | 15.387253 |
| stationary | central | restaurant_variety_market_size | 6.711441 |
| stationary | central | formal_volunteering_outside_group | 4.046568 |
| stationary | central | total_consumer_scale | 2.344365 |
| stationary | central | total_trade_travel_fdi | 7.468226 |
| stationary | central | pm25_government_side | -9.811274 |
| stationary | central | pm25_respending | 14.029432 |
| stationary | central | source_rounding | 0.000000 |
| stationary | central | item11_stayers_ACA | -0.022578 |
| stationary | central | item11_stayers_M1_federal | 8.498956 |
| stationary | central | item11_stayers_M2_state | 0.850817 |
| stationary | central | item11_stayers_M3_refunds | 1.723087 |
| stationary | central | item11_stayers_M6_biological_children | 1.928522 |
| stationary | central | item11_stayers_Medicaid | -0.579262 |
| stationary | central | item11_stayers_SNAP | -1.409733 |
| stationary | central | mixed_boundary | -56.010303 |
| stationary | central | future_cohorts | -0.000000 |
| stationary | high | trust_accrual | -84.051580 |
| stationary | high | general_federal | -62.794573 |
| stationary | high | current_trust_cash | 0.000000 |
| stationary | high | state_local | -292.493027 |
| stationary | high | unlocated_fiscal | -6.893744 |
| stationary | high | wages_positive | 72.271920 |
| stationary | high | wages_negative | -72.756927 |
| stationary | high | displaced_beneficiaries | -9.263855 |
| stationary | high | fiscal_source_rounding | 0.000000 |
| stationary | high | victims | -60.861461 |
| stationary | high | property_crime | -1.544966 |
| stationary | high | unreimbursed_care | -7.483487 |
| stationary | high | congestion | -25.654223 |
| stationary | high | housing_gain | 2.074555 |
| stationary | high | fear_avoidance | -21.897662 |
| stationary | high | private_security | 0.368300 |
| stationary | high | school_disruption | 0.603847 |
| stationary | high | pm25_consumption | -142.994795 |
| stationary | high | road_crash_externality | -85.661023 |
| stationary | high | scale_net_earnings | -62.497839 |
| stationary | high | restaurant_variety_market_size | 1.061006 |
| stationary | high | formal_volunteering_outside_group | 2.942941 |
| stationary | high | total_consumer_scale | -6.501060 |
| stationary | high | total_trade_travel_fdi | 1.253163 |
| stationary | high | pm25_government_side | -10.119462 |
| stationary | high | pm25_respending | 15.695152 |
| stationary | high | source_rounding | 0.000000 |
| stationary | high | item11_stayers_ACA | 0.448672 |
| stationary | high | item11_stayers_M1_federal | 8.498956 |
| stationary | high | item11_stayers_M2_state | 0.850817 |
| stationary | high | item11_stayers_M3_refunds | 1.723087 |
| stationary | high | item11_stayers_M6_biological_children | 1.928522 |
| stationary | high | item11_stayers_Medicaid | -0.087048 |
| stationary | high | item11_stayers_SNAP | -0.477360 |
| stationary | high | mixed_boundary | -56.010303 |
| stationary | high | future_cohorts | -0.000000 |
| cohort30 | low | general_federal | -16.716564 |
| cohort30 | low | current_trust_cash | 0.000000 |
| cohort30 | low | trust_accrual | -50.158470 |
| cohort30 | low | borrowing_service | -5.328003 |
| cohort30 | low | state_local | -246.257179 |
| cohort30 | low | unlocated_fiscal | -2.939947 |
| cohort30 | low | wages_positive | 109.866071 |
| cohort30 | low | wages_negative | -110.603366 |
| cohort30 | low | displaced_beneficiaries | -9.263855 |
| cohort30 | low | fiscal_source_rounding | 0.000000 |
| cohort30 | low | victims | -18.573432 |
| cohort30 | low | property_crime | -1.326445 |
| cohort30 | low | unreimbursed_care | -2.550811 |
| cohort30 | low | congestion | -2.124060 |
| cohort30 | low | housing_gain | -0.412728 |
| cohort30 | low | fear_avoidance | -3.296335 |
| cohort30 | low | private_security | -2.235128 |
| cohort30 | low | school_disruption | 13.094526 |
| cohort30 | low | pm25_consumption | -36.772442 |
| cohort30 | low | road_crash_externality | 65.234700 |
| cohort30 | low | scale_net_earnings | 93.272345 |
| cohort30 | low | restaurant_variety_market_size | 18.986077 |
| cohort30 | low | formal_volunteering_outside_group | 5.150195 |
| cohort30 | low | total_consumer_scale | 12.744518 |
| cohort30 | low | total_trade_travel_fdi | 26.203227 |
| cohort30 | low | pm25_government_side | -9.503085 |
| cohort30 | low | pm25_respending | 12.363712 |
| cohort30 | low | source_rounding | 0.000000 |
| cohort30 | low | item11_stayers_ACA | -0.493828 |
| cohort30 | low | item11_stayers_M1_federal | 8.498956 |
| cohort30 | low | item11_stayers_M2_state | 0.850817 |
| cohort30 | low | item11_stayers_M3_refunds | 1.723087 |
| cohort30 | low | item11_stayers_M6_biological_children | 1.928522 |
| cohort30 | low | item11_stayers_Medicaid | -1.071476 |
| cohort30 | low | item11_stayers_SNAP | -2.342106 |
| cohort30 | low | mixed_boundary | -56.010303 |
| cohort30 | low | future_cohorts | -34.390618 |
| cohort30 | central | general_federal | -31.561292 |
| cohort30 | central | current_trust_cash | 0.000000 |
| cohort30 | central | trust_accrual | -50.158470 |
| cohort30 | central | borrowing_service | -10.158474 |
| cohort30 | central | state_local | -269.375103 |
| cohort30 | central | unlocated_fiscal | -4.916845 |
| cohort30 | central | wages_positive | 91.068996 |
| cohort30 | central | wages_negative | -91.680146 |
| cohort30 | central | displaced_beneficiaries | -9.263855 |
| cohort30 | central | fiscal_source_rounding | 0.000000 |
| cohort30 | central | victims | -39.394626 |
| cohort30 | central | property_crime | -1.377571 |
| cohort30 | central | unreimbursed_care | -4.693120 |
| cohort30 | central | congestion | -12.266357 |
| cohort30 | central | housing_gain | 2.295526 |
| cohort30 | central | fear_avoidance | -7.088766 |
| cohort30 | central | private_security | -0.512160 |
| cohort30 | central | school_disruption | 2.180557 |
| cohort30 | central | pm25_consumption | -81.349333 |
| cohort30 | central | road_crash_externality | -12.615029 |
| cohort30 | central | scale_net_earnings | 15.387253 |
| cohort30 | central | restaurant_variety_market_size | 6.711441 |
| cohort30 | central | formal_volunteering_outside_group | 4.046568 |
| cohort30 | central | total_consumer_scale | 2.344365 |
| cohort30 | central | total_trade_travel_fdi | 7.468226 |
| cohort30 | central | pm25_government_side | -9.811274 |
| cohort30 | central | pm25_respending | 14.029432 |
| cohort30 | central | source_rounding | 0.000000 |
| cohort30 | central | item11_stayers_ACA | -0.022578 |
| cohort30 | central | item11_stayers_M1_federal | 8.498956 |
| cohort30 | central | item11_stayers_M2_state | 0.850817 |
| cohort30 | central | item11_stayers_M3_refunds | 1.723087 |
| cohort30 | central | item11_stayers_M6_biological_children | 1.928522 |
| cohort30 | central | item11_stayers_Medicaid | -0.579262 |
| cohort30 | central | item11_stayers_SNAP | -1.409733 |
| cohort30 | central | mixed_boundary | -56.010303 |
| cohort30 | central | future_cohorts | -34.841668 |
| cohort30 | high | general_federal | -46.406021 |
| cohort30 | high | current_trust_cash | 0.000000 |
| cohort30 | high | trust_accrual | -50.158470 |
| cohort30 | high | borrowing_service | -14.988945 |
| cohort30 | high | state_local | -292.493027 |
| cohort30 | high | unlocated_fiscal | -6.893744 |
| cohort30 | high | wages_positive | 72.271920 |
| cohort30 | high | wages_negative | -72.756927 |
| cohort30 | high | displaced_beneficiaries | -9.263855 |
| cohort30 | high | fiscal_source_rounding | -0.000000 |
| cohort30 | high | victims | -60.861461 |
| cohort30 | high | property_crime | -1.544966 |
| cohort30 | high | unreimbursed_care | -7.483487 |
| cohort30 | high | congestion | -25.654223 |
| cohort30 | high | housing_gain | 2.074555 |
| cohort30 | high | fear_avoidance | -21.897662 |
| cohort30 | high | private_security | 0.368300 |
| cohort30 | high | school_disruption | 0.603847 |
| cohort30 | high | pm25_consumption | -142.994795 |
| cohort30 | high | road_crash_externality | -85.661023 |
| cohort30 | high | scale_net_earnings | -62.497839 |
| cohort30 | high | restaurant_variety_market_size | 1.061006 |
| cohort30 | high | formal_volunteering_outside_group | 2.942941 |
| cohort30 | high | total_consumer_scale | -6.501060 |
| cohort30 | high | total_trade_travel_fdi | 1.253163 |
| cohort30 | high | pm25_government_side | -10.119462 |
| cohort30 | high | pm25_respending | 15.695152 |
| cohort30 | high | source_rounding | 0.000000 |
| cohort30 | high | item11_stayers_ACA | 0.448672 |
| cohort30 | high | item11_stayers_M1_federal | 8.498956 |
| cohort30 | high | item11_stayers_M2_state | 0.850817 |
| cohort30 | high | item11_stayers_M3_refunds | 1.723087 |
| cohort30 | high | item11_stayers_M6_biological_children | 1.928522 |
| cohort30 | high | item11_stayers_Medicaid | -0.087048 |
| cohort30 | high | item11_stayers_SNAP | -0.477360 |
| cohort30 | high | mixed_boundary | -56.010303 |
| cohort30 | high | future_cohorts | -35.292718 |
| cohort10 | low | general_federal | -16.716564 |
| cohort10 | low | current_trust_cash | 0.000000 |
| cohort10 | low | trust_accrual | -50.158470 |
| cohort10 | low | borrowing_service | -5.688075 |
| cohort10 | low | state_local | -246.257179 |
| cohort10 | low | unlocated_fiscal | -2.939947 |
| cohort10 | low | wages_positive | 109.866071 |
| cohort10 | low | wages_negative | -110.603366 |
| cohort10 | low | displaced_beneficiaries | -9.263855 |
| cohort10 | low | fiscal_source_rounding | 0.000000 |
| cohort10 | low | victims | -18.573432 |
| cohort10 | low | property_crime | -1.326445 |
| cohort10 | low | unreimbursed_care | -2.550811 |
| cohort10 | low | congestion | -2.124060 |
| cohort10 | low | housing_gain | -0.412728 |
| cohort10 | low | fear_avoidance | -3.296335 |
| cohort10 | low | private_security | -2.235128 |
| cohort10 | low | school_disruption | 13.094526 |
| cohort10 | low | pm25_consumption | -36.772442 |
| cohort10 | low | road_crash_externality | 65.234700 |
| cohort10 | low | scale_net_earnings | 93.272345 |
| cohort10 | low | restaurant_variety_market_size | 18.986077 |
| cohort10 | low | formal_volunteering_outside_group | 5.150195 |
| cohort10 | low | total_consumer_scale | 12.744518 |
| cohort10 | low | total_trade_travel_fdi | 26.203227 |
| cohort10 | low | pm25_government_side | -9.503085 |
| cohort10 | low | pm25_respending | 12.363712 |
| cohort10 | low | source_rounding | 0.000000 |
| cohort10 | low | item11_stayers_ACA | -0.493828 |
| cohort10 | low | item11_stayers_M1_federal | 8.498956 |
| cohort10 | low | item11_stayers_M2_state | 0.850817 |
| cohort10 | low | item11_stayers_M3_refunds | 1.723087 |
| cohort10 | low | item11_stayers_M6_biological_children | 1.928522 |
| cohort10 | low | item11_stayers_Medicaid | -1.071476 |
| cohort10 | low | item11_stayers_SNAP | -2.342106 |
| cohort10 | low | mixed_boundary | -56.010303 |
| cohort10 | low | future_cohorts | -34.030546 |
| cohort10 | central | general_federal | -31.561292 |
| cohort10 | central | current_trust_cash | 0.000000 |
| cohort10 | central | trust_accrual | -50.158470 |
| cohort10 | central | borrowing_service | -10.844994 |
| cohort10 | central | state_local | -269.375103 |
| cohort10 | central | unlocated_fiscal | -4.916845 |
| cohort10 | central | wages_positive | 91.068996 |
| cohort10 | central | wages_negative | -91.680146 |
| cohort10 | central | displaced_beneficiaries | -9.263855 |
| cohort10 | central | fiscal_source_rounding | -0.000000 |
| cohort10 | central | victims | -39.394626 |
| cohort10 | central | property_crime | -1.377571 |
| cohort10 | central | unreimbursed_care | -4.693120 |
| cohort10 | central | congestion | -12.266357 |
| cohort10 | central | housing_gain | 2.295526 |
| cohort10 | central | fear_avoidance | -7.088766 |
| cohort10 | central | private_security | -0.512160 |
| cohort10 | central | school_disruption | 2.180557 |
| cohort10 | central | pm25_consumption | -81.349333 |
| cohort10 | central | road_crash_externality | -12.615029 |
| cohort10 | central | scale_net_earnings | 15.387253 |
| cohort10 | central | restaurant_variety_market_size | 6.711441 |
| cohort10 | central | formal_volunteering_outside_group | 4.046568 |
| cohort10 | central | total_consumer_scale | 2.344365 |
| cohort10 | central | total_trade_travel_fdi | 7.468226 |
| cohort10 | central | pm25_government_side | -9.811274 |
| cohort10 | central | pm25_respending | 14.029432 |
| cohort10 | central | source_rounding | 0.000000 |
| cohort10 | central | item11_stayers_ACA | -0.022578 |
| cohort10 | central | item11_stayers_M1_federal | 8.498956 |
| cohort10 | central | item11_stayers_M2_state | 0.850817 |
| cohort10 | central | item11_stayers_M3_refunds | 1.723087 |
| cohort10 | central | item11_stayers_M6_biological_children | 1.928522 |
| cohort10 | central | item11_stayers_Medicaid | -0.579262 |
| cohort10 | central | item11_stayers_SNAP | -1.409733 |
| cohort10 | central | mixed_boundary | -56.010303 |
| cohort10 | central | future_cohorts | -34.155147 |
| cohort10 | high | general_federal | -46.406021 |
| cohort10 | high | current_trust_cash | 0.000000 |
| cohort10 | high | trust_accrual | -50.158470 |
| cohort10 | high | borrowing_service | -16.001913 |
| cohort10 | high | state_local | -292.493027 |
| cohort10 | high | unlocated_fiscal | -6.893744 |
| cohort10 | high | wages_positive | 72.271920 |
| cohort10 | high | wages_negative | -72.756927 |
| cohort10 | high | displaced_beneficiaries | -9.263855 |
| cohort10 | high | fiscal_source_rounding | -0.000000 |
| cohort10 | high | victims | -60.861461 |
| cohort10 | high | property_crime | -1.544966 |
| cohort10 | high | unreimbursed_care | -7.483487 |
| cohort10 | high | congestion | -25.654223 |
| cohort10 | high | housing_gain | 2.074555 |
| cohort10 | high | fear_avoidance | -21.897662 |
| cohort10 | high | private_security | 0.368300 |
| cohort10 | high | school_disruption | 0.603847 |
| cohort10 | high | pm25_consumption | -142.994795 |
| cohort10 | high | road_crash_externality | -85.661023 |
| cohort10 | high | scale_net_earnings | -62.497839 |
| cohort10 | high | restaurant_variety_market_size | 1.061006 |
| cohort10 | high | formal_volunteering_outside_group | 2.942941 |
| cohort10 | high | total_consumer_scale | -6.501060 |
| cohort10 | high | total_trade_travel_fdi | 1.253163 |
| cohort10 | high | pm25_government_side | -10.119462 |
| cohort10 | high | pm25_respending | 15.695152 |
| cohort10 | high | source_rounding | 0.000000 |
| cohort10 | high | item11_stayers_ACA | 0.448672 |
| cohort10 | high | item11_stayers_M1_federal | 8.498956 |
| cohort10 | high | item11_stayers_M2_state | 0.850817 |
| cohort10 | high | item11_stayers_M3_refunds | 1.723087 |
| cohort10 | high | item11_stayers_M6_biological_children | 1.928522 |
| cohort10 | high | item11_stayers_Medicaid | -0.087048 |
| cohort10 | high | item11_stayers_SNAP | -0.477360 |
| cohort10 | high | mixed_boundary | -56.010303 |
| cohort10 | high | future_cohorts | -34.279749 |



The mixed_boundary row is added only for the mixed_unit sharing arm. It is excluded from the ordinary pooled/person channel sum. Item 11 is the budget's recomputation and the stayers' direct resource changes; the pooling arm compares the household's before/after sharing of resources. Actual surviving-person tax and benefit flows enter that arm once; its separate pooling residual is the member/non-member resource boundary. The budget retains every item-11 part. Fixed-pool attribution movements and unlocated credit extrapolation do not by themselves create disposable resources; the complete attribution reading is the explicit item11_attribution beside arm. Raw surviving-person flows are measured before subtracting either direction of the old-credit convention, so a second crossing-credit gain is forbidden. Neither pooling rule models re-partnering. [CALCULATION: p8_stayers.py; p8_membership.replacement_credit; p7_mixed_reconciliation.csv]



### Isolated v8 source items and round-3 social changes



| item | basis | end | cost_bn | A_bn | P_bn | F_bn | capital_bn |
|---|---|---|---|---|---|---|---|
| foreign_source_tax | set | low | 3.774626 | -3.774626 | 0.000000 | 0.000000 | 0.000000 |
| foreign_source_tax | set | high | 1.396612 | -1.396612 | 0.000000 | 0.000000 | 0.000000 |
| foreign_source_tax | cash | low | 3.774626 | -3.774626 | 0.000000 | 0.000000 | 0.000000 |
| foreign_source_tax | cash | high | 1.396612 | -1.396612 | 0.000000 | 0.000000 | 0.000000 |
| union_completion | set | low | 2.893211 | -2.893395 | -0.000007 | 0.000191 | 0.069799 |
| union_completion | set | high | 3.754616 | -3.754737 | -0.000005 | 0.000126 | 0.110318 |
| union_completion | cash | low | 2.031263 | -2.031446 | -0.000007 | 0.000191 | 0.069799 |
| union_completion | cash | high | 2.892668 | -2.892789 | -0.000005 | 0.000126 | 0.110318 |
| mixed_unit_removal | set | low | 10.740016 | -10.740016 | 0.000000 | 0.000000 | 0.000000 |
| mixed_unit_removal | set | high | 14.531690 | -14.531690 | 0.000000 | 0.000000 | 0.000000 |
| mixed_unit_removal | cash | low | 10.740016 | -10.740016 | 0.000000 | 0.000000 | 0.000000 |
| mixed_unit_removal | cash | high | 14.531690 | -14.531690 | 0.000000 | 0.000000 | 0.000000 |
| coverage | set | low | 8.802814 | -9.393324 | -0.032830 | 0.623340 | 0.000000 |
| coverage | set | high | 12.638785 | -13.027233 | -0.021596 | 0.410044 | 0.000000 |
| coverage | cash | low | 0.751840 | -1.342350 | -0.032830 | 0.623340 | 0.000000 |
| coverage | cash | high | 4.587811 | -4.976259 | -0.021596 | 0.410044 | 0.000000 |



The isolated dollar increments above execute each source item alone on v7's actual endpoint specifications. The isolated share changes below add each source item to the all-off fiscal base with current incidence keys, payer frame and paired budget counterflows held fixed. Its exported social-key contributions follow completion/coverage counts in each scope and consumption receipts; item 11 replaces the old direct-credit vector with raw survivor flows. The leave-one-out rows provide a second controlled decomposition. These do not claim a separately solved one-item population equilibrium. The item-interaction financing parts remain explicit in p8_item_effects.json. [ASSUMPTION; CALCULATION: specs.cjs; p8_ablations.py]



| scenario | frame | level | financing | total_bn | winners_share | delta_total_bn | delta_ahead_pp |
|---|---|---|---|---|---|---|---|
| v8_all_off_fixed_keys | stationary | low | a | -444.433219 | 7.2639% | 24.125828 | 1.288263 |
| isolated_foreign_source_tax | stationary | low | a | -448.207845 | 6.8305% | -3.774626 | -0.433411 |
| without_foreign_source_tax | stationary | low | a | -464.784422 | 6.2923% | 3.774626 | 0.316698 |
| isolated_union_completion | stationary | low | a | -448.052548 | 7.1176% | -3.619329 | -0.146258 |
| without_union_completion | stationary | low | a | -464.939718 | 6.0717% | 3.619329 | 0.096100 |
| isolated_mixed_unit_removal | stationary | low | a | -448.859492 | 6.4129% | -4.426273 | -0.850938 |
| without_mixed_unit_removal | stationary | low | a | -464.132774 | 6.6627% | 4.426273 | 0.687106 |
| isolated_coverage | stationary | low | a | -456.709574 | 7.2078% | -12.276355 | -0.056058 |
| without_coverage | stationary | low | a | -456.282692 | 5.9667% | 12.276355 | -0.008856 |
| without_round3_government_side | stationary | low | a | -459.055962 | 6.1662% | 9.503085 | 0.190602 |
| without_round3_added_people | stationary | low | a | -464.163269 | 5.8941% | 4.395778 | -0.081451 |
| without_round3_item11_consumption | stationary | low | a | -471.234851 | 5.9709% | -2.675804 | -0.004659 |
| without_round3_completion_receivers | stationary | low | a | -468.755167 | 5.9787% | -0.196119 | 0.003057 |
| government_legacy_response | stationary | low | a | -466.085048 | 6.0369% | 2.473999 | 0.061337 |
| respending_without_government_side | stationary | low | a | -459.055962 | 6.1662% | 9.503085 | 0.190602 |
| neither_budget_side | stationary | low | a | -471.419674 | 5.9216% | -2.860627 | -0.053960 |
| matched_justice_footing | stationary | low | a | -463.990944 | 6.0747% | 4.568103 | 0.099125 |
| borrowing_0 | stationary | low | a | -468.559047 | 5.9756% | 0.000000 | 0.000000 |
| borrowing_1 | stationary | low | a | -468.559047 | 5.9756% | 0.000000 | 0.000000 |
| v8_all_off_fixed_keys | stationary | high | a | -533.961730 | 2.0073% | 26.563055 | -0.327610 |
| isolated_foreign_source_tax | stationary | high | a | -535.358341 | 2.0010% | -1.396612 | -0.006300 |
| without_foreign_source_tax | stationary | high | a | -559.128173 | 2.3384% | 1.396612 | 0.003537 |
| isolated_union_completion | stationary | high | a | -538.463768 | 2.0064% | -4.502038 | -0.000833 |
| without_union_completion | stationary | high | a | -556.022747 | 2.3296% | 4.502038 | -0.005225 |
| isolated_mixed_unit_removal | stationary | high | a | -538.388003 | 2.3343% | -4.426273 | 0.327031 |
| without_mixed_unit_removal | stationary | high | a | -556.098512 | 2.0009% | 4.426273 | -0.334003 |
| isolated_coverage | stationary | high | a | -550.189042 | 2.0055% | -16.227312 | -0.001808 |
| without_coverage | stationary | high | a | -544.297473 | 2.3201% | 16.227312 | -0.014725 |
| without_round3_government_side | stationary | high | a | -550.405322 | 2.3653% | 10.119462 | 0.030443 |
| without_round3_added_people | stationary | high | a | -555.978205 | 2.2849% | 4.546580 | -0.049999 |
| without_round3_item11_consumption | stationary | high | a | -563.200589 | 2.3206% | -2.675804 | -0.014269 |
| without_round3_completion_receivers | stationary | high | a | -560.735417 | 2.3349% | -0.210632 | 0.000000 |
| government_legacy_response | stationary | high | a | -557.434408 | 2.3389% | 3.090376 | 0.004066 |
| respending_without_government_side | stationary | high | a | -550.405322 | 2.3653% | 10.119462 | 0.030443 |
| neither_budget_side | stationary | high | a | -566.100474 | 2.3134% | -5.575689 | -0.021514 |
| matched_justice_footing | stationary | high | a | -560.524785 | 2.3349% | 0.000000 | 0.000000 |
| borrowing_0 | stationary | high | a | -560.524785 | 2.3349% | 0.000000 | 0.000000 |
| borrowing_1 | stationary | high | a | -560.524785 | 2.3349% | -0.000000 | 0.000000 |
| v8_all_off_fixed_keys | cohort30 | low | a | -413.717258 | 13.8428% | 20.451171 | 0.559477 |
| isolated_foreign_source_tax | cohort30 | low | a | -417.427518 | 13.5776% | -3.710260 | -0.265244 |
| without_foreign_source_tax | cohort30 | low | a | -430.458170 | 13.5770% | 3.710260 | 0.293664 |
| isolated_union_completion | cohort30 | low | a | -417.012947 | 13.7656% | -3.295688 | -0.077169 |
| without_union_completion | cohort30 | low | a | -430.872741 | 13.3775% | 3.295688 | 0.094193 |
| isolated_mixed_unit_removal | cohort30 | low | a | -417.994627 | 13.2343% | -4.277368 | -0.608467 |
| without_mixed_unit_removal | cohort30 | low | a | -429.891062 | 13.8266% | 4.277368 | 0.543277 |
| isolated_coverage | cohort30 | low | a | -422.856367 | 14.2121% | -9.139108 | 0.369281 |
| without_coverage | cohort30 | low | a | -425.029321 | 12.7763% | 9.139108 | -0.507044 |
| without_round3_government_side | cohort30 | low | a | -424.665345 | 13.5725% | 9.503085 | 0.289177 |
| without_round3_added_people | cohort30 | low | a | -429.772651 | 13.3020% | 4.395778 | 0.018714 |
| without_round3_item11_consumption | cohort30 | low | a | -436.844233 | 13.2111% | -2.675804 | -0.072267 |
| without_round3_completion_receivers | cohort30 | low | a | -434.364549 | 13.2823% | -0.196119 | -0.000988 |
| government_legacy_response | cohort30 | low | a | -431.694431 | 13.3709% | 2.473999 | 0.087585 |
| respending_without_government_side | cohort30 | low | a | -424.665345 | 13.5725% | 9.503085 | 0.289177 |
| neither_budget_side | cohort30 | low | a | -437.029057 | 13.1755% | -2.860627 | -0.107869 |
| matched_justice_footing | cohort30 | low | a | -429.600327 | 13.4306% | 4.568103 | 0.147320 |
| borrowing_0 | cohort30 | low | a | -434.665937 | 13.3453% | -0.497508 | 0.061939 |
| borrowing_1 | cohort30 | low | a | -432.820126 | 13.1368% | 1.348304 | -0.146555 |
| v8_all_off_fixed_keys | cohort30 | high | a | -502.350263 | 3.6661% | 22.881804 | -0.134577 |
| isolated_foreign_source_tax | cohort30 | high | a | -503.723059 | 3.6148% | -1.372796 | -0.051277 |
| without_foreign_source_tax | cohort30 | high | a | -523.859271 | 3.8482% | 1.372796 | 0.047464 |
| isolated_union_completion | cohort30 | high | a | -506.521043 | 3.6551% | -4.170779 | -0.010975 |
| without_union_completion | cohort30 | high | a | -521.061288 | 3.8019% | 4.170779 | 0.001176 |
| isolated_mixed_unit_removal | cohort30 | high | a | -506.627631 | 3.6778% | -4.277368 | 0.011734 |
| without_mixed_unit_removal | cohort30 | high | a | -520.954699 | 3.8550% | 4.277368 | 0.054357 |
| isolated_coverage | cohort30 | high | a | -515.400487 | 3.9122% | -13.050224 | 0.246132 |
| without_coverage | cohort30 | high | a | -512.181843 | 3.6404% | 13.050224 | -0.160337 |
| without_round3_government_side | cohort30 | high | a | -515.112605 | 3.9324% | 10.119462 | 0.131742 |
| without_round3_added_people | cohort30 | high | a | -520.685487 | 3.7519% | 4.546580 | -0.048831 |
| without_round3_item11_consumption | cohort30 | high | a | -527.907871 | 3.7977% | -2.675804 | -0.003036 |
| without_round3_completion_receivers | cohort30 | high | a | -525.442699 | 3.8062% | -0.210632 | 0.005480 |
| government_legacy_response | cohort30 | high | a | -522.141691 | 3.8497% | 3.090376 | 0.049053 |
| respending_without_government_side | cohort30 | high | a | -515.112605 | 3.9324% | 10.119462 | 0.131742 |
| neither_budget_side | cohort30 | high | a | -530.807756 | 3.7630% | -5.575689 | -0.037674 |
| matched_justice_footing | cohort30 | high | a | -525.232067 | 3.8007% | 0.000000 | 0.000000 |
| borrowing_0 | cohort30 | high | a | -526.631675 | 3.5601% | -1.399608 | -0.240563 |
| borrowing_1 | cohort30 | high | a | -521.438966 | 4.8003% | 3.793101 | 0.999659 |
| v8_all_off_fixed_keys | cohort10 | low | a | -414.022703 | 13.8312% | 20.505799 | 0.598210 |
| isolated_foreign_source_tax | cohort10 | low | a | -417.779548 | 13.5395% | -3.756845 | -0.291642 |
| without_foreign_source_tax | cohort10 | low | a | -430.771657 | 13.5560% | 3.756845 | 0.323060 |
| isolated_union_completion | cohort10 | low | a | -417.300932 | 13.7504% | -3.278229 | -0.080815 |
| without_union_completion | cohort10 | low | a | -431.250273 | 13.3268% | 3.278229 | 0.093845 |
| isolated_mixed_unit_removal | cohort10 | low | a | -418.407842 | 13.1594% | -4.385138 | -0.671775 |
| without_mixed_unit_removal | cohort10 | low | a | -430.143363 | 13.8040% | 4.385138 | 0.571049 |
| isolated_coverage | cohort10 | low | a | -423.079183 | 14.1800% | -9.056479 | 0.348808 |
| without_coverage | cohort10 | low | a | -425.472022 | 12.7341% | 9.056479 | -0.498911 |
| without_round3_government_side | cohort10 | low | a | -425.025417 | 13.5560% | 9.503085 | 0.323058 |
| without_round3_added_people | cohort10 | low | a | -430.132724 | 13.2724% | 4.395778 | 0.039394 |
| without_round3_item11_consumption | cohort10 | low | a | -437.204306 | 13.1885% | -2.675804 | -0.044458 |
| without_round3_completion_receivers | cohort10 | low | a | -434.724621 | 13.2298% | -0.196119 | -0.003216 |
| government_legacy_response | cohort10 | low | a | -432.054503 | 13.3188% | 2.473999 | 0.085842 |
| respending_without_government_side | cohort10 | low | a | -425.025417 | 13.5560% | 9.503085 | 0.323058 |
| neither_budget_side | cohort10 | low | a | -437.389129 | 13.1421% | -2.860627 | -0.090870 |
| matched_justice_footing | cohort10 | low | a | -429.960399 | 13.3886% | 4.568103 | 0.155594 |
| borrowing_0 | cohort10 | low | a | -434.665937 | 13.3453% | -0.137435 | 0.112287 |
| borrowing_1 | cohort10 | low | a | -434.156036 | 12.9408% | 0.372466 | -0.292160 |
| v8_all_off_fixed_keys | cohort10 | high | a | -503.303832 | 3.5803% | 22.941204 | -0.155279 |
| isolated_foreign_source_tax | cohort10 | high | a | -504.693865 | 3.5333% | -1.390033 | -0.046988 |
| without_foreign_source_tax | cohort10 | high | a | -524.855003 | 3.7672% | 1.390033 | 0.031624 |
| isolated_union_completion | cohort10 | high | a | -507.462665 | 3.5746% | -4.158833 | -0.005708 |
| without_union_completion | cohort10 | high | a | -522.086203 | 3.7365% | 4.158833 | 0.000864 |
| isolated_mixed_unit_removal | cohort10 | high | a | -507.688970 | 3.5711% | -4.385138 | -0.009215 |
| without_mixed_unit_removal | cohort10 | high | a | -521.859897 | 3.7568% | 4.385138 | 0.021178 |
| isolated_coverage | cohort10 | high | a | -516.300262 | 3.8032% | -12.996430 | 0.222864 |
| without_coverage | cohort10 | high | a | -513.248606 | 3.5295% | 12.996430 | -0.206092 |
| without_round3_government_side | cohort10 | high | a | -516.125574 | 3.8355% | 10.119462 | 0.099894 |
| without_round3_added_people | cohort10 | high | a | -521.698456 | 3.6684% | 4.546580 | -0.067209 |
| without_round3_item11_consumption | cohort10 | high | a | -528.920840 | 3.7132% | -2.675804 | -0.022404 |
| without_round3_completion_receivers | cohort10 | high | a | -526.455668 | 3.7434% | -0.210632 | 0.007798 |
| government_legacy_response | cohort10 | high | a | -523.154659 | 3.7585% | 3.090376 | 0.022892 |
| respending_without_government_side | cohort10 | high | a | -516.125574 | 3.8355% | 10.119462 | 0.099894 |
| neither_budget_side | cohort10 | high | a | -531.820725 | 3.6558% | -5.575689 | -0.079811 |
| matched_justice_footing | cohort10 | high | a | -526.245036 | 3.7356% | 0.000000 | 0.000000 |
| borrowing_0 | cohort10 | high | a | -526.631675 | 3.5601% | -0.386639 | -0.175482 |
| borrowing_1 | cohort10 | high | a | -525.197199 | 4.5056% | 1.047837 | 0.770022 |
| v8_all_off_fixed_keys | stationary | low | b | -444.433219 | 9.4969% | 24.125828 | 1.185081 |
| isolated_foreign_source_tax | stationary | low | b | -448.207845 | 9.1763% | -3.774626 | -0.320626 |
| without_foreign_source_tax | stationary | low | b | -464.784422 | 8.6018% | 3.774626 | 0.289986 |
| isolated_union_completion | stationary | low | b | -448.052548 | 9.3576% | -3.619329 | -0.139312 |
| without_union_completion | stationary | low | b | -464.939718 | 8.4215% | 3.619329 | 0.109681 |
| isolated_mixed_unit_removal | stationary | low | b | -448.859492 | 8.8185% | -4.426273 | -0.678439 |
| without_mixed_unit_removal | stationary | low | b | -464.132774 | 8.9204% | 4.426273 | 0.608527 |
| isolated_coverage | stationary | low | b | -456.709574 | 9.3767% | -12.276355 | -0.120231 |
| without_coverage | stationary | low | b | -456.282692 | 8.4040% | 12.276355 | 0.092092 |
| without_round3_government_side | stationary | low | b | -459.055962 | 8.5153% | 9.503085 | 0.203443 |
| without_round3_added_people | stationary | low | b | -464.163269 | 8.2737% | 4.395778 | -0.038174 |
| without_round3_item11_consumption | stationary | low | b | -471.234851 | 8.3056% | -2.675804 | -0.006243 |
| without_round3_completion_receivers | stationary | low | b | -468.755167 | 8.3160% | -0.196119 | 0.004172 |
| government_legacy_response | stationary | low | b | -466.085048 | 8.3626% | 2.473999 | 0.050766 |
| respending_without_government_side | stationary | low | b | -459.055962 | 8.5153% | 9.503085 | 0.203443 |
| neither_budget_side | stationary | low | b | -471.419674 | 8.2628% | -2.860627 | -0.049030 |
| matched_justice_footing | stationary | low | b | -463.990944 | 8.4074% | 4.568103 | 0.095569 |
| borrowing_0 | stationary | low | b | -468.559047 | 8.3119% | 0.000000 | 0.000000 |
| borrowing_1 | stationary | low | b | -468.559047 | 8.3119% | 0.000000 | 0.000000 |
| v8_all_off_fixed_keys | stationary | high | b | -533.961730 | 3.1177% | 26.563055 | -0.147940 |
| isolated_foreign_source_tax | stationary | high | b | -535.358341 | 3.1023% | -1.396612 | -0.015316 |
| without_foreign_source_tax | stationary | high | b | -559.128173 | 3.2700% | 1.396612 | 0.004435 |
| isolated_union_completion | stationary | high | b | -538.463768 | 3.0969% | -4.502038 | -0.020797 |
| without_union_completion | stationary | high | b | -556.022747 | 3.2821% | 4.502038 | 0.016539 |
| isolated_mixed_unit_removal | stationary | high | b | -538.388003 | 3.3339% | -4.426273 | 0.216232 |
| without_mixed_unit_removal | stationary | high | b | -556.098512 | 3.0356% | 4.426273 | -0.229955 |
| isolated_coverage | stationary | high | b | -550.189042 | 3.0711% | -16.227312 | -0.046604 |
| without_coverage | stationary | high | b | -544.297473 | 3.3101% | 16.227312 | 0.044449 |
| without_round3_government_side | stationary | high | b | -550.405322 | 3.3024% | 10.119462 | 0.036815 |
| without_round3_added_people | stationary | high | b | -555.978205 | 3.2159% | 4.546580 | -0.049692 |
| without_round3_item11_consumption | stationary | high | b | -563.200589 | 3.2592% | -2.675804 | -0.006387 |
| without_round3_completion_receivers | stationary | high | b | -560.735417 | 3.2656% | -0.210632 | 0.000000 |
| government_legacy_response | stationary | high | b | -557.434408 | 3.2810% | 3.090376 | 0.015417 |
| respending_without_government_side | stationary | high | b | -550.405322 | 3.3024% | 10.119462 | 0.036815 |
| neither_budget_side | stationary | high | b | -566.100474 | 3.2463% | -5.575689 | -0.019334 |
| matched_justice_footing | stationary | high | b | -560.524785 | 3.2656% | 0.000000 | 0.000000 |
| borrowing_0 | stationary | high | b | -560.524785 | 3.2656% | 0.000000 | 0.000000 |
| borrowing_1 | stationary | high | b | -560.524785 | 3.2656% | 0.000000 | 0.000000 |
| v8_all_off_fixed_keys | cohort30 | low | b | -413.717258 | 15.6650% | 20.451171 | 0.554911 |
| isolated_foreign_source_tax | cohort30 | low | b | -417.427518 | 15.3414% | -3.710260 | -0.323613 |
| without_foreign_source_tax | cohort30 | low | b | -430.458170 | 15.3767% | 3.710260 | 0.266594 |
| isolated_union_completion | cohort30 | low | b | -417.012947 | 15.5936% | -3.295688 | -0.071418 |
| without_union_completion | cohort30 | low | b | -430.872741 | 15.1614% | 3.295688 | 0.051370 |
| isolated_mixed_unit_removal | cohort30 | low | b | -417.994627 | 15.0563% | -4.277368 | -0.608666 |
| without_mixed_unit_removal | cohort30 | low | b | -429.891062 | 15.6693% | 4.277368 | 0.559275 |
| isolated_coverage | cohort30 | low | b | -422.856367 | 16.0039% | -9.139108 | 0.338926 |
| without_coverage | cohort30 | low | b | -425.029321 | 14.7637% | 9.139108 | -0.346371 |
| without_round3_government_side | cohort30 | low | b | -424.665345 | 15.3835% | 9.503085 | 0.273477 |
| without_round3_added_people | cohort30 | low | b | -429.772651 | 15.1675% | 4.395778 | 0.057473 |
| without_round3_item11_consumption | cohort30 | low | b | -436.844233 | 15.0672% | -2.675804 | -0.042879 |
| without_round3_completion_receivers | cohort30 | low | b | -434.364549 | 15.1018% | -0.196119 | -0.008272 |
| government_legacy_response | cohort30 | low | b | -431.694431 | 15.1852% | 2.473999 | 0.075146 |
| respending_without_government_side | cohort30 | low | b | -424.665345 | 15.3835% | 9.503085 | 0.273477 |
| neither_budget_side | cohort30 | low | b | -437.029057 | 15.0394% | -2.860627 | -0.070631 |
| matched_justice_footing | cohort30 | low | b | -429.600327 | 15.2379% | 4.568103 | 0.127807 |
| borrowing_0 | cohort30 | low | b | -434.665937 | 15.1291% | -0.497508 | 0.019035 |
| borrowing_1 | cohort30 | low | b | -432.820126 | 15.1004% | 1.348304 | -0.009689 |
| v8_all_off_fixed_keys | cohort30 | high | b | -502.350263 | 6.8026% | 22.881804 | 0.047660 |
| isolated_foreign_source_tax | cohort30 | high | b | -503.723059 | 6.7579% | -1.372796 | -0.044738 |
| without_foreign_source_tax | cohort30 | high | b | -523.859271 | 6.7997% | 1.372796 | 0.044757 |
| isolated_union_completion | cohort30 | high | b | -506.521043 | 6.7742% | -4.170779 | -0.028438 |
| without_union_completion | cohort30 | high | b | -521.061288 | 6.7854% | 4.170779 | 0.030420 |
| isolated_mixed_unit_removal | cohort30 | high | b | -506.627631 | 6.6589% | -4.277368 | -0.143739 |
| without_mixed_unit_removal | cohort30 | high | b | -520.954699 | 6.8985% | 4.277368 | 0.143547 |
| isolated_coverage | cohort30 | high | b | -515.400487 | 6.9825% | -13.050224 | 0.179855 |
| without_coverage | cohort30 | high | b | -512.181843 | 6.5741% | 13.050224 | -0.180845 |
| without_round3_government_side | cohort30 | high | b | -515.112605 | 6.8912% | 10.119462 | 0.136258 |
| without_round3_added_people | cohort30 | high | b | -520.685487 | 6.7138% | 4.546580 | -0.041221 |
| without_round3_item11_consumption | cohort30 | high | b | -527.907871 | 6.7348% | -2.675804 | -0.020226 |
| without_round3_completion_receivers | cohort30 | high | b | -525.442699 | 6.7531% | -0.210632 | -0.001844 |
| government_legacy_response | cohort30 | high | b | -522.141691 | 6.8078% | 3.090376 | 0.052777 |
| respending_without_government_side | cohort30 | high | b | -515.112605 | 6.8912% | 10.119462 | 0.136258 |
| neither_budget_side | cohort30 | high | b | -530.807756 | 6.6804% | -5.575689 | -0.074607 |
| matched_justice_footing | cohort30 | high | b | -525.232067 | 6.7550% | 0.000000 | 0.000000 |
| borrowing_0 | cohort30 | high | b | -526.631675 | 6.7679% | -1.399608 | 0.012970 |
| borrowing_1 | cohort30 | high | b | -521.438966 | 6.7952% | 3.793101 | 0.040200 |
| v8_all_off_fixed_keys | cohort10 | low | b | -414.022703 | 15.6466% | 20.505799 | 0.555917 |
| isolated_foreign_source_tax | cohort10 | low | b | -417.779548 | 15.3035% | -3.756845 | -0.343067 |
| without_foreign_source_tax | cohort10 | low | b | -430.771657 | 15.3669% | 3.756845 | 0.276217 |
| isolated_union_completion | cohort10 | low | b | -417.300932 | 15.5841% | -3.278229 | -0.062536 |
| without_union_completion | cohort10 | low | b | -431.250273 | 15.1436% | 3.278229 | 0.052907 |
| isolated_mixed_unit_removal | cohort10 | low | b | -418.407842 | 15.0459% | -4.385138 | -0.600709 |
| without_mixed_unit_removal | cohort10 | low | b | -430.143363 | 15.6548% | 4.385138 | 0.564104 |
| isolated_coverage | cohort10 | low | b | -423.079183 | 15.9890% | -9.056479 | 0.342392 |
| without_coverage | cohort10 | low | b | -425.472022 | 14.7242% | 9.056479 | -0.366507 |
| without_round3_government_side | cohort10 | low | b | -425.025417 | 15.3366% | 9.503085 | 0.245880 |
| without_round3_added_people | cohort10 | low | b | -430.132724 | 15.1243% | 4.395778 | 0.033651 |
| without_round3_item11_consumption | cohort10 | low | b | -437.204306 | 15.0549% | -2.675804 | -0.035803 |
| without_round3_completion_receivers | cohort10 | low | b | -434.724621 | 15.0862% | -0.196119 | -0.004490 |
| government_legacy_response | cohort10 | low | b | -432.054503 | 15.1448% | 2.473999 | 0.054059 |
| respending_without_government_side | cohort10 | low | b | -425.025417 | 15.3366% | 9.503085 | 0.245880 |
| neither_budget_side | cohort10 | low | b | -437.389129 | 15.0339% | -2.860627 | -0.056795 |
| matched_justice_footing | cohort10 | low | b | -429.960399 | 15.1949% | 4.568103 | 0.104193 |
| borrowing_0 | cohort10 | low | b | -434.665937 | 15.1291% | -0.137435 | 0.038405 |
| borrowing_1 | cohort10 | low | b | -434.156036 | 14.9609% | 0.372466 | -0.129800 |
| v8_all_off_fixed_keys | cohort10 | high | b | -503.303832 | 6.7253% | 22.941204 | 0.065270 |
| isolated_foreign_source_tax | cohort10 | high | b | -504.693865 | 6.6632% | -1.390033 | -0.062112 |
| without_foreign_source_tax | cohort10 | high | b | -524.855003 | 6.6916% | 1.390033 | 0.031536 |
| isolated_union_completion | cohort10 | high | b | -507.462665 | 6.6986% | -4.158833 | -0.026720 |
| without_union_completion | cohort10 | high | b | -522.086203 | 6.6873% | 4.158833 | 0.027277 |
| isolated_mixed_unit_removal | cohort10 | high | b | -507.688970 | 6.5674% | -4.385138 | -0.157944 |
| without_mixed_unit_removal | cohort10 | high | b | -521.859897 | 6.7963% | 4.385138 | 0.136298 |
| isolated_coverage | cohort10 | high | b | -516.300262 | 6.8830% | -12.996430 | 0.157684 |
| without_coverage | cohort10 | high | b | -513.248606 | 6.4923% | 12.996430 | -0.167790 |
| without_round3_government_side | cohort10 | high | b | -516.125574 | 6.8005% | 10.119462 | 0.140436 |
| without_round3_added_people | cohort10 | high | b | -521.698456 | 6.6284% | 4.546580 | -0.031652 |
| without_round3_item11_consumption | cohort10 | high | b | -528.920840 | 6.6488% | -2.675804 | -0.011258 |
| without_round3_completion_receivers | cohort10 | high | b | -526.455668 | 6.6600% | -0.210632 | 0.000000 |
| government_legacy_response | cohort10 | high | b | -523.154659 | 6.7039% | 3.090376 | 0.043850 |
| respending_without_government_side | cohort10 | high | b | -516.125574 | 6.8005% | 10.119462 | 0.140436 |
| neither_budget_side | cohort10 | high | b | -531.820725 | 6.5851% | -5.575689 | -0.074980 |
| matched_justice_footing | cohort10 | high | b | -526.245036 | 6.6600% | 0.000000 | 0.000000 |
| borrowing_0 | cohort10 | high | b | -526.631675 | 6.7679% | -0.386639 | 0.107904 |
| borrowing_1 | cohort10 | high | b | -525.197199 | 6.3729% | 1.047837 | -0.287111 |
| v8_all_off_fixed_keys | stationary | low | c | -444.433219 | 14.5721% | 24.125828 | 1.394306 |
| isolated_foreign_source_tax | stationary | low | c | -448.207845 | 14.3035% | -3.774626 | -0.268609 |
| without_foreign_source_tax | stationary | low | c | -464.784422 | 13.3969% | 3.774626 | 0.219043 |
| isolated_union_completion | stationary | low | c | -448.052548 | 14.3562% | -3.619329 | -0.215899 |
| without_union_completion | stationary | low | c | -464.939718 | 13.4220% | 3.619329 | 0.244122 |
| isolated_mixed_unit_removal | stationary | low | c | -448.859492 | 14.1169% | -4.426273 | -0.455261 |
| without_mixed_unit_removal | stationary | low | c | -464.132774 | 13.6050% | 4.426273 | 0.427173 |
| isolated_coverage | stationary | low | c | -456.709574 | 14.0784% | -12.276355 | -0.493719 |
| without_coverage | stationary | low | c | -456.282692 | 13.6833% | 12.276355 | 0.505471 |
| without_round3_government_side | stationary | low | c | -459.055962 | 13.9154% | 9.503085 | 0.737574 |
| without_round3_added_people | stationary | low | c | -464.163269 | 13.3918% | 4.395778 | 0.213928 |
| without_round3_item11_consumption | stationary | low | c | -471.234851 | 13.0951% | -2.675804 | -0.082764 |
| without_round3_completion_receivers | stationary | low | c | -468.755167 | 13.1749% | -0.196119 | -0.002933 |
| government_legacy_response | stationary | low | c | -466.085048 | 13.3246% | 2.473999 | 0.146775 |
| respending_without_government_side | stationary | low | c | -459.055962 | 13.9154% | 9.503085 | 0.737574 |
| neither_budget_side | stationary | low | c | -471.419674 | 13.0465% | -2.860627 | -0.131322 |
| matched_justice_footing | stationary | low | c | -463.990944 | 13.2666% | 4.568103 | 0.088799 |
| borrowing_0 | stationary | low | c | -468.559047 | 14.5474% | 0.000000 | 1.369607 |
| borrowing_1 | stationary | low | c | -468.559047 | 10.9176% | -0.000000 | -2.260234 |
| v8_all_off_fixed_keys | stationary | high | c | -533.961730 | 5.7108% | 26.563055 | 0.317324 |
| isolated_foreign_source_tax | stationary | high | c | -535.358341 | 5.6729% | -1.396612 | -0.037879 |
| without_foreign_source_tax | stationary | high | c | -559.128173 | 5.4308% | 1.396612 | 0.037385 |
| isolated_union_completion | stationary | high | c | -538.463768 | 5.6305% | -4.502038 | -0.080260 |
| without_union_completion | stationary | high | c | -556.022747 | 5.4497% | 4.502038 | 0.056285 |
| isolated_mixed_unit_removal | stationary | high | c | -538.388003 | 5.6679% | -4.426273 | -0.042883 |
| without_mixed_unit_removal | stationary | high | c | -556.098512 | 5.4054% | 4.426273 | 0.011988 |
| isolated_coverage | stationary | high | c | -550.189042 | 5.4978% | -16.227312 | -0.212998 |
| without_coverage | stationary | high | c | -544.297473 | 5.5786% | 16.227312 | 0.185217 |
| without_round3_government_side | stationary | high | c | -550.405322 | 5.6986% | 10.119462 | 0.305196 |
| without_round3_added_people | stationary | high | c | -555.978205 | 5.4112% | 4.546580 | 0.017781 |
| without_round3_item11_consumption | stationary | high | c | -563.200589 | 5.3554% | -2.675804 | -0.037982 |
| without_round3_completion_receivers | stationary | high | c | -560.735417 | 5.3928% | -0.210632 | -0.000637 |
| government_legacy_response | stationary | high | c | -557.434408 | 5.4716% | 3.090376 | 0.078168 |
| respending_without_government_side | stationary | high | c | -550.405322 | 5.6986% | 10.119462 | 0.305196 |
| neither_budget_side | stationary | high | c | -566.100474 | 5.2472% | -5.575689 | -0.146277 |
| matched_justice_footing | stationary | high | c | -560.524785 | 5.3934% | 0.000000 | 0.000000 |
| borrowing_0 | stationary | high | c | -560.524785 | 6.8015% | 0.000000 | 1.408091 |
| borrowing_1 | stationary | high | c | -560.524785 | 3.9420% | 0.000000 | -1.451390 |
| v8_all_off_fixed_keys | cohort30 | low | c | -413.717258 | 20.1081% | 20.451171 | 0.649668 |
| isolated_foreign_source_tax | cohort30 | low | c | -417.427518 | 19.9204% | -3.710260 | -0.187653 |
| without_foreign_source_tax | cohort30 | low | c | -430.458170 | 19.7409% | 3.710260 | 0.282462 |
| isolated_union_completion | cohort30 | low | c | -417.012947 | 20.0050% | -3.295688 | -0.103073 |
| without_union_completion | cohort30 | low | c | -430.872741 | 19.6016% | 3.295688 | 0.143204 |
| isolated_mixed_unit_removal | cohort30 | low | c | -417.994627 | 19.7371% | -4.277368 | -0.370973 |
| without_mixed_unit_removal | cohort30 | low | c | -429.891062 | 19.8534% | 4.277368 | 0.395030 |
| isolated_coverage | cohort30 | low | c | -422.856367 | 20.1939% | -9.139108 | 0.085803 |
| without_coverage | cohort30 | low | c | -425.029321 | 19.3515% | 9.139108 | -0.106875 |
| without_round3_government_side | cohort30 | low | c | -424.665345 | 20.1257% | 9.503085 | 0.667298 |
| without_round3_added_people | cohort30 | low | c | -429.772651 | 19.7941% | 4.395778 | 0.335704 |
| without_round3_item11_consumption | cohort30 | low | c | -436.844233 | 19.3113% | -2.675804 | -0.147157 |
| without_round3_completion_receivers | cohort30 | low | c | -434.364549 | 19.4533% | -0.196119 | -0.005071 |
| government_legacy_response | cohort30 | low | c | -431.694431 | 19.6675% | 2.473999 | 0.209046 |
| respending_without_government_side | cohort30 | low | c | -424.665345 | 20.1257% | 9.503085 | 0.667298 |
| neither_budget_side | cohort30 | low | c | -437.029057 | 19.2849% | -2.860627 | -0.173498 |
| matched_justice_footing | cohort30 | low | c | -429.600327 | 19.5840% | 4.568103 | 0.125633 |
| borrowing_0 | cohort30 | low | c | -434.665937 | 20.9173% | -0.497508 | 1.458843 |
| borrowing_1 | cohort30 | low | c | -432.820126 | 16.2647% | 1.348304 | -3.193680 |
| v8_all_off_fixed_keys | cohort30 | high | c | -502.350263 | 11.2339% | 22.881804 | 0.494123 |
| isolated_foreign_source_tax | cohort30 | high | c | -503.723059 | 11.1907% | -1.372796 | -0.043173 |
| without_foreign_source_tax | cohort30 | high | c | -523.859271 | 10.8139% | 1.372796 | 0.074138 |
| isolated_union_completion | cohort30 | high | c | -506.521043 | 11.1704% | -4.170779 | -0.063507 |
| without_union_completion | cohort30 | high | c | -521.061288 | 10.8398% | 4.170779 | 0.099982 |
| isolated_mixed_unit_removal | cohort30 | high | c | -506.627631 | 10.8751% | -4.277368 | -0.358816 |
| without_mixed_unit_removal | cohort30 | high | c | -520.954699 | 11.1174% | 4.277368 | 0.377627 |
| isolated_coverage | cohort30 | high | c | -515.400487 | 11.2602% | -13.050224 | 0.026296 |
| without_coverage | cohort30 | high | c | -512.181843 | 10.7586% | 13.050224 | 0.018864 |
| without_round3_government_side | cohort30 | high | c | -515.112605 | 11.2468% | 10.119462 | 0.507036 |
| without_round3_added_people | cohort30 | high | c | -520.685487 | 10.9409% | 4.546580 | 0.201066 |
| without_round3_item11_consumption | cohort30 | high | c | -527.907871 | 10.6174% | -2.675804 | -0.122372 |
| without_round3_completion_receivers | cohort30 | high | c | -525.442699 | 10.7334% | -0.210632 | -0.006428 |
| government_legacy_response | cohort30 | high | c | -522.141691 | 10.9074% | 3.090376 | 0.167632 |
| respending_without_government_side | cohort30 | high | c | -515.112605 | 11.2468% | 10.119462 | 0.507036 |
| neither_budget_side | cohort30 | high | c | -530.807756 | 10.5054% | -5.575689 | -0.234405 |
| matched_justice_footing | cohort30 | high | c | -525.232067 | 10.7398% | 0.000000 | 0.000000 |
| borrowing_0 | cohort30 | high | c | -526.631675 | 12.2833% | -1.399608 | 1.543516 |
| borrowing_1 | cohort30 | high | c | -521.438966 | 7.8125% | 3.793101 | -2.927279 |
| v8_all_off_fixed_keys | cohort10 | low | c | -414.022703 | 20.0714% | 20.505799 | 0.674785 |
| isolated_foreign_source_tax | cohort10 | low | c | -417.779548 | 19.8304% | -3.756845 | -0.241055 |
| without_foreign_source_tax | cohort10 | low | c | -430.771657 | 19.6504% | 3.756845 | 0.253759 |
| isolated_union_completion | cohort10 | low | c | -417.300932 | 19.9501% | -3.278229 | -0.121282 |
| without_union_completion | cohort10 | low | c | -431.250273 | 19.4988% | 3.278229 | 0.102152 |
| isolated_mixed_unit_removal | cohort10 | low | c | -418.407842 | 19.6195% | -4.385138 | -0.451953 |
| without_mixed_unit_removal | cohort10 | low | c | -430.143363 | 19.8336% | 4.385138 | 0.437006 |
| isolated_coverage | cohort10 | low | c | -423.079183 | 20.1655% | -9.056479 | 0.094028 |
| without_coverage | cohort10 | low | c | -425.472022 | 19.2613% | 9.056479 | -0.135307 |
| without_round3_government_side | cohort10 | low | c | -425.025417 | 20.0634% | 9.503085 | 0.666793 |
| without_round3_added_people | cohort10 | low | c | -430.132724 | 19.7115% | 4.395778 | 0.314879 |
| without_round3_item11_consumption | cohort10 | low | c | -437.204306 | 19.2664% | -2.675804 | -0.130276 |
| without_round3_completion_receivers | cohort10 | low | c | -434.724621 | 19.3891% | -0.196119 | -0.007582 |
| government_legacy_response | cohort10 | low | c | -432.054503 | 19.5607% | 2.473999 | 0.164014 |
| respending_without_government_side | cohort10 | low | c | -425.025417 | 20.0634% | 9.503085 | 0.666793 |
| neither_budget_side | cohort10 | low | c | -437.389129 | 19.2462% | -2.860627 | -0.150410 |
| matched_justice_footing | cohort10 | low | c | -429.960399 | 19.5163% | 4.568103 | 0.119632 |
| borrowing_0 | cohort10 | low | c | -434.665937 | 20.9173% | -0.137435 | 1.520619 |
| borrowing_1 | cohort10 | low | c | -434.156036 | 16.1450% | 0.372466 | -3.251618 |
| v8_all_off_fixed_keys | cohort10 | high | c | -503.303832 | 11.0406% | 22.941204 | 0.483492 |
| isolated_foreign_source_tax | cohort10 | high | c | -504.693865 | 10.9817% | -1.390033 | -0.058850 |
| without_foreign_source_tax | cohort10 | high | c | -524.855003 | 10.6001% | 1.390033 | 0.042993 |
| isolated_union_completion | cohort10 | high | c | -507.462665 | 10.9704% | -4.158833 | -0.070145 |
| without_union_completion | cohort10 | high | c | -522.086203 | 10.5963% | 4.158833 | 0.039183 |
| isolated_mixed_unit_removal | cohort10 | high | c | -507.688970 | 10.6721% | -4.385138 | -0.368448 |
| without_mixed_unit_removal | cohort10 | high | c | -521.859897 | 10.9627% | 4.385138 | 0.405607 |
| isolated_coverage | cohort10 | high | c | -516.300262 | 11.0764% | -12.996430 | 0.035789 |
| without_coverage | cohort10 | high | c | -513.248606 | 10.5268% | 12.996430 | -0.030325 |
| without_round3_government_side | cohort10 | high | c | -516.125574 | 11.0416% | 10.119462 | 0.484542 |
| without_round3_added_people | cohort10 | high | c | -521.698456 | 10.7168% | 4.546580 | 0.159688 |
| without_round3_item11_consumption | cohort10 | high | c | -528.920840 | 10.4593% | -2.675804 | -0.097833 |
| without_round3_completion_receivers | cohort10 | high | c | -526.455668 | 10.5486% | -0.210632 | -0.008482 |
| government_legacy_response | cohort10 | high | c | -523.154659 | 10.7101% | 3.090376 | 0.152964 |
| respending_without_government_side | cohort10 | high | c | -516.125574 | 11.0416% | 10.119462 | 0.484542 |
| neither_budget_side | cohort10 | high | c | -531.820725 | 10.3002% | -5.575689 | -0.256879 |
| matched_justice_footing | cohort10 | high | c | -526.245036 | 10.5571% | 0.000000 | 0.000000 |
| borrowing_0 | cohort10 | high | c | -526.631675 | 12.2833% | -0.386639 | 1.726207 |
| borrowing_1 | cohort10 | high | c | -525.197199 | 7.2183% | 1.047837 | -3.338761 |



Government purchases removed and re-spending of the saving are both central, with the same age-mortality recipient vector. Their one-sided and neither-side readings are named beside variants. The low fiscal row uses the adopted case while victims keep equal NCVS footing; matched_justice_footing stays beside. The added people's crime sender rows are zero; their other rows use the producer's own key shares, including item 11's consumption shift. Current row levels and declared producer ranges come from the live JSON; producer ratios transport its uncertainty, while separately declared point budget counterflows stay fixed. [DATA: live real_costs_totals.json v8_social_environment; p7_channel_coverage.csv]



### Joint change from accepted oct14 Phase A



| frame | level | financing | total_bn_oct14 | total_bn_oct15 | delta_total_bn | winners_share_oct14 | winners_share_oct15 | delta_ahead_pp |
|---|---|---|---|---|---|---|---|---|
| stationary | low | a | -166.016109 | -186.443126 | -20.427017 | 38.0203% | 41.8631% | 3.842810 |
| stationary | central | a | -483.071540 | -514.541916 | -31.470376 | 3.3392% | 2.6140% | -0.725230 |
| stationary | high | a | -794.037481 | -844.313155 | -50.275673 | 1.3945% | 2.7980% | 1.403462 |
| cohort30 | low | a | -135.423617 | -152.052508 | -16.628892 | 37.0670% | 38.7429% | 1.675877 |
| cohort30 | central | a | -452.035388 | -479.700248 | -27.664861 | 8.7499% | 7.3989% | -1.350987 |
| cohort30 | high | a | -762.557669 | -809.020437 | -46.462768 | 1.4793% | 2.9927% | 1.513433 |
| cohort10 | low | a | -135.726414 | -152.412580 | -16.686166 | 37.0364% | 38.7179% | 1.681475 |
| cohort10 | central | a | -452.659443 | -480.386769 | -27.727326 | 8.6929% | 7.2975% | -1.395406 |
| cohort10 | high | a | -763.502982 | -810.033406 | -46.530424 | 1.4808% | 2.9912% | 1.510480 |
| stationary | low | b | -166.016109 | -186.443126 | -20.427017 | 36.2336% | 39.4044% | 3.170862 |
| stationary | central | b | -483.071540 | -514.541916 | -31.470376 | 5.5002% | 4.4926% | -1.007589 |
| stationary | high | b | -794.037481 | -844.313155 | -50.275673 | 1.8401% | 3.0309% | 1.190720 |
| cohort30 | low | b | -135.423617 | -152.052508 | -16.628892 | 36.4572% | 37.8530% | 1.395747 |
| cohort30 | central | b | -452.035388 | -479.700248 | -27.664861 | 11.4392% | 10.2894% | -1.149780 |
| cohort30 | high | b | -762.557669 | -809.020437 | -46.462768 | 2.8893% | 3.8448% | 0.955528 |
| cohort10 | low | b | -135.726414 | -152.412580 | -16.686166 | 36.3949% | 37.7444% | 1.349521 |
| cohort10 | central | b | -452.659443 | -480.386769 | -27.727326 | 11.3728% | 10.2282% | -1.144636 |
| cohort10 | high | b | -763.502982 | -810.033406 | -46.530424 | 2.8658% | 3.8082% | 0.942381 |
| stationary | low | c | -166.016109 | -186.443126 | -20.427017 | 38.8739% | 41.4392% | 2.565318 |
| stationary | central | c | -483.071540 | -514.541916 | -31.470376 | 9.7373% | 8.0294% | -1.707913 |
| stationary | high | c | -794.037481 | -844.313155 | -50.275673 | 2.3181% | 3.5593% | 1.241142 |
| cohort30 | low | c | -135.423617 | -152.052508 | -16.628892 | 40.0211% | 41.7275% | 1.706421 |
| cohort30 | central | c | -452.035388 | -479.700248 | -27.664861 | 15.9081% | 14.7177% | -1.190328 |
| cohort30 | high | c | -762.557669 | -809.020437 | -46.462768 | 4.0175% | 4.7692% | 0.751756 |
| cohort10 | low | c | -135.726414 | -152.412580 | -16.686166 | 40.0083% | 41.6993% | 1.691010 |
| cohort10 | central | c | -452.659443 | -480.386769 | -27.727326 | 15.7825% | 14.5937% | -1.188846 |
| cohort10 | high | c | -763.502982 | -810.033406 | -46.530424 | 3.9294% | 4.7394% | 0.809926 |



The accepted Phase-A reference is an archived calculated table; no oct14 output is regenerated. The comparison retains all Phase-A corrections and the stationary-first ruling. [DATA: inputs/phase_a_joint_oct14.csv]



### Geography, uncertainty, provenance and limits



| arm | financing | cut | group | persons_m | mean_usd | winners_share |
|---|---|---|---|---|---|---|
| recommended | a | tenure | landlord | 24.221679 | -1137.589043 | 22.1196% |
| recommended | a | tenure | owner_no_rental_income | 182.500990 | -1691.535289 | 0.9738% |
| recommended | a | tenure | renter | 85.551404 | -2083.901902 | 0.5903% |
| recommended | a | state3 | CA | 25.246685 | -5428.719931 | 2.9521% |
| recommended | a | state3 | TX | 20.163439 | -4009.258461 | 2.4249% |
| recommended | a | state3 | rest | 246.863949 | -1201.650927 | 2.5949% |
| stack | a | tenure | landlord | 24.221679 | -3426.841449 | 2.2244% |
| stack | a | tenure | owner_no_rental_income | 182.500990 | -1737.167582 | 0.9725% |
| stack | a | tenure | renter | 85.551404 | -1338.414725 | 2.8836% |
| stack | a | state3 | CA | 25.246685 | -5509.092932 | 6.1969% |
| stack | a | state3 | TX | 20.163439 | -4010.197120 | 4.3146% |
| stack | a | state3 | rest | 246.863949 | -1193.354542 | 0.9504% |
| coverage | a | tenure | landlord | 24.221679 | -1188.808026 | 14.9462% |
| coverage | a | tenure | owner_no_rental_income | 182.500990 | -1707.132240 | 0.2846% |
| coverage | a | tenure | renter | 85.551404 | -2047.786523 | 0.0835% |
| coverage | a | state3 | CA | 25.246685 | -5473.058276 | 1.8924% |
| coverage | a | state3 | TX | 20.163439 | -3969.390489 | 1.7108% |
| coverage | a | state3 | rest | 246.863949 | -1204.412880 | 1.3726% |
| item11_attribution | a | tenure | landlord | 24.221679 | -1107.286230 | 22.3113% |
| item11_attribution | a | tenure | owner_no_rental_income | 182.500990 | -1664.981149 | 1.1380% |
| item11_attribution | a | tenure | renter | 85.551404 | -2066.112189 | 0.7986% |
| item11_attribution | a | state3 | CA | 25.246685 | -5361.113878 | 3.2421% |
| item11_attribution | a | state3 | TX | 20.163439 | -3937.622804 | 2.8530% |
| item11_attribution | a | state3 | rest | 246.863949 | -1185.646862 | 2.7426% |
| recommended | b | tenure | landlord | 24.221679 | -217.280112 | 27.9374% |
| recommended | b | tenure | owner_no_rental_income | 182.500990 | -1670.656352 | 3.0733% |
| recommended | b | tenure | renter | 85.551404 | -2389.003310 | 0.8824% |
| recommended | b | state3 | CA | 25.246685 | -5378.902689 | 3.1088% |
| recommended | b | state3 | TX | 20.163439 | -3998.413149 | 2.8470% |
| recommended | b | state3 | rest | 246.863949 | -1207.631545 | 4.7685% |
| stack | b | tenure | landlord | 24.221679 | -3278.597666 | 3.0767% |
| stack | b | tenure | owner_no_rental_income | 182.500990 | -1734.752649 | 1.2396% |
| stack | b | tenure | renter | 85.551404 | -1385.537751 | 2.9505% |
| stack | b | state3 | CA | 25.246685 | -5459.275690 | 6.4266% |
| stack | b | state3 | TX | 20.163439 | -3999.351808 | 5.0053% |
| stack | b | state3 | rest | 246.863949 | -1199.335160 | 1.1747% |
| coverage | b | tenure | landlord | 24.221679 | -268.499095 | 22.3879% |
| coverage | b | tenure | owner_no_rental_income | 182.500990 | -1686.253303 | 2.4815% |
| coverage | b | tenure | renter | 85.551404 | -2352.887930 | 0.7853% |
| coverage | b | state3 | CA | 25.246685 | -5423.241034 | 2.5525% |
| coverage | b | state3 | TX | 20.163439 | -3958.545177 | 2.9856% |
| coverage | b | state3 | rest | 246.863949 | -1210.393498 | 3.7984% |
| item11_attribution | b | tenure | landlord | 24.221679 | -186.977299 | 28.0293% |
| item11_attribution | b | tenure | owner_no_rental_income | 182.500990 | -1644.102212 | 3.2118% |
| item11_attribution | b | tenure | renter | 85.551404 | -2371.213596 | 1.0726% |
| item11_attribution | b | state3 | CA | 25.246685 | -5311.296636 | 3.3300% |
| item11_attribution | b | state3 | TX | 20.163439 | -3926.777492 | 3.4134% |
| item11_attribution | b | state3 | rest | 246.863949 | -1191.627480 | 4.8769% |
| recommended | c | tenure | landlord | 24.221679 | -5.726608 | 35.0321% |
| recommended | c | tenure | owner_no_rental_income | 182.500990 | -1559.348772 | 7.6019% |
| recommended | c | tenure | renter | 85.551404 | -2686.344128 | 1.2962% |
| recommended | c | state3 | CA | 25.246685 | -5391.777465 | 4.3327% |
| recommended | c | state3 | TX | 20.163439 | -3984.351167 | 3.8064% |
| recommended | c | state3 | rest | 246.863949 | -1207.463406 | 8.7524% |
| stack | c | tenure | landlord | 24.221679 | -3184.092989 | 5.7633% |
| stack | c | tenure | owner_no_rental_income | 182.500990 | -1680.311388 | 3.4337% |
| stack | c | tenure | renter | 85.551404 | -1528.430156 | 3.4481% |
| stack | c | state3 | CA | 25.246685 | -5472.150466 | 6.4477% |
| stack | c | state3 | TX | 20.163439 | -3985.289827 | 5.0139% |
| stack | c | state3 | rest | 246.863949 | -1199.167021 | 3.2300% |
| coverage | c | tenure | landlord | 24.221679 | -56.945591 | 29.8448% |
| coverage | c | tenure | owner_no_rental_income | 182.500990 | -1574.945724 | 7.1974% |
| coverage | c | tenure | renter | 85.551404 | -2650.228749 | 1.8636% |
| coverage | c | state3 | CA | 25.246685 | -5436.115811 | 3.6924% |
| coverage | c | state3 | TX | 20.163439 | -3944.483195 | 2.9356% |
| coverage | c | state3 | rest | 246.863949 | -1210.225359 | 8.2776% |
| item11_attribution | c | tenure | landlord | 24.221679 | 24.576205 | 35.2191% |
| item11_attribution | c | tenure | owner_no_rental_income | 182.500990 | -1532.794632 | 7.7885% |
| item11_attribution | c | tenure | renter | 85.551404 | -2668.554415 | 1.4744% |
| item11_attribution | c | state3 | CA | 25.246685 | -5324.171412 | 4.5008% |
| item11_attribution | c | state3 | TX | 20.163439 | -3912.715510 | 4.2840% |
| item11_attribution | c | state3 | rest | 246.863949 | -1191.459341 | 8.9142% |



State and landlord claims are specific to the displayed arm. Rental stock enters capitalization, and landlord ownership reassignment preserves state dollars. FARS fatal victim ages/roles proxy crash injuries. School correction geography remains an explicitly degraded administrative/district proxy, and S&L net financing follows responded spending geography. Source item 11 retains its adopted fixed-membership counterfactual; the item10 × item11 nonlinear recomputation is uncomputed. Unlocated stayer flows use named same-state buckets and D a national per-head bucket. Coverage is constructed, with source limitations. The LLM instrument can introduce framing bias. [DEGRADED / FRAMING-SENSITIVE; DATA: p7_inputs.json]



| extreme | sharing | future_bn | case | financing | frame | level | arm | social_setting | persons_m | total_bn | winners_share | losers_share | mean_usd |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| share_min | mixed_unit | -34.030546 | oct15 | a | cohort10 | low | stack | high | 292.274073 | -767.517633 | 1.5968% | 98.4032% | -2626.020240 |
| share_max | mixed_unit | -34.030546 | oct15 | a | cohort10 | low | stack | low | 292.274073 | -208.422884 | 39.0288% | 60.9712% | -713.107670 |
| dollar_min | mixed_unit | -34.279749 | oct15 | a | cohort10 | high | stack | high | 292.274073 | -866.043709 | 2.6472% | 97.3528% | -2963.121904 |
| dollar_max | mixed_unit | -34.030546 | oct15 | a | cohort10 | low | recommended | low | 292.274073 | -208.422884 | 38.6185% | 61.3815% | -713.107670 |
| share_min | person | -34.030546 | oct15 | a | cohort10 | low | stack | high | 292.274073 | -711.507329 | 2.4358% | 97.5642% | -2434.384004 |
| share_max | person | -34.030546 | oct15 | a | cohort10 | low | stack | low | 292.274073 | -152.412580 | 40.7530% | 59.2470% | -521.471434 |
| dollar_min | person | -34.279749 | oct15 | a | cohort10 | high | recommended | high | 292.274073 | -810.033406 | 3.6485% | 96.3515% | -2771.485668 |
| dollar_max | person | -34.030546 | oct15 | a | cohort10 | low | stack | low | 292.274073 | -152.412580 | 40.7530% | 59.2470% | -521.471434 |
| share_min | pooled | -34.030546 | oct15 | a | cohort10 | low | stack | high | 292.274073 | -711.507329 | 1.4544% | 98.5456% | -2434.384004 |
| share_max | pooled | -34.030546 | oct15 | a | cohort10 | low | stack | low | 292.274073 | -152.412580 | 39.1450% | 60.8550% | -521.471434 |
| dollar_min | pooled | -34.279749 | oct15 | a | cohort10 | high | stack | high | 292.274073 | -810.033406 | 2.5286% | 97.4714% | -2771.485668 |
| dollar_max | pooled | -34.030546 | oct15 | a | cohort10 | low | stack | low | 292.274073 | -152.412580 | 39.1450% | 60.8550% | -521.471434 |
| share_min | mixed_unit | -34.390618 | oct15 | a | cohort30 | low | stack | high | 292.274073 | -767.157561 | 1.5979% | 98.4021% | -2624.788273 |
| share_max | mixed_unit | -34.390618 | oct15 | a | cohort30 | low | stack | low | 292.274073 | -208.062811 | 39.1402% | 60.8598% | -711.875703 |
| dollar_min | mixed_unit | -35.292718 | oct15 | a | cohort30 | high | recommended | high | 292.274073 | -865.030740 | 3.1051% | 96.8949% | -2959.656085 |
| dollar_max | mixed_unit | -34.390618 | oct15 | a | cohort30 | low | stack | low | 292.274073 | -208.062811 | 39.1402% | 60.8598% | -711.875703 |
| share_min | person | -34.390618 | oct15 | a | cohort30 | low | stack | high | 292.274073 | -711.147257 | 2.4416% | 97.5584% | -2433.152037 |
| share_max | person | -34.390618 | oct15 | a | cohort30 | low | stack | low | 292.274073 | -152.052508 | 40.8780% | 59.1220% | -520.239467 |
| dollar_min | person | -35.292718 | oct15 | a | cohort30 | high | recommended | high | 292.274073 | -809.020437 | 3.7144% | 96.2856% | -2768.019849 |
| dollar_max | person | -34.390618 | oct15 | a | cohort30 | low | recommended | low | 292.274073 | -152.052508 | 37.1442% | 62.8558% | -520.239467 |
| share_min | pooled | -34.390618 | oct15 | a | cohort30 | low | stack | high | 292.274073 | -711.147257 | 1.4556% | 98.5444% | -2433.152037 |
| share_max | pooled | -34.390618 | oct15 | a | cohort30 | low | stack | low | 292.274073 | -152.052508 | 39.2539% | 60.7461% | -520.239467 |
| dollar_min | pooled | -35.292718 | oct15 | a | cohort30 | high | recommended | high | 292.274073 | -809.020437 | 2.9927% | 97.0073% | -2768.019849 |
| dollar_max | pooled | -34.390618 | oct15 | a | cohort30 | low | recommended | low | 292.274073 | -152.052508 | 38.7429% | 61.2571% | -520.239467 |
| share_min | mixed_unit | -0.000000 | oct15 | a | stationary | low | stack | high | 292.274073 | -801.548178 | 1.4596% | 98.5404% | -2742.453919 |
| share_max | mixed_unit | -0.000000 | oct15 | a | stationary | low | recommended | low | 292.274073 | -242.453429 | 41.7271% | 58.2729% | -829.541349 |
| dollar_min | mixed_unit | -0.000000 | oct15 | a | stationary | high | recommended | high | 292.274073 | -900.323458 | 2.9194% | 97.0806% | -3080.408218 |
| dollar_max | mixed_unit | -0.000000 | oct15 | a | stationary | low | recommended | low | 292.274073 | -242.453429 | 41.7271% | 58.2729% | -829.541349 |
| share_min | person | -0.000000 | oct15 | a | stationary | low | stack | high | 292.274073 | -745.537875 | 1.7993% | 98.2007% | -2550.817683 |
| share_max | person | -0.000000 | oct15 | a | stationary | low | recommended | low | 292.274073 | -186.443126 | 50.8410% | 49.1590% | -637.905113 |
| dollar_min | person | -0.000000 | oct15 | a | stationary | high | stack | high | 292.274073 | -844.313155 | 2.4290% | 97.5710% | -2888.771982 |
| dollar_max | person | -0.000000 | oct15 | a | stationary | low | recommended | low | 292.274073 | -186.443126 | 50.8410% | 49.1590% | -637.905113 |
| share_min | pooled | -0.000000 | oct15 | a | stationary | low | stack | high | 292.274073 | -745.537875 | 1.3034% | 98.6966% | -2550.817683 |
| share_max | pooled | -0.000000 | oct15 | a | stationary | low | recommended | low | 292.274073 | -186.443126 | 41.8631% | 58.1369% | -637.905113 |
| dollar_min | pooled | -0.000000 | oct15 | a | stationary | high | recommended | high | 292.274073 | -844.313155 | 2.7980% | 97.2020% | -2888.771982 |
| dollar_max | pooled | -0.000000 | oct15 | a | stationary | low | recommended | low | 292.274073 | -186.443126 | 41.8631% | 58.1369% | -637.905113 |
| share_min | mixed_unit | -34.030546 | oct15 | b | cohort10 | low | stack | high | 292.274073 | -767.517633 | 1.9302% | 98.0698% | -2626.020240 |
| share_max | mixed_unit | -34.030546 | oct15 | b | cohort10 | low | stack | low | 292.274073 | -208.422884 | 42.2394% | 57.7606% | -713.107670 |
| dollar_min | mixed_unit | -34.279749 | oct15 | b | cohort10 | high | stack | high | 292.274073 | -866.043709 | 3.0326% | 96.9674% | -2963.121904 |
| dollar_max | mixed_unit | -34.030546 | oct15 | b | cohort10 | low | recommended | low | 292.274073 | -208.422884 | 37.6896% | 62.3104% | -713.107670 |
| share_min | person | -34.030546 | oct15 | b | cohort10 | low | stack | high | 292.274073 | -711.507329 | 2.7407% | 97.2593% | -2434.384004 |
| share_max | person | -34.030546 | oct15 | b | cohort10 | low | stack | low | 292.274073 | -152.412580 | 42.8932% | 57.1068% | -521.471434 |
| dollar_min | person | -34.279749 | oct15 | b | cohort10 | high | stack | high | 292.274073 | -810.033406 | 3.3396% | 96.6604% | -2771.485668 |
| dollar_max | person | -34.030546 | oct15 | b | cohort10 | low | stack | low | 292.274073 | -152.412580 | 42.8932% | 57.1068% | -521.471434 |
| share_min | pooled | -34.030546 | oct15 | b | cohort10 | low | stack | high | 292.274073 | -711.507329 | 1.7803% | 98.2197% | -2434.384004 |
| share_max | pooled | -34.030546 | oct15 | b | cohort10 | low | stack | low | 292.274073 | -152.412580 | 42.3685% | 57.6315% | -521.471434 |
| dollar_min | pooled | -34.279749 | oct15 | b | cohort10 | high | stack | high | 292.274073 | -810.033406 | 2.9079% | 97.0921% | -2771.485668 |
| dollar_max | pooled | -34.030546 | oct15 | b | cohort10 | low | recommended | low | 292.274073 | -152.412580 | 37.7444% | 62.2556% | -521.471434 |
| share_min | mixed_unit | -34.390618 | oct15 | b | cohort30 | low | stack | high | 292.274073 | -767.157561 | 1.9329% | 98.0671% | -2624.788273 |
| share_max | mixed_unit | -34.390618 | oct15 | b | cohort30 | low | stack | low | 292.274073 | -208.062811 | 42.2474% | 57.7526% | -711.875703 |
| dollar_min | mixed_unit | -35.292718 | oct15 | b | cohort30 | high | recommended | high | 292.274073 | -865.030740 | 3.9635% | 96.0365% | -2959.656085 |
| dollar_max | mixed_unit | -34.390618 | oct15 | b | cohort30 | low | stack | low | 292.274073 | -208.062811 | 42.2474% | 57.7526% | -711.875703 |
| share_min | person | -34.390618 | oct15 | b | cohort30 | low | stack | high | 292.274073 | -711.147257 | 2.7572% | 97.2428% | -2433.152037 |
| share_max | person | -34.390618 | oct15 | b | cohort30 | low | stack | low | 292.274073 | -152.052508 | 42.9777% | 57.0223% | -520.239467 |
| dollar_min | person | -35.292718 | oct15 | b | cohort30 | high | stack | high | 292.274073 | -809.020437 | 3.3725% | 96.6275% | -2768.019849 |
| dollar_max | person | -34.390618 | oct15 | b | cohort30 | low | stack | low | 292.274073 | -152.052508 | 42.9777% | 57.0223% | -520.239467 |
| share_min | pooled | -34.390618 | oct15 | b | cohort30 | low | stack | high | 292.274073 | -711.147257 | 1.7828% | 98.2172% | -2433.152037 |
| share_max | pooled | -34.390618 | oct15 | b | cohort30 | low | stack | low | 292.274073 | -152.052508 | 42.3764% | 57.6236% | -520.239467 |
| dollar_min | pooled | -35.292718 | oct15 | b | cohort30 | high | recommended | high | 292.274073 | -809.020437 | 3.8448% | 96.1552% | -2768.019849 |
| dollar_max | pooled | -34.390618 | oct15 | b | cohort30 | low | stack | low | 292.274073 | -152.052508 | 42.3764% | 57.6236% | -520.239467 |
| share_min | mixed_unit | -0.000000 | oct15 | b | stationary | low | stack | high | 292.274073 | -801.548178 | 1.6180% | 98.3820% | -2742.453919 |
| share_max | mixed_unit | -0.000000 | oct15 | b | stationary | low | recommended | low | 292.274073 | -242.453429 | 39.3568% | 60.6432% | -829.541349 |
| dollar_min | mixed_unit | -0.000000 | oct15 | b | stationary | high | stack | high | 292.274073 | -900.323458 | 2.6385% | 97.3615% | -3080.408218 |
| dollar_max | mixed_unit | -0.000000 | oct15 | b | stationary | low | stack | low | 292.274073 | -242.453429 | 38.9599% | 61.0401% | -829.541349 |
| share_min | person | -0.000000 | oct15 | b | stationary | low | stack | high | 292.274073 | -745.537875 | 1.9189% | 98.0811% | -2550.817683 |
| share_max | person | -0.000000 | oct15 | b | stationary | low | recommended | low | 292.274073 | -186.443126 | 45.1695% | 54.8305% | -637.905113 |
| dollar_min | person | -0.000000 | oct15 | b | stationary | high | recommended | high | 292.274073 | -844.313155 | 3.0974% | 96.9026% | -2888.771982 |
| dollar_max | person | -0.000000 | oct15 | b | stationary | low | stack | low | 292.274073 | -186.443126 | 44.3021% | 55.6979% | -637.905113 |
| share_min | pooled | -0.000000 | oct15 | b | stationary | low | stack | high | 292.274073 | -745.537875 | 1.4601% | 98.5399% | -2550.817683 |
| share_max | pooled | -0.000000 | oct15 | b | stationary | low | recommended | low | 292.274073 | -186.443126 | 39.4044% | 60.5956% | -637.905113 |
| dollar_min | pooled | -0.000000 | oct15 | b | stationary | high | stack | high | 292.274073 | -844.313155 | 2.5006% | 97.4994% | -2888.771982 |
| dollar_max | pooled | -0.000000 | oct15 | b | stationary | low | recommended | low | 292.274073 | -186.443126 | 39.4044% | 60.5956% | -637.905113 |
| share_min | mixed_unit | -34.030546 | oct15 | c | cohort10 | low | stack | high | 292.274073 | -767.517633 | 2.4578% | 97.5422% | -2626.020240 |
| share_max | mixed_unit | -34.030546 | oct15 | c | cohort10 | low | recommended | low | 292.274073 | -208.422884 | 41.5887% | 58.4113% | -713.107670 |
| dollar_min | mixed_unit | -34.279749 | oct15 | c | cohort10 | high | recommended | high | 292.274073 | -866.043709 | 4.8085% | 95.1915% | -2963.121904 |
| dollar_max | mixed_unit | -34.030546 | oct15 | c | cohort10 | low | stack | low | 292.274073 | -208.422884 | 39.2312% | 60.7688% | -713.107670 |
| share_min | person | -34.030546 | oct15 | c | cohort10 | low | stack | high | 292.274073 | -711.507329 | 3.6025% | 96.3975% | -2434.384004 |
| share_max | person | -34.030546 | oct15 | c | cohort10 | low | recommended | low | 292.274073 | -152.412580 | 42.9031% | 57.0969% | -521.471434 |
| dollar_min | person | -34.279749 | oct15 | c | cohort10 | high | recommended | high | 292.274073 | -810.033406 | 6.3134% | 93.6866% | -2771.485668 |
| dollar_max | person | -34.030546 | oct15 | c | cohort10 | low | stack | low | 292.274073 | -152.412580 | 40.8171% | 59.1829% | -521.471434 |
| share_min | pooled | -34.030546 | oct15 | c | cohort10 | low | stack | high | 292.274073 | -711.507329 | 2.3156% | 97.6844% | -2434.384004 |
| share_max | pooled | -34.030546 | oct15 | c | cohort10 | low | recommended | low | 292.274073 | -152.412580 | 41.6993% | 58.3007% | -521.471434 |
| dollar_min | pooled | -34.279749 | oct15 | c | cohort10 | high | recommended | high | 292.274073 | -810.033406 | 4.7394% | 95.2606% | -2771.485668 |
| dollar_max | pooled | -34.030546 | oct15 | c | cohort10 | low | stack | low | 292.274073 | -152.412580 | 39.3394% | 60.6606% | -521.471434 |
| share_min | mixed_unit | -34.390618 | oct15 | c | cohort30 | low | stack | high | 292.274073 | -767.157561 | 2.4597% | 97.5403% | -2624.788273 |
| share_max | mixed_unit | -34.390618 | oct15 | c | cohort30 | low | recommended | low | 292.274073 | -208.062811 | 41.6169% | 58.3831% | -711.875703 |
| dollar_min | mixed_unit | -35.292718 | oct15 | c | cohort30 | high | recommended | high | 292.274073 | -865.030740 | 4.8374% | 95.1626% | -2959.656085 |
| dollar_max | mixed_unit | -34.390618 | oct15 | c | cohort30 | low | recommended | low | 292.274073 | -208.062811 | 41.6169% | 58.3831% | -711.875703 |
| share_min | person | -34.390618 | oct15 | c | cohort30 | low | stack | high | 292.274073 | -711.147257 | 3.6291% | 96.3709% | -2433.152037 |
| share_max | person | -34.390618 | oct15 | c | cohort30 | low | recommended | low | 292.274073 | -152.052508 | 43.0094% | 56.9906% | -520.239467 |
| dollar_min | person | -35.292718 | oct15 | c | cohort30 | high | recommended | high | 292.274073 | -809.020437 | 6.4770% | 93.5230% | -2768.019849 |
| dollar_max | person | -34.390618 | oct15 | c | cohort30 | low | recommended | low | 292.274073 | -152.052508 | 43.0094% | 56.9906% | -520.239467 |
| share_min | pooled | -34.390618 | oct15 | c | cohort30 | low | stack | high | 292.274073 | -711.147257 | 2.3183% | 97.6817% | -2433.152037 |
| share_max | pooled | -34.390618 | oct15 | c | cohort30 | low | recommended | low | 292.274073 | -152.052508 | 41.7275% | 58.2725% | -520.239467 |
| dollar_min | pooled | -35.292718 | oct15 | c | cohort30 | high | recommended | high | 292.274073 | -809.020437 | 4.7692% | 95.2308% | -2768.019849 |
| dollar_max | pooled | -34.390618 | oct15 | c | cohort30 | low | recommended | low | 292.274073 | -152.052508 | 41.7275% | 58.2725% | -520.239467 |
| share_min | mixed_unit | -0.000000 | oct15 | c | stationary | low | stack | high | 292.274073 | -801.548178 | 2.0629% | 97.9371% | -2742.453919 |
| share_max | mixed_unit | -0.000000 | oct15 | c | stationary | low | recommended | low | 292.274073 | -242.453429 | 41.3455% | 58.6545% | -829.541349 |
| dollar_min | mixed_unit | -0.000000 | oct15 | c | stationary | high | stack | high | 292.274073 | -900.323458 | 3.1536% | 96.8464% | -3080.408218 |
| dollar_max | mixed_unit | -0.000000 | oct15 | c | stationary | low | recommended | low | 292.274073 | -242.453429 | 41.3455% | 58.6545% | -829.541349 |
| share_min | person | -0.000000 | oct15 | c | stationary | low | stack | high | 292.274073 | -745.537875 | 2.6708% | 97.3292% | -2550.817683 |
| share_max | person | -0.000000 | oct15 | c | stationary | low | recommended | low | 292.274073 | -186.443126 | 45.9733% | 54.0267% | -637.905113 |
| dollar_min | person | -0.000000 | oct15 | c | stationary | high | stack | high | 292.274073 | -844.313155 | 3.2348% | 96.7652% | -2888.771982 |
| dollar_max | person | -0.000000 | oct15 | c | stationary | low | recommended | low | 292.274073 | -186.443126 | 45.9733% | 54.0267% | -637.905113 |
| share_min | pooled | -0.000000 | oct15 | c | stationary | low | stack | high | 292.274073 | -745.537875 | 1.8976% | 98.1024% | -2550.817683 |
| share_max | pooled | -0.000000 | oct15 | c | stationary | low | recommended | low | 292.274073 | -186.443126 | 41.4392% | 58.5608% | -637.905113 |
| dollar_min | pooled | -0.000000 | oct15 | c | stationary | high | stack | high | 292.274073 | -844.313155 | 2.9807% | 97.0193% | -2888.771982 |
| dollar_max | pooled | -0.000000 | oct15 | c | stationary | low | recommended | low | 292.274073 | -186.443126 | 41.4392% | 58.5608% | -637.905113 |



All 44,167 retained gates pass; fiscal and social ledgers close at every end and pension set within the declared absolute bn tolerance. Inputs are checked by SHA-256 and immutable source commit; missing manifests and source drift stop the run. Conditional prevalence SEs are not newly estimated for v8. Cut files use deterministic gzip and explicit frame tags. Historical debt interest remains a separate unpriced stock object. [DATA: p7_gates.json.gz; p7_inputs.json; inputs/p8_pins_oct15.json]



```sh
sh infra/immigration-fiscal/winners_losers_2026_09_24/run_all.sh
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/winners_losers_2026_09_24 "sh {lane}/run_all.sh"
```



Would change it: measured recipient keys, a joint completion/removal counterfactual, or different explicit financing/sharing premises. Model self-report: inherited GPT-6 agent; no unverified exact served-model claim. The executed source totals and verifier receipts carry the numerical claims. [UNVERIFIED: exact model id]

2026-10-20 20:53:24 JST — Moved the live run to adopted oct16. Stationary pooled central shares ahead under a/b/c are 2.7939% / 4.7146% / 8.3071%; annual net -$505.650039bn, from `derived/oct16/p7_net_shares.csv`. All40,680 computation gates and102 tests pass. The full source ledger reproduces set $368.029739–436.561527bn and cash $284.397043–352.928831bn; generation splits close at1e-9. Historical oct15 outputs are preserved. [CALCULATION: derived/oct16/{fiscal_specs.csv,p7_net_shares.csv,p7_gates.json.gz,p7_inputs.json}]

2026-10-20 21:03:34 JST — Final full replay passed: IDENTICAL238/238, exit0;102 tests. All163 historical derived files separately match HEAD byte for byte. The static coverage declaration now names all three p9 test files; no exemption is used. A document-only replay verifies this appended receipt without rerunning unchanged scientific work. [CALCULATION: parent scratch prop9/winners-final-rerun2.log; changed-paths.txt]

## v9 case (oct16)

**Verdict:** On adopted v9, stationary financing, the paired social stack and household pooling, 2.7939% / 4.7146% / 8.3071% of other residents are ahead under rules a/b/c; their central annual net is $-505.650039bn. Cohort financing is beside. [MODEL / FRAMING-SENSITIVE; CALCULATION: derived/oct16/p7_net_shares.csv]

The complete calibrated lineage contains 44903074.08624522 people; 42951314.00418314 are placed on observed/proxy records and 1951760.08206208 remain unlocated. Native-minor calibration changes only observed member weights; the original unreported descendants retain their measured age proxy. Coverage is excluded from payer households. [DATA: derived/oct16/p7_inputs.json population; main-case meta.population_v9]

The full set/cash typed source ledger carries selected military, retirement administration, college, joint count/tenure, taxable-basket, common capital-rate and health-key components. Capital is an imputed resource cost, outside borrowing. Item19/W09 remain beside. Per-item isolated and leave-one-out ablations are not computed for v9: they need a per-item effects export for items 13-21, which does not exist. Financing and attribution scenarios are computed on oct16. [DATA: derived/oct16/p8_channel_ledger.csv; p7_trust_inputs.json; p7_net_shares.csv]

Reporter/count combined production is retained as an explicit unlocated carrier. The distribution source consumer uses assumed generation P/F shares for the same carriers; their declared difference is reconciled at1e-9 before pricing. No private-income split is inferred here. [CALCULATION: fiscal_one_definition; fiscal_specs.csv; p7_gates.json.gz]

Upstream oct16 consumers are explicit SHA256 worktree snapshots because this worker cannot commit. Every used source hash is checked before and after pricing; changes stop the run. Allocation keys and household pooling are modeled incidence, not measured winners. [DATA: inputs/p9_pins_oct16.json; derived/oct16/p7_inputs.json source_pins]

Run `sh infra/immigration-fiscal/winners_losers_2026_09_24/run_all.sh`. Explicit acquisition after reviewing upstream changes: `uv run --no-project python3 infra/immigration-fiscal/winners_losers_2026_09_24/p8_phase_b.py --prepare-pins` (use --revise-pins for an existing snapshot). Normal pricing never changes source pins.
