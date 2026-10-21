"""Harm inside the Mexican-immigrant lineage and to members' families in Mexico, beside the pairing (2024 $).

The fiscal-plus-social pairing prices what the 44.90M lineage costs residents OUTSIDE it and removes
harm members do to members (U->U, U->D, D->D). This lane prices that removed part, and what the pairing's
frame never sees, as BESIDE rows. None of them enters the "cost to other residents" pairing.

Frames
  A, B  whole US population, members included: harm members' conduct imposes on other members.
  C     world frame: effects of members' US presence on their relatives in Mexico, and (C0) the
        counterfactual the world frame needs before A's victims enter it.

Blocks
  A  the in-group counterpart of every pairing row with a defined in-group share: crime victims (homicide
     and non-fatal 12+), property crime, fear/avoidance, private security, PM2.5, road crashes, congestion.
     School disruption is computed and kept out of A's total (no without-world for in-group pupils).
     Rule for a row whose current v9 outside level is L, recipient share r (P7 lineage boundary),
     completion-receiver share c and union-frame in-group-to-outside ratio rho:
         O = L / ((1 - r)(1 - c))      the lineage senders' harm to non-union residents
         in-group = O (1 + rho) - L    [ASSUMPTION: the lineage's senders share the union's in/out mix]
     Crime victims are rebuilt from the victim lane's cells on the pairing's own arm and gated to it.
  B  harm NCVS cannot see inside the group: victims under 12 (NCANDS maltreatment, Peterson et al. 2018
     prices; NIBRS police-recorded non-family violence) and child maltreatment deaths that WONDER does not
     code as assault. Domestic violence 12+ is already inside A's NCVS counts; its share is reported.
  C  families in Mexico: schooling, health and mental health of the left-behind (literature, totals that
     already include remittances; the world ledger carries remittances), and C0, members' homicide risk in
     Mexico against the US.

Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/within_group_harm_2026_10_21/within_group_harm.py
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = FISCAL.parent.parent
OUT = HERE / "derived"
sys.path.insert(0, str(HERE))
import nibrs_children  # noqa: E402

CRIME = FISCAL / "crime_victim_cost_2026_09_23"
P7 = FISCAL / "social_costs_unpriced_2026_09_28/derived/p7_payload.json"
TOTALS = FISCAL / "sept24_propagation_2026_09_24/derived/oct16/real_costs_totals.json"
FRAME = FISCAL / "population_basis_2026_09_29/derived/frame_counts.csv"
PM_ITEMS = FISCAL / "air_pollution_2026_09_28/derived/mortality_items.csv"
CRASH_COMP = FISCAL / "road_crash_externality_2026_09_28/derived/capacity_components_oct15.csv"
CRASH_ITEMS = FISCAL / "road_crash_externality_2026_09_28/derived/capacity_items_oct15.csv"
FARS = FISCAL / "road_crash_externality_2026_09_28/derived/fars_group_2023.json"
UA = FISCAL / "congestion_2026_09_23/derived/ua_exposure.csv"
METRO = FISCAL / "congestion_2026_09_23/derived/metro_distribution.csv"
NIBRS_LANE = FISCAL / "offender_ethnicity_nibrs_2026_09_23/derived/cost_by_offence_nibrs_central.csv"
WDI = FISCAL / "world_ledger_2026_09_27/_cache/mexico"
G2_PREMIUM = FISCAL / "world_ledger_2026_09_27/derived/g2_premium_oct16.csv"
WORLD_ROWS = FISCAL / "world_ledger_2026_09_27/derived/readings_cash_oct16.csv"
CPI = FISCAL / "ncvs_victim_offender_2026_09_18/derived/cpi_u_annual.csv"

POPULATION_M = None            # set from the totals file: the per-member denominator
# Pairing rows with a defined in-group share. The pecuniary and benefit rows (housing gain, scale earnings,
# consumer scale, trade/travel, restaurant variety, volunteering) are prices and transfers whose in-group
# counterparts net to zero inside the whole population; unreimbursed care is a cost shift through payers.
IN_GROUP_ROWS = ("victims", "property_crime", "fear_avoidance", "private_security", "pm25_consumption",
                 "road_crash_externality", "congestion", "school_disruption")
ENDS = ("low", "high")
FOOTING = {"low": "mixed", "high": "custody"}   # the pairing's P7 victim footings at the two case ends
GATES: list[dict] = []
SOURCES: dict[str, str] = {}


def gate(label: str, ok: bool, detail: str = "") -> None:
    GATES.append(dict(gate=label, result="PASS" if ok else "FAIL", detail=detail))
    if not ok:
        raise SystemExit(f"[BLOCKED] {label}: {detail}")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def read(path: Path, role: str):
    """Record a repository input's bytes before reading it."""
    if not path.exists():
        raise SystemExit(f"[BLOCKED] missing input {path}")
    SOURCES[str(path.relative_to(ROOT))] = role
    return path


def rows(path: Path, role: str) -> list[dict]:
    with read(path, role).open() as f:
        return list(csv.DictReader(f))


def write_csv(name: str, table: list[dict]) -> None:
    with (OUT / name).open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(table[0]), lineterminator="\n")
        w.writeheader()
        for r in table:
            w.writerow({k: (f"{v:.12g}" if isinstance(v, float) else v) for k, v in r.items()})


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, read(path, "imported read-only"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------------------------- sources
def pinned_texts() -> dict[str, str]:
    pins = json.loads(read(HERE / "inputs/pins.json", "pins").read_text())
    texts = {}
    for p in pins["files"]:
        path = HERE / p["path"]
        if not path.exists():
            raise SystemExit(f"[BLOCKED] missing pinned source {p['path']} (restore from {p['url']})")
        gate(f"pin {p['id']}", digest(path) == p["sha256"], p["path"])
        if path.suffix == ".txt":
            texts[p["id"]] = path.read_text(errors="replace")
    return texts


def normalize(s: str) -> str:
    s = re.sub(r"(?<=\d),(?=\d{3})", "", s)
    return re.sub(r"\s+", " ", s).strip()


def transcribed(texts: dict[str, str]) -> dict[str, float]:
    """Every number enters through a quote that must appear in its pinned text."""
    norm = {k: normalize(v) for k, v in texts.items()}
    values = {}
    for r in rows(HERE / "inputs/transcribed.csv", "transcriptions"):
        quote = normalize(r["quote"])
        gate(f"quote {r['key']}", quote in norm[r["source"]], r["quote"][:60])
        nums = [float(x.replace("−", "-")) for x in re.findall(r"[−-]?\d+(?:\.\d+)?", quote.replace("$", ""))]
        pick = r["pick"]
        if pick.startswith("sum:"):
            a, b = (int(x) for x in pick[4:].split("-"))
            values[r["key"]] = float(sum(nums[a:b + 1]))
        else:
            values[r["key"]] = nums[int(pick)]
    return values


# ---------------------------------------------------------------------------------------------- frame
def case_inputs() -> dict:
    global POPULATION_M
    doc = json.loads(read(TOTALS, "v9 pairing totals (oct16)").read_text())
    p7 = json.loads(read(P7, "P7 crime payload").read_text())
    gate("pairing totals are the live case", doc["case"] == "oct16")
    gate("P7 payload is DOT uniform", p7["vsl_standard"] == "dot_uniform")
    live = json.loads(read(FISCAL / "live_case.json", "live case declaration").read_text())
    gate("live_case.json names oct16", "oct16" in json.dumps(live), json.dumps(live)[:120])
    POPULATION_M = doc["per_member_population_m"]["oct16"]
    env = doc["v9_social_environment"]
    current = {r["item"]: r["total_by_end_bn"] for r in env["current_social_rows"]}
    # The members' own-conduct level of each row: the v8 parts (P7/union level, the added people, item 11's
    # consumption shift, completion receivers). PM2.5's current row also nets the re-spending of the budget
    # saving, which happens only in the world without the lineage and so has no in-group counterpart.
    level = {}
    for end in ("low", "high"):
        parts = env["variants"]["central"]["parts"][end]
        for item, p in parts["v8_added_by_item"].items():
            if item not in IN_GROUP_ROWS:
                continue
            own =p["level_bn"] + p["added_people_bn"] + p["item11_consumption_bn"] + p["completion_receivers_bn"]
            level.setdefault(item, {})[end] = own
            other = parts["terms"]["pm_respending"] if item == "pm25_consumption" else 0.0
            gate(f"own-conduct level + re-spending = current row ({item}, {end})", abs(own + other - current[item][end]) < 1e-9,
                 f"{own:.9f} + {other:.9f} / {current[item][end]:.9f}")
    keys = doc["lineage_social_rows"]["keys"]
    frame = {r["count"]: (float(r["published"]), float(r["row4"])) for r in rows(FRAME, "population frame")}
    factor = (frame["union|12_plus"][1] / frame["cps_hispanic_civilian|12_plus"][1]
              / (frame["union|12_plus"][0] / frame["cps_hispanic_civilian|12_plus"][0]))
    # The people v9 adds as crime senders (completion and item 16, aged 12+) and as payers (consumption key, item 11):
    # the pairing's crime_senders rule (sept24_propagation_2026_09_24/v9_totals.py crime_rows).
    senders = env["v8_added_social"]["crime_senders"]
    payers = {end: env["v8_added_social"]["shares"][end]["consumption"] + env["v8_added_social"]["item11_consumption_factor"]
              for end in ENDS}
    return dict(doc=doc, p7=p7, level=level, keys=keys, frame=frame, factor=factor,
                recipient=p7["recipient_shares"], completion=env["v8_added_social"]["completion_receiver_share"],
                added=env["v8_added_social"]["shares"], senders=senders["share_12_plus"], payers=payers)


def scope(item: str) -> str:
    return "5_17" if item == "school_disruption" else "18_plus" if item == "formal_volunteering_outside_group" else "all"


def keep(case: dict, item: str) -> float:
    """(1 - r)(1 - c): the share of the lineage senders' former-outsider harm still outside the v9 lineage."""
    return (1 - case["recipient"][item]) * (1 - case["completion"][scope(item)])


def ingroup_by_ratio(case: dict, item: str, end: str, rho: float) -> dict:
    final = case["level"][item][end]
    pre = final / keep(case, item)
    return dict(final_outside_bn=final, senders_to_nonunion_bn=pre, union_frame_ingroup_bn=pre * rho,
                boundary_bn=pre - final, ingroup_bn=pre * (1 + rho) - final)


# ---------------------------------------------------------------------------------------------- A: victims
def victim_cells(standard: str, footing: str, rate: float = 0.0) -> list[dict]:
    sel = [r for r in rows(CRIME / "derived/mortality_detail.csv", "victim cells (crime lane)")
           if r["footing"] == footing and r["vsl_standard"] == standard
           and float(r["real_discount_rate"]) == rate and r["missing_age_arm"] == "central"]
    gate(f"victim cells {footing}/{standard}/{rate}", len(sel) == 20, str(len(sel)))
    return sel


def residual_unit(offence: str, unit: float, cpi: dict) -> float:
    """P7's fear WTP residual per victim at the central arm (items.py: Cohen 2004 WTP, 2000 $, CPI-U)."""
    wtp2000 = {"Murder": 9.7e6, "Rape/sexual assault": 237e3, "Aggravated assault": 70e3, "Armed robbery": 232e3}
    to2024 = cpi[2024] / cpi[2000]
    if offence in ("Murder", "Rape/sexual assault", "Aggravated assault"):
        return max(0.0, wtp2000[offence] * to2024 - unit)
    if offence == "Robbery":
        return min(max(0.0, 0.45 * (wtp2000["Armed robbery"] * to2024 - unit)), unit)
    return 0.0                                     # simple assault: zero at the central arm


def victims_block(case: dict, cpi_items: dict) -> tuple[list[dict], list[dict], dict]:
    p7, keys, F = case["p7"], case["keys"], case["factor"]
    r_v, c_all = case["recipient"]["victims"], case["completion"]["all"]
    m_nibrs = [r for r in rows(NIBRS_LANE, "NIBRS lane victim cells") if r["arm"] == "victim-conditional, SHR-calibrated"]
    gate("NIBRS preferred arm has four non-fatal offences", len(m_nibrs) == 4)
    nf_in_n = sum((float(r["group_victimisations"]) - float(r["outside_victims"])) * float(r["unit_full"]) for r in m_nibrs)
    nf_out_n = sum(float(r["outside_victims"]) * float(r["unit_full"]) for r in m_nibrs)
    rho_nf_nibrs = nf_in_n / nf_out_n
    detail, arms, summary = [], [], {}
    for end in ENDS:
        a = keys[f"{end}_end"][("justice_use_raw_coding", "justice_use")[ENDS.index(end)]]
        gate(f"sender key {end} matches P7", abs(a - p7["response_parameters"][end]["added_offending_share"]) < 1e-12)
        d9 = case["senders"][end]
        lin = F * (1 + a + d9)
        cells = victim_cells("dot_uniform", FOOTING[end])
        out_union = sum(float(r["cost_full"]) for r in cells) / 1e9 * F
        gate(f"union outside victims reproduce P7 ({end})", abs(out_union - p7["union_crime_rows"][end]["victims"]) < 1e-9,
             f"{out_union:.9f}")
        gate(f"lineage senders' outside victims reproduce P7 ({end})",
             abs(out_union * (1 + a) - p7["lineage_crime_rows_before_boundary"][end]["victims"]) < 1e-9,
             f"{out_union * (1 + a):.9f}")
        pre = out_union * (1 + a + d9)
        final = case["level"]["victims"][end]
        gate(f"v9 victims row = senders x (1-r)(1-c) ({end})", abs(pre * keep(case, "victims") - final) < 1e-9,
             f"{pre * keep(case, 'victims'):.9f} / {final:.9f}")
        bshare = 1 - keep(case, "victims")
        tot = dict(full=0.0, tangible=0.0, deaths=0.0, nonfatal=0.0, fear_wtp=0.0, nf_out=0.0)
        for r in cells:
            g, o = float(r["group_victimisations"]), float(r["outside_victims"])
            uf, ut = float(r["unit_full"]), float(r["unit_tangible"])
            n_in = (g - o) * lin + o * lin * bshare             # U->U and D->U, plus U->D and D->D
            detail.append(dict(end=end, footing=FOOTING[end], block=r["block"], victim=r["victim"], offence=r["offence"],
                               ingroup_victims=n_in, unit_full_usd=uf, unit_tangible_usd=ut,
                               ingroup_full_bn=n_in * uf / 1e9, ingroup_tangible_bn=n_in * ut / 1e9))
            tot["full"] += n_in * uf / 1e9
            tot["tangible"] += n_in * ut / 1e9
            tot["deaths" if r["block"] == "homicide" else "nonfatal"] += n_in
            tot["fear_wtp"] += n_in * residual_unit(r["offence"], uf, cpi_items) / 1e9
            if r["block"] != "homicide":
                tot["nf_out"] += o * lin * uf / 1e9
        gate(f"in-group victims = all-victim harm - outside row ({end})",
             abs(tot["full"] - (sum(float(r["group_victimisations"]) * float(r["unit_full"]) for r in cells) / 1e9 * lin - final)) < 1e-9)
        summary[end] = dict(tot, sender_key=a, v9_sender_share=d9, final_outside_bn=final, boundary_bn=pre - final)
        arms.append(dict(item="victims", arm="central (NCVS victim mix, tract m 0.786, DOT $13.7M)", end=end, value_bn=tot["full"]))
        arms.append(dict(item="victims", arm="tangible only (medical, earnings, property)", end=end, value_bn=tot["tangible"]))
        # NIBRS police-recorded victim mix: the pairing's outside count, police records' in/out ratio.
        hom_in = sum(d["ingroup_full_bn"] for d in detail if d["end"] == end and d["block"] == "homicide")
        nibrs = hom_in + tot["nf_out"] * (rho_nf_nibrs + bshare)
        summary[end] = dict(summary[end], nibrs_nonfatal_bn=tot["nf_out"] * (rho_nf_nibrs + bshare),
                            ncvs_nonfatal_bn=tot["full"] - hom_in)
        arms.append(dict(item="victims", arm=f"NIBRS police-recorded victim mix (non-fatal in/out {rho_nf_nibrs:.3f})",
                         end=end, value_bn=nibrs))
        # In-group share m of Hispanic victims.
        hisp = [r for r in cells if r["victim"] == "Hispanic"]
        m_c = 1 - sum(float(r["outside_victims"]) for r in hisp if r["block"] == "homicide") / \
            sum(float(r["group_victimisations"]) for r in hisp if r["block"] == "homicide")
        for m_alt, label in ((0.744, "county exposure 0.744"), (0.586, "national share 0.586"), (1.0, "every Hispanic victim in-group")):
            delta = sum(float(r["group_victimisations"]) * (m_alt - m_c) * float(r["unit_full"]) for r in hisp) / 1e9 * lin
            arms.append(dict(item="victims", arm=f"m at {label}", end=end, value_bn=tot["full"] + delta))
        for rate in (0.0, 0.03):
            ly = victim_cells("dot_life_years", FOOTING[end], rate)
            v = sum(((float(r["group_victimisations"]) - float(r["outside_victims"])) * lin
                     + float(r["outside_victims"]) * lin * bshare) * float(r["unit_full"]) for r in ly) / 1e9
            arms.append(dict(item="victims", arm=f"life-years, {rate:.0%} real (beside)", end=end, value_bn=v))
        summary[end]["m_central"] = m_c
    summary["rho_nonfatal_nibrs"] = rho_nf_nibrs
    return detail, arms, summary


def security_fear(case: dict, summary: dict) -> tuple[dict, list[dict]]:
    """P7's response rule with members as the victims and payers; gated by reproducing P7's lineage rows."""
    p7 = case["p7"]
    phi = {"low": 0.25, "central": 0.5, "high": 1.0}
    out, arms = {}, []
    for end in ENDS:
        rp = p7["response_parameters"][end]
        a = summary[end]["sender_key"]
        res, com = rp["national_spending"]["residential"], rp["national_spending"]["commercial"]
        off = rp["offending_share_union"] * (1 + a)
        out_l = rp["outside_share_before_boundary"] * (1 - rp["recipient_share"])
        pay = rp["payment_share_lineage"]
        forward = (res + com * (1 - pay)) * off * out_l
        security = forward - com * pay * (1 - off)
        gate(f"P7 lineage security reproduced ({end})", abs(security - p7["lineage_crime_rows"][end]["private_security"]) < 1e-9,
             f"{security:.9f}")
        # Outsiders' WTP residual: rebuild from the victim cells on the P7 lineage boundary (r only).
        cells = victim_cells("dot_uniform", FOOTING[end])
        lin = case["factor"] * (1 + a)
        wtp_out = sum(float(r["outside_victims"]) * lin * (1 - rp["recipient_share"])
                      * residual_unit(r["offence"], float(r["unit_full"]), CPI_ITEMS) for r in cells) / 1e9
        fear = phi["central"] * max(0.0, wtp_out - forward)
        gate(f"P7 lineage fear reproduced ({end})", abs(fear - p7["lineage_crime_rows"][end]["fear_avoidance"]) < 1e-9,
             f"{fear:.9f}")
        # The members' side on the v9 lineage: its senders and payers include the people v9 adds.
        off = rp["offending_share_union"] * (1 + a + summary[end]["v9_sender_share"])
        pay = pay + rp["payment_share_union"] * case["payers"][end]
        in_share = 1 - rp["outside_share_before_boundary"] * keep(case, "fear_avoidance")
        sec_in = res * off * in_share + com * off * pay
        fear_in = {k: v * max(0.0, summary[end]["fear_wtp"] - sec_in) for k, v in phi.items()}
        out[end] = dict(security_bn=sec_in, fear_bn=fear_in["central"], in_share=in_share, offending_share=off)
        arms += [dict(item="fear_avoidance", arm=f"phi {k} {v}", end=end, value_bn=fear_in[k]) for k, v in phi.items()]
        arms.append(dict(item="private_security", arm="central (members' residential + members' purchases)", end=end, value_bn=sec_in))
        arms.append(dict(item="private_security", arm="residential only", end=end, value_bn=res * off * in_share))
    return out, arms


def property_rho() -> float:
    prop = [r for r in rows(CRIME / "derived/property_proxy.csv", "property proxy") if r["price_set"] == "miller2021"]
    i = sum((float(r["group_offences"]) - float(r["outside_offences"])) * float(r["unit_victim_cost"]) for r in prop)
    o = sum(float(r["outside_offences"]) * float(r["unit_victim_cost"]) for r in prop)
    return i / o


# ---------------------------------------------------------------------------------------------- A: environment
def pm_block(case: dict) -> tuple[dict, list[dict]]:
    pm = [r for r in rows(PM_ITEMS, "PM2.5 mortality items") if r["item"] in ("pm25_consumption_mortality", "pm25_consumption_mortality_vsly")
          and r["population_basis"] == "row4"]
    uni = [r for r in pm if r["valuation"] == "dot_uniform" and float(r["real_discount_rate"]) == 0]
    gate("one row4 uniform PM row", len(uni) == 1)
    uni = uni[0]
    sigma = float(uni["self_share"])
    union_part = case["doc"]["v9_social_environment"]["variants"]["central"]["parts"]["low"]["v8_added_by_item"]["pm25_consumption"]["union_part_bn"]
    gate("v9 PM union part = row4 uniform central x (1 - r)",
         abs(float(uni["central_bn"]) * (1 - case["recipient"]["pm25_consumption"]) - union_part) < 1e-6,
         f"{float(uni['central_bn']):.6f} / {union_part:.6f}")
    rho = sigma / (1 - sigma)
    out, arms = {}, []
    for end in ENDS:
        r = ingroup_by_ratio(case, "pm25_consumption", end, rho)
        out[end] = r
        arms.append(dict(item="pm25_consumption", arm=f"central (mortality-weighted self-share {sigma:.4f})", end=end, value_bn=r["ingroup_bn"]))
        for lab, key in (("CRF grid low", "low_bn"), ("CRF grid high", "high_bn")):
            arms.append(dict(item="pm25_consumption", arm=lab, end=end, value_bn=r["ingroup_bn"] * float(uni[key]) / float(uni["central_bn"])))
        for vs in pm:
            if vs["valuation"] == "dot_life_years":
                arms.append(dict(item="pm25_consumption", arm=f"life-years, {float(vs['real_discount_rate']):.0%} real (beside; outsiders' age ratio)",
                                 end=end, value_bn=r["ingroup_bn"] * float(vs["central_bn"]) / float(uni["central_bn"])))
        s_hi = 0.193                                  # the lane's pre-correction exposure self-share (RESULT table)
        arms.append(dict(item="pm25_consumption", arm="exposure self-share 0.193 (pre mortality weighting)", end=end,
                         value_bn=ingroup_by_ratio(case, "pm25_consumption", end, s_hi / (1 - s_hi))["ingroup_bn"]))
    return dict(sigma=sigma, rho=rho, ends=out), arms


def crash_block(case: dict, m_mex: float) -> tuple[dict, list[dict]]:
    fars = json.loads(read(FARS, "FARS group parameters").read_text())
    q = sum(float(r["acs_group_vehicle_minutes"]) * float(r["phi_commute_route"]) for r in ua_rows()) / \
        sum(float(r["acs_group_vehicle_minutes"]) for r in ua_rows())
    gate("self-exposure q reproduces the crash lane's 0.299", abs(q - 0.29879) < 1e-4, f"{q:.5f}")
    tp = {r["group"]: r for r in rows(CRIME / "derived/target_population_cps2025.csv", "CPS target population")}
    mex_of_hisp = float(tp["union_hispanic"]["all_ages"]) / float(tp["cps_hispanic_civilian"]["all_ages"])
    h = fars["hispanic_share_of_known_origin_pedestrian_deaths"] * mex_of_hisp
    sv_pax, pax_in = fars["single_vehicle_passenger_share_of_occupant_deaths"], fars["passengers_killed_with_killed_hispanic_driver_hispanic_share"]
    e_sv = 0.04                                       # crash lane central external share of single-vehicle losses
    comps = [r for r in rows(CRASH_COMP, "crash capacity components") if r["valuation"] == "dot_uniform"
             and float(r["real_discount_rate"]) == 0 and r["arm"] == "multivehicle_only"]
    items = [r for r in rows(CRASH_ITEMS, "crash capacity items") if r["valuation"] == "dot_uniform"
             and float(r["real_discount_rate"]) == 0 and r["arm"] == "multivehicle_only" and r["population"] == "union"]
    out, arms = {}, []

    def rho_for(c, q_, m_):
        parts = {"mv_nonfatal": q_ / (1 - q_), "mv_fatal": q_ / (1 - q_), "nonmotorist": h / (1 - h),
                 "single_vehicle": sv_pax * pax_in * m_ / e_sv}
        tot = sum(float(c[k]) for k in parts)
        return sum(float(c[k]) * parts[k] for k in parts) / tot, tot

    for end in ENDS:
        c = [r for r in comps if r["end"] == end]
        gate(f"one crash component row ({end})", len(c) == 1)
        rho, tot = rho_for(c[0], q, m_mex)
        it = [r for r in items if r["end"] == end]
        gate(f"crash components add to the union central ({end})", len(it) == 1 and abs(tot - float(it[0]["central_bn"])) < 1e-6,
             f"{tot:.6f}")
        r = ingroup_by_ratio(case, "road_crash_externality", end, rho)
        out[end] = dict(r, rho=rho)
        arms.append(dict(item="road_crash_externality", arm=f"central (q {q:.3f}, h {h:.3f}, own passengers x m {m_mex:.3f})", end=end, value_bn=r["ingroup_bn"]))
        for lab, q_, m_ in (("q x1.3 (segregation within metros)", min(q * 1.3, 0.95), m_mex),
                            ("q at uniform mixing (s 0.108)", 0.108, m_mex),
                            ("every Hispanic passenger in-group", q, 1.0),
                            ("no own-driver passengers (household-internal)", q, 0.0)):
            arms.append(dict(item="road_crash_externality", arm=lab, end=end,
                             value_bn=ingroup_by_ratio(case, "road_crash_externality", end, rho_for(c[0], q_, m_)[0])["ingroup_bn"]))
    return dict(q=q, h=h, single_vehicle_inside_per_external=sv_pax * pax_in * m_mex / e_sv, ends=out), arms


_UA = None


def ua_rows() -> list[dict]:
    global _UA
    if _UA is None:
        _UA = []
        for r in rows(UA, "congestion urban-area exposure"):
            try:
                float(r["acs_group_vehicle_minutes"]), float(r["phi_commute_route"]), float(r["acs_other_vehicle_minutes"])
            except ValueError:
                continue
            _UA.append(r)
    return _UA


def congestion_block(case: dict) -> tuple[dict, list[dict]]:
    ua = {r["ua"]: r for r in ua_rows()}
    metro = rows(METRO, "congestion metro distribution")
    num = {"all": 0.0, "peak": 0.0}
    den = 0.0
    for m in metro:
        u = ua.get(m["ua"])
        if u is None or float(u["acs_other_vehicle_minutes"]) <= 0:
            continue
        b1 = float(m["B1_bn"])
        den += b1
        num["all"] += b1 * float(u["acs_group_vehicle_minutes"]) / float(u["acs_other_vehicle_minutes"])
        num["peak"] += b1 * float(u["acs_group_vehicle_minutes_peak"]) / float(u["acs_other_vehicle_minutes_peak"])
    total_b1 = sum(float(m["B1_bn"]) for m in metro)
    gate("congestion areas cover the B1 total", abs(den - total_b1) / total_b1 < 0.01, f"{den:.4f} / {total_b1:.4f}")
    rho = num["all"] / den
    out, arms = {}, []
    for end in ENDS:
        r = ingroup_by_ratio(case, "congestion", end, rho)
        out[end] = dict(r, rho=rho)
        arms.append(dict(item="congestion", arm=f"central (vehicle-minute ratio, B1-weighted {rho:.3f})", end=end, value_bn=r["ingroup_bn"]))
        arms.append(dict(item="congestion", arm="peak vehicle minutes", end=end,
                         value_bn=ingroup_by_ratio(case, "congestion", end, num["peak"] / den)["ingroup_bn"]))
    return dict(rho=rho, rho_peak=num["peak"] / den, ends=out), arms


def isolation() -> dict:
    """Mexican-origin isolation index (P*) and the outsider exposure, ACS 2020-24 tracts (victim lane cache)."""
    num = mex = pop = exp_o = out = 0.0
    files = sorted((CRIME / "_cache").glob("acs5_2024_b03001_tract_*.json"))
    gate("B03001 tract files for 51 states", len(files) == 51, str(len(files)))
    for f in files:
        SOURCES[str(f.relative_to(ROOT))] = "ACS B03001 tracts (victim lane cache)"
        d = json.loads(f.read_text())
        idx = {k: i for i, k in enumerate(d[0])}
        for r in d[1:]:
            p, m = float(r[idx["B03001_001E"]]), float(r[idx["B03001_004E"]])
            if p <= 0:
                continue
            num += m * m / p
            mex += m
            pop += p
            exp_o += (p - m) * m / p
            out += p - m
    return dict(isolation=num / mex, outsider_exposure=exp_o / out, mexican_share=mex / pop)


# ---------------------------------------------------------------------------------------------- B
def nibrs_ratios() -> tuple[list[dict], dict, list[dict]]:
    cells, manifest = nibrs_children.cells()
    for m in manifest:
        SOURCES[m["path"]] = f"NIBRS state file (read-only), sha256 {m['sha256']}"
    hh = cells[(cells.vclass == "vH")]
    table, ratios = [], {}
    for name, states in (("TX+AZ", ("TX", "AZ")), ("CA", ("CA",)), ("TX+AZ+CA", ("TX", "AZ", "CA")), ("TX", ("TX",))):
        s = hh[hh.state.isin(states)]
        for off in ("Rape/sexual assault", "Robbery", "Aggravated assault", "Simple assault"):
            o = s[s.offence == off]
            w = o.groupby("age").hisp_weight.sum()
            lt, ad = float(w.get("lt12", 0.0)), float(w.get("12p", 0.0))
            fam_child = float(o[(o.age == "lt12") & o.rel.isin(["family", "intimate"])].hisp_weight.sum())
            fam_adult = float(o[(o.age == "12p") & o.rel.isin(["family", "intimate"])].hisp_weight.sum())
            rel_known_adult = float(o[(o.age == "12p") & (o.rel != "unknown")].hisp_weight.sum())
            table.append(dict(scope=name, offence=off, hisp_to_hisp_lt12=lt, hisp_to_hisp_12p=ad,
                              hisp_to_hisp_age_unknown=float(w.get("unk", 0.0)), ratio_lt12_to_12p=lt / ad,
                              lt12_family_share=fam_child / lt, lt12_nonfamily_share=1 - fam_child / lt,
                              p12_family_intimate_share=fam_adult / ad, p12_family_intimate_share_rel_known=fam_adult / rel_known_adult))
            ratios[(name, off)] = table[-1]
    return table, ratios, manifest


def children_block(case: dict, t: dict, summary: dict, detail: list[dict], ratios: dict, cpi: dict) -> tuple[dict, list[dict]]:
    vsl = load_module("vsl_standard", CRIME / "vsl_standard.py")
    frame = case["frame"]
    mex_child = frame["union_hispanic|0_11"][1] / frame["cps_hispanic_civilian|0_11"][1]
    child_scale = (1 + case["keys"]["low_end"]["pupils"]) * (1 + case["added"]["low"]["pupils"])
    share_0_11 = (t["ncands_victims_age_lt1_to_9"] + t["ncands_victims_age_10_11"]) / t["ncands_victims_total"]
    gate("NCANDS victims 0-11 = 73.8% (worker's sum)", abs(share_0_11 - 0.738) < 0.0005, f"{share_0_11:.4f}")
    first = t["ncands_first_time_pct"] / 100
    perp = {"low (parents only, 0.891)": t["ncands_parents_pct"] / 100, "central (0.95)": 0.95, "high (1.0)": 1.0}
    victims = {k: t["ncands_hispanic_victims"] * share_0_11 * mex_child * p * child_scale for k, p in perp.items()}
    infl15 = cpi[2024] / cpi[2015]
    infl14 = cpi[2024] / cpi[2014]
    health = (t["peterson_short_health_2015"] + t["peterson_long_health_2015"]) * infl15
    qaly = t["peterson_qaly_decrement"]
    price = {"DOT VSL per discounted life-year (3%)": qaly * vsl.dot_vsl() / vsl.reference_life_years(0.03) + health,
             "HHS guidance QALY ($490k, 2014)": qaly * t["peterson_hhs_qaly_2014"] * infl14 + health,
             "Peterson native (Corso VSL)": t["peterson_qaly_value_2015"] * infl15 + health}
    gov = (t["peterson_child_welfare_2015"] + t["peterson_criminal_justice_2015"] + t["peterson_special_education_2015"]) * infl15
    gate("Peterson nonfatal components add to $830,928",
         abs(t["peterson_short_health_2015"] + t["peterson_long_health_2015"] + t["peterson_qaly_value_2015"]
             + t["peterson_child_welfare_2015"] + t["peterson_criminal_justice_2015"] + t["peterson_special_education_2015"]
             - t["peterson_total_nonfatal_2015"]) < 1)
    central_price = price["DOT VSL per discounted life-year (3%)"]
    nonfatal = victims["central (0.95)"] * first * central_price / 1e9
    arms = []
    for k, v in victims.items():
        arms.append(dict(item="child_maltreatment_0_11", arm=f"perpetrator in-group share {k}", end="both", value_bn=v * first * central_price / 1e9))
    for k, p in price.items():
        arms.append(dict(item="child_maltreatment_0_11", arm=f"price: {k}", end="both", value_bn=victims["central (0.95)"] * first * p / 1e9))
    arms.append(dict(item="child_maltreatment_0_11", arm="incidence: CPS-investigated base (Peterson's alternative, beside)", end="both",
                     value_bn=nonfatal * t["peterson_investigated_incident"] / t["peterson_substantiated_incident"]))
    arms.append(dict(item="child_maltreatment_0_11", arm="tangible only (health care)", end="both",
                     value_bn=victims["central (0.95)"] * first * health / 1e9))
    # Deaths NCANDS counts that WONDER does not code as assault: the share without physical abuse.
    ages = [t[f"ncands_fatal_age_{a}"] for a in range(12)]
    fatal_0_11 = sum(ages) / t["ncands_fatalities_age_known"]
    mean_age = int(round(sum((a if a else 0) * n for a, n in enumerate(ages)) / sum(ages)))
    hisp_deaths = t["ncands_hispanic_fatality_rate_per_100k"] / 1e5 * t["ncands_hispanic_child_population"]
    not_assault = 1 - t["ncands_fatal_physical_abuse_pct"] / 100
    deaths = hisp_deaths * fatal_0_11 * mex_child * 0.95 * child_scale * not_assault
    fatal = deaths * vsl.dot_vsl() / 1e9
    arms.append(dict(item="child_maltreatment_deaths_0_11", arm="central (deaths without physical abuse; DOT $13.7M)", end="both", value_bn=fatal))
    arms.append(dict(item="child_maltreatment_deaths_0_11", arm="every maltreatment death (overlaps the homicide row)", end="both", value_bn=fatal / not_assault))
    arms.append(dict(item="child_maltreatment_deaths_0_11", arm="perpetrators parents only (0.814)", end="both",
                     value_bn=fatal * t["ncands_fatal_parents_pct"] / 100 / 0.95))
    for rate in (0.0, 0.03):
        arms.append(dict(item="child_maltreatment_deaths_0_11", arm=f"life-years at mean age {mean_age}, {rate:.0%} real (beside)", end="both",
                         value_bn=fatal * vsl.remaining_years(mean_age, rate) / vsl.reference_life_years(rate)))
    # NIBRS: police-recorded non-family violence against under-12s, on the in-group 12+ counts of A.
    nibrs = {}
    for end in ENDS:
        for name in ("TX+AZ", "CA", "TX+AZ+CA"):
            nf = total = 0.0
            for off in ("Rape/sexual assault", "Robbery", "Aggravated assault", "Simple assault"):
                ad = sum(d["ingroup_victims"] for d in detail if d["end"] == end and d["offence"] == off)
                unit = next(d["unit_full_usd"] for d in detail if d["end"] == end and d["offence"] == off)
                rr = ratios[(name, off)]
                total += ad * rr["ratio_lt12_to_12p"] * unit / 1e9
                nf += ad * rr["ratio_lt12_to_12p"] * rr["lt12_nonfamily_share"] * unit / 1e9
            nibrs[(end, name)] = dict(nonfamily_bn=nf, all_relationships_bn=total)
            arms.append(dict(item="police_recorded_nonfamily_violence_lt12", arm=f"{name} ratios", end=end, value_bn=nf))
            arms.append(dict(item="police_recorded_violence_lt12_all_relationships (alternative to NCANDS, beside)",
                             arm=f"{name} ratios", end=end, value_bn=total))
        nibrs_struct = nibrs[(end, "TX+AZ")]["nonfamily_bn"] * summary[end]["nibrs_nonfatal_bn"] / summary[end]["ncvs_nonfatal_bn"]
        arms.append(dict(item="police_recorded_nonfamily_violence_lt12", arm="TX+AZ ratios on the NIBRS victim mix", end=end, value_bn=nibrs_struct))
    out = dict(mex_share_hispanic_0_11=mex_child, child_scale=child_scale, share_0_11=share_0_11, first_time=first,
               victims_0_11=victims["central (0.95)"], incident_victims_0_11=victims["central (0.95)"] * first,
               price_central_usd=central_price, health_usd=health, government_services_excluded_usd=gov,
               nonfatal_bn=nonfatal, deaths=deaths, fatal_bn=fatal, fatal_share_0_11=fatal_0_11,
               mean_fatal_age=mean_age, nibrs=nibrs)
    return out, arms


# ---------------------------------------------------------------------------------------------- C
def wdi(code: str, iso: str, year: str) -> float:
    path = read(WDI / f"wdi_{code}.json", f"WDI {code} (world ledger cache)")
    d = json.loads(path.read_text())
    v = [r["value"] for r in d[1] if r["countryiso3code"] == iso and r["date"] == year]
    gate(f"WDI {code} {iso} {year}", len(v) == 1 and v[0] is not None)
    return float(v[0])


def mexico_block(t: dict, case: dict) -> tuple[dict, list[dict]]:
    vsl = load_module("vsl_standard_c", CRIME / "vsl_standard.py")
    gdppc = {iso: wdi("NY.GDP.MKTP.PP.CD", iso, "2024") / wdi("SP.POP.TOTL", iso, "2024") for iso in ("MEX", "USA")}
    income_ratio = gdppc["MEX"] / gdppc["USA"]
    vsl_mx = {e: vsl.dot_vsl() * income_ratio ** e for e in (0.8, 1.0, 1.2)}   # [ASSUMPTION] income elasticity of VSL
    prem = [r for r in rows(G2_PREMIUM, "world ledger premium (oct16)") if r["generation"] == "G1"
            and r["convention"] == "own_schooling_all_ages" and r["ppp"] == "gdp" and r["selection"] == "p56"
            and r["mishra"] == "False" and r["diploma_reread"] == "0"]
    gate("one central G1 premium row", len(prem) == 1)
    e_mx = float(prem[0]["mexico_earnings_bn"]) * 1e9 / (float(prem[0]["persons_15plus_m"]) * 1e6)
    children = t["nobles2013_children_father_in_us_m"] * 1e6
    cohort = children / 15                              # under 15, uniform by age [ASSUMPTION]
    pv = e_mx * sum(1.03 ** -k for k in range(18 - 7, 65 - 7))     # earnings 18-64, child aged 7, 3% real
    arms, out = [], {}
    for ret in (0.06, 0.08, 0.10):                       # [ASSUMPTION] Mincer return per year of schooling
        value = ret * pv
        harm = -t["mckenzie_rapoport_males_16_18_years"] * cohort * value / 1e9
        gain = -max(t["hanson_woodruff_girls_10_12_years"], t["antman2012_girls_years"]) * cohort * value / 1e9
        arms.append(dict(item="C1 left-behind schooling", arm=f"every child at McKenzie-Rapoport -1.37 yr, return {ret:.0%}", end="both", value_bn=harm))
        arms.append(dict(item="C1 left-behind schooling", arm=f"every child at Hanson-Woodruff +0.89 yr, return {ret:.0%}", end="both", value_bn=gain))
        if ret == 0.08:
            out["schooling"] = dict(harm_bound_bn=harm, gain_bound_bn=gain, value_per_year_usd=value, pv_earnings_usd=pv, e_mx_usd=e_mx)
    # Left-behind mothers' depressive symptoms: 0.031 log points (FE) at one-sixth SD per 0.041.
    sd = t["nobles2015_fe_log_depression"] / (6 * t["nobles2015_log_per_sixth_sd"])
    mothers = children / 2.2                            # [ASSUMPTION] children under 15 per mother with a US spouse
    vsly_mx = vsl_mx[1.0] / vsl.reference_life_years(0.0)
    for q in (0.01, 0.05):                              # [ASSUMPTION] QALY loss per SD of depressive symptoms
        arms.append(dict(item="C3 left-behind mothers' depression", arm=f"{q} QALY a year per SD, VSL income-scaled (e=1)", end="both",
                         value_bn=mothers * sd * q * vsly_mx / 1e9))
    out["depression"] = dict(sd=sd, mothers=mothers, vsly_mx_usd=vsly_mx)
    # C0: members' homicide risk in Mexico against the US (world frame only).
    wonder = {r["group"]: r for r in rows(CRIME / "derived/wonder_2024_homicide_victims.csv", "WONDER 2024 homicide victims")}
    tp = {r["group"]: r for r in rows(CRIME / "derived/target_population_cps2025.csv", "CPS target population")}
    us_rate = float(wonder["hispanic"]["deaths_not_stated_allocated"]) / float(tp["cps_hispanic_civilian"]["all_ages"])
    mx_rate = wdi("VC.IHR.PSRC.P5", "MEX", "2023") / 1e5
    g1, g2 = float(tp["mexico_born"]["all_ages"]), float(tp["mexican_second_gen"]["all_ages"])
    for who, n in (("G1", g1), ("G1+G2", g1 + g2)):
        deaths = n * (mx_rate - us_rate)
        arms.append(dict(item="C0 homicide risk avoided by US residence (world frame, sign: benefit)", arm=f"{who}, DOT $13.7M", end="both",
                         value_bn=-deaths * vsl.dot_vsl() / 1e9))
        arms.append(dict(item="C0 homicide risk avoided by US residence (world frame, sign: benefit)", arm=f"{who}, income-scaled VSL (e=1)", end="both",
                         value_bn=-deaths * vsl_mx[1.0] / 1e9))
        out[f"homicide_{who}"] = dict(deaths_avoided=deaths, value_dot_bn=-deaths * vsl.dot_vsl() / 1e9)
    out.update(income_ratio=income_ratio, vsl_mx=vsl_mx, us_hispanic_homicide_rate=us_rate, mexico_homicide_rate=mx_rate,
               children_father_in_us=children)
    return out, arms


# ---------------------------------------------------------------------------------------------- main
def main() -> None:
    global CPI_ITEMS
    OUT.mkdir(exist_ok=True)
    texts = pinned_texts()
    t = transcribed(texts)
    cpi = {int(r["year"]): float(r["cpi_u"]) for r in rows(CPI, "CPI-U annual")}
    CPI_ITEMS = {2000: 172.2, 2024: 313.689}            # items.py's CPI (fear residual), gated by reproducing P7 fear
    case = case_inputs()

    detail, arms, vs = victims_block(case, CPI_ITEMS)
    sf, a2 = security_fear(case, vs)
    arms += a2
    rho_p = property_rho()
    pm, a3 = pm_block(case)
    arms += a3
    m_mex = vs["low"]["m_central"]
    crash, a4 = crash_block(case, m_mex)
    arms += a4
    cong, a5 = congestion_block(case)
    arms += a5
    iso = isolation()
    rho_school = iso["isolation"] / (1 - iso["isolation"])
    nibrs_table, ratios, _ = nibrs_ratios()
    # Domestic and intimate violence is already inside A's NCVS counts; police records give its share.
    dv = {}
    for end in ENDS:
        nf = [d for d in detail if d["end"] == end and d["block"] != "homicide"]
        cost = {o: sum(d["ingroup_full_bn"] for d in nf if d["offence"] == o) for o in {d["offence"] for d in nf}}
        dv[end] = dict(family_intimate_bn=sum(c * ratios[("TX+AZ", o)]["p12_family_intimate_share"] for o, c in cost.items()),
                       family_intimate_rel_known_bn=sum(c * ratios[("TX+AZ", o)]["p12_family_intimate_share_rel_known"]
                                                        for o, c in cost.items()),
                       nonfatal_ingroup_bn=sum(cost.values()))
    child, a6 = children_block(case, t, vs, detail, ratios, cpi)
    arms += a6
    mx, a7 = mexico_block(t, case)
    arms += a7

    rows_out = []

    def add(block, item, low, high, frame, note, arm_values=None):
        vals = [low, high] + (arm_values or [])
        rows_out.append(dict(block=block, item=item, frame=frame, low_end_bn=low, high_end_bn=high,
                             arm_min_bn=min(vals), arm_max_bn=max(vals),
                             per_member_low_usd=low / POPULATION_M * 1e3, per_member_high_usd=high / POPULATION_M * 1e3, note=note))

    arm_vals = lambda item: [a["value_bn"] for a in arms if a["item"] == item]  # noqa: E731
    whole = "whole US population; harm by lineage members to lineage members"
    add("A", "victims (homicide + non-fatal 12+)", vs["low"]["full"], vs["high"]["full"], whole,
        "NCVS mix, tract m, DOT uniform VSL; replaces the world ledger's ingroup_victims rows", arm_vals("victims"))
    prop = {e: ingroup_by_ratio(case, "property_crime", e, rho_p)["ingroup_bn"] for e in ENDS}
    add("A", "property crime", prop["low"], prop["high"], whole, f"arrest-share proxy; in/out {rho_p:.3f}")
    add("A", "fear/avoidance", sf["low"]["fear_bn"], sf["high"]["fear_bn"], whole, "P7 WTP residual on in-group victims", arm_vals("fear_avoidance"))
    add("A", "private security", sf["low"]["security_bn"], sf["high"]["security_bn"], whole,
        "members' households and purchases", arm_vals("private_security"))
    add("A", "PM2.5 from consumption", pm["ends"]["low"]["ingroup_bn"], pm["ends"]["high"]["ingroup_bn"], whole,
        f"self-share {pm['sigma']:.4f}", arm_vals("pm25_consumption"))
    add("A", "road crashes", crash["ends"]["low"]["ingroup_bn"], crash["ends"]["high"]["ingroup_bn"], whole,
        "members' crashes with members' traffic; own driver's injury excluded", arm_vals("road_crash_externality"))
    add("A", "congestion", cong["ends"]["low"]["ingroup_bn"], cong["ends"]["high"]["ingroup_bn"], whole,
        "members' delay from members' traffic", arm_vals("congestion"))
    a_total = [sum(r[f"{e}_end_bn"] for r in rows_out if r["block"] == "A") for e in ENDS]
    school = {e: ingroup_by_ratio(case, "school_disruption", e, rho_school)["ingroup_bn"] for e in ENDS}
    add("A-beside", "school disruption (not in A's total)", school["low"], school["high"], whole,
        f"gap-based peer effect; isolation {iso['isolation']:.3f}; no without-world for in-group pupils")
    add("B", "child maltreatment 0-11, non-fatal (NCANDS, Peterson prices)", child["nonfatal_bn"], child["nonfatal_bn"], whole,
        "caregiver maltreatment NCVS cannot see; government services excluded", arm_vals("child_maltreatment_0_11"))
    add("B", "child maltreatment deaths 0-11 not coded as assault", child["fatal_bn"], child["fatal_bn"], whole,
        "WONDER assault homicides are in A", arm_vals("child_maltreatment_deaths_0_11"))
    add("B", "police-recorded non-family violence against under-12s", child["nibrs"][("low", "TX+AZ")]["nonfamily_bn"],
        child["nibrs"][("high", "TX+AZ")]["nonfamily_bn"], whole, "NIBRS TX+AZ ratios on A's in-group 12+ counts; Miller prices",
        arm_vals("police_recorded_nonfamily_violence_lt12"))
    b_total = [sum(r[f"{e}_end_bn"] for r in rows_out if r["block"] == "B") for e in ENDS]
    world = "world frame: members' relatives in Mexico"
    sch = mx["schooling"]
    add("C", "C1 left-behind schooling (central 0: signs conflict)", 0.0, 0.0, world,
        "interval only; total effects incl. remittances", arm_vals("C1 left-behind schooling"))
    add("C", "C2 left-behind child health (sign: benefit, unpriced)", 0.0, 0.0, world, "birth weight +335-364 g; IMR lower; GAP")
    add("C", "C3 left-behind mothers' depression (no defensible central)", 0.0, 0.0, world,
        "interval only; QALY mapping assumed", arm_vals("C3 left-behind mothers' depression"))
    c0 = mx["homicide_G1"]["value_dot_bn"]
    add("C0", "members' homicide risk avoided by US residence, G1 (benefit)", c0, c0, "world frame: members themselves",
        "counterfactual for A's victims in the world frame; not a cost row",
        arm_vals("C0 homicide risk avoided by US residence (world frame, sign: benefit)"))

    write_csv("rows.csv", rows_out)
    write_csv("arms.csv", arms)
    write_csv("victims_detail.csv", detail)
    write_csv("nibrs_child_ratios.csv", nibrs_table)
    summary = dict(
        case="oct16", frame_note="beside rows; never added to the cost-to-other-residents pairing",
        per_member_population_m=POPULATION_M,
        block_A_total_bn=dict(zip(ENDS, a_total)), block_B_total_bn=dict(zip(ENDS, b_total)),
        A_plus_B_bn=dict(zip(ENDS, [a + b for a, b in zip(a_total, b_total)])),
        A_plus_B_per_member_usd=dict(zip(ENDS, [(a + b) / POPULATION_M * 1e3 for a, b in zip(a_total, b_total)])),
        victims={e: {k: v for k, v in vs[e].items()} for e in ENDS}, rho_nonfatal_nibrs=vs["rho_nonfatal_nibrs"],
        security_fear=sf, property_rho=rho_p, pm={"sigma": pm["sigma"], "rho": pm["rho"]},
        crash={k: v for k, v in crash.items() if k != "ends"}, congestion={k: v for k, v in cong.items() if k != "ends"},
        isolation=iso, school_rho=rho_school, domestic_violence_inside_A=dv, children={k: v for k, v in child.items() if k != "nibrs"},
        mexico=mx, transcribed=t, factor=case["factor"])
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1, sort_keys=True, default=float) + "\n")
    manifest = [dict(path=p, role=r, sha256=digest(ROOT / p)) for p, r in sorted(SOURCES.items())]
    write_csv("source_manifest.csv", manifest)
    write_csv("gates.csv", GATES)
    print(f"✓ {len(GATES)} gates pass")
    for r in rows_out:
        print(f"  {r['block']:8} {r['item'][:62]:62} {r['low_end_bn']:9.3f} {r['high_end_bn']:9.3f}  [{r['arm_min_bn']:.2f}, {r['arm_max_bn']:.2f}]")
    print(f"  A total {a_total[0]:.3f} / {a_total[1]:.3f}; B total {b_total[0]:.3f} / {b_total[1]:.3f}")


CPI_ITEMS: dict = {}

if __name__ == "__main__":
    main()
