claude-opus-5[1m]

**Verdict:** all 14 parameter groups fetched from primary sources and written to `params/params.json`; 252 entries verified, 13 unverified with `value: null`. Ready for the builder.

- Per group verified/unverified: omb 62/0 · enforcement 37/0 · meps_coverage 25/0 · city_migrant 22/1 · state_medicaid_undocumented 16/6 · corporate 17/1 · k12 14/2 · unauthorized 12/0 · ell 12/0 · underreporting 12/3 · improper_payments 9/0 · veterans_federal_retirement 6/0 · deflator 5/0 · population 3/0.
- 48 files staged under `~/research-data/immigration-fiscal/data/external/` with sha256 and parsing notes. Nothing committed; nothing edited outside `params/`.
- Every key your `params_placeholder.json` expects now exists, under your naming and units, as an ALIAS KEY pointing at the canonical entry. Your `ratio_*` are admin/survey, so they are the inverse of the published survey/admin ratios; I inverted them for you.
- Two placeholder values were wrong years: EITC improper payments FY2024 is 15,941.61 M (21,900 is FY2025); ACTC FY2024 is 3,446.56 M.
- `underreporting.ratio_housing` is null and must stay null. Neither Meyer et al. paper covers housing assistance. Do not substitute SNAP's ratio.
- `omb.subf_551_health_care_services` is NOT Medicaid — the OMB classification has no Medicaid subfunction. For Medicaid use `meps_coverage.nhea_2023_medicaid_federal` (592.6 USD billions).
- `meps_coverage.nhea_to_meps_ratio_*` reaches the ADJUSTED NHEA, which already excludes nursing homes, the institutionalized and non-patient revenue. Reference year 2012; no later reconciliation exists.
- DHS FY2025 Budget in Brief is staged as a trap marker only — its FY2024 column is an annualized CR. Use the FY2026 BIB and FY2026 CJs, which carry "FY 2024 Enacted".
- CCD membership CSV is long format: filter `TOTAL_INDICATOR` before summing `STUDENT_COUNT`, treat blanks as missing not zero, join `LEAID` to F-33 `NCESID`.
