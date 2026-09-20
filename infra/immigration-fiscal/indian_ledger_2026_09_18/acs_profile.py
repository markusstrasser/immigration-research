#!/usr/bin/env python3
"""ACS 2024 1-year PUMS profile: India-born vs China-born vs all foreign-born vs US-born.

Measures the household-level and labour-market traits the brief names: education, household
income, occupation concentration, self-employment and the industry of the self-employed,
naturalisation by years in the US, English, spousal endogamy and geographic concentration.

Point estimates on the full person weight PWGTP (household items on WGTP). Successive-difference
replicate standard errors are NOT computed here: the 80 replicate columns would be ~2 GB for the
national file and every cell reported below has an unweighted n in the thousands. Unweighted cell
counts are printed with every number so the reader can judge precision.

Inputs (defaults are the local read-only copies):
  person    ~/research-data/.../acs_pums_2024_1yr/csv_pus.zip   (psam_pusa.csv, psam_pusb.csv)
  household _cache/csv_hus_2024.zip                              (psam_husa.csv, psam_husb.csv)
  dictionary ~/research-data/.../acs_pums_dict/PUMS_Data_Dictionary_2024.csv

Run: uv run --no-project --with "pandas>=2" --with "numpy>=2" python3 acs_profile.py
"""
from __future__ import annotations

import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "build"))
import paths as _data_paths


import argparse
import csv
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = _data_paths.data_root(require_exists=False) / 'external'

PERSON_COLS = ["SERIALNO", "SPORDER", "PWGTP", "ST", "PUMA", "AGEP", "SEX", "CIT", "NATIVITY",
               "POBP", "YOEP", "SCHL", "ENG", "OCCP", "INDP", "COW", "ESR", "WAGP", "PINCP",
               "ANC1P", "ANC2P", "RELSHIPP", "MSP", "ADJINC"]
HOUSE_COLS = ["SERIALNO", "WGTP", "HINCP", "ADJINC", "TYPEHUGQ", "NP"]

INDIA, CHINA, HONGKONG, TAIWAN, MEXICO = 210, 207, 209, 240, 303
ANC_ASIAN_INDIAN = 615


def load_person(zip_path: Path) -> pd.DataFrame:
    frames = []
    with zipfile.ZipFile(zip_path) as z:
        members = sorted(n for n in z.namelist() if n.lower().endswith(".csv"))
        header = z.open(members[0]).readline().decode().strip().split(",")
        # The 2023 vintage names the state column STATE, the 2024 vintage ST.
        state_col = "ST" if "ST" in header else "STATE"
        want = [state_col if c == "ST" else c for c in PERSON_COLS]
        for i, name in enumerate(members, 1):
            print(f"  [{i}/{len(members)}] reading {name}", flush=True)
            part = pd.read_csv(z.open(name), usecols=want, dtype={"SERIALNO": "string"},
                               na_values=[], keep_default_na=False, low_memory=False)
            part = part.rename(columns={state_col: "ST"})
            for c in PERSON_COLS:
                if c != "SERIALNO":
                    part[c] = pd.to_numeric(part[c], errors="coerce")
            frames.append(part)
    d = pd.concat(frames, ignore_index=True)
    print(f"  person rows {len(d):,}", flush=True)
    return d


def load_household(zip_path: Path) -> pd.DataFrame:
    frames = []
    with zipfile.ZipFile(zip_path) as z:
        members = sorted(n for n in z.namelist() if n.lower().endswith(".csv"))
        for i, name in enumerate(members, 1):
            print(f"  [{i}/{len(members)}] reading {name}", flush=True)
            part = pd.read_csv(z.open(name), usecols=HOUSE_COLS, dtype={"SERIALNO": "string"},
                               na_values=[], keep_default_na=False, low_memory=False)
            for c in HOUSE_COLS:
                if c != "SERIALNO":
                    part[c] = pd.to_numeric(part[c], errors="coerce")
            frames.append(part)
    h = pd.concat(frames, ignore_index=True)
    print(f"  household rows {len(h):,}", flush=True)
    return h


def occ_labels(dict_csv: Path) -> tuple[dict[int, str], dict[int, str]]:
    occ, ind = {}, {}
    with dict_csv.open(newline="", encoding="latin-1") as f:
        for row in csv.reader(f):
            # VAL rows are: VAL,<var>,C,<len>,<min>,<max>,<label> — the label is field 6.
            if len(row) >= 7 and row[0] == "VAL" and row[1] in ("OCCP", "INDP"):
                try:
                    code = int(row[4])
                except ValueError:
                    continue
                (occ if row[1] == "OCCP" else ind)[code] = row[6]
    return occ, ind


def wmedian(values: np.ndarray, weights: np.ndarray) -> float:
    keep = np.isfinite(values) & (weights > 0)
    v, w = values[keep], weights[keep]
    if len(v) == 0:
        return float("nan")
    order = np.argsort(v, kind="stable")
    v, w = v[order], w[order]
    cum = np.cumsum(w) / w.sum()
    return float(v[np.searchsorted(cum, 0.5)])


def share(mask: np.ndarray, weight: np.ndarray, universe: np.ndarray) -> float:
    den = weight[universe].sum()
    return float(weight[universe & mask].sum() / den) if den > 0 else float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, default=2023)
    ap.add_argument("--person-zip", type=Path,
                    default=_data_paths.data_root(require_exists=False) / 'census/acs_pums_2023_person.zip')
    ap.add_argument("--household-zip", type=Path,
                    default=_data_paths.data_root(require_exists=False) / 'census/acs_pums_2023_household.zip')
    ap.add_argument("--dictionary", type=Path,
                    default=HERE / "_cache" / "PUMS_Data_Dictionary_2023.csv")
    ap.add_argument("--tag", default="2023")
    ap.add_argument("--out", type=Path, default=HERE / "derived")
    args = ap.parse_args()
    global YEAR
    YEAR = args.year
    args.out.mkdir(parents=True, exist_ok=True)

    print("[1/5] person file", flush=True)
    d = load_person(args.person_zip)
    print("[2/5] household file", flush=True)
    h = load_household(args.household_zip) if args.household_zip.exists() else None
    occ_lab, ind_lab = occ_labels(args.dictionary)

    w = d.PWGTP.to_numpy(dtype=float)
    age = d.AGEP.to_numpy()
    pobp = d.POBP.to_numpy()
    nativity = d.NATIVITY.to_numpy()
    anc1, anc2 = d.ANC1P.to_numpy(), d.ANC2P.to_numpy()

    groups = {
        "india_born": pobp == INDIA,
        "china_born": pobp == CHINA,
        "china_born_broad": np.isin(pobp, [CHINA, HONGKONG, TAIWAN]),
        "mexico_born": pobp == MEXICO,
        "all_foreign_born": nativity == 2,
        "us_born": nativity == 1,
        "us_born_asian_indian_anc": (nativity == 1) & ((anc1 == ANC_ASIAN_INDIAN)
                                                       | (anc2 == ANC_ASIAN_INDIAN)),
    }
    order = ["india_born", "china_born", "china_born_broad", "mexico_born",
             "all_foreign_born", "us_born", "us_born_asian_indian_anc"]

    adults = (age >= 25) & (age <= 64)
    employed = np.isin(d.ESR.to_numpy(), [1, 2, 4, 5])
    schl = d.SCHL.to_numpy()
    occp = d.OCCP.to_numpy()
    indp = d.INDP.to_numpy()
    cow = d.COW.to_numpy()
    cit = d.CIT.to_numpy()
    eng = d.ENG.to_numpy()
    yoep = d.YOEP.to_numpy()

    cmm_codes = np.array(sorted(c for c, lab in occ_lab.items() if lab.startswith("CMM-")))
    cmm = np.isin(occp, cmm_codes)
    phys = np.isin(occp, [3090, 3100])

    rows = []

    def add(group, metric, value, n, universe_label):
        rows.append({"group": group, "metric": metric, "value": value,
                     "n_unweighted": int(n), "universe": universe_label})

    print("[3/5] education, income, occupation, self-employment", flush=True)
    for g in order:
        m = groups[g]
        u = m & adults
        add(g, "population_all_ages", float(w[m].sum()), m.sum(), "all ages")
        add(g, "population_25_64", float(w[u].sum()), u.sum(), "adults 25-64")
        add(g, "median_age", wmedian(age[m].astype(float), w[m]), m.sum(), "all ages")
        add(g, "ba_plus_share", share(schl >= 21, w, u), u.sum(), "adults 25-64")
        add(g, "graduate_degree_share", share(schl >= 22, w, u), u.sum(), "adults 25-64")
        add(g, "doctorate_share", share(schl == 24, w, u), u.sum(), "adults 25-64")
        add(g, "hs_or_less_share", share(schl <= 17, w, u), u.sum(), "adults 25-64")

        emp = u & employed
        add(g, "employment_rate_25_64", share(employed, w, u), u.sum(), "adults 25-64")
        add(g, "computer_math_occ_share_of_employed", share(cmm, w, emp), emp.sum(), "employed 25-64")
        add(g, "physician_surgeon_share_of_employed", share(phys, w, emp), emp.sum(), "employed 25-64")
        # Occupation concentration: top 10 detailed OCCP codes.
        sub = pd.DataFrame({"occ": occp[emp], "w": w[emp]}).dropna().groupby(
            "occ").w.sum().sort_values(ascending=False)
        top10 = sub.head(10)
        add(g, "top10_occupation_share_of_employed", float(top10.sum() / sub.sum()),
            emp.sum(), "employed 25-64")
        for rank, (code, weight) in enumerate(top10.items(), 1):
            rows.append({"group": g, "metric": f"top_occupation_{rank:02d}",
                         "value": float(weight / sub.sum()), "n_unweighted": int(emp.sum()),
                         "universe": f"{int(code)} {occ_lab.get(int(code), '?')}"})

        selfemp = np.isin(cow, [6, 7])
        add(g, "self_employed_share_of_employed", share(selfemp, w, emp), emp.sum(), "employed 25-64")
        add(g, "self_employed_incorporated_share", share(cow == 7, w, emp), emp.sum(), "employed 25-64")
        se = emp & selfemp
        add(g, "accommodation_7211_share_of_self_employed", share(indp == 8660, w, se),
            se.sum(), "self-employed 25-64")
        add(g, "accommodation_7211_share_of_employed", share(selfemp & (indp == 8660), w, emp),
            emp.sum(), "employed 25-64")
        sub_i = pd.DataFrame({"ind": indp[se], "w": w[se]}).dropna().groupby(
            "ind").w.sum().sort_values(ascending=False)
        for rank, (code, weight) in enumerate(sub_i.head(5).items(), 1):
            rows.append({"group": g, "metric": f"top_selfemployed_industry_{rank:02d}",
                         "value": float(weight / sub_i.sum()), "n_unweighted": int(se.sum()),
                         "universe": f"{int(code)} {ind_lab.get(int(code), '?')}"})

        # The group's share of a national occupation/industry, not the occupation's share of the
        # group: this is the direction the "Patel motel" and "Indian doctors" claims are made in.
        nat_emp = adults & employed
        for label, sel in (("all_employed", nat_emp),
                           ("self_employed_traveler_accommodation",
                            nat_emp & selfemp & (indp == 8660)),
                           ("physicians_surgeons", nat_emp & phys),
                           ("computer_math_occupations", nat_emp & cmm),
                           ("all_self_employed", nat_emp & selfemp)):
            den = w[sel].sum()
            add(g, f"group_share_of_{label}", float(w[sel & m].sum() / den) if den else float("nan"),
                int((sel & m).sum()), "national denominator, 25-64")

        # English and naturalisation (foreign-born universes only where meaningful).
        fb = m & (nativity == 2) & (age >= 5)
        if fb.sum():
            add(g, "english_very_well_or_only_share", share((eng == 1) | ~np.isfinite(eng), w, fb),
                fb.sum(), "foreign-born 5+")
            add(g, "english_not_well_or_not_at_all_share", share(np.isin(eng, [3, 4]), w, fb),
                fb.sum(), "foreign-born 5+")
        fb_all = m & (nativity == 2)
        if fb_all.sum():
            add(g, "naturalised_share", share(cit == 4, w, fb_all), fb_all.sum(), "foreign-born")
            years = YEAR - yoep
            for lo, hi, lab in [(0, 4, "0_4"), (5, 9, "5_9"), (10, 14, "10_14"),
                                (15, 19, "15_19"), (20, 200, "20_plus")]:
                sel = fb_all & (years >= lo) & (years <= hi)
                if sel.sum():
                    add(g, f"naturalised_share_years_in_us_{lab}", share(cit == 4, w, sel),
                        sel.sum(), "foreign-born in that entry window")
            add(g, "median_years_in_us", wmedian((YEAR - yoep)[fb_all].astype(float), w[fb_all]),
                fb_all.sum(), "foreign-born")

        # Geographic concentration: top 10 PUMAs.
        geo = pd.DataFrame({"g": d.ST.to_numpy()[m] * 100000 + d.PUMA.to_numpy()[m], "w": w[m]})
        agg = geo.groupby("g").w.sum().sort_values(ascending=False)
        add(g, "top10_puma_share", float(agg.head(10).sum() / agg.sum()), m.sum(), "all ages")
        add(g, "top50_puma_share", float(agg.head(50).sum() / agg.sum()), m.sum(), "all ages")
        st = pd.DataFrame({"s": d.ST.to_numpy()[m], "w": w[m]}).groupby("s").w.sum().sort_values(
            ascending=False)
        add(g, "top5_state_share", float(st.head(5).sum() / st.sum()), m.sum(), "all ages")

    print("[4/5] household income and endogamy", flush=True)
    # Householder (RELSHIPP == 20) carries the household's group for household-level items.
    href = d.RELSHIPP.to_numpy() == 20
    if h is not None:
        hh = h.set_index("SERIALNO")
        ref = d.loc[href, ["SERIALNO"]].copy()
        ref["idx"] = np.flatnonzero(href)
        joined = ref.join(hh, on="SERIALNO", how="left")
        keep = joined.TYPEHUGQ.eq(1).to_numpy() & np.isfinite(joined.HINCP.to_numpy())
        hinc = joined.HINCP.to_numpy(dtype=float) * (joined.ADJINC.to_numpy(dtype=float) / 1e6)
        hwgt = joined.WGTP.to_numpy(dtype=float)
        hidx = joined.idx.to_numpy()
        for g in order:
            sel = keep & groups[g][hidx]
            add(g, "median_household_income_householder_group", wmedian(hinc[sel], hwgt[sel]),
                sel.sum(), "households, householder's group, WGTP")
            add(g, "mean_household_size", float((joined.NP.to_numpy(dtype=float)[sel]
                                                 * hwgt[sel]).sum() / hwgt[sel].sum()),
                sel.sum(), "households, householder's group, WGTP")
    else:
        print("  household file missing — household income SKIPPED", flush=True)

    # Endogamy: spouse pairs are (reference person, RELSHIPP in {21, 23}) in the same SERIALNO.
    spouse_flag = np.isin(d.RELSHIPP.to_numpy(), [21, 23])
    pair_src = d.loc[href | spouse_flag, ["SERIALNO", "POBP", "NATIVITY", "ANC1P", "ANC2P",
                                          "RELSHIPP", "AGEP", "PWGTP"]].copy()
    refs = pair_src[pair_src.RELSHIPP == 20].set_index("SERIALNO")
    sps = pair_src[pair_src.RELSHIPP.isin([21, 23])].set_index("SERIALNO")
    pairs = refs.join(sps, how="inner", lsuffix="_a", rsuffix="_b")
    print(f"  married couple records: {len(pairs):,}", flush=True)
    pa, pb = pairs.POBP_a.to_numpy(), pairs.POBP_b.to_numpy()
    na, nb = pairs.NATIVITY_a.to_numpy(), pairs.NATIVITY_b.to_numpy()
    aa = (pairs.ANC1P_a.to_numpy() == ANC_ASIAN_INDIAN) | (pairs.ANC2P_a.to_numpy() == ANC_ASIAN_INDIAN)
    ab = (pairs.ANC1P_b.to_numpy() == ANC_ASIAN_INDIAN) | (pairs.ANC2P_b.to_numpy() == ANC_ASIAN_INDIAN)
    pw = pairs.PWGTP_a.to_numpy(dtype=float)

    def endogamy(label, own_a, own_b, same_a, same_b):
        """Share of married persons of the group whose spouse is also of the group."""
        num = (own_a & same_b).astype(float) + (own_b & same_a).astype(float)
        den = own_a.astype(float) + own_b.astype(float)
        value = float((num * pw).sum() / (den * pw).sum()) if (den * pw).sum() > 0 else float("nan")
        add(label[0], label[1], value, int(den.sum()), "married spouse-present couples")

    endogamy(("india_born", "spouse_india_born_share"), pa == INDIA, pb == INDIA,
             pa == INDIA, pb == INDIA)
    endogamy(("india_born", "spouse_india_born_or_indian_ancestry_share"),
             pa == INDIA, pb == INDIA, (pa == INDIA) | aa, (pb == INDIA) | ab)
    endogamy(("china_born", "spouse_china_born_share"), pa == CHINA, pb == CHINA,
             pa == CHINA, pb == CHINA)
    endogamy(("mexico_born", "spouse_mexico_born_share"), pa == MEXICO, pb == MEXICO,
             pa == MEXICO, pb == MEXICO)
    endogamy(("us_born_asian_indian_anc", "spouse_indian_origin_share"),
             (na == 1) & aa, (nb == 1) & ab, (pa == INDIA) | aa, (pb == INDIA) | ab)

    frame = pd.DataFrame(rows).sort_values(["group", "metric"], kind="stable")
    out_csv = args.out / f"acs_profile_{args.tag}.csv"
    frame.to_csv(out_csv, index=False, float_format="%.6f")
    print(f"[5/5] wrote {out_csv.name} ({len(frame):,} rows)", flush=True)

    lines = render(frame, order, args)
    (args.out / f"acs_profile_{args.tag}_result.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


def render(frame, order, args) -> list[str]:
    L = [f"ACS {args.year} 1-year PUMS profile — person file {args.person_zip.name}, "
         f"household file {args.household_zip.name}",
         "Point estimates on PWGTP (households: WGTP). No replicate standard errors; see docstring.",
         ""]
    def get(g, m, field="value"):
        q = frame.query("group == @g and metric == @m")
        return float(q[field].iloc[0]) if len(q) == 1 else float("nan")

    headline = [
        ("Population, all ages (millions)", "population_all_ages", 1e-6, ",.2f"),
        ("Population 25-64 (millions)", "population_25_64", 1e-6, ",.2f"),
        ("Median age", "median_age", 1, ",.0f"),
        ("BA or higher, 25-64", "ba_plus_share", 100, ",.1f"),
        ("Graduate degree, 25-64", "graduate_degree_share", 100, ",.1f"),
        ("Doctorate, 25-64", "doctorate_share", 100, ",.1f"),
        ("High school or less, 25-64", "hs_or_less_share", 100, ",.1f"),
        ("Employed, 25-64", "employment_rate_25_64", 100, ",.1f"),
        ("Median household income (householder)", "median_household_income_householder_group", 1, ",.0f"),
        ("Mean household size", "mean_household_size", 1, ",.2f"),
        ("Computer/math occupations, employed", "computer_math_occ_share_of_employed", 100, ",.1f"),
        ("Physicians/surgeons, employed", "physician_surgeon_share_of_employed", 100, ",.2f"),
        ("Top-10 occupation concentration", "top10_occupation_share_of_employed", 100, ",.1f"),
        ("Self-employed, employed", "self_employed_share_of_employed", 100, ",.1f"),
        ("  of which incorporated", "self_employed_incorporated_share", 100, ",.1f"),
        ("Traveler accommodation (7211), self-employed", "accommodation_7211_share_of_self_employed", 100, ",.2f"),
        ("Naturalised (foreign-born)", "naturalised_share", 100, ",.1f"),
        ("  entered 0-4 years ago", "naturalised_share_years_in_us_0_4", 100, ",.1f"),
        ("  entered 5-9 years ago", "naturalised_share_years_in_us_5_9", 100, ",.1f"),
        ("  entered 10-14 years ago", "naturalised_share_years_in_us_10_14", 100, ",.1f"),
        ("  entered 15-19 years ago", "naturalised_share_years_in_us_15_19", 100, ",.1f"),
        ("  entered 20+ years ago", "naturalised_share_years_in_us_20_plus", 100, ",.1f"),
        ("Median years in the US", "median_years_in_us", 1, ",.0f"),
        ("English very well / only English", "english_very_well_or_only_share", 100, ",.1f"),
        ("English not well / not at all", "english_not_well_or_not_at_all_share", 100, ",.1f"),
        ("Top-10 PUMA concentration", "top10_puma_share", 100, ",.1f"),
        ("Top-50 PUMA concentration", "top50_puma_share", 100, ",.1f"),
        ("Top-5 state concentration", "top5_state_share", 100, ",.1f"),
        ("Group's share of all US employed 25-64", "group_share_of_all_employed", 100, ",.2f"),
        ("  of all self-employed", "group_share_of_all_self_employed", 100, ",.2f"),
        ("  of self-employed in traveler accommodation",
         "group_share_of_self_employed_traveler_accommodation", 100, ",.2f"),
        ("  of physicians and surgeons", "group_share_of_physicians_surgeons", 100, ",.2f"),
        ("  of computer/math occupations", "group_share_of_computer_math_occupations", 100, ",.2f"),
    ]
    L.append(f"{'metric':46s}" + "".join(f"{g[:17]:>19s}" for g in order))
    L.append(f"{'unweighted n, adults 25-64':46s}" + "".join(
        f"{get(g, 'population_25_64', 'n_unweighted'):>19,.0f}" for g in order))
    for label, metric, scale, fmt in headline:
        cells = ""
        for g in order:
            v = get(g, metric) * scale
            cells += (f"{v:>19{fmt}}" if np.isfinite(v) else "—".rjust(19))
        L.append(f"{label:46s}{cells}")

    L.append("")
    L.append("== spousal endogamy, married spouse-present couples ==")
    for g, m in [("india_born", "spouse_india_born_share"),
                 ("india_born", "spouse_india_born_or_indian_ancestry_share"),
                 ("china_born", "spouse_china_born_share"),
                 ("mexico_born", "spouse_mexico_born_share"),
                 ("us_born_asian_indian_anc", "spouse_indian_origin_share")]:
        L.append(f"  {g:28s} {m:48s} {get(g, m) * 100:6.1f}%  (n={get(g, m, 'n_unweighted'):,.0f})")

    L.append("")
    L.append("== top occupations of the employed 25-64, by group ==")
    for g in order:
        L.append(f"-- {g} --")
        for rank in range(1, 11):
            name = f"top_occupation_{rank:02d}"
            q = frame.query("group == @g and metric == @name")
            if len(q) == 1:
                L.append(f"   {rank:2d}. {q.universe.iloc[0][:70]:70s} {q.value.iloc[0] * 100:5.1f}%")
    L.append("")
    L.append("== top industries of the self-employed 25-64, by group ==")
    for g in order:
        L.append(f"-- {g} --")
        for rank in range(1, 6):
            name = f"top_selfemployed_industry_{rank:02d}"
            q = frame.query("group == @g and metric == @name")
            if len(q) == 1:
                L.append(f"   {rank:2d}. {q.universe.iloc[0][:70]:70s} {q.value.iloc[0] * 100:5.1f}%")
    return L


if __name__ == "__main__":
    main()
