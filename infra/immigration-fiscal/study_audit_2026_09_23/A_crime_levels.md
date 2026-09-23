claude-opus-5-5[1m]

**Verdict:** None of the five studies shows any sign of fabricated or unreproducible data; the repo reproduced Light, He & Robey from the public package. Gunadi and Ousey & Kubrin hold for what they measure (Ousey & Kubrin is area-level only and cannot speak to offending by status). The Texas numbers hold in sign but not in magnitude, and the repo overstates their robustness: Light's own extreme recode moves total felonies from about 0.40 to 0.73 of the native rate, and the other leak (undocumented arrestees with no DHS record who self-report as citizens and land in the native group) is unbounded. Cato's Texas homicide-conviction figure (−26%), which ladder :617 says "closes the arrests ≠ guilt objection", rests on relabelling DPS's "unknown/other" residual as native-born and on an extract date that has moved a single year's rate from 8% below to 20% above the state rate. The single most consequential problem is asymmetry. The repo discards Lott's Arizona result over a contaminated status flag ("D4", author reputation, "AZ DOC itself confirms" with no ADC source on file), while Texas flags with a documented contamination in the opposite direction are rated HIGH/robust. On the only published bound, Arizona's contamination (10–21%) does not reverse Lott's sign, and Cato's reversal relied on a bound its author later withdrew. Corrected wordings are given per study. [SOURCE/INFERENCE tags per section]

---

## 1. Light, He & Robey 2020, PNAS 117(51), doi:10.1073/pnas.2014704117

### 1.1 Repo claim
- `research/immigration-crime-rates-unauthorized-vs-native-born.md:37-48` — ">2x violent, 2.5x drug, >4x property"; "Results robust to: alternative population estimates, alternate undocumented classification…"; claims table rows 1–2 rated HIGH / VERIFIED (lines ~237–238).
- `research/immigration-confidence-ladder.md:589` — "DIRECTION … strong"; raw 2018 violent undocumented 104 vs native 231 per 100k; "Use the sign, not the multiplier."
- Ladder entry 144 (`:219`) — cost-weighted ratio 0.40→0.43; "the undocumented row is robust, the legal row depends on the IDENT boundary."
- Load-bearing conclusion: unauthorized immigrants in Texas are arrested at well under half the native rate, and the direction is robust.

### 1.2 Data-capture pipeline (sign = effect on the undocumented/native ratio)
| Stage | Institution | What happens | Residual goes to | Sign of error on ratio |
|---|---|---|---|---|
| Event → arrest | local police, ~all Texas agencies | only detected, arrested felonies enter; each charge counted | — | deflate if undocumented victims/witnesses under-report (AER 2026 Gonçalves et al., victims not offenders) [SOURCE: bias memo row 20]; unknown for offender detection |
| Booking → CCH | jail, TCOLE-trained intake; DPS CCH | birthplace + citizenship **self-reported** at intake; missing in 3% of felony arrests [SOURCE: PNAS Methods "citizenship information is missing in only 3%"] | missing → unclear (not documented in main text) [GAP] | unknown |
| Status check | S-Comm/PEP: fingerprints → DHS IDENT; ICE returns "legal"/"illegal" **only for people with a prior DHS encounter** [SOURCE: PNAS Methods; DPS 2022 Border Crime Report quoted in `.brainstorm/2026-09-16-crime-stat-bias/research-classification.md:195-199`] | no IDENT record ⇒ no status | EWI never encountered + self-reports US birth ⇒ **"native-born"**; self-reports foreign-born noncitizen ⇒ **"legal immigrant"** (Light's rule: legal = DHS-legal + non-citizens not designated illegal + naturalized) | **deflate** (undocumented numerator down, native numerator up). Native denominator ~13× larger, so the undocumented rate moves far more [INFERENCE] |
| Later identification | TDCJ + DHS in prison | 11,000 people identified as unlawfully present only after prison entry; >50,000 charges, >27,000 convictions over their histories; DPS: activity "under represented" [SOURCE: DPS page quoted at research-classification.md:36-62] | whether Light's extract includes the TDCJ "prison" category is not stated in the main text [UNVERIFIED] | **deflate**, concentrated in serious offences (long terms ⇒ TDCJ investigation) |
| Exclusion | Light's coding | >39,000 bookings for "federal offenses", 70% undocumented, excluded as federal holds [SOURCE: PNAS Methods, fn ‖] | dropped | defensible (immigration holds are not state crime); small deflate if some carried state charges [INFERENCE] |
| Denominator | CMS residual (Pew alt.) | undocumented = foreign-born − imputed legal; legal immigrant = foreign-born − undocumented | residual | parity needs true undocumented pop <45% (violent) / <23% (property) of estimate [SOURCE: PNAS Sensitivity]; Fazel-Zarandi-type higher counts would **deflate** the rate further |

**The IDENT boundary is the weakest stage and the repo understates it.** Light's own extreme-case recoding (every noncitizen not DHS-"legal" counted as undocumented) moves total felony rates 2012–18 to **761 undocumented vs 1,046 US-born per 100k = 0.73** [SOURCE: PNAS footnote \*\*; CALCULATION 761/1046]. The headline total-felony ratio is ~400/1,000 ≈ 0.40 [SOURCE: PNAS Results "~1,000 … 400 per 100,000"]. So on one recoding the ratio nearly doubles, and that recoding still does not touch the other leak (undocumented arrestees who self-report as US citizens, which lands them in the native numerator). Nobody has bounded that second leak [SOURCE: bias memo §5, `research/immigration-crime-statistics-bias-mechanisms-2026-09-16.md:58`]. The violent-only extreme case is in SI, not read [GAP].

**Timing (the Texas deflator).** CIS showed the 2015 illegal-immigrant homicide-conviction rate moving from 8% below to 20% above the state rate between a 2018 and a 2021 extract of the same year as identification accrued [SOURCE: CIS 2022 quoted at research-classification.md:88-93; Cato disputes CIS's extract, not the mechanism]. Consequence for Light: (a) if their status field includes back-filled identifications, later years are under-identified relative to early years, which by itself produces the "stable or decreasing" undocumented share that their trend test reports [INFERENCE]; (b) if it is PEP-at-booking only, the 11,000-person prison-identified stock is missing throughout. Either way the trend finding (Table 1, ADF tests) is exposed and the repo cites it at `:44` without this caveat.

### 1.3 Design and precision
Descriptive population ratio, universe of arrests, no sampling clusters. Uncertainty is entirely measurement: denominator (CMS vs Pew within 0.02 on the repo's replication, ladder 144) and classification (0.40 → 0.73 on Light's own recode). No pre-registration; outcomes reported across 4 aggregate + 7 specific offence categories, all same sign, so no sign of cherry-picking among outcomes [SOURCE: PNAS Fig. 2]. The repo replicated the 2018 violent ratio 0.4571 from openICPSR 124923 [SOURCE: bias memo §5].

### 1.4 Replication and critique
- Reproduced by this repo from the authors' package (ladder 589, entry 144) [DATA: `crime_tx_arrests_by_status`].
- CIS (Kennedy, Richwine, Camarota 2022) attacks the at-arrest classification of Texas data, primarily aimed at Cato; the mechanism applies to Light's native residual too [SOURCE: CIS 2022].
- No published comment in PNAS found [UNVERIFIED — not searched this pass].

### 1.5 Politicization signals
Funded by NSF #1849297 and NIJ 2019-R2-CX-0058; "no competing interest" [SOURCE: PNAS Acknowledgments]. Academic criminologists, not advocacy staff. The discussion goes beyond the tables: "our results suggest that undocumented immigrants pose substantially less criminal risk than native US citizens" and "clearly run counter to … strict immigration enforcement" [SOURCE: PNAS Discussion] — arrest rates are read as risk. The paper's own misclassification paragraph leads with the error direction that favours its result (citizens wrongly flagged as undocumented) before the opposite one. Mild.

### 1.6 Verdict — **MEASUREMENT RISK (direction: flatters the undocumented), OVERSTATED IN REPO on robustness**
No sign of fabrication: the repo reproduced the numbers from the public package. The sign is supported against the denominator attack. The magnitude is not: the classification boundary alone spans 0.40–0.73 on total felonies before the unbounded self-report leak.
- Repo text `:45` "Results robust to: … alternate undocumented classification" → **corrected:** "Under the authors' most extreme recoding (all noncitizens not DHS-legal counted as undocumented) the total felony rate rises to 761 vs 1,046 per 100k (0.73); the direction holds, the magnitude does not. Undocumented arrestees with no prior DHS encounter who self-report as US citizens remain in the native group and are unbounded."
- Claims-table row 2 confidence HIGH → **MODERATE on magnitude**.
- Ladder 144 "the undocumented row is robust" → "the undocumented row's sign is robust; its level depends on the IDENT no-match residual, which runs against the immigrant ratio."
- `:44` trend claim → add: "identification lag can generate a falling undocumented share mechanically."

---

## 2. Landgrave & Nowrasteh, Cato (Texas convictions 2013–2022; ACS incarceration, PA 994, 2025)

### 2.1 Repo claim
- `research/immigration-crime-rates-unauthorized-vs-native-born.md:81-89` (Study 4) — homicide conviction rate "approximately 26% lower"; "the underlying data (Texas DPS) is the same administrative dataset used by … PNAS study, and the findings are directionally consistent. Grade: [C2]".
- Ladder `:617` — "Conviction-margin UPGRADE … 2.2 vs 3.0/100k native (−26%), homicide being near-fully-reported and detection-resistant; **closes the 'arrests ≠ guilt' objection**."
- Memo `:151-165` and ladder `:589` — PA 994 ACS table: native 1,221, illegal 613, legal 319 per 100k (2023); race restriction ~50% → ~30%.

### 2.2 Pipeline
**Texas convictions (Cato).** Same capture as §1.2 with two harsher steps: (i) Cato uses the DHS field alone, so legal immigrants without an IDENT "legal" return go to native (Light: 37,000 DHS-only vs ~60,000 legal arrests in 2018) [SOURCE: PNAS Methods]; (ii) Cato relabels DPS's "unknown or other" as native-born by definition: "The only other category of people left is native-born Americans, so the 'unknown or other' category is identified herein as native-born Americans" [SOURCE: Cato PA text quoted at research-classification.md:210-214]. The residual is defined by measurement failure. Sign: **deflate** (undocumented numerator short; native numerator padded). Extract-date sensitivity: CIS 2015 homicide conviction −8% → +20% vs state rate between extracts; Cato disputes CIS's extract (46 vs 56 homicide convictions in 2018, two contradictory DPS emails) and denominator (CIS's own 1.94M Texas estimate gives 2.9 vs 3.0) [SOURCE: research-classification.md:88-135]. Net: the sign of the homicide gap is within the dispute range; −26% is not a stable number.

**ACS incarceration (PA 994).** Event → conviction → institution → ACS group-quarters sample (CAPI interview of sampled inmate, proxies allowed; not administrator records despite Cato's premise) [SOURCE: research-classification.md:395-410] → status **imputed** by a legal-first residual (Gunadi's method): legal if citizen, pre-1982 arrival, military, Cuba, benefits, public housing, licence, legal/citizen spouse; everyone else "illegal" [SOURCE: PA 994 method quoted at research-classification.md:430-442]. In prison, the spouse and housing criteria cannot fire (ACS GQ form drops relationship) and 12-month benefit items mostly cannot either ⇒ legal inmates fall into "illegal" ⇒ **inflates** the illegal incarceration rate (against Cato's conclusion) [INFERENCE on ACS D&M Ch. 6 §6.5]. Cato's 2017 admission that it "likely overestimate[s]" incarcerated illegal immigrants was dropped from the 2025–26 method text [SOURCE: Cato Immigration Brief 1]. The ACS GQ citizenship/birthplace item has never been separately validated in prisons [GAP, bias memo :52]. Direction of the self-report item in custody: unknown.

### 2.3 Design and precision
Descriptive. ACS GQ is a sample; PA 994 prints no standard errors for the illegal-immigrant incarceration rate in the table the repo quotes [UNVERIFIED — table not re-parsed this pass]. The 613 vs 626 "excluding Black" rise is inside plausible sampling noise for a small imputed cell [INFERENCE]. Texas convictions: universe counts, but homicide convictions for illegal immigrants are ~46–56 a year [SOURCE: Cato/CIS dispute], so ±10 convictions moves the rate ~20%; the −26% is a ratio of small counts with a disputed numerator.

### 2.4 Replication and critique
CIS 2022 critique of the Texas method and Cato's reply (above). Light, He & Robey 2020 criticise Cato's DHS-only legal coding [SOURCE: PNAS Methods]. No external critique of the ACS legal-first imputation applied to inmates found [SOURCE: research-classification.md:520-528].

### 2.5 Politicization signals
Cato is a pro-immigration libertarian institute; Nowrasteh is its immigration director and a public advocate. Not peer-reviewed. The Texas relabelling of "unknown/other" as native is a choice that favours the conclusion and is stated in the text. Symmetry: the repo accepted Cato's variable-meaning critique of Lott (§3) but grades Cato's own residual-relabelling as C2 "probably true given convergence" — convergence with Light is partly shared-pipeline, not independent confirmation [INFERENCE].

### 2.6 Verdict — Texas: **OVERSTATED IN REPO**; ACS: **MEASUREMENT RISK (imputation inflates illegal rate; custody self-report unvalidated)**
No sign of fabrication; the Texas numbers are DPS counts and the ACS table is from public microdata.
- Ladder `:617` "−26% … homicide being near-fully-reported and detection-resistant; closes the 'arrests ≠ guilt' objection" → **corrected:** "Cato's Texas homicide conviction rate (2.2 vs 3.0 per 100k) treats DPS's 'unknown/other' residual as native-born and uses at-arrest DHS matches only; the same year's rate moved from 8% below to 20% above the state rate as later identifications accrued (CIS, disputed). Homicide resists under-detection, not status misclassification, and prison-identified cases concentrate in serious offences. The sign of the homicide gap is not settled by this source."
- Memo `:88-89` "the underlying data … is the same … findings are directionally consistent. Grade: [C2]" → add: "shared data means shared classification error; agreement with Light is not independent corroboration."

---

## 3. Lott 2018, "Undocumented Immigrants, U.S. Citizens, and Convicted Criminals in Arizona" (CPRC / SSRN 3099992)

### 3.1 Repo claim
- `research/immigration-crime-rates-unauthorized-vs-native-born.md:97-120` — "serious possible immigration-status classification problem"; Assessment "[D4] — not usually reliable source (advocacy-adjacent)… outlier"; item 5 "Author context: Lott has a history of controversial methodological claims".
- Ladder `:617` — "the one reversing study (Lott AZ +142%) rests on a status-variable coding error **AZ DOC itself confirms**."

### 3.2 Pipeline
Event → conviction → ADC admission 1985–2017 → `CITIZEN` variable (7 categories), Lott uses "non-US citizen and deportable" as undocumented [SOURCE: Nowrasteh 2018-02-05, cato.org/blog/fatal-flaw…]. Lott says status comes from the **pre-sentencing report**, on guidance from the Arizona County Attorneys' Association (Bill Montgomery), and that LPRs are labelled deportable only after sentencing, so the category at admission is undocumented [SOURCE: Lott response, crimeresearch.org 2018-02; Lott report fn 7, prisonlegalnews.org mirror]. Nowrasteh: the category also contains deportable legal immigrants; ADC regulations determine "criminal alien" first, then illegal status; June 2017 stock: 38.3% of criminal aliens had ICE detainers [SOURCE: Cato 2018-02-05]. Denominator: Pew 2014 Arizona unauthorized ~325,000 (4.9%) [SOURCE: same]. Sign of the flag contamination: **inflates** the undocumented share by the LPR/visa share of "deportable" — Lott estimates 10.5–21%, reducing the 11.8% conviction share to 10.6%–9.3%, still +94% to +121% over population share [SOURCE: Lott response]. Nowrasteh's counter-estimate (4.3% max, below population share) rested on ICE detainers as an upper bound, which he then conceded in a note is "much more likely to be an undercount" [SOURCE: Cato 2018-02-05, note on Dara Lind].

### 3.3 Design and precision
Descriptive share-of-admissions vs share-of-population, 32.5 years, not peer-reviewed. Lott claims no sampling error ("entire universe"). The real uncertainty is the flag meaning; neither side published the ADC codebook definition [GAP]. Lott's +142% is a ratio of shares with a residual (Pew) denominator, same class as Light's.

### 3.4 Replication and critique
Critiques: Cato (2 posts), WaPo Fact Checker 2018-03-21, Latino Decisions. Rebuttal: Lott 2018-02-06 and fn 7 of the report. No independent reanalysis of the ADC file exists [SOURCE: memo claims-table row 6 already says so].

### 3.5 Symmetry test — **FAILS**
| Test | Arizona (Lott) | Texas (Light, Cato) |
|---|---|---|
| Status flag produced by | ADC / pre-sentence report; ICE detainer | DHS IDENT match at booking |
| Documented contamination | legal "deportables" in the undocumented flag (inflates) — size estimated 10–21% by Lott, unknown by Cato | never-encountered undocumented in native/legal (deflates) — floor 11,000 prison-identified; unbounded self-report leak |
| Critic's own bound | Cato's 4.3% max withdrawn as a max (detainers undercount) | Light's own recode moves 0.40 → 0.73 |
| Repo treatment | "D4", "outlier", "fatal"-adjacent, author reputation cited, "AZ DOC itself confirms" | "robust", HIGH/VERIFIED, "the undocumented row is robust" |

Both flags are agency-produced status fields with a documented residual problem running in opposite directions. The repo discounted Arizona to near zero and kept Texas at HIGH. The critique that would put Lott in the "sign contested" bin puts Cato's Texas homicide conviction number in the same bin. The author-reputation item (memo `:114`) is an ad hominem that the repo does not apply to Cato's advocacy role. The ladder's "AZ DOC itself confirms" has no source in the repo: the memo cites Cato, WaPo and Latino Decisions, not ADC [SOURCE: memo :104-110; `rg` of repo found no ADC statement] — WaPo was not re-read this pass [UNVERIFIED].

### 3.6 Verdict on Lott — **MEASUREMENT RISK (direction: inflates undocumented share by the legal-deportable fraction), not DO NOT RELY**; repo treatment **OVERSTATED**
No sign of fabrication; the ADC file came from the same criminologist source Cato used. The contamination Cato identified is real in kind but, on the only published bound, too small to reverse the sign; Cato's reversal used a bound its author withdrew.
- Ladder `:617` "the one reversing study (Lott AZ +142%) rests on a status-variable coding error AZ DOC itself confirms" → **corrected:** "Lott's Arizona result (+142%) uses an ADC 'non-US citizen and deportable' flag that includes some deportable legal immigrants; the size of that share is disputed (Lott: 10–21%, leaving +94% to +121%; Cato's reversal rested on ICE detainers its author later called an undercount). No ADC statement confirming a coding error is on file."
- Memo `:114` author-context item → drop, or apply the same line to Cato.
- Memo `:116` "[D4] … doubtful information" → "[D3] … possibly true, status flag contaminated in the inflating direction by an unknown share; not peer-reviewed; no independent reanalysis."

---

## 4. Gunadi 2019/2021, Oxford Economic Papers 73(1):200–224, doi:10.1093/oep/gpz057

### 4.1 Repo claim
Memo `:50-61` and claims-table row 3 (`:239`): "Undocumented immigrants are 33% less likely to be institutionalized … despite possessing demographic characteristics usually associated with higher crime"; MODERATE / VERIFIED. Also the source of the imputation rule Cato uses in PA 994 (§2).

### 4.2 Pipeline
Event → conviction → any institutional group quarter (ACS "institutionalized": prisons, jails, but also nursing homes, psychiatric and other institutions) → ACS GQ sample, inmate/proxy CAPI → nativity and citizenship self-report → **legal-first residual**: legal if citizen, early arrival, benefits, military, government job, public housing, Cuban, licensed occupation, legal/citizen spouse; remainder = undocumented [SOURCE: abstract, ideas.repec.org; method as restated by Cato WP 60, cato.org/…/working-paper-60.pdf]. Two opposite errors:
- Inside institutions the spouse, housing and most benefit criteria cannot fire, so legal inmates fall into "undocumented" ⇒ **inflates** the undocumented institutionalization rate (makes the 33% conservative) [INFERENCE, same mechanism as §2.2].
- Undocumented people convicted and then removed, or held in ICE custody, leave the resident stock; whether ICE detention facilities are coded as correctional GQ in ACS was not checked ⇒ possible **deflate** through deportation censoring (Butcher–Piehl logic) [UNVERIFIED].
- The ACS GQ citizenship/birthplace item is unvalidated in custody [GAP, bias memo :52].

### 4.3 Design and precision
The institutionalization comparison is descriptive with covariates; the abstract's "despite possessing characteristics" suggests a demographic-adjusted estimate but the specification and its standard error were not read [UNVERIFIED — full text not fetched: `fetch_paper` failed; corpus lookup by DOI empty, although the memo's search log says it was read via `read_paper`]. The state-panel IV (crime rates not significantly increased) is a separate, area-level estimand and its instrument was not inspected.

### 4.4 Replication and critique
Method reused by Cato (WP 60, PA 994, BP 198). No published critique of the legal-first imputation applied to institutionalized respondents found (bias-memo sweep) [SOURCE: research-classification.md §4b].

### 4.5 Politicization signals
Academic economist, peer-reviewed field journal; no advocacy tie found in this pass. Cato's adoption of the method is Cato's, not Gunadi's.

### 4.6 Verdict — **SOUND BUT IMPRECISE (measurement risk runs both ways; not read in full this pass)**
No sign of fabrication. Repo wording is acceptable if "institutionalized" stays literal. Add to row 3: "status imputed by a legal-first residual that misfires inside institutions (inflating the undocumented rate) while deportation removes convicted undocumented people from the stock (deflating it); net sign unknown."

---

## 5. Ousey & Kubrin 2018, Annual Review of Criminology 1:63–84, doi:10.1146/annurev-criminol-032317-092026

### 5.1 Repo claim
Memo `:63-79`, claims-table rows 4–5: overall r = −0.031, CI −0.055 to −0.003; longitudinal −0.147, cross-sectional 0.000, small units −0.073, etc.; HIGH / VERIFIED. Memo itself says "Macrosocial units only — cannot speak to individual-level offending" (`:78`).

### 5.2 Pipeline
51 studies, 543 effect sizes, 1994–2014, "immigration-crime research focused on macrosocial (i.e., geospatial) units" — neighbourhoods, cities, MSAs, counties; exposure = immigrant share or change in it; outcome = area crime rates (UCR-type offences known to police, some homicide) [SOURCE: Annual Reviews abstract and text, verbatim above]. No study is individual-level; none measures legal status. Area crime counts include offences by natives, and immigrant inflows can change natives' behaviour and police recording. So the estimand is "areas with more immigrants have ≈ the same crime", which says nothing about the offending rate of immigrants versus natives (ecological fallacy either way) [INFERENCE].

### 5.3 Design and precision
Overall estimate verified verbatim: −0.031, p = 0.032, 95% CI −0.055 to −0.003 [SOURCE: Annual Reviews full text]. Significant between- and within-study heterogeneity (variance components 0.008, 0.013). Moderator values in the repo (−0.147 longitudinal etc.) came from an `ask_papers` synthesis, not a parsed table [SOURCE: memo `:67`, search log]; in a meta-regression these may be coefficients rather than subgroup means [UNVERIFIED]. Correlation-scale pooling across regressions with different controls is crude but standard.

### 5.4 Replication and critique
Consistent with later macro reviews (e.g. Marie & Pinotti 2024 JEP reconciling offender over-representation in Europe with null area effects, cited at ladder `:617`) [SOURCE: repo]. No critique alleging data problems.

### 5.5 Politicization signals
Kubrin is a prominent public voice on the "immigrants do not raise crime" side [INFERENCE — not sourced this pass]; the meta-analysis itself is transparent and reports a near-zero effect rather than a strong one. No signal that the abstract overstates the tables.

### 5.6 Verdict — **SOUND for its estimand; cannot speak to individual offending by status**
No sign of fabrication. The repo already scopes it correctly at `:78`. Risk is downstream reuse: any sentence that cites r = −0.031 next to status-specific rates should say "area-level association, all immigrants, not offending rates". Moderator numbers need table verification before reuse.

---

## Summary table

| Study | Repo use | Weakest pipeline stage | Precision | Politicization signal | Verdict |
|---|---|---|---|---|---|
| Light, He & Robey 2020 (PNAS) | TX undocumented arrests <½ native; "robust"; ladder 144, 589 | IDENT no-match: never-encountered undocumented filed as native or legal; prison-identified stock | universe counts; classification spans 0.40–0.73 (authors' own recode, total felonies); self-report leak unbounded | NSF/NIJ funded; discussion reads arrests as "risk" | MEASUREMENT RISK (flatters undocumented); robustness OVERSTATED IN REPO |
| Landgrave & Nowrasteh / Cato TX + PA 994 | homicide conviction −26% "closes arrests≠guilt"; ACS 613 vs 1,221 | TX: "unknown/other" relabelled native; extract date moves 2015 rate −8% → +20%. ACS: legal-first imputation misfires in custody | ~50 homicide convictions/yr; ACS cell SEs not printed | advocacy institute, not peer-reviewed; relabelling favours conclusion | TX: OVERSTATED IN REPO. ACS: MEASUREMENT RISK (inflates illegal rate) |
| Lott 2018 (Arizona) | discarded as "D4 outlier"; ladder "AZ DOC itself confirms" coding error | "non-US citizen and deportable" includes some deportable legal immigrants | share ratio; contamination 10–21% (Lott) leaves +94–121% | CPRC gun-rights advocacy; not peer-reviewed | MEASUREMENT RISK (inflates undocumented); repo dismissal OVERSTATED; symmetry test fails |
| Gunadi 2019/21 (OEP) | undocumented 33% less likely institutionalized | ACS GQ status imputation + deportation censoring | SE not read | none found | SOUND BUT IMPRECISE (net sign of error unknown) |
| Ousey & Kubrin 2018 | r = −0.031 | area-level exposure, not individual/status | CI −0.055 to −0.003 verified; moderators unverified | author public stance (unsourced); results modest | SOUND for area-level estimand only |

## Coverage
- **Done:** all five studies. Light read in full from corpus (`/Users/alien/Projects/corpus/doi_10_1073_pnas_2014704117/…/page.md`). Cato Lott critique read in full (cato.org, 2018-02-05); Lott rebuttal and report fn 7 read from search extracts (crimeresearch.org; prisonlegalnews.org mirror); Ousey–Kubrin abstract and main-effect paragraph read verbatim. Texas timing, Cato PA 994 imputation and ACS GQ evidence reused from `.brainstorm/2026-09-16-crime-stat-bias/research-classification.md` (primary quotes there), not re-fetched.
- **Not reached / partial:** Light SI (violent-only extreme recode, misdemeanour and conviction figures, whether status includes TDCJ "prison" category) [GAP]; PA 994 tables not re-parsed (repo's 1,221/613/891/626 taken as quoted) [GAP]; Gunadi full text (fetch failed; OUP paywall; author's pre-publication PDF link exists on sites.google.com/view/christian-gunadi) [GAP]; WaPo fact check body not retrievable (metered; scrape returned no text), so the ADC position on the flag is unverified [GAP]; Ousey–Kubrin Table 2 moderators not parsed [GAP].
- Budget: brief set 12 turns; this pass used ~18 to reach Studies 4–5.
- **Next queries if re-dispatched:** Light SI PDF from pnas.org supplementary (`pnas.2014704117.sapp.pdf`) for violent extreme-case and status-field definition; Gunadi pre-publication PDF from author site; PA 994 Table 1 parse; WaPo via archive.org `id_` capture.
