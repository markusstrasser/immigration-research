"""Gates for the generation carry-over lane. Run after analyze_*.py, disconfirm.py and summarize.py."""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
D = HERE / "derived"
FAIL = []


def check(ok, msg):
    print(("  ✓ " if ok else "  ✗ ") + msg)
    if not ok:
        FAIL.append(msg)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# 1. CPS 2025 G3/G4+ counts reproduce the split lane before any year was added.
audit = json.loads((D / "cps_audit_CPS_ASEC_2022_2025.json").read_text())
ref = pd.read_csv(HERE.parent / "generation_split_2026_09_20/derived/cps_generation_split.csv").query(
    "arm == 'reported_linkage' and age == 'all'").set_index("generation").people
for k, exp in [("G3_Mexico_GP_observed", 2.870e6), ("G4plus_all_US_GP_observed", 2.073e6)]:
    got = audit["gate_2025"][k]
    check(abs(got - ref[k]) < 1 and round(got / 1e6, 3) == exp / 1e6, f"CPS2025 {k} {got:,.0f} = split lane {ref[k]:,.0f} ({exp/1e6:.3f}m)")

# 2. Adopted-account ratios are computed from the CSV, not retyped.
acc = pd.read_csv(HERE.parent / "generation_account_2026_09_24/derived/generation_results.csv")
co = pd.read_csv(D / "carryover.csv")
aa = co[co.source.str.startswith("adopted_account_")]
check(len(aa) == 8, "eight adopted-account ratio rows (2 conventions x 2 ends x 2 steps)")
for r in aa.itertuples():
    conv = r.frame.split()[1]
    band = r.frame.rsplit(", ", 1)[1].split()[0]
    v = acc[acc.convention.eq(conv) & acc.band_end.eq(band)].set_index("generation").per_adult_usd
    a, b = r.generation.split("->")
    check(np.isclose(r.rho, v[b] / v[a], rtol=1e-12), f"adopted {conv}/{band} {r.generation} rho {r.rho:.4f}")

# 3. Every published NLSY97 number used is printed on its cited PDF page.
pages = (HERE / "_cache/dp12704.txt").read_text().split("\f")
s = _load("carry_sum", HERE / "summarize.py")


def on_page(val, page, fmt="{:.2f}"):
    txt = pages[page - 1]
    cands = {fmt.format(val), fmt.format(val).lstrip("0").replace("-0.", "-."), f"{val:.3f}", f"{val:.3f}".replace("0.", ".", 1),
             f"{val:,.0f}" if float(val).is_integer() else "__"}
    return any(re.search(r"(?<![\d.])" + re.escape(c) + r"(?![\d])", txt) for c in cands)


bad = []
for m, gens in s.NLSY_T2.items():
    for g, (v, se, n) in gens.items():
        for x in (v, se):
            if not on_page(x, 45):
                bad.append(("T2", m, g, x))
for (m, cite), gens in s.NLSY_REG.items():
    page = int(re.search(r"PDF p\.(\d+)", cite).group(1))
    for g, (b, se) in gens.items():
        for x in (b, se):
            if not (on_page(x, page, "{:.3f}") or on_page(x, page)):
                bad.append((cite[:25], g, x))
for g, pair in s.NLSY_T5.items():
    for v, se in pair:
        for x in (v, se):
            if not on_page(x, 48):
                bad.append(("T5", g, x))
for g, (v, se) in s.NLSY_T6_DELTA.items():
    for x in (v, se):
        if not on_page(x, 49):
            bad.append(("T6", g, x))
check(on_page(.28, 49) and on_page(.02, 49), "Table 6 parental coefficients .28 (.02) on p.49")
for tab in (s.NLSY_T12, s.NLSY_T12_COMBINED):
    for g, (v, se, n) in tab.items():
        for x in (v, se):
            if not on_page(x, 56):
                bad.append(("T12", g, x))
for k, dct in s.NLSY_T13.items():
    for m in ("educ_years", "ba_plus"):
        if not on_page(dct[m], 57):
            bad.append(("T13", k, dct[m]))
check(not bad, f"all NLSY97 table numbers found on their cited PDF pages ({'none missing' if not bad else bad})")

# 4. Deliverable CSVs carry the required columns and LF line endings.
for f in ["gaps_by_generation.csv", "carryover.csv", "attrition_bounds.csv", "projection.csv"]:
    t = pd.read_csv(D / f)
    check({"source", "measure", "generation", "n", "se"} <= set(t.columns), f"{f} has source/measure/generation/n/se")
    check(b"\r\n" not in (D / f).read_bytes(), f"{f} uses LF line endings")

# 5. Reweighting reproduces the group's cell distribution (synthetic).
cps = _load("carry_cps", HERE / "analyze_cps.py")
rng = np.random.default_rng(0)
cg, cr = rng.integers(0, 5, 300), rng.integers(0, 5, 2000)
wg, wr = rng.uniform(.5, 2, (300, 3)), rng.uniform(.5, 2, (2000, 3))
out, unc = cps.reweight(cg, wg, cr, wr)
for r in range(3):
    sg = np.bincount(cg, weights=wg[:, r], minlength=5)
    so = np.bincount(cr, weights=out[:, r], minlength=5)
    check(np.allclose(sg / sg.sum(), so / so.sum()) and unc == 0, f"reweight replicate {r} matches group cell shares")

# 6. Pooled CPS frames: co-resident observed G3/G4+ never appear in the population frame.
g = pd.read_csv(D / "cps_gaps_CPS_ASEC_2022_2025.csv")
check(not g[g.frame.eq("pop")].generation.isin(["G3_obs", "G4plus_obs"]).any(), "observed G3/G4+ only in co-resident frames")
check(g[g.frame.eq("cores_both") & g.generation.eq("G4plus_obs") & g.measure.eq("ba_plus")].n.iloc[0] == 302,
      "cores_both G4+ BA n = 302 (all G4+ require both parents)")

# 7. Drift test: the split rule's constants still match the identity lane's pooled G3 closing shares. summarize.py copies
#    them and never reads that lane, which imports this one; this gate only compares.
ci = pd.read_csv(HERE.parent / "carryover_identity_2026_09_27/derived/corrected_step.csv")
comp = ci[ci.attriter_value.str.startswith("composite: G3-rate share at the pooled same-sample G3 value")]
A3 = s.RATES["G3"][0][1]
label = {"CPS_ASEC_2022_2025": s.SPLIT_C3_CENTRAL, "CPS_ASEC_2022_2026": s.SPLIT_C3_SENSITIVITY}
drift = []
for r in comp.itertuples():
    c3, c3se = s.SPLIT_C3[label[r.source]]["educ_years" if r.measure == "educ_years" else "ba_plus"]
    got = (r.closing_share * r.hidden_share / A3, r.closing_share_se * r.hidden_share / A3,
           (1 - r.g3plus_lineage_gap / r.g3plus_identifier_gap) / A3)
    if max(abs(got[0] - c3), abs(got[1] - c3se), abs(got[2] - c3)) > 1e-4:
        drift.append((r.source, r.measure, r.hidden_share, got))
check(len(comp) == 24 and not drift, f"SPLIT_C3 matches carryover_identity corrected_step.csv to 1e-4 ({len(comp)} composite rows"
      f"{'' if not drift else '; drift ' + str(drift)})")
check(np.isclose(A3, ci.hidden_share.min(), rtol=0, atol=1e-12), f"G3-rate share {A3} = the identity lane's")

# 8. The years convention survives only as labelled sensitivity rows; every split row obeys lineage = gap x (1 - a3 C3).
att = pd.read_csv(D / "attrition_bounds.csv")
led = att[att.measure.eq("ledger_partial_per_adult")]
yrs = led[led.scenario.eq("sensitivity_years_share_convention")]
check(len(yrs) == 2 * len(led[led.scenario.eq("attriters_like_identifiers")]) and yrs.delta_source.str.startswith(s.YEARS_SHARE).all(),
      f"years convention kept on every ledger cell and rate, labelled '{s.YEARS_SHARE}'")
check(not led.scenario.eq("attriters_at_measured_nonidentifier_values").any(), "no ledger row presents the years share as measured")
sp = att[att.scenario.eq(s.SPLIT)]
check(len(sp) > 0 and np.allclose(sp.lineage_gap, sp.observed_gap * (1 - sp.g3_rate_share * sp.closing_share_g3), rtol=1e-12),
      f"{len(sp)} split rows: lineage gap = observed x (1 - a3 C3)")

# 9. Corrected G3 -> G4+ ratios under the split rule, and the projection built on them.
cr = pd.read_csv(D / "attrition_corrected_rho.csv")
ids = cr[cr.scenario.eq("attriters_like_identifiers")].groupby(["source", "measure"]).rho_G3_G4plus.first()
spr = cr[cr.scenario.eq(s.SPLIT)]
nl = spr.source.eq("NLSY97_published")
check(np.allclose(spr[~nl].rho_G3_G4plus, [ids[(a, b)] for a, b in zip(spr[~nl].source, spr[~nl].measure)], rtol=1e-12),
      "split rule leaves CPS and GSS G3->G4+ ratios at the identifiers' (both cells scale alike)")
nl_obs = cr[cr.scenario.eq("attriters_like_identifiers") & cr.source.eq("NLSY97_published")].groupby("measure").gap_G3.first()
check(np.allclose(spr[nl].gap_G3, spr[nl].measure.map(nl_obs)), "NLSY97 G3 takes no split correction (its G3 includes non-identifiers)")
pr = pd.read_csv(D / "projection.csv")
b0 = pr[pr.path.str.startswith("stall") & pr.generation.eq("G3+ (measured base)")].set_index("measure").gap
for key, lab in [("generation split, central", s.SPLIT_C3_CENTRAL),
                 ("generation split, sensitivity", s.SPLIT_C3_SENSITIVITY)]:
    sel = spr[spr.measure.eq("ba_plus") & spr.attrition_G4plus.eq(.292) & spr.delta_source.str.contains(lab, regex=False)]
    p = pr[pr.path.str.startswith(key)]
    c3 = s.SPLIT_C3[lab]["ba_plus"][0]
    lin = p[p.generation.eq("G3+ (lineage base)")].set_index("measure").gap
    check(sorted(sel.source) == ["CPS_ASEC_2022_2025", "GSS_2000_2024", "NLSY97_published"]
          and np.allclose(p[p.generation.eq("G4")].rho_step, sel.rho_G3_G4plus.mean(), rtol=1e-12),
          f"{key}: step {sel.rho_G3_G4plus.mean():.4f} is the mean of CPS, GSS and NLSY97 (NLSY97 was dropped before 2026-09-28)")
    check(np.allclose(lin[["ba_plus", "ledger_partial_per_adult"]], b0[["ba_plus", "ledger_partial_per_adult"]] * (1 - A3 * c3),
                      rtol=1e-12) and np.isclose(lin["educ_years"], b0["educ_years"]),
          f"{key}: lineage base = CPS identifiers' G3+ x (1 - {A3} x {c3}); NLSY97 years base unchanged")
w = pr[pr.path.str.startswith("attrition worst case")].set_index(["measure", "generation"]).gap
check(np.isclose(w[("ledger_partial_per_adult", "G4")], (1 - .556) * b0["ledger_partial_per_adult"]),
      "worst case: lineage G4 = (1 - 0.556) x identifiers' gap, as its basis states")
sn = cr[cr.scenario.eq("sensitivity_nlsy97_g3_as_published") & cr.delta_source.str.startswith("generation split")]
s_nl = 1 - s.NLSY_T12_COMBINED["G3"][0] / 100
sn_label = sn.delta_source.map(lambda d: [k for k in s.SPLIT_C3 if k in d])
c3n = pd.Series([s.SPLIT_C3[k[0]][s.SPLIT_C3_FOR[m]][0] if len(k) == 1 else np.nan for k, m in zip(sn_label, sn.measure)],
                index=sn.index)
check(len(sn) == 4 and np.allclose(sn.rho_G3_G4plus, sn.measure.map(ids.loc["NLSY97_published"]) * (1 - s_nl * c3n), rtol=1e-12),
      f"NLSY97 G3 as published ({s_nl:.1%} non-identifiers): split ratio = observed x (1 - s C3)")

print(f"\n{'FAILED: ' + str(len(FAIL)) if FAIL else 'all gates pass'}")
raise SystemExit(1 if FAIL else 0)
