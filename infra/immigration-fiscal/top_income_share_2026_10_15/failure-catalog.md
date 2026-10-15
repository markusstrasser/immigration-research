# Measurement failures guarded by this lane

| Failure | Guard / regression |
|---|---|
| Applying row4 before the IRS rake and again through the case stack | Published-weight key reproduces heldout to 1e-12; supplementary row4 count separately gated; `test_pool_cps.py` |
| Assuming aligned replicate numbers measure cross-year covariance | One-year-at-a-time perturbations, independence estimate and maximum-positive-covariance bound; `test_pool_cps.py` |
| Missing/changed raw source, unmatched person or unsupported income cell | Pinned Census source hashes, validated replicate join, fail-loud IRS/CBO support; pool and federal tests |
| Treating SCF implicates as independent families | Five-implicate/ID validation and deduplicated family counts; `test_outside_checks.py` |
| Combining SCF extracts with silently changing price bases | Reconstruct nominal raw income from Fed macro; compare against existing official 2022 summary; outside tests |
| Substituting an older working paper for final published tables | Version mismatch preserved in `outside-note.md`; final-paper numbers excluded as UNVERIFIED |
| Calling federal liabilities or SALT deductions state PIT | Actual FTB liability table and object gates; `test_state_correction.py` |
| Attributing all CA administrative reshaping to the upper share | `current_CA_admin` control and separate share changes in `state_arms.json` |
| Calling an isotonic fit an independent aggregate confirmation | Weighted-mean conservation regression in federal/state tests and `test_v8.py` |
| Pricing stale case ends or missing set/cash/post-engine corrections | Full-precision v8 principal and exact set/cash baseline/receipt-cost closure gates; `test_v8.py` |
| Losing temporal or memory evidence when macOS time cannot inspect processes | `run_all.py` uses perf_counter/getrusage, date timestamps, return-code and 2.5GB checks |

Source numbers, missing estimates and transport assumptions stay distinct in `RESULT.md`.
