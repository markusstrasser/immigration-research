#!/usr/bin/env python3
"""Fixed-price two-block capital reallocation; each arm starts from frozen v7.

Native refill in N comes out of T. Wage dollars are factor units at the pinned
wage; tax dollars per wage are a proxy for the released capital's tax intensity.
Native refill in resource sectors is a distinct mechanism, never added twice.
"""
from __future__ import annotations
import csv
import json
import resource
import time
import numpy as np
from core import CACHE, DERIVED, FISCAL, HERE, SOURCE, digest
from refine import se

LINES = ("corporate", "c_and_i_property", "other_production_taxes")


def record(parts, central_responses, rsp=None):
    """No falsey-response fallback: malformed explicit responses fail loudly."""
    rsp = central_responses if rsp is None else rsp
    if set(rsp) != {"low", "high"} or any(set(rsp[r]) != set(parts) for r in rsp):
        raise ValueError("[BLOCKED] explicit responses must name both readings and every line")
    if any(not np.isfinite(v) for r in rsp.values() for v in r.values()):
        raise ValueError("[BLOCKED] nonfinite response")
    return {r: sum(parts[l]*rsp[r][l] for l in parts) for r in rsp}


def two_block(w, wg, shares, taxes, tradable, nontradable, fixed,
              demand, reallocation=1., intensity="national"):
    """Return tax loss and the refill terms in bn, for each replicate.

    taxes is cell x replicate (or singleton column); shares are the frozen
    tax-allocation shares, including thin-cell pooling. w/wg retain actual cells.
    Signed N refill is essential: negative refill returns native labor to T.
    """
    jobs = (shares*taxes).sum(axis=0)
    jt = (shares[tradable]*taxes[tradable]).sum(axis=0)
    if intensity == "national":
        rate = taxes[tradable].sum(axis=0)/w[tradable].sum(axis=0)
    elif intensity == "group":
        rate = jt/wg[tradable].sum(axis=0)
    else:
        raise ValueError("[BLOCKED] unknown tradable intensity")
    demand = np.asarray(demand)
    n_release = demand*taxes[nontradable].sum(axis=0)
    refill = (wg[nontradable]-demand*w[nontradable]).sum(axis=0)
    jn = (shares[nontradable]*taxes[nontradable]).sum(axis=0)
    # Fixed sectors' existing tax treatment is unchanged here.
    delta = n_release + rate*refill - jn
    return jobs + reallocation*delta, dict(rate=rate, n_release=n_release,
        n_refill_wages=refill, t_release_for_refill=rate*refill,
        fixed_jobs=(shares[fixed]*taxes[fixed]).sum(axis=0))


def main():
    start = time.perf_counter()
    c = np.load(CACHE/"core.npz")
    k1 = np.load(CACHE/"k1_targets.npz")
    co = json.loads((DERIVED/"core.json").read_text())
    old = json.loads((DERIVED/"summary.json").read_text())
    dem = json.loads((DERIVED/"demand_keys.json").read_text())
    nat = json.loads((SOURCE/"derived/national.json").read_text())
    gates = []
    def gate(name, ok, value=None):
        gates.append(dict(name=name, passed=bool(ok), value=value))
        if not ok:
            raise RuntimeError(f"[BLOCKED] {name}: {value}")
    for p, pin in json.loads((HERE/"inputs/pins.json").read_text()).items():
        gate(f"upstream source pin: {p}", digest(p)==pin["sha256"])
    for file in ("core.json", "k1_summary.json", "summary.json", "demand_keys.json"):
        gate(f"upstream gates: {file}", all(x["passed"] for x in json.loads((DERIVED/file).read_text())["gates"]))
    # The requested 0.0814 comes from the case's adopted net consumption basis.
    keyfile = FISCAL/"consumption_key_2026_09_24/derived/key_specs.csv"
    with keyfile.open() as f:
        basis = next(r for r in csv.DictReader(f) if r["spec"]=="both_corridor_net_h2")
    demand_basis = float(basis["adopted_basis_share"])
    demand = {"union": demand_basis, "lineage": demand_basis+dem["added_demand_share"]}
    cells = c["cells"]
    source_rows = list(csv.DictReader((SOURCE/"derived/wages_by_industry.csv").open()))
    sectors = {r["cell"]:r["sector"] for r in source_rows}
    mining = np.array([sectors.get(x)=="mining" for x in cells])
    ag = np.array([sectors.get(x)=="agriculture" for x in cells])
    government = np.isin(cells,["GOVF","GOVSL"])
    active = c["size_wages_national"].sum(axis=1)[...,0]>0
    private = active & ~government
    narrow = np.array([sectors.get(x) in {"agriculture","durable","nondurable"} for x in cells])
    # Summary 511 includes software and other publishing; 5412OP mixes several
    # professional services. Explicit broad proxy also contains media (512), as
    # in the reviewer's broad tradables definition; the no-media arm is separate.
    broad = narrow | np.isin(cells,["511","512","514","523","5415","5412OP","481","483","55"])
    network = np.isin(cells,["22","513","482","486"])
    w = c["size_wages_national"].sum(axis=1)/1e9
    rates = co["lineage_rates"]
    def mix(key, pop):
        v = c[f"{key}_union"].copy()
        if pop=="lineage":
            v += sum(rates[g]*c[f"{key}_{g}"] for g in rates)
        return v
    arms, vectors, details = {}, {}, {}
    land0 = nat["tpp"]["tau_of_business_line"]+(1-nat["tpp"]["tau_of_business_line"])*(1-nat["land"]["lambda_b"])
    for rd in ("low","high"):
        tax = {ln:c[f"tax_{ln}"] for ln in LINES}
        responses = co["responses"][rd]
        amount = sum(tax[ln]*responses[ln] for ln in LINES)[:,None]
        corrected_amount = (c["tax_corporate_ex_foreign"]*responses["corporate"]+
             tax["c_and_i_property"]*responses["c_and_i_property"]+tax["other_production_taxes"])[:,None]
        for pop in ("union","lineage"):
            s = mix("shares",pop)
            wg = mix("size_wages",pop).sum(axis=1)/1e9
            # K1 changes C exposure only. Its group-specific shares can be encoded
            # as an effective per-cell tax vector; the same vector travels through
            # N demand and T intensity in the conditional stack.
            sk = k1["industry_size_cell_shares_union"].copy()
            if pop=="lineage":
                sk += sum(rates[g]*k1[f"industry_size_cell_shares_{g}"] for g in rates)
            # Propensity group-v-national belongs to the removed group's exposure,
            # NOT to the national demand-release/intensity: keep those national
            # vectors domestic; replace only target corporate jobs exposure.
            baseline = record({ln:s.T@tax[ln] for ln in LINES},co["responses"])[rd]
            gate(f"{rd} {pop} central control 1e-9", abs(baseline[0]-co["control"][rd][f"{pop}_bn"])<1e-9)
            candidates = {}
            for name,t in (("narrow",narrow),("broad",broad),("broad_no_media",broad & (cells!="512"))):
                n = private & ~t & ~mining
                fixed = active & ~(t|n)
                gate(f"{name} partitions wage universe", np.array_equal(t|n|fixed,active) and not ((t&n)|(t&fixed)|(n&fixed)).any())
                for intensity in ("national","group"):
                    loss, terms = two_block(w,wg,s,amount,t,n,fixed,demand[pop],intensity=intensity)
                    off,_ = two_block(w,wg,s,amount,t,n,fixed,demand[pop],0.,intensity)
                    gate(f"{rd} {pop} {name} {intensity} reallocation off reproduces jobs 1e-9", np.max(abs(off-baseline))<1e-9)
                    arm = f"K7_{name}_{intensity}"
                    candidates[arm] = loss
                    refill = terms["rate"]*wg[mining].sum(axis=0)
                    candidates[f"K6_mining_refill_{name}_{intensity}"] = baseline+refill
                    candidates[f"K7_with_mining_{name}_{intensity}"] = loss+refill
                    details[f"{arm}_{rd}_{pop}"] = {k:float(v[0]) for k,v in terms.items()}
                    # Agricultural fixed-land arm: both farm taxes and the farm
                    # jobs vanish from the departure key; native refill draws T.
                    ta = t & ~ag
                    ra = amount[ta].sum(axis=0)/w[ta].sum(axis=0) if intensity=="national" else (s[ta]*amount[ta]).sum(axis=0)/wg[ta].sum(axis=0)
                    candidates[f"K6_agriculture0_refill_{name}_{intensity}"] = baseline-(s[ag]*amount[ag]).sum(axis=0)+ra*wg[ag].sum(axis=0)
                    if intensity=="national" and name in ("narrow","broad"):
                        # Simultaneous legal/source correction: substitute corporate
                        # target exposure in jobs terms, while released native
                        # capital uses national domestic-source intensity.
                        corp = c["tax_corporate_ex_foreign"][:,None]*responses["corporate"]
                        job_correction = (sk-s)*corp
                        legal_jobs = (s*corrected_amount).sum(axis=0)+job_correction.sum(axis=0)
                        gate(f"{rd} {pop} K1K2 rekey reproduces existing stack 1e-9",abs(baseline[0]-legal_jobs[0]-old["arms"]["stack_K1_industry_size_K2"][rd][pop]["delta_net_cost_bn"])<1e-9)
                        stackloss, st = two_block(w,wg,s,corrected_amount,t,n,fixed,demand[pop])
                        # Only T and fixed jobs enter directly after reallocating N.
                        stackloss += job_correction[t|fixed].sum(axis=0)
                        stackloss += st["rate"]*wg[mining].sum(axis=0)
                        candidates[f"stack_K1_K2_K7_mining_{name}"] = stackloss
                        # Full stress stack: lower network and land mobility before
                        # computing both demand release and the T refill intensity.
                        mult = np.where(network,.7,1.)[:,None]
                        fulltax = (c["tax_corporate_ex_foreign"][:,None]*responses["corporate"]+
                            tax["c_and_i_property"][:,None]*land0+
                            tax["other_production_taxes"][:,None])*mult
                        full_loss, ft = two_block(w,wg,s,fulltax,t,n,fixed,demand[pop])
                        full_loss += ((sk-s)*corp*mult)[t|fixed].sum(axis=0)
                        full_loss += ft["rate"]*wg[mining].sum(axis=0)
                        candidates[f"stack_K1_K2_K7_mining_network_land_{name}"] = full_loss
                # Live payload demand is a separately labelled key sensitivity.
                live,_ = two_block(w,wg,s,amount,t,n,fixed,dem[f"{pop}_live"])
                candidates[f"K7_{name}_live_demand"] = live
            candidates["network_response_0_7"] = baseline-.3*(s[network]*amount[network]).sum(axis=0)
            candidates["commercial_land_response_0"] = baseline+(s.T@tax["c_and_i_property"])*(land0-responses["c_and_i_property"])
            # Merge to one sector, retaining exactly the frozen central nationals
            # and all wages; the resulting q*T is the authoritative plain arm.
            plain = wg.sum(axis=0)/w.sum(axis=0)*amount.sum()
            one,_ = two_block(w.sum(axis=0)[None,:],wg.sum(axis=0)[None,:],(wg.sum(axis=0)/w.sum(axis=0))[None,:],amount.sum()*np.ones((1,1)),np.array([True]),np.array([False]),np.array([False]),demand[pop])
            gate(f"{rd} {pop} one-sector equals plain-share all replicates 1e-6", np.max(abs(one-plain))<1e-6)
            if pop=="union":
                item = json.loads((SOURCE/"derived/item.json").read_text())
                gate(f"{rd} one-sector equals frozen plain-share arm 1e-6", abs(one[0]-item["arms"]["plain_wage_share"]["central_bn"][rd]["personal"])<1e-6)
                gate(f"{rd} land0 equals frozen arm 1e-9", abs(candidates["commercial_land_response_0"][0]-item["arms"]["business_land_at_0"]["central_bn"][rd]["personal"])<1e-9)
            for name,loss in candidates.items():
                delta = baseline-loss
                gate(f"finite 161 replicates {name} {rd} {pop}",delta.shape==(161,) and np.isfinite(delta).all())
                vectors[f"{name}__{rd}__{pop}"] = delta
                result = dict(delta_net_cost_bn=float(delta[0]),delta_conditional_se_bn=se(delta),item_net_cost_bn=float(-loss[0]),over_5bn=bool(abs(delta[0])>=5))
                if pop=="lineage":
                    ri=("low","high").index(rd)
                    result.update(headline_bn=old["adopted_headline_bn"][ri]+float(delta[0]),cash_headline_bn=old["adopted_cash_bn"][ri]+float(delta[0]))
                arms.setdefault(name,{}).setdefault(rd,{})[pop]=result
    pin_paths=[keyfile,SOURCE/"derived/national.json",SOURCE/"derived/wages_by_industry.csv",DERIVED/"demand_keys.json",DERIVED/"core.json",DERIVED/"k1_summary.json",CACHE/"core.npz",CACHE/"k1_targets.npz"]
    pins={str(p):{"sha256":digest(p)} for p in pin_paths}
    pinfile=HERE/"inputs/reallocation_pins.json"
    if pinfile.exists():
        gate("pinned reallocation inputs unchanged",json.loads(pinfile.read_text())==pins)
    pinfile.write_text(json.dumps(pins,indent=2)+"\n")
    out=dict(demand_basis=demand_basis,demand=demand,live_demand=dem,land_response_0=land0,
             tradable_cells={"narrow":list(map(str,cells[narrow])),"broad":list(map(str,cells[broad]))},network_cells=list(map(str,cells[network])),arms=arms,details=details,gates=gates,
             uncertainty="160 CPS SDR replicates conditional on demand shares, source totals, fixed added-person calibration and sector classification. No GE response, demand or ancestry uncertainty estimated.")
    (DERIVED/"reallocation.json").write_text(json.dumps(out,indent=2)+"\n")
    fields=["arm","reading","population","delta_net_cost_bn","delta_conditional_se_bn","item_net_cost_bn","over_5bn","headline_bn","cash_headline_bn"]
    with (DERIVED/"reallocation.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");writer.writeheader()
        writer.writerows(dict(arm=a,reading=r,population=p,**v) for a,rs in arms.items() for r,ps in rs.items() for p,v in ps.items())
    np.savez(CACHE/"reallocation_vectors.npz",**vectors)
    metric=dict(elapsed_s=time.perf_counter()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if metric["peak_rss_bytes"]>=2.5e9:
        raise RuntimeError("[BLOCKED] reallocation RSS exceeds 2.5GB")
    (CACHE/"reallocation_runtime.json").write_text(json.dumps(metric)+"\n")
    print(json.dumps(dict(gates=len(gates),demand=demand,metrics=metric)))


if __name__=="__main__":
    main()
