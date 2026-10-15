"""Reproduce the audit using original local data and the committed v9 candidate."""
import argparse
import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CASE = "fb822a950085142ac424477297902762b4e446ba"
BASE_INPUTS = {
    "infra/immigration-fiscal/assumption_explorer_2026_09_21/derived/model.json": "c659b9d89a415c5794ee49422711bb7c6bb13c1fd0b345617ac42cd188fc14dd",
    "infra/immigration-fiscal/assumption_explorer_2026_09_21/derived/scaling_check.json": "7ecccd9c803813b5f34c3336a41355228180d6bababa747a04d2bc25218ba795",
    "infra/immigration-fiscal/union_completion_2026_10_14/_cache/cash/oct14/lines.json": "3df4a72d2ee21eb8d6ba1e3be42ec00f441d0b13dd43b6a3b422c10f64e3dd30",
    "infra/immigration-fiscal/union_completion_2026_10_14/_cache/set/oct14/lines.json": "00a5d68278ca8fb2d99ed2db3197c3eddf5d4fe338a03cb8f8f7dc8840462d38",
}


def copy_principal_inputs(data, case_root):
    for relative, expected in BASE_INPUTS.items():
        source = data / relative
        if not source.is_file():
            raise ValueError(f"[BLOCKED] missing frozen-case input: {relative}")
        payload = source.read_bytes()
        if hashlib.sha256(payload).hexdigest() != expected:
            raise ValueError(f"[BLOCKED] changed frozen-case input: {relative}")
        target = case_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=ROOT)
    parser.add_argument("--out-dir", type=Path, default=HERE / "derived")
    args = parser.parse_args()
    env = {**os.environ, "OPENBLAS_NUM_THREADS": "1"}
    data, output = args.data_root.resolve(), args.out_dir.resolve()
    for script in [HERE / "raw_audit.py", HERE / "wage_check.py"]:
        subprocess.run([sys.executable, str(script), "--data-root", str(data),
                        "--out-dir", str(output)], check=True, env=env)
    # Export tracked bytes only. No reset, new branch, or dependence on peers' edits.
    with tempfile.TemporaryDirectory(prefix="school-audit-v9-") as folder:
        scratch = Path(folder)
        archive, case_root = scratch / "case.tar", scratch / "case"
        case_root.mkdir()
        subprocess.run(["git", "-C", str(ROOT), "archive", "--format=tar",
                        "--output", str(archive), CASE], check=True)
        subprocess.run(["tar", "-xf", str(archive), "-C", str(case_root)], check=True)
        # The model reads older pinned objects with git show. Give the export a
        # detached HEAD and its own index, borrowing the source object store only.
        objects = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse",
                                           "--path-format=absolute", "--git-path", "objects"], text=True).strip()
        subprocess.run(["git", "-C", str(case_root), "init", "--quiet"], check=True)
        (case_root / ".git/objects/info/alternates").write_text(objects + "\n")
        subprocess.run(["git", "-C", str(case_root), "update-ref", "--no-deref", "HEAD", CASE], check=True)
        subprocess.run(["git", "-C", str(case_root), "read-tree", CASE], check=True)
        copy_principal_inputs(data, case_root)
        subprocess.run(["node", str(HERE / "price.cjs"), "--case-root", str(case_root),
                        "--out-dir", str(output)], check=True, env=env)


if __name__ == "__main__":
    main()
