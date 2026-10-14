**Verdict:** No material correctness or operational defect found in the seven scoped extension files. The calculations reproduce their stated conditional models; this review does not establish the economic response assumptions.

Findings: none requiring correction. Confidence is high for the checked arithmetic and sign, moderate for economic completeness because programme overlap and general-equilibrium responses remain explicitly unresolved.

Covered in full: `demand_keys.cjs`, `reallocation.py`, `test_reallocation.py`, `extended_integrate.py`, `k5_cells.py`, `test_k5_cells.py`, `within_firm.py`. Supporting reads covered relevant portions of `core.py`, `refine.py`, the frozen industry wage table, the spending builder, source SUT workbook, NPZ arrays and derived JSON/CSV records.

Verification performed read-only, except this requested result file and a temporary independent checker:

- Both scoped test files pass: 9 tests, 0.23 seconds, exit 0; pytest cache and Python bytecode writes disabled.
- Five existing positive-control output files are byte-identical to their frozen counterparts. Independently reconstructed central union/lineage totals agree within 1e-9bn; reallocation-off controls pass at 1e-9bn; union one-sector totals match the frozen plain-share arm at 1e-6bn. The frozen producer itself was not rerun during this review.
- Mining refill draws the selected tradable sector's tax-per-wage intensity; agriculture removes both `111CA` and `113FF` from the donor pool before calculating refill. Independently reconstructed national/group refill arms match their stored deltas within 1e-9bn.
- K1/K2 changes corporate target exposure while the donor rate and demand release use national domestic-source amounts. Independent direct T/fixed plus N-demand plus native-refill reconstruction matches the exact narrow/broad stack: maximum discrepancy 5.684341886080802e-14bn. The existing legal/source-only stack also closes at 1e-9bn.
- Primary SUT rows total 91.171bn and 4.883bn. All eight subsidy vectors and union point estimates independently reproduce. Housing/enterprise exclusions and the 624/ORE alternative treatments are explicit. Four fresh live engine probes (two methods, two personal ends) confirm that changing transport subsidy response from zero to one raises cost by its allocated line amount, with discrepancies below 1e-9bn.
- Outer envelopes select one extreme per family, retain zero as an alternative, sum only same-direction moves, and reproduce their root-sum-square results. They explicitly describe component arithmetic rather than an exact joint economic model; exact interacting stacks are separate.
- Explicit empty response dictionaries raise; explicit all-zero responses remain zero. `None` alone selects the central response.
- Independently recomputed within-industry standardization agrees for all 161 columns. Point gaps are +2.627072pp under 100 employees, -3.799106pp at 1000+, +1.172034pp at 100–999 and zero unknown.

Limits/omissions: no fresh raw-CPS rebuild, acquisition, primary-source verification of external economic assumptions, or review of unscoped producers in full; no frozen edits or git writes. Stored positive-control bytes were compared, not newly generated. Full network/land/subsidy-stack formulas were traced in code, while independent numerical reconstruction concentrated on the K1/K2/reallocation/mining stack and subsidy vectors. The live 624/programme overlap remains unmeasured, as the output states; passing tests cannot turn these arms into measured policy responses.

Convention reconciliation: the choice to report sums and quadrature of overlapping mechanism families is a stated project reporting convention, not a confidence interval. Its explicit labeling is essential; interpreting those envelopes as jointly executable scenarios would exceed what the code establishes.
