# Research — Getting to the Truth

## Purpose
This repo pursues empirical questions with the rigor of investigative scholarship. The current topic is the **fiscal and crime impact of immigration**; the methodology is constant: primary sources, competing interpretations, falsifiable claims, honest uncertainty. (Split 2026-06-23 from the former combined `research` repo — IQ sex differences moved to `~/Projects/iq-sex-differences`, one-off notes to `~/Projects/research-misc`.)

## Constitution

### Generative Principle

> Maximize the rate at which claims converge toward ground truth, measured by the ratio of verified/falsified claims to total claims produced.

Truth is the objective. Not consensus, not novelty, not volume. A single well-sourced falsification is worth more than ten plausible syntheses. Error correction is the mechanism — every claim should be easier to kill than to keep alive.

### Principles

**1. Source everything.** No floating claims. Tag with `[SOURCE: url/citation]`, `[DATA: local file/table]`, `[CALCULATION: script/output]` (older memos also write `[DERIVATION]`), `[INFERENCE]`, `[TRAINING-DATA]`, or `[UNVERIFIED]`. Unsourced claims in research output are bugs.

**2. Steel-man before criticizing.** Present the strongest version of any position before evaluating it. If you can't articulate why smart people believe X, you don't understand X well enough to refute it.

**3. Distinguish levels of evidence.** Empirical fact > expert consensus > contested evidence > opinion > speculation. Label which level you're operating at. Don't dress speculation as fact. For a modelled number, state which inputs are measured and which are assumed.

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

Worktrees are temporary. Once a worktree's output is committed on main, remove it in the same
session (`git worktree remove <path>`); `git worktree list` should show only main between
sessions. A stale worktree keeps an old copy of this file and pre-integration drafts that a
search can mistake for current work. Before removing one, confirm its HEAD is on main and that
its uncommitted and ignored files (`_cache/`, `raw/`) exist on main.

## Tools Available

### Skills

Symlinked into `.claude/skills/` from `~/Projects/skills/`; each `SKILL.md` carries its own
description, and the session's skill listing shows which are enabled.

### MCP Servers (`.mcp.json`)
- **exa** — semantic web search, entity enrichment, deep research
- **research** (research-mcp) — Semantic Scholar, corpus management, claim verification, preprint surveillance
- **firecrawl** — web scraping and structured extraction

Only these three are configured in `.mcp.json` (checked 2026-09-21); brave-search,
agent-infra, parallel and context7 are not available in this project.

## Structure

```
GOALS.md           — human-owned mission, strategy, success metrics (read at session start)
research/          — topic files, one per question or area
decisions/         — concept-level pivots, approach selections, methodology shifts
infra/immigration-fiscal/<lane>_<date>/ — one analysis per directory: script, README or
                     RESULT.md, tracked `derived/` summaries, ignored `_cache/` raw pulls
warehouse/         — DuckDB warehouses (context, lifetime evidence); not a full inventory
sources/           — archived source material, data files; ignored, a real directory here
                     (`~/research-data` is a symlink to it, not a second copy)
notes/             — working notes, drafts, threads of analysis
queries/immigration/ — checked-in SQL reproducing the headline numbers (`-- requires:`/`-- backs:`)
scripts/reproduce-immigration-data.sh — init, doctor, download, verify, build, smoke, query
casebank/          — verbatim example cases with induced principles
HUMAN.md           — async asks to the operator; CYCLE.md is a finished April–June loop log
```

### Running analysis lanes

```sh
# from the repository root; lanes document any extra --with wheels in their README
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/<lane>/<script>.py
uv run --no-project python3 -m pytest infra/immigration-fiscal/<lane>/ -q
# Census API: the key lives in the untracked acquire/config.local.env; never print it
set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
```

- `--no-project` reuses the main checkout's `.venv`. In a worktree or fresh clone it fails with
  `ModuleNotFoundError`; drop the flag there (`uv run python3 …` builds from `uv.lock`).

- Consumers of `ledger_absolute_2026_09_17` (the `lifetime.py` loaders, `age_normalizations.py`)
  verify stored source hashes, including upstream
  `gen_ledger_extension_2026_09_16/extend_ledger.py`, and stop with
  `[BLOCKED] missing or stale source` after any edit to a fingerprinted `.py`. Repair by
  rebuilding to a scratch `--out-dir`, byte-comparing the outputs, then re-running
  `absolute_ledger.py`, `check_gates.py` and `lifetime.py` in place. Never edit a hash.
  Hashes in other lanes' `audit.json` or `manifest.json` are build-time provenance, rewritten
  by each build (the `full_account_*` builders replay their upstream instead); an older hash
  there records what produced the outputs.
- Pipe Census API output through a redaction filter; error messages and `pgrep`/`ps`
  dumps carry the key in the URL. A hook blocks reads of `~/.config` secret stores.

### Finding local data and current results

For a question about what our data show, follow these existing entry points before
substituting a web summary or declaring a measurement unavailable:

- [Topic index](research/immigration-INDEX.md): current results and supersession notes.
- [Dataset register](research/immigration-dataset-register.md): local inputs, fields,
  join keys, coverage and limitations; follow its linked analysis README and outputs.
- [Raw-file manifest](sources/immigration-fiscal/data/MANIFEST.md): storage inventory;
  verify that the referenced file exists and resolve `sources` on this machine.
- [Reproduction inputs](infra/immigration-fiscal/REPRODUCTION_INPUTS.md): official
  acquisition routes, pinned versions, normalization and reproduction commands.
- [Objections FAQ](research/immigration-objections-faq-2026-09-21.md): standard objections,
  each routed to its executed table; start here for "what about X?" questions. Before
  writing any summary or ranking of results, in chat as much as in a memo, read its section
  "Before combining numbers from different entries": the commit-time bias gate does not see
  a chat answer.
- Fiscal results **by generation against a white reference** exist only in
  `infra/immigration-fiscal/ledger_absolute_2026_09_17/derived/` (`complete_gaps.csv`,
  `age_profile_components.csv`, `age_normalizations*.csv`). The later finance-refresh,
  enrollment and complete accounts carry the all-generation union only; do not flat-scale
  the split onto their totals.
- Only income-year 2024 is a measured account. Earlier years are a
  [model back-cast](research/immigration-historical-backcast-2026-09-20.md).
- The headline's "CBO-informed" label covers two inputs only: CBO's tax-incidence rules and
  its 63–66% school-spending response. Since 2026-09-23 the main case ($203–250bn; September
  20: $165–197bn) lets general public services respond at 0.59–0.84, from cross-state scale,
  and charges justice and uncompensated care by use
  ([decision](decisions/2026-09-23-main-case-general-government-and-use-keys.md)). Defense,
  existing interest and business subsidies stay at **zero response by assumption**; see the
  [complete annual account](research/immigration-complete-annual-account-2026-09-20.md)
  and FAQ entry 2 for the sensitivity.

The unified warehouse is one entry point, not a complete inventory of newer
analysis directories. Use `rg --files --no-ignore` when locating ignored raw or
derived files. Distinguish data absent, data present but not yet tabulated, and an
unidentified causal effect. Older acquisition roadmaps describe leads; check the
current register before treating a listed dataset as missing.

For crime, incarceration or detention-cost claims, first read the
[custody/crime measurement rule](research/immigration-detention-crime-and-fiscal-scope-2026-09-20.md)
and [completed detention spending audit](infra/immigration-fiscal/detention_reconciliation_2026_09_20/README.md).
The [verification handoff](research/immigration-verification-handoff.md#detention-crime-and-spending-reuse-before-researching)
identifies the preserved distinctions, runnable checks and evidence needed to
reopen the remaining gaps. Reuse the pinned work before repeating acquisition.

## Decision Journal (`decisions/`)

Records of concept-level pivots — when an interpretation shifts, a methodology is adopted/dropped, a causal node gets resolved or reopened. One file per decision, `YYYY-MM-DD-slug.md`. Template in `decisions/.template.md`. Records use YAML frontmatter for machine-readable metadata (concept grouping, typed relations, provenance).

**When to write:** path-dependent interpretation choices, dropping a hypothesis after evidence, adopting a new dataset/method that forecloses alternatives, resolving a causal fork where the reasoning is costly to reconstruct. Do NOT write for: parameter tweaks, routine implementation, local execution details.

**Research memos:** when updating with revised understanding, add a dated `## Revisions` entry at the bottom linking to the triggering decision. Only for claim/interpretation/confidence changes — not for wording or organization edits. The git diff shows what changed; the revision note says *why*. Commits touching `research/` or `decisions/` need a non-empty body naming the concept affected.

**Cross-repo:** Cross-repo decisions live canonically in one repo (usually the repo where the evidence lives). Affected repos get a one-line stub: `See [repo]/decisions/YYYY-MM-DD-slug.md`.

## Research Topics

Each topic has a file prefix and its own index. Read the relevant topic index when working on that topic — don't load all indexes.

| Topic | Prefix | Index | Files |
|-------|--------|-------|-------|
| Immigration (fiscal/crime) | `immigration-*` | `research/immigration-INDEX.md` | `ls research/immigration-*.md \| wc -l` |

New topics: create `research/<topic>-INDEX.md`, add a row here, use `<topic>-*` prefix for all files. Every top-level `research/*.md` file carries the `immigration-*` prefix — the pre-prefix legacy files were migrated 2026-06-24.

## Cross-Topic Notes

| File | Topic | Consult before |
|------|-------|----------------|
| `notes/llm-bias-caveat.md` | LLM instrument bias on politically charged topics | Any politically sensitive analysis |
| `notes/quant-bias-checklist.md` | Quant-bias gate, project instance + self-audit record (canonical list: research skill `references/quant-bias-checklist.md`) | Committing any memo with numbers doing argumentative work, causal language, or welfare conclusions |
| `notes/fact-check-prompt-template.md` | Multi-agent fact-check template | Running fact-check sweeps |
| `notes/exa-answer-evaluation.md` | Exa /answer accuracy evaluation | Choosing Exa vs alternatives |

<!-- knowledge-index
generated: 2026-04-19T04:06:29Z
hash: ff7356d91502

cross_refs: decisions/.template.md, decisions/YYYY-MM-DD-slug.md, research/<topic>-INDEX.md, research/immigration-INDEX.md, research/iq-sex-differences-INDEX.md

end-knowledge-index -->
