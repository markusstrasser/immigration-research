# Review and verification — 2026-10-16

**Verdict:** No material implementation or claim-layer defect found in the bounded
conclusion. This is not empirical confirmation of the assumed earnings response.

Source implementation: local `/code-review` scout, GPT-6 Astra, patterns lens,
exact `bound.py` scope, exit 0 and zero findings. The scout groups modules only
two directory levels deep, so the lane was selected with `--file`, not its
unrecognized deeper module name. Tests were covered by parent inspection and
execution, not silently represented as scout-reviewed. Six tests passed and the
generator/test rerun exited 0, `IDENTICAL: 6/6`, before prose additions. The
original source archive and upstream analysis outputs were not changed.

Claim layer: Gemini 4 Argon and GPT-6 Astra reviewed the memo, design, full output
table/audit, two independent source/API assessments and the high-wage kernel
probe. Both explicitly reported no material defect. Served-model receipts show
both requested models, exit 0, no fallback; no packet blocks were truncated or
dropped. Dispatch took 101.6 seconds, followed by structured extraction and
anchor verification. Raw local evidence is in
`.model-review/2026-10-16-v9-household-work-response-4158a6/`; packet builder and
exploration probes are in `.model-review/household-bound-2026-10-16/`.
The reviewed packet hash is
`dcca1a65fb12a5f13d719ebd64bcf201dd8bf18903842414de8893afe67cc1d2`.

The extractor produced eleven records, mostly already-disclosed limitations and
future-use cautions. Automated anchor checking labeled ten inconclusive because
they lacked exact code anchors; that is not a substantive verdict. Every record
was assessed against the actual memo, output, source rule or executed fixture:

| ID | Disposition and evidence |
|---|---|
| 1 | Confirmed already handled: combined kernel FICA fails the high-wage statutory example. `payroll` uses the SSA cap directly; regression passes. |
| 2 | Valid reuse caution: uniform shocks do not identify responses to every aggregate loss. Added an explicit sentence beside the crossing. No new response distribution is claimed. |
| 3 | Already constrained: care needs are a roster screen, not observed caregiving or a causal ranking. Memo and design retain that boundary. |
| 4 | Already constrained: statutory survey-dollar output is only compared with v9 as a scale reference; no five-percent v9 correction is asserted. Calibration/compliance/overlap/accrual integration is excluded. |
| 5 | Same source concern as 1, including Additional Medicare. Independent single/joint/wage-plus-SE tests pass; the kernel component is removed before the IRS amount is inserted. |
| 6 | Valid future-study caution: externally induced departure plus controls alone is not identification. The memo proposes an estimand, not a certified design; selection, concurrent shocks, trends and attrition remain study requirements. |
| 7 | Fixed minor omission: the design's secondary accrual scale reference, $18.401bn, is now stated as scale only. |
| 8 | Already enforced: zero-response identity and unchanged-return isolation run in the generator and pass across all signed replicates. Future membership changes must rerun them. |
| 9 | Accurate existing distinction: exposure is net earnings; shocks scale positive components and preserve losses. The $0.009812bn difference is consistent with that rule. No numerical correction is needed. |
| 10 | Already constrained: unknown descendant identities and missing household locations are neither silently allocated nor assigned a convenient direction. No complete-population bound is claimed. |
| 11 | Already constrained: health and accrued retirement/Medicare responses remain unpriced, explicitly preventing mechanical addition to the main-case headline. |

The two prose clarifications after review do not change calculations or verdict.
The upstream historical income-tax calibrations retain their pinned kernel's
Additional Medicare discrepancy; changing them is deferred because it requires
a separate measured propagation audit, not a silent alteration of source lanes
while conducting this one-link sensitivity. Earlier payroll allocation code did
not consume this kernel's `fica` field.

Quantitative self-check: ledger is annual partial statutory cash, year2024,
observed2025 households; population and unknown coverage are explicit; tax/benefit
netting and signs are traced; both response directions and all prescribed
specifications are shown; sampling and behavioral uncertainty are separate;
neither a policy conclusion nor causal effect is inferred from the scenarios.
