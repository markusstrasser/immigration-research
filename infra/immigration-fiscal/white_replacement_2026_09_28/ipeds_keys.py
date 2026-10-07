"""IPEDS keys for public higher education, tuition and Pell, by race, for the rough re-keys. Not the engine.

Main case v6 (main_case_2026_10_07, item 4, from user_fee_allocation_2026_10_07) keys the union's public higher
education by measured use, credits the tuition it pays and keys its Pell grants by its share of Pell. The rough
re-keys of this lane, the Black lane and the Indian lane gave every group the CPS college key (A_HSCOL 2: enrolled,
ages 16-24, any sector) on education_services' part outside K-12, and charged other_federal_benefits, which holds
Pell (NIPA T3.12 line 26), by Social Security receipts. From v5 (oct05) on, both sides of every comparison take the
IPEDS keys instead, and on v6 (oct07) the fee terms as well (rekey_sept29.py, IPEDS_CASES and FEE_CASES; a defect fix
decided in the v6 propagation, 2026-10-07). This script measures the keys at the level IPEDS reports them, a race, and
writes derived/ipeds_keys.json:
  use      a race's share of public institutions' education-and-related cost by its FTE (graduate FTE at twice the
           cost), from the fee lane's higher_ed.py run unchanged with the race's IPEDS FTE (EF2023A EFWHITT, EFBKAAT,
           EFASIAT at each enrollment row's FTE factor) in the group column;
  tuition  its share of net tuition plus Pell (the fee lane's fee measure), at residency theta = 1 (arms 0.5 and 1.5)
           [ASSUMPTION: IPEDS has no residency by race; theta = 1 puts the race at each unit's out-of-state rate. The
           union keeps the fee lane's theta = 0.5] with its Pell at its intensity (below);
  Pell     its share of Pell grants. At public institutions (F1E01) it is the race's undergraduate FTE share times its
           within-unit intensity, capped at 1, the fee lane's rule. The intensity is halfway between 1 and NPSAS:20's
           Pell dollars per undergraduate relative to all (receipt x average award) [SOURCE: NCES 2023-466, Tables A-5
           and A-6], as the fee lane takes it for Hispanic students (its "mid"): the national ratio also carries where
           the race enrolls, which the unit shares already hold. At private institutions it is the public share times
           the race's private / public undergraduate enrollment ratio (EF2023A fall 2023, CONTROL 2-3 against 1, 50
           states and DC) [DATA; the fee lane assumes 0.75 for the union, where IPEDS gives 0.677 for Hispanic
           students]. The two are weighted by the fee lane's public share of Pell (0.68).
The union keeps the fee lane's own shares (fee_lines.json: U, s_R and the Pell share, on the account's 39,712,493).
Also written, for the library: the higher-education share of the education line (BEA's consolidated weight, the fee
lane's central), kappa (higher education's share of non-K-12 education investment), NIPA tuition, Pell's total, and
the hospital term's central inputs (health.json: government hospitals' cost, payer mix and payment-to-cost ratios).

Gates (exit 1, nothing written): higher_ed.py on its own inputs reproduces its central s_U and s_R and its Pell shares
(1e-9); the NPSAS:20 Hispanic ratio is the fee lane's PELL_HISPANIC_RATIO (1e-12); the race columns line up with
higher_ed.py's enrollment rows; each race's s_U is the same at every theta; each race's Pell share at intensity 1 is
within 0.1 of its undergraduate FTE share; the fee lane's union use and tuition shares are higher_ed.json's times phi
and its Pell share is its own formula (1e-12); the higher-education weight times the education line is the fee lane's
higher-education dollars (1e-9); the fee lane's central weights, Pell total, Pell split and hospital inputs are the
ones read here.
Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/white_replacement_2026_09_28/ipeds_keys.py
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True   # read-only import from the fee lane: write nothing beside it

import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
FEE = FISCAL / "user_fee_allocation_2026_10_07"
OUT = HERE / "derived/ipeds_keys.json"
RACES = {"white": "EFWHITT", "black": "EFBKAAT", "asian": "EFASIAT"}
THETA = (1.0, (0.5, 1.5))        # a race's residency: central and arms [ASSUMPTION, module docstring]
# NPSAS:20 undergraduates, 2019-20: Pell receipt (%) and average Pell award ($) [SOURCE: NCES 2023-466, Table A-5
# "Federal Pell Grants" and Table A-6, the total and race/ethnicity rows; Hispanic of any race, the others not Hispanic]
NPSAS = {"all": (40.2, 4100), "white": (32.1, 3900), "black": (59.5, 4200), "asian": (33.7, 4700),
         "hispanic": (49.5, 4200)}
CONTROL = {"public": [1], "private": [2, 3]}
PAYERS = ("medicare", "medicaid", "private_other")

checks = []


def gate(label, ok, detail=""):
    checks.append(label)
    print(f"  {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        raise SystemExit(f"[BLOCKED] {label}")


def constant(path, name):
    """A module-level literal of a lane script, read from its syntax tree (the script is not run)."""
    for node in ast.parse(path.read_text()).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise SystemExit(f"[BLOCKED] {path.name} defines no {name}")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_higher_ed():
    spec = importlib.util.spec_from_file_location("fee_higher_ed", FEE / "higher_ed.py")
    he = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(he)
    return he


def npsas_ratio(race):
    """Pell dollars per undergraduate of a race relative to all undergraduates (NPSAS:20)."""
    (r, a), (r0, a0) = NPSAS[race], NPSAS["all"]
    return (r / 100 * a) / (r0 / 100 * a0)


def private_ratios(he):
    """Each race's share of undergraduates at private institutions over its share at public ones."""
    hd = he.read(he.CACHE / "HD2023.csv")[["UNITID", "CONTROL", "FIPS"]]
    ef = he.num(he.read(he.CACHE / "ef2023a.csv"), ["EFTOTLT", *RACES.values(), "EFHISPT"])
    ug = ef[ef.EFALEVEL.isin([22, 42])].merge(hd, on="UNITID", how="inner", validate="many_to_one")
    ug = ug[ug.FIPS.between(1, 56)]
    out = {}
    for race, col in {**RACES, "hispanic": "EFHISPT"}.items():
        sh = {k: float(ug[ug.CONTROL.isin(v)][col].sum() / ug[ug.CONTROL.isin(v)].EFTOTLT.sum()) for k, v in CONTROL.items()}
        out[race] = dict(public_share=sh["public"], private_share=sh["private"], ratio=sh["private"] / sh["public"])
    return out


def pell_public(u, intensity):
    """A group's share of Pell at public institutions: its undergraduate FTE share times the intensity, capped at 1,
    weighted by each unit's Pell (higher_ed.py's main())."""
    uu = u[(u.fte_UG + u.fte_GR) > 0]
    m_ug = (uu.fte_mex_UG / uu.fte_UG).where(uu.fte_UG > 0, 0.0)
    return float(((m_ug * intensity).clip(upper=1.0) * uu.F1E01).sum() / uu.F1E01.sum())


def race_shares(he, pub, ef, f, ic, o, pell_split):
    """Each race's use, tuition and Pell shares: higher_ed.py's units() and shares() with the group FTE column set to
    the race's FTE (each enrollment row's FTE factor is load()'s)."""
    raw = he.num(he.read(he.CACHE / "ef2023a.csv"), ["EFTOTLT", *RACES.values()])
    key = ["UNITID", "EFALEVEL"]
    m = ef[key + ["EFTOTLT", "fte"]].merge(raw[key + ["EFTOTLT", *RACES.values()]].rename(columns={"EFTOTLT": "total_check"}),
                                           on=key, how="left", validate="one_to_one")
    gate("the race columns line up with higher_ed.py's enrollment rows", bool(np.allclose(m.total_check, m.EFTOTLT)))
    factor = (m.fte / m.EFTOTLT.where(m.EFTOTLT > 0)).fillna(0.0).to_numpy()
    priv = private_ratios(he)
    out = {}
    for race, col in RACES.items():
        mid = (1 + npsas_ratio(race)) / 2
        e2 = ef.copy()
        e2["fte_mex"] = m[col].to_numpy() * factor
        u = he.units(pub, e2, f, ic, o)
        saved = he.PELL
        he.PELL = {race: mid}          # shares() reads the intensity from the module's table
        try:
            s = {t: he.shares(u, cost="education_and_related", fee="net_tuition_plus_pell", grad_cost=2.0, theta=t,
                              pell_intensity=race) for t in (THETA[0], *THETA[1])}
        finally:
            he.PELL = saved
        gate(f"{race}: s_U is the same at every theta (residency moves fees only)",
             max(abs(v["s_U"] - s[THETA[0]]["s_U"]) for v in s.values()) < 1e-12)
        ug = float(u.fte_mex_UG.sum() / u.fte_UG.sum())
        p1 = pell_public(u, 1.0)
        gate(f"{race}: its Pell share at the unit's average intensity is within 0.1 of its undergraduate FTE share",
             abs(p1 - ug) < 0.1, f"{p1:.4f} against {ug:.4f}")
        pp = pell_public(u, mid)
        r = priv[race]["ratio"]
        out[race] = dict(use=s[THETA[0]]["s_U"], tuition=s[THETA[0]]["s_R"],
                         tuition_arms={str(t): s[t]["s_R"] for t in THETA[1]}, theta=THETA[0],
                         pell=pp * (pell_split["public"] + (1 - pell_split["public"]) * r), pell_public=pp,
                         pell_public_at_intensity_1=p1, pell_intensity=mid, npsas_ratio=npsas_ratio(race),
                         private_public_ratio=r, fte_share=float(e2.fte_mex.sum() / e2.fte.sum()), ug_fte_share=ug)
    return out, priv


def main():
    print("[IPEDS keys by race]", flush=True)
    he = load_higher_ed()
    hej = json.loads((FEE / "derived/higher_ed.json").read_text())
    fee = json.loads((FEE / "derived/fee_lines.json").read_text())
    hl = json.loads((FEE / "derived/health.json").read_text())
    fee_py = FEE / "fee_lines.py"
    pub, ef, f, ic, o = he.load()
    u = he.units(pub, ef, f, ic, o)
    c = he.shares(u, **he.CENTRAL)
    gate("positive control: higher_ed.py on its own inputs reproduces its central s_U and s_R (1e-9)",
         abs(c["s_U"] - hej["central"]["s_U"]) < 1e-9 and abs(c["s_R"] - hej["central"]["s_R"]) < 1e-9,
         f"{c['s_U']:.6f}, {c['s_R']:.6f}")
    gate("positive control: and its Pell shares at public institutions at each intensity (1e-9)",
         all(abs(pell_public(u, v) - hej["pell_share_public"][k]) < 1e-9 for k, v in he.PELL.items()))
    gate("the NPSAS:20 Hispanic ratio is the fee lane's PELL_HISPANIC_RATIO (1e-12)",
         abs(npsas_ratio("hispanic") - he.PELL_HISPANIC_RATIO) < 1e-12, f"{npsas_ratio('hispanic'):.10f}")
    split = {"public": constant(fee_py, "PELL_PUBLIC")["central"], "private_relative_union": constant(fee_py, "PELL_PRIVATE_RELATIVE")["central"]}
    gate("the fee lane's Pell total is the one it wrote", constant(fee_py, "PELL_BN") == fee["pell"]["total_bn"])
    races, priv = race_shares(he, pub, ef, f, ic, o, split)

    phi = fee["frames"]["phi"]
    gate("the fee lane's union use and tuition shares are higher_ed.json's central times phi (1e-12)",
         abs(fee["higher_ed"]["U"] - hej["central"]["s_U"] * phi) < 1e-12
         and abs(fee["higher_ed"]["s_R"] - hej["central"]["s_R"] * phi) < 1e-12)
    want = hej["pell_share_public"]["mid"] * phi * (split["public"] + (1 - split["public"]) * split["private_relative_union"])
    gate("the fee lane's union Pell share is its formula at its central (1e-12)", abs(fee["pell"]["share"] - want) < 1e-12,
         f"{fee['pell']['share']:.6f}")
    gate("the fee lane's education weights are its central (consolidated)", constant(fee_py, "CENTRAL_WEIGHTS") == "consolidated")
    h = fee["nipa"]["weights"]["consolidated"]["higher"]
    gate("the higher-education weight times the education line is the fee lane's higher-education dollars (1e-9)",
         abs(h * fee["nipa"]["education_line_bn"] - fee["higher_ed"]["higher_dollars_bn"]) < 1e-9,
         f"{h:.10f} x {fee['nipa']['education_line_bn']}")
    mix = {q: hl["mix"][q][0] for q in PAYERS}
    pcr = {q: hl["pcr"][q][0] for q in PAYERS}
    gate("health.json's payers are the hospital term's (Medicare, Medicaid, private and other)", set(hl["mix"]) == set(PAYERS) == set(hl["pcr"]))

    out = dict(
        note=("IPEDS keys for the rough re-keys (ipeds_keys.py docstring). races: a race's share of public higher "
              "education's use (education-and-related cost by FTE), of net tuition plus Pell (tuition, theta = 1; "
              "tuition_arms at 0.5 and 1.5) and of Pell (public at the race's mid intensity, private at its "
              "enrollment ratio). union: the fee lane's shares on the account's 39,712,493. constants: the fee "
              "lane's. hospital: health.json's central inputs; net_bn = g x mix x (1 - pcr), the insured payers' "
              "unpaid cost (negative where payments exceed cost)."),
        races=races,
        union=dict(use=fee["higher_ed"]["U"], tuition=fee["higher_ed"]["s_R"], pell=fee["pell"]["share"], theta=0.5,
                   source="user_fee_allocation_2026_10_07/derived/fee_lines.json"),
        constants=dict(higher_weight=h, kappa=fee["nipa"]["kappa"], tuition_bn=fee["nipa"]["tuition_bn"],
                       pell_bn=fee["pell"]["total_bn"], pell_public=split["public"],
                       pell_private_relative_union=split["private_relative_union"],
                       education_line_bn=fee["nipa"]["education_line_bn"],
                       higher_dollars_bn=fee["higher_ed"]["higher_dollars_bn"]),
        hospital=dict(g_bn=hl["g_bn"], mix=mix, pcr=pcr, net_bn={q: hl["g_bn"] * mix[q] * (1 - pcr[q]) for q in PAYERS},
                      union_fee_bn=fee["health"]["central"]["personal"]["fee_term_bn"],
                      union_key_bn=fee["health"]["central"]["personal"]["key_term_bn"]),
        npsas={k: dict(pell_receipt_pct=v[0], average_pell_usd=v[1]) for k, v in NPSAS.items()},
        private_public_enrollment=priv,
        inputs={p: sha(FEE / p) for p in ("derived/fee_lines.json", "derived/higher_ed.json", "derived/health.json",
                                          "higher_ed.py", "fee_lines.py")},
    )
    OUT.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    for race, v in races.items():
        print(f"  {race:6s} use {v['use']:.6f}  tuition {v['tuition']:.6f} (theta 0.5 {v['tuition_arms']['0.5']:.6f}, "
              f"1.5 {v['tuition_arms']['1.5']:.6f})  Pell {v['pell']:.6f} (public {v['pell_public']:.6f} at intensity "
              f"{v['pell_intensity']:.4f}; private/public {v['private_public_ratio']:.3f})")
    print(f"  union  use {out['union']['use']:.6f}  tuition {out['union']['tuition']:.6f}  Pell {out['union']['pell']:.6f}")
    print(f"[written] {OUT.relative_to(FISCAL.parent.parent)} ({len(checks)} gates)")


if __name__ == "__main__":
    main()
