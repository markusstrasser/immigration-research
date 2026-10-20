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

History was rewritten on 2026-10-08 to purge personal files left over from the pre-split combined
repo. Living docs (this file, INDEX, FAQ, register, lane READMEs) cite the new hashes. Code pins
(`*_COMMIT`, `FREEZE`, `pins.json`), derived files and records keep the old ones, because derived
bytes are fingerprinted. The local-only ref `refs/pre-rewrite/2026-10-08` keeps those commits
resolvable here; it holds the purged files, so never push it or use `--mirror`. Resolve an old hash
through `notes/2026-10-08-history-rewrite-commit-map.tsv` before calling a cited commit missing.

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
  `citation_freshness.py --out <scratch>` in the same lane lists living prose that cites a superseded
  case's files (exit 1 while any remain). `infra/immigration-fiscal/live_case.json` declares the live
  case; an adoption updates it in the same commit.
- Python `csv.writer` defaults to CRLF; pass `lineterminator="\n"`. The repo stores LF
  (`core.autocrlf=input`), so CRLF outputs never byte-match on rerun (e2476da), and a fresh clone
  fails any pin of a CRLF file. `rerun_lane.py` fails on a lane file git would convert (an EOL line). A
  pinned raw download with CRLF goes in `.gitattributes` as `-text`, which also lists the older
  writers' outputs stored byte for byte.
- Before asserting that a line's key biases a result, read how the engine keys it (schools have
  been state-priced since 2026-09-20, not national-average). The adopted case is
  `infra/immigration-fiscal/main_case_2026_10_16/main_case.cjs`; its package (`package.cjs`) builds on v8
  (`main_case_2026_10_15`) with eight selected items, 13–18, 20 and 21; item 19 stays beside with W09.
  `meta.items` locates each item's edits, and `forItems`/`withItems` apply them. The ends are the personal
  specifications 16 / 11 in both methods (`summary.json` `v9.end_specifications`). The line and receipt responses,
  capital return, mixed-unit removal, coverage and the new method- or specification-specific post-engine terms travel
  in `derived/corrections.json`; `evaluateFull` is the canonical full evaluator. A raw-engine consumer must use
  `Engine.evaluate(withSyntheticLines(m), stateFor(m, spec, profile))` and apply every post term; `postFor` returns
  the new dynamic additions and `postEngine` the complete canonical-method post total. A partial reading alone is
  insufficient for the dynamic capital/service calculation. `withSyntheticLines` adds every absent carrier and
  component. `meta.population_v9.with_coverage` is the complete calibrated denominator; earlier population blocks
  remain historical. `meta.lineage` retains the pre-v8 descendant decomposition, not a closure of the later payload.
  Consumers splitting by generation, household or person need a rule for each item's typed parts and count/coverage
  changes (Consumers R1–R4 in v6, R5–R9 in v7, R10–R13 in v8, and the v9 RESULT's payload contract). Item 4 splits
  by `meta.user_fees.splits`, Pell and the K-12 weight by the education line. Item 17 is joint-minus-16; item 21's
  source arms have their own signed coverage/count increments. Consumer lanes compute the live case only (`oct16`);
  outputs of earlier cases stay in git and are not regenerated.

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
  `age_profile_components.csv`, `age_normalizations*.csv`). Since 2026-10-07 its expanded account
  carries item T, the income tax the survey misses, on the case's keys; the partial account keeps the
  survey's taxes, quoted as "taxes as the survey reports them", and a caller of `build_charges` without
  the keys stops `[BLOCKED]` unless it passes `--off T` (decision 2026-10-07-ledger-item-t). The finance-refresh and
  enrollment accounts carry the all-generation union only; do not flat-scale the ledger's split
  onto any account total. The adopted main case has its own split, computed on the account with
  no reference group: `infra/immigration-fiscal/generation_account_2026_09_24/derived/generation_results_oct16.csv`,
  the added descendants counted in G3+ (ladder 224; earlier cases' files are in git).
- The account prices 39,712,493 people (dataset audit row 4); the CPS ASEC's published weights give
  40.90M. A lane that sums CPS weights gates its total at row 4 (pattern:
  `world_ledger_2026_09_27/population_basis.py`) or states why the published frame is right; five
  v4 items used the published weights (ladder 275). The main case adds three groups the survey's
  union leaves out: since 2026-10-05, 3.04M descendants who no longer report Mexican origin (arm b,
  put on the account's frame by factor 0.997189, since row 4 reweights only the Mexico-born); since
  2026-10-15, the 0.52M US-born reporters with one US-born parent and their nonreporting children whom
  v7's generation rule dropped (item 10), and the 1.95M members the Census misses (item 12).
  Per-member figures divide by the 44.90M lineage (42.95M before coverage; v9 item 16 calibrates
  native minors, −0.33M). The CPS cannot see the
  descendants or the missed people, so a lane that re-keys the CPS takes their cost from the case lane
  or covers the union and says so (ladder 281); it takes item 10's people from
  `union_completion_2026_10_14`'s flags.
- The evidence map (`overview_2026_09_28/`) and figures page (`figures_2026_09_22/`) move to a new
  main case only when the operator asks. The map is on main case v9 since 2026-10-21; the figures page
  is on v6 since 2026-10-08; both moves were at his request. The figures page's unlinked prototypes stay on the
  September 24 account. The assumption explorer's page was deleted on 2026-10-15 at his word; its
  directory (`assumption_explorer_2026_09_21/`) keeps the engine, the model builder and the scaling
  check, which the case lanes import by that path.
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
  their measured ages, and public colleges, fees and Pell keyed by use
  ([decision](decisions/2026-10-07-main-case-v6.md)). Since 2026-10-14 it takes the group total at the
  personal allocation at both ends, follows child credits across mixed tax units, and counts the source
  taxes on the business capital that serves the group's jobs: mining at 0, corporate tax at 1 at the low
  end and at Treasury's normal-return share (0.37) at the high, and the production module's capital-tax
  term stays zero, so nothing counts twice; it also folds in v6's two measured residuals
  ([decision](decisions/2026-10-14-main-case-v7.md)). Since 2026-10-15 it removes the US tax on
  foreign-source income from item 6's corporate lines, completes the union's reporting rule, recomputes
  the taxes, credits, benefits and spending of the non-members who stay in mixed households (replacing
  the child-credit item), and carries the 2020 PES Hispanic undercount, which the 2024 population
  controls keep ([decision](decisions/2026-10-15-main-case-v8.md)). Adopted 2026-10-20, v9 makes the following
  changes ([decision](decisions/2026-10-16-main-case-v9.md)):
  - item 13 holds military service costs at zero long-run response under equal-cost replacement, with the
    means-tested pension still responsive and military costs retained in the first-year reading;
  - item 14 keys income-security administration's retirement block by Social Security caseloads, leaving its
    unmeasured remainder on the existing proxy;
  - item 15 splits public colleges' response by budget block, with tuition and Pell on their own keys;
  - item 16 calibrates native Mexican-origin minors to ACS counts while preserving CPS Hispanic totals;
  - item 17 prices the missed people's PES Table D tenure at fixed counts, jointly with item 16;
  - item 18 excludes food-at-home and SNAP purchases under the household taxable-basket exemption proxy;
  - item 20 charges public capital at the Trustees' flat-equivalent rate, the path pricing Social Security and
    Part A promises; booked employee pension and retiree-health normal costs keep their valuations;
  - item 21 keys the health residual outside VA by other-federal and state/local payments, with pooled ethnic
    translation; its program/exposure bridge remains unsettled and its arms stay beside.
  The case is income-year 2024 under 2024 tax and benefit rules, with Social Security and Part A promises at what
  current law can pay (2026 Trustees); a complete present-law total is unmeasured: **$368–437bn**.
  Companion figures from `main_case_2026_10_16/derived/summary.json` `v9.companions`:
  - $368.0–436.6bn at one decimal; counting benefits when paid (the cash set), $284.4–352.9bn;
    per member of the 44.90M lineage, $8,196–9,722;
  - the count's arms a and c: $354.4–421.5bn and $381.6–451.6bn;
    C3 ± one SE: $363.8–440.7bn;
  - counted by share of Mexican-immigrant ancestry (beside, never the headline), the two structural readings:
    $248.7–297.4bn with G4+ at nothing and $298.8–355.7bn at its bound;
  - schools at the within-district 0.836 response: $337.9–409.7bn;
  - the household-sharing allocation across members and nonmembers, item 11 excluded (for distribution,
    not the removal total): $322.8–390.5bn ($7,189–8,696 per member);
  - Census coverage from demographic analysis (beside): through age 17, $365.4–433.8bn;
    through 29, $364.1–431.1bn;
  - year-one response coefficients applied to this account: $313.8–370.8bn,
    $230.2–287.2bn counting benefits when paid; this is not next year's cash saving;
  - item 21's population, no-translation and plain-pooled arms: $361.7–430.2bn, $361.9–430.4bn and
    $375.2–443.7bn set, respectively; construction sensitivities, not error bounds.
  - Earlier cases: the decision records and the INDEX's case table.

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
