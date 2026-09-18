"""Format the estimate files into the memo's §3 tables (_parts/30_estimates.md)."""
import pathlib
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).parent
D = HERE / "derived"
OUT = HERE / "_parts" / "30_estimates.md"


def fmt(c, s):
    if pd.isna(c):
        return "—"
    star = "***" if abs(c / s) > 2.58 else "**" if abs(c / s) > 1.96 else \
           "*" if abs(c / s) > 1.645 else ""
    return f"{c:+.3f}{star} ({s:.3f})"


def tbl(df, rows, cols, rowname, colname, label):
    out = [f"**{label}**", "", "| " + rowname + " | " + " | ".join(cols) + " |",
           "|" + "---|" * (len(cols) + 1)]
    for r in rows:
        cells = []
        for c in cols:
            m = df[(df[rowname] == r) & (df[colname] == c)]
            cells.append(fmt(float(m.coef.iloc[0]), float(m.se.iloc[0])) if len(m) else "—")
        out.append(f"| {r} | " + " | ".join(cells) + " |")
    out.append("")
    return out


def main():
    L = ["---", "", "## 3. Estimates", "",
         "Coefficients with standard errors in parentheses. "
         "`*` p<0.10, `**` p<0.05, `***` p<0.01. "
         "Metro regressions are weighted by the base-year enrolment of the group in the "
         "outcome and use HC1 or metro-clustered standard errors; district regressions are "
         "weighted by enrolment and clustered on the district.", ""]

    # ---- design (a)
    try:
        f = pd.read_csv(D / "estimates_flight.csv")
    except FileNotFoundError:
        f = None
    if f is not None and len(f):
        long_spec = sorted(s for s in f.spec.unique() if s.startswith("long "))[0]
        window = long_spec.split()[-1]
        L += [f"### 3.1 Metro panel: does the native private share rise with the Hispanic share?",
              "",
              f"Long differences are over {window}. A coefficient of 0.10 means that a "
              "10-point rise in the Hispanic share of enrolled children raises the private "
              "share of US-born non-Hispanic white children by 1 point.", ""]
        sub = f[f.spec == long_spec]
        L += tbl(sub, ["elem", "sec", "all"], ["d hisp_share", "d fb_share"],
                 "level", "treatment",
                 f"Long difference {window}, outcome = change in private share of US-born "
                 "non-Hispanic white children")
        hr = f[f.spec.str.startswith("horse-race ")]
        L += tbl(hr, ["elem", "sec", "all"],
                 ["d hisp_share", "d asian_share", "d black_share"], "level", "treatment",
                 "Horse race: is the response specific to the Hispanic share? "
                 "(all three entered together)")
        gs = f[f.spec.str.startswith("generation split")]
        L += tbl(gs, ["elem", "sec", "all"],
                 ["d hisp foreign-born share", "d hisp US-born share"], "level", "treatment",
                 "Generation split: first-generation (largely English-learner) vs "
                 "second-generation Hispanic children")
        bg = f[f.spec.str.startswith("by group")]
        if len(bg):
            L += ["**Is the response white-specific?**", "",
                  "| level | all US-born non-Hispanic | US-born Hispanic |",
                  "|---|---|---|"]
            for lv in ("elem", "sec", "all"):
                cells = []
                for oc in ("d priv share (all US-born non-Hispanic)",
                           "d priv share (US-born Hispanic)"):
                    m = bg[(bg.level == lv) & (bg.outcome == oc)]
                    cells.append(fmt(float(m.coef.iloc[0]), float(m.se.iloc[0]))
                                 if len(m) else "—")
                L.append(f"| {lv} | " + " | ".join(cells) + " |")
            L.append("")
        fe = f[f.spec == "two-way FE"]
        L += tbl(fe, ["elem", "sec", "all"], ["hisp_share", "fb_share"], "level",
                 "treatment", "Two-way fixed effects (metro and year), levels not differences")
        iv = f[f.spec.str.startswith("IV ")]
        if len(iv):
            L += ["**2SLS on the 2000-base shift-share instrument**", "",
                  "| level | instrument | coefficient (SE) | first-stage F | n |",
                  "|---|---|---|---|---|"]
            for _, r in iv.iterrows():
                L.append(f"| {r.level} | {r.estimator} | {fmt(r.coef, r.se)} | "
                         f"{r.first_stage_F:.1f} | {int(r.n)} |")
            L += ["", "The instrument's first-stage strength is reported so that weak-"
                  "instrument estimates can be discounted rather than quoted.", ""]
        pl = f[f.spec.str.startswith("placebo")]
        if len(pl):
            L += ["**Reverse-timing placebo.** The early change in the private share is "
                  "regressed on the *later* change in the Hispanic share. A non-zero "
                  "coefficient means the association is a pre-trend, not a response.", "",
                  "| level | coefficient (SE) | n |", "|---|---|---|"]
            for _, r in pl.iterrows():
                L.append(f"| {r.level} | {fmt(r.coef, r.se)} | {int(r.n)} |")
            L.append("")
        inf = f[f.spec.str.startswith("influence")]
        if len(inf):
            L += ["**Influence checks, secondary level**", "",
                  "| sample | coefficient on Δ Hispanic share (SE) | n |", "|---|---|---|"]
            for _, r in inf.iterrows():
                L.append(f"| {r.spec.replace('influence: ', '')} | {fmt(r.coef, r.se)} | "
                         f"{int(r.n)} |")
            L.append("")
        cn = f[f.spec == f"counts {window}"]
        cg = f[f.spec == f"counts, growth controlled {window}"]
        if len(cn):
            L += ["**Counts, the specification comparable to Betts & Fairlie's ratio.** "
                  "Both sides are expressed per 100 children enrolled in the base year, "
                  "so the coefficient is the number of US-born non-Hispanic white children "
                  "moved into private school per additional child in the public schools. "
                  "The second row of each pair adds the metro's total enrolment growth as "
                  "a control, because a growing metro adds Hispanic public pupils and "
                  "white private pupils at the same time.", "",
                  "| level | control | per Hispanic child added | per foreign-born child "
                  "added | n |", "|---|---|---|---|---|"]
            for lv in ("elem", "sec", "all"):
                for src, lab in ((cn, "none"), (cg, "+ total enrolment growth")):
                    cells = []
                    for tr in ("d hispanic public enrol (per 100 base)",
                               "d foreign-born public enrol (per 100 base)"):
                        m = src[(src.level == lv) & (src.treatment == tr)]
                        cells.append(fmt(float(m.coef.iloc[0]), float(m.se.iloc[0]))
                                     if len(m) else "—")
                    sub = src[src.level == lv]
                    n = int(sub.n.iloc[0]) if len(sub) else 0
                    L.append(f"| {lv} | {lab} | " + " | ".join(cells) + f" | {n} |")
            L.append("")

    # ---- design (b)
    try:
        d = pd.read_csv(D / "estimates_districts.csv")
    except FileNotFoundError:
        d = None
    if d is not None and len(d):
        L += ["### 3.2 District finance: does spending or local tax effort fall?", "",
              "Outcomes are per pupil in 2020 dollars unless the name says otherwise. "
              "A coefficient of 1,000 on `hisp_share` means that moving a district from "
              "0% to 100% Hispanic raises the outcome by $1,000 per pupil, so a 10-point "
              "rise is worth $100.", ""]
        outs = ["pp_current", "pp_instruction", "pp_rev_local", "pp_rev_proptax",
                "pp_rev_state", "pp_rev_total", "local_effort", "proptax_effort"]
        for spec in ("A district+year FE", "B district+state-year FE"):
            sub = d[(d.spec == spec) & (d.treatment == "hisp_share")]
            if not len(sub):
                continue
            L += [f"**{spec}, treatment = Hispanic share of enrolment**", "",
                  "| outcome | coefficient (SE) | n |", "|---|---|---|"]
            for o in outs:
                m = sub[sub.outcome == o]
                if len(m):
                    L.append(f"| {o} | {fmt(float(m.coef.iloc[0]), float(m.se.iloc[0]))} "
                             f"| {int(m.n.iloc[0]):,} |")
            L.append("")
        pot = d[d.spec.str.startswith("C + elderly")]
        if len(pot):
            L += tbl(pot, ["pp_current", "pp_rev_local", "pp_rev_proptax"],
                     ["hisp_share", "share65_c", "hisp_x_65"], "outcome", "treatment",
                     "Poterba-style: county elderly share (centred on its mean) and its "
                     "interaction with the Hispanic share, district and state-year fixed "
                     "effects. The Hispanic-share coefficient is therefore the effect at "
                     "the average elderly share.")
        elf = d[d.spec.str.startswith("B-elf")]
        if len(elf):
            L += tbl(elf, ["pp_current", "pp_rev_local"], ["elf"], "outcome", "treatment",
                     "Ethnic fractionalisation index instead of the Hispanic share")
        for sp in sorted(s for s in d.spec.unique() if s.startswith("E")):
            ld = d[d.spec == sp]
            L += tbl(ld, ["d_" + o for o in outs[:6]],
                     [c for c in ("d_hisp_share", "d_hisp_early") if c in set(ld.treatment)],
                     "outcome", "treatment",
                     f"Long difference: {sp.replace('E long diff ', '').replace('E2 long diff ', '')}")
        for sp in sorted(s for s in d.spec.unique() if s.startswith("F placebo")):
            pl = d[d.spec == sp]
            L += tbl(pl, sorted(pl.outcome.unique()), ["d_hisp_late"], "outcome",
                     "treatment",
                     "Reverse-timing placebo. The EARLY change in the outcome is "
                     "regressed on the LATER change in the Hispanic share; a non-zero "
                     "coefficient means the association is a pre-trend, not a response. "
                     f"({sp.replace('F placebo: ', '')})")

    # ---- bonds
    try:
        b = pd.read_csv(D / "estimates_bonds.csv")
    except FileNotFoundError:
        b = None
    if b is not None and len(b):
        L += ["### 3.3 California school bond and parcel-tax measures", "",
              "| specification | treatment | coefficient (SE) | n |", "|---|---|---|---|"]
        for _, r in b.iterrows():
            L.append(f"| {r.spec} | {r.treatment} | {fmt(r.coef, r.se)} | {int(r.n):,} |")
        L.append("")

    # ---- size
    try:
        s = pd.read_csv(D / "size_estimates.csv")
    except FileNotFoundError:
        s = None
    if s is not None and len(s):
        L += ["### 3.4 Size: what the coefficient implies in head counts and dollars", "",
              "Mechanical projection of the long-difference coefficient onto the observed "
              "Hispanic-share change. These are **not** measured head counts, and the 95% "
              "interval is carried through so the width is visible.", "",
              "| level | region | Δ Hispanic share | natives moved (point) | 95% interval | "
              "tuition, $m | state aid shifted, $m |", "|---|---|---|---|---|---|---|"]
        for (lv, reg), g in s.groupby(["level", "region"], sort=False):
            pt = g[g.bound == "point"].iloc[0]
            lo = g[g.bound == "lo95"].iloc[0]
            hi = g[g.bound == "hi95"].iloc[0]
            L.append(f"| {lv} | {reg} | {pt.d_hisp_share:+.3f} | "
                     f"{pt.implied_natives_moved:,.0f} | "
                     f"{lo.implied_natives_moved:,.0f} to {hi.implied_natives_moved:,.0f} | "
                     f"{pt.implied_tuition_spend_musd:,.0f} | "
                     f"{pt.implied_state_aid_shifted_musd:,.0f} |")
        L.append("")

    OUT.write_text("\n".join(L) + "\n")
    print(f"wrote {OUT} ({len(L)} lines)")


if __name__ == "__main__":
    main()
