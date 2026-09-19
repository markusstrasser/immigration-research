"""Assemble the repo's Mexican-origin measurements as Clemens-Pritchett parameters.

Assimilation a: every outcome is a gap of a Mexican-origin generation against
third-plus non-Hispanic whites. The model's a is the exponential decay rate of
the unassimilated deviation, so a = -ln(gap_late/gap_early)/years, the same
convention as the paper's own a = ln2/t_half.

Transmission tau: the paper's method is tau = delta/gamma with delta the
earnings gap of a new immigrant conditional on age, education and sex, five
years after arrival, and gamma the origin-country TFP gap. The repo's
arrival-cohort lane computes exactly that delta object (log wage residual of
Mexico-born full-time full-year workers against US-born non-Hispanic white
cells of the same year, sex, age group and education), by years-since-arrival
band, so it substitutes directly.

Reads (all read-only repo files, never modified) and writes derived/parameters.csv,
derived/tau_repo.csv, derived/inputs_provenance.csv.
"""
import csv
import os
import re

import cpmodel as M

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "derived")
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
INFRA = os.path.join(REPO, "infra", "immigration-fiscal")

GEN_YEARS = 29.0          # brief stipulation: one generation = 29 years
GEN_YEARS_SENS = (25.0, 33.0)

# Origin TFP gap for Mexico. The paper's own Table 1 value, from Jones (2016),
# is used as primary because it is the denominator its tau is defined against.
GAMMA_MEXICO_SOURCE = "Clemens & Pritchett Table 1 (gamma from Jones 2016), parsed from _cache/dp9730.txt"


def read_csv(path):
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------- outcomes


def cps_gap_outcomes():
    """Common-age per-person earnings and income gaps vs third-plus NH whites."""
    p = os.path.join(INFRA, "acs_earnings_replication_2026_09_17", "derived", "cps_gaps.csv")
    rows = read_csv(p)
    src = "infra/immigration-fiscal/acs_earnings_replication_2026_09_17/derived/cps_gaps.csv"
    out = []
    for var, label in (("WSAL_VAL", "CPS wage and salary, common age"),
                       ("PTOTVAL", "CPS total personal income, common age")):
        g = {}
        for r in rows:
            if (r["survey"] == "CPS" and r["domain"] == "national"
                    and r["reference"] == "third_plus_nh_white" and r["variable"] == var):
                g[r["group"]] = float(r["common_age_gap_per_person"])
        out.append({
            "domain": "earnings", "outcome": label, "units": "$ per standardized person",
            "g1": g["mexico_born"], "g2": g["mexican_second_gen"],
            "g3": g["mexican_third_plus_selfid"], "source": src,
            "tag": "SOURCE", "note": "reference third-plus NH white; replicate-variance SEs in the file",
        })
    return out


def ledger_outcomes():
    """Fiscal balance gaps vs third-plus NH whites at two standardization standards."""
    est = os.path.join(INFRA, "all_age_ledger_2026_09_17", "derived", "estimates.csv")
    stm = os.path.join(INFRA, "ledger_stress_2026_09_17", "derived", "state_matched.csv")
    src_age = "infra/immigration-fiscal/all_age_ledger_2026_09_17/derived/estimates.csv"
    src_sp = "infra/immigration-fiscal/ledger_stress_2026_09_17/derived/state_matched.csv"
    rows_age, rows_sp = read_csv(est), read_csv(stm)
    keys = ("mexico_born", "mexican_second_gen", "mexican_third_plus_selfid")
    out = []
    for scen in ("all_age_shared", "personal_sources"):
        a = {r["target"]: float(r["estimate"]) for r in rows_age
             if r["scenario"] == scen and r["reference"] == "third_plus_nh_white"
             and r["matching"] == "common_age"}
        s = {r["target"]: float(r["estimate"]) for r in rows_sp
             if r["scenario"] == scen and r["reference"] == "third_plus_nh_white"
             and r["cells"] == "state_x_age" and r["metric"] == "standardized_gap_per_person"}
        out.append({
            "domain": "fiscal", "outcome": f"ledger balance, common age ({scen})",
            "units": "$ per standardized person per year",
            "g1": a[keys[0]], "g2": a[keys[1]], "g3": a[keys[2]], "source": src_age,
            "tag": "SOURCE", "note": "all ages, age-only standard (ladder 125 'common age')",
        })
        out.append({
            "domain": "fiscal", "outcome": f"ledger balance, common age and place ({scen})",
            "units": "$ per standardized person per year",
            "g1": s[keys[0]], "g2": s[keys[1]], "g3": s[keys[2]], "source": src_sp,
            "tag": "SOURCE", "note": "joint state x age cells (ladder 125 'common age and place')",
        })
    return out


def memo_outcomes():
    """Two headline earnings levels quoted from the generation memo's own table."""
    memo = "research/immigration-mexican-origin-by-generation-2026-09-16.md"
    path = os.path.join(REPO, memo)
    lines = open(path, encoding="utf-8").read().splitlines()

    def cell(label):
        for i, ln in enumerate(lines, 1):
            if ln.startswith(f"| {label} |"):
                v = [c.strip().split(" ")[0].replace(",", "").replace("$", "")
                     for c in ln.strip("|").split("|")]
                return i, [float(x) for x in v[1:6]]
        raise SystemExit(f"memo row {label!r} not found")

    out = []
    for label, name in (("Mean earnings, all adults, $", "mean earnings, adults 25-64"),
                        ("Median earnings, workers, $", "median earnings, workers 25-64")):
        ln, v = cell(label)
        mex1, mex2, mex3, white = v[0], v[1], v[2], v[3]
        out.append({
            "domain": "earnings", "outcome": name, "units": "share of white-native level",
            "g1": 1.0 - mex1 / white, "g2": 1.0 - mex2 / white, "g3": 1.0 - mex3 / white,
            "source": f"{memo}:{ln}", "tag": "CALCULATION",
            "note": f"1 - group/white from the memo row; white level {white:.0f}; unconditional",
        })
    return out


def norms_outcomes():
    """Mexican-origin attitude and institutional items, parsed from the norms lane table."""
    p = os.path.join(INFRA, "norms_gen_2026_09_18", "derived", "mex_synth_table.md")
    src = "infra/immigration-fiscal/norms_gen_2026_09_18/derived/mex_synth_table.md"
    out = []
    for ln in open(p, encoding="utf-8").read().splitlines():
        if not ln.startswith("|") or ln.startswith("| Item") or set(ln) <= set("|-: "):
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        item = cells[0]

        def val(c):
            m = re.match(r"([+-]?\d+\.?\d*)\s*\(([\d.]+)\)", c)
            return (float(m.group(1)), float(m.group(2))) if m else (None, None)

        (g1, se1), (g2, _), (g3, _) = val(cells[1]), val(cells[2]), val(cells[3])
        if None in (g1, g2, g3) or 0.0 in (g1, g2, g3):
            continue
        # An outcome with no measured first-generation deviation has nothing to
        # assimilate: its implied a is noise, not a slow rate. Flag, do not drop.
        usable = abs(g1) >= 1.96 * se1
        note = "Mexican-origin only; adjusted for age, education, income, year (ladder 135)"
        if "Obedience" in item:
            note += "; ladder 135: interviewer mode inflates the G1 gap by roughly 20 points"
        out.append({
            "domain": "norms", "outcome": item, "units": "pp" if "pp)" in item else "scale points",
            "g1": g1, "g2": g2, "g3": g3, "g1_se": se1, "usable": "yes" if usable else "no",
            "source": src, "tag": "SOURCE", "note": note,
        })
    return out


def ladder_outcomes():
    """Generalized trust: the ladder's own adjusted Hispanic-generation gaps."""
    lad = "research/immigration-confidence-ladder.md"
    path = os.path.join(REPO, lad)
    for i, ln in enumerate(open(path, encoding="utf-8").read().splitlines(), 1):
        if ln.startswith("110.") and "trust gaps remain" in ln:
            m = re.search(r"trust gaps remain[−-]?([\d.]+)/[−-]?([\d.]+)/[−-]?([\d.]+)pp", ln)
            if not m:
                raise SystemExit("ladder 110 trust triple not matched")
            g1, g2, g3 = (-float(x) for x in m.groups())
            return [{
                "domain": "norms", "outcome": "Generalized trust (GSS, adjusted)",
                "units": "pp", "g1": g1, "g2": g2, "g3": g3,
                "source": f"{lad}:{i}", "tag": "SOURCE",
                "note": "Hispanic generations, not Mexican-origin only; ladder 117 puts "
                        "adjusted G3+ minus G1 at +2.08pp [-2.36, 6.52], i.e. no measured convergence",
            }]
    raise SystemExit("ladder entry 110 not found")


# ------------------------------------------------------------------- tau


def tau_constructions(gamma_mex):
    """delta from the repo's conditional log-wage residuals, tau = delta/gamma."""
    import math
    acs = os.path.join(INFRA, "arrival_cohorts_2026_09_18", "derived", "acs_wage_residual_by_ysm_band.csv")
    ipu = os.path.join(INFRA, "arrival_cohorts_2026_09_18", "derived", "ipums_wage_residual_by_ysm_band.csv")
    src_a = "infra/immigration-fiscal/arrival_cohorts_2026_09_18/derived/acs_wage_residual_by_ysm_band.csv"
    src_i = "infra/immigration-fiscal/arrival_cohorts_2026_09_18/derived/ipums_wage_residual_by_ysm_band.csv"
    out = []

    # ACS: pool the two sex rows of a cohort x ysm cell by unweighted n
    rows = [r for r in read_csv(acs) if r["ysm_band"] == "0-5"]
    by = {}
    for r in rows:
        by.setdefault(r["cohort"], []).append(r)
    for cohort in sorted(by):
        rs = by[cohort]
        n = sum(int(r["n"]) for r in rs)
        resid = sum(int(r["n"]) * float(r["resid_lnw"]) for r in rs) / n
        ysm = sum(int(r["n"]) * float(r["mean_ysm"]) for r in rs) / n
        d = 1.0 - math.exp(resid)
        out.append({
            "construction": f"ACS 2023-24, arrivals {cohort}, 0-5 years since arrival",
            "mean_ysm": ysm, "n": n, "resid_lnw": resid, "delta": d,
            "gamma": gamma_mex, "tau": d / gamma_mex, "source": src_a,
            "tag": "CALCULATION",
            "note": "conditional on year x sex x age group x education, vs US-born NH white; "
                    "full-time full-year workers only",
        })

    # IPUMS census panel: total income, all-sex, no sex control
    for r in read_csv(ipu):
        if r["ysm_band"] != "0-5":
            continue
        resid = float(r["resid_lninc"])
        d = 1.0 - math.exp(resid)
        out.append({
            "construction": f"IPUMS census/ACS {r['years']}, arrivals {r['cohort']}, 0-5 years since arrival",
            "mean_ysm": float("nan"), "n": int(r["n"]), "resid_lnw": resid, "delta": d,
            "gamma": gamma_mex, "tau": d / gamma_mex, "source": src_i,
            "tag": "CALCULATION",
            "note": "total income, all-sex (panel has no SEX/INCWAGE, ladder 133); "
                    "conditional on age and education vs US-born NH white",
        })
    out.sort(key=lambda r: r["construction"])
    return out


# ------------------------------------------------------------------- main


def main():
    with open(os.path.join(OUT, "paper_table1.csv"), encoding="utf-8") as fh:
        gamma_mex = next(float(r["gamma_country"]) for r in csv.DictReader(fh)
                         if r["country"] == "Mexico")

    outs = (memo_outcomes() + cps_gap_outcomes() + ledger_outcomes()
            + norms_outcomes() + ladder_outcomes())

    for o in outs:
        o.setdefault("usable", "yes")
        o.setdefault("g1_se", float("nan"))
        o["a_g1_g2"] = M.gen_rate(o["g1"], o["g2"], GEN_YEARS)
        o["a_g2_g3"] = M.gen_rate(o["g2"], o["g3"], GEN_YEARS)
        o["a_g1_g3"] = M.gen_rate(o["g1"], o["g3"], 2 * GEN_YEARS)
        o["a_g1_g3_gen25"] = M.gen_rate(o["g1"], o["g3"], 2 * GEN_YEARS_SENS[0])
        o["a_g1_g3_gen33"] = M.gen_rate(o["g1"], o["g3"], 2 * GEN_YEARS_SENS[1])
    outs.sort(key=lambda o: (o["domain"], o["outcome"]))

    cols = ["domain", "outcome", "units", "usable", "g1", "g1_se", "g2", "g3",
            "a_g1_g2", "a_g2_g3", "a_g1_g3", "a_g1_g3_gen25", "a_g1_g3_gen33",
            "tag", "source", "note"]
    with open(os.path.join(OUT, "parameters.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for o in outs:
            w.writerow([o[c] if c in ("domain", "outcome", "units", "usable", "tag", "source", "note")
                        else M.f(o[c], 6) for c in cols])

    taus = tau_constructions(gamma_mex)
    tcols = ["construction", "n", "mean_ysm", "resid_lnw", "delta", "gamma", "tau",
             "tag", "source", "note"]
    with open(os.path.join(OUT, "tau_repo.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(tcols)
        for t in taus:
            w.writerow([t[c] if c in ("construction", "tag", "source", "note", "n")
                        else M.f(t[c], 6) for c in tcols])

    with open(os.path.join(OUT, "inputs_provenance.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["quantity", "value", "tag", "source"])
        w.writerow(["generation_length_years", M.f(GEN_YEARS, 1), "INFERENCE",
                    "lane brief stipulation; sensitivity at 25 and 33 in parameters.csv"])
        w.writerow(["gamma_mexico", M.f(gamma_mex, 6), "SOURCE", GAMMA_MEXICO_SOURCE])

    print(f"outcomes {len(outs)}  tau constructions {len(taus)}")
    a13 = sorted(o["a_g1_g3"] for o in outs if o["usable"] == "yes")
    print(f"usable outcomes {sum(1 for o in outs if o['usable']=='yes')}")
    print(f"a(G1->G3+, 29y generations) range {M.f(a13[0],5)} .. {M.f(a13[-1],5)}")
    tv = sorted(t["tau"] for t in taus)
    print(f"tau range {M.f(tv[0],4)} .. {M.f(tv[-1],4)}")


if __name__ == "__main__":
    main()
