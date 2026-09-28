# Urban housing evidence: local incidence, source scope, and model limits

**Current assessment — 2026-09-05.** Housing supply and migration can interact, and current primary research supplies useful local estimates. The earlier memo overstated what datasets, null results, cross-study agreement, and model calibrations settle. A housing-price effect is not by itself a net welfare or fiscal effect. [INFERENCE]

## The current housing estimate

Wilson and Zhou's **March 2026 working paper** uses administrative unauthorized worker-flow estimates and a two-way leave-out shift-share design for the 2021m3–2024m3 boom. Its housing regressions estimate an inflow equal to **1% of initial employment**, not population, raising house prices about **2.2%** and rents **1.4%**. The paper's Table 6 was checked: rent coefficient 1.438 (SE 0.344), price coefficient 2.189 (0.741). These are substantive local estimates under the paper's identification assumptions. [SOURCE: [Wilson–Zhou, sections 3–4 and 6.1, Table 6](https://www.dallasfed.org/~/media/documents/research/papers/2026/wp2607.pdf)]

Its permit IV estimates are imprecise, not proof of zero supply response. The reported roughly 30%/20% price/rent-growth contributions apply the coefficients to **weighted-MSA** exposure; the authors explicitly distinguish weighted local effects from national effects with spillovers/general equilibrium. The labor-income-per-capita result can reflect composition; lower transfers do not measure the complete fiscal balance. These findings do not identify regulation as the sole constraint or settle long-run/open-borders policy. [SOURCE: same, Table 6 and footnote 23; INFERENCE]

A similar coefficient in another paper does not validate transfer across immigration status, skill, era, population denominator, or housing market. Nonsignificant pretrend tests support a diagnostic; they do not prove an instrument's exclusion restriction. These cautions qualify this study's scope without replacing its evidence with an unrelated repository correlation. [INFERENCE]

## Other numerical anchors

Cabral–Steingress's cited working paper reports average house-price growth of 17% in its sample and a predicted immigration contribution of 1.3%. That means approximately **1.3 percentage points of price growth**, or **7.6% of the 17% increase**; “1.3% of a 17% rise” confuses the denominator. This different sample/calculation is not a direct test of the 2021–2024 worker-flow estimate, and immigrant concentration alone does not mathematically establish a small aggregate effect. [SOURCE: [Bank of Canada working paper](https://www.bankofcanada.ca/wp-content/uploads/2024/10/swp2024-40.pdf), aggregate-effects discussion; CALCULATION]

The Hsieh–Moretti **36% aggregate-growth** statement is a spatial-model result, not a measured immigration effect or a 36% GDP-level loss. It must now be presented alongside **Greaney's published April 2026 replication critique**, which reports code errors, population-unit dependence, and much smaller effects in a modified model. The journal abstract for that critique was verified; its full replication and any response were not adjudicated here. The old memo's unqualified use of this model as a settled quantitative policy bridge is withdrawn. [SOURCE: [original article](https://www.aeaweb.org/articles?id=10.1257/mac.20170388), [Greaney comment](https://www.aeaweb.org/articles?id=10.1257/mac.20230141); GAP]

## What the data can identify

ACS B25064 is **median gross rent**, including the relevant utility costs, not contract rent. ZORI tracks asking-rent changes and ZHVI home values; differences from incumbent contract-rent paths are an estimand distinction, not guaranteed upward bias. These indices do not separately identify renter and homeowner welfare. The downloaded Zillow file inspected here uses a provider **RegionID**, not a documented direct CBSA-code key. Modern CBSA and historical Saiz/PMSA names still need boundary reconciliation. [SOURCE: raw Zillow header; [ZORI methodology](https://www.zillow.com/research/methodology-zori-repeat-rent-27092/), [ACS B25064 definition](https://api.census.gov/data/2022/acs/acs5/groups/B25064.html); INFERENCE]

Public LODES describes commuting/job geography and selected demographic categories; it has **no nativity/status dimension**. It cannot by itself show where immigrants work versus live. Geographic allocation also does not create individual linkage: assigning a metro elasticity to PUMAs does not measure within-metro capacity or resolve multi-area overlap automatically. [SOURCE: [Census LODES technical schema](https://lehd.ces.census.gov/doc/help/onthemap/LODESTechDoc.pdf); INFERENCE]

The actual repository MSA builders calculate correlations using ACS 2023 foreign-born **stock share**, not the study's worker-flow treatment. A second ACS year plus an instrument is not guaranteed to replicate a paper; the treatment denominator, assignment/exclusion assumptions, timing, outcome, weights, and geography must match. The [repaired MSA panel review](immigration-msa-rent-elasticity-panel-2026-06-25.md) states the limits. [SOURCE: tracked builders linked there; INFERENCE]

## Causal synthesis and welfare

Within-neighborhood sorting can coexist with little measured net metro outflow, but that compatibility does not resolve every Card–Borjas identification question. A result among observed nonmovers is evidence on that selected population; it does not by itself identify all incumbents' welfare or rule out displacement. Likewise, a cross-city rent/income ratio cannot show that affected renters' incomes compensated them, and conditioning on nonmoving after an exposure can introduce selection. [INFERENCE]

A naive correlation is not an upper bound without a signed-bias argument. Publication prestige and “against-interest” political positioning are not mechanical evidence grades. The earlier bibliography (removed 2026-09-29; recover with `git show 080ddae:research/immigration-urbanism-frontier-2026-06-25.md`) includes useful competing results, but its remaining paper-specific magnitudes were not independently reread in this bounded audit and should not inherit certainty from these checks. [GAP; INFERENCE]

Housing demand, construction, sorting, productivity, ownership, taxation, and service use can produce different gains and losses. Rent payments transfer income to owners; net resource/welfare accounting needs the chosen population, horizon, and counterfactual. Short-run local pressure does not prove a fixed long-run national or global capacity ceiling. [INFERENCE]

## Revisions

- **2026-09-05:** Checked the primary housing treatment and scope, corrected the contribution denominator and dataset universes, recorded the published Hsieh–Moretti replication dispute, and withdrew causal/welfare and guaranteed-replication overreach. [Decision](../decisions/2026-09-05-material-inference-repair.md).
- **2026-09-29:** Removed the verbatim pre-repair analysis that followed this section; recover it with `git show 080ddae:research/immigration-urbanism-frontier-2026-06-25.md`. [Decision](../decisions/2026-09-29-delete-superseded-and-cruft-docs.md).
