**Verdict:** Only the arrest-footed high victim scenario clears the $5bn review bar (+$10.63bn before matching the new mixed-offender/VSL conventions). Geographic transfer and state custody reassignment are below it. ICE overlap is bounded only under explicitly matched-stock assumptions; it is not identified within annual ACS. These four checks change no adopted producer.

Coverage: brief item 7(a)–(d); custody/crime measurement rule, detention spending reconciliation, CJ allocator and victim-model callers. No git writes or edits outside assigned `report_checks*` files.

Inputs are pinned in `inputs/report_checks_pins.json`; the one new primary input is the ACS 2024 state × nativity × origin × institutional table. Other primary inputs already existed locally. [CALCULATION: report_checks.py → derived/report_checks*; report_checks_fiscal.cjs → derived/report_checks_fiscal.json]

## 7(a): geography and the active caller

| Residential geography, ACS 2020–2024 B03001 tracts | Hispanic share at average Mexican-origin resident's tract | Mexican share among that resident's Hispanic neighbors |
|---|---:|---:|
| National | 49.136% | 78.618% |
| Texas | 60.326% | 84.180% |
| Arizona | 50.877% | 87.677% |
| Texas + Arizona | 58.716% | 84.775% |

[SOURCE: Census 2024 ACS5 B03001, 51 primary tract JSONs, pinned by state; DATA: derived/report_checks_geography.csv. Population weighted by Mexican-origin residents, not an unweighted average of tracts.]

The active low victim arm takes NCVS incidents and moves the share `theta=0.497673` of mixed-offender incident excess to Hispanic attribution. That share is the mean Hispanic fraction of **mixed Hispanic/non-Hispanic offender groups**, drawn from central TX/AZ NIBRS agencies. It is neither the Hispanic victim share nor the general Hispanic population share. Its national transfer is unidentified. [DATA: crime_ratio_direction_2026_09_24/derived/nibrs_mixed_group_hispanic_fraction.csv; SOURCE: dollar_effects.py:89–119,132–142 and population_basis_2026_09_29/basis.py:115–121.]

[ASSUMPTION] Preserve the mixed-group log-odds enrichment relative to tract Hispanic exposure: `logit(theta_US)=logit(theta_TXAZ)+logit(exposure_US)-logit(exposure_TXAZ)`. This yields 0.402245. At original Miller prices, the row4 victim change is **−$0.379bn low / −$0.424bn high** (high uses the held 1.118080 institutional proxy). This is a sensitivity, not a correction supported by victim-offender linkage. The full feasible theta 0–1 change is **−$1.976 to +$1.994bn low / −$2.209 to +$2.230bn high**: the mixed-offender correction alone cannot clear $5bn. [CALCULATION: derived/report_checks_victims.json.]

The separate NIBRS victim-model alternative already transfers observed TX/AZ Hispanic victim shares nationally through tract exposure. Keeping its national-transfer shares rather than raw TX/AZ shares changes its victims by **+$2.585bn row4**, below $5bn. It is a disconfirmation/context check, not an omitted correction in the adopted NCVS mixed arm. The Mexican-neighbor coefficient differs by 6.158 percentage points: changing only that coefficient from US to pooled TX/AZ changes the original NCVS central victim value by **−$1.552bn row4**, also conditional. These quantities answer different questions and must not be added. [SOURCE: offender_ethnicity_nibrs_2026_09_23/nibrs_rates.py:460–529, victim_cost_rerun.py:15–18; DATA: derived/report_checks_victims.json.]

## 7(b): state-level generic-Hispanic institutional reassignment

Apply the existing allocator's rule inside each state and nativity: generic-Hispanic institutional excess over that state/nativity's all-origin institutional rate, allocated to named Hispanic origins by their population share. Sum the reassigned Mexican counts, then apply the existing national CPS nativity transport and national institutional denominator. This changes only the location at which the generic-origin correction is computed; it does **not** identify prisons or ordinary offending. [SOURCE: cj_use_allocation_2026_09_23/allocate.py:163–205; DATA: inputs/report_checks_acs1_2024_state1864.json.]

The adjusted Mexican share of Hispanic institutions moves **0.653493 → 0.642519**, and the transported custody share moves **0.141918 → 0.139555**. The national institutional total (2,121,482, ages 18–64 both sexes) closes exactly across states; raw Mexican counts are conserved. The all-state national reassignment reproduces the existing key exactly. [CALCULATION: derived/report_checks_state_reallocation.csv, derived/report_checks_custody.json.]

| Change only from current v7 personal ends 16 / 11 | Low fiscal change | High fiscal change | Changed fiscal endpoints |
|---|---:|---:|---:|
| State custody reassignment, prisons only | −$0.319bn | −$0.321bn | $339.233 / 423.329bn |
| Also transport the changed origin coefficient to arrest-keyed police/courts | −$0.723bn | −$0.728bn | $338.829 / 422.921bn |

Both keep the added descendants at their current keyed amounts: the absolute union-only change is identical on the 39.71M union and 42.75M lineage, and the per-lineage-member changes are correspondingly smaller. Both include the same account's union state-price correction using the row4 index and held state-price gap per service unit. Police holds its half-arrest/half-population key; courts hold 60% criminal/40% population. Every receipt and every unrelated spending line is byte-equivalent in memory; changed keys conserve national amounts. Both sides remain below $5bn. [CALCULATION: report_checks_fiscal.cjs → derived/report_checks_fiscal.json; ASSUMPTION: descendants and state service prices held.]

[GAP] Public tabulation lacks replicate weights, so no state-reallocation sampling SE is manufactured. This is not a state-priced correctional-only resident count. Computing that requires institution type and matched service prices.

## 7(c): ICE contract overlap envelope

Primary ICE records give **37,684 all-ICE detainees at FY2024 year-end**, **37,721.8 FY2024 average daily population**, and **5,089 Mexican nationals at year-end**. All-ICE stock is 1.776% of the ACS 18–64 institutional total; Mexican-national stock is 1.818% of the adjusted Mexican-origin institutional count (279,850.6). These percentages are cross-source diagnostics, not matched corrections. [SOURCE: ICE FY2024 workbook `Detention FY24`, ICE FY2024 annual report country-of-citizenship detained table; pinned URLs/hashes; CALCULATION: derived/report_checks_ice.json.]

For a **single date with complete matched ICE coverage**, contract detainees are a subset of all ICE detainees, so overlap with ACS institutions lies between zero and the smaller of the institution count and 37,684. The matched Mexican-national contract subset cannot exceed 5,089. This cannot be transferred unchanged to an annual ACS survey stock: year/date, geography, ages, nationality versus origin, household frame and coverage must align. The facility workbook also excludes several facility categories and lists facilities having population at its extraction; its contract-bed detail does not identify origin/age overlap in ACS. [MEASUREMENT; SOURCE: custody rule:40–45 and workbook `Facilities EOFY24` header.]

Under an intentionally generous **full year-end overlap stress test**, subtracting the full ICE total from the national institutional denominator and the Mexico-national count from the adjusted foreign-born Mexican numerator changes the raw prison-key amount by **−$0.0188bn**. Extreme assignments of all ICE stock to Mexican-origin numerator versus none yield **−$2.133 / +$0.311bn**. Those are modeled stock stresses, not statutory costs, corrected crime rates, statistical confidence bounds or inferred matched annual overlaps. No victim harm is assigned to ICE detention. [ASSUMPTION; CALCULATION: derived/report_checks_ice.json.]

[GAP] Contract-only origin × age × person-time overlap with ACS institutional residence is not identified by the public fields examined. Civil detention spending stays within its fiscal ledger boundary regardless of the offending interpretation. Existing all-vintage detention reconciliation was reused; no broad account re-acquisition occurred.

## 7(d): high victim footing

The high arm explicitly takes the **1.118080 ACS institutional-residence ratio for men 18–39** (Mexican versus specifically named Hispanic origins) as a multiplicative scale on the group's offending. ACS `TYPEHUGQ` does not distinguish prison, civil ICE detention or other institutions. It is a conditional institutional proxy scenario; calling it a measured ordinary-offending ratio violates the measurement rule. [SOURCE: victim_cost.py:304–313,324,527–528; custody rule:13,32–55; population_basis/basis.py:123–128.]

Beside: the existing **FBI 2019 adult-arrest ethnicity-share** arm prices $43.119943bn on published CPS weights, **$42.500518bn row4**, versus the custody-only arm's $32.338107bn published / **$31.873565bn row4**: **+$10.626953bn**. This clears $5bn and changes the footing claim. It applies offence-specific Hispanic adult-arrest shares to 2024 NCVS national victimisations, retains NCVS victim distribution, sets within-Hispanic Mexican-origin offending ratio to one and keeps homicide on the same WONDER/SHR inputs. Arrests remain enforcement/charging/panel proxies, not incidents or convictions; FBI rape and other-assault categories differ from NCVS rape/sexual assault and simple assault. [SOURCE: victim_cost.py:283–301; CALCULATION: derived/report_checks_victims.json.]

These are **beside values at the original Miller prices and without the mixed-offender addition**. The parent must match its chosen active victim/VSL/mixed convention through the sibling's API before including arrest victims and reconciled fear in a pairing or stacked span. This report does not add the institutional multiplier to the arrest-based arm, because no arrest source identifies that Mexican/Hispanic institutional-to-offending transport. [ASSUMPTION; scope boundary.]

## Checks, source coverage and reproduction

Covered: custody rule and completed detention spending audit; dataset register local source entries; all 51 ACS tract files; new 51-state/DC ACS institutional tabulation; CJ national positive controls and primary BEA/CPS checks; victim model primary price parser and central positive control; v7 personal end reproduction; national weight conservation; unchanged fiscal lines/receipts; primary input sha256 verification. Skipped: new account downloads (existing audit closes accounts), causal offending attribution (unidentified), final mixed/VSL/lineage pairing (parent owns its live integration).

Commands from repository root:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/social_costs_unpriced_2026_09_28/report_checks.py --acquire
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/social_costs_unpriced_2026_09_28/report_checks.py
node infra/immigration-fiscal/social_costs_unpriced_2026_09_28/report_checks_fiscal.cjs
```

`--acquire` pins missing inputs but rejects changed existing pins. Ordinary runs require every pin and stop on missing/stale data. Runtime/memory use Python perf_counter/getrusage: successful run 5.265 seconds, peak RSS 238,354,432 bytes. Initial Census `row+ST` failed (HTTP400); official Census microdata guide specifies `row+for&for=state:*`; the repaired query is pinned. A repeated construction of the 83,608-tract state set inside the API-cell loop was caught with faulthandler and hoisted once. Whitespace around workbook `Average` is normalized before reading its number. No source, git metadata or shared producer was modified.

LLM instrument: choices in the theta transfer and ICE overlap scenarios are explicit assumptions; labels prevent an institution count or geography association from becoming a measured offending effect.

Validation log, 2026-10-14T12:38:39Z: Python compile and Node syntax checks passed; modified primary bytes were rejected by the pin gate. `rerun_lane.py` ran the two report commands successfully (both rc0), `IDENTICAL: 56/56`; `items.py`, `p7_crime.py` and `security_inputs.py` were explicitly allow-unrun because their concurrent parent/sibling owners validate them. This covers report-only reproducibility, not those producers' new behavior.
