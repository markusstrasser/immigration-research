# Audit of v9's long-run school-cost response

Question: does the original evidence support charging the full average K–12 cost
for the group's pupils in a stationary comparison? One link only. The audit does
not change the adopted case, population, accounting basis or policy horizon.

## Selection and decision rule, before results

The selected link is pupil numbers → long-run school expenditure at unchanged
service quality. The existing v9 school sensitivity moves the annual account by
about $27–30bn. General administration has weaker within-state identification but
a smaller well-supported alternative; corporate pure-rent response is unmeasured;
the medical residual is under active peer review. These are selection checks,
not additional audits.

An independent reconstruction of the original Census F-33 files tests the
cross-district proportionality claim and the long-difference evidence. One
additional discriminating check controls for NCES's comparable wages outside
teaching: large districts may face higher input prices within a state. The
wage-adjusted and unadjusted fits must use the identical matched sample. The
index is a measured estimate with uncertainty, not an instrument for enrollment.

Material threshold: a defensible change capable of moving the full annual
account by $5bn. A statistically significant descriptive slope is insufficient
to replace a causal counterfactual. Replacement requires evidence about enduring
cost at comparable quality, geography and input prices. Otherwise report a
conditional sensitivity and say the central assumption was not falsified. Apply
that standard to upward and downward revisions alike. Do not manufacture a defect.

## Original inputs and prespecified comparisons

- Original Census F-33 FY2000, FY2010 and FY2019 CSVs; Table 8 summary workbooks
  for 2010 and 2019; original item documentation. Own-year `V33` is enrollment;
  `TCURELSC` is current expenditure in thousands of dollars; `TCURINST` is
  instructional expenditure. Use valid NCES IDs and school levels 01/02/03,
  at least 100 pupils and positive costs; exclude DC from regressions.
- 2019 state-intercept cross-sections, equal and pupil weights; state-intercept
  long differences for 2000–2019, 2000–2010 and 2010–2019, equal and initial-pupil
  weights. Preserve every computed growing/shrinking, instructional and
  stable-identifier/large-enrollment-change sensitivity. No outcome-tail trimming.
- NCES CWIFT2019 official archive, LEA1920 member: `LEAID`, `LEA_CWIFTEST`,
  `LEA_CWIFTSE`. Compare the same 2019 sample with and without log wage index;
  estimate its coefficient rather than assume that all school expenditure is wages.
- State-clustered CR1 uncertainty with t critical values. The intervals describe
  regression uncertainty conditional on the design; they exclude causal and
  transport uncertainty. Common inflation is absorbed by state intercepts in
  each fixed-year cross-section or common-endpoint long difference.
- Reconcile raw component identities and report original-file national totals
  beside published Table 8. Do not calibrate away definition differences.

## Frozen case and limitations

The evaluated v9 is the proposed candidate at `fb822a95`, annual set
$344.023286/$412.555074bn. Initial HEAD `10dd7284` changed a beside business-tax
source after the candidate was built; its principal-source hash guard correctly
rejected loading the older coverage snapshot. This audit therefore uses the
internally consistent proposed-v9 commit, without bypassing the guard or taking
concurrent uncommitted changes. The original-source regression data are separate
from this model snapshot.

Only the school response changes in the fiscal calculation. Use the case's full
evaluator and companion post-engine transport, search all personal specifications
in both methods, check response 1 and the existing 0.836-elasticity companion,
and report all conditional scenarios. The inherited power curve is a scenario
mapping, not identified by the expenditure regressions. A school-only zero-cost
bound and sign break-even establish whether this link can overturn the sign.

The final memo is written after the calculations. Raw inputs are read-only;
generated outputs are reproducible. No new policy effect or causal estimate is
claimed from these observational checks.

## Result and reproduction

The [memo](../../../research/immigration-v9-school-response-audit-2026-10-15.md)
records the result: no new material correction established. The wage-adjusted
pupil-weighted cross-sectional slope is 1.004; the nineteen-year slope is 0.846,
close to the existing lower school scenario. Neither identifies the national
counterfactual. See all 54 raw specifications and 12 wage specifications in
`derived/`; do not treat the regression intervals as fiscal confidence bands.

From a checkout with the registered original data and the frozen commit locally:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project --with scipy --with xlrd --with statsmodels python3 infra/immigration-fiscal/school_response_audit_2026_10_15/reproduce.py
uv run --no-project --with scipy --with xlrd --with statsmodels --with pytest python3 -m pytest infra/immigration-fiscal/school_response_audit_2026_10_15/ -q
```

`--data-root /path/to/main` permits running from an isolated worktree. The wrapper
exports the pinned v9 commit with a temporary detached Git index for historical
`git show` calls, supplies four existing ignored model inputs only
if their fixed hashes match, and deletes the temporary export on completion.
It never resets the checkout or alters source data. The fiscal evaluator's
vendored September stack is the frozen case's supported cache-free input; its
hash is in `fiscal_sensitivity.json`. Missing or changed principal inputs stop
the run. `failure-catalog.md` records the encountered failures and checks.

`raw_sources.json` records original-file pins; `raw_coverage.json` records filters,
component identities and panel coverage; `raw_benchmarks.json` discloses published
Table 8 differences; `wage_receipt.json` records unmatched IDs and source hashes.
`fiscal_sensitivity.json` records all account scenarios, dependencies and twelve
gates, including exact proposed-v9 and stored-school-companion agreement in both
accounting bases. Its extra response-zero, half-response, direct-0.836 and
near-proportional-0.93 rows are diagnostics/scenarios, not new empirical findings.

## Source-read and verification log

2026-10-15; original evidence read before comparison with prior interpretations:

| Source | What was read and used | Limit |
|---|---|---|
| Census F-33 original 2000/2010/2019 files and 2010/2019 Table 8 | Existing source-manifest URLs and pinned bytes; own-year enrollment, current/instruction spending, state/ID alignment, every component identity, published national comparison | Released administrative records, not district invoices; matched IDs do not prove fixed boundaries |
| [Census FY2019 dictionary](https://www2.census.gov/programs-surveys/school-finances/tables/2019/secondary-education-finance/school19doc.doc) | Item definitions, charter treatment, per-pupil adjustments, California reporting change | Exact published/raw discrepancy was disclosed, not fully decomposed |
| [NCES FY2019 dictionary](https://nces.ed.gov/ccd/pdf/2021306_FY19F33_Documentation.pdf) | Membership, imputation, summary items and historical definitions | NCES and Census releases differ: did not impose NCES's FY2009 definition break on Census bytes |
| [NCES CWIFT](https://nces.ed.gov/programs/edge/economic/teacherwage) | Original 2019 ZIP LEA member and [codebook](https://nces.ed.gov/programs/edge/docs/EDGE_ACS_CWIFT_FILEDOC.pdf); no prior local CWIFT file; exact district-ID join | Labor-price estimate, not all input prices; estimate uncertainty not propagated |
| [Lee–Scafidi original paper](https://edworkingpapers.com/sites/default/files/ai25-1266.pdf) | Methods pp. 17–19, Table 4, appendices; growth/decline distinction and percentage-change functional form | Twenty-year association is not a causal removal elasticity; did not import its coefficient as a new model parameter |
| [CBO June 2025](https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf) | Education and Appendix A, pp. 10 and 28–30; annual changes and immediate surge estimand | Does not identify the long-run response |

Searches were confined to these source routes: official CBO surge/state-local
education report; NCES FY2019 F-33 documentation; NCES CWIFT2019 download/codebook.
No broad literature sweep or other fiscal channel was opened. The bounded code
review found no material defect in the estimator or fiscal path; deterministic
tests and the clean-export rerun independently check the implementation.

Quantitative construction check: same all-generation population, year, perspective
and account across scenarios; accrual versus cash shown separately; capital
return is not a debt flow; response mappings and scenario bands labelled modelled;
no sum of unrelated offsets; equal/pupil weights and contrary longitudinal
evidence retained. The $5bn materiality rule applies in both directions.
