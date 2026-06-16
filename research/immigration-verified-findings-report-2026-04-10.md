# Verified findings report: low-skill immigration, ledgers, datasets, and economist claims

Date: 2026-04-10

## Scope

This report does **not** treat "is low-skill immigration bad for a country?" as a well-posed scalar question. That framing collapses too many ledgers, horizons, and incidence groups into one sign. The defensible question is:

> Under explicit horizons and counterfactuals, which low-skill immigration flows, into which destinations, improve or degrade institutional resilience, local-system capacity, and net citizen welfare, and on which ledger?

[FRAMING-SENSITIVE] [SOURCE: research/immigration-main-question-reset.md]

The report integrates the verified local warehouse work, the survey/economist audit, and the external literature. It also states where the repo still does **not** have enough evidence to make a hard claim.

## Executive verdict

1. The strongest verified result is an **incidence split**, not a scalar verdict. National consumer and employer gains can coexist with local school, housing, and capacity pressure. `High certainty`, `A1/A2`. [SOURCE: research/immigration-unified-scenarios-memo.md] [SOURCE: https://d279m997dpfwgl.cloudfront.net/wp/2016/09/0922_immigrant-economics-full-report.pdf] [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
2. The local warehouse does support a real local-burden story, but for a **narrow operational definition** of low-skill: foreign-born adults ages `25-64`, `YOEP >= 2014`, and `SCHL < 16`. In ACS coding, `SCHL = 16` is a regular high-school diploma, so the current warehouse's `low-skill` group is effectively **less than high school**, not the broader public-use meaning of "non-college." `High certainty`, `A1`. [SOURCE: sources/immigration-fiscal/data/derived/extend_immigration_context_with_pumas.sql] [SOURCE: https://api.census.gov/data/2023/acs/acs5/pums/variables/SCHL.json] [SOURCE: https://api.census.gov/data/2023/acs/acs5/pums/variables/YOEP.json] [SOURCE: https://api.census.gov/data/2023/acs/acs5/pums/variables/AGEP.json]
3. Within that narrow group, origin mix matters a lot. The largest recent low-education origin groups in the warehouse are `Mexico`, `Guatemala`, `Honduras`, `El Salvador`, `Cuba`, and `Haiti`. `High certainty`, `A1`. [SOURCE: DuckDB query on `acs_origin_national_2023` run 2026-04-10]
4. The household-normalized child-burden correction materially improved the analysis, but its verified object is **linked-household child exposure**, not a current full-stock school-burden-per-adult or origin `federal - school` sign. On that linked-household metric, the strongest school-age exposure groups remain `Afghanistan`, `Honduras`, `Myanmar`, `El Salvador`, `Mexico`, and `Guatemala`. June 2026 tensor work now withholds origin school/net rows until numerator and denominator universes match. `High certainty` for the exposure correction; `unresolved` for full-stock origin school/adult net. `A1`. [SOURCE: research/immigration-household-weighted-correction.md] [SOURCE: DuckDB query on `acs_origin_household_national_2023` run 2026-04-10] [SOURCE: research/immigration-school-burden-per-adult-2026-06-15.md]
5. State averages hid real destination sorting. On a `PUMA` basis, some origins are substantially more rent-exposed than the state average suggested. `China`, `Colombia`, `Brazil`, and `Venezuela` are the clearest large-group cases in the current warehouse. `High certainty`, `A1`. [SOURCE: research/immigration-local-burden-puma-layer.md] [SOURCE: DuckDB query on `origin_puma_household_context_2023` run 2026-04-10]
6. The current repo still does **not** support a hard all-in federal or full fiscal number. The April Texas/CPS prototype remains a useful failure trace, but June 2026 work supersedes it for the current narrow federal cash-flow layer with a SIPP-style proxy: payroll/FICA minus SNAP, TANF, and SSI. That proxy is stronger than the old CPS shortcut, but it is not income tax, Medicare/Medicaid, EITC, capital/corporate tax, a household-filing model, or a lifetime NPV. `High certainty` that the old prototype was weak; `Moderate certainty` for the current narrow annual federal proxy; `Low certainty` for any all-in federal number. `A1`. [SOURCE: sources/immigration-fiscal/data/derived/build_federal_microsim_prototype.py] [SOURCE: DuckDB query on `sipp_household_donor_cells_2023` run 2026-04-10] [SOURCE: research/immigration-federal-distribution-findings-2026-06-15.md] [SOURCE: research/immigration-country-fiscal-tensor-2026-06-15.md]
7. The Clark Center economists who agreed are usually **not factually wrong on the channel they are talking about**. The problem is that many are answering a narrower question than readers think: wages, prices, firm efficiency, or average consumer surplus, not a full local-capacity or fiscal ledger. `Moderate certainty`, `A2/B1`. [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/] [SOURCE: research/immigration-clark-respondent-audit.md] [SOURCE: research/immigration-economist-effects-matrix.md]
8. Under an `AGI-soon` frame, long-run lifetime-NPV arguments become less decisive, and short-run adjustment, housing, schooling, and political legitimacy become more central. `Moderate certainty`, `A2/B2`, partly inferential. [SOURCE: research/immigration-agi-reframing.md] [SOURCE: https://docs.iza.org/dp18218.pdf] [SOURCE: https://www.imf.org/-/media/files/research/imf-and-g20/2025/g20-background-note-on-aging-and-migration.pdf] [INFERENCE]

## How this report grades evidence

This report uses two separate grading axes.

### Claim certainty

1. `High`: directly replicated in the local warehouse or explicit in a primary source.
2. `Moderate`: supported by multiple good sources but still model-dependent or indirect.
3. `Low`: prototype-only, donor-based, or dependent on an unresolved measurement issue.

### Source grade

1. `A1`: official data, official documentation, or direct primary text; claim is directly supported.
2. `A2`: high-quality academic paper or major official synthesis; relevant but model-dependent.
3. `B1`: direct survey statement or strong secondary analysis; useful but narrower.
4. `B2`: think-tank or adjacent-source argument; useful context, not decisive on its own.

## How I approached the question

1. I split the problem into ledgers instead of asking for a single sign: labor-market prices, federal budget, state/local budget, housing, descendants, political economy, and `AGI-soon` transition. [SOURCE: research/immigration-unified-scenarios-memo.md]
2. I treated origin, destination, household structure, and time-since-entry as first-order. I did **not** use ad hoc exclusions like "not Japan" or "not the EU." [SOURCE: research/immigration-origin-data-stack.md]
3. I preferred direct public-use geography over fake metro precision. That is why the local warehouse is built around `PUMA`, then bridged outward carefully, rather than pretending ACS microdata identify exact districts or metros. [SOURCE: research/immigration-local-burden-puma-layer.md] [SOURCE: research/immigration-stage2-county-bridge-batch.md]
4. I corrected unit-of-analysis errors before interpreting results. The household correction mattered because adult-linked child counts are not the same thing as household-normalized child exposure, and June 2026 work later showed that scenario-household school numerators cannot be paired with full-microsim adult denominators. [SOURCE: research/immigration-household-weighted-correction.md] [SOURCE: research/immigration-school-burden-per-adult-2026-06-15.md]
5. I treated the April federal prototype as provisional once the donor-library failure became visible, then treated the June SIPP-style build as a narrow annual federal proxy rather than a full federal answer. That is the correct move; forcing a precise all-in federal number out of either surface would be worse than leaving the broader question unresolved. [SOURCE: sources/immigration-fiscal/data/derived/build_federal_microsim_prototype.py] [SOURCE: research/immigration-prototype-progress.md] [SOURCE: research/immigration-federal-distribution-findings-2026-06-15.md]

## Terms and assumptions

### Key terms

1. `PUMA`: Public Use Microdata Area. This is the smallest public-use geography reliably available in ACS PUMS for this project. [SOURCE: research/immigration-glossary.md]
2. `ACS PUMS`: American Community Survey Public Use Microdata Sample. Person and housing microdata used for the core warehouse. [SOURCE: research/immigration-glossary.md]
3. `Origin x destination x household`: the main analytical cell. Origin is birthplace, destination is `state x PUMA`, household comes from `SERIALNO`-linked person and housing files. [SOURCE: research/immigration-origin-data-stack.md]
4. `Incidence`: who gets the gains or bears the costs. This report separates employers/consumers, competing low-skill natives, federal taxpayers, local governments, renters, and homeowners. [SOURCE: research/immigration-glossary.md]
5. `Household-normalized child burden`: school-age and preschool child exposure measured with the ACS housing file and `WGTP`, not by naively attaching all children to every qualifying adult. This term describes linked-household exposure; it is not itself a full-stock school-burden-per-adult, district marginal-cost estimate, or all-government net. [SOURCE: research/immigration-household-weighted-correction.md] [SOURCE: research/immigration-school-burden-per-adult-2026-06-15.md]

### Core operational assumptions in the current warehouse

1. `Age`: adults `25-64`. [SOURCE: sources/immigration-fiscal/data/derived/extend_immigration_context_with_pumas.sql]
2. `Recent`: `YOEP >= 2014`. [SOURCE: sources/immigration-fiscal/data/derived/extend_immigration_context_with_pumas.sql]
3. `Low-skill`: `SCHL < 16`, which in ACS coding means less than a regular high-school diploma. This is narrower than the usual policy shorthand for low-skill. [SOURCE: sources/immigration-fiscal/data/derived/extend_immigration_context_with_pumas.sql] [SOURCE: https://api.census.gov/data/2023/acs/acs5/pums/variables/SCHL.json]
4. `Local burden`: measured through schooling context, rent exposure, and housing stress, not through a fully specified municipal general-equilibrium model. [SOURCE: research/immigration-stage2-county-bridge-batch.md] [SOURCE: research/immigration-local-burden-puma-layer.md]
5. `Federal burden`: still provisional as an all-in concept. The April Texas/CPS donor prototype is not good enough for a headline federal net number; the current June SIPP-style federal annual proxy is usable only for its narrow FICA-minus-selected-cash-benefits ledger. [SOURCE: research/immigration-prototype-progress.md] [SOURCE: research/immigration-federal-distribution-findings-2026-06-15.md] [SOURCE: research/immigration-country-fiscal-tensor-2026-06-15.md]

## Datasets used and how they are fused

### Stage 1: origin, household, and state/PUMA stack

| Dataset | Role | Key fields | How fused | Status |
|---|---|---|---|---|
| ACS PUMS person file `csv_pus.csv` and state extracts such as `psam_p48.csv` | Core person microdata for origin, education, income, benefits, commute, language, year of entry | `SERIALNO`, `ST`, `PUMA`, `POBP`, `SCHL`, `YOEP`, `AGEP`, `PWGTP` | Filter to foreign-born adults `25-64`; construct `recent` and `low-skill` cells; aggregate to origin/state/PUMA | Core, `A1` [SOURCE: /Volumes/SSK1TB/corpus/census_acs/csv_pus.csv] [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/external/acs/psam_p48.csv] |
| ACS PUMS housing files `psam_husa.csv`, `psam_husb.csv` | Correct household weighting and child counts | `SERIALNO`, `WGTP` | Join to person file on `SERIALNO`; compute household-normalized school-age and preschool burdens | Core correction, `A1` [SOURCE: /Volumes/SSK1TB/corpus/census_acs/psam_husa.csv] [SOURCE: /Volumes/SSK1TB/corpus/census_acs/psam_husb.csv] |
| ACS PUMS code lists workbook | Decode `POBP` codes | `POBP` | Official birthplace decode for ACS microdata | Core, `A1` [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/external/origin/ACSPUMS2019_2023CodeLists.xlsx] |
| ACS `B05006` metadata and state table | Official origin labels and state-by-origin validation | state, birthplace categories | Used to validate and label origin stocks | Validation, `A1` [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/external/origin/census_acs1_2023_B05006_metadata.json] [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/external/origin/census_acs1_2023_B05006_state_origin.json] |
| ACS `B25064` state and PUMA median gross rent | Renter-side housing cost context | `state`, `PUMA` | Joined to `state x PUMA` cells | Core local context, `A1` [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/external/origin/census_acs1_2023_state_median_gross_rent.json] [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/external/origin/census_acs1_2023_puma_median_gross_rent.json] |
| World Bank country metadata | Region and income ontology | ISO2/ISO3, country name | Joined to decoded origins to avoid ad hoc regional groupings | Ontology, `A1` [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/external/origin/worldbank_country_metadata.json] |
| UN M49 country mapping | Region/subregion ontology | country name / codes | Materialized into derived dimension table | Ontology, `A1/A2` [SOURCE: research/immigration-origin-data-stack.md] |
| OHSS LPR workbooks | Administrative lawful-permanent-resident composition by country / major class | country of birth, major class, fiscal year | Joined at country layer where possible; county workbook stored but only partly joinable | Useful admin context, `A1/B1` [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/external/origin/ohss/lpr_country_birth_major_class_2005_2022.xlsx] [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/external/origin/ohss/lpr_counties_top_200_fy2022.xlsx] |
| FHFA state purchase-only HPI | Ownership-side housing context | state | Joined at state level | Context, `A1` [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/external/fhfa_hpi_po_state.txt] |
| Census school-finance state summary | Early state-level school-cost context | state | Joined before county upgrade | Superseded for local work, still useful, `A1` [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/external/census_school_finance_2023_summary.txt] |

### Stage 2: county bridge for local burden

| Dataset | Role | Key fields | How fused | Status |
|---|---|---|---|---|
| TIGER 2023 PUMA geometry | Build `PUMA x county` area crosswalk | geometry, county FIPS, PUMA | Spatial intersection; area-weighted bridge from PUMA to county | Necessary but weak bridge, `A1` data / `Moderate` claim quality [SOURCE: research/immigration-stage2-county-bridge-batch.md] |
| Census school finance full file `census_school_finance_2023.txt` | County school-finance layer | `CONUM` county FIPS | Aggregated to county current-spend-per-pupil; joined to crosswalk | Core local cost context, `A1` [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/external/census_school_finance_2023.txt] |
| HUD CHAS `Table11` 2018-2022 | County housing stress layer | county FIPS | Joined through county crosswalk | Good stress proxy, not welfare scalar, `A1` [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage2/hud/chas/2018thru2022-050-csv.zip] |
| IRS SOI county/state migration | Background local mobility / tax-base context | county FIPS, state | Normalized county net-flow context joined through county crosswalk | Contextual only, `A1` data / `Weak` as burden evidence [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage2/irs/countyinflow2223.csv] [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage2/irs/countyoutflow2223.csv] |
| NCES CCD fiscal bundle | District finance / local education context staging | `NCESID`, state | Used in later prototype work; helps attach district finance correctly in Texas | Prototype support, `A1` [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage2/nces/ccd_2024_25_universe_2025306_0.zip] |

### Stage 3: prototype federal and Texas local integration

| Dataset | Role | Key fields | How fused | Status |
|---|---|---|---|---|
| CPS ASEC 2024 March | Historical prototype federal donor library | household fields, income recodes | Used in the April Texas scaffold for household earnings / net estimates | **Superseded for current federal-proxy work**; still useful as a failure mode because `HHINC` was mishandled, `A1` for identifying the problem [SOURCE: sources/immigration-fiscal/data/derived/build_federal_microsim_prototype.py] [SOURCE: https://www2.census.gov/programs-surveys/cps/datasets/2024/march/asec2024_ddl_pub_full.pdf] |
| SIPP-style federal annual proxy tables | Narrow federal annual cash-flow layer | ACS adults, education/origin cells, SIPP donor cells | Builds origin and NH-white annual proxy rows for FICA minus SNAP/TANF/SSI | Useful for a narrow annual federal cash proxy only; not all-in federal liability, Medicare/Medicaid, income tax, EITC, capital/corporate tax, or NPV [SOURCE: research/immigration-federal-distribution-findings-2026-06-15.md] [SOURCE: research/immigration-country-fiscal-tensor-2026-06-15.md] |
| Texas ACS person/housing extract | State-specific local prototype | `SERIALNO`, `PUMA`, state-specific records | Built verified Texas stage-3 local tables | Prototype, locally useful, `A1` [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/external/acs/psam_p48.csv] |
| Texas stage-3 tract and PUMA context outputs | Local prototype integration | tract, PUMA | Combined local finance and housing stress context | Prototype, `A1` [SOURCE: research/immigration-prototype-progress.md] |

### Materialized warehouse layers

The original fused warehouse is [immigration_context.duckdb](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/immigration_context.duckdb). Later June 2026 fiscal-tensor work also uses the fiscal-union warehouse views named below.

Important materialized tables and views include:

1. `acs_origin_national_2023`
2. `acs_origin_puma_2023`
3. `acs_origin_household_national_2023`
4. `origin_puma_household_context_2023`
5. `state_origin_stock_2023`
6. `country_origin_dim`
7. `worldbank_country_dim`
8. `un_m49_country_dim`
9. `school_finance_county_2023`
10. `chas_county_housing_stress_2018_2022`
11. `puma_county_area_xwalk_2023`
12. `origin_puma_household_stage2_context_2023`
13. `tx_origin_puma_household_stage3_context_2023`
14. `acs_origin_household_federal_microsim_2023`
15. `acs_nh_white_federal_microsim_2023`
16. `v_country_fiscal_rollup`
17. `v_three_layer_annual`

[SOURCE: research/immigration-origin-data-stack.md] [SOURCE: research/immigration-stage2-county-bridge-batch.md] [SOURCE: research/immigration-prototype-progress.md] [SOURCE: research/immigration-country-fiscal-tensor-2026-06-15.md] [SOURCE: research/immigration-school-burden-per-adult-2026-06-15.md]

## Verified findings by certainty

### High-certainty findings

#### 1. The repo's strongest local findings apply to a very low-education subgroup, not all "low-skill" workers.

The current ACS warehouse defines low-skill as `SCHL < 16`. In ACS PUMS, `16` is a regular high-school diploma. So the warehouse's main subgroup is recent foreign-born adults with **less than a regular high-school diploma**. This is narrower and more adverse-selection-heavy than the common policy shorthand for low-skill. `High certainty`, `A1`.

Why it matters:
1. It makes the repo's local-burden findings more credible for the very bottom of the skill distribution.
2. It also means those findings should **not** be overgeneralized to all non-college or all lower-wage immigrants.

[SOURCE: sources/immigration-fiscal/data/derived/extend_immigration_context_with_pumas.sql] [SOURCE: https://api.census.gov/data/2023/acs/acs5/pums/variables/SCHL.json]

#### 2. The largest recent low-education origin groups are concentrated, not diffuse.

Direct warehouse query on `acs_origin_national_2023` shows the largest recent low-education origin groups are:

1. `Mexico` `225,180`
2. `Guatemala` `82,230`
3. `Honduras` `48,968`
4. `El Salvador` `47,738`
5. `Cuba` `39,518`
6. `Haiti` `28,117`
7. `Vietnam` `27,306`
8. `China` `21,799`
9. `Colombia` `20,638`
10. `Brazil` `19,021`

`High certainty`, `A1`.

[SOURCE: DuckDB query on `acs_origin_national_2023` run 2026-04-10]

#### 3. Linked-household school-age child exposure differs sharply by origin even after the household correction.

Direct warehouse query on `acs_origin_household_national_2023` for origins with at least `10,000` recent low-education adults shows:

1. `Afghanistan` `2.6291` school-age children per linked household; `86.67%` of linked households have school-age children
2. `Honduras` `1.2855`; `70.87%`
3. `Myanmar` `1.2650`; `66.14%`
4. `El Salvador` `1.0600`; `58.63%`
5. `Mexico` `1.0114`; `53.49%`
6. `Guatemala` `0.9960`; `59.07%`

`High certainty`, `A1`.

That is one of the cleanest verified findings in the repo as a **linked-household exposure metric**. It survives the correction from adult-linked counts to housing-weighted household estimates. It should not be cited as a current full-stock school-burden-per-adult or origin fiscal net row: the June 2026 tensor withholds origin school/net rows pending a same-universe rebuild. [SOURCE: research/immigration-household-weighted-correction.md] [SOURCE: DuckDB query on `acs_origin_household_national_2023` run 2026-04-10] [SOURCE: research/immigration-school-burden-per-adult-2026-06-15.md]

#### 4. Housing exposure also differs sharply by origin, and `PUMA` geography matters.

For origins with at least `10,000` recent low-education adults, the highest weighted `PUMA` median gross rent exposures are:

1. `China` `1879.82`
2. `Colombia` `1870.13`
3. `Brazil` `1829.60`
4. `Vietnam` `1794.55`
5. `India` `1757.39`
6. `Venezuela` `1750.48`

`High certainty`, `A1`.

The earlier state-average approach understated rent exposure for several urban-concentrated groups and overstated it for some large groups such as Mexico. [SOURCE: research/immigration-local-burden-puma-layer.md] [SOURCE: DuckDB query on `origin_puma_household_context_2023` run 2026-04-10]

#### 5. The local-burden story is real, but it is heterogeneous.

The verified pattern is not "all low-skill immigration has the same local effect." The better summary is:

1. Some groups are `school-heavy`.
2. Some are `housing-heavy`.
3. Some are both.
4. The burden depends heavily on destination mix.

`High certainty`, `A1/A2`.

[SOURCE: research/immigration-household-weighted-correction.md] [SOURCE: research/immigration-local-burden-puma-layer.md] [SOURCE: research/immigration-unified-scenarios-memo.md]

### Moderate-certainty findings

#### 6. A federal-positive / local-negative split is likely real, but the repo has not yet pinned it down numerically.

This is one of the most plausible readings of the combined literature and local warehouse structure:

1. some national output and consumer-price gains exist,
2. some indirect federal fiscal offsets likely exist,
3. but local schooling, housing, and service-capacity costs remain concentrated.

`Moderate certainty`, `A2`.

This is consistent with the National Academies framing, the newer CBO state/local work, and the indirect-fiscal-effects literature. The repo now has a cleaner narrow annual federal proxy than it had in April, but that proxy does not quantify all federal channels or the local offset numerically. [SOURCE: https://d279m997dpfwgl.cloudfront.net/wp/2016/09/0922_immigrant-economics-full-report.pdf] [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf] [SOURCE: https://www.econstor.eu/bitstream/10419/282044/1/352.pdf] [SOURCE: research/immigration-federal-distribution-findings-2026-06-15.md]

#### 7. Descendants are a real positive channel, but they do not erase local burdens by assumption.

The best literature supports some substantial upward mobility and long-run tax-base contribution for children of immigrants, but this is heterogeneous by origin and destination and should not be assumed to cancel near-term local costs automatically. `Moderate certainty`, `A2`.

[SOURCE: https://www.nber.org/papers/w26408] [SOURCE: https://www.nber.org/papers/w24394] [SOURCE: https://www.nber.org/system/files/working_papers/w33961/w33961.pdf]

#### 8. Housing should not be treated as a pure national loss.

Higher rents are bad for renters, but they are not automatically a pure aggregate welfare loss because there are offsetting gains to owners and tax bases. The correct object is incidence, not just price level. `Moderate certainty`, `A2/B2`.

[SOURCE: https://doi.org/10.1016/j.jue.2006.07.004] [SOURCE: https://www.cato.org/briefing-paper/immigrants-housing-wealth-local-government-finances] [SOURCE: research/immigration-unified-scenarios-memo.md]

#### 9. Political legitimacy and backlash belong in the main model, not the appendix.

If a policy raises output but undermines perceived fairness, local-state capacity, or political legitimacy, that is part of the country's welfare story. The literature on backlash and distribution supports treating this as a first-order policy channel. `Moderate certainty`, `A2/B2`.

[SOURCE: https://www.aeaweb.org/articles?id=10.1257/jel.20221643] [SOURCE: research/immigration-unified-scenarios-memo.md]

#### 10. Under `AGI-soon`, short-run transition management matters more than distant lifetime NPV.

This is partly inferential, but it follows from the combination of automation uncertainty and local-system constraints. If labor demand for the bottom tail is about to change rapidly, then the dominant policy question shifts from "what is the discounted lifetime fiscal contribution" to "can local systems absorb the transition without institutional stress." `Moderate certainty`, `A2/B2`, partly `[INFERENCE]`.

[SOURCE: https://docs.iza.org/dp18218.pdf] [SOURCE: https://www.imf.org/-/media/files/research/imf-and-g20/2025/g20-background-note-on-aging-and-migration.pdf] [SOURCE: research/immigration-agi-reframing.md] [INFERENCE]

### Low-certainty or unresolved findings

#### 11. The repo does not yet have a full federal/all-in fiscal microsimulation.

The April Texas prototype table is useful mainly because it reveals an old problem.

April verified counts from `tx_origin_puma_household_stage3_context_2023`:
1. total rows: `845`
2. matched donor rows: `238`
3. matched row share: `28.17%`
4. matched qualifying-adult weight share: `26.84%`

The donor library table `sipp_household_donor_cells_2023` then contained `24` cells, and both the minimum and maximum `income_band` were `lt30k`. That made the April prototype unfit for a serious net-fiscal claim. `High certainty` that this prototype was weak; `Low certainty` on any federal number derived from it. `A1`.

[SOURCE: DuckDB queries on `tx_origin_puma_household_stage3_context_2023` and `sipp_household_donor_cells_2023` run 2026-04-10] [SOURCE: sources/immigration-fiscal/data/derived/build_federal_microsim_prototype.py] [SOURCE: research/immigration-prototype-progress.md]

June 2026 work added a better SIPP-style annual federal proxy and country tensor. That newer surface supports narrow statements such as Mexico-origin adults scoring about `$1,519` per adult per year and NH white US-born adults about `$2,746` on the FICA-minus-SNAP/TANF/SSI ledger. It does **not** support an all-in federal number, a full tax-transfer household filing model, or a lifetime NPV. [SOURCE: research/immigration-federal-distribution-findings-2026-06-15.md] [SOURCE: research/immigration-country-fiscal-tensor-2026-06-15.md]

#### 12. The current local county bridge is useful, but still imperfect.

The county-first bridge is the right move relative to fake metro precision, but it still relies on area-weighted `PUMA x county` crosswalks. That is acceptable for context; it is not the same as exact person, student, or filer location. `Moderate certainty` on usefulness, `Low-to-Moderate` on precise exposure magnitudes. `A1` data, `Weak-to-Moderate` inference quality.

[SOURCE: research/immigration-stage2-county-bridge-batch.md] [SOURCE: research/immigration-confidence-ladder.md]

## Which economists are mostly right and which are wrong for the actual question

The right distinction is not "good economist" versus "bad economist." It is whether the economist is answering the **full welfare/local-capacity question** or a narrower channel question.

### Mostly right on a narrow question

1. `David Autor` — `Agree` on Question A. Mostly right **if** the claim is that average wage effects for natives need not be large and some complementarity exists. Not a full local-budget or housing-capacity answer. `Moderate certainty`, `A2/B1`. [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/] [SOURCE: research/immigration-economist-effects-matrix.md]
2. `Hilary Hoynes` — `Agree`. Mostly right **if** the claim is that average national incidence can be positive even with distributional losses. Too narrow if read as a full local-ledger answer. `Moderate certainty`, `A2/B1`. [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/] [SOURCE: research/immigration-clark-respondent-audit.md]
3. `Janet Currie` — `Agree`. Mostly right on broad average-benefit possibilities, but not a full school/housing/capacity answer. `Moderate certainty`, `A2/B1`. [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/] [SOURCE: research/immigration-clark-respondent-audit.md]
4. `Robert Shimer` — `Agree`. One of the better-framed responses because he explicitly separates wage effects for low-skill workers from fiscal costs for high-skill workers and says both could be small. That is closer to an incidence analysis than a slogan. `Moderate certainty`, `B1`. [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/]
5. `Jonathan Levin` — `Uncertain`, not `Agree`, but epistemically stronger than many of the agree responses. He explicitly notes that pro-immigration arguments often concern immigrant welfare rather than resident welfare, which is exactly the framing distinction this project keeps surfacing. `High certainty`, `B1`. [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/]
6. `Robert Hall` — `Uncertain`, but again epistemically stronger than many agree responses because he explicitly raises family burden and tax-revenue dependence. `High certainty`, `B1`. [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/]

### Mostly wrong or overbroad for the actual question

These are not necessarily wrong on labor-market or gains-from-trade logic. They are wrong **if their answer is read as a full-country, full-ledger welfare claim**.

1. `Oliver Hart` — `Agree`, confidence `8`. His explicit reasoning was classical gains from trade plus a welfare caveat. That is too incomplete for the actual question because it does not seriously account for local schooling, housing, and destination capacity. `Moderate certainty`, `B1/A2`. [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/]
2. `Christopher Udry` — `Strongly Agree`, confidence `4`. The complementarity logic may be valid on one channel, but it is too weak a basis for a full average-citizen claim. `Moderate certainty`, `B1/A2`. [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/]
3. `Maurice Obstfeld` — `Agree`, confidence `8`. The survey page gives no full local-ledger basis. That makes the answer overbroad for the actual question. `Moderate certainty`, `B1`. [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/]
4. `Nancy Stokey` — `Agree`, confidence `8`. Same issue: without an explicit local-incidence or fiscal basis, the answer is too broad for the question as stated. `Moderate certainty`, `B1`. [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/]
5. `Daron Acemoglu` — `Agree`, confidence `8`. He may be right on some general-equilibrium or complementarity channels, but as an answer to the full welfare/local-capacity question it is too broad. `Low-to-Moderate certainty`, `B1/A2`. [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/] [SOURCE: research/immigration-economist-effects-matrix.md]

### The economists who were closest to the truth structurally

The best-structured survey responses were often the `Uncertain` ones.

1. `Jonathan Levin`
2. `Robert Hall`
3. `Caroline Hoxby`
4. `Larry Samuelson`
5. `Richard Schmalensee`

Why:
1. they flagged horizon problems,
2. they flagged incidence problems,
3. they resisted reducing the issue to one number,
4. they separated resident welfare from immigrant welfare.

That is closer to the actual state of evidence than a flat `Agree` or `Disagree`. [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/]

## What is solidly proven, what is not, and what should not be claimed

### Solidly proven enough to say now

1. Origin heterogeneity is large.
2. Destination heterogeneity is large.
3. Household structure matters.
4. The local-burden story survives the household correction.
5. The economist-agree case is usually a partial-channel argument, not a full welfare ledger.

### Not yet proven enough to say now

1. one all-in net fiscal number for the country,
2. one all-in net welfare number for the average citizen,
3. a precise all-in federal-positive / local-negative estimate by origin,
4. a clean causal housing or school-cost effect size from this repo alone.

### Claims this report rejects

1. `"Low-skill immigration is simply good for the average American."`
2. `"Low-skill immigration is simply bad for the country."`
3. `"The Clark economist poll settled the issue."`
4. `"The current narrow federal proxy is good enough for a hard all-in fiscal number."`

## Bottom line

The verified evidence in this repo does **not** support a one-word answer.

What it does support is this:

1. For a narrow but important subgroup of recent foreign-born adults with less than a high-school diploma, local burdens on schools, housing stress, and destination capacity are real and heterogeneous.
2. Those burdens are not evenly distributed across origins or destinations.
3. Some national gains from labor supply, complementarity, and consumer prices are plausible and well supported in the literature.
4. Many economists who answered `Agree` were mostly right about those narrow gains, but wrong or overbroad if their answer is taken as a full-country, full-ledger verdict.
5. The current repo is strongest on descriptive origin/destination/household surfaces and now has a useful narrow federal annual proxy, but it remains weak on all-in federal, lifetime, and same-universe origin school-net estimates.
6. Under an `AGI-soon` frame, transition management and institutional resilience become more important than distant average-lifetime NPV.

That is the actual verified picture.

## Revisions

| Date | Change | Trigger |
|---|---|---|
| 2026-06-16 | Scoped April household-normalized school language to linked-household child exposure; updated the federal section for the June SIPP-style narrow annual proxy and same-universe school/net guard. | `research/immigration-federal-distribution-findings-2026-06-15.md`, `research/immigration-country-fiscal-tensor-2026-06-15.md`, and `research/immigration-school-burden-per-adult-2026-06-15.md` superseded parts of the April prototype surface. |
