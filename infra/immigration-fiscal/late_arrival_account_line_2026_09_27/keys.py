"""Step 1: every allocation key of the complete account restricted to each generation.

For each key, allocation (personal, shared) and convention ((a) own generation, (b) minors with their
parents), the union's key total is split into the three generations' totals on the same per-person
vectors the producers use:
  - CPS receipt and spending keys: the account's definitions (cps_imputation_keys_2026_09_23/common.py,
    gated to the producers' exports by that lane's gate.py); the shared allocation splits each SPM unit's
    total equally over its members, so a mixed-generation unit splits by person;
  - modeled owner property: the owner-housing model of all_age_ledger_2026_09_17 (state effective rate
    times property value over household members, split equally in the SPM unit), which
    full_account_receipts_2026_09_20 uses as an explicit override;
  - MEPS payer keys: the spending builder's age-band x US-birth transport with its coverage exposure;
  - school, postsecondary (the account's item P, non-school state and local capital per head by state)
    and their mix: school_enrollment_2026_09_20's per-pupil cost times measured enrollment by age and
    origin cell, and the Census 2024 finance refresh of item P (macro_closure_2026_09_19);
  - public order and safety by use (cj_use_allocation_2026_09_23): per-head parts by population, prisons
    by the lane's custody split (Mexico-born to G1, US-born to G2 and G3plus by their counts aged 18-64,
    the key's own base), arrest-keyed parts like custody (the lane's proxy), ICE interior custody to G1;
  - Medicaid with uninsured use (uncompensated_care_2026_09_23): the Medicaid key plus each generation's
    part of the lane's inside-account under-charge g x (s - k) x N, with s its uninsured person-years
    and k its offsets on the account's keys, at the arms that give the lane's low and high values.
Gates (exit 1): every union key total equals the producer's published total (1e-9 relative); the three
generations sum to the union (1e-12 relative); the use and uninsured keys reproduce the model's cells.
Outputs: derived/generation_keys.csv (totals) and derived/generation_key_shares.json (shares).
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/generation_account_2026_09_24/keys.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import frame as F

C = F.C
ALLOC = ["personal", "shared"]
FAILS = []


def gate(label, ok, detail=""):
    print(f"  {'✓' if ok else '✗'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def owner_property(d):
    """all_age_ledger analyze.matrices column 5: extend_ledger property_tax_owner, SPM-shared in both."""
    params = pd.read_csv(F.FISCAL / "gen_ledger_extension_2026_09_16/state_parameters.csv").set_index("fips")
    rate = d.GESTFIPS.map(params.property_tax_effective_rate).to_numpy(float)
    members = d.groupby("PH_SEQ").PPPOS.transform("size").to_numpy(float)
    owner = d.H_TENURE.eq(1).to_numpy()
    person = np.where(owner, rate * d.HPROP_VAL.to_numpy(float), 0.0) / members
    return C.unit_equal(person, C.spm_index(d)), params


def meps_keys(d):
    """full_account_spending_2026_09_20/builder.py build_keys, MEPS payer means (personal = shared)."""
    sys.path.insert(0, str(F.FISCAL / "build"))
    from meps_health_transport_2024 import read_meps, donor_model
    meps = F.ROOT / "sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip"
    md, _ = read_meps(meps, meps.with_name("h256su.txt"))
    cells, codes, _ = donor_model(md, d, False)
    valid = md.PERWT24F.gt(0) & md.AGE24X.ge(0) & md.BORNUSA.isin([1, 2])
    sample = md.loc[valid]
    index = pd.MultiIndex.from_frame(cells[["age_band", "born"]])
    exposure = ~(d.PUB.eq(0) & d.PRIV.eq(0)).to_numpy()
    if d.loc[~exposure, "A_AGE"].gt(0).any():
        raise ValueError("Reference exclusion includes noninfant")
    out = {}
    for name, cols in [("medicare", ["TOTMCR24"]), ("medicaid", ["TOTMCD24"]), ("va_medical", ["TOTVA24"]),
                       ("tricare", ["TOTTRI24"]), ("health_other", ["TOTVA24", "TOTTRI24", "TOTOFD24", "TOTSTL24"])]:
        sums = sample.assign(wx=sample[cols].sum(axis=1) * sample.PERWT24F).groupby(["age_band", "born"]).wx.sum()
        pop = sample.groupby(["age_band", "born"]).PERWT24F.sum()
        mean = (sums / pop).reindex(index)
        if mean.isna().any():
            raise ValueError("Unmatched payer cell")
        out[name] = mean.to_numpy()[codes] * exposure
    return out, cells, codes, exposure


def school_keys(d, civ, params):
    """school_enrollment_2026_09_20 'all_ages' school component and macro_closure's refreshed item P."""
    sys.path.insert(0, str(F.FISCAL / "school_enrollment_2026_09_20"))
    import measurement
    rates = pd.read_csv(F.FISCAL / "school_enrollment_2026_09_20/derived/national_rates.csv").set_index("cell").rate
    march = d.assign(PRTAGE=d.A_AGE)
    code = measurement.cells(march)
    code[~civ] = "out"
    rate = np.array([0.0 if c == "out" else rates[c] for c in code])
    cost = d.GESTFIPS.map(params.per_pupil_current_spending).to_numpy(float)
    school = cost * rate
    sys.path.insert(0, str(F.FISCAL / "macro_closure_2026_09_19"))
    import finance_vintage as fv
    current, _ = fv.read_finance(F.FISCAL / "macro_closure_2026_09_19/_cache", 2024)
    pinned = json.loads((F.FISCAL / "ledger_absolute_2026_09_17/params/params.json").read_text())
    source = next(r for r in pinned["staged_files"] if r["path"].endswith("NST-EST2024-ALLDATA.csv"))
    if F.sha(source["path"]) != source["sha256"]:
        raise ValueError("State population source changed")
    population = fv.us_state_population(pd.read_csv(source["path"]))
    p_item = d.GESTFIPS.map(current.P / population).to_numpy(float)
    index = C.spm_index(d)
    return {"personal": {"school": school, "P": p_item},
            "shared": {"school": C.unit_equal(school, index), "P": p_item}}


def generation_shares(totals):
    union = totals.sum(axis=0)
    return np.where(union != 0, totals / np.where(union == 0, 1, union), 0.0)


def main():
    print("[frame]", flush=True)
    d = F.load()
    civ, union, gens = F.masks(d)
    omega, rule, _ = F.assignments(d, civ, union, gens)
    W = d[F.REPS].to_numpy(float)
    w = W[:, 0]
    index = C.spm_index(d)
    rows, shares = [], {"receipt": {a: {} for a in ALLOC}, "spending": {a: {} for a in ALLOC}}

    def record(side, allocation, key, vector, published=None, national_published=None):
        v = np.asarray(vector, float)
        national = float(v[civ] @ w[civ])
        entry = {}
        for conv in ("a", "b"):
            gt = F.totals(v, w, omega[conv])
            union_total = float(v[union] @ w[union])
            gate_ok = abs(gt.sum() - union_total) <= 1e-12 * max(abs(union_total), 1.0)
            if not gate_ok:
                gate(f"{side}/{allocation}/{key}/{conv} generations sum to the union", False)
            entry[conv] = (gt / union_total).tolist() if union_total else [0.0, 0.0, 0.0]
            rows.append(dict(side=side, allocation=allocation, key=key, convention=conv, national=national,
                             union=union_total, **dict(zip(F.GENS, gt)), published_union=published,
                             rel_diff=(abs(union_total / published - 1) if published else np.nan)))
        if published is not None:
            union_total = float(v[union] @ w[union])
            ok = abs(union_total / published - 1) < 1e-9
            if national_published is not None:
                ok = ok and abs(national / national_published - 1) < 1e-9
            if not ok:
                gate(f"{side}/{allocation}/{key} reproduces the published union total", False,
                     f"{union_total:.6f} vs {published:.6f}")
        shares[side][allocation][key] = entry

    print("[receipt keys]", flush=True)
    pub_r = pd.read_csv(F.FISCAL / "full_account_receipts_2026_09_20/derived/allocation_keys.csv")
    rkeys = C.receipt_keys(d, index)
    owner, params = owner_property(d)
    for allocation in ALLOC:
        for key, vector in rkeys[allocation].items():
            p = pub_r.query("allocation == @allocation and allocation_key == @key")
            record("receipt", allocation, key, vector, float(p.target_key_total.iloc[0]), float(p.national_key_total.iloc[0]))
        p = pub_r.query("allocation == @allocation and allocation_key == 'resident_population'")
        record("receipt", allocation, "resident_population", np.ones(len(d)), float(p.target_key_total.iloc[0]))
        record("receipt", allocation, "modeled_owner_property", owner)
    checked = sum(1 for r in rows if r["side"] == "receipt" and r["convention"] == "a" and r["published_union"])
    gate(f"{checked} receipt key totals reproduce allocation_keys.csv (1e-9)", not FAILS)

    # The owner-property override and its national pool (category_allocations, modeled_owner_property).
    cats = pd.read_csv(F.FISCAL / "full_account_receipts_2026_09_20/derived/category_allocations.csv")
    own = cats.query("scenario_id == 'cbo_collective' and category == 'modeled_owner_property'").set_index("allocation")
    for allocation in ALLOC:
        union_bn = float(owner[union] @ w[union]) / 1e9
        national_bn = float(owner[civ] @ w[civ]) / 1e9
        gate(f"owner property ({allocation}) reproduces the override {own.loc[allocation, 'target_bn']:.6f}",
             abs(union_bn - own.loc[allocation, "target_bn"]) < 1e-6
             and abs(national_bn - own.loc[allocation, "national_bn"]) < 1e-6, f"{union_bn:.9f} / {national_bn:.6f}")

    print("[spending keys]", flush=True)
    pub_s = pd.read_csv(F.FISCAL / "full_account_spending_2026_09_20/derived/incidence_keys.csv")
    skeys = C.spending_vectors(d, index)
    medical, cells, codes, exposure = meps_keys(d)
    n_before = len(FAILS)
    for allocation in ALLOC:
        vectors = dict(skeys[allocation])
        vectors.update(medical)
        for key, vector in vectors.items():
            p = pub_s.query("allocation == @allocation and key == @key")
            record("spending", allocation, key, vector, float(p.target_key_total.iloc[0]), float(p.national_key_total.iloc[0]))
    gate(f"{len(ALLOC) * (len(skeys['personal']) + len(medical))} CPS and MEPS spending keys reproduce incidence_keys.csv (1e-9)",
         len(FAILS) == n_before)

    print("[education keys]", flush=True)
    edu = school_keys(d, civ, params)
    comp = pd.read_csv(F.FISCAL / "school_enrollment_2026_09_20/derived/updated_account_components.csv")
    for allocation in ALLOC:
        part = comp.query("allocation == @allocation").set_index(["group", "component"]).signed_bn
        for name, vec in edu[allocation].items():
            u = float(vec[union] @ w[union]) / 1e9
            n = float(vec[civ] @ w[civ]) / 1e9
            want_u, want_n = -part[("mexican_observed_total", name)], -part[("national_civilian", name)]
            gate(f"{name} ({allocation}) reproduces the account component {want_u:.6f} / {want_n:.3f}",
                 abs(u - want_u) < 1e-6 and abs(n - want_n) < 1e-5, f"{u:.9f} / {n:.6f}")
        mix = edu[allocation]["school"] + edu[allocation]["P"]
        for key, vec in [("school_operating", edu[allocation]["school"]), ("postsecondary", edu[allocation]["P"]),
                         ("education_mix", mix)]:
            p = pub_s.query("allocation == @allocation and key == @key")
            record("spending", allocation, key, vec, float(p.target_key_total.iloc[0]), float(p.national_key_total.iloc[0]))

    model = json.loads((F.FISCAL / "assumption_explorer_2026_09_21/derived/model.json").read_text())
    lines = {l["id"]: l for l in model["spending"]["lines"]}

    print("[justice use key]", flush=True)
    split = pd.read_csv(F.FISCAL / "cj_use_allocation_2026_09_23/derived/central_split.csv").set_index("component")
    age = d.A_AGE.to_numpy()
    pop_share = {c: F.totals(np.ones(len(d)), w, omega[c]) / F.TARGET_POP for c in ("a", "b")}
    t1864 = {c: F.totals(((age >= 18) & (age <= 64)).astype(float), w, omega[c]) for c in ("a", "b")}
    adults = {c: F.totals((age >= 18).astype(float), w, omega[c]) for c in ("a", "b")}
    use_parts = {}
    for conv in ("a", "b"):
        # Late-arrival lane: G1's parts (custody, ICE interior) go to the G1 cells by their counts aged 18-64, the
        # rule the lane uses for the US-born. [INFERENCE: FLAGGED; no custody data by age at arrival.]
        isg1 = np.array(F.IS_G1, float)
        pop = pop_share[conv]
        us_born = t1864[conv] * (1 - isg1) / (t1864[conv] * (1 - isg1)).sum()
        g1_1864 = t1864[conv] * isg1 / (t1864[conv] * isg1).sum()
        # Custody: Mexico-born part to G1 (convention (b) moves no adults), US-born by counts aged 18-64.
        custody = split.loc["prisons", "mexico_born_bn"] * g1_1864 + split.loc["prisons", "us_born_bn"] * us_born
        custody_share = custody / custody.sum()
        per_head = sum(split.loc[c, "mexico_born_bn"] + split.loc[c, "us_born_bn"] for c in split.index
                       if c not in ("prisons", "police_ice_interior"))
        arrest = split.unsplit_bn.sum()
        parts = dict(per_head=per_head * pop, custody=custody, arrest_like_custody=arrest * custody_share,
                     arrest_per_adult=arrest * adults[conv] / adults[conv].sum(),
                     ice_interior=split.loc["police_ice_interior", "use_bn"] * g1_1864)
        use_parts[conv] = parts
    use_total = split.use_bn.sum()
    per_head_ref = split.per_head_bn.sum()
    gate("justice components sum to the model's use cell",
         abs(use_total - lines["public_order_safety"]["keys"]["use"]["personal"]["target_bn"]) < 1e-5,
         f"{use_total:.6f}")
    for conv in ("a", "b"):
        p = use_parts[conv]
        central = p["per_head"] + p["custody"] + p["arrest_like_custody"] + p["ice_interior"]
        alt = p["per_head"] + p["custody"] + p["arrest_per_adult"] + p["ice_interior"]
        # central_split.csv carries six decimals, so the parts close to the lane's total within 1e-5 bn;
        # the model cell is then split by the parts' shares, which closes exactly.
        gate(f"use key ({conv}) generations sum to the lane's total", abs(central.sum() - use_total) < 1e-5
             and abs(alt.sum() - use_total) < 1e-5, f"{central.sum() - use_total:+.1e}")
        for allocation in ALLOC:
            shares["spending"][allocation].setdefault("use", {})[conv] = (central / central.sum()).tolist()
            shares["spending"][allocation].setdefault("use|arrest_per_adult", {})[conv] = (alt / alt.sum()).tolist()
            # Raw-coding variant: population part plus the raw change, split like the central change.
            pop_part = pop_share[conv] * per_head_ref
            change = central - pop_part
            raw_change = lines["public_order_safety"]["keys"]["use_raw_coding"]["personal"]["target_bn"] - per_head_ref
            raw = pop_part + raw_change * change / change.sum()
            shares["spending"][allocation].setdefault("use_raw_coding", {})[conv] = (raw / raw.sum()).tolist()
        rows.append(dict(side="spending", allocation="both", key="use", convention=conv, national=np.nan,
                         union=central.sum(), **dict(zip(F.GENS, central)),
                         published_union=use_total, rel_diff=abs(central.sum() / use_total - 1)))

    print("[uninsured-use keys]", flush=True)
    uc = json.loads((F.FISCAL / "uncompensated_care_2026_09_23/derived/summary.json").read_text())
    exposure_py = d.NOCOV_CYR.eq(3).to_numpy(float) + 0.5 * d.NOCOV_CYR.eq(2).to_numpy(float)
    all_py = float(exposure_py[civ] @ w[civ])
    aha, uplift = uc["aha_national_bn"], uc["uplift_2024"]
    offsets = {2013: dict(total_uc=84.9 - 8.1 - 2.1, programs={"medicaid": 13.5, "medicare": 8.0,
                                                               "state_local": 9.8 + 7.3 + 3.0 + 1.5 + 0.1}),
               2017: dict(total_uc=42.4 - 10.3 - 2.3, programs={"medicaid": 9.8, "state_local": 9.9 + 1.3})}
    for conv in ("a", "b"):
        py_g = F.totals(exposure_py, w, omega[conv])
        py_t = py_g.sum()
        py_o = all_py - py_t
        # The lane's k: each program's line, personal allocation target over the national line.
        kg = {}
        for key, line_id in [("medicaid", "medicaid_and_chip_other_medical"), ("medicare", "medicare"),
                             ("health_other", "health_services")]:
            line = lines[line_id]
            cell = line["keys"][line["preferred_key"]]["personal"]["target_bn"]
            kg[key] = cell * np.array(shares["spending"]["personal"][line["preferred_key"]][conv]) / line["national_bn"]
        kg["per_head"] = 0.120245 * pop_share[conv]
        for r, suffix in [(1.0, ""), (0.7, "_07")]:
            arms = []
            for year, spec in offsets.items():
                total_off = sum(spec["programs"].values())
                g = total_off / spec["total_uc"]
                for sl in ("health_other", "per_head"):
                    k = sum(v / total_off * kg[sl if p == "state_local" else p] for p, v in spec["programs"].items())
                    s = r * py_g / (r * py_t + py_o)
                    for n in (aha, aha * uplift):
                        arms.append(g * (s - k) * n)
            arms = np.array(arms)
            totals_ = arms.sum(axis=1)
            for end, pick in [("low", int(np.argmin(totals_))), ("high", int(np.argmax(totals_)))]:
                want = uc[f"inside_undercharged_bn_use_{r}"][0 if end == "low" else 1]
                gate(f"uninsured {r} {end} ({conv}) reproduces the lane", abs(totals_[pick] - want) < 1e-9,
                     f"{totals_[pick]:.9f} vs {want:.9f}")
                key = f"uninsured_use{suffix}_{end}"
                for allocation in ALLOC:
                    base = lines["medicaid_and_chip_other_medical"]["keys"]["medicaid"][allocation]["target_bn"]
                    med = base * np.array(shares["spending"][allocation]["medicaid"][conv])
                    cellg = med + arms[pick]
                    cell = lines["medicaid_and_chip_other_medical"]["keys"][key][allocation]["target_bn"]
                    if abs(cellg.sum() - cell) > 1e-6:
                        gate(f"{key} ({allocation}, {conv}) reproduces the model cell", False, f"{cellg.sum()} vs {cell}")
                    shares["spending"][allocation].setdefault(key, {})[conv] = (cellg / cellg.sum()).tolist()
    shares["spending"]["personal"]["external"] = shares["spending"]["shared"]["external"] = {c: [0] * len(F.GENS) for c in "ab"}
    shares["receipt"]["personal"]["none"] = shares["receipt"]["shared"]["none"] = {c: [0] * len(F.GENS) for c in "ab"}

    # Federal-gap arm: CPS liability plus the BEA gap on the high-AGI key (category_allocations).
    gap = cats.query("scenario_id == 'federal_gap_high_agi' and category == 'federal_income_tax'").set_index("allocation")
    tax = pd.read_csv(F.FISCAL / "admin_tax_checks_2026_09_19/derived/group_components.csv")
    for allocation in ALLOC:
        fb = rkeys[allocation]["federal_liability"]
        hi = rkeys[allocation]["federal_high_agi"]
        nat_fb = float(tax.query("allocation == @allocation and group == 'national_civilian' and metric == 'federal_before_refundable'").value.iloc[0]) / 1e9
        k_hi = float(hi[union] @ w[union]) / float(hi[civ] @ w[civ])
        p3 = gap.loc[allocation, "national_bn"]
        entry = {}
        for conv in ("a", "b"):
            fbg = F.totals(fb, w, omega[conv]) / 1e9
            hig = F.totals(hi, w, omega[conv]) / float(hi[civ] @ w[civ])
            cellg = fbg + (p3 - nat_fb) * hig
            entry[conv] = (cellg / cellg.sum()).tolist()
            if conv == "a":
                gate(f"federal-gap arm ({allocation}) reproduces {gap.loc[allocation, 'target_bn']:.6f}",
                     abs(cellg.sum() - gap.loc[allocation, "target_bn"]) < 1e-6, f"{cellg.sum():.9f}")
        shares["receipt"][allocation]["observed_liability_plus_positive_gap_high_agi"] = entry

    out = pd.DataFrame(rows)
    F.OUT.mkdir(exist_ok=True)
    out.to_csv(F.OUT / "generation_keys.csv", index=False, lineterminator="\n")
    meta = dict(convention_rules={k: float(w[union & (rule == k)].sum()) for k in sorted(set(rule[union]))},
                population={c: F.totals(np.ones(len(d)), w, omega[c]).tolist() for c in ("a", "b")},
                adults_18plus={c: adults[c].tolist() for c in ("a", "b")},
                use_parts={c: {k: v.tolist() for k, v in use_parts[c].items()} for c in ("a", "b")})
    (F.OUT / "generation_key_shares.json").write_text(json.dumps(dict(meta=meta, shares=shares), indent=1) + "\n")
    worst = out[out.key.ne("use")].dropna(subset=["rel_diff"]).rel_diff.max()
    print(f"  keys written: {len(out)} rows; worst relative difference to published totals {worst:.1e}"
          " (the use key closes to its six-decimal source within 1e-5 bn)")
    if FAILS:
        print(f"✗ {len(FAILS)} gate(s) failed: {FAILS}")
        sys.exit(1)
    print("  ✓ all key gates passed")


if __name__ == "__main__":
    main()
