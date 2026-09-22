# Seven papers from the Marginal Revolution archive, read in full

Date: 2026-09-21. [SOURCE / CALCULATION / FRAMING-SENSITIVE] Reading record and two calculations;
narrative authorship remains operator-owned. Follows section 5 of the
[blog audit](immigration-marginal-revolution-claims-audit-2026-09-18.md), which listed these
papers from abstracts only.

**Result:** None of the seven changes the $165–197bn conditional net cost. Two identify benefits
to other residents that the [complete account](immigration-complete-annual-account-2026-09-20.md)
omits. The nursing-home channel is real in the literature but transfers weakly to Mexican-origin
immigrants: its Medicaid value for the Mexico-born is bounded at **$2.3–14.6bn a year**, $5.6bn
at the preferred coefficient weighted by who staffs direct care. Native–immigrant complementarity
is the larger open item: the account's production term ($8.8–13.3bn) treats union and outside
workers as perfect substitutes within two skill groups, while a 2026 general-equilibrium model
with imperfect substitution implies native wage gains of **$27–80bn** from half of all
unauthorized workers, offset by losses to other immigrants. The municipal-bond paper I flagged
as bearing on the service-response parameter cannot settle it.

## What was read and how

[SOURCE: [lane README, reading protocol and notes](../infra/immigration-fiscal/mr_leads_papers_2026_09_21/README.md)]
Each paper's primary PDF was converted to text and read whole by a reader agent that had to give
a page or table reference and a verbatim quote for every number. I re-checked the decisive
numbers of each note against the cached text. Figures that exist only as images supplied no
numbers.

| Paper | Design and evidence level | Transfers to the Mexican-origin account? |
|---|---|---|
| Butcher, Moran, Watson, NBER w29520 (published *Rev. Int. Econ.* 2022) | Shift-share IV, commuting zones, Census 1980–2000; one design, fragile to year-by-state effects | Partly: treatment is all-origin; the identifying variation is south-western |
| Grabowski, Gruber, McGarry, NBER w34791 (2026), "Is Immigration Good for Health?" | Shift-share IV weighted by health-occupation propensity, 18.0m Medicare beneficiaries, 2008–2019 | Barely: 1.2% of Mexican immigrants work as aide, nurse or doctor against 14% of Philippine immigrants (p.16) |
| Cornaggia, Cornaggia, Israelsen, SSRN 5026977 (Jan 2025) | Reduced form on quintiles of a push-predicted court-filing index; no first stage, no robustness section | No: 2010–2023 recent-arrival flow, largely not Mexican; local governments only |
| Cravino, Levchenko, Ortega, Pandalai-Nayar, NBER w34790 (2026), "The Economic Impact of Mass Deportations" | Calibrated general-equilibrium model; no estimation, no standard errors, no fiscal block | As a check on one assumption only |
| Boustan, Cai, Tseng, NBER w31434 | Shift-share IV with a full diagnostic battery, 152 high-income California districts | No: no estimate for Hispanic arrivals |
| Cesur, Yıldırım, NBER w33163, "The Misery of Diversity" | Cross-country IV on predicted genetic diversity, 151 countries | No: the authors make no claim about immigration |
| NBER w34327, Black–white earnings gap by generation | Descriptive CPS 1995–2024; no standard errors | Contrast only |

## 1. Elder care

**Butcher–Moran–Watson.** [SOURCE: notes `butcher_moran_watson_w29520.md`] Treatment is the
share of the working-age population that is foreign-born with less than one year of college, all
origins. A ten-point rise lowers institutionalization of the US-born aged 65 and over by 1.5
points (2SLS −0.151, SE 0.027, F 28.3, Table 2) and of those 80 and over by 3.8 points (−0.380,
SE 0.074). Aide wages fall about 8% at the 1980–2000 shift and aide employment rises (Table 8).
The authors concede the result loses significance with year-by-state effects (−0.061, SE 0.058,
F 4.8; p.25), and dropping California gives −0.090 with F 9.2. The 2000–2010 decade has a
wrong-signed first stage. The Census cannot separate nursing homes from other institutions
(p.10). The paper contains no cost, mortality or quality estimate. [INFERENCE] State Medicaid
home-care waivers expanded over the same years at the level where the coefficient dies, and the
paper never controls for them.

**Grabowski–Gruber–McGarry.** [SOURCE: notes `grabowski_gruber_mcgarry_w34791.md`] Per 1,000
more working-age immigrants in a metro area: 143 more foreign-born health workers (SE 21), a
statistically empty effect on native health workers (+44, 95% interval −52 to +139), 9.8 fewer
deaths a year among Medicare beneficiaries (−0.00761, SE 0.00208, F 21.2, Table 4) and 17 fewer
users of skilled nursing (Table 5). Medicare spending does not move (p.23); Medicaid is not
examined. Africa, India and the West Indies carry 68% of the identifying weight (Table A3);
Mexico is outside the top five. The instrument weighted by work *outside* health care gives
−0.00252 (SE 0.00370) and turns positive beside the health-weighted one (Table 4 cols 3–4): that
is the estimate relevant to a low-health-propensity inflow. The abstract's 5,000 deaths is the
first-year effect of one extra cohort of 325,000 (fn.12), and the coefficient cannot be scaled to
a resident stock.

**Who staffs direct care in 2024.** [DATA: `derived/acs_care_inputs.csv`, ACS 2024 one-year PUMS]
3.68m employed aides and nursing assistants; 28.1% foreign-born. The foreign-born Mexico-born are 150,000:
4.1% of the workforce and 14.5% of its foreign-born part, against 37.7% of the
Butcher–Moran–Watson treatment population. Mexican-origin workers of every generation are
416,000, or 11.3% of the workforce, while the union is 12.0% of residents and 4.9% of people 65
and over (2.99m of 61.2m).

**Bound.** [CALCULATION: `elder_care_bound.py` → `derived/elder_care_bound.csv`; model output]
The less-educated foreign-born are 8.95% of the working-age population and the Mexico-born part
is 3.37%. Applying each published coefficient to that share, to 52.1m US-born elderly, and
pricing each avoided institutional resident at Medicaid's $78.9bn of nursing-facility spending
over 1.43m institutional residents ($55,051; CMS NHE 2024, Table 15):

| Coefficient | Weighted by labour share | Weighted by share of foreign-born care workers |
|---|---:|---:|
| Preferred, −0.151 | 265,000 fewer residents, $14.6bn | 102,000, $5.6bn |
| Without California, −0.090 | 158,000, $8.7bn | 61,000, $3.4bn |
| Year-by-state, −0.061 (not significant) | 107,000, $5.9bn | 41,000, $2.3bn |

All-payer values are 2.8 times larger ($6.3–40.7bn), most of it private. Ledger: Medicaid
nursing-facility spending. Unit: 2024 dollars a year. Gross: no offset for Medicaid home-care
spending on those who stay at home. Out of window: a coefficient identified on a 3.3-point change
is applied to a 3.37-point share, and the per-resident price is overstated because CMS totals
include residents under 65. Against the $165–197bn headline the bound is 1–9%.

## 2. Local budgets and municipal bond yields

[SOURCE: notes `muni_bonds_unauthorized_ssrn5026977.md`] The treatment is a twelve-month flow of
immigration-court charging documents (TRAC), predicted from origin-country conditions, allocated
by county shares lagged one year and entered as quintiles; the paper never converts a quintile
into people. The unconditional yield effect is a null (top quintile +1.4bp, SE 1.7, Table IV).
Yields fall 5.7bp in "structurally tight" counties and rise 8.6bp in sanctuary counties (10%
level), both interaction results. Total revenue at two years: +0.2% (SE 1.0), an interval of
−1.8% to +2.2% that brackets every spending effect. Education +2.0% (SE 1.0) at two years;
welfare cash assistance +10.3% at one year, fading to +3.7% (SE 4.6). No total-expenditure
outcome is estimated, transfers received from states are not examined, off-year finance data are
interpolated, a language model assigned issuers to counties, and no shift-share diagnostic is
run. [INFERENCE] "Not offset by higher tax revenues" is an imprecise zero. The paper cannot
discriminate between the account's response cases (18.5–25.8% break-even, 63–66% schools,
full proportionality), and its flow is the 2021–2023 Venezuelan, Haitian and Nicaraguan surge.
My September 21 note in the blog audit that it "speaks to the least-identified parameter" is
withdrawn.

## 3. The removal model and the account's production term

[SOURCE: notes `cravino_levchenko_ortega_pandalai_w34790.md`] Removing half of 4.95m unauthorized
workers leaves the aggregate long-run real wage exactly unchanged (Corollary 1, p.18): capital
adjusts and the model has no scale effects. Native wages fall 0.33% because natives and
immigrants are imperfect substitutes (elasticity 3, the midpoint of two published estimates,
1.3 and 4.6; p.23), and the counterpart is a gain of 3.2% for authorized and 12.2% for remaining
unauthorized immigrants. Farm consumer prices rise 1.2%, other sectors −0.2% to +0.4%. The
short-run native gain of 0.15% rests on a capital share of 0.5 that the authors call overstated
(fn.10). There is no tax, transfer or public-service block, and "natives" include naturalized
citizens.

[CALCULATION] With BEA 2024 wages and salaries of $12,410bn (NIPA Table 1.10) and a native
wage-bill weight of 0.942 [INFERENCE, backed out of Corollary 1 by the reader], the native loss
from the removal is **$38.6bn a year**, $26.8bn at elasticity 4.6 and $80.4bn at 1.3: about
$15,600 per removed worker.

[INFERENCE] The account's production term is built differently. It has two skill groups, puts
union and outside workers in the same group as perfect substitutes, and so credits other
residents only with the skill-composition gain: $8.8–13.3bn for a union earning 8.35% of national
earnings [DATA: `matched_benefits_2026_09_19/derived/skill_composition.csv`]. With a
native–immigrant nest inside each skill group, a native's wage gain per unit of immigrant labour
is `s_F × (1/ε − (1 − a_j)/σ)` in the same group and `s_F × a_j/σ` in the other, where `s_F` is
the immigrant earnings share, `a_j` the group's share of labour income, `σ` the elasticity
between skill groups and `ε` between natives and immigrants. At `ε = 3` that adds tens of
billions of dollars to natives' side, and other immigrants, who are closer substitutes, lose a
large part of it; "other residents" in the account contains both. The sign of the headline is
not at stake at these magnitudes, the size is. This is the largest untested assumption found in
this pass. Executing it needs earnings by skill, nativity and citizenship for union and outside
workers from the CPS file the production lane already reads.

## 4. Three context papers

[SOURCE: notes in the lane] **Boustan–Cai–Tseng:** each Asian student arriving in a high-income
California district is followed by 1.5 white departures (IV −1.470, SE 0.268, F 56), to other
districts and not to private schools (published as a *Journal of Urban Economics* Insight, 141,
2024). Within the sample the effect shrinks as district income rises, −4.5, −2.3 and −0.84 by
tercile, and the best-instrumented top tercile (F 97) is below one for one (Appendix Table 2).
The Hispanic and Black coefficients in the paper measure
whether Asian arrivals coincide with minority arrivals; white flight from Hispanic arrivals is
not estimated, and the proposed mechanism, academic competition, does not carry over. It leaves
the repo's non-reproduction for Hispanic inflows (ladder 141) where it was. **Cesur–Yıldırım:**
diversity is predicted genetic heterozygosity instrumented by prehistoric migratory distance, in
one cross-section of countries; immigration appears in a literature footnote only. It does not
bear on ladder 133–134. **Black–white gap:** second-generation Black women earn 7.7 log points
above white women at the median and men 11.0 below, against −34.0 for native Black men (Table
1); 812 and 961 second-generation observations in 2019–24 and no standard errors. Both results
are conditional on working: with non-workers included the men's gap more than doubles to −26.9
(Table S3, p.39), and the women's advantage fell from about +19 log points in 1995–2000 to +8 in
2019–24. A by-origin contrast for the Mexican second-generation result, with selection of the
parents untested.

## What changes

Headline unchanged. Ladder 164–167 added; FAQ entries 13 and 14 added and entry 2 extended. Open:
the native–immigrant nest in the production term, and a Medicaid long-term-care line in the
complete account if the operator wants the bound carried as a sensitivity.

[DISCONFIRMATION] Two results cut against the account's size: an omitted Medicaid saving of up to
$14.6bn and an omitted native wage gain of tens of billions. One result that seemed to support a
full spending response does not survive reading.

[INSTRUMENT] LLM-assisted reading and calculation on a politically charged topic. Reader agents
were told to steel-man each paper first; every criticism tagged [INFERENCE] is the reader's or
mine, not the authors'. See `notes/llm-bias-caveat.md`.

## Revisions

- 2026-09-22: The Mexico-born numerators counted both nativity codes for birthplace Mexico, adding
  about 4,000 care workers and 162,000 working-age adults who were US citizens at birth, while the
  denominators and the Butcher–Moran–Watson treatment are foreign-born only. `elder_care_bound.py`
  now takes foreign-born Mexico-born only: shares 14.5% and 37.7% (were 14.9% and 38.5%), bound
  $2.3–14.6bn (was $2.3–14.9bn), preferred $5.6bn (was $5.8bn). Still 1–9% of the headline. Found by
  the [number audit](../infra/immigration-fiscal/number_audit_2026_09_22/AUDIT.md), item 1.
