**Verdict:** Deliver conditional item-18 arms; **withhold the complete central item**. The joint state-law food/SNAP proxy raises v8 net cost by **$0.263314888bn at both ends**, versus an isolated grocery effect of $0.259561619bn and SNAP effect of $0.190408891bn. A **crosscheck-only** national business-sales assumption plus the conditional BEA customs bridge gives **+$12.057795774bn**; adding the joint household basket gives **+$12.211045038bn**. None is a measured national business correction. The current-law companion is also partial: its old broad break-even claim is not certified on the full law or v8 frame. [CALCULATION: `derived/evaluation.json`, `derived/companion_summary.json`] [INFERENCE]

## Measurement and sign

Perspective: annual fiscal cost for other US residents when the lineage is absent, under the adopted v8 removal rules; positive deltas raise cost attributed to presence. All item-18 amounts below are income-year-2024 account dollars. The accounting set and cash set differ in retirement timing; these receipt arms move both identically. Per-member figures divide by **45,230,062.30075857**, `meta.population_v8.with_coverage`. These are modeled attribution changes, not observed removal outcomes. [DATA: `derived/case_snapshot.json`; CALCULATION]

| Explicit arm | Set low change, $bn | Set high | Cash low | Cash high | Change per member, $ |
|---|---:|---:|---:|---:|---:|
| v8 unchanged | 0 | 0 | 0 | 0 | 0 |
| Grocery only, state-law proxy | +0.259561619 | +0.259561619 | +0.259561619 | +0.259561619 | +5.739 |
| SNAP only | +0.190408891 | +0.190408891 | +0.190408891 | +0.190408891 | +4.210 |
| Joint grocery/SNAP | +0.263314888 | +0.263314888 | +0.263314888 | +0.263314888 | +5.822 |
| Business sales: 41.8% crosscheck at item6 aggregate job key | +12.291257388 | +12.291257388 | +12.291257388 | +12.291257388 | +271.750 |
| BEA proportional customs; unresolved uses retain old key | −0.233461615 | −0.233461615 | −0.233461615 | −0.233461615 | −5.162 |
| Customs; unresolved purchaser response/key = 0 | +0.938013542 | +0.938013542 | +0.938013542 | +0.938013542 | +20.739 |
| Customs; unresolved purchaser response/key = 1 | −12.125218779 | −12.125218779 | −12.125218779 | −12.125218779 | −268.079 |
| Conditional business sales + customs | +12.057795774 | +12.057795774 | +12.057795774 | +12.057795774 | +266.588 |
| Conditional business + joint household basket | +12.211045038 | +12.211045038 | +12.211045038 | +12.211045038 | +269.976 |

[CALCULATION: `evaluate.cjs` → `derived/evaluation.csv`; every arm re-evaluates all 32 personal specifications in both fill-in methods and both sets. Ends remain 16/11.]

The conditional joint arm gives set **$378.002975294–468.192829627bn**, cash **$293.963608714–384.153463048bn**. The full central item has **null**, not zero, deltas. Customs' zero/one rows are logical bounds on the **unkeyed purchaser contribution conditional on the other customs assumptions**; they are not a confidence interval or unconditional full-item bounds. The aggregate business-sales crosscheck is not substituted into any missing state as a measurement. [CALCULATION / SCOPE]

## Business purchases: what is sourced and what remains missing

The primary Texas January-2025 report, Table 1 printed p51, forecasts FY2027 business limited-sales/use receipts of $22,727.0m/$54,835.6m (**41.445703%**), including $3,541.5m mining. Its 2023 predecessor forecasts FY2025 at **41.811775%**. Minnesota's March-2026 report Table 1-2 printed p10 estimates CY2023 **state** general-sales business share **48.0%**; its local-sales row includes selective/lodging taxes and cannot be combined into a matched general-sales share. These are dated government model estimates, not observed 2024 payer records. All 51 state/DC central-2024 entries remain null with explicit missingness. [SOURCE: [Texas 2025](https://comptroller.texas.gov/transparency/reports/tax-exemptions-and-incidence/2025/96-463.pdf), [Texas 2023](https://comptroller.texas.gov/transparency/reports/tax-exemptions-and-incidence/2023/96-463.pdf), [Minnesota 2026](https://www.revenue.state.mn.us/sites/default/files/2026-03/2026-tax-incidence-study-final-cover.pdf); DATA: `inputs/business_bridge.json`; hashes and source-row checks in `business_bases.py`]

COST/EY's FY2024 $245.3bn/41.8% business-sales estimate enters **only the named crosscheck arm**, as permitted by the brief. That arm transports item6's aggregate other-production-tax industry/state mix to business sales. It does not measure purchasers' actual industry/state mix. [SOURCE: [COST/EY FY2024, printed p2](https://www.cost.org/globalassets/cost/state-tax-resources-pdf-pages/cost-studies-articles-reports/2511-10951-cs-50-state-report-final.pdf); ASSUMPTION: `assemble.py`]

Primary BEA 2024 supply MDTY gives **$83.587bn** import duties. Allocating these proportionally to positive domestic use **within summary commodity**, excluding direct exports/inventory changes, gives PCE **46.216856%**, intermediate purchases **38.980137%** (including housing), and investment/government final demand **14.803007%**. Intermediate inputs used by exporters stay included. This is a modeled bridge, not observed buyer duties: [BEA explicitly imputes commodity imports by purchaser](https://www.bea.gov/help/faq/453). Mining responds at zero. The HS housing purchaser lacks a wage key; its **0.103072%** share is separately unresolved. Combined unkeyed uses are **14.906079%**. [SOURCE: [BEA supply/use](https://apps.bea.gov/industry/release/zip/SUPPLY-USE.zip); CALCULATION: `business_bases.py`, `assemble.py`; DATA: `inputs/business_bridge.json`]

The customs producer component uses item6's actual industry wage shares, its union normalization and its G3+/white latent wage parts. State composition is transported nationally; no state-purchaser observation is claimed. BEA TOP's **$1,015.461bn** combines sales/excise/other product taxes and cannot supply an excise-only purchaser vector. **The excise business correction is unmeasured and held**, never estimated as zero. Collection totals on every receipt line remain fixed. [CALCULATION / ASSUMPTION; SOURCE: [BEA product-tax definition](https://apps.bea.gov/scb/issues/2018/08-august/0818-industry-economic-accounts-preview.htm)]

## Food and SNAP: one joint basket

The [BLS Interview questionnaire break](https://www.bls.gov/cex/pumd/errata/errata-2023.htm) means 2024 Interview groceries include nonfood. `TFOODHOP/C` are trip groceries, not ordinary food at home. The model therefore calibrates Interview grocery rank shape to BLS's **published 2024 food-at-home decile totals**, with bottom-decile pooling as in the adopted saving curve. It reproduces the adopted `both_corridor_net_h2` saving/remittance pool, then gates the CPS original union on **39,712,493.331** row4 weights. Exact observed item10 IDs enter a separate completed-union basket. [DATA: existing CE ZIP/dictionary/published tables; `derived/household_meta.json`, `household_ce_deciles.csv`; CALCULATION: `household.py`]

For consumption C, food F, SNAP S and state grocery exemption fraction e, the joint taxable basket is **C − eF − (1−e)S**, with SNAP capped at imputed food. It is not the sum of the isolated SNAP and grocery subtractions. The cap binds on **$7.095467bn nationally**, so this is a model limitation; observed benefit dollars are not all measured redeemed purchases. State-law rate ratios cover the 2024 grocery schedule; county/city levies and candy/hot-food exceptions remain unmeasured. The nationwide original-union joint factor is 0.992288; the collection-weighted completed-union correction used by this arm is **0.995813132**. Their denominators differ. [SOURCE: [7 USC 2013(a)](https://www.govinfo.gov/content/pkg/USCODE-2024-title7/html/USCODE-2024-title7-chap51-sec2013.htm); DATA: `inputs/grocery_state_2024.csv`, `inputs/household_*receipt*.json`; CALCULATION]

Each state's 2024 Census T09 collection pool stays fixed, rescaled to the case's unchanged national line; the member **and nonmember** taxable denominators are recomputed. The new ratio is a relative basket correction to the adopted line, not a replacement estimate of its level. Latent/missed-person price ratios are transported, not observed. `ce_rank` SNAP factors are supplied as a sensitivity and gated against being silently omitted. The small proxy result does not verify a $3–6bn grocery correction; missing local, product, household and purchaser detail prevents ruling out a different complete correction. [DATA: `derived/state_collection_weights.csv`, `household_state_factors.csv`, `item.json`; CALCULATION / INFERENCE]

## Case declaration and interactions

`item.cjs.registry()` returns item `consumption_tax_bases`, kind `post_engine`, with explicit arms and `build(ctx, arm, which)`. Default/unknown central calls fail `[BLOCKED]`. `build` returns actual receipt cell edits in every scenario/allocation, signed item10 reporter-carrier edits, parts pointing to each edit, and `meta.consumption_tax_bases.by_end` with coverage deltas by source line/generation. `editsAt(model)` is supplied for the parent's dynamic composition. `derived/item_payloads.json` materializes each arm for both sets. The parent must add the new metadata's by-end total after the existing v8 `evaluateFull`, as `evaluate.cjs` does; v8 itself is never edited or rebuilt. [CODE: `item.cjs`, `evaluate.cjs`]

- **Item9:** domestic-source corporate correction held. No consumption-tax receipt is added to corporate tax or the production module a second time.
- **Item10:** every parent receipt scenario and its signed reporter carriers move together; observed native-child consumption receipts are already in the affected parent cells. These arms transport one relative basket/producer ratio rather than claiming child-specific purchases.
- **Item11:** **held explicitly**. The full mixed-unit consumption response has not been repriced by taxable basket. Its unidentified new delta is null in output; held cost is not evidence of zero interaction. A complete adopted item must replace M5 on a single joint mixed-unit basket.
- **Item12:** receipt source parts are repriced by matching line ratio, separately at each end/set/generation; the remaining coverage costs are held. This is a disclosed proportional price transport, not a new missed-person basket measurement.
- **Round5 W14:** changing omitted-person tenure can change taxable baskets and source prices, so these conditional arms cannot be flat-added to a tenure correction. Recompute their joint bridge before adoption. **W16** has a future-law/year counterfactual and stays separate.

[CALCULATION / ASSUMPTION: `derived/item.json`, `item_payloads.json`, `evaluation.json`]

## Separate post-2024-law companion

Replacement lead: **The priced individual-tax and eligibility subset approximately balances on its legacy v5 frame. Full current-law net effects in FY2028 for the 45.23M v8 lineage remain unidentified.** [DATA: upstream companion summaries; INFERENCE]

Treasury Table4 FY2025 actual customs **$194.865739873bn**, versus FY2024 **$77.036909945bn**, bridge by replacing prior October–December with current October–December to calendar cash **$264.044068431bn** and **$78.917019985bn**. BEA September-30 vintage calendar NIPA is **$268.663bn** and **$83.587bn**. The NIPA-minus-cash residual is measured, not identified wholly as accrual. On the unchanged v8 household customs key, the CPI-adjusted historical sensitivity is **−$16.934117151bn**, both ends/sets, **−$374.400 per member**; it is **not FY2028 tariff policy**. [SOURCE: Treasury MTS Table4 and BEA Table3.2, URLs/hashes in `inputs/companion_sources.json`; CALCULATION: `derived/companion_bridge.json`, `companion_rows.csv`]

The primary legal ledger records IEEPA's rejection, refunds and reviewed Section122/232/301/338 instruments, together with incomplete later-amendment/court/HTS coverage. [BEA FAQ1488](https://www.bea.gov/index.php/help/faq/1488) records the one-time IEEPA refunds as a **$166bn 2026Q1 capital transfer**, with interest separate; this is not a recurring FY2028 customs subtraction. A FY2025 receipt carry-forward is not certified. [SOURCE: linked primary acts/opinions and anchors in `inputs/companion_legal.json`]

JCT FY2028 national scores are **−$57.507bn** bonus depreciation and **−$13.794bn** domestic R&E. Allocating the complete scores conditionally on item6's evaluated domestic corporate shares, in 2024 prices, gives cost **+$4.232590296bn low / +$1.566058410bn high**, or **+$93.579 / +$34.624 per member**, equal in both sets. These scores compare January2025 law, not frozen2024 law, and include pass-through effects not separately identified here. They cannot be promoted into a complete companion or summed with the historical customs sensitivity. Legacy individual/benefit rows have not been rerun on v8 tax units/eligibility. `companion.py --require-full` exits2 rather than fabricate a total. [SOURCE: CBO61570/JCT enacted-law workbook, cells in `derived/companion_summary.json`; [IRS bonus depreciation](https://www.irs.gov/publications/p946), [IRS section174A](https://www.irs.gov/irb/2025-38_IRB); CALCULATION]

## Validation and run log

Reproduce from repo root:

```sh
sh infra/immigration-fiscal/consumption_tax_bases_r5_2026_10_15/run_all.sh
uv run --no-project python3 -m pytest infra/immigration-fiscal/consumption_tax_bases_r5_2026_10_15 -q
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/consumption_tax_bases_r5_2026_10_15 \
  'sh {lane}/run_all.sh' \
  'uv run --no-project python3 -m pytest {lane}/test_business_bases.py {lane}/test_household.py {lane}/test_companion.py {lane}/test_item.py -q -o cache_dir={lane}/_cache/pytest'
```

- 2026-10-15T02:23:08Z: first source-case unchanged gate passes. Python wrapper measured 8.41s; child peak318MB. Set **365.791930255/455.981784589**, cash **281.752563676/371.942418010** (1e-6bn gate); 16/11 independently in both methods. [CALCULATION]
- 2026-10-15T02:27:41Z: initial integration rejects missing BEA `HS` purchaser. Repaired as explicitly unkeyed housing with positive mass, fail-loud mapping guard and regression check; no silent zero. [CODE: `failure-catalog.md`]
- 2026-10-15T02:32:44Z–02:33:30Z: full six-command rebuild exit0. Snapshot9.47s/325MB; business2.71s/58MB; household13.23s/427MB; companion10.51s/362MB; assembly2.72s/144MB; evaluator6.43s/355MB. All measurements use `time.perf_counter` and `resource.getrusage`; memory is per process, not concurrent sum. Source snapshots are below the10GB download cap. [CALCULATION: ignored `_cache/timings.jsonl`]
- Code review found no critical defect; confirmed CE sensitivity selector mismatch was fixed and a presence gate added. Review scope excludes comprehensive legal certification and independent reconstruction of every state law. [REVIEW: scratch `L3a-review.md`]
- Final validation: **26 tests pass**; all nine Python files compile; all39 deliverable files are LF; the complete `rerun_lane.py` ends **IDENTICAL: 39/39**, **exit0**, with all four test modules explicitly named. Its preceding directory-pytest invocation compared39/39 but exited3 for static coverage; the corrected command clears that gate without exemptions. No Git writes, upstream lane changes, headline adoption or publication. [CALCULATION / SCOPE]

LLM-assisted analysis can inherit directional framing bias. Source tables, symmetric cost/receipt signs, unchanged-case controls, explicit nulls and counterexamples constrain implementation error; they do not identify the removal counterfactual or eliminate model bias. [INFERENCE; project `notes/llm-bias-caveat.md`]
