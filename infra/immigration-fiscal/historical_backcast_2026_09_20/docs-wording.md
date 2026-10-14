**Status — 2026-10-15:** Earlier oct14/P7 replacement passages below are superseded and retained as historical records. Use the final "Current replacement wording" section for the live fixed2%/3%, per-part-income joint stack.

**Verdict:** Replace the programme-series claim with wording that distinguishes the actual live base from the beside programme rule. The frozen central series has not been replaced.

## Memo: current live rules

These are model back-casts in 2024 dollars, not measured historical accounts. The `ratio` rule carries a whole-budget base with national current receipts and all current expenditures, with the group's 2024 ratios held fixed. Separately carried corrections follow their own national line series and population paths; public-capital returns follow net-stock series at fixed 2% / 3%. The current `income` rule scales only the base receipts by measured ACS relative income; the carried corrections are unchanged. `flat` holds 2024 cost per member fixed, with added descendants on the identified G3+ count path. Across these live rules, 2015–2024 is $3.0–4.0tn. [DATA: `derived/oct14/backcast_windows.csv`; ASSUMPTION]

## Memo: controlled corrections beside

Historical real ten-year yields floored at zero at the low end (high fixed 3%), a spending base excluding defence, interest and subsidies, and income scaling on all separately carried income-linked parts give $2.8509–3.7536tn (`ratio`) and $3.1185–4.0089tn (`income`) over 2015–2024. The flat-with-historical-rate arm is $2.9850–4.0185tn. Each year's measured yield is used including 2024, so this sensitivity moves the 2024 low anchor as well; the change is shown separately and is below $5bn. These are beside sensitivities, not the adopted annual fiscal case. [CALCULATION: `derived/p7/windows.csv`; ASSUMPTION]

## Memo: programme beside rule

The v7 `programme` rule carries every charged spending and receipt line with its national programme or tax series, payroll-earned pension accrual with contribution series, capital returns with stocks at fixed 2% / 3%, production with real GDP and population shares, and constants per person. With measured pandemic payment shares, historical school-age shares and available 2019–2024 coverage shares, it gives $3.2555–3.9536tn for 2015–2024, or $3.4567–4.1398tn under `programme_income`. Medicaid before 2019, fee and capital-use keys stay at 2024. Added non-identifying descendants follow measured G3+ population/use proxies. Both programmes reconcile to the 2024 v7 specifications at the personal allocation; their historical group shares remain modeled. [CALCULATION; ASSUMPTION]

## FAQ 8: replacement passage

The $3.0–4.0tn over 2015–2024 is a model back-cast across the current whole-budget `ratio`, base-receipt `income` and per-person `flat` rules. It is not a historical fiscal ledger: the base follows national whole-budget totals and separate corrections follow line series. The three corrected rules beside give roughly $2.9–4.0tn; the programme-by-programme versions with measured pandemic shares and available yearly use keys give $3.2555–3.9536tn (or $3.4567–4.1398tn with income scaling). Public-capital returns and accrued pension promises are inside these resource-cost totals, so they cannot be described as accumulated government borrowing. [CALCULATION; ASSUMPTION]

## Round-2 corrections — 2026-10-15

The adopted payloads differ from the candidate's only in their stamps: meta.adopted "2026-10-15", status
"adopted: main case v8; ...", case "...; v8 adopted"; summary.json v8.status "adopted". Every number is unchanged.
A pin you took on the candidate's corrections.json / corrections_cash.json / summary.json bytes must be refreshed
to the committed bytes (verify the numbers match, then re-pin; never enrol silently).

REQUIRED before your phase 2: read the amendment file for your lane name; it changes your phase 2.
- p8-prop-a: already delivered by resume (note_a8_phase2.md); nothing new.
- p8-prop-b: /private/tmp/claude-501/-Users-alien-Projects-immigration-research/75b08f57-63cc-4e3d-96dc-60050327b5c1/scratchpad/prop8/note_b8_r2b.md
- p8-prop-d: nothing new (note_d8_r2.md and note_d8_r2b.md stand).`.

| Rule/scenario | 2015–2024 low / high, $bn | 74ce1f67 comparison low / high, $bn | Change low / high, $bn |
|---|---:|---:|---:|
| ratio: live_fixed_resource_rates | 3597.709115 / 4350.283007 | 2850.858677 / 3753.615749 | +746.850438 / +596.667258 |
| income: live_fixed_resource_rates | 3906.869647 / 4647.415995 | 3118.521350 / 4008.904121 | +788.348297 / +638.511874 |
| flat: live_fixed_resource_rates | 3485.772136 / 4338.405633 | 2984.959801 / 4018.492547 | +500.812335 / +319.913086 |
| programme: v7_measured_programme_overlay_beside | 3515.606037 / 4268.925394 | 3255.471617 / 3953.588138 | +260.134420 / +315.337256 |
| programme_income: v7_measured_programme_overlay_beside | 3758.381245 / 4496.968549 | 3456.748965 / 4139.786677 | +301.632280 / +357.181872 |
| joint: live_programme_measured_per_part_income | 3758.381245 / 4496.968549 | 3118.521350 / 4008.904121 | +639.859895 / +488.064428 |
| joint: programme_measured_before_unit_income | 3720.764203 / 4459.351507 | 3118.521350 / 4008.904121 | +602.242854 / +450.447386 |
| income: before_unit_income_fixed_rates | 3869.252606 / 4609.798954 | 3118.521350 / 4008.904121 | +750.731256 / +600.894832 |
| income: median_earnings_proxy_beside | 3917.674886 / 4658.221234 | 3118.521350 / 4008.904121 | +799.153536 / +649.317113 |
| income: wage_only_worker_split_beside | 3890.729557 / 4631.275905 | 3118.521350 / 4008.904121 | +772.208207 / +622.371783 |
| ratio: previous_unit_income_dfii10_stack | 3098.144149 / 4066.718388 | 2850.858677 / 3753.615749 | +247.285471 / +313.102638 |
| income: previous_unit_income_dfii10_stack | 3369.687639 / 4326.234334 | 3118.521350 / 4008.904121 | +251.166289 / +317.330212 |
| flat: previous_unit_income_dfii10_stack | 3237.338708 / 4338.405633 | 2984.959801 / 4018.492547 | +252.378907 / +319.913086 |
| ratio: financing_cost_dfii10_floor0_beside | 3374.759810 / 4350.283007 | 2850.858677 / 3753.615749 | +523.901133 / +596.667258 |

Capital-rate correction on the same ratio account, financing-cost DFII10 → fixed resource rates, $bn over2015–2024:

- low: 3374.759810 → 3597.709115 (+222.949305).
- high: 4350.283007 → 4350.283007 (+0.000000).

Income-linked carried-component change (before unit elasticity → after per-part rules), $bn over 2015–2024:

- low: -26.099349 → +11.517692.
- high: -38.126894 → -0.509852.

Own-formula PIA response derived from the pension lane, with its careers and vesting rules:

| Group | PIA earnings elasticity at 2024 | Mean AIME / first bend point |
|---|---:|---:|
| union | 0.557993 | 3.590069 |
| g1 | 0.566128 | 2.947100 |
| g2 | 0.557955 | 3.966727 |
| g3plus | 0.550857 | 4.037374 |

Part A has zero earnings elasticity conditional on covered workers: its transport follows under65 workers per member. Earned OASDI follows all positive-tax workers per member times the finite benefit-formula response. Current cash offsets retain benefit/use rules. Retiree-health national function price swaps carry no additional individual earnings elasticity. Legal/on-books participation adjustments are held assumptions. CPS earned-income proxies do not identify an exact ACS split into workers and earnings: ACS nonlabor income, survey composition, work-spell age and legal coverage remain unmatched.

Changes against74ce1f67 include v7→v8 propagation and round-2 rules. The previous_unit_income_dfii10_stack rows price the old74ce1f67 rule on the same v8 components, including its2024 financing-rate movement, to isolate that distinction.

2024 lineage: 45.2301 million. Annual anchors/per-member gates: 1e-4bn/$0.01; explicit component closure: 1e-9bn. Fixed capital and pension-rule regressions are in test_backcast.py. Programme paths replace the broad charged-base scaling and retain fixed resource rates, with new items on their own typed series.
[CALCULATION: derived/oct15/round2_windows.csv, round2_income_parts.csv, round2_pension_audit.json; ASSUMPTION: fixed legal/on-books adjustment; pre2019 fixed relative worker coverage and unsplit ACS earnings proxy]

The live joint stack starts with programme spending, then measured EIP shares, historical school/Medicaid use and per-part income. The broad charged-base correction stays a diagnostic because programme paths replace that same expenditure scaling. New completion/coverage school and Medicaid pieces receive their known source use keys. The old v7 programme displacement is transported onto v8. Item11 now uses its exact source r0 programme/generation split, including income and state taxes, non-EIP refundable credits, Medicaid, ACA, SNAP, property, housing and consumption. Its D_added residual remains a separate G3+ lineage part. The preserved consumption aggregate uses a declared national-receipt composite; historical allocations within that aggregate are unobserved. Unclassified coverage retains its declared population proxy. This remains conditional transport of the current programme scope rather than a reconstruction of historical statutes.

| Live branch: leave-one-branch-out → joint, $bn over 2015–2024 | Low before → after | High before → after |
|---|---:|---:|
| historical_school_medicaid | 3674.865731 → 3758.381245 (+83.515515) | 4399.484233 → 4496.968549 (+97.484316) |
| new_known_use_keys | 3756.522926 → 3758.381245 (+1.858319) | 4494.733985 → 4496.968549 (+2.234564) |
| pandemic_measured | 3809.227782 → 3758.381245 (-50.846536) | 4547.815085 → 4496.968549 (-50.846536) |
| per_part_income | 3515.606037 → 3758.381245 (+242.775208) | 4268.925394 → 4496.968549 (+228.043155) |
| precision_anchor | 3758.381415 → 3758.381245 (-0.000170) | 4496.968174 → 4496.968549 (+0.000375) |
| programme_spending | 3542.762307 → 3758.381245 (+215.618938) | 4286.603191 → 4496.968549 (+210.365358) |

Charged-base → programme replacement reconciliation (income branch excluded), $bn:

- low: original ratio 3265.459971 → charged ratio 3597.709115 (+332.249144) → programme 3515.606037; replacement -82.103078; maximum annual closure residual 2.84e-14.
- high: original ratio 4009.687317 → charged ratio 4350.283007 (+340.595690) → programme 4268.925394; replacement -81.357614; maximum annual closure residual 2.84e-14.

Exact item11 programme split and covered-G3+ count-path correction, replacing the previous aggregate tax proxy/count path together:

- low: 3768.372422 → 3758.381245bn (-9.991177). The count correction affects per-member denominators, not these cost totals. In the pre2024 fixture, the old path counts9.00 units and the corrected path8.72 units; the2024 anchor remains13.00. Actual covered-G3+2024 people690117.6475 now follow the same identified-G3+ path as their costs.
- high: 4504.665274 → 4496.968549bn (-7.696725). The count correction affects per-member denominators, not these cost totals. In the pre2024 fixture, the old path counts9.00 units and the corrected path8.72 units; the2024 anchor remains13.00. Actual covered-G3+2024 people690117.6475 now follow the same identified-G3+ path as their costs.

Missing school-age and Medicaid cells now fail by (key, group, income year); only absent Medicaid coverage before2019 is held. Deletion fixtures verify both a school cell and a 2021 Medicaid cell fail.

Added-descendant expenditure has an explicit gross base; all of it is separately priced by programme, leaving a zero residual broad base. Applying a second broad sigma would double count those components.
- low: gross added expenditure2024 $60.955268bn; separately carried $60.955268bn; residual $0; broad sigma before carrier exclusion would be $+4.431454bn over2015–24.
- high: gross added expenditure2024 $62.851571bn; separately carried $62.851571bn; residual $0; broad sigma before carrier exclusion would be $+4.569316bn over2015–24.
- Held-ratio descendants, low: live lineage–union gap $214.758353bn; an illustrative20% lower average ratio changes it by $-42.951671bn. Reviewer's earlier $169bn/$34bn illustration remains an illustration, not an estimated historical decline.
- Held-ratio descendants, high: live lineage–union gap $258.202950bn; an illustrative20% lower average ratio changes it by $-51.640590bn. Reviewer's earlier $169bn/$34bn illustration remains an illustration, not an estimated historical decline.
[CALCULATION: round2_programme_branches.csv, round2_added_expenditure_base.csv, round2_descendants.csv; ASSUMPTION: held descendants/identified-G3+ ratio]

Final validation receipts:

- bridge7: exit0, 27.584s, peak child RSS 0.455GB. See `/private/tmp/claude-501/-Users-alien-Projects-immigration-research/75b08f57-63cc-4e3d-96dc-60050327b5c1/scratchpad/prop8/backcast-bridge7.log`.
- producer7: exit0, 29.498s, peak child RSS 0.438GB. See `/private/tmp/claude-501/-Users-alien-Projects-immigration-research/75b08f57-63cc-4e3d-96dc-60050327b5c1/scratchpad/prop8/backcast-producer7.log`.
- tests3: exit0, 42.813s, peak child RSS 0.556GB. See `/private/tmp/claude-501/-Users-alien-Projects-immigration-research/75b08f57-63cc-4e3d-96dc-60050327b5c1/scratchpad/prop8/backcast-tests3.log`.
- orderfix: exit0, 0.466s, peak child RSS 0.131GB. See `/private/tmp/claude-501/-Users-alien-Projects-immigration-research/75b08f57-63cc-4e3d-96dc-60050327b5c1/scratchpad/prop8/backcast-orderfix.log`.
- rerun: exit0, 125.115s, peak child RSS 0.834GB. See `/private/tmp/claude-501/-Users-alien-Projects-immigration-research/75b08f57-63cc-4e3d-96dc-60050327b5c1/scratchpad/prop8/backcast-rerun.log`.
- Regression result: 42 passed in 42.33s.
- Physical-footprint gates before publication: native bridge0.596GB and latest back-cast0.484GB, below the shared2.5GB budget. Source scanning is streaming; deterministic audit bytes contain no timing or memory readings.
- The official seven-command gate sums required work. The measured stage receipts above identify the bridge, producer and full regression costs; worker extraction previously took23.550s and the longest individual regression fixture9.45s. The rerun harness records stage return codes but does not expose stage timing/stdout on success, so these are pre-rerun timings, not invented per-stage rerun measurements. No full rerun was repeated after exit0.
- The first official rerun exited1 with93/94 files unchanged: round2_income_parts.csv differed only in row order. All25,120 rows were exactly equal after canonical key sorting. The linked-set loops and writer now sort explicitly; the existing joint fixture verifies canonical CSV order. Failure log/timing are retained in backcast-rerun-failed-order.log and backcast-rerun-failed-order-timing.json; full original backup remains at /var/folders/td/k9yd1c8n5478my_42k9tb89h0000gn/T/rerun_m26uj0m4/lane. No values, rounding or gate tolerances were changed. The final rerun below validates the fix.
- The next attempt exited1 at the coverage source gate before comparing outputs: completion_keys.py and completion_jobs changed after the source freeze. Evidence is retained in backcast-rerun-failed-completion-source.log and its timing JSON; backup rerun_q6qcrk5w remains beside the first backup. No provenance gate was waived. The final recipe validates the exact original pricing arrays under the current source before rerunning.
- A subsequent bridge stopped when the authoritative cash recipe was refreshed between conversion and use. Re-conversion and repeated read-only pair checks passed: original set/cash compressed caches are exactly the owned replay bytes; every economic audit field matches, with only dependency_manifest_sha256 differing. This was a provenance update, not a cohort or price change. Stable source manifest hashes and both cache hashes are retained in backcast-contract-proof.json. The successful final bridge/source gate validates the current authoritative contracts.
- Official lane reproducibility: [rerun] IDENTICAL: 94/94 files unchanged (backup removed).

Covered: live oct15 set/cash, all typed items9–12, historical worker/pension and programme paths, archived-case byte-preservation fixtures and physical-memory gates. Earlier case outputs remain archived rather than being regenerated as live results. Raw source files were read only. Social and debt/uncertainty outputs remain the parent and sibling agents' responsibilities. The bridge physical probe executes bridge_memory.py dynamically; the official rerun exemption names only that demonstrated dynamic call, not a missing analysis command.

### Current replacement wording (earlier oct14/P7 passages superseded)

The live oct15 joint back-cast gives $3.7584–4.4970tn over 2015–2024, in 2024 dollars. It combines programme spending, measured pandemic shares, historical school-age and Medicaid use, and per-part income rules. Ratio, income and flat transports remain separately reported. It uses a spending base excluding defence, interest and subsidies and fixed 2% / 3% imputed capital returns. Income-linked receipts keep unit elasticity. Part A follows workers per member; OASDI follows workers times the finite PIA response to earnings per worker. Preserved CPS labor inputs measure earnings-positive worker/earnings proxies in income years 2019–2024 (ASEC surveys 2020–2025), under a held legal/on-books adjustment. Part A uses workers under 65 and OASDI uses all positive-tax ages. Earlier years keep relative worker coverage fixed and use ACS total income as an earnings proxy. This is not an exact split of ACS income. The added descendants' 2024 ratio to identified G3+ is held back in time, likely overstating early years by an unquantified amount. DFII10 financing costs and wage-only/median earnings proxies stay beside. The programme transport is conditional on the current scope and source keys. These resource costs include capital returns and earned pension promises; they are not observed historical fiscal ledgers or accumulated borrowing. [CALCULATION: derived/oct15/round2_windows.csv, round2_income_parts.csv, worker_income.csv; ASSUMPTION]
