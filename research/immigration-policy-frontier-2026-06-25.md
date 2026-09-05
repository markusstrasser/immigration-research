# Immigration policy frontier — evidence and identification (2026-06-25; repaired2026-09-05)

**Verdict:** Several quasi-experiments find reductions in recorded crime following particular legalization policies; several enforcement/sanctuary designs fail to detect aggregate crime effects. That evidence does not prove a universal policy sign, eliminate all mechanisms, or make every rollout an exogenous instrument. A title, abstract or publication venue is not a full design review. [SOURCE references below; INFERENCE]

## Legalization, crime and reporting

| Source | What is supported | Limit |
|---|---|---|
| Baker2015, AER Papers & Proceedings, DOI10.1257/aer.p20151041 | IRCA-related geographic/timing variation is used to estimate lower crime, particularly property crime; June summary reports3–5% | Exposure differences require identification assumptions; this is not necessarily the same individuals observed before/after a randomly assigned legalization |
| Pinotti2017, AER, DOI10.1257/aer.20150355 | Permit-quota click-day RD links applications with individual records; published abstract reports **−0.6 percentage points from1.1% baseline** | About54.5% relative reduction and an implied0.5% level; a local RD estimate requires continuity/no precise sorting and has a local applicant population |
| Freedman, Owens & Bohn2018, AEJ:Policy, DOI10.1257/pol.20150165 | IRCA’s eligibility/employer-sanction contrast supplies evidence for employment-access mechanisms in recorded felony charges | Different cohorts and simultaneous channels do not prove that jobs are the exclusive mediator or that every legalization works identically |
| Mastrobuoni & Pinotti2015, AEJ:Applied, DOI10.1257/app.20140039 | Legal-status changes associated with EU enlargement used to study released inmates’ recidivism | Selected released-inmate risk set, removal and policy-specific external validity; June full text not read |
| Ibáñez, Rozo, Bahar & Urbina2026, JDE179:103667, DOI10.1016/j.jdeveco.2025.103667 | Publisher abstract reports reduced recorded migrant offending and increased women’s reporting of domestic/sexual crimes under Colombian regularization | Distinct offender/reporting outcomes; income, documentation/enforcement and trust are proposed mechanisms, not proof of jobs-only mediation |

Primary links: https://www.aeaweb.org/articles?id=10.1257/aer.p20151041; https://www.aeaweb.org/articles?id=10.1257/aer.20150355; https://www.aeaweb.org/articles?id=10.1257/pol.20150165; https://www.aeaweb.org/articles?id=10.1257/app.20140039; https://www.sciencedirect.com/science/article/pii/S0304387825002184.

The June Pinotti transcription “1.1–2.2 … to0.4” was inconsistent with the primary abstract and with its own roughly-half description. The corrected abstract values give `0.6/1.1≈54.5%`. This is a recorded-crime policy effect among the design’s relevant applicants, not a universal latent-offending estimate. [SOURCE: AEA abstract; RECALCULATION; INFERENCE]

Comino, Mastrobuoni & Nicolò2020 correctly study the **1986 US amnesty** using victimization/admin data. The primary abstract reports very low inferred unauthorized reporting and an approximately20-point reporting increase among amnesty applicants. This concerns victims’ reporting, not direct admission of their own offending. Reporting changes can affect recorded offenses and resulting arrests, but the study does not supply a universal numerical correction to every immigrant/native crime ratio. [SOURCE: https://doi.org/10.1002/pam.22221]

## Enforcement and sanctuary

Miles & Cox2014 (DOI10.1086/680935), Kang & Song2021 (DOI10.1093/jleo/ewab013), Hausman2020 (DOI10.1073/pnas.2014673117) and Kubrin & Bartos2020 (DOI10.1080/24751979.2020.1745662) study different enforcement/sanctuary changes. Several report no detectable aggregate crime increase/decrease for the tested policy/outcome. That is not proof of zero or evidence that deterrence and incapacitation are individually absent: other channels, noisy measurement and confidence intervals matter. Treat the net policy outcome separately from the removal of a particular offender. [SOURCE: linked DOIs; INFERENCE]

Kubrin–Bartos’s quoted conclusion is "**neither robust nor sufficiently
   large to rule out a null effect**". Its short post-period and state-level aggregation limit precision and heterogeneity analysis. Hausman’s finding of fewer deportations and no detectable crime effect does not generalize automatically to all sanctuary rules. [SOURCE: https://doi.org/10.1080/24751979.2020.1745662; https://doi.org/10.1073/pnas.2014673117]

Staggered activation dates are treatment timing, not automatically a valid instrument or a clean difference-in-differences design. Administrative rollout rationales do not prove parallel trends or exclusion restrictions. Check policy targeting, anticipation, spillovers, reporting coverage and heterogeneous treatment timing before estimating a causal effect. E-Verify is a separate policy and must be coded by scope/date. [INFERENCE]

## DACA and refugee outcomes

The DACA source leads retain distinct outcomes: Kuka–Shenhav–Shih2020 (DOI10.1257/pol.20180352) on schooling/teen births; Hsin–Ortega2018 (DOI10.1007/s13524-018-0691-6) on CUNY schooling/work tradeoffs; Villanueva Kiser–Wilson2024 (DOI10.17848/wp24-395) on mobility; Tran2025 (DOIs10.1017/dem.2025.5 and10.1111/coep.70009) on labor and child coverage. A positive schooling outcome and a dropout response in a different subgroup need not conflict. Schooling/labor outcomes do not directly establish a crime effect, and eligibility rules alone do not certify the design. [SOURCE: named primary records; June read depths varied]

**Evans & Fitzgerald2017, w23498:** Uses2010–2014 ACS records, imputes likely refugee status from origin/arrival cohorts and constructs a synthetic20-year profile for arrivals aged18–45. Annual taxes tend to exceed the covered benefits after year8. That is **annual crossover, not cumulative payback at year8**. Their discounted20-year taxes-minus-covered-costs estimate is about+$21,000; it is not a followed-person panel or an all-ages/all-costs refugee fiscal theorem. [SOURCE: https://www.nber.org/papers/w23498; https://leo.nd.edu/assets/240441/44914_w23498.pdf, pp.6–7]

## Dataset leads and valid uses

| Source | Useful measurements | Before claiming causality or full coverage |
|---|---|---|
| TRAC, https://trac.syr.edu/immigration/ | FOIA-derived enforcement/court counts and characteristics | Check availability, reporting gaps and court venue versus residence; a count is not a risk rate |
| DHS/OHSS yearbooks, https://www.dhs.gov/ohss/topics/immigration/yearbook | Defined admission/enforcement flows | Flows are not resident stocks; series definitions and periods differ |
| Secure Communities activation records and replication packages | County treatment timing | Establish identification; do not label every rollout an instrument |
| E-Verify legislative records | Effective date and employer scope | Verify scope/year; the existing QWI earnings outcome has no nativity field |
| ORR/RPC arrivals and Annual Survey of Refugees | Cohort characteristics and available short-run outcomes | Verify access and selection; placement is not automatically random conditional only on nationality |

The QWI sex-by-education API’s `EarnS` is stable/full-quarter average monthly earnings, not native-born hourly pay. The existing wage-side label was wrong. [SOURCE: https://api.census.gov/data/timeseries/qwi/se/variables.html]

Dataset-card access details and corpus inventory were June records, not a fresh September certification. The historical fetch log is retained below; failed fetches are transport limits, while metadata acquisition is not full-text verification. The bounded search did not establish that287(g)-specific or DACA-crime literature is absent.

## Historical June acquisition log — read-depth record only

## (A) FETCH RESULTS

| # | Paper | DOI | Status |
|---|-------|-----|--------|
| 1 | Ousey & Kubrin (2018) Immigration and Crime, Annu Rev Criminol | 10.1146/annurev-criminol-032317-092026 | **METADATA-ONLY** — saved to corpus (S2 `33034e4c…`, 310 cites); full-text PDF unfetchable (annualreviews JS-gated, not on Sci-Hub). NOTE: corpus crime memo already synthesized this paper's body in a prior session (r = -0.031 weighted mean, quoted) — the analytic content is captured even though the PDF isn't re-fetchable now. |
| 2 | Light, He & Robey (2020) PNAS 117(51):32340 | 10.1073/pnas.2014704117 | **ALREADY IN CORPUS, full text ✓** (`10.1073_pnas.2014704117`, PMC7768760, pdf_path present). No fetch needed. |
| 3 | Abramitzky et al. (2024) Law-Abiding Immigrants, NBER w31440 | 10.3386/w31440 | **FETCHED ✓** (`doi_10_3386_w31440`, 63k chars full text, quality-assessed). [The metadata-only SSRN copy `10dc2477…` (DOI 10.2139/ssrn.4878020) was already in corpus but had no body; w31440 supplies the full text.] |
| 4 | Butcher & Piehl (2007) NBER w13229 | 10.3386/w13229 | **FETCHED ✓** (`doi_10_3386_w13229`, 126k chars full text, quality-assessed). |
| 5 | Hausman (2020) Sanctuary policies, PNAS 117(44):27262 | 10.1073/pnas.2014673117 | **METADATA + KEY FINDINGS captured** (abstract saved; results archived via `save_source` from PMC7959582). Full-text PDF exists (PMC7959582/pdf/pnas.202014673.pdf) but research-mcp `fetch_paper` rejected it — **transport-layer failure**, not paywall (the same fetcher got PNAS Light-He-Robey fine). Findings verified: sanctuary policies cut deportations ~1/3 (2010-15), no-conviction deportations fell >50%, violent-conviction deportations unchanged, NO detectable crime effect. |

**Fetch summary: 2 newly fetched full-text (#3, #4); 1 already-present full-text (#2); 2 metadata/findings-captured (#1, #5) where the MCP PDF fetcher failed (annualreviews JS-gate; PNAS transport quirk — both bodies' key results are nonetheless captured).**



## Revisions

- **2026-09-05 — Corrected policy magnitudes, mediation, null inference and refugee payback.** See [material-inference repair](../decisions/2026-09-05-material-inference-repair.md). Earlier dated revision entries describe the historical state, including superseded conclusions.
