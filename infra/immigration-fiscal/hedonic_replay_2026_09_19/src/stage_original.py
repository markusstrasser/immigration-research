"""Validate and preserve the operator-authorized ICPSR V1 ZIP without executing it."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

LANE = Path(__file__).resolve().parents[1]
ARCHIVE_SHA256 = "5315ad6e4118accafc94a0aad8fb923441c86ed6b21d5f8da75d44ee66e42a41"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    if args.archive.suffix != ".zip":
        raise ValueError("Use the completed ZIP, not a browser partial download")
    if sha(args.archive) != ARCHIVE_SHA256:
        raise ValueError("Archive does not match the acquired ICPSR V1 bytes; review provenance")
    cache = LANE / "_cache"
    target = cache / "original.zip"
    extracted = cache / "original"
    with zipfile.ZipFile(args.archive) as z:
        if z.testzip() is not None:
            raise ValueError("Archive CRC validation failed")
        members = z.infolist()
        if sum(m.file_size for m in members) > 1_000_000_000:
            raise ValueError("Unexpected archive size: review contents before staging")
        for m in members:
            p = Path(m.filename)
            if p.is_absolute() or ".." in p.parts:
                raise ValueError(f"Unsafe archive path: {m.filename}")
        cache.mkdir(exist_ok=True)
        if target.exists() and sha(target) != sha(args.archive):
            raise ValueError("Refusing to overwrite a different original archive")
        if not target.exists():
            shutil.copyfile(args.archive, target)
        files = []
        for m in members:
            if m.is_dir():
                continue
            p = extracted / m.filename
            payload = z.read(m)
            if p.exists() and p.read_bytes() != payload:
                raise ValueError(f"Refusing to overwrite changed source: {p}")
            p.parent.mkdir(parents=True, exist_ok=True)
            if not p.exists():
                p.write_bytes(payload)
            files.append({"path": str(p.relative_to(LANE)), "bytes": len(payload), "sha256": sha(p)})
    manifest = {"source": "https://doi.org/10.3886/E114757V1", "acquired": "2026-09-19",
                "archive_bytes": target.stat().st_size, "archive_sha256": sha(target), "files": files}
    (LANE / "derived").mkdir(exist_ok=True)
    (LANE / "derived/source_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
