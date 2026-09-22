<!-- reader extraction, opus-low agent, 2026-09-22; every numeric row carries a verbatim quote re-found in the parsed corpus text with rg -F; parent spot-checked the rows cited in the memo -->
[SOURCE: Amuedo-Dorantes, Arenas-Arroyo, Mahajan, Schmidpeter, "Low-Wage Jobs, Foreign-Born
Workers, and Firm Performance", IZA DP No. 16438, Sept 2023 / this version July 2024;
doi:10.2139/ssrn.4568747. Parsed text:
/Users/alien/Projects/corpus/doi_10_2139_ssrn_4568747/parsed.pymupdf4llm@0.3.4+cfg-99914b93/page.md]

**Verdict:** A credible firm-level quasi-experiment — an unanticipated 7:00am EST cutoff in DoL
processing of H-2B applications filed on 1 Jan 2018 — showing that access to ~8 low-wage guest
workers raises firm revenue (elasticity ~0.14) and multi-year survival with essentially no
crowd-out of other employment and no measurable harm to competitors; the design is strong on the
first stage and pre-trends, but the survival result is the least robust to parallel-trends
violations and the paper cannot separate native from foreign-born incumbents.

## Population, period, unit

- **Unit:** the firm (LBD firm identifiers; establishment data collapsed to firm). ~3,300 firms
  that filed a Temporary Labor Certification (TLC) application with the Department of Labor on
  1 January 2018 — effectively the near-universe of 2nd-half-FY2018 H-2B applicant firms.
  Quarterly employment/payroll exist only for single-unit firms (91% of sample; 2,900–3,000
  firms). Revenues: 2,400 firms. Spillover regressions run on the whole 2017 US firm universe
  (6.2–6.7 million firms, 712k–744k county×6-digit-NAICS markets).
- **Period:** 2015–2021 for firm outcomes; **revenues only through 2018** ("data are only
  currently available through 2018", p.13). Treatment year is calendar 2018, hiring period
  calendar Q2–Q3 2018.
- **Workers:** H-2B is non-agricultural, non-college, temporary. Mean posted wage $13.24/hr;
  ~80% of postings below $15/hr. Landscaping is 52.6% of the 1 Jan 2018 applications; hotels/
  motels (maids and housekeeping) is the other main cell. So this is a **low-wage, seasonal,
  locally-traded-sector** population, not immigration in general.
- **Firms are large and productive relative to the US economy:** median research-sample revenue
  $2.1m vs ~$0.5–1.0m for the median US firm; median employment ~3× the average US employer
  (Table 2, p.15).

## Design and identification

**Source of variation — not a lottery.** On 1 Jan 2018 the DoL received ~81,000 TLC applications
(≈250% of the semi-annual 33,000 visa allotment), the first time the cap could be filled on the
first possible filing date. On **17 January 2018, after the fact**, DoL announced it would release
certifications by exact day *and time down to the millisecond*. 96% of applications received
before 7:00am EST were processed before the 27 Feb USCIS cutoff; only 19% of those received after
7:00am were. The firms could not have known this ex ante.

**Estimator:** continuous difference-in-differences / event study. Treatment is
`Prop Apps Before 7am_j` = the share of firm *j*'s 1 Jan 2018 applications filed before 7:00am
(0 for 27.8% of firms, 1 for 71.8%, strictly interior for 0.4%). Outcome is the
Davis-Haltiwanger-Schuh growth rate relative to base period (2017Q2 for quarterly, 2017 for
annual), which differences out the firm fixed effect while admitting zeros (needed because of the
survival effect). Controls: 6-digit-NAICS×year, state×year, prior-H-2B-user×year, and two
size-quartile×year fixed effects (2017 employment; number of 1 Jan 2018 TLC requests). Standard
errors clustered at the firm (spillovers: at the county×industry market).

**Why not RD:** the authors explicitly reject a regression discontinuity at 7:00am — "we observe
very few firms around the threshold, which leads to small sample problems" (fn.4, p.3).

**First stage (Figure 6 Panel D, p.19–20):** original-tranche 2HFY visa approvals "grew 75
percentage points more at early relative to late applicants" ≈ 8 extra approvals at the mean of
~22 applications. Adding the May-2018 supplemental tranche of 15,000 visas shrinks the gap to
about 64% of that (≈5.7 extra approvals), i.e. late applicants partially caught up in Q3.
IV first-stage F statistics 240.8 / 107.7 / 257.4 / 109.8 (Table 4, p.25).

**Placebo/pre-trend checks that pass:** no differential trend in TLC applications, in TLC
certifications (quality proxy), or in 1st-half-FY approvals *through* 2018; flat pre-trends in
quarterly employment and payroll; no differential employment on 12 March 2018 (after firms knew
the rule change but before any H-2B worker could start). Match rate to Census data is uncorrelated
with pre-7am timing (Table 1, p.14: −0.009 (0.008), −0.017 (0.011)).

**Approval→hire conversion:** DoS issues fewer visas than USCIS approves; the only public data
(DHS 2016 report to Congress) gives conversion rates 57.0%–88.1%, and the authors use **78%** as
the benchmark. Every "per hire" number below is an approval estimate divided by 0.78, i.e.
**assumed, not measured**.

## Headline estimates

All standard errors clustered at the firm level unless noted. "pp" = percentage points of the DHS
growth rate. Page numbers are the printed page numbers in the parsed text.

| Outcome | Estimate | SE / CI | Table–figure, page | Verbatim quote (≤40 words) |
|---|---|---|---|---|
| First stage: 2HFY original-tranche approvals, event study 2018 | +75 pp | 95% CI in Fig. 6D | Fig. 6 Panel D, p.19–20 | "The results indicate that original tranche visa approvals grew 75 percentage points more at early relative to late applicants." |
| First stage: initial-tranche + cap-exempt approvals per 1 Jan application | 0.369 | (0.023), F=240.8 | Table 4 col.(1), p.25 | "each application sent in before 7 am on January 1, 2018, resulted in 0.369 additional USCIS approvals for initial tranche or continuing H-2B visas" |
| First stage: all 2HFY approvals (incl. supplemental) per application | 0.262 | (0.025), F=107.7 | Table 4 col.(2), p.25 | "each application sent in before 7 am on January 1, 2018, resulted in 0.262 additional approvals for initial tranche, continuing, or supplemental USCIS H-2B visas" |
| Total firm employment per H-2B approval, 2018Q2 (2SLS) | +0.737 | (0.125), 95% CI ≈ [0.49, 0.98] | Table 4 col.(3), p.25 | "Approvals_j 0.737*** 0.796*** 5,453*** 6,157***" ; "Each i129 approval resulted in 0.74 additional employees in 2018Q2." |
| Total firm employment per H-2B approval, 2018Q3 (2SLS) | +0.796 | (0.192), 95% CI ≈ [0.42, 1.17] | Table 4 col.(4), p.25 | "each 2HFY H-2B visa approval leads to 0.80 additional employees per approval in Q3" |
| Employment per H-2B **hire** (approvals ÷ 0.78) | Q2 ≈ 0.95; Q3 ≈ 1.02 | derived, no separate SE | text p.24–25 | "our estimates suggest an increase of around 0.95 employees per H-2B hire" ; "this estimate suggests an increase of 1.02 employees per H-2B hire in Q3" |
| Implied crowd-out of non-H-2B workers | ~1 displaced per 20 hires | authors call it a lower bound | text p.24–25 | "it would take 20 H-2B hires to crowd out one non-H-2B worker" |
| Firm payroll per H-2B approval, 2018Q2 | +$5,453 (2009 USD) | (860) | Table 4 col.(5), p.25 | "firm payroll increased by 5,453 USD (in 2009 dollars) per approval in 2018Q2" |
| Firm payroll per H-2B approval, 2018Q3 | +$6,157 (2009 USD) | (1,355) | Table 4 col.(6), p.25 | "and by 6,157 USD (in 2009 dollars) per approval in 2018Q3" |
| Payroll per **hire** vs. one H-2B worker's own quarterly pay | $6,992 (Q2) / $7,894 (Q3) vs ~$4,990 expected | derived | text p.25 | "these figures translate to 6,992 USD (in 2009 dollars) per H-2B hire in Q2 and 7,894 USD (in 2009 dollars) per H-2B hire in Q3" |
| Quarterly employment growth gap, 2017Q2→2018Q2 (event study) | +18 pp | 95% CI in Fig. 7 | Fig. 7, p.22 | "early applicants experience an 18 percentage point higher growth in employment and a 19 percentage point higher growth in payroll between the second quarter of 2017 (2017Q2) and the second quarter of 2018" |
| 2HFY employment (mean Q2,Q3), single cross-section 2018 | +0.149 | (0.022); no-controls 0.142 (0.021); Δlog 0.204 (0.036); PPML 0.102 (0.017) | Table 5 Panel B, p.31 | "Prop Apps Before 7a _j_ 0.142*** 0.149*** 0.204*** 0.102***" |
| 2HFY payroll, 2018 | +0.163 | (0.024); Δlog 0.258 (0.058); PPML 0.118 (0.017) | Table 5 Panel C, p.31 | "Prop Apps Before 7a _j_ 0.161*** 0.163*** 0.258*** 0.118***" |
| Annual revenue growth, 2018 | +0.055 (≈5.5 pp) | (0.014); unweighted 0.050 (0.013); Δlog 0.052 (0.020); PPML 0.037 (0.020) | Fig. 8A p.27, Table 5 Panel A p.31 | "Prop Apps Before 7a _j_ 0.051*** 0.055*** 0.052** 0.037* 0.050***" ; "early applicants experience more than 5 percentage point higher revenue growth rates compared to late applicants in 2018" |
| Revenue elasticity w.r.t. H-2B approvals | 0.11 | no SE reported | text p.27, fn.41 | "This translates to a revenue elasticity with respect to H-2B approvals of 0.11 and an elasticity with respect to H-2B hires of approximately 0.14." |
| Revenue elasticity w.r.t. H-2B **hires** | ≈0.14 | derived via 78% conversion | text p.27, fn.41 | (same quote as above) |
| Probability firm still active, 2018 | +2.05 pp | 95% CI in Fig. 8B | Fig. 8 Panel B, p.27 | "The likelihood of remaining active is 2.05 percentage points higher among early applicants in 2018" |
| Probability firm still active, 2021 | +4.18 pp | 95% CI in Fig. 8B | Fig. 8 Panel B, p.27 | "an impact that rises to 4.18 percentage points by 2021" |
| Active operation, pooled 2018–2021 | +0.029 | (0.009); no-controls 0.027 (0.008) | Table 5 Panel D, p.31 | "Prop Apps Before 7a _j_ 0.027*** 0.029***" |
| Spillover — direct effect on early applicants (emp/payroll/rev/active) | 0.161 / 0.209 / 0.056 / 0.021 | (0.031)/(0.035)/(0.024)/(0.009) | Table 6, p.33 | "_β_ : Direct Effect 0.161*** 0.209*** 0.056** 0.021**" |
| Spillover — onto **late-applicant** participants whose rivals applied early | 0.037 / 0.087 / 0.030 / −0.017 | (0.046)/(0.048)/(0.033)/(0.012) | Table 6, p.33 | "_ϕ_ : Participant Spillover Effect 0.037 0.087* 0.030 -0.017" |
| Spillover — "siphon" (direct effect eroded by early-applying rivals) | −0.040 / −0.095 / −0.013 / 0.011 | (0.054)/(0.057)/(0.036)/(0.015) | Table 6, p.33 | "_δ_ : Siphon Effect -0.040 -0.095* -0.013 0.011" |
| Spillover — onto **non-participant** firms in the same county×NAICS market | 0.002 / 0.003 / −0.002 / 0.004 | (0.005)/(0.007)/(0.005)/(0.004) | Table 6, p.33 | "_θ_ : Non-Participant Spillover Effect 0.002 0.003 -0.002 0.004" |
| Heterogeneity: extra employment effect in universal-E-Verify states | +0.133 | (0.071), p<0.10 | Table 7 Panel B col.(2), p.36 | "Prop Apps Before 7a _j_ 0.133*" ; "_×_ E-Verify _s_ ( _j_ ) (0.071)" |
| Heterogeneity: extra survival effect in universal-E-Verify states | +0.061 | (0.028), p<0.05 | Table 7 Panel D col.(2), p.36 | "Prop Apps Before 7a _j_ 0.061**" ; "_×_ E-Verify _s_ ( _j_ ) (0.028)" |
| Heterogeneity: revenue × E-Verify | +0.016 | (0.056), null | Table 7 Panel A col.(2), p.36 | "Prop Apps Before 7a _j_ 0.016" ; "_×_ E-Verify _s_ ( _j_ ) (0.056)" |
| Heterogeneity: per SD of initial productivity (log 2017 rev/worker) | rev +0.018 (0.037); emp +0.043 (0.034); payroll +0.030 (0.035); active +0.008 (0.011) | all null | Table 7 col.(3), p.36 | "Prop Apps Before 7a _j_ 0.018" ; "_×_ Std. Log 2017 Rev. pw _j_ (0.037)" |
| Parallel-trends breakdown values (Rambachan–Roth M̄^min) | rev 1.60; emp 2.52; payroll 3.16; active 0.70 (2018) and 0.41 (pooled) | — | Table 5, p.31 | "_M_ ¯ _[min]_, _H_ 0 : _β_ 2018 = 0 1.60" ; "2.52" ; "3.16" ; "0.70" ; "_M_ ¯ _[min]_, _H_ 0 : E[ _βt_ ] = 0 0.41" |

## What it says about

- **Native wages by skill/education:** *not studied directly.* No worker-level or nativity-split
  wage data. The only wage-adjacent evidence is firm payroll: payroll rose **more** per H-2B
  approval ($6,992–$7,894 in 2009 USD per hire) than one H-2B worker's own expected quarterly
  earnings (~$4,990 in 2009 USD, from a ~$450 weekly wage × 13 weeks), which the authors read as
  "some suggestive evidence of positive spillovers on non-H-2B workers" and as ruling out the
  "firms use H-2B to undercut wages" story. They caution this cannot see within-firm pay
  dispersion. Context: mean posted H-2B wage $13.24/hr, must exceed the BLS prevailing wage.
- **Native employment / crowd-out:** the central result. ~0.74–0.80 additional total employees per
  H-2B approval, ~0.95–1.02 per hire, so approximately one-for-one with the guest workers
  themselves and no room for large displacement. One-for-one crowd-out (β^IV = 0) is strongly
  rejected. **Critical caveat: the data have no nativity split** — "Since we do not observe firm
  workforce composition by nativity, we cannot explore whether any extant crowd-out affects
  foreign-born or natives" (fn.7, p.3). So "no crowd-out of natives" is an inference, not a
  measurement.
- **Housing prices, rents:** not studied.
- **Fiscal: taxes, transfers, public services, schooling:** not studied. The only fiscal touchpoint
  is mechanical: H-2B workers are subject to federal income tax, which is why they appear in the
  LBD employment and payroll counts. Program fees are described ($460 USCIS base, $1,500 premium
  processing, $190 DoS per worker) but never used as an outcome.
- **Firms, production, investment, profits:** revenue +~5.5 pp growth in 2018 (elasticity 0.11 per
  approval, ~0.14 per hire); survival +2.05 pp in 2018 rising to +4.18 pp by 2021; employment and
  payroll both up during Q2–Q3 2018 and reverting by Q4 when the workers leave. **Investment and
  profits are not observed** (no capex, no margin data — a real gap versus Clemens–Lewis). The
  authors infer price effects only theoretically: "in a wide swath of theoretical models featuring
  imperfect competition in the product market (e.g., Dixit and Stiglitz, 1977), revenue increases
  imply output price decreases."
- **Mechanism the authors claim:** genuine seasonal labor shortage in a tight low-wage market, not
  wage arbitrage. Evidence offered: employment rises ~one-for-one and reverts to zero in Q4; payroll
  rises at least proportionally to employment; effects are larger where E-Verify blocks unauthorized
  hiring, implying **H-2B workers and unauthorized workers are substitutes in production**; and
  H-2B users are large, productive, locally-traded-sector firms for whom the margin is survival.
- **Survival benchmark:** the 2.05–4.18 pp survival effect is compared to Bernard et al. (2006),
  where a one-SD rise in low-wage-country import competition cuts same-industry firm survival by
  2.2 pp over five years — i.e. losing H-2B access for half a fiscal year is comparable to years
  of import competition.

## Elasticities or parameters a model could transport

1. **Firm revenue elasticity with respect to H-2B hires: ≈0.14** (0.11 with respect to USCIS
   approvals). Estimated on ~2,400 US firms that applied for H-2B workers on 1 Jan 2018, mostly
   landscaping and hotels, median revenue $2.1m, 2018 only. Clemens–Lewis (2024) get ≈0.2 on the
   2021–22 lottery, a different and more productivity-selected sample.
2. **Total-employment response per additional low-wage guest worker: 0.74–0.80 per visa approval,
   0.95–1.02 per realized hire** (firm level, Q2 and Q3 2018). This is the transportable crowd-out
   parameter: it says the marginal H-2B worker adds himself to firm headcount and displaces
   essentially nobody, with the 95% CI on the Q2 estimate roughly [0.49, 0.98] per approval. It is
   a **firm-level**, not market-level, object — it does not net out reallocation across firms
   (though the spillover regressions bound that at near zero).
3. **Firm payroll response: $5,453 (Q2) and $6,157 (Q3) in 2009 USD per approval**, i.e. ~$6,992
   and ~$7,894 per hire, against an expected ~$4,990 of own-earnings per quarter for a full-time
   H-2B worker. The residual $2,000–$2,900 per hire is the upper bound on incumbent pay gains or
   unmeasured crowd-in in that sample.
4. **Firm survival semi-elasticity: +2.05 pp in the treatment year, +4.18 pp four years later**,
   per unit of `Prop Apps Before 7am` (i.e. per ~8 extra approvals at the mean firm). Note the
   weak parallel-trends breakdown value here (M̄^min = 0.70 and 0.41) — transport this one with
   caution.
5. **Substitution between H-2B and unauthorized labour:** signed but not parameterized. The
   E-Verify interaction (+0.133 on employment, p<0.10; +0.061 on survival, p<0.05) is the only
   quantitative handle and it is an interaction on a binary state policy, not an elasticity of
   substitution. **It cannot be read as a CES ε.**
6. **Approval-to-hire conversion rate: 78%** (range 57.0–88.1% across years, from a 2016 DHS
   report to Congress). Any "per hire" number above is `per approval / 0.78`; this is an assumed
   input, and it is the single largest non-sampling uncertainty in the transportable numbers.
7. **Wage level of the population:** mean $13.24/hr (SD $2.44, median $13.29), ~80% below $15/hr,
   >99% below $22/hr, in nominal 2018 dollars for calendar Q2–Q3 2018.

**Caution for the parent's production-term model:** this paper estimates **no elasticity of
substitution between natives and foreign-born workers**, within education cells or otherwise. It
cannot be used to set ε. What it can discipline is the *firm-level* crowd-out assumption (near
zero for seasonal low-wage guest workers in these sectors) and an output/revenue response to a
marginal low-skill foreign worker. It is also a seasonal, temporary-visa population with no
dependants in the US, so it says nothing about the stationary fiscal comparison the parent is
building.

## Authors' stated limitations and external-validity notes

- **No nativity split in the outcome data** (fn.7, p.3; fn.39, p.25). They cannot say whether the
  residual crowd-out falls on natives or on other foreign-born workers, and lean on H-1B results
  (Doran et al. 2022; Mahajan et al. 2024) and Clemens–Lewis to argue any displacement hits other
  foreign-born workers first.
- **No individual compensation data,** so within-firm pay dispersion is invisible: "To fully
  understand these dynamics, a closer examination of within-firm pay structures is necessary."
- **Revenue coverage ends in 2018**, so the revenue effect is one year only; survival is the only
  medium-run outcome.
- **RD infeasible** at the 7:00am threshold due to few firms near the cutoff; and the cutoff is not
  perfectly sharp — 4% of pre-7am applications were not processed on time and 19% of post-7am ones
  were, with no explanation from DoL and no predictability in their data.
- **Survival is the least robust result**: Rambachan–Roth breakdown values of 0.70 (2018) and 0.41
  (pooled) mean parallel-trends violations smaller than those already observed pre-period would
  overturn it. Revenue (1.60), employment (2.52) and payroll (3.16) are much safer.
- **Partial treatment leakage:** the 15,000 supplemental visas announced 25 May 2018 let some late
  applicants hire after mid-June, shrinking the first stage to ~64% of the original-tranche effect
  and biasing Q3 comparisons toward zero.
- **Sector and firm selection:** dominated by landscaping (52.6%) and hotels; H-2B users are
  larger and more productive than the average US firm; concentrated in locally traded sectors.
  The conclusion says explicitly: "it remains an open question whether these results are specific
  to the H-2B visa program or applicable to 'low-skill' U.S. immigration more broadly."
- **Treatment is continuous, not binary** — a small number of firms filed both before and after
  7:00am.
- The market-level generalization ("H-2B visas could have been made available to late applicants
  without generating large, adverse effects on local markets") rests on imprecise spillover
  estimates; the authors say "standard errors do not permit definitive conclusions."

## How this differs from the Clemens–Lewis lottery design

| | Amuedo-Dorantes et al. (this paper) | Clemens & Lewis (2024) |
|---|---|---|
| Source of variation | Unanticipated DoL processing-rule change, 7:00am EST cutoff on 1 Jan 2018, announced 17 Jan *after* filing | The 2021 and 2022 USCIS H-2B visa **lotteries** |
| Anticipation | None possible — the rule did not exist at filing time | Fully anticipated; firms knew they were entering a lottery before applying, so selection into applying may respond |
| Randomization | Quasi-random, not literal; a continuous DiD with pre-trend and placebo tests rather than an RD | Literal randomization |
| Data | Census restricted administrative data: LBD (establishment panel from tax records), BRFIRM_REV revenues, linked to DoL TLC and USCIS i129 records. Near-universe of applicant firms | A **survey** of participant firms |
| Sample selection | Near-universe of 1 Jan 2018 applicants; 92.8% match rate | Survey respondents, "positively selected on productivity relative to our sample" |
| Outcomes reachable | Revenue, employment, payroll, multi-year survival; no investment, no profits | Production, revenues, **investment**, employment |
| Spillovers | Can test competitors and non-participants across the entire 6.2m-firm US economy by county×NAICS market | Cannot — no comparison firms outside the survey |
| Horizon | Survival through 2021 (medium run) | Shorter, contemporaneous |
| Revenue elasticity | ≈0.14 per hire (0.11 per approval) | ≈0.2 |
| Crowd-out | No significant crowd-out or crowd-in in headcounts; payroll rises more than proportionally | "a statistically imprecise amount of crowd in of other employment"; rules out substantive native displacement |

The authors position their contribution as: medium-run **survival** (new), **competitor and
non-participant spillovers** on the full firm universe (new), and a replication of the revenue and
no-crowd-out findings under an *unanticipated* shock, a different year, and a different method —
"the similarity of findings across these studies further buttresses the case that H-2B workers are
essential to the operation of H-2B users."

## Data availability

**Restricted.** The firm outcomes come from US Census Bureau confidential microdata (Longitudinal
Business Database 2021 vintage; BRFIRM_REV) accessed at a Federal Statistical Research Data Center
under **FSRDC Project Number 2105**, disclosure release **CBDRB-FY24-P2105-R11439**, with help from
the Philadelphia FSRDC. All firm counts are rounded and medians are reported as means between the
40th and 60th percentile per Census disclosure rules. No replication package is mentioned.

The two H-2B inputs are **public**: DoL Office of Foreign Labor Certification performance data
(TLC applications, including the millisecond timestamp for 1 Jan 2018) and the USCIS H-2B Employer
Data Hub (i129 approvals). The linkage is a fuzzy name/state/city/ZIP match described in
Appendix A. An earlier manuscript version had firm size and age heterogeneity analyses "available
upon request."

---

**Verification:** every numeric row in the Headline estimates table carries a verbatim quote that
was re-found in the parsed text with `rg -F`. 30 of 30 quote fragments tested returned a hit;
3 initially failed on line-wrap boundaries and were re-tested with corrected in-line fragments
(`1.02 employees per H-2B hire`, `57.0% to 88.1%`, `data are only currently available through
2018`), all of which then hit. **31 numeric table rows verified, 0 dropped.**
