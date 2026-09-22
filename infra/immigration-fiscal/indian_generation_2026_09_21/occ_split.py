#!/usr/bin/env python3
"""ACS 2023 + CPS ASEC: is the Indian earnings gap just computer/IT occupations?

ACS identifies India-born and US-born Asian Indian ancestry (G2+G3 mix).
CPS identifies true G2 (US-born, India-born parent) via PEFNTVTY/PEMNTVTY.
H-1B is unobserved; ACS CIT=5 & YOEP>=2018 is the same recent-noncitizen proxy
as CPS PEINUSYR>=26 in indian_ledger_2026_09_18.

Run: OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy \\
     python3 occ_split.py
"""
from __future__ import annotations

import csv
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "build"))
import paths as _data_paths  # noqa: E402

import numpy as np
import pandas as pd

from analyze_cps import GROUPS, ZIPS, masks
OUT = HERE / "derived"
OUT.mkdir(exist_ok=True)
PERSON_ZIP = _data_paths.data_root(require_exists=False) / "census/acs_pums_2023_person.zip"
DICT_CSV = HERE.parent / "indian_ledger_2026_09_18" / "_cache" / "PUMS_Data_Dictionary_2023.csv"
ANC_ASIAN_INDIAN = 615
ACS_COLS = [
    "PWGTP", "AGEP", "RAC1P", "HISP", "NATIVITY", "POBP", "ANC1P", "ANC2P",
    "SCHL", "PINCP", "WAGP", "ADJINC", "ESR", "OCCP", "CIT", "YOEP",
]
SOFTWARE = {1021}
CIS_MGR = {110}
HW_ENG = {1400}
PHYS = {3090, 3100}
MATH = {1200, 1220, 1240}
BIN_ORDER = [
    "software", "other_computer", "cis_manager", "computer_hardware",
    "math", "physician", "other_healthcare", "other_engineer",
    "other_manager", "rest",
]
COLLAPSE = {
    "software": "it_broad",
    "other_computer": "it_broad",
    "cis_manager": "it_broad",
    "computer_hardware": "it_broad",
    "math": "other_stem",
    "physician": "physician",
    "other_healthcare": "other_healthcare",
    "other_engineer": "other_engineer",
    "other_manager": "other_manager",
    "rest": "rest",
}
COLLAPSE_ORDER = [
    "it_broad", "physician", "other_engineer", "other_healthcare",
    "other_manager", "other_stem", "rest",
]


def occ_labels(path: Path) -> dict[int, str]:
    occ = {}
    with path.open(newline="", encoding="latin-1") as f:
        for row in csv.reader(f):
            if len(row) >= 7 and row[0] == "VAL" and row[1] == "OCCP":
                try:
                    occ[int(row[4])] = row[6]
                except ValueError:
                    continue
    return occ


def code_sets(labs: dict[int, str]) -> dict[str, set[int]]:
    cmm = {c for c, lab in labs.items() if lab.startswith("CMM-")}
    med = {c for c, lab in labs.items() if lab.startswith("MED-")}
    eng = {c for c, lab in labs.items() if lab.startswith("ENG-")}
    mgr = {c for c, lab in labs.items() if lab.startswith("MGR-")}
    computer = cmm - MATH
    return {
        "software": SOFTWARE,
        "other_computer": computer - SOFTWARE,
        "cis_manager": CIS_MGR,
        "computer_hardware": HW_ENG,
        "math": MATH,
        "physician": PHYS,
        "other_healthcare": med - PHYS,
        "other_engineer": eng - HW_ENG,
        "other_manager": mgr - CIS_MGR,
    }


def bin_codes(codes: np.ndarray, sets: dict[str, set[int]]) -> np.ndarray:
    out = np.full(len(codes), "rest", dtype=object)
    valid = np.isfinite(codes)
    c = np.where(valid, codes, -1).astype(int)
    for name in BIN_ORDER:
        if name == "rest":
            continue
        out[np.isin(c, list(sets[name]))] = name
    out[~valid] = "unknown"
    return out


def wmean(x, w):
    s = w.sum()
    return float("nan") if s <= 0 else float(np.dot(x, w) / s)


def wmedian(x, w):
    order = np.argsort(x, kind="stable")
    x, w = x[order], w[order]
    cdf = np.cumsum(w) / w.sum()
    return float(x[np.searchsorted(cdf, 0.5)])


def load_acs(path: Path) -> pd.DataFrame:
    frames = []
    with zipfile.ZipFile(path) as z:
        members = sorted(n for n in z.namelist() if n.lower().endswith(".csv"))
        header = z.open(members[0]).readline().decode().strip().split(",")
        want = [c for c in ACS_COLS if c in header]
        missing = [c for c in ACS_COLS if c not in header]
        if missing:
            print(f"  ACS missing {missing}", flush=True)
        for i, name in enumerate(members, 1):
            print(f"  [{i}/{len(members)}] {name}", flush=True)
            frames.append(pd.read_csv(z.open(name), usecols=want, low_memory=False))
    d = pd.concat(frames, ignore_index=True)
    print(f"  person rows {len(d):,}", flush=True)
    return d


def kitagawa(share_g, mean_g, share_r, mean_r):
    """Mix uses reference means; within uses reference shares; interaction residual."""
    mix = float(np.sum((share_g - share_r) * mean_r))
    within = float(np.sum(share_r * (mean_g - mean_r)))
    inter = float(np.sum((share_g - share_r) * (mean_g - mean_r)))
    return mix, within, inter, mix + within + inter


def tabulate(group_masks: dict[str, np.ndarray], bins: np.ndarray, income: np.ndarray,
             wage: np.ndarray, w: np.ndarray, universe: np.ndarray, label: str) -> pd.DataFrame:
    rows = []
    for gname, gmask in group_masks.items():
        use = gmask & universe & np.isfinite(income)
        if use.sum() == 0:
            continue
        ww, yy, wg = w[use], income[use], wage[use]
        bb = bins[use]
        rec_base = {
            "source": label, "group": gname, "n": int(use.sum()),
            "weighted": float(ww.sum()),
            "mean_pinc": wmean(yy, ww),
            "median_pinc": wmedian(yy, ww),
            "mean_wag": wmean(wg[np.isfinite(wg)], ww[np.isfinite(wg)]) if np.isfinite(wg).any() else float("nan"),
        }
        for bname in BIN_ORDER + ["unknown"]:
            hit = bb == bname
            rec = {
                **rec_base, "bin": bname, "collapse": COLLAPSE.get(bname, bname),
                "n_bin": int(hit.sum()),
                "share": float(ww[hit].sum() / ww.sum()) if ww.sum() else float("nan"),
            }
            if hit.sum() == 0:
                rec["mean_pinc_bin"] = rec["median_pinc_bin"] = rec["mean_wag_bin"] = float("nan")
            else:
                rec["mean_pinc_bin"] = wmean(yy[hit], ww[hit])
                rec["median_pinc_bin"] = wmedian(yy[hit], ww[hit])
                finite = np.isfinite(wg[hit])
                rec["mean_wag_bin"] = wmean(wg[hit][finite], ww[hit][finite]) if finite.any() else float("nan")
            rows.append(rec)
        it = np.isin(bb, ["software", "other_computer", "cis_manager", "computer_hardware"])
        md = bb == "physician"
        eng = bb == "other_engineer"
        for sub, name in [
            (~it, "not_it"),
            (~it & ~md, "not_it_not_md"),
            (~it & ~md & ~eng, "not_it_not_md_not_eng"),
        ]:
            rec = {
                **rec_base, "bin": name, "collapse": name,
                "n_bin": int(sub.sum()),
                "share": float(ww[sub].sum() / ww.sum()) if ww.sum() else float("nan"),
            }
            if sub.sum() == 0:
                rec["mean_pinc_bin"] = rec["median_pinc_bin"] = rec["mean_wag_bin"] = float("nan")
            else:
                rec["mean_pinc_bin"] = wmean(yy[sub], ww[sub])
                rec["median_pinc_bin"] = wmedian(yy[sub], ww[sub])
                finite = np.isfinite(wg[sub])
                rec["mean_wag_bin"] = wmean(wg[sub][finite], ww[sub][finite]) if finite.any() else float("nan")
            rows.append(rec)
    return pd.DataFrame(rows)


def decompose(tab: pd.DataFrame, source: str, focal: str, ref: str, bins: list[str],
              share_col="share", mean_col="mean_pinc_bin") -> dict:
    t = tab[(tab.source == source) & tab.bin.isin(bins)]
    g = t[t.group == focal].set_index("bin")
    r = t[t.group == ref].set_index("bin")
    common = [b for b in bins if b in g.index and b in r.index]
    sg = g.loc[common, share_col].to_numpy(float)
    sr = r.loc[common, share_col].to_numpy(float)
    yg = g.loc[common, mean_col].to_numpy(float)
    yr = r.loc[common, mean_col].to_numpy(float)
    # renormalise in case unknown leaked
    sg = sg / sg.sum()
    sr = sr / sr.sum()
    mix, within, inter, tot = kitagawa(sg, yg, sr, yr)
    y_g = float(g.iloc[0]["mean_pinc"]) if "mean_pinc" in g.columns else float(np.dot(sg, yg))
    y_r = float(r.iloc[0]["mean_pinc"]) if "mean_pinc" in r.columns else float(np.dot(sr, yr))
    return {
        "source": source, "focal": focal, "ref": ref, "bins": "+".join(bins),
        "focal_mean": y_g, "ref_mean": y_r, "raw_gap": y_g - y_r,
        "mix": mix, "within": within, "interaction": inter, "kitagawa_sum": tot,
        "mix_share_of_gap": mix / (y_g - y_r) if y_g != y_r else float("nan"),
        "within_share_of_gap": within / (y_g - y_r) if y_g != y_r else float("nan"),
    }


def acs_groups(d: pd.DataFrame) -> dict[str, np.ndarray]:
    nativity = d.NATIVITY.to_numpy()
    anc = (d.ANC1P.eq(ANC_ASIAN_INDIAN) | d.ANC2P.eq(ANC_ASIAN_INDIAN)).to_numpy()
    india = d.POBP.eq(210).to_numpy()
    yoep = pd.to_numeric(d.YOEP, errors="coerce").to_numpy()
    cit = d.CIT.to_numpy()
    recent = india & (cit == 5) & np.isfinite(yoep) & (yoep >= 2018)
    return {
        "us_born_nh_white": (nativity == 1) & d.RAC1P.eq(1).to_numpy() & d.HISP.eq(1).to_numpy(),
        "india_born": india,
        "india_born_recent_noncit": recent,
        "india_born_settled": india & ~recent,
        "us_born_asian_indian_anc": (nativity == 1) & anc,
    }


def run_acs(labs: dict[int, str], sets: dict[str, set[int]]) -> pd.DataFrame:
    print(f"[1] ACS {PERSON_ZIP}", flush=True)
    if not PERSON_ZIP.exists():
        raise SystemExit(f"missing {PERSON_ZIP}")
    d = load_acs(PERSON_ZIP)
    adj = d.ADJINC.to_numpy(float) / 1_000_000.0
    pinc = np.where(d.PINCP.to_numpy(float) == -19999, np.nan, d.PINCP.to_numpy(float) * adj)
    wag = np.where(d.WAGP.to_numpy(float) == -19999, np.nan, d.WAGP.to_numpy(float) * adj)
    occp = pd.to_numeric(d.OCCP, errors="coerce").to_numpy(float)
    bins = bin_codes(occp, sets)
    esr = pd.to_numeric(d.ESR, errors="coerce").to_numpy()
    employed = np.isin(esr, [1, 2, 4, 5])
    age = d.AGEP.to_numpy()
    adult = (age >= 25) & (age <= 64)
    w = d.PWGTP.to_numpy(float)
    groups = acs_groups(d)
    tab = tabulate(groups, bins, pinc, wag, w, adult & employed, "acs2023_employed_25_64")
    tab.to_csv(OUT / "acs_occ_earnings.csv", index=False, float_format="%.6f")
    print(f"  wrote {OUT / 'acs_occ_earnings.csv'} ({len(tab)} rows)", flush=True)
    return tab


def run_cps(sets: dict[str, set[int]]) -> pd.DataFrame:
    print("[2] CPS ASEC 2022-2026 OCCUP of longest job last year", flush=True)
    extra = ["OCCUP", "PEIOOCC", "PEMLR", "PEARNVAL"]
    frames = []
    for year, path in ZIPS.items():
        print(f"  {year} {path.name}", flush=True)
        person = f"pppub{year % 100:02d}.csv"
        with zipfile.ZipFile(path) as z:
            header = z.open(person).readline().decode().strip().split(",")
            base = ["PH_SEQ", "PPPOS", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY",
                    "PEFNTVTY", "PEMNTVTY", "PEHSPNON", "PRDTRACE", "PRDASIAN",
                    "MARSUPWT", "PEARNVAL"]
            cols = [c for c in base + extra if c in header]
            d = pd.read_csv(z.open(person), usecols=cols, low_memory=False)
        d["year"] = year
        if "PRDASIAN" not in d.columns:
            d["PRDASIAN"] = np.nan
        frames.append(d)
    d = pd.concat(frames, ignore_index=True)
    m = masks(d)
    adult = d.A_AGE.between(25, 64).to_numpy() & d.PRPERTYP.eq(2).to_numpy()
    occ = pd.to_numeric(d.OCCUP, errors="coerce").to_numpy(float)
    occ = np.where(occ <= 0, np.nan, occ)
    bins = bin_codes(occ, sets)
    earn = d.PEARNVAL.to_numpy(float)
    w = d.MARSUPWT.to_numpy(float) / 100.0  # ASEC person weight
    # Longest-job occupation is filled when the person had a job last year.
    had_job = np.isfinite(occ)
    groups = {k: m[k] for k in GROUPS}
    tab = tabulate(groups, bins, earn, earn, w, adult & had_job, "cps_pool_occup_25_64")
    tab.to_csv(OUT / "cps_occ_earnings.csv", index=False, float_format="%.6f")
    print(f"  wrote {OUT / 'cps_occ_earnings.csv'} ({len(tab)} rows)", flush=True)
    return tab


def print_gap_block(tab: pd.DataFrame, source: str, focals: list[str], ref: str, income_name: str):
    t = tab[tab.source == source]
    ref_all = t[(t.group == ref) & (t.bin == "software")].iloc[0]
    print(f"\n== {source}: {income_name} vs {ref} ==", flush=True)
    header = (f"{'group':28} {'n':>7} {'mean':>10} {'gap':>9}  "
              f"{'IT%':>6} {'soft%':>6} {'MD%':>5}  "
              f"{'notIT':>10} {'ΔnotIT':>9}  "
              f"{'notITMD':>10} {'ΔexMD':>9}")
    print(header, flush=True)
    ref_not = t[(t.group == ref) & (t.bin == "not_it")].iloc[0]
    ref_not2 = t[(t.group == ref) & (t.bin == "not_it_not_md")].iloc[0]
    for g in focals:
        g_all = t[(t.group == g) & (t.bin == "software")]
        if g_all.empty:
            continue
        g_all = g_all.iloc[0]
        git = t[(t.group == g) & t.bin.isin(["software", "other_computer", "cis_manager", "computer_hardware"])]
        it_share = float(git["share"].sum())
        soft = float(t[(t.group == g) & (t.bin == "software")].iloc[0]["share"])
        md = float(t[(t.group == g) & (t.bin == "physician")].iloc[0]["share"])
        notit = t[(t.group == g) & (t.bin == "not_it")].iloc[0]
        not2 = t[(t.group == g) & (t.bin == "not_it_not_md")].iloc[0]
        print(
            f"{g:28} {int(g_all['n']):7,d} {g_all['mean_pinc']:10,.0f} "
            f"{g_all['mean_pinc']-ref_all['mean_pinc']:+9,.0f}  "
            f"{it_share:6.1%} {soft:6.1%} {md:5.1%}  "
            f"{notit['mean_pinc_bin']:10,.0f} {notit['mean_pinc_bin']-ref_not['mean_pinc_bin']:+9,.0f}  "
            f"{not2['mean_pinc_bin']:10,.0f} {not2['mean_pinc_bin']-ref_not2['mean_pinc_bin']:+9,.0f}",
            flush=True,
        )


def main():
    labs = occ_labels(DICT_CSV)
    sets = code_sets(labs)
    computer = sets["software"] | sets["other_computer"]
    print(f"  CMM computer codes {len(computer)}; software {SOFTWARE}", flush=True)
    acs = run_acs(labs, sets)
    cps = run_cps(sets)
    print_gap_block(
        acs, "acs2023_employed_25_64",
        ["india_born", "india_born_recent_noncit", "india_born_settled", "us_born_asian_indian_anc"],
        "us_born_nh_white", "PINCP",
    )
    print_gap_block(
        cps, "cps_pool_occup_25_64",
        ["india_g1", "india_g2", "india_g3plus_race", "asian_indian_native_selfid"],
        "white_g3plus", "PEARNVAL",
    )
    decomp_rows = []
    # Build collapsed two-bin shares for Kitagawa
    for tab, source, focals, ref in [
        (acs, "acs2023_employed_25_64",
         ["india_born", "india_born_recent_noncit", "india_born_settled", "us_born_asian_indian_anc"],
         "us_born_nh_white"),
        (cps, "cps_pool_occup_25_64",
         ["india_g1", "india_g2", "india_g3plus_race"],
         "white_g3plus"),
    ]:
        for focal in focals:
            sub = tab[(tab.source == source) & (tab.group == focal)]
            refsub = tab[(tab.source == source) & (tab.group == ref)]
            if sub.empty or refsub.empty:
                continue
            fine = BIN_ORDER
            decomp_rows.append(decompose(tab, source, focal, ref, fine))
            # two-bin IT vs rest
            g_it = float(sub[sub.bin.isin(["software", "other_computer", "cis_manager", "computer_hardware"])]["share"].sum())
            r_it = float(refsub[refsub.bin.isin(["software", "other_computer", "cis_manager", "computer_hardware"])]["share"].sum())
            g_yit = wmean_from_rows(sub, ["software", "other_computer", "cis_manager", "computer_hardware"])
            r_yit = wmean_from_rows(refsub, ["software", "other_computer", "cis_manager", "computer_hardware"])
            g_yn = float(sub[sub.bin == "not_it"].iloc[0]["mean_pinc_bin"])
            r_yn = float(refsub[refsub.bin == "not_it"].iloc[0]["mean_pinc_bin"])
            mix, within, inter, tot = kitagawa(
                np.array([g_it, 1 - g_it]), np.array([g_yit, g_yn]),
                np.array([r_it, 1 - r_it]), np.array([r_yit, r_yn]),
            )
            g_mean = float(sub.iloc[0]["mean_pinc"])
            r_mean = float(refsub.iloc[0]["mean_pinc"])
            decomp_rows.append({
                "source": source, "focal": focal, "ref": ref, "bins": "it_broad+not_it",
                "focal_mean": g_mean, "ref_mean": r_mean, "raw_gap": g_mean - r_mean,
                "mix": mix, "within": within, "interaction": inter, "kitagawa_sum": tot,
                "mix_share_of_gap": mix / (g_mean - r_mean) if g_mean != r_mean else float("nan"),
                "within_share_of_gap": within / (g_mean - r_mean) if g_mean != r_mean else float("nan"),
            })
    decomp = pd.DataFrame(decomp_rows)
    decomp.to_csv(OUT / "occ_kitagawa.csv", index=False, float_format="%.6f")
    print("\n== Kitagawa (IT vs not-IT, mix at white means) ==", flush=True)
    k = decomp[decomp.bins == "it_broad+not_it"]
    for _, r in k.iterrows():
        print(f"  {r.source:24} {r.focal:28} gap {r.raw_gap:+,.0f}  "
              f"mix {r.mix:+,.0f} ({r.mix_share_of_gap:.0%})  "
              f"within {r.within:+,.0f} ({r.within_share_of_gap:.0%})  "
              f"inter {r.interaction:+,.0f}", flush=True)


def wmean_from_rows(sub: pd.DataFrame, bins: list[str]) -> float:
    part = sub[sub.bin.isin(bins)]
    w = part.share.to_numpy(float)
    y = part.mean_pinc_bin.to_numpy(float)
    keep = np.isfinite(y) & (w > 0)
    return float(np.dot(y[keep], w[keep]) / w[keep].sum()) if keep.any() else float("nan")


if __name__ == "__main__":
    main()
