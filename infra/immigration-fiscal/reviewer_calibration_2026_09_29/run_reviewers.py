"""Bundle the cases per reviewer, write the prompts, and launch the reviewer calls detached.

    uv run --no-project --offline python3 run_reviewers.py build    # prompts/ + prompts/manifest.json only
    uv run --no-project --offline python3 run_reviewers.py freeze   # freeze.json: sha256 of the design files
    uv run --no-project --offline python3 run_reviewers.py launch [--only opus_b3 ...]

Each call runs `llmx chat` in its own session (survives this process), writes the reply to
runs/<reviewer>_b<k>.txt, stderr to .stderr, and `rc= start= end=` to .done. LLMX_CALLER tags
the llmx usage log line so score.py can read tokens per call.
"""
import hashlib
import json
import random
import shlex
import subprocess
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parent
PROMPTS, RUNS = LANE / "prompts", LANE / "runs"
N_BUNDLES, N_ERR, N_VAL = 8, 3, 3

PROMPT_HEAD = """Below are {n} cases. Each case is a claim with the evidence, code or table excerpt behind it. The cases are independent; judge each one on its own.

For each case: Review this claim and its evidence. Is there an error that changes the conclusion? Answer ERROR or SOUND, name the error's location and why, and give your confidence from 0 to 1.

Answer every case, in this exact format:

CASE <id>
VERDICT: ERROR or SOUND
LOCATION: <where the error is, or "none">
WHY: <one to three sentences>
CONFIDENCE: <a number from 0 to 1: your confidence in your verdict>
"""

REVIEWERS = {
    "opus": dict(seed=20260929, model="claude-opus-5-5", effort="max",
                 cmd=["llmx", "chat", "--subscription", "-m", "claude-opus-5-5", "-e", "max",
                      "--timeout", "3600"]),
    "astra": dict(seed=20260930, model="gpt-6-astra", effort="xhigh",
                  cmd=["llmx", "chat", "-p", "codex-cli", "--subscription", "-m", "gpt-6-astra",
                       "-e", "xhigh", "--timeout", "3600"]),
}


def load_cases():
    return [json.loads(p.read_text()) for p in sorted((LANE / "cases").glob("*.json"))]


def opaque_id(seed, cid):
    return "K" + hashlib.sha256(f"{seed}:{cid}".encode()).hexdigest()[:4].upper()


def make_bundles(cases, seed):
    """Stratified bundles (3 ERROR + 3 VALID); no two cases of one topic share a bundle."""
    errs = [c for c in cases if c["type"] == "ERROR"]
    vals = [c for c in cases if c["type"] == "VALID"]
    for attempt in range(2_000_000):
        rng = random.Random(seed * 10_000_000 + attempt)
        e, v = errs[:], vals[:]
        rng.shuffle(e)
        rng.shuffle(v)
        bundles = [e[N_ERR * k:N_ERR * (k + 1)] + v[N_VAL * k:N_VAL * (k + 1)] for k in range(N_BUNDLES)]
        if all(len({c["topic"] for c in b}) == len(b) for b in bundles):
            for b in bundles:
                rng.shuffle(b)
            return bundles, attempt
    raise SystemExit("no bundling satisfies the topic constraint")


def build():
    cases = load_cases()
    for spec in REVIEWERS.values():
        ids = [opaque_id(spec["seed"], c["id"]) for c in cases]
        assert len(set(ids)) == len(ids), "opaque id collision"
    PROMPTS.mkdir(exist_ok=True)
    manifest = {"prompt_head": PROMPT_HEAD, "reviewers": {}}
    for rev, spec in REVIEWERS.items():
        bundles, attempt = make_bundles(cases, spec["seed"])
        entry = {"seed": spec["seed"], "attempt": attempt, "model": spec["model"], "effort": spec["effort"],
                 "cmd": spec["cmd"], "bundles": []}
        for k, b in enumerate(bundles, 1):
            name = f"{rev}_b{k}"
            body = "\n\n".join(f"CASE {opaque_id(spec['seed'], c['id'])}\n{c['packet_text']}" for c in b)
            text = PROMPT_HEAD.format(n=len(b)) + "\n=====\n\n" + body.replace("\n\nCASE ", "\n\n=====\n\nCASE ") + "\n"
            (PROMPTS / f"{name}.txt").write_text(text)
            entry["bundles"].append({"name": name, "cases": [
                {"case_id": c["id"], "reviewer_id": opaque_id(spec["seed"], c["id"])} for c in b]})
        manifest["reviewers"][rev] = entry
    (PROMPTS / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    print(f"built {sum(len(r['bundles']) for r in manifest['reviewers'].values())} prompts")


def freeze():
    files = sorted([*(LANE / "cases").glob("*.json"), *PROMPTS.glob("*"), LANE / "build_cases.py",
                    LANE / "run_reviewers.py", LANE / "RESULT.md"])
    digest = {str(p.relative_to(LANE)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (LANE / "freeze.json").write_text(json.dumps(digest, indent=1) + "\n")
    print(f"froze {len(digest)} files")


def launch(only=None):
    manifest = json.loads((PROMPTS / "manifest.json").read_text())
    RUNS.mkdir(exist_ok=True)
    for rev, entry in manifest["reviewers"].items():
        for b in entry["bundles"]:
            name = b["name"]
            if only and name not in only:
                continue
            out = RUNS / f"{name}.txt"
            if out.exists() and not only:
                print(f"skip {name}: output exists")
                continue
            cmd = " ".join(shlex.quote(x) for x in entry["cmd"])
            script = (f"S=$(date +%s); LLMX_CALLER=reviewer_calibration:{name} {cmd} "
                      f"-o {shlex.quote(str(out))} \"$(cat {shlex.quote(str(PROMPTS / (name + '.txt')))})\" "
                      f"2> {shlex.quote(str(RUNS / (name + '.stderr')))}; "
                      f"echo \"rc=$? start=$S end=$(date +%s)\" > {shlex.quote(str(RUNS / (name + '.done')))}")
            subprocess.Popen(["sh", "-c", script], start_new_session=True, stdin=subprocess.DEVNULL,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=str(LANE))
            print(f"launched {name}")


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "build"
    if action == "build":
        build()
    elif action == "freeze":
        freeze()
    elif action == "launch":
        launch(sys.argv[3:] if len(sys.argv) > 2 and sys.argv[2] == "--only" else None)
    else:
        raise SystemExit(f"unknown action {action}")
