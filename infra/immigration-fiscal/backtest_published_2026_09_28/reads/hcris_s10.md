claude-opus-5-5

# CMS HCRIS Worksheet S-10: the line-30 definition, the data file and the year rule

Every source below was read after the parent's go. PREDICTIONS.md required the line-30 definition to come from the
primary pages before scoring. Hashes are in `derived/sources.json`; all accessed 2026-09-28.

## What line 30 is

**The data dictionary** for data.cms.gov's Hospital Provider Cost Report (update of March 2024), variable
"Cost of Uncompensated Care":

> "S10‐Line30‐Column1 — The total cost of non‐Medicare uncompensated care." [SOURCE: CMS, Hospital Provider Cost
> Report Data Dictionary Update,
> https://data.cms.gov/sites/default/files/2024-03/9756088d-5280-4090-80b9-449d31ef25a3/Cost%20Report%20Data%20Dictionary%20Update.pdf]

**The form instructions**, CMS Provider Reimbursement Manual Part 2, chapter 40, §4012.1 (Transmittal 18, 12-22)
[SOURCE: https://www.cms.gov/files/document/r18p240ipdf.pdf, p. 40-80.3 to 40-80.4]:

> "Line 23--Calculate the cost of charity care for columns 1 and 2 by subtracting line 22 from line 21. In column 1,
> enter the cost for uninsured patients and patients with coverage from an entity that does not have a contractual
> relationship (or an inferred contractual relationship for cost reporting periods beginning on or after October 1,
> 2022) with the provider. In column 2, enter the cost for patients covered by a public program or private insurer
> with which the provider has a contractual relationship [...]. In column 3, enter the sum of columns 1 and 2."

> "Line 29--Calculate the non-Medicare and nonreimbursable Medicare bad debt amount. [...] B. For cost reporting
> periods beginning on or after October 1, 2013, calculate the non-Medicare and nonreimbursable Medicare bad debt
> amount as the sum of: non-Medicare bad debt amount on line 28 multiplied by the CCR on line 1, plus
> nonreimbursable Medicare bad debt amount calculated by subtracting line 27 from line 27.01 (this amount is not
> multiplied by the CCR on line 1)."

> "Line 30--Calculate the cost of uncompensated care by entering the sum of line 23, column 3, and line 29."

**The frozen description matches.** PREDICTIONS.md described line 30 as "charity care at cost plus non-Medicare and
non-reimbursable Medicare bad debt at cost". One nuance: the non-reimbursable Medicare bad debt enters without the
cost-to-charge ratio.

**Insured patients' charity care is in line 30.** This was a gap named at the freeze. CMS's S-10 questions and answers:

> "A3. [...] The amounts written off to charity care for insured patients are reported on line 20, column 2 with no
> application of the CCR." [SOURCE: CMS, Worksheet S-10 Q&As following the 2018 IPPS final rule,
> https://www.cms.gov/medicare/medicare-fee-for-service-payment/acuteinpatientpps/downloads/worksheet-s-10-ucc-qandas.pdf]

## The data file and the year

- **Files.** data.cms.gov's Hospital Provider Cost Report is published in annual files, 2011–2023. The four latest
  were fetched: `_cache/hcris/CostReport_{2020..2023}_Final.csv`, with URLs in `derived/sources.json`.
- **What "2023" covers.** Its reports begin between 2022-10-01 and 2023-09-28, so a file year is the federal fiscal
  year in which the cost-reporting period begins. [CALCULATION: `score.py`]
- **Year rule.** The rule was applied to the counts before any state total was formed. Unique reports: 6,059 (2020),
  6,053 (2021), 6,064 (2022) and 6,103 (2023). 2023 is at least 95% of 2022, so Y = 2023. [CALCULATION]
- **Cleaning (the declared rules).**
  - The 2023 file holds 6,103 reports, 6,034 of them in the 50 states and DC.
  - 4,459 of those have a line 30.
  - 21 negative values and 1 value above total costs were dropped, leaving 4,437 reports from 4,407 providers.
    Each provider's reports are summed within the year.
  - 78 reports lack total costs and were kept.

  [CALCULATION: `score.py`, `derived/sources.json` → `parsed.hcris_tally`]
- **National total.** Line 30 over the 50 states and DC is $43.03bn for FY2023. [CALCULATION]
