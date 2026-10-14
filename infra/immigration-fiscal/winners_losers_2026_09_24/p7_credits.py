"""Exact crossing-credit incidence by filer, reusing the validated source lane.

The source lane keeps its calibrated per-return vectors inside main(). Run it in a
subprocess, redirect only its outputs, and capture the successful return frame.
This avoids copying the tax model or retaining its replicate matrix in the caller.
Every component closes to the committed primary summary before export. Arrays are
2024 dollars per carrier, unweighted; totals and SDR SEs are account $bn on row 4.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import tempfile
import time

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = HERE.parent / "mixed_unit_credits_2026_10_14/credits.py"
PRIMARY = SOURCE.parent / "derived/summary.json"
COMPONENTS = {
    "forward_A": ("A_nonref", "A_care", "A_actc", "A_eitc"),
    "forward_C": ("C_status",),
    "reverse_B": ("B_nonref", "B_care", "B_actc", "B_eitc"),
    "reverse_Cr": ("Cr_status",),
}


def _require(ok, message):
    if not ok:
        raise RuntimeError(f"[BLOCKED] crossing-credit helper: {message}")


def _sha(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def _build(out: Path):
    started = time.perf_counter()
    sys.dont_write_bytecode = True
    read_paths = set()

    def audit(event, args):
        if event != "open" or not isinstance(args[0], (str, bytes, os.PathLike)):
            return
        path = Path(os.fsdecode(args[0])).resolve()
        if not path.is_relative_to(ROOT):
            return
        flags = args[2]
        write = bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
        if write:
            _require(path.is_relative_to(out), f"source attempted an upstream write: {path}")
        elif path.is_file() and not path.is_relative_to(out):
            read_paths.add(path)

    sys.addaudithook(audit)
    spec = importlib.util.spec_from_file_location("p7_primary_credits", SOURCE)
    source = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source)
    source.OUT = out / "primary_rebuild"
    captured = {}

    def profile(frame, event, arg):
        if event == "return" and frame.f_code is source.main.__code__:
            captured.update(frame.f_locals)

    # Capture only a successful main return. Exceptions cannot authorize export.
    sys.setprofile(profile)
    try:
        source.main()
    finally:
        sys.setprofile(None)
    required = {"d", "h", "wr", "comp_ruled", "side", "per_fit", "per_ref", "keep_of", "account", "owner"}
    _require(required <= captured.keys(), f"source main contract changed: missing {required - captured.keys()}")
    primary = json.loads(PRIMARY.read_text())
    loc = captured
    d, h, weights = loc["d"], loc["h"], loc["wr"]
    arrays = {"PH_SEQ": d.PH_SEQ.to_numpy()[h], "PPPOS": d.PPPOS.to_numpy()[h],
              "source_weight": weights[:, 0], "member": loc["R"].mem_h.to_numpy()}
    meta = {"reading": "R3", "units": "unweighted 2024 dollars per tax-return carrier",
            "total_units": "account $bn on audit row 4", "components": {}, "gates": {}}
    lookup = {"forward_A": "forward_A", "forward_C": "status_C_forward",
              "reverse_B": "reverse_B", "reverse_Cr": "status_Cr_reverse"}
    replicates = {}
    for name, keys in COMPONENTS.items():
        vector = np.zeros(len(h))
        reps = np.zeros(161)
        for key in keys:
            x = loc["comp_ruled"][key] * loc["keep_of"]("R3", key)
            conversion = loc["per_fit"] if loc["side"][key] == "receipts" else loc["per_ref"][0]
            vector += x * conversion * 1e9
            reps += loc["account"](x, key)
        got, se = float(reps[0]), source.sdr(reps)
        target = primary["account"]["R3"][lookup[name]]
        _require(abs(got - target["bn"]["total"]) < 1e-8, f"{name} primary total drift")
        _require(abs(se - target["se_bn"]["total"]) < 1e-9, f"{name} primary replicate SE drift")
        _require(abs(vector @ weights[:, 0] / 1e9 - got) < 1e-9, f"{name} carrier-vector closure")
        expected_member = name.startswith("reverse")
        _require(not np.any((np.abs(vector) > 1e-10) & (arrays["member"] != expected_member)),
                 f"{name} assigned to the wrong side of the group")
        arrays[name] = vector
        replicates[name] = reps
        meta["components"][name] = {"total_bn": got, "se_bn": se, "primary_total_bn": target["bn"]["total"]}
        meta["gates"][name] = True
    for name, parts in {"forward": ("forward_A", "forward_C"),
                        "reverse": ("reverse_B", "reverse_Cr")}.items():
        arrays[name] = sum(arrays[k] for k in parts)
        reps = sum(replicates[k] for k in parts)
        meta[name] = {"total_bn": float(reps[0]), "se_bn": source.sdr(reps)}
    g3_vector=np.zeros(len(h))
    g3_reps=np.zeros(161)
    for key in (*COMPONENTS["forward_A"],*COMPONENTS["forward_C"]):
        x=loc["comp_ruled"][key]*loc["owner"][key][2]*loc["keep_of"]("R3",key)
        conversion=loc["per_fit"] if loc["side"][key]=="receipts" else loc["per_ref"][0]
        g3_vector+=x*conversion*1e9
        g3_reps+=loc["account"](x,key)
    g3_primary=sum(primary["account"]["R3"][k]["bn"]["G3+"] for k in ("forward_A","status_C_forward"))
    _require(abs(g3_reps[0]-g3_primary)<1e-8,"G3+ forward primary total drift")
    _require(abs(g3_vector@weights[:,0]/1e9-g3_reps[0])<1e-9,"G3+ forward carrier closure")
    arrays["forward_g3plus"]=g3_vector
    meta["forward_g3plus"]={"total_bn":float(g3_reps[0]),"se_bn":source.sdr(g3_reps)}
    combined = sum(replicates.values())
    target = primary["account"]["R3"]["child_credit_and_status_net"]
    _require(abs(combined[0] - target["bn"]["total"]) < 1e-8, "R3 item total closure")
    _require(abs(source.sdr(combined) - target["se_bn"]["total"]) < 1e-9, "R3 item joint SE closure")
    meta["gates"]["R3_item_joint_total_and_SE"] = True
    np.savez_compressed(out / "carriers.npz", **arrays)
    meta["source_paths"] = [str(path) for path in sorted(read_paths)]
    meta["source_sha256"] = {str(path): _sha(path) for path in sorted(read_paths)}
    meta["source_gates"] = len(source.GATES)
    meta["wall_seconds"] = time.perf_counter() - started
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    meta["peak_memory_bytes"] = peak if sys.platform == "darwin" else peak * 1024
    _require(meta["peak_memory_bytes"] < 2.5 * 1024**3, "subprocess exceeded the 2.5 GiB budget")
    (out / "metadata.json").write_text(json.dumps(meta, indent=1) + "\n")


def crossing_credit_arrays(d, wl=None):
    """Return carrier-dollar arrays in d's row order, plus exact source totals/SEs.

    forward=A+C belongs to non-member filers; reverse=B+Cr (signed negative)
    remains on member filers and is available for a mixed-unit resource arm.
    The caller must state how added descendants change recipient weights; these
    source vectors cover the identified union and close on source row-4 weights.
    """
    cache = HERE / "_cache"
    cache.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="p7_credits_", dir=cache) as temp:
        out = Path(temp)
        env = dict(os.environ, OPENBLAS_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
        proc = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--build", str(out)],
                              cwd=ROOT, env=env, capture_output=True, text=True)
        _require(proc.returncode == 0, f"source subprocess exit {proc.returncode}:\n{proc.stdout[-3000:]}\n{proc.stderr[-3000:]}")
        meta = json.loads((out / "metadata.json").read_text())
        with np.load(out / "carriers.npz") as loaded:
            carrier_index = pd.MultiIndex.from_arrays([loaded["PH_SEQ"], loaded["PPPOS"]])
            target_index = pd.MultiIndex.from_arrays([d.PH_SEQ.to_numpy(), d.PPPOS.to_numpy()])
            _require(carrier_index.is_unique and target_index.is_unique, "duplicate person join key")
            positions = target_index.get_indexer(carrier_index)
            _require(np.all(positions >= 0), "caller is missing a source tax-return carrier")
            result = {}
            for name in [*COMPONENTS, "forward", "reverse", "forward_g3plus"]:
                values = np.zeros(len(d))
                values[positions] = loaded[name]
                result[name] = values
            result["source_weight"] = np.zeros(len(d))
            result["source_weight"][positions] = loaded["source_weight"]
            for name in [*COMPONENTS, "forward", "reverse", "forward_g3plus"]:
                total = result[name] @ result["source_weight"] / 1e9
                want = meta["components"][name]["total_bn"] if name in COMPONENTS else meta[name]["total_bn"]
                _require(abs(total - want) < 1e-9, f"{name} caller join loses mass")
        result["metadata"] = meta
        if wl is not None:
            wl.gate("p7_crossing_credit_source_and_join_close", True,
                    forward_bn=meta["forward"]["total_bn"], reverse_bn=meta["reverse"]["total_bn"],
                    source_gates=meta["source_gates"])
        return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", type=Path, required=True)
    args = parser.parse_args()
    args.build.mkdir(parents=True, exist_ok=True)
    _build(args.build.resolve())
