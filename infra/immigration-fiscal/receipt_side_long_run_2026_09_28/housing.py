#!/usr/bin/env python3
"""Where the group pays owner property tax and rent, and the land share and housing-supply response there.

The group is the ACS proxy of the case's Mexican-origin population: HISP=02 (Mexican) or POBP=303 (born in
Mexico), the dataset register's convention for ACS 2024 person PUMS. Household amounts are shared equally
among members (the case's shared allocation): owner property tax TAXAMT on owned units (TEN 1-2) and contract
rent RNTP x 12 on rented units (TEN 3), both times ADJHSG; gross rent GRNTP is a check.

PUMAs are split across counties by 2020 tract population (tracts nest in both). Each county carries FHFA's land
share of single-family property value (Working Paper 19-01, Version 4.0: the 2022 panel value; else the pooled
2012-2022 cross section; else its state's 2022 value) and the Saiz (2010) supply elasticity of its 1999 metro
(MSA, or PMSA where one exists). Missing metros take an assumption, flagged per county: Orange County, CA takes
Los Angeles-Long Beach's value; other unlisted metro counties the median of their state's listed metros;
counties outside any 1999 metro Saiz's unweighted mean (2.5, his p. 1281).

The long-run owner response in a county is r = (1 - land share) + land share x land-price fall (RESULT.md,
item 2): the tax on structures leaves with the households that would occupy them, and the tax on land stays
with the land, falling only as far as its price. The land-price fall is derived from the house-price fall,
all of it land in the long run (structures at construction cost): with unit demand elasticity (Saiz 2007: an
inflow of 1% of population raises rents and values about 1%) and the metro's supply elasticity e, removing a
population share s lowers house prices by 1 - (1 - s)^(1/(1 + e)). Variants: the same at the national share
and the population-weighted elasticity (others relocate freely), the short run (e = 0), and Combes, Duranton
and Gobillon's land-price elasticity (0.6-0.8, French cross section) applied to the land directly.

  OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl python3 \
      infra/immigration-fiscal/receipt_side_long_run_2026_09_28/housing.py

Outputs: derived/counties.csv, derived/states.csv, derived/housing.json.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CACHE = HERE / "_cache"
OUT = HERE / "derived"
EXT = ROOT / "sources/immigration-fiscal/data/external"
LOCAL = {  # read-only inputs outside the lane, pinned by content
    "acs_hus": (EXT / "acs_pums_2024_1yr/csv_hus.zip", "8281008e53de98f0ef81e7a2ee5a8725991dda1ecfd2713ead73246425e515d0"),
    "acs_pus": (EXT / "acs_pums_2024_1yr/csv_pus.zip", "afdc6d90c6e2f0bab365ed32d95ba4c4d8ac651162f46ac7861295b2dc469894"),
    "saiz": (EXT / "lifetime/saiz/saiz_2010_msa_elasticity.dta", "8699efc85e76322494b804d9695727c0f6bd916a6a80ef2341e537c9a8520807"),
    "lincoln": (HERE / "inputs/lincoln_limits_2024.csv", "849f8a77381f16eddd8893032893212ab44c44a806015fef0d5bdb1427ff6ed4"),
}
PINS = json.loads((HERE / "inputs/pins.json").read_text())
STATES = {"01": "AL", "02": "AK", "04": "AZ", "05": "AR", "06": "CA", "08": "CO", "09": "CT", "10": "DE", "11": "DC",
          "12": "FL", "13": "GA", "15": "HI", "16": "ID", "17": "IL", "18": "IN", "19": "IA", "20": "KS", "21": "KY",
          "22": "LA", "23": "ME", "24": "MD", "25": "MA", "26": "MI", "27": "MN", "28": "MS", "29": "MO", "30": "MT",
          "31": "NE", "32": "NV", "33": "NH", "34": "NJ", "35": "NM", "36": "NY", "37": "NC", "38": "ND", "39": "OH",
          "40": "OK", "41": "OR", "42": "PA", "44": "RI", "45": "SC", "46": "SD", "47": "TN", "48": "TX", "49": "UT",
          "50": "VT", "51": "VA", "53": "WA", "54": "WV", "55": "WI", "56": "WY"}
ORANGE_CA, LA_PMSA = "06059", 4480
NONMETRO_ELASTICITY = 2.5          # Saiz (2010) p. 1281: unweighted metro mean
CDG_LAND_ELASTICITY = (0.6, 0.7, 0.8)  # Combes, Duranton and Gobillon: IV "mostly between 0.60 and 0.80"


def blocked(msg: str) -> None:
    raise SystemExit(f"[BLOCKED] {msg}")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pinned(name: str) -> Path:
    if name in LOCAL:
        path, digest = LOCAL[name]
    else:
        path, digest = CACHE / name, PINS[name]["sha256"]
    if not path.exists() or sha256(path) != digest:
        blocked(f"missing or changed input {path.name}; run acquire.py (lane inputs) or restore {path}")
    return path


def r6(x: float) -> float:
    return float(f"{x:.6f}")


# ---------------------------------------------------------------------------------------------------
def puma_county_factors() -> pd.DataFrame:
    """Share of each 2020 PUMA's 2020 population in each county, from tract populations."""
    rel = pd.read_csv(pinned("census_2020_tract_to_puma.txt"), dtype=str, encoding="utf-8-sig")
    rel = rel[rel.STATEFP.isin(STATES)]
    pops = []
    for st in STATES:
        rows = json.loads(pinned(f"pl2020_tracts/{st}.json").read_text())
        head = rows[0]
        if head != ["P1_001N", "state", "county", "tract"]:
            blocked(f"unexpected PL header for state {st}: {head}")
        pops.append(pd.DataFrame(rows[1:], columns=["pop", "STATEFP", "COUNTYFP", "TRACTCE"]))
    pop = pd.concat(pops, ignore_index=True)
    pop["pop"] = pop["pop"].astype(np.int64)
    m = rel.merge(pop, on=["STATEFP", "COUNTYFP", "TRACTCE"], how="outer", indicator=True)
    if not (m["_merge"] == "both").all():
        blocked(f"tract files disagree: {m['_merge'].value_counts().to_dict()}")
    total = int(m["pop"].sum())
    if total != 331449281:  # 2020 Census resident population, 50 states and DC
        blocked(f"2020 tract populations sum to {total:,}, not 331,449,281")
    g = m.groupby(["STATEFP", "PUMA5CE", "COUNTYFP"], as_index=False)["pop"].sum()
    g["factor"] = g["pop"] / g.groupby(["STATEFP", "PUMA5CE"])["pop"].transform("sum")
    g["county"] = g["STATEFP"] + g["COUNTYFP"]
    return g.rename(columns={"STATEFP": "st", "PUMA5CE": "puma"})[["st", "puma", "county", "factor"]]


def read_zip_csvs(zpath: Path, members: list[str], usecols: list[str], dtype: dict) -> pd.DataFrame:
    with zipfile.ZipFile(zpath) as z:
        return pd.concat([pd.read_csv(z.open(m), usecols=usecols, dtype=dtype) for m in members], ignore_index=True)


def acs_person_amounts() -> tuple[pd.DataFrame, dict]:
    """Per-person shared amounts, summed by state, PUMA and group."""
    hus = read_zip_csvs(pinned("acs_hus"), ["psam_husa.csv", "psam_husb.csv"],
                        ["SERIALNO", "WGTP", "NP", "TEN", "TAXAMT", "VALP", "RNTP", "GRNTP", "ADJHSG", "BLD", "VEH"],
                        {"SERIALNO": str, "TEN": "Int64", "BLD": "Int64", "VEH": "Int64"})
    pus = read_zip_csvs(pinned("acs_pus"), ["psam_pusa.csv", "psam_pusb.csv"],
                        ["SERIALNO", "STATE", "PUMA", "PWGTP", "HISP", "POBP"],
                        {"SERIALNO": str, "STATE": str, "PUMA": str, "HISP": int, "POBP": int})
    pus["st"] = pus["STATE"].str.zfill(2)
    pus["PUMA"] = pus["PUMA"].str.zfill(5)
    pus = pus[pus.st.isin(STATES)]
    if hus.SERIALNO.duplicated().any():
        blocked("duplicate housing SERIALNO")
    p = pus.merge(hus, on="SERIALNO", how="left", validate="many_to_one")
    adj = p["ADJHSG"] / 1e6
    own = p["TEN"].isin([1, 2]) & p["TAXAMT"].notna()
    rent = p["TEN"].eq(3) & p["RNTP"].notna()
    np_ = p["NP"].where(p["NP"] > 0)
    p["group"] = (p["HISP"].eq(2) | p["POBP"].eq(303)).astype(int)
    w = p["PWGTP"].astype(float)
    p["owner_tax"] = np.where(own, w * p["TAXAMT"] * adj / np_, 0.0)
    p["owner_value"] = np.where(own & p["VALP"].notna(), w * p["VALP"] * adj / np_, 0.0)
    p["rent"] = np.where(rent, w * 12 * p["RNTP"] * adj / np_, 0.0)
    p["gross_rent"] = np.where(rent & p["GRNTP"].notna(), w * 12 * p["GRNTP"] * adj / np_, 0.0)
    p["rent_single_family"] = np.where(rent & p["BLD"].isin([2, 3]), p["rent"], 0.0)
    p["pop"] = w
    p["owner_pop"] = np.where(own, w, 0.0)
    p["renter_pop"] = np.where(rent, w, 0.0)
    p["vehicles"] = np.where(p["VEH"].notna() & np_.notna(), w * p["VEH"].fillna(0) / np_, 0.0)  # 6 = six or more
    cols = ["owner_tax", "owner_value", "rent", "gross_rent", "rent_single_family", "pop", "owner_pop", "renter_pop", "vehicles"]
    if p[cols].isna().any().any():
        blocked("missing amounts after the household merge")
    by = p.groupby(["st", "PUMA", "group"], as_index=False)[cols].sum().rename(columns={"PUMA": "puma"})
    # Household-weighted aggregates, the published-table definition (ACS B25090-style): a check on the person route.
    h_own = hus["TEN"].isin([1, 2]) & hus["TAXAMT"].notna()
    checks = {
        "owner_tax_household_weighted_bn": r6(float((hus.WGTP * hus.TAXAMT * hus.ADJHSG / 1e6)[h_own].sum()) / 1e9),
        "owner_tax_person_route_bn": r6(float(p["owner_tax"].sum()) / 1e9),
        "persons": int(len(p)), "group_persons_weighted": r6(float(w[p.group.eq(1)].sum())),
        "all_persons_weighted": r6(float(w.sum())),
    }
    return by, checks


def saiz_by_county(counties: pd.Index) -> pd.DataFrame:
    """1999 metro (PMSA where one exists) and Saiz (2010) elasticity for each county."""
    saiz = pd.read_stata(pinned("saiz"))
    saiz["code"] = saiz["msanecma"].astype(int)
    el = dict(zip(saiz.code, saiz.elasticity.astype(float)))
    rows = {}
    for line in pinned("census_1999_msa_fips.txt").read_text(encoding="latin-1").splitlines():
        if len(line) < 30 or not line[:4].strip().isdigit():
            continue
        county, town = line[24:29].strip(), line[40:45].strip()
        if not (county.isdigit() and len(county) == 5) or town:  # New England towns: not county-based
            continue
        code = int(line[8:12]) if line[8:12].strip() else int(line[:4])
        rows[county] = code
    st_median = {}
    for county, code in rows.items():
        if code in el:
            st_median.setdefault(county[:2], []).append(el[code])
    st_median = {k: float(np.median(v)) for k, v in st_median.items()}
    out = []
    for c in counties:
        code = rows.get(c)
        if c == ORANGE_CA:
            e, src = el[LA_PMSA], "imputed: Orange County takes Los Angeles-Long Beach"
        elif code is not None and code in el:
            e, src = el[code], "Saiz 2010"
        elif code is not None:
            e, src = st_median.get(c[:2], NONMETRO_ELASTICITY), "imputed: state median of listed metros"
        else:
            e, src = NONMETRO_ELASTICITY, "imputed: outside 1999 metros, Saiz unweighted mean"
        out.append((c, code if code is not None else -1, e, src))
    return pd.DataFrame(out, columns=["county", "metro", "elasticity", "elasticity_source"]).set_index("county")


def land_shares(counties: pd.Index) -> tuple[pd.DataFrame, dict]:
    book = pd.ExcelFile(pinned("fhfa_land_prices_2024_06.xlsx"))
    names = {n.strip(): n for n in book.sheet_names}  # "Cross-Section Counties " carries a trailing space
    panel, cross, states, nation = (book.parse(names[n], header=1) for n in
                                    ("Panel Counties", "Cross-Section Counties", "Panel States", "Panel Nation"))
    col = "Land Share of Property Value"
    for d in (panel, cross, states, nation):
        if col not in d.columns:
            blocked(f"FHFA sheet without '{col}': {list(d.columns)[:6]}")
    p22 = panel[panel.Year == 2022].assign(county=lambda d: d.FIPS.astype(int).astype(str).str.zfill(5))
    cs = cross.dropna(subset=["FIPS"]).assign(county=lambda d: d.FIPS.astype(int).astype(str).str.zfill(5))
    s22 = states[states.Year == 2022].assign(st=lambda d: d["State FIPS"].astype(int).astype(str).str.zfill(2))
    p22m, csm, s22m = (dict(zip(p22.county, p22[col])), dict(zip(cs.county, cs[col])), dict(zip(s22.st, s22[col])))
    out = []
    for c in counties:
        if c in p22m:
            out.append((c, p22m[c], csm.get(c, np.nan), "FHFA county 2022 panel"))
        elif c in csm:
            out.append((c, csm[c], csm[c], "FHFA county pooled cross section (2012-2022, base 2015)"))
        elif c[:2] in s22m:
            out.append((c, s22m[c[:2]], np.nan, "FHFA state 2022 panel (county not covered)"))
        else:
            blocked(f"no FHFA land share for county {c}")
    meta = {"nation_2022": r6(float(nation.loc[nation.Year == 2022, col].iloc[0])),
            "counties_in_2022_panel": int(len(p22m)), "counties_in_cross_section": int(len(csm))}
    return pd.DataFrame(out, columns=["county", "land_share", "land_share_cross_section", "land_share_source"]).set_index("county"), meta


def fall(share: np.ndarray | float, elasticity: np.ndarray | float) -> np.ndarray:
    """House-price fall when a population share leaves: unit demand elasticity, supply elasticity e."""
    return 1 - np.power(1 - np.asarray(share, float), 1 / (1 + np.asarray(elasticity, float)))


# ---------------------------------------------------------------------------------------------------
def census_property_tax_by_government() -> dict:
    """FY2022 property tax (item T01) by type of government, U.S. totals, $bn (22statetypepu.txt)."""
    labels = {"1": "state_and_local", "2": "state", "3": "local", "5": "counties", "6": "municipalities",
              "7": "townships", "8": "special_districts", "9": "school_districts"}
    with zipfile.ZipFile(pinned("census_2022_individual_unit_file.zip")) as z:
        text = z.read("2022_Individual_Unit_files/22statetypepu.txt").decode("latin-1")
    out = {}
    for line in text.splitlines():
        if line[:2] == "00" and line[4:7] == "T01":
            out[labels[line[2]]] = r6(int(line[7:20]) / 1e6)
    local = out["local"]
    parts = ["school_districts", "counties", "municipalities", "townships", "special_districts"]
    if abs(sum(out[k] for k in parts) - local) > 1e-3:
        blocked("local property tax by type does not sum to the local total")
    return {"bn": out, "share_of_local": {k: r6(out[k] / local) for k in parts},
            "source": "Census 2022 Individual Unit File, 22statetypepu.txt, U.S. rows, item T01 (property tax), $ thousands",
            "note": "dependent school systems are counted with their parent county or city, so schools' part of the property tax exceeds the school-district share"}


def bea_housing_taxes() -> dict:
    """NIPA Table 7.4.5 (housing sector): output by tenure and taxes on production and imports, 2024, $bn."""
    t = pd.read_excel(pinned("bea_Section7All_xls.xlsx"), sheet_name="T70405-A", header=None)
    head = t.index[t[0].astype(str).eq("Line")][0]
    years = [str(int(float(x))) if str(x).replace(".0", "").isdigit() else str(x) for x in t.iloc[head].tolist()]
    col = years.index("2024")
    rows = {int(t.iloc[i, 0]): (str(t.iloc[i, 1]).strip(), float(t.iloc[i, col])) for i in range(head + 1, len(t))
            if str(t.iloc[i, 0]).isdigit()}
    want = {1: "Housing output", 3: "Owner-occupied", 4: "Tenant-occupied", 15: "Taxes on production and imports"}
    for k, v in want.items():
        if not rows[k][0].startswith(v):
            blocked(f"Table 7.4.5 line {k} reads {rows[k][0]!r}, expected {v!r}")
    output, owner, tenant, topi = (rows[k][1] / 1e3 for k in (1, 3, 4, 15))
    share = tenant / output
    return {"year": 2024, "housing_output_bn": r6(output), "owner_occupied_output_bn": r6(owner),
            "tenant_occupied_output_bn": r6(tenant), "taxes_on_production_bn": r6(topi),
            "tenant_share_of_output": r6(share), "tenant_taxes_bn": r6(topi * share), "owner_taxes_bn": r6(topi * (1 - share)),
            "rule": "Table 7.4.5 gives the housing sector's taxes on production and imports (line 15) without a tenure split; they are split here by tenure's share of housing output (lines 3-4 over line 1), an equal tax per dollar of rent [INFERENCE]",
            "source": "BEA NIPA Table 7.4.5 (Section7All_xls.xlsx, sheet T70405-A)"}


# ---------------------------------------------------------------------------------------------------
def main() -> None:
    factors = puma_county_factors()
    by, checks = acs_person_amounts()
    cols = ["owner_tax", "owner_value", "rent", "gross_rent", "rent_single_family", "pop", "owner_pop", "renter_pop", "vehicles"]
    miss = by.merge(factors[["st", "puma"]].drop_duplicates(), on=["st", "puma"], how="left", indicator=True)
    if not (miss["_merge"] == "both").all():
        blocked(f"ACS PUMAs without a 2020 relationship: {miss.loc[miss._merge != 'both', ['st', 'puma']].head().values.tolist()}")
    alloc = by.merge(factors, on=["st", "puma"])
    for c in cols:
        alloc[c] = alloc[c] * alloc["factor"]
    wide = alloc.pivot_table(index="county", columns="group", values=cols, aggfunc="sum", fill_value=0.0)
    cty = pd.DataFrame(index=wide.index)
    for c in cols:
        cty[f"group_{c}"] = wide[(c, 1)] if (c, 1) in wide.columns else 0.0
        cty[f"all_{c}"] = wide[(c, 0)] + cty[f"group_{c}"]
    for c in cols:  # conservation: the county split keeps every national total
        if abs(cty[f"all_{c}"].sum() - by[c].sum()) > 1e-6 * max(1.0, by[c].sum()):
            blocked(f"county allocation loses {c}")
    land, land_meta = land_shares(cty.index)
    cty = cty.join(land).join(saiz_by_county(cty.index))
    # The group's share of its metro's population (the county's own share outside 1999 metros).
    metro_key = np.where(cty.metro >= 0, "m" + cty.metro.astype(str), "c" + cty.index.to_series())
    cty["metro_key"] = metro_key
    grp = cty.groupby("metro_key")[["group_pop", "all_pop"]].transform("sum")
    cty["metro_group_share"] = grp.group_pop / grp.all_pop
    nat_share = float(cty.group_pop.sum() / cty.all_pop.sum())
    saiz = pd.read_stata(pinned("saiz"))
    e_nat = float(np.average(saiz.elasticity, weights=saiz.population))
    lam = cty.land_share.to_numpy()
    cty["fall_lr_metro"] = np.minimum(fall(cty.metro_group_share, cty.elasticity), lam)
    cty["fall_lr_national"] = np.minimum(fall(nat_share, e_nat), lam)
    cty["fall_sr_metro"] = fall(cty.metro_group_share, 0.0)
    for tag, e in zip(["low", "mid", "high"], CDG_LAND_ELASTICITY):
        cty[f"fall_lr_cdg_{tag}"] = lam * (1 - np.power(1 - cty.metro_group_share, e))
    cty["r_lr_metro"] = 1 - lam + cty.fall_lr_metro
    cty["r_lr_national"] = 1 - lam + cty.fall_lr_national

    lincoln = pd.read_csv(pinned("lincoln"), dtype=str)
    lincoln["st"] = lincoln.fips.str.zfill(2)
    lincoln = lincoln.set_index("st")

    def regime(st: str) -> str:
        r = lincoln.loc[st]
        if r.assessment_limit == "Y":
            return "assessment-limited"
        if r.levy_limit == "Y":
            return "levy-limited (levy-set)"
        if r.overall_rate_limit == "Y" or r.specific_rate_limit == "Y":
            return "rate-limited"
        return "no limit or disclosure only"

    cty["st"] = cty.index.str[:2]
    cty["regime"] = cty.st.map(regime)
    # Short run (fixed stock): market-value regimes lose the price fall on the vacated homes; where assessments
    # are capped below market for incumbent owners, a price fall does not reach the roll (0), and reassessment
    # of vacated homes on resale (California) can raise revenue.
    cty["r_sr"] = np.where(cty.regime.eq("assessment-limited"), 0.0, cty.fall_sr_metro)

    def weighted(weight: str) -> dict:
        w = cty[weight] / cty[weight].sum()
        out = {k: r6(float((w * cty[k]).sum())) for k in
               ["land_share", "elasticity", "metro_group_share", "fall_lr_metro", "fall_lr_national", "fall_sr_metro",
                "fall_lr_cdg_low", "fall_lr_cdg_mid", "fall_lr_cdg_high", "r_lr_metro", "r_lr_national", "r_sr"]}
        out["land_share_cross_section_where_available"] = r6(float(
            (w * cty.land_share_cross_section).sum() / w[cty.land_share_cross_section.notna()].sum()))
        out["land_share_2022_on_the_same_counties"] = r6(float(
            (w * cty.land_share)[cty.land_share_cross_section.notna()].sum() / w[cty.land_share_cross_section.notna()].sum()))
        out["r_lr_cdg"] = {t: r6(1 - out["land_share"] + out[f"fall_lr_cdg_{t}"]) for t in ["low", "mid", "high"]}
        out["weight_by_land_share_source"] = {k: r6(float(v)) for k, v in w.groupby(cty.land_share_source).sum().items()}
        out["weight_by_elasticity_source"] = {k: r6(float(v)) for k, v in w.groupby(cty.elasticity_source).sum().items()}
        out["weight_by_regime"] = {k: r6(float(v)) for k, v in w.groupby(cty.regime).sum().items()}
        out["r_sr_by_regime"] = {k: r6(float((w * cty.r_sr)[cty.regime.eq(k)].sum() / w[cty.regime.eq(k)].sum()))
                                 for k in sorted(cty.regime.unique()) if w[cty.regime.eq(k)].sum() > 0}
        return out

    owner, renter = weighted("group_owner_tax"), weighted("group_rent")
    nat = {c: float(cty[f"all_{c}"].sum()) for c in cols}
    grp = {c: float(cty[f"group_{c}"].sum()) for c in cols}
    key = {
        "owner_tax_share": r6(grp["owner_tax"] / nat["owner_tax"]),
        "rent_share": r6(grp["rent"] / nat["rent"]), "gross_rent_share": r6(grp["gross_rent"] / nat["gross_rent"]),
        "population_share": r6(nat_share), "renter_population_share": r6(grp["renter_pop"] / nat["renter_pop"]),
        "owner_population_share": r6(grp["owner_pop"] / nat["owner_pop"]),
        "vehicle_share": r6(grp["vehicles"] / nat["vehicles"]),
        "group_rent_in_single_family_share": r6(grp["rent_single_family"] / grp["rent"]),
        "all_rent_in_single_family_share": r6(nat["rent_single_family"] / nat["rent"]),
    }
    amounts = {f"{s}_{c}_bn": r6(v / 1e9) for s, d in (("group", grp), ("all", nat)) for c, v in d.items()
               if c not in ("pop", "owner_pop", "renter_pop", "vehicles")}
    amounts.update({f"{s}_{c}": r6(v) for s, d in (("group", grp), ("all", nat)) for c, v in d.items()
                    if c in ("pop", "owner_pop", "renter_pop", "vehicles")})
    if not 36e6 < grp["pop"] < 42e6:
        blocked(f"group proxy population {grp['pop']:,.0f} outside 36-42 million")
    bea = bea_housing_taxes()
    iuf = census_property_tax_by_government()

    st = cty.groupby("st").agg(group_owner_tax=("group_owner_tax", "sum"), all_owner_tax=("all_owner_tax", "sum"),
                               group_rent=("group_rent", "sum"), all_rent=("all_rent", "sum"),
                               group_pop=("group_pop", "sum"), all_pop=("all_pop", "sum"))
    for k in ["land_share", "r_lr_metro", "r_sr", "fall_lr_metro"]:
        st[f"owner_weighted_{k}"] = (cty[k] * cty.group_owner_tax).groupby(cty.st).sum() / st.group_owner_tax
    st["share_of_group_owner_tax"] = st.group_owner_tax / st.group_owner_tax.sum()
    st["regime"] = [regime(s) for s in st.index]
    for k in ["levy_limit", "overall_rate_limit", "specific_rate_limit", "assessment_limit", "truth_in_taxation"]:
        st[k] = lincoln.loc[st.index, k].to_numpy()
    st = st.sort_values("group_owner_tax", ascending=False)

    OUT.mkdir(exist_ok=True)
    ccols = ["group_owner_tax", "all_owner_tax", "group_rent", "all_rent", "group_pop", "all_pop", "land_share",
             "land_share_source", "metro", "elasticity", "elasticity_source", "metro_group_share", "fall_lr_metro",
             "fall_lr_national", "fall_sr_metro", "r_lr_metro", "r_lr_national", "r_sr", "regime"]
    with (OUT / "counties.csv").open("w", newline="") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(["county"] + ccols)
        for c, row in cty.sort_values("group_owner_tax", ascending=False).iterrows():
            wr.writerow([c] + [f"{row[k]:.6f}" if isinstance(row[k], (float, np.floating)) else row[k] for k in ccols])
    scols = ["share_of_group_owner_tax", "group_owner_tax", "all_owner_tax", "group_rent", "all_rent", "group_pop",
             "all_pop", "owner_weighted_land_share", "owner_weighted_fall_lr_metro", "owner_weighted_r_lr_metro",
             "owner_weighted_r_sr", "regime", "levy_limit", "overall_rate_limit", "specific_rate_limit",
             "assessment_limit", "truth_in_taxation"]
    with (OUT / "states.csv").open("w", newline="") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(["state"] + scols)
        for s, row in st.iterrows():
            wr.writerow([STATES[s]] + [f"{row[k]:.6f}" if isinstance(row[k], (float, np.floating)) else row[k] for k in scols])
    top = st.head(8)
    result = {
        "group": "ACS 2024 proxy: HISP=02 or POBP=303; household amounts shared per member (PWGTP)",
        "amounts": amounts, "keys": key, "checks": checks,
        "owner": owner, "renter": renter,
        "national": {"group_population_share": r6(nat_share), "saiz_population_weighted_elasticity": r6(e_nat),
                     "fall_lr_national": r6(float(fall(nat_share, e_nat)))},
        "land_share_meta": land_meta,
        "top_states_by_group_owner_tax": {STATES[s]: {"share": r6(float(r.share_of_group_owner_tax)),
                                                     "regime": r.regime} for s, r in top.iterrows()},
        "bea_housing": bea, "census_property_tax_fy2022": iuf,
        "assumptions": {
            "demand_elasticity": "1 (Saiz 2007: an inflow of 1% of population raises rents and values about 1%, short run)",
            "long_run_fall": "1 - (1 - s)^(1/(1 + e)), capped at the land share (land cannot fall below zero)",
            "nonmetro_elasticity": NONMETRO_ELASTICITY, "orange_county": "Los Angeles-Long Beach elasticity",
            "renter_land_share": "the county single-family land share (FHFA covers single-family parcels only); multifamily land shares are lower, so this understates the renters' response",
            "short_run": "0 where assessments are capped (Lincoln assessment limit), else the fixed-stock price fall",
        },
    }
    (OUT / "housing.json").write_text(json.dumps(result, indent=1) + "\n")
    print(json.dumps({"keys": key, "owner": {k: owner[k] for k in ["land_share", "metro_group_share", "fall_lr_metro", "r_lr_metro", "r_lr_national", "r_sr"]},
                      "renter": {k: renter[k] for k in ["land_share", "r_lr_metro", "r_lr_national"]},
                      "amounts": {k: amounts[k] for k in ["group_owner_tax_bn", "all_owner_tax_bn", "group_rent_bn", "all_rent_bn"]},
                      "checks": checks, "bea_tenant_taxes_bn": bea["tenant_taxes_bn"]}, indent=1))


if __name__ == "__main__":
    sys.exit(main())
