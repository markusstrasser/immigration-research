#!/usr/bin/env python3
"""The taxes on the business capital that serves the group's jobs (job-capital taxes lane, the item).

For each line, the item is sum over industry cells of (the group's share of the cell's wage bill) x (the line's
national amount in the cell, national.py) x (the line's response at the reading). The group's share comes from CPS
ASEC 2025 (income year 2024): wage and salary income (WSAL_VAL, clipped at 0, the employer_hi key's wage concept), the
industry of the longest job (INDUSTRY) mapped to BEA cells by inputs/census_industry_crosswalk.csv, government
workers (LJCW 2 federal; 3-4 state and local) in the government cells whatever their industry. The frame is
full_account_receipts_2026_09_20/builder.py's (civilian household persons; the union of the Mexico-born, the
second generation and self-identified Mexican-origin third-plus; personal = own wages, shared = the resource unit's
wages split equally among its members), on row 4's weights: the Mexico-born outside California and Texas raked to
ACS 2024 by citizenship (main_case_candidate_2026_09_28/derived/production_row4.json), column by column for the
160 replicates; national totals include the reweighted records (the pattern of world_ledger_2026_09_27
population_basis.py and v4_inputs.py). The case's fill-in correction of the union's wages (cps_imputation_keys
status_combination_keys.csv, wage key, the case's two methods averaged) moves the union's wages, split across the
generations as the case splits the same methods' wage-key change (generation_account_2026_09_24
stack_by_generation.json, components D, convention a); it is a measurement correction of wages. The status rules
of the case's wage key (the imputed unauthorized's wages at the on-books lane's shares) do not apply: an off-books
job's capital is taxed at its source, and the case's production term counts all CPS earnings. Whites and Blacks:
third-plus non-Hispanic white alone and Black alone (the lineage's whites), and every nativity (white_all, black_all).
Two small-sample rules: each group's wages at or above $1M (the public file caps each earnings source at $1,099,999)
are spread over the cells as the nation's such wages are, group totals unchanged; a cell with fewer than N_MIN CPS
wage earners takes its sector's pooled share.

Responses, at the band's two readings (the team lead, 2026-10-14): corporate tax at 1 at the low end (the whole base
leaves with the capital) and at the base's normal-return share at the high end (Treasury OTA Technical Paper 5, p. 7:
37 percent; OTA's July 2021 methodology still gives labor half of it, 18.5 percent); other production taxes at 1 at
both; business property r = tau + (1 - tau) x r_b at both, tau the tangible personal property share of the line (it
leaves whole) and r_b = 1 - lambda_b (1 - delta_L) on the real property: lambda_b the land share of business real
estate (national.py, Z.1 against Fixed Assets) and delta_L the long-run land-price fall where the group lives (receipt
lane housing.py, counties.csv: fall_lr_metro / land_share, weighted by the group's population as the place of its
jobs). Mining (BEA 211, 212, 213) responds at 0 on all three lines at both readings: severance, the property tax on
mineral interests and mining's profits fall on a fixed, world-priced resource that is still extracted without the
group (the team lead, 2026-10-14), so the item's cell vectors carry its cells at zero.

Arms, each one change from the central (both readings): mining as other industries; corporate at the normal-return
share (0.37) at both readings; the high reading's corporate response at Power and Frerick's 2003-2013 normal-return
share (0.25) or at each industry's (their Table 1, 2011-2013); the plain wage share in place of the industry key;
federal tax on foreign-source income removed; business land at response 0 and 1; the case's wage key (status rules on)
in place of all wages; the floor (corporate_labor at the wage key). Beside: mining as other industries at the plain
wage share or with severance at 0, agriculture at 0, the top wages out or in their own
industries, the earnings key, other pooling, the structures base, BEA's housing split, management of companies kept,
lessors not reallocated, the for-profit key, other delta_L weights, published weights, no fill-in correction, the
fill-in at one rate. Also measured: mining's part by cell and tax component, and the residential parts of documentary
taxes and special assessments (outside the item) at the case's owner and tenant property keys.

Gates (exit 1, nothing written): every input's sha256; the CPS frame reproduces the builder's wage key (personal and
shared: totals 1e-9 relative, share and its SE 1e-9) on published weights; every wage-bearing industry code maps to
a cell; every cell with a tax amount has CPS wages; the row-4 mask, counts and factors are production_row4.json's
(main factor 1e-12, replicate range 1e-12) and the union sums to 39,712,493 (1e-3), its G3+ to the case's identified
G3+; cell wages add to the group and national totals; spreading the top wages keeps every group's total (1e-12);
generations add to the union; each fill-in method's change splits into the generations' (1e-9 bn) and the corrected
generations add to the union's change (1e-12); national.py's and case_keys.json's gates passed; the high reading's
corporate response is twice OTA's 2021 labor share; mining's cells carry no tax in the item; the plain-wage-share
ceiling reproduces -86.848983 / -80.976701 (1e-6); in the item file every block has group_bn = key_share x national,
generations adding to it and factor.union = key_share / plain_wage_share (1e-9), plain_wage_share the case's wage key,
the central's nationals the case's lines (1e-6) and its central and arms items.csv's (1e-9).

The item file (derived/item.json) follows main_case_2026_10_14's contract (item_job_capital.cjs): the case scales the
lane's industry key by the union's share of its own wage key, so plain_wage_share is that share and the factors are
key shares over it (the union and its generations) or over the lane's plain share (whites, Blacks). Every line's
response is {low, high}; group_bn is before the response and item_bn after it.

  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/job_capital_taxes_2026_10_14/job_capital.py
Outputs: derived/wages_by_industry.csv, derived/industry_crosswalk.csv, derived/items.csv, derived/summary.json,
derived/item.json.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
DERIVED = HERE / "derived"
CPS = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
CPS_SHA = "318845a2b5e0034eb2973898de1738f4df0025727de38499e7669cb9c0deef0b"
KEYS = FISCAL / "full_account_receipts_2026_09_20/derived/allocation_keys.csv"
KEYS_SHA = "942b63bd737a547394dc5b44f3dbd40f36137f52927e551d156ac0c2893c859c"
ROW4 = FISCAL / "main_case_candidate_2026_09_28/derived/production_row4.json"
ROW4_SHA = "69839e58a9601363562c0884ae1f7ba9ed7c25086cb3eb545e181806704ac3ac"
FILLIN = FISCAL / "cps_imputation_keys_2026_09_23/derived/status_combination_keys.csv"
FILLIN_SHA = "83b7e5517b2c643bf86b19240522ca5fa4f2cd24f152005bc7c2a8c2fc5f7c94"
COUNTIES = FISCAL / "receipt_side_long_run_2026_09_28/derived/counties.csv"
COUNTIES_SHA = "42fe3b780dfdf1a1523f46b21c737541f7c8c76eb5a3e377af67ffc03e42cda1"
V6 = FISCAL / "main_case_2026_10_07/derived/corrections.json"
V6_SHA = "f8d346aacf05bcdaed8495f870ba23ac6154ab3eaf34cc0bcf85861f0c85d091"
STACK = FISCAL / "generation_account_2026_09_24/derived/stack_by_generation.json"
STACK_SHA = "35039234a00eee6e7e08d2ab920ab40d369b542adc4b3eaac90f4d7d8a0404f1"
CROSSWALK = HERE / "inputs/census_industry_crosswalk.csv"
METHODS = ["b_hotdeck_union_matched", "b_matched_over_pooled"]   # main_case_2026_09_24/package.cjs METHODS
ALLOCS = ["personal", "shared"]
READINGS = ["low", "high"]   # the band's low end (corporate at 1) and high end (corporate at its normal-return share)
GENS = ["G1", "G2", "G3plus"]
# white / black: third-plus (native, both parents US-born) non-Hispanic white alone / Black alone, the lineage's whites;
# white_all / black_all: every nativity (the comparator lanes' groups).
GROUPS = ["union", "G1", "G2", "G3plus", "white", "black", "white_all", "black_all"]
REPS = [f"pwwgt{i}" for i in range(161)]
PERSON = ["PH_SEQ", "PPPOS", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY", "PEMNTVTY", "PEHSPNON", "PRDTRACE",
          "PRDTHSP", "MARSUPWT", "SPM_ID", "WSAL_VAL", "SEMP_VAL", "FRSE_VAL", "INDUSTRY", "LJCW", "PEIO1COW", "NOEMP"]
# The item file's lines (main_case_2026_10_14 item_job_capital.cjs) and this lane's.
ITEM_LINES = {"corporate": "corporate", "other_production_taxes": "other_production_taxes", "business_property": "c_and_i_property"}
ITEM_GROUPS = {"G1": "G1", "G2": "G2", "G3plus": "G3plus", "white_nh": "white", "black_nh": "black", "union": "union",
               "white_nh_all": "white_all", "black_nh_all": "black_all"}
NOEMP = ["niu", "under 10", "10-24", "25-99", "100-499", "500-999", "1000+"]   # ddl25.txt: employer size, all locations
US_AREA = [57, 60, 66, 69, 73, 78]
MILITARY = range(9670, 9891)
LINES = ["c_and_i_property", "other_production_taxes", "corporate"]
# A cell with fewer CPS wage earners than N_MIN takes its BEA sector's pooled share (a sector below N_MIN, every private
# cell's): oil and gas extraction has 38 earners, and two top-coded union records carry 74% of its union wages.
N_MIN = 100
# Wages at or above TOP (the public file caps each earnings source at $1,099,999: 233 civilian records, 5.2% of the
# wage bill, 15 of them the union's) are spread over the cells as all such wages are, at each group's own share of
# them: in mining the three records at the cap are all the union's and carry 9.6% of the sector's wages.
TOP = 1e6
SECTOR = {"111CA": "agriculture", "113FF": "agriculture", "211": "mining", "212": "mining", "213": "mining", "22": "utilities",
          "23": "construction", **{c: "durable" for c in ("321", "327", "331", "332", "333", "334", "335", "3361MV", "3364OT", "337", "339")},
          **{c: "nondurable" for c in ("311FT", "313TT", "315AL", "322", "323", "324", "325", "326")}, "42": "wholesale",
          **{c: "retail" for c in ("441", "445", "452", "4A0")},
          **{c: "transportation" for c in ("481", "482", "483", "484", "485", "486", "487OS", "493")},
          **{c: "information" for c in ("511", "512", "513", "514")}, **{c: "finance" for c in ("521CI", "523", "524")},
          "ORE": "real_estate", "532RL": "real_estate", **{c: "professional" for c in ("5411", "5415", "5412OP")},
          "55": "management", "561": "administrative", "562": "administrative", "61": "education",
          **{c: "health" for c in ("621", "622", "623", "624")}, "711AS": "arts", "713": "arts", "721": "accommodation_food",
          "722": "accommodation_food", "81": "other_services", "GOVF": "government", "GOVSL": "government", "HH814": "households",
          "RESIDENTIAL": "none", "NOIND": "none"}

GATES: list[dict] = []


def gate(name: str, ok: bool, detail: str = "") -> None:
    GATES.append({"gate": name, "passed": bool(ok), "detail": detail})
    print(f"  {'✓' if ok else '✗'} {name}{f' ({detail})' if detail else ''}")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def checked(path: Path, digest: str) -> Path:
    if not path.exists() or sha256(path) != digest:
        raise SystemExit(f"[BLOCKED] missing or stale source: {path}")
    return path


def se(values: np.ndarray) -> float:
    """SDR standard error over the 160 replicates (column 0 is the main estimate)."""
    return float(np.sqrt(4 / 160 * np.square(values[..., 1:] - values[..., :1]).sum(axis=-1)))


def load_frame():
    with zipfile.ZipFile(checked(CPS, CPS_SHA)) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=PERSON)
        r = pd.read_csv(z.open("asec_csv_repwgt_2025.csv"), usecols=["h_seq", "PPPOS"] + REPS)
        hh = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "GESTFIPS"])
    r = r.rename(columns={"h_seq": "PH_SEQ"})
    d = d.merge(r, on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one")
    gate("every person has 161 replicate weights", not d[REPS].isna().any().any())
    gate("pwwgt0 is MARSUPWT / 100 (0.01)", float((d.MARSUPWT / 100 - d.pwwgt0).abs().max()) < 0.01)
    d = d.merge(hh, left_on="PH_SEQ", right_on="H_SEQ", how="left", validate="many_to_one")
    gate("every person has a household state", not d.GESTFIPS.isna().any())
    d = d.sort_values(["SPM_ID", "PPPOS"]).reset_index(drop=True)
    return d


def masks(d: pd.DataFrame) -> dict:
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    parents_us = (d.PEFNTVTY.isin(US_AREA) & d.PEMNTVTY.isin(US_AREA)).to_numpy()
    parent_mexico = (d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)).to_numpy()
    civ = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    nh_white = d.PEHSPNON.eq(2).to_numpy() & d.PRDTRACE.eq(1).to_numpy()
    nh_black = d.PEHSPNON.eq(2).to_numpy() & d.PRDTRACE.eq(2).to_numpy()
    g = {"G1": d.PRCITSHP.isin([4, 5]).to_numpy() & d.PENATVTY.eq(303).to_numpy(),
         "G2": native & parent_mexico,
         "G3plus": native & parents_us & d.PRDTHSP.eq(1).to_numpy(),
         "white": native & parents_us & nh_white, "black": native & parents_us & nh_black,
         "white_all": nh_white, "black_all": nh_black}
    g = {k: v & civ for k, v in g.items()}
    g["union"] = g["G1"] | g["G2"] | g["G3plus"]
    g["civilian"] = civ
    return g


def row4_weights(d: pd.DataFrame, m: dict, row4: dict) -> np.ndarray:
    """Every weight column with the Mexico-born outside California and Texas raked to ACS 2024 by citizenship."""
    w = d[REPS].to_numpy(float)
    outside = ~d.GESTFIPS.isin([6, 48]).to_numpy()
    moved = np.zeros(len(d), bool)
    for label, status in (("naturalized", 4), ("noncitizen", 5)):
        mask = d.PENATVTY.eq(303).to_numpy() & d.PRCITSHP.eq(status).to_numpy() & outside
        ref = row4["row4_factors"][label]
        cps = w[mask].sum(axis=0)
        f = ref["acs_population"] / cps
        gate(f"row 4 {label}: records, CPS population and main factor are production_row4.json's",
             int(mask.sum()) == ref["records"] and abs(cps[0] - ref["cps_population"]) < 1e-6 and abs(f[0] - ref["factor"]) < 1e-12,
             f"{int(mask.sum())} records, factor {f[0]:.12f}")
        gate(f"row 4 {label}: the replicate factors' range is production_row4.json's (1e-12)",
             abs(f[1:].min() - ref["replicate_factor_range"][0]) < 1e-12 and abs(f[1:].max() - ref["replicate_factor_range"][1]) < 1e-12)
        w[mask] *= f
        moved |= mask
    gate("row 4 moves no civilian outside the union", not np.any(moved & m["civilian"] & ~m["union"]))
    head = float(w[m["union"], 0].sum())
    gate("the union on row 4 is the account's 39,712,493 (1e-3)", abs(head - row4["populations"]["row4"]) < 1e-3, f"{head:,.3f}")
    return w


def cell_of(d: pd.DataFrame, crosswalk: pd.DataFrame) -> np.ndarray:
    xw = dict(zip(crosswalk.census_code.astype(int), crosswalk.bea_industry))
    code = d.INDUSTRY.to_numpy()
    cell = np.array([xw.get(int(c), "UNMAPPED") if c > 0 else "NOIND" for c in code], dtype=object)
    gov = cell == "GOV"
    federal_code = np.isin(code, list(MILITARY)) | (code == 6370)
    cell[gov & federal_code] = "GOVF"
    cell[gov & ~federal_code] = "GOVSL"
    ljcw = d.LJCW.to_numpy()
    cell[ljcw == 2] = "GOVF"
    cell[np.isin(ljcw, [3, 4])] = "GOVSL"
    return cell


def cell_wages(wage, cellidx, n_cells, members, w, unit, n_unit, alloc):
    """(n_cells x 161) wages of `members` by the earner's cell: own wages (personal) or the unit's wages split
    equally among its members (shared)."""
    out = np.zeros((n_cells, w.shape[1]))
    if alloc == "personal":
        k = members & (wage > 0)
        np.add.at(out, cellidx[k], wage[k, None] * w[k])
        return out
    gu = np.zeros((n_unit.size, w.shape[1]))
    np.add.at(gu, unit[members], w[members])
    gu /= n_unit[:, None]
    k = wage > 0
    np.add.at(out, cellidx[k], wage[k, None] * gu[unit[k]])
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-dir", type=Path, default=DERIVED)
    args = ap.parse_args()

    print("[upstream gates]")
    nat_json = json.loads((DERIVED / "national.json").read_text())
    case = json.loads((DERIVED / "case_keys.json").read_text())
    gate("national.py's gates all passed", all(g["passed"] for g in nat_json["gates"]), f"{len(nat_json['gates'])} gates")
    gate("case_keys.cjs's gates all passed", all(g["passed"] for g in case["gates"]), f"{len(case['gates'])} gates")
    nat = pd.read_csv(DERIVED / "national_by_industry.csv").set_index("cell")
    cells = list(nat.index)
    gate("national lines are case_keys.json's (1e-6 bn)", all(abs(nat[f"{ln}_bn"].sum() - case["national_bn"][ln]) < 1e-6 for ln in LINES))

    print("\n[CPS frame]")
    d = load_frame()
    m = masks(d)
    crosswalk = pd.read_csv(CROSSWALK, dtype={"census_code": str})
    gate("the crosswalk names one cell per code, all of them national.py's cells or GOV / NOIND",
         crosswalk.census_code.is_unique and set(crosswalk.bea_industry) <= set(cells) | {"GOV", "NOIND"})
    cell = cell_of(d, crosswalk)
    wage = d.WSAL_VAL.clip(lower=0).to_numpy(float)
    unmapped = sorted(set(d.INDUSTRY[(cell == "UNMAPPED") & (wage > 0)]))
    gate("every wage-bearing industry code maps to a cell", not unmapped, str(unmapped[:10]))
    all_cells = cells + ["NOIND"]
    cellidx = np.array([all_cells.index(c) for c in cell])
    n_cells = len(all_cells)
    unit = pd.factorize(d.SPM_ID, sort=True)[0]
    n_unit = np.bincount(unit).astype(float)
    w_pub = d[REPS].to_numpy(float)

    # The builder's wage key on published weights: totals, shares and SEs.
    keys = pd.read_csv(checked(KEYS, KEYS_SHA)).query("allocation_key == 'wage'").set_index("allocation")
    pub = {}
    for a in ALLOCS:
        grp = cell_wages(wage, cellidx, n_cells, m["union"], w_pub, unit, n_unit, a)
        natl = cell_wages(wage, cellidx, n_cells, m["civilian"], w_pub, unit, n_unit, a)
        g_tot, n_tot = grp.sum(axis=0), natl.sum(axis=0)
        share = g_tot / n_tot
        k = keys.loc[a]
        gate(f"{a}: the union's wage total is the builder's (1e-9 relative)", abs(g_tot[0] / k.target_key_total - 1) < 1e-9,
             f"{g_tot[0]:,.4f}")
        gate(f"{a}: the national civilian wage total is the builder's (1e-9 relative)", abs(n_tot[0] / k.national_key_total - 1) < 1e-9)
        gate(f"{a}: the wage share and its SE are the builder's (1e-9)", abs(share[0] - k.target_key_share) < 1e-9
             and abs(se(share) - k.target_share_sampling_se) < 1e-9, f"{share[0]:.9f} (SE {se(share):.9f})")
        pub[a] = {"group": grp, "national": natl}
    noind_bn = {a: float(pub[a]["national"][-1, 0] / 1e9) for a in ALLOCS}

    print("\n[row 4]")
    row4 = json.loads(checked(ROW4, ROW4_SHA).read_text())
    w4 = row4_weights(d, m, row4)
    v6 = json.loads(checked(V6, V6_SHA).read_text())
    counts = v6["meta"]["lineage"]["counts"]
    members = v6["meta"]["lineage"]["members"]
    g3_head = float(w4[m["G3plus"], 0].sum())
    gate("the union's G3+ on row 4 is the case's identified G3+ (1e-3)", abs(g3_head - counts["identified_g3plus"]) < 1e-3, f"{g3_head:,.3f}")
    gate("the case's account union is row 4's (1e-3)", abs(counts["account_union"] - row4["populations"]["row4"]) < 1e-3)

    print("\n[fill-in correction]")
    # The case's fill-in correction of the union's wages (cps_imputation_keys: the wage key's change under its two
    # fill-in methods, averaged), split across the generations as the case splits the same methods' change on the wage
    # key (generation_account_2026_09_24 stack_by_generation.json, components D_<method>, convention a): generation G's
    # wages move by rc x d_G x (union wages / G's wages), so the generations' changes add to the union's rc.
    fill = pd.read_csv(checked(FILLIN, FILLIN_SHA)).query("key == 'wage'").set_index(["method", "allocation"])
    rc = {a: float(np.mean([fill.loc[(meth, a), "rel_change"] for meth in METHODS])) for a in ALLOCS}
    rc_se = {a: float(np.mean([fill.loc[(meth, a), "rel_change_se"] for meth in METHODS])) for a in ALLOCS}
    stack = json.loads(checked(STACK, STACK_SHA).read_text())
    comp = [stack["components"][f"D_{meth}"] for meth in METHODS]
    cl = lambda c, G, a: c["a"][G]["receipts"]["corporate_labor"][a] if G in GENS else c["union"]["union"]["receipts"]["corporate_labor"][a]
    def group_wage_cells(wvec, w, a, groups, pool_top=True):
        """Cell wages (n_cells x 161) of the groups and the nation from the wage vector wvec on the weights w; with
        pool_top, each group's wages at or above TOP are spread over the cells as the nation's such wages are."""
        out = {"national": cell_wages(wvec, cellidx, n_cells, m["civilian"], w, unit, n_unit, a)}
        hi = wvec >= TOP
        if not (pool_top and hi.any()):
            return out | {g: cell_wages(wvec, cellidx, n_cells, m[g], w, unit, n_unit, a) for g in groups}
        lo_v, hi_v = np.where(hi, 0.0, wvec), np.where(hi, wvec, 0.0)
        nat_hi = cell_wages(hi_v, cellidx, n_cells, m["civilian"], w, unit, n_unit, a)
        spread = nat_hi / nat_hi.sum(axis=0)
        return out | {g: cell_wages(lo_v, cellidx, n_cells, m[g], w, unit, n_unit, a)
                      + spread * cell_wages(hi_v, cellidx, n_cells, m[g], w, unit, n_unit, a).sum(axis=0) for g in groups}

    raw, direct, d_split, corr, top_share = {}, {}, {}, {}, {}
    for a in ALLOCS:
        raw[a] = group_wage_cells(wage, w4, a, GROUPS)
        direct[a] = group_wage_cells(wage, w4, a, GROUPS, pool_top=False)
        hi_cells = group_wage_cells(np.where(wage >= TOP, wage, 0.0), w4, a, ["union"], pool_top=False)
        top_share[a] = float(hi_cells["union"][:, 0].sum() / hi_cells["national"][:, 0].sum())
        moved = max(abs(raw[a][g].sum(axis=0) / direct[a][g].sum(axis=0) - 1).max() for g in GROUPS)
        gate(f"{a}: spreading the wages at or above $1M keeps every group's total in every weight column (1e-12)", moved < 1e-12, f"{moved:.1e}")
        parts = raw[a]["G1"] + raw[a]["G2"] + raw[a]["G3plus"]
        gap = float(np.abs(parts - raw[a]["union"]).max() / np.abs(raw[a]["union"]).max())
        gate(f"{a}: the generations add to the union in every cell and weight column (1e-12 of the largest cell)", gap < 1e-12,
             f"{gap:.1e}")
        raw[a]["union"] = parts
        split_gap = max(abs(sum(cl(c, G, a) for G in GENS) - cl(c, "union", a)) for c in comp)
        gate(f"{a}: each fill-in method's change on the wage key splits into the generations' (1e-9 bn)", split_gap < 1e-9, f"{split_gap:.1e}")
        d_union = float(np.mean([cl(c, "union", a) for c in comp]))
        d_split[a] = {G: float(np.mean([cl(c, G, a) for c in comp])) / d_union for G in GENS}
        w_u = float(raw[a]["union"][:, 0].sum())
        corr[a] = {g: 1 + rc[a] * d_split[a][g] * w_u / float(raw[a][g][:, 0].sum()) if g in GENS else 1.0 for g in GROUPS}
        print(f"  {a}: rc {rc[a]:+.6f}; generations' parts {', '.join(f'{G} {d_split[a][G]:+.4f}' for G in GENS)}; "
              f"factors {', '.join(f'{G} {corr[a][G]:.6f}' for G in GENS)}")

    def group_cells(wvec, w, a, fill_in=True, groups=GROUPS, pool_top=True):
        """group_wage_cells with the fill-in correction on the generations (when fill_in), the union their sum."""
        out = group_wage_cells(wvec, w, a, [g for g in groups if g != "union"], pool_top)
        for g in groups:
            if g != "union" and fill_in:
                out[g] = out[g] * corr[a][g]
        out["union"] = out["G1"] + out["G2"] + out["G3plus"]
        return out

    wages = {a: {g: raw[a][g] * corr[a][g] for g in GROUPS if g != "union"} for a in ALLOCS}
    for a in ALLOCS:
        wages[a]["union"] = wages[a]["G1"] + wages[a]["G2"] + wages[a]["G3plus"]
        wages[a]["national"] = raw[a]["national"]
        got = float(wages[a]["union"][:, 0].sum() / raw[a]["union"][:, 0].sum() - 1)
        gate(f"{a}: the corrected generations add to the union's fill-in change (1e-12)", abs(got - rc[a]) < 1e-12, f"{got:+.9f}")
    tax_cells = [c for c in cells if c != "RESIDENTIAL" and any(nat.loc[c, f"{ln}_bn"] > 0 for ln in LINES)]
    missing = [c for c in tax_cells if wages["personal"]["national"][all_cells.index(c), 0] <= 0
               or wages["shared"]["national"][all_cells.index(c), 0] <= 0]
    gate("every cell with a tax amount has national CPS wages under both allocations", not missing, str(missing))

    # Shares by cell (n_cells x 161): own, or pooled over the sector (thin cells), the RESIDENTIAL cell and NOIND at zero.
    gate("every cell has a sector", set(all_cells) <= set(SECTOR))
    earners = m["civilian"] & (wage > 0)
    n_rec = np.bincount(cellidx[earners], minlength=n_cells)
    sector_of = np.array([SECTOR[c] for c in all_cells])
    private_cells = np.flatnonzero(~np.isin(sector_of, ["government", "households", "none"]))
    pools = {}

    def pooled_index(n_min):
        if n_min not in pools:
            out = []
            for i in range(n_cells):
                if n_rec[i] >= n_min or sector_of[i] == "none":
                    out.append(np.array([i]))
                    continue
                sec = np.flatnonzero(sector_of == sector_of[i])
                out.append(sec if n_rec[sec].sum() >= n_min else private_cells)
            pools[n_min] = out
        return pools[n_min]

    def shares(a, g, n_min=N_MIN, src=None):
        src = src or wages[a]
        natl, grp = src["national"], src[g]
        out = np.zeros_like(natl)
        for i, idx in enumerate(pooled_index(n_min)):
            den = natl[idx].sum(axis=0)
            out[i] = np.divide(grp[idx].sum(axis=0), den, out=np.zeros_like(den), where=den > 0)
        return out

    thin = [all_cells[i] for i in range(n_cells) if len(pooled_index(N_MIN)[i]) > 1]
    print(f"  cells pooled at N_MIN {N_MIN}: {', '.join(thin)}")


    print("\n[responses]")
    land = nat_json["land"]
    lam_b, tau = land["lambda_b"], nat_json["tpp"]["tau_of_business_line"]
    cty = pd.read_csv(checked(COUNTIES, COUNTIES_SHA), dtype={"county": str})
    gate("counties: every land share is positive and every implied land-price fall in [0, 1]",
         bool((cty.land_share > 0).all() and (cty.fall_lr_metro / cty.land_share).between(0, 1 + 1e-12).all()))
    dl_c = (cty.fall_lr_metro / cty.land_share).to_numpy()
    dl_nat_c = (cty.fall_lr_national / cty.land_share).to_numpy()
    delta = {"group_population": float(np.average(dl_c, weights=cty.group_pop)),
             "group_owner_tax": float(np.average(dl_c, weights=cty.group_owner_tax)),
             "national_share_group_population": float(np.average(dl_nat_c, weights=cty.group_pop))}
    r_b = {k: 1 - lam_b * (1 - v) for k, v in delta.items()}
    resp = {"central": tau + (1 - tau) * r_b["group_population"]}
    normal = nat_json["normal_return"]
    pf = normal["power_frerick"]
    nr_tp5, nr_pf = normal["share"], pf["2003_2013"]
    gate("the high reading's corporate response is TP-5's normal-return share, twice OTA's 2021 labor share (1e-12)",
         abs(nr_tp5 - 2 * normal["ota_2021_labor_share_pct"] / 100) < 1e-12, f"{nr_tp5}")
    # The band's two readings (the team lead, 2026-10-14): corporate tax leaves whole at the low end and only its
    # normal-return share at the high end; business property and other production taxes respond alike at both.
    LINE_RESP = {"low": {"c_and_i_property": resp["central"], "other_production_taxes": 1.0, "corporate": 1.0},
                 "high": {"c_and_i_property": resp["central"], "other_production_taxes": 1.0, "corporate": nr_tp5}}

    def with_resp(**kw):
        """LINE_RESP with some lines' responses replaced: a number at both readings, or {low, high}."""
        return {rd: LINE_RESP[rd] | {k: (v[rd] if isinstance(v, dict) else v) for k, v in kw.items()} for rd in READINGS}

    print(f"  lambda_b {lam_b:.6f}, tau {tau:.6f}, delta_L {delta['group_population']:.6f}, r_b {r_b['group_population']:.6f}, "
          f"business property response {resp['central']:.6f}; corporate {LINE_RESP['low']['corporate']} low / {nr_tp5} high")

    # The item's cell vectors: each line's tax by cell (national.py), the residential parts and NOIND at zero. Mining's
    # cells respond at 0 on every line at both readings, so the item's vectors carry them at zero; `full` keeps them
    # for the arm that prices mining as other industries.
    num_cols = [c for c in nat.columns if c.endswith(("_bn", "_mn"))]
    vec = {c: np.append(nat[c].to_numpy(float), 0.0) for c in num_cols}   # NOIND carries no tax
    ri = all_cells.index("RESIDENTIAL")
    for k in vec:
        if not k.endswith("_mn"):
            vec[k][ri] = 0.0                                                    # residential parts are outside the item
    full = {k: v.copy() for k, v in vec.items()}
    mining = np.flatnonzero(sector_of == "mining")
    responds = np.ones(n_cells)
    responds[mining] = 0.0
    for k in vec:
        if k.endswith("_bn"):
            vec[k] = vec[k] * responds
    pf_cell = np.append(nat["pf_normal_share"].to_numpy(float), nr_pf)
    LINE_COL = {"c_and_i_property": "c_and_i_property_bn", "other_production_taxes": "other_production_taxes_bn", "corporate": "corporate_bn"}
    nat_lines = {ln: vec[c] for ln, c in LINE_COL.items()}
    full_lines = {ln: full[c] for ln, c in LINE_COL.items()}
    national_in_item = {ln: float(t.sum()) for ln, t in nat_lines.items()}
    keep_cells = np.flatnonzero(responds > 0)
    gate("mining's cells carry no tax in the item's vectors, and every other cell keeps its own",
         all(not nat_lines[ln][mining].any() and np.array_equal(nat_lines[ln][keep_cells], full_lines[ln][keep_cells]) for ln in LINES),
         ", ".join(f"{ln} {float(full_lines[ln][mining].sum()):.3f} bn out" for ln in LINES))

    rows = []
    nan = float("nan")

    def record(row, label, a, parts, rsp=None, note=""):
        """Rows for each reading and line, and each reading's sum. parts = {line: (target (161,), base_bn)} before the
        response, or {reading: {line: ...}} when the target moves with the reading; rsp = {reading: {line: response}}.
        Returns {reading: total (161,)}, negative = the group's net cost falls."""
        rsp = rsp or LINE_RESP
        out = {}
        for rd in READINGS:
            p = parts[rd] if rd in parts else parts
            tot = np.zeros(161)
            for ln, (tg, base) in p.items():
                v = -tg * rsp[rd][ln]
                rows.append({"row": row, "reading": rd, "label": label, "allocation": a, "line": ln, "base_bn": base,
                             "response": rsp[rd][ln], "group_share": float(tg[0] / base) if base else 0.0, "value_bn": float(v[0]),
                             "se_bn": se(v), "note": note})
                tot += v
            rows.append({"row": row, "reading": rd, "label": label, "allocation": a, "line": "all",
                         "base_bn": float(sum(b for _, b in p.values())), "response": nan, "group_share": nan,
                         "value_bn": float(tot[0]), "se_bn": se(tot), "note": note})
            out[rd] = tot
        return out

    def parts_of(s, lines=None):
        """{line: (the group's target (161,), the base)} from an effective share matrix s (cells x 161)."""
        return {ln: (s.T @ t, float(t.sum())) for ln, t in (lines or nat_lines).items()}

    def line_parts(a, lines=None, g="union", n_min=N_MIN, src=None):
        return parts_of(shares(a, g, n_min, src), lines)

    central = {a: record("central", "central", a, line_parts(a)) for a in ALLOCS}

    trim = np.where(wage >= 1e6, 0.0, wage)
    trimmed = {a: group_cells(trim, w4, a, groups=GENS) for a in ALLOCS}
    # Earnings: wages plus self-employment and farm income (positive parts), by the longest job's industry.
    earn = (d.WSAL_VAL.clip(lower=0) + d.SEMP_VAL.clip(lower=0) + d.FRSE_VAL.clip(lower=0)).to_numpy(float)
    earned = {a: group_cells(earn, w4, a, groups=GENS) for a in ALLOCS}
    land_0 = tau + (1 - tau) * (1 - lam_b)
    pf_corp = nat_lines["corporate"] * pf_cell
    nat_pf = float(pf_corp.sum() / nat_lines["corporate"].sum())   # the cells' corporate-weighted Table 1 share
    pf_corp_tp5 = pf_corp * nr_tp5 / nat_pf                          # the same industry pattern at TP-5's level
    agri = (sector_of != "agriculture").astype(float)
    arms = {}
    for a in ALLOCS:
        s_u = shares(a, "union")
        lp = parts_of(s_u)
        arms[("mining_as_other_industries", a)] = record("arm_mining_as_other_industries", "mining's three taxes respond as other industries' do",
                                                         a, parts_of(s_u, full_lines))
        arms[("normal_return_share", a)] = record("arm_normal_return_share", "corporate at TP-5's normal-return share (0.37) at both readings",
                                                  a, lp, with_resp(corporate=nr_tp5))
        arms[("normal_return_share_0_25", a)] = record("arm_normal_return_share_0_25", "the high reading's corporate response at Power and "
                                                       "Frerick's 2003-2013 normal-return share (0.25)", a, lp,
                                                       with_resp(corporate={"low": 1.0, "high": nr_pf}))
        arms[("normal_return_share_by_industry", a)] = record(
            "arm_normal_return_share_by_industry", "the high reading's corporate response at each industry's normal-return share (Power and "
            "Frerick Table 1, 2011-2013)", a, {"low": lp, "high": lp | {"corporate": (s_u.T @ pf_corp, float(pf_corp.sum()))}},
            with_resp(corporate=1.0), "high reading: each cell's corporate tax times its industry's share, at response 1")
        record("beside_normal_return_share_by_industry_tp5", "the high reading's corporate response at each industry's Power and Frerick share "
               "scaled to TP-5's level (the cells' corporate-weighted mean 0.37)", a,
               {"low": lp, "high": lp | {"corporate": (s_u.T @ pf_corp_tp5, float(pf_corp_tp5.sum()))}}, with_resp(corporate=1.0),
               "[INFERENCE] TP-5's level with Power and Frerick's industry pattern")
        arms[("foreign_removed", a)] = record("arm_foreign_removed", "federal tax on foreign-source income removed", a,
                                              parts_of(s_u, nat_lines | {"corporate": vec["corporate_ex_foreign_bn"]}))
        arms[("land_0", a)] = record("arm_land_0", "business land at response 0", a, lp, with_resp(c_and_i_property=land_0))
        arms[("land_1", a)] = record("arm_land_1", "business land at response 1", a, lp, with_resp(c_and_i_property=1.0))
        # Beside rows.
        record("beside_mgmt_own", "management of companies kept at NAICS 55", a, parts_of(s_u, nat_lines | {"corporate": vec["corporate_mgmt_own_bn"]}))
        record("beside_no_lessor_realloc", "lessors' taxes kept with the lessors", a,
               parts_of(s_u, nat_lines | {"corporate": vec["corporate_no_lessor_realloc_bn"],
                                          "c_and_i_property": vec["c_and_i_property_no_lessor_realloc_bn"]}))
        record("beside_bea_housing_split", "business property at BEA's housing split (396.137bn)", a,
               parts_of(s_u, nat_lines | {"c_and_i_property": vec["c_and_i_property_bea_housing_split_bn"]}))
        for k in ("group_owner_tax", "national_share_group_population"):
            record(f"beside_delta_{k}", f"delta_L weighted by {k.replace('_', ' ')}", a, lp, with_resp(c_and_i_property=tau + (1 - tau) * r_b[k]))
        record("beside_rb_whole_line", "r_b on the whole business property line (no TPP split)", a, lp,
               with_resp(c_and_i_property=r_b["group_population"]))
        # Mining as other industries with its cells at the union's plain wage share: 359 CPS earners, and its only three
        # records at $1M or more are union members.
        s_min = s_u.copy()
        s_min[mining] = wages[a]["union"].sum(axis=0) / wages[a]["national"].sum(axis=0)
        record("beside_mining_plain_share", "mining as other industries, its cells at the union's plain wage share", a, parts_of(s_min, full_lines))
        record("beside_mining_severance_0", "mining as other industries but severance at 0 (the reserve stays in the ground)", a,
               parts_of(s_u, full_lines | {"other_production_taxes": full_lines["other_production_taxes"] - full["otp_severance_bn"]}))
        # Agriculture at 0 as well: land is its fixed factor and its crops are world-priced, mining's reason.
        record("beside_agriculture_0", "agriculture also at response 0 (its land fixed, its crops world-priced)", a,
               parts_of(s_u, {ln: t * agri for ln, t in nat_lines.items()}))
        record("beside_top_wages_out", "wage records at $1M or more out of both sides of every share", a, line_parts(a, src=trimmed[a]))
        record("beside_top_wages_own_industry", "wages at $1M or more in their own records' industries (the top not spread)", a,
               line_parts(a, src={g: direct[a][g] * corr[a][g] for g in GENS} | {
                   "union": sum(direct[a][G] * corr[a][G] for G in GENS), "national": direct[a]["national"]}))
        record("beside_earnings_key", "earnings (wages plus self-employment and farm income) in place of wages", a, line_parts(a, src=earned[a]))
        record("beside_no_pooling", "no pooling: every cell's own share", a, line_parts(a, n_min=0))
        record("beside_pool_300", "thin cells pooled below 300 earners", a, line_parts(a, n_min=300))

    # Structures base for business property: nonprofit structures out (each cell's nonprofit share of private wages,
    # current job's class, scaled to FA's nonprofit total), then structures alone and with equipment at tau.
    cow = d.PEIO1COW.to_numpy()
    private = np.isin(cow, [4, 5, 6, 7]) & (wage > 0) & m["civilian"] & ~np.isin(cell, ["GOVF", "GOVSL", "NOIND"])
    npw = np.zeros(n_cells)
    allw = np.zeros(n_cells)
    np.add.at(allw, cellidx[private], wage[private] * w4[private, 0])
    np.add.at(npw, cellidx[private & (cow == 5)], wage[private & (cow == 5)] * w4[private & (cow == 5), 0])
    np_share = np.divide(npw, allw, out=np.zeros(n_cells), where=allw > 0)
    sb = nat_json["structures_base"]
    S, E = vec["structures_stock_mn"], vec["equipment_stock_mn"]
    k_s = sb["nonprofit_structures_mn"] / float((S * np_share).sum())
    k_e = sb["nonprofit_equipment_mn"] / float((E * np_share).sum())
    gate("the nonprofit cut stays inside each cell's stock (scaled share <= 1)", bool((np_share * k_s <= 1).all() and (np_share * k_e <= 1).all()),
         f"scale {k_s:.3f} / {k_e:.3f}")
    S_tax, E_tax = S * (1 - np_share * k_s), E * (1 - np_share * k_e)
    ci = nat_json["national_bn"]["c_and_i_property"]
    ci_struct = ci * S_tax / S_tax.sum() * responds
    ci_struct_eq = ci * ((1 - tau) * S_tax / S_tax.sum() + tau * E_tax / E_tax.sum()) * responds
    keep = cow != 5
    for a in ALLOCS:
        s_u = shares(a, "union")
        record("beside_structures", "business property by private nonresidential structures (nonprofit out)", a,
               parts_of(s_u, nat_lines | {"c_and_i_property": ci_struct}))
        record("beside_structures_equipment", "business property by structures, and equipment at tau", a,
               parts_of(s_u, nat_lines | {"c_and_i_property": ci_struct_eq}))
        # The for-profit key (nonprofit current jobs out of both sides in private cells); published weights, no fill-in
        # correction and the fill-in at one rate for every generation, for reference.
        record("beside_for_profit", "the for-profit key (nonprofit current jobs out)", a,
               line_parts(a, src=group_cells(np.where(keep, wage, 0.0), w4, a, groups=GENS)))
        record("beside_published_weights", "published CPS weights (40.90M), not row 4", a, line_parts(a, src=group_cells(wage, w_pub, a, groups=GENS)))
        record("beside_no_fill_in", "without the fill-in correction", a, line_parts(a, src=raw[a]))
        record("beside_fill_in_one_rate", "the fill-in correction at the union's rate for every generation", a,
               parts_of(shares(a, "union", N_MIN, raw[a]) * (1 + rc[a])))

    # The plain wage share: the case's employer_hi key (Sept 27, specifications 48 shared and 11 personal; the
    # receipt lane's ceiling, every line at 1), v6's key at the same specifications, and this lane's own plain share.
    total3 = case["national_bn"]["total"]
    s27 = case["sept27"]["employer_hi_share"]
    ceiling = {"spec48_shared": -s27["spec48"] * total3, "spec11_personal": -s27["spec11"] * total3}
    gate("the plain-wage-share ceiling reproduces the receipt lane's -86.848983 / -80.976701 (1e-6)",
         abs(ceiling["spec48_shared"] + 86.848983) < 1e-6 and abs(ceiling["spec11_personal"] + 80.976701) < 1e-6,
         f"{ceiling['spec48_shared']:.6f} / {ceiling['spec11_personal']:.6f}")
    v6s = case["v6"]["specs"]
    v6_share = {"spec48_shared": v6s["48"]["lines"]["employer_hi"]["share"], "spec11_personal": v6s["11"]["lines"]["employer_hi"]["share"],
                "spec16_personal": v6s["16"]["lines"]["employer_hi"]["share"]}
    plain = {}
    for a in ALLOCS:
        g_t, n_t = wages[a]["union"].sum(axis=0), wages[a]["national"].sum(axis=0)
        plain[a] = g_t / n_t
    for a, spec in (("shared", "spec48_shared"), ("personal", "spec11_personal")):
        rows.append({"row": "ceiling_sept27", "reading": "both", "label": "the case's employer_hi key (Sept 27), all three lines at 1: "
                     "the receipt lane's ceiling", "allocation": a, "line": "all", "base_bn": total3, "response": 1.0,
                     "group_share": s27[spec.split("_")[0]], "value_bn": ceiling[spec], "se_bn": nan,
                     "note": "receipt_side_long_run_2026_09_28 probe.json item4"})
        rows.append({"row": "ceiling_v6", "reading": "both", "label": "v6's employer_hi key, all three lines at 1", "allocation": a,
                     "line": "all", "base_bn": total3, "response": 1.0, "group_share": v6_share[spec],
                     "value_bn": -v6_share[spec] * total3, "se_bn": nan, "note": "case_keys.json v6"})
        rows.append({"row": "ceiling_lane", "reading": "both", "label": "this lane's plain wage share (row 4, fill-in), all three lines at 1",
                     "allocation": a, "line": "all", "base_bn": total3, "response": 1.0, "group_share": float(plain[a][0]),
                     "value_bn": float(-plain[a][0] * total3), "se_bn": se(-plain[a] * total3), "note": ""})
    floor = case["sept27"]["floor_corporate_labor_bn"]
    for a, spec in (("shared", "spec48"), ("personal", "spec11")):
        rows.append({"row": "floor_corporate_labor", "reading": "both", "label": "the floor: CBO's 25% labor share at the wage key (Sept 27)",
                     "allocation": a, "line": "corporate", "base_bn": case["national_bn"]["corporate"] * 0.25, "response": 1.0,
                     "group_share": nan, "value_bn": floor[spec], "se_bn": nan, "note": "receipt_side_long_run_2026_09_28 trace.csv corporate_labor"})

    # Generations and whites: amounts, wages, tax per wage dollar, per person, at each reading.
    tg_by = {a: {g: {ln: shares(a, g).T @ t for ln, t in nat_lines.items()} for g in GROUPS} for a in ALLOCS}
    gen = {rd: {a: {} for a in ALLOCS} for rd in READINGS}
    for a in ALLOCS:
        for g in GROUPS:
            w_g = wages[a][g].sum(axis=0)
            persons = float(w4[m[g], 0].sum())
            for rd in READINGS:
                by_line = {ln: -tg_by[a][g][ln] * LINE_RESP[rd][ln] for ln in LINES}
                tot = sum(by_line.values())
                gen[rd][a][g] = {"persons": persons, "wages_bn": float(w_g[0] / 1e9), "item_bn": float(tot[0]), "item_se_bn": se(tot),
                                 "by_line_bn": {ln: float(v[0]) for ln, v in by_line.items()},
                                 "per_wage_dollar": float(-tot[0] / (w_g[0] / 1e9)),
                                 "per_wage_dollar_by_line": {ln: float(-v[0] / (w_g[0] / 1e9)) for ln, v in by_line.items()},
                                 "per_wage_dollar_se": se(-tot / (w_g / 1e9)), "per_person_usd": float(tot[0] * 1e9 / persons)}
        for rd in READINGS:
            parts = sum(gen[rd][a][G]["item_bn"] for G in GENS)
            gate(f"{rd}, {a}: the generations' items add to the union's, and the union's is the central (1e-9 bn)",
                 abs(parts - gen[rd][a]["union"]["item_bn"]) < 1e-9 and abs(gen[rd][a]["union"]["item_bn"] - central[a][rd][0]) < 1e-9)
    # Where the item comes from: each sector's part of the central.
    by_sector = {rd: {} for rd in READINGS}
    for a in ALLOCS:
        s_c = shares(a, "union")[:, 0]
        for rd in READINGS:
            part = s_c * sum(nat_lines[ln] * LINE_RESP[rd][ln] for ln in LINES)
            by_sector[rd][a] = {sec: float(-part[sector_of == sec].sum()) for sec in dict.fromkeys(sector_of)}
            gate(f"{rd}, {a}: the sectors' parts add to the central (1e-9 bn)", abs(sum(by_sector[rd][a].values()) - central[a][rd][0]) < 1e-9)
    # The top wages by sector (personal, row 4, before the fill-in): records at or above TOP, the union's, their part of
    # the sector's wages, and the union's direct wage share with and without them against its share of earners.
    hi, ww, w0 = wage >= TOP, wage * w4[:, 0], w4[:, 0]
    top_by_sector = {}
    for sec in dict.fromkeys(sector_of):
        k = m["civilian"] & (wage > 0) & (sector_of[cellidx] == sec)
        if k.any():
            top_by_sector[sec] = {"records": int(k.sum()), "records_at_top": int((k & hi).sum()),
                                  "union_records_at_top": int((k & hi & m["union"]).sum()), "top_share_of_wages": float(ww[k & hi].sum() / ww[k].sum()),
                                  "union_wage_share": float(ww[k & m["union"]].sum() / ww[k].sum()),
                                  "union_wage_share_top_out": float(ww[k & m["union"] & ~hi].sum() / ww[k & ~hi].sum()),
                                  "union_earner_share": float(w0[k & m["union"]].sum() / w0[k].sum())}
    # Employer size (NOEMP, all locations): the share of wages by size class, union and national (personal, row 4).
    noemp = d.NOEMP.to_numpy()
    firm_size = {}
    for g in ("union", "civilian"):
        k = m[g] & (wage > 0)
        tot = np.bincount(noemp[k], weights=wage[k] * w4[k, 0], minlength=len(NOEMP))
        firm_size["national" if g == "civilian" else g] = {lab: float(v) for lab, v in zip(NOEMP, tot / tot.sum())}
    # National intensity: the item's line taxes per dollar of national CPS wages, for comparison.
    for rd in READINGS:
        for a in ALLOCS:
            n_w = wages[a]["national"].sum(axis=0)[0] / 1e9
            gen[rd][a]["national"] = {"wages_bn": float(n_w), "per_wage_dollar": float(sum(national_in_item[ln] * LINE_RESP[rd][ln] for ln in LINES) / n_w)}

    # The lineage's added people [INFERENCE]: priced as G3+ members (per person) and as whites at the G3+'s ages
    # (whites' per-person item by five-year age band, weighted to the union G3+'s band mix).
    band = np.minimum(d.A_AGE.to_numpy() // 5, 17)
    nat_hi = {a: cell_wages(np.where(wage >= TOP, wage, 0.0), cellidx, n_cells, m["civilian"], w4, unit, n_unit, a)[:, 0] for a in ALLOCS}
    lineage = {rd: {} for rd in READINGS}
    for rd in READINGS:
        t_tot = sum(nat_lines[ln] * LINE_RESP[rd][ln] for ln in LINES)
        for a in ALLOCS:
            # Tax per wage dollar earned in each cell: its own line taxes over its wages, plus, for every thin cell pooled
            # over a set of cells, that cell's taxes over the set's wages (the decomposition of sum_i s_i T_i); wages at or
            # above TOP earn the rate of the nation's such wages (they are spread as those are).
            natl0 = wages[a]["national"][:, 0]
            rate = np.zeros(n_cells)
            for i, idx in enumerate(pooled_index(N_MIN)):
                den = natl0[idx].sum()
                if den > 0:
                    rate[idx] += t_tot[i] / den
            r_person = np.where(wage >= TOP, float(nat_hi[a] @ rate / nat_hi[a].sum()), rate[cellidx])
            if a == "personal":
                pers = wage * r_person
            else:
                pers = (np.bincount(unit, weights=wage * r_person, minlength=n_unit.size) / n_unit)[unit]
            wv = w4[:, 0]
            g3m, wm = m["G3plus"], m["white"]
            g3_mix = np.bincount(band[g3m], weights=wv[g3m], minlength=18)
            g3_mix /= g3_mix.sum()
            wcount = np.bincount(band[wm], weights=wv[wm], minlength=18)
            white_band = np.divide(np.bincount(band[wm], weights=wv[wm] * pers[wm], minlength=18), wcount, out=np.zeros(18), where=wcount > 0)
            white_at_g3_ages = float(white_band @ g3_mix)
            g3_pp = -gen[rd][a]["G3plus"]["item_bn"] / gen[rd][a]["G3plus"]["persons"]
            added = -(members["g3plus"] * g3_pp + members["white"] * white_at_g3_ages)
            lineage[rd][a] = {"added_bn": added, "union_plus_added_bn": gen[rd][a]["union"]["item_bn"] + added,
                              "g3plus_per_person_usd": g3_pp * 1e9, "white_at_g3plus_ages_per_person_usd": white_at_g3_ages * 1e9,
                              "white_per_person_usd": -gen[rd][a]["white"]["per_person_usd"]}
            check = sum(float((wv[m[G]] * pers[m[G]]).sum()) * corr[a][G] for G in GENS)
            gate(f"{rd}, {a}: per-person items sum to the union's item (1e-6 bn)", abs(-check - gen[rd][a]["union"]["item_bn"]) < 1e-6)

    # Mining's part, by cell and tax component: the union's target before the response, what the arm adds at each
    # reading, and the reading where only its reproducible capital responds [INFERENCE: corporate at Power and Frerick's
    # mining normal-return share, business property as other industries (the line is keyed by the Fixed Assets stock,
    # reproducible by construction), severance at 0, the other components at 1].
    COMP = {"corporate": "corporate_bn", "c_and_i_property": "c_and_i_property_bn", "otp_licenses_and_other": "otp_licenses_and_other_bn",
            "otp_severance": "otp_severance_bn", "otp_documentary": "otp_documentary_bn", "otp_special_assessments": "otp_special_assessments_bn"}
    COMP_LINE = {k: (k if k in ("corporate", "c_and_i_property") else "other_production_taxes") for k in COMP}
    pf_mining = float(pf["table1_2011_2013"]["Mining"]["risk_free"])
    REPRO = {"corporate": pf_mining, "c_and_i_property": resp["central"], "otp_licenses_and_other": 1.0, "otp_severance": 0.0,
             "otp_documentary": 1.0, "otp_special_assessments": 1.0}
    mining_part = {"cells": [all_cells[i] for i in mining],
                   "national_bn": {k: {all_cells[i]: float(full[c][i]) for i in mining} for k, c in COMP.items()},
                   "union_share": {}, "union_target_bn": {}, "at_readings_bn": {rd: {} for rd in READINGS},
                   "reproducible_only_bn": {}}
    for a in ALLOCS:
        s_u = shares(a, "union")
        tgt = {k: sum(s_u[i] * full[c][i] for i in mining) for k, c in COMP.items()}   # (161,) per component
        mining_part["union_share"][a] = {all_cells[i]: float(s_u[i, 0]) for i in mining}
        mining_part["union_target_bn"][a] = {k: {all_cells[i]: float(s_u[i, 0] * full[c][i]) for i in mining} for k, c in COMP.items()}
        for rd in READINGS:
            v = -sum(tgt[k] * LINE_RESP[rd][COMP_LINE[k]] for k in COMP)
            mining_part["at_readings_bn"][rd][a] = {"value_bn": float(v[0]), "se_bn": se(v)}
            gap = abs(float(v[0]) - (arms[("mining_as_other_industries", a)][rd][0] - central[a][rd][0]))
            gate(f"{rd}, {a}: mining's components add to what the arm adds to the central (1e-9 bn)", gap < 1e-9, f"{float(v[0]):.4f} bn")
        v = -sum(tgt[k] * REPRO[k] for k in COMP)
        mining_part["reproducible_only_bn"][a] = {"value_bn": float(v[0]), "se_bn": se(v)}

    # The residential parts of documentary taxes and special assessments: outside the item (homes, not the capital that
    # serves jobs). Priced beside at the case's owner and tenant property keys and v6's responses for those lines, the
    # parts split between owners and tenants by Z.1 market value (households' owner-occupied real estate against
    # noncorporate residential real estate).
    hk = case["case_housing_key"]
    OWN, TEN = "modeled_owner_property", "tenant_occupied_property"
    z = nat_json["land"]["z1_mn"]
    f_owner = z["household_owner_real_estate"] / (z["household_owner_real_estate"] + z["noncorp_res_real_estate"])
    res_parts = nat_json["residential_split"]["residential_parts_bn"]
    res_total = float(sum(res_parts.values()))
    gate("the residential parts are the RESIDENTIAL cell's other production taxes (1e-6 bn)",
         abs(res_total - float(nat.loc["RESIDENTIAL", "other_production_taxes_bn"])) < 1e-6, f"{res_total:.6f}")
    gate("v6's owner and tenant property responses are the same at both ends", all(hk["responses"][x]["low"] == hk["responses"][x]["high"] for x in (OWN, TEN)))
    r_own, r_ten = hk["responses"][OWN]["low"], hk["responses"][TEN]["low"]
    residential = {}
    for F in ["union"] + GENS:
        residential[F] = {}
        for a in ALLOCS:
            s_o, s_t = hk["lines"][OWN]["shares"][F][a], hk["lines"][TEN]["shares"][F][a]
            residential[F][a] = {"target_bn": res_total * (f_owner * s_o + (1 - f_owner) * s_t),
                                 "lost_bn": res_total * (f_owner * s_o * r_own + (1 - f_owner) * s_t * r_ten)}
    gate("the residential parts' generations add to the union (1e-9 bn)", all(abs(sum(residential[G][a]["lost_bn"] for G in GENS)
                                                                                - residential["union"][a]["lost_bn"]) < 1e-9 for a in ALLOCS))

    # ----------------------------------------------------------------------------------------------------------
    # The item file for main case v7 (main_case_2026_10_14 item_job_capital.cjs, the contract of its brief). Per item
    # line: the case's national, the response at each reading, the union's key share and target (group_bn = key_share x
    # national, before the response; item_bn after it), plain_wage_share = the union's share of the case's wage key
    # (case_keys.json case_wage_key), the generations' targets, and factors: a group's key share over its share of the
    # case's wage key (the union and its generations) or over its plain wage share on this lane's frame (whites and
    # Blacks, who have no case cells).
    print("\n[item file]")
    cw = case["case_wage_key"]["shares"]
    item_nat = {g: case["national_bn"][ln] for g, ln in ITEM_LINES.items()}
    lane_plain = {F: {a: float(wages[a][g][:, 0].sum() / wages[a]["national"][:, 0].sum()) for a in ALLOCS} for F, g in ITEM_GROUPS.items()}
    denom = {F: (cw[F] if F in cw else lane_plain[F]) for F in ITEM_GROUPS}
    sh0 = {(a, g): shares(a, g)[:, 0] for a in ALLOCS for g in GROUPS}

    def targets(tv, level=None):
        """Main-estimate targets ($bn, before the response) by item group, line and allocation: each group's shares
        times the cell vectors tv, or level[F][a] x the base (a key without industries); the union is its generations' sum."""
        out = {F: {g: {a: float(sh0[(a, grp)] @ tv[g]) if level is None else level[F][a] * float(tv[g].sum()) for a in ALLOCS}
                   for g in ITEM_LINES} for F, grp in ITEM_GROUPS.items() if F != "union"}
        out["union"] = {g: {a: sum(out[G][g][a] for G in GENS) for a in ALLOCS} for g in ITEM_LINES}
        return out

    def block(label, T, rsp, tv, note, **extra):
        lines = {}
        for g, ln in ITEM_LINES.items():
            key = {a: T["union"][g][a] / item_nat[g] for a in ALLOCS}
            gb = {a: key[a] * item_nat[g] for a in ALLOCS}
            lines[g] = {"national_bn": item_nat[g], "response": {rd: rsp[rd][ln] for rd in READINGS}, "key_share": key, "group_bn": gb,
                        "item_bn": {rd: {a: rsp[rd][ln] * gb[a] for a in ALLOCS} for rd in READINGS},
                        "plain_wage_share": dict(cw["union"]), "lane_plain_wage_share": dict(lane_plain["union"]), "base_bn": float(tv[g].sum())}
        factor = {F: {g: {a: T[F][g][a] / item_nat[g] / denom[F][a] for a in ALLOCS} for g in ITEM_LINES} for F in ITEM_GROUPS}
        factor["union"] = {g: {a: lines[g]["key_share"][a] / lines[g]["plain_wage_share"][a] for a in ALLOCS} for g in ITEM_LINES}
        central_bn = {rd: {a: sum(lines[g]["item_bn"][rd][a] for g in ITEM_LINES) for a in ALLOCS} for rd in READINGS}
        return {"label": label, "note": note, "lines": lines, "by_generation": {G: {g: dict(T[G][g]) for g in ITEM_LINES} for G in GENS},
                "factor": factor, "central_bn": central_bn,
                "net_cost_change_bn": {rd: {a: -v for a, v in x.items()} for rd, x in central_bn.items()}, **extra}

    tv_c = {g: nat_lines[ln] for g, ln in ITEM_LINES.items()}
    tv_full = {g: full_lines[ln] for g, ln in ITEM_LINES.items()}
    T_c = targets(tv_c)
    blocks = {"central": block("the lane's central reading: every line by industry at the union's share of each industry's CPS wage bill, "
                               "mining at 0", T_c, LINE_RESP, tv_c, "")}
    T_pf = targets(tv_c | {"corporate": pf_corp})
    eff_pf = {F: {a: T_pf[F]["corporate"][a] / T_c[F]["corporate"][a] for a in ALLOCS} for F in T_c}
    T_foreign = targets(tv_c | {"corporate": vec["corporate_ex_foreign_bn"]})
    floor_tv = tv_c | {"corporate": 0.25 * full_lines["corporate"]}
    T_floor = targets(floor_tv, denom)
    T_floor = {F: {g: (T_floor[F][g] if g == "corporate" else T_c[F][g]) for g in ITEM_LINES} for F in T_floor}
    onbooks = {F: ({g: {a: T_c[F][g][a] * cw[F][a] / lane_plain[F][a] for a in ALLOCS} for g in ITEM_LINES} if F in GENS else T_c[F])
               for F in ITEM_GROUPS if F != "union"}
    onbooks["union"] = {g: {a: sum(onbooks[G][g][a] for G in GENS) for a in ALLOCS} for g in ITEM_LINES}
    blocks |= {
        "mining_as_other_industries": block("mining's three taxes respond as other industries' do (the build before 2026-10-14)",
                                            targets(tv_full), LINE_RESP, tv_full, ""),
        "normal_return_share": block("corporate at TP-5's normal-return share (0.37) at both readings", T_c, with_resp(corporate=nr_tp5),
                                     tv_c, "Treasury OTA Technical Paper 5, p. 7"),
        "normal_return_share_0_25": block("the high reading's corporate response at Power and Frerick's 2003-2013 normal-return share (Treasury "
                                          "OTA Working Paper 111, abstract)", T_c, with_resp(corporate={"low": 1.0, "high": nr_pf}), tv_c, ""),
        "normal_return_share_by_industry": block("the high reading's corporate response at each industry's normal-return share (Power and "
                                                 "Frerick Table 1, 2011-2013), as the union's personal effective share", T_c,
                                                 with_resp(corporate={"low": 1.0, "high": eff_pf["union"]["personal"]}), tv_c,
                                                 "one response for every group and allocation; each group's own effective share is in "
                                                 "effective_high_corporate_response", effective_high_corporate_response=eff_pf),
        "plain_wage_share": block("the plain wage share in place of the industry key: every line's base at each group's share of all CPS "
                                  "wages on this lane's frame", targets(tv_c, lane_plain), LINE_RESP, tv_c,
                                  "the base that responds (mining and the residential parts out); the receipt lane's ceiling on the case's "
                                  "frame is minus plain_wage_share x the three lines' national, every line at 1"),
        "foreign_source_removed": block("federal tax on foreign-source corporate income removed from the corporate base (IRS SOI TY2021)",
                                        T_foreign, LINE_RESP, tv_c | {"corporate": vec["corporate_ex_foreign_bn"]}, ""),
        "business_land_at_0": block("business land at response 0: the land part of business property tax stays", T_c,
                                    with_resp(c_and_i_property=land_0), tv_c, "response tau + (1 - tau)(1 - lambda_b)"),
        "business_land_at_1": block("business land at response 1: the whole business property tax leaves", T_c,
                                    with_resp(c_and_i_property=1.0), tv_c, ""),
        "floor": block("the floor: CBO's labour share of corporate tax only, at the case's wage key; the other lines at response 0",
                       T_floor, {rd: {"corporate": 1.0, "other_production_taxes": 0.0, "c_and_i_property": 0.0} for rd in READINGS}, floor_tv,
                       "corporate base 25% of the whole corporate national (corporate_labor's 165.92125bn), mining included"),
        "case_wage_key": block("the case's wage key (the status rules at the on-books lane's shares) in place of all CPS wages: each generation's "
                               "targets times its share of the case's wage key over its plain share on this lane's frame", onbooks, LINE_RESP, tv_c,
                               "[INFERENCE] the off-books wages take each generation's own industry mix"),
    }
    for name, b in blocks.items():
        ok = all(abs(b["lines"][g]["group_bn"][a] - b["lines"][g]["key_share"][a] * b["lines"][g]["national_bn"]) <= 1e-9
                 and abs(sum(b["by_generation"][G][g][a] for G in GENS) - b["lines"][g]["group_bn"][a]) <= 1e-9
                 and abs(b["factor"]["union"][g][a] - b["lines"][g]["key_share"][a] / b["lines"][g]["plain_wage_share"][a]) <= 1e-9
                 and b["lines"][g]["plain_wage_share"][a] == cw["union"][a]
                 and all(np.isfinite(b["lines"][g]["response"][rd]) for rd in READINGS) for g in ITEM_LINES for a in ALLOCS)
        gate(f"item file {name}: group_bn = key_share x national, the generations add to it, factor.union = key_share / "
             "plain_wage_share (1e-9), plain_wage_share is the case's wage key and both readings have a response", ok)
    cb = blocks["central"]
    gate("item file central: the lines' nationals are the case's (1e-6); corporate responds 1 low and TP-5's share high, the other "
         "two lines alike at both", all(abs(cb["lines"][g]["national_bn"] - item_nat[g]) <= 1e-6 for g in ITEM_LINES)
         and cb["lines"]["corporate"]["response"] == {"low": 1.0, "high": nr_tp5}
         and cb["lines"]["other_production_taxes"]["response"] == {"low": 1.0, "high": 1.0}
         and cb["lines"]["business_property"]["response"] == {"low": resp["central"], "high": resp["central"]})
    item_rows = {"central": "central", "mining_as_other_industries": "arm_mining_as_other_industries",
                 "normal_return_share": "arm_normal_return_share", "normal_return_share_0_25": "arm_normal_return_share_0_25",
                 "foreign_source_removed": "arm_foreign_removed", "business_land_at_0": "arm_land_0", "business_land_at_1": "arm_land_1"}
    pick_all = lambda rr, rd, a: next(r["value_bn"] for r in rows if r["row"] == rr and r["reading"] == rd and r["allocation"] == a and r["line"] == "all")
    gap = max(abs(blocks[k]["net_cost_change_bn"][rd][a] - pick_all(rr, rd, a)) for k, rr in item_rows.items() for rd in READINGS for a in ALLOCS)
    gate("item file: the central and six arms are items.csv's at both readings (1e-9 bn)", gap < 1e-9, f"{gap:.1e}")
    pf_gap = {a: blocks["normal_return_share_by_industry"]["net_cost_change_bn"]["high"][a]
              - pick_all("arm_normal_return_share_by_industry", "high", a) for a in ALLOCS}
    gate("item file normal_return_share_by_industry: personal is items.csv's at the high reading (1e-9 bn), shared within 0.25 bn "
         "(one response, the personal one, for both allocations)", abs(pf_gap["personal"]) < 1e-9 and abs(pf_gap["shared"]) < 0.25,
         f"shared {pf_gap['shared']:+.4f} bn")
    for k in ("plain_wage_share", "floor", "case_wage_key", "normal_return_share_by_industry"):
        for rd in READINGS:
            for a in ALLOCS:
                rows.append({"row": f"item_arm_{k}", "reading": rd, "label": blocks[k]["label"], "allocation": a, "line": "all",
                             "base_bn": sum(item_nat.values()), "response": nan, "group_share": nan,
                             "value_bn": blocks[k]["net_cost_change_bn"][rd][a], "se_bn": nan, "note": "derived/item.json arms"})
    wage_bn = {F: {a: float(wages[a][grp][:, 0].sum()) / 1e9 for a in ALLOCS} for F, grp in ITEM_GROUPS.items()}
    per_wage = {rd: {F: {**{g: {a: LINE_RESP[rd][ITEM_LINES[g]] * T_c[F][g][a] / wage_bn[F][a] for a in ALLOCS} for g in ITEM_LINES},
                         "all": {a: sum(LINE_RESP[rd][ITEM_LINES[g]] * T_c[F][g][a] for g in ITEM_LINES) / wage_bn[F][a] for a in ALLOCS}}
                     for F in ITEM_GROUPS} for rd in READINGS}
    for rd in READINGS:
        n_w = {a: float(wages[a]["national"][:, 0].sum()) / 1e9 for a in ALLOCS}
        per_wage[rd]["national"] = {**{g: {a: LINE_RESP[rd][ITEM_LINES[g]] * float(tv_c[g].sum()) / n_w[a] for a in ALLOCS} for g in ITEM_LINES},
                                    "all": {a: sum(LINE_RESP[rd][ITEM_LINES[g]] * float(tv_c[g].sum()) for g in ITEM_LINES) / n_w[a] for a in ALLOCS}}

    if any(not g["passed"] for g in GATES):
        print(f"\n[BLOCKED] {sum(not g['passed'] for g in GATES)} gate(s) failed; nothing written")
        return 1

    # ----------------------------------------------------------------------------------------------------------
    args.out_dir.mkdir(parents=True, exist_ok=True)
    with (args.out_dir / "wages_by_industry.csv").open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["cell", "sector", "allocation", "cps_earners", "share_pooled_over", "national_wages_bn", "union_wages_bn",
                    "union_own_share", "union_own_share_se", "union_share", "union_share_se", "G1_share", "G2_share",
                    "G3plus_share", "white_share", "nonprofit_wage_share", "corporate_bn", "c_and_i_property_bn",
                    "other_production_taxes_bn", "responds", "pf_normal_share", "union_item_low_bn", "union_item_high_bn"])
        for a in ALLOCS:
            sh = {g: shares(a, g) for g in GROUPS}
            own = shares(a, "union", 0)
            cell_item = {rd: -sh["union"][:, 0] * sum(nat_lines[ln] * LINE_RESP[rd][ln] for ln in LINES) for rd in READINGS}
            for i, c in enumerate(all_cells):
                idx = pooled_index(N_MIN)[i]
                over = "own" if len(idx) == 1 else (sector_of[i] if len(idx) < len(private_cells) else "private")
                w.writerow([c, sector_of[i], a, int(n_rec[i]), over, f"{wages[a]['national'][i, 0] / 1e9:.6f}",
                            f"{wages[a]['union'][i, 0] / 1e9:.6f}", f"{own[i, 0]:.9f}", f"{se(own[i]):.9f}",
                            f"{sh['union'][i, 0]:.9f}", f"{se(sh['union'][i]):.9f}", f"{sh['G1'][i, 0]:.9f}", f"{sh['G2'][i, 0]:.9f}",
                            f"{sh['G3plus'][i, 0]:.9f}", f"{sh['white'][i, 0]:.9f}", f"{np_share[i]:.9f}",
                            f"{full_lines['corporate'][i]:.9f}", f"{full_lines['c_and_i_property'][i]:.9f}",
                            f"{full_lines['other_production_taxes'][i]:.9f}", int(responds[i]), f"{pf_cell[i]:.2f}",
                            f"{cell_item['low'][i]:.9f}", f"{cell_item['high'][i]:.9f}"])
    # The industry crosswalk with what the CPS puts in each code (civilian wage earners on row 4's weights, personal,
    # own wages before the top-wage spreading and the fill-in; government workers counted under their code, though
    # the cells move them to GOVF and GOVSL).
    earners = m["civilian"] & (wage > 0)
    by_code = pd.DataFrame({"code": d.INDUSTRY.to_numpy()[earners], "w": (wage * w4[:, 0])[earners],
                            "u": (wage * w4[:, 0] * m["union"])[earners]}).groupby("code").agg(n=("w", "size"), w=("w", "sum"), u=("u", "sum"))
    pf_of = pf["cells"]
    with (args.out_dir / "industry_crosswalk.csv").open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["census_code", "description", "naics", "bea_industry", "sector", "pf_industry", "cps_wage_earners",
                    "national_wages_bn", "union_wages_bn", "union_wage_share"])
        for r in crosswalk.itertuples():
            code = int(r.census_code)
            n_c, w_c, u_c = (int(by_code.at[code, "n"]), float(by_code.at[code, "w"]), float(by_code.at[code, "u"])) if code in by_code.index else (0, 0.0, 0.0)
            sec = "government" if r.bea_industry == "GOV" else SECTOR.get(r.bea_industry, "")
            w.writerow([r.census_code, r.description, r.naics, r.bea_industry, sec, pf_of.get(r.bea_industry, ""), n_c,
                        f"{w_c / 1e9:.6f}", f"{u_c / 1e9:.6f}", f"{u_c / w_c:.9f}" if w_c > 0 else ""])
    fmt = lambda x: "" if x is None or (isinstance(x, float) and np.isnan(x)) else (f"{x:.9f}" if isinstance(x, float) else str(x))
    with (args.out_dir / "items.csv").open("w", newline="") as f:
        cols = ["row", "reading", "label", "allocation", "line", "base_bn", "response", "group_share", "value_bn", "se_bn", "note"]
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cols)
        for r in rows:
            w.writerow([fmt(r[c]) for c in cols])
    r9 = lambda x: round(float(x), 9)
    rr9 = lambda o: {k: (rr9(v) if isinstance(v, dict) else r9(v)) for k, v in o.items()}
    line_value = lambda row, rd, a, ln: next(r["value_bn"] for r in rows if r["row"] == row and r["reading"] == rd and r["allocation"] == a and r["line"] == ln)
    line_se = lambda row, rd, a, ln: next(r["se_bn"] for r in rows if r["row"] == row and r["reading"] == rd and r["allocation"] == a and r["line"] == ln)
    tg_union = {a: {ln: float(tg_by[a]["union"][ln][0]) for ln in LINES} for a in ALLOCS}
    summary = {
        "meta": {
            "item": "taxes on the business capital that serves the group's jobs: business property, other production taxes, corporate",
            "frame": "CPS ASEC 2025 civilian household persons, income 2024; the union on row 4's weights (39,712,493); wages WSAL_VAL",
            "readings": {"low": "the band's low end: corporate at 1", "high": "the band's high end: corporate at the normal-return share"},
            "mining": "BEA 211, 212 and 213 respond at 0 on all three lines at both readings (their cells out of the item's vectors)",
            "fill_in": {"methods": METHODS, "rel_change": {a: r9(rc[a]) for a in ALLOCS}, "rel_change_se": {a: r9(rc_se[a]) for a in ALLOCS},
                        "generation_parts": {a: {G: r9(v) for G, v in d_split[a].items()} for a in ALLOCS},
                        "generation_factors": {a: {G: r9(corr[a][G]) for G in GENS} for a in ALLOCS},
                        "rule": "the union's wages move by the two methods' mean wage rel_change (status_combination_keys.csv), split across "
                                "the generations as the same methods' wage-key change splits in generation_account_2026_09_24 "
                                "stack_by_generation.json (components D_<method>, convention a): G's cell wages x (1 + rc x part_G x union "
                                "wages / G's wages); whites and Blacks uncorrected"},
            "inputs_sha256": {"cps": CPS_SHA, "builder_keys": KEYS_SHA, "row4": ROW4_SHA, "fill_in": FILLIN_SHA, "counties": COUNTIES_SHA,
                              "v6_corrections": V6_SHA, "stack_by_generation": STACK_SHA, "crosswalk": sha256(CROSSWALK)},
            "sign": "negative = the group's net cost falls (taxes the case counts at zero that leave with the group)",
        },
        "parameters": {"lambda_b": r9(lam_b), "tau": r9(tau), "delta_L": {k: r9(v) for k, v in delta.items()},
                       "r_b": {k: r9(v) for k, v in r_b.items()}, "business_property_response": r9(resp["central"]),
                       "corporate_response": {"low": 1.0, "high": nr_tp5}, "normal_return_share": nr_tp5,
                       "power_frerick_2003_2013": nr_pf, "power_frerick_mining": pf_mining,
                       "foreign_removed_national_bn": nat_json["foreign"]["removed_bn"]},
        "central": {rd: {a: {"value_bn": r9(central[a][rd][0]), "se_bn": r9(se(central[a][rd])),
                             "by_line_bn": {ln: r9(line_value("central", rd, a, ln)) for ln in LINES},
                             "fill_in_se_bn": r9(abs(central[a][rd][0]) * rc_se[a] / (1 + rc[a]))} for a in ALLOCS} for rd in READINGS},
        "arms": {name: {rd: {a: {"value_bn": r9(arms[(name, a)][rd][0]), "se_bn": r9(se(arms[(name, a)][rd]))} for a in ALLOCS} for rd in READINGS}
                 for name in ("mining_as_other_industries", "normal_return_share", "normal_return_share_0_25", "normal_return_share_by_industry",
                              "foreign_removed", "land_0", "land_1")}
                | {"plain_wage_share_ceiling": {"shared": r9(ceiling["spec48_shared"]), "personal": r9(ceiling["spec11_personal"])}},
        "floor_corporate_labor_bn": {"shared": r9(floor["spec48"]), "personal": r9(floor["spec11"])},
        "beside_bn": {r["row"]: {rd: {} for rd in READINGS} for r in rows if r["row"].startswith("beside")},
        "keys": {a: {"plain_wage_share": r9(plain[a][0]), "plain_wage_share_se": r9(se(plain[a])),
                     "case_wage_key_share": cw["union"][a], "lane_over_case_wage_share": r9(plain[a][0] / cw["union"][a]),
                     "industry_weighted_share_of_base_by_line": {ln: r9(tg_union[a][ln] / national_in_item[ln]) for ln in LINES},
                     "industry_weighted_share_of_base_all": r9(sum(tg_union[a].values()) / sum(national_in_item.values())),
                     "base_bn": {ln: r9(national_in_item[ln]) for ln in LINES},
                     "case_employer_hi_sept27": s27["spec48" if a == "shared" else "spec11"],
                     "case_employer_hi_v6": v6_share["spec48_shared" if a == "shared" else "spec11_personal"],
                     "noind_national_wages_bn": r9(noind_bn[a])} for a in ALLOCS},
        "generations": {rd: {a: {g: {k: (r9(v) if not isinstance(v, dict) else {kk: r9(vv) for kk, vv in v.items()}) for k, v in x.items()}
                                 for g, x in gen[rd][a].items()} for a in ALLOCS} for rd in READINGS},
        "central_by_sector_bn": {rd: {a: {k: r9(v) for k, v in x.items()} for a, x in by_sector[rd].items()} for rd in READINGS},
        "mining": {"cells": mining_part["cells"], "national_bn": rr9(mining_part["national_bn"]), "union_share": rr9(mining_part["union_share"]),
                   "union_target_bn": rr9(mining_part["union_target_bn"]), "added_by_the_arm_bn": rr9(mining_part["at_readings_bn"]),
                   "reproducible_only_bn": rr9(mining_part["reproducible_only_bn"]),
                   "reproducible_rule": "[INFERENCE] corporate at Power and Frerick's mining normal-return share (Table 1), business property "
                                        "at the central response (its key is the Fixed Assets stock), severance at 0, licenses, documentary "
                                        "taxes and special assessments at 1, at both readings"},
        "normal_return": {"tp5": nr_tp5, "power_frerick": {"1992_2002": pf["1992_2002"], "2003_2013": nr_pf},
                          "power_frerick_by_industry_effective": {F: {a: r9(v) for a, v in x.items()} for F, x in eff_pf.items()},
                          "power_frerick_national_effective": r9(nat_pf),
                          "rule": "effective = the group's corporate target with each cell at its industry's Table 1 share over its target "
                                  "at 1, on the item's base (mining out); national on the cells' corporate tax"},
        "residential_parts": {"parts_bn": res_parts, "owner_share_of_value": r9(f_owner), "responses": {"owner": r_own, "tenant": r_ten},
                              "by_group": {F: {a: rr9(v) for a, v in x.items()} for F, x in residential.items()},
                              "rule": "beside, outside the item: the residential parts of documentary and stamp taxes and special assessments "
                                      "(Z.1 residential share) split owner / tenant by Z.1 market value, at the case's owner and tenant "
                                      "property keys and v6's responses for those lines"},
        "pooling": {"n_min": N_MIN, "pooled_cells": thin,
                    "rule": "a cell with fewer CPS civilian wage earners than n_min takes its sector's pooled share (a sector below n_min: "
                            "every private cell's), in every weight column",
                    "top_wages": {"threshold_usd": TOP, "union_share_of_top_wages": {a: r9(v) for a, v in top_share.items()},
                                  "rule": "each group's wages at or above the threshold are spread over the cells as the nation's such wages are "
                                          "(group totals unchanged); the public file caps each earnings source at $1,099,999"}},
        "firm_size_wage_shares": {g: {k: r9(v) for k, v in x.items()} for g, x in firm_size.items()},
        "top_wages_by_sector": {sec: {k: (r9(v) if isinstance(v, float) else v) for k, v in x.items()} for sec, x in top_by_sector.items()},
        "lineage_inference": {"counts": {k: counts[k] for k in ("added", "identified_g3plus", "lineage_population")},
                              "members": {"g3plus": members["g3plus"], "white": members["white"]},
                              "by_reading": {rd: {a: {k: r9(v) for k, v in x.items()} for a, x in lineage[rd].items()} for rd in READINGS},
                              "rule": "[INFERENCE] added people priced as the G3+'s per-person item and as whites' per-person item at the "
                                      "G3+'s five-year age mix; v7 prices them with its own machinery and the factors"},
        "gates": GATES,
    }
    for r in rows:
        if r["row"].startswith("beside") and r["line"] == "all":
            summary["beside_bn"][r["row"]][r["reading"]][r["allocation"]] = r9(r["value_bn"])
    (args.out_dir / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    se_line = {rd: {g: {a: line_se("central", rd, a, ln) for a in ALLOCS} for g, ln in ITEM_LINES.items()} for rd in READINGS}
    mining_out = {g: {"national_bn": float(full_lines[ln][mining].sum()),
                      "union_target_bn": {a: float(shares(a, "union")[mining, 0] @ full_lines[ln][mining]) for a in ALLOCS}} for g, ln in ITEM_LINES.items()}
    otp = nat_json["other_production_components_bn"]
    item = {
        "lane": "job_capital_taxes_2026_10_14",
        "contract": "main_case_2026_10_14 item_job_capital.cjs (the v7 brief): lines, by_generation, factor, per_wage_dollar, central_bn, arms, gates",
        "frame": "the identified union (39,712,493 on audit row 4's weights), CPS ASEC 2025 wage and salary income (WSAL_VAL) by the longest "
                 "job's industry, the case's fill-in correction split by generation; no status rules: an off-books job's capital is taxed at "
                 "its source whether or not the wage is reported (the case's production term also counts all CPS earnings)",
        "conventions": {
            "readings": "low = the band's low end (corporate at 1), high = its high end (corporate at the normal-return share); every line's "
                        "response is {low, high}",
            "group_bn": "the union's target before the response, key_share x national_bn, $bn (taxes on the capital that serves its jobs)",
            "item_bn": "response x group_bn at each reading: the taxes a removal loses; central_bn sums the lines and net_cost_change_bn is minus it",
            "plain_wage_share": "the union's share of the case's wage key (corporate_labor at cbo_collective on the September 29 payload "
                                "model, case_keys.json case_wage_key); lane_plain_wage_share is the union's share of all CPS wages here",
            "factor": "a group's key share over its share of the case's wage key (union, G1, G2, G3plus: case_wage_key.shares) or over its "
                      "plain wage share on this lane's frame (white_nh, black_nh: third-plus non-Hispanic white and Black alone; *_all: "
                      "every nativity); by_generation[G] = factor[G] x case share of G x national_bn",
            "by_generation": "the union's generations' targets before the response, convention a; they add to group_bn",
            "national_bn": "the case's line: corporate = corporate_capital + corporate_labor, business_property = "
                           "remaining_production_property, other_production_taxes the whole line; base_bn is the part the key spreads "
                           "(mining's cells out of every line; other production taxes: the residential parts of documentary taxes and "
                           "special assessments out as well)",
        },
        **{k: v for k, v in blocks["central"].items() if k != "note"},
        "se_bn": {"central": {rd: {a: se(central[a][rd]) for a in ALLOCS} for rd in READINGS}, "by_line": se_line,
                  "fill_in": {rd: {a: abs(central[a][rd][0]) * rc_se[a] / (1 + rc[a]) for a in ALLOCS} for rd in READINGS},
                  "rule": "SDR over the 160 replicate weights (the CPS sample); fill_in from the fill-in rel_change SE"},
        "per_wage_dollar": {"rule": "tax lost at the line's response per dollar of the group's CPS wage and salary income on this lane's frame "
                                    "(all wages, row 4 and the fill-in; the employer_hi key's wage concept, WSAL_VAL), by reading; all sums "
                                    "the lines; national is the item's bases over national CPS wages", **per_wage},
        "responses_rule": {"lambda_b": lam_b, "delta_L": delta["group_population"], "tau": tau, "r_b": r_b["group_population"],
                           "business_property": resp["central"], "corporate": {"low": 1.0, "high": nr_tp5}, "other_production_taxes": 1.0,
                           "mining": "0 on every line at both readings (its cells carry no tax in the key)",
                           "rule": "business property = tau + (1 - tau) x r_b: r_b = 1 - lambda_b (1 - delta_L) on the real property, "
                                   "the tangible personal property part tau leaving whole; corporate leaves whole at the low end and only its "
                                   "normal-return share at the high end"},
        "normal_return": {"high_reading": nr_tp5, "source": normal["source"], "ota_2021": normal["ota_2021_source"],
                          "power_frerick": {"1992_2002": pf["1992_2002"], "2003_2013": nr_pf, "source": pf["source"],
                                            "table1_2011_2013": pf["table1_2011_2013"], "union_effective": eff_pf["union"],
                                            "national_effective_on_the_item_base": nat_pf},
                          "fox_2020": "beside, no arm: Fox, Does Capital Bear the U.S. Corporate Tax After All?, Journal of Empirical Legal "
                                      "Studies 17(1), 2020, p. 72: actual 1995-2013 revenue exceeded a hypothetical cash-flow tax's by \"about 4 "
                                      "percent on average\" (21 percent under more conservative assumptions, note 5)",
                          "what_supernormal_includes": "Power and Frerick p. 4: returns above the risk-free rate \"including returns to risk, "
                                                       "entrepreneurial labor, decreasing returns to scale, market power, luck, etc.\"; most "
                                                       "self-created intangibles are already expensed (Appendix A p. 21), so their returns sit "
                                                       "in the excess part"},
        "mining": {"cells": mining_part["cells"], "by_line": mining_out,
                   "rule": "excluded from the key: its cells carry no tax on any line (the team lead, 2026-10-14); the arm "
                           "mining_as_other_industries keeps them"},
        "other_production_line": {"national_bn": item_nat["other_production_taxes"], "components_bn": otp,
                                  "residential_parts_bn": res_parts, "mining_part_bn": mining_out["other_production_taxes"]["national_bn"],
                                  "base_bn": national_in_item["other_production_taxes"],
                                  "key_rule": "key_share = the union's tax on the base over the whole case line: the residential parts and "
                                              "mining's cells give the group no share, which leaves them at zero as v6 does",
                                  "residential_beside": residential, "residential_rule": summary["residential_parts"]["rule"]},
        "case_wage_key": case["case_wage_key"],
        "arms": {k: v for k, v in blocks.items() if k != "central"},
        "beside_net_cost_change_bn": summary["beside_bn"],
        "upstream_gates": {"national.py": len(nat_json["gates"]), "case_keys.cjs": len(case["gates"]), "all_passed": True},
        "gates": [{"name": g["gate"], "passed": g["passed"], "value": g["detail"]} for g in GATES],
    }
    (args.out_dir / "item.json").write_text(json.dumps(item, indent=1) + "\n")
    print(f"\ncentral personal {central['personal']['low'][0]:.4f} low / {central['personal']['high'][0]:.4f} high bn, shared "
          f"{central['shared']['low'][0]:.4f} / {central['shared']['high'][0]:.4f} bn; wrote wages_by_industry.csv, industry_crosswalk.csv, "
          "items.csv, summary.json, item.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
