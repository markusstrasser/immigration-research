"""Shift-share instrument for enrollment: fall-2000 Hispanic and other pupils grown at national rates.

Predicted pupils in fall t-1 (F-33 fiscal year t) for district d:
    Nhat = H_d,2000 * H_t-1 / H_2000 + O_d,2000 * O_t-1 / O_2000
with H, O the district's CCD fall-2000 Hispanic and other members (Urban Institute redistribution of
NCES CCD) and the national totals from NCES Digest table 203.50 (fall 2000-2022, thousands). Within a
district, log Nhat moves only through the district's fall-2000 Hispanic share, so the instrument asks
whether districts that were more Hispanic in 2000 than their state peers gained pupils faster, and
how their spending followed. State-year fixed effects absorb every state-level policy and price.

It isolates enrollment growth that tracks the group's own growth, which is the variation the account
cares about. It is not clean: districts that were Hispanic in 2000 differ in other ways (urban, poorer,
exposed to compensatory formulas), so the exclusion restriction is an assumption [INFERENCE].

Sample: estimate_functions.load(2019) spells that contain FY2001, FY2001-FY2019. Standard errors are
clustered by state; the first-stage F is the squared cluster-robust t of the single instrument.
Writes derived/iv_first_stage.csv and derived/iv_elasticities.csv.

    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with pyarrow --with pyfixest \
      python3 infra/immigration-fiscal/school_dilution_2026_09_24/estimate_iv.py
"""
import html
import re
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import pyfixest as pf

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from estimate_functions import FUNCS, load  # noqa: E402

OUT = HERE / "derived"
CCD = HERE / "_cache" / "ccd"
# Same Urban endpoints, pulled 2026-09-18 by that lane (school_flight_2026_09_18/pull_districts.py);
# its API throughput was the bottleneck this time as well, so the complete state-year files are reused.
FLIGHT = HERE.parent / "school_flight_2026_09_18" / "_cache" / "dist"
BASE_FALL = 2000


def national_by_race():
    """Digest 203.50 rows: fall year -> (total, Hispanic) public enrollment, thousands. Actual years only."""
    t = (HERE / "_cache" / "dt23_203.50.html").read_text(encoding="utf-8", errors="replace")
    out = {}
    for r in re.findall(r"<tr[^>]*>(.*?)</tr>", t, flags=re.S):
        cells = [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", c))).strip()
                 for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, flags=re.S)]
        if not cells or not re.match(r"^(19|20)\d\d", cells[0]):
            continue
        year = int(cells[0][:4])
        if year in out or year > 2022:          # first block is the US; later blocks are regions; 2023+ projected
            continue
        # Cells in the US block: year, Total, American Indian/Alaska Native, Asian, a footnote-marker cell,
        # Black, Hispanic, Pacific Islander, White, Two or more races.
        out[year] = (float(cells[1].replace(",", "")), float(cells[6].replace(",", "")))
    d = pd.DataFrame(out, index=["total", "hispanic"]).T
    d["other"] = d.total - d.hispanic
    if abs(d.loc[2000, "hispanic"] - 7726) > 0.5 or abs(d.loc[2019, "hispanic"] - 14055) > 0.5:
        raise SystemExit("[BLOCKED] Digest 203.50 parse: Hispanic fall 2000/2019 not 7,726/14,055 thousand")
    return d


def ccd_files(kind, fall):
    """This lane's pull if complete, else the school-flight lane's pull of the same Urban endpoint."""
    for folder in (CCD, FLIGHT):
        files = sorted(folder.glob(f"{kind}_{fall}_*.csv"))
        if len(files) == 51:
            return files
    raise SystemExit(f"[BLOCKED] no complete set of 51 CCD {kind} files for fall {fall}; run pull_ccd.py "
                     f"with KINDS={kind} YEARS={fall}")


def base_shares():
    frames = [pd.read_csv(p, dtype={"leaid": str}) for p in ccd_files("enr", BASE_FALL)]
    b = pd.concat(frames, ignore_index=True)
    b["leaid"] = b.leaid.str.zfill(7)
    b = b[b.enr_total.gt(0) & b.enr_hisp.notna()]
    b["h0"] = (b.enr_hisp / b.enr_total).clip(0, 1)
    return b.set_index("leaid")[["h0", "enr_total", "enr_hisp"]]


def main():
    nat = national_by_race()
    base = base_shares()
    d, _ = load(2019)
    d = d[d.year.ge(BASE_FALL + 1)].copy()
    in_base = d[d.year.eq(BASE_FALL + 1)][["spell"]].drop_duplicates()
    d = d[d.spell.isin(in_base.spell)].join(base, on="leaid", how="inner")
    fall = d.year - 1
    gh = fall.map(nat.hispanic) / nat.loc[BASE_FALL, "hispanic"]
    go = fall.map(nat.other) / nat.loc[BASE_FALL, "other"]
    d["z"] = np.log(d.h0 * gh + (1 - d.h0) * go)
    d["w_pupil"] = d.groupby("spell").V33.transform("mean")
    fs_rows, iv_rows = [], []
    for wname, w in [("unweighted", None), ("pupils", "w_pupil")]:
        m = pf.feols("lnN ~ z | spell + stateyear", data=d, vcov={"CRV1": "fips"}, weights=w)
        b, se = float(m.coef()["z"]), float(m.se()["z"])
        fs_rows.append({"weight": wname, "first_stage_coef": b, "se": se, "F_cluster": (b / se) ** 2,
                        "n_obs": int(m._N), "districts": int(d.leaid.nunique()),
                        "mean_h0_pupil_weighted": float((d.h0 * d.V33).sum() / d.V33.sum())})
        for f in FUNCS:
            pos = d[d[f] > 0].assign(ly=lambda x: np.log(x[f]))
            iv = pf.feols("ly ~ 1 | spell + stateyear | lnN ~ z", data=pos, vcov={"CRV1": "fips"}, weights=w)
            rf = pf.feols("ly ~ z | spell + stateyear", data=pos, vcov={"CRV1": "fips"}, weights=w)
            b_iv, se_iv = float(iv.coef()["lnN"]), float(iv.se()["lnN"])
            ols = pf.feols("ly ~ lnN | spell + stateyear", data=pos, vcov={"CRV1": "fips"}, weights=w)
            iv_rows.append({"spec": "iv_shiftshare_fe_fy2001_2019", "function": f, "weight": wname,
                            "beta_iv": b_iv, "se_iv": se_iv, "ci_low": b_iv - 1.96 * se_iv,
                            "ci_high": b_iv + 1.96 * se_iv, "reduced_form": float(rf.coef()["z"]),
                            "reduced_form_se": float(rf.se()["z"]), "beta_ols_same_sample": float(ols.coef()["lnN"]),
                            "n_obs": int(iv._N)})
    # Long difference FY2001 -> FY2019 within one spell, state fixed effects: the same instrument's
    # cross-district content without the yearly noise.
    a = d[d.year.eq(BASE_FALL + 1)].set_index("spell")
    b_ = d[d.year.eq(2019)].set_index("spell")
    both = a.index.intersection(b_.index)
    ld = pd.DataFrame({"fips": a.loc[both, "fips"], "dlnN": b_.loc[both, "lnN"] - a.loc[both, "lnN"],
                       "dz": b_.loc[both, "z"] - a.loc[both, "z"], "w": a.loc[both, "V33"]})
    for wname, w in [("unweighted", None), ("pupils", "w")]:
        m = pf.feols("dlnN ~ dz | fips", data=ld, vcov={"CRV1": "fips"}, weights=w)
        b, se = float(m.coef()["dz"]), float(m.se()["dz"])
        fs_rows.append({"weight": wname, "spec": "long_difference_fy2001_2019", "first_stage_coef": b, "se": se,
                        "F_cluster": (b / se) ** 2, "n_obs": int(m._N), "districts": len(ld)})
        for f in FUNCS:
            ok = (a.loc[both, f] > 0) & (b_.loc[both, f] > 0)
            s = ld[ok].assign(dly=np.log(b_.loc[both, f][ok] / a.loc[both, f][ok]))
            iv = pf.feols("dly ~ 1 | fips | dlnN ~ dz", data=s, vcov={"CRV1": "fips"}, weights=w)
            b_iv, se_iv = float(iv.coef()["dlnN"]), float(iv.se()["dlnN"])
            iv_rows.append({"spec": "iv_shiftshare_ld_fy2001_2019", "function": f, "weight": wname,
                            "beta_iv": b_iv, "se_iv": se_iv, "ci_low": b_iv - 1.96 * se_iv,
                            "ci_high": b_iv + 1.96 * se_iv, "n_obs": int(iv._N)})
    fs, ivr = pd.DataFrame(fs_rows), pd.DataFrame(iv_rows)
    fs["spec"] = fs["spec"].fillna("fe_fy2001_2019") if "spec" in fs else "fe_fy2001_2019"
    fs["strong_F_ge_10"] = fs.F_cluster.ge(10)
    OUT.mkdir(exist_ok=True)
    fs.to_csv(OUT / "iv_first_stage.csv", index=False, lineterminator="\n", float_format="%.6f")
    ivr.to_csv(OUT / "iv_elasticities.csv", index=False, lineterminator="\n", float_format="%.6f")
    print(fs.to_string(index=False))
    print(ivr[ivr.function.isin(["current", "instruction", "instr_support", "administration", "om",
                                 "capital_outlay", "interest"])].to_string(index=False))


if __name__ == "__main__":
    sys.exit(main())
