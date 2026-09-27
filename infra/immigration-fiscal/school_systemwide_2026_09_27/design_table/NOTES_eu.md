claude-opus-5-5

# Design table: European and other non-US immigrant-peer studies

**Verdict:** One of the eleven designs, Brunello and Rocco 2013 (countries over PISA waves), can see a shift common to a whole school system, and it finds harm: -0.275% of natives' PISA score per point of first-generation share. Tumen 2021 sees regions within Turkey; the other nine cannot see a system-wide shift, because they compare pupils within a school or a year, or standardize scores within each year. (Verdict line written by the lane lead on 2026-09-28 from the rows below. The helper stopped at its 40-turn cap after its last write at 02:42 JST, before its German Länder and grade-inflation searches.)

Scope: for each study, the outcome measure and its normalization, stakes, identifying comparison and fixed effects, and whether the design could detect a shift common to every school in the system. Filled from primary text only; `[UNVERIFIED]` marks cells where primary text was unreachable. Companion CSV: `design_eu.csv`.

## Studies

### 1. Brunello & Rocco 2013 (EER 32; read as IZA DP 5479, Feb 2011) — detects system-wide shift: YES

Text: `_cache/br_dp5479.pdf` (pdfinfo Title matches). Printed page numbers.

- Panel: 27 countries x PISA waves 2000/2003/2006/2009 x 3 subjects = 238 cells (p. 10). Each domain enters only from its major-domain wave onward (reading 2000-09, maths 2003-09, science 2006-09) "to enhance the comparability over time" (p. 8). Outcome = log of the country mean score of natives; share = PISA-sample share of first-generation immigrant 15-year-olds (born abroad of two foreign parents), computed from PISA itself.
- Effects: country, time (wave) and subject dummies (eq. 1, p. 6; Table 2 notes p. 19); controls GDP level/growth, secondary spending, total immigrant stock (the Gould-Lavy-Paserman idea moved to country level: "Conditional on this stock, the share of immigrant pupils ... is as good as random", p. 6), books, share boys. SE clustered country x time.
- Variation: "two thirds of the total variation in this share occurs between countries, one third" within countries over time (p. 10). The estimate uses the within third.
- Headline: Table 2 col. 1, -0.275** (0.135) log points per unit share [SOURCE: dp5479 Table 2, p. 19]; poor-background -0.409*** (0.155). Split-sample IV mean -0.281 (Table 4, p. 21). Per 10 pp = -2.75% of score [CALCULATION].
- Why it sees a system-wide shift: the cell is the whole country, the scale is linked across waves, and identification is the country's change relative to other countries. What it cannot see: a shift common to all 27 countries in the same wave (absorbed by wave dummies), and it cannot separate "lower standards" from "less learning" since PISA measures skill, not grading. [INFERENCE]
- [GAP] Journal version (EER 2013) not read; IZA World of Labor describes the journal sample as 19 countries, the DP has 27.

### 2. Ohinata & van Ours 2013 (EJ; read as IZA DP 6212) — NO

Text `_cache/ovo_dp6212.pdf` (Title matches). Absolute IEA scale (PIRLS/TIMSS plausible values, points), low-stakes, but school FE and one regression per survey year: "separate regressions are estimated for each year" (p. 16). The only variation is between classes of one school in one year. All six school-FE coefficients are within about +/-1.5 points per pp and five are insignificant (Table 4) [SOURCE: dp6212 Table 4]. The DP has two survey years per subject but never compares them; a Dutch-wide change between 2001 and 2006 is outside the design. [GAP] EJ version not read.

### 3. Geay, McNally & Telhaj 2013 (EJ; read as IZA DP 6451) — NO

Text `_cache/gmt_dp6451.pdf` (Title matches). KS2 percentile score (native mean ~50), high-stakes for schools (p. 8, performance tables). Year dummies + school FE + school trends + age-7 prior attainment (eq. 1, p. 12; Table 4 p. 32). Full-spec reading 0.002 (0.008) percentile points per pp. Two independent reasons it is blind to a national shift: the outcome is a rank, and year dummies absorb national cohort shifts. High stakes for schools also make KS2 exposed to teaching-to-the-test, but the DP does not test that. [GAP] Whether percentiles are ranked within each year is not stated in words; [INFERENCE] from a native mean of ~50 in each year.

### 4. Ballatore, Fort & Ichino 2018 (JOLE; read as authors' accepted version, 22 Feb 2018) — NO

Text `_cache/bfi2018.pdf` (no pdfinfo Title; first-page title and authors match). INVALSI 2009-10, grades 2 and 5, fraction correct, school-grade means; one cross-section. Institution x grade FE, identification from class-formation rules between schools of the same principal. PEC (swap one native for one immigrant) language -0.0158** (0.0077), weak first stage (F 2.93); one-endogenous -0.0085*** (0.0025), F 18.0 [SOURCE: accepted version Table 2, pdf p. 27]. Blind to a national shift by construction (single year, within-institution). Of interest for this lane: sec. 5.6 treats teacher score manipulation as a threat and tests it with the Angrist et al. cheating indicator, i.e. grading behaviour on INVALSI is itself a documented margin in Italy.

### 5. Tonello 2016 (Empirical Economics 51:383-414; read as IEB WP 2011/21 precursor) — NO

Text `_cache/tonello_ieb.pdf`. Grade-8 INVALSI First Cycle exam (part of the final state exam: plausibly high-stakes for pupils), log of the natives' school mean; school FE + 5 macro-area x year FE (fn. 13, p. 11); within-school adjacent-cohort variation. Language -0.0653** (0.0253), maths -0.0499 (0.0344) per unit share (Table 5, p. 27) [SOURCE]. Territory x year FE absorb any Italy-wide or macro-region shift. [GAP] Journal version not read (Springer paywall); coefficients may differ.

### 6. Frattini & Meschi 2019 (EER 113; read as IZA DP 11027) — NO

Text `_cache/fm_dp11027.pdf` (Title matches). Lombardy vocational schools; end-of-third-year externally marked tests that are part of the final qualification exam (p. 6); scores z-scored "in each wave" (p. 7); school FE, cohort dummy, entrance-score value added. Maths -0.463** (0.203) per unit class share, low-ability -0.754*** (0.235) (Table 5.1) [SOURCE]. Within-wave z-scoring alone makes it blind to a region-wide level shift. [GAP] EER version not read (revision text quotes 7.6% SD per 15 pp vs DP 7.4% per 16 pp).

### 7. Jensen & Rasmussen 2011 (EER 30(6)) — NO; journal text [UNVERIFIED]

Journal unreachable: ScienceDirect subscriber-only, `fetch_paper` on the DOI fails (re-tried 2026-09-28), SSRN 2629091 "Not Available for Download". Read instead the April 2008 WP (`_cache/jr2008.pdf`, pure.au.dk/ws/files/2953/immigrant_children_wp.pdf; reading only, WLE on the OECD 500/100 metric). Natives-only reading: OLS -0.28** (Table 9), IV -0.31* (Table 11) points per pp non-Western school share; SEs not printed. Design: PISA 2000 + 2005 PISA-Ethnic, between schools, IV = county concentration (Dustmann-Preston). An absolute scale, but no between-system or over-time contrast: a Denmark-wide level is invisible. The journal's native maths estimate remains [GAP].

### 8. Schilling & Hoeckel 2026, Hamburg (EJ 136:1217-1253) — NO

Published text via KOPS Konstanz (`_cache/hamburg_ej2026.pdf`, Title matches). The native part (sec. 5) follows Figlio et al.: cumulative grade 1-4 refugee share, first-school FE + test-year FE (eq. 1, p. 1244). KERMIT 5 is a low-stakes Hamburg diagnostic, z-scored "across all years and students" (p. 1228-29), so the score itself is not re-centred each year, but the test-year FE remove any city-wide yearly shift. Table 10 panel B: raw -4.39*** (1.35) per unit share, which vanishes to 0.27 (0.58) with school FE (p. 1246) [SOURCE]. The raw negative comes from between-school differences. Note for the lane: the pooled-over-years z-score means a Hamburg time series of German-born KERMIT means could be built from the same data; the paper does not report it. [GAP]

### 9. Hassan, Hvidtfeldt, Andersen & Udsen 2023, Denmark refugees (ESR 39(3), doi 10.1093/esr/jcac059) — NO

Published advance-article PDF via the Rockwool Foundation (`_cache/dk_esr2023.pdf`, 14 pp.). Danish national tests, z-scored "within grade-year" per profile area, averaged, re-standardized (p. 6). DiD: score growth grade 2->4 (Danish), 3->6 (maths) for cohorts receiving a refugee between tests vs not, with school FE (p. 7). Table 3 col. 3: Danish -0.010 (0.009), maths -0.010 (0.010) [SOURCE, p. 11]; the level gap (Refugee, col. 1: -0.067***) is pre-existing selection. Grade-year z-scoring alone makes it blind to a national shift. Stakes low for pupils [TRAINING-DATA].

### 10. Gould, Lavy & Paserman 2009, Israel (EJ 119:1243-1269) — NO

Read as IZA DP 1883 (Dec 2005; `_cache/glp_dp1883.pdf`, Title matches), the version with the birth-date IV that the EJ abstract describes; also fetched NBER w10844 (2004, earlier design, `_cache/glp_w10844.pdf`). One national cohort (5th graders 1993-94); no school FE ("This prevents us from using ... multiple cohorts and school fixed effects", fn. 4, p. 8); comparison among schools with the same number of immigrants in grades 4-6 (stratified IV). Outcomes are attainment: matriculation pass (high-stakes, national threshold) and dropout. Table 7B weighted IV: matriculation -0.0028 (t -2.00), dropout +0.0015 (t 2.51) per pp [SOURCE, p. 38]; 0->10% = -3.16 pp matriculation (p. 26). Blind to anything common to all Israeli schools, including a national change in the bagrut standard. [GAP] EJ numbers not verified against the published text.

## Search log

(appended as searches run)
