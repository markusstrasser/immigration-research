# Remaining adults around SIPP household departures

Written before estimating outcome changes, 2026-10-16. One descriptive link:
an adult co-resident leaves and the same remaining adult's own work changes.
No deportation identification, causal effect, fiscal calibration or figure-page
update is promised. Official survey edits and retrospective recall remain part
of the measurement even when record checks pass.

## Population and events

Start with reference-year 2024 in the public 2025 SIPP, the source of the previous
214-person tracked screen. Primary events require a working-age focal adult
(18–64 before departure), stable adult identity, observed co-residence with
another adult for t−3 through t−1, and distinct valid addresses at t with the
focal adult still at the previous address. Verify residence spell boundaries,
survey-universe status, and allocation flags against original definitions.
Report each successive exclusion and competing valid definitions.

Use the first eligible event per focal adult, collapsing simultaneous departures;
cluster uncertainty by original sample unit. Follow the focal adult after later
moves; retain return/re-entry as diagnostics rather than requiring permanent
separation in the primary sample. Show a persistent-separation sensitivity.
Type-2 slot candidates are audited separately using person sets, age, relationship
and consistency across the records that report them. Do not combine the two
routes unless identity/overlap can be resolved. If Type-2 identity fails, report
that failure and estimate only the tracked route.

## Outcomes and contrasts

The primary window averages t−3…t−1 versus t…t+2 (April–October departures).
Report employment probability, average weekly hours in the month, and personal
monthly earnings/profits in nominal 2024 dollars. Retain negative earnings and
nonworkers. The official job/universe definitions, not convenience, decide
structural zeros; unresolved missing values stay missing. Report an available
balanced cohort separately for each outcome and a common-outcome sensitivity.
Show all six monthly means, immediate t−1→t changes, and pre-event trajectories.

Lead with unweighted same-person descriptive changes and 95% original-sample-unit
bootstrap intervals (fixed seed, 1,999 draws). A baseline-month survey-weighted
sensitivity uses the corresponding official replicate weights and variance rule,
if the documentation supports that calculation. These weights do not correct
event selection or post-event nonresponse; neither construction is advertised as
the national response to all departures.

As a seasonality/ordinary-change benchmark, compare to adults who share a stable
household before the same calendar month and have no observed adult departure
at that month. Standardize to event month, sex, broad age (18–29/30–44/45–64),
and baseline employment (all/no/some pre-months employed), with children-present
as an additional sensitivity if supported. Do not condition controls on later
work, later moves or future departures. Report support failures and future
departure contamination. This benchmark is descriptive and does not make exits
exogenous. Do not choose a favorable specification or an outcome-dependent
window.

## Sensitivity and interpretation

Show reported-residence versus allocation-inclusive events; reported-outcome
versus allocation-inclusive observations; spouse/partner versus other exits;
children present versus absent; prior departed-person earner versus non-earner
where observed; persistent versus any validated split. Sparse cells remain
imprecise; suppress individual records and do not invent a precision threshold
that discards valid null results. Preserve counts and reasons for missing follow-up.
No subgroup or association becomes a deportation or lineage-wide parameter.

### Documentation refinement before any outcome estimates

The official guide recommends December weights for a single-calendar-year
cohort. Use December WPFINWGT and matching December 240 replicate weights for
the weighted sensitivity (Fay BRR, k=0.5), replacing the provisional baseline-
month choice above. The dictionary provides TPEARN_ALT, which removes variation
in earnings caused solely by month length: lead with that monthly earnings
measure and retain TPEARN as the actual-calendar-month sensitivity. Both retain
nominal 2024 units and valid negative profits. These refinements follow source
definitions and precede inspecting outcome contrasts.

Raw records, schema/guide definitions, independently reconstructed events,
source hashes, synthetic tests of event/zero handling, deterministic rerun and
review of the final claims supply checks independent of the analyst's judgment.
Any outcome-informed departure from this protocol must be dated and explained.
