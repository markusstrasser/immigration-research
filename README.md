# Immigration Research — fiscal & crime impact

An empirical investigation into the **fiscal and crime impact of immigration** (US, low-skill
focus), conducted with the discipline of investigative scholarship: primary sources, competing
interpretations, falsifiable claims, and honest uncertainty.

> **This repo does not answer "is immigration good or bad?" with one number.** It builds a
> sourced, queryable evidence stack and a memo trail that decomposes the question into separable
> coordinates (federal vs state-local, annual vs lifetime NPV, aggregate vs distributional,
> native vs immigrant-borne) and tracks which claims survive scrutiny.

### Read this first

Start with the [topic index](research/immigration-INDEX.md) for current results and
the [dataset register](research/immigration-dataset-register.md) for data already
held, their fields, local paths and limits. Follow the relevant analysis README
to its actual inputs and outputs. The warehouse alone does not inventory newer
analysis directories; ignored files require `rg --files --no-ignore`.

**Current result (income year 2024).** The adopted main case puts the conditional net cost of the
Mexican-origin population (a 42.75M-person lineage, all generations, counting the 3.04M descendants who
no longer report Mexican origin) to other US residents at **$390–461bn a
year**, counting the pension promises members earn as they work, or $307–383bn counting benefits
when paid ([lane](infra/immigration-fiscal/main_case_2026_10_05/RESULT.md),
[decision](decisions/2026-10-05-main-case-v5.md)). Other residents' social costs and benefits outside the public
budget bring it to $490–571bn (on the September 29 case, $463–536bn). Only 2024 is measured;
earlier years are a model back-cast. The [objections FAQ](research/immigration-objections-faq-2026-09-21.md)
routes the standard objections to their executed tables, and the
[evidence map](infra/immigration-fiscal/overview_2026_09_28/) (`build.py` writes the reader page)
summarizes the confidence ladder; its figures are still the September 27 case's.

**Earlier errors.** A September 5, 2026 audit found material fiscal-unit, source-version and inference
errors in earlier analyses; the [repair report](research/immigration-material-repair-report-2026-09-05.md)
preserves it. Check historical dollar figures and causal verdicts against their supersession notes.
Superseded memos were deleted on 2026-09-29; the topic index lists them with the commit that holds them.

This research is conducted *through an LLM*, which carries systematic post-training dispositions
on politically charged topics. **Before treating any synthesis as neutral, read
[`notes/llm-bias-caveat.md`](notes/llm-bias-caveat.md).** The generative principle (from
[`CLAUDE.md`](CLAUDE.md)): *maximize the rate at which claims converge toward ground truth* — a
single well-sourced falsification beats ten plausible syntheses.

---

## What's in here

| Path | What |
|------|------|
| `research/immigration-*.md` | The memo stack — about 185 sourced memos with confidence tiers and supersession notes. Start at the [topic index](research/immigration-INDEX.md). |
| `warehouse/immigration.duckdb` | **The unified data warehouse** — all cleaned/joined panels in one schema-namespaced file (`context` / `lifetime` / `fiscal`) with a self-describing `_catalog` table. *(Built locally; gitignored.)* |
| `infra/immigration-fiscal/` | The acquisition + build pipeline (acquire → parse → warehouse). See its [`REPRODUCE.md`](infra/immigration-fiscal/REPRODUCE.md). |
| `queries/immigration/` | Checked-in warehouse queries: descriptive checks of the September 5 warehouses (each file has `-- requires:` and `-- backs:` headers). The headline is one engine run of the [main-case lane](infra/immigration-fiscal/main_case_2026_10_05/); [REPRODUCTION_INPUTS](infra/immigration-fiscal/REPRODUCTION_INPUTS.md#the-adopted-main-case-the-headline) gives its inputs. |
| `decisions/` | Concept-level pivots — when an interpretation shifted or a method was adopted/dropped. |
| `notes/` | Cross-topic working notes (instrument bias, quant-bias checklist, fact-check templates). |
| `GOALS.md` · `CLAUDE.md` | Human-owned mission / the research constitution + agent operating rules. |

## Reproduce it (friend quickstart)

**Two paths.** Grab the packaged data if you just want to query; rebuild from source if you want
to re-derive or extend the panels.

The [input and normalization guide](infra/immigration-fiscal/REPRODUCTION_INPUTS.md)
maps official downloads, cleared mirror candidates and reader/browser steps to
the actual join keys, recodes and validation recipes. AWS URLs are not yet
registered; a staged package is not an automatically cleared public release.

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

./scripts/reproduce-immigration-data.sh download minimal
./scripts/reproduce-immigration-data.sh verify required
./scripts/reproduce-immigration-data.sh build context  # core warehouse only
# Or: ./scripts/reproduce-immigration-data.sh all standard  # ~50 GB attempts

./scripts/reproduce-immigration-data.sh smoke    # sanity-check the warehouse
./scripts/reproduce-immigration-data.sh query    # rerun the warehouse queries
```

`scripts/reproduce-immigration-data.sh` is a thin wrapper over
`infra/immigration-fiscal/reproduce.sh` — run either. Paths live in
`infra/immigration-fiscal/acquire/config.local.env` (gitignored).

**License note:** raw IPUMS records are kept in a separate local microdata warehouse;
rebuilding the historical cells requires the specified extract. Other sources have
their own redistribution terms too. The current packager exports the whole unified
warehouse without a licensing filter; use the [source-specific routes](infra/immigration-fiscal/REPRODUCTION_INPUTS.md)
before publishing a bundle.

## Where to start reading

The detailed reading order, the **canonical-vs-superseded claims table**, and warehouse query
definitions live in **[`research/immigration-friend-reproduce-guide.md`](research/immigration-friend-reproduce-guide.md)**.
Shortest path into the reasoning:

1. [`GOALS.md`](GOALS.md) — what the repo actually asks
2. [`immigration-glossary.md`](research/immigration-glossary.md) — `low-skill`, `incidence`, `PUMA`, … defined
3. [`immigration-confidence-ladder.md`](research/immigration-confidence-ladder.md) — strong vs weak vs contextual-only
4. [`immigration-objections-faq-2026-09-21.md`](research/immigration-objections-faq-2026-09-21.md) — the standard objections, each routed to its executed table
5. [`decisions/`](decisions/) — what changed and why (read before citing any number)

## Status & how to cite

This repo is public for transparency and scrutiny, but it is **working research, not a finished
publication**: memos carry explicit confidence tiers, many are marked superseded, and the analysis is
LLM-conducted (see the instrument-bias caveat above). Cite the dated artifact, not the headline, and
treat any conclusion as provisional. The agent operating this repo does not publish or promote findings
externally on its own — that stays a human decision (`CLAUDE.md` → Autonomy Boundaries).
