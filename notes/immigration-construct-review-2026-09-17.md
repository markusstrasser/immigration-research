# All-age accounts and family histories: review disposition

Date: September 17, 2026. Target: the scientific meaning and implementation of the new all-age fiscal and IIMMLA analyses. This records actual coverage, not a blanket validation of the immigration project. [Findings](../research/immigration-all-age-and-lineage-findings-2026-09-17.md).

## Scope and independent work

A live-premise scout checked the held CPS/SPM component builders, generation masks and medical-donor interface before design review. A fresh-eyes in-task reviewer formed its initial scientific assessment from the bounded packet, then traced the relevant code. A separate reviewer tested the fiscal estimator with independent scalar calculations and numerical gradients. Another independently reconstructed IIMMLA rows from primary questions. A primary-source researcher checked fiscal-policy constructs against NAS, CBO, Clemens and Colas–Sachs. Native model agreement is not treated as source evidence.

Raw reports are preserved locally under [ignored review artifacts](../infra/immigration-fiscal/all_age_ledger_2026_09_17/derived/review/). The numerical probe is retained as `check_multicell.py`, alongside the authored hand checks. Source hashes and the full-run guards are recorded by the generators.

## All findings and dispositions

| Finding | Grounding and disposition |
|---|---|
| Shared-to-person attribution with unequal person weights can change national dollar totals | **Confirmed algebraically and in live arrays. Implemented:** paired shared/personal head-dollar arms, unchanged person-weighted population and direct health, exhaustive other-record transfers, component/replicate budget conservation, and paired uncertainty. These are attribution diagnostics, not official national expenditure controls. |
| Each generation's population-normalized gap uses its own age distribution | **Confirmed by the estimator formula. Implemented:** a separate common-age per-person metric and paired generation contrasts. Target-standard uncertainty is explicitly conditioned away. Observed-population totals are retained. |
| Broad child bands mix schooling exposures | **Confirmed from the age rules. Implemented:** fixed 0–4/5–11/12–17 sensitivity with unchanged medical donors. White-reference total changes by −$1.47bn. This does not validate finer medical transport or every possible adult age partition. |
| Fiscal audit claimed component checks for scenarios where the assertion was skipped | **Confirmed in source. Fixed:** the component identity now runs in every matched contrast in all 13 scenarios; the full raw run passed. Selected component CSV exports remain a reporting choice rather than a false check-coverage claim. |
| IIMMLA source-coded generations include unresolved or conflicting raw histories | **Confirmed by independent row reconstruction. Implemented:** source and strict groups both retained; counts 212/189 become 196/187, then 192/182 with common valid raw endpoints. Unknown crime paths remain missing. Known raw outcomes all agree with source binaries. |
| Generic G3 and Mexican-grandparent G3 are not interchangeable; G4 origin verification is asymmetric | **Confirmed by questionnaire. Implemented:** separate labels, paired grandparent-country test, complete-country sensitivity, and explicit missing great-grandparent information. No genetic fractions or national attrition rates inferred. |
| IIMMLA age caption 20–39 is inaccurate; incarceration includes juvenile settings | **Confirmed in the primary codebook/questionnaire. Corrected:** ages 20–40 and broad lifetime endpoint named in the new memo; dated correction appended to the earlier audit. |
| A stock benchmark gap cannot identify marginal admissions, incumbent welfare or lifetime NPV | **Confirmed by definitions and primary fiscal literature. Retained as scope, not a reason to discard adverse descriptions.** The memo separates these quantities and keeps unfavorable local-cost and dropout evidence beside omitted-benefit mechanisms. |
| “First-versus-later improvement” overstates which adjacent contrasts are supported | **Confirmed in the final claim-source check. Narrowed:** the supported contrast under both assignment rules is first-to-third-plus. The main memo now also prints the shared first-to-second interval, which includes zero. |

No consequential numerical defect was found in the estimator or the IIMMLA reconstruction. This verdict covers the specified calculations, not completeness of fiscal accounts, external validity, country-specific health transport or causal identification. Source-label uncertainty in the publisher's ethnicity/credential recodes and unidentified raw-unknown outcome derivations is preserved rather than relabeled as a publisher bug.

## External critique status

The user requested the [critique skill](../../skills/critique/SKILL.md). A repository-grounded scientific packet and matching dispatch manifest were prepared; subscription preflight passed. No paid API was used. The intended GPT/Claude subscription dispatch was rejected by automatic approval review because it would transfer a non-public internal research packet and repository methods externally without destination-and-payload-specific permission. Explicit permission for that exact transfer was requested asynchronously; no response had arrived when this record was written.

The packet remains at `.model-review/allage-construct-20260917.md`. No transport workaround was attempted, and no external cross-model review is claimed. Work that did not require that transfer continued: native independent critiques, raw calculations, source verification and reproducible checks. The workflow distinction is explicit so that “reviewed” cannot be mistaken for “passed an external panel.”
