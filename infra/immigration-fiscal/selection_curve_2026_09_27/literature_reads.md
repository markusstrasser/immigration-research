claude-opus-5-5

**Verdict:** Across origin groups, the published G1→G2 carry-over of group means is about 0.4–0.6 on schooling and log wages (Borjas 1993 Table 4: 0.45, 0.36 without Mexico; Card–DiNardo–Estes 2000 Table 7: schooling 0.41–0.43, sons' wages 0.44–0.62). The published G2→G3 figure is about 0.45–0.55 (Borjas 1994 GSS Table 8: wages 0.46, schooling 0.53; Borjas 1992 Table V: 0.47–0.55), so the rule is roughly half the gap per generation, about a quarter by G3 (Borjas 1994 G1→G3 wages 0.20–0.27). Ward 2020, on linked 1880–1910–1940 occupational scores, is the high outlier (G1→G2 about 1.0, G2→G3 0.57–0.74, G1→G3 about 0.5), and his estimate halves under an alternative occupation-income scoring. The individual rank-rank slopes (ABJP about 0.25–0.3) and the ethnic-capital coefficients (about 0.2–0.3) measure different things; do not use them as the group slope. Every source except ABJP and Feliciano–Lanuza was read from a working paper or an appendix, not the journal print (see [GAP]s).

# Literature reads: generational carry-over of origin-group position (G1→G2, G2→G3)

Lane: literature for selection_curve_2026_09_27. Date 2026-09-27. Source tags per repo CLAUDE.md.
Numbers are quoted from the papers' own tables unless tagged [UNVERIFIED].

## Findings


### Repo reuse (checked first)

- Feliciano & Lanuza 2017 was already read in full on 2026-09-16 (corpus `doi_10_1177_0003122416684777`); its coefficients are in `research/immigration-secgen-origin-divergence-mechanisms-2026-09-16.md` "Verified block 1". Re-verified below against the same corpus text.
- Opportunity Insights origin tables (Chetty-Hendren-Jones-Porter 2020, son rank by parent ventile by origin) were tabulated in `infra/immigration-fiscal/oi_origin_regression_2026_09_16/RESULT.md`: every origin's parent-child slope is flatter than the US-born (0.7-1.4 pctile per ventile vs 1.65), i.e. individual regression toward an origin mean. G2 only.
- Ladder 75 (`research/immigration-confidence-ladder.md`): 29 parental origins, CPS, G2 BA share on a Feliciano-style selectivity index, slope 0.81, R² 0.91 (repo's own computation, not a published slope).
- Borjas 1992/1993/1994, Card-DiNardo-Estes 2000 and ABJP 2021 had no table-level reads in the repo (ABJP was read for its sample rule only, `study_audit_2026_09_23/C_children_status.md` §6).

### 1. Borjas (1994), "Long-Run Convergence of Ethnic Skill Differentials: The Children and Grandchildren of the Great Migration," ILRR 47(4):553-573

Read from NBER Working Paper w4641 (1994, 43 pp.), full text via pdftotext [SOURCE: https://www.nber.org/system/files/working_papers/w4641/w4641.pdf]. Page numbers below are the WP's printed page numbers; the ILRR pagination was not available (fetch_paper by DOI 10.1177/001979399404700403 failed). The WP tables may differ in detail from the published ILRR tables [GAP].

Design. Unit: individual second-generation (1940 Census, native-born men with foreign-born fathers, 25-64, N = 11,079) or third-generation proxies (1980 Census, first-reported ancestry, N = 251,658) regressed on their ethnic group's 1910 first-generation mean (literacy rate or adjusted log wage), random-effects estimator with a group error. So the coefficient is an **origin-group-mean → group-mean** slope estimated on micro data ("the coefficient gamma is the intergenerational transmission coefficient", WP p.11); 32 ethnic groups.

**Table 5 (WP p.12), G1 1910 → G2 1940, no education control unless noted:**
- Education (years) on 1910 literacy rate: "5.1176*" "(.9597)". Text: "a 20 percentage point difference in literacy rates among two immigrant groups in 1910 translated to a difference of about one year of schooling for their children" (p.11).
- Occupational log wage on 1910 log wage: ".6018*" "(.1374)"; with 1940 education control ".2260" "(.0872)".
- Reported log wage on 1910 log wage: ".6724*" "(.1942)"; with education control ".2689" "(.1516)".
- Text: "The intergenerational transmission coefficient is in the order of .6" (p.11).

**Table 6 (WP p.15), G1 1910 → G3 proxy 1980 (a two-generation link, not G2→G3):**
- Education on literacy: "2.4202*" "(.7926)".
- Occupational log wage: ".2006*" "(.0469)"; with education ".0686*" "(.0156)".
- Reported log wage: ".2684" "(.0867)"; with education ".0673" "(.0442)".
- Implied G2→G3 education correlation, Borjas's own ratio of Table 6 to Table 5 row 1: "The implied correlation is .47" (p.14).
- Borjas: "Table 5 estimates [gamma] to be between .6 to .7, while Table 6 estimates [theta] to be between .2 and .3 ... I cannot reject the hypothesis that [gamma]^2 = [theta]. The t-statistic associated with this test equals .72" (p.15).
- [CALCULATION: ratios of the quoted coefficients] implied G2→G3 wage link = .2006/.6018 = 0.33 (occupational), .2684/.6724 = 0.40 (reported). Not printed by Borjas as such.

**Table 8 (WP p.20), GSS third generation with grandparent birthplace (N = 2,197 education, 1,970 log wage), random effects; true G2→G3 with the parent observed:**
- Education, row 1: parental education ".2571*" "(.0147)"; mean education in parent's generation (ethnic capital) ".2669*" "(.1277)". Sum = mean convergence G2→G3 education; text: "Row 1 estimates the rate of mean convergence in educational attainment to be .53" (p.21).
- Education, row 2: 1910 literacy rate alone "2.5280" "(1.7837)" (n.s.); row 3 with parental education: literacy "1.5195" "(1.3678)", parent ".2589*" "(.0147)".
- Log wage, row 1: parental log wage ".1630*" "(.0198)"; mean log wage in parent's generation ".2945*" "(.1274)". Text: "The sum of the two coefficients, which estimates the rate of mean-convergence between the second and third generations, is approximately .46" (p.21).
- Log wage, row 2: mean log wage of 1910 immigrants (G1→G3 direct) ".2155*" "(.1083)"; text: "Because this statistic is approximately the square of .46, the results suggest that the intergenerational transmission coefficient is relatively the same across any two generations" (p.21).
- Row 3: 1910 mean ".1202" "(.0997)" with parent ".1667*" "(.0197)"; implied G1→G2 mean convergence "approximately .41 (or the ratio .1202/.2945)" (p.21).
- Conclusion: "the coefficient measuring mean convergence in the log wages of ethnic groups is in the order of .4 to .5, and is relatively constant across generations" (p.21); "it might take four generations, or roughly 100 years" (p.22).

Reading. Two numbers for G1→G2 on wages: 0.60-0.67 (Census, Table 5) and ~0.41 (GSS, implied). G2→G3: 0.46 wages, 0.53 education (GSS, direct), 0.33-0.40 wages implied from Census. G1→G3 direct: 0.20-0.27 wages. These are European-dominated 1910 origins (Mexico is one of 32 groups; GSS Mexico N = 89). [GAP] published ILRR table/page numbers not checked.

### 2a. Borjas (1993), "The Intergenerational Mobility of Immigrants," JOLE 11(1):113-135

Read from NBER WP w3972 (1992, 38 pp.), pdftotext [SOURCE: https://www.nber.org/system/files/working_papers/w3972/w3972.pdf]; DOI 10.1086/298319 fetch failed. WP page numbers.

Design. Unit: **origin-group means**, OLS across national-origin groups (N = 23; 21-22 in some rows): relative log earnings (vs third+ generation) of second-generation men in the 1970 Census on the relative earnings of immigrant men from the same country in the 1940 Census (equation 9, WP p.13-14). Pseudo-cohort intercensal link, not parent-child pairs.

**Table 4 (WP p.14), "Relationship Between the Earnings of the First- and Second-Generations", t-ratios in parentheses (not SEs):**
- Row 1, unadjusted: intercept ".0695" "(4.19)", slope on z1(1940) ".4465" "(6.85)", R² ".691", n 23. [CALCULATION] SE ≈ .4465/6.85 = .065.
- Row 2, omits Mexico: ".3627" "(2.06)", R² ".176", n 22.
- Row 3, adjusted wage (education, age, marital status, metro held constant in G1): ".2696" "(5.10)".
- Row 4, young sample 25-44: ".4967" "(8.91)"; row 5, older 45-64: ".3785" "(4.34)".
- Rows 6-7 adjusted + age split: ".2334" "(4.90)", ".2433" "(2.94)".
- Rows 8-13 add 1970 immigrants' earnings: G1 1940 slope stays .20-.58, 1970 immigrant coefficient never significant.
- Text: "the estimate of the coefficient δ in equation (9) is .45 ... even after three generations, the earnings of third-generation ethnic groups depend on the earnings of their immigrant grandparents" (WP p.15); about 7 percent common G1→G2 uplift (intercept).

Reading. G1→G2 log-earnings group slope 0.45 (0.36 without Mexico; 0.27 on education-adjusted wages). Mexico is influential: dropping it cuts the slope by a fifth and R² from .69 to .18.

### 2b. Borjas (1992), "Ethnic Capital and Intergenerational Mobility," QJE 107(1):123-150

Read from the research corpus (`/Users/alien/Projects/corpus/doi_10_2307_2118325/`, JSTOR PDF parsed by Marker; it was already in the corpus; `fetch_paper` for this DOI now errors on a missing paper.pdf). The parse carries no journal page numbers, so page cites below are [GAP]; tables are cited by number.

Design. Unit: **individual parent-child** regressions (GSS, NLSY79), with "ethnic capital" = mean of the characteristic in the ethnic group in the father's generation; random-effects GLS. The sum parental + ethnic-capital coefficients = rate at which a group mean carries across one generation (Borjas: "the intergenerational transmission parameter describing how the mean educational attainment of the ethnic group changes over time is the sum of the coefficients of parental and ethnic capital, which in the education regression for the GSS is 0.48").

**Table III (all generations pooled):**
- GSS education (N = 6,756), col. (3): parental "0.2501" "(0.0076)", ethnic capital "0.2265" "(0.0466)"; col. (4) with X: "0.2586" "(0.0080)", "0.1455" "(0.0882)". Col. (1) parental only "0.2664".
- GSS occupational prestige (N = 7,066), col. (3): parental "0.1829" "(0.0128)", ethnic "0.4589" "(0.2244)".
- NLSY education (N = 5,619), col. (3): "0.2570" "(0.0075)", ethnic "0.1165" "(0.0630)".
- NLSY log wage (N = 3,734), col. (3): parental "0.3257" "(0.0291)", ethnic "0.2843" "(0.0955)"; col. (4): "0.2983" "(0.0284)", "0.2983" "(0.0967)".
- Text sums: "the NLSY data yield a transmission coefficient of 0.37 for educational attainment and 0.61 for log wages. The respective statistics in the GSS are 0.48 and 0.63" (GSS 0.63 is occupation).
- Borjas cites his 1940→1970 Census group estimate: "the Census estimate of γ1 + γ2 was 0.45" (= Borjas 1993 Table 4 row 1).

**Table V, by generation (random effects; "second generation" = children of immigrants, i.e. the G1→G2 link; "third generation" = natives with US-born parents, i.e. G2+→G3+):**
- GSS education, no X: G2 parental "0.1741" "(0.0225)", ethnic "0.2267" "(0.1079)" (N 796); G3+ parental "0.2620" "(0.0080)", ethnic "0.2071" "(0.1099)" (N 5,960). [CALCULATION] sums 0.40 (G1→G2) and 0.47 (G2→G3+).
- GSS occupation, no X: G2 "0.1637" "(0.0346)", ethnic "0.7807" "(0.0559)"; G3+ "0.1843" "(0.0137)", "0.3008" "(0.4049)". Sums 0.94 and 0.49.
- NLSY education, no X: G2 "0.1020" "(0.0223)", ethnic "0.0681" "(0.0970)"; G3+ "0.2836" "(0.0080)", "0.1340" "(0.0589)". Sums 0.17 and 0.42.
- NLSY log wage, no X: G2 "0.2162" "(0.0844)", ethnic "0.7017" "(0.2255)" (N 346); G3+ "0.3385" "(0.0310)", "0.2078" "(0.1054)" (N 3,388). Sums 0.92 and 0.55.
- With X: GSS educ G2 0.1538/0.2568, G3+ 0.2744/0.1983; NLSY log wage G2 0.2675/0.4188, G3+ 0.3048/0.1152.
- Table IV (drops Mexicans and Puerto Ricans): "In the GSS the intergenerational transmission coefficient ... is 0.52 for education and 0.62 for occupation. In the NLSY it is 0.50 for education and 0.53 for wages."

Reading. The ethnic-capital coefficient itself is ~0.2 on education and 0.2-0.3 on log wages pooled; the G2 samples are small (346-947) and the G2 ethnic-capital coefficients have SEs of 0.06-0.23. On wages the G1→G2 group carry is larger (0.9 NLSY) than G2→G3 (0.55), on education smaller (0.17-0.40 vs 0.42-0.47). Noisy; do not read the difference as established.

### 4. Abramitzky, Boustan, Jácome & Pérez (2021), "Intergenerational Mobility of Immigrants in the United States over Two Centuries," AER 111(2):580-608

Read from the published AER PDF hosted by Jácome [SOURCE: https://elisajacome.github.io/Jacome/ImmigrantMobility_AER.pdf, header "American Economic Review 2021, 111(2): 580–608, https://doi.org/10.1257/aer.20191586"], pdftotext, journal page numbers. `fetch_paper` by DOI failed; NBER w26408 also downloaded.

Design. Unit: **individual father-son pairs**, son's national income rank on father's rank (equation 2, p.590), with intercept and slope shifts for sons of immigrants. Links G1 father → G2 son only; no G3.

**Table 1 (p.592), "Intergenerational Mobility Estimates, by Cohort", SE in brackets:**
- 1880-1910 cohort: α "30.98" "[0.06]", β0 immigrant father "8.39" "[0.12]", β1 father's rank "0.36" "[0.00]", β2 immigrant × rank "−0.08" "[0.00]".
- 1910-1940: "31.01", "6.75", "0.36", "−0.04".
- GSS cohort: "35.42" "[1.17]", "6.76" "[3.06]", "0.29" "[0.02]", "−0.09" "[0.06]".
- Opportunity Insights cohort: "36.64" "[0.40]", "7.42" "[0.60]", "0.33" "[0.01]", "−0.08" "[0.01]".
- So the within-group rank-rank slope for sons of immigrants is 0.21-0.32 (Figure 2 legends, p.591: immigrant father "Slope: 0.27", "0.32", "0.21", "0.25") against 0.29-0.36 for sons of US-born.
- Expected son rank at father p25: sons of immigrants about 5-6 percentiles above sons of US-born (p.592); by origin in Figure 3 (graph only; numbers in online Appendix Table A4, not read [GAP]). Exceptions below the US-born line: "Norway and Belgium in 1880; Norway in 1910; and Haiti, Trinidad and Tobago, and Jamaica in the modern cohort" (p.592).
- Origin-group-mean carry-over is shown only graphically (Figure 1, first- vs second-generation log-earnings gaps by origin, p.589) with no fitted slope printed. Text: "it is still the case that the children of low-earning immigrants tend to earn less than the children of high-earning immigrants, consistent with the persistence results in Abramitzky, Boustan, and Eriksson (2014) and Ward (2020)" (p.590); gaps stay above 5 log points in G2 for "Norwegians in 1910 and 1940; Finns in 1940; and Jamaicans, Haitians, and Mexicans in the modern data" (p.590).

Reading. ABJP is an individual-level mobility paper. The rank-rank slope (0.2-0.3) is NOT the group-mean carry-over; with origin-specific intercepts it implies strong regression toward an origin-specific mean, which is the Borjas ethnic-capital pattern (repo's OI table: `oi_origin_regression_2026_09_16`). ABJP print no cross-origin G1→G2 slope. [GAP] A cross-origin slope could be computed from Appendix Table A4 (origin intercepts and slopes) plus Figure 1's gaps; not done here. Pointer: Ward (2020) AEJ:Applied, "The Not-So-Hot Melting Pot", is the grandfather-linked G3 persistence paper ABJP cite (reads below if reached).

### 3. Card, DiNardo & Estes (2000), "The More Things Change: Immigrants and the Children of Immigrants in the 1940s, the 1970s, and the 1990s," in Borjas (ed.), *Issues in the Economics of Immigration* (NBER/Chicago)

Read from NBER WP 6519 (1998), a scanned PDF with no text layer; OCR'd locally with tesseract at 200 dpi [SOURCE: https://www.nber.org/system/files/working_papers/w6519/w6519.pdf; OCR text at scratchpad `lit/w6519_ocr.txt`]. Table 7 sits on PDF page 57 of 62 (tables appended, no printed page number); discussion on WP pp. 23-35. The book-chapter pagination was not read [GAP]; OCR digits were checked against the text's own summary ("range from 0.41 to 0.47" education; "0.21 to 0.62" wages), which they match.

Design. Unit: **origin-group means**, WLS weighted by the number of G2 sons and daughters; immigrant men's age-40 predicted education or log weekly wage by country in 1940 (or 1970) → G2 sons'/daughters' age-40 predicted outcome by father's country in 1970 (or 1994-96 CPS). 34 origin groups (1940-70), 33 (1970-95). Following Borjas (1993). Authors note the grouped estimator absorbs any ethnic-capital effect (it estimates b + d) and removes attenuation (WP pp. 26-27).

**Table 7 (PDF p.57), "Relationship Between Education and Earnings of Immigrant Fathers and Education and Earnings of Second Generation Sons and Daughters", SE in parentheses:**
- Panel A, 1940→1970: sons' education on fathers' mean education "0.41" "(0.10)", R² 0.35; sons' log wage on fathers' mean log wage "0.44" "(0.05)", R² 0.72; daughters' education "0.47" "(0.08)"; daughters' log wage "0.21" "(0.06)".
- Panel B, 1970→1995: sons' education "0.43" "(0.05)", R² 0.68; sons' log wage "0.62" "(0.12)", R² 0.45; daughters' education "0.42" "(0.04)"; daughters' log wage "0.50" "(0.13)".
- Cross links: sons' education on fathers' log wage "4.74" "(0.68)" (1940-70), "4.50" "(0.72)" (1970-95); sons' log wage on fathers' education "0.03" "(0.01)", "0.06" "(0.01)".
- **Table 8** (both father measures): in 1970-95 only fathers' education matters, sons' education "0.36" "(0.10)", fathers' log wage "0.94" "(1.19)"; in 1940-70 the wage dominates (sons' education on father wage "4.08" "(0.86)", education "0.12" "(0.10)").
- Text: "Using education as the outcome measure for fathers and children the estimates of the intergenerational coefficient b in equation 1 are very stable, with a range from 0.41 to 0.47. Using wages as the outcome measure the estimates of b are more variable, ranging from 0.21 to 0.62" (WP p.29). Benchmark: GSS individual father→child education 0.318 (0.005), reliability-corrected "0.40 (= 0.318/.80)" (WP pp.34-35), i.e. the G1→G2 group slope on education equals an ordinary father-child coefficient.
- Also: "native children earn 15-20 percent less than one would expect, given their fathers' earnings and the patterns for second generation children", and 0.8-1.4 fewer years of schooling (WP p.30): the G2 line has a positive intercept shift over natives.

Reading. G1→G2 group-mean slope, sons: education 0.41-0.43, log wage 0.44 (1940-70) and 0.62 (1970-95). No G3.

### 5a. Feliciano & Lanuza (2017), "An Immigrant Paradox? Contextual Attainment and Intergenerational Educational Mobility," ASR 82(1):211-241, DOI 10.1177/0003122416684777

Re-read from the corpus PDF (`/Users/alien/Projects/corpus/doi_10_1177_0003122416684777/paper.pdf`, pdftotext), journal pages. Add Health W1→W4, N = 9,285; "contextual attainment" = parent's percentile in the same-age, same-sex schooling distribution of the birth country (Barro-Lee based; Ichou 2014 definition); the higher of the two parents.

**Table 3 (p.226-227), OLS, child's completed years of schooling, individual level:**
- "Highest Parental Years of Schooling Completed" Model 1 ".274***" "(.016)"; Model 3 ".192***" "(.030)".
- "Highest Parental Contextual Attainment" Model 2 ".023***" "(.001)"; Model 3 ".008**" "(.003)".
- Controls: generation×ethnicity dummies, income, occupation, household. So 1 origin-percentile point = 0.008 child years holding absolute parental years; 0.023 alone. Restricted to parents ≤12 years, the contextual effect is "50 percent larger" (p.227; repo memo gives 0.012 (0.006) from Appendix Table A2, not re-read here).
- Re-verification: these match the repo's 2026-09-16 transcription exactly.

**Table 5 (p.230), group means, percentiles in the US distribution (by gender and age) and parents' birth-country percentile:** e.g. 1.5/2nd East Asians: child US pctile "77.29", parent US pctile "56.65", parent birth-country pctile "88.54" (N 109); 2nd Mexicans: "39.80", "16.42", "67.60" (N 282); 1.5 Mexicans "44.65", "12.05", "57.32"; 3rd+ Whites "54.01", "57.53" (N 4,887); 2.5/3rd+ Mexicans "41.45", "41.21", "47.33" (N 377). Text: "none demonstrates an upward trend in intergenerational educational mobility when parental educational attainments are considered within their home country contexts" (p.232); East Asian "89th percentile in their home countries, but their children score at the 77th percentile" (p.231).

**[CALCULATION: scratchpad `fl_slope.py`, from the 13 immigrant-parent rows of Table 5]** Group-level rank-on-rank, published group means (not a published slope):
- child US percentile on parent US percentile: WLS (weights = N) slope **0.46**, intercept 34.4; OLS 0.42 (0.40 without the two Mexican rows).
- child US percentile on parent birth-country percentile: WLS 0.77, OLS 0.56 (driven by the Mexican rows, which are the only groups below the 80th origin percentile).
- For the 5 native-parent groups (2.5/3rd+, a G2.5+→G3+ contrast, race-defined): WLS 0.76, OLS 0.69 — a much stronger carry once parents are US-born, consistent with the Borjas/CDE pattern that the G1→G2 step has a large common uplift and a flatter slope. 5 points; illustrative only.

### 6. Ward (2020), "The Not-So-Hot Melting Pot: The Persistence of Outcomes for Descendants of the Age of Mass Migration," AEJ: Applied 12(4):73-102, DOI 10.1257/app.20170382

Read from the **Online Appendix** only [SOURCE: https://www.aeaweb.org/articles/materials/13417, 23 pp., pdftotext]; the main-paper PDF returned an HTML page (not fetched), so main-text Table 4 and page numbers are [GAP]. Design: 1880 immigrant grandfathers linked to 1910 sons and 1940 grandsons (base sample 96,726), outcome log occupational score; European and other origins. Two estimators reported side by side: "Mean Convergence (ϴ1), collapsed at ethnic level" (**origin-group means**, WLS by group size) and "Mean Convergence (β1+β2), from microdata" (individual own-ancestor outcome + ethnic mean, i.e. Borjas's ethnic-capital sum).

**Appendix Table A1, ln(occupational score), 1950 basis column / 1890-1950 basis column, SE in parentheses:**
- Panel A, G1 1880 → G2 1910: group-collapsed "0.976" "(0.236)" / "0.888" "(0.209)"; microdata "1.019" "(0.032)" / "0.920" "(0.031)".
- Panel B, G2 1910 → G3 1940: group-collapsed "0.736" "(0.048)" / "0.566" "(0.038)"; microdata "0.737" "(0.025)" / "0.562" "(0.019)".
- Panel C, G1 1880 → G3 1940: group-collapsed "0.739" "(0.156)" / "0.512" "(0.110)"; microdata "0.734" "(0.032)" / "0.508" "(0.023)".
- Occupational-category outcomes (Farmer, White collar, Skilled, Unskilled) vary widely, e.g. G2→G3 white collar "1.198" "(0.282)", unskilled "0.334" "(0.160)".

**Appendix Table A3, G1 1880 → G3 1940, microdata, grandparental outcome + ethnic mean = sum:**
- Row 1 base (ln occ score): "0.206 (0.005)", "0.303 (0.022)", sum "0.508 (0.023)", N 96,726.
- Row 9, education years in 1940 on literacy in 1880: sum "14.53 (2.750)" (literacy is a 0-1 share; 20-point literacy gap → ~2.9 years, far larger than Borjas 1994's 2.42 × 0.2 = 0.5 years) [CALCULATION].
- Row 10, 1940 wage income on 1880 occ score: sum "0.545 (0.057)", N 68,912.
- Row 12-13, 1901 Cost of Living Survey income scores: sums "0.270 (0.040)" and "0.248 (0.037)" — the persistence estimate halves under a different occupational-income mapping.
- Table A2 (Europeans only): ln occ score sums "0.468 (0.022)" (1890-1950 basis) and "0.683 (0.032)" (1950 basis).

AEA Research Highlight (secondary, not the paper): "Over half of the original income gap between ethnic groups persisted to the third generation"; excluding farmers "the occupational gap persists across three generations at only 28 percent, as opposed to 51 percent" [SOURCE: https://www.aeaweb.org/research/persistence-outcomes-descendants-immigration-us, 2020-11-06]. Abstract: persistence of ethnic gaps "is 2.5 times stronger than predicted by a standard grandfather-grandson elasticity".

Reading. Ward's group-mean carry-over is far stronger than Borjas's: G1→G2 ~0.9-1.0 and G2→G3 ~0.56-0.74 on log occupational score; G1→G3 ~0.5. The magnitude depends heavily on how occupations are scored (0.25 with CLS income scores vs 0.51 base) and on farming (0.28 without farmers). Occupational scores ignore within-occupation pay, which likely inflates group persistence relative to wages [INFERENCE].

### Not done
- Feliciano 2005 Demography / IMR selectivity index by origin: not re-read (fetch_paper failed for 10.1353/dem.2005.0001; skipped on the parent's 10-turn instruction). The repo's ladder 75 has its own Feliciano-style index (slope 0.81 on BA share, 29 origins). [GAP]
- Borjas 2006 Future of Children: skipped (URL returned HTML). Commonly quoted rule "about half the gap closes each generation" is [UNVERIFIED] here; Borjas 1994's own statement (read above) is "in the order of .4 to .5".
- Hermansen (Norway), Hammarstedt (Sweden) G3, Duncan-Trejo: not reached.
- Corpus: Borjas 1992 and Feliciano-Lanuza 2017 are in the research corpus. `fetch_paper` failed for Borjas 1993/1994, ABJP 2021, Feliciano 2005 and for the NBER URL; those were read from local PDFs in the scratchpad (`lit/`), not saved to the corpus. [GAP]

## Summary table

"Group slope" = regression across origin-group means (or its micro-data equivalent: own-parent + ethnic-capital coefficients summed). Individual = parent-child micro regression, which is a different, smaller quantity.

| paper | outcome | unit of analysis | generation link | coefficient (SE) | table/page | verified? |
|---|---|---|---|---|---|---|
| Borjas 1993 JOLE | log earnings (relative to G3+) | origin means, OLS, 23 groups | G1 1940 → G2 1970 | 0.4465 (t 6.85; SE≈0.065); 0.3627 w/o Mexico; 0.2696 adj. wage | Table 4 rows 1-3, WP w3972 p.14 | yes (NBER WP, not JOLE print) |
| Borjas 1994 ILRR | occupational log wage | micro on group mean, RE, 32 groups | G1 1910 → G2 1940 | .6018 (.1374); reported wage .6724 (.1942) | Table 5, WP w4641 p.12 | yes (WP) |
| Borjas 1994 ILRR | years of schooling on 1910 literacy | same | G1 1910 → G2 1940 | 5.1176 (.9597) per unit literacy | Table 5, WP p.12 | yes (WP) |
| Borjas 1994 ILRR | occupational / reported log wage | same, 1980 ancestry proxy | G1 1910 → G3 1980 | .2006 (.0469) / .2684 (.0867) | Table 6, WP p.15 | yes (WP) |
| Borjas 1994 ILRR | schooling on literacy | same | G1 → G3; implied G2→G3 = .47 | 2.4202 (.7926) | Table 6, WP p.14-15 | yes (WP) |
| Borjas 1994 ILRR | log wage, GSS | individual + ethnic capital (sum) | G2 → G3 | .1630 (.0198) + .2945 (.1274) ≈ .46 | Table 8 panel II row 1, WP p.20-21 | yes (WP) |
| Borjas 1994 ILRR | education, GSS | individual + ethnic capital (sum) | G2 → G3 | .2571 (.0147) + .2669 (.1277) ≈ .53 | Table 8 panel I row 1, WP p.20-21 | yes (WP) |
| Borjas 1994 ILRR | log wage, GSS | grandchild on 1910 group mean | G1 → G3 | .2155 (.1083) | Table 8 panel II row 2, WP p.20 | yes (WP) |
| Borjas 1992 QJE | education (GSS) | individual + ethnic capital, RE | G1 → G2 | .1741 (.0225) + .2267 (.1079) ≈ .40 | Table V | yes (JSTOR parse; page [GAP]) |
| Borjas 1992 QJE | education (GSS) | same | G2+ → G3+ | .2620 (.0080) + .2071 (.1099) ≈ .47 | Table V | yes |
| Borjas 1992 QJE | log wage (NLSY) | same | G1 → G2 / G2+ → G3+ | .2162+.7017 ≈ .92 / .3385+.2078 ≈ .55 | Table V | yes |
| Borjas 1992 QJE | ethnic-capital coefficient alone, pooled | individual, RE | all | educ .2265 (.0466) GSS; log wage .2843 (.0955) NLSY | Table III col. 3 | yes |
| Card-DiNardo-Estes 2000 | years of schooling, sons | origin means, WLS, 34/33 groups | G1 → G2 (1940→70; 1970→95) | 0.41 (0.10); 0.43 (0.05) | Table 7, WP 6519 PDF p.57 | yes (OCR of WP) |
| Card-DiNardo-Estes 2000 | log weekly wage, sons | same | G1 → G2 | 0.44 (0.05); 0.62 (0.12) | Table 7 | yes (OCR of WP) |
| Card-DiNardo-Estes 2000 | daughters educ / log wage | same | G1 → G2 | 0.47/0.21 (1940-70); 0.42/0.50 (1970-95) | Table 7 | yes (OCR of WP) |
| ABJP 2021 AER | income rank, sons | individual father-son | G1 → G2 | immigrant slope 0.36−0.08 = 0.28 (1880-1910); OI cohort 0.33−0.08 [0.01] | Table 1, p.592 | yes (AER print) |
| ABJP 2021 AER | cross-origin group slope | — | G1 → G2 | not printed (Fig. 1 graphic only) | Fig. 1, p.589 | n/a [GAP] |
| Feliciano-Lanuza 2017 ASR | years of schooling | individual; parent origin-country percentile | G1 → G2 | .023 (.001) alone; .008 (.003) with parental years .192 (.030) | Table 3, p.226-227 | yes (corpus PDF) |
| Feliciano-Lanuza 2017 ASR | US schooling percentile | 13 origin-generation group means (our fit) | G1 → G2 | WLS 0.46 on parent US pctile; 0.77 on parent origin pctile | computed from Table 5, p.230 | [CALCULATION], not published |
| Ward 2020 AEJ:App | ln occupational score | origin means (WLS) / micro sum | G1 1880 → G2 1910 | 0.976 (0.236) / 1.019 (0.032) | App. Table A1 panel A | yes (appendix) |
| Ward 2020 AEJ:App | ln occupational score | same | G2 1910 → G3 1940 | 0.736 (0.048) / 0.737 (0.025); 1890-1950 basis 0.566 (0.038) | App. Table A1 panel B | yes (appendix) |
| Ward 2020 AEJ:App | ln occ score; wage income; schooling | micro sum (grandparent + ethnic mean) | G1 → G3 | 0.508 (0.023); wages 0.545 (0.057); CLS scores 0.248-0.270 | App. Table A3 rows 1, 10, 12-13 | yes (appendix); main Table 4 [GAP] |
