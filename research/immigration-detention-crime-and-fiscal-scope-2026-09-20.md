# Immigration detention, ordinary offenses and government costs

Date: 2026-09-20. [MEASUREMENT / ACCOUNTING] Civil immigration custody,
immigration-only criminal offenses, other criminal offenses and institutional
residence are different outcomes. Removing immigration custody from a crime
comparison does not remove its government cost. This scope clarification follows
the user's instruction; it does not change the project's welfare objective.

## What our sources can separate

| Source and outcome | Separation available | Permitted interpretation |
|---|---|---|
| ACS PUMS `TYPE`/`TYPEHUGQ=2` | No detailed institutional type or offense; no ICE-custody flag | Institutional-residence share only. Includes correctional and noncorrectional institutions and can include immigration detention. |
| Texas Light–He–Robey 2012–18 felony arrest charges | Named offense categories and legal-status groups; civil ICE detention is not a felony arrest charge | Compare named ordinary offenses with matched population denominators. Arrest charges are not convictions, people or proven incidents. Broad residual categories need their own scope check. |
| BJS sentenced state-prisoner stock by offense | Criminal state-prison custody and broad offense groups; different population from ICE civil detention | Prisoner composition, not all offending. Hispanic is not Mexican-born or an immigrant-generation category; stock reflects sentence length as well as admissions. |
| USSC federal sentencing Table 9 | Primary immigration offense group can be separated | Primary offense is not all conviction counts. The category also includes smuggling and document crimes; it does not establish immigration-only cases. Citizens include naturalized immigrants. Covers sentenced federal cases, not all crimes or civil custody. |
| ICE detention records | Custody system, facility and dated criminal-history classifications where supplied | ICE custody and resource use. A prior conviction, pending charge and no recorded conviction/charge are distinct; none identifies an ordinary offense committed during the current detention spell. |

[SOURCE: [2024 ACS dictionary](https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/PUMS_Data_Dictionary_2024.pdf),
`TYPEHUGQ`; [Census group-quarters definitions](https://www2.census.gov/programs-surveys/decennial/2010/technical-documentation/complete-tech-docs/summary-file/aiansf.pdf),
Federal Detention Centers; [Texas methods](https://www.pnas.org/doi/10.1073/pnas.2014704117);
[held institutional producer](../infra/immigration-fiscal/acs_institutional_2026_09_16/pull_and_compute.py);
[BJS/Texas coverage](immigration-crime-race-ethnicity-2026-09-05.md).]

The ACS origin rows use Mexican Hispanic self-identification crossed with
nativity. They are not exactly a Mexico-birthplace population. Their native side
pools second and later generations; native white and Black comparators also
include immigrants' US-born children. Restricting ages to 18–39 does not identify
institution type or perform exact within-band age standardization. [SOURCE:
the producer above and its `acs_institutional_rates.csv`.]

## Reporting rule and affected claims

Every comparison must name its outcome, population/comparator, time window,
offense coverage, and whether immigration detention/offenses can be excluded.
When separation is unavailable, state that at the claim, not only in a distant
methods note. Use “institutionalized” for the ACS measure. Do not translate it
into “committed crimes,” “convicted,” or a detention-adjusted incarceration rate.

An ICE administrative count cannot simply be subtracted from an ACS weighted
estimate: geography, date or person-time, coverage, origin, age, sex and overlap
must match. Civil custody and a person's criminal history are separate axes, so
“has a conviction” is not a mutually exclusive alternative to “in ICE custody.”
Removing all detention from a crime numerator also does not establish that those
people have no criminal history. [MEASUREMENT PRINCIPLE]

The legacy `crime_cost_2026_09_16` A2 route multiplies ACS institutional shares by
a BJS Hispanic/white sentenced-prisoner offense mix and unit costs. This is a
conditional proxy scenario, not an observed Mexican-origin ordinary-crime cost.
Its native-only population does not solve the noncorrectional-institution issue.
The `institutional_bound_2026_09_17` cost arms likewise assign hypothetical costs
to unsplit institutions, not measured detention or prison costs. The historical
lineage consumer imports A1/A2 and Texas rates; it does not add missing offense,
detention or generation information. [SOURCE: `crime_cost.py:route_a2`,
`compute_bound.py:cost`, `lineage_cost_2026_09_19/inputs.py:crime_rates`.]

Those scenarios remain reproducible, with this qualification governing their
reuse. They are not newly added to the current national account. The existing
[crime-harm rule](immigration-policy-causal-evidence-2026-09-20.md#crime-harm-rule)
already keeps unmatched crime valuations outside that total.

## Federal, state and local detention costs

**Later September20 completion audit:** [all-vintage federal accounts now reconcile](../infra/immigration-fiscal/detention_reconciliation_2026_09_20/README.md).
The public data do not identify a unique detention total: older-funding ERO
payments mix custody and other missions; fee and shared costs need allocation;
national local-finance records lack ICE-purpose expenses matched to receipts.
The $2.917bn subtotal is gross observed custody payments, not consolidated net
cost. The records specification and acquired data establish this limitation
without treating missing costs as zero or broad enforcement as detention.

**September 20 follow-up:** [Actual FY2024 payments are now verified](../infra/immigration-fiscal/detention_evidence_2026_09_20/ACTUAL_SPENDING_FY2024.md).
Two explicitly identified federal Custody Operations accounts report $2.917bn
in outlays, separately from $3.438bn obligated. The initial gap below is therefore
narrowed to a complete all-funding-vintage federal and consolidated local total;
the observed subtotal is neither zero nor the entire national cost.

The [acquired detention bundle](../infra/immigration-fiscal/detention_evidence_2026_09_20/RESULT.md)
pins the primary records, source definitions and reproducible probes:

- **ICE FY2024:** average daily population 37,721.8 and 13,806,180 midnight
  detainee-days over the 366-day fiscal year. The year-end stock is separately
  37,684. Recorded conviction/pending-charge/history categories describe people
  in civil ICE custody; they are not separate criminal-sentence populations.
- **BJS June 2023 local jails:** approximately 7,000 people held for ICE (standard
  error 594). They may also appear in ICE custody statistics: do not add the two.
- **SCAAP FY2024:** $144,957,461 in awards across 485 applications, based on
  July 2022–June 2023 custody. This reimburses eligible state/local criminal
  custody, not civil ICE bed contracts. Awards are not verified cash outlays;
  unknown-status inmate-days are not all confirmed undocumented days.
- **USSC FY2024 Table 9:** separates the primary immigration offense group,
  but that includes smuggling and document offenses and does not report every
  conviction count. It cannot strictly identify immigration-only cases.
  Citizens also appear in that group: excluding the entire category would remove
  some conduct that citizens can commit, not just entry/status violations.

[SOURCE: source manifest and probe receipts in the linked bundle; ICE FY2024
workbook, BJS Table 12, SCAAP award table/solicitation, USSC Table 9/Appendix A.]

No actual FY2024/25 detention-spending total has been verified in this bundle.
ICE's FY2025 budget justification reports an estimated **FY2023** direct adult
bed cost of $187.48/day; it is not an observed FY2024/25 unit cost or marginal
cost. Appropriations and budget targets are retained with their original labels,
not converted into actual outlays. The FY2025 custody workbook also ends before
fiscal year-end and cannot be annualized as a completed year. [SOURCE: linked
bundle, ICE Strategic Context p5 and workbook footnotes.]

For a matched period and accounting basis, let F be direct federal detention
expenditure, T federal payments to state/local providers, L those providers'
detention expenditure, and R other external recoveries:

```text
Federal budget cost = F + T
State/local net budget cost = L - T - R
Consolidated government cost = F + L - R
```

Transfers between governments cancel in consolidation; detention services do
not. A federal payment to a private provider remains government spending, not an
intergovernmental transfer to subtract. A county can receive more reimbursement
than its narrowly reported incremental cost while the combined government cost
is still positive. Show gross local spending and reimbursements separately.
[ACCOUNTING IDENTITY; cash/accrual, period and program scope must match]

Appropriations, requested budgets, obligations, outlays, contract ceilings,
reimbursement awards, daily population and bed-days are different measures.
Do not call a budget request observed spending or multiply annual admissions by
a full-year bed cost. A population snapshot is not annual person-time.

Existing consolidated government totals already cover spending within their
declared national-account boundary. Any detention breakout must reconcile to
that boundary before it becomes an additional cost; the same corrections or
detention expenditure cannot be added through both a fiscal ledger and a
crime-cost unit price. Group attribution and marginal policy savings remain
separate from observing actual total spending. [SOURCE:
[complete-account boundary](immigration-complete-annual-account-2026-09-20.md),
[BEA government accounting](https://www.bea.gov/resources/methodologies/nipa-handbook/pdf/chapter-09.pdf).]

No automatic victim-harm price is attached to civil detention or an immigration-only
offense. Separately observed violence, fraud or other harm is measured on its own
outcome. Actual enforcement, adjudication and custody resources remain fiscal
costs under the chosen policy. [FRAMING-SENSITIVE; operator instruction]

## Audit boundary

Reviewed the ACS producers, their institutional-bound and crime-cost consumers,
the lineage consumer, and the current fiscal/crime summaries. Historical text is
retained with dated qualifications at the main points of reuse. No raw counts
were altered, no ICE count was subtracted from ACS, and no new causal cost or
detention-adjusted crime ratio is claimed. LLM-assisted framing is checked in
both directions: custody is not automatically offending, and excluding it from
crime does not make its spending disappear.

## Revisions

- 2026-09-20, later completion audit: expired-funding USAspending and SF133 records
  plus Treasury now reconcile account-wide actual payments. Custody allocation
  and local matched-ledger gaps remain. [Evidence and records specification](../infra/immigration-fiscal/detention_reconciliation_2026_09_20/README.md).

- 2026-09-20, follow-up: DHS year-end execution records establish an actual federal
  custody-outlay subtotal; the earlier gap now concerns completeness and
  consolidation. [Source](../infra/immigration-fiscal/detention_evidence_2026_09_20/ACTUAL_SPENDING_FY2024.md),
  [accounting decision](../decisions/2026-09-20-separate-detention-offenses-and-spending.md).
