"""Reproduction gate: rebuild the paper's own reported figures from its stated
parameters before any repo value is substituted.

Seven checks, all against numbers parsed out of _cache/dp9730.txt by parse_paper.py:

  G1  delta (initial earnings gap at 5 years) for all 9 countries, from (zeta, lambda, mu)
  G2  a (individual assimilation) for all 9 countries, from the eq. (12) half-life
  G3  tau = delta/gamma for all 9 countries
  G4  the section 5.3 text claim: c=0.5, tau<0.5, a>0.03  =>  m* > 0.01
  G5  the section 8 stated ranges for a and tau are the Table 1 min/max
  G6  the Figure 9 claim: at c=0.5 every country's m* is "at least several times" m0
  G7  eq. (9) and footnote 5 give the same transition time T

Output: derived/gate_log.txt (human), derived/gate.csv (per-country numbers).
"""
import csv
import json
import os

import cpmodel as M

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "derived")

SEVERAL = 3.0  # reading of "at least several times current levels" (Figure 9 text)


def load():
    with open(os.path.join(OUT, "paper_table1.csv"), encoding="utf-8") as fh:
        rows = [{k: (v if k == "country" else float(v)) for k, v in r.items()}
                for r in csv.DictReader(fh)]
    with open(os.path.join(OUT, "paper_constants.json"), encoding="utf-8") as fh:
        const = json.load(fh)
    return rows, const


def main():
    rows, K = load()
    gamma, beta, alpha, rho = K["gamma"], K["beta"], K["alpha"], K["rho"]
    g = M.gtil(gamma, beta, alpha)
    log = []
    checks = []

    log.append("Clemens & Pritchett, IZA DP 9730 (Feb 2016) -- reproduction gate")
    log.append("source PDF sha256 pinned in _cache/SHA256SUMS.txt; text via pdftotext -layout")
    log.append(f"known parameters parsed from section 5.3: gamma={gamma} beta={beta} "
               f"alpha={alpha} rho={rho}; derived gamma-tilde={M.f(g)}")
    log.append("")

    # ---- G1/G2/G3 per country ----------------------------------------
    per = []
    for r in rows:
        z, lam, mu = r["zeta"], r["lambda"], r["mu"]
        d = M.initial_gap(z, lam, mu, K["delta_years_since_arrival"])
        t_half, a = M.half_life_assimilation(z, lam, mu)
        tau = r["delta_paper"] / r["gamma_country"]
        ms = M.mstar(r["a_paper"], r["tau_paper"], K["congestion_upper"], gamma, beta, alpha, rho)
        per.append({
            "country": r["country"],
            "delta_calc": d, "delta_paper": r["delta_paper"], "delta_abs_err": abs(d - r["delta_paper"]),
            "t_half_calc": t_half,
            "a_calc": a, "a_paper": r["a_paper"], "a_rel_err": abs(a - r["a_paper"]) / r["a_paper"],
            "tau_calc": tau, "tau_paper": r["tau_paper"], "tau_abs_err": abs(tau - r["tau_paper"]),
            "mstar_c0.5": ms, "mstar_over_m0": ms / K["m0_observed"],
            "T_years_c0.5": M.tstar(r["a_paper"], r["tau_paper"], K["congestion_upper"], gamma, beta, alpha, rho),
            # eq. (2) steady-state unassimilated share at the paper's own optimum
            "phi_at_optimum": ms / r["a_paper"],
        })

    d_max = max(p["delta_abs_err"] for p in per)
    a_max = max(p["a_rel_err"] for p in per)
    t_max = max(p["tau_abs_err"] for p in per)
    checks.append(("G1 delta, 9 countries, |err| <= 0.001", d_max <= 0.001, f"max abs err {M.f(d_max)}"))
    checks.append(("G2 a, 9 countries, rel err <= 0.01", a_max <= 0.01, f"max rel err {M.f(a_max)}"))
    checks.append(("G3 tau = delta/gamma, 9 countries, |err| <= 0.001", t_max <= 0.001, f"max abs err {M.f(t_max)}"))

    # ---- G4 the section 5.3 text claim -------------------------------
    m_claim = M.mstar(K["claim_a"], K["claim_tau"], K["claim_c"], gamma, beta, alpha, rho)
    ok4 = m_claim > K["claim_mstar"]
    checks.append((f"G4 c={K['claim_c']}, tau={K['claim_tau']}, a={K['claim_a']} => m* > {K['claim_mstar']}",
                   ok4, f"m* = {M.f(m_claim)}"))

    # ---- G5 stated ranges are the Table 1 min/max ---------------------
    a_lo, a_hi = min(r["a_paper"] for r in rows), max(r["a_paper"] for r in rows)
    t_lo, t_hi = min(r["tau_paper"] for r in rows), max(r["tau_paper"] for r in rows)
    # the prose quotes the Table 1 extremes at the precision it prints them,
    # so compare after rounding to the stated number of decimals
    def tol(x):
        s = repr(float(x))
        return 0.5 * 10 ** -(len(s.split(".")[1]) if "." in s else 0)

    ok5 = all(abs(v - s) <= tol(s) + 1e-12 for v, s in
              ((a_lo, K["range_a_lo"]), (a_hi, K["range_a_hi"]),
               (t_lo, K["range_tau_lo"]), (t_hi, K["range_tau_hi"])))
    checks.append(("G5 section 8 ranges == Table 1 min/max (at the prose's precision)", ok5,
                   f"a [{a_lo}, {a_hi}] vs stated [{K['range_a_lo']}, {K['range_a_hi']}] "
                   f"(the stated lower bound is Somalia's {a_lo} rounded); "
                   f"tau [{t_lo}, {t_hi}] vs stated [{K['range_tau_lo']}, {K['range_tau_hi']}]"))

    # ---- G6 Figure 9 claim -------------------------------------------
    worst = min(per, key=lambda p: p["mstar_over_m0"])
    ok6 = worst["mstar_over_m0"] >= SEVERAL
    checks.append((f"G6 Figure 9: every country's m* at c=0.5 is >= {SEVERAL:.0f}x m0={K['m0_observed']}",
                   ok6, f"minimum is {worst['country']} at {M.f(worst['mstar_over_m0'], 2)}x "
                        f"(m* = {M.f(worst['mstar_c0.5'])})"))

    # ---- G7 eq. (9) vs footnote 5 ------------------------------------
    m_probe = 0.01
    t9 = (beta - 1.0 - (1.0 - gamma) ** (1.0 / (1.0 - alpha))) / m_probe
    tf = M.tstar_footnote(m_probe, gamma, beta, alpha)
    ok7 = abs(t9 - tf) < 1e-9
    checks.append(("G7 eq. (9) transition time == footnote 5 form", ok7,
                   f"eq9 {M.f(t9, 9)} vs fn5 {M.f(tf, 9)}"))

    # ---- write ---------------------------------------------------------
    cols = ["country", "delta_calc", "delta_paper", "delta_abs_err", "t_half_calc",
            "a_calc", "a_paper", "a_rel_err", "tau_calc", "tau_paper", "tau_abs_err",
            "mstar_c0.5", "mstar_over_m0", "T_years_c0.5", "phi_at_optimum"]
    with open(os.path.join(OUT, "gate.csv"), "w", encoding="utf-8") as fh:
        fh.write(",".join(cols) + "\n")
        for p in per:
            fh.write(",".join(M.f(p[c], 6) if c != "country" else p[c] for c in cols) + "\n")

    log.append("Per-country reproduction (paper Table 1 rows recomputed from its own coefficients):")
    log.append(f"{'country':<11}{'delta':>18}{'a':>20}{'tau':>18}{'m*(c=0.5)':>12}{'x m0':>8}")
    for p in per:
        log.append(f"{p['country']:<11}"
                   f"{M.f(p['delta_calc'],4)+' vs '+M.f(p['delta_paper'],4):>18}"
                   f"{M.f(p['a_calc'],4)+' vs '+M.f(p['a_paper'],4):>20}"
                   f"{M.f(p['tau_calc'],3)+' vs '+M.f(p['tau_paper'],3):>18}"
                   f"{M.f(p['mstar_c0.5'],4):>12}{M.f(p['mstar_over_m0'],1):>8}")
    log.append("")
    log.append("Baseline transition time, eq. (9): at the paper's own observed rate "
               f"m0={K['m0_observed']}, T = {M.f(M.tstar_footnote(K['m0_observed'], gamma, beta, alpha), 0)} years; "
               f"at Mexico's Table 1 m* it is "
               f"{M.f(next(p['T_years_c0.5'] for p in per if p['country']=='Mexico'), 0)} years.")
    log.append("")
    over = [p for p in per if p["phi_at_optimum"] >= 1.0]
    log.append("Diagnostic, not a gate check: eq. (2) puts the steady-state unassimilated share "
               "at phi = m/a, and eq. (2) states 0 < phi < 1.")
    log.append("  phi at each country's own reported optimum (c=0.5): "
               + ", ".join(f"{p['country']} {M.f(p['phi_at_optimum'], 2)}" for p in per))
    log.append(f"  {len(over)} of {len(per)} countries have phi >= 1 at their own optimum: "
               + (", ".join(p["country"] for p in over) or "none")
               + ". At phi >= 1 the congestion term 1-c*phi in eq. (3) is at or past its"
                 " own bound and the first-order approximations behind eq. (8) do not hold.")
    log.append("")
    log.append("Checks:")
    n_ok = 0
    for name, ok, detail in checks:
        n_ok += bool(ok)
        log.append(f"  [{'PASS' if ok else 'FAIL'}] {name}  --  {detail}")
    log.append("")
    log.append(f"GATE: {n_ok}/{len(checks)} checks pass "
               f"(brief requires at least 2 reported optimal-migration figures reproduced).")

    with open(os.path.join(OUT, "gate_log.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(log) + "\n")
    print("\n".join(log))
    raise SystemExit(0 if n_ok == len(checks) else 1)


if __name__ == "__main__":
    main()
