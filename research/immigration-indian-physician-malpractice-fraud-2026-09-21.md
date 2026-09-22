# Indian vs white physicians: malpractice, fraud, ranking

**Question:** What is the fraud and malpractice rate of Indian doctors versus white doctors, and how do they rank?
**Tier:** Standard | **Date:** 2026-09-21
**Ground truth:** ACS 2023 employed 25–64: 12.1% of US-born Asian Indians and 2.5% of India-born are physicians, vs 0.6% of US-born NH whites (`indian_generation_2026_09_21`). That is occupational share, not a claims rate.

Model: Cursor Grok 4.6. Instrument caveat: `notes/llm-bias-caveat.md`.

### Claims

| # | Claim | Evidence | Confidence | Status |
|---|---|---|---|---|
| 1 | No published US rate of malpractice payments or Medicare exclusions for Indian-origin vs White physicians | NPDB public file has no race or school country; AAMC race tables stop at Asian | High | VERIFIED as absent |
| 2 | US IMGs as a class do not have a higher *fraud* exclusion rate after adjustment (aOR 0.95) | Chen, Blumenthal, Jena 2018 | High for IMG lump, not India | VERIFIED |
| 3 | US IMGs have higher overall exclusion (aOR 1.30), driven by health-crime (1.62) and substance (1.34) codes, not billing fraud | Same | High | VERIFIED |
| 4 | National US malpractice payments 2004–08: IMGs vs USMGs, no significant difference | GAO-10-412 | Medium (old window; weak competence marker) | VERIFIED |
| 5 | Illinois: non-US schools ~higher paid-claim risk, not higher board discipline (Caribbean higher for negligence) | Hyman et al. JELS 2020; Indiana JELS 2021 | Medium | VERIFIED |
| 6 | Rankings exist for *country of medical school* in AU/UK complaints, not US malpractice | Elkin 2012; Mehdizadeh 2017 | High for those systems | VERIFIED |
| 7 | Medicare patients of US internist IMGs have slightly *lower* 30-day mortality | Tsugawa, Jena et al. BMJ 2017 | High for internists 2011–14 | VERIFIED |

[SCITE: tool unavailable this session]

### Key findings

**The US does not publish Indian vs White doctor malpractice or fraud rates.** The National Practitioner Data Bank public file has payments and adverse actions, not race, ethnicity, or country of medical school. [SOURCE: https://npdb.hrsa.gov/resources/publicData.jsp] AAMC’s active-physician race table is White 56.2% / Asian 17.1% (2018); it does not split Asian Indian. [SOURCE: https://www.aamc.org/data-reports/workforce/data/figure-18-percentage-all-active-physicians-race/ethnicity-2018] “Indian doctors” in the US mix India-trained IMGs and US-trained Indian-origin physicians. Those are different populations.

Stock, not a rate: FSMB 2017, **49,901** actively licensed physicians trained in India — **23% of IMGs**, **5.1% of 970,090** licensed physicians. Next IMG countries: Caribbean 18%, Philippines 6%, Pakistan 6%, Mexico 5%. [SOURCE: https://golive.ecfmg.org/echonews/issue47.html]

#### Malpractice (civil claims / paid NPDB)

GAO, national 2004–08: IMGs were a somewhat larger share of license revocations/suspensions than of the workforce; **not statistically significant**. Malpractice payments: “data on the whole suggest little difference.” GAO also notes malpractice is a **weak competence marker**. Florida showed a significant IMG excess of *revocations*. [SOURCE: https://www.gao.gov/products/GAO-10-412]

Illinois 1990–2016 (Hyman et al.): physicians from **non-US medical schools are more likely to have paid claims**, but (except high-discipline specialties) **not more likely to be disciplined**. A later Hyman/Black working paper puts foreign-trained paid-claim risk at about **1.2×** US-trained and flags that patients may sue foreign-trained doctors more readily. [SOURCE: https://doi.org/10.1111/jels.12277] [SOURCE: https://laweconcenter.org/wp-content/uploads/2022/07/SSRN-id3750392.pdf]

Indiana 1972–2015: US vs non-US school **same overall discipline risk**. Non-US: *lower* drug/alcohol/diversion, *higher* negligence and sexual misconduct. **Caribbean** higher for negligence/incompetence — **India is not the named outlier**. [SOURCE: https://doi.org/10.1111/jels.12292]

**No US ranking of India vs other school countries on malpractice.** Waters 2003 ranked *US* medical schools only. [SOURCE: https://doi.org/10.1136/qhc.12.5.330]

Specialty swamps origin. Paid-claim rates range several-fold by specialty (Schaffer et al. 2017, NPDB 1992–2014). Indian IMGs are concentrated in internal medicine / family medicine, not orthopedics/OB. Unadjusted “Indian vs White” would mostly be a specialty mix. [SOURCE: https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2612118]

#### Fraud (OIG exclusion / criminal billing)

Chen, Blumenthal, Jena, *JAMA Network Open* 2018: 2,222 physicians excluded 2007–17 (**0.29%** of US physicians). Relative to US graduates, **IMGs**:

| Outcome | Adjusted OR (95% CI) |
|---|---|
| Any exclusion | **1.30 (1.18–1.44)** |
| Fraud codes | **0.95 (0.83–1.09)** — not different |
| Health-crime codes | **1.62 (1.37–1.91)** |
| Substance/prescribing | **1.34 (1.04–1.73)** |

Male, older, DO, family medicine, and psychiatry predict exclusion more than IMG status. **No India row.** [SOURCE: https://doi.org/10.1001/jamanetworkopen.2018.5805]

Pande & Maas 2013: among physicians *convicted* of criminal Medicare/Medicaid fraud, **59% were IMGs** vs ~25% of the workforce. That is a selected convict sample, unadjusted for specialty/age/practice type, and **not India-specific**. Do not treat 59% as an India fraud rate. [SOURCE: https://doi.org/10.1108/17506121311315391]

Dow & Harris 2002 (family/GP only): non-OECD IMGs, if board-certified, RR **2.19** of federal exclusion vs USMGs. OECD IMGs matched USMGs. Old, one-specialty. [SOURCE: https://doi.org/10.1097/00005650-200201000-00009]

#### Rankings that do exist (not US malpractice)

These are **country of primary medical qualification** vs domestic graduates. They are not race, not White-US physicians, and not transferable to the US ECFMG/residency filter.

**Australia** (Elkin, Spittal, Studdert, *MJA* 2012; Victoria + WA; 39,155 doctors): complaint OR vs Australian-trained, adjusted for sex, years since qualification, location, registration type:

| Country of qualification | Complaint OR (95% CI) |
|---|---|
| Nigeria | 4.02 (2.38–6.77) |
| Egypt | 2.32 (1.77–3.03) |
| Poland | 2.28 (1.43–3.61) |
| Russia | 2.21 (1.14–4.26) |
| Pakistan | 1.80 (1.09–2.98) |
| Philippines | 1.80 (1.08–3.00) |
| **India** | **1.61 (1.33–1.95)** |
| UK/Ireland, NZ, SA, Germany, China, … | ns vs Australia |

India: 1,871 doctors (5% of register), 291 complaints (5% of complaints). Higher *rate*, not a volume spike. Adverse findings: IMGs overall OR 1.41; **underpowered by country**. Missing specialty. [SOURCE: https://doi.org/10.5694/mja12.10632]

**UK GMC performance assessments** (Mehdizadeh et al. 2017; 1996–2013). Crude assessments per 1,000 doctors on the 2013 register, and year-adjusted IRR vs UK (Wakeford’s table from the paper’s Fig. 7):

| Country | n on register | Assessments | /1,000 | IRR vs UK |
|---|---:|---:|---:|---:|
| Bangladesh | 874 | 23 | 26.3 | 13 |
| Egypt | 3,215 | 45 | 14.0 | 8 |
| Nigeria | 4,067 | 47 | 11.6 | 8 |
| Iraq | 2,326 | 30 | 12.9 | 8 |
| **India** | **25,114** | **242** | **9.6** | **5** |
| Pakistan | 9,400 | 61 | 6.5 | 4 |
| Ireland | 4,020 | 28 | 7.0 | 2 |
| South Africa | 5,444 | 17 | 3.1 | 1 |
| UK | 164,691 | 332 | 2.0 | 1 |

India is **2nd in counts** because it is the largest non-UK group, **mid-pack in rate** among non-UK countries, about **5×** UK-trained. Performance assessment ≠ malpractice payment ≠ fraud. No age/sex/specialty controls. [SOURCE: https://doi.org/10.1186/s12909-017-0903-6] [SOURCE: https://www.springermedizin.de/country-of-qualification-is-linked-to-doctors-general-medical-co/13354628]

Humphrey, Hickman, Gulliford *BMJ* 2011: non-EU qualified doctors, higher-impact GMC decisions at each stage (referral aOR 1.61; adjudication 1.68). India not separated. [SOURCE: https://doi.org/10.1136/bmj.d1817]

#### Quality (disconfirmation of “worse doctors”)

Tsugawa, Jena et al., *BMJ* 2017: 1.2M Medicare medical admissions, 44,227 internists, 2011–14. 30-day mortality, hospital fixed effects: IMGs **11.2%** vs US graduates **11.6%** (aOR **0.95**, 0.93–0.96). India is listed among the eight largest IMG source countries; country-specific mortality was **underpowered** (supplement figs A–C, numbers not recovered this session). US IMGs pass USMLE and a residency match (~50% match vs ~94% US MD). That filter is stricter than UK/Australia historically. [SOURCE: https://doi.org/10.1136/bmj.j273]

### Steel-man

The claim that Indian-trained doctors are over-represented in *complaints and regulator performance reviews* is true in Australia (OR 1.61) and the UK (~5× GMC performance assessments). IMGs are over-represented among US *exclusion* cases overall and among criminal-fraud *convicts* (Pande 59%). High-profile individual fraud cases exist; they do not make a rate.

### Disconfirmation

That does not imply higher US *malpractice payments* or higher US *billing-fraud exclusions*. The best US fraud study puts IMG fraud aOR at 1. The best US outcome study puts IMG internist mortality slightly *below* USMGs. Indiana’s negligence outlier is Caribbean schools, not India. Complaint rates mix competence, communication, racism, and who works where (area-of-need, solo primary care).

### What's uncertain

- US Indian-origin (race) vs White rates: **not measured**.
- US India-trained vs US-trained paid-claim rate: **not published**.
- Whether UK/AU complaint excess is competence vs language/culture/patient bias.
- Pande’s 59% IMG share after specialty and practice-setting adjustment.
- Tsugawa’s India-specific mortality.

What would change the US answer: NPDB research-identifiable file merged to AMA Masterfile (school country, race). Public NPDB cannot do it.

[FRAMING-SENSITIVE: complaint ≠ negligence ≠ fraud; IMG ≠ Indian-origin; UK/AU ≠ US selection.]
