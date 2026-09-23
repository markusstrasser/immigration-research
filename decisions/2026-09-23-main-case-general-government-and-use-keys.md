---
date: 2026-09-23
concepts: [service-response, general-government, cost-allocation, crime-costs, uncompensated-care, headline]
supersedes: []
relations:
  - refines: decisions/2026-09-20-category-service-response.md
  - refines: decisions/2026-09-20-service-scaling-calibration.md
evidence: infra/immigration-fiscal/main_case_2026_09_23/RESULT.md
---

# 2026-09-23: The main case lets general government grow with the population and charges justice and uncompensated care by use

## Context

The complete account's main CBO-informed case ($165.1–197.4bn) held general public services at
zero response by assumption. Only its tax-incidence rules and its 63–66% school response come
from CBO. Public order and safety was charged per head. Uncompensated hospital care was charged
through Medicaid and health keys based on measured MEPS payments, which record no payment for
free care. The operator asked whether equal charges should give way to charges by use and
whether zero government growth is defensible. On 2026-09-23 he said to adopt the pending
proposals ("Do the remaining all").

## Alternatives considered

1. **Keep zero response for general government.** The only zero-compatible evidence is the
   within-state panel of 2012–2023 (elasticity 0.47, 95% interval −0.72 to 1.66). It cannot tell
   zero from one. Zero is a budget-scoring convention for appropriations within a 10-year window.
   It does not describe a stationary comparison with 41m fewer residents.
2. **Full proportional response (1.0).** Cross-state evidence shows scale economies in
   administration (0.84, not 1), and the federal legislature does not grow with the population.
3. **0.59–0.84, derived from the cross-state elasticities** (selected). State administration
   scales at 0.842 (SE 0.039) and financial administration at 0.789. The low end holds the
   federal executive and legislative budget fixed.
4. For justice and hospital care: **keep per-head and MEPS keys**, or **key by use** (selected).
   Use keys follow the account's own absent-target logic: removing the group removes its custody
   share, its arrests and its uninsured care.

## Decision

The main case and the other published benchmarks now include three changes:
- general government at 0.59–0.84;
- public order and safety keyed by use (justice lane central: prisons by adjusted custody, police
  half by arrests, courts 60% criminal, CBP per head);
- the under-charged government part of uncompensated hospital care keyed to uninsured use.

The part of uncompensated care borne outside government budgets, crime victims' harm and the
housing net are reported as social items beside the fiscal headline, never inside it. Defense,
interest on existing debt and business subsidies stay at zero. Result: main case
**$203.2–249.6bn**, fixed non-school education $158.9–212.6bn, proportional $307.9–341.0bn.

## Evidence

- `infra/immigration-fiscal/main_case_2026_09_23/` (gated reproduction of the published bands,
  then the three changes)
- `assumption_explorer_2026_09_21/scaling_check.py`
- `cj_use_allocation_2026_09_23/` (38 gates)
- `uncompensated_care_2026_09_23/` (corrected 575e2ee)
- `research/immigration-administration-response-test-2026-09-20.md`
- `research/immigration-real-fiscal-and-social-costs-2026-09-23.md`

## Revisit if

- A causal estimate of administration spending's response to population contradicts the
  cross-state scale range.
- Post-2019 arrest data by ethnicity move the police key.
- Jail records are shown to under-record Hispanic origin, which would raise the custody key.
- A held file observes free care by origin, which would replace the equal-use assumption.

## Supersedes

None. Earlier bands stay in their dated memos; the INDEX and FAQ route to this one.
