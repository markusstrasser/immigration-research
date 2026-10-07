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

**Never without human:** delete records (ladder entries, decisions, lane RESULTs, dated audits) or analysis lanes, publish or share findings externally, modify this constitution. Superseded and cruft documents may be deleted autonomously, with an INDEX tombstone, once their last version is on GitHub.

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
queries/immigration/ — checked-in warehouse checks (`-- requires:`/`-- backs:`); the headline is the main-case lane
scripts/reproduce-immigration-data.sh — init, doctor, download, verify, build, smoke, query
casebank/          — verbatim example cases with induced principles
HUMAN.md           — async asks to the operator
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
- Read a rerun's exit code before trusting an "outputs identical" check: a failed rerun (e.g. a
  missing `--with lxml`) leaves the old files untouched and they still compare identical.
- Check a lane reproduces before committing it: `uv run --no-project python3 scripts/rerun_lane.py
  infra/immigration-fiscal/<lane> "uv run --no-project python3 {lane}/<script>.py" …` must end
  `IDENTICAL: n/n` with exit 0; exit 3 names a script no command runs (rules in its docstring).
- Before committing a number edit to the INDEX, the FAQ or this file, run the drift audit's
  `audit_numbers.py --out <scratch>` and `memo_sweep.py --worktree --out <scratch>`
  (`infra/immigration-fiscal/number_drift_audit_2026_09_29/`; no MISMATCH or STALE). A new number
  in an audited span needs a `source_map.csv` row; without `--out` the audit rewrites its tracked `derived/`.
- Python `csv.writer` defaults to CRLF; pass `lineterminator="\n"`. The repo stores LF
  (`core.autocrlf=input`), so CRLF outputs never byte-match on rerun (cd96b04).
- Before asserting that a line's key biases a result, read how the engine keys it (schools have
  been state-priced since 2026-09-20, not national-average). The adopted case is one engine
  run plus a post-engine return on public capital:
  `infra/immigration-fiscal/main_case_2026_10_07/main_case.cjs`. Its package (`package.cjs`) is
  v5's (`main_case_2026_10_05`, built on the September 29 case's) plus an item registry: `meta.items`
  locates each item's edits, and `forItems`/`withItems` apply them. The line and receipt responses and
  the capital return travel in `derived/corrections.json` → `meta.responses` and
  `meta.capital_return`. A consumer that applies the payload must set all of them. The payload adds
  eight spending and two receipt lines that `model.json` lacks, plus item 4's three carrier receipt
  lines and four offset capital components: evaluate as `Engine.evaluate(withSyntheticLines(m),
  stateFor(m, spec, profile))`, or call `evaluateFull` for the full cost. `meta.lineage` records the
  added descendants (arm b, C3, the members priced as G3+ and as whites); their edits sit in every
  engine cell, and the items' edits follow them, so the lineage no longer closes the payload. A
  consumer that splits the case by generation, household or person needs a stated rule for both (the
  lane's Consumers table; item 4 splits by `meta.user_fees.splits`, Pell and the K-12 weight by the
  education line). Consumer lanes key the case `oct07`, beside their `oct05` outputs.

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
  `age_profile_components.csv`, `age_normalizations*.csv`). The finance-refresh and
  enrollment accounts carry the all-generation union only; do not flat-scale the ledger's split
  onto any account total. The adopted main case has its own split, computed on the account with
  no reference group: `infra/immigration-fiscal/generation_account_2026_09_24/derived/generation_results_oct07.csv`,
  the added descendants counted in G3+ (ladder 224; `generation_results_oct05.csv` keeps the
  October 5 case, `generation_results_sept29.csv` the September 29 case and `generation_results.csv`
  the September 27 case).
- The account prices 39,712,493 people (dataset audit row 4); the CPS ASEC's published weights give
  40.90M. A lane that sums CPS weights gates its total at row 4 (pattern:
  `world_ledger_2026_09_27/population_basis.py`) or states why the published frame is right; five
  v4 items used the published weights (ladder 275). Since 2026-10-05 the main case adds 3.04M
  descendants who no longer report Mexican origin (arm b, put on the account's frame by factor
  0.997189, since row 4 reweights only the Mexico-born): a 42.75M lineage, which per-member figures
  divide by. The CPS cannot see them, so a lane that re-keys the CPS either takes their cost from
  the case lane or covers the 39.71M union and says so (ladder 281).
- The evidence map (`overview_2026_09_28/`), assumption explorer (`assumption_explorer_2026_09_21/`)
  and figures page (`figures_2026_09_22/`) move to a new main case only when the operator asks. The
  map has been on main case v5 since 2026-10-06, at his request; the explorer and the figures page
  stay on earlier cases.
- Only income-year 2024 is a measured account. Earlier years are a
  [model back-cast](research/immigration-historical-backcast-2026-09-20.md).
- The headline's "CBO-informed" label covers CBO's tax-incidence rules and its category rule for
  which budgets respond; since 2026-09-26 the school response is no longer CBO's. Since
  2026-09-23 the main case lets general public services respond at 0.59–0.84, from cross-state
  scale, and charges justice and uncompensated care by use
  ([decision](decisions/2026-09-23-main-case-general-government-and-use-keys.md)). Since
  2026-09-24 it also carries the dataset audit, the pooled medical figure, care, shelter and the
  outside checks ([decision](decisions/2026-09-24-main-case-audit-and-outside-checks.md)). Since
  2026-09-26 general government is read as a finite removal (0.60–0.85), the consumption key is
  corrected for saving and remittances
  ([decision](decisions/2026-09-26-main-case-finite-removal-and-consumption-key.md)), and schools
  are charged at their full average cost per pupil
  ([decision](decisions/2026-09-26-main-case-schools-full-cost.md)). Since 2026-09-27 the main case also
  takes long-run road and park responses, rental assistance at 1, a 2–3% real return on public capital
  and every government enterprise
  ([decision](decisions/2026-09-27-main-case-capital-return-and-long-run-responses.md)). Since
  2026-09-29 it counts the Social Security and Part A promises members earn as they work, at the
  benefits current law can pay, and takes long-run property taxes, the IRS income-tax key, state
  prices, roads by miles and five smaller keys ([decision](decisions/2026-09-29-main-case-v4.md)).
  Since 2026-10-05 it also counts, as whole people and under the same rules, the 3.04M descendants
  of Mexican immigrants who no longer report Mexican origin
  ([decision](decisions/2026-10-05-main-case-v5.md)). Since 2026-10-07 it takes the 2026 Trustees
  Reports on current law's separate OASI and DI funds, retiree health on accrual, the added people at
  their measured ages, and public colleges, fees and Pell keyed by use: **$389–461bn**
  ([decision](decisions/2026-10-07-main-case-v6.md)). Earlier and companion figures:
  - $389.1–461.5bn unrounded; counting benefits when paid (the cash set), $307.4–385.4bn; per member
    of the 42.75M lineage, $9,101–10,794;
  - the count's arms a and c: $378.0–445.3bn and $400.2–477.7bn; C3 (0.557) ± 1 SE: $386.3–465.4bn;
  - counted by share of Mexican-immigrant ancestry instead of whole (beside, never the headline):
    $274.9–374.8bn;
  - low side with the within-district 0.836: $361–435bn;
  - October 5: $390.3–461.2bn, $307.4–383.4bn counting benefits when paid;
  - September 29: $371.4–434.8bn, $294.7–361.8bn counting benefits when paid;
  - September 27: $322–387bn; the schools case: $258–292bn;
  - first-year budget response with CBO's 0.63–0.66: $289–336bn, $207–260bn counting benefits when paid
    (ladder 270's lane; on the October 5 case $289–335bn and $206–258bn, on the September 29 case $277–318bn and
    $201–245bn; the September 26 run gave $201–246bn);
  - September 24: $201–246bn; September 23: $203–250bn; September 20: $165–197bn.

  The capital return is an imputed resource cost, never a debt flow. Defense,
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
