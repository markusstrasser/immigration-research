# Immigration Research — fiscal & crime impact

An empirical investigation into the **fiscal and crime impact of immigration** (US, low-skill
focus), conducted with the discipline of investigative scholarship: primary sources, competing
interpretations, falsifiable claims, and honest uncertainty.

> **This repo does not answer "is immigration good or bad?" with one number.** It builds a
> sourced, queryable evidence stack and a memo trail that decomposes the question into separable
> coordinates (federal vs state-local, annual vs lifetime NPV, aggregate vs distributional,
> native vs immigrant-borne) and tracks which claims survive scrutiny.

### Read this first

This research is conducted *through an LLM*, which carries systematic post-training dispositions
on politically charged topics. **Before treating any synthesis as neutral, read
[`notes/llm-bias-caveat.md`](notes/llm-bias-caveat.md).** The generative principle (from
[`CLAUDE.md`](CLAUDE.md)): *maximize the rate at which claims converge toward ground truth* — a
single well-sourced falsification beats ten plausible syntheses.

---

## What's in here

| Path | What |
|------|------|
| `research/immigration-*.md` | The memo stack — 130+ sourced memos with confidence tiers and supersession notes. Start at the [topic index](research/immigration-INDEX.md). |
| `warehouse/immigration.duckdb` | **The unified data warehouse** — all cleaned/joined panels in one schema-namespaced file (`context` / `lifetime` / `fiscal`) with a self-describing `_catalog` table. *(Built locally; gitignored.)* |
| `infra/immigration-fiscal/` | The acquisition + build pipeline (acquire → parse → warehouse). See its [`REPRODUCE.md`](infra/immigration-fiscal/REPRODUCE.md). |
| `queries/immigration/` | Checked-in SQL that reproduces the headline numbers (each file has `-- requires:` and `-- backs:` headers). |
| `decisions/` | Concept-level pivots — when an interpretation shifted or a method was adopted/dropped. |
| `notes/` | Cross-topic working notes (instrument bias, quant-bias checklist, fact-check templates). |
| `GOALS.md` · `CLAUDE.md` | Human-owned mission / the research constitution + agent operating rules. |

## Reproduce it (friend quickstart)

**Two paths.** Grab the packaged data if you just want to query; rebuild from source if you want
to re-derive or extend the panels.

### Fastest — download the data (no multi-GB rebuild)

```bash
# immigration-data-v<date>.tar.gz, staged by the maintainer (reproduce.sh package)
tar xzf immigration-data-v*.tar.gz && cd immigration-data-v*
shasum -a 256 -c SHA256SUMS                                  # verify integrity
duckdb immigration.duckdb "SELECT * FROM _catalog ORDER BY n_rows DESC"
```

The tarball carries `immigration.duckdb`, per-table Parquet, `DATA_DICTIONARY.md`, the query
pack, and checksums.

### Rebuild from source

**Requirements:** macOS/Linux, `bash`, `curl`, `unzip`, [`uv`](https://docs.astral.sh/uv/),
[`duckdb`](https://duckdb.org/) CLI. ~2 GB for the minimal warehouse, ~50 GB for the full public stack.

```bash
git clone git@github.com:markusstrasser/immigration-research.git
cd immigration-research

./scripts/reproduce-immigration-data.sh init     # write config.local.env (edit paths if needed)
./scripts/reproduce-immigration-data.sh doctor   # check required binaries

# Playwright is only needed for two WAF-blocked sources (HUD CHAS + SAFMR):
uv run --with playwright python -m playwright install chromium

./scripts/reproduce-immigration-data.sh all minimal    # ~2 GB, core warehouse only
# or: all standard                                      # ~50 GB, full public stack

./scripts/reproduce-immigration-data.sh smoke    # sanity-check the warehouse
./scripts/reproduce-immigration-data.sh query    # rerun the headline SQL
```

`scripts/reproduce-immigration-data.sh` is a thin wrapper over
`infra/immigration-fiscal/reproduce.sh` — run either. Paths live in
`infra/immigration-fiscal/acquire/config.local.env` (gitignored).

**License note:** the IPUMS census microdata panel (44 M rows, used to derive the Borjas
supply-shock cells) is **license-restricted and excluded from any redistributable release** — only
the aggregated `borjas_supply_shock_panel` ships. Rebuilding it requires your own IPUMS USA
extract; see `infra/immigration-fiscal/REPRODUCE.md`.

## Where to start reading

The detailed reading order, the **canonical-vs-superseded claims table**, and warehouse query
definitions live in **[`research/immigration-friend-reproduce-guide.md`](research/immigration-friend-reproduce-guide.md)**.
Shortest path into the reasoning:

1. [`immigration-main-question-reset.md`](research/immigration-main-question-reset.md) — what the repo actually asks
2. [`immigration-glossary.md`](research/immigration-glossary.md) — `low-skill`, `incidence`, `PUMA`, … defined
3. [`immigration-confidence-ladder.md`](research/immigration-confidence-ladder.md) — strong vs weak vs contextual-only
4. [`immigration-fiscal-welfare-ledger-map.md`](research/immigration-fiscal-welfare-ledger-map.md) — the unifying "positive vs negative?" decomposition
5. [`immigration-conclusion-audit-running-fixes.md`](research/immigration-conclusion-audit-running-fixes.md) — what changed (read before citing any number)

## Status & how to cite

This repo is public for transparency and scrutiny, but it is **working research, not a finished
publication**: memos carry explicit confidence tiers, many are marked superseded, and the analysis is
LLM-conducted (see the instrument-bias caveat above). Cite the dated artifact, not the headline, and
treat any conclusion as provisional. The agent operating this repo does not publish or promote findings
externally on its own — that stays a human decision (`CLAUDE.md` → Autonomy Boundaries).
