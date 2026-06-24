# Immigration Graph — Integration Opportunities (Wiring, not Datasets)

**Date:** 2026-06-24
**Scope:** BRIDGES and LINKAGES across the existing DuckDB warehouse (schemas `context`/`lifetime`/`fiscal`, unified `immigration.duckdb`) + the claims/sources/generators lifetime-evidence catalog. This is **design + light verification**, not new raw-dataset acquisition. Each entry = {nodes connected · join key · crosswalk/source · what it unlocks · effort}.

**Warehouse key facts (verified from builders 2026-06-24):**
- Geo keys: `state_fips` (LPAD 2-digit string), `puma_code`, county FIPS; existing `context.puma_county_area_xwalk_2023` (cousub→county area-weighted, ~4,701 rows from `tab20_puma520_cousub20_natl.txt`).
- Origin key: `POBP` (4-digit ACS Place-of-Birth code, LPAD), `origin_label`, decoded via `ACSPUMS2019_2023CodeLists.xlsx`.
- Status keys: `NATIVITY` (1=native, 2=foreign-born), education via `education_bucket`/`acs_education_bucket` ({`<HS`, `HS/GED`, `some college/associate`, ...}), `bridge_dimensions` table catalogs the canonical join dims.
- Cross-domain views live in `build_fiscal_union_views.py` (`v_education_stock_with_npv`, `v_origin_federal_with_education_npv`, etc.), materialized into `fiscal` schema + bare `main` views.

A shared dimension/crosswalk plan precedes the wiring: the recurring blocker across nodes is that **status** is coded five different ways and **geography** lives at incompatible levels. Two reference tables (below, INT-06 and INT-07) are the spine everything else hangs on; build them first.

---

## Cluster 1 — Wiring incoming crime data into the fiscal warehouse

### INT-01 — Texas DPS / Light arrest rates → fiscal stock layer (status × state)
- **Nodes:** new `crime.tx_dps_arrests_by_status` ↔ `context.acs_origin_household_federal_microsim_2023` / `acs_foreign_born_education_bucket_totals_2023` (foreign-born stock by state).
- **Join key:** `state_fips` (Texas = '48' only) × a harmonized **legal-status path** ({undocumented, legal immigrant, US-born}). This is the ONE crime source with status at the unit level, so it joins the warehouse's status axis directly, no ecological step.
- **Crosswalk needed:** the status-harmonization table (INT-06). Light's denominators (CMS vs Pew undocumented population) must be carried as a column, not collapsed — store `denom_source` so a query can swap them.
- **Unlocks claim:** "undocumented immigrants in Texas have lower/higher felony-arrest rates than the US-born" *per 100k of the matching stock denominator* — currently un-runnable because no crime node exists. Lets the crime rate be expressed against the SAME foreign-born denominators the fiscal side already uses.
- **Effort:** M (openICPSR download + one harmonization table + a `crime` schema).

### INT-02 — BJS SPI 2016 incarceration rate ↔ ACS/IPUMS institutionalized-GQ-by-nativity
- **Nodes:** new `crime.spi_inmates_by_citizenship` ↔ IPUMS microdata (`GQ` group-quarters × `NATIVITY`/`CITIZEN`, the 44M-row local panel) and `context` nativity stock.
- **Join key:** `citizenship_status` × age × `state_fips` (state+federal split carried as a column). Numerator = SPI noncitizen inmate counts; denominator = ACS/IPUMS institutionalized + non-institutionalized population by the SAME citizenship class (the Butcher–Piehl method).
- **Crosswalk needed:** INT-06 status harmonization (SPI nativity/citizenship items → canonical class); IPUMS `CITIZEN`/`BPL` already in the panel.
- **Unlocks claim:** "noncitizen incarceration rate vs native-born rate" — the standard rebuttal surface. Cannot be computed today because the denominator (ACS GQ-by-nativity) and numerator (SPI) sit in unconnected layers with no shared citizenship key.
- **Effort:** M (SPI DS1 public-use + IPUMS GQ tabulation we can already run locally).

### INT-03 — SCAAP criminal-alien inmate-days → state/local cost ledger ($ bridge between halves)
- **Nodes:** new `crime.scaap_awards` ↔ `fiscal` state/local cost views (stage5 `state_stage5_context_2023`, `calculate_state_local_example_ledgers`).
- **Join key:** `state_fips` (+ county FIPS where the SCAAP PDF gives jurisdiction) × `fiscal_year`. Measures: criminal-alien inmate-days, reimbursement $, total inmates.
- **Crosswalk needed:** SCAAP jurisdiction names → county FIPS (a name→FIPS gazetteer match; Census place/county gazetteer). [UNVERIFIED: exact jurisdiction granularity per FY PDF]
- **Unlocks claim:** "incarceration cost attributable to criminal aliens, per state, vs federal SCAAP reimbursement share" — the only admin series tying crime burden to dollars; today the crime and cost ledgers have no connecting line. Slots directly beside Medicaid/SNAP in the net-negative cost layer.
- **Effort:** M-L (PDF parse like existing EOIR/CBO PDFs + name→FIPS match).

### INT-04 — FBI NIBRS / UCR county crime ↔ county foreign-born share (ecological design)
- **Nodes:** new `crime.county_offense_arrest_panel` ↔ a county foreign-born share derived from ACS via the PUMA→county crosswalk (INT-07).
- **Join key:** county FIPS × year. NIBRS has NO nativity at incident level → ecological only (county crime rate vs county foreign-born %), the Ousey–Kubrin / Wadsworth approach.
- **Crosswalk needed:** INT-07 (PUMA→county, because ACS foreign-born share is native to PUMA, not county) + a NIBRS agency-ORI→county FIPS crosswalk [SOURCE: ICPSR UCR county series #57 already does this ORI→county aggregation — adopt their county file rather than rolling our own].
- **Unlocks claim:** "counties with rising foreign-born share show no increase (or a decrease) in crime rates 2010–2023" — testable once county crime joins the county context warehouse. Must be tagged ecological / no-causal.
- **Effort:** M (ICPSR county file is pre-aggregated; main work is the PUMA→county foreign-born denominator).

### INT-05 — ICE ERO removals-by-criminality → enforcement cost inputs + origin layer
- **Nodes:** new `crime.ice_removals_by_criminality` ↔ existing CBP/ICE budget-justification cost inputs (`usaspending`, DHS PDFs) and the origin layer.
- **Join key:** `origin_country` (→ POBP via INT-06 country crosswalk) × `fiscal_year` × criminality class (conviction / pending / none).
- **Crosswalk needed:** ICE country names → ISO/POBP (INT-06 country side).
- **Unlocks claim:** "share of removals that are criminal vs the enforcement $ per removal, by origin" — ties an outcome count to the cost inputs we hold only as budget aggregates today.
- **Effort:** S-M (ICE dashboard Excel + country-name match).

---

## Cluster 2 — Missing crosswalks between layers we already hold (build these FIRST)

### INT-06 — Canonical status/citizenship harmonization table ⭐ (spine)
- **Nodes:** ACS (`NATIVITY`, `CIT` 1–5) · IPUMS (`CITIZEN`, `BPL`) · BJS SPI (nativity/citizenship items) · USSC (`NEWCIT`/citizen field: US citizen / legal alien / illegal alien / etc.) · Light TX-DPS ({undocumented, legal immigrant, US-born}).
- **Join key:** a new canonical `status_class` enum, e.g. {`native_born`, `naturalized`, `lpr_legal_noncitizen`, `unauthorized`, `other_noncitizen`}, with a per-source column mapping each source's native codes into it. Stored as `context.status_class_crosswalk` (source, native_code, native_label, status_class, lossy_flag).
- **Crosswalk source:** ACS CIT code list (`ACSPUMS2019_2023CodeLists.xlsx`, already local) [SOURCE: local]; USSC codebook NEWCIT field [UNVERIFIED — confirm exact categories from codebook]; SPI DS1 codebook [UNVERIFIED]. Mark `lossy_flag` where a source can't separate LPR from unauthorized (ACS/IPUMS cannot → both fold to `other_noncitizen` unless imputed).
- **Unlocks:** EVERY status-keyed crime↔fiscal join (INT-01, 02, 05) and resolves the recurring "citizenship coded five ways" blocker. Without it each crime node re-invents the mapping inconsistently (the shared-invariant-defined-once rule).
- **Effort:** S (one reference table; the hard part is honest `lossy_flag` discipline, not volume).

### INT-07 — PUMA ↔ county ↔ tract population-weighted crosswalk (upgrade the area-weighted one)
- **Nodes:** ACS PUMS (PUMA-native) ↔ county context warehouse (county FIPS) ↔ tract-level nodes (Opportunity Atlas 2nd-gen, future NIBRS-adjacent).
- **Join key:** `state_fips`+`puma_code` ↔ county FIPS ↔ tract GEOID, with **population** allocation factors (`afact`), not area. The existing `puma_county_area_xwalk_2023` is **area-weighted** (its own register note flags this as a limit) — area weighting misallocates population for immigrant-dense urban PUMAs.
- **Crosswalk source:** Census MABLE/**Geocorr 2022** correspondence engine generates PUMA→county→tract with population `afact` allocation factors [SOURCE: https://mcdc.missouri.edu/applications/geocorr2022.html — verified live 2026-06-24]. Use 2020-vintage PUMAs to match ACS 2023/2024.
- **Unlocks:** correct county foreign-born denominators for INT-04, and a tract bridge for Opportunity Atlas (INT-08). Replaces the area-weighted approximation flagged in the receiver-node kill-test limit ("PUMA bridge is area-weighted").
- **Effort:** M (Geocorr pull + rebuild xwalk table + migrate the ~2 callers — breaking replacement, not a shim).

### INT-08 — POBP ↔ ISO-3166 ↔ World-Bank-region origin concordance
- **Nodes:** ACS `POBP` / `origin_label` ↔ World Bank country metadata (`worldbank_country_metadata.json`, already local: region + income group) ↔ OHSS/ICE country names ↔ ABJP mobility origin ↔ remittance country.
- **Join key:** ISO-3166 alpha-3 as the hub; POBP→ISO and country-name→ISO both map into it.
- **Crosswalk source:** ACS POBP code list (local xlsx) + a POBP→ISO mapping [UNVERIFIED — no official Census POBP↔ISO file; build from the labelled POBP list, ~150 foreign codes, hand/fuzzy-matched]. World Bank metadata already keyed to ISO-ish codes.
- **Unlocks:** region-level rollups joining origin across ALL origin-keyed nodes (fiscal scenario, remittances, mobility, ICE removals) — e.g. "Central America" as one row instead of per-POBP. Currently `origin_label` is free POBP text, so origin can't be rolled to region without a manual case-when each time.
- **Effort:** S-M (one concordance table, ~200 rows).

### INT-09 — Education-bucket harmonization across NAS / SIPP / ACS / SPI
- **Nodes:** `acs_education_bucket` (already the bridge key) ↔ NAS NPV `acs_education_bucket` ↔ SIPP `EEDUC` ↔ SPI educational-attainment item.
- **Join key:** the existing `education_bucket` enum, extended with a per-source mapping table `context.education_bucket_crosswalk` so SPI/SIPP raw education codes fold into the same {`<HS`, `HS/GED`, `some college/associate`, `BA+`} buckets the NPV and ACS layers use.
- **Crosswalk source:** the buckets already exist in `bridge_dimensions`; this just adds the SIPP/SPI source mappings [SOURCE: local bridge_dimensions]. The "BA+" bucket is presently underused — NAS has it, ACS totals stop at "some college".
- **Unlocks:** lets crime nodes (SPI offenders carry education) join the SAME NPV/earnings gradient the fiscal side uses → "is the offender population concentrated in the fiscally-negative `<HS` cell?" — a direct crime↔fiscal-cell bridge.
- **Effort:** S.

---

## Cluster 3 — Joins that unlock a currently-untestable existing claim

### INT-10 — Origin-fiscal-scenario × second-gen mobility (annual-NPV vs descendant uplift)
- **Nodes:** `lifetime.origin_fiscal_scenario_2023` (per-origin annual net) ↔ ABJP mobility / Opportunity Atlas 2nd-gen ranks ↔ `npv_education_benchmarks` (descendants booked separately).
- **Join key:** `origin_country`/POBP (via INT-08).
- **Unlocks claim:** the unified-theory thesis explicitly flags "descendants booked separately" as a falsifier of the M1 NAS-negative frame, but there is **no descendant node wired in**. This join lets "low-skill parent ⇒ permanent fiscal drag" be tested against measured father→child rank uplift by origin — currently asserted in the narrative spine (line 84 of the unified-theory memo) with no joinable data behind it.
- **Effort:** M (needs ABJP/Atlas acquisition from roadmap + INT-08).

### INT-11 — Same-universe school numerator ↔ federal microsim denominator (resolve the withheld cell)
- **Nodes:** `v_three_layer_annual` (currently withholds "Mexico school burden/adult" and "crude annual fed−school" — flagged unresolved in unified-theory anchors table) ↔ `school_finance_county_2023` ↔ `acs_origin_household_federal_microsim_2023`.
- **Join key:** the bug is a **universe mismatch** — scenario-household numerator vs full-microsim denominator. Fix = a county→origin allocation so the school-cost numerator and the federal-net denominator share one population universe, joined via INT-07 (PUMA→county population weights).
- **Unlocks claim:** the "Mexico crude annual (fed − school)" cell the warehouse currently refuses to emit — a named, withheld value blocked precisely by a missing same-universe bridge.
- **Effort:** M (this is a view-logic + crosswalk fix, no new data).

### INT-12 — CMS Emergency Medicaid (admin) replaces MEPS health-cost inference
- **Nodes:** new `fiscal.cms_emergency_medicaid_state_year` ↔ existing inferential MEPS proxy (`meps_health_cost_module_2023`) ↔ stage5 Medicaid layer.
- **Join key:** `state_fips` × `fiscal_year`.
- **Unlocks claim:** the unified-theory health-cost line is presently a MEPS-based **inference** (flagged "Descriptive module only, not legality-specific"). Wiring CMS-64 emergency-Medicaid actuals gives a **direct administrative** cost line by state, letting the inferred MEPS number be validated/replaced — turning an `[INFERENCE]` ledger line into `[SOURCE]`.
- **Effort:** S-M (CBO/CMS table parse + state-year join).

---

## Build order (dependency-aware)
1. **INT-06 + INT-07 + INT-08 + INT-09** (the four crosswalk/harmonization spines) — everything else depends on them.
2. **`crime` schema** + INT-01, INT-02 (status-keyed, highest-value crime joins).
3. INT-03, INT-04, INT-05 (cost-bridge + ecological + enforcement).
4. INT-10, INT-11, INT-12 (unlock withheld/inferential existing claims).

**Discipline notes:** INT-06 is a shared invariant → define once, every node loads it (don't let each crime parser re-map citizenship). INT-07 is a **breaking replacement** of the area-weighted xwalk — migrate the ~2 callers, no shim. Ecological joins (INT-04) carry a mandatory no-causal tag. Lossy status folds (ACS/IPUMS can't split LPR from unauthorized) must surface as a column, never silently imputed.

