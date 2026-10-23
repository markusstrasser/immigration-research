# 2026-10-23: Carry the measured range into the routing layer and screen noisy estimates

## Context
Two failures surfaced in one session. First, an agent read the INDEX and FAQ's
"the sign turns on ordinary service budgets" and treated the frozen-services
break-even (12–16% of assigned service costs) as a live scenario. The measured
service scaling is near-proportional (0.6–1.0 across the ten state/local
functions), so the break-even sits outside the measured range; the routing layer
had dropped that qualifier. Second, the scaling table showed the within-state
library estimate (0.676, CI [0.020, 1.331]) next to the across-state estimate
(0.974, CI [0.871, 1.076]) with only a prose caveat, even though the within-state
series is too noisy to distinguish proportional from a 3/4 exponent (state 28:
60,524 in 2017, 27,965 in 2018; windows 0.590–1.519).

## Alternatives considered
1. **Prose-only fixes** — edit the four passages. Pros: minimal. Cons: the same
   compression recurs at the next case move; no mechanical check.
2. **Rule + lint + estimate gate** — a routing-layer rule, a lint that flags
   conditional-without-range sentences, and a four-test screen that demotes
   failing estimates to "not identified". Pros: catches the failure class, keeps
   the numbers auditable. Cons: a heuristic lint with false positives; the
   screen's thresholds need calibration.
3. **Suppress all uncertain estimates** — delete failing point estimates.
   Pros: clean tables. Cons: hides the audit trail and violates the
   error-correction principle; a reader cannot see what was tried.

## Decision
Option 2. The routing layer must carry the measured range or a link to the lane
that does. A break-even is tagged `[THRESHOLD]`, not presented as an estimate. An
estimate that fails precision, stability, influence or data quality is demoted,
not deleted: the point estimate stays in `estimates_screened.csv` with
`screen=fail`, and the memo table prints "not identified (codes)".

## Evidence
- `research/immigration-service-scaling-test-2026-09-20.md`: across-state
  elasticities 0.727–1.085; within-state intervals all include 1; the exact
  finite-removal bridge gives r = 0.762 at b = 0.75 and 0.842 at b = 5/6, so a
  12–16% response requires b ≈ 0.11–0.19.
- `infra/immigration-fiscal/scaling_test_2026_09_20/derived/state/estimates.csv`
  and `panel.csv`: the library within-state series and the state-28 swing.
- `main_case_2026_10_16/derived/sign_reversal.csv`, oct16 personal rows: frozen
  services give −$50.9bn to +$76.1bn; enterprises at s give −$33.4bn to
  +$93.6bn.

## Revisit if
The lint's false-positive rate is high enough to be ignored, or the screen's
precision/stability thresholds fail estimates the lane's authors consider sound
(or pass ones they consider noise). The thresholds are in
`scripts/estimate_screen.py` and should be recalibrated on the ten functions
before being applied to a new domain.

## Supersedes
None.
