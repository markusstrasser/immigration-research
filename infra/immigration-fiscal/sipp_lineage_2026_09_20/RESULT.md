**Verdict:** Stop this public SIPP route for the requested Mexican nonidentifier outcome correction. The country fields have been coarsened to world regions, and the executed generic-generation adult samples are too small and selected to close the main gap. This is a documented negative result, not proof that deeper restricted SIPP data contain no useful information.

## Correction to the previous frontier memo

The previous [ancestry-outcomes discovery memo](../../../research/immigration-ancestry-outcomes-evidence-2026-09-20.md) overread the labels `TBIOMOMNAT` and `TBIODADNAT` as usable country codes. That claim is superseded by their actual value definitions: both release only US incl Puerto Rico/island areas, Europe, Asia/Pacific, Americas/Caribbean, Africa, Oceania, Other. Own `TBORNPLACE` also pools foreign birth into regions. Thus linking a respondent to a parent or grandparent **cannot establish Mexican birthplace from these public variables**. Mexican identification and Mexican birthplace are separate evidence.

Principal source: [2025 SIPP Data Dictionary](https://www2.census.gov/programs-surveys/sipp/tech-documentation/data-dictionaries/2025/2025_SIPP_Data_Dictionary.pdf), printed pp. 884–885 (own birth), 2812–2813 (parent birth); [2024 dictionary](https://www2.census.gov/programs-surveys/sipp/tech-documentation/data-dictionaries/2024/2024_SIPP_Data_Dictionary.pdf), printed pp. 886–887 and 2816–2817 confirms the same boundary in the preceding release. PDF indexing is zero-based; printed pages are one greater. An independent three-column scan of every record in the local 2024 (437,168 rows) and 2023 (476,744 rows) files confirmed exactly the same own-country region codes 61–66 and parent codes 1,3–8. The 2025 raw file also contains two TBORNPLACE=99 unknown cases, explicitly allowed as unknown by the guard.

## Executed 2025 audit (reference year 2024)

Read the local official ZIP once, selecting columns; did not redownload. Source SHA-256: `570798a6f512c8f82af311ee01a1668d178063c9076c18a05bc3a5a0039b67ed`. There are 379,215 person-months, 32,052 distinct people and 31,364 positive-weight, in-frame December people. Target selection counts people once, not twelve monthly records.

| Mexican-identifying target | Generic G3 n | G3 Kish n_eff | Generic G4+ n | G4+ Kish n_eff | G3+ unresolved n |
|---|---:|---:|---:|---:|---:|
| Age 18+, released fields | 61 | 42.6 | 35 | 28.4 | 633 |
| Age 25–64, released fields | 28 | 19.4 | 16 | 12.3 | 423 |
| Age 18+, birth/parent-link flags as reported | 52 | 36.5 | 20 | 17.8 | 508 |
| Age 25–64, birth/parent-link flags as reported | 23 | 15.8 | 8 | 7.0 | 332 |

Kish n_eff measures weight concentration only; these are not survey-design effective sample sizes or confidence intervals. Sensitivity categories are not fixed cohorts: records failing required flags move into unresolved nearer-generation categories, so the unresolved column can decrease when parent nativity becomes unknown.

The generic-G3 identification requires focal US birth, two US-born biological parents and at least one foreign-born grandparent; it does not prove that grandparent was Mexican. Generic G4+ requires four US-born grandparents and does not identify exact G4 vs G5+. The comparison is conditional on **reported Mexican identity** (`EORIGIN=1, EHISPAN=1`). US birth uses `EBORNUS` / `EBIOMOMUS` / `EBIODADUS`, not the broader citizenship-based ACS-native concept.

Only 22 of the 61 adult generic-G3 identifiers have all four grandparent nativity fields; an observed foreign grandparent is sufficient to establish generic G3 once both parents are known US-born. All 35 G4+ cases have four observed US-born grandparents by definition.

No income contrast was fitted. Among the age25–64 identifier samples there are only 21 positive-earner G3 records and 10 positive-earner G4+ records, with 3 vs 1 SNAP-covered records, 0 vs 0 TANF-covered and 2 vs 2 SSI records. Zeros do not establish absence in the population. The selected coresident family sample and tiny benefit cells make a precise later-generation fiscal comparison indefensible.

Nonidentifiers: across adult non-Hispanic records, the audit found just **one** generic-G3 person and **three** generic-G4+ people with a linked biological parent reporting Mexican identity in the released data. These are parent–child identification discrepancies, not verified Mexican-born-grandparent descendants or an ethnic-attrition rate. No outcomes for those tiny cells are presented in the narrative.

## Source fields and checks

- Household links: `SPANEL + SSUID + PNUM`; `EPNPAR1/2`, `EPAR1/2TYP=1` for biological parents; mother/father branch resolved using parent `ESEX` (male1, female2), ambiguous branches remain missing. Parent IDs are taken from the current interview roster; monthly EHC links and cross-release history were not added.
- US birthplace: direct `EBORNUS`; parental `EBIOMOMUS`, `EBIODADUS`; resident-parent own birth fills a missing report. Contradictory direct and linked reports stay unknown. Grandparents are linked parents' own parental reports or their resident-parent records.
- Imputation sensitivity: each used birthplace and parent ID/type allocation flag must be **1 = in universe, as reported**. **0 means not in universe**, not unimputed. This sensitivity does not exclude imputed sex or identification and is labeled accordingly.
- The code asserts unique person-month keys and invariant person fields within the annual file, validates region-code supports to prevent Mexico-from-Americas mistakes, and leaves missing birthplace unknown. Source-code compile check passed. Reusing the selected-column cache requires a matching input SHA-256 and exact column schema in a paired `.cache.json`; otherwise it rereads the source.
- Weighted coverage aggregates use December `WPFINWGT`; no annual exposure is manufactured. Earnings and benefit flags are only counted for support, with no individual amounts published. Benefits are coverage flags, not a full fiscal balance.

Other primary code definitions: same 2025 dictionary, printed p.6 (allocation flags), pp.889–890 (Hispanic identity), pp.919–922 (parent links/type), p.927 (sex).

## Files and stopping rule

- Portable generator: [`audit.py`](audit.py).
- Aggregate cells: ignored `derived/sipp-lineage-2025.csv`.
- Source hash, row counts, field distributions: `derived/sipp-lineage-2025.json`.
- Earlier-release probes: `derived/country2024.json`, `derived/country2023.json`; generator [`country_probe.py`](country_probe.py) with `--zip` and `--out`.
- Ignored selected-column cache: `derived/sipp-lineage-2025.parquet` (microdata; not an output for publication).

Reproduce from repository root: `UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run --no-project --with pandas --with numpy --with pyarrow python3 infra/immigration-fiscal/sipp_lineage_2026_09_20/audit.py --zip sources/immigration-fiscal/data/external/stage3/census/sipp_2025/pu2025_csv.zip --out infra/immigration-fiscal/sipp_lineage_2026_09_20/derived/sipp-lineage-2025`.

Covered: latest2025 annual microdata, reference year2024; 2024 codebook and complete three-column scans of2023/2024 raw files to check whether earlier files could restore country. Skipped2024/2023 full lineage reconstruction and cross-wave linkage because those do not repair the crucial country suppression; no further identifier-only model fitted. This is a stop on the requested *Mexican lineage/nonidentifier outcome correction*, not a claim that all longitudinal generic-nativity analyses are futile.
