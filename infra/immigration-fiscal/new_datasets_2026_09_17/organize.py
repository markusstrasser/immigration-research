"""Build a named survey library from verified raw copies without altering originals."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

from stage import sha256

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
# Existing source filenames remain provenance keys; only the library copies are renamed.
COLLECTION = [
    ("nlsy97_gen_crime_1 (9).zip", "nlsy97/nlsy97-longitudinal-extract-part1.zip", "Microdata: 8,984 people; same cohort as other NLS files"),
    ("nlsy97_gen_crime_2.zip", "nlsy97/nlsy97-crime-event-history-part2.zip", "Microdata: same 8,984 people; adds crime histories"),
    ("default.zip", "nlsy97/nlsy97-family-history-crime-core.zip", "Microdata: all 98 requested fields plus one extra; use for audited core analysis"),
    ("gen_crime_2026.NLSY97", "nlsy97/nlsy97-original-variable-selection.NLSY97", "Selection request only; not respondent data"),
    ("PHCNSL2011PubRelease.zip", "pew/pew-national-survey-latinos-2011.zip", "Microdata: independent survey"),
    ("PHCNSL2012PublicRelease.zip", "pew/pew-national-survey-latinos-2012.zip", "Microdata: independent survey"),
    ("Pew-Research-Center-2013-U.S.-Latino-Religion-Survey.zip", "pew/pew-latino-religion-survey-2013.zip", "Microdata: independent religion survey"),
    ("Pew-Research-Center_2014-National-Survey-of-Latinos-Dataset.zip", "pew/pew-national-survey-latinos-2014.zip", "Microdata: independent survey"),
    ("Pew-Research-Center_2015-National-Survey-of-Latinos-Dataset.zip", "pew/pew-national-survey-latinos-2015.zip", "Microdata: identifying sample paired analytically with 2015–16 nonidentifiers"),
    ("Pew-Research-Center_2016-Survey-of-Self-Identified-non-Hispanics-Dataset.zip", "pew/pew-hispanic-ancestry-nonidentifiers-2015-2016.zip", "Microdata: complementary population to NSL2015; no matched-person join"),
    ("Pew-Research-Center_2016-National-Survey-of-Latinos-Dataset.zip", "pew/pew-national-survey-latinos-2016.zip", "Microdata: independent survey"),
    ("Pew-Research-Center_2018-National-Survey-of-Latinos-Dataset.zip", "pew/pew-national-survey-latinos-2018.zip", "Microdata: independent survey"),
    ("ICPSR_30302-V1.zip", "icpsr/icpsr-30302-new-york-second-generation-v1-DOCUMENTATION-ONLY.zip", "Documentation only: restricted respondent data absent"),
    ("ICPSR_20862-V6.zip", "icpsr/icpsr-20862-latino-national-survey-2006-v6-DOCUMENTATION-ONLY.zip", "Documentation only: public respondent data absent"),
    ("ICPSR_20862-V6 (1).zip", "icpsr/icpsr-20862-lns2006-v6-dataset3-DOCUMENTATION-SUBSET.zip", "Documentation subset: all seven members already present in full documentation package"),
]


def organize(destination, downloads):
    evidence = []
    for name in ["manifest.json", "nlsy/followup_export_check.json", "completion_check.json"]:
        evidence.extend(json.loads((ROOT / name).read_text())["files"])
    by_staged = {}
    for record in evidence:
        by_staged.setdefault(Path(record["staged"]).name, []).append(record)
    assert set(by_staged) == {source for source, _, _ in COLLECTION}, "Unmapped source archives"
    rows = []
    for source_name, target_name, purpose in COLLECTION:
        source = ROOT / "raw" / source_name
        checks = by_staged[source_name]
        digest = sha256(source)
        assert all(c["sha256"] == digest for c in checks), f"Source drift: {source}"
        target = destination / target_name
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            shutil.copy2(source, target)
        assert sha256(target) == digest, f"Existing library file differs: {target}"
        rows.append({"name": target_name, "purpose": purpose, "bytes": source.stat().st_size,
                     "sha256": digest, "staged_source": str(source.relative_to(REPO)),
                     "original_inputs": [c["input"] for c in checks]})
    # The operator also pointed to an extracted folder. Compare actual bytes to ZIP members.
    folder = downloads / "ICPSR_20862"
    folder_check = {"path": str(folder), "status": "NOT_PRESENT"}
    if folder.is_dir():
        members = [p for p in folder.rglob("*") if p.is_file()]
        with zipfile.ZipFile(ROOT / "raw/ICPSR_20862-V6.zip") as archive:
            matches = [p for p in members if "ICPSR_20862/" + p.relative_to(folder).as_posix() in archive.namelist()
                       and sha256(p) == hashlib.sha256(archive.read("ICPSR_20862/" + p.relative_to(folder).as_posix())).hexdigest()]
        folder_check.update(files=len(members), matching_files=len(matches),
                            status="EXACT_EXTRACTED_COPY" if len(matches) == len(members) == 10 else "REQUIRES_INSPECTION")
        assert folder_check["status"] == "EXACT_EXTRACTED_COPY", "Folder has new or changed evidence"
    additional = downloads / "nlsy97_gen_crime_2 (4).zip"
    if additional.exists():
        row = next(x for x in rows if "event-history-part2" in x["name"])
        assert sha256(additional) == row["sha256"], "Additional export differs"
        row["original_inputs"].append(str(additional))
    # Rebuilt ZIPs can differ at the archive level despite identical data/document bytes.
    equivalent = []
    extra_names = ["nlsy97_gen_crime.zip", "ICPSR_20862-V6 (2).zip", "ICPSR_20862-V6 (3).zip"]
    for name in extra_names:
        original = downloads / name
        if not original.exists():
            continue
        staged = ROOT / "raw" / name
        if not staged.exists():
            shutil.copy2(original, staged)
        assert sha256(staged) == sha256(original)
        baseline = "default.zip" if name.startswith("nlsy") else "ICPSR_20862-V6.zip"
        with zipfile.ZipFile(staged) as new, zipfile.ZipFile(ROOT / "raw" / baseline) as old:
            assert new.testzip() is None
            if name.startswith("nlsy"):
                checked = [".csv", ".cdb", ".NLSY97"]
                same = all(new.read("nlsy97_gen_crime" + suffix) == old.read("default" + suffix) for suffix in checked)
                scope = "Identical CSV, codebook and tagset; generated control filenames may differ"
            else:
                checked = new.namelist()
                same = set(checked) == set(old.namelist()) and all(new.read(member) == old.read(member) for member in checked)
                scope = "Identical member names and bytes; ZIP wrapper differs"
        assert same, f"Additional download has new evidence: {name}"
        equivalent.append({"input": str(original), "sha256": sha256(staged), "bytes": staged.stat().st_size,
                           "staged": str(staged.relative_to(REPO)), "equivalent_to": baseline,
                           "comparison": scope, "checked_members": checked})
    request_source = ROOT / "nlsy/required_analyzed_fields.NLSY97"
    request_target = destination / "nlsy97/nlsy97-audited-core-request-98.NLSY97"
    if not request_target.exists():
        shutil.copy2(request_source, request_target)
    assert sha256(request_target) == sha256(request_source)
    catalog = {"organized": "2026-09-17", "files": rows, "extracted_folder": folder_check,
               "equivalent_redownloads": equivalent,
               "analysis_request": str(request_target.relative_to(destination)),
               "join_rule": "NLS files join by validated respondent ID. Pew years do not join people. ICPSR held files contain no respondent data."}
    (destination / "catalog.json").write_text(json.dumps(catalog, indent=2) + "\n")
    lines = ["# Immigration survey library", "", "Organized September 17, 2026. Every renamed copy is SHA-256 verified against the staged original. Originals and prior analysis paths remain intact.", "",
             "Use the NLS core export for the audited family-history/crime fields. NLS parts add columns for the same people. Pew years are independent cross-sections. Both ICPSR studies currently contain documentation only.", "",
             "| Named file | Contents / use | Original download names |", "|---|---|---|"]
    for row in rows:
        aliases = "; ".join(Path(x).name for x in row["original_inputs"])
        lines.append(f"| [{Path(row['name']).name}]({row['name']}) | {row['purpose']} | {aliases} |")
    lines += ["", "Duplicate filenames map to one copy. The DS0003 documentation subset is retained and explicitly labeled; it is not an additional survey. The extracted ICPSR folder adds no files beyond the full documentation ZIP.", "",
              "[Machine-readable catalog and hashes](catalog.json). The 98-field Investigator request is `nlsy97/nlsy97-audited-core-request-98.NLSY97`; its requested data are already acquired."]
    lines += ["", "## Equivalent later downloads", ""]
    for item in equivalent:
        lines.append(f"- `{Path(item['input']).name}` → `{item['equivalent_to']}`: {item['comparison']}. Original and staged archive retained.")
    (destination / "README.md").write_text("\n".join(lines) + "\n")
    print(f"Organized {len(rows)} unique supplied file variants plus audited request in {destination}")
    print(f"Original file paths accounted for: {sum(len(r['original_inputs']) for r in rows) + len(equivalent)}; extracted folder: {folder_check['status']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, default=ROOT / "library")
    parser.add_argument("--downloads", type=Path, default=Path("/Users/alien/Downloads"))
    args = parser.parse_args()
    organize(args.destination, args.downloads)
