# SIPP departure work: verification and review record

**Verdict:** No material correction to the estimates or bounded interpretation
was identified. The analysis supplies descriptive evidence for the observed
separations, not a deportation-response coefficient or a v9 revision.

## Deterministic and independent evidence

- Original-source definitions: `definitions.md` records the dictionary/guide
  checks and the distinction between recodes and reported components.
- Independent event reconstruction: `event_validation.md` reconciles all 524
  directed pairs and all pair-level flags. Initial age-boundary disagreement was
  resolved by applying the declared pre-event age rule. This validates internal
  survey consistency, not an external address register.
- Independent numerical calculation: `numerical_verification.md` and
  `derived/independent_numerical_check.json` cover eight unweighted principal
  summaries and eight December-weighted summaries, including all weighted Fay
  confidence limits. They do not independently verify the benchmark or the
  unweighted percentile-bootstrap intervals.
- Seven synthetic tests pass, including event collapse, whole-household moves,
  subsequent focal moves, birthdays, missing/zero handling, shared-cluster
  resampling, missing relationship counterparts and unsupported comparisons.
- Full lane replay exited zero: `IDENTICAL: 34/34 files unchanged`. The command
  is in README. The final replay includes the figure-title clarification.
- The earlier benchmark row-loop and the optimized cluster/stratum aggregation
  gave identical numerical results for all 24 rows using the same bootstrap
  draws. This is optimization parity, not independent causal validation.

## Code and visual review

Astra's separate code review covered all eight Python/shell implementation and
test files. Two medium findings were confirmed and repaired: require each
relationship-person-ID column's value counterpart, and emit an explicit
unsupported-comparison row instead of silently returning an empty result.
Both fixes have targeted regression tests. Receipt:
`/Users/alien/Projects/agent-infra/artifacts/code-review/sipp_departure_work_2026_10_16/2026-10-16.jsonl`.

A blind figure reader correctly recovered the event-time axis, zero baseline,
outcomes, separate cohorts and uncertainty. The title now says "estimated"
work changes; the caption states that intervals are pointwise and descriptive.
No fiscal figures-page change was made.

## Requested claim critique: Gemini and Astra

The packet included the memo, protocol, definitions, independent numerical
record, event audit, all estimates, benchmark, distributions and influence
diagnostics. Code was excluded because the separate code review owned it.
The actual served models were `gemini-4-argon` and `gpt-6-astra`; both completed
and explicitly reported **no material error**. Saved local review directory:
`.model-review/2026-10-16-sipp-departure-work-8b4a40/`.

Every substantive suggestion was checked against the outputs:

| Review point | Disposition and evidence |
|---|---|
| Keep the positive tracked earnings benchmark contrast | Retained +$862 [+$31, +$2,075], and the children-standardized counterpart; `derived/benchmark.csv`. It is observational and sensitive to the earnings tail. |
| Small means do not establish equivalence; cohorts and measurement differ | Already explicit. No null-proof, population equivalence, external address validation or deportation inference is added. |
| Resampling omits measurement/selection uncertainty; flat retrospective spells are not payroll invariance | Retained explicitly in the memo and README. The December Fay analysis is separate from the unweighted bootstrap, and neither quantifies all missing uncertainty. |
| Independent checks do not cover every bootstrap/benchmark calculation | Scope is retained in `numerical_verification.md` and above. No wider independent-verification claim is made. |
| Six monthly means were not present in the review packet | Packet omission, not a missing analysis: `derived/monthly.csv` has all six months for all four outcomes and both routes. Added direct memo links to that table and the figure. |
| Surface pre-trends and distinguish the benchmark resampling method | Added the source-checked +$170 earnings and −0.54 h pre-trend benchmark contrasts and an explicit Poisson-bootstrap label. These are not a parallel-trends test proving identification. |
| Influence key could be misread as unsigned contributions | The generator ranks by absolute change, then sums signed changes divided by the full N. Thus the top-five net contribution can be below the top-three contribution. The memo already says "largest absolute earnings changes" and reports the signed +$709 contribution; no estimate or schema change is needed. |
| Add more calendar-length earnings movement counts | Not added to the prose: both earnings definitions and all distribution counts are retained in CSV; the memo identifies `TPEARN_ALT` and the calendar-month sensitivity. More counts do not change this one-link conclusion. |
| A packet cannot prove the historical absence of a significance target | Correct scope limit. The protocol and retained specification outputs make the stated analysis policy inspectable; reviewer agreement is not proof of an analyst's private motives. |

This accounts for all 14 extracted low-priority entries: influence (1),
verification scope (2), pre-trends/method label (3–4), acknowledged inference
and measurement limits (5–7, 9–11, 13), packet-only omission (8), calendar
sensitivity presentation (12), and historical analysis policy (14). The
automatic anchor checker marked two confirmed and twelve inconclusive; those
labels concern textual anchors, not scientific truth. The table above is the
source-grounded disposition.

Gemini's claims to have "verified" join implementation from a claims-only packet
are not adopted as additional implementation evidence. Source-record and code
checks above support those details. Neither model's agreement replaces data.

## Tooling incident

The initial preflight tested unused Claude quota and blocked this explicitly
Gemini/Astra panel. The shared critique tool now permits an explicit Astra
subscription probe, with a failing selected route still blocking. Both requested
routes passed live checks; 120 tests and 38 subtests passed in the shared tool.
Repair: skills commit `94b4b74`. No model substitution or quota bypass occurred.
