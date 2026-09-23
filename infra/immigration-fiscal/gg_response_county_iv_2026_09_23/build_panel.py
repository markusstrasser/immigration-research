"""Build the county panel: local administration spending, population and the two instruments.

Geography. County areas, harmonised across 2000-2022: New York City's five boroughs are one unit
(the city government is filed under New York County); Shannon SD (46113) is Oglala Lakota (46102);
Bedford city VA (51515) joins Bedford County (51019) and Clifton Forge (51560) joins Alleghany
(51005). Dropped: Alaska (boroughs and census areas redrawn in the window), Connecticut (2022 files
use planning regions), the District of Columbia (one government doing state, county and city work),
Kalawao HI (no local government) and Broomfield CO (created in 2001, so no 2000 settlement shares).
National totals for the instruments always use every county, dropped or not.

Spending. Current operations (E-codes) and direct expenditure (E, F, G, J) on financial
administration (23), central staff (29), general public buildings (31) and judicial and legal (25),
summed over every local unit located in the county area. 2012, 2017 and 2022 from the Census
individual-unit files (finance.py); 1997, 2002 and 2007 from the Government Finance Database
(gfd_stream.py), whose current-operations columns equal the Census files exactly in 2012 and 2022
(gates.py). Real 2022 dollars with the CPI-U annual average of the fiscal year's calendar year.

Population. July 1 estimates: 2002 and 2007 from the 2000-2010 intercensal series, 2012 and 2017 from
the 2010-2020 intercensal series (YEAR 4 and 9), 2022 from vintage 2023 (YEAR 4, AGEGRP 0).

Instrument (a), industry mix. County Business Patterns private employment by 3-digit NAICS in the
base year, suppressed cells imputed (establishment size-class midpoints, clipped to the flag's
employment range, scaled to the reported parent total), times national leave-one-out employment
growth by industry over the window. Industries that change code between the two years are pooled
into their sector; retail (44-45) and information (51) are pooled for windows ending in 2022,
when NAICS 2022 redrew them. The pay variant uses the same shares and national leave-one-out growth
of annual payroll per employee.

Instrument (b), immigrant settlement. 2000 Census SF3 PCT019 county shares of each origin's
foreign-born population times the origin's national leave-one-out change between ACS 5-year windows
centred on the window's end years (2009, 2014, 2019, 2024 for 2007, 2012, 2017, 2022), divided by
base-year population. Origins: the 2000 table's named countries, with the rest pooled into eight
regional residuals. Variants without Mexico and Mexico alone.

Outputs: derived/panel.csv, derived/build_audit.json, _cache/bartik_<window>.npz (components for
the Rotemberg decomposition).
"""
import csv
import io
import json
import re
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FISCAL = HERE.parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
EXTERNAL = ROOT / "sources/immigration-fiscal/data/external"
sys.path.insert(0, str(HERE))
import finance  # noqa: E402

CPI = {int(k): v for k, v in json.loads((FISCAL / "local_spending_composition_2026_09_18/_cache/cpi.json").read_text()).items()}
CPI.update({int(k): v for k, v in json.loads((CACHE / "cpi_extra.json").read_text()).items()})
DROP_STATES = {"02", "09", "11", "60", "66", "69", "72", "78"}
DROP_FIPS = {"15005", "08014"}
RECODE = {"36005": "36NYC", "36047": "36NYC", "36061": "36NYC", "36081": "36NYC", "36085": "36NYC",
          "46113": "46102", "51515": "51019", "51560": "51005"}
FIN_YEARS = [1997, 2002, 2007, 2012, 2017, 2022]
ITEMS = ["e23", "e29", "e31", "e25", "d23", "d29", "d31", "d25"]
POP_YEARS = [2002, 2007, 2012, 2017, 2022]
WINDOWS = {"1222": (2012, 2022), "0717": (2007, 2017), "1217": (2012, 2017), "1722": (2017, 2022),
           "0712": (2007, 2012)}
ACS_FOR = {2007: 2009, 2012: 2014, 2017: 2019, 2022: 2024}
AUDIT = {}


def harm(fips):
    if fips[:2] in DROP_STATES or fips in DROP_FIPS:
        return None
    return RECODE.get(fips, fips)


# ----------------------------------------------------------------------------- spending
def spending():
    out = defaultdict(lambda: defaultdict(float))
    present = defaultdict(set)
    with (CACHE / "gfd_admin_county.csv").open() as fh:
        for r in csv.DictReader(fh):
            year = int(r["year"])
            if year not in FIN_YEARS or year >= 2012:
                continue
            unit = harm(r["fips"])
            if unit is None:
                continue
            present[year].add(unit)
            for item in ITEMS:
                out[(unit, year)][item] += float(r[item])
    for year in (2012, 2017, 2022):
        for fips, rec in finance.read_indunit(year).items():
            unit = harm(fips)
            if unit is None:
                continue
            present[year].add(unit)
            for item in ITEMS:
                out[(unit, year)][item] += rec[item]
    national = {y: {i: sum(v[i] for (u, yy), v in out.items() if yy == y) / 1e6 for i in ITEMS} for y in FIN_YEARS}
    AUDIT["spending_nominal_bn_in_sample_geography"] = national
    AUDIT["spending_units_by_year"] = {y: len(present[y]) for y in FIN_YEARS}
    return out, present


def county_government_flags():
    flags = {}
    for year in (2012, 2022):
        has = defaultdict(bool)
        for fips, typ, _name in finance.unit_directory(year):
            unit = harm(fips)
            if unit is not None:
                has[unit] |= typ == "1"
        for unit, v in has.items():
            flags.setdefault(unit, {})[year] = v
    return flags


# ----------------------------------------------------------------------------- population
def population():
    pop = defaultdict(lambda: defaultdict(float))
    raw = defaultdict(dict)
    with (CACHE / "pep/co-est00int-tot.csv").open(encoding="latin-1") as fh:
        for r in csv.DictReader(fh):
            if int(r["SUMLEV"]) != 50:
                continue
            fips = f"{int(r['STATE']):02d}{int(r['COUNTY']):03d}"
            for y in (2002, 2007):
                raw[fips][y] = float(r[f"POPESTIMATE{y}"])
    with (CACHE / "pep/cc-est2020int-agesex-all.csv").open(encoding="latin-1") as fh:
        for r in csv.DictReader(fh):
            if int(r["SUMLEV"]) != 50 or r["YEAR"] not in ("4", "9"):
                continue
            fips = f"{int(r['STATE']):02d}{int(r['COUNTY']):03d}"
            raw[fips][2012 if r["YEAR"] == "4" else 2017] = float(r["POPESTIMATE"])
    with (EXTERNAL / "census_county_pop/cc-est2023-alldata.csv").open(encoding="latin-1") as fh:
        for r in csv.DictReader(fh):
            if r["YEAR"] == "4" and r["AGEGRP"] == "0":
                raw[f"{int(r['STATE']):02d}{int(r['COUNTY']):03d}"][2022] = float(r["TOT_POP"])
    national = {y: sum(v.get(y, 0.0) for f, v in raw.items() if f[:2] != "72") for y in POP_YEARS}
    AUDIT["population_national_millions"] = {y: round(v / 1e6, 3) for y, v in national.items()}
    for fips, years in raw.items():
        unit = harm(fips)
        if unit is None:
            continue
        for y, v in years.items():
            pop[unit][y] += v
    missing = sorted(u for u, v in pop.items() if any(y not in v for y in POP_YEARS))
    AUDIT["population_units_missing_a_year"] = missing
    return pop


# ----------------------------------------------------------------------------- County Business Patterns
FLAG_RANGE = {"A": (0, 19), "B": (20, 99), "C": (100, 249), "E": (250, 499), "F": (500, 999), "G": (1000, 2499),
              "H": (2500, 4999), "I": (5000, 9999), "J": (10000, 24999), "K": (25000, 49999), "L": (50000, 99999),
              "M": (100000, 10_000_000)}
MIDPOINT = {"n1_4": 2.5, "n<5": 2.5, "n5_9": 7, "n10_19": 14.5, "n20_49": 34.5, "n50_99": 74.5, "n100_249": 174.5,
            "n250_499": 374.5, "n500_999": 749.5, "n1000_1": 1249.5, "n1000_2": 1999.5, "n1000_3": 3749.5, "n1000_4": 7500}
THREE = re.compile(r"^\d\d\d///$")
TWO = re.compile(r"^\d\d----$")


def sector(code):
    d = code[:2]
    return {"45": "44", "49": "48", "32": "31", "33": "31"}.get(d, d)


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def size_estimate(row):
    total = 0.0
    for k, m in MIDPOINT.items():
        v = num(row.get(k))
        if v:
            total += v * m
    if not any(num(row.get(k)) for k in ("n1000_1", "n1000_2", "n1000_3", "n1000_4")):
        v = num(row.get("n1000"))
        if v:
            total += v * 2000
    return total


def clip(value, flag):
    lo, hi = FLAG_RANGE.get(flag, (0, 10_000_000))
    return min(max(value, lo), hi)


def fill(children, parent):
    """Reported children kept; flagged children get size-class estimates scaled to the parent's residual."""
    out = {k: c["emp"] for k, c in children.items() if not c["flag"]}
    flagged = {k: c for k, c in children.items() if c["flag"]}
    if flagged:
        guess = {k: clip(c["size"], c["flag"]) for k, c in flagged.items()}
        resid = None if parent is None else parent - sum(out.values())
        s = sum(guess.values())
        if resid is not None and resid > 0 and s > 0:
            guess = {k: clip(v * resid / s, flagged[k]["flag"]) for k, v in guess.items()}
        out.update(guess)
    return out


def read_cbp(year):
    if year == 2007:
        zf = zipfile.ZipFile(CACHE / "cbp/cbp07co.zip")
        fh = io.TextIOWrapper(zf.open(zf.namelist()[0]), encoding="latin-1")
    else:
        fh = (EXTERNAL / f"cbp_county/cbp{str(year)[2:]}co.txt").open(encoding="latin-1")
    cells = defaultdict(dict)
    with fh:
        for r in csv.DictReader(fh):
            naics = r["naics"]
            if naics != "------" and not TWO.match(naics) and not THREE.match(naics):
                continue
            fips = r["fipstate"] + r["fipscty"]
            flag = (r.get("empflag") or "").strip()
            cells[fips][naics] = {"emp": num(r["emp"]) or 0.0, "ap": num(r["ap"]) or 0.0, "flag": flag,
                                  "size": size_estimate(r)}
    emp, pay = defaultdict(dict), defaultdict(dict)
    n3 = nflag3 = 0
    reported_pay = defaultdict(lambda: [0.0, 0.0])
    for fips, c in cells.items():
        for k, v in c.items():
            if THREE.match(k) and not v["flag"] and v["emp"] > 0:
                reported_pay[k][0] += v["ap"]
                reported_pay[k][1] += v["emp"]
    avg_pay = {k: a / e for k, (a, e) in reported_pay.items() if e > 0}
    for fips, c in cells.items():
        total = c.get("------")
        total_v = None if total is None else (total["emp"] if not total["flag"] else clip(total["size"], total["flag"]))
        two = fill({k: v for k, v in c.items() if TWO.match(k)}, total_v)
        kids = defaultdict(dict)
        for k, v in c.items():
            if THREE.match(k):
                kids[sector(k)][k] = v
                n3 += 1
                nflag3 += bool(v["flag"])
        for sec, children in kids.items():
            values = fill(children, two.get(sec + "----"))
            for k, e in values.items():
                if k.startswith("99"):
                    continue
                emp[fips][k] = e
                pay[fips][k] = children[k]["ap"] if not children[k]["flag"] else e * avg_pay.get(k, 0.0)
    AUDIT.setdefault("cbp", {})[year] = {"three_digit_cells": n3, "flagged_share": round(nflag3 / n3, 4),
                                         "national_private_employment_millions":
                                             round(sum(sum(v.values()) for v in emp.values()) / 1e6, 3)}
    return emp, pay


def industry_groups(years_emp, pool_2022):
    """3-digit codes with employment in every listed year; the rest pooled by sector."""
    totals = []
    for d in years_emp:
        n = Counter()
        for v in d.values():
            n.update(v)
        totals.append(n)
    common = {k for k in totals[0] if all(n.get(k, 0) > 0 for n in totals)}
    if pool_2022:
        common = {k for k in common if sector(k) not in ("44", "51")}
    return lambda k: k if k in common else f"{sector(k)}_pooled"


def bartik(window, shares, e0, e1, p0, p1, units, pool_2022):
    """Shares from `shares` (a base-year CBP), national leave-one-out growth from e0 to e1."""
    group = industry_groups([shares, e0, e1], pool_2022)
    def regroup(d):
        out = defaultdict(lambda: defaultdict(float))
        for fips, row in d.items():
            for k, v in row.items():
                out[fips][group(k)] += v
        return out
    g_s, g_e0, g_e1, g_p0, g_p1 = regroup(shares), regroup(e0), regroup(e1), regroup(p0), regroup(p1)
    groups = sorted({g for d in (g_s, g_e0, g_e1) for row in d.values() for g in row})
    gi = {g: i for i, g in enumerate(groups)}
    def national(d):
        v = np.zeros(len(groups))
        for row in d.values():
            for g, x in row.items():
                v[gi[g]] += x
        return v
    N0, N1, P0, P1 = national(g_e0), national(g_e1), national(g_p0), national(g_p1)
    def unit_matrix(d):
        m = np.zeros((len(units), len(groups)))
        ui = {u: i for i, u in enumerate(units)}
        for fips, row in d.items():
            u = harm(fips) if fips[2:] != "999" else None
            if u is None or u not in ui:
                continue
            for g, x in row.items():
                m[ui[u], gi[g]] += x
        return m
    S, E0, E1, A0, A1 = unit_matrix(g_s), unit_matrix(g_e0), unit_matrix(g_e1), unit_matrix(g_p0), unit_matrix(g_p1)
    tot = S.sum(axis=1, keepdims=True)
    Z = np.divide(S, tot, out=np.zeros_like(S), where=tot > 0)
    with np.errstate(divide="ignore", invalid="ignore"):
        G = (N1 - E1) / (N0 - E0) - 1
        W = ((P1 - A1) / (N1 - E1)) / ((P0 - A0) / (N0 - E0)) - 1
        national = N1 / N0 - 1
    bad = int((~np.isfinite(G) & (Z > 0)).sum())
    G = np.where(np.isfinite(G), G, 0.0)
    W = np.where(np.isfinite(W), W, 0.0)
    np.savez_compressed(CACHE / f"bartik_{window}.npz", units=np.array(units), groups=np.array(groups), Z=Z, G=G,
                        national_growth=np.where(np.isfinite(national), national, 0.0), national_emp0=N0)
    AUDIT.setdefault("bartik", {})[window] = {"groups": len(groups), "pooled_groups": [g for g in groups if "_pooled" in g],
                                              "national_growth": round(float(N1.sum() / N0.sum() - 1), 4),
                                              "nonfinite_growth_cells_with_share": bad}
    return dict(zip(units, (Z * G).sum(axis=1))), dict(zip(units, (Z * W).sum(axis=1))), dict(zip(units, tot[:, 0]))


# ----------------------------------------------------------------------------- immigrant settlement
REGIONS = ["Europe", "Asia", "Africa", "Oceania", "Caribbean", "Central America", "South America", "Northern America"]


def norm(s):
    s = re.sub(r"\(.*?\)", "", s).lower().replace(",", " ").strip()
    return re.sub(r"\s+", " ", s)


def tree(dataset, group):
    meta = json.loads((CACHE / "api" / f"{dataset.replace('/', '_')}_{group}_vars.json").read_text())["variables"]
    nodes = {}
    for k, v in meta.items():
        if not k.startswith(group) or (group == "B05006" and not k.endswith("E")):
            continue
        path = [p.strip().rstrip(":") for p in v["label"].replace("Estimate!!", "").split("!!")]
        nodes[k] = path
    return nodes


def county_table(dataset, group):
    rows = json.loads((CACHE / "api" / f"{dataset.replace('/', '_')}_{group}_county.json").read_text())
    head = rows[0]
    out = {}
    for r in rows[1:]:
        fips = r[0] + r[1]
        if fips[:2] == "72":
            continue
        out[fips] = {h: (float(x) if x not in (None, "", "null") else 0.0) for h, x in zip(head[2:], r[2:])}
    return out


def origin_scheme():
    base = tree("2000/dec/sf3", "PCT019")
    acs = {y: tree(f"{y}/acs/acs5", "B05006") for y in ACS_FOR.values()}
    paths = [tuple(p) for p in base.values()]
    named = []
    for k, p in sorted(base.items()):
        is_leaf = not any(len(q) > len(p) and q[:len(p)] == tuple(p) for q in paths)
        n = norm(p[-1])
        if len(p) < 3 or not is_leaf or n.startswith("other") or "n.e.c" in n or p[1] == "Born at sea":
            continue
        named.append(n)
    scheme = {}
    for label, nodes in [("2000", base)] + [(str(y), n) for y, n in acs.items()]:
        by_name = defaultdict(list)
        for k, p in nodes.items():
            by_name[norm(p[-1])].append(k)
        region_var = {}
        for reg in REGIONS:
            hits = by_name.get(norm(reg), [])
            if len(hits) != 1:
                raise SystemExit(f"[BLOCKED] {label}: region {reg} matched {hits}")
            region_var[reg] = hits[0]
        countries = {}
        for n in named:
            hits = by_name.get(n, [])
            if len(hits) == 1:
                path = nodes[hits[0]]
                reg = next((r for r in REGIONS if r in path), None)
                countries[n] = (hits[0], reg)
        scheme[label] = {"regions": region_var, "countries": countries, "total": sorted(nodes)[0]}
    keep = [n for n in named if all(n in s["countries"] for s in scheme.values())]
    for n in keep:
        regs = {s["countries"][n][1] for s in scheme.values()}
        if len(regs) != 1 or None in regs:
            raise SystemExit(f"[BLOCKED] origin {n} changes region across tables: {regs}")
    AUDIT["origins"] = {"named": keep, "dropped_to_residual": sorted(set(named) - set(keep)), "regions": REGIONS}
    return scheme, keep


def origin_values(table, scheme, keep):
    out = {}
    for fips, row in table.items():
        v = {}
        for n in keep:
            v[n] = row[scheme["countries"][n][0]]
        for reg in REGIONS:
            inside = sum(row[scheme["countries"][n][0]] for n in keep if scheme["countries"][n][1] == reg)
            v[f"rest of {reg}"] = row[scheme["regions"][reg]] - inside
        v["_total"] = row[scheme["total"]]
        out[fips] = v
    return out


def immigrant_instruments(pop, units):
    scheme, keep = origin_scheme()
    base = origin_values(county_table("2000/dec/sf3", "PCT019"), scheme["2000"], keep)
    acs = {y: origin_values(county_table(f"{y}/acs/acs5", "B05006"), scheme[str(y)], keep) for y in ACS_FOR.values()}
    origins = keep + [f"rest of {r}" for r in REGIONS]
    coverage = {}
    for label, data in [("2000", base)] + [(str(y), d) for y, d in acs.items()]:
        tot = sum(v["_total"] for v in data.values())
        covered = sum(sum(v[o] for o in origins) for v in data.values())
        coverage[label] = {"foreign_born_millions": round(tot / 1e6, 3), "share_in_origin_groups": round(covered / tot, 5)}
        if any(min(v[o] for o in origins) < -1e-6 for v in data.values()):
            raise SystemExit(f"[BLOCKED] {label}: negative residual origin count")
    AUDIT["origin_coverage"] = coverage
    def to_units(data):
        out = defaultdict(lambda: defaultdict(float))
        for fips, v in data.items():
            u = harm(fips)
            if u is None:
                continue
            for o in origins + ["_total"]:
                out[u][o] += v[o]
        return out
    base_u = to_units(base)
    acs_u = {y: to_units(d) for y, d in acs.items()}
    nat_base = {o: sum(v[o] for v in base.values()) for o in origins}
    nat_acs = {y: {o: sum(v[o] for v in d.values()) for o in origins + ["_total"]} for y, d in acs.items()}
    result = {}
    for w, (t0, t1) in WINDOWS.items():
        a0, a1 = ACS_FOR[t0], ACS_FOR[t1]
        inst = {}
        for u in units:
            if u not in base_u or u not in acs_u[a0] or u not in acs_u[a1]:
                continue
            total = nomex = mex = 0.0
            for o in origins:
                if nat_base[o] <= 0:
                    continue
                share = base_u[u][o] / nat_base[o]
                change = (nat_acs[a1][o] - acs_u[a1][u][o]) - (nat_acs[a0][o] - acs_u[a0][u][o])
                total += share * change
                if o == "mexico":
                    mex += share * change
                else:
                    nomex += share * change
            p0 = pop[u][t0]
            fb_change = acs_u[a1][u]["_total"] / pop[u][t1] - acs_u[a0][u]["_total"] / p0
            inst[u] = {"imm": total / p0, "imm_nomex": nomex / p0, "imm_mex": mex / p0, "dfbshare": fb_change}
        result[w] = inst
        AUDIT.setdefault("immigrant_national_change_millions", {})[w] = {
            "all": round((nat_acs[a1]["_total"] - nat_acs[a0]["_total"]) / 1e6, 3),
            "mexico": round((nat_acs[a1]["mexico"] - nat_acs[a0]["mexico"]) / 1e6, 3)}
    return result


# ----------------------------------------------------------------------------- income
def median_income():
    out = defaultdict(dict)
    with (FISCAL / "local_spending_composition_2026_09_18/derived/county_shares.csv").open() as fh:
        for r in csv.DictReader(fh):
            u = harm(r["fips"])
            if u is None or not r["medhhinc"] or u == "36NYC":
                continue
            out[u][int(r["wave"])] = float(r["medhhinc"])
    return out


def main():
    DERIVED.mkdir(exist_ok=True)
    spend, present = spending()
    flags = county_government_flags()
    pop = population()
    units = sorted(u for u in pop if all(y in pop[u] for y in POP_YEARS))
    print(f"[ok  ] population for {len(units)} county areas", flush=True)
    cbp = {y: read_cbp(y) for y in (2007, 2012, 2017, 2022)}
    print("[ok  ] county business patterns read and imputed", flush=True)
    bart = {}
    for w, (t0, t1) in WINDOWS.items():
        bart[w] = bartik(w, cbp[t0][0], cbp[t0][0], cbp[t1][0], cbp[t0][1], cbp[t1][1], units, t1 == 2022)
    # Stacked second period on fixed 2012 shares: growth 2017->2022, shares from 2012.
    bart["1722_s12"] = bartik("1722_s12", cbp[2012][0], cbp[2017][0], cbp[2022][0], cbp[2017][1], cbp[2022][1], units, True)
    # Break-free stacked design (2007->2012, 2012->2017): second period on fixed 2007 shares.
    bart["1217_s07"] = bartik("1217_s07", cbp[2007][0], cbp[2012][0], cbp[2017][0], cbp[2012][1], cbp[2017][1], units, False)
    print("[ok  ] industry-mix instruments", flush=True)
    imm = immigrant_instruments(pop, units)
    print("[ok  ] immigrant settlement instruments", flush=True)
    inc = median_income()
    cols = ["fips", "state", "no_county_govt"] + [f"pop_{y}" for y in POP_YEARS]
    cols += [f"{i}_{y}" for y in FIN_YEARS for i in ITEMS] + [f"present_{y}" for y in FIN_YEARS]
    for w in WINDOWS:
        cols += [f"bartik_{w}", f"bartik_pay_{w}", f"cbp_emp0_{w}", f"imm_{w}", f"imm_nomex_{w}", f"imm_mex_{w}", f"dfbshare_{w}"]
    cols += ["bartik_1722_s12", "bartik_1217_s07", "medhhinc_2009", "medhhinc_2012", "medhhinc_2017", "medhhinc_2022"]
    rows = []
    for u in units:
        r = {"fips": u, "state": u[:2], "no_county_govt": int(not (flags.get(u, {}).get(2012, False) and flags.get(u, {}).get(2022, False)))}
        for y in POP_YEARS:
            r[f"pop_{y}"] = f"{pop[u][y]:.0f}"
        for y in FIN_YEARS:
            rec = spend.get((u, y))
            r[f"present_{y}"] = int(u in present[y])
            for i in ITEMS:
                r[f"{i}_{y}"] = "" if rec is None else f"{rec[i] * CPI[2022] / CPI[y]:.3f}"
        for w in WINDOWS:
            b, bp, e0 = bart[w]
            r[f"bartik_{w}"] = f"{b[u]:.8f}"
            r[f"bartik_pay_{w}"] = f"{bp[u]:.8f}"
            r[f"cbp_emp0_{w}"] = f"{e0[u]:.1f}"
            for k in ("imm", "imm_nomex", "imm_mex", "dfbshare"):
                v = imm[w].get(u, {}).get(k)
                r[f"{k}_{w}"] = "" if v is None else f"{v:.8f}"
        r["bartik_1722_s12"] = f"{bart['1722_s12'][0][u]:.8f}"
        r["bartik_1217_s07"] = f"{bart['1217_s07'][0][u]:.8f}"
        for y in (2009, 2012, 2017, 2022):
            r[f"medhhinc_{y}"] = inc.get(u, {}).get(y, "")
        rows.append(r)
    with (DERIVED / "panel.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    AUDIT["units"] = len(rows)
    AUDIT["no_county_govt_units"] = sum(r["no_county_govt"] for r in rows)
    (DERIVED / "build_audit.json").write_text(json.dumps(AUDIT, indent=1, sort_keys=True, default=str) + "\n")
    print(f"[done] derived/panel.csv {len(rows)} county areas", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
