# Indian 2nd and 3rd generation fiscal position at white ages

**Question:** What is the fiscal contribution of 2nd- and 3rd-generation Indian-origin US residents compared with non-Hispanic whites of the same age?
**Tier:** Standard | **Date:** 2026-09-21
**Ground truth:** G1 and G2 were already on `indian_ledger_2026_09_18` (adults 25–64 vs 3rd+ NH whites). G3 was not. Age-standardised G2 was an arm, not the headline.

Model: Cursor Grok 4.6. Instrument caveat: `notes/llm-bias-caveat.md`.

### Claims

| # | Claim | Evidence | Confidence | Status |
|---|---|---|---|---|
| 1 | At the white 25–64 age mix, Indian G2 run +$23,692 (se 5,482) per person-year on the 2025 extended ledger | CPS ASEC 2025, n=209 | High for this ledger | VERIFIED |
| 2 | Indian G3+ (race/ID) point estimate is still above whites (+$11,806 se 8,150) but does not reject parity | Same ledger, n=49 | Low | VERIFIED as noisy |
| 3 | Five-year own-tax G3 gap +$4,101 (se 3,880); 2023 below whites | ASEC 2022–2026, n=203 stacked | Medium-low | VERIFIED |
| 4 | US-born Asian Indian adults out-earn US-born NH whites in every ACS 2023 working-age band | ACS 2023 PUMS, 25–64 n=2,937 | High for income, not generation | VERIFIED |
| 5 | G2→G3 BA 85%→72% vs white 44%: toward the white mean, not to it | ASEC pool | Medium | VERIFIED |
| 6 | The G2 earnings gap is not an IT-occupation mix: dropping IT leaves CPS G2 at +$47k of +$48k; ACS US-born ancestry IT mix is 4% of the gap | ACS 2023 employed; ASEC 2022–2026 OCCUP | High for earnings, not the fiscal ledger | VERIFIED |
| 7 | H-1B is G1 only. Proxy ~30% of India-born 25–64; lowest-net G1 arm. G2 is US-born | CPS visa unobserved; `PEINUSYR>=26` & `PRCITSHP=5` | High for the mapping; medium for the proxy’s purity | VERIFIED |

[DATA: `infra/immigration-fiscal/indian_generation_2026_09_21/`]

### Key findings

**Yes, we can estimate G2 at the same ages as whites.** Direct standardisation to the 3rd+ NH white 25–64 distribution on the repo's extended ledger (equal shares among unit members, person weights, after K-12 and MEPS health) gives **+$37,123** for G2 against **+$13,431** for those whites. The gap **+$23,692 (se 5,482)** is larger than the India-born age-standardised gap **+$10,955 (se 1,449)**. The adults-only allocation widens G2 to **+$27,090 (5,317)** raw. [CALCULATION: `india_g3_ledger.csv`; matches `indian_ledger_2026_09_18`]

**G3 is identifiable but not precise.** Native, both parents US-area-born, `PRDASIAN=1`: 26–49 working-age records per ASEC year (~0.13M weighted in 2025). On the same 2025 ledger the age-standardised gap is **+$11,806 (se 8,150)**; adults-only **+$14,076 (se 11,346)**. Neither rejects zero. A five-year pool on own modeled income/payroll/state tax minus SS/SSI/cash — a thinner object — gives **+$4,101 (se 3,880)** age-standardised, and **2023 is −$1,665**. [CALCULATION] [DISCONFIRMATION]

That G3 definition is **not** observed grandparents. It is the people who still check Asian Indian after two US-born parents. Carnegie IAAS 2024 (opt-in adults) puts 5% of Indian Americans in the third generation and 3% in the fourth. [SOURCE: https://assets.carnegieendowment.org/static/files/2024%20IAAS_Survey3-1.pdf]

**Same-age ACS income (mostly G2 among adults).** ACS has no parent birthplace. US-born Asian Indian ancestry 25–64: BA 83.6% vs 42.2% for US-born NH whites; mean PINCP **$130,278 vs $71,173**. Gaps by band: 25–34 +$33,842; 35–44 +$86,645; 45–54 +$101,021; 55–64 +$55,924. The 65–80 ancestry cell (n=97) is **below** whites on the mean (−$8,384). India-born 25–64 sit between: mean PINCP $111,334. [CALCULATION: `acs_age_bands.csv`] [DISCONFIRMATION]

**Papers.** Tran, Lee and Huang (2019), CPS 2008–2016 ages 25–40: 2nd-gen Indians 84.45% BA vs 39.95% for 3rd+ whites; after education controls the professional-occupation advantage vs whites is not significant. No Indian G3 cell. [SOURCE: https://www.russellsage.org/sites/default/files/Tran-Lee-Huang-2019.pdf] NAS (2017) Table 8-12 is by education, not origin: a recent BA immigrant arriving at 25–64 has a 75-year NPV of **+$994k** including descendants (2012 dollars, CBO outlook, no public goods). Indian G1 is heavier on graduate degrees than that BA row. [SOURCE: https://nap.nationalacademies.org/read/23550/chapter/13]

### Steel-man

The claim that “Indians only look good because they are young visa holders” is the right objection. Age-standardising the India-born 25–64 mix to whites **raises** the gap slightly (+$10,732 → +$10,955). G2, who are younger still (mean age 37 vs 45), look **better** after standardisation (+$20,572 → +$23,692). ACS same-age bands confirm the income gap is not an age artifact in working ages.

The claim that “the third generation becomes white” is the right objection for G3. BA and the fiscal point estimate move toward whites. On the 2025 ledger we **cannot reject** that they have already arrived. The five-year tax measure still sits a bit above whites, with a year below. Identity selection can bias the remaining G3 cell either way (Duncan–Trejo for Mexicans finds attriters positively selected; the Indian case is unmeasured). [INFERENCE]

### What's uncertain

Exact G3 vs G4+; mixed-race coding; whether G3 identifiers are the high-SES or low-SES tail of biological grandchildren; India-specific medical costs; a lifetime NPV with return migration. A stacked multi-year **extended** ledger (not just own-tax) would tighten G3 SEs; it was not built here because SPM extensions are year-specific.

[FRAMING-SENSITIVE: whose welfare; partial vs complete account; resident vs admission.]

## Revisions — 2026-09-21 (same day): why G2 > G3, and G4

Pooled ASEC 2022–2026 own-person earnings/tax. [CALCULATION: `g2_g3_decompose.csv`, `g4_coresident.csv`]

**Null first.** The 2025 extended-ledger G3–white gap does not reject zero. The G2–G3 gap in the five-year pool does: G2 net $34,926 vs G3 $20,943 (n=941 vs 203). That is the observation to explain.

**What it is not.** Every G3 adult 25–64 in the cell is `PRDTRACE=4` (Asian only); mixed White-Asian is not hiding in the ID cell. G2 with one India-born parent matches two-India-parent G2 on tax-minus-cash. G2 who identify as White-only (n=86) earn *less* than G2 who check Asian Indian ($86k vs $117k), so identity dropouts are not the high-SES tail. Older G3 (40–64) have *higher* BA than younger G3 (78% vs 63%), so a weak pioneer remnant is not dragging the mean.

**What it is.** Two stacked facts.

1. **Different inflows, not the same people later.** Today's G2 adults are children of the post-1965 / H-1B wave. A working-age G3 of that wave is only now appearing (25–39). At the same ages 25–39, G2 BA is 85% and earnings $101k; G3 BA is 63% and earnings $81k. That is not an age artifact.

2. **Education plus a G2 graduate premium.** G3 BA-holders earn $97,599 and net $25,871 — the same as white BA-holders ($94,467 / $25,425). G2 BA-holders still earn $125,689 and net $39,467. Without a BA, G2, G3 and whites are all ~$43–45k. The G2 advantage is “more degrees, and those degrees pay more,” which is what hyper-selected parents produce. G3 graduates look like white graduates. [CALCULATION]

**G4.** There is no post-1965 Indian fourth generation of working age. Hart-Celler arrivals ~1966 have G2 born ~1968–80, G3 born ~1990–2005, G4 born ~2015–. Adult G4 would have to come from the pre-1965 stock: 2,544 India-born in 1910, 8,746 in 1960, then 387,223 in 1980. [SOURCE: Leonard 1993 Table 1, from Melendy / Census; https://escholarship.org/uc/item/2q10n4bh] About 500 Punjabi–Mexican pioneer marriages; those descendants often did not keep an Asian Indian race box. Among children <18 in our G3+ ID cell with observed grandparents, **66% have an India-born grandparent (G3)** and **17.5% have four US-born grandparents (G4+)** — n=31 stacked, unusable for earnings. Adults 25–64: 7 co-resident all-US-GP cases. Carnegie IAAS 2024’s 3% “fourth generation” is an opt-in adult share, not a Census stock. [SOURCE: https://assets.carnegieendowment.org/static/files/2024%20IAAS_Survey3-1.pdf]

The test that would identify within-lineage decline is to wait until today’s G2’s children (now mostly under 18) are 25–39 and compare them to today’s G2 at those ages. Public CPS cannot do that now.

## Revisions — 2026-09-21 (same day): IT mix and H-1B

Question: is the G2/G1 earnings advantage just computer/IT jobs, and are H-1B holders inside the high-skill counts? [CALCULATION: `occ_split.py`]

**IT for G2: killed.** True G2 with a job last year (CPS, n=816) is 13.2% IT / 7.9% software / 8.6% physicians against 4.2% / 1.1% / 0.6% for 3rd+ NH whites. 2-bin Kitagawa (IT vs not, mix at white means) assigns **8%** of the +$48,222 earnings gap to IT mix. Dropping every IT worker leaves **+$47,244**. ACS 2023 employed US-born Asian Indian ancestry (n=2,495, G2-heavy): 11.0% IT, 5.7% software, **12.1% physicians** — the opposite of a CS-centric generation. Dropping IT *widens* that gap (+$64,022 → +$64,754). They still out-earn whites inside other managers ($193k vs $128k) and the residual rest bin ($112k vs $71k). Broadening the objection from IT to “high-pay professional niches,” physicians are the G2 mix that survives; dropping IT and MDs still leaves +$38k (CPS) / +$45k (ACS). [DISCONFIRMATION]

**IT for G1: partly true, not the whole gap.** India-born employed 25–64 are 32.5% IT and 19.3% software. Mix is 23% of their +$48,056 ACS gap; dropping IT leaves +$39,027. Within software $162k vs $153k; other managers $186k vs $128k; rest $86k vs $71k. A 10-bin occupation mix (IT + MD + engineers + managers + rest) is about half of G1’s gap — professional mix, not CS alone.

**H-1B-like G1 is the IT story.** Recent noncitizen India-born (ACS CIT=5, YOEP≥2018): 38.3% IT, 26.1% software; **83%** of a smaller +$16,147 gap is IT mix; inside software they earn *less* than white developers ($126k vs $153k). 10-bin within-occupation is negative. That is the body-shop/prevailing-wage pattern, not the G2 pattern. [DISCONFIRMATION of a uniform Indian CS premium]

**H-1B in the counts.** Unobserved visa. **G2/G3 cannot hold H-1B** (US-born). **G1 includes them.** Ledger proxy (noncitizen, entered 2018+): 30.0% of India-born 25–64, fiscal +$17,956 vs settled +$26,828; excluding them raises the G1 gap +$10,732 → +$13,397. They are inside the G1 high-skill average, not a separate bucket, and they are the lowest-net G1 arm. Proxy also contains H-4, F-1 OPT and other nonimmigrants. [DATA: `indian_ledger_2026_09_18`]

Universe is employed earnings, not the extended fiscal ledger. G3 occupation cells are tiny (n=168 with a job; MD n=3).
