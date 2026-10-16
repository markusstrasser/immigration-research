"""Read-only raw SIPP allocation diagnostic; no outcomes or effects estimated.

Run: uv run --no-project python3 <this script>
The diagnostic reads fixed official component definitions and streams the raw ZIP.
"""
from __future__ import annotations

import hashlib
import json
import time
import zipfile
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RAW = ROOT / "sources/immigration-fiscal/data/external/stage3/census/sipp_2025/pu2025_csv.zip"
DEFINITIONS = HERE / "component_definitions.json"
OUT = HERE / "_cache/component_flags.parquet"
TOTALS = HERE / "derived/component_allocation_totals.json"
RECEIPT = HERE / "_cache/component_allocation_receipt.json"
EXPECTED_RAW_SHA256 = "570798a6f512c8f82af311ee01a1668d178063c9076c18a05bc3a5a0039b67ed"
KEYS = ["SSUID", "PNUM", "MONTHCODE"]
RECODE_PAIRS = {"AMESR": "RMESR", "AMWKHRS": "TMWKHRS", "APEARN_ALT": "TPEARN_ALT"}
CHUNKSIZE = 20_000


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def dump(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def main() -> None:
    start = time.monotonic()
    source_digest = digest(RAW)
    if source_digest != EXPECTED_RAW_SHA256:
        raise RuntimeError("[BLOCKED] original SIPP 2025 archive hash differs")
    definitions = json.loads(DEFINITIONS.read_text())
    groups = {k: [v["name"] for v in vs] for k, vs in definitions["groups"].items()}
    groups["nonemployment"] = [v["name"] for v in definitions["nonemployment_flags"]]
    components = sorted(v for vs in groups.values() for v in vs)
    if components != definitions["names"] or len(set(components)) != len(components):
        raise RuntimeError("[BLOCKED] component groups differ from exact names or overlap")
    if len(components) != 393:
        raise RuntimeError("[BLOCKED] expected 393 primary-schema component flags")
    sets = {f"base_{k}": [k] for k in groups}
    sets.update({
        "employment": ["job_presence_and_timing", "nonemployment"],
        "hours": ["job_presence_and_timing", "hours", "unpaid_absence"],
        "earnings": ["job_presence_and_timing", "hours", "unpaid_absence", "earnings"],
        "all_visible": list(groups),
    })
    widths = {k: sum(len(groups[g]) for g in gs) for k, gs in sets.items()}
    receipt = {
        "status": "running",
        "raw": {"path": str(RAW.relative_to(ROOT)), "sha256": source_digest,
                "bytes": RAW.stat().st_size,
                "url": "https://www2.census.gov/programs-surveys/sipp/data/datasets/2025/pu2025_csv.zip"},
        "definitions_sha256": digest(DEFINITIONS), "script_sha256": digest(Path(__file__)),
        "chunk_size": CHUNKSIZE,
        "semantics": {
            "allocation_count": "Number of flags in 2..8: any imputation or mixture.",
            "unresolved_recode_count": "Number of flags equal to9: component provenance unresolved.",
            "observed_clean": "Every nonmissing visible flag is0 or1; missing flags counted separately. An all-missing set is vacuously true; check observed_count.",
            "complete_clean": "observed_clean and missing_count==0.",
            "limit": "Public-component allocation screen; not proof that all underlying or suppressed components are unallocated. No causal or effect estimate.",
        },
        "categories": {k: {"groups": gs, "n_flags": widths[k]} for k, gs in sets.items()},
    }
    dump(RECEIPT, receipt)
    sums = {k: Counter() for k in sets}
    histograms = {k: Counter() for k in groups}
    recodes = {k: {"all_rows": Counter(), "numeric_outcome_rows": Counter()} for k in RECODE_PAIRS}
    seen = set()
    rows = 0
    partial = OUT.with_suffix(".partial.parquet")
    writer = None
    parse_start = time.monotonic()
    try:
        with zipfile.ZipFile(RAW) as archive:
            members = [n for n in archive.namelist() if n.lower().endswith(".csv")]
            if members != ["pu2025.csv"]:
                raise RuntimeError(f"[BLOCKED] unexpected archive members: {members}")
            receipt["raw"]["member"] = members[0]
            with archive.open(members[0]) as stream:
                header = stream.readline().decode("utf-8-sig").strip().split("|")
            usecols = KEYS + components + list(RECODE_PAIRS) + list(RECODE_PAIRS.values())
            if len(header) != len(set(header)) or set(usecols) - set(header):
                raise RuntimeError("[BLOCKED] duplicate header or missing required fields")
            dtypes = {name: "float32" for name in usecols if name not in KEYS}
            dtypes.update({"SSUID": "string", "PNUM": "int16", "MONTHCODE": "int8"})
            with archive.open(members[0]) as stream:
                reader = pd.read_csv(stream, sep="|", usecols=usecols, dtype=dtypes,
                                     chunksize=CHUNKSIZE)
                for chunk_no, chunk in enumerate(reader, 1):
                    keys = list(chunk[KEYS].itertuples(index=False, name=None))
                    if chunk[KEYS].isna().any().any() or len(set(keys)) != len(keys) or seen.intersection(keys):
                        raise RuntimeError("[BLOCKED] missing or duplicate person-month key")
                    seen.update(keys)
                    if not chunk.MONTHCODE.between(1, 12).all():
                        raise RuntimeError("[BLOCKED] invalid reference month")
                    base = {}
                    for name, names in groups.items():
                        array = chunk[names].to_numpy()
                        missing = np.isnan(array)
                        if ((~missing) & ((array < 0) | (array > 9) | (array != np.floor(array)))).any():
                            raise RuntimeError(f"[BLOCKED] invalid flag in {name}")
                        base[name] = {
                            "missing_count": missing.sum(axis=1, dtype=np.int16),
                            "niu_count": (array == 0).sum(axis=1, dtype=np.int16),
                            "reported_count": (array == 1).sum(axis=1, dtype=np.int16),
                            "allocation_count": ((array >= 2) & (array <= 8)).sum(axis=1, dtype=np.int16),
                            "unresolved_recode_count": (array == 9).sum(axis=1, dtype=np.int16),
                        }
                        codes, counts = np.unique(array[~missing], return_counts=True)
                        histograms[name].update({str(int(c)): int(n) for c, n in zip(codes, counts)})
                        histograms[name]["missing"] += int(missing.sum())
                    columns = {k: chunk[k].to_numpy() for k in KEYS}
                    for name, selected in sets.items():
                        values = {metric: sum((base[g][metric] for g in selected),
                                              np.zeros(len(chunk), dtype=np.int16))
                                  for metric in next(iter(base.values()))}
                        values["observed_count"] = widths[name] - values["missing_count"]
                        values["observed_clean"] = (values["allocation_count"] == 0) & (values["unresolved_recode_count"] == 0)
                        values["complete_clean"] = values["observed_clean"] & (values["missing_count"] == 0)
                        values["has_observed_components"] = values["observed_count"] > 0
                        if not (sum(values[k] for k in ("missing_count", "niu_count", "reported_count", "allocation_count", "unresolved_recode_count")) == widths[name]).all():
                            raise RuntimeError("[BLOCKED] component accounting does not close")
                        for metric, array in values.items():
                            columns[f"{name}__{metric}"] = array
                            sums[name][metric] += int(array.sum())
                        for metric in ("missing_count", "allocation_count", "unresolved_recode_count"):
                            sums[name][f"rows_with_{metric.removesuffix('_count')}"] += int((values[metric] > 0).sum())
                    for flag, outcome in RECODE_PAIRS.items():
                        for scope, mask in (("all_rows", np.ones(len(chunk), dtype=bool)),
                                            ("numeric_outcome_rows", chunk[outcome].notna())):
                            codes = chunk.loc[mask, flag].value_counts(dropna=False)
                            recodes[flag][scope].update({"missing" if pd.isna(k) else str(int(k)): int(n) for k, n in codes.items()})
                    table = pa.Table.from_pandas(pd.DataFrame(columns), preserve_index=False)
                    if writer is None:
                        writer = pq.ParquetWriter(partial, table.schema, compression="zstd")
                    writer.write_table(table)
                    rows += len(chunk)
                    print(json.dumps({"chunk": chunk_no, "rows": rows,
                                      "elapsed_seconds": round(time.monotonic()-start, 2)}), flush=True)
        if writer is not None:
            writer.close()
            writer = None
        if not rows:
            raise RuntimeError("[BLOCKED] empty data")
        partial.replace(OUT)
        totals = {"rows": rows, "unique_person_months": len(seen),
                  "categories": {k: dict(v) for k, v in sums.items()},
                  "component_flag_histograms": {k: dict(v) for k, v in histograms.items()},
                  "aggregate_recode_flags": recodes,
                  "direct_flag1_sensitivity_valid": False,
                  "direct_flag1_reason": "The numeric aggregate outcomes use recode status9, which directs users to components; flag1 does not select reported aggregate outcomes."}
        for flag in RECODE_PAIRS:
            if set(recodes[flag]["numeric_outcome_rows"]) != {"9"}:
                raise RuntimeError(f"[BLOCKED] aggregate flag9-only finding did not reproduce: {flag}")
        dump(TOTALS, totals)
        receipt.update({"status": "complete", "rows": rows,
                        "elapsed_seconds": round(time.monotonic()-start, 3),
                        "parse_and_reduce_seconds": round(time.monotonic()-parse_start, 3),
                        "output": {"path": str(OUT), "bytes": OUT.stat().st_size, "sha256": digest(OUT)},
                        "totals_sha256": digest(TOTALS)})
        dump(RECEIPT, receipt)
        print(json.dumps({"status": "complete", "rows": rows,
                          "elapsed_seconds": receipt["elapsed_seconds"], "output": str(OUT)}))
    except Exception as exc:
        if writer is not None:
            writer.close()
        receipt.update({"status": "failed", "error": str(exc), "rows_completed": rows,
                        "elapsed_seconds": round(time.monotonic()-start, 3)})
        dump(RECEIPT, receipt)
        raise


if __name__ == "__main__":
    main()
