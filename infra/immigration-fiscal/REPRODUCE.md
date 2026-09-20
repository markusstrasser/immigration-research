# Reproduce immigration-fiscal data stack

For the **official URL → cleared AWS mirror → reader/browser acquisition** routes,
exact source versions, and **join/normalization recipes**, use
[Reader inputs, joins and normalization](REPRODUCTION_INPUTS.md).
It distinguishes the core warehouse from newer standalone analysis lanes.

From the repository root:

```bash
./scripts/reproduce-immigration-data.sh init
./scripts/reproduce-immigration-data.sh download minimal
./scripts/reproduce-immigration-data.sh verify required
./scripts/reproduce-immigration-data.sh build context # core warehouse only
# Alternatively, attempt the full public stack (~50 GB):
# ./scripts/reproduce-immigration-data.sh all standard
```

Or from `infra/immigration-fiscal/`:

```bash
./reproduce.sh init
./reproduce.sh doctor
./reproduce.sh download standard
./reproduce.sh verify required
./reproduce.sh build all          # context + mvp + lifetime + unified
./reproduce.sh package            # stage downloadable release in dist/
```

`build all` ends by merging the three warehouses into a single portable
`warehouse/immigration.duckdb` (schema-namespaced `context`/`lifetime`/`fiscal`,
self-describing `_catalog`). `build unified` rebuilds just that file.
`package` bundles it (duckdb + parquet + data dictionary + query pack +
checksums) into `dist/immigration-data-v<date>/`.

## Why scripts live in `infra/`

Dataset bytes are kept in the project's ignored `sources/` directory. Download and build logic is versioned under `infra/immigration-fiscal/`.

## Tiers

| Tier | Download | Build | Disk (approx) |
|------|----------|-------|----------------|
| `minimal` | ACS 2023 PUMS + CPS ASEC | Use `build context` for only the core warehouse | ~2 GB |
| `standard` | + stage2/3/5, IRS panel, lifetime PDFs | + MVP + lifetime union | ~50 GB |
| `full` | + tier-a labor + restrictionist + causal (Saiz, BEA) | same as standard | +5 GB |

## Configure paths

`./reproduce.sh init` creates `acquire/config.local.env` from portable defaults:

```bash
PNY_DATA_ROOT=$REPO_ROOT/sources/immigration-fiscal/data
DERIVED_ROOT=$REPO_ROOT/sources/immigration-fiscal/derived
CORPUS_ROOT=$REPO_ROOT/sources/corpus
REUSED_SURVEYS_ROOT=$REPO_ROOT/sources/reused-surveys
DUCKDB_PATH=$REPO_ROOT/warehouse/immigration_context.duckdb
```

`init` accepts the physical local directories and creates the relative compatibility link:

`sources/immigration-fiscal/data/derived` → `../derived`

Deliberate external overrides remain supported; conflicting existing directories are never replaced.

## Verify

```bash
./reproduce.sh verify required    # 3 census zips (pre-build)
./reproduce.sh verify optional    # full manifest downloads
./reproduce.sh verify derived     # manifest-listed build/compose outputs
```

Manifest: `DOWNLOAD_MANIFEST.tsv`

These are presence/minimum-size checks, not checksum verification. `all minimal`
limits the download tier but still calls `build all`; it does not isolate a core
build. Use the separate commands above. For result-specific checks and missing
input handling, see [verification limits](REPRODUCTION_INPUTS.md#verify-what-was-actually-reproduced).

## Manual / blocked

Scripts **skip** (not fail) when Playwright is unavailable: HUD CHAS (needs `uv run --with playwright`), ORR, some SSA/CBO PDFs. HUD moved bulk CSV zips to `portal/datasets/cp/` (Dec 2025); county Table 11 is `2018thru2022-050-csv.zip`.

After `download`, see:

- `$PNY_DATA_ROOT/external/stage5_net_negative/kff_refs/MANUAL_ACQUIRE.md`
- `$PNY_DATA_ROOT/external/lifetime/applications/MANUAL_ACQUIRE.md`

Application-gated (never scripted): PSID, IRS SOI PUF, Synthetic SIPP, FSRDC LEHD.

## Requirements

`bash`, `curl`, `unzip`, `uv` (Python builders). Optional: `playwright` for HUD CHAS retry.

## CI smoke

GitHub Actions runs `./reproduce.sh doctor` only (no multi-GB download).

Local end-to-end:

```bash
./reproduce.sh smoke   # minimal download + context build + DuckDB probe
./reproduce.sh query   # rerun headline SQL after full build
```

## Share reasoning with someone else

1. Send them `research/immigration-friend-reproduce-guide.md` (reading order + supersession rules).
2. They clone the repo and run `./scripts/reproduce-immigration-data.sh all standard`.
3. They rerun checks: `./scripts/reproduce-immigration-data.sh query`.
4. Query pack: `queries/immigration/` (each file cites the backing memo).
