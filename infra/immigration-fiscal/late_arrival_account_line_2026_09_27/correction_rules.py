"""Step 4: generation splits of the adopted corrections outside the tax-records block and the three
outside-check re-keys (those are in stack_split.py and external_split.py).

Each rule is written per source lane; every split adds to the union's figure. Amounts are the
union's changes before `package.cjs` scales them by the stack (run_generations.cjs does that per
generation). Convention (a) counts each person in their own generation; (b) counts minors in the
parents' generation (F.assignments).

- Pooled medical (`medical_ethnicity_pooled_2026_09_23/translate.py`): each account line moves by
  its target x (key-weighted ratio - 1), the key weights being the union's MEPS key dollars in the ten
  age x US-birth cells. A generation's part is its own key dollars in each cell times that cell's
  ratio - 1 (winsor_p995, the adopted specification). Exact. The Medicaid ratio part, which the LTSS
  carve-out re-bases onto the key without home health, splits by the same cell rule on that key.
- Long-term care (`ltss_share_2026_09_23/translate.py`, central): each category moves by
  L_c x (users' share - key rate) and the rest of the line by R x hf x (k_ex - k). The removed charge
  L_c x key rate splits as the MEPS Medicaid key does; the remainder term by each generation's own
  key shares; the users' charge L_c x share_c by the users' generation: in each TAF age group of the
  category, the union's users are Mexico-born in the proportion the ACS 2024 proxy population shows
  (institutional residents for nursing facilities; community Medicaid enrollees with a cognitive
  difficulty for ICF/IID; all residents for mental-health facilities; community Medicaid enrollees
  with a self-care or independent-living difficulty for HCBS, as the lane's central proxies), and
  the US-born users split between the second and third generations as the CPS's union members with
  Medicaid in that age group do. Age groups are weighted by TAF dollars x the union's share of the
  proxy population. [INFERENCE: the ACS has no parents' birthplace, so the US-born split is the
  CPS household population's.]
- Schools priced where enrolled (`school_cost_where_enrolled_2026_09_24/lines.py`, row 6 at w 0.77
  and 0.82, preferred k): the line's target is he x (w k T_s/N_s + (1 - w) T_p/N_p). A generation
  takes its own pupils' school component T_s,g and its own postsecondary component T_p,g (keys.py);
  k is one district premium for all the group's pupils, so it scales every generation's pupils alike.
- Benefits (`admin_benefit_keys_2026_09_24`, package_central): the lane scales the union's key share
  by one factor per programme, so every generation's share takes the same factor: the change splits
  as the line's key does. FLAGGED (the factor mixes state geography and Hispanic reporting, which
  need not fall alike on the generations); the band gives the change to G1 alone and to the US-born
  alone.
- Justice (audit row 7 and the booking factor): both move the arrest-keyed parts of the use key, so
  they split as those parts do (keys.py: like custody, central; per adult, alternative).
- Lane constants:
  - row 8, unallocable state and local spending at the all-spending response: a response change on
    the general-public-services line, keyed per head: splits by population;
  - row 9, MEPS donor filter (bounded, -0.8): splits as the Medicaid and Medicare keys it acts on,
    by their union dollars. FLAGGED;
  - row 10, foster care keyed by WIC (bounded, -1.5): the WIC key's split. FLAGGED; alternative:
    the union's children;
  - small audit items (-0.1): population. FLAGGED;
  - shelter: the account's charge (four lines' keys, as the shelter lane maps NYC's increase) leaves
    every generation; the use-based charge is recent arrivals, the first generation;
  - care and household services (-4.15): hours taxes and output by the generation of the union's
    household-service workers (maids, childcare), elder care by that of its home-care aides: the
    Mexico-born share of the union's hours from the care lane's ACS table, the US-born part split by
    the CPS union workers in those occupations. [INFERENCE: the care lane's hours are ACS; the
    US-born split uses CPS persons, not hours.]

For comparison only, the brief's literal rule for the fill-in component of the tax-records stack
(stack_split.py splits it exactly): each of its cells by the generations' shares of the union's
imputed key dollars (the CPS lane's 5% material-imputation flags), written as `fill_in_literal`.

Gates (exit 1): every union figure is reproduced from its lane's own outputs (medical line deltas
1e-9 bn, LTSS parts 1e-9 bn, school targets 1e-9 bn, shelter over-charge 0.05 $m); every split adds
to the union (1e-12 bn).
Output: derived/correction_rules.json. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/generation_account_2026_09_24/correction_rules.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import json  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import frame as F  # noqa: E402
import acs_rates  # noqa: E402  (late-arrival lane)

C = F.C
NG = len(F.GENS)
FAILS = []
MED = F.FISCAL / "medical_ethnicity_pooled_2026_09_23/derived"
LTSS = F.FISCAL / "ltss_share_2026_09_23"
SCHOOL = F.FISCAL / "school_cost_where_enrolled_2026_09_24/derived"
BENEFITS = F.FISCAL / "admin_benefit_keys_2026_09_24/derived/line_deltas.json"
SHELTER = F.FISCAL / "migrant_shelter_costs_2026_09_23/derived"
CARE = F.FISCAL / "care_household_services_2026_09_23/derived"
MEPS = F.ROOT / "sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip"
HH = ["HHAMCD24", "HHNMCD24"]
SPEC = "winsor_p995"
TRANSPORT_LABELS = ["0-17", "18-34", "35-49", "50-64", "65+"]
NAT = {1: "us_born", 2: "foreign_born"}
# account line -> (MEPS key, cells.csv measure)
MED_LINES = {"medicaid_and_chip_other_medical": ("medicaid", "medicaid"), "medicare": ("medicare", "medicare"),
             "health_services": ("health_other", "other_public"), "military_medical": ("tricare", "tricare"),
             "veterans_other": ("va_medical", "va")}
CATS = ["NF", "ICF", "MHF", "HCBS"]
TAF_AGES = [("age_0_20", 0, 20), ("age_21_44", 21, 44), ("age_45_64", 45, 64), ("age_65plus", 65, 200)]
ROW6_W = ("0.77", "0.82")
BENEFIT_KEYS = {"snap": "snap", "other_state_welfare": "wic", "family_and_general_assistance": "cash_assistance",
                "unemployment": "unemployment", "housing_subsidies": "housing_support"}
CONSTANTS = {"row8": 2.0, "row9": -0.8, "row10": -1.5, "small": -0.1}  # package.cjs CONSTANTS, central
SHELTER_GG = {"shared": 0.59, "personal": 0.84}  # package.cjs: shared takes the 0.59 row, personal the 0.84
CARE_CHANNELS = {"hours_tax": ("household_services_ev", [4230, 4600]),
                 "output": ("household_services_ev", [4230, 4600]),
                 "elder_care": ("home_care_aaf", [3601, 3602, 4230])}


def gate(label, ok, detail=""):
    print(f"  {'✓' if ok else '✗'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def meps_person_keys(d):
    """The spending builder's MEPS payer keys per person, plus Medicaid without home health
    (ltss_share_2026_09_23/meps_hh_key.py), and each person's transport cell."""
    sys.path.insert(0, str(F.FISCAL / "build"))
    import meps_health_transport_2024 as transport
    transport.FIELDS = list(dict.fromkeys(transport.FIELDS + HH))  # this process only
    md, _ = transport.read_meps(MEPS, MEPS.with_name("h256su.txt"))
    cells, codes, _ = transport.donor_model(md, d, False)
    valid = md.PERWT24F.gt(0) & md.AGE24X.ge(0) & md.BORNUSA.isin([1, 2])
    sample = md.loc[valid].copy()
    sample["mcd_ex_hh"] = sample.TOTMCD24 - sample[HH].sum(axis=1)
    index = pd.MultiIndex.from_frame(cells[["age_band", "born"]])
    exposure = ~(d.PUB.eq(0) & d.PRIV.eq(0)).to_numpy()
    pop = sample.groupby(["age_band", "born"]).PERWT24F.sum()
    out = {}
    for name, cols in [("medicare", ["TOTMCR24"]), ("medicaid", ["TOTMCD24"]), ("va_medical", ["TOTVA24"]),
                       ("tricare", ["TOTTRI24"]), ("health_other", ["TOTVA24", "TOTTRI24", "TOTOFD24", "TOTSTL24"]),
                       ("medicaid_ex_hh", ["mcd_ex_hh"])]:
        sums = sample.assign(wx=sample[cols].sum(axis=1) * sample.PERWT24F).groupby(["age_band", "born"]).wx.sum()
        out[name] = (sums / pop).reindex(index).to_numpy()[codes] * exposure
    cell = [f"{TRANSPORT_LABELS[b]}|{NAT[n]}" for b, n in zip(cells.age_band.to_numpy()[codes], cells.born.to_numpy()[codes])]
    return out, np.array(cell), exposure


def split(amount, fractions):
    return {g: amount * f for g, f in zip(F.GENS, fractions)}


def main():
    d = F.load()
    civ, union, gens = F.masks(d)
    omega, _, _ = F.assignments(d, civ, union, gens)
    w = d.pwwgt0.to_numpy(float)
    age = d.A_AGE.to_numpy()
    keyshares = json.loads((F.OUT / "generation_key_shares.json").read_text())
    shares, meta = keyshares["shares"], keyshares["meta"]
    model = json.loads((F.FISCAL / "assumption_explorer_2026_09_21/derived/model.json").read_text())
    lines = {x["id"]: x for x in model["spending"]["lines"]}
    out = {"meta": dict(layout="lane -> item -> union | a | b -> generation -> allocation, $bn of the group's target "
                               "before the package's stack scaling"), "rules": {}}

    def frac(key, a, conv):
        return shares["spending"][a][key][conv]

    def g1_split(v, conv):
        """Late-arrival lane: fractions over GENS of a G1 amount, by a per-person weight vector v (n) through
        the convention's weights, kept inside the G1 cells; the G1 total is the generation lane's."""
        x = np.array([float(v @ omega[conv][:, j]) for j in range(NG)]) * np.array(F.IS_G1, float)
        if x.sum() <= 0:
            raise SystemExit("[BLOCKED] no weight inside G1 for a G1 amount")
        return x / x.sum()

    def check_sum(label, item):
        worst = 0.0
        for conv in ("a", "b"):
            for a in ("personal", "shared"):
                worst = max(worst, abs(sum(item[conv][g][a] for g in F.GENS) - item["union"][a]))
        gate(f"{label}: generations add to the union", worst < 1e-12, f"{worst:.1e} bn")

    def by_fractions(union_by, key_of):
        """union_by {allocation: $bn}; key_of(a, conv) -> 3 fractions."""
        item = {"union": dict(union_by)}
        for conv in ("a", "b"):
            item[conv] = {g: {} for g in F.GENS}
            for a in ("personal", "shared"):
                for g, v in split(union_by[a], key_of(a, conv)).items():
                    item[conv][g][a] = v
        return item

    # ---- pooled medical -------------------------------------------------------------------------
    print("[medical]", flush=True)
    keys, cell, exposure = meps_person_keys(d)
    cps_cells = pd.read_csv(MED / "cps_cells.csv")
    worst = 0.0
    for r in cps_cells.itertuples():
        m = union & (cell == f"{r.band}|{r.nativity}")
        worst = max(worst, abs(float((w * exposure)[m].sum()) - r.union_exposed) / max(r.union_exposed, 1))
        if m.any():
            worst = max(worst, abs(keys["medicaid"][m & exposure][0] - r.meps2024_medicaid) / max(r.meps2024_medicaid, 1))
    gate("MEPS keys and cells reproduce the medical lane's cps_cells.csv", worst < 1e-9, f"{worst:.1e}")
    hh = json.loads((LTSS / "derived/meps_hh_key.json").read_text())["key_share"]
    for name, key in [("medicaid", "medicaid"), ("medicaid_ex_home_health", "medicaid_ex_hh")]:
        s = float((keys[key] * w)[union].sum() / (keys[key] * w)[civ].sum())
        gate(f"MEPS {name} key share reproduces meps_hh_key.json", abs(s - hh[name]) < 1e-12, f"{s:.12f}")
    cm = pd.read_csv(MED / "cells.csv").query("sample == 'pooled_2016_2024' and spec == @SPEC and scheme == 'transport'")
    cm = cm.set_index(["band", "nativity", "group", "measure"])["mean"]
    trans = pd.read_csv(MED / "translation_account.csv").query("spec == @SPEC").set_index("line")
    med = {}
    for line, (key, measure) in MED_LINES.items():
        ratio = np.array([cm[(c.split("|")[0], c.split("|")[1], "mexican_origin", measure)]
                          / cm[(c.split("|")[0], c.split("|")[1], "all_donors", measure)] for c in cell])
        v = keys[key] * w
        tb = float(trans.loc[line, "account_target_bn"])
        total = float(v[union].sum())
        excess = v * (ratio - 1)
        delta = tb * float(excess[union].sum()) / total
        gate(f"{line}: cell ratios reproduce the lane's {SPEC} change {trans.loc[line, 'delta_bn']:+.4f}bn",
             abs(delta - trans.loc[line, "delta_bn"]) < 1e-9, f"{delta:+.9f}")
        item = {"union": {"personal": delta, "shared": delta}}
        for conv in ("a", "b"):
            gv = [tb * float(excess @ omega[conv][:, j]) / total for j in range(NG)]
            item[conv] = {g: {"personal": x, "shared": x} for g, x in zip(F.GENS, gv)}
        med[line] = item
        check_sum(f"medical {line}", item)
        if line == "medicaid_and_chip_other_medical":
            vx = keys["medicaid_ex_hh"] * w * (ratio - 1)
            u = float(vx[union].sum())
            med["ratio_part_weights"] = {conv: [float(vx @ omega[conv][:, j]) / u for j in range(NG)] for conv in ("a", "b")}
    out["rules"]["medical"] = med

    # ---- long-term care -------------------------------------------------------------------------
    print("[long-term care]", flush=True)
    sh = pd.read_csv(LTSS / "derived/shares.csv").query("variant == 'central'").set_index("category")
    summ = json.loads((LTSS / "derived/summary.json").read_text())
    gj = json.loads((LTSS / "derived/gate.json").read_text())
    B, hf, k = gj["medicaid_national_bn"], gj["household_pool_fraction"], gj["household_key_share"]
    k_ex = hh["medicaid_ex_home_health"]
    growth = summ["bea_growth_2024_over_2023"]
    L = {c: float(sh.loc[c, "L2023"]) * growth for c in CATS}
    R = B - sum(L.values())
    rate = hf * k
    eff = pd.read_csv(LTSS / "derived/effects.csv").set_index("variant").loc["central"]
    parts = {c: L[c] * (float(sh.loc[c, "share"]) - rate) for c in CATS}
    parts["remainder_key"] = R * hf * (k_ex - k)
    worst = max(abs(parts[c] - float(eff[c])) for c in parts)
    gate(f"LTSS parts reproduce effects.csv central ({eff['total']:+.4f}bn)", worst < 1e-9, f"{worst:.1e}")
    # Users' generation by category.
    acs = pd.read_parquet(LTSS / "_cache/acs2024_ltss.parquet",
                          columns=["PWGTP", "AGEP", "HISP", "POBP", "RELSHIPP", "HINS4", "DDRS", "DOUT", "DREM"])
    a_union = acs.HISP.eq(2) | acs.POBP.eq(303)
    inst, comm = acs.RELSHIPP.eq(37), ~acs.RELSHIPP.eq(37)
    proxy = {"NF": inst, "ICF": comm & acs.HINS4.eq(1) & acs.DREM.eq(1), "MHF": pd.Series(True, index=acs.index),
             "HCBS": comm & acs.HINS4.eq(1) & (acs.DDRS.eq(1) | acs.DOUT.eq(1))}
    taf = pd.read_csv(LTSS / "derived/taf_age.csv")
    taf = taf[(taf.year == 2023) & (taf.measure == "expenditures") & taf.state.eq("National")] \
        .pivot(index="category", columns="group", values="pct") / 100
    mcaid = d.MCAID.eq(1).to_numpy()
    usborn_union = union & ~F.g1(gens)
    # Late-arrival lane: the Mexico-born users' share goes to the G1 cells in proportion to each CPS
    # Mexico-born person's ACS proxy rate at their arrival class and five-year age band (acs_rates.py).
    # [INFERENCE: the proxy rates are ACS 2019-2023 without the disability items.]
    g1m, g1cls = F.g1(gens), F.g1_class(d)
    proxy_of = {"NF": "inst", "ICF": "comm_medicaid", "MHF": "all", "HCBS": "comm_medicaid"}
    users = {}
    for c in CATS:
        rows = []
        for name, lo, hi in TAF_AGES:
            band = acs.AGEP.between(lo, hi)
            pw = acs.PWGTP.to_numpy(float)
            pm = (proxy[c] & band).to_numpy()
            um = pm & a_union.to_numpy()
            union_share = pw[um].sum() / pw[pm].sum() if pw[pm].sum() else 0.0
            g1 = pw[um & acs.POBP.eq(303).to_numpy()].sum() / pw[um].sum() if pw[um].sum() else 0.0
            cps = usborn_union & mcaid & (age >= lo) & (age <= hi)
            weight = float(taf.loc[c, name]) * union_share
            gm = g1m & (age >= lo) & (age <= hi)
            g1v = np.zeros(len(d))
            g1v[gm] = w[gm] * acs_rates.person_rate(proxy_of[c], g1cls[gm], age[gm])
            rows.append(dict(age=name, weight=weight, g1=g1, cps=cps, g1v=g1v))
        total = sum(r["weight"] for r in rows)
        users[c] = {}
        for conv in ("a", "b"):
            u = np.zeros(NG)
            for r in rows:
                us = np.array([float((w[r["cps"]] * omega[conv][r["cps"], j]).sum()) for j in range(NG)])
                us = us / us.sum()
                u += r["weight"] / total * (r["g1"] * g1_split(r["g1v"], conv) + (1 - r["g1"]) * us)
            users[c][conv] = u.tolist()
        print(f"  users' generation, {c} (a): " + ", ".join(f"{g} {x:.3f}" for g, x in zip(F.GENS, users[c]['a'])),
              flush=True)
    kx = keys["medicaid_ex_hh"] * w
    km = keys["medicaid"] * w
    ltss_items = {}
    for c in CATS:
        added = L[c] * float(sh.loc[c, "share"])
        removed = L[c] * rate
        item = {"union": {"personal": parts[c], "shared": parts[c]}}
        for conv in ("a", "b"):
            mf = frac("medicaid", "personal", conv)
            item[conv] = {g: {"personal": added * users[c][conv][j] - removed * mf[j]} for j, g in enumerate(F.GENS)}
            for g in F.GENS:
                item[conv][g]["shared"] = item[conv][g]["personal"]
        check_sum(f"LTSS {c}", item)
        ltss_items[c] = item
    item = {"union": {"personal": parts["remainder_key"], "shared": parts["remainder_key"]}}
    for conv in ("a", "b"):
        vals = [R * hf * (float(kx @ omega[conv][:, j]) / float(kx[civ].sum())
                          - float(km @ omega[conv][:, j]) / float(km[civ].sum())) for j in range(NG)]
        item[conv] = {g: {"personal": v, "shared": v} for g, v in zip(F.GENS, vals)}
    check_sum("LTSS remainder key", item)
    ltss_items["remainder_key"] = item
    ltss_items["users_generation"] = users
    out["rules"]["ltss"] = ltss_items

    # ---- schools priced where enrolled ----------------------------------------------------------
    print("[schools]", flush=True)
    base = json.loads((SCHOOL / "engine_base.json").read_text())
    he = base["education_national_bn"] * base["household_fraction"]
    comp = pd.read_csv(F.FISCAL / "school_enrollment_2026_09_20/derived/updated_account_components.csv")
    variants = json.loads((SCHOOL / "school_key_variants.json").read_text())
    edu = {}
    for a in ("personal", "shared"):
        x = comp[comp.allocation == a].pivot(index="component", columns="group", values="spending_bn")
        Ts, Ns = x.loc["school", "mexican_observed_total"], x.loc["school", "national_civilian"]
        Tp, Np = x.loc["P", "mexican_observed_total"], x.loc["P", "national_civilian"]
        t0 = lines["education_services"]["keys"]["education_mix"][a]["target_bn"]
        gate(f"education ({a}): he x (T_s + T_p) / (N_s + N_p) is the model's target", abs(he * (Ts + Tp) / (Ns + Np) - t0) < 1e-6,
             f"{he * (Ts + Tp) / (Ns + Np):.6f} vs {t0:.6f}")
        for wv in ROW6_W:
            wf = float(wv)
            school_t = variants[f"row6_w{wv}|preferred"]["school_target_bn"][a]
            college_t = variants[f"row6_w{wv}_whole_line"]["college_target_bn"][a]
            kk = (school_t / he - (1 - wf) * Tp / Np) / (wf * Ts / Ns)
            gate(f"education ({a}, w {wv}): college target reproduces row 6's",
                 abs(he * (wf * Ts / Ns + (1 - wf) * Tp / Np) - college_t) < 1e-9)
            for step, target, kf in [("school", school_t, kk), ("college", college_t, 1.0)]:
                item = edu.setdefault(f"{step}|{wv}", {"union": {}, "a": {g: {} for g in F.GENS},
                                                       "b": {g: {} for g in F.GENS}, "k": {}})
                item["union"][a] = target - t0
                item["k"][a] = kf
                for conv in ("a", "b"):
                    fs, fp = frac("school_operating", a, conv), frac("postsecondary", a, conv)
                    fmix = frac("education_mix", a, conv)
                    for j, g in enumerate(F.GENS):
                        new = he * (wf * kf * Ts * fs[j] / Ns + (1 - wf) * Tp * fp[j] / Np)
                        # The generation models split the model's cell by the mix key (build_models.py).
                        item[conv][g][a] = new - t0 * fmix[j]
                gate(f"education ({a}, w {wv}, {step}): the components rebuild the lane's target",
                     abs(he * (wf * kf * Ts / Ns + (1 - wf) * Tp / Np) - target) < 1e-9)
    for name, item in edu.items():
        check_sum(f"education {name}", item)
        print(f"  education {name}: k {item['k']['personal']:.4f}; personal union {item['union']['personal']:+.3f}; (a) "
              + ", ".join(f"{g} {item['a'][g]['personal']:+.3f}" for g in F.GENS), flush=True)
    out["rules"]["education"] = edu

    # ---- benefits (flagged) ---------------------------------------------------------------------
    print("[benefits]", flush=True)
    bd = json.loads(BENEFITS.read_text())["deltas"]["package_central"]
    ben = {}
    for line, by in bd.items():
        key = BENEFIT_KEYS[line]
        gate(f"benefit line {line} keyed by {key} in the model", lines[line]["preferred_key"] == key)
        item = by_fractions(by, lambda a, conv, key=key: frac(key, a, conv))
        item["key"], item["flag"] = key, "uniform factor on the union's key share (the lane's construction)"
        for conv in ("a", "b"):
            # Late-arrival lane: G1's part over the G1 cells, and the US-born part over G2 and G3plus, by
            # the key's own shares.
            isg1 = np.array(F.IS_G1, float)
            fk = {a: np.array(frac(key, a, conv)) for a in ("personal", "shared")}
            item[f"alt_g1_{conv}"] = {g: {a: by[a] * (fk[a] * isg1)[j] / (fk[a] * isg1).sum() for a in ("personal", "shared")}
                                      for j, g in enumerate(F.GENS)}
            item[f"alt_usborn_{conv}"] = {g: {a: by[a] * (fk[a] * (1 - isg1))[j] / (fk[a] * (1 - isg1)).sum()
                                              for a in ("personal", "shared")} for j, g in enumerate(F.GENS)}
        check_sum(f"benefits {line}", item)
        ben[line] = item
    out["rules"]["benefits"] = ben

    # ---- justice ---------------------------------------------------------------------------------
    parts_use = meta["use_parts"]
    out["rules"]["justice"] = {
        conv: {name: (np.array(parts_use[conv][name]) / sum(parts_use[conv][name])).tolist()
               for name in ("arrest_like_custody", "arrest_per_adult")} for conv in ("a", "b")}

    # ---- lane constants ----------------------------------------------------------------------------
    print("[constants]", flush=True)
    const = {}
    pop = {conv: np.array(meta["population"][conv]) / sum(meta["population"][conv]) for conv in ("a", "b")}
    const["row8"] = by_fractions({"personal": CONSTANTS["row8"], "shared": CONSTANTS["row8"]},
                                 lambda a, conv: frac("population", a, conv))
    mcd_t = lines["medicaid_and_chip_other_medical"]["keys"]["medicaid"]["personal"]["target_bn"]
    mcr_t = lines["medicare"]["keys"]["medicare"]["personal"]["target_bn"]

    def row9_frac(a, conv):
        fm, fr = np.array(frac("medicaid", a, conv)), np.array(frac("medicare", a, conv))
        return ((mcd_t * fm + mcr_t * fr) / (mcd_t + mcr_t)).tolist()
    const["row9"] = by_fractions({"personal": CONSTANTS["row9"], "shared": CONSTANTS["row9"]}, row9_frac)
    const["row9"]["flag"] = "bounded constant; split as the Medicaid and Medicare keys it acts on"
    const["row10"] = by_fractions({"personal": CONSTANTS["row10"], "shared": CONSTANTS["row10"]},
                                  lambda a, conv: frac("wic", a, conv))
    kids = {conv: F.totals((age < 18).astype(float), w, omega[conv]) for conv in ("a", "b")}
    for conv in ("a", "b"):
        const["row10"][f"alt_children_{conv}"] = {g: {a: CONSTANTS["row10"] * kids[conv][j] / kids[conv].sum()
                                                      for a in ("personal", "shared")} for j, g in enumerate(F.GENS)}
    const["row10"]["flag"] = "bounded constant; split as the WIC key it corrects; alternative: the union's children"
    const["small"] = by_fractions({"personal": CONSTANTS["small"], "shared": CONSTANTS["small"]},
                                  lambda a, conv: pop[conv].tolist())
    const["small"]["flag"] = "mixed small items; split by population"
    # Shelter.
    kp = pd.read_csv(SHELTER / "account_keying_parts.csv", nrows=4).set_index("part")
    kp["weight"] = kp.nyc_increase_fy2022_fy2024_k / kp.nyc_increase_fy2022_fy2024_k.sum()  # unrounded
    alloc = pd.read_csv(F.FISCAL / "full_account_spending_2026_09_20/derived/allocations.csv")
    alloc = alloc[(alloc.scenario_id == "complete_preferred_F_per_capita") & (alloc.allocation == "personal")]
    target_share = alloc.set_index("category").target_share_national  # the lane's shares
    ks = pd.read_csv(SHELTER / "account_keying.csv").query(
        "outlays_case == 'central' and mapping == 'A_nyc_codes_consumption' and served_case == 'nyc_jun2025'")
    item = {"union": {}, "a": {g: {} for g in F.GENS}, "b": {g: {} for g in F.GENS}}
    # Late-arrival lane: the use-based charge (recent arrivals) goes to the G1 cells by their Mexico-born
    # persons who entered in 2022-2025 (PEINUSYR 28). [INFERENCE: shelter users are recent arrivals.]
    recent = w * (F.g1(gens) & d.PEINUSYR.eq(28).to_numpy())
    shelter_g1 = {conv: g1_split(recent, conv) for conv in ("a", "b")}
    for a, gg in SHELTER_GG.items():
        r = ks[np.isclose(ks.general_govt_response, gg)].iloc[0]
        total = float(r.cy2024_outlays_musd)
        charged, used = 0.0, 0.0
        per = {conv: np.zeros(NG) for conv in ("a", "b")}
        for part, row in kp.iterrows():
            line = lines[row["A_nyc_codes_consumption_category"]]
            resp = gg if line["response_class"] == "public_goods" else 1.0
            key = line["preferred_key"]
            s = float(target_share[line["id"]])
            charged += total * row.weight * s * resp
            used += total * row.weight * float(r.served_share) * resp
            for conv in ("a", "b"):
                per[conv] += total * row.weight * s * resp * np.array(frac(key, "personal", conv))
        gate(f"shelter ({a}, gg {gg}): charge and use reproduce the lane's {r.account_charge_musd} / {r.use_based_charge_musd} $m",
             abs(charged - float(r.account_charge_musd)) < 0.05 and abs(used - float(r.use_based_charge_musd)) < 0.05,
             f"{charged:.2f} / {used:.2f}")
        over = -(float(r.overcharge_musd)) / 1000  # package.cjs shelterCentral
        item["union"][a] = over
        for conv in ("a", "b"):
            # The rebuilt charge carries the lane's rounding (0.1 $m); scale so the split closes on the
            # package's figure exactly.
            raw = used * shelter_g1[conv] - per[conv]
            raw = raw * (over * 1000) / raw.sum()
            for j, g in enumerate(F.GENS):
                item[conv][g][a] = raw[j] / 1000
    item["rule"] = "use-based charge to G1 (recent arrivals); the account's keyed charge leaves every generation"
    const["shelter"] = item
    # Care and household services.
    summary = pd.read_csv(CARE / "summary.csv")
    central = dict(zip(summary.channel, summary.central_bn))
    channel_bn = {"hours_tax": -central["taxes on native women's extra hours (household-service channel)"],
                  "output": -central["output gain to other factors from those hours, and its taxes (CES)"],
                  "elder_care": -central["elder care: Medicaid nursing-facility saving net of Medicaid home care"]}
    gate("care channels sum to the package's -4.15", abs(sum(channel_bn.values()) + 4.15) < 0.005,
         f"{sum(channel_bn.values()):+.4f}")
    ms = pd.read_csv(CARE / "acs_care_market_shares.csv").set_index(["market", "group"]).hours_share
    occ = d.PEIOOCC.to_numpy()
    worker = (d.WSAL_VAL.to_numpy(float) + d.SEMP_VAL.to_numpy(float)) > 0
    care = {"union": {"personal": 0.0, "shared": 0.0}, "a": {g: {"personal": 0.0, "shared": 0.0} for g in F.GENS},
            "b": {g: {"personal": 0.0, "shared": 0.0} for g in F.GENS}, "workers": {}}
    scale = -4.15 / sum(channel_bn.values())  # the package carries -4.15 (rounded)
    for ch, (market, codes) in CARE_CHANNELS.items():
        g1 = ms[(market, "union_fb")] / ms[(market, "union")]
        m = union & worker & np.isin(occ, codes) & ~F.g1(gens)
        for conv in ("a", "b"):
            us = np.array([float((w[m] * omega[conv][m, j]).sum()) for j in range(NG)])
            # Late-arrival lane: the Mexico-born hours' share over the G1 cells by their CPS workers in the
            # same occupations. [INFERENCE: CPS persons, not ACS hours.]
            g1w = w * (union & worker & np.isin(occ, codes) & F.g1(gens))
            f = g1 * g1_split(g1w, conv) + (1 - g1) * us / us.sum()
            care["workers"].setdefault(ch, {})[conv] = f.tolist()
            for j, g in enumerate(F.GENS):
                for a in ("personal", "shared"):
                    care[conv][g][a] += channel_bn[ch] * scale * f[j]
        for a in ("personal", "shared"):
            care["union"][a] += channel_bn[ch] * scale
    care["rule"] = "workers' generation: ACS Mexico-born share of the union's hours; US-born split by CPS union workers"
    const["care"] = care
    for name, item in const.items():
        check_sum(f"constant {name}", item)
        print(f"  constant {name}: personal union {item['union']['personal']:+.3f}; (a) "
              + ", ".join(f"{g} {item['a'][g]['personal']:+.3f}" for g in F.GENS), flush=True)
    out["rules"]["constants"] = const

    # ---- the brief's literal fill-in rule, for comparison with stack_split.py's exact split ---------
    # Each cell of the fill-in component (D) splits by the generations' shares of the union's imputed key
    # dollars (key value x the lane's material-imputation flag, 5% rule); a key with no imputed dollars in
    # the union splits as the key does.
    print("[fill-in component, literal rule]", flush=True)
    import translate  # noqa: E402  (CPS lane, on sys.path through frame.py)
    stack = json.loads((F.OUT / "stack_by_generation.json").read_text())
    index = C.spm_index(d)
    rk, sk = C.receipt_keys(d, index), C.spending_vectors(d, index)
    imputed, _, _ = C.key_status(d, 0.05)
    receipt_key = {x["id"]: x["cells"]["cbo_collective"] for x in model["receipts"]["lines"]}

    def weights(side, line, key, a, conv):
        lk = translate.lane_key(translate.KEYS, "receipts" if side == "receipts" else "spending",
                                receipt_key[line][a]["key"] if side == "receipts" else key, a)
        vectors = {**rk[a], **sk[a]}
        v = vectors.get(lk) if lk else None
        if v is None:
            v = np.ones(len(d))
        imp = imputed[a].get(lk, np.zeros(len(d), bool)) if lk else np.zeros(len(d), bool)
        for x in (v * imp * w, v * w, w):
            u = float(x[union].sum())
            if u > 0:
                return [float(x @ omega[conv][:, j]) / u for j in range(NG)]
        raise SystemExit("[BLOCKED] no weight for " + str((side, line, key)))

    literal = {}
    for name in ("D_b_hotdeck_union_matched", "D_b_matched_over_pooled"):
        u = stack["components"][name]["union"]["union"]
        literal[name] = {}
        for conv in ("a", "b"):
            gen = {g: {"receipts": {}, "spending": {}} for g in F.GENS}
            for line, by in u["receipts"].items():
                for a, v in by.items():
                    for j, g in enumerate(F.GENS):
                        gen[g]["receipts"].setdefault(line, {})[a] = v * weights("receipts", line, None, a, conv)[j]
            for line, keysd in u["spending"].items():
                for key, by in keysd.items():
                    for a, v in by.items():
                        for j, g in enumerate(F.GENS):
                            gen[g]["spending"].setdefault(line, {}).setdefault(key, {})[a] = \
                                v * weights("spending", line, key, a, conv)[j]
            literal[name][conv] = gen
    out["rules"]["fill_in_literal"] = literal

    (F.OUT / "correction_rules.json").write_text(json.dumps(out, sort_keys=True, indent=1) + "\n")
    if FAILS:
        print(f"✗ {len(FAILS)} gate(s) failed: {FAILS}")
        sys.exit(1)
    print("  ✓ all correction-rule gates passed")


if __name__ == "__main__":
    main()
