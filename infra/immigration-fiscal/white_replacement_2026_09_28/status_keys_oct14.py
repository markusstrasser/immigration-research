"""Additive, record-level status arm; explicitly not the full adopted row-13 stack.

Use build(rekey_sept29) after setup(), then receipt_amount(sc, lid, national_bn).
The source_proxy arm separates the change from PEARNVAL to the account's wage and
self-payroll proxies from the status rule itself. rules_only additionally applies
the state-aware unauthorized flag and origin-specific central on-books fractions.
Income tax holds the existing IRS/CBO raked personal carrier key and applies the
source status fraction before national normalization. The adopted row-13 net
method is a ratio of group shares, not a closed additive person vector; requesting
it stops. No summary multiplier is used as a record substitute.
"""
from __future__ import annotations

import csv
import json
import resource
import time
import zipfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
LINE_KEYS = {
    "federal_income_tax": "fit_case", "state_local_income_tax": "sit_case",
    "other_personal_tax": "sit_case", "employee_oasdi": "oasdi",
    "employer_oasdi": "oasdi", "employee_hi": "hi", "employer_hi": "hi",
    "self_employment_oasdi_hi": "self_payroll",
}
RULES = ("raw", "source_proxy", "rules_only")


def require(ok, message):
    if not ok:
        raise SystemExit(f"[BLOCKED] status arm: {message}")


def normalized(vectors, weights):
    """Person key densities whose civilian weighted integral is one."""
    out = {}
    for k, v in vectors.items():
        v = np.asarray(v, float)
        require(v.shape == weights.shape and np.isfinite(v).all() and (v >= 0).all(),
                f"invalid record vector {k}")
        total = float(weights @ v)
        require(total > 0, f"empty national vector {k}")
        out[k] = v / total
        require(abs(float(weights @ out[k]) - 1) <= 1e-12, f"national key closure {k}")
    return out


@dataclass
class StatusKeys:
    vectors: dict
    weights: np.ndarray
    unauthorized: np.ndarray
    on_books: np.ndarray
    source_info: dict

    def shares(self, sc, rule="rules_only"):
        require(rule in RULES, f"unsupported rule {rule!r}; row13 ratio lacks an additive definition")
        cw = np.asarray(sc["cps_w"], float)
        require(cw.shape == self.weights.shape and np.isfinite(cw).all() and (cw >= 0).all(),
                "scenario weights do not align")
        require(abs(float(cw.sum()) - sc["population"]) <= 1e-6,
                "scenario population is not its record-weight sum")
        return {k: float(cw @ v) for k, v in self.vectors[rule].items()}

    def receipt_amount(self, sc, lid, national_bn, rule="rules_only"):
        if lid not in LINE_KEYS:
            return None
        shares = self.shares(sc, rule)
        return float(national_bn) * shares[LINE_KEYS[lid]]

    def closure(self, national_lines):
        rows = []
        for rule, vectors in self.vectors.items():
            for lid, key in LINE_KEYS.items():
                national = national_lines[lid]
                got = float(self.weights @ vectors[key]) * national
                require(abs(got - national) <= 1e-6, f"{rule} national receipts do not close: {lid}")
                rows.append(dict(rule=rule, line=lid, national_bn=national,
                                 all_residents_bn=got, error_bn=got - national))
        return rows


def align_source(d, ids, rough):
    """Join by actual person IDs, preserving the rough frame's original file order."""
    require(not ids.duplicated(["PH_SEQ", "PPPOS"]).any(), "duplicate raw person IDs")
    require(not d.duplicated(["PH_SEQ", "PPPOS"]).any(), "duplicate source person IDs")
    out = ids.merge(d, on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one", indicator=True)
    require(len(out) == len(rough) and out._merge.eq("both").all(), "incomplete source person join")
    for col in ("PH_SEQ", "SPM_ID", "A_AGE", "PRCITSHP", "PENATVTY", "FEDTAX_AC", "STATETAX_A"):
        require(np.array_equal(out[col].to_numpy(), rough[col].to_numpy()), f"source mismatch {col}")
    return out.drop(columns="_merge")


def engine_accrual_rates(m, end):
    """Exact engine liabilities per engine payer dollar; includes post-pension edits.

    Applying these to new tax vectors is a coupled per-tax-dollar arm, not an
    eligibility rerun. Holding benefits fixed instead requires preserving the
    original liability numerator while recalibrating its new tax denominator.
    """
    cash = {x["side"] + "|" + x["id"]: x["amount_bn"]
            for x in m.DUMP["cash"][end]["lines"] if x["side"] != "scalar"}
    accrual = {x["side"] + "|" + x["id"]: x["amount_bn"]
               for x in m.DUMP["accrual"][end]["lines"] if x["side"] != "scalar"}
    se = cash["receipts|self_employment_oasdi_hi"]
    oasdi = cash["receipts|employee_oasdi"] + cash["receipts|employer_oasdi"] + m.SE_SHARE * se
    hi = cash["receipts|employee_hi"] + cash["receipts|employer_hi"] + (1 - m.SE_SHARE) * se
    part_a = accrual["spending|medicare"] - (1 - m.PART_A_SHARE) * cash["spending|medicare"]
    require(oasdi > 0 and hi > 0 and cash["spending|social_security"] > 0, "engine pension denominator empty")
    return dict(net=accrual["spending|social_security"] / oasdi, part_a=part_a / hi,
                per_rel_ben=(cash["receipts|federal_income_tax"] - accrual["receipts|federal_income_tax"])
                / cash["spending|social_security"] / m.REL_UNION)


def build(m):
    """Build on the current row-4 national frame, without modifying it or upstream caches."""
    require(m.CASE == "oct14" and m.TAX_ALLOC == "personal", "requires oct14 personal case keys")
    c, cs, lane = m.L.c, m.L.cs, m.L
    require((c.CACHE / "asec25_lane.parquet").exists(), "missing existing authoritative source frame")
    # This computation uses point record vectors, not the 160 replicate columns.
    # Keep every other source field so the source's flag/key APIs remain exact.
    import pyarrow.parquet as pq
    path = c.CACHE / "asec25_lane.parquet"
    columns = [col for col in pq.read_schema(path).names if col not in c.REPS[1:]]
    d = pd.read_parquet(path, columns=columns)
    with zipfile.ZipFile(c.CPS_ZIP) as z:
        ids = pd.read_csv(z.open("pppub25.csv"), usecols=["PH_SEQ", "PPPOS"])
    d = align_source(d, ids, m.R.d)
    civ, union = c.masks(d)
    require(np.array_equal(civ, m.R.civ) and np.array_equal(union, m.R.MASK["mex"] & civ),
            "source and comparator population masks differ")
    s, hh = cs.status_inputs()
    unauthorized = lane.state_aware_flag(s, hh, d, lane.STATUS_BLIND_2024)
    fractions, _ = lane.share_configs(d)
    on_books = fractions[("origin", "central")]
    factor = np.where(unauthorized, on_books, 1.0)
    index = c.spm_index(d)
    raw_source = c.receipt_vectors(d)
    adjusted, _ = cs.status_vectors(d, unauthorized, on_books, index)
    adjusted = adjusted["personal"]
    for key in cs.SCALED:
        require(np.array_equal(adjusted[key], raw_source[key] * factor),
                f"source rule does not reproduce {key}")
    w = np.asarray(m.R.w, float).copy()
    raw = {"fit_case": m.R.K["fit_case_personal"], "sit_case": m.R.K["sit_case_personal"],
           "oasdi": m.R.K["oasdi"], "hi": m.R.K["hi"], "self_payroll": m.R.K["oasdi"]}
    source = {"fit_case": raw["fit_case"], "sit_case": raw["sit_case"],
              "oasdi": raw_source["wage_oasdi"], "hi": raw_source["wage"],
              "self_payroll": raw_source["self_payroll"]}
    rules = {"fit_case": source["fit_case"] * factor, "sit_case": adjusted["state_liability"],
             "oasdi": adjusted["wage_oasdi"], "hi": adjusted["wage"],
             "self_payroll": adjusted["self_payroll"]}
    vectors = {name: normalized(v, w) for name, v in zip(RULES, (raw, source, rules))}
    # Positive control: every old raw share is the existing scenario's own key.
    for sc in (m.R.scenario("mex"), m.R.scenario("blk", scaled=False), m.R.scenario("w3")):
        for key, old in (("fit_case", "fit_case"), ("sit_case", "sit_case"),
                         ("oasdi", "oasdi"), ("hi", "hi"), ("self_payroll", "oasdi")):
            require(abs(float(sc["cps_w"] @ vectors["raw"][key]) - sc["share"][old]) <= 1e-12,
                    f"raw positive control {sc['name']} {key}")
    info = dict(frame="cps_imputation_keys_2026_09_23/_cache/asec25_lane.parquet",
                status="combine_onbooks_lane.state_aware_flag(STATUS_BLIND_2024)",
                rules="combine_status.status_vectors; origin central share_configs",
                allocation="personal", row13="not applied; nonlinear ratio has no closed additive definition",
                income_tax="existing IRS/CBO-raked carrier key times source status factor, normalized on row4",
                payroll="source wage_oasdi / wage / self_payroll vectors, separate SE key",
                civilian_population=float(w.sum()), union_population=float(w[union].sum()),
                unauthorized_population=float(w[unauthorized].sum()))
    info["source_sha256"] = {str(p.relative_to(HERE.parent)): c.sha(p) for p in (
        c.CACHE / "asec25_lane.parquet", Path(c.__file__), Path(cs.__file__), Path(lane.__file__),
        lane.ONBOOKS / "onbooks_split.csv", lane.ONBOOKS / "onbooks_inputs.json")}
    return StatusKeys(vectors, w, unauthorized, on_books, info)


def main():
    import rekey_sept29 as m
    started = time.perf_counter()
    m.use_case("oct14")
    m.setup()
    m.stop_if_failed()
    status = build(m)
    nationals = {x["id"]: x["national_bn"] for x in m.DUMP["cash"]["low"]["lines"] if x["side"] == "receipts"}
    closure = status.closure(nationals)
    rows = []
    white = m.R.scenario("w3")
    lineage_population = m.META["lineage"]["counts"]["lineage_population"]
    scale = lineage_population / white["population"]
    white_lineage = {**white, "cps_w": white["cps_w"] * scale, "population": lineage_population}
    for group, sc in (("identified_union", m.R.scenario("mex")),
                      ("nh_black_own_population", m.R.scenario("blk", scaled=False)),
                      ("third_plus_nh_white_identified_union_population", white),
                      ("third_plus_nh_white_lineage_population", white_lineage)):
        for rule in RULES:
            for end in m.ENDS:
                for ln in m.DUMP["cash"][end]["lines"]:
                    if ln["side"] != "receipts" or ln["id"] not in LINE_KEYS:
                        continue
                    value = status.receipt_amount(sc, ln["id"], ln["national_bn"], rule)
                    raw = status.receipt_amount(sc, ln["id"], ln["national_bn"], "raw")
                    rows.append(dict(group=group, population=sc["population"], rule=rule, end=end,
                                     line=ln["id"], receipts_bn=value, change_from_raw_bn=value-raw,
                                     engine_union_bn=ln["amount_bn"] if sc["name"] == "mex" else ""))
    # This stored headline-scope positive control is distinct from the eight
    # identified-union receipt lines above: full lineage, after the pension rule.
    stored = pd.read_csv(m.BLACK_LANE / "derived/rekey_by_program_oct14.csv")
    require({"cost_bn", "program", "basis", "group"} <= set(stored), "stored by-program control schema changed")
    controls = []
    for basis in ("accrual", "cash"):
        for bucket in ("income taxes", "payroll taxes and Medicare premiums"):
            sub = stored.query("basis == @basis and program == @bucket")
            engine = sub[sub.group.eq("mexican_origin_engine")].iloc[0]
            rough = sub[sub.group.eq("mexican_origin_rough")].iloc[0]
            controls.append(dict(basis=basis, bucket=bucket, source="black_comparator_rough_2026_09_28/derived/rekey_by_program_oct14.csv",
                                 rough_less_engine_bn=float(engine.cost_bn)-float(rough.cost_bn)))
    for filename, records in (("status_receipts_oct14.csv", rows), ("status_closure_oct14.csv", closure),
                              ("status_stored_control_oct14.csv", controls)):
        with (HERE / "derived" / filename).open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(records[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(records)
    # Timing is printed, not fingerprinted into the deterministic provenance output.
    (HERE / "derived/status_method_oct14.json").write_text(json.dumps(status.source_info, indent=2, sort_keys=True)+"\n")
    print(f"[PASS] raw positive controls and {len(closure)} national closure gates; "
          f"elapsed={time.perf_counter()-started:.3f}s maxrss={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")


if __name__ == "__main__":
    main()
