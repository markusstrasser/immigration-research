# Immigration fiscal — Europe, Caucasian natives, and low-skill corridors (2026-06-15)

**Date:** 2026-06-15
**Status:** Working findings — distribution pass + population tensor extension (sweep 12 write-up)
**Frame:** [FRAMING-SENSITIVE] — layer-specific; no scalar “immigration is +/− $X.”
**Related:** `immigration-federal-distribution-findings-2026-06-15.md`, `immigration-country-fiscal-tensor-2026-06-15.md`, `immigration-lifetime-country-approx-brainstorm-2026-06-15.md`
**Instrument:** LLM-assisted synthesis; politically charged topic — see `notes/llm-bias-caveat.md`.

---

## I. Definitions (do not mix groups)

| Label | ACS definition | What it is NOT |
|-------|----------------|----------------|
| **Caucasian / NH white** | `HISP=01` (not Hispanic) + `RAC1P=1` (white alone) | Hispanic white; Indigenous / American Indian |
| **NH white US-born** | Above + `NATIVITY=1` | “All whites including European immigrants” |
| **NH white foreign-born** | Above + `NATIVITY=2` | All FB whites (Canada, UK, Eastern Europe, etc.) |
| **EU27 immigrant** | FB + birth in EU member state POBP codes (+ legacy Czechoslovakia/Yugoslavia) | UK (post-Brexit), Russia, Ukraine, Canada |
| **Low-skill immigrant (operational)** | FB + `education_bucket='<HS'` in microsim | Mexico-origin (mixed skill — 46% `<HS`) |

**Ledger:** federal annual proxy = SIPP donor **payroll (FICA 7.65%)** minus **SNAP + TANF + SSI** annualized. [INFERENCE] Not income tax, Medicare, Medicaid, or full federal budget.

**Population:** ACS 2023 PUMS person, ages **25–64**, both person files (pusa+pusb). [SOURCE: `warehouse/immigration_context.duckdb`, ACS imputation / microsim tables]

---

## II. Headline comparison (federal annual $/adult)

| Population | Adults | Avg wage (`WAGP`) | % `<HS` | % college+ | Fed $/adult/yr |
|------------|--------|-------------------|---------|------------|----------------|
| **NH white US-born** | 93.6M | $60,401 | 4.9% | 52.2% | **$2,746** |
| **NH white all nativity** | 98.3M | $61,127 | 5.0% | 52.8% | **$2,803–3,005** |
| NH white foreign-born | 4.7M | $75,480 | 6.7% | 63.7% | **$3,898** |
| **EU27 foreign-born** | 1.46M | $80,771 | 6.2% | 54–62% | **$4,695** |
| **UK foreign-born** | 0.42M | $99,621 | 3.0% | 61–69% | **$5,486** |
| All Europe (POB 100–199) | 3.05M | $76,392 | 5.5% | 64.4% | $4,170 |
| All foreign-born stock | 33.5M | — | 22.9% | 43.2% | $3,003 |
| Mexico-origin | 8.5M | ~$31k | **46%** | 14% | **$1,519** |
| **FB `<HS` pooled** | 7.7M | — | 100% | 0% | **$677** |
| MX + N. Triangle cluster | 11.1M | — | ~44% | ~16% | $1,519 |

[SOURCE: microsim `acs_origin_household_federal_microsim_2023`, `acs_nh_white_federal_microsim_2023`, `v_country_fiscal_rollup`; wages from ACS person CSV imputation]

### Ratios that matter

| Comparison | Ratio | Interpretation |
|------------|-------|----------------|
| EU27 FB / NH white US-born | **1.71×** | Selected European immigrants **beat** native Caucasians on this proxy |
| UK FB / NH white US-born | **2.00×** | Same, stronger |
| NH white US-born / Mexico-origin | **1.81×** | Mostly education mix, not race tariff |
| NH white all / FB `<HS` | **~4.1×** | “Caucasian average” vs strict low-skill pool |
| EU27 FB / Mexico-origin | **3.09×** | Two immigration corridors, opposite selection |

---

## III. Caucasian natives vs foreign-born whites

**Foreign-born whites raise the Caucasian average — they do not drag it down.**

| Group | Fed $/adult/yr |
|-------|----------------|
| NH white US-born | $2,746 |
| NH white all | $2,803 |
| NH white foreign-born | $3,898 |

Mechanism: **positive selection** — H-1B/L-1/skilled paths, Anglosphere professionals, age-at-arrival, English proficiency. EU27 and NH-white-FB have **similar education mix** to US-born whites (~5–7% `<HS`, ~54% college+) but **higher within-cell wages**. [INFERENCE]

**Tail below natives (NH white FB only):** small Eastern European / UK cohorts at ~0.7–1.0× US-born wages; dominated in the aggregate by Germany, France, Ireland, Poland professionals. [SOURCE: ACS `WAGP` by POBP — conversation query 2026-06-15]

---

## IV. European immigrants — country slice

Top EU-origin countries (microsim, donor-matched):

| Origin | Adults | Fed $/adult/yr |
|--------|--------|----------------|
| Poland | 0.25M | $3,950 |
| Germany | 0.25M | $4,427 |
| France | 0.12M | $6,025 |
| Italy | 0.12M | $4,624 |
| Ireland | 0.07M | $5,780 |
| Romania | 0.11M | $4,511 |
| Sweden | 0.03M | $6,557 |

**Verdict:** EU immigration on this ledger looks like **high-skill FB white / Canada tier**, not like Mexico / Central America. Poland is the EU floor here (~$4k); still **above** NH white US-born.

---

## V. Low-skill corridor vs Caucasian natives

| “Low skill” definition | Fed $/adult/yr | vs NH white US-born |
|------------------------|----------------|---------------------|
| FB `<HS` only | $677 | **4.0×** gap |
| Mexico-origin (mixed) | $1,519 | **1.8×** gap |
| MX + N. Triangle | $1,519 | **1.8×** gap |

**Lifetime NPV (NAS grammar, 1st order — where cells exist):**

| Population | NPV/adult (weighted) |
|------------|----------------------|
| FB `<HS` | **−$109k** |
| Mexico-origin | **~+$45.6k synthetic age-25 benchmark** |
| US FB stock | **~+$212.5k synthetic age-25 benchmark** |

[SOURCE: `v_country_fiscal_rollup`, `npv_education_benchmarks`]

**Warehouse caveat:** these `lifetime_npv` rollups are NAS Table 8-13 age-at-arrival-25 education-cell benchmarks applied to current ACS education weights. They are not actual remaining-lifetime NPVs for current resident stocks. Lifetime rollups for EU27 / NH white are still incomplete until their ACS education weights are joined to the staged NAS cells. [SOURCE: `v_country_fiscal_rollup`; `country_fiscal_tensor` notes]

**Directional [INFERENCE]:** EU27 age-25 benchmark should sit **closer to high-skill foreign-born than to FB `<HS`** on education mix alone; EU27 is college-heavy relative to Mexico and the pooled `<HS` slice.

---

## VI. Matched education — Mexico vs NH white (disconfirmation)

Symmetric SIPP microsim at **education cell** (NH white `<HS` cell patched with FB `<HS` donor — US-born `<HS` SIPP cell is noisy at −$7.5k/adult):

| Education cell | Mexico / white (adj) | Who pays more on federal proxy |
|----------------|----------------------|--------------------------------|
| `<HS` | ~0.95× | ~parity |
| HS / GED | **~3.9×** | **Mexico** |
| some college | ~1.29× | Mexico |
| college+ | ~0.73× | White |

[SOURCE: `education_matched_federal` in `immigration_fiscal_union.duckdb`]

**Verdict:** Aggregate “whites pay more” is **not** a uniform within-cell premium. At HS and some-college, **Mexico-born cells show higher federal proxy** than white cells. The headline gap is **composition** (52% vs 14% college+), not ethnicity-coded tax rates.

---

## VII. School spend — still not where the gap lives

| Metric | Value |
|--------|-------|
| Per-pupil (Mexico area-weighted, post F-33 fix) | ~$20,907/yr |
| Per-pupil (NH white HH area-weighted) | ~$20,833/yr |
| Federal proxy (Mexico adult) | ~$1,519/yr |
| Federal proxy (NH white US-born) | ~$2,746/yr |

[SOURCE: `immigration-federal-distribution-findings-2026-06-15.md`]

---

## VIII. Two-corridor model (synthesis)

**Corridor A — composition-weighted low education:** Mexico, Northern Triangle, FB `<HS` → low federal annual proxy, negative NAS lifetime on `<HS` cells.

**Corridor B — positively selected high education:** EU27, UK, India, Canada, NH-white-FB → federal proxy **above** NH white US-born despite similar degree shares.

**US-born NH white** sits in the middle — high college share but **no immigrant selection filter**.

Politically, debates that contrast “immigrants” vs “natives” without naming **corridor and education cell** are comparing Corridor A stock to Corridor B natives or mixing annual federal with lifetime K–12. [FRAMING-SENSITIVE] [INFERENCE]

---

## IX. Limitations

| Limitation | Implication |
|------------|-------------|
| Federal proxy ≠ income tax | True tax gap may differ; payroll cap binds high earners |
| Origin ≠ visa class | EU includes refugees, family, retirees — country averages hide tails |
| Annual ≠ lifetime | Bridge grid: all `scope_mismatch` — do not sum |
| EU / white lifetime rollup missing | Cannot publish EU / white synthetic age-25 benchmark until their ACS education weights are joined |
| NH white `<HS` SIPP cell | Noisy; exclude from scalar claims |
| POBP / EU list | UK excluded from EU27; Russia/Ukraine in “Europe” but not EU |

---

## X. Reproduce

```bash
cd infra/immigration-fiscal
bash rebuild.sh
bash rebuild_lifetime_warehouse.sh
# Query:
# SELECT * FROM v_country_fiscal_rollup WHERE fiscal_layer='federal_annual';
# SELECT * FROM education_matched_federal;
```

---

## Revisions

| Date | Change |
|------|--------|
| 2026-06-15 | Initial write-up — EU vs Caucasian vs low-skill corridors after sweep 12 distribution pass |
