# ENADID 2018 and 2023 public microdata

Official INEGI open-data bundles acquired on 2026-09-20 to supply the Mexico-side evidence missing from US-only migration cohorts. This acquisition is a pair of surveys, not an annual net-migration series.

## Reproduce

Run from the lane directory (Python standard library only):

```sh
uv run --no-project python3 acquire.py
uv run --no-project python3 inspect_metadata.py
uv run --no-project python3 validate.py
uv run --no-project python3 -O test_acquisition.py
```

`acquire.py` HEAD-probes before downloads, records statuses/headers/bytes/SHA256, checks ZIP CRC and PDF signatures, and preserves completed raw files read-only. INEGI individual streams can be slow. `range_download.py 2023` is the bounded eight-connection fallback; it requires HTTP206 and exact Content-Range/length, then validates the assembled ZIP. Raw files and reproducible outputs are under `_cache/` and `derived/` respectively. `sources.json` is the canonical provenance manifest; `derived/validation.json` contains exact microdata member names/hashes, row counts and key/weight checks. Generated field mappings come from official DDI XML; original CSV dictionaries and category catalogs are also contained within each complete bundle.

The frozen `sources.json` hashes are authoritative. Cached inputs are verified before reuse; new downloads must match before promotion. A changed source fails loudly and its partial is preserved. Neither downloader silently refreshes the frozen manifest or overwrites a completed input. Validation uses explicit exceptions that remain active under Python `-O`.

## What each table measures

`TMigrante`: people reported by sampled Mexico households as having departed to live, study or work abroad during the five-year reference window, including those who returned. It misses emigrants not represented by reporting households, including whole-household departures. Returnees in this table belong to the recent departure cohort; they are **not all US-to-Mexico returnees**.

`TSDem`: people currently resident in sampled Mexican households. Prior residence five years earlier locates US-to-Mexico moves between endpoints, including older departure cohorts. It omits under-five children from this question, people who died, and intermediate moves ending back in the starting country. Retain Mexico-born, US-born and other birthplace groups separately.

Do not subtract these examples and label the result net Mexican migration. Household-reported departures and resident endpoint transitions have different coverage. Align periods, ages, birthplaces, household loss/return and US survey residence rules before a bilateral estimate. Survey estimates require design-based uncertainty; example counts here have no calculated intervals.

## Field mapping

| Construct | 2018 | 2023 |
|---|---|---|
| Departure destination US | TMigrante `P4_11=1` | same |
| Departure time | `P4_10_1`, `P4_10_2` | same |
| Current migrant country | `P4_15` | same |
| Returned within departure cohort | `COND_RESID=1` | same |
| Migrant weight | `FAC_VIV` | `FAC_HOG` |
| Resident weight | TSDem `FAC_VIV` | same |
| Resident US five years before | `P3_19=3` (August2013) | `P3_24=3` (August2018) |
| Resident Mexico-born | `P3_7` in1,2 | `P3_10` in1,2 |
| Unique person/migrant keys | `LLAVE_PER`, `LLAVE_MIG` | same |
| Survey design | `EST_DIS`, `UPM_DIS` | same |

Question numbers drift between waves. `ESTRATO` is socioeconomic stratum and does not replace the sampling-design stratum `EST_DIS`. IDs are strings, not numeric quantities. Do not use a woman-specific fertility weight for migration totals.

## Sources, terms and scope

- [ENADID2023](https://www.inegi.org.mx/programas/enadid/2023/), [ENADID2018](https://www.inegi.org.mx/programas/enadid/2018/).
- [Official2023 DDI](https://www.inegi.org.mx/rnm/index.php/metadata/export/981/ddi), [official2018 DDI](https://www.inegi.org.mx/rnm/index.php/metadata/export/554/ddi).
- [Terms](https://www.inegi.org.mx/inegi/terminos.html): free use includes copying/distribution, adaptation and commercial use. Preserve metadata, credit INEGI and source/date, disclose transformations, and do not imply INEGI endorsement. This is INEGI free-use permission, not a claim of US public-domain status.

Household questionnaires for both waves, full2023 interviewer conceptual manual and sampling design, DDI dictionaries for both waves, embedded CSV dictionaries/category catalogs,2023 results and archived terms are acquired. All tables in both bundles are preserved; this lane validates the migration/resident pair, not fertility/women modules. No external contact or paid service was used.

Pre-download checks found no ENADID/TMigrante files in the topic data root, topic register, intel dataset directory/inventory/tool registries, or accessible SSD corpus. A default sandbox DNS failure required the authorized network route. Incorrect RNM `/catalog/981/export` returned500; the official linked `/metadata/export/981/ddi` worked. Use the latter. Source landing pages require dynamic rendering but expose the official ZIP URL in JSON-LD.
