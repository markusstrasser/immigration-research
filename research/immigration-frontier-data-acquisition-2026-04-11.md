# Immigration frontier data acquisition update

Date: 2026-04-11

## Purpose

This note records the targeted acquisition pass for the next local-burden modules:

1. `school service complexity`
2. `court and interpreter friction`

It is narrower than the earlier public-MVP acquisition memo. The goal here was to stage public files that can support local-capacity analysis rather than lifetime-fiscal microsimulation.

## Acquired and verified

### 1. Census `SAIPE` 2023 school-district files

Downloaded to:
1. [ussd23.txt](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage4/saipe/ussd23.txt)
2. [ussd23.xls](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage4/saipe/ussd23.xls)
3. [2023-district-layout.txt](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage4/saipe/2023-district-layout.txt)

Official sources:
1. [SOURCE: https://www.census.gov/data/datasets/2023/demo/saipe/2023-school-districts.html]
2. [SOURCE: https://www2.census.gov/programs-surveys/saipe/datasets/2023/2023-school-districts/ussd23.txt]
3. [SOURCE: https://www2.census.gov/programs-surveys/saipe/datasets/2023/2023-school-districts/ussd23.xls]
4. [SOURCE: https://www2.census.gov/programs-surveys/saipe/technical-documentation/file-layouts/school-district/2023-district-layout.txt]

Why this matters:
1. `SAIPE` gives a clean public district-level child-count anchor for local school-burden sizing.
2. It is an easier direct-file source than many NCES endpoints.

### 2. Court and language-access documents

Downloaded to:
1. [ca_language_need_interpreter_use_2025.pdf](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage4/courts/ca_language_need_interpreter_use_2025.pdf)
2. [wa_interpreter_reimbursement_2025_2027.pdf](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage4/courts/wa_interpreter_reimbursement_2025_2027.pdf)
3. [nyc_local_law_6_report_2024.pdf](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage4/courts/nyc_local_law_6_report_2024.pdf)

Official sources:
1. [SOURCE: https://languageaccess.courts.ca.gov/system/files/2025-07/2025%20Language%20Need%20and%20Interpreter%20Use%20Study.pdf]
2. [SOURCE: https://www.courts.wa.gov/content/Financial%20Services/documents/2025_2027/Biennial/BD%20Stabilize%20Interpreter%20Reimbursement%20Program.pdf]
3. [SOURCE: https://www.nyc.gov/assets/immigrants/downloads/pdf/Local-Law-6-Report_MOIA_2024.pdf]

Why this matters:
1. These are concrete operational-cost documents for language access, interpreter staffing, and reimbursement pressure.
2. They are useful for the `court and interpreter friction` branch even though they are not immigrant-status-specific microdata.

### 3. NCES CCD file-tool artifacts for current `LEA` releases

Downloaded to:
1. [nces_ccd_file_tool_lea_2023_2024_v1a.json](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage4/nces/nces_ccd_file_tool_lea_2023_2024_v1a.json)
2. [ccd_lea_029_2324_w_1a_073124.zip](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage4/nces/ccd_lea_029_2324_w_1a_073124.zip)
3. [SY_2023-24_Universe_1a_CCD_Nonfiscal_Release_Notes.docx](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage4/nces/SY_2023-24_Universe_1a_CCD_Nonfiscal_Release_Notes.docx)
4. [SY_2023-24_Final_1a_Data_Notes.xlsx](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage4/nces/SY_2023-24_Final_1a_Data_Notes.xlsx)
5. [SY_2023-24_LEA_Membership_Companion_2024-252.xlsx](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage4/nces/SY_2023-24_LEA_Membership_Companion_2024-252.xlsx)

Official sources:
1. [SOURCE: https://nces.ed.gov/ccd/files.asp]
2. [SOURCE: https://nces.ed.gov/ccd/datatables/api/File/2/5/38/7/10/38]
3. [SOURCE: https://nces.ed.gov/ccd/Data/zip/ccd_lea_029_2324_w_1a_073124.zip]
4. [SOURCE: https://nces.ed.gov/ccd/doc/SY_2023-24_Universe_1a_CCD_Nonfiscal_Release_Notes.docx]
5. [SOURCE: https://nces.ed.gov/ccd/xls/SY_2023-24_Final_1a_Data_Notes.xlsx]
6. [SOURCE: https://nces.ed.gov/ccd/xls/SY_2023-24_LEA_Membership_Companion_2024-252.xlsx]

Important finding:
1. The file tool exposes an authoritative JSON endpoint for current `LEA` files, so acquisition does not need brittle filename guessing. [SOURCE: https://nces.ed.gov/ccd/datatables/api/File/2/5/38/7/10/38]
2. In the saved `2023-24` `LEA` `v1a` response, the surfaced district data-file components were `Directory`, `Membership`, and `Staff`. [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage4/nces/nces_ccd_file_tool_lea_2023_2024_v1a.json]
3. The small companion workbook confirms the district membership file is a `15`-variable grade/race/sex membership table, not an English-learner table. [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage4/nces/SY_2023-24_LEA_Membership_Companion_2024-252.xlsx]

## What was probed but not cleanly acquired

### 1. Current district-level `English learner` counts

What is true:
1. NCES public documentation still says nonfiscal CCD includes `Counts of Children with disabilities and English learners (LEA)`. [SOURCE: https://nces.ed.gov/ccd/files.asp]
2. The older `pubagency.asp` pages show explicit historical `English Learners` LEA files such as `ccd_lea_141_1718_l_1a_083118.zip`. [SOURCE: https://nces.ed.gov/ccd/pubagency.asp]
3. In this pass, the current `2023-24` file-tool response did not surface a separate district `English Learners` component. [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage4/nces/nces_ccd_file_tool_lea_2023_2024_v1a.json]

Inference:
1. [INFERENCE] There is a documentation-to-distribution mismatch for current public district `EL` counts, or the relevant file path is exposed through a different route than the `LEA` `v1a` file-tool query used here.

Status:
1. unresolved
2. do not claim current district `EL` counts are already staged locally

### 2. Ed Data Express CSV export

What happened:
1. The page source exposed a plausible CSV export route and confirmed `Title III students served` metadata.
2. Direct command-line export attempts returned an HTML landing page rather than CSV.

Sources:
1. [SOURCE: https://eddataexpress.ed.gov/download/data-builder/data-download-tool]

Status:
1. `HTML trap`
2. not worth escalating into browser automation unless a human explicitly wants that route

### 3. `TRAC` immigration report pages

What happened:
1. Public report URLs resolved to the newer site shell or migration notice rather than a clean dataset endpoint.
2. No stable public CSV or JSON path was found in this bounded pass.

Sources:
1. [SOURCE: https://trac.syr.edu/immigration/reports/637/]
2. [SOURCE: https://trac.syr.edu/immigration/reports/558/]

Status:
1. not pursued further in this pass

## Practical next step

The best next move is not more generic scraping.

It is:
1. use `SAIPE` immediately for district child-concentration overlays
2. use the court/language-access PDFs to draft an operational-cost memo
3. do one more bounded NCES pass specifically for current district `EL` counts, using the file-tool API or `ELSi`, and stop if the path remains indirect

## Bottom line

This pass succeeded at staging the easiest high-value public local-capacity files.

The strongest new acquisition result is:
1. `SAIPE` is on disk
2. court/interpreter source PDFs are on disk
3. the current NCES CCD file-tool API path is now known and saved locally

The main unresolved item is narrower than before:
1. the exact current public route to district-level `English learner` counts
