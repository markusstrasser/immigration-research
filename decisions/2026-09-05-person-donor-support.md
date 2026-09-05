---
date: 2026-09-05
concept: fiscal-donor-population-and-support
status: adopted
trigger: source-definition-and-observed-support-failure
---

# Harmonize nativity and pool the unsupported upper income bands

The [person-unit repair](2026-09-05-material-inference-repair.md) exposed a second population mismatch. SIPP `EBORNUS` measures US birthplace; ACS nativity also classifies people born in US island areas or abroad to US-citizen parents as native. The official SIPP dictionary's `ENATCIT` codes 4/5 identify those categories. Acquired citizenship codes 1–3 remain foreign born. [SOURCE: [Census nativity definition](https://www.census.gov/topics/population/foreign-born/about/faq.html), [SIPP dictionary, pp.915–917](https://www2.census.gov/programs-surveys/sipp/tech-documentation/data-dictionaries/2024/2024_SIPP_Data_Dictionary.pdf)]

After harmonization, the fine foreign-born donor grid has no `<HS × age 45–54 × income $150k+` donor. It represents 25,571 ACS adults, 0.076% of that target population. The strict join correctly refuses to produce a silently restricted full-stock estimate. [DATA: `.scratch/repair-validation/pooled-donors/pooling_validation.json`]

The adopted rule combines $75–150k and $150k+ into $75k+ **globally**, for both nativities and every recipient, while retaining the other age, education and income bands. The rule was chosen from covariate support before inspecting the resulting fiscal changes. It assumes transport within the coarser band. It does not estimate the missing fine-cell mean. Supported-cell-only estimation is a valid alternative for a restricted target population, but would not answer the declared full-stock descriptive question. Assigning zero or an undisclosed neighboring-cell mean is not an acceptable missing-data treatment. [INFERENCE]

Both grids now have 64 cells and complete recipient coverage. Pooling preserves all donor counts, weights and weighted dollar sums, but need not preserve ACS projections because recipient and donor composition differ inside the pooled band. It changes the specification for 24.13% of foreign-born ACS adults. On the originally supported foreign-born population, the mean proxy changes from $3,608.39 to $3,657.82; mean absolute cell reassignment is $588.05 per adult. This is a measured sensitivity, not a confidence interval. Minimum donor count is seven and 295,247 ACS adults rely on cells with fewer than ten donors. Complete support does not establish adequate precision. [DATA: pooling validation]

The [repair report](../research/immigration-material-repair-report-2026-09-05.md) records final results, limitations and verification. Revisit this choice with larger compatible donor samples, justified partial pooling, or a changed target population; do not choose bins to manufacture a fiscal ranking.
