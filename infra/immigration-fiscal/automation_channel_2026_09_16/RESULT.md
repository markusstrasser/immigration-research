# Automation & Capital-Deepening Channel — Does Low-Skill Immigration Delay Mechanisation?

**Verdict:** The automation-delay mechanism is **real as technique choice and unproven as a
welfare cost.** Lewis 2011, Danzer et al. 2020 and San 2023 all find low-skill labour supply
shifts technique away from automation, and Peri 2012 concedes it with a skill-bias elasticity near
−1. But no study identifies a durable national output cost, the one setting with the largest and
most persistent induced innovation (bracero) still left incumbents **poorer** (permanent farm-value
decline), and the best-identified study in the literature — a **randomised H-2B visa lottery** —
finds low-skill immigrants **raise** firm investment with elasticity **1.5–2.1**. Recommendation:
name the mechanism, do **not** monetise it into the fiscal ledger.

Model self-report: claude-opus-5[1m] (Opus 5, 1M context), researcher agent lane
`automation_channel_2026_09_16`. Dispatched by team-lead 2026-09-16.

## Scope
1. Lewis 2011 QJE — technique choice vs less-skilled immigrant supply across metros.
2. Clemens/Lewis/Postel 2018 AER (bracero); San 2023 AEJ:Applied; Zhang 2024 SSRN.
3. Danzer/Feuerbaum/Gaessler 2024 JPubE (German ethnic Germans → automation patents).
4. 2023–2026: enforcement (Secure Communities, E-Verify, 287(g)) × firm automation/capital; H-2A × mechanisation.
5. Peri 2012 REStat + Peri 2016 JEP (pro side, TFP/task specialisation).
6. Central Valley: BEA CAINC1 per-capita income ratios 1970→latest, 8 San Joaquin counties.
7. [INFERENCE] magnitude sketch vs −$8.3k/adult-year 2nd-gen fiscal gap.
8. Disconfirmers: Beerli et al. 2021 AER; Mitaritonna et al.; Orefice & Peri.

## Findings
See Appends 1–3 below. Remaining gaps are listed at the end of Append 3.

---

## APPEND 1 (2026-09-16) — Danzer/Feuerbaum/Gaessler + Central Valley BEA

### 3. Danzer, Feuerbaum & Gaessler — "Labor Supply and Automation Innovation"
[SOURCE: IZA DP No. 13429, June 2020, https://docs.iza.org/dp13429.pdf — full text fetched and quoted]
Published version: *Journal of Public Economics* (the team-lead's "2024 JPubE" citation; the IZA WP
is the version verified here — see [GAP] below on whether published coefficients moved).

- **Identification.** Inflow of ethnic Germans (*Aussiedler*) from the FSU/Eastern Europe, ~2.5M
  entrants 1990–2006, skill-distribution bottom. Quasi-experimental **Assigned Place of Residence
  Act**, binding 1996/97: allocation to states by the *Königsteiner Schlüssel* historical budget
  quota, then to counties by relative population size. Unit = German labour-market regions
  (*Arbeitsmarktregionen*, following Glitz 2012); balanced yearly panel **1992–2006**.
- **Headline coefficient.** Table 2 col. 4: interaction β₃ = **−0.896 (s.e. 0.211)**; total effect
  β₁+β₃ = **−0.757, p = 0.001**. Verbatim: "increasing the inflow rate by one ethnic German per
  1,000 employed workers leads to a significant decline in the share of automation patents by
  around 0.75 percentage points (column 4, full specification)" (p. 15).
  Units: **pp change in automation share of patents per +1 immigrant / 1,000 employed workers.**
  (Team-lead's brief said "+10% low-skilled workforce → −3.3 pp". That is a *different*
  normalisation and I could not reproduce −3.3 pp from the WP text — see [GAP].)
- **Persistence: transient.** "The effect on automation innovation is confined to the first five
  years after the labor supply shock. The estimated coefficient in t = 6 is insignificant and close
  to zero suggesting that the negative automation innovation response is only transient." (p. 20)
- **Sector.** Concentrated in **mechanical engineering** (−0.55 pp, Table 5 Panel A col. 4), some
  chemistry. **Labour-market state:** present only in **tight** labour markets; "small in magnitude
  and statistically insignificant in regions with high pre-determined unemployment, i.e., slack
  labor markets" (p. 25, Table 6).
- **Falsifications pass.** (i) No effect on *non*-automation patents (Table 3 cols 5–8) — rules out
  a product-demand channel. (ii) No effect in the pre-binding allocation period (Table B-11).
  (iii) No contemporaneous-year association (Table 4 cols 1, 5).
- **Reading for the essay.** This is the *strongest clean causal evidence for* the mortmain
  mechanism — and it simultaneously bounds it: **transient (≤5 yrs), one sector, tight markets
  only, share not level.** It is a redirection-of-R&D result, not a productivity-level result.

### 6. Central Valley: San Joaquin Valley per-capita income vs CA and US
[SOURCE: BEA Regional CAINC1, https://apps.bea.gov/regional/zip/CAINC1.zip, vintage covering
1969–2024, downloaded 2026-09-16. Script: `bea_sjv.py`; 8 counties = Fresno, Kern, Tulare, Kings,
Merced, Madera, Stanislaus, San Joaquin. SJV aggregate PCI = Σ personal income ÷ Σ population.]

| Year | SJV PCI $ | CA PCI $ | US PCI $ | SJV/CA | SJV/US | SJV pop |
|---|---|---|---|---|---|---|
| 1969 | 3,797 | 4,676 | 3,931 | 0.812 | 0.966 | 1,603,575 |
| 1970 | 4,057 | 4,965 | 4,198 | 0.817 | 0.966 | 1,635,563 |
| 1975 | 6,409 | 7,320 | 6,324 | 0.876 | 1.013 | 1,813,395 |
| 1980 | 10,426 | 11,950 | 10,184 | 0.872 | 1.024 | 2,063,519 |
| 1985 | 12,906 | 16,788 | 14,746 | 0.769 | 0.875 | 2,371,902 |
| 1990 | 16,271 | 21,483 | 19,619 | 0.757 | 0.829 | 2,766,305 |
| 1995 | 18,275 | 24,596 | 23,577 | 0.743 | 0.775 | 3,064,553 |
| 2000 | 22,318 | 33,175 | 30,551 | 0.673 | 0.731 | 3,316,754 |
| 2005 | 27,070 | 38,737 | 35,669 | 0.699 | 0.759 | 3,726,185 |
| 2010 | 30,784 | 43,137 | 40,557 | 0.714 | 0.759 | 3,979,527 |
| 2015 | 37,183 | 53,816 | 48,062 | 0.691 | 0.774 | 4,145,341 |
| 2019 | 41,581 | 64,219 | 55,567 | 0.648 | 0.748 | 4,293,333 |
| 2022 | 49,763 | 77,196 | 66,298 | 0.645 | 0.751 | 4,366,202 |
| 2024 | 55,548 | 86,232 | 73,204 | 0.644 | 0.759 | 4,420,399 |

**The claim survives, with a shape correction.** SJV went from **parity with the US** (0.966 in
1970, peaking at **1.024 in 1980**) to **0.759 in 2024** — a **~26 % relative decline**, i.e. the
Valley lost roughly a quarter of its income position in 54 years. Against California the fall is
**0.817 → 0.644** (−21 %). Nearly the whole break happens **1980–2000** (1.024 → 0.731); since 2000
the ratio to the US is flat-to-slightly-up (0.731 → 0.759), so this is a **1980s–90s event**, not a
continuing slide. Every one of the 8 counties falls; Kern is the largest (0.977 → 0.692), San
Joaquin the mildest (1.045 → 0.861).

**Compositional vs incumbent-income:** SJV population grew **×2.70** (1.64M → 4.42M) versus **×1.97**
for California and **×1.67** for the US. Per-capita income is mechanically diluted by adding
low-income residents, so a large part of the ratio decline is **compositional by construction** —
PCI divides total income by *everyone*, including children and non-earners, and the SJV has the
higher dependency ratio. [UNVERIFIED] whether incumbents' own incomes fell relative to the US; the
BEA table cannot answer it. Needs ACS per-capita income **by nativity** for these counties.
[GAP] ACS nativity split not yet pulled — next step.

### Gaps after Append 1
- [GAP] Lewis 2011 QJE exact coefficient + the "−0.5 technologies on a base of 6" SMT result.
- [GAP] Clemens/Lewis/Postel 2018, San 2023, Zhang 2024.
- [GAP] Enforcement × automation 2023–26; H-2A × mechanisation.
- [GAP] Peri 2012/2016 coefficients; Beerli et al. 2021; Mitaritonna; Orefice & Peri.
- [GAP] Danzer published-version (JPubE) coefficient reconciliation with the "−3.3 pp" figure.
- [GAP] ACS nativity income for the 8 SJV counties.

---

## APPEND 2 (2026-09-16) — Lewis 2011, bracero trio, enforcement, H-2A

### 1. Lewis 2011 QJE — "Immigration, Skill Mix, and Capital Skill Complementarity"
[SOURCE: DOI 10.1093/qje/qjr011, QJE 126(2):1029–1069; full text fetched and quoted]

- **Identification.** 1970 immigrant settlement shares predict 1980s/90s inflows (Card-style
  enclave shift-share). Instrument Z_c = (predicted immigrant share) × (immigrant skill mix −
  incumbent skill mix), eq. 9 p. 19. Endogenous regressor = **change in high-school dropouts per
  high-school equivalent (U/S)** in a metro area. Data: **Surveys of Manufacturing Technology 1988
  and 1993** (plant-level automation-technology counts), plus the Annual Survey of Manufactures.
- **Base rate.** Mean number of automation technologies in use per plant in 1988 = **6.01
  (s.d. 4.68)**, Table I p. 11. This is the "base of 6".
- **Headline coefficients — technologies IN USE (Table VI, p. 25), d(U/S) 1980–88:**

  | Spec | OLS | IV |
  |---|---|---|
  | no controls | −4.91 (1.61) | −7.02 (2.10) |
  | + industry effects | −6.80 (1.79) | −9.59 (2.10) |
  | + industry × price controls | −5.62 (2.02) | −8.21 (1.90) |

  **Technologies ADDED 1988–93 (Table V, p. 23):** OLS −2.32 (1.68) / −3.02 (1.67); IV −7.75 (4.20)
  / −11.44 (4.42).
- **Units and the "0.5 on a base of 6" claim.** Coefficients are *technologies per unit change in
  the dropout/HS-equivalent ratio*. A **0.10 rise in U/S** therefore implies **−0.49 to −0.68
  technologies (OLS)** or **−0.70 to −1.14 (IV)** against a base of 6.01. **[VERIFIED — but the
  sentence is NOT in the paper.]** The "10-point rise → −0.5 of 6" summary is an *arithmetic
  restatement* of the OLS column of Table VI, and it quotes the **conservative** end. The IV
  estimates, which are Lewis's preferred causal numbers, are **1.4–1.9× larger**. Anyone using the
  −0.5 figure is understating Lewis's own causal estimate. Also note the regressor is the
  **dropout-to-graduate ratio**, not the "less-skilled share" — at the sample mean U/S ≈ 0.3 these
  are not the same units, so "10 points" needs stating as **+0.10 in U/S**.
- **Capital deepening (Table VII, p. 27), 1987–92:** ln(machinery/worker) OLS −0.16 (0.16), **IV
  −0.59 (0.31)**; ln(value added/worker) OLS −0.14 (0.10), **IV −0.03 (0.24)**. So machinery per
  worker falls materially while output per worker is **statistically indistinguishable from zero**.
  That combination is the whole argument in one line: capital intensity adjusts, measured labour
  productivity barely moves.
- **Lewis rejects the pure "choice of technique" story.** Per the Lewis 2012 survey: "Lewis (2011a)
  considers the choice of technique model ... but rules this out after finding non-zero response of
  relative wages to relative supply." Immigration is **not** fully absorbed by technique change.
- Survey cross-check [SOURCE: NBER w18310 / Annu. Rev. Econ. 5, Table 2 note c]: ∂ln s_K/∂(U/S) =
  **−0.56**, an elasticity of **0.168** at mean U/S = 0.3.

### 2a. Clemens, Lewis & Postel 2018 AER — bracero exclusion
[SOURCE: DOI 10.1257/aer.20170765; full text fetched and quoted]
- **Design.** Continuous-treatment DiD. Exposure = mean fraction of bracero workers in a state's
  seasonal hired farm workforce across all months of **1955** (a decade before exclusion).
  y_st = α'I_s + β'I_t + γ(I_{t≥1965} · ℓ̄_s^1955). Monthly state farm-employment stocks 1943–73,
  quarterly farm wages 1948–71. Exclusion effective 31 Dec 1964.
- **Wages (Table 1).** Hourly composite, all years: γ = **−0.0356 (0.0426)**; semi-elasticity
  ∂ln w/∂(B/L) = **−0.0831 (0.0654)**. 1960–70 window: γ = **−0.0401 (0.0315)**. Daily wage w/o
  board: **−0.385 (0.495)**. **All statistically zero, and point estimates are the WRONG SIGN for
  the restrictionist prediction.**
- **Employment (Table 2).** Domestic seasonal farm employment, all states all years: **−6,949
  (9,094)**; 1960–70: **+1,843 (6,859)**; exposed states only: **+312 (7,463)**. Zero throughout.
  By type (Table 3): local −2,971 (4,678), intrastate −9,083 (9,778), interstate +579 (1,128).
- **Mechanisation.** Tomato: the **Blackwelder harvester**, "machines that roughly doubled harvest
  productivity per worker," available since the late 1950s; Figure 5 shows California tomato-harvest
  mechanisation going from **near 0 % in 1964 to ~100 % by 1968**, with **no such shift in Ohio**
  (zero bracero exposure). Also "encouraged mechanization in cotton harvesting ... and sugar beet
  field preparation" (p. 15).
- **Caveat CLP themselves state.** They give **no quantitative decomposition** of the null into
  mechanisation vs crop switching. The mechanisation evidence is descriptive/graphical; the
  causal estimates are the wage and employment nulls. [FRAMING-SENSITIVE] Both camps over-read
  Figure 5: it is a striking picture, not an estimated share of the null.

### 2b. San 2023 AEJ:Applied — directed technical change
[SOURCE: DOI 10.1257/app.20200664, AEJ:Applied 15(1):136–63; author copy
https://mulysan.github.io/San_bracero.pdf — quoted from the AEA full text]
- **Design.** Crop-level DiD, 16 crops. ln E[Innovation_it] = β·ForeignShare_i·post_t + γ_i + δ_t,
  where ForeignShare_i is the bracero share of seasonal workers in crop i in 1964. Patents assigned
  to crops by a **text-search algorithm**. IV robustness: average distance from Mexico and average
  historical Mexican share.
- **Headline (Table 2).** Foreign share × post = **3.258 (0.474)** on patents, **2.271 (0.497)** on
  citations. I.e. **a 1-percentage-point higher pre-policy bracero share raises patenting by 3.3 %**
  (significant at 1 %). A 1 s.d. exposure increase (s.d. = 0.16, mean 0.19) raises patents by
  **70.7 %**, = **+2.87 annual patents per crop** against a pre-1965 mean of **4.06**. IV version:
  3.6 % and 2.5 %.
- **Persistence: the opposite of Danzer.** "the effect of Bracero exclusion persisted for at least
  15–20 years," with no pre-trend. San reads this as invention of genuinely new technology, not
  pull-forward of existing patents.
- **Task heterogeneity.** Effect **3.2 % higher** in technology classes serving 100 %-labour tasks
  vs 0 %-labour tasks — labour scarcity induces *labour-saving* more than labour-augmenting tech.
- **The kicker for the mortmain thesis.** Farm land values per acre **fell permanently** in exposed
  counties (Census of Agriculture 1950–82, Figure 6), and only in bracero states. San's own
  sentence: "**innovation was not enough to offset the lower labor supply for the affected farms**"
  and, on CLP, "Bracero exclusion made capital worse off while making labor no better off."
  **This is a direct empirical refutation of the strong mortmain welfare claim** in the one setting
  where the induced innovation is largest and most durable. Forcing mechanisation raised patents
  15–20 years and still destroyed farm value.

### 2c. Zhang 2024 — bracero and labour productivity
[SOURCE: Chengguo Zhang, "Do Low-skilled Immigrants Hurt Labor Productivity in the Destination
Country? Evidence from the Bracero Program," SSRN, DOI 10.2139/ssrn.5009570]
[GAP] Located and cited only. Full text not retrieved; coefficients **[UNVERIFIED]**. Title implies
the productivity-cost framing the essay needs; do not cite a number from it until read.

### 4a. Immigration enforcement × firms/capital (2019–2026)
- **Ayromloo, Feigenberg & Lubotsky, NBER w26676** ("States Taking the Reins?", E-Verify mandates).
  [SOURCE: https://www.nber.org/system/files/working_papers/w26676/w26676.pdf] Mandates raise
  E-Verify usage **+25 pp off a 21 % base four years out**; formal-sector employment falls for the
  likely-ineligible; **"no evidence that ... native-born workers' labor market outcomes improve"**;
  the number of establishments with 20+ employees **falls**. Firms exit rather than mechanise.
- **East, Luck, Mansour & Velásquez**, *J. Labor Economics* 2023 (Secure Communities)
  [SOURCE: https://www.journals.uchicago.edu/doi/10.1086/721152; WP https://docs.iza.org/dp11486.pdf].
  Staggered SC rollout DiD, ACS 2005–14. SC cut employment of likely-undocumented men **and cut
  the employment and hourly wages of US-born workers**, concentrated in medium-skill occupations in
  sectors that rely on undocumented labour. Mechanism they endorse: **higher labour costs reduce
  job creation** plus lower local consumption. Removing low-skill labour did **not** trigger
  offsetting capital deepening that rescued natives.
- [GAP] **No paper found that directly estimates enforcement → firm-level automation or capital
  expenditure.** This looks like a **genuine hole in the literature**, not a search failure: the
  enforcement literature measures employment, wages, consumption and firm exit, never capital
  stock or robot adoption. Worth stating in the essay as an unanswered question.
- **Adjacent anchor — Brynjolfsson, Li, Miranda, Seamans & Wang, NBER w34895 (Feb 2026),
  "Minimum Wages and Rise of the Robots"** [SOURCE: https://www.nber.org/papers/w34895]. Plant-level
  robot imports linked to Census microdata 1992–2021, state-border-discontinuity design: **a 10 %
  minimum-wage increase raises robot adoption by ~8 % relative to the mean.** This is the cleanest
  available **price-of-low-skill-labour → automation elasticity** for the US and is the right
  parameter for the magnitude sketch (see Append 3).

### 4b. H-2A and farm mechanisation
- **Valencia, "Visa Regulations, Agricultural Employment, and Productivity"** (AAEA 2026)
  [SOURCE: https://ideas.repec.org/p/ags/aaea26/404392.html]. County-level 2002–2022 USDA Census of
  Agriculture, **border-county-pair design** on the H-2A Adverse Effect Wage Rate. **A 1 % increase
  in the visa wage → +1.2 % machinery values**, +3.9 % intermediate inputs (intensive margin),
  +1.1 % input variety (extensive margin), and **no effect on employment or payrolls**. This is the
  mortmain mechanism *in reverse and in the present day*: make the guest worker more expensive and
  capital goes up roughly one-for-one in elasticity terms. [Working paper; not peer-reviewed.]
- **Jain, "The Rise of H-2A"** (AAEA 2026) [SOURCE: https://ideas.repec.org/p/ags/aaea26/404599.html].
  740 commuting zones 2008–2024, Bartik shift-share on enforcement. **For each settled non-citizen
  farm worker lost, farms hire ~2 H-2A guestworkers**; that substitution accounts for **~48 % of
  aggregate H-2A growth**. Enforcement thus produces *visa substitution*, not mechanisation — the
  single most policy-relevant finding in this block.
- Survey evidence (Georgia specialty crops, Choices 2025) reports mechanisation as the **dominant**
  grower response to AEWR hikes, but explicitly notes small farms **cannot** afford to mechanise.
  [Survey, non-causal; use only as colour.]
- **Hémous, Olsen, Zanella & Dechezleprêtre, "Induced Automation Innovation: Evidence from
  Firm-Level Patent Data," JPE 133(6):1975–2028 (2025)** — surfaced as the general theory-side
  anchor for induced automation. [GAP] coefficients not yet read.


---

## APPEND 3 (2026-09-16) — the pro side, the disconfirmers, and the magnitude sketch

### 5. Peri 2012 REStat — "The Effect of Immigration on Productivity: Evidence from U.S. States"
[SOURCE: DOI 10.1162/REST_a_00137; full text fetched and quoted]
- **Design.** State-decade panel 1960–2006. Instruments: 1960 immigrant-community shares, and
  distance from the Mexican border interacted with decade dummies. Regressor = **net inflow of
  immigrant workers over an intercensus period as a percentage of initial employment.**
- **2SLS coefficients (Table 2, col. 1, "Basic 2SLS"):**

  | Outcome | Coef. (s.e.) |
  |---|---|
  | TFP (Â) | **+1.37 (0.27)** |
  | Income per worker (ŷ) | **+0.88 (0.25)** |
  | Total employment (N̂) | **+1.09 (0.45)** |
  | Capital intensity, (α/1−α)(K̂−Ŷ) | **−0.08 (0.13)** |
  | Skill bias of technology (β̂) | **−1.14 (0.15)** |

- **Read it carefully — Peri concedes the mechanism and denies the cost.** The skill-bias
  coefficient is **−1.14, elasticity about −1**: immigration "promotes production techniques that
  are more unskilled-efficient (as suggested by Lewis, 2005, and consistent with the idea of
  directed technological choice)." That IS the mortmain mechanism, measured, significant, and
  **Peri names it**. His claim is that it is *not a cost*, because TFP rises anyway (+1.37) and
  capital intensity is unchanged (−0.08, indistinguishable from zero — "U.S. states have been
  growing along their balanced growth path"). Employment coefficient of 1.09, never statistically
  different from 1, means **zero native crowd-out** by construction of his variables (fn. 14).
- **The two sides are NOT estimating the same parameter.** Lewis identifies the *skill-mix*
  channel within manufacturing plants and finds capital intensity falls. Peri identifies *total
  immigrant inflow* at the state level and finds capital intensity flat and TFP up. They agree on
  the direction of technique change (unskilled-biased) and disagree on whether aggregate
  productivity pays for it. [FRAMING-SENSITIVE] Anyone who says "the evidence is settled" in
  either direction is choosing a level of aggregation.
- Peri 2016 JEP ("Immigrants, Productivity, and Labor Markets", JEP 30(4):3–30) is the narrative
  restatement of the above. [GAP] not separately fetched; do not quote a coefficient from it.

### 8. DISCONFIRMING EVIDENCE (mandatory, and it is strong)

**(a) Clemens & Lewis 2022, NBER w30589 — the single best-identified study in this whole file.**
[SOURCE: https://www.nber.org/papers/w30589, PDF text extracted and quoted]
US **H-2B randomized visa lottery**, 2021 and 2022, with a **pre-analysis plan**. Firms
exogenously allowed to employ more low-skill immigrants:

| Outcome | Elasticity |
|---|---|
| Production / revenue | **0.20–0.22** |
| **Investment** | **1.5–2.1** |
| Rate of profit | **0.15** |
| Foreign-native elasticity of substitution (low-skill) | **0.8–2.2** |
| Native employment | **zero or positive overall; positive in rural areas** |

Verbatim: firms losing immigrant labour "reduce revenue with elasticity 0.20–0.22, reduce
investment with elasticity 1.5–2.1, and reduce the rate of profit with elasticity 0.15 (all
statistically precise at conventional levels)." **More low-skill immigrants caused MORE
investment, by a factor of roughly 7–10 relative to the output response.** This is randomised,
recent, US, low-skill, and pre-registered. It is the hardest single fact against the mortmain
mechanism as a firm-level theory of capital: at the firm, low-skill immigrant labour and capital
are **complements**, not substitutes. Clemens & Lewis note the contrary theory explicitly
("capital instead substitutes for low-skill [labour] ... such substitution helps account for a
smaller-than-expected labor market impact of immigration") and their data reject it.

**(b) Beerli, Ruffner, Siegenthaler & Peri 2021 AER** [SOURCE: DOI 10.1257/aer.20181779; NBER
w25302 PDF read]. Swiss free movement for cross-border workers, DiD on travel time to the border,
1991–2011 business censuses plus innovation surveys. Shock size: **+10 pp of 1998 employment** in
municipalities within 15 minutes of the border. Effects: incumbent skill-intensive firms grew in
size, **labour productivity (value added per FTE)**, R&D employment, patent applications and
product innovation; **share of new establishments +4 pp** in the closest regions ("relatively
quick capital adjustments to immigration"); wages of **highly educated natives rose**.
**IMPORTANT CAVEAT, and it cuts against using this as a disconfirmer:** the cross-border workers
were disproportionately **tertiary-educated** (IT, R&D, analysts, consultants), and the effects
are concentrated in firms that reported **pre-reform skill and R&D-personnel shortages**. The
paper does note CBW "were on average less educated than natives before the reform," but the
identified mechanism runs through **high-skill** scarcity relief. **This is evidence that
high-skill immigration raises innovation. It is weak evidence about low-skill immigration and
automation.** Do not use it as the counterweight to Arctotherium; use Clemens & Lewis 2022.
[GAP] exact Beerli table coefficients not transcribed — the PDF table body did not extract cleanly.
**(c)** Mitaritonna, Orefice & Peri (French firms) and Orefice & Peri (job matching): identified as
the remaining pro-side firm-level papers but **[GAP] not fetched; no coefficients — do not cite.**

### 7. [INFERENCE] Magnitude sketch — what the automation channel would cost, and why it cannot be booked

Assumptions, all stated: (i) take Lewis's **IV** estimate ln(machinery/worker) = **−0.59** per unit
Δ(U/S), so a **+0.10 rise in dropouts per HS-equivalent → −5.9 % machinery per worker**; (ii)
Cobb-Douglas with capital share **α = 0.33**, so output per worker falls by α × 5.9 % ≈ **1.9 %**;
(iii) US output per worker ≈ **$174,000** (2024 GDP ≈ $29.2T ÷ ≈168M employed); (iv) at the sample
mean U/S = 0.3 with high-school-equivalents ≈ 77 % of the workforce, a +0.10 move in U/S
corresponds to adding low-skill workers equal to **≈7.7 % of the workforce**, i.e. about **13
incumbent workers per added low-skill worker**.

Arithmetic: 1.9 % × $174,000 ≈ **$3,300 lost output per incumbent worker per year**; × 13
incumbents ≈ **$43,000 per added low-skill immigrant worker per year**. Using the **OLS** capital
coefficient (−0.16) instead gives 0.5 % → **≈$11,000**. So the naive range is **$11k–$43k per
low-skill immigrant worker-year**, i.e. **1.3× to 5.2× the −$8,286 per-adult-year extended fiscal
gap** for the Mexican second generation (§12 of
`research/immigration-mexican-origin-generation-incarceration-2026-09-16.md`, se 443; the ASEC-2026
replication gives −8,727, se 594).

**Four reasons that number must NOT be put in the ledger, in descending order of severity:**
1. **Lewis measured output per worker directly and got nothing.** ln(VA/worker) IV = **−0.03
   (0.24)**. At Δ(U/S)=0.10 the 95 % interval spans roughly **−5 % to +4 %**. The $43k is imputed
   from the *capital* coefficient through an assumed production function; the *productivity*
   coefficient that would confirm it is a precise-enough-to-be-useless zero.
2. **Metro-level capital shortfalls do not aggregate to national ones.** Capital is nationally
   mobile. A plant that does not buy the machine in Fresno does not destroy the machine; the
   general-equilibrium counterfactual is unidentified by any study in this file.
3. **Peri 2012 gets the opposite sign at the level where aggregation matters:** capital intensity
   −0.08 (0.13), TFP **+1.37 (0.27)**.
4. **Randomised firm-level evidence says the sign is backwards:** Clemens & Lewis 2022 investment
   elasticity **+1.5 to +2.1**.

**Honest conclusion.** The automation channel is real as a *technique-choice* phenomenon —
Lewis, Danzer and San all find it, and Peri concedes it with an elasticity near −1. What no study
establishes is a **national, durable output cost**. The one setting where forced mechanisation was
largest and most persistent (bracero, San 2023, +3.3 % patents per pp, lasting 15–20 years) is also
the setting where the **incumbents lost anyway** (permanent farm-value decline). A fiscal ledger
that booked $11k–$43k per immigrant-year for foregone automation would be asserting a general-
equilibrium magnitude that the literature has not identified, in the face of the best-identified
study pointing the other way. **Recommended treatment in the essay: name the mechanism, quote
Lewis/Danzer/San, then state that the welfare cost is unmeasured and that the randomised evidence
runs against it. Do not monetise it.**

### Remaining gaps
- [GAP] Danzer published JPubE version: could not reconcile the brief's "+10 % low-skilled
  workforce → −3.3 pp automation-patent share" with the IZA WP's "−0.75 pp per immigrant per 1,000
  workers". Someone should open the published paper before that number goes in print.
- [GAP] Zhang 2024 (SSRN 5009570) unread. Peri 2016 JEP unread. Mitaritonna/Orefice & Peri unread.
  Hémous et al. JPE 2025 induced-automation coefficients unread. Beerli table values untranscribed.
- [GAP] No study anywhere links **US immigration enforcement to firm capital or automation.**
- [GAP] ACS per-capita income by nativity for the 8 San Joaquin counties — see below.

### 6b. ACS nativity split for the Valley — RESOLVED
[SOURCE: Census ACS 5-year 2023 API, tables B06011 (median income by place of birth) and B19301
(per capita income), pulled 2026-09-16.]

```
ACS 5-year 2019-2023, table B06011 (median income past 12 months by place of birth) and
B19301 (per capita income). 2023 dollars. Ratios are county / United States.

geography         med_all  med_bornInState  med_foreignBorn      pci |  all/US  bornInSt/US  pci/US
United States       39982            37423            37393    43289 |   1.000        1.000   1.000
Fresno              33875            35138            29407    31777 |   0.847        0.939   0.734
Kern                30912            31805            27145    29238 |   0.773        0.850   0.675
Kings               34210            34866            30532    26420 |   0.856        0.932   0.610
Madera              30316            31661            27426    29698 |   0.758        0.846   0.686
Merced              31343            31179            31045    27711 |   0.784        0.833   0.640
San Joaquin         38674            38133            37104    36192 |   0.967        1.019   0.836
Stanislaus          36126            37140            32546    33653 |   0.904        0.992   0.777
Tulare              31326            33532            26747    27550 |   0.784        0.896   0.636
```

**Mostly compositional, but not entirely.** Compare two columns. Per-capita income
(`pci/US`) runs **0.610 to 0.836** across the eight counties, a shortfall of roughly **29 % on
average** — that is the BEA gap, reproduced in a different dataset. Median income of people **born
in the state they live in** (`bornInSt/US`), the settled incumbent population, runs **0.833 to
1.019**, a shortfall of only about **9 %**, and **San Joaquin County is actually above the national
figure (1.019)** with Stanislaus at parity (0.992). The foreign-born column is lower again
(0.716–0.992 of the US foreign-born median).

So the decomposition is: **roughly two thirds of the Valley's per-capita income gap is
compositional** — more children, more non-earners, more low-income residents per capita — and
**roughly one third is a genuine shortfall in what settled incumbents earn**. Arctotherium's claim
that the Valley's incumbents were left behind is **directionally supported but about three times
smaller than the headline per-capita series implies.**

[INFERENCE] The residual incumbent shortfall is consistent with the mortmain story and equally
consistent with every other account of regional decline: agriculture's falling share of value
added, Kern's oil economy, and selective out-migration of the educated. **The ACS cross-section
cannot separate them and nothing in this file does.** Present the Valley series as the descriptive
fact Arctotherium is pointing at, with three qualifications attached: the break is **1980–2000**,
the ratio has been **flat since 2000**, and **two thirds of it is composition**.
