### CPS_OCT2024_SCHOOL — School enrollment supplement and replicate weights

**Source:** US Census Bureau, Current Population Survey.
**Acquired:** 2026-09-20; public-use download, no registration.
**Local path:** `infra/immigration-fiscal/school_enrollment_2026_09_20/_cache/` (ignored).
**Official:** https://www.census.gov/data/datasets/2024/demo/cps/cps-school-enrollment.html
**Codebook:** `cpsoct24.pdf` | https://www2.census.gov/programs-surveys/cps/techdocs/cpsoct24.pdf
**Size:** Four files, 82,301,431 bytes. Exact source lock in `sources.json`.
**Release:** bulk directory files dated 2025-12-18; reference October 2024.

**Key variables:** `PESSCHOL/PEPUBLIC/PRGRADE` older-student branch;
`PESCH35/PESCH614/PECHPUB/PECHGRDE` child branch; `PWSUPWGT` supplement
weight; `repwgt0..160`; `QSTNUM/OCCURNUM` within-month merge keys;
`PRDTHSP/PENATVTY/PEMNTVTY/PEFNTVTY/PRCITSHP` observed origin categories;
`PRTAGE/GESTFIPS` age and state.

**Known quirks:** Supplement ASCII 126,387 ×1,090 characters, including 27,342
zero-weight nonperson records absent from the 99,045-row replicate file.
Weights have four implied decimals; all 161 official totals supplied in SAS.
Two grade/public-private branches must be combined; basic `PESCHENR` alone
is insufficient. Parent birthplace permits the canonical CPS union but does
not identify distant genealogy. Different survey-month keys are not linkage.

**Used in:** `school_enrollment_2026_09_20/measurement.py` and `builder.py`;
measured enrollment correction with heldout CA/TX and unused ACS/admin checks.
This is a registration snippet only; the parent owns the shared register update.
