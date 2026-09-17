**Verdict:** Metro-level matching does **not** shrink the per-person standardized gap toward zero — it reproduces the state-matched result almost exactly (union vs third-plus NH white, `all_age_shared`: −$5,734 age-only → −$5,758 state×age → −$5,797 metro×age, all at 4 age bands, every 95% interval strictly adverse) — and at a common age *and* metro the first-to-third-plus generation contrast falls to +$1,282 [−$719, +$3,284], indistinguishable from zero, while the second-generation gap becomes the *worst* of the three.

Model: claude-opus-5[1m]

[SOURCE: own computation on held CPS ASEC 2025 (income year 2024) + MEPS HC-256, reusing `infra/immigration-fiscal/all_age_ledger_2026_09_17/{analyze,estimator}.py` and `infra/immigration-fiscal/ledger_stress_2026_09_17/common.py` unmodified]
[INFERENCE] for every interpretive statement about what the shifts mean.

---

## What was built

CPS ASEC carries the CBSA code on the **household** record (`hhpub25.csv`: `GTCBSA`,
`GTMETSTA`), not on the person extract the upstream build keeps, so `geo.attach()` merges
those two columns onto `d` by `PH_SEQ` exactly as `extend_ledger.build` merges `GESTFIPS`,
and asserts the merged `GESTFIPS` matches the build's own column record for record. 75.9% of
records sit in an identified CBSA; the remainder are the suppressed/non-metro residual.

Twenty-three metro groups are defined in the brief's priority order (first matching rule
wins). Three fail the positivity gate at 4 age bands and are merged into their state's "other
metro" group; twenty are retained. Cells are metro group × 4 age bands (0–17, 18–44, 45–64,
65+), 80 cells. Estimator, weights, donor model, coefficients and reporting domain are
identical to the source lane; only the cell definition changes.

Three standards are computed at the same 4-band age resolution so they are comparable:
age only (4 cells), state group × age (16 cells), metro group × age (80 cells). A fourth,
`metro_x_age_4_rf5`, repeats the metro standard under a stricter 5-sample-record floor — see
[Sparsity](#sparsity-the-real-limit).

## 1. Union standardized per-person gaps under the three standards

Dollars per standardized person per year at the white reference's own joint shares,
pointwise 95% intervals. `mexican_observed_total` = the three Mexican-origin generations.

| Scenario | Reference | age only | state × age | metro × age |
|---|---|---|---|---|
| all_age_shared | third-plus NH white | −5,734 [−6,348, −5,121] | −5,758 [−6,571, −4,946] | **−5,797 [−6,592, −5,002]** |
| all_age_shared | all natives | −4,204 [−4,751, −3,657] | −4,066 [−4,858, −3,275] | **−3,960 [−4,735, −3,184]** |
| personal_sources | third-plus NH white | −5,824 [−6,464, −5,185] | −5,840 [−6,667, −5,013] | **−5,900 [−6,701, −5,099]** |
| personal_sources | all natives | −4,435 [−5,011, −3,859] | −4,303 [−5,098, −3,508] | **−4,249 [−5,020, −3,478]** |

The three standards agree to within $170 on the union, against standard errors of $280–$410.
Moving from state to metro changes the union gap by at most $106. Whatever the age-only
standard was hiding about where Mexican-origin people live, the state grouping already
captured essentially all of it; metro resolution adds nothing to the union figure. [INFERENCE]

## 2. Per-generation standardized gaps

Versus third-plus NH white, dollars per standardized person, 95% intervals.

| Scenario | Target | age only | state × age | metro × age |
|---|---|---|---|---|
| all_age_shared | Mexico-born | −6,575 [−7,533, −5,617] | −5,847 [−7,020, −4,674] | −5,900 [−7,054, −4,745] |
| all_age_shared | Second gen | −6,216 [−7,078, −5,355] | −7,092 [−8,205, −5,978] | −7,081 [−8,173, −5,989] |
| all_age_shared | Third-plus self-ID | −4,555 [−5,268, −3,842] | −4,678 [−6,363, −2,993] | −4,617 [−6,243, −2,992] |
| personal_sources | Mexico-born | −6,606 [−7,604, −5,608] | −5,670 [−6,927, −4,414] | −5,713 [−6,942, −4,484] |
| personal_sources | Second gen | −5,802 [−6,892, −4,711] | −7,123 [−8,324, −5,922] | −6,955 [−8,105, −5,805] |
| personal_sources | Third-plus self-ID | −4,580 [−5,404, −3,757] | −4,628 [−6,389, −2,867] | −4,650 [−6,369, −2,931] |

The same rotation the state standard produced: geographic matching *narrows* the
first-generation gap by $0.7k–$0.9k and *widens* the second-generation gap by $0.9k–$1.3k, so
the second generation, not the first, carries the largest adverse gap once place is held
fixed. Every interval is strictly adverse under every standard. [INFERENCE]

Versus all natives the same rotation holds: Mexico-born −5,045 → −4,062 (shared, age-only →
metro), second gen −4,686 → −5,243, third-plus −3,025 → −2,780. Full grid in
`derived/metro_matched.csv`.

## 3. Matched gap totals ($bn, vs third-plus NH white)

| Scenario | Target | age only | state × age | metro × age |
|---|---|---|---|---|
| all_age_shared | Mexico-born | −102.08 | −138.56 | −142.07 |
| all_age_shared | Second gen | −115.09 | −162.41 | −163.93 |
| all_age_shared | Third-plus self-ID | −74.13 | −114.59 | −106.58 |
| all_age_shared | **Union** | **−291.29** | **−415.57** | **−412.59** |
| personal_sources | **Union** | **−248.88** | **−350.40** | **−345.50** |

Versus all natives the union runs −215.29 → −259.38 → −240.81 (`all_age_shared`) and
−189.79 → −234.09 → −218.34 (`personal_sources`). Matching on geography makes the matched
total 30–40% more adverse than age alone; metro resolution pulls it back by $3bn (shared) and
$5bn (personal) relative to state, i.e. essentially not at all.

## 4. Generation contrasts at a common age and place

Paired later-minus-earlier differences with replicate covariance, white reference, dollars
per standardized person, pointwise 95% intervals. `derived/metro_generation_contrasts.csv`.

| Scenario | Standard | G2 − G1 | G3+ − G2 | G3+ − G1 |
|---|---|---|---|---|
| all_age_shared | age only | +358 [−764, +1,481] | +1,661 [+666, +2,656] | +2,019 [+890, +3,149] |
| all_age_shared | state × age | −1,244 [−2,722, +233] | +2,414 [+390, +4,437] | +1,169 [−883, +3,221] |
| all_age_shared | **metro × age** | **−1,181 [−2,607, +244]** | **+2,464 [+493, +4,435]** | **+1,282 [−719, +3,284]** |
| personal_sources | age only | +804 [−530, +2,138] | +1,221 [−100, +2,543] | +2,025 [+791, +3,259] |
| personal_sources | state × age | −1,453 [−3,131, +225] | +2,496 [+366, +4,625] | +1,043 [−1,190, +3,276] |
| personal_sources | **metro × age** | **−1,242 [−2,865, +381]** | **+2,305 [+250, +4,361]** | **+1,063 [−1,117, +3,244]** |

At 4 age bands the age-only first-to-third-plus narrowing is +$2.0k and its interval excludes
zero under both allocation rules. Holding state fixed cuts it to +$1.0k–$1.2k with the
interval spanning zero; holding *metro* fixed leaves it there, at +$1.1k–$1.3k. The single
contrast that survives geographic matching is third-plus minus second generation, positive
and interval-excluding-zero under all three standards. The first-to-second step reverses sign
once place is held fixed, though its interval contains zero. [INFERENCE]

Metro matching therefore does not rescue the cross-sectional narrowing claim, and it does not
kill it either. It reproduces what state matching already showed, which is the substantive
finding: the geographic confound operates at the state level, and going finer does not move
the answer.

## 5. Single-metro common-age gaps

4 age bands, each metro's own white age shares, 95% intervals, dollars per standardized
person. Union = the three generations combined.

| Scenario | Metro | Union vs white | Union vs all natives |
|---|---|---|---|
| all_age_shared | Los Angeles | −17,196 [−21,144, −13,249] | −8,028 [−10,177, −5,879] |
| all_age_shared | Chicago | −11,838 [−14,888, −8,788] | −8,344 [−10,762, −5,926] |
| all_age_shared | Dallas–Fort Worth | −9,823 [−13,311, −6,334] | −6,016 [−8,297, −3,735] |
| all_age_shared | Riverside–San Bernardino | −8,621 [−14,519, −2,723] | −3,684 [−6,492, −877] |
| all_age_shared | Houston | −7,493 [−10,939, −4,048] | −4,293 [−6,274, −2,313] |
| all_age_shared | Phoenix | −6,721 [−11,141, −2,301] | −4,089 [−7,254, −923] |
| personal_sources | Los Angeles | −18,053 [−22,283, −13,822] | −8,503 [−10,558, −6,447] |
| personal_sources | Chicago | −11,806 [−14,768, −8,843] | −8,447 [−10,871, −6,023] |
| personal_sources | Riverside–San Bernardino | −10,166 [−16,133, −4,198] | −5,667 [−9,346, −1,987] |
| personal_sources | Dallas–Fort Worth | −8,950 [−12,220, −5,681] | −6,376 [−8,658, −4,094] |
| personal_sources | Houston | −8,106 [−11,682, −4,529] | −5,050 [−7,227, −2,874] |
| personal_sources | Phoenix | −6,722 [−11,450, −1,994] | −4,294 [−7,605, −984] |

Every union interval in all twenty-four metro × reference × scenario combinations excludes
zero and is adverse. Los Angeles is roughly three times the national metro-matched figure
against the local white reference, which is the same pattern the state lane found for
California as a whole, sharpened. [INFERENCE]

Per-generation single-metro rows are in `derived/metro_matched.csv` (`cells` =
`<metro>_age_4`). Several of those per-generation intervals do cross zero, notably third-plus
self-identified in Chicago (−$6,100 [−$12,892, +$692], shared) and in Phoenix (−$4,461
[−$9,598, +$677]); at a single metro × single generation × 4 bands the samples are small
enough that the estimator cannot separate them from the local white reference.

## 6. Populations

`derived/metro_populations.csv` carries records, full-weight population, minimum cell record
count and minimum cell population over all 161 weight vectors, for every metro group × target
group, at both the as-defined 23-group stage and the retained 20-group stage.

Retained-stage totals: 5,631 Mexico-born records (12.22m), 6,349 second generation (14.33m),
6,351 third-plus self-ID (14.34m), 18,331 union (40.90m), 73,873 third-plus NH white
(173.05m), 119,938 all natives (283.67m).

Largest Mexican-origin metro groups by union population: `rest_metro` 8.76m, Los Angeles
4.50m, `ca_other_metro` 4.38m, Riverside 2.41m, `tx_other_metro` 2.17m, `rest_nonmetro`
2.17m, Houston 2.05m, Dallas 1.88m, Chicago 1.74m, `swil_other_metro` 1.59m, San Antonio
1.37m, Phoenix 1.41m.

Two border metros are the reverse case: McAllen holds 0.81m Mexican-origin people against a
third-plus NH white reference of 0.06m (17 records), and El Paso 0.70m against 0.09m (28
records). They clear the positivity gate but their local white benchmark is close to
non-existent, which is why they are not in the single-metro table.

### Merges

| Merged | Into | Trigger |
|---|---|---|
| San Jose | `ca_other_metro` | `mexico_born` band 0 (age 0–17): 0 records |
| California non-metro / unidentified | `ca_other_metro` | `mexican_second_gen` band 3 (65+): 0 records |
| Texas non-metro / unidentified | `tx_other_metro` | `mexico_born` band 0: 0 records |

Each failed the brief's positivity gate outright with an empty cell, not marginally.

### Sparsity, the real limit

Under the retained 20-group geography the thinnest key-group cells rest on a **single CPS
record**: Houston `mexico_born` age 0–17 (1 record, 2,980 full-weight persons), McAllen
`third_plus_nh_white` age 0–17 (1 record, 2,517), San Antonio `mexico_born` age 0–17 (1),
Denver `mexican_second_gen` age 0–17 (1). The brief's gate is positivity in all 161 weight
vectors, which these pass, but the underlying samples are thinner than the state standard's
by two orders of magnitude (state × age minimum: 24 records, 48,091 persons).

`metro_x_age_4_rf5` therefore repeats the whole metro standard under an additional
5-sample-record floor per key group × cell, which retains 10 metro groups (Los Angeles,
Riverside, San Francisco, `ca_other_metro`, `tx_other_metro`, Phoenix, `swil_other_metro`,
`swil_nonmetro`, `rest_metro`, `rest_nonmetro`) and merges Houston, Dallas, San Antonio,
Austin, McAllen, El Paso, Chicago, Denver, Las Vegas, San Diego, San Jose and the two
non-metro residuals upward. It moves nothing: union vs white −5,872 (shared) and −5,965
(personal) against −5,797 and −5,900 on the primary geography; G3+ − G1 +1,172 and +970
against +1,282 and +1,063. The metro result is not an artifact of the one-record cells.

## Gates

| Gate | Result |
|---|---|
| (a) Every key group × cell positive in all 161 weight vectors | **PASS** on all four standards. Minimum population over 161 vectors under metro × age: `mexico_born` 601.2 (1 record), `mexican_second_gen` 513.0 (1), `mexican_third_plus_selfid` 4,490.1 (5), `third_plus_nh_white` 1,358.6 (1), `all_native` 37,923.3 (27). Under the rf5 arm: 7,974.5 / 4,099.7 / 4,672.4 / 101,310.7 / 416,702.6 |
| (b) Collapse to one geography group, ORIGINAL 8 bands, reproduces stored results | **PASS**. Max `gap_total` residual $3.05e−5 (tolerance $1); every `standardized_gap_per_person` residual exactly 0.0 (tolerance $0.001); 20 anchors across both scenarios |
| (c) Self-reference contrast vanishes on the joint metro cells | **PASS**. Max abs gap 0.0, max abs gradient 0.0, both scenarios |
| (d) 4-band vs 8-band age-only union `gap_total` | **Reported, not gated**, as the brief instructs |

Gate (d) values, union `gap_total` in $bn:

| Scenario | Reference | 4 bands | 8 bands | Difference |
|---|---|---|---|---|
| all_age_shared | third-plus NH white | −291.29 | −290.59 | −0.70 |
| all_age_shared | all natives | −215.29 | −215.00 | −0.30 |
| personal_sources | third-plus NH white | −248.88 | −240.01 | −8.87 |
| personal_sources | all natives | −189.79 | −190.63 | +0.83 |

**Why they differ.** A matched `gap_total` is Σ_cells [target balance − (n_target/n_ref) ×
reference balance]. Refining a partition leaves that invariant only if the reference's
per-person balance is constant inside each coarse cell, which it is not: within 18–44, for
example, the white reference's net balance rises steeply with age while the Mexican-origin
age distribution inside the band is younger. Collapsing 8 bands to 4 therefore discards the
within-band composition and shifts the total. The shifts are small (0.1–0.4% of the total)
except `personal_sources` vs white at −$8.87bn (3.7%), where the within-band earnings
gradient is steepest because taxes sit on the recorded earner rather than being spread across
the SPM unit. All are far inside the ±$19bn union standard error. [INFERENCE]

All of the above is recorded in `derived/audit.json` with SHA-256 hashes of the CPS ZIP, the
MEPS file and SAS positions, the state parameter table, the upstream modules, the stored
`estimates.csv` anchor, `common.py`, `geo.py` and `metro_tests.py`.

## Scope limits

- **CBSA suppression.** 24.1% of CPS records carry `GTCBSA = 0` — non-metro plus metro areas
  Census suppresses for confidentiality. Those records are pooled into the state's "non-metro
  or unidentified" group, which mixes genuinely rural residents with suppressed-metro urban
  ones. Two of those three pooled groups had to be merged away for emptiness, so some of the
  suppressed-metro population ends up inside a state's "other metro" group. The metro
  standard is therefore an approximation of geographic matching, not an exact one.
- **Coarser age bands.** 4 bands, not the source lane's 8, to keep cells estimable. Gate (d)
  measures what that costs at the age-only standard: 0.1–3.7% of the union total. The three
  standards in every table above are compared at the *same* 4 bands, so the comparison across
  standards is clean even though none of them is directly comparable to the stored 8-band
  numbers.
- **Thin cells.** See [Sparsity](#sparsity-the-real-limit). Several retained cells rest on
  1–4 CPS records; the rf5 robustness arm shows the conclusions do not depend on them.
- **Nominal dollars, no price-parity adjustment.** Every figure is nominal. Coastal
  California metros carry regional price levels well above the national average and border
  Texas metros well below it [TRAINING-DATA: BEA regional price parities, not fetched or
  checked in this lane], so a nominal per-person gap in a high-cost metro overstates the real
  resource gap and a low-cost metro understates it. No regional price parity is applied
  anywhere, in either this lane or the source lane, and none of the cross-metro differences
  above are adjusted for it. The single-metro table should not be read as a real-terms
  ranking across metros.
- **No causal content.** These are matched descriptive contrasts conditional on the source
  lane's model: modeled rather than observed taxes, MEPS donor medical means, mixed-source
  state parameters, a partial account omitting corporate tax and pure public goods, and
  cross-sectional generation groups rather than linked families. Nothing here identifies a
  causal effect of immigration or a marginal fiscal response.
- **Intervals.** Pointwise normal 95% intervals conditional on fixed standard shares and
  model parameters, CPS replicate and MEPS donor variance added as first-order independent
  components. Not simultaneous over the 160 standardized-gap rows reported.
- **Geography is residence, not history.** A metro group is where a person lived in March
  2025. It carries no information about where they were educated, where their parents lived,
  or how long they have been there.

## Files

Covered, all under `infra/immigration-fiscal/metro_match_2026_09_17/`:

- `geo.py` — household CBSA merge, the 23 metro rules, the 4-band age standard, and the
  upward-merge resolver
- `metro_tests.py` → `derived/metro_matched.csv` (480 rows), `derived/metro_generation_contrasts.csv`
  (24 rows), `derived/metro_populations.csv` (258 rows), `derived/audit.json`
- `README.md`, this file

Read, not modified: `ledger_stress_2026_09_17/{README.md,RESULT.md,common.py,test1_state_matched.py,test1b_generation_contrasts.py}`,
`all_age_ledger_2026_09_17/{analyze.py,estimator.py,derived/estimates.csv}`,
`gen_ledger_extension_2026_09_16/extend_ledger.py` and its cached CPS ZIP.

Skipped, and why:

- **Head-weighted arms.** `common.setup()` rebuilds `head_weights`, but the brief fixes every
  statistic to person weights, as both stress tests do. Not run.
- **8-band metro cells.** Not attempted; at 8 bands the metro cells are empty for the target
  groups in most metros, which is why the brief specifies 4.
- **McAllen and El Paso single-metro rows.** Computed and present in
  `derived/metro_matched.csv` under the primary geography, but deliberately not promoted to
  the single-metro table: their local white reference is 17 and 28 records. The brief's
  six-metro list does not include them.
- **No commits.** Nothing outside this directory was written.
