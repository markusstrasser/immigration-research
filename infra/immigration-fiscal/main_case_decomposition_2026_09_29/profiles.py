"""Age profiles of the keys the September 27 main case charges, for the union and the national frame.

For every per-person key vector the account allocates by (the complete account's own definitions, built
by the generation lane's read-only imports: `generation_account_2026_09_24/frame.py` and `keys.py`, which
take them from `cps_imputation_keys_2026_09_23/common.py`), this writes the key's weighted total in each
age bin, once over the canonical union and once over the civilian national frame, under two weight sets:

  published  the ASEC 2025 person weights (union 40.897M);
  row4       audit row 4's weights, the ones the case's stack uses: Mexico-born persons outside CA+TX
             scaled to their ACS 2024 cells (`combine_onbooks_lane.weight_arms`, arm "row4"; union
             39.712M). The case's corrected account charges its per-head lines for this count.

Age bins: single years 0-24, five-year bins 25-79, then the CPS top codes 80 (80-84) and 85 (85+).
Extra vectors: `exposure_py` (uninsured person-years, NOCOV_CYR, the uncompensated-care lane's
exposure) and `population`. The national arrest profile by age (FBI CIUS 2024 Table 38, all offenses)
is spread over the bins by national population and written beside the keys; decompose.cjs uses it for
the justice key's non-per-head parts.

Gates (exit 1): every key's union and national totals under the published weights reproduce the
generation lane's `derived/generation_keys.csv` (convention a, 1e-9 relative); bins add to totals; the
row-4 union count reproduces 39.712M (the CPS lane's RESULT, to 0.001M).
Outputs: derived/age_bins.csv, derived/arrest_profile.csv. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/main_case_decomposition_2026_09_29/profiles.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import csv  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
sys.path.insert(0, str(FISCAL / "generation_account_2026_09_24"))
import frame as F  # noqa: E402  (puts the CPS lane on sys.path)
import keys as K  # noqa: E402
import combine_onbooks_lane as L  # noqa: E402

C = F.C
OUT = HERE / "derived"
ALLOC = ["personal", "shared"]
EDGES = list(range(25)) + list(range(25, 81, 5)) + [85]  # bin lower bounds; 80 = CPS 80-84, 85 = 85+
ARRESTS = FISCAL / "nibrs_arrests_2026_09_16/_cache/x/pa2024/CIUS_Table_38_Arrests_by_Age_2024.xlsx"
FAILS: list[str] = []


def gate(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def bins_of(age):
    return np.searchsorted(np.array(EDGES), age, side="right") - 1


def arrest_profile(pop_bins):
    """CIUS 2024 Table 38 TOTAL row, spread over the bins by national population within each CIUS band."""
    x = pd.read_excel(ARRESTS, header=None)
    head = [str(v).replace("\n", " ").strip() for v in x.iloc[4]]
    total = x.iloc[5]
    if str(total.iloc[0]).strip() != "TOTAL":
        raise SystemExit("[BLOCKED] CIUS Table 38 layout changed: no TOTAL row at line 6")
    bands = {"Under 10": (0, 9), "10-12": (10, 12), "13-14": (13, 14), "25-29": (25, 29), "30-34": (30, 34),
             "35-39": (35, 39), "40-44": (40, 44), "45-49": (45, 49), "50-54": (50, 54), "55-59": (55, 59),
             "60-64": (60, 64), "65 and over": (65, 200)}
    for a in range(15, 25):
        bands[str(a)] = (a, a)
    got = {}
    for label, value in zip(head, total):
        key = label.replace("Ages ", "").strip()
        key = "17" if key == "17.0" else key
        if key in bands:
            got[key] = float(value)
    if set(got) != set(bands):
        raise SystemExit(f"[BLOCKED] CIUS Table 38 bands not all found: {sorted(set(bands) - set(got))}")
    lo = np.array(EDGES)
    arrests = np.zeros(len(EDGES))
    for key, (a, b) in bands.items():
        inside = (lo >= a) & (lo <= b)
        arrests[inside] += got[key] * pop_bins[inside] / pop_bins[inside].sum()
    gate("CIUS 2024 arrests spread over the bins add to the table's total of the listed bands",
         abs(arrests.sum() - sum(got.values())) < 1e-6, f"{arrests.sum():,.0f}")
    return arrests, sum(got.values())


def main():
    print("[frame]", flush=True)
    d = F.load()
    civ, union, _ = F.masks(d)
    W = d[F.REPS].to_numpy(float)
    print("[row 4 weights]", flush=True)
    cells = L.acs_cells()
    arms, info = L.weight_arms(d, W, cells)
    weights = {"published": W[:, 0], "row4": arms["row4"][:, 0]}
    del arms, W
    n4 = float(weights["row4"][union].sum())
    gate("row-4 union count reproduces the CPS lane's 39.712M", abs(n4 / 1e6 - 39.712) < 0.001, f"{n4 / 1e6:.6f}M")
    b = bins_of(d.A_AGE.to_numpy())
    index = C.spm_index(d)

    print("[keys]", flush=True)
    rkeys = C.receipt_keys(d, index)
    skeys = C.spending_vectors(d, index)
    medical, _, _, _ = K.meps_keys(d)
    _, params = K.owner_property(d)
    edu = K.school_keys(d, civ, params)
    exposure = d.NOCOV_CYR.eq(3).to_numpy(float) + 0.5 * d.NOCOV_CYR.eq(2).to_numpy(float)
    vectors = {}
    for a in ALLOC:
        v = {f"receipt|{k}": x for k, x in rkeys[a].items()}
        v.update({f"spending|{k}": x for k, x in skeys[a].items()})
        v.update({f"spending|{k}": x for k, x in medical.items()})
        v["spending|school_operating"] = edu[a]["school"]
        v["spending|postsecondary"] = edu[a]["P"]
        v["spending|education_mix"] = edu[a]["school"] + edu[a]["P"]
        v["extra|exposure_py"] = exposure
        vectors[a] = v

    print("[gates against the generation lane's key totals]", flush=True)
    pub = pd.read_csv(FISCAL / "generation_account_2026_09_24/derived/generation_keys.csv")
    pub = pub[pub.convention.eq("a")]
    w = weights["published"]
    checked, worst = 0, 0.0
    for a in ALLOC:
        for name, v in vectors[a].items():
            side, key = name.split("|")
            if side == "extra":
                continue
            row = pub[(pub.side == side) & (pub.allocation == a) & (pub.key == key)]
            if row.empty:
                continue
            u, n = float(v[union] @ w[union]), float(v[civ] @ w[civ])
            ru, rn = float(row.union.iloc[0]), float(row.national.iloc[0])
            rel = max(abs(u / ru - 1) if ru else abs(u), abs(n / rn - 1) if rn else abs(n))
            worst = max(worst, rel)
            checked += 1
    gate(f"{checked} key totals reproduce generation_keys.csv (union and national, convention a)", worst < 1e-9,
         f"worst relative difference {worst:.1e}")

    print("[bins]", flush=True)
    rows = []
    nb = len(EDGES)
    pop_bins = {}
    for wname, wv in weights.items():
        wu, wc = np.where(union, wv, 0.0), np.where(civ, wv, 0.0)
        pu = np.bincount(b, weights=wu, minlength=nb)
        pc = np.bincount(b, weights=wc, minlength=nb)
        pop_bins[wname] = pc
        if (pu <= 0).any():
            gate(f"{wname}: every bin holds union members", False)
        for i in range(nb):
            rows.append(dict(weights=wname, allocation="both", key="extra|pop", bin=EDGES[i], union=pu[i], national=pc[i]))
        for a in ALLOC:
            for name, v in vectors[a].items():
                ub = np.bincount(b, weights=v * wu, minlength=nb)
                cb = np.bincount(b, weights=v * wc, minlength=nb)
                if abs(ub.sum() - float(v[union] @ wv[union])) > 1e-6 * max(1.0, abs(ub.sum())):
                    gate(f"{wname}/{a}/{name}: bins add to the union total", False)
                for i in range(nb):
                    rows.append(dict(weights=wname, allocation=a, key=name, bin=EDGES[i], union=ub[i], national=cb[i]))
    OUT.mkdir(exist_ok=True)
    with (OUT / "age_bins.csv").open("w", newline="") as handle:
        out = csv.DictWriter(handle, fieldnames=["weights", "allocation", "key", "bin", "union", "national"],
                             lineterminator="\n")
        out.writeheader()
        for r in rows:
            out.writerow({**r, "union": repr(float(r["union"])), "national": repr(float(r["national"]))})
    arrests, total = arrest_profile(pop_bins["published"])
    with (OUT / "arrest_profile.csv").open("w", newline="") as handle:
        out = csv.writer(handle, lineterminator="\n")
        out.writerow(["bin", "arrests_2024", "share"])
        for i in range(nb):
            out.writerow([EDGES[i], repr(float(arrests[i])), repr(float(arrests[i] / total))])
    print(f"  row-4 factors: naturalized {info['factor_natz']:.6f}, noncitizen {info['factor_noncit']:.6f}; "
          f"union {float(weights['published'][union].sum()) / 1e6:.6f}M published, {n4 / 1e6:.6f}M row 4; national "
          f"{float(weights['published'][civ].sum()) / 1e6:.6f}M / {float(weights['row4'][civ].sum()) / 1e6:.6f}M", flush=True)
    print(f"  wrote {len(rows)} bin rows and {nb} arrest bins", flush=True)
    if FAILS:
        print(f"FAIL: {len(FAILS)} gate(s): {FAILS}")
        sys.exit(1)
    print("  all profile gates passed")


if __name__ == "__main__":
    main()
