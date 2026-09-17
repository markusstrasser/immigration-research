"""Preserve and check the three follow-up exports against the audited NLS fields."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
NAMES = ["nlsy97_gen_crime_2.zip", "nlsy97_gen_crime_2 (2).zip",
         "nlsy97_gen_crime_2 (3).zip"]


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main(source):
    required = set(Path(__file__).with_name("required_analyzed_fields.NLSY97").read_text().split())
    baseline_path = ROOT / "derived/nlsy/full_selected_data.csv"
    baseline = pd.read_csv(baseline_path).set_index("R0000100").sort_index()
    assert len(baseline) == 8984 and baseline.index.is_unique
    report = {"acquired": "2026-09-17", "files": [],
              "baseline_selected_sha256": digest(baseline_path)}
    seen = {}
    for name in NAMES:
        original = source / name
        checksum = digest(original)
        canonical = seen.setdefault(checksum, name)
        staged = ROOT / "raw" / canonical
        if not staged.exists():
            shutil.copy2(original, staged)
        assert digest(staged) == checksum, f"Staged archive differs: {staged}"
        report["files"].append({"input": str(original), "bytes": original.stat().st_size,
                                "sha256": checksum, "staged": str(staged.relative_to(ROOT)),
                                "exact_duplicate_of": canonical if canonical != name else None})
    # Keep different exports separate rather than silently choosing one.
    assert len(seen) == 1, "Follow-up exports differ; each requires separate comparison"
    with zipfile.ZipFile(ROOT / "raw" / NAMES[0]) as archive:
        assert archive.testzip() is None, "Archive CRC failure"
        report["members"] = [{"name": member.filename, "bytes": member.file_size,
                              "crc32": member.CRC} for member in archive.infolist()]
        with archive.open("nlsy97_gen_crime_2.csv") as stream:
            columns = list(pd.read_csv(stream, nrows=0).columns)
        tags = set(archive.read("nlsy97_gen_crime_2.NLSY97").decode().split())
        assert len(columns) == len(set(columns)) and set(columns) == tags
        overlap = sorted(required.intersection(columns))
        with archive.open("nlsy97_gen_crime_2.csv") as stream:
            data = pd.read_csv(stream, usecols=overlap).set_index("R0000100").sort_index()
    assert len(data) == 8984 and data.index.is_unique and data.index.equals(baseline.index)
    mismatches = {col: int((data[col].ne(baseline[col]) &
                           ~(data[col].isna() & baseline[col].isna())).sum())
                  for col in data.columns}
    with zipfile.ZipFile(ROOT / "raw/nlsy97_gen_crime_1 (9).zip") as archive:
        previous = set(archive.read("nlsy97_gen_crime_1.NLSY97").decode().split())
    report.update({"rows": len(data), "unique_ids": data.index.nunique(),
                   "exported_fields": len(columns), "required_present": overlap,
                   "required_missing": sorted(required - tags),
                   "fields_added_to_previous_export": len(tags - previous),
                   "combined_exported_fields": len(tags | previous),
                   "required_missing_from_combined": sorted(required - (tags | previous)),
                   "baseline_value_mismatches": mismatches,
                   "all_examined_values_match": not any(mismatches.values()),
                   "scope": "ID and seven overlapping non-ID fields checked; no claim about unexamined fields or latest release."})
    target = ROOT / "nlsy/followup_export_check.json"
    target.write_text(json.dumps(report, indent=2) + "\n")
    data.to_csv(ROOT / "derived/nlsy/followup_selected_data.csv")
    print(json.dumps({k: v for k, v in report.items() if k not in {"files", "members"}}, indent=2))
    assert not any(mismatches.values()), "Audited fields changed; reassess prior outcome tables"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("/Users/alien/Downloads"))
    main(parser.parse_args().source)
