#!/usr/bin/env python3
"""Phase 1 of the pre-registered back-test: what the account's own frame predicts for state administrative totals.

Frame: CPS ASEC 2025 (income 2024), the file behind the account's keys, in two readings.
- adopted, the prediction: the adopted case's CPS stack before its fill-in step, the arm
  `row4+status_state_aware|central|audit_rules_alone` of cps_imputation_keys_2026_09_23/combine_onbooks_lane.py,
  built with that lane's own functions and aligned to this frame's rows. Audit row 4's weights scale the
  Mexico-born naturalized and noncitizens outside CA+TX to the ACS 2024 in all 161 columns; the state-aware
  status flag marks the unauthorized, who lose their EITC and keep the on-books lane's central share of their
  ACTC (0.526 Mexico-born, 0.550 other Latin-American-born). The fill-in step (the union-matched hot deck) and
  the package's national shifts on these lines have no state dimension; phase 2 reports them beside any miss.
- published, a secondary: the builder's keys on the published weights with the audit's paper flag
  (combine_status.unauthorized) at a flat on-books share of 0.60, the reading before the stack.
ASEC 2024 (income 2023) in the published reading gives a matched-year secondary for IRS SOI tax year 2023, the
latest year SOI publishes by state.

The union and the sharing rule come from full_account_spending_2026_09_20/builder.py (`canonical_target`,
`equal_unit_share`) in the published reading and from the CPS lane's `common` in the adopted one.

Writes, and reads no external figure:
  derived/predictions.csv           reading x check x series x state: share of the 50-state + DC total, its
                                    replicate standard error, the group's share of the state's amount under both
                                    allocations, and other foreign-born persons' share (a declared diagnostic)
  derived/prediction_scalars.csv    national quantities: key shares, birth counts, Medicaid coverage and ratios
  derived/state_replicates.csv.gz   the 161 replicate values behind each keyed state share and group share
  derived/birth_cells.csv           the six declared birth cells with their 161 replicate shares
  derived/power.csv                 every scored statistic: its role, rule, tolerance and the standard error
                                    sampling alone gives it
  derived/prediction_audit.json     pins, gates, sample counts, the row-4 factors and on-books shares

Gates (exit with [BLOCKED]): the published reading reproduces the account's incidence keys
(full_account_spending_2026_09_20/derived/incidence_keys.csv) and the paper rule's change to the credit key
(cps_imputation_keys_2026_09_23/derived/status_combination_keys.csv, status_0.60) to 1e-9; the CPS lane's frame
matches this one row for row (weights, civilians, union); the adopted shares, through the lane's
translate.line_deltas, reproduce the stored stack cells of the credit, SSI, Social Security and railroad lines
(main_case_2026_09_24/derived/stack_line_deltas.json, the file the adopted package reads) to 1e-9 bn.

Run from the repository root (about three minutes):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/backtest_admin_totals_2026_09_28/predict.py
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True  # read-only imports from other lanes

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FISCAL = ROOT / "infra/immigration-fiscal"
sys.path.insert(0, str(HERE))
sys.path.insert(1, str(FISCAL / "full_account_spending_2026_09_20"))
sys.path.insert(2, str(FISCAL / "cps_imputation_keys_2026_09_23"))
from estimators import Z, delta_fit  # noqa: E402
from builder import CPS_SHA, canonical_target, equal_unit_share  # noqa: E402
import combine_onbooks_lane as L  # noqa: E402
import combine_status as cs  # noqa: E402
import common as lane  # noqa: E402  the CPS lane's frame and masks
import translate  # noqa: E402

SOURCES = {  # survey year -> (zip, sha256); income year is one less
    2024: (FISCAL / "same_year_tax_2026_09_20/_cache/asecpub24csv.zip",
           "cdb39cdac34bef99dd0940ab28e306f692404c2eea44d85dfd634214872a0a09"),
    2025: (FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip", CPS_SHA),
}
ACCOUNT_KEYS = FISCAL / "full_account_spending_2026_09_20/derived/incidence_keys.csv"
STATUS_KEYS = FISCAL / "cps_imputation_keys_2026_09_23/derived/status_combination_keys.csv"
STACK = FISCAL / "main_case_2026_09_24/derived/stack_line_deltas.json"
STACK_ARM = "row4+status_state_aware|central|audit_rules_alone"  # the adopted stack before its fill-in step
STACK_LINES = {"refundable_tax_credits": "refundable_credits", "ssi": "ssi", "social_security": "social_security",
               "railroad_retirement": "social_security"}
ADOPTED_SHARES = ("origin", "central")
PAPER_ON_BOOKS = 0.60
PRIMARY = "asec2025_adopted"
REPS = [f"pwwgt{i}" for i in range(161)]
PERSON = sorted(set(cs.STATUS_COLS) | {
    "A_SEX", "PEFNTVTY", "PEMNTVTY", "PRDTHSP", "SPM_ID", "EIT_CRED", "ACTC_CRD", "NOW_MCAID",
    "PEPAR1", "PEPAR2", "PEPAR1TYP", "PEPAR2TYP", "MARSUPWT"})
MEXICO = 303
US_BORN = [57, 60, 66, 69, 73, 78]  # builder.py `canonical_target`: US states and outlying areas
LINE_AMOUNTS = HERE / "derived/line_amounts.json"  # line_amounts.cjs: the September 27 case at specs 48 and 11
MATERIAL_BN = 2.0            # a key error is material when it moves the September 27 case by more than this
NON_PTC_BN = 110.46          # dataset_integrity_2026_09_23/derived/spending_mts_credits.json: line 25 less PTC
TOLERANCE = {"births_count": 0.10, "births_distribution": 0.05, "medicaid_level": 0.05, "medicaid_ratio": 0.10,
             "medicaid_group_share": 0.10}
STATES = {1: "AL", 2: "AK", 4: "AZ", 5: "AR", 6: "CA", 8: "CO", 9: "CT", 10: "DE", 11: "DC", 12: "FL", 13: "GA",
          15: "HI", 16: "ID", 17: "IL", 18: "IN", 19: "IA", 20: "KS", 21: "KY", 22: "LA", 23: "ME", 24: "MD", 25: "MA",
          26: "MI", 27: "MN", 28: "MS", 29: "MO", 30: "MT", 31: "NE", 32: "NV", 33: "NH", 34: "NJ", 35: "NM", 36: "NY",
          37: "NC", 38: "ND", 39: "OH", 40: "OK", 41: "OR", 42: "PA", 44: "RI", 45: "SC", 46: "SD", 47: "TN", 48: "TX",
          49: "UT", 50: "VT", 51: "VA", 53: "WA", 54: "WV", 55: "WI", 56: "WY"}
FIPS = sorted(STATES)
# Birth cells for the distribution test: the brief's high-share states, with NM, NV and CO pooled (too few children
# in the frame to stand alone) and every other state in "rest". Chosen for power before any external figure was read.
BIRTH_CELLS = {"CA": [6], "TX": [48], "AZ": [4], "IL": [17], "NM_NV_CO": [35, 32, 8]}
BIRTH_CELLS["rest"] = [c for c in FIPS if not any(c in v for v in BIRTH_CELLS.values())]
KEYED = {  # check -> [(series, role)]; the first series is the prediction
    "1_refundable_credits": [("credits_ssn", "prediction"), ("credits_raw", "baseline_1"), ("population", "baseline_2"),
                             ("eitc_ssn", "component"), ("eitc_raw", "component_baseline_1"),
                             ("actc_ssn", "component"), ("actc_raw", "component_baseline_1")],
    "2_ssi": [("ssi", "prediction"), ("population", "baseline_1"), ("age65plus", "baseline_2")],
    "2_oasdi": [("social_security", "prediction"), ("population", "baseline_1"), ("age65plus", "baseline_2")],
}
ALLOCATIONS = ("personal", "shared")


def sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def sdr(values) -> np.ndarray:
    """Successive-difference replicate standard error along the last axis; index 0 is the full sample."""
    values = np.asarray(values, float)
    return np.sqrt(4 / 160 * np.square(values[..., 1:] - values[..., :1]).sum(axis=-1))


def load(year: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    path, pin = SOURCES[year]
    if sha(path) != pin:
        raise SystemExit(f"[BLOCKED] {path.name} does not match its pin")
    with zipfile.ZipFile(path) as z:
        d = pd.read_csv(z.open(f"pppub{year % 100}.csv"), usecols=PERSON)
        hh = pd.read_csv(z.open(f"hhpub{year % 100}.csv"), usecols=["H_SEQ", "GESTFIPS", "HPUBLIC", "HLORENT"])
        w = pd.read_csv(z.open(f"asec_csv_repwgt_{year}.csv"), usecols=["h_seq", "PPPOS", *REPS])
    d = d.merge(w.rename(columns={"h_seq": "PH_SEQ"}), on=["PH_SEQ", "PPPOS"], validate="one_to_one", how="left")
    d = d.merge(hh[["H_SEQ", "GESTFIPS"]], left_on="PH_SEQ", right_on="H_SEQ", validate="many_to_one", how="left")
    if d[REPS + ["GESTFIPS"]].isna().any().any():
        raise SystemExit(f"[BLOCKED] ASEC {year}: missing replicate weights or state")
    np.testing.assert_allclose(d.MARSUPWT / 100, d.pwwgt0, rtol=0, atol=.01)
    if sorted(d.GESTFIPS.unique()) != FIPS:
        raise SystemExit(f"[BLOCKED] ASEC {year}: GESTFIPS is not the 50 states and DC")
    return d, hh


def quiet_flag(run) -> np.ndarray:
    """A status flag from the lane's rules; impute() prints its Medicaid caveat, which must still be there."""
    with contextlib.redirect_stderr(io.StringIO()) as note:
        flag = run()
    if "[DEGRADED]" not in note.getvalue():
        raise SystemExit("[BLOCKED] impute_status no longer reports its Medicaid caveat; recheck the rule")
    return flag


def mothers(d: pd.DataFrame) -> np.ndarray:
    """Row index of each person's mother in the household (a female PEPAR1/PEPAR2; biological first), else -1."""
    key = d.PH_SEQ.to_numpy(np.int64) * 100 + d.A_LINENO.to_numpy(np.int64)
    row = pd.Series(np.arange(len(d)), index=key)
    if row.index.duplicated().any():
        raise SystemExit("[BLOCKED] duplicate household line numbers")
    female = d.A_SEX.eq(2).to_numpy()
    cand = []
    for p in (1, 2):
        line = d[f"PEPAR{p}"].to_numpy(np.int64)
        idx = row.reindex(d.PH_SEQ.to_numpy(np.int64) * 100 + line).to_numpy()
        idx = np.where((line > 0) & ~np.isnan(idx), idx, -1).astype(np.int64)
        ok = (idx >= 0) & female[np.maximum(idx, 0)]
        cand.append((np.where(ok, idx, -1), d[f"PEPAR{p}TYP"].to_numpy()))
    (m1, t1), (m2, t2) = cand
    return np.where((m1 >= 0) & ((m2 < 0) | (t1 == 1) | (t2 != 1)), m1, m2)


class Frame:
    """One ASEC file with the account's universe, union and state."""

    def __init__(self, year: int):
        self.year = year
        self.d, self.hh = load(year)
        self.civ, self.target = canonical_target(self.d)
        self.state = pd.Categorical(self.d.GESTFIPS, categories=FIPS).codes
        self.onehot = np.eye(len(FIPS))[self.state]
        self.other_fb = self.civ & ~self.target & ~self.d.PENATVTY.isin(US_BORN).to_numpy()


class View:
    """A frame under one reading: its 161 weights and its key vectors by allocation."""

    def __init__(self, f: Frame, reading: str, W: np.ndarray, vec: dict[str, dict[str, np.ndarray]]):
        self.f, self.label, self.W, self.vec = f, f"asec{f.year}_{reading}", W, vec
        self.d, self.civ, self.target, self.state = f.d, f.civ, f.target, f.state

    def by_state(self, v, mask: np.ndarray) -> np.ndarray:
        """Weighted totals by state x replicate over the rows in mask (51 x 161)."""
        v = np.broadcast_to(np.asarray(v, float), mask.shape)
        keep = mask & (v != 0)
        return self.f.onehot[keep].T @ (v[keep, None] * self.W[keep])

    def total(self, v, mask: np.ndarray) -> np.ndarray:
        v = np.broadcast_to(np.asarray(v, float), mask.shape)
        return v[mask] @ self.W[mask]

    def rate(self, flag: np.ndarray, mask: np.ndarray) -> np.ndarray:
        return self.total(flag.astype(float), mask) / self.total(1.0, mask)


def describe(v: View, flag: np.ndarray) -> dict:
    w = v.W[:, 0]
    return {"persons": len(v.d), "civilian_m": float(w[v.civ].sum() / 1e6), "union_m": float(w[v.target].sum() / 1e6),
            "flagged_m": float(w[v.civ & flag].sum() / 1e6), "flagged_union_m": float(w[v.target & flag].sum() / 1e6)}


def published_view(f: Frame) -> tuple[View, np.ndarray]:
    """The builder's keys on the published weights, with the audit's paper flag at a flat on-books share."""
    d = f.d
    u = quiet_flag(lambda: cs.unauthorized(d[cs.STATUS_COLS], f.hh, d))
    eitc, actc = d.EIT_CRED.to_numpy(float), d.ACTC_CRD.to_numpy(float)
    eitc_ssn, actc_ssn = np.where(u, 0.0, eitc), np.where(u, actc * PAPER_ON_BOOKS, actc)
    dollars = {"credits_ssn": eitc_ssn + actc_ssn, "credits_raw": eitc + actc, "eitc_ssn": eitc_ssn,
               "eitc_raw": eitc, "actc_ssn": actc_ssn, "actc_raw": actc,
               "ssi": d.SSI_VAL.to_numpy(float), "social_security": d.SS_VAL.to_numpy(float)}
    vec = {k: {"personal": v, "shared": equal_unit_share(v, d.SPM_ID)} for k, v in dollars.items()}
    for k, v in (("population", np.ones(len(d))), ("age65plus", d.A_AGE.ge(65).to_numpy(float))):
        vec[k] = {"personal": v, "shared": v}
    return View(f, "published", d[REPS].to_numpy(float), vec), u


def gate_stack(W, W4, civ, union, plain, ruled) -> tuple[float, dict]:
    """The adopted shares through the lane's translate.line_deltas, against the stored stack cells."""
    base = L.weigh(plain, W[civ], W[union], civ, union)
    plain4 = L.weigh(plain, W4[civ], W4[union], civ, union)
    new = L.weigh(ruled, W4[civ], W4[union], civ, union, cs.STATUS_KEYS, plain4)
    model = json.loads(translate.MODEL.read_text())
    line25 = next(x for x in model["spending"]["lines"] if x["id"] == L.REFUNDABLE)
    f_new = json.loads(L.MTS.read_text())["non_ptc_remainder_bn"] / line25["national_bn"]
    hf = W[civ].sum(axis=0) / lane.RESIDENT
    stored = json.loads(STACK.read_text())["payloads"][STACK_ARM]["spending"]
    gaps = [abs(r["reps"][0] * (f_new if r["line"] == L.REFUNDABLE else 1.0)
                - stored[r["line"]][r["key"]][r["allocation"]])
            for r in translate.line_deltas(model, base, new, hf)
            if r["side"] == "spending" and STACK_LINES.get(r["line"]) == r["key"]]
    if len(gaps) != 2 * len(STACK_LINES) or max(gaps) > 1e-9:
        raise SystemExit(f"[BLOCKED] the adopted shares do not reproduce the stored stack cells: "
                         f"{max(gaps):.2e} bn over {len(gaps)} cells")
    return max(gaps), new


def adopted_view(f: Frame, pub: View, audit: dict) -> View:
    """The stack arm STACK_ARM, built by the CPS lane's own functions on its frame and aligned to f's rows."""
    if not (lane.CACHE / "asec25_lane.parquet").exists():
        raise SystemExit("[BLOCKED] the CPS lane's frame cache is missing; rebuilding it would write outside this lane")
    d = lane.load_frame()
    civ, union = lane.masks(d)
    index = lane.spm_index(d)
    W = d[lane.REPS].to_numpy(float)
    rows = f.d[["PH_SEQ", "PPPOS"]].merge(
        pd.DataFrame({"PH_SEQ": d.PH_SEQ.to_numpy(), "PPPOS": d.PPPOS.to_numpy(), "row": np.arange(len(d))}),
        on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one").row
    if len(d) != len(f.d) or rows.isna().any():
        raise SystemExit("[BLOCKED] the CPS lane's frame does not hold this frame's persons")
    at = rows.to_numpy(np.int64)
    if not (np.array_equal(W[at], pub.W) and np.array_equal(civ[at], f.civ) and np.array_equal(union[at], f.target)):
        raise SystemExit("[BLOCKED] the CPS lane's frame disagrees with this frame on weights, civilians or union")
    s_in, hh = cs.status_inputs()
    aware = quiet_flag(lambda: L.state_aware_flag(s_in, hh, d, L.STATUS_BLIND_2024))
    configs, labels = L.share_configs(d)
    on_books = configs[ADOPTED_SHARES]
    arms, info = L.weight_arms(d, W, L.acs_cells())
    W4 = arms["row4"]
    del arms
    plain = L.frame_vectors(d, aware, None, index)
    ruled = L.frame_vectors(d, aware, on_books, index, cs.STATUS_KEYS)
    worst, new = gate_stack(W, W4, civ, union, plain, ruled)
    parts = {}
    for name, frame in (("eitc", d.assign(ACTC_CRD=0.0)), ("actc", d.assign(EIT_CRED=0.0))):
        parts[f"{name}_ssn"] = cs.status_vectors(frame, aware, on_books, index)[1]
        parts[f"{name}_raw"] = cs.status_vectors(frame, aware, None, index)[1]
    for a in ALLOCATIONS:
        for kind, whole in (("ssn", ruled), ("raw", plain)):
            split = parts[f"eitc_{kind}"][a]["refundable_credits"] + parts[f"actc_{kind}"][a]["refundable_credits"]
            if np.abs(split - whole[a]["refundable_credits"]).max() > 1e-6:
                raise SystemExit(f"[BLOCKED] EITC and ACTC parts do not add to the {kind} credit key ({a})")

    def pick(source, key):
        return {a: source[a][key][at] for a in ALLOCATIONS}

    vec = {"credits_ssn": pick(ruled, "refundable_credits"), "credits_raw": pick(plain, "refundable_credits"),
           **{name: pick(p, "refundable_credits") for name, p in parts.items()},
           **{k: pick(plain, k) for k in ("ssi", "social_security", "population", "age65plus")}}
    view = View(f, "adopted", W4[at], vec)
    w0 = view.W[:, 0]
    for series, key in (("credits_ssn", "refundable_credits"), ("ssi", "ssi"), ("social_security", "social_security")):
        for a in ALLOCATIONS:
            v = vec[series][a]
            if abs((v[f.target] @ w0[f.target]) / (v[f.civ] @ w0[f.civ]) - new[(a, key)][0]) > 1e-12:
                raise SystemExit(f"[BLOCKED] the aligned {series} vector does not give the lane's share ({a})")
    audit[view.label] = {**describe(view, aware[at]), "gate_stack_max_abs_bn": worst, "stack_arm": STACK_ARM,
                         "on_books_mexico_born_other_latin": list(labels[ADOPTED_SHARES]),
                         "row4_factors": {k: v for k, v in info.items() if k in ("factor_natz", "factor_noncit")}}
    return view


def gate_account(v: View) -> float:
    account = pd.read_csv(ACCOUNT_KEYS).set_index(["allocation", "key"]).target_share
    w, worst = v.W[:, 0], 0.0
    medicaid = v.d.MCAID.eq(1).to_numpy(float)
    for allocation in ALLOCATIONS:
        for key, series in (("refundable_credits", "credits_raw"), ("ssi", "ssi"), ("social_security", "social_security"),
                            ("population", "population"), ("age65plus", "age65plus"), ("medicaid_covered", None)):
            x = medicaid if series is None else v.vec[series][allocation]
            share = (x[v.target] @ w[v.target]) / (x[v.civ] @ w[v.civ])
            worst = max(worst, abs(share - account[(allocation, key)]))
    if worst > 1e-9:
        raise SystemExit(f"[BLOCKED] the account's incidence keys are not reproduced: {worst:.2e}")
    return worst


def gate_status(v: View) -> float:
    lane_keys = pd.read_csv(STATUS_KEYS).set_index(["method", "allocation", "key"]).rel_change
    w, worst = v.W[:, 0], 0.0
    for allocation in ALLOCATIONS:
        s = {name: (v.vec[name][allocation][v.target] @ w[v.target]) / (v.vec[name][allocation][v.civ] @ w[v.civ])
             for name in ("credits_raw", "credits_ssn")}
        change = s["credits_ssn"] / s["credits_raw"] - 1
        worst = max(worst, abs(change - lane_keys[(f"status_{PAPER_ON_BOOKS:.2f}", allocation, "refundable_credits")]))
    if worst > 1e-9:
        raise SystemExit(f"[BLOCKED] the paper rule does not reproduce status_combination_keys.csv: {worst:.2e}")
    return worst


class Out:
    def __init__(self):
        self.rows, self.scalars, self.reps, self.cells, self.power = [], [], [], [], []
        self.arrays, self.cell_arrays = {}, {}

    def scalar(self, v: View, check: str, quantity: str, values, note: str = "") -> np.ndarray:
        values = np.asarray(values, float)
        self.scalars.append(dict(frame=v.label, check=check, quantity=quantity, value=values[0],
                                 se=float(sdr(values)), note=note))
        return values


def keyed(out: Out, v: View, check: str, series: str, role: str, pop_share: np.ndarray) -> None:
    """State shares of a key, the group's share of each state's amount under both allocations, and other
    foreign-born persons' share of it (the declared diagnostic regressor)."""
    vp, vs = v.vec[series]["personal"], v.vec[series]["shared"]
    amount = v.by_state(vp, v.civ)
    share = amount / amount.sum(axis=0)
    shared_civ = v.by_state(vs, v.civ)
    g = {"personal": v.by_state(vp, v.target) / amount, "shared": v.by_state(vs, v.target) / shared_civ}
    other = {"personal": v.by_state(vp, v.f.other_fb)[:, 0] / amount[:, 0],
             "shared": v.by_state(vs, v.f.other_fb)[:, 0] / shared_civ[:, 0]}
    positive = np.bincount(v.state[v.civ & (vp > 0)], minlength=len(FIPS))
    for i, fips in enumerate(FIPS):
        out.rows.append(dict(frame=v.label, check=check, series=series, role=role, state=STATES[fips], fips=fips,
                             share=share[i, 0], share_se=sdr(share[i]), amount=amount[i, 0],
                             group_share_shared=g["shared"][i, 0], group_share_shared_se=sdr(g["shared"][i]),
                             group_share_personal=g["personal"][i, 0], group_share_personal_se=sdr(g["personal"][i]),
                             other_fb_share_shared=other["shared"][i], other_fb_share_personal=other["personal"][i],
                             pop_group_share=pop_share[i, 0], sample_persons=int(positive[i])))
    if role in ("prediction", "baseline_1", "component", "component_baseline_1"):
        for quantity, values in (("share", share), ("group_share_shared", g["shared"]),
                                 ("group_share_personal", g["personal"])):
            for i, fips in enumerate(FIPS):
                out.reps.append(dict(frame=v.label, check=check, series=series, quantity=quantity,
                                     state=STATES[fips], **{f"r{k}": values[i, k] for k in range(161)}))
    out.arrays[(v.label, check, series)] = (share, g)


def counts(out: Out, v: View, check: str, series: str, role: str, mask: np.ndarray) -> None:
    amount = v.by_state(1.0, mask)
    share = amount / amount.sum(axis=0)
    n = np.bincount(v.state[mask], minlength=len(FIPS))
    for i, fips in enumerate(FIPS):
        out.rows.append(dict(frame=v.label, check=check, series=series, role=role, state=STATES[fips], fips=fips,
                             share=share[i, 0], share_se=sdr(share[i]), amount=amount[i, 0], sample_persons=int(n[i])))
    cell_shares = np.vstack([share[[FIPS.index(c) for c in members]].sum(axis=0) for members in BIRTH_CELLS.values()])
    out.cell_arrays[(v.label, check, series)] = cell_shares
    for name, values in zip(BIRTH_CELLS, cell_shares):
        out.cells.append(dict(frame=v.label, check=check, series=series, role=role, cell=name,
                              **{f"r{k}": values[k] for k in range(161)}))


def keyed_checks(out: Out, v: View, checks: list[str]) -> None:
    pop_share = v.by_state(1.0, v.target) / v.by_state(1.0, v.civ)
    for check in checks:
        for series, role in KEYED[check]:
            keyed(out, v, check, series, role, pop_share)
    for name, by in v.vec.items():
        if name == "age65plus":
            continue
        for allocation in ALLOCATIONS:
            x = by[allocation]
            out.scalar(v, "group_key_share", f"{name}_{allocation}", v.total(x, v.target) / v.total(x, v.civ))


def births(out: Out, v: View, audit: dict) -> None:
    """Births to mothers of Mexican origin and to Mexico-born mothers, from children in the frame by their mother.
    Age 0 at the March 2025 interview is the birth cohort of about March 2024 - March 2025 (national counts);
    ages 0-2 triple the sample for the state distribution."""
    d, civ, target = v.d, v.civ, v.target
    m = mothers(d)
    present, mi = m >= 0, np.maximum(m, 0)
    hisp, born = d.PRDTHSP.to_numpy(), d.PENATVTY.to_numpy()
    mex_mother = np.where(present, hisp[mi] == 1, hisp == 1)
    mexico_mother = d.PEMNTVTY.eq(MEXICO).to_numpy()
    foreign_mother = np.where(present, ~np.isin(born[mi], US_BORN), ~np.isin(d.PEMNTVTY, US_BORN))
    infant = civ & d.A_AGE.eq(0).to_numpy()
    child = civ & d.A_AGE.le(2).to_numpy()
    female15_44 = civ & d.A_SEX.eq(2).to_numpy() & d.A_AGE.between(15, 44).to_numpy()
    women = {"union": female15_44 & target, "mex_origin": female15_44 & (hisp == 1),
             "mexico_born": female15_44 & (born == MEXICO), "all": female15_44}
    spec = {"3_births_mex_origin": (mex_mother, women["union"], target),
            "3_births_mexico_born": (mexico_mother, women["mexico_born"], civ & (born == MEXICO))}
    audit["birth_cells"] = {name: [STATES[c] for c in members] for name, members in BIRTH_CELLS.items()}
    for check, (flag, women_mask, population) in spec.items():
        counts(out, v, check, "children_0_2", "prediction", child & flag)
        counts(out, v, check, "infants", "secondary", infant & flag)
        counts(out, v, check, "women_15_44", "baseline_1", women_mask)
        counts(out, v, check, "group_population", "baseline_2", population)
    counts(out, v, "3_births_mex_origin", "infants_union", "secondary", infant & target)

    all_infants = v.total(1.0, infant)
    for name, mask in (("all", infant), ("mex_origin", infant & mex_mother), ("mexico_born", infant & mexico_mother),
                       ("mex_origin_foreign_mother", infant & mex_mother & foreign_mother),
                       ("union", infant & target)):
        count = out.scalar(v, "3_births_count", f"infants_{name}", v.total(1.0, mask))
        out.scalar(v, "3_births_share", f"infants_{name}", count / all_infants, "share of all infants in the frame")
        out.scalar(v, "3_births_mother_present", f"infants_{name}", v.rate(present, mask))
    for group, women_mask, population in (("mex_origin", women["union"], target),
                                          ("mexico_born", women["mexico_born"], civ & (born == MEXICO))):
        out.scalar(v, "3_births_share", f"baseline_1_{group}", v.total(1.0, women_mask) / v.total(1.0, women["all"]),
                   "the group's share of women 15-44")
        out.scalar(v, "3_births_share", f"baseline_2_{group}", v.total(1.0, population) / v.total(1.0, civ),
                   "the group's share of civilians")
    for name, mask in women.items():
        out.scalar(v, "3_births_count", f"women_15_44_{name}", v.total(1.0, mask))
    for group, women_mask, population in (("mex_origin", women["union"], target),
                                          ("mexico_born", women["mexico_born"], civ & (born == MEXICO))):
        out.scalar(v, "3_births_count", f"baseline_1_{group}_births",
                   all_infants * v.total(1.0, women_mask) / v.total(1.0, women["all"]),
                   "all infants x the group's share of women 15-44")
        out.scalar(v, "3_births_count", f"baseline_2_{group}_births",
                   all_infants * v.total(1.0, population) / v.total(1.0, civ),
                   "all infants x the group's share of civilians")

    # Medicaid-paid share. MCAID: Medicaid, PCHIP or other means-tested coverage in 2024; NOW_MCAID: at interview.
    last_year, now = d.MCAID.eq(1).to_numpy(), d.NOW_MCAID.eq(1).to_numpy()
    mother_cov = present & last_year[mi]
    level = {}
    for group, flag in (("mex_origin", mex_mother), ("mexico_born", mexico_mother), ("all", np.ones(len(d), bool))):
        level[("mothers", group)] = out.scalar(v, "3_medicaid_paid_level", f"mothers_covered_2024_{group}",
                                               v.rate(mother_cov, infant & flag & present),
                                               "mothers of infants, present in the household")
        level[("infants", group)] = out.scalar(v, "3_medicaid_paid_level", f"infants_covered_now_{group}",
                                               v.rate(now, infant & flag), "infants' own coverage at interview")
    for name, mask in women.items():
        level[("women", name)] = out.scalar(v, "3_medicaid_paid_level", f"women_15_44_covered_2024_{name}",
                                            v.rate(last_year, mask))
    union_all = out.scalar(v, "3_medicaid_paid_level", "union_all_ages_covered_2024", v.rate(last_year, target))
    everyone = out.scalar(v, "3_medicaid_paid_level", "civilians_all_ages_covered_2024", v.rate(last_year, civ))
    for reading in ("mothers", "infants"):
        for group in ("mex_origin", "mexico_born"):
            out.scalar(v, "3_medicaid_paid_ratio", f"{reading}_{group}",
                       level[(reading, group)] / level[(reading, "all")],
                       "group rate over the all-births rate from the same reading")
    out.scalar(v, "3_medicaid_paid_ratio", "women_15_44_union", level[("women", "union")] / level[("women", "all")],
               "brief's reading: union women 15-44 over all women 15-44")
    out.scalar(v, "3_medicaid_paid_ratio", "women_15_44_mexico_born",
               level[("women", "mexico_born")] / level[("women", "all")])
    out.scalar(v, "3_medicaid_paid_ratio", "baseline_2_union_all_ages", union_all / everyone,
               "the group's all-age coverage over everyone's")

    covered_women = last_year & female15_44
    out.scalar(v, "3_medicaid_births_group_share", "women_15_44_covered_union",
               v.total(1.0, covered_women & target) / v.total(1.0, covered_women),
               "brief's reading: the union's share of Medicaid-covered women 15-44")
    out.scalar(v, "3_medicaid_births_group_share", "women_15_44_covered_mexico_born",
               v.total(1.0, covered_women & (born == MEXICO)) / v.total(1.0, covered_women))
    for reading, weight, base in (("infants", now, infant), ("mothers", mother_cov, infant & present)):
        for group, flag in (("mex_origin", mex_mother), ("mexico_born", mexico_mother)):
            out.scalar(v, "3_medicaid_births_group_share", f"{reading}_{group}",
                       v.total(weight.astype(float), base & flag) / v.total(weight.astype(float), base))
    out.scalar(v, "3_medicaid_births_group_share", "baseline_1_union_share_women_15_44",
               v.total(1.0, women["union"]) / v.total(1.0, women["all"]))
    out.scalar(v, "3_medicaid_births_group_share", "baseline_2_union_share_medicaid_covered",
               v.total(last_year.astype(float), target) / v.total(last_year.astype(float), civ))
    audit[v.label]["sample"] = {name: int(mask.sum()) for name, mask in (
        ("infants", infant), ("infants_mex_origin", infant & mex_mother), ("infants_mexico_born", infant & mexico_mother),
        ("children_0_2_mex_origin", child & mex_mother), ("children_0_2_mexico_born", child & mexico_mother),
        ("women_15_44_union", women["union"]), ("women_15_44_mexico_born", women["mexico_born"]))}


def power_screen(out: Out, audit: dict) -> None:
    """Every scored statistic with its role, rule, declared tolerance and the standard error the frame's sampling
    alone gives it. Roles: verdict (the adopted reading's statistic whose call is the check's call), baseline,
    secondary (reported with a call, not the verdict). Powered by sampling: 1.96 SE <= 2 x tolerance (the call
    rule in estimators.call); delta's scored SE is the larger of this and the fit's HC3 term (estimators.delta_se),
    so a check powered here can still end without power. Distributions follow estimators.distribution_call."""
    lines = json.loads(LINE_AMOUNTS.read_text())["lines"]
    keyed_bn = {"1_refundable_credits": NON_PTC_BN, "2_ssi": lines["ssi"]["national_bn"]["low"],
                "2_oasdi": lines["social_security"]["national_bn"]["low"] + lines["railroad_retirement"]["national_bn"]["low"]}
    hf = audit["household_fraction"]
    value = {(r["frame"], r["check"], r["quantity"]): r for r in out.scalars}

    def add(frame, check, statistic, role, prediction, se, tolerance, basis, rule="call", powered=None, note=""):
        out.power.append(dict(frame=frame, check=check, statistic=statistic, role=role, rule=rule,
                              prediction=prediction, sampling_se=se, tolerance=tolerance, tolerance_basis=basis,
                              powered_by_sampling=bool(Z * se <= 2 * tolerance) if powered is None else powered,
                              note=note))

    for (frame, check, series), (share, g) in out.arrays.items():
        role = dict(KEYED[check])[series]
        if role not in ("prediction", "baseline_1") or series == "population":
            continue
        key = "credits_ssn" if check.startswith("1_") else series
        stat_role = "baseline" if role == "baseline_1" else "verdict" if frame == PRIMARY else "secondary"
        for allocation in ("shared", "personal"):
            s = value[(frame, "group_key_share", f"{key}_{allocation}")]["value"]
            dollars = keyed_bn[check] * hf * s
            tolerance = MATERIAL_BN / (dollars * (1 - s))
            fits = np.array([delta_fit(share[:, 0], share[:, k], g[allocation][:, k])["delta"] for k in range(161)])
            note = ""
            if role == "baseline_1":
                p_share, _ = out.arrays[(frame, check, "credits_ssn")]
                gap = delta_fit(p_share[:, 0], share[:, 0], g[allocation][:, 0])["delta"]
                note = f"delta this series would score if the prediction were exact: {gap:.4f}"
            add(frame, check, f"delta_{series}_{allocation}", stat_role, 0.0, float(sdr(fits)), tolerance,
                f"${MATERIAL_BN:g}bn over the key's group dollars ${dollars:.2f}bn (${keyed_bn[check]:.3f}bn x "
                f"household fraction {hf:.5f} x share {s:.4f}) x (1 - share)", note=note)
    for frame in (PRIMARY, "asec2025_published"):
        for group in ("mex_origin", "mexico_born"):
            check = f"3_births_{group}"
            for kind in ("share", "count"):
                r = value[(frame, f"3_births_{kind}", f"infants_{group}")]
                role = "verdict" if frame == PRIMARY and kind == "share" else "secondary"
                add(frame, check, f"national_{kind}_relative", role, r["value"], r["se"] / r["value"],
                    TOLERANCE["births_count"], f"relative error of the national {kind}")
            for series in ("children_0_2", "infants"):
                cells = out.cell_arrays[(frame, check, series)]
                noise = float(np.abs(cells[:, 1:] - cells[:, :1]).sum(axis=0).mean())
                base = {b: 0.5 * float(np.abs(cells[:, 0] - out.cell_arrays[(frame, check, b)][:, 0]).sum())
                        for b in ("women_15_44", "group_population")}
                role = "verdict" if frame == PRIMARY and series == "children_0_2" else "secondary"
                add(frame, check, f"distribution_{series}", role, np.nan, noise, TOLERANCE["births_distribution"],
                    f"dissimilarity over the {len(BIRTH_CELLS)} declared cells; sampling_se is the expected "
                    "dissimilarity from sampling noise alone", rule="distribution",
                    powered=bool(noise <= TOLERANCE["births_distribution"]),
                    note=f"dissimilarity to baseline 1 {base['women_15_44']:.4f}, "
                         f"to baseline 2 {base['group_population']:.4f}")
        for check, quantity, kind in (
                ("3_medicaid_births_group_share", "women_15_44_covered_union", "medicaid_group_share"),
                ("3_medicaid_paid_ratio", "women_15_44_union", "medicaid_ratio"),
                ("3_medicaid_paid_level", "women_15_44_covered_2024_union", "medicaid_level"),
                ("3_medicaid_births_group_share", "mothers_mex_origin", "medicaid_group_share"),
                ("3_medicaid_births_group_share", "infants_mex_origin", "medicaid_group_share"),
                ("3_medicaid_paid_ratio", "mothers_mex_origin", "medicaid_ratio"),
                ("3_medicaid_paid_ratio", "infants_mex_origin", "medicaid_ratio"),
                ("3_medicaid_paid_level", "mothers_covered_2024_mex_origin", "medicaid_level"),
                ("3_medicaid_paid_level", "infants_covered_now_mex_origin", "medicaid_level")):
            r = value[(frame, check, quantity)]
            relative = kind != "medicaid_level"
            role = "verdict" if frame == PRIMARY and quantity == "women_15_44_covered_union" else "secondary"
            add(frame, check, quantity, role, r["value"], r["se"] / r["value"] if relative else r["se"],
                TOLERANCE[kind], "relative error" if relative else "absolute error, share of births")
    audit["tolerances"] = {"material_bn": MATERIAL_BN, "non_ptc_bn": NON_PTC_BN, **TOLERANCE}


def write(frame: pd.DataFrame, path: Path) -> None:
    gz = {"method": "gzip", "mtime": 0} if path.suffix == ".gz" else None
    frame.to_csv(path, index=False, float_format="%.10g", lineterminator="\n", compression=gz)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=HERE / "derived")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    audit = {"sources": {f"asec{y}": {"path": str(p.relative_to(ROOT)), "sha256": pin} for y, (p, pin) in SOURCES.items()},
             "stack_file": {"path": str(STACK.relative_to(ROOT)), "sha256": sha(STACK)},
             "rules": {"published": {"flag": "cps_imputation_keys_2026_09_23/combine_status.py::unauthorized",
                                     "eitc": "zeroed", "actc_on_books_share": PAPER_ON_BOOKS},
                       "adopted": {"flag": "combine_onbooks_lane.py::state_aware_flag (STATUS_BLIND_2024)",
                                   "eitc": "zeroed", "actc_on_books_share": "share_configs origin central",
                                   "weights": "weight_arms row4"}}}
    out = Out()
    f = Frame(2025)
    pub, paper = published_view(f)
    audit[pub.label] = {**describe(pub, paper), "gate_account_max_abs": gate_account(pub),
                        "gate_status_max_abs": gate_status(pub)}
    # translate.household_fraction as stack_split.py takes it: the account's spending lines reach the frame's
    # civilians at this fraction, so a key's group dollars are national x fraction x share
    audit["household_fraction"] = float(pub.W[pub.civ, 0].sum() / lane.RESIDENT)
    adopted = adopted_view(f, pub, audit)
    for v in (adopted, pub):
        keyed_checks(out, v, list(KEYED))
        births(out, v, audit)
        print(f"  ✓ {v.label} predicted")
    del f, pub, adopted
    f = Frame(2024)
    pub, paper = published_view(f)
    audit[pub.label] = describe(pub, paper)
    keyed_checks(out, pub, ["1_refundable_credits"])
    print(f"  ✓ {pub.label} predicted")
    power_screen(out, audit)
    write(pd.DataFrame(out.rows), args.out_dir / "predictions.csv")
    write(pd.DataFrame(out.scalars), args.out_dir / "prediction_scalars.csv")
    write(pd.DataFrame(out.reps), args.out_dir / "state_replicates.csv.gz")
    write(pd.DataFrame(out.cells), args.out_dir / "birth_cells.csv")
    write(pd.DataFrame(out.power), args.out_dir / "power.csv")
    (args.out_dir / "prediction_audit.json").write_text(json.dumps(audit, indent=1, sort_keys=True) + "\n")
    a, p = audit[PRIMARY], audit["asec2025_published"]
    print(f"  ✓ gates: account keys {p['gate_account_max_abs']:.1e}, paper rule {p['gate_status_max_abs']:.1e}, "
          f"stack cells {a['gate_stack_max_abs_bn']:.1e} bn")


if __name__ == "__main__":
    main()
