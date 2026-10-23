"""Measure institutional college prices from primary files; orchestrate the lane.

All prices are conditional allocation keys, not causal enrollment responses.
Use python -I: raw CSVs/ZIPs are data and never enter the import path.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import resource
import subprocess
import sys
import time
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
FISCAL = HERE.parent
STAGE = REPO / "sources/immigration-fiscal/data/external/stage3/nces/ipeds_2023"
OLD = FISCAL / "affirmative_action_cost_2026_09_24/_cache/ipeds"
PUMS = REPO / "sources/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip"
OUT = HERE / "derived"
PINS = {
    PUMS: "afdc6d90c6e2f0bab365ed32d95ba4c4d8ac651162f46ac7861295b2dc469894",
    OLD / "HD2023.csv": "d779a92d637e122c90009112e284ab5c75bc2b3d26774a29746800f522aace0f",
    OLD / "ef2023a.csv": "527ba4696abe0168e086fbc437587008fbfa89fbf1062f95fc3d33652977a2ea",
    STAGE / "F2223_F1A.zip": "beabdb0384f000a2fa487e7083512f880013c897d8e10bab9682f4c836687de9",
    STAGE / "EFIA2023.zip": "87229fac9a64563df477b47f392d5af7913e474363b440739a70a636c449560d",
    STAGE / "FLAGS2023.zip": "df763ac04b15821bbcaa1dac238cbea9c2d88a5ae1b3532e2d1cd90489c8e3d3",
}
ACQUIRE_SPEC = importlib.util.spec_from_file_location("where_used_acquire", HERE / "acquire.py")
ACQUIRE = importlib.util.module_from_spec(ACQUIRE_SPEC)
ACQUIRE_SPEC.loader.exec_module(ACQUIRE)
source = ACQUIRE.source
FUNCTIONS = {
    "instruction": "F1C011", "research": "F1C021", "public_service": "F1C031",
    "academic_support": "F1C051", "student_support": "F1C061", "institutional_support": "F1C071",
    "other": "F1C141", "auxiliary": "F1C111", "auxiliary_sales": "F1B05",
    "tuition": "F1B01", "pell": "F1E01", "education_sales": "F1B26",
    "hospital": "F1C121", "depreciation": "F1C19DP",
    "land_improvements": "F1A214", "infrastructure": "F1A224", "buildings": "F1A234",
    "equipment": "F1A324", "construction": "F1A274", "gross_plant": "F1A27T4",
    "accumulated_depreciation": "F1A284", "net_depreciable": "F1A31",
}


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=2, sort_keys=True, allow_nan=False) + "\n")


def normal(name):
    return name.replace("ï»¿", "").replace("\ufeff", "").strip()


def read_csv(source, columns):
    d = pd.read_csv(source, encoding="latin-1", dtype="string", keep_default_na=False,
                    usecols=lambda col: normal(col) in columns)
    d.columns = [normal(col) for col in d]
    if set(d) != set(columns):
        raise ValueError(f"[BLOCKED] missing primary columns: {set(columns) - set(d)}")
    return d


def zipped_csv(archive, member, columns):
    with zipfile.ZipFile(archive) as zipped:
        with zipped.open(member) as stream:
            return read_csv(stream, columns)


def numeric(frame, columns, *, flagged=False):
    out = frame.copy()
    for col in columns:
        values = pd.to_numeric(frame[col], errors="coerce")
        missing = values.isna()
        if missing.any() and (not flagged or not frame.loc[missing, "X" + col].eq("A").all()):
            raise ValueError(f"[BLOCKED] missing applicable primary value: {col}")
        out[col] = values.fillna(0.0).astype(float)
    return out


def acs_ratios():
    """Recompute ACS state/degree ratios; include thin-cell rule used by case."""
    cols = ["STATE", "PWGTP", "SCH", "SCHG", "HISP", "POBP"]
    pieces = []
    population = {"all": 0.0, "mexican_union_proxy": 0.0}
    with zipfile.ZipFile(source(PUMS)) as archive:
        members = sorted(name for name in archive.namelist() if name.startswith("psam_pus") and name.endswith(".csv"))
        if members != ["psam_pusa.csv", "psam_pusb.csv"]:
            raise ValueError("[BLOCKED] unexpected ACS PUMS members")
        for name in members:
            with archive.open(name) as stream:
                for d in pd.read_csv(stream, usecols=cols, dtype="string", chunksize=100_000):
                    weight = pd.to_numeric(d.PWGTP, errors="raise").astype(float)
                    if d[["STATE", "PWGTP", "HISP", "POBP"]].isna().any().any():
                        raise ValueError("[BLOCKED] missing ACS population/origin")
                    mex = d.HISP.eq("02") | d.POBP.eq("303")
                    population["all"] += float(weight.sum())
                    population["mexican_union_proxy"] += float(weight[mex].sum())
                    public = d.SCH.eq("2") & d.SCHG.isin(["15", "16"])
                    c = d.loc[public, ["STATE", "SCHG", "HISP"]].copy()
                    c["students"] = weight[public]
                    c["records"] = 1
                    c["hispanic"] = weight[public] * c.HISP.ne("01").astype(float)
                    c["mexican"] = weight[public] * c.HISP.eq("02").astype(float)
                    pieces.append(c.groupby(["STATE", "SCHG"])[["students", "records", "hispanic", "mexican"]].sum())
    t = pd.concat(pieces).groupby(level=[0, 1]).sum().reset_index()
    t.STATE = pd.to_numeric(t.STATE)
    t["level"] = t.SCHG.map({"15": "UG", "16": "GR"})
    pooled = t.groupby("STATE")[["hispanic", "mexican"]].sum()
    t["pooled"] = t.STATE.map(pooled.mexican / pooled.hispanic)
    t["ratio_raw"] = np.where(t.records >= 100, t.mexican / t.hispanic, t.pooled)
    # The adopted higher_ed.py reads the ACS lane's six-decimal CSV ratio.
    # Reproduce that explicit serialization before comparing its principal key;
    # retain the unrounded reconstruction as a separate measured column.
    t["ratio"] = np.where(t.records >= 100, (t.mexican / t.hispanic).round(6), t.pooled)
    if not t.ratio.between(0, 1).all() or population["mexican_union_proxy"] <= 1e6:
        raise ValueError("[BLOCKED] ACS coding/ratio check failed")
    t.to_csv(OUT / "acs_college_states.csv", index=False, lineterminator="\n", float_format="%.12g")
    return t, population


def institutions():
    hd = numeric(read_csv(OLD / "HD2023.csv", {"UNITID", "INSTNM", "STABBR", "FIPS", "SECTOR", "CONTROL", "ICLEVEL"}),
                 ["UNITID", "FIPS", "SECTOR", "CONTROL", "ICLEVEL"])
    pub = hd[hd.CONTROL.eq(1) & hd.FIPS.between(1, 56)].copy()
    flags = zipped_csv(source(STAGE / "FLAGS2023.zip"), "Flags2023.csv", {"UNITID", "PRCH_F", "IDX_F", "FORM_F"})
    flags = numeric(flags, list(flags))
    pub = pub.merge(flags, on="UNITID", validate="one_to_one")
    pub["finance_unit"] = np.where(pub.PRCH_F.eq(2), pub.IDX_F, pub.UNITID).astype(int)
    return pub


def enrollment(pub, acs, annual=False):
    if annual:
        prefix, total, hisp, level = "EFY", "EFYTOTLT", "EFYHISPT", "EFFYALEV"
        ef = zipped_csv(HERE / "_cache/ipeds/EFFY2023.zip", "EFFY2023_RV.csv",
                        {"UNITID", level, total, hisp})
    else:
        prefix, total, hisp, level = "EF", "EFTOTLT", "EFHISPT", "EFALEVEL"
        ef = read_csv(OLD / "ef2023a.csv", {"UNITID", level, total, hisp})
    ef = numeric(ef, list(ef))
    ef = ef[ef[level].isin([22, 42, 32, 52])].merge(pub, on="UNITID", validate="many_to_one")
    ef["level"] = ef[level].map({22: "UG", 42: "UG", 32: "GR", 52: "GR"})
    part = ef[level].isin([42, 52])
    pt_factor = np.where(ef.level.eq("GR"), 0.361702, np.where(ef.ICLEVEL.eq(1), 0.403543, 0.335737))
    ef["fte"] = ef[total] * np.where(part, pt_factor, 1.0)
    ef["hisp_fte"] = ef[hisp] * np.where(part, pt_factor, 1.0)
    if annual:
        efia = zipped_csv(source(STAGE / "EFIA2023.zip"), "EFIA2023_RV.csv", {"UNITID", "FTEUG", "FTEGD", "XFTEUG", "XFTEGD"})
        efia = numeric(efia, ["UNITID"])
        efia = numeric(efia, ["FTEUG", "FTEGD"], flagged=True).set_index("UNITID")
        ef = ef.groupby(["UNITID", "level"], as_index=False).agg(fte=("fte", "sum"), hisp_fte=("hisp_fte", "sum"))
        annual_fte = np.array([efia.loc[u, "FTEUG" if lev == "UG" else "FTEGD"] for u, lev in zip(ef.UNITID, ef.level)])
        ef["hisp_fte"] = np.divide(ef.hisp_fte, ef.fte, out=np.zeros(len(ef)), where=ef.fte.gt(0)) * annual_fte
        ef["fte"] = annual_fte
        ef = ef.merge(pub, on="UNITID", validate="many_to_one")
    ef = ef.merge(acs[["STATE", "level", "ratio"]], left_on=["FIPS", "level"], right_on=["STATE", "level"], validate="many_to_one")
    ef["mex_fte"] = ef.hisp_fte * ef.ratio
    if not (ef.mex_fte <= ef.fte + 1e-8).all():
        raise ValueError(f"[BLOCKED] invalid {prefix} group enrollment weights")
    return ef


def finance(pub):
    cols = {"UNITID", *FUNCTIONS.values(), *("X" + v for v in FUNCTIONS.values())}
    f = zipped_csv(source(STAGE / "F2223_F1A.zip"), "f2223_f1a.csv", cols)
    f = numeric(f, ["UNITID"])
    f = f[f.UNITID.isin(pub.UNITID)]
    f = numeric(f, list(FUNCTIONS.values()), flagged=True)
    f = f.rename(columns={v: k for k, v in FUNCTIONS.items()}).set_index("UNITID")
    f["er"] = f[["instruction", "academic_support", "student_support", "institutional_support"]].sum(axis=1)
    f["responsive_net"] = f.er + f.other + f.auxiliary - f.auxiliary_sales - f.tuition - f.pell - f.education_sales
    f["responsive_gross"] = f.er + f.other + f.auxiliary
    f["responsive_after_auxiliary_sales"] = f.responsive_gross - f.auxiliary_sales
    f["public_service_net_bridge"] = f.responsive_net + f.public_service
    gross = f.er + f.research + f.public_service + f.auxiliary + f.other
    f["responsive_asset_fraction_proxy"] = ((f.er + f.auxiliary + f.other) / gross).fillna(0)
    f["depreciable_gross"] = f[["land_improvements", "infrastructure", "buildings", "equipment"]].sum(axis=1)
    f["assets_responsive_proxy"] = f.depreciable_gross * f.responsive_asset_fraction_proxy
    f["net_plant"] = f.gross_plant - f.accumulated_depreciation
    return f


def use_weights(ef, finance_ids, grad=2.0):
    ef = ef[ef.finance_unit.isin(finance_ids)]
    amount = ef.assign(den=ef.fte * np.where(ef.level.eq("GR"), grad, 1),
                       group=ef.mex_fte * np.where(ef.level.eq("GR"), grad, 1))
    grouped = amount.groupby("finance_unit")[["den", "group"]].sum()
    grouped["share"] = np.divide(grouped.group, grouped.den, out=np.zeros(len(grouped)), where=grouped.den.gt(0))
    return grouped


def measure_colleges():
    for path, wanted in PINS.items():
        actual = source(path)
        if actual != path:
            print(f"[SOURCE-MIRROR] verifying exact pinned bytes for {path.relative_to(REPO)}", flush=True)
        if sha(actual) != wanted:
            raise ValueError(f"[BLOCKED] changed primary source: {path}")
    acquisition = json.loads((OUT / "acquisition.json").read_text())
    for row in acquisition["files"]:
        if sha(REPO / row["path"]) != row["sha256"]:
            raise ValueError("[BLOCKED] changed acquired primary ZIP")
    acs, population = acs_ratios()
    pub = institutions()
    fall = enrollment(pub, acs)
    annual = enrollment(pub, acs, annual=True)
    f = finance(pub)
    base_w = use_weights(fall, f.index)
    valid = base_w.den.gt(0)
    fbase = f.reindex(base_w.index[valid])
    base_share = float((base_w.loc[valid, "share"] * fbase.er).sum() / fbase.er.sum())
    old = json.loads((FISCAL / "user_fee_allocation_2026_10_07/derived/higher_ed.json").read_text())
    if not np.isclose(base_share, old["central"]["s_U"], atol=1e-11, rtol=0):
        raise ValueError(f"[BLOCKED] reconstructed college key {base_share} differs from case {old['central']['s_U']}")
    # Preserve the case's state-by-degree distribution and total cost-adjusted
    # group-FTE share. This isolates institution allocation, rather than replacing
    # the account's population or state mix with annual headcounts.
    target = fall.groupby(["FIPS", "level"]).mex_fte.sum()
    annual_totals = annual.groupby(["FIPS", "level"]).mex_fte.sum()
    annual_raked = annual.copy()
    factors = (target / annual_totals).mask(target.eq(0) & annual_totals.eq(0), 1.0)
    if not np.isfinite(factors).all():
        raise ValueError("[BLOCKED] absent annual enrollment in a case state/degree cell")
    annual_raked["mex_fte"] *= [factors.loc[(s, l)] for s, l in zip(annual_raked.FIPS, annual_raked.level)]
    raked = annual_raked.groupby(["FIPS", "level"]).mex_fte.sum()
    if not np.allclose(raked.reindex(target.index), target, atol=1e-7, rtol=0):
        raise ValueError("[BLOCKED] college raking failed")
    concepts = ["er", "responsive_gross", "responsive_after_auxiliary_sales", "responsive_net", "depreciable_gross", "assets_responsive_proxy", "gross_plant", "net_plant", "net_depreciable", "depreciation"]
    rows, unit_frames, state_rows = [], [], []
    for scheme, ef in [("case_fall", fall), ("annual_unraked", annual), ("annual_case_state_raked", annual_raked)]:
        for grad in [1.0, 2.0, 3.0]:
            w = use_weights(ef, f.index, grad)
            w = w[w.den.gt(0)]
            unit = f.reindex(w.index).join(w).rename_axis("UNITID")
            # Normalize annual/cost-weight arms to the case's overall group FTE
            # share: no new population or graduate enrollment level is introduced.
            normalization = (base_w.group.sum() / base_w.den.sum()) / (w.group.sum() / w.den.sum())
            unit["use_share"] = unit["share"] * normalization
            unit["er_share"] = unit.er / unit.er.sum()
            for concept in concepts:
                amount = unit[concept]
                share = float((amount * unit.use_share).sum() / amount.sum())
                simple_fte_share = float((unit.group.sum() / unit.den.sum()) * normalization)
                rows.append({"scheme": scheme, "graduate_weight": grad, "concept": concept,
                             "units": len(unit), "national_amount_bn": float(amount.sum() / 1e9),
                             "use_share": share, "relative_to_simple_fte": share / simple_fte_share,
                             "factor_vs_case_er_key": share / base_share,
                             "normalization": normalization,
                             "status": "invalid_negative_asset_values" if concept in {"depreciable_gross", "assets_responsive_proxy", "gross_plant", "net_plant", "net_depreciable"} and amount.lt(0).any() else "conditional_allocation_proxy",
                             "negative_amount_units": int(amount.lt(0).sum())})
            if grad == 2:
                unit["scheme"] = scheme
                unit_frames.append(unit.reset_index()[["UNITID", "scheme", "den", "group", "use_share", *concepts]])
                geo = unit.reset_index().merge(pub[["UNITID", "STABBR", "FIPS", "INSTNM", "SECTOR"]], on="UNITID", validate="one_to_one")
                for state, block in geo.groupby("STABBR"):
                    state_rows.append({"scheme": scheme, "state": state, "fte": float(block.den.sum()),
                                       "group_fte": float(block.group.sum()), "er_bn": float(block.er.sum() / 1e9),
                                       "weighted_er_bn": float((block.use_share * block.er).sum() / 1e9),
                                       "gross_capital_bn": float(block.depreciable_gross.sum() / 1e9)})
    table = pd.DataFrame(rows)
    table.to_csv(OUT / "college_factors.csv", index=False, lineterminator="\n", float_format="%.12g")
    coverage_rows = []
    for concept in concepts:
        all_amount = float(f[concept].sum())
        covered_amount = float(fbase[concept].sum())
        group_amount = float((fbase[concept] * base_w.loc[valid, "share"]).sum())
        nonnegative = bool(f[concept].ge(0).all())
        coverage_rows.append({"concept": concept, "total_bn": all_amount / 1e9, "covered_bn": covered_amount / 1e9,
                              "covered_share": covered_amount / all_amount,
                              "unallocated_bn": (all_amount - covered_amount) / 1e9,
                              "nonnegative_allocation_bound_valid": nonnegative,
                              "factor_low_all_unallocated_to_nonmembers": group_amount / all_amount / base_share if nonnegative else None,
                              "factor_high_all_unallocated_to_members": (group_amount + all_amount - covered_amount) / all_amount / base_share if nonnegative else None})
    pd.DataFrame(coverage_rows).to_csv(OUT / "college_finance_coverage.csv", index=False, lineterminator="\n", float_format="%.12g")
    f.loc[~f.index.isin(fbase.index)].reset_index().merge(pub[["UNITID", "INSTNM", "STABBR"]], on="UNITID", validate="one_to_one").to_csv(OUT / "college_unallocated_finance.csv", index=False, lineterminator="\n", float_format="%.12g")
    pd.DataFrame(state_rows).to_csv(OUT / "college_states.csv", index=False, lineterminator="\n", float_format="%.12g")
    pd.concat(unit_frames).to_csv(OUT / "college_units.csv", index=False, lineterminator="\n", float_format="%.12g")
    missing = fall[~fall.finance_unit.isin(f.index)]
    fasb = zipped_csv(HERE / "_cache/ipeds/F2223_F2.zip", "f2223_f2.csv", {"UNITID", "F2A19", "F2A17", "F2E011", "F2E041", "F2E051", "F2E061"})
    fasb = numeric(fasb, ["UNITID"])
    public_fasb = fasb[fasb.UNITID.isin(pub.UNITID)]
    public_fasb.to_csv(OUT / "college_public_fasb.csv", index=False, lineterminator="\n")
    state_check = pd.DataFrame({"case_group_fte": target, "raked_group_fte": raked}).reset_index()
    state_check.to_csv(OUT / "college_raking.csv", index=False, lineterminator="\n", float_format="%.12g")
    response = float(f.responsive_net.sum() / f.public_service_net_bridge.sum())
    case_response = json.loads((FISCAL / "spending_keys_r5_2026_10_15/derived/item15.json").read_text())["central_response"]
    if not np.isclose(response, case_response, atol=1e-12, rtol=0):
        raise ValueError("[BLOCKED] primary college functional bridge differs from item15")
    result = {"case_er_share_acs": base_share, "case_er_share_reproduced": True,
              "case_response_reproduced": response,
              "population": population,
              "coverage": {"public_fall_fte": float(fall.fte.sum()),
                           "gasb_fall_fte": float(fall.loc[fall.finance_unit.isin(f.index), "fte"].sum()),
                           "gasb_fall_fte_share": float(fall.loc[fall.finance_unit.isin(f.index), "fte"].sum() / fall.fte.sum()),
                           "gasb_group_fte_share": float(fall.loc[fall.finance_unit.isin(f.index), "mex_fte"].sum() / fall.mex_fte.sum()),
                           "excluded_public_fasb_units": public_fasb.UNITID.astype(int).tolist(),
                           "missing_finance_units": sorted(missing.finance_unit.astype(int).unique().tolist()),
                           "state_degree_cells_raked": len(target)},
              "operating": {"already_where_enrolled": True, "new_er_factor": 1.0,
                            "responsive_net_factor_case_fall": float(table[(table.scheme == "case_fall") & table.graduate_weight.eq(2) & table.concept.eq("responsive_net")].factor_vs_case_er_key.iloc[0])},
              "limits": ["IPEDS Hispanic within state/degree is a proxy for the lineage; ACS cannot observe parental birthplace.",
                         "Annual Hispanic FTE uses attendance-weighted headcounts normalized to EFIA actual FTE; race-specific credit hours are unavailable.",
                         "Case-state raking holds the case college key's state/degree mix, not the K12 pupil mix.",
                         "Responsive-net institution weighting transports item15's conditional finance-to-NIPA bridge; fees/Pell remain fixed.",
                         "National item15 finance includes units without allocated enrollment: see concept-specific coverage and bounds, not FTE coverage alone.",
                         "Historic-cost book assets and whole-campus depreciation do not identify current replacement-cost responsive instructional assets.",
                         "Public FASB colleges are reported separately; no silent harmonization or zero-cost imputation."]}
    dump("colleges.json", result)
    print("Colleges coverage: " + json.dumps(result["coverage"], sort_keys=True))
    print(table[(table.scheme == "case_fall") & table.graduate_weight.eq(2)][["concept", "relative_to_simple_fte", "factor_vs_case_er_key"]].to_string(index=False))
    return result


def main():
    started = time.perf_counter()
    OUT.mkdir(exist_ok=True)
    colleges = measure_colleges()
    # Parks and the case adapter are separate executables, keeping primary data
    # construction independent of the account's accounting decomposition.
    subprocess.run([sys.executable, "-I", str(HERE / "parks.py")], check=True)
    subprocess.run(["bun", str(HERE / "case_prices.cjs")], check=True)
    dump("sources.json", {str(path.relative_to(REPO)): {"bytes": source(path).stat().st_size, "sha256": sha(source(path))} for path in PINS})
    print(json.dumps({"elapsed_seconds": time.perf_counter() - started,
                      "max_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      "case_key_reproduced": colleges["case_er_share_reproduced"]}, sort_keys=True))


if __name__ == "__main__":
    main()
