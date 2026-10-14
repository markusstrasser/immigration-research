**Verdict:** The observed-take-up SNAP survivor response is a bounded **arm**, **−$2.342bn to −$0.477bn** on the primary union-plus-located-latent departure rule. The envelope combines shelter-zero/cap assumptions with low/high observed CPS take-up; it is a structural arm range, not a confidence interval. All four primary arm values and their 160-replicate SEs are retained. The original union-only envelope is **−$2.631bn to −$0.528bn**. [CALCULATION: `snap_arm.py`; `derived/snap_arm_latent_results.json`, `snap_arm_results.json`]

Covered: SNAP survivor financial rules, observed CPS take-up, explicit pooled cells, newly eligible/ineligible spending, all 161 columns, located latent biological-child departure. Skipped: Medicaid/CHIP/PTC, M1/M2/M3/M5/M6 own-cost accounting, added-person residual transport and unified removal headline, owned by peers. Original `benefits.py` was reused without editing.

| SNAP removal correction, $bn | Primary departure mask | Replicate SE | Original union | Replicate SE |
|---|---:|---:|---:|---:|
| Zero shelter, low take-up | −1.964814 | 0.208721 | −2.195441 | 0.218580 |
| Zero shelter, high take-up | −2.342106 | 0.235122 | −2.631240 | 0.245841 |
| Capped shelter, low take-up | −0.477360 | 0.151481 | −0.527782 | 0.150981 |
| Capped shelter, high take-up | −0.629939 | 0.159199 | −0.707893 | 0.159310 |

Both end specifications use the same SNAP spending key and response 1; these components therefore apply equally at each end, set and cash. All correction vectors are 3×161 with generations G1/G2/G3+. Positive raises the removal net cost; additional benefits for surviving nonmembers lower it. [DATA: `derived/case_inputs.json` `evaluated`; `derived/snap_arm_latent_replicates.csv`]

The primary mask adds **517,863.293** located latent biological children to the departure mask, using the shared `membership.latent_mask` predicate; their generation owner is G3+. It preserves the row-4 39.71M CPS person weights and the original union's positive-control allocation. It adds no population or own fiscal cost: matching the located subset to existing added-person costs and transporting the remaining latent pool remains the parent driver's responsibility. [DATA: `membership.py`, `latent_mask`; `snap_arm.py`, `--membership latent`; CALCULATION: `snap_arm_latent_results.json`]

## Newly eligible and newly ineligible

| Primary mask, $bn | Zero shelter | Capped shelter |
|---|---:|---:|
| Newly eligible nonparticipants, low take-up | −0.993542 | −0.401089 |
| Newly eligible nonparticipants, high take-up | −1.370834 | −0.553667 |
| Prior recipient loses financial eligibility | +0.219341 | +0.267711 |

These are separate components of the full response. Remaining changes arise from current recipients' amount changes and the survivor baseline allocation. They must not be added to the full response again. With zero shelter, **655,717** unit events become financially eligible (939,598 surviving people) and **78,922** become ineligible (115,452 people). Observed take-up implies 136,215–189,872 newly enrolled previously nonparticipating unit events. With capped shelter, the respective unit-event counts are 379,654 and 270,286, with 42,455–57,830 new enrollments. These are proxy assistance units weighted by the original mean person weight, not legally adjudicated households or administrative enrollment observations. [CALCULATION: `derived/snap_arm_latent_results.json` `diagnostics`; ASSUMPTION: SPM-unit proxy]

## Rules and take-up

The helper reuses `benefits.rules`, `snap_rule` and `sized`: primary parsed federal income tests, deductions and maximum benefits, 9 months FY2024 plus 3 months FY2025. No new legal constants were typed. Annual household incomes stand for steady monthly incomes; departing members' own income leaves, the SPM residual stays, and the existing unit deduction totals are proportional to surviving persons. Shelter is zero or capped as separate arms. [DATA: `benefits.py` and its pinned primary USDA/CFR sources; ASSUMPTION]

Take-up is observed `SPM_SNAPSUB > 0` among units passing the before-removal financial proxy, at the survivor state's and size category's cells. Reference cells use original unit size; destinations use surviving size. Rates are weighted by original unit event weights. Low/high are the full-sample empirical rate ± one 160-replicate SDR SE, clipped to [0,1], then held across outcome replicates. Thus the arm width includes a take-up uncertainty choice, while each component SE conditions on that fixed arm. [CALCULATION: `observed_takeup`]

Size bins are 1/2/3/4+. A cell needs 20 eligible sample units; an explicit pooling hierarchy is state/size → state → region/size → national/size → national. Every selected tier, sample support, rate, SE and bound is written in the result. The actual primary zero-shelter arm uses state/size or state pools; capped shelter uses state/size throughout. A nonpositive replicate denominator or unsupported final pool blocks. Signed survey replicates are retained. [CALCULATION: `observed_takeup`; `snap_arm_latent_results.json` `diagnostics.takeup_cells`; ASSUMPTION: support threshold and pooling]

Observed recipients retain `observed benefit + rule(after) − rule(before)`, floored at zero and capped at the new maximum. A genuine financial-eligibility loss (`rule(before)>0`, `rule(after)=0`) ends their benefit. Prior observed recipients failing both financial proxies retain their disclosed Census residual; the model does not silently relabel them as newly ineligible. Previously nonparticipating units begin only when they become financially eligible, at the observed take-up bound. Previously eligible nonparticipants remain nonparticipants; this preserves no-event identity. [CALCULATION: `after_benefit`; ASSUMPTION]

The helper inherits the original benefit lane's national SNAP price conversion and household fraction, exactly reproduces its original union allocation, and attributes each weighted unit-event change to departing generations by their weight shares. This conserves national and generation totals in all 161 columns without changing any person's weight. Assets, BBCE, ABAWD, students and immigration/legal eligibility remain unobserved. Alaska mixed units and units containing a noncivilian are explicitly excluded, matching the original SNAP arm. Recommend **arm**, not a measured entitlement correction. [DATA: `compute`; `benefits.attribute`; ASSUMPTION / SCOPE]

## Integration and verification

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/mixed_unit_removal_2026_10_14/snap_arm.py --arrays-out infra/immigration-fiscal/mixed_unit_removal_2026_10_14/_cache/snap_arm_arrays.npz
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/mixed_unit_removal_2026_10_14/snap_arm.py --membership latent --out infra/immigration-fiscal/mixed_unit_removal_2026_10_14/derived/snap_arm_latent_results.json --arrays-out infra/immigration-fiscal/mixed_unit_removal_2026_10_14/_cache/snap_arm_latent_arrays.npz
```

Terms contain `SNAP_{zero|cap}_observed_{low|high}_takeup`, plus `observed_newly_eligible_{low|high}` and `observed_newly_ineligible`. Use a fresh subprocess for bounded memory; all 3×161 arrays are available in the NPZ, and identical vectors are tracked in the corresponding `derived/*replicates.csv`. `compute(..., baseline_union=original_union)` supports the parent frame directly. [DATA: callable/CLI contract]

Six tests pass: weighted observed rates, original-size reference cells, declared sparse-cell pooling, missing support fails loudly, residual identity, eligibility starts/losses and signed-denominator handling. Union runs reproduce numeric results exactly; the final union run took 13.61s, peak RSS 1.50GB. The first latent run took 12.30s, peak RSS 1.93GB. Timing/memory use Python `time.perf_counter`/`resource.getrusage`. The parent's full-lane byte replay and unified headline remain separate checks.
