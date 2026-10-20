# Number and citation audit failures

## 2026-10-20: adoption after a case's source date

**Symptom:** `citation_freshness.py` stopped with `[BLOCKED] live key and adoption date disagree` for
`oct16`, lane `main_case_2026_10_16`, adopted `2026-10-20`.

**Cause:** the loader treated the case vintage and adoption date as one date. Its lane check, superseded-key
ordering and observed-output completeness check inherited that assumption, so a simple inequality change would
also falsely require the live output key in `superseded`.

**Repair:** derive case identity from the key, validate the lane against it, allow adoption on or after that date,
and compare old keys and observed output vintages against the case date. Package and both payload adoption
metadata must still agree with the manifest; those independent custody checks remain fail-closed.

**Regression:** `test_adoption_can_follow_case_date_without_losing_identity_guards` covers later adoption,
current-vintage output files, adoption before the case date, a lane/key mismatch and a live key in `superseded`.
All four parameter cases passed on 2026-10-20.

Evidence: the v9 adoption brief specifies the October 16 case and October 20 adoption; the pre-fix live gate
returned exit 2 before scanning. This is a validation defect, not evidence of fresh citations.
