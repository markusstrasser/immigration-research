**Verdict:** Both authorized ENADID waves are acquired and the migration/resident tables verified against actual public microdata. The package contains12 source files totaling118,976,710 bytes, including complete2018 and2023 open-data bundles, codebooks, questionnaires,2023 methodology and archived terms. This fills the Mexico-side data acquisition gap; it does not yet establish a harmonized bilateral net-migration estimate.

## Verified coverage

| Wave | TMigrante records / columns | TSDem records / columns | ZIP bytes |
|---|---:|---:|---:|
| 2018 | 2,611 /55 | 385,978 /93 | 49,551,192 |
| 2023 | 3,660 /52 | 359,018 /103 | 42,898,941 |

All12 downloaded sources have verified SHA256; both ZIPs pass CRC; both table types in both waves have nonempty rows, unique declared record keys and strictly positive weights.2023 ZIP independently downloaded by full stream and21 validated byte ranges produced the identical SHA256 `248836ef8d4b74dda66d855b390e3557cdc79a1d487cd957b2273baa93ac4485`. Field mappings retain code/category definitions from official DDI and archive dictionaries.

## Weighted examples, kept as distinct objects

| Object | ENADID2018 | ENADID2023 |
|---|---:|---:|
| Reported US-destination departures during reference window | 645,458 | 1,072,331 |
| Returned members of that US-destination departure cohort | 220,218 | 215,021 |
| Current Mexican residents age5+ who lived inUS five years earlier, all birthplaces | 392,451 | 304,005 |
| Same resident endpoint measure, Mexico-born only | 300,976 | 238,190 |

Examples use FAC_VIV except2023 TMigrante, which uses FAC_HOG. The2023 US-destination share is87.917% (1,072,331 /1,219,710), reproducing the official results PDF’s rounded87.9%. The first two rows concern departures sinceAugust2013 orAugust2018, respectively, through the survey; the last two concern residence inAugust2013 orAugust2018 versus current survey residence. These are weighted point estimates without intervals. They are not interchangeable flow counts. Do not subtract them and report net migration. A full net exercise must align coverage and include movements not represented by these household retrospective questions.

## Repository location and reproduction

The repository lane is `infra/immigration-fiscal/enadid_2026_09_20/`. Raw `_cache/` and generated `derived/` are ignored. `sources.json` contains authoritative URLs, dates, HTTP status/headers, bytes, SHA256 and archive members. See README.md for acquisition and validation commands.

Commands run successfully: `uv run --no-project python3 inspect_metadata.py`; `uv run --no-project python3 validate.py`; Python compile checks on all acquisition/validation scripts. The migration source requires no Python package beyond standard library. Generated artifacts and their hashes are in `derived/output_hashes.json`.

Final hardening verified with Python `-O`: cached `acquire.py`, cached `range_download.py 2023`, and full `validate.py` succeeded. All guards are explicit exceptions; empty/duplicate/incomplete source manifests, changed frozen bytes and ambiguous/empty data selection fail. Completed inputs are preserved, and mismatch downloads never replace them.

## Limits and skipped coverage

Both complete bundles preserve all bundled tables and category dictionaries. Validation focuses on TMigrante and TSDem; fertility/women/household/housing tables were not analytically validated because unrelated to the bounded migration task.2018 detailed interviewer manual and standalone sampling-design PDF were not separately downloaded;2018 DDI and household questionnaire plus embedded dictionaries are present. No other wave, new net model, acquisition outside INEGI, contact, spend, repo mutation or commit occurred. User authorization covered actual acquisition. Parent owns registration/index integration.
