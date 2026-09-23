#!/usr/bin/env python3
"""ACS 2024 one-year PUMS tabulations for the care and household-services lane.

One pass over the zipped national person files (local copy, SHA-256 recorded). Group person
(the "union"): Hispanic origin Mexican (HISP=02) or born in Mexico (POBP=303), the housing and
congestion lanes' rule; it is scaled to the CPS union (40,896,574) downstream, not here.

Outputs (derived/):
  acs_national.csv        named national totals with replicate standard errors: the
                          Cortés–Tessada low-skill share and its parts, the Cortés (2008) share,
                          the Butcher–Moran–Watson treatment share, elderly and care-need counts
  acs_care_workforce.csv  workers and annual hours by care/household occupation x sector x group
  acs_women.csv           the two affected populations (Cortés–Tessada top-quartile native women;
                          East–Velásquez college-educated US-born mothers of children under 6)
  acs_puma_cells.csv      PUMA-level components for the metro-level shock (main weight only)
  acs_audit.json          source hash, record counts, gates

Definitions follow the papers (see RESULT.md "Definitions"):
  Cortés–Tessada L = ln[(no-diploma immigrants + no-diploma natives) / labor force], ages 16-64,
    in the labor force (ESR 1-5), not enrolled (SCH=1); no diploma = SCHL<=15.
  Cortés (2008) share = foreign-born no-diploma / civilian labor force 16+ (the 2026-09-18 lane's
    construction, kept for comparability).
  Butcher–Moran–Watson share = foreign-born with less than one year of college (SCHL<=18) /
    population 16-64.
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/care_household_services_2026_09_23/acs_extract.py
"""
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ZIP = ROOT / "sources/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip"
OUT = HERE / "derived"
REPS = [f"PWGTP{i}" for i in range(1, 81)]
COLS = ["SERIALNO", "STATE", "DIVISION", "PUMA", "PWGTP", "AGEP", "SEX", "NATIVITY", "POBP",
        "HISP", "CIT", "SCHL", "SCH", "ESR", "WKHP", "WKWN", "WAGP", "PERNP", "ADJINC", "OCCP",
        "INDP", "RELSHIPP", "PAOC", "DDRS", "DOUT", "HINS4"] + REPS
CHUNK = 300_000
MEXICO = 303
ACS_TOTAL_POP = 340_110_988  # ACS 2024 1-year resident population, the account's denominator
POP_TOLERANCE = 10  # PUMS person weights sum to 340,110,990: published-table rounding only

OCC = {3601: "home_health_aides", 3602: "personal_care_aides", 3603: "nursing_assistants",
       3605: "orderlies_psych_aides", 4230: "maids_housekeepers", 4600: "childcare_workers",
       4251: "landscaping_groundskeeping"}
SECTOR = {8170: "home_health_care", 9290: "private_households", 8370: "individual_family_services",
          8270: "nursing_care_facilities", 8290: "residential_care", 8470: "child_care_services",
          7690: "services_to_buildings", 7770: "landscaping_services"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def sdr(vec: np.ndarray) -> tuple[float, float]:
    vec = np.asarray(vec, dtype=float)
    return float(vec[0]), float(np.sqrt(4.0 / 80.0 * np.square(vec[1:] - vec[0]).sum()))


def chunks():
    dtypes = {c: "float32" for c in REPS}
    dtypes.update({"SERIALNO": str, "PUMA": str, "STATE": str, "PWGTP": "float64"})
    with zipfile.ZipFile(ZIP) as z:
        members = sorted(n for n in z.namelist() if n.lower().endswith(".csv"))
        if len(members) != 2:
            raise SystemExit(f"[BLOCKED] expected 2 csv members, got {members}")
        for name in members:
            print(f"[read] {name}", flush=True)
            with z.open(name) as fh:
                yield from pd.read_csv(fh, usecols=COLS, dtype=dtypes, chunksize=CHUNK,
                                       low_memory=False)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    totals: dict[str, np.ndarray] = {}
    work_frames, women_frames, puma_frames = [], [], []
    n_records = 0

    def add(name: str, w: np.ndarray, mask: np.ndarray) -> None:
        v = w[mask].sum(axis=0)
        totals[name] = totals.get(name, 0) + v

    for df in chunks():
        n_records += len(df)
        W = df[["PWGTP"] + REPS].to_numpy(dtype=np.float64)
        age = df.AGEP.to_numpy()
        nat = df.NATIVITY.to_numpy() == 1
        fb = ~nat
        mexb = df.POBP.to_numpy() == MEXICO
        union = (df.HISP.to_numpy() == 2) | mexb
        schl = df.SCHL.to_numpy()
        esr = df.ESR.to_numpy()
        sch = df.SCH.to_numpy()
        rel = df.RELSHIPP.to_numpy()
        inst = rel == 37
        nongq_inst = rel == 38
        hh = ~(inst | nongq_inst)
        groups = {"union_fb": union & fb, "union_nat": union & nat,
                  "other_fb": ~union & fb, "other_nat": ~union & nat}

        add("pop_all", W, np.ones(len(df), bool))
        add("pop_union", W, union)
        for g, m in groups.items():
            add(f"pop_{g}", W, m)

        # --- Cortés–Tessada low-skill share (16-64, in labor force incl. armed forces, not enrolled)
        ct_base = (age >= 16) & (age <= 64) & np.isin(esr, [1, 2, 3, 4, 5]) & (sch == 1)
        ls = schl <= 15
        add("ct_lf_all", W, ct_base)
        add("ct_lf_union", W, ct_base & union)
        for g, m in groups.items():
            add(f"ct_ls_{g}", W, ct_base & ls & m)
            add(f"ct_lf_{g}", W, ct_base & m)
        add("ct_ls_mexborn", W, ct_base & ls & mexb)
        # --- Cortés (2008) share as built by the 2026-09-18 lane (civilian labor force 16+)
        civ = (age >= 16) & np.isin(esr, [1, 2, 3])
        add("c08_lf_all", W, civ)
        add("c08_lf_union", W, civ & union)
        add("c08_lsi_all", W, civ & fb & ls)
        add("c08_lsi_union", W, civ & fb & ls & union)
        add("c08_lsi_mexborn", W, civ & fb & ls & mexb)
        # --- Butcher–Moran–Watson treatment: foreign-born, < 1 year of college, share of 16-64
        wa = (age >= 16) & (age <= 64)
        add("bmw_wa_all", W, wa)
        add("bmw_wa_union", W, wa & union)
        add("bmw_lowed_fb_all", W, wa & fb & (schl <= 18))
        add("bmw_lowed_fb_union", W, wa & fb & (schl <= 18) & union)
        add("bmw_lowed_fb_mexborn", W, wa & fb & (schl <= 18) & mexb)

        # --- elderly, institutions, Medicaid, citizenship
        old = age >= 65
        citizen = df.CIT.to_numpy() <= 4
        medicaid = df.HINS4.to_numpy() == 1
        for g, m in groups.items():
            add(f"e65_{g}", W, old & m)
            add(f"e65_inst_{g}", W, old & inst & m)
            add(f"e65_inst_medicaid_{g}", W, old & inst & m & medicaid)
            add(f"e65_citizen_{g}", W, old & m & citizen)
            add(f"e65_citizen_inst_{g}", W, old & m & citizen & inst)
            add(f"e80_{g}", W, (age >= 80) & m)
            add(f"e80_inst_{g}", W, (age >= 80) & inst & m)
        # --- care need: self-care (DDRS) or independent-living (DOUT) difficulty
        need = (df.DDRS.to_numpy() == 1) | (df.DOUT.to_numpy() == 1)
        for g, m in groups.items():
            for band, bm in {"u65": age < 65, "65p": old}.items():
                add(f"need_hh_{band}_{g}", W, need & hh & bm & m)
                add(f"need_inst_{band}_{g}", W, need & inst & bm & m)
                add(f"need_hh_medicaid_{band}_{g}", W, need & hh & bm & m & medicaid)

        # --- care and household-service workers (employed, current occupation)
        occ = df.OCCP.to_numpy()
        emp = np.isin(esr, [1, 2]) & np.isin(occ, list(OCC))
        if emp.any():
            sub = df.loc[emp, ["OCCP", "INDP", "WKHP", "WKWN", "SCHL", "HISP", "NATIVITY",
                               "POBP"]].copy()
            g4 = np.select([groups[k][emp] for k in groups], list(groups), "none")
            sub["group"] = g4
            hours = (sub.WKHP.fillna(0) * sub.WKWN.fillna(0)).to_numpy()
            sub["likely_undoc"] = ((sub.NATIVITY == 2) & (sub.HISP >= 2) & (sub.SCHL <= 15))
            sub["mexborn"] = sub.POBP == MEXICO
            # Butcher–Moran–Watson treatment group: foreign-born, < 1 year of college
            sub["lowed_fb"] = (sub.NATIVITY == 2) & (sub.SCHL <= 18)
            Wsub = W[emp]
            sub_w = pd.DataFrame(Wsub, columns=["w"] + REPS, index=sub.index)
            sub_h = pd.DataFrame(Wsub * hours[:, None], columns=["h"] + [f"h{r}" for r in REPS],
                                 index=sub.index)
            keys = sub[["OCCP", "INDP", "group", "likely_undoc", "mexborn", "lowed_fb"]]
            work_frames.append(pd.concat([keys, sub_w, sub_h], axis=1)
                               .groupby(["OCCP", "INDP", "group", "likely_undoc", "mexborn",
                                         "lowed_fb"],
                                        dropna=False).sum())

        # --- women rows kept for the wage-quartile and mothers populations
        female = df.SEX.to_numpy() == 2
        keep = female & (age >= 20) & (age <= 64)
        if keep.any():
            cols = ["STATE", "PUMA", "DIVISION", "AGEP", "NATIVITY", "SCHL", "ESR", "WKHP", "WKWN",
                    "WAGP", "PERNP", "ADJINC", "PAOC"]
            wdf = df.loc[keep, cols].copy()
            wdf["union"] = union[keep]
            wdf["w"] = W[keep, 0]
            wdf[REPS] = W[keep, 1:].astype(np.float32)
            women_frames.append(wdf)

        # --- PUMA cells, main weight only
        w0 = W[:, 0]
        cell = pd.DataFrame({
            "STATE": df.STATE.to_numpy(), "PUMA": df.PUMA.to_numpy(),
            "pop": w0, "pop_union": w0 * union,
            "ct_lf": w0 * ct_base, "ct_lf_union": w0 * (ct_base & union),
            "ct_ls": w0 * (ct_base & ls), "ct_ls_union": w0 * (ct_base & ls & union),
            "c08_lf": w0 * civ, "c08_lf_union": w0 * (civ & union),
            "c08_lsi": w0 * (civ & fb & ls), "c08_lsi_union": w0 * (civ & fb & ls & union),
            "bmw_wa": w0 * wa, "bmw_wa_union": w0 * (wa & union),
            "bmw_lowed_fb": w0 * (wa & fb & (schl <= 18)),
            "bmw_lowed_fb_union": w0 * (wa & fb & (schl <= 18) & union),
            "e65_other_nat": w0 * (old & ~union & nat), "e65_other": w0 * (old & ~union),
        })
        puma_frames.append(cell.groupby(["STATE", "PUMA"]).sum())
        print(f"  records so far {n_records:,}", flush=True)

    # ------------------------------------------------------------------ national totals
    rows = []
    for name, vec in totals.items():
        est, se = sdr(vec)
        rows.append({"item": name, "estimate": est, "se": se})
    nat = pd.DataFrame(rows).sort_values("item")
    nat.to_csv(OUT / "acs_national.csv", index=False)
    pop = float(totals["pop_all"][0])
    if abs(pop - ACS_TOTAL_POP) > POP_TOLERANCE:
        raise SystemExit(f"[BLOCKED] weighted population {pop:,.0f} != {ACS_TOTAL_POP:,}")

    # ------------------------------------------------------------------ care workforce
    work = pd.concat(work_frames).groupby(level=[0, 1, 2, 3, 4, 5], dropna=False).sum()
    out = []
    for key, row in work.iterrows():
        occp, indp, group, lu, mx, lo = key
        wv = row[["w"] + REPS].to_numpy(float)
        hv = row[["h"] + [f"h{r}" for r in REPS]].to_numpy(float)
        out.append({"occp": int(occp), "occupation": OCC[int(occp)],
                    "indp": int(indp) if pd.notna(indp) else -1,
                    "sector": SECTOR.get(int(indp), "other") if pd.notna(indp) else "none",
                    "group": group, "likely_undocumented": bool(lu), "mexico_born": bool(mx),
                    "lowed_fb": bool(lo),
                    "workers": wv[0], "hours": hv[0]})
    pd.DataFrame(out).to_csv(OUT / "acs_care_workforce.csv", index=False)
    # replicate-weight SEs for the union share of hours in the lane's two key markets
    se_rows = []
    wk = work.reset_index()
    wk["sector"] = wk.INDP.map(lambda x: SECTOR.get(int(x), "other") if pd.notna(x) else "none")
    hcols = ["h"] + [f"h{r}" for r in REPS]
    markets = {
        "home_care_aaf": (wk.OCCP.isin([3601, 3602, 4230]) & wk.sector.isin(
            ["home_health_care", "private_households"])),
        "home_care_broad": (wk.OCCP.isin([3601, 3602, 4230]) & wk.sector.isin(
            ["home_health_care", "private_households", "individual_family_services"])),
        # Kreider–Werner: aides (2010 codes 3600, 4610) in home health, individual and
        # family services, and private households
        "home_care_kw": (wk.OCCP.isin([3601, 3602, 3603, 3605]) & wk.sector.isin(
            ["home_health_care", "private_households", "individual_family_services"])),
        "direct_care_all": wk.OCCP.isin([3601, 3602, 3603, 3605]),
        "nursing_facility_cna": wk.OCCP.isin([3603]) & wk.sector.eq("nursing_care_facilities"),
        "household_services_ev": wk.OCCP.isin([4230, 4600]),
        "maids": wk.OCCP.eq(4230),
        "childcare_workers": wk.OCCP.eq(4600),
        "landscaping": wk.OCCP.eq(4251),
    }
    for mname, mmask in markets.items():
        allv = wk.loc[mmask, hcols].sum().to_numpy(float)
        for g in ["union_fb", "union_nat"]:
            gv = wk.loc[mmask & wk.group.eq(g), hcols].sum().to_numpy(float)
            est, se = sdr(gv / allv)
            se_rows.append({"market": mname, "group": g, "hours_share": est, "se": se,
                            "hours_total": allv[0]})
        gv = wk.loc[mmask & wk.group.isin(["union_fb", "union_nat"]), hcols].sum().to_numpy(float)
        est, se = sdr(gv / allv)
        se_rows.append({"market": mname, "group": "union", "hours_share": est, "se": se,
                        "hours_total": allv[0]})
        gv = wk.loc[mmask & wk.lowed_fb.astype(bool), hcols].sum().to_numpy(float)
        est, se = sdr(gv / allv)
        se_rows.append({"market": mname, "group": "lowed_fb_all_origins", "hours_share": est,
                        "se": se, "hours_total": allv[0]})
    pd.DataFrame(se_rows).to_csv(OUT / "acs_care_market_shares.csv", index=False)

    # ------------------------------------------------------------------ women populations
    women = pd.concat(women_frames, ignore_index=True)
    adj = women.ADJINC / 1e6
    ann_hours = women.WKHP.fillna(0) * women.WKWN.fillna(0)
    wage_inc = women.WAGP.fillna(0) * adj
    earn = women.PERNP.fillna(0) * adj
    with np.errstate(divide="ignore", invalid="ignore"):
        hourly_wage = np.where(ann_hours > 0, wage_inc / ann_hours, np.nan)
        hourly_earn = np.where(ann_hours > 0, earn / ann_hours, np.nan)
    native = women.NATIVITY == 1
    pos_wage = (wage_inc > 0) & (ann_hours > 0)
    # quartile cut-off within census division, among native women 20-64 with a positive wage
    women["hourly_wage"], women["hourly_earn"], women["ann_hours"] = hourly_wage, hourly_earn, ann_hours
    women["earn"] = earn
    cut = {}
    for div, d in women[native & pos_wage].groupby("DIVISION"):
        order = np.argsort(d.hourly_wage.to_numpy())
        hw = d.hourly_wage.to_numpy()[order]
        cw = np.cumsum(d.w.to_numpy()[order]) / d.w.sum()
        cut[int(div)] = float(hw[np.searchsorted(cw, 0.75)])
    base_all = pos_wage.to_numpy()
    hwv = women.hourly_wage.to_numpy()
    nat_cut = float(np.nan)
    d = women[pos_wage]
    order = np.argsort(d.hourly_wage.to_numpy())
    nat_cut = float(d.hourly_wage.to_numpy()[order][np.searchsorted(
        np.cumsum(d.w.to_numpy()[order]) / d.w.sum(), 0.75)])
    women["p75_div"] = women.DIVISION.map(lambda x: cut.get(int(x), np.nan))
    top_div = base_all & (hwv >= women.p75_div.to_numpy())
    top_nat = base_all & (hwv >= nat_cut)
    union_w = women.union.to_numpy()
    college = women.SCHL.to_numpy() >= 21
    young_kids = women.PAOC.isin([1, 3]).to_numpy()
    age = women.AGEP.to_numpy()
    pops = {
        "ct_topq_div_native_nonunion": top_div & native.to_numpy() & ~union_w,
        "ct_topq_div_native_union": top_div & native.to_numpy() & union_w,
        "ct_topq_div_foreign_nonunion": top_div & ~native.to_numpy() & ~union_w,
        "ct_topq_nat_native_college_nonunion": top_nat & native.to_numpy() & college & ~union_w,
        "ct_topq_nat_native_college_all": top_nat & native.to_numpy() & college,
        "ev_college_mothers_u6_native_nonunion": (native.to_numpy() & ~union_w & college
                                                   & young_kids & (age <= 63)),
        "ev_college_mothers_u6_foreign_nonunion": (~native.to_numpy() & ~union_w & college
                                                    & young_kids & (age <= 63)),
        "ev_college_women_nokids_native_nonunion": (native.to_numpy() & ~union_w & college
                                                     & women.PAOC.eq(4).to_numpy() & (age <= 63)),
        "ev_college_women_all_native_nonunion": native.to_numpy() & ~union_w & college & (age <= 63),
    }
    Wm = women[["w"] + REPS].to_numpy(float)
    wkhp0 = women.WKHP.fillna(0).to_numpy()
    wkwn0 = women.WKWN.fillna(0).to_numpy()
    he = np.nan_to_num(women.hourly_earn.to_numpy())
    rows = []
    for pname, m in pops.items():
        cnt = sdr(Wm[m].sum(axis=0))
        w0 = Wm[m, 0]
        working = m & (wkhp0 > 0) & (wkwn0 > 0)
        wk0 = Wm[working, 0]
        rows.append({
            "population": pname, "women": cnt[0], "women_se": cnt[1],
            "share_working": float(wk0.sum() / w0.sum()),
            "mean_usual_hours_incl_zero": float((w0 * wkhp0[m]).sum() / w0.sum()),
            "mean_usual_hours_workers": float((wk0 * wkhp0[working]).sum() / wk0.sum()),
            "mean_weeks_workers": float((wk0 * wkwn0[working]).sum() / wk0.sum()),
            "earnings_bn": float((w0 * women.earn.to_numpy()[m]).sum() / 1e9),
            "annual_hours_bn": float((w0 * ann_hours.to_numpy()[m]).sum() / 1e9),
            # dollar value of one more usual weekly hour for every working member, $bn a year
            "value_one_weekly_hour_bn": float((wk0 * wkwn0[working] * he[working]).sum() / 1e9),
        })
    wpop = pd.DataFrame(rows)
    wpop.to_csv(OUT / "acs_women.csv", index=False)

    # PUMA cells for the women (value of one weekly hour, earnings) joined to the other cells
    women["ct_value_hour"] = np.where(pops["ct_topq_div_native_nonunion"] & (wkhp0 > 0),
                                      women.w * wkwn0 * he, 0.0)
    women["ct_women"] = np.where(pops["ct_topq_div_native_nonunion"], women.w, 0.0)
    women["ev_earn"] = np.where(pops["ev_college_mothers_u6_native_nonunion"],
                                women.w * women.earn, 0.0)
    women["ev_women"] = np.where(pops["ev_college_mothers_u6_native_nonunion"], women.w, 0.0)
    women["ev_all_earn"] = np.where(pops["ev_college_women_all_native_nonunion"],
                                    women.w * women.earn, 0.0)
    wcells = women.groupby(["STATE", "PUMA"])[["ct_value_hour", "ct_women", "ev_earn",
                                               "ev_women", "ev_all_earn"]].sum()
    puma = pd.concat(puma_frames).groupby(level=[0, 1]).sum().join(wcells, how="left").fillna(0.0)
    puma.reset_index().to_csv(OUT / "acs_puma_cells.csv", index=False)

    audit = {
        "source_zip": str(ZIP.relative_to(ROOT)), "zip_sha256": sha256(ZIP),
        "records": n_records, "weighted_population": pop,
        "gate_population_equals_acs_total": abs(pop - ACS_TOTAL_POP) <= POP_TOLERANCE,
        "union_acs_persons": float(totals["pop_union"][0]),
        "female_p75_hourly_wage_by_division_native_20_64": cut,
        "female_p75_hourly_wage_national_all_20_64": nat_cut,
        "puma_cells": int(len(puma)),
        "gate_puma_pop_sum": float(puma["pop"].sum()),
    }
    (OUT / "acs_audit.json").write_text(json.dumps(audit, indent=2))
    print(json.dumps(audit, indent=2))
    print(wpop.to_string(index=False))


if __name__ == "__main__":
    main()
