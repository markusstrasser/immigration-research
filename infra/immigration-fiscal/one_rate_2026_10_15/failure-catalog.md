# Failure catalog

| Failure | Root cause | Guard and regression |
|---|---|---|
| First control read raised `KeyError: groups`; next raised `KeyError: net_own_rate` | The Trustees summary deliberately flattens its group results, and its CSV calls the net ratio `net_per_tax_dollar`. The adapter assumed the in-memory schema survived serialization. | `build.py` now checks the actual summary schema and complete group CSV explicitly; the unchanged arm must recover its full-precision scalars and each nine-decimal CSV ratio. `test_one_rate.py` verifies both source schemas and the positive control. Both failed runs exited before producing output. |
| Published-frame rate factors could miss the adopted account's row-4 adjustment | v7 item `row4_frame` changes the union ratio and Part A level as well as its population. | Replay `row4_oct07.py:93–114` on the source person frame; gate unchanged row-4 groups against its original full-precision results before writing outputs. |
| Reviewer found native-child accrual summing alternative keys | Each native-child edit set includes preferred benefit keys and alternative `age65plus` cells. Summing every edit counts alternative representations together. | `childAmount` now selects the actual model's preferred key. The payload-based regression independently sums only `social_security` / `medicare` cells and checks the reported child accrual basis, including the cash Part B/D subtraction. |
| Reproduction reported IDENTICAL 15/15 but exited 3 | Both commands passed, but the reproduction auditor's static command coverage cannot infer pytest's directory-based collection of the new test file. | Name `test_one_rate.py` explicitly in the pytest reproduction command. This runs the same suite, makes the static coverage principal explicit, and requires exit 0; no exemption is used. |

No upstream files are edited. All substitutions are confined to imported objects in this process.
