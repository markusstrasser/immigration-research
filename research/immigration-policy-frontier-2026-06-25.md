# Immigration Policy / Enforcement / Legalization Frontier — Scout (2026-06-25)

Axis: POLICY-EVALUATION frontier — legalization (IRCA/DACA), enforcement (Secure Communities,
287(g), E-Verify causal-on-crime, deportation), sanctuary, refugee resettlement. Two jobs:
(A) execute already-scouted OA fetches; (B) scout the 2020-26 + landmark policy-eval frontier.

INSTRUMENT-BIAS NOTE (mandatory): politically charged, LLM-assisted, left-tilted field.
Disconfirming/against-interest evidence weighted as higher-information. Tags:
`[SOURCE: url]` `[INFERENCE]` `[UNVERIFIED]` `[TRAINING-DATA]`; framing flagged `[FRAMING-SENSITIVE]`.
ALREADY COVERED by parent/siblings (do not re-derive): E-Verify staggered-TWFE on QWI (wage side);
surge 2021-24 / CHNV / EOIR court panels.

---

## (A) FETCH RESULTS

| # | Paper | DOI | Status |
|---|-------|-----|--------|
| 1 | Ousey & Kubrin (2018) Immigration and Crime, Annu Rev Criminol | 10.1146/annurev-criminol-032317-092026 | **METADATA-ONLY** — saved to corpus (S2 `33034e4c…`, 310 cites); full-text PDF unfetchable (annualreviews JS-gated, not on Sci-Hub). NOTE: corpus crime memo already synthesized this paper's body in a prior session (r = -0.031 weighted mean, quoted) — the analytic content is captured even though the PDF isn't re-fetchable now. |
| 2 | Light, He & Robey (2020) PNAS 117(51):32340 | 10.1073/pnas.2014704117 | **ALREADY IN CORPUS, full text ✓** (`10.1073_pnas.2014704117`, PMC7768760, pdf_path present). No fetch needed. |
| 3 | Abramitzky et al. (2024) Law-Abiding Immigrants, NBER w31440 | 10.3386/w31440 | **FETCHED ✓** (`doi_10_3386_w31440`, 63k chars full text, quality-assessed). [The metadata-only SSRN copy `10dc2477…` (DOI 10.2139/ssrn.4878020) was already in corpus but had no body; w31440 supplies the full text.] |
| 4 | Butcher & Piehl (2007) NBER w13229 | 10.3386/w13229 | **FETCHED ✓** (`doi_10_3386_w13229`, 126k chars full text, quality-assessed). |
| 5 | Hausman (2020) Sanctuary policies, PNAS 117(44):27262 | 10.1073/pnas.2014673117 | **METADATA + KEY FINDINGS captured** (abstract saved; results archived via `save_source` from PMC7959582). Full-text PDF exists (PMC7959582/pdf/pnas.202014673.pdf) but research-mcp `fetch_paper` rejected it — **transport-layer failure**, not paywall (the same fetcher got PNAS Light-He-Robey fine). Findings verified: sanctuary policies cut deportations ~1/3 (2010-15), no-conviction deportations fell >50%, violent-conviction deportations unchanged, NO detectable crime effect. |

**Fetch summary: 2 newly fetched full-text (#3, #4); 1 already-present full-text (#2); 2 metadata/findings-captured (#1, #5) where the MCP PDF fetcher failed (annualreviews JS-gate; PNAS transport quirk — both bodies' key results are nonetheless captured).**

## (B) NEW PAPERS (graded; what each tests / disconfirms)

All verified via S2/OpenAlex/Exa this session (not memory). Grades follow the constitution's
evidence ladder; "design" notes the identification strategy because for policy eval the design IS
the evidence. Saved-to-corpus papers flagged `[CORPUS+]`; abstract/metadata-only `[META]`.

### B1. LEGALIZATION → CRIME  (the strongest new cluster — a coherent quasi-experimental literature)

This is the genuinely NEW spine. The corpus's crime memo is *descriptive/cross-sectional* (arrest/incarceration
*levels* by status). This cluster is *causal*: it estimates what happens to crime when the SAME people gain
legal status. It converges, from multiple countries and designs, on **legalization REDUCES crime, via the
labor-market channel.** That is a strong, against-the-restrictionist-prior, well-identified finding.

1. **Baker (2015), "Effects of Immigrant Legalization on Crime," AER 105(5):210-13.** DOI 10.1257/aer.p20151041. ~110 cites. **[META]** (AER P&P short; full WP is the SIEPR 2013 version).
   [SOURCE: https://www.aeaweb.org/articles?id=10.1257/aer.p20151041]
   **Design:** IRCA 1986 legalized ~3M; exploits quasi-random *timing* of legalization + geographic variation in
   treatment intensity (share of county legalized), using IRCA application admin data. **Finding:** crime fell
   **3-5%** (WP range 2-6%), concentrated in **property** crime; ≈120,000-180,000 fewer crimes/yr. A calibrated
   labor-market model attributes most of the drop to improved job opportunities for applicants. **Tests:** the
   central legalization→crime claim with US data. **Grade: STRONG (contested-to-good evidence; well-identified
   natural experiment, top journal).** Note: pre-legalization, IRCA applicants had HIGHER crime — the effect is
   the *disappearance* of that gap post-legalization (against-interest detail the corpus should hold).

2. **Pinotti (2017), "Clicking on Heaven's Door: The Effect of Immigrant Legalization on Crime," AER 107(1):138-68.** DOI 10.1257/aer.20150355. **183 cites.** **[META]** (saved metadata; OA PDF at aeaweb).
   **Design:** the cleanest available — a *true RD*. Italy issues fixed annual residence-permit quotas; applications
   submitted on specific "click days," processed first-come-first-served until the quota runs out. Compares
   applicants just-above vs just-below the cutoff. **Finding:** legalization cut the probability of committing a
   serious crime from **~1.1–2.2 percentage points to ~0.4 pp** in the following year (roughly halving it).
   **Tests/strengthens:** the legalization→crime mechanism with the strongest identification in the literature
   (knife-edge RD removes selection). **Grade: STRONG (best-identified causal estimate in the cluster).**
   [FRAMING-SENSITIVE] external validity: Italy, economic migrants — transfer to US undocumented carefully.

3. **Freedman, Owens & Bohn (2018), "Immigration, Employment Opportunities, and Criminal Behavior," AEJ:Econ Policy 10(2):117-51.** DOI 10.1257/pol.20150165. **112 cites.** **[CORPUS+]** (saved `W2163425697`).
   **Design:** exploits IRCA's *dual* structure — it legalized long-time unauthorized residents (↑ employment access)
   but simultaneously imposed employer sanctions that *cut* employment access for *more recent* arrivals. San Antonio
   felony charge data. **Finding:** the group whose job access IMPROVED saw crime fall; the group whose job access
   WORSENED (recent arrivals locked out by employer sanctions) saw crime RISE. **Tests the mechanism directly:** it
   is *labor-market access*, not legal status per se, that moves crime — and shows enforcement that removes work
   access can *increase* crime. **Grade: STRONG. Important nuance/partial-disconfirmer for naïve "legalize = less
   crime": the channel is jobs, so enforcement-without-work-access is criminogenic.**

4. **Mastrobuoni & Pinotti (2015), "Legal Status and the Criminal Activity of Immigrants," AEJ:Applied 7(2):175-206.** DOI 10.1257/app.20140039 (per AEA). ~100+ cites. **[META]** (surfaced via Exa/RePEc; not separately saved — Pinotti 2017 RD is the stronger same-author result already in corpus).
   **Design:** EU enlargement changed legal status for some nationalities of released inmates; compares recidivism.
   **Finding:** legal status → **lower recidivism**, larger for economically-motivated migrants. **Grade: MODERATE
   (small N <2,000 released inmates, possibly non-representative — Baker's own caveat).** Triangulates B1-B3.

5. **Ibáñez, Rozo, Bahar & Urbina (2025), "Protecting the vulnerable: How migrant regularization reduces crime and empowers women," J. Development Economics.** DOI 10.1016/j.jdeveco.2025.103667. **[CORPUS+, META-only body]** (already in corpus, no full text).
   **Design:** Colombia's mass regularization of Venezuelan migrants. **Finding (per title/venue):** regularization
   **reduces crime**, with a gendered empowerment channel. **Tests:** external validity of the legalization→crime
   finding in a *South-South*, very-recent, mass-scale setting (closest analog to a US surge-legalization). **Grade:
   MODERATE-STRONG pending full-text read (JDevEcon, 2025, but body not yet fetched — flagged for parent).**

### B2. ENFORCEMENT → CRIME  (does deporting "criminal aliens" reduce crime? — largely NULL)

The enforcement-side complement. The restrictionist frame is that removing criminal aliens makes communities
safer. The best-identified studies say enforcement intensity did **not** measurably reduce crime.

6. **Miles & Cox (2014), "Does Immigration Enforcement Reduce Crime? Evidence from Secure Communities," J. Law & Economics 57(4).** DOI 10.1086/680935. **197 cites — the landmark.** **[CORPUS+]** (saved `f5edf5e34acc…`).
   **Design:** staggered county-by-county activation of Secure Communities (SC fingerprint-sharing → ~deported
   hundreds of thousands). DD on activation timing. **Finding:** SC led to **no observable reduction** in the FBI
   index-crime rate, including violent crime — despite removing many noncitizens. **Tests:** the core
   "enforcement-reduces-crime" claim. **Grade: STRONG (large, well-identified, top field journal). A central
   disconfirmer of the enforcement-works frame.**

7. **Kang & Song (2021), "Did Secure Communities Lead to Safer Communities? … Geographical Externalities," J. Law, Econ. & Org. 37(?).** DOI 10.1093/jleo/ewab013. 7 cites. **[CORPUS+]** (saved `a557d011…`).
   **Design:** re-examines SC rollout, adds *spatial spillover* (deportation in county A displacing crime to/from
   neighbors). **Finding:** largely **null** main effect on crime; some geographic-externality structure. **Tests:**
   robustness of Miles-Cox with externalities. **Grade: MODERATE-STRONG (replication + extension; smaller footprint).**

8. **Hausman (2020), "Sanctuary policies reduce deportations without increasing crime," PNAS 117(44):27262.** (see FETCH §A #5). **[META + key findings archived]**
   **Design:** SC rollout + sanctuary adoption timing; the *flip side* of enforcement. **Finding:** sanctuary cut
   deportations ~1/3 (no-conviction deportations >50%), violent-conviction deportations unchanged, **NO crime
   effect.** **Grade: STRONG (PNAS, causal, single Stanford author).** Bridges B2↔B3.

### B3. SANCTUARY → CRIME  (the sanctuary-crime null literature)

9. **Kubrin & Bartos (2020), "Sanctuary Status and Crime in California: What's the Connection?," Justice Evaluation Journal 3(2):116-33.** DOI 10.1080/24751979.2020.1745662. **[META + full method captured via Exa]** (paywalled body; SSRN 3557558).
   [SOURCE: https://www.tandfonline.com/doi/abs/10.1080/24751979.2020.1745662]
   **Design:** **synthetic control** — California's 2018 violent + property crime vs a "Synthetic California"
   (weighted donor states matched on 1970-2017 crime trends), treating SB54 (2017 sanctuary-state law) as the
   intervention. **Finding:** SB54's impact on violent and property crime is "**neither robust nor sufficiently
   large to rule out a null effect**"; post-estimation placebo/sensitivity tests confirm. **Tests:** the politically
   central "sanctuary state → crime spike" claim, at the state level, first of its kind. **Grade: MODERATE-STRONG
   (clean synthetic-control design; limitations the authors name — short post-period, statewide aggregation may
   mask local heterogeneity).** [FRAMING-SENSITIVE: a null is "fail to reject," not proof of zero — but the
   *direction of the political claim* (crime rises) is specifically not supported.]

### B4. DACA → LABOR / EDUCATION / HEALTH  (legalization-lite causal evals; RD/DD on eligibility cutoffs)

The corpus is thin on DACA. These are the load-bearing causal evals — most exploit DACA's sharp eligibility
cutoffs (age at arrival ≤16, arrived by 2007, under 31 in 2012, HS-educated) for RD/DD.

10. **Kuka, Shenhav & Shih (2020), "Do Human Capital Decisions Respond to the Returns to Education? Evidence from DACA," AEJ:Econ Policy 12(1):293-324.** DOI 10.1257/pol.20180352. **101 cites.** **[CORPUS+]** (saved `W2786285019`; NBER w24315 OA).
    **Design:** DD using DACA eligibility cutoffs (age/arrival/education) vs ineligible undocumented. **Finding:**
    DACA eligibility **raised high-school completion and reduced teen births**; human-capital investment responds to
    the returns that work authorization unlocks. **Tests:** the schooling/assimilation channel of legalization.
    **Grade: STRONG (AEJ:Pol, clean DD on administrative cutoffs).**

11. **Hsin & Ortega (2018), "The Effects of DACA on the Educational Outcomes of Undocumented Students," Demography 55(4):1487.** DOI 10.1007/s13524-018-0691-6. **127 cites.** **[CORPUS+]** (saved `W2769440843`).
    **Design:** CUNY administrative records, DD on DACA-eligibility. **Finding:** mixed — DACA *raised* employment but
    *increased dropout* among some community-college students (work-now incentive vs school). **Grade: STRONG.
    Against-interest nuance:** legalization's education effect is not uniformly positive — the work option can pull
    marginal students out of school. Good steelman material.

12. **Villanueva Kiser & Wilson (2024), "DACA, Mobility Investments, and Economic Outcomes," Upjohn WP 24-395.** DOI 10.17848/wp24-395. **[META]** (OA WP at research.upjohn.org).
    **Design:** DACA-eligibility variation. **Finding:** DACA increased geographic + job mobility of young immigrants,
    raising earnings. **Grade: MODERATE (recent WP, not yet peer-reviewed).** Adds the mobility channel.

13. **Tran (2025), "The effects of DACA on labor market outcomes," J. Demographic Economics**, DOI 10.1017/dem.2025.5; and Tran (2025) "Parents' legal status and children's health insurance: Evidence from DACA," Contemp. Econ. Policy, DOI 10.1111/coep.70009. **[META]**
    **Finding:** DACA raised recipients' employment/earnings; parental DACA raised US-born children's public-insurance
    take-up (reduced chilling-effect). **Grade: MODERATE (2025, low cites, single author).** Newest DACA evidence;
    the health-insurance one is a *fiscal-adjacent* spillover (take-up of public benefits by citizen children).

### B5. UNDERREPORTING / SELECTION CAVEAT  (the mechanism that complicates ALL crime estimates)

14. **Comino, Mastrobuoni & Nicolò (2020), "Silence of the Innocents: Undocumented Immigrants' Underreporting of Crime and their Victimization," J. Policy Analysis & Management 39(4):1214.** DOI 10.1002/pam.22221. 38 cites. **[CORPUS+]** (saved `W3008368453`).
    **Design:** victimization surveys + admin data around the 1986 US amnesty. **Finding:** undocumented migrants
    **underreport** crimes (to avoid deportation) AND are **disproportionately victimized** because offenders exploit
    that silence. **Tests:** the measurement caveat the corpus crime memo already flags — here it is *quantified
    causally* (amnesty raised reporting). **Grade: STRONG. Critical for honest interpretation: arrest/report-based
    crime stats UNDERSTATE undocumented victimization and may bias offending estimates downward — cuts both ways,
    and the corpus must hold it against any "low arrest rate = low offending" reading.**

## (C) DATASET CARDS (policy/enforcement admin data — new ones for the register)

Format: Source / gated? / URL / key vars / quirks / what-it-settles. The corpus ALREADY HAS: EOIR Case Data
(court load by nationality/proceeding), ICE budget justifications, USAspending DHS obligations, OHSS state
immigration flat file (refugee/LPR/naturalization panel), EOIR workload PDFs. The cards below are the gaps.

**DS-1. TRAC Immigration (Syracuse U.) — ICE/EOIR enforcement & court microdata.**
- Gated? Partly — public dashboards free; full data tools / bulk behind TRAC subscription (FOIA-derived).
- URL: https://trac.syr.edu/immigration/
- Key vars: ICE detainers, arrests, removals by criminality/charge/origin/field-office; EOIR case
  outcomes (asylum grant rates by judge/court/nationality); detention facility populations; ICE
  book-ins. Monthly granularity.
- Quirks: FOIA-sourced, so coverage gaps + lags; judge-level asylum data is TRAC's signature (huge
  judge heterogeneity). Court venue ≠ respondent residence (same caveat as the corpus EOIR data).
- Settles: enforcement *intensity* time series for staggered-rollout designs (Secure Communities,
  287(g)); asylum-grant variation; the "criminal alien" removal composition (INT-05 in the roadmap).

**DS-2. DHS Yearbook of Immigration Statistics (+ OHSS data tables).**
- Gated? No — fully public.
- URL: https://www.dhs.gov/ohss/topics/immigration/yearbook  (OHSS now publishes; legacy at dhs.gov/immigration-statistics)
- Key vars: LPRs by class-of-admission/country/state; naturalizations; refugees & asylees admitted by
  country; nonimmigrant admissions; **enforcement actions** (apprehensions, removals, returns,
  detentions) by year back to ~1892 (some series). Annual.
- Quirks: definitions shift across decades (removals vs returns reclassified post-IIRIRA 1996); state
  detail only for some tables. Aggregate, not micro.
- Settles: long-run denominators (stock/flow by origin) and the removals/returns enforcement series —
  the national-level treatment-intensity backbone. Partly overlaps the corpus OHSS flat file but the
  Yearbook adds the *enforcement-action* tables the flat file lacks.

**DS-3. Secure Communities activation dates (county × month rollout).**
- Gated? No — published; reconstructable from ICE/DHS records + the Miles-Cox / Cox-Miles replication files.
- URL: ICE SC archive (via web.archive.org of ice.gov/secure-communities); replication data in
  Miles & Cox (2014) JLE supplement & Cox-Miles SSRN.
- Key vars: county FIPS, SC activation month (2008-2013 staggered rollout to full national coverage Jan 2013).
- Quirks: the *staggering was plausibly not policy-targeted on local crime* (DHS rolled out by
  administrative readiness) — that's exactly why it's a clean DD instrument. Re-activated under Trump 2017,
  paused 2014-2017 — discontinuity to exploit.
- Settles: THE enforcement-intensity instrument for crime + labor DD designs (pairs with QWI wage panel
  the parent already built). High value, low acquisition cost.

**DS-4. State E-Verify mandate effective dates (state × date, with scope).**
- Gated? No — legislative public record (NCSL tracks).
- URL: NCSL E-Verify / employment-verification legislation tracker (ncsl.org); Arizona LAWA 2007 is the
  canonical first.
- Key vars: state, mandate effective date, scope (all employers / public only / public contractors),
  enforcement teeth (license revocation = "business death penalty" in AZ).
- Quirks: scope heterogeneity is large — "mandate" means very different things (AZ universal vs FL public-only);
  must code scope, not just a binary. The parent's E-Verify-QWI work uses the wage side; **crime-side and
  internal-migration-side are still open.**
- Settles: staggered-adoption instrument for E-Verify effects on crime, undocumented internal migration,
  and labor displacement (complements the already-covered wage TWFE).

**DS-5. ORR / refugee resettlement admin data (arrivals + ORR outcomes).**
- Gated? Partly — arrivals public (WRAPS/RPC); ORR outcome microdata (Annual Survey of Refugees) restricted.
- URL: Refugee Processing Center interactive reporting (wrapsnet.org); ORR reports (acf.hhs.gov/orr);
  Annual Survey of Refugees (restricted-use via ORR).
- Key vars: refugee arrivals by nationality × state × month × age/sex; ORR ASR: employment, English
  proficiency, public-assistance use, earnings trajectory over first 5 years post-arrival.
- Quirks: corpus already has the OHSS state refugee panel (replaces the dead ACF ORR CSV); the *new* piece
  is the ASR microdata for individual labor/fiscal trajectories (restricted). Resettlement *placement* is
  quasi-random conditional on nationality (assigned by agencies) → an under-used natural experiment.
- Settles: refugee fiscal/labor *trajectory* (the Evans-Fitzgerald estimand: refugees turn net-positive
  ~8 years in); refugee-vs-economic-migrant contrast.

## (D) GENUINELY NEW vs ALREADY-COVERED

**ALREADY COVERED (do not re-derive — confirmed in corpus/sibling memos):**
- Crime *levels* by status: Light-He-Robey 2020 (full text), Gunadi 2019, Ousey-Kubrin 2018 meta (synthesized),
  Abramitzky et al. 2024 incarceration gap (now full text). The *descriptive* crime picture is well-held.
- Wage-side E-Verify staggered TWFE on QWI; surge 2021-24 / CHNV / EOIR court panels (parent/sibling).
- EOIR court load, ICE budget, USAspending DHS, OHSS refugee/LPR panel (datasets).

**GENUINELY NEW (this scout's contribution):**
1. **The legalization→crime CAUSAL cluster (B1).** The corpus had crime *levels*; it did NOT have the
   quasi-experimental literature showing legalization *causes* crime to fall via jobs (Baker IRCA, Pinotti RD,
   Freedman-Owens-Bohn dual-treatment, Ibáñez Colombia). This is the single biggest gap closed. It reframes the
   crime question from "do immigrants commit crime" (levels) to "does *legal status* change behavior" (causal).
2. **The enforcement→crime NULL literature (B2).** Miles-Cox (197 cites, landmark) + Kang-Song + Hausman.
   The corpus could not previously speak to "does enforcement reduce crime." Answer: largely no.
3. **The sanctuary-crime null (B3, Kubrin-Bartos synthetic control).** Method + result captured.
4. **The DACA causal-eval cluster (B4).** Kuka-Shenhav-Shih, Hsin-Ortega, etc. — the corpus was thin on DACA.
5. **The underreporting/victimization caveat quantified (B5, Comino et al.).** Turns a hand-waved caveat in the
   crime memo into a causally-estimated bias.
6. **Five dataset cards** (TRAC, DHS Yearbook enforcement tables, SC activation dates, E-Verify mandate dates,
   ORR/ASR) — the enforcement-intensity instruments for staggered designs.

**Captured at close (was the top gap):**
- **Evans & Fitzgerald (2017), "The Economic and Social Outcomes of Refugees in the United States: Evidence from
  the ACS," NBER w23498.** DOI 10.3386/w23498. **[CORPUS+, full text ✓ — `doi_10_3386_w23498`, 92k chars,
  quality-assessed].** Did not surface in S2/OpenAlex (queries returned noise) but fetched directly by the NBER OA
  PDF URL at close. THE refugee-fiscal landmark: refugees' outcomes converge toward natives' over time; by ~20 years
  in the US, refugees pay substantially more in taxes than the cost of resettlement + benefits received (the
  oft-cited net-positive-after-~8-years result). **Design:** ACS, identifies likely refugees by country-of-origin ×
  arrival-cohort. **Grade: STRONG (the reference refugee-fiscal study; NBER WP, widely cited).** Closes the refugee
  sub-axis the brief named. Body now available for ask_papers extraction of the exact NPV/payback numbers.

**Deferred / [GAP] (surfaced but not captured — for parent / re-dispatch):**
- **Mastrobuoni & Pinotti (2015) AEJ:Applied** body not fetched (metadata only; Pinotti 2017 RD is the stronger
  same-finding paper, so lower priority).
- **287(g)-specific crime evals** did not surface cleanly (the search returned legal/ethnographic work, e.g.
  Armenta "Protect, Serve, and Deport" Nashville, not econometric crime DD). [GAP] Suggested: "287(g) program
  crime Forsyth county difference-in-differences" / look for O'Neil or Treyger-Epp-Shafer work.
- **DACA→crime specifically** (vs labor/education) is thin — Kuka-Shenhav-Shih and others measure schooling/labor,
  not crime directly. [GAP] One candidate: work on DACA and recidivism/arrests is sparse; may be a genuine
  literature gap worth flagging as such rather than a search miss.

## (E) DISCONFIRMATION (constitution mandate — actively held against the corpus's priors)

**What this scout's evidence DISCONFIRMS (against the restrictionist / crime-cost prior the corpus must stress-test):**
- "Enforcement reduces crime" — Miles-Cox + Kang-Song + Hausman: largely NULL. Deporting "criminal aliens" via
  Secure Communities did not measurably lower crime.
- "Sanctuary policies raise crime" — Kubrin-Bartos + Hausman: NULL. SB54 had no detectable crime effect.
- "Legalization/amnesty raises crime" — Baker, Pinotti, Freedman-Owens-Bohn, Ibáñez: REVERSED. Legalization
  *lowers* crime (property especially), via labor-market access.

**What this scout's evidence DISCONFIRMS in the OPPOSITE direction (against a naïve pro-immigration "more legal
status always better" read — weighted as higher-information because it cuts against the field's tilt):**
- **The channel is JOBS, not legal status per se (Freedman-Owens-Bohn).** The SAME law (IRCA) that cut crime among
  the legalized *raised* crime among recent arrivals locked out of work by employer sanctions. Implication: a
  legalization that does NOT deliver real labor-market access, or enforcement that strips work access, can be
  *criminogenic*. "Legalize and crime falls" is mechanism-contingent, not automatic.
- **DACA's education effect is not uniformly positive (Hsin-Ortega).** Work authorization pulled some marginal
  community-college students OUT of school (drop-out ↑). A legalization-fiscal model that assumes monotone
  human-capital gains overstates the benefit for that margin.
- **Underreporting cuts both ways (Comino-Mastrobuoni-Nicolò).** The corpus's crime memo leans on low
  arrest/report rates among undocumented. But undocumented *underreport* their own victimization and offending
  due to deportation fear — so low *recorded* crime partly reflects *silence*, not only low offending. This is a
  genuine measurement confound the corpus already flags; here it's quantified, and it weakens (does not destroy)
  the "low arrest rate = low offending" inference.

**Methodological honesty flags [FRAMING-SENSITIVE]:**
- All the "null" enforcement/sanctuary results are *failures to reject*, not proofs of zero effect; short
  post-periods (especially SB54) limit power. The *direction* of the political claim (crime rises) is specifically
  unsupported, which is the relevant test — but "no detectable effect" ≠ "certainly zero."
- The legalization→crime cluster is strongest in non-US settings (Pinotti Italy, Ibáñez Colombia); US evidence
  (Baker, Freedman-Owens-Bohn) is solid but rests on one policy (IRCA 1986) — external validity to a *future* US
  legalization of a different-composition population is an open question, not settled.
- Instrument-bias check: this scout deliberately surfaced and weighted the against-pro-immigration disconfirmers
  (jobs-channel-contingency, DACA dropout, underreporting) because the field tilts the other way and the LLM
  instrument shares that tilt. The net picture still favors "legalization↓crime, enforcement≈null on crime," but
  the corpus should carry the mechanism-contingency, not a flat slogan.

---
**Status: COMPLETE.** Fetch (Job A): 2 new full-text (#3 Abramitzky w31440, #4 Butcher-Piehl w13229) + 1
pre-existing full-text (#2 Light-He-Robey) + 2 findings-captured where the MCP fetcher failed (#1 Ousey-Kubrin
metadata, #5 Hausman findings archived). Scout (Job B): 15 papers graded across 5 clusters + Evans-Fitzgerald
w23498 (refugee landmark, full text fetched at close) + 5 dataset cards. NEW full-text papers added to corpus this
session: w31440, w13229, w23498, + saved metadata for Miles-Cox, Kang-Song, Kuka-Shenhav-Shih, Hsin-Ortega,
Freedman-Owens-Bohn, Comino et al., Ousey-Kubrin. Remaining gaps: 287(g)-specific crime DD; DACA→crime (may be a
true literature gap). Parent integrates INDEX + dataset-register; this agent did NOT commit.
