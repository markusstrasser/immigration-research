# Immigration — Topic Index

Files the agent should consult before acting. Start with Core State, then branch by question.

## Core State

| File | Topic | Consult before |
|------|-------|----------------|
| `immigration-main-question-reset.md` | What the repo is actually trying to answer | Reframing the project or proposing new scope |
| `immigration-evidence-base-audit.md` | Which claims are well-supported vs thin | Repeating literature claims or writing summaries |
| `immigration-verified-findings-report-2026-04-10.md` | Current verified findings snapshot | Answering "what do we know?" |
| `immigration-confidence-ladder.md` | Claim confidence by tier | Making strong claims or publishing conclusions |
| `immigration-glossary.md` | Definitions and term discipline | Using terms like `unauthorized`, `low-skill`, `surge`, `fiscal` |
| `immigration-epistemic-check.md` | Framing-sensitive guardrails | Politically charged synthesis |
| `immigration-economist-effects-matrix.md` | What economists are actually pricing vs omitting | Comparing Smith, Decker, Borjas, Clark poll economists |
| `immigration-dataset-register.md` | Use-case-oriented data register | Asking "what data do we have?" |
| `immigration-verification-handoff.md` | Verification map: repo files, datasets, paper families, disciplines | Handing the topic to another agent |

## Fiscal Ledger

| File | Topic | Consult before |
|------|-------|----------------|
| `fiscal-impact-unauthorized-immigration-research-memo.md` | Main fiscal memo: federal/state-local split, wage debate, child-attribution dispute | Any fiscal bottom line |
| `full-spectrum-costs-unauthorized-immigration-research-memo.md` | Non-ledger costs: congestion, courts, labor-law erosion, backlash | Claiming "hidden" costs beyond taxes/transfers |
| `immigration-unified-scenarios-memo.md` | Scenario comparison across methods | Converting arguments into a bounded range |
| `immigration-costs-causal-analysis.md` | DAG and causal-path discipline | Proposing controls, mediators, or attribution rules |
| `state-local-cost-examples-ny-ca-tx.md` | Concrete state/local examples | Generalizing from national ledgers to local burden |
| `immigration-household-weighted-correction.md` | Household vs person correction issues | Reusing external figures without checking unit of analysis |
| `immigration-nas-scope-and-bias-update-2026-04-10.md` | What NAS does and does not cover | Treating NAS as final or complete |
| `immigration-adversarial-review.md` | Strongest case against our own position | Closing out a conclusion or writing a public-facing memo |

## Data Stack

| File | Topic | Consult before |
|------|-------|----------------|
| `immigration-lifetime-fiscal-data-stack-2026-04-10.md` | Minimum viable and gold-standard lifetime model stack | Saying ACS alone is enough |
| `immigration-public-data-acquisition-2026-04-11.md` | What public files were actually staged locally | Assuming a dataset has been acquired |
| `immigration-origin-data-stack.md` | Origin/destination and ontology layer | Making claims by origin mix |
| `immigration-next-data-upgrades.md` | Highest-value missing acquisitions | Planning the next data tranche |
| `immigration-frontier-data-acquisition-2026-04-11.md` | Stage 4 local-capacity acquisition pass: `SAIPE`, court/interpreter docs, and NCES CCD file-tool artifacts | Building school-service or court-friction modules |
| `immigration-school-service-complexity-2026-04-11.md` | Built district/state school-side context layer from `SAIPE` + school finance + current NCES directory, plus bounded `ELSi` probe | Doing district school-burden or school-service-complexity analysis |
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
| `immigration-claims-matrix-2026-04-11.md` | One-page verified/inferred/unresolved claim ledger for current artifacts and commentators | Making a quick final assertion |
| `immigration-david-d-friedman-claims-audit-2026-04-11.md` | Named audit of David D. Friedman claims with a first-principles quantitative pass | Checking libertarian open-borders arguments against the repo and official sources |
| `immigration-noah-smith-nicholas-decker-claims-audit-2026-04-11.md` | Named audit of Noah Smith and Nicholas Decker claims | Checking pundit or commentator claims against the repo and official sources |
| `immigration-low-skill-origin-incidence-memo.md` | Why origin mix and household structure matter | Treating low-skill immigration as one undifferentiated object |
| `immigration-fiscal-deceptive-data-reading-pack.md` | Common bad-faith or sloppy readings of the data | Debunking a chart, thread, or pundit claim |
| `immigration-fiscal-camarota-cis-testimony-audit.md` | Restrictionist benchmark audit | Using CIS/Camarota as baseline evidence |
| `immigration-crime-rates-unauthorized-vs-native-born.md` | Crime-rate evidence review | Mixing crime claims into a fiscal memo |
| `immigration-agi-reframing.md` | Off-mainline strategic reframing | Pulling the project into speculative macro territory |

## Causal-design layer (2026-04-18)

| File | Topic | Consult before |
|------|-------|----------------|
| `immigration-causal-synthesis-2026-04-18.md` | Cycle synthesis: Saiz × E-Verify findings, Card-vs-Borjas verdict | Saying "Borjas vs Card is unresolved" or "rent exposure is just price discovery" |
| `immigration-causal-everify-card-vs-borjas.md` | E-Verify staggered TWFE on QWI 2003-2023, native low-skill wages | Citing Borjas wage prediction for the U.S. policy variation |
| `immigration-causal-saiz-elasticity-rent.md` | Saiz 2010 housing supply elasticity × ACS rent + foreign-born | Treating PUMA rent burden as elasticity-neutral |
| `immigration-causal-paradigm-escape-synthesis-2026-04-18.md` | Evening cycle synthesis: 5 verdict updates, 8-finding ladder | Writing the headline immigration position; asking "what changed?" |
| `immigration-causal-internal-vs-immigrant-newcomers.md` | IRS SOI × ACS — native county inflow is 33× immigrant inflow | Treating "newcomer burden" as immigration-driven by default |

## Raw Data & Warehouse

| File | Topic | Consult before |
|------|-------|----------------|
| `../sources/immigration-fiscal/data/MANIFEST.md` | Raw-file manifest with paths and acquisition notes | Looking for a specific local file |
| `../sources/immigration-fiscal/data/derived/immigration_context.duckdb` | Main derived DuckDB warehouse | Querying state/origin/context data |
| `../sources/immigration-fiscal/data/derived/build_immigration_context_duckdb.sql` | Warehouse build script | Rebuilding or extending the DuckDB |
| `../sources/immigration-fiscal/data/derived/stage3_proto/` | Prototype local-context build outputs | Using tract/PUMA prototype artifacts |

## Quick Start

If the question is:

1. `What do we currently think?` Start with `immigration-verified-findings-report-2026-04-10.md`, then `immigration-confidence-ladder.md`.
2. `Is low-skill immigration good or bad for natives?` Start with `immigration-economist-effects-matrix.md`, then `fiscal-impact-unauthorized-immigration-research-memo.md`, then `full-spectrum-costs-unauthorized-immigration-research-memo.md`.
3. `What data do we have locally?` Start with `immigration-dataset-register.md`, then `../sources/immigration-fiscal/data/MANIFEST.md`.
4. `Can we model this ourselves?` Start with `immigration-lifetime-fiscal-data-stack-2026-04-10.md`, then `immigration-public-data-acquisition-2026-04-11.md`, then `immigration-frontier-data-acquisition-2026-04-11.md`, then the DuckDB build files.
5. `What is the current `<HS` / `HS` / `some college` stock split?` Start with `immigration-education-bucket-stock-and-lifetime-status-2026-04-11.md`.

<!-- knowledge-index
generated: 2026-04-19T04:22:10Z
hash: 664d7e8f10d3

table_claims: 12

end-knowledge-index -->
