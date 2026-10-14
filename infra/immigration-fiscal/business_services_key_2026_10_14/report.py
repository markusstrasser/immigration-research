#!/usr/bin/env python3
"""Render the lane's result from computed outputs. --stamp records date once."""
from pathlib import Path
import argparse
import csv
import json
import subprocess

HERE = Path(__file__).resolve().parent


def load(path):
    return json.loads((HERE / path).read_text())


def table(header, rows):
    return "| " + " | ".join(header) + " |\n|" + "|".join(["---"]*len(header)) + "|\n" + "\n".join("| "+" | ".join(map(str,row))+" |" for row in rows) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stamp", action="store_true")
    args = parser.parse_args()
    log = HERE / "inputs/report_log.json"
    if args.stamp:
        if log.exists():
            raise RuntimeError("[BLOCKED] refusing to overwrite date log")
        log.write_text(json.dumps({"rendered_at": subprocess.check_output(["date", "+%Y-%m-%d %H:%M:%S %Z"], text=True).strip()}, indent=2)+"\n")
    stamp = load("inputs/report_log.json")["rendered_at"]
    s, inv, activity = load("derived/summary.json"), load("derived/inventory.json"), load("derived/activity_keys.json")
    rows = s["rows"]
    def pair(arm,frame,field):
        return [next(r[field] for r in rows if r["arm"]==arm and r["frame"]==frame and r["end"]==e) for e in ["low","high"]]
    def show(values):
        return " / ".join(f"{v:+.3f}" for v in values)
    base = pair("unchanged_recommended","lineage","baseline_bn")
    incident = pair("incident_proxy","lineage","change_bn")
    union = pair("incident_proxy","union","change_bn")
    supply = pair("freight_goods_output","lineage","change_bn")
    body = f"""**Verdict:** Retain v7's central ({base[0]:.3f}–{base[1]:.3f}bn/year); no measured national business-serving spending/stock share was identified that justifies a central change. The narrow incident-proxy arm lowers the identified union by {abs(union[0]):.3f}bn and the lineage by {abs(incident[0]):.3f}bn at both personal endpoints, below the $5bn review bar. Freight already enters the existing road key. Its goods-output arm raises the lineage endpoints by {supply[0]:.3f}/{supply[1]:.3f}bn, conditional on an approximate effective lineage split. None of the reported one-change arms reaches $5bn; unmeasured administration/enterprise shares leave larger changes unresolved. [CALCULATION: `analyze.py` → `derived/summary.json`] [INFERENCE]

Perspective: annual net resource/fiscal cost to other residents, income year 2024, personal allocation, specifications 16/11. Negative changes reduce that cost. These are conditional modeled reallocations of the frozen account, not measured causal budget effects, migration admission effects or welfare judgments. The public-capital return is imputed and never a cash/debt flow. The instrument is an LLM; primary-file parsing, positive controls and symmetric supply/demand arms constrain interpretive drift. [FRAMING-SENSITIVE] [DATA: frozen v7 payload, `meta.allocation`, `meta.capital_return`]

## Frame and the change being tested

The identified union has {inv['frame']['union']:,.2f} members; the lineage {inv['frame']['lineage']:,.2f}. The union is the affine zero-addition intercept **at the lineage's current responses**, not a separate union-only removal with its own scale response. Its baseline is {pair('unchanged_recommended','union','baseline_bn')[0]:.3f}/{pair('unchanged_recommended','union','baseline_bn')[1]:.3f}bn. `inventory.cjs` reuses the frozen `lineage_addition.cjs` construction with later-only and G3-rate-only cases; both the full case and the union intercept reproduce its oracle at 1e-9bn. The two fill-in methods are averaged after computing their individual changes. Endpoints remain specifications 16/11; tables give a fixed-endpoint pair and do not claim a newly optimized band over altered specifications. [CALCULATION: `inventory.cjs` → `derived/inventory.json`]

All arms start from the same v7 baseline. National budgets/stocks, responses, the household-serving part, production, all receipts, state-price intensity and the population frame hold fixed. Item 6's tax changes are neither added again nor recalculated. Business activity follows its corrected/smoothed industry wage-share method, weighted here by private gross output rather than tax bases. Government and housing output are excluded; private nonprofits remain. Mining's old service allocation is retained in the main proxy: nonmining numerator / full output + mining output fraction × old household/demand key. Added people take the case's G3plus/white wage shares times those groups' output factors, exactly the item-6 addition rule. This is a modeled industry profile for the unobserved added people. [DATA: `activity_keys.json`; `inventory.json:added_wage_shares`] [ASSUMPTION]

## Primary shares and what they measure

Police: the FBI 2023/2024 NIBRS location archives are parsed into selected commercial-location offense fractions. These are reported **offenses**, not deduplicated incidents, business victims or staff time. Fire: USFA NFIRS 2020 all-run property-use percentages, including EMS and aid, are parsed; the fire-only denominator is expressly rejected for all-department spending. Their dates/coverage differ. Commercial locations can contain household victims or medical calls. Treating a location fraction as a spending fraction requires equal resource intensity, an unverified assumption. The broad arm adds mixed/public uses and is not a higher measured business share. [SOURCE: FBI/USFA primary links and pins in `source-evidence.md`; DATA: `inputs/incident_shares.json`] [ASSUMPTION]

Police preserves the current half-offending/half-population construction, applying the business proxy only to the protective population half of the non-border pool. CBP and all ICE custody retain their keys. Fire's business fraction replaces its population allocation. Both changes preserve the current state-price correction using a common intensity factor; the location or cost index of business-serving work is not measured. BEA 2024 Table 3.16 provides police/fire/courts/prisons proportions; they close to the parent public-safety total and reproduce the existing CJ lane. That expense mix is a crosswalk to the current aggregate, not a newly observed line-specific budget. [CALCULATION: `spending_inputs.py` → `inputs/spending_shares.json`; `analyze.py` → `line_changes.csv`] [ASSUMPTION]

Courts and general administration: measured business involvement in state contract trials exists, but its denominator excludes most court work and gives no spending share. Their rekeying is **0 by unresolved-data assumption**, not a finding of zero business use. Courthouses are in office/general-government capital; those components remain unchanged. Municipal-enterprise business load fractions were not identified here. Their current capital keys and enterprise surplus remain unchanged; no generic output share is imposed on water, sewer, power, transit, airports, ports, toll roads or the residual. [SOURCE: BJS primary table and U.S. Courts catalog traced in `source-evidence.md`; DATA: `inventory.json:meta.capital_return`; GAP] [ASSUMPTION]

Highways: FHWA HCAS V-21 already splits cost responsibility between passenger vehicles (autos, pickups/vans, buses) and freight trucks. The inherited transcription was parsed, its 44 cells independently checked visually against the pinned primary image; this is not claimed as fresh OCR. Federal addendum HTML, VM-1 XLSX and Oregon's corrected PDF are parsed directly. Current truck mileage, federal cost responsibility and Oregon's heavy-vehicle forecast have different estimands; substitution arms do not form a statistical confidence interval. No measured national business-use share for light pickups/vans was obtained. [SOURCE: primary links/pins in `highways-evidence.md`; DATA: `inputs/highway_shares.json`]

The road demand arm retains the existing consumption-keyed freight contribution and changes nothing. The union freight key is verified against the authoritative pre-road v4 model with `roadKeysOf`, 1e-12; gasoline receipts remain fixed. The supply arm changes only that existing freight contribution and the corresponding highway-capital key once. [CALCULATION: `inventory.cjs:direct_union_road_keys`; `analyze.py`]

**[DEGRADED] Lineage freight split:** the age-mix item independently profiles the economic-affairs parent, roads correction and excise receipts. Their current totals can be inverted into an effective passenger/consumption pair, but that pair is not a literal measured lineage consumption key. Lineage supply-key and share-substitution arms are therefore effective-key approximations; union freight results use the verified principal key. This limitation affects the freight sensitivities, not the central-zero recommendation or the police/fire arm. [DATA: `method-review.md`; `main_case_2026_10_07/item_age_mix.cjs:profileOf`; INFERENCE]

## Every arm, one change from v7

Each entry is low / high in $bn/year. SEs apply only to the union and condition on the national functional/location shares, BEA output, pooling, mean fill-in factors, state-price intensity and mapped household key. Road consumption is held fixed in its SE. Replicate covariance is preserved by combining vectors before calculating SDR errors. No full lineage SE is reported: added people are not observed in CPS, and correlated model uncertainties are not propagated. [CALCULATION: `activity_keys.py`, `analyze.py`]

"""
    table_rows=[]
    for arm in s["arms"]:
        name=arm["arm"]
        table_rows.append([f'`{name}`',show(pair(name,"union","change_bn")),show(pair(name,"lineage","change_bn"))," / ".join(f"{x:.3f}" for x in pair(name,"union","conditional_union_key_se_bn")),"below"])
    body += table(["Arm", "Union Δ", "Lineage Δ", "Conditional union SE", "$5bn bar"],table_rows)
    body += "\n[CALCULATION: `derived/arms.csv`; full resulting levels and members in that file. `line_changes.csv` preserves method/line changes; `break_shares.csv` stores unresolved-share diagnostics.]\n\n"
    breaks=list(csv.DictReader((HERE/"derived/break_shares.csv").open()))
    b=[next(float(r["business_share_for_5bn"]) for r in breaks if r["component"]=="general_administration" and r["frame"]=="lineage" and r["end"]==e) for e in ["low","high"]]
    ent=[next(float(r["delta_if_all_business_bn"]) for r in breaks if r["component"]=="municipal_enterprise_capital" and r["frame"]=="lineage" and r["end"]==e) for e in ["low","high"]]
    body += f"General administration would need a business-serving share of about {b[0]*100:.1f}%/{b[1]*100:.1f}% to move the lineage endpoints by $5bn under this output key and expense/stock crosswalk. An illustrative 100% business allocation of the nonhousing municipal-enterprise capital alone moves them {ent[0]:+.3f}/{ent[1]:+.3f}bn, holding its surplus receipts fixed; that construction is not recommended. Thus the review's rough $3.5–14bn fall is not established by the acquired event data, but a larger fall cannot be ruled out without those missing expenditure/load shares. [CALCULATION: `break_shares.csv`] [ASSUMPTION]\n\n"
    body += "## Complete spending and capital inventory\n\nAmounts below are union / lineage charge at low then high, $bn/year, averaged across methods. Every responsive spending row and public-capital component is present; fixed spending rows also appear in `inventory.csv`. Synthetic corrections are signed adjustments, not new national budgets. The engine's authoritative amounts are used; the stored `share` field can differ from target/national after source re-pricing. Capital rule definitions and exact stocks/responses are retained in `inventory.json:meta.capital_return`. [CALCULATION: `inventory.cjs`]\n\n"
    def mean(kind,id,end,field):
        vals=[next(x[field] for x in r[kind] if x["id"]==id) for r in inv["runs"] if r["end"]==end]
        return sum(vals)/len(vals)
    display=[]
    for x in inv["runs"][0]["spending"]:
        if not any(mean("spending",x["id"],e,"response")!=0 for e in ["low","high"]):
            continue
        display.append([x["id"],x["key"],f'{mean("spending",x["id"],"low","response"):.3f}/{mean("spending",x["id"],"high","response"):.3f}'," / ".join(f'{mean("spending",x["id"],e,f):.3f}' for e in ["low","high"] for f in ["union_charge_bn","lineage_charge_bn"])])
    body+=table(["Spending line","Key","Response low/high","U low / L low / U high / L high"],display)
    body+="\nCapital business shares are zero in the recommended central. Highway supply arms carry their altered road key through both spending and capital. The POS-capital arm additionally imposes the expense proxy mix on public-safety structures; that spending-to-stock crosswalk is unmeasured, so it stays beside the central. Office/courthouse stock stays fixed. [ASSUMPTION]\n\n"
    display=[]
    for x in inv["runs"][0]["capital"]:
        display.append([x["id"],x["key_rule"]["kind"],x["response_rule"]["kind"]," / ".join(f'{mean("capital",x["id"],e,f):.3f}' for e in ["low","high"] for f in ["union_return_bn","return_bn"])])
    body+=table(["Capital component","Key rule","Response rule","U low / L low / U high / L high"],display)
    body += f"""
## Gates, files and reproduction

- Source/control SHA256 manifest: `inputs/pins.json` (26 records); changing a pinned source fails loudly.
- Existing-case positive controls: `inventory.cjs`, {len(inv['gates'])} gates, v7 and union intercept to 1e-9bn.
- Activity: {len(activity['gates'])} gates; generation/replicate conservation, old cell shares/SEs, primary-output normalization and national closure to 1e-6bn.
- National safety subfunctions close to one at 1e-12 and reproduce the CJ lane to 1e-9bn. FBI totals close exactly; printed source percentages retain explicit rounding bounds.
- Sensitivities: {len(s['gates'])} gates, union road keys independently verified, zero-change controls, unchanged national budget/stock construction.
- `test_gates.py`: demand/freight overlap regression, every output's line closure, stale-source rejection, absent lineage SE. Incident acquisition also has source-corruption and wrong-total negative controls.
- Derived files: `inventory.json`, `inventory.csv`, `activity_keys.json`, `arms.csv`, `line_changes.csv`, `break_shares.csv`, `summary.json`.

Run offline from the repository root (default extraction commands do not download):

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/business_services_key_2026_10_14 \\
  "uv run --no-project python3 {{lane}}/pins.py" \\
  "node {{lane}}/inventory.cjs" \\
  "uv run --no-project python3 {{lane}}/spending_inputs.py" \\
  "uv run --no-project python3 {{lane}}/acquire_highways.py" \\
  "uv run --no-project python3 {{lane}}/acquire_incidents.py --self-check" \\
  "uv run --no-project python3 {{lane}}/activity_keys.py" \\
  "uv run --no-project python3 {{lane}}/analyze.py" \\
  "uv run --no-project python3 {{lane}}/test_gates.py" \\
  "uv run --no-project python3 {{lane}}/report.py"
```

No `--allow-unrun` is needed. The final handoff records the lane-wide command's observed exit code and IDENTICAL count. Source acquisition for a fresh cache is documented in the source evidence files; initialization refuses to replace existing pins. No frozen case, other lane, research document or Git metadata is mutated.

## Log

- 2026-10-14 20:36:37 JST (`date`): scope/status read; handoff created before computation.
- 2026-10-14 20:41:31 JST (`date`): existing freight split and safety keys traced; inventory and safety-source controls passed.
- 2026-10-14 20:52:51 JST (`date`): all primary source subtasks read; first integrated proxy/freight rows inspected.
- {stamp} (`date`): result rendered from current outputs; independent method review integrated. Activity builds used 3.85–17.22s and 1.09–1.60GB peak RSS; incident/highway/safety parsers each under 1s and 0.08GB. Integrated analysis under 0.02s. Measurements are Python `time.perf_counter`/`resource.getrusage`, not `/usr/bin/time -l`. Final combined rerun timing belongs to the handoff. [CALCULATION: script stdout and source evidence logs]
"""
    (HERE/"RESULT.md").write_text(body)
    print("PASS rendered RESULT.md from current computed outputs")


if __name__ == "__main__":
    main()
