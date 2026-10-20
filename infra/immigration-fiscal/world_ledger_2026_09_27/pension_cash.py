"""Exact matched-cash adapter: existing valuation and package CASH functions.

The source producer writes to an explicit external directory, never through a
historical case producer's frozen-output guard. --verify-artifact rebuilds there
and compares every byte with the active case's pinned artifact.
"""
from copy import deepcopy
import hashlib
import io
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
import valuation as V
from gz_io import read_artifact
import mexico_pensions as C


def gate(condition, name, **detail):
    C.block(condition, name, **detail)


def _frame(records):
    return pd.DataFrame(records).replace({"generation": {"G3plus": "G3+"}})


def _value(case, raw, basis="cash"):
    """Reuse existing valuation_row, receipt_contract and child-credit routing.

    Their case metadata are safe only after set/cash classification metadata are
    proven identical below. ITEM_CLASS changes are restored for the importing caller.
    """
    glines = _frame(raw["lines"])
    union = _frame(raw["union_lines"])
    credit = V.child_credit_adjustments(case, glines)
    old = dict(V.ITEM_CLASS)
    try:
        V.ITEM_CLASS.clear()
        V.ITEM_CLASS.update(V.offset_classes(case))
        classes, payers = V.receipt_contract(case)
        if "coverage" in raw["payload"].get("meta", {}):
            V.prepare_coverage_values(case, glines, union, payload=raw["payload"], basis=basis)
        rows = []
        for r in glines[glines.side.ne("total")].assign(side=lambda x: x.side.replace({"capital": "spending"})).itertuples():
            k = (r.band_end, r.generation, r.side, r.line)
            rows.append(dict(case=case, end=r.band_end, generation=r.generation, side="receipt" if r.side=="receipt" else "spending",
                             line=r.line, **V.valuation_row(r, classes, payers, credit.get(k, 0.0))))
        vgen = pd.DataFrame(rows)
        union_credit = {}
        for (end, _, side, line), amount in credit.items():
            k = end, side, line
            union_credit[k] = union_credit.get(k, 0.0)+amount
        rows = []
        for r in union[union.side.ne("total")].assign(side=lambda x: x.side.replace({"capital": "spending"})).itertuples():
            k = r.band_end, r.side, r.line
            rows.append(dict(case=case, end=r.band_end, side="receipt" if r.side=="receipt" else "spending", line=r.line, F_bn=0.0,
                             **V.valuation_row(r, classes, payers, union_credit.get(k, 0.0))))
        val = pd.DataFrame(rows)
    finally:
        V.ITEM_CLASS.clear()
        V.ITEM_CLASS.update(old)
    return glines, vgen, val


def _metadata_equivalent(set_raw, cash_raw):
    def relevant(raw):
        p = raw["payload"]
        items = {x["id"]: x for x in p["meta"]["items"] if x.get("applied")}
        def item(identifier):
            x = items[identifier]
            first, count = x["edits"]["first"], x["edits"]["count"]
            return dict(parts=x.get("parts"), edits=p["edits"][first:first+count])
        return dict(child_credits=item("child_credits"), job_capital_taxes=item("job_capital_taxes"),
                    offsets=[(x["id"], x.get("of_component")) for x in p["meta"]["capital_return"]["components"]])
    if "coverage" in cash_raw["payload"].get("meta", {}):
        # v8 pensions alter cash coverage donor costs. Compare identities and
        # routes, not the pension-dependent magnitudes that this rerun rebuilds.
        a,b=set_raw["payload"]["meta"],cash_raw["payload"]["meta"]
        for key in ("union_completion", "capital_return"):
            gate(set(a[key])==set(b[key]), "cash_metadata_schema_changed", key=key)
        gate(set_raw["ends"]==cash_raw["ends"], "cash_end_specs_changed")
    else:
        gate(relevant(set_raw) == relevant(cash_raw), "cash_valuation_metadata_differs_from_set")


def _closure(raw, glines, vgen, val):
    checks = {}
    for column in ("amount_bn", "G_bn", "V_low_bn", "V_central_bn", "V_high_bn", "net_cost_bn",
                   "source_tax_credit_bn", "child_credit_other_residents_bn"):
        keys = ["end", "side", "line"]
        s = vgen.groupby(keys)[column].sum()
        u = val.set_index(keys)[column]
        gate(s.index.sort_values().equals(u.index.sort_values()), "cash_generation_union_keys", column=column)
        err = float((s-u.reindex(s.index)).abs().max())
        gate(err <= 1e-6, "cash_generation_union_values", column=column, error_bn=err)
        checks[f"union_{column}"] = err
    for r in raw["specs"]:
        end = r["band_end"]
        cost = glines[glines.band_end.eq(end) & glines.line.eq("cost") & glines.side.eq("total")].effect_bn.sum()
        err = abs(cost-r["cost_bn"])
        gate(err <= 1e-6, "cash_generation_union_cost", end=end, error_bn=err)
        checks[f"union_cost_{end}"] = err
        for gen in ("G1", "G2", "G3+"):
            totals = glines[glines.band_end.eq(end) & glines.generation.eq(gen) & glines.side.eq("total")].set_index("line")
            accounted = vgen[vgen.end.eq(end) & vgen.generation.eq(gen)].net_cost_bn.sum()+totals.loc["production", "effect_bn"]
            err = abs(accounted-totals.loc["cost", "effect_bn"])
            gate(err <= 1e-6, "cash_generation_cost", end=end, generation=gen, error_bn=err)
            checks[f"generation_cost_{end}_{gen}"] = err
    return checks


def _financing(raw, artifact):
    """Same pinned debt per-line fractions as winners_losers.federal_split.

    Cash cells already exclude pension accrual, so no pension-split line is added.
    The upstream debt file rounds amounts to six decimals: its established 1e-5
    line/federal reconciliation tolerance is retained and recorded.
    """
    debt = pd.read_csv(io.StringIO(artifact["debt_lines_csv"]))
    out, checks = {}, {}
    f_ind = artifact["induced_receipts_federal_share"]
    dshare = artifact["winner_meta"]["deficit"]["share"]
    union = _frame(raw["union_lines"])
    for spec in raw["specs"]:
        end = spec["band_end"]
        lines = union[union.band_end.eq(end) & union.side.ne("total")].copy()
        cap = lines.side.eq("capital")
        lines.loc[cap, "side"] = "capital_return"
        lines.loc[cap, "line"] = lines.loc[cap, "line"].str.removeprefix("capital_")
        lines = lines.set_index(["side", "line"])
        cost = -lines.effect_bn
        principal = debt[debt.end.eq(end) & debt.convention.eq("central")]
        principal = principal[principal.side.ne("pension_accrual") & principal.side.ne("production")].set_index(["side", "line"])
        gate(principal.index.is_unique and lines.index.is_unique, "cash_financing_unique_keys")
        unknown = [k for k in cost.index if k not in principal.index and abs(cost[k]) > 1e-12]
        gate(not unknown, "cash_financing_fraction_missing", keys=unknown)
        common = cost.index.intersection(principal.index)
        diff = float((cost.loc[common]-principal.loc[common, "gap_bn"]).abs().max())
        gate(diff < 1e-5, "cash_line_financing_control", end=end, error_bn=diff)
        checks[f"financing_line_{end}"] = diff
        ratio = (principal.federal_bn/principal.gap_bn).where(principal.gap_bn.ne(0), 0.0)
        masks = {k: common[principal.loc[common, "financing"].eq(k)] for k in ("cash", "resource_cost", "displaced_beneficiaries")}
        sums = {k: float(cost.loc[m].sum()) for k,m in masks.items()}
        feds = {k: float((cost.loc[m]*ratio.loc[m]).sum()) for k,m in masks.items()}
        sums["cash"] -= spec["F_bn"]
        feds["cash"] -= spec["F_bn"]*f_ind
        # The pinned set financing has already separated its pension accrual.
        old = artifact["winner_meta"]["fiscal"][end]
        checks[f"cash_federal_{end}"] = abs(feds["cash"]-old["cash_federal"])
        gate(checks[f"cash_federal_{end}"] < 1e-5, "cash_federal_financing_control", end=end)
        borrowing = dshare*feds["cash"]
        out[end] = dict(cost=-(spec["A_bn"]+spec["F_bn"]), cash=sums["cash"],
                        cash_federal=feds["cash"], resource=sums["resource_cost"],
                        resource_federal=feds["resource_cost"], displaced=sums["displaced_beneficiaries"],
                        displaced_federal=feds["displaced_beneficiaries"], future_borrowing=borrowing,
                        federal_today=(1-dshare)*feds["cash"]+feds["resource_cost"],
                        state_local=sums["cash"]-feds["cash"]+sums["resource_cost"]-feds["resource_cost"])
        gate(abs(sum(sums.values())-out[end]["cost"]) <= 1e-6, "cash_financing_total", end=end)
    out["central"] = {k:(out["low"][k]+out["high"][k])/2 for k in out["low"]}
    return out, checks


def adapt_cash(I, *, cells_path=None, artifact_key=None, allow_p032_proxy=True,
               public_pension_share=1.0, valuation_builder=None):
    """Return a new I dict on exact US cash cells; original I stays unchanged.

    public_pension_share affects Mexico fiscal_bn only; recipient_bn remains the
    domestic cash receipt. The row constructor must consume those separate fields.
    Default proxy is explicitly DEGRADED, never a claim of identified public spending.
    """
    gate(np.isfinite(public_pension_share) and 0 <= public_pension_share <= 1,
         "cash_public_pension_share_outside_bound", share=public_pension_share)
    gate(I.get("pension_basis") != "matched_cash", "cash_adapter_already_applied")
    mode = C.pension_basis("matched_cash", "cash", allow_p032_proxy=allow_p032_proxy)
    if public_pension_share != 1:
        mode["status"] = "[DEGRADED] P032 public-funding sensitivity; funding share is unverified"
    artifact_key = artifact_key or I["case"] + "_cash"
    manifest = HERE / "inputs/pension_cash_pins.json"
    gate(manifest.is_file(), "cash_source_manifest_missing", path=str(manifest))
    pins = json.loads(manifest.read_text())["artifacts"]
    gate(artifact_key in pins, "cash_source_artifact_missing", case=I["case"], key=artifact_key,
         recommendation="supply a separately pinned source artifact for this case; no v7 fallback")
    record = pins[artifact_key]
    gate(record["case"] == I["case"] and record["package_set"] == "cash", "cash_source_artifact_case_mismatch")
    source_path = Path(cells_path) if cells_path is not None else HERE / record["path"]
    gate(source_path.is_file(), "cash_source_artifact_file_missing", path=str(source_path))
    body = read_artifact(source_path)
    gate(hashlib.sha256(body).hexdigest() == record["sha256"], "cash_source_artifact_stale", path=str(source_path))
    artifact = json.loads(body)
    gate(artifact["mode"] in {"historical_probe", "exact_package_cash"} and artifact["case"] == I["case"]
         and artifact["package_set"] == "cash", "cash_cells_case_contract")
    set_raw, cash_raw = artifact["results"]["set"], artifact["results"]["cash"]
    _metadata_equivalent(set_raw,cash_raw)
    builder=valuation_builder or _value
    set_gl, set_vg, set_val = builder(I["case"],set_raw,basis="set")
    gl, vg, val = builder(I["case"],cash_raw,basis="cash")
    checks = _closure(cash_raw,gl,vg,val)
    for k, actual in (("vgen",set_vg),("val",set_val)):
        keys=["end","side","line"]+(["generation"] if k=="vgen" else [])
        a=actual.set_index(keys); old=I[k].set_index(keys)
        cols=["amount_bn","G_bn","V_low_bn","V_central_bn","V_high_bn","net_cost_bn"]
        gate(a.index.sort_values().equals(old.index.sort_values()), "set_snapshot_keys", table=k)
        err=float((a[cols]-old.reindex(a.index)[cols]).abs().to_numpy().max())
        gate(err<=1e-6,"set_snapshot_valuation_positive_control",table=k,error_bn=err)
        checks[f"set_snapshot_{k}"]=err
    # Route full recalculated cells; never subtract one aggregate accrual number.
    out=dict(I, glines=gl, vgen=vg, val=val, specs=I["specs"].copy(deep=True),
             gen=pd.read_csv(io.StringIO(cash_raw["generation_results_csv"])), ch=I["ch"].copy(deep=True),
             mxb=I["mxb"].copy(deep=True), pension_basis="matched_cash", us_pension_basis="cash")
    for spec in cash_raw["specs"]:
        end=spec["band_end"]
        gate(int(I["specs"].loc[end,"spec_id"]) == spec["spec_id"], "cash_end_specification_changed", end=end)
        for k in ("A_bn","P_bn","F_bn","cost_bn","welfare_bn","engine_A_bn","capital_total_bn"):
            out["specs"].loc[end,k]=spec[k]
    if artifact["mode"] == "exact_package_cash":
        financing,fc={},{}
        out["financing_basis"]="pooled_no_debt_split"
    else:
        financing,fc = _financing(cash_raw,artifact)
    checks.update(fc)
    ch=out["ch"]
    ch["pension_basis"]="set_reference_not_recomputed"
    def put(name,values):
        for end,value in values.items(): ch.loc[name,f"bn_{end}"]=value
        ch.loc[name,"pension_basis"]="matched_cash"
        ch.loc[name,"status"]=artifact["mode"]
        ch.loc[name,"note"]=str(ch.loc[name,"note"])+"; exact CASH package cells; matched-cash reading"
    specs=out["specs"]
    mid=lambda low,high:dict(low=low,central=(low+high)/2,high=high)
    put("main_case",mid(-specs.loc["low","cost_bn"],-specs.loc["high","cost_bn"]))
    if financing:
        put("fiscal",{end:-f["cost"]+f["displaced"] for end,f in financing.items()})
        put("future_taxpayers",{end:-f["future_borrowing"] for end,f in financing.items()})
        put("displaced_beneficiaries",{end:-f["displaced"] for end,f in financing.items()})
        put("fiscal_federal_today",{end:-f["federal_today"] for end,f in financing.items()})
        put("fiscal_state_local",{end:-f["state_local"] for end,f in financing.items()})
        put("fiscal_cash",{end:-(f["cash"]-f["future_borrowing"]) for end,f in financing.items()})
        put("fiscal_resource",{end:-f["resource"] for end,f in financing.items()})
    else:
        # All recipients outside the group stay in their incidence classes. The
        # pooled payer row has no timing/geographic financing assertion.
        def capped_cells(raw):
            payload=raw["payload"]["meta"]
            # distribution_weights inputs.json capped_programs declaration:
            # rental assistance, LIHEAP and public housing's enterprise deficit.
            programs={"housing_subsidies","energy_assistance","housing_enterprise_surplus"}
            carriers={line for line,source in payload.get("union_completion",{}).get("carriers",{}).items()
                      if source.get("parent_line") in programs}
            values={("line",r["band_end"],r["side"],r["line"],column):r[column]
                    for r in raw["union_lines"] if r["line"] in programs|carriers
                    for column in ("amount_bn","response","effect_bn")}
            for end,block in payload["coverage"]["by_end"].items():
                for r in block["decomposition"]["line_parts"]:
                    if r.get("source_line") in programs:
                        values[("coverage",end,r["generation"],r["line"],"coverage_bn")]=r["coverage_bn"]
            return values
        original_capped,cash_capped=capped_cells(set_raw),capped_cells(cash_raw)
        gate(set(original_capped)==set(cash_capped),"cash_displaced_source_keys_unchanged")
        error=max(abs(value-cash_capped[key]) for key,value in original_capped.items())
        gate(error<1e-9,"cash_displaced_sources_unchanged",error_bn=error)
        mixed_set,mixed_cash=set_raw["payload"]["meta"]["mixed_unit_removal"],cash_raw["payload"]["meta"]["mixed_unit_removal"]
        gate({k:v for k,v in mixed_set.items() if k!="which"}=={k:v for k,v in mixed_cash.items() if k!="which"},
             "cash_displaced_mixed_sources_unchanged")
        checks["displaced_sources_unchanged"]=error
        displaced={end:-float(I["ch"].loc["displaced_beneficiaries",f"bn_{end}"]) for end in ("low","high")}
        put("displaced_beneficiaries",mid(-displaced["low"],-displaced["high"]))
        put("fiscal",mid(specs.loc["low","A_bn"]+specs.loc["low","F_bn"]+displaced["low"],
                         specs.loc["high","A_bn"]+specs.loc["high","F_bn"]+displaced["high"]))
        for name in ("future_taxpayers","fiscal_federal_today","fiscal_state_local","fiscal_cash","fiscal_resource"):
            if name in ch.index:
                ch.loc[name,["bn_low","bn_central","bn_high"]]=np.nan
                ch.loc[name,"status"]=artifact["financing_status"]
    put("wages",mid(specs.loc["low","P_bn"],specs.loc["high","P_bn"]))
    ch.drop(index="future_pension_accrual",inplace=True,errors="ignore")
    cash_mask=out["mxb"].item.str.contains("pensions paid",regex=False)
    out["mxb"]["recipient_bn"]=out["mxb"].bn
    out["mxb"]["fiscal_bn"]=out["mxb"].bn
    out["mxb"].loc[cash_mask,"fiscal_bn"]*=public_pension_share
    for end in ("low","high"):
        got=ch.loc[["fiscal","displaced_beneficiaries","wages"],f"bn_{end}"].sum()
        err=abs(got-ch.loc["main_case",f"bn_{end}"])
        gate(err<=1e-6,"cash_registry_closure",end=end,error_bn=err)
        checks[f"registry_{end}"]=err
    out["pension_meta"]=dict(**mode,public_pension_share=public_pension_share,
        source_funding_status="[UNVERIFIED] all-public P032 proxy" if public_pension_share==1 else "[INFERENCE] P032 public-funding sensitivity",
        cash_oracle_bn=cash_raw["oracle_bn"],full_accrual_status="[BLOCKED] missing Mexico actuarial histories",
        financing=financing,checks=checks,cells_sha256=hashlib.sha256(body).hexdigest(),
        source_reads=deepcopy(artifact["sources"]), artifact_key=artifact_key,artifact_path=record["path"],
        mexico_split_requires="consume fiscal_bn on saved-budget posting and recipient_bn on group valuation posting")
    out["pension_cash_adapter"]=out["pension_meta"]
    return out


def private_cash_inputs(I):
    """Cash counterpart for private-gain reporting; no earned Part-A addon.

    Cash Medicare value is already in the public-services-inclusive recipient row.
    Current Social Security cash can be disclosed beside wage compensation, but
    neither is labelled as a new promise earned during 2024.
    """
    gate(I.get("pension_basis")=="matched_cash", "private_cash_basis_required")
    v=I["vgen"]
    from beside_extra import WAGE_TAX_LINES
    mean=lambda mask,col: v[mask].groupby(["generation","end"])[col].sum().groupby(level="generation").mean()
    tax=mean(v.cls.eq("tax"),"V_central_bn")
    wage=mean(v.cls.eq("tax") & v.line.isin(WAGE_TAX_LINES),"V_central_bn")
    ss=mean(v.line.eq("social_security"),"V_central_bn")
    medical=mean(v.line.eq("medicare"),"V_central_bn")
    return {g:dict(us_taxes_bn=float(tax[g]),us_wage_taxes_bn=float(wage[g]),
                   social_security_cash_bn=float(ss[g]),medicare_cash_value_bn=float(medical[g]),
                   earned_pension_addon_bn=0.0,pension_basis="matched_cash") for g in ("G1","G2","G3+")}


def verify_artifact(case):
    """Deterministic package-cell replay; runtime measurements only go to stdout."""
    if case == "oct16":
        from v9_artifact import run
        return run()
    import resource
    import subprocess
    import tempfile
    import time
    pins=json.loads((HERE/"inputs/pension_cash_pins.json").read_text())["artifacts"]
    gate(case+"_cash" in pins,"cash_source_artifact_missing",case=case)
    record=pins[case+"_cash"]
    started=time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="world-cash-") as temporary:
        command=["node",str(HERE/"pension_cash_cells.cjs"),"--historical-probe","--case",case,"--out-dir",temporary]
        result=subprocess.run(command,capture_output=True,text=True)
        gate(result.returncode==0,"cash_source_replay_failed",returncode=result.returncode,stderr=result.stderr)
        got=(Path(temporary)/"pension-cash-cells.json").read_bytes()
        expected=read_artifact(HERE/record["path"])
        gate(got==expected,"cash_source_replay_bytes_changed",actual_sha256=hashlib.sha256(got).hexdigest(),
             expected_sha256=record["sha256"])
    sys.path.insert(0,str(HERE.parent/"scripts"))
    from memory_budget import require_within_budget
    print(json.dumps(dict(status="IDENTICAL",case=case,sha256=record["sha256"],
                          seconds=time.perf_counter()-started,physical_peak_bytes=require_within_budget("cash artifact verification"),
                          child_peak_rss_bytes=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                          child_memory_note="child RSS is reported; no gate on RSS")))


if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--case",default="oct15")
    parser.add_argument("--verify-artifact",action="store_true",required=True)
    args=parser.parse_args()
    verify_artifact(args.case)
