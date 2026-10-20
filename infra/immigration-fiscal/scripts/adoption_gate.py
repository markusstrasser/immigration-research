"""Use the same live declaration/package adoption check as Node consumers."""
import json
from pathlib import Path
import subprocess


def require_adopted(key, live_path=None):
    command = ["node", str(Path(__file__).with_suffix(".cjs")), key]
    if live_path is not None:
        command.append(str(live_path))
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        raise SystemExit("[BLOCKED] adoption check failed: " + result.stderr.strip())
    return json.loads(result.stdout)
