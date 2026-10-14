**Verdict:** In 2024, the Mexican-origin union's consumption caused about **6,100 premature deaths from PM2.5**. About **4,900 of those deaths were among residents outside the group**. At the repo's DOT value of a statistical life, $13.7m, plus 3% for illness, that is **$70bn a year of harm to other residents (range $31–122bn), or $1,700 per member**. [CALCULATION: `air_items.py` → `derived/items.csv`]

Per head, the group causes 35% less PM2.5 exposure than the average resident because it consumes less. About a fifth of the pollution it causes falls on its own members. A same-size group of average residents would impose $116bn on outsiders, so the **normalized figure is −$47bn (−$82bn to −$18bn)**.

The concentration–response function (CRF) drives most of the range. The low end uses Wu et al. 2020, applied to people 65 and older. The high end takes Di et al. 2017's estimate for concentrations below 12 µg/m³ and extends it to all adults.

Other items:
- **Government services used by the group:** $6bn ($2–16bn).
- **Ozone:** $3bn ($1–18bn); this estimate is speculative.
- **CO2** [FRAMING-SENSITIVE]: the group adds a net 471 Mt a year. That figure subtracts the Mexico-born members' footprint in their country of origin and adds the Mexican consumption their remittances pay for. At EPA's 2023 social cost of carbon, $250/t in 2024 dollars, the global damage is $118bn. Of that, **$12bn ($2–48bn)** falls on other US residents.

**Non-Hispanic Black comparator**, same method:
- PM2.5: $85bn to others ($38–139bn), or $2,030 per member;
- PM2.5 normalized: −$34bn;
- CO2: $14bn.

Positive figures are costs to people outside the group; negative figures mean less cost than a same-size group of average residents.

Model: claude-opus-5-5

**Read the absolute figure with its scale.** In 2024, consumption-driven PM2.5 from US sources did about $1.09 trillion of harm at the DOT value of a statistical life. That is roughly $3,200 per resident, and every resident's consumption contributes to it. The absolute item is the group's share of that total. It fits the account's with-and-without comparison, but most of its size reflects scale, not anything specific to the group; the normalized item carries the group-specific part.

Life-year valuation is a large lever [FRAMING-SENSITIVE]. PM2.5 deaths fall mostly on older people. Valuing them by life-years instead of the flat value of a statistical life would put the central near $26bn. That assumes about 10 life-years lost per death [INFERENCE, UNVERIFIED].

Lane opened 2026-09-28 20:55 JST; computation run 21:32 JST (both from `date`). Frame: the stationary 2024 comparison with and without the 40,896,574 CPS 2025 Mexican-origin residents; effects on everyone else; 2024 dollars.

## Verdict table

$bn a year, low / central / high. Low and high are the minimum and maximum over the full factorial grid of arms (2,187 cells for PM2.5; 19,683 for CO2).

| Item | Group | Absolute | Per member (central) | Normalized | Evidence |
|---|---|---:|---:|---:|---|
| PM2.5 from consumption, DOT VSL | Mexican-origin | 31.5 / **69.7** / 122.5 | $1,704 | −81.8 / **−46.5** / −17.9 | contested (modelled) |
| — same, EPA VSL ($11.5m) | Mexican-origin | 26.5 / 58.6 / 102.9 | $1,432 | — | alternative; never add both |
| PM2.5 from government services the group uses | Mexican-origin | 1.6 / **6.2** / 16.3 | $152 | −2.8 / 0.1 / 3.1 | speculative |
| Ozone from consumption | Mexican-origin | 0.6 / **2.5** / 18.4 | $61 | −12.3 / −1.7 / −0.4 | speculative |
| CO2, share of damage borne by other US residents [FRAMING-SENSITIVE] | Mexican-origin | 1.7 / **12.0** / 48.2 | $293 | −21.5 / −4.3 / −0.5 | contested |
| PM2.5 from consumption, DOT VSL | NH Black | 38.5 / **85.1** / 138.6 | $2,028 | −64.8 / **−33.7** / −13.8 | contested (modelled) |
| — same, EPA VSL | NH Black | 32.3 / 71.5 / 116.5 | $1,705 | — | alternative |
| PM2.5 from government services | NH Black | 1.7 / 5.9 / 14.3 | $140 | −2.7 / −0.4 / 0.8 | speculative |
| Ozone | NH Black | 0.8 / 3.1 / 20.8 | $73 | −9.7 / −1.2 / −0.3 | speculative |
| CO2 [FRAMING-SENSITIVE] | NH Black | 2.2 / **14.3** / 54.4 | $340 | −10.8 / −2.2 / −0.2 | contested |

Central intermediate values:

| Quantity | Mexican-origin | NH Black | Basis |
|---|---:|---:|---|
| Population share *s* | 12.15% | 12.46% | CPS ASEC 2025 [DATA] |
| Caused exposure per head vs average, *r* | 0.653 (0.61–0.73) | 0.77 (0.72–0.80) | Tessum 2015 × CE 2024 [SOURCE/CALCULATION] |
| Exposure breathed vs average, *E* | 1.12 | 1.21 | Tessum 2015 [SOURCE] |
| Group share of residents in its own urban areas, *ι* | 0.302 | 0.25 (assumed) | ACS 2024 PUMS, 481 urban areas [CALCULATION]; Black [INFERENCE] |
| Self-share *σ* | 0.193 (0.163–0.229) | 0.185 (0.157–0.222) | formula below [CALCULATION] |
| Deaths caused / deaths among others | 6,122 / 4,938 | 7,403 / 6,030 | [CALCULATION] |
| Harm to others vs a same-size average group | 0.60 | 0.72 | *r*(1−*σ*)/(1−*s*) |
| CO2 footprint per head vs average | 0.772 | 0.868 | [INFERENCE on weights, CE on ratios] |
| CO2 net addition | 471 Mt (495 gross − 45 origin + 21 remittances) | 571 Mt | [CALCULATION] |

National deaths from PM2.5 caused by US anthropogenic emissions [CALCULATION: `derived/national_deaths.csv`]:

| CRF | 2019 (Bekbulat et al.) | 2024, central trend (range) | 2024, consumption-attributable |
|---|---:|---:|---:|
| Wu et al. 2020, ages 65+ (low) | ~52,000 | 51,400 (49,000–53,900) | 41,800 |
| Orellano et al. 2024, RR 1.095 (central) | 96,000 | 94,800 (90,400–99,400) | 77,200 |
| Di et al. 2017, below 12 µg/m³, extended to adults (high) | 134,900 (scaled) | 133,200 (127,000–139,700) | 108,400 |

## Method and sources

### 1. National deaths in 2024

- **Anchor.** Bekbulat, Ünal, Sharma, Apte and Marshall, *ES&T Letters* 2025 ([doi:10.1021/acs.estlett.5c00901](https://doi.org/10.1021/acs.estlett.5c00901); author PDF [Marshall_200.pdf](https://depts.washington.edu/airqual/Marshall_200.pdf) → `_cache/bekbulat.txt`) run InMAP source–receptor matrices on EPA's EQUATES inventory for 2002–2019. They estimate PM2.5 deaths from US anthropogenic emissions [SOURCE]:
  - 2019: 96,000 with the Orellano 2024 meta-analysis (RR 1.095 per 10 µg/m³);
  - 2019: ~52,000 with Wu 2020, applied to the 65+ Medicare population;
  - 2019: ~139,000 with Lepeule 2012;
  - 2002: 197,000.

  They exclude wildfire, dust, biogenic and transboundary sources, which no one's consumption causes. Their population-weighted anthropogenic PM2.5 in 2019 is 4.5 µg/m³.
- **High arm.** Di et al. 2017, *NEJM* (Medicare, 2000–2012), found all-cause mortality rose 7.3% per 10 µg/m³, and 13.6% (95% CI 13.1–14.1) in person-years below 12 µg/m³ [SOURCE: PubMed 28657878 abstract, `_cache/di2017_abstract.txt`]. Scaling Orellano's 96,000 by ln(1.136)/ln(1.095) = 1.405 gives 134,900.

  The same scaling reproduces Bekbulat's Lepeule total within 0.3% (138,600 against ~139,000), so the log-ratio shortcut holds. Restricted to Di's own 65+ population (76.2% of 2024 deaths), the arm gives 102,800, about the central value. [CALCULATION: `derived/params.csv`]
- **2019 to 2024.** The update multiplies an emissions factor by a baseline-deaths factor:
  - Sector weights are the 2019 deaths in the ChemRxiv version, which used the Nasari CRF [SOURCE]: electricity 4,600; industry 18,500; transportation 15,700; agriculture 22,800; residential 4,700.
  - Assumed 2019→2024 changes [INFERENCE]: electricity ×0.50–0.70, industry ×0.90–1.00, transportation ×0.75–0.85, agriculture ×1.00–1.05, residential ×0.95–1.02. These extend the 2002–2019 trends that Bekbulat reports: coal retirements, vehicle-fleet turnover, and flat-to-rising farm ammonia.
  - Together these give an emissions factor of ×0.875 / 0.918 / 0.962.
  - US deaths rose from 2,854,838 in 2019 [TRAINING-DATA] to 3,072,666 in 2024 [SOURCE: NCHS Data Brief 548], a factor of ×1.076.
  - Net effect: ×0.94–1.04, so 2024 deaths are about the same as 2019's.

### 2. Attribution to consumption

- **Source.** Tessum et al. 2019, *PNAS* 116:6001, full text [SOURCE: PMC6442600 via NCBI efetch, `_cache/tessum2019_text.txt`]. The year is 2015; emissions come from NEI 2014, dispersion from InMAP, and demand from the BEA input–output tables, with personal consumption split by the CE survey. Of the 102,000 deaths caused by US anthropogenic emissions:
  - **83,000 (81%)** come from US personal consumption. This includes 16,000 from residential investment and 21,000 from other private investment, allocated in proportion to consumption.
  - 8,000 come from government end use.
  - 11,000 come from exports.
- **Exposure by group.** Per-head exposure caused, relative to the average: Hispanic 0.69, Black 0.77, white/other 1.12. Exposure experienced, on the same basis: 1.12, 1.21 and 0.93. Tessum finds that the amount consumed matters more than what is consumed.
- **Scaling to the Mexican-origin union.** The CE 2024 interview survey gives per-person spending by the reference person's origin [CALCULATION: `ce_energy.py` → `derived/ce_group_spending.csv`]. The Mexican-origin definition is HORREF1 1–3, as in `consumption_key_2026_09_24/ce_pumd.py`; 1,739 Mexican-origin consumer-unit quarters. Relative to all residents:

  | Group | Total spending | Gasoline | Home energy |
  |---|---:|---:|---:|
  | Mexican-origin | 0.706 | 1.063 | 0.727 |
  | All Hispanic | 0.746 | — | — |
  | Non-Hispanic Black | 0.802 | — | — |

  - Central *r* = 0.69 × 0.706/0.746 = **0.653**.
  - The low value, 0.61, allows for CE's under-coverage of top spending, which would make the true ratio lower.
  - The high value, 0.73, is the consumption key lane's CPS resources with CE saving ratios: 8.894% of consumption against 12.145% of population.
  - Tessum's Hispanic and Black ratios sit 4–8% below the CE 2024 spending ratios, which matches the composition effect it calls secondary.

### 3. Share that falls on people outside the group

Tessum reports the exposure each group causes and the exposure it breathes, but not whose pollution each group breathes. The self-share is therefore built as *σ* = *L*·*ι* + (1−*L*)·*s*·*E*:
- **Local part, *L*** (0.25 / 0.35 / 0.45): the share of the group's pollution released in its own metro areas. There it falls in proportion to the group's share of residents, *ι* = 0.302. This is the population-weighted group share across the 481 urban areas in the congestion lane's ACS 2024 PUMS table, which hold 31.2m members [CALCULATION from `congestion_2026_09_23/derived/ua_exposure.csv`].

  *L* is anchored on Goodkind et al. 2019, *PNAS* (PMC6500143): 33% of all PM2.5 damage occurs within 8 km of the source and 25% beyond 256 km [SOURCE]. The group's tailpipe and household emissions are local, and its gasoline spending per person is 1.06× the average; its supply chains are not local. [INFERENCE]
- **Non-local part:** spreads like all consumption-caused PM2.5, which the group breathes at *E* = 1.12 times the average (1.05–1.20).
- **Black comparator:** *ι* is set at 0.25 (0.20–0.30) [INFERENCE; not measured here].

### 4. Valuation

- **Value of a statistical life (VSL):** the DOT 2024 value, $13.7m [DATA: `crime_victim_cost_2026_09_23/derived/unit_costs_victim_only_2024usd.csv`]. The alternative is EPA's $7.4m in 2006 dollars [TRAINING-DATA] × CPI-U 313.689/201.6, which gives **$11.5m**. EPA's income adjustment would lift that toward about $12.5m [INFERENCE].
- **Morbidity:** +1% / 3% / 6% [TRAINING-DATA: in EPA's PM regulatory analyses, illness is a few percent of mortality benefits].
- **Timing:** the comparison is an annual steady state, so the lag between exposure and death is not discounted.

### 5. Government services and ozone

- **Government services.** Tessum attributes 8/102 of deaths to government end use. The row multiplies that by:
  - the group's population share;
  - its use relative to the average (1.1, for the extra school-age children; range 0.9–1.3);
  - the share of those budgets that shrink with the group, 0.35–0.80. This is below the main case's 0.60–1 because defense stays fixed and the split between defense and civilian emissions is unmeasured. [INFERENCE]
- **Ozone** is priced as a ratio to PM2.5 deaths:
  - central 0.036, from Fann et al. 2012 (4,700 ozone deaths against 130,000 PM2.5 deaths in 2005; the PM2.5 figure is confirmed in Goodkind [SOURCE], the ozone figure is [TRAINING-DATA]);
  - low 0.02;
  - high 0.15, for long-term ozone CRFs [UNVERIFIED].

### 6. CO2 [FRAMING-SENSITIVE]

This arm follows `frontier_execution_2026_09_17/social/institutions-environment.md`: count emissions added globally, not emissions moved.
- **Per-head footprint.** US consumption-based CO2 was 5,431.7 Mt in 2023 (Global Carbon Budget via OWID [DATA: `_cache/owid-co2-data.csv`]). Scaled by the 2024/2023 territorial ratio (4,904/4,918), that is **15.68 t per resident**.
- **Group footprint ratio** = 0.772, a weighted sum:
  - 33% direct household energy at 0.80. CE energy spending is 0.899 of the average; the 0.80 adjusts for California's higher prices and cleaner grid.
  - 12% government at 1.0.
  - 55% other spending at 0.706.

  The weights are [INFERENCE]: household fuel, electricity and gasoline come to about 1.9 of 5.4 Gt [TRAINING-DATA]. The result is **495 Mt** gross.
- **Origin counterfactual** for the 12.22m Mexico-born: Mexico's consumption-based footprint of 4.355 t (2023) × 0.85 (0.7–1.0), because migrants come mostly from the middle and lower-middle of Mexico's income distribution. That removes **45 Mt**.
- **Remittances.** Remittance-funded Mexican consumption adds $52.9bn × 0.40 kg/$ = **21 Mt**. The $52.9bn is the consumption key lane's corridor central (`derived/remittance_flows.csv`); the kg/$ figure is [INFERENCE].
- **US-born members** count in full, as the brief specifies. **Net addition: 471 Mt.**
- **Social cost of carbon.** EPA 2023 Table ES.1 (2020$) gives $190 / $230 per tonne at 2% for 2020 / 2030 emissions [SOURCE: EPA SC-GHG final report]; interpolated for 2024, that is $206. At CPI ×1.212, that is **$250** in 2024 dollars. Low: the 2021 interagency working group's (IWG's) 3% value, $55 (2020$) → $67 [TRAINING-DATA]. High: EPA's 1.5% value, $356 → $431.
- **US share of global damage:** 11%, range 7–23%:
  - Nordhaus's decomposition gives 10.6%, $4.24 of $40 [SOURCE: Kotchen, citing Nordhaus 2015];
  - Ricke et al. 2018 put the US at about $48–50 of a $417 global median [SOURCE: *Nature Climate Change* abstract + ScienceDaily];
  - the 7–23% range is the 2010 IWG's [TRAINING-DATA].
- **Share borne by other residents** = 1 − the group's income share (7.27%) = 0.927.
- **Black comparator:** no origin offset, although about a tenth of the group is foreign-born.

## Disconfirmation

1. **Is the CRF too steep at today's low concentrations?** If there were a threshold near the lowest observed levels, damages would shrink sharply. The low arm (Wu, 65+ only) is 54% of the central. Studies on the other side include Di 2017, which finds a steeper effect below 12 µg/m³ in the Medicare population [SOURCE], and Wu 2020 [TRAINING-DATA]. EPA's Integrated Science Assessment calls the link causal [TRAINING-DATA]. Evidence level: contested at the low end, well established overall. The range spans it.
2. **Valuation by age** [FRAMING-SENSITIVE]. The deaths are concentrated among older people. A value per life-year derived from the $13.7m VSL (40 years at 3% → $0.59m a year), applied to about 10 life-years lost per death, gives about 0.37 × VSL. On that basis the central would be **about $26bn**. The DOT and EPA convention applies one VSL at every age; the repo's victim lane does the same.
3. **Is consumption the right attribution?**
   - Steel-man for a larger figure: the group works disproportionately in agriculture, construction and trucking, and agriculture is now the largest PM2.5 source. A production-based count would load those emissions on the group.
   - Against it: removing workers does not remove demand. Output would move to other workers, machines or imports. Imports would lower US PM2.5, which would add to this cost but move emissions abroad.
   - Rebound, another residents' response not modelled: other residents consuming more when prices fall would claw back part of the reduction.
   - This lane keeps Tessum's consumption frame and does not model either general-equilibrium response. [FRAMING-SENSITIVE]
4. **Model bias.** InMAP's population-weighted mean bias is −3.1 µg/m³ against monitors, partly because it leaves out non-anthropogenic sources [SOURCE: Bekbulat]. If it also understates anthropogenic secondary particles, the true totals would be higher.
5. **Self-share.** The approximation could miss neighborhood-level clustering along freeways. If *L* = 0.6 and *ι* = 0.35, *σ* ≈ 0.25 and the absolute figure falls 7%. The grid's highest *σ*, 0.229, is close to that.
6. **Relative consumption drift.** Tessum's ratios describe 2015. With no composition discount, *r* would be CE 2024's 0.706, and the figure 8% higher.
7. **Search for contrary evidence.** No study found that Hispanic or immigrant consumption causes more PM2.5 per head than average. Tessum 2019 and its sequel give the reverse. The attribution rests on one group's model family (InMAP/EIEIO). A different pollution–income gradient, such as environmental Engel curves with elasticity below one, would raise *r* toward 0.75 [TRAINING-DATA, not verified].
8. **CO2.** The arm is dominated by the SCC (×6.4 from low to high) and the US share (×3.3). A US-only damage measure excludes costs that reach US residents through the rest of the world. EPA treats this as a reason to use the global value [SOURCE: EPA report text]. The global damage from the net 471 Mt is $118bn.

## Double counting

- **Fiscal account:** it charges the group's own public health use and government costs. No line charges pollution harm to other residents, so nothing overlaps. Premature deaths of retirees reduce pension and Medicare outlays. Neither this lane nor the account nets that out.
- **Congestion** (`congestion_2026_09_23`): prices time and private fuel only. Extra emissions from idling in congestion are counted nowhere; they are small.
- **Road crashes** (parallel lane): separate harm, no overlap.
- **Government-services row:** the account charges the dollar cost of those services; this row charges their emissions. It belongs beside the account only where the main case lets those budgets shrink, which it does for schools and general government.
- **EPA-VSL row:** an alternative to the DOT row; never add both.
- **Ozone and PM2.5:** separate pollutants attributed from the same consumption; no overlap.
- **CO2 and PM2.5:** one is a climate harm and the other a local health harm. Using both is not double counting, but CO2 stays in its own flagged arm.

## What can be added beside the account

[2026-09-28, later: the operator added the PM2.5 absolute row (`pm25_consumption`, $69.7bn) to the social rows of the fiscal-plus-social total, from the September 27 case on. The normalized row sits beside it, never added. CO2, ozone, government services and the EPA-VSL row stay out ([decision](../../../decisions/2026-09-28-social-items-pollution-crashes.md)).]

| Row | Add? | Figure |
|---|---|---|
| PM2.5 from consumption, absolute | Yes, as a social item under the with/without frame, flagged that its size is mostly national scale | **$70bn** ($31–122bn) |
| PM2.5, normalized | In normalized tables | **−$47bn** |
| Government services | With a flag, only where the relevant budgets respond | $6bn ($2–16bn) |
| Ozone | Note only; speculative | $3bn |
| CO2 | Separate [FRAMING-SENSITIVE] arm; keep out of the social total | **$12bn** ($2–48bn); global damage $118bn |

## Files covered and skipped

- **Written:**
  - `RESULT.md`;
  - `ce_energy.py`, which writes `derived/ce_group_spending.csv`;
  - `air_items.py`, which writes `derived/items.csv`, `items_detail.csv`, `national_deaths.csv` and `params.csv`;
  - `_cache/`: the Tessum 2019 XML and text, the Bekbulat PDF and text, the Di 2017 abstract and the OWID CO2 CSV.
- **Read from the repo:**
  - the CPS target population and Black comparator profile;
  - the victim lane's unit costs;
  - the consumption key lane's CE 2024 interview zip, BLS CPI files and remittance flows;
  - the congestion lane's `ua_exposure.csv` and `nhts_ratios.csv`;
  - `institutions-environment.md`.
- **Skipped or blocked:**
  - Tessum SI (Table S15 CRFs, S16–S18 consumption): PMC's file route returns a bot page. The main text had every number used.
  - Tessum 2021 *Science Advances*: EuropePMC returned 503, and Bekbulat's sector split replaced it.
  - EPA emissions Trends data for 2019–2024: not fetched, so the trend factor is assumed.
  - Fann 2012: PMID 21627672 was found but not read, so the ozone ratio is [TRAINING-DATA].
  - The 2010 IWG technical support document (the 7–23% range), EPA's VSL page and the Ricke primary table: not fetched.
- **Firecrawl** was not used (402).

**Gaps and next queries**
- [GAP] Pin the 2019→2024 trend with EPA's national Tier 1 emissions (2019 vs 2024) or NEI 2023.
- [GAP] Measure Black metro-level *ι* from ACS PUMS by core-based statistical area.
- [GAP] Replace the *σ* approximation by running the ISRM (Zenodo record 2589760) on the group's consumption, locating tailpipe and household emissions at its residences.
- [GAP] Verify the Fann 2012 ozone ratio, the IWG 2010 domestic share and EPA's 2024-dollar VSL from their primary sources.

## Log

- 2026-09-28 20:55 JST — lane directory and stub created. Read the repo CLAUDE.md, the environment memo, the target-population CSV, the Black comparator's profile and the victim lane's unit costs.
- 2026-09-28 21:25 JST — checkpoint 1: primary numbers in hand (Tessum 2019 full text, Bekbulat 2025, Goodkind 2019, EPA SC-GHG Table ES.1, OWID/GCB, US-share sources).
- 2026-09-28 21:32 JST — `ce_energy.py` and `air_items.py` run (rc 0; range-order assertion passed); `derived/` written.
- 2026-09-28 21:35 JST — RESULT.md written in full; untagged claims in the first disconfirmation item tagged; researcher memory note saved. Lane not committed (brief: do not commit).
- 2026-09-28 22:43 JST (lead): the operator added `pm25_consumption` (absolute) to the social rows of the fiscal-plus-social total (decision 2026-09-28-social-items-pollution-crashes); lane outputs unchanged.

## P7 correction, 2026-10-14: mortality receivers and common life-year arm

**Verdict:** At the current row-4 source frame, replacing exposure self-share with an age-mortality-weighted self-share raises the consumption row from **$68.092104bn to $74.427766bn**, **+$6.335662bn at each personal end**. The self-share is **11.5902%**, rather than 19.1161%. The common crime-lane life-year arm is **$28.975658bn** at 0% real discount and **$35.448484bn** at 3%, beside the uniform-VSL figure. The $5bn review bar is crossed by the self-share correction and the valuation arms. These are conditional model estimates, not observed group-attributable deaths. [CALCULATION: `mortality_items.py` → `derived/mortality_items.csv`, `mortality_context.json`]

### Population, receiver and valuation declarations

`population_basis_2026_09_29/derived/frame_counts.csv` supplies the source union, 39,712,493.3312, and civilian denominator, 335,543,722.1788. The unchanged exposure formula reproduces that lane's **68.092103594** control within 1e-9bn. Historical `air_items.py` and its original files stay unchanged: their 40.90M control remains 69.680798370bn. Changing the source population frame and changing mortality receivers are separate operations. [DATA: `frame_counts.csv`, `reeval.csv`; CALCULATION: `derived/mortality_gates.json`]

Receiver ages come from **ACS 2024 one-year person microdata**, including group quarters. Baseline rates are parsed from [NCHS Data Brief 548, table for Figure 3](https://www.cdc.gov/nchs/products/databriefs/db548.htm), with the infant rate from the primary 2024 life table. Common national age rates isolate age composition: ethnicity-specific survival, disease risk and county-specific mortality are held equal within age. The ACS identified union has 39.429519M people; its age/place profile is calibrated to the desired union count by a single factor, with the complement transferred from nonmembers so every national and PUMA total is conserved. This bridge is an assumption, not the fiscal account's person-level raking. [SOURCE: pinned `_cache/db548.html`, `_cache/lt2024_Table01.xlsx`; DATA: pinned ACS archive; ASSUMPTION]

For the nonlocal component, turn exposure share *p = sE* into death share *p r / (1−p+pr)*, where *r* is the group's expected baseline deaths per all-age resident divided by nonmembers'. For the local component, allocate ACS age cells from PUMAs to 2,612 urban areas using the preserved crosswalk; weight areas by member population. Apply the measured local death-versus-population odds ratio to the original *iota* arm. Hold *L*, *E*, *iota*, national PM deaths, consumption attribution and all original CRF/trend arms fixed. This preserves the original spatial assumptions while correcting the age-risk mismatch; it does **not** supply a missing consumption-source-to-receptor matrix. The central national mortality share of the union is **5.98981%**, distinct from the group-source self-share of 11.5902%. [CALCULATION: `receiver_context`, `self_share` → `mortality_context.json`; ASSUMPTION: local source weights and within-component exposure/age independence]

The Orellano central source applies to all ages (Bekbulat Table 1, author PDF inspected); Wu's arm uses ages 65+, and the preserved Di-to-adults extension uses 18+. Life-years are weighted over the modelled outsider deaths, using national and local outsider age structures. The open 85+ interval uses the primary period table's death distribution to avoid interpreting survey topcodes as exact ages. `crime_victim_cost_2026_09_23/vsl_standard.py` owns the common valuation: uniform DOT 2024 VSL or life-years calibrated to it at age 40, 0% central and 3% beside. Expected remaining years are **15.2107**, with a mortality value of **$5.08259M per death** at 0%; the prior paragraph's unverified ten-year guess is superseded for this arm. The original morbidity dollars remain fixed instead of being multiplied by the mortality life-year ratio. [SOURCE: primary NVSS 2024 life table, pinned and byte-equal to the crime source; CALCULATION: `mortality_context.json`; FRAMING-SENSITIVE: age-dependent valuation and age-40 calibration]

| Change from current central, $bn at both personal ends | Identified union | Conditional lineage, fixed identified-union receiver boundary |
|---|---:|---:|
| Current original PM row | 68.092104 | 74.182130 |
| Mortality-weighted PM, uniform VSL | 74.427766 | 81.084442 |
| Change | +6.335662 | +6.902312 |
| Same mortality receivers, life-years 0% | 28.975658 | 31.567185 |
| Change from original | −39.116446 | −42.614946 |
| Same mortality receivers, life-years 3% | 35.448484 | 38.618928 |

[CALCULATION: `derived/mortality_items.csv`; ASSUMPTION: lineage consumption factor **1.089438076069**, read from the preserved original consumer snapshot, identical at specifications 16 and 11.]

The lineage rows extrapolate source emissions at the existing consumer key while retaining the **identified-union recipient boundary**. They therefore still count unobserved added descendants among outsider receivers. Beside, exchangeable added recipients imply factor **0.989724818421**, and uniform harm to people outside the lineage becomes **$80.251285bn**. This factor is assumed; without a recipient matrix the no-data factor bound is 0–1. Do not call the fixed-boundary figure an identified full-lineage externality. [CALCULATION: `mortality_context.json` `lineage_fixed_boundary`; ASSUMPTION]

Conditional ACS SDR SE for the union's uniform-VSL row is **$0.032281bn** (self-share SE 0.00038345). Rates, source assumptions and the population bridge factor are held fixed; this is survey variation only and does not quantify the much larger model uncertainty. Signed ACS replicate weights are preserved, as the primary Census 2024 dictionary specifies; primary population weights remain nonnegative. Both death and dollar conservation gates cover every 2,187-cell/81-weight grid. [SOURCE: pinned `_cache/acs2024_dictionary.pdf`; CALCULATION: `mortality_items.py`, `mortality_gates.json`]

### Integration and re-spending primitives

Use `derived/mortality_items.csv`, keys `item`, `group`, `measure`, `population_basis`, `valuation`, `real_discount_rate`. Replace `pm25_consumption` with `pm25_consumption_mortality` at `row4`, or with `pm25_consumption_mortality_vsly` at a specified discount rate; never add these alternatives. `lineage_fixed_boundary` rows already include the consumer factor. Comparator, beneficiary, valuation and overlap declarations travel with each row. No fiscal, crime, congestion, government-service or re-spending row is changed here.

For the parent re-spending producer, `mortality_context.json.row4` exposes *D*, *theta*, caused and outsider deaths, `national_group_baseline_mortality_share`, `without_group_receiver_fraction_fixed_geography`, `uniform_harm_per_spending_usd`, and `national_other_vsly_harm_per_spending_usd_r0.0` / `_r0.03`. National CE spending is quarterly per-person total ×4 × the matching source-frame population, not national PCE; private investment follows consumption as in the original source attribution. Uniform harm is **$0.10206245 per spending dollar** before receptor adjustment; the national other-resident receiver fraction is **0.94010190**. The context's government-use primitive is **$6.644171bn**, under the original government-use and response assumptions, supplied separately for the parent's mirror row. [CALCULATION: `mortality_context.json`; ASSUMPTION: spending mix and private-capital adjustment]

### Binding caps: dated facts, with the missing quantities explicit

- **ARP SO2 auction, 26 March 2024:** spot and advance clearing price **$0.02/ton**. This is an auction observation, not an estimate of a marginal health cost. [SOURCE: [EPA 2024 auction](https://www.epa.gov/power-sector/2024-so2-allowance-auction), pinned HTML, parsed by `primary_caps`]
- **CSAPR prices, February 2024:** EPA reports original annual SO2/NOx allowances at **$2–3/ton**, and Group 3 seasonal allowances at **$925/ton on 28 February**. Those are dated observations, not year averages or year-end prices. [SOURCE: EPA March 2024 partial-denial enclosure, pinned `_cache/csapr2024_feb_prices.pdf`, p.30, parsed]
- **Twelve-state Revised CSAPR Update, 2024 season:** the May 2025 rule records budget **96,975**, carry-in bank **56,869**, available allowances after its retrospective change **155,525**, and reported emissions **84,189 tons**. The implied residual **71,336** is arithmetic, not a separately observed final bank. Emissions were **86.8152% of the unamended annual seasonal budget**. This is seasonal NOx for those states; it does not describe national annual SO2/NOx. [SOURCE: [90 FR 21423, footnote 11](https://www.govinfo.gov/content/pkg/FR-2025-05-20/pdf/2025-08964.pdf); CALCULATION: `derived/binding_caps.json`]
- **[GAP] Exact ARP 2024 bank and annual CSAPR SO2/NOx banks.** EPA's current [progress page](https://www.epa.gov/power-sector/progress-report-program-compliance-and-market-activity) explicitly exposes data through 2022. The [allowance-data page](https://www.epa.gov/power-sector/allowance-data) routes 2024 account/compliance queries to CAMPD; the official account API probes returned HTTP 403, preserved in `_cache/cap_probe_status.json`. No older bank is substituted. CAMPD also needs a year-end/vintage/use-year definition; current holdings alone would not reconstruct a 2024 bank.
- **[GAP] Share of marginal precursor emissions under binding caps:** `null`, not zero. Coverage, a nonzero bank or a positive allowance price alone does not identify the current marginal cap. Re-spending can change the bank or the location/timing of emissions even under an intertemporal cap; primary PM, ammonia and other uncovered emissions remain outside these programs. A marginal spending-to-sector-to-source-to-receptor bridge and program-specific banking constraints are needed before applying a waterbed adjustment. No cap adjustment is added to the stack here. [INFERENCE, CONDITIONAL ON CAP DESIGN]

The instrument is an LLM with the project's stated immigration-related framing risks. Primary files and deterministic controls support the arithmetic; source geography, receiver assignment and valuation remain explicit assumptions in both directions.

### Checks, acquisition failures and run log

- Original producer outputs preserved. Original rounded low/central/high values match exactly after their documented four-decimal serialization; the current row-4 control matches within 1e-9bn. National/PUMA weights are conserved to 1e-5 persons, all-grid death closure to 1e-8 deaths and dollar closure to 1e-6bn. No pre-existing gate or tolerance changed.
- Acquisition catalog: CDC urllib 403 was repaired by curl to the identical primary URL; Regulations.gov 403 was repaired by the canonical GovInfo FR-document PDF. CAMPD's API 403 remains a data-access gap, never a numerical zero. Initial JSON NumPy scalar serialization was corrected to native scalars. A candidate nonnegative-replicate check was corrected to Census's explicitly signed variance-weight definition; primary weights retain their nonnegative check.
- 2026-10-14 12:56 UTC (`date`) — task stub created; mandatory case docs read.
- 2026-10-14 13:05 UTC — first primary mortality computation complete; baseline receiver correction exceeds the review bar.
- 2026-10-14 13:11 UTC — matched-current-source-frame control added after tracing `reeval.py`; all historical outputs retained.
- 2026-10-14 13:17 UTC (`date`) — six regression checks pass. Python `perf_counter`/`resource.getrusage` measured the warm full producer at 21.15s and 2,019,278,848 bytes peak RSS; cold cube build was about one minute, below 2.5GB. Timings append only to ignored `_cache/mortality_timings.jsonl`, never to deterministic outputs.
- Final six-command lane rerun: **IDENTICAL: 20/20**, exit **0**, including the original CE and air producers, new source/PM producers, cap probe receipt and six regression tests. No `--allow-unrun` exceptions. The rerun's PM build took 11.87s and 2,013,069,312 bytes peak RSS.

Reproduce (run from repo root; the final byte-rerun result is recorded in the task handoff):

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/air_pollution_2026_09_28/mortality_sources.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/air_pollution_2026_09_28/mortality_items.py
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/air_pollution_2026_09_28/test_mortality_items.py -q
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/air_pollution_2026_09_28 "uv run --no-project python3 {lane}/ce_energy.py" "uv run --no-project python3 {lane}/air_items.py" "uv run --no-project python3 {lane}/mortality_sources.py" "uv run --no-project python3 {lane}/cap_probe.py" "uv run --no-project python3 {lane}/mortality_items.py" "uv run --no-project python3 -m pytest {lane}/test_mortality_items.py -q"
```

Files covered: only this lane's new mortality/cap producer, source pins, positive-control consumer snapshot, tests and derived mortality/cap outputs; append-only revision to this RESULT. Skipped deliberately: the frozen main case, parent integration producers, re-spending, crashes, volunteering, CO2, city-size tax computation and all other peer-owned paths. The parent owns their combined stack and review/commit.
