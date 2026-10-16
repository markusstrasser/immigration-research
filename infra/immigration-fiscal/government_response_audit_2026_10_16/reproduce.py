"""Replay original inputs, then price only general-public-services response on frozen v9."""
import argparse
import importlib.util
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CASE = "a24d2468ed51d37ae4919fcec55ba153a343a5e1"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=ROOT)
    parser.add_argument("--out-dir", type=Path, default=HERE / "derived")
    args = parser.parse_args()
    data, output = args.data_root.resolve(), args.out_dir.resolve()
    env = {**os.environ, "OPENBLAS_NUM_THREADS": "1"}
    for script in ["raw_finance.py", "employment.py"]:
        subprocess.run([sys.executable, str(HERE / script), "--data-root", str(data),
                        "--out-dir", str(output)], check=True, env=env)
    prior = HERE.parent / "school_response_audit_2026_10_15/reproduce.py"
    spec = importlib.util.spec_from_file_location("frozen_case_inputs", prior)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    with tempfile.TemporaryDirectory(prefix="government-audit-v9-") as folder:
        scratch = Path(folder)
        archive, case_root = scratch / "case.tar", scratch / "case"
        case_root.mkdir()
        subprocess.run(["git", "-C", str(ROOT), "archive", "--format=tar",
                        "--output", str(archive), CASE], check=True)
        subprocess.run(["tar", "-xf", str(archive), "-C", str(case_root)], check=True)
        objects = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse",
                                           "--path-format=absolute", "--git-path", "objects"], text=True).strip()
        subprocess.run(["git", "-C", str(case_root), "init", "--quiet"], check=True)
        (case_root / ".git/objects/info/alternates").write_text(objects + "\n")
        subprocess.run(["git", "-C", str(case_root), "update-ref", "--no-deref", "HEAD", CASE], check=True)
        subprocess.run(["git", "-C", str(case_root), "read-tree", CASE], check=True)
        helper.copy_principal_inputs(data, case_root)
        subprocess.run(["node", str(HERE / "price.cjs"), "--case-root", str(case_root),
                        "--out-dir", str(output)], check=True, env=env)


if __name__ == "__main__":
    main()
