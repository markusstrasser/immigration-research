# Final Immigration Review Context

Date: 2026-06-16
Repo: /Users/alien/Projects/research

## Task

Review the current immigration research surfaces after the June 16 cleanup. Find remaining statistical, mathematical, logical, econometric, data-science, or process-loop issues. Focus on stale scalar exports, denominator/base-rate mismatches, causal language from descriptive/correlational evidence, unscaled extrapolation, internal contradictions, and whether the agent loop can replace human search-space shaping. Do not do prose-only style review. Treat factual claims as untrusted unless supported by quoted file lines below. Separate confirmed findings from speculative preferences, cite file:line from this packet, and give minimal fixes.

## Recent Commits

```
be4548a [research] Mark stale school rows — prevent current-row reuse
403152a [research] Align legacy syntheses — prevent stale net exports
c705dab [research] Scope economist summaries — keep capacity evidence descriptive
dcc2f7d [research] Scope quick claims matrix — avoid false-label exports
89fda26 [research] Mark stale sweep rows — prevent net sign reuse
375e4fb [research] Refresh verified surfaces — June tensor narrowed claims
52918c1 [docs] Route generator audit — keep sweep loop current
f3abecd [research] Add thesis generator audit — widen search loop
4a6857c [research] Preserve model reviews — keep audit packets
f42dfea [research] Add causal reading stack — preserve queue
287c77a [research] Backfill IQ frontier artifacts — preserve access work
c9807d0 [docs] Route immigration memos — index preserved artifacts
```

## Current Git Status

```
## main...origin/main [ahead 156]
?? .model-review/2026-06-16-final-immigration-review/
```


--- BEGIN FILE: research/immigration-knowledge-delta-agent-loop-2026-06-16.md ---
     1	# Immigration knowledge delta and autonomous research loop (2026-06-16)
     2	
     3	**Question:** What do we know now that we did not know two days ago, and what loop should an agent run to replace constant human steering of search space and narrative?
     4	
     5	**Comparison baseline:** state before the 2026-06-15 fiscal sweeps and the 2026-06-16 conclusion audit. At that point, the repo already had the April wage/housing/capacity/crime/surge analyses and the 2026-06-11 CHNV/receiver-election correction, but not the June 15-16 fiscal tensor, denominator audit, or model-review cleanup pass.
     6	
     7	---
     8	
     9	## 1. Net Change Since Two Days Ago
    10	
    11	### A. The fiscal story moved from scalar debate to ledger tensor
    12	
    13	Two days ago, the live fight could still collapse into "Mexico positive or negative?" or "immigrants pay in or drain?" The current state is stricter:
    14	
    15	- `federal_annual` is one layer, not a verdict.
    16	- NAS Table 8-13 is a synthetic age-at-arrival-25 education-mix benchmark, not current-stock lifetime NPV.
    17	- school burden, state/local surge, admin/enforcement, courts, and episodic shelter are separate layers.
    18	- any single "Mexico net" without layer tags is now a known error class.
    19	
    20	**New knowledge:** the correct object is a tensor: `population/group x layer x time horizon x effect order x population universe`.
    21	
    22	### B. The Mexico fiscal result became less certain but more true
    23	
    24	The June 15 loop first found a plausible correction: the old `-$13.5k/adult` school result used the scenario-subset denominator. That briefly made the crude annual `federal - school` row positive (`+$748/adult`).
    25	
    26	The June 16 Opus review then caught the mirror-image bug: the school numerator still came from the scenario household universe, while the denominator was changed to the full microsim stock. We verified this in DuckDB:
    27	
    28	- scenario adults: `436,819`
    29	- scenario linked household weight: `322,539.5`
    30	- full microsim adults: `8,496,334`
    31	- current guarded `v_three_layer_annual` now withholds origin `school_per_adult` and `net_crude_per_adult`.
    32	
    33	**New knowledge:** both the negative and positive Mexico `federal - school` signs were artifacts. The current live scalar is only the narrow federal annual proxy (`~$1,519/adult/yr`); full-stock origin school sign is unresolved until same-universe rebuilt.
    34	
    35	### C. The NAS Mexico headline was relabeled
    36	
    37	`+$45,631/adult` and `+$387.7B` are now known to be current education mix times NAS age-25 cells. They block a crude "all Mexico-origin adults are `<HS` NAS negatives" export, but they do not measure remaining-lifetime NPV of the current Mexico-born stock.
    38	
    39	**New knowledge:** education mix matters, but age-at-arrival/current-age lifecycle remains a missing dimension.
    40	
    41	### D. E-Verify became a bounded wage-margin result, not a Card/Borjas verdict
    42	
    43	Two days ago, short forms still overread E-Verify as a broad Card-side or Borjas-rejection result. Current wording:
    44	
    45	- no statistically significant positive QWI wage effect in the observed mandate margin;
    46	- large native wage gains are not observed in that margin;
    47	- small effects and scaled-shock Borjas benchmarks are not ruled out;
    48	- the E1 employment point estimate is negative but nonsignificant (`t=-1.40`, `p≈0.16`);
    49	- adjustment channels remain hypotheses, not measured mechanisms.
    50	
    51	**New knowledge:** E-Verify is a useful marginal enforcement wage-channel test, not a direct surge, mass-deportation, or open-borders test.
    52	
    53	### E. The surge/capacity evidence became descriptive rather than causal
    54	
    55	Receiver-city gross loads are real and large. The 2024 receiver election association survives the Hispanic-share kill-test at about `+2.4pp`, but it is still correlational. Capacity/load county models are useful screens, but:
    56	
    57	- wage-model ranking gaps are thin;
    58	- permit denominators may proxy local economic vitality;
    59	- q90 threshold weakness may be a power artifact;
    60	- native sorting is association until counterfactual identification exists.
    61	
    62	**New knowledge:** capacity is still a promising search frontier, but it should be framed as descriptive stress-screening plus open causal work.
    63	
    64	### F. Crime conclusion got cleaner
    65	
    66	The observed-rate conclusion survives, but it is now explicitly:
    67	
    68	- observed arrest/conviction/incarceration rates, not true offending;
    69	- aggregate Texas ratios with race-composition caveats;
    70	- Lott classification critique as serious unresolved critique, not independently verified flaw.
    71	
    72	**New knowledge:** the pro-immigration crime conclusion remains strong directionally, but the estimand is narrower.
    73	
    74	### G. Model review was useful because it found drift, not because it supplied facts
    75	
    76	The llmx Opus/GPT and Cursor passes were most valuable at finding internal contradictions:
    77	
    78	- Opus found the school numerator/denominator universe mismatch.
    79	- Multiple reviewers independently flagged E-Verify employment nonsignificance.
    80	- Reviewers surfaced stale synthesis phrases after source memos had been fixed.
    81	
    82	**Process knowledge:** frontier review should be used as adversarial pressure on internal coherence; every finding still needs local verification against data, code, or exact file text.
    83	
    84	---
    85	
    86	## 2. Current Truth State
    87	
    88	The narrative is now:
    89	
    90	1. **No scalar verdict.** Immigration fiscal effects are layer-specific and universe-specific.
    91	2. **Federal annual proxy:** Mexico-origin full microsim row remains about `+$1,519/adult/yr`.
    92	3. **School/full-stock origin row:** unresolved after same-universe guard.
    93	4. **NAS benchmark:** Mexico education mix looks positive under age-25 NAS cells, but that is not current-stock lifetime NPV.
    94	5. **Wages:** observed E-Verify/sanctuary-style policy margins cut against large native wage gains, not all wage effects.
    95	6. **Capacity/surge:** receiver gross load and county load/capacity screens are real descriptive signals; mechanisms and welfare signs remain open.
    96	7. **Crime:** lower observed justice-system rates remain supported; true-offending and subgroup generalization remain lower confidence.
    97	
    98	This is less rhetorically satisfying than two days ago. It is better research.
    99	
   100	---
   101	
   102	## 3. Autonomous Agent Loop
   103	
   104	The human was doing three jobs:
   105	
   106	1. choosing where to look next;
   107	2. noticing when the narrative had outrun the evidence;
   108	3. forcing divergence when the current frame became too comfortable.
   109	
   110	The agent loop has to mechanize those jobs.
   111	
   112	```text
   113	START
   114	  |
   115	  v
   116	1. Load Constitution + Current Frontier
   117	  - read topic index, current synthesis, running fixes, last decisions
   118	  - list live claims with SOURCE / INFERENCE / UNVERIFIED tags
   119	  - identify what changed since last run
   120	  |
   121	  v
   122	2. Claim Inventory
   123	  - split every narrative into atomic claims
   124	  - attach layer, population universe, time horizon, denominator, evidence level
   125	  - mark each claim as live / superseded / unresolved / historical
   126	  |
   127	  v
   128	3. Weakest-Link Audit
   129	  - find claims whose conclusion depends on one fragile bridge:
   130	    denominator, scalar export, causal verb, significance, proxy, stale table
   131	  - rank by decision impact, not by ease
   132	  |
   133	  v
   134	4. Divergence
   135	  - generate 5+ different kill paths:
   136	    data bug, denominator mismatch, rival estimand, omitted layer,
   137	    alternative causal mechanism, external-validity boundary, value-frame shift
   138	  - search by functionality and claim structure, not filenames
   139	  |
   140	  v
   141	5. Cheap Probe
   142	  - one SQL query, one grep, one table checksum, one 10-row sample,
   143	    one coefficient check, or one source quote
   144	  - if probe fails, fix conclusion before building more machinery
   145	  |
   146	  v
   147	6. Evidence Build
   148	  - acquire or rebuild only the minimum dataset needed
   149	  - preserve raw data; derived outputs are rebuildable
   150	  - record exact command and output rows for load-bearing numbers
   151	  |
   152	  v
   153	7. Convergence
   154	  - update source memo, synthesis memo, ladder, index/frontier surfaces
   155	  - append running-fixes entry: issue, evidence, fix, unresolved remainder
   156	  - delete/mark stale scalar exports; do not leave both versions live
   157	  |
   158	  v
   159	8. Adversarial Review
   160	  - llmx Opus/GPT + Cursor lanes on exact packet
   161	  - require file:line findings and minimal fixes
   162	  - verify every finding locally before accepting
   163	  |
   164	  v
   165	9. Commit + Diff Audit
   166	  - commit exact paths per logical fix
   167	  - grep for stale phrases and superseded claims
   168	  - check worktree for unrelated/untracked artifacts
   169	  |
   170	  v
   171	10. RSI Close / Next Frontier
   172	  - verify one load-bearing claim from this loop
   173	  - compare knowledge state to previous baseline
   174	  - promote one process guard if recurrence is hookable
   175	  - choose the next frontier by value of information
   176	  |
   177	  v
   178	REPEAT
   179	```
   180	
   181	---
   182	
   183	## 4. The Search-Space Shaping Heuristic
   184	
   185	Each cycle should maintain a frontier table:
   186	
   187	| Frontier | Ask | Stop rule |
   188	|---|---|---|
   189	| Denominator | Are numerator and denominator the same population/time/unit? | exact row-level reconciliation passes |
   190	| Layer | Which ledger layer does this claim live in? | claim has layer tag and no scalar export |
   191	| Margin | What policy/data variation identifies the claim? | no extrapolation beyond named margin |
   192	| Mechanism | Is the mechanism measured or inferred? | causal verbs removed unless design identifies |
   193	| Significance | Is non-significance being read as zero or as effect? | wording distinguishes point estimate, CI, MDE |
   194	| Counterfactual | What would falsify the current narrative? | explicit kill path or unresolved label |
   195	| Narrative | What slogan would a reader wrongly quote? | grepable stale phrase removed or marked historical |
   196	
   197	The agent replaces constant human steering by forcing every cycle through this table before and after evidence work.
   198	
   199	---
   200	
   201	## 5. Divergence and Convergence Rhythm
   202	
   203	Use a fixed cadence:
   204	
   205	1. **Diverge hard:** at least five mechanism-distinct ways current conclusions could be wrong.
   206	2. **Probe cheap:** test one high-impact weak link first.
   207	3. **Converge narrowly:** patch only conclusions the evidence actually changes.
   208	4. **Review adversarially:** outside models search for drift and contradiction.
   209	5. **Verify locally:** accept nothing from reviewers without repo/data evidence.
   210	6. **RSI:** capture one durable process improvement or next frontier, not a broad retrospective.
   211	
   212	The key is not "more agents." It is parent-controlled epochs: dispatch, read, verify, patch, then redispatch only if the frontier actually changed.
   213	
   214	---
   215	
   216	## 6. Next High-Value Frontiers
   217	
   218	1. **Same-universe origin school burden rebuild.**
   219	   Build a full-stock household school numerator or keep the row null. This is the biggest live fiscal blocker.
   220	
   221	2. **Current-stock lifetime NPV.**
   222	   Age-at-arrival x current-age x education x return migration. The age-25 benchmark is useful but not enough.
   223	
   224	3. **Capacity causal design.**
   225	   Show load adds signal beyond permit level and local growth, or demote load/capacity from frontier to descriptive screen.
   226	
   227	4. **Receiver-city synthetic controls.**
   228	   Gross load is measured; vote/fiscal mechanism needs better counterfactuals.
   229	
   230	5. **Crime subgroup/time heterogeneity.**
   231	   Preserve observed-rate conclusion while testing whether recent-surge origin mix or second-generation patterns change any local claims.
   232	
   233	The next loop should start with frontier 1, because it gates several fiscal narratives and has a concrete denominator invariant.
--- END FILE: research/immigration-knowledge-delta-agent-loop-2026-06-16.md ---

--- BEGIN FILE: research/immigration-thesis-generator-audit-2026-06-16.md ---
     1	# Immigration thesis/narrative generator audit and upgrade - 2026-06-16
     2	
     3	**Purpose:** evaluate the current immigration thesis-generation loop, compare what it knows now against the June 14 baseline, and add better cross-disciplinary generators from economics, micro, macro, psychology, political economy, and urbanism.
     4	
     5	**Companion loop (broader):** `research/immigration-knowledge-delta-agent-loop-2026-06-16.md` owns full claim inventory, probe, adversarial review, and commit routing. This memo owns generator and XDISC divergence only.
     6	
     7	**Verdict:** the current generator system is useful and materially better than two days ago, but it is still too fiscal-ledger-native. It catches scalar exports, denominator slips, and layer laundering; it does not yet force enough narrative, legitimacy, sorting, contact/threat, spatial-equilibrium, and agenda-setting alternatives before convergence. [SOURCE: `notes/immigration-lifetime-synthesis-diverge-cookbook.md`; `research/immigration-lifetime-fiscal-generators.md`; DuckDB query on `warehouse/immigration_lifetime_evidence.duckdb`] [INFERENCE]
     8	
     9	---
    10	
    11	## Ground inventory
    12	
    13	### Current artifacts
    14	
    15	| Surface | Current state | Audit read |
    16	|---|---:|---|
    17	| Diverge/converge cookbook | Explicit loop: carry prior thesis + generator menu + DuckDB state -> diverge -> converge -> next sweep | Strong process spine; mostly fiscal-lifetime scoped. [SOURCE: `notes/immigration-lifetime-synthesis-diverge-cookbook.md`] |
    18	| Generator registry | Markdown has `106` `G-LIF-*` headings; DuckDB has `104` rows across `19` clusters; MD-only IDs are `G-LIF-Q06`, `G-LIF-S15` | Useful but count/lifecycle sync is not clean enough for automated yield scoring. [SOURCE: `rg -c '^### G-LIF'`; DuckDB `count(*)`; `comm -23`; `describe lifetime_generators`] |
    19	| Generator schema in DuckDB | `generator_id`, `name`, `prompt_template`, `retrodiction_example`, `negative_space`, `unnamed_assumptions`, `topics`, `source_rel_paths`, `cluster`, `theory_tested` | Good minimum schema; missing status/yield/last-fired/retirement fields. [SOURCE: DuckDB `describe lifetime_generators`] |
    20	| Parameter claims | DuckDB has `563` rows in `parameter_claims` | Header/index counts must use warehouse truth or explicitly say Markdown-only. [SOURCE: DuckDB `select count(*) from parameter_claims`] |
    21	| Unified theory | Layered incidence tensor: cell x ledger layer x time; no scalar "Mexican lifetime NPV" | Strong correction against the main fiscal overclaim. [SOURCE: `research/immigration-lifetime-unified-theory-2026-06-15.md`] |
    22	| Running fixes ledger | Many June 16 fixes demote overclaims to scoped, model- or margin-bound claims | Good error-correction surface; should also log process fixes. [SOURCE: `research/immigration-conclusion-audit-running-fixes.md`] |
    23	
    24	### Two-day knowledge delta
    25	
    26	Using the repository baseline before the end of June 14, the named lifetime generator/cookbook/unified-theory/knowledge-delta artifacts were not yet present in tracked history. By June 16, the repo has a dedicated divergence cookbook, a lifetime fiscal generator registry, a unified theory memo, and a knowledge-delta agent loop memo. [SOURCE: `git rev-list -1 --before='2026-06-14 23:59' main -- ...`; `git log --since='2026-06-14' -- ...`; `research/immigration-knowledge-delta-agent-loop-2026-06-16.md`] [DATA]
    27	
    28	What changed:
    29	
    30	1. **From memo accumulation to loop discipline.** Two days ago, the repo had immigration memos and audits; now it has an explicit loop: carry thesis, generate negative space, mine sources, converge into layered theory, then disconfirm before the next sweep. [SOURCE: git history; `notes/immigration-lifetime-synthesis-diverge-cookbook.md`] [INFERENCE]
    31	2. **From scalar fiscal answers to tensor grammar.** The central object is now `cell x ledger layer x time`, not "immigrants are net positive/negative." This is the largest conceptual improvement. [SOURCE: `research/immigration-lifetime-unified-theory-2026-06-15.md`] [INFERENCE]
    32	3. **From source harvesting to generator harvesting.** The system now stores prompts that can retrodict prior misses and name negative space, instead of only storing paper findings. [SOURCE: `research/immigration-lifetime-fiscal-generators.md`] [INFERENCE]
    33	4. **From confidence to correction.** The June 16 fix ledger repeatedly converts strong rhetoric into scoped evidence claims: non-significance is not zero, gross load is not causal mechanism, observed justice-system rate is not true offending, local burden is not all-in NPV. [SOURCE: `research/immigration-conclusion-audit-running-fixes.md`] [INFERENCE]
    34	5. **Still missing:** generator yield accounting, non-fiscal narrative generators, and a self-prompt that forces an agent to ask what a public-finance economist, urbanist, macroeconomist, psychologist, restrictionist, and open-borders advocate would each call false. [INFERENCE]
    35	
    36	---
    37	
    38	## Evaluation of existing generators
    39	
    40	### What is working
    41	
    42	1. **Retrodiction as quality control.** The cookbook requires each generator to retrodict at least two prior findings. This is the right filter: a generator that cannot explain past misses is usually just a topic suggestion. [SOURCE: `notes/immigration-lifetime-synthesis-diverge-cookbook.md`] [INFERENCE]
    43	2. **Negative-space fields.** The registry forces each generator to name what the standing frame excludes, which directly fights search-space narrowing. [SOURCE: `research/immigration-lifetime-fiscal-generators.md`] [INFERENCE]
    44	3. **Layer discipline.** Existing generators repeatedly catch fiscal/lifetime/annual/local layer switching. This is the repo's main statistical advantage over pundit-style immigration narratives. [SOURCE: `research/immigration-lifetime-fiscal-generators.md`] [INFERENCE]
    45	4. **Disconfirmation after convergence.** The protocol makes contradiction hunts part of convergence rather than an optional review step. [SOURCE: `notes/immigration-lifetime-sweep-protocol.md`] [INFERENCE]
    46	
    47	### What is weak
    48	
    49	1. **Fiscal center of gravity.** The existing registry is excellent for public-finance and immigration-economics errors, and it has partial housing/capacity/admin/political clusters. It still underweights psychology, agenda-setting, urban sorting, legitimacy, symmetric pro-immigration steelmanning, and social contact/threat narratives. [INFERENCE]
    50	2. **Urbanism is too rent/supply-centered.** The E cluster goes beyond Saiz alone, but urban incidence still needs Tiebout sorting, Roback spatial equilibrium, Diamond amenity sorting, local employment multipliers, zoning/productivity misallocation, and service-capacity politics. [SOURCE: Saiz 2010 QJE; Tiebout 1956 JPE; Roback 1982 JPE; Diamond 2016 AER; Hsieh & Moretti 2019 AEJ Macro] [INFERENCE]
    51	3. **Micro/macro identification prompts are too implicit.** The loop should force estimand classification, target/instrument matching, shift-share/enclave identification, household/firm adaptation margins, capital deepening, dependency-ratio transitions, and reflection/social-effects identification. [SOURCE: Tinbergen policy target/instrument framework; Manski 1993 reflection problem; Card 2001; Goldsmith-Pinkham et al. 2020] [INFERENCE]
    52	4. **Narrative self-prompting is underbuilt and asymmetry-prone.** The loop asks for thesis bursts, but not enough for frame audits: who is the hero/victim/villain, what causal story is being smuggled in, what pro-immigration frame is absent, and what would make the story politically salient even if the fiscal ledger is small? [SOURCE: Entman 1993 framing; Stone 1989 causal stories; Kingdon multiple-streams framework] [INFERENCE]
    53	5. **Lifecycle accounting is missing.** There is no `status`, `last_fired`, `adopted_outputs`, or `retirement_counter` in the DuckDB schema; the cookbook now says to park zero-yield generators while applicable, but that rule still has no machine-readable state. [SOURCE: DuckDB `describe lifetime_generators`; `notes/immigration-lifetime-synthesis-diverge-cookbook.md`] [DATA]
    54	
    55	---
    56	
    57	## Cross-disciplinary generator upgrade
    58	
    59	Use these as a new "XDISC" packet before the next immigration sweep. They are not yet loaded into `lifetime_generators`; the first implementation should either add a new loaded cluster or keep them as a separate `thesis_generators` table so fiscal generators do not silently become all-purpose narrative prompts. [INFERENCE]
    60	
    61	| ID | Family | Generator prompt | Retrodicts / first probe |
    62	|---|---|---|---|
    63	| XDISC-ECO-01 | Policy economics | For every recommendation, name the target variable and the policy instrument. Fail the claim if one instrument is asserted to solve multiple independent targets without tradeoff. | Retrodicts layer laundering: enforcement, welfare, housing, and fiscal goals were being treated as one target. First probe: annotate one memo's recommendations. [SOURCE: Tinbergen 1952/1956 policy framework] |
    64	| XDISC-ECO-02 | Public finance | Split statutory payer, economic payer, beneficiary, jurisdiction, public-goods cost rule (average vs marginal; pure vs congestible), descendant boundary, and time horizon for every dollar claim. Fail any net-fiscal sign claim that lacks a public-goods rule and descendant boundary. | Retrodicts federal-positive/local-negative compatibility, school-cost numerator bugs, and NAS-style sign sensitivity. Probe: one row per cost/revenue line. [SOURCE: existing fiscal ledger memos; National Academies 2017] |
    65	| XDISC-ECO-03 | Immigration surplus | For any wage/output effect, separate aggregate efficiency gain from redistribution between competing labor, complementary labor, and capital; state short-run vs capital-adjusted horizon. | Retrodicts how small average native effects can coexist with real distributional losses. Probe: decompose one Borjas/Card claim into efficiency triangle vs transfers. [SOURCE: Borjas 1995; Ottaviano & Peri 2012] |
    66	| XDISC-MIC-01 | Micro adaptation | Before accepting a wage/fiscal effect, list household, firm, native, immigrant, and government adjustment margins: hours, tasks, location, household composition, take-up, compliance, exit. | Retrodicts why wage effect != fiscal effect and why native out-migration changes local incidence. Probe: annotate Borjas/Card/Saiz claims. [SOURCE: `research/immigration-lifetime-fiscal-generators.md`] |
    67	| XDISC-MIC-02 | Social interactions | If group outcomes correlate, identify whether the claim is endogenous peer effect, contextual effect, correlated unobservables, selection, or measurement artifact. | Retrodicts receiver-city mechanism ambiguity and backlash overclaim downgrades. Probe: classify one political-response claim. [SOURCE: Manski 1993 reflection problem] |
    68	| XDISC-MIC-03 | Labor identification | For any local immigration effect, name the design: spatial correlation, enclave/shift-share IV, factor-proportions national skill-cell, or event-study/policy shock. State skill cells, substitution elasticity, and leading endogeneity threat. | Retrodicts Borjas/Card divergence and native out-migration disputes. Probe: re-derive one local estimate's identifying variation and exclusion restriction. [SOURCE: Card 2001; Goldsmith-Pinkham, Sorkin & Swift 2020] |
    69	| XDISC-MAC-01 | Macro transition path | For each static fiscal claim, ask what happens to capital/labor, age structure, dependency ratios, public debt, and tax rates over transition and steady state. | Retrodicts why annual federal proxy cannot be integrated into lifetime NPV without a bridge. Probe: draw 3-period transition table. [INFERENCE] |
    70	| XDISC-MAC-02 | Open-economy welfare | Separate destination public ledger, origin-country welfare, remittances, and global output. State which welfare function is being optimized before using "gain/loss." | Retrodicts open-borders welfare-weight fixes and remittance/private-layer separation. Probe: add welfare-function column to one memo. [INFERENCE] |
    71	| XDISC-MAC-03 | NPV sensitivity | For every lifetime/NPV claim, report discount rate, projection horizon, public-debt closure rule, capital adjustment, and mortality/return-migration horizon. | Retrodicts annual-to-lifetime bridge errors and sign flips under accounting conventions. Probe: sensitivity grid before any lifetime sign. [SOURCE: National Academies 2017] |
    72	| XDISC-URB-01 | Tiebout/local public goods | Ask whether residents are sorting into tax/service bundles and whether immigration changes the bundle, the population choosing it, or only measured averages. | Retrodicts county capacity and school-service framing problems. Probe: map one state/local cost claim to bundle changes. [SOURCE: Tiebout 1956] |
    73	| XDISC-URB-02 | Spatial equilibrium | Never infer welfare from wage or rent alone. Force wage, rent, amenity, and public-service bundle together. | Retrodicts Saiz/rent-exposure != welfare-loss fixes. Probe: convert one rent claim to a Roback-style welfare question. [SOURCE: Roback 1982; Diamond 2016] |
    74	| XDISC-URB-03 | Housing constraint/productivity | Ask whether housing constraints turn national productivity gains into local renter losses, congestion, or spatial misallocation. | Retrodicts why open-borders/global gains and local-capacity losses can both be true. Probe: classify high-inflow MSAs by housing supply elasticity and productivity. [SOURCE: Saiz 2010; Hsieh & Moretti 2019] |
    75	| XDISC-URB-04 | Local employment/demand multipliers | For every immigrant inflow cost claim, ask whether local demand, traded-sector employment, or service-sector multipliers offset or amplify the local tax base. Do not treat an employment multiplier as a fiscal multiplier without an induced-tax-base bridge. | Retrodicts why fiscal costs cannot be read from population count alone. Probe: separate tradable vs non-tradable exposure and fiscal bridge. [SOURCE: Moretti 2010] |
    76	| XDISC-URB-05 | Agglomeration/innovation | Ask whether high-skill inflows generate innovation, entrepreneurship, patenting, or knowledge spillovers that offset congestion/housing losses, and at what spatial scale. | Retrodicts why high-skill immigration can be positive in national productivity while still worsening constrained-city housing incidence. Probe: separate innovation scale from local rent incidence. [SOURCE: Kerr & Lincoln 2010; Hunt & Gauthier-Loiselle 2010] |
    77	| XDISC-INST-01 | Congestible club/local goods | Treat schools, courts, permits, shelters, and public safety as congestible club/local public goods with capacity, congestion, rationing, and jurisdiction rules. Use Ostrom only for genuine common-pool-resource cases. | Retrodicts receiver-node overload and admin-capacity findings without misclassifying every local service as a commons. Probe: identify one capacity bottleneck per local layer. [SOURCE: Buchanan 1965; Tiebout 1956; Ostrom 2009] |
    78	| XDISC-PE-01 | Distributive political economy | Name winning and losing coalitions for each recommendation: employers/capital, native low-skill labor, native high-skill labor, taxpayers, immigrants, local incumbents. State who is organized and who is diffuse. | Retrodicts why aggregate gains can coexist with intense opposition. Probe: three coalitions per policy recommendation. [INFERENCE; verify source before registry load] |
    79	| XDISC-PE-02 | Diversity and redistribution | Ask whether heterogeneity changes support for redistribution/public goods separately from measured fiscal cost. | Retrodicts welfare-state and public-goods political feedback arguments without collapsing them into budget arithmetic. Probe: tag each welfare claim as cost-channel vs solidarity-channel. [SOURCE: Alesina & Glaeser 2004; Putnam 2007] |
    80	| XDISC-PSY-01 | Threat vs load | Split material burden from perceived group threat; tag theory as realistic threat, symbolic threat, group-conflict, or authoritarian-by-threat interaction. | Retrodicts political-response mechanism ambiguity. Probe: compare actual vs perceived immigrant share where available. [SOURCE: Quillian 1995] |
    81	| XDISC-PSY-02 | Contact vs segregation | Ask whether contact is equal-status/cooperative/institutionally supported or concentrated, competitive, and capacity-stressed; apply XDISC-MIC-02 to check contact selection/reverse causation. | Retrodicts why "more contact reduces prejudice" is not a universal migration argument. Probe: classify receiver settings by contact conditions. [SOURCE: Pettigrew & Tropp 2006] |
    82	| XDISC-PSY-03 | Misperception mediator | For any public-opinion or redistribution claim, insert a belief-mediator row: perceived immigrant share, skill, benefit use, origin, legality, and fiscal contribution. Then test whether correcting the belief changes the attitude; do not assume it does. | Retrodicts Alesina-style salience/redistribution channel and anti-overclaiming fixes. Probe: list belief variables before causal story. [SOURCE: Alesina, Miano & Stantcheva 2018] |
    83	| XDISC-PSY-04 | Sociotropic vs egocentric | Split personal/pocketbook from national/collective, and economic from cultural. Fail attitude claims that infer personal self-interest from group-level correlations. | Retrodicts why immigration opposition can be weakly tied to direct local exposure. Probe: classify one opinion finding on both axes. [SOURCE: Hainmueller & Hopkins 2014] |
    84	| XDISC-PSY-05 | Motivated reasoning | Ask whether the belief is identity-expressive; if so, predict that more evidence may widen, not narrow, group gaps. | Retrodicts why source-corrected memos may not move public narratives. Probe: mark each public-facing claim as accuracy-driven vs identity-expressive. [SOURCE: Kahan et al. 2017] |
    85	| XDISC-AGS-01 | Agenda-setting/priming | Separate salience, attribute framing, priming/evaluation criteria, issue ownership, and elite cueing; ask whether perceived share is bottom-up or messaging-driven. | Retrodicts salience shifts without matching ground-condition changes. Probe: decompose one "why salient now" story into agenda/prime/frame/owner rows. [SOURCE: McCombs & Shaw 1972; Petrocik 1996] |
    86	| XDISC-POL-01 | Agenda process (MSF) | Ask why this issue is salient now: indicator change, focusing event, policy entrepreneur, media frame, or coalition opening. Tag MSF output as narrative/process, not causal identification. | Retrodicts surge-era timing errors as process hypotheses only. Probe: problem/policy/politics stream table. [SOURCE: Kingdon/MSF literature] |
    87	| XDISC-NAR-01 | Causal-story audit | For each narrative, name cause type: mechanical, accidental, intentional, inadvertent. Ask who becomes victim, villain, beneficiary, and fixer. Name one absent frame and one observation that would distinguish frame-effect from null. | Retrodicts overstrong "backlash" and "system collapse" language. Probe: annotate one public-facing paragraph. [SOURCE: Stone 1989] |
    88	| XDISC-NAR-02 | Frame function | For each paragraph, identify problem definition, causal interpretation, moral evaluation, and treatment recommendation. Fail if the frame cannot be falsified or contrasted with an absent frame. | Retrodicts hidden policy conclusion drift. Probe: Entman-frame one memo section before publishing. [SOURCE: Entman 1993] |
    89	| XDISC-NAR-03 | Deservingness | Score implicit deservingness criteria by migrant category: control, attitude, reciprocity, identity, and need. | Retrodicts refugee-vs-economic-migrant splits and legality/deservingness shortcuts. Probe: tag one public paragraph. [SOURCE: van Oorschot 2000] |
    90	| XDISC-NAR-04 | Steelman symmetry | Each sweep emits one pro-immigration and one restrictionist steelman that the other side would accept as fair; fail convergence if either is missing or strawmanned. | Retrodicts selection toward the house frame. Probe: store both steelmen as rows before thesis burst. [INFERENCE] |
    91	| XDISC-ADV-01 | Pro-immigration steelman | Mirror the restrictionist S cluster by forcing the best destination-capacity-aware pro-immigration case: global gains, innovation, dynamism, humanitarian legitimacy, and rule-designed absorptive capacity. | Retrodicts why restrictionist steelmanning alone can bias the generator menu. Probe: write the strongest pro case and its own falsifiers before critique. [INFERENCE] |
    92	| XDISC-CAU-01 | DAG/confounder gate | Before any causal mechanism claim, sketch treatment, outcome, confounders, mediators, colliders, and post-treatment variables. | Retrodicts overread county/surge associations and bad-control risks. Probe: one DAG line before one regression interpretation. [SOURCE: `research/immigration-costs-causal-analysis.md`] |
    93	| XDISC-MEAS-01 | Legal-status/arrival measurement | For any unauthorized/recent-arrival claim, state how legal status, YOEP, country of birth, citizenship, and household linkage are observed or imputed. | Retrodicts ICE docket denominator and school universe bugs. Probe: measurement row for each headline subgroup. [SOURCE: `research/immigration-conclusion-audit-running-fixes.md`] |
    94	| XDISC-PIPE-01 | View/unit drift | For any derived table or view, assert units, withheld rows, denominator universe, and source build commit before exporting a headline. | Retrodicts F-33 thousands bug, withheld school net, and generator count drift. Probe: fail if view units are not machine-checked. [SOURCE: `research/immigration-conclusion-audit-running-fixes.md`] |
    95	| XDISC-DS-01 | Estimand classifier | Blocking check: label every load-bearing claim as descriptive, causal, welfare, forecast, mechanism, or narrative. Claims cannot borrow confidence across labels. | Retrodicts non-significance != zero and observed justice rates != true offending. Probe: fail a memo table if any load-bearing row lacks an estimand. [SOURCE: `notes/quant-bias-checklist.md`] |
    96	| XDISC-DS-02 | Universe twin | Blocking check: for every ratio, print numerator universe, denominator universe, sample frame, time window, and missingness/attrition. | Retrodicts school numerator/full-microsim denominator mismatch and ICE docket denominator fix. Probe: fail any row where universes differ without label. [SOURCE: `research/immigration-conclusion-audit-running-fixes.md`] |
    97	| XDISC-RSI-01 | Generator yield loop | After each sweep, record which generators fired, which produced adopted changes, which produced no output, and which should retire. | Retrodicts current Markdown/header/DuckDB generator count mismatch. Probe: add `status`, `last_fired`, `adopted_outputs`, `retirement_counter`. [INFERENCE] |
    98	
    99	### Dedup/load gate before registry adoption
   100	
   101	Do not bulk-load XDISC into `lifetime_generators`. First add a `duplicates_g_lif` or `supersedes` field and keep only net-new prompts as registry rows. Probable overlaps from review:
   102	
   103	| XDISC row | Existing overlap to check |
   104	|---|---|
   105	| ECO-02 | `G-LIF-C01`, `G-LIF-K01`, `G-LIF-O01` |
   106	| MIC-01 | `G-LIF-B01`, `G-LIF-B04`, `G-LIF-F02` |
   107	| URB-02 | `G-LIF-E01`, partial `G-LIF-E03` |
   108	| DS-02 | `G-LIF-Q*`, `G-LIF-N*`, `G-LIF-K01` |
   109	| INST-01 | `G-LIF-C02`, `G-LIF-J*`, `G-LIF-P02` |
   110	
   111	Candidate net-new families: `MIC-02`, `MIC-03`, `MAC-*`, `URB-01/03/04/05`, `PE-*`, `PSY-*`, `AGS-01`, `POL-01`, `NAR-*`, `ADV-01`, `CAU-01`, `MEAS-01`, `PIPE-01`, `DS-01`, `RSI-01`. [INFERENCE]
   112	
   113	---
   114	
   115	## Self-prompt packet
   116	
   117	Use this as the agent's self-prompt before and after research sweeps.
   118	
   119	### Before divergence
   120	
   121	1. What thesis am I tempted to prove?
   122	2. What would make that thesis false on a different ledger layer, time horizon, geography, or welfare function?
   123	3. Which denominator, sample universe, or unit conversion would flip the sign?
   124	4. What is the policy target, and what is the instrument? Are multiple targets being laundered into one instrument?
   125	5. What public-goods rule, descendant boundary, discount rate, and projection horizon would flip the fiscal sign?
   126	6. Which identification strategy is actually present: descriptive correlation, shift-share/enclave, event study, factor-proportions, or none?
   127	7. Which discipline would object first: public finance, labor micro, macro, urban economics, psychology, political science, law/admin, or data engineering?
   128	8. What would a fair restrictionist and a fair open-borders advocate each accept as bad news?
   129	
   130	### During search
   131	
   132	1. Run one rightward and one leftward debias pass; do not let either become the synthesis.
   133	2. For every source, extract one parameter, one identification limit, one narrative move, and one missing counterfactual.
   134	3. Stop a source path when it no longer changes a claim, generator, dataset acquisition, or falsifier.
   135	4. If a source only restates a known generator, cite it as support but do not create a duplicate generator.
   136	
   137	### Before convergence
   138	
   139	1. Which active thesis got demoted? If none, suspect selection.
   140	2. Which generator produced a new artifact, and which produced no adopted output?
   141	3. Which disagreement is a data fight, and which is a frame/welfare-function fight?
   142	4. Does the final narrative state what data cannot kill because it is a different layer?
   143	5. What is the next cheapest probe that can falsify the highest-impact remaining claim?
   144	
   145	---
   146	
   147	## Agent flowchart for replacing constant human search-space shaping
   148	
   149	The human has been doing three jobs: interrupting stale narratives, forcing better search axes, and catching overclaims. The agent loop has to mechanize those jobs.
   150	
   151	```
   152	START
   153	  |
   154	  v
   155	1. Load live state
   156	   - topic index, current thesis, generator registry, running fixes, DuckDB tables
   157	   - write down the current thesis before new evidence
   158	   - assert MD headings == DuckDB rows == header count, or mark [DEGRADED]
   159	   - load dead-paths/aborted probes so the agent does not repeat known-failed searches
   160	  |
   161	  v
   162	2. Classify the question
   163	   - descriptive / causal / welfare / forecast / narrative / implementation
   164	   - choose the ledger layer and unit of analysis
   165	  |
   166	  v
   167	3. Generate alternatives before search
   168	   - run at most 8 generators/sweep
   169	   - include >=1 denominator/unit, >=1 local/urban, >=1 pro-immigration or restrictionist steelman,
   170	     >=1 psychology/narrative/political generator, and DS-01 on every load-bearing number
   171	  |
   172	  v
   173	4. Retrodiction gate
   174	   - keep generators that explain >=2 prior findings/misses on a held-out slice
   175	   - also require >=1 negative-space item no existing generator names
   176	   - reject one-off topic ideas without mechanism
   177	  |
   178	  v
   179	5. Probe cheaply
   180	   - one SQL slice, one PDF/page check, one denominator check, one source quote/parameter
   181	   - abort or redirect if the probe contradicts the plan
   182	  |
   183	  v
   184	6. Mine evidence
   185	   - extract parameter claims, identification limits, assumptions, and narrative frames
   186	   - tag every load-bearing claim with SOURCE / DATA / INFERENCE / FRAMING-SENSITIVE
   187	  |
   188	  v
   189	7. Converge
   190	   - update layered theory
   191	   - run five mechanism models
   192	   - write three disconfirmation hunts
   193	   - separate data-resolvable fights from frame-resolvable fights
   194	  |
   195	  v
   196	8. Narrative audit
   197	   - Entman frame: problem / cause / moral evaluation / treatment
   198	   - Stone causal story: victim / villain / fixer / cause type
   199	   - slogan inversion: how each side would overquote this
   200	  |
   201	  v
   202	9. Update durable artifacts
   203	   - thesis memo, generator registry or generator-audit memo, running fixes, index
   204	   - never leave a confirmed no-downside fix as an offer
   205	   - write registry + DuckDB + fixes atomically or mark the sweep incomplete
   206	  |
   207	  v
   208	10. RSI / yield accounting
   209	   - fired? adopted output? false lead? retired?
   210	   - adoption must be judged by a separate pass or artifact diff, not the generator author alone
   211	   - two dry applicable sweeps parks a generator; retirement is manual
   212	   - if a human correction repeats, turn it into a generator, hook, or checklist row
   213	  |
   214	  v
   215	STOP after 2 consecutive sweeps with zero adopted outputs, or when the budget/max-sweep cap is reached.
   216	Otherwise LOOP.
   217	```
   218	
   219	---
   220	
   221	## Implementation recommendation
   222	
   223	Do **not** add a global hook yet. The process gap is real, but the first fix is to add a loaded generator-lifecycle table or a YAML/CSV sidecar and run it manually for one more sweep. A hook is justified only after the same generator-lifecycle miss repeats. [INFERENCE]
   224	
   225	Minimum schema:
   226	
   227	```text
   228	generator_id
   229	family
   230	prompt
   231	retrodicts
   232	negative_space
   233	first_probe
   234	source_grade
   235	duplicates_g_lif
   236	applicable_corpus
   237	status              # active | parked | retired
   238	fired_count          # produced >=1 candidate
   239	dry_count            # fired while applicable, zero adopted
   240	adoption_attributions
   241	adoption_judge
   242	last_integrity_check
   243	notes
   244	```
   245	
   246	Next concrete run:
   247	
   248	1. Run `XDISC-URB-01` through `XDISC-URB-05` over the school/housing/capacity memos.
   249	2. Run `XDISC-PE-01`, `XDISC-PE-02`, `XDISC-PSY-*`, `XDISC-AGS-01`, and `XDISC-POL-01` over the surge/political-response memos.
   250	3. Run `XDISC-DS-01` and `XDISC-DS-02` over every remaining headline ratio in the current verified-findings/confidence-ladder surface.
   251	4. Reconcile `research/immigration-lifetime-fiscal-generators.md` counts against DuckDB before depending on counts in automation; current MD-only IDs are `G-LIF-Q06` and `G-LIF-S15`.
   252	
   253	## Review disposition
   254	
   255	Reviewer packet: `.model-review/2026-06-16-immigration-thesis-generator-audit/`.
   256	
   257	Accepted from Opus/Cursor review:
   258	
   259	1. Public-goods rule, descendant boundary, discount rate, and NPV horizon need explicit generators.
   260	2. Shift-share/enclave identification and labor-supply surplus/distribution prompts were missing.
   261	3. Ostrom/common-pool language was too broad for schools/courts/shelters; use congestible club/local public goods unless the resource is genuinely common-pool.
   262	4. Political-economy, sociotropic-vs-egocentric attitudes, motivated reasoning, agenda-setting/priming, deservingness, and symmetric pro-immigration steelman generators were missing.
   263	5. Retrodiction-only gating and two-cycle retirement are unsafe; use held-out retrodiction + novelty, park rather than retire, and judge adoption separately.
   264	6. XDISC must deduplicate against existing `G-LIF-*` rows before loading into a registry.
   265	
   266	Deferred:
   267	
   268	1. A DuckDB lifecycle migration is not included in this memo patch; it needs a build-path change, not prose-only edits.
   269	2. A global hook is deferred until repeated misses justify it.
   270	3. The full source upgrade for every political-economy citation should happen before registry load; rows marked `[INFERENCE; verify source before registry load]` are not ready as cited source claims.
   271	
   272	---
   273	
   274	## Sources used for generator expansion
   275	
   276	- Tinbergen policy target/instrument logic: `https://www.elibrary.imf.org/downloadpdf/journals/024/1968/003/article-A001-en.pdf`; `https://garfield.library.upenn.edu/classics1986/A1986C401200001.pdf`
   277	- Tiebout local public goods/sorting: `https://fbaum.unc.edu/teaching/PLSC541_Fall08/tiebout_1956.pdf`; `https://www.journals.uchicago.edu/doi/10.1086/257839`
   278	- Manski reflection/social effects: `https://users.econ.umn.edu/~holmes/class/2003f8601/papers/manksi_reflection.pdf`; `https://academic.oup.com/restud/article-abstract/60/3/531/1570385`
   279	- Roback spatial equilibrium: `https://matthewturner.org/ec2410/readings/Roback_JPE_1982.pdf`; `https://www.journals.uchicago.edu/doi/abs/10.1086/261120`
   280	- Saiz housing supply elasticity: `https://joeornstein.github.io/pols-4641/readings/Saiz%20-%202010-%20The%20Geographic%20Determinants%20of%20Housing%20Supply.pdf`; `https://econpapers.repec.org/RePEc%3Aoup%3Aqjecon%3Av%3A125%3Ay%3A2010%3Ai%3A3%3Ap%3A1253-1296.`
   281	- Moretti local multipliers: `https://eml.berkeley.edu/~moretti/multipliers.pdf`; `https://www.aeaweb.org/articles?id=10.1257%2Faer.100.2.373`
   282	- Hsieh & Moretti housing constraints/spatial misallocation: `https://eml.berkeley.edu/~moretti/growth.pdf`; `https://www.aeaweb.org/articles?id=10.1257%2Fmac.20170388`
   283	- Diamond sorting/amenities: `https://matthewturner.org/ec2410/readings/Diamond_AER_2016.pdf`; `https://www.aeaweb.org/articles?id=10.1257%2Faer.20131706`
   284	- National Academies immigration fiscal report: `https://nap.nationalacademies.org/catalog/23550/the-economic-and-fiscal-consequences-of-immigration`
   285	- Borjas immigration surplus: `https://www.aeaweb.org/articles?id=10.1257/jep.9.2.3`
   286	- Card immigrant inflows/local labor markets: `https://davidcard.berkeley.edu/papers/immig-inflows.pdf`
   287	- Goldsmith-Pinkham, Sorkin & Swift shift-share critique: `https://www.aeaweb.org/articles?id=10.1257/aer.20181047`
   288	- Ottaviano & Peri immigrant/native substitution: `https://academic.oup.com/jeea/article-abstract/10/1/152/2297898`
   289	- Buchanan club goods: `https://www.jstor.org/stable/2552442`
   290	- Kerr & Lincoln high-skill innovation: `https://www.nber.org/papers/w15768`
   291	- Hunt & Gauthier-Loiselle immigration and innovation: `https://www.aeaweb.org/articles?id=10.1257/mac.2.2.31`
   292	- Ostrom social-ecological systems/resource governance: `https://www.science.org/doi/10.1126/science.1172133`; `https://pubmed.ncbi.nlm.nih.gov/19628857/`
   293	- Pettigrew & Tropp intergroup contact meta-analysis: `https://pubmed.ncbi.nlm.nih.gov/16737372/`; `https://ideas.wharton.upenn.edu/wp-content/uploads/2018/07/Pettigrew-Tropp.pdf`
   294	- Quillian perceived group threat: `https://www.semanticscholar.org/paper/Prejudice-as-a-response-to-perceived-group-threat%3A-Quillian/d4ceb81eb7a2e67d10db27545b8f2ec6c2702cd7`; `https://perception.org/other-publications/prejudice-as-a-response-to-perceived-group-threat-population-composition-and-anti-immigrant-and-racial-prejudice-in-europe/`
   295	- Alesina, Miano & Stantcheva on immigration and redistribution perceptions: `https://www.nber.org/papers/w24733`; `https://www.nber.org/system/files/working_papers/w24733/w24733.pdf`
   296	- Hainmueller & Hopkins public attitudes review: `https://www.annualreviews.org/content/journals/10.1146/annurev-polisci-102512-194818`
   297	- Kahan motivated numeracy: `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2319992`
   298	- Alesina & Glaeser diversity/redistribution: `https://academic.oup.com/book/36351`
   299	- Putnam diversity/social capital: `https://onlinelibrary.wiley.com/doi/10.1111/j.1467-9477.2007.00176.x`
   300	- McCombs & Shaw agenda setting: `https://academic.oup.com/poq/article-abstract/36/2/176/1853310`
   301	- Petrocik issue ownership: `https://www.jstor.org/stable/2111797`
   302	- van Oorschot deservingness criteria: `https://www.tandfonline.com/doi/abs/10.1080/713701159`
   303	- Entman framing: `https://fbaum.unc.edu/teaching/articles/J-Communication-1993-Entman.pdf`; `https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1460-2466.1993.tb01304.x`
   304	- Stone causal stories: `https://www.uvm.edu/~dguber/POLS293/articles/stone.pdf`; `https://academic.oup.com/psq/article/104/2/281/7134156`
   305	- Multiple Streams/Kingdon overview and refinement: `https://pmc.ncbi.nlm.nih.gov/articles/PMC8861624/`; `https://www.cambridge.org/core/elements/multiple-streams-and-policy-ambiguity/FBA20248D4A359D38AF7083D00F5149E`
--- END FILE: research/immigration-thesis-generator-audit-2026-06-16.md ---

--- BEGIN FILE: research/immigration-mexico-npv-population-synthesis-2026-06-15.md ---
     1	# Mexico NPV, population denominator, and full ledger — synthesis (2026-06-15)
     2	
     3	**Trigger:** Post-sweeps 23–32 session + full-ledger critique (local, justice, legal costs not in NAS headline).
     4	
     5	**Frame:** [FRAMING-SENSITIVE]
     6	
     7	**Warehouse:** `immigration_fiscal_union.duckdb`, `immigration_context.duckdb`
     8	
     9	**Mining:** `.mining/immigration-lifetime-cluster-q-stock-flow.json`, `.mining/immigration-lifetime-cluster-r-full-ledger.json`
    10	
    11	**Generators:** `immigration-lifetime-fiscal-generators.md` §Q, §R
    12	
    13	---
    14	
    15	## I. Conclusions (executive)
    16	
    17	### 1. There is no defensible scalar
    18	
    19	Honest fiscal object is a **vector across ledger layers ℓ**:
    20	
    21	`lifetime_npv | school_burden | state_local | admin_enforcement | justice_courts | episodic_local`
    22	
    23	**Kill:** Any single "Mexico net +" or "Mexico net −" without ℓ tags is layer laundering.
    24	
    25	### 2. NAS +$45,631/adult is a synthetic age-25 benchmark, not stock NPV
    26	
    27	| What +$46k is | What it is NOT |
    28	|---------------|----------------|
    29	| NAS Table 8-13 **individual age-at-arrival-25** education-mix benchmark | Actual remaining-lifetime NPV of current Mexico-born stock |
    30	| Federal + some state/local inside NAS cell | School burden for current HH kids (same-universe origin row currently withheld) |
    31	| Public goods **excluded** | Descendants / US-born kids path |
    32	| 2012$, 3%, 75yr | CBP/ICE/detention (~$2.1k/yr if ÷ stock) |
    33	| Composition-weighted **mean** | EOIR / immigration courts |
    34	| Applied to ACS current 25–64 education weights | Net after all local costs; NYC/Chicago shelter (surge episodic) |
    35	
    36	NAS Table 8-13 is explicitly a comparison of an immigrant **entering at age 25** with a native-born person followed from age 25. The warehouse applies those age-25 education cells to the current Mexico-born 25–64 stock because public data lack a full age-at-arrival × education × origin NPV table. That makes `+$45,631/adult` a **synthetic composition benchmark**, not a measured lifetime NPV for existing residents. [SOURCE: NAS 2017 Table 8-13 text via local PDF; `country_fiscal_tensor` notes] [INFERENCE]
    37	
    38	**Honest short-horizon (built):** federal annual proxy remains **+$1,519/adult/yr**; the origin `federal − school` row is **withheld** after a scenario-household numerator vs full-microsim denominator mismatch was confirmed. [SOURCE: `v_three_layer_annual`; `immigration-conclusion-audit-running-fixes.md`]
    39	
    40	**Illustrative lifetime stack [INFERENCE]:**
    41	
    42	| Step | $/adult |
    43	|------|---------|
    44	| NAS age-25 education-mix benchmark | +$45,631 |
    45	| − school annuitized | unresolved — needs same-universe origin school row |
    46	| − CBO state/local surge annuitized ($657/yr) | −$15,300 |
    47	| − enforcement if fully loaded ($2,100/yr) | −$49,000 |
    48	| **Band** | **−$37k to +$28k** |
    49	
    50	Enforcement allocation is **[FRAMING-SENSITIVE]** — fixed vs marginal split not resolved.
    51	
    52	### 3. Multiply-out (synthetic NAS age-25 benchmark only)
    53	
    54	| Bucket | N | Share | NAS/cell | Bucket $ |
    55	|--------|---|-------|----------|----------|
    56	| `<HS` | 3.96M | 46.6% | −$109k | −$431.5B |
    57	| HS | 2.43M | 28.6% | +$49k | +$119.1B |
    58	| some college | 1.24M | 14.6% | +$205k | +$253.7B |
    59	| BA+ | 0.87M | 10.2% | +$514k | +$446.4B |
    60	| **Total** | **8.50M** | | | **+$387.7B** |
    61	
    62	**10.2% BA+** — mean is pulled by thin top tail; median person likely `<HS` or HS.
    63	
    64	**Do not read `+$387.7B` as an actual stock asset.** It is `current education mix × NAS age-25 cells`. The denominator is a current 25–64 stock: only **17.4%** of Mexico-origin adults in the microsim are age 25–34, while **53.2%** are age 45–64. The table does not model their remaining working years, prior U.S. taxes/transfers, arrival age, return migration, or legal-status path. [SOURCE: `acs_origin_household_federal_microsim_2023` age bands; NAS 2017 Table 8-13] [INFERENCE]
    65	
    66	### 4. Denominator discipline
    67	
    68	- **8.5M** = Mexico **birthplace**, foreign-born, 25–64, ACS self-report [SOURCE: microsim]
    69	- **≠** 4.3M Mexico-**unauthorized** (Pew 2023)
    70	- **≠** 437k `origin_national` (recent `<HS` only — wrong denominator)
    71	
    72	### 5. Biden “10M+ illegals”
    73	
    74	- **~10.8M encounters** (events) + **~2M gotaways** ≠ net residents
    75	- **Net stock Δ:** Pew **+3.5M** (2021→23); CIS **+5.6M** (2021→25)
    76	- **Mexico unauthorized flat ~4.3M**; post-2021 unauthorized-stock growth was non-Mexico on this ledger
    77	
    78	### 6. Build priorities (from generators)
    79	
    80	1. `v_full_fiscal_stack` view + overlap matrix (G-LIF-R05)
    81	2. Legal-status split within `mexico_origin` (G-LIF-Q03)
    82	3. EOIR → origin rollup (G-LIF-R04)
    83	4. CBP/ICE marginal allocation rule (G-LIF-R03)
    84	5. Never subtract `local_flow` $20,907/pupil from per-adult NPV (G-LIF-R02)
    85	
    86	---
    87	
    88	## II. Generators
    89	
    90	### Cluster Q — stock vs flow
    91	
    92	| ID | One-line |
    93	|----|----------|
    94	| G-LIF-Q01 | Encounter ≠ stock — IDENT unique subjects before per-capita |
    95	| G-LIF-Q02 | Gotaway trap — never sum gotaways + encounters + Pew stock |
    96	| G-LIF-Q03 | Birthplace ≠ legal status |
    97	| G-LIF-Q04 | Education-mix mean ≠ median — ship bucket table |
    98	| G-LIF-Q05 | Pew 14M vs CIS 15.8M band on unauthorized-layer only |
    99	
   100	### Cluster R — full ledger stack
   101	
   102	| ID | One-line |
   103	|----|----------|
   104	| G-LIF-R01 | NAS scope lock — list in/excluded ℓ before net claim |
   105	| G-LIF-R02 | School double-count guard vs descendants |
   106	| G-LIF-R03 | CBP/ICE allocation rule (fixed vs marginal) |
   107	| G-LIF-R04 | EOIR justice/court layer by nationality |
   108	| G-LIF-R05 | Publish stacked vector only — `v_full_fiscal_stack` |
   109	
   110	Full prompts: `immigration-lifetime-fiscal-generators.md` §Q, §R.
   111	
   112	---
   113	
   114	## III. Warehouse layers (`mexico_origin`)
   115	
   116	| fiscal_layer | $/adult | Netted into lifetime_npv? |
   117	|--------------|---------|---------------------------|
   118	| `lifetime_npv` | +$45,631 synthetic age-25 benchmark | — |
   119	| `federal_annual` | +$1,519/yr | partial overlap |
   120	| `school_burden_per_adult` | **withheld** — prior `$771/yr` mixed scenario-household numerator with full-stock adult denominator | **NO** |
   121	| `net_crude_federal_minus_school` | **withheld** — prior `+$748/yr` depends on the superseded school row | **NO** |
   122	| `local_flow` | $20,907/pupil | **NO** (unit mismatch) |
   123	
   124	Missing from warehouse rollup: EOIR $/case, ICE bed-days allocated, shelter episodic per Mexico adult.
   125	
   126	---
   127	
   128	## IV. Disconfirmation
   129	
   130	| Hypothesis | Result |
   131	|------------|--------|
   132	| +$46k = immigrant pays for themselves all-in | **Unsupported / not a valid export** — school, admin, courts, shelter not netted |
   133	| Subtract `local_flow` from NPV | **Falsified** — per_pupil ≠ per_adult burden |
   134	| Use the old `$771` school row or `+$748` crude net as current Mexico-origin fiscal result | **Falsified** — same-universe school numerator is not built |
   135	| 10M+ net new unauthorized since Biden | **Falsified** — stock +3.5M to +5.6M |
   136	| Mexico drove post-2021 unauthorized-stock growth | **Falsified on this stock ledger** — Mexico unauthorized flat |
   137	| NAS `<HS` cell applies to the whole Mexico-origin stock | **Falsified** by education mix — but actual current-stock NPV remains unmeasured |
   138	| +$387.7B is the actual lifetime NPV of the current Mexico-born stock | **Falsified** — it is current ACS education weights × NAS age-25 cells |
   139	
   140	---
   141	
   142	## V. Open gaps
   143	
   144	1. Build `v_full_fiscal_stack` + overlap matrix (R-005).
   145	2. Legal-status imputation for Mexico microsim cells.
   146	3. EOIR nationality → `mexico_origin` court cost proxy.
   147	4. ICE marginal $/bed-day × detention probability by status path.
   148	5. EU27/NH-white lifetime rollup (education mix).
   149	6. Surge cohort vs Mexico stock NAS cell separation.
   150	7. Age-at-arrival/current-age NPV mapping for Mexico stock; current warehouse lacks it.
   151	
   152	---
   153	
   154	## Revisions
   155	
   156	| Date | Change |
   157	|------|--------|
   158	| 2026-06-15 | Initial: multiply-out, denominator, Biden stock vs flow (cluster Q) |
   159	| 2026-06-15 | Full-ledger critique: NAS ≠ net; cluster R generators; stacked bounds −$37k to +$28k |
   160	| 2026-06-16 | Corrected lifetime label: `+$45,631/adult` and `+$387.7B` are synthetic NAS age-25 education-mix benchmarks, not actual current-stock lifetime NPV |
   161	| 2026-06-16 | Reframed `+$46k = pays for themselves all-in` from falsified to unsupported/not a valid export: omitted ledgers block the inference, but the full all-in sign remains unmeasured. See `immigration-conclusion-audit-running-fixes.md`. |
   162	| 2026-06-16 | Scoped "Mexico drove surge" to post-2021 unauthorized-stock growth; the flat Mexico stock result does not adjudicate encounter events or receiver-load composition. See `immigration-conclusion-audit-running-fixes.md`. |
   163	| 2026-06-16 | Replaced the stale `$771/+748` warehouse-layer rows with withheld status after the same-universe school guard. See `immigration-conclusion-audit-running-fixes.md`. |
--- END FILE: research/immigration-mexico-npv-population-synthesis-2026-06-15.md ---

--- BEGIN FILE: research/immigration-claims-evolution-ledger-2026-04-23.md ---
     1	# Immigration Claims Evolution Ledger
     2	
     3	Date: 2026-04-23
     4	
     5	Purpose: collapse the repo's immigration claims into a claim-by-claim evolution map: what the claim now says, how it changed, what it connects to, the takeaway, and the common misunderstanding. This is a synthesis over existing repo artifacts, not a fresh external verification pass. Source tags point to the repo documents that carry the underlying citations, data pulls, or prior audits.
     6	
     7	**Status note (2026-06-16):** June denominator and model-review passes narrowed several older shortcuts: E-Verify is an observed mandate-margin wage test, not measured labor-supply contraction; capacity/surge evidence is descriptive or correlational unless a design identifies the mechanism; and origin `federal - school` signs are withheld until school numerators and adult denominators share the same universe. [SOURCE: research/immigration-conclusion-audit-running-fixes.md]
     8	
     9	## Claim List
    10	
    11	### 1. The central question is not "is immigration good or bad?"
    12	
    13	The repo's most important evolution is away from a scalar verdict and toward incidence accounting. Early frames treated the dispute as "immigration helps" versus "immigration hurts"; the current frame splits global migrant gains, national GDP/federal revenue, destination-country per-capita welfare, state/local budgets, housing, schools, labor markets, and political legitimacy. The takeaway is that a single sign is structurally misleading unless the ledger and welfare weights are named. The misunderstanding is to treat GDP, federal deficit reduction, local budget strain, and native welfare as if they answer the same question. [SOURCE: research/immigration-reasoning-evolution-2026-04-21.md] [SOURCE: research/immigration-claims-matrix-2026-04-11.md] [SOURCE: research/immigration-confidence-ladder.md] [INFERENCE]
    14	
    15	### 2. The strongest durable finding is an incidence split: federal/national channels can be favorable while local channels are negative.
    16	
    17	The claim evolved from a vague "fiscal impact" debate into a level-of-government split. CBO 2024 supports a favorable federal/macroeconomic channel for the 2021-2026 surge scenario: more workers, more revenue, higher GDP, and lower federal deficits. CBO 2025 supports a less favorable state/local 2023 channel: direct state/local net costs around $9.2B and potential net costs around $9.8B for added residents. The takeaway is not "immigration pays for itself" or "immigration bankrupts us"; it is that fiscal winners and losers are institutionally separated. The misunderstanding is using federal gains to dismiss city, school, shelter, and state Medicaid pressure, or using local pressure to deny federal revenue effects. [SOURCE: research/immigration-claims-matrix-2026-04-11.md] [SOURCE: research/immigration-verified-findings-report-2026-04-10.md] [SOURCE: research/fiscal-impact-unauthorized-immigration-research-memo.md]
    18	
    19	### 3. Unauthorized-immigration fiscal totals are not cleanly identifiable from one headline estimate.
    20	
    21	The repo moved from looking for "the" unauthorized fiscal number toward a sensitivity model. The sign depends heavily on public-goods attribution, child-cost and child-contribution treatment, time horizon, discount rate, marginal versus average benefit costs, and which government level is counted. NAS/Orrenius-style methods can turn positive under marginal public goods and long horizons; Heritage/CIS-style estimates get large costs through average public goods, child attribution, and shorter horizons. The takeaway is that fiscal estimates are mostly methodology machines. The misunderstanding is to quote one number as empirical ground truth without disclosing the model choices that produced it. [SOURCE: research/fiscal-impact-unauthorized-immigration-research-memo.md] [SOURCE: research/immigration-confidence-ladder.md]
    22	
    23	### 4. The repo's own federal microsimulation is not yet a trustworthy fiscal estimator.
    24	
    25	An important correction in the project is that the early federal prototype should not be used as a final answer. The verified-findings memo flags a CPS household-income recode problem that collapsed donor cells into a low-income bucket, making the federal number unresolved. The takeaway is that the federal-positive/local-negative thesis is supported by official and literature evidence, but the repo's custom federal microsim is not yet the proof. The misunderstanding is to confuse "the direction is plausible from external sources" with "our local model has solved the number." [SOURCE: research/immigration-verified-findings-report-2026-04-10.md] [SOURCE: research/immigration-confidence-ladder.md] [LIMIT]
    26	
    27	### 5. "Low-skill immigrant" was narrowed from a rhetorical category to a measured subgroup.
    28	
    29	The repo corrected "low-skill" from a broad cultural or low-wage label into a specific ACS subgroup: foreign-born adults age 25-64, recent arrival in the relevant analysis, and less than high school where `SCHL < 16`; `SCHL = 16` is a regular high-school diploma, not dropout status. The takeaway is that several claims only apply to a narrower less-than-HS population, not to all non-college immigrants or all unauthorized immigrants. The misunderstanding is category inflation: taking findings about one education/origin/arrival subgroup and applying them to all immigration. [SOURCE: research/immigration-verified-findings-report-2026-04-10.md] [SOURCE: research/immigration-confidence-ladder.md] [DATA]
    30	
    31	### 6. Origin composition matters because local burden is family-structure and destination-specific.
    32	
    33	The project moved from per-person averages to origin-by-household and destination exposure. Recent low-education origin counts are concentrated in Mexico, Guatemala, Honduras, El Salvador, Cuba, Haiti, Vietnam, China, Colombia, and Brazil, but the child-burden profile differs sharply by origin. The corrected household-weighted school-age child metrics put Afghanistan, Honduras, Myanmar, El Salvador, Mexico, and Guatemala near the top for school exposure. The takeaway is that local fiscal strain is not just "how many immigrants"; it is who arrives, household structure, school-age children, and where they settle. The misunderstanding is treating immigrant fiscal impact as demographically homogeneous. [SOURCE: research/immigration-verified-findings-report-2026-04-10.md] [SOURCE: research/immigration-claims-matrix-2026-04-11.md] [DATA]
    34	
    35	### 7. Housing exposure became more central than the earlier evidence base allowed.
    36	
    37	The repo initially treated housing as one component among many; later work elevated it because immigrants concentrate in high-rent, low-elasticity metro areas. PUMA-level rent exposure showed high weighted destination rent for groups including China, Colombia, Brazil, Vietnam, India, and Venezuela, while the confidence ladder adds a stronger descriptive result that high foreign-born-share MSAs have lower Saiz housing-supply elasticity. The takeaway is that housing is not a decorative local-cost caveat; it is a core incidence channel. The misunderstanding is saying "immigration does not raise national CPI much" as if that resolves rent, crowding, and shelter pressure in constrained destinations. [SOURCE: research/immigration-verified-findings-report-2026-04-10.md] [SOURCE: research/immigration-confidence-ladder.md] [SOURCE: research/immigration-claims-matrix-2026-04-11.md]
    38	
    39	### 8. The old labor-market collapse story weakened, but the "no worker effects" story is also too broad.
    40	
    41	The repo's labor view evolved through Card/Borjas/E-Verify and QWI work. The current E-Verify surface shows no statistically significant positive QWI wage effect in the observed mandate margin and cuts against large native wage gains there, while leaving small effects, scaled Borjas benchmarks, and out-of-margin shocks unresolved. Surge-era and capacity-constrained analyses also prevent upgrading older average-effect results into "workers are unaffected everywhere." The takeaway is that crude native job-collapse claims are weak in the best marginal-policy evidence, while wage progression, housing-mediated real income, and local capacity channels remain open. The misunderstanding is treating "small average wage effect" as "no economic incidence on workers." [SOURCE: research/immigration-confidence-ladder.md] [SOURCE: research/immigration-reasoning-evolution-2026-04-21.md] [SOURCE: research/immigration-evidence-base-audit.md] [SOURCE: research/immigration-conclusion-audit-running-fixes.md]
    42	
    43	### 9. Pre-2020 marginal immigration studies do not settle surge-era politics or receiver-city capacity.
    44	
    45	The reasoning-evolution memo explicitly demotes older labor-market evidence as a complete answer to the 2021-2024 regime. The surge changed the object from marginal labor-market absorption to shelter saturation, court backlogs, state/local budgets, housing, and legitimacy under concentrated arrivals. The takeaway is that the old papers remain valuable for labor-market margins, but they are not sufficient for mass-flow/capacity claims. The misunderstanding is to cite Mariel, Card 1990, or H-2B lottery studies as if they answer Denver shelter overload, NYC migrant spending, or EOIR venue pressure. [SOURCE: research/immigration-reasoning-evolution-2026-04-21.md] [SOURCE: research/immigration-evidence-base-audit.md] [SOURCE: research/immigration-frontier-rethink-2026-04-22.md]
    46	
    47	### 10. The capacity threshold claim was demoted from a universal cutoff to a stress-marker surface.
    48	
    49	The project tried to find county-level thresholds using flow/capacity and outcome panels, then narrowed the claim after critique. Descriptive load/capacity markers survived robustness checks, but clean annual pre-COVID wage windows did not line up and employment signals looked more confounded. The current claim is that flow-to-capacity is a strong screening surface, not a proven universal causal breakpoint. The takeaway is to use it for case selection and hypothesis generation, not as a final law. The misunderstanding is either declaring "thresholds proved" or throwing away the signal because one annual wage panel is not clean. [SOURCE: research/immigration-reasoning-evolution-2026-04-21.md] [SOURCE: research/immigration-frontier-rethink-2026-04-22.md] [LIMIT]
    50	
    51	### 11. Receiver-node saturation is now the frontier causal-design object.
    52	
    53	The repo's newest move is from national averages and county screens to receiver nodes: specific cities/counties where recent-entry exposure, housing stress, shelter capacity, EOIR load, labor indicators, and electoral shifts can be compared together. The first public-data kill test finds Miami-Dade and NYC as the strongest survivors, Bexar as second-tier, and Harris, Denver, Boston, Chicago, DC, and El Paso as mixed or channel-specific. The takeaway is that the most informative cases are not "high immigrant share" in general; they are places where multiple pressure channels synchronize. The misunderstanding is assuming every politically salient receiver city has the same mechanism. [SOURCE: research/immigration-receiver-node-kill-test-2026-04-23.md] [SOURCE: research/immigration-frontier-rethink-2026-04-22.md]
    54	
    55	### 12. NYC and Miami-Dade support the receiver-node theory more cleanly than Denver or Chicago.
    56	
    57	The kill test found Miami-Dade and NYC with high recent-entry exposure, high renter/crowding stress, elevated EOIR load relative to 2017-2019, and above-median 2024 GOP shift. Denver showed shelter and EOIR pressure but weaker ACS exposure and household stress; Chicago showed strong court load but weaker synchronization across ACS, housing, and shelter metrics. The takeaway is that the theory is not "migrant buses caused all receiver-city stress"; it is "some nodes show synchronized overload and others show narrower channels." The misunderstanding is reading any single spending headline, shelter count, or court docket as sufficient proof of broad local saturation. [SOURCE: research/immigration-receiver-node-kill-test-2026-04-23.md] [DATA] [INFERENCE]
    58	
    59	### 13. Domestic newcomer comparisons were corrected: the ratio is contextual, not a burden ratio.
    60	
    61	The repo previously leaned too hard on domestic-versus-abroad newcomer ratios. The confidence ladder now treats domestic newcomer counts as much larger than moved-from-abroad counts at the median county, but explicitly says this is not a burden ratio; the safer order-of-magnitude is about 20.5x, not the older 33x. The takeaway is that resident-weighted exposure matters because the typical resident's encounter with migration differs from national totals. The misunderstanding is using domestic mobility to dismiss immigrant-specific service/court/shelter burdens, or using immigrant arrival counts without resident exposure context. [SOURCE: research/immigration-confidence-ladder.md] [SOURCE: research/immigration-reasoning-evolution-2026-04-21.md] [LIMIT]
    62	
    63	### 14. Political feedback became first-order, not an afterthought.
    64	
    65	The repo's political claim evolved from "immigrants may vote differently" to a broader feedback model: citizen political response, local overload, perceived loss of institutional control, and legitimacy costs can matter before naturalization or voting. Receiver cities swung more Republican in 2024 than comparable nonreceivers in the current medium-confidence correlation, but causality and voter motivation remain confounded. The takeaway is that political-response evidence belongs in the policy cost function even when immigrants themselves do not vote. The misunderstanding is to restrict political externalities to immigrant median-voter effects, or to treat citizen response as irrational noise outside welfare analysis. [SOURCE: research/immigration-confidence-ladder.md] [SOURCE: research/immigration-economist-rhetorical-failures-2026-04-22.md] [SOURCE: research/immigration-receiver-node-kill-test-2026-04-23.md] [SOURCE: research/immigration-conclusion-audit-running-fixes.md]
    66	
    67	### 15. The crime objection is weaker than many restrictionist arguments imply.
    68	
    69	The crime memo's current position is high confidence on the directional claim that unauthorized immigrants commit crimes at lower rates than native-born U.S. citizens in the best U.S. evidence, with moderate confidence about exact magnitude and caution around post-2020 surge generalization. The race-composition caveat narrows but does not erase the gap. The takeaway is that crime should not be treated as the strongest empirical restrictionist case in the U.S. context. The misunderstanding is using ICE docket stock counts, pending charges, or outlier/non-peer-reviewed classifications as annual crime-rate evidence. [SOURCE: research/immigration-crime-rates-unauthorized-vs-native-born.md]
    70	
    71	### 16. Open-borders global gains survive directionally, but the "double world GDP" slogan is not a central forecast.
    72	
    73	The repo shifted from treating open-borders gains as either fake or decisive to bounding them. Large place-premium gains are plausible, but literal near-doubling depends on stylized assumptions and rich-destination capacity remaining intact. The open-borders bounds memo shows that a +200M migrant scenario with a conservative annual gain can still produce large global gains, yet requires enormous housing absorption and has nontrivial incumbent-loss break-even thresholds. The takeaway is that global-gains arguments are real but capacity-constrained. The misunderstanding is converting upper-bound model outputs into operational forecasts, or dismissing global gains because destination local strain is real. [SOURCE: research/immigration-open-borders-break-even-bounds-2026-04-22.md] [SOURCE: research/immigration-reasoning-evolution-2026-04-21.md] [SOURCE: research/immigration-economist-rhetorical-failures-2026-04-22.md]
    74	
    75	### 17. Welfare conclusions depend on whose welfare gets counted.
    76	
    77	The confidence ladder now treats the open-borders welfare verdict as strongly framing-sensitive. With zero weight on migrant welfare, losses to destination incumbents dominate by construction in many setups; with meaningful migrant welfare weight, large place-premium gains can dominate unless destination capacity erosion is severe. The takeaway is that the moral and empirical disputes are entangled but not identical. The misunderstanding is pretending the welfare-weight choice is a neutral empirical parameter, or hiding a citizen-only frame behind universal language. [SOURCE: research/immigration-confidence-ladder.md] [SOURCE: research/immigration-open-borders-break-even-bounds-2026-04-22.md] [FRAMING-SENSITIVE]
    78	
    79	### 18. Economist "consensus" claims usually fail by ledger-switching, not because every cited paper is false.
    80	
    81	The evidence-base audit found that core pro-immigration papers are often not factually wrong on their own objects: small wage effects, complementarity, service-price channels, firm output, and indirect fiscal benefits can all be real. The failure is using partial papers as whole-welfare answers. The rhetorical-failures memo labels the recurring pattern: ledger switching, upper-bound laundering, marginal-to-mass extrapolation, capacity erasure, and underpriced political feedback/local incidence. The takeaway is that the strongest critique is overextension, not fraud. The misunderstanding is either "economists are lying" or "economists found one positive channel, so the whole debate is settled." [SOURCE: research/immigration-evidence-base-audit.md] [SOURCE: research/immigration-economist-rhetorical-failures-2026-04-22.md]
    82	
    83	### 19. Caplan/Friedman-style arguments are strongest globally and normatively, weakest on local incidence.
    84	
    85	The Caplan audit concludes that migrant/global gains, crime skepticism, and employment-collapse skepticism survive better than taxpayer-protection, worker, political-externality, and capacity claims. Friedman-style liberty/global arguments remain coherent, but do not settle native-local welfare or institutional-capacity questions. The takeaway is that these theorists are not useless; they are answering a different and often broader question than city-budget, school, rent, and shelter ledgers. The misunderstanding is treating moral permission for freer movement as a solved empirical local-welfare theorem. [SOURCE: research/immigration-bryan-caplan-claims-audit-2026-04-21.md] [SOURCE: research/immigration-claims-matrix-2026-04-11.md] [FRAMING-SENSITIVE]
    86	
    87	### 20. Health-cost evidence weakened a crude immigrant-cost story but did not resolve the fiscal ledger.
    88	
    89	The SIPP-MEPS bridge work produced a complete 98/98 match and found working-age foreign-born payer-cost patterns lower than U.S.-born comparisons across private, public-only, and uninsured cells in the cited public MVP. The takeaway is that crude "immigrants are more expensive health users" claims are not supported by that module. The misunderstanding is to upgrade lower working-age health expenditures into a full fiscal answer; healthcare is one channel and excludes schools, housing, courts, shelters, taxes, children, and lifetime horizons. [SOURCE: research/immigration-claims-matrix-2026-04-11.md] [DATA] [LIMIT]
    90	
    91	### 21. School burden is real as exposure, but final magnitude claims remain weak.
    92	
    93	The repo corrected household weighting and found strong origin heterogeneity in school-age children per linked household, which supports school-exposure concerns for some origin groups and localities. But the confidence ladder still rates magnitude claims for local school burden as weak because district assignment, English-learner intensity, special services, timing, and local finance formulas are not fully pinned down. The takeaway is that "schools matter" is strong; "this exact dollar burden by origin/place" is not. The misunderstanding is to treat either per-pupil spending times child counts as final cost, or to dismiss school costs because lifetime descendants may later contribute. [SOURCE: research/immigration-verified-findings-report-2026-04-10.md] [SOURCE: research/immigration-confidence-ladder.md] [LIMIT]
    94	
    95	### 22. Mass deportation output-shock claims are calibration bounds, not precise predictions.
    96	
    97	The confidence ladder includes a medium-confidence calibration that deporting 7M unauthorized workers could imply an output shock around $1.5T-$2.3T, roughly 5%-8% of GDP under the stated assumptions. The takeaway is that deportation is not a costless reversal of immigration; labor, firms, supply chains, and demand would adjust painfully. The misunderstanding is to read this as a fully identified forecast, or to ignore transition costs because a static fiscal ledger looks negative. [SOURCE: research/immigration-confidence-ladder.md] [LIMIT]
    98	
    99	### 23. AGI/automation uncertainty shifts emphasis toward near-term absorption rather than lifetime precision.
   100	
   101	The verified-findings memo explicitly notes that an AGI-soon frame makes very long-run lifetime NPV less decisive and raises the value of short-run transition analysis: housing, schooling, service capacity, legitimacy, and institutional response. The takeaway is not that long-run fiscal analysis is useless, but that 75-year precision may be less decision-relevant if labor-market structure changes radically. The misunderstanding is treating lifetime fiscal estimates as the only serious policy object when near-term capacity constraints can dominate political feasibility. [SOURCE: research/immigration-verified-findings-report-2026-04-10.md] [FRAMING-SENSITIVE] [LIMIT]
   102	
   103	## Current Synthesis
   104	
   105	The repo's current position is best stated as: immigration creates large real gains for migrants and often favorable national/federal channels, while also creating concentrated local burdens through housing, schools, shelters, courts, and political legitimacy when flow, composition, destination, and capacity line up badly. The strongest next analysis is not another abstract pro/con literature review; it is receiver-node causal work with cleaner residence mapping, service-load measures, and resident-weighted exposure. [SOURCE: research/immigration-reasoning-evolution-2026-04-21.md] [SOURCE: research/immigration-receiver-node-kill-test-2026-04-23.md] [SOURCE: research/immigration-frontier-rethink-2026-04-22.md] [INFERENCE]
--- END FILE: research/immigration-claims-evolution-ledger-2026-04-23.md ---

--- BEGIN FILE: research/immigration-economist-one-pager-2026-04-22.md ---
     1	# Immigration economists keep answering the wrong question — 2026-04-22
     2	
     3	**Purpose:** Short public-facing one-pager.  
     4	**Use:** Forwardable summary of the strongest fair critique of the mainstream pro-immigration economics line after the repo's current evidence.
     5	
     6	**Status update (2026-06-16):** Public-facing summary only. Later audit passes narrowed the capacity evidence to descriptive stress screens, gross receiver-load evidence, and correlational political-response signals. Do not read this as a causal fiscal-load-to-vote model, a native-exit proof, or an origin `federal - school` estimate. [SOURCE: research/immigration-conclusion-audit-running-fixes.md]
     7	
     8	## The core problem
     9	
    10	The slick economist case for immigration usually works by answering a **different question** than the one ordinary people are asking.
    11	
    12	When people ask:
    13	
    14	1. `Will this be good for the country I live in?`
    15	2. `Will this help or hurt current residents?`
    16	3. `What happens to housing, schools, wages, and local capacity?`
    17	
    18	the economist often answers:
    19	
    20	1. `Migrants gain a lot`
    21	2. `World output rises`
    22	3. `Aggregate GDP goes up`
    23	
    24	Those are real effects.
    25	
    26	They are also **not the same ledger**.
    27	
    28	That is the central bait-and-switch. [SOURCE: research/immigration-claims-matrix-2026-04-11.md] [SOURCE: research/immigration-reasoning-evolution-2026-04-21.md]
    29	
    30	## The seven standard moves
    31	
    32	### 1) Ledger switching
    33	
    34	They move back and forth between:
    35	
    36	1. migrant welfare
    37	2. world output
    38	3. national aggregate GDP
    39	4. GDP per person
    40	5. incumbent local welfare
    41	
    42	Then they speak as if one positive result settles them all.
    43	
    44	It does not. [SOURCE: research/immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md]
    45	
    46	### 2) Upper-bound laundering
    47	
    48	They cite stylized open-borders papers and then talk as if near-doubling world GDP is a realistic baseline.
    49	
    50	It is not.
    51	
    52	The strongest repo reading is:
    53	
    54	1. large gains are plausible in principle
    55	2. the near-doubling rhetoric is an upper-bound extrapolation
    56	3. it depends on destination-country capacity staying largely intact
    57	
    58	[SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md]
    59	
    60	### 3) Marginal-to-mass extrapolation
    61	
    62	Economists often have evidence that moderate inflows are absorbed without obvious collapse.
    63	
    64	They do **not** therefore have evidence that:
    65	
    66	1. concentrated surge inflows
    67	2. weak housing response
    68	3. shelter overload
    69	4. school and court strain
    70	5. multi-year political response
    71	
    72	will also be absorbed cleanly.
    73	
    74	That is a different regime. [SOURCE: research/immigration-frontier-rethink-2026-04-22.md]
    75	
    76	### 4) Capacity erasure
    77	
    78	Housing, shelter, schools, courts, and administrative systems are not one small friction term.
    79	
    80	They are separate bottlenecks.
    81	
    82	The repo's current descriptive screens point to `flow x capacity x composition x regime`, not a simple stock-share story. That is a research object and warning surface, not clean causal identification. [SOURCE: research/immigration-capacity-frontier-2026-04-21.md] [SOURCE: research/immigration-receiver-failure-atlas-2026-04-22.md]
    83	
    84	### 5) Denominator masking
    85	
    86	If a city expands beds or emergency capacity in response to a surge, then a ratio like `PIT/HIC` can look stable even while absolute sheltered load and gross emergency burden rise.
    87	
    88	That is why the receiver work had to check absolute load, not just ratios.
    89	
    90	`Chicago` is the clearest ratio-vs-absolute-load warning in that pass. [SOURCE: research/immigration-receiver-counterfactuals-2026-04-22.md]
    91	
    92	### 6) Political-economy erasure
    93	
    94	The economist often reduces politics to:
    95	
    96	1. immigrant voting
    97	2. maybe welfare-state demand
    98	
    99	But the real channels also include:
   100	
   101	1. citizen political response
   102	2. legitimacy effects
   103	3. assignment rules
   104	4. emergency procurement
   105	5. right-to-shelter obligations
   106	
   107	[SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md] [SOURCE: research/full-spectrum-costs-unauthorized-immigration-research-memo.md]
   108	
   109	### 7) Aggregate-output trump card
   110	
   111	If aggregate GDP rises, they act as if the argument is basically over.
   112	
   113	But the official U.S. evidence already blocks that move:
   114	
   115	1. aggregate GDP can rise
   116	2. GDP per person can fall
   117	3. CBO or narrow federal-proxy channels can be positive
   118	4. state/local and receiver gross-load channels can be negative or unresolved on the all-in net
   119	
   120	[SOURCE: research/immigration-claims-matrix-2026-04-11.md]
   121	
   122	## What the current evidence actually supports
   123	
   124	The honest current position is:
   125	
   126	1. migrant gains are real
   127	2. some national aggregate gains are real
   128	3. crude collapse rhetoric is too strong
   129	4. blanket economist optimism is also too strong
   130	5. destination incidence likely depends on `flow x capacity x composition x regime`, with current public-data evidence strongest as descriptive screening
   131	
   132	[SOURCE: research/immigration-economist-rhetorical-failures-2026-04-22.md]
   133	
   134	## The shortest fair summary
   135	
   136	The economist case is not wrong because immigration has no gains.
   137	
   138	It is wrong because it repeatedly uses a bounded efficiency argument to answer a different question:
   139	
   140	`Is this good for incumbent residents once housing, local capacity, and political-response channels are priced in?`
   141	
   142	That question is not answered by:
   143	
   144	1. place-premium gains
   145	2. aggregate GDP
   146	3. one-line “economists agree” survey rhetoric
   147	
   148	## Best final line
   149	
   150	**The economist case does not fail on first-order gains. It fails where it pretends those gains settle every ledger at once.**
   151	
   152	## Revisions
   153	
   154	| Date | Change | Trigger |
   155	|---|---|---|
   156	| 2026-06-16 | Scoped capacity, denominator, and political-response wording to descriptive/gross/correlational evidence rather than causal mechanism. | `research/immigration-conclusion-audit-running-fixes.md` capacity/surge corrections. |
--- END FILE: research/immigration-economist-one-pager-2026-04-22.md ---

--- BEGIN FILE: research/immigration-economist-debate-sheet-2026-04-22.md ---
     1	# Immigration economist debate sheet — 2026-04-22
     2	
     3	**Purpose:** Quote-driven sheet for live debate, writing, or adversarial review.  
     4	**Method:** Each row uses a short direct quote or exact title, identifies the hidden move, and gives the strongest repo-backed counter.
     5	
     6	**Status update (2026-06-16):** Use these as debate counters, not as causal proof. Later corrections keep capacity/load evidence descriptive, receiver fiscal evidence gross rather than net, and election evidence correlational rather than a fiscal-load-to-vote mechanism. [SOURCE: research/immigration-conclusion-audit-running-fixes.md]
     7	
     8	## How to use this
     9	
    10	For each claim:
    11	
    12	1. identify the `ledger`
    13	2. identify the `failure mode`
    14	3. answer with the shortest counter that forces the speaker back onto a single claim
    15	
    16	This sheet is not trying to prove immigration is bad on every ledger.
    17	It is trying to stop optimistic economist rhetoric from cheating. [SOURCE: research/immigration-economist-rhetorical-failures-2026-04-22.md]
    18	
    19	## Core challenge question
    20	
    21	Before engaging any claim, ask:
    22	
    23	`Which ledger are you talking about: migrants, world output, aggregate GDP, GDP per person, or incumbent residents?`
    24	
    25	That question alone kills a lot of bad argument. [SOURCE: research/immigration-claims-matrix-2026-04-11.md]
    26	
    27	## Debate table
    28	
    29	| Quote / claim | Source | Hidden move | Short counter | Strongest repo anchor |
    30	|---|---|---|---|---|
    31	| “`the average US citizen would be better off`” | Clark Center survey question [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/] | Compresses many ledgers into one survey answer | `That depends on which ledger you mean. Aggregate GDP, GDP per person, and local incumbent welfare already split apart in the official evidence.` | [immigration-claims-matrix-2026-04-11.md](/Users/alien/Projects/research/research/immigration-claims-matrix-2026-04-11.md:1) |
    32	| “`Unskilled natives likely to be worse off, skilled native better off. Who's average?`” | Liran Einav comment on Clark survey [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/] | Shows the survey’s headline already hides internal incidence conflict | `Exactly. Once the "average citizen" category breaks, the slogan loses its force.` | [immigration-economist-effects-matrix.md](/Users/alien/Projects/research/research/immigration-economist-effects-matrix.md:1) |
    33	| “`classical gains from trade`” | Oliver Hart comment on Clark survey [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/] | Uses general-equilibrium efficiency language to answer a local-incidence question | `Trade-style gains do not answer housing, shelter, school, or local fiscal incidence.` | [immigration-economist-effects-matrix.md](/Users/alien/Projects/research/research/immigration-economist-effects-matrix.md:1) |
    34	| “`welfare of immigrants, rather than residents`” | Jonathan Levin comment on Clark survey [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/] | Quietly admits the ledger switch | `Exactly. Migrant welfare can be strongly positive without proving current residents are better off.` | [immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md](/Users/alien/Projects/research/research/immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md:1) |
    35	| “`real income for many current Americans would rise, but social strains and inequality would also increase`” | Joseph Altonji comment on Clark survey [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/] | Hints at the omitted right-hand side without pricing it | `Right. Once those omitted local costs are admitted, the blanket "better off" answer is no longer earned.` | [immigration-economist-effects-matrix.md](/Users/alien/Projects/research/research/immigration-economist-effects-matrix.md:1) |
    36	| “`we've only a partial grasp`” | Caroline Hoxby comment on Clark survey [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/] | Admits the GE confidence is weaker than the public consensus rhetoric suggests | `Then the public-facing certainty is doing more work than the underlying knowledge.` | [immigration-economist-effects-matrix.md](/Users/alien/Projects/research/research/immigration-economist-effects-matrix.md:1) |
    37	| “`The data is not decisive, though`” | Christopher Udry comment on Clark survey [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/] | Survey rhetoric sounds more decisive than some economists' own comments | `Then "economists agree" is already overstated.` | [immigration-economist-effects-matrix.md](/Users/alien/Projects/research/research/immigration-economist-effects-matrix.md:1) |
    38	| “`economically, the U.S. needs large-scale immigration in order to support its economy`” | Noah Smith, *A bunch of thoughts and evidence on immigration* [SOURCE: https://www.noahpinion.blog/p/a-bunch-of-thoughts-and-evidence] | National macro need is presented as if it settles destination incidence | `Maybe on the aggregate-growth ledger. It still does not settle per-person or local-incumbent welfare.` | [immigration-noah-smith-nicholas-decker-claims-audit-2026-04-11.md](/Users/alien/Projects/research/research/immigration-noah-smith-nicholas-decker-claims-audit-2026-04-11.md:1) |
    39	| “`Why immigration doesn't reduce wages`” | Noah Smith title [SOURCE: https://www.noahpinion.blog/p/why-immigration-doesnt-reduce-wages] | Turns a narrow labor-market question into a broad exoneration | `Even if average wage effects are small, housing, shelter, schools, and local budgets remain separate stress ledgers.` | [immigration-county-outcome-panel-2026-04-21.md](/Users/alien/Projects/research/research/immigration-county-outcome-panel-2026-04-21.md:1) |
    40	| “`immigration is mostly unrelated to the inflation issue`” | Noah Smith, *Did immigration bring down inflation?* [SOURCE: https://www.noahpinion.blog/p/did-immigration-bring-down-inflation] | Uses headline inflation to erase housing incidence | `The better read is: not the main driver of overall disinflation, but still a real housing-pressure channel.` | [immigration-noah-smith-nicholas-decker-claims-audit-2026-04-11.md](/Users/alien/Projects/research/research/immigration-noah-smith-nicholas-decker-claims-audit-2026-04-11.md:1) |
    41	| “`Immigrants Must Make Us Richer`” | Nicholas Decker title [SOURCE: https://nicholasdecker.substack.com/p/yes-immigrants-must-make-us-richer] | Converts some increasing-returns channels into a universal conclusion | `No. Official and repo evidence support an incidence split, not a must-be-positive theorem.` | [immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md](/Users/alien/Projects/research/research/immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md:1) |
    42	| “`restrictions are not necessary to protect American workers`” | Bryan Caplan, Cato Journal [SOURCE: https://www.cato.org/sites/cato.org/files/serials/files/cato-journal/2012/1/cj32n1-2.pdf] | Collapses `job collapse is false` into `worker objection is trivial` | `The broad collapse story is false, but constrained-place wage pressure remains a live descriptive screen, not a settled causal zero.` | [immigration-bryan-caplan-claims-audit-2026-04-21.md](/Users/alien/Projects/research/research/immigration-bryan-caplan-claims-audit-2026-04-21.md:1) |
    43	| “`the fiscal effects are small`” | Bryan Caplan, Cato Journal [SOURCE: https://www.cato.org/sites/cato.org/files/serials/files/cato-journal/2012/1/cj32n1-2.pdf] | Treats federal and state/local incidence as one small ledger | `That fails once you separate narrow federal gains, state/local costs, gross receiver loads, and still-withheld origin school-net rows.` | [immigration-bryan-caplan-claims-audit-2026-04-21.md](/Users/alien/Projects/research/research/immigration-bryan-caplan-claims-audit-2026-04-21.md:1) |
    44	| “`double world GDP`” | Open Borders slogan [SOURCE: https://openborders.info/double-world-gdp/] | Launders stylized upper bounds into realistic forecast language | `Large gains in principle survive. The realistic near-doubling baseline does not.` | [immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md](/Users/alien/Projects/research/research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md:1) |
    45	
    46	## Failure-mode map
    47	
    48	Use this when you want to label the trick quickly.
    49	
    50	| Claim pattern | Failure mode | Best follow-up |
    51	|---|---|---|
    52	| `Immigration helps Americans` | `ledger switching` | `Which Americans, on which ledger?` |
    53	| `Overall GDP rises` | `aggregate-output trump card` | `Why does that settle GDP per person or local incumbent welfare?` |
    54	| `Open borders could double world GDP` | `upper-bound laundering` | `Why are you presenting a stylized upper bound as a realistic policy baseline?` |
    55	| `Moderate inflows were absorbed fine` | `marginal-to-mass extrapolation` | `Why should that survive concentrated surge conditions and weak housing response?` |
    56	| `Ratios look stable` | `denominator masking` | `Did capacity expand endogenously while the absolute burden still rose?` |
    57	| `Immigrant voting is low` | `political-economy erasure` | `What about citizen political response, assignment rules, and legitimacy effects?` |
    58	| `Housing will adjust` | `capacity erasure` | `Show the actual build-rate and service-capacity path, not a scalar assumption.` |
    59	
    60	## Best counters by topic
    61	
    62	### If the economist is talking about growth
    63	
    64	Say:
    65	
    66	`Aggregate growth is not the disputed point. The disputed point is destination incidence after housing, local capacity, and politics are priced in.`
    67	
    68	### If the economist is talking about wages
    69	
    70	Say:
    71	
    72	`Broad job-collapse rhetoric is too strong. That still does not erase constrained-place wage screens or the rest of the local ledger.`
    73	
    74	### If the economist is talking about housing
    75	
    76	Say:
    77	
    78	`Don’t hide behind ratios. Show me absolute load, build response, renter incidence, and overflow behavior.`
    79	
    80	### If the economist is talking about open borders
    81	
    82	Say:
    83	
    84	`Your gains only survive if destination capacity degrades less than the place-premium gains you are counting. Show the break-even assumption explicitly.`
    85	
    86	## Best closing line
    87	
    88	**The economist case is strongest where it talks about migrant gains and aggregate efficiency. It becomes evasive where it acts as if those gains settle destination-country welfare, local capacity, and political-response channels.**
    89	
    90	## Revisions
    91	
    92	| Date | Change | Trigger |
    93	|---|---|---|
    94	| 2026-06-16 | Scoped wage/capacity, fiscal, and political counters to descriptive/gross/correlational evidence. | `research/immigration-conclusion-audit-running-fixes.md` capacity/surge corrections. |
--- END FILE: research/immigration-economist-debate-sheet-2026-04-22.md ---

--- BEGIN FILE: research/immigration-economist-rhetorical-failures-2026-04-22.md ---
     1	# Immigration economist rhetorical failures — 2026-04-22
     2	
     3	**Question:** What is the strongest fair case that the mainstream pro-immigration economics rhetoric is misleading, evasive, or dishonest after the repo's current evidence?  
     4	**Tier:** Deep | **Date:** 2026-04-22  
     5	**Instrument caveat:** Immigration is politically charged and the LLM instrument has known asymmetry risk here. This memo leans on repo-built artifacts, official sources, and named claim audits rather than generic training-data impressions. [SOURCE: notes/llm-bias-caveat.md]
     6	
     7	**Status update (2026-06-16):** Later conclusion audits narrowed the capacity/surge evidence. Treat load/capacity and receiver-city panels as descriptive screens, receiver-cost rows as gross-load evidence, and election rows as correlational political-response signals. They do not identify a fiscal-load-to-vote mechanism, a native-exit mechanism, or a globally ranked worker-incidence channel. [SOURCE: research/immigration-conclusion-audit-running-fixes.md]
     8	
     9	## Bottom line
    10	
    11	The strongest attack is **not**:
    12	
    13	1. `economists are all liars`
    14	
    15	The strongest attack is:
    16	
    17	1. a large share of the pro-immigration economics rhetoric relies on `ledger switching`
    18	2. it repeatedly `launders upper-bound model outputs into realistic baselines`
    19	3. it `extrapolates marginal mover gains to mass inflow regimes`
    20	4. it often `erases destination capacity as a separate stress system`
    21	5. it underprices `political-response channels and local incidence`
    22	
    23	That is enough to kill the strongest economist slogans without making claims the repo cannot prove. [INFERENCE]
    24	
    25	## Executive verdict
    26	
    27	The current repo position is:
    28	
    29	1. `global gains` are real enough that pure restrictionist collapse rhetoric fails [SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md]
    30	2. `destination-local stress and gross-load evidence` is serious enough that blanket economist optimism fails [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md] [SOURCE: research/immigration-receiver-failure-atlas-2026-04-22.md]
    31	3. the clean synthesis is not `immigration good` or `immigration bad`
    32	4. the current descriptive synthesis is `flow x capacity x composition x regime` [SOURCE: research/immigration-frontier-rethink-2026-04-22.md]
    33	
    34	So the economist case is weakest exactly where it acts as if one efficiency argument settles all ledgers at once. [INFERENCE]
    35	
    36	## Claims table
    37	
    38	| # | Claim about the rhetoric | Verdict | Why |
    39	|---|---|---|---|
    40	| 1 | `Economists agree immigration is good for Americans` | `Misleading` | The Clark-style consensus rhetoric compresses multiple ledgers into one answer and outruns the evidence. [SOURCE: research/immigration-economist-effects-matrix.md] |
    41	| 2 | `Large migrant gains imply large gains for destination-country incumbents` | `Rejected` | Migrant/global gains survive, but destination per-capita and local-incidence claims do not follow automatically. [SOURCE: research/immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md] |
    42	| 3 | `Open-borders papers justify near-doubling as a realistic forecast` | `Rejected` | The strong papers are stylized upper-bound models, not policy-realist central forecasts. [SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md] |
    43	| 4 | `Capacity is a second-order friction that does not change the sign` | `Too broad` | Housing, shelter, and local service capacity are first-order stress systems in the repo's current descriptive evidence, even where causal identification is incomplete. [SOURCE: research/immigration-capacity-frontier-2026-04-21.md] [SOURCE: research/immigration-receiver-failure-atlas-2026-04-22.md] |
    44	| 5 | `Political effects are mostly about immigrant voting` | `Too narrow` | Citizen political response, legitimacy, assignment regimes, and local overload remain live channels; the current receiver-election evidence is correlational, not a clean backlash mechanism estimate. [SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md] [SOURCE: research/full-spectrum-costs-unauthorized-immigration-research-memo.md] |
    45	| 6 | `If overall GDP rises, restrictionist objections are mostly answered` | `Rejected` | Aggregate GDP, GDP per capita, and local incumbent welfare are distinct ledgers. [SOURCE: research/immigration-claims-matrix-2026-04-11.md] |
    46	
    47	## The strongest fair steel-man
    48	
    49	Before attacking the economist case, keep the strongest version in view:
    50	
    51	1. place-premium and migrant-income gains are real [SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md]
    52	2. broad `job collapse` rhetoric is too crude [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md]
    53	3. first-generation / unauthorized crime claims are usually overstated by restrictionists [SOURCE: research/immigration-crime-rates-unauthorized-vs-native-born.md]
    54	4. some national aggregate channels are genuinely favorable in recent official scoring [SOURCE: https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf]
    55	
    56	So the repo does **not** support the claim that the economist case is fake from top to bottom.
    57	
    58	The stronger and more disciplined claim is that the economist case is repeatedly **overextended beyond its own evidentiary warrant**. [INFERENCE]
    59	
    60	## Failure mode 1: ledger switching
    61	
    62	This is the biggest one.
    63	
    64	The rhetoric often slides between:
    65	
    66	1. `migrant welfare`
    67	2. `world output`
    68	3. `national aggregate GDP`
    69	4. `destination GDP per capita`
    70	5. `incumbent local welfare`
    71	
    72	Those are not the same object. The repo's own current claim ladder already depends on separating them. [SOURCE: research/immigration-claims-matrix-2026-04-11.md] [SOURCE: research/immigration-reasoning-evolution-2026-04-21.md]
    73	
    74	This is why slogans such as:
    75	
    76	1. `immigration makes the country richer`
    77	2. `immigration benefits Americans`
    78	3. `immigration is good for the average citizen`
    79	
    80	are often not false in a clean literal sense, but still misleading as public argument. They glide from one ledger to another without saying so. [INFERENCE]
    81	
    82	**Best accusation:** `equivocation`
    83	
    84	## Failure mode 2: upper-bound laundering
    85	
    86	This is the core open-borders move.
    87	
    88	The economist rhetoric often cites:
    89	
    90	1. place-premium papers
    91	2. Kennan-style long-run model papers
    92	3. Clemens's literature summary
    93	
    94	and then speaks as if:
    95	
    96	1. mass liberalization would realistically yield near-doubling output gains
    97	2. destination institutions would mostly remain intact
    98	3. transition constraints are implementation details
    99	
   100	The repo's full-paper audit already killed that stronger reading. The fair statement is:
   101	
   102	1. very large gains remain plausible in principle
   103	2. the classic near-doubling rhetoric is an `upper-bound extrapolation`, not a realistic baseline [SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md]
   104	
   105	**Best accusation:** `laundering stylized upper bounds into policy baselines`
   106	
   107	## Failure mode 3: marginal-to-mass extrapolation
   108	
   109	Economists often have evidence that:
   110	
   111	1. marginal migrants gain a lot
   112	2. labor markets absorb moderate inflows without obvious collapse
   113	3. long-run capital adjustment helps
   114	
   115	What they often do **not** have is evidence that these results survive:
   116	
   117	1. concentrated surge conditions
   118	2. weak local housing response
   119	3. shelter and school bottlenecks
   120	4. multi-year political feedback
   121	
   122	The repo's current frontier moved away from county stock-share arguments for exactly this reason. The live descriptive object is now `flow x capacity x composition x regime`, not a generic stock effect. Causal identification still needs stronger counterfactual design. [SOURCE: research/immigration-frontier-rethink-2026-04-22.md] [SOURCE: research/immigration-capacity-frontier-2026-04-21.md]
   123	
   124	**Best accusation:** `external-validity abuse`
   125	
   126	## Failure mode 4: capacity erasure
   127	
   128	The strongest economist rhetoric often treats capacity as:
   129	
   130	1. a nuisance parameter
   131	2. a short-run friction
   132	3. a housing-zoning side issue
   133	
   134	The repo no longer supports that.
   135	
   136	The strongest local descriptive evidence now points to:
   137	
   138	1. `permit throughput` and `flow/build capacity` as a useful wage-side stress screen, with thin ranking margins [SOURCE: research/immigration-capacity-frontier-2026-04-21.md]
   139	2. concrete receiver-node overload in shelter and related systems, especially `Denver` [SOURCE: research/immigration-receiver-failure-atlas-2026-04-22.md]
   140	3. `Chicago` surviving as an absolute-load case even when the saturation ratios are muted [SOURCE: research/immigration-receiver-counterfactuals-2026-04-22.md]
   141	4. `Boston` looking like a regime-cost / assignment-burden case rather than a simple physical saturation case [SOURCE: same]
   142	
   143	That means capacity is not one scalar friction. It is a system of separate bottlenecks.
   144	
   145	**Best accusation:** `category error about what the destination system is`
   146	
   147	## Failure mode 5: denominator masking
   148	
   149	This is the cleanest technical attack on some optimistic rhetoric.
   150	
   151	If a city expands shelter beds or emergency capacity in response to a surge, then:
   152	
   153	1. `PIT/HIC` ratios can stay flat or even improve
   154	2. while absolute sheltered load and gross emergency burden still rise
   155	
   156	That is exactly why the receiver counterfactual pass needed log-count outcomes instead of only ratios. `Chicago` is the clearest example. [SOURCE: research/immigration-receiver-counterfactuals-2026-04-22.md]
   157	
   158	Economist rhetoric that relies on `capacity adjusted, therefore no problem` reasoning is often vulnerable to this exact mistake. [INFERENCE]
   159	
   160	**Best accusation:** `endogenous-denominator masking`
   161	
   162	## Failure mode 6: political-economy erasure
   163	
   164	The optimistic economist argument often treats politics as:
   165	
   166	1. immigrant voting
   167	2. perhaps welfare-state demand
   168	3. maybe culture/trust as a soft residual
   169	
   170	That is too narrow.
   171	
   172	The repo's current work points to:
   173	
   174	1. citizen political-response associations in high-immigration constrained places [SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md]
   175	2. local burden channels in shelter, schools, and services [SOURCE: research/full-spectrum-costs-unauthorized-immigration-research-memo.md]
   176	3. assignment rules, right-to-shelter, and emergency procurement as separate causal levers [SOURCE: research/immigration-frontier-rethink-2026-04-22.md]
   177	
   178	So if the rhetoric acts as if `lower immigrant turnout` answers the political objection, that is not analysis. It is a drastic underspecification of the system. [INFERENCE]
   179	
   180	**Best accusation:** `partial-channel answer presented as complete`
   181	
   182	## Failure mode 7: aggregate-output trump card
   183	
   184	This is where a lot of public-facing economist argument becomes indefensible.
   185	
   186	The move is:
   187	
   188	1. show overall GDP rises
   189	2. infer the country is better off
   190	3. treat local losers as politically noisy rather than analytically central
   191	
   192	The repo's comparative and official-source work already blocks that:
   193	
   194	1. aggregate GDP can rise while GDP per capita falls [SOURCE: research/immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md]
   195	2. CBO or narrow federal-proxy channels can be positive while state/local and receiver gross-load ledgers are negative or unresolved on all-in net [SOURCE: research/immigration-claims-matrix-2026-04-11.md]
   196	3. local receiver systems can overload while national macro aggregates still look fine [SOURCE: research/immigration-causal-surge-2021-2024.md]
   197	
   198	So the aggregate-output trump card is not serious if the question is about incumbent resident welfare. [INFERENCE]
   199	
   200	**Best accusation:** `answering a different question than the one being argued`
   201	
   202	## What we can fairly call dishonest
   203	
   204	The repo can cleanly support the following accusations when the rhetoric does them repeatedly:
   205	
   206	1. `equivocation across ledgers`
   207	2. `presenting upper-bound model outputs as realistic forecasts`
   208	3. `using marginal mover evidence to answer mass-flow policy questions`
   209	4. `ignoring capacity and political-response channels after being shown they are first-order stress systems`
   210	5. `using aggregate GDP as if it settles local incidence`
   211	
   212	What the repo cannot yet cleanly support:
   213	
   214	1. `all mainstream immigration economists know their conclusions are false`
   215	2. `the gains literature is entirely fake`
   216	3. `immigration is net bad on every coherent ledger`
   217	
   218	That broader language would weaken the case rather than strengthen it. [INFERENCE]
   219	
   220	## Best short-form attack lines
   221	
   222	These are the sharpest fair questions to ask an economist making a strong optimistic claim:
   223	
   224	1. `Which ledger are you talking about: migrants, world output, aggregate GDP, GDP per capita, or incumbent residents?`
   225	2. `Why should marginal mover estimates survive under mass inflow and stressed destination capacity?`
   226	3. `What exact destination-country degradation would be required to wipe out your claimed gains?`
   227	4. `Why are you treating stylized long-run upper bounds as realistic policy baselines?`
   228	5. `Why does your model ignore housing, shelter, schools, courts, and political-response channels as separate capacity systems?`
   229	6. `If your destination denominator expands endogenously, why should your ratio metric be taken as evidence of no overload?`
   230	
   231	## Best current formulation
   232	
   233	The best current repo line is:
   234	
   235	1. the economist case survives on `migrant gains`, `global gains`, and the rejection of crude collapse rhetoric
   236	2. it fails as a blanket destination-country welfare story
   237	3. it fails hardest where it compresses all ledgers into one efficiency claim
   238	4. the current public-data object is `flow x capacity x composition x regime`, not a scalar immigration sign, and remains partly descriptive rather than fully causal
   239	
   240	That is the strongest fair version of `the economist rhetoric is dishonest` that the repo can defend right now.
   241	
   242	## Revisions
   243	
   244	| Date | Change | Trigger |
   245	|---|---|---|
   246	| 2026-06-16 | Scoped capacity, wage, receiver-load, and political-response language to descriptive/gross/correlational evidence. | `research/immigration-conclusion-audit-running-fixes.md` capacity/surge corrections. |
--- END FILE: research/immigration-economist-rhetorical-failures-2026-04-22.md ---

--- BEGIN FILE: research/immigration-INDEX.md ---
     1	# Immigration — Topic Index
     2	
     3	Files the agent should consult before acting. Start with Core State, then branch by question.
     4	
     5	Instrument note: this topic is politically charged and much of the synthesis is LLM-assisted. Treat this index as a routing layer, not as a neutral substitute for the cited artifacts. Consult `notes/llm-bias-caveat.md` before writing headline claims.
     6	
     7	## Core State
     8	
     9	| File | Topic | Consult before |
    10	|------|-------|----------------|
    11	| `immigration-main-question-reset.md` | What the repo is actually trying to answer | Reframing the project or proposing new scope |
    12	| `immigration-evidence-base-audit.md` | Which claims are well-supported vs thin | Repeating literature claims or writing summaries |
    13	| `immigration-verified-findings-report-2026-04-10.md` | Current verified findings snapshot | Answering "what do we know?" |
    14	| `immigration-confidence-ladder.md` | Claim confidence by tier | Making strong claims or publishing conclusions |
    15	| `immigration-claims-evolution-ledger-2026-04-23.md` | Claim-by-claim evolution ledger with takeaways and recurring misunderstandings | Asking how the immigration claims changed or how they relate |
    16	| `immigration-glossary.md` | Definitions and term discipline | Using terms like `unauthorized`, `low-skill`, `surge`, `fiscal` |
    17	| `immigration-epistemic-check.md` | Framing-sensitive guardrails | Politically charged synthesis |
    18	| `immigration-economist-effects-matrix.md` | What economists are actually pricing vs omitting | Comparing Smith, Decker, Borjas, Clark poll economists |
    19	| `immigration-dataset-register.md` | Use-case-oriented data register | Asking "what data do we have?" |
    20	| `immigration-verification-handoff.md` | Verification map: repo files, datasets, paper families, disciplines | Handing the topic to another agent |
    21	| `immigration-conclusion-audit-running-fixes.md` | Live overclaim/denominator/layer fix ledger | Auditing conclusions, applying XDISC-DS-02, checking what changed on 2026-06-16 |
    22	
    23	## Fiscal Ledger
    24	
    25	| File | Topic | Consult before |
    26	|------|-------|----------------|
    27	| `fiscal-impact-unauthorized-immigration-research-memo.md` | Main fiscal memo: federal/state-local split, wage debate, child-attribution dispute | Any fiscal bottom line |
    28	| `full-spectrum-costs-unauthorized-immigration-research-memo.md` | Non-ledger costs: congestion, courts, labor-law erosion, backlash | Claiming "hidden" costs beyond taxes/transfers |
    29	| `immigration-unified-scenarios-memo.md` | Scenario comparison across methods | Converting arguments into a bounded range |
    30	| `immigration-costs-causal-analysis.md` | DAG and causal-path discipline | Proposing controls, mediators, or attribution rules |
    31	| `state-local-cost-examples-ny-ca-tx.md` | Concrete state/local examples | Generalizing from national ledgers to local burden |
    32	| `immigration-household-weighted-correction.md` | Household vs person correction issues | Reusing external figures without checking unit of analysis |
    33	| `immigration-nas-scope-and-bias-update-2026-04-10.md` | What NAS does and does not cover | Treating NAS as final or complete |
    34	| `immigration-adversarial-review.md` | Strongest case against our own position | Closing out a conclusion or writing a public-facing memo |
    35	
    36	## Data Stack
    37	
    38	| File | Topic | Consult before |
    39	|------|-------|----------------|
    40	| `immigration-lifetime-fiscal-data-stack-2026-04-10.md` | Minimum viable and gold-standard lifetime model stack | Saying ACS alone is enough |
    41	| `immigration-country-fiscal-tensor-2026-06-15.md` | **Built** country fiscal tensor + rollup anchors (union DuckDB) | Querying population × layer × order |
    42	| `immigration-federal-distribution-findings-2026-06-15.md` | Distribution pass — school units, federal proxy white vs Mexico | “Do whites pay multiples?” |
    43	| `immigration-europe-caucasian-fiscal-findings-2026-06-15.md` | **EU27 / UK / Caucasian natives / low-skill corridors** — federal proxy + matched-education | “European immigrants vs white Americans”; corridor A vs B |
    44	| `immigration-school-burden-per-adult-2026-06-15.md` | **per_pupil × kids/adult** — three-layer annual (`v_three_layer_annual`) | “Did you multiply child burden?” |
    45	| `immigration-sweep-cycles-13-22-2026-06-15.md` | Diverge/synthesis cycles 13–22 (school burden build) — **rushed SQL pass, superseded by 23–32** | Post-sweep thesis burst |
    46	| `immigration-sweep-cycles-23-32-2026-06-15.md` | **Full protocol** sweeps 23–32: NAS college+ NPV, school weights, lifetime flip, converge; origin school/net rows partly superseded by same-universe guard | Post-rebuild thesis; three-layer + lifetime; do not cite old `$771/+748` origin school/net rows |
    47	| `immigration-mexico-npv-population-synthesis-2026-06-15.md` | **Mexico NPV multiply-out**, ACS denominator, Biden stock vs encounters, **full ledger stack (Q+R)** | "Reported Mexicans"; "10M illegals"; NAS ≠ net fiscal |
    48	| `immigration-restrictionist-arguments-steelman-2026-06-15.md` | **Steel-man** restrictionist chains: Borjas, BGH, NAS/Orrenius, Gould, Razin, FAIR | Arguing against immigration; follow their logic |
    49	| `immigration-restrictionist-corpus-parse-2026-06-15.md` | **Full marker-modal parse** of 8 restrictionist PDFs → perspectives, narratives, generators S06–S14 | Deep read of restrictionist corpus; generator mining |
    50	| `immigration-restrictionist-corpus-full-extract-2026-06-15.md` | **Section-by-section full read** of all 9 papers (~220 claims, 62 sections) | Authoritative claim register after full parse |
    51	| `immigration-restrictionist-dataset-integration-2026-06-15.md` | **Paper → dataset → DuckDB** map; Tier A–C acquire list | Planning integration after restrictionist corpus read |
    52	| `immigration-lifetime-country-approx-brainstorm-2026-06-15.md` | Brainstorm: country lifetime +/- with 1st/2nd/3rd order stacks | Designing country rollup without scalar lies |
    53	| `immigration-lifetime-dataset-brainstorm-2026-06-15.md` | Brainstorm + tier map for lifetime proxies; `setup-lifetime.sh` acquisition | Picking datasets for lifetime NPV calibration |
    54	| `immigration-lifetime-fiscal-generators.md` | 563 DuckDB parameter claims; 106 MD / 104 DuckDB generators (MD-only Q06, S15) | Negative-space sweeps, unnamed-assumption audits |
    55	| `immigration-thesis-generator-audit-2026-06-16.md` | Cross-disciplinary generator/self-prompt audit (economics, micro/macro, urbanism, psychology, narrative) | Running divergence/convergence loops; asking what to search next |
    56	| `immigration-knowledge-delta-agent-loop-2026-06-16.md` | Two-day delta + parent-controlled agent loop (claim inventory → probe → converge → review) | Starting a full immigration research epoch; pairing with generator audit |
    57	| `immigration-lifetime-unified-theory-2026-06-15.md` | **Living synthesis** — unified theory + 5 formal models + critique matrix (update each sweep) | After every corpus round; before next download burst |
    58	| `../notes/immigration-lifetime-sweep-protocol.md` | Mandatory post-sweep workflow (theory → 5 models → thesis burst → disconfirm → round N+1) | Structuring research cycles |
    59	| `../notes/immigration-lifetime-synthesis-diverge-cookbook.md` | **Prompt template / cookbook** — full diverge↔converge loop, subagent JSON schema, synthesis prompt | Running sweeps; adapting to new topics |
    60	| `immigration-public-data-acquisition-2026-04-11.md` | What public files were actually staged locally | Assuming a dataset has been acquired |
    61	| `immigration-origin-data-stack.md` | Origin/destination and ontology layer | Making claims by origin mix |
    62	| `immigration-next-data-upgrades.md` | Highest-value missing acquisitions | Planning the next data tranche |
    63	| `immigration-net-negative-dataset-frontier-2026-06-15.md` | Datasets to test net-negative fiscal/local-cost claims (+ disconfirmation) | Building cost ledger or federal microsim |
    64	| `immigration-scenario-composition-2026-06-15.md` | Integrated SIPP+MEPS+federal+local scenario ledgers | Cell-level fiscal reasoning; not scalar verdict |
    65	| `immigration-frontier-data-acquisition-2026-04-11.md` | Stage 4 local-capacity acquisition pass: `SAIPE`, court/interpreter docs, and NCES CCD file-tool artifacts | Building school-service or court-friction modules |
    66	| `immigration-school-service-complexity-2026-04-11.md` | Built district/state school-side context layer from `SAIPE` + school finance + current NCES directory, plus bounded `ELSi` probe | Doing district school-burden or school-service-complexity analysis |
    67	| `immigration-surge-threshold-dataset-frontier-2026-04-21.md` | Dataset frontier and research designs that can actually identify surge and threshold effects | Asking what data and empirical design would settle nonlinear local-capacity questions |
    68	| `immigration-prototype-progress.md` | Current prototype state | Claiming the model is further along than it is |
    69	| `immigration-public-mvp-readiness-2026-04-11.md` | What is ready for a public-use MVP | Shipping a simplified public model |
    70	| `immigration-public-mvp-meps-module-2026-04-11.md` | Built MEPS health-cost module for the public MVP | Using MEPS-derived health-cost outputs |
    71	| `immigration-public-mvp-sipp-meps-bridge-2026-04-11.md` | Completed SIPP-to-MEPS bridge and expected-health output | Integrating transition and payer-incidence profiles |
    72	| `immigration-education-bucket-stock-and-lifetime-status-2026-04-11.md` | Weighted ACS stock cut by education bucket plus current lifetime-estimate status | Asking for `<HS` / `HS` / `some college` counts or state shares |
    73	| `immigration-local-burden-puma-layer.md` | PUMA/local burden layer | Moving from state averages to sub-state analysis |
    74	| `immigration-stage2-county-bridge-batch.md` | County bridge build status | County-level joining or school/housing overlays |
    75	
    76	## Interpretation & External Debate
    77	
    78	| File | Topic | Consult before |
    79	|------|-------|----------------|
    80	| `immigration-clark-respondent-audit.md` | How to read the Clark poll without overclaiming | Saying "economists agree" |
    81	| `immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md` | Unified comparative audit with one quantitative framework across all three commentators | Wanting a more decisive first-principles comparison |
    82	| `immigration-claims-matrix-2026-04-11.md` | One-page verified/inferred/unresolved claim ledger for artifacts and commentators; 2026-06-16 scoped to quick ledger, not latest tensor | Making a quick final assertion; confirm latest fiscal/school rows in verified findings and running fixes |
    83	| `immigration-david-d-friedman-claims-audit-2026-04-11.md` | Named audit of David D. Friedman claims with a first-principles quantitative pass | Checking libertarian open-borders arguments against the repo and official sources |
    84	| `immigration-bryan-caplan-claims-audit-2026-04-21.md` | Claim-by-claim audit of Bryan Caplan with a causal graph tying his optimistic channels to current surge, housing, fiscal, and political-response evidence | Evaluating Caplan directly rather than treating him as generic open-borders rhetoric |
    85	| `immigration-economist-one-pager-2026-04-22.md` | Short public-facing one-pager on why the strongest pro-immigration economics rhetoric keeps answering the wrong question | Needing a concise forwardable version rather than a full memo |
    86	| `immigration-economist-debate-sheet-2026-04-22.md` | Quote-driven debate sheet mapping economist claims to the hidden move, failure mode, and strongest repo-backed counter | Wanting direct quotes and fast counters for debate or adversarial writing |
    87	| `immigration-economist-rhetorical-failures-2026-04-22.md` | Bounded memo on the strongest fair critique of mainstream pro-immigration economics rhetoric: ledger switching, upper-bound laundering, marginal-to-mass extrapolation, capacity erasure, denominator masking, and political-economy underspecification | Asking how to kill the strongest economist arguments without overclaiming beyond the repo's current evidence |
    88	| `immigration-noah-smith-nicholas-decker-claims-audit-2026-04-11.md` | Named audit of Noah Smith and Nicholas Decker claims | Checking pundit or commentator claims against the repo and official sources |
    89	| `immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md` | Audit of the Open Borders “double world GDP” slogan, cited papers, repo capacity constraints, and apartheid framing | Evaluating classic open-borders macro claims or apartheid analogies |
    90	| `immigration-threshold-first-panel-2026-04-21.md` | First joined-data threshold pass using BPS permits, HUD PIT/HIC, election shift, and receiver-city costs | Asking whether threshold effects are measurable in current public data |
    91	| `immigration-threshold-causal-levers-2026-04-21.md` | Deeper normalized pass identifying which levers actually move political response and receiver stress | Asking what the real causal levers are after joining threshold datasets |
    92	| `immigration-low-skill-origin-incidence-memo.md` | Why origin mix and household structure matter | Treating low-skill immigration as one undifferentiated object |
    93	| `immigration-fiscal-deceptive-data-reading-pack.md` | Common bad-faith or sloppy readings of the data | Debunking a chart, thread, or pundit claim |
    94	| `immigration-fiscal-camarota-cis-testimony-audit.md` | Restrictionist benchmark audit | Using CIS/Camarota as baseline evidence |
    95	| `immigration-crime-rates-unauthorized-vs-native-born.md` | Crime-rate evidence review | Mixing crime claims into a fiscal memo |
    96	| `immigration-agi-reframing.md` | Off-mainline strategic reframing | Pulling the project into speculative macro territory |
    97	
    98	## Causal-design layer (2026-04-18)
    99	
   100	| File | Topic | Consult before |
   101	|------|-------|----------------|
   102	| `immigration-causal-synthesis-2026-04-18.md` | Cycle synthesis: Saiz × E-Verify findings, Card-vs-Borjas verdict | Saying "Borjas vs Card is unresolved" or "rent exposure is just price discovery" |
   103	| `immigration-causal-everify-card-vs-borjas.md` | E-Verify staggered TWFE on QWI 2003-2023, native low-skill wages | Citing Borjas wage prediction for the U.S. policy variation |
   104	| `immigration-causal-saiz-elasticity-rent.md` | Saiz 2010 housing supply elasticity × ACS rent + foreign-born | Treating PUMA rent burden as elasticity-neutral |
   105	| `immigration-causal-paradigm-escape-synthesis-2026-04-18.md` | Evening cycle synthesis: 5 verdict updates, 8-finding ladder | Writing the headline immigration position; asking "what changed?" |
   106	| `immigration-causal-internal-vs-immigrant-newcomers.md` | IRS SOI × ACS moved-from-abroad flow comparison for “newcomer burden” | Treating "newcomer burden" as immigration-driven by default |
   107	| `immigration-causal-surge-2021-2024.md` | OHSS encounters + CHNV + city costs + 2024 election: surge analysis | Extrapolating pre-2020 findings to surge magnitudes; discussing 2024 election in immigration terms |
   108	| `immigration-county-outcome-panel-2026-04-21.md` | QCEW + IRS domestic migration + threshold spine: county wages, employment, domestic migration, and political response in one frame | Reusing the county outcome panel while remembering the IRS layer is not native-incumbent-only |
   109	| `immigration-capacity-frontier-2026-04-21.md` | Stock vs flow vs flow-to-capacity comparison, threshold robustness grid, and a clearer statement of what still remains open on subgroups, voting, welfare, and receiver counterfactuals | Asking what is actually left to check after the first county threshold passes |
   110	| `immigration-capacity-falsification-2026-04-21.md` | Corrected falsification pass with clean `2017–2018` and `2018–2019` annual pre-COVID windows, `1,000`-draw permutation inference, division/state leave-out, explicit window metadata, and wage-threshold null benchmarking | Asking which parts of the new flow-capacity story still survive after fixing the earlier placebo bug |
   111	| `immigration-reasoning-evolution-2026-04-21.md` | Narrative provenance trace of how the repo’s immigration reasoning changed, including the `/critique close` correction and later downgrade that left the annual wage/employment split unresolved | Wanting the evolution of reasoning itself traced rather than only the latest stance |
   112	| `immigration-frontier-rethink-2026-04-22.md` | Zoomed-out rethink after the corrected falsification pass; demotes the annual county panel to a screening surface and ranks the better next frontiers | Asking where the research should go once county threshold work hits diminishing returns |
   113	| `immigration-receiver-failure-atlas-2026-04-22.md` | Receiver-node overload atlas joining shelter load, permits, spending, and political shift from `2018–2024` | Asking what the actual local failure nodes look like once counties stop being the main causal object |
   114	| `immigration-resident-weighted-exposure-2026-04-22.md` | Resident-, renter-, and child-weighted correction to the newcomer and stress-exposure framing | Asking what the typical resident or renter is exposed to rather than what the median county looks like |
   115	| `immigration-open-borders-break-even-bounds-2026-04-22.md` | Converts the repo’s conservative open-borders calibration into explicit break-even loss bounds and housing-absorption requirements | Asking how much destination-country degradation would be needed to wipe out global gains |
   116	| `immigration-receiver-counterfactuals-2026-04-22.md` | National-CoC synthetic-control style counterfactuals for `NYC`, `Denver`, `Boston`, `Chicago`, and `Bexar`, including ratio outcomes, absolute-load checks, and donor-pool exclusions | Asking whether the receiver-node stories survive a real donor-pool counterfactual rather than a local comparison |
   117	| `immigration-receiver-data-acquisition-2026-04-23.md` | Staged 2024 ACS PUMS, EOIR Case Data 2026-0301, and QWI county-quarter receiver panel with hashes, limits, and next kill-test sequence | Asking what new datasets were acquired for the receiver-node/capacity theory |
   118	| `immigration-receiver-node-kill-test-2026-04-23.md` | End-to-end nine-node kill test joining ACS 2024 exposure, PUMA bridge, EOIR broad/strict court pressure, QWI labor outcomes, shelter/capacity, and political shift | Asking whether the receiver-node theory survives the new data |
   119	
   120	## Raw Data & Warehouse
   121	
   122	| File | Topic | Consult before |
   123	|------|-------|----------------|
   124	| `../sources/immigration-fiscal/data/MANIFEST.md` | Raw-file manifest with paths and acquisition notes | Looking for a specific local file |
   125	| `../warehouse/immigration_context.duckdb` | Main derived DuckDB warehouse (internal disk) | Querying state/origin/context data |
   126	| `../sources/immigration-fiscal/data/derived/build_immigration_warehouse.py` | Warehouse rebuild script | Rebuilding or extending the DuckDB |
   127	| `../sources/immigration-fiscal/data/derived/stage3_proto/` | Prototype local-context build outputs | Using tract/PUMA prototype artifacts |
   128	| `../sources/immigration-causal/data/external/census_acs_2024_1yr/` | ACS 2024 PUMS person/household/dictionary staging with acquisition manifest | Building post-surge PUMA receiver exposure |
   129	| `../sources/immigration-causal/data/derived/acs_2024_receiver_exposure/acs_2024_receiver_exposure_puma.parquet` | First ACS 2024 receiver-state PUMA exposure layer | Screening high-exposure PUMAs before county/metro joins |
   130	| `../sources/immigration-causal/data/outcomes/analysis/receiver_node_kill_test/` | End-to-end receiver-node kill-test outputs | Comparing synchronized pressure across ACS, EOIR, shelter/capacity, QWI, and politics |
   131	| `../sources/immigration-causal/data/external/eoir_case_data_2026_02/` | EOIR Case Data 2026-0301 archive and code key with acquisition manifest | Building immigration-court pressure panels |
   132	| `../sources/immigration-causal/data/lehd/qwi_county_receiver_panel.parquet` | Repaired QWI county-quarter receiver-state panel, 2017Q1-2024Q4 | Joining labor outcomes to receiver stress panels |
   133	
   134	## Quick Start
   135	
   136	If the question is:
   137	
   138	1. `What do we currently think?` Start with `immigration-verified-findings-report-2026-04-10.md`, then `immigration-confidence-ladder.md`.
   139	2. `Is low-skill immigration good or bad for natives?` Start with `immigration-economist-effects-matrix.md`, then `fiscal-impact-unauthorized-immigration-research-memo.md`, then `full-spectrum-costs-unauthorized-immigration-research-memo.md`.
   140	3. `What data do we have locally?` Start with `immigration-dataset-register.md`, then `../sources/immigration-fiscal/data/MANIFEST.md`.
   141	4. `Can we model this ourselves?` Start with `immigration-lifetime-fiscal-data-stack-2026-04-10.md`, then `immigration-public-data-acquisition-2026-04-11.md`, then `immigration-frontier-data-acquisition-2026-04-11.md`, then the DuckDB build files.
   142	5. `What is the current `<HS` / `HS` / `some college` stock split?` Start with `immigration-education-bucket-stock-and-lifetime-status-2026-04-11.md`.
   143	6. `How do I run the next fiscal/generator sweep?` Start with `../notes/immigration-lifetime-synthesis-diverge-cookbook.md`, then `immigration-thesis-generator-audit-2026-06-16.md`, then `immigration-conclusion-audit-running-fixes.md`.
   144	
   145	<!-- knowledge-index
   146	generated: 2026-04-19T04:47:48Z
   147	hash: 25555c17344c
   148	
   149	table_claims: 97
   150	
   151	end-knowledge-index -->
--- END FILE: research/immigration-INDEX.md ---

--- BEGIN FILE: notes/immigration-lifetime-synthesis-diverge-cookbook.md ---
     1	# Synthesis ↔ Diverge cookbook (immigration lifetime fiscal)
     2	
     3	**Purpose:** Reusable prompt template for the loop that worked in rounds 1–10: **diverge** (data + generators + angles) → **converge** (unified theory + formal multi-model critique) → repeat with a sharper thesis.
     4	
     5	**Instance memos:** `research/immigration-lifetime-unified-theory-2026-06-15.md`, `notes/immigration-lifetime-sweep-protocol.md`, `research/immigration-thesis-generator-audit-2026-06-16.md`
     6	
     7	**Principle:** Data does not automatically kill a good explanation — it kills bad **scalar exports** and unnamed **layer laundering**. Synthesis names the object; divergence hunts what the current frame excludes.
     8	
     9	---
    10	
    11	## The loop (one sweep)
    12	
    13	```
    14	┌─────────────────────────────────────────────────────────────┐
    15	│  CARRY: prior thesis burst + generator menu + DuckDB state  │
    16	└───────────────────────────┬─────────────────────────────────┘
    17	                            ▼
    18	┌─────────────────────────────────────────────────────────────┐
    19	│  DIVERGE (expand surface)                                   │
    20	│  1. Denial cascade / constraint inversion brainstorm        │
    21	│  2. Probe URLs → setup-lifetime.sh → rebuild warehouse      │
    22	│  3. Parallel mine clusters → .mining/*.json → generators MD │
    23	└───────────────────────────┬─────────────────────────────────┘
    24	                            ▼
    25	┌─────────────────────────────────────────────────────────────┐
    26	│  CONVERGE (sharpen thesis)                                  │
    27	│  4. Unified theory (central object, 3-sentence thesis)      │
    28	│  5. Five formal models + critique matrix                      │
    29	│  6. Thesis burst (revise in place) + 3 disconfirmation hunts  │
    30	└───────────────────────────┬─────────────────────────────────┘
    31	                            ▼
    32	                    next sweep (N+1)
    33	```
    34	
    35	**Rule:** Never start diverge round N+1 until converge for round N is written.
    36	
    37	---
    38	
    39	## Non-negotiables (immigration fiscal instance)
    40	
    41	| Do | Don't |
    42	|----|-------|
    43	| Model **education × arrival × state × legal path × time × ledger layer** | Publish "Mexican lifetime NPV" |
    44	| Tag every load-bearing number: DuckDB table or `[SOURCE:]` | Float claims from paper memory |
    45	| Separate **federal annual**, **lifetime NPV**, **local episodic** | Prove layer A → conclude layer B |
    46	| Mine **generators** (mechanical prompts + retrodiction) | Mine only parameter lists |
    47	| Steel-man each model before killing it | Debate authors |
    48	
    49	**Central object (template):**
    50	
    51	```
    52	cell  = {dimensions of the population slice}
    53	layer = {which ledger: federal_annual | lifetime_npv | state_local | local_episodic | private_transfer | admin}
    54	sign  = F(cell, layer, t)   # often opposite-signed across layer
    55	```
    56	
    57	---
    58	
    59	## Phase A — Diverge procedure
    60	
    61	### A1. Brainstorm perturbation (15 min, in-conversation)
    62	
    63	Run three passes; write bullets to sweep memo (`research/immigration-lifetime-dataset-brainstorm-*.md`):
    64	
    65	1. **Denial cascade** — "If microdata never arrives, what still bounds the answer?"
    66	2. **Domain forcing** — map domains (demography, labor, housing, health, legal, admin) → dataset → lifetime lever
    67	3. **Constraint inversion** — "What if we only had aggregates / only had annual / only had local?"
    68	
    69	Output: 8–12 **angles**, each with: what it bounds, what it cannot say, acquire path (automated / copy / manual).
    70	
    71	### A2. URL probe batch (script, not hope)
    72	
    73	```bash
    74	# Pattern: curl first 120KB, pdftotext page 1, grep immigration keywords
    75	# Keep only if title matches; skip NBER ID fishing without title check
    76	```
    77	
    78	Add winners to `infra/immigration-fiscal/acquire/setup-lifetime.sh` + `DOWNLOAD_MANIFEST.tsv`.
    79	
    80	**Copy layer:** derived CSVs, admin PDFs, and sibling-stack files often beat new PDF hunts.
    81	
    82	### A3. Acquire + warehouse
    83	
    84	```bash
    85	cd infra/immigration-fiscal && bash acquire/setup-lifetime.sh
    86	bash rebuild_lifetime_warehouse.sh   # loads .mining/*.json into DuckDB
    87	```
    88	
    89	### A4. Parallel mine (subagent prompt template)
    90	
    91	Dispatch **3–4 clusters** per sweep (not one mega-agent). Each cluster = 3–8 sources max.
    92	
    93	```
    94	You are mining corpus cluster {CLUSTER_ID} for lifetime fiscal immigration research.
    95	
    96	**Frame (non-negotiable):**
    97	- No scalar "Mexican lifetime NPV."
    98	- Model: education_bucket × age_at_arrival × state × legal_status_path × descendants.
    99	- Distinguish ledger layers: federal_annual vs lifetime_npv vs local_episodic.
   100	
   101	**Sources (read with pdftotext / pandas for CSV):**
   102	{LIST_PATHS}
   103	
   104	**Cross-read:** research/immigration-lifetime-unified-theory-2026-06-15.md (current thesis)
   105	**Avoid duplicating generators in:** research/immigration-lifetime-fiscal-generators.md
   106	
   107	**Output JSON:** research/.mining/immigration-lifetime-cluster-{slug}.json
   108	
   109	{
   110	  "cluster": "{CLUSTER_NAME}",
   111	  "mined_at": "YYYY-MM-DD",
   112	  "parameter_claims": [
   113	    {
   114	      "claim_id": "X-001",
   115	      "source_rel_path": "external/lifetime/...",
   116	      "parameter_name": "...",
   117	      "value_numeric": null,
   118	      "unit": "...",
   119	      "population": "...",
   120	      "unnamed_assumption": true,
   121	      "page_ref": "pdftotext p.N",
   122	      "notes": "..."
   123	    }
   124	  ],
   125	  "generators": [
   126	    {
   127	      "id": "G-LIF-{X}01",
   128	      "name": "...",
   129	      "prompt": "Mechanical question an agent can run without creativity...",
   130	      "retrodiction": "Would have surfaced findings A and B before we had them because...",
   131	      "negative_space": "What the standing frame excludes",
   132	      "unnamed_assumptions_surfaced": ["..."],
   133	      "topics": ["..."],
   134	      "source_rel_paths": ["..."]
   135	    }
   136	  ],
   137	  "theories_tested": [
   138	    {
   139	      "theory": "...",
   140	      "prediction": "...",
   141	      "duckdb_test": "SQL against life.* or ctx.* tables",
   142	      "falsifier": "..."
   143	    }
   144	  ]
   145	}
   146	
   147	**Targets per cluster:** 6–10 claims, 4–5 generators (retrodiction required), 3 theories with SQL.
   148	Return brief summary only.
   149	```
   150	
   151	**Cluster menu (reuse / extend):**
   152	
   153	| ID | Theme | Example sources |
   154	|----|-------|-----------------|
   155	| A | NPV / generational / NAS critique | NAS, Clemens, Colas-Sachs, Lee-Miller |
   156	| B | Labor / Mariel / wages | Borjas, Card, Peri, Foged-Peri |
   157	| C | Local / welfare / capacity | CBO 61256, Gould, magnets, crime |
   158	| D | Composition / descendants | Hanson, Abramitzky, Duncan-Trejo |
   159	| E | Housing / Saiz | elasticity .dta, FRBSF, VMT |
   160	| F | High-skill / H-1B | Bound w23153, Ottaviano w12497 |
   161	| G | Legal / tax floor | ITEP, Pew, border enforcement |
   162	| H | Refugee / mortality | IZA refugee, CDC life tables |
   163	| I | Return migration | Duleep-Regets IZA |
   164	| J | Admin / enforcement | CBP/ICE budgets, LPR xlsx |
   165	| K | Incidence bridge | stage2/5 derived CSVs |
   166	| L | OECD / health bridge | Ortega-Peri, MEPS cells |
   167	
   168	After mining: rebuild DuckDB, regenerate `research/immigration-lifetime-fiscal-generators.md`.
   169	
   170	### A5. Generator quality gate
   171	
   172	From `~/Projects/skills/leverage/references/generators.md`:
   173	
   174	1. **Cluster** miss-patterns into abstract moves (not one generator per paper).
   175	2. **Retrodiction:** each generator must retrodict ≥2 prior findings.
   176	3. **Negative space:** name what the frame excludes.
   177	4. **Consumption:** every generator links to DuckDB test or explicit data gap.
   178	5. **Park** generators that cycle twice with zero adopted output while applicable; retirement is manual and append-only.
   179	
   180	---
   181	
   182	## Phase B — Converge procedure (synthesis prompt)
   183	
   184	Run **after** diverge, **before** next downloads. Paste into main agent or dedicated synthesis pass.
   185	
   186	```
   187	You are writing the post-sweep CONVERGE pass for immigration lifetime fiscal research.
   188	
   189	**Read first:**
   190	- research/immigration-lifetime-unified-theory-2026-06-15.md (prior thesis burst)
   191	- research/immigration-lifetime-fiscal-generators.md (new generators)
   192	- Query DuckDB:
   193	  ATTACH 'warehouse/immigration_context.duckdb' AS ctx (READ_ONLY);
   194	  ATTACH 'warehouse/immigration_lifetime_evidence.duckdb' AS life (READ_ONLY);
   195	  -- key tables: origin_fiscal_scenario_2023, npv_education_benchmarks,
   196	  -- acs_foreign_born_education_bucket_totals_2023, parameter_claims, lifetime_generators
   197	
   198	**Write / update:** research/immigration-lifetime-unified-theory-2026-06-15.md
   199	
   200	## I. Unified theory
   201	- Name the central object (tensor / cell × layer × time — NOT a scalar).
   202	- 3-sentence thesis: what is compatible, what only looks contradictory, why politics fights over layers.
   203	- Table: layer → best instrument → what it is NOT.
   204	- Verifiable anchors table (number | value | DuckDB/SOURCE).
   205	
   206	## II. Five formal models
   207	For M1–M5 (mechanisms, not authors):
   208	- Grammar (ledger rules)
   209	- Core prediction
   210	- Falsifiers
   211	- Unnamed assumptions
   212	- Data status (strong / medium / gap)
   213	
   214	Use the five-model menu unless the sweep surfaced a better split:
   215	  M1 NAS accountant | M2 GE offset | M3 Local incidence | M4 Borjas pessimist | M5 Dynamic composition
   216	
   217	## III. Cross-model critique matrix
   218	Rows = questions (lifetime sign, annual federal, rent, shelter, descendants).
   219	Columns = M1–M5.
   220	Mark irreconcilables as frame fights vs data fights.
   221	State explicitly: "What data cannot kill" (coherent stories in wrong layer).
   222	
   223	## IV. Disconfirmation
   224	Three active hunts that would flip thesis sign on some layer.
   225	
   226	## V. Thesis burst
   227	Paste prior sweep thesis verbatim, then revise in place:
   228	- Sharper than last sweep
   229	- Killed
   230	- Survived despite weak data
   231	
   232	## Revisions table
   233	| Date | Sweep | What changed and why |
   234	
   235	**Constitution tags:** [SOURCE:] [INFERENCE] [FRAMING-SENSITIVE] on load-bearing claims.
   236	**Quant gate:** notes/quant-bias-checklist.md for numbers doing argumentative work.
   237	```
   238	
   239	---
   240	
   241	## Phase B2 — Five-model critique (standalone mini-prompt)
   242	
   243	Use when you only need formal adversarial structure without full memo rewrite.
   244	
   245	```
   246	Given thesis T and datasets D, produce five MECHANISM models (not people):
   247	
   248	For each model Mi:
   249	1. State variables and ledger (what enters the sum)
   250	2. Prediction for cell = <HS, recent arrival, Mexico-weighted> on layers {federal_annual, lifetime_npv, local}
   251	3. One empirical fact from D that supports Mi
   252	4. One fact from D that threatens Mi
   253	5. One unnamed assumption Mi smuggles in
   254	
   255	Then:
   256	- 5×5 matrix: models vs {lifetime, annual, local, housing, descendants}
   257	- List disagreements that are DATA-resolvable vs FRAME-resolvable
   258	- One paragraph: "Data cannot kill X because ..."
   259	
   260	Do not pick a winner. Name what each model is for.
   261	```
   262	
   263	---
   264	
   265	## Phase B3 — Thesis burst (carry-forward template)
   266	
   267	Paste at top of `## V. Thesis burst` every sweep:
   268	
   269	```markdown
   270	### Sweep {N-1} thesis (verbatim)
   271	> {paste previous 3 sentences}
   272	
   273	### Sweep {N} revision
   274	> {new 3 sentences}
   275	
   276	**Sharper:** ...
   277	**Killed:** ...
   278	**Survived (weak data):** ...
   279	**New falsifier:** ...
   280	```
   281	
   282	---
   283	
   284	## Artifact checklist (per sweep)
   285	
   286	| Artifact | Path | Done? |
   287	|----------|------|-------|
   288	| Brainstorm angles | `research/immigration-lifetime-dataset-brainstorm-*.md` | ☐ |
   289	| Manifest rows | `infra/immigration-fiscal/DOWNLOAD_MANIFEST.tsv` | ☐ |
   290	| Staged files | `infra/immigration-fiscal/external/lifetime/` (from acquisition cwd) | ☐ |
   291	| Mining JSON | `research/.mining/immigration-lifetime-cluster-*.json` | ☐ |
   292	| Generators registry | `research/immigration-lifetime-fiscal-generators.md` | ☐ |
   293	| DuckDB rebuild | `bash rebuild_lifetime_warehouse.sh` | ☐ |
   294	| **Unified theory** | `research/immigration-lifetime-unified-theory-*.md` | ☐ |
   295	| Cross-disciplinary audit | `research/immigration-thesis-generator-audit-2026-06-16.md` | ☐ |
   296	| Running fixes | `research/immigration-conclusion-audit-running-fixes.md` | ☐ |
   297	| Index row | `research/immigration-INDEX.md` | ☐ |
   298	
   299	---
   300	
   301	## Anti-patterns (learned the hard way)
   302	
   303	| Anti-pattern | Fix |
   304	|--------------|-----|
   305	| NBER ID fishing without `pdftotext` title check | Probe → title → then acquire |
   306	| Scalar "Mexico NPV" | Composition weights on education cells only |
   307	| Download without synthesis | Converge memo before round N+1 |
   308	| Generators without retrodiction | Reject; cluster into abstract moves |
   309	| Wage paper → fiscal verdict | Generator: "wage effect ≠ fiscal effect" |
   310	| Layer laundering | Matrix: which layer each model owns |
   311	| Ignoring unit bugs ($21 per-pupil) | Incidence-bridge generator + disconfirmation hunt |
   312	| One mega subagent for all PDFs | 3–4 clusters × 4–5 generators |
   313	
   314	---
   315	
   316	## One-liner prompts (quick invoke)
   317	
   318	| Intent | Prompt |
   319	|--------|--------|
   320	| Full sweep diverge | `brainstorm more angles → probe → acquire → mine 4 clusters → rebuild DuckDB` |
   321	| Full sweep converge | `run converge pass per notes/immigration-lifetime-synthesis-diverge-cookbook.md Phase B` |
   322	| Generators only | `mine cluster {X}; retrodiction-test; append to generators MD` |
   323	| Cross-disciplinary generators | `run research/immigration-thesis-generator-audit-2026-06-16.md XDISC packet before source search` |
   324	| Theory only | `update unified theory + 5 models; thesis burst; 3 falsifiers` |
   325	| Negative space | `what layer is the current thesis silently exporting? name 5 unnamed assumptions` |
   326	
   327	---
   328	
   329	## Adapting to other topics
   330	
   331	Replace:
   332	
   333	- `cell` dimensions (e.g. genotype × tissue × time for bio)
   334	- `layer` ledgers (e.g. molecular vs clinical vs population)
   335	- Five-model menu (mechanisms native to the field)
   336	- DuckDB attach paths
   337	- Cluster source lists
   338	
   339	Keep the **loop order**: diverge → converge → repeat. The fruitful part was never volume alone — it was **synthesis forcing the thesis to get sharper while divergence hunted what the thesis could not yet see**.
--- END FILE: notes/immigration-lifetime-synthesis-diverge-cookbook.md ---

--- BEGIN FILE: notes/immigration-lifetime-sweep-protocol.md ---
     1	# Immigration lifetime fiscal — sweep protocol
     2	
     3	**Purpose:** After every acquisition/mining sweep (round N), force synthesis before the next download burst. Data does not automatically kill good explanations — but unexplained predictions should.
     4	
     5	**Full prompt templates:** `notes/immigration-lifetime-synthesis-diverge-cookbook.md`
     6	
     7	## After each sweep (mandatory order)
     8	
     9	1. **Unified theory** — one memo section answering: *What is the single best story that holds all layers together?* Name the central object (not a scalar), the dimensions, what is compatible vs contradictory, and the current thesis in ≤3 sentences.
    10	2. **Five-model formal critique** — state five competing models (not authors — *mechanisms*). For each: core equation/ledger, predictions, data that would falsify, unnamed assumptions exposed.
    11	3. **Thesis burst (carry-forward)** — paste the prior sweep's thesis; revise it in place. Mark what got sharper, what got killed, what survived despite weak data.
    12	4. **Disconfirmation pass** — three active hunts for evidence that would flip the thesis sign on any layer.
    13	5. **Only then** — run `research/immigration-thesis-generator-audit-2026-06-16.md` XDISC packet, then brainstorm round N+1 downloads, generators, DuckDB loads.
    14	
    15	## Output locations
    16	
    17	| Artifact | Path |
    18	|----------|------|
    19	| Living unified theory + 5 models | `research/immigration-lifetime-unified-theory-YYYY-MM-DD.md` (update in place; add `## Revisions` at bottom per sweep) |
    20	| Generators / claims | `research/.mining/` → DuckDB rebuild |
    21	| Sweep brainstorm | `research/immigration-lifetime-dataset-brainstorm-*.md` |
    22	
    23	## Central object (do not collapse)
    24	
    25	**Fiscal incidence tensor** — not "Mexican lifetime NPV."
    26	
    27	```
    28	(cell) = education_bucket × age_at_arrival × state/PUMA × legal_status_path × cohort_time
    29	(layer) = federal_annual | lifetime_npv | state_local_flow | local_episodic | private_transfer | admin_enforcement
    30	```
    31	
    32	Mexico enters only as **ACS composition weights** on cells, never as a single number.
    33	
    34	## Five-model menu (reuse every sweep)
    35	
    36	| Model | Mechanism | Typical sign for `<HS` recent surge |
    37	|-------|-----------|--------------------------------------|
    38	| **M1 NAS accountant** | Education-age lifetime NPV; public goods excluded | Negative individual NPV |
    39	| **M2 GE offset** | Capital tax + labor complementarity + indirect fiscal | Positive or flipped NPV |
    40	| **M3 Local incidence** | Inelastic housing + schools + shelter episodics | Negative local / renter welfare |
    41	| **M4 Borjas pessimist** | Substitution, welfare assimilation, spatial attenuation | Negative wages → negative fiscal |
    42	| **M5 Dynamic composition** | Time-varying weights, return migration, legal-status selection | Sign depends on horizon & attrition |
    43	
    44	Critique = where these agree, where they talk past each other, and which disagreements are **data-resolvable** vs **frame-resolvable**.
    45	
    46	## Quant gate
    47	
    48	Before committing numbers in the unified theory memo: load-bearing figures must cite DuckDB table or `[SOURCE:]` tag. See `notes/quant-bias-checklist.md`.
--- END FILE: notes/immigration-lifetime-sweep-protocol.md ---

--- BEGIN FILE: research/immigration-lifetime-fiscal-generators.md ---
     1	# Immigration lifetime fiscal — idea generators
     2	
     3	**Date:** 2026-06-15 (rounds A–P)
     4	**DuckDB:** `warehouse/immigration_lifetime_evidence.duckdb`
     5	
     6	**Totals:** 563 DuckDB `parameter_claims`, 106 Markdown `G-LIF-*` headings / 104 DuckDB `lifetime_generators` rows across 19 clusters (Q,R,S added 2026-06-15; S06–S15 from marker-modal parse 2026-06-15). Count reconciliation pending: MD-only IDs are `G-LIF-Q06` and `G-LIF-S15`. See `immigration-thesis-generator-audit-2026-06-16.md`.
     7	
     8	## A_npv_generational
     9	
    10	### G-LIF-A01 — Capital-tax omission audit
    11	
    12	**Prompt:** For each lifetime fiscal NPV study in the corpus: list every tax base counted on the revenue side. If corporate/capital income is absent, mechanically apply α/(1-α) × τ_K/τ_L × labor tax base (Clemens 2023 eq. 14) and re-rank education cells by sign. Flag any headline scalar that flips.
    13	
    14	**Retrodiction:** Would have surfaced Clemens (2023) capital-tax flip (-$109k→+$128k for <HS) AND Colas-Sachs critique that Storesletten (2000) omits capital-supply response — both hinge on the same omitted tax base before reading either paper's policy conclusion.
    15	
    16	**Negative space:** Standing frame treats 'taxes paid by immigrants' as labor+payroll cashflow only; excludes owner-side capital incidence entirely.
    17	
    18	### G-LIF-A02 — Public-goods allocation stress grid
    19	
    20	**Prompt:** Build a 3×3 grid for every NPV table: {zero marginal, 0.25×AC, full AC} × {exclude defense, include defense, include all public goods}. Extract the cell each paper reports as 'the' estimate. Never cite a scalar without grid coordinates.
    21	
    22	**Retrodiction:** Would have flagged NAS Table 8-12/8-13 dual panels (public goods in/out) AND Orrenius marginal-cost sensitivity AND Colas-Sachs Table 3 (-$86/yr vs -$2,429/yr for HS dropouts) before treating -$109k as robust.
    23	
    24	**Negative space:** Debates anchor a single NPV number; papers bury allocation rules in table notes.
    25	
    26	### G-LIF-A03 — Composition-vs-level decomposition
    27	
    28	**Prompt:** For generational-accounting immigration papers: (1) simulate level change holding 1990 education mix fixed; (2) simulate education-mix shift holding count fixed; (3) report which moves fiscal imbalance >10× more than the other. Reject any study reporting only total immigrant NPV.
    29	
    30	**Retrodiction:** Would have extracted Auerbach-Oreopoulos (2000) finding that composition beats level AND Lee-Miller (1998) $2.2k vs $49.7k scale result AND NAS contrast of recent (+$259k) vs all-immigrant (+$58k) pools.
    31	
    32	**Negative space:** Policy argument uses 'more immigrants' scalar; literature says education mix is first-order.
    33	
    34	### G-LIF-A04 — Unit harmonizer: annual incidence vs lifetime NPV
    35	
    36	**Prompt:** Whenever a fiscal claim uses $/year (incidence, MVPF, annuitized direct), convert to 75-year NPV at stated discount AND label incomparable if indirect/general-equilibrium. Block synthesis until units match.
    37	
    38	**Retrodiction:** Would have caught Colas-Sachs ~$753/yr indirect vs NAS -$109k lifetime as different objects AND Clemens factor-3.2 adjustment on same NAS table AND Orrenius mixing cross-section billions with NPV thousands.
    39	
    40	**Negative space:** Standing frame collapses 'fiscal effect' into one ledger line.
    41	
    42	### G-LIF-A05 — Immigrant attribution convention check
    43	
    44	**Prompt:** In generational accounting papers: trace whether immigrants' taxes are folded into native cohorts or separate Q_{s,k} terms. Recompute headline imbalance under both conventions. Document which convention each citation uses.
    45	
    46	**Retrodiction:** Would have found Lee-Miller 54% vs GPS 72% imbalance gap AND Green-Kotlikoff warning that fiscal labels are reference-dependent AND NAS Table 8-13 native/immigrant pairing.
    47	
    48	**Negative space:** Treats generational accounting as objective balance sheet.
    49	
    50	### G-LIF-A06 — Descendant ledger split
    51	
    52	**Prompt:** For every lifetime NPV, force extraction of {individual, descendants, total} columns. Flag papers that report total only. Test whether descendant surplus drives positive headline for low-skilled arrivals.
    53	
    54	**Retrodiction:** Would have surfaced NAS $173k individual + $85k descendants (= $259k) AND Clemens -$109k individual vs +$326k with grandchildren AND NAS No-Budget scenario where descendants are -$15k while immigrant +$92k.
    55	
    56	**Negative space:** Headline 'immigrant fiscal impact' silently includes second/third generation without education×age path.
    57	
    58	---
    59	
    60	## B_labor_market
    61	
    62	### G-LIF-B01 — Native out-migration fiscal residue
    63	
    64	**Prompt:** For each immigration shock geography (state, MSA, PUMA), ask: what fraction of the measured local wage/fiscal burden is attenuated because natives left (Borjas w11610 40-60% band)? Who remains to pay state/local taxes and use schools — incumbents, in-migrants, or replacement population? Build a sensitivity table: full shock vs attenuated shock on origin×PUMA ledger.
    65	
    66	**Retrodiction:** Would have surfaced w11610 attenuation, Card-Peri JEL Table 3 mobility debate, and brainstorm Round 8 note on PUMA fiscal attribution before treating ACS snapshot populations as shock bearers.
    67	
    68	**Negative space:** Standing NAS/SIPP frame assigns costs to immigrants present in a cell without modeling native selective exit from high-immigrant PUMAs.
    69	
    70	### G-LIF-B02 — Task complementarity vs substitution band
    71	
    72	**Prompt:** When national estimates show large wage losses for <HS (Borjas) but area studies show nulls (Card), search for task-specialization or native-immigrant imperfect substitution mechanisms (Peri-Sparber, Ottaviano-Peri, Foged-Peri). Map the implied earnings-path band to indirect fiscal offsets (Colas-Sachs-style) rather than point-estimate NAS <HS NPV.
    73	
    74	**Retrodiction:** Would have connected Peri-Sparber w13389, Foged-Peri w19315, Ottaviano-Peri w14188, and Card-Peri w32389 into a single complementarity sensitivity band before treating Borjas -4% as the earnings anchor.
    75	
    76	**Negative space:** Canonical CES perfect substitution within education cell — no task reallocation, no σ_IMMI heterogeneity.
    77	
    78	### G-LIF-B03 — Mariel <HS calibration bracket
    79	
    80	**Prompt:** Treat Mariel boatlift as mandatory stress-test for <HS lifetime cell calibration: Card null (7% labor force, ~20% less-skilled supply) vs Borjas -13% to -15% immediate log wage vs race-adjusted recovery by 1990. Require any <HS NPV projection to declare where it sits in this bracket and why.
    81	
    82	**Retrodiction:** Would have flagged Mariel stack (w3069, w21850, w23504) as the key falsifier for mapping wage pessimism into NAS -$109k <HS age-25 cell without sensitivity.
    83	
    84	**Negative space:** Single canonical wage elasticity applied to all low-skill inflows regardless of shock size, sample definition, or recovery horizon.
    85	
    86	### G-LIF-B04 — Wage effect ≠ fiscal effect
    87	
    88	**Prompt:** Whenever a paper reports wage elasticity (e.g., 10% supply → 3-4% wage), ask what fiscal ledger line it actually moves: earnings tax base? transfer take-up? incarceration cost? school demand? Flag papers that infer fiscal sign from wage sign without PAYG, capital adjustment, or local cost channels.
    89	
    90	**Retrodiction:** Would have blocked silent import of Borjas w9755 -4% into NAS <HS NPV without Storesletten/Clemens capital-tax and federal-offset disconfirmation passes.
    91	
    92	**Negative space:** Competitive labor market partial equilibrium — wage change is sufficient statistic for immigrant fiscal externality.
    93	
    94	### G-LIF-B05 — Sample-specification audit for <HS cells
    95	
    96	**Prompt:** Before accepting any <HS wage estimate, audit sample rules: age floor (exclude 16-18 enrolled students misclassified as dropouts), sex pooling, Hispanic inclusion in 'native' trends, placebo city choice. Re-run sensitivity on Mexico-weighted <HS cell with each contamination flagged.
    97	
    98	**Retrodiction:** Would have caught Borjas w21850 critique of Peri-Yasenov 16-18 misclassification and Card-Peri JEL pit-vs-mit specification fork before locking calibration parameters.
    99	
   100	**Negative space:** Education bucket from CPS highest grade completed taken at face value without age/enrollment filters.
   101	
   102	### G-LIF-B06 — Distributional spillover beyond average native
   103	
   104	**Prompt:** Search for immigration effects on subgroups omitted from average-native fiscal cells: Black employment/incarceration (Borjas-Grogger-Hanson), young/low-tenure manual workers (Foged-Peri). Ask whether lifetime ledger needs subgroup rows, not just education×state averages.
   105	
   106	**Retrodiction:** Would have surfaced w12518 incarceration channel and Foged-Peri young-worker upgrading as missing ledger lines in Mexico <HS scalar debates.
   107	
   108	**Negative space:** Representative native worker sufficient for fiscal incidence; no racial or tenure heterogeneity.
   109	
   110	---
   111	
   112	## C_local_welfare_capacity
   113	
   114	### G-LIF-C01 — Federal-positive / local-negative ledger split
   115	
   116	**Prompt:** For each fiscal immigration study, tag every cost and revenue line as FEDERAL vs STATE/LOCAL vs EPISODIC-SHOCK (shelter, border). Where does the paper silently aggregate jurisdictions? Cross-walk to our SIPP annual federal proxy (+$1,519/yr Mexico <HS) vs CBO-style local shock ledger (school, shelter, Medicaid). List papers that report net positive lifetime NPV but omit local surge lines.
   117	
   118	**Retrodiction:** Would have surfaced CBO 61256 $9.2B direct net cost, Gould shelter 60% of homelessness rise, Orrenius 2025 federal-positive/state-local-negative split, and our scenario-composition frame tension before treating SIPP cells as scalar verdict.
   119	
   120	**Negative space:** Lifetime NPV and generational accounting collapse jurisdiction and time horizon — hiding episodic shelter shocks and balanced-budget state constraints.
   121	
   122	### G-LIF-C02 — Welfare magnet: selection vs treatment vs policy regime
   123	
   124	**Prompt:** Map each welfare-migration paper to (a) migrant self-selection (treatment on movers), (b) host policy filter (treatment on admissions), (c) free vs restricted mobility regime. Does generosity affect skill mix (Razin-Wahba) or flow level (Landais Denmark DiD)? Flag studies that interpret correlation as magnet without regime dummies.
   125	
   126	**Retrodiction:** Would have found Razin-Wahba sign flip, Landais 5k/yr causal reduction and elasticity 1.3, Bitler-Hoynes post-PRWORA immigrant lower participation within poor households, Borjas w4872 assimilation-into-welfare cohort effects.
   127	
   128	**Negative space:** US interstate magnet literature often ignores that PRWORA made immigration policy federalism — treatment is policy+selection entangled.
   129	
   130	### G-LIF-C03 — Crime/incarceration: fiscal line item or labor spillover?
   131	
   132	**Prompt:** Separate incarceration as (1) direct state/local budget line (CBO incarceration spending) from (2) labor-market/competition spillover (Borjas-Grogger-Hanson) from (3) compositional base-rate artifact (Butcher-Piehl native 2.16% vs immigrant 0.7%). Which lifetime fiscal models include any of these channels?
   133	
   134	**Retrodiction:** Would have flagged Butcher w6067 low immigrant incarceration vs rising native rates, CBO surge prison share (4% state, 7% pop), and brainstorm note that NAS ledger omits crime channel.
   135	
   136	**Negative space:** Advocacy frames swap fiscal incarceration costs for crime rates; empirical lit shows immigrants lower institutionalization — channel is distributional not average fiscal drain.
   137	
   138	### G-LIF-C04 — Asylum/shelter episodic shock outside lifetime NPV
   139	
   140	**Prompt:** Identify spending that is (a) emergency/episodic, (b) city-concentrated, (c) absent from NAS/CBO federal lifetime tables. Quantify shelter PIT/HUD linkage (Gould) vs K-12 entitlement (CBO Plyler) vs Medicaid federal-state match. Would discounting lifetime NPV miss 2022-2024 shelter spike?
   141	
   142	**Retrodiction:** Would have surfaced Gould 60% of 43% sheltered rise, CBO $3.3B shelter in 4 states, NYC +77,352 sheltered 2022-2024, and mismatch with smooth lifetime NPV curves.
   143	
   144	**Negative space:** Lifetime fiscal synthesis uses steady-state education/transfer paths — asylum parole surges are state-local balance-sheet events.
   145	
   146	### G-LIF-C05 — County fiscal capacity heterogeneity
   147	
   148	**Prompt:** Where do national-average fiscal estimates hide county-level capacity constraints? Use BoC county IV design: low-skilled inflow → per-capita revenue down, spending down (Presidio −15%) vs high-skilled uplift (Monterey +14%). Cross to our PUMA/stage5 school spend weights and FRBSF urban concentration.
   149	
   150	**Retrodiction:** Would have found BoC 0.3%/yr national offset masking ±15% county swings, FRBSF urban/remittance concentration, VMT $0.218/urban-mile congestion add-on, CBO 56% surge in 6 states.
   151	
   152	**Negative space:** Scalar 'Mexico NPV' erases geography — same immigrant type can expand or contract local public goods depending on county skill mix and transfer insurance.
   153	
   154	### G-LIF-C06 — Descendant and mobility offsets on local burden
   155	
   156	**Prompt:** Track who bears local costs vs who captures fiscal upside: Orrenius assigns K-12 cost to US-born children; Akers-Boustan shows bottom-decile native HS completion +2.2pp per 10pp inflow; Blau-Kahn decomposes inequality not net fiscal position. Does immigrant-headed household federal proxy include citizen-child benefits without citizen-child future taxes?
   157	
   158	**Retrodiction:** Would have connected Orrenius descendant-cost framing, Akers-Boustan decile-heterogeneous mobility, Blau-Kahn compositional inequality, Bitler-Hoynes 90% immigrant households contain native-born members.
   159	
   160	**Negative space:** Household-weighted federal proxy treats citizen children as immigrant fiscal property in both costs and benefits.
   161	
   162	---
   163	
   164	## D_composition_descendants
   165	
   166	### G-LIF-D01 — Static ACS snapshot vs Hanson composition time series
   167	
   168	**Prompt:** For each origin×education_bucket cell in the scenario ledger, compare (a) a single ACS 2023 composition weight to (b) a Hanson w23753 time-varying weight series (1990–2015 Mexico/Latin America <HS shares, post-2007 inflow slowdown). Where does a static snapshot mis-state the stock entering the NAS <HS age-25 NPV cell?
   169	
   170	**Retrodiction:** Would have surfaced Hanson 510k→−160k undocumented swing, Mexico share peaking 2005 then declining, and the brainstorm memo's Round 8 'composition over time' angle before building origin_fiscal_scenario with fixed ACS weights.
   171	
   172	**Negative space:** Standing frame treats ACS 2023 as sufficient composition prior; excludes epochal composition drift and attrition-driven stock stabilization.
   173	
   174	### G-LIF-D02 — Return migration / attrition ledger (CHCP blocked)
   175	
   176	**Prompt:** Build an attrition sensitivity band on lifetime NPV: (1) Lubotsky/Dustmann selective re-migration bias on assimilation, (2) Hanson post-2007 net undocumented outflow, (3) Duncan-Trejo ethnic attrition on 3rd+ Hispanic measurement. Flag data gaps: Aydemir-Robinson CHCP working paper HTML-only trap; no US fiscal micro for return migration. What ledger line adjusts NPV horizon when attrition is negatively selected?
   177	
   178	**Retrodiction:** Would have flagged brainstorm Round 8 item 10 (CHCP blocked) and Dustmann survey §5.9 return-migration gap before treating SIPP annual proxy as full lifetime residence.
   179	
   180	**Negative space:** Lifetime fiscal models assume immigrants remain until death; cross-sectional assimilation overstates economic success.
   181	
   182	### G-LIF-D03 — Descendant NPV as separate ledger line
   183	
   184	**Prompt:** Split lifetime ledger into (A) first-generation immigrant NPV from NAS education×age cells and (B) descendant offset line with two bounds: Abramitzky w26408 (+3–6 percentile mobility at bottom; geographic sorting explains 70%) vs Duncan-Trejo w24394 (Hispanic 2nd→3rd+ earnings stall; ethnic attrition may understate progress). UK Dustmann-Frattini shows descendant accounting breaks at age 16. Where is descendant NPV missing from compose_scenario_ledger?
   185	
   186	**Retrodiction:** Would have paired brainstorm Round 5 items 3–4 (descendant upside/downside) and UK methodology comparator before collapsing descendants into same NAS cell as parents.
   187	
   188	**Negative space:** NAS descendant column treated as single calibrated offset; no explicit Abramitzky–Duncan-Trejo band or separate ledger row.
   189	
   190	### G-LIF-D04 — Political economy of transfers (taxpayer wallet frame)
   191	
   192	**Prompt:** Audit lifetime fiscal memos for the unnamed assumption fiscal impact = native taxpayer wallet only. Cross-read Razin-Sadka-Swagel (demogrant coalitions; unskilled policy dominance), Alesina w24733/w25562 (immigration salience → less redistribution; welfare-state size heterogeneity), and IMF remittance offset. What transfers are excluded from the ledger (remittances, origin-country education subsidy, voter preference shift)?
   193	
   194	**Retrodiction:** Would have surfaced brainstorm Round 3 item 4 (Alesina redistribution) and Round 5 political-economy pairing before treating NAS net fiscal as welfare-neutral accounting.
   195	
   196	**Negative space:** Technical NPV treated as sufficient for policy; political feedback on transfer generosity and native fiscal capacity ignored.
   197	
   198	### G-LIF-D05 — Legal-status → education-bucket transition path
   199	
   200	**Prompt:** Map legal-status shocks (DACA w24315: +5.9pp HS completion, 40% citizen gap closure; Hanson undocumented share of <HS stock) to education_bucket transitions in the scenario ledger. Does a legalization path move cells from <HS toward HS, changing NAS NPV sign within the same ACS origin weight?
   201	
   202	**Retrodiction:** Would have connected brainstorm Round 4 Kuka DACA item to education-bucket composition before treating legal status as orthogonal to NAS cell assignment.
   203	
   204	**Negative space:** Legal status treated as parallel unauthorized earnings path, not as human-capital investment response shifting education bucket.
   205	
   206	### G-LIF-D06 — Migrant networks and destination-selection composition
   207	
   208	**Prompt:** Borjas-Monras w23756: hurricane shocks × prior US migrant stock (threshold 0.86%) → legal immigration via family reunification. Abramitzky w22381: name-based assimilation closes half the gap in 20 years. How does network-driven destination selection reweight state/PUMA fiscal incidence vs national ACS composition weights?
   209	
   210	**Retrodiction:** Would have surfaced network-fixed-cost mechanism and border-state concentration (Hanson table 3) before applying national Mexico weights to state stage5 context.
   211	
   212	**Negative space:** Origin composition weights applied nationally; destination network sorting and border-state hours-share ignored.
   213	
   214	---
   215	
   216	## E_housing_rent
   217	
   218	### G-LIF-E01 — Rent exposure vs renter welfare loss (Saiz gate)
   219	
   220	**Prompt:** For each fiscal/local-burden memo, tag rent findings as (a) price level, (b) renter incidence, (c) owner offset, (d) supply elasticity quartile. Where does the paper treat median gross rent as welfare loss without Saiz? Cross-walk adversarial review 'rent exposure ≠ welfare loss' to repo merge: inelastic Q1 FB 11.6% vs elastic Q4 4.4%.
   221	
   222	**Retrodiction:** Would have surfaced Saiz merge re-grade before using origin_puma_household_context rent burden as benign exposure; Miami/LA/SF/SJ at elasticity floor.
   223	
   224	**Negative space:** Lifetime NPV and PUMA rent tables omit housing supply elasticity — same rent $ can be absorbed (elastic) or pure renter loss (inelastic).
   225	
   226	### G-LIF-E02 — Regulatory vs topographic supply channel
   227	
   228	**Prompt:** Decompose Saiz inelastic MSAs into WRLURI (regulation) vs S_LAND_50 / FLAT_SHARE_50_15 (topography). Which immigrant-heavy destinations are regulation-bound vs land-bound? Flag papers that cite 'build more housing' without naming which constraint binds.
   229	
   230	**Retrodiction:** Would have split Boston/NYC/SF (low elasticity + high WRLURI) from mountain/desert MSAs; policy lever differs (zoning reform vs nothing).
   231	
   232	**Negative space:** Fiscal immigration debate treats housing as generic local cost — not as regulatory externality vs geographic fact.
   233	
   234	### G-LIF-E03 — Remittance-attenuated housing demand (FRBSF offset)
   235	
   236	**Prompt:** Map FRBSF/Albert-Monras mechanism (lower housing consumption, remittance-reduced COL pass-through) against Saiz-conditional rent burden. When does urban selection into inelastic cities dominate demand attenuation? Tag origin groups by remittance intensity (World Bank) × MSA elasticity.
   237	
   238	**Retrodiction:** Would have reconciled FRBSF 'immigrants less deterred by COL' with repo 'immigrants in inelastic expensive MSAs' — both true; net renter welfare sign needs tenure mix.
   239	
   240	**Negative space:** Remittance literature and rent-burden warehouse rarely joint-conditioned on elasticity quartile.
   241	
   242	### G-LIF-E04 — Urban per-mile externality layer (VMT) missing from lifetime NPV
   243	
   244	**Prompt:** Identify local costs that scale with urban driving not gallons: VMT/congestion (Langer-Maheshri-Winston), differentiated urban/rural tax welfare +$10.5B. Cross to FRBSF urban immigrant concentration. Does NAS lifetime ledger include any non-housing urban externality?
   245	
   246	**Retrodiction:** Would have added per-mile congestion margin alongside PUMA rent; immigrant urban sorting → double local channel (rent + VMT) in same MSAs.
   247	
   248	**Negative space:** Housing-heavy vs school-heavy typology ignores third 'urban mobility' ledger line.
   249	
   250	### G-LIF-E05 — education_bucket × state × elasticity scenario cell
   251	
   252	**Prompt:** Refuse scalar Mexico NPV. Build scenario cells: education_bucket × state × descendant_band × Saiz quartile. Which NAS cells assume national average destination when ACS weights imply inelastic-state concentration for <HS vs H-1B/high-skill buckets?
   253	
   254	**Retrodiction:** Would have blocked pooling Mexico <HS surge cells with national rent average; CA/NY/TX gateway elasticity Q1 dominates origin_puma weights for multiple groups.
   255	
   256	**Negative space:** Lifetime benchmarks in npv_education_benchmarks have no destination elasticity dimension — housing incidence silently averaged out.
   257	
   258	---
   259	
   260	## F_high_skill
   261	
   262	### G-LIF-F01 — H-1B bucket ≠ Mexico <HS NAS cell
   263	
   264	**Prompt:** Split lifetime fiscal scenarios by admission channel: H-1B/STEM high-skill (Bound-Khanna) vs <HS unauthorized/surge (Hanson/CBO). Where does any memo pool them into one 'immigrant NPV'? Map H-1B to separate education_bucket with innovation/firm-profit offsets not in NAS Table 8-12.
   265	
   266	**Retrodiction:** Would have blocked scalar Mexico verdict from absorbing H-1B federal-positive innovation path; CS wage −2.6–5.1% distributional fork explicit.
   267	
   268	**Negative space:** NAS education cells conflate arrival credential with visa/channel-specific fiscal and labor dynamics.
   269	
   270	### G-LIF-F02 — Partial vs general equilibrium wage claims
   271	
   272	**Prompt:** Tag each wage study as partial (same education cell competition) or GE (capital adjustment + cross-education complementarity). Ottaviano-Peri: σ≈0.13–0.21 → +1.8% avg native vs Borjas −3% partial. Bound-Khanna: CS harmed, non-college +0.44% utility. Which fiscal memos cite partial elasticities as lifetime verdict?
   273	
   274	**Retrodiction:** Would have flagged Borjas-style −8% <HS partial estimates incompatible with O-P −2.2% short run when occupational differentiation allowed.
   275	
   276	**Negative space:** Lifetime fiscal synthesis cites wage losses without GE capital/complementarity or occupational reallocation.
   277	
   278	### G-LIF-F03 — Occupational mobility vs education-at-arrival bucket
   279	
   280	**Prompt:** Use Chiswick DP452 U-shaped ANU3 path: pre-migration prestige → arrival downgrade → partial recovery. Does NAS/education_bucket treat sheepskin at arrival as permanent skill proxy? Cross to Ottaviano-Peri occupational congruence 0.6–0.7. High-skilled visa (Business/Humanitarian) vs tied-migrant steepness.
   281	
   282	**Retrodiction:** Would have warned that professionals arriving at 67.96 ANU3 score first job at 55.78 — lifetime NPV keyed on education alone misses assimilation dynamics and descendant occupational path.
   283	
   284	**Negative space:** Descendant band in scenario ledger has earnings projection but no occupational downgrade/recovery state.
   285	
   286	### G-LIF-F04 — Innovation spillover vs substitute crowd-out (H-1B)
   287	
   288	**Prompt:** Decompose Bound-Khanna counterfactual: β≈0.23 innovation spillover raises aggregate native utility to ~0.21% vs 0.02–0.03% without; IT profits +0.61–0.70%; CS stayers −5.13% utility. Which lifetime studies count patent/innovation fiscal externality? Separate firm-owner surplus from worker incidence.
   289	
   290	**Retrodiction:** Would have surfaced that killing spillovers collapses H-1B welfare case — fiscal ledger needs explicit innovation row or H-1B bucket stays incomplete.
   291	
   292	**Negative space:** Federal positive NPV for college+ often assumes static payroll tax without IT sector profit/innovation feedback or CS distributional loss.
   293	
   294	### G-LIF-F05 — State × education_bucket high-skill destination sorting
   295	
   296	**Prompt:** Map H-1B/STEM concentration (CA/WA/NY/TX) vs <HS surge states. Ottaviano-Peri: 90% of natives have ≥HS and gain 0.7–3.4%. Bound-Khanna: non-college natives gain +0.44% utility from H-1B era GE. Build state×education_bucket×descendants cells — refuse national scalar.
   297	
   298	**Retrodiction:** Would have prevented applying Mexico <HS state-local shock ledger to H-1B-heavy states where federal payroll and innovation channels dominate.
   299	
   300	**Negative space:** State fiscal capacity literature (BoC Presidio) rarely splits high-skill tech hubs from border <HS counties within same state.
   301	
   302	---
   303	
   304	## G_legal_status_tax
   305	
   306	### G-LIF-G01 — Tax-floor vs benefit-ban ledger split
   307	
   308	**Prompt:** For any undocumented/refugee fiscal cell, decompose annual flows into (a) taxes paid regardless of status — payroll, sales, property pass-through, ITIN income tax — and (b) benefits legally barred. ITEP shows 35% of taxes fund SS/Medicare/UI with exclusion from benefits. Do not net to zero without explicit benefit-access matrix.
   309	
   310	**Retrodiction:** Would have separated ITEP $96.7B tax floor from NAS benefit-cost rows before treating unauthorized as net-negative by default.
   311	
   312	**Negative space:** Single net fiscal scalar assuming undocumented immigrants receive Medicaid/SNAP at citizen rates.
   313	
   314	### G-LIF-G02 — Legal-status stock reconciler
   315	
   316	**Prompt:** Before lifetime NPV, reconcile population stocks: Pew residual (14M 2023, upward undercount adjustment) vs ITEP/Warren (10.9M 2022) vs temp-protection subgroups (6M). Map each stock to work-authorization, ITIN filing, and benefit-eligibility states. Flag when model uses one stock for taxes and another for costs.
   317	
   318	**Retrodiction:** Would have caught 2.5M headcount mismatch and 40% temp-protection heterogeneity before applying scalar Mexico undocumented parameters.
   319	
   320	**Negative space:** Single undocumented count from one source year applied to all fiscal lines.
   321	
   322	### G-LIF-G03 — ITIN compliance sensitivity band
   323	
   324	**Prompt:** Treat federal income tax contribution rate as explicit sensitivity: ITEP base 60% (50–75% literature), json pessimistic −10.6% / optimistic +15.5% on grand total. Require any lifetime undocumented cell to show tax floor under {50%, 60%, 75%} before point estimate.
   325	
   326	**Retrodiction:** Would have surfaced ITEP advocacy-adjacent microsim and CBO 50–75% band before locking undocumented federal income proxy.
   327	
   328	**Negative space:** 100% compliance or 0% undocumented income tax as unstated extremes.
   329	
   330	### G-LIF-G04 — Border-selection earnings updater
   331	
   332	**Prompt:** When calibrating Mexico-origin lifetime cells, ask whether border-enforcement era shifted immigrant selection (Lozano-López: fewer older/high-ed women, higher earnings among survivors). Compare pre-2000 vs post-2000 arrival cohorts; do not use pooled Mexico <HS wage path for recent-surge entrants without selection flag.
   333	
   334	**Retrodiction:** Would have linked IZA dp4898 positive selection channel to Mexico earnings donor cells before assuming uniform undocumented wage floor.
   335	
   336	**Negative space:** Random emigration from Mexican wage distribution (no gender/cost selection).
   337	
   338	### G-LIF-G05 — Tenure-split forward stock
   339	
   340	**Prompt:** Pew 2023: 3.2M unauthorized <5 years vs 4.3M 18+ years. Split lifetime NPV into forward stock (short tenure, high flow uncertainty, temp protection) vs established stock (ITEP 16+ year median). Apply different discount horizons and legalization uplift ($40.2B/yr scenario) by tenure bucket.
   341	
   342	**Retrodiction:** Would have prevented applying established-immigrant tax parameters to 2021–2023 parole-heavy inflow before forward-stock analysis.
   343	
   344	**Negative space:** Steady-state unauthorized population with homogeneous tenure.
   345	
   346	---
   347	
   348	## H_refugee_mortality
   349	
   350	### G-LIF-H01 — Refugee employment ramp calibrator
   351	
   352	**Prompt:** For humanitarian/refugee lifetime cells, impose employment ramp from Dustmann et al.: −50pp year 0–3, −16pp unconditional steady-state gap, convergence ~15–25 years. Do not use economic-migrant employment rates in arrival year. Pair with Clemens 8-year U.S. fiscal breakeven as cross-check.
   353	
   354	**Retrodiction:** Would have blocked flat employment assumption for parole/asylum entrants before forward-stock NPV.
   355	
   356	**Negative space:** Refugees enter at native-average employment and earnings in year 1.
   357	
   358	### G-LIF-H02 — Mortality forward-stock multiplier
   359	
   360	**Prompt:** When projecting SS/Medicare NPV for Hispanic/refugee cells, require explicit life-table anchor: CDC 2021 Hispanic e₀=77.8, e₂₅=53.8, e₆₅=19.3 vs total-pop 76.4. Flag use of White NH or generic SSA tables without Hispanic adjustment. Note Medicare imputation uncertainty for Hispanic old-age mortality.
   361	
   362	**Retrodiction:** Would have surfaced +1.4yr Hispanic e₀ vs total before applying uniform 75-year NAS horizon to Latin American humanitarian entrants.
   363	
   364	**Negative space:** Single life table for all immigrant origins in lifetime model.
   365	
   366	### G-LIF-H03 — Permanence vs subsidiary protection fork
   367	
   368	**Prompt:** Dustmann: full GCR asylum → permanent settlement vs subsidiary/temporary protection → return incentive → lower host-country human-capital investment. For U.S. parole/TPS/asylum pending, branch lifetime NPV into {permanent, temporary, rejected} with different education/employment investment paths. EU ~10% recognition rate is lower-bound permanence probability.
   369	
   370	**Retrodiction:** Would have split Pew 40% temp-protection subshare into permanence branches before scalar unauthorized NPV.
   371	
   372	**Negative space:** All humanitarian entrants eventually permanent with identical integration path.
   373	
   374	### G-LIF-H04 — Formal LMA breakeven clock
   375	
   376	**Prompt:** Clemens WP496: formal labor market access is lever once refugees already present — avg U.S. refugee net fiscal positive at 8 years; work-access timing shifts breakeven (Marbach). For each humanitarian cell, declare LMA state {banned yr0-3, informal, formal} and map to Evans-Fitzgerald clock.
   377	
   378	**Retrodiction:** Would have paired Clemens 8-year breakeven with Dustmann 50pp yr-3 employment ban before assuming humanitarian entrants are permanent fiscal negatives.
   379	
   380	**Negative space:** Work authorization irrelevant to refugee fiscal path.
   381	
   382	### G-LIF-H05 — Origin-area employment penalty mapper
   383	
   384	**Prompt:** Dustmann Figure 9: MENA refugees −32.5pp conditional employment vs natives; other Africa/Asia also elevated. When modeling Syrian/Afghan/Venezuelan humanitarian cells, do not use Mexico <HS employment defaults — apply origin-area penalty decay schedule from EU evidence.
   385	
   386	**Retrodiction:** Would have differentiated MENA humanitarian employment penalty from Mexico economic-migrant path in lifetime ledger.
   387	
   388	**Negative space:** All humanitarian entrants share one employment gap regardless of origin.
   389	
   390	---
   391	
   392	## I_return_migration
   393	
   394	### G-LIF-I01 — Inverse entry-earnings / assimilation growth band
   395	
   396	**Prompt:** For each origin×education_bucket in origin_fiscal_scenario_2023, attach Duleep-Regets inverse elasticity band: unweighted -5.8 pp / weighted -9.7 pp / LDC +28.9 pp per $1,000 lower entry earnings (dp631 Table 1-3). Refuse cross-sectional assimilation slope as lifetime earnings path. Pair low entry with high growth before NAS NPV sign call.
   397	
   398	**Retrodiction:** Would have blocked Borjas-style 'slow assimilation' from low entry earnings alone AND Clemens/NAS positive paths that assume flat growth across cohorts — dp631 resolves Chiswick-Borjas contradiction via inverse relationship.
   399	
   400	**Negative space:** Lifetime fiscal models use entry earnings or a single YSM coefficient; no paired {entry level, entry-specific growth} cell.
   401	
   402	### G-LIF-I02 — Country-of-origin convergence decay on scenario ledger
   403	
   404	**Prompt:** Map dp8628 R² and CV convergence (country-origin explanatory power falls 22-91% over 10 years; cross-origin CV -13 to -55%) onto origin_fiscal_scenario rows. Flag origins where year-0 fiscal heterogeneity (avg_federal_net spread) is assumed permanent. Weight Mexico by convergence-adjusted earnings path, not entry-only snapshot.
   405	
   406	**Retrodiction:** Would have surfaced that ACS 2023 origin weights × static avg_federal_net overstate Mexico-vs-Europe fiscal gap at year 10+ residence before any return-migration adjustment.
   407	
   408	**Negative space:** Origin label treated as permanent fiscal modifier; no time-in-US decay of country-of-origin earnings premium.
   409	
   410	### G-LIF-I03 — Return-migration / emigration selection sensitivity grid
   411	
   412	**Prompt:** Build 3×3 attrition grid on lifetime NPV horizon: {low, base, high exit rate} × {failure-selective, random, success-selective outflow} × {years 0-5, 5-15, 15+ exit windows}. Anchor base rate: Warren-Kraly 75% emigrants in first 5 years; dp631 high/low emigration cohorts show similar inverse growth (emigration does not kill assimilation signal). No US fiscal micro — manual band only until CHCP acquired.
   413	
   414	**Retrodiction:** Would have flagged G-LIF-D02 CHCP blocked gap and Dustmann survey §5.9 before treating SIPP annual proxy × 75-year horizon as full residence.
   415	
   416	**Negative space:** Immigrant remains until death; selective return migration absent from NAS/Storesletten generational accounting.
   417	
   418	### G-LIF-I04 — Skill-transferability vs immigrant-quality trap audit
   419	
   420	**Prompt:** Audit lifetime memos equating low entry earnings with low 'immigrant quality' (Borjas cohort-quality frame). Cross-read dp631: entry earnings are poor human-capital stock measure when transferability τM<1 drives investment; dp8628: post-1965 LDC composition + family-reunification chain (Korean 75%→44% native parity) explains entry decline with rising growth. Separate {transferability, investment rate, exit hazard} before education_bucket NPV assignment.
   421	
   422	**Retrodiction:** Would have prevented Mexico <HS scalar from inheriting 'declining immigrant quality' narrative while ignoring IHCI fast-growth offset and IRC A Mexican cohort selection exception.
   423	
   424	**Negative space:** Single 'quality' dimension collapses transferability, ability, and selective return into entry wage.
   425	
   426	### G-LIF-I05 — Cohort-dummy assimilation methodology falsifier
   427	
   428	**Prompt:** For any pooled YSM regression or NAS cell using average assimilation rate: simulate dp8628 bias — recent low-entry cohorts get underestimated growth, high-entry cohorts overestimated when cohort dummies constrain growth. Require separate year-of-entry cohort paths or explicit inverse entry×growth interaction before lifetime NPV aggregation on acs_foreign_born_education_bucket_totals weights.
   429	
   430	**Retrodiction:** Would have caught standard dummy-cohort assimilation estimates that dp631/dp8628 prove invalid when entry earnings trend down — directly relevant to building lifetime evidence warehouse assimilation parameters.
   431	
   432	**Negative space:** Pooled assimilation coefficient applied to all entry cohorts regardless of entry-earnings level.
   433	
   434	---
   435	
   436	## J_admin_enforcement
   437	
   438	### G-LIF-J01 — Enforcement budget ≠ per-migrant fiscal cost
   439	
   440	**Prompt:** For each CBP/ICE appropriation line, tag as (a) fixed agency overhead, (b) volume-linked (encounters/beds/removals), (c) non-immigration mission (HSI fentanyl, trade). Never divide total CBP $19.8B or ICE $9.7B by immigrant stock without an explicit allocation rule. Cross-check to NAS/CBO lifetime tables that omit enforcement entirely.
   441	
   442	**Retrodiction:** Would have blocked treating DHS budget growth as direct per-capita immigrant lifetime cost and surfaced NAS enforcement omission.
   443	
   444	**Negative space:** Advocacy and restrictionist frames both treat agency budget as immigrant line-item without encounter/bed denominator.
   445	
   446	### G-LIF-J02 — Recidivism-inflated flow vs unique-person stock
   447	
   448	**Prompt:** Separate CBP apprehension/encounter counts (2.15M interdicted; 2.81 avg per recidivist) from unique-subject stock (1.42M) and from Pew/DHS unauthorized LPR residual. Where do lifetime models use flow denominators on stock numerators?
   449	
   450	**Retrodiction:** Would have flagged repeat-encounter inflation before calibrating per-apprehension detention cost or fiscal scalars.
   451	
   452	**Negative space:** Headline apprehension totals treated as unduplicated immigrant arrivals in media and some fiscal shorthand.
   453	
   454	### G-LIF-J03 — Detention bed-day cost bridge
   455	
   456	**Prompt:** Build marginal detention cost from ICE custody PPA ($3.27B FY25) ÷ ADP × 365 vs published bed rate ($187.48/day FY23). Compare to Alternatives to Detention ($360M FY25) and transportation/removal surge (+54% YoY). Which NAS/CBO lifetime paths include interior detention?
   457	
   458	**Retrodiction:** Would have quantified interior custody as episodic federal cost absent from state-local K-12/shelter ledgers and NAS education NPV cells.
   459	
   460	**Negative space:** Lifetime NPV studies silent on ICE bed-days while local shock ledgers silent on federal detention.
   461	
   462	### G-LIF-J04 — LPR admission-class fiscal path decomposition
   463	
   464	**Prompt:** For Mexico and top surge origins (Cuba, Venezuela, Haiti), sum LPR totals by admission class (immediate relative, family preference, employment, diversity). Map family-heavy paths to descendant-inclusive NAS rows vs employment paths to high-skill positive cells. Track Fam 2nd Mexico collapse 2005→2022 as legalization-channel shift under visa caps.
   465	
   466	**Retrodiction:** Would have prevented treating Mexico as monolithic <HS unauthorized cell when 2022 LPR flow is 83k+ immediate-relative dominated.
   467	
   468	**Negative space:** Origin labels in ACS fiscal scenarios collapse legal-status and admission-class heterogeneity.
   469	
   470	### G-LIF-J05 — Border enforcement selection interacts with LPR mix
   471	
   472	**Prompt:** Joint read: CBP interdiction rate + ICE ADP growth + Lozano-López border-enforcement selection (Round 9) + Mexico LPR class mix. Does rising interior detention correlate with positive earnings selection on observables while LPR family backlog lengthens?
   473	
   474	**Retrodiction:** Would have linked Round 9 IZA dp4898 selection story to admin budget shift border→interior and LPR Fam2 collapse.
   475	
   476	**Negative space:** Enforcement papers treat selection; budget docs treat dollars; LPR tables treat legal paths — rarely joint.
   477	
   478	---
   479	
   480	## K_incidence_bridge
   481	
   482	### G-LIF-K01 — County incidence join audit
   483	
   484	**Prompt:** For each origin in `origin_fiscal_scenario_2023`, trace PUMA→county via `puma_county_area_xwalk_2023` and join `school_finance_county_2023` + `chas_county_housing_stress`. Confirm `area_wtd_current_spend_per_pupil` is in the expected ~$8k–$30k band after the F-33 thousands fix, then bridge per-pupil to per-adult with full microsim adult denominators rather than the scenario subset.
   485	
   486	**Retrodiction:** Would have caught both school spend ~$21 unit anomaly and the later Mexico denominator error (~437k scenario adults vs ~8.5M microsim adults) before using the local layer in a per-adult conclusion.
   487	
   488	**Negative space:** National NAS education cost vs county-weighted ACS incidence
   489	
   490	### G-LIF-K02 — Receiver-node episodic ledger
   491	
   492	**Prompt:** Sum receiver_city_migrant_costs by node; compare to federal avg_federal_net for Mexico <HS in origin_fiscal_scenario. Build explicit episodic shock line (shelter/admin) outside 75-year NPV horizon.
   493	
   494	**Retrodiction:** Would have separated Gould w33655 asylum shelter shock from Hanson composition weights.
   495	
   496	**Negative space:** Lifetime NPV treats all fiscal incidence as smooth annual flows
   497	
   498	### G-LIF-K03 — IRS migration × immigrant stock falsifier
   499	
   500	**Prompt:** Join irs_migration_county_2022_2023 net inflow to ACS origin_puma stock changes. Does tax-base mobility co-move with immigrant share increases? If not, IRS migration is a weak falsifier for fiscal attribution.
   501	
   502	**Retrodiction:** Would have flagged IRS county migration as income mobility not immigrant-specific fiscal shock.
   503	
   504	**Negative space:** Tax return address change = immigrant fiscal burden
   505	
   506	### G-LIF-K04 — State stage5 heterogeneity band
   507	
   508	**Prompt:** From state_stage5_context_2023, build state_fips × education_bucket fiscal capacity quartiles (RPP, Medicaid, EL). Mexico composition weights × state shares should produce state-level lifetime bands, not one national scalar.
   509	
   510	**Retrodiction:** Would have blocked national Mexico NPV scalar before stage5 context existed.
   511	
   512	**Negative space:** National average fiscal incidence
   513	
   514	---
   515	
   516	## L_oecd_health_bridge
   517	
   518	### G-LIF-L01 — Push-flow vs pull-fiscal attribution split
   519	
   520	**Prompt:** For every lifetime fiscal claim citing 'immigration increases GDP/jobs': tag whether evidence is Ortega-Peri-style push-IV macro (scale, flat per-capita) or NAS/CBO micro ledger (education × transfers). Block synthesis that imports macro 1:1 employment response into individual NPV cells without capital-tax and public-goods grid.
   521	
   522	**Retrodiction:** Would have separated Ortega-Peri Table 5 ΔL/L≈1 from NAS -$109k <HS before debate conflated 'immigrants grow GDP' with 'immigrants are net fiscal drains'.
   523	
   524	**Negative space:** Standing frame: macro OECD panel = US lifetime fiscal scalar.
   525	
   526	### G-LIF-L02 — MEPS annual cell → lifetime health NPV harmonizer
   527	
   528	**Prompt:** Given meps_health_cost_module_2023 age×nativity×insurance cells: (1) map SIPP arrival age to age-band path; (2) apply survival/ Medicare eligibility; (3) discount at NAS 3% real over 75yr; (4) split payer columns (MCR/MCD/PRV/SLF). Never cite expected_mean_totexp23 as lifetime cost without horizon tag.
   529	
   530	**Retrodiction:** Would have flagged scenario-composition memo disconfirmation #2 (FB working-age lower) AND elderly Medicaid reversal (L-009) before treating $600/yr bridge as −$109k NPV health line.
   531	
   532	**Negative space:** Annual cross-section MEPS mean = lifetime immigrant health fiscal externality.
   533	
   534	### G-LIF-L03 — Employer-recruitment channel vs stock composition
   535	
   536	**Prompt:** When Winkelmann-style employer demand shows complementarity (languages, know-how; not wage undercutting), require separate high-skill recruited bucket in scenario ledger — do not pool with ACS stock <HS Mexico weights. Cross-check: firms with ≥1000 employees +32pp FHQE probability vs economy-wide 3.5% FHQE share.
   537	
   538	**Retrodiction:** Would have blocked mapping IZA employer survey (IT/R&D 50-68% firm incidence) onto NAS average-recent-immigrant +$259k without education×visa path.
   539	
   540	**Negative space:** All immigrants modeled as undifferentiated labor supply shock.
   541	
   542	### G-LIF-L04 — Lifecycle Medicaid phase-shift audit
   543	
   544	**Prompt:** Compare MEPS mean_totmcd23 by age_band for foreign_born vs us_born. Identify crossover age where fiscal sign flips. For lifetime NPV: stress-test with (a) working-age-only horizon to 65, (b) full 75yr with elderly weights, (c) uninsured→Medicaid transition scenarios. Flag any headline using only 25-44 cells.
   545	
   546	**Retrodiction:** Would have surfaced L-007 (−42% working-age totexp) AND L-009 (+252% elderly Medicaid) as mandatory paired disconfirmation before Medicaid-drain advocacy.
   547	
   548	**Negative space:** Health fiscal sign from single working-age snapshot.
   549	
   550	### G-LIF-L05 — OECD policy-shock × health-bridge scenario grid
   551	
   552	**Prompt:** Cross Ortega-Peri entry-law elasticity (−6%/reform) with SIPP scenario_ledger health columns. For each policy counterfactual (tighter entry, income-gap shock): re-weight origin cells AND recompute expected_mean_totmcd23 — immigration policy and health incidence treated as joint state, not independent scalars.
   553	
   554	**Retrodiction:** Would have connected OECD law-reform flow shifts to which SIPP nativity/education cells enter the ledger, instead of static 98-cell health attach.
   555	
   556	**Negative space:** Immigration policy affects counts only; payer incidence held fixed at 2023 MEPS.
   557	
   558	---
   559	
   560	## M_annual_npv_bridge
   561	
   562	### G-LIF-M01 — Annual→NPV bridge with scope lock
   563	
   564	**Prompt:** For cell {education_bucket, origin_label}: (1) pull avg_federal_net from origin_fiscal_scenario_2023; (2) pull NAS individual_npv for same education cell; (3) annuitize NPV at {2%,3%,4%} over 75y; (4) label MATCH/MISMATCH and list which costs are in NAS but not SIPP. Block synthesis if scopes differ.
   565	
   566	**Retrodiction:** Would have blocked equating Mexico +$1,519/yr with NAS −$109k; flagged Lee-Miller dynamic vs cross-section mismatch.
   567	
   568	**Negative space:** One annual proxy confirms or refutes lifetime NPV.
   569	
   570	### G-LIF-M02 — Remittance private-layer offset
   571	
   572	**Prompt:** Join World Bank remittance series to both (a) `origin_fiscal_scenario_2023` scenario-subset adults and (b) full `mexico_origin` microsim adults. Compare remittance per adult to `avg_federal_net` only after labeling the denominator.
   573	
   574	**Retrodiction:** Mexico ~$66B remittances vs ~$664M scenario-subset federal net, or vs ~$12.9B full-stock federal net, before treating federal layer as household budget.
   575	
   576	**Negative space:** Public fiscal ledger = complete household accounting.
   577	
   578	### G-LIF-M03 — PAYG pension phase shift
   579	
   580	**Prompt:** Map immigrant taxes vs benefits by age (Abel/Lee-Miller). Test if annual federal+ is lifecycle phase not lifetime verdict.
   581	
   582	**Retrodiction:** Explains NAS school-age cost vs adult tax timing before working-age cross-section cited as lifetime proof.
   583	
   584	**Negative space:** Lifetime NPV collapsed into current working-age cash flow.
   585	
   586	### G-LIF-M04 — Policy-adjustment convention audit
   587	
   588	**Prompt:** Extract whether generational-accounting PV requires future tax hikes for debt stabilization. Recompute under no-policy-change.
   589	
   590	**Retrodiction:** Lee-Miller/NRC +$80k PV policy-adjustment reliance before citing generational surplus.
   591	
   592	**Negative space:** Generational accounting as objective balance sheet.
   593	
   594	### G-LIF-M05 — Surge cohort vs stock annualization
   595	
   596	**Prompt:** Tag CBO surge federal path vs steady-state SIPP Mexico proxy SURGE vs STOCK. Forbid surge gains as lifetime NPV for 1990s stock.
   597	
   598	**Retrodiction:** CBO $897B deficit reduction separated from Mexico ACS weights before layer laundering.
   599	
   600	**Negative space:** One wave's federal gains applied to all stocks.
   601	
   602	---
   603	
   604	## N_school_unit_harmonization
   605	
   606	### G-LIF-N01 — F-33 thousands gate
   607	
   608	**Prompt:** Verify spend/enroll ratio is $8k–$30k/pupil; if median < $500 multiply expenditures by 1000.
   609	
   610	**Retrodiction:** Caught ~$21 per-pupil bug before local K-12 lifetime assignment.
   611	
   612	**Negative space:** Derived CSVs without unit sanity band.
   613	
   614	### G-LIF-N02 — County vs origin per-pupil join audit
   615	
   616	**Prompt:** CORR(county per_pupil, origin area_wtd per_pupil) after PUMA join; flag r<0.3.
   617	
   618	**Retrodiction:** Failed pre-fix correlation; passes post-fix ~$20k band.
   619	
   620	**Negative space:** Origin school cost without county anchor.
   621	
   622	### G-LIF-N03 — K-12 lifetime cost band
   623	
   624	**Prompt:** per_pupil × 13 years × school_age_share vs NAS education cost component.
   625	
   626	**Retrodiction:** Pre-fix K-12 cost ~1000× too low to enter any local sum.
   627	
   628	**Negative space:** School costs omitted because proxy numerically negligible (bug).
   629	
   630	### G-LIF-N04 — NCES digest triangulation
   631	
   632	**Prompt:** NCES 236.20 national per-pupil vs county F-33 weighted mean; reject if ratio outside [0.7,1.3] without RPP.
   633	
   634	**Retrodiction:** ~$19k county median triangulated against NCES after unit fix.
   635	
   636	**Negative space:** Single derived table without external scalar check.
   637	
   638	---
   639	
   640	## O_welfare_political
   641	
   642	### G-LIF-O01 — Federal vs state-local ledger split enforcer
   643	
   644	**Prompt:** Tag FEDERAL (CBO 60569) vs STATE_LOCAL (61256) vs LIFETIME_NPV (NAS). Reject unlike-ledger sums.
   645	
   646	**Retrodiction:** Blocked federal $897B surplus dismissing NYC shelter + state/local $9.2B.
   647	
   648	**Negative space:** One government budget.
   649	
   650	### G-LIF-O02 — Welfare magnet destination sort
   651	
   652	**Prompt:** Rank states by Medicaid per capita × immigrant PUMA weights; test magnet sort.
   653	
   654	**Retrodiction:** Razin magnet theory linked to stage5 Medicaid heterogeneity before fiscal sign treated as immigrant-fixed.
   655	
   656	**Negative space:** Fiscal type independent of destination policy.
   657	
   658	### G-LIF-O03 — Tax-paid floor without benefit ceiling
   659	
   660	**Prompt:** Pair ITEP taxes with SIPP transfer proxy for same legal-status band.
   661	
   662	**Retrodiction:** Blocked $96.7B taxes rhetoric without transfer_outflow pairing.
   663	
   664	**Negative space:** Tax contributions as net fiscal verdict.
   665	
   666	### G-LIF-O04 — Political equilibrium skill-mix shift
   667	
   668	**Prompt:** Map Razin voter blocs to DHS LPR class mix — family vs employment predicts education shift?
   669	
   670	**Retrodiction:** Legal-path mix linked to education composition via political economy before static NAS weights.
   671	
   672	**Negative space:** Skill mix exogenous to US policy.
   673	
   674	---
   675	
   676	## P_restriction_admin
   677	
   678	### G-LIF-P01 — Enforcement admin ledger
   679	
   680	**Prompt:** Sum CBP+ICE budgets per unauthorized (Pew stock); compare to ITEP tax per unauthorized.
   681	
   682	**Retrodiction:** Missing admin ℓ layer before restriction advocacy used only NAS negatives.
   683	
   684	**Negative space:** Restriction costless aside from lost immigrant surplus.
   685	
   686	### G-LIF-P02 — Receiver episodic vs federal annual dominance
   687	
   688	**Prompt:** N × avg_federal_net vs sum(receiver_city spending FY2023-24) for surge scale N.
   689	
   690	**Retrodiction:** NYC+Chicago episodic rivals federal proxy for surge narrative.
   691	
   692	**Negative space:** Federal surplus settles city shelter.
   693	
   694	### G-LIF-P03 — Restriction changes cell not scalar
   695	
   696	**Prompt:** 20% cut in `<HS` weight vs 20% cut in employment LPR — re-weight NAS cells.
   697	
   698	**Retrodiction:** Enforcement selection + LPR mix before count-only restriction debate.
   699	
   700	**Negative space:** Restriction = fewer identical immigrants.
   701	
   702	### G-LIF-P04 — CBO restriction macro offset
   703	
   704	**Prompt:** Invert CBO 60569 GDP/revenue channels for restriction sketch — federal cost of lost workers vs local savings.
   705	
   706	**Retrodiction:** Federal GDP/revenue loss required in restriction debates citing only local shelter savings.
   707	
   708	**Negative space:** Local relief from restriction has no federal offset cost.
   709	
   710	---
   711	
   712	## Q_stock_flow_denominator
   713	
   714	### G-LIF-Q01 — Encounter ≠ stock
   715	
   716	**Prompt:** Before any fiscal per-capita from border data: separate CBP encounter events, IDENT unique subjects, gotaways, and Pew/CIS unauthorized stock. Flag when flow denominators hit stock numerators.
   717	
   718	**Retrodiction:** Would have blocked "10M illegals since Biden" → lifetime NPV without dedupe and outflow ledger.
   719	
   720	**Negative space:** Encounter count treated as net new US residents.
   721	
   722	### G-LIF-Q02 — Gotaway additive trap
   723	
   724	**Prompt:** Gotaway sensitivity: add detected gotaways to stock only after subtracting repeat crossers, later apprehensions, and outflows. Never sum gotaways + encounters + Pew stock.
   725	
   726	**Retrodiction:** Would have prevented double-counting ~2M gotaways on top of 14M Pew stock.
   727	
   728	**Negative space:** Gotaways as permanent additive residents.
   729	
   730	### G-LIF-Q03 — Birthplace ≠ legal status
   731	
   732	**Prompt:** Map ACS birthplace (POBP) → Pew residual legal-status subcounts by origin before labeling "illegal Mexican" fiscal impact.
   733	
   734	**Retrodiction:** Would have separated 8.5M Mexico-born adults from 4.3M Mexico-unauthorized stock.
   735	
   736	**Negative space:** `origin_label=Mexico` equals unauthorized pool.
   737	
   738	### G-LIF-Q04 — Education-mix mean ≠ median cell
   739	
   740	**Prompt:** Any population-weighted NAS NPV scalar must ship with education-bucket share table; report `<HS` cell alongside weighted mean.
   741	
   742	**Retrodiction:** Would have blocked "+$46k per Mexican" without 47% `<HS` at −$109k disclosure.
   743	
   744	**Negative space:** Single lifetime scalar for heterogeneous education mix.
   745	
   746	### G-LIF-Q05 — Pew vs CIS stock band
   747	
   748	**Prompt:** Stock band sensitivity: Pew 14M vs CIS 15.8M unauthorized; apply Mexico ~30% share only to unauthorized-layer lines, not NAS education-mix rows.
   749	
   750	**Retrodiction:** Would have bounded undercount debate to ~1–2M national band instead of +10M.
   751	
   752	**Negative space:** One advocacy stock count applied to all fiscal layers.
   753	
   754	### G-LIF-Q06 — Age-25 NPV benchmark ≠ current-stock NPV
   755	
   756	**Prompt:** Before multiplying NAS Table 8-13 cells by ACS stock weights, verify whether the claim is about an immigrant entering at age 25, a recent-arrival cohort, or the current age-25–64 stock. If the warehouse lacks age-at-arrival/current-age NPV paths, label the result `synthetic_age25_benchmark`, not lifetime NPV of the stock.
   757	
   758	**Retrodiction:** Would have blocked reading Mexico `+$387.7B` as actual stock lifetime NPV when the tensor only applies NAS age-25 cells to current ACS education weights.
   759	
   760	**Negative space:** Current-stock population count treated as a cohort of new age-25 entrants.
   761	
   762	---
   763	
   764	## R_full_ledger_stack
   765	
   766	### G-LIF-R01 — NAS scope lock before net claim
   767	
   768	**Prompt:** Before citing any NAS NPV scalar: list {in: federal, state/local in cell, descendants, public goods, enforcement, courts, episodic shelter}. Block "net contributor" language until missing ℓ layers tagged.
   769	
   770	**Retrodiction:** Would have blocked +$46k Mexico headline without stating descendants excluded and ICE/EOIR absent.
   771	
   772	**Negative space:** NAS individual NPV treated as all-government lifetime net.
   773	
   774	### G-LIF-R02 — School double-count guard
   775	
   776	**Prompt:** Cross-check NAS cell (individual, no descendants) vs `school_burden_per_adult`. If NAS excludes kids' K-12, add school layer; if NAS includes immigrant own education only, do not subtract cross-section school twice.
   777	
   778	**Retrodiction:** Would have separated individual NAS path from current-HH school burden ($771/yr) before merging layers.
   779	
   780	**Negative space:** Subtract school on top of NAS without checking descendant booking.
   781	
   782	### G-LIF-R03 — Admin enforcement allocation rule
   783	
   784	**Prompt:** Allocate CBP+ICE only via explicit rule: {per encounter, per bed-day, per unauthorized stock, fixed national}. Never divide total budget by stock without tagging fixed vs marginal share.
   785	
   786	**Retrodiction:** Would have flagged $29.5B / 14M ≈ $2.1k/yr enforcement line missing from lifetime NPV.
   787	
   788	**Negative space:** Full agency budget attributed to average immigrant.
   789	
   790	### G-LIF-R04 — Justice/court layer
   791	
   792	**Prompt:** Join EOIR case load × nationality to origin cells; express $/case or $/adult for asylum/backlog cohorts. Separate from NAS criminal-justice paths.
   793	
   794	**Retrodiction:** Would have surfaced staged EOIR data with no Mexico rollup before claiming fiscal closure.
   795	
   796	**Negative space:** Court costs assumed zero or inside NAS education cell.
   797	
   798	### G-LIF-R05 — Publish stacked object only
   799	
   800	**Prompt:** Export `v_full_fiscal_stack` with columns per ℓ and explicit overlap matrix. Headline = vector, never scalar.
   801	
   802	**Retrodiction:** Would have required three-layer annual + lifetime + admin before any "Mexico net" thesis.
   803	
   804	**Negative space:** Single number politics.
   805	
   806	---
   807	
   808	## S_restrictionist_steelman
   809	
   810	### G-LIF-S01 — Restrictionist ledger tagger
   811	
   812	**Prompt:** For each restrictionist claim, extract {ledger, cell, cohort, layer} before agreeing/disagreeing.
   813	
   814	**Retrodiction:** Would have separated FAIR $150B (advocacy full ℓ) from NAS `<HS` (academic lifetime ℓ) from Gould 60% (episodic local).
   815	
   816	**Negative space:** Restrictionist scalar applied to all immigrants.
   817	
   818	### G-LIF-S02 — Subgroup row requirement
   819	
   820	**Prompt:** Map BGH black employment/incarceration results to required tensor rows — block education-only NAS for distributional harm claims.
   821	
   822	**Retrodiction:** Would have blocked inferring all native harm from immigrant `<HS` NPV alone.
   823	
   824	**Negative space:** Distributional politics from education-average cells.
   825	
   826	### G-LIF-S03 — FAIR vs ITEP vs Pew reconciliation
   827	
   828	**Prompt:** Build stock and tax reconciliation before citing FAIR or ITEP in warehouse scalars.
   829	
   830	**Retrodiction:** Would have flagged FAIR 15.5M stock vs Pew 14M before $8,776/per-capita.
   831	
   832	**Negative space:** Advocacy ledger as empirical fact.
   833	
   834	### G-LIF-S04 — Episodic vs lifetime dominance
   835	
   836	**Prompt:** Gould shelter $ vs NAS lifetime for same surge cohort — which ℓ drives local political backlash?
   837	
   838	**Retrodiction:** Would have connected NYC $3.7B to restrictionist wins independent of Mexico +$46k mix.
   839	
   840	**Negative space:** Lifetime NAS settles shelter debate.
   841	
   842	### G-LIF-S05 — Razin policy co-evolution
   843	
   844	**Prompt:** How does welfare eligibility / magnet policy change fiscal sign of same ACS immigrant cell?
   845	
   846	**Retrodiction:** Would have modeled M5 political equilibrium before static NAS weights.
   847	
   848	**Negative space:** Fiscal type invariant to destination policy.
   849	
   850	### G-LIF-S06 — National cell before Card
   851	
   852	**Prompt:** Before citing Card spatial null, require national education×experience cell regression or document spatial attenuation factor (Borjas w9755: ~⅔ hidden).
   853	
   854	**Retrodiction:** Would have blocked Mariel → "immigration harmless" without w11610 migration offset.
   855	
   856	**Negative space:** MSA coefficient as sufficient statistic for national harm.
   857	
   858	### G-LIF-S07 — Wage decomposition triple
   859	
   860	**Prompt:** Decompose immigration wage impact into {log weekly, log annual, weeks worked} — does harm operate on intensive or extensive margin?
   861	
   862	**Retrodiction:** Would have surfaced w9755 10% supply → −4% weekly but −6.4% annual + −3.7pp weeks.
   863	
   864	**Negative space:** Weekly wage elasticity alone.
   865	
   866	### G-LIF-S08 — Native migration offset
   867	
   868	**Prompt:** For local labor-market immigration regressions, estimate native in/out-migration response; compare implied attenuation to Borjas w11610 40–60% band.
   869	
   870	**Retrodiction:** Would have explained Card-Borjas gap as equilibrium diffusion not zero effect.
   871	
   872	**Negative space:** Local wage coefficient = structural national elasticity.
   873	
   874	### G-LIF-S09 — Subgroup triple margin
   875	
   876	**Prompt:** For distributional harm claims, require {wage, employment, incarceration} rows — BGH shows black employment/incarceration elasticities >> white.
   877	
   878	**Retrodiction:** Would have blocked NAS `<HS` NPV → "harms all natives equally."
   879	
   880	**Negative space:** Education-average fiscal cell as subgroup harm proxy.
   881	
   882	### G-LIF-S10 — HUD PIT decomposition
   883	
   884	**Prompt:** Split homelessness into {sheltered asylum-attributable, sheltered other, unsheltered}; block Gould 60% → "all homelessness."
   885	
   886	**Retrodiction:** Would have separated NYC episodic shelter from lifetime Mexico NPV.
   887	
   888	**Negative space:** Affordability-only homelessness narrative.
   889	
   890	### G-LIF-S11 — Orrenius dual-scenario gate
   891	
   892	**Prompt:** Every NAS fiscal citation must show avg-cost AND marginal-cost rows plus federal/state split (Orrenius Table 1 pattern).
   893	
   894	**Retrodiction:** Would have blocked restrictionist use of avg-public-goods negative without marginal federal +$963.
   895	
   896	**Negative space:** Single NAS table cell in politics.
   897	
   898	### G-LIF-S12 — Razin policy vector shock
   899	
   900	**Prompt:** Simulate {τ, μ, σ} change on fiscal sign of fixed ACS immigrant cell (Razin w15597 Markov PE).
   901	
   902	**Retrodiction:** Would have linked welfare generosity to skill composition before static lifetime NPV.
   903	
   904	**Negative space:** Fiscal type invariant to immigration/welfare policy.
   905	
   906	### G-LIF-S13 — Mobility-regime tag
   907	
   908	**Prompt:** Welfare-magnet claims require {free vs restricted} mobility regime tag — EUR evidence does not transfer to US selective policy (Razin-Wahba w17515).
   909	
   910	**Retrodiction:** Would have blocked "Europe proves magnet" without regime control.
   911	
   912	**Negative space:** Cross-regime magnet inference.
   913	
   914	### G-LIF-S14 — Secular supply forecast
   915	
   916	**Prompt:** Pair Hanson w23753 secular low-skill decline + Pew stock series before "flooding" rhetoric; encounters ≠ residents.
   917	
   918	**Retrodiction:** Would have deflated Biden 10M encounter → stock panic against flat Mexico unauthorized.
   919	
   920	**Negative space:** Flow headline as permanent stock shock.
   921	
   922	### G-LIF-S15 — Intergenerational welfare channels
   923	
   924	**Prompt:** For intergenerational fiscal/welfare claims, separate {parental welfare receipt, ethnic environment externality, own earnings path} — Borjas w6175: ~80% of ethnic welfare gap transmits.
   925	
   926	**Retrodiction:** Would have blocked attributing second-gen costs to first-gen immigrant NPV alone.
   927	
   928	**Negative space:** Immigrant lifetime NPV = ethnic externality.
   929	
   930	---
--- END FILE: research/immigration-lifetime-fiscal-generators.md ---

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
    28	- E-Verify mandates show no statistically significant positive QWI wage effect on native low-skill workers in the wage specifications. This cuts against large Borjas-style native wage gains in the observed mandate margin, not every Borjas wage claim or surge/mass-shock regime.
    29	- E-Verify mandates have a negative ~6% stable E1 W-2 employment point estimate in exposed industries, but it is not conventionally significant (t=-1.40, p≈0.16). Consistent in sign with Bohn-Lofstrom-Raphael 2014 AZ finding, but not a measured pooled employment drop. Capital, output, relocation, cash-economy substitution, hours, and composition remain candidate channels rather than measured mechanisms.
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
    42	- E-Verify TWFE: pre-trends visually flat in event study; formal staggered-DiD robustness was not run. The result is consistent with bounded Card-side wage evidence and passes at the level of "large Borjas-style native wage gains are not observed in this design"; it is not a direct replication of Card-Peri / Foged-Peri or a test of surge, mass-deportation, or extreme counterfactual regimes.
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

--- BEGIN FILE EXCERPT: research/immigration-conclusion-audit-running-fixes.md lines 1-95 ---
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
    11	**Status update (2026-06-16): superseded again.** The 2026-06-15 correction fixed one denominator misuse but introduced the mirror-image problem: the school numerator still came from the `origin_fiscal_scenario_2023` household universe (~436,819 Mexico scenario adults / 322,540 linked household weight), while the denominator was changed to the full microsim adult stock (~8,496,334). The live builder now withholds origin school and `federal - school` rows until numerator and denominator universes match.
    12	
    13	### Issue
    14	
    15	The school-burden memo and a stale exported CSV still supported the conclusion that Mexico-origin adults had a crude annual federal-minus-school balance of about **-$13.5k/adult**. That result used the `origin_fiscal_scenario_2023` scenario subset denominator (~436,819 adults) after multiplying area-weighted per-pupil school spend by household school-age children. [DATA]
    16	
    17	That denominator was wrong for a full Mexico-origin adult-stock conclusion. The live tensor now uses the full Mexico microsim adult denominator (~8,496,334 adults). [DATA]
    18	
    19	### Evidence Checked
    20	
    21	```sql
    22	SELECT *
    23	FROM v_three_layer_annual
    24	WHERE population_group = 'mexico_origin';
    25	```
    26	
    27	Then-current DuckDB result from `warehouse/immigration_fiscal_union.duckdb`, now superseded by the 2026-06-16 same-universe guard:
    28	
    29	| federal_per_adult | school_per_adult | net_crude_per_adult | weight_adults |
    30	|------------------:|-----------------:|--------------------:|--------------:|
    31	| 1519.278 | 771.285 | 747.993 | 8496334 |
    32	
    33	Scenario source check from `warehouse/immigration_lifetime_evidence.duckdb`:
    34	
    35	| origin | scenario adults | avg federal net | area-wtd per pupil | school-age kids/HH | HH weight |
    36	|--------|----------------:|----------------:|-------------------:|-------------------:|----------:|
    37	| Mexico | 436819 | 1519.278 | 20907.09 | 0.9718 | 322540 |
    38	
    39	The old ~-$13.5k conclusion came from dividing the household school burden by the scenario subset. The intermediate correction computed school burden as:
    40	
    41	`20907.09 * 0.9718 * 322540 / 8496334 = ~$771/adult` [INFERENCE]
    42	
    43	### Fixes Made
    44	
    45	1. Updated `research/immigration-school-burden-per-adult-2026-06-15.md`:
    46	   - Briefly changed the Mexico-origin row to `$1,519` federal, `$771` school, `+$748` crude annual.
    47	   - This row is now superseded by the 2026-06-16 universe-mismatch fix below.
    48	   - Removed the stale verdict that Mexico looks far worse than natives on crude static federal-minus-school math, but the replacement positive net is also not live.
    49	
    50	2. Updated `research/immigration-scenario-composition-2026-06-15.md`:
    51	   - Replaced obsolete `~$21/pupil` text with post-F-33 `~$20,907/pupil`.
    52	   - Added a warning not to use `436,819` scenario adults as the full Mexico-origin stock denominator.
    53	
    54	3. Updated `research/immigration-lifetime-fiscal-generators.md`:
    55	   - Rewrote G-LIF-K01 so future audits check both F-33 units and per-adult denominator discipline.
    56	
    57	4. Updated `infra/immigration-fiscal/build/build_country_fiscal_tensor.py`:
    58	   - The tensor builder now exports `three_layer_annual_2023.csv` from the live `v_three_layer_annual` view.
    59	
    60	5. Regenerated canonical staged CSVs under `infra/immigration-fiscal/build/stage3_proto/`, including `three_layer_annual_2023.csv`, from the live DuckDB view.
    61	
    62	### Current Conclusion
    63	
    64	This intermediate finding is now superseded: the built annual **federal-minus-school** layer should not be reported for Mexico-origin adults until its school numerator and adult denominator use the same universe. [DATA]
    65	
    66	The lifetime NPV, state/local surge, enforcement, courts, and episodic shelter layers remain separate and cannot be collapsed into the narrow federal annual row. [INFERENCE]
    67	
    68	### Remaining Risk
    69	
    70	The corrected current conclusion is now narrower: the Mexico-origin **federal annual** row remains about `$1,519/adult/yr`, but the origin-specific `school_burden_per_adult` and `net_crude_federal_minus_school` rows are unresolved until the school numerator is rebuilt on the same population universe as the adult denominator. The old `+$748/adult/yr` net should not be cited as a live finding. [DATA]
    71	
    72	---
    73	
    74	## 2026-06-16 — Origin school layer withheld after universe mismatch
    75	
    76	### Issue
    77	
    78	The 2026-06-15 school correction divided a school-cost numerator from the origin scenario household universe by the full Mexico microsim adult denominator:
    79	
    80	`20907.09 * 0.9718 * 322540 / 8496334 = ~$771/adult`
    81	
    82	That arithmetic was reproducible, but the numerator and denominator did not describe the same population. `322,540 * 0.9718` is about `313k` linked school-age children in the scenario household universe; spreading that numerator over `8.5M` full-stock adults implies only about `0.037` school-age children per adult for Mexico-origin households, which is not a defensible full-stock school-incidence estimate. [DATA] [INFERENCE]
    83	
    84	### Evidence Checked
    85	
    86	Current DB probes:
    87	
    88	```text
    89	ctx.acs_origin_household_national_2023 Mexico:
    90	linked_household_wgt=322,539.5
    91	linked_mean_hh_school_age_children=0.971785
    92	
    93	ctx.acs_origin_national_2023 Mexico:
    94	weighted_adults=436,819
    95	
--- END FILE EXCERPT ---

--- BEGIN FILE EXCERPT: research/immigration-conclusion-audit-running-fixes.md lines 2360-2620 ---
  2360	---
  2361	
  2362	## 2026-06-16 — Caplan worker-incidence channel kept evidence-surface scoped
  2363	
  2364	### Issue
  2365	
  2366	`research/immigration-bryan-caplan-claims-audit-2026-04-21.md` said the "strongest current worker-incidence channel" is slower wage progression in constrained places rather than job destruction. [DATA]
  2367	
  2368	### Why it was wrong
  2369	
  2370	The memo can say current repo evidence better develops constrained-place wage progression than broad job-destruction rhetoric. But "strongest current channel" implies a global channel ranking across worker incidence that the cited county panel does not establish. [SOURCE: memo] [INFERENCE]
  2371	
  2372	### Fix
  2373	
  2374	Changed the line to say that in the repo's current worker-incidence evidence surface, the better-developed concern is slower wage progression in constrained places rather than broad job destruction. [SOURCE: memo]
  2375	
  2376	### Updated conclusion
  2377	
  2378	The Caplan audit still rejects crude job-collapse rhetoric, while keeping the alternative worker-incidence channel scoped to the current evidence surface. [INFERENCE]
  2379	
  2380	---
  2381	
  2382	## 2026-06-16 — E-Verify event-study interpretation kept unresolved
  2383	
  2384	### Issue
  2385	
  2386	`research/immigration-causal-everify-card-vs-borjas.md` said slightly negative, nonsignificant event-study point estimates were "suggestive of mild complementarity loss," and said a mass-deportation shock would "probably not" behave the same as the E-Verify design. [DATA]
  2387	
  2388	### Why it was wrong
  2389	
  2390	The event-study coefficients are not statistically distinguishable from zero, so the memo should not give one mechanism a suggestive gloss. Likewise, mass deportation is outside the observed mandate margin; "probably not" is plausible, but the stronger source-anchored statement is simply that the behavior is unknown because magnitudes and equilibria differ. [SOURCE: memo] [INFERENCE]
  2391	
  2392	### Fix
  2393	
  2394	Changed the event-study sentence to say the slightly negative points should not be read as evidence for a specific complementarity-loss mechanism, and changed the mass-deportation bullet to "unknown" rather than "probably not." [SOURCE: memo]
  2395	
  2396	### Updated conclusion
  2397	
  2398	The E-Verify memo now keeps nonsignificant event-study movement and out-of-margin mass-shock behavior unresolved instead of assigning them a preferred mechanism. [INFERENCE]
  2399	
  2400	---
  2401	
  2402	## 2026-06-16 — E-Verify null and Borjas-scaling language made symmetric
  2403	
  2404	### Issue
  2405	
  2406	A post-fix model review found that the E-Verify memo and summaries still applied significance discipline asymmetrically: wage coefficients were described as nonsignificant, but the E1 employment coefficient was still written as a realized `~6%` fall despite `t=-1.40` / `p≈0.16`. The same review flagged that the memo's `~5-15%` Borjas benchmark was not scaled to the observed mandate-margin shock. [DATA]
  2407	
  2408	### Why it was wrong
  2409	
  2410	The QWI employment point estimate is negative, but not conventionally significant. Treating it as a measured drop made the "employment fell while wages did not rise" contrast too strong. Separately, Borjas's own elasticity framing implies that a smaller effective supply shock maps to a smaller wage benchmark, so the memo can cut against large gains in the observed margin without rejecting every scaled Borjas effect. [SOURCE: `research/immigration-causal-everify-card-vs-borjas.md`] [INFERENCE]
  2411	
  2412	### Fix
  2413	
  2414	Updated `research/immigration-causal-everify-card-vs-borjas.md`, `CYCLE.md`, `research/immigration-causal-synthesis-2026-04-18.md`, `research/immigration-confidence-ladder.md`, `research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md`, and `research/immigration-restrictionist-arguments-steelman-2026-06-15.md`:
  2415	
  2416	- E1 employment is now a negative, statistically nonsignificant point estimate rather than a measured drop.
  2417	- The wage result now cuts against large Borjas-style native wage gains in the observed mandate margin, while leaving small effects and scaled-shock benchmarks unresolved.
  2418	- "Card/Borjas" comparison labels now name directional readings in each design rather than global debate verdicts.
  2419	
  2420	### Updated conclusion
  2421	
  2422	The current E-Verify conclusion is narrower: observed mandate variation shows no statistically significant positive QWI wage effect for native low-skill workers and cuts against large native wage gains in that margin. It does not prove an exact zero wage effect, a measured labor-supply contraction, a significant employment decline, or a global rejection of Borjas-style mechanisms. [INFERENCE]
  2423	
  2424	---
  2425	
  2426	## 2026-06-16 — Crime memo Lott narrative matched critique status
  2427	
  2428	### Issue
  2429	
  2430	`research/immigration-crime-rates-unauthorized-vs-native-born.md` had downgraded the Lott Arizona row to `SUPPORTED CRITIQUE — not independent reanalysis`, but the bottom line and contrarian-case heading still said Lott had been criticized for a "fundamental data classification error." [DATA]
  2431	
  2432	### Why it was wrong
  2433	
  2434	The memo cites serious critiques from Cato, Washington Post, and Latino Decisions; it does not independently reanalyze Arizona DOC records. The supported claim is an unresolved immigration-status classification critique, not a verified data error. The Texas `>2x` violent-arrest row also needed the memo's own aggregate-native-denominator / race-composition caveat. [SOURCE: memo] [INFERENCE]
  2435	
  2436	### Fix
  2437	
  2438	Changed the bottom-line and contrarian-case Lott wording to "serious unresolved" / "serious possible" immigration-status classification problem. Added a denominator caveat to the Texas `>2x` violent-arrest claim row. [SOURCE: memo]
  2439	
  2440	### Updated conclusion
  2441	
  2442	The crime memo still supports lower observed criminal-justice rates for unauthorized immigrants in the best current U.S. datasets, but it no longer treats the Lott classification critique as independently verified by this memo or the aggregate Texas ratio as race-composition-adjusted. [INFERENCE]
  2443	
  2444	---
  2445	
  2446	## 2026-06-16 — Capacity and surge model rankings kept descriptive
  2447	
  2448	### Issue
  2449	
  2450	Model review flagged several remaining places where descriptive county or receiver-city model output was being read too strongly: the capacity memo called load/capacity the "cleaner" wage signal despite tiny adjusted-`R²` gaps, the surge memo bundled gross fiscal load and election shift into one "empirical support" story, and the Caplan audit treated constrained-place wage pressure as more established than the county screen supports. [DATA]
  2451	
  2452	### Why it was wrong
  2453	
  2454	The county capacity pass is useful descriptive screening, not causal identification. For wages, the load-only adjusted-`R²` edge over stock/flow is only about 0.007-0.010, and permit units in the denominator can proxy local economic vitality. The surge receiver fiscal figures are observable gross loads, but the +2.4pp receiver election coefficient is still correlational. Caplan's labor critique should cite evidence consistent with constrained-place wage pressure, not treat it as a settled channel. [SOURCE: memos] [INFERENCE]
  2455	
  2456	### Fix
  2457	
  2458	Updated:
  2459	
  2460	- `research/immigration-capacity-frontier-2026-04-21.md`: stock/load claims now say "one-predictor county model signal," wage ranking is "marginally best-fitting," q90 threshold weakness is caveated for power/multiple-testing, and permit-denominator confounding is explicit.
  2461	- `research/immigration-causal-surge-2021-2024.md`: per-migrant costs are scoped to sheltered-migrant-day gross cost, receiver load is separated from the correlational election result, the stale `~50K/month` flow line is replaced with the corrected Total-CBP range, and the original no-Hispanic receiver regression is reconciled with the later Hispanic-share kill-test sample.
  2462	- `research/immigration-bryan-caplan-claims-audit-2026-04-21.md`: constrained-place wage pressure is evidence-consistent rather than a settled pressure channel.
  2463	
  2464	### Updated conclusion
  2465	
  2466	The capacity/surge evidence remains decision-relevant as descriptive screening: it points to load/capacity, receiver fiscal load, and constrained-place wage-growth concerns. It does not yet identify a causal native-exit mechanism, a fiscal-load-to-vote mechanism, or a globally ranked worker-incidence channel. [INFERENCE]
  2467	
  2468	---
  2469	
  2470	## 2026-06-16 — Thesis generator loop widened beyond fiscal ledger monoculture
  2471	
  2472	### Issue
  2473	
  2474	The lifetime generator loop was strong on fiscal layers, denominator discipline, and scalar-export prevention, but the active prompts were still mostly fiscal/lifetime-native. The registry also had a lifecycle-sync problem: `research/immigration-lifetime-fiscal-generators.md` had 106 `G-LIF-*` headings, its header said 105 generators, and DuckDB had 104 `lifetime_generators` rows. [DATA]
  2475	
  2476	### Why it was wrong
  2477	
  2478	The user's search-space shaping has repeatedly added non-fiscal axes: psychology, political legitimacy, narrative formation, urban capacity, macro transition paths, and micro adaptation. A generator loop that only mines fiscal papers risks converging too early on ledger-correct but narrative-blind theses. The count mismatch also blocks honest yield tracking and retirement rules. [SOURCE: `research/immigration-thesis-generator-audit-2026-06-16.md`] [INFERENCE]
  2479	
  2480	### Fix
  2481	
  2482	Added `research/immigration-thesis-generator-audit-2026-06-16.md`, with cross-disciplinary `XDISC-*` generators, a self-prompt packet, a human-replacement flowchart for search-space shaping, and an implementation recommendation for generator lifecycle fields. Updated the topic index, sweep protocol, and divergence cookbook to route future sweeps through this packet. Changed the fiscal-generator header and index wording from stale counts to warehouse-grounded counts plus the explicit reconciliation issue (`G-LIF-Q06`, `G-LIF-S15` MD-only). [SOURCE: memo]
  2483	
  2484	### Updated conclusion
  2485	
  2486	The current loop should not run another immigration sweep from fiscal generators alone. Before source search, it should run the cross-disciplinary packet, then converge with explicit data-vs-frame separation and generator-yield accounting. [INFERENCE]
  2487	
  2488	---
  2489	
  2490	## 2026-06-16 — Verified federal and school surfaces refreshed
  2491	
  2492	### Issue
  2493	
  2494	`research/immigration-verified-findings-report-2026-04-10.md` and `research/immigration-confidence-ladder.md` still treated two April surfaces as if they were current: the household-normalized child-burden correction was easy to read as a live full-stock school/adult or origin net sign, and the failed Texas/CPS donor prototype was still described as the repo's current federal surface. [DATA]
  2495	
  2496	### Why it was wrong
  2497	
  2498	June work changed both surfaces. The school-burden tensor now withholds origin school/net rows because the available school numerator came from the scenario-household universe while the federal row uses full microsim adults. Separately, the SIPP-style federal annual proxy supersedes the April ACS/CPS shortcut for the narrow cash-flow ledger, but only as payroll/FICA minus SNAP, TANF, and SSI; it is not income tax, Medicare/Medicaid, EITC, capital/corporate tax, household filing, lifetime NPV, or all-government net. [SOURCE: `research/immigration-school-burden-per-adult-2026-06-15.md`] [SOURCE: `research/immigration-federal-distribution-findings-2026-06-15.md`] [SOURCE: `research/immigration-country-fiscal-tensor-2026-06-15.md`]
  2499	
  2500	### Fix
  2501	
  2502	Updated:
  2503	
  2504	- `research/immigration-verified-findings-report-2026-04-10.md`: scoped household-normalized school language to linked-household child exposure, marked origin school/net rows as withheld pending same-universe rebuild, replaced the current-federal-prototype language with the June SIPP-style narrow annual proxy plus all-in limitations, and added a revisions table.
  2505	- `research/immigration-confidence-ladder.md`: qualified the household metric, downgraded the old ACS income/benefit ranking to historical screen, added entry `41` for the current narrow federal annual proxy, and updated the reading rule.
  2506	
  2507	### Updated conclusion
  2508	
  2509	The current verified surface is narrower and cleaner: strong linked-household child-exposure evidence; medium-strong descriptive evidence for a narrow annual federal cash-flow proxy; no live all-in federal number; and no current origin `federal - school` sign until the school numerator and adult denominator are rebuilt on the same universe. [INFERENCE]
  2510	
  2511	---
  2512	
  2513	## 2026-06-16 — Full-protocol sweep rows marked superseded
  2514	
  2515	### Issue
  2516	
  2517	`research/immigration-sweep-cycles-23-32-2026-06-15.md` was still routed by the topic index as the "full protocol" sweep and contained old origin school/net rows: Mexico `school` `$771`, Mexico `crude` `+$748`, EU27 `school` `$64`, and similar rows for cycle 32. Those rows came from the intermediate correction that was later rejected by the same-universe guard. [DATA]
  2518	
  2519	### Why it was wrong
  2520	
  2521	The current `v_three_layer_annual` view withholds origin and aggregate foreign-born school/net rows. A direct DuckDB query on 2026-06-16 returned `NULL` `school_per_adult` and `net_crude_per_adult` for `mexico_origin`, `mx_ca_cluster`, `eu27_origin`, `uk_origin`, and `fb_lt_hs`; only `nh_white_usborn` retained a built school/net row in that slice. Leaving the old numeric rows unqualified in the full-protocol memo made it too easy for later agents to cite a stale `federal - school` sign. [DATABASE: `warehouse/immigration_fiscal_union.duckdb` view `v_three_layer_annual`] [INFERENCE]
  2522	
  2523	### Fix
  2524	
  2525	Updated `research/immigration-sweep-cycles-23-32-2026-06-15.md` with a 2026-06-16 status block, supersession notes on cycles 24, 26, 30, and 32, and a revisions table. Updated `research/immigration-INDEX.md` so the route row warns not to cite the old `$771/+748` origin school/net outputs. [SOURCE: memo]
  2526	
  2527	### Updated conclusion
  2528	
  2529	Sweeps 23–32 still preserve useful NAS education-mix, federal-proxy, and thesis-generation work, but their origin school/net numbers are historical traces, not current facts. Current live origin `federal - school` signs remain withheld until same-universe school numerators are rebuilt. [INFERENCE]
  2530	
  2531	---
  2532	
  2533	## 2026-06-16 — Quick claims matrix labels narrowed
  2534	
  2535	### Issue
  2536	
  2537	`research/immigration-claims-matrix-2026-04-11.md` was still framed as the current defensible claim set and used terse verdict labels such as `MODERATE-FALSE`, `VERIFIED false`, and `MODERATE-FALSE (as complete fix)` for commentator claims. It also described the household child metric as "school burden" without carrying the later same-universe guard. [DATA]
  2538	
  2539	### Why it was wrong
  2540	
  2541	The named Smith/Decker and Friedman audits support strong critiques, but their own language is narrower: Decker's "must make us richer" fails as a universal theorem; the politics-only claim is false as an exclusivity claim; Friedman's transfer/voting proposal is incomplete rather than empirically false in all frames. Separately, the child rows are linked-household exposure metrics, not current full-stock school-burden-per-adult or origin `federal - school` signs. [SOURCE: `research/immigration-noah-smith-nicholas-decker-claims-audit-2026-04-11.md`] [SOURCE: `research/immigration-david-d-friedman-claims-audit-2026-04-11.md`] [SOURCE: `research/immigration-school-burden-per-adult-2026-06-15.md`]
  2542	
  2543	### Fix
  2544	
  2545	Updated `research/immigration-claims-matrix-2026-04-11.md` with a 2026-06-16 status note, added an `OVERBROAD` legend entry, scoped row 5 to linked-household child exposure, replaced hard false labels with scoped overbreadth/incomplete verdicts, and updated the verdict envelope to include the narrow SIPP-style federal proxy plus withheld origin school/net signs. Updated the index route row to warn that this matrix is a quick ledger, not the latest tensor. [SOURCE: memo]
  2546	
  2547	### Updated conclusion
  2548	
  2549	The quick matrix still supports the same broad incidence split, but it no longer exports overconfident boolean labels or treats linked-household child exposure as a live school/adult fiscal scalar. [INFERENCE]
  2550	
  2551	---
  2552	
  2553	## 2026-06-16 — Public economist summaries scoped to descriptive evidence
  2554	
  2555	### Issue
  2556	
  2557	The public-facing economist one-pager, debate sheet, and rhetorical-failures memo still used several stronger causal or mechanism-flavored phrases after the underlying capacity/surge corrections had been narrowed. Examples included treating `flow x capacity x composition x regime` as a live causal object, describing destination-local "harm" rather than stress/gross-load evidence, using native-backlash language where the measured object is political-response association, and presenting constrained-place wage pressure as firmer than the county screen supports. [DATA]
  2558	
  2559	### Why it was wrong
  2560	
  2561	The later capacity/surge corrections say the county capacity pass is useful descriptive screening, not causal identification; the receiver fiscal rows are gross load and shelter-stress evidence, not net fiscal-burden estimates; and the receiver-election result is a correlational `+2.4pp` upper-bound after controls, not a fiscal-load-to-vote mechanism. Public summaries are high-reuse artifacts, so causal overtones there can undo the narrower source memos. [SOURCE: `research/immigration-capacity-frontier-2026-04-21.md`] [SOURCE: `research/immigration-causal-surge-2021-2024.md`] [SOURCE: `research/immigration-conclusion-audit-running-fixes.md`]
  2562	
  2563	### Fix
  2564	
  2565	Updated:
  2566	
  2567	- `research/immigration-economist-one-pager-2026-04-22.md`: added a 2026-06-16 status warning and changed capacity, denominator, federal/local, and political wording to descriptive/gross/correlational language.
  2568	- `research/immigration-economist-debate-sheet-2026-04-22.md`: added the same scope warning and narrowed the wage, fiscal, and political counters.
  2569	- `research/immigration-economist-rhetorical-failures-2026-04-22.md`: changed "harm," "rejected," "native backlash," and "live causal object" style language to stress/gross-load/political-response/descriptive-screen language.
  2570	
  2571	### Updated conclusion
  2572	
  2573	The public economist critique remains intact: partial efficiency and migrant-gain arguments do not settle destination-country welfare. The evidence basis is now stated more precisely: current capacity/surge support is descriptive and correlational where the underlying designs do not identify causal mechanisms. [INFERENCE]
  2574	
  2575	---
  2576	
  2577	## 2026-06-16 — Legacy synthesis surfaces aligned with same-universe guard
  2578	
  2579	### Issue
  2580	
  2581	Two high-reuse synthesis surfaces still carried language from before the June 16 narrowing pass. `research/immigration-mexico-npv-population-synthesis-2026-06-15.md` said the executive short-horizon row was withheld, but its warehouse-layer table still printed the superseded Mexico-origin `$771` school and `+$748` crude-net rows. `research/immigration-claims-evolution-ledger-2026-04-23.md` also kept older Card/Borjas and native-backlash shorthand that could be read as stronger than the current E-Verify and political-response surfaces support. [DATA]
  2582	
  2583	### Why it was wrong
  2584	
  2585	The same-universe guard withholds origin `school_burden_per_adult` and `net_crude_federal_minus_school` until the school numerator is rebuilt on the same population universe as the adult denominator. Separately, the current E-Verify conclusion is mandate-margin and nonsignificance-scoped, and receiver-election evidence is correlational political response, not identified backlash motivation. [SOURCE: `research/immigration-conclusion-audit-running-fixes.md`] [INFERENCE]
  2586	
  2587	### Fix
  2588	
  2589	Updated `research/immigration-mexico-npv-population-synthesis-2026-06-15.md` to mark the old `$771/+748` rows as withheld/superseded and added an explicit disconfirmation row against citing them as current. Updated `research/immigration-claims-evolution-ledger-2026-04-23.md` with a 2026-06-16 status note, narrowed the labor-market summary to observed E-Verify mandate variation, and replaced native-backlash wording with citizen political-response language. [SOURCE: memos]
  2590	
  2591	### Updated conclusion
  2592	
  2593	The evolution ledger and Mexico synthesis now match the current frontier: no live Mexico-origin `federal - school` sign, no measured E-Verify labor-supply contraction, and no identified fiscal-load-to-vote or backlash mechanism. [INFERENCE]
--- END FILE EXCERPT ---
