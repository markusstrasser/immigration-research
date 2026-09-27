"""Child-stage identification loss per generation of the Mexican-origin parent, from this lane's
derived tables (intermarriage.csv, child_identification.csv). Replaces the 2026-09-27 RESULT
arithmetic 0.40 x 0.16, which multiplied a share of married *people* by a share of *children*.

Couple shares. Among married Mexican-origin persons of generation g, the spouse is Mexican origin
(m), other Hispanic (h) or non-Hispanic (q). A couple of two Mexican-origin persons contains two of
them, a mixed couple one, so under equal fertility per couple the shares of Mexican-origin-parented
children by couple type are m/2 : h : q, normalised by m/2 + h + q. With only the two types
Mexican x Mexican and Mexican x non-Hispanic (the audit's formula) the mixed share is 2q/(1+q).

Loss = sum over couple types of (child share) x (1 - identification rate of children of that
couple type), for "reported Hispanic" and "reported Mexican". Identification rates, both parents
biological: Mexican x non-Hispanic by the Mexican parent's generation; Mexican x Mexican with both
parents of generation g; Mexican x other Hispanic pooled over generations (not tabulated by
generation). The generation of the other Mexican-origin parent in an endogamous couple is taken
to be g. SE: delta method on the component SEs treated as independent (replicate `se` column).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DERIVED = HERE / "derived"
GENS = ["mex_G1", "mex_G2", "mex_G3plus"]


def inputs():
    im = pd.read_csv(DERIVED / "intermarriage.csv")
    im = im[im.adjustment == "raw"].set_index(["measure", "generation"])
    ci = pd.read_csv(DERIVED / "child_identification.csv").set_index(["adjustment", "generation", "measure"])
    out = {}
    for g in GENS:
        spouse = {k: (im.loc[(f"spouse_{v}", g), "estimate"], im.loc[(f"spouse_{v}", g), "se"], int(im.loc[(f"spouse_{v}", g), "n"]))
                  for k, v in (("m", "mexican_origin"), ("h", "other_hispanic"), ("q", "non_hispanic"))}
        rates = {}
        for outcome in ("id_hispanic", "id_mexican"):
            m = f"child_{outcome}"
            rates[outcome] = {
                "mixed_nh": ci.loc[("mexican_x_non_hispanic, Mexican parent's generation; both parents biological", g, m)],
                "endo": ci.loc[("both_mexican_origin, both parents this generation; both parents biological", g, m)],
                "mixed_oh": ci.loc[("mexican_x_other_hispanic; both parents biological", "all", m)],
            }
        out[g] = (spouse, rates)
    return out


def loss(x, three_type):
    m, h, q, r_nh, r_endo, r_oh = x
    if three_type:
        tot = m / 2 + h + q
        s_nh, s_oh, s_endo = q / tot, h / tot, (m / 2) / tot
    else:
        s_nh = 2 * q / (1 + q)
        s_oh, s_endo = 0.0, 1 - s_nh
    return s_nh * (1 - r_nh) + s_oh * (1 - r_oh) + s_endo * (1 - r_endo), s_nh, s_oh, s_endo


def delta_se(x, se, three_type):
    base = loss(x, three_type)[0]
    grad = []
    for i in range(len(x)):
        step = np.array(x, float)
        step[i] += 1e-6
        grad.append((loss(step, three_type)[0] - base) / 1e-6)
    return float(np.sqrt(np.sum((np.array(grad) * np.array(se)) ** 2)))


def build():
    rows = []
    for g, (spouse, rates) in inputs().items():
        for outcome, r in rates.items():
            for three_type, label in ((True, "three couple types m/2:h:q, equal fertility per couple"),
                                      (False, "two couple types, mixed share 2q/(1+q), equal fertility per couple")):
                x = [spouse["m"][0], spouse["h"][0], spouse["q"][0], r["mixed_nh"].estimate, r["endo"].estimate,
                     r["mixed_oh"].estimate]
                se = [spouse["m"][1], spouse["h"][1], spouse["q"][1], r["mixed_nh"].se, r["endo"].se, r["mixed_oh"].se]
                est, s_nh, s_oh, s_endo = loss(x, three_type)
                rows.append({"source": "CPS ASEC 2022-2025 (this lane: intermarriage.csv, child_identification.csv)",
                             "measure": f"child-stage loss: not {outcome.replace('id_', 'reported ')}",
                             "generation": g, "n": int(r["mixed_nh"].n + r["endo"].n), "estimate": est,
                             "se": delta_se(x, se, three_type), "adjustment": label,
                             "child_share_mexican_x_non_hispanic": s_nh, "child_share_mexican_x_other_hispanic": s_oh,
                             "child_share_mexican_x_mexican": s_endo, "q_spouse_non_hispanic": spouse["q"][0]})
    return pd.DataFrame(rows)


def main():
    t = build()
    t.to_csv(DERIVED / "identity_loss.csv", index=False, float_format="%.6g", lineterminator="\n")
    show = t.assign(pct=(100 * t.estimate).round(1).astype(str) + " (" + (100 * t.se).round(1).astype(str) + ")")
    print(show.pivot_table(index=["adjustment", "measure"], columns="generation", values="pct", aggfunc="first").to_string())
    print(t[["generation", "adjustment", "child_share_mexican_x_non_hispanic", "child_share_mexican_x_other_hispanic",
             "child_share_mexican_x_mexican"]].drop_duplicates().round(3).to_string())


if __name__ == "__main__":
    sys.exit(main())
