# Immigration fiscal — distribution findings (federal proxy + school units)

**Date:** 2026-06-15
**Status:** Working findings from sweep 11 + ACS/SIPP distribution pass (conversation 2026-06-15)
**Frame:** [FRAMING-SENSITIVE] — no scalar “Mexican lifetime NPV”; these are **layer-specific** stock estimates for adults 25–64 unless noted.
**Related:** `research/immigration-lifetime-unified-theory-2026-06-15.md`, `research/immigration-lifetime-fiscal-generators.md`

---

## I. What we were testing

Can we explain “whites pay multiples more” when you multiply **headcount × education × income × location** — separately from lifetime NPV and local school spend?

**Ledger in this memo:** narrow **federal annual cash-flow proxy** = SIPP-style **payroll (FICA 7.65% on wages, cap $168,600)** minus **SNAP + TANF + SSI** annualized. [INFERENCE: not income tax, Medicare, Medicaid, or full federal budget.]

---

## II. School spend ($/pupil) — not an ethnicity tariff

| Finding | Value | Source |
|---------|-------|--------|
| F-33 unit bug (pre sweep 11) | ~$21/pupil | Thousands treated as dollars |
| County median (post fix) | **~$19,385/pupil** | `school_finance_county_2023` |
| Mexico-origin area-weighted (post fix) | **~$20,907/pupil** | `origin_fiscal_scenario_2023` |
| NH white HH area-weighted (ACS sample) | **~$20,833/pupil** | PUMA×county join [INFERENCE] |

**Verdict:** Per-pupil public K–12 spend is a **location average** (~$20k/yr per enrolled pupil), not “Mexicans cost $20k vs whites cost $X.” Groups differ mainly **where they live**, not a race-specific price.

**Lifetime K–12 rough band:** ~$20k × ~13 years ≈ **~$260k undiscounted** per child using public schools — before discounting, not marginal cost. [INFERENCE]

---

## III. Same education — income (NH white vs Mexico-born)

ACS 2023 person microdata, ages 25–64, weighted PINCP:

| Education | NH white | Mexico-born | Ratio |
|-----------|----------|-------------|-------|
| `<HS` | ~$27,539 | ~$26,858 | **1.0×** |
| HS/GED | ~$42,665 | ~$34,932 | **1.2×** |
| Some college | ~$55,680 | ~$42,536 | **1.3×** |
| College+ | ~$98,759 | ~$58,968 | **1.7×** |

**Verdict:** “Multiples” at **same education** only appear at **HS+**; at `<HS` incomes are **parity**. Gap is **not** primarily a within-`<HS` wage story.

---

## IV. Distribution-weighted federal proxy (multiply it out)

### Populations & education mix (ACS 2023, ages 25–64)

| Group | Weighted adults | `<HS` | HS | Some coll | College+ |
|-------|-----------------|-------|-----|-----------|----------|
| NH white (US-born) | **~93.6M** | 5% | 24% | 19% | **52%** |
| Mexico-born | **~8.5M** | **46%** | 29% | 11% | 14% |

### Per-capita federal net proxy

| Group | $/adult/yr | Method |
|-------|------------|--------|
| Mexico-born | **~$1,300–1,600** | `acs_origin_household_federal_microsim_2023` by education (SIPP FB donors) |
| NH white | **~$3,600–4,000** | ACS `WAGP` → FICA − SIPP US-born transfers by education |
| **Ratio** | **~2.3–3.0×** | Per person |

Sensitivity (white payroll from ACS, transfer assumptions): **~2.8–3.1×** [INFERENCE]

### Aggregate (people × per-capita)

| Group | Total proxy $/yr |
|-------|-------------------|
| Mexico-born (~8.5M) | **~$13–14B** |
| NH white (~93.6M) | **~$340B** |
| **Ratio** | **~25×** |

**~11×** of the 25× is **population** (93.6M / 8.5M), not per-person tax rate.

### Decomposition (per-capita gap)

1. **Education composition alone ~1.9×** — Mexico-born with NH-white education shares but Mexico microsim cells → ~$2,970/yr vs actual ~$1,580/yr.
2. **Within-cell earnings / transfers ~1.2–1.5×** — NH white weighted `WAGP` ~$60k vs Mexico ~$31k (~**1.9×**); same-education gaps smaller (Section III).
3. **Both groups positive** on this proxy — Mexico scenario table **~+$1,519/yr** federal net at origin level is consistent in sign.

**Verdict:** “Whites pay multiples more” is **~2–3× per adult** on this **narrow federal cash proxy**, mostly **education mix + earnings**, not 25× per person and not school per-pupil.

---

## V. Warehouse limitations (do not over-read)

| Limitation | Implication |
|------------|-------------|
| Federal microsim donors are **foreign-born SIPP only** | No native-white microsim; white side uses ACS wages + transfer imputation |
| One federal-net number per education in scenario ledger | Hides origin×education heterogeneity unless microsim queried |
| Proxy omits income tax, Medicare, EITC mechanics, capital gains | True federal liability gap may differ from 2–3× |
| NH white `<HS` SIPP transfer cell is noisy | Can imply negative federal net for that tiny slice — do not use for scalar exports |
| Stock 25–64 ≠ surge cohort, ≠ lifetime NPV | CBO 60569 surge federal channel is a different **t** |

---

## VI. Compatible with unified theory

- **Layer laundering:** Annual federal +, `<HS` lifetime NPV −, education-mix age-25 benchmark +, and local episodic − can coexist.
- **Mexico is a weight, not a number:** Use education × arrival × state cells.
- **Sign wars are composition wars** when groups are compared without matching education and ledger layer.

---

## VII. Open hunts

1. ~~Native-born federal microsim~~ → `acs_nh_white_federal_microsim_2023` [done 2026-06-15]
2. ~~Annual ↔ NPV bridge~~ → `annual_npv_bridge_grid` (all `scope_mismatch`) [done]
3. ~~Country-level stack v1~~ → `immigration-country-fiscal-tensor-2026-06-15.md` [done]

---

## VIII. Country tensor query

`warehouse/immigration_fiscal_union.duckdb` → `v_country_fiscal_rollup`, `v_country_fiscal_compare`

---

## Sources

| Tag | Reference |
|-----|-----------|
| [SOURCE] | ACS 2023 PUMS person (`psam_pusa.csv`, `psam_pusb.csv`) |
| [SOURCE] | `warehouse/immigration_context.duckdb` — microsim, scenario |
| [SOURCE] | `warehouse/immigration_lifetime_evidence.duckdb` — scenario, school finance |
| [SOURCE] | `infra/immigration-fiscal/build/build_federal_microsim_sipp_2024.py` — payroll 7.65%, transfer definition |
| [INFERENCE] | Decomposition and sensitivity calculations (this session) |
