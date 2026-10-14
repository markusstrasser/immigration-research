**Verdict:** Credit ownership transfers preserve the identified union and national amounts. On the mean of both methods, convention (a) moves $9.657bn of net cost out of G1; convention (b) moves $0.458bn out. The reviewer's $13–20bn estimate is not reproduced after SSN, hotdeck, OTA and PTC corrections. Final validation is recorded below.

Owned files: `credit_routing.py`, `test_credit_routing.py`, `derived/credit_routing.json`, `inputs/credit_pins.json`, this evidence file, and ignored replay/cache files in this lane. Other workers own the runner and route contract.

[CALCULATION: `credit_routing.py` → `derived/credit_routing.json`] The helper keeps the identified union and national corrected amounts fixed while moving child-related credit amounts among its generations. Childless EITC and Marketplace premium credits retain their existing owners.

| One change from central, $bn, mean methods | G1 | G2 | G3+ |
|---|---:|---:|---:|
| (a), refundable spending | −6.859595 | +2.567093 | +4.292502 |
| (a), federal income-tax receipts | +2.797340 | −0.656576 | −2.140764 |
| (a), net cost at both personal ends, set and cash | −9.656935 | +3.223669 | +6.433266 |
| (b), refundable spending | −0.301511 | +0.197342 | +0.104169 |
| (b), federal income-tax receipts | +0.156559 | −0.041564 | −0.114995 |
| (b), net cost at both personal ends, set and cash | −0.458069 | +0.238906 | +0.219164 |
| (a), SDR SE of net change, mean methods | 1.345770 | 1.055329 | 0.598380 |
| (b), SDR SE of net change, mean methods | 0.240822 | 0.252752 | 0.121583 |
| R6 only, (b) corrected minus previous (a) tags, net cost | +0.929885 | −0.337468 | −0.592417 |
| R6 only, SDR SE of net change | 0.143929 | 0.166817 | 0.105425 |

[CALCULATION: `derived/credit_routing.json` `base`; federal rows use `treasury_815`, the personal-end scenario.] The $5bn redistribution bar is cleared for G1(a) and G3+(a). The headline, the 39.71M identified union and the 42.75M lineage total do not move. The added people's existing terms do not move in this helper; the parent handles their separate age-routing fix.

Rules and coverage:

- Base refundable amount on each linked return is split equally among its qualifying dependents, using `DEP_STAT` claimant links and the return's weights. Under (a), its union children take their own generations; under (b), they take `frame.assignments` (co-resident union parents or the declared family fallback). Only within-union transfers occur here. The portion belonging to an outside-union dependent retains its union claimant; item 5b covers the separate removal-boundary term. [ASSUMPTION: equal allocation of observed return-level dollars among qualifying children; individual child tax dollars are not observed.]
- The raw refundable transfer is carried through the exact five-seed matched and pooled hotdeck runs and the adopted row-4, state-aware SSN/onbooks vectors. The ratio method follows `stack_split.py`'s mean-matched-minus-mean-pooled formula, not a mean of seed ratios. [DATA: `cps_imputation_keys_2026_09_23/_cache/hotdeck_key_shares.npz`; `generation_account_2026_09_24/derived/stack_by_generation.json`.]
- Row 1 removes the rerouted credit share from PTC while preserving the exact rounded booked amount. Marketplace persons stay with their existing owners. OTA uses its own source frame's SSN rule and EITC/CTC ratios, not a substitute state-aware flag. [DATA: `dataset_integrity_2026_09_23/derived/spending_mts_credits.json`; `external_benchmarks_2026_09_24/derived/ota_shares.csv`; `generation_account_2026_09_24/derived/external_by_generation.json`.]
- Nonrefundable Census CTC/other-dependent credits and modeled dependent-care credits follow the dependents, with the source lane's state-aware onbooks factors and IRS-raked personal receipt key. The high-AGI scenario uses item 5b's declared scenario scaling. [CALCULATION: `mixed_unit_credits_2026_10_14/credits.py`, its reproduced `per_fit`, `base.ctc`, `base.cdcc0`.]
- R6 parts are routed jointly by the original dependent generation and the convention-(b) parent generation. A product of return-level marginal owner shares would erase which original child has which parent; the regression test rejects that error. Each `r6_b_parts` row keeps the exact original frozen part identity and conserves its amount. [CALCULATION: `route_r6`; `test_r6_keeps_joint_old_and_new_child_owners_on_mixed_return`.]
- `average_net_cost_se` combines the two method replicate vectors before estimating SE and preserves spending/receipt covariance. `r6_b_net_shift` does the same for the change of R6 ownership. These are survey SDR SEs conditional on the five fixed hotdeck seeds, not total imputation uncertainty. [CALCULATION: `sdr`, `credit_routing.json`.]

Limitations: the hotdeck changes `FEDTAX_BC` but does not persist/recompute a child-specific CTC/care decomposition. Receipt transfers therefore use the observed base return's CTC plus the source lane's modeled care credit, with final IRS/onbooks rules. The refundable routing is an exact replay of the stack's vectors; the receipt-credit decomposition remains the source lane's model and attribution assumption. Disability exceptions for care eligibility are not identified in the public fields. These limits are explicit in the JSON; the helper does not label child-level dollar allocation observed.

Validation log:

- 2026-10-14 21:32:50 JST (`date`): 10 raw hotdeck source shares reproduce to 1e-12; both complete row4/SSN refundable stack payloads reproduce to 1e-9; OTA union reproduces to 1e-9; source item 5b's 18 parts reproduce to 1e-9. The source replay passes its original 83 gates. Helper all-replicate zero-sum worst residual: 4.44e-14bn.
- Profiling: the first full replay retained irrelevant source locals and constructed all row4 sensitivity matrices, with peak 2.85GB. Selecting needed source locals, projecting generation-frame reads and constructing only the adopted weight arm reduces measured peak to 1.573GB. The concurrent full run took 170.695s, mostly ten 6–18s hotdeck runs. The final code also removes a redundant second raw-CPS load. A provenance-keyed cache makes unchanged reruns fast without dropping seeds or weakening controls.
- Final source replay: exit 0, 91.960s, peak 2,280,636,416 bytes (under 2.5GB), 112 helper gates plus the source's 83. Final tests: `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/generation_account_2026_09_24/test_credit_routing.py -q` → 6 passed in 0.70s.
- Cached deterministic repeat: exit 0, `credit_routing.json` SHA256 identical; 0.932s including subprocess startup, peak 97,353,728 bytes. The parent includes `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/credit_routing.py` in the final whole-lane `rerun_lane.py` command, because other workers still own/write the remaining runner outputs.

Owned changed paths (lane-relative; replay files are ignored):

- `credit_routing.py`
- `test_credit_routing.py`
- `derived/credit_routing.json`
- `inputs/credit_pins.json`
- `credit-evidence.md`
- `_cache/credit_routing/sufficient_statistics.json`
- `_cache/credit_routing/source_replay/allocation_check.csv`
- `_cache/credit_routing/source_replay/terms.csv`
- `_cache/credit_routing/source_replay/example.json`
- `_cache/credit_routing/source_replay/validation.csv`
- `_cache/credit_routing/source_replay/summary.json`
- `_cache/credit_routing/source_replay/item.json`
- `__pycache__/test_credit_routing.cpython-313-pytest-9.1.1.pyc` (ignored test compilation)
- `__pycache__/credit_routing.cpython-313.pyc` (ignored test import compilation)

Skipped: runner, route contract, age/state routing and common RESULT files, owned by other workers. Frozen upstream lanes and Git metadata are untouched.
