"""Germany PISA 2012-2022: shift-share decomposition by immigrant background, and the cross-country test.

Inputs: derived/pisa2022_annex_long.csv (parse_tables.py over OECD PISA 2022 Vol I annex StatLinks
qmuad8 = Tables I.B1.7.x, https://stat.link/qmuad8). Outputs: derived/germany_inputs.csv,
derived/germany_decomposition.csv, derived/crosscountry.csv, derived/crosscountry_slopes.csv,
reads/oecd_tables_germany.md (verbatim cells).
"""
import csv, math
from collections import defaultdict
import numpy as np

ROWS = list(csv.DictReader(open("derived/pisa2022_annex_long.csv")))
IDX = defaultdict(dict)
for r in ROWS:
    IDX[(r["table"], r["country"])][r["column"]] = r["value"]
SECTION = {r["country"]: r["section"] for r in ROWS if r["table"] == "Table I.B1.7.20"}
GROUPS = {"all": "All students", "nat": "Non-immigrant students", "imm": "All immigrant students",
          "g2": "Second-generation immigrant students", "g1": "First-generation immigrant students"}
READS = []


def cell(table, country, tokens, unit):
    """Value of the unique column whose path contains every token (in order) and ends with unit."""
    d = IDX[(table, country)]
    hits = [c for c in d if c.split(" / ")[-1] == unit and all(t in c for t in tokens)
            and _ordered(c, tokens)]
    if "Non-immigrant students" not in tokens and "All students" not in tokens:
        hits = [c for c in hits if "Non-immigrant" not in c.split(" / ")[-2]]
    if len(hits) != 1:
        raise KeyError((table, country, tokens, unit, hits))
    v = d[hits[0]]
    if country == "Germany":
        READS.append((table, hits[0], v))
    try:
        return float(v)
    except ValueError:
        return float("nan")


def _ordered(c, tokens):
    pos = -1
    for t in tokens:
        p = c.find(t, pos + 1)
        if p < 0:
            return False
        pos = p
    return True


SUBJ = {"math": ("I.B1.7.17", "I.B1.7.18", "I.B1.7.19", "I.B1.7.20", "mathematics"),
        "reading": ("I.B1.7.21", "I.B1.7.22", "I.B1.7.23", "I.B1.7.24", "reading"),
        "science": ("I.B1.7.25", "I.B1.7.26", "I.B1.7.27", "I.B1.7.28", "science")}


def share(country, cyc, g):
    if cyc == 2022:
        return cell("Table I.B1.7.1", country, ["PISA 2022", GROUPS[g]], "%") / 100
    return cell("Table I.B1.7.2", country, [f"PISA {cyc}", GROUPS[g]], "%") / 100


def share_se(country, cyc, g):
    if cyc == 2022:
        return cell("Table I.B1.7.1", country, ["PISA 2022", GROUPS[g]], "S.E.") / 100
    return cell("Table I.B1.7.2", country, [f"PISA {cyc}", GROUPS[g]], "S.E.") / 100


def mean(country, subj, cyc, g, unit="Mean score"):
    t22, told = SUBJ[subj][0], SUBJ[subj][1]
    if cyc == 2022:
        return cell(f"Table {t22}", country, [GROUPS[g]], unit)
    return cell(f"Table {told}", country, [f"PISA {cyc}", GROUPS[g]], unit)


def change(country, subj, c0, g, unit="Score dif."):
    t1822, t1222 = SUBJ[subj][2], SUBJ[subj][3]
    if c0 == 2018:
        return cell(f"Table {t1822}", country, [GROUPS[g]], unit)
    return cell(f"Table {t1222}", country, [f"between PISA {c0} and PISA 2022", GROUPS[g]], unit)


def gap(country, subj, cyc, unit="Score dif."):
    t22, told = SUBJ[subj][0], SUBJ[subj][1]
    tok = ["Difference between immigrant and non-immigrant students"]
    if cyc == 2022:
        return cell(f"Table {t22}", country, tok, unit)
    return cell(f"Table {told}", country, [f"PISA {cyc}"] + tok, unit)


def shift_share(s0, s1, m0, m1):
    """Return dict of within/composition under weighting A (base shares, end means) and B (end shares, base means)."""
    wA = sum(s0[g] * (m1[g] - m0[g]) for g in s0); cA = sum((s1[g] - s0[g]) * m1[g] for g in s0)
    wB = sum(s1[g] * (m1[g] - m0[g]) for g in s0); cB = sum((s1[g] - s0[g]) * m0[g] for g in s0)
    return wA, cA, wB, cB


def germany():
    C, cycles = "Germany", [2012, 2015, 2018, 2022]
    inputs, dec = [], []
    for subj in SUBJ:
        S = {c: {g: share(C, c, g) for g in ("nat", "imm", "g2", "g1")} for c in cycles}
        M = {c: {g: mean(C, subj, c, g) for g in GROUPS} for c in cycles}
        for c in cycles:
            valid = S[c]["nat"] * M[c]["nat"] + S[c]["g2"] * M[c]["g2"] + S[c]["g1"] * M[c]["g1"]
            valid2 = S[c]["nat"] * M[c]["nat"] + S[c]["imm"] * M[c]["imm"]
            inputs.append(dict(subject=subj, cycle=c, **{f"share_{g}": round(S[c][g], 4) for g in S[c]},
                               **{f"mean_{g}": round(M[c][g], 2) for g in M[c]},
                               **{f"se_{g}": round(mean(C, subj, c, g, "S.E."), 2) for g in M[c]},
                               valid_mean_3grp=round(valid, 2), valid_mean_2grp=round(valid2, 2),
                               missing_residual=round(M[c]["all"] - valid, 2)))
        for c0, c1 in [(2012, 2022), (2015, 2022), (2018, 2022), (2012, 2018), (2015, 2018), (2012, 2015)]:
            tot_all = M[c1]["all"] - M[c0]["all"]
            for label, gs in (("2grp", ("nat", "imm")), ("3grp", ("nat", "g2", "g1"))):
                s0 = {g: S[c0][g] for g in gs}; s1 = {g: S[c1][g] for g in gs}
                m0 = {g: M[c0][g] for g in gs}; m1 = {g: M[c1][g] for g in gs}
                wA, cA, wB, cB = shift_share(s0, s1, m0, m1)
                tot_valid = wA + cA
                # delta-method SE of the 2-group composition term: ds * gap
                ds = S[c1]["imm"] - S[c0]["imm"]
                if c1 == 2022 and label == "2grp":
                    ds_se = (cell("Table I.B1.7.3", C, [GROUPS["imm"]], "S.E.") if c0 == 2018 else
                             cell("Table I.B1.7.4", C, [f"between PISA {c0} and PISA 2022", GROUPS["imm"]], "% dif.") and
                             cell("Table I.B1.7.4", C, [f"between PISA {c0} and PISA 2022", GROUPS["imm"]], "S.E.")) / 100
                else:
                    ds_se = math.hypot(share_se(C, c0, "imm"), share_se(C, c1, "imm"))
                g1_, g1se = gap(C, subj, c1), gap(C, subj, c1, "S.E.")
                seA = math.sqrt((g1_ * ds_se) ** 2 + (ds * g1se) ** 2) if label == "2grp" else float("nan")
                dec.append(dict(subject=subj, period=f"{c0}-{c1}", groups=label,
                                change_all_students=round(tot_all, 2), change_valid_status=round(tot_valid, 2),
                                within_A=round(wA, 2), composition_A=round(cA, 2),
                                within_B=round(wB, 2), composition_B=round(cB, 2),
                                comp_share_A=round(cA / tot_valid, 3), comp_share_B=round(cB / tot_valid, 3),
                                composition_A_se=round(seA, 2) if not math.isnan(seA) else "",
                                native_change=round(M[c1]["nat"] - M[c0]["nat"], 2),
                                native_share_of_all_change=round((M[c1]["nat"] - M[c0]["nat"]) / tot_all, 3)))
    return inputs, dec


def ols(y, X, w=None):
    X = np.column_stack([np.ones(len(y)), X]); y = np.asarray(y, float)
    W = np.ones(len(y)) if w is None else np.asarray(w, float)
    XtW = X.T * W
    XtWX_inv = np.linalg.inv(XtW @ X)
    b = XtWX_inv @ (XtW @ y)
    e = y - X @ b
    n, k = X.shape
    meat = (X.T * (W * e) ** 2) @ X
    V = XtWX_inv @ meat @ XtWX_inv * n / (n - k)  # HC1
    yb = np.average(y, weights=W)
    r2 = 1 - np.sum(W * e ** 2) / np.sum(W * (y - yb) ** 2)
    H = X @ XtWX_inv @ XtW  # hat matrix (weighted)
    h = np.diag(H)
    s2 = np.sum(W * e ** 2) / (n - k)
    cook = (W * e ** 2 / (k * s2)) * h / (1 - h) ** 2
    return b, np.sqrt(np.diag(V)), r2, e, cook


def crosscountry():
    rows = []
    for (t, c), d in IDX.items():
        if t != "Table I.B1.7.20" or c.startswith(("OECD", "EU", "Partners")):
            continue
        r = dict(country=c, section=SECTION.get(c))
        try:
            r["share_imm_2012"] = share(c, 2012, "imm") * 100; r["share_imm_2018"] = share(c, 2018, "imm") * 100
            r["share_imm_2022"] = share(c, 2022, "imm") * 100
            r["dshare_12_22"] = cell("Table I.B1.7.4", c, ["between PISA 2012 and PISA 2022", GROUPS["imm"]], "% dif.")
            r["dshare1_12_22"] = cell("Table I.B1.7.4", c, ["between PISA 2012 and PISA 2022", GROUPS["g1"]], "% dif.")
            r["dshare_18_22"] = cell("Table I.B1.7.3", c, [GROUPS["imm"]], "% dif.")
            r["dshare_12_18"] = r["share_imm_2018"] - r["share_imm_2012"]
        except KeyError:
            continue
        for s in SUBJ:
            try:
                r[f"nat_{s}_2012"] = mean(c, s, 2012, "nat")
                r[f"dnat_{s}_12_22"] = change(c, s, 2012, "nat"); r[f"dnat_{s}_12_22_se"] = change(c, s, 2012, "nat", "S.E.")
                r[f"dnat_{s}_18_22"] = change(c, s, 2018, "nat"); r[f"dnat_{s}_18_22_se"] = change(c, s, 2018, "nat", "S.E.")
                r[f"dnat_{s}_12_18"] = mean(c, s, 2018, "nat") - r[f"nat_{s}_2012"]
                r[f"dall_{s}_12_22"] = change(c, s, 2012, "all")
            except KeyError:
                pass
        rows.append(r)
    slopes = []
    for sample in ("OECD", "all"):
        for s in SUBJ:
            for per, xk, extra in (("12_22", "dshare_12_22", None), ("12_22", "dshare_12_22", "nat_2012"),
                                   ("12_22", "dshare1_12_22", None), ("12_18", "dshare_12_18", None),
                                   ("18_22", "dshare_18_22", None)):
                yk = f"dnat_{s}_{per}"
                use = [r for r in rows if (sample == "all" or r["section"] == "OECD")
                       and all(isinstance(r.get(k), float) and not math.isnan(r[k]) for k in
                               (yk, xk) + ((f"nat_{s}_2012",) if extra else ()))]
                y = [r[yk] for r in use]
                X = np.array([[r[xk]] + ([r[f"nat_{s}_2012"]] if extra else []) for r in use])
                b, se, r2, e, cook = ols(y, X)
                loo = []
                for i in range(len(use)):
                    keep = [j for j in range(len(use)) if j != i]
                    loo.append(ols([y[j] for j in keep], X[keep])[0][1])
                order = np.argsort(-np.abs(e))[:4]
                outl = "; ".join(f"{use[i]['country']} resid {e[i]:+.1f} (x={use[i][xk]:+.1f}, D={cook[i]:.2f})" for i in order)
                de = next((i for i, r in enumerate(use) if r["country"] == "Germany"), None)
                slopes.append(dict(sample=sample, subject=s, period=per, regressor=xk, control=extra or "",
                                   n=len(use), slope_per10pp=round(10 * b[1], 2), se_per10pp=round(10 * se[1], 2),
                                   t=round(b[1] / se[1], 2), intercept=round(b[0], 2), r2=round(r2, 3),
                                   loo_min_per10=round(10 * min(loo), 2), loo_max_per10=round(10 * max(loo), 2),
                                   germany_resid=round(e[de], 2) if de is not None else "",
                                   top_residuals=outl))
    return rows, slopes


def write(path, rows):
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, keys, lineterminator="\n"); w.writeheader(); w.writerows(rows)


if __name__ == "__main__":
    inputs, dec = germany()
    write("derived/germany_inputs.csv", inputs); write("derived/germany_decomposition.csv", dec)
    rows, slopes = crosscountry()
    write("derived/crosscountry.csv", rows); write("derived/crosscountry_slopes.csv", slopes)
    with open("reads/oecd_tables_germany.md", "w") as f:
        f.write("# OECD PISA 2022 Results Vol. I, annex B1 chapter 7 — Germany cells read by decompose.py\n\n")
        f.write("Source: OECD (2023), PISA 2022 Results (Volume I), doi:10.1787/53f23881-en; workbook "
                "https://stat.link/qmuad8 (fetched 2026-09-27 as https://stat.link/files/53f23881-en/qmuad8.xlsx). "
                "Each line: table | column path | cell value as stored. Shares are % of students with valid "
                "immigrant-status data; means are PISA scale points.\n\n")
        for t, c, v in dict.fromkeys(READS):
            f.write(f"- {t} | {c} | {v}\n")
    print("germany inputs:", len(inputs), "decomp rows:", len(dec), "countries:", len(rows), "slopes:", len(slopes))
