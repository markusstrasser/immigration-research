**Verdict:** The historical healthcare multiplier remains unvalidated for current complete spending. Actual 2023 administrative data show a large residual that published institutional care cannot explain by itself; they do not identify a uniform or ethnic correction. The useful identified change is to compare enrolled member-years rather than everyone ever enrolled. [CALCULATION / INFERENCE]

## Executed national comparison

| CY2023 quantity | MEPS raw | MEPS × inherited 1.5432 | CMS administrative |
|---|---:|---:|---:|
| Medicaid/SCHIP service spending / Medicaid administrative spending | $278.156bn | $429.250bn | $877.2bn |
| Member-years | 69.585m | same denominator | 94.0m |
| Dollars/member-year | $3,997 | $6,169 | $9,332 |

[SOURCE / CALCULATION] CMS national inputs are the actual [2026 Beneficiary Profile page 15](https://www.medicaid.gov/medicaid/quality-of-care/downloads/beneficiary-profile-2026.pdf), with five eligibility groups' enrollment, expenditure and rate values saved in `cms_national_2023.csv`. MEPS results use staged HC-251 and the existing parameter; outputs are `meps_national_2023.csv` and `national_scope_comparison.csv`. CMS total rate is calculated from its rounded published totals. The $447.950bn difference (51.07% of CMS spending) is a **mixed-scope gap**, not a proven survey error or missing Mexican-origin expenditure.

[CALCULATION] MEPS has 81.353m ever-covered people but 69.585m member-years. Using member-years raises the raw rate from $3,419 to $3,997, **16.91%**. The equivalent age-group changes are 10.74% (0–20), 20.36% (21–64), 26.53% (65+). This is an identified denominator correction for this diagnostic; it changes no annual ledger dollars. No unknown monthly coverage was encountered. Conditional design SE for the calibrated national rate is $368, excluding calibration/scope uncertainty.

## Scope explanations quantified

[SOURCE / CALCULATION] The observed [2023 LTSS workbooks](https://www.medicaid.gov/medicaid/long-term-services-supports/downloads/ltss-data-notes-taf-users-expenditures-2023.zip), A2 sheet `A.2.1 All-Total`, report $228.649900bn total, consisting of $82.739761bn institutional and $145.910139bn HCBS spending. Its institutional sheet identifies $0.060903bn mental-health DSH; that is already excluded from Scorecard, so the subtraction below removes it from LTSS first.

| Scope stress applied only to CMS comparator | Remaining gap versus calibrated MEPS |
|---|---:|
| Subtract published institutional LTSS excluding DSH | $365.271bn |
| Subtract **all** published LTSS excluding DSH, including overlapping home care | $219.361bn |

[INFERENCE] Published institutional care is only about 18.5% of the original gap. Even the much broader subtraction leaves a material remainder. **These are scale tests, not exact adjustments or hard lower bounds:** TAF encounter/service payments differ from CMS-64 cash, and LTSS data quality is incomplete. California HCBS spending receives high concern ratings for both FFS and managed care; CA/TX institutional spending receives medium concern ratings. The EX.5 per-capita quality assessment is low concern in both states. The different assessments must not be conflated. [SOURCE: downloaded workbook, `DQ Measures`; Scorecard API `notes`; [LTSS methodology](https://www.medicaid.gov/medicaid/long-term-services-supports/downloads/ltss-users-ident-method-2023.pdf).]

[SOURCE / CALCULATION] Actual Scorecard EX.2 **FY2023** rows put Medicaid managed-care payments at **$488.402bn**, CHIP total at **$23.395bn**, and total Medicaid spending including administration at $894.244bn. These are scale comparisons only: FY and CY differ. Capitation cannot simply be subtracted: MEPS already imputes the services financed by those payments. The required bridge is capitation less comparable service payments, including insurer overhead/retained amounts and payment timing; this lane does not observe it. CHIP is included in the MEPS coverage concept but excluded by EX.5, so that difference does not straightforwardly explain why MEPS is lower. [Sources: pinned production API EX.2, `cms_fy2023_service_spending.csv`; [MEPS HC-251 expenditure documentation, C-117](https://meps.ahrq.gov/data_files/pufs/h251doc.pdf).]

## State and eligibility checks

[SOURCE / CALCULATION] All actual EX.5 rates, including its five eligibility groups, were acquired. Selected 2023 rates are:

| Eligibility | California | Texas |
|---|---:|---:|
| Total | $8,416 | $9,133 |
| Children | $3,574 | $5,276 |
| Non-expansion, non-disabled adults | $4,489 | $6,323 |
| Aged | $17,309 | $16,946 |
| Disability | $35,443 | $28,289 |
| ACA expansion adults | $7,034 | Not applicable/missing; not zero |

[CALCULATION] Reconstructing the canonical age/birth donor model on matching 2023 CPS inputs gives calibrated state spending of $47.178bn CA and $36.943bn TX. Dividing by the available CPS combined-coverage member-year bounds yields **$4,678–4,950 in CA** (41.2–44.4% below CMS) and **$8,784–9,917 in TX** (−3.8% to +8.6%). These are not sampling intervals or exact eligibility comparisons. They combine reported coverage, state composition and national transported costs; they do not identify a state multiplier. The reconstruction applies the canonical civilian restriction, excludes post-reference-year infant spending, and uses the canonical observed Mexican-origin union. [SOURCE: `cps_transport_2023.csv`, `state_comparison_2023.csv`.]

[CALCULATION] The direct national MEPS result includes 141 positive-weight records with negative `AGE23X`: 2.566m weighted people and $9.228bn raw spending, 3.32% of the total. The age table retains them explicitly as `age_unknown_or_out_of_scope`, and all age rows reconcile to the national total. The canonical transported donor model excludes these records because it requires nonnegative end-year age. This lane discloses that exclusion rather than substituting the different `AGELAST` concept; a last-eligible-age donor model would be a separate sensitivity. [SOURCE: `meps_national_2023.csv`, `audit.json`; [HC-251 documentation, C-22](https://meps.ahrq.gov/data_files/pufs/h251doc.pdf).]

## Disposition and gaps

[INFERENCE] Retain 1.5432 as a declared historical assumption, not an administratively validated contemporary correction. The much larger administrative spending scope is real; its allocation to current civilian households requires further payer/service/enrollment reconciliation. No observed number here identifies a Mexican-origin adjustment. The administrative source lacks that origin detail, and the MEPS matching cells do not recover disability/ACA eligibility or state-specific costs. No institutions were added, no residual distributed, and no canonical model changed.

[GAP] Exact state eligibility expenditures/member-months are not in the published EX.5 API response, though national eligibility totals are available. Separating CHIP in MEPS, territory spending, institutional residents' non-LTSS services, Medicare premiums, insurer overhead, cash/service timing and administrative undercoverage remains necessary for a matched comparison. State age-only proxies cannot substitute for administrative eligibility. Future work should use the released state numerators/denominators if CMS makes them available, or restricted TAF/MEPS state data with appropriate approval.

Validation: eight tests pass, including member-year/ever-enrolled distinction, unknown coverage bounds, reference-year infant exposure, civilian and canonical-origin domains, age residual reconciliation, full-design zero-domain PSUs, missing expansion values, source/output hashes and exclusion of scope tests from corrections; Python compilation passes. Nine newly acquired raw files total 8,224,811 bytes. Code covers source acquisition, matched-year donor reconstruction, national and CA/TX diagnostics, LTSS scope stresses and provenance. Skipped: exact unavailable state eligibility counts, complete cash/service reconciliation, and group recalibration; reasons above.
