"""ACS PUMS allocation audit by group x residence type (household / institutional / other GQ).

Reads _cache/acs_person_<YEAR>.parquet (acs_extract.py). Weighted by PWGTP. Writes
derived/acs_alloc_rates_<YEAR>.csv, acs_alloc_nativity_inst_<YEAR>.csv,
acs_custody_sensitivity_<YEAR>.csv. A flag value of 1 means "allocated" (PUMS F*P convention).
Usage: acs_alloc.py YEAR [YEAR ...]
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
FLAGS = ["FHISP", "FPOBP", "FCITP", "FYOEP", "FRACP", "FAGEP", "FSEXP", "FSCHLP", "FSCHP",
         "FSCHGP", "FPERNP", "FWAGP", "FPINCP", "FSSIP", "FPAP", "FHICOVP", "FANCP", "FLANXP",
         "FESRP", "FENGP"]


def load(year):
    d = pd.read_parquet(HERE / "_cache" / f"acs_person_{year}.parquet")
    rel = d["RELSHIPP"] if "RELSHIPP" in d and d["RELSHIPP"].notna().any() else None
    if rel is not None:
        d["res"] = np.select([rel.eq(37), rel.eq(38)], ["inst", "noninst_gq"], "household")
    else:  # pre-2019 RELP: 16 institutional GQ, 17 noninstitutional GQ
        d["res"] = np.select([d.RELP.eq(16), d.RELP.eq(17)], ["inst", "noninst_gq"], "household")
    d["fb"] = d.NATIVITY.eq(2)
    groups = {
        "mexican_origin_hisp02": d.HISP.eq(2),
        "mexico_born_pobp303": d.POBP.eq(303),
        "usborn_mexican": d.NATIVITY.eq(1) & d.HISP.eq(2),
        "native_nh_white": d.NATIVITY.eq(1) & d.HISP.eq(1) & d.RAC1P.eq(1),
        "native_all": d.NATIVITY.eq(1),
        "foreign_born_all": d.fb,
        "hisp24_other_hispanic": d.HISP.eq(24),
        "all": pd.Series(True, index=d.index),
    }
    return d, groups


def rates(d, groups, year):
    rows = []
    adult = d.AGEP.between(18, 64)
    for g, m in groups.items():
        for res in ["household", "inst", "noninst_gq"]:
            s = d[m & adult & d.res.eq(res)]
            if len(s) == 0:
                continue
            row = dict(year=year, group=g, residence=res, ages="18-64", n=len(s),
                       pop=float(s.PWGTP.sum()))
            for f in FLAGS:
                if f in s:
                    v = s[f]
                    ok = v.notna()
                    row[f] = float((s.PWGTP[ok] * v[ok].eq(1)).sum() / s.PWGTP[ok].sum()) if ok.any() else np.nan
            # joint flags: records with 5+ of the core demographic/content items allocated
            core = [f for f in ["FHISP", "FPOBP", "FCITP", "FRACP", "FSCHLP", "FPERNP", "FLANXP",
                                "FHICOVP", "FESRP"] if f in s]
            k = s[core].fillna(0).eq(1).sum(axis=1)
            row["share_5plus_core_allocated"] = float((s.PWGTP * k.ge(5)).sum() / s.PWGTP.sum())
            rows.append(row)
    return pd.DataFrame(rows)


def nativity_by_flag(d, year):
    """Among institutional 18-64: foreign-born share by birthplace reported vs allocated."""
    s = d[d.res.eq("inst") & d.AGEP.between(18, 64)].copy()
    s["hgrp"] = np.select([s.HISP.eq(2), s.HISP.eq(24), s.HISP.gt(1)],
                          ["mexican", "hisp24", "other_named_hispanic"], "non_hispanic")
    s["pobp_alloc"] = s.FPOBP.eq(1)
    out = []
    for (h, a), t in s.groupby(["hgrp", "pobp_alloc"]):
        out.append(dict(year=year, hisp_group=h, pobp_allocated=bool(a), n=len(t),
                        pop=float(t.PWGTP.sum()),
                        fb_share=float((t.PWGTP * t.fb).sum() / t.PWGTP.sum()),
                        mexico_born_share=float((t.PWGTP * t.POBP.eq(303)).sum() / t.PWGTP.sum())))
    return pd.DataFrame(out)


def custody_sensitivity(d, year):
    """Mexican-coded (HISP=2) institutional rate by nativity, 18-64, as recorded and with
    allocated birthplaces spread in the reported nativity mix of the same Hispanic group."""
    a = d[d.AGEP.between(18, 64) & d.HISP.eq(2)]
    hh = a[a.res.ne("inst")]  # non-institutional denominator = household + other GQ
    inst = a[a.res.eq("inst")]
    hh_fb = float(hh.PWGTP[hh.fb].sum()); hh_us = float(hh.PWGTP[~hh.fb].sum())
    rec = inst[inst.FPOBP.ne(1)]; alc = inst[inst.FPOBP.eq(1)]
    fb_rec_share = float(rec.PWGTP[rec.fb].sum() / rec.PWGTP.sum())
    rows = []
    for arm, i_fb, i_us in [
        ("as_recorded", inst.PWGTP[inst.fb].sum(), inst.PWGTP[~inst.fb].sum()),
        ("allocated_spread_in_reported_mix",
         rec.PWGTP[rec.fb].sum() + alc.PWGTP.sum() * fb_rec_share,
         rec.PWGTP[~rec.fb].sum() + alc.PWGTP.sum() * (1 - fb_rec_share)),
        ("allocated_dropped_both_sides", rec.PWGTP[rec.fb].sum(), rec.PWGTP[~rec.fb].sum()),
    ]:
        rows.append(dict(year=year, arm=arm, inst_fb=float(i_fb), inst_us=float(i_us),
                         rate_fb=float(i_fb) / hh_fb, rate_us=float(i_us) / hh_us,
                         fb_share_of_inst=float(i_fb) / float(i_fb + i_us),
                         inst_pobp_allocated_share=float(alc.PWGTP.sum() / inst.PWGTP.sum())))
    return pd.DataFrame(rows)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for y in map(int, sys.argv[1:]):
        d, groups = load(y)
        r = rates(d, groups, y); r.to_csv(OUT / f"acs_alloc_rates_{y}.csv", index=False)
        n = nativity_by_flag(d, y); n.to_csv(OUT / f"acs_alloc_nativity_inst_{y}.csv", index=False)
        c = custody_sensitivity(d, y); c.to_csv(OUT / f"acs_custody_sensitivity_{y}.csv", index=False)
        pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
        print(r[["group", "residence", "n", "FHISP", "FPOBP", "FCITP", "FYOEP", "FRACP", "FSCHLP",
                 "FPERNP", "FSEXP", "FAGEP", "share_5plus_core_allocated"]].round(3).to_string(index=False))
        print(n.round(3).to_string(index=False))
        print(c.round(4).to_string(index=False))
