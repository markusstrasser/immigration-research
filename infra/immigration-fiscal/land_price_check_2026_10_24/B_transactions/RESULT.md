DeepSeek V4.1 Flash 1017 (DeepInfra US)

**Verdict:** Priced all five counties from land-transaction research, not from FHFA land data. The primary figure for every county is the metro/PMSA land value per acre in Albouy, Ehrlich & Shin (2018), estimated from CoStar vacant-land sales in 2005-2010, converted to 2024 with the Case-Shiller metro index (Los Angeles, Orange, San Diego) or CPI-U (San Bernardino, Santa Clara — those metros have no Case-Shiller index). A second, independent CoStar-based estimate (Gyourko & Krimmel 2021, single-family development land, 2013-2018) corroborates Los Angeles, San Bernardino and Santa Clara and is reported in `notes`. Every number below is traceable to a table cell in the downloaded files; nothing is imputed or guessed.

| FIPS | County | $/acre 2024 | n sales | Measured | Second independent estimate (2024 $/acre) |
|---|---|---|---|---|---|
| 06037 | Los Angeles | **5,336,514** | 1,760 | 2005-2010 | 3,908,592 |
| 06059 | Orange | **5,252,329** | 233 | 2005-2010 | — |
| 06073 | San Diego | **2,391,962** | 957 | 2005-2010 | — |
| 06071 | San Bernardino | **479,076** | 2,452 | 2005-2010 | 516,479 |
| 06085 | Santa Clara | **3,553,718** | 217 | 2005-2010 | 1,857,392 |

`low`/`high` are blank in `prices.csv`: neither source publishes an interquartile range or a range for the metro-level average value per acre, and I did not invent one.

## What the sources measure

**Albouy, Ehrlich & Shin (2018).** They estimate a transaction-based land-value surface for each U.S. metro from CoStar COMPS vacant-land sales, then report the value averaged over the metro's *urban* area in dollars per acre. It is land only — the input is vacant-land sale prices — but it is **all urban land**, not residential only: the paper says its index "includes highly valuable central and commercial land" (p. 461). So for a residential-comparable question this is best read as an urban land price level, plausibly an upper bound where commercial cores are expensive.

Quote, Table 2 notes (p. 460): *"Land value data from CoStar COMPS database for years 2005 to 2010."*
Quote, p. 459: *"In fifth place, Los Angeles–Long Beach has average values of $2.7 million per acre over its extended area of 1,359 square miles."*
Table 2 rows (col. 3 urban area sq mi, col. 4 land sales, col. 5 naive model, col. 6 central, col. 7 urban average, col. 9 total value $bn):

```
5  Los Angeles–Long Beach, CA   1,359  1,760  3,709  16,801  2,675  5.5  2,326.8
6  Orange County, CA             494    233  3,163   3,208  2,595  1.3    820.5
7  San Jose, CA                  305    217  2,580   3,552  2,347  1.6    458.3
```

San Diego and Riverside–San Bernardino are not in the printed Table 2, so I took their values from the paper's own replication file rather than from any secondary compilation:

- Harvard Dataverse, doi:10.7910/DVN/KSTT2Q, file `tab_lv_log2m6_estX_M2.xls`, sheet `land_values (MSAs)`.
- Rows: `Los Angeles-Long Beach CA` (n=1760), `Orange County CA` (n=233), `San Diego CA` (n=957), `Riverside-San Bernardino CA` (n=2452), `San Jose CA` (n=217).
- Columns used: `LV (UA)` (the published urban average, equals Table 2 col. 7 — LA 2,675,114 vs 2,675 printed), `LV-2005` … `LV-2010`, and `n`.

**Gyourko & Krimmel (2021).** Their data are CoStar vacant parcels "bought by builders for the purpose of single-family home development between 2013-2018". Appendix Table 2 reports `Mean P(L) / ft2`, the mean transaction price per square foot of land, within 30 miles of each CBSA centroid. Multiplied by 43,560 this is a per-acre price of *residential development* land — the closest thing in this literature to "urban residential-comparable" — but the parcels are large (median 75,489 sq ft = 1.7 acres in Los Angeles; 463,479 sq ft = 10.6 acres in Riverside), so the per-square-foot price is platted-down relative to a finished urban lot, and the mean is right-skewed (LA mean $49.64/ft², s.d. $87.48).

Quote, Appendix 2 header (p. 54 of the working-paper PDF): *"Summary Statistics on Vacant Land Purchases Intended for Single Family Home Development, 2013 - 2018 (within 30 miles)"*, column *"Mean P(L) / ft2 (Std. Dev.)"*. Rows used:

```
Los Angeles  157  75,489   725,481  $49.64 ($87.48)  2,615
Riverside    286  463,479  1,452,707 $9.09 ($15.33)  9,538
San Jose      44  306,227  1,200,930 $32.69 ($48.66) 1,213
```

(columns: CBSA, number of observations, median parcel ft², mean parcel ft², mean P(L)/ft², total acres transacted.)

## Conversion to 2024

I converted **year by year**, not with a single mid-period ratio: each annual value `LV-yyyy` was multiplied by `index(2024)/index(yyyy)` and the six converted values were averaged. This reproduces the published pooled value exactly when the multiplier is 1 (mean of LV-2005..2010 = LV (UA) for all five rows), which is a useful check.

Indexes used — S&P CoreLogic Case-Shiller metro HPI, monthly, seasonally adjusted (FRED series `LXXRSA`, `SDXRSA`, `SFXRSA`), annual averages; and CPI-U U.S. city average, all items, NSA (BLS `CUUR0000SA0`), annual averages. Values read from `_cache/cs_cities_sa.csv` (FRED mirror) and `_cache/cpi_u_monthly.json` (BLS API). The 2005 monthly LA values in the mirror match FRED `/data/LXXRSA` exactly (Jan 221.4714 … Dec 265.4194).

| Year | CS Los Angeles | CS San Diego | CS San Francisco | CPI-U |
|---|---|---|---|---|
| 2005 | 243.15 | 243.84 | 206.77 | 195.292 |
| 2006 | 271.29 | 246.58 | 215.96 | 201.592 |
| 2007 | 257.14 | 225.89 | 206.22 | 207.342 |
| 2008 | 194.81 | 173.31 | 156.15 | 215.303 |
| 2009 | 164.85 | 150.26 | 127.44 | 214.537 |
| 2010 | 173.61 | 161.17 | 139.29 | 218.055 |
| 2024 | 437.16 | 438.54 | 356.24 | 313.689 |

Nominal values read from the replication file ($/acre) and the resulting 2024 figures:

| County | 2005 | 2006 | 2007 | 2008 | 2009 | 2010 | pooled | index | × | 2024 |
|---|---|---|---|---|---|---|---|---|---|---|
| Los Angeles | 3,187,199 | 3,513,437 | 3,069,420 | 2,392,865 | 1,863,282 | 2,024,479 | 2,675,114 | CS-LA | 1.995 | 5,336,514 |
| Orange | 2,996,071 | 3,144,356 | 2,743,101 | 2,562,989 | 1,934,065 | 2,190,705 | 2,595,214 | CS-LA | 2.024 | 5,252,329 |
| San Diego | 1,234,034 | 1,231,514 | 1,102,079 | 990,489 | 952,333 | 924,964 | 1,072,569 | CS-SD | 2.230 | 2,391,962 |
| San Bernardino | 411,963 | 487,852 | 320,770 | 267,216 | 179,695 | 219,834 | 314,555 | CPI-U | 1.523 | 479,076 |
| Santa Clara | 2,636,609 | 2,765,387 | 2,751,971 | 2,481,628 | 1,826,162 | 1,623,036 | 2,347,465 | CPI-U | 1.514 | 3,553,718 |

Why CPI for two counties: there is no Case-Shiller index for the San Jose MSA or the Riverside–San Bernardino–Ontario MSA (Case-Shiller publishes 20 metros; San Jose and Riverside are not among them). Per the brief I used CPI-U there. That is a conservative choice for a land asset — house prices in those metros rose faster than consumer prices. If I instead use the nearest Case-Shiller metro, the figures would be **$616,983/acre** for San Bernardino (CS-Los Angeles, same 1999 CMSA) and **$4,795,918/acre** for Santa Clara (CS-San Francisco, same CSA); both alternatives are recorded in `notes`.

Gyourko–Krimmel conversion (2013-2018 average → 2024): CS-LA 437.16 / 241.85 = 1.808; CPI 313.689 / 240.49 = 1.304. Applied to $2,162,318, $395,960 and $1,423,976 per acre respectively.

## Sources

1. **Albouy, D., Ehrlich, G. & Shin, M. (2018).** "Metropolitan Land Values." *Review of Economics and Statistics* 100(3): 454-466. DOI 10.1162/rest_a_00710. Author PDF: https://davidalbouy.com/s/landvalue_index.pdf (downloaded to `_cache/albouy_mlv.pdf`). Replication data: https://doi.org/10.7910/DVN/KSTT2Q → `_cache/aes_msa_table.xls`. Table 2 (p. 460) and replication sheet `land_values (MSAs)`.
2. **Gyourko, J. & Krimmel, J. (2021).** "The impact of local residential land use restrictions on land values across and within single family housing markets." *Journal of Urban Economics* 126: 103374. Published PDF: https://static1.squarespace.com/static/5f75531c54380e4fb4b0f839/t/6220ea407c11c05699c079f8/1646324290953/Gyourko%2C+Krimmel+%282021%2C+JUE%29+-+Zoning+Tax.pdf (`_cache/gk2021_jue.pdf`). The `Mean P(L)/ft2` table is Appendix 2 of the **June 13, 2020 working-paper version** (https://realestate.wharton.upenn.edu/wp-content/uploads/2020/06/Zoning-Tax-Paper-AER-Version-June-13-2020.pdf, `_cache/zoning_tax.pdf`, pp. 54-56); the 14-page published JUE article does not print that appendix, so the appendix numbers come from the working paper. Both are CoStar/CoreLogic-based; neither uses FHFA land data.
3. **Deflators.** S&P CoreLogic Case-Shiller metro HPI via FRED (`LXXRSA`, `SDXRSA`, `SFXRSA`), annual averages of monthly SA values, read from the `datasets/house-prices-us` FRED mirror `data/cities-month-SA.csv` (through 2026-07) and cross-checked against `github.com/aalokpatwa/case-shiller` and FRED `/data/LXXRSA`. CPI-U `CUUR0000SA0` annual averages via the BLS public API.

Sources checked and not used: **Kok, Monkkonen & Quigley (2014, JUE 81:136-148)** is Bay Area only and its land-price sample is intra-metro, not a metro-wide $/acre figure; the eScholarship PDF returned HTTP 403. **Nichols, Oliner & Mulhall (2013)** produces a national land-price index, not metro $/acre levels. FHFA's county land series (Davis, Larson, Oliner & Shui 2021) and anything built on it were deliberately not opened.

## Limitations

- **Not residential-only.** Albouy et al. is the average value of *all* urban land in the metro, commercial and industrial included. For Los Angeles and Orange County, where the commercial core is extremely valuable, this likely overstates a residential-comparable per-acre price; for San Bernardino it likely understates residential values in built-up areas while overstating them relative to the desert fringe.
- **2005-2010 is a bubble-and-crash window.** The pooled value is a six-year average that includes the 2006 peak and the 2009 trough. A 2006-only or 2010-only base would move the LA figure by roughly 25-30%.
- **Modeled, not a raw mean.** Albouy et al. fit a monocentric hedonic surface with Bayesian shrinkage and average it over the urban area; it is not the arithmetic mean of observed sale prices (that is their "naive" column, which is ~39% higher for LA and ~22% higher for Orange).
- **Geography.** Los Angeles, Orange, San Diego and San Jose PMSAs map 1:1 to the named counties. The **Riverside–San Bernardino PMSA covers two counties**, so the San Bernardino figure is a two-county average, not a San Bernardino-only number; both sources share this limitation. No per-county split exists in either paper.
- **Gyourko–Krimmel measures a different thing** — large vacant parcels bought for subdivision, 2013-2018, mean (not median) $/ft², right-skewed. Its agreement with Albouy is good for San Bernardino ($516k vs $479k) and moderate for Los Angeles ($3.91M vs $5.34M), but poor for Santa Clara ($1.86M vs $3.55M); the gap is consistent with plattage (large-parcel discount) plus Albouy's inclusion of commercial land.
- **Index mismatch.** Case-Shiller is a repeat-sales *house* price index; land prices need not move with it. The conversion assumes land and house prices in a metro move proportionally, which is the standard shortcut but not a measurement.
- **No uncertainty band.** Neither source publishes an IQR for the metro average, so `low`/`high` are blank rather than fabricated.
- **Vintage of the second source.** The Gyourko–Krimmel appendix numbers are from the 2020 working paper; the published 2021 article reports the same zoning-tax results but does not reprint the P(L)/ft² appendix.

## Log

- 19:41 — repo inspected; `B_transactions/` created; `RESULT.md` seeded with "in progress".
- 19:43 — Albouy et al. author PDF downloaded (1.9 MB); Table 2 read: LA 2,675, San Jose 2,347, Orange 2,595 ($000/acre).
- 19:45 — MIT Press online appendix returned AccessDenied (signed URL expired); pivot to Harvard Dataverse replication file.
- 19:46 — Gyourko & Krimmel 2020 working paper downloaded; Table 1 (zoning tax) and Appendix 2 (`Mean P(L)/ft2`) located.
- 19:49 — Dataverse `tab_lv_log2m6_estX_M2.xls` downloaded; all five PMSA rows extracted (LA, Orange, San Diego, Riverside-San Bernardino, San Jose).
- 19:50 — `build_prices.py` written; first pass produced all five counties.
- 19:52 — FRED CSV endpoint blocked for curl/requests; used the `datasets/house-prices-us` mirror, verified 2005 LA monthly values against FRED `/data/LXXRSA` and 2023-10 values against a second mirror.
- 19:55 — CPI-U annual averages pulled from BLS API (`CUUR0000SA0`), 2005-2024.
- 20:06 — Published JUE 2021 PDF downloaded and checked; confirmed the P(L)/ft² appendix is only in the working-paper version.
- 20:08 — `prices.csv` rebuilt with per-county conversion notes and second-source figures.
- 20:13 — `RESULT.md` finalized; `prices.csv` checked (5 data rows, LF-only line endings, cache 7.9 MB).

Reproduce with: `uv run --with pandas --with xlrd python3 B_transactions/build_prices.py` (expects `_cache/aes_msa_table.xls`, `_cache/cs_cities_sa.csv`, `_cache/cpi_u_monthly.json`).
