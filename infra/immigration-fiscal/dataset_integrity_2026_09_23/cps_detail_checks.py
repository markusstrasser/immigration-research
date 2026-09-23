"""Follow-up checks on CPS ASEC 2025: (1) parent-birthplace donor rule for Mexican self-ID natives,
(2) union members who are in the union only through an allocated value, (3) nativity flag codes for
the Mexico-born, (4) born-abroad-of-US-parent records, (5) Mexico-born sample size, mean weight and
replicate SE by region, 2025 vs 2026. Writes derived/cps_detail_checks.json.
"""
from __future__ import annotations

import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
FISCAL = ROOT / "infra/immigration-fiscal"
CPS25 = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
CPS26 = FISCAL / "ledger_asec2026_2026_09_16/_cache/asecpub26csv.zip"
US = [57, 60, 66, 69, 73, 78]
REPS = [f"pwwgt{i}" for i in range(161)]


def load(path: Path, year: str) -> pd.DataFrame:
    cols = ["PH_SEQ", "PPPOS", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PXNATVTY", "PEFNTVTY",
            "PXFNTVTY", "PEMNTVTY", "PXMNTVTY", "PEHSPNON", "PXHSPNON", "PRDTHSP", "MARSUPWT"]
    with zipfile.ZipFile(path) as z:
        p = pd.read_csv(z.open(f"pppub{year}.csv"), usecols=cols)
        h = pd.read_csv(z.open(f"hhpub{year}.csv"), usecols=["H_SEQ", "GESTFIPS"])
        r = pd.read_csv(z.open(f"asec_csv_repwgt_20{year}.csv"))
    p = p.merge(h.rename(columns={"H_SEQ": "PH_SEQ"}), on="PH_SEQ", how="left", validate="many_to_one")
    r = r.rename(columns={"h_seq": "PH_SEQ"})
    p = p.merge(r, on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one")
    return p


def se(v: np.ndarray) -> float:
    return float(np.sqrt(4 / 160 * np.square(v[1:] - v[0]).sum()))


def main() -> None:
    d = load(CPS25, "25")
    w = d.MARSUPWT / 100
    civ = d.PRPERTYP.eq(2) | d.A_AGE.lt(15)
    nat = d.PRCITSHP.isin([1, 2, 3]) & civ
    alloc_f = d.PXFNTVTY.between(10, 43)
    alloc_m = d.PXMNTVTY.between(10, 43)
    out: dict = {}

    # (1) Donor rule: for Mexican self-ID natives, allocated vs reported parent birthplace.
    mid = nat & d.PRDTHSP.eq(1)
    def dist(mask, col):
        cls = pd.Series(np.select([d[col].eq(303), d[col].isin(US)], ["Mexico", "US area"], "other"), index=d.index)
        s = w[mask].groupby(cls[mask]).sum()
        return (100 * s / s.sum()).round(2).to_dict()
    out["mexican_selfid_native_father_birthplace"] = {
        "reported": dist(mid & ~alloc_f, "PEFNTVTY"), "allocated": dist(mid & alloc_f, "PEFNTVTY"),
        "allocated_weighted_m": float(w[mid & alloc_f].sum() / 1e6)}
    out["mexican_selfid_native_mother_birthplace"] = {
        "reported": dist(mid & ~alloc_m, "PEMNTVTY"), "allocated": dist(mid & alloc_m, "PEMNTVTY"),
        "allocated_weighted_m": float(w[mid & alloc_m].sum() / 1e6)}
    # Same for non-Hispanic natives: does allocation ever assign Mexico?
    nh = nat & d.PEHSPNON.eq(2)
    out["nonhispanic_native_father_allocated_to_mexico_m"] = float(w[nh & alloc_f & d.PEFNTVTY.eq(303)].sum() / 1e6)
    out["nonhispanic_native_mother_allocated_to_mexico_m"] = float(w[nh & alloc_m & d.PEMNTVTY.eq(303)].sum() / 1e6)

    # (2) In the union only via an allocated value.
    g2 = nat & (d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303))
    mex_par_alloc_only = g2 & ~((d.PEFNTVTY.eq(303) & ~alloc_f) | (d.PEMNTVTY.eq(303) & ~alloc_m))
    g1 = d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303) & civ
    out["g2_only_by_allocated_mexico_parent_m"] = float(w[mex_par_alloc_only].sum() / 1e6)
    out["g2_only_by_allocated_mexico_parent_not_mexican_id_m"] = float(w[mex_par_alloc_only & d.PRDTHSP.ne(1)].sum() / 1e6)
    out["g1_birthplace_hotdeck_m"] = float(w[g1 & d.PXNATVTY.between(30, 43)].sum() / 1e6)
    out["g1_nativity_flag_codes_weighted_m"] = {int(k): round(float(v) / 1e6, 4) for k, v in w[g1].groupby(d.PXNATVTY[g1]).sum().items()}
    g3 = nat & d.PEFNTVTY.isin(US) & d.PEMNTVTY.isin(US) & d.PRDTHSP.eq(1)
    out["g3_hispanic_origin_allocated_m"] = float(w[g3 & d.PXHSPNON.between(10, 43)].sum() / 1e6)
    out["g3_with_any_parent_allocated_to_us_m"] = float(w[g3 & (alloc_f | alloc_m)].sum() / 1e6)

    # (4) Born abroad of a US parent, born in Mexico.
    b3 = d.PRCITSHP.eq(3) & d.PENATVTY.eq(303) & civ
    out["born_mexico_of_us_parent"] = {
        "total_m": float(w[b3].sum() / 1e6), "in_g2_m": float(w[b3 & g2].sum() / 1e6),
        "in_g3_m": float(w[b3 & g3 & ~g2].sum() / 1e6),
        "outside_union_m": float(w[b3 & ~g2 & ~g3].sum() / 1e6),
        "outside_union_mexican_id_m": float(w[b3 & ~g2 & ~g3 & d.PRDTHSP.eq(1)].sum() / 1e6)}

    # (5) Mexico-born by region, both years: n, mean weight, estimate, replicate SE.
    reg = {}
    for year, path in [("2025", CPS25), ("2026", CPS26)]:
        x = d if year == "2025" else load(path, "26")
        m = x.PRCITSHP.isin([4, 5]) & x.PENATVTY.eq(303)
        rows = {}
        for lab, sm in [("CA+TX", x.GESTFIPS.isin([6, 48])), ("other", ~x.GESTFIPS.isin([6, 48])),
                        ("all", pd.Series(True, index=x.index))]:
            mm = (m & sm).to_numpy()
            est = x.loc[mm, REPS].sum().to_numpy()
            rows[lab] = dict(n=int(mm.sum()), mean_weight=float(x.MARSUPWT[mm].mean() / 100),
                             est_m=float(est[0] / 1e6), se_m=se(est) / 1e6)
        allw = x.MARSUPWT.mean() / 100
        rows["mean_weight_all_records"] = float(allw)
        reg[year] = rows
    out["mexico_born_by_region"] = reg
    (HERE / "derived/cps_detail_checks.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
