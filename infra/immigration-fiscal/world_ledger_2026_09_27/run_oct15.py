"""Run one selected live case on matched cash, preserving every producer exit.

Native-First: the lane's existing commands and exact package-cell export.
"""
import argparse
import json
import subprocess
from pathlib import Path
import phase_c_report
import valuation as V

HERE = Path(__file__).resolve().parent
REL = HERE.relative_to(V.REPO)
PYTHON = ["uv", "run", "--no-project", "python3"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", default="oct16")
    case = parser.parse_args().case
    V.require_pins(case, "main_case", "generation", "winners", "distribution")
    if case != "oct16":
        raise SystemExit(f"[BLOCKED] live case is oct16; {case} outputs are frozen")
    from v9_snapshot import require_adopted, verify
    require_adopted(case)
    verify()
    basis = V.basis_of(case)
    commands = [
        PYTHON + [str(REL / "mexico.py")],
        PYTHON + [str(REL / "employer_ui_basis.py")],
        PYTHON + [str(REL / "v9_transport.py"), "--case", case, "--basis", "cash"],
        PYTHON + [str(REL / "g2_premium.py"), "--basis", basis, "--case", case],
        PYTHON + [str(REL / "weights.py"), "--basis", basis, "--case", case],
        PYTHON + [str(REL / "state_price_quantity.py")],
        PYTHON + [str(REL / "pension_cash.py"), "--case", case, "--verify-artifact"],
        PYTHON + [str(REL / "coverage_recipient_values.py"), "--case", case, "--basis", "cash"],
        PYTHON + [str(REL / "cash_readings.py"), "--case", case, "--prepare"],
        PYTHON + [str(REL / "cash_readings.py"), "--case", case],
        PYTHON + [str(REL / "phase_c_report.py"), "--case", case],
    ]
    cache = HERE / "_cache"
    cache.mkdir(exist_ok=True)
    completed, result = [], 0
    for index, command in enumerate(commands):
        path = cache / f"{case}_stage_{index:02d}.log"
        with path.open("w") as stream:
            proc = subprocess.run(PYTHON + [str(REL / "measured_run.py"), *command], stdout=stream,
                                  stderr=subprocess.STDOUT)
        completed.append(dict(command=command, exit_code=proc.returncode, log=str(path.relative_to(HERE))))
        print(f"[{case}] rc={proc.returncode}: {' '.join(command)}", flush=True)
        if proc.returncode:
            print("\n".join(path.read_text().splitlines()[-12:]), flush=True)
            result = proc.returncode
            break
    record = dict(case=case, basis="matched_cash", status="PASS" if result == 0 else "[BLOCKED] route did not finish",
                  executed=completed, pending=commands[len(completed):], exit_code=result)
    (HERE / f"derived/route_{case}.json").write_text(json.dumps(record, indent=1, sort_keys=True) + "\n")
    verify()
    return result


if __name__ == "__main__":
    raise SystemExit(main())
