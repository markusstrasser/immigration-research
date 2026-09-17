# NYC: what the spending decline and homelessness increase actually measure

**Verdict:** Lower shelter population exposure accounts for essentially all of NYC's FY2024–25 asylum-service spending decline. An approximately flat program-spending-per-census-day ratio does not support a large efficiency improvement. Separately, the best matched homelessness accounting attributes much of the 2022–24 sheltered-count increase to newly arrived people themselves needing shelter; it does not establish that they made existing residents homeless. A joint account of spending and exposure is now computed. Effects on incumbent rents, schooling and welfare remain only partly observed. [DATA; INFERENCE]

## Newly computed exposure and financing

The Comptroller's public chart is backed by an openly readable Google spreadsheet. We downloaded the actual monthly agency and household-type series, not values inferred from a chart image. The agency series is the primary denominator. For each July–June fiscal year, we multiply each monthly mean by calendar days, including February29,2024. These are **approximate census person-days**, not actual occupied bed-nights or unique recipients. The numerator is the June2026 executive-budget report's accrued program spending, including services beyond shelter. [SOURCE: `raw/local/source_manifest.json`; [census](https://comptroller.nyc.gov/services/for-the-public/accounting-for-asylum-seeker-services/asylum-seeker-census/); [Table38](https://comptroller.nyc.gov/reports/comments-on-new-york-citys-executive-budget-for-fiscal-year-2027-and-financial-plan-for-fiscal-years-2026-2030/).]

| Fiscal year | Approximate census person-days | Mean people sheltered | Gross program spending | City-funded portion | Gross spending / census person-day |
|---|---:|---:|---:|---:|---:|
| 2024 | 23,369,664 | 63,852 | $3.752bn | $2.323bn | $160.55 |
| 2025 | 18,678,758 | 51,175 | $3.020bn | $1.477bn | $161.68 |

**What changed:** gross spending −19.51%; exposure −20.07%; gross spending per census-day +0.70%. The exact symmetric decomposition of `cost = exposure × spending/exposure` assigns −$755.78m to exposure and +$23.78m to the ratio, summing to the −$732m observed change. This is accounting, not causal attribution to shelter time limits or federal policy. The ratio mixes service intensity, population composition, timing and prices; it is not a marginal cost or provider productivity measure. [DATA: `derived/local/fiscal_year_exposure.csv`, `audit.json`.]

The city-funded portion falls faster, by36.42%. City funding per census-day falls from$99.40 to$79.07. State/federal funding assignments explain why the local treasury's burden can fall while gross cost per served person remains flat. These are accrued allocations, not cash receipts or net taxes minus all costs. [DATA; same Table38.]

**A source discrepancy survives the check.** Agency and household-type totals differ by up to521 people in January2025, beyond rounding. Using the type series instead gives23,370,455 and18,694,765 census-days and approximately$160.54/$161.54 per day: the substantive conclusion is unchanged. Both series and every monthly difference remain in `monthly_reconciliation.csv`. We do not silently average them or claim exact reconciliation. The share of people in families with children, within the type series, rises76.59%→78.95%. A household-based per diem and a person-based rate can therefore move differently. [DATA]

The archived fiscal page reports household per diems of$373 inFY2024 and$371 inFY2025. These cannot be read as per-person charges. The new population denominator improves on a hypothetical two-or-three-person household conversion, but is still approximate and program-wide. The charts include City-funded facilities; the separately displayed outside-NYC series is a subset and is **not added again**. [SOURCE: [fiscal definitions](https://comptroller.nyc.gov/services/for-the-public/accounting-for-asylum-seeker-services/fiscal-impacts/).]

## A different explanation for the homelessness headline

The current peer-reviewed version is Meyer, Wyse and Williams, *Journal of Public Economics*255(2026),105577, not the older working paper's misleading local filename `gould_2024...`. The [open author-hosted article](https://bpb-us-w2.wpmucdn.com/voices.uchicago.edu/dist/a/3122/files/2026/02/Meyer-Wyse-Williams-JPubE-2026.pdf) is archived with its hash. Its Table1 distinguishes direct administrative counts from an indirect demographic calculation. [SOURCE]

| Area | Increase in sheltered PIT count, 2022–24 | Direct new-arrival estimate | Share of increase | Indirect estimate's share |
|---|---:|---:|---:|---:|
| NYC | 77,352 | 66,700 | 86.23% | 66.06% |
| Chicago | 14,590 | 13,679 | 93.76% | 93.41% |
| Massachusetts | 13,353 | 7,821 | 58.57% | 58.57%* |
| Denver | 6,556 | 4,300 | 65.59% | 72.10% |
| Nationwide | 148,626 | 92,500 | 62.24% | 58.95% |

*Massachusetts reuses the direct estimate in the indirect approach; it is not an independent confirmation. National indirect estimation is performed on national demographic counts, rather than by adding all local estimates. Ratios above reproduce published-table arithmetic; raw HUD re-estimation is not claimed. [SOURCE: Table1 and footnotes; DATA: `published_homelessness_accounting.csv`.]

The strongest supported interpretation is that the recent rise in the sheltered count substantially reflects **additional people being sheltered**, not only worsening housing conditions for an unchanged population. This strengthens the case for a real, concentrated local service burden while weakening the claim that the same headline measures incumbent displacement. The direct NYC count and HUD count may cover different facilities/eligibility; the indirect method assumes a stable counterfactual Hispanic share and can miss non-Hispanic arrivals. Neither construction observes every existing resident's counterfactual housing outcome. [SOURCE: article§§3–5; INFERENCE]

The paper's approximately59–62% range is **not a confidence interval**. Direct and indirect methods are partly dependent. Incumbents displaced into doubled-up housing would escape a test based only on unsheltered counts. Conversely, an increase in measured shelter use can reflect better access/capacity as well as increased need. The result neither establishes no displacement nor an immigration-caused nationwide rent effect. [SOURCE: article caveats; INFERENCE]

## Housing and service quality: evidence that constrains the story

The [2023 NYC Housing and Vacancy Survey](https://www.nyc.gov/assets/hpd/downloads/pdfs/about/2023-nychvs-selected-initial-findings.pdf) reports net rental vacancy1.41%, down from4.54% in2021; survey collection ran January–mid-June2023. It also reports that overall rent burden declined, while median rent/income among renters below$70,000 was54%. The coexistence of very low vacancy and a lower aggregate rent-burden measure illustrates why a single citywide average is insufficient. These are different resident samples and outcomes, not a measured immigration effect or a panel of incumbents. The report was read through the web PDF reader; direct local download returned403 and is not falsely listed as archived. [SOURCE; INFERENCE]

The [May2024 shelter-limit investigation](https://comptroller.nyc.gov/reports/report-on-the-investigation-of-the-implementation-of-the-60-day-rule-for-asylum-seeker-families/) documents absent outcome tracking after families leave and missing requested case files. Its school-disruption accounts are explicitly self-selected anecdotes. Therefore neither fewer shelter residents nor the audit's rhetoric establishes how much the60-day rule changed stable housing, attendance, work authorization or incumbent classroom quality. This is evidence of a consequential evaluation failure; it is not an estimated zero effect. The report's finding is dated2024, not represented as a live2026 audit. [SOURCE]

The downloaded school chart tabs end March2024 and include no adequate contemporary definition of longitudinal student exposure. They are retained as source artifacts, but not turned into pupil-days or a causal enrollment/attendance estimate. The separately held citywide enrollment series cannot identify effects on schools that actually received newcomers. QWI has no nativity field; no native-worker effect is inferred from it here. Renters, owners and workers therefore still lack a common identified outcome panel for this episode. [SOURCE / COVERAGE LIMIT]

## What this resolves and what would discriminate next

- **Leading explanation:** the fiscal decline is mainly fewer census-days; the earlier sheltered-homelessness rise largely includes new arrivals directly. [DATA / INFERENCE]
- **Top alternatives still live:** composition and service changes alter unit spending; shelter exits can shift unmet need outside the measured system; housing displacement can occur without visible street homelessness.
- **Discriminator:** match admissions/exits to subsequent housing, employment and school attendance; compare a credibly assigned policy/capacity change, including nonreturners. Renter outcomes need actual pre-existing residents or a justified stable-population design.
- **Decision impact:** defend the local cost burden in its measured units; reject both “the entire homelessness increase means incumbents lost homes” and “budget savings prove successful integration.” Do not add these shelter dollars again to a fiscal account already containing them.
- **Next action:** service follow-up microdata or a real placement-policy design would change the result. Another citywide correlational regression would not close that gap. This joint case is complete for aligned spending/exposure and partial for full welfare incidence.

Reproduce from repository root: `uv run python3 infra/immigration-fiscal/frontier_execution_2026_09_17/local/stage.py`, then `local/analyze.py` at the same lane path. Network access is needed only for staging missing public inputs. Existing raw snapshots are hash-checked and never overwritten. Python dependencies: requests, pandas, numpy, BeautifulSoup; PDF extraction: `pdftotext`.
