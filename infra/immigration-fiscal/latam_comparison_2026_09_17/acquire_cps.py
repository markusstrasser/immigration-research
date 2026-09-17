#!/usr/bin/env python3
"""Acquire only the missing 2022/23 public ASEC releases, with provenance."""
import argparse
import hashlib
import json
import shutil
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def acquire(url, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(request, timeout=60) as response:
        headers = dict(response.headers)
        size = response.headers.get("Content-Length")
    if not path.exists():
        temporary = path.with_suffix(path.suffix + ".partial")
        with urllib.request.urlopen(url, timeout=180) as response, temporary.open("wb") as stream:
            shutil.copyfileobj(response, stream)
        if size is not None and temporary.stat().st_size != int(size):
            raise ValueError(f"Download length mismatch: {url}")
        temporary.rename(path)
    if size is not None and path.stat().st_size != int(size):
        raise ValueError(f"Existing file differs from server length: {path}")
    if path.suffix == ".pdf" and not path.read_bytes().startswith(b"%PDF"):
        raise ValueError(f"Not a PDF: {path}")
    members = None
    if path.suffix in {".zip", ".docx"}:
        with zipfile.ZipFile(path) as archive:
            if archive.testzip() is not None:
                raise ValueError(f"Bad ZIP CRC: {path}")
            members = archive.namelist()
    result = dict(url=url, path=str(path.resolve()), bytes=path.stat().st_size,
                  sha256=digest(path), checked_utc=datetime.now(timezone.utc).isoformat(),
                  content_type=headers.get("Content-Type", headers.get("content-type")),
                  members=members)
    print(json.dumps(result), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["docs", "data"], required=True)
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "_cache")
    args = parser.parse_args()
    manifest_path = args.output / "acquisition.json"
    records = json.loads(manifest_path.read_text()) if manifest_path.exists() else []
    for year in [2022, 2023]:
        base = f"https://www2.census.gov/programs-surveys/cps/datasets/{year}/march/"
        folder = args.output / str(year)
        if args.phase == "docs":
            names = [f"asec{year}_ddl_pub_full.pdf",
                     f"{year}_ASEC_Replicate_Weight_Usage_Instructions.docx"]
        else:
            if not (folder / f"asec{year}_ddl_pub_full.pdf").exists():
                raise ValueError("Acquire and read documentation before bulk files")
            names = [f"asecpub{year % 100}csv.zip"]
        for name in names:
            record = acquire(base + name, folder / name)
            records = [r for r in records if r["url"] != record["url"]] + [record]
            manifest_path.write_text(json.dumps(records, indent=2) + "\n")
    lines = ["# Acquired public CPS files", "", "Government public-use releases; retrieved without account or payment.", ""]
    for record in records:
        lines.extend([f"- {record['path']}", f"  - URL: {record['url']}",
                      f"  - Checked UTC: {record['checked_utc']}",
                      f"  - Bytes: {record['bytes']}; SHA256: {record['sha256']}"])
    (args.output / "ACQUIRED.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
