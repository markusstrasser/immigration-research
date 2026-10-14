"""Preserve the committed oct14 positive control without modifying Git metadata."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BASE = HERE / "_cache/p7_baseline"


def main():
    BASE.mkdir(parents=True, exist_ok=True)
    paths = subprocess.run(
        ["git", "-C", str(REPO), "ls-tree", "-r", "--name-only", "0b41a200", "--", str(HERE.relative_to(REPO))],
        capture_output=True, check=True, text=True).stdout.splitlines()
    pins = {}
    for name in paths:
        rel = Path(name).relative_to(HERE.relative_to(REPO))
        if rel.parts[0] != "derived":
            continue
        raw = subprocess.run(["git", "-C", str(REPO), "show", f"0b41a200:{name}"],
                             capture_output=True, check=True).stdout
        target = BASE / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        pins[str(rel)] = hashlib.sha256(raw).hexdigest()
    (BASE / "manifest.json").write_text(json.dumps(pins, indent=2, sort_keys=True) + "\n")
    print(f"Pinned committed positive control: {len(pins)} files at 0b41a200")


if __name__ == "__main__":
    main()
