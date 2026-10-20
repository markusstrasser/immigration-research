"""Rebuild the live account's retained measured source-replicate stacks.

Native-First: invoke the existing exporter and account evaluator in bounded processes.
"""
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent


def main():
    for basis in ("set", "cash"):
        env = {**os.environ, "UNCERTAINTY_ACCOUNT_CORE": "1", "UNCERTAINTY_BASIS": basis,
               "OPENBLAS_NUM_THREADS": "1", "PYTHONDONTWRITEBYTECODE": "1"}
        subprocess.run(["node", str(HERE/"sept24_specs.cjs")], check=True, env=env)
        subprocess.run([sys.executable, str(HERE/"propagate.py"), "--case", "oct16",
                        "--coverage-pes-rule", "common_nce_source"], check=True, env=env)


if __name__ == "__main__":
    main()
