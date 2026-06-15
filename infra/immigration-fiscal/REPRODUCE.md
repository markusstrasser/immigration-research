# Reproduce immigration-fiscal data stack

## Why scripts live in `infra/`

`research/sources` is a symlink to an external SSD. Git cannot track files there. **All download and build scripts are versioned under `infra/immigration-fiscal/`.**

## Steps (any machine)

### 1. Clone + configure

```bash
git clone <research-repo> ~/Projects/research
cd ~/Projects/research/infra/immigration-fiscal
cp acquire/config.env.example acquire/config.local.env
```

Edit `acquire/config.local.env`:

```bash
export PNY_DATA_ROOT="$HOME/research-data/immigration-fiscal/data"   # ~50GB+
export CORPUS_ROOT="$HOME/research-data/corpus"                      # optional mirrors
export DERIVED_ROOT="$HOME/research-data/immigration-fiscal/derived"
export DUCKDB_PATH="$HOME/Projects/research/warehouse/immigration_context.duckdb"
```

### 2. Download

```bash
bash acquire/setup.sh          # required: ACS + CPS zips; optional: SIPP, MEPS, stage2-5
bash scripts/verify-downloads.sh
```

Logs: `acquire/setup.log`

**Required failures** exit non-zero if ACS person/household or CPS ASEC zips are missing.

### 3. Build

```bash
bash rebuild.sh                # DuckDB warehouse (stage1+2 + federal microsim)
bash rebuild_mvp.sh            # SIPP/MEPS cells + bridge (~2 min SIPP stream)
```

### 4. Query

```bash
uv run --with duckdb python -c "
import duckdb
c=duckdb.connect('$DUCKDB_PATH', read_only=True)
print(c.execute('SHOW TABLES').fetchall())
"
```

## Disk budget (approximate)

| Tier | Size | Scripts |
|------|------|---------|
| Minimum (warehouse) | ~2 GB | ACS + CPS required |
| Stage 2 county bridge | +500 MB | IRS migration, school finance, crosswalk |
| Stage 3 MVP | +4 GB | SIPP 2024 + MEPS HC-251 |
| Full corpus mirror | +10 GB | IRS SOI migration panel, ACS corpus zip |

## Blocked sources

Automated scripts **skip** (not fail) when WAF/403 blocks: HUD CHAS, BLS LAUS, ORR, ACF. Manual list written to:

`$PNY_DATA_ROOT/external/stage5_net_negative/kff_refs/MANUAL_ACQUIRE.md`

## Updating URLs

1. Edit `acquire/setup.sh` or `acquire/setup-net-negative.sh`
2. Add a row to `DOWNLOAD_MANIFEST.tsv`
3. Run `bash scripts/verify-downloads.sh`

## PNY symlink users

If `sources/immigration-fiscal` exists on SSD, wrappers call infra automatically when:

```bash
export IMMIGRATION_FISCAL_INFRA="$HOME/Projects/research/infra/immigration-fiscal"
```
