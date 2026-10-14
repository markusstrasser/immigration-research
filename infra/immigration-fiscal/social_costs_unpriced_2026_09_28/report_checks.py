"""Report-only crime checks; never write a producer outside report_checks* paths."""
from pathlib import Path
import argparse
import faulthandler
import hashlib
import importlib.util
import json
import os
import re
import resource
import time
import urllib.request
import openpyxl

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
F = HERE.parent
INPUT = HERE / "inputs"
OUT = HERE / "derived"
PINS = INPUT / "report_checks_pins.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def gate(ok, text):
    if not ok:
        raise SystemExit(f"[BLOCKED] {text}")


def pin(path, url, acquire=False):
    pins = json.loads(PINS.read_text()) if PINS.exists() else {}
    k = str(path.relative_to(F))
    record = {"url": url, "sha256": sha(path), "bytes": path.stat().st_size}
    if acquire:
        gate(k not in pins or pins[k] == record, f"changed pin {k}")
        pins[k] = record
        PINS.write_text(json.dumps(pins, indent=2, sort_keys=True) + "\n")
    else:
        gate(pins.get(k) == record, f"missing or changed input pin {k}; run --acquire")


def main():
    faulthandler.dump_traceback_later(30, repeat=True)
    ap = argparse.ArgumentParser()
    ap.add_argument("--acquire", action="store_true")
    args = ap.parse_args()
    start = time.perf_counter()
    INPUT.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    state_file = INPUT / "report_checks_acs1_2024_state1864.json"
    url = "https://api.census.gov/data/2024/acs/acs1/pums?tabulate=weight(PWGTP)&col+TYPEHUGQ&row+NATIVITY&row+HISP&row+for&for=state:*&AGEP=18:64"
    if not state_file.exists():
        gate(args.acquire, "state table missing; run --acquire")
        secret = os.environ.get("CENSUS_API_KEY", "")
        if not secret:
            m = re.search(r'CENSUS_API_KEY="?([A-Za-z0-9]+)', (F / "acquire/config.local.env").read_text())
            secret = m.group(1) if m else ""
        gate(bool(secret), "Census key unavailable")
        try:
            body = urllib.request.urlopen(url + "&key=" + secret, timeout=120).read()
            json.loads(body)
        except Exception as exc:
            detail = exc.read().decode(errors="replace") if hasattr(exc, "read") else str(exc)
            raise SystemExit("[BLOCKED] ACS state fetch: " + detail.replace(secret, "<KEY>")) from None
        state_file.write_bytes(body)
    pin(state_file, url, args.acquire)
    tables = []
    tract_files = sorted((F / "crime_victim_cost_2026_09_23/_cache").glob("acs5_2024_b03001_tract_*.json"))
    gate(len(tract_files) == 51, "51 state/DC tract files required")
    for p in tract_files:
        st = p.stem.rsplit("_", 1)[-1]
        pin(p, f"https://api.census.gov/data/2024/acs/acs5?get=NAME,B03001_001E,B03001_003E,B03001_004E&for=tract:*&in=state:{st}", args.acquire)
        a = json.loads(p.read_text())
        tables.append(pd.DataFrame(a[1:], columns=a[0]))
    t = pd.concat(tables, ignore_index=True)
    for c in ["B03001_001E", "B03001_003E", "B03001_004E"]:
        t[c] = pd.to_numeric(t[c])
    gate((t.B03001_004E <= t.B03001_003E).all() and (t.B03001_003E <= t.B03001_001E).all(), "tract nesting")
    t = t[t.B03001_001E > 0]
    geo = []
    for label, s in [("national", t), ("Texas", t[t.state == "48"]), ("Arizona", t[t.state == "04"]), ("Texas+Arizona", t[t.state.isin(["48", "04"])])]:
        h, m, p = s.B03001_003E, s.B03001_004E, s.B03001_001E
        geo.append(dict(geography=label, tracts=len(s), mexican=float(m.sum()), hispanic=float(h.sum()), population=float(p.sum()),
                        hispanic_tract_share_at_mexican_residence=float((m * h / p).sum() / m.sum()),
                        mexican_share_of_hispanic_neighbors=float((m[h > 0] * m[h > 0] / h[h > 0]).sum() / m.sum())))
    pd.DataFrame(geo).to_csv(OUT / "report_checks_geography.csv", index=False, lineterminator="\n")

    raw = json.loads(state_file.read_text())
    cols = {list(x.values())[0]: i for i, x in enumerate(raw[0]) if isinstance(x, dict)}
    rows = []
    us_states = set(t.state.unique())
    for r in raw[1:]:
        nat, hisp, st = map(str, r[len(cols):len(cols) + 3])
        if st.zfill(2) not in us_states:
            gate(all(float(r[i]) == 0 for i in cols.values()), "non-US state carries weight")
            continue
        rows.append(dict(nativity={"1": "native", "2": "foreign_born"}[nat], hisp=hisp.zfill(2), state=st.zfill(2),
                         hh=float(r[cols["1"]]), inst=float(r[cols["2"]]), noninst=float(r[cols["3"]])))
    a = pd.DataFrame(rows)
    gate(set(a.state) == us_states and len(us_states) == 51, "state table covers all 50 states and DC")
    a["total"] = a.hh + a.inst + a.noninst
    cj = load("report_cj", F / "cj_use_allocation_2026_09_23/allocate.py")
    national = a.groupby(["nativity", "hisp"], as_index=False)[["hh", "inst", "noninst", "total"]].sum()
    national_by = cj.by_nativity(national)
    original = pd.read_csv(cj.ACS, dtype={"hisp": str})
    original = original[(original["product"] == "acs1_2024") & (original.ages.astype(str) == "1864")]
    original_by = cj.by_nativity(original)
    gate(abs(a.inst.sum() - original.inst.sum()) < 1e-6, "state institutional counts close to national")
    # API table cells contain exact weights; original national CSV rounded each cell.
    gate(max(abs(national_by[n]["I_mex_adj"] - original_by[n]["I_mex_adj"]) for n in national_by) < 50, "national allocator positive control within cell rounding")
    b = []
    for st, g in a.groupby("state"):
        for nat, gn in g.groupby("nativity"):
            mex = gn[gn.hisp == "02"].iloc[0]
            gen = gn[gn.hisp == "24"].iloc[0]
            named = gn[~gn.hisp.isin(["01", "24"])]
            gate(gn.total.sum() > 0, f"empty state/nativity {st}/{nat}")
            excess = max(0.0, gen.inst - gn.inst.sum()/gn.total.sum()*gen.total)
            named_share = mex.total/named.total.sum() if named.total.sum() else 0.0
            gate(named.total.sum() > 0 or (mex.total == 0 and excess == 0), "unallocatable Hispanic excess")
            b.append(dict(state=st, nativity=nat, I_mex=float(mex.inst), HH_mex=float(mex.hh),
                          excess=excess, mex_share_named_pop=named_share, I_mex_adj=float(mex.inst)+excess*named_share))
    b = pd.DataFrame(b)
    gate(abs(b.I_mex.sum() - national[national.hisp == "02"].inst.sum()) < 1e-6, "Mexican raw count conserved")
    b.to_csv(OUT / "report_checks_state_reallocation.csv", index=False, lineterminator="\n")
    builder = cj.load_builder()
    cps = cj.cps_target(builder)
    held = json.loads((cj.DERIVED / "summary.json").read_text())
    I_all = float(a.inst.sum())
    shares = {}
    for mode in ["national", "state"]:
        by = national_by if mode == "national" else {n: {"I_mex_adj": float(b[b.nativity == n].I_mex_adj.sum()), "HH_mex": national_by[n]["HH_mex"]} for n in national_by}
        shares[mode] = sum(cps[{"native": "us_born", "foreign_born": "mexico_born"}[n]]["18_64"] * by[n]["I_mex_adj"] / by[n]["HH_mex"] for n in by) / I_all
    gate(abs(shares["national"] - held["shares"]["custody_acs_adj"]) < 1e-5, "CJ custody share positive control")
    pool = cj.bea_cells(builder)["scaled_bn"]["prisons"]
    prison_delta = (shares["state"] - shares["national"]) * pool
    m_nat = sum(v["I_mex_adj"] for v in national_by.values()) / national[national.hisp != "01"].inst.sum()
    m_state = float(b.I_mex_adj.sum()) / national[national.hisp != "01"].inst.sum()
    # Police half arrest/per-head and courts 60% criminal share: allocator's central selection.
    arrest_change = held["shares"]["arrest_adj"] * (m_state / m_nat - 1)
    ki = pd.read_csv(cj.DERIVED / "key_inputs.csv")
    police_pool = float(ki.set_index(ki.columns[0]).loc["police_pool_bn", "value"])
    court_pool = cj.bea_cells(builder)["scaled_bn"]["law_courts"]
    other_delta = arrest_change * (0.5 * police_pool + 0.6 * court_pool)
    summary = dict(custody_national=shares["national"], custody_state=shares["state"], custody_share_change=shares["state"]-shares["national"],
                   m_national=m_nat, m_state=m_state, prison_raw_key_change_bn=prison_delta,
                   arrests_derived_key_change_bn=other_delta, custody_and_arrests_raw_key_change_bn=prison_delta+other_delta,
                   caution="Conditional redistribution of unsplit institutional residence, not measured ordinary offending; state census sampling SE unavailable from tabulation.")
    (OUT / "report_checks_custody.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    # ICE overlap: a deliberately broad scenario envelope, never a subtraction from ACS.
    det = F / "detention_evidence_2026_09_20"
    manifest = json.loads((det / "manifest.json").read_text())
    for name in ["ice_fy2024_yearend.xlsx", "ice_fy2024_annual.pdf"]:
        record = next(r for r in manifest if r["file"] == name)
        pin(det / "_cache" / name, record["url"], args.acquire)
    wb = openpyxl.load_workbook(cj.ICE_XLSX, read_only=True, data_only=True)
    dr = [[x for x in r if x is not None] for r in wb["Detention FY24"].values]
    at = next(i for i, r in enumerate(dr) if r and str(r[0]).startswith("ICE Currently Detained by Criminality and Arresting Agency"))
    stock = next(r for r in dr[at:] if r and r[0] == "Total")[5]
    adp = next(r for r in dr if r and str(r[0]).strip() == "Average")[-1]
    import subprocess
    text = subprocess.run(["pdftotext", "-layout", str(cj.ICE_PDF), "-"], capture_output=True, text=True, check=True).stdout
    text = text[text.index("Country of Citizenship                          Detained"):]
    mex_ice = int(re.search(r"Mexico\s+([\d,]+)", text).group(1).replace(",", ""))
    fb = national_by["foreign_born"]
    mex_inst = sum(v["I_mex_adj"] for v in national_by.values())
    def overlap_share(total, mexico):
        numerator = cps["mexico_born"]["18_64"] * max(0, fb["I_mex_adj"]-mexico) / fb["HH_mex"]
        numerator += cps["us_born"]["18_64"] * national_by["native"]["I_mex_adj"] / national_by["native"]["HH_mex"]
        return numerator / (I_all-total)
    ice = dict(ice_yearend_stock=stock, ice_fy2024_adp=adp, mexico_national_yearend= mex_ice,
               acs_institutional_18_64=I_all, acs_mexican_adjusted_18_64=mex_inst,
               stock_over_acs_all=stock/I_all, mexican_national_stock_over_acs_mexican_adjusted=mex_ice/mex_inst,
               conditional_nationality_matched_all_overlap_prison_change_bn=(overlap_share(stock,mex_ice)-shares["national"])*pool,
               extreme_all_ice_assigned_mexican_prison_change_bn=(overlap_share(stock,stock)-shares["national"])*pool,
               extreme_zero_mexican_overlap_prison_change_bn=(overlap_share(stock,0)-shares["national"])*pool,
               label="[ASSUMPTION] Full-overlap stock stress tests; not matched ACS corrections or statistical bounds. Contract-only origin/age/year overlap unidentified. All ICE stock dominates its contract subset.")
    (OUT / "report_checks_ice.json").write_text(json.dumps(ice, indent=2, sort_keys=True)+"\n")
    # Victim-model recomputation uses the existing read-only API and primary price parser.
    rerun = load("report_victim_rerun", F / "offender_ethnicity_nibrs_2026_09_23/victim_cost_rerun.py")
    vc = rerun.load_victim_lane()
    S = rerun.setup(vc)
    cen = rerun.run(vc, S)
    arr = rerun.run(vc, S, nonfatal_source="arrests_2019")
    ir = vc.institutional_ratio()
    cust = rerun.run(vc, S, ratio=ir["ratio_generic_reallocated"])
    # Inputs checked to 1e-4bn: arms.csv stores four decimal places.
    held_v = pd.read_csv(vc.HERE / "derived/arms.csv").set_index("arm")
    gate(abs(cen["full"]/1e9-held_v.loc["central","full_bn"]) < 1e-4, "victim central positive control")
    base_exposure = next(r for r in geo if r["geography"] == "national")
    delta_m = next(r for r in geo if r["geography"] == "Texas+Arizona")["mexican_share_of_hispanic_neighbors"] - base_exposure["mexican_share_of_hispanic_neighbors"]
    S_geo = {**S, "m_geo": {**S["m_geo"], "tract": S["m_geo"]["tract"]+delta_m}}
    geo_central = rerun.run(vc, S_geo)
    # Same offence incidence, NIBRS victim-share transfer vs raw TX/AZ share (existing lane).
    costs = pd.read_csv(F / "offender_ethnicity_nibrs_2026_09_23/derived/cost_arms.csv")
    costs = costs[costs.spec == "central"].set_index("arm")
    frame = pd.read_csv(F / "population_basis_2026_09_29/derived/frame_counts.csv").set_index("count")
    fs = float((frame.loc["union|12_plus","row4"] / frame.loc["cps_hispanic_civilian|12_plus","row4"]) /
               (frame.loc["union|12_plus","published"] / frame.loc["cps_hispanic_civilian|12_plus","published"]))
    victims = dict(central_published_bn=cen["full"]/1e9, custody_high_published_bn=cust["full"]/1e9,
                   arrest_based_published_bn=arr["full"]/1e9, frame_factor=fs,
                   arrest_based_row4_bn=arr["full"]/1e9*fs, custody_high_row4_bn=cust["full"]/1e9*fs,
                   arrest_minus_custody_row4_bn=(arr["full"]-cust["full"])/1e9*fs,
                   nibrs_national_transfer_minus_raw_txaz_row4_bn=float(costs.loc["offender+victims","full_bn"]-costs.loc["offender+victims (TX/AZ as observed)","full_bn"])*fs,
                   mexican_share_neighbor_gap=delta_m, mexican_neighbor_geography_sensitivity_row4_bn=(geo_central["full"]-cen["full"])/1e9*fs,
                   assumption="Geography m shift is a sensitivity, not an empirical national victim-matching correction. Arrest ethnic shares proxy incidents and assume equal per-person offending within Hispanics; homicide unchanged. Mixed-offender correction and unified VSL left to adopting worker.")
    direction = F / "crime_ratio_direction_2026_09_24/derived"
    theta = float(pd.read_csv(direction / "nibrs_mixed_group_hispanic_fraction.csv").set_index("offence").loc["All five", "mean_hispanic_fraction"])
    eff = pd.read_csv(direction / "dollar_effects.csv")
    mixed = eff[(eff.item == "non-fatal: mixed-offender groups with a Hispanic member") & eff.method.str.contains("theta 1.0000")].iloc[0]
    mixed0 = eff[(eff.item == "non-fatal: mixed-offender groups with a Hispanic member") & eff.method.str.contains("theta 0.0000")].iloc[0]
    increment_at_one = float(mixed.full_bn-mixed0.full_bn)
    e_us = base_exposure["hispanic_tract_share_at_mexican_residence"]
    e_txaz = next(r for r in geo if r["geography"] == "Texas+Arizona")["hispanic_tract_share_at_mexican_residence"]
    logit = lambda x: np.log(x/(1-x))
    transferred_theta = float(1/(1+np.exp(-(logit(theta)+logit(e_us)-logit(e_txaz)))))
    victims.update(theta_nibrs_txaz=theta, theta_logodds_exposure_sensitivity=transferred_theta,
                   theta_geography_shift_low_row4_bn=(transferred_theta-theta)*increment_at_one*fs,
                   theta_geography_shift_high_row4_bn=(transferred_theta-theta)*increment_at_one*fs*ir["ratio_generic_reallocated"],
                   theta_feasible_shift_low_row4_bn=[-theta*increment_at_one*fs,(1-theta)*increment_at_one*fs],
                   theta_feasible_shift_high_row4_bn=[-theta*increment_at_one*fs*ir["ratio_generic_reallocated"],(1-theta)*increment_at_one*fs*ir["ratio_generic_reallocated"]],
                   theta_transfer_caution="[ASSUMPTION] Preserved mixed-offender log-odds enrichment relative to population exposure; conditional mixed-group composition does not identify this transfer. Feasible theta 0–1 envelope only applies to the mixed-offender correction, not all crime costs.")
    (OUT / "report_checks_victims.json").write_text(json.dumps(victims, indent=2, sort_keys=True)+"\n")
    print(json.dumps(summary, indent=2))
    faulthandler.cancel_dump_traceback_later()
    print(f"elapsed_seconds={time.perf_counter()-start:.3f} peak_rss_bytes={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")


if __name__ == "__main__":
    main()
