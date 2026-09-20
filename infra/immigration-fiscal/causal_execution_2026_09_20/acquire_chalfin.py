"""Stage and pin the already-downloaded official Chalfin replication package."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ARCHIVE_SHA = "d7cfaf74028b1dc74ea87e4dea4075e941909317403014fad1da24958fbd0fa9"
MEMBERS = {"LICENSE.txt", "data/chalfin_code.do", "data/chalfin_data.dta"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    args = parser.parse_args()
    payload = args.archive.read_bytes()
    if hashlib.sha256(payload).hexdigest() != ARCHIVE_SHA:
        raise ValueError("Archive differs from the inspected official V1 snapshot")
    out = Path(__file__).resolve().parent / "raw/chalfin"
    with zipfile.ZipFile(args.archive) as archive:
        names = {m.filename for m in archive.infolist() if not m.is_dir()}
        if names != MEMBERS or archive.testzip() is not None:
            raise ValueError("Unexpected or damaged archive members")
        out.mkdir(parents=True, exist_ok=True)
        records = []
        for name in sorted(MEMBERS):
            data = archive.read(name)
            target = out / name
            if target.exists() and target.read_bytes() != data:
                raise ValueError(f"Refusing to replace different bytes: {target}")
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                target.write_bytes(data)
            records.append({"member": name, "bytes": len(data),
                            "sha256": hashlib.sha256(data).hexdigest()})
    target_archive = out / "113382-V1.zip"
    if target_archive.exists() and target_archive.read_bytes() != payload:
        raise ValueError("Existing staged archive differs")
    if not target_archive.exists():
        shutil.copyfile(args.archive, target_archive)
    receipt = {"dataset": "openICPSR113382V1", "verified_local_on": "2026-09-20",
               "official_url": "https://www.openicpsr.org/openicpsr/project/113382/version/V1/view",
               "archive_bytes": len(payload), "archive_sha256": ARCHIVE_SHA,
               "acquisition": "Existing user download; no new agreement accepted by this run",
               "code_license": "BSD-3-Clause", "data_license": "CC-BY-4.0",
               "members": records}
    (out / "acquisition.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
