#!/usr/bin/env python3
"""Preserve round-1 outputs and write the extension's stacks and outer envelopes.

Outer envelopes follow decision-09-27 arithmetic, not statistical independence.
Mutually exclusive arms never enter the same family's extreme more than once.
"""
from __future__ import annotations
import csv
import json
import resource
import time
import numpy as np
from core import CACHE, DERIVED, HERE
from refine import se
from reallocation import two_block


def main():
    start=time.perf_counter()
    old=json.loads((DERIVED/"summary.json").read_text())
    realloc=json.loads((DERIVED/"reallocation.json").read_text())
    k5=json.loads((DERIVED/"k5_cells_summary.json").read_text())
    c=np.load(CACHE/"core.npz")
    rv=np.load(CACHE/"reallocation_vectors.npz")
    co=json.loads((DERIVED/"core.json").read_text())
    gates=[]
    def gate(name,ok,value=None):
        gates.append(dict(name=name,passed=bool(ok),value=value))
        if not ok: raise RuntimeError(f"[BLOCKED] {name}: {value}")
    for name,block in (("round1",old),("reallocation",realloc),("subsidy_cells",k5)):
        gate(f"upstream {name} gates pass",all(g["passed"] for g in block["gates"]))
    cells=c["cells"]
    subsidy="ag0_624excluded_oreexcluded"
    with (DERIVED/"k5_cells_vectors.csv").open() as f:
        subsidynat={r["cell"]:float(r["responding_national_bn"]) for r in csv.DictReader(f) if r["arm"]==subsidy}
    sv=np.array([subsidynat[str(x)] for x in cells])[:,None]
    with (DERIVED/"k5_cells_replicates.csv").open() as f:
        reps={p:np.zeros(161) for p in ("union","lineage")}
        for r in csv.DictReader(f):
            if r["arm"]==subsidy and r["population"] in reps:
                reps[r["population"]][int(r["replicate"])]=float(r["delta_net_cost_bn"])
    w=c["size_wages_national"].sum(axis=1)/1e9
    mining=np.isin(cells,["211","212","213"])
    gov=np.isin(cells,["GOVF","GOVSL"])
    active=w[:,0]>0
    arms={}
    diagnostics={}
    def result(v,rd,pop):
        r=dict(delta_net_cost_bn=float(v[0]),delta_conditional_se_bn=se(v),over_5bn=bool(abs(v[0])>=5))
        if pop=="lineage":
            i=("low","high").index(rd)
            r.update(headline_bn=old["adopted_headline_bn"][i]+float(v[0]),cash_headline_bn=old["adopted_cash_bn"][i]+float(v[0]))
        return r
    for rd in ("low","high"):
        for pop in ("union","lineage"):
            s=c["shares_union"].copy();wg=c["size_wages_union"].sum(axis=1)/1e9
            if pop=="lineage":
                s+=sum(co["lineage_rates"][g]*c[f"shares_{g}"] for g in co["lineage_rates"])
                wg+=sum(co["lineage_rates"][g]*c[f"size_wages_{g}"].sum(axis=1)/1e9 for g in co["lineage_rates"])
            gate(f"{pop} subsidy jobs-key control 1e-9",np.max(abs((s*sv).sum(axis=0)-reps[pop]))<1e-9)
            for tname,tcells in realloc["tradable_cells"].items():
                t=np.isin(cells,tcells);n=active&~gov&~mining&~t;fixed=active&~(t|n)
                spend,terms=two_block(w,wg,s,sv,t,n,fixed,realloc["demand"][pop])
                # This conservative vector has no mining subsidies; check rather
                # than inheriting that fact silently in the stacked loss.
                gate(f"{tname} resource subsidy kept out",not sv[mining].any())
                spend+=terms["rate"]*wg[mining].sum(axis=0)
                for networkland in (False,True):
                    taxarm=f"stack_K1_K2_K7_mining_{'network_land_' if networkland else ''}{tname}"
                    name=f"stack_K1_K2_K7_mining_subsidy_{'network_land_' if networkland else ''}{tname}"
                    v=rv[f"{taxarm}__{rd}__{pop}"]+spend
                    arms.setdefault(name,{}).setdefault(rd,{})[pop]=result(v,rd,pop)
                    summed=old["arms"]["stack_K1_industry_size_K2"][rd][pop]["delta_net_cost_bn"]+realloc["arms"][f"K7_with_mining_{tname}_national"][rd][pop]["delta_net_cost_bn"]+float(reps[pop][0])
                    if networkland:
                        summed+=sum(realloc["arms"][a][rd][pop]["delta_net_cost_bn"] for a in ("network_response_0_7","commercial_land_response_0"))
                    diagnostics[f"{name}__{rd}__{pop}"]=dict(standalone_sum_bn=summed,exact_stack_bn=float(v[0]),interaction_bn=float(v[0])-summed,subsidy_loss_after_reallocation_bn=float(spend[0]))
    # Named point-arm envelope. K3 special assessments known to overlap are out;
    # legal-form selection envelopes remain separately unresolved. Broad T is
    # fixed throughout the joint family to avoid mixing incompatible intensities.
    families={
      "K1_legal_form":[("old","K1_industry_size")],
      "K2_foreign_source":[("old","K2_foreign_source_removed")],
      "K3_documentary":[("old","K3_documentary_only")],
      "K4_finer_detail":[("old","K4_strict_conly")],
      "K5_subsidies":[("sub","ag1_624included_oreincluded"),("sub",subsidy)],
      "K6_mining_refill":[("new","K6_mining_refill_broad_national")],
      "agriculture0_with_refill":[("new","K6_agriculture0_refill_broad_national")],
      "K7_nontradable_reallocation":[("new","K7_broad_national")],
      "network":[("new","network_response_0_7")],
      "land":[("new","commercial_land_response_0")]}
    envelope={}
    selected={}
    for rd in ("low","high"):
        envelope[rd]={}
        for pop in ("union","lineage"):
            entries=[]
            for family,options in families.items():
                vals=[(0.,"central")]
                for kind,name in options:
                    value=k5["arms"][name][pop]["delta_net_cost_bn"] if kind=="sub" else (old if kind=="old" else realloc)["arms"][name][rd][pop]["delta_net_cost_bn"]
                    vals.append((value,name))
                lo,loname=min(vals);hi,hiname=max(vals)
                entries.append(dict(family=family,down_bn=lo,down_arm=loname,up_bn=hi,up_arm=hiname))
            selected[f"{rd}_{pop}"]=entries
            down=sum(x["down_bn"] for x in entries);up=sum(x["up_bn"] for x in entries)
            qdown=-float(np.sqrt(sum(x["down_bn"]**2 for x in entries)));qup=float(np.sqrt(sum(x["up_bn"]**2 for x in entries)))
            r=dict(all_down_delta_bn=down,all_up_delta_bn=up,quadrature_down_delta_bn=qdown,quadrature_up_delta_bn=qup)
            if pop=="lineage":
                center=old["adopted_headline_bn"][("low","high").index(rd)]
                r.update(all_down_headline_bn=center+down,all_up_headline_bn=center+up,quadrature_down_headline_bn=center+qdown,quadrature_up_headline_bn=center+qup)
            envelope[rd][pop]=r
            gate(f"{rd} {pop} envelopes ordered",down<=qdown<=0<=qup<=up)
    out=dict(arms=arms,stack_diagnostics=diagnostics,subsidy_stack=subsidy,joint=envelope,joint_selected_components=selected,
        outer_convention="decision-2026-09-27: sum same-direction point-arm components and root-sum-squares. Arithmetic envelopes, not confidence intervals or proof of independent uncertainty; excludes K1 unidentified legal-form selection envelope. Broad tradables fixed for all joint refill terms. Shared tax-vector and response interactions only in exact stack, not component-envelope convention.",
        recommendations={"K1":"arm: conditional legal-payroll model, no observed C-only employment", "K2":"adopt as source-measurement correction, retaining TY2021 proxy warning", "K3":"documentary arm; reject additive special assessment because owner measure includes it", "K4":"arm; retain summary key", "K5":"cell-based arms; withhold central pending programme/nonprofit/enterprise reconciliation", "K6":"mining/agriculture refill arms; reject support-equipment departure as measured correction", "K7":"two-block reallocation arm, not identified GE; broad low-side move crosses review bar", "network":"arm; 0.7 unmeasured", "land":"arm; zero price response unmeasured", "stack":"K2-only is measured scope correction. K1+K2 preserved conditional candidate. Exact two-block and full network/land/subsidy stacks are conditional stress candidates, not automatic adoption."},gates=gates)
    (DERIVED/"extended_summary.json").write_text(json.dumps(out,indent=2)+"\n")
    with (DERIVED/"extended_stacks.csv").open("w",newline="") as f:
        fields=["arm","reading","population","delta_net_cost_bn","delta_conditional_se_bn","over_5bn","headline_bn","cash_headline_bn"]
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");writer.writeheader()
        writer.writerows(dict(arm=a,reading=r,population=p,**v) for a,rs in arms.items() for r,ps in rs.items() for p,v in ps.items())
    runtime=dict(elapsed_s=time.perf_counter()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if runtime["peak_rss_bytes"]>=2.5e9:raise RuntimeError("[BLOCKED] integrate RSS exceeds 2.5GB")
    (CACHE/"extended_runtime.json").write_text(json.dumps(runtime)+"\n")
    print(json.dumps(dict(arms=arms,joint=envelope,gates=len(gates),runtime=runtime),indent=2))


if __name__=="__main__":
    main()
