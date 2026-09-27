### MCBS-CSPUF-2022 — CMS medical spending by payer, unused-year cross-check

**Source:** Centers for Medicare & Medicaid Services. **Acquired:** 2026-09-28.
**Local:** `infra/immigration-fiscal/validation_medical_2026_09_28/_cache/` (ignored;
restorable through the lane's pinned `acquire.py`).
**Official:** [CMS dataset catalog](https://catalog.data.gov/dataset/medicare-current-beneficiary-survey-cost-supplement).
**Codebook:** `CSPUF2022_Codebook.txt`;
[official codebook](https://data.cms.gov/sites/default/files/2025-01/CSPUF2022_Codebook.txt).
**Size:** ZIP 10,208,378 bytes plus codebook 32,191 bytes; 6,621 records, 134 variables.
**License/access:** federal public-use data. **Pins:** data SHA256
`d500832a0d832419f7c5ff23df56d91ee5348bc092d53f0dd7345e01fb699875`;
codebook SHA256 `7b7da7f5f7ded9c5c424e5cd3805c4580179d20c0574348e70af052bce71655e`.

**Fields:** `CSP_AGE`, `CSP_SEX`, `CSP_RACE`, `CSP_INCOME`, payer amounts
`PAMTCARE`, `PAMTMADV`, `PAMTCAID`, full weight `CSPUFWGT`, 100 Fay BRR replicate weights.
**Quirks:** no Mexican origin or birthplace; age/income coarse; facility/hospice users
excluded; service costs adjusted; payer tails replaced by tail means; payer-positive
is not enrollment; PUF IDs cannot link to other years or the survey PUF. The chronic
condition field contains a refusal code, and is not used here. Codebook age and race
frequencies reproduce exactly.
**Used in:** `validation_medical_2026_09_28/analysis.py` and `RESULT.md`.
