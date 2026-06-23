# Immigrant Supply Shock by Education Cell, 1980–2023 (IPUMS panel)

**Date:** 2026-06-23
**Status:** New empirical surface. Measurement = high confidence; wage interpretation = NOT settled here.
**Data:** `[SOURCE: IPUMS USA extract — 1980/1990/2000 5% census + 2010/2023 ACS, 44.4M persons]`, aggregated to `borjas_supply_shock_panel` (160 education×experience×year cells). Local microdata in `immigration_microdata.duckdb` (license-restricted, not redistributed); the aggregate cells ship in the unified release.

## Claim

The immigrant share of the U.S. working-age (18–64) workforce rose sharply from 1980 to 2023, and the rise is **steepest among the least-educated** — the classic Borjas (2003) low-skill supply shock.

**Immigrant share of workers, by education bucket (PERWT-weighted):**

| Education | 1980 | 1990 | 2000 | 2010 | 2023 |
|-----------|-----:|-----:|-----:|-----:|-----:|
| **< HS (dropout)** | 9.8% | 17.6% | 29.6% | 37.9% | **40.8%** |
| HS grad | 5.1% | 8.0% | 11.4% | 14.3% | 16.6% |
| Some college | 6.6% | 7.9% | 10.5% | 12.2% | 13.2% |
| College+ | 8.0% | 10.6% | 14.6% | 17.3% | 19.7% |
| *All workers* | 7.1% | 10.0% | 14.3% | 17.1% | 18.4% |

`[INFERENCE]` Two structural facts:
1. **Low-skill concentration.** The <HS cell went from ~1-in-10 to ~2-in-5 foreign-born — a **~4.2× increase**, far larger than any other cell. This is the supply shock Borjas argued depresses native low-skill wages.
2. **U-shape across education.** By 2023 the immigrant share is high at the bottom (40.8%) *and* elevated at the top (19.7% college+), lowest in the middle — the well-documented bimodal immigrant education distribution. High-skill immigration grew too, just less dramatically.

## Validation `[SOURCE: panel vs Census published series]`

Foreign-born flagged by `BPL >= 150` (birthplace = foreign country). PERWT-weighted national foreign-born share comes out 6.7%(1980) → 8.7 → 11.7 → 13.7 → 15.4%(2023), matching the official Census foreign-born series to within a few tenths of a point each decade. The cell shares above are therefore trustworthy as *measurement*.

## What this does and does NOT show `[FRAMING-SENSITIVE]`

**Does (empirical fact):** the *quantity* of the supply shock — how much the immigrant share of each skill cell grew. High confidence.

**Does NOT (contested):** the *wage effect*. A supply shock only depresses wages given (a) a downward-sloping labor demand curve within the cell, (b) imperfect substitution offsets, and (c) no full general-equilibrium washout. The repo already holds the adversarial wage debate — Borjas (pessimistic, ~national skill-cell) vs Card/Peri (optimistic, local + capital adjustment + native out-migration attenuating 40–60% of the local shock, `[SOURCE: borjas_2005_native_internal_migration]`). **This panel is the input that debate argues over; it does not adjudicate it.** See `immigration-economist-effects-matrix.md` and `immigration-adversarial-review.md`.

## Caveats on the panel itself

- **All-sex.** The extract lacked SEX, so cells pool men and women (the prior ACS anchor was male-only). Immigrant *share* is robust to this; pooled-sex *income* mixes the gender gap — treat `avg_total_income_nominal` as indicative only.
- **Income is nominal total personal income** (INCTOT), not wage (INCWAGE). Deflate (CPI) before any cross-year earnings comparison; prefer INCWAGE for a pure wage study.
- **Potential experience** approximated as `age − assumed_school_years − 6` (HSD=10, HSG=12, SMC=14, COL=16 years), standard but coarse.
- **BPL≥150** counts Puerto Rico / US territories as native (correct); 1980 share (6.7%) runs ~0.5pp above the official 6.2% — small edge-case inclusion, does not affect the trend.

## Instrument note

`[INFERENCE]` The numbers are mechanical (weighted counts from census microdata) and not LLM-susceptible. The *interpretation* — calling this a "shock" that "competes with" native workers — is the contested framing this repo deliberately holds at arm's length (`notes/llm-bias-caveat.md`). The table is the fact; the wage story is not.

## Reproduce

```bash
./reproduce.sh build ipums   # needs the manual IPUMS extract in external/ipums/usa_extract/
duckdb warehouse/immigration.duckdb "SELECT * FROM borjas_supply_shock_panel"
```
Builder: `infra/immigration-fiscal/build/build_borjas_supply_shock_panel.py`.
