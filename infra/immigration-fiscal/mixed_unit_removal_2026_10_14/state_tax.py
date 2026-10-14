#!/usr/bin/env python3
"""M2: local 2024 TAXSIM re-filing, calibrated to CPS positive state liabilities.

This is a conditional sensitivity, not an exact tax-return reconstruction. Source
tax rules are evaluated by the pinned NBER executable. Unobserved deductions,
retirement-income taxability and QBI classifications remain unidentified.
No CPS records are submitted to a remote service.
"""
from __future__ import annotations

import hashlib
import io
import json
import subprocess
import sys
from pathlib import Path
from urllib.request import urlopen

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
BINARY = LANE / "_cache/state_taxsimtest_osx"
PINS = LANE / "inputs/state_pins.json"
SOURCES = {
    "_cache/state_taxsimtest_osx": "https://taxsim.nber.org/stata/taxsimtest/osx",
    "inputs/state_tax_parameters.xlsx": "https://www2.census.gov/library/working-papers/2026/demo/Federal_and_State_Tax_Parameter_Workbook_TY2025.xlsx",
    "inputs/state_taxsim_documentation.html": "https://taxsim.nber.org/taxsimtest/",
    "inputs/state_workbook_documentation.pdf": "https://www2.census.gov/library/working-papers/2026/demo/Federal_and_State_Tax_Parameter_Workbook_Documentation_TY2025.pdf",
}


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def acquire_sources():
    """Explicit acquisition, never an implicit runtime download or pin replacement."""
    if PINS.exists():
        raise RuntimeError("[BLOCKED] source pins already exist; verify instead of replacing")
    pins = {}
    for relative, url in SOURCES.items():
        path = LANE / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            with urlopen(url, timeout=60) as response:
                path.write_bytes(response.read())
        pins[relative] = {"url": url, "sha256": sha(path)}
    BINARY.chmod(BINARY.stat().st_mode | 0o100)
    # Preserve the 2024 parameters and their exact workbook cell/source labels.
    import openpyxl
    workbook = openpyxl.load_workbook(LANE / "inputs/state_tax_parameters.xlsx", data_only=True)
    parsed = {}
    for sheet in workbook:
        headers = next(((i, row) for i, row in enumerate(sheet.values, 1)
                        if any(str(x).startswith("2024 Value") for x in row)), None)
        if headers is None:
            continue
        index, columns = headers
        col = next(i for i, x in enumerate(columns) if str(x).startswith("2024 Value"))
        entries = []
        for row in sheet.iter_rows(min_row=index + 1):
            if row[0].value is not None and row[col].value is not None:
                entries.append({"parameter": str(row[0].value), "description": str(row[1].value),
                                "value": row[col].value, "cell": row[col].coordinate,
                                "source": str(row[col + 1].value)})
        parsed[sheet.title] = entries
    if "CA" not in parsed or "Federal" not in parsed:
        raise RuntimeError("[BLOCKED] workbook 2024 columns missing")
    parsed_path = LANE / "inputs/state_parameters_2024.json"
    parsed_path.write_text(json.dumps(parsed, indent=2) + "\n")
    pins["inputs/state_parameters_2024.json"] = {
        "generated_from": "inputs/state_tax_parameters.xlsx", "sha256": sha(parsed_path)}
    PINS.write_text(json.dumps(pins, indent=2) + "\n")


def verify_sources():
    pins = json.loads(PINS.read_text())
    for relative, pin in pins.items():
        path = LANE / relative
        if not path.exists() or sha(path) != pin["sha256"]:
            raise RuntimeError(f"[BLOCKED] missing or stale state source: {relative}")
    return pins


def run_taxsim(frame):
    """Return the pinned local kernel's full output, including fiitax/v25/actc.

    fiitax + v25 + actc is income tax before these two refundable credits.
    `siitax` is after state credits; `staxbc` is before state credits. All
    identifiers, row counts, ordering, finite results and process status gate.
    """
    verify_sources()
    if frame.empty:
        return pd.DataFrame(columns=["taxsimid", "siitax", "fiitax", "v25", "actc", "staxbc"])
    f = frame.copy()
    f["taxsimid"] = np.arange(1, len(f) + 1)
    f["idtl"] = 2
    if not np.isfinite(f.to_numpy(float)).all():
        raise RuntimeError("[BLOCKED] nonfinite TAXSIM input")
    try:
        result = subprocess.run([str(BINARY)], input=f.to_csv(index=False, lineterminator="\n"),
                                capture_output=True, text=True, timeout=120, check=False)
    except OSError as exc:
        raise RuntimeError("[BLOCKED] pinned local TAXSIM executable cannot run on this host") from exc
    if result.returncode:
        raise RuntimeError(f"[BLOCKED] local TAXSIM exit {result.returncode}: {result.stdout[:1800]} {result.stderr[:600]}")
    try:
        out = pd.read_csv(io.StringIO(result.stdout))
    except (pd.errors.ParserError, pd.errors.EmptyDataError) as exc:
        raise RuntimeError("[BLOCKED] malformed local TAXSIM output") from exc
    required = ["taxsimid", "siitax", "fiitax", "v25", "actc", "staxbc"]
    if not set(required) <= set(out) or len(out) != len(f):
        raise RuntimeError("[BLOCKED] incomplete local TAXSIM output")
    if not np.array_equal(out.taxsimid.to_numpy(), f.taxsimid.to_numpy()):
        raise RuntimeError("[BLOCKED] local TAXSIM output IDs/order differ")
    if not np.isfinite(out[required].to_numpy(float)).all():
        raise RuntimeError("[BLOCKED] nonfinite local TAXSIM output")
    return out


def taxsim_frame(d, R, P=None, *, own=None, label="all", dep_counts=None):
    """Build actual joint/individual or own-survivor inputs without shared residual.

    own: person row positions (one per R row), makes every row unmarried.
    dep_counts: optional arrays n/k13/k17/keitc to override linked dependents.
    Unknown itemized deductions, rents/property tax and childcare are zero.
    Self-employment is mapped to non-QBI psemp/ssemp; all dividends qualified,
    all CAP_VAL long-term. These are explicit modeling assumptions.
    """
    h = R.row.to_numpy(int) if own is None else np.asarray(own, int)
    n = len(h)
    has_s = (R.spouse.to_numpy(int) >= 0) if own is None else np.zeros(n, bool)
    s = np.maximum(R.spouse.to_numpy(int), 0) if own is None else np.zeros(n, int)
    joint = R.status.eq("joint").to_numpy() & has_s if own is None else np.zeros(n, bool)
    val = lambda column: d[column].to_numpy(float)  # noqa: E731
    pick = lambda column: val(column)[h] + np.where(has_s, val(column)[s], 0.0)  # noqa: E731
    k = ({"n": R[f"n_{label}"].to_numpy(), "k13": R[f"k13_{label}"].to_numpy(),
          "k17": R[f"k17_{label}"].to_numpy(), "keitc": R[f"keitc_{label}"].to_numpy()}
         if dep_counts is None else dep_counts)
    frame = pd.DataFrame({
        "year": np.full(n, 2024), "mstat": np.where(joint, 2, 1),
        "statefip": val("GESTFIPS")[h], "page": val("A_AGE")[h],
        "sage": np.where(has_s, val("A_AGE")[s], 0),
        "depx": k["n"], "dep13": k["k13"], "dep17": k["k17"], "dep18": k["keitc"],
        "pwages": np.maximum(val("WSAL_VAL")[h], 0),
        "swages": np.where(has_s, np.maximum(val("WSAL_VAL")[s], 0), 0),
        "psemp": (val("SEMP_VAL") + val("FRSE_VAL"))[h],
        "ssemp": np.where(has_s, (val("SEMP_VAL") + val("FRSE_VAL"))[s], 0),
        "dividends": pick("DIV_VAL"), "intrec": pick("INT_VAL"), "ltcg": pick("CAP_VAL"),
        "otherprop": pick("RNT_VAL"), "pensions": pick("PNSN_VAL") + pick("ANN_VAL"),
        "gssi": pick("SS_VAL"), "pui": val("UC_VAL")[h],
        "sui": np.where(has_s, val("UC_VAL")[s], 0),
    })
    if own is None:
        frame.loc[R.depfiler.to_numpy(bool), "mstat"] = 8
    return frame


def sdr(x):
    return float(np.sqrt(4 / 160 * np.square(np.asarray(x)[1:] - x[0]).sum()))


def compute(d, R, P, base, W, union, gen, flag, onbooks, model, civ=None,
            refiling=None):
    """Return M2's 3x161 net-cost changes, survivor fields and JSON-safe audit.

    Default scope: mixed civilian joint returns only. A shared refiling registry
    also permits conditional state-credit changes on unchanged non-member
    returns, retaining their own Census residual. Positive liabilities retain
    the case's floor at zero; state refund spending is outside M2. Calibration is
    by original-return state and replicate to CPS positive liability, before the
    adopted status/on-books rule. The new survivor gets their own status factor.
    Original and surviving amounts keep their respective person's weights.

    Optional refiling dict supplies full-return-aligned `own` and dep_counts,
    and optionally `R` (surviving return registry aligned to the old rows).
    It may reassign surviving dependents under the shared registry's policy.
    """
    if civ is None:
        civ = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    civ = np.asarray(civ, bool)
    h, sp = R.row.to_numpy(int), R.spouse.to_numpy(int)
    valid_sp = np.maximum(sp, 0)
    mh, ms = union[h], union[valid_sp]
    mixed = (sp >= 0) & (mh != ms) & civ[h] & civ[valid_sp] & R.status.eq("joint").to_numpy()
    own = np.where(mh, valid_sp, h)
    if refiling is not None:
        own = np.asarray(refiling["own"], int)
        if own.shape != h.shape:
            raise RuntimeError("[BLOCKED] M2 refiling rows are not aligned to original returns")
    if np.any(own[mixed] < 0) or np.any(union[own[mixed]]):
        raise RuntimeError("[BLOCKED] M2 survivor is a member")
    member_gen = np.where(mh, gen[h], gen[valid_sp])
    if np.any(member_gen[mixed] < 0):
        raise RuntimeError("[BLOCKED] M2 mixed joint return has no member generation")
    actual_frame = (refiling["before_input"].copy() if refiling is not None and "before_input" in refiling
                    else taxsim_frame(d, R, P))
    if len(actual_frame) != len(R):
        raise RuntimeError("[BLOCKED] M2 canonical before input is not return-aligned")
    actual_output = run_taxsim(actual_frame)
    dep_counts = None if refiling is None else refiling.get("dep_counts")
    survivor_frame = taxsim_frame(d, R, P, own=np.maximum(own, 0), label="non", dep_counts=dep_counts)
    # Original two-nonmember joint returns stay joint when their dependents move.
    # A dependent filer remains a dependent filer; survivor ownership alone does
    # not turn it into a head of household.
    same = (own == h) & ~mixed & ~mh & civ[h]
    if refiling is not None and "R" in refiling:
        survivor_frame = taxsim_frame(d, refiling["R"], P)
    else:
        survivor_frame.loc[same] = actual_frame.loc[same]
        if dep_counts is not None:
            for column, key in [("depx", "n"), ("dep13", "k13"), ("dep17", "k17"), ("dep18", "keitc")]:
                survivor_frame.loc[same, column] = np.asarray(dep_counts[key])[same]
    if refiling is not None and "after_input" in refiling:
        survivor_frame = refiling["after_input"].copy()
        if len(survivor_frame) != len(R):
            raise RuntimeError("[BLOCKED] M2 canonical after input is not return-aligned")
    scope = mixed | (same if refiling is not None else False)
    survivor_output = run_taxsim(survivor_frame.loc[scope].reset_index(drop=True))
    # Swapping the head/spouse labels must leave the survivor's physical inputs
    # and their evaluated liability unchanged; the personal baseline is separate.
    swapped = R.copy()
    swapped["row"], swapped["spouse"] = valid_sp, h
    own_swap = np.where(ms, h, valid_sp)
    swap_frame = taxsim_frame(d, swapped, P, own=own_swap, label="non", dep_counts=dep_counts)
    for column in set(survivor_frame) - set(swap_frame):
        # Care spending and any other explicit shared-driver input follow the
        # physical surviving return, irrespective of original head/spouse label.
        swap_frame[column] = survivor_frame[column]
    swap_frame = swap_frame[list(survivor_frame)]
    symmetry = float(np.abs(swap_frame.loc[mixed].to_numpy(float)
                            - survivor_frame.loc[mixed].to_numpy(float)).max()) if mixed.any() else 0.0
    if symmetry > 1e-9:
        raise RuntimeError(f"[BLOCKED] M2 survivor head/spouse symmetry: {symmetry}")
    source_signed = d.STATETAX_A.to_numpy(float)
    source = np.maximum(source_signed, 0)
    # The original returns must span the national positive-liability key.
    carrier = np.zeros(len(d), bool)
    carrier[h] = True
    if np.any(source[civ & ~carrier] > 0):
        raise RuntimeError("[BLOCKED] state taxes occur outside the reused return frame")
    positive = np.maximum(actual_output.siitax.to_numpy(float), 0)
    states = d.GESTFIPS.to_numpy(int)
    state_rows = []
    ratios = {}
    closure = 0.0
    for state in np.unique(states):
        rows = (states[h] == state) & civ[h]
        cps = source[h[rows]] @ W[h[rows]]
        sim = positive[rows] @ W[h[rows]]
        if np.any((sim <= 0) & (cps > 0)):
            raise RuntimeError(f"[BLOCKED] state {state} has CPS positive taxes but no simulated base")
        factor = np.divide(cps, sim, out=np.zeros_like(cps), where=sim > 0)
        # Zero / zero is a structural no-positive-liability stratum, not fallback.
        ratios[state] = factor
        closure = max(closure, float(np.abs(sim * factor - cps).max() / 1e9))
        err = np.abs(positive[rows] - source[h[rows]])
        state_rows.append({"fips": int(state), "returns": int(rows.sum()),
                           "cps_positive_bn": float(cps[0] / 1e9),
                           "taxsim_positive_bn": float(sim[0] / 1e9),
                           "calibration_factor": float(factor[0]),
                           "structural_zero": bool((cps == 0).all() and (sim == 0).all()),
                           "raw_mae_usd": float(err @ W[h[rows], 0] / W[h[rows], 0].sum())})
    if closure > 1e-6:
        raise RuntimeError(f"[BLOCKED] M2 state calibration closure {closure}bn")
    central = onbooks["central"] if isinstance(onbooks, dict) else np.asarray(onbooks)
    f = np.where(flag, central, 1.0)
    original_nonmember = np.where(~mh[scope], source[h[scope]] * f[h[scope]], 0)
    remaining_positive = np.maximum(survivor_output.siitax.to_numpy(float), 0)
    original_weighted = original_nonmember[:, None] * W[h[scope]]
    surviving_weighted = np.empty_like(original_weighted)
    remaining_by_return = np.zeros(len(R))
    remaining_live = (own >= 0) & (same | mixed)
    remaining_by_return[same] = source[h[same]] * f[h[same]]
    for i, row in enumerate(np.flatnonzero(scope)):
        ratio = ratios[states[own[row]]]
        if same[row]:
            change = survivor_output.siitax.iloc[i] - actual_output.siitax.iloc[row]
            liability = np.maximum(source_signed[h[row]] + change * ratio, 0)
        else:
            liability = remaining_positive[i] * ratio
        ruled = liability * f[own[row]]
        remaining_by_return[row] = ruled[0]
        surviving_weighted[i] = ruled * W[own[row]]
    difference = surviving_weighted - original_weighted
    national_key = (source[civ] * f[civ]) @ W[civ]
    line = next(x for x in model["receipts"]["lines"] if x["id"] == "state_local_income_tax")
    if np.any(national_key <= 0):
        raise RuntimeError("[BLOCKED] M2 national state-tax key nonpositive")
    conversion = line["national_bn"] / national_key
    # Reassigned children on a continuing return follow the departing member
    # dependents, counted equally. New credits transferred from another return
    # need the shared registry's owner matrix to preserve generation accounting.
    owners = np.stack([(member_gen == g).astype(float) for g in range(3)])
    if refiling is not None and "owner" in refiling:
        registry_owner = np.asarray(refiling["owner"], float)
        if registry_owner.shape == (len(R), 3):
            registry_owner = registry_owner.T
        if registry_owner.shape != owners.shape:
            raise RuntimeError("[BLOCKED] M2 refiling generation owner shape")
        owners[:, same] = registry_owner[:, same]
    elif refiling is not None and same.any():
        count_mem = R.n_mem.to_numpy(float)
        owners[:, same] = np.stack([R[f"g{g}_mem"].to_numpy(float)[same] for g in range(3)]) / np.maximum(count_mem[same], 1)
    changed = np.any(np.abs(difference) > 1e-9, axis=1)
    if np.any(np.abs(owners[:, scope][:, changed].sum(axis=0) - 1) > 1e-9):
        raise RuntimeError("[BLOCKED] M2 changed return needs shared generation ownership")
    account = np.stack([(difference * owners[g, scope, None]).sum(axis=0) * conversion for g in range(3)])
    direct = difference.sum(axis=0) * conversion
    raw_surviving = remaining_positive[:, None] * f[own[scope], None] * W[own[scope]]
    raw_direct = (raw_surviving - original_weighted).sum(axis=0) * conversion
    closure_gen = float(np.abs(account.sum(axis=0) - direct).max())
    if closure_gen > 1e-6:
        raise RuntimeError("[BLOCKED] M2 generations do not close")
    terms = []
    for label, m in [("nonmember_head", ~mh[scope]), ("member_head", mh[scope])]:
        x = difference[m].sum(axis=0) * conversion
        terms.append({"component": "M2", "carrier": label, "account_bn": float(x[0]), "se_bn": sdr(x),
                      "sample_returns": int(m.sum())})
    details = {"status": "[DEGRADED] conditional calibrated local TAXSIM sensitivity; not adoptable",
               "recommended_adopt": False,
               "scope": "identified union, mixed civilian joint returns" + (" plus continuing returns' state credits" if refiling is not None else " only"),
               "source_pins": json.loads(PINS.read_text()), "source_year": 2024,
               "returns": int(mixed.sum()), "additional_continuing_returns": int((scope & same).sum()),
               "national_line_bn": line["national_bn"],
               "national_ruled_cps_key_bn": float(national_key[0] / 1e9),
               "raw_surviving_signed_cps_bn": float(survivor_output.siitax.to_numpy(float) @ W[own[scope], 0] / 1e9),
               "surviving_positive_calibrated_cps_bn": float(surviving_weighted[:, 0].sum() / 1e9),
               "original_nonmember_positive_cps_bn": float(original_weighted[:, 0].sum() / 1e9),
               "union_bn": float(direct[0]), "union_se_bn": sdr(direct),
               "uncalibrated_union_bn": float(raw_direct[0]), "uncalibrated_union_se_bn": sdr(raw_direct),
               "generation_bn": {g: float(account[i, 0]) for i, g in enumerate(["G1", "G2", "G3+"])},
               "generation_se_bn": {g: sdr(account[i]) for i, g in enumerate(["G1", "G2", "G3+"])},
               "state_calibration": state_rows,
               "gates": {"state_calibration_closure_bn": closure, "generation_closure_bn": closure_gen,
                         "survivor_head_spouse_swap_max_input_difference": symmetry,
                         "original_weights_preserved": True, "survivor_own_weights_preserved": True},
               "held": ["zero unobserved itemized deductions/rents/property taxes",
                        ("shared canonical childcare attribution held as supplied by driver"
                         if refiling is not None and "before_input" in refiling
                         else "zero unobserved attributable childcare"),
                        "all dividends qualified; capital gains long-term; pensions taxable",
                        "self-employment non-QBI; no shared unexplained original AGI residual",
                        "positive after-credit tax floor; negative state refunds not spending",
                        "state-level calibration factor transports across refiling/income change",
                        "identified union; added lineage extrapolation external and assumed",
                        "other_personal_tax held (same proxy key does not establish same behavioral response)"]}
    return {"M2": account, "details": details, "terms": terms,
            "remaining_state_liability": remaining_by_return,
            "remaining_state_own": np.where(remaining_live, own, -1),
            "remaining_state_live": remaining_live}


if __name__ == "__main__":
    if sys.argv[1:] == ["--acquire"]:
        acquire_sources()
    elif sys.argv[1:] == ["--run"]:
        import importlib.util
        import resource
        import time
        started = time.perf_counter()
        path = LANE.parent / "mixed_unit_credits_2026_10_14/credits.py"
        spec = importlib.util.spec_from_file_location("mixed_state_credits", path)
        credits = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(credits)
        d = credits.load()
        civ, union, gen = credits.groups(d)
        W, _, _ = credits.row4_weights(d, civ, union)
        d = d.drop(columns=credits.REPS[1:])
        flag, onbooks, _ = credits.status_flag(d)
        R, *_ = credits.returns(d, union, gen, civ)
        P = credits.person_income(d)
        model = json.loads(credits.MODEL.read_text())
        result = compute(d, R, P, None, W, union, gen, flag, onbooks, model, civ=civ)
        out = LANE / "derived"
        out.mkdir(exist_ok=True)
        (out / "state_sensitivity.json").write_text(json.dumps(result["details"], indent=2) + "\n")
        pd.DataFrame(result["terms"]).to_csv(out / "state_terms.csv", index=False, lineterminator="\n")
        pd.DataFrame(result["M2"], index=["G1", "G2", "G3+"],
                     columns=credits.REPS).to_csv(out / "state_replicates.csv", lineterminator="\n")
        print(json.dumps({"union_bn": result["details"]["union_bn"],
                          "se_bn": result["details"]["union_se_bn"],
                          "elapsed_s": time.perf_counter() - started,
                          "self_maxrss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                          "child_maxrss_bytes": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}))
    else:
        print(json.dumps(verify_sources(), indent=2))
