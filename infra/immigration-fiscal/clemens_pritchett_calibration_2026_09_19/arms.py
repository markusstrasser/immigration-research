"""Disconfirmation arms: constructions that could reverse the headline, run and reported.

Headline being tested: with the repo's generational assimilation rate and its own
cohort-measured transmission rate for Mexico, eq. (8) returns m* <= 0, i.e. the
paper's conclusion does not survive substitution.

Arms
  A0  headline, no correction
  A1  ethnic attrition: the self-identified third generation is negatively selected,
      so the measured G3+ gap overstates the lineage gap and understates a
  A2  reference group: the repo residual is against US-born non-Hispanic whites,
      the paper's against all US natives, which inflates the repo delta and tau
  A3  both corrections at once (the arm most likely to reverse the sign)
  A4  generation length 25 instead of 29 years
  A5  substitute only a, keeping the paper's own Mexico tau
  A6  substitute only tau, keeping the paper's own Mexico a
  A7  the paper's own Mexico row, as the reference line
  A8  upper-bound a: the fastest-converging measured outcome of any domain
  A9  the opposite bound on tau: unconditional earnings gap instead of the
      education-conditional residual

Every arm resting on a repo-measured a is run at both ends of the economic-outcome
range, because the range across constructions is the headline, not any one point.

Output: derived/arms.csv
"""
import csv
import json
import math
import os

import cpmodel as M

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "derived")
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

# Ethnic attrition among third-generation Mexican-ancestry youth. Memo section 1
# and ladder entry 67 give 17% (Duncan & Trejo) rising to 30% among youth, with
# leavers positively selected.
ATTRITION = (0.17, 0.30)
MEMO = "research/immigration-mexican-origin-by-generation-2026-09-16.md"
C_REF = 0.5      # the paper's Figure 8 upper bound on congestion
GEN_YEARS = 29.0


def rd(name):
    with open(os.path.join(OUT, name), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def white_vs_all_native_log_gap():
    """ln(all-native mean earnings / white mean earnings) from the memo's own row."""
    path = os.path.join(REPO, MEMO)
    for i, ln in enumerate(open(path, encoding="utf-8").read().splitlines(), 1):
        if ln.startswith("| Mean earnings, all adults, $ |"):
            v = [float(c.strip().split(" ")[0].replace(",", ""))
                 for c in ln.strip("|").split("|")[1:6]]
            return math.log(v[4] / v[3]), f"{MEMO}:{i}"
    raise SystemExit("memo mean-earnings row not found")


def main():
    K = json.load(open(os.path.join(OUT, "paper_constants.json"), encoding="utf-8"))
    gamma, beta, alpha, rho = K["gamma"], K["beta"], K["alpha"], K["rho"]
    mex = next(r for r in rd("paper_table1.csv") if r["country"] == "Mexico")
    a_paper, tau_paper = float(mex["a_paper"]), float(mex["tau_paper"])

    obs = {r["quantity"]: float(r["value"]) for r in rd("observed_migration.csv")}
    m_obs = obs["m_mexico, FY2024 LPR"]

    head = min((t for t in rd("tau_repo.csv") if t["mean_ysm"] not in ("nan", "")),
               key=lambda t: abs(float(t["mean_ysm"]) - K["delta_years_since_arrival"]))
    tau_repo, resid_repo = float(head["tau"]), float(head["resid_lnw"])
    gamma_mex = float(head["gamma"])

    params = [r for r in rd("parameters.csv") if r["usable"] == "yes"]
    econ = [p for p in params if p["domain"] in ("earnings", "fiscal")]
    a_econ = {p["outcome"]: float(p["a_g1_g3"]) for p in econ}
    a_lo, a_hi = min(a_econ.values()), max(a_econ.values())
    slow_name = min(a_econ, key=a_econ.get)
    fast_econ_name = max(a_econ, key=a_econ.get)
    fast_row = max(params, key=lambda p: float(p["a_g1_g3"]))
    a_fast, fast_name = float(fast_row["a_g1_g3"]), fast_row["outcome"]

    rows = []

    def add(arm, desc, a, tau, note=""):
        m = M.mstar(a, tau, C_REF, gamma, beta, alpha, rho)
        rows.append({
            "arm": arm, "description": desc,
            "a": M.f(a, 6), "tau": M.f(tau, 6), "c": M.f(C_REF, 2),
            "a_needed_for_positive_mstar": M.f(M.a_sign_flip(tau, gamma, beta, alpha, rho), 6),
            "mstar": M.f(m, 6), "mstar_over_observed": M.f(m / m_obs, 3),
            "sign": "positive" if m > 0 else "zero or negative",
            "reverses_headline": "yes" if m > 0 else "no",
            "note": note,
        })

    def add_both(arm, desc, a_slow, a_fast_, tau, note=""):
        add(arm + " [slow end]", desc, a_slow, tau, f"{note}; {slow_name}")
        add(arm + " [fast end]", desc, a_fast_, tau, f"{note}; {fast_econ_name}")

    add_both("A0 headline", "repo generational a, repo cohort tau, c=0.5",
             a_lo, a_hi, tau_repo, "no correction")

    for s in ATTRITION:
        bump = -math.log(1.0 - s) / (2 * GEN_YEARS)
        add_both(f"A1 attrition {s:.0%}",
                 "third-generation gap scaled by (1-s), leavers assumed fully converged",
                 a_lo + bump, a_hi + bump, tau_repo,
                 f"upper bound on the correction, adds {bump:.6f} to a")

    dlog, dsrc = white_vs_all_native_log_gap()
    resid_adj = resid_repo - dlog          # dlog is negative, so this shrinks the gap
    tau_adj = (1.0 - math.exp(resid_adj)) / gamma_mex
    add_both("A2 reference group",
             f"delta re-referenced from white natives to all natives using {dsrc}",
             a_lo, a_hi, tau_adj, f"log shift {dlog:.6f}, tau {tau_repo:.4f} -> {tau_adj:.4f}")

    for s in ATTRITION:
        bump = -math.log(1.0 - s) / (2 * GEN_YEARS)
        add_both(f"A3 attrition {s:.0%} + reference group", "both corrections at once",
                 a_lo + bump, a_hi + bump, tau_adj, "the arm most able to reverse the sign")

    a25 = [float(p["a_g1_g3_gen25"]) for p in econ]
    add_both("A4 generation 25 years", "shorter generational interval raises a",
             min(a25), max(a25), tau_repo, "brief stipulates 29, 25 is the aggressive end")

    add_both("A5 repo a only", "repo generational a with the paper's own Mexico tau",
             a_lo, a_hi, tau_paper, "isolates the assimilation substitution")
    add("A6 repo tau only", "the paper's Mexico a with the repo's cohort tau",
        a_paper, tau_repo, "isolates the transmission substitution")
    add("A7 paper both", "the paper's own Mexico row, reproduced",
        a_paper, tau_paper, "gate reference line")
    add("A8 fastest measured outcome", f"a from {fast_name}",
        a_fast, tau_repo, "upper bound on a from any repo outcome, an attitude item")

    unc = next(p for p in params if p["outcome"] == "mean earnings, adults 25-64")
    tau_unc = min(float(unc["g1"]) / gamma_mex, 1.0)
    add_both("A9 unconditional tau", "delta from the unconditional mean-earnings gap",
             a_lo, a_hi, tau_unc,
             "not the paper's definition, its gamma is already net of human capital, "
             "shown as the opposite bound")

    cols = ["arm", "description", "a", "tau", "c", "a_needed_for_positive_mstar",
            "mstar", "mstar_over_observed", "sign", "reverses_headline", "note"]
    with open(os.path.join(OUT, "arms.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, cols)
        w.writeheader()
        w.writerows(rows)

    n_rev = sum(1 for r in rows if r["reverses_headline"] == "yes")
    for r in rows:
        print(f"{r['arm']:<40} a={r['a']} tau={r['tau']} need={r['a_needed_for_positive_mstar']} "
              f"m*={r['mstar']:>10} ({r['mstar_over_observed']:>8}x obs)  reverses={r['reverses_headline']}")
    print(f"\n{n_rev}/{len(rows)} arms give a positive m*.")


if __name__ == "__main__":
    main()
