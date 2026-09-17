# Consistent all-age fiscal accounts — September 17, 2026

This lane replaces the mixed all-age-baseline/adult-only-extension calculation with one all-age partial account, four reference populations, survey uncertainty and attribution sensitivities. It does not estimate an admission-policy effect or lifetime NPV. Findings and source interpretation: [research memo](../../../research/immigration-all-age-and-lineage-findings-2026-09-17.md).

## Reproduce

From the repository root, using the held inputs:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/all_age_ledger_2026_09_17/check_estimator.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/all_age_ledger_2026_09_17/check_multicell.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/all_age_ledger_2026_09_17/analyze.py
```

Requires NumPy and pandas. No downloads, raw-file changes or writes to other analysis lanes. The upstream builder is imported; its output-producing `analyse` function is not called. Generated files are ignored under `derived/`.

Inputs are the held CPS ASEC 2025 ZIP (income year 2024), MEPS 2024 full-year file and SAS positions, the earlier extension's state parameters, its adult component CSV, and the independent baseline audit JSON. CPS contains 142,125 records, 58,147 SPM resource units and full plus 160 replicate person weights. Source and imported-generator hashes are recorded in `audit.json`. State parameters combine FY2024 school spending, 2024 sales rates and 2023 ACS property/rent proxies; this is a mixed-source annual model, not observed Treasury receipts.

## Populations and account

Reporting domain: civilian household population of all ages, defined as `PRPERTYP=2` or age below15. Target categories are disjoint:

- Mexico-born foreign-born citizens/noncitizens (`PRCITSHP=4/5`, country303).
- CPS-native with at least one Mexico-born parent.
- CPS-native with two US-area-born parents and Mexican self-identification. This is **third-plus self-ID**, not complete third-generation ancestry.

US-area parent codes are57/60/66/69/73/78; missing parents never count as US-born. References are third-plus non-Hispanic white, all CPS natives, all natives with two US-area-born parents, and other natives excluding the observed target categories. The all-native reference overlaps the targets; replicate contrasts preserve the covariance. These choices are comparisons, not proposed replacements for immigrants.

Main allocation: source-unit modeled employee payroll/federal/state income taxes minus selected cash and noncash benefits, plus employer payroll, modeled sales tax and owner property tax, minus public K–12, plus school-lunch overlap correction. All these components are shared equally over SPM members. Public medical costs are assigned directly by person's age and US/foreign birthplace, using MEPS donor means. They are never reallocated with household dollars. CPS infants born after the income reference year (`PUB=PRIV=0`) receive zero medical exposure; any noninfant in that path fails the run.

Employer payroll uses the held 2024 wage cap/rates and wages; it omits self-employment and other tax details not in that model. Sales tax assumes90% of nonnegative resources consumed and35% taxable. K–12 uses state per-pupil current spending and the held native-household public-pupil/child ratio, approximately0.803, applied to children5–17. Owner property tax and renter pass-through are proxies. The lunch addback avoids retaining both the SPM lunch benefit and its presumed inclusion in total school current spending; imperfect overlap is tested separately. See the source [extension](../gen_ledger_extension_2026_09_16/extend_ledger.py) for parameter provenance. These assumptions are not person-level receipts or marginal spending responses.

## Estimands and uncertainty

For group `g`, age band `a`, reference `r`, account totals `Y` and populations `N`:

`absolute = sum_a Y_ga`

`age-matched gap = sum_a [Y_ga − (N_ga/N_ra)Y_ra]`

`common-age gap per person = sum_a s_a [Y_ga/N_ga − Y_ra/N_ra]`

The third quantity uses the same fixed white-reference full-weight age shares `s` for all groups. The second divided by the group's population uses that group's own age shares and is not interchangeable with the third. Crude gaps are also emitted. Main bands:0–17,18–24,25–34,35–44,45–54,55–64,65–74,75+. A sensitivity splits children0–4/5–11/12–17.

Every CPS replicate recomputes populations, denominators, reference schedules and composite balances. CPS variance is `4/160 × sum((replicate−full)^2)`. The MEPS donor gradient is computed for the exact contrast; its full stratified-PSU covariance contributes `q'Vq`. The two independent-survey variances are added as a first-order approximation. Shared donor cells, reference overlap, components and combined generations are not treated as independent. Intervals are pointwise normal95% intervals, conditional on fixed age-standard shares and model parameters; they omit model/transport error, coverage bias and higher-order CPS–MEPS interactions. They are not simultaneous bands over all scenarios or origin definitions.

## Sensitivity coverage

Thirteen scenarios produce1,144 estimates:

| Scenario | Change from expanded main account |
|---|---|
| `baseline` | Earlier taxes/selected benefits/medical components only; reproduction anchor |
| `all_age_shared` | Expanded main account, person weights, shared unit dollars |
| `personal_sources` | Taxes/cash to recorded people, employer payroll to earners, schooling to children; other unit dollars shared |
| `unit_head_weighted` | Shared unit-component dollars use one head's replicate weight throughout each unit |
| `personal_head_weighted` | Same unit-dollar weighting, personal-source assignment |
| `finer_child_age` | Split child age bands; health donor bins remain unchanged |
| `insurance_health` | Add insurance to medical-donor matching |
| `no_health` | Omit health entirely as a component diagnostic |
| `retain_lunch_overlap` | Leave the possible lunch overlap in place |
| `sales25`, `sales45` | Taxable consumption share25% or45% |
| `pupil90` | Public-pupil ratio90% |
| `renter_property` | Add the source model's15%-of-rent property-tax proxy |

**Fixed-budget attribution test:** the two head-dollar arms retain ordinary person weights for population and direct medical exposure. Only unit-component dollar weights change. Within this pair, reassignment conserves each national component budget in all161 weight vectors. An exhaustive “all other records” cell includes non-target and noncivilian shares. Thus the paired difference isolates attribution conditional on that dollar estimator. Switching shared to personal allocation while retaining unequal person weights does *not* conserve weighted national dollars; both calculations are retained and distinguished.

These are named, mostly one-at-a-time checks, not a search over all joint assumptions or empirical bounds. Missing corporate taxes, pure public goods, institutional care and other omitted channels can affect complete fiscal accounts. A common per-person charge cancels from relative gaps while reducing absolute balances.

## Outputs and validation

- `estimates.csv`: absolute, crude, age-matched and common-age estimates with separate CPS/MEPS errors.
- `generation_contrasts.csv`: paired common-age later-minus-earlier contrasts, preserving covariance; cross-sectional populations, not family trajectories.
- `component_gaps.csv`, `age_profiles.csv`: component and age decompositions for named scenarios.
- `fixed_budget_attribution.csv`, `fixed_budget_transfers.csv`, `fixed_budget_gap_decomposition.csv`: paired changes, exhaustive signed transfers and separate target/reference movements.
- `replicates.npz`, donor-cell CSVs and `audit.json`: replication vectors, donor means, provenance and executed checks.

Executed guards cover joins, credit identities, raw unit conservation, each matched composite's component sum, union additivity, self-reference, common-charge cancellation, finite-difference donor gradients, all-age baseline anchors, and35 held adult component means **and** standard errors. Hand calculations and an independent numerical review cover denominator perturbation, multi-cell covariance, shared-reference cancellation, common ages and missing-band failure. The reviewer caught a falsely broad component-check flag; the assertion now actually runs for all13 scenarios. The full raw run passed after the repair.

## Construct review disposition

The independent in-task design review proposed three consequential tests, all implemented: fixed national dollars when changing attribution; one common age distribution when comparing generations; and narrower child bands. A separate code review tested the estimator rather than adjudicating the design. The IIMMLA lane had its own source/code review. [Review disposition](../../../notes/immigration-construct-review-2026-09-17.md).

External cross-model review was prepared and preflighted but automatic approval review blocked transmission of the private packet to GPT/Claude subscription services pending explicit permission. No cross-model verdict is claimed; the local review and validation above were completed independently of that pending step.
