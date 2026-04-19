# Saiz housing supply elasticity × MSA rent and immigrant share — finding

**Date:** 2026-04-18
**Question:** Does immigrant rent exposure measured in the existing PUMA warehouse correspond to welfare loss, or is it benign price discovery? Test by linking Saiz 2010 MSA-level housing supply elasticity to current ACS rent and foreign-born share.
**Status:** Cross-sectional descriptive — instrumental-variable extension is the next step.

## Bottom line

Immigrants are concentrated in MSAs where housing supply *cannot respond*. The most inelastic quartile of MSAs (Saiz elasticity 0.6–1.5) has **2.6× the foreign-born share** of the most elastic quartile (11.6% vs 4.4%) and **45% higher median rent** ($1,343 vs $929). This re-grades the existing repo's "rent exposure ≠ welfare loss" caveat: in the actual destination markets immigrants pick, rent appreciation has nowhere to go but into renter cost burden. **Confidence:** HIGH on the descriptive correlation, MODERATE on the welfare-loss implication (needs IV identification to attribute causation to immigrant inflow specifically).

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

**Reading:** Going from elastic to inelastic, immigrant share roughly triples and rent burden rises 3 percentage points. The inelastic quartile is a different country: ~$80K incomes paying $1,343 rent in places where housing supply cannot expand to absorb new arrivals.

### MSAs binned by foreign-born share (D1 lowest → D5 highest)

| FB-share decile | n | median elasticity | median rent |
|-----------------|---|-------------------|-------------|
| D1 lowest | 48 | 3.40 | $878 |
| D2 | 47 | 2.41 | $990 |
| D3 | 47 | 2.58 | $1,007 |
| D4 | 47 | 2.48 | $1,146 |
| **D5 highest** | 48 | **1.51** | **$1,421** |

**Reading:** The places immigrants concentrate are systematically less elastic. The top-quintile FB MSAs have median elasticity 1.51 — meaning a 10% population shock produces a ~6.5% price increase rather than a ~3% increase you'd see in the median MSA.

### Top 10 inelastic MSAs (where immigrant inflow has nowhere to go)

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
- In **inelastic** destination markets (which is where immigrants actually concentrate), rent exposure is much closer to welfare loss because the housing supply can't expand. Marginal newcomers compete for a fixed stock and drive up cost burden for incumbent renters.
- In **elastic** destination markets, immigrant inflow gets absorbed by new construction. But these markets contain few immigrants in the first place.
- Net: the existing PUMA rent burden findings should be read as *closer* to welfare loss than the adversarial review allowed.

### Confidence ladder upgrades

- `Housing-heavy versus school-heavy origin-group typology` → from Medium to **Medium-Strong**, conditional on the destination MSA's elasticity quartile. The existing repo had no way to make this call.
- `Magnitude claims for local school burden from current warehouse` → unchanged (Saiz only addresses housing).

### What changes in the verdict

The existing verified-findings report bottom-line said: "Higher rents are bad for renters, but they are not automatically a pure aggregate welfare loss because there are offsetting gains to owners and tax bases. The correct object is incidence, not just price level." [SOURCE: research/immigration-verified-findings-report-2026-04-10.md, finding #8]

This finding doesn't overturn that — owner gains still exist. But it raises the *renter incidence* component because most immigrants live in places where supply doesn't respond. Owner-gain-to-renter-loss ratio in inelastic markets is structurally different from elastic markets. The aggregate welfare frame requires accounting for tenure mix (which the warehouse can do via ACS housing file once SSD is mounted again).

## Limitations and next steps

1. **Cross-sectional only.** This shows correlation in 2022. The causal reading "immigrant inflows raise rent more in inelastic markets" needs panel variation. Saiz 2007 JUE did this with 1980-2000 changes; we should replicate with 2010-2020 ACS panel.

2. **Saiz definitions are 1999 OMB.** Some MSAs have been split or merged since (PMSAs deprecated, NECMAs partially obsolete). Match rate 88% is reasonable but the 32 unmatched are not random — they're mostly New England consolidations.

3. **No instrument for immigrant share.** Endogeneity: high-amenity inelastic cities attract both immigrants and natives. The proper IV is historical (1970-1990) origin-shares × current national flow (Card shift-share). Doable with the warehouse's `acs_origin_*` tables once SSD is mounted.

4. **Unit of analysis mismatch.** Saiz is at MSA level; the warehouse rent table is at PUMA level. PUMAs nest within MSAs imperfectly. Right thing is to weight Saiz elasticity into PUMA-level by the MSA-PUMA crosswalk, then re-run origin × PUMA × elasticity tabulations once the warehouse is accessible.

## Decision-relevant claim

For the current evidence base, this finding **strengthens the housing-burden side of the local-burden ledger**. The earlier adversarial caveat "rent exposure isn't welfare loss" is partially defeated when destination is in the inelastic quartile, which is where >40% of immigrant population lives.

Confidence: **HIGH** that the descriptive correlation is real (n=237 MSAs, monotonic gradient across quartiles, replicates Saiz's own pattern); **MODERATE** that this should update the welfare interpretation (causal step requires IV).

[SOURCE: data/analysis/saiz_msa_rent_immigrant_2022.parquet]
[SOURCE: scripts/merge_saiz_rent_immigrant.py]

<!-- knowledge-index
generated: 2026-04-19T03:34:38Z
hash: 029eef46ab33

cross_refs: research/immigration-adversarial-review.md, research/immigration-verified-findings-report-2026-04-10.md

end-knowledge-index -->
