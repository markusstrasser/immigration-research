"""Solve eq. (8) over the repo-derived (a, tau) parameters at three congestion rates.

Outputs
  derived/mstar_by_outcome.csv  m*, m*/observed, T and the implied steady-state
                                unassimilated stock for every usable outcome x tau x c
  derived/mstar_grid.csv        a x tau x c grid, the Figure 3/9 surface re-solved
  derived/sign_flip.csv         where eq. (8) crosses zero, in both parameters

Reading note on "the stock at which the model turns the sign": eq. (8) has no
stock argument. m* is set by parameters alone and the sign turns when
a = rho*tau*gamma-tilde. Congestion c enters only the denominator, so it scales
m* but cannot flip it. What the stock does control is the realised TFP loss
through eq. (3), which this script reports at the observed Mexican-origin stock.
"""
import csv
import json
import os

import cpmodel as M

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "derived")

CONGESTION = (0.0, 0.5, 0.9)   # 0; the paper's Figure 8 upper bound; its "quite large"


def rd(name):
    with open(os.path.join(OUT, name), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    K = json.load(open(os.path.join(OUT, "paper_constants.json"), encoding="utf-8"))
    gamma, beta, alpha, rho = K["gamma"], K["beta"], K["alpha"], K["rho"]
    gt = M.gtil(gamma, beta, alpha)

    paper = {r["country"]: r for r in rd("paper_table1.csv")}
    mex = paper["Mexico"]
    a_paper, tau_paper = float(mex["a_paper"]), float(mex["tau_paper"])

    obs = {r["quantity"]: float(r["value"]) for r in rd("observed_migration.csv")}
    m_obs = obs["m_mexico, FY2024 LPR"]
    m_obs10 = obs["m_mexico, FY2015-FY2024 LPR mean"]
    phi_obs = obs["phi_mexico_born, stock share"]

    taus = rd("tau_repo.csv")
    # the construction nearest the paper's "five years after arrival"
    with_ysm = [t for t in taus if t["mean_ysm"] not in ("nan", "")]
    head = min(with_ysm, key=lambda t: abs(float(t["mean_ysm"]) - K["delta_years_since_arrival"]))
    tv = sorted(float(t["tau"]) for t in taus)
    TAUS = [
        ("paper Mexico row", tau_paper),
        ("repo, nearest 5 years since arrival", float(head["tau"])),
        ("repo minimum", tv[0]),
        ("repo maximum", tv[-1]),
    ]

    params = [r for r in rd("parameters.csv") if r["usable"] == "yes"]

    # ---- m* for every usable outcome -----------------------------------
    rows = []
    for p in params:
        for a_name, a_key in (("a(G1->G3+)", "a_g1_g3"), ("a(G1->G2)", "a_g1_g2"),
                              ("a(G2->G3+)", "a_g2_g3")):
            a = float(p[a_key])
            for t_name, tau in TAUS:
                for c in CONGESTION:
                    m = M.mstar(a, tau, c, gamma, beta, alpha, rho)
                    rows.append({
                        "domain": p["domain"], "outcome": p["outcome"], "a_basis": a_name,
                        "a": M.f(a, 6), "tau_basis": t_name, "tau": M.f(tau, 6), "c": M.f(c, 2),
                        "mstar": M.f(m, 6),
                        "mstar_over_observed": M.f(m / m_obs, 3),
                        "T_years": M.f(M.tstar(a, tau, c, gamma, beta, alpha, rho), 1),
                        "phi_at_optimum": M.f(m / a, 6) if m > 0 else "",
                    })
    # paper's own Mexico parameters, as the reference line
    for t_name, tau in TAUS:
        for c in CONGESTION:
            m = M.mstar(a_paper, tau, c, gamma, beta, alpha, rho)
            rows.append({
                "domain": "reference", "outcome": "paper Table 1 Mexico a",
                "a_basis": "paper individual-level", "a": M.f(a_paper, 6),
                "tau_basis": t_name, "tau": M.f(tau, 6), "c": M.f(c, 2),
                "mstar": M.f(m, 6), "mstar_over_observed": M.f(m / m_obs, 3),
                "T_years": M.f(M.tstar(a_paper, tau, c, gamma, beta, alpha, rho), 1),
                "phi_at_optimum": M.f(m / a_paper, 6) if m > 0 else "",
            })
    rows.sort(key=lambda r: (r["domain"], r["outcome"], r["a_basis"], r["tau_basis"], r["c"]))
    cols = ["domain", "outcome", "a_basis", "a", "tau_basis", "tau", "c",
            "mstar", "mstar_over_observed", "T_years", "phi_at_optimum"]
    with open(os.path.join(OUT, "mstar_by_outcome.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, cols)
        w.writeheader()
        w.writerows(rows)

    # ---- the (a, tau) surface, re-solved on a regular grid --------------
    grid = []
    for i in range(41):                      # a from 0.000 to 0.040 in 0.001
        a = i / 1000.0
        for j in range(1, 21):               # tau from 0.05 to 1.00 in 0.05
            tau = j / 20.0
            for c in CONGESTION:
                grid.append({"a": M.f(a, 3), "tau": M.f(tau, 2), "c": M.f(c, 2),
                             "mstar": M.f(M.mstar(a, tau, c, gamma, beta, alpha, rho), 6)})
    with open(os.path.join(OUT, "mstar_grid.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, ["a", "tau", "c", "mstar"])
        w.writeheader()
        w.writerows(grid)

    # ---- sign flip ------------------------------------------------------
    flips = []
    for p in params:
        a = float(p["a_g1_g3"])
        flips.append({
            "basis": f"{p['domain']}: {p['outcome']}", "kind": "a fixed, tau that sets m*=0",
            "a": M.f(a, 6), "tau_flip": M.f(M.tau_sign_flip(a, gamma, beta, alpha, rho), 6),
            "note": "m* > 0 only for tau below this",
        })
    for t_name, tau in TAUS:
        flips.append({
            "basis": f"tau: {t_name}", "kind": "tau fixed, a that sets m*=0",
            "a": M.f(M.a_sign_flip(tau, gamma, beta, alpha, rho), 6),
            "tau_flip": M.f(tau, 6), "note": "m* > 0 only for a above this",
        })
    flips.sort(key=lambda r: (r["kind"], r["basis"]))
    with open(os.path.join(OUT, "sign_flip.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, ["kind", "basis", "a", "tau_flip", "note"])
        w.writeheader()
        w.writerows(flips)

    # ---- console summary -------------------------------------------------
    print(f"gamma-tilde {M.f(gt,6)}; observed m_mexico {m_obs:.6f} (FY2024 LPR), "
          f"{m_obs10:.6f} (10-year mean); Mexico-born stock share {phi_obs:.4f}")
    tau_h = float(head["tau"])
    print(f"headline tau {M.f(tau_h,4)} from: {head['construction']}")
    print(f"a needed for m* > 0 at that tau: {M.f(M.a_sign_flip(tau_h, gamma, beta, alpha, rho), 6)}")
    for dom in ("earnings", "fiscal", "norms"):
        vals = sorted(float(p["a_g1_g3"]) for p in params if p["domain"] == dom)
        if vals:
            print(f"  a(G1->G3+) {dom:<9} {M.f(vals[0],5)} .. {M.f(vals[-1],5)}  (n={len(vals)})")


if __name__ == "__main__":
    main()
