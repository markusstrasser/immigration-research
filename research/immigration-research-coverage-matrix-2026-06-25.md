# Research Coverage Matrix — "every possible research" bounded honestly (2026-06-25)

**Trigger.** Operator goal: *get every possible research on this topic across sociology, urbanism, economics, policy, crime — and get the datasets.* This doc is the **frame** (constitution principle #5, "name the frame"): it states per-domain what is **saturated** vs a **genuine frontier**, so "every possible" is a bounded, falsifiable claim, not a vibe. Filled by a 4-agent parallel research+acquisition pass; the parent integrates.

Instrument note: politically charged topic, LLM-assisted corpus, left-tilted academic field. Disconfirming / against-interest evidence is weighted as **higher-information** throughout (see `notes/llm-bias-caveat.md`).

## The frame — where the repo actually is, by the 5 named domains

| Domain | State | Evidence of saturation / gap |
|--------|-------|------------------------------|
| **Economics** (fiscal NPV, wage, labor supply) | **SATURATED — spine** | Fiscal ledgers, country tensor, microsim, Borjas supply-shock panel (1980-2023), E-Verify wage TWFE, assimilation profile. 57-dataset roadmap returned VEIN:SATURATED on fiscal axes. *Exception:* 4 named wage/fiscal **disconfirmers** never fetched → econ-disc agent. |
| **Crime** | **STRONG — recent** | Light TX (in-data), BJS SPI, SCAAP, INT-06 status spine, 188-spec curve (direction robust). Corpus has Light 2020, Abramitzky 2024 incarceration, homicide-disentangle 2020. Frontier is thin (enforcement/sanctuary *policy* evals) → folded into policy agent. |
| **Policy** (enforcement, legalization, sanctuary, refugee) | **PARTIAL — frontier** | E-Verify wage side + surge/EOIR covered; but DACA/IRCA legalization evals, Secure Communities/287g crime evals, sanctuary-crime nulls, refugee fiscal trajectories under-weighted. Several OA papers *identified but unfetched* (paper-gaps memo). → policy agent. |
| **Sociology** (assimilation, cohesion, enclaves, segregation) | **PARTIAL — frontier** | Corpus already strong on segmented-assimilation (2024/25), Putnam West-EU replication, ethnic networks/capital, deep-roots cluster-V. Gap: the trust **meta-analyses** (van der Meer-Tolsma), CILS/NIS datasets, intermarriage/linguistic indices, generational segregation. → socio agent. |
| **Urbanism** (housing incidence, sorting, agglomeration) | **THIN — biggest gap** | No dedicated urban frame. Saiz rent screen + receiver-node shelter stress only. No MSA rent × immigrant panel (4 warehouse theories pending on it). Housing-incidence ledger flagged missing by both red-team models. → urban agent. |

**Honest headline:** "every possible research" is *not* an open-ended infinite search. Economics and crime are at diminishing returns (saturated/strong). The real, fundable frontier is **urbanism > sociology > policy-disconfirmers**. This pass expands those three and executes the already-scouted econ disconfirmers.

## Corpus baseline (immigration-relevant, already in `research-mcp` corpus as of dispatch)

Already held — agents must NOT recount these as "new acquisitions":
- **Crime:** Light et al. 2020 (TX, PNAS); Abramitzky-Boustan-Jácome-Pérez-Torres 2024 (incarceration gap 1870-2020); homicide-incarceration-by-status TX 2020; "migrant regularization reduces crime" 2025.
- **Sociology:** Putnam-2007 West-European trust replication (2011); "Ethnic networks foster economic integration of refugees" (2019); "Segmented assimilation, then and now" (2025); "Assimilation Theories in the 21st Century" (2024); ethnic-identity transmission, Mexican Americans (2025); Borjas "Ethnic Capital & Intergenerational Mobility" (1992); "Inherited Trust and Growth" (2010); Guiso-Sapienza-Zingales culture; "How Deep Are the Roots of Economic Development?" (2012).
- **Economics:** Peri-Yasenov "Labor Market Effects of a Refugee Wave" (Mariel synthetic control, 2018) — **already in**, so econ-disc's Mariel delta = Clemens-Hunt 2019 + Borjas 2017 reappraisal; Ottaviano-Peri "Rethinking the Effect of Immigration on Wages" (2012); Cortes "Low-skilled immigration on US prices" (2008); "Immigration & Entrepreneurship in the US" (2020); Clemens place-premium (2008); "The new economic case for migration restrictions" (2019).

## Dispatch (4 parallel researcher agents, background; this run)

| Agent | Axis | Memo (on return) | Key deltas it must hit |
|-------|------|------------------|------------------------|
| `socio` | Sociology / cohesion | `immigration-sociology-frontier-2026-06-25.md` | van der Meer-Tolsma trust meta; CILS/NIS datasets; intermarriage/linguistic; generational segregation |
| `urban` | Urban & housing econ | `immigration-urbanism-frontier-2026-06-25.md` | **MSA rent × immigrant panel dataset map**; Saiz-2007 rent incidence; Card tipping/native-mobility; agglomeration |
| `policy` | Policy/enforcement | `immigration-policy-frontier-2026-06-25.md` | fetch 5 OA crime/enforcement papers; DACA/IRCA evals; Secure Communities/287g crime nulls; refugee fiscal |
| `econ-disc` | Econ disconfirmers | `immigration-economics-disconfirmers-2026-06-25.md` | Clemens-Hunt+Borjas-2017 Mariel; Dustmann-Frattini UK; US dynamic NPV + CBO 2024; Cato TX convictions |

## Integration log (parent fills as agents return)
- [ ] socio — returned? findings + new datasets + new corpus papers
- [ ] urban — returned? dataset map verdict (buildable now vs gated)
- [ ] policy — returned? fetch results table + new evals
- [ ] econ-disc — returned? confidence-ladder deltas

## Synthesis verdict (filled at close)
*(per-domain: did the frontier yield new load-bearing evidence, or confirm saturation? what's the single highest-value next acquisition? what stays gated/HUMAN.md?)*
