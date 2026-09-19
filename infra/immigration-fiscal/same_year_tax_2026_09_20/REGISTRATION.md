# Registration handoff

Parent owns the shared catalog and index. Suggested entry:

| Dataset / release | Local source | Use / limitations |
|---|---|---|
| CPS ASEC 2024, calendar income 2023, public CSV + 160 replicates | Existing `sources/immigration-fiscal/data/census/cps_asec_2024_march.zip`; identical lane `_cache/asecpub24csv.zip` | Native `TAX_ID`, observed payload carriers, dependent filers; 560 zero-income filing units require explicit count convention/bounds; no observed IRS filing or coverage identifier. |
| IRS SOI 2023 complete Tables 1.2 and 1.4 | Lane `_cache/23in12ms.xls`, `23in14ar.xls` | 19 AGI bands, return counts, AGI, taxable income, liability, total/W-2 wages; source dollar cells are thousands. |
| IRS SOI 2022 complete Tables 1.2 and 1.4 + Pub4801 June2026 | Lane `_cache/22in12ms.xls`, `22in14ar.xls`, `p4801.pdf` | Demonstrates that Pub4801 p.9 anchors are exactly2022 despite2023 text; retain earlier findings with corrected year. |
| SSA 2025 Supplement 4.B10/4.B12, income2023 | `ssa_sources.json` pinned primary transcription | OASDI/HI wages/SE, US all-area/CA/TX/PR/other; preliminary 1% CWHS, no ethnicity; direct403, primary page read via web. |
| ACS2024 one-year person PUMS, 80 replicates | Existing `sources/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip` | Common civilian household wage distributions; `STATE`, `HISP=2`, `POBP=303`; rolling income/ADJINC; cannot reconstruct CPS parental-origin union. |

Generator: `infra/immigration-fiscal/same_year_tax_2026_09_20/`; detailed source hashes and source URLs in `source_lock.json`, checks and limitations in README. Raw data and derived tables remain ignored; all output is reproducible. The historical local CPS2024 pointer is usable and must not be described as unavailable.
