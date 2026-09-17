"""Stage the final supplied NLS request and check ICPSR respondent-data presence."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import zipfile

import pandas as pd

from stage import inspect_zip, sha256

ROOT = Path(__file__).resolve().parent


def main(source):
    files = []
    for name in ["default.zip", "ICPSR_20862-V6 (1).zip"]:
        original = source / name
        checksum = sha256(original)
        target = ROOT / "raw" / name
        if not target.exists():
            shutil.copy2(original, target)
        assert sha256(target) == checksum, f"Staged file differs: {target}"
        files.append({"input": str(original), "sha256": checksum,
                      "bytes": original.stat().st_size,
                      "staged": str(target.relative_to(ROOT)),
                      "members": inspect_zip(target)})
    required = set((ROOT / "nlsy/required_analyzed_fields.NLSY97").read_text().split())
    baseline_path = ROOT / "derived/nlsy/full_selected_data.csv"
    baseline = pd.read_csv(baseline_path).set_index("R0000100").sort_index()
    with zipfile.ZipFile(ROOT / "raw/default.zip") as archive:
        frame = pd.read_csv(archive.open("default.csv"))
        tags = set(archive.read("default.NLSY97").decode().split())
        codebook = archive.read("default.cdb").decode()
    documented = {a + b for a, b in re.findall(r"(?m)^([A-Z]\d{5})\.(\d{2})\s+\[", codebook)}
    assert set(frame) == tags and len(frame.columns) == len(tags)
    assert not required - tags and not required - documented, "Incomplete requested fields/codebook"
    supplied = frame.set_index("R0000100").sort_index()
    assert len(supplied) == len(baseline) == 8984
    assert supplied.index.is_unique and baseline.index.is_unique
    assert supplied.index.equals(baseline.index), "Respondent IDs differ"
    mismatches = {c: int((supplied[c].ne(baseline[c]) &
                         ~(supplied[c].isna() & baseline[c].isna())).sum())
                  for c in sorted(required - {"R0000100"})}
    # Inventory actual files, never treat catalog manifest entries as downloaded data.
    icpsr_data = [m["name"] for m in files[1]["members"]
                 if Path(m["name"]).suffix.lower() in {".dta", ".sav", ".por", ".csv", ".tsv", ".dat", ".rds", ".rda", ".rdata"}]
    with zipfile.ZipFile(ROOT / "raw/ICPSR_20862-V6.zip") as previous:
        identical_members = [m["name"] for m in files[1]["members"]
                             if m["name"] in previous.namelist() and
                             hashlib.sha256(previous.read(m["name"])).hexdigest() == m["sha256"]]
    report = {"acquired": "2026-09-17", "files": files,
              "nls": {"rows": len(frame), "columns": len(frame.columns),
                      "required_fields": len(required), "required_missing": sorted(required - tags),
                      "extra_fields": sorted(tags - required), "required_codebooks_present": True,
                      "same_unique_ids": True, "baseline_selected_sha256": sha256(baseline_path),
                      "non_id_value_mismatches": mismatches,
                      "all_requested_values_match": not any(mismatches.values())},
              "icpsr": {"members": len(files[1]["members"]), "identical_to_previous": identical_members,
                        "respondent_data_files": icpsr_data,
                        "status": "DATA_PRESENT_REQUIRES_VALIDATION" if icpsr_data else "DOCUMENTATION_ONLY"}}
    (ROOT / "completion_check.json").write_text(json.dumps(report, indent=2) + "\n")
    frame.to_csv(ROOT / "derived/nlsy/completed_request_data.csv", index=False)
    assert not any(mismatches.values()), "Requested values changed; reassess analysis"
    print(f"NLS: {len(frame)} rows, {len(frame.columns)} columns; all {len(required)} requested fields and codebooks present; zero mismatches")
    print(f"ICPSR: {report['icpsr']['status']}; {len(files[1]['members'])} archive members")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("/Users/alien/Downloads"))
    main(parser.parse_args().source)
