claude-opus-5-5[1m]

**Verdict:** None of the six studies shows any sign of fabricated or unreproducible data. Pinotti, Baker, Freedman–Owens–Bohn and Gunadi all use public or archived data or ship replication files. The problem is how ladder entry 49 uses them.

- **Freedman–Owens–Bohn (FOB) does not support the half of the claim the ladder assigns to it.** The ladder says "job access ↑ for legalized → crime↓", but FOB's legalization-phase (IRCA enactment) estimate for income-generating crime is 0.003 [SE 0.007], a null. The study's actual finding is that losing access to legal work raised felony charges against Hispanic residents of immigrant neighbourhoods. That is an enforcement-raises-crime result, and it contradicts the entry's own headline, "enforcement ≈ NULL on crime".
- **Pinotti is well identified but its "halves serious crime" figure is a point estimate.** The parametric 2SLS estimate is −0.006 (SE 0.003) on a 1.1% base, giving a 95% interval of roughly −1.2 to 0.0 percentage points (about −109% to 0% of the base). The whole effect comes from applicants sponsored through what are likely fictitious domestic-worker job offers. The estimate cannot separate reduced offending from the effect of expulsions.
- **Baker holds as the author states it (3–5%, mainly property crime).** It is a county-level estimate on imputed UCR county data, and its standard errors were not parsed in this pass.
- **Miles–Cox is sound and was independently replicated.** Its null appears only once county-specific trends are controlled. Without them the estimate is a significant −4%.
- **Gunadi's incarceration null is informative, but its property-crime result should not be relied on as causal.** The same 51-state panel produces a murder effect of −6.8% per approved application per 1,000 people. That implies about 340 murders averted per 100,000 DACA recipients per year, which cannot be a behavioural effect.
- **Bersani & Pittman's numbers match the paper.**

The single most consequential problem is that, once FOB's null legalization-phase estimate is read correctly, **the US evidence that legalization reduces crime rests on one ecological county-UCR study (Baker)**, and the entry's "enforcement ≈ null" headline is contradicted by one of its own three sources.

Scope: ladder entry 49 (`research/immigration-confidence-ladder.md:619–621`) and the verdict and table of `research/immigration-generational-crime-mechanisms-2026-09-16.md`.

---

## 1. Baker 2015, AER P&P 105(5):210–13, DOI 10.1257/aer.p20151041

**Repo claim.** `immigration-confidence-ladder.md:621`: "Legalization↓crime: Baker (IRCA, −3-5%, property)". This is one of three legs of "Legalization REDUCES crime via the labor-market (jobs) channel", rated medium-strong.

**What was read.** The AER P&P PDF and the SSRN WP 1829368 were both blocked (AEA returned HTML, SSRN returned a "Content Blocked" page, and Sci-Hub/OA fetch failed). Read instead:
- the author's LSE blog summary of the AER P&P paper (LSE eprint 63547) [SOURCE];
- the SSRN abstract (2014 WP: "decreases in crime of 2%-6%", 80,000–240,000 crimes a year) [SOURCE];
- the openICPSR replication deposit e113380 (abstract: "3-5 percent", 120,000–180,000 crimes a year) [SOURCE: doi 10.3886/e113380].

The core specification, in the author's words: "Regressing logged crime per capita on the cumulative number of county-level IRCA legalizations per capita, I find an approximate 4.5 percent decline in crime associated with 1 percent of a county's population being legalized … significantly smaller effects for violent crimes and larger effects when restricting to property crimes." [SOURCE: LSE eprint 63547]

**Data-capture pipeline.**

| Stage | Institution | Likely error on the headline |
|---|---|---|
| Offence, then victim report to police | local agency | Under-reporting. The sign on the estimate is ambiguous: if newly legal immigrants report *more* crime after IRCA (a reporting effect Gunadi invokes for DACA, fn 38), the measured decline is **understated**. |
| Agency submits UCR Return A | agency, then FBI | Agency non-reporting is common in 1980s UCR [TRAINING-DATA: Maltz & Targonski 2002, J. Quant. Criminol. 18(3):297–318]. |
| Aggregation to county | NACJD/ICPSR county files | Pre-1994 county files impute missing agency-months with a crude ratio and were flagged as unreliable for county panels (same Maltz & Targonski source) [TRAINING-DATA]. The error is noise that may be correlated with county size or urbanicity. IRCA-heavy counties (LA, Cook, Harris) are large agencies with better reporting, so the direction is unknown [INFERENCE]. |
| Treatment: INS legalization applications by county | INS (LAPS) | Counts are recorded at the applicant's county. Fraud in SAW applications inflated counts in agricultural areas, and fraudulent applicants were not a newly legalized population. Effect on the headline: attenuation [INFERENCE]. |
| Denominator: county population | Census | Undercount of the undocumented population before 1990 [INFERENCE]. |

Ecological design means the outcome is total county crime. It cannot distinguish applicants' own offending from native responses.

**Design and precision.**
- Identification comes from the timing of IRCA and cross-county intensity of legalizations.
- The number of clusters and the confidence intervals were **not parsed** [GAP].
- The headline moved across versions: 2–6% (2014 WP), 3–5% (published).

Plausibility arithmetic [CALCULATION, inputs from the author's summary and my own approximations]:
- 120,000–180,000 fewer crimes a year across about 2.7 million legalized people is 0.044–0.067 reported index crimes averted per legalized person per year.
- The late-1980s US reported index-crime rate was about 0.057 per resident per year [TRAINING-DATA, approximate].
- So legalized people would have had to stop committing roughly the average American's entire reported per-capita crime volume.
- That is possible only if this group offended above the population average before IRCA, or if the effect includes spillovers onto others. It sits uneasily with the repo's own finding that first-generation immigrants offend below natives (ladder 42/48). This is a plausibility flag, not a refutation.

**Replication and critique.** No published comment or reanalysis found. FOB (study 3) is the closest test, and it finds the IRCA enactment phase null for income-generating crime in San Antonio.

**Politicization signals.** None found. The author is a finance economist with no advocacy ties found. The blog summary matches the abstract.

**Verdict: SOUND BUT IMPRECISE, with MEASUREMENT RISK of unknown sign** (pre-1994 imputed county UCR, ecological design). The repo's "−3-5%, property" matches the author's framing. It should add "per 1% of county population legalized; county-level, cannot isolate applicants' behaviour". No sign of fake data; a replication deposit exists.

[GAP] Parse the AER P&P table (clusters, SEs, and whether the county UCR series is imputed or restricted to fully reporting agencies). Route: openICPSR e113380 README, or the AEA PDF through an institutional route.

---

## 2. Pinotti 2017, AER 107(1):138–68, DOI 10.1257/aer.20150355

**Repo claim.** `immigration-confidence-ladder.md:621`: "Pinotti (Italy click-day RD, halves serious crime — best-identified)". `immigration-generational-crime-mechanisms-2026-09-16.md:46` uses it to support the opportunity-cost channel.

**What was read.** CReAM DP 25/16 (October 2016, the pre-publication version of the AER paper). I read the full text as crawled, including Tables 3 and 4, §4.2.3 on measurement error, and the tables by type, offence and sponsor [SOURCE: cream-migration.org/publ_uploads/CDP_25_16.pdf]. The published AER tables were not compared line by line [GAP].

**Data-capture pipeline.**

| Stage | Institution | Likely error on the headline |
|---|---|---|
| Serious offence (robbery, theft, drug trafficking, smuggling, extortion, kidnapping, murder, rape) | victim or police | Unreported crimes are missing. If under-reporting is symmetric between legal and irregular immigrants, the gap is scaled down, not biased [SOURCE: §4.2.3]. |
| Police report ("reported for having committed a serious crime") | Italian police (Ministry of Interior restricted data) | These are police charges, not convictions. 82% of offenders were arrested in flagrante, and the result holds on that subset (Table 5 col 7) [SOURCE]. |
| Linkage to Click Day applicants | author and Ministry of Interior | Matched on **name, surname, nationality and year of birth**. Irregular immigrants have no biometric record, so they can use aliases and escape the match (false negatives). Legalized immigrants are fingerprinted, so they are *easier* to match. This pushes *against* finding a decline, making the estimate conservative on this channel [SOURCE: §4.2.3 plus inference]. |
| Exit from Italy (expulsion or emigration) | not observed | "It is impossible to separately identify" reduced offending from differential expulsion [SOURCE: intro]. Denied applicants are *more* at risk of expulsion, which would remove them from the Italian crime records and bias the estimate **toward zero**. Legalized immigrants re-entering from their home country for a visa is addressed in the paper and ruled out [SOURCE]. |
| Denominator | 110,337 male applicants within one hour of the cutoff | Complete for the application universe. |

**Design and precision.**
- Regression discontinuity (RD) on the millisecond of application. The 2007 placebo (the year before) is zero: −0.000 (0.002).
- Parametric Table 3, all applicants: reduced form −0.003* (0.002), significant **at 10% only**. 2SLS −0.006* (SE 0.003), 95% CI ≈ −0.0119 to −0.0001, i.e. −108% to −1% of the 1.1% base [CALCULATION].
- With lottery fixed effects and clustering (col 4): −0.006 (0.004), **not significant**.
- Non-parametric Table 4: −0.008** (0.004) and −0.010** (0.005) under CCT bandwidths.
- "55 percent of the baseline" is the point estimate.
- **The whole effect is in type-A applicants** (domestic-worker sponsorship; base rate 1.8%): 2SLS −0.013 (0.005). Type B (firm-sponsored, real job offers) is 0.000 (0.005).
- The paper argues type-A male applicants are largely unemployed people with fictitious job offers. 38% share the sponsor's nationality and 21% share the sponsor's surname (Ministry of Interior 2009).
- Within type A, the effect is on economically motivated crime (−0.009**), not violent crime (−0.002). It is present when the sponsor is foreign (−0.015**) but not significant when the sponsor is native (−0.008).
- Several heterogeneity cuts are reported. Main results are stable across polynomial orders 0–6 and bandwidths of 1–30 minutes, and a permutation placebo is reported. No pre-registration.

**Replication and critique.** A ReplicationWiki entry exists and AER posts replication files. No published comment found. The companion paper, Mastrobuoni & Pinotti 2015 (AEJ: Applied), on the 2007 EU enlargement and pardoned inmates, finds a 50% fall in recidivism, which is consistent.

**Politicization signals.** None found. The abstract ("0.6 percentage points … on a baseline crime rate of 1.1 percent") matches Table 3. Symmetry check: the repo accepts police-charge outcomes here. It does not reject the same outcome type elsewhere, though it does downgrade arrest-based comparisons when used against immigrants (ladder 48 "arrests ≠ guilt"). Pinotti's in-flagrante restriction answers that objection better than most studies.

**Verdict: SOUND BUT IMPRECISE; OVERSTATED IN REPO.**

Repo text: "halves serious crime — best-identified". Corrected wording: "Italian 2007 click-day RD: legal status cut the one-year police-reported serious-crime rate of male applicants by 0.6 pp on a 1.1% base (95% CI about −1.2 to 0.0 pp; about −55% at the point estimate). The effect is concentrated in applicants sponsored through likely fictitious domestic-worker offers (−1.3 pp on 1.8%) and zero for firm-sponsored applicants. It includes any expulsion channel. Best-identified design; imprecise size; Italian undocumented population."

No sign of fake data.

---

## 3. Freedman, Owens & Bohn 2018, AEJ: Economic Policy 10(2):117–51, DOI 10.1257/pol.20150165

**Repo claim.** `immigration-confidence-ladder.md:621`: "Freedman-Owens-Bohn (IRCA's dual structure — job access ↑ for legalized → crime↓, but employer-sanctions side cut job access for recent arrivals → crime↑)". The ladder's caveat, "enforcement that strips work access can be criminogenic", also cites it. The citation is the correct paper. The DOI matches the San Antonio (Bexar County) study.

**What was read.** The accepted manuscript, 58 pp: Table 2 (all panels), Table 3, the main-results text and footnote 44 [SOURCE: faculty.sites.uci.edu FreedmanOwensBohn_Manuscript.pdf].

**Data-capture pipeline.**

| Stage | Institution | Likely error on the headline |
|---|---|---|
| Alleged felony | Bexar County police, then DA | These are felony **charges** (by offence date), not convictions. |
| Ethnicity of defendant | court record | "Hispanic" is the treatment proxy. There is **no immigration status or nativity field**: "the immigration status of people who violate state laws is generally not collected by local authorities". Most Hispanic defendants are US-born, so measured effects are diluted. The sign is toward attenuation of the per-immigrant effect [SOURCE plus inference]. |
| Residence to block group | geocoded court address | An "immigrant destination index" (poverty, % Mexican, % foreign-born, persons per unit, % Spanish at home) proxies the likelihood that a Hispanic resident is a recent immigrant. Poverty is in the index, so the index also picks up anything that hit poor Hispanic neighbourhoods in 1988 [INFERENCE]. |
| Offence type | charge code | The result is **drug-led**: drug triple-diff 0.047*** vs 0.037*** for income-generating crime. Drug charges depend on enforcement. The 1986 Anti-Drug Abuse Act took effect in the same window (the authors' fn). They test for a policing shift through conviction rates (Table 5) and non-Hispanic minorities (Panel D). |
| Denominator | estimated ethnicity-specific block-group population | Unknown flow of unauthorized arrivals after IRCA. The authors bound it with "extreme population" assumptions (Table 3 col 2, 0.054** vs 0.038* baseline). |

**Design and precision.** Triple difference: Hispanic × destination index × IRCA phase. 1,000 block groups, monthly, April 1985–December 1989. SEs are clustered by block group (1,000 clusters), with permutation p-values reported.

| Coefficient | Income-generating | Non-income | Drug |
|---|---|---|---|
| Index × **IRCA enactment** (legalization phase) | **0.003 [0.007], p 0.677** | −0.012** | +0.008* |
| Index × **LAW expiry** (employer sanctions bind) | **0.037*** [0.011]** | 0.007 | 0.047*** |
| Index × SAW expiry | −0.004 | 0.001 | −0.008 |

[SOURCE: Table 2 triple-difference column]

The **legalization phase shows no decline in income-generating crime.** The only significant enactment coefficients are a small decline in non-income crime and a small *increase* in drug crime. Everything the paper establishes concerns the loss of work access after May 1988: about +14% income-generating charges at +1 SD of the index, or about 142 extra charges a year countywide (fn 44). The authors themselves say the result changed newly arrived undocumented immigrants "from a relatively low-risk group to a moderate-risk one".

**Replication and critique.** AEJ replication package. Bohn, Freedman & Owens 2015 on police behaviour during IRCA supports the no-policing-shift reading. No independent reanalysis found.

**Politicization signals.** None. The abstract matches the tables and does not claim a legalization-lowers-crime result. Symmetry check: the repo accepts a **Hispanic-ethnicity proxy** for immigrant status here, while ladder 51 and the classification memos treat ethnicity-based coding as a known measurement bias when it cuts the other way. Grade the proxy the same both ways.

**Verdict: OVERSTATED IN REPO.**

Repo text: "job access ↑ for legalized → crime↓". Corrected wording: "Freedman–Owens–Bohn (San Antonio felony charges, 1985–89): IRCA's legalization phase had no detectable effect on income-generating charges against Hispanic residents of immigrant-destination neighbourhoods (0.003, SE 0.007). After the amnesty deadline, when employer sanctions barred new arrivals from legal work, such charges rose about 14% at +1 SD of the destination index, led by drug felonies. Immigrant status is proxied by ethnicity plus neighbourhood; the outcome is charges."

FOB also contradicts entry 49's headline "enforcement ≈ NULL on crime". It should read "deportation screening of arrestees ≈ null; employment-based enforcement raised charges (one county)". No sign of fake data.

---

## 4. Miles & Cox 2014, J. Law & Econ. 57(4):937–73, DOI 10.1086/680935

**Repo claim.** `immigration-confidence-ladder.md:621`: "Enforcement≈null on crime: Miles-Cox Secure Communities (landmark)". The headline generalizes this to "enforcement ≈ NULL on crime".

**What was read.** The author-posted August 2014 draft, §5.A, the Table 2 detention-elasticity text and §5.D [SOURCE: antoniocasella.eu/nume/Miles_Cox_2014.pdf, via Exa highlights]. The JLE full text was paywalled. Tables were not parsed in full [GAP].

**Data-capture pipeline.**

| Stage | Institution | Likely error on the headline |
|---|---|---|
| Outcome: FBI index crime | UCR agency reports aggregated to county-month | Same agency non-reporting issues as Baker, but 2008–2012 reporting is better. Noise, attenuating [INFERENCE]. |
| Treatment: Secure Communities activation date | ICE rollout schedule | Rollout was not random: ICE prioritized border and high-immigrant counties first. This drives the trend sensitivity below. |
| Detentions: county-month counts of detainees | ICE via FOIA | A good intensity measure. It counts detentions, not removals of active offenders. |
| Mechanism | — | Secure Communities acts on **people already arrested**, so the incapacitation gain is limited to those who would not otherwise have been jailed. |

**Design and precision.**
- Staggered difference-in-differences across more than 3,000 counties.
- **Without county-specific trends: a statistically significant 4% decline in index crime**, concentrated in high foreign-born counties.
- With county trends, the effect goes to zero. The elasticity with respect to detentions moves from −0.0163 to −0.0006, and "a coefficient as small as .009 would be statistically significant", so the null with trends is precise [SOURCE].
- "Modest declines" appear in burglary and motor-vehicle theft in some specifications [SOURCE].
- The verdict therefore depends on one specification choice (county trends). It is a defensible choice given the non-random rollout, but it is a choice.

**Replication and critique.**
- Treyger, Chalfin & Loeffler 2014, *Criminology & Public Policy*, DOI 10.1111/1745-9133.12085: an independent city-level analysis, also null on crime and on arrest patterns [SOURCE: abstract].
- Hines & Peri (Secure Communities, crime null) are known but not re-read here [UNVERIFIED].
- Miles–Cox criticize Chalfin et al.'s city/county mismatch.

**Politicization signals.** Both authors are law professors, and Cox has an immigration-law scholarship profile. The WP abstract's "the program has not served its central objective of making communities safer" is a policy conclusion slightly stronger than "no detectable effect with county trends". The −4% no-trend estimate is reported openly in the body [SOURCE]. No sign of fake data.

**Verdict: SOUND for the study; OVERSTATED IN REPO as generalized.**

Repo text: "enforcement ≈ NULL on crime". Corrected wording: "Deportation screening of people already arrested (Secure Communities 2008–12) had no detectable effect on county index crime once county trends are controlled (elasticity −0.0006; a −4% no-trend estimate disappears with trends); a city-level replication is also null. This does not cover employment-based enforcement, which FOB finds raised charges."

---

## 5. Gunadi 2020, J. Econ. Behav. & Org. 178:327–53, DOI 10.1016/j.jebo.2020.07.033

The repo's DOI suffix is not given. The correct suffix is .033, not .030.

**Repo claim.**
- `immigration-generational-crime-mechanisms-2026-09-16.md:69`: "I fail to find evidence that DACA statistically significantly affected the incarceration rate…; one DACA approval per 1,000 population is associated with a 1.6% fall in property crime".
- Line 28: "DACA … has no detectable effect on incarceration of the eligible".
- Line 46: "matches … Gunadi's DACA property-crime result … which points to opportunity cost rather than fear".

**What was read.** The 61-page working-paper version: Tables 2 and 4 and the pp. on data and results [SOURCE: read-me.org/s/does-immigrant.pdf].

**Data-capture pipeline.**

| Stage | Institution | Likely error on the headline |
|---|---|---|
| Incarceration | ACS institutional group quarters (GQ) | Institutionalization is a proxy for incarceration (men 18–35). The ACS GQ frame undercounts noncitizens in immigration detention and cannot tell jail from prison. The repo's crime-classification memo covers ACS GQ [SOURCE: memory; A_crime_levels scope]. |
| Undocumented status | ACS has no status field | Three proxies: noncitizen, Hispanic noncitizen, and Borjas 2017 residual imputation. Lawful noncitizens are in the "undocumented" cell, which attenuates any DACA effect [INFERENCE]. The results are consistent across all three proxies. |
| State crime | FBI UCR state totals | The outcome includes everyone's crime, not recipients' crime. |
| Treatment intensity | USCIS cumulative approvals by state | Clean administrative count. |
| Denominator | state population | — |

**Design and precision.**
- **Incarceration:** difference-in-differences, eligible × post = 0.000 (0.001) to −0.002 (0.002) on a base of 0.012–0.014, with SEs clustered by state. The 95% CI is about ±0.003–0.004, or ±25–30% of the base. This is an informative null, with proxy attenuation [CALCULATION].
- **State crime:** 51 states × 10 years = 510 observations, 51 clusters. OLS and two IVs (network IV with first-stage F 61.6; push IV with F 15.8).
- Property overall: OLS −0.027***, network IV −0.018***, push IV −0.016*.
- The same design produces **murder −0.068*** (network IV) / −0.087*** (push IV) and rape +0.070*** / +0.047*** per approval per 1,000** (Table 4 Panel A).

Plausibility [CALCULATION, pre-DACA means from Table 4]:
- Murder: −6.8% × 5.0 per 100,000 per 0.1% of population approved = 0.0034 murders averted per recipient per year, i.e. **340 per 100,000 recipients, about 68× the national murder rate**.
- Property: −1.6% × 3,071 per 100,000 = about 0.49 reported property crimes averted per recipient per year, **about 16× the national per-capita reported property-crime rate**, for a group whose institutionalization rate is at or below natives' (Table 1: 1.2–1.4%).
- The design is picking up state-level confounds, not recipients' behaviour. The author's own footnote 38 explains the rape increase as a reporting effect, which concedes the outcome moves for reasons other than offending.
- Many outcomes and specifications; no pre-registration.

**Replication and critique.** None found.

**Politicization signals.** The abstract says "associated with", but the conclusion draws a policy lesson ("policies that expand the employment opportunities of immigrants may reduce crimes"). The abstract does not report the implausible murder and rape coefficients. Symmetry check: the repo would reject an anti-immigration state-panel study with coefficients 68× the base rate, and it should apply the same standard here.

**Verdict:**
- **Incarceration null: SOUND BUT IMPRECISE**, attenuated by status proxies.
- **Property-crime result: DO NOT RELY** as causal evidence. The memo at line 69 quotes it accurately ("associated"), but line 46 uses it as corroboration of an opportunity-cost mechanism. Corrected wording for line 46: drop "Gunadi's DACA property-crime result" as support, or add "(state-panel association; the same design yields implausible murder and rape effects, so it is not evidence on recipients' behaviour)".

No sign of fake data.

---

## 6. Bersani & Pittman 2019, JRCD 56(6):851–87, DOI 10.1177/0022427819850600; and Inkpen 2024, Crime & Delinquency, DOI 10.1177/00111287231225125

**Repo claim.** Memo verdict (line 1) and table (lines 13–14): the first-to-second-generation rise is "a first-generation floor, not a second-generation ceiling".

**What was read.** Bersani & Pittman in full from the corpus copy (Marker parse): Table 1 and the dyad-difference table [SOURCE: corpus doi_10_1177_0022427819850600]. Inkpen was not re-read (Sage paywall). The memo reports results passages verified at source [UNVERIFIED this pass].

**Numbers check (Bersani & Pittman), all match the memo.**
- Total-crime prevalence: 26.73% / 49.25% / 53.18% for first / second / third-plus generation mothers (Table 1).
- First-generation mother to second-generation child difference: −.36, 95% CI (−.48, −.23); variety −1.34 (−1.76, −.96) [SOURCE].
- The memo writes the CI as ".23–.48", the sign-flipped absolute value, which is fine.

**Data-capture pipeline.**
- Self-reported offending, eight items.
- Mothers answered in NLSY79 1980 at ages 15–22. Children answered NLSY79-CYA items at 15+ in 1994/96/98.
- Different instruments, different decades (the early-1990s crime peak versus 1980), different modes.
- The dyad differences therefore carry a period and instrument confound that shifts **all** generations' dyad gaps. The authors acknowledge this (their Figure 2 "sociohistorical differences").
- The first-generation floor itself comes from the within-survey 1980 cross-section (26.7 vs 53.2), which the period confound does not touch.
- Generation is coded from maternal and grandparental birthplace. The size of the first-generation mother cell was not extracted [GAP]; NLSY79 foreign-born women are a small cell.
- The footnote that the low offending comes from mothers who migrated at 11 or older was confirmed in the memo, not re-checked here.

**Design and precision.** Descriptive: χ², ANOVA, OLS on difference scores. Single cohort. No causal claim. Self-report avoids police-contact bias. The repo's generational-bias memo already grades self-report as unbiased by generation, via Bersani & Piquero.

**Politicization signals.** The abstract's "decline in well-being across successive generations" is interpretive but matches the dyad tables. The authors are criminologists with no advocacy ties found.

**Verdict:**
- **Bersani & Pittman: SOUND BUT IMPRECISE** for the floor claim. There is **MEASUREMENT RISK** on the dyad (child-minus-mother) figures from the 1980 versus 1990s instrument confound, with unknown direction but common to all generations. The repo already grades it B+ with this caveat. Not overstated.
- **Inkpen 2024: not audited this pass** [GAP]; see Coverage.

---

## Summary

| Study | Repo use | Weakest pipeline stage | Precision | Politicization signal | Verdict |
|---|---|---|---|---|---|
| Baker 2015 | Ladder 49 leg: IRCA legalization −3–5% crime | Pre-1994 imputed county UCR; ecological outcome | CIs not parsed [GAP]; implied effect per legalized person large | None | SOUND BUT IMPRECISE + MEASUREMENT RISK (sign unknown) |
| Pinotti 2017 | Ladder 49: "halves serious crime — best-identified" | Unobserved expulsion (bias toward 0); alias-driven linkage misses (bias toward 0) | −0.6 pp (SE 0.3) on 1.1%; 95% CI ≈ −1.2 to 0.0 pp; all in type-A applicants | None | SOUND BUT IMPRECISE; OVERSTATED IN REPO |
| Freedman–Owens–Bohn 2018 | Ladder 49: "job access ↑ for legalized → crime↓" + employer-sanctions ↑ | Ethnicity proxy for status; drug charges enforcement-sensitive | Legalization phase 0.003 (0.007), null; LAW expiry +0.037 (0.011) | None; repo accepts an ethnicity proxy it rejects elsewhere | OVERSTATED IN REPO (legalization half absent; contradicts "enforcement ≈ null") |
| Miles–Cox 2014 | Ladder 49: "enforcement ≈ NULL" | Non-random rollout, so the result depends on county trends | Precise null with trends; −4% significant without | Abstract policy language a bit stronger than the estimate | SOUND; OVERSTATED IN REPO as generalized to all enforcement |
| Gunadi 2020 | Generational memo: DACA incarceration null; property −1.6% as opportunity-cost support | ACS GQ + noncitizen proxy; state-panel confounds | Incarceration ±25–30% of base; murder/rape coefficients implausible (68× base) | Policy conclusion beyond an association | Incarceration SOUND BUT IMPRECISE; property DO NOT RELY |
| Bersani & Pittman 2019 | Generational memo verdict: first-generation floor | Self-report; 1980 vs 1990s instruments for dyads | Dyad −.36 (−.48, −.23) | None | SOUND BUT IMPRECISE (dyads carry a period confound) |
| Inkpen 2024 | Generational memo: second generation regresses to the mean | not audited | — | — | NOT REACHED [GAP] |

**Fabrication check:** no signal in any study. Pinotti, FOB and Baker have AEA/openICPSR replication deposits. Gunadi uses public ACS, UCR and USCIS data. Miles–Cox detention data came from FOIA, and an independent replication (Treyger et al.) reaches the same null.

**Suggested replacement for ladder 49's reason line** (for the lead to apply; not edited here): "Legalization → lower recorded crime among the legalized: one well-identified but imprecise Italian RD (Pinotti: −0.6 pp on 1.1%, 95% CI ≈ −1.2 to 0.0 pp, concentrated in applicants with likely fictitious job offers, includes expulsion) and one US county-UCR estimate (Baker: 3–5% per 1% of population legalized, property-led). Loss of legal work access raised felony charges (Freedman–Owens–Bohn, San Antonio: +~14% income-generating charges at +1 SD of an immigrant-destination index, drug-led; the legalization phase itself null). Deportation screening of arrestees had no detectable crime effect once county trends are controlled (Miles–Cox; Treyger–Chalfin–Loeffler)." Suggested rating: `medium on direction for legalization; weak on US magnitude; enforcement result is program-specific`.

## Coverage

- **Done:** Pinotti (WP full text, Tables 3/4 and heterogeneity), FOB (manuscript Tables 2/3, results text), Gunadi (WP Tables 2/4), Bersani & Pittman (corpus full text, Table 1 and dyad table).
- **Partial:**
  - Baker: author summaries and abstracts only. The AER P&P PDF and SSRN are blocked and research-MCP fetch failed, so no SEs [GAP].
  - Miles–Cox: author draft highlights only; tables not parsed [GAP].
- **Not reached:** Inkpen 2024. It is paywalled, and the memo already reports a source verification of the results passages.
- **Not checked:** Hines & Peri Secure Communities; Maltz & Targonski is cited from training data.
- **Next queries if re-dispatched:**
  - openICPSR e113380 README and do-file for Baker's county UCR construction and clustering;
  - the JLE Miles–Cox Table 2 (antoniocasella PDF via curl + pdftotext);
  - Inkpen via Sage highlights or the author's page;
  - FOB Table 5 conviction-rate estimates for the policing-shift test.
