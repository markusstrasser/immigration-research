**Verdict:** Neither checked study identifies a share of the Mexican foreign-born 65+ advantage attributable to salmon bias. Turra & Elo identify a very small pooled-Hispanic retiree correction; it can support a labelled proxy arm, not a measured Mexican correction. Pre-retirement age-specific departures exist, but permanent loss of future Part A spending is not identified; recommend unpriced.

## Log

- 2026-10-14: Primary-source check started; scope is Turra & Elo (2008), Arenas et al. (2015), and existing age-specific emigration evidence.

- 2026-10-14: Retrieved Turra & Elo's NIH author-manuscript PDF from a full-text mirror after PMC returned a challenge page and Europe PMC returned HTTP 500. Parsed using `pdftotext -layout`, not a model. Copied the repo's previously acquired Van Hook & Zhang primary HTML and inspected its Methods, Table 1, Results, and Discussion. Arenas full text was read through Exa's primary-PMC fetch; direct raw-file acquisition remains blocked (details below).

- 2026-10-14: Verification PASS: both primary SHA256 pins, 24 CSV rows (12 Hispanic), anchor cells, and LF for evidence/CSV/text. Python measured 0.00266 seconds and 21,053,440 bytes process maximum RSS for this check (macOS `resource.getrusage`); no `time -l`, git mutation, or edits outside owned lane paths.

## Primary files and pins

All paths below are relative to this lane. No `pins.json` edits were made; these pins are for the parent to incorporate.

| File | Exact acquisition URL / provenance | Bytes | SHA256 |
|---|---|---:|---|
| `inputs/salmon_turra_elo_2008.pdf` | https://artefacts-discovery.researcher.life/full_text/DA-2/e2/e285c4d9b9f835799eded1acd9e1f52d/full_text/ac6ec3fbd082a0eb9d3165d716ddf65f.pdf | 351477 | `a70d7b848353f3bd1098d7099eadd9c6f3fd0b6c0b76462d7b9797731ac42d2d` |
| `inputs/salmon_vanhook_zhang_2011.html` | https://pmc.ncbi.nlm.nih.gov/articles/PMC3367327/ ; exact copy of `../ir5_adjusters_2026_09_27/_cache/lit/PMC3367327.html`, acquired 2026-09-28 with curl and generic User-Agent | 254954 | `7f6ecc3564199587c35e80b274a4d8f5075e621e96aba6d178b62d662ad61742` |

`inputs/salmon_turra_elo_2008.txt` is deterministic Poppler text from the PDF. `inputs/salmon_turra_rates.csv` is a deterministic whitespace parse of its Table 4 rows: 24 rows, including both Hispanic and NH-white series. `age_high=120` represents the source's open-ended `90+` band for the model's terminal support; it is not a measured source ceiling. Rates are **deaths per 1,000 person-years**, not qx. The CSV preserves source rates; a ratio of combined to US rates is the possible proxy multiplier. [SOURCE: PDF Table 4, manuscript p. 16] [CALCULATION: `pdftotext -layout`; source text rows 1006–1018]

## Turra & Elo (2008): measured scope and correction

The PDF identifies Turra and Elo, *Population Research and Policy Review* 27(5):515–530, DOI `10.1007/s11113-008-9087-4`, PMCID PMC2546603. It uses SSA Master Beneficiary Record and NUMIDENT, December 1995–December 2000, with 21.6 million primary beneficiaries present at baseline (0.9 million Hispanic); outcome ages 65+. Death ascertainment covers residents abroad as well as in the US. Country-of-origin specificity is inadequate: Puerto Rican birthplace is separate, other foreign-born Hispanics are pooled, and some birthplaces are unknown. [SOURCE: primary PDF, Data/manuscript pp. 3–5; Limitations pp. 9–10]

The **foreign-born Hispanic** resident-abroad versus US mortality ratios are 1.15 men and 1.20 women (Table 2, both printed p-values .000, p<.001). These measure emigrant/stayer mortality, **not** mortality-rate attenuation from excluding emigrants. Table 1 reports foreign residence as 9.3% of foreign-born Hispanic men's person-years and 4.8% of women's. Multiplying these crude exposure shares by the Table 2 excess would be a further age-composition/model assumption, not the study's measured age-specific correction. [SOURCE: PDF Tables 1–2, manuscript pp. 13–14]

Table 4 uses **all Hispanics, all nativities**, separately by sex and age. Its US-resident versus all-resident estimates do not provide foreign-born-only Mexican cells. Exact cells for possible pricing are below; units are deaths per 1,000 person-years. [SOURCE: PDF Table 4, manuscript p. 16]

| Sex | Age | Hispanic US | Hispanic combined | Hispanic/NH-white ratio US (95% CI) | Ratio combined (95% CI) |
|---|---|---:|---:|---|---|
| Men | 65–69 | 24.61 | 24.71 | 0.86 (0.84, 0.88) | 0.86 (0.85, 0.88) |
| Men | 70–74 | 34.53 | 34.63 | 0.87 (0.86, 0.88) | 0.88 (0.87, 0.89) |
| Men | 75–79 | 53.07 | 53.28 | 0.87 (0.86, 0.89) | 0.88 (0.87, 0.89) |
| Men | 80–84 | 88.34 | 88.46 | 0.89 (0.88, 0.90) | 0.89 (0.88, 0.90) |
| Men | 85–89 | 142.08 | 142.04 | 0.87 (0.86, 0.89) | 0.87 (0.86, 0.89) |
| Men | 90+ | 248.44 | 248.04 | 0.86 (0.85, 0.88) | 0.86 (0.85, 0.88) |
| Women | 65–69 | 12.92 | 12.93 | 0.82 (0.80, 0.84) | 0.82 (0.80, 0.85) |
| Women | 70–74 | 18.58 | 18.60 | 0.82 (0.80, 0.83) | 0.82 (0.80, 0.83) |
| Women | 75–79 | 30.72 | 30.92 | 0.83 (0.82, 0.85) | 0.84 (0.82, 0.85) |
| Women | 80–84 | 54.63 | 54.60 | 0.86 (0.84, 0.87) | 0.86 (0.84, 0.87) |
| Women | 85–89 | 98.35 | 98.50 | 0.88 (0.86, 0.89) | 0.88 (0.86, 0.89) |
| Women | 90+ | 199.96 | 199.54 | 0.88 (0.87, 0.90) | 0.88 (0.86, 0.89) |

The Hispanic combined/US multiplier ranges from 0.99789958 to 1.00651042: some cells decrease after inclusion, so do not clip below 1. For an arm retaining the current NH-white reference, using raw Hispanic combined/US isolates the measured pooled-Hispanic rate change; for a relative mortality correction that also removes selection in the reference, divide that multiplier by NH-white combined/US from the same Table 4. These are different estimands. Neither is a measured share of the Mexican foreign-born versus US-born hazard gap. [CALCULATION: ratios from `inputs/salmon_turra_rates.csv`] [INFERENCE]

Disconfirmation of the strongest salmon explanation is direct: accounting for residents abroad barely changes these pooled ratios. The study also finds elevated mortality on return **to the US**, counterbalancing departure selection. It excludes non-primary beneficiaries; the manuscript notes exclusion of 25–30% of resident men and about half of women, address changes may represent seasonal movement or a representative's address, and birthplace information limits subgroup analysis. Its data include 65+ deaths of primary beneficiaries who left before retirement, but do not estimate an age-specific pre-retirement exit hazard. [SOURCE: primary PDF Results pp. 6–7, Limitations pp. 9–10]

## Arenas et al. (2015): selection, not an attenuation share

*Return Migration to Mexico: Does Health Matter?*, Demography 52:1853–1868, DOI `10.1007/s13524-015-0429-7`, PMCID PMC4644732. The full primary-PMC text was read through Exa's fetch, https://pmc.ncbi.nlm.nih.gov/articles/PMC4644732/ . Mexican Family Life Survey follows 2002 Mexico residents who moved to the US by 2005; return outcome is Mexico residence at Wave 3, 2009–2012. Final analytic sample is 518 adults age 15+, mean age about 27. Recent migrants and self-reported health are the instrument, not retiree deaths. The paper finds health-related selection, but expressly says its results do not establish the magnitude explaining the Latino mortality paradox. No mortality-attenuation share can be transferred from this study. It cannot distinguish voluntary from forced return, and its snapshot return outcome omits interim circular moves back to the US. [SOURCE: primary-PMC full text, Data, Results, Discussion]

[GAP] Raw Arenas primary bytes could not be pinned. PMC returned challenge HTML; Europe PMC fullTextXML returned HTTP 500; Princeton old URLs returned 404/401; Springer exposed abstract, references and notes but not the body; the AUSJAL repository's linked IBERO PDF now redirects to a DSpace application rather than PDF. No Arenas numerical table was used or reconstructed from Exa text. This limits reproducible offline verification, not the conclusion that no measured mortality share was identified.

Contradictory evidence is present in the checked primary sources: Van Hook & Zhang's CPS-matching study finds health is weakly associated with emigration and its health-composition simulations change little; Arenas explains that its younger, recent-arrival longitudinal sample differs from both CPS and SSA retiree samples. The latter supports a selection mechanism but does not override the mortality magnitude identified in the former. [SOURCE: Van Hook & Zhang primary HTML Abstract, Discussion; Arenas primary-PMC Introduction, Discussion] [INFERENCE]

## Pre-retirement emigration: available rates, unsuitable absorbing hazard

Van Hook & Zhang, *Who Stays? Who Goes? Selective Emigration Among the Foreign-Born*, Popul Res Policy Rev 30(1):1–24 (2011 issue; online 2010), DOI `10.1007/s11113-010-9183-0`, PMCID PMC3367327. Table 1 reports **estimated annual percentage probabilities** for foreign-born age-sex-origin groups, not the share of emigrants in an age band. The paper's method matches March CPS 1996–2008 respondents to 1997–2009 and infers departure from attrition, subtracting modeled deaths, internal migration, and other attrition; it assumes second-generation emigration zero and transport of residual attrition. These are group residual estimates, not observed individual departures. [SOURCE: primary HTML Methodology, Eq. 5; Table 1]

| Mexican foreign-born group | All ages 18+ | 18–34 | 35–64 | 65+ | Samples 18–34 / 35–64 / 65+ |
|---|---:|---:|---:|---:|---|
| Men, annual % | 4.3 | 7.0 | 2.1 | 0.0 | 7,520 / 6,516 / 608 |
| Women, annual % | 1.6 | 3.8 | 0.0 | 4.0 | 6,081 / 5,972 / 758 |

These are the exact Table 1 cells, with no printed standard errors/CIs for these rate cells. The small elderly Mexican-women cell is explicitly cautioned in Results. A printed 0.0 is a point estimate, not proof of zero departures or an exact bound. No separate under-18 rates appear. [SOURCE: primary HTML Table 1, Rates of Emigration]

The authors do not adjust for emigrants returning to the US; their one-year method captures circular departures. They contrast it with 5–10-year residual estimates (generally around 1.0% for all foreign-born) and say a portion of annual emigrants subsequently return. The stated returning-emigrant rate below 1% annually concerns all foreign-born, not Mexican age-sex residence persistence through retirement; it does not identify the needed retention factor. Applying Table 1 departures as an absorbing exit hazard until retirement would price an assumed permanent exit, repeat a 1996–2009 mix through future ages, and ignore duration/status selection and return for Medicare. [SOURCE: primary HTML The Current Study, Methodology, Rates of Emigration; Turra & Elo Limitations] [INFERENCE]

## For the parent

1. Price the full salmon bound in the brief as an assumption: G1 65+ at US-born Mexican ratios. No identified measured share of that extra advantage is available from these studies. Keep the bound's meaning separate from return migration's empirical existence.
2. If a smaller literature arm is useful, `inputs/salmon_turra_rates.csv` supports a **pooled-Hispanic SSA-retiree rate-inclusion proxy**, applied only to G1 age 65+ as transport. Label that pooling/transport; do not call the file foreign-born rates or a measured Mexican correction. Model 2's foreign-born ratios are emigrant/stayer risks and cannot be substituted for this correction.
3. Recommend **pre-retirement emigration not priced**: age-specific gross departures are present but age-sex-specific permanent residence/Part A access after retirement is not. An absorbing-exit calculation can be an explicitly assumed extreme arm, not the earlier informal −$1–3bn as a verified estimate. The brief permits leaving it unpriced with this reason.
4. Covered: full Turra manuscript, Van Hook & Zhang primary cached HTML, Arenas primary full text via Exa. Skipped: transferring unrelated health-outcome odds to death hazards; newer evidence searches beyond the bounded task; estimating a new permanent-emigration model. [GAP] Reopen with an age-sex-origin US↔Mexico multistate residence model that identifies residence during eligible retirement years and return visits for Part A use.

This evidence synthesis uses an LLM on a politically charged topic. The decisive rate cells were taken from deterministic primary-PDF/HTML text; the policy transport judgments remain inferences.
