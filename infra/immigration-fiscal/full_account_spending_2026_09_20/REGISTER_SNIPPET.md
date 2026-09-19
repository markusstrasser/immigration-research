### FULL_CURRENT_SPENDING_2024_20260920 — Exhaustive BEA account with conditional incidence

**Source:** BEA NIPA3.1/3.12/3.13/3.17; Census CPS2025/population2024; AHRQ MEPS2024; existing measured-school outputs.
**Recorded:** 2026-09-20; all raw files reused locally read-only.
**Local generator:** `infra/immigration-fiscal/full_account_spending_2026_09_20/`.
**Official:** https://apps.bea.gov/national/Release/XLS/Survey/Section3All_xls.xlsx
**Codebooks:** https://www.bea.gov/resources/methodologies/nipa-handbook ; Census/AHRQ document URLs in `SOURCE_PINS.json`.
**Size:** 5 existing primary files, 156,789,838 bytes; **zero newly downloaded raw bytes**. Upstream derived school file separately hashed, not counted as primary raw.
**Access:** Public federal releases; no restricted data or external uploads.

**Key variables:** 42 disjoint spending categories; $10,061.458bn CY2024 current national expenditure; target/other/external/unallocated amounts; positive-key exposures and denominators; personal/shared allocation; F average/fixed attribution; every proxy alternative. Ten allocation/scenario combinations (two attribution rules × five scenarios).

**Known quirks:** Complete arms are conditional proxy assignments, not administrative origin measurements. Domestic outside-CPS allocation is a population proportional assumption; unexplained health residuals are not reclassified as institutions. Explicit foreign/territory flows stay external. Table3.17 consumption is net of sales and excludes gross investment. Federal grants are consolidated once by BEA. Represented-only diagnostic retains unallocated residuals. Fixed-cost attribution does not identify fiscal response.

**Used in:** `builder.py`, `CONTRACT.md`, parent complete-account sensitivity integration. Generator receipts fingerprint every raw/upstream-derived source and output.
