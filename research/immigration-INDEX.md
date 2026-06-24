# Immigration — Topic Index

Files the agent should consult before acting. Start with Core State, then branch by question.

Instrument note: this topic is politically charged and much of the synthesis is LLM-assisted. Treat this index as a routing layer, not as a neutral substitute for the cited artifacts. Consult `notes/llm-bias-caveat.md` before writing headline claims.

## Core State

| File | Topic | Consult before |
|------|-------|----------------|
| `immigration-main-question-reset.md` | What the repo is actually trying to answer | Reframing the project or proposing new scope |
| `immigration-evidence-base-audit.md` | Which claims are well-supported vs thin | Repeating literature claims or writing summaries |
| `immigration-verified-findings-report-2026-04-10.md` | Verified findings snapshot, June-scoped by running fixes | Answering "what do we know?" after checking the June delta/fixes |
| `immigration-confidence-ladder.md` | Claim confidence by tier | Making strong claims or publishing conclusions |
| `immigration-claims-evolution-ledger-2026-04-23.md` | Claim-by-claim evolution ledger with takeaways and recurring misunderstandings | Asking how the immigration claims changed or how they relate |
| `immigration-glossary.md` | Definitions and term discipline | Using terms like `unauthorized`, `low-skill`, `surge`, `fiscal` |
| `immigration-epistemic-check.md` | Framing-sensitive guardrails | Politically charged synthesis |
| `immigration-economist-effects-matrix.md` | What economists are actually pricing vs omitting | Comparing Smith, Decker, Borjas, Clark poll economists |
| `immigration-fiscal-welfare-ledger-map.md` | **Unifying map** — "positive vs negative?" decomposed into 4 coordinates × the full fiscal+benefit ledger set; maps generator clusters A–U | **Answering "is low-skill immigration good/bad?"**; before quoting any single sign |
| `immigration-source-incentive-regrade-2026-06-23.md` | **Against-interest re-grade** — discounts advocacy (FAIR/ITEP/Cato/CIS) both sides, rewards against-interest (Borjas surplus, NAS cost); `source_incentive_grades` | Weighting a source by prominence/citation; trusting media framing over primary tables |
| `immigration-dataset-register.md` | Use-case-oriented data register | Asking "what data do we have?" |
| `immigration-dataset-roadmap.md` | **Acquisition roadmap** — 12 verified datasets we *don't* have yet, chosen to fill the crime + benefit-side gaps | Asking "what data should we get next?"; planning acquisition |
| `immigration-verification-handoff.md` | Verification map: repo files, datasets, paper families, disciplines | Handing the topic to another agent |
| `immigration-friend-reproduce-guide.md` | **Clone → build → read → query** for a human collaborator | Sharing reasoning + reproduction steps |
| `immigration-conclusion-audit-running-fixes.md` | Live overclaim/denominator/layer fix ledger | Auditing conclusions, applying XDISC-DS-02, checking what changed on 2026-06-16 |

## Fiscal Ledger

| File | Topic | Consult before |
|------|-------|----------------|
| `immigration-fiscal-impact-unauthorized-memo.md` | Main fiscal memo: federal/state-local split, wage debate, child-attribution dispute | Any fiscal bottom line |
| `immigration-full-spectrum-costs-unauthorized-memo.md` | Non-ledger costs: congestion, courts, labor-law erosion, backlash | Claiming "hidden" costs beyond taxes/transfers |
| `immigration-unified-scenarios-memo.md` | Scenario comparison across methods | Converting arguments into a bounded range |
| `immigration-costs-causal-analysis.md` | DAG and causal-path discipline | Proposing controls, mediators, or attribution rules |
| `immigration-state-local-cost-examples-ny-ca-tx.md` | Concrete state/local examples | Generalizing from national ledgers to local burden |
| `immigration-household-weighted-correction.md` | Household vs person correction issues | Reusing external figures without checking unit of analysis |
| `immigration-nas-scope-and-bias-update-2026-04-10.md` | What NAS does and does not cover | Treating NAS as final or complete |
| `immigration-adversarial-review.md` | Strongest case against our own position | Closing out a conclusion or writing a public-facing memo |

## Data Stack

| File | Topic | Consult before |
|------|-------|----------------|
| `immigration-lifetime-fiscal-data-stack-2026-04-10.md` | Minimum viable and gold-standard lifetime model stack | Saying ACS alone is enough |
| `immigration-country-fiscal-tensor-2026-06-15.md` | **Built** country fiscal tensor + rollup anchors (union DuckDB) | Querying population × layer × order |
| `immigration-borjas-supply-shock-panel-2026-06-23.md` | **Built** real 1980–2023 immigrant-share-by-skill panel from IPUMS census/ACS (`borjas_supply_shock_panel`); <HS share 9.8%→40.8% | Citing the supply-shock *quantity*; do NOT read it as a wage verdict (that's the Card-vs-Borjas debate) |
| `immigration-federal-distribution-findings-2026-06-15.md` | Distribution pass — school units, federal proxy white vs Mexico | “Do whites pay multiples?” |
| `immigration-europe-caucasian-fiscal-findings-2026-06-15.md` | **EU27 / UK / Caucasian natives / low-skill corridors** — federal proxy + matched-education | “European immigrants vs white Americans”; corridor A vs B |
| `immigration-school-burden-per-adult-2026-06-15.md` | **per_pupil × kids/adult** — three-layer annual (`v_three_layer_annual`) | “Did you multiply child burden?” |
| `immigration-sweep-cycles-13-22-2026-06-15.md` | Diverge/synthesis cycles 13–22 (school burden build) — **rushed SQL pass, superseded by 23–32 and same-universe guard; do not cite old `$771/+748` origin school/net rows** | Historical thesis burst only |
| `immigration-sweep-cycles-23-32-2026-06-15.md` | **Full protocol** sweeps 23–32: NAS college+ NPV, school weights, lifetime flip, converge; origin school/net rows partly superseded by same-universe guard | Post-rebuild thesis; three-layer + lifetime; do not cite old `$771/+748` origin school/net rows |
| `immigration-mexico-npv-population-synthesis-2026-06-15.md` | **Mexico NPV multiply-out**, ACS denominator, Biden stock vs encounters, **full ledger stack (Q+R)** | "Reported Mexicans"; "10M illegals"; NAS ≠ net fiscal |
| `immigration-restrictionist-arguments-steelman-2026-06-15.md` | **Steel-man** restrictionist chains: Borjas, BGH, NAS/Orrenius, Gould, Razin, FAIR | Arguing against immigration; follow their logic |
| `immigration-restrictionist-corpus-parse-2026-06-15.md` | **Full marker-modal parse** of 8 restrictionist PDFs → perspectives, narratives, generators S06–S14 | Deep read of restrictionist corpus; generator mining |
| `immigration-restrictionist-corpus-full-extract-2026-06-15.md` | **Section-by-section full read** of all 9 papers (~220 claims, 62 sections) | Authoritative claim register after full parse |
| `immigration-restrictionist-dataset-integration-2026-06-15.md` | **Paper → dataset → DuckDB** map; Tier A–C acquire list | Planning integration after restrictionist corpus read |
| `immigration-lifetime-country-approx-brainstorm-2026-06-15.md` | Brainstorm: country lifetime +/- with 1st/2nd/3rd order stacks | Designing country rollup without scalar lies |
| `immigration-lifetime-dataset-brainstorm-2026-06-15.md` | Brainstorm + tier map for lifetime proxies; `setup-lifetime.sh` acquisition | Picking datasets for lifetime NPV calibration |
| `immigration-lifetime-fiscal-generators.md` | 563 DuckDB parameter claims; 106 MD / 104 DuckDB generators (MD-only Q06, S15) | Negative-space sweeps, unnamed-assumption audits |
| `immigration-thesis-generator-audit-2026-06-16.md` | Cross-disciplinary generator/self-prompt audit (economics, micro/macro, urbanism, psychology, narrative) | Running divergence/convergence loops; asking what to search next |
| `immigration-knowledge-delta-agent-loop-2026-06-16.md` | Two-day delta + parent-controlled agent loop (claim inventory → probe → converge → review) | Starting a full immigration research epoch; pairing with generator audit |
| `immigration-lifetime-unified-theory-2026-06-15.md` | **Living synthesis** — unified theory + 5 formal models + critique matrix (update each sweep) | After every corpus round; before next download burst |
| `../notes/immigration-lifetime-sweep-protocol.md` | Mandatory post-sweep workflow (theory → 5 models → thesis burst → disconfirm → round N+1) | Structuring research cycles |
| `../notes/immigration-lifetime-synthesis-diverge-cookbook.md` | **Prompt template / cookbook** — full diverge↔converge loop, subagent JSON schema, synthesis prompt | Running sweeps; adapting to new topics |
| `immigration-public-data-acquisition-2026-04-11.md` | What public files were actually staged locally | Assuming a dataset has been acquired |
| `immigration-origin-data-stack.md` | Origin/destination and ontology layer | Making claims by origin mix |
| `immigration-next-data-upgrades.md` | Highest-value missing acquisitions | Planning the next data tranche |
| `immigration-net-negative-dataset-frontier-2026-06-15.md` | Datasets to test net-negative fiscal/local-cost claims (+ disconfirmation) | Building cost ledger or federal microsim |
| `immigration-scenario-composition-2026-06-15.md` | Integrated SIPP+MEPS+federal+local scenario ledgers | Cell-level fiscal reasoning; not scalar verdict |
| `immigration-frontier-data-acquisition-2026-04-11.md` | Stage 4 local-capacity acquisition pass: `SAIPE`, court/interpreter docs, and NCES CCD file-tool artifacts | Building school-service or court-friction modules |
| `immigration-school-service-complexity-2026-04-11.md` | Built district/state school-side context layer from `SAIPE` + school finance + current NCES directory, plus bounded `ELSi` probe | Doing district school-burden or school-service-complexity analysis |
| `immigration-surge-threshold-dataset-frontier-2026-04-21.md` | Dataset frontier and research designs that can actually identify surge and threshold effects | Asking what data and empirical design would settle nonlinear local-capacity questions |
| `immigration-prototype-progress.md` | Current prototype state | Claiming the model is further along than it is |
| `immigration-public-mvp-readiness-2026-04-11.md` | What is ready for a public-use MVP | Shipping a simplified public model |
| `immigration-public-mvp-meps-module-2026-04-11.md` | Built MEPS health-cost module for the public MVP | Using MEPS-derived health-cost outputs |
| `immigration-public-mvp-sipp-meps-bridge-2026-04-11.md` | Completed SIPP-to-MEPS bridge and expected-health output | Integrating transition and payer-incidence profiles |
| `immigration-education-bucket-stock-and-lifetime-status-2026-04-11.md` | Weighted ACS stock cut by education bucket plus current lifetime-estimate status | Asking for `<HS` / `HS` / `some college` counts or state shares |
| `immigration-local-burden-puma-layer.md` | PUMA/local burden layer | Moving from state averages to sub-state analysis |
| `immigration-stage2-county-bridge-batch.md` | County bridge build status | County-level joining or school/housing overlays |

## Interpretation & External Debate

| File | Topic | Consult before |
|------|-------|----------------|
| `immigration-clark-respondent-audit.md` | How to read the Clark poll without overclaiming | Saying "economists agree" |
| `immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md` | Unified comparative audit with one quantitative framework across all three commentators | Wanting a more decisive first-principles comparison |
| `immigration-claims-matrix-2026-04-11.md` | One-page verified/inferred/unresolved claim ledger for artifacts and commentators; 2026-06-16 scoped to quick ledger, not latest tensor | Making a quick final assertion; confirm latest fiscal/school rows in verified findings and running fixes |
| `immigration-david-d-friedman-claims-audit-2026-04-11.md` | Named audit of David D. Friedman claims with a first-principles quantitative pass | Checking libertarian open-borders arguments against the repo and official sources |
| `immigration-bryan-caplan-claims-audit-2026-04-21.md` | Claim-by-claim audit of Bryan Caplan with a causal graph tying his optimistic channels to current surge, housing, fiscal, and political-response evidence | Evaluating Caplan directly rather than treating him as generic open-borders rhetoric |
| `immigration-economist-one-pager-2026-04-22.md` | Short public-facing one-pager on why the strongest pro-immigration economics rhetoric keeps answering the wrong question | Needing a concise forwardable version rather than a full memo |
| `immigration-economist-debate-sheet-2026-04-22.md` | Quote-driven debate sheet mapping economist claims to the hidden move, failure mode, and strongest repo-backed counter | Wanting direct quotes and fast counters for debate or adversarial writing |
| `immigration-economist-rhetorical-failures-2026-04-22.md` | Bounded memo on the strongest fair critique of mainstream pro-immigration economics rhetoric: ledger switching, upper-bound laundering, marginal-to-mass extrapolation, capacity erasure, denominator masking, and political-economy underspecification | Asking how to kill the strongest economist arguments without overclaiming beyond the repo's current evidence |
| `immigration-noah-smith-nicholas-decker-claims-audit-2026-04-11.md` | Named audit of Noah Smith and Nicholas Decker claims | Checking pundit or commentator claims against the repo and official sources |
| `immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md` | Audit of the Open Borders “double world GDP” slogan, cited papers, repo capacity constraints, and apartheid framing | Evaluating classic open-borders macro claims or apartheid analogies |
| `immigration-threshold-first-panel-2026-04-21.md` | First joined-data threshold pass using BPS permits, HUD PIT/HIC, election shift, and receiver-city costs | Asking whether threshold effects are measurable in current public data |
| `immigration-threshold-causal-levers-2026-04-21.md` | Deeper normalized pass identifying which levers actually move political response and receiver stress | Asking what the real causal levers are after joining threshold datasets |
| `immigration-low-skill-origin-incidence-memo.md` | Why origin mix and household structure matter | Treating low-skill immigration as one undifferentiated object |
| `immigration-fiscal-deceptive-data-reading-pack.md` | Common bad-faith or sloppy readings of the data | Debunking a chart, thread, or pundit claim |
| `immigration-fiscal-camarota-cis-testimony-audit.md` | Restrictionist benchmark audit | Using CIS/Camarota as baseline evidence |
| `immigration-crime-rates-unauthorized-vs-native-born.md` | Crime-rate evidence review | Mixing crime claims into a fiscal memo |
| `immigration-agi-reframing.md` | Off-mainline strategic reframing | Pulling the project into speculative macro territory |

## Causal-design layer (2026-04-18)

| File | Topic | Consult before |
|------|-------|----------------|
| `immigration-causal-synthesis-2026-04-18.md` | Cycle synthesis: Saiz × E-Verify findings, observed mandate-margin wage read; not global Card-vs-Borjas verdict | Citing the bounded E-Verify wage result or Saiz rent screen |
| `immigration-causal-everify-card-vs-borjas.md` | E-Verify staggered TWFE on QWI 2003-2023, native low-skill wages | Citing Borjas wage prediction for the U.S. policy variation |
| `immigration-causal-saiz-elasticity-rent.md` | Saiz 2010 housing supply elasticity × ACS rent + foreign-born | Treating PUMA rent burden as elasticity-neutral |
| `immigration-causal-paradigm-escape-synthesis-2026-04-18.md` | Evening cycle synthesis: 5 verdict updates, 8-finding ladder | Writing the headline immigration position; asking "what changed?" |
| `immigration-causal-internal-vs-immigrant-newcomers.md` | IRS SOI × ACS moved-from-abroad flow comparison for “newcomer burden” | Treating "newcomer burden" as immigration-driven by default |
| `immigration-causal-surge-2021-2024.md` | OHSS encounters + CHNV + city costs + 2024 election: surge analysis | Extrapolating pre-2020 findings to surge magnitudes; discussing 2024 election in immigration terms |
| `immigration-county-outcome-panel-2026-04-21.md` | QCEW + IRS domestic migration + threshold spine: county wages, employment, domestic migration, and political response in one frame | Reusing the county outcome panel while remembering the IRS layer is not native-incumbent-only |
| `immigration-capacity-frontier-2026-04-21.md` | Stock vs flow vs flow-to-capacity comparison, threshold robustness grid, and a clearer statement of what still remains open on subgroups, voting, welfare, and receiver counterfactuals | Asking what is actually left to check after the first county threshold passes |
| `immigration-capacity-falsification-2026-04-21.md` | Corrected falsification pass with clean `2017–2018` and `2018–2019` annual pre-COVID windows, `1,000`-draw permutation inference, division/state leave-out, explicit window metadata, and wage-threshold null benchmarking | Asking which parts of the new flow-capacity story still survive after fixing the earlier placebo bug |
| `immigration-reasoning-evolution-2026-04-21.md` | Narrative provenance trace of how the repo’s immigration reasoning changed, including the `/critique close` correction and later downgrade that left the annual wage/employment split unresolved | Wanting the evolution of reasoning itself traced rather than only the latest stance |
| `immigration-frontier-rethink-2026-04-22.md` | Zoomed-out rethink after the corrected falsification pass; demotes the annual county panel to a screening surface and ranks the better next frontiers | Asking where the research should go once county threshold work hits diminishing returns |
| `immigration-receiver-failure-atlas-2026-04-22.md` | Receiver-node overload atlas joining shelter load, permits, spending, and political shift from `2018–2024` | Asking what the actual local failure nodes look like once counties stop being the main causal object |
| `immigration-resident-weighted-exposure-2026-04-22.md` | Resident-, renter-, and child-weighted correction to the newcomer and stress-exposure framing | Asking what the typical resident or renter is exposed to rather than what the median county looks like |
| `immigration-open-borders-break-even-bounds-2026-04-22.md` | Converts the repo’s conservative open-borders calibration into explicit break-even loss bounds and housing-absorption requirements | Asking how much destination-country degradation would be needed to wipe out global gains |
| `immigration-receiver-counterfactuals-2026-04-22.md` | National-CoC synthetic-control style counterfactuals for `NYC`, `Denver`, `Boston`, `Chicago`, and `Bexar`, including ratio outcomes, absolute-load checks, and donor-pool exclusions | Asking whether the receiver-node stories survive a real donor-pool counterfactual rather than a local comparison |
| `immigration-receiver-data-acquisition-2026-04-23.md` | Staged 2024 ACS PUMS, EOIR Case Data 2026-0301, and QWI county-quarter receiver panel with hashes, limits, and next kill-test sequence | Asking what new datasets were acquired for the receiver-node/capacity theory |
| `immigration-receiver-node-kill-test-2026-04-23.md` | End-to-end nine-node kill test joining ACS 2024 exposure, PUMA bridge, EOIR broad/strict court pressure, QWI labor outcomes, shelter/capacity, and political shift | Asking whether the receiver-node theory survives the new data |

## Raw Data & Warehouse

| File | Topic | Consult before |
|------|-------|----------------|
| `../sources/immigration-fiscal/data/MANIFEST.md` | Raw-file manifest with paths and acquisition notes | Looking for a specific local file |
| `../warehouse/immigration_context.duckdb` | Main derived DuckDB warehouse (internal disk) | Querying state/origin/context data |
| `../sources/immigration-fiscal/data/derived/build_immigration_warehouse.py` | Warehouse rebuild script | Rebuilding or extending the DuckDB |
| `../sources/immigration-fiscal/data/derived/stage3_proto/` | Prototype local-context build outputs | Using tract/PUMA prototype artifacts |
| `../sources/immigration-causal/data/external/census_acs_2024_1yr/` | ACS 2024 PUMS person/household/dictionary staging with acquisition manifest | Building post-surge PUMA receiver exposure |
| `../sources/immigration-causal/data/derived/acs_2024_receiver_exposure/acs_2024_receiver_exposure_puma.parquet` | First ACS 2024 receiver-state PUMA exposure layer | Screening high-exposure PUMAs before county/metro joins |
| `../sources/immigration-causal/data/outcomes/analysis/receiver_node_kill_test/` | End-to-end receiver-node kill-test outputs | Comparing synchronized pressure across ACS, EOIR, shelter/capacity, QWI, and politics |
| `../sources/immigration-causal/data/external/eoir_case_data_2026_02/` | EOIR Case Data 2026-0301 archive and code key with acquisition manifest | Building immigration-court pressure panels |
| `../sources/immigration-causal/data/lehd/qwi_county_receiver_panel.parquet` | Repaired QWI county-quarter receiver-state panel, 2017Q1-2024Q4 | Joining labor outcomes to receiver stress panels |

## Quick Start

If the question is:

1. `What do we currently think?` Start with `immigration-knowledge-delta-agent-loop-2026-06-16.md`, then `immigration-conclusion-audit-running-fixes.md`, then `immigration-confidence-ladder.md`; use `immigration-verified-findings-report-2026-04-10.md` only with its June scoping notes.
2. `Is low-skill immigration good or bad for natives?` Start with `immigration-economist-effects-matrix.md`, then `immigration-fiscal-impact-unauthorized-memo.md`, then `immigration-full-spectrum-costs-unauthorized-memo.md`.
3. `What data do we have locally?` Start with `immigration-dataset-register.md`, then `../sources/immigration-fiscal/data/MANIFEST.md`.
4. `Can we model this ourselves?` Start with `immigration-lifetime-fiscal-data-stack-2026-04-10.md`, then `immigration-public-data-acquisition-2026-04-11.md`, then `immigration-frontier-data-acquisition-2026-04-11.md`, then the DuckDB build files.
5. `What is the current `<HS` / `HS` / `some college` stock split?` Start with `immigration-education-bucket-stock-and-lifetime-status-2026-04-11.md`.
6. `How do I run the next fiscal/generator sweep?` Start with `immigration-knowledge-delta-agent-loop-2026-06-16.md`, then `../notes/immigration-lifetime-synthesis-diverge-cookbook.md`, `../notes/immigration-lifetime-sweep-protocol.md`, `immigration-thesis-generator-audit-2026-06-16.md`, and `immigration-conclusion-audit-running-fixes.md`.

<!-- knowledge-index
generated: 2026-06-16T11:56:44Z
hash: manual-june-route-refresh

table_claims: 97

end-knowledge-index -->
