"""Part 3 (BRIEF_3.md, f437563): can any design see a national channel?

Test 1: the pre-pandemic window 2015->2018 around the 2015-16 asylum wave. Natives' change 2015->2018 (math,
reading, science) on the size of the wave: (a) first-time asylum applicants 2015+2016 as % of the 1 Jan 2015
population (Eurostat migr_asyappctza, applicant=FRST; demo_pjan), plus positive first-instance decisions 2015-2017
(migr_asydcfsta, decision=POS) as the measure of who stayed; (b) the change in PISA's first-generation share
2015->2018 (OECD 2022 Vol I Table I.B1.7.2). Natives' 2015 means from PISA 2015 Vol I Tables I.7.15a/b/c
(cross-checked against the 2022 Vol I trend columns); 2012 and 2018 from 2022 Vol I Tables I.B1.7.18/7.22/7.26.
Controls: natives' 2012->2015 change (pre-trend; it contains the 2015 switch to computer-based testing) and the 2015
level. Sweden is bounded for exclusion (P10: excluded pupils at the mean - 1.2816 SD, charged to natives).
Test 1b (lagged): the same wave against natives' 2018->2022 and 2015->2022 changes, with closure weeks added.
Test 2: minimum detectable effect at 80% power, two-sided 5%: MDE = 2.80 x SE.
Test 3: selection heterogeneity - the part-2 models without the settler countries (Australia, Canada, New Zealand),
the slope at Germany's immigrant-native gap (interaction), and the regional panel without Canada.
Outputs: derived/national_channel_{data,slopes,power}.csv, reads/national_channel_inputs.md.
"""
import csv, json, math
import numpy as np
import openpyxl
from decompose import mean, share, gap, change, write
from parse_tables import parse_sheet
import deconfound as dc

GEO = {"Austria": "AT", "Belgium": "BE", "Bulgaria": "BG", "Croatia": "HR", "Cyprus": "CY", "Czech Republic": "CZ",
       "Denmark": "DK", "Estonia": "EE", "Finland": "FI", "France": "FR", "Germany": "DE", "Greece": "EL",
       "Hungary": "HU", "Iceland": "IS", "Ireland": "IE", "Italy": "IT", "Latvia": "LV", "Lithuania": "LT",
       "Luxembourg": "LU", "Malta": "MT", "Netherlands": "NL", "Norway": "NO", "Poland": "PL", "Portugal": "PT",
       "Romania": "RO", "Slovak Republic": "SK", "Slovenia": "SI", "Spain": "ES", "Sweden": "SE", "Switzerland": "CH",
       "United Kingdom": "UK", "Montenegro": "ME"}
# subject -> (2022 Vol I SD-by-cycle table, 2015 Vol I natives table, 2015 Vol I label)
SUBJ = {"math": ("Table I.B1.5.10", "Table I.7.15c", "Mathematics"),
        "reading": ("Table I.B1.5.11", "Table I.7.15b", "Reading"),
        "science": ("Table I.B1.5.12", "Table I.7.15a", "Science")}
ALIAS15 = {"Turkey": "Türkiye", "Former Yugoslav Republic of Macedonia": "North Macedonia"}
SETTLER = {"Australia", "Canada", "New Zealand"}
# paper in 2015, computer in 2018 [INFERENCE from the two quoted lists in reads/national_channel_inputs.md]
MODE_SWITCH_15_18 = {"Albania", "Georgia", "Indonesia", "Kazakhstan", "Kosovo", "Malta"}
Z10 = 1.2816
clean = dc.clean


def eurostat(path):
    d = json.load(open(path))
    dims, size = d["id"], d["size"]
    cats = {k: d["dimension"][k]["category"]["index"] for k in dims}
    def get(**sel):
        idx = 0
        for k, n in zip(dims, size):
            if k in sel and sel[k] not in cats[k]:
                return None
            idx = idx * n + (cats[k][sel[k]] if k in sel else 0)
        return d["value"].get(str(idx))
    return get


def ols(y, X):
    """OLS with an intercept; returns b, HC1 covariance, residuals."""
    X = np.column_stack([np.ones(len(y)), X]); y = np.asarray(y, float)
    XtX_inv = np.linalg.inv(X.T @ X); b = XtX_inv @ X.T @ y; e = y - X @ b
    n, k = X.shape
    return b, XtX_inv @ ((X.T * e ** 2) @ X) @ XtX_inv * n / (n - k), e


def ok(r, k):
    return isinstance(r.get(k), float) and not math.isnan(r[k])


def fit(rows, y, xs, label, sample, test, scale, unit, show=("Germany", "Austria", "Sweden")):
    use = [r for r in rows if all(ok(r, k) for k in [y] + xs)]
    if len(use) < len(xs) + 3:
        return None
    X = np.array([[r[k] for k in xs] for r in use]); Y = [r[y] for r in use]
    b, V, e = ols(Y, X)
    loo = []
    for i in range(len(use)):
        keep = [j for j in range(len(use)) if j != i]
        loo.append((round(scale * ols([Y[j] for j in keep], X[keep])[0][1], 2), use[i]["country"]))
    se = math.sqrt(V[1, 1])
    res = dict(test=test, sample=sample, outcome=y, regressors="+".join(xs), label=label, n=len(use), unit=unit,
               slope=round(scale * b[1], 2), se=round(scale * se, 2), mde80=round(2.8 * scale * se, 2),
               r2=round(1 - float(np.sum(e ** 2) / np.sum((np.array(Y) - np.mean(Y)) ** 2)), 3),
               loo_min=f"{min(loo)[0]:.2f} (drop {min(loo)[1]})", loo_max=f"{max(loo)[0]:.2f} (drop {max(loo)[1]})")
    for i, k in enumerate(xs[1:], start=2):
        res[f"coef_{k.split('_')[0]}"] = round(float(b[i]), 3); res[f"se_{k.split('_')[0]}"] = round(math.sqrt(V[i, i]), 3)
    for c in show:
        i = next((i for i, r in enumerate(use) if r["country"] == c), None)
        res[f"resid_{c}"] = round(float(e[i]), 2) if i is not None else ""
    res["countries"] = ";".join(r["country"] for r in use)
    return res


def natives2015():
    wb = openpyxl.load_workbook("_cache/statlink_888933433226.xlsx", read_only=True, data_only=True)
    out = {}
    for s, (_, t, lab) in SUBJ.items():
        for n, _, c, v in parse_sheet(wb[t]):
            if c == f"{lab} performance in PISA 2015 / Non-immigrant students / Mean score" and isinstance(v, (int, float)):
                n = clean(n); out[(ALIAS15.get(n, n), s)] = float(v)
    return out


def build():
    cc = list(csv.DictReader(open("derived/crosscountry.csv")))
    asy = eurostat("_cache/eurostat_asy_first_2015_2016.json")
    pos = eurostat("_cache/eurostat_asy_decisions_pos_2015_2018.json")
    pop = eurostat("_cache/eurostat_pop_2015.json")
    ex = {(clean(r["country"]), int(r["cycle"])): float(r["overall_excl_rate_pct"])
          for r in csv.DictReader(open("derived/exclusion_coverage.csv")) if r["overall_excl_rate_pct"]}
    dc.natl.wb = openpyxl.load_workbook("_cache/statlink_wh9d4z.xlsx", read_only=True, data_only=True); dc.natl.cache = {}
    n15 = natives2015()
    closures = {clean(r["country"]): r["closure_total_wk"] for r in csv.DictReader(open("derived/deconfound_covariates.csv"))}
    rows, quotes, xcheck = [], [], []
    for x in cc:
        nm, c = x["country"], clean(x["country"])
        r = dict(country=c, section=x["section"], europe=int(c in dc.EUROPE), mode_switch_15_18=int(c in MODE_SWITCH_15_18))
        try:
            r["g1_2015"], r["g1_2018"] = 100 * share(nm, 2015, "g1"), 100 * share(nm, 2018, "g1")
            r["dg1_15_18"] = r["g1_2018"] - r["g1_2015"]
            r["dimm_15_18"] = 100 * (share(nm, 2018, "imm") - share(nm, 2015, "imm"))
        except KeyError:
            pass
        for s in SUBJ:
            try:
                m18 = mean(nm, s, 2018, "nat")
            except KeyError:
                continue
            try:
                m15_22 = mean(nm, s, 2015, "nat")
            except KeyError:
                m15_22 = float("nan")
            m15 = n15.get((c, s))
            if m15 is None and math.isnan(m15_22):
                continue
            if m15 is None:
                m15 = m15_22; r[f"src15_{s}"] = "2022 Vol I (not in 2015 Vol I I.7.15)"
            elif not math.isnan(m15_22):
                xcheck.append((c, s, m15, m15_22))
            r[f"nat_{s}_2015"] = m15
            try:
                r[f"pre_{s}_12_15"] = m15 - mean(nm, s, 2012, "nat")
            except KeyError:
                pass
            r[f"dnat_{s}_15_18_obs"] = m18 - m15
            if (c, 2015) in ex and (c, 2018) in ex:
                sd = {y: dc.natl(SUBJ[s][0], c, y, "Standard deviation / S.D.") for y in (2015, 2018)}
                corr = {y: -ex[(c, y)] / 100 * Z10 * sd[y] for y in (2015, 2018)}
                r[f"dnat_{s}_15_18_allbound"] = m18 - m15 + corr[2018] - corr[2015]
                if c == "Sweden":
                    r[f"sweden_bound_{s}"] = corr[2018] - corr[2015]
                    quotes.append(f"- Sweden {s}: exclusion {ex[(c, 2015)]} % (2015), {ex[(c, 2018)]} % (2018); SD "
                                  f"{sd[2015]:.2f} (2015), {sd[2018]:.2f} (2018) [Table {SUBJ[s][0][6:]}]; bound "
                                  f"{corr[2018] - corr[2015]:+.2f} points")
            # BRIEF_3: bounded Swedish values for 2018; other countries as observed
            r[f"dnat_{s}_15_18"] = r[f"dnat_{s}_15_18_obs"] + r.get(f"sweden_bound_{s}", 0.0)
            r[f"nat_{s}_2018"] = m18
            try:  # lagged window 2018->2022 (Table I.B1.7.19/7.23/7.27); Sweden's 2018 value bounded as above
                r[f"dnat_{s}_18_22_obs"] = change(nm, s, 2018, "nat")
                b18 = 0.0
                if (c, 2022) in ex and (c, 2018) in ex:
                    sd = {y: dc.natl(SUBJ[s][0], c, y, "Standard deviation / S.D.") for y in (2018, 2022)}
                    b18 = ex[(c, 2018)] / 100 * Z10 * sd[2018] - ex[(c, 2022)] / 100 * Z10 * sd[2022]
                    r[f"dnat_{s}_18_22_allbound"] = r[f"dnat_{s}_18_22_obs"] + b18
                r[f"dnat_{s}_18_22"] = r[f"dnat_{s}_18_22_obs"] + (b18 if c == "Sweden" else 0.0)
            except KeyError:
                pass
            try:
                r[f"dnat_{s}_12_22"] = change(nm, s, 2012, "nat"); r[f"dnat_{s}_15_22"] = change(nm, s, 2015, "nat")
                r[f"gap_{s}_2012"], r[f"gap_{s}_2015"] = gap(nm, s, 2012), gap(nm, s, 2015)
                r[f"gap_{s}_2022"] = gap(nm, s, 2022)
            except KeyError:
                pass
        try:
            r["dimm_12_22"] = 100 * (share(nm, 2022, "imm") - share(nm, 2012, "imm"))
            r["dimm_15_22"] = 100 * (share(nm, 2022, "imm") - share(nm, 2015, "imm"))
        except KeyError:
            pass
        cw = closures.get(c, "")
        if cw not in ("", None):
            r["closure_total_wk"] = float(cw)
        g = GEO.get(c)
        p15 = pop(geo=g, time="2015") if g else None
        if p15:
            a = {(ag, t): asy(geo=g, age=ag, time=t) for ag in ("TOTAL", "Y_LT18") for t in ("2015", "2016")}
            p = {(ag, t): pos(geo=g, age=ag, time=t) for ag in ("TOTAL", "Y_LT18") for t in ("2015", "2016", "2017")}
            if all(v is not None for v in a.values()):
                r["asy_1516_pct"] = 100 * (a[("TOTAL", "2015")] + a[("TOTAL", "2016")]) / p15
                r["asy_lt18_1516_pct"] = 100 * (a[("Y_LT18", "2015")] + a[("Y_LT18", "2016")]) / p15
            if all(v is not None for v in p.values()):
                r["pos_1517_pct"] = 100 * sum(p[("TOTAL", t)] for t in ("2015", "2016", "2017")) / p15
                r["pos_lt18_1517_pct"] = 100 * sum(p[("Y_LT18", t)] for t in ("2015", "2016", "2017")) / p15
            quotes.append(f"- {c} ({g}): population 1 Jan 2015 = {p15}; first-time applicants, all ages 2015 = "
                          f"{a[('TOTAL', '2015')]}, 2016 = {a[('TOTAL', '2016')]}; under 18: 2015 = {a[('Y_LT18', '2015')]}, "
                          f"2016 = {a[('Y_LT18', '2016')]}; positive first-instance decisions, all ages 2015/16/17 = "
                          f"{p[('TOTAL', '2015')]}/{p[('TOTAL', '2016')]}/{p[('TOTAL', '2017')]}; under 18 = "
                          f"{p[('Y_LT18', '2015')]}/{p[('Y_LT18', '2016')]}/{p[('Y_LT18', '2017')]}")
        rows.append(r)
    return rows, quotes, xcheck


def test1(rows):
    out = []
    eu = [r for r in rows if r["europe"] == 1]
    oecd = [r for r in rows if r["section"] == "OECD"]
    def run(rs, y, xs, lab, smp, scale, unit):
        x = fit(rs, y, xs, lab, smp, "P3-1 window 2015-18", scale, unit)
        if x: out.append(x)
    for s in SUBJ:
        y, ctl = f"dnat_{s}_15_18", [f"pre_{s}_12_15", f"nat_{s}_2015"]
        for smp, rs in (("Europe", eu), ("Europe excl. Hungary", [r for r in eu if r["country"] != "Hungary"])):
            for xk, lab in (("asy_1516_pct", "asylum applicants 2015-16"), ("asy_lt18_1516_pct", "asylum applicants <18")):
                run(rs, y, [xk], lab, smp, 1.0, "per 1% of population")
                run(rs, y, [xk] + ctl, lab + " + pre-trend + 2015 level", smp, 1.0, "per 1% of population")
        for xk, lab in (("pos_1517_pct", "positive decisions 2015-17"), ("pos_lt18_1517_pct", "positive decisions <18")):
            run(eu, y, [xk], lab, "Europe", 1.0, "per 1% of population")
            run(eu, y, [xk] + ctl, lab + " + pre-trend + 2015 level", "Europe", 1.0, "per 1% of population")
        for smp, rs in (("OECD", oecd), ("Europe", eu)):
            for xk, lab in (("dg1_15_18", "first-gen share change"), ("dimm_15_18", "immigrant share change")):
                run(rs, y, [xk], lab, smp, 10.0, "per 10 pp")
                run(rs, y, [xk] + ctl, lab + " + pre-trend + 2015 level", smp, 10.0, "per 10 pp")
        # sensitivity: pre-trend control dropped (it carries the 2012->2015 mode switch), exclusion, mode switchers
        run(eu, y, ["asy_1516_pct", f"nat_{s}_2015"], "asylum applicants 2015-16 + 2015 level only", "Europe", 1.0,
            "per 1% of population")
        run(eu, f"dnat_{s}_15_18_obs", ["asy_1516_pct"] + ctl, "asylum + controls, Sweden unbounded", "Europe", 1.0,
            "per 1% of population")
        run(eu, f"dnat_{s}_15_18_allbound", ["asy_1516_pct"] + ctl, "asylum + controls, all countries bounded (P10)",
            "Europe", 1.0, "per 1% of population")
        run([r for r in oecd + [q for q in eu if q["section"] != "OECD"] if not r["mode_switch_15_18"]], y,
            ["dg1_15_18"] + ctl, "first-gen + controls, OECD+Europe excl. 2015->18 mode switchers", "OECD+Europe",
            10.0, "per 10 pp")
    # lagged national channel: the same 2015-16 wave against natives' 2018->2022 and 2015->2022 changes
    def lag(rs, y, xs, lab):
        x = fit(rs, y, xs, lab, "Europe", "P3-1b lagged", 1.0, "per 1% of population")
        if x: out.append(x)
    for s in SUBJ:
        for xk, lab in (("asy_1516_pct", "asylum applicants 2015-16"), ("pos_1517_pct", "positive decisions 2015-17")):
            lag(eu, f"dnat_{s}_18_22", [xk], f"{lab}, 2018-22")
            lag(eu, f"dnat_{s}_18_22", [xk, f"dnat_{s}_15_18", f"nat_{s}_2018", "closure_total_wk"],
                f"{lab}, 2018-22 + 2015-18 change + 2018 level + closures")
            lag(eu, f"dnat_{s}_15_22", [xk], f"{lab}, 2015-22")
            lag(eu, f"dnat_{s}_15_22", [xk, f"pre_{s}_12_15", f"nat_{s}_2015", "closure_total_wk"],
                f"{lab}, 2015-22 + pre-trend + 2015 level + closures")
        lag(eu, f"dnat_{s}_18_22_allbound", ["asy_1516_pct", f"dnat_{s}_15_18", f"nat_{s}_2018", "closure_total_wk"],
            "asylum applicants 2015-16, 2018-22 + controls, all countries bounded (P10)")
    return out


def test3(rows):
    out = []
    cov = [dict({k: (float(v) if k not in ("country", "section") and v not in ("", None) else v) for k, v in r.items()},
                country=clean(r["country"])) for r in csv.DictReader(open("derived/deconfound_covariates.csv"))]
    specs = (("2012", "dnat_math_12_22", ["dshare_12_22"], "share only"),
             ("2012", "dnat_math_12_22", ["dshare_12_22", "nat_math_2012", "closure_total_wk", "dlog_gdppc_12_22",
                                          "dnat_escs_12_22"], "joint"),
             ("2015", "dnat_math_15_22", ["dshare_15_22"], "share only"),
             ("2015", "dnat_math_15_22", ["dshare_15_22", "nat_math_2015", "closure_total_wk", "dlog_gdppc_15_22",
                                          "dnat_escs_15_22"], "joint"))
    for base, y, xs, lab in specs:
        for smp, rs in (("OECD", [r for r in cov if r["section"] == "OECD"]),
                        ("OECD excl. AUS/CAN/NZL", [r for r in cov if r["section"] == "OECD" and r["country"] not in SETTLER])):
            x = fit(rs, y, xs, f"{base} base, {lab}", smp, "P3-3 selection", 10.0, "per 10 pp")
            if x: out.append(x)
    de = next(r for r in rows if r["country"] == "Germany")
    for base, yk, xk, gk in (("2012", "dnat_math_12_22", "dimm_12_22", "gap_math_2012"),
                             ("2015", "dnat_math_15_22", "dimm_15_22", "gap_math_2015")):
        for smp, rs in (("OECD", [r for r in rows if r["section"] == "OECD"]), ("Europe", [r for r in rows if r["europe"]])):
            use = [r for r in rs if all(ok(r, k) for k in (yk, xk, gk))]
            b, V, e = ols([r[yk] for r in use], np.array([[r[xk], r[gk], r[xk] * r[gk]] for r in use]))
            for at, gv in (("gap 0", 0.0), ("Germany's base-year gap", de[gk]), ("Germany's 2022 gap", de["gap_math_2022"])):
                w = np.array([0.0, 1.0, 0.0, gv]); sl, sse = float(w @ b), math.sqrt(float(w @ V @ w))
                out.append(dict(test="P3-3 selection", sample=smp, outcome=yk, regressors=f"{xk}+{gk}+{xk}x{gk}",
                                label=f"{base} base, interaction: slope at {at} ({gv:.1f})", n=len(use), unit="per 10 pp",
                                slope=round(10 * sl, 2), se=round(10 * sse, 2), mde80=round(28 * sse, 2),
                                coef_interaction=round(float(b[3]) * 10, 3), se_interaction=round(math.sqrt(V[3, 3]) * 10, 3)))
    reg = list(csv.DictReader(open("derived/regional_changes_math_2012_2022.csv")))
    allc = {r["country"] for r in reg}
    def fe(rs):
        ctry = sorted({r["country"] for r in rs if sum(q["country"] == r["country"] for q in rs) >= 2})
        rs = [r for r in rs if r["country"] in ctry]
        X = np.array([[float(r["dshare"])] + [float(r["country"] == k) for k in ctry[1:]] for r in rs])
        b, V, e = ols([float(r["dnat"]) for r in rs], X)
        return rs, ctry, b, V
    for lab, keep in (("country FE, all (part-2 replication)", lambda r: True),
                      ("country FE, excl. Canada", lambda r: r["country"] != "Canada"),
                      ("country FE, excl. Canada and Catalonia", lambda r: r["country"] != "Canada" and "Catal" not in r["region"]),
                      ("country FE, excl. Canada and Spain", lambda r: r["country"] not in ("Canada", "Spain")),
                      ("Spain only", lambda r: r["country"] == "Spain"),
                      ("Spain only, excl. Catalonia", lambda r: r["country"] == "Spain" and "Catal" not in r["region"])):
        rs, ctry, b, V = fe([r for r in reg if keep(r)])
        loo = sorted((round(10 * fe([q for q in rs if q is not r])[2][1], 2), r["region"]) for r in rs)
        out.append(dict(test="P3-3 selection", sample="regions, math 2012-2022", outcome="dnat_math", regressors="dshare",
                        label=lab, n=len(rs), unit="per 10 pp", slope=round(10 * b[1], 2),
                        se=round(10 * math.sqrt(V[1, 1]), 2), mde80=round(28 * math.sqrt(V[1, 1]), 2),
                        loo_min=f"{loo[0][0]:.2f} (drop {loo[0][1]})", loo_max=f"{loo[-1][0]:.2f} (drop {loo[-1][1]})",
                        countries=";".join(ctry)))
    assert allc  # regional input present
    return out


def power(rows, t1, t3):
    """Test 2: MDE and Germany's implied share of its native decline, per design."""
    de = next(r for r in rows if r["country"] == "Germany")
    p2 = list(csv.DictReader(open("derived/deconfound_slopes.csv")))
    exp = {"2012": (de["dimm_12_22"], de["dnat_math_12_22"]), "2015": (de["dimm_15_22"], de["dnat_math_15_22"])}
    out = []
    def add(design, sees, smp, slope, se, n, unit, x_de, x_lab, dec, dec_lab):
        k = 10.0 if unit == "per 10 pp" else 1.0
        pts = lambda v: v * x_de / k
        out.append(dict(design=design, sees_national_channel=sees, sample=smp, n=n, unit=unit, slope=slope, se=se,
                        mde80=round(2.8 * se, 2), germany_exposure=round(x_de, 3), exposure=x_lab,
                        germany_native_change=round(dec, 2), change_window=dec_lab,
                        mde80_share_of_decline=round(pts(2.8 * se) / abs(dec), 3),
                        point_share=round(-pts(slope) / abs(dec), 3),
                        ci95_share_lo=round(-pts(slope + 1.96 * se) / abs(dec), 3),
                        ci95_share_hi=round(-pts(slope - 1.96 * se) / abs(dec), 3)))
    def p2row(test, smp, y, lab):
        return next(r for r in p2 if r["test"] == test and r["sample"] == smp and r["outcome"] == y and r["label"] == lab)
    for smp in ("OECD", "Europe"):
        for base, y, lab in (("2012", "dnat_math_12_22", "share only"), ("2012", "dnat_math_12_22", "joint"),
                             ("2015", "dnat_math_15_22", "2015-22 share only"), ("2015", "dnat_math_15_22", "2015-22 joint")):
            r = p2row("1 covariates", smp, y, lab)
            x, d = exp[base]
            add(f"part 2 cross-country, {lab} ({base} base)", "yes", smp, float(r["slope_per10pp"]), float(r["se_per10pp"]),
                int(r["n"]), "per 10 pp", x, f"immigrant share change {base}-22 (pp)", d, f"{base}-22")
            if base == "2015":  # same model, set against the 2012->2022 decline
                add(f"part 2 cross-country, {lab} (2015 base, vs 2012-22 decline)", "yes", smp, float(r["slope_per10pp"]),
                    float(r["se_per10pp"]), int(r["n"]), "per 10 pp", x, "immigrant share change 2015-22 (pp)",
                    de["dnat_math_12_22"], "2012-22")
    r = p2row("3 regional", "math 2012-2022", "dnat_math", "country FE")
    add("part 2 regional panel, country FE", "no (country x cycle FE)", "regions", float(r["slope_per10pp"]),
        float(r["se_per10pp"]), int(r["n"]), "per 10 pp", exp["2012"][0], "immigrant share change 2012-22 (pp)",
        exp["2012"][1], "2012-22")
    for r in t3:
        if r["sample"].startswith("regions") and "excl." in r["label"]:
            add(f"regional panel, {r['label']}", "no (country x cycle FE)", "regions", r["slope"], r["se"], r["n"],
                "per 10 pp", exp["2012"][0], "immigrant share change 2012-22 (pp)", exp["2012"][1], "2012-22")
        if r["sample"] == "OECD excl. AUS/CAN/NZL":
            base = r["label"][:4]
            add(f"cross-country without settler countries, {r['label']}", "yes", r["sample"], r["slope"], r["se"], r["n"],
                "per 10 pp", exp[base][0], f"immigrant share change {base}-22 (pp)", exp[base][1], f"{base}-22")
    for r in t1:
        if r["outcome"] == "dnat_math_15_18" and r["label"].endswith("pre-trend + 2015 level") and \
                r["sample"] in ("Europe", "OECD") and r["regressors"].split("+")[0] in ("asy_1516_pct", "pos_1517_pct", "dg1_15_18"):
            xk = r["regressors"].split("+")[0]
            for dec, lab in ((de["dnat_math_15_18"], "2015-18"), (de["dnat_math_12_22"], "2012-22")):
                add(f"test 1 window, {r['label']}", "yes", r["sample"], r["slope"], r["se"], r["n"], r["unit"], de[xk],
                    xk, dec, lab)
        if r["test"] == "P3-1b lagged" and r["outcome"] in ("dnat_math_18_22", "dnat_math_15_22") and "closures" in r["label"]:
            xk = r["regressors"].split("+")[0]
            w = r["outcome"][-5:].replace("_", "-")
            for dec, lab in ((de[r["outcome"]], f"20{w[:2]}-{w[3:]}"), (de["dnat_math_12_22"], "2012-22")):
                add(f"lagged wave, {r['label']}", "yes", r["sample"], r["slope"], r["se"], r["n"], r["unit"], de[xk],
                    xk, dec, lab)
    return out


def main():
    rows, quotes, xcheck = build()
    for r in rows:
        for k, v in r.items():
            if isinstance(v, float):
                r[k] = round(v, 6)
    t1, t3 = test1(rows), test3(rows)
    pw = power(rows, t1, t3)
    write("derived/national_channel_data.csv", rows)
    write("derived/national_channel_slopes.csv", t1 + t3)
    write("derived/national_channel_power.csv", pw)
    dmax = max(abs(a - b) for _, _, a, b in xcheck)
    worst = max(xcheck, key=lambda t: abs(t[2] - t[3]))
    L = ["# Part-3 inputs, verbatim", "",
         "## Eurostat (retrieved 2026-09-28 via the dissemination API; JSON-stat in `_cache/`)", "",
         "- First-time asylum applicants: `migr_asyappctza?format=JSON&lang=EN&citizen=TOTAL&sex=T&applicant=FRST&age=TOTAL"
         "&age=Y_LT18&age=Y14-17&time=2015&time=2016&time=2017&unit=PER` -> `_cache/eurostat_asy_first_2015_2016.json`.",
         "- Positive first-instance decisions: `migr_asydcfsta?format=JSON&lang=EN&citizen=TOTAL&sex=T&decision=POS"
         "&age=TOTAL&age=Y_LT18&time=2015&time=2016&time=2017&time=2018&unit=PER` -> "
         "`_cache/eurostat_asy_decisions_pos_2015_2018.json` (label: \"First instance decisions on applications by type "
         "of decision, citizenship, age and sex - annual aggregated data\"; POS = \"Positive decision\").",
         "- Population on 1 January: `demo_pjan` (sex=T, age=TOTAL, time=2015) -> `_cache/eurostat_pop_2015.json`.", ""]
    L += quotes + ["", "## PISA natives' 2015 means: 2015 Vol I Tables I.7.15a/b/c vs the 2022 Vol I trend columns", "",
                   f"- {len(xcheck)} country-subject pairs matched; max absolute difference {dmax:.3f} points "
                   f"({worst[0]}, {worst[1]}: {worst[2]:.3f} vs {worst[3]:.3f}).",
                   "- Germany (2015 Vol I, `statlink_888933433226.xlsx`): \"Mathematics performance in PISA 2015 / "
                   "Non-immigrant students / Mean score\" 519.434; reading 525.612; science 527.198.", "",
                   "## Test mode", "",
                   "- PISA 2015 Vol I, p. text line 1570 of `_cache/pisa2015_vol1.txt`: \"The paper-based form was used in 15 "
                   "countries/economies including Albania, Algeria, Argentina, Georgia, Indonesia, Jordan, Kazakhstan, Kosovo, "
                   "Lebanon, the Former Yugoslav Republic of Macedonia, Malta, Moldova, Romania, Trinidad and Tobago, and Viet "
                   "Nam, as well as in Puerto Rico\".",
                   "- PISA 2022 Vol I (`_cache/pisa2022_vol1.txt` line 7971): \"Argentina, Jordan, Moldova, North Macedonia, "
                   "Romania, Saudi Arabia and Ukraine switched from paper to computer assessment in 2022.\"",
                   "- PISA 2015 Vol I (line 13714): \"It was not possible to rule out small and moderate effects of the mode "
                   "of delivery on the mean performance of countries/economies.\"",
                   "- [INFERENCE] Paper in 2015 and computer in 2018: Albania, Georgia, Indonesia, Kazakhstan, Kosovo, Malta. "
                   "Most other countries switched from paper (2012) to computer (2015), so the switch sits in the 2012->2015 "
                   "pre-trend and the 2015 level.", "",
                   "PISA natives' 2012/2018 means (2022 Vol I Tables I.B1.7.18/7.22/7.26), first-generation and immigrant shares "
                   "(I.B1.7.2) and gaps are listed per country in `derived/national_channel_data.csv`."]
    open("reads/national_channel_inputs.md", "w").write("\n".join(L) + "\n")
    for r in t1 + t3:
        extra = " ".join(f"{k}={r[k]}" for k in r if k.startswith(("coef_", "resid_")) and r[k] != "")
        print(f"{r['test'][:6]:6} {r['sample'][:22]:22} {r['outcome'][:18]:18} {r['label'][:58]:58} n={r['n']:<3} "
              f"b={r['slope']:>7} se={r['se']:>6} mde={r['mde80']:>6} {r.get('loo_min', '')} .. {r.get('loo_max', '')} {extra}")
    for r in pw:
        print(" | ".join(str(r[k]) for k in ("design", "sample", "n", "slope", "se", "mde80", "germany_exposure",
                                             "change_window", "mde80_share_of_decline", "point_share", "ci95_share_lo",
                                             "ci95_share_hi")))


if __name__ == "__main__":
    main()
