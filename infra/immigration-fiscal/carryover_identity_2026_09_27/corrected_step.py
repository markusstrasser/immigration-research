"""The G2 -> G3+ step with the hidden third-plus put back, and the NLSY97 same-sample reconstruction.

Corrected ratio. CPS G2 is defined by a Mexico-born parent and already holds its non-identifiers, so only
the G3+ side changes. With a the hidden share of the G3+ lineage and c the share of the identifiers' gap
that a hidden member closes,

    lineage G3+ gap = (1 - a) g3 + a g3 (1 - c) = g3 (1 - a c),   rho* = rho (1 - a c).

c = 0 is "like identifiers", c = 1 "like whites". Measured c comes from non-identifiers observed directly:
CPS G2 adults and CPS co-resident G3 adults (cps_identity.py; same replicate index as the published gaps, so
their SEs are joint), ACS ancestry-revealed adults (acs_ancestry.py; independent sample, delta method),
and the published BA+ sources the carry-over lane used (NLSY97 Table 13, Pew, MASP). The years-of-schooling
convention (54.3% / 72.4%) is carried as the object under review, not as a measurement.

NLSY97 reconstruction (published tables only): within the cross-sectional sample, which did not screen on
Hispanic identification, G3 identifiers against all G3 (Table 13); the full sample's G3 with its screened
non-identifiers removed or restored (Tables 2, 12, 13).

Inputs: _cache/reps_<label>.npz (cps_identity.py), derived/acs_ancestry_contrasts.csv, the carry-over lane's
NLSY97 Table 2 constants (imported read-only from its summarize.py). Outputs: derived/corrected_step.csv,
derived/nlsy97_same_sample.csv, derived/cps_nlsy_decomposition.csv.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import csv
import importlib.util
import math
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CARRY = HERE.parent / "generation_carryover_2026_09_27"
DERIVED = HERE / "derived"
CACHE = HERE / "_cache"
LABELS = ["CPS_ASEC_2022_2025", "CPS_ASEC_2022_2026"]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


carry = _load("carryover_summarize", CARRY / "summarize.py")
T2 = carry.NLSY_T2  # IZA DP12704 Table 2, PDF p.45: {measure: {generation: (value, se, n)}}
# IZA DP12704 Table 12, PDF p.56: % identified as Hispanic (value, se, n).
T12 = {"cross_section": {"G2": (94.63, 1.82, 155), "G3": (79.38, 4.58, 79)},
       "combined": {"G2": (97.37, 0.82, 384), "G3": (86.97, 2.71, 155)}}
# IZA DP12704 Table 13, PDF p.57: cross-sectional G3 by Hispanic identification (value, se); n 65 / 11 / 76.
T13 = {"educ_years": {"id": (13.58, .35), "nonid": (14.22, 1.16), "all": (13.70, .35)},
       "ba_plus": {"id": (23.01, 5.18), "nonid": (29.17, 13.70), "all": (24.28, 4.85)}}

# Hidden share of the G3+ lineage [assumption brackets named in the brief].
HIDDEN = [(0.1119, "G3 children and co-resident G3 adults, CPS (population-total lane; this lane 0.106-0.124)"),
          (0.1749, "propagation (b): G4+ one more step (identity_loss_propagation population_arms.csv)"),
          (0.2295, "propagation (c): compounding, rho 0.5 (population_arms.csv)"),
          (0.2825, "Duncan-Trejo 1994-2006 G3 (population-total lane decomposition)")]
MEASURES = ["ba_plus", "earnings_worker_mean", "ledger_partial_per_adult", "educ_years"]
ACS_FOR = {"ba_plus": "ba_plus", "earnings_worker_mean": "earnings_worker_mean",
           "ledger_partial_per_adult": "income_person_mean", "educ_years": "educ_years"}


def sdr(v):
    return float(np.sqrt(4 / 160 * np.square(v[1:] - v[0]).sum()))


def reps(label):
    z = np.load(CACHE / f"reps_{label}.npz")
    return {tuple(k.split("|")): z[k] for k in z.files}


def closing(R, label, frame, m, nid, idg):
    return 1 - R[(label, frame, m, nid, "white3plus")] / R[(label, frame, m, idg, "white3plus")]


def c_sources(R, label, m, acs):
    """(name, kind, c) with c a replicate vector (joint with the CPS gaps) or (value, se) external."""
    out = [("like identifiers", "bound", (0.0, 0.0))]
    out.append(("CPS G2 adults 25-64, not Mexican, same measure", "cps", closing(R, label, "pop", m, "G2_nonmex", "G2_id")))
    out.append(("CPS co-resident G3 adults 18+ (25+ for schooling), not Mexican, same measure", "cps",
                closing(R, label, "cores_one", m, "G3anc_nonmex", "G3anc_id")))
    a = acs[(acs.measure == ACS_FOR[m]) & (acs.contrast == "closing share, anc_nonmex vs anc_id")].iloc[0]
    out.append((f"ACS 2024 US-born 25-64 with Mexican ancestry, not Mexican ({ACS_FOR[m]})", "ext", (a.value, a.se)))
    if m == "ba_plus":
        g_id = T13["ba_plus"]["id"][0] - T2["ba_plus"]["white4plus"][0]
        d = T13["ba_plus"]["nonid"][0] - T13["ba_plus"]["id"][0]
        se = math.hypot(T13["ba_plus"]["nonid"][1], T13["ba_plus"]["id"][1]) / abs(g_id)
        out.append(("NLSY97 G3 cross-section, not Hispanic (Table 13, n 11)", "ext", (d / -g_id, se)))
        g3 = -R[(label, "pop", m, "G3plus_all", "white3plus")][0]
        out.append(("Pew 2015-16 US-born of US-born parents 25+, +2.54 pts over the CPS G3+ gap (n 34)", "ext",
                    (2.54 / g3, math.nan)))
        out.append(("MASP only-Anglo mention, +0.63 pts over the CPS G3+ gap (n 24)", "ext", (0.63 / g3, math.nan)))
    if m == "educ_years":
        g_id = T13["educ_years"]["id"][0] - T2["educ_years"]["white4plus"][0]
        d = T13["educ_years"]["nonid"][0] - T13["educ_years"]["id"][0]
        se = math.hypot(T13["educ_years"]["nonid"][1], T13["educ_years"]["id"][1]) / abs(g_id)
        out.append(("NLSY97 G3 cross-section, not Hispanic (Table 13, n 11)", "ext", (d / -g_id, se)))
    if m != "ba_plus":
        out.append(("years convention under review: DT 2017 +0.57 y / 1.049 y (0.543)", "convention", (0.5433, 0.0)))
        out.append(("years convention under review: DT 2017 +0.76 y / 1.049 y (0.724)", "convention", (0.7244, 0.0)))
    out.append(("like whites", "bound", (1.0, 0.0)))
    return out


def pooled_g3(R, label, m):
    """Inverse-variance mean of the two same-sample G3 closing shares on a schooling measure: CPS co-resident
    G3 adults (replicate SE) and NLSY97 Table 13 (published SEs). Returns (value, se)."""
    c = closing(R, label, "cores_one", m, "G3anc_nonmex", "G3anc_id")
    g_id = T13[m]["id"][0] - T2[m]["white4plus"][0]
    nl = (T13[m]["nonid"][0] - T13[m]["id"][0]) / -g_id
    nl_se = math.hypot(T13[m]["nonid"][1], T13[m]["id"][1]) / abs(g_id)
    w = np.array([1 / sdr(c) ** 2, 1 / nl_se ** 2])
    return float((w * [c[0], nl]).sum() / w.sum()), float(1 / math.sqrt(w.sum()))


def corrected(label, acs):
    R = reps(label)
    rows = []
    for m in MEASURES:
        g2 = R[(label, "pop", m, "G2", "white3plus")]
        g3 = R[(label, "pop", m, "G3plus_all", "white3plus")]
        rho = g3 / g2
        for a, a_src in HIDDEN:
            for name, kind, c in c_sources(R, label, m, acs):
                if kind == "cps":
                    rs = rho * (1 - a * c)
                    cv, cse, se = float(c[0]), sdr(c), sdr(rs)
                else:
                    cv, cse = c
                    rs = rho * (1 - a * cv)
                    se = math.sqrt(sdr(rs) ** 2 + (0 if not np.isfinite(cse) else (rho[0] * a * cse) ** 2))
                rows.append(dict(source=label, measure=m, hidden_share=a, hidden_share_source=a_src, attriter_value=name,
                                 kind=kind, closing_share=cv, closing_share_se=cse, rho_published=float(rho[0]),
                                 rho_published_se=sdr(rho), rho_corrected=float(rs[0]), rho_corrected_se=se,
                                 g3plus_identifier_gap=float(g3[0]), g3plus_lineage_gap=float(g3[0] * (1 - a * cv)),
                                 g2_gap=float(g2[0])))
            # Composite: the G3-rate share of hidden members (0.1119) at white parity, as the co-resident G3
            # non-identifiers measure; the extra share beyond it (the post-G3 losses) at the value measured for
            # adult children whose parent reports Mexican origin (co-resident G4 lineage), or at 0 and 1.
            if a <= HIDDEN[0][0]:
                continue
            a3, a4 = HIDDEN[0][0], a - HIDDEN[0][0]
            c4m = 1 - R[(label, "cores_both", m, "G4par_nonmex", "white3plus")] / R[(label, "cores_both", m, "G4par_id", "white3plus")]
            stable = abs(R[(label, "cores_both", m, "G4par_id", "white3plus")][0]) > 2 * sdr(R[(label, "cores_both", m, "G4par_id", "white3plus")])
            comps = [("composite: G3-rate share like whites, extra share like identifiers", np.zeros_like(rho)),
                     ("composite: G3-rate share like whites, extra share like whites", np.ones_like(rho))]
            # Same composite with the G3-rate share at the pooled same-sample G3 value instead of exactly 1.
            c3, c3se = pooled_g3(R, label, "educ_years" if m == "educ_years" else "ba_plus")
            rs = rho * (1 - a3 * c3)
            rows.append(dict(source=label, measure=m, hidden_share=a, hidden_share_source=a_src,
                             attriter_value="composite: G3-rate share at the pooled same-sample G3 value "
                                            "(CPS co-resident + NLSY97; schooling), extra share like identifiers",
                             kind="composite", closing_share=float(a3 * c3 / a), closing_share_se=c3se * a3 / a,
                             rho_published=float(rho[0]), rho_published_se=sdr(rho), rho_corrected=float(rs[0]),
                             rho_corrected_se=math.sqrt(sdr(rs) ** 2 + (rho[0] * a3 * c3se) ** 2),
                             g3plus_identifier_gap=float(g3[0]), g3plus_lineage_gap=float(g3[0] * (1 - a3 * c3)),
                             g2_gap=float(g2[0])))
            if stable:
                comps.append(("composite: G3-rate share like whites, extra share at the measured G4 one-step value", c4m))
            for name, c4 in comps:
                rs = rho * (1 - a3 - a4 * c4)
                rows.append(dict(source=label, measure=m, hidden_share=a, hidden_share_source=a_src, attriter_value=name,
                                 kind="composite", closing_share=float((a3 + a4 * c4[0]) / a), closing_share_se=sdr(c4) * a4 / a,
                                 rho_published=float(rho[0]), rho_published_se=sdr(rho), rho_corrected=float(rs[0]),
                                 rho_corrected_se=sdr(rs), g3plus_identifier_gap=float(g3[0]),
                                 g3plus_lineage_gap=float(g3[0] * (1 - a3 - a4 * c4[0])), g2_gap=float(g2[0])))
    return rows


def nlsy97():
    """Same-sample attrition checks on the published NLSY97 tables. Gaps are to white 4th+."""
    rows = []
    for m in ("ba_plus", "educ_years"):
        w, sw, _ = T2[m]["white4plus"]
        g2, sg2, _ = T2[m]["G2"]
        g2 -= w
        g3_full, sg3, _ = T2[m]["G3"]
        idv, ids = T13[m]["id"]
        nidv, nids = T13[m]["nonid"]
        allv, alls = T13[m]["all"]
        # (i) Cross-section only: all G3 against identifiers only, same sample. G2 is the full sample's.
        shift = allv - idv
        rows.append(dict(measure=m, quantity="cross-section G3: all minus identifiers (same sample)", value=shift,
                         se=math.hypot(nids, ids) * (1 - T12["cross_section"]["G3"][0] / 100), note="Table 13"))
        rows.append(dict(measure=m, quantity="attrition component of rho G2->G3 in the cross-section (shift over the G2 gap)",
                         value=-shift / abs(g2), se=math.hypot(nids, ids) * (1 - T12["cross_section"]["G3"][0] / 100) / abs(g2),
                         note="lineage G3 minus identifier G3 over the full-sample G2 gap"))
        # (ii) Full sample: remove or restore non-identifiers at the cross-section non-identifier mean.
        s_full = 1 - T12["combined"]["G3"][0] / 100
        s_true = 1 - T12["cross_section"]["G3"][0] / 100
        id_full = (g3_full - s_full * nidv) / (1 - s_full)
        lin_full = (1 - s_true) * id_full + s_true * nidv
        for q, v in (("full-sample G3: identifiers only", id_full), ("full-sample G3: published (13.0% non-identifiers)", g3_full),
                     ("full-sample G3: lineage-complete (20.6% non-identifiers)", lin_full)):
            rows.append(dict(measure=m, quantity=q + ": level", value=v, se=math.nan, note="Tables 2 12 13"))
            rows.append(dict(measure=m, quantity=q + ": rho G2->G3", value=(v - w) / g2,
                             se=abs((v - w) / g2) * math.hypot(sg3 / (v - w), sg2 / g2), note="delta method; gaps independent"))
        rows.append(dict(measure=m, quantity="rho G2->G3+ pooled (published)", value=(T2[m]["G3plus_all"][0] - w) / g2,
                         se=math.nan, note="Table 2"))
    return rows


def decomposition(nl):
    """CPS 0.92 against NLSY97 0.76 on BA+: cohort, identification convention, remainder."""
    out = []
    for label in LABELS:
        c = pd.read_csv(DERIVED / f"cps_identity_contrasts_{label}.csv")
        pick = lambda f, name: c[(c.frame == f) & (c.measure == "ba_plus") & (c.reference == "white3plus") & (c.contrast == name)].iloc[0]
        for f in ("pop", "pop_25_44", "pop_45_64", "pop_cohort"):
            r = pick(f, "rho G2 -> G3+ identifiers (published convention)")
            out.append(dict(source=label, step=f"CPS {f}: rho G2 -> G3+ identifiers", value=r.value, se=r.se))
    n = pd.DataFrame(nl)
    for q in ("full-sample G3: identifiers only: rho G2->G3", "full-sample G3: published (13.0% non-identifiers): rho G2->G3",
              "full-sample G3: lineage-complete (20.6% non-identifiers): rho G2->G3", "rho G2->G3+ pooled (published)"):
        r = n[(n.measure == "ba_plus") & (n.quantity == q)].iloc[0]
        out.append(dict(source="NLSY97_published", step=f"NLSY97 {q}", value=r.value, se=r.se))
    return out


def write(rows, name):
    with open(DERIVED / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main():
    acs = pd.read_csv(DERIVED / "acs_ancestry_contrasts.csv")
    rows = [r for label in LABELS for r in corrected(label, acs)]
    write(rows, "corrected_step.csv")
    nl = nlsy97()
    write(nl, "nlsy97_same_sample.csv")
    dec = decomposition(nl)
    write(dec, "cps_nlsy_decomposition.csv")
    pd.set_option("display.width", 250)
    pd.set_option("display.max_rows", 400)
    t = pd.DataFrame(rows)
    t = t[t.source.eq(LABELS[0])]
    print(t[["measure", "hidden_share", "attriter_value", "closing_share", "closing_share_se", "rho_published",
             "rho_corrected", "rho_corrected_se"]].round(3).to_string(index=False))
    print(pd.DataFrame(nl).round(3).to_string(index=False))
    print(pd.DataFrame(dec).round(3).to_string(index=False))


if __name__ == "__main__":
    main()
