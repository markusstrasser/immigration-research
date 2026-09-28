#!/usr/bin/env python3
"""Phase 2, step 2: every declared statistic scored against the administrative targets with the frozen estimators.

Reads the frozen phase-1 outputs (derived/predictions.csv, prediction_scalars.csv, state_replicates.csv.gz,
birth_cells.csv, power.csv, prediction_audit.json) and the targets (derived/targets.csv, target_national.csv).
Every call uses estimators.py as committed at 883182b; nothing here changes a tolerance, a rule or a prediction.

Writes:
  derived/scores.csv            every statistic in power.csv, plus the declared secondary targets: prediction,
                                target, error, scored SE, tolerance, call; for delta, the dollars at both ends
  derived/check_calls.csv       one call per check, combined as PREDICTIONS.md says
  derived/dissimilarity.csv     prediction and baselines against each target (state distributions)
  derived/state_errors.csv      A_s / P_s - 1 with the replicate SE for the states the brief names
  derived/diagnostics.csv       the declared diagnostics: leave-one-out, other foreign-born control, slope on pi
  derived/candidate_shifts.json the key correction each missed delta implies, for candidate.cjs

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/backtest_admin_totals_2026_09_28/score.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
DER = HERE / "derived"
sys.path.insert(0, str(HERE))
from estimators import (Z, call, delta_fit, delta_fit_controlled, delta_se, dissimilarity,  # noqa: E402
                        distribution_call, implied_share, replicate_cov, slope_on, wald)

PRIMARY = "asec2025_adopted"
COLS = [f"r{k}" for k in range(161)]
ALLOCATIONS = ("shared", "personal")
END = {"shared": "low (spec 48)", "personal": "high (spec 11)"}
BRIEF_STATES = ["CA", "TX", "AZ", "NM", "NV", "CO", "IL"]
CELLS = {"CA": ["CA"], "TX": ["TX"], "AZ": ["AZ"], "IL": ["IL"], "NM_NV_CO": ["NM", "NV", "CO"]}
# keyed check -> (prediction series, primary target, national total the key splits in $bn, lines it drives)
KEYED = {"1_refundable_credits": ("credits_ssn", "soi_credits_total", 110.46,
                                  {"refundable_tax_credits": ("refundable_credits", 1.0)}),
         "2_ssi": ("ssi", "ssa_ssi_fed_admin_2024", 65.134, {"ssi": ("ssi", 1.0)}),
         "2_oasdi": ("social_security", "ssa_oasdi_dec2024", 1447.965 + 14.493,
                     {"social_security": ("social_security", 1447.965 / (1447.965 + 14.493)),
                      "railroad_retirement": ("social_security", 14.493 / (1447.965 + 14.493))})}
# declared secondary targets and components (PREDICTIONS.md, diagnostics 3 and 5): (check, series, target, label)
EXTRA = [("1_refundable_credits", "credits_ssn", "soi_credits_refundable", "refundable EIC + ACTC"),
         ("1_refundable_credits", "eitc_ssn", "soi_eitc_total", "EITC component"),
         ("1_refundable_credits", "actc_ssn", "soi_actc", "ACTC component"),
         ("1_refundable_credits", "eitc_raw", "soi_eitc_total", "EITC component, no rule"),
         ("1_refundable_credits", "actc_raw", "soi_actc", "ACTC component, no rule"),
         ("2_ssi", "ssi", "ssa_ssi_federal_2024", "federal SSI alone"),
         ("2_ssi", "ssi", "ssa_ssi_fed_admin_dec2024", "December 2024 (ASR tables 10 x 11)")]


def load():
    pred = pd.read_csv(DER / "predictions.csv")
    reps = pd.read_csv(DER / "state_replicates.csv.gz")
    scal = pd.read_csv(DER / "prediction_scalars.csv")
    power = pd.read_csv(DER / "power.csv")
    audit = json.loads((DER / "prediction_audit.json").read_text())
    targets = pd.read_csv(DER / "targets.csv")
    national = pd.read_csv(DER / "target_national.csv").set_index("quantity").value
    return pred, reps, scal, power, audit, targets, national


class Data:
    def __init__(self):
        self.pred, self.reps, self.scal, self.power, self.audit, targets, self.national = load()
        self.states = sorted(self.pred.state.unique())
        self.A = {t: g.set_index("state").share.loc[self.states].to_numpy() for t, g in targets.groupby("target")}
        self.hf = self.audit["household_fraction"]

    def series(self, frame, check, series):
        g = self.pred[(self.pred.frame == frame) & (self.pred.check == check) & (self.pred.series == series)]
        return g.set_index("state").loc[self.states]

    def replicates(self, frame, check, series, quantity):
        g = self.reps[(self.reps.frame == frame) & (self.reps.check == check) & (self.reps.series == series)
                      & (self.reps.quantity == quantity)]
        return g.set_index("state").loc[self.states, COLS].to_numpy()

    def scalar(self, frame, check, quantity):
        r = self.scal[(self.scal.frame == frame) & (self.scal.check == check) & (self.scal.quantity == quantity)]
        if len(r) != 1:
            raise SystemExit(f"[BLOCKED] no unique scalar {frame} {check} {quantity}")
        return float(r.value.iloc[0]), float(r.se.iloc[0])

    def tolerance(self, frame, statistic, check=None):
        r = self.power[(self.power.frame == frame) & (self.power.statistic == statistic)]
        if check is not None:
            r = r[r.check == check]
        if len(r) != 1:
            raise SystemExit(f"[BLOCKED] no unique declared tolerance for {frame} {statistic}")
        return r.iloc[0]


def fit_delta(d: Data, frame, check, series, target, allocation):
    """delta for one series against one target, its scored SE and every piece of the SE."""
    A = d.A[target]
    P = d.replicates(frame, check, series, "share")
    g = d.replicates(frame, check, series, f"group_share_{allocation}")
    fit = delta_fit(A, P[:, 0], g[:, 0])
    reps = [delta_fit(A, P[:, k], g[:, k])["delta"] for k in range(161)]
    se = delta_se(fit, reps)
    rep_se = float(np.sqrt(4 / 160 * np.square(np.array(reps[1:]) - reps[0]).sum()))
    return fit, se, rep_se


def dollars(d: Data, frame, check, series, allocation, delta):
    """The group's dollar change on the key's national total for a misstatement delta (national totals held)."""
    s, _ = d.scalar(frame, "group_key_share", f"{series}_{allocation}")
    total = KEYED[check][2]
    return total * d.hf * (implied_share(s, delta) - s), s


def keyed_scores(d: Data, rows: list, candidates: dict) -> None:
    stats = d.power[d.power.statistic.str.startswith("delta_")]
    for r in stats.itertuples():
        series = r.statistic[len("delta_"):].rsplit("_", 1)[0]
        allocation = r.statistic.rsplit("_", 1)[1]
        target = KEYED[r.check][1]
        fit, se, rep_se = fit_delta(d, r.frame, r.check, series, target, allocation)
        verdict = call(fit["delta"], se, r.tolerance)
        row = dict(frame=r.frame, check=r.check, statistic=r.statistic, role=r.role, target=target,
                   prediction=0.0, actual=fit["delta"], error=fit["delta"], se=se, se_hc3=fit["se_hc3"],
                   se_replicate=rep_se, tolerance=r.tolerance, call=verdict, end=END[allocation],
                   max_leverage=fit["max_leverage"])
        if series == KEYED[r.check][0]:  # dollars only for the key itself, not for a baseline series
            point, s = dollars(d, r.frame, r.check, series, allocation, fit["delta"])
            lo, _ = dollars(d, r.frame, r.check, series, allocation, fit["delta"] - Z * se)
            hi, _ = dollars(d, r.frame, r.check, series, allocation, fit["delta"] + Z * se)
            row.update(key_share=s, dollars_bn=point, dollars_lo_bn=lo, dollars_hi_bn=hi)
            if r.role == "verdict":
                candidates.setdefault(r.check, {})[allocation] = dict(delta=fit["delta"], call=verdict, key_share=s,
                                                                       dollars_bn=point)
        rows.append(row)
    for check, series, target, label in EXTRA:
        for frame in (PRIMARY, "asec2025_published"):
            for allocation in ALLOCATIONS:
                base = f"delta_{KEYED[check][0]}_{allocation}"
                tol = d.tolerance(frame, base).tolerance
                fit, se, rep_se = fit_delta(d, frame, check, series, target, allocation)
                row = dict(frame=frame, check=check, statistic=f"delta_{series}_{allocation}", role="secondary",
                           target=target, target_label=label, prediction=0.0, actual=fit["delta"],
                           error=fit["delta"], se=se, se_hc3=fit["se_hc3"], se_replicate=rep_se, tolerance=tol,
                           call=call(fit["delta"], se, tol), end=END[allocation], max_leverage=fit["max_leverage"])
                if series == KEYED[check][0]:
                    row["dollars_bn"], row["key_share"] = dollars(d, frame, check, series, allocation, fit["delta"])
                rows.append(row)


def dissimilarities(d: Data) -> list:
    out = []
    specs = {"1_refundable_credits": ["credits_ssn", "credits_raw", "population"],
             "2_ssi": ["ssi", "population", "age65plus"], "2_oasdi": ["social_security", "population", "age65plus"]}
    for check, series_list in specs.items():
        targets = [KEYED[check][1]] + [t for c, s, t, _ in EXTRA if c == check and s == series_list[0]]
        for frame in sorted(d.pred.frame.unique()):
            if d.pred[(d.pred.frame == frame) & (d.pred.check == check)].empty:
                continue
            for target in targets:
                A = d.A[target]
                for role, series in zip(("prediction", "baseline_1", "baseline_2"), series_list):
                    P = d.series(frame, check, series).share.to_numpy()
                    row = dict(frame=frame, check=check, target=target, role=role, series=series,
                               dissimilarity=dissimilarity(A, P))
                    if role == "prediction":
                        reps = d.replicates(frame, check, series, "share")
                        row["dissimilarity_se"] = float(np.sqrt(4 / 160 * np.square(
                            np.array([dissimilarity(A, reps[:, k]) for k in range(1, 161)])
                            - dissimilarity(A, reps[:, 0])).sum()))
                    out.append(row)
    return out


def state_errors(d: Data) -> list:
    out = []
    for check, (series, target, _, _) in KEYED.items():
        for frame in (PRIMARY, "asec2025_published"):
            s = d.series(frame, check, series)
            A = pd.Series(d.A[target], index=d.states)
            for st in BRIEF_STATES:
                r = A[st] / s.share[st] - 1
                se = s.share_se[st] / s.share[st]
                out.append(dict(frame=frame, check=check, state=st, target=target, actual_share=A[st],
                                predicted_share=s.share[st], predicted_share_se=s.share_se[st], error=r,
                                error_se=se, z=r / se, group_share_shared=s.group_share_shared[st],
                                group_share_personal=s.group_share_personal[st]))
    return out


def diagnostics(d: Data) -> list:
    out = []
    for check, (series, target, _, _) in KEYED.items():
        for frame in (PRIMARY, "asec2025_published"):
            s = d.series(frame, check, series)
            A, P = d.A[target], s.share.to_numpy()
            for allocation in ALLOCATIONS:
                g = s[f"group_share_{allocation}"].to_numpy()
                h = s[f"other_fb_share_{allocation}"].to_numpy()
                base = dict(frame=frame, check=check, series=series, target=target, allocation=allocation)
                for drop in ("CA", "TX"):
                    keep = np.array([st != drop for st in d.states])
                    fit = delta_fit(A[keep] / A[keep].sum(), P[keep] / P[keep].sum(), g[keep])
                    out.append(dict(base, diagnostic=f"without {drop}", delta=fit["delta"], se_hc3=fit["se_hc3"]))
                c = delta_fit_controlled(A, P, g, h)
                out.append(dict(base, diagnostic="other foreign-born control", delta=c["delta"], se_hc3=c["se_hc3"],
                                gamma=c["gamma"]))
            pi = s.pop_group_share.to_numpy()
            sl = slope_on(A, P, pi)
            out.append(dict(frame=frame, check=check, series=series, target=target, allocation="",
                            diagnostic="brief's slope on the group's share of residents", slope=sl["slope"],
                            slope_se_hc1=sl["se_hc1"]))
    return out


def relative(rows, frame, check, statistic, role, prediction, se, actual, tolerance, absolute=False, target=""):
    error = actual - prediction if absolute else actual / prediction - 1
    scored_se = se if absolute else se / prediction
    rows.append(dict(frame=frame, check=check, statistic=statistic, role=role, target=target, prediction=prediction,
                     actual=actual, error=error, se=scored_se, tolerance=tolerance,
                     call=call(error, scored_se, tolerance)))


def birth_scores(d: Data, rows: list, dist_rows: list) -> None:
    n = d.national
    births_all = n["wonder_births_all"]
    for frame in (PRIMARY, "asec2025_published"):
        for group, target in (("mex_origin", "wonder_births_mex_origin"), ("mexico_born", "wonder_births_mexico_born")):
            check = f"3_births_{group}"
            for kind, actual in (("share", n[target] / births_all), ("count", n[target])):
                decl = d.tolerance(frame, f"national_{kind}_relative", check)
                value, se = d.scalar(frame, f"3_births_{kind}", f"infants_{group}")
                relative(rows, frame, check, f"national_{kind}_relative", decl.role, value, se, actual,
                         decl.tolerance, target=target)
                for b in ("baseline_1", "baseline_2"):
                    q = f"{b}_{group}" + ("_births" if kind == "count" else "")
                    bv, _ = d.scalar(frame, f"3_births_{kind}", q)
                    rows.append(dict(frame=frame, check=check, statistic=f"national_{kind}_relative", role=b,
                                     target=target, prediction=bv, actual=actual, error=actual / bv - 1))
            A_state = pd.Series(d.A[target], index=d.states)
            A = np.array([A_state[CELLS[c]].sum() if c in CELLS else np.nan for c in list(CELLS) + ["rest"]])
            A[-1] = 1 - A[:-1].sum()
            cells = pd.read_csv(DER / "birth_cells.csv")
            cells = cells[(cells.frame == frame) & (cells.check == check)]
            for b in ("women_15_44", "group_population"):
                B = cells[cells.series == b].set_index("cell").loc[list(CELLS) + ["rest"], "r0"].to_numpy()
                dist_rows.append(dict(frame=frame, check=check, target=target, role=b, series=b,
                                      dissimilarity=dissimilarity(A, B)))
            for series in ("children_0_2", "infants"):
                decl = d.tolerance(frame, f"distribution_{series}", check)
                arr = cells[cells.series == series].set_index("cell").loc[list(CELLS) + ["rest"], COLS].to_numpy()
                cov = replicate_cov(arr)
                P = arr[:, 0]
                verdict = distribution_call(A, P, cov, decl.tolerance, decl.sampling_se)
                rows.append(dict(frame=frame, check=check, statistic=f"distribution_{series}", role=decl.role,
                                 target=target, actual=dissimilarity(A, P), error=dissimilarity(A, P),
                                 se=decl.sampling_se, tolerance=decl.tolerance, call=verdict, wald=wald(A, P, cov)))
                dist_rows.append(dict(frame=frame, check=check, target=target, role=f"prediction_{series}",
                                      series=series, dissimilarity=dissimilarity(A, P),
                                      cells_actual=json.dumps({c: round(float(a), 5) for c, a in
                                                               zip(list(CELLS) + ["rest"], A)}),
                                      cells_predicted=json.dumps({c: round(float(p), 5) for c, p in
                                                                  zip(list(CELLS) + ["rest"], P)})))
        # Medicaid-paid births, Mexican-origin mothers (declared) and Mexico-born mothers (reported)
        for quantity, kind, actual in (
                ("women_15_44_covered_union", "group_share", n["wonder_medicaid_group_share_mex_origin"]),
                ("mothers_mex_origin", "group_share", n["wonder_medicaid_group_share_mex_origin"]),
                ("infants_mex_origin", "group_share", n["wonder_medicaid_group_share_mex_origin"]),
                ("women_15_44_union", "ratio", n["wonder_medicaid_ratio_mex_origin"]),
                ("mothers_mex_origin", "ratio", n["wonder_medicaid_ratio_mex_origin"]),
                ("infants_mex_origin", "ratio", n["wonder_medicaid_ratio_mex_origin"]),
                ("women_15_44_covered_2024_union", "level", n["wonder_medicaid_share_mex_origin"]),
                ("mothers_covered_2024_mex_origin", "level", n["wonder_medicaid_share_mex_origin"]),
                ("infants_covered_now_mex_origin", "level", n["wonder_medicaid_share_mex_origin"])):
            check = {"group_share": "3_medicaid_births_group_share", "ratio": "3_medicaid_paid_ratio",
                     "level": "3_medicaid_paid_level"}[kind]
            decl = d.tolerance(frame, quantity, check)
            value, se = d.scalar(frame, check, quantity)
            relative(rows, frame, check, quantity, decl.role, value, se, actual, decl.tolerance,
                     absolute=kind == "level", target=f"wonder_medicaid_{kind}_mex_origin")
        for check, quantity, b in (("3_medicaid_births_group_share", "baseline_1_union_share_women_15_44", "baseline_1"),
                                   ("3_medicaid_births_group_share", "baseline_2_union_share_medicaid_covered",
                                    "baseline_2"),
                                   ("3_medicaid_paid_ratio", "baseline_2_union_all_ages", "baseline_2")):
            bv, _ = d.scalar(frame, check, quantity)
            actual = n["wonder_medicaid_group_share_mex_origin" if "group_share" in check
                       else "wonder_medicaid_ratio_mex_origin"]
            rows.append(dict(frame=frame, check=check, statistic=quantity, role=b, prediction=bv, actual=actual,
                             error=actual / bv - 1))
        rows.append(dict(frame=frame, check="3_medicaid_paid_ratio", statistic="baseline_1_no_difference",
                         role="baseline_1", prediction=1.0, actual=n["wonder_medicaid_ratio_mex_origin"],
                         error=n["wonder_medicaid_ratio_mex_origin"] - 1))
        for check, quantity, actual in (
                ("3_medicaid_births_group_share", "women_15_44_covered_mexico_born",
                 n["wonder_medicaid_group_share_mexico_born"]),
                ("3_medicaid_births_group_share", "infants_mexico_born", n["wonder_medicaid_group_share_mexico_born"]),
                ("3_medicaid_paid_ratio", "women_15_44_mexico_born", n["wonder_medicaid_ratio_mexico_born"]),
                ("3_medicaid_paid_ratio", "infants_mexico_born", n["wonder_medicaid_ratio_mexico_born"]),
                ("3_medicaid_paid_level", "infants_covered_now_mexico_born", n["wonder_medicaid_share_mexico_born"])):
            value, se = d.scalar(frame, check, quantity)
            absolute = check == "3_medicaid_paid_level"
            rows.append(dict(frame=frame, check=check, statistic=quantity, role="reported (no declared call)",
                             prediction=value, actual=actual,
                             error=actual - value if absolute else actual / value - 1,
                             se=se if absolute else se / value))


def check_calls(scores: pd.DataFrame) -> list:
    """PREDICTIONS.md: a delta check misses when either end misses, hits when both hit, else has no power; checks
    with several verdict statistics report each."""
    out = []
    v = scores[(scores.frame == PRIMARY) & (scores.role == "verdict")]
    for check, g in v.groupby("check", sort=False):
        calls = g.set_index("statistic").call.to_dict()
        if check in KEYED:
            combined = "miss" if "miss" in calls.values() else "hit" if set(calls.values()) == {"hit"} else "no power"
        else:
            combined = "; ".join(f"{k}: {c}" for k, c in calls.items())
        out.append(dict(check=check, call=combined, statistics=json.dumps(calls)))
    return out


def main() -> None:
    d = Data()
    rows, dist_rows, candidates = [], [], {}
    keyed_scores(d, rows, candidates)
    birth_scores(d, rows, dist_rows)
    scores = pd.DataFrame(rows)
    write = lambda frame, name: frame.to_csv(DER / name, index=False, float_format="%.10g", lineterminator="\n")
    write(scores, "scores.csv")
    calls = pd.DataFrame(check_calls(scores))
    write(calls, "check_calls.csv")
    write(pd.DataFrame(dissimilarities(d) + dist_rows), "dissimilarity.csv")
    write(pd.DataFrame(state_errors(d)), "state_errors.csv")
    write(pd.DataFrame(diagnostics(d)), "diagnostics.csv")
    shifts = {}
    for check, ends in candidates.items():
        if not any(e["call"] == "miss" for e in ends.values()):
            continue
        shifts[check] = {"lines": {line: {"key": key, "fraction": frac} for line, (key, frac) in KEYED[check][3].items()},
                         "by_allocation": {a: ends[a]["dollars_bn"] for a in ALLOCATIONS},
                         "delta": {a: ends[a]["delta"] for a in ALLOCATIONS}}
    (DER / "candidate_shifts.json").write_text(json.dumps(shifts, indent=1, sort_keys=True) + "\n")
    for r in calls.itertuples():
        print(f"  ✓ {r.check}: {r.call}")


if __name__ == "__main__":
    main()
