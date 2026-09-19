# Healthcare donor sensitivity: current adult residents

**Verdict:** Adding education or insurance to the medical transport changes annual healthcare costs enough to matter for fiscal comparisons. Education matching is a useful sensitivity, but this run does not establish it as a better point estimate: its education crosswalk excludes a substantial ambiguous share and several donor means have large sampling errors. Detailed origins share pooled US/not-US donor rates; their differences remain transported scenarios.

## Executed comparison

[MODEL OUTPUT] Positive annual public healthcare cost per resident, 2024 dollars, income-year-2024 CPS ASEC 2025 civilian household residents aged25–64. Education is current attained education. Public medical charges include the annual account's joint Medicaid/Medicare M calibration; these are healthcare costs alone, not net fiscal balances. The canonical model conditions on age and US/not-US birth. Education and insurance columns add those donor dimensions separately. All models and outcome definitions are retained in `derived/estimates.csv`.

| Origin/reference | Education | Canonical cost | Education match cost | Insurance match cost | Education minus canonical (joint SE) |
|---|---|---:|---:|---:|---:|
| Mexico-born | Below HS | $2,382 | $3,147 | $3,142 | +$765 ($847) |
| Other Central America | Below HS | $1,903 | $2,950 | $2,206 | +$1,047 ($678) |
| Caribbean | Below HS | $2,034 | $3,000 | $3,932 | +$966 ($713) |
| South America | Below HS | $1,955 | $2,845 | $2,837 | +$890 ($675) |
| Southeast Asia | Below HS | $2,652 | $3,371 | $5,112 | +$719 ($979) |
| All native | Below HS | $3,215 | $11,176 | $6,890 | +$7,961 ($3,153) |
| Third-plus NH-white | Below HS | $3,311 | $11,438 | $6,638 | +$8,127 ($3,150) |
| Mexico-born | HS only | $1,988 | $3,630 | $2,524 | +$1,642 ($1,350) |
| Other Central America | HS only | $1,565 | $2,612 | $1,978 | +$1,048 ($837) |
| Caribbean | HS only | $2,230 | $4,198 | $2,610 | +$1,968 ($1,643) |
| South America | HS only | $1,833 | $3,220 | $2,106 | +$1,386 ($1,140) |
| Southeast Asia | HS only | $2,601 | $5,105 | $2,500 | +$2,505 ($2,113) |
| All native | HS only | $3,102 | $3,885 | $3,906 | +$783 ($327) |
| Third-plus NH-white | HS only | $3,263 | $4,073 | $3,648 | +$810 ($350) |

[SOURCE: `derived/estimates.csv`, `band=25_64`, `outcome=calibrated`, `model=canonical/education_backoff/insurance_backoff`. Here all adult targets pass the support screen, so backoff has zero weight. The SE is for the **paired donor-model change**, including shared MEPS covariance, not the SE of either individual mean.]

The education model uses donors aged25+ to reduce ongoing-schooling ambiguity. The age-only adult-donor control changes the canonical annual figures little in these rows: Mexico-born below-HS education delta is +$772 against that control versus +$765 against canonical; HS-only is +$1,657 versus +$1,642. For native below-HS it is +$7,953 versus +$7,961. Thus the large differences above are not principally caused by removing age18–24 donors. [SOURCE: `delta_vs_adult_age_birth` and `delta_vs_canonical` on those same rows.]

The direction is not uniformly toward higher costs: BA+ costs for Mexico-born change from $1,891 to $826 with education matching; native BA+ changes from $3,008 to $1,232. This exposes the education gradient the original age/birth model cannot represent. It does not validate the gradient's magnitude. [SOURCE: same table, `education=ba_plus`.]

For a concrete same-education comparison, Mexico-born below-HS medical cost minus all-native below-HS cost is −$834 under canonical matching, −$8,029 under education matching, and −$3,748 under insurance matching. The paired sampling SEs of those comparisons are $643, $3,473 and $973. These constructions are sensitivity scenarios, **not three measurements or a confidence interval over model validity**. [SOURCE: `derived/native_contrasts.csv`, calibrated, age25–64, same-education all-native reference.]

## What the support checks do and do not establish

[MEASURED SAMPLE SUPPORT] The MEPS file has 18,683 positive-weight records and 264 observed survey PSUs. Every domain variance retains that full design. There are10 canonical donor cells,8 adult-age/birth cells,32 education cells and26 insurance cells. All education cells pass the chosen n≥30, Kish ESS≥20, at least two PSU screen. The smallest education cell has30 records and ESS24.06. One insurance cell fails (foreign-born uninsured under18: n27); it has no weight in the adult targets here. [SOURCE: `audit.json`, `donor_cells.csv`, `target_support.csv`.]

Passing that screen does not imply precise means. Native-born below-HS donors aged25–34 have n89, ESS60.85, calibrated mean $8,505 and SE $5,232. At35–49 the corresponding n131, ESS94.04, mean $13,469 and SE $8,013. Foreign-born HS-only donors aged50–64 have n178, ESS127.62, mean $8,542 and SE $5,117. These noisy cells help explain the large uncertainty after education matching. [SOURCE: `donor_cells.csv`, `model=education`.]

**Education harmonization remains incomplete.** The conservative HIDEG/EDUCYR crosswalk leaves HIDEG=7 “other degree” and other unmapped/missing values unresolved. Among eligible MEPS adults aged25+ with known US birth, this excludes23.761 million of186.489 million weighted native-born people (12.74%,1,342 of11,050 records), and4.440 million of46.983 million foreign-born people (9.45%,233 of2,692 records). This donor exclusion is different from CPS unsupported-target mass, which is zero here. The model assumes the classifiable donors represent each mapped education category; no test here validates that assumption. [SOURCE: `audit.json:education_unknown_by_birth`; crosswalk source and exact codes in README.]

Insurance matching is an alternative conditioning choice, not a causal adjustment: program eligibility, enrollment and health can jointly determine coverage. MEPS65+ categories remain pooled. Neither richer model identifies costs by legal status, admission channel, exact origin or entry education. All foreign-origin profiles within a donor cell receive the same cost. [SOURCE: declared matching keys and codebook contracts in README; INFERENCE about identification limits.]

## Handoff for lifetime and fiscal integration

The run writes2,940 annual estimates,5,880 same-education native/white contrasts and1,260 age-specific donor-model differences. `age_deltas.csv` includes six adult age bands for every origin/education; it checks identical CPS records and weighted population between each comparison. Positive medical deltas reduce a fiscal balance by the same amount. The joint arrays preserve both cross-age and cross-model sampling correlation. Exact API, matrix ordering and a survival-weighted combination formula are in README. [SOURCE: output schemas and `audit.json`.]

Artifacts: `medical_uncertainty.npz` has covariance152×152; per-person gradients2,940×152; CPS per-person replicates2,940×161; age-delta gradients1,260×152; age-delta replicates1,260×161. Full-weight estimates reconstructed from exported gradients have maximum dollar error below4e−12. Source/output freshness passes. Three focused tests pass, including an outside-domain PSU case that would fail if the survey frame were improperly subset and a paired-change covariance check. [SOURCE: executed builder/test commands in README.]

Do not add a raw-medical sensitivity delta and the calibrated delta: the latter already includes raw costs and M. The actual M ratios are adjusted-NHEA/MEPS ratios whose numerator excludes institutional care; source verification therefore does **not** support an automatic N/M institutional double-count claim. Institutional N remains separately assumption-dependent. [Primary reconciliation, Tables4–6](https://meps.ahrq.gov/data_files/publications/workingpapers/wp_17003.pdf).

Retained limits: the historical calibration multipliers are fixed; no uncertainty from the education crosswalk, donor transport validity or future policies is included in sampling SEs. The report makes no policy-effect or total lifetime-cost claim. LLM-assisted model selection can favor a construction; retaining all attempted donor models and their disagreement makes that choice inspectable.
