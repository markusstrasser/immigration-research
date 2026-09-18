"""Format derived/estimates.csv into the markdown tables the memo carries."""
import pathlib
import pandas as pd

D = pathlib.Path(__file__).parent / "derived"


def fmt(r):
    return f"{r.coef:+.3f} [{r.ci_lo:+.3f}, {r.ci_hi:+.3f}]"


def block(df, title, cols=("estimator", "n_metro", "coef", "ci", "first_stage_F",
                           "shea_partial_r2", "corr_Zm_Zmlag")):
    out = [f"\n**{title}**\n"]
    d = df.copy()
    d["ci"] = d.apply(lambda r: f"[{r.ci_lo:+.2f}, {r.ci_hi:+.2f}]", axis=1)
    d["coef"] = d["coef"].map(lambda v: f"{v:+.3f}")
    for c in ("first_stage_F", "shea_partial_r2", "corr_Zm_Zmlag"):
        if c in d:
            d[c] = d[c].map(lambda v: "" if pd.isna(v) else f"{v:.3g}")
        else:
            d[c] = ""
    use = [c for c in cols if c in d.columns]
    hdr = {"estimator": "estimator", "n_metro": "metros", "coef": "coef (pp)",
           "ci": "95% CI", "first_stage_F": "1st-stage F",
           "shea_partial_r2": "Shea partial R2", "corr_Zm_Zmlag": "corr(Z, Z lag)"}
    out.append("| " + " | ".join(hdr[c] for c in use) + " |")
    out.append("|" + "|".join("---" for _ in use) + "|")
    for _, r in d.iterrows():
        out.append("| " + " | ".join(str(r[c]) for c in use) + " |")
    return "\n".join(out)


def national_shifts():
    """The 'shift' half of the shift-share, per window. A window in which the national stock
    barely moves gives the conventional single-origin instrument almost nothing to work with."""
    ns = pd.read_csv(D / "national_origin_stock.csv")
    piv = ns.pivot(index="year", columns="origin", values="natl_stock")
    mex = piv["mexico"] if "mexico" in piv.columns else None
    tot = piv.sum(axis=1)
    wins = [(2005, 2010), (2008, 2013), (2010, 2015), (2013, 2018), (2018, 2023),
            (2005, 2015), (2008, 2018), (2013, 2023)]
    rows = []
    for a, b in wins:
        if a in piv.index and b in piv.index:
            rows.append(dict(window=f"{a}-{b}",
                             mex_change_m=round((mex[b] - mex[a]) / 1e6, 3) if mex is not None else None,
                             all_matched_change_m=round((tot[b] - tot[a]) / 1e6, 3)))
    d = pd.DataFrame(rows)
    out = ["\n**National stock change over each window, millions of people**\n",
           "| window | Mexico-born | all matched origins |", "|---|---:|---:|"]
    for _, r in d.iterrows():
        out.append(f"| {r.window} | {r.mex_change_m:+.2f} | {r.all_matched_change_m:+.2f} |")
    return "\n".join(out)


def main():
    df = pd.read_csv(D / "estimates.csv")
    main_ = df[df.min_pop == 50_000]
    parts = [national_shifts()]

    parts.append("### Headline: pooled across 5-year windows, both sexes, ages 18–29\n")
    for tname in ("Mexico-born", "all foreign-born"):
        for oname in ("E/POP 18-29", "LFP 18-29"):
            d = main_[(main_.treatment == tname) & (main_.sex == "both")
                      & (main_.outcome == oname) & (main_.window == "POOLED")
                      & (main_.length == "5y")]
            if len(d):
                parts.append(block(d, f"{oname}, treatment = {tname}, pooled 5-year windows"))

    parts.append("\n### By sex, pooled 5-year windows, E/POP 18–29\n")
    for sname in ("men", "women"):
        d = main_[(main_.treatment == "Mexico-born") & (main_.sex == sname)
                  & (main_.outcome == "E/POP 18-29") & (main_.window == "POOLED")
                  & (main_.length == "5y")]
        if len(d):
            parts.append(block(d, f"E/POP 18-29, {sname}, Mexico-born treatment"))

    parts.append("\n### Pooled 16–24 arm and 10-year windows\n")
    for oname, wl in (("E/POP 16-24", "5y"), ("E/POP 18-29", "10y")):
        d = main_[(main_.treatment == "Mexico-born") & (main_.sex == "both")
                  & (main_.outcome == oname) & (main_.window == "POOLED")
                  & (main_.length == wl)]
        if len(d):
            parts.append(block(d, f"{oname}, {wl} windows, Mexico-born treatment"))

    parts.append("\n### Window by window, E/POP 18–29, both sexes, Mexico-born treatment\n")
    d = main_[(main_.treatment == "Mexico-born") & (main_.sex == "both")
              & (main_.outcome == "E/POP 18-29") & (main_.window != "POOLED")
              & (main_.length == "5y")]
    for w in sorted(d.window.unique()):
        parts.append(block(d[d.window == w], f"window {w}"))

    txt = "\n".join(parts)
    (D / "tables.md").write_text(txt)
    print(txt)


if __name__ == "__main__":
    main()
