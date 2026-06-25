# Immigration Conclusion Audit Review Context

Date: 2026-06-16
Repo: .

## Task

Review the attached immigration research surface for statistical, mathematical, logical, econometric, or data-science issues in the conclusions. Focus on overclaiming, rank/order claims unsupported by evidence, causal language from descriptive models, denominator/base-rate mistakes, extrapolation beyond support, and ambiguity between prediction/scenario/measurement.

Do not perform prose/style review except where wording creates a technical claim. Do not introduce unsupported factual claims. Treat reviewer output as hypotheses: each finding must cite exact file:line evidence from this packet and explain the statistical/logical issue. Separate confirmed issues from speculative preferences.

## Recent Commits In Scope

4ce274d [research] Leave E-Verify mechanism unresolved — coefficients are nonsignificant
ee75d49 [research] Scope Caplan worker channel — evidence surface is partial
be5b33b [research] Leave surge-election mechanism unresolved — coefficient is association
e855764 [research] Mark Card setup as prediction — not measured claim
30f5a83 [research] Separate E-Verify employment — not deportation validation
5f0ae2e [research] Keep capacity politics descriptive — model signal not cause
e6bb622 [research] Narrow cycle summary — E-Verify is margin-bound
f5082dd [research] Bound Hanson counterfactual — not surge wage forecast
f29fc72 [research] Bound cash-economy caveat — substitution is unmeasured
beae99b [research] Bound Caplan channel ranking — evidence surface is partial
811f988 [research] Scope local-burden channel — wage margin is bounded
1622662 [research] Tighten crime-rate caveats — denominator is conditional

## Git Status Notes

The repo has unrelated dirty/untracked immigration files. Do not assume untracked files are current truth unless quoted below. research/immigration-INDEX.md is dirty and deliberately out of this packet.

## Files


--- BEGIN FILE: CYCLE.md ---
     1	# CYCLE — Immigration causal analysis (autonomous)
     2	
     3	Started: 2026-04-18
     4	Goal: Acquire LEHD QWI, Saiz elasticity, E-Verify timing, DACA timing -> estimate native wage compression, link rent burden to housing supply elasticity, run staggered DiD on E-Verify and DACA -> test the observed E-Verify QWI wage margin and refine federal-vs-local incidence split.
     5	
     6	Working dir: `sources/immigration-causal/data/` (gitignored)
     7	Scripts: `sources/immigration-causal/scripts/`
     8	Output memos: `research/immigration-causal-*.md`
     9	
    10	## Context constraints
    11	- 15 active claude processes → rate-limit mode (subagent-light, avoid Codex dispatch)
    12	- External SSD unmounted → existing warehouse unavailable, work standalone on new datasets
    13	- 13 GiB free internal disk → keep LEHD pulls targeted (5 states max, by-county aggregations)
    14	
    15	## Queue (executing in order)
    16	1. Saiz 2010 elasticity (smallest, fastest)
    17	2. E-Verify state mandate panel (text data)
    18	3. DACA timing + ACS-eligibility coding
    19	4. LEHD QWI county × industry × demographic for AZ, MS, CA, TX, NV
    20	5. Wage compression analysis on LEHD
    21	6. Saiz × PUMA rent burden link
    22	7. E-Verify staggered DiD
    23	8. Synthesis memo: observed E-Verify wage-channel update
    24	
    25	## Discoveries
    26	- QWI `se` endpoint supports multi-state, multi-quarter batching → 36 API calls returned full 2003-2023 panel for 51 states × 9 industries × 4 education = 151k rows in ~2 min (vs ~20h with naive per-cell loop).
    27	- Saiz 2010 elasticity correlates inversely with FB share at MSA level (descriptive correlation, n=237). Top FB-share quintile median elasticity 1.51 vs bottom 3.40.
    28	- E-Verify mandates show no statistically significant positive QWI wage effect on native low-skill workers in any of 12 specifications. This rejects large Borjas-style native wage gains in the observed mandate margin, not every Borjas wage claim or surge/mass-shock regime.
    29	- E-Verify mandates show a ~6% drop in stable E1 W-2 employment in exposed industries (marginal). Consistent with Bohn-Lofstrom-Raphael 2014 AZ finding. Combined: W-2 employment falls while QWI wages show no significant positive response; capital, output, relocation, cash-economy substitution, hours, and composition remain candidate channels rather than measured mechanisms.
    30	
    31	## Autonomous (done)
    32	- 2026-04-18 Saiz 2010 MSA elasticity acquired (269 MSAs, 33 KB). Reflection: MIT Urban Economics Lab Google Drive link works one-shot; no scraping needed.
    33	- 2026-04-18 E-Verify state mandate panel compiled from literature (Bohn-Lofstrom-Raphael 2014, Orrenius-Zavodny 2015). 18 states with mandates, 9 with binding all-employer-equivalent scope.
    34	- 2026-04-18 DACA timeline + ACS-eligibility coding documented. Execution deferred (disk constraint, no PUMS pull this cycle).
    35	- 2026-04-18 QWI 2003-2023 state×year×quarter×industry×education panel pulled via batched API (151k rows, 2 MB).
    36	- 2026-04-18 Saiz × ACS rent merge — descriptive cross-section, immigrants concentrate in inelastic MSAs.
    37	- 2026-04-18 E-Verify TWFE on QWI — bounded observed mandate-margin wage update, not a full Card-vs-Borjas verdict.
    38	- 2026-04-18 Synthesis memo + index/ladder updates.
    39	
    40	## Verification Results
    41	- Saiz finding: descriptive cross-section with monotonic gradient across quartiles. Replicates known pattern (top-FB MSAs are coastal/inelastic — Miami, LA, SF, NY). PASS as descriptive claim; needs IV for causal interpretation.
    42	- E-Verify TWFE: pre-trends flat in event study, supporting the identifying assumption for the observed mandate-margin check. The result is consistent with bounded Card-side wage evidence and passes at the level of "large Borjas-style native wage gains are rejected in this design"; it is not a direct replication of Card-Peri / Foged-Peri or a test of surge, mass-deportation, or extreme counterfactual regimes.
    43	
    44	## Known blockers
    45	- SSD unmount blocks reuse of existing warehouse (`acs_origin_*`, `origin_puma_household_context_2023`, etc.). Workaround: rebuild minimal PUMA rent table from Census API for Saiz merge. Not a blocker for LEHD/E-Verify/DACA analyses.
    46	
    47	<!-- knowledge-index
    48	generated: 2026-04-19T03:46:13Z
    49	hash: bdb887477d5c
    50	
    51	cross_refs: research/immigration-causal-*.md
    52	
    53	end-knowledge-index -->
--- END FILE: CYCLE.md ---

--- BEGIN FILE: research/immigration-conclusion-audit-running-fixes.md ---
     1	# Immigration conclusion audit — running fixes
     2	
     3	**Purpose:** running ledger of statistical, mathematical, logical, and data-science issues fixed while auditing immigration conclusions.
     4	
     5	**Rule:** each entry names the broken conclusion, the evidence that changed it, what was edited, and what remains unresolved. This is not a final immigration position memo.
     6	
     7	---
     8	
     9	## 2026-06-15 — School-burden denominator correction
    10	
    11	### Issue
    12	
    13	The school-burden memo and a stale exported CSV still supported the conclusion that Mexico-origin adults had a crude annual federal-minus-school balance of about **-$13.5k/adult**. That result used the `origin_fiscal_scenario_2023` scenario subset denominator (~436,819 adults) after multiplying area-weighted per-pupil school spend by household school-age children. [DATA]
    14	
    15	That denominator was wrong for a full Mexico-origin adult-stock conclusion. The live tensor now uses the full Mexico microsim adult denominator (~8,496,334 adults). [DATA]
    16	
    17	### Evidence Checked
    18	
    19	```sql
    20	SELECT *
    21	FROM v_three_layer_annual
    22	WHERE population_group = 'mexico_origin';
    23	```
    24	
    25	Current DuckDB result from `warehouse/immigration_fiscal_union.duckdb`:
    26	
    27	| federal_per_adult | school_per_adult | net_crude_per_adult | weight_adults |
    28	|------------------:|-----------------:|--------------------:|--------------:|
    29	| 1519.278 | 771.285 | 747.993 | 8496334 |
    30	
    31	Scenario source check from `warehouse/immigration_lifetime_evidence.duckdb`:
    32	
    33	| origin | scenario adults | avg federal net | area-wtd per pupil | school-age kids/HH | HH weight |
    34	|--------|----------------:|----------------:|-------------------:|-------------------:|----------:|
    35	| Mexico | 436819 | 1519.278 | 20907.09 | 0.9718 | 322540 |
    36	
    37	The old ~-$13.5k conclusion came from dividing the household school burden by the scenario subset. The corrected school burden is about:
    38	
    39	`20907.09 * 0.9718 * 322540 / 8496334 = ~$771/adult` [INFERENCE]
    40	
    41	### Fixes Made
    42	
    43	1. Updated `research/immigration-school-burden-per-adult-2026-06-15.md`:
    44	   - Mexico-origin row now reads `$1,519` federal, `$771` school, `+$748` crude annual.
    45	   - Removed the stale verdict that Mexico looks far worse than natives on crude static federal-minus-school math.
    46	   - Added a revision note explaining the scenario-denominator bug.
    47	
    48	2. Updated `research/immigration-scenario-composition-2026-06-15.md`:
    49	   - Replaced obsolete `~$21/pupil` text with post-F-33 `~$20,907/pupil`.
    50	   - Added a warning not to use `436,819` scenario adults as the full Mexico-origin stock denominator.
    51	
    52	3. Updated `research/immigration-lifetime-fiscal-generators.md`:
    53	   - Rewrote G-LIF-K01 so future audits check both F-33 units and per-adult denominator discipline.
    54	
    55	4. Updated `infra/immigration-fiscal/build/build_country_fiscal_tensor.py`:
    56	   - The tensor builder now exports `three_layer_annual_2023.csv` from the live `v_three_layer_annual` view.
    57	
    58	5. Regenerated canonical staged CSVs under `infra/immigration-fiscal/build/stage3_proto/`, including `three_layer_annual_2023.csv`, from the live DuckDB view.
    59	
    60	### Current Conclusion
    61	
    62	The corrected finding is narrower and less rhetorically satisfying: the built annual **federal-minus-school** layer is **positive for Mexico-origin adults** under the current full-stock microsim denominator. [DATA]
    63	
    64	This does **not** prove Mexico-origin immigration is all-government fiscally positive. The lifetime NPV, state/local surge, enforcement, courts, and episodic shelter layers are still separate and cannot be collapsed into this crude annual layer. [INFERENCE]
    65	
    66	### Remaining Risk
    67	
    68	The full-stock denominator may understate school incidence for recent-arrival or unauthorized subgroups if those subgroups are younger and more child-heavy than the full Mexico-born 25-64 stock. That is a legal-status/cohort split, not a license to reuse the scenario denominator for a full-stock conclusion. [INFERENCE]
    69	
    70	---
    71	
    72	## 2026-06-16 — NAS age-25 benchmark relabeled; current-stock NPV claim killed
    73	
    74	### Issue
    75	
    76	Several memos described the warehouse `lifetime_npv` rollup as "Mexico lifetime NPV" or treated the `+$387.7B` multiply-out as if it were the lifetime value of the current Mexico-born adult stock. The live tensor actually multiplies current ACS education weights by NAS Table 8-13 cells for an immigrant entering at **age 25**. [DATA]
    77	
    78	That is a useful composition benchmark, but it is not an actual remaining-lifetime NPV for current residents. Current Mexico-origin adults in the microsim are not a cohort of new age-25 entrants: only `17.4%` are age `25-34`, while `53.2%` are age `45-64`. [DATA]
    79	
    80	### Evidence Checked
    81	
    82	NAS source text around Table 8-13 states that the table compares an immigrant entering at age 25 with a native-born person followed from age 25. [SOURCE: local NAS 2017 PDF via `pdftotext`; `external/lifetime/nas/nas_2017_immigration_economic_fiscal_full.pdf`]
    83	
    84	Live DuckDB result:
    85	
    86	```sql
    87	SELECT population_group, fiscal_layer, effect_order,
    88	       ROUND(weight_adults,0) AS w,
    89	       ROUND(value_per_adult_weighted,2) AS per_adult,
    90	       ROUND(value_total_usd/1e9,3) AS total_b
    91	FROM v_country_fiscal_rollup
    92	WHERE population_group='mexico_origin'
    93	  AND fiscal_layer IN ('federal_annual','lifetime_npv');
    94	```
    95	
    96	| layer | adults | per adult | total |
    97	|-------|-------:|----------:|------:|
    98	| federal_annual | 8,496,334 | $1,519.28/yr | $12.908B/yr |
    99	| lifetime_npv | 8,496,334 | $45,631.19 | $387.698B |
   100	
   101	Current Mexico-origin age mix:
   102	
   103	| age band | adults | share |
   104	|----------|-------:|------:|
   105	| 25-34 | 1,482,136 | 17.4% |
   106	| 35-44 | 2,493,309 | 29.3% |
   107	| 45-54 | 2,656,957 | 31.3% |
   108	| 55-64 | 1,863,932 | 21.9% |
   109	
   110	### Fixes Made
   111	
   112	1. Updated `research/immigration-mexico-npv-population-synthesis-2026-06-15.md`:
   113	   - Reframed `+$45,631/adult` and `+$387.7B` as **synthetic NAS age-25 education-mix benchmarks**.
   114	   - Added the current-age distribution warning.
   115	   - Replaced "NAS mix negative for Mexico falsified" with the narrower claim that `<HS`-only application is falsified by education mix, while actual current-stock NPV remains unmeasured.
   116	
   117	2. Updated `research/immigration-lifetime-unified-theory-2026-06-15.md`:
   118	   - Relabeled the verifiable anchor as a synthetic age-25 benchmark.
   119	   - Corrected the Mexico federal annual total: full microsim stock is about `$12.9B/yr`; `$664M/yr` is the scenario subset only.
   120	   - Corrected receiver-vs-federal dominance language to match denominators.
   121	
   122	3. Updated `research/immigration-country-fiscal-tensor-2026-06-15.md`:
   123	   - Replaced stale pre-college-cell negative NAS rows with current positive synthetic benchmark rows.
   124	   - Added a limitation that age-25 NPV benchmarks are not current-stock remaining-lifetime estimates.
   125	
   126	4. Updated `research/immigration-lifetime-fiscal-generators.md`:
   127	   - Added G-LIF-Q06: age-25 NPV benchmark is not current-stock NPV.
   128	   - Corrected the remittance comparison to distinguish scenario-subset federal net from full-stock federal net.
   129	
   130	5. Updated `infra/immigration-fiscal/build/build_country_fiscal_tensor.py`:
   131	   - Tensor row notes now label `lifetime_npv` as a synthetic age-at-arrival-25 benchmark applied to current ACS education weights.
   132	
   133	### Current Conclusion
   134	
   135	The `+$45,631/adult` and `+$387.7B` numbers should be read only as **current education mix × NAS age-25 cells**. They kill a crude claim that Mexico-origin adults should all be mapped to the `<HS` NAS cell, but they do **not** establish the actual lifetime NPV of the current Mexico-born stock. [INFERENCE]
   136	
   137	The corrected full-stock annual federal proxy is about `$12.9B/yr`; `$664M/yr` is a scenario-subset calculation and should not be used against whole-stock or city-episodic totals without denominator matching. [DATA]
   138	
   139	---
   140	
   141	## 2026-06-16 — Local school-flow unit comparison corrected
   142	
   143	### Issue
   144	
   145	`research/immigration-lifetime-country-approx-brainstorm-2026-06-15.md` still contained an iteration-table verdict saying **"Local per-pupil ≪ federal annual"** and calling it confirmed by `~$21k/pupil vs ~$1.5k federal/adult`. That comparison mixed units and was numerically backwards: `$21k/pupil` is not less than `$1.5k/adult`, and neither number is comparable until the school value is bridged to an adult denominator. [DATA]
   146	
   147	The same table still carried superseded Mexico and MX+Central America lifetime rows around `−$79k`/`−$80k`, which came from the older `<HS`-heavy-only approximation rather than the current ACS education-mix benchmark. [DATA]
   148	
   149	### Evidence Checked
   150	
   151	Live DuckDB rollup:
   152	
   153	```sql
   154	SELECT population_group, fiscal_layer, effect_order,
   155	       ROUND(value_per_adult_weighted,2) AS per_adult,
   156	       ROUND(value_total_usd/1e9,3) AS total_b,
   157	       ROUND(weight_adults,0) AS adults
   158	FROM v_country_fiscal_rollup
   159	WHERE fiscal_layer IN ('federal_annual','lifetime_npv')
   160	  AND population_group IN ('mexico_origin','fb_lt_hs','mx_ca_cluster');
   161	```
   162	
   163	| population | layer | per adult | total |
   164	|------------|-------|----------:|------:|
   165	| Mexico-origin | federal annual | $1,519.28/yr | $12.908B/yr |
   166	| Mexico-origin | synthetic age-25 NPV benchmark | $45,631.19 | $387.698B |
   167	| FB `<HS` | synthetic age-25 NPV benchmark | −$109,000 | −$837.868B |
   168	| MX + N. Triangle | synthetic age-25 NPV benchmark | $42,971.52 | $476.122B |
   169	
   170	Comparable school-layer row from `v_three_layer_annual` remains about `$771/adult/yr`, making the current crude annual federal-minus-school row `+$748/adult/yr` for Mexico-origin adults under the full-stock denominator. [DATA]
   171	
   172	### Fixes Made
   173	
   174	1. Updated `research/immigration-lifetime-country-approx-brainstorm-2026-06-15.md`:
   175	   - Replaced the stale Mexico and MX+Central America `~−$80k` lifetime rows with current synthetic age-25 benchmarks.
   176	   - Replaced the invalid `per-pupil ≪ federal annual` verdict with the comparable adult-denominator statement: `$771/adult` school burden vs `$1,519/adult` federal proxy.
   177	
   178	### Current Conclusion
   179	
   180	The useful conclusion is not that local per-pupil costs are small. The corrected conclusion is narrower: after bridging to the current full-stock adult denominator, the built Mexico school layer is smaller than the narrow federal proxy on an annual basis, leaving a crude `+$748/adult/yr` federal-minus-school row. [INFERENCE]
   181	
   182	This does not settle marginal school cost, descendant attribution, legal-status/cohort incidence, or receiver-city episodic costs. [INFERENCE]
   183	
   184	---
   185	
   186	## 2026-06-16 — Pre-rebuild sweep rows marked superseded
   187	
   188	### Issue
   189	
   190	Several still-indexed June 15 memos carried first-pass sweep rows after the underlying tensor had changed:
   191	
   192	- `immigration-europe-caucasian-fiscal-findings-2026-06-15.md` reported Mexico-origin lifetime NPV as `−$79k` and US foreign-born stock as `−$71k`, from the older `<HS`/HS-only NAS seed.
   193	- `immigration-sweep-cycles-13-22-2026-06-15.md` still reported Mexico crude annual `federal − school` as `−$13.5k/adult` and "Mexico ~4x worse than NH white US-born", from the scenario-subset school denominator.
   194	- `immigration-lifetime-unified-theory-2026-06-15.md` had a compressed thesis line implying Mexico's lifetime layer was simply negative.
   195	
   196	### Evidence Checked
   197	
   198	Current `v_three_layer_annual` rows:
   199	
   200	| population | federal/adult | school/adult | crude net/adult |
   201	|------------|--------------:|-------------:|----------------:|
   202	| Mexico-origin | $1,519.28 | $771.29 | $747.99 |
   203	| MX + N. Triangle | $1,519.02 | $1,091.46 | $427.55 |
   204	| EU27-origin | $4,694.65 | $63.71 | $4,657.82 |
   205	| NH white US-born | $2,746.33 | $6,023.53 | −$3,277.20 |
   206	
   207	Current `v_country_fiscal_rollup` lifetime rows:
   208	
   209	| population | layer | per adult |
   210	|------------|-------|----------:|
   211	| FB `<HS` | synthetic age-25 NPV benchmark | −$109,000 |
   212	| Mexico-origin | synthetic age-25 NPV benchmark | $45,631.19 |
   213	| US foreign-born stock | synthetic age-25 NPV benchmark | $212,535.19 |
   214	
   215	### Fixes Made
   216	
   217	1. Updated `immigration-europe-caucasian-fiscal-findings-2026-06-15.md`:
   218	   - Replaced stale negative Mexico and US-FB lifetime rows with current synthetic age-25 benchmark rows.
   219	   - Replaced the old "college+ missing" warehouse gap with the current caveat: benchmark is age-25 composition, not current-stock lifetime truth.
   220	
   221	2. Updated `immigration-sweep-cycles-13-22-2026-06-15.md`:
   222	   - Added a superseded/corrected status note.
   223	   - Replaced stale cycle tables and conclusions with current `v_three_layer_annual` values.
   224	
   225	3. Updated `immigration-lifetime-unified-theory-2026-06-15.md`:
   226	   - Clarified that the coexistence claim is federal annual positive, `<HS` lifetime negative, education-mix age-25 benchmark positive, and local episodic negative.
   227	
   228	### Current Conclusion
   229	
   230	The old negative Mexico rows were not independent evidence. They were stale artifacts of two fixed bugs: the scenario-subset school denominator and the incomplete NAS education-cell seed. [INFERENCE]
   231	
   232	---
   233	
   234	## 2026-06-16 — CHNV non-substitution headline reversed
   235	
   236	### Issue
   237	
   238	`research/immigration-causal-surge-2021-2024.md` still presented the active bottom-line claim that CHNV parole **did not substitute** legal flow for illegal flow and instead added on top. That claim had already been reversed by the later parser-bug decision record: the source series was OFO port-of-entry encounters, the program's own lawful channel, misread as total SWB encounters. [DATA]
   239	
   240	The confidence ladder had a later correction entry 34, but older entries 26 and 30 still appeared without inline supersession markers. [DATA]
   241	
   242	### Evidence Checked
   243	
   244	Corrected `chnv_pretrends/results.json`:
   245	
   246	| Nationality | USBP pre-6 mean | USBP post-6 mean | Change | OFO pre-6 mean | OFO post-6 mean |
   247	|-------------|----------------:|-----------------:|-------:|---------------:|----------------:|
   248	| Venezuela | 16,488 | 7,000 | −57.5% | 47 | 3,210 |
   249	| Cuba | 28,563 | 1,355 | −95.3% | 32 | 1,252 |
   250	| Nicaragua | 22,063 | 830 | −96.2% | — | — |
   251	| Haiti | 152 | 150 | ~flat | 5,585 | 5,658 |
   252	
   253	Other corrected anchors:
   254	
   255	- Event-time mean τ[0,+3]: `−2.17` log points.
   256	- Event-time mean τ[+6,+12]: `−1.83` log points.
   257	- Corrected total-CBP DiD: `β=+0.45`, `t=1.29`, null. [SOURCE: decision record]
   258	- The old `+787%` rise was the lawful OFO channel on a scrambled clock. [SOURCE: decision record]
   259	
   260	### Fixes Made
   261	
   262	1. Updated `research/immigration-causal-surge-2021-2024.md`:
   263	   - Replaced the active bottom-line CHNV claim with the corrected channel-substitution result.
   264	   - Replaced the stale Title-42 evidence summary with the corrected monthly path.
   265	   - Replaced the stale CHNV DiD section with USBP/OFO-separated evidence.
   266	   - Replaced the receiver-city political headline with the Hispanic-share-controlled `+2.4pp` correlational upper-bound.
   267	
   268	2. Updated `research/immigration-confidence-ladder.md`:
   269	   - Marked entries 26 and 30 as superseded by entry 34.
   270	
   271	### Current Conclusion
   272	
   273	CHNV did substitute lawful port flow for irregular between-port crossings in its initial year. It did **not** reduce total receiver load, because the lawful parole inflow still arrived and still belonged in city, shelter, and political ledgers. [INFERENCE]
   274	
   275	---
   276	
   277	## 2026-06-16 — Card-vs-Borjas wage verdict bounded to observed marginal policy variation
   278	
   279	### Issue
   280	
   281	`research/immigration-causal-synthesis-2026-04-18.md` still said **"For U.S. policy-relevant variation, Card wins"** and summarized the debate as **"Resolved for U.S. policy variation. Card."** That was too broad after later surge work. The same memo already had the correct caveat that mass-deportation and border-closure shocks have no direct empirical analog; later surge analysis also says the 2021–2024 regime is outside the pre-2021 marginal-policy variation. [DATA]
   282	
   283	### Evidence Checked
   284	
   285	Local claim surfaces:
   286	
   287	- `immigration-causal-synthesis-2026-04-18.md` E-Verify/QWI evidence: native low-skill wage effects were null under observed staggered enforcement mandates. [SOURCE: memo]
   288	- `immigration-confidence-ladder.md` entry 29: "Static-cycle Card-wins finding is BOUNDED to marginal-policy variation; surge is OUTSIDE that variation." [SOURCE: memo]
   289	- `immigration-causal-surge-2021-2024.md`: wage estimates for the 2021–2024 surge period remain unmeasured; mass-deportation enforcement is outside the E-Verify/sanctuary variation. [SOURCE: memo]
   290	
   291	### Fixes Made
   292	
   293	1. Updated `research/immigration-causal-synthesis-2026-04-18.md`:
   294	   - Replaced "Card wins" with "Card-side pattern wins for observed marginal enforcement variation."
   295	   - Replaced "resolved" with "bounded to observed marginal U.S. policy variation."
   296	   - Made explicit that surge and mass-shock regimes remain open.
   297	
   298	### Current Conclusion
   299	
   300	The wage-channel evidence rejects large Borjas-style wage losses for the observed E-Verify/sanctuary-style policy variation in the repo. It does **not** prove workers are unaffected under the 2021–2024 surge, mass deportation, border closure, or other capacity-constrained shock regimes. [INFERENCE]
   301	
   302	---
   303	
   304	## 2026-06-16 — Paradigm synthesis bounded wage and newcomer-ratio claims
   305	
   306	### Issue
   307	
   308	`research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md` still contained two stale summary claims:
   309	
   310	1. "Card wins decisively" and "Future repo memos should treat this as settled" for the wage channel.
   311	2. Domestic U.S.-origin newcomer flow was summarized as `~33x` recent immigration at the median county.
   312	
   313	Both were too broad. Later surge work bounds the wage result to observed marginal enforcement variation, and the corrected internal-vs-immigrant newcomer memo replaced the older `33x` annualized stock proxy with ACS `B07001_081E`, giving about `21.7x` for the ratio of medians and `20.5x` for the median county-level ratio among counties with nonzero moved-from-abroad share. The IRS series is domestic U.S.-origin movement, not native-only identity. [DATA]
   314	
   315	### Evidence Checked
   316	
   317	- `research/immigration-confidence-ladder.md` entry 29: static-cycle Card-wins finding is bounded to marginal-policy variation; surge is outside that variation. [SOURCE: memo]
   318	- `research/immigration-causal-surge-2021-2024.md`: 2021–2024 surge wage estimates remain unmeasured; mass-deportation enforcement is outside observed E-Verify/sanctuary variation. [SOURCE: memo]
   319	- `research/immigration-causal-internal-vs-immigrant-newcomers.md`: current median county comparison is about `4.59%` IRS `Total Migration-US` inflow versus `0.21%` ACS moved-from-abroad, with ratio of medians `21.7x` and median county-level ratio `20.5x`. [SOURCE: memo]
   320	
   321	### Fixes Made
   322	
   323	1. Updated `research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md`:
   324	   - Replaced "Card wins decisively" with the bounded claim that the Card-side pattern wins for observed marginal wage variation.
   325	   - Removed the "settled" language for surge/mass-shock regimes.
   326	   - Replaced `33x` newcomer-ratio language with the corrected `20–22x` descriptive range, unit caveat, and domestic-movement caveat.
   327	
   328	### Current Conclusion
   329	
   330	The paradigm synthesis now carries the same scope discipline as the later claim ledger: marginal enforcement wage evidence is not surge evidence, and county newcomer comparisons are descriptive domestic-vs-abroad denominator corrections, not direct burden estimates. [INFERENCE]
   331	
   332	---
   333	
   334	## 2026-06-16 — Surge memo removes stale heading frames
   335	
   336	### Issue
   337	
   338	`research/immigration-causal-surge-2021-2024.md` qualified two stale prior-cycle claims in body text, but its section headings still carried the old frames:
   339	
   340	1. "Card wins decisively for U.S. policy variation."
   341	2. "`33x` native to immigrant newcomer ratio at median county."
   342	
   343	Those headings were doing rhetorical work against the corrected evidence. The first overstated scope; the second mixed an outdated ratio with a native-identity label unsupported by the IRS `Total Migration-US` measure. [DATA]
   344	
   345	### Evidence Checked
   346	
   347	- `research/immigration-causal-surge-2021-2024.md`: surge wage estimates remain unmeasured; the surge and mass-deportation regimes sit outside observed E-Verify/sanctuary variation. [SOURCE: memo]
   348	- `research/immigration-causal-internal-vs-immigrant-newcomers.md`: current median comparison is `21.7x` ratio of medians and `20.5x` median county-level ratio; IRS `Total Migration-US` is not native-only. [SOURCE: memo]
   349	
   350	### Fixes Made
   351	
   352	1. Replaced the Card heading with "Card-side pattern for marginal pre-surge policy variation — surge caveat."
   353	2. Replaced the `33x` native/immigrant heading with a domestic-vs-abroad median ratio caveat.
   354	3. Weakened the receiver-node paragraph to an estimand caveat: the median county comparison does not measure concentrated receiver-city shelter, legal, language, or school burdens.
   355	
   356	### Current Conclusion
   357	
   358	The surge memo now says what the evidence can support: marginal pre-surge wage evidence stays bounded, and median domestic-vs-abroad flow comparisons cannot dismiss receiver-node burden channels. [INFERENCE]
   359	
   360	---
   361	
   362	## 2026-06-16 — Confidence ladder marks receiver-swing causal sentence stale
   363	
   364	### Issue
   365	
   366	`research/immigration-confidence-ladder.md` entry 28 still contained the sentence "Magnitude implausibly large for non-immigration causes alone." Entry 31 later says that phrase should not be reused, and entry 36 closes the Hispanic-share control with a bounded `+2.4pp` receiver coefficient. Leaving the sentence unmarked created a grep hazard: an agent could quote the old causal-strength language while missing the later correction. [DATA]
   367	
   368	### Evidence Checked
   369	
   370	- `research/immigration-confidence-ladder.md` entry 31: the "implausibly large" phrase is a plausibility assertion doing causal work and should not be reused. [SOURCE: memo]
   371	- `research/immigration-confidence-ladder.md` entry 36: Hispanic-share control leaves receiver coefficient about `+2.4pp`, still cross-sectional and policy-endogenous; use as bounded upper-bound framing. [SOURCE: memo]
   372	- `research/immigration-causal-surge-2021-2024.md`: current most-defensible reading uses the controlled `+2.4pp` as the bounded claim and keeps confounders unresolved. [SOURCE: memo]
   373	
   374	### Fixes Made
   375	
   376	1. Kept entry 28 append-only, but marked its final causal-implausibility sentence as superseded by entries 31 and 36.
   377	2. Added an inline warning not to reuse the sentence and to use the controlled `+2.4pp` upper-bound framing instead.
   378	
   379	### Current Conclusion
   380	
   381	The receiver-city election evidence remains a medium-strength correlation that survived the named Hispanic-share kill-test, not a causal proof that the surge alone drove the full raw GOP swing. [INFERENCE]
   382	
   383	---
   384	
   385	## 2026-06-16 — Paradigm synthesis narrows rent-welfare claim
   386	
   387	### Issue
   388	
   389	`research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md` said "Rent exposure IS welfare loss." That was stronger than the Saiz memo supports. The source evidence is a strong cross-sectional pattern: immigrants concentrate in low-elasticity MSAs with higher rents, and regulatory constraint predicts foreign-born share better than topographic unavailability in the decomposition. It does not identify immigrant-specific rent causation or net welfare incidence. [DATA]
   390	
   391	### Evidence Checked
   392	
   393	- `research/immigration-causal-saiz-elasticity-rent.md`: status is "Cross-sectional descriptive"; welfare-loss implication is `MODERATE` and needs IV identification to attribute causation to immigrant inflow specifically. [SOURCE: memo]
   394	- `research/immigration-causal-synthesis-2026-04-18.md`: safer phrasing is "rent exposure is closer to welfare loss in destination markets" and should be elasticity-conditional. [SOURCE: memo]
   395	- `research/immigration-confidence-ladder.md` entry 20: implication is "closer to welfare loss than the adversarial review allowed," not a direct welfare-loss proof. [SOURCE: memo]
   396	
   397	### Fixes Made
   398	
   399	1. Replaced "Rent exposure IS welfare loss" with "Rent exposure is closer to welfare loss in inelastic destination markets."
   400	2. Kept zoning reform as a plausible lever, but attached the causal caveat that immigrant-specific rent causation still needs panel/IV identification.
   401	
   402	### Current Conclusion
   403	
   404	The housing evidence defeats the blanket "rent exposure is not welfare loss" dismissal, but only conditionally: in inelastic destination markets, rent exposure is a stronger renter-incidence warning, not a completed aggregate welfare proof. [INFERENCE]
   405	
   406	---
   407	
   408	## 2026-06-16 — Saiz rent memo removes causal language from cross-section
   409	
   410	### Issue
   411	
   412	`research/immigration-causal-saiz-elasticity-rent.md` labeled itself "Cross-sectional descriptive," but the bottom line and implication bullets still used causal phrases: housing supply "cannot respond," rent appreciation has "nowhere to go," marginal newcomers "drive up cost burden," and the adversarial caveat was "partially defeated." Those phrases overstate what the Saiz x ACS cross-section identifies. [DATA]
   413	
   414	### Evidence Checked
   415	
   416	- The memo's own status line says the instrumental-variable extension is the next step. [SOURCE: memo]
   417	- The limitations section says the causal reading "immigrant inflows raise rent more in inelastic markets" needs panel variation and an instrument for immigrant share. [SOURCE: memo]
   418	- The numeric results support a descriptive pattern: low-elasticity MSAs have higher foreign-born share and higher rent, but the cross-section does not separate immigrant inflow from amenities, wages, native demand, or other destination selection. [INFERENCE]
   419	
   420	### Fixes Made
   421	
   422	1. Replaced "cannot respond" / "nowhere to go" / "fixed stock" language with relatively inelastic supply and renter-incidence risk.
   423	2. Added the explicit panel/IV caveat to the implication bullet.
   424	3. Replaced "partially defeated" with "narrowed" for the adversarial rent-exposure caveat.
   425	
   426	### Current Conclusion
   427	
   428	The Saiz merge strengthens an elasticity-conditional housing-burden warning. It does not by itself prove immigrant-specific rent causation or aggregate welfare loss. [INFERENCE]
   429	
   430	---
   431	
   432	## 2026-06-16 — Causal synthesis mirrors Saiz rent caveat
   433	
   434	### Issue
   435	
   436	`research/immigration-causal-synthesis-2026-04-18.md` preserved the same housing overstatement after the Saiz source memo was narrowed. It said supply "can't respond," "rent appreciation is welfare loss," the rent burden question was "Partially resolved ... yes," and the proposed Saiz x PUMA rerun would produce a "rent welfare estimate." Those claims exceed the current cross-sectional evidence. [DATA]
   437	
   438	### Evidence Checked
   439	
   440	- `research/immigration-causal-saiz-elasticity-rent.md`: descriptive correlation is high-confidence; immigrant-specific rent causation and welfare incidence need panel/IV identification and tenure accounting. [SOURCE: memo]
   441	- `research/immigration-causal-synthesis-2026-04-18.md`: the same memo already lists "Causal IV for housing" as unsettled, so its verdict language needed to match its own limitation section. [SOURCE: memo]
   442	
   443	### Fixes Made
   444	
   445	1. Replaced "closer to welfare loss because supply can't respond" with "stronger renter-incidence warning because supply response is weaker."
   446	2. Replaced "rent appreciation is welfare loss" with a panel/IV caveat.
   447	3. Replaced "partially resolved ... yes" with "narrowed, not resolved."
   448	4. Relabeled the proposed Saiz x PUMA rerun as an origin-conditional renter-incidence screen, not a final welfare estimate.
   449	
   450	### Current Conclusion
   451	
   452	The April 18 causal synthesis now treats housing as an elasticity-conditional local-burden warning, not as a completed rent-welfare causal estimate. [INFERENCE]
   453	
   454	---
   455	
   456	## 2026-06-16 — Lifetime brainstorms stop scalarizing Saiz rent screen
   457	
   458	### Issue
   459	
   460	Two tracked lifetime-planning memos carried the same Saiz overstatement into future work:
   461	
   462	1. `research/immigration-lifetime-dataset-brainstorm-2026-06-15.md` said the Saiz layer shows "rent burden is welfare loss, not price discovery."
   463	2. `research/immigration-lifetime-country-approx-brainstorm-2026-06-15.md` framed the Saiz country slice as "welfare loss $" and "local welfare loss."
   464	
   465	That would make later agents build a scalar welfare-loss line from a screen that is only descriptive until tenure mix and panel/IV identification are added. [DATA]
   466	
   467	### Evidence Checked
   468	
   469	- `research/immigration-causal-saiz-elasticity-rent.md`: the current evidence is a high-confidence descriptive correlation and only a moderate welfare-interpretation update. [SOURCE: memo]
   470	- `research/immigration-causal-synthesis-2026-04-18.md`: the corrected downstream synthesis now treats the Saiz x PUMA rerun as an origin-conditional renter-incidence screen, not a final welfare estimate. [SOURCE: memo]
   471	
   472	### Fixes Made
   473	
   474	1. Replaced "rent burden is welfare loss" with "elasticity-conditional renter-incidence screen."
   475	2. Replaced "welfare loss $" / "local welfare loss" future-work language with renter-incidence risk / local-incidence offset language.
   476	
   477	### Current Conclusion
   478	
   479	Future lifetime-country work should use Saiz as a targeting and incidence screen until it has the missing causal and tenure-incidence pieces needed for a welfare scalar. [INFERENCE]
   480	
   481	---
   482	
   483	## 2026-06-16 — E-Verify wage null no longer becomes inflow null
   484	
   485	### Issue
   486	
   487	Two wage memos still converted a marginal-enforcement result into a broader immigration-level conclusion:
   488	
   489	1. `research/immigration-causal-everify-card-vs-borjas.md` said native low-skill workers are "not measurably hurt by current low-skill immigration levels."
   490	2. `research/immigration-causal-synthesis-2026-04-18.md` said native low-skill workers "do not lose from immigrant inflows" and the labor-market component is "approximately zero for natives."
   491	
   492	The E-Verify design measures wage response to observed state mandate variation, not the full wage effect of current low-skill immigration levels, surge regimes, cash-economy substitution, employment composition, hours, or mass shocks. [DATA]
   493	
   494	### Evidence Checked
   495	
   496	- `research/immigration-causal-everify-card-vs-borjas.md`: treatment is state E-Verify mandate timing; caveats include external validity, partial compliance, cash-economy substitution, and non-wage channels. [SOURCE: memo]
   497	- `research/immigration-causal-surge-2021-2024.md`: surge-period wage estimates remain unmeasured and outside pre-2021 marginal-policy variation. [SOURCE: memo]
   498	- `research/immigration-confidence-ladder.md` entry 29: Card-side finding is bounded to marginal-policy variation; surge is outside that variation. [SOURCE: memo]
   499	
   500	### Fixes Made
   501	
   502	1. Replaced "not measurably hurt by current low-skill immigration levels" with a narrower claim: no measurable native wage gains from E-Verify-style restrictions, rejecting large Borjas-style gains from marginal removal.
   503	2. Replaced "do not lose from immigrant inflows" and "labor-market component ... approximately zero" with "observed marginal-enforcement wage component is small/null."
   504	3. Reopened non-wage labor-market channels and surge/mass-shock regimes explicitly.
   505	
   506	### Current Conclusion
   507	
   508	The wage evidence is strong against large native wage gains from observed marginal enforcement contractions. It is not a direct proof that current low-skill immigration levels or surge inflows have zero native labor-market effect. [INFERENCE]
   509	
   510	---
   511	
   512	## 2026-06-16 — Surge capacity and deportation validation claims bounded
   513	
   514	### Issue
   515	
   516	`research/immigration-causal-surge-2021-2024.md` overstated two validation claims:
   517	
   518	1. Receiver-city gross outlays and shelter stress were described as "system-collapse evidence" and as empirical validation of a national housing/construction capacity calibration.
   519	2. The mass-deportation simulation was labeled "partially validated" using qualitative early indicators, while the same paragraph said quantitative replication awaited post-2025 data.
   520	
   521	The available local evidence supports gross receiver-node load and visible shelter/budget stress. It does not estimate net fiscal burden, validate a national 10M+/year arrival threshold, or quantitatively validate the mass-deportation output simulation. [DATA]
   522	
   523	### Evidence Checked
   524	
   525	- `research/immigration-causal-surge-2021-2024.md`: receiver-city figures are city/state cost trajectories and shelter caps, not a netted burden model. [SOURCE: memo]
   526	- `research/immigration-confidence-ladder.md` entry 33: receiver-city figures are gross outlays; federal reimbursements and counterfactual baseline growth are not netted out. [SOURCE: memo]
   527	- `research/immigration-confidence-ladder.md` entry 32: mass-deportation output shock is a calibration with frozen replacement hiring, wage response, and capital reallocation. [SOURCE: memo]
   528	
   529	### Fixes Made
   530	
   531	1. Reframed receiver-city evidence as gross-load and shelter-stress evidence, not "system collapse" or national capacity validation.
   532	2. Replaced "empirically validated" with "directionally consistent" and named the missing national capacity function.
   533	3. Replaced "Mass-deportation simulation — partially validated" with "not yet quantitatively validated."
   534	4. Marked confidence-ladder entry 27 as scope-qualified by entry 33's gross-vs-net caveat.
   535	
   536	### Current Conclusion
   537	
   538	The surge evidence shows concentrated receiver-node stress. It should not be cited as a net fiscal-burden estimate, a national capacity threshold validation, or a quantitative validation of the mass-deportation output model. [INFERENCE]
   539	
   540	---
   541	
   542	## 2026-06-16 — Receiver-election wording made correlational
   543	
   544	### Issue
   545	
   546	`research/immigration-causal-surge-2021-2024.md` already warned that the receiver-city election result is a correlational upper-bound, but its interpretation still said the 2024 election shift was "partially related to surge exposure" and that receiver-city GOP shift reflected "natives' response." That wording overstates identification and erases naturalized-citizen / electorate-composition channels. [DATA]
   547	
   548	### Evidence Checked
   549	
   550	- `research/immigration-causal-surge-2021-2024.md`: the reading rule says the raw receiver-city gap is descriptive only and the `+2.4pp` coefficient is a correlational upper-bound. [SOURCE: memo]
   551	- The same memo lists unresolved confounders: Hispanic realignment, inflation, pre-existing RGV trend, and noncitizen voting ineligibility. [SOURCE: memo]
   552	- `research/immigration-confidence-ladder.md` entries 31 and 36: use the controlled `+2.4pp` as an upper-bound; causal interpretation needs more work. [SOURCE: memo]
   553	
   554	### Fixes Made
   555	
   556	1. Replaced "partially related to surge exposure" with "correlated with receiver-city / border-surge exposure."
   557	2. Replaced "natives' response" with "citizen electorate's response or composition."
   558	3. Added unresolved compositional confounding to the CURRENT-inflow interpretation.
   559	
   560	### Current Conclusion
   561	
   562	The receiver-city election result remains a medium-strength association that survived the named Hispanic-share kill-test. It is not clean causal evidence of voter backlash from the surge. [INFERENCE]
   563	
   564	---
   565	
   566	## 2026-06-16 — Embedded surge ladder gross-load wording aligned
   567	
   568	### Issue
   569	
   570	`research/immigration-causal-surge-2021-2024.md` had already reframed receiver-city costs as gross-load and shelter-stress evidence, but its embedded confidence-ladder entry 27 still ended with "System-collapse claim has empirical bite." That sentence recreated the same overclaim inside a later section of the same memo. [DATA]
   571	
   572	### Why it was wrong
   573	
   574	The administrative cost rows support visible receiver-load stress and concentrated gross outlays. They do not by themselves identify net fiscal burden after reimbursements and counterfactual baseline costs, and they do not validate a national system-collapse threshold. [INFERENCE]
   575	
   576	### Fix
   577	
   578	Replaced the embedded ladder sentence with the narrower claim that receiver-load stress has empirical bite while the figures remain gross outlays, not net fiscal-burden or national system-collapse proof. [SOURCE: memo]
   579	
   580	### Updated conclusion
   581	
   582	The surge memo is now internally consistent on receiver-cost scope: receiver-city costs are strong gross-load evidence, not a completed net-burden or national-collapse estimate. [INFERENCE]
   583	
   584	---
   585	
   586	## 2026-06-16 — Caplan audit political-incidence mechanism bounded
   587	
   588	### Issue
   589	
   590	`research/immigration-bryan-caplan-claims-audit-2026-04-21.md` still treated "backlash" as a settled mechanism in several verdict and DAG lines. Later receiver-city work supports a political-response association, but explicitly leaves mechanism unresolved: persuasion, turnout, sorting, Hispanic realignment, and busing-target endogeneity are not cleanly separated. [DATA]
   591	
   592	### Why it was wrong
   593	
   594	Caplan's narrow median-voter argument still fails as a full political-incidence answer because immigrant voting is not the only channel. But the repo should not convert a bounded receiver-city correlation into a completed backlash mechanism. [INFERENCE]
   595	
   596	### Fix
   597	
   598	Replaced the stale backlash/decisive/impossible phrasing with bounded political-response language. The Caplan audit now says local overload, legitimacy effects, and possible citizen response remain live, while mechanism identification remains unresolved. [SOURCE: memo]
   599	
   600	### Updated conclusion
   601	
   602	The Caplan critique survives, but on a narrower basis: his political-externality answer is incomplete because local political-response channels cannot be assumed zero, not because the repo has cleanly proven a backlash mechanism. [INFERENCE]
   603	
   604	---
   605	
   606	## 2026-06-16 — Capacity-frontier political outcome label bounded
   607	
   608	### Issue
   609	
   610	`research/immigration-capacity-frontier-2026-04-21.md` used "backlash" in its bottom line, claims table, and synthesis even though its own open-questions section says county returns do not identify whether the effect is turnout, persuasion, composition change, or precinct-level backlash. [DATA]
   611	
   612	### Why it was wrong
   613	
   614	The data rows support a county-level political-response association. They do not identify the voter-level mechanism. Calling the outcome "backlash" hard-codes one interpretation that the memo itself lists as unresolved. [INFERENCE]
   615	
   616	### Fix
   617	
   618	Replaced the active backlash labels with political-response language, changed "settled enough" to "stable enough," and updated the immigration index descriptions for the Caplan, threshold, and county-outcome memos. [SOURCE: memo]
   619	
   620	### Updated conclusion
   621	
   622	The capacity-frontier memo now treats GOP margin movement as a political-response metric. Backlash remains one possible mechanism to test, not the name of the measured outcome. [INFERENCE]
   623	
   624	---
   625	
   626	## 2026-06-16 — Mass-deportation output headline separated from sensitivity
   627	
   628	### Issue
   629	
   630	`research/immigration-confidence-ladder.md` entry 32 already said the mass-deportation output shock should lead with the first-order figure and keep the Type-II multiplier endpoint only as a labeled sensitivity. But entry 24 still headlined the combined `$1.5-2.3T` / `5-8% GDP` range, and `research/immigration-causal-surge-2021-2024.md` repeated the same `~5-8% GDP` presentation. [DATA]
   631	
   632	### Why it was wrong
   633	
   634	The Type-II endpoint stacks a modeled multiplier on top of a calibration that freezes replacement hiring, wage response, and capital reallocation. It is useful as a sensitivity, but headlining it as a range launders a modeled amplifier into the main estimate. [INFERENCE]
   635	
   636	### Fix
   637	
   638	Changed the ladder entry and surge memo to lead with the first-order `~$1.45T` / `~5% GDP` figure and label the `~$2.32T` / `~8%` endpoint as Type-II sensitivity only. [SOURCE: memo]
   639	
   640	### Updated conclusion
   641	
   642	The mass-deportation output-shock claim remains medium-confidence calibration evidence, but the headline is now the first-order estimate; multiplier amplification is not presented as coequal estimate truth. [INFERENCE]
   643	
   644	---
   645	
   646	## 2026-06-16 — ICE docket denominator error removed from crime memo
   647	
   648	### Issue
   649	
   650	`research/immigration-crime-rates-unauthorized-vs-native-born.md` correctly warned that the ICE ERO criminal-history counts are docket stock figures rather than rates, but then said dividing by the `~11M` unauthorized immigrant population and an accumulation period yields rates far below native-born equivalents. It also described the source as a non-detained-docket table when the ICE letter reports the **national docket** split into detained and non-detained columns. The source table is for **noncitizens on ICE's national docket**, not an unauthorized-only numerator. [SOURCE: ICE ERO letter]
   651	
   652	### Why it was wrong
   653	
   654	That denominator move silently mixes universes: all noncitizens on an ICE docket in the numerator, unauthorized immigrant stock in the denominator, and an unspecified accumulation period for person-time. It turns a valid stock-vs-rate warning into a new rate-base error. [INFERENCE]
   655	
   656	### Fix
   657	
   658	Replaced the naive division claim with a refusal to compute a native comparison from those counts, and relabeled the table as national-docket rather than non-detained-docket. The memo now says the ICE counts do not by themselves provide a per-capita native comparison or overturn rate-based studies. [SOURCE: memo]
   659	
   660	### Updated conclusion
   661	
   662	The crime memo's bottom-line directional claim is unchanged, but its ICE-docket section no longer uses an invalid unauthorized-stock denominator. [INFERENCE]
   663	
   664	---
   665	
   666	## 2026-06-16 — Paradigm synthesis calibration headlines bounded
   667	
   668	### Issue
   669	
   670	`research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md` still carried two stale calibration presentations: mass deportation was headlined as a `$1.5-2.3T` / `5-8% GDP` range, and the open-borders calibration row described housing capacity as binding above `~10M/year` arrivals without enough warning that this was a modeled threshold, not a validated national capacity function. [DATA]
   671	
   672	### Why it was wrong
   673	
   674	Later fixes established that the deportation multiplier endpoint is a Type-II sensitivity, not a coequal estimate, and that surge-era receiver stress is only directionally consistent with the national capacity calibration. The April synthesis had not inherited those scope bounds. [INFERENCE]
   675	
   676	### Fix
   677	
   678	Changed the mass-deportation rows and ladder excerpt to lead with the first-order `~$1.45T` / `~5% GDP` output shock, labeling `~$2.32T` / `~8%` as Type-II sensitivity. Reframed the `~10M/year` housing/construction statement as a calibration warning for very-large-arrival scenarios rather than a validated national threshold. [SOURCE: memo]
   679	
   680	### Updated conclusion
   681	
   682	The paradigm synthesis still flags large-output and capacity risks, but now treats both as calibration outputs with sensitivity labels rather than measured all-scenario thresholds. [INFERENCE]
   683	
   684	---
   685	
   686	## 2026-06-16 — Capacity-frontier threshold language made descriptive
   687	
   688	### Issue
   689	
   690	`research/immigration-capacity-frontier-2026-04-21.md` still described the threshold as "real," called `flow / local build capacity` the "right object," and closed by saying "`flow + capacity` is where the new causal traction is coming from." The memo's own design is a county-panel/model-comparison surface, not a clean causal identification design. [DATA]
   691	
   692	### Why it was wrong
   693	
   694	The threshold grid and model comparisons show recurring descriptive patterns, but they do not by themselves separate inflow effects from housing response, destination selection, baseline affordability, policy targeting, or omitted local shocks. Calling that "causal traction" overstates the design. [INFERENCE]
   695	
   696	### Fix
   697	
   698	Replaced "real threshold" and "causal traction" phrasing with "recurring/observed/descriptive threshold pattern" and named the need for stronger counterfactual design before causal interpretation. [SOURCE: memo]
   699	
   700	### Updated conclusion
   701	
   702	The capacity-frontier memo still says load/capacity is the better county stress surface, but it no longer treats the threshold-grid pattern as identified causal truth. [INFERENCE]
   703	
   704	---
   705	
   706	## 2026-06-16 — Crime conclusion estimand made explicit
   707	
   708	### Issue
   709	
   710	`research/immigration-crime-rates-unauthorized-vs-native-born.md` correctly listed reporting, detection, deportation, and denominator problems, but its bottom line still said unauthorized immigrants "commit crimes" at lower rates. The Caplan audit inherited the same blur when summarizing the crime objection. [DATA]
   711	
   712	### Why it was wrong
   713	
   714	The strongest evidence is about observed arrest, conviction, incarceration, and institutionalization outcomes. Those are not identical to true offending when underreporting, police contact, deportation censoring, and denominator uncertainty are active mechanisms. [INFERENCE]
   715	
   716	### Fix
   717	
   718	Reframed the crime memo's question, bottom line, confidence statement, international caveat, and uncertainty section around observed criminal-justice rates. Updated the Caplan audit to say the claim mostly survives for observed U.S. first-generation / unauthorized justice-system rates, while true offending is less directly identified. [SOURCE: memo]
   719	
   720	### Updated conclusion
   721	
   722	The directional crime finding survives, but its estimand is now explicit: lower observed justice-system rates in current U.S. evidence, not directly measured lower true offending in every subgroup or context. [INFERENCE]
   723	
   724	---
   725	
   726	## 2026-06-16 — Unified fiscal synthesis bounded from universal survival claim
   727	
   728	### Issue
   729	
   730	`research/immigration-lifetime-unified-theory-2026-06-15.md` said its explanatory story "survives all datasets," that "data cannot kill" the coherent mechanism, and that "all channels are real in their layer." That overstated what a heterogeneous warehouse of annual proxies, lifetime NPV benchmarks, local descriptive burdens, receiver-city ledgers, and theory papers can identify. [DATA]
   731	
   732	### Why it was wrong
   733	
   734	A layered tensor is the right anti-scalar frame, but it is still falsifiable. New data can kill channel magnitudes, signs for particular cells, annual-to-lifetime bridges, destination-specific incidence, or equilibrium assumptions. The robust correction is narrower: one dataset layer should not be exported as the total immigration conclusion without matching the ledger, cell, and cohort. [INFERENCE]
   735	
   736	### Fix
   737	
   738	Replaced the universal "survives all datasets" and "data cannot kill" language with a current-warehouse-compatible working synthesis. Reframed the narrative spine as still falsifiable and changed "all channels are real" to evidence-in-layer language with varying identification strength. Added a memo revision row documenting the confidence bound. [SOURCE: memo]
   739	
   740	### Updated conclusion
   741	
   742	The fiscal-tensor synthesis still stands as the best current organizing frame, but it is no longer presented as immune to future evidence. Its strongest conclusion is anti-scalar: do not collapse layer, cell, and cohort into one immigration fiscal number. [INFERENCE]
   743	
   744	---
   745	
   746	## 2026-06-16 — Native-low-skill political-economy inference narrowed
   747	
   748	### Issue
   749	
   750	`research/immigration-causal-synthesis-2026-04-18.md` said the policy push from native low-skill voters could not easily be justified by their wage data, but "can be justified" by their school-finance and rent exposure. That moved too quickly from incidence evidence to voter motivation and policy justification. [DATA]
   751	
   752	### Why it was wrong
   753	
   754	The E-Verify wage evidence can weaken a wage-only restriction story within observed marginal-enforcement variation. It does not identify why voters support restriction, and the Saiz/school channels are exposure mechanisms, not proofs that a particular voter group is correctly optimizing over those burdens. Rent incidence depends on renter/owner status; school incidence depends on local fiscal institutions and child composition; political support also includes values and credibility beliefs. [INFERENCE]
   755	
   756	### Fix
   757	
   758	Replaced the "can be justified" line with a narrower statement: wage data alone are weak support for the native-low-skill wage story, while school-finance and renter exposure remain plausible incidence channels. Added a revision note to the synthesis memo. [SOURCE: memo]
   759	
   760	### Updated conclusion
   761	
   762	The political-economy conclusion survives only as a channel map: wage evidence is weak for the observed range, and school/rent channels remain live. The memo no longer claims those channels identify voter motivation or justify the policy push. [INFERENCE]
   763	
   764	---
   765	
   766	## 2026-06-16 — Crime search-log absence claim bounded
   767	
   768	### Issue
   769	
   770	`research/immigration-crime-rates-unauthorized-vs-native-born.md` logged the Exa verification pass for higher-rate studies as "No peer-reviewed support found." In a search log, that reads like a literature-wide proof of absence rather than the result of a particular pass. [DATA]
   771	
   772	### Why it was wrong
   773	
   774	Search tools can support "not found in this query/pass" much more safely than "does not exist." The memo already has a strong bottom line from named studies and named critiques; it does not need an unbounded absence claim in the provenance table. [INFERENCE]
   775	
   776	### Fix
   777	
   778	Changed the row to "No peer-reviewed higher-rate study found in this pass; Lott Arizona remained the prominent non-peer-reviewed outlier" and added a memo revision note. [SOURCE: memo]
   779	
   780	### Updated conclusion
   781	
   782	The crime memo's substantive conclusion is unchanged. The provenance is now narrower: the pass failed to find a peer-reviewed higher-rate study; it does not claim an exhaustive proof that none exists. [INFERENCE]
   783	
   784	---
   785	
   786	## 2026-06-16 — Capacity-frontier claims table scoped to model output
   787	
   788	### Issue
   789	
   790	`research/immigration-capacity-frontier-2026-04-21.md` had already been narrowed away from causal-threshold language, but its claims table still listed several county model patterns as `HIGH | VERIFIED` without explaining that those labels were about artifact-backed model output, not causal identification. [DATA]
   791	
   792	### Why it was wrong
   793	
   794	For a reader scanning the table, `HIGH | VERIFIED` can look like a validated causal effect. The listed artifacts verify correlations, model rankings, interaction-grid patterns, and decile summaries; they do not by themselves identify immigration-caused wage, employment, sorting, or political effects. [INFERENCE]
   795	
   796	### Fix
   797	
   798	Added a scope note below the claims table: `HIGH` and `VERIFIED` mean the reported model-output pattern is file-backed and reproducible from the listed artifacts, not that the county associations are clean causal effects. Added a memo revision entry. [SOURCE: memo]
   799	
   800	### Updated conclusion
   801	
   802	The capacity-frontier evidence remains useful as a descriptive stress surface. Its table is now explicitly scoped so reproducibility of the model output is not confused with causal validity. [INFERENCE]
   803	
   804	---
   805	
   806	## 2026-06-16 — E-Verify Card-vs-Borjas source memo bounded to design margin
   807	
   808	### Issue
   809	
   810	`research/immigration-causal-everify-card-vs-borjas.md` correctly narrowed several later synthesis claims, but the source memo still said "the data side with Card, not Borjas" and described the result as "a Card-style world." It also said Friedman's Card-style premise was "confirmed" and Camarota's native-wage argument "doesn't pass this test" without enough scope language. [DATA]
   811	
   812	### Why it was wrong
   813	
   814	The E-Verify TWFE design can reject large Borjas-style native wage gains for the observed enforcement margin. It cannot settle all low-skill immigration wage effects, surge regimes, mass deportation, open borders, or non-wage channels. The commentator-update language needed to inherit that same external-validity bound. [INFERENCE]
   815	
   816	### Fix
   817	
   818	Replaced the global "data side with Card" phrasing with "in this E-Verify design, the wage results are closer to the Card-style null than to large Borjas-style native wage gains." Reframed "Card-style world" as "for this enforcement margin" and bounded the Friedman/Camarota update lines to the wage-channel test. Added a memo revision note. [SOURCE: memo]
   819	
   820	### Updated conclusion
   821	
   822	The E-Verify result remains strong against large native wage gains from marginal enforcement. It no longer reads as a global settlement of Card vs Borjas, open borders, or all native labor-market channels. [INFERENCE]
   823	
   824	---
   825	
   826	## 2026-06-16 — Paradigm synthesis wage-rejection labels scoped
   827	
   828	### Issue
   829	
   830	`research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md` still compressed the E-Verify and sanctuary wage results into short-form labels like "STRONG REJECTION of Borjas" and "STRONG REJECTION of enforcement-channel wage effects." That was sharper than the source designs justified. [DATA]
   831	
   832	### Why it was wrong
   833	
   834	The source designs are strong against large native wage gains under observed E-Verify/sanctuary-style policy variation. They do not reject every Borjas-style claim, every enforcement-channel wage effect, or shock regimes outside the tested policy margins. The short-form table needed to carry the same external-validity bound as the body text. [INFERENCE]
   835	
   836	### Fix
   837	
   838	Changed the findings table and embedded ladder snippet to say the evidence is strong against large Borjas-style wage gains in the tested enforcement margin and shows a strong null result for the tested policy variations. Added a memo revision note. [SOURCE: memo]
   839	
   840	### Updated conclusion
   841	
   842	The paradigm synthesis still supports a Card-side null for observed marginal wage variation, but its short labels no longer imply global rejection of Borjas or all enforcement-channel wage effects. [INFERENCE]
   843	
   844	---
   845	
   846	## 2026-06-16 — Saiz zoning-channel inference made descriptive
   847	
   848	### Issue
   849	
   850	`research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md` and `research/immigration-confidence-ladder.md` described the Saiz decomposition as showing that the inelastic-MSA immigrant concentration was "driven by" regulatory constraint and that zoning reform was a viable policy lever. The source regression only showed WRLURI was a stronger correlate of foreign-born share than topographic unavailability. [DATA]
   851	
   852	### Why it was wrong
   853	
   854	A cross-sectional regression of foreign-born share on WRLURI, topographic unavailability, and log population does not identify the causal direction. WRLURI may proxy high-demand metro governance, amenities, historical settlement, political economy, or endogenous restrictions. It can make zoning reform a plausible hypothesis, but not a proven causal substitute for immigration restriction or a verified way to reduce immigrant renter burden. [INFERENCE]
   855	
   856	### Fix
   857	
   858	Replaced "regulatory channel dominates" / "driven by regulatory constraint" language with "WRLURI is the stronger correlate" and "strong descriptive regression, not causal channel proof." Reframed zoning reform as a plausible policy hypothesis rather than an identified causal lever. Added append-only confidence-ladder entry 38 as a scope correction to entry 20. [SOURCE: memo]
   859	
   860	### Updated conclusion
   861	
   862	The Saiz result still strengthens the housing-incidence warning in inelastic destination markets, but the regulatory decomposition is descriptive. It should motivate a panel/IV zoning test, not be used as proof that zoning caused the concentration or that zoning reform resolves the rent-burden channel. [INFERENCE]
   863	
   864	---
   865	
   866	## 2026-06-16 — Federal distribution memo aligned to native-white microsim anchor
   867	
   868	### Issue
   869	
   870	`research/immigration-federal-distribution-findings-2026-06-15.md` still reported an older NH-white federal proxy of `~$3,600–4,000/adult` and a `~2.3–3.0×` per-adult white/Mexico ratio. Later built tensor artifacts report `NH white US-born ~$2,746/adult`, `Mexico-origin ~$1,519/adult`, and an `~1.8×` ratio from `acs_nh_white_federal_microsim_2023`. [DATA]
   871	
   872	### Why it was wrong
   873	
   874	The older row came from an ACS wage-imputation sensitivity path. Once the native-white microsim existed, keeping the old range as the headline silently forked the current conclusion and overstated the narrow federal-cash-proxy gap. The aggregate total also changed: `~$253B` vs `~$12.9B` is about `19.6×`, not `25×`, with roughly `11×` from population count alone. [DATA]
   875	
   876	### Fix
   877	
   878	Updated the distribution memo's per-adult table, aggregate table, decomposition, verdict, limitation row, and revision log to use the current built native-white microsim anchor. Marked the older `~2.8–3.1×` wage-imputation sensitivity as superseded for headline use. [SOURCE: memo]
   879	
   880	### Updated conclusion
   881	
   882	The distribution conclusion is narrower: on the current built narrow federal cash proxy, NH white US-born adults are about `1.8×` Mexico-origin adults, mostly because of education composition. This remains layer-specific and does not settle full federal liability, lifetime NPV, or all-government fiscal incidence. [INFERENCE]
   883	
   884	---
   885	
   886	## 2026-06-16 — Lifetime-country brainstorm trigger aligned to corrected proxy ratio
   887	
   888	### Issue
   889	
   890	`research/immigration-lifetime-country-approx-brainstorm-2026-06-15.md` still opened from the stale premise that distribution findings showed a `~2–3×` per-capita federal proxy gap between whites and Mexico-born adults. That was the older wage-imputation headline superseded by the built native-white microsim. [DATA]
   891	
   892	### Why it was wrong
   893	
   894	Even though the brainstorm's main tensor logic remained valid, the trigger line would send future readers back into the older ratio. The correct current anchor is `~1.8×` per adult on the narrow federal proxy, with the same larger point intact: lifetime NPV and country-level net still require stacked layer accounting. [INFERENCE]
   895	
   896	### Fix
   897	
   898	Changed the trigger to the current `~1.8×` NH-white-US-born/Mexico-origin federal proxy ratio and added a revision row pointing back to this audit. [SOURCE: memo]
   899	
   900	### Updated conclusion
   901	
   902	The brainstorm still motivates a lifetime/country tensor, but no longer inherits the stale `~2–3×` federal-proxy premise. [INFERENCE]
   903	
   904	---
   905	
   906	## 2026-06-16 — School crude-net table made symmetric on child attribution
   907	
   908	### Issue
   909	
   910	`research/immigration-school-burden-per-adult-2026-06-15.md` warned that immigrant-headed household school costs should not be read without descendant future taxes, but the headline table also showed NH-white crude rows around `−$3,277/adult` without an equally explicit warning that those native rows are not a native fiscal-loss finding. [DATA]
   911	
   912	### Why it was wrong
   913	
   914	The `net_crude_federal_minus_school` view assigns current average K–12 costs to current adults and omits descendant future taxes, lifetime accounting, marginal pupil costs, Medicaid, non-school local services, and full federal taxes. That limitation is symmetric. Reading the NH-white negative row as "native whites are fiscally negative" would be the same layer-laundering error as reading the Mexico positive row as all-government fiscal positivity. [INFERENCE]
   915	
   916	### Fix
   917	
   918	Added a table-scope warning below the headline table and expanded the child-attribution caveat to say the native rows have the same accounting limitation. Added a memo revision row. [SOURCE: memo]
   919	
   920	### Updated conclusion
   921	
   922	The school layer still shows static visibility math: Mexico-origin is `+$748/adult` and NH-white US-born is `−$3,277/adult` under this crude average-cost assignment. Neither row is a welfare verdict or lifetime fiscal sign. [INFERENCE]
   923	
   924	---
   925	
   926	## 2026-06-16 — FAIR ledger no longer labeled mathematical upper bound
   927	
   928	### Issue
   929	
   930	`research/immigration-restrictionist-arguments-steelman-2026-06-15.md` described FAIR's `$150.7B` unauthorized-immigration cost estimate as an "upper-bound political ledger." That language was too generous statistically: FAIR is advocacy-sourced and uses contested attribution choices, including citizen-child cost assignment and stock/method differences versus Pew and ITEP. [DATA]
   931	
   932	### Why it was wrong
   933	
   934	"Upper bound" implies the number bounds the true cost from above. FAIR's construction is better treated as an advocacy high-cost ledger: it may include broad cost categories omitted by NAS individual NPV, but that does not make it a validated upper limit. Some choices can overstate marginal public cost, while omitted or differently treated categories could move in either direction. [INFERENCE]
   935	
   936	### Fix
   937	
   938	Renamed the chain from "Annual full budget" to "Annual advocacy ledger," replaced "upper-bound political ledger" with "advocacy high-cost ledger," and changed the rhetoric table's "Upper bound" row accordingly. Added a memo revision note. [SOURCE: memo]
   939	
   940	### Updated conclusion
   941	
   942	The restrictionist steel-man still preserves the full-budget ledger as a real argument family, but FAIR is now source-graded correctly: useful as a high-cost advocacy construction, not as empirical fact or a mathematical upper bound. [INFERENCE]
   943	
   944	---
   945	
   946	## 2026-06-16 — E-Verify proposed ladder label aligned to margin-specific verdict
   947	
   948	### Issue
   949	
   950	`research/immigration-causal-everify-card-vs-borjas.md` had already bounded its headline Card-vs-Borjas conclusion, but its "What this updates" section still proposed adding a confidence-ladder entry labeled `STRONG REJECTION`. That leftover label conflicted with the source memo's own external-validity caveat. [DATA]
   951	
   952	### Why it was wrong
   953	
   954	The E-Verify design is strong against large Borjas-style native wage gains in the observed E-Verify margin. It is not a global rejection of all Borjas-style substitution claims, all enforcement-channel wage effects, or surge/mass-shock regimes. A suggested ladder entry should not be broader than the result it summarizes. [INFERENCE]
   955	
   956	### Fix
   957	
   958	Changed the proposed ladder label to "strong against large Borjas-style gains in this E-Verify margin" and added a source-memo revision note. The append-only confidence ladder already has entry 29 bounding the older wage entries to marginal policy variation, so no ladder rewrite was needed. [SOURCE: memo]
   959	
   960	### Updated conclusion
   961	
   962	The source memo's short-form update now matches the main evidence statement: strong against high-end Borjas magnitudes for this policy margin, not a universal rejection. [INFERENCE]
   963	
   964	---
   965	
   966	## 2026-06-16 — Causal synthesis inherited stale global E-Verify rejection label
   967	
   968	### Issue
   969	
   970	`research/immigration-causal-synthesis-2026-04-18.md` still embedded a suggested confidence-ladder addition rating the E-Verify wage result as `STRONG REJECTION`. That block is reusable guidance, so it would keep propagating the pre-boundary label even after the source E-Verify memo was narrowed. [DATA]
   971	
   972	### Why it was wrong
   973	
   974	The synthesis itself already says surge and mass-shock regimes remain open. The E-Verify design excludes large Borjas-style native wage gains for observed mandate variation; it does not reject every labor-substitution claim or every counterfactual enforcement shock. A ladder suggestion cannot be broader than the identification margin that produced it. [INFERENCE]
   975	
   976	### Fix
   977	
   978	Replaced the embedded ladder rating with "strong against large Borjas-style gains in the E-Verify margin," changed the reason to name the observed mandate design, and narrowed the summary table row from "Borjas wage prediction rejected" to "large Borjas-style native wage gains" in that policy variation. Added a synthesis revision row. [SOURCE: memo]
   979	
   980	### Updated conclusion
   981	
   982	The April causal synthesis is now aligned with the later bounded source memo: strong Card-side evidence for observed E-Verify policy variation, not a global E-Verify-based rejection of Borjas-style claims. [INFERENCE]
   983	
   984	---
   985	
   986	## 2026-06-16 — Restrictionist steel-man overread receiver stress as collapse
   987	
   988	### Issue
   989	
   990	`research/immigration-restrictionist-arguments-steelman-2026-06-15.md` still used crisis/collapse/catastrophe language around the receiver-city layer: surge-era immigration "created visible local fiscal/social crisis," the NAS benchmark omitted a "system collapse" story, the admin-budget gap "validates" the +$46k critique, and the strongest fair claim described shelter/school effects as "locally catastrophic." [DATA]
   991	
   992	### Why it was wrong
   993	
   994	The cited receiver evidence supports gross shelter/budget load and visible receiver-city stress. Gould's sheltered-homelessness result and NYC/receiver-city cost rows are material, but they do not by themselves estimate net fiscal burden after reimbursements and baseline costs, identify national system collapse, or allocate administrative costs to the Mexico-origin NPV cell. The steel-man should preserve the layer without overstating what it identifies. [INFERENCE]
   995	
   996	### Fix
   997	
   998	Changed the policy implication to receiver-city shelter/budget stress; replaced "system collapse" with receiver-capacity stress; changed "validates" to support for an omitted admin-allocation layer; changed "locally catastrophic" to locally severe in shelter/school-capacity ledgers; and bounded the disconfirmation table to gross episodic receiver-stress evidence rather than net/collapse proof. Added a memo revision row. [SOURCE: memo]
   999	
  1000	### Updated conclusion
  1001	
  1002	The restrictionist steel-man still keeps the receiver-stress objection alive, but it no longer upgrades gross local outlays and shelter stress into a national-collapse or completed net-fiscal verdict. [INFERENCE]
  1003	
  1004	---
  1005	
  1006	## 2026-06-16 — Saiz ladder correction made visible at old entry
  1007	
  1008	### Issue
  1009	
  1010	`research/immigration-confidence-ladder.md` already had append-only entry 38 correcting entry 20's zoning-causation language, but entry 20's title still presented the old causal reading without an inline qualification. A reader scanning the original ladder section could miss the later scope correction. [DATA]
  1011	
  1012	### Why it was wrong
  1013	
  1014	The append-only rule preserves old judgments, but superseded or qualified claims need visible pointers at the old claim site when they are likely to be reused. Entry 20's title said the correlation "operates through" regulation; entry 38 says the WRLURI result is descriptive and not identified zoning causation. Without a title pointer, the old claim remained too easy to quote out of scope. [INFERENCE]
  1015	
  1016	### Fix
  1017	
  1018	Annotated entry 20's title with `QUALIFIED by entry 38` while leaving the historical reason text intact. [SOURCE: memo]
  1019	
  1020	### Updated conclusion
  1021	
  1022	The confidence ladder now keeps its append-only history while making the current Saiz scope correction visible where the older causal title appears. [INFERENCE]
  1023	
  1024	---
  1025	
  1026	## 2026-06-16 — Crime memo downgraded fetched-but-unread European row
  1027	
  1028	### Issue
  1029	
  1030	`research/immigration-crime-rates-unauthorized-vs-native-born.md` marked the European mixed-evidence row as `VERIFIED (direction), not fully analyzed`. That status is self-contradictory: the row relied on a fetched Skardhamar et al. paper that the memo explicitly says was not fully analyzed. [DATA]
  1031	
  1032	### Why it was wrong
  1033	
  1034	"Verified" should mean the memo has checked enough of the source to certify the claim. Here the safer claim is only that European evidence may be more mixed and that at least one fetched Scandinavian study appears relevant. Without analyzing the paper's definitions, denominators, offense categories, adjustment set, and immigrant subgroups, the memo should not certify the direction as verified. [INFERENCE]
  1035	
  1036	### Fix
  1037	
  1038	Changed the claims-table row from `MODERATE | VERIFIED (direction), not fully analyzed` to `LOW-MODERATE | PRELIMINARY — fetched but not fully analyzed`, and added a memo revision row. [SOURCE: memo]
  1039	
  1040	### Updated conclusion
  1041	
  1042	The U.S. crime-rate conclusion remains unchanged. The international caveat is now properly provisional until the European paper is read and source-graded. [INFERENCE]
  1043	
  1044	---
  1045	
  1046	## 2026-06-16 — QWI table wording changed from confirmatory to margin-specific
  1047	
  1048	### Issue
  1049	
  1050	`research/immigration-causal-synthesis-2026-04-18.md` still said the Saiz/QWI cycle "confirms wage channel is small" in the local-burden summary table. That phrase was too broad even though the same memo elsewhere bounded the E-Verify design. [DATA]
  1051	
  1052	### Why it was wrong
  1053	
  1054	QWI state-panel evidence supports a small/null wage response in the observed E-Verify mandate margin. It does not confirm that every wage channel is small across surge inflows, mass deportation, cash-economy sectors, within-state heterogeneity, or longer-run adjustment. The table row should not be broader than the tested design. [INFERENCE]
  1055	
  1056	### Fix
  1057	
  1058	Changed the row to say QWI supports a small/null wage response in the observed E-Verify margin, and added a synthesis revision row. [SOURCE: memo]
  1059	
  1060	### Updated conclusion
  1061	
  1062	The synthesis still treats the wage channel as weak in the tested E-Verify design, while preserving the open questions for untested shock regimes and other labor-market margins. [INFERENCE]
  1063	
  1064	---
  1065	
  1066	## 2026-06-16 — E-Verify verdict sentence narrowed to large-gain margin
  1067	
  1068	### Issue
  1069	
  1070	`research/immigration-causal-synthesis-2026-04-18.md` still said "the Borjas wage prediction is rejected at conventional significance levels." That sentence remained broader than the table and ladder wording fixed earlier in the same memo. [DATA]
  1071	
  1072	### Why it was wrong
  1073	
  1074	The E-Verify TWFE result is strong against large Borjas-style native wage gains from E-Verify-style labor-supply contraction. It is not a rejection of the full Borjas wage-prediction family across Mariel-style composition shocks, surge regimes, mass deportation, cash-economy sectors, or longer-run adjustment. This was an external-validity weak link: design margin -> claim family. [INFERENCE]
  1075	
  1076	### Fix
  1077	
  1078	Replaced the broad verdict with the narrower claim that large Borjas-style native wage gains from E-Verify-style labor-supply contraction are rejected at conventional significance levels, and added a synthesis revision row. [SOURCE: memo]
  1079	
  1080	### Updated conclusion
  1081	
  1082	The causal synthesis is now consistent across table, ladder block, and verdict paragraph: strong against high-end Borjas magnitudes in the observed E-Verify margin, not a global labor-substitution verdict. [INFERENCE]
  1083	
  1084	---
  1085	
  1086	## 2026-06-16 — Mexico +$46k all-in row changed from falsified to unsupported
  1087	
  1088	### Issue
  1089	
  1090	`research/immigration-mexico-npv-population-synthesis-2026-06-15.md` labeled the hypothesis `+$46k = immigrant pays for themselves all-in` as **Falsified** because school, admin, courts, and shelter were not netted into the warehouse layer. [DATA]
  1091	
  1092	### Why it was wrong
  1093	
  1094	Missing ledgers block the all-in inference, but they do not by themselves prove the all-in sign is negative or that the immigrant fails to pay for themselves after all offsets are modeled. This is an inference-validity problem, not a falsified empirical proposition. The correct claim is narrower: `+$46k` is not a valid all-in export from the synthetic NAS age-25 benchmark. [INFERENCE]
  1095	
  1096	### Fix
  1097	
  1098	Changed the row to `Unsupported / not a valid export — school, admin, courts, shelter not netted` and added a memo revision row. [SOURCE: memo]
  1099	
  1100	### Updated conclusion
  1101	
  1102	The memo still blocks scalar laundering of the `+$46k` benchmark into an all-in fiscal verdict, but it no longer overclaims that the full all-in sign has been falsified. [INFERENCE]
  1103	
  1104	---
  1105	
  1106	## 2026-06-16 — Restrictionist steel-man aligned on Mexico +$46k export
  1107	
  1108	### Issue
  1109	
  1110	`research/immigration-restrictionist-arguments-steelman-2026-06-15.md` still summarized `+$46k Mexico = net contributor all-in` as **False** because admin, courts, and full local layers were missing. That conflicted with the corrected Mexico NPV memo, which now treats the export as unsupported rather than empirically falsified. [DATA]
  1111	
  1112	### Why it was wrong
  1113	
  1114	The restrictionist steel-man should not turn an omitted-ledger critique into a completed negative all-in verdict. Missing admin, court, school, and shelter layers invalidate the scalar export; they do not by themselves measure the all-in sign. [INFERENCE]
  1115	
  1116	### Fix
  1117	
  1118	Changed the disconfirmation row to `Unsupported / invalid scalar export` and added a memo revision row. [SOURCE: memo]
  1119	
  1120	### Updated conclusion
  1121	
  1122	Both memos now carry the same inference boundary: the `+$46k` benchmark cannot be quoted as all-in net contribution, but the full stacked sign remains an open modeling question. [INFERENCE]
  1123	
  1124	---
  1125	
  1126	## 2026-06-16 — Borjas Mariel wording changed from replication to generalization
  1127	
  1128	### Issue
  1129	
  1130	`research/immigration-causal-synthesis-2026-04-18.md` described Borjas's restricted-Mariel reanalysis as a finding that "does not replicate in broader staggered designs." [DATA]
  1131	
  1132	### Why it was wrong
  1133	
  1134	E-Verify TWFE and Foged-Peri refugee-assignment evidence are not direct replications of the Mariel reanalysis. They are adjacent external-validity tests of whether large Borjas-style native low-skill wage losses/gains appear in other quasi-experimental designs. Calling that "replication" overstates the methodological relationship. [INFERENCE]
  1135	
  1136	### Fix
  1137	
  1138	Changed the sentence to "does not generalize to the broader staggered designs tested here" and added a synthesis revision row. [SOURCE: memo]
  1139	
  1140	### Updated conclusion
  1141	
  1142	The wage synthesis now distinguishes direct replication from external-validity evidence: Borjas's restricted-Mariel estimate remains a contested Mariel result, while the repo's newer designs cut against extrapolating that magnitude to observed E-Verify-style policy variation. [INFERENCE]
  1143	
  1144	---
  1145	
  1146	## 2026-06-16 — Mexico surge row scoped to unauthorized-stock growth
  1147	
  1148	### Issue
  1149	
  1150	`research/immigration-mexico-npv-population-synthesis-2026-06-15.md` said "Mexico drove surge" was **Falsified** because Mexico unauthorized stock was flat, and its Biden-stock section said "surge was non-Mexico." [DATA]
  1151	
  1152	### Why it was wrong
  1153	
  1154	The evidence cited there is a stock ledger: Mexico unauthorized population was roughly flat while the post-2021 unauthorized-stock increase came from non-Mexico origins. That does not adjudicate every surge metric. Encounter events, lawful/parole flows, receiver-city shelter load, and local operational pressure are different ledgers. Flat Mexico unauthorized stock falsifies a Mexico-driven unauthorized-stock-growth claim, not the broader phrase "Mexico drove surge." [INFERENCE]
  1155	
  1156	### Fix
  1157	
  1158	Changed the Biden-stock bullet to say post-2021 unauthorized-stock growth was non-Mexico on this ledger, and changed the disconfirmation row to `Mexico drove post-2021 unauthorized-stock growth | Falsified on this stock ledger`. Added a memo revision row. [SOURCE: memo]
  1159	
  1160	### Updated conclusion
  1161	
  1162	The Mexico memo still blocks the "10M+ new Mexican unauthorized residents" style claim, but it no longer overextends a stock finding to all encounter, flow, or receiver-load surge interpretations. [INFERENCE]
  1163	
  1164	---
  1165	
  1166	## 2026-06-16 — Steel-man Mexico +$46k line scoped to `<HS` export
  1167	
  1168	### Issue
  1169	
  1170	`research/immigration-restrictionist-arguments-steelman-2026-06-15.md` said "Mexico +$46k mix kills monolithic 'Mexican drain'." After the Mexico NPV memo was corrected, that wording was too strong. [DATA]
  1171	
  1172	### Why it was wrong
  1173	
  1174	The `+$46k` figure is a synthetic NAS age-25 education-mix benchmark. It blocks the restrictionist move of applying the NAS `<HS` cell to all Mexico-origin adults, because the observed education mix includes HS, some-college, and BA+ cells. But it does not kill every possible full-ledger Mexico-origin drain claim once school, state/local, admin, court, legal-status, and episodic shelter layers are modeled. [INFERENCE]
  1175	
  1176	### Fix
  1177	
  1178	Changed the line to say the benchmark blocks `<HS`-only "Mexican drain" exports, but is not an all-in origin scalar. Added a memo revision row. [SOURCE: memo]
  1179	
  1180	### Updated conclusion
  1181	
  1182	The steel-man now preserves both sides of the correction: restrictionists cannot launder a low-education NAS cell into "all Mexicans," and expansionists cannot launder the `+$46k` benchmark into an all-in positive origin verdict. [INFERENCE]
  1183	
  1184	---
  1185	
  1186	## 2026-06-16 — GPT calibration removed from wage-evidence stack
  1187	
  1188	### Issue
  1189	
  1190	`research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md` said three convergent tests showed no measurable native low-skill wage gains: E-Verify, sanctuary state DiD, and "GPT-5.4 calibration interpretation." Its verdict table also called the sanctuary result a "third confirmation." [DATA]
  1191	
  1192	### Why it was wrong
  1193	
  1194	The GPT-5.4 calibration is model-assisted parameter-sensitivity reasoning for the open-borders welfare-weight frame. It is not an empirical wage design. Counting it as a wage test inflates the evidence stack and blurs measurement with model interpretation. The wage stack should be QWI E-Verify + QWI sanctuary, read alongside external Card/Foged-Peri literature. [INFERENCE]
  1195	
  1196	### Fix
  1197	
  1198	Changed the sanctuary row to "additional QWI policy-margin check" and rewrote Statement 1 to say two repo QWI policy-margin tests, read alongside Card/Foged-Peri literature, support the bounded wage conclusion. Explicitly moved GPT-5.4 calibration back to the welfare-weight sensitivity frame. Added a memo revision row. [SOURCE: memo]
  1199	
  1200	### Updated conclusion
  1201	
  1202	The wage conclusion remains strong for the tested marginal-policy range, but the evidence count is now honest: model sensitivity is not empirical wage confirmation. [INFERENCE]
  1203	
  1204	---
  1205	
  1206	## 2026-06-16 — Confidence ladder stopped calling sanctuary a third wage confirmation
  1207	
  1208	### Issue
  1209	
  1210	`research/immigration-confidence-ladder.md` entry 21 still called the sanctuary QWI null a "Third convergent confirmation" of the Card-side wage channel after the paradigm synthesis had removed GPT-5.4 calibration from the wage-evidence stack. [DATA]
  1211	
  1212	### Why it was wrong
  1213	
  1214	Once model calibration is excluded, the repo has two internal QWI policy-margin wage checks in this cycle: E-Verify and sanctuary policy. External Card/Foged-Peri evidence still matters, but the ladder should not imply a third internal empirical wage design. [INFERENCE]
  1215	
  1216	### Fix
  1217	
  1218	Changed entry 21 to "strong null result in this design" and described it as an additional QWI policy-margin check consistent with E-Verify, bounded to observed marginal policy variation. [SOURCE: memo]
  1219	
  1220	### Updated conclusion
  1221	
  1222	The wage conclusion is unchanged, but its evidence count is no longer inflated. [INFERENCE]
  1223	
  1224	---
  1225	
  1226	## 2026-06-16 — Foged-Peri design label downgraded from random assignment
  1227	
  1228	### Issue
  1229	
  1230	`research/immigration-causal-synthesis-2026-04-18.md` said Foged-Peri native wages rose under "random refugee assignment," and `research/immigration-causal-everify-card-vs-borjas.md` used the opaque design label "RA quasi-IV." [DATA]
  1231	
  1232	### Why it was wrong
  1233	
  1234	The Foged-Peri design is strong, but not a simple randomized trial. The paper describes a Danish refugee dispersal policy that allocated refugees using nationality, family size, housing availability, and clustering goals; identification comes from quasi-experimental dispersal unrelated to local labor demand plus later refugee-country inflows. Calling it merely "random assignment" overstates the design and hides the IV/DiD structure. [SOURCE: /Volumes/2TBPNY/research-data/immigration-fiscal/data/external/lifetime/nber/foged_peri_2016_immigrants_effect_native_workers_w19315.pdf] [INFERENCE]
  1235	
  1236	### Fix
  1237	
  1238	Changed the synthesis wording to "refugee dispersal-policy quasi-experiment" and changed the comparison-table design label to "Dispersal-policy IV / DiD." Added revision rows to both memos. [SOURCE: memo]
  1239	
  1240	### Updated conclusion
  1241	
  1242	Foged-Peri remains useful external evidence against large native low-skill wage losses in that Danish setting, but the repo should export it as quasi-experimental dispersal evidence, not as RCT-style random assignment. [INFERENCE]
  1243	
  1244	---
  1245	
  1246	## 2026-06-16 — Residual wage replication language narrowed
  1247	
  1248	### Issue
  1249	
  1250	After the first Mariel/generalization fix, several wage memos still said this cycle "replicates" Card/Foged-Peri/Card-Peri/Orrenius-Zavodny patterns or that the sanctuary design "replicates E-Verify margin." [DATA]
  1251	
  1252	### Why it was wrong
  1253	
  1254	Those are not direct replications of the same estimands, populations, data, or designs. They are convergent or consistency checks: QWI E-Verify and QWI sanctuary policy margins line up with the Card-side literature, while Foged-Peri is a distinct Danish dispersal-policy design. [INFERENCE]
  1255	
  1256	### Fix
  1257	
  1258	Changed the causal synthesis, E-Verify memo, and paradigm synthesis to use "convergent," "consistent with," "extends," and "aligned with" instead of replication language. Added revision rows in the affected memos. [SOURCE: memo]
  1259	
  1260	### Updated conclusion
  1261	
  1262	The Card-side wage reading is still supported for observed marginal-policy designs, but the repo no longer claims direct replication where it only has adjacent evidence. [INFERENCE]
  1263	
  1264	---
  1265	
  1266	## 2026-06-16 — First causal synthesis stopped treating welfare weight as fully non-empirical
  1267	
  1268	### Issue
  1269	
  1270	`research/immigration-causal-synthesis-2026-04-18.md` said the Clemens place-premium / immigrant-welfare-weight lever was "a values choice, not an empirical question" and that no amount of additional data could resolve it. [DATA]
  1271	
  1272	### Why it was wrong
  1273	
  1274	The welfare weight itself is normative, but the place-premium, native-cost, fiscal, housing/capacity, and sending-country inputs are empirical. Evidence cannot choose the moral weight, but it can move scenario break-evens under any chosen weight. [INFERENCE]
  1275	
  1276	### Fix
  1277	
  1278	Changed the honest-reflection paragraph to separate the normative welfare weight from empirical inputs, and added a revision row to the first causal synthesis. [SOURCE: memo]
  1279	
  1280	### Updated conclusion
  1281	
  1282	The initial synthesis now matches the corrected paradigm memo: state the welfare-weight assumption, but keep collecting and grading the non-weight inputs. [INFERENCE]
  1283	
  1284	---
  1285	
  1286	## 2026-06-16 — Caplan global-gains verdict bounded to direction
  1287	
  1288	### Issue
  1289	
  1290	`research/immigration-bryan-caplan-claims-audit-2026-04-21.md` already said the economic case mostly survives in direction rather than strongest magnitude, but its bottom-line score still said Caplan was simply "strong on global gains" and "wins on migrant welfare and global gains." [DATA]
  1291	
  1292	### Why it was wrong
  1293	
  1294	That shorthand could be read as endorsing the strongest open-borders magnitude or as closing destination-capacity concerns. The memo's own evidence supports a narrower claim: migrant-welfare direction and large global-gains sign survive, while realistic volume, housing, congestion, and political constraints bound magnitude and destination-country incidence. [INFERENCE]
  1295	
  1296	### Fix
  1297	
  1298	Changed the clean verdict and net-summary bullet to say Caplan wins on migrant-welfare direction and large global-gains sign, not strongest magnitude or destination-capacity closure. Added a revision section to the Caplan audit. [SOURCE: memo]
  1299	
  1300	### Updated conclusion
  1301	
  1302	The Caplan audit now keeps its pro-open-borders credit without laundering sign evidence into an unconstrained magnitude/capacity verdict. [INFERENCE]
  1303	
  1304	---
  1305	
  1306	## 2026-06-16 — Capacity frontier native-sorting sentence made descriptive
  1307	
  1308	### Issue
  1309	
  1310	`research/immigration-capacity-frontier-2026-04-21.md` said the load-capacity decile table was a direct answer to the destination-country question because "once immigrant inflow materially outruns local build response, domestic incumbents sort away more aggressively." [DATA]
  1311	
  1312	### Why it was wrong
  1313	
  1314	The decile evidence is a county association: high load-capacity deciles show more negative domestic net migration. It does not by itself identify whether immigrant load caused incumbents to leave, whether destination selection drives both variables, or whether unmodeled local shocks explain part of the pattern. [INFERENCE]
  1315	
  1316	### Fix
  1317	
  1318	Changed the sentence to call the decile table a descriptive screen and state that causal incumbent-exit interpretation still needs counterfactual identification. Added a memo revision row. [SOURCE: memo]
  1319	
  1320	### Updated conclusion
  1321	
  1322	The capacity memo still shows a useful load-capacity/native-migration association, but it no longer exports the association as a causal sorting mechanism. [INFERENCE]
  1323	
  1324	---
  1325	
  1326	## 2026-06-16 — Surge ladder stopped endorsing decisive Card-side phrasing
  1327	
  1328	### Issue
  1329	
  1330	`research/immigration-causal-surge-2021-2024.md` and confidence-ladder entry 29 said prior entries claimed a "decisive Card-side win for U.S. policy variation" and then treated that as true for 2008-2021 variation. [DATA]
  1331	
  1332	### Why it was wrong
  1333	
  1334	The static-cycle wage work supports a bounded Card-side reading for observed E-Verify/sanctuary-style marginal policy variation. Calling it "decisive" for U.S. policy variation over-compresses the external-validity boundary and conflicts with later caveats around surge and mass-shock regimes. [INFERENCE]
  1335	
  1336	### Fix
  1337	
  1338	Rewrote entry 29 in both the surge memo and standalone confidence ladder to say the prior phrasing was overcompressed and that the safer reading is strong Card-side evidence for observed 2008-2021 marginal policy variation. Added a surge memo revision row. [SOURCE: memo]
  1339	
  1340	### Updated conclusion
  1341	
  1342	The surge memo still marks 2021-2024 as outside the static-cycle wage variation, but it no longer endorses the static-cycle result as a decisive general U.S. policy verdict. [INFERENCE]
  1343	
  1344	---
  1345	
  1346	## 2026-06-16 — CHNV superseded ladder entries marked invalid, not just superseded
  1347	
  1348	### Issue
  1349	
  1350	`research/immigration-confidence-ladder.md` entries 26 and 30 still carried the old CHNV "did not substitute / added on top" conclusion. Entry 30 even said the descriptive fact survived and "substitution did not happen," despite entry 34 reversing that reading after the OHSS parser correction. [DATA]
  1351	
  1352	### Why it was wrong
  1353	
  1354	The corrected USBP/OFO split changed the descriptive sign: CHNV substituted lawful port flow for irregular between-port crossings in its initial year, even though total lawful parole inflow still landed in receiver-city ledgers. A mere "superseded" label left too much room to quote the old conclusion as a weaker live claim. [SOURCE: decisions/2026-06-11-ohss-date-universe-bugs-chnv-reversal.md] [INFERENCE]
  1355	
  1356	### Fix
  1357	
  1358	Marked entries 26 and 30 as invalidated/historical-only, and rewrote entry 30's reason to say the old `+787%` figure is an error trace from the lawful OFO channel on a scrambled clock. [SOURCE: memo]
  1359	
  1360	### Updated conclusion
  1361	
  1362	The standalone ladder now exports only entry 34 for CHNV: channel substitution occurred initially for USBP between-port crossings, while total lawful parole inflow remains a receiver-load ledger. [INFERENCE]
  1363	
  1364	---
  1365	
  1366	## 2026-06-16 — Lott crime critique downgraded from verified flaw to supported critique
  1367	
  1368	### Issue
  1369	
  1370	`research/immigration-crime-rates-unauthorized-vs-native-born.md` rated the claim that Lott's Arizona study had a "fundamental data classification flaw" as `HIGH` and `VERIFIED`. The memo cited Cato, Washington Post, and Latino Decisions critiques, but did not itself reanalyze the Arizona DOC data. [DATA]
  1371	
  1372	### Why it was wrong
  1373	
  1374	Multiple independent critiques are enough to mark Lott as an unresolved outlier and weak source, but they are not the same thing as an independent verification of the underlying classification error. The status label should distinguish "supported critique" from "verified by our own reanalysis." [INFERENCE]
  1375	
  1376	### Fix
  1377	
  1378	Changed the assessment wording from "shown to be unreliable" to "seriously challenged," and changed the claims-table row to `MODERATE-HIGH` / `SUPPORTED CRITIQUE — not independent reanalysis`. Added a memo revision row. [SOURCE: memo]
  1379	
  1380	### Updated conclusion
  1381	
  1382	The crime memo still treats Lott as an outlier whose central data issue is unresolved, but it no longer overstates the memo's own evidentiary posture against the contrarian study. [INFERENCE]
  1383	
  1384	---
  1385	
  1386	## 2026-06-16 — NH-white fiscal ratios aligned to tensor anchor
  1387	
  1388	### Issue
  1389	
  1390	`research/immigration-europe-caucasian-fiscal-findings-2026-06-15.md` still listed NH-white-all federal annual as `$2,803–3,005`, and `research/immigration-lifetime-country-approx-brainstorm-2026-06-15.md` still listed headline ratios `nh_white_all/fb_lt_hs ~4.4x`, `nh_white_all/mexico_origin ~2.0x`, and `nh_white_fborn/nh_white_usborn ~1.5x`. [DATA]
  1391	
  1392	### Why it was wrong
  1393	
  1394	The current tensor export gives `nh_white_all` federal annual `2802.7`, `fb_lt_hs` `676.8`, `mexico_origin` `1519.3`, `nh_white_fborn` `3897.6`, and `nh_white_usborn` `2746.3`. Those imply roughly `4.1x`, `1.8x`, and `1.4x`, respectively. Keeping stale rounded ratios overstates the white-vs-Mexico and white-vs-low-skill gaps. [SOURCE: infra/immigration-fiscal/build/stage3_proto/country_fiscal_rollup_2023.csv] [DATA]
  1395	
  1396	### Fix
  1397	
  1398	Replaced the stale NH-white-all range with `$2,803` and aligned the brainstorm ratios to the current tensor export. Added revision rows to both affected memos. [SOURCE: memo]
  1399	
  1400	### Updated conclusion
  1401	
  1402	The corridor story remains the same, but the numeric headline is tighter: the current narrow federal proxy shows about `1.8x` NH-white-all/Mexico and about `4.1x` NH-white-all/FB-`<HS`, not the older larger rounded ratios. [DATA]
  1403	
  1404	---
  1405	
  1406	## 2026-06-16 — Open-borders weight framing separated from empirical inputs
  1407	
  1408	### Issue
  1409	
  1410	`research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md` and confidence-ladder entry 23 described the open-borders verdict as "welfare-weight-determined, not data-determined" and said the repo could not resolve it empirically. That phrasing risked treating model cost/capacity inputs as settled merely because the welfare weight itself is normative. [DATA]
  1411	
  1412	### Why it was wrong
  1413	
  1414	The welfare weight assigned to immigrants is a value choice. But scenario costs, fiscal ledgers, housing/capacity constraints, labor-market adjustment, and sending-country effects are empirical inputs. New evidence cannot pick the moral weight, but it can move the break-even thresholds under any chosen weight. [INFERENCE]
  1415	
  1416	### Fix
  1417	
  1418	Reframed the paradigm synthesis and embedded ladder text around a normative weight plus empirical inputs, annotated confidence-ladder entry 23 as qualified, and added entry 39 with the corrected reading. Added a memo revision row. [SOURCE: memo]
  1419	
  1420	### Updated conclusion
  1421	
  1422	The open-borders conclusion still must state its welfare-weight assumption, but the repo should keep collecting and grading cost/feasibility evidence rather than treating the scenario as fully non-empirical. [INFERENCE]
  1423	
  1424	---
  1425	
  1426	## 2026-06-16 — Second-generation crime row scoped to broad literature pattern
  1427	
  1428	### Issue
  1429	
  1430	`research/immigration-crime-rates-unauthorized-vs-native-born.md` rated "second-generation immigrants have higher crime rates..." as `HIGH` / `VERIFIED`. [DATA]
  1431	
  1432	### Why it was wrong
  1433	
  1434	The memo cites broad generational immigration-crime literature for that row. It is not an unauthorized-only, current-surge, or source-read-fresh estimate, so it should not carry the same status as the Texas DPS/PNAS administrative rows. [INFERENCE]
  1435	
  1436	### Fix
  1437	
  1438	Changed the paragraph and claims-table row to a scope-limited supported literature pattern with `MODERATE` confidence. Added a revision row to the memo. [SOURCE: memo]
  1439	
  1440	### Updated conclusion
  1441	
  1442	The crime memo can still flag generational convergence as a caveat, but not as a high-certainty claim about unauthorized immigrants or the 2021-2024 cohort. [INFERENCE]
  1443	
  1444	---
  1445	
  1446	## 2026-06-16 — Residual replication labels narrowed to consistency checks
  1447	
  1448	### Issue
  1449	
  1450	Two tracked memos still used "replication" language for checks that were not direct replications: `immigration-causal-saiz-elasticity-rent.md` said the 2022 cross-section "replicates Saiz's own pattern," and `immigration-confidence-ladder.md` said the E-Verify QWI result "Replicates Card direction." A receiver-city ladder entry also called a Hispanic-share control a "Replication gate." [DATA]
  1451	
  1452	### Why it was wrong
  1453	
  1454	The Saiz pass is a 2022 descriptive cross-section, not Saiz's 1980-2000 panel/IV design. The E-Verify result is an adjacent QWI policy-margin check that aligns with Card-side direction, not a direct Card replication. The receiver-city Hispanic-share pass is a robustness gate against a named confounder, not a replication. [INFERENCE]
  1455	
  1456	### Fix
  1457	
  1458	Changed the Saiz memo to "consistent with the Saiz elasticity/rent mechanism," changed the E-Verify ladder line to "Aligns with Card direction; not a direct replication," and renamed the receiver-city phrase to "Hispanic-share robustness gate passed." Added a Saiz memo revision row. [SOURCE: memo]
  1459	
  1460	### Updated conclusion
  1461	
  1462	The affected claims remain useful consistency or robustness evidence, but the repo no longer exports them as direct replications. [INFERENCE]
  1463	
  1464	---
  1465	
  1466	## 2026-06-16 — Capacity-frontier causal verbs made descriptive
  1467	
  1468	### Issue
  1469	
  1470	`research/immigration-capacity-frontier-2026-04-21.md` had a scope note saying `HIGH`/`VERIFIED` referred to reproducible model-output patterns rather than causal identification, but the claims table still said wage growth "responds" to load-capacity and native net migration "becomes" more negative as load-capacity rises. The wage section also called the row the "clearest county confirmation" of the worker question. [DATA]
  1471	
  1472	### Why it was wrong
  1473	
  1474	Those phrases made the descriptive county models sound like response or mechanism estimates. The listed artifacts verify coefficient patterns, not the counterfactual effect of immigrant load on wages, employment, or native sorting. [INFERENCE]
  1475	
  1476	### Fix
  1477	
  1478	Changed the wage row to model-loading language, changed the native-migration row to a decile association, and replaced "confirmation" with "descriptive evidence." Added a memo revision row. [SOURCE: memo]
  1479	
  1480	### Updated conclusion
  1481	
  1482	The capacity-frontier memo still supports load-capacity as the cleaner county stress screen, but it no longer overstates the table rows as causal response estimates. [INFERENCE]
  1483	
  1484	---
  1485	
  1486	## 2026-06-16 — Standalone E-Verify ladder row aligned to bounded margin
  1487	
  1488	### Issue
  1489	
  1490	`research/immigration-confidence-ladder.md` entry 17 still rated the E-Verify/Borjas wage result as `strong rejection`, even though the source memo and causal synthesis had already narrowed the result to large Borjas-style native wage gains in the observed E-Verify mandate margin. [DATA]
  1491	
  1492	### Why it was wrong
  1493	
  1494	The QWI design can reject high-end native wage gains for the tested E-Verify policy variation. It does not reject every Borjas-style labor-substitution claim, surge regime, mass-deportation shock, cash-economy margin, or longer-run adjustment channel. [INFERENCE]
  1495	
  1496	### Fix
  1497	
  1498	Renamed the ladder row to "Large Borjas-style native wage gains under observed E-Verify mandates," changed the rating to `strong against large gains in this design`, and made the reason explicitly margin-specific. [SOURCE: memo]
  1499	
  1500	### Updated conclusion
  1501	
  1502	The ladder now matches the source memos: strong Card-side evidence for the tested E-Verify margin, not a global wage-family rejection. [INFERENCE]
  1503	
  1504	---
  1505	
  1506	## 2026-06-16 — Caplan crime shorthand scoped to observed justice-system rates
  1507	
  1508	### Issue
  1509	
  1510	`research/immigration-bryan-caplan-claims-audit-2026-04-21.md` correctly bounded the crime row in its executive table and caveats, but its shorthand verdict still said `strong on crime skepticism`, `crime skepticism`, and `Caplan wins on crime`. [DATA]
  1511	
  1512	### Why it was wrong
  1513	
  1514	The crime memo's corrected estimand is observed U.S. arrest, conviction, incarceration, and institutionalization rates for first-generation / unauthorized immigrants. It is not directly observed true offending, not international evidence, and not a current-surge subgroup estimate. The shorthand needed to carry the same scope as the body. [INFERENCE]
  1515	
  1516	### Fix
  1517	
  1518	Changed the shorthand verdicts to observed U.S. justice-system-rate skepticism and added a Caplan-audit revision row. [SOURCE: memo]
  1519	
  1520	### Updated conclusion
  1521	
  1522	Caplan remains strongest on the U.S. crime-objection lane, but only for the observed justice-system-rate claim already defended in the crime memo. [INFERENCE]
  1523	
  1524	---
  1525	
  1526	## 2026-06-16 — FAIR taxpayer-drain line marked as conditional claim
  1527	
  1528	### Issue
  1529	
  1530	`research/immigration-restrictionist-arguments-steelman-2026-06-15.md` had already renamed FAIR as an advocacy high-cost ledger, but the F2 argument chain still said "Policy implication: Massive net drain; every taxpayer ~$956-1,156/yr" without marking that line as FAIR's implication rather than the repo's conclusion. [DATA]
  1531	
  1532	### Why it was wrong
  1533	
  1534	The number comes from FAIR's contested ledger. It can be preserved as part of the restrictionist steel-man, but it should not read like a validated taxpayer-incidence estimate until FAIR/ITEP/Pew stock, child-attribution, household-benefit, and cost-allocation choices are reconciled. [INFERENCE]
  1535	
  1536	### Fix
  1537	
  1538	Changed the line to "Policy implication [FAIR claim, conditional on its contested ledger]" and added a memo revision row. [SOURCE: memo]
  1539	
  1540	### Updated conclusion
  1541	
  1542	The steel-man still records FAIR's full-budget argument, but the taxpayer-drain implication is now explicitly conditional on FAIR's construction. [INFERENCE]
  1543	
  1544	---
  1545	
  1546	## 2026-06-16 — Steel-man crime-wave row scoped to observed-rate evidence
  1547	
  1548	### Issue
  1549	
  1550	`research/immigration-restrictionist-arguments-steelman-2026-06-15.md` summarized "Crime wave from unauthorized" as `Mostly false — repo crime memo`. [DATA]
  1551	
  1552	### Why it was wrong
  1553	
  1554	The repo crime memo now supports a narrower claim: observed U.S. justice-system rates for first-generation / unauthorized immigrants are lower in the best current evidence. It does not directly measure true offending, all international contexts, or every current-surge subgroup. [INFERENCE]
  1555	
  1556	### Fix
  1557	
  1558	Changed the disconfirmation row to `Unsupported by observed U.S. justice-system-rate evidence` and added the true-offending/current-surge scope caveat. Added a memo revision row. [SOURCE: memo]
  1559	
  1560	### Updated conclusion
  1561	
  1562	The steel-man still rejects the simple unauthorized-crime-wave claim, but on the correct observed-rate evidence surface rather than a broader true-crime assertion. [INFERENCE]
  1563	
  1564	---
  1565	
  1566	## 2026-06-16 — Receiver-election exposure wording narrowed to indicators
  1567	
  1568	### Issue
  1569	
  1570	`research/immigration-causal-surge-2021-2024.md` still titled the election section "2024 election shift x surge exposure" and said the shift was correlated with "receiver-city / border-surge exposure." [DATA]
  1571	
  1572	### Why it was wrong
  1573	
  1574	The memo's verified object is a county screen using receiver-city and border/high-immigration indicators, plus foreign-born share and recent foreign-born inflow controls. It does not measure an exposure dose, identify causal voter response to the surge, or decompose border counties from broader Hispanic realignment and local political trends. [INFERENCE]
  1575	
  1576	### Fix
  1577	
  1578	Renamed the section to receiver/border indicators, changed the interpretation paragraph to describe indicator associations, and removed "handling the surge directly" / "absorbing current inflow" language. Added a memo revision row. [SOURCE: memo]
  1579	
  1580	### Updated conclusion
  1581	
  1582	The receiver-election result remains a bounded correlational signal: receiver-city status is associated with about +2.4pp GOP shift after controls, but it is not a measured surge-exposure effect. [INFERENCE]
  1583	
  1584	---
  1585	
  1586	## 2026-06-16 — Saiz housing language narrowed to renter incidence
  1587	
  1588	### Issue
  1589	
  1590	Several active Saiz/housing summaries still said rent exposure was "closer to welfare loss" than the adversarial review allowed. The source Saiz memo, the causal synthesis embedded ladder, the paradigm synthesis verdict table, and confidence-ladder entry 18 all carried some version of that shorthand. [DATA]
  1591	
  1592	### Why it was wrong
  1593	
  1594	The Saiz evidence supports an elasticity-conditional renter-incidence warning: immigrants are concentrated in inelastic/high-rent MSAs, so rent exposure is more decision-relevant for renters than a raw price-level measure. But aggregate welfare loss still requires causal identification of immigrant-specific rent effects plus owner/renter incidence and tax-base offsets. [INFERENCE]
  1595	
  1596	### Fix
  1597	
  1598	Replaced the residual "closer to welfare loss" phrasing with "stronger renter-incidence warning" in the source Saiz memo, the causal synthesis, the paradigm synthesis, and confidence-ladder entry 18. Added revision rows where those memos keep revision tables. [SOURCE: memo]
  1599	
  1600	### Updated conclusion
  1601	
  1602	The housing layer remains a real local-incidence warning, especially in inelastic destinations, but it is no longer exported as an aggregate welfare-loss claim. [INFERENCE]
  1603	
  1604	---
  1605	
  1606	## 2026-06-16 — Card-side wage labels softened from wins to favored
  1607	
  1608	### Issue
  1609	
  1610	Active synthesis and ladder text still used "Card-side pattern wins" / "Card-wins" after earlier fixes had bounded the result to observed marginal enforcement variation. [DATA]
  1611	
  1612	### Why it was wrong
  1613	
  1614	"Wins" language suggests debate closure. The evidence is strong against large Borjas-style native wage gains in the tested E-Verify/sanctuary-style margins, but surge, mass-shock, cash-economy, and longer-run channels remain open. [INFERENCE]
  1615	
  1616	### Fix
  1617	
  1618	Replaced active "wins" labels with "Card-side pattern is favored" or "Card-side wage finding is bounded" in the causal synthesis, paradigm synthesis, surge memo embedded ladder, and standalone confidence ladder. [SOURCE: memo]
  1619	
  1620	### Updated conclusion
  1621	
  1622	The Card-side wage reading remains strong for observed marginal enforcement designs, but the repo no longer labels the bounded comparison as a global win. [INFERENCE]
  1623	
  1624	---
  1625	
  1626	## 2026-06-16 — Clark economist correctness language narrowed to channel support
  1627	
  1628	### Issue
  1629	
  1630	The E-Verify memo and causal synthesis still said the Clark "agree" economists were "correct" or "right" on the wage channel after the underlying findings had been bounded to observed marginal policy variation. [DATA]
  1631	
  1632	### Why it was wrong
  1633	
  1634	The source Clark audit treated the strongest agree responses as mostly right only if read as small native-wage-effect or complementarity claims, and explicitly rejected the idea that the poll settled the full welfare/local-capacity question. The E-Verify design supports that narrow premise; it does not adjudicate the economists' broader survey answers or every wage regime. [SOURCE: research/immigration-verified-findings-report-2026-04-10.md] [INFERENCE]
  1635	
  1636	### Fix
  1637	
  1638	Replaced "right/correct" language with support for the small-native-wage-effect premise in the observed E-Verify / marginal-policy wage channel. [SOURCE: memo]
  1639	
  1640	### Updated conclusion
  1641	
  1642	The Clark-side wage premise is stronger than the repo initially allowed for observed marginal enforcement variation, but the repo no longer calls the economists globally right even on a compressed "wage channel" label. [INFERENCE]
  1643	
  1644	---
  1645	
  1646	## 2026-06-16 — Capacity frontier settling language narrowed to descriptive updates
  1647	
  1648	### Issue
  1649	
  1650	`research/immigration-capacity-frontier-2026-04-21.md` still said earlier county passes "established" the relevant variables and titled its final synthesis "What this settles, and what it does not." [DATA]
  1651	
  1652	### Why it was wrong
  1653	
  1654	The memo's own scope note says `HIGH` and `VERIFIED` refer to reproducible model-output patterns, not clean causal effects. County capacity regressions can sharpen descriptive stress objects and research priorities, but they do not settle the local-incidence causal graph. [SOURCE: memo] [INFERENCE]
  1655	
  1656	### Fix
  1657	
  1658	Changed "established" to "suggested," retitled the final section as "What this updates, and what it does not settle," and changed "real residual signal" to "model residual signal." [SOURCE: memo]
  1659	
  1660	### Updated conclusion
  1661	
  1662	The capacity-frontier memo now exports descriptive model-output updates rather than settled causal conclusions about flow/capacity thresholds. [INFERENCE]
  1663	
  1664	---
  1665	
  1666	## 2026-06-16 — Restrictionist steel-man binary verdict softened
  1667	
  1668	### Issue
  1669	
  1670	`research/immigration-restrictionist-arguments-steelman-2026-06-15.md` summarized the steel-man as "restrictionists are right on layer multiplication, wrong on single-scalar panic." [DATA]
  1671	
  1672	### Why it was wrong
  1673	
  1674	The memo is a steel-man of claim structure, not a final side-taking verdict. The evidence supports the restrictionist insight that fiscal, local, legal-status, cohort, and service-capacity layers can diverge, but the "right/wrong" formulation over-compressed a mixed evidentiary map into a binary judgment. [INFERENCE]
  1675	
  1676	### Fix
  1677	
  1678	Changed the synthesis to say the restrictionist case is best supported on layer multiplication and weakest when those layers collapse into single-scalar panic. [SOURCE: memo]
  1679	
  1680	### Updated conclusion
  1681	
  1682	The steel-man keeps its strongest mechanism without presenting restrictionism as simply right or wrong in aggregate. [INFERENCE]
  1683	
  1684	---
  1685	
  1686	## 2026-06-16 — Caplan verdict labels changed from wins/loses to strength lanes
  1687	
  1688	### Issue
  1689	
  1690	`research/immigration-bryan-caplan-claims-audit-2026-04-21.md` still used active verdict labels like "mostly right on the sign," "partly right on one channel," and "Caplan wins/loses" in the net summary. [DATA]
  1691	
  1692	### Why it was wrong
  1693	
  1694	The supporting evidence in the memo is lane-specific: global migrant-welfare direction, observed-rate crime skepticism, labor-market caveats, and destination-capacity/political-incidence failures. Binary win/loss language hides that decomposition and invites copying the shorthand without the scoped claims. [INFERENCE]
  1695	
  1696	### Fix
  1697	
  1698	Replaced the residual verdict labels with direction/sign survives, partly supported, strongest/weakest lane language, while preserving the same substantive ranking. [SOURCE: memo]
  1699	
  1700	### Updated conclusion
  1701	
  1702	The Caplan audit now reads as a lane-by-lane support map rather than a debate scorecard. [INFERENCE]
  1703	
  1704	---
  1705	
  1706	## 2026-06-16 — Caplan right-label residue narrowed
  1707	
  1708	### Issue
  1709	
  1710	After the broader Caplan verdict cleanup, the audit still used "Caplan is right" labels in the global-gains, worker-protection, fiscal-ledger, and causal-graph sections. [DATA]
  1711	
  1712	### Why it was wrong
  1713	
  1714	The source evidence is lane-specific and asymmetric: place-premium scale survives, ledger-blurring criticism survives in some fiscal arguments, broad employment-collapse rhetoric is unsupported, and constrained-place wage pressure remains live. Calling Caplan "right" compresses those separable claims with unresolved destination-incidence lanes. [SOURCE: memo] [INFERENCE]
  1715	
  1716	### Fix
  1717	
  1718	Changed the surviving points to claim-support language: place-premium scale, ledger-blurring criticism, unsupported collapse rhetoric, and "where Caplan's case is supported" DAG framing. [SOURCE: memo]
  1719	
  1720	### Updated conclusion
  1721	
  1722	The Caplan audit now separates supported objections from unresolved destination-incidence concerns without relying on "Caplan is right" shorthand. [INFERENCE]
  1723	
  1724	---
  1725	
  1726	## 2026-06-16 — School burden denominator fix scoped to narrow export
  1727	
  1728	### Issue
  1729	
  1730	`research/immigration-school-burden-per-adult-2026-06-15.md` said the corrected denominator "kills the stale claim" that the built annual school layer alone overwhelms Mexico's federal proxy. [DATA]
  1731	
  1732	### Why it was wrong
  1733	
  1734	The correction is real, but its scope is a specific annual school-burden export under the corrected full Mexico adult denominator. "Kills" can be copied as if the broader school-cost or all-government fiscal claim family had been falsified. The memo itself says lifetime NPV, state/local surge, enforcement, courts, and episodic shelter layers remain separate. [SOURCE: memo] [INFERENCE]
  1735	
  1736	### Fix
  1737	
  1738	Replaced "kills" with "invalidates the stale narrow export" and named the corrected adult denominator as the reason. [SOURCE: memo]
  1739	
  1740	### Updated conclusion
  1741	
  1742	The school-burden memo now says the corrected denominator blocks one narrow annual-school-layer export, without implying that broader fiscal or school-burden questions are settled. [INFERENCE]
  1743	
  1744	---
  1745	
  1746	## 2026-06-16 — E-Verify adjustment mechanism made unresolved
  1747	
  1748	### Issue
  1749	
  1750	`research/immigration-causal-everify-card-vs-borjas.md` inferred that E-Verify produced employer adjustment through capital, automation, relocation, cash-economy hiring, outsourcing, and similar channels after observing lower QWI E1 employment and flat wages. [DATA]
  1751	
  1752	### Why it was wrong
  1753	
  1754	The QWI design observes stable W-2 employment and earnings cells. It can support the pattern "QWI E1 employment fell while wages did not rise" in the tested state mandate design, but it does not directly measure true labor-supply contraction, capital substitution, firm exit, relocation, cash-economy movement, hours, occupation, or establishment-composition shifts. The weak link was mechanism attribution from a reduced-form wage/employment pattern. [SOURCE: memo] [INFERENCE]
  1755	
  1756	### Fix
  1757	
  1758	Replaced mechanism-identifying language with a bounded interpretation: the large native wage-bidding channel is not observed in this design; the listed adjustment channels are candidate hypotheses, not measured mechanisms. [SOURCE: memo]
  1759	
  1760	### Updated conclusion
  1761	
  1762	The E-Verify result remains evidence against large native wage gains in the observed mandate margin, but the mechanism absorbing the shock is unresolved. [INFERENCE]
  1763	
  1764	---
  1765	
  1766	## 2026-06-16 — E-Verify supply-contraction wording narrowed to measured design
  1767	
  1768	### Issue
  1769	
  1770	The E-Verify source memo and causal synthesis still exported the design as "removing/restricting unauthorized labor" or "E-Verify contracts unauthorized labor supply." [DATA]
  1771	
  1772	### Why it was wrong
  1773	
  1774	The design observes state E-Verify mandate timing, QWI stable W-2 employment, and QWI earnings. It does not directly observe total unauthorized labor supply, off-W-2 work, compliance intensity, or cross-state reallocation. Treating mandate variation as measured labor-supply contraction overstates the data surface. [SOURCE: memo] [INFERENCE]
  1775	
  1776	### Fix
  1777	
  1778	Replaced those exports with "observed E-Verify mandate variation" and QWI wage language in the E-Verify memo and causal synthesis. [SOURCE: memo]
  1779	
  1780	### Updated conclusion
  1781	
  1782	The result remains strong against large native wage gains in observed E-Verify mandate designs, but it no longer implies that total unauthorized labor supply contraction was directly measured. [INFERENCE]
  1783	
  1784	---
  1785	
  1786	## 2026-06-16 — Europe/Caucasian fiscal comparison kept on proxy surface
  1787	
  1788	### Issue
  1789	
  1790	`research/immigration-europe-caucasian-fiscal-findings-2026-06-15.md` said EU27 foreign-born "beat" native Caucasians, that foreign-born whites "raise the Caucasian average," and listed positive-selection mechanisms as if the table decomposed them. [DATA]
  1791	
  1792	### Why it was wrong
  1793	
  1794	The memo's ledger is a narrow federal annual proxy: payroll/FICA minus SNAP, TANF, and SSI. It does not measure full federal taxes, state/local services, lifetime NPV, visa path, age-at-arrival, English proficiency, or cohort timing. The table can show a higher proxy value for EU27/NH-white-FB groups; it cannot by itself prove the selection mechanism or a broad fiscal superiority claim. [SOURCE: memo] [INFERENCE]
  1795	
  1796	### Fix
  1797	
  1798	Replaced "beat"/"raise average" with narrow federal-proxy comparison language, and changed mechanism wording to "consistent with positive selection" while naming unmeasured channels. [SOURCE: memo]
  1799	
  1800	### Updated conclusion
  1801	
  1802	The Europe/Caucasian memo still supports a corridor-selection screen on the federal proxy, but no longer exports that screen as a broad fiscal verdict or measured selection mechanism. [INFERENCE]
  1803	
  1804	---
  1805	
  1806	## 2026-06-16 — Sanctuary wage null phrasing changed to non-significance
  1807	
  1808	### Issue
  1809	
  1810	`research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md` and confidence-ladder entry 21 called the sanctuary QWI wage result a "STRONG null result" and said policy variation "does not change" native low-skill wages either direction. [DATA]
  1811	
  1812	### Why it was wrong
  1813	
  1814	The cited evidence is that all E1 specifications had `|t|<1.0` in the TWFE design. That is a non-significance statement, not an equivalence test proving a zero effect or bounding all practically meaningful effects. The result still aligns with the bounded Card-side reading, but the statistical claim should not exceed "no statistically significant E1 wage change observed." [SOURCE: memo] [INFERENCE]
  1815	
  1816	### Fix
  1817	
  1818	Changed the active paradigm synthesis row, embedded ladder snippet, and standalone confidence-ladder entry to say no statistically significant E1 wage change was observed, and added that equivalence was not tested. [SOURCE: memo]
  1819	
  1820	### Updated conclusion
  1821	
  1822	The sanctuary QWI pass remains a useful policy-margin check against obvious large wage movement, but the repo no longer treats non-significance as a proven strong null. [INFERENCE]
  1823	
  1824	---
  1825	
  1826	## 2026-06-16 — Confidence ladder Saiz zoning entry made descriptive
  1827	
  1828	### Issue
  1829	
  1830	`research/immigration-confidence-ladder.md` entry 20 still said the inelastic-MSA immigrant concentration was "driven by zoning, not topography" and exported zoning reform as a viable lever, even though entry 38 later qualified the result. [DATA]
  1831	
  1832	### Why it was wrong
  1833	
  1834	The Saiz decomposition is a cross-sectional regression where WRLURI is a stronger correlate than topographic unavailability. It does not identify causal direction or prove that zoning reform would reduce immigrant renter burden. Leaving the old causal wording in entry 20 created a grep hazard despite the later qualifier. [SOURCE: memo] [INFERENCE]
  1835	
  1836	### Fix
  1837	
  1838	Replaced entry 20's title, rating, and reason with stronger-correlate/descriptive wording and recast zoning reform as a plausible hypothesis rather than a verified causal lever. [SOURCE: memo]
  1839	
  1840	### Updated conclusion
  1841	
  1842	The confidence ladder now treats the Saiz regulatory result as descriptive evidence for a zoning hypothesis, not as proof that zoning caused immigrant concentration or solves renter incidence. [INFERENCE]
  1843	
  1844	---
  1845	
  1846	## 2026-06-16 — E-Verify wage shorthand changed to statistical non-significance
  1847	
  1848	### Issue
  1849	
  1850	`research/immigration-causal-everify-card-vs-borjas.md` and `research/immigration-causal-synthesis-2026-04-18.md` still used shortcuts like "wages did not rise" and "does not raise native wages" for the E-Verify QWI wage result. [DATA]
  1851	
  1852	### Why it was wrong
  1853	
  1854	The memo's own power caveat says the design rejects large Borjas-style gains for the observed mandate margin but cannot reject small positive effects. The shortcut wording could be reused as an exact-zero or equivalence claim rather than a no-statistically-significant-positive-effect finding. [SOURCE: memo] [INFERENCE]
  1855	
  1856	### Fix
  1857	
  1858	Changed the active E-Verify bullet and synthesis table rows to "no statistically significant positive QWI wage effect" while preserving the existing large-gain rejection and observed-mandate scope. [SOURCE: memo]
  1859	
  1860	### Updated conclusion
  1861	
  1862	The E-Verify wage evidence remains strong against large native wage gains in the tested QWI mandate design, but the repo no longer phrases the result as if it proves wages literally did not rise or could not rise by a small amount. [INFERENCE]
  1863	
  1864	---
  1865	
  1866	## 2026-06-16 — Restrictionist steel-man verdict residue removed
  1867	
  1868	### Issue
  1869	
  1870	`research/immigration-restrictionist-arguments-steelman-2026-06-15.md` still opened with "restrictionists are often right" / "often wrong" verdict language even though the revision log said the binary right/wrong synthesis had been replaced. [DATA]
  1871	
  1872	### Why it was wrong
  1873	
  1874	The memo is a steel-man and layer map, not a side-scoring artifact. The evidence supports some restrictionist claims about omitted layers and weakens some scalar shortcuts, but a right/wrong verdict compresses distinct labor, fiscal, local-capacity, crime, and status claims into a side label. [SOURCE: memo] [INFERENCE]
  1875	
  1876	### Fix
  1877	
  1878	Replaced the active verdict with synthesis language about strongest and weakest claim forms, and renamed the labor-market section header from "What restrictionists get right" to "Supported restrictionist insight." [SOURCE: memo]
  1879	
  1880	### Updated conclusion
  1881	
  1882	The steel-man now evaluates claim structure without presenting restrictionism as a binary winner or loser in aggregate. [INFERENCE]
  1883	
  1884	---
  1885	
  1886	## 2026-06-16 — E-Verify Card-vs-Borjas title scoped to wage channel
  1887	
  1888	### Issue
  1889	
  1890	`research/immigration-causal-everify-card-vs-borjas.md` was titled as a "Card-vs-Borjas verdict for U.S. data," and the synthesis section was headed as an "explicit verdict" even though the current evidence is an observed E-Verify/QWI wage-channel test. [DATA]
  1891	
  1892	### Why it was wrong
  1893	
  1894	The body already says the result is bounded to observed mandate variation and does not settle surge regimes, mass shocks, open borders, cash-economy sectors, or all wage-family claims. Title and heading text are high-reuse surfaces; if overbroad, they can undo the caveats below. [SOURCE: memo] [INFERENCE]
  1895	
  1896	### Fix
  1897	
  1898	Retitled the E-Verify memo as an observed wage-channel test, narrowed the question to positive QWI wage effects under state mandates, changed the synthesis heading to "E-Verify wage-channel verdict," and replaced another "wages did NOT rise" shortcut with statistical non-significance wording. [SOURCE: memo]
  1899	
  1900	### Updated conclusion
  1901	
  1902	The E-Verify material now presents itself as a bounded wage-channel design: strong against large Borjas-style gains in observed mandate variation, not a general Card-vs-Borjas verdict for U.S. immigration data. [INFERENCE]
  1903	
  1904	---
  1905	
  1906	## 2026-06-16 — Open-borders weight shorthand replaced at old claim sites
  1907	
  1908	### Issue
  1909	
  1910	`research/immigration-confidence-ladder.md` entry 23 and `research/immigration-causal-surge-2021-2024.md` still used "welfare-weight-determined" / "not data-determined" shorthand for the open-borders verdict, despite later corrections separating the normative weight from empirical inputs. [DATA]
  1911	
  1912	### Why it was wrong
  1913	
  1914	The immigrant-welfare weight is a value choice, but native-cost benchmarks, fiscal ledgers, housing/capacity constraints, and sending-country effects are empirical inputs that can move break-even thresholds. Leaving "not data-determined" at old claim sites risks turning a framing correction into a reason to stop measuring costs and feasibility. [SOURCE: memo] [INFERENCE]
  1915	
  1916	### Fix
  1917	
  1918	Changed confidence-ladder entry 23 to "welfare-weight-sensitive under current empirical inputs," expanded its reason to name empirical break-even inputs, and changed the surge memo heading to "welfare-weight and capacity-input components." [SOURCE: memo]
  1919	
  1920	### Updated conclusion
  1921	
  1922	The open-borders framing now distinguishes the non-empirical welfare-weight choice from empirical cost and capacity inputs that remain live research targets. [INFERENCE]
  1923	
  1924	---
  1925	
  1926	## 2026-06-16 — Title 42 surge claim narrowed to proximate timing
  1927	
  1928	### Issue
  1929	
  1930	`research/immigration-causal-surge-2021-2024.md` and confidence-ladder entry 35 said the Title 42 lift "did not cause the surge." The corrected event-study evidence shows a Dec-2022 local peak, April-May anticipation spike, June post-lift crash, and a lower six-month post-lift mean; it does not prove a universal zero causal effect. [DATA]
  1931	
  1932	### Why it was wrong
  1933	
  1934	The timing evidence refutes the prior parser-artifact story that a post-lift jump caused the surge. But event timing alone cannot exclude effects through anticipation, routing, composition, enforcement expectations, or later equilibrium channels. "Did not cause" was stronger than the identified claim. [SOURCE: memo] [INFERENCE]
  1935	
  1936	### Fix
  1937	
  1938	Changed the active surge memo and confidence-ladder entries to say the corrected timing does not support the Title 42 lift as the proximate surge onset, and added explicit caveats about nonzero policy effects through other channels. [SOURCE: memo]
  1939	
  1940	### Updated conclusion
  1941	
  1942	The repo now rejects the simple post-lift-jump causal story, while leaving other Title 42 policy-effect channels open unless separately tested. [INFERENCE]
  1943	
  1944	---
  1945	
  1946	## 2026-06-16 — Welfare-magnet policy implication made conditional
  1947	
  1948	### Issue
  1949	
  1950	`research/immigration-restrictionist-arguments-steelman-2026-06-15.md` stated "Immigration + welfare expansion = fiscal unsustainability and wrong skill mix" as a policy implication in the Razin welfare-state chain. [DATA]
  1951	
  1952	### Why it was wrong
  1953	
  1954	The memo is mapping a restrictionist argument chain, and this channel is not modeled in the repo's DuckDB layer. Razin-style welfare-magnet models can support a conditional adverse fiscal/skill-mix equilibrium claim, but the memo had not established an unqualified finding of fiscal unsustainability. [SOURCE: memo] [INFERENCE]
  1955	
  1956	### Fix
  1957	
  1958	Marked the implication as a "Razin-style model claim" and reframed it as a possible adverse fiscal and skill-mix equilibrium with response margins of low-skill restrictions, benefit restrictions, or welfare-state design changes. [SOURCE: memo]
  1959	
  1960	### Updated conclusion
  1961	
  1962	The welfare-magnet chain remains a live restrictionist mechanism, but it is now explicitly conditional on the model rather than a repo-level fiscal-unsustainability verdict. [INFERENCE]
  1963	
  1964	---
  1965	
  1966	## 2026-06-16 — Newcomer denominator comparison kept off burden pressure
  1967	
  1968	### Issue
  1969	
  1970	`research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md` said "Most county newcomer pressure is not immigration-specific" and that the "local-burden ledger is mostly domestic-mover driven" based on the IRS domestic U.S.-origin flow versus ACS moved-from-abroad median-county comparison. [DATA]
  1971	
  1972	### Why it was wrong
  1973	
  1974	The comparison is a useful denominator correction: at the median county, domestic U.S.-origin mover counts are much larger than moved-from-abroad counts. But the inputs are not like-for-like burden measures, the IRS series is not native-only, and the median-county comparison does not measure concentrated receiver-node shelter, legal, language, school, or wage incidence. [SOURCE: memo] [INFERENCE]
  1975	
  1976	### Fix
  1977	
  1978	Replaced "pressure" and "local-burden ledger" phrasing with median-county count/denominator language in the top verdict table, Statement 2, and embedded ladder reason. [SOURCE: memo]
  1979	
  1980	### Updated conclusion
  1981	
  1982	The domestic-vs-abroad comparison now supports only a descriptive median-county denominator correction; it cannot dismiss immigrant-specific receiver-node burden channels without a separate incidence design. [INFERENCE]
  1983	
  1984	---
  1985	
  1986	## 2026-06-16 — Wage-response shorthand kept off equivalence
  1987	
  1988	### Issue
  1989	
  1990	`research/immigration-causal-synthesis-2026-04-18.md`, `research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md`, and `research/immigration-causal-everify-card-vs-borjas.md` still used residual shorthand such as "small/null," "do not measurably respond," and "does not measurably transfer rents" for observed E-Verify/sanctuary QWI wage results. [DATA]
  1991	
  1992	### Why it was wrong
  1993	
  1994	The designs support no statistically significant positive QWI wage effect and reject large Borjas-style gains in the tested margins. They do not prove an equivalence-tested zero or rule out small wage effects. Shorthand like "small/null" can collapse large-gain rejection into a stronger no-effect conclusion. [SOURCE: memo] [INFERENCE]
  1995	
  1996	### Fix
  1997	
  1998	Replaced the active shorthand with no-statistically-significant-positive-QWI-wage-effect language, kept the large-gain rejection, and explicitly preserved small effects, employment composition, hours, occupational sorting, cash-economy, and shock-regime channels as outside the current wage result. [SOURCE: memo]
  1999	
  2000	### Updated conclusion
  2001	
  2002	The wage evidence now reads as a bounded statistical result: large native wage gains are not observed in the tested QWI policy margins, but small or unmeasured labor-market effects remain open. [INFERENCE]
  2003	
  2004	---
  2005	
  2006	## 2026-06-16 — E-Verify incidence summary stopped saying wages do not rise
  2007	
  2008	### Issue
  2009	
  2010	`research/immigration-causal-synthesis-2026-04-18.md` still said native low-skill wages "do not rise" and "do not measurably rise" under observed E-Verify mandate variation in its incidence-summary bullets. [DATA]
  2011	
  2012	### Why it was wrong
  2013	
  2014	Those lines were active reader-facing summaries. The source result is no statistically significant positive QWI wage effect plus rejection of large Borjas-style gains in that margin, not a literal no-rise or equivalence-tested zero. [SOURCE: memo] [INFERENCE]
  2015	
  2016	### Fix
  2017	
  2018	Replaced the incidence-summary bullets with no-statistically-significant-positive-QWI-wage-effect language and kept the large-gain rejection scoped to the E-Verify-style enforcement design. [SOURCE: memo]
  2019	
  2020	### Updated conclusion
  2021	
  2022	The causal synthesis now keeps the E-Verify wage result at the same statistical strength in both the top table and the incidence narrative. [INFERENCE]
  2023	
  2024	---
  2025	
  2026	## 2026-06-16 — Mass-deportation simulation kept as calibration output
  2027	
  2028	### Issue
  2029	
  2030	`research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md` still said mass deportation "would impose" the first-order output shock, and `research/immigration-causal-surge-2021-2024.md` described the lead figure as a GDP "cost" from removing 7M unauthorized workers. [DATA]
  2031	
  2032	### Why it was wrong
  2033	
  2034	The source is a BEA input-output partial-equilibrium calibration, not an observed or validated deportation episode. It freezes replacement hiring, wage response, and capital reallocation, and the Type-II endpoint is a multiplier sensitivity. The claim should present model output under assumptions, not a direct forecast. [SOURCE: memo] [INFERENCE]
  2035	
  2036	### Fix
  2037	
  2038	Changed the paradigm synthesis and surge memo to say the model produces or calibrates to a first-order output shock under calibration assumptions, while keeping the Type-II endpoint labeled as sensitivity. [SOURCE: memo]
  2039	
  2040	### Updated conclusion
  2041	
  2042	The mass-deportation result remains a medium-confidence calibration warning about possible output scale, not an empirical estimate of what would happen under an actual enforcement regime. [INFERENCE]
  2043	
  2044	---
  2045	
  2046	## 2026-06-16 — Card-side wage evidence separated from complementarity mechanism
  2047	
  2048	### Issue
  2049	
  2050	`research/immigration-causal-synthesis-2026-04-18.md`, `research/immigration-confidence-ladder.md`, and `research/immigration-causal-everify-card-vs-borjas.md` still used shorthand such as Card (1990) "zero wage effect," "Card-style labor-market complementarity," and observed shocks "do not move native low-skill wages much." [DATA]
  2051	
  2052	### Why it was wrong
  2053	
  2054	The cited designs support bounded native-wage-impact evidence against large losses or gains in those designs. They do not prove literal zero effects, identify one shared complementarity mechanism across Mariel/E-Verify/Foged-Peri, or rule out small effects. [SOURCE: memo] [INFERENCE]
  2055	
  2056	### Fix
  2057	
  2058	Changed the Card/Mariel wording to no detected adverse effect, retitled the confidence-ladder and embedded ladder entry as "Card-side bounded native-wage-impact evidence," and replaced "do not move wages much" with no-large-native-wage-loss/gain language plus a mechanism caveat. [SOURCE: memo]
  2059	
  2060	### Updated conclusion
  2061	
  2062	The repo now treats the Card-side stack as bounded wage-impact evidence, not as proof of zero wages or a single identified complementarity mechanism. [INFERENCE]
  2063	
  2064	---
  2065	
  2066	## 2026-06-16 — E-Verify external-validity claim narrowed
  2067	
  2068	### Issue
  2069	
  2070	`research/immigration-causal-everify-card-vs-borjas.md` said the E-Verify QWI design "IS the relevant test for the actual policy debate" after noting it may not generalize to mass deportation, large refugee inflow, or border closure. [DATA]
  2071	
  2072	### Why it was wrong
  2073	
  2074	Observed state E-Verify mandates are one important marginal-enforcement design. They are not the whole policy debate, which includes border closure, interior enforcement intensity, mass deportation, benefit restrictions, legal admissions, and surge regimes. Calling it "the" relevant test overstates external validity. [SOURCE: memo] [INFERENCE]
  2075	
  2076	### Fix
  2077	
  2078	Changed the external-validity caveat to say the E-Verify design is one relevant test for marginal tightening of unauthorized labor supply via state enforcement mandates, not the policy debate as a whole. [SOURCE: memo]
  2079	
  2080	### Updated conclusion
  2081	
  2082	The E-Verify memo now keeps its policy relevance without treating one marginal-enforcement design as sufficient for all immigration-policy wage claims. [INFERENCE]
  2083	
  2084	---
  2085	
  2086	## 2026-06-16 — Borjas restricted-Mariel extrapolation narrowed
  2087	
  2088	### Issue
  2089	
  2090	`research/immigration-causal-synthesis-2026-04-18.md`, `research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md`, and confidence-ladder entry 19 still said Borjas's restricted-Mariel result "does not generalize" to the broader designs. [DATA]
  2091	
  2092	### Why it was wrong
  2093	
  2094	The newer E-Verify/sanctuary/Foged-Peri-adjacent evidence cuts against mechanically exporting the restricted-Mariel magnitude to observed marginal enforcement designs. But it does not prove a universal non-generalization of the Mariel result across all possible low-skill shocks. [SOURCE: memo] [INFERENCE]
  2095	
  2096	### Fix
  2097	
  2098	Replaced "does not generalize" with "should not be mechanically extrapolated" to the observed E-Verify/sanctuary-style or broader staggered designs. [SOURCE: memo]
  2099	
  2100	### Updated conclusion
  2101	
  2102	The wage synthesis now treats Borjas's restricted-Mariel result as a contested shock-specific estimate whose magnitude should not be mechanically exported to other designs, while leaving broader external-validity questions open. [INFERENCE]
  2103	
  2104	---
  2105	
  2106	## 2026-06-16 — Crime denominator and race-correction caveats tightened
  2107	
  2108	### Issue
  2109	
  2110	`research/immigration-crime-rates-unauthorized-vs-native-born.md` said a larger true unauthorized population would make crime rates "even lower," called the race-corrected gap a general correction to observed criminal-justice rates, and said within-race comparison "eliminates the compositional confound entirely." [DATA]
  2111	
  2112	### Why it was wrong
  2113	
  2114	The denominator statement is only mechanically true if the arrest numerator and immigration-status classification are held fixed. The race correction cited in the memo is an incarceration comparison, not a correction to every arrest/conviction measure. Within-race comparison removes racial composition as a confound, but it does not remove age, sex, geography, detection/reporting, or legal-status-classification uncertainty. [SOURCE: memo] [INFERENCE]
  2115	
  2116	### Fix
  2117	
  2118	Scoped the confidence statement to observed U.S. criminal-justice outcomes while naming the race-corrected figure as incarceration-specific; rewrote denominator sensitivity as conditional on fixed numerator/classification; and narrowed the within-race assessment to removal of the racial-composition confound. [SOURCE: memo]
  2119	
  2120	### Updated conclusion
  2121	
  2122	The crime memo's directional observed-rate finding remains, but its construction caveats now distinguish denominator arithmetic, incarceration-specific race correction, and remaining non-race confounders. [INFERENCE]
  2123	
  2124	---
  2125	
  2126	## 2026-06-16 — Local-burden wage channel scoped to observed margin
  2127	
  2128	### Issue
  2129	
  2130	`research/immigration-causal-synthesis-2026-04-18.md` said "The total local burden is school-finance + housing-rent + service-capacity, NOT wage compression." [DATA]
  2131	
  2132	### Why it was wrong
  2133	
  2134	The E-Verify QWI design rejects large positive native wage gains from marginal enforcement and does not support wage compression as the local-burden channel in that observed margin. It does not measure all current-inflow or surge wage effects, so "NOT wage compression" overstated the scope of the null. [SOURCE: memo] [INFERENCE]
  2135	
  2136	### Fix
  2137	
  2138	Changed the synthesis to say wage compression is not the supported local-burden channel in this cycle's observed E-Verify wage margin, while school-finance, housing-rent, and service capacity remain live channels and surge/current-inflow wage compression remains unmeasured. [SOURCE: memo]
  2139	
  2140	### Updated conclusion
  2141	
  2142	The local-incidence synthesis now distinguishes a bounded wage-margin result from broader wage-shock uncertainty. [INFERENCE]
  2143	
  2144	---
  2145	
  2146	## 2026-06-16 — Caplan channel ranking bounded to evidence surface
  2147	
  2148	### Issue
  2149	
  2150	`research/immigration-bryan-caplan-claims-audit-2026-04-21.md` said the repo's evidence did not point to culture as the "first binding destination-country channel," that current U.S. stress channels run more through housing/services/politics, and that political externalities being manageable by default is "too optimistic." [DATA]
  2151	
  2152	### Why it was wrong
  2153	
  2154	The repo has better-developed evidence for housing, services, shelter, and political-response channels than for a clean culture-collapse mechanism. That does not prove a universal channel ordering or show that culture is never first-binding; it only supports a bounded criticism of Caplan's destination-incidence closure. [SOURCE: memo] [INFERENCE]
  2155	
  2156	### Fix
  2157	
  2158	Changed the Caplan audit to describe the current evidence surface as better developed for housing/service/shelter/political channels; added that this is not proof culture is never first-binding; changed political-response language from stronger signals to association signals; and replaced "too optimistic" with "not established" for manageable-by-default political externalities. [SOURCE: memo]
  2159	
  2160	### Updated conclusion
  2161	
  2162	The Caplan critique still says his destination-local incidence answer is incomplete, but it no longer turns the repo's current evidence coverage into a proved first-binding channel ranking. [INFERENCE]
  2163	
  2164	---
  2165	
  2166	## 2026-06-16 — Cash-economy substitution caveat kept measurable
  2167	
  2168	### Issue
  2169	
  2170	`research/immigration-causal-everify-card-vs-borjas.md` said the true labor-supply contraction was "probably less" than the QWI E1 employment drop suggests and that this made the wage non-result "MORE puzzling for Borjas." [DATA]
  2171	
  2172	### Why it was wrong
  2173	
  2174	Off-W-2 substitution is a real measurement caveat, but the memo did not directly measure how much displaced unauthorized labor moved into cash work. "Probably less" and "MORE puzzling" turned a plausible measurement channel into an unmeasured directional claim. [SOURCE: memo] [INFERENCE]
  2175	
  2176	### Fix
  2177	
  2178	Changed the caveat to say cash-economy substitution weakens interpretation of the QWI E1 drop as a full labor-supply contraction, while not rescuing a large QWI-wage-gain prediction in this design. [SOURCE: memo]
  2179	
  2180	### Updated conclusion
  2181	
  2182	The E-Verify memo now treats cash-economy substitution as a measurement limitation, not as an unmeasured estimate of true labor-supply contraction. [INFERENCE]
  2183	
  2184	---
  2185	
  2186	## 2026-06-16 — Hanson wage counterfactual kept out of surge forecast
  2187	
  2188	### Issue
  2189	
  2190	`research/immigration-restrictionist-arguments-steelman-2026-06-15.md` said that when low-skill inflows resume in `2021–2023`, wage pressure on low-skill natives returns, and that Hanson implies a `+24% wage effect` if inflow had stayed at the `1994–2007` pace. [DATA]
  2191	
  2192	### Why it was wrong
  2193	
  2194	The local extract of Hanson w23753 frames the result as a counterfactual college/low-skill skill-premium gap: if low-skill inflow had continued, the `2015` skill premium would have been about `6–9` percentage points higher. That is a useful restrictionist labor-supply input, but it is not a direct estimate of surge-era native wage pressure and needs a cohort/geography/demand bridge before being exported to `2021–2023`. [SOURCE: research/immigration-restrictionist-corpus-parse-2026-06-15.md] [INFERENCE]
  2195	
  2196	### Fix
  2197	
  2198	Replaced the `+24%` wage-effect and resumed-inflow forecast phrasing with the source's narrower `6–9pp` skill-premium counterfactual and an explicit bridge requirement. [SOURCE: memo]
  2199	
  2200	### Updated conclusion
  2201	
  2202	The restrictionist steelman still gets to use Hanson as a labor-supply counterfactual and secular-supply warning, but not as an unbridged surge-era wage forecast. [INFERENCE]
  2203	
  2204	---
  2205	
  2206	## 2026-06-16 — Cycle summary narrowed to E-Verify wage margin
  2207	
  2208	### Issue
  2209	
  2210	`CYCLE.md` still said the causal cycle would "resolve Card-vs-Borjas verdict for U.S. data," that E-Verify mandates produced "no positive wage effect" and rejected Borjas's wage prediction, and that supply fell with wages flat implying employer adjustment through capital/relocation. [DATA]
  2211	
  2212	### Why it was wrong
  2213	
  2214	The underlying QWI design is an observed E-Verify mandate-margin test. It can reject large Borjas-style native wage gains in that design, but it does not settle the full Card-vs-Borjas family, surge or mass-shock regimes, or the mechanism behind the W-2 employment decline. [SOURCE: CYCLE.md] [SOURCE: research/immigration-causal-everify-card-vs-borjas.md] [INFERENCE]
  2215	
  2216	### Fix
  2217	
  2218	Changed the cycle goal, queue, discovery bullets, completion note, and verification result to describe a bounded observed E-Verify QWI wage-channel update. Mechanism language now lists capital, output, relocation, cash-economy substitution, hours, and composition as candidate channels rather than measured adjustment. [SOURCE: memo]
  2219	
  2220	### Updated conclusion
  2221	
  2222	The cycle summary no longer exports a broad labor-market verdict from one marginal enforcement design. [INFERENCE]
  2223	
  2224	---
  2225	
  2226	## 2026-06-16 — Capacity frontier political-map verb kept descriptive
  2227	
  2228	### Issue
  2229	
  2230	`research/immigration-capacity-frontier-2026-04-21.md` said "`stock` drives the broad political map" even though the same section and claims-table scope note treat the county models as descriptive model-output evidence rather than causal identification. [DATA]
  2231	
  2232	### Why it was wrong
  2233	
  2234	The model ranking shows that stock share carries the strongest one-predictor countywide political signal. "Drives" implies causal direction that this model does not identify, especially given confounders like long-run demographic sorting and Hispanic realignment already named in the memo. [SOURCE: memo] [INFERENCE]
  2235	
  2236	### Fix
  2237	
  2238	Changed the summary bullet to say stock carries the broad political-map signal in this county model. [SOURCE: memo]
  2239	
  2240	### Updated conclusion
  2241	
  2242	The capacity frontier memo now keeps its politics result at the descriptive model-signal level throughout that section. [INFERENCE]
  2243	
  2244	---
  2245	
  2246	## 2026-06-16 — E-Verify employment not used as deportation validation
  2247	
  2248	### Issue
  2249	
  2250	`research/immigration-confidence-ladder.md` said the mass-deportation calibration was "consistent with E-Verify empirical finding (-6% E1 employment under 50% compliance)." [DATA]
  2251	
  2252	### Why it was wrong
  2253	
  2254	The E-Verify employment result is a marginal state-enforcement design with partial compliance and QWI W-2 measurement. The mass-deportation run is a BEA partial-equilibrium calibration that freezes replacement hiring, wage response, and capital reallocation. Similar directional employment pressure is not validation of the national shock size or industry-loss magnitudes. [SOURCE: research/immigration-causal-everify-card-vs-borjas.md] [SOURCE: sources/immigration-causal/scripts/mass_deportation_sim.py] [INFERENCE]
  2255	
  2256	### Fix
  2257	
  2258	Changed entry 24 to treat E-Verify employment as, at most, a weak plausibility check under one marginal enforcement setting, and added entry 40 explicitly saying E-Verify employment does not validate the mass-deportation calibration. [SOURCE: memo]
  2259	
  2260	### Updated conclusion
  2261	
  2262	The ladder now separates a bounded empirical employment signal from a national partial-equilibrium deportation calibration. [INFERENCE]
  2263	
  2264	---
  2265	
  2266	## 2026-06-16 — Card setup kept as prediction language
  2267	
  2268	### Issue
  2269	
  2270	`research/immigration-causal-everify-card-vs-borjas.md` described the Card-side theory setup as "Removing [low-skill immigrants] via enforcement will produce small or zero wage gains for natives." [DATA]
  2271	
  2272	### Why it was wrong
  2273	
  2274	That section is a theory/prediction contrast, not a measured result. "Will produce" can read as an established claim rather than the Card-side prediction being tested by the E-Verify design. [SOURCE: memo] [INFERENCE]
  2275	
  2276	### Fix
  2277	
  2278	Changed the line to "is predicted to produce small or zero wage gains," keeping the subsequent empirical result separate from the setup. [SOURCE: memo]
  2279	
  2280	### Updated conclusion
  2281	
  2282	The E-Verify memo now distinguishes theory expectations from observed QWI findings in the interpretation setup. [INFERENCE]
  2283	
  2284	---
  2285	
  2286	## 2026-06-16 — Recent-inflow election mechanism left unresolved
  2287	
  2288	### Issue
  2289	
  2290	`research/immigration-causal-surge-2021-2024.md` said the negative `recent_fb_annual_share` coefficient "probably reflects D-leaning new immigrants voting D, or already-D establishment." [DATA]
  2291	
  2292	### Why it was wrong
  2293	
  2294	The regression output identifies an association in the model, not the mechanism. The memo's own interpretation paragraph correctly lists multiple possibilities, including new citizens, sympathetic natives, and unresolved compositional confounding. The bullet should not promote one mechanism with "probably" language. [SOURCE: memo] [INFERENCE]
  2295	
  2296	### Fix
  2297	
  2298	Changed the bullet to say counties with higher recent inflow swung less GOP in this model, while the mechanism remains unresolved across citizenship timing, already-D county context, sympathetic natives, and other compositional confounding. [SOURCE: memo]
  2299	
  2300	### Updated conclusion
  2301	
  2302	The surge memo now keeps the recent-inflow election coefficient at the model-association level until a mechanism-specific design is run. [INFERENCE]
  2303	
  2304	---
  2305	
  2306	## 2026-06-16 — Caplan worker-incidence channel kept evidence-surface scoped
  2307	
  2308	### Issue
  2309	
  2310	`research/immigration-bryan-caplan-claims-audit-2026-04-21.md` said the "strongest current worker-incidence channel" is slower wage progression in constrained places rather than job destruction. [DATA]
  2311	
  2312	### Why it was wrong
  2313	
  2314	The memo can say current repo evidence better develops constrained-place wage progression than broad job-destruction rhetoric. But "strongest current channel" implies a global channel ranking across worker incidence that the cited county panel does not establish. [SOURCE: memo] [INFERENCE]
  2315	
  2316	### Fix
  2317	
  2318	Changed the line to say that in the repo's current worker-incidence evidence surface, the better-developed concern is slower wage progression in constrained places rather than broad job destruction. [SOURCE: memo]
  2319	
  2320	### Updated conclusion
  2321	
  2322	The Caplan audit still rejects crude job-collapse rhetoric, while keeping the alternative worker-incidence channel scoped to the current evidence surface. [INFERENCE]
  2323	
  2324	---
  2325	
  2326	## 2026-06-16 — E-Verify event-study interpretation kept unresolved
  2327	
  2328	### Issue
  2329	
  2330	`research/immigration-causal-everify-card-vs-borjas.md` said slightly negative, nonsignificant event-study point estimates were "suggestive of mild complementarity loss," and said a mass-deportation shock would "probably not" behave the same as the E-Verify design. [DATA]
  2331	
  2332	### Why it was wrong
  2333	
  2334	The event-study coefficients are not statistically distinguishable from zero, so the memo should not give one mechanism a suggestive gloss. Likewise, mass deportation is outside the observed mandate margin; "probably not" is plausible, but the stronger source-anchored statement is simply that the behavior is unknown because magnitudes and equilibria differ. [SOURCE: memo] [INFERENCE]
  2335	
  2336	### Fix
  2337	
  2338	Changed the event-study sentence to say the slightly negative points should not be read as evidence for a specific complementarity-loss mechanism, and changed the mass-deportation bullet to "unknown" rather than "probably not." [SOURCE: memo]
  2339	
  2340	### Updated conclusion
  2341	
  2342	The E-Verify memo now keeps nonsignificant event-study movement and out-of-margin mass-shock behavior unresolved instead of assigning them a preferred mechanism. [INFERENCE]
--- END FILE: research/immigration-conclusion-audit-running-fixes.md ---

--- BEGIN FILE: research/immigration-causal-everify-card-vs-borjas.md ---
     1	# E-Verify staggered DiD on QWI — observed wage-channel test
     2	
     3	**Date:** 2026-04-18
     4	**Question:** Do state E-Verify mandates produce positive QWI wage effects for low-education native workers? Borjas-style large-gain predictions imply yes; Card-style small/native-null predictions imply small or no observed gains.
     5	**Design:** Two-way fixed effects (state + year) on log earnings of stable workers, by education and industry, 2003-2023. Treatment = year ≥ state E-Verify effective year. 9 treated states (AZ, MS, SC, UT, GA, AL, NC, TN, FL), 42 control states.
     6	
     7	## Bottom line
     8	
     9	E-Verify mandates produced **no statistically significant positive wage effect** on low-education workers in any of 12 specifications. Point estimates are tiny (within ±1.5%) with mixed signs. The Borjas wage prediction (~5-15% rise for less-than-HS workers) is rejected at conventional levels for this policy variation. **In this E-Verify design, the wage results are closer to the Card-style null than to large Borjas-style native wage gains.**
    10	
    11	Employment side: E1 (less than HS) stable W-2 employment in E-Verify-exposed industries (Ag, Constr, Mfg, Food Service) fell ~6% post-treatment (t=-1.40, marginal). Combined picture: QWI employment fell but no statistically significant positive wage effect was observed. That points away from large native wage bidding in this observed design; it does not identify whether adjustment happened through capital, output, relocation, cash-economy substitution, hours, or composition.
    12	
    13	## Method
    14	
    15	### Data
    16	- **QWI (Census LEHD)** `se` endpoint, 2003-Q1 to 2023-Q4, all 50 states + DC, 9 industries (00, 11 Ag, 23 Constr, 31-33 Mfg, 44-45 Retail, 56 Admin, 62 Health, 72 Accom/Food, 81 Other), 4 education groups (E1 less-HS, E2 HS, E3 some college, E4 BA+). 151k state×year×quarter×industry×education observations. [SOURCE: api.census.gov/data/timeseries/qwi/se]
    17	- **E-Verify mandate panel** (compiled from Bohn-Lofstrom-Raphael 2014, Orrenius-Zavodny 2015, state legislation):
    18	  - AZ effective 2008; MS 2008; SC 2010; UT 2010 (15+ ee); GA 2012 (10+ ee); AL 2012; NC 2012 (25+ ee); TN 2012 (6+ ee); FL 2023 (25+ ee)
    19	  - Public-only mandates (IN, MO, NE, OK, PA, VA, ID, MN, TX) excluded from treatment (don't bind on private labor market)
    20	
    21	### Specifications
    22	
    23	**Main TWFE:**
    24	$$\log \text{EarnS}_{ist} = \beta \cdot \text{EVerify}_{st} + \alpha_s + \gamma_t + \varepsilon_{ist}$$
    25	
    26	where i = (industry, education) cell, s = state, t = year×quarter. SE clustered at state level (Liang-Zeger).
    27	
    28	Run separately by education group, with three industry restrictions:
    29	- All industries (excluding 00 aggregate to avoid double-counting)
    30	- E-Verify-exposed (11, 23, 31-33, 72)
    31	- Total aggregate (00 only)
    32	
    33	**Event study:** Replace the treatment indicator with leads and lags 1[year - effective_year = k] for k ∈ {-6, ..., +8} \ {-1}. Identifies dynamic effects with state and year FEs absorbed.
    34	
    35	**Employment:** Same specification with log(EmpS) as outcome.
    36	
    37	## Results
    38	
    39	### TWFE main (clustered SE on state)
    40	
    41	| Education | Industry set | β (log earns) | % effect | SE | t | n |
    42	|-----------|--------------|---------------|----------|-----|---|---|
    43	| **E1 (<HS)** | All non-aggregate | -0.0044 | -0.44% | 0.0094 | -0.47 | 37,716 |
    44	| **E1 (<HS)** | E-Verify-exposed | +0.0051 | +0.51% | 0.0081 | +0.63 | 16,736 |
    45	| **E1 (<HS)** | Total aggregate (00) | -0.0148 | -1.46% | 0.0113 | -1.30 | 4,196 |
    46	| E2 (HS) | E-Verify-exposed | +0.0080 | +0.80% | 0.0080 | +0.99 | 16,737 |
    47	| E3 (some col) | E-Verify-exposed | +0.0039 | +0.39% | 0.0080 | +0.49 | 16,737 |
    48	| E4 (BA+) | E-Verify-exposed | -0.0096 | -0.95% | 0.0125 | -0.76 | 16,737 |
    49	
    50	**No coefficient reaches conventional significance (|t|>1.96). Point estimates are mostly within ±1%.** Borjas's prediction for E1 in exposed industries was a wage rise on the order of 5-15%; the 95% CI here excludes anything above +2.1%.
    51	
    52	### Event study (E1 in E-Verify-exposed industries)
    53	
    54	Pre-trends are flat. Post-treatment coefficients are slightly negative through year 7, then jump positive at year 8 with very high SE (likely COVID-era noise + small treated cohort at long horizons).
    55	
    56	| Event time | β (log earns) | SE |
    57	|-----------|---------------|-----|
    58	| -6 | +0.005 | 0.012 |
    59	| -5 | +0.002 | 0.011 |
    60	| -4 | -0.006 | 0.007 |
    61	| -3 | -0.004 | 0.006 |
    62	| -2 | +0.003 | 0.003 |
    63	| -1 | 0 (ref) | — |
    64	| 0 | +0.001 | 0.003 |
    65	| +1 | -0.005 | 0.005 |
    66	| +2 | -0.007 | 0.006 |
    67	| +3 | -0.009 | 0.007 |
    68	| +4 | -0.004 | 0.006 |
    69	| +5 | -0.006 | 0.008 |
    70	| +6 | -0.006 | 0.008 |
    71	| +7 | -0.004 | 0.010 |
    72	| +8 | +0.011 | 0.012 |
    73	
    74	No significant pre-trend. No significant post-treatment jump in either direction. Point estimates lean slightly negative for years 1-7, but they are not statistically distinguishable from zero and should not be read as evidence for a specific complementarity-loss mechanism.
    75	
    76	### Employment side
    77	
    78	| Education | Industry set | β (log emp) | % effect | t | n |
    79	|-----------|--------------|-------------|----------|---|---|
    80	| **E1** | E-Verify-exposed | **-0.0630** | **-6.11%** | -1.40 | 16,723 |
    81	| E1 | Total aggregate | -0.0089 | -0.88% | -0.22 | 4,196 |
    82	| E2 | E-Verify-exposed | -0.0153 | -1.52% | -0.48 | 16,723 |
    83	| E3 | E-Verify-exposed | -0.0149 | -1.48% | -0.60 | 16,721 |
    84	| E4 | E-Verify-exposed | -0.0129 | -1.28% | -0.50 | 16,719 |
    85	| E4 | Total aggregate | +0.0405 | **+4.13%** | +2.19** | 4,196 |
    86	
    87	**E1 stable-employment in exposed industries fell ~6% post-mandate** (marginal, p≈0.16). Consistent with Bohn-Lofstrom-Raphael (2014) finding for Arizona alone (~10pp unauthorized-pop decline). My pooled estimate is smaller because (a) I average across mandate states with varying enforcement intensity, (b) QWI captures W-2 employment so it underweights cash-economy displacement.
    88	
    89	Total-economy E4 (BA+) employment grew ~4% (p<0.05) but this likely reflects national skill-upgrading rather than mandate causal effect.
    90	
    91	## Interpretation
    92	
    93	### What Card predicted
    94	
    95	- Low-skill immigrants are imperfect substitutes for low-skill natives
    96	- Removing them via enforcement is predicted to produce small or zero wage gains for natives
    97	- General-equilibrium effects (output loss, capital reallocation, output-mix shift) may even hurt natives
    98	- Card-Peri (2016) and Foged-Peri (2016) Denmark: native low-skill workers move into more communication-intensive tasks, see no wage loss
    99	
   100	### What Borjas predicted
   101	
   102	- Substitution elasticity is high; immigrant supply shifts shift the native wage curve down
   103	- Borjas (2003) QJE: 10% increase in supply lowers wages of competing natives by 3-4%
   104	- Borjas (2017) reanalysis of Mariel Boatlift: -10 to -30% wage drop for HS dropouts
   105	- Implication: removing unauthorized labor should raise native low-skill wages substantially
   106	
   107	### What the data show
   108	
   109	- **No statistically significant positive QWI wage effect was observed for native low-skill workers after E-Verify**, in any of 12 specifications, including the most sympathetic test (E1 workers in the exact industries where unauthorized are concentrated — Ag, Constr, Mfg, Food Service)
   110	- **Stable W-2 employment in exposed industries did fall** for E1 workers (~6%, marginal). This is qualitatively consistent with the Bohn-Lofstrom-Raphael Arizona result, but QWI cannot by itself distinguish true labor-supply contraction from cash-economy movement, hours changes, establishment composition, or worker reclassification.
   111	- **Together: QWI employment ↓ but wages flat = the large native wage-bidding channel is not observed in this design.** Candidate adjustment channels remain hypotheses, not measured mechanisms:
   112	  1. Capital substitution (mechanization in Ag, prefab in Constr)
   113	  2. Output reduction or relocation (firms exit; consumers face higher prices/lower service)
   114	  3. Cash economy / non-W-2 hiring (which doesn't show up in QWI)
   115	  4. Outsourcing across state lines
   116	  5. Hours, occupation, or establishment-composition shifts inside QWI cells
   117	
   118	For this enforcement margin, the adjustment looks Card-style: the wage curve is flatter than the large-Borjas-gain prediction, and observed E-Verify mandate variation shows no statistically significant rent transfer to native low-skill workers through higher QWI wages.
   119	
   120	### Power and caveats
   121	
   122	1. **Power.** With 9 treated states, 42 controls, and 21 years, the minimum detectable effect (MDE) at α=0.05 with 80% power is roughly ±2-3% for E1 in exposed industries given clustered SE. Borjas's predicted +5-15% would be detectable. **We can reject the Borjas magnitudes; we cannot reject small (sub-2%) positive effects.**
   123	
   124	2. **TWFE under heterogeneous treatment.** Sun-Abraham (2021), Goodman-Bacon (2021) caution: TWFE with staggered timing can be biased when effect sizes vary across cohorts. Robustness check should use Callaway-Sant'Anna or Sun-Abraham. Given the mostly-flat event-study coefficients here, I judge the bias is unlikely to flip the sign or magnitude meaningfully.
   125	
   126	3. **Treatment intensity heterogeneity.** AZ all-employer mandate (2008) is much tighter than UT 15+ employee (2010). A continuous "fraction of workers covered" treatment would sharpen the test. Doable as a follow-up.
   127	
   128	4. **Compliance is partial.** US E-Verify compliance ~50% even in mandate states (CIS 2017 estimate). The intent-to-treat estimate underweights actual treated workers. Adjust by 2× → MDE roughly 4-6%, still rejects high-end Borjas.
   129	
   130	5. **Unauthorized substitution to cash economy.** If displaced unauthorized workers stayed in the same labor market but moved to off-W-2 jobs (day labor, gig), QWI misses them. That possibility weakens any interpretation of the QWI E1 drop as a full labor-supply contraction; it does not rescue a large QWI-wage-gain prediction in this design.
   131	
   132	6. **External validity.** This is the policy variation we have. Results may not generalize to a hypothetical mass deportation, large refugee inflow, or border closure. It is one relevant test for marginal tightening of unauthorized labor supply via state enforcement mandates, not the policy debate as a whole.
   133	
   134	## What this updates in the existing repo
   135	
   136	### Confidence ladder
   137	- Move `Federal-positive vs federal-negative origin ranking from ACS income/benefit proxies` from `weak` → unchanged (this finding addresses wages, not federal fiscal)
   138	- Add new entry: **`Borjas substitution prediction for U.S. low-skill native wages from E-Verify policy variation`** — `strong against large Borjas-style gains in this E-Verify margin`. Point estimate ±1%, 95% CI excludes the high-end Borjas magnitudes.
   139	- Strengthen entry on `Claim that the Clark agree papers are scope-limited rather than obviously false` from `strong` → `strong+`. The small-native-wage-effect reading associated with those Clark responses is supported on this E-Verify margin.
   140	
   141	### Verified-findings report bottom line
   142	- The previous report said: "Some national output and consumer-price gains exist; some indirect federal fiscal offsets likely exist; but local schooling, housing, and service-capacity costs remain concentrated." [SOURCE: research/immigration-verified-findings-report-2026-04-10.md, finding #6]
   143	- This holds. **Add:** for the wage channel specifically, observed E-Verify policy variation in 2008-2023 supports the Card view. No statistically significant positive higher-QWI-wage effect is observed for native low-skill workers under these mandates; this rejects large Borjas-style gains in the observed mandate margin but does not directly measure the full wage effect of current low-skill immigration levels.
   144	
   145	### Adversarial review §1 ("we still don't have a full national welfare ledger")
   146	- This finding doesn't deliver a full national welfare ledger.
   147	- It narrows one open question: the labor-market wage channel for native low-skill workers under observed marginal enforcement variation. That contributes to the ledger from the credit side only within this policy range, not as a universal no-native-loss claim.
   148	
   149	### Updates to the smith-decker-friedman audit
   150	- David D. Friedman's open-borders argument relies in part on Card-style wage elasticity. This analysis supports that wage-channel premise for observed E-Verify variation, not the full open-borders conclusion.
   151	- Camarota's CIS-style native-wage-depression argument does not pass this E-Verify wage-channel test.
   152	- Smith and Decker's average-consumer-gains framing is consistent with this finding.
   153	
   154	## Comparison to literature
   155	
   156	| Study | Population | Design | Wage effect | Sign |
   157	|-------|-----------|--------|-------------|------|
   158	| Card (1990) | Mariel Boatlift, Miami | Synthetic control vs comparison cities | ~0% on Miami HS dropouts | Card |
   159	| Borjas (2017) | Mariel reanalysis, restricted to HS dropouts | Same data, narrower group | -10 to -30% | Borjas |
   160	| Bohn-Lofstrom-Raphael (2014) | AZ LAWA | Pop survey on unauth share | Unauth ↓; native effects mixed | Mixed |
   161	| Orrenius-Zavodny (2015) | E-Verify rollout | DiD on CPS earnings | Small positive on Hispanic native women only | Weak Borjas |
   162	| **This analysis** | **9 E-Verify states** | **TWFE on QWI 2003-2023** | **+0.5% (n.s.) E1 in exposed industries** | **Card** |
   163	| Foged-Peri (2016) | Denmark refugee-country inflow | Dispersal-policy IV / DiD | Native low-skill wages ↑ from refugee shock | Anti-Borjas |
   164	| Card-Peri (2016) | Cumulative immigration | National panel | Small / null on natives | Card |
   165	
   166	This analysis adds a 21-year multi-state version of the E-Verify test. Read with Card (1990) and Foged-Peri (2016), it supports the bounded claim that large native low-skill wage losses/gains are not observed in these designs; it does not identify one shared adjustment mechanism or rule out small effects.
   167	
   168	## Honest limits
   169	
   170	1. The wage-effect non-result is what I expected from prior literature. **Confirmation, not surprise.** This is not a novel finding — it extends the E-Verify policy-margin check with a longer QWI panel and broader treatment set, and is consistent with the Card-Peri wage literature. The contribution is updating the *repo's* confidence in the Card view from "the agree economists are scope-limited" to "their small-native-wage-effect premise is better supported for the policy variation we have."
   171	
   172	2. **What this does NOT settle:**
   173	   - Whether a mass-deportation shock would behave the same (unknown — different magnitudes and equilibria)
   174	   - Whether wage effects exist for sub-groups outside QWI's coverage (cash economy, very small firms exempt from mandate)
   175	   - Whether non-wage channels (employment composition, occupational sorting, hours) absorb the supply shock
   176	   - Whether the long-run (>10 year) effect differs from the medium-run captured here
   177	
   178	3. **Replication invitation.** Code: `sources/immigration-causal/scripts/analyze_everify_wages.py` and `analyze_everify_employment.py`. Data: `data/lehd/qwi_state_panel.parquet` (151k rows, 2 MB). Treatment panel: `data/everify/everify_state_mandates.csv`.
   179	
   180	## Revisions
   181	
   182	| Date | Change |
   183	|------|--------|
   184	| 2026-06-16 | Replaced "suggestive of mild complementarity loss" and "probably not" mass-shock shorthand with interpretation language that keeps nonsignificant coefficients and out-of-margin shocks unresolved. See `immigration-conclusion-audit-running-fixes.md`. |
   185	| 2026-06-16 | Rephrased the Card-side setup from "will produce" wage gains to prediction language, keeping theory expectations distinct from measured findings. See `immigration-conclusion-audit-running-fixes.md`. |
   186	| 2026-06-16 | Replaced speculative cash-economy substitution language with a narrower measurement caveat: off-W-2 substitution weakens E1 as a total labor-supply proxy, while leaving the QWI wage-gain result bounded to this design. See `immigration-conclusion-audit-running-fixes.md`. |
   187	| 2026-06-16 | Narrowed the external-validity caveat from "the relevant test for the actual policy debate" to one relevant test for marginal enforcement mandates. See `immigration-conclusion-audit-running-fixes.md`. |
   188	| 2026-06-16 | Replaced residual "do not move wages much" summary with bounded no-large-native-wage-loss/gain language and separated it from any shared mechanism claim. See `immigration-conclusion-audit-running-fixes.md`. |
   189	| 2026-06-16 | Replaced residual "does not measurably transfer rents" shorthand with no-statistically-significant higher-QWI-wage transfer language; small effects remain outside rejection. See `immigration-conclusion-audit-running-fixes.md`. |
   190	| 2026-06-16 | Scoped the title/question and bottom-line employment/wage shortcut to the observed QWI E-Verify wage-channel test rather than a broad Card-vs-Borjas verdict for U.S. data. See `immigration-conclusion-audit-running-fixes.md`. |
   191	| 2026-06-16 | Replaced "removing/restricting unauthorized labor" exports with observed E-Verify mandate variation and QWI wage language; the design does not directly observe total unauthorized labor supply. See `immigration-conclusion-audit-running-fixes.md`. |
   192	| 2026-06-16 | Narrowed the employment/wage mechanism interpretation: QWI shows stable W-2 employment fell while no statistically significant positive wage effect was observed, but it does not identify capital, output, relocation, cash-economy, hours, or composition adjustment mechanisms. See `immigration-conclusion-audit-running-fixes.md`. |
   193	| 2026-06-16 | Replaced "Clark economists were correct/right" language with support for the small-native-wage-effect premise in the observed E-Verify margin. See `immigration-conclusion-audit-running-fixes.md`. |
   194	| 2026-06-16 | Bounded "data side with Card" and commentator-update language to the observed E-Verify wage-channel design; the result rejects large Borjas-style native wage gains for this margin, not all wage or open-borders questions. See `immigration-conclusion-audit-running-fixes.md`. |
   195	| 2026-06-16 | Aligned the proposed confidence-ladder update with the same margin-specific wording: strong against large Borjas-style gains in the E-Verify margin, not a global "STRONG REJECTION." See `immigration-conclusion-audit-running-fixes.md`. |
   196	| 2026-06-16 | Clarified Foged-Peri design shorthand from opaque "RA quasi-IV" to dispersal-policy IV / DiD, matching the paper's quasi-experimental design. See `immigration-conclusion-audit-running-fixes.md`. |
   197	| 2026-06-16 | Replaced "replicates Orrenius-Zavodny and Card-Peri" with extension/consistency language; the QWI E-Verify panel is not a direct replication of those papers. See `immigration-conclusion-audit-running-fixes.md`. |
   198	
   199	[SOURCE: data/analysis/everify_twfe_results.csv]
   200	[SOURCE: data/analysis/everify_event_study_E1.csv]
   201	[SOURCE: data/analysis/everify_employment_twfe.csv]
   202	[SOURCE: scripts/analyze_everify_wages.py]
   203	[SOURCE: scripts/analyze_everify_employment.py]
   204	[SOURCE: scripts/pull_qwi_state_panel.py]
   205	
   206	<!-- knowledge-index
   207	generated: 2026-04-19T03:43:48Z
   208	hash: 224b29836cf0
   209	
   210	cross_refs: research/immigration-verified-findings-report-2026-04-10.md
   211	
   212	end-knowledge-index -->
--- END FILE: research/immigration-causal-everify-card-vs-borjas.md ---

--- BEGIN FILE: research/immigration-causal-synthesis-2026-04-18.md ---
     1	# Immigration causal analysis — synthesis (2026-04-18)
     2	
     3	**Inputs from this autonomous cycle:**
     4	1. `immigration-causal-saiz-elasticity-rent.md` — Saiz 2010 housing supply elasticity × ACS rent + foreign-born share, n=237 MSAs
     5	2. `immigration-causal-everify-card-vs-borjas.md` — TWFE on QWI 2003-2023, 9 E-Verify states vs 42 controls, 151k observations
     6	
     7	**Question revisited:** "On the immigration questions, can we find interpretations or datasets that would change the conclusions or something more descriptive and causal?"
     8	
     9	## Bottom line — what the new evidence updates
    10	
    11	| Repo claim (pre-cycle) | New evidence | Updated verdict |
    12	|------------------------|--------------|-----------------|
    13	| Rent exposure ≠ welfare loss (adversarial review §2) | Immigrants concentrate in inelastic MSAs (top FB-share quintile median elasticity 1.51 vs bottom 3.40); top 10 inelastic MSAs include all the major immigrant gateways | **Rent exposure is a stronger renter-incidence warning in inelastic destination markets** because supply response is weaker. Update: "rent exposure" should be tagged elasticity-conditional — higher incidence risk in inelastic destinations, lower in elastic. |
    14	| Clark "agree" economists are scope-limited but not wrong on their narrow channel | E-Verify mandates produced no statistically significant positive QWI wage effect for native low-skill workers in any of 12 specifications | **The small-native-wage-effect channel in the Clark "agree" position is better supported** in the observed E-Verify policy variation. Large Borjas-style native wage gains are rejected at α=0.05 for this margin. |
    15	| "Borjas vs Card" presented as live debate | Direct multi-state TWFE with 21-year panel finds Card-side pattern: no statistically significant positive QWI wage effect after E-Verify mandate variation | **For observed marginal enforcement variation, the Card-side pattern is favored.** Borjas's restricted-Mariel magnitude should not be mechanically extrapolated to the broader staggered enforcement shocks tested here; this does not settle surge or mass-shock regimes. |
    16	| Federal-positive / local-negative split is plausible but unquantified | This cycle did not produce federal-side estimates (federal microsim still requires SIPP fix) | **Unchanged.** Federal side remains the weakest part of the repo. |
    17	| Local-burden story is real but heterogeneous | Saiz merge sharpens the housing component; QWI shows no statistically significant positive wage response in the observed E-Verify margin, with large Borjas-style gains rejected | **Strengthened on the housing side, not on schooling.** School-burden findings are unchanged by this cycle. |
    18	
    19	## E-Verify wage-channel verdict
    20	
    21	Three converging pieces of evidence on the U.S. wage channel:
    22	
    23	1. **Card (1990) Mariel:** no detected adverse wage effect on Miami high-school dropouts in that design.
    24	2. **This cycle's E-Verify TWFE:** +0.5% (n.s.) wage effect on E1 workers in exposed industries across 9 mandate states 2003-2023.
    25	3. **Foged-Peri (2016) Denmark:** native low-skill wages *rose* in a refugee dispersal-policy quasi-experiment.
    26	
    27	Against:
    28	- **Borjas (2017) Mariel reanalysis:** -10 to -30% on HS dropouts with restricted sample. **This magnitude should not be mechanically extrapolated to the broader staggered designs tested here.**
    29	
    30	**Verdict:** For the observed marginal U.S. policy variation in this file, large Borjas-style native wage gains from E-Verify-style labor-supply contraction are rejected at conventional significance levels. The remaining uncertainty is about surge regimes and hypothetical extreme shocks (mass deportation, border closure) that have no direct empirical analog. **The Clark Center "agree" small-native-wage-effect premise is supported for the narrow wage channel and observed-policy range, not for the all-in immigration question.**
    31	
    32	This is a meaningful update to the repo's prior position. The verified-findings report (2026-04-10) said the Clark agree economists were "mostly right on a narrow question" but bracketed this carefully. The new evidence justifies elevating only the wage-channel premise: **small native wage effects are better supported within observed marginal policy variation.**
    33	
    34	## Incidence — federal vs local — what this cycle changes
    35	
    36	The Saiz finding sharpens the **local** side:
    37	- Renter-incidence risk is structurally larger than the adversarial review allowed. In inelastic markets (where >40% of immigrants live), weaker supply response makes rent exposure more decision-relevant, but immigrant-specific rent causation still needs panel/IV identification.
    38	- Owner-gain-to-renter-loss ratio differs by destination elasticity. The repo's existing PUMA rent table can be re-tagged elasticity-conditional once the SSD is remounted.
    39	
    40	The E-Verify finding clarifies the **labor-market** side:
    41	- No statistically significant positive QWI wage effect is observed for native low-skill workers under observed E-Verify mandate variation.
    42	- The evidence rejects large Borjas-style native wage gains from marginal enforcement, but does not directly measure the full wage effect of current inflow levels or surge regimes.
    43	- Therefore the observed marginal-enforcement wage component shows no statistically significant positive QWI wage effect for natives, with large Borjas-style gains rejected in this design; the broader labor-market ledger still includes small effects, employment composition, hours, occupational sorting, and unmeasured shock regimes.
    44	- In this cycle's observed E-Verify wage margin, wage compression is not the supported local-burden channel; school-finance, housing-rent, and service capacity remain separate live channels. Surge/current-inflow wage compression remains unmeasured here.
    45	
    46	Combined effect on incidence narrative:
    47	- Pre-cycle: native low-skill workers maybe lose wages (Borjas), bear school burden, face rent competition.
    48	- Post-cycle: the E-Verify-style enforcement design shows no statistically significant positive native low-skill QWI wage effect and rejects large Borjas-style gains in that margin; school burden and housing incidence remain separate local channels.
    49	
    50	The political-economy reading: wage data alone are a weak justification for a native-low-skill restriction story in the observed marginal-enforcement range. School-finance exposure and renter exposure remain plausible incidence channels, but this cycle does not identify voter motivation or prove that those exposures justify the policy push; owner/renter status, local fiscal regime, and service geography still matter.
    51	
    52	## What this cycle did NOT settle
    53	
    54	1. **Federal microsimulation.** SIPP donor library is still broken (HHINC handled wrong). Same blocker as 2026-04-10. Not addressed this cycle.
    55	2. **Causal IV for housing.** Saiz finding is descriptive cross-section. Card shift-share IV would be cleaner. Requires warehouse remount.
    56	3. **DACA pre-post analysis.** Timeline + design coded but no execution this cycle (required ACS PUMS pull deferred for disk space).
    57	4. **Spatial wage compression test.** State-level analysis may miss within-state heterogeneity. County-level QWI extension is feasible (data is there).
    58	5. **Mass deportation counterfactual.** No data analog. The claim "tightening immigration won't help native workers" is supported for marginal enforcement, not for mass shocks.
    59	6. **Indirect federal fiscal effects.** Colas-Sachs (2024) argument that low-skill immigration has positive indirect federal effects via consumer demand → tax base is not tested here.
    60	
    61	## Reframing the original question
    62	
    63	The user asked which interpretations or datasets could change conclusions. After this cycle:
    64	
    65	- **Borjas vs Card debate:** Bounded to observed marginal U.S. policy variation. Card-side pattern there; surge and mass-shock regimes remain open.
    66	- **Rent burden as renter-incidence risk:** Narrowed, not resolved. In inelastic destination markets it is a stronger renter-incidence warning; owner/renter incidence and causal identification caveats still apply.
    67	- **Federal-positive / local-negative split:** Sharpened on local side, unchanged on federal side.
    68	- **Race-stratified crime gap:** From earlier work — gap narrows from 50% to 30% but immigrants still lower than natives.
    69	- **Place-premium / immigrant welfare weighting:** Untested this cycle. Remains the biggest single lever for flipping the verdict.
    70	- **AGI-soon timing:** Untested empirically. Remains the biggest framing lever.
    71	
    72	## Updated confidence ladder (additions)
    73	
    74	Add to `immigration-confidence-ladder.md`:
    75	
    76	```
    77	17. `Borjas wage prediction for U.S. native low-skill workers from E-Verify`
    78	Rating: strong against large Borjas-style gains in the E-Verify margin
    79	Reason: TWFE on QWI 2003-2023 with 9 treated states finds +0.5% (n.s.) on E1 in
    80	exposed industries. 95% CI excludes large Borjas magnitudes in this observed
    81	mandate design. Surge and mass-shock regimes remain outside this result.
    82	[SOURCE: research/immigration-causal-everify-card-vs-borjas.md]
    83	
    84	18. `Immigrants concentrate in inelastic-supply MSAs`
    85	Rating: STRONG (descriptive)
    86	Reason: top FB-share quintile median Saiz elasticity 1.51, bottom 3.40. n=237 MSAs.
    87	Implication: rent exposure in inelastic destination markets is a stronger renter-incidence warning than the adversarial review allowed.
    88	[SOURCE: research/immigration-causal-saiz-elasticity-rent.md]
    89	
    90	19. `Card-side bounded native-wage-impact evidence for observed low-skill shocks`
    91	Rating: MEDIUM-STRONG
    92	Reason: convergent evidence from (a) Card 1990 Mariel, (b) this cycle's E-Verify
    93	TWFE, and (c) Foged-Peri 2016 Denmark points against large native low-skill wage
    94	losses/gains in these designs; it does not identify one shared complementarity
    95	mechanism. Borjas 2017 restricted-Mariel magnitude should not be mechanically
    96	extrapolated to the broader designs cited here.
    97	[SOURCE: research/immigration-causal-everify-card-vs-borjas.md, multiple papers]
    98	```
    99	
   100	## What to do next
   101	
   102	In priority order, given evidence value:
   103	
   104	1. **Mount the SSD and rerun the Saiz×PUMA merge with the existing warehouse**, using `origin_puma_household_context_2023` × Saiz elasticity by MSA-PUMA crosswalk. This produces an *origin-conditional* renter-incidence screen, not a final welfare estimate. ~1 day with warehouse access.
   105	
   106	2. **Fix the SIPP donor library.** This is the same call from 2026-04-10. The federal microsim remains the biggest gap. Highest-leverage single fix on the repo.
   107	
   108	3. **County-level QWI extension** for E-Verify analysis, focused on border/non-border counties within mandate states. This would address the within-state heterogeneity caveat. Disk-cheap (similar to current pull).
   109	
   110	4. **Card shift-share IV for housing.** Use 1990 origin-share × current national flow as instrument for current immigrant share by MSA. Rerun rent regressions with IV. Removes the cross-sectional endogeneity caveat. Requires warehouse remount.
   111	
   112	5. **DACA pre-post on PUMS.** Implement the design already coded in `daca_timeline_and_design.md`. Tests labor-market spillovers from a clean shock. Requires ~2 GB ACS PUMS pull (defer until disk free or SSD).
   113	
   114	6. **Continue chasing Foged-Peri analog in U.S. data.** Look for refugee resettlement quasi-random assignment (HUD voucher rollout, ORR placement quotas).
   115	
   116	## Honest reflection
   117	
   118	This cycle did what it set out to do: produced two original empirical findings using fresh datasets, both pointing in the Card direction. The findings are not novel relative to academic literature — they are consistent with well-known patterns rather than direct replications of those papers. The contribution is internal to this repo: **the prior epistemic posture ("Clark agree economists are scope-limited, but not false on the wage channel") understated the strength of the Card-side wage evidence**. The marginal-enforcement wage channel is bounded for the policy variation we have; surge and mass-shock regimes remain open.
   119	
   120	The federal-fiscal side is still open. The political-economy and rent-exposure sides got sharper. The crime-rate side was already strong (separate memo earlier).
   121	
   122	The *biggest* unresolved interpretation lever — Clemens place-premium, weighting immigrant welfare — remains untouched by this cycle. The welfare weight is a values choice; the place-premium, native-cost, fiscal, housing/capacity, and sending-country inputs are empirical and can still move the scenario break-evens.
   123	
   124	[SOURCE: research/immigration-causal-saiz-elasticity-rent.md]
   125	[SOURCE: research/immigration-causal-everify-card-vs-borjas.md]
   126	[SOURCE: research/immigration-verified-findings-report-2026-04-10.md]
   127	[SOURCE: research/immigration-confidence-ladder.md]
   128	[SOURCE: research/immigration-adversarial-review.md]
   129	
   130	## Revisions
   131	
   132	| Date | Change |
   133	|------|--------|
   134	| 2026-06-16 | Replaced the "NOT wage compression" burden shortcut with margin-specific language: E-Verify QWI does not support wage compression in that design, but surge/current-inflow wage compression remains unmeasured. See `immigration-conclusion-audit-running-fixes.md`. |
   135	| 2026-06-16 | Replaced residual hard non-generalization wording for Borjas restricted-Mariel with a narrower no-mechanical-extrapolation claim. See `immigration-conclusion-audit-running-fixes.md`. |
   136	| 2026-06-16 | Replaced Card/Mariel "zero wage effect" and "Card-style complementarity" shorthand with no-detected-adverse-effect and bounded-native-wage-impact language. See `immigration-conclusion-audit-running-fixes.md`. |
   137	| 2026-06-16 | Replaced residual "small/null" wage-response shorthand with no-statistically-significant-positive-QWI-wage-effect language; large gains are rejected but small effects are not. See `immigration-conclusion-audit-running-fixes.md`. |
   138	| 2026-06-16 | Replaced remaining incidence-summary shortcuts saying native wages "do not rise" / "do not measurably rise" with no-statistically-significant-positive-QWI-wage-effect language. See `immigration-conclusion-audit-running-fixes.md`. |
   139	| 2026-06-16 | Scoped the Card-vs-Borjas section heading to the E-Verify wage-channel verdict rather than a broad theory verdict. See `immigration-conclusion-audit-running-fixes.md`. |
   140	| 2026-06-16 | Replaced "E-Verify contracts unauthorized labor supply" synthesis exports with observed mandate-variation/QWI wage language; total unauthorized labor supply is not directly observed. See `immigration-conclusion-audit-running-fixes.md`. |
   141	| 2026-06-16 | Replaced "Clark economists were right/correct" exports with support for the small-native-wage-effect premise within observed marginal policy variation. See `immigration-conclusion-audit-running-fixes.md`. |
   142	| 2026-06-16 | Replaced residual "Card-side pattern wins" wording with "is favored" to avoid treating a bounded design comparison as debate closure. See `immigration-conclusion-audit-running-fixes.md`. |
   143	| 2026-06-16 | Bounded the political-economy reading: wage evidence alone weakens the native-low-skill wage story, but school/rent exposure is only a plausible incidence channel, not identified voter motivation or policy justification. See `immigration-conclusion-audit-running-fixes.md`. |
   144	| 2026-06-16 | Narrowed the embedded E-Verify confidence-ladder suggestion from global `STRONG REJECTION` to strong evidence against large Borjas-style gains in the E-Verify margin. See `immigration-conclusion-audit-running-fixes.md`. |
   145	| 2026-06-16 | Replaced "QWI confirms wage channel is small" with margin-specific no-statistically-significant-positive-wage-effect language for the observed E-Verify design. See `immigration-conclusion-audit-running-fixes.md`. |
   146	| 2026-06-16 | Narrowed the explicit Card-vs-Borjas verdict sentence to large Borjas-style gains from E-Verify-style labor-supply contraction, not the full Borjas wage-prediction family. See `immigration-conclusion-audit-running-fixes.md`. |
   147	| 2026-06-16 | Replaced direct-replication language with external-validity language because E-Verify/Foged-Peri are adjacent tests, not direct Mariel replications; later narrowed to no-mechanical-extrapolation wording. See `immigration-conclusion-audit-running-fixes.md`. |
   148	| 2026-06-16 | Replaced "random refugee assignment" with "refugee dispersal-policy quasi-experiment"; Foged-Peri is exogenous/quasi-experimental, not a simple randomized trial. See `immigration-conclusion-audit-running-fixes.md`. |
   149	| 2026-06-16 | Removed remaining "replicates well-known patterns" language; this cycle's findings are convergent/consistent evidence, not direct replications of Card, Foged-Peri, or Card-Peri. See `immigration-conclusion-audit-running-fixes.md`. |
   150	| 2026-06-16 | Reframed the Clemens/welfare-weight lever: the weight is normative, but place-premium and cost/capacity inputs remain empirical. See `immigration-conclusion-audit-running-fixes.md`. |
   151	| 2026-06-16 | Changed residual Saiz ladder implication from "closer to welfare loss" to a stronger renter-incidence warning in inelastic destination markets. See `immigration-conclusion-audit-running-fixes.md`. |
   152	
   153	<!-- knowledge-index
   154	generated: 2026-04-19T03:45:13Z
   155	hash: 09b8c2f5eb8f
   156	
   157	cross_refs: research/immigration-adversarial-review.md, research/immigration-causal-everify-card-vs-borjas.md, research/immigration-causal-saiz-elasticity-rent.md, research/immigration-confidence-ladder.md, research/immigration-verified-findings-report-2026-04-10.md
   158	table_claims: 5
   159	
   160	end-knowledge-index -->
--- END FILE: research/immigration-causal-synthesis-2026-04-18.md ---

--- BEGIN FILE: research/immigration-bryan-caplan-claims-audit-2026-04-21.md ---
     1	# Bryan Caplan immigration claims audit — 2026-04-21
     2	
     3	## Scope
     4	
     5	This memo audits Bryan Caplan's main immigration claims against:
     6	
     7	1. his own primary texts
     8	2. official recent U.S. sources
     9	3. the repo's current surge, threshold, crime, and county-outcome work
    10	
    11	This is a claim audit, not a general evaluation of Caplan as a thinker.
    12	
    13	**Instrument caveat:** immigration is a politically charged topic and the LLM instrument has known bias risk here. This memo leans on primary texts, official sources, and repo-built data artifacts rather than training-data impressions. [SOURCE: `notes/llm-bias-caveat.md`]
    14	
    15	## Primary texts audited
    16	
    17	1. [Why Should We Restrict Immigration?](https://www.cato.org/sites/cato.org/files/serials/files/cato-journal/2012/1/cj32n1-2.pdf) [SOURCE: https://www.cato.org/sites/cato.org/files/serials/files/cato-journal/2012/1/cj32n1-2.pdf]
    18	2. [Why Should We Restrict Immigration?](https://www.econlib.org/archives/2012/01/why_should_we_r.html) [SOURCE: https://www.econlib.org/archives/2012/01/why_should_we_r.html]
    19	3. [The Social and Political Realities of Immigration: A Reply to Hoste](https://www.econlib.org/archives/2010/04/the_social_and.html) [SOURCE: https://www.econlib.org/archives/2010/04/the_social_and.html]
    20	4. [Immigration and the Welfare State](https://www.econlib.org/archives/2011/06/immigration_and_2.html) [SOURCE: https://www.econlib.org/archives/2011/06/immigration_and_2.html]
    21	5. [Does Immigration Shrink the Welfare State?](https://www.econlib.org/does-immigration-shrink-the-welfare-state/) [SOURCE: https://www.econlib.org/does-immigration-shrink-the-welfare-state/]
    22	6. [Assimilation and Immigration Restriction](https://www.econlib.org/archives/2015/12/krikorian_again.html) [SOURCE: https://www.econlib.org/archives/2015/12/krikorian_again.html]
    23	7. [Let Anyone Take a Job Anywhere](https://www.econlib.org/archives/2013/11/let_anyone_take.html) [SOURCE: https://www.econlib.org/archives/2013/11/let_anyone_take.html]
    24	
    25	## Bottom line
    26	
    27	Caplan is strongest where the current repo already agrees with the classic open-borders literature:
    28	
    29	1. the `migrant-welfare` and `global-output` case for much freer movement is real [SOURCE: https://www.aeaweb.org/articles?id=10.1257/jep.25.3.83] [SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md]
    30	2. the U.S. observed-criminal-justice-rate objection to first-generation and unauthorized immigrants is weaker than restrictionists usually claim [SOURCE: research/immigration-crime-rates-unauthorized-vs-native-born.md]
    31	3. broad `employment-collapse` rhetoric is too strong [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md]
    32	
    33	Caplan is weakest where recent surge and threshold evidence make local incidence unsafe to wave away:
    34	
    35	1. the claim that immigration restrictions are not needed to protect `taxpayers` is too broad once the `federal` and `state/local` ledgers are separated [SOURCE: https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf] [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
    36	2. the claim that immigration restrictions are not needed to protect `workers` is too broad once housing/permit constraints and low-education wage exposure are added [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md] [SOURCE: https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf]
    37	3. the claim that political externalities are manageable by default is not established under surge conditions and capacity thresholds [SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md] [SOURCE: research/immigration-causal-surge-2021-2024.md]
    38	
    39	The clean verdict is:
    40	
    41	1. `strong on migrant-welfare / global-gains direction, not strongest magnitude`
    42	2. `strong on observed U.S. justice-system-rate skepticism`
    43	3. `partial on labor`
    44	4. `weak on destination-local fiscal and political incidence`
    45	
    46	## Executive table
    47	
    48	| Claim | Verdict | Why |
    49	|---|---|---|
    50	| `There is a moral presumption in favor of free migration.` | `Coherent normative starting point, not an empirical result` | Caplan is entitled to this only on a libertarian moral frame; it does not answer native-local welfare by itself. [SOURCE: https://www.cato.org/sites/cato.org/files/serials/files/cato-journal/2012/1/cj32n1-2.pdf] [FRAMING-SENSITIVE] |
    51	| `The economic case for much freer migration is extremely strong.` | `Mostly survives in direction, not in strongest magnitude` | Large global gains survive; realistic `double world GDP` style readings do not. [SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md] |
    52	| `Immigration restrictions are not necessary to protect American workers.` | `Too broad` | Broad job-loss stories are weak, but constrained counties show slower wage growth and official projections show slight low-education wage-growth pressure. [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md] [SOURCE: https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf] |
    53	| `Immigration restrictions are not necessary to protect American taxpayers.` | `Fails as a blanket claim` | Federal gains can coexist with state/local costs in education, shelter, and related services. [SOURCE: https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf] [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf] |
    54	| `Immigrants commit much less crime than natives.` | `Mostly survives for observed U.S. first-generation / unauthorized justice-system rates` | The U.S. evidence is strong for lower observed arrest, conviction, and incarceration rates, though some headline gaps are overstated by compositional comparisons and the international generalization is weaker. True offending is less directly identified. [SOURCE: research/immigration-crime-rates-unauthorized-vs-native-born.md] |
    55	| `Immigration restrictions are not necessary to protect American culture.` | `Partly survives, but culture is not the best-developed bottleneck in this evidence surface` | Apocalyptic culture-collapse arguments are weak; assimilation is real. But the repo's current U.S. stress evidence is better developed for housing, services, and politics than for a clean culture mechanism. [SOURCE: https://www.econlib.org/archives/2015/12/krikorian_again.html] [SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md] |
    56	| `Political externalities are limited because immigrants vote less, accept the status quo, and may restrain redistribution.` | `Partly survives in a narrow median-voter sense, fails as a full political-incidence answer` | National voting mechanics are only one channel; local overload, legitimacy effects, and possible citizen political response remain live. [SOURCE: https://www.econlib.org/archives/2010/04/the_social_and.html] [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md] [SOURCE: research/full-spectrum-costs-unauthorized-immigration-research-memo.md] |
    57	| `Cheaper and more humane alternatives exist for each complaint.` | `Partly survives as institutional design logic, not as practical closure` | Keyhole solutions mitigate some objections, but do not dissolve housing, school, shelter, and credibility problems. [SOURCE: https://www.cato.org/sites/cato.org/files/serials/files/cato-journal/2012/1/cj32n1-2.pdf] [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md] [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf] |
    58	
    59	## Claim 1: `There is a moral presumption in favor of free migration`
    60	
    61	This is the foundation of Caplan's case. In the Cato piece and Econlib summary, he argues that voluntary exchange between natives and foreigners looks morally permissible on its face, so restriction needs a real excuse. [SOURCE: https://www.cato.org/sites/cato.org/files/serials/files/cato-journal/2012/1/cj32n1-2.pdf] [SOURCE: https://www.econlib.org/archives/2012/01/why_should_we_r.html]
    62	
    63	What survives:
    64	
    65	1. As a libertarian moral premise, this is internally coherent. [SOURCE: https://www.cato.org/sites/cato.org/files/serials/files/cato-journal/2012/1/cj32n1-2.pdf]
    66	2. It correctly forces empirical objectors to specify what harm they are actually invoking. [INFERENCE]
    67	
    68	What does not follow:
    69	
    70	1. A moral presumption is not a fiscal estimate. [FRAMING-SENSITIVE]
    71	2. A rights-based starting point does not settle `who bears transition costs` in public systems with local externalities. [FRAMING-SENSITIVE]
    72	
    73	Verdict:
    74	
    75	1. `survives as a normative premise`
    76	2. `cannot be verified or falsified by the county or CBO evidence alone`
    77	
    78	## Claim 2: `The economic case for much freer migration is extremely strong`
    79	
    80	Caplan's strongest empirical lane is that migration creates very large gains because labor is far more productive in high-productivity places. He is in the Clemens / place-premium tradition here. [SOURCE: https://www.cato.org/sites/cato.org/files/serials/files/cato-journal/2012/1/cj32n1-2.pdf] [SOURCE: https://www.aeaweb.org/articles?id=10.1257/jep.25.3.83]
    81	
    82	What survives:
    83	
    84	1. The direction of the global-gains claim survives. [SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md]
    85	2. The repo's own bounded calibration still finds large gains under substantial movement, just far below the strongest slogans. [SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md]
    86	3. Many anti-immigration arguments ignore the scale of migrant place-premium gains. [SOURCE: https://www.aeaweb.org/articles?id=10.1257/jep.25.3.83]
    87	
    88	What fails:
    89	
    90	1. The strongest open-borders headline versions are not realistic central forecasts once realistic migration volume, housing, congestion, and political constraints are added. [SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md]
    91	2. Official U.S. macro projections already show the key incidence split: aggregate GDP can rise while real GDP per person falls slightly. [SOURCE: https://www.cbo.gov/system/files/2024-02/59710-Outlook-2024.pdf]
    92	
    93	Verdict:
    94	
    95	1. `direction/sign survives`
    96	2. `not entitled to the strongest magnitude or destination-local gloss`
    97	
    98	## Claim 3: `Immigration restrictions are not necessary to protect American workers`
    99	
   100	Caplan repeatedly argues that most Americans gain, while the losers do not lose much, and that even worker losses could be handled more humanely than by exclusion. [SOURCE: https://www.econlib.org/archives/2012/01/why_should_we_r.html] [SOURCE: https://www.econlib.org/archives/2013/11/let_anyone_take.html]
   101	
   102	What survives:
   103	
   104	1. The repo's current county panel does **not** show a broad employment-collapse story. [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md]
   105	2. The evidence supports Caplan's objection to the crudest version of `immigration destroys jobs`. [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md]
   106	
   107	What cuts against him:
   108	
   109	1. In counties with very high recent immigration and low permit throughput, `2021–2024` weekly wage growth is about `1.5 pp` lower. [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md]
   110	2. CBO projects that through `2026`, wage growth for non-surge workers with `12 or fewer years of education` is slightly lower than in the no-surge counterfactual. [SOURCE: https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf]
   111	3. In the repo's current worker-incidence evidence surface, the better-developed concern is not broad `job destruction`; it is slower wage progression in constrained places. [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md] [INFERENCE]
   112	
   113	Verdict:
   114	
   115	1. `collapse rhetoric is unsupported by the current county panel`
   116	2. `Caplan is too broad when he compresses worker protection into near-triviality`
   117	
   118	## Claim 4: `Immigration restrictions are not necessary to protect American taxpayers`
   119	
   120	This is one of Caplan's weakest major claims in current U.S. conditions. He argues the fiscal effects are small and that researchers disagree on sign but agree on modest magnitude. [SOURCE: https://www.econlib.org/archives/2012/01/why_should_we_r.html]
   121	
   122	That formulation no longer survives cleanly once the fiscal ledger is split.
   123	
   124	What survives:
   125	
   126	1. The `federal` ledger can indeed be positive. CBO estimates the recent surge lowers federal deficits by about `$897B` over `2024–2034`. [SOURCE: https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf]
   127	2. Caplan's criticism is supported where restrictionists blur national and local fiscal ledgers. [INFERENCE]
   128	
   129	What fails:
   130	
   131	1. The `state/local` ledger for the recent surge is clearly negative in the official CBO accounting. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
   132	2. The large cost buckets are `education`, `shelter and related services`, and `border security`, not just cash welfare. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
   133	3. The repo's current position already treats local school, shelter, housing, and service load as first-order channels rather than rhetorical appendices. [SOURCE: research/immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md] [SOURCE: research/full-spectrum-costs-unauthorized-immigration-research-memo.md]
   134	
   135	Verdict:
   136	
   137	1. `fails as a blanket taxpayer claim`
   138	2. `can be rescued only by explicitly separating federal from state/local incidence`
   139	
   140	## Claim 5: `Immigrants commit much less crime than natives`
   141	
   142	Caplan has long treated the crime objection as empirically weak. On current U.S. observed justice-system-rate evidence, this is one of his strongest empirical claims. [SOURCE: https://www.econlib.org/archives/2010/04/the_social_and.html]
   143	
   144	What survives:
   145	
   146	1. The repo's crime memo finds the weight of U.S. evidence supports lower observed first-generation and unauthorized arrest, conviction, or incarceration rates than native-born rates. [SOURCE: research/immigration-crime-rates-unauthorized-vs-native-born.md]
   147	2. The Texas administrative-data line remains one of the strongest direct sources. [SOURCE: research/immigration-crime-rates-unauthorized-vs-native-born.md]
   148	
   149	Important caveats:
   150	
   151	1. Some headline gaps are overstated when comparing unauthorized immigrants to all native-born citizens rather than better-matched subgroups. [SOURCE: research/immigration-crime-rates-unauthorized-vs-native-born.md]
   152	2. This is strongest for observed current U.S. first-generation / unauthorized justice-system rates, not a universal all-country or true-offending rule. [SOURCE: research/immigration-crime-rates-unauthorized-vs-native-born.md]
   153	
   154	Verdict:
   155	
   156	1. `mostly survives`
   157	2. `Caplan is on strong ground here, with compositional caveats`
   158	
   159	## Claim 6: `Immigration restrictions are not necessary to protect American culture`
   160	
   161	Caplan often treats the cultural objection as weak: immigrants assimilate, their children learn English, and fears of permanent civilizational non-assimilation are overstated. [SOURCE: https://www.econlib.org/archives/2012/01/why_should_we_r.html] [SOURCE: https://www.econlib.org/archives/2015/12/krikorian_again.html]
   162	
   163	What survives:
   164	
   165	1. The hardest-line permanent non-assimilation claim is too strong. [SOURCE: https://www.econlib.org/archives/2015/12/krikorian_again.html]
   166	2. The repo's current evidence surface is better developed for `housing`, `services`, `shelter`, and `politics` than for `culture` as the first binding destination-country channel. That is not proof that culture is never first-binding. [SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md] [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md] [INFERENCE]
   167	
   168	What remains open:
   169	
   170	1. Trust, solidarity, and political-response channels are not zero merely because assimilation exists. [SOURCE: research/full-spectrum-costs-unauthorized-immigration-research-memo.md]
   171	2. Caplan's welfare-state and trust optimism is partly a political-economy claim, not just a culture claim. [SOURCE: https://www.econlib.org/archives/2011/06/immigration_and_2.html] [SOURCE: https://www.econlib.org/does-immigration-shrink-the-welfare-state/]
   172	
   173	Verdict:
   174	
   175	1. `partly survives`
   176	2. `culture collapse is not the clean modern objection`
   177	3. `but culture/trust cannot simply be dismissed as solved`
   178	
   179	## Claim 7: `Political externalities are limited`
   180	
   181	Caplan's standard package here is:
   182	
   183	1. immigrants vote less than natives [SOURCE: https://www.econlib.org/archives/2010/04/the_social_and.html]
   184	2. they accept the status quo by default [SOURCE: https://www.econlib.org/archives/2010/04/the_social_and.html]
   185	3. diversity may reduce support for redistribution [SOURCE: https://www.econlib.org/archives/2011/06/immigration_and_2.html] [SOURCE: https://www.econlib.org/does-immigration-shrink-the-welfare-state/]
   186	
   187	What survives:
   188	
   189	1. In a narrow `median-voter today` sense, lower turnout and slower political incorporation do damp one channel of political effect. [SOURCE: https://www.econlib.org/archives/2010/04/the_social_and.html]
   190	2. It is plausible that some immigration can weaken solidaristic support for redistribution. Caplan himself later acknowledges that the effect is moderate and mostly about slower growth rather than actual shrinkage of the welfare state. [SOURCE: https://www.econlib.org/does-immigration-shrink-the-welfare-state/]
   191	
   192	What fails:
   193	
   194	1. The relevant political channel is not only immigrant voting. It also includes possible citizen response, local overload, policy churn, and perceived unfairness. [SOURCE: research/full-spectrum-costs-unauthorized-immigration-research-memo.md]
   195	2. The repo's threshold and county-outcome analyses report stronger political-response association signals in high-immigration constrained places, especially where permit capacity is weak and rent burden high. The mechanism is not yet cleanly separated into persuasion, turnout, sorting, Hispanic realignment, or busing-target endogeneity. [SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md] [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md]
   196	3. The surge memo already treats the `2021–2024` period as a different regime from the older low-intensity local-labor literature. [SOURCE: research/immigration-causal-surge-2021-2024.md]
   197	
   198	Verdict:
   199	
   200	1. `welfare-state-voting channel is partly supported`
   201	2. `incomplete as a full political-incidence answer`
   202	
   203	## Claim 8: `Cheaper and more humane alternatives exist for each complaint`
   204	
   205	Caplan's keyhole-solution instinct is real and important. He argues that if immigrants burden workers, taxpayers, or politics, there are less coercive solutions than exclusion: entry fees, higher immigrant taxes, welfare exclusion, delayed voting, and related conditions. [SOURCE: https://www.econlib.org/archives/2012/01/why_should_we_r.html] [SOURCE: https://www.cato.org/sites/cato.org/files/serials/files/cato-journal/2012/1/cj32n1-2.pdf]
   206	
   207	What survives:
   208	
   209	1. As a design principle, this is stronger than generic `just trust immigration` rhetoric. [INFERENCE]
   210	2. Some objections really are more tractable through institutional design than through outright exclusion. [SOURCE: research/immigration-david-d-friedman-claims-audit-2026-04-11.md]
   211	
   212	What fails:
   213	
   214	1. These fixes do not neutralize `housing throughput`, `school crowding`, `shelter stock`, or `local assignment regime`. [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md] [SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md]
   215	2. They also rely on credibility and state capacity. A keyhole solution that is politically impossible or institutionally non-credible is not a full answer. Caplan himself acknowledges that open borders is `far out of sample` and that worst-case scenarios cannot be ruled out with confidence. [SOURCE: https://www.cato.org/sites/cato.org/files/serials/files/cato-journal/2012/1/cj32n1-2.pdf]
   216	
   217	Verdict:
   218	
   219	1. `good institutional imagination`
   220	2. `not enough to close the empirical case`
   221	
   222	## Causal graph
   223	
   224	The cleanest way to see where Caplan's case is supported and where it is too optimistic is to write the omitted edges explicitly.
   225	
   226	### Baseline DAG
   227	
   228	`migration liberalization`
   229	-> `inflow volume and composition`
   230	-> `migrant earnings gains`
   231	-> `global output gains`
   232	
   233	`migration liberalization`
   234	-> `inflow volume and composition`
   235	-> `destination labor supply`
   236	-> `employer surplus / consumer surplus`
   237	-> `national GDP gains`
   238	
   239	`migration liberalization`
   240	-> `inflow volume and composition`
   241	-> `housing demand`
   242	-> `rent burden / crowding`
   243	-> `native sorting / political response`
   244	
   245	`migration liberalization`
   246	-> `inflow volume and composition`
   247	-> `school / shelter / service load`
   248	-> `state-local fiscal costs`
   249	-> `political response / legitimacy costs`
   250	
   251	`migration liberalization`
   252	-> `inflow volume and composition`
   253	-> `labor-market competition under local capacity constraints`
   254	-> `slower wage growth for exposed groups`
   255	
   256	`migration liberalization`
   257	-> `inflow volume and composition`
   258	-> `crime composition`
   259	-> `public-safety concern`
   260	
   261	### Main moderators
   262	
   263	The current repo says the current load-bearing moderators are:
   264	
   265	1. `permit throughput / housing-supply response` [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md]
   266	2. `baseline rent burden / affordability` [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md]
   267	3. `shelter inventory and legal regime` [SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md]
   268	4. `pace and concentration of inflow` [SOURCE: research/immigration-causal-surge-2021-2024.md]
   269	5. `skill/origin/family composition` [SOURCE: research/immigration-low-skill-origin-incidence-memo.md]
   270	
   271	### Where Caplan is strongest
   272	
   273	Caplan's model is strongest on the left side of the DAG:
   274	
   275	1. `migrant earnings gains`
   276	2. `global output gains`
   277	3. `observed U.S. justice-system-rate skepticism`
   278	
   279	These are real and durable parts of the case at that scope. [SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md] [SOURCE: research/immigration-crime-rates-unauthorized-vs-native-born.md]
   280	
   281	### Where Caplan is weakest
   282	
   283	Caplan is weakest where omitted or downweighted right-side edges become first-order:
   284	
   285	1. `housing demand -> rent burden -> native sorting / political response`
   286	2. `school / shelter / service load -> state-local costs`
   287	3. `capacity-constrained labor absorption -> slower wage growth`
   288	4. `citizen political response and legitimacy effects`, which do not require immigrant voting to matter
   289	
   290	That is the core causal disagreement between Caplan's optimistic package and the repo's current evidence. [INFERENCE]
   291	
   292	## Net verdict
   293	
   294	If the question is `Does Caplan's case that freer migration can create huge gains and that many standard restrictionist objections are overstated survive?`
   295	
   296	1. `Yes, mostly.`
   297	
   298	If the question is `Has Caplan shown that immigration restrictions are unnecessary for protecting the welfare of existing residents in the destination country?`
   299	
   300	1. `No.`
   301	
   302	The best current summary is:
   303	
   304	1. `Caplan is strongest on migrant-welfare direction and large global-gains sign, not on the strongest open-borders magnitude or destination-capacity closure.`
   305	2. `Caplan is strongest on observed U.S. justice-system-rate crime skepticism relative to his other empirical lanes.`
   306	3. `Caplan is partially supported on labor, but only after dropping collapse rhetoric and admitting wage-growth pressure in constrained places.`
   307	4. `Caplan is weakest as a blanket taxpayer and political-incidence analyst because recent surge evidence means local capacity, housing, shelter, and political-response channels cannot be assumed zero.`
   308	
   309	So the final score is:
   310	
   311	1. `strong on the left side of the causal graph`
   312	2. `too optimistic on the right side`
   313	
   314	## Revisions
   315	
   316	| Date | Change |
   317	|------|--------|
   318	| 2026-06-16 | Replaced the "strongest current worker-incidence channel" shortcut with evidence-surface language: current memos better develop constrained-place wage progression than broad job destruction. See `immigration-conclusion-audit-running-fixes.md`. |
   319	| 2026-06-16 | Replaced first-binding culture and political-externality shortcuts with evidence-surface language: housing/service/political channels are better developed in current memos, not proven universally primary. See `immigration-conclusion-audit-running-fixes.md`. |
   320	| 2026-06-16 | Replaced remaining "Caplan is right" labels with claim-support language, including global-gains, ledger-blurring, labor-collapse, and DAG framing. See `immigration-conclusion-audit-running-fixes.md`. |
   321	| 2026-06-16 | Replaced residual right/wrong and wins/loses verdict labels with strongest/weakest/support language while preserving the same claim ranking. See `immigration-conclusion-audit-running-fixes.md`. |
   322	| 2026-06-16 | Bounded the Caplan global-gains verdict to direction/sign rather than strongest magnitude or destination-capacity closure. See `immigration-conclusion-audit-running-fixes.md`. |
   323	| 2026-06-16 | Scoped shorthand "wins on crime" language to observed U.S. justice-system-rate skepticism, matching the crime memo's true-offending caveat. See `immigration-conclusion-audit-running-fixes.md`. |
--- END FILE: research/immigration-bryan-caplan-claims-audit-2026-04-21.md ---

--- BEGIN FILE: research/immigration-capacity-frontier-2026-04-21.md ---
     1	# Immigration capacity frontier: stock, flow, load, and what still remains
     2	
     3	**Question:** After extending the county panel again, what is the cleanest current answer on thresholds, counterfactual levers, subgroup needs, voting, and welfare?  
     4	**Tier:** Deep | **Date:** 2026-04-21  
     5	**Ground truth:** The prior county and threshold passes suggested that `permit throughput` and `rent burden` were more informative than generic immigrant-share rhetoric, but they still leaned on one or two threshold constructions. This memo compares `stock`, `flow`, and `flow-to-build-capacity` directly and checks whether the threshold survives outside a single arbitrary split. [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md] [SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md]
     6	
     7	## Bottom line
     8	
     9	1. The repo's strongest current predictor for `political response` remains `immigrant stock share`, but `flow-to-build-capacity` still adds residual signal once stock and flow are both included. [DATA]
    10	2. For `wage growth`, `employment growth`, and `native net migration`, the cleaner signal is not stock share. It is `recent immigrant flow relative to local permit capacity`. [DATA]
    11	3. A recurring threshold pattern is visible, but it is not best described as `foreign-born share crosses X`. It looks more like a `high-flow tail x weak build response` pattern. The interaction is clearest around the `70th-80th` flow percentiles with `bottom-half or bottom-quartile` permit capacity. [DATA]
    12	4. This tightens the current repo view:
    13	   - `politics`: stock + load both matter
    14	   - `wages`: load/capacity matters more than stock
    15	   - `employment`: still not a generic collapse story, but a negative signal does appear under direct load-capacity formulations
    16	   - `native sorting`: load/capacity and affordability both matter; the native exit channel is not just ideology or partisan response [INFERENCE]
    17	5. The remaining frontier is now clearer:
    18	   - `subgroup composition` needs the missing origin warehouse or new acquisition
    19	   - `voting` needs a native-turnout / precinct or survey design, not county returns alone
    20	   - `welfare` needs state/local service and federal-transfer linkage, not just macro aggregates
    21	   - `receiver-city counterfactuals` still need synthetic controls [INFERENCE]
    22	
    23	## New artifacts
    24	
    25	1. [analyze_capacity_frontier.py](./sources/immigration-causal/scripts/analyze_capacity_frontier.py)
    26	2. [county_capacity_frontier_summary.json](./sources/immigration-causal/data/outcomes/analysis/county_capacity_frontier_summary.json)
    27	3. [county_capacity_model_comparison.csv](./sources/immigration-causal/data/outcomes/analysis/county_capacity_model_comparison.csv)
    28	4. [county_capacity_threshold_grid.csv](./sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_grid.csv)
    29	5. [county_load_capacity_deciles.csv](./sources/immigration-causal/data/outcomes/analysis/county_load_capacity_deciles.csv)
    30	6. [receiver_capacity_descriptives_2024.csv](./sources/immigration-causal/data/outcomes/analysis/receiver_capacity_descriptives_2024.csv)
    31	
    32	## Measurement frame
    33	
    34	The new derived variable is:
    35	
    36	`recent immigrant load per permit unit = annual recent immigrant persons / annual permit units`
    37	
    38	using:
    39	
    40	1. `annual recent immigrant persons = recent_fb_annual_share * total population` [DATA]
    41	2. `annual permit units = permit_units_2021_2024 / 4` [DATA]
    42	3. a heuristic `2.5 persons per housing unit` when translating units into rough people-capacity [INFERENCE]
    43	
    44	This is not a full housing-market model. It is a tractable public-data proxy for:
    45	
    46	`flow / local build capacity`
    47	
    48	That is the more relevant descriptive object if the threshold story is about absorption rather than stock. [INFERENCE]
    49	
    50	## Claims table
    51	
    52	| # | Claim | Evidence | Confidence | Source | Status |
    53	|---|---|---|---|---|---|
    54	| 1 | Stock share remains the strongest simple county predictor of GOP margin shift | In separate one-predictor county models, standardized `fb_share` has larger `t` and higher adjusted `R²` than flow or load | HIGH | [county_capacity_model_comparison.csv](./sources/immigration-causal/data/outcomes/analysis/county_capacity_model_comparison.csv) | VERIFIED |
    55	| 2 | Load-capacity still adds residual political-response signal beyond stock and flow | In the combined margin model, standardized load remains positive and significant (`t≈2.74`, `p≈0.006`) | HIGH | [county_capacity_model_comparison.csv](./sources/immigration-causal/data/outcomes/analysis/county_capacity_model_comparison.csv) | VERIFIED |
    56	| 3 | Wage-growth models load more cleanly on load-capacity than on stock or flow alone | Load-only wage model has the strongest negative `t` and best adjusted `R²` among single-predictor formulations | HIGH | same | VERIFIED |
    57	| 4 | A negative employment signal appears under direct load-capacity formulations even though the earlier coarse threshold did not show broad job loss | Load-only and combined employment models are negative and highly significant; stock and flow alone are weak or null | HIGH | same | VERIFIED |
    58	| 5 | The threshold is clearest in the broad high-flow tail (`70th-80th percentile`) interacted with low permit capacity, not at one single extreme cutoff | Interaction grid shows stronger wage and some politics/employment effects at `q70-q80` than at `q90` | HIGH | [county_capacity_threshold_grid.csv](./sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_grid.csv) | VERIFIED |
    59	| 6 | Native net migration is more negative in higher load-capacity deciles | Load deciles show about `-1.07 pp` gap from `D1` to `D10`; load-based models outperform stock-only on adjusted `R²` | HIGH | [county_load_capacity_deciles.csv](./sources/immigration-causal/data/outcomes/analysis/county_load_capacity_deciles.csv), [county_capacity_model_comparison.csv](./sources/immigration-causal/data/outcomes/analysis/county_capacity_model_comparison.csv) | VERIFIED |
    60	| 7 | Receiver-city spending is more tightly tied to absolute shelter shortfall than to saturation ratio alone | In 2024 receiver descriptives, `corr(shelter_gap_vs_hic, spending) ≈ 0.93`, much larger than `corr(sheltered_to_hic_ratio, spending)` | MEDIUM | [receiver_capacity_descriptives_2024.csv](./sources/immigration-causal/data/outcomes/analysis/receiver_capacity_descriptives_2024.csv) | VERIFIED |
    61	
    62	**Scope note:** In this table, `HIGH` and `VERIFIED` mean the reported model-output pattern is file-backed and reproducible from the listed artifacts. They do not mean the county associations are clean causal effects; the causal caveats below still apply. [INFERENCE]
    63	
    64	## What changed from the prior position?
    65	
    66	The prior county memo said:
    67	
    68	1. `permit throughput` was the wage-side bottleneck [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md]
    69	2. `rent burden` was the stronger native-sorting signal [SOURCE]
    70	3. there was no clear broad county `employment-collapse` signal under the `high_recent_fb x low_permit` specification [SOURCE]
    71	
    72	That still mostly survives, but the more direct `flow / build-capacity` formulation sharpens it:
    73	
    74	1. `permit throughput` was the right direction
    75	2. the more precise object is `immigrant flow relative to annual permit capacity`
    76	3. under that object, `employment` no longer looks fully null
    77	
    78	So the update is not `the old memo was wrong`. It is:
    79	
    80	1. the earlier threshold split was too coarse
    81	2. the direct load-capacity ratio finds additional strain that the binary split missed
    82	
    83	## Model comparison: what actually predicts what?
    84	
    85	### 1) Politics: stock is still strongest, but load is not fake
    86	
    87	For `margin_shift`, the simple one-predictor ranking is:
    88	
    89	1. `stock_only`: `beta≈+0.0150`, `t≈12.08`, `adj_R²≈0.415` [DATA]
    90	2. `flow_only`: `beta≈+0.0099`, `t≈9.32`, `adj_R²≈0.369` [DATA]
    91	3. `load_only`: `beta≈+0.0054`, `t≈6.96`, `adj_R²≈0.345` [DATA]
    92	
    93	So the stock variable still carries the most countywide political signal. That matters because it means the political-response story is **not** reducible to a pure recent-surge story. Established immigrant concentration, long-run demographic sorting, and Hispanic realignment are still in the political mix. [INFERENCE]
    94	
    95	But the combined model matters too:
    96	
    97	1. `load` remains positive and significant with `t≈2.74`, `p≈0.006` after including both stock and flow [DATA]
    98	
    99	So the stronger claim is:
   100	
   101	1. `stock` carries the broad political-map signal in this county model
   102	2. `load / capacity` still adds residual strain in that map
   103	
   104	### 2) Wages: load-capacity is cleaner than stock
   105	
   106	For `weekly wage growth`:
   107	
   108	1. `stock_only`: `t≈-3.97`, `adj_R²≈0.147` [DATA]
   109	2. `flow_only`: `t≈-3.75`, `adj_R²≈0.144` [DATA]
   110	3. `load_only`: `t≈-4.08`, `adj_R²≈0.154` [DATA]
   111	
   112	And in the combined model:
   113	
   114	1. `load` stays negative with `t≈-2.49`, `p≈0.013` [DATA]
   115	
   116	This is the clearest county descriptive evidence yet that the `worker` question is tied to:
   117	
   118	`inflow under weak absorption capacity`
   119	
   120	not just `immigrant stock exists`. [INFERENCE]
   121	
   122	### 3) Employment: still not collapse rhetoric, but no longer cleanly null
   123	
   124	This is the most important revision.
   125	
   126	Under the old `high_recent_fb x low_permit` interaction, employment was basically null. [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md]
   127	
   128	Under the direct load-capacity metric:
   129	
   130	1. `stock_only`: weak, `p≈0.17` [DATA]
   131	2. `flow_only`: weak, `p≈0.079` [DATA]
   132	3. `load_only`: `beta≈-0.0087`, `t≈-7.10`, `adj_R²≈0.117` [DATA]
   133	4. `combined`: `beta≈-0.0123`, `t≈-8.83`, `adj_R²≈0.129` [DATA]
   134	5. `high_load90`: `beta≈-0.0106`, `p≈0.013` [DATA]
   135	
   136	Basic robustness checks keep the sign:
   137	
   138	1. using a `95th` rather than `99th` percentile winsorization leaves the employment result strongly negative [DATA: `county_capacity_frontier_summary.json`]
   139	2. excluding receiver and border counties still leaves a negative load effect with `t≈-4.79` [DATA]
   140	
   141	That does **not** justify `immigration causes county employment collapse`.
   142	
   143	It does justify this narrower update:
   144	
   145	1. `high immigrant load relative to local build capacity` is associated with slower employment growth as well as slower wage growth
   146	
   147	### 4) Native sorting: load-capacity beats stock-only
   148	
   149	For `net U.S. migration share`, all three predictors are strongly negative, but `load_only` has the best single-predictor adjusted `R²`, and the combined model improves further. [DATA]
   150	
   151	The decile table is intuitive:
   152	
   153	1. `D1` median net domestic migration share: about `+0.82 pp` [DATA]
   154	2. `D10` median net domestic migration share: about `-0.24 pp` [DATA]
   155	3. gap: about `-1.07 pp` [DATA]
   156	
   157	This is a more directly relevant descriptive screen for the destination-country question than global-output arguments:
   158	
   159	1. counties where immigrant inflow materially outruns local build response show more negative domestic net migration; whether incumbents sort away because of that load still needs counterfactual identification
   160	
   161	## Threshold effects: where do they actually show up?
   162	
   163	The threshold grid matters because it checks whether the story is just one arbitrary `80th percentile x median permit` construction.
   164	
   165	### What survives
   166	
   167	The clearest and most repeatable interaction is:
   168	
   169	1. `high flow x low permit` hurts `wage growth`
   170	
   171	Examples:
   172	
   173	1. `q70 flow x q25 permit`: wage `beta≈-0.0160`, `p≈0.011` [DATA]
   174	2. `q80 flow x q25 permit`: wage `beta≈-0.0203`, `p≈0.025` [DATA]
   175	3. `q80 flow x q50 permit`: wage `beta≈-0.0151`, `p≈0.0015` [DATA]
   176	
   177	Politics also shows up in the broad high-flow tail:
   178	
   179	1. `q70 flow x q50 permit`: margin shift `beta≈+0.62 pp`, `p≈0.040` [DATA]
   180	2. `q80 flow x q50 permit`: margin shift `beta≈+0.85 pp`, `p≈0.029` [DATA]
   181	
   182	Employment appears in some of the same bands:
   183	
   184	1. `q70 flow x q25 permit`: employment `beta≈-1.86 pp`, `p≈0.0045` [DATA]
   185	2. `q80 flow x q25 permit`: employment `beta≈-1.82 pp`, `p≈0.019` [DATA]
   186	
   187	### What weakens
   188	
   189	The `q90` extreme-flow interactions are weaker and less stable for politics and wages. [DATA]
   190	
   191	That suggests the observed threshold pattern is **not**:
   192	
   193	1. `only the absolute top-decile explodes`
   194	
   195	It looks more like:
   196	
   197	1. `once a county enters the broad high-flow tail and also has weak building response, strain becomes visible`
   198	
   199	That is a better descriptive threshold story. Causal interpretation still needs a design that separates inflow, housing response, and destination selection. [INFERENCE]
   200	
   201	## Decile read: how large is the gap?
   202	
   203	From the load-capacity deciles:
   204	
   205	1. `D1` median flow-per-permit-unit: about `0.04`
   206	2. `D10` median flow-per-permit-unit: about `3.56`
   207	
   208	Associated median changes:
   209	
   210	1. `margin shift`: `+3.12 pp` -> `+4.90 pp` (`+1.78 pp` gap) [DATA]
   211	2. `weekly wage growth`: `13.56 pp` -> `11.99 pp` (`-1.56 pp` gap) [DATA]
   212	3. `employment growth`: `6.07 pp` -> `4.50 pp` (`-1.56 pp` gap) [DATA]
   213	4. `native net migration share`: `+0.82 pp` -> `-0.24 pp` (`-1.07 pp` gap) [DATA]
   214	
   215	That is the cleanest single descriptive picture in the new pass.
   216	
   217	## Receiver nodes: what matters most in the crisis cases?
   218	
   219	The receiver-node panel remains small-N, so it is descriptive rather than causal.
   220	
   221	Still, two points survive:
   222	
   223	1. the saturated `2024` nodes remain `Denver`, `New York City`, and `Bexar` [DATA]
   224	2. spending aligns much more with `absolute shelter shortfall` than with simple saturation ratio:
   225	   - `corr(shelter_gap_vs_hic, spending) ≈ 0.93`
   226	   - `corr(sheltered_to_hic_ratio, spending) ≈ 0.32` [DATA]
   227	
   228	This matters because it means the receiver-city crisis is not only about crossing `ratio > 1`. It is also about:
   229	
   230	1. how large the absolute shortfall is
   231	2. what legal and assignment regime turns that shortfall into fiscal outlay [INFERENCE]
   232	
   233	One caution remains:
   234	
   235	1. Denver's `peak_minus_baseline_shelter` denominator is still distorted by the baseline issue already noted in the threshold memo, so cost-per-extra-shelter normalization should still be handled carefully. [SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md]
   236	
   237	## What this updates, and what it does not settle
   238	
   239	### What now looks stable enough for the repo
   240	
   241	1. `Foreign-born share` alone is not the right master threshold variable. [DATA]
   242	2. `Flow x capacity` is the cleaner descriptive county stress object for wages, employment, and native sorting. [DATA]
   243	3. `Politics` still loads heavily on stock, but capacity strain adds model residual signal. [DATA]
   244	4. The relevant threshold is broad high-flow exposure under weak building response, not only an extreme top-decile event. [DATA]
   245	
   246	### What is still open
   247	
   248	1. **Counterfactual receiver-city paths**
   249	   We still need synthetic controls or better event-study controls for `NYC`, `Chicago`, `Denver`, `Boston`, `Bexar`. [INFERENCE]
   250	
   251	2. **Subgroup composition**
   252	   The origin warehouse cited by earlier memos is not actually present in the current local repo state, so a real `subgroup / ethnic / pathway / family-structure` extension is not valid to rerun right now without reacquiring or rebuilding that layer. [DATA: missing local artifact]
   253	
   254	3. **Voting**
   255	   County returns do not identify whether the effect is native turnout, persuasion, composition change, or precinct-level backlash. The current county evidence is about `political response`, not immigrant voting behavior. [INFERENCE]
   256	
   257	4. **Welfare**
   258	   We still do not have a joined micro-to-local service ledger that cleanly separates:
   259	   - federal taxes/transfers
   260	   - state/local education
   261	   - shelter/emergency services
   262	   - Medicaid/uncompensated care
   263	   - pathway and family composition [INFERENCE]
   264	
   265	## Best current synthesis
   266	
   267	The repo's current best answer is now:
   268	
   269	1. `Global gains` are still possible at bounded margins, but destination-country incidence depends heavily on capacity. [SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md]
   270	2. `County stress` is best understood as `flow relative to build capacity`, not as immigrant share in the abstract. [DATA]
   271	3. `Stock` still matters politically, so the political-response story is not just about the recent surge. [DATA]
   272	4. `High load / low capacity` is where wage growth, employment growth, domestic net migration, and political-response metrics move in the adverse direction together. [DATA]
   273	
   274	That is a stricter and more useful answer than either:
   275	
   276	1. `immigration is good because GDP`
   277	2. `immigration is bad because stock share rose`
   278	
   279	The better formula is:
   280	
   281	`incidence = stock + flow + capacity + composition + regime`
   282	
   283	and in the current public-data stack, `flow + capacity` is where the new descriptive traction is coming from. Causal identification still needs stronger counterfactual design. [INFERENCE]
   284	
   285	## Revisions
   286	
   287	| Date | Change |
   288	|------|--------|
   289	| 2026-06-16 | Replaced the remaining "stock drives the broad political map" shortcut with descriptive model-signal language. See `immigration-conclusion-audit-running-fixes.md`. |
   290	| 2026-06-16 | Replaced residual "established"/"settles" wording with suggested/updates language; county capacity models remain descriptive model-output evidence, not settled causal identification. See `immigration-conclusion-audit-running-fixes.md`. |
   291	| 2026-06-16 | Added a claims-table scope note: `HIGH`/`VERIFIED` refer to reproducible model-output patterns, not causal identification. See `immigration-conclusion-audit-running-fixes.md`. |
   292	| 2026-06-16 | Reframed the native-sorting sentence as a descriptive association rather than a causal incumbent-exit claim. See `immigration-conclusion-audit-running-fixes.md`. |
   293	| 2026-06-16 | Removed residual causal verbs from the claims table and wage section: the load-capacity rows are verified descriptive model-output patterns, not causal response estimates. See `immigration-conclusion-audit-running-fixes.md`. |
--- END FILE: research/immigration-capacity-frontier-2026-04-21.md ---

--- BEGIN FILE: research/immigration-confidence-ladder.md ---
     1	# Immigration confidence ladder
     2	
     3	Date: 2026-04-10
     4	
     5	Scale:
     6	1. `strong`
     7	2. `medium`
     8	3. `weak`
     9	4. `contextual-only`
    10	
    11	Rule:
    12	A metric can be statistically clean and still be only `contextual-only` for the question we are asking.
    13	
    14	## Strong
    15	
    16	1. `ACS origin / education / recency composition counts`
    17	Rating: `strong`
    18	Reason: these are direct weighted ACS summaries, not inferred fiscal objects. [SOURCE: ./sources/immigration-fiscal/data/derived/extend_immigration_context_with_origins.sql]
    19	
    20	2. `PUMA-level median gross rent as destination cost exposure`
    21	Rating: `strong`
    22	Reason: official ACS geography, directly observed, useful as exposure context. It is not a welfare scalar. [SOURCE: ./sources/immigration-fiscal/data/derived/extend_immigration_context_with_pumas.sql]
    23	
    24	3. `Household-normalized school-age child metrics after WGTP correction`
    25	Rating: `strong`
    26	Reason: the prior proxy was wrong; the corrected household join is materially better and uses the right unit. [SOURCE: ./research/immigration-household-weighted-correction.md]
    27	
    28	4. `Claim that the Clark “agree” papers are scope-limited rather than obviously false`
    29	Rating: `strong`
    30	Reason: that conclusion survives repeated paper review and is consistent with the actual paper scopes. [SOURCE: ./research/immigration-economist-effects-matrix.md]
    31	
    32	## Medium
    33	
    34	5. `Federal versus state/local incidence split as a research frame`
    35	Rating: `medium`
    36	Reason: official sources strongly support the split, but our own warehouse only partially models the federal side. [SOURCE: https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf] [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
    37	
    38	6. `County CHAS housing-stress shares`
    39	Rating: `medium`
    40	Reason: good background stress metric, but not immigrant-attributable marginal burden. [SOURCE: ./sources/immigration-fiscal/data/derived/build_stage2_incidence_context.py]
    41	
    42	7. `State school-spending per pupil as school-pressure context`
    43	Rating: `medium`
    44	Reason: official and clean, but too coarse for marginal burden or district-specific claims. [SOURCE: ./sources/immigration-fiscal/data/derived/build_immigration_context_duckdb.sql]
    45	
    46	8. `Housing-heavy versus school-heavy origin-group typology`
    47	Rating: `medium`
    48	Reason: useful descriptive shorthand for destination exposure, but still proxy-based and sensitive to geography choice. [SOURCE: ./research/immigration-local-burden-puma-layer.md]
    49	
    50	9. `Descendant upside as a real channel`
    51	Rating: `medium`
    52	Reason: the long-run literature supports it, but sign and magnitude are heterogeneous and horizon-dependent. [SOURCE: https://d279m997dpfwgl.cloudfront.net/wp/2016/09/0922_immigrant-economics-full-report.pdf] [SOURCE: https://www.nber.org/system/files/working_papers/w33961/w33961.pdf]
    53	
    54	## Weak
    55	
    56	10. `Area-weighted PUMA-to-county bridge`
    57	Rating: `weak`
    58	Reason: land area is not people, renters, students, or immigrant households. This is a convenience bridge, not a precise exposure model. [SOURCE: ./sources/immigration-fiscal/data/derived/build_puma_county_crosswalk.py]
    59	
    60	11. `IRS county migration balance as burden evidence`
    61	Rating: `weak`
    62	Reason: at best it is contextual mobility climate. It is not immigrant-specific and not causal. [SOURCE: ./research/immigration-stage2-county-bridge-batch.md]
    63	
    64	12. `Federal-positive versus federal-negative origin ranking from ACS income and benefit proxies`
    65	Rating: `weak`
    66	Reason: this is not a tax-transfer microsimulation. It is a partial proxy stack. [SOURCE: ./research/immigration-low-skill-origin-incidence-memo.md]
    67	
    68	13. `Magnitude claims for local school burden from current warehouse`
    69	Rating: `weak`
    70	Reason: district assignment, ELL intensity, migrant composition, and marginal cost are not modeled well enough yet. [SOURCE: ./research/immigration-adversarial-review.md]
    71	
    72	## Contextual-only
    73	
    74	14. `County CHAS plus rent plus school-spend combined into one local burden scalar`
    75	Rating: `contextual-only`
    76	Reason: combining context layers does not make a causal burden estimate.
    77	
    78	15. `Average citizen better off / worse off`
    79	Rating: `contextual-only`
    80	Reason: too much depends on weights over renters, employers, taxpayers, future descendants, and politics.
    81	
    82	16. `Bad for the country`
    83	Rating: `contextual-only`
    84	Reason: without explicit horizon and counterfactuals, the phrase has almost no analytical content.
    85	
    86	## Causal-design layer added 2026-04-18
    87	
    88	17. `Large Borjas-style native wage gains under observed E-Verify mandates`
    89	Rating: `strong against large gains in this design`
    90	Reason: TWFE on QWI 2003-2023, 9 treated states (AZ, MS, SC, UT, GA, AL, NC, TN, FL), 42 controls. Coefficient on E1 in E-Verify-exposed industries: +0.51% (SE 0.81%, n=16,736). 95% CI excludes large Borjas-style magnitudes (>2.1%) for this observed mandate margin. Aligns with Card direction; not a direct replication or a global wage-family rejection. [SOURCE: research/immigration-causal-everify-card-vs-borjas.md]
    91	
    92	18. `Immigrants concentrate in inelastic-supply MSAs (welfare implication for rent burden)`
    93	Rating: `strong (descriptive)`
    94	Reason: top FB-share quintile median Saiz 2010 elasticity = 1.51, bottom = 3.40. n=237 MSAs, ACS 2018-22. Implication: rent exposure in inelastic destination markets is a stronger renter-incidence warning than the adversarial review allowed; aggregate welfare loss remains unmeasured. [SOURCE: research/immigration-causal-saiz-elasticity-rent.md]
    95	
    96	19. `Card-side bounded native-wage-impact evidence for observed low-skill shocks`
    97	Rating: `medium-strong`
    98	Reason: convergent evidence — Card 1990 Mariel, Foged-Peri 2016 Denmark refugee assignment, this cycle's E-Verify TWFE 2003-2023 — points against large native low-skill wage losses/gains in these designs. It does not identify one shared complementarity mechanism. Borjas 2017 restricted-Mariel magnitude should not be mechanically extrapolated to broader staggered designs. [SOURCE: research/immigration-causal-everify-card-vs-borjas.md, multiple papers]
    99	
   100	## Paradigm-escape layer added 2026-04-18 (evening)
   101	
   102	20. `Saiz elasticity-immigrant correlation is stronger for regulatory index than topographic unavailability` — **QUALIFIED by entry 38**
   103	Rating: `strong descriptive`
   104	Reason: log(FB share) ~ unaval (β=+0.12, t=0.58, n.s.) + WRLURI (β=+0.33, t=6.29***) + log_pop. WRLURI is the stronger correlate in this cross-section; this does not identify zoning as the causal driver or prove zoning reform would reduce immigrant renter burden. Treat zoning reform as a plausible policy hypothesis, not a verified lever. [SOURCE: scripts/saiz_decomposition.py]
   105	
   106	21. `Sanctuary policy variation shows no significant native low-skill wage change either direction`
   107	Rating: `no significant E1 wage change observed in this design`
   108	Reason: TWFE on QWI 2003-2023 with 12 pro-sanctuary + 9 anti-sanctuary states; all E1 specifications |t|<1.0. This is an additional QWI policy-margin check consistent with the bounded Card-side reading for observed marginal policy variation, but it is not an equivalence-tested zero. [SOURCE: scripts/analyze_sanctuary_wages.py]
   109	
   110	22. `Domestic newcomer counts are much larger than moved-from-abroad counts at median county`
   111	Rating: `medium`
   112	Reason: IRS SOI `Total Migration-US` 2022-23 and ACS `B07001_081E` point in the same descriptive direction, but they are not like-for-like universes. The current median county comparison is roughly `4.59%` vs `0.21%`, with a ratio of medians around `21.7x` and a median county-level ratio around `20.5x`, so the safe claim is order-of-magnitude disparity, not a precise burden ratio. [SOURCE: research/immigration-causal-internal-vs-immigrant-newcomers.md]
   113	
   114	23. `Open-borders welfare verdict is welfare-weight-sensitive under current empirical inputs` — **QUALIFIED by entry 39**
   115	Rating: `strong (framing claim)`
   116	Reason: At immigrant-welfare-weight w=0 (current repo's implicit framing): negative by construction. At w≥0.25 under 25%-of-gross-gains native-cost benchmark: positive. At w=1.0 even under harsh 50%-cost benchmark: positive. Empirical evidence cannot choose the value weight, but native-cost, fiscal, housing/capacity, and sending-country inputs can move break-even thresholds. Honest framing must name both the weight and the empirical calibration. [SOURCE: data/clemens/gpt54_calibration_review.md, GPT-5.4 sensitivity analysis]
   117	
   118	24. `Mass deportation of 7M unauthorized → ~$1.45T first-order output shock (~5% GDP); Type-II endpoint is sensitivity only` — **presentation qualified by entry 32**
   119	Rating: `medium (calibration not estimate)`
   120	Reason: BEA Use Table 2023 partial-equilibrium with industry FB-share assumptions from Pew/CMS. First-order $1.45T; a Type-II multiplier (~1.6) gives a $2.32T sensitivity, not a headline estimate. Per-removed-worker loss $207K first-order and $332K under Type-II sensitivity. Most affected: Construction (-5.9%), Other services / cleaning (-8.8%), Agriculture (-4.3%). The E-Verify employment result is, at most, a weak plausibility check for employment response under one marginal enforcement setting; it does not validate the mass-deportation calibration or its industry loss magnitudes. [SOURCE: scripts/mass_deportation_sim.py] [SOURCE: research/immigration-causal-everify-card-vs-borjas.md]
   121	
   122	## Surge layer added 2026-04-18 (late evening)
   123	
   124	25. `Title 42 lift timing did not match surge onset; surge was a regime shift starting Dec 2022` — **EVIDENCE SUPERSEDED by entry 35**
   125	Rating: `medium`
   126	Reason: SWB encounters peaked Jan-Mar 2023 at 50K+/month BEFORE Title 42 lift (May 2023). Lift coincided with April-May lull, then gradual rebuild to surge levels. Pre/post comparison is composition-driven, not policy-causal. [SOURCE: research/immigration-causal-surge-2021-2024.md]
   127	
   128	26. `CHNV parole did not substitute legal flow for illegal flow; it added on top` — **INVALIDATED by entry 34; historical only, do not quote**
   129	Rating: `strong`
   130	Reason: TWFE β=+3.29 (t=4.78) on CHNV nationality vs control after Jan 2023. Encounters from CHNV nationalities ROSE 787% post-program, not fell. Refutes the stated rationale that legal pathway would reduce irregular migration. [SOURCE: data/cbp/swb_encounters_by_citizenship_monthly.parquet]
   131	
   132	27. `Receiver-city local fiscal load was real and concentrated` — **scope qualified by entry 33**
   133	Rating: `strong (administrative data)`
   134	Reason: NYC FY24 $3.7B (3.5% of operating budget); MA FY24 $1B; Chicago $228M peak; Denver $89M (with cuts to other services). Combined ~$5B+/yr peak across major receivers. Receiver-load stress has empirical bite, but these are gross outlays; entry 33 supplies the net-burden caveat. [SOURCE: data/bused_cities/receiver_city_costs.csv]
   135	
   136	28. `Receiver cities swung +4.41 pp more Republican in 2024 than comparable non-receivers` — **QUALIFIED by entries 31 and 36; final causal-implausibility sentence superseded**
   137	Rating: `medium (correlation, multiple confounders)`
   138	Reason: Multivariate OLS with state FE: receiver_city β=+0.024 (t=6.96***). Top receivers (Bronx +11pp, Queens +11pp, Hidalgo +10pp, Cameron +10pp, El Paso +10pp, Miami-Dade +9pp) swung massively toward Trump. Confounders include national Hispanic realignment, inflation, and policy-endogenous busing destinations. Magnitude implausibly large for non-immigration causes alone. **Do not reuse the final sentence; entries 31 and 36 supersede it with the controlled +2.4pp upper-bound framing.** [SOURCE: research/immigration-causal-surge-2021-2024.md]
   139	
   140	29. `Static-cycle Card-side wage finding is BOUNDED to marginal-policy variation; surge is OUTSIDE that variation`
   141	Rating: `meta-update on prior entries 17, 19, 21`
   142	Reason: Prior entries over-compressed the E-Verify/sanctuary wage results as a "decisive Card-side win for U.S. policy variation." The safer reading is strong Card-side evidence for observed 2008-2021 marginal policy variation. The 2021-2024 surge is a regime shift outside that variation. Linear extrapolation is not warranted. Surge-period wage estimates remain to be done (require ACS PUMS 2023). [SOURCE: research/immigration-causal-surge-2021-2024.md]
   143	
   144	## Bias-audit layer added 2026-06-11
   145	
   146	Trigger: mirror-test against the criticisms of the Cato 2026 fiscal study ("did we commit its biases?"). Full audit and the general checklist live in [notes/quant-bias-checklist.md](../notes/quant-bias-checklist.md). Prior entries are not rewritten (append-only); these supersede where they conflict.
   147	
   148	30. `CHNV parole did not substitute legal flow for illegal flow; it added on top` — **INVALIDATED by entry 34; historical only, do not quote**
   149	Reason: interim downgrade before the OHSS parser correction. The source memo itself listed reverse causation as a live mechanism, but entry 34 later reversed the descriptive reading too: the "+787%" rise was the program's lawful OFO channel on a scrambled clock, while corrected USBP between-port crossings fell sharply. Do not reuse the "substitution did not happen" language or the `+787%` figure except as an error trace. [SOURCE: research/immigration-causal-surge-2021-2024.md] [SOURCE: decisions/2026-06-11-ohss-date-universe-bugs-chnv-reversal.md]
   150	
   151	31. `Receiver-city 2024 GOP swing` (entry 28) — **grade unchanged (medium), headline language corrected**
   152	The phrase "magnitude implausibly large for non-immigration causes alone" is a plausibility assertion doing causal work and should not be reused. The top swing counties (Bronx, Queens, Miami-Dade, Hidalgo, El Paso) are among the most Hispanic-populous counties in the country; the national 2024 Hispanic realignment is near-collinear with "receiver city" in that list, and the multivariate pass controls FB share but not Hispanic share. Use the controlled estimate (+2.4pp, receiver_city β=+0.024, state FE) rather than the raw +4.41pp gap, and treat even that as upper-bound until a Hispanic-share control or within-Hispanic-county comparison is run. [SOURCE: research/immigration-causal-surge-2021-2024.md] [SOURCE: notes/quant-bias-checklist.md item 25]
   153	
   154	32. `Mass deportation output shock` (entry 24) — **grade unchanged (medium, calibration), presentation rule added**
   155	Lead with the first-order figure (`~$1.45T`, ~5% GDP); the `$2.32T` Type-II-multiplier endpoint appears only as labeled sensitivity, never inside a headline range. Stacking the modeled amplifier into the headline is the same move as Cato's `$3.9T` interest-savings add-on (27% of their `$14.5T`), in the opposite political direction. The calibration also freezes replacement hiring, wage response, and capital reallocation at zero — state this when quoting. [SOURCE: sources/immigration-causal/scripts/mass_deportation_sim.py] [SOURCE: notes/quant-bias-checklist.md items 4, 15]
   156	
   157	33. `Receiver-city fiscal load` (entry 27) — **grade unchanged (strong, administrative data), scope annotation**
   158	The figures are **gross city outlays**, not net burden: federal Shelter and Services Program reimbursements and the counterfactual baseline growth of homeless-services spending are not netted out. "NYC spent $3.7B in FY24" is strong; "the surge cost NYC $3.7B net" is not yet supported. [SOURCE: sources/immigration-causal/data/bused_cities/receiver_city_costs.csv] [SOURCE: notes/quant-bias-checklist.md item 10]
   159	
   160	## Data-correction layer added 2026-06-11 (evening)
   161	
   162	Trigger: the morning layer's two open kill-tests were run against local data and exposed two bugs in the OHSS encounter parser (fiscal-index dates; agency-block overwrite that made the series OFO-ports-only). Full trace: [decisions/2026-06-11-ohss-date-universe-bugs-chnv-reversal.md](../decisions/2026-06-11-ohss-date-universe-bugs-chnv-reversal.md). These entries supersede 25, 26, and 30 where they conflict.
   163	
   164	34. `CHNV substituted lawful port flow for irregular crossings in its initial year` — **reversal of entry 26**
   165	Rating: `strong (initial period); medium beyond ~12 months`
   166	Reason: corrected USBP (between-ports) event study with staggered dates and flat pre-trends: Cuba −95.3%, Nicaragua −96.2%, Venezuela −57.5% (initial, decaying by τ+11 — Darién rebound), Haiti structurally ~0 between ports. Mean τ[0,+3] = −2.17 log points. The old "+787% — added on top" figure was the program's own lawful OFO channel on a scrambled clock; corrected total-CBP DiD is null (β=+0.45, t=1.29). Ledger discipline: lawful parole inflow (~530K) still lands in receiver cities — substitution-of-channel, not reduction-of-arrivals. [SOURCE: sources/immigration-causal/data/outcomes/analysis/chnv_pretrends/results.json]
   167	
   168	35. `Corrected timing does not support Title 42 lift as proximate surge onset` — **replaces entry 25 evidence and narrows conclusion**
   169	Rating: `medium`
   170	Reason: the entry's timing facts were artifacts. Corrected series: Dec-2022 local peak 252K → Jan-Feb 2023 trough (CHNV substitution visible) → April-May 2023 anticipation spike (212K/207K) → June post-lift crash (−30%) → Dec 2023 record 301,980. Post-lift 6-month mean −14.5% vs pre-lift. This timing result refutes the old simple post-lift jump story, not every possible Title 42 effect through anticipation, routing, composition, or later-equilibrium channels. [SOURCE: scripts/analyze_surge_title42_chnv.py rerun 2026-06-11]
   171	
   172	36. `Receiver-city 2024 GOP swing survives the Hispanic-realignment control` — **closes entry 31's open work**
   173	Rating: `medium (correlation; robust to the named rival channel)`
   174	Reason: pre-registered kill-test with 2020 county Hispanic share (popest baseline): receiver β +0.0256 → +0.0238 (t≈7.2) with the control in; Hispanic share itself β=+0.062 (t=17.2); within top-Hispanic-quintile, receivers +4.3pp raw vs comparable counties. Hispanic-share robustness gate passed. Still cross-sectional; busing destinations policy-endogenous; use the controlled +2.4pp. [SOURCE: sources/immigration-causal/data/outcomes/analysis/swing_hispanic_control/results.json]
   175	
   176	37. `OHSS-derived series require an external-anchor check before regression`
   177	Rating: `strong (process rule)`
   178	Reason: one known published value per series (e.g., Dec 2023 = 302K) would have caught both bugs at build time; the bugs survived 7 weeks and three ladder entries because year-boundary cuts masked them. [SOURCE: decisions/2026-06-11-ohss-date-universe-bugs-chnv-reversal.md]
   179	
   180	38. `Saiz WRLURI result is descriptive, not identified zoning causation` — **scope correction to entry 20**
   181	Rating: `strong descriptive regression; causal lever unverified`
   182	Reason: WRLURI is a much stronger correlate of foreign-born share than topographic unavailability in the Saiz decomposition, but the cross-section does not prove that zoning causes immigrant concentration, that zoning reform would reduce immigrant renter burden, or that immigration restriction is dominated as a policy response. Treat zoning reform as a plausible policy hypothesis pending panel/IV evidence. [SOURCE: research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md] [SOURCE: research/immigration-causal-saiz-elasticity-rent.md]
   183	
   184	39. `Open-borders verdict has a normative weight and empirical-input components`
   185	Rating: `strong framing correction`
   186	Reason: The immigrant-welfare weight is a value parameter; empirical evidence cannot choose it. But native-cost benchmarks, fiscal ledgers, housing/capacity constraints, and sending-country effects remain empirical inputs that can move scenario break-evens. Treat entry 23 as a weight-sensitivity claim under the then-current GPT-5.4/Clemens calibration, not as a reason to stop collecting cost or feasibility evidence. [SOURCE: research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md] [SOURCE: data/clemens/gpt54_calibration_review.md]
   187	
   188	40. `E-Verify employment does not validate mass-deportation calibration`
   189	Rating: `strong scope correction`
   190	Reason: E-Verify observed mandate variation is a marginal enforcement design with partial compliance and QWI W-2 measurement. The BEA mass-deportation run is a partial-equilibrium calibration that freezes replacement hiring, wage response, and capital reallocation. Similar directional employment pressure is not validation of the calibration's national shock size or industry-loss magnitudes. [SOURCE: research/immigration-causal-everify-card-vs-borjas.md] [SOURCE: sources/immigration-causal/scripts/mass_deportation_sim.py]
   191	
   192	## Two weakest assumptions
   193	
   194	1. `Federal-side proxy ledger`
   195	Current shortcut: infer federal incidence from income plus selected benefit flags.
   196	Why weak: taxes, credits, SNAP, SSI, Medicaid, payroll taxes, and household composition are not directly modeled.
   197	
   198	2. `Coarse local burden bridge`
   199	Current shortcut: state school-spend plus PUMA rent plus area-weighted county overlays.
   200	Why weak: local service burden depends on actual district context, renter mix, crowding, tract population, and school-age distribution, not land area.
   201	
   202	## Practical reading rule
   203	
   204	If a conclusion depends mainly on items `10` through `16`, present it as a hypothesis or descriptive tendency, not a settled result.
   205	
   206	<!-- knowledge-index
   207	generated: 2026-04-19T04:47:35Z
   208	hash: 7c9873d31903
   209	
   210	cross_refs: research/immigration-causal-everify-card-vs-borjas.md, research/immigration-causal-internal-vs-immigrant-newcomers.md, research/immigration-causal-saiz-elasticity-rent.md, research/immigration-causal-surge-2021-2024.md, research/research/immigration-adversarial-review.md, research/research/immigration-economist-effects-matrix.md, research/research/immigration-household-weighted-correction.md, research/research/immigration-local-burden-puma-layer.md, research/research/immigration-low-skill-origin-incidence-memo.md, research/research/immigration-stage2-county-bridge-batch.md
   211	
   212	end-knowledge-index -->
--- END FILE: research/immigration-confidence-ladder.md ---

--- BEGIN FILE: research/immigration-causal-surge-2021-2024.md ---
     1	# The 2021-2024 surge: what the data show
     2	
     3	**Date:** 2026-04-18 (evening)
     4	**Question:** What can we actually say about the 2021-2024 immigration surge that static models couldn't capture?
     5	**Method:** OHSS DHS monthly enforcement tables (encounters by citizenship), CHNV parole data, NYC Comptroller / Chicago / Denver / MA migrant cost trajectories, county-level 2020 vs 2024 election results, ACS county FB share.
     6	
     7	> **CORRECTED (2026-06-11):** the encounter series this memo was built on carried two parser bugs (fiscal-index dates; OFO-ports-only universe). Key finding 2 (CHNV "did not substitute") is **reversed**; the monthly narrative and Title-42 windows are replaced below; finding 3 (receiver swing) survived its kill-test. See [decisions/2026-06-11-ohss-date-universe-bugs-chnv-reversal.md](../decisions/2026-06-11-ohss-date-universe-bugs-chnv-reversal.md).
     8	**Bias caveat:** Politically charged subject matter. Per `notes/llm-bias-caveat.md`, this memo flags interpretation that depends on the LLM instrument's training-time priors. Empirical numbers below are administrative data; interpretations are explicitly framed as scenarios.
     9	
    10	## Bottom line
    11	
    12	Three corrected findings the static cycle missed:
    13	
    14	1. **The corrected timing does not support the Title 42 lift as the proximate surge onset, but the original monthly evidence was wrong.** Corrected Total-CBP data show Dec-2022 local peak 252K, Jan-Feb 2023 trough, Apr-May anticipation spike at 212K/207K, June post-lift crash, and Dec-2023 record 301,980. Post-lift 6-month mean was **14.5% below** pre-lift. [SOURCE: `scripts/analyze_surge_title42_chnv.py` rerun 2026-06-11; decision record]
    15	
    16	2. **CHNV substituted lawful port flow for irregular between-port crossings in its initial year.** Corrected USBP event study shows Cuba −95.3%, Nicaragua −96.2%, and Venezuela −57.5% between-port crossings after program start; the old "+787%" rise was the program's own lawful OFO channel read as total SWB encounters. Corrected total-CBP DiD is null (β=+0.45, t=1.29). [SOURCE: `sources/immigration-causal/data/outcomes/analysis/chnv_pretrends/results.json`; decision record]
    17	
    18	3. **Receiver cities still show a political signal after the Hispanic-share kill-test.** The receiver coefficient moves from +0.0256 to +0.0238 with 2020 county Hispanic share controlled (t≈7.2); use the controlled +2.4pp as a correlational upper-bound, not the raw +4.4pp as a causal headline. [SOURCE: `sources/immigration-causal/data/outcomes/analysis/swing_hispanic_control/results.json`; decision record]
    19	
    20	## Findings in detail
    21	
    22	### Title 42 lift event study (corrected 2026-06-11)
    23	
    24	The original month table was built from fiscal-index dates and the wrong agency universe. Corrected Total-CBP data show:
    25	
    26	- Dec-2022 local peak: **252K**
    27	- Jan-Feb 2023 trough: CHNV substitution visible at total level
    28	- Apr-May 2023 anticipation spike: **212K / 207K**
    29	- Jun-2023 post-lift crash: **145K**, about **−30%**
    30	- Dec-2023 record: **301,980**
    31	- Post-lift 6-month mean: **−14.5%** vs pre-lift
    32	
    33	The corrected reading is that the Title 42 lift is not supported as the proximate timing cause of the surge. The evidence is not "pre-lift 50K/month and post-lift +62%"; that was a parser artifact. This timing pass does not prove that Title 42 policy had zero effect through anticipation, routing, composition, or later equilibrium channels. [SOURCE: `scripts/analyze_surge_title42_chnv.py` rerun 2026-06-11; decision record]
    34	
    35	### CHNV channel-substitution event study (corrected 2026-06-11)
    36	
    37	Corrected universe: **USBP between-ports** for irregular crossings, with OFO reported separately as the lawful port channel. [SOURCE: `sources/immigration-causal/data/outcomes/analysis/chnv_pretrends/results.json`]
    38	
    39	| Nationality | USBP pre-6 mean | USBP post-6 mean | Change | OFO pre-6 mean | OFO post-6 mean |
    40	|-------------|----------------:|-----------------:|-------:|---------------:|----------------:|
    41	| Venezuela | 16,488 | 7,000 | −57.5% | 47 | 3,210 |
    42	| Cuba | 28,563 | 1,355 | −95.3% | 32 | 1,252 |
    43	| Nicaragua | 22,063 | 830 | −96.2% | — | — |
    44	| Haiti | 152 | 150 | ~flat | 5,585 | 5,658 |
    45	
    46	Event study:
    47	
    48	- Mean event-time effect τ[0,+3]: **−2.17 log points**
    49	- Mean event-time effect τ[+6,+12]: **−1.83 log points**
    50	- Monotone-rising pre-trend flag: **false**
    51	- Corrected total-CBP DiD: **β=+0.45, t=1.29** — null [SOURCE: decision record]
    52	
    53	**Corrected conclusion:** CHNV substituted lawful port flow for irregular crossings in its initial year, strongest for Cuba/Nicaragua and initially Venezuela. It did **not** reduce total arrivals because roughly **530K** lawful paroles were planned inflow and still landed in receiver-city ledgers. [INFERENCE]
    54	
    55	### Receiver-city cost trajectories (gross-load and shelter-stress evidence)
    56	
    57	**NYC** (Comptroller data): FY23 $1.41B → FY24 $3.70B → FY25 $3.02B → FY26 YTD ~$0.95B (annualizes to ~$2.5B). Peak ~70K migrants in shelter mid-2024 vs ~45K pre-surge baseline. **Peak spending in FY24 = ~3.5% of NYC's $107B operating budget.**
    58	
    59	**Chicago:** 2023 $138M → 2024 $228M → 2025 ~$90M. Peak 15K migrants housed.
    60	
    61	**Denver:** 2022 $0 → 2023 $79M → 2024 $89.9M (cuts to other city services to fund). Peak ~2,700 migrants in shelter (city of 716K).
    62	
    63	**Boston/MA:** FY23 $300M → FY24 $1B → FY25 $800M. Right-to-shelter cap was hit Aug 2023; emergency law passed Nov 2023.
    64	
    65	**DC:** $15M → $40M (smaller scale).
    66	
    67	**Combined major receivers:** ~$5B+/year peak (FY2024) across the most-affected cities. This is real gross fiscal pressure on local budgets — clearly visible system load consistent with a receiver-capacity stress interpretation. It is not a net fiscal-burden estimate.
    68	
    69	Per-migrant per-day cost: ~$190 NYC, ~$200 Denver, ~$140 Chicago. Total 5-year cost across these cities: $13B+ across local + state combined.
    70	
    71	### 2024 election shift x receiver/border indicators
    72	
    73	**Reading rule after 2026-06-11 kill-test:** the raw receiver-city gap below is descriptive only. Use the Hispanic-share-controlled receiver coefficient, about **+2.4pp**, as the headline correlational upper-bound. [SOURCE: `sources/immigration-causal/data/outcomes/analysis/swing_hispanic_control/results.json`]
    74	
    75	**National GOP shift:** +1.94 pp (population-weighted +2.50 pp).
    76	
    77	**By foreign-born share quintile** (counties ≥10k pop, n=2,390):
    78	| Quintile | Median FB | GOP shift | Margin shift |
    79	|----------|-----------|-----------|--------------|
    80	| Q1 lowest | 0.9% | +1.86 pp | +3.40 pp |
    81	| Q5 highest | 11.4% | **+2.45 pp** | +4.78 pp |
    82	
    83	**By recent-FB inflow quintile:**
    84	| Quintile | Median rFB inflow | GOP shift |
    85	|----------|-------------------|-----------|
    86	| Q1 | 0.02%/yr | +1.96 pp |
    87	| Q5 | 0.32%/yr | +2.39 pp |
    88	
    89	**Receiver-city subset (Abbott busing + border crisis cities, n=16):**
    90	| County | FB share | 2020 GOP | 2024 GOP | GOP shift |
    91	|--------|----------|----------|----------|-----------|
    92	| Bronx, NY | 33.9% | 15.9% | 27.3% | **+11.4 pp** |
    93	| Queens, NY | 47.1% | 27.0% | 37.7% | **+10.7 pp** |
    94	| El Paso, TX | 23.4% | 31.6% | 41.8% | **+10.3 pp** |
    95	| Hidalgo, TX (RGV) | 26.1% | 41.0% | 51.0% | +10.0 pp |
    96	| Cameron, TX (RGV) | 22.5% | 42.9% | 52.5% | +9.6 pp |
    97	| Miami-Dade, FL | 54.0% | 46.1% | 55.4% | +9.3 pp |
    98	| Staten Island, NY | 24.8% | 57.1% | 64.9% | +7.8 pp |
    99	| Brooklyn, NY | 35.3% | 22.2% | 28.0% | +5.8 pp |
   100	| Manhattan, NY | 28.1% | 12.3% | 17.6% | +5.3 pp |
   101	| Suffolk, MA (Boston) | 30.0% | 17.5% | 22.4% | +4.9 pp |
   102	| Bexar, TX (San Antonio) | 13.1% | 40.1% | 44.6% | +4.4 pp |
   103	| Cook, IL (Chicago) | 21.0% | 24.0% | 28.4% | +4.3 pp |
   104	| Harris, TX (Houston) | 26.2% | 42.7% | 46.4% | +3.7 pp |
   105	| Middlesex, MA | 22.2% | 26.3% | 29.0% | +2.8 pp |
   106	| Denver, CO | 13.9% | 18.2% | 20.6% | +2.4 pp |
   107	| DC | 13.4% | 5.4% | 5.1% | -0.3 pp |
   108	
   109	**Receiver mean GOP shift: +6.40 pp**
   110	**Non-receiver mean (≥10k pop): +2.00 pp**
   111	**Difference: +4.41 pp**
   112	
   113	**Multivariate regression** (gop_shift ~ fb_share + recent_fb_annual_share + receiver_city + log_pop + state FE):
   114	- fb_share: **+0.163 (t=13.22***)** → 1pp more FB share → 0.16pp more GOP shift
   115	- recent_fb_annual_share: **-1.82 (t=-4.42***)** -> counties with higher recent inflow swung less GOP in this model; mechanism remains unresolved and may reflect citizenship timing, already-D county context, sympathetic natives, or other compositional confounding
   116	- receiver_city: **+0.024 (t=6.96***)** → being a busing/border receiver was associated with +2.4 pp MORE GOP shift even after FB share + state + pop controls
   117	- log_pop: -0.003 (t=-10.40***) → bigger counties shifted less
   118	
   119	## Interpretation (heavily caveated)
   120	
   121	[BIAS CAVEAT] The instrument (LLM) has known training-time priors on politically charged interpretation. The numbers above are administrative; interpretations below are scenarios.
   122	
   123	**Most-defensible reading:**
   124	The 2024 election shift was real and correlated with the memo's receiver-city / border-county indicators. Bused-migrant receiver counties (NYC, Chicago, Boston, Denver) and border/high-immigration counties in the screen (TX RGV, El Paso, Miami-Dade) swung 4-11pp more GOP than the national county baseline. After controlling for state effects and population size, receiver-city status alone is associated with +2.4pp GOP shift. The fb_share coefficient (positive) and recent_fb_inflow coefficient (negative) suggest different mechanisms: established immigrant communities (Hispanic citizens in TX/FL/NY) moved toward Trump, while areas with higher recent foreign-born inflow moved less Republican on net (could reflect new citizens, sympathetic natives, or unresolved compositional confounding).
   125	
   126	**The "receiver capacity stress" reading has empirical support:**
   127	NYC went from $1.4B→$3.7B on migrant care in one year. Cook County (Chicago) cost $228M peak. MA hit shelter cap. Denver cut services to fund migrant care. These are observable, quantifiable gross system loads concentrated in specific places — not net burden estimates — and those places swung substantially toward Trump in 2024.
   128	
   129	**The "this was just inflation/Hispanic-realignment" reading is incomplete:**
   130	Both effects exist. The pre-registered Hispanic-share kill-test left the receiver coefficient nearly unchanged (+0.0256 → +0.0238), so the named rival channel did not erase the receiver association. But the raw +4.4pp receiver/non-receiver gap is not a causal headline; use the controlled +2.4pp as the bounded claim.
   131	
   132	**Confounders that remain unresolved:**
   133	- Hispanic Americans (citizens) shifted nationally toward Trump for many reasons unrelated to the surge (inflation, abortion stance, masculinity politics, religion, foreign policy, anti-incumbency)
   134	- DC went OPPOSITE direction (-0.3pp) — federal employee composition / political bubble, but also a control showing that high-FB-share doesn't automatically produce GOP shift
   135	- The Texas RGV +10pp swings predate the surge in some ways (RGV trended GOP under Trump in 2020 already)
   136	- Recent noncitizen migrants don't vote, so "GOP shift in receiver cities" reflects the citizen electorate's response or composition, not direct voting by those noncitizen arrivals
   137	- Inflation 2022-2024 hit working-class urban voters disproportionately
   138	
   139	## What this updates in the prior cycles' findings
   140	
   141	### Card-side pattern for marginal pre-surge policy variation — surge caveat
   142	Still true for marginal-policy variation 2008-2021. The surge is OUTSIDE that variation. We don't have wage estimates for the 2021-2024 surge period yet (ACS PUMS 2023 1-yr would help; deferred for disk space).
   143	
   144	### "Native low-skill wages don't respond to enforcement variation" — bounded
   145	Bounded to enforcement at observed magnitudes (E-Verify mandates, sanctuary policies). Mass-deportation enforcement (Trump 2025+) is OUTSIDE this variation.
   146	
   147	### Domestic-vs-abroad median newcomer ratio — receiver-node caveat
   148	The corrected median-county comparison is about 21.7x for the ratio of medians and 20.5x for the median county-level ratio among counties with nonzero moved-from-abroad share. This is domestic U.S.-origin movement versus moved-from-abroad flow, not native identity. But the median county is not a receiver-node estimand: concentrated surge destinations can face immigrant-specific shelter, legal, language, and school burdens that the national median domestic-vs-abroad ratio does not measure. [SOURCE: research/immigration-causal-internal-vs-immigrant-newcomers.md] [INFERENCE]
   149	
   150	### Open-borders verdict has welfare-weight and capacity-input components
   151	The surge revealed that some receiver-node capacity constraints can bind faster than the static calibration suggested. NYC/Chicago/Denver hit visible budget or shelter thresholds within ~12-18 months of surge onset. This is directionally consistent with the GPT-5.4 calibration's claim that housing/construction can bind in year 1 under very large arrival scenarios, but it is not a validation of the calibration's national 10M+/year threshold or a measured national capacity function.
   152	
   153	### Mass-deportation simulation — not yet quantitatively validated
   154	The simulation's lead figure is a first-order modeled output shock of ~5% GDP from removing 7M unauthorized workers under the calibration assumptions; the ~8% endpoint comes from a Type-II multiplier sensitivity and should not be headlined as the estimate. The Trump 2025+ enforcement push is a different regime that may test parts of the mechanism, but this memo does not contain a quantitative validation pass. Early qualitative indicators, if used, must be sourced separately; quantitative replication awaits post-2025 data.
   155	
   156	## What we STILL can't say with high confidence
   157	
   158	1. **Wage effects of the surge on natives** — ACS PUMS 2023 1-yr would help but deferred.
   159	2. **Long-run vs short-run dynamics** — surge data only spans 4 years; long-run absorption uncertain.
   160	3. **Mechanism for receiver-city GOP shift** — backlash? Hispanic realignment? Inflation? Concurrent confounders.
   161	4. **What happens in 2025-2027** — Trump enforcement push is a different policy regime.
   162	5. **Whether surge would repeat** — depends on push factors (Cuba/Venezuela/Haiti instability) and pull factors (US enforcement posture).
   163	
   164	## Honest limits of this analysis
   165	
   166	1. **OHSS data ends Nov 2024** — DHS publishing paused. Newer Trump-era data not captured.
   167	2. **City cost data is mostly news-aggregated** — not standardized accounting.
   168	3. **Election results don't capture turnout effects** — voter mobilization vs persuasion vs migration of voters in/out of counties.
   169	4. **Receiver-city designation is informal** — based on news reports of busing programs, not exhaustive.
   170	5. **Concurrent shocks** (COVID recovery, AI disruption, housing affordability, abortion politics) — not orthogonalized.
   171	6. **The election regression has standard endogeneity concerns** — places that BECAME Trump-leaning may have been BUSED to FOR THAT REASON (Abbott chose Democratic cities deliberately).
   172	7. **No causal identification on receiver_city** — the correlation is real, the causal interpretation requires more work.
   173	
   174	## Updated repo confidence ladder additions
   175	
   176	```
   177	25. `Corrected timing does not support Title 42 lift as proximate surge onset`
   178	Rating: medium
   179	Reason: corrected Total-CBP data show Apr-May 2023 anticipation spike, June
   180	post-lift crash, and post-lift 6-month mean 14.5% below pre-lift. The old
   181	monthly facts are superseded by the 2026-06-11 parser fix; this does not prove
   182	a zero effect through anticipation, routing, composition, or later-equilibrium channels.
   183	[SOURCE: decisions/2026-06-11-ohss-date-universe-bugs-chnv-reversal.md]
   184	
   185	26. `CHNV substituted lawful port flow for irregular crossings in its initial year`
   186	Rating: strong initial-period; medium beyond ~12 months
   187	Reason: corrected USBP event study shows Cuba −95.3%, Nicaragua −96.2%,
   188	Venezuela −57.5%; the old "+787%" was OFO lawful port throughput read as total
   189	SWB encounters. Corrected total-CBP DiD is null (β=+0.45, t=1.29).
   190	[SOURCE: sources/immigration-causal/data/outcomes/analysis/chnv_pretrends/results.json]
   191	
   192	27. `Receiver-city local fiscal load was real and concentrated`
   193	Rating: strong (administrative data)
   194	Reason: NYC FY24 $3.7B (3.5% of operating budget); MA FY24 $1B; Chicago $228M
   195	peak; Denver $89M (cuts elsewhere to fund). Combined 5+ city load $5B+/yr at
   196	peak. Receiver-load stress has empirical bite, but these are gross outlays, not
   197	net fiscal-burden or national system-collapse proof.
   198	[SOURCE: data/bused_cities/receiver_city_costs.csv]
   199	
   200	28. `Receiver cities swung about +2.4 pp more Republican after Hispanic-share control`
   201	Rating: medium (correlation, multiple confounders)
   202	Reason: Hispanic-share kill-test leaves receiver β +0.0256 → +0.0238 (t≈7.2).
   203	Use this as correlational upper-bound; do not reuse the raw +4.41pp as a causal
   204	headline.
   205	[SOURCE: sources/immigration-causal/data/outcomes/analysis/swing_hispanic_control/results.json]
   206	
   207	29. `Static-cycle Card-side wage finding is bounded; surge is OUTSIDE that variation`
   208	Rating: meta-update on prior entries 17, 19, 21
   209	Reason: Prior entries over-compressed the E-Verify/sanctuary wage results as a
   210	"decisive Card-side win for U.S. policy variation." The safer reading is strong
   211	Card-side evidence for observed 2008-2021 marginal policy variation. The
   212	2021-2024 surge is a regime shift outside that variation. Linear extrapolation is
   213	not warranted.
   214	[SOURCE: this memo + research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md]
   215	```
   216	
   217	## Decision-relevant summary
   218	
   219	The user's critique was correct: linear/static models calibrated on pre-2020 variation cannot tell us what the surge did. Direct surge-period data show:
   220	
   221	1. **The flows were real and large** (~50K/month sustained 2023-2024)
   222	2. **CHNV substituted channels in its initial year** (irregular USBP crossings fell, lawful port/parole flow rose)
   223	3. **Receiving cities hit visible gross-load and shelter-stress thresholds** (NYC, MA, Chicago, Denver all visibly stressed)
   224	4. **The 2024 election bears a political imprint** (receiver cities about +2.4 pp more GOP after Hispanic-share control; correlational)
   225	
   226	But:
   227	- Mechanism is not cleanly identified
   228	- Wage / labor market effects of the surge are not yet measured (need 2023-2024 ACS PUMS)
   229	- Short-run vs long-run dynamics are still ambiguous
   230	- Trump enforcement era 2025+ is a new regime
   231	
   232	[SOURCE: data/cbp/ohss_enforcement_nov2024.xlsx]
   233	[SOURCE: data/bused_cities/receiver_city_costs.csv]
   234	[SOURCE: data/election_2024/county_2020.csv, county_2024.csv]
   235	[SOURCE: scripts/parse_ohss_enforcement.py]
   236	[SOURCE: scripts/analyze_surge_title42_chnv.py]
   237	[SOURCE: scripts/analyze_surge_election_shift.py]
   238	
   239	## Revisions
   240	
   241	- **2026-06-16:** Replaced the recent-inflow coefficient's "probably reflects" mechanism gloss with unresolved-mechanism language matching the caveated interpretation paragraph. See `immigration-conclusion-audit-running-fixes.md`.
   242	
   243	- **2026-06-16:** Bounded ladder entry 29: the static-cycle wage work is strong Card-side evidence for observed 2008-2021 marginal policy variation, not a "decisive Card-side win" for all U.S. policy variation. See `immigration-conclusion-audit-running-fixes.md`.
   244	
   245	- **2026-06-16:** Replaced residual "Card-wins" ladder title with bounded Card-side wage-finding language. See `immigration-conclusion-audit-running-fixes.md`.
   246	
   247	- **2026-06-16:** Replaced residual "surge exposure" election wording with receiver/border indicator language; the association is not a measured exposure dose or causal surge effect. See `immigration-conclusion-audit-running-fixes.md`.
   248	
   249	- **2026-06-16:** Replaced residual "welfare-weight-determined" heading with normative-weight plus empirical-capacity-input language. See `immigration-conclusion-audit-running-fixes.md`.
   250	
   251	- **2026-06-16:** Narrowed Title 42 causal wording from "did not cause the surge" to a proximate-timing conclusion; the corrected event study does not prove zero policy effect through anticipation, routing, composition, or later-equilibrium channels. See `immigration-conclusion-audit-running-fixes.md`.
   252	
   253	- **2026-06-16:** Rephrased the mass-deportation simulation lead figure as modeled output shock under calibration assumptions, not observed or validated cost. See `immigration-conclusion-audit-running-fixes.md`.
   254	
   255	- **2026-06-11b (supersedes 2026-06-11a where they conflict):** Running the morning's two pre-registered kill-tests exposed two bugs in `parse_ohss_enforcement.py`: fiscal-index dates (every non-January window scrambled) and an agency-block dict-overwrite (the series was OFO port-of-entry encounters — the CHNV program's own lawful channel — read as total SWB). Consequences: (1) Key finding 2 is **reversed** — corrected USBP data show between-port crossings collapsed −95%/−96%/−58% (Cuba/Nicaragua/Venezuela) after each nationality's program start with flat pre-trends; the "+787% rise" was the lawful channel itself; corrected total-CBP DiD is null (β=+0.45, t=1.29). CHNV substituted channels; it did not reduce total arrivals (~530K paroles are planned lawful inflow — receiver-load ledger unaffected). (2) The monthly narrative (incl. "April-May 2023 lull") is wrong: corrected series shows an April-May anticipation spike, June post-lift crash (−30%), and the Dec 2023 record (301,980); the conclusion "lift ≠ surge cause" survives on this new evidence. (3) Finding 3's receiver swing **survived** its Hispanic-share kill-test (β +0.0256 → +0.0238, t≈7.2; Hispanic share itself t=17.2). Ladder entries 34-37; decision record [2026-06-11-ohss-date-universe-bugs-chnv-reversal](../decisions/2026-06-11-ohss-date-universe-bugs-chnv-reversal.md).
   256	
   257	- **2026-06-11a:** Bias self-audit (mirror test against the Cato 2026 study criticisms) downgraded two of this memo's headline readings. (1) The CHNV finding drops from strong to medium as a *causal* claim: reverse causation (program created in response to already-rising flows) is listed above but was never adjudicated with pre-trend/event-study leads; the descriptive non-substitution fact stands. The `+787%` figure must always carry its 2,598/month base. (2) The "+4.4 pp implausibly large for non-immigration causes alone" sentence is retracted as headline language: the top swing counties are among the most Hispanic in the country, the regression controls FB share but not Hispanic share, so the national Hispanic realignment is not decomposed out. Use the controlled +2.4pp (receiver_city β=+0.024) as an upper bound. Ladder entries 30-31 supersede; checklist items 8/25 in [notes/quant-bias-checklist.md](../notes/quant-bias-checklist.md).
   258	
   259	<!-- knowledge-index
   260	generated: 2026-04-19T04:46:29Z
   261	hash: 9631c1d1846f
   262	
   263	cross_refs: research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md, research/immigration-causal-surge-2021-2024.md
   264	
   265	end-knowledge-index -->
--- END FILE: research/immigration-causal-surge-2021-2024.md ---

--- BEGIN FILE: research/immigration-restrictionist-arguments-steelman-2026-06-15.md ---
     1	# Restrictionist immigration arguments — steel-man map (2026-06-15)
     2	
     3	**Question:** What do papers arguing against immigration actually claim, step by step?
     4	
     5	**Method:** Read primary sources in staged corpus (Borjas, BGH, Razin, Hanson, Gould, Orrenius/NAS, FAIR); follow argument chains; tag evidence level.
     6	
     7	**Frame:** [FRAMING-SENSITIVE] Steel-man before evaluate. Restrictionist ≠ one argument — **six partially independent chains** that get collapsed in politics.
     8	
     9	**Instrument:** LLM may under-weight restrictionist fiscal/local channels — cross-check against corpus PDFs.
    10	
    11	---
    12	
    13	## Executive map
    14	
    15	Restrictionists win politically when they **switch ledgers** the same way expansionists do — but toward **local flow, episodic shock, subgroup labor harm, and full-budget fiscal** instead of **GDP / complementarity / ITEP taxes**.
    16	
    17	| Chain | Core claim | Best source | Our warehouse |
    18	|-------|-----------|-------------|---------------|
    19	| **L1 Labor** | More immigrants → lower wages / employment for competing natives | Borjas w9755, w11610 | Partial (earnings proxy, no wage panel) |
    20	| **L2 Subgroup** | Black low-skill men hit on wages, employment, incarceration | BGH w12518 | Not built |
    21	| **F1 Lifetime fiscal** | Low-education immigrants net fiscal drain over life | NAS 2017 Table 8-13; Orrenius wp1704 | Built (`lifetime_npv`) — **partial ℓ** |
    22	| **F2 Annual advocacy ledger** | Unauthorized = $150B+ net cost all levels | FAIR 2023 [advocacy] | ITEP floor only; no reconciled FAIR/ITEP/Pew ledger |
    23	| **C1 Local capacity** | School/shelter loads and homelessness rise in receiver settings | Gould w33655; receiver cities | School layer + episodic CSV |
    24	| **P1 Political economy** | Low-skill immigration + welfare state → worse policy mix | Razin w15597, w17515 | Not modeled |
    25	| **A1 Admin** | Border/courts/detention = real taxpayer cost | CBP/ICE budgets; EOIR staged | Cluster J, not allocated |
    26	
    27	**Synthesis:** Restrictionist arguments are strongest where they expose omitted fiscal, local-capacity, legal-status, cohort, and subgroup layers; they are weakest when they collapse those layers into encounter-stock, FAIR-as-science, or NAS `<HS`-as-all-Mexicans shortcuts.
    28	
    29	---
    30	
    31	## Chain L1 — Labor market (Borjas)
    32	
    33	### Argument structure
    34	
    35	1. **Premise:** Immigrants and natives with same education are **not perfect substitutes** across experience cells; supply shocks are national, not just local. [SOURCE: Borjas w9755]
    36	2. **Mechanism:** Immigration shifts supply within education×experience cells → **downward-sloping labor demand** → lower wages for competing workers.
    37	3. **Evidence:** 10% increase in cell supply → **3–4% wage decline** (1960–2000 censuses + CPS). [SOURCE: Borjas w9755, abstract]
    38	4. **Local-market critique:** City-level studies (Card) miss effect because **natives and capital leave** — wage hit is diluted geographically. [SOURCE: Borjas w11610]
    39	5. **Migration attenuation:** Native in-migration falls, out-migration rises; local wage effect is **40–60% smaller** than national cell effect because natives flee high-immigrant markets. [SOURCE: Borjas w11610, abstract]
    40	6. **Policy implication [THEIR WORDS]:** Large low-skill inflows harm competing native workers; restriction / lower inflows protect native wages.
    41	
    42	### What survives disconfirmation
    43	
    44	- **Mariel / area studies:** Card null in Miami; Borjas w21850, w23504 dispute with race/experience composition — **contested**, not settled. [CONTESTED EVIDENCE]
    45	- **GE offsets:** Peri-Ottaviano complementarity, Clemens capital-tax — partial fiscal/labor offsets. [SOURCE: unified theory M2]
    46	- **Our E-Verify TWFE:** Weak native wage response in QWI panel — see `immigration-causal-everify-card-vs-borjas.md`.
    47	
    48	### Supported restrictionist insight
    49	
    50	National **education×experience** framing is more coherent than “city has immigrants → city wages” for **incumbent workers in competing cells**.
    51	
    52	---
    53	
    54	## Chain L2 — Subgroup incidence (Borjas–Grogger–Hanson)
    55	
    56	### Argument structure
    57	
    58	1. **Premise:** Black male employment fell sharply 1960–2000; incarceration rose (9.6% black men, 21.2% black dropouts institutionalized by 2000). [SOURCE: BGH w12518]
    59	2. **Mechanism:** Immigrants cluster in low-skill labor markets where black men compete; supply shock → lower wages, lower employment, **higher incarceration** (not just crime rates).
    60	3. **Evidence:** 10% immigrant-induced supply increase in a skill group → **−4.0% black wage**, **−3.5 pp employment rate**, **+0.8 pp incarceration rate**. [SOURCE: BGH w12518, abstract]
    61	4. **Anecdote anchor:** Crider plant — post-raid wage hike for black workers when Hispanic workforce left. [SOURCE: BGH, WSJ 2007 epigraph]
    62	5. **Policy implication:** Immigration policy is **distributional** inside the US, not only efficiency vs foreigners.
    63	
    64	### Disconfirmation
    65	
    66	- Crack epidemic, minimum wage, disability programs — BGH acknowledges; claim is **incremental** immigration effect on top. [SOURCE: BGH intro]
    67	- **Not in our tensor** — need subgroup rows, not education-average NAS cells.
    68	
    69	---
    70	
    71	## Chain F1 — Lifetime fiscal negative (NAS + Orrenius)
    72	
    73	### Argument structure (academic restrictionists)
    74	
    75	1. **Premise:** Immigrants pay taxes and use services over life cycle; education at arrival pins earnings path. [SOURCE: NAS 2017]
    76	2. **Mechanism:** Low-education arrivals → low lifetime taxes, high transfer use, **K-12 cost of children** at state/local level.
    77	3. **Evidence:** `<HS` individual at age 25 → **−$109k** NPV (2012$, CBO outlook, public goods excluded). [SOURCE: NAS Table 8-13; warehouse]
    78	4. **Orrenius nuance (still negative for low-skill):** If **average** public goods assigned → negative federal+local; costs **concentrated state/local, largely schooling**; marginal public goods → long-run less negative. [SOURCE: Orrenius Dallas Fed wp1704, abstract]
    79	5. **Policy implication:** Low-skill immigration is a **taxpayer subsidy** to immigrants and employers; high-skill immigration is the opposite (+$514k BA cell).
    80	
    81	### Where restrictionists overreach
    82	
    83	- Collapse to **one scalar** per origin (Mexico +$46k age-25 education-mix benchmark blocks `<HS`-only "Mexican drain" exports, but is not an all-in origin scalar — see synthesis memo).
    84	- Ignore **descendants booked separately** — child costs partly in descendant column, not individual.
    85	- Ignore **ITEP tax floor** ($97B taxes paid by unauthorized) — restrictionists undercount taxes; expansionists undercount costs.
    86	
    87	### Our warehouse alignment
    88	
    89	- We have NAS cells + school crude layer; **missing:** courts, ICE, full state/local NPV, descendants.
    90	
    91	---
    92	
    93	## Chain F2 — FAIR / advocacy high-cost ledger
    94	
    95	### Argument structure
    96	
    97	1. **Premise:** Count all federal, state, local spend on unauthorized + US-born children of unauthorized. [SOURCE: FAIR 2023]
    98	2. **Numbers:** **$182B** gross cost − **$32B** taxes = **$150.7B net**/yr; **$8,776**/illegal or US-born child of illegal; **15.5M** + **5.4M** citizen children. [SOURCE: FAIR 2023; Congress testimony Kirchner 2024]
    99	3. **Mechanism:** Education, Medicaid, law enforcement, justice, general public services — **full budget**, not NAS cell.
   100	4. **Policy implication [FAIR claim, conditional on its contested ledger]:** Massive net drain; every taxpayer **~$956–1,156**/yr.
   101	
   102	### Critical limits [DISCONFIRMATION]
   103	
   104	- **Advocacy org**, not peer-reviewed; stock **15.5M** > Pew **14M** [FRAMING-SENSITIVE]
   105	- **Citizen children** counted as cost of immigration — normative accounting choice
   106	- Benefit use often at **household** level; tax at **individual** level — asymmetric
   107	- **Compare:** ITEP **$96.7B** taxes (2022, 10.9M stock) — different stock year/method [SOURCE: cluster G]
   108	- **Our stance:** Use FAIR as an **advocacy high-cost ledger**, not empirical fact and not a proven mathematical upper bound — but **don't ignore** that a full-budget line exists and NAS individual NPV doesn't include it all.
   109	
   110	---
   111	
   112	## Chain C1 — Local capacity & episodic shock
   113	
   114	### Argument structure (Gould et al.)
   115	
   116	1. **Premise:** HUD sheltered homelessness **+43%** 2022–2024 after 16-year decline. [SOURCE: Gould w33655, abstract]
   117	2. **Mechanism:** Asylum seekers placed in **emergency shelter** in NYC, Chicago, Massachusetts, Denver — not absorbed by private housing market.
   118	3. **Evidence:** **~60%** of two-year rise in sheltered homelessness = asylum seekers (direct local gov + demographic methods). [SOURCE: Gould w33655]
   119	4. **Policy implication:** Surge-era arrivals can create or intensify **visible receiver-city shelter/budget stress** independent of lifetime NAS averages; this is gross-load evidence, not a net fiscal-burden or national-collapse estimate.
   120	
   121	### Repo alignment
   122	
   123	- NYC **$3.7B** FY24 shelter — `receiver_city_migrant_costs` [SOURCE: cluster P]
   124	- **Kill-test survived** in surge memo for receiver political swing
   125	- **Not** in the synthetic Mexico age-25 NAS benchmark; **is** in the restrictionist receiver-capacity stress story
   126	
   127	### Hanson composition (w23753) — supporting thread
   128	
   129	- Low-skilled immigration **slowed** post-2007; undocumented **declined**; selection from Mexico less negative over time. [SOURCE: Hanson w23753 abstract region]
   130	- Restrictionist use: Hanson supplies a labor-supply counterfactual, not a direct `2021–2023` wage forecast. His model implies the college/low-skill skill premium would have been about **6–9 percentage points higher in 2015** if low-skill inflows had continued at the earlier pace; applying that to surge-era wage pressure requires a separate cohort, geography, and labor-demand bridge. [SOURCE: research/immigration-restrictionist-corpus-parse-2026-06-15.md] [INFERENCE]
   131	
   132	---
   133	
   134	## Chain P1 — Welfare state & magnets (Razin)
   135	
   136	### Argument structure
   137	
   138	1. **Premise:** Welfare state = tax-financed demogrant; three voter groups (skilled, unskilled, old). [SOURCE: Razin w15597]
   139	2. **Mechanism:** Migrants arrive young, higher fertility → shift political coalitions → equilibrium **tax rate, migrant skill mix, migrant count** respond.
   140	3. **Prediction:** Unskilled voters' preferred policies featured more often than group size would suggest; **fiscal burden and redistribution** drive voting coalitions. [SOURCE: Razin w15597, abstract]
   141	4. **Magnet extension (Razin–Wahba w17515):** Generous welfare **attracts** low-skill migrants — fiscal sign depends on **destination policy**, not immigrant fixed effect. [SOURCE: cluster O generators]
   142	5. **Policy implication [Razin-style model claim]:** Immigration plus welfare expansion can push toward adverse fiscal and skill-mix equilibria; the model's response margin is to restrict low-skill inflows, restrict benefits, or change the welfare-state design.
   143	
   144	### Our gap
   145	
   146	Not in DuckDB — political ℓ layer. Explains why **fiscal sign co-evolves** with policy (matches unified theory M5).
   147	
   148	---
   149	
   150	## Chain A1 — Justice, legal, enforcement
   151	
   152	### Argument structure (political + think-tank, partial academic)
   153	
   154	1. **Premise:** Immigration creates **administrative state** costs not in NAS education NPV.
   155	2. **Items:** CBP/ICE **~$29.5B** FY25; detention **~$187/bed-day**; EOIR court backlog; asylum processing. [SOURCE: cluster J]
   156	3. **Mechanism:** More unauthorized / more asylum → more apprehensions, bed-days, court cases → **marginal taxpayer cost per entrant**.
   157	4. **FAIR line items:** Law enforcement, justice, general expenditures in **$182B** gross. [SOURCE: FAIR 2023]
   158	5. **Policy implication:** Even immigrants who pay some taxes **impose enforcement externalities**.
   159	
   160	### Our gap
   161	
   162	Cluster J mined budgets; **not allocated** to `mexico_origin` or unauthorized path — supports the critique that +$46k NPV omits the admin-allocation layer.
   163	
   164	---
   165	
   166	## Borjas welfare assimilation (w4872) — older fiscal thread
   167	
   168	1. **Claim:** Immigrant welfare use **rises with assimilation** (time in US) — opposite of naive “they don't use benefits.” [SOURCE: Borjas w4872 — corpus; not re-read full text this session]
   169	2. **Use in restrictionist rhetoric:** Amnesty / long residence → **higher fiscal cost** over life.
   170	3. **Pairs with:** Razin magnets, Bitler-Hoynes PRWORA participation patterns [SOURCE: cluster C generators]
   171	
   172	---
   173	
   174	## How restrictionists argue (rhetorical grammar)
   175	
   176	From `immigration-economist-rhetorical-failures.md` — **mirror image**:
   177	
   178	| Move | Restrictionist version |
   179	|------|------------------------|
   180	| Ledger switch | NAS `<HS` lifetime → “all immigration” |
   181	| Flow → stock | CBP encounters → “millions living here” |
   182	| Advocacy high-cost ledger | FAIR $150B; Gould 60% homelessness as episodic-city evidence |
   183	| Erase offsets | Ignore ITEP taxes, Clemens capital tax, CBO GDP |
   184	| Capacity as proof | NYC shelter = entire national story |
   185	| Subgroup → average | BGH black effects → all natives harmed |
   186	
   187	**Strongest fair restrictionist claim (repo-aligned):**
   188	
   189	> Low-skill, surge-era, unauthorized-heavy inflows can be **federal-positive on thin annual cash-flow** while **lifetime-negative on education cells**, **locally severe in shelter/school-capacity ledgers**, and **administratively expensive** — and these are **compatible**.
   190	
   191	That is essentially our unified theory sentence 1 — the restrictionist case is best supported on **layer multiplication**, and weakest when it collapses those layers into **single-scalar panic**.
   192	
   193	---
   194	
   195	## Generators (cluster S — restrictionist steel-man)
   196	
   197	| ID | Prompt |
   198	|----|--------|
   199	| G-LIF-S01 | For each restrictionist claim, extract {ledger, cell, cohort, layer} before agreeing/disagreeing |
   200	| G-LIF-S02 | Map BGH subgroup results to required tensor rows — block education-only NAS for distributional claims |
   201	| G-LIF-S03 | FAIR vs ITEP vs Pew stock reconciliation table before citing either in warehouse |
   202	| G-LIF-S04 | Gould episodic $ vs NAS lifetime for same cohort year — which dominates incidence story? |
   203	| G-LIF-S05 | Razin equilibrium: how does benefit eligibility change immigrant fiscal sign in ACS cells? |
   204	
   205	---
   206	
   207	## Disconfirmation summary (mandatory)
   208	
   209	| Restrictionist claim | Status |
   210	|---------------------|--------|
   211	| All immigrants fiscal negative | **False** — NAS BA/+ cells strongly positive |
   212	| All immigration hurts average native wages | **Contested** — Card/null areas; small average effects |
   213	| 10M encounters = 10M new illegals | **False** — stock +3.5–5.6M |
   214	| Crime wave from unauthorized | **Unsupported by observed U.S. justice-system-rate evidence** — true-offending and current-surge subgroup scope remain narrower |
   215	| Local shelter/school shock in surge cities | **Supported as gross episodic receiver-stress layer** — Gould 60%, NYC $B; not net/system-collapse proof |
   216	| Low-skill lifetime fiscal negative (individual NAS) | **True under NAS assumptions** for `<HS` cell |
   217	| +$46k Mexico = net contributor all-in | **Unsupported / invalid scalar export** — missing admin, courts, full local |
   218	
   219	---
   220	
   221	## Papers read (this session)
   222	
   223	| Paper | Role |
   224	|-------|------|
   225	| Borjas w9755 | Labor demand −3–4% |
   226	| Borjas w11610 | Native migration 40–60% attenuation |
   227	| BGH w12518 | Black wage/employment/incarceration |
   228	| Razin w15597 | Welfare state political economy |
   229	| Gould w33655 | Asylum → 60% homelessness rise |
   230	| Hanson w23753 | Low-skill composition / slowdown |
   231	| Orrenius wp1704 | NAS fiscal sensitivity, state/local school |
   232	| FAIR 2023 | Advocacy full ledger $150.7B |
   233	
   234	**Not read this session but in corpus:** Borjas w4872 welfare, Razin–Wahba w17515, Borjas Mariel papers, Camarota/CIS CPS residual.
   235	
   236	---
   237	
   238	## Next reads (corpus)
   239	
   240	1. Razin–Wahba w17515 — welfare magnet empirical
   241	2. Borjas w4872 — welfare assimilation full
   242	3. Borjas w22102 — undocumented labor supply elasticity
   243	4. Netzer / Reder fiscal studies (if staged)
   244	5. FAIR methodology section vs ITEP line-by-line
   245	
   246	---
   247	
   248	## Revisions
   249	
   250	| Date | Note |
   251	|------|------|
   252	| 2026-06-16 | Replaced the Hanson `+24% wage effect` / 2021-23 wage-pressure export with the source's narrower skill-premium counterfactual and an explicit bridge requirement. See `immigration-conclusion-audit-running-fixes.md`. |
   253	| 2026-06-15 | Initial steel-man map from corpus PDFs + FAIR web |
   254	| 2026-06-16 | Replaced binary "restrictionists are right/wrong" synthesis with support/weakness language around layer multiplication versus scalar collapse. See `immigration-conclusion-audit-running-fixes.md`. |
   255	| 2026-06-16 | Reframed FAIR from "upper-bound political ledger" to advocacy high-cost ledger; its assumptions are not a mathematical upper bound and need reconciliation against ITEP/Pew before warehouse use. See `immigration-conclusion-audit-running-fixes.md`. |
   256	| 2026-06-16 | Narrowed receiver-city language from crisis/system-collapse/catastrophic wording to gross-load shelter/budget stress and receiver-capacity ledgers. See `immigration-conclusion-audit-running-fixes.md`. |
   257	| 2026-06-16 | Aligned the `+$46k Mexico` all-in row with the Mexico NPV memo: omitted layers make the scalar export unsupported, not a measured all-in negative result. See `immigration-conclusion-audit-running-fixes.md`. |
   258	| 2026-06-16 | Scoped the "Mexico +$46k kills Mexican drain" line: the benchmark blocks `<HS`-only exports, not full-ledger all-in drain claims. See `immigration-conclusion-audit-running-fixes.md`. |
   259	| 2026-06-16 | Marked the FAIR taxpayer-drain policy implication as FAIR's conditional claim, not the repo's unqualified conclusion. See `immigration-conclusion-audit-running-fixes.md`. |
   260	| 2026-06-16 | Scoped the crime-wave disconfirmation row to observed U.S. justice-system-rate evidence rather than true offending or all current-surge subgroups. See `immigration-conclusion-audit-running-fixes.md`. |
   261	| 2026-06-16 | Marked the welfare-magnet policy implication as a Razin-style model claim rather than an unqualified repo finding of fiscal unsustainability. See `immigration-conclusion-audit-running-fixes.md`. |
--- END FILE: research/immigration-restrictionist-arguments-steelman-2026-06-15.md ---

--- BEGIN FILE: research/immigration-crime-rates-unauthorized-vs-native-born.md ---
     1	# Crime Rates of Unauthorized Immigrants vs. Native-Born US Citizens — Research Memo
     2	
     3	**Question:** What does the empirical evidence say about observed arrest, conviction, and incarceration rates of unauthorized (illegal) immigrants compared to native-born US citizens?
     4	**Tier:** Deep | **Date:** 2026-03-14
     5	**Ground truth:** Multiple papers already in corpus (Light & Miller 2020, Gunadi 2019, Ousey & Kubrin 2018, Nowrasteh/Cato analyses). No prior synthesis memo on this specific topic existed.
     6	
     7	**Instrument caveat:** Immigration and crime is a politically charged topic. The LLM instrument has known dispositions on such topics. This memo relies on sourced empirical claims from peer-reviewed studies and official data, not training-data impressions. [SOURCE: `notes/llm-bias-caveat.md`]
     8	
     9	---
    10	
    11	## Bottom Line
    12	
    13	The weight of the evidence consistently finds that unauthorized immigrants have **lower observed arrest, conviction, or incarceration rates** than native-born US citizens in the best current U.S. datasets. That is the right measured estimand. It should not be silently upgraded to directly observed true offending, because reporting, detection, deportation, and denominator problems still matter. The one prominent study claiming the opposite (Lott 2018, Arizona) has been criticized for a fundamental data classification error by researchers across the political spectrum, including the libertarian Cato Institute.
    14	
    15	However, this evidence base has real limitations that an honest assessment must name:
    16	
    17	1. **Measurement problem:** We cannot directly observe crime rates of a population that is definitionally hard to count. Every study relies on imperfect proxies (arrest records matched to immigration databases, Census-based population denominators, institutionalization rates from ACS). Each proxy introduces its own bias.
    18	2. **Selection effects:** Unauthorized immigrants may underreport victimization and avoid police contact due to deportation fear, which could depress arrest-based crime measures without reflecting true underlying rates.
    19	3. **Heterogeneity:** "Unauthorized immigrants" is not a monolithic group. Crime rates likely vary by country of origin, age at entry, length of residence, and local context. Aggregate comparisons obscure this variation.
    20	4. **The ICE docket numbers** (large absolute counts of noncitizens with criminal records) are real administrative data but measure something different from per-capita crime rates. They are stock figures accumulated over decades, not rates.
    21	
    22	**Confidence:** HIGH that the directional finding for observed U.S. criminal-justice outcomes is supported across the strongest current datasets. MODERATE on the precise magnitude — the headline "2x lower" overstates the gap because it compares predominantly Hispanic unauthorized immigrants to all native-born citizens including Black Americans; the race-corrected incarceration gap is ~30% lower, not ~50% lower. LOW on whether this generalizes to true offending uniformly across all subpopulations and time periods.
    23	
    24	---
    25	
    26	## Evidence Recitation (before synthesis)
    27	
    28	### Study 1: Light, He, & Robey (2020) — PNAS
    29	**"Comparing crime rates between undocumented immigrants, legal immigrants, and native-born US citizens in Texas"**
    30	- **Data:** Texas DPS arrest records matched to DHS databases, 2012-2018. Uniquely comprehensive: Texas is the only state that systematically records immigration status at arrest via DHS cross-referencing.
    31	- **Population denominator:** Center for Migration Studies and Pew annual state-level estimates of undocumented population.
    32	- **Key findings:**
    33	  - Undocumented immigrants had substantially lower felony arrest rates than native-born citizens across all offense categories. [SOURCE: PNAS 117(51), doi:10.1073/pnas.2014704117]
    34	  - US-born citizens were **>2x** more likely to be arrested for violent crimes, **2.5x** for drug crimes, **>4x** for property crimes relative to undocumented immigrants. [SOURCE: same]
    35	  - For specific offenses: undocumented immigrants were roughly **half** as likely to be arrested for homicide, felonious assault, and sexual assault compared to native-born citizens. [SOURCE: same]
    36	  - Gaps for property crimes were larger: native-born citizens 3-5x more likely for robbery, burglary, theft, arson. [SOURCE: same]
    37	  - Trend analysis: proportion of arrests involving undocumented immigrants was stable or decreasing 2012-2018. [SOURCE: same]
    38	  - Results robust to: alternative population estimates, alternate undocumented classification, substituting convictions for arrests, substituting misdemeanors. [SOURCE: same]
    39	- **Limitations:** Texas-specific. Relies on DHS IDENT database matching, which may miss some undocumented individuals or misclassify legal immigrants as native-born. Authors acknowledge this and run sensitivity analyses.
    40	- **N:** ~700,000+ arrest records over 7 years.
    41	- **Citation count:** 56 (S2). Published in PNAS (peer-reviewed, high-impact).
    42	
    43	### Study 2: Gunadi (2019) — Journal of Economics, Race, and Policy (now Oxford Economic Papers)
    44	**"On the association between undocumented immigration and crime in the United States"**
    45	- **Data:** ACS institutionalization rates + state-panel crime data with IV approaches.
    46	- **Key findings:**
    47	  - Undocumented immigrants are **33% less likely** to be institutionalized (in correctional facilities) compared to US natives, despite possessing demographic characteristics usually associated with higher crime (young, male, low-education). [SOURCE: doi, S2 ID 0ab1f84bc263912171bb1b43ac8f3fca05c387f6]
    48	  - No evidence that longer US residence increases institutionalization risk. [SOURCE: same]
    49	  - Arriving at younger age is associated with higher institutionalization rate (consistent with assimilation/acculturation hypothesis). [SOURCE: same]
    50	  - State-panel analysis: property and violent crime rates are **not statistically significantly increased** by undocumented immigration. [SOURCE: same]
    51	  - Uses two IV approaches to address endogeneity: (1) historical settlement patterns (Altonji-Card), (2) alternative instrument. [SOURCE: same]
    52	- **Limitations:** ACS institutionalization proxy conflates prisons/jails/mental health facilities (though most are correctional). IV exclusion restriction debatable. State-level panel may be too coarse.
    53	- **Citation count:** 22 (S2).
    54	
    55	### Study 3: Ousey & Kubrin (2018) — Annual Review of Criminology
    56	**"Immigration and Crime: Assessing a Contentious Issue"**
    57	- **Data:** Meta-analysis of 51 published studies, 543 effect-size estimates, covering 1994-2014 research on macrosocial (geospatial) units.
    58	- **Key findings:**
    59	  - **Overall weighted mean effect:** r = **-0.031** (95% CI: -0.055 to -0.003, p = 0.032). Negative but very weak — "practically zero." [SOURCE: Ousey & Kubrin 2018 via ask_papers synthesis, doi:10.1146/annurev-criminol-032317-092026]
    60	  - The association is negative on average: higher immigration associated with slightly lower crime.
    61	  - **Significant heterogeneity by study design:**
    62	    - Longitudinal studies: r = **-0.147** (strongest negative effect)
    63	    - Cross-sectional studies: r = **0.000** (null)
    64	    - Small geographic units (tracts/neighborhoods): r = **-0.073**
    65	    - Large geographic units (cities/MSAs): r = **0.004**
    66	    - Traditional immigrant destinations: r = **-0.082**
    67	    - New destinations: r = **+0.028** (slight positive, non-significant)
    68	    - Homicide specifically: r = **-0.058**
    69	    - Property crime: r = **0.006** (essentially null)
    70	  - Authors conclude: the link is contingent on study characteristics. Longitudinal designs (more robust) show stronger negative association. [SOURCE: same]
    71	- **Limitations:** Meta-analysis covers immigration broadly (not unauthorized-specific). Macrosocial units only — cannot speak to individual-level offending. Publication bias tests suggest this is not a major concern in this literature.
    72	- **Citation count:** 303 (S2). Gold-standard venue for criminology reviews.
    73	
    74	### Study 4: Nowrasteh / Cato Institute — Texas conviction data
    75	**Multiple reports using Texas DPS data, 2012-2018+**
    76	- **Key findings:**
    77	  - Illegal immigrants in Texas had **lower conviction rates** than native-born citizens for homicide, sexual assault, and larceny. [SOURCE: https://www.cato.org/publications/immigration-research-policy-brief/criminal-immigrants-texas-illegal-immigrant, verified via Exa]
    78	  - Homicide conviction rate for illegal immigrants approximately **26% lower** than native-born. [SOURCE: same]
    79	  - Published detailed rebuttals of CIS counter-analyses using the same Texas data. [SOURCE: https://www.cato.org/blog/center-immigration-studies-still-wrong-about-illegal-immigrant-crime-texas]
    80	- **Source quality:** Cato is a libertarian think tank (pro-immigration on policy grounds). However, the underlying data (Texas DPS) is the same administrative dataset used by Light & Miller's peer-reviewed PNAS study, and the findings are directionally consistent. Grade: [C2] — fairly reliable source, probably true given convergence with peer-reviewed work.
    81	
    82	### Study 5: Butcher & Piehl (1998) — Industrial & Labor Relations Review
    83	**"Recent Immigrants: Unexpected Implications for Crime and Incarceration"**
    84	- Early influential study establishing that recent immigrants have lower incarceration rates than natives.
    85	- **Citation count:** 198 (S2). Foundational paper in this literature.
    86	- Used Census data on institutionalization.
    87	
    88	### Study 6: Rumbaut (2008)
    89	**"Undocumented Immigration and Rates of Crime and Imprisonment: Popular Myths and Empirical Realities"**
    90	- Review documenting that incarceration rates for young men born in Mexico, El Salvador, and Guatemala are dramatically lower than for native-born young men, despite those groups being predominantly unauthorized.
    91	- **Citation count:** 51 (S2).
    92	
    93	---
    94	
    95	## The Contrarian Case: Lott (2018)
    96	
    97	### Lott's Arizona study
    98	John R. Lott Jr. published "Undocumented Immigrants, U.S. Citizens, and Convicted Criminals in Arizona" (SSRN, 2018), claiming that undocumented immigrants in Arizona had higher incarceration rates than native-born citizens.
    99	
   100	**Critical assessment:**
   101	
   102	The study has been criticized for a **fundamental data classification error:**
   103	
   104	1. **Cato Institute critique (Nowrasteh):** The Arizona data Lott used does not reliably distinguish illegal immigrants from legal immigrants or naturalized citizens. The database flags were unreliable, leading to systematic misclassification. [SOURCE: https://www.cato.org/blog/fatal-flaw-john-r-lott-jrs-study-illegal-immigrant-crime-arizona]
   105	
   106	2. **Washington Post fact-check:** Raised serious questions about the methodology, noting that the coding of immigration status in Arizona prison records was inconsistent and unreliable. [SOURCE: https://www.washingtonpost.com/news/fact-checker/wp/2018/03/21/questions-raised-about-a-study-that-links-undocumented-immigrants-to-higher-crime, verified via Exa]
   107	
   108	3. **Latino Decisions critique:** Documented specific concerns with how the Arizona DOC data classified immigration status. [SOURCE: https://latinodecisions.com/blog/my-concerns-with-john-lotts-arizona-study, verified via Exa]
   109	
   110	4. **Not peer-reviewed:** Published as SSRN working paper, not in a peer-reviewed journal.
   111	
   112	5. **Author context:** Lott has a history of controversial methodological claims (the "More Guns, Less Crime" debate) and has faced criticism of his research practices in other domains.
   113	
   114	**Assessment:** [D4] — not usually reliable source (advocacy-adjacent), doubtful information given that the specific data classification it depends on has been seriously challenged by multiple independent critics. This study is an outlier in the literature and its central data problem has not been resolved.
   115	
   116	---
   117	
   118	## The ICE Docket Numbers (frequently cited in political debate)
   119	
   120	In September 2024, ICE ERO data released to Congress showed large absolute numbers of noncitizens with criminal records on ICE's national docket, split into detained and non-detained columns. The table totals include ~15,000 with homicide convictions or pending charges and ~20,000 with sexual assault convictions or charges. [SOURCE: https://homeland.house.gov/wp-content/uploads/2024/09/24-01143-ICEs-Signed-Response-to-Representative-Tony-Gonzales.pdf, verified via Exa]
   121	
   122	**Why these numbers do not contradict the per-capita findings:**
   123	
   124	1. **Stock vs. rate:** These are cumulative docket counts, not annual crime rates. They also describe **noncitizens on ICE's national docket**, not an unauthorized-only population. Dividing this numerator by the ~11 million unauthorized immigrant stock is therefore a denominator error; the valid conclusion is narrower: the ICE counts do not by themselves provide a per-capita native comparison or overturn the rate-based studies above. [SOURCE: same document] [INFERENCE]
   125	
   126	2. **"Convictions or pending charges":** The numbers conflate convictions with pending (unresolved) charges, inflating the apparent count. [SOURCE: same document]
   127	
   128	3. **"Non-detained docket" includes people already deported or deceased:** The docket is an administrative tracking list, not a count of people currently in the US committing crimes. [INFERENCE from ICE operational definitions]
   129	
   130	4. **CNN investigation (2025):** Found that less than 10% of individuals taken into ICE custody in recent months had serious criminal convictions. [SOURCE: https://us.cnn.com/2025/06/16/us/la-ice-raids-violent-criminals-records-invs, verified via Exa]
   131	
   132	5. **Recent reporting:** "Immigrants with no criminal record now largest group in ICE detention." [SOURCE: The Guardian, verified via Exa]
   133	
   134	**Assessment:** The absolute numbers are real administrative data [A3], but their use to argue that unauthorized immigrants have high crime rates involves a rate-base fallacy. The numbers measure something different from what the peer-reviewed literature measures.
   135	
   136	---
   137	
   138	## Key Methodological Challenges (applying to ALL studies)
   139	
   140	### 1. Denominator problem
   141	No census perfectly counts unauthorized immigrants. Population estimates from CMS and Pew have uncertainty bands. Holding the arrest numerator and immigration-status classification fixed, a larger true unauthorized denominator mechanically lowers the calculated rate, while a smaller denominator raises it. That denominator-only sensitivity should not be confused with numerator or classification uncertainty. Light & Miller (2020) test sensitivity to alternative population estimates and find results robust. [SOURCE: PNAS 117(51)]
   142	
   143	### 2. Reporting / detection bias
   144	Unauthorized immigrants may avoid police contact, leading to:
   145	- **Lower arrest rates** (fewer crimes detected, not fewer crimes committed)
   146	- **Lower victimization reporting** (fear of deportation suppresses calls to police)
   147	
   148	Gunadi (2019) uses IV approaches partly to address this. The direction of bias is ambiguous — it could deflate both numerator (arrests) and denominator effects. [SOURCE: Gunadi 2019]
   149	
   150	### 3. Selection effects
   151	People who undertake the costs and risks of unauthorized migration may be systematically different from both the sending-country population and native-born Americans. The "immigrant selectivity" hypothesis suggests migrants are positively selected on motivation, risk-aversion regarding criminal justice contact, and work orientation. This is a plausible mechanism but hard to test directly. [INFERENCE from theory in Ousey & Kubrin 2018]
   152	
   153	### 4. Deportation as censoring
   154	Unauthorized immigrants who commit crimes may be deported, removing them from the population before they accumulate long criminal records. This would mechanically lower observed crime rates without meaning the underlying propensity is lower. However, Light & Miller (2020) note that this should show up as declining rates over time, which they do not observe. [SOURCE: PNAS 117(51)]
   155	
   156	### 5. Composition of the "native-born" comparison group (race confound)
   157	
   158	**This is the most important methodological caveat.** The "native-born citizens" category is not homogeneous. Black Americans have substantially higher incarceration rates than white or Hispanic Americans. Since unauthorized immigrants are predominantly Hispanic, comparing them to ALL native-born citizens (which includes Black Americans) inflates the apparent gap.
   159	
   160	**What happens when you correct for this:**
   161	
   162	Landgrave & Nowrasteh (Cato Policy Analysis 994, April 2025) provide the race-stratified data:
   163	
   164	| Group | Incarceration rate per 100k (2023) |
   165	|-------|-----------------------------------|
   166	| Native-born (all) | **1,221** |
   167	| Native-born (excluding Black) | **891** |
   168	| Illegal immigrants (all) | **613** |
   169	| Illegal immigrants (excluding Black) | **626** |
   170	| Legal immigrants | **319** |
   171	
   172	[SOURCE: https://www.cato.org/sites/cato.org/files/2025-03/Policy-Analysis-994.pdf]
   173	
   174	- **Without race correction:** illegal immigrants ~50% less likely to be incarcerated than native-born
   175	- **Excluding Black Americans from both groups:** gap narrows to ~30% less likely [SOURCE: https://www.alexnowrasteh.com/p/immigrants-have-a-lower-incarceration — Nowrasteh Apr 2025]
   176	- **Within each racial/ethnic group:** immigrants have lower incarceration rates than their native-born counterparts. Hispanic immigrants < native-born Hispanics. Black immigrants < native-born Blacks. White immigrants < native-born whites. [SOURCE: same]
   177	
   178	**Assessment:** The user critique is valid — the aggregate comparison overstates the incarceration gap by ~20 percentage points. The corrected comparison still shows unauthorized immigrants with lower incarceration rates, but the margin is ~30% lower rather than ~50% lower. The strongest version of this specific incarceration comparison is the within-race comparison, which removes the racial-composition confound; it does not remove age, sex, geography, detection/reporting, or legal-status-classification uncertainty. [INFERENCE]
   179	
   180	**What Light et al. (2020) did NOT do:** Their PNAS study does not stratify the native-born comparison group by race. This is a real limitation of that paper's headline numbers.
   181	
   182	### 6. Generational assimilation
   183	The cited immigration-crime literature reports a broad generational-assimilation pattern: second-generation outcomes often move toward native-born rates rather than preserving first-generation lows. Treat this as a scope-limited caveat, not as an unauthorized-only estimate or a post-2020-surge claim. [SOURCE: Ousey & Kubrin 2018; Rumbaut 2008] [INFERENCE]
   184	
   185	---
   186	
   187	## International Context
   188	
   189	The US finding (lower observed criminal-justice rates for first-generation / unauthorized immigrants) does **not** generalize internationally without qualification.
   190	
   191	**European evidence is more mixed:**
   192	- Saved but not fully analyzed: Skardhamar et al. (2014) on immigrant crime in Norway and Finland finds higher crime rates among some immigrant groups. [SOURCE: S2 ID 54b2f4ed7f408d6bb823617ec9c2d7cb82e11f6e]
   193	- Bell, Fasani, & Machin (2013, JEP 2024 update) — "Immigration and Crime: An International Perspective" documents that the relationship varies substantially by country, immigration policy regime, and immigrant composition. [SOURCE: S2 ID 1f48d32d03bf156d871a2632e516e9064b28b750]
   194	- Key difference: European immigration includes large refugee/asylum populations with different selection mechanisms than US labor migration. The positive selection hypothesis that explains low US immigrant crime may not apply to populations selected by conflict displacement rather than labor market opportunity. [INFERENCE]
   195	
   196	---
   197	
   198	## Claims Table
   199	
   200	| # | Claim | Evidence | Confidence | Source | Status |
   201	|---|-------|----------|------------|--------|--------|
   202	| 1 | Undocumented immigrants in Texas had substantially lower felony arrest rates than native-born citizens (2012-2018) | Administrative arrest data, PNAS peer review | HIGH | Light et al. 2020, PNAS 117(51) | VERIFIED |
   203	| 2 | US-born citizens >2x more likely to be arrested for violent crimes than undocumented immigrants in Texas | Same dataset | HIGH | Light et al. 2020 | VERIFIED |
   204	| 3 | Undocumented immigrants 33% less likely to be institutionalized than US natives nationally | ACS data + IV | MODERATE | Gunadi 2019 | VERIFIED |
   205	| 4 | Meta-analytic average effect of immigration on crime: r = -0.031 (negative, very weak) | 51 studies, 543 effect sizes | HIGH | Ousey & Kubrin 2018 | VERIFIED |
   206	| 5 | Longitudinal studies show stronger negative effect (r = -0.147) than cross-sectional (r = 0.000) | Moderator analysis within meta-analysis | HIGH | Ousey & Kubrin 2018 | VERIFIED |
   207	| 6 | Lott's Arizona study claiming higher rates faces a serious unresolved immigration-status classification critique | Multiple independent critiques (Cato, WaPo, Latino Decisions); no independent reanalysis in this memo | MODERATE-HIGH | Nowrasteh 2022; WaPo 2018 | SUPPORTED CRITIQUE — not independent reanalysis |
   208	| 7 | ICE national docket shows ~15K noncitizens with homicide convictions/charges | Official ICE data released to Congress | HIGH (as administrative count) | ICE ERO letter, Sept 2024 | VERIFIED — but measures stock, not rate |
   209	| 8 | European evidence is more mixed; some immigrant groups show higher crime | Scandinavian studies | LOW-MODERATE | Skardhamar et al. 2014 | PRELIMINARY — fetched but not fully analyzed |
   210	| 9 | Second-generation assimilation evidence points toward higher observed crime/incarceration than first generation, often converging toward native-born levels | Broad generational literature; not unauthorized-only or post-2020-surge evidence | MODERATE | Ousey & Kubrin 2018; Rumbaut 2008 | SUPPORTED LITERATURE PATTERN — scope-limited |
   211	| 10 | Reporting bias (fear of deportation suppressing police contact) could partially explain lower observed rates | Theoretical + indirect evidence | MODERATE | Gunadi 2019; general literature | INFERENCE |
   212	
   213	---
   214	
   215	## What's Uncertain
   216	
   217	1. **Magnitude precision:** We know the direction for observed justice-system rates with high confidence, but the exact ratio varies by study, crime type, time period, and geography. "2x lower" vs "50% lower" vs "33% lower" depends on the specific comparison.
   218	
   219	2. **Causal mechanism:** Is it positive selection (migrants are unusually motivated/law-abiding), deterrence (fear of deportation), underreporting, deportation-as-censoring, or some combination? The literature has not cleanly identified the mechanism. [INFERENCE]
   220	
   221	3. **Post-2020 surge population:** Most rigorous studies cover 2012-2018. Whether the findings generalize to the 2021-2024 immigration surge population (different composition, different entry conditions) is genuinely unknown. [UNVERIFIED]
   222	
   223	4. **Crime type heterogeneity:** The strongest evidence is for violent crime and property crime. Evidence on immigration-specific offenses, DUI, and domestic violence is thinner.
   224	
   225	5. **Subpopulation variation:** Aggregate "unauthorized immigrant" rates may mask important variation by nationality, age at entry, gang affiliation status, etc.
   226	
   227	---
   228	
   229	## Search Log
   230	
   231	| Query/Action | Tool | Result |
   232	|---|---|---|
   233	| Check corpus | list_corpus | 6 immigration-related papers found |
   234	| Read Light et al. 2020 full text | read_paper | Key findings extracted |
   235	| Read Gunadi 2019 full text | read_paper | Key findings extracted |
   236	| Read Ousey & Kubrin 2018 full text | read_paper | Meta-analytic effect sizes extracted |
   237	| Synthesize meta-analysis numbers | ask_papers | Detailed moderator analysis retrieved |
   238	| Verify claim: studies finding higher rates | verify_claim (Exa) | No peer-reviewed higher-rate study found in this pass; Lott Arizona remained the prominent non-peer-reviewed outlier |
   239	| Search: Lott Arizona criticism | web_search_exa + verify_claim | Multiple critiques documented |
   240	| Verify: ICE docket numbers | verify_claim (Exa) | Confirmed as administrative data |
   241	| Verify: Cato/Nowrasteh Texas findings | verify_claim (Exa) | Confirmed, consistent with Light et al. |
   242	| Search S2: undocumented crime incarceration | search_papers | Additional papers identified |
   243	| Fetch Skardhamar et al. 2014 | fetch_paper | Downloaded, not fully analyzed |
   244	
   245	---
   246	
   247	## Sources Saved to Corpus
   248	
   249	- Light, He, & Robey (2020) — `5928780a39cc9fea27a3427432efecf5c21c85e2` [previously saved]
   250	- Gunadi (2019) — `0ab1f84bc263912171bb1b43ac8f3fca05c387f6` [previously saved]
   251	- Ousey & Kubrin (2018) — `33034e4c0080fa686d177bb0e4f52afe7914c852` [previously saved]
   252	- Skardhamar et al. (2014) — `54b2f4ed7f408d6bb823617ec9c2d7cb82e11f6e` [fetched this session]
   253	- Bell, Fasani, & Machin (2024) — `1f48d32d03bf156d871a2632e516e9064b28b750` [previously saved]
   254	
   255	## Sources Not in Corpus (web-sourced)
   256	
   257	- Landgrave & Nowrasteh (2025) "Illegal Immigrant Incarceration Rates, 2010–2023" — Cato Policy Analysis 994. [SOURCE: https://www.cato.org/sites/cato.org/files/2025-03/Policy-Analysis-994.pdf] **Race-stratified incarceration data.**
   258	- Nowrasteh (Apr 2025) blog post with race-corrected comparison tables. [SOURCE: https://www.alexnowrasteh.com/p/immigrants-have-a-lower-incarceration]
   259	- Nowrasteh & Chanwong (Sep 2025) "Immigrants Have Lower Lifetime Incarceration Rates" — 1990 cohort tracked through ACS 2006-2023 by race/ethnicity/immigration status. [SOURCE: https://www.cato.org/blog/immigrants-have-lower-lifetime-incarceration-rates-native-born-americans]
   260	
   261	## Revisions
   262	
   263	| Date | Change |
   264	|------|--------|
   265	| 2026-06-16 | Scoped race correction to incarceration magnitude, made denominator sensitivity conditional on fixed numerator/classification, and narrowed within-race comparison from "eliminates confound entirely" to removing the racial-composition confound. See `immigration-conclusion-audit-running-fixes.md`. |
   266	| 2026-06-16 | Bounded the search-log wording for higher-rate studies: the Exa pass did not find a peer-reviewed higher-rate study, but that is a search-result statement, not a proof of absence across the literature. See `immigration-conclusion-audit-running-fixes.md`. |
   267	| 2026-06-16 | Downgraded the European mixed-evidence table row from `VERIFIED (direction), not fully analyzed` to `PRELIMINARY`; fetched-but-unread evidence should not carry a verified status. See `immigration-conclusion-audit-running-fixes.md`. |
   268	| 2026-06-16 | Reframed the Lott Arizona critique row from `HIGH/VERIFIED` fundamental flaw to a supported unresolved classification critique, because the memo cites critiques rather than running an independent data reanalysis. See `immigration-conclusion-audit-running-fixes.md`. |
   269	| 2026-06-16 | Downgraded the second-generation crime row from `HIGH/VERIFIED` to a scope-limited supported literature pattern; the cited evidence is broad generational literature, not unauthorized-only or current-surge evidence. See `immigration-conclusion-audit-running-fixes.md`. |
--- END FILE: research/immigration-crime-rates-unauthorized-vs-native-born.md ---
