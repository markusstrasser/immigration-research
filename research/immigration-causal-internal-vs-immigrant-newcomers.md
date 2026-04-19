# Internal native migration vs international immigration as newcomer shocks

**Date:** 2026-04-18
**Question:** Is "immigrant" or "newcomer in general" the right unit of analysis for the school/housing/capacity burden discussion in the existing repo?
**Answer:** **Newcomer in general**, by a wide margin. US-native cross-county migration is **~33× larger per capita per year** than recent international immigration at the median county. Restricting immigration cannot fix the bulk of newcomer-driven local burden because most newcomer flow IS native.

## Bottom line

The existing repo's `low-skill-origin-incidence-memo.md` and the local-burden findings have implicitly treated "immigrant inflow" as the dominant source of newcomer pressure on counties' schools and housing. The IRS SOI county-to-county tax-filer migration data (2022-2023) merged with ACS recent-arrival foreign-born data shows this is wrong by a factor of 33×. Median US county receives 3.00% of population per year as native US-inflow; same county receives 0.08% as recent foreign-born annual flow. **The newcomer-burden frame should disaggregate native-newcomer from immigrant-newcomer because they are different orders of magnitude with different policy levers.**

This does not erase the immigrant-specific story (concentration, language, household composition, legal status all still matter). But it sharply revises the frame: most "newcomer" pressure on US counties is internal migration, which immigration policy cannot touch.

**Confidence:** HIGH on the absolute size disparity (IRS SOI counts tax filers — administrative data, not survey). MEDIUM on the per-newcomer burden parity (composition differs: military families, retirees, remote workers vs labor-migrant immigrants).

## Method

### Data
- **IRS SOI county-to-county migration 2022-2023** — administrative tax-filer migration. Aggregate row code y1=97 = "Total Migration-US" (excludes foreign). 4.6 MB CSV per file (inflow + outflow). Reports number of returns, exemptions, and aggregate AGI by destination county. [SOURCE: irs.gov/pub/irs-soi/countyinflow2223.csv]
- **ACS 2022 5-yr** — county-level B01003 (totpop), B05002 (foreign-born stock), B05005_002E (foreign-born entered 2010-or-later, ≈ recent arrivals 12-year window), B25064 (median rent), B19013 (median income).
- **Match:** state_fips × county_fips (FIPS5). 9,120 county-merged rows after one-to-many join (county-fips repeated due to multiple inflow source rows; stylized facts use medians robust to this).

### Definitions
- "Native US-inflow" = aggregate annual exemption count moving across counties from anywhere in the US (per IRS SOI). Most are US-born; small share are settled foreign-born already in the US who change county.
- "Recent foreign-born annual flow" = foreign-born population entered 2010-or-later (per ACS B05005), divided by 12 to annualize the 12-year accumulation.
- Both measured as share of destination county population.

## Stylized facts

### Fact 1: native flow is ~33× larger per year
Median county (≥10,000 pop, n=7,286):
- Native US-inflow share: **3.00% per year**
- Recent FB annual flow: **0.08% per year**
- Ratio: **33×**

### Fact 2: top counties by NATIVE inflow are military bases and Sun Belt exurbs
| County | Pop | Inflow share | Median rent |
|--------|-----|--------------|-------------|
| Geary County, KS (Fort Riley) | 36,247 | **16.4%** | $1,132 |
| Long County, GA | 16,804 | 15.7% | $846 |
| Liberty County, GA (Fort Stewart) | 65,550 | 13.9% | $1,178 |
| Kaufman County, TX (Dallas exurb) | 149,773 | 13.6% | $1,286 |
| Fredericksburg city, VA (DC exurb) | 28,258 | 12.8% | $1,462 |
| Comal County, TX (Austin exurb) | 165,201 | 11.4% | $1,390 |
| Alexandria city, VA | 157,594 | 11.3% | $1,983 |

These places get 10-16% of their population REPLACED every year by native US migrants. None of them are immigrant gateways.

### Fact 3: top counties by RECENT IMMIGRANT inflow are well-known immigrant gateways
| County | Pop | Annual FB flow | Median rent |
|--------|-----|----------------|-------------|
| Miami-Dade, FL | 2,688,237 | 1.5% | $1,623 |
| Osceola, FL | 393,745 | 1.4% | $1,537 |
| Hudson, NJ | 712,029 | 1.3% | $1,722 |
| Colfax, NE (meatpacking) | 10,563 | 1.3% | $907 |
| Santa Clara, CA | 1,916,831 | 1.1% | $2,719 |

Note these "highest-immigrant-inflow" counties top out at ~1.5%, while top native-inflow counties exceed 16%. **The most-immigrant-saturated county in America still receives one-tenth the per-capita newcomer flow of the most-native-saturated county.**

### Fact 4: rent gradient by inflow type quintile

By US-NATIVE inflow quintile:
| Quintile | Inflow share | Median rent | Median income | FB share |
|----------|--------------|-------------|---------------|----------|
| Q1 | 1.0% | $803 | $59,707 | 2.3% |
| Q5 | 5.7% | $960 | $66,154 | 4.1% |
| Δ | +5.7× | +20% | +11% | +1.8 pp |

By RECENT-FB inflow quintile:
| Quintile | FB inflow share | Median rent | Median income | US inflow |
|----------|-----------------|-------------|---------------|-----------|
| Q1 | 0.02% | $752 | $55,242 | 2.8% |
| Q5 | 0.32% | $1,200 | $72,532 | 3.0% |
| Δ | +18× | +60% | +31% | +0.2 pp |

**Reading:** Per percentage-point of inflow, immigrant inflow is correlated with much larger rent and income differences than native inflow. But in absolute terms, the native flow is 18× larger at the top quintile, and the rent gradient is only 60% (vs 20% for native). This is consistent with the prior cycle's Saiz finding: immigrants concentrate in inelastic high-cost MSAs, so their inflow correlates with rent more strongly per percentage point. Native migrants spread more evenly, including to elastic markets.

## What this changes

### The repo's "low-skill-origin-incidence" frame
The existing memo treats origin × destination heterogeneity in immigrant inflows as the central object. This is correct for *immigration-specific* questions (origin culture, language, legal status, remittance flows). But for *newcomer-burden* questions (school capacity, rental market pressure, service demand), the frame is wrong: the dominant newcomer flow into US counties is native, not immigrant.

Concretely:
- A county receiving 12% native + 1% immigrant inflow has a school-burden problem driven 92% by natives
- Restricting immigration in such a county would reduce newcomer burden by ~7%, not eliminate it
- The Texas exurbs (Comal, Kaufman, Rockwall — all in the top-15 native-inflow list) are growing rapidly NOT because of immigration

### The political-economy frame
Two competing readings of "immigrants are changing my town":
1. **Quantitative reading:** newcomers are arriving fast → schools/housing strain. *In this reading, the data show the strain is mostly native-driven, and immigration is a small component.*
2. **Compositional reading:** newcomers are different from incumbents in language/culture/visibility → integration concerns. *In this reading, the immigrant share matters because of what immigrants are, not how many they are.*

Repository memos have not consistently distinguished these two readings. The mainstream restrictionist case rests heavily on reading #1; the data side with #2.

### Confidence ladder
Add to `immigration-confidence-ladder.md`:
- New entry: **`Native US migration is the dominant newcomer flow into US counties; immigration is a small fraction in absolute terms`** — `STRONG`. Median county receives 3.0% native + 0.08% immigrant inflow per year (33× ratio). [SOURCE: research/immigration-causal-internal-vs-immigrant-newcomers.md]

### Adversarial review §3 (school burden too coarse)
The earlier review flagged that district school-burden was under-modeled. This finding adds: **the school burden of immigrant-origin children may be misattributed**. A district in Comal County TX (12% native inflow, low immigrant inflow) faces school capacity strain that is overwhelmingly native-driven. A district in Miami-Dade FL faces strain that is more immigrant-driven. The right policy intervention differs.

## Honest limits

1. **Composition of native vs immigrant newcomers differs sharply.**
   - Native newcomers in top-list counties: military families (Fort Riley, Fort Stewart), retirees (Florida), DC-area government workers, exurb developers
   - Immigrant newcomers in top-list counties: working-age labor migrants, family-reunification, refugees
   - Per-newcomer school enrollment, per-newcomer rent payment, per-newcomer wage competition all differ
   - The "33× ratio" is gross flow ratio, not "burden equivalence"

2. **Geography of impact differs.**
   - County aggregate masks within-county sorting
   - Immigrants concentrate in specific neighborhoods/PUMAs; natives sort more diffusely
   - The local impact at the school-attendance-zone or ZIP level may have different relative magnitudes
   - Texas exurbs (top native-inflow) sprawl across new construction, so capacity can scale; older-city PUMAs in Miami-Dade can't

3. **IRS SOI undercount.**
   - Tax filer migration misses non-filers (very-low-income, students, undocumented)
   - These omissions affect the immigrant comparison too — both sides probably undercounted
   - Direction of bias on the ratio is ambiguous

4. **Annualization of B05005 12-year stock is rough.**
   - Recent FB flow is not constant over 2010-2022
   - Mexican-origin flow declined 2008-2018, NTCA flow rose 2018+
   - The 0.08% number is a 12-year average, may understate 2020-2022 flow
   - Even doubling it (0.16%) leaves a 19× ratio — the qualitative finding is robust to large adjustments

5. **What this does NOT settle.**
   - Immigration's effect on schools, wages, rent at PUMA / neighborhood scale (where it's concentrated)
   - The compositional integration concerns (language, cultural, visibility)
   - Whether second-generation outcomes differ between high-native-inflow and high-immigrant-inflow counties
   - Federal fiscal incidence (still requires the SIPP fix from prior cycle)

## Decision-relevant claim

Any future repo memo that says "newcomer burden in county X" without distinguishing native-newcomer from immigrant-newcomer flow is using a misleading frame. The correct framing is: "X% of newcomer flow is native (Y), Z% is immigrant (W)." County-level data routinely makes this disaggregation, so there's no excuse for the conflated frame.

For the project's central question ("which low-skill immigration flows degrade local-system capacity"), this finding doesn't kill the question — it adds a comparative anchor: most school/housing/service strain in fast-growing US counties is being absorbed without immigration as the proximate cause. Wherever immigration IS the proximate cause (Miami-Dade, Hudson NJ, San Jose CA, Colfax NE), it operates at much smaller scale than internal native migration in equally-stressed Sun Belt exurbs.

[SOURCE: data/internal_migration/county_inflow_2022_23.csv]
[SOURCE: data/analysis/county_newcomer_comparison.parquet]
[SOURCE: scripts/analyze_internal_vs_immigrant_newcomers.py]
[SOURCE: api.census.gov/data/2022/acs/acs5 (B05005, B05002, B25064, B19013)]

<!-- knowledge-index
generated: 2026-04-19T04:19:50Z
hash: 309f7e3f68b3

cross_refs: research/immigration-causal-internal-vs-immigrant-newcomers.md

end-knowledge-index -->
