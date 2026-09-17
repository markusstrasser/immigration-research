**Verdict:** Adding public institutional costs cannot flip any headline sign. Across both arms and both references the age-matched gap for Mexican-origin groups moves by at most $5.3bn against stored gaps of −$290.6bn and −$215.0bn, and by at most $467 per standardized person against −$5,795 and −$4,289. The +$50.2bn absolute partial balance falls to roughly +$30–32bn once the target groups' own institutional cost ($18.4–19.8bn) is charged, and would need a per-institutionalized-person cost of about $155,000–167,000 per year to reach zero.

## Gate 1 — replication of the stored institutional count

| Quantity | Value |
|---|---|
| Stored `institutional`, 2024 `Mexican / native` row, `acs_institutional_2026_09_16/acs_institutional_rates.csv` | 107,917 |
| Fresh pull, `SEX=1&AGEP=18:39&NATIVITY=1&HISP=02&TYPEHUGQ=2`, ACS 2024 1-year PUMS | 107,917 |
| Result | **PASS**, exact |

Recorded in `derived/audit.json` as `gate1_stored_acs_institutional_2026_09_16`, `gate1_fresh_pull`, `gate1_pass`.

Two further executed gates: the pooled `mexican_total` cells equal the sum of their parts in every band, and the self-reference delta (white group against itself) is exactly 0.

## Cost parameters

All figures were fetched in this lane on 2026-09-17. None are recalled.

| Parameter | Value | Source | URL |
|---|---|---|---|
| Annual state spending per prisoner (median state, 2023) | $60,989 | USAFacts, compiled from Bureau of Justice Statistics and Census Bureau corrections expenditure data; same page gives $63.6bn total state prison spending and just over 1 million incarcerated as of December 2023 | https://usafacts.org/articles/how-much-do-states-spend-on-prisons/ |
| Annual cost per jail inmate (35 responding jurisdictions) | $47,057 | Vera Institute, *The Price of Jails* | https://www.vera.org/publications/the-price-of-jails-measuring-the-taxpayer-cost-of-local-incarceration |
| Institutional long-term care spending, 2023 | $147bn, of which Medicaid paid 44% | KFF, *5 Key Facts About Nursing Facilities and Medicaid* | https://www.kff.org/medicaid/5-key-facts-about-nursing-facilities-and-medicaid/ |
| Nursing facility residents, July 2024 | 1.2 million | KFF, same page | https://www.kff.org/medicaid/5-key-facts-about-nursing-facilities-and-medicaid/ |
| Primary payer of certified nursing facility residents, 2025 | Medicaid 63%, Medicare 14%, private/other 23% | KFF State Health Facts, analysis of CASPER data | https://www.kff.org/state-health-policy-data/state-indicator/distribution-of-certified-nursing-facilities-by-primary-payer-source/ |
| Nursing care facilities and CCRC national spending, 2024 | $219.9bn (+7.3%) | CMS, *National Health Expenditures 2024 Highlights* | https://www.cms.gov/files/document/highlights.pdf |

Derived nursing parameter used in the headline arms: total cost per resident-year = $147bn / 1.2m = **$122,500**; public share = Medicaid 63% + Medicare 14% = **77%** of residents; public cost per institutionalized person 65+ = **$94,325** per year.

The public share is taken from the payer mix of *residents*, not of *dollars*. A dollar-share alternative, Medicaid's 44% of institutional long-term care spending, gives $53,900 and is reported as the `*_nf_medicaid_only` arms in the output. That alternative is Medicaid-only and excludes Medicare-covered skilled nursing, so it is a floor. CMS's published highlights give the nursing-facility total but no payer split, so the payer split rests on KFF rather than on a CMS table.

The jail figure was sourced but is **not** used in the headline arms: it is older, covers 35 jurisdictions rather than the nation, and is lower than the prison figure, so using the prison figure everywhere is the more adverse choice. The CMS 2024 nursing total is reported for context; the per-resident calculation uses the KFF 2023 institutional long-term care figure because it matches the resident denominator.

## Arms

For group `g` and band `b`, with `N` the total ACS population in the band (all `TYPEHUGQ` values) and `I` the institutional count (`TYPEHUGQ=2`):

- `adverse` — every institutionalized person under 65 is charged the prison figure, $60,989. This over-charges ICE detention, mental facilities and juvenile facilities, all of which fall disproportionately on the foreign-born, so it is adverse to the Mexico-born group. Every institutionalized person 65+ is charged $94,325.
- `moderate` — under 65, the prison figure times the band's male share of the institutional population, so women's institutional presence proxies non-correctional facilities. 65+ unchanged.
- `adverse_nf_medicaid_only`, `moderate_nf_medicaid_only` — the same two arms with the $53,900 Medicaid-only nursing parameter.

`C_gb = I_gb × cost_b`. Age-matched change versus reference `r`: `Δ_r = −Σ_b [C_gb − (N_gb/N_rb) C_rb]`. Per standardized person: `−Σ_b s_b [C_gb/N_gb − C_rb/N_rb]`, with `s` the native non-Hispanic white ACS age shares. A positive Δ means the omission was working *against* the Mexican-origin group, so including it improves the balance.

## Results

Headline arms, in $bn and $ per standardized person. Full output including the Medicaid-only sensitivity is in `derived/institutional_bound.csv`.

| Arm | Target | Own institutional cost ($bn) | Δ gap vs native NH white ($bn) | Δ per std. person vs white | Δ gap vs all natives ($bn) | Δ per std. person vs all natives |
|---|---|---|---|---|---|---|
| adverse | Mexico-born | 5.88 | +1.93 | +275 | +4.81 | +467 |
| adverse | US-born Mexican | 13.91 | −4.04 | −75 | +0.44 | +117 |
| adverse | Mexican total | 19.79 | −2.11 | +109 | +5.25 | +301 |
| moderate | Mexico-born | 5.66 | +1.26 | +235 | +3.98 | +417 |
| moderate | US-born Mexican | 12.69 | −4.14 | −74 | +0.11 | +108 |
| moderate | Mexican total | 18.35 | −2.88 | +89 | +4.09 | +271 |

The Medicaid-only nursing arms move the same quantities to between −$4.40bn and +$4.07bn and between −$159 and +$335 per standardized person.

Institutional rates per 1,000, with the male share of the institutional population and the white age shares used as the standard, are in `derived/institutional_rates.csv`. The pattern that drives the signs: Mexican-origin institutionalization is higher than the white reference in the working ages (for example 14.7 versus 9.8 per 1,000 at 35–44 for the pooled Mexican total) and much lower at 75+ (22.8 versus 41.9 per 1,000). Against all natives the working-age excess largely disappears (15.6 per 1,000 at 35–44), leaving the 75+ deficit, which is why every Δ against all natives is positive or near zero.

## Can the bound flip a sign

| Comparison | Stored value | Largest institutional move | Verdict |
|---|---|---|---|
| Age-matched gap vs third-plus NH white | −$290.6bn | −$4.4bn to +$1.9bn (Mexican total: −$2.9 to −$2.1bn) | No flip; the cost parameters would have to rise about 100 to 140 fold, and in that direction the gap only deepens |
| Age-matched gap vs all natives | −$215.0bn | +$0.11bn to +$5.25bn | No flip; a flip needs about a 41 fold increase |
| Standardized gap per person vs white | −$5,795 | −$159 to +$275 | No flip |
| Standardized gap per person vs all natives | −$4,289 | +$43 to +$467 | No flip |
| Absolute partial balance | +$50.2bn | Target-group institutional cost $16.6bn to $19.8bn | No flip; the balance falls to about +$30bn to +$34bn. Zero requires a 2.5 to 2.7 fold cost increase, about $155,000 to $167,000 per institutionalized person-year, above every nationwide figure sourced here and matched only by a few of the most expensive individual state prison systems |

Multipliers are in `derived/audit.json` under `signflip_cost_multiplier_needed_for_age_matched_gap` and `signflip_cost_multiplier_needed_for_absolute_50_2bn`. A negative multiplier there means the institutional charge pushes that gap further negative at any cost level, so no flip is reachable in that direction.

## Scope differences that qualify the comparison

These numbers bound an omission; they are not a drop-in adjustment to the ledger.

1. The ACS `NATIVITY=1&HISP=02` group pools second and third-plus generations, because the ACS has no parental birthplace. The CPS ledger separates `mexican_second_gen` from `mexican_third_plus_selfid`. Only the pooled `mexican_total` here is comparable in scope to `mexican_observed_total` there.
2. The ACS reference is **all** native non-Hispanic whites. The ledger's reference is **third-plus** non-Hispanic white. The two are not the same population and the Δ against the ACS white group is applied to a gap defined against a narrower one.
3. `TYPEHUGQ=2` is all institutional group quarters: correctional, nursing, mental and juvenile facilities, and since 2010 it includes ICE detention, which biases the Mexico-born institutional count upward.
4. The ledger covers the civilian household population and uses CPS ASEC 2025 with income year 2024; this lane uses ACS 2024 one-year PUMS. The two surveys are not linked, and no sampling variance is propagated here. The Δ figures carry no standard errors.
5. The charge is an average operating cost per institutionalized person-year, not a marginal cost and not an observed expenditure attributable to these individuals. Institutionalized people also drop out of the household account entirely, so the true net effect includes the taxes and benefits they would otherwise have registered; that offset is not estimated here and would work in the direction of smaller Δ.
6. Self-identified Mexican origin in the ACS and CPS-native-with-Mexico-born-parent are different constructs; the ledger's own README already notes the self-ID qualification.

[UNVERIFIED] The 1.2 million resident denominator (July 2024) and the $147bn spending figure (2023) come from different reference dates on the same KFF page, and the resident payer mix is 2025. The resulting per-resident cost is therefore approximate to within a few percent, which is immaterial at the resolution of this bound.

## Files

Covered: `derived/acs_cells.csv` (192 weighted cells, 4 groups × 8 bands × 2 sexes × 3 GQ types), `derived/institutional_bound.csv` (24 rows, 4 arms × 3 targets × 2 references), `derived/institutional_rates.csv`, `derived/audit.json`, `derived/gate_raw.json`, raw API JSON under `_cache/` (33 responses, gitignored).

Read but not modified: `all_age_ledger_2026_09_17/README.md` and its `derived/estimates.csv`, `acs_institutional_2026_09_16/pull_and_compute.py` and `acs_institutional_rates.csv`, `acquire/config.local.env` (key only).

Skipped and why:
- **Three target groups.** The brief asks for three; the ACS supports only two, because it cannot separate second from third-plus generation. The third reported row is the pooled Mexican total, which is the sum asked for and the scope match to `mexican_observed_total`.
- **State-level tabulations.** Not needed; the bound is national. The PUMS `tabulate` endpoint has no ST dimension, as the brief noted.
- **A separate jail cost arm.** The jail figure is sourced above but is lower and older than the prison figure, so it would only shrink the bound.
- **Sampling variance on Δ.** No replicate weights were pulled; the endpoint returns point estimates only. This is a deterministic bound, not an interval.
- **No commits.** As instructed.
