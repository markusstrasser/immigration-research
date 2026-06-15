# Lifetime fiscal datasets — brainstorm + acquisition pass

**Date:** 2026-06-15
**Goal:** Expand beyond the annual SIPP/MEPS/stage5 stack toward defensible lifetime NPV proxies for education-arrival-state cells (not “Mexican” scalars). [FRAMING-SENSITIVE]
**Status:** `external/lifetime/` — **110 files, ~107MB** (rounds 1–10; `bash acquire/setup-lifetime.sh`).
**Synthesis:** `research/immigration-lifetime-unified-theory-2026-06-15.md` (update each sweep per `notes/immigration-lifetime-sweep-protocol.md`).
**Cookbook:** `notes/immigration-lifetime-synthesis-diverge-cookbook.md` (diverge↔converge prompts).

## Brainstorm (perturbation rounds)

### Denial cascade — if microdata never arrives

1. **NAS/NRC education NPV tables only** — calibrate lifetime from published age-education cells; ACS supplies composition weights only.
2. **CBO scenario PDFs** — federal macro offset bounds; not immigrant-specific but mandatory disconfirmation.
3. **ITEP undocumented tax PDF** — tax *paid* floor for unauthorized (already in `setup.sh`).
4. **IRS SOI migration panel** — tax-base mobility, not immigrant status (corpus + stage2).
5. **Pew unauthorized stock PDF** — legal-status mix prior, not fiscal ledger.
6. **DHS LPR by country** — Mexico legalization path mix (OHSS tables in `setup.sh`).
7. **Receiver-city cost CSV** — local shock for NYC/Chicago nodes, not lifetime NPV.
8. **Remittance outflows (World Bank)** — private transfer offset to public fiscal (not yet acquired).
9. **SAIPE district poverty** — incidence context for school/medicaid take-up (stage4).
10. **QCEW industry wages** — stylized earnings paths by sector (construction/ag for Mexico-heavy cells).

### Domain forcing

| Domain | Dataset idea | Lifetime lever |
|--------|--------------|----------------|
| Demography | SSA life tables, CDC Hispanic LE | Mortality / horizon |
| Public finance | OMB historical outlays | Spending category allocation |
| Education | NCES Digest 236.10, CCD finance | School cost + attainment transmission |
| Labor | LEHD/QCEW | Earnings trajectory |
| Health | MEPS + CMS Medicaid | Late-life public cost |
| Legal | EOIR backlog, ORR refugee costs | Administrative + refugee fiscal paths |
| Political economy | CBO state-local 61256 | Who bears the shock |

### Constraint inversion — aggregates beat micro when…

- **Education bucket NPV** → NAS Table 8-12/8-13 beats origin-only ACS.
- **Descendants** → NAS descendant column until PSID arrives.
- **Discount rate** → SSA Trustees band (2.4–3.4%) sensitivity like NAS Ch.8.
- **Unauthorized share** → Pew + DHS LPR residual, not SIPP citizenship alone.

## Tier map (post-brainstorm)

| Tier | Dataset | Lifetime role | Acquire |
|------|---------|---------------|---------|
| A | NAS 2017 full PDF | Education NPV benchmark | **automated** → `external/lifetime/nas/` |
| A | NRC 1997 New Americans | Older education NPV (-$13k `<HS`) | **automated** → `external/lifetime/nrc/` |
| A | Orrenius WP1704 | NAS sensitivity / public-goods critique | **automated** |
| A | Storesletten NBER w9489 | Fiscal heterogeneity by skill | **automated** |
| B | Census linkage inventory + SEHSD WP2024-01 | FSRDC project spec | **automated** |
| B | IRS SOI PUF limitations (06resconf) | Tax engine caveats | **automated** |
| B | Synthetic SIPP landing HTML | Application workflow | **automated** (HTML only) |
| C | Synthetic SIPP microdata | Earnings histories | **apply** |
| C | IRS SOI individual PUF | Tax mapping | **apply** |
| C | PSID | Descendants | **register** |
| C | SSA life tables + Trustees | Mortality + discount | **browser** (curl 403) |
| D | FSRDC SIPP-SSA-IRS + LEHD | Gold standard | restricted |

## Mexico mapping (unchanged principle)

Do not produce a “Mexican lifetime NPV.” Weight NAS cells by Mexico ACS education mix (~47% `<HS` among FB 25–64) and recent-surge slice (`<HS`, YOEP≥2014 → ~437k adults) maps to NAS `<HS` age-25 cell (−$109k individual, 2012$). [SOURCE: NAS 2017 Ch.8]

## Reproduce

```bash
cd infra/immigration-fiscal
bash acquire/setup-lifetime.sh
```

Wired from `acquire/setup.sh` after stage5 pass.

## Disconfirmation

1. NAS positive for average immigrant under baseline assumptions — education mix dominates.
2. Storesletten: lifetime fiscal sign highly sensitive to assumptions (−$36k to +$96k range in his framework).
3. Without PSID/Synthetic SIPP, descendant offset is NAS-calibrated, not re-estimated.
4. SSA mortality/discount files bot-blocked — manual browser pull still needed.

## Round 2 brainstorm (2026-06-15 pass)

### New perturbations

1. **Remittance offset** — World Bank `BX.TRF.PWKR.CD.DT` for Mexico: private outflow not in NAS ledger.
2. **Generational accounting lane** — Lee & Miller w7041 + Auerbach-Oreopoulos c10849 bridge NRC → NAS methodology.
3. **NAP Immigration Debate (1998)** — Lee/Miller fiscal chapter updating NRC with forward-looking model (+$80k PV per 1994 arrival in their frame).
4. **AGI-soon frame** — IZA dp18218: long-run NPV less decision-relevant if labor transforms.
5. **IMF G20 aging note** — demographic dependency context for discount/horizon.
6. **Borjas w22102** — undocumented labor supply elasticity → earnings-path sensitivity, not direct NPV.
7. **Card w11547** — disconfirmation: “new immigration” fiscal/wage pessimism overstated.
8. **BEA state personal income** — state earnings capacity denominator for lifetime allocation.
9. **Medicare Trustees 2024** — late-life public cost / discount anchor companion to SSA (SSA tables still browser-only).
10. **Inversion: annualize NPV** — Lee/Miller convert 3% PV to ~$2,400/yr per immigrant (1994$) for sanity-check vs our SIPP +$1,519/yr Mexico proxy.

### Round 2 acquired (automated)

| Path | Role |
|------|------|
| `lifetime/imf/g20_2025_aging_and_migration.pdf` | AGI/aging macro frame |
| `lifetime/iza/iza_dp18218_agi_soon_migration.pdf` | AGI-soon reframing |
| `lifetime/worldbank/mexico_worker_remittances_*.json` | Mexico remittance series |
| `lifetime/nap/nap_1998_immigration_debate_fiscal_effects.pdf` | Lee/Miller generational fiscal |
| `lifetime/nber/lee_miller_*_w7041.pdf` | Generational accounting |
| `lifetime/nber/auerbach_oreopoulos_*_immigration.pdf` | GA critique/extension |
| `lifetime/aer/lee_miller_2000_*_aer.pdf` | Social Security fiscal short |
| `lifetime/nber/borjas_2016_*_w22102.pdf` | Undocumented earnings |
| `lifetime/nber/card_2005_*_w11547.pdf` | Disconfirmation |
| `lifetime/bea/spi_state_summary_2023.zip` | State income context |
| `lifetime/cms/medicare_trustees_report_2024.pdf` | Late-life Medicare anchor |

### Round 3 brainstorm (2026-06-15)

**New angles:**
1. **Hispanic mortality** — CDC NVSR 72-12 (2021 life tables by Hispanic origin): SSA substitute for NPV horizon.
2. **Capital-tax omission** — Clemens 2023: NAS `<HS` −$109k → **+$128k** with employer capital-income tax adjustment (mandatory disconfirmation).
3. **Refugee fiscal path** — Clemens/Huang/Graham 2018: formal LMA changes fiscal sign for refugee cohorts.
4. **Redistribution politics** — Alesina w24733: fiscal estimates interact with native preferences (not ledger math).
5. **Efficiency vs fiscal** — Clemens/Pritchett 2016: fiscal second-best to migration efficiency gains.

**Round 3 acquired:**

| Path | Role |
|------|------|
| `lifetime/cdc/nvsr72_12_us_life_tables_2021_hispanic_origin.pdf` | Hispanic mortality tables |
| `lifetime/cgdev/clemens_2023_fiscal_effect_capital_tax_adjustment.pdf` | NAS bias correction |
| `lifetime/cgdev/clemens_pritchett_2016_migration_restrictions_wp423.pdf` | Migration efficiency frame |
| `lifetime/cgdev/clemens_huang_graham_2018_refugee_labor_market_access_wp496.pdf` | Refugee LMA fiscal |
| `lifetime/nber/alesina_miano_stantcheva_2018_immigration_redistribution_w24733.pdf` | Redistribution / preferences |

### Round 4 brainstorm (2026-06-15)

**New angles:**
1. **Welfare trajectory** — Borjas w4872 (1970–1990): immigrant welfare recipiency rising faster than natives → transfer-layer calibration for lifetime paths.
2. **Descendant pessimism** — Duncan & Trejo w24394: Hispanic 2nd-gen convergence slower than NAS assumes → downward sensitivity on descendant offset.
3. **Legal-status human capital** — Kuka et al. w24315 (DACA): education returns to status → path for unauthorized → authorized transition.
4. **Federal spend allocation** — OMB Table 3-1 (outlays by function) + Table 12-1 (federal grants): category weights for lifetime cost assignment.
5. **Remittance bilateral** — World Bank USA outflow series complements Mexico inflow (round 2).
6. **Handbook pre-NAS** — Borjas c6051 intro: CA native household +$1,200/yr tax from immigration (1990s frame).

**Round 4 acquired:**

| Path | Role |
|------|------|
| `lifetime/borjas/borjas_2000_handbook_*_c6051.pdf` | Handbook fiscal framing |
| `lifetime/borjas/borjas_1994_immigration_welfare_*_w4872.pdf` | Welfare receipt trajectory |
| `lifetime/nber/duncan_trejo_2018_*_w24394.pdf` | 2nd-gen integration skepticism |
| `lifetime/nber/kuka_shenhav_shih_2018_daca_*_w24315.pdf` | Legal status → education path |
| `lifetime/worldbank/usa_worker_remittances_*.json` | US remittance outflows |
| `lifetime/omb/budget_fy2025_table_3_1_*.xlsx` | Federal outlays by function |
| `lifetime/omb/budget_fy2025_table_12_1_*.xlsx` | Federal grants to state/local |

### Round 5 brainstorm (2026-06-15)

**New angles:**
1. **International fiscal comparator** — Dustmann & Frattini UK CDP 22/13: static fiscal accounting by cohort/skill; EEA vs non-EEA split (methodology transfer, not US numbers).
2. **Assimilation path** — Abramitzky w22381 (mass migration): name-change assimilation → earnings convergence parameter.
3. **Descendant upside** — Abramitzky w26408: intergenerational mobility over two centuries → counterweight to Duncan-Trejo pessimism.
4. **Redistribution politics (EU)** — Alesina w25562: pairs with w24733 for preference-shift channel.
5. **Fiscal accounting grammar** — Green & Kotlikoff w12344: "relativity of fiscal language" → guards against mixing NAS/CBO/Heritage accounting frames.
6. **Return migration** — still no clean public micro (CBO 55967 blocked); attrition remains manual sensitivity.

**Round 5 acquired:**

| Path | Role |
|------|------|
| `lifetime/cream/dustmann_frattini_*_cdp_22_13.pdf` | UK fiscal methodology comparator |
| `lifetime/nber/abramitzky_*_cultural_assimilation_*_w22381.pdf` | Assimilation / earnings path |
| `lifetime/nber/abramitzky_*_intergenerational_mobility_*_w26408.pdf` | Descendant mobility (optimistic bound) |
| `lifetime/nber/alesina_*_redistribution_europe_*_w25562.pdf` | EU redistribution preferences |
| `lifetime/methodology/green_kotlikoff_*_fiscal_language_*_w12344.pdf` | Fiscal accounting methodology |

### Round 6 brainstorm (2026-06-15)

**New angles (shift from NPV benchmarks → offset/local-shock ledger):**
1. **Indirect federal offset** — Colas-Sachs (2024): ~$750/yr indirect fiscal benefit per low-skill immigrant via resident wage/tax spillovers → mandatory disconfirmation band on NAS `<HS` negatives.
2. **Recent synthesis** — Orrenius/Viard/Zavodny AEI 2025: federal-positive average, low-skill direct-negative, indirect effects shrink gap.
3. **Local shock-load** — Gould w33655: asylum seekers ≈60% of 2022–24 sheltered-homelessness rise (NYC/Chicago/MA/Denver) → national NPV useless without receiver-node weighting.
4. **Native descendant channel** — Akers-Boustan w33961: immigration raises mobility for poor native kids, lowers for affluent → pairs with Duncan-Trejo on immigrant 2nd-gen.
5. **Safety-net layer** — Bitler-Hoynes w17667: immigrant SNAP/Medicaid participation post-welfare reform → transfer-path calibration.
6. **Welfare magnets** — Razin-Wahba w17515 + Landais et al. w26454 (Denmark): selection into generous jurisdictions → attrition/legal-status sensitivity.
7. **Firm-level disconfirmation** — Clemens-Lewis w30589: H-2B lottery — restrictions hurt firms, native employment ≥0.
8. **Congestion add-on** — Brookings VMT external-cost paper: commute congestion priced separately from NAS.
9. **Housing nuance** — FRBSF 2023 econ letter: immigrants consume less housing per capita → offsets naive rent-demand stories.
10. **International comparator** — BoC swp2023-57: fiscal-capacity framing parallel to CBO 61256.
11. **Income distribution frame** — Blau-Kahn w18515: immigration × inequality handbook chapter → composition not scalar.
12. **Return migration** — still no clean US public micro (Duleep-Regets/Aydemir-Robinson are earnings-frame, not fiscal); manual attrition sensitivity remains.

**Round 6 acquired:**

| Path | Role |
|------|------|
| `lifetime/econstor/colas_sachs_*_indirect_fiscal_*.pdf` | Indirect federal offset |
| `lifetime/aei/orrenius_*_2025_fiscal_impact_update.pdf` | 2025 fiscal synthesis |
| `lifetime/nber/gould_*_asylum_*_w33655.pdf` | Local shelter shock-load |
| `lifetime/nber/akers_boustan_*_w33961.pdf` | Native-child mobility offset |
| `lifetime/nber/bitler_hoynes_*_w17667.pdf` | Safety-net calibration |
| `lifetime/nber/clemens_lewis_*_w30589.pdf` | Firm-level disconfirmation |
| `lifetime/nber/razin_wahba_*_w17515.pdf` | Welfare magnet (US frame) |
| `lifetime/nber/landais_*_w26454.pdf` | Welfare magnet (Denmark) |
| `lifetime/nber/blau_kahn_*_w18515.pdf` | Immigration × income distribution |
| `lifetime/brookings/vmt_external_cost_*.pdf` | Congestion proxy |
| `lifetime/frbsf/econ_letter_2023_*.html` | Housing-demand nuance |
| `lifetime/banqueducanada/swp2023_57_*.pdf` | Fiscal capacity comparator |

### Round 7 brainstorm (2026-06-15)

**New angles (earnings-path + debate calibration for lifetime projection):**
1. **Task-upgrading earnings path** — Foged-Peri w19315: Denmark refugee quasi-IV → natives shift to less manual work, wages rise → feeds indirect-fiscal / complementarity band in lifetime earnings projection.
2. **National wage complementarity** — Peri-Ottaviano w14188/w11672: −0.7% short-run / +0.6% long-run on average native wages (1990–2006 frame).
3. **Recent wage revival** — Card-Peri w32389 (2024): +1.7–2.6% for less-educated natives 2000–2019 via complementarity.
4. **Borjas debate anchor** — Card-Peri JEL 2016 review + w23504 Mariel race: mandatory sensitivity on low-skill cell calibration.
5. **Welfare inheritance** — Borjas w6175: intergenerational welfare dependency by ethnicity → transfer-path pessimism layer.
6. **Job-quality path** — Shapiro w6195: immigration × job quality (earnings trajectory, not just quantity).
7. **Old-age fiscal layer** — Abel w6229: immigrants/children in PAYG pension → Social Security/Medicare horizon.
8. **Local non-fiscal cost** — Butcher w6067: crime/incarceration channel absent from NAS ledger.
9. **Data discipline** — Edelberg Brookings 2026: CPS invalid for foreign-born *levels* → composition weights from ACS only.
10. **Microsim anchor** — SIPP 2024 Users Guide: admin earnings imputation methodology for annual→lifetime bridge.
11. **School cost scalar** — NCES Digest 236.20 per-pupil expenditure (HTML) for K-12 lifetime cost assignment.
12. **Return migration** — Aydemir-Robinson (Canada) paywalled; no US fiscal micro yet.

**Round 7 acquired:**

| Path | Role |
|------|------|
| `lifetime/nber/foged_peri_*_w19315.pdf` | Task-upgrading / earnings path |
| `lifetime/iza/iza_dp8961_*.pdf` | IZA mirror Foged-Peri |
| `lifetime/nber/peri_ottaviano_*_w14188.pdf` | National wage path |
| `lifetime/nber/peri_ottaviano_*_w11672.pdf` | Complementarity gains |
| `lifetime/nber/card_peri_*_w32389.pdf` | Recent wage effects 2000-2022 |
| `lifetime/card/card_peri_*_jel_review_*.pdf` | Card-Peri Borjas review |
| `lifetime/nber/borjas_*_mariel_*_w23504.pdf` | Mariel race sensitivity |
| `lifetime/nber/shapiro_*_w6195.pdf` | Job quality path |
| `lifetime/nber/borjas_*_w6175.pdf` | Welfare dependency transmission |
| `lifetime/nber/abel_*_w6229.pdf` | PAYG pension fiscal layer |
| `lifetime/nber/butchart_*_w6067.pdf` | Crime/incarceration local cost |
| `lifetime/brookings/edelberg_*_2026_*.html` | CPS level invalidity warning |
| `lifetime/census/sipp_2024_users_guide.pdf` | SIPP earnings imputation docs |
| `lifetime/nces/digest_dt23_236_20_*.html` | Per-pupil school spend anchor |

### Round 8 brainstorm (2026-06-15)

**New angles (composition + attrition + debate stack):**
1. **Low-skill composition over time** — Hanson-Liu-McGee w23753: rise/fall of US low-skilled immigration → time-varying weights for Mexico `<HS` cells, not static ACS snapshot.
2. **Native out-migration attenuation** — Borjas w11610: immigration induces native out-migration; local wage impact attenuated **40–60%** → critical for state/PUMA fiscal attribution (who stays to bear costs).
3. **Pessimistic wage path** — Borjas w9755: 10% labor supply ↑ → 3–4% wage ↓ (education-experience cells).
4. **Mariel debate stack** — Card w3069 (null) + Borjas w21850 (rejoinder) + w23504 (race, round 7) → low-skill cell calibration sensitivity.
5. **Task complementarity** — Peri-Sparber w13389: immigrants in manual tasks, natives upgrade to communication → explains modest wage effects; feeds indirect fiscal band.
6. **Dustmann survey** — w16736: fiscal impacts literature map (methodology guardrails).
7. **Migration × welfare state** — Razin-Sadka-Swagel w15597: political-economy of transfers (pairs w17515/w26454).
8. **Migrant networks** — Borjas-Monras w23756: network-driven immigration paths (destination selection).
9. **Labor spillovers** — Borjas-Grogger-Hanson w12518: immigration × Black employment/incarceration (local distributional cost).
10. **Return migration** — Aydemir-Robinson CHCP wp HTML trap; PMC unauthorized-method PDFs also HTML — still manual.

**Round 8 acquired:**

| Path | Role |
|------|------|
| `lifetime/nber/dustmann_*_survey_w16736.pdf` | Immigration impacts survey |
| `lifetime/nber/razin_*_welfare_state_w15597.pdf` | Migration × welfare state |
| `lifetime/nber/hanson_*_low_skilled_immigration_w23753.pdf` | Low-skill composition time series |
| `lifetime/nber/borjas_monras_*_migrant_networks_w23756.pdf` | Migrant network paths |
| `lifetime/nber/borjas_*_labor_demand_w9755.pdf` | Pessimistic wage elasticity |
| `lifetime/nber/borjas_*_native_internal_migration_w11610.pdf` | Out-migration attenuation (40-60%) |
| `lifetime/nber/card_*_mariel_w3069.pdf` | Card Mariel null anchor |
| `lifetime/nber/borjas_*_marielitos_w21850.pdf` | Borjas Mariel rejoinder |
| `lifetime/nber/peri_sparber_*_task_specialization_w13389.pdf` | Task complementarity |
| `lifetime/nber/borjas_grogger_hanson_*_w12518.pdf` | Black employment spillovers |

### Round 9 brainstorm (2026-06-15)

**New layers (housing + high-skill + legal-status floor + refugee/mortality):**
1. **Saiz elasticity × destination rent** — MSA housing supply inelasticity; immigrants concentrate in low-elasticity markets → rent burden is welfare loss, not price discovery [SOURCE: immigration-causal-saiz-elasticity-rent.md].
2. **Ottaviano-Peri w12497** — wage decomposition precursor to w11672/w14188; separate short/long-run band.
3. **H-1B fiscal layer** — Bound-Khanna-Morales w23153: high-skill path distinct from Mexico `<HS` cells.
4. **Border enforcement selection** — Lozano-Lopez IZA dp4898: enforcement shifts composition, not just stock.
5. **Occupational mobility panel** — IZA dp452: earnings-path dynamics for assimilation calibration.
6. **Refugee political economy** — IZA dp10234: separate ledger from economic immigrant NPV.
7. **ITEP + Pew tax/stock floor** — undocumented tax paid vs unauthorized count prior (copied from main stack).
8. **Full CDC life tables** — all-races NVSR 72-12 for mortality horizon (Hispanic slice alone insufficient).
9. **Scenario ledger bridge** — copy `origin_fiscal_scenario_2023.csv` into lifetime DuckDB for annual↔lifetime joins.

**Round 9 acquired:**

| Path | Role |
|------|------|
| `lifetime/nber/ottaviano_peri_*_w12497.pdf` | Wage decomposition (2006) |
| `lifetime/nber/bound_khanna_*_h1b_w23153.pdf` | H-1B economic impact |
| `lifetime/iza/iza_dp4898_*_border_enforcement_*.pdf` | Mexican selection under enforcement |
| `lifetime/iza/iza_dp452_*_occupational_mobility_*.pdf` | Immigrant occupational mobility panel |
| `lifetime/iza/iza_dp10234_*_refugee_*.pdf` | Refugee migration political economy |
| `lifetime/cdc/nvsr72_12_*_all_races.pdf` | Full US life tables 2021 |
| `lifetime/saiz/saiz_2010_msa_elasticity.dta` | Housing supply elasticity by MSA |
| `lifetime/itep/*` | Undocumented tax floor |
| `lifetime/pew/*` | Unauthorized stock prior |
| `lifetime/derived/stage3_proto/*.csv` | Scenario ledger bridge (when built) |

**Blocked:** Census np2023-t1.xls (404); SSA life tables (403).

### Round 10 brainstorm (2026-06-15)

**New layers (return migration + incidence bridge + admin):**
1. **Return migration / assimilation bias** — Duleep-Regets IZA dp631/dp8628: selective emigration biases observed assimilation and lifetime NPV; build attrition sensitivity not point estimate.
2. **OECD migration flows** — Ortega-Peri w14833: bilateral migration 1980–2005; macro flow context for composition weights.
3. **Employer recruitment** — IZA dp331: firm-driven high-skill path separate from family/LPR mix.
4. **Derived incidence bridge** — stage2 county school/housing/IRS + stage5 state/receiver CSVs copied into lifetime staging for DuckDB joins.
5. **Admin/enforcement ledger** — CBP/ICE FY25–26 budget PDFs + DHS LPR-by-country xlsx: federal enforcement cost vector (not in NAS NPV).
6. **Health annual→lifetime** — MEPS + SIPP-MEPS health cells in lifetime DuckDB for horizon bridge.
7. **Education bucket + SIPP cells** — public MVP cells copied for microsim scaffold.

**Round 10 acquired:** see manifest rows `ortega_*_w14833`, `iza_dp631`, `iza_dp8628`, `iza_dp331`, `derived/stage2/*`, `derived/stage5/*`, `admin/cbp_*`, `admin/ice_*`, `dhs/plcy_lpr_*`.

**Blocked:** Fed FEDS note 20240105 (404); Census pop projections (404).

### Round 11 brainstorm (2026-06-15)

**New layers (bridge + unit fix + political equilibrium + restriction admin):**
1. **Annual↔NPV bridge** — Lee-Miller w7041 + remittances + SIPP scenario: forbid sign comparison without discount/scope lock (cluster M).
2. **F-33 thousands bug** — `current_spend_per_pupil` was ~$21 not ~$21k; fixed `*1000` in `build_stage2_incidence_context.py`; Mexico now ~$20,907/pupil [INFERENCE: verified post-rebuild].
3. **Welfare-state political economy** — Razin w15597/w17515: skill mix and transfers are equilibrium, not exogenous (cluster O).
4. **Restriction admin ledger** — CBP/ICE budgets + receiver episodic vs federal annual dominance test (cluster P).
5. **CBO layer split** — federal $897B deficit improvement (surge) vs state/local $9.2B direct cost — mandatory disconfirmation pair.
6. **Remittance private layer** — Mexico ~$66.2B inbound (2023 WB) vs ~$664M scenario-subset federal net proxy or ~$12.9B full-stock federal net proxy; label denominator before comparing layers.
7. **PAYG pension phase** — Abel w6229 (scanned PDF): lifecycle timing explains annual+ vs lifetime− compatibility.
8. **NBER ID fishing killed** — w2748/w15248/w24721 probes rejected (wrong titles); Lazear self-selection still manual.

**Round 11 acquired:** derived CSV refresh only (school_finance + origin_fiscal_scenario post unit fix). No new PDFs.

**Blocked:** CBO 59752 deportation PDF (curl 403); SSA life tables (403); Storesletten correct WP (Cleveland/Minneapolis 403); Fed FEDS note (404).
