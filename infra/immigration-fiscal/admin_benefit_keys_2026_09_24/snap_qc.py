"""SNAP Quality Control FY2024 public-use file: Hispanic shares of participants and benefits.

Source: USDA FNS / Mathematica, FY2024 SNAP QC database (qc_pub_fy2024.csv, released 2026-08) and its
technical documentation (FY-2024-Tech-Doc.pdf). Average month of FY2024 (October 2023 to September
2024) with the full-year weight FYWGT. Race/ethnicity is RACETHi per person: 13-22 Hispanic or
Latino, 3-12 not Hispanic, 1-2 not available / not recorded (codebook, Chapter V).

Gates (primary-document anchors):
- weighted individuals (FSUSIZE) and benefits (FSBEN) equal Table II.2's QC weighted totals;
- the weighted share of participants with unreported race/ethnicity is "about 17 percent" and the
  states with at least 10 percent unreported are exactly the 20 listed in Appendix A.

Hispanic share estimands (participants are FSAFILi = 1; benefits are FSBEN):
- participants: persons, by own ethnicity;
- dollars: each unit's benefit split equally over its participants (the account key's analogue);
- head_dollars: each unit's benefit by the ethnicity of its head (RELi = 1);
- listed_dollars: the benefit split over every person listed in the home, participants or not.
Unknown ethnicity is reported three ways: known-only (missing at random), the two bounds (every
unknown non-Hispanic / every unknown Hispanic), and imputed (unknown members take the Hispanic
share of known members of their own unit; wholly unknown units take the share of known units in
the same state x noncitizen-in-home x child-in-unit cell). Linearized SEs treat units as
with-replacement draws within state strata.

Validity diagnostic (derived/admin_snap_qc_validity.csv): by state, the Hispanic share of known
participants who live with an undocumented noncitizen (CTZNi = 8; codebook, printed p. 79) and of
noncitizen participants (CTZNi >= 3), beside all participants. Where most undocumented members'
households are Hispanic, a near-zero share there means the state codes Hispanic participants as
not Hispanic. The codebook itself "recommend[s] against using RACETHi for national tabulations"
(RACETHi entry, printed p. 82).

Writes derived/admin_snap_qc.csv. Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy python3 \
      infra/immigration-fiscal/admin_benefit_keys_2026_09_24/snap_qc.py
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache/snap"
BASE = "https://snapqcdata.net/sites/default/files/2026-08/"
FILES = {"qcfy2024_csv.zip": None, "FY-2024-Tech-Doc.pdf": None}
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
PINS = CACHE / "SOURCE_PINS.json"
TABLE_II2 = {"individuals": 40_168_146, "benefits_thousand": 7_366_534}
APPX_A_20 = {"California", "Colorado", "Connecticut", "Delaware", "Hawaii", "Illinois", "Louisiana",
             "Minnesota", "Mississippi", "New Hampshire", "New Mexico", "Oregon", "Rhode Island",
             "Tennessee", "Texas", "Utah", "Vermont", "Washington", "Wisconsin", "Wyoming"}
P = 18


def sha(path: Path) -> str:
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def fetch():
    CACHE.mkdir(parents=True, exist_ok=True)
    pins = json.loads(PINS.read_text()) if PINS.exists() else {}
    for name in FILES:
        path = CACHE / name
        if not path.exists():
            subprocess.run(["curl", "-sS", "--fail", "-L", "-m", "600", "-A", UA, "-o", str(path), BASE + name],
                           check=True)
        digest = sha(path)
        if name in pins and pins[name]["sha256"] != digest:
            raise SystemExit(f"[BLOCKED] {name} changed since it was pinned")
        pins.setdefault(name, {"url": BASE + name, "retrieved": "2026-09-24", "sha256": digest,
                               "route": "direct, browser user agent"})
    PINS.write_text(json.dumps(pins, indent=1) + "\n")


def persons(d: pd.DataFrame, stem: str) -> np.ndarray:
    return d[[f"{stem}{k}" for k in range(1, P + 1)]].to_numpy(float)


def lin_se(num, den, w_num, w_den, strata):
    """SE of sum(num)/sum(den) (already weighted per unit) by stratified linearization."""
    r = num.sum() / den.sum()
    z = pd.Series((num - r * den) / den.sum())
    g = z.groupby(strata)
    n = g.transform("size")
    dev = z - g.transform("mean")
    var = (n / (n - 1).clip(lower=1) * dev ** 2).groupby(strata).sum().sum()
    return float(np.sqrt(var))


def main():
    fetch()
    with zipfile.ZipFile(CACHE / "qcfy2024_csv.zip") as z:
        d = pd.read_csv(z.open("qc_pub_fy2024.csv"), low_memory=False)
    w = d.FYWGT.to_numpy(float)
    if abs((w * d.FSUSIZE).sum() - TABLE_II2["individuals"]) > 1 or \
            abs((w * d.FSBEN).sum() / 1000 - TABLE_II2["benefits_thousand"]) > 1:
        raise SystemExit("[GATE FAIL] Table II.2 weighted totals")
    fsafil, race, ctzn, age, rel = (persons(d, s) for s in ("FSAFIL", "RACETH", "CTZN", "AGE", "REL"))
    listed = ~np.isnan(fsafil)
    part = fsafil == 1
    if not np.array_equal(part.sum(1), d.FSUSIZE.to_numpy()):
        raise SystemExit("[GATE FAIL] participants per unit differ from FSUSIZE")
    hisp = (race >= 13) & (race <= 22)
    nonh = (race >= 3) & (race <= 12)
    unk = listed & ~hisp & ~nonh
    # Appendix A anchors: national unreported share among weighted participants, and the 20 states.
    unk_part = (w[:, None] * (part & unk)).sum() / (w[:, None] * part).sum()
    if not 0.165 <= unk_part < 0.175:
        raise SystemExit(f"[GATE FAIL] unreported share {unk_part:.4f}, Appendix A says about 17 percent")
    by_state = pd.DataFrame({"state": d.STATENAME, "u": w * (part & unk).sum(1), "p": w * part.sum(1)}) \
        .groupby("state").sum()
    over10 = set(by_state.index[(by_state.u / by_state.p) >= 0.10])
    if over10 != APPX_A_20:
        raise SystemExit(f"[GATE FAIL] states >=10% unreported differ from Appendix A: {over10 ^ APPX_A_20}")

    # Imputation: own unit's known members first, then the state x noncitizen x child cell.
    known = hisp | nonh
    k_n = known.sum(1)
    unit_h = np.where(k_n > 0, hisp.sum(1) / np.maximum(k_n, 1), np.nan)
    noncit = ((ctzn >= 3) & listed).any(1)
    child = ((age < 18) & part).any(1)
    cell = pd.Series(d.STATENAME.astype(str) + "|" + noncit.astype(str) + "|" + child.astype(str))
    fully_known = (unk & part).sum(1) == 0
    ph = (w[:, None] * (part & hisp)).sum(1)
    pk = (w[:, None] * (part & known)).sum(1)
    cell_h = (pd.Series(ph[fully_known]).groupby(cell[fully_known].to_numpy()).sum()
              / pd.Series(pk[fully_known]).groupby(cell[fully_known].to_numpy()).sum())
    state_h = (pd.Series(ph).groupby(d.STATENAME.to_numpy()).sum()
               / pd.Series(pk).groupby(d.STATENAME.to_numpy()).sum())
    fill = cell.map(cell_h).to_numpy()
    fill = np.where(np.isnan(fill), d.STATENAME.map(state_h).to_numpy(), fill)
    p_unit = np.where(np.isnan(unit_h), fill, unit_h)             # probability for unknown members
    h_imp = np.where(hisp, 1.0, np.where(unk, p_unit[:, None], 0.0))

    head = rel == 1
    has_head = head.sum(1) == 1
    head = np.where(has_head[:, None], head, np.arange(P)[None, :] == 0)  # person 1 if no single head
    ben = d.FSBEN.to_numpy(float)
    n_part = part.sum(1)
    n_list = listed.sum(1)
    measures = {
        "participants": (part.astype(float), "persons with FSAFIL = 1"),
        "dollars": (part * (ben / np.maximum(n_part, 1))[:, None], "FSBEN split equally over participants"),
        "head_dollars": (head * ben[:, None], "FSBEN by the head's ethnicity"),
        "listed_dollars": (listed * (ben / np.maximum(n_list, 1))[:, None],
                           "FSBEN split equally over everyone listed in the home"),
        "listed_persons": (listed.astype(float), "everyone listed in the home"),
        "units_by_head": (head.astype(float), "SNAP units counted once, by the head's ethnicity"),
    }
    geos = {"US": np.ones(len(d), bool)}
    for s in sorted(d.STATENAME.unique()):
        geos[s] = (d.STATENAME == s).to_numpy()
    strata = d.STATENAME.to_numpy()
    rows = []
    for m, (x, note) in measures.items():
        xw = w[:, None] * x
        H, N, U = (xw * hisp).sum(1), (xw * nonh).sum(1), (xw * unk).sum(1)
        HI = (xw * h_imp).sum(1)
        T = xw.sum(1)
        for g, mask in geos.items():
            h, n, u, t, hi = H[mask], N[mask], U[mask], T[mask], HI[mask]
            if t.sum() <= 0:
                continue
            rows.append(dict(
                measure=m, note=note, geography=g, units=int(mask.sum()), total=t.sum(),
                unknown_share=u.sum() / t.sum(),
                hisp_share_known=h.sum() / (h + n).sum() if (h + n).sum() > 0 else np.nan,
                hisp_share_known_se=lin_se(h, h + n, None, None, strata[mask]) if (h + n).sum() > 0 else np.nan,
                hisp_share_lower=h.sum() / t.sum(), hisp_share_upper=(h + u).sum() / t.sum(),
                hisp_share_imputed=hi.sum() / t.sum(),
                hisp_share_imputed_se=lin_se(hi, t, None, None, strata[mask])))
    out = pd.DataFrame(rows)
    out.to_csv(HERE / "derived/admin_snap_qc.csv", index=False, lineterminator="\n")
    und = (ctzn == 8) & listed
    nonc = (ctzn >= 3) & listed
    groups = {"with_undocumented": part & und.any(1)[:, None], "noncitizen": part & nonc, "all": part}
    vrows = []
    for g, mask in geos.items():
        row = dict(geography=g, in_appendix_a_20=g in APPX_A_20)
        for name, sel in groups.items():
            sel = sel & mask[:, None]
            h, n_, u = ((w[:, None] * (sel & x)).sum() for x in (hisp, nonh, unk))
            row[f"{name}_records"] = int(sel.sum())
            row[f"{name}_hisp_share_known"] = h / (h + n_) if h + n_ > 0 else np.nan
            row[f"{name}_unknown_share"] = u / (h + n_ + u) if h + n_ + u > 0 else np.nan
        vrows.append(row)
    val = pd.DataFrame(vrows)
    val.to_csv(HERE / "derived/admin_snap_qc_validity.csv", index=False, lineterminator="\n")
    pd.set_option("display.width", 220)
    sel = out[out.geography.isin(["US", "Texas", "California", "Arizona", "New Mexico", "Nevada"])]
    print(sel.drop(columns=["note"]).round(4).to_string(index=False))
    print(val[val.geography.isin(["US", "California", "Nevada", "Arizona", "Texas", "New Mexico", "New Jersey",
                                  "North Carolina", "Pennsylvania"])].round(3).to_string(index=False))
    print(f"[gate] Table II.2 totals match; unreported share of participants {unk_part:.4f}; "
          f"the 20 states with >=10% unreported match Appendix A")


if __name__ == "__main__":
    main()
