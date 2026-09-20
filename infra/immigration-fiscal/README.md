# immigration-fiscal — reproducible acquisition

**Canonical location (git-tracked):** `infra/immigration-fiscal/` in the immigration-research repo.

Dataset bytes live in this project's ignored `sources/` directory. All download logic lives here so anyone can reproduce on their machine. Explicit environment overrides remain available.

## New machine quickstart

```bash
cd /path/to/immigration-research
./scripts/reproduce-immigration-data.sh init
./scripts/reproduce-immigration-data.sh doctor
./scripts/reproduce-immigration-data.sh all minimal   # or: standard | full
```

See `REPRODUCE.md` for tiers, verify modes, and manual-acquire list.

**Share with a friend:** `research/immigration-friend-reproduce-guide.md` — reading order + `./scripts/reproduce-immigration-data.sh query`.

**Requirements:** `bash`, `curl`, `unzip`, `uv` (for Python builders). **Playwright** for HUD CHAS + SAFMR (`uv run --with playwright python -m playwright install chromium`).

## Layout

| Path | Role |
|------|------|
| `reproduce.sh` | **One-command** init / download / verify / build / **package** |
| `build/build_unified_warehouse.py` | **Single portable `immigration.duckdb`** — merges context+lifetime+fiscal, schema-namespaced, self-describing `_catalog` (`reproduce.sh build unified`) |
| `build/package_data_release.py` | **Downloadable release** — duckdb + parquet + dict + checksums → `dist/` (`reproduce.sh package`) |
| `build/emit_data_dictionary.py` | Markdown data dictionary from the unified DB |
| `acquire/setup.sh` | Main acquisition (~80 URLs) |
| `acquire/setup-net-negative.sh` | Stage-5 fiscal/local-cost datasets |
| `acquire/setup-lifetime.sh` | Lifetime benchmarks + linkage docs (NAS/NRC/Orrenius/Storesletten) |
| `build-lifetime.sh` | `immigration_lifetime_evidence.duckdb` + `immigration_fiscal_union.duckdb` (country tensor) |
| `build/build_country_fiscal_tensor.py` | Population × ledger × order tensor + bridge grid |
| `acquire/config.env.example` | Portable default paths |
| `acquire/config.local.env` | Your machine (gitignored) |
| `DOWNLOAD_MANIFEST.tsv` | Machine-readable catalog + verify script input |
| `scripts/fetch_hud_chas.py` | Playwright fetch for HUD CHAS (`cp/` portal) |
| `scripts/fetch_browser.py` | Generic Playwright fetch with optional referer warm-up |
| `scripts/verify-downloads.sh` | Check manifest paths exist |
| `build/*.py` | Warehouse + MVP builders (env-driven paths) |
| `build-context.sh` | `immigration_context.duckdb` |
| `build-mvp.sh` | SIPP/MEPS/federal microsim CSVs |

## Environment variables

| Variable | Purpose |
|----------|---------|
| `IMMIGRATION_DATA_ROOT` | Alias for `PNY_DATA_ROOT` (raw data root) |
| `PNY_DATA_ROOT` | Where `setup.sh` writes zips/CSVs |
| `IMMIGRATION_CORPUS_ROOT` / `CORPUS_ROOT` | Large mirrors (ACS corpus, IRS SOI panel) |
| `IMMIGRATION_DERIVED_ROOT` / `DERIVED_ROOT` | Builder outputs (stage2/3 CSVs) |
| `IMMIGRATION_DUCKDB_PATH` / `DUCKDB_PATH` | Slim warehouse file |
| `IMMIGRATION_CAUSAL_DATA` | Path to `immigration-causal/data` for receiver-city CSV copy |
| `REUSED_SURVEYS_ROOT` | Locally retained ECLS, ELS, PIAAC and NLSY source files |
| `ITEP_TABLE_PATH` | Exact ITEP table for the Tiebout lane; replaces its former use of `IMMIGRATION_FISCAL_ROOT` as a data override |

## Project-local dataset layout

Paths default to these directories relative to the checkout, regardless of the shell's working directory:

```text
sources/immigration-fiscal/data/       raw fiscal inputs
sources/immigration-fiscal/derived/    derived tables and microdata warehouse
sources/corpus/                       optional source mirrors
sources/reused-surveys/               reused survey releases and metadata
```

`data/derived` is a relative link to `../derived`. The layout initializer accepts physical directories and refuses to replace conflicting paths. Python callers share `build/paths.py`; shell callers share `acquire/lib.sh` and `config.env.example`. Missing default input roots fail loudly. Reconnect the USB only to recover a specifically identified missing source; it is no longer a default runtime dependency.

Setting only `PNY_DATA_ROOT` (or `IMMIGRATION_DATA_ROOT`) retains that root's `derived/` subtree. An explicit `DERIVED_ROOT` (or `IMMIGRATION_DERIVED_ROOT`) takes precedence. The sibling local derived directory above applies when no raw-root override is supplied. `IMMIGRATION_FISCAL_ROOT` identifies code, including for the Tiebout lane; use `ITEP_TABLE_PATH` to select a different ITEP table.

## Manual / WAF-blocked

See `data/external/stage5_net_negative/kff_refs/MANUAL_ACQUIRE.md` after setup (KFF exports, EDFacts EL, etc.). HUD CHAS, SAFMR, and SNAP are scripted when Playwright/azureedge paths work.

## Specs

- `research/immigration-dataset-register.md`
- `research/immigration-verified-findings-report-2026-04-10.md`
- `research/immigration-net-negative-dataset-frontier-2026-06-15.md`
