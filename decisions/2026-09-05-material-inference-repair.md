---
date: 2026-09-05
concept: fiscal-accounting-and-causal-identification
status: adopted
trigger: user-authorized-comprehensive-repair
---

# 2026-09-05: Repair fiscal units and separate evidence from inference

## Context

The [material audit](../research/immigration-conceptual-audit-2026-09-05.md) confirmed household/person and education-code errors in the fiscal model and invalid inferences in several literature rebuttals. The operator instructed us to perform the repairs and continue checking for material causal, statistical and economic errors.

## Alternatives considered

1. Relabel the existing fiscal outputs: insufficient because the donor/recipient units themselves disagree.
2. Divide household totals by an average adult count: insufficient because matching bands, benefit units and tax caps are nonlinear.
3. Rebuild with household donors and household ACS recipients: coherent, but changes the current adult estimand and still requires an explicit adult allocation.
4. Use person donors, valid education codes, annual individual earnings and once-only benefit allocation: chosen because it directly matches the adult recipient cells while preserving inspectable accounting.
5. Remove the local model and rely solely on published benchmarks: unnecessary if the public raw data support repair, but unvalidated outputs must remain unavailable until validation succeeds.

## Decision

Rebuild the narrow employee-payroll-minus-allocated-selected-benefits model with consistent person units. It remains a partial accounting model, not a full fiscal balance or causal welfare estimate. Migrate executable callers together; no old-schema compatibility aliases.

Correct the research artifacts themselves. Preserve primary quotations and dated belief-change history. Withdraw conclusions that do not follow from the measured object; distinguish population averages from incumbent outcomes, accounting sensitivities from sign reversals, projected from observed outcomes, and descriptive regression patterns from identified causal effects. Scope uncertainty precisely rather than replacing unsupported negative claims with unsupported positive ones.

## Evidence

- The actual-builder two-adult fixture doubles payroll under the old donor mapping.
- Census's SIPP EEDUC dictionary contradicts the old code thresholds.
- The Cato study includes both costs and taxes in its separate descendant calculation.
- A population mean can fall while every incumbent gains; constant returns does not exclude that pattern.
- The global-gains calibration gives 20.45%, not doubling, for three billion additional migrants.
- The direction of the second-generation comparator change requires its rate relative to third-plus-generation natives.

Primary sources and calculation traces are in the audit. Subsequent repairs and fresh-review findings are recorded in the repair report.

## Revisit if

Source definitions or validation reveal a different coherent allocation is required; new data identify previously unresolved causal effects; or an independent review finds a remaining material error. A successful execution alone does not close a scientific claim.

## Supersedes

The specific invalid inferences and implementation conventions identified in the September audit. The mission, central question and constitution are unchanged.
