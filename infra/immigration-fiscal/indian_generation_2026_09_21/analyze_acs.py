#!/usr/bin/env python3
"""ACS 2023 1-year: US-born Asian Indian ancestry vs US-born NH whites by age.

ACS has no parental birthplace, so this is a G2+G3 mix. Adult US-born Asian Indians
are mostly G2 (post-1965 immigration); the CPS G3+ race cell is the generation split.

Run: uv run --no-project --with pandas --with numpy python3 analyze_acs.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "build"))
import paths as _data_paths  # noqa: E402

import zipfile

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
OUT.mkdir(exist_ok=True)
PERSON_ZIP = _data_paths.data_root(require_exists=False) / "census/acs_pums_2023_person.zip"
ANC_ASIAN_INDIAN = 615
BANDS = [(18, 24), (25, 34), (35, 44), (45, 54), (55, 64), (65, 80)]
COLS = ["PWGTP", "AGEP", "SEX", "RAC1P", "HISP", "NATIVITY", "POBP",
        "ANC1P", "ANC2P", "SCHL", "PINCP", "ADJINC", "ESR"]


def load_person(path: Path) -> pd.DataFrame:
    frames = []
    with zipfile.ZipFile(path) as z:
        members = sorted(n for n in z.namelist() if n.lower().endswith(".csv"))
        header = z.open(members[0]).readline().decode().strip().split(",")
        want = [c for c in COLS if c in header]
        if "HISP" not in header and "HISP" in COLS:
            # 2023 uses HISP
            pass
        for i, name in enumerate(members, 1):
            print(f"  [{i}/{len(members)}] {name}", flush=True)
            part = pd.read_csv(z.open(name), usecols=want, low_memory=False)
            frames.append(part)
    d = pd.concat(frames, ignore_index=True)
    print(f"  person rows {len(d):,}", flush=True)
    return d


def wmean(x, w):
    s = w.sum()
    return float("nan") if s <= 0 else float(np.dot(x, w) / s)


def wmedian(x, w):
    order = np.argsort(x, kind="stable")
    x, w = x[order], w[order]
    cdf = np.cumsum(w) / w.sum()
    return float(x[np.searchsorted(cdf, 0.5)])


def main():
    print(f"[1] {PERSON_ZIP}", flush=True)
    if not PERSON_ZIP.exists():
        raise SystemExit(f"missing {PERSON_ZIP}")
    d = load_person(PERSON_ZIP)
    w = d.PWGTP.to_numpy(float)
    age = d.AGEP.to_numpy()
    nativity = d.NATIVITY.to_numpy()
    anc = (d.ANC1P.eq(ANC_ASIAN_INDIAN) | d.ANC2P.eq(ANC_ASIAN_INDIAN)).to_numpy()
    schl = d.SCHL.to_numpy()
    adj = d.ADJINC.to_numpy(float) / 1_000_000.0
    pinc = np.where(d.PINCP.to_numpy(float) == -19999, np.nan, d.PINCP.to_numpy(float) * adj)
    ba = (schl >= 21).astype(float)
    grad = (schl >= 22).astype(float)
    groups = {
        # ACS HISP=1 is not Hispanic (CPS PEHSPNON=2 is the opposite convention).
        "us_born_nh_white": (nativity == 1) & d.RAC1P.eq(1).to_numpy() & d.HISP.eq(1).to_numpy(),
        "india_born": d.POBP.eq(210).to_numpy(),
        "us_born_asian_indian_anc": (nativity == 1) & anc,
    }
    rows = []
    print("[2] age bands", flush=True)
    for gname, mask in groups.items():
        for lo, hi in BANDS + [(25, 64)]:
            use = mask & (age >= lo) & (age <= hi) & np.isfinite(pinc)
            if use.sum() == 0:
                continue
            rec = {
                "group": gname, "age_lo": lo, "age_hi": hi,
                "n": int(use.sum()), "weighted": float(w[use].sum()),
                "ba_share": wmean(ba[use], w[use]),
                "grad_share": wmean(grad[use], w[use]),
                "mean_pinc": wmean(pinc[use], w[use]),
                "median_pinc": wmedian(pinc[use], w[use]),
            }
            rows.append(rec)
            print(f"  {gname:28} {lo:3d}-{hi:<3d} n={rec['n']:7,d}  "
                  f"BA={rec['ba_share']:5.1%}  mean={rec['mean_pinc']:9,.0f}  "
                  f"med={rec['median_pinc']:9,.0f}", flush=True)
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "acs_age_bands.csv", index=False, float_format="%.6f")
    white = out[out.group == "us_born_nh_white"].set_index(["age_lo", "age_hi"])
    print("\n== gap vs US-born NH white ==", flush=True)
    for gname in ["india_born", "us_born_asian_indian_anc"]:
        for _, r in out[out.group == gname].iterrows():
            key = (r.age_lo, r.age_hi)
            if key not in white.index:
                continue
            wr = white.loc[key]
            print(f"  {gname:28} {int(r.age_lo):3d}-{int(r.age_hi):<3d}  "
                  f"BA gap {r.ba_share-wr.ba_share:+.1%}  "
                  f"mean PINCP gap {r.mean_pinc-wr.mean_pinc:+,.0f}  "
                  f"median gap {r.median_pinc-wr.median_pinc:+,.0f}", flush=True)


if __name__ == "__main__":
    main()
