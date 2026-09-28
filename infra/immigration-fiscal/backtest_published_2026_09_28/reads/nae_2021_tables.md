claude-opus-5-5

# NAE 2021, "Examining the Economic Contributions of Undocumented Immigrants by Country of Origin": the cells scored

Opened only after the parent's go (commit 0f9eea7 froze the predictions). Source: the original NAE page as archived
by the Wayback Machine, `_cache/aic/wb_nae_undoc_by_country_2021.html`, sha256
`ff404e07f325526c92b24411ff64e6416ebb2061de179921ee95e255e428b14a`
(https://web.archive.org/web/20211227214554id_/https://research.newamericaneconomy.org/report/contributions-of-undocumented-immigrants-by-country/),
accessed 2026-09-28. `score.py` parses the same cells from that file and stops if any differ.

## Person count (the denominator for income per immigrant)

> "Analyzing data from the 2019 American Community Survey, 1-Year Sample, we find that there were more than 4.2
> million immigrants from Mexico who lack legal status in 2019. Together, they make up more than 40.8 percent of the
> 10.3 million undocumented immigrants in the United States." [SOURCE: NAE 2021]

The report states no count of households. Every "households" in the text is unnumbered ("Mexican undocumented
households earned almost $92 billion"; "only half of all undocumented households filed taxes"). The declared rule
therefore scores income per Mexican undocumented immigrant. [CALCULATION: `score.py`, pattern search]

## Headline paragraph

> "In 2019 alone, Mexican undocumented households earned almost $92 billion in household income and contributed
> $9.8 billion in federal, state, and local taxes, even assuming conservative estimates that only half of all
> undocumented households filed taxes. This is in addition to the $11.7 billion in contributions to Social Security
> and $2.8 billion to the Medicare Trust Fund that were made by or on behalf of employers of Mexican undocumented
> immigrants. After taxes, Mexican undocumented immigrants held more than $82.2 billion in spending power, money
> that often goes back into local economies as they spend on housing, consumer goods, and services."
> [SOURCE: NAE 2021]

## Table 4: Economic Contributions of Mexican Undocumented Immigrants by State, 2019 [SOURCE: NAE 2021]

| States | Household Income, in M$ | Federal income taxes, in M$ | State and Local taxes, in M$ | Spending Power, in M$ | Social Security contributions, in M$ | Medicare contributions, in M$ |
|---|---:|---:|---:|---:|---:|---:|
| California | $25,128 | $1,570 | $1,147 | $22,411 | $3,289 | $784 |
| Texas | $21,549 | $1,199 | $1,032 | $19,318 | $2,630 | $632 |
| Illinois | $5,258 | $316 | $320 | $4,622 | $677 | $159 |
| Arizona | $3,541 | $194 | $167 | $3,180 | $438 | $103 |
| Georgia | $2,986 | $159 | $142 | $2,684 | $381 | $90 |
| North Carolina | $3,236 | $194 | $143 | $2,899 | $359 | $96 |
| Washington | $2,892 | $169 | $162 | $2,561 | $388 | $91 |
| Florida | $2,070 | $104 | $85 | $1,881 | $294 | $69 |
| New York | $2,538 | $189 | $155 | $2,194 | $306 | $72 |
| Nevada | $2,287 | $134 | $81 | $2,071 | $286 | $67 |
| United States | $91,992 | $5,396 | $4,391 | $82,205 | $11,689 | $2,798 |

## Table 5: Economic Contributions for the Top 5 Countries of Origin Among Undocumented Immigrants, 2019, Mexico row [SOURCE: NAE 2021]

| Country of Origin | Total Household Income (in Millions $) | Federal Income Taxes (in Millions $) | State & Local Taxes (in Millions $) | Spending Power (in Millions $) |
|---|---:|---:|---:|---:|
| Mexico | $91,992 | $5,396 | $4,391 | $82,205 |

Table 5's Mexico row equals Table 4's United States row. In every row, spending power equals household income less
the two tax columns, to within $1M. [CALCULATION: `score.py`]

## Quantities derived for scoring [CALCULATION: `score.py`, `derived/scores.csv`]

- Income per Mexican undocumented immigrant: $91,992M / 4.2M = $21,903. With the count bounded by 40.8% of
  10.3 million (4.202M), it is $21,890.
- Payroll share: ($11,689M + $2,798M) / $91,992M = 0.1575.
- Federal: 0.0587 of household income. State and local: 0.0477. Spending power: 0.8936.
- State shares of household income: CA 0.273, TX 0.234, IL 0.057, AZ 0.038, NC 0.035, GA 0.032, WA 0.031,
  NY 0.028, NV 0.025, FL 0.023; rest 0.223.
