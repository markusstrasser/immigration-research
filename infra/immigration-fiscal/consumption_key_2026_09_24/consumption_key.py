"""Test the account's consumption key for remittances and saving (BRIEF.md), and write the proposed
receipt edits.

Run from the repository root (about two minutes):
    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with openpyxl \
        --with pyreadstat --with duckdb --with pyarrow python3 \
        infra/immigration-fiscal/consumption_key_2026_09_24/consumption_key.py
then `node infra/immigration-fiscal/consumption_key_2026_09_24/engine_run.cjs`.

The key: full_account_receipts_2026_09_20/builder.py gives each person positive SPM resources over
unit size; the union's share, 8.104%, keys general sales taxes, selective excises, customs duties
and personal current transfers. Each specification replaces a person's key by
    c(unit) * max(resources - M(unit), 0) / size
with c the consumption per resource dollar at the unit's income rank (saving.py; 1 for the raw key)
and M the unit's modelled remittance outflow (remittance.py; 0 without remittances).

Composition with the adopted corrections (main_case_2026_09_24/derived/corrections.json). The adopted
payload scales the union's share of every consumption line by one stack factor phi = 0.949694 and
re-keys the $99.964bn federal-excise part of the selective-excise line to CBO's group shares. Here:
- a ratio correction (saving, or survey and BEA flows built on CPS counts) scales with phi:
  S_adopted = phi * S;
- the Banxico corridor is fixed in dollars, so its outflow is not scaled by phi:
  S_adopted = (phi * G_before_remittances - (G_before - G_after)) / N;
- the federal-excise part keeps CBO's group shares and takes the specification's union share inside
  each CBO group: phi * sum_j cbo_j * theta_j(spec) * 99.964, times the corridor adjustment above.
Each line's edit is its specification target less the adopted target. The four lines are keyed on
consumption in all eight receipt scenarios with equal targets, so package.cjs expand() carries the
same dollar edit to every scenario and both allocations. remaining_production_property is keyed on
consumption only in property_residual_consumption (an indirect cell); there it takes the proportional
change of the key, and nowhere else, because its other seven cells are keyed on capital.
Spending lines keyed on resources take the same proportional change (symmetry, task 5).
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
os.environ.setdefault("PYTHONUNBUFFERED", "1")

import ce_pumd  # noqa: E402
import ce_tables  # noqa: E402
import cps_frame  # noqa: E402
import fetch  # noqa: E402
import outside  # noqa: E402
import remittance  # noqa: E402
import saving  # noqa: E402

FISCAL = HERE.parent
DERIVED = HERE / "derived"
MODEL = FISCAL / "assumption_explorer_2026_09_21" / "derived" / "model.json"
ADOPTED = FISCAL / "main_case_2026_09_24" / "derived" / "corrections.json"
CBO_TRANSLATION = FISCAL / "external_benchmarks_2026_09_24" / "derived" / "cbo_translation.csv"
LINES = ["general_sales_tax", "excise_selective_sales", "customs_duties", "personal_current_transfers"]
FEDERAL_EXCISE_BN = 99.964   # BEA Table 3.5 line 4, 2024, inside the 371.262 selective-excise line
RPP, RPP_SCENARIO = "remaining_production_property", "property_residual_consumption"
SPENDING_RESOURCE_LINES = ["economic_affairs_services", "housing_community_services", "recreation_culture",
                           "agricultural_subsidies", "housing_subsidies", "transport_subsidies", "other_subsidies"]
ALLOCS = ["personal", "shared"]
CE_REPS = 200


def _ok(msg):
    print(f"  ✓ {msg}")


def _fail(msg):
    print(f"  ✗ {msg}")
    raise SystemExit(f"[FAIL] {msg}")


def sdr(x):
    return cps_frame.sdr(np.asarray(x, float))


# ------------------------------------------------------------------------------------------------
# Adopted state of the consumption lines
# ------------------------------------------------------------------------------------------------
def adopted_state() -> dict:
    model = json.loads(MODEL.read_text())
    payload = json.loads(ADOPTED.read_text())
    lines = {l["id"]: l for l in model["receipts"]["lines"]}
    scenarios = model["receipts"]["scenarios"]
    edits = {}
    for e in payload["edits"]:
        if e["side"] == "receipt":
            cell = edits.setdefault((e["line"], e["scenario"]), {a: 0.0 for a in ALLOCS})
            for a in ALLOCS:
                cell[a] += e["by"][a]
    out = {"scenarios": scenarios, "reference": model["receipts"]["reference"], "lines": {}}
    for lid in LINES:
        raw = {(sc, a): lines[lid]["cells"][sc][a]["target_bn"] for sc in scenarios for a in ALLOCS}
        adopted = {(sc, a): raw[(sc, a)] + edits.get((lid, sc), {a: 0.0})[a] for sc, a in raw}
        keys = {lines[lid]["cells"][sc][a]["key"] for sc in scenarios for a in ALLOCS}
        if keys != {"consumption"} or len({round(v, 9) for v in raw.values()}) != 1 \
                or len({round(v, 9) for v in adopted.values()}) != 1:
            _fail(f"{lid}: cells are not one consumption-keyed target across scenarios and allocations")
        out["lines"][lid] = dict(national=lines[lid]["national_bn"], raw=next(iter(raw.values())),
                                 adopted=next(iter(adopted.values())))
    phis = [v["adopted"] / v["raw"] for k, v in out["lines"].items() if k != "excise_selective_sales"]
    if max(phis) - min(phis) > 1e-9:
        _fail(f"stack factors differ across lines: {phis}")
    out["phi"] = phis[0]
    rpp = lines[RPP]["cells"][RPP_SCENARIO]
    if rpp["personal"]["key"] != "consumption" or rpp["personal"]["direct"]:
        _fail("remaining_production_property is not an indirect consumption cell in its scenario")
    out["rpp"] = {a: rpp[a]["target_bn"] + edits.get((RPP, RPP_SCENARIO), {a: 0.0})[a] for a in ALLOCS}
    # Spending cells keyed on resources, adopted targets.
    sp_edits = {}
    for e in payload["edits"]:
        if e["side"] == "spending":
            cell = sp_edits.setdefault((e["line"], e["key"]), {a: 0.0 for a in ALLOCS})
            for a in ALLOCS:
                cell[a] += e["by"][a]
    out["spending"] = {}
    for l in model["spending"]["lines"]:
        if l["id"] in SPENDING_RESOURCE_LINES:
            k = l["keys"]["resources"]
            out["spending"][l["id"]] = dict(
                preferred=l["preferred_key"] == "resources", response_class=l["response_class"],
                raw_share=k["personal"]["share"],
                adopted={a: k[a]["target_bn"] + sp_edits.get((l["id"], "resources"), {a: 0.0})[a] for a in ALLOCS})
    return out


# ------------------------------------------------------------------------------------------------
# Key totals for a specification
# ------------------------------------------------------------------------------------------------
class Frame:
    def __init__(self, a: dict):
        self.a = a
        self.u = a["unit"]
        self.size = a["size"]
        self.civ, self.tgt, self.W = a["civilian"], a["target"], a["weights"]
        n = int(a["n_units"])
        head = a["head"]
        self.res = np.zeros(n)
        self.res[self.u[head]] = np.clip(a["spm_resources"][head], 0, None)

    def totals_fixed(self, c_unit: np.ndarray):
        """Group and national totals (161 replicates) of c * resources per person."""
        k = (c_unit * self.res)[self.u] / self.size
        return k[self.tgt] @ self.W[self.tgt], k[self.civ] @ self.W[self.civ], k

    def totals_remit(self, c_unit: np.ndarray, spec: dict, un: dict, mode: str = "proportional"):
        """Totals with remittance outflows; theta differs by replicate, so loop over columns."""
        G, N = np.empty(161), np.empty(161)
        k0 = None
        for r in range(161):
            m = remittance.outflow_matrix(spec, un, r)
            if mode == "proportional":
                ku = c_unit * np.maximum(self.res - m, 0)
            elif mode == "dollar":
                ku = np.maximum(c_unit * self.res - m, 0)
            else:
                raise ValueError(mode)
            k = ku[self.u] / self.size
            G[r] = k[self.tgt] @ self.W[self.tgt, r]
            N[r] = k[self.civ] @ self.W[self.civ, r]
            if r == 0:
                k0 = k
        return G, N, k0


def ce_bootstrap_share(fr: Frame, pumd: pd.DataFrame, concept: str, reps: int = CE_REPS, seed: int = 11) -> np.ndarray:
    """CE sampling error of the saving-corrected union share: resample CE consumer units, rebuild the
    ratio curve from the microdata alone (50 rank bins, bottom decile pooled) and re-key."""
    a = fr.a
    cu = pumd.newid.astype(str).str.zfill(8).str[:7].to_numpy()
    cus, inv = np.unique(cu, return_inverse=True)
    b = saving.rank_bins(pumd["rank"], 50)
    dec = np.arange(50) * 10 // 50
    w = pumd.weight.to_numpy()
    c = pumd[concept].to_numpy()
    y = pumd.income.to_numpy()
    units = saving.cps_units(a)
    ub = saving.rank_bins(units["rank"], 50)
    Y = np.bincount(ub, weights=units["weight"] * units["income"], minlength=50)
    R = np.bincount(ub, weights=units["weight"] * units["resources"], minlength=50)
    Y[dec == 0], R[dec == 0] = Y[dec == 0].sum(), R[dec == 0].sum()
    conv = Y / R
    rng = np.random.default_rng(seed)
    out = []
    w0 = fr.W[:, 0]
    for _ in range(reps):
        kk = np.bincount(rng.integers(0, len(cus), len(cus)), minlength=len(cus))[inv]
        C = np.bincount(b, weights=w * kk * c, minlength=50)
        Yc = np.bincount(b, weights=w * kk * y, minlength=50)
        ratio = C / Yc
        ratio[dec == 0] = C[dec == 0].sum() / Yc[dec == 0].sum()
        f = (ratio * conv)[ub]
        k = (f * fr.res)[fr.u] / fr.size
        out.append((k[fr.tgt] @ w0[fr.tgt]) / (k[fr.civ] @ w0[fr.civ]))
    return np.array(out)


# ------------------------------------------------------------------------------------------------
# Checks against CE tables by Hispanic origin
# ------------------------------------------------------------------------------------------------
def published_hispanic_check() -> pd.DataFrame:
    """Table 1110 decile composition (Hispanic % of consumer units by decile) predicts Hispanic
    income and spending; Table 2200 gives the actual Hispanic column."""
    dec = ce_tables.parse(saving.DECILE_TABLE)
    lat = ce_tables.parse("reference-person-latino-2024.xlsx")
    cdec, clat = ce_tables.concepts(dec), ce_tables.concepts(lat)
    col = lat["_columns"].index(next(c for c in lat["_columns"] if c.startswith("Hispanic")))
    share = np.array(dec["Hispanic or Latino"][1:]) / 100 * np.array(dec["Number of consumer units (in thousands)"][1:])
    rows = []
    pred_y = share @ np.array(dec["Income before taxes"][1:]) / share.sum()
    act_y = lat["Income before taxes"][col]
    rows.append(dict(item="income_before_taxes", predicted=pred_y, actual=act_y, actual_over_predicted=act_y / pred_y))
    for k in saving.CONCEPTS:
        pred = share @ np.array(cdec[k][1:]) / share.sum()
        act = clat[k][col]
        rows.append(dict(item=k, predicted=pred, actual=act, actual_over_predicted=act / pred))
        rows.append(dict(item=f"{k}_over_income", predicted=pred / pred_y, actual=act / act_y,
                         actual_over_predicted=(act / act_y) / (pred / pred_y)))
    rows.append(dict(item="cash_contributions", predicted=share @ np.array(dec["Cash contributions"][1:]) / share.sum(),
                     actual=lat["Cash contributions"][col],
                     actual_over_predicted=lat["Cash contributions"][col] / (share @ np.array(dec["Cash contributions"][1:]) / share.sum())))
    all_c = cdec["consumption"][0] / dec["Income before taxes"][0]
    rows.append(dict(item="hispanic_vs_all_consumption_over_income", predicted=np.nan,
                     actual=(clat["consumption"][col] / act_y) / all_c, actual_over_predicted=np.nan))
    return pd.DataFrame(rows)


def cps_ce_ratio(fr: Frame, curve: dict) -> dict:
    """CE-concept consumption over pre-tax income that the curve predicts for the union and for all
    CPS units, to set beside CE's Hispanic and Mexican-origin ratios."""
    a = fr.a
    units = saving.cps_units(a)
    b = saving.rank_bins(units["rank"], curve["nb"])
    c_u = curve["ratio"][b] * units["income"]
    w = fr.W[:, 0]
    cp = c_u[fr.u] / fr.size
    yp = units["income"][fr.u] / fr.size
    out = {}
    for name, m in (("union", fr.tgt), ("all_civilians", fr.civ)):
        out[name] = (cp[m] @ w[m]) / (yp[m] @ w[m])
    out["union_over_all"] = out["union"] / out["all_civilians"]
    return out


# ------------------------------------------------------------------------------------------------
# Specifications
# ------------------------------------------------------------------------------------------------
def main() -> None:
    DERIVED.mkdir(exist_ok=True)
    print("[gate 1] current key from the CPS archive")
    a = cps_frame.frame()
    g1 = cps_frame.reproduce(a)
    if not g1["ok"]:
        _fail(f"key {g1['reproduced']} != stored {g1['stored']}")
    _ok(f"union share {g1['reproduced']:.12f} (stored {g1['stored']:.12f}); SE {g1['se']:.5f}")
    fr = Frame(a)
    state = adopted_state()
    phi = state["phi"]
    _ok(f"adopted stack factor phi = {phi:.9f}; lines one target across 8 scenarios x 2 allocations")

    # CBO translation of the raw key must reproduce the adopted federal-excise re-key.
    g_cbo, cbo = outside.cbo_groups_for(a)
    base_fed = outside.cbo_federal_share(fr.totals_fixed(np.ones(int(a["n_units"])))[2], a, g_cbo, cbo)
    trans = pd.read_csv(CBO_TRANSLATION)
    stored = trans.query("spec == 'excise_taxes|2022' and allocation == 'personal'").reweighted_share.iloc[0]
    if abs(float(base_fed["share_at_cbo"][0]) - stored) > 1e-12:
        _fail(f"CBO federal-excise share {base_fed['share_at_cbo'][0]} != outside-checks lane {stored}")
    exc = state["lines"]["excise_selective_sales"]
    s0 = g1["reproduced"]
    rebuilt = phi * (s0 * (exc["national"] - FEDERAL_EXCISE_BN) + stored * FEDERAL_EXCISE_BN)
    if abs(rebuilt - exc["adopted"]) > 1e-6:
        _fail(f"adopted excise target {exc['adopted']} not rebuilt ({rebuilt})")
    _ok(f"adopted excise target {exc['adopted']:.6f} = phi x (8.104% non-federal + CBO {stored:.6%} federal)")

    # ---------------- saving curves ----------------
    print("[saving] CE 2024 ratio curves")
    pub = saving.published_deciles()
    pumd = saving.pumd_ranked()
    curves = {}
    for concept in saving.CONCEPTS:
        curves[(concept, True)] = saving.ce_curve(concept, 50, pumd, pub, within=True)
        curves[(concept, False)] = saving.ce_curve(concept, 50, pumd, pub, within=False)
    pd.DataFrame([dict(concept=c, within_decile_shape=w, bin=i, decile=i * 10 // 50, ratio_to_pretax_income=r,
                       level_per_cu=l) for (c, w), cv in curves.items()
                  for i, (r, l) in enumerate(zip(cv["ratio"], cv["level"]))]).to_csv(
        DERIVED / "saving_curves.csv", index=False, lineterminator="\n")
    # PUMD reproduces Table 1110 deciles (positive control).
    dec_p = saving.rank_bins(pumd["rank"], 10)
    ctrl = []
    for k in range(10):
        m = dec_p == k
        wk = pumd.weight[m]
        ctrl.append(dict(decile=k + 1, pumd_income=np.average(pumd.income[m], weights=wk), table_income=pub["income"][k],
                         pumd_consumption=np.average(pumd.consumption[m], weights=wk), table_consumption=pub["consumption"][k]))
    ctrl = pd.DataFrame(ctrl)
    ctrl["income_gap_pct"] = 100 * (ctrl.pumd_income / ctrl.table_income - 1)
    ctrl["consumption_gap_pct"] = 100 * (ctrl.pumd_consumption / ctrl.table_consumption - 1)
    ctrl.to_csv(DERIVED / "pumd_decile_control.csv", index=False, lineterminator="\n")
    _ok(f"PUMD deciles vs Table 1110: income within {ctrl.income_gap_pct.abs().max():.1f}%, "
        f"consumption within {ctrl.consumption_gap_pct.abs().max():.1f}%")

    ones = np.ones(int(a["n_units"]))
    factors = {
        "raw": ones,
        "saving_central": saving.unit_factor(a, curves[("consumption", True)], "ratio"),
        "saving_step_deciles": saving.unit_factor(a, curves[("consumption", False)], "ratio"),
        "saving_level_transport": saving.unit_factor(a, curves[("consumption", True)], "level"),
        "saving_total_expenditure": saving.unit_factor(a, curves[("total", True)], "ratio"),
        "saving_taxable_broad": saving.unit_factor(a, curves[("taxable_broad", True)], "ratio"),
        "saving_bottom_capped": saving.unit_factor(a, curves[("consumption", True)], "ratio", cap_bottom=1.0),
        "saving_rank_x_size": saving.unit_factor_by_size(a, "consumption", pumd, pub, nb=20),
        "saving_rank_x_size_x_age": saving.unit_factor_by_size_age(a, "consumption", pumd, pub, nb=20),
    }
    # CE under-measures spending at the top of the income distribution [INFERENCE: its aggregate
    # falls short of PCE and the shortfall is not known to be income-neutral]; a steeper true top
    # would flatten the gradient. Sensitivity: the top decile's ratio raised by a quarter and a half.
    for s in (1.25, 1.5):
        cv = dict(curves[("consumption", True)])
        cv["ratio"] = cv["ratio"] * np.where(np.arange(50) * 10 // 50 == 9, s, 1.0)
        factors[f"saving_top_decile_x{s:g}"] = saving.unit_factor(a, cv, "ratio")
    # Outside check in main-case dollars: ITEP's sales-and-excise rate for the unit's money-income
    # group times the account's own base (only relative rates matter to a share).
    factors["outside_itep_gradient"] = outside.itep_unit_rates(a, "sales_excise")

    # ---------------- CE checks ----------------
    print("[ce check] Hispanic and Mexican-origin consumer units")
    pubcheck = published_hispanic_check()
    pubcheck.to_csv(DERIVED / "ce_published_hispanic_check.csv", index=False, lineterminator="\n")
    checks = []
    for concept in saving.CONCEPTS:
        for cells in (("vig",), ("vig", "size"), ("vig", "size", "age")):
            checks.append(saving.ce_check(pumd, concept, cells, reps=CE_REPS))
    checks = pd.concat(checks, ignore_index=True)
    checks.to_csv(DERIVED / "ce_microdata_check.csv", index=False, lineterminator="\n")
    mex = checks.query("group == 'mexican_origin' and concept == 'consumption'").set_index("cells")
    _ok("Mexican-origin CUs, consumption actual/predicted: " + ", ".join(
        f"{c} {r.actual_over_predicted:.3f} (SE {r.bootstrap_se:.3f})" for c, r in mex.iterrows()))
    gifts = pd.DataFrame([dict(group=g, gift_to_persons_outside_cu=np.average(pumd.gift_other_persons[m], weights=pumd.weight[m]),
                               share_giving=np.average(pumd.gift_other_persons[m] > 0, weights=pumd.weight[m]),
                               records=int(m.sum()))
                          for g, m in [("all", pumd.weight > 0), ("hispanic", pumd.hispanic), ("mexican_origin", pumd.mexican_origin)]])
    gifts.to_csv(DERIVED / "ce_gifts_to_persons.csv", index=False, lineterminator="\n")
    ce_ratio = {}
    for g, m in [("all", pumd.weight > 0), ("hispanic", pumd.hispanic), ("mexican_origin", pumd.mexican_origin)]:
        ce_ratio[g] = (pumd.consumption[m] @ pumd.weight[m]) / (pumd.income[m] @ pumd.weight[m])
    cps_ratio = cps_ce_ratio(fr, curves[("consumption", True)])

    # ---------------- remittance flows ----------------
    print("[remittances] outflows calibrated to national flows")
    flows_read = remittance.primary_flows()
    if (flows_read["quarters"] != 4 or abs(flows_read["banxico_us_2024"] - remittance.BANXICO_US) > 1e-6
            or abs(flows_read["banxico_total_2024"] - remittance.BANXICO_TOTAL) > 1e-6
            or abs(flows_read["bea_2024"] - remittance.BEA_PERSONAL_TRANSFERS) > 1e-9):
        _fail(f"flow constants differ from the primary files: {flows_read}")
    _ok(f"Banxico CE167 2024: US ${flows_read['banxico_us_2024']:.3f}bn of ${flows_read['banxico_total_2024']:.3f}bn; "
        f"BEA personal transfers ${flows_read['bea_2024']:.3f}bn")
    rates = remittance.sender_rates()
    un = remittance.units(a)
    cpi = fetch.cpi_annual()
    rspecs, amounts = remittance.spec_flows(a, un, rates, cpi)
    flow_rows = []
    for name, sp in rspecs.items():
        split = remittance.outflow_split(a, un, remittance.outflow_matrix(sp, un, 0), 1.0, rates)
        flow_rows.append(dict(spec=name, note=sp["note"], rho=sp["rho"], others=sp["others"],
                              theta_share_of_earnings=float(sp["theta"][0]), absolute=sp["absolute"], **split))
    flows = pd.DataFrame(flow_rows)
    flows.to_csv(DERIVED / "remittance_flows.csv", index=False, lineterminator="\n")
    cen = flows.set_index("spec").loc["corridor_net_h2"]
    _ok(f"central corridor: theta {cen.theta_share_of_earnings:.4f} of sending units' earnings, "
        f"${cen.sent_per_expected_sending_union_unit:,.0f} per expected sending unit; union bears "
        f"${cen.bearer_union_bn:.1f}bn in the key")

    # ---------------- specifications ----------------
    print("[specs] key shares, adopted-basis shares and edits")
    specs = {}

    def record(name, family, G, N, k0, G_noR=None, absolute=False, note=""):
        S = G / N
        if absolute:
            SA = (phi * G_noR - (G_noR - G)) / N
        else:
            SA = phi * S
        fed = outside.cbo_federal_share(k0, a, g_cbo, cbo)
        specs[name] = dict(family=family, note=note, S=S, SA=SA, fed_share_cbo=fed["share_at_cbo"],
                           fed_share_key=fed["share_key"], absolute=absolute, pi=fed["pi"], theta=fed["theta"],
                           cbo=fed["cbo"], G=G, N=N)

    for name, c in factors.items():
        G, N, k0 = fr.totals_fixed(c)
        family = "raw" if name == "raw" else ("outside" if name.startswith("outside_") else "saving")
        record(name, family, G, N, k0,
               note={"raw": "positive SPM resources per person (the account's key)",
                     "outside_itep_gradient": "ITEP Who Pays? sales-and-excise rate by money-income group x resources"
                     }.get(name, name))
    # CE Mexican-origin calibration: the union's consumption times CE's actual/predicted ratio.
    for name, base, cells in [("saving_ce_mexican_rank", "saving_central", "vig"),
                              ("saving_ce_mexican_rank_x_size", "saving_rank_x_size", "vigxsize")]:
        f_mex = float(mex.loc[cells, "actual_over_predicted"])
        G, N, k0 = fr.totals_fixed(factors[base])
        k1 = np.where(fr.tgt, k0 * f_mex, k0)
        G1 = G * f_mex
        N1 = N + G * (f_mex - 1)
        record(name, "saving", G1, N1, k1, note=f"{base} with the union's consumption x {f_mex:.3f} (CE Mexican-origin, {cells})")
    for rname, sp in rspecs.items():
        G, N, k0 = fr.totals_remit(ones, sp, un)
        record("remit_" + rname, "remittances", G, N, k0, G_noR=specs["raw"]["G"], absolute=sp["absolute"],
               note=sp["note"])
    both = [("corridor_net_h2", "proportional"), ("corridor_net_h2", "dollar"), ("survey_cemla", "proportional"),
            ("bea", "proportional"), ("corridor_full", "proportional"), ("corridor_net_h2_illicit", "proportional"),
            ("corridor_net_h2_others_bea", "proportional"), ("corridor_net_h2_others_zero", "proportional")]
    for rname, mode in both:
        sp = rspecs[rname]
        G, N, k0 = fr.totals_remit(factors["saving_central"], sp, un, mode)
        tag = "" if mode == "proportional" else "_dollar_for_dollar"
        record("both_" + rname + tag, "both", G, N, k0, G_noR=specs["saving_central"]["G"], absolute=sp["absolute"],
               note=f"saving_central with {rname}, remittances {'out of consumption dollar for dollar' if mode == 'dollar' else 'out of resources before the consumption ratio'}")
    for sname in ("saving_rank_x_size", "saving_rank_x_size_x_age"):
        for rname in ("corridor_net_h2", "survey_cemla"):
            sp = rspecs[rname]
            G, N, k0 = fr.totals_remit(factors[sname], sp, un)
            record(f"both_{sname.removeprefix('saving_')}_{rname}", "both", G, N, k0, G_noR=specs[sname]["G"],
                   absolute=sp["absolute"], note=f"{sname} with {rname}")

    # CE sampling error for the saving specifications' central curve.
    ce_draws = ce_bootstrap_share(fr, pumd, "consumption")
    base_S = float(specs["raw"]["S"][0])

    # ---------------- edits ----------------
    rows, payloads, receipts_by_spec = [], {}, {}
    SA_base = phi * specs["raw"]["S"]
    for name, sp in specs.items():
        SA, S = sp["SA"], sp["S"]
        adj = SA / (phi * S)
        by_line = {}
        for lid, ln in state["lines"].items():
            if lid == "excise_selective_sales":
                nonfed = SA * (ln["national"] - FEDERAL_EXCISE_BN)
                fedp = phi * sp["fed_share_cbo"] * adj * FEDERAL_EXCISE_BN
                target = nonfed + fedp
            else:
                target = SA * ln["national"]
            by_line[lid] = target - ln["adopted"]
        ratio = SA / SA_base
        edits = []
        for lid in LINES:
            v = float(by_line[lid][0])
            for sc in state["scenarios"]:
                edits.append(dict(side="receipt", line=lid, scenario=sc, by={"personal": v, "shared": v}))
        edits.append(dict(side="receipt", line=RPP, scenario=RPP_SCENARIO,
                          by={al: float((ratio[0] - 1) * state["rpp"][al]) for al in ALLOCS}))
        for lid, cell in state["spending"].items():
            edits.append(dict(side="spending", line=lid, key="resources",
                              by={al: float((ratio[0] - 1) * cell["adopted"][al]) for al in ALLOCS}))
        payloads[name] = dict(family=sp["family"], note=sp["note"], edits=edits)
        receipts = sum(by_line.values())
        receipts_by_spec[name] = receipts
        # The correction's own sampling error: the change against the raw key, replicate by replicate.
        change_se = sdr(receipts - receipts_by_spec["raw"])
        econ = state["spending"]["economic_affairs_services"]["adopted"]["personal"]
        rows.append(dict(
            spec=name, family=sp["family"], key_share=float(S[0]), key_share_se_cps=sdr(S),
            key_share_change_pp=100 * (float(S[0]) - base_S), adopted_basis_share=float(SA[0]),
            federal_excise_union_share_cbo=float(sp["fed_share_cbo"][0]),
            general_sales_tax_bn=float(by_line["general_sales_tax"][0]),
            excise_selective_sales_bn=float(by_line["excise_selective_sales"][0]),
            customs_duties_bn=float(by_line["customs_duties"][0]),
            personal_current_transfers_bn=float(by_line["personal_current_transfers"][0]),
            receipts_change_bn=float(receipts[0]), receipts_change_se_bn=change_se,
            receipts_level_se_bn=sdr(receipts),
            linear_cost_change_bn=-float(receipts[0]),
            rpp_property_residual_consumption_personal_bn=float((ratio[0] - 1) * state["rpp"]["personal"]),
            economic_affairs_resources_edit_bn=float((ratio[0] - 1) * econ),
            note=sp["note"]))
    table = pd.DataFrame(rows)
    ce_se = float(np.std(ce_draws, ddof=1))
    ce_mean = float(np.mean(ce_draws))
    # CE sampling error, bootstrapped for the central curve only; it carries to specifications built on it.
    on_central = (table.spec.isin(["saving_central", "saving_ce_mexican_rank"])
                  | (table.spec.str.startswith("both_") & ~table.spec.str.contains("rank_x_size")))
    table["key_share_se_ce"] = np.where(on_central, ce_se, np.nan)
    table.to_csv(DERIVED / "key_specs.csv", index=False, lineterminator="\n")
    meta = dict(source="consumption_key_2026_09_24/consumption_key.py", status="proposed, not adopted",
                composes_with="main_case_2026_09_24/derived/corrections.json", phi=phi,
                federal_excise_bn=FEDERAL_EXCISE_BN)
    (DERIVED / "payloads.json").write_text(json.dumps(dict(meta=meta, specs=payloads), indent=1) + "\n")

    # ---------------- outside checks ----------------
    print("[outside] CBO federal excise and ITEP Who Pays?")
    f_groups = list(specs["raw"]["pi"])
    cbo_rows = []
    for name in ["raw", "saving_central", "saving_step_deciles", "saving_level_transport", "saving_total_expenditure",
                 "saving_taxable_broad", "saving_rank_x_size", "saving_rank_x_size_x_age", "saving_top_decile_x1.25",
                 "remit_corridor_net_h2", "remit_survey_cemla", "both_corridor_net_h2"]:
        sp = specs[name]
        for j in f_groups:
            cbo_rows.append(dict(spec=name, group=j, key_share_pi=float(sp["pi"][j][0]),
                                 cbo_excise_share=sp["cbo"][j], union_share_theta=float(sp["theta"][j][0])))
    cbo_df = pd.DataFrame(cbo_rows)
    cbo_df.to_csv(DERIVED / "cbo_check.csv", index=False, lineterminator="\n")
    cbo_sum = pd.DataFrame([dict(spec=n, union_bn_key=float(specs[n]["fed_share_key"][0]) * FEDERAL_EXCISE_BN,
                                 union_bn_at_cbo=float(specs[n]["fed_share_cbo"][0]) * FEDERAL_EXCISE_BN,
                                 gap_bn=float(specs[n]["fed_share_key"][0] - specs[n]["fed_share_cbo"][0]) * FEDERAL_EXCISE_BN,
                                 gap_se_bn=sdr((specs[n]["fed_share_key"] - specs[n]["fed_share_cbo"]) * FEDERAL_EXCISE_BN),
                                 q1_key=float(specs[n]["pi"]["q1"][0]), q1_cbo=specs[n]["cbo"]["q1"],
                                 top1_key=float(specs[n]["pi"]["top1"][0]), top1_cbo=specs[n]["cbo"]["top1"])
                            for n in dict.fromkeys(cbo_df.spec)])
    cbo_sum.to_csv(DERIVED / "cbo_check_summary.csv", index=False, lineterminator="\n")
    keys_for_itep = {n: (fr.totals_fixed(factors[n])[2] if n in factors else None) for n in
                     ["raw", "saving_central", "saving_step_deciles", "saving_total_expenditure", "saving_taxable_broad",
                      "saving_rank_x_size", "saving_rank_x_size_x_age", "saving_top_decile_x1.25"]}
    itep = outside.itep_compare(keys_for_itep, a)
    itep.to_csv(DERIVED / "itep_check.csv", index=False, lineterminator="\n")
    itep_share = {}
    for base in ("resources", "money_income"):
        for c in ["sales_excise", "general_sales_individuals", "other_sales_excise_individuals"]:
            itep_share[(base, "all_civilians", c)] = outside.itep_keyed_share(a, c, True, base)
        itep_share[(base, "non_elderly", "sales_excise")] = outside.itep_keyed_share(a, "sales_excise", False, base)
    # Flat keys on each base, for the gradient's own effect.
    head = a["head"]
    money = np.clip(a["spm_totval"][head][np.argsort(a["unit"][head])][a["unit"]], 0, None) / a["size"]
    ne = fr.civ & outside.itep_groups(a)[1]
    flat = {("money_income", "all_civilians"): cps_frame.key_shares(money, a),
            ("money_income", "non_elderly"): (money[ne & fr.tgt] @ fr.W[ne & fr.tgt]) / (money[ne] @ fr.W[ne])}
    pd.DataFrame([dict(base=b, universe=u, concept=c, itep_keyed_union_share=float(v[0]), se=sdr(v),
                       flat_same_base=float(flat[(b, u)][0]) if (b, u) in flat else
                       (float(specs["raw"]["S"][0]) if u == "all_civilians" else np.nan))
                  for (b, u, c), v in itep_share.items()]).to_csv(DERIVED / "itep_keyed_shares.csv", index=False,
                                                                   lineterminator="\n")
    key_ne = {n: float((k[ne & fr.tgt] @ fr.W[ne & fr.tgt, 0]) / (k[ne] @ fr.W[ne, 0])) for n, k in keys_for_itep.items()}

    # ---------------- summary ----------------
    summary = dict(
        gate_key=g1, phi=phi, ce_bootstrap=dict(reps=CE_REPS, se=ce_se, mean=ce_mean),
        amounts_2024_dollars=amounts, cpi=dict((str(k), v) for k, v in cpi.items() if k in (2003, 2015, 2024)),
        published_hispanic_check=pubcheck.to_dict(orient="records"),
        ce_consumption_over_income=ce_ratio, cps_predicted_consumption_over_income=cps_ratio,
        itep_keyed_union_share={f"{b}|{u}|{c}": dict(share=float(v[0]), se=sdr(v)) for (b, u, c), v in itep_share.items()},
        key_union_share_non_elderly=key_ne,
        specs={r["spec"]: {k: r[k] for k in ("key_share", "key_share_se_cps", "adopted_basis_share",
                                             "receipts_change_bn", "receipts_change_se_bn")} for r in rows},
    )
    (DERIVED / "summary.json").write_text(json.dumps(summary, indent=1, default=float) + "\n")
    pd.set_option("display.width", 220)
    show = table[["spec", "key_share", "key_share_se_cps", "adopted_basis_share", "federal_excise_union_share_cbo",
                  "receipts_change_bn", "receipts_change_se_bn"]].copy()
    for c in ["key_share", "key_share_se_cps", "adopted_basis_share", "federal_excise_union_share_cbo"]:
        show[c] = (100 * show[c]).round(3)
    show[["receipts_change_bn", "receipts_change_se_bn"]] = show[["receipts_change_bn", "receipts_change_se_bn"]].round(3)
    print(show.to_string(index=False))
    print(f"\nCE sampling SE of the saving-corrected share: {100 * ce_se:.3f} points (bootstrap mean {100 * ce_mean:.3f}%)")
    print("\nCBO federal excise ($99.964bn):")
    print(cbo_sum.round(4).to_string(index=False))
    print("\nITEP-keyed union shares:", {k: round(100 * v["share"], 3) for k, v in summary["itep_keyed_union_share"].items()})
    print("Key union shares among non-elderly:", {k: round(100 * v, 3) for k, v in key_ne.items()})
    print("\nCE consumption/income:", {k: round(v, 4) for k, v in ce_ratio.items()},
          "| CPS predicted:", {k: round(v, 4) for k, v in cps_ratio.items()})
    print("\nPublished Table 2200 check:")
    print(pubcheck.round(4).to_string(index=False))
    print("\nRemittance flows ($bn):")
    cols = ["spec", "theta_share_of_earnings", "all_civilians_bn", "bearer_union_bn", "bearer_union_first_generation_bn",
            "bearer_union_us_born_bn", "sent_per_expected_sending_union_unit"]
    print(flows[cols].round(3).to_string(index=False))
    sent = [c for c in flows.columns if c.startswith("sent_by_union_")]
    print(flows[["spec"] + sent].round(3).to_string(index=False))
    print(flows[["spec", "union_units_m", "union_expected_sending_units_m", "mexico_born_headed_units_m"]].round(3).head(1).to_string(index=False))


if __name__ == "__main__":
    main()
