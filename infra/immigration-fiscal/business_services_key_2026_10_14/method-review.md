**Verdict:** No material arithmetic defect found in the narrow police/fire sensitivities or the unchanged-central recommendation. The union freight inversion is exact against its authoritative pre-road key. The lineage inversion is an **effective two-key decomposition**, not an exact recovery of the case's underlying passenger/freight demand: its added age profiles differ by line. That limitation must accompany every lineage freight arm. Zero recommended rekeying is an unresolved-resource-share default, not a finding that business service use or the correction is zero. [CALCULATION; INFERENCE]

Read-only review, 2026-10-14 20:53:43 JST (`date`). Only this file is written. Covered: `inventory.cjs`, `analyze.py`, inventory/activity/arm/line/break outputs, highway and incident evidence, spending-share inputs, frozen v4 road code, v6 added-age code, v7 added-job-capital code. Skipped: new acquisition, raw workbook re-extraction and rerunning generators (their owners supply source/closure checks); full causal re-estimation of business-serving resource fractions (unidentified in these sources).

## 1. Freight inversion: exact for union, conditional approximation for lineage

Let p be the passenger highway-cost fraction, a gasoline taxes / total excise, R the current highway capital key and E the current excise amount / its national. The solution is C = (pE − aR)/(p − a), V = (R − (1−p)C)/p. This is the correct inverse of R = pV + (1−p)C and E = aV + (1−a)C. `analyze.py:140-149` implements it correctly. The reconstruction gate alone is an algebraic identity for any R/E; it cannot establish that recovered C is the original consumption key. [CALCULATION]

For the identified union, the authoritative pre-road v4 construction does use these equations: `main_case_candidate_v4_2026_09_29/package.cjs:182-211`, especially `kRoad` at 194 and the gasoline shift at 197. An independent executable comparison obtains:

| Method | Direct pre-road consumption | Inferred from inventory | Direct passenger |
|---|---:|---:|---:|
| b_hotdeck_union_matched | 0.08182385296795937 | 0.08182385296795938 | 0.10123231345222686 |
| b_matched_over_pooled | 0.08146335903121468 | 0.08146335903121471 | 0.10123231345222686 |

[CALCULATION: node read-only probe below, exit 0; DATA: `derived/inventory.json` union highway/receipt amounts]

```javascript
const fs=require('fs'), path=require('path');
const F=path.resolve('infra/immigration-fiscal');
const P=require(path.join(F,'main_case_2026_10_14/package.cjs'));
const V4=require(path.join(F,'main_case_candidate_v4_2026_09_29/package.cjs'));
const x=JSON.parse(fs.readFileSync(path.join(F,'business_services_key_2026_10_14/derived/inventory.json')));
for(const method of P.METHODS){
 const pre=V4.modelFor('central',method,V4.withCentral({roads:V4.OFF.roads})), direct=V4.roadKeysOf(pre).personal;
 const r=x.runs.find(z=>z.method===method&&z.end==='low'), R=r.capital.find(z=>z.id==='hwy_sl').union_key, e=r.receipts.find(z=>z.id==='excise_selective_sales'), a=x.meta.roads_mileage_key.gasoline_bn/e.national_bn, p=x.meta.roads_mileage_key.passenger_share;
 console.log(method,direct,'inferredFreight',(p*e.union_amount_bn/e.national_bn-a*R)/(p-a));
}
```

The parent can gate union inferred C and V against `direct.k_cons` and `direct.s_vmt` at 1e-12. This is stronger than the current inverse/reconstruction check.

For the lineage, `main_case_2026_10_07/item_age_mix.cjs:83-88,118-125,225-234` independently re-profiles each added person's line. `added_age_mix_2026_10_07/g3_age_keys.py:164-177` gives the road correction a persons-aged-5+ profile; economic-affairs retains its own preferred-key profile and excise retains its receipt consumption profile. The capital highway key is the sum of parent economic-affairs and correction contributions (`main_case_lineage_2026_10_05/lineage_case.cjs:245-262`, capital key via evaluated amounts). These transformations do not preserve the original road/excise mixture automatically. The independent part-model probe confirmed different later/g3-rate cell amounts for economic-affairs, roads and excise. Thus the lineage's inferred C/V is a convenient effective split that reproduces its current R/E, **not observed or uniquely recovered physical passenger/goods demand**. [DATA; INFERENCE]

The unchanged-demand arm's zero change is nevertheless exact by construction: substitute its inferred C/V into the same blend and recover R. Any alternative freight-key arm holds this effective passenger piece fixed, which is an additional modeling choice. Label its lineage result `[APPROX]`, conditional on that effective split. The union freight arms need no such age-split approximation label. This issue does not change the police/fire arms or zero adopted change. [CALCULATION; ASSUMPTION]

## 2. Frozen population, lineage and stock rules

`analyze.py:111` correctly obtains the population allocation from **amount / national** on general-public-services. In the frozen inventory, its lineage amount share is 0.12614434763606788, while the inherited display `share` is 0.12741175044421638. Using the latter would be wrong. The union amount key is 0.11717537467643238; the CPS row-4 population key has another national frame (0.118352664), so the explicit main-estimate mapping of replicate deviations at 123-127 is appropriate as a conditional variance convention. [DATA: `derived/inventory.json`, `derived/activity_keys.json`; CALCULATION]

The added output factor rule at `analyze.py:68-72` matches the case's item-6 contract: added G3plus/white case wage shares, already taking their own age composition, times the relevant group's industry-output-over-wage factor. The authoritative route is `main_case_2026_10_14/item_job_capital.cjs:155-180,190-194`; inventory serializes its actual `ITEM_DETAIL.job_capital_taxes.set.wage_share` at 62. This is an assumed transferable industry profile, not a count-based flat scale. G3plus factors use the case wage-key denominator and white factors the lane plain-wage denominator, consistently with item 6. [DATA; ASSUMPTION]

Mining-fixed business keys retain the full denominator and add mining fraction times the old baseline (`analyze.py:63,72`); fixed mining is not silently assigned zero services. Highway arms replace the freight term exactly once and include consumption plus public-capital return coefficients at 155-161. Public-order safety and its state-price correction respond at 1 in the frozen case, so no missing response multiplier was found in police/fire arithmetic (`main_case_candidate_v4_2026_09_29/package.cjs:277-280`). [CALCULATION]

The safety-capital arm is a weaker extrapolation than the narrow spending arm: `analyze.py:130-138` applies the expense mix to stock, then replaces that fraction of each component's **composite public-safety key**, rather than identifying the protective-police/fire slice's own population key. The frozen union composite safety key is 0.13417132057610864, compared with population 0.11717537467643238. This is an explicit stock-average substitution assumption, not a measured protective-service decomposition. Its incremental lineage capital move is only about −$0.023bn at the low end and −$0.034bn at the high (capital proxy minus narrow incident proxy); it does not affect the $5bn verdict or central recommendation. Preserve the assumption label; do not call that stock proxy exact. [DATA: `derived/arms.csv`, `derived/inventory.json`; INFERENCE]

## 3. Delta SEs and recommendation

The narrow union police/fire SE propagates their joint output-minus-mapped-population replicate vector and therefore preserves their covariance; `analyze.py:125-127,176-180` averages vectors across the two fill-in methods before taking SDR. Combined-arm vectors also preserve covariance with goods output. The freight consumption/passenger baseline is held fixed, and the stock proxy baseline/component mix is held fixed, so the reported SEs are **conditional CPS key errors**, not full errors of the fiscal correction. Lineage SE is omitted rather than manufactured from independent quadrature (`analyze.py:180,186`). Those distinctions are substantively necessary. No incorrect variance arithmetic found under that stated conditioning. [CALCULATION]

Primary incident tables count offenses or department runs, not personnel time, marginal expenditure or capital demand (`source-evidence.md:17-27`). Highway freight is already present at demand (`highways-evidence.md:20-28`), so neither a second freight charge nor a large assumed correction follows from identifying trucks. The narrow proxy moves lineage net cost by about −$1.124bn at both ends, with the broader proxy about −$2.001bn; all executed arms remain below $5bn (`derived/arms.csv`). Retaining the central while keeping those arms beside it is justified by the absence of identified resource shares. [DATA; INFERENCE]

That does **not** falsify a larger correction in unmeasured components. The general-administration diagnostic reaches $5bn at roughly half its business share at the low lineage end and about one-third at the high; no measured national business-resource fraction resolves it (`derived/break_shares.csv`). State the unresolved gap instead of claiming every possible business-service correction is below $5bn. [DATA; INFERENCE]

## Concurrent parent correction checked

2026-10-14 20:55:21 JST (`date`): the parent added authoritative union keys at `inventory.cjs:35-36,54` and `analyze.py:150-153` gates and uses them. This matches the independent probe. The parent also added a lineage effective-split marker in output rows. One scope correction was sent: demand-side arms that **change freight cost share** (Oregon, federal-cost and truck-VMT arms) also depend on the lineage effective split. Only the unchanged `freight_demand_control` is algebraically exact. The approximation marker should cover every lineage freight arm except that unchanged control, including the alternative cost-share arms whose `freight` field is `demand`. This is a labeling boundary, not a demonstrated $5bn numerical failure. [DATA: concurrent code inspection; INFERENCE]
