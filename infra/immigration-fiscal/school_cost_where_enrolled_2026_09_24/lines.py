"""Turn the per-pupil correction factors into school lines, main-case bands and audit-package bands.

The explorer's school step is school_share x response x (education line x household fraction x key
share). The key (`education_mix`) blends the school component T_s/N_s with the postsecondary component
T_p/N_p. A per-pupil correction k re-prices the group's school component only:
  blend   key share (k T_s + T_p) / (N_s + N_p): the account's key structure kept;
  school  key share k T_s / N_s: the school step keyed by schools alone (the colleges step keeps
          the published key; what splitting it would do there is reported, not proposed).
The audit package's row 6 re-blends the key at BEA's K-12 weight w (0.77-0.82): its school line uses
w T_s/N_s + (1 - w) T_p/N_p, and a re-priced version w k T_s/N_s + (1 - w) T_p/N_p. The explorer holds
one key for the whole education line, so `*_whole_line` rows also move the colleges step to the same
key; they show what the re-pricing does if that structure is kept and reproduce the audit's row 6.

Writes derived/school_key_variants.json, runs engine_school.cjs (the explorer's engine) on every
variant, and writes derived/per_pupil_weighting.csv. Run weighting.py, within_district.py and
el_check.py first.

    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy \
      python3 infra/immigration-fiscal/school_cost_where_enrolled_2026_09_24/lines.py
"""
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
COMPONENTS = FISCAL / "school_enrollment_2026_09_20/derived/updated_account_components.csv"
AUDIT_PUBLISHED = {"shared": 202.9, "personal": 251.1}     # README verdict, central values
ROW6_W = (0.77, 0.82)                                       # BEA K-12 weight, dataset_integrity spending.md #5
PREFERRED = "B_current_mexican_district_share"
LOW = "B_current_within_state_factor_fy2019_mexican_district_share"


def key_parts():
    c = pd.read_csv(COMPONENTS)
    parts = {}
    for alloc in ["personal", "shared"]:
        x = c[c.allocation == alloc].pivot(index="component", columns="group", values="spending_bn")
        parts[alloc] = dict(Ts=x.loc["school", "mexican_observed_total"], Ns=x.loc["school", "national_civilian"],
                            Tp=x.loc["P", "mexican_observed_total"], Np=x.loc["P", "national_civilian"])
    return parts


def main():
    base = json.loads((OUT / "engine_base.json").read_text())
    he = base["education_national_bn"] * base["household_fraction"]
    parts = key_parts()
    keys = base["keys"]
    for alloc, p in parts.items():   # gates: the components reproduce the model's executed key shares
        for name, share in [("education_mix", (p["Ts"] + p["Tp"]) / (p["Ns"] + p["Np"])), ("school_operating", p["Ts"] / p["Ns"])]:
            if abs(share - keys[name][alloc]["share"]) > 1e-8:
                raise SystemExit(f"[BLOCKED] {name}/{alloc} share {share} != model {keys[name][alloc]['share']}")

    def blend(k):
        return {a: he * (k * p["Ts"] + p["Tp"]) / (p["Ns"] + p["Np"]) for a, p in parts.items()}

    def school(k):
        return {a: he * k * p["Ts"] / p["Ns"] for a, p in parts.items()}

    def row6(w, k):
        return {a: he * (w * k * p["Ts"] / p["Ns"] + (1 - w) * p["Tp"] / p["Np"]) for a, p in parts.items()}

    r = pd.read_csv(OUT / "r_by_spec.csv").set_index("spec")
    wd = json.loads((OUT / "within_district.json").read_text())
    el = json.loads((OUT / "el_within_district.json").read_text())
    concepts = pd.read_csv(OUT / "r_other_concepts.csv").set_index(["concept", "weighting"])
    link = json.loads((OUT / "linkage.json").read_text())
    acct = json.loads((OUT / "account_embedded_price.json").read_text())
    school_all = wd["TCURELSCS"]["factor_all_districts"]
    school_state_local = wd["TCURELSCSE"]["factor_all_districts"]
    k_pref = r.k[PREFERRED] * school_all
    k_low = r.k[LOW] * school_state_local
    el_premium = el["within_district_el_premium_per_group_pupil_fy2024"] / r.group_price[PREFERRED]
    # BEA consumption includes depreciation: key a share c of it by capital outlay (or interest) per pupil.
    cfc = 312.559 / 2550.362    # state-local CFC / consumption 2024, BEA T3.10.5 lines 51 and 47
    rc = concepts.R[("pp", "mexican_district_share")]
    bea_capout = (1 - cfc) + cfc * concepts.R[("pp_capout", "mexican_district_share")] / rc
    bea_interest = (1 - cfc) + cfc * concepts.R[("pp_interest", "mexican_district_share")] / rc
    core = concepts.R[("pp_core", "mexican_district_share")] / rc
    count_ratio = link["group_pupils_admin"] / acct["target_pupils"]

    variants, meta = {}, {}

    def add(name, targets, **info):
        variants[name] = {"school_target_bn": targets}
        meta[name] = info

    add("published", blend(1.0), spec="published", family="", weighting="", key="blend", R=acct["r_embedded_personal"], k=1.0)
    add("school_key_only", school(1.0), spec="school_key_only", family="", weighting="", key="school", R=acct["r_embedded_personal"], k=1.0)
    for spec, row in r.iterrows():
        for key, fn in [("blend", blend), ("school", school)]:
            add(f"{spec}|{key}", fn(row.k), spec=spec, family=row.family, weighting=row.weighting, key=key, R=row.R, k=row.k)
    extra = [
        ("preferred_district_and_school_level", k_pref, "B, Mexican district share, x SLFS school-level factor (all funds)"),
        ("low_fy2019_factor_state_local_school_level", k_low, "B, FY2019 within-state factor, x SLFS factor (state and local funds)"),
        ("high_preferred_plus_el_upper_bound", k_pref * (1 + el_premium), "preferred x within-district EL premium (upper bound)"),
        ("preferred_bea_depreciation_by_capital_outlay", k_pref * bea_capout, "preferred, 12.3% depreciation keyed by capital outlay"),
        ("preferred_bea_depreciation_by_interest", k_pref * bea_interest, "preferred, 12.3% depreciation keyed by interest"),
        ("preferred_instruction_support_only", k_pref * core, "preferred, instruction + support spending only"),
        ("preferred_admin_pupil_count", k_pref * count_ratio, "preferred x CCD/ACS pupil count over the account's"),
    ]
    for name, k, label in extra:
        for key, fn in [("blend", blend), ("school", school)]:
            add(f"{name}|{key}", fn(k), spec=name, family="B+", weighting="mexican_district_share", key=key, R=None, k=k, label=label)
    # The brief's literal instruction: R x the current line (double counts the state prices the key holds).
    for spec in [PREFERRED, "C_current_mexican_district_share"]:
        mix = {a: r.R[spec] * keys["education_mix"][a]["target_bn"] for a in parts}
        add(f"literal_R_times_line|{spec}", mix, spec=f"literal_R_times_line:{spec}", family="literal",
            weighting="mexican_district_share", key="blend", R=r.R[spec], k=r.R[spec])
    # Both steps split: schools on the school component (at k), colleges on the postsecondary component.
    post = {a: he * p["Tp"] / p["Np"] for a, p in parts.items()}
    for label, k in [("split_both_keys", 1.0), ("split_both_keys|preferred", k_pref)]:
        variants[label] = {"school_target_bn": school(k), "college_target_bn": post}
        meta[label] = dict(spec=label.split("|")[0] + ("_preferred" if "|" in label else ""), family="key", weighting="",
                           key="split_both", R=None, k=k, label="schools keyed by the school component, colleges by postsecondary")
    # One key for the whole line, as the explorer holds it: the re-priced key also moves the colleges step.
    variants["blend_whole_line|preferred"] = {"school_target_bn": blend(k_pref), "college_target_bn": blend(k_pref)}
    meta["blend_whole_line|preferred"] = dict(spec="preferred_district_and_school_level", family="B+", weighting="mexican_district_share",
                                              key="blend_whole_line", R=None, k=k_pref, label="re-priced key on both education steps")
    tiers = [("preferred", "preferred_district_and_school_level", k_pref),
             ("low", "low_fy2019_factor_state_local_school_level", k_low),
             ("high", "high_preferred_plus_el_upper_bound", k_pref * (1 + el_premium))]
    for w in ROW6_W:
        add(f"row6_w{w}", row6(w, 1.0), spec=f"audit_row6_w{w}", family="audit", weighting="", key=f"row6_w{w}", R=None, k=1.0)
        for tag, spec, k in tiers:
            add(f"row6_w{w}|{tag}", row6(w, k), spec=spec, family="audit", weighting="mexican_district_share",
                key=f"row6_w{w}", R=None, k=k)
        # The audit's row 6 re-keys the whole education line; both steps at the re-blended key.
        for tag, k in [("", 1.0), ("|preferred", k_pref)]:
            name = f"row6_w{w}_whole_line{tag}"
            variants[name] = {"school_target_bn": row6(w, k), "college_target_bn": row6(w, k)}
            meta[name] = dict(spec=f"audit_row6_w{w}_whole_line" if not tag else "preferred_district_and_school_level",
                              family="audit", weighting="" if not tag else "mexican_district_share",
                              key=f"row6_w{w}_whole_line", R=None, k=k, label="row-6 key on both education steps")

    (OUT / "school_key_variants.json").write_text(json.dumps(variants, indent=1) + "\n")
    run = subprocess.run(["node", str(HERE / "engine_school.cjs")], capture_output=True, text=True)
    print(run.stdout[-3000:])
    if run.returncode:
        print(run.stderr[-2000:])
        raise SystemExit("[BLOCKED] engine_school.cjs failed")
    lines = pd.read_csv(OUT / "engine_school_lines.csv").set_index("variant")

    # Audit package: its row 6 re-blends the education key at w. A re-priced variant with the same key
    # moves the audit total by the change in main-case band ends against its unre-priced row-6 base
    # (the audit adds its deltas to the main case's band ends: low = shared allocation, high = personal).
    # The base rows' own change against the published main case is the row-6 effect, to set beside the
    # audit's -2.2 to -4.8 (spending.md #5).
    pub = lines.loc["published"]
    records = []
    for name, info in meta.items():
        L = lines.loc[name]
        rec = dict(spec=info["spec"], family=info["family"], weighting=info["weighting"], key_treatment=info["key"],
                   R=info["R"], k=info["k"], label=info.get("label", ""),
                   school_low_bn=L.school_low_bn, school_high_bn=L.school_high_bn,
                   change_low_bn=L.school_change_low_bn, change_high_bn=L.school_change_high_bn,
                   main_low_bn=L.main_low_bn, main_high_bn=L.main_high_bn,
                   main_change_low_bn=L.main_low_bn - pub.main_low_bn, main_change_high_bn=L.main_high_bn - pub.main_high_bn)
        if info["key"].startswith("row6_w") and "|" in name:
            B = lines.loc[name.split("|")[0]]
            lo, hi = L.main_low_bn - B.main_low_bn, L.main_high_bn - B.main_high_bn
            rec.update(school_change_vs_row6_low_bn=L.school_low_bn - B.school_low_bn,
                       school_change_vs_row6_high_bn=L.school_high_bn - B.school_high_bn,
                       audit_change_low_bn=lo, audit_change_high_bn=hi,
                       audit_total_low_bn=AUDIT_PUBLISHED["shared"] + lo, audit_total_high_bn=AUDIT_PUBLISHED["personal"] + hi)
        records.append(rec)
    table = pd.DataFrame(records)
    table.to_csv(OUT / "per_pupil_weighting.csv", index=False, lineterminator="\n", float_format="%.4f")
    summary = dict(k_preferred=k_pref, k_low=k_low, k_high=k_pref * (1 + el_premium), el_premium=el_premium,
                   bea_capout_factor=bea_capout, bea_interest_factor=bea_interest, core_factor=core,
                   count_ratio=count_ratio, school_level_factor_all_funds=school_all,
                   school_level_factor_state_local=school_state_local, cfc_share=cfc,
                   row6_school_lines={str(w): [lines.loc[f"row6_w{w}"].school_low_bn, lines.loc[f"row6_w{w}"].school_high_bn]
                                      for w in ROW6_W},
                   # Row 6's change in the education line's allocation before any response, to set
                   # beside the audit's -3.5 (-4.8 to -2.2).
                   row6_allocation_change_bn={str(w): {a: row6(w, 1.0)[a] - keys["education_mix"][a]["target_bn"]
                                                       for a in parts} for w in ROW6_W})
    (OUT / "lines_summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    show = table[table.spec.isin(["published", PREFERRED, "preferred_district_and_school_level",
                                  "low_fy2019_factor_state_local_school_level", "high_preferred_plus_el_upper_bound"])]
    pd.set_option("display.width", 250)
    print(show[["spec", "key_treatment", "k", "school_low_bn", "school_high_bn", "change_low_bn", "change_high_bn",
                "main_low_bn", "main_high_bn"]].to_string(index=False))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    sys.exit(main())
