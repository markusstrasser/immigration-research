**Verdict:** In the 2025 CPS ASEC, households headed by the US-born children of immigrants (second generation) use at least one means-tested program at **34.6%**, against **29.4%** for households headed by natives with two US-born parents (third-plus generation) and **44.9%** for immigrant-headed households. Almost all of the second generation's 5-point excess is composition: second-generation heads are younger, more often have children, and are 40% Hispanic. Age-standardised to the third-plus age distribution the gap is 1.5 points (30.9 vs 29.4), and within the white and Black groups the second generation uses *less* than the third-plus (non-Hispanic white 20.9 vs 24.3); Asian cells are too small to call. Cash assistance is lowest in the second generation (3.8% vs 4.8%). The 2024 ASEC gives the same picture. A true "third generation" cannot be isolated in any US survey; third-plus pools everyone from grandchildren of immigrants to colonial descent.

# Welfare use by immigrant generation: second and third-plus generation vs the foreign-born (CPS ASEC 2024–2025)

## 1. Question, data, definitions

The question was how much the second and third generations use welfare compared with natives of native parentage. Only the CPS ASEC carries parents' birthplace (`PEFNTVTY`, `PEMNTVTY`) alongside program receipt, so the answer comes from the 2025 and 2024 ASEC person files pulled from the Census microdata API (`api.census.gov/data/<year>/cps/asec/mar`, 142,125 and 144,265 interviewed persons; 55,762 and 56,251 households). [SOURCE: pull and analysis in `../infra/immigration-fiscal/cps_generation_welfare_2026_09_16/`, raw JSON on the SSD data root under `external/cps/asec/`, pulled 2026-09-16]

- **Generation of a person.** First = foreign-born (`PRCITSHP` 4 or 5). Second = native-born with at least one parent born outside the US and its territories. Third-plus = native-born with both parents born in the US or a territory. Puerto Rico and the island areas count as US. The CPS has no grandparents' birthplace, so third-plus is everything from the third generation onward; the CIS report on the same question makes the same caveat (footnote 30). [SOURCE: https://api.census.gov/data/2025/cps/asec/mar/variables.json; https://cis.org/Report/Welfare-Use-Immigrants-and-USBorn-2024]
- **Household generation** = the reference person's, the unit CIS uses. Interviewed households only; household weight of the reference person.
- **"Any welfare"** follows the CIS program list so the numbers are comparable to the ones circulating: any member on SNAP, SSI, cash assistance (TANF or general assistance), WIC, free or reduced-price school lunch, Medicaid in the prior year, public or subsidised housing, or a Census-simulated EITC above zero. Also shown without the EITC, and cash only (SSI or TANF/GA). [FRAMING-SENSITIVE: the list counts a child's Medicaid or school lunch as the household "on welfare"; the tweet-era 1970 figure counted cash only.]

## 2. Results, 2025 ASEC (calendar-2024 receipt)

Percent of households with any member using the program, by generation of the reference person. The 2024 ASEC column is the same "any" rate a year earlier.

| Program | Gen 1 (foreign-born) | Gen 2 | Gen 3+ ("bio Americans") |
|---|---|---|---|
| Any program, CIS list | **44.9** | **34.6** | **29.4** |
| Any program, 2024 ASEC | 46.0 | 34.9 | 29.3 |
| Any excluding EITC | 39.6 | 31.4 | 26.7 |
| Medicaid (prior year) | 25.6 | 20.3 | 16.8 |
| EITC (simulated) | 20.7 | 13.3 | 9.5 |
| Free/reduced school lunch | 19.3 | 13.8 | 9.7 |
| SNAP | 12.1 | 9.5 | 9.9 |
| Cash: SSI or TANF/GA | 4.3 | 3.8 | 4.8 |
| Housing assistance | 5.4 | 4.2 | 4.9 |
| WIC | 3.2 | 2.8 | 1.9 |
| Households (unweighted) | 9,471 | 4,939 | 41,352 |
| Weighted share of all households | 17.0% | 8.9% | 74.1% |

Within the first generation: naturalised-citizen heads 39.9%, non-citizen heads 51.2%.

**Age-standardised** (direct standardisation to the third-plus head-age distribution in five bands): any program 43.0 / 30.9 / 29.4; cash 4.7 / 4.3 / 4.8; Medicaid 24.5 / 17.9 / 16.8. The 2024 ASEC gives 44.0 / 31.1 / 29.3. [SOURCE: `result_2025.txt`, `result_2024.txt` in the infra directory above]

**By head age group** (any program, gen 1 / gen 2 / gen 3+): under 35: 43.7 / 43.0 / 34.8; 35–64: 48.6 / 35.9 / 34.4; 65 and over: 34.7 / 17.4 / 18.5. The second generation's excess is entirely among young heads and reverses after 65.

**Households with children** (any program): 67.7 / 59.9 / 56.3; free/reduced lunch 48.6 / 42.0 / 37.7; cash 3.9 / 4.7 / 5.2. **Heads with high school or less:** 61.2 / 52.6 / 41.8.

**Persons aged 25–64, own receipt** (person weight; gen 1 / gen 2 / gen 3+): SSI 0.9 / 1.9 / 2.6; TANF or GA 0.6 / 0.6 / 0.8; Medicaid 16.3 / 14.6 / 13.3; EITC 13.3 / 9.9 / 8.2; lives in a SNAP household 10.3 / 9.3 / 9.9. Adult second-generation individuals draw less cash and slightly more Medicaid and EITC than third-plus adults.

## 3. Composition, not generation

Second-generation reference persons are 39.6% Hispanic, 37.0% non-Hispanic white, 13.2% Asian and 5.8% Black; third-plus reference persons are 76.2% non-Hispanic white, 14.2% Black and 6.4% Hispanic. Mean head age is 46.1 vs 53.6, and 31.6% vs 24.7% of households have children. Second-generation heads are *better* educated than third-plus heads (27.4% vs 31.7% with high school or less), so education does not explain the raw excess.

Any-program rate by ethnicity of the reference person, 2025 (households; 2024 values in brackets):

| Ethnicity | Gen 2 | Gen 3+ | Gen 2 minus gen 3+ |
|---|---|---|---|
| Hispanic | 48.4 [49.0] (n 2,154) | 43.5 [43.5] (n 3,156) | +4.9 |
| Non-Hispanic white | 20.9 [22.7] (n 1,637) | 24.3 [24.5] (n 30,567) | −3.4 |
| Non-Hispanic Asian | 29.4 [29.8] (n 690) | 29.6 [21.9] (n 329) | −0.2 (2024: +7.9) |
| Non-Hispanic Black | 41.6 [37.7] (n 235) | 46.9 [47.0] (n 5,833) | −5.3 |

Ethnic differentials are three to five times the generational ones: white third-plus 24, Hispanic 44–49, Black 42–47, Asian 22–30 on small third-plus cells. The second generation converges on the rate of its own ethnic group in the third-plus, and lands below it for whites and Blacks; the Asian comparison flips sign between years and is not called. The Hispanic second generation's 5-point excess over Hispanic third-plus is concentrated in heads under 35 (53.3 vs 43.4), that is in young families with children; among non-Hispanic white heads under 35 the second generation is lower (24.9 vs 27.7). [INFERENCE from the tables above; no regression adjustment was run]

Reading against the CIS SIPP-based figures the tweet drew on: the CPS immigrant–native gap is 15.0 points (44.9 vs 29.9 for all US-born households) against 15.4 in the 2024 SIPP (52.7 vs 37.3), so the two surveys agree on the gap while the CPS sits about 8 points lower on levels. [SOURCE: CIS 2024 report above; `result_2025.txt`]

## 4. What "third generation" can and cannot mean

No US survey identifies grandparents' birthplace, so a third generation defined by ancestry does not exist as a measured group; CIS's Table 16 pools "third generation and beyond" for the same reason. The closest proxy for the third generation of the post-1965 wave is third-plus Hispanic households (43.5%). That proxy is biased upward as a measure of all descendants, because the most assimilated descendants stop reporting Hispanic origin and drop out of the measured group (ethnic attrition; Duncan & Trejo [TRAINING-DATA, not re-verified this session]). The same selection affects the Mexican-origin incarceration comparator in `immigration-mexican-origin-generation-incarceration-2026-09-16.md`.

## 5. Disconfirmation and limits

- **CPS under-reports program receipt** relative to SIPP and administrative counts, most for SNAP, TANF and Medicaid (Meyer, Mok & Sullivan 2015 [TRAINING-DATA]). That lowers every level here by roughly a quarter and could change the generational *gaps* if under-reporting differs by generation; there is no evidence either way in this session. The SIPP would be the check, and its public file carries parental nativity only for the SIPP-based CIS Table 16, which was not obtainable (cis.org returns 403; the Excel tables were not retrieved).
- **EITC is simulated** by the Census from tax-unit income, not reported; the "any excluding EITC" row is the reported-receipt measure.
- **No standard errors.** Cells above about 500 households are stable across the two years to within a point; the second-generation Black (n 235) cell moved 4 points between years and the third-plus Asian cell (n 329 and 363) moved 8 (29.6 vs 21.9); read those as ±5 and ±8.
- **Household-head unit.** Rates by generation of the head assign a mixed household to one generation; second-generation heads with foreign-born spouses and immigrant heads with second-generation children are both common. Person-level rates for adults 25–64 (section 2) do not depend on this and show the same ordering.
- **Not tested:** any adjustment beyond age and ethnicity (state of residence, family structure, income); a regression would tighten the composition claim but was outside the question.

## 6. Bearing on the circulating numbers

The tweet's series (6% in 1970, 59% and 61% today) compares 1970 cash assistance among all immigrant households with any-program use among illegal-immigrant-headed households; see the fiscal-impact and CIS-audit memos for the 59.4% claim's grading. The generational result adds: the immigrant excess does not compound across generations. It is 15 points in the first generation, 1.5 points after age adjustment in the second, negative for the second generation within the white and Black groups, and the cash-assistance excess is zero or negative from the first generation on (gen 1 4.3, gen 2 3.8, gen 3+ 4.8). The persistent element is ethnic, not generational, and it is already visible in third-plus natives.

## 7. Sources and provenance

- CPS ASEC 2025 and 2024 person microdata, Census Bureau microdata API, pulled 2026-09-16 with `pull_cps_asec.sh` (36 person variables plus a 14-variable supplement joined on household and person sequence). Raw files are read-only on the SSD data root; not in the repo.
- Variable universe and codes: https://api.census.gov/data/2025/cps/asec/mar/variables.json (PRCITSHP, PENATVTY, PEFNTVTY, PEMNTVTY, PERRP, HFOODSP, SSI_YN, PAW_YN, WICYN, HFLUNCH, CAID, HPUBLIC, HLORENT, EIT_CRED, HSUP_WGT, MARSUPWT).
- CIS, *Welfare Use by Immigrants and the U.S.-Born, 2024* (2024 SIPP): 52.7% immigrant-headed vs 37.3% US-born; Table 16 "welfare use by race and generation" with footnote 30 on third-plus pooling. https://cis.org/Report/Welfare-Use-Immigrants-and-USBorn-2024
- Borjas & Trejo 1991, NBER w3423, Table 1: 1970 census cash public-assistance receipt 5.9% immigrant vs 6.1% native households. https://www.nber.org/papers/w3423
- Repo: `immigration-sipp-2024-benefits-2026-09-05.md` (per-adult allocated SNAP/TANF/SSI, foreign-born vs native), `immigration-fiscal-camarota-cis-testimony-audit.md` (grading of the 59.4% claim).

**Instrument note.** The tables are mechanical tabulations of public microdata; the interpretation in sections 3 and 6 (composition over generation) is this model's reading and is the part an LLM's dispositions on immigration could colour (`notes/llm-bias-caveat.md`). The falsifier is a SIPP or regression-adjusted CPS estimate showing a second-generation excess that survives age and ethnicity controls.
