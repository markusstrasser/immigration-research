"""Live oct16 fiscal/social pairing, reusing explicit channel source contracts.

Native-First: the existing named stack evaluator, own calibration records and
source-v8 quantity-price bridge; historical output files are immutable inputs.
"""
from __future__ import annotations
import ast
import copy
import csv
import hashlib
import importlib.util
from functools import lru_cache
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent


def require(ok, message):
    if not ok:
        raise ValueError("[BLOCKED] oct16 social pairing: " + message)


@lru_cache(maxsize=1)
def load_transport():
    """Bind this lane's formula despite foreign modules added to sys.path."""
    path = HERE / "v9_transport.py"
    spec = importlib.util.spec_from_file_location("oct16_social_transport", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    require(Path(module.__file__).resolve() == path.resolve() and
            callable(getattr(module, "build_roads", None)), "own road transport module")
    return module


def added_social(old_meta, payload, R):
    """Own observed age weights; conditional source missing-person ages/tenure prices.

    The source item16 changes native minors only. Its own observed ages locate
    the change; coverage keeps each generation's source five-year minor shape.
    Item17's fixed-count tenure changes consumption intensity, not head counts.
    """
    out = R.v8_added_social(old_meta)
    meta = payload["meta"]
    sys.path.insert(0, str(FISCAL / "world_ledger_2026_09_27"))
    from population_basis import reweight
    spec = importlib.util.spec_from_file_location("oct16_social_frame", FISCAL / "distribution_weights_2026_09_23/distribute.py")
    B = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(B)
    d = B.load_cps()
    # reweight validates the loader's display calibration, then restores its
    # declared production weights before row4; do not reset one side first.
    def gate(name, ok, **detail):
        require(ok, name + " " + str(detail))
    d = reweight(d, B.PATHS["cps"], gate, "lineage")
    sys.path.insert(0, str(FISCAL / "closed_budget_2026_10_06"))
    from households import age_tilted
    from calibrated_frame import complete_calibrated
    old_weights = age_tilted(d, FISCAL / "main_case_2026_10_16/derived/corrections.json")
    old_target = d.target.to_numpy(copy=True)
    weights, target, construction = complete_calibrated(d, old_weights, old_target, payload, gate, coverage=False)
    delta = np.where(target, weights, 0.)-np.where(old_target, old_weights, 0.)
    age = d.A_AGE.to_numpy()
    scopes = {"all":np.ones(len(d), bool), "5_plus":age>=5, "5_17":(age>=5)&(age<18), "18_plus":age>=18}
    located_delta = {s:float(delta[m].sum()) for s,m in scopes.items()}
    # The crime rows' offender scope (crime_senders): the victim lane's population share is of people aged 12+.
    located_12_plus = float(delta[age>=12].sum())
    old_completion = out["people"]["completion_by_scope"]
    cov = json.loads((FISCAL / "coverage_bound_2026_10_14/derived/coverage_bound_oct15.json").read_text())["sets"]["set"]
    bands = {}
    cov_scope = {s:0. for s in scopes}
    for g, by_age in cov["implied_net_missing_people_by_age_band"].items():
        if g == "added":
            continue
        minor_delta = meta["native_minor_calibration"]["coverage_people_change_by_generation"].get(g, 0.)
        minor = sum(n*(3/5 if b=="15-19" else 1.) for b,n in by_age.items() if b in ("0-4","5-9","10-14","15-19"))
        require(minor>0 or abs(minor_delta)<1e-8, "coverage native-minor age support")
        for scope in scopes:
            if scope == "18_plus":
                change = 0.
            elif scope == "all":
                change = minor_delta
            else:
                change = minor_delta*(minor-by_age.get("0-4",0.))/minor if minor else 0.
            cov_scope[scope] += R.scope_people(by_age,scope)+change
        for b,n in by_age.items():
            child_share = 3/5 if b=="15-19" else float(b in ("0-4","5-9","10-14"))
            bands[b] = bands.get(b,0.)+n+(n*child_share*minor_delta/minor if minor else 0.)
    # Native calibration affects minors; never spill the15–17 change into18–19
    # merely because the source reports both in one five-year band.
    require(abs(cov_scope["all"]-sum(construction["coverage_people"].values()))<1e-4, "calibrated coverage count")
    for end in ("low","high"):
        for key,scope in R.V8_KEY_SCOPE.items():
            out["shares"][end][key] = (located_delta[scope]+cov_scope[scope])/out["people"]["union_by_scope"][scope]
    # At pre-item18 prices these signed receipt changes are a consumption-key
    # proxy. A narrower taxable basket is not lower physical consumption.
    source = FISCAL / "count_composition_r5_2026_10_15/derived/line_parts_set.csv"
    count = pd.read_csv(source)
    for end in ("low","high"):
        rows = count[(count.scenario=="joint") & (count.end==end) & (count.source_side=="receipt") & count.source_line.isin(R.CONSUMPTION_LINES)]
        change = -float(rows.change_bn.sum())
        out["shares"][end]["consumption"] += change/out["union_consumption_keyed_receipts_bn"]
    # Newly included completion and newly excluded calibrated records also
    # leave/return to the exchangeable outsider receiver pool.
    frames = {r["count"]:float(r["row4"]) for r in csv.DictReader((FISCAL / "population_basis_2026_09_29/derived/frame_counts.csv").open())}
    for scope in ("all","18_plus","5_17"):
        outside = frames[f"cps_all_civilian|{scope}"]-frames[f"union|{scope}"]
        out["completion_receiver_share"][scope] = located_delta[scope]/outside
    out["people"].update(coverage=cov_scope["all"], coverage_by_scope=cov_scope,
                         located_change_by_scope=located_delta, calibrated_complete=meta["population_v9"]["with_coverage"],
                         located_change_12_plus=located_12_plus)
    out["native_calibration"] = construction
    out["rule"] = added_social.__doc__
    out["sources_sha256"][R.rel(source)] = hashlib.sha256(source.read_bytes()).hexdigest()
    return out


BUSINESS = FISCAL / "business_crime_2026_10_21/derived"
BUSINESS_SUMMARY_SHA256 = "2d41773a36bea2c81edbb4ec28dfa2c77a70fcdcee76458e09c539ac086f9d83"


def crime_rows(doc, added, R):
    """The business-crime row, the commercial-security row and the crime rows' terms for the people v9 adds.

    Senders. The victim lane gives the union Hispanic-offender incidents in proportion to its CPS share of Hispanics
    aged 12+ (P7 puts that share on row 4). National incident counts include offences by people the Census misses,
    and the CPS share carries the same undercount in its numerator and denominator, so the coverage people's
    offending is already in the union's rows. The completion reporters are CPS Hispanics outside the union, so their
    share went to outsiders, and item 16 moves native minors between the union and other Hispanics. Their change in
    the union's count aged 12+ is the crime rows' sender share [ASSUMPTION: the lane's equal-rate population share].
    Payers. The security and business rows also carry the group's payment share. Every person v9 adds pays, at the
    consumption key's share, and item 11 moves its consumption to the stayers.
    Commercial security. P7 charges businesses' security at offending x outside-victim share x (1 - payment share).
    A business guards against offending at its premises whoever the offender's other victims are, and it passes the
    cost to purchasers, as the business-crime row passes its losses; the part P7 leaves out, offending x (1 - outside
    share) x (1 - payment share), is its own row. Outsiders' fear residual is priced on outside victims only, so this
    spending has no counterpart there and P7's fear row is unchanged [FRAMING-SENSITIVE].
    """
    path = BUSINESS / "summary.json"
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    require(digest == BUSINESS_SUMMARY_SHA256, "stale business-crime summary " + digest)
    pairing = json.loads(path.read_text())["pairing"]
    printed = {r["end"]: r for r in csv.DictReader((BUSINESS / "summary.csv").open()) if r["arm"] == "central"}
    p7, keys = doc["p7_crime"], doc["lineage_social_rows"]["keys"]
    frame = {r["count"]: float(r["row4"]) for r in csv.DictReader((FISCAL / "population_basis_2026_09_29/derived/frame_counts.csv").open())}
    delta = added["people"]["located_change_12_plus"] / frame["union|12_plus"]
    tree = ast.parse((FISCAL / "social_costs_unpriced_2026_09_28/items.py").read_text())
    phis = [ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == "PHI" for t in n.targets)]
    require(len(phis) == 1, "one PHI declaration in the P7 items module")
    phi = phis[0]["central"]
    terms, gross, levels = {}, {}, {"business_crime": {}, "commercial_security_member_victims": {}}
    for end in ("low", "high"):
        q = p7["response_parameters"][end]
        k, r = q["added_offending_share"], p7["recipient_shares"]["victims"]
        require(abs(k - keys[f"{end}_end"]["justice_use_raw_coding" if end == "low" else "justice_use"]) < 1e-15, "P7 crime key")
        res, com = q["national_spending"]["residential"], q["national_spending"]["commercial"]
        out, off_u, p_u, p = q["outside_share_before_boundary"] * (1 - r), q["offending_share_union"], q["payment_share_union"], q["payment_share_lineage"]
        b = pairing["ends"][end]
        require(abs(b["crime_key"] - k) < 1e-15 and abs(pairing["payment_share_lineage"] - p) < 1e-15
                and abs(pairing["payment_share_union"] - p_u) < 1e-15, "business crime on the pairing's keys")
        require(abs(b["net_bn"] - float(printed[end]["net_with_without_bn"])) < 5e-7
                and abs(b["gross_bn"] - float(printed[end]["gross_forward_bn"])) < 5e-7, "business summary.json against summary.csv")
        lines, direct = b["loss_lines"].values(), sum(b["direct_union_bn"].values())

        def business(g, pay):
            return sum(x["L_bn"] * (x["S_union"] * g - pay) for x in lines) + direct * g
        def security(o, pay):
            return res * o * out + com * o * out * (1 - pay) - com * pay * (1 - o)
        def forward(o, pay):
            return (res + com * (1 - pay)) * o * out
        def commercial(o, pay):
            return com * o * (1 - out) * (1 - pay)
        lineage = p7["lineage_crime_rows"][end]
        o0, o9 = off_u * (1 + k), off_u * (1 + k + delta)
        require(abs(business(1 + k, p) - b["net_bn"]) < 1e-9, f"business net from its parts ({end})")
        require(abs(security(o0, p) - lineage["private_security"]) < 1e-9, f"P7 lineage security from its parameters ({end})")
        wtp = lineage["fear_avoidance"] / phi + forward(o0, p)
        require(lineage["fear_avoidance"] > 0, "P7 fear residual above its floor")
        def fear(o, pay):
            return phi * max(0.0, wtp * o / o0 - forward(o, pay))
        c9, f11 = added["shares"][end]["consumption"], added["item11_consumption_factor"]
        pa, p9 = p + p_u * c9, p + p_u * (c9 + f11)
        rules = dict(private_security=security, fear_avoidance=fear, commercial_security_member_victims=commercial,
                     business_crime=lambda o, pay: business(o / off_u, pay))
        for item, f in rules.items():
            terms.setdefault(item, {})[end] = dict(added_people_bn=f(o9, pa) - f(o0, p), item11_consumption_bn=f(o9, p9) - f(o9, pa))
        levels["business_crime"][end] = b["net_bn"]
        levels["commercial_security_member_victims"][end] = commercial(o0, p)
        gross[end] = b["gross_bn"]
    contract = lambda valuation, overlaps: dict(comparator="with_without", beneficiary_population="residents_outside_lineage",  # noqa: E731
                                                valuation_basis=valuation, overlap_set=overlaps)
    extra = [dict(item="business_crime", level_by_end_bn=levels["business_crime"], key=R.CRIME,
                  share_by_end={e: p7["response_parameters"][e]["added_offending_share"] for e in ("low", "high")},
                  contract=dict(contract("loss_pass_through_net", ["victims", "property_crime", "private_security"]),
                                source=R.rel(path), gross_beside_bn=gross,
                                decision="decisions/2026-10-21-business-crime-in-pairing.md")),
             dict(item="commercial_security_member_victims", level_by_end_bn=levels["commercial_security_member_victims"], key=R.CRIME,
                  share_by_end={e: p7["response_parameters"][e]["added_offending_share"] for e in ("low", "high")},
                  contract=dict(contract("resource_spending", ["private_security", "fear_avoidance", "business_crime"]),
                                source="p7_crime.response_parameters", decision="decisions/2026-10-21-business-crime-in-pairing.md"))]
    senders = dict(share_12_plus={e: delta for e in ("low", "high")}, rows=terms,
                   people_12_plus=added["people"]["located_change_12_plus"], union_12_plus_row4=frame["union|12_plus"],
                   rule=crime_rows.__doc__)
    return extra, senders, {R.rel(path): digest}


def main(args):
    import real_costs_totals as R
    out = args.out_dir
    bands = json.loads((out / "band_variants.json").read_text())
    summary = json.loads((FISCAL / "main_case_2026_10_16/derived/summary.json").read_text())
    require(summary["v9"]["status"]=="adopted", "adopted case required")
    for path,digest in bands["sources_sha256"].items():
        require(hashlib.sha256((FISCAL/path).read_bytes()).hexdigest()==digest, "stale band source "+path)
    old = json.loads((HERE / "derived/oct15/real_costs_totals.json").read_text())
    old_meta = json.loads((HERE / "derived/oct15/band_variants.json").read_text())
    payload = json.loads((FISCAL / "main_case_2026_10_16/derived/corrections.json").read_text())
    doc = copy.deepcopy(old)
    inherited_fields = ("congestion_by_band_end_bn", "social_items_in_the_social_rows", "beside_the_central_total", "target_population_m")
    doc["inherited_oct15"] = {key: doc.pop(key) for key in inherited_fields}
    doc.update(case="oct16", columns=["oct16"], sources_sha256=dict(bands["sources_sha256"]))
    doc["per_member_population_m"] = {"oct16":payload["meta"]["population_v9"]["with_coverage"]/1e6}
    doc["target_population_m"] = doc["per_member_population_m"]["oct16"]
    for field in ("joint_social_stack","v8_social_environment"):
        doc.pop(field,None)
    rows = []
    baseline_social = {end:sum(r[f"union_{end}_bn"]+r[f"added_{end}_bn"] for r in doc["lineage_social_rows"]["rows"]) for end in ("low","high")}
    for i,end in enumerate(("low","high")):
        before = summary["v9"]["band_bn"][i]+baseline_social[end]
        rows.append(dict(section="7",column="pairing_on_priced_count",item=f"published pairing ({end})",unit="bn",oct16=before,
                         sept24=None,change=None,note="live oct16 fiscal plus source-key social rows"))
        old_fiscal = old["joint_social_stack"]["ends"][end]["fiscal_pairing_bn"]
        doc["without_round1_social_fixes_bn"][end] += summary["v9"]["band_bn"][i]-old_fiscal
    # Count changes' public consumption is located by source, apart from capital.
    sys.path.insert(0, str(FISCAL / "debt_legacy_2026_09_23"))
    from v9_flow import count_parts, load_native_frame
    frame = load_native_frame()
    family = {r["id"]:r["family"] for r in frame["sets"]["cash"]["endpoints"]["low"]["r"]["evaluation"]["spending"]}
    for end in ("low","high"):
        for item in ("native_minor_calibration","coverage_tenure"):
            parts = count_parts(payload,item,end)
            value = sum(r["change_bn"] for r in parts if r["source_side"]=="spending" and family.get(r["source_line"])=="consumption")
            bands["social_resource_account"]["ends"][end]["government_consumption_removed_bn"] += value
    added = added_social(old_meta,payload,R)
    extra, added["crime_senders"], extra_sources = crime_rows(doc, added, R)
    for i, end in enumerate(("low", "high")):
        rows[i]["oct16"] += sum(r["level_by_end_bn"][end] for r in extra)
        rows[i]["note"] += "; business crime (net) and commercial security against offending on members"
    doc["sources_sha256"].update(extra_sources)
    bands["oct16_transport"] = load_transport().build_roads(frame)
    R.apply_v8_environment(rows,doc,bands,summary,args.v8_social_transport,case="oct16",added_override=added,
                           extra_rows=extra)
    env = doc.pop("v8_social_environment")
    env.update(current_fiscal_population=payload["meta"]["population_v9"]["with_coverage"],
               source_vintage="live source bundles verified by named-stack receipts; native count16 and tenure17 at source pre18 physical-consumption prices",
               government_side="removed public consumption at government-average PM intensity; public investment emissions omitted",
               fiscal_resource_label="cash budgets plus displaced aid and explicitly conditional unlocated resources; capital/promise timing separate")
    doc["v9_social_environment"] = env
    doc["joint_social_stack"]["funding"] = "same oct16 conditional H; displaced housing aid is reassigned to beneficiaries, not a budget saving"
    doc["cash_timing_contract"] = "same 2024 physical social effects and current-resource respending; cash replaces only pension fiscal timing, not a future cash forecast"
    doc["cash_pairing_bn"] = {end:doc["joint_social_stack"]["ends"][end]["with_round1_social_fixes_bn"]
                              -summary["v9"]["band_bn"][i]+summary["v9"]["cash_set_bn"][i] for i,end in enumerate(("low","high"))}
    for i,end in enumerate(("low","high")):
        row = doc["joint_social_stack"]["ends"][end]
        require(abs(row["fiscal_pairing_bn"]-summary["v9"]["band_bn"][i])<1e-9,"own set fiscal pairing")
        require(abs(row["with_round1_social_fixes_bn"]-row["fiscal_pairing_bn"]-row["social_rows_bn"])<1e-9,"joint row closure")
        rows.append(dict(rows[0],column="cash_pairing",item=f"published pairing ({end})",oct16=doc["cash_pairing_bn"][end]))
    # Equal-count comparator is built by the separate source-native component helper.
    from average_social_oct16 import build_average_social
    decompositions = {basis:json.loads((FISCAL / "main_case_decomposition_2026_09_29/derived" /
                       ("summary_oct16_cash.json" if basis=="cash" else "summary_oct16.json")).read_text())
                      for basis in ("set","cash")}
    national = {basis:{} for basis in ("set","cash")}
    road = json.loads((FISCAL / "service_response_long_run_2026_09_27/derived/responses.json").read_text())
    road_parts = [r for r in road["lines"]["economic_affairs_services"]["subfunctions"] if r["subfunction"]=="Highways"]
    for basis, decomp in decompositions.items():
        for end in ("low","high"):
            state = decomp["v9"]["state_source_rows"][end]["NNN"]
            scale = state["national_added_people_scale"]
            capital = state["base_capital"]["total_bn"]*scale
            capital += sum(state["changes_bn"].get(k,0.) for k in ("one_rate","college15_rate20_interaction"))
            capital += sum(r["delta_bn"] for r in state["universal_source_rows"] if r.get("kind")=="college_capital")
            P = state["base_production"]["P_bn"]*scale
            fiscal = decomp["parts"][end]["shared"]
            state_spending = state["base_spending"]
            families = {r["id"]:r["family"] for r in state_spending}
            consumption = -sum(r["effect_bn"] for r in state_spending if r["family"]=="consumption")*scale
            consumption += sum(r["delta_bn"] for r in state["universal_source_rows"]
                               if r.get("kind")!="college_capital" and families.get(r.get("source_line",r["line"]))=="consumption")
            national_consumption = sum(r["national_bn"] for r in state_spending if r["family"]=="consumption")
            cap = {r["id"]:r for r in state["base_capital"]["components"]}
            highway = sum(r["national_bn"]*cap["hwy_fed" if r["level"]=="federal" else "hwy_sl"]["response"] for r in road_parts)/sum(r["national_bn"] for r in road_parts)
            national[basis][end] = dict(fiscal_cost_bn=fiscal,current_H_bn=fiscal-capital+P,
                government_consumption_removed_bn=consumption,
                government_consumption_national_bn=national_consumption,highway_response=highway)
    # Physical/current-resource effects use the cash national frame in both sets;
    # earned promises and capital resource charges are never treated as spendable.
    for end in ("low","high"):
        for field in ("current_H_bn","government_consumption_removed_bn","government_consumption_national_bn","highway_response"):
            national["set"][end][field] = national["cash"][end][field]
    absolute_fiscal = {basis:dict(zip(("low","high"),summary["v9"]["band_bn" if basis=="set" else "cash_set_bn"])) for basis in ("set","cash")}
    doc["joint_social_excess_vs_average"] = build_average_social(env["current_social_rows"],national,
        absolute_fiscal_by_basis=absolute_fiscal,population_people=payload["meta"]["population_v9"]["with_coverage"],
        national_people=decompositions["set"]["frame"]["row4"]["NC"],
        congestion_state=load_transport().congestion_setup())
    doc["joint_social_excess_vs_average"]["national_fiscal_inputs"] = national
    # The shared historical evaluator retains its vocabulary for archived routes.
    # Relabel only this live export, leaving earlier keyed outputs byte-identical.
    for row in rows:
        if "note" in row:
            row["note"] = row["note"].replace("v8 fiscal account", "v9 fiscal account").replace(
                "v8 current", "v9 current").replace("v8 added people", "v9 calibrated added people")
    R.require_within_budget("oct16 real-costs totals")
    out.mkdir(parents=True,exist_ok=True)
    with (out/"real_costs_totals.csv").open("w",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator="\n")
        writer.writeheader();writer.writerows(rows)
    (out/"real_costs_totals.json").write_text(json.dumps(doc,indent=1,allow_nan=False)+"\n")
    print("PASS oct16 set/cash pairing",{e:doc["joint_social_stack"]["ends"][e]["with_round1_social_fixes_bn"] for e in ("low","high")},doc["cash_pairing_bn"])
