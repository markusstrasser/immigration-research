"""One exact-byte guard for committed oct15 input files, including tamper checks."""
import hashlib
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]


def checked_bytes(commit, relative, repo=REPO):
    if commit == "WORKTREE_SHA256_OCT16":
        record = __import__("json").loads((Path(__file__).parent / "inputs/oct16_source_hashes.json").read_text())
        if record.get("case") != "oct16" or record.get("provenance") != "[WORKTREE INPUT]":
            raise SystemExit("[BLOCKED] oct16 worktree snapshot identity")
        path = repo / relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != record["sha256"].get(relative):
            raise SystemExit(f"[BLOCKED] stale or undeclared oct16 worktree input: {relative}")
        return path.read_bytes()
    if not commit or commit == "WORKTREE_SHA256":
        raise SystemExit(f"[BLOCKED] committed input required: {relative}")
    result = subprocess.run(["git", "-C", str(repo), "show", f"{commit}:{relative}"],
                            capture_output=True)
    if result.returncode:
        raise SystemExit(f"[BLOCKED] missing input at {commit}: {relative}")
    path = repo / relative
    if not path.is_file() or path.read_bytes() != result.stdout:
        raise SystemExit(f"[BLOCKED] pin does not match file: {commit}:{relative}")
    return result.stdout


def file_receipt(commit, relative):
    body = checked_bytes(commit, relative)
    return dict(commit=commit, path=relative, sha256=hashlib.sha256(body).hexdigest())
