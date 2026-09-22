**Verdict:** Second-generation Indian adults, put at the 3rd+ non-Hispanic white 25–64 age mix, run **+$23,692 (se 5,482)** per person-year on the repo's extended 2025 ledger — wider than the India-born **+$10,955 (se 1,449)**. Third-plus Indian (US-born, both parents US-born, `PRDASIAN=1`) is a **tiny, noisy cell**: 2025 n=49, gap **+$11,806 (se 8,150)** after age-standardising, which does not reject white parity. A five-year ASEC pool (n=203 stacked) on a thinner own-tax-minus-cash measure gives **+$4,101 (se 3,880)** age-standardised; 2023 is below whites. ACS same-age personal income, which cannot split G2 from G3, shows US-born Asian Indian adults 25–64 at **+$59k** mean PINCP vs US-born NH whites. [DATA: this lane; `indian_ledger_2026_09_18`]

Model: Cursor Grok 4.6. Instrument caveat: `notes/llm-bias-caveat.md`.

The absolute sign is a convention of a partial ledger (no public goods, defence, debt service or benefit accrual). **The gap against same-age whites is not.** Residents, not admissions. G3 is race/ID, not observed grandparents.

## 1. Same ledger, same ages (CPS ASEC 2025)

Adults 25–64, `equal_all_members`, person weights, after employer payroll, sales, property, K-12 and MEPS public-paid health. Age-standardised arm reweights each group to the white 25–64 four-band mix. [CALCULATION: `ledger_g3.py`; white/G1/G2 byte-match `indian_ledger_2026_09_18`]

| Group | n | After health | Gap vs white (se) | Age-std after health | Age-std gap (se) |
|---|---:|---:|---:|---:|---:|
| 3rd+ NH white | 36,287 | +13,431 | — | +13,431 | — |
| India-born (G1) | 1,232 | +24,163 | +10,732 (1,351) | +24,386 | +10,955 (1,449) |
| India G2 (India-born parent) | 209 | +34,003 | +20,572 (3,872) | +37,123 | **+23,692 (5,482)** |
| India G3+ (`PRDASIAN=1`, US-born parents) | 49 | +24,446 | +11,015 (8,613) | +25,237 | **+11,806 (8,150)** |
| Native Asian Indian self-ID (G2+G3+diaspora) | 258 | +30,344 | +16,913 (3,382) | +32,093 | +18,662 (4,679) |

[CALCULATION: `derived/india_g3_ledger.csv`]

Per-adult allocation (`equal_adults_18plus`, raw): G2 **+$27,090 (5,317)**; G3 **+$14,076 (11,346)**; G1 +$15,460 (1,695). [CALCULATION]

G3 2025 components vs white: modeled taxes $21,677 vs $14,383; selected cash $837 vs $2,453; K-12 $1,598 vs $1,652; MEPS health $2,112 vs $2,553. The G3 point estimate is a tax surplus, not a transfer-side trick. Sampling error on n=49 still spans zero. [CALCULATION]

## 2. Five-year pool, thinner tax measure

ASEC 2022–2026, own-person federal+payroll+state income tax minus SS/SSI/cash assistance. **Not** the extended ledger (no K-12, MEPS, employer payroll, sales, property). Equal-year mean; SE is the between-year sd/√5. Adults 25–64. [CALCULATION: `analyze_cps.py`, `year_cluster.py`]

| Group | n stacked | BA | Earnings | Tax−cash | Age-std tax−cash gap vs white (se) |
|---|---:|---:|---:|---:|---:|
| 3rd+ NH white | 185,993 | 44.3% | 67,008 | 15,608 | — |
| India G1 | 5,442 | 89.2% | 105,868 | 28,639 | +13,461 (1,626) |
| India G2 | 941 | 84.9% | 112,889 | 34,746 | **+19,842 (3,238)** |
| India G3+ race | 203 | 71.6% | 79,396 | 20,156 | **+4,101 (3,880)** |
| India G2 diaspora (foreign parents, not India) | 313 | 66.9% | 80,941 | 20,378 | +5,671 (2,179) |

[CALCULATION: `derived/cps_generation_pooled.csv`, `derived/cps_generation_year_cluster.csv`]

G3 year-by-year tax−cash gap vs white: 2022 +$8,959; **2023 −$1,665**; 2024 +$1,030; 2025 +$3,525; 2026 +$10,890. One of five years is negative. [DISCONFIRMATION]

G2→G3 BA 84.9% → 71.6% vs white 44.3%. That is regression toward the white mean, not arrival at it. [CALCULATION]

## 3. Same-age ACS income (G2 and G3 mixed)

ACS 2023 1-year PUMS, no parental birthplace. US-born Asian Indian ancestry (ANC 615) is mostly G2 among adults; median age of the all-age ancestry group is 15 in the 2026-09-18 profile. US-born NH white is `RAC1P=1` and `HISP=1` (ACS, not the CPS Hispanic code). Person income × `ADJINC`. [DATA: `analyze_acs.py`; India-born and US-born ancestry 25–64 n match `indian_ledger_2026_09_18` ACS profile]

| Age | White BA | Indian US-born BA | White mean PINCP | Indian US-born mean | Gap |
|---|---:|---:|---:|---:|---:|
| 25–34 | 45.7% | 84.6% | 55,251 | 89,093 | **+$33,842** |
| 35–44 | 46.2% | 84.7% | 75,729 | 162,374 | **+$86,645** |
| 45–54 | 42.8% | 81.7% | 82,530 | 183,551 | **+$101,021** |
| 55–64 | 35.1% | 68.9% | 71,543 | 127,467 | **+$55,924** |
| 25–64 | 42.2% | 83.6% | 71,173 | 130,278 | **+$59,105** |
| 65–80 | 35.1% | 45.1% | 55,264 | 46,880 | **−$8,384** (n=97) |

[CALCULATION: `derived/acs_age_bands.csv`]

India-born 25–64: BA 84.4%, mean PINCP $111,334, gap vs white **+$40,162**. US-born Indian *adults* out-earn India-born at the same working ages; the 65–80 US-born cell is the one that falls below whites, on 97 records. [CALCULATION] [DISCONFIRMATION]

## 4. What the papers add (not a substitute for the ledger)

Tran, Lee and Huang (2019), pooled CPS ASEC 2008–2016, ages 25–40: second-generation Indians 84.45% BA and 45.22% graduate vs 3rd+ whites 39.95% and 12.04%; 78.91% in managerial/professional jobs vs 45.24%. After education controls the occupational advantage vs whites is not significant. They do not report a third-generation Indian cell. [SOURCE: https://www.russellsage.org/sites/default/files/Tran-Lee-Huang-2019.pdf]

NAS (2017) Table 8-12, 75-year NPV, CBO long-term outlook, no public goods, 2012 dollars: a **recent immigrant with a BA arriving at 25–64** is **+$994k** including descendants (**+$190k** of that is descendants). That table is by education, not by Indian origin. ACS 2023: 52.4% of India-born adults 25–64 hold a graduate degree, so the BA row is a **lower bound on the education mix**, not an Indian G3 measurement. [SOURCE: https://nap.nationalacademies.org/read/23550/chapter/13]

Carnegie IAAS 2024 (YouGov opt-in, n=1,206 adults): 30% second generation, 5% third, 3% fourth. Survey composition, not a Census stock. [SOURCE: https://assets.carnegieendowment.org/static/files/2024%20IAAS_Survey3-1.pdf]

## Limits

- G3+ is self-identified Asian Indian with two US-born parents. Exact G3 via grandparents is unobserved except for co-resident links. Identity attrition can bias the remaining cell in either direction. [UNVERIFIED]
- CPS India-born **levels** (4.28M in ASEC 2025 vs 2.94M in ACS 2023) are not to be quoted; gaps are within-file. [DATA: `indian_ledger_2026_09_18/RESULT.md`]
- MEPS health is US/not-US, not India-specific. Sales, property and K-12 are accounting scenarios. [UNVERIFIED]
- Age-standardising G3 uses 2–7 people in the 55–64 band in single years.
- 2026 ASEC recodes `PEINUSYR`; this lane does not use that variable.

## 5. Why G2 > G3, and G4

Pooled ASEC 2022–2026. [CALCULATION: `derived/g2_g3_decompose.csv`]

Killed: mixed-race inside the G3 ID cell (all 203 adults are Asian-only); one vs two India-born parents; G2 identity dropouts as the successful tail (White-only G2 n=86 earn $86k vs $117k for Asian-Indian G2); older G3 as a weak pioneer remnant (40–64 BA 78% vs 25–39 BA 63%).

Remains: G2 is the H-1B/post-1965 children. At ages 25–39, G2 BA 85% / earn $101k against G3 63% / $81k. Conditional on a BA, G3 graduates match white graduates ($98k vs $94k); G2 graduates still pay a premium ($126k). Without a BA all three groups sit at $43–45k.

G4 working-age post-1965 does not exist yet. Children <18 in the G3+ ID cell with observed grandparents: 66% India-born GP (G3), 17.5% all-US GP (G4+), n=31 stacked. Adult co-resident G4 n=7. [CALCULATION: `derived/g4_coresident.csv`] Pre-1965 India-born stock was 2.5k (1910) / 8.7k (1960) before 387k in 1980. [SOURCE: https://escholarship.org/uc/item/2q10n4bh]

## 6. Not just IT — and H-1B is G1 only

Earnings among people with an occupation, not the extended ledger. ACS 2023 employed 25–64 (`ESR` 1/2/4/5, PINCP). CPS ASEC 2022–2026, longest job last year (`OCCUP`, `PEARNVAL`). IT = software + other computer occupations + CIS managers + computer-hardware engineers. [CALCULATION: `occ_split.py`; `derived/acs_occ_earnings.csv`, `cps_occ_earnings.csv`, `occ_kitagawa.csv`]

| Group | n | Mean | Gap vs white | IT | Software | MD | Gap after dropping IT | Gap after dropping IT and MD |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| US-born NH white (ACS) | 771,130 | 85,313 | — | 4.0% | 1.2% | 0.6% | — | — |
| India-born | 17,232 | 133,369 | **+$48,056** | 32.5% | 19.3% | 2.5% | **+$39,027** | +$33,656 |
| … recent noncitizen (H-1B/H-4/OPT proxy) | 2,625 | 101,460 | +$16,147 | 38.3% | 26.1% | 1.5% | +$6,390 | +$5,099 |
| … settled | 14,607 | 140,023 | +$54,709 | 31.3% | 17.9% | 2.7% | +$45,138 | +$39,085 |
| US-born Asian Indian ancestry | 2,495 | 149,336 | **+$64,022** | 11.0% | 5.7% | 12.1% | **+$64,754** | +$44,911 |
| White G3+ (CPS) | 152,498 | 82,419 | — | 4.2% | 1.1% | 0.6% | — | — |
| India G1 | 4,484 | 130,538 | +$48,119 | 36.0% | 20.1% | 2.8% | +$40,629 | +$34,413 |
| India G2 | 816 | 130,641 | **+$48,222** | 13.2% | 7.9% | 8.6% | **+$47,244** | +$38,484 |
| India G3+ race | 168 | 98,531 | +$16,111 | 14.4% | 7.3% | 1.8% | +$8,228 | +$4,775 |

**Killed for G2.** Putting G2 at the white IT share (2-bin Kitagawa, mix at white means) accounts for **8%** of the CPS G2 earnings gap and **4%** of the ACS US-born-ancestry gap. Dropping every IT worker leaves G2 at +$47k (CPS) and *widens* the ACS ancestry gap. The US-born Indian top occupation is physicians (12.1%), not software (5.7%). [DISCONFIRMATION]

G2 still out-earn same-occupation whites in the large non-IT bins: other managers $158k vs $120k; the residual “rest” bin $105k vs $69k. Physicians are the G2 mix story that survives (8.6% vs 0.6%); dropping IT *and* physicians still leaves +$38k (CPS) / +$45k (ACS). [CALCULATION]

**G1 is the IT generation, and even there it is not the whole gap.** 19% software / 33% IT vs 1.2% / 4.0% for whites. 2-bin IT mix is **23%** of the India-born employed-income gap; dropping IT leaves +$39k of +$48k. Within software they also earn more ($162k vs $153k), as do other managers ($186k vs $128k) and the rest bin ($86k vs $71k). A 10-bin mix (IT + MD + engineers + managers + rest) is ~half of G1’s gap — occupation mix in a broad professional sense, not CS alone. [CALCULATION]

**The H-1B-like slice is the one place “it’s IT” holds.** Recent noncitizen India-born: 26% software, 38% IT; **83%** of their smaller +$16k gap is IT mix; inside software they earn *less* than white developers ($126k vs $153k). 10-bin within-occupation is negative. [DISCONFIRMATION of a uniform Indian-in-CS premium]

**H-1B in the counts.** Visa class is unobserved. G2 and G3 are US-born, so they cannot hold H-1B. G1 includes them. The ledger proxy is noncitizen, entered 2018+ (`PEINUSYR>=26`): **30.0%** of India-born adults 25–64, n=362, +$17,956 after health vs +$26,828 for settled G1. Excluding them *raises* the G1 fiscal gap (+$10,732 → +$13,397). They sit inside the G1 high-skill average; they are not a separate bucket, and they are the lowest-net G1 arm. ACS CIT=5 and YOEP≥2018 is the same idea among the employed. The proxy also contains H-4, F-1 OPT and other nonimmigrants. [DATA: `indian_ledger_2026_09_18`]

Universe caveat: employed / had a job last year, so these gaps are larger than the all-adult PINCP gaps in §3 (non-workers pull the mean down). Not age-standardised; G2 is younger, which is the wrong sign for explaining a *larger* G2 gap.

## Draft memo section

> **Indian 2nd and 3rd generation at white ages.** On the repo's 2025 extended ledger, US-born adults with an India-born parent, reweighted to the 3rd+ non-Hispanic white 25–64 age mix, run **+$37,123** per person-year against **+$13,431** for those whites, a gap of **+$23,692 (se 5,482)** on 209 cases. That is larger than the India-born age-standardised gap of **+$10,955 (se 1,449)**. The third-plus cell that can be formed — native, both parents US-born, Asian Indian race — has **49** working-age records in 2025: point estimate **+$25,237**, gap **+$11,806 (se 8,150)**, which does not reject parity with whites. Pooling 2022–2026 on a thinner own-tax measure (n=203) gives an age-standardised gap of **+$4,101 (se 3,880)** and one year (2023) below whites. ACS 2023, which cannot separate G2 from G3, shows US-born Asian Indian adults out-earning US-born NH whites in every 25–64 age band (25–64 mean PINCP **+$59,105**); the 65–80 ancestry cell does not. BA falls from 85% in G2 to 72% in the G3+ ID cell against 44% for whites: toward the white mean, not to it. The G3 figure is an identified-race remainder of a still-young descendant population, not a completed third generation.
