claude-opus-5-5

# Main case v6: v5 plus an item registry

**Verdict:** Main case v6 is v5 plus four items: **$389.08–461.48bn** (389.083 / 461.480; the ends are specifications
48 / 11 in both methods). Counting benefits when paid (the cash set), it is **$307.40–385.36bn**. Per member of the
42.75M lineage that is **$9,101–10,794** (cash set $7,190–9,014). Against v5 ($390.29–461.24bn) the set moves
−$1.21 / +0.24bn and the cash set +$0.02 / +1.95bn. Beyond the items' sum, two exact pairwise interactions add
+$0.022 / +0.043bn to the set (+0.021 / +0.029 to the cash set). Item 4 interacts with none of the other items, and there
is no three-way term.

[2026-10-07: adopted as main case v6, decision 2026-10-07-main-case-v6.md]

Item 4, user fees and the education keys, takes every part of the fee lane except transit. Alone on v5 it changes both
sets by −$0.296 / −0.726bn. That net is a +$3.87–3.97bn Pell term against service and capital terms of about
−$4.2 / −4.7bn. Under frozen services only the Pell term remains, so item 4 moves the frozen-services welfare
(`sign_reversal.csv`) by −$3.97 / −3.87bn.

The case was adopted on 2026-10-07 (`decisions/2026-10-07-main-case-v6.md`, which the parent wrote). Its payloads carry
v5's stamp form, and consumers key it `oct07`. All five gates pass:
- G1: 129 gates (109 on the case, the adopted bands pinned among them; 20 on the companion readings), plus the
  zero-item identity;
- G2: the contract;
- G3: generality;
- G4: 99 API checks, with 8 consumer gates recorded as needing code;
- G5: `rerun_lane.py` IDENTICAL 25/25, exit 0; with `lineage_addition.cjs` since 16:44, IDENTICAL 27/27, exit 0.

The companion readings that the record quotes for v5 are rebuilt on v6 (section Companion readings). The count's arms a
and c give $378.0–445.3bn and $400.2–477.7bn. C3 ± 1 SE gives $386.3–465.4bn and the count by ancestry share
$274.9–374.8bn. The school low side is $361.3–434.9bn.

v5's package needed no structural change. The item API gained two extensions:
- an optional `capital` field for item 4 (carrier receipt lines and offset capital components);
- lineage options for the companions (`caseOf`'s fourth argument, `lineage_count.cjs`).

No other lane was edited. The parent committed the lane (218a2fb2) and the decision (025203f4); the consumer lanes
pin `corrections.json`, `corrections_cash.json` and `summary.json` as committed there (For the parent).

## The items

Every item is an entry in `package.cjs` REGISTRY. Applied alone on v5, each reproduces its source lane's band to 1e-9,
with the ends at 48 / 11.

| # | Item | Kind and edits | Source (commit, arm) | Alone on v5, set | Alone on v5, cash set | In the cash set |
|---|---|---|---|---|---|---|
| 1 | `pension_tr2026`: the pension accrual on the 2026 Trustees inputs, all six, on current law's separate OASI and DI funds | edit set: 2 cell shifts (`social_security`, `medicare`), edits 752–753 | `pension_tr2026_2026_10_06` @ 8cefec37, `all_2026_inputs_separate_funds` | −2.847 / −2.674 → 387.447–458.569 | 0 | no: the cash set has the pension switch off |
| 2 | `retiree_health`: retiree health on accrual, legacy at response 0 | edit set: 10 national-scale edits (engine.js `scaleLine`), edits 754–763 (cash set 750–759) | `public_pension_legacy_2026_10_07` @ 96a8799b, `central` | +0.563 / +0.737 → 390.857–461.980 | +0.563 / +0.737 → 307.939–384.146 | yes |
| 3 | `added_age_mix`: the 3.04M added people priced at their measured age mix | lineage: v5's 336 lineage edits and production grid, re-valued in place (edits 416–751, row 8 at 751) | `added_age_mix_2026_10_07` @ 21d9a21d, keys route, 2007–26 cross-section | +1.347 / +2.857 → 391.641–464.100 | −0.265 / +1.915 → 307.111–385.325 | yes |
| 4 | `user_fees`: user fees and the education keys on the union, every part of the fee lane but transit | edit set: 5 cell shifts on the parent lines, edits 764–768 (cash set 760–764); 3 carrier receipt lines and 4 offset capital components | `user_fee_allocation_2026_10_07` @ 81bd22da, `all_but_transit` | −0.296 / −0.726 → 389.998–460.517 | −0.296 / −0.726 → 307.080–382.683 | yes |

Item 3 applied alone matches the lane's central bands to within 1.7e-13. The lane stores only its ends
(`price_bands.csv`), so the check at all 64 specifications is against the lane's part models rerun here from
`price.cjs`'s functions. Those add to the consumer's change to within 3.3e-13 (set) and 2.9e-13 (cash set).

The parent's message gave item 2 as +0.565. That is the lane's line table, a sum of rounded lines. Its band change is
+0.563 (`case_oct05.json` `band_change_bn` 0.56310 / 0.73667).

**Parts at the end specifications** (low / high, $bn; `summary.json` `change_at_fixed_specifications.items`):

- `pension_tr2026`. On v5's added people the parts are:
  - union_oasdi −2.261 / −2.123 and union_part_a −0.354 / −0.354;
  - lineage_oasdi −0.199 / −0.168 and lineage_part_a −0.033 / −0.028.

  The union parts are (ratio_net 0.95355 − 0.97367) × the union's OASDI receipts, and Part A at 40.783 − 41.137. The
  lineage parts are (f − 1) × the added people's accrual, with f_ss 0.97923 and f_pa 0.99014 (G3+'s factors).
- `retiree_health`, by line:

  | Line | Change |
  |---|---|
  | other_federal_benefits (military retirees' civilian care set to zero) | −0.989 / −0.915 |
  | education_services | +0.891 / +0.928 |
  | public_order_safety | +0.294 |
  | health_services | +0.112 |
  | general_public_services | +0.088 / +0.125 |
  | income_security_services | +0.085 / +0.079 |
  | economic_affairs_services | +0.041 / +0.067 |
  | housing_community_services | +0.027 |
  | recreation_culture | +0.016 / +0.019 |
  | defense (response 0) | 0 |
  | the capital return | −0.0001 / +0.0002 |

  The change splits into the union's +0.536 / +0.683 and the added people's +0.028 / +0.053. The national change
  is −$6.257bn.
- `added_age_mix`:
  - set: G3-rate persons +0.123 / +0.333 and later losses +1.224 / +2.524;
  - by member: G3+ members +1.119 / +2.611 and whites +0.228 / +0.246;
  - cash set: G3-rate −0.722 / −0.584 and later +0.456 / +2.499.
- `user_fees` (the same on both sets; low is specification 48, shared, and high is 11, personal). The parts carry
  `meta.items`' names, `union_<term>`:

  | Part | Line it edits | Change |
  |---|---|---|
  | union_fee_tuition | education_services | +1.845 / +1.845 |
  | union_key_higher_ed | education_services | −5.452 / −5.452 |
  | union_fee_health | health_services | +0.945 / +0.945 |
  | union_key_health | health_services | −0.304 / −0.304 |
  | union_key_pell | other_federal_benefits | +3.868 / +3.969 |
  | union_k12_weight_school (A + B) | school_reprice | −0.435 / −0.645 |
  | union_k12_weight_other (A) | college_rekey | −0.135 / −0.082 |
  | union_capital_k12 (K-12 stock at its own key) | offset `k12_user_fees` | +0.276 / +0.507 |
  | union_capital_college (college stock at use) | offset `college_user_fees` | −0.904 / −1.509 |
  | union_capital_health_sl, union_capital_health_fed (health stocks kept at v5's keys) | offsets `health_sl_user_fees`, `health_fed_user_fees` | 0 / 0 |
  | **total** | | **−0.296 / −0.726** |

## Item 4: what it takes and how it is folded

**Taken** from `user_fee_allocation_2026_10_07` @ 81bd22da: the engine lines fee_tuition, key_higher_ed, fee_health,
key_health and key_pell. The lane gates that each parent line responds at 1 at all 64 specifications. Also taken are
the post-engine terms k12_weight_bn (BEA's K-12 weight 0.7748 in place of 0.795), capital_college_bn and
capital_k12_bn.

**Left out:** key_transit (−1.981 / −1.981) and capital_transit_bn (−0.300 / −0.451). v3's item 8 tested the same
object at the same ACS ratio. Weighted by where the deficit falls, the riders' key is 1.019 times the population key, and
v4 kept it beside (`decisions/2026-09-29-main-case-v4.md`, rejected 4). This is recorded in `meta.user_fees.excluded`.

**Gate (a).** The brief's rule, recomputed from `case_oct05.json`, is sum(lines_bn without key_transit) + k12_weight_bn
+ capital_college_bn + capital_k12_bn. It gives **−0.296058 (specification 48, shared) / −0.726064 (11, personal)**,
and item 4 alone on v5 gives the same on both sets to 1e-6. Specifications 48 and 11 stay the lowest and highest
costs. At all 64 specifications the item matches the lane's `case_oct05.csv` less its transit columns to 1e-9. The
brief printed −0.296104 / −0.726103. I could not reproduce those from the file; they differ by 4.6e-5 / 3.9e-5bn.

**The fold.** The amounts are folded into the parent lines, as the parent preferred, so by-line consumers need no new
synthetic lines.
- **Edits.** There are five cell shifts, in order:
  - education_services (key education_mix) by fee_tuition + key_higher_ed;
  - school_reprice by A + B and college_rekey by A;
  - health_services (key health_other) by fee_health + key_health;
  - other_federal_benefits (key all_cash) by key_pell.
- **The K-12 weight.** Edits 2 and 3 are audit row 6's re-blend at w_K = 0.7748343991 in place of W = 0.795, gated
  against the lane's A and B (1e-9). At the case's school response of 1, (A + B) s r + A (1 − s) = A + B s, the lane's
  term (gated 1e-12). The lane's arms for the weight (sl_mix, federal_k12, federal_non_k12) are recorded in
  `meta.user_fees.k12_weight.arms_not_wired`, not wired.
- **The capital re-keys.** The engine keys capital by line amounts, so the education edits would move the K-12 and
  college keys by their own dollars. Four offset components cancel that move and put the lane's re-key in its place:
  - Each offset copies its target's part, level, stock and response, names it in `of_component`, and is keyed
    `receipt_amount_over_national` on a carrier receipt line (`user_fees_key_k12`, `user_fees_key_college`,
    `user_fees_key_health`).
  - A carrier's value is v = (key_target − key_union) − (the item's edits on the key's numerator lines) / the
    denominator's national total, on the model the item applies to.
  - The health targets keep v5's keys, so key_target − key_union is 0 for them.
  - Carriers respond at 0 and add under $1 (national 1e-9bn). Each re-key is exact (1e-12).

Capital at the end specifications on v6 ($bn):

| Target | Its return | Offset | Together |
|---|---|---|---|
| k12 | 9.231 / 14.441 | +0.463 / +0.797 | 9.694 / 15.238 |
| college | 3.956 / 6.189 | −0.824 / −1.386 | 3.132 / 4.803 |
| health_sl | 0.459 / 0.689 | −0.015 / −0.023 | 0.444 / 0.666 |
| health_fed | 0.133 / 0.200 | −0.004 / −0.007 | 0.129 / 0.193 |

**Why item 4 has no interaction.** Its edits are fixed amounts on the union. Its carriers are computed on whatever model
it applies to, so they cancel its own move of the capital keys at that model's nationals. Item 3 changes the lineage's
education amounts, and with them the capital keys' lineage part. The carriers do not read the lineage's amounts, and
item 3 leaves the nationals as they are, so the pair is 0. Item 2 moves the education and health nationals, but the
cancellation holds at any nationals. All three pairs are 0 to 1.1e-13.

**Limits** (`summary.json` `v6.user_fees`):
- **Union-only.** The 3.04M added people keep their v5 and item 3 pricing. At the union's per-member terms they would
  add −0.023 / −0.056 (the lineage scale is 1.0765). This is not counted, and the rule is in
  `meta.user_fees.union_only`.
- **[APPROX] Item 2's line totals are not carried into item 4's key terms.** The amounts are the lane's on v5's line
  totals. Item 2 raises education by 0.43% and health by 0.59%, and key_higher_ed, the K-12 weight and key_health are
  shares of those lines' dollars. Carrying the move would add −0.028 / −0.028. The fee terms and Pell are dollars of
  their own and would not move.
- **The school low side.** The fold makes the education terms respond at the education line's response. The lane's form
  holds its engine lines at 1 and writes (A + B s)(s r + 1 − s). At the case's school response of 1 the two agree.
  Below 1 they differ:

  | School rule (response) | v5 | v5 + item 4, folded | v5 + item 4, lane's form | Folded − lane's form |
  |---|---|---|---|---|
  | within_district (0.8489) | 362.266 / 434.649 | 362.459 / 434.337 | 361.985 / 433.943 | +0.474 / +0.394 |
  | within_district_as_response (0.836) | 359.806 / 432.456 | 360.043 / 432.178 | 359.528 / 431.750 | +0.514 / +0.428 |

  On v6 the within-district row is 361.26 / 434.91 with the fold and about 360.78 / 434.52 in the lane's form. Both
  round to $361–435bn.

## Items 1–4 jointly

| $bn, low / high | Set | Cash set |
|---|---|---|
| v5 | 390.294 / 461.243 | 307.376 / 383.409 |
| sum of the items alone | −1.233 / +0.194 | +0.002 / +1.926 |
| pension_tr2026 × retiree_health | 0 / 0 | 0 / 0 |
| pension_tr2026 × added_age_mix | +0.001 / +0.014 | 0 |
| retiree_health × added_age_mix | +0.021 / +0.029 | +0.021 / +0.029 |
| user_fees × each of the other three | 0 (max 1.1e-13) | 0 |
| three-way remainder | 0 | 0 |
| **v6 − v5** | **−1.211 / +0.237** | **+0.023 / +1.955** |
| **v6** | **389.083 / 461.480** | **307.399 / 385.364** |
| per member of 42,752,213 | $9,101 / 10,794 | $7,190 / 9,014 |

**Each item's marginal.** Taken at specifications 48 / 11, an item's marginal is v6 less v6 without that item: its
change alone plus its pairs. The marginals do not add to v6 − v5, because each pair appears in two of them.

| Item | Alone on v5, set | Marginal on v6, set | Alone on v5, cash set | Marginal on v6, cash set |
|---|---|---|---|---|
| pension_tr2026 | −2.847 / −2.674 | −2.846 / −2.660 | 0 | 0 |
| retiree_health | +0.563 / +0.737 | +0.584 / +0.766 | +0.563 / +0.737 | +0.584 / +0.766 |
| added_age_mix | +1.347 / +2.857 | +1.368 / +2.900 | −0.265 / +1.915 | −0.244 / +1.944 |
| user_fees | −0.296 / −0.726 | −0.296 / −0.726 | −0.296 / −0.726 | −0.296 / −0.726 |

The two nonzero interactions are mechanical, and both are gated exactly:

- **pension_tr2026 × added_age_mix.** Item 1's lineage parts are (f − 1) × the added people's Social Security and Part
  A. The age mix moves those amounts.
- **retiree_health × added_age_mix.** Item 2 scales every cell of its lines, the added people's included.
- **pension_tr2026 × retiree_health** is 0: the two edit different lines, and no capital key reads Social Security or
  Medicare.

At every one of the 64 specifications the case moves from v5 by personal +0.236 / +0.490 and shared −1.479 / −1.211.
The ends do not move.

The rest of v5's figures move by the items too:

| Row | v6, $bn |
|---|---|
| without the capital return | 352.50 / 400.42 |
| general government at 0 | 356.38 / 413.59 |
| option A (beside) | 372.32 / 438.65 |
| 7% capital return (beside) | 480.54 / 542.90 |
| school low side, within-district (0.8489) | 361.26 / 434.91 |
| school low side, within-district as the response (0.836) | 358.82 / 432.72 |
| K-12 capital at the pupil share | 388.91 / 460.53 |
| range | 311.89–515.60 (quadrature 353.57–483.99) |
| the frozen-services welfare (CBO preferred) | −83.64 / +27.52 |
| the personal break-even (`sign_reversal.csv`) | −9.05% / −0.66% |

For the frozen-services welfare and the personal break-even:
- v5 is −82.72 / +28.20 and −8.76% / −0.37%;
- the three-item candidate was −79.67 / +31.39 and −8.06% / +0.27%.

Item 4 moves the frozen-services welfare by −3.969 / −3.868, which is −key_pell at the personal and shared allocations.
With services frozen and capital fixed, its service and capital terms drop out and the Pell transfer stays.

## Arms

Each arm row in `main_case_bands.csv` is the whole v6 case with that item at the arm (`caseOf(OCT05, ids, {item: arm})`).
Each is gated in two ways:
- on its payload, consumer.cjs gives the row's band, with the ends at 48 / 11;
- the arm alone on v5 is the source lane's band (1e-9), for the set and for the cash set.

Item 4 has no arm: transit is left out, not carried as an arm.

| Arm row | Set | From the case | Cash set | Alone on v5, set |
|---|---|---|---|---|
| `pension_tr2026_combined_funds` (the 2026 inputs on combined OASDI funds, `all_2026_inputs`) | 390.203 / 462.520 | +1.121 / +1.040 | the case's | 388.568 / 459.614 |
| `retiree_health_mu_low` (μ 1.326) | 388.716 / 461.094 | −0.366 / −0.386 | 307.033 / 384.978 | 390.492 / 461.596 |
| `retiree_health_mu_high` (μ 2.300) | 389.449 / 461.866 | +0.366 / +0.386 | 307.766 / 385.750 | 391.222 / 462.363 |
| `retiree_health_rho_one` (ρ = 1, accrual = pay-go) | 387.719 / 460.042 | −1.364 / −1.438 | 306.036 / 383.926 | 389.498 / 460.551 |
| `retiree_health_rho_high` (ρ 1.506) | 391.177 / 463.689 | +2.095 / +2.209 | 309.494 / 387.573 | 392.945 / 464.174 |
| `retiree_health_military_low` ($9.7bn) | 389.578 / 461.936 | +0.496 / +0.456 | 307.895 / 385.820 | 391.362 / 462.446 |
| `retiree_health_military_high` ($22.4bn) | 388.955 / 461.362 | −0.128 / −0.118 | 307.272 / 385.247 | 390.727 / 461.860 |
| `retiree_health_no_federal` | 389.862 / 462.152 | +0.779 / +0.672 | 308.179 / 386.037 | 391.653 / 462.672 |
| `added_age_mix_cohort_at_birth` | 383.514 / 452.025 | −5.569 / −9.454 | 304.764 / 376.736 | 386.171 / 454.806 (v5 −4.12 / −6.44) |
| `added_age_mix_rough_keys` | 390.132 / 461.315 | +1.049 / −0.165 | 309.171 / 385.153 | 392.658 / 463.932 |
| `oct05_case`, `oct05_cash_set` (history: v5) | 390.294 / 461.243 | | 307.376 / 383.409 | |

The cohort reading moves the case by more than it moves v5 (−5.57 / −9.45 against −4.12 / −6.44). The arm replaces the
central age mix, so its row also gives up the central reading's +1.35 / +2.86.

## Companion readings

The record quotes five readings beside v5's case (CLAUDE.md's headline list, FAQ 19). Each is rebuilt on v6 as a
whole-case row in `main_case_bands.csv`, with a cash row wherever v5 has one, and `summary.json` `v6.companions` holds
the detail. None is left unbuilt.

| Reading ($bn, low / high) | v5 | v6, set | v6, cash set | v6 per member, set |
|---|---|---|---|---|
| The count's arm a, 1.81M added (`lineage_arm_a`) | 380.374 / 447.551 | 378.000 / 445.254 | 299.820 / 371.116 | $9,104 / 10,724 (41.52M) |
| The count's arm c, 4.27M added (`lineage_arm_c`) | 400.206 / 474.928 | 400.158 / 477.698 | 314.972 / 399.605 | $9,098 / 10,860 (43.98M) |
| C3 − 1 SE, 0.3110 (`lineage_c3_minus_se`) | 393.289 / 465.190 | 391.912 / 465.373 | 309.979 / 389.300 | $9,167 / 10,885 (42.75M) |
| C3 + 1 SE, 0.8024 (`lineage_c3_plus_se`) | 387.299 / 457.296 | 386.253 / 457.586 | 304.820 / 381.428 | $9,035 / 10,703 (42.75M) |
| C3 ± 1 SE, the outer span | 387.299 / 465.190 | 386.253 / 465.373 | 304.820 / 389.300 | |
| Ancestry share, G4+ at nothing (`ancestry_share_g4_at_nothing`; ends 16 / 43) | 275.390 / 322.127 | 274.874 / 320.835 | 219.833 / 268.184 | $9,194 / 10,731 (29.90M) |
| Ancestry share, G4+ at its bound (`ancestry_share_g4_at_bound`) | 326.681 / 375.813 | 325.196 / 374.793 | 261.064 / 311.877 | $9,268 / 10,681 (35.09M) |
| Ancestry share, the outer span | 275.390 / 375.813 | 274.874 / 374.793 | 219.833 / 311.877 | |
| School low side, within-district b 0.836 (`school_within_district`) | 362.266 / 434.649 | 361.258 / 434.909 | none (set only, as v5) | |

Printed, v6 against v5:
- arms a and c: $378.0–445.3bn and $400.2–477.7bn (v5 $380.4–447.6bn and $400.2–474.9bn);
- C3 ± 1 SE: $386.3–465.4bn (v5 $387.3–465.2bn);
- the count by ancestry share: $274.9–374.8bn (v5 $275.4–375.8bn); the cash set's is $219.8–311.9bn;
- the school low side: $361.3–434.9bn (v5 $362.3–434.6bn, printed $362–435bn).

**How the count and C3 rows are built.** They are lineage options: `caseOf(OCT05, CANDIDATE, {}, name)`, with names
`arm_a`, `arm_c`, `c3_minus_se` and `c3_plus_se`.
- `lineage_count.cjs` builds the lineage's addition at the option by the lineage lane's own route
  (`lineage_case.cjs` at d3b7e6e6: `augmented()`, `payloadFor()` and `responsesAt()`, ported with their gates).
- At v5's arm and C3 the port rebuilds v5's addition byte for byte, gated on every build.
- At arms a and c the count moves the group's share s. The 19 group-size responses move with it, as do row 8's edit
  (−0.0047 and −0.0112bn against v5's −0.0080) and the long-run capital values. C3 does not move s.
- Item 3 is rebuilt on the option's addition. Items 1, 2 and 4 rebuild on that base, as they do on item 3's.
- Each option's payload is a variant: adopted null, `meta.lineage.count_option`, payload null.

The gates:
- With no item, each option reproduces the lineage lane's stored v5 value at 1e-9, set and cash, with ends 48 / 11. For
  arms a and c that value is the arm's band. For the C3 options it is arm b's C3 line at the option's C3.
- Each row is consumer.cjs's band on its payload (1e-9), with ends 48 / 11 in both methods.

Each row's change from v6 splits into two parts: the option's own change on v5, and how much more or less the items
move the case there than at the case.

| Option | Row − v6, set | The option on v5 | The items at the option | The items at the case |
|---|---|---|---|---|
| arm_a | −11.082 / −16.226 | −9.920 / −13.692 | −2.374 / −2.297 | −1.211 / +0.237 |
| arm_c | +11.075 / +16.218 | +9.912 / +13.684 | −0.048 / +2.770 | −1.211 / +0.237 |
| c3_minus_se | +2.830 / +3.894 | +2.995 / +3.947 | −1.377 / +0.183 | −1.211 / +0.237 |
| c3_plus_se | −2.830 / −3.894 | −2.995 / −3.947 | −1.046 / +0.290 | −1.211 / +0.237 |

**How item 3 enters these rows [ASSUMPTION].** The age-mix lane priced arm b only. At each option the two count parts
keep the mixes it measured on arm b's counts: the G3-rate persons take the G3-rate mix and the later losses the
later-loss mix, at the option's counts and C3.

Item 3's size at each option is the case there less the case there without item 3. It is largest where later losses
are largest:

| Option | Item 3, set | Item 3, cash set |
|---|---|---|
| the case (its marginal) | +1.368 / +2.900 | −0.244 / +1.944 |
| arm_a (no later losses) | +0.119 / +0.315 | −0.662 / −0.533 |
| arm_c (2.19M later losses) | +2.618 / +5.486 | +0.175 / +4.422 |
| c3_minus_se | +1.209 / +2.839 | −0.324 / +1.923 |
| c3_plus_se | +1.528 / +2.961 | −0.164 / +1.966 |

Arm c's later losses reach past the fourth generation through compounding. The lane did not measure those
generations' ages.

**How the ancestry-share rows are built** (`ancestry_share.cjs`). The lineage lane's fractional count runs on v6. At each
specification f = G1 + s_G2 G2 + s_G3+ G3+ + s_added × added, and the band is f's minimum and maximum over the 64. The
shares are those in `fractional_shares.json`: s_G2 0.9248, s_G3+ 0.3046 (G4+ at nothing) or 0.6665 (at its bound), and
s_added 0.4075.
- Each union generation is the generation account's corrected model (convention a), with its part of row 8's edit and
  of the items.
- The added people are the case less the three generations.
- Item 3 enters through the added people's cost, at s_added. It adds +1.168 / +0.558 (G4+ at nothing) and
  +0.558 / +1.182 (at its bound) to the set.
- **[ASSUMPTION] The items' union parts split by generation** by the rule G4 pattern 3 checks:
  - item 1's union parts by each generation's share of the union's OASDI receipts and Part A accrual;
  - item 4's parts and carriers by their split-basis line's union amount (`meta.user_fees.splits`): the education
    line for the higher-education parts, Pell and the K-12 weight's parts, the health line for the health parts;
  - item 2's national-scale edits as they are.

  Splitting Pell instead on the line it is folded into, other federal benefits (keyed by cash assistance), moves the
  rows by +0.161 / −0.244 (G4+ at nothing) and −0.099 / +0.111 (at its bound), the same in both sets.

  Splitting item 1's union parts instead by the pension lane's measured per-generation changes
  (`pension_tr2026_2026_10_06/derived/arms.csv`) moves the rows by +0.012 / −0.126 (G4+ at nothing) and −0.049 / +0.016
  (at its bound). Under the measured split G1 takes 22.7% of the OASDI part, against 22.6% (shared) and 28.8% (personal) under the
  rule.
- **Gates.** On v5 (no item) the count reproduces the lineage lane's four rows exactly: set and cash, both scenarios,
  with their ends and fractional populations. The generations with their parts add to the union, with the same edits,
  at all 64 specifications (1e-9).
- The scenarios' ends stay at 16 / 43 (G4+ at nothing) and 48 / 11 (at its bound), as on v5.

**The school low side** is the existing row `school_within_district`. Its within-district elasticity is 0.836, which
gives a response of 0.8489 at the group's share. It is set only, as on v5.

## The lineage's addition, by part

`lineage_addition.cjs` splits the 3.04M added people's cost and the lineage's addition at the case's end
specifications (48 low, 11 high; each figure the two methods' mean). The record's figures on the added people (FAQ
entry 19, the INDEX, the complete account) come from it. It reads the package and writes only
`derived/lineage_addition.json`, so no payload or band file moves. The parts come from the package's case at lineage
options that `lineage_count.cjs` builds (`additionsAt`). With the responses fixed the cost is affine in the counts
(gated at twice the later losses), so each count part is the case less the case without those people, and the
union-only case is the intercept at the union's own responses (v4's share and metro factor). 41 gates pass. Among them:
with no item the route gives v5's stored figures and its published $8,541 / 11,731, $5,052 / 7,133, +$18.9 / +26.4bn,
$6,309–8,790 and $9,353–10,950, and the union-only case is the September 29 case; with every item it gives the adopted
band to six decimals; item 4 leaves the added people's parts unchanged.

| $bn a year, low / high | persons | set | per person, set | cash set | per person, cash |
|---|---:|---:|---:|---:|---:|
| later losses, priced as identified third-plus members of the same ages | 1,094,828 | 10.513 / 15.360 | $9,603 / 14,030 | 7.322 / 13.657 | $6,688 / 12,474 |
| G3-rate attriters, (1 − C3) × G3+ + C3 × white | 1,944,892 | 9.829 / 14.115 | $5,054 / 7,257 | 5.435 / 10.248 | $2,795 / 5,269 |
| all added people | 3,039,720 | 20.342 / 29.475 | $6,692 / 9,696 | 12.757 / 23.905 | $4,197 / 7,864 |
| the union's response to the larger group | | −0.298 / −0.316 | | −0.298 / −0.316 | |
| the lineage's addition | | 20.044 / 29.159 | | 12.459 / 23.589 | |
| the union-only case (39.71M) | 39,712,493 | 369.039 / 432.321 | $9,293 / 10,886 | 294.940 / 361.775 | $7,427 / 9,110 |
| v6, the case (42.75M) | 42,752,213 | 389.083 / 461.480 | $9,101 / 10,794 | 307.399 / 385.364 | $7,190 / 9,014 |

The high end's union response, −0.3154, prints as −0.316 so the printed parts add. On v5 the added people cost $8,541 /
11,731, $5,052 / 7,133 and $6,309 / 8,790 a person, the addition was +18.879 / +26.402 and the union-only case $9,353 /
10,950 per member. The items add $1.164 / 2.757bn to the added people on the set, almost all of it to the later losses
(+$1.162 / 2.516bn): item 3 prices them at their measured ages. An added person costs less than an identified member,
so the cost per member of the 42.75M is below the union-only case's.

## The payloads

- **`derived/corrections.json`** has 769 edits:
  - 416 are the September 29 payload's;
  - 336 are the lineage's (item 3's values in v5's cells and order, with v5's row 8 edit last, edits 416–751);
  - 2 are item 1's (752–753), 10 are item 2's (754–763) and 5 are item 4's (764–768).

  It also carries:
  - `receipt_lines`: v5's two (housing_enterprise_surplus, tenant_occupied_property), then item 4's three carriers;
  - `meta.capital_return.components`: v5's 24, then item 4's 4 offsets (`k12_user_fees`, `college_user_fees`,
    `health_sl_user_fees`, `health_fed_user_fees`).
- **`derived/corrections_cash.json`** has 765 edits: 414 + 336 + item 2's 10 (750–759) + item 4's 5 (760–764). It has
  the same carriers and offsets.
- **`meta.items`** gives each item's id, kind, source, arm and applied flag. An edit set also gets its edits
  `{first, count}` and its parts; the lineage item gets `lineage_edits`. In the cash set, item 1 is `applied: false`,
  with its reason. Item 4's entry adds:
  - `capital`: its `receipt_lines` and `components`, the `carrier_values` on the model at its step, and the rule;
  - `union_only: true`, with `union_only_rule`, so consumers can route it as union-only;
  - parts named `union_<term>`, as item 1's union parts are. Each names its edit, line and key and the lane's term:
    union_fee_tuition, union_key_higher_ed, union_k12_weight_school, union_k12_weight_other, union_fee_health,
    union_key_health and union_key_pell;
  - `parent_lines`: the lines the amounts are folded into, each with its key and parts:
    - education_services (education_mix): union_fee_tuition and union_key_higher_ed;
    - school_reprice (k): union_k12_weight_school;
    - college_rekey (k): union_k12_weight_other;
    - health_services (health_other): union_fee_health and union_key_health;
    - other_federal_benefits (all_cash): union_key_pell;
  - `capital_components`: each target component's offset, carrier, parent line and part:
    - k12 → `k12_user_fees`, carrier `user_fees_key_k12`, education_services, re-keyed, union_capital_k12;
    - college → `college_user_fees`, carrier `user_fees_key_college`, education_services, re-keyed,
      union_capital_college;
    - health_sl and health_fed → `health_sl_user_fees` and `health_fed_user_fees`, carrier `user_fees_key_health`,
      health_services, not re-keyed, union_capital_health_sl and union_capital_health_fed;
  - its rule, parts_rule, split_rule, carriers and offsets;
  - source_band_bn and source_change_bn.

  The carrier values in key units, personal / shared, are:
  - k12: 0.0097530 / 0.0084974;
  - college: −0.0385486 / −0.0343686;
  - health: −0.0020799 for both.
- **`meta.pension_accrual`** (set only) holds the arm's values:
  - ratio_net 0.95355 and part_a_accrual_bn 40.783;
  - the lineage factors f_ss 0.97923 and f_pa 0.99014;
  - `source`: `pension_tr2026_2026_10_06/derived/summary.json` @ 8cefec37, arm `all_2026_inputs_separate_funds`, with
    its sha256 and the case file's; `builds_on` keeps the 2025 lane's pin (9ea1beb);
  - `paths`: TR 2026, MTR 2026, Note 2026.3 and the separate funds;
  - `previous.oct05`: v5's values;
  - `arms.combined_funds`: ratio_net 0.96280 and f_ss 0.98764.

  The scheduled-benefits arm is stamped as still on the 2025 reports.
- **`meta.retiree_health`** (both payloads):
  - the rule and the arm (`central`);
  - the inputs: μ 1.8129, ρ 1.1995, military retirees' purchased care $19.80bn, Pew FY2019, the Financial Report FY2024
    and MERHCF;
  - the national change by line (−6.257bn) and the documents;
  - the source hashes, and the lane @ 96a8799b with each file's sha256;
  - `beside`: the school-key reading, not wired;
  - the other arms' national changes.
- **`meta.user_fees`** (both payloads):
  - rule, edits and engine_lines;
  - `k12_weight`: w_K, W, A and B per allocation, and the arms not wired;
  - `capital`: key_target, key_union and the change for each re-key; the carriers with their parent lines; the carrier
    rule and the options rule;
  - `excluded`: the transit terms, why, and the lane's values at the ends;
  - `union_only`: the lineage scale and added_people_at_union_terms_bn;
  - `splits`: generation, household_person, basis_rule and split_basis. Each part splits on its parent line except
    Pell and the K-12 weight's two parts, which split on the education line (the decision's rule, `basis_rule`).
    [ASSUMPTION] Pell goes to students. Its parent line, other federal benefits, is keyed by adult cash assistance
    (all_cash) and would put it on cash recipients, and no consumer lane has a college-enrollment key by person or
    generation. The fold into other federal benefits' cells is unchanged;
  - school_response and lane_change_at_ends_bn;
  - `source`: the lane, the commit and each file's sha256.
- **`meta.lineage`** is v5's but for two keys:
  - `payload` now points to this lane's `derived/lineage_payload.json` and `lineage_payload_cash.json`;
  - `age_mix` is added. It holds the measurement (the basic monthly CPS 1994–2026), the reading (2007–26
    cross-section), the route (keys) and the source lane and commit with file hashes. Its under-20 shares are 45.4% of
    G3-rate persons and 61.5% of later losses, against 46.7% of the identified third-plus.

  Counts, members and responses are v5's. At a lineage option, meta.lineage carries the option's counts, C3 and s,
  `count_option`, and `payload` null.
- **Stamps** (v5's form, `adopted_2026_10_05`):
  - source `main_case_2026_10_07/package.cjs`, adopted `2026-10-07`, decision `decisions/2026-10-07-main-case-v6.md`;
  - status `adopted 2026-10-07 (decisions/2026-10-07-main-case-v6.md): v5 plus items pension_tr2026, retiree_health,
    added_age_mix, user_fees, built by main_case_2026_10_07/package.cjs on main_case_2026_10_05/derived/corrections.json`;
  - the cash set's status `the cash set of the case adopted 2026-10-07 (the pension switch off):
    main_case_2026_10_05/derived/corrections_cash.json plus items retiree_health, added_age_mix, user_fees, built by
    main_case_2026_10_07/package.cjs`;
  - `case`: v5's text, then `; v6, adopted 2026-10-07: ` and each item.

  Every other combination is a variant: an arm, fewer items or a lineage option. A variant has adopted null, a status
  beginning `variant: ` and case text naming it a variant of v6.

## The item mechanism

An item is `{id, kind, label, source, cash: {applies, why}, arms, build}`. Adding one is a REGISTRY entry plus a
builder; nothing else changes. There are two kinds:

- **`edit_set`.** `build(ctx, arm, which)` returns:
  - `edits`: cell shifts or national-scale edits, appended after the lineage's;
  - `editsAt(m)`, optional: edits as a function of the model. Item 2 uses it, so an option that moves a line's
    total keeps the item's rule;
  - `parts`: named parts that add to the cell shifts exactly;
  - `meta`: keys outside `RESERVED_META`;
  - `record`;
  - `capital`, optional (item 4): `carriers`, `receiptLinesAt(m)`, `zeroLines(m)`, `componentsFor(comps, caseComps)`,
    `checkEvaluation(ev)` and `offsets`.

  `cash.applies` decides whether the builder also runs for the cash set.

  The package keeps the case's national totals at each step. It stops on an option that moves the national total of a
  line that a fixed-amount item (items 1 and 4) edits.

  With a `capital` field, `forItems` overrides the base API:
  - `withSyntheticLines` adds the carriers at zero;
  - `componentsFor` appends the offsets;
  - `capitalReturn` and `evaluateFull` add the offsets' return;
  - viaCandidate, cost, bandFor, band, evalPackage and central route through these.

  `withItems()` replaces zero carriers with their values on the model. It stops when the carriers already carry
  amounts, so the item cannot be applied twice. `checkBuilt` dry-runs the carriers and offsets through
  `applyCorrections`. `checkEvaluation` stops when an evaluation keys an edited line by another key.
- **`lineage`.** `build(ctx, arm)` returns the lineage's additions for both sets, in the lineage lane's format, plus
  `lineage_meta`. `checkLineage` gates them: v5's cells in v5's order, v5's row 8 edit, the grid's dimensions and SEs,
  and v5's counts, responses and capital values. At a lineage option it checks against the option's row 8 edit,
  counts, responses and capital values instead. `rebase()` then builds the base with v5's own `merge`, `adoptLineage`
  and `forCase` on the September 29 payloads, and the edit sets rebuild on that base. One lineage item at a time.

Arms are options: `caseOf(base, ids, {id: arm})` is the whole case at the arm. `caseOf(OCT05, [])` is v5, byte for
byte.

Lineage options: `caseOf(base, ids, arms, name)` is the whole case with the lineage at another arm of the count or
another C3. The names are in `LINEAGE_OPTIONS`: arm_a, arm_c, c3_minus_se and c3_plus_se.
- `lineage_count.cjs` builds the option's addition by the lineage lane's route.
- With the lineage item, item 3 adds its deltas to that addition. Without it, the option's addition is the base's
  lineage.
- The edit sets rebuild on that base.
- Every option is a variant. A new option is an `OPTIONS` entry naming a `population.json` arm or a C3 offset in SEs.

**Slots** (`SLOTS` in package.cjs; described, not implemented):

- **`lineage_count`**: a count that `population.json` does not hold, such as the VHB fourth-plus arm (ladder 287).
  Since 2026-10-07, `population.json`'s arms and other C3 values are lineage options. A new count needs:
  - the count as a `population.json` arm (added, g3_rate, later, population, s, k_metro), from which
    `lineage_count.cjs` builds the addition at its responses;
  - the age mix of its parts where it is not arm b's (the options take arm b's mixes);
  - the per-member divisor, `meta.lineage.counts` and the consumers' lineage splits taken from the new base, as for the
    options.
- **`split_line`**: an item that puts a legacy part of a service line at zero response. It needs:
  - a payload line for the zero part, with paired shifts so national totals hold;
  - a `meta.responses` entry at 0 for that line at both readings, read by consumer.cjs and by `line_responses`;
  - the base package to accept lines and responses beyond v4's (`forCase` stops on both today), with
    `withSyntheticLines`, `PAYLOAD_LINES` and `PARENT` carrying the new line;
  - the lineage's edits on the parent split by the same share;
  - the capital keys that read the parent re-keyed or stated.

## Gates

- **G1** (`main_case.cjs`, 129 gates, all pass: 109 on the case and 20 on the companion readings).
  - v5 re-derives. The band is v5 plus consumer.cjs's change at all 64 specifications (1e-9).
  - The adopted bands are the ones the consumer lanes pinned at adoption, to the sixth decimal: the set 389.082553 /
    461.479709 and the cash set 307.399411 / 385.364123. Moving them takes a new case.
  - Both methods find the ends at 48 / 11, in the set and the cash set: b_hotdeck 384.968 / 458.602 and
    b_matched_over_pooled 393.197 / 464.357.
  - Each item alone matches its source lane (1e-9). Item 2 alone is the lane's own route exactly, on both sets. Item 3
    alone matches the lane at all 64 specifications through the lane's part models. At the ends it gives the lane's
    change and parts.
  - Item 4 alone matches the lane's `case_oct05.csv` less transit at all 64 specifications (1e-9). The other item 4
    gates:
    - gate (a) at 1e-6, with 48 / 11 as the lowest and highest;
    - the K-12 weight fold (1e-12);
    - the carriers at response 0 and under $1, and each re-key exact (1e-12);
    - every pair with item 4 at 0 (1e-9).
  - The payload models are model.json plus the September 29 payloads, the lineage addition, the edit sets and the
    carriers, exactly.
  - The interactions, the parts and the arms are gated as described above. Parts with capital add to the change.
  - The companion readings (section Companion readings) have 20 gates:
    - each lineage option with no item is the lineage lane's stored v5 value, set and cash (8);
    - each option's case is consumer.cjs's band on its payload, a variant, with ends 48 / 11 (8);
    - the count by ancestry share on v5 is the lineage lane's rows (4).
  - The identity (`zero_items.cjs`): with `--items none`, `main_case.cjs` (54 gates) and `sign_reversal.cjs` (15 gates)
    write v5's seven files byte for byte.
- **G2** (`contract.cjs`). Every v5 file, column, row and key is present. The additions are listed:
  - 33 band rows, 12 of them the companion readings;
  - 10 `per_spec.csv` columns, the four offset columns last;
  - 2 `sign_reversal.csv` columns;
  - the meta subtrees, `meta.capital_return.components[].of_component` among them;
  - two files, the lineage payloads.

  No type change is documented: since the adoption, `meta.adopted` is a string, as in v5. The relocations are listed:
  `change_at_fixed_specifications`' v5 parts are now under `.oct05_case`.
- **G3** (`generality.cjs`). v5's own `main_case.cjs` and `sign_reversal.cjs`, unmodified, run on `caseOf(OCT05, [])` and
  write v5's files byte for byte.
- **G4** (`api_check.cjs`). 9 patterns and 99 checks pass. Patterns 1–8 are v5's consumer call patterns. Pattern 9 is
  the item API. 8 consumer gates need code (`derived/api_check.json` `consumer_code`). Each recorded gate re-runs the
  consumer's code as written at HEAD b7c453a9. Some earlier records reconstructed older code: the winners, band_variants
  and uncertainty specification records, decompose.cjs's SYN_LINES treatment and export_lines.cjs's capRule. Since
  2026-10-07 they run HEAD's code, which passes (log, 14:04 and 14:36). The checks for v6:
  - **Generation split.** The September 29 generation payloads with `withLineage()` on G3+ add to the item base (1e-9).
    The edit sets then make them add to v6 (1e-9) under a stated rule:
    - national-scale edits as they are on every generation model (their totals are the case's);
    - item 1's lineage parts on G3+;
    - its union parts by each generation's share of the union's OASDI receipts and Part A accrual;
    - item 4's parts and carriers by each generation's share of the split-basis line's union amount (`split_basis`).

    Every split basis is a spending line of model.json, as the generation lane's `v6_split.cjs` `splitBasis()`
    requires, and union_key_pell's is education_services.
  - **decompose.cjs.** Three gates stop as written:
    - the receipt-line gate (:283-284), on item 4's carriers;
    - the lineage-last gate (:308-311);
    - the pension-source sha gate (:286-290).

    Its v4 line gate (:281-282) passes: the lines beyond SYN_LINES are the state-price and road lines, which it classes
    itself (:423-427). The lineage block and the item positions locate exactly.
  - **export_lines.cjs.** Its pension gate (:302) misses by exactly item 1's lineage parts. Its capRule (:97) reads the
    case's payload, the offsets included, and passes.
  - **band_variants.cjs.** Its layout gate (:312-320) stops as written. Its specification rebuild (:260-269) reads
    every `meta.responses` entry and passes.

    Its split move gate (:450-454, header :68-73) misses by the edit sets' move of the variants, up to 0.0169bn
    (justice_raw_coding). That move is item 2's: it changes national totals, `public_order_safety`'s among them, that
    the variants' keys divide by. Item 1 moves no variant (1.1e-13).
  - **sept24_specs.cjs.** keyLines (:104-115) stops on the offsets' key kind, which has no derivative (:160-170). Its
    scaled gate (:197-200) passes: the coefficients differ only where a national total they divide by moves.
  - **winners specs.cjs.** Its specification rebuild (:162-172) reads all 13 `meta.responses` entries and passes.
  - **The roads-off pattern** skips the item's offsets and counts any unknown component.
  - **Pattern 9:**
    - no item gives v5;
    - `meta.items` and the edit locations, and the parts adding exactly;
    - the lineage payload files;
    - `withItems()` on a consumer's model, the fixed-amount guard and `editsAt()`;
    - item 4's carriers and offsets in both payloads, with `componentsFor(null)` as the payload's components. Its
      carriers are zero on model.json, and `withItems()` on a `withSyntheticLines()` model is the case (1e-9). A second
      application stops ("already"). The pupil-share option drops the k12 offset. Moving other_federal_benefits stops
      at user_fees;
    - an arm's payload against its band row;
    - the order and arm guards, the reserved meta, and the stop on a count change in a lineage item;
    - a lineage option (`arm_a`). It is a variant whose payload, through consumer.cjs, gives its band row. With no item
      it gives the lineage lane's arm a band. An unknown option stops.
- **G5**. Command:

  ```
  uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/main_case_2026_10_07 "node {lane}/main_case.cjs" "node {lane}/lineage_addition.cjs" "node {lane}/sign_reversal.cjs" "node {lane}/generality.cjs" "node {lane}/zero_items.cjs" "node {lane}/contract.cjs" "node {lane}/api_check.cjs" --allow-unrun infra/immigration-fiscal/main_case_2026_10_07/package.cjs --allow-unrun infra/immigration-fiscal/main_case_2026_10_07/item_age_mix.cjs --allow-unrun infra/immigration-fiscal/main_case_2026_10_07/item_user_fees.cjs --allow-unrun infra/immigration-fiscal/main_case_2026_10_07/lineage_count.cjs --allow-unrun infra/immigration-fiscal/main_case_2026_10_07/ancestry_share.cjs
  ```

  Result: IDENTICAL, 25/25 files unchanged, exit 0, in 55 s (15:02:51–15:03:46 JST). The five `--allow-unrun` files
  are modules the scripts load. With `lineage_addition.cjs` second (16:43:07–16:44:17 JST): IDENTICAL 27/27, exit 0,
  and the three payload files' sha256 are unchanged.

## Approximations and assumptions

- **[ASSUMPTION] Variants leave the fixed-amount items' edits at the case's**, as they leave the added people's amounts.
  This covers item 1, and item 4's edits (its carriers are recomputed on each option's model). The worst error this
  leaves for item 1 is $0.043bn (payroll_compliance high-cost readings; `range.items_at_the_case_data`). Item 2 follows
  each option's totals (`editsAt`).
- **[APPROX] The added people's pension factors are G3+'s** (f_ss, f_pa), on v5's and on the age-mix base.
- **[APPROX] National cost weights stand in for each worker's OASI/DI mix** in the separate-funds reading. This comes from
  the pension lane (TR 2026 Tables IV.B1 and IV.B2). The scheduled-benefits arm stays on the 2025 reports.
- **Item 2 inherits its lane's assumptions:** μ high is symmetric about the central value [ASSUMPTION]; the legacy part
  is at response 0; enterprises are left off. The school key's legacy-stripped prices (+$0.27–0.87bn) are not wired, as
  briefed.
- **Item 3 inherits its lane's measurement and route.** The count is v5's arm b, unchanged at 3.04M. The per-cell age
  factors use `price.cjs`'s functions, copied from 21d9a21d into `item_age_mix.cjs`. They are gated to rebuild v5's
  addition exactly at the identified mix and to reproduce the lane.
- **Item 4 inherits its lane's measurement.** The limits above apply:
  - [ASSUMPTION] union-only (−0.023 / −0.056 left out);
  - [ASSUMPTION] Pell splits by generation and household on the education line (`meta.user_fees.splits.basis_rule`).
    Splitting it on its parent line instead moves the ancestry-share rows by +0.161 / −0.244 and −0.099 / +0.111;
  - [APPROX] item 2's line totals not carried (−0.028 / −0.028);
  - the fold's school low side (+0.47 / +0.39 against the lane's form);
  - transit left out;
  - the K-12 weight arms not wired.
- **The `adopted` row in `main_case_bands.csv` is v6**, adopted 2026-10-07. It keeps v5's row name for the contract.
  v5's own rows are `oct05_case` and `oct05_cash_set`.
- **The companion readings** (section Companion readings) carry the following:
  - [ASSUMPTION] item 3 at the lineage options uses the age mixes measured on arm b's counts. Its size at each option
    is listed there; at arm c it is +2.618 / +5.486 on the set.
  - [ASSUMPTION] in the count by ancestry share, items 1 and 4's union parts split by generation by the stated rule.
    The measured pension split moves the rows by at most 0.126bn.
  - Everything else is the lineage lane's route, ported and gated at v5's values: its responses, its C3 line and its
    fractional count, including that count's [FRAMING-SENSITIVE] shares.

## Consumers

This is the brief for the propagation to `oct07`. **Every consumer below needs code, except distribution (a path
swap) and the three lanes that only inherit the white and debt lanes' runs.** A consumer that applies the payload whole
and evaluates it through `package.cjs` gets every item. A consumer that splits the case by generation, household or person needs a rule for each item:

- **R1, `pension_tr2026` (set only).** Its union and lineage parts per allocation, from `meta.items` parts:
  - union_oasdi and union_part_a go to the union by a stated split. G4 checks each generation's share of the union's
    OASDI receipts and Part A accrual; the pension lane's per-generation rows (`arms.csv`) are the measured
    alternative;
  - lineage_oasdi and lineage_part_a go to the added people (G3+).
- **R2, `retiree_health` (set and cash).** National-scale edits (`national_bn`). Apply each as it is to every split
  model, so each part keeps its share of the line and the split follows the keys. Never apportion the national change by
  hand.
- **R3, `added_age_mix` (set and cash).** The lineage slot: `meta.lineage.edits` (first 416, count 336, row 8 at 751)
  and `derived/lineage_payload*.json`; `P.LINEAGE_EDITS` and `P.withLineage()` on G3+ carry it. The added people's parts
  are in `summary.json` `v6.lineage_item_parts`.
- **R4, `user_fees` (set and cash).** Union-only. Split each edit's parts and each carrier's cells pro rata to the
  group's share of the split-basis line's union amount at its preferred key (`meta.user_fees.splits.split_basis`):
  education_services for the higher-education parts, Pell and the K-12 weight's parts, health_services for the health
  parts. Pell is folded into other_federal_benefits but splits on the education line, because it goes to students
  (`basis_rule`). The added people take none. An offset goes with its
  `of_component`: its target's part, level, class and financing.

Line numbers are at HEAD b7c453a9. Propagation workers are editing some of these files. I re-read each cited line in
code on 2026-10-07, or G4 ran it. The exceptions are `real_costs_totals.py`, `reweight.py` and `profiles_oct05.py`, which
are the item-1 sweep's [UNVERIFIED].

| Consumer | Stops at | Rules it needs | Fields to read |
|---|---|---|---|
| Generation account (`generation_account_2026_09_24`) | `v5_split.cjs:43-55` loadCase: the item edits after the lineage's, and receipt lines that must be the base's (the carriers). `run_generations_v5.cjs:127-136`: the payload-route gate | R1, R2, R3, R4 per generation, with the carriers scaled by the same shares. G4 pattern 3 checks that this rule adds to v6 (1e-9). Then write `generation_corrections_oct07*.json` | `meta.items` (edits, parts, capital), `meta.lineage.edits`, `meta.user_fees.splits`, `receipt_lines` |
| Late-arrival line (`late_arrival_account_line_2026_09_27`) | `medicaid_check.py:155` reads `pension_accrual` from the September 29 payload, and `:174-177` gates Part A at 41.137 × scale (v6 is 40.783). `:166-169` holds G1's Medicare parts at the previous case's, which item 1's union Part A moves [INFERENCE: not run]. `run_cells.cjs:511` gates the cells' edits and receipt lines | Inherits the generation lane's oct07 split (R1–R4) over its nine cells | the oct07 `meta.pension_accrual.part_a_accrual_bn`; the generation lane's oct07 files |
| Debt legacy (`debt_legacy_2026_09_23`) | `debt_legacy.py:2065-2073` v5_parts: the lineage must close the payload, and the receipt lines must be the previous case's. `:2084-2086`: meta keys beyond `V5_META_KEYS` stop it; its `meta.adopted` check passes since the adoption | Its union twin (previous payload + row 8) takes R1's union parts, R2's edits and R4 whole; the lineage step takes R1's lineage parts and R3. Its port already handles the offsets' key kind (`capital_rows`, :670-680) once the carriers are applied as receipt lines (:438). Replace the oracle bands | `meta.items`, `meta.lineage.edits`, `receipt_lines`, `meta.capital_return.components` |
| Sept 24 propagation and pairing (`sept24_propagation_2026_09_24`) | `band_variants.cjs:312-320`: the case must be the September 29 payload plus the lineage's edits. `:450-454` (G4): the split move gate misses by item 2's move of the variants, up to 0.0169bn (justice_raw_coding). Its specification rebuild (`:260-269`) passes | No split. Compare `slice(n29, n29 + 336)` with `LINEAGE_EDITS` and the tail with the items' edits by `meta.items`. Variants follow `v6.variants_rule`; the split move gate takes the edit sets' move of each variant. `real_costs_totals.py` takes `v6.per_member_usd` (a path swap); constant_choices waits on debt legacy | `meta.items`, `meta.lineage.edits`, the offsets, `receipt_lines`, `v6.per_member_usd` |
| Uncertainty (`uncertainty_propagation_2026_09_22`) | `propagate.py:499-501` lineage_cells. `sept24_specs.cjs:104-115` keyLines stops on the offsets' key kind (`receipt_amount_over_national`, new with item 4), which has no derivative (`:160-170`). Its scaled gate (`:197-200`) handles the national totals item 2 moves (G4 passes) | R1's lineage parts go with the lineage; propagate.py re-applies `meta.pension_accrual`, so :534-537 otherwise miss by them. R2 as is. R3: re-base `lineage_component` (propagate.py:320) and `test_uncertainty.py:221-225`, which gate against the lineage lane's arms, on this lane's lineage payload. R4 union-only; an offset's derivative is 0 per unit of a group's amount, since its key comes from national totals | `meta.lineage.edits`, `meta.items`, `meta.pension_accrual`, the offsets |
| Winners and losers (`winners_losers_2026_09_24`) | None in `specs.cjs`: its rebuild (`:162-172`) reads all 13 `meta.responses` entries and passes on v6 (G4). `winners_losers.py:175-181` pins the oct05 lanes | No split of its own: it takes the case's lines at the ends. The offsets arrive as `capital_<id>` lines and take their `of_component`'s class. If the debt lane's lines carry them, they also need financing fractions, since :667-676 stops on a line without one [INFERENCE: not run]. Path swap and pins after the generation, debt and distribution lanes rerun | `of_component`, `meta.items` |
| Back-cast (`historical_backcast_2026_09_20`) | `case_components.cjs:157-158`: `pension_accrual` must be September 29's. If only that gate is relaxed, `change29` (:238-243) silently books the whole Social Security and Medicare move as v5 accrual parts | By component: R1's union and lineage parts as their own components, R2 by line, R3 the lineage, R4 by parent line with the offsets under their targets. `change_at_fixed_specifications.sept29_case` is now at `.oct05_case.sept29_case` | `meta.pension_accrual`, `meta.items` (parts, capital), `change_at_fixed_specifications.items` |
| Distribution (`distribution_weights_2026_09_23`) | None found. `distribute.py:431-447` chains each case on the previous adopted row | Whole case; a path swap: `Case(main_case_2026_10_07, "oct05_case", …)`, with summary key `adopted_2026_10_05` (`change` is v6 − v5). `case_ends.cjs:104` sums capital by `level`, which the offsets carry from their targets. The items move A, and item 3 also moves the production term: the added people's grid moves by up to 2.14bn in P, and at the band-end evaluations P + F moves −0.038 (specification 48) and −0.025 (11) | `summary.json` `main_case`, `adopted_2026_10_05`, `change`, `cash_set`; the components' `level` |
| World ledger (`world_ledger_2026_09_27`) | `valuation.py:235-236` stops on an unclassified line: `CAPITAL_COMPONENTS` (:181-188) has no offset ids. `generation_lines.cjs:105-116` gates the generations' union against the `adopted` row (5e-5), which passes once the generation payloads carry the items | Inherits the generation lane's split (R1–R4). The offsets take their `of_component`'s class (education, health_services). Its carriers are receipt lines classed as tax, at effect 0 | `of_component`; the generation lane's oct07 files and pins |
| Household split (`within_group_distribution_2026_09_29`) | `export_lines.cjs:280-304` (the gate at `:302`): the pension gate misses by exactly item 1's lineage parts (G4). Its capRule (`:97`) reads the case's payload, offsets included (G4 passes). `households.py:621-623` stops on a receipt key other than enterprise_surplus, which is the offsets (new with item 4) | R1: count the lineage parts in `own`; households.py re-applies ratio_net (now 0.95355). R2 per generation model. R3. R4 pro rata to the parent line's amount in the household or person (`splits.household_person`); each offset splits like its carrier's parent line | `meta.pension_accrual`, `meta.items`, `meta.user_fees.splits`, the offsets; the generation lane's oct07 files |
| White replacement and Black rough comparators (`white_replacement_2026_09_28`, `black_comparator_rough_2026_09_28`) | `engine_lines.cjs:33-42` unionOnly, in both lanes, misattributes **silently**: the union dump is BASE + row 8, so items 1, 2 and 4's union parts land in "full − union" and count as the added people's. `rekey_sept29.py` stops at `:281-282` (the white lane's union ratio 0.97367 against 0.95355), `:945-946` (`pension_accrual` must be September 29's) and `:950-955` (the case less the dump must be the lane's added-people parts) | The union dump takes R1's union parts, R2's edits and R4 whole. The added people take R1's lineage parts and R3 (`v6.lineage_item_parts`: g3plus_members, whites). Rerun `accrual_white.py` and `accrual_black.py` on the 2026 separate-funds path | `meta.items` parts, `meta.pension_accrual` (ratio_net, source, paths), `v6.lineage_item_parts` |
| Indian full account, legacy comparators, pension legacy (`indian_full_account_2026_09_29`, `legacy_comparators_2026_09_30`, `pension_legacy_2026_09_30`) | No gate of their own found: they read the white lane's library and dumps and the debt lane's stocks (`legacy.py` gates those at 1e-6) | Inherit the white and debt lanes' oct07 runs. `accrual_indian.py` goes on the 2026 separate-funds path. Pension legacy reads only `meta.lineage.counts.lineage_population`, which is unchanged | `meta.lineage.counts`; `meta.pension_accrual` for the Indian accrual |
| Break conditions (`break_conditions_2026_09_29`) | `engine_breaks_sept29.cjs:144-147`: the sha gate on the 2025 pension file, while v6's `meta.pension_accrual.source` is the 2026 lane's. `:324-326`: the lineage's edits close the payload | R1's union parts go into TAIL_SS / TAIL_MED and its lineage parts into linSS / linPA. R2 and R4 go in the tail. R3 is LINT, sliced by `meta.lineage.edits` rather than to the end as :327 does. schedAdd mixes the 2025 scheduled arm with the 2026 ratio. Write `tables_oct07.py` | `meta.pension_accrual` (source, paths), `meta.items`, `meta.lineage.edits` |
| Decomposition (`main_case_decomposition_2026_09_29`) | `decompose.cjs:283-284` (G4): the receipt lines must be v4's two, so the carriers stop it (new with item 4). `:286-290`: the 2025 pension sha. `:308-311`: the lineage last. Its v4 line gate (`:281-282`) passes | R1's lineage parts go with `lin` and its union parts in the tail by `meta.items`. R2 by line, R3 the lineage, R4 in its parent line's parts, the offsets with their targets (`CAPITAL_GROUP` of `of_component`). `profiles_oct05.py` is a path swap | `meta.pension_accrual.source` and `.paths`, `meta.items`, `meta.lineage.edits`, `of_component`, `receipt_lines` |
| Closed budget (`closed_budget_2026_10_06`) | `closed_budget.py:167-174`: the per-person excess must reproduce `EXCESS_PRINTED` (:74, ladder 269's $280.5 / 297.4bn), which v6 moves. `:155-163`: the decomposition's parts add to the case. Inputs are pinned to oct05 at :61, :75, :149 and :244 | No split of its own. The items enter through the decomposition's oct07 line groups. Re-pin `EXCESS_PRINTED`. `trust_funds.py:60` takes the combined OASDI fund's depletion (2034 Q3), while item 1 is on separate funds (OASI depleted Q4 2032): switch to OASI's date, or state the mismatch | `summary.json` `main_case`, `cash_set`; the decomposition's `summary_oct07.json` and `decomposition_lines_oct07*.csv` |

Notes:
- **Locate items by `meta.items`**: `edits.first` and `count`, and `capital.receipt_lines` and `components`. Never use
  counts or positions. Today the set has 769 edits (752 + 2 + 10 + 5) and the cash set 765.
- **Item 4's capital rides on carriers.** A consumer that builds its own models (per-group payloads, variants,
  derivatives) must carry the carriers (`receipt_lines` after v5's two) or call `withItems()`, which recomputes them on
  the model.
  - Four consumers stop on item 4's capital as written: `sept24_specs.cjs:104-115`, `households.py:621-623` and
    `valuation.py:235-236` on the offsets, and `decompose.cjs:283-284` on the carriers.
  - Map each offset to its `of_component` wherever capital is grouped by id.
- **Fixed amounts.** Items 1 and 4 edit by fixed amounts. An option that moves the national total of a line they edit
  stops in the package. Item 2 follows each option's totals. The pupil-share option drops the k12 offset.
- **The adopted stamp.** `meta.adopted` is `2026-10-07`, in v5's form, so `debt_legacy.py:2085`'s check passes.
- **The oracle.** Each consumer gates its oct07 total against `main_case_bands.csv`: `adopted` is 389.0826 / 461.4797
  and `cash_set` 307.3994 / 385.3641.
- **The companion readings** are the rows `lineage_<option>` and `ancestry_share_<scenario>` (each with `_cash_set`) in
  `main_case_bands.csv`, and `v6.companions` in `summary.json`. The record and the drift audit should quote them from
  there.
- **The producers stay on oct05:** `pension_tr2026_2026_10_06`, `public_pension_legacy_2026_10_07`,
  `added_age_mix_2026_10_07` and `user_fee_allocation_2026_10_07`. Keyed to oct07, each would add its item twice; for
  example, case_opeb.cjs appends its scale edits after all existing ones.
- **Outside v5's table** (the item-1 sweep's classes):
  - nonresponse bias (`reweight.py`): a path swap that re-applies `meta.pension_accrual`;
  - public charge and post-2024 law: path swaps, since the decomposition frame (NG, NC) is unchanged;
  - number drift audit: oct07 records (`_pairing("oct07")`), with EARLIER pointing at v5;
  - evidence map: moves only when the operator asks. Its waterfall then needs the four item steps and a v5 subtotal.

## For the parent

- **The adoption is in place.** In `package.cjs`, `STATUS` is `adopted` and `ADOPTED` is `2026-10-07`.
  - The stamp gate checks that `decisions/2026-10-07-main-case-v6.md` exists, and G4 checks the stamps. G2 documents no
    type change.
  - The adoption changed only meta's adopted, case, status, user_fees and items. The edits, lines, production grid and
    every band are unchanged.
- **The pinned files.** The consumer lanes pin these as committed in 218a2fb2; every later rerun reproduces them byte
  for byte:
  - `derived/corrections.json` f8d346aacf05bcdaed8495f870ba23ac6154ab3eaf34cc0bcf85861f0c85d091;
  - `derived/corrections_cash.json` e9033bfff737299e76d09b0c600e8f42c6b6110713f402fb293a6324b2721e80;
  - `derived/summary.json` 547092591e23ebd69e7dfaec28e6eebe441c7cc61a9f3d32f328a3991f321bf3.

  The companion readings are inside the pinned `summary.json` (`v6.companions`) and in `main_case_bands.csv`, as
  committed. Moving them to files of their own, as the parent asked before the commit, would change `summary.json`.
- **The decision (025203f4) agrees with this lane,** Pell's split basis and the ancestry-share figure ($274.9–374.8bn)
  included. Pell splits on the education line since the 14:51 run: only `meta.user_fees.splits`, the record's
  `split_rule` and the four ancestry-share rows changed then. With this round's two gates its counts become G1 129 and
  G4 99 (it says 128 and 98).
- **The parent's exact Pell wording is not in meta.** Its parenthetical for the generation rule and an [ASSUMPTION]
  tag in `basis_rule` would change both payloads' hashes. The committed rule already lists union_key_pell under
  education_services, and `basis_rule` gives the reason; the tag is here (Payloads, Assumptions).
- **Gate (a).** It uses the file's −0.296058 / −0.726064, not the brief's −0.296104 / −0.726103.
- **The school low side: I recommend keeping the fold.** The fold follows the engine's convention that an edit responds
  at its line's response, so by-line consumers stay right without synthetic response-1 lines. It differs from the
  lane's form only below a school response of 1, by +0.47 / +0.39 on the within-district row. The companion figure rounds
  the same either way ($361–435bn on v6).
- **Item 2's figure.** The parent's +0.565 is the lane's rounded line sum. The band change is +0.563.
- **The producers stay on oct05.** Re-keying the item lanes to oct07 would count each item twice.
- **Committed by the parent** (218a2fb2, the lane; 025203f4, the decision). Not yet committed: the pinned-band gate in
  `main_case.cjs`, the split-basis check in `api_check.cjs` with `derived/api_check.json`, and this RESULT. None of them
  changes a pinned file. Peak memory in the last full run was 736 MB (`main_case.cjs`) and 362 MB (`api_check.cjs`).

## Files

- `package.cjs`: the registry, the builders (items 1 and 2), `forItems` (with the capital overrides), `caseOf` (with
  lineage options), `rebase`, `checkBuilt`, `checkLineage` and SLOTS.
- `item_age_mix.cjs`: item 3's builder, using `price.cjs`'s functions from 21d9a21d; at a lineage option it takes the
  option's counts, C3 and addition.
- `lineage_count.cjs`: the lineage options, the lineage lane's route (`lineage_case.cjs` at d3b7e6e6) ported and gated
  to rebuild v5's addition exactly.
- `ancestry_share.cjs`: the count by share of Mexican-immigrant ancestry on a case, the lineage lane's fractional count
  with the items split by generation.
- `item_user_fees.cjs`: item 4's builder. It holds the fold, the K-12 weight re-blend, the carriers and offsets, and
  `meta.user_fees`.
- `main_case.cjs`: G1 and the derived files; `--items none` gives v5.
- `sign_reversal.cjs`.
- `zero_items.cjs`: G1's identity.
- `contract.cjs` (G2), `generality.cjs` (G3) and `api_check.cjs` (G4).
- `lineage_addition.cjs`: the lineage's addition by part (section above). The v6 docs pass wrote it; it was moved
  here unchanged, and its output is byte-identical to that pass's scratch run.
- `derived/`:
  - `corrections.json` and `corrections_cash.json`;
  - `lineage_payload.json` and `lineage_payload_cash.json`;
  - `main_case_bands.csv`, `components.csv`, `per_spec.csv`, `summary.json` and `sign_reversal.csv`;
  - the gate records `zero_items.json`, `contract.json`, `generality.json` and `api_check.json`.
  - `lineage_addition.json`, with its own gate record.

**Run order**, about 50 s:

```
node main_case.cjs && node lineage_addition.cjs && node sign_reversal.cjs && node generality.cjs && node zero_items.cjs && node contract.cjs && node api_check.cjs
```

## Log (append-only; times from `date`)

- 2026-10-07 10:49 JST — lane created; reading CLAUDE.md, main_case_2026_10_05 and pension_tr2026_2026_10_06.
- 2026-10-07 11:20 JST — read v5's package.cjs, main_case.cjs, sign_reversal.cjs, contract.cjs, generality.cjs, api_check.cjs and the
  pension lane (case_tr2026.cjs, derived/case_oct05.json, summary.json; committed 8cefec37). Plan [INFERENCE, from the code]:
  - **The package wraps v5's package; it does not re-merge.** v5's `forCase` blocks when the edits after v4's are not
    exactly the lineage's, so v6 cannot be `forCase(SEPT29, v6 payload)`. `forItems(base, items, which)` takes v5's
    API (set or cash) and applies each item's edits on top of every model it builds (`withItems`), overriding only
    `modelFor`, `evalPackage`, `central`, `payloadModel` and `correctionsPayload`. With zero items it is v5's API
    with v5's payload, unstamped.
  - **Item edits are appended after the lineage's** (positions 752-753). `meta.lineage.edits` stays v5's (row 8 at 751
    is no longer last); `meta.items` locates each item's edits. Consumers that assume the lineage closes the payload
    then stop loudly instead of misattributing the item (a parallel read-only sweep found seven such gates; to verify).
  - **Item 1's two edits are rebuilt from the source lane's rule** (case_tr2026.cjs `editsFor`: union and lineage
    parts per allocation) and gated equal to the arm's stored edits in case_oct05.json, exactly; the four parts go in
    `meta.items` for consumers that split the case.
  - social_security and medicare are household transfers on their preferred keys in every state (no state sets
    `spending_keys`; transfers respond at 1), so the item's change is `by[allocation]` at every specification.
- 2026-10-07 11:37 JST — package.cjs and main_case.cjs written. With item 1, main_case.cjs passes 73 gates (16 s, 421 MB peak): the set
  is $387.447–458.569bn, the base plus −2.847 (shared) / −2.674 (personal) at every one of the 64 specifications (max
  |diff| 5.7e-14 against consumer.cjs), ends 48/11 in both methods; the cash set is v5's exactly. With `--items none`
  it passes v5's 54 gates and writes v5's six files byte for byte. Not yet run: sign_reversal, contract, generality,
  zero_items, api_check, rerun.
- 2026-10-07 11:40 JST (the written files' mtimes, `ls -l derived/`) — sign_reversal.cjs, generality.cjs (G3 PASS: v5's own scripts on the zero-item package write
  v5's seven files byte for byte), zero_items.cjs (G1 identity PASS: this lane's two scripts with `--items none` write
  v5's seven files byte for byte) and contract.cjs (G2 PASS) run on item 1. A read-only consumer sweep (Explore agent)
  classed the 26 v5 consumers; seven stop on the lineage-closes-the-payload or edits-length gates (verified in code:
  v5_split.cjs loadCase, band_variants.cjs, propagate.py lineage_cells, debt_legacy.py v5_parts, engine_breaks_sept29.cjs,
  decompose.cjs), and engine_lines.cjs `unionOnly` would misattribute silently.
- 2026-10-07 11:57 JST — the parent's items 2 and 3 arrived (sent 11:01 and 11:13 JST, read from the queue now):
  item 2 = retiree health on accrual (public_pension_legacy_2026_10_07, arm central: ten national-scale edits, set
  AND cash, +$0.565 / +0.737bn); item 3 = the added people at their measured age mix (added_age_mix_2026_10_07, keys
  route, 2007–26 cross-section: set +1.35 / +2.86bn, cash −0.27 / +1.92bn). Plan:
  - **Item 3 needs no structural change to v5's package.** It is the lineage slot: its builder rebuilds v5's lineage
    addition (335 cell edits, row 8's edit, the production grid) as v5's values plus the age-mix deltas
    (later x (G_L − G) + (1 − C3) g3 x (G_3 − G) + C3 g3 x (W_3 − W)), so the identified mix gives v5's addition
    exactly; v5's exported merge(), adoptLineage() and forCase() then build the base on the September 29 payloads,
    set and cash. The per-cell age factors are price.cjs's (g3_age_keys.json, band_lines.json; its functions copied).
  - **Items 1 and 2 are rebuilt on that base.** Item 1's lineage part is (f − 1) x the added people's amounts there;
    item 2's edits are a function of the model (national + δ per line, engine.js scaleLine), so its change follows the
    group's share. The pairwise interactions are run and reported, not assumed away.
  - Arms are item options: `caseOf(base, ids, {item: arm})` rebuilds the case with one item at an arm, so every arm
    row is the v6 case with that reading (and its source-lane arm is checked alone on v5).
- 2026-10-07 12:16 JST (the derived files' mtimes) — the three-item case built. main_case.cjs passes 101 gates: $389.379–462.206bn, cash
  set $307.695–386.090bn, ends 48/11. A first run failed the parts-sum gate because item 1's parts came from the joint
  record, which is on the age-mix base; the gate now reads the item-alone record. sign_reversal.cjs, generality.cjs
  (G3 PASS), zero_items.cjs (G1 identity PASS) and contract.cjs (G2 PASS) rerun on the three-item case (12:17).
- 2026-10-07 12:20 JST — resumed after a context compaction; read the parent's checkpoint and the team inbox (no message
  after item 3).
- 2026-10-07 12:33 JST (`api_check.cjs` mtime 12:33:49) — api_check.cjs (G4) written from v5's. The first run crashed in pattern 2: a payload line (school_reprice,
  college_rekey) is absent from model.json. The second failed one check: v5's statement that only key-picking variants
  move the case differently from September 29 does not hold on v6. Item 2 moves public_order_safety's national total,
  which the capital keys divide by, so the justice grids move by up to 0.0006bn more. The check was restated (v5's
  statement on the item base; item 1 isolated at 1.1e-13; item 2 on the lines it scales). G4 PASS: 9 patterns, 90
  checks, 14 consumer gates need code.
- 2026-10-07 12:34–12:35 JST (`date` 12:34:11 and 12:34:58) — G5: rerun_lane.py IDENTICAL 22/22, exit 0.
- 2026-10-07 12:37 JST — RESULT finalized; the PROBE stub removed.
- 2026-10-07 12:41 JST — the parent's item 4 (fees and education keys, user_fee_allocation_2026_10_07 @ 81bd22da, all parts but transit) and the Consumers-table addendum arrived.
- 2026-10-07 12:57 JST — resumed after a context compaction. Plan for item 4: fold the amounts into the parent lines;
  take the K-12 weight as row 6's re-blend at w_K; re-key the college and K-12 capital through carrier receipt lines and
  offset components, an optional `capital` field on the item. The three-item files were copied to the scratchpad first.
- 2026-10-07 13:16:56–13:17:15 JST — the first four-item run of main_case.cjs failed 10 gates. The fixes:
  - the payload-model identity and the set and cash framing now allow the carriers and offsets;
  - the retiree check compares models through retiree_health only;
  - the parts sum takes the capital parts;
  - a `viaCandidate` override adds the item's capital;
  - the pupil share treats k12 with its offset;
  - the `withSyntheticLines` gate keeps the carriers' national;
  - zero carriers keep a national total, since 0/0 gave NaN;
  - land rows map an offset to its target.
- 2026-10-07 13:21:53–13:22:12 JST — a scratch run passes 108 gates.
- 2026-10-07 13:25:13–13:26:07 JST — the lane's main_case.cjs and sign_reversal.cjs ran; generality and zero_items
  PASS. contract FAIL: the offset columns sat mid-file in `per_spec.csv`, and were moved to the end.
- 2026-10-07 13:26:42–13:27:29 JST — all five scripts pass.
- 2026-10-07 13:27:34 JST — api_check crashed in the roads-off pattern: V4's evaluation has no item components. It now
  skips them and counts unknown ones.
- 2026-10-07 13:28:10–13:28:13 JST — G4 PASS. The double-application check was then retargeted to item 4 alone, because
  on the case the stop came from the nationals guard rather than the carriers. It now requires "already". G4 PASS again.
- 2026-10-07 13:28:47–13:29:36 JST — G5: rerun_lane.py IDENTICAL 23/23, exit 0.
- 2026-10-07 13:34–13:42 JST — resumed after a context compaction. Re-read the consumers' gates at HEAD b7c453a9 for the
  Consumers table. Three newly found consumer gates stop on item 4's offsets: sept24_specs.cjs keyLines, households.py
  and valuation.py. Also decompose.cjs's receipt-line gate.
- 2026-10-07 13:42 JST — RESULT rewritten for the four-item case.
- 2026-10-07 13:47:56 JST (transcript time) — the parent's five messages arrived together: item 4 resent, the adoption
  step (the operator's "ok do what you think is good", 12:02 JST), the companion readings, prop-c's corrections and
  item 4's metadata.
- 2026-10-07 13:57:56–14:00:34 JST (transcript times) — item 4's record gets `union_only`, union_* part names,
  `parent_lines` and `capital_components`. `STATUS` adopted and `ADOPTED` 2026-10-07 in v5's stamp form; G2 documents
  no type change; G4 checks the adopted stamps. The winners and band_variants records restated to HEAD's code.
- 2026-10-07 14:01:28–14:02:17 JST (`date`) — the full order in place with the adoption stamps: all pass (the
  decision file existed). G4: 94 checks, 11 consumer gates.
- 2026-10-07 14:02:21–14:04:49 JST (transcript times) — prop-c's corrections. Neither "already fails on v5" claim
  reproduces at HEAD b7c453a9: winners' gate (specs.cjs :162-172) passes, band_variants' specification rebuild
  (:260-269) passes and its split gate misses on v6 by up to 0.0169bn. The uncertainty records restated to
  sept24_specs.cjs at HEAD (keyLines :104-115; the scaled gate :197-200 passes). G4: 95 checks, 9 consumer gates.
- 2026-10-07 14:06:57 JST — resumed after a context compaction. 14:07:38: status sent to the parent.
- 2026-10-07 14:17:59 JST (`lineage_count.cjs` mtime) — the lineage options. The port of `lineage_case.cjs`'s route
  rebuilds v5's addition byte for byte at arm b and C3 0.557. At arms a and c it reproduces the lineage lane's stored
  mG, mW, row 8 edit, s and general-government responses exactly (14:18:09).
- 2026-10-07 14:18:27–14:19:57 JST (transcript times) — `item_age_mix.cjs` and `package.cjs` take a lineage option.
  With no item, each option gives the lineage lane's stored v5 value, set and cash, to 4e-13 (14:20:12). A scratch run
  of `main_case.cjs` writes the adopted payloads byte for byte (14:20:46).
- 2026-10-07 14:24:01–14:24:42 JST (transcript times) — `ancestry_share.cjs`. On v5 it reproduces the lineage lane's
  four fractional rows exactly.
- 2026-10-07 14:28:50–14:29:41 JST (`date`) — the full order in place with the companion readings: all pass, G1 128
  gates, G4 96 checks with 9 consumer gates.
- 2026-10-07 14:29:53–14:30:51 JST (`date`) — G5: IDENTICAL 25/25, exit code not captured (`PIPESTATUS` is bash-only;
  the shell is zsh). Rerun 14:30:59–14:32:11: IDENTICAL 25/25, exit 0.
- 2026-10-07 14:33:05 JST (transcript time) — prop-c's correction 3 confirmed: item 3 moves the production term,
  P + F −0.038 (specification 48) and −0.025 (11), and P by up to 2.14bn over the grid.
- 2026-10-07 14:33:10–14:35:34 JST (transcript times) — two more api_check reconstructions that were not HEAD's code,
  the same class as prop-c's: decompose's synthetic-line list and export_lines' capRule. Both now check HEAD
  b7c453a9's code. decompose.cjs's receipt-line gate (:283-284), which stops on item 4's carriers, is now recorded.
  G4: 98 checks, 8 consumer gates.
- 2026-10-07 14:37:50–14:40:35 JST (transcript times) — RESULT updated: the adoption line, Companion readings, the
  gates and the Consumers table (prop-c's corrections).
- 2026-10-07 14:40:47–14:41:38 JST (`date`) — the full order in place: all pass (G1 128, G4 98 with 8 consumer
  gates). 14:41:44–14:42:34 (`date`): G5 IDENTICAL 25/25, exit 0. 14:42:40: the payloads match the 14:18 backup
  byte for byte; `main_case_bands.csv` differs only by the 12 companion rows.
- 2026-10-07 14:44:40 JST — resumed after a context compaction. The decision file, rewritten at 14:41:16 (its birth
  time), checked against this lane. Every figure agrees, but its rule for Pell does not: Pell splits on the education
  line, where the payload split it on other federal benefits.
- 2026-10-07 14:51:23 JST (transcript time) — Pell's split basis set to the education line (`SPLIT_OVER` and
  `basis_rule` in `item_user_fees.cjs`), with "split-basis line" wording in `ancestry_share.cjs` and `api_check.cjs`.
  Only `meta.user_fees.splits`, the record's `split_rule` and the four ancestry-share rows change. The rows move by
  −0.161 / +0.244 (G4+ at nothing) and +0.099 / −0.111 (at its bound), and the outer span becomes 274.874 / 374.793.
- 2026-10-07 14:51:34–14:52:24 JST (`date`) — the full order in place: all pass (G1 128, G4 98 with 8 consumer
  gates). 14:53:26–14:54:17 (`date`): G5 IDENTICAL 25/25, exit 0.
- 2026-10-07 14:56:10 JST (`date`) — RESULT finalized; the final report sent to the parent. Nothing committed.
- 2026-10-07 14:56:58 JST (transcript time) — six of the parent's messages, written before it saw the 14:51 run (the last cites the
  14:42 payload's hash), arrived together: skip the companion arms and adopt; Pell's split basis to education_services with an [ASSUMPTION] rationale;
  gates on the bands and the split bases; the companions in files of their own so that `corrections.json`,
  `corrections_cash.json` and `summary.json` stay fixed once pinned; and the exact Pell rule wording.
- 2026-10-07 14:58:40 and 14:58:45 JST (`git log`) — the parent committed the lane (218a2fb2), with the Pell basis on
  education_services and the companion readings inside `summary.json` and `main_case_bands.csv`, and the decision
  (025203f4).
- 2026-10-07 14:58:57–15:01:23 JST (transcript times) — began the parent's patch (the pre-companion `main_case.cjs`,
  the exact Pell wording), then found the commit. Since the consumer lanes pin the committed files, `main_case.cjs` and
  `item_user_fees.cjs` went back to their committed versions, and only two gates that change no pinned file were
  kept: the adopted bands pinned to the sixth decimal (G1) and the split bases as model.json spending lines with Pell
  on education_services (G4).
- 2026-10-07 15:01:35–15:02:43 JST (`date`) — the full order in place: all pass (G1 129, G4 99 with 8 consumer gates).
  15:02:51–15:03:46 (`date`): G5 IDENTICAL 25/25, exit 0. `corrections.json`, `corrections_cash.json`, `summary.json`
  and `main_case_bands.csv` are byte-identical to 218a2fb2. The hashes went to the parent.
- 2026-10-07 15:05:27 JST (`date`) — RESULT updated for the two gates, the Pell [ASSUMPTION] and the commit. It,
  `main_case.cjs`, `api_check.cjs` and `derived/api_check.json` are left for the parent to commit.
- 2026-10-07 16:38:17–16:38:24 JST (`date`) — the parent moved `lineage_addition.cjs` from the v6 docs pass's scratch
  run into the lane unchanged and ran it in place: 41 gates pass, and `derived/lineage_addition.json` is byte-identical
  to the scratch output. No payload or band file moves.
- 2026-10-07 16:41:32–16:42:33 JST (`date`) — G5 with the script last: DIFFERS 26/27. `contract.json` gained
  `lineage_addition.json` in its list of files v5 lacks, since the committed contract predates the file. The script now
  runs second, after `main_case.cjs`, whose outputs it hashes, so a clean rebuild gives the contract the same list.
- 2026-10-07 16:43:07–16:44:17 JST (`date`) — G5: IDENTICAL 27/27, exit 0; `corrections.json`, `corrections_cash.json`
  and `summary.json` keep sha256 f8d346aa…, e9033bff… and 54709259….
