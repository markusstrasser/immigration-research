#!/usr/bin/env python3
"""Conditional K3 sampling SE: CPS modeled owner key and ACS rent proxy.

ACS/CPS samples are independent. Live v7 main estimates, response parameters,
lineage factors and source tax totals are fixed calibration targets. These SEs
do not cover national/source uncertainty, lineage counts, or overlap uncertainty.
"""
from __future__ import annotations
import gc
import json
import resource
import time
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from core import CACHE, DERIVED, FISCAL, HERE, digest, load


def main():
    start = time.perf_counter()
    source = load()
    d = source.load_frame()
    masks = source.masks(d)
    weights = source.row4_weights(d, masks, json.loads(source.ROW4.read_text()))
    with zipfile.ZipFile(source.CPS) as z:
        hh = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "H_TENURE", "HPROP_VAL"])
    d = d.merge(hh, left_on="PH_SEQ", right_on="H_SEQ", how="left", validate="many_to_one", suffixes=("", "_housing"))
    params_path = FISCAL / "gen_ledger_extension_2026_09_16/state_parameters.csv"
    params = pd.read_csv(params_path).set_index("fips")
    members = d.groupby("PH_SEQ").PPPOS.transform("size").to_numpy(float)
    owner = np.where(d.H_TENURE.eq(1), d.GESTFIPS.map(params.property_tax_effective_rate)*d.HPROP_VAL/members, 0)
    # The existing owner model distributes the household amount within SPM units.
    unit = pd.factorize(d.SPM_ID, sort=True)[0]
    count = np.bincount(unit)
    vector = np.bincount(unit, weights=owner)[unit]/count[unit]
    num = np.array([np.sum(vector[masks["union"]]*weights[masks["union"],r]) for r in range(161)])
    den = np.array([np.sum(vector[masks["civilian"]]*weights[masks["civilian"],r]) for r in range(161)])
    owner_share = num/den
    owner_se = source.se(owner_share)
    raw_owner = {"share":float(owner_share[0]),"se":owner_se,"group_bn":float(num[0]/1e9),"national_bn":float(den[0]/1e9)}
    del d, weights, hh, owner, vector, unit, count, masks, members
    gc.collect()
    ext = FISCAL.parents[1] / "sources/immigration-fiscal/data/external/acs_pums_2024_1yr"
    hus_path, pus_path = ext/"csv_hus.zip", ext/"csv_pus.zip"
    expected = {hus_path:"8281008e53de98f0ef81e7a2ee5a8725991dda1ecfd2713ead73246425e515d0",
                pus_path:"afdc6d90c6e2f0bab365ed32d95ba4c4d8ac651162f46ac7861295b2dc469894"}
    pins={str(params_path):{"sha256":digest(params_path)}}
    for path, sha in expected.items():
        actual=digest(path)
        if actual!=sha:
            raise RuntimeError(f"[BLOCKED] changed ACS source {path.name}")
        pins[str(path)]={"sha256":actual}
    chunks=[]
    with zipfile.ZipFile(hus_path) as z:
        for name in ("psam_husa.csv","psam_husb.csv"):
            for h in pd.read_csv(z.open(name),usecols=["SERIALNO","TEN","NP","RNTP","ADJHSG"],dtype={"SERIALNO":str},chunksize=100000):
                h=h.loc[h.TEN.eq(3)&h.NP.gt(0)&h.RNTP.notna()].copy()
                h["rent"]=12*h.RNTP*h.ADJHSG/1e6/h.NP
                chunks.append(h[["SERIALNO","rent"]])
    rents=pd.concat(chunks,ignore_index=True).set_index("SERIALNO").rent
    if not rents.index.is_unique:
        raise RuntimeError("[BLOCKED] duplicate ACS housing ID")
    del chunks
    sums=np.zeros((2,81))
    cols=["PWGTP"]+[f"PWGTP{i}" for i in range(1,81)]
    with zipfile.ZipFile(pus_path) as z:
        for name in ("psam_pusa.csv","psam_pusb.csv"):
            for p in pd.read_csv(z.open(name),usecols=["SERIALNO","STATE","HISP","POBP"]+cols,dtype={"SERIALNO":str},chunksize=50000):
                p=p.loc[p.STATE.le(56)].copy()
                amount=p.SERIALNO.map(rents).fillna(0).to_numpy(float)
                member=(p.HISP.eq(2)|p.POBP.eq(303)).to_numpy()
                k=amount>0
                w=p.loc[k,cols].to_numpy(float)
                sums[0]+=amount[k]@w
                sums[1]+=amount[k&member]@p.loc[k&member,cols].to_numpy(float)
    rent_share=sums[1]/sums[0]
    rent_se=float(np.sqrt(4/80*np.square(rent_share[1:]-rent_share[0]).sum()))
    housing=json.loads((DERIVED/"housing_keys.json").read_text())
    if abs(owner_share[0]-housing["lines"]["modeled_owner_property"]["union_share"])>1e-9:
        raise RuntimeError("[BLOCKED] CPS owner model does not reproduce live v7 key")
    expected_rent=housing["lines"]["tenant_occupied_property"]["union_share"]
    if abs(rent_share[0]-expected_rent)>5e-7:
        raise RuntimeError(f"[BLOCKED] ACS proxy does not reproduce frozen rounded rent key: {rent_share[0]}")
    nat=json.loads((DERIVED/"k236.json").read_text())["K3"]
    out={"owner_CPS_raw":raw_owner,"renter_ACS_proxy":{"share":float(rent_share[0]),"se":rent_se},
         "uncertainty":"Independent CPS owner-model and ACS renter-proxy sampling SEs, calibrated to live main keys; responses, nationwide taxes and lineage scaling fixed. Not a joint full-estimator SE.","components":{},
         "gates":[{"name":"ACS renter proxy reproduces frozen rounded key <=5e-7", "passed":True},
                   {"name":"CPS modeled owner key reproduces live v7 <=1e-9", "passed":True}]}
    for name, component in nat["components"].items():
        out["components"][name]={}
        for pop in ("union","lineage"):
            variance=0
            for kind,line in (("owner","modeled_owner_property"),("tenant","tenant_occupied_property")):
                h=housing["lines"][line]
                raw,se=(owner_share[0],owner_se) if kind=="owner" else (rent_share[0],rent_se)
                cal=h[f"{pop}_share"]/raw
                variance+=(component[f"{kind}_bn"]*h["response"]["low"]*cal*se)**2
            out["components"][name][f"{pop}_conditional_se_bn"]=float(np.sqrt(variance))
    total={}
    for pop in ("union","lineage"):
        # Components use the same keys: perfect shared sampling error across
        # documentary/assessment components, not separate quadrature terms.
        scale=sum(c["national_bn"] for c in nat["components"].values())/nat["components"]["documentary"]["national_bn"]
        total[f"{pop}_conditional_se_bn"]=out["components"]["documentary"][f"{pop}_conditional_se_bn"]*scale
    out["gross"]=total
    pin_path=HERE/"inputs/k3_sampling_pins.json"
    if pin_path.exists() and json.loads(pin_path.read_text())!=pins:
        raise RuntimeError("[BLOCKED] K3 sampling source pins changed")
    pin_path.write_text(json.dumps(pins,indent=2)+"\n")
    (DERIVED/"k3_sampling.json").write_text(json.dumps(out,indent=2)+"\n")
    metric={"elapsed_s":time.perf_counter()-start,"peak_rss_bytes":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if metric["peak_rss_bytes"]>=2.5e9:
        raise RuntimeError(f"[BLOCKED] peak exceeds 2.5GB: {metric}")
    (CACHE/"k3_sampling_runtime.json").write_text(json.dumps(metric)+"\n")
    print(json.dumps({"gross":total,"runtime":metric},indent=2))


if __name__=="__main__":
    main()
