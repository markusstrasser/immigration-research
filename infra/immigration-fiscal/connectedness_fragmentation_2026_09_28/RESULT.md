claude-opus-5-5

**Verdict:** H1 holds in part and H2 fails, so step 4 (sizing in $bn) was not run [CALCULATION: `derived/verdict.csv`]. At equal income, poverty, education, density, Black share and state, a county with 10 points more Hispanic residents has economic connectedness (EC) lower by 0.027 (se 0.006), or 0.15 SD. Weighted by low-income children the fall is 0.019 (0.005), and it survives dropping any one state [CALCULATION: `derived/h1_county.csv`, `h1_loso.csv`]. Between ZIP codes in the same county the fall is 0.044 (0.003) [CALCULATION: `derived/h1_zip.csv`]. Between 50% and 89% of it is exposure, meaning fewer high-SES people in the same groups. The rest is class friending bias [CALCULATION: `derived/decomposition.csv`]. Network cohesion (clustering, support ratio) barely moves. EC does predict upward mobility, including for white children, and non-Hispanic white household income at equal controls. But the slope does not steepen with county size: of 40 connectedness × log-population cells, 1 is positive at p<0.05, 16 are negative and 23 are null [CALCULATION: `derived/bridge_county.csv`]. Fractionalization × log population is positive for mobility and per-capita income, the opposite of the scale claim. All of this is cross-sectional; nothing here identifies a causal effect. The Atlas measures ties across social class, not across ethnic groups (§1).

# Connectedness and fragmentation (lane 2026-09-28)

## 1. Steel-man, written before any regression

**For H1 (a larger Hispanic share lowers connectedness).** The literature below measures ethnic fractionalization (1 − Σ shares², which counts groups and their evenness, not who they are); each result is read for which groups drive it. Putnam (2007, *Scandinavian Political Studies*
30(2):137–174) reports from the 2000 Social Capital Community Benchmark survey that in more
ethnically diverse US communities residents trust neighbours less, including neighbours of their own
group ("hunkering down"), and have fewer friends, controlling for individual and area SES
[TRAINING-DATA]. Alesina & La Ferrara (2000, *QJE* 115(3):847–904) find lower participation in
associations in more racially fragmented US localities [TRAINING-DATA]. Alesina, Baqir & Easterly
(1999, *QJE* 114(4):1243–1284) find that more ethnically fragmented US cities and counties spend
less of their budgets on productive public goods (roads, sewers, education) [TRAINING-DATA]. The
repo's own survey work finds the Hispanic-generation trust gap near −10 to −12 pp persists after
fuller measurement (ladder 117) [SOURCE: `research/immigration-confidence-ladder.md` entry 117],
and Mexican-origin civic gaps at equal SES of −9 to −13 turnout points (ladder 233) [SOURCE: entry
233]. The mechanism the operator names is plausible on network grounds: ties form more readily
within language and ethnic groups, so a population split into groups has fewer bridging ties per
person at equal size.

**For H2 (connectedness scales output).** Bettencourt et al. (2007, *PNAS* 104(17):7301–7306)
find urban socioeconomic outputs (wages, GDP, patents) scale superlinearly with population
(exponent ~1.1–1.3), and the model attributes this to social interaction density [TRAINING-DATA].
Chetty et al. (2022a, *Nature* 608:108–121) find county economic connectedness (EC) is the
strongest single correlate of upward mobility among the social-capital measures, with a county
correlation near 0.65, and it survives controls for race shares, income and segregation
[TRAINING-DATA]. If ties are the channel for superlinear scaling, fragmentation would reduce the
effective network size.

**Against.** Ottaviano & Peri (2006, *JEG* 6(1):9–44) find US-born workers' wages and rents are
higher in metros with more birthplace diversity (instrumented) [TRAINING-DATA]. Alesina, Harnoss &
Rapoport (2016, *JEG* 21(2):101–138) find birthplace diversity of the skilled raises country income
[TRAINING-DATA]. Burchardi et al. (NBER w27075, 2020) instrument county immigration with historic
ancestry and find more immigration raises local patenting and wages [TRAINING-DATA]. Abascal &
Baldassarri (2015, *AJS* 121(3):722–782) re-analyse Putnam's data and find the diversity–trust
association mostly reflects the lower trust reported by disadvantaged and minority residents
(composition), not whites trusting less in diverse places [TRAINING-DATA]; Dinesen, Schaeffer &
Sønderskov (2020, *Annual Review of Political Science* 23:441–465) meta-analyse 87 studies and find
a small negative diversity–trust association, concentrated in neighbour trust [TRAINING-DATA]. The
repo's own county and state work finds no diversity effect on coercion spending (ladder 89) and no
shift of local budgets from schools to police (ladder 149) [SOURCE: entries 89, 149]. On H2, the
repo's scaling test found no universal sublinear service-cost exponent that transfers from cross
section to growth (`scaling_test_2026_09_20`) [SOURCE: lane README], and a cross-sectional scaling
exponent is not the effect of adding people.

**Construct limit of the Atlas (read before any result).** The Social Capital Atlas measures
friendships *across socioeconomic status*, not across ethnic groups. EC is twice the share of
high-SES friends among low-SES Facebook users aged 25–44 with ≥100 US friends; SES is ranked
nationally; friending bias is class friending bias; clustering and support ratio are network
cohesiveness regardless of group [SOURCE: Atlas codebook, `_cache/sca/readme.pdf` §2.1]. So "less
fragmentation" in the operator's ethnic sense has no direct Atlas measure; the county association of
Hispanic share with EC mixes (i) fewer high-SES people nearby, (ii) Hispanic low-SES users having
fewer high-SES friends than other low-SES users (composition of whom EC averages over), and (iii)
any spillover onto other residents' ties. Only (iii) is the operator's claim, and county means
cannot separate it from (ii). Users with networks mostly abroad or off Facebook are excluded.

## 2. Data acquired

| File | URL | Retrieved (UTC) | Bytes | sha256 |
|---|---|---|---|---|
| `_cache/sca/social_capital_county.csv` | https://data.humdata.org/dataset/85ee8e10-0c66-4635-b997-79b6fad44c71/resource/ec896b64-c922-4737-b759-e4bd7f73b8cc/download/social_capital_county.csv | 2026-09-28 13:26 | 717,799 | 69de384096214aad20d0739d522b3731d6fa9bee5cff32c66eb5df89b8fb3828 |
| `_cache/sca/social_capital_zip.csv` | …/resource/ab878625-279b-4bef-a2b3-c132168d536e/download/social_capital_zip.csv | 2026-09-28 13:27 | 4,052,257 | 8eec444ff54ed2cad0bf7e3b2927938c80d262f46c9a2405359e7265184936a3 |
| `_cache/sca/readme.pdf` (codebook, July 2022) | …/resource/fbe5b0b9-e81c-41c7-a9f2-3ebf8212cf64/download/data_release_readme_31_07_2022_nomatrix.pdf | 2026-09-28 13:27 | 310,184 | 431f73ada2720112f6eea209377719a8ccac99766a44fa3d6b25ae55b2844723 |
| `_cache/oa/county_outcomes_simple.csv` (Opportunity Atlas) | https://opportunityinsights.org/wp-content/uploads/2018/10/county_outcomes_simple.csv | 2026-09-28 | 1,731,009 | see `derived/input_hashes.csv` |
| `_cache/gaz/2020_Gaz_{counties,zcta}_national.zip` | https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2020_Gazetteer/ | 2026-09-28 | 141,524 / 998,037 | see `derived/input_hashes.csv` |
| `_cache/acs/acs5_2018_{county,zcta}.json` | ACS 5-year 2014–2018 API, `pull_acs.py`; URLs (key redacted) in `_cache/acs/manifest.json` | 2026-09-28 | 497,460 / 4,318,901 | in manifest |
| BEA CAINC4 (reused, not re-fetched) | `causal_evidence_2026_09_20/raw/county_outcomes/raw/bea_cainc4/CAINC4.csv`, official https://apps.bea.gov/regional/zip/CAINC4.zip | 2026-09-20 | 29,012,947 | 61858e273cbd7dcfb2a9d374952cc65ef0f3cb4ce45eac5a7c851f291b6d0ceb |

No county patent series is local (the agglomeration lane's Lai inventor file was never staged) and
the USPTO county page returns 404; patents are dropped per the brief's "only if cheap" rule [DATA:
`curl -I` 404 on 2026-09-28]. The Opportunity Atlas county file was not previously local (ladder 82
used the national race tables), so it was fetched. The dataset register is not edited from this lane
(worker scope); the rows above are what a register entry needs.

## 3. Design

[CALCULATION: `analyze.py`] OLS with state fixed effects (county FE in the within-county ZIP arm).
CR1 standard errors are clustered by state (51 clusters), with t critical values on 50 degrees of
freedom. Every regression runs unweighted (county as the unit) and weighted by `num_below_p50`
(the Atlas's own weight). Coefficients on shares are per 10 percentage points. `coef_in_y_sd`
divides by the outcome's SD, and `mde80` is the minimum detectable effect at 80% power and 5% size,
(t₀.₉₇₅ + 0.84) × se. The controls follow the brief: log median household income, poverty rate,
BA+ share, log population density, non-Hispanic Black share. Covariates come from ACS 2014–2018,
matching the Atlas's 2018 population base. Shares tested: Hispanic; Mexican and non-Mexican
Hispanic entered together; foreign-born; four-group fractionalization (NH white, NH Black,
Hispanic, other).

The gates all pass [DATA: `derived/gates.csv`]:
- 3,016 of 3,018 Atlas EC counties join to the ACS and land area.
- All 18,980 EC ZIPs join.
- ACS population equals the Atlas `pop2018` (median deviation 0).
- The identity ec_grp/exposure = 1 − bias holds to 2×10⁻⁵.
- 3,089 counties have an Opportunity Atlas record and 3,057 have BEA data.
- The population-weighted Hispanic share is 0.178.

Rerunning twice gives byte-identical `derived/*.csv` [CALCULATION: sha256 of two consecutive
runs compared, 2026-09-28].

## 4. H1: connectedness and Hispanic share (tests 1–2)

County, with controls, per 10 points of Hispanic share [CALCULATION: `derived/h1_county.csv`]:

| Measure | Unweighted | SD units | Weighted | Reading |
|---|---|---|---|---|
| EC (adults) | −0.027 (0.006) | −0.15 | −0.019 (0.005) | holds; leave-one-state-out range −0.039 to −0.025 (unw), −0.023 to −0.015 (w), all p<0.002 |
| EC, Mexican share / non-Mexican Hispanic | −0.028 (0.008) / −0.022 (0.010) | −0.16 / −0.12 | −0.025 (0.008) / −0.009 (0.008) | Mexican share carries it |
| Childhood EC (high-school friends) | −0.010 (0.002) | −0.04 | −0.006 (0.006) | small; null weighted (MDE 0.018) |
| EC of high-SES people | −0.010 (0.003) | −0.06 | −0.012 (0.009) | small |
| Clustering | −0.0006 (0.0006) | −0.03 | −0.0021 (0.0006) | null unweighted; −0.12 SD weighted |
| Support ratio | −0.0002 (0.0004) | −0.01 | −0.0016 (0.0009) | null (MDE ≈ 0.001–0.003) |
| Volunteering rate | −0.0072 (0.0005) | −0.21 | −0.0060 (0.0004) | lower |
| Civic organizations per 1,000 users | −0.0012 (0.0002) | −0.12 | −0.0006 (0.0002) | lower |

At ZIP level with controls, EC is lower by 0.033 (0.004) with state FE and by 0.044 (0.003)
between ZIPs in the same county (−0.20 SD). Clustering falls by 0.001, or −0.05 SD, and the support
ratio is null [CALCULATION: `derived/h1_zip.csv`].

**Decomposition.** ln EC_grp = ln exposure + ln(1 − bias) exactly, so the slope on Hispanic share
splits additively [CALCULATION: `derived/decomposition.csv`]:

| Arm (controls) | Exposure share | Friending-bias share |
|---|---|---|
| County, unweighted | 0.50 | 0.50 |
| County, weighted | 0.79 | 0.21 (bias not significant, p=0.34) |
| ZIP, state FE, unweighted / weighted | 0.69 / 0.89 | 0.31 / 0.11 |
| ZIP, within county, unweighted / weighted | 0.73 / 0.80 | 0.27 / 0.20 |
| Childhood (high school), county, unweighted / weighted | 0.51 / 0.46 | 0.49 / 0.54 |

In the population-weighted arms, exposure is the larger part: fewer high-SES people in the groups
where low-SES people make friends. The parent predicted this.

**What H1 does and does not show [INFERENCE].** EC averages over all low-SES residents, Hispanic
ones included, and SES is ranked nationally. A county with more low-income Hispanic residents
therefore has lower exposure mechanically. Its EC also falls if Hispanic low-SES users have fewer
high-SES friends than other low-SES users, even when nobody else's ties change. The Atlas's public
files carry no race-specific EC, so county and ZIP means cannot separate that composition from a
spillover onto other residents' ties, and only the spillover is the operator's fragmentation claim.
The cohesion measures, which describe the tie structure itself, move little. Clustering is null
unweighted, −0.05 SD at ZIP level and −0.12 SD weighted at county level. The support ratio is null.
Volunteering and civic-page counts are lower. Both rest on classifiers of Facebook group and page
titles, and the codebook does not say whether Spanish-language groups are classified as reliably;
the sign may be partly a measurement artifact [INFERENCE; SOURCE: codebook §2.1].

## 5. H2: does connectedness scale output? (test 3)

The outcomes are:
- Opportunity Atlas p25 child income rank, pooled and white (1978–83 cohorts);
- BEA 2018 per-capita personal income;
- BEA 2018 place-of-work earnings per resident;
- ACS 2014–2018 non-Hispanic white median household income.

Predictors are standardized (county SD), and the controls are Hispanic share, Black share, BA+ share
and log density, with state FE [CALCULATION: `derived/bridge_county.csv`, spec `base`].

**Level (EC, per SD):**

| Outcome | Unweighted | Weighted |
|---|---|---|
| Pooled mobility (rank) | +0.033 (0.003), 0.55 SD | +0.027 (0.002), 0.64 SD |
| White children's mobility | +0.020 (0.002), 0.36 SD | +0.018 (0.004), 0.43 SD |
| NH white median household income | +11.1% (2.1) | +8.9% (1.5) |
| Per-capita personal income | +5.9% (0.9) | −0.8% (2.6) |
| Place-of-work earnings per resident | −1.8% (1.8) | −14% (6.3) |

The mobility links survive adding income and poverty controls: pooled +0.028 unweighted and
+0.021 weighted; white +0.015 and +0.013. Childhood EC is weaker and turns negative weighted for
white mobility (−0.011, se 0.003). Clustering's level link is mixed in sign across weights.

**Scale interaction (predictor × centered ln population).** Across 40 cells (4 predictors × 5
outcomes × 2 weights), 1 is positive at p<0.05, 16 are negative and 23 are null. The one positive
cell is EC × ln pop for NH white income, unweighted: +1.25% per SD per log point (se 0.37). Weighted
it is +0.15% (se 0.38, MDE 1.1%). For pooled mobility the EC interaction is −0.0025 (0.0006)
unweighted and −0.0003 (0.0011) weighted, with MDE 0.003 rank points per SD per log point: the
design would have caught an interaction a tenth the size of the level effect. The support-ratio
interaction is negative in 7 of 10 cells. **H2 fails** as a scale claim; connectedness predicts
outcomes about equally in small and large counties, or more strongly in small ones [CALCULATION:
`derived/verdict.csv`].

**Direct fragmentation × size check.** Fractionalization × ln pop is positive for pooled mobility
(+0.028, se 0.005 unweighted; +0.025, se 0.006 weighted), for white mobility and for per-capita
income (+0.042 and +0.106). More fractionalized large counties do better than more fractionalized
small counties, the opposite of the operator's prediction. This is the cosmopolitan-metro pattern
and confounded; it rules out neither sign causally [CALCULATION: `bridge_county.csv`,
`frac_scale_interaction`; INFERENCE].

## 6. Step 4: sizing

Step 4 was not run. The brief says to stop if either hypothesis fails, and H2 failed. For scale
only, H1's own coefficient implies the following. Moving a county's Hispanic share by 10 points
moves EC by 0.019–0.027, or 0.11–0.15 SD. The level link then predicts child mobility at
0.02–0.03 rank per SD of EC, which is 0.0021–0.0050 rank points per 10 points of share
[CALCULATION: products of the §4 and §5 coefficients].

That chain is a product of two cross-sectional slopes. It includes the composition term, which
changes no other resident's ties, and it is not a causal or dollar estimate. Turning it into $bn
would state a precision the design does not have [INFERENCE].

## 7. Limits

- The Atlas measures class connectedness, not ethnic connectedness. The operator's "less
  fragmentation" has no direct measure here; fractionalization is the closest regressor.
- The sample is Facebook users aged 25–44 with ≥100 US friends. People whose networks are abroad
  or offline, disproportionately recent immigrants, are excluded, so EC describes the more
  integrated slice.
- The design is cross-sectional with state FE only. No instrument and no panel: the Atlas is a
  single 2022 snapshot.
- Mobility outcomes are for 1978–83 birth cohorts and predate the EC snapshot. Adult EC is where
  people live now; childhood EC is by high-school county.
- No patents: no primary county series was local or cheaply fetchable (§2).
- Dataset register not updated (worker scope); the §2 rows carry what an entry needs.
