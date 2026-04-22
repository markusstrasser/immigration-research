# Research — Getting to the Truth

## Purpose
This repo pursues empirical questions with the rigor of investigative scholarship. Topics vary (currently IQ sex differences) but the methodology is constant: primary sources, competing interpretations, falsifiable claims, honest uncertainty.

## Constitution

### Generative Principle

> Maximize the rate at which claims converge toward ground truth, measured by the ratio of verified/falsified claims to total claims produced.

Truth is the objective. Not consensus, not novelty, not volume. A single well-sourced falsification is worth more than ten plausible syntheses. Error correction is the mechanism — every claim should be easier to kill than to keep alive.

### Principles

**1. Source everything.** No floating claims. Tag with `[SOURCE: url/citation]`, `[INFERENCE]`, `[TRAINING-DATA]`, or `[UNVERIFIED]`. Unsourced claims in research output are bugs.

**2. Steel-man before criticizing.** Present the strongest version of any position before evaluating it. If you can't articulate why smart people believe X, you don't understand X well enough to refute it.

**3. Distinguish levels of evidence.** Empirical fact > expert consensus > contested evidence > opinion > speculation. Label which level you're operating at. Don't dress speculation as fact.

**4. Disconfirmation is mandatory.** For every hypothesis, actively search for contradictory evidence before concluding. Output without disconfirmation is incomplete — structurally, not stylistically.

**5. Name the frame.** Analysis is always framed. State whose perspective you're presenting. Flag verdicts that depend on framing judgment vs hard data with `[FRAMING-SENSITIVE]`.

**6. Quantify when possible.** Vague qualifiers become numbers with citations. "Likely" vs "possible" vs "speculative" are different — say which, and ideally say how different.

**7. Flag the instrument's bias.** This research is conducted through an LLM. The model has systematic dispositions from post-training (see `notes/llm-bias-caveat.md`). On politically charged topics, acknowledge this. Don't pretend neutrality where the instrument isn't neutral.

### Autonomy Boundaries

**Autonomous:** conduct research, write memos, update docs index, save papers to corpus, run analyses on local data, commit findings.

**Propose first:** restructure the docs index, change the analysis protocol, modify the causal tree, reframe the central question.

**Never without human:** delete research files, publish or share findings externally, modify this constitution.

## Git Workflow

All commits to main. No branches.

```
[scope] Verb thing — why
```

Scopes: `[research]` (findings), `[analysis]` (data work), `[docs]` (index/notes), `[infra]` (tooling/config).

## Tools Available

### Skills (symlinked from `~/Projects/skills/`)

Research & evidence:
- **research** — one-shot research with source grading
- **research-ops** — autonomous research loops, knowledge compilation, training-data diff
- **bio-verify** — bio/medical/scientific claim verification with evidence hierarchy
- **analyze** — causal/DAG/hypotheses/forensic analysis modes
- **observe** — session retrospectives, architectural patterns, supervision audits
- **review** — adversarial review (model-review, verify, close)
- **brainstorm** — divergent ideation via systematic perturbation
- **negative-space-sweep** — discover what's MISSING from an optimized system
- **de-slop** — adversarial editor for AI-generated prose patterns

Workflow & project:
- **upgrade** — full codebase audit and improvement
- **improve** — harvest findings, suggest skills, maintain quality
- **goals** — project goals and constitutional principles elicitation
- **constitution** — constitution authoring for projects
- **entity-management** — versioned knowledge management for entities
- **trending-scout** — scan for new AI/agent developments

Data acquisition:
- **data-acquisition** — probe→stage→register pattern for external datasets (Census, NCES, PSID, MEPS, etc.)
- **census-data** — Census Data API + IPUMS extracts (ACS, CPS, SIPP, QWI variable codes)
- **youtube-transcript** — fetch video transcripts via yt-dlp (podcasts, interviews)
- **dataset-register** — standardize per-topic dataset catalogs

Infra & integrations:
- **browse** — persistent headless browser daemon
- **google-workspace** — Google Workspace automation (Drive, Sheets, Gmail, Calendar)
- **scientific-drawing** — Typst/CeTZ, TikZ, D2, Asymptote diagrams
- **modal** — Modal serverless Python cloud compute
- **llmx-guide** — llmx CLI routing and gotchas
- **model-guide** — frontier model selection and prompting

### MCP Servers (`.mcp.json`)
- **exa** — semantic web search, entity enrichment, deep research
- **research** (research-mcp) — Semantic Scholar, corpus management, claim verification, preprint surveillance
- **brave-search** — independent web index (triangulation with Exa)
- **agent-infra** — cross-project knowledge base (hook designs, agent patterns, research findings)
- **firecrawl** — web scraping and structured extraction
- **parallel** — deep web research via Parallel Task API (lite/core/ultra tiers)
- **context7** — library documentation lookup

## Structure

```
GOALS.md           — human-owned mission, strategy, success metrics (read at session start)
research/          — topic files, one per question or area
decisions/         — concept-level pivots, approach selections, methodology shifts
sources/           — archived source material, data files
notes/             — working notes, drafts, threads of analysis
```

## Decision Journal (`decisions/`)

Records of concept-level pivots — when an interpretation shifts, a methodology is adopted/dropped, a causal node gets resolved or reopened. One file per decision, `YYYY-MM-DD-slug.md`. Template in `decisions/.template.md`. Records use YAML frontmatter for machine-readable metadata (concept grouping, typed relations, provenance).

**When to write:** path-dependent interpretation choices, dropping a hypothesis after evidence, adopting a new dataset/method that forecloses alternatives, resolving a causal fork where the reasoning is costly to reconstruct. Do NOT write for: parameter tweaks, routine implementation, local execution details.

**Research memos:** when updating with revised understanding, add a dated `## Revisions` entry at the bottom linking to the triggering decision. Only for claim/interpretation/confidence changes — not for wording or organization edits. The git diff shows what changed; the revision note says *why*. Commits touching `research/` or `decisions/` need a non-empty body naming the concept affected.

**Cross-repo:** Cross-repo decisions live canonically in one repo (usually the repo where the evidence lives). Affected repos get a one-line stub: `See [repo]/decisions/YYYY-MM-DD-slug.md`.

## Research Topics

Each topic has a file prefix and its own index. Read the relevant topic index when working on that topic — don't load all indexes.

| Topic | Prefix | Index | Files |
|-------|--------|-------|-------|
| IQ sex differences | `iq-sex-differences-*` | `research/iq-sex-differences-INDEX.md` | 118 |
| Immigration (fiscal/crime) | `immigration-*` | `research/immigration-INDEX.md` | 30 |

New topics: create `research/<topic>-INDEX.md`, add a row here, use `<topic>-*` prefix for all files.

**Unprefixed files:** Some older files (`jre-2460-*`, `review-1*`, `fiscal-impact-*`, `full-spectrum-costs-*`, `zion/`) predate the prefix rule. When touching them, migrate to the right topic prefix; don't create new unprefixed files.

## Cross-Topic Notes

| File | Topic | Consult before |
|------|-------|----------------|
| `notes/llm-bias-caveat.md` | LLM instrument bias on politically charged topics | Any politically sensitive analysis |
| `notes/fact-check-prompt-template.md` | Multi-agent fact-check template | Running fact-check sweeps |
| `notes/exa-answer-evaluation.md` | Exa /answer accuracy evaluation | Choosing Exa vs alternatives |

<!-- knowledge-index
generated: 2026-04-19T04:06:29Z
hash: ff7356d91502

cross_refs: decisions/.template.md, decisions/YYYY-MM-DD-slug.md, research/<topic>-INDEX.md, research/immigration-INDEX.md, research/iq-sex-differences-INDEX.md

end-knowledge-index -->
