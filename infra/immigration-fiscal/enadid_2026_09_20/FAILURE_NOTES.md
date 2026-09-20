# Acquisition and parsing evidence

- Sandbox DNS resolution failed for INEGI; authorized network execution worked. Treat this as environment transport, not missing data.
- RNM `/catalog/981/export` returned500. Official linked `/metadata/export/981/ddi` returned the usable codebook;2018 uses554. Both XMLs parsed and yielded148/155 selected field definitions.
- INEGI single HTTP streams were slow. Fallback uses eight concurrent bounded byte ranges, requires status206/exact Content-Range, validates each length and whole ZIP CRC.2023 ranged and normal download hashes independently agree.
-2018 contains `bitacora_de_cambios_tmigrante.csv` beside the real data file. Generic directory/extension matching was ambiguous and the validator stopped. Fix: basename must start `conjunto_`, and exactly one candidate is mandatory. Regression check: both2018 and2023 actual ZIPs now select the four intended members, with pinned row counts, unique keys and source hashes. Do not delete the source change log.
- DDI file names have whitespace and `.NSDstat` suffixes. Normalize these only for mapping; retain original XML. Zero selected definitions fails loudly.
- Native code review reproduced an unknown source argument returning success with an empty receipt. Acquisition now rejects unknown/empty selections before receipt writes; `test_acquisition.py` checks the failure under optimized Python.
- Native review reproduced a concurrent writer's completed file being replaced during download publication. Both ENADID routes now use unique partial files and exclusive hard-link installation; the same raw-publication repair covers the detention downloader. A raced completed destination is preserved and the competing run fails. Regression fixtures inject this interleaving without network access.
