# Remaining-household work response beside v9

**Verdict:** The raw household roster narrows the direct care concern but leaves
the broad work-response channel open. This lane supplies conditional partial
cash sensitivities, not causal estimates or adopted main-case adjustments.

See the [memo](../../../research/immigration-v9-household-work-response-2026-10-16.md)
for the complete table, interpretation and exclusions; [DESIGN.md](DESIGN.md)
records the decision rule before fiscal results and the subsequent SNAP rule
correction. [derived/audit.json](derived/audit.json) records exposure, source
hashes, membership, weights and checks; [derived/responses.csv](derived/responses.csv)
contains every prescribed scenario, component and full signed-replicate SE.

Raw input: Census 2025 ASEC (2024 earnings), archive hash
`318845a2b5e0034eb2973898de1738f4df0025727de38499e7669cb9c0deef0b`.
No original source or upstream analysis output is modified. NBER/benefit source
pins are verified by reused loaders; the local tax binary is macOS-specific and
fails closed on unsupported hosts. No records are sent to a tax service.

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/household_behavior_bound_2026_10_16/bound.py
uv run --no-project python3 -m pytest infra/immigration-fiscal/household_behavior_bound_2026_10_16/test_bound.py -q
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/household_behavior_bound_2026_10_16 'uv run --no-project python3 {lane}/bound.py' 'uv run --no-project python3 -m pytest {lane}/test_bound.py -q'
```

Validation: six tests pass; deterministic rerun exited 0 with `IDENTICAL: 6/6`
before prose was added. Zero shocks are exactly zero in all 161 weight columns;
unaffected tax returns do not change; exposed adults are represented once.
Fixtures cover capped payroll, self-employment losses, Additional Medicare,
refundable credits, original-data isolation, and SNAP eligibility transitions.
The source implementation received an Astra code-review scout pass with zero
findings; tests were checked by execution and parent review. A separate memo
critique and its dispositions are recorded in [review.md](review.md).

Known limits include unlocated lineage/coverage, 2025 household rosters paired
with 2024 earnings, proxy care needs, frozen claimant/dependent relationships,
unmeasured work responses, statutory rather than calibrated taxes, and unpriced
health/other benefits, consumption taxes, accrual and market-wide channels. The
five-percent cash reference is a convention, not a statistical rejection rule.
