# Saiz elasticity and current rents: descriptive comparison and corrected calculation

**Current assessment — 2026-09-05.** The reported MSA cross-section is compatible with higher rents and foreign-born shares in less elastic housing markets. It does not identify immigration's causal rent effect or establish that renters are unharmed. The earlier conversion from a 10% population shock to a 6.5% price rise omitted necessary demand assumptions. [INFERENCE]

## Cross-section and measurement

The analysis reports matching 237 of 269 historical Saiz metro observations to modern outcomes using names. A first-city/state name match is not a geographic boundary crosswalk, and the 32 unmatched observations need not be random. Historical elasticity estimates, current rents, incomes, and population composition also refer to different periods. The author's data remain useful, but merging them does not transfer the identification of the original paper to this new cross-section. [SOURCE: historical matching account; [Saiz author publication/data page](https://urbaneconomics.mit.edu/research/publications); INFERENCE]

The reported least- versus most-elastic quartiles have median rents of $1,343 versus $929: the arithmetic rent premium is **44.6%**. Reported foreign-born shares of 11.6% versus 4.4% give a ratio of **2.64**. These are group descriptions, not effects of elasticity or migration. The original joined panel and scripts were not recovered, so matching, weighting, quartiles, and household-burden construction were not independently reproduced. [SOURCE: historical table; CALCULATION; GAP]

An MSA's median rent divided by its all-household median income is not a household rent-burden measure: tenants and all households are different populations, and a ratio of medians is not the median of household ratios. Even a valid average burden comparison can conceal renters who lose when rents rise. Neither the observed income differences nor a metro-level ratio establishes that migration's rent effect is offset for affected households. Claims about the fraction of immigrants in a metro group also require person weights; an unweighted metro count is not enough. [INFERENCE]

## Corrected elasticity calculation

The earlier calculation effectively divided a 10% population change by supply elasticity 1.51 to obtain about 6.6%. A supply elasticity is a quantity response to a price change; using it for a population-driven equilibrium price forecast requires a demand relationship and a housing-market definition. It is not automatically a rent elasticity. [SOURCE: [Saiz (2010)](https://academic.oup.com/qje/article-abstract/125/3/1253/1903664); DERIVATION]

For an illustrative log-linear market, let supply change be `εs × Δlog P` and demand change be `d − εd × Δlog P`, where `d` is an exogenous housing-demand shift and `εd ≥ 0` the magnitude of demand elasticity. Market clearing gives:

`Δlog P = d / (εs + εd)`.

If `d = 0.10` and `εs = 1.51`, an assumed `εd = 1` gives **0.0398 log points**, approximately 4.0%, rather than 6.6%. Dividing by 1.51 alone corresponds to assuming zero demand elasticity, or to imposing a quantity increase and moving along the supply curve. Neither assumption was stated or estimated. A 10% population change also need not equal a 0.10 log-point housing-demand shift: occupancy, household formation, income, and location choice matter. These numbers illustrate the missing assumptions, not a replacement empirical forecast. [DERIVATION]

## Causal and welfare interpretation

Observed immigrants can select growing or high-wage cities, and supply constraints and regulation can correlate with amenities and prior demand. Cross-sectional signs or t-statistics cannot isolate migration's contribution or rank causal mechanisms. A proposed shift-share instrument needs justified shocks/shares and an exclusion restriction; naming an instrument does not resolve those issues. [INFERENCE]

Rent increases may redistribute income to owners and impose losses on particular renters, while construction and congestion involve real resource costs. Measuring one channel cannot settle net welfare without the relevant counterfactual and incidence. This memo supports examining heterogeneous local effects; it does not establish a national absorption threshold or refute long-run gains. [INFERENCE]

## Revisions

- **2026-09-05:** Corrected the supply-only price calculation, clarified metro versus household estimands and matching limits, and withdrew unsupported causal and welfare conclusions. [Decision](../decisions/2026-09-05-material-inference-repair.md).

<!-- historical-snapshot:start superseded=2026-09-05 -->
<details>
<summary>Superseded historical analysis — retained verbatim for source and correction provenance</summary>

**Historical text, not the current assessment.** Its earlier verdicts, confidence labels, and source-version claims are superseded by the corrections above. It is retained to preserve quotations and the reasoning that was corrected.

# Saiz housing supply elasticity × MSA rent and immigrant share — finding

**Date:** 2026-04-18
**Question:** Does immigrant rent exposure measured in the existing PUMA warehouse correspond to welfare loss, or is it benign price discovery? Test by linking Saiz 2010 MSA-level housing supply elasticity to current ACS rent and foreign-born share.
**Status:** Cross-sectional descriptive — instrumental-variable extension is the next step.

## Bottom line

Immigrants are concentrated in MSAs where housing supply is relatively inelastic. The most inelastic quartile of MSAs (Saiz elasticity 0.6–1.5) has **2.6× the foreign-born share** of the most elastic quartile (11.6% vs 4.4%) and **45% higher median rent** ($1,343 vs $929). This re-grades the existing repo's "rent exposure ≠ welfare loss" caveat: in the actual destination markets immigrants pick, rent exposure is a stronger renter-incidence warning than a raw price-level measure. **Confidence:** HIGH on the descriptive correlation, MODERATE on translating it into aggregate welfare loss (needs IV identification to attribute causation to immigrant inflow specifically, plus owner/renter incidence).

## Method

1. Saiz (2010) MSA elasticity dataset (n=269 MSAs, 1999 OMB definitions). [SOURCE: https://urbaneconomics.mit.edu/research/data]
2. ACS 2018-2022 5-year estimates: B25064 (median gross rent), B05002 (foreign-born population), B19013 (median household income), at MSA/CBSA level. [SOURCE: https://api.census.gov/data/2022/acs/acs5]
3. Match by MSA name (first city + first state, normalized). 237/269 Saiz MSAs matched (88%). Unmatched are mostly old PMSA splits that no longer exist as separate CBSAs.
4. Quartile MSAs by elasticity; tabulate rent, income, and FB share.
5. Independently quintile MSAs by FB share; tabulate elasticity.

## Results

### MSAs binned by elasticity (Saiz Q1 most inelastic → Q4 most elastic)

| Quartile | n | median rent | median HH income | rent-to-income | FB share % | median elasticity |
|----------|---|-------------|------------------|----------------|------------|-------------------|
| Q1 inelastic | 60 | $1,343 | $81,089 | 20.8% | **11.6%** | 1.23 |
| Q2 | 59 | $1,089 | $68,329 | 19.0% | 6.5% | 2.06 |
| Q3 | 59 | $994 | $66,823 | 18.2% | 6.4% | 2.79 |
| Q4 elastic | 59 | $929 | $62,941 | 17.7% | **4.4%** | 4.26 |

**Reading:** Going from elastic to inelastic, immigrant share roughly triples and rent burden rises 3 percentage points. The inelastic quartile is a different country: ~$80K incomes paying $1,343 rent in places where housing supply is more constrained.

### MSAs binned by foreign-born share (D1 lowest → D5 highest)

| FB-share decile | n | median elasticity | median rent |
|-----------------|---|-------------------|-------------|
| D1 lowest | 48 | 3.40 | $878 |
| D2 | 47 | 2.41 | $990 |
| D3 | 47 | 2.58 | $1,007 |
| D4 | 47 | 2.48 | $1,146 |
| **D5 highest** | 48 | **1.51** | **$1,421** |

**Reading:** The places immigrants concentrate are systematically less elastic. The top-quintile FB MSAs have median elasticity 1.51 — meaning a 10% population shock produces a ~6.5% price increase rather than a ~3% increase you'd see in the median MSA.

### Top 10 inelastic MSAs (where renter-incidence risk is highest)

| MSA | Elasticity | Rent | FB share | Rent/income |
|-----|-----------|------|----------|-------------|
| Miami, FL | 0.60 | $1,657 | **41.5%** | 28.8% |
| Los Angeles–Long Beach | 0.63 | $1,892 | 32.4% | 25.5% |
| San Francisco | 0.66 | $2,336 | 30.9% | 21.7% |
| San Diego | 0.67 | $2,011 | 22.6% | 24.9% |
| Salt Lake City–Ogden | 0.75 | $1,386 | 12.4% | 18.4% |
| New York | 0.76 | $1,711 | 29.5% | 21.9% |
| San Jose | 0.76 | $2,697 | **39.7%** | 21.3% |
| New Orleans | 0.81 | $1,151 | 7.7% | 22.0% |
| Chicago | 0.81 | $1,310 | 17.7% | 18.5% |
| Boston (NECMA) | 0.86 | $1,827 | 19.6% | 20.5% |

These are the destinations that anchor the existing repo's `origin_puma_household_context_2023` rent-burden findings. Without exception they are at the bottom of the Saiz elasticity distribution.

### Top 10 elastic MSAs (housing absorbs inflow)

| MSA | Elasticity | Rent | FB share |
|-----|-----------|------|----------|
| Pine Bluff, AR | 12.1 | $806 | 1.7% |
| St. Joseph, MO | 7.9 | $846 | 3.0% |
| Columbia, MO | 7.8 | $981 | 5.8% |
| Alexandria, LA | 7.1 | $922 | 2.6% |
| Terre Haute, IN | 6.5 | $833 | 2.0% |
| Joplin, MO | 6.4 | $853 | 3.9% |
| Fargo–Moorhead, ND-MN | 6.0 | $919 | 7.3% |
| Wichita, KS | 5.5 | $931 | 7.5% |
| Fort Wayne, IN | 5.4 | $922 | 7.0% |
| Sioux City, IA-NE | 5.4 | $924 | 10.7% |

**Reading:** Elastic markets where immigrants don't go. Sioux City and Fargo are interesting exceptions — meatpacking towns with non-trivial FB shares but elastic land.

## Implications for the existing repo

### Updates the rent-burden interpretation

Adversarial review §2 said: "PUMA rent layer measures exposure to expensive rental markets ... not by itself a measure of net welfare loss." [SOURCE: research/immigration-adversarial-review.md]

The Saiz merge sharpens that:
- In **inelastic** destination markets (which is where immigrants actually concentrate), rent exposure is much closer to a renter-incidence problem because supply response is weaker. The causal claim that marginal immigrant inflows raise incumbent renter costs still needs panel/IV identification.
- In **elastic** destination markets, population inflow should be absorbed more by new construction in expectation. But these markets contain few immigrants in the first place.
- Net: the existing PUMA rent burden findings should be read as a stronger renter-incidence warning than the adversarial review allowed.

### Confidence ladder upgrades

- `Housing-heavy versus school-heavy origin-group typology` → from Medium to **Medium-Strong**, conditional on the destination MSA's elasticity quartile. The existing repo had no way to make this call.
- `Magnitude claims for local school burden from current warehouse` → unchanged (Saiz only addresses housing).

### What changes in the verdict

The existing verified-findings report bottom-line said: "Higher rents are bad for renters, but they are not automatically a pure aggregate welfare loss because there are offsetting gains to owners and tax bases. The correct object is incidence, not just price level." [SOURCE: research/immigration-verified-findings-report-2026-04-10.md, finding #8]

This finding doesn't overturn that — owner gains still exist. But it raises the *renter incidence risk* component because most immigrants live in places where supply response is weaker. Owner-gain-to-renter-loss ratio in inelastic markets is structurally different from elastic markets. The aggregate welfare frame requires accounting for tenure mix (which the warehouse can do via ACS housing file once SSD is mounted again).

## Limitations and next steps

1. **Cross-sectional only.** This shows correlation in 2022. The causal reading "immigrant inflows raise rent more in inelastic markets" needs panel variation. Saiz 2007 JUE did this with 1980-2000 changes; we should replicate with 2010-2020 ACS panel.

2. **Saiz definitions are 1999 OMB.** Some MSAs have been split or merged since (PMSAs deprecated, NECMAs partially obsolete). Match rate 88% is reasonable but the 32 unmatched are not random — they're mostly New England consolidations.

3. **No instrument for immigrant share.** Endogeneity: high-amenity inelastic cities attract both immigrants and natives. The proper IV is historical (1970-1990) origin-shares × current national flow (Card shift-share). Doable with the warehouse's `acs_origin_*` tables once SSD is mounted.

4. **Unit of analysis mismatch.** Saiz is at MSA level; the warehouse rent table is at PUMA level. PUMAs nest within MSAs imperfectly. Right thing is to weight Saiz elasticity into PUMA-level by the MSA-PUMA crosswalk, then re-run origin × PUMA × elasticity tabulations once the warehouse is accessible.

## Decision-relevant claim

For the current evidence base, this finding **strengthens the housing-burden side of the local-burden ledger**. The earlier adversarial caveat "rent exposure isn't welfare loss" is narrowed when destination is in the inelastic quartile, which is where >40% of immigrant population lives.

Confidence: **HIGH** that the descriptive correlation is real (n=237 MSAs, monotonic gradient across quartiles, consistent with the Saiz elasticity/rent mechanism); **MODERATE** that this should update the welfare interpretation (causal step requires IV).

[SOURCE: data/analysis/saiz_msa_rent_immigrant_2022.parquet]
[SOURCE: scripts/merge_saiz_rent_immigrant.py]

## Revisions

| Date | Change |
|------|--------|
| 2026-06-16 | Replaced "replicates Saiz's own pattern" with consistency language; the memo is a 2022 descriptive cross-section, not a direct panel replication of Saiz. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Replaced residual "closer to welfare loss" language with renter-incidence warning; aggregate welfare loss still requires owner/renter incidence and causal identification. See `immigration-conclusion-audit-running-fixes.md`. |

<!-- knowledge-index
generated: 2026-04-19T03:34:38Z
hash: 029eef46ab33

cross_refs: research/immigration-adversarial-review.md, research/immigration-verified-findings-report-2026-04-10.md

end-knowledge-index -->

</details>
<!-- historical-snapshot:end -->
