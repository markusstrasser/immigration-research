#!/usr/bin/env python3
"""Integrate one-at-a-time K arms and the exact conditional K1×K2 stack."""
from __future__ import annotations
import csv
import json
import resource
import time

import numpy as np
from core import CACHE, DERIVED, FISCAL, HERE, digest


def se(v):
    return float(np.sqrt(4/160*np.square(v[1:]-v[0]).sum()))


def main():
    start=time.perf_counter()
    core=json.loads((DERIVED/"core.json").read_text())
    c=np.load(CACHE/"core.npz")
    k1=np.load(CACHE/"k1_targets.npz")
    k4=np.load(CACHE/"k4_targets.npz")
    k5=np.load(CACHE/"k5_changes.npz")
    k236=np.load(CACHE/"k236_targets.npz")
    sampling=json.loads((DERIVED/"k3_sampling.json").read_text())
    housing=json.loads((DERIVED/"k236.json").read_text())["K3"]
    maincase=json.loads((FISCAL/"main_case_2026_10_14/derived/summary.json").read_text())["v7"]
    gates=[]
    for file in ("core.json","k1_summary.json","k4_summary.json","k5_summary.json","k236.json","k3_sampling.json","housing_keys.json"):
        block=json.loads((DERIVED/file).read_text())
        if not all(g["passed"] for g in block["gates"]):
            raise RuntimeError(f"[BLOCKED] upstream gates fail: {file}")

    def gate(name,ok,value=None):
        gates.append({"name":name,"passed":bool(ok),"value":value})
        if not ok:
            raise RuntimeError(f"[BLOCKED] {name}: {value}")

    for path,record in json.loads((HERE/"inputs/pins.json").read_text()).items():
        gate(f"upstream source pin: {path}",digest(path)==record["sha256"])
    groups=["union","G3plus","white"]
    baseline={g:c[f"shares_{g}"].T@c["tax_corporate"] for g in groups}

    def add_lineage(parts):
        return parts["union"]+sum(core["lineage_rates"][g]*parts[g] for g in ("G3plus","white"))

    arms={}
    interactions={}
    records=[]
    table=[]
    for ri,rd in enumerate(("low","high")):
        response=core["responses"][rd]["corporate"]
        independent={}
        for variant in ("size_only","industry_size","industry_size_selection_min","industry_size_selection_max"):
            independent[f"K1_{variant}"]={g:(baseline[g]-k1[f"{variant}_{g}"])*response for g in groups}
        independent["K2_foreign_source_removed"]={g:(baseline[g]-k236[f"foreign_removed_{g}"])*response for g in groups}
        for mode in ("allform","conly","strict_allform","strict_conly"):
            independent[f"K4_{mode}"]={g:(baseline[g]-k4[f"{mode}_{g}"])*response for g in groups}
        independent["K6_support_only"]={g:k236[f"support_{rd}_{g}"] for g in groups}
        independent["K6_support_equipment_proxy"]={g:k236[f"support_equipment_proxy_{rd}_{g}"] for g in groups}
        stacked_target={g:k1[f"industry_size_cell_shares_{g}"].T@c["tax_corporate_ex_foreign"] for g in groups}
        independent["stack_K1_industry_size_K2"]={g:(baseline[g]-stacked_target[g])*response for g in groups}
        stacked=independent["stack_K1_industry_size_K2"]
        interaction={g:stacked[g]-independent["K1_industry_size"][g]-independent["K2_foreign_source_removed"][g] for g in groups}
        expected={g:(k1[f"industry_size_cell_shares_{g}"]-c[f"shares_{g}"]).T@(c["tax_corporate"]-c["tax_corporate_ex_foreign"])*response for g in groups}
        gate(f"{rd} exact K1×K2 interaction equals cross product in every replicate",all(np.max(abs(interaction[g]-expected[g]))<1e-9 for g in groups))
        interactions[rd]={"union_bn":float(interaction["union"][0]),"lineage_bn":float(add_lineage(interaction)[0]),"lineage_se_bn":se(add_lineage(interaction))}
        for name,parts in independent.items():
            values={"union":parts["union"],"lineage":add_lineage(parts)}
            arms.setdefault(name,{})[rd]={}
            for pop,delta in values.items():
                gate(f"{name} {rd} {pop} finite 161 replicates",delta.shape==(161,) and np.isfinite(delta).all())
                if name=="K2_foreign_source_removed" and pop=="lineage":
                    oracle=maincase["arms"]["job_capital_taxes_foreign_source_removed"]["change_from_the_case_bn"][ri]
                    gate(f"K2 {rd} reproduces exact adopted full-case arm",abs(delta[0]-oracle)<1e-9,float(delta[0]-oracle))
                result={"delta_net_cost_bn":float(delta[0]),"delta_conditional_se_bn":se(delta),
                        "item_net_cost_bn":-core["control"][rd][f"{pop}_bn"]+float(delta[0]),
                        "over_5bn":bool(abs(delta[0])>=5)}
                if pop=="lineage":
                    result["headline_bn"]=maincase["band_bn"][ri]+float(delta[0])
                    result["cash_headline_bn"]=maincase["cash_set_bn"][ri]+float(delta[0])
                arms[name][rd][pop]=result
                records.append({"arm":name,"reading":rd,"population":pop,**result})
    # K3 uses independent survey sampling errors, rather than creating a false
    # 161-column combined CPS/ACS replicate estimator.
    for name,components,ses in (("K3_gross_documentary_assessments",list(housing["components"]),sampling["gross"]),
                                 ("K3_documentary_only",["documentary"],sampling["components"]["documentary"]),
                                 ("K3_assessments_only",["special_assessments"],sampling["components"]["special_assessments"])):
        arms[name]={}
        for ri,rd in enumerate(("low","high")):
            arms[name][rd]={}
            for pop in ("union","lineage"):
                delta=sum(housing["components"][n][f"{pop}_delta_bn"] for n in components)
                result={"delta_net_cost_bn":delta,"delta_conditional_se_bn":ses[f"{pop}_conditional_se_bn"],"over_5bn":abs(delta)>=5}
                if pop=="lineage":
                    result["headline_bn"]=maincase["band_bn"][ri]+delta
                    result["cash_headline_bn"]=maincase["cash_set_bn"][ri]+delta
                arms[name][rd][pop]=result
                records.append({"arm":name,"reading":rd,"population":pop,**result})
    for name in sorted(k for k in k5.files if k.endswith("__union")):
        name=name.removesuffix("__union")
        full="K5_"+name
        arms[full]={}
        for ri,rd in enumerate(("low","high")):
            arms[full][rd]={}
            for pop in ("union","lineage"):
                v=k5[f"{name}__{pop}"]
                result={"delta_net_cost_bn":float(v[0]),"delta_conditional_se_bn":se(v),"over_5bn":bool(abs(v[0])>=5)}
                if pop=="lineage":
                    result["headline_bn"]=maincase["band_bn"][ri]+float(v[0])
                    result["cash_headline_bn"]=maincase["cash_set_bn"][ri]+float(v[0])
                arms[full][rd][pop]=result
                records.append({"arm":full,"reading":rd,"population":pop,**result})
    counts=json.loads((FISCAL/"main_case_2026_10_14/derived/corrections.json").read_text())["meta"]["lineage"]["counts"]
    summary={"frame":{"union_persons":counts["account_union"],"lineage_persons":counts["lineage_population"],"allocation":"personal","end_specifications":[16,11]},
      "baseline":core["control"],"adopted_headline_bn":maincase["band_bn"],"adopted_cash_bn":maincase["cash_set_bn"],
      "arms":arms,"interactions":interactions,"gates":gates,
      "recommendations":{"K1":"Conditional industry-size payroll refinement recommended only as a labelled modelled key, not observed member C-corporation employment. Size-only diagnostic; excluded sectors keep original key. Selection envelope can exceed review bar.",
        "K2":"Recommend exclusion of foreign-source residence tax from source tax at US jobs; retain historical SOI ratio as a year-mismatched proxy.",
        "K3":"Withhold central addition pending owner/tenant overlap reconciliation. Gross and documentary-only requested pricing retained as sensitivities.",
        "K4":"Keep central summary key; strict C-only minor refinement is a limited sizing check. No 2024 finer property-only analogue.",
        "K5":"Keep agricultural response0 under fixed-land premise. Withhold residual subsidy change until programs and enterprise offsets reconciled.",
        "K6":"Size only. Withhold departure assumption; extraction equipment fraction is a national proxy. Fixed output may refill support jobs.",
        "stack":"K1 industry-size conditional proxy plus K2 exclusion; exact simultaneous cell rekey, interaction measured. Conditional candidate, not adoption."},
      "uncertainty":core["uncertainty"],"K3_uncertainty":sampling["uncertainty"]}
    (DERIVED/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    fields=["arm","reading","population","delta_net_cost_bn","delta_conditional_se_bn","item_net_cost_bn","over_5bn","headline_bn","cash_headline_bn"]
    with (DERIVED/"arms.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");writer.writeheader();writer.writerows(records)
    for arm,values in arms.items():
        row={"arm":arm}
        for rd in ("low","high"):
            for pop in ("union","lineage"):
                for key in ("delta_net_cost_bn","delta_conditional_se_bn"):
                    row[f"{pop}_{rd}_{key}"]=values[rd][pop][key]
        table.append(row)
    with (DERIVED/"comparison.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(table[0]),lineterminator="\n");writer.writeheader();writer.writerows(table)
    metrics={"elapsed_s":time.perf_counter()-start,"peak_rss_bytes":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if metrics["peak_rss_bytes"]>=2.5e9:
        raise RuntimeError("[BLOCKED] integration RSS exceeds 2.5GB")
    (CACHE/"refine_runtime.json").write_text(json.dumps(metrics)+"\n")
    print(json.dumps({"stack":arms["stack_K1_industry_size_K2"],"interactions":interactions,"gates":len(gates),"runtime":metrics},indent=2))


if __name__=="__main__":
    main()
