# Immigration thesis/narrative generator audit and upgrade - 2026-06-16

**Purpose:** evaluate the current immigration thesis-generation loop, compare what it knows now against the June 14 baseline, and add better cross-disciplinary generators from economics, micro, macro, psychology, political economy, and urbanism.

**Companion loop (broader):** `research/immigration-knowledge-delta-agent-loop-2026-06-16.md` owns the canonical umbrella loop: claim inventory, probe, adversarial review, commit routing, and stop/escalation. This memo owns the generator and XDISC sub-loop for that loop's divergence/probe steps.

**Verdict:** the current generator system is useful and materially better than two days ago, but it is still too fiscal-ledger-native. It catches scalar exports, denominator slips, and layer laundering; it does not yet force enough narrative, legitimacy, sorting, contact/threat, spatial-equilibrium, and agenda-setting alternatives before convergence. [SOURCE: `notes/immigration-lifetime-synthesis-diverge-cookbook.md`; `research/immigration-lifetime-fiscal-generators.md`; DuckDB query on `warehouse/immigration_lifetime_evidence.duckdb`] [INFERENCE]

---

## Ground inventory

### Current artifacts

| Surface | Current state | Audit read |
|---|---:|---|
| Diverge/converge cookbook | Explicit loop: carry prior thesis + generator menu + DuckDB state -> diverge -> converge -> next sweep | Strong process spine; mostly fiscal-lifetime scoped. [SOURCE: `notes/immigration-lifetime-synthesis-diverge-cookbook.md`] |
| Generator registry | Markdown has `106` `G-LIF-*` headings; DuckDB has `104` rows across `19` clusters; MD-only IDs are `G-LIF-Q06`, `G-LIF-S15` | Useful but count/lifecycle sync is not clean enough for automated yield scoring. [SOURCE: `rg -c '^### G-LIF'`; DuckDB `count(*)`; `comm -23`; `describe lifetime_generators`] |
| Generator schema in DuckDB | `generator_id`, `name`, `prompt_template`, `retrodiction_example`, `negative_space`, `unnamed_assumptions`, `topics`, `source_rel_paths`, `cluster`, `theory_tested` | Good minimum schema; missing status/yield/last-fired/retirement fields. [SOURCE: DuckDB `describe lifetime_generators`] |
| Parameter claims | DuckDB has `563` rows in `parameter_claims` | Header/index counts must use warehouse truth or explicitly say Markdown-only. [SOURCE: DuckDB `select count(*) from parameter_claims`] |
| Unified theory | Layered incidence tensor: cell x ledger layer x time; no scalar "Mexican lifetime NPV" | Strong correction against the main fiscal overclaim. [SOURCE: `research/immigration-lifetime-unified-theory-2026-06-15.md`] |
| Running fixes ledger | Many June 16 fixes demote overclaims to scoped, model- or margin-bound claims | Good error-correction surface; should also log process fixes. [SOURCE: `research/immigration-conclusion-audit-running-fixes.md`] |

### Two-day knowledge delta

Using the repository baseline before the end of June 14, the named lifetime generator/cookbook/unified-theory/knowledge-delta artifacts were not yet present in tracked history. By June 16, the repo has a dedicated divergence cookbook, a lifetime fiscal generator registry, a unified theory memo, and a knowledge-delta agent loop memo. [SOURCE: `git rev-list -1 --before='2026-06-14 23:59' main -- ...`; `git log --since='2026-06-14' -- ...`; `research/immigration-knowledge-delta-agent-loop-2026-06-16.md`] [DATA]

What changed:

1. **From memo accumulation to loop discipline.** Two days ago, the repo had immigration memos and audits; now it has an explicit loop: carry thesis, generate negative space, mine sources, converge into layered theory, then disconfirm before the next sweep. [SOURCE: git history; `notes/immigration-lifetime-synthesis-diverge-cookbook.md`] [INFERENCE]
2. **From scalar fiscal answers to tensor grammar.** The central object is now `cell x ledger layer x time`, not "immigrants are net positive/negative." This is the largest conceptual improvement. [SOURCE: `research/immigration-lifetime-unified-theory-2026-06-15.md`] [INFERENCE]
3. **From source harvesting to generator harvesting.** The system now stores prompts that can retrodict prior misses and name negative space, instead of only storing paper findings. [SOURCE: `research/immigration-lifetime-fiscal-generators.md`] [INFERENCE]
4. **From confidence to correction.** The June 16 fix ledger repeatedly converts strong rhetoric into scoped evidence claims: non-significance is not zero, gross load is not causal mechanism, observed justice-system rate is not true offending, local burden is not all-in NPV. [SOURCE: `research/immigration-conclusion-audit-running-fixes.md`] [INFERENCE]
5. **Still missing:** generator yield accounting, non-fiscal narrative generators, and a self-prompt that forces an agent to ask what a public-finance economist, urbanist, macroeconomist, psychologist, restrictionist, and open-borders advocate would each call false. [INFERENCE]

---

## Evaluation of existing generators

### What is working

1. **Retrodiction as quality control.** The cookbook requires each generator to retrodict at least two prior findings. This is the right filter: a generator that cannot explain past misses is usually just a topic suggestion. [SOURCE: `notes/immigration-lifetime-synthesis-diverge-cookbook.md`] [INFERENCE]
2. **Negative-space fields.** The registry forces each generator to name what the standing frame excludes, which directly fights search-space narrowing. [SOURCE: `research/immigration-lifetime-fiscal-generators.md`] [INFERENCE]
3. **Layer discipline.** Existing generators repeatedly catch fiscal/lifetime/annual/local layer switching. This is the repo's main statistical advantage over pundit-style immigration narratives. [SOURCE: `research/immigration-lifetime-fiscal-generators.md`] [INFERENCE]
4. **Disconfirmation after convergence.** The protocol makes contradiction hunts part of convergence rather than an optional review step. [SOURCE: `notes/immigration-lifetime-sweep-protocol.md`] [INFERENCE]

### What is weak

1. **Fiscal center of gravity.** The existing registry is excellent for public-finance and immigration-economics errors, and it has partial housing/capacity/admin/political clusters. It still underweights psychology, agenda-setting, urban sorting, legitimacy, symmetric pro-immigration steelmanning, and social contact/threat narratives. [INFERENCE]
2. **Urbanism is too rent/supply-centered.** The E cluster goes beyond Saiz alone, but urban incidence still needs Tiebout sorting, Roback spatial equilibrium, Diamond amenity sorting, local employment multipliers, zoning/productivity misallocation, and service-capacity politics. [SOURCE: Saiz 2010 QJE; Tiebout 1956 JPE; Roback 1982 JPE; Diamond 2016 AER; Hsieh & Moretti 2019 AEJ Macro] [INFERENCE]
3. **Micro/macro identification prompts are too implicit.** The loop should force estimand classification, target/instrument matching, shift-share/enclave identification, household/firm adaptation margins, capital deepening, dependency-ratio transitions, and reflection/social-effects identification. [SOURCE: Tinbergen policy target/instrument framework; Manski 1993 reflection problem; Card 2001; Goldsmith-Pinkham et al. 2020] [INFERENCE]
4. **Narrative self-prompting is underbuilt and asymmetry-prone.** The loop asks for thesis bursts, but not enough for frame audits: who is the hero/victim/villain, what causal story is being smuggled in, what pro-immigration frame is absent, and what would make the story politically salient even if the fiscal ledger is small? [SOURCE: Entman 1993 framing; Stone 1989 causal stories; Kingdon multiple-streams framework] [INFERENCE]
5. **Lifecycle accounting is missing.** There is no `status`, `last_fired`, `adopted_outputs`, or `retirement_counter` in the DuckDB schema; the cookbook now says to park zero-yield generators while applicable, but that rule still has no machine-readable state. [SOURCE: DuckDB `describe lifetime_generators`; `notes/immigration-lifetime-synthesis-diverge-cookbook.md`] [DATA]

---

## Cross-disciplinary generator upgrade

Use these as a new "XDISC" packet before the next immigration sweep. They are not yet loaded into `lifetime_generators`; the first implementation should either add a new loaded cluster or keep them as a separate `thesis_generators` table so fiscal generators do not silently become all-purpose narrative prompts. [INFERENCE]

### Source-anchor audit added 2026-06-16

The XDISC rows below are prompts, not literature-review conclusions. Before registry loading, each source-backed row needs either a verified DOI/local source path or an explicit `[INFERENCE]` tag. This spot check verified the following anchors through `mcp__research.resolve_doi`; rows outside this table, especially book/framework-only sources, still need bibliographic cleanup before they become machine-loaded source claims. [DATA]

| Area | Verified anchor | DOI |
|---|---|---|
| Social effects / reflection | Manski, "Identification of Endogenous Social Effects: The Reflection Problem" (1993) | `10.2307/2298123` |
| Shift-share identification | Goldsmith-Pinkham, Sorkin & Swift, "Bartik Instruments: What, When, Why, and How" (2020) | `10.1257/aer.20181047` |
| Housing supply | Saiz, "The Geographic Determinants of Housing Supply" (2010) | `10.1162/qjec.2010.125.3.1253` |
| Local public goods | Tiebout, "A Pure Theory of Local Expenditures" (1956) | `10.1086/257839` |
| Spatial equilibrium | Roback, "Wages, Rents, and the Quality of Life" (1982) | `10.1086/261120` |
| Skill sorting / amenities | Diamond, "The Determinants and Welfare Implications of US Workers' Diverging Location Choices by Skill" (2016) | `10.1257/aer.20131706` |
| Housing constraints / macro misallocation | Hsieh & Moretti, "Housing Constraints and Spatial Misallocation" (2019) | `10.1257/mac.20170388` |
| Local multipliers | Moretti, "Local Multipliers" (2010) | `10.1257/aer.100.2.373` |
| High-skill immigration / innovation | Kerr & Lincoln, "The Supply Side of Innovation: H-1B Visa Reforms and U.S. Ethnic Invention" (2010) | `10.1086/651934` |
| Immigration / innovation | Hunt & Gauthier-Loiselle, "How Much Does Immigration Boost Innovation?" (2010) | `10.1257/mac.2.2.31` |
| Club goods | Buchanan, "An Economic Theory of Clubs" (1965) | `10.2307/2552442` |
| Resource governance | Ostrom, "A General Framework for Analyzing Sustainability of Social-Ecological Systems" (2009) | `10.1126/science.1172133` |
| Diversity / social capital | Putnam, "E Pluribus Unum" (2007) | `10.1111/j.1467-9477.2007.00176.x` |
| Group threat | Quillian, "Prejudice as a Response to Perceived Group Threat" (1995) | `10.2307/2096296` |
| Contact theory | Pettigrew & Tropp, "A meta-analytic test of intergroup contact theory" (2006) | `10.1037/0022-3514.90.5.751` |
| Immigration attitudes | Hainmueller & Hopkins, "Public Attitudes Toward Immigration" (2014) | `10.1146/annurev-polisci-102512-194818` |
| Immigration misperceptions / redistribution | Alesina, Miano & Stantcheva, "Immigration and Redistribution" (2018) | `10.3386/w24733` |
| Information and attitudes | Grigorieff, Roth & Ubfal, "Does Information Change Attitudes Toward Immigrants?" (2020) | `10.1007/s13524-020-00882-8` |
| Diversity / redistribution | Alesina & Stantcheva, "Diversity, Immigration, and Redistribution" (2020) | `10.1257/pandp.20201088` |
| Motivated numeracy | Kahan et al., "Motivated numeracy and enlightened self-government" (2017) | `10.1017/bpp.2016.2` |
| Agenda-setting | McCombs & Shaw, "The Agenda-Setting Function of Mass Media" (1972) | `10.1086/267990` |
| Issue ownership | Petrocik, "Issue Ownership in Presidential Elections, with a 1980 Case Study" (1996) | `10.2307/2111797` |
| Causal stories | Stone, "Causal Stories and the Formation of Policy Agendas" (1989) | `10.2307/2151585` |
| Framing | Entman, "Framing: Toward Clarification of a Fractured Paradigm" (1993) | `10.1111/j.1460-2466.1993.tb01304.x` |
| Deservingness | van Oorschot, "Who should get what, and why?" (2000) | `10.1332/0305573002500811` |

| ID | Family | Generator prompt | Retrodicts / first probe |
|---|---|---|---|
| XDISC-ECO-01 | Policy economics | For every recommendation, name the target variable and the policy instrument. Fail the claim if one instrument is asserted to solve multiple independent targets without tradeoff. | Retrodicts layer laundering: enforcement, welfare, housing, and fiscal goals were being treated as one target. First probe: annotate one memo's recommendations. [SOURCE: Tinbergen 1952/1956 policy framework] |
| XDISC-ECO-02 | Public finance | Split statutory payer, economic payer, beneficiary, jurisdiction, public-goods cost rule (average vs marginal; pure vs congestible), descendant boundary, and time horizon for every dollar claim. Fail any net-fiscal sign claim that lacks a public-goods rule and descendant boundary. | Retrodicts federal-positive/local-negative compatibility, school-cost numerator bugs, and NAS-style sign sensitivity. Probe: one row per cost/revenue line. [SOURCE: existing fiscal ledger memos; National Academies 2017] |
| XDISC-ECO-03 | Immigration surplus | For any wage/output effect, separate aggregate efficiency gain from redistribution between competing labor, complementary labor, and capital; state short-run vs capital-adjusted horizon. | Retrodicts how small average native effects can coexist with real distributional losses. Probe: decompose one Borjas/Card claim into efficiency triangle vs transfers. [SOURCE: Borjas 1995; Ottaviano & Peri 2012] |
| XDISC-MIC-01 | Micro adaptation | Before accepting a wage/fiscal effect, list household, firm, native, immigrant, and government adjustment margins: hours, tasks, location, household composition, take-up, compliance, exit. | Retrodicts why wage effect != fiscal effect and why native out-migration changes local incidence. Probe: annotate Borjas/Card/Saiz claims. [SOURCE: `research/immigration-lifetime-fiscal-generators.md`] |
| XDISC-MIC-02 | Social interactions | If group outcomes correlate, identify whether the claim is endogenous peer effect, contextual effect, correlated unobservables, selection, or measurement artifact. | Retrodicts receiver-city mechanism ambiguity and backlash overclaim downgrades. Probe: classify one political-response claim. [SOURCE: Manski 1993 reflection problem] |
| XDISC-MIC-03 | Labor identification | For any local immigration effect, name the design: spatial correlation, enclave/shift-share IV, factor-proportions national skill-cell, or event-study/policy shock. State skill cells, substitution elasticity, and leading endogeneity threat. | Retrodicts Borjas/Card divergence and native out-migration disputes. Probe: re-derive one local estimate's identifying variation and exclusion restriction. [SOURCE: Card 2001; Goldsmith-Pinkham, Sorkin & Swift 2020] |
| XDISC-MAC-01 | Macro transition path | For each static fiscal claim, ask what happens to capital/labor, age structure, dependency ratios, public debt, and tax rates over transition and steady state. | Retrodicts why annual federal proxy cannot be integrated into lifetime NPV without a bridge. Probe: draw 3-period transition table. [INFERENCE] |
| XDISC-MAC-02 | Open-economy welfare | Separate destination public ledger, origin-country welfare, remittances, and global output. State which welfare function is being optimized before using "gain/loss." | Retrodicts open-borders welfare-weight fixes and remittance/private-layer separation. Probe: add welfare-function column to one memo. [INFERENCE] |
| XDISC-MAC-03 | NPV sensitivity | For every lifetime/NPV claim, report discount rate, projection horizon, public-debt closure rule, capital adjustment, and mortality/return-migration horizon. | Retrodicts annual-to-lifetime bridge errors and sign flips under accounting conventions. Probe: sensitivity grid before any lifetime sign. [SOURCE: National Academies 2017] |
| XDISC-URB-01 | Tiebout/local public goods | Ask whether residents are sorting into tax/service bundles and whether immigration changes the bundle, the population choosing it, or only measured averages. | Retrodicts county capacity and school-service framing problems. Probe: map one state/local cost claim to bundle changes. [SOURCE: Tiebout 1956] |
| XDISC-URB-02 | Spatial equilibrium | Never infer welfare from wage or rent alone. Force wage, rent, amenity, and public-service bundle together. | Retrodicts Saiz/rent-exposure != welfare-loss fixes. Probe: convert one rent claim to a Roback-style welfare question. [SOURCE: Roback 1982; Diamond 2016] |
| XDISC-URB-03 | Housing constraint/productivity | Ask whether housing constraints turn national productivity gains into local renter losses, congestion, or spatial misallocation. | Retrodicts why open-borders/global gains and local-capacity losses can both be true. Probe: classify high-inflow MSAs by housing supply elasticity and productivity. [SOURCE: Saiz 2010; Hsieh & Moretti 2019] |
| XDISC-URB-04 | Local employment/demand multipliers | For every immigrant inflow cost claim, ask whether local demand, traded-sector employment, or service-sector multipliers offset or amplify the local tax base. Do not treat an employment multiplier as a fiscal multiplier without an induced-tax-base bridge. | Retrodicts why fiscal costs cannot be read from population count alone. Probe: separate tradable vs non-tradable exposure and fiscal bridge. [SOURCE: Moretti 2010] |
| XDISC-URB-05 | Agglomeration/innovation | Ask whether high-skill inflows generate innovation, entrepreneurship, patenting, or knowledge spillovers that offset congestion/housing losses, and at what spatial scale. | Retrodicts why high-skill immigration can be positive in national productivity while still worsening constrained-city housing incidence. Probe: separate innovation scale from local rent incidence. [SOURCE: Kerr & Lincoln 2010; Hunt & Gauthier-Loiselle 2010] |
| XDISC-INST-01 | Congestible club/local goods | Treat schools, courts, permits, shelters, and public safety as congestible club/local public goods with capacity, congestion, rationing, and jurisdiction rules. Use Ostrom only for genuine common-pool-resource cases. | Retrodicts receiver-node overload and admin-capacity findings without misclassifying every local service as a commons. Probe: identify one capacity bottleneck per local layer. [SOURCE: Buchanan 1965; Tiebout 1956; Ostrom 2009] |
| XDISC-PE-01 | Distributive political economy | Name winning and losing coalitions for each recommendation: employers/capital, native low-skill labor, native high-skill labor, taxpayers, immigrants, local incumbents. State who is organized and who is diffuse. | Retrodicts why aggregate gains can coexist with intense opposition. Probe: three coalitions per policy recommendation. [INFERENCE; verify source before registry load] |
| XDISC-PE-02 | Diversity and redistribution | Ask whether heterogeneity changes support for redistribution/public goods separately from measured fiscal cost. | Retrodicts welfare-state and public-goods political feedback arguments without collapsing them into budget arithmetic. Probe: tag each welfare claim as cost-channel vs solidarity-channel. [SOURCE: Alesina & Glaeser 2004; Putnam 2007] |
| XDISC-PSY-01 | Threat vs load | Split material burden from perceived group threat; tag theory as realistic threat, symbolic threat, group-conflict, or authoritarian-by-threat interaction. | Retrodicts political-response mechanism ambiguity. Probe: compare actual vs perceived immigrant share where available. [SOURCE: Quillian 1995] |
| XDISC-PSY-02 | Contact vs segregation | Ask whether contact is equal-status/cooperative/institutionally supported or concentrated, competitive, and capacity-stressed; apply XDISC-MIC-02 to check contact selection/reverse causation. | Retrodicts why "more contact reduces prejudice" is not a universal migration argument. Probe: classify receiver settings by contact conditions. [SOURCE: Pettigrew & Tropp 2006] |
| XDISC-PSY-03 | Misperception mediator | For any public-opinion or redistribution claim, insert a belief-mediator row: perceived immigrant share, skill, benefit use, origin, legality, and fiscal contribution. Then test whether correcting the belief changes the attitude; do not assume it does. | Retrodicts Alesina-style salience/redistribution channel and anti-overclaiming fixes. Probe: list belief variables before causal story. [SOURCE: Alesina, Miano & Stantcheva 2018; Grigorieff, Roth & Ubfal 2020] |
| XDISC-PSY-04 | Sociotropic vs egocentric | Split personal/pocketbook from national/collective, and economic from cultural. Fail attitude claims that infer personal self-interest from group-level correlations. | Retrodicts why immigration opposition can be weakly tied to direct local exposure. Probe: classify one opinion finding on both axes. [SOURCE: Hainmueller & Hopkins 2014] |
| XDISC-PSY-05 | Motivated reasoning | Ask whether the belief is identity-expressive; if so, predict that more evidence may widen, not narrow, group gaps. | Retrodicts why source-corrected memos may not move public narratives. Probe: mark each public-facing claim as accuracy-driven vs identity-expressive. [SOURCE: Kahan et al. 2017] |
| XDISC-AGS-01 | Agenda-setting/priming | Separate salience, attribute framing, priming/evaluation criteria, issue ownership, and elite cueing; ask whether perceived share is bottom-up or messaging-driven. | Retrodicts salience shifts without matching ground-condition changes. Probe: decompose one "why salient now" story into agenda/prime/frame/owner rows. [SOURCE: McCombs & Shaw 1972; Petrocik 1996] |
| XDISC-POL-01 | Agenda process (MSF) | Ask why this issue is salient now: indicator change, focusing event, policy entrepreneur, media frame, or coalition opening. Tag MSF output as narrative/process, not causal identification. | Retrodicts surge-era timing errors as process hypotheses only. Probe: problem/policy/politics stream table. [SOURCE: Kingdon/MSF literature; framework/book anchor, not DOI-verified in this pass] |
| XDISC-NAR-01 | Causal-story audit | For each narrative, name cause type: mechanical, accidental, intentional, inadvertent. Ask who becomes victim, villain, beneficiary, and fixer. Name one absent frame and one observation that would distinguish frame-effect from null. | Retrodicts overstrong "backlash" and "system collapse" language. Probe: annotate one public-facing paragraph. [SOURCE: Stone 1989] |
| XDISC-NAR-02 | Frame function | For each paragraph, identify problem definition, causal interpretation, moral evaluation, and treatment recommendation. Fail if the frame cannot be falsified or contrasted with an absent frame. | Retrodicts hidden policy conclusion drift. Probe: Entman-frame one memo section before publishing. [SOURCE: Entman 1993] |
| XDISC-NAR-03 | Deservingness | Score implicit deservingness criteria by migrant category: control, attitude, reciprocity, identity, and need. | Retrodicts refugee-vs-economic-migrant splits and legality/deservingness shortcuts. Probe: tag one public paragraph. [SOURCE: van Oorschot 2000] |
| XDISC-NAR-04 | Steelman symmetry | Each sweep emits one pro-immigration and one restrictionist steelman that the other side would accept as fair; fail convergence if either is missing or strawmanned. | Retrodicts selection toward the house frame. Probe: store both steelmen as rows before thesis burst. [INFERENCE] |
| XDISC-ADV-01 | Pro-immigration steelman | Mirror the restrictionist S cluster by forcing the best destination-capacity-aware pro-immigration case: global gains, innovation, dynamism, humanitarian legitimacy, and rule-designed absorptive capacity. | Retrodicts why restrictionist steelmanning alone can bias the generator menu. Probe: write the strongest pro case and its own falsifiers before critique. [INFERENCE] |
| XDISC-CAU-01 | DAG/confounder gate | Before any causal mechanism claim, sketch treatment, outcome, confounders, mediators, colliders, and post-treatment variables. | Retrodicts overread county/surge associations and bad-control risks. Probe: one DAG line before one regression interpretation. [SOURCE: `research/immigration-costs-causal-analysis.md`] |
| XDISC-MEAS-01 | Legal-status/arrival measurement | For any unauthorized/recent-arrival claim, state how legal status, YOEP, country of birth, citizenship, and household linkage are observed or imputed. | Retrodicts ICE docket denominator and school universe bugs. Probe: measurement row for each headline subgroup. [SOURCE: `research/immigration-conclusion-audit-running-fixes.md`] |
| XDISC-PIPE-01 | View/unit drift | For any derived table or view, assert units, withheld rows, denominator universe, and source build commit before exporting a headline. | Retrodicts F-33 thousands bug, withheld school net, and generator count drift. Probe: fail if view units are not machine-checked. [SOURCE: `research/immigration-conclusion-audit-running-fixes.md`] |
| XDISC-DS-01 | Estimand classifier | Blocking check: label every load-bearing claim as descriptive, causal, welfare, forecast, mechanism, or narrative. Claims cannot borrow confidence across labels. | Retrodicts non-significance != zero and observed justice rates != true offending. Probe: fail a memo table if any load-bearing row lacks an estimand. [SOURCE: `notes/quant-bias-checklist.md`] |
| XDISC-DS-02 | Universe twin | Blocking check: for every ratio, print numerator universe, denominator universe, sample frame, time window, and missingness/attrition. | Retrodicts school numerator/full-microsim denominator mismatch and ICE docket denominator fix. Probe: fail any row where universes differ without label. [SOURCE: `research/immigration-conclusion-audit-running-fixes.md`] |
| XDISC-RSI-01 | Generator yield loop | After each sweep, record which generators fired, which produced adopted changes, which produced no output, and which should retire. | Retrodicts current Markdown/header/DuckDB generator count mismatch. Probe: add `status`, `last_fired`, `adopted_outputs`, `retirement_counter`. [INFERENCE] |

### Dedup/load gate before registry adoption

Do not bulk-load XDISC into `lifetime_generators`. First add a `duplicates_g_lif` or `supersedes` field and keep only net-new prompts as registry rows. Probable overlaps from review:

| XDISC row | Existing overlap to check |
|---|---|
| ECO-02 | `G-LIF-C01`, `G-LIF-K01`, `G-LIF-O01` |
| MIC-01 | `G-LIF-B01`, `G-LIF-B04`, `G-LIF-F02` |
| URB-02 | `G-LIF-E01`, partial `G-LIF-E03` |
| DS-02 | `G-LIF-Q*`, `G-LIF-N*`, `G-LIF-K01` |
| INST-01 | `G-LIF-C02`, `G-LIF-J*`, `G-LIF-P02` |

Candidate net-new families: `MIC-02`, `MIC-03`, `MAC-*`, `URB-01/03/04/05`, `PE-*`, `PSY-*`, `AGS-01`, `POL-01`, `NAR-*`, `ADV-01`, `CAU-01`, `MEAS-01`, `PIPE-01`, `DS-01`, `RSI-01`. [INFERENCE]

---

## Self-prompt packet

Use this as the agent's self-prompt before and after research sweeps.

### Before divergence

1. What thesis am I tempted to prove?
2. What would make that thesis false on a different ledger layer, time horizon, geography, or welfare function?
3. Which denominator, sample universe, or unit conversion would flip the sign?
4. What is the policy target, and what is the instrument? Are multiple targets being laundered into one instrument?
5. What public-goods rule, descendant boundary, discount rate, and projection horizon would flip the fiscal sign?
6. Which identification strategy is actually present: descriptive correlation, shift-share/enclave, event study, factor-proportions, or none?
7. Which discipline would object first: public finance, labor micro, macro, urban economics, psychology, political science, law/admin, or data engineering?
8. What would a fair restrictionist and a fair open-borders advocate each accept as bad news?

### During search

1. Run one rightward and one leftward debias pass; do not let either become the synthesis.
2. For every source, extract one parameter, one identification limit, one narrative move, and one missing counterfactual.
3. Stop a source path when it no longer changes a claim, generator, dataset acquisition, or falsifier.
4. If a source only restates a known generator, cite it as support but do not create a duplicate generator.

### Before convergence

1. Which active thesis got demoted? If none, suspect selection.
2. Which generator produced a new artifact, and which produced no adopted output?
3. Which disagreement is a data fight, and which is a frame/welfare-function fight?
4. Does the final narrative state what data cannot kill because it is a different layer?
5. What is the next cheapest probe that can falsify the highest-impact remaining claim?

---

## Generator Sub-Loop Flowchart

This flowchart expands steps 3-5 of `research/immigration-knowledge-delta-agent-loop-2026-06-16.md`. It helps mechanize stale-narrative interruption, search-axis generation, and overclaim catching; it is not a standalone replacement for the umbrella loop.

```
START
  |
  v
1. Load live state
   - topic index, current thesis, generator registry, running fixes, DuckDB tables
   - write down the current thesis before new evidence
   - assert MD headings == DuckDB rows == header count, or mark [DEGRADED]
   - load dead-paths/aborted probes so the agent does not repeat known-failed searches
  |
  v
2. Classify the question
   - descriptive / causal / welfare / forecast / narrative / implementation
   - choose the ledger layer and unit of analysis
  |
  v
3. Generate alternatives before search
   - run at most 8 generators/sweep
   - include >=1 denominator/unit, >=1 local/urban, >=1 pro-immigration or restrictionist steelman,
     >=1 psychology/narrative/political generator, and DS-01 on every load-bearing number
  |
  v
4. Retrodiction gate
   - keep generators that explain >=2 prior findings/misses on a held-out slice
   - also require >=1 negative-space item no existing generator names
   - reject one-off topic ideas without mechanism
  |
  v
5. Probe cheaply
   - one SQL slice, one PDF/page check, one denominator check, one source quote/parameter
   - abort or redirect if the probe contradicts the plan
  |
  v
6. Mine evidence
   - extract parameter claims, identification limits, assumptions, and narrative frames
   - tag every load-bearing claim with canonical provenance tags from notes/provenance-tags.md
  |
  v
7. Converge
   - update layered theory
   - run five mechanism models
   - write three disconfirmation hunts
   - separate data-resolvable fights from frame-resolvable fights
  |
  v
8. Narrative audit
   - Entman frame: problem / cause / moral evaluation / treatment
   - Stone causal story: victim / villain / fixer / cause type
   - slogan inversion: how each side would overquote this
  |
  v
9. Update durable artifacts
   - thesis memo, generator registry or generator-audit memo, running fixes, index
   - never leave a confirmed no-downside fix as an offer
   - write registry + DuckDB + fixes atomically or mark the sweep incomplete
  |
  v
10. RSI / yield accounting
   - fired? adopted output? false lead? retired?
   - adoption must be judged by a separate pass or artifact diff, not the generator author alone
   - manual until lifecycle sidecar or DuckDB fields exist
   - two dry applicable sweeps parks a generator; retirement is manual
   - if a human correction repeats, turn it into a generator, hook, or checklist row
  |
  v
STOP after 2 consecutive sweeps with zero adopted outputs, or when the budget/max-sweep cap is reached.
Otherwise LOOP.
```

---

## Implementation recommendation

Do **not** add a global hook yet. The process gap is real, but the first fix is to add a loaded generator-lifecycle table or a YAML/CSV sidecar and run it manually for one more sweep. A hook is justified only after the same generator-lifecycle miss repeats. [INFERENCE]

Minimum schema:

```text
generator_id
family
prompt
retrodicts
negative_space
first_probe
source_grade
duplicates_g_lif
applicable_corpus
status              # active | parked | retired
fired_count          # produced >=1 candidate
dry_count            # fired while applicable, zero adopted
adoption_attributions
adoption_judge
last_integrity_check
notes
```

Next concrete run:

1. Run `XDISC-URB-01` through `XDISC-URB-05` over the school/housing/capacity memos.
2. Run `XDISC-PE-01`, `XDISC-PE-02`, `XDISC-PSY-*`, `XDISC-AGS-01`, and `XDISC-POL-01` over the surge/political-response memos.
3. Run `XDISC-DS-01` and `XDISC-DS-02` over every remaining headline ratio in the current verified-findings/confidence-ladder surface.
4. Reconcile `research/immigration-lifetime-fiscal-generators.md` counts against DuckDB before depending on counts in automation; current MD-only IDs are `G-LIF-Q06` and `G-LIF-S15`.

## Review disposition

Reviewer packets:

- `.model-review/2026-06-16-immigration-thesis-generator-audit/` — initial generator-audit Opus/Cursor lanes.
- `.model-review/2026-06-16-final-immigration-review/` — final post-cleanup Opus/Cursor lanes.

Accepted from Opus/Cursor review:

1. Public-goods rule, descendant boundary, discount rate, and NPV horizon need explicit generators.
2. Shift-share/enclave identification and labor-supply surplus/distribution prompts were missing.
3. Ostrom/common-pool language was too broad for schools/courts/shelters; use congestible club/local public goods unless the resource is genuinely common-pool.
4. Political-economy, sociotropic-vs-egocentric attitudes, motivated reasoning, agenda-setting/priming, deservingness, and symmetric pro-immigration steelman generators were missing.
5. Retrodiction-only gating and two-cycle retirement are unsafe; use held-out retrodiction + novelty, park rather than retire, and judge adoption separately.
6. XDISC must deduplicate against existing `G-LIF-*` rows before loading into a registry.

Deferred:

1. A DuckDB lifecycle migration is not included in this memo patch; it needs a build-path change, not prose-only edits.
2. A global hook is deferred until repeated misses justify it.
3. The full source upgrade for every political-economy citation should happen before registry load; rows marked `[INFERENCE; verify source before registry load]` are not ready as cited source claims.

---

## Sources used for generator expansion

- Tinbergen policy target/instrument logic: `https://www.elibrary.imf.org/downloadpdf/journals/024/1968/003/article-A001-en.pdf`; `https://garfield.library.upenn.edu/classics1986/A1986C401200001.pdf`
- Tiebout local public goods/sorting: `https://fbaum.unc.edu/teaching/PLSC541_Fall08/tiebout_1956.pdf`; `https://www.journals.uchicago.edu/doi/10.1086/257839`
- Manski reflection/social effects: `https://users.econ.umn.edu/~holmes/class/2003f8601/papers/manksi_reflection.pdf`; `https://academic.oup.com/restud/article-abstract/60/3/531/1570385`
- Roback spatial equilibrium: `https://matthewturner.org/ec2410/readings/Roback_JPE_1982.pdf`; `https://www.journals.uchicago.edu/doi/abs/10.1086/261120`
- Saiz housing supply elasticity: `https://joeornstein.github.io/pols-4641/readings/Saiz%20-%202010-%20The%20Geographic%20Determinants%20of%20Housing%20Supply.pdf`; `https://econpapers.repec.org/RePEc%3Aoup%3Aqjecon%3Av%3A125%3Ay%3A2010%3Ai%3A3%3Ap%3A1253-1296.`
- Moretti local multipliers: `https://eml.berkeley.edu/~moretti/multipliers.pdf`; `https://www.aeaweb.org/articles?id=10.1257%2Faer.100.2.373`
- Hsieh & Moretti housing constraints/spatial misallocation: `https://eml.berkeley.edu/~moretti/growth.pdf`; `https://www.aeaweb.org/articles?id=10.1257%2Fmac.20170388`
- Diamond sorting/amenities: `https://matthewturner.org/ec2410/readings/Diamond_AER_2016.pdf`; `https://www.aeaweb.org/articles?id=10.1257%2Faer.20131706`
- National Academies immigration fiscal report: `https://nap.nationalacademies.org/catalog/23550/the-economic-and-fiscal-consequences-of-immigration`
- Borjas immigration surplus: `https://www.aeaweb.org/articles?id=10.1257/jep.9.2.3`
- Card immigrant inflows/local labor markets: `https://davidcard.berkeley.edu/papers/immig-inflows.pdf`
- Goldsmith-Pinkham, Sorkin & Swift shift-share critique: `https://www.aeaweb.org/articles?id=10.1257/aer.20181047`
- Ottaviano & Peri immigrant/native substitution: `https://academic.oup.com/jeea/article-abstract/10/1/152/2297898`
- Buchanan club goods: `https://www.jstor.org/stable/2552442`
- Kerr & Lincoln high-skill innovation: `https://www.nber.org/papers/w15768`
- Hunt & Gauthier-Loiselle immigration and innovation: `https://www.aeaweb.org/articles?id=10.1257/mac.2.2.31`
- Ostrom social-ecological systems/resource governance: `https://www.science.org/doi/10.1126/science.1172133`; `https://pubmed.ncbi.nlm.nih.gov/19628857/`
- Pettigrew & Tropp intergroup contact meta-analysis: `https://pubmed.ncbi.nlm.nih.gov/16737372/`; `https://ideas.wharton.upenn.edu/wp-content/uploads/2018/07/Pettigrew-Tropp.pdf`
- Quillian perceived group threat: `https://www.semanticscholar.org/paper/Prejudice-as-a-response-to-perceived-group-threat%3A-Quillian/d4ceb81eb7a2e67d10db27545b8f2ec6c2702cd7`; `https://perception.org/other-publications/prejudice-as-a-response-to-perceived-group-threat-population-composition-and-anti-immigrant-and-racial-prejudice-in-europe/`
- Alesina, Miano & Stantcheva on immigration and redistribution perceptions: `https://www.nber.org/papers/w24733`; `https://doi.org/10.3386/w24733`
- Grigorieff, Roth & Ubfal on information and immigrant attitudes: `https://doi.org/10.1007/s13524-020-00882-8`
- Hainmueller & Hopkins public attitudes review: `https://www.annualreviews.org/content/journals/10.1146/annurev-polisci-102512-194818`
- Kahan motivated numeracy: `https://doi.org/10.1017/bpp.2016.2`
- Alesina & Stantcheva diversity/immigration/redistribution overview: `https://doi.org/10.1257/pandp.20201088`
- Alesina & Glaeser diversity/redistribution: `https://academic.oup.com/book/36351`
- Putnam diversity/social capital: `https://onlinelibrary.wiley.com/doi/10.1111/j.1467-9477.2007.00176.x`
- McCombs & Shaw agenda setting: `https://academic.oup.com/poq/article-abstract/36/2/176/1853310`
- Petrocik issue ownership: `https://www.jstor.org/stable/2111797`
- van Oorschot deservingness criteria: `https://www.tandfonline.com/doi/abs/10.1080/713701159`
- Entman framing: `https://fbaum.unc.edu/teaching/articles/J-Communication-1993-Entman.pdf`; `https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1460-2466.1993.tb01304.x`
- Stone causal stories: `https://www.uvm.edu/~dguber/POLS293/articles/stone.pdf`; `https://academic.oup.com/psq/article/104/2/281/7134156`
- Multiple Streams/Kingdon overview and refinement: `https://pmc.ncbi.nlm.nih.gov/articles/PMC8861624/`; `https://www.cambridge.org/core/elements/multiple-streams-and-policy-ambiguity/FBA20248D4A359D38AF7083D00F5149E`
