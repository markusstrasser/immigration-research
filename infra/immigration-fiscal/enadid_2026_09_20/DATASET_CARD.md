### INEGI_ENADID_2018_2023 — Mexico migration and resident histories

**Source:** Instituto Nacional de Estadística y Geografía (INEGI)
**Acquired:** 2026-09-20
**Local path:** `infra/immigration-fiscal/enadid_2026_09_20/_cache/`
**Official:** https://www.inegi.org.mx/programas/enadid/2023/ and https://www.inegi.org.mx/programas/enadid/2018/
**Codebooks:** `metadata2023.xml`, `metadata2018.xml`, embedded CSV dictionaries/catalogs; household questionnaires for both waves,2023 sampling design and interviewer conceptual manual.
**License:** Public direct download; INEGI free-use terms permit copying/distribution with preserved metadata and attribution, disclosed transformations and no implied endorsement. Archived `terminos.html`.

**Key variables:** TMigrante P4_11 destination, P4_10_* departure date, P4_15 current residence, COND_RESID return status; TSDem prior five-year residence and birthplace; FAC_VIV/FAC_HOG weights; EST_DIS/UPM_DIS design; LLAVE_* joins. See README field mapping; question numbers and migration weight differ between waves.

**Known quirks:** Household-reported departures miss entire households no longer represented. Recent-departure returnees are not all return migrants. Resident prior-residence questions cover age5+ and endpoints. Mexico-born return migration must exclude US-born/other-born people for a birthplace-consistent estimand. No bilateral net estimate is yet computed. Examples are weighted survey estimates without intervals.

**Used in:** `validate.py` acquisition checks and separate weighted examples. No causal or net-migration conclusion claimed. See `sources.json` for bytes/hashes/archive members and `derived/validation.json` for rows/schema validation.
