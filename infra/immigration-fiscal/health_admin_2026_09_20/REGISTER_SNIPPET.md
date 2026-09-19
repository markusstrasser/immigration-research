### CMS_SCORECARD_HEALTH_ADMIN_2023_20260920 — Medicaid eligibility and LTSS checks

**Source:** CMS Medicaid and CHIP Scorecard, CMS/Mathematica LTSS tables; Census CPS codebook.
**Acquired:** 2026-09-20.
**Local path:** `infra/immigration-fiscal/health_admin_2026_09_20/raw/` (ignored; worktree release).
**Official:** https://www.medicaid.gov/state-overviews/scorecard/main
**Codebook:** `methodology.pdf` | https://www.medicaid.gov/state-overviews/scorecard/content/scorecard-rel/PerCapitaExpendDataMethod-2025.pdf ; `ltss2023_methodology.pdf` | https://www.medicaid.gov/medicaid/long-term-services-supports/downloads/ltss-users-ident-method-2023.pdf
**Size:** 9 files, 8,224,811 bytes (7.84 MiB), excluding existing MEPS/CPS inputs.
**License/access:** Public federal downloads; no restricted microdata acquired.

**Key variables:** EX.5 state, year, eligibility, dollars/member-year and quality notes; national five-category spending and member-years from Beneficiary Profile page15; observed LTSS spending by state/delivery system; EX.2 fiscal-year spending by program/service. Source pins include API POST bodies and hashes; version ETL3.9.61/data20251205.

**Known quirks:** CY2023 latest EX.5; excludes CHIP/admin/DSH but includes institutions and Medicare premiums. National profile includes territories. MEPS has CHIP, excludes institutions and uses service-payment concepts. LTSS and Scorecard quality ratings differ; California HCBS has high concern in LTSS. EX.2 is FY2023 and its displayed categories do not exhaust its reported total. No origin-specific administrative calibration is supported. Source pins fail on changed raw bytes.

**Used in:** `infra/immigration-fiscal/health_admin_2026_09_20/{builder.py,RESULT.md}`. Existing HC-251 ASCII/SAS/doc and CPS ASEC2024 public CSV ZIP are reused read-only from the main workspace. The builder receipt records exact input hashes.
