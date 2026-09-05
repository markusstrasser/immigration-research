# Native comparisons and the recent immigration cohorts

**Later same-day extension:** The [current integrated findings](immigration-clarity-update-2026-09-05.md) complete the broader2024 fiscal, admission and conduct checks proposed below and add separate Black wage/crime groups and recording/undercount sensitivities. This memo's2019/2024 arrival-cohort results and narrower2023 fiscal account retain their stated scope.

**Verdict:** The repaired partial fiscal model gives all US-native adults a higher mean than Mexico-born adults. The newer arrival cohort also differs materially from its pre-2021 counterpart, but the differences run in several directions: employment is higher, real earnings lower and the graduate share lower. Recent Mexican arrivals improve on education and earnings. Somalia-born residents are a very small share of the measured recent cohort. None of those descriptive findings identifies a policy effect, a complete fiscal balance, religion or extremist conduct. [DATA; INFERENCE: computations and sources below]

Date: **September 5, 2026**. Frame: resident characteristics, public-budget components and policy effects are separate outcomes. Birthplace is the grouping variable; US-born Mexican Americans belong in the native group. This is an LLM-assisted analysis, with adverse and favorable findings retained and uncertainty reported. It supplements the [material repair report](immigration-material-repair-report-2026-09-05.md), rather than changing the central research question.

## What the native–Mexico comparison now establishes

Per adult aged **25–64**, annual **2023 dollars**, the existing SIPP-to-ACS model yields:

| Population | Modeled employee payroll taxes | Allocated SNAP/TANF/SSI | Partial balance |
|---|---:|---:|---:|
| All US-native adults | $4,128 | $421 | **$3,708** |
| Native non-Hispanic white adults | $4,408 | $375 | $4,033 |
| Mexico-born adults | $2,668 | $297 | **$2,371** |
| All foreign-born adults | $3,870 | $210 | $3,661 |

[DATA: `fiscal_comparison_2023.csv` generated below; existing 64-cell native and foreign-born SIPP donor grids, reference calendar 2023, applied to the full national ACS2023 person sample. Native and foreign-born groups overlap neither; white natives are a subset of natives, Mexico-born a subset of foreign-born. These are different populations, not identical people under alternative migration policies.]

The all-native partial mean is **56.4% higher**, a **$1,336.60** gap. Its decomposition is a $1,460.34 modeled payroll advantage **minus $123.74 more selected transfers received by natives**. Thus this calculation does not substantiate “Mexicans receive more welfare.” It covers three allocated programs, not all assistance, and excludes children’s allocated shares from the adult denominator. The former 70% gap used white natives as the comparator. [DATA: `summary.json`; allocation details in the [repair report](immigration-material-repair-report-2026-09-05.md)]

SIPP targets the civilian noninstitutionalized population, whereas the older ACS recipients included institutional residents and military personnel. A like-target sensitivity excludes ACS `RELSHIPP=37` and `ESR=4/5`: all-native **$3,757**, Mexico-born **$2,383**, gap **$1,374**. This removes 2,567,975 native and 65,827 Mexico-born weighted adults from the old recipient population. The ranking survives; retrospective SIPP and current ACS universe membership still cannot be made identical. [DATA: old/new weighted denominators in the fiscal output; SOURCE: [SIPP2024 guide](https://www2.census.gov/programs-surveys/sipp/tech-documentation/methodology/2024_SIPP_Users_Guide.pdf), section2.1.1]

A stronger check uses **ACS earnings directly**, avoiding the SIPP payroll transport. Applying the same employee payroll formula person by person produces $4,110 for all natives and $2,600 for Mexico-born adults. The payroll-only gap is **$1,509.59**, ACS sampling 95% interval **$1,486.88–$1,532.30**. This confirms a substantial earnings/payroll difference in the measured population. It does not validate the benefit transport or actual tax compliance: the formula treats positive earnings as wage-equivalent, and ACS earnings span a rolling prior year. [DATA: full-replicate difference in `summary.json`; formula in `build_federal_microsim_sipp_2024.py`]

**Three different questions remain distinct:** whether one group's mean exceeds another's; whether either group's full fiscal balance is positive; and how admitting an additional person changes incumbent outcomes and budgets. The first result does not settle the other two. For the same adult accounting comparison, write full net contribution as partial balance plus omitted net components. Mexico's omitted net contribution would have to exceed natives' by **more than $1,337 per adult** to reverse the all-adult ranking, or $1,374 for the civilian noninstitutionalized sensitivity. That is a break-even identity, not an estimate that the omitted difference has either sign. Employer and income taxes, credits, health expenditure, children, retirement, public goods and effects on others require compatible attribution and counterfactuals. [INFERENCE; arithmetic from the measured partial gaps]

## What changed in the newer cohort

I acquired the national **2019 ACS PUMS** and used the existing **2024** national files. The comparison is residents observed in 2019 reporting entry in **2016–2019**, versus residents observed in 2024 reporting entry in **2021–2024**. Both contain approximately 0–3 years since entry. Outcomes below cover **civilian noninstitutionalized adults aged25–64**, include people without jobs, and use common **2024 dollars**. Weighted recent-adult populations are 2,885,470 and 4,172,880; actual sample sizes are **21,543** and **30,382**. [DATA; SOURCE: [2019 files](https://www2.census.gov/programs-surveys/acs/data/pums/2019/1-Year/), [2024 files](https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/)]

| Outcome | Earlier cohort, observed2019 | Newer cohort, observed2024 | Change, with 95% sampling interval |
|---|---:|---:|---:|
| Employed / adult population | 65.9% | **68.8%** | +2.89pp [1.86,3.92] |
| Mean annual earnings, including zeros/losses | $41,864 | **$39,163** | −$2,701 [−3,985,−1,416] |
| Bachelor’s degree or higher | 51.0% | **45.8%** | −5.15pp [−6.42,−3.87] |
| Less than high-school completion | 16.8% | **18.7%** | +1.90pp [0.91,2.90] |

[DATA: `cohort_comparison.csv`; all 80 person replicate weights, including negative/zero weights, recompute each ratio. Between-year intervals assume independent survey samples. Earnings use person `ADJINC/1,000,000`, then the [Census-recommended R-CPI-U-RS](https://www.census.gov/programs-surveys/acs/guidance/comparing-acs-data/2024.html) factor462.5/375.8 for2019→2024. These intervals cover sampling, not survey undercoverage or causal uncertainty.]

The adverse earnings difference is **6.5%**, while the education profile remains mixed: a higher graduate share than all native adults in2024 (39.4%) coexists with a much larger low-education share than natives (6.1%). Excluding interview-year entrants leaves the same directions: employment68.8→71.3%, earnings$43,414→$40,080, graduate share51.4→45.8%. [DATA: same output, `entry_1_3`; no causal inference]

**The employment/earnings pattern survives explicit standardization.** Among entrants1–3 integer years since entry, assigning the same equal weights to all24 age-band × sex × duration cells in both surveys gives **+2.97pp employment** (95%CI1.57–4.38) and **−$4,247 mean earnings** (−$6,271 to−$2,224). Equalizing duration alone gives+3.23pp and−$2,838. This defines synthetic balanced populations, not national averages; age is held in four ten-year bands, and education/origin composition remains unconditioned. The smallest recent-cohort cells have210 and252 sampled adults, with positive denominators in every replicate. Native age/sex-balanced earnings rise$2,361 over the same period. The decline is not shared by this measured native benchmark; common or differential period shocks, selection and within-cell composition remain unresolved. [DATA: `standardization/results.json` and `differences.csv`; INFERENCE]

**Mexico-born newcomers move differently:** mean earnings rise **$28,887→$32,500** in common dollars; the share below high school falls **43.4→37.1%**; graduates rise **20.0→23.0%**. Employment rises69.9→72.1%, but its change interval crosses zero. These figures are about recent Mexico-born residents, not the entire established Mexican-origin population or their US-born descendants. [DATA: `mexico_born/entry_0_3`; earnings change95%CI+$1,059 to+$6,167]

The all-age recent-resident origin mix also changes: Mexico's share11.4→14.1%, India's10.6→8.4%, China's8.1→4.1%, Venezuela's3.3→6.2%, Cuba's2.7→6.0%. This establishes composition change; decomposing its contribution to outcomes requires within-origin comparisons, not merely reading a country label as skill or legal status. [DATA: `origin_mix_2019.csv`, `origin_mix_2024.csv`]

These are surviving, sampled residents. ACS `YOEP` records the **most recent entry to live** in the country, not necessarily first admission. Exact arrival month, emigration, missed residents, admission class and current legal status remain unobserved here. Equal four-year windows need not have equal duration distributions. Period conditions, pandemic exposure, selection and moves also differ. Income can partly precede arrival even after excluding interview-year entrants. Consequently, “newer cohort differs” is supported; “Biden policy caused this difference” is not identified. [SOURCE: [ACS subject definitions](https://www2.census.gov/programs-surveys/acs/tech_docs/subject_definitions/2024_ACSSubjectDefinitions.pdf); INFERENCE]

## Somali-origin claims and current data

In the **2024 all-age recent-entry resident** sample, Somalia-born people number an estimated **7,327 out of7,059,716**, or **0.104%** (sampling95%CI0.063–0.145%). Among recent adults25–64, the share is0.143%:5,961 of4,172,880. At that fixed measured share, even changing subgroup employment from0% to100% could move the recent cohort's overall employment rate by at most **0.143 percentage points**. This is a direct composition bound holding everybody else fixed; it estimates neither spillovers nor local effects. [DATA; arithmetic: `origin_mix_2024.csv`, `summary.json`]

Somalia-born working-age residents as a whole have estimated employment69.4% and mean earnings$29,119, below natives'78.2% and$63,168. But the Somali stock estimate uses only337 sampled adults, and its **recent-entry subset only22**; recent employment's interval is roughly47–83%. The data warrant reporting the measured disadvantage and substantial uncertainty, not an exact recent-Somali fiscal ranking. This measures birthplace, not Somali ancestry, religion, ability or extremist affiliation. A national-origin stock is also not a proxy for all post-2021 arrivals. [DATA; construct boundary]

The newest verified ACS microdata are **2024**, released December4,2025. Census has delayed its2025 ACS release while assessing a disclosure-avoidance order. **SIPP2025**, released July15,2026, covers calendar2024; current **BLS** nativity totals reach August2026 but do not isolate this arrival cohort. “Last four years,”2021–2024 entries, and2025–2026 flows are different windows. The [availability review](immigration-recent-cohort-data-availability-2026-09-05.md) gives official dates, real SSD locations and access gaps. The often-cited [CBO2024 surge analysis](https://www.cbo.gov/publication/60165) already modeled incremental2021–2026 immigration; it is a projection under that vintage's assumptions, not a measurement of all subsequent policies or all-government outcomes. [SOURCE; MODEL]

The targeted **official X API** sample adds111 posts,103 not in the previous sample. The [narrative review](immigration-cohort-narratives-2026-09-05.md) checks the consequential claims: an individual fraud prosecution cannot identify the whole refugee program's incidence, and Numbeo's survey crime index is not crimes per100,000. Posts locate claims; case records, compatible denominators and outcomes must establish their truth. The sample is selective, not an estimate of public opinion. [SOURCE; INFERENCE]

## The work that would most reduce the remaining uncertainty

Six distinct approaches were considered; the first is completed here, with the second the next useful extension. These are proposed empirical routes, not a change to the project's causal tree. [INFERENCE]

| Priority / mechanism | Concrete data and comparison | What would become clearer; what remains outside it |
|---|---|---|
| **1. Comparable resident cohorts** | 2019/2024 ACS person files; fixed age/universe, duration sensitivities, earnings including zeros, replicate intervals | Done: avoids confusing established immigrants with new arrivals and reveals opposing dimensions. Repeated cross-sections remain descriptive. |
| **2. Complete the budget components** | New reference2024 SIPP; income/credit and benefit modules, health spending; direct earnings payroll check; federal and state/local ledgers separately | Estimate whether omitted net components plausibly clear the $1,337 ranking-reversal threshold. Admission eligibility and donor uncertainty must be modeled explicitly. A new SIPP ZIP alone cannot identify legal status or a lifetime effect. |
| **3. Admission selection and work access** | Refugee/RPC, OHSS new-arrival-versus-adjustment records, work-authorization dates, EOIR processing, linked where valid | Separate entry volume, channel mix and time barred from work. Encounters, court cases, status adjustments and residents are not additive people counts. |
| **4. Local capacity and incumbent outcomes** | Actual school enrollment/English-learner needs, rents and completions, hospital use, fiscal outlays and incumbent earnings around plausibly external placement/processing shocks | Test short-run local costs and adjustment. Allocation assumptions and permits alone do not identify marginal expenditures or incumbent losses. Existing BPS/QWI/BEA layers need the exposure and design. |
| **5. Longitudinal persistence** | SIPP/CPS linked observations; tax/admin earnings where access permits; documented attrition/emigration | Distinguish lasting low earnings from entry costs and track employment transitions. Cohort means and age-period-cohort identities do not recover individual progress unaided. |
| **6. Direct conduct and institutional outcomes** | Offense-specific defendants/convictions and matched origin/status denominators; victimization, program losses/recoveries, case selection and referral rates | Test fraud, violence or extremist conduct as defined outcomes. Birthplace, religion, national crime indices and selected prosecutions cannot substitute for the relevant rate. |

The practical stopping rule is decision-specific: settle a named ranking or incidence claim when plausible omitted components cannot change it. A larger collection of loosely related papers will not resolve an undefined ledger, incompatible populations or an unidentified counterfactual. [INFERENCE]

## Reproduction and checks

Tracked generators: `infra/immigration-fiscal/build/analyze_arrival_cohorts.py`, `summarize_arrival_cohorts.py`, `standardize_arrival_profiles.py`; uncertainty/window tests: `infra/immigration-fiscal/tests/test_arrival_cohorts.py`. Generated profiles, 81-replicate estimates, origin shares, fiscal components, source hashes and contrasts live in `.scratch/cohort-clarity-20260905/analysis/`; fixed-weight results and cell sufficient statistics are in sibling `standardization/`. The [dataset register](immigration-dataset-register.md) records raw paths and additional source files. No canonical warehouse was modified for this comparison.

```bash
uv run infra/immigration-fiscal/build/analyze_arrival_cohorts.py --year 2019 --person-data /Volumes/2TBPNY/corpus/census_acs_2019_1yr/csv_pus.zip --database warehouse/immigration_context.duckdb --out .scratch/cohort-clarity-20260905/analysis
uv run infra/immigration-fiscal/build/analyze_arrival_cohorts.py --year 2024 --person-data /Volumes/2TBPNY/corpus/census_acs_2024_1yr/csv_pus.zip --database warehouse/immigration_context.duckdb --out .scratch/cohort-clarity-20260905/analysis
uv run infra/immigration-fiscal/build/analyze_arrival_cohorts.py --year 2023 --person-data /Volumes/2TBPNY/research-data/immigration-fiscal/data/census/acs_pums_2023_person.zip --database warehouse/immigration_context.duckdb --out .scratch/cohort-clarity-20260905/analysis
uv run infra/immigration-fiscal/build/summarize_arrival_cohorts.py --analysis .scratch/cohort-clarity-20260905/analysis --inflation .scratch/cohort-clarity-20260905/availability/inflation.json
uv run infra/immigration-fiscal/build/standardize_arrival_profiles.py --inflation .scratch/cohort-clarity-20260905/availability/inflation.json --out .scratch/cohort-clarity-20260905/standardization
uv run --with duckdb --with pandas --with numpy python3 -m unittest discover -s infra/immigration-fiscal/tests -p test_arrival_cohorts.py -v
```

National raw person counts reproduce official PUMS counts:2019 **3,239,553**,2024 **3,422,888**; weighted totals and published rounded replicate SEs also match. All2023 legacy Mexico/white-native model means reproduce the canonical outputs. An independent reviewer recomputed raw-sample employment and payroll means and their SEs. Four tests cover negative weights, paired covariance, cohort boundaries and invalid denominators. These checks validate calculations, not the causal or omitted-fiscal assumptions. [DATA: manifests, `summary.json`, reviewer artifact `.scratch/cohort-clarity-20260905/fiscal-comparison-review.md`; SOURCE: official PUMS verification CSVs in availability staging]

The independent standardization pass also reproduces all six official national population, male-population and age25–34 anchors across the two years, including their rounded SDR standard errors. Its self-test checks fixed cell weights, losses, cancellation in whole-estimate covariance and rejection of empty or nonpositive cells. [DATA: `standardization/results.json`, generator `--self-test`]

## Revisions

- **2026-09-05:** Added the actual all-native comparison and recent-entry resident analysis under the [cohort-comparison decision](../decisions/2026-09-05-arrival-cohort-comparison.md). The newer arrival sample does not inherit a stock fiscal estimate or an identified assimilation effect.
