claude-opus-5-5

**Verdict:** H1 holds in part and H2 fails, so step 4 (sizing in $bn) was not run [CALCULATION: `derived/verdict.csv`]. A county with 10 points more Hispanic residents has economic connectedness (EC) lower by 0.027 (se 0.006, 0.15 SD). The comparison holds median income, poverty, BA+ share, density, Black share and state fixed. Weighted by low-income children the fall is 0.019 (0.005), and it survives dropping any one state. Between ZIP codes in the same county the fall is 0.044 (0.003) [CALCULATION: `derived/h1_county.csv`, `h1_loso.csv`, `h1_zip.csv`]. Three named components move EC at an equal Hispanic share [CALCULATION: `h1_county.csv`, `h1_county_seg_restricted.csv`, set `hisp_components*`]:
- **Hispanic adults' schooling:** +10 points BA+ among Hispanic adults goes with EC +0.005 to +0.021.
- **Residential segregation:** +0.10 Hispanic/non-Hispanic-white dissimilarity goes with EC −0.011 to −0.028 and higher friending bias.
- **Limited-English Spanish households:** null.

Between 50% and 89% of the Hispanic-share association is exposure, meaning fewer high-SES people in the groups where low-SES people make friends. The rest is class friending bias [CALCULATION: `derived/decomposition.csv`]. Network cohesion (clustering, support ratio) barely moves. EC predicts upward mobility, including for white children, and non-Hispanic white household income. The link does not steepen with county size: of 40 connectedness × log-population cells, 1 is positive at p<0.05, 16 are negative and 23 are null. The Hispanic share × log-population interaction is null for non-Hispanic white income (+0.0002, se 0.0026) [CALCULATION: `derived/bridge_county.csv`]. All of this is cross-sectional and identifies no causal effect. The Atlas measures ties across social class, not across ethnic groups (§1).

# Connectedness, Hispanic share and its components (lane 2026-09-28)

Wording rule (operator, 2026-09-28): no composite heterogeneity index is used as an explanatory
variable or in any claim. Each variable is named: the share of a named group, its schooling,
limited English, residential segregation, or friending bias. One regression on the four-group
Herfindahl complement is kept, labelled `lit_comparison_*`, only to line up with the papers in §1.

## 1. Steel-man, written before any regression

**For H1 (a larger Hispanic share lowers connectedness at equal SES).** The repo's survey work
finds a Hispanic-generation trust gap near −10 to −12 pp that persists after fuller measurement
(ladder 117) [SOURCE: `research/immigration-confidence-ladder.md` entry 117]. It finds
Mexican-origin turnout gaps of −9 to −13 points at equal SES and spousal endogamy of 90/72/56% by
generation (ladder 233) [SOURCE: entry 233]. On network grounds, ties form more readily within a
language and origin group, so a population with a larger, residentially separate minority group
has fewer bridging ties per person at equal size [INFERENCE].

**For H2 (connectedness raises output superlinearly with size).** Bettencourt et al. (2007, *PNAS*
104(17):7301–7306) find that urban wages, GDP and patents scale with population at exponents of
about 1.1–1.3 and attribute this to interaction density [TRAINING-DATA]. Chetty et al. (2022a,
*Nature* 608:108–121) find county EC is the strongest correlate of upward mobility among their
social-capital measures, near r = 0.65 [TRAINING-DATA].

**What the index-based papers count.** These citations are from training data and were not
re-read in this lane:
- **Putnam (2007)** [TRAINING-DATA]. The index is one minus the Herfindahl over four census groups
  (Hispanic, non-Hispanic white, Black, Asian) in the respondent's community, from the 2000 Social
  Capital Community Benchmark survey. Across US places it varies mainly with the Hispanic and Black
  shares. Abascal & Baldassarri (2015, *AJS* 121(3):722–782) re-analyse the data. They attribute
  most of the trust association to Black and Hispanic respondents reporting lower trust and to
  economic disadvantage, not to white residents trusting less where those shares are higher.
- **Alesina & La Ferrara (2000, *QJE* 115(3):847–904)** [TRAINING-DATA; INFERENCE on the driver].
  The index covers five 1990 census race categories (white, Black, American Indian, Asian/Pacific
  Islander, other) by metro area. Hispanics are mostly coded "white" or "other" race, so the index
  moves mainly with the Black share. Lower group participation is concentrated among respondents
  who state aversion to racial mixing.
- **Alesina, Baqir & Easterly (1999, *QJE* 114(4):1243–1284)** [TRAINING-DATA; INFERENCE on the
  driver]. Same five-race 1990 index for cities, counties and metro areas, again mostly Black–white
  variation. Higher values go with smaller budget shares for roads, sewers and education.
- **Ottaviano & Peri (2006, *JEG* 6(1):9–44)** [TRAINING-DATA]. The index is one minus the
  Herfindahl over country-of-birth groups, with the US-born as one group, for about 160 metro areas
  1970–1990. The US-born are 80–95% of residents, so the index is close to twice the foreign-born
  share and effectively measures foreign-born share. Their positive effect on US-born wages and
  rents is instrumented. I do not recall them separating it by origin group or schooling
  [UNVERIFIED].
- **Alesina, Harnoss & Rapoport (2016, *JEG* 21(2):101–138)** [TRAINING-DATA]. The index is the
  Herfindahl over origin countries within each country's immigrant population, about 195 countries
  in 1990–2000. The positive income result comes from the origin spread of tertiary-educated
  immigrants and is larger in richer destination countries.
- **Burchardi et al. (NBER w27075, 2020)** [TRAINING-DATA]. The main regressor is the number of
  immigrants into a county, instrumented with historical ancestry-predicted flows, not an index.
  More immigrants raise local patenting and wages.
- **Dinesen, Schaeffer & Sønderskov (2020, *Annual Review of Political Science* 23:441–465)**
  [TRAINING-DATA]. A meta-analysis of 87 studies that use either indices or minority and immigrant
  shares. They find a small negative association with trust, concentrated in trust of neighbours.

**The repo's own results against H1.** Ladder 89: foreign-born share shows no association with
police and corrections spending per capita across states, at equal income, urbanization, Black
share and crime [SOURCE: entry 89]. Ladder 149: a rising Hispanic share does not shift local budgets
from schools to police [SOURCE: entry 149]. On H2, `scaling_test_2026_09_20` found that a
cross-sectional scaling exponent does not transfer to growth [SOURCE: lane README].

**Construct limit of the Atlas (read before any result).**
- The Social Capital Atlas measures friendships across socioeconomic status (SES), not across
  ethnic groups [SOURCE: Atlas codebook, `_cache/sca/readme.pdf` §2.1].
  - EC is twice the share of high-SES friends among low-SES Facebook users aged 25–44 with ≥100 US
    friends, with SES ranked nationally.
  - Friending bias is class friending bias.
  - Clustering and support ratio measure network cohesion regardless of group.
- The county association of Hispanic share with EC therefore mixes three things:
  1. fewer high-SES people nearby;
  2. Hispanic low-SES users having fewer high-SES friends than other low-SES users (EC averages
     over them too);
  3. any spillover onto other residents' ties.
- Only (3) is the operator's claim, and county means cannot separate it from (2).
- Users whose networks are mostly abroad or off Facebook are excluded.

## 2. Data acquired

| File | URL | Retrieved (UTC) | Bytes | sha256 |
|---|---|---|---|---|
| `_cache/sca/social_capital_county.csv` | https://data.humdata.org/dataset/85ee8e10-0c66-4635-b997-79b6fad44c71/resource/ec896b64-c922-4737-b759-e4bd7f73b8cc/download/social_capital_county.csv | 2026-09-28 13:26 | 717,799 | 69de384096214aad20d0739d522b3731d6fa9bee5cff32c66eb5df89b8fb3828 |
| `_cache/sca/social_capital_zip.csv` | …/resource/ab878625-279b-4bef-a2b3-c132168d536e/download/social_capital_zip.csv | 2026-09-28 13:27 | 4,052,257 | 8eec444ff54ed2cad0bf7e3b2927938c80d262f46c9a2405359e7265184936a3 |
| `_cache/sca/readme.pdf` (codebook, July 2022) | …/resource/fbe5b0b9-e81c-41c7-a9f2-3ebf8212cf64/download/data_release_readme_31_07_2022_nomatrix.pdf | 2026-09-28 13:27 | 310,184 | 431f73ada2720112f6eea209377719a8ccac99766a44fa3d6b25ae55b2844723 |
| `_cache/oa/county_outcomes_simple.csv` (Opportunity Atlas) | https://opportunityinsights.org/wp-content/uploads/2018/10/county_outcomes_simple.csv | 2026-09-28 | 1,731,009 | in `derived/input_hashes.csv` |
| `_cache/gaz/2020_Gaz_{counties,zcta}_national.zip` | https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2020_Gazetteer/ | 2026-09-28 | 141,524 / 998,037 | in `derived/input_hashes.csv` (unzipped .txt) |
| `_cache/acs/acs5_2018_{county,zcta}.json` | ACS 5-year 2014–2018 API, `pull_acs.py`; URLs with the key redacted in `_cache/acs/manifest.json` | 2026-09-28 | 497,460 / 4,318,901 | in manifest and `input_hashes.csv` |
| `_cache/acs/comp_{county,zcta}.json`, `_cache/acs/tract/tract_{51 states+DC}.json` | ACS 5-year 2014–2018 API, `pull_acs_components.py`: B03002_006 (Asian), C16002 (limited-English households by language), C15002I (Hispanic adults' schooling); tract B03002 for segregation | 2026-09-28 13:45 | 289,984 / 2,416,902; tracts 7,374,520 in total | per file in `_cache/acs/manifest_components.json` (that file's hash is in `input_hashes.csv`) |
| BEA CAINC4 (reused, not re-fetched) | `causal_evidence_2026_09_20/raw/county_outcomes/raw/bea_cainc4/CAINC4.csv`, official https://apps.bea.gov/regional/zip/CAINC4.zip | 2026-09-20 | 29,012,947 | 61858e273cbd7dcfb2a9d374952cc65ef0f3cb4ce45eac5a7c851f291b6d0ceb |

- **Patents:** dropped under the brief's "only if cheap" rule. No county series is local (the
  agglomeration lane's Lai inventor file was never staged), and the USPTO county page returns 404
  [DATA: `curl -I` 404 on 2026-09-28].
- **Opportunity Atlas:** the county file was not previously local (ladder 82 used the national race
  tables), so it was fetched.
- **Dataset register:** not edited from this lane (worker scope). The rows above carry what a
  register entry needs.

## 3. Design

[CALCULATION: `analyze.py`] OLS with state fixed effects (county FE in the within-county ZIP arm).
CR1 standard errors are clustered by state (51 clusters), with t critical values on 50 degrees of
freedom. Every regression runs unweighted (county as the unit) and weighted by `num_below_p50`, the
Atlas's own weight. All regressors are per 10 points (0.10). `coef_in_y_sd` divides by the outcome
SD, and `mde80` is the minimum detectable effect at 80% power and 5% size.

**Controls** (brief): log median household income, poverty rate, BA+ share, log population
density, non-Hispanic Black share. Covariates come from ACS 2014–2018, matching the Atlas's 2018
population base.

**Named components:**

| Variable | Definition |
|---|---|
| `hisp_sh`, `mex_sh`, `nonmex_hisp_sh` | Hispanic, Mexican-origin and other-Hispanic shares |
| `asian_sh`, `black_sh` | Non-Hispanic Asian and non-Hispanic Black shares |
| `fb_sh` | Foreign-born share |
| `hisp_ba_sh` | BA+ share among Hispanic adults 25+ |
| `lep_spanish_sh` | Share of households that are limited-English and Spanish-speaking |
| `seg_d_hisp_white` | Tract-level Hispanic/non-Hispanic-white dissimilarity, ½Σ\|hᵢ/H − wᵢ/W\| |
| `seg_white_exposure_hisp` | Non-Hispanic-white exposure to Hispanics, Σ(wᵢ/W)(hᵢ/tᵢ) |

Segregation is defined for counties with ≥2 populated tracts. A restricted arm keeps counties with
≥1,000 Hispanic residents and ≥5 tracts, because dissimilarity is inflated where the group is small.

**Gates**, all passing [DATA: `derived/gates.csv`]:
- 3,016 of 3,018 Atlas EC counties join to the ACS and land area, and all 18,980 EC ZIPs join.
- ACS population equals the Atlas `pop2018`.
- The identity ec_grp/exposure = 1 − bias holds to 2×10⁻⁵.
- 3,089 counties have an Opportunity Atlas record and 3,057 have BEA data.
- The population-weighted Hispanic share is 0.178.
- Segregation is defined for all 2,882 eligible counties. The median dissimilarity in the 101
  counties with ≥100k Hispanics is 0.455, within the published metro range [INFERENCE].
- Limited-English and Asian shares join for all 3,018 counties.

Rerunning twice gives byte-identical `derived/*.csv`, checked after the component revision
[CALCULATION: sha256 of two consecutive runs, 2026-09-28].

## 4. H1: connectedness and the Hispanic share (tests 1–2)

County, with controls, per 10 points of Hispanic share [CALCULATION: `derived/h1_county.csv`]:

| Measure | Unweighted | SD units | Weighted | Reading |
|---|---|---|---|---|
| EC (adults) | −0.027 (0.006) | −0.15 | −0.019 (0.005) | holds; leave-one-state-out range −0.039 to −0.025 (unw) and −0.023 to −0.015 (w), all p<0.002 |
| EC, Mexican-origin / other-Hispanic share | −0.028 (0.008) / −0.022 (0.010) | −0.16 / −0.12 | −0.025 (0.008) / −0.009 (0.008) | the Mexican-origin share carries it |
| Childhood EC (high-school friends) | −0.010 (0.002) | −0.04 | −0.006 (0.006) | small; null weighted (MDE 0.018) |
| EC of high-SES people | −0.010 (0.003) | −0.06 | −0.012 (0.009) | small |
| Clustering | −0.0006 (0.0006) | −0.03 | −0.0021 (0.0006) | null unweighted; −0.12 SD weighted |
| Support ratio | −0.0002 (0.0004) | −0.01 | −0.0016 (0.0009) | null |
| Volunteering rate | −0.0072 (0.0005) | −0.21 | −0.0060 (0.0004) | lower |
| Civic organizations per 1,000 users | −0.0012 (0.0002) | −0.12 | −0.0006 (0.0002) | lower |

At ZIP level with controls, EC is lower by 0.033 (0.004) with state FE and by 0.044 (0.003)
between ZIPs in the same county (−0.20 SD). Clustering falls by 0.001 (−0.05 SD) and the support
ratio is null [CALCULATION: `derived/h1_zip.csv`].

**Named groups entered together** (county, controls, per 10 points; set `named_groups`)
[CALCULATION: `h1_county.csv`]:

| Share | EC, unweighted | EC, weighted |
|---|---|---|
| Hispanic | −0.016 (0.004) | −0.014 (0.005) |
| Black | −0.020 (0.003) | −0.025 (0.002) |
| Asian | +0.045 (0.019) | +0.034 (0.021) |
| Foreign-born | −0.036 (0.010) | −0.009 (0.011), null |

The Hispanic coefficient shrinks from −0.027 to −0.016 once the foreign-born share enters, since
the two overlap. At ZIP level within county: Hispanic −0.034 (0.003), Black −0.033 (0.002),
foreign-born −0.026 (0.004), Asian +0.009 (0.006) [CALCULATION: `h1_zip.csv`].

**Hispanic components at equal Hispanic share** (county, controls; each per 10 points or 0.10)
[CALCULATION: `h1_county.csv`, `h1_county_seg_restricted.csv`]:

| Component | EC, unw / w | Exposure, unw / w | Friending bias, unw / w |
|---|---|---|---|
| Hispanic adults' BA+ share | +0.005 (0.002) / +0.021 (0.005) | +0.003 / +0.012 | −0.003 (0.001) / −0.010 (0.003) |
| Limited-English Spanish households | +0.001 (0.021) / +0.008 (0.021), null | +0.014 / +0.040, imprecise | −0.019 / −0.026 (0.006) |
| Dissimilarity, Hispanic/NH white (+0.10) | −0.011 (0.002) / −0.023 (0.004) | −0.010 / −0.024 | +0.003 (0.001) / +0.007 (0.003) |
| Same, restricted arm | −0.020 (0.003) / −0.028 (0.004) | −0.020 / −0.032 | +0.003 / +0.009 (p≈0.08) |
| NH-white exposure to Hispanics (+0.10) | +0.049 (0.018) / +0.054 (0.009) | +0.058 / +0.044 | −0.004 / −0.033 (0.016) |

The Hispanic share itself stays at −0.024 unweighted and −0.018 weighted with schooling,
limited English and dissimilarity held fixed. Where Hispanic and white residents live in the
same tracts, EC is higher and friending bias lower at the same Hispanic share. Where Hispanic
adults hold more degrees, EC is higher. The limited-English share of households adds nothing
detectable once those are held.

At ZIP level within county, Hispanic adults' BA+ share goes with EC +0.004 (0.001) unweighted and
+0.010 (0.002) weighted. The limited-English Spanish share goes with exposure −0.035 (0.012) and
with EC −0.012 (0.007), not significant [CALCULATION: `h1_zip.csv`, set `hisp_components`].

**Decomposition of the Hispanic-share slope.** ln EC_grp = ln exposure + ln(1 − bias) exactly, so
the slope splits additively [CALCULATION: `derived/decomposition.csv`]:

| Arm (controls) | Exposure share | Friending-bias share |
|---|---|---|
| County, unweighted | 0.50 | 0.50 |
| County, weighted | 0.79 | 0.21 (bias not significant, p=0.34) |
| ZIP, state FE, unweighted / weighted | 0.69 / 0.89 | 0.31 / 0.11 |
| ZIP, within county, unweighted / weighted | 0.73 / 0.80 | 0.27 / 0.20 |
| Childhood (high school), county, unweighted / weighted | 0.51 / 0.46 | 0.49 / 0.54 |

**What H1 does and does not show [INFERENCE].**
- **Mechanism.** EC averages over all low-SES residents, Hispanic ones included, and SES is ranked
  nationally. The Hispanic-share slope is therefore partly the Hispanic residents' own ties
  (composition), not other residents' ties, and the public files carry no race-specific EC to split
  them.
- **Segregation is the actionable part.** The segregation and schooling components are closer to
  the operator's mechanism. At equal Hispanic share, more residential separation and less Hispanic
  schooling go with fewer cross-class ties and more friending bias.
- **Cohesion.** Clustering and support ratio, which describe tie structure, move little with any
  named share.
- **Volunteering and civic pages.** Both are lower, but they rest on classifiers of Facebook group
  and page titles, and the codebook does not say whether Spanish-language groups are classified as
  reliably [SOURCE: codebook §2.1].

## 5. H2: does connectedness scale output? (test 3)

The outcomes are:
- Opportunity Atlas p25 child income rank, pooled and white (1978–83 cohorts);
- BEA 2018 per-capita personal income;
- BEA 2018 place-of-work earnings per resident;
- ACS 2014–2018 non-Hispanic white median household income.

Predictors are standardized (county SD), and the controls are Hispanic share, Black share, BA+
share and log density, with state FE [CALCULATION: `derived/bridge_county.csv`, spec `base`].

**Level (EC, per SD):**

| Outcome | Unweighted | Weighted |
|---|---|---|
| Pooled mobility (rank) | +0.033 (0.003), 0.55 SD | +0.027 (0.002), 0.64 SD |
| White children's mobility | +0.020 (0.002), 0.36 SD | +0.018 (0.004), 0.43 SD |
| NH white median household income | +11.1% (2.1) | +8.9% (1.5) |
| Per-capita personal income | +5.9% (0.9) | −0.8% (2.6) |
| Place-of-work earnings per resident | −1.8% (1.8) | −14% (6.3) |

The mobility links survive adding income and poverty controls: pooled +0.028 unweighted and
+0.021 weighted; white +0.015 and +0.013.

**Connectedness × centered ln population.** Across 40 cells (EC, childhood EC, clustering and
support ratio × 5 outcomes × 2 weights), 1 is positive at p<0.05, 16 are negative and 23 are null.
- The one positive cell is EC × ln pop for non-Hispanic white income, unweighted: +1.25% per SD per
  log point (se 0.37). Weighted it is +0.15% (se 0.38, MDE 1.1%).
- For pooled mobility the EC interaction is −0.0025 (0.0006) unweighted and −0.0003 (0.0011)
  weighted, with MDE 0.003. The design would have caught an interaction a tenth the size of the
  level effect.
- **H2 fails.** Connectedness predicts outcomes about equally in small and large counties, or more
  strongly in small ones [CALCULATION: `derived/verdict.csv`].

**Direct check on named shares: does the population slope weaken where the Hispanic share is
higher?** Per 10 points of share per log point of population [CALCULATION: `bridge_county.csv`,
`hisp_share_scale_interaction`, `fb_share_scale_interaction`]:

| Outcome | Hispanic share × ln pop, unw / w | Foreign-born share × ln pop, unw / w |
|---|---|---|
| NH white median household income | +0.0002 (0.0026) / −0.0004 (0.0024) | −0.003 (0.003) / −0.007 (0.003) |
| Per-capita personal income | −0.004 (0.003) / +0.003 (0.003) | +0.003 (0.004) / +0.010 (0.005) |
| Place-of-work earnings per resident | −0.020 (0.004) / −0.006 (0.004) | −0.032 (0.008) / −0.010 (0.010) |
| Pooled mobility | +0.0014 (0.0005) / +0.0014 (0.0008) | +0.0037 (0.0006) / +0.0020 (0.0007) |
| White children's mobility | +0.0011 (0.0007) / +0.0015 (0.0010) | +0.0044 (0.0012) / +0.0033 (0.0009) |

For non-Hispanic white income the Hispanic-share interaction is a precise null. A 10-point higher
Hispanic share changes the income–population slope by less than about ±0.5% per log point (95% CI).
Two unweighted cells point in the operator's direction: earnings per resident falls with the
Hispanic and foreign-born shares × size. Neither survives weighting. Mobility runs the other way.

The comparison with the index literature (`lit_comparison_frac_scale_interaction`, four-group
Herfindahl complement × ln pop) is positive for mobility and per-capita income. It is kept only so
the numbers line up with the papers in §1, not as an explanatory claim.

## 6. Step 4: sizing

Step 4 was not run. The brief says to stop if either hypothesis fails, and H2 failed. For scale
only, H1's own coefficient implies the following. Moving a county's Hispanic share by 10 points
moves EC by 0.019–0.027, or 0.11–0.15 SD. The level link then predicts child mobility at
0.02–0.03 rank per SD of EC, which is 0.0021–0.0050 rank points per 10 points of share
[CALCULATION: products of the §4 and §5 coefficients].

That chain is a product of two cross-sectional slopes. It includes the composition term, which
changes no other resident's ties, and it is not a causal or dollar estimate. If the operator
wants a lever rather than a headcount, §4 points at residential segregation and Hispanic adults'
schooling, both with the same identification limits [INFERENCE].

## 7. Limits

- The Atlas measures class connectedness, not ethnic connectedness. No Atlas file measures ties
  across ethnic groups directly.
- The sample is Facebook users aged 25–44 with ≥100 US friends. People whose networks are abroad
  or offline, disproportionately recent immigrants, are excluded.
- The design is cross-sectional with state FE only. No instrument and no panel: the Atlas is a
  single 2022 snapshot. Segregation is as endogenous as the share: people sort on both.
- Mobility outcomes are for 1978–83 birth cohorts and predate the EC snapshot.
- The limited-English measure is a household status (no one 14+ speaks English "very well"),
  not individual proficiency.
- No patents (§2). Dataset register not updated (worker scope).

## Revisions

- 2026-09-28, after the operator's wording instruction relayed by the lead:
  - dropped the composite index as an explanatory variable;
  - added named-group shares, Hispanic adults' schooling, limited-English households and tract
    segregation (dissimilarity, exposure) with a restricted arm, and Hispanic- and foreign-born-share
    × ln-population interactions;
  - rewrote §1 to state what each cited index counts.

  The H1/H2 verdict is unchanged.
