# Reproduce immigration-fiscal data stack

**One command:** from repo root:

```bash
./scripts/reproduce-immigration-data.sh init
./scripts/reproduce-immigration-data.sh all minimal   # ~2 GB download + warehouse
./scripts/reproduce-immigration-data.sh all standard  # full public stack (~50 GB attempts)
```

Or from `infra/immigration-fiscal/`:

```bash
./reproduce.sh init
./reproduce.sh doctor
./reproduce.sh download standard
./reproduce.sh verify required
./reproduce.sh build all
```

## Why scripts live in `infra/`

`research/sources` is often a symlink to an external SSD and is **not in git**. Download and build logic is versioned under `infra/immigration-fiscal/`.

## Tiers

| Tier | Download | Build | Disk (approx) |
|------|----------|-------|----------------|
| `minimal` | ACS 2023 PUMS + CPS ASEC | `immigration_context.duckdb` | ~2 GB |
| `standard` | + stage2/3/5, IRS panel, lifetime PDFs | + MVP + lifetime union | ~50 GB |
| `full` | + tier-a labor + restrictionist + causal (Saiz, BEA) | same as standard | +5 GB |

## Configure paths

`./reproduce.sh init` creates `acquire/config.local.env` from portable defaults:

```bash
PNY_DATA_ROOT=$HOME/research-data/immigration-fiscal/data
DERIVED_ROOT=$PNY_DATA_ROOT/derived
DUCKDB_PATH=$REPO_ROOT/warehouse/immigration_context.duckdb
```

On machines with `sources/` in-repo (not symlinked), `init` also links:

`sources/immigration-fiscal/data` → `$PNY_DATA_ROOT`

## Verify

```bash
./reproduce.sh verify required    # 3 census zips (pre-build)
./reproduce.sh verify optional    # full manifest downloads
./reproduce.sh verify derived     # post-build CSV outputs
```

Manifest: `DOWNLOAD_MANIFEST.tsv`

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
