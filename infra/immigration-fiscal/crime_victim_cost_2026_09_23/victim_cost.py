"""Victim cost of offences the Mexican-origin group commits against other US residents, 2024.

    victim cost = sum_offence  incidents committed by the group
                               x share with a victim outside the group
                               x victim-only unit cost

Frame: the complete annual account's absent-target comparison (40,896,574 CPS ASEC 2025
Mexican-origin residents; beneficiaries are all other residents). Crime-harm rule
(research/immigration-policy-causal-evidence-2026-09-20.md): victim-only unit costs; no
criminal-justice, public-service, offender or crime-career cost; no overlapping mortality
and earnings valuation; immigration-only and drug offences carry no victim price.

Inputs are all local and pinned; run homicide_inputs.py, target_population.py and
acs_exposure.py first. Every gate stops the run with [BLOCKED]. Writes derived/*.csv and
derived/run_log.txt.
"""
from __future__ import annotations

from pathlib import Path
import re
import subprocess

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
NCVS = FISCAL / "ncvs_victim_offender_2026_09_18"
CRIME = FISCAL / "crime_cost_2026_09_16"
HOM = FISCAL / "homicide_cost_2026_09_18"
ACSI = FISCAL / "acs_institutional_2026_09_16"
OUT = HERE / "derived"
LOG: list[str] = []
TARGET_ALL_AGES = 40_896_574
VICTIMS = ["White", "Black", "Hispanic", "Other"]            # NCVS rows (non-Hispanic except Hispanic)
HOM_GROUPS = {"nh_white": "White", "nh_black": "Black", "hispanic": "Hispanic", "nh_other": "Other"}
NONFATAL = ["Rape/sexual assault", "Robbery", "Aggravated assault", "Simple assault"]


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def gate(name: str, ok: bool, detail: str) -> None:
    say(f"[gate] {name}: {'PASS' if ok else 'FAIL'} — {detail}")
    if not ok:
        raise SystemExit(f"[BLOCKED] gate failed: {name}")


# ---------------------------------------------------------------------------------------
# 1. Prices
# ---------------------------------------------------------------------------------------
def cpi() -> dict[int, float]:
    c = pd.read_csv(NCVS / "derived/cpi_u_annual.csv").set_index("year").cpi_u.to_dict()
    gate("CPI-U annual averages (BLS CUUR0000SA0, held by the NCVS lane)",
         c[2008] == 215.303 and c[2017] == 245.12 and c[2024] == 313.689,
         f"2008 {c[2008]}, 2017 {c[2017]}, 2024 {c[2024]}")
    return c


def mccollister_tables() -> dict[str, dict[str, float]]:
    """Tables 3-5 parsed from the PMC JATS record of McCollister, French & Fang (2010)."""
    import xml.etree.ElementTree as ET
    tree = ET.parse(HERE / "_cache/oai_PMC2835847.xml")

    def local(t):
        return t.split("}")[-1] if isinstance(t, str) else ""

    def txt(e):
        return " ".join("".join(e.itertext()).split())

    tables = {}
    for tw in tree.getroot().iter():
        if local(tw.tag) != "table-wrap":
            continue
        label = next((txt(c) for c in tw if local(c.tag) == "label"), "")
        rows = []
        for tr in tw.iter():
            if local(tr.tag) == "tr":
                rows.append([txt(c) for c in tr if local(c.tag) in ("td", "th")])
        tables[label] = rows

    def money(s: str) -> float:
        s = s.strip()
        return 0.0 if s in ("N/A", "") else float(re.sub(r"[^\d.]", "", s))

    def by_offence(label: str, cols: int) -> dict[str, list[float]]:
        out = {}
        for r in tables[label]:
            if len(r) == cols + 1 and r[0] and not r[0].startswith("Type of"):
                name = re.sub(r"[ab]$", "", r[0]).strip()
                out[name] = [money(x) for x in r[1:]]
        return out

    t3 = by_offence("Table 3", 4)   # victim, CJS, career, total tangible
    t4 = by_offence("Table 4", 3)   # pain and suffering, corrected risk-of-homicide, total intangible
    t5 = by_offence("Table 5", 3)   # tangible, intangible, total
    names = {"murder": "Murder", "rape_sa": "Rape/Sexual Assault", "agg_assault": "Aggravated Assault",
             "robbery": "Robbery", "mvt": "Motor Vehicle Theft", "burglary": "Household Burglary",
             "larceny": "Larceny/Theft"}
    res = {}
    for k, n in names.items():
        vic, cjs, car, _ = t3[n]
        ps, roh, intang = t4[n]
        total = t5[n][2]
        # Table 5 note a: total = tangible without the uncorrected (earnings-based)
        # risk-of-homicide cost + intangible.  Recover that slice from the components.
        removed = vic + cjs + car + intang - total
        res[k] = dict(victim=vic, cjs=cjs, career=car, pain_suffering=ps, roh_corrected=roh,
                      intangible=intang, total=total, roh_uncorrected=removed)
    gate("McCollister Table 4 intangible = pain and suffering + corrected risk of homicide",
         all(abs(v["pain_suffering"] + v["roh_corrected"] - v["intangible"]) < 1 for v in res.values()),
         "7/7 offences, parsed from the PMC JATS record")
    return res


def miller_2021(text: str) -> dict[str, dict[str, float]]:
    """Miller, Cohen, Swedler, Ali & Hendrie (2021) Table 5 and Table 4 counts, 2017 dollars.

    Columns: medical, mental health, productivity, property loss, public services,
    adjudication and sanctioning, perpetrator work loss, tangible subtotal, quality of life,
    total.  Every value is gated against the pdftotext extraction of the held PDF."""
    t5 = {
        "murder": [12735, 11976, 1828638, 197, 148832, 478072, 177869, 2658319, 5150836, 7809155],
        "rape": [1835, 4108, 4575, 176, 25, 852, 351, 11923, 214518, 226441],
        "other_sa": [706, 1580, 1760, 68, 51, 328, 135, 4627, 82507, 87134],
        "robbery": [1436, 156, 3401, 1279, 647, 6754, 2905, 16578, 11145, 27723],
        "assault": [1734, 177, 1192, 44, 1891, 2705, 1002, 8745, 20581, 29326],
        "burglary": [0, 0, 23, 1641, 240, 386, 384, 2675, 0, 2675],
        "larceny": [0, 0, 15, 465, 678, 1935, 170, 3263, 0, 3263],
        "mvt": [0, 0, 102, 6214, 565, 1552, 606, 9039, 0, 9039],
    }
    counts = {"rape": 4938892, "other_sa": 3856756, "assault": 8909594, "aggravated": 1417526,
              "simple": 7492068}
    cols = ["medical", "mental", "productivity", "property", "public_services", "adjudication",
            "perpetrator", "tangible", "qol", "total"]

    def present(v: int) -> bool:
        toks = [f"{v:,}", f"{v}"] if v >= 1000 else [f"{v}"]
        return any(re.search(rf"(?<![\d,]){re.escape(t)}(?![\d,])", text) for t in toks)

    missing = [(k, v) for k, row in t5.items() for v in row if v and not present(v)]
    missing += [(k, v) for k, v in counts.items() if not present(v)]
    gate("Miller 2021 transcription appears in the PDF text", not missing,
         f"{sum(len(r) for r in t5.values()) + len(counts)} values checked; missing {missing}")
    off = {k: sum(r[:7]) - r[7] for k, r in t5.items()}
    closes = all(abs(x) <= 1 for x in off.values()) and all(r[7] + r[8] == r[9] for r in t5.values())
    gate("Miller 2021 Table 5 rows close to published rounding", closes,
         "seven tangible columns sum to the subtotal within $1 (rape, other sexual assault and burglary "
         f"are off by one: {', '.join(f'{k} {v:+.0f}' for k, v in off.items() if v)}); subtotal + QoL = total")
    return {k: dict(zip(cols, map(float, r))) for k, r in t5.items()}, counts


def price_sets(c: dict[int, float], mcc: dict, m21: dict, m21n: dict, k_assault: float) -> pd.DataFrame:
    f08, f17 = c[2024] / c[2008], c[2024] / c[2017]
    rows = []

    def add(pset, offence, tangible, qol, excluded, note):
        rows.append(dict(price_set=pset, offence=offence, victim_tangible=tangible, intangible=qol,
                         full=tangible + qol, excluded_non_victim=excluded, note=note))

    # --- Miller 2021 victim-only: medical + mental health + productivity + property; + QoL.
    def mv(r):
        return (r["medical"] + r["mental"] + r["productivity"] + r["property"]) * f17

    def mx(r):
        return (r["public_services"] + r["adjudication"] + r["perpetrator"]) * f17

    add("miller2021", "Murder", mv(m21["murder"]), m21["murder"]["qol"] * f17, mx(m21["murder"]),
        "productivity is PV of lost earnings + household work; QoL is net of work loss (no overlap)")
    wr = m21n["rape"] / (m21n["rape"] + m21n["other_sa"])
    rsa = {k: wr * m21["rape"][k] + (1 - wr) * m21["other_sa"][k] for k in m21["rape"]}
    add("miller2021", "Rape/sexual assault", mv(rsa), rsa["qol"] * f17, mx(rsa),
        f"rape and other sexual assault pooled at Miller's Table 4 incidence ({wr:.3f} rape)")
    add("miller2021", "Robbery", mv(m21["robbery"]), m21["robbery"]["qol"] * f17, mx(m21["robbery"]), "")
    # Assault: Miller prices one pooled category (84.1% simple by count).  Split with the NCVS
    # lane's cost ratio k (aggravated / simple) on the victim-only cost; the tangible split uses
    # the lane's injury-scaled simple-assault victim tangible, property loss held flat.
    sa = pd.read_csv(NCVS / "derived/simple_assault_unit_cost.csv").set_index("route")
    low = sa.loc["3_derived_tangible_bracket_low"]
    v_simple = float(low.tangible_2024 - low.cjs_component_2024) + m21["assault"]["property"] * f17
    ws = m21n["simple"] / m21n["assault"]
    wa = m21n["aggravated"] / m21n["assault"]
    pooled_v = mv(m21["assault"])
    pooled_full = pooled_v + m21["assault"]["qol"] * f17
    t_simple = pooled_full / (ws + wa * k_assault)
    t_agg = k_assault * t_simple
    v_agg = (pooled_v - ws * v_simple) / wa
    gate(f"assault split (k={k_assault:.4f}) reconstructs Miller's pooled victim-only cost",
         abs(ws * t_simple + wa * t_agg - pooled_full) < 0.01 and abs(ws * v_simple + wa * v_agg - pooled_v) < 0.01,
         f"pooled ${pooled_full:,.0f}; simple ${t_simple:,.0f}, aggravated ${t_agg:,.0f}")
    add("miller2021", "Aggravated assault", v_agg, t_agg - v_agg, mx(m21["assault"]),
        f"split from Miller's pooled assault at k={k_assault:.2f}")
    add("miller2021", "Simple assault", v_simple, t_simple - v_simple, mx(m21["assault"]),
        f"split from Miller's pooled assault at k={k_assault:.2f}")
    for o, key in [("Burglary", "burglary"), ("Larceny/theft", "larceny"), ("Motor vehicle theft", "mvt")]:
        add("miller2021", o, mv(m21[key]), 0.0, mx(m21[key]), "no quality-of-life loss priced")

    # --- McCollister 2010 victim-only with the risk-of-homicide component removed.
    # Murder: tangible = PV of lifetime earnings; full = VSL alone (it subsumes earnings).
    m = mcc["murder"]
    add("mccollister2010", "Murder", m["victim"] * f08, (m["intangible"] - m["victim"]) * f08 + 0.0,
        (m["cjs"] + m["career"]) * f08, "full = Viscusi-Aldy VSL only; earnings are inside it")
    for o, key in [("Rape/sexual assault", "rape_sa"), ("Robbery", "robbery"), ("Aggravated assault", "agg_assault")]:
        r = mcc[key]
        vic = (r["victim"] - r["roh_uncorrected"]) * f08
        add("mccollister2010", o, vic, r["pain_suffering"] * f08,
            (r["cjs"] + r["career"] + r["roh_corrected"] + r["roh_uncorrected"]) * f08,
            "risk-of-homicide removed from both victim cost and intangible (deaths counted as murders)")
    simple_row = [r for r in rows if r["price_set"] == "miller2021" and r["offence"] == "Simple assault"][0]
    add("mccollister2010", "Simple assault", simple_row["victim_tangible"], simple_row["intangible"],
        simple_row["excluded_non_victim"], "not priced by McCollister; Miller-derived value carried")
    for o, key in [("Burglary", "burglary"), ("Larceny/theft", "larceny"), ("Motor vehicle theft", "mvt")]:
        r = mcc[key]
        add("mccollister2010", o, (r["victim"] - r["roh_uncorrected"]) * f08, 0.0,
            (r["cjs"] + r["career"] + r["intangible"] + r["roh_uncorrected"]) * f08,
            "intangible is risk-of-homicide only, removed")
    # Murder "full" for McCollister: VSL itself.  (Stored as tangible + (VSL - tangible).)
    out = pd.DataFrame(rows)
    # --- Miller 2021 with the DOT 2024 VSL for the statistical life of a murder victim.
    import json
    vsl = json.loads((HOM / "derived/external_params.json").read_text())["vsl_dot_2024"]["value"]
    dot = out[out.price_set.eq("miller2021")].copy()
    dot["price_set"] = "miller2021_dot_vsl"
    i = dot.offence.eq("Murder")
    dot.loc[i, "intangible"] = vsl - dot.loc[i, "victim_tangible"]
    dot.loc[i, "full"] = vsl
    dot.loc[i, "note"] = f"full = US DOT 2024 VSL ${vsl:,.0f} (includes earnings)"
    out = pd.concat([out, dot], ignore_index=True)
    return out, f08, f17


# ---------------------------------------------------------------------------------------
# 2. Incidence
# ---------------------------------------------------------------------------------------
def ncvs_inputs() -> dict:
    mat = pd.read_csv(NCVS / "derived/matrix_pooled_2022_2024.csv")
    I = mat.pivot_table(index="victim", columns="offender", values="count", aggfunc="sum")
    rates = pd.read_csv(NCVS / "derived/rates_by_victim_and_offender_2022_2024.csv")
    h = rates[(rates.group == "Hispanic") & (rates.side == "offender")].iloc[0]
    rate = h.incidents / h.person_years * 1000
    gate("positive control: Hispanic perceived-offender rate 13.9 per 1,000 residents 12+",
         round(rate, 1) == 13.9 and abs(I["Hispanic"].sum() - h.incidents) < 1,
         f"{I['Hispanic'].sum():,.0f} incidents / {h.person_years:,.0f} person-years = {rate:.4f}")
    col = I["Hispanic"] / I["Hispanic"].sum()
    gate("positive control: Hispanic-offender same-group share 0.404",
         round(col["Hispanic"], 3) == 0.404, f"{col['Hispanic']:.5f}")
    pop = pd.read_csv(NCVS / "derived/cv_population_12plus.csv")
    pop_h = pop[(pop.group == "Hispanic")].set_index("year").population
    gate("NCVS Hispanic person-years 2022-2024 equal the rate denominator",
         abs(pop_h.loc[[2022, 2023, 2024]].sum() - h.person_years) < 1, f"{pop_h.loc[[2022, 2023, 2024]].sum():,.0f}")
    nd = pd.read_csv(NCVS / "derived/ndash_rate_by_victim_race.csv")
    nd = nd[nd.year.between(2022, 2024) & nd.crimeType.isin(NONFATAL)]
    v = nd.pivot_table(index="victim_race", columns="crimeType", values="count", aggfunc="sum")[NONFATAL]
    mix = v.div(v.sum(axis=1), axis=0)
    ratio = v.sum(axis=1) / I.sum(axis=1)
    gate("victimisations per incident within 1.06-1.09 (NCVS lane cross-check)",
         ratio.between(1.05, 1.10).all(), ", ".join(f"{g} {ratio[g]:.4f}" for g in VICTIMS))
    ann = pd.read_csv(NCVS / "derived/cv_matrix_violent.csv")
    a24 = ann[(ann.year == 2024) & (ann.measure == "count")].pivot_table(
        index="victim", columns="offender", values="value", aggfunc="sum")
    ct = pd.read_csv(NCVS / "derived/matrix_by_crime_type_2019.csv")
    ct = ct[ct.offender.eq("Hispanic")].pivot_table(index="victim", columns="scope", values="count")
    serious_2019 = (ct["serious_violent"] / ct["violent"]).to_dict()
    return dict(I=I, rate=rate, py=h.person_years, pop_h_2024=float(pop_h.loc[2024]), mix=mix,
                vict_ratio=ratio, I2024=a24, serious_2019=serious_2019)


def cv2024_number(table: str, label: str) -> float:
    """The 2024 number in a BJS *Criminal Victimization, 2024* table (it sits under '2024*')."""
    t = pd.read_csv(NCVS / "_cache/cv24" / table, header=None, encoding="latin-1", dtype=str,
                    names=range(30)).fillna("")
    year_row = t[t.apply(lambda r: "2024*" in [c.strip() for c in r], axis=1)].iloc[0]
    j = [c.strip() for c in year_row].index("2024*")
    for _, r in t.iterrows():
        cells = [c.strip() for c in r]
        if label in cells:
            return float(cells[j].replace(",", ""))
    raise SystemExit(f"[BLOCKED] {table} row {label} not found")


def arrest_share_incidence() -> dict[str, float]:
    """Disconfirmation input: Hispanic-offender victimisations by offence if offender ethnicity
    followed the Hispanic share of 2019 adult arrests (FBI Table 43C, ethnicity panel) rather
    than NCVS victims' perceptions.  National 2024 victimisations from CV2024 table 1.  FBI
    'Rape' is narrower than NCVS rape/sexual assault; 'Other assaults' stands in for simple
    assault.  Arrests carry enforcement, charging and panel-geography differences."""
    n = {"Rape/sexual assault": cv2024_number("cv24t01.csv", "Rape/sexual assault/c"),
         "Robbery": cv2024_number("cv24t01.csv", "Robbery"),
         "Aggravated assault": cv2024_number("cv24t01.csv", "Aggravated assault"),
         "Simple assault": cv2024_number("cv24t01.csv", "Simple assault")}
    gate("CV2024 table 1, 2024 violent victimisations", n == {
        "Rape/sexual assault": 560_890, "Robbery": 642_150, "Aggravated assault": 1_341_950,
        "Simple assault": 4_126_640}, ", ".join(f"{k} {v:,.0f}" for k, v in n.items()))
    x = pd.read_csv(HERE / "derived/fbi_2019_table43c_adult_arrests.csv").drop_duplicates().set_index("offense")
    lab = {"Rape/sexual assault": "Rape3", "Robbery": "Robbery", "Aggravated assault": "Aggravated assault",
           "Simple assault": "Other assaults"}
    share = {o: float(x.loc[l, "hispanic"]) / float(x.loc[l, "ethnicity_total"]) for o, l in lab.items()}
    say("[input] Hispanic share of 2019 adult arrests: " + ", ".join(f"{o} {s:.3f}" for o, s in share.items()))
    return {o: n[o] * share[o] for o in NONFATAL}


def institutional_ratio() -> dict[str, float]:
    a = pd.read_csv(ACSI / "acs5_2020_2024_origins.csv")
    h = a[a.block.eq("hispanic_origin")]
    mex = h[h.group.eq("Mexican")]
    r_mex = mex.institutional.sum() / mex.population.sum()
    r_all = h.institutional.sum() / h.population.sum()
    spec = h[~h.group.str.startswith("Other Hispanic")]
    r_spec = spec.institutional.sum() / spec.population.sum()
    return dict(rate_mexican=r_mex, rate_listed_hispanic=r_all, rate_specific_origins=r_spec,
                ratio_generic_kept=r_mex / r_all, ratio_generic_reallocated=r_mex / r_spec)


# ---------------------------------------------------------------------------------------
# 3. One run of the model
# ---------------------------------------------------------------------------------------
def run(o: dict, P: pd.DataFrame, nc: dict, hom: dict, s_pop: float, m_geo: dict) -> dict:
    prices = P[P.price_set.eq(o["price"])].set_index("offence")
    I = nc["I2024"] if o["ncvs_year"] == "2024" else nc["I"]
    known = ["White", "Black", "Hispanic", "Other"]
    m = m_geo[o["m"]]
    s = s_pop[o["pop_basis"]] * o["ratio"]
    rows = []
    for v in VICTIMS:
        ih = float(I.loc[v, "Hispanic"])
        if o["unknown"] == "proportional":
            ih *= 1 + float(I.loc[v, "Unknown"]) / float(I.loc[v, known].sum())
        if o["ncvs_year"] == "pooled":
            ih *= nc["pop_h_2024"] / nc["py"]          # pooled rate x 2024 Hispanic population
        mex = ih * s
        vict = mex * (float(nc["vict_ratio"][v]) if o["victimisations"] else 1.0)
        outside = vict * (1.0 if v != "Hispanic" else 1.0 - m)
        mix = nc["mix"].loc[v].to_dict()
        if o["mix"] == "pair_2019" and v in nc["serious_2019"]:
            ser = nc["serious_2019"][v]
            within = {k: mix[k] / (1 - mix["Simple assault"]) for k in NONFATAL[:3]}
            mix = {**{k: ser * within[k] for k in NONFATAL[:3]}, "Simple assault": 1 - ser}
        for off in NONFATAL:
            rows.append(dict(block="nonfatal_violence", victim=v, offence=off,
                             hispanic_offender_incidents_2024=ih * mix[off],
                             hispanic_victimisations=ih * float(nc["vict_ratio"][v]) * mix[off],
                             group_incidents=mex * mix[off], group_victimisations=vict * mix[off],
                             outside_victims=outside * mix[off]))
    if o["nonfatal_source"] == "arrests_2019":
        # keep NCVS's victim distribution; rescale each offence to the arrest-share total
        nf = pd.DataFrame(rows)
        for off in NONFATAL:
            f = nc["arrest_based"][off] / nf.loc[nf.offence.eq(off), "hispanic_victimisations"].sum()
            for r in rows:
                if r["offence"] == off:
                    for k in ["hispanic_offender_incidents_2024", "hispanic_victimisations",
                              "group_incidents", "group_victimisations", "outside_victims"]:
                        r[k] *= f
    for g, v in HOM_GROUPS.items():
        p = hom["p"].loc[(o["hom_window"], g)]
        n_h = hom["wonder"][g] * p.p_off_hispanic
        if o["hom_scope"] == "cleared_only":
            n_h *= p.cleared_share
        rows.append(dict(block="homicide", victim=v, offence="Murder", hispanic_offender_incidents_2024=n_h))
    df = pd.DataFrame(rows)
    hm = df.block.eq("homicide")
    if o["hom_dist"] == "joint_imputed":
        tot = df.loc[hm, "hispanic_offender_incidents_2024"].sum()
        share = hom["joint"]
        df.loc[hm, "hispanic_offender_incidents_2024"] = [tot * share[g] for g in HOM_GROUPS]
    df.loc[hm, "group_incidents"] = df.loc[hm, "hispanic_offender_incidents_2024"] * s
    df.loc[hm, "group_victimisations"] = df.loc[hm, "group_incidents"]
    df.loc[hm, "outside_victims"] = [x * (1.0 if v != "Hispanic" else 1.0 - m)
                                     for x, v in zip(df.loc[hm, "group_incidents"], df.loc[hm, "victim"])]
    df["unit_tangible"] = df.offence.map(prices.victim_tangible)
    df["unit_full"] = df.offence.map(prices.full)
    df["cost_tangible"] = df.outside_victims * df.unit_tangible
    df["cost_full"] = df.outside_victims * df.unit_full
    tot_t, tot_f = df.cost_tangible.sum(), df.cost_full.sum()
    mur = df[df.offence.eq("Murder")]
    return dict(detail=df, tangible=tot_t, full=tot_f,
                all_victims_tangible=(df.group_victimisations * df.unit_tangible).sum(),
                all_victims_full=(df.group_victimisations * df.unit_full).sum(),
                murder_share_tangible=mur.cost_tangible.sum() / tot_t,
                murder_share_full=mur.cost_full.sum() / tot_f,
                per_person_tangible=tot_t / TARGET_ALL_AGES, per_person_full=tot_f / TARGET_ALL_AGES,
                outside_nonfatal=df.loc[~hm, "outside_victims"].sum(),
                group_nonfatal=df.loc[~hm, "group_victimisations"].sum(),
                outside_homicide=df.loc[hm, "outside_victims"].sum(),
                group_homicide=df.loc[hm, "group_incidents"].sum())


def main() -> None:
    OUT.mkdir(exist_ok=True)
    c = cpi()
    mcc = mccollister_tables()
    f08 = c[2024] / c[2008]
    held = pd.read_csv(CRIME / "crime_cost_by_group.csv")
    held = held[held.route.eq("unit_cost")].set_index("arm")
    gate("positive control: McCollister murder and aggravated assault in 2024$ equal the crime_cost lane",
         abs(mcc["murder"]["total"] * f08 - held.loc["murder", "difference"]) < 1
         and abs(mcc["agg_assault"]["total"] * f08 - held.loc["assault", "difference"]) < 1,
         f"murder ${mcc['murder']['total'] * f08:,.0f} (held ${held.loc['murder', 'difference']:,.0f}); "
         f"aggravated assault ${mcc['agg_assault']['total'] * f08:,.0f} (held ${held.loc['assault', 'difference']:,.0f})")
    txt = NCVS / "_cache/miller2021_jbca.txt"
    if not txt.exists():
        subprocess.run(["pdftotext", "-layout", str(NCVS / "_cache/miller2021_jbca.pdf"), str(txt)], check=True)
    m21, m21n = miller_2021(txt.read_text(errors="replace"))
    ps = pd.read_csv(NCVS / "derived/miller2021_price_set.csv").set_index("ncvs_offence")
    f17 = c[2024] / c[2017]
    k_central = (m21["assault"]["total"] * f17 / ps.loc["Simple assault", "total_2024"]
                 - m21n["simple"] / m21n["assault"]) / (m21n["aggravated"] / m21n["assault"])
    say(f"[input] NCVS lane central aggravated-to-simple assault cost ratio k = {k_central:.4f}")
    P = {}
    for k_label, k in [("k_central", k_central), ("k_floor", 1.93)]:
        pk, _, _ = price_sets(c, mcc, m21, m21n, k)
        P[k_label] = pk
    P["k_central"].to_csv(OUT / "unit_costs_victim_only_2024usd.csv", index=False, float_format="%.2f")
    say("\n-- Victim-only unit costs, 2024 dollars (central k) --")
    say(P["k_central"][["price_set", "offence", "victim_tangible", "intangible", "full", "excluded_non_victim"]]
        .to_string(index=False, float_format=lambda x: f"{x:,.0f}"))
    # McCollister as the crime_cost lane priced it, for the diagnostic comparison only.
    diag = pd.DataFrame([dict(offence=o, mccollister_total_2024=mcc[k]["total"] * f08,
                              risk_of_homicide_2024=(mcc[k]["roh_corrected"]) * f08,
                              cjs_and_career_2024=(mcc[k]["cjs"] + mcc[k]["career"]) * f08)
                         for o, k in [("Murder", "murder"), ("Rape/sexual assault", "rape_sa"),
                                      ("Robbery", "robbery"), ("Aggravated assault", "agg_assault")]])
    diag.to_csv(OUT / "mccollister_total_decomposition_2024usd.csv", index=False, float_format="%.2f")

    nc = ncvs_inputs()
    nc["arrest_based"] = arrest_share_incidence()
    tp = pd.read_csv(HERE / "derived/target_population_cps2025.csv").set_index("group")
    gate("target population reproduces the complete account",
         abs(tp.loc["union", "all_ages"] - TARGET_ALL_AGES) < 1, f"{tp.loc['union', 'all_ages']:,.1f}")
    s_pop = {"cps_share": tp.loc["union", "age_12_plus"] / tp.loc["cps_hispanic_civilian", "age_12_plus"],
             "rate_x_target": tp.loc["union", "age_12_plus"] / nc["pop_h_2024"]}
    ir = institutional_ratio()
    ex = pd.read_csv(HERE / "derived/mexican_share_of_hispanic_exposure.csv").set_index("level").m
    m_geo = {"tract": ex["tract"], "county": ex["county"], "national": ex["national"], "none": 1.0}
    scaling = pd.DataFrame([
        dict(item="target 12+ (CPS ASEC 2025 union)", value=tp.loc["union", "age_12_plus"]),
        dict(item="CPS Hispanic civilian 12+", value=tp.loc["cps_hispanic_civilian", "age_12_plus"]),
        dict(item="NCVS Hispanic 12+ 2024", value=nc["pop_h_2024"]),
        dict(item="population share, within CPS (central)", value=s_pop["cps_share"]),
        dict(item="population share, NCVS denominator (rate x target)", value=s_pop["rate_x_target"]),
        *[dict(item=f"ACS 2020-24 institutional, men 18-39: {k}", value=v) for k, v in ir.items()],
        *[dict(item=f"Mexican share of Hispanic neighbours, {k}", value=v) for k, v in ex.items()],
    ])
    scaling.to_csv(OUT / "scaling_hispanic_to_mexican.csv", index=False, float_format="%.6f")
    say("\n-- Hispanic-to-Mexican-origin scaling and in-group share of Hispanic victims --")
    say(scaling.to_string(index=False, float_format=lambda x: f"{x:,.4f}"))

    p = pd.read_csv(HERE / "derived/shr_p_offender_given_victim.csv").set_index(["window", "victim"])
    w = pd.read_csv(HERE / "derived/wonder_2024_homicide_victims.csv").set_index("group")
    joint = pd.read_csv(HOM / "derived/c1b_matrix_joint_impute.csv").set_index("off_eth").loc["hispanic"].to_dict()
    hom = dict(p=p, wonder=w.deaths_not_stated_allocated.to_dict(), joint=joint)
    gate("WONDER 2024 victims with not-stated allocated sum to the published total",
         abs(w.deaths_not_stated_allocated.sum() - w.deaths.sum()) < 0.5, f"{w.deaths.sum():,.0f}")

    base = dict(price="miller2021", unknown="proportional", victimisations=True, ratio=1.0,
                pop_basis="cps_share", m="tract", ncvs_year="pooled", mix="victim_group",
                hom_window="2024", hom_scope="all", hom_dist="victim_conditional", k="k_central",
                nonfatal_source="ncvs")

    def go(**kw):
        o = {**base, **kw}
        return run(o, P[o["k"]], nc, hom, s_pop, m_geo)

    central = go()
    d = central["detail"]
    d.to_csv(OUT / "cost_by_victim_and_offence_central.csv", index=False, float_format="%.4f")
    by_off = d.groupby("offence", sort=False)[["hispanic_offender_incidents_2024", "group_incidents",
                                               "group_victimisations", "outside_victims",
                                               "cost_tangible", "cost_full"]].sum()
    by_off["unit_tangible"] = by_off.cost_tangible / by_off.outside_victims
    by_off["unit_full"] = by_off.cost_full / by_off.outside_victims
    by_off["share_of_full"] = by_off.cost_full / by_off.cost_full.sum()
    by_off.loc["Total"] = by_off.sum(numeric_only=True)
    by_off.loc["Total", ["unit_tangible", "unit_full"]] = np.nan
    by_off.to_csv(OUT / "cost_by_offence_central.csv", float_format="%.4f")
    say("\n-- Central: 2024, cost to other residents by offence (Miller 2021 victim-only prices) --")
    say(by_off.to_string(float_format=lambda x: f"{x:,.0f}" if abs(x) >= 10 else f"{x:.3f}"))
    say(f"\nCENTRAL: tangible ${central['tangible'] / 1e9:,.2f}bn, full ${central['full'] / 1e9:,.2f}bn; "
        f"murder share {central['murder_share_tangible']:.3f} tangible / {central['murder_share_full']:.3f} full; "
        f"per person ${central['per_person_tangible']:,.0f} / ${central['per_person_full']:,.0f}")
    say(f"All of the group's victims, including its own members, priced the same way: tangible "
        f"${central['all_victims_tangible'] / 1e9:,.2f}bn, full ${central['all_victims_full'] / 1e9:,.2f}bn")

    # NCVS sampling error on the non-fatal part: BJS generalized-variance SEs of the pooled
    # Hispanic-offender cells, summed in quadrature across years by the NCVS lane (understated:
    # the rotating panel correlates adjacent years).  Delta method, cells independent.
    mat = pd.read_csv(NCVS / "derived/matrix_pooled_2022_2024.csv")
    se = mat[mat.offender.eq("Hispanic")].set_index("victim").se
    nf = d[d.block.eq("nonfatal_violence")].groupby("victim")[["cost_tangible", "cost_full"]].sum()
    samp = []
    for col in ["cost_tangible", "cost_full"]:
        var = sum((se[v] / nc["I"].loc[v, "Hispanic"] * nf.loc[v, col]) ** 2 for v in VICTIMS)
        samp.append(dict(measure=col, nonfatal_cost=nf[col].sum(), se=np.sqrt(var),
                         relative_se=np.sqrt(var) / nf[col].sum()))
    samp = pd.DataFrame(samp)
    samp.to_csv(OUT / "ncvs_sampling_error_central.csv", index=False, float_format="%.4f")
    say("NCVS sampling error on the non-fatal cost (one SE, understated): "
        + ", ".join(f"{r.measure} ${r.se / 1e9:,.2f}bn ({r.relative_se:.1%})" for r in samp.itertuples()))

    # Cross-group shares actually implied, both margins
    grp = d.groupby("block")
    shares = []
    for blk, g in grp:
        h = g[g.victim.eq("Hispanic")].group_victimisations.sum()
        tot = g.group_victimisations.sum()
        shares.append(dict(block=blk, group_victims=tot, non_hispanic_share_lower_bound=1 - h / tot,
                           outside_share_estimate=g.outside_victims.sum() / tot))
    shares = pd.DataFrame(shares)
    shares.to_csv(OUT / "outside_victim_shares_central.csv", index=False, float_format="%.6f")
    say("\n-- Share of the group's victims who are other residents --")
    say(shares.to_string(index=False, float_format=lambda x: f"{x:,.4f}"))

    # One-at-a-time arms
    arms = [("central", {})]
    arms += [("price: McCollister 2010, risk of homicide removed", dict(price="mccollister2010")),
             ("price: Miller 2021 non-fatal + DOT 2024 VSL for murder", dict(price="miller2021_dot_vsl")),
             ("assault cost ratio k at the NCVS injury/arrest floor 1.93", dict(k="k_floor")),
             ("NCVS unknown-offender incidents dropped (known only)", dict(unknown="known_only")),
             ("incidents not converted to victimisations", dict(victimisations=False)),
             ("NCVS 2024 alone instead of pooled 2022-2024 rate", dict(ncvs_year="2024")),
             ("offence mix: 2019 Hispanic-offender serious share by victim", dict(mix="pair_2019")),
             ("scaling: rate x target (NCVS 2024 denominator)", dict(pop_basis="rate_x_target")),
             (f"scaling: ACS institutional ratio {ir['ratio_generic_kept']:.3f} (generic Hispanic kept apart)",
              dict(ratio=ir["ratio_generic_kept"])),
             (f"scaling: ACS institutional ratio {ir['ratio_generic_reallocated']:.3f} (generic reallocated)",
              dict(ratio=ir["ratio_generic_reallocated"])),
             ("Hispanic victims all in-group (non-Hispanic victims only: lower bound)", dict(m="none")),
             ("Hispanic victims Mexican at county exposure 0.744", dict(m="county")),
             ("Hispanic victims Mexican at national share 0.586", dict(m="national")),
             ("homicide: SHR 2019-2024 offender distribution", dict(hom_window="2019_2024")),
             ("homicide: cleared cases only", dict(hom_scope="cleared_only")),
             ("homicide: joint-imputed victim distribution (homicide lane C1b)", dict(hom_dist="joint_imputed")),
             ("non-fatal offender ethnicity from 2019 adult arrest shares, not NCVS perception",
              dict(nonfatal_source="arrests_2019"))]
    lo_kw = dict(unknown="known_only", victimisations=False, ratio=ir["ratio_generic_kept"], m="none",
                 hom_scope="cleared_only", k="k_floor")
    hi_kw = dict(ratio=ir["ratio_generic_reallocated"], m="county", hom_dist="joint_imputed",
                 ncvs_year="2024", pop_basis="rate_x_target")
    for pr in ["miller2021", "mccollister2010", "miller2021_dot_vsl"]:
        arms.append((f"ENVELOPE low, {pr}", dict(lo_kw, price=pr)))
        arms.append((f"ENVELOPE high, {pr}", dict(hi_kw, price=pr)))
    res = []
    for name, kw in arms:
        r = go(**kw)
        res.append(dict(arm=name, tangible_bn=r["tangible"] / 1e9, full_bn=r["full"] / 1e9,
                        murder_share_tangible=r["murder_share_tangible"], murder_share_full=r["murder_share_full"],
                        per_person_tangible=r["per_person_tangible"], per_person_full=r["per_person_full"],
                        outside_nonfatal_victims=r["outside_nonfatal"], outside_homicide_victims=r["outside_homicide"],
                        group_nonfatal_victims=r["group_nonfatal"], group_homicides=r["group_homicide"]))
    arms_df = pd.DataFrame(res)
    arms_df.to_csv(OUT / "arms.csv", index=False, float_format="%.4f")
    say("\n-- Arms (one at a time; ENVELOPE rows stack every low or high choice) --")
    say(arms_df[["arm", "tangible_bn", "full_bn", "murder_share_full", "per_person_full",
                 "outside_nonfatal_victims", "outside_homicide_victims"]]
        .to_string(index=False, float_format=lambda x: f"{x:,.3f}" if abs(x) < 10 else f"{x:,.0f}"))

    # Diagnostic: the same outside incidents at the McCollister totals the older lanes used
    dg = d.copy()
    tot_map = diag.set_index("offence").mccollister_total_2024.to_dict()
    tot_map["Simple assault"] = float(ps.loc["Simple assault", "total_2024"])
    dg["cost_old_totals"] = dg.outside_victims * dg.offence.map(tot_map)
    say(f"\n[diagnostic] the central outside victims priced at McCollister totals as the crime_cost/NCVS "
        f"lanes used them (with CJS, crime career and risk of homicide): ${dg.cost_old_totals.sum() / 1e9:,.2f}bn "
        f"against the victim-only full ${central['full'] / 1e9:,.2f}bn")

    offender_rate_crosscheck(hom).to_csv(OUT / "offender_rate_crosscheck.csv", index=False, float_format="%.4f")

    # Property: arrest-based proxy, reported separately, not in the headline
    prop = property_proxy(P["k_central"], nc, s_pop["cps_share"], shares)
    prop.to_csv(OUT / "property_proxy.csv", index=False, float_format="%.4f")
    say("\n-- Property crime, arrest-share proxy (separate line, not in the headline) --")
    say(prop.to_string(index=False, float_format=lambda x: f"{x:,.3f}" if abs(x) < 10 else f"{x:,.0f}"))
    (OUT / "run_log.txt").write_text("\n".join(LOG) + "\n")


def offender_rate_crosscheck(hom: dict) -> pd.DataFrame:
    """Offending ratios implied by this lane's inputs against BJS official imprisonment rates.

    BJS *Prisoners in 2023* Table 6 (adult imprisonment per 100,000, race/Hispanic reporting
    adjusted by BJS with SPI 2016) is held by the 2026-09-05 ethnicity audit
    (research/immigration-crime-race-ethnicity-2026-09-05.md); parsed here from its pdftotext."""
    root = HERE.parents[2]
    arch = root / ".scratch/clarity-next-20260905/conduct-race"
    pdf, txt = arch / "p23st.pdf", arch / "p23st.txt"
    import hashlib
    if not txt.exists() or hashlib.sha256(pdf.read_bytes()).hexdigest() != (
            "22a4cbe8ee0ff6156db97b4825db60907d53f0a345d02166b8484e0ac307b2e9"):
        raise SystemExit("[BLOCKED] BJS p23st.pdf/.txt missing or changed; restore from "
                         "https://bjs.ojp.gov/document/p23st.pdf (pdftotext -layout) into " + str(arch))
    lines = txt.read_text(errors="replace").splitlines()
    start = next(i for i, l in enumerate(lines) if l.strip() == "TABLE 6")
    rates = {}
    for l in lines[start:start + 25]:
        f = l.split()
        if f and f[0] in ("2019", "2023") and len(f) == 11:
            v = [float(x.replace(",", "")) for x in f[1:]]
            rates[int(f[0])] = dict(nh_white=v[5], nh_black=v[6], hispanic=v[7])
    held = pd.read_csv(arch / "analysis/bjs_p23st_table6_adult_rates.csv").set_index("year")
    gate("BJS Prisoners in 2023 Table 6 parse equals the ethnicity audit's table",
         all(rates[y][k] == held.loc[y, {"nh_white": "non_hispanic_white", "nh_black": "non_hispanic_black",
                                          "hispanic": "hispanic_any_race"}[k]] for y in rates for k in rates[y]),
         f"2023 NH white {rates[2023]['nh_white']:.0f}, NH Black {rates[2023]['nh_black']:.0f}, "
         f"Hispanic {rates[2023]['hispanic']:.0f} per 100,000 adults")
    pop = pd.read_csv(NCVS / "derived/cv_population_12plus.csv")
    pop = pop[pop.year.eq(2024)].set_index("group").population
    p = hom["p"].xs("2024", level="window")
    off = {o: sum(hom["wonder"][g] * p.loc[g, f"p_off_{o}"] for g in HOM_GROUPS) for o in ["hispanic", "nh_white", "nh_black"]}
    hr = {"hispanic": off["hispanic"] / pop["Hispanic"], "nh_white": off["nh_white"] / pop["White"],
          "nh_black": off["nh_black"] / pop["Black"]}
    r = pd.read_csv(NCVS / "derived/rates_by_victim_and_offender_2022_2024.csv")
    r = r[r.side.eq("offender")].set_index("group").rate_per_1000
    rows = []
    for g, lab in [("hispanic", "Hispanic"), ("nh_black", "Black")]:
        rows.append(dict(group=g,
                         homicide_offending_ratio_2024=hr[g] / hr["nh_white"],
                         ncvs_nonfatal_offending_ratio_2022_2024=r[lab] / r["White"],
                         bjs_imprisonment_ratio_2023=rates[2023][g] / rates[2023]["nh_white"],
                         bjs_imprisonment_ratio_2019=rates[2019][g] / rates[2019]["nh_white"]))
    out = pd.DataFrame(rows)
    say("\n-- Offending ratios vs non-Hispanic white: this lane's inputs against BJS imprisonment --")
    say(f"homicide offenders 2024 (WONDER x SHR): Hispanic {off['hispanic']:,.0f}, NH white {off['nh_white']:,.0f}, "
        f"NH Black {off['nh_black']:,.0f}; per 100,000 residents 12+: "
        + ", ".join(f"{k} {v * 1e5:.2f}" for k, v in hr.items()))
    say(out.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    return out


def property_proxy(P: pd.DataFrame, nc: dict, s: float, shares: pd.DataFrame) -> pd.DataFrame:
    """NCVS 2024 household property victimisations x Hispanic share of adult arrests
    (FBI 2019 Table 43C, the ethnicity-reporting panel) x population share x outside share."""
    vict = {"Burglary": cv2024_number("cv24t02.csv", "Burglary/c"),
            "Motor vehicle theft": cv2024_number("cv24t02.csv", "Motor vehicle theft"),
            "Larceny/theft": cv2024_number("cv24t02.csv", "Other theft/e")}
    gate("CV2024 table 2, 2024 property victimisations", vict["Burglary"] == 1_103_790
         and vict["Motor vehicle theft"] == 841_120 and vict["Larceny/theft"] == 10_618_790,
         ", ".join(f"{k} {v:,.0f}" for k, v in vict.items()))
    x = pd.read_csv(HERE / "derived/fbi_2019_table43c_adult_arrests.csv").drop_duplicates().set_index("offense")
    share = {}
    for label, off in [("Burglary", "Burglary"), ("Larceny-theft", "Larceny/theft"),
                       ("Motor vehicle theft", "Motor vehicle theft")]:
        share[off] = float(x.loc[label, "hispanic"]) / float(x.loc[label, "ethnicity_total"])
    gate("FBI 2019 Table 43C Hispanic shares of adult arrests (ethnicity panel)",
         abs(share["Burglary"] - 18958 / 93297) < 1e-9 and abs(share["Motor vehicle theft"] - 10659 / 42130) < 1e-9,
         ", ".join(f"{k} {v:.4f}" for k, v in share.items()))
    outside = float(shares.set_index("block").loc["nonfatal_violence", "outside_share_estimate"])
    rows = []
    for pset in ["miller2021", "mccollister2010"]:
        pr = P[P.price_set.eq(pset)].set_index("offence")
        for off, n in vict.items():
            grp = n * share[off] * s
            rows.append(dict(price_set=pset, offence=off, victimisations_2024=n, hispanic_arrest_share=share[off],
                             group_offences=grp, outside_offences=grp * outside,
                             unit_victim_cost=pr.loc[off, "full"], cost=grp * outside * pr.loc[off, "full"]))
    df = pd.DataFrame(rows)
    tot = df.groupby("price_set").cost.sum()
    say(f"[property] total ${tot['miller2021'] / 1e9:,.2f}bn (Miller) / ${tot['mccollister2010'] / 1e9:,.2f}bn "
        f"(McCollister); outside share borrowed from non-fatal violence {outside:.3f}")
    return df


if __name__ == "__main__":
    main()
