# Consumer-price and native-hours benefits of Mexico-born low-skill labor

**Verdict:** Both pro-side channels are real and both are an order of magnitude too small to close the Mexican-origin fiscal gap. Central arm: **$23.8bn/yr** of native consumer surplus on immigrant-intensive services and **$8.7bn/yr** of tax on the extra hours of high-wage native college women. Netting the same paper's implied **$10.7bn/yr wage gain to native high-school dropouts** leaves **$21.8bn/yr** defensible, **7.5%** of the −$290.59bn reference gap; the purely fiscal part is **$8.7bn, 3.0%**. Conservative arm: $10.5bn total, $4.4bn fiscal. Two recent US studies (IMF WP 2025/005; a 2026 barcode-level paper) fail to reproduce the services-price channel at all.

Memo: [`research/immigration-consumer-price-and-native-hours-2026-09-18.md`](../../../research/immigration-consumer-price-and-native-hours-2026-09-18.md)

## Shock

ACS 2024 1-year PUMS, civilian labor force 16+: foreign-born high-school dropouts 6,635,078 / 175,478,713 = **3.781%**. Mexico-born component 3,165,994 = **1.804% of the labor force, 47.7% of all low-skilled immigrants**. Removing them from numerator and labor force: share → 2.013%, **Δln = −0.6303**.

## Scripts (run in this order)

| Script | Output | Notes |
|---|---|---|
| `acs_extract.py` | `derived/lowskill_share.csv`, `industry_shares.csv`, `women_top_quartile.csv`, `households.csv`, `acs_audit.json` | 80 replicate weights; `STATE` not `ST`; HU/GQ from SERIALNO[4:6] |
| `acs_households.py` | `derived/native_hh_by_quintile.csv` | native-householder share at the CEX income cut-points |
| `acs_native_lowskill.py` | `derived/native_lowskill_base.csv` | earnings base for the offsetting wage channel |
| `cex_parse.py` | `derived/cex_detail_all.csv`, `cex_quintile_parents.csv`, `cex_audit.json` | **Gate: 14 major components sum to published total, max $2 on $150,342** |
| `cortes_table1.py` | `derived/cortes_table1_cities.csv` | places our Δln inside the identifying variation |
| `compute.py` | `derived/partA_price_results.csv`, `partB_hours_results.csv`, `native_lowskill_wage_offset.csv`, `expenditure_map.csv`, `compute_audit.json` | all arms |
| `summary.py` | `derived/summary_table.csv` | the memo's headline table |

## Gotchas found

- **BLS 403s a default curl UA.** A browser User-Agent string carrying a contact address gets 200 on every `bls.gov/cex/tables/...xlsx`.
- **cbo.gov returns 403** to WebFetch and to curl; the marginal-rate text had to come through a search index.
- **PMC bot-walls curl** but `agent-browser read` gets the full article text (Furtado & Hock).
- **Cortés 2008 published (2%) ≠ working paper (1.3%)** for the same study — a 54% difference. Same pattern in Lach (published 0.5pp vs WP 1.4–1.8pp).
- **Cortés & Tessada main-text coefficients are unreachable** (AEA, JSTOR, ResearchGate, UC Chile repo, openICPSR all failed). The AEA-hosted Online Appendix at `aeaweb.org/articles/materials/1197` is a free primary substitute, but for top-25% *occupations*, not top-quartile *wages*.
- **Furtado & Hock 2010 has no hours estimate** — it regresses the tetrachoric fertility/LFP correlation. [VERIFIED NEGATIVE]
- One CEX line ("Household laundry and dry cleaning, sent out, non-clothing, not coin-operated") is published as `d/` (no data) and is dropped; recorded in `compute_audit.json`.

## The extrapolation breaks its own model

Applying Cortés's low-skilled-immigrant wage elasticity (−8.0% per 10%) to this shock implies the remaining low-skilled immigrants' wages rise **73.6%**. Since she attributes 50–80% of the price effect to that wage channel, the 14.3% price rise inherits the implausibility. The conservative arm is closer to what the evidence carries. Our |Δln| = 0.63 is matched by 9 of Cortés's 25 cities in 1980–2000, but by only 1 in the negative direction, and none nationally.
