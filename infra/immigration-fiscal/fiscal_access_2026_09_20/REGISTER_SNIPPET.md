### MCBS_COST_PUF_2023 — Community Medicare expenditure validation

**Source/acquired:** CMS;2026-09-20. Public microdata; no DUA or purchase.
**Local:** `infra/immigration-fiscal/fiscal_access_2026_09_20/_cache/CSPUF2023_Data.zip`; codebook/methodology alongside. Manifest pins sources, bytes, hashes and ZIP members.
**Official:** https://www.cms.gov/data-research/research/medicare-current-beneficiary-survey
**Shape:**6,920 unique people ×134fields;100replicate weights; validated by`validate_mcbs.py`.
**Key variables:** age3groups,sex,race/Hispanic4groups,income2groups,chronic conditions;total/Medicare/Medicaid/MedicareMCO/private/OOP/other payments;service categories;`CSPUFWGT`,`CSPUF001–100`.
**Limits:** community entire year; excludes any facility/hospice/institution events/costs;cost/event topcode99.5%;no Mexico/birthplace/parents;no linkage to otherMCBS files,years orclaims. Useful community-cost validation,not origin-specific administrative fiscal account.
**Restricted status:** CPS–SSA/IRS and detailed TAF/MBSF/claims access routes documented in laneRESULT;none acquired. Do not count access documentation as data.
