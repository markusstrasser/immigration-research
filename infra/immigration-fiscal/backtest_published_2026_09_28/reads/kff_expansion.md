claude-opus-5-5

# KFF: Medicaid expansion implementation dates (governing the check-3 indicator)

Source: KFF, "Status of State Medicaid Expansion Decisions" (published 21 August 2026),
https://www.kff.org/affordable-care-act/issue-brief/status-of-state-medicaid-expansion-decisions/, which embeds the
map whose data file is https://datawrapper.dwcdn.net/ZJUAA/5/dataset.csv (`_cache/kff/dw_ZJUAA_5_dataset.csv`),
accessed 2026-09-28. The page text: "To date, 41 states (including DC) have adopted the Medicaid expansion and 10 states
have not adopted the expansion." [SOURCE: KFF]

The rows that decide the frozen rule (not expanded if not implemented by 1 July of the year)
[SOURCE: KFF map data, column "Expansion Implementation Date"]:

| State | Expansion Status | Expansion Implementation Date |
|---|---|---|
| AL, FL, GA, KS, MS, SC, TN, TX, WI, WY | Not adopted | (blank) |
| Missouri | Adopted and implemented | "Processing applications beginning 10/1/2021 with coverage retroactive to 7/1/2021" |
| Oklahoma | Adopted and implemented | "Implemented expansion on 7/1/2021" |
| South Dakota | Adopted and implemented | "Implemented expansion on 7/1/2023" |
| North Carolina | Adopted and implemented | "Implemented expansion on 12/1/2023" |
| Nebraska | Adopted and implemented | "Implemented expansion on 10/1/2020" |

Not expanded by 1 July 2023 (Y = 2023): AL, FL, GA, KS, MS, NC, SC, TN, TX, WI and WY. This is identical to the
frozen 2023 list in `PREDICTIONS.md`. South Dakota counts as expanded, having implemented on 1 July 2023, and North
Carolina as not expanded. [CALCULATION: `score.py`, `kff_not_expanded(2023)`]
