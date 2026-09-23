# One store for IPUMS USA extracts 3–15: sort, name, catalog, join

Date: 2026-09-23. Operator: "move, grok, sort, rename, integrate, join ... then delete duplicates
etc. Maybe we can answer more questions with them".

## What exists (checked by the lead)

The operator's IPUMS USA account holds extracts 1–15. Extracts 3–15 were submitted today through
the API by four lanes, which saved them under their own `_cache/`:

| # | Lane cache copy (complete, sha256 verified by the lane) |
|---|---|
| 3 | `schooling_selection_position_2026_09_23/_cache/us_mexborn.data.csv.gz` |
| 4, 5, 6, 9, 14, 15 | `crime_selection_cohorts_2026_09_23/_cache/ipums/{census,acs_mex,census_q,acs_movers_lite,census_inst_q,census2000_inst}.csv.gz` (+ `.xml` DDI) |
| 7, 8 | none: `acs_movers` and `acs_us`, with replicate weights, were submitted but never downloaded |
| 10, 11 | `ancestry_iv_congestion_wages_2026_09_23/_cache/ipums/{core,pre}.csv.gz` (+ `.xml`); that lane is still running |
| 12, 13 | `schooling_selection_position_2026_09_23/_cache/us_mexborn_{acs0004,qeduc}.data.csv.gz` (+ manifests) |

Extract 2, the June decennial panel, is already at
`sources/immigration-fiscal/data/external/ipums/usa_extract/usa_00002.csv.gz`. Extract 1 was
superseded by it.

`~/Downloads/usa_00003…15.csv.gz` are the operator's browser downloads. The lead ran `gzip -t` on
all of them and hashed the complete ones:
- 10–15 pass and are byte-identical to the lane copies.
- 3–9 are truncated partial downloads.

Do not touch the Downloads files. The lead deletes them after checking your catalog.

## Task

1. **Canonical store.** Use `sources/immigration-fiscal/data/external/ipums/usa_extract/`.
   - For each held extract, create a **hard link** (`os.link`; same volume, no copy) named
     `usa_000NN_<slug>.csv.gz`, plus `usa_000NN_<slug>.xml` for its DDI codebook. Where a lane
     holds only a basic `.cbk`, fetch the DDI from the API.
   - Choose short slugs that say sample and universe, e.g. `census1980-2000_men18-40`.
   - Never move, rewrite or delete a lane cache file. Hard links keep every lane's paths
     working, including the running one.
2. **Complete 7 and 8.** Download them through the IPUMS API, using the crime lane's
   `ipums_extract.py` logic or `ipums_api.py`. The key is `IPUMS_API_KEY` in
   `infra/immigration-fiscal/acquire/config.local.env`: source it, never print it, and pipe
   URL-bearing output through `sed -E 's/key=[A-Za-z0-9]+/key=<KEY>/g'`.
   - They are about 150 MB and 130 MB, under the 10 GB preflight threshold.
   - Verify each against IPUMS's published sha256, then hard-link each into the crime lane's
     `_cache/ipums/` as `acs_movers.csv.gz` and `acs_us.csv.gz` so that lane can use them later.
   - If an extract has expired, say so and record it as `expired`.
3. **Catalog.** Fetch every extract definition (1–15) from the API: samples, variables, case
   selections, description. Write `usa_extract/catalog.json` and `usa_extract/CATALOG.md`. One
   row per extract, with:
   - number, file, slug and status (held / superseded / expired);
   - samples, universe in plain words, and the variable list;
   - rows (counted), bytes and sha256;
   - the lane(s) and RESULT.md that used it.

   For each extract, add one line naming the questions it can serve beyond its lane.
4. **Integrate and join.** Convert each held extract to typed Parquet under
   `sources/immigration-fiscal/derived/ipums_usa/`. Build `sources/immigration-fiscal/derived/ipums_usa_extracts.duckdb`
   with one view per extract, a `catalog` table, and join views that attach allocation flags to
   their base files on `YEAR, SAMPLE, SERIAL, PERNUM`: #4 with #6, #3 with #13, #15 with #14 for
   2000, plus any other pair whose universes overlap. Report the match rate of every join and
   gate it: a flag file's records must all find their base, or you explain why not.
   - Row-count gates: Parquet rows equal CSV rows, which equal the DDI or API record count
     where one is given.
   - Check disk first (`df -h`). Parquet should add roughly 1–2 GB.
5. **Register.** Everything the repo tracks lives in `research/` and the lane directory; the raw
   store is git-ignored.
   - Append one card, `IPUMS_USA_EXTRACTS_2026_09_23`, to `research/immigration-dataset-register.md`
     in its existing style. See the IPUMS CPS card near the end, and
     `.agents/skills/dataset-register/SKILL.md`.
   - Append sha256 lines to the untracked `sources/immigration-fiscal/data/MANIFEST.md` in its
     existing format.
   - Append a section to `sources/immigration-fiscal/data/external/ipums/README.md`.
6. **Deliverables.**
   - `infra/immigration-fiscal/ipums_usa_store_2026_09_23/organize.py`: idempotent, prints one
     line per step, and never deletes anything.
   - `README.md` there, opening with `**Verdict:**`: what is held, what was added, the join match
     rates, and what the store can answer that it could not before.
   - Run with `OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb --with pyarrow python3 <script>`
     from the repo root.
   - Do not commit.
