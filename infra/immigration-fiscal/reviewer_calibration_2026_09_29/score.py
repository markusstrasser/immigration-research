"""Score the reviewer runs against the case bank.

    uv run --no-project --offline python3 score.py collect   # snapshot tagged llmx usage lines -> runs/usage.jsonl
    uv run --no-project --offline python3 score.py pending   # list verdicts that still need a grade
    uv run --no-project --offline python3 score.py           # derived/scores.csv, derived/summary.json

Scoring reads only cases/, prompts/manifest.json, runs/ and grades/, so it reruns byte-identically.
"""
import csv
import json
import math
import re
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parent
REVIEWERS = ("opus", "astra")
USAGE_LOG = Path.home() / ".claude" / "llmx-usage.jsonl"
Z = 1.959963984540054
FIELDS = ("VERDICT", "LOCATION", "WHY", "CONFIDENCE")
LABEL = re.compile(r"^[\s*_>#`-]*(VERDICT|LOCATION|WHY|CONFIDENCE)[\s*_`]*:[\s*_`]*", re.I | re.M)
CASE_HEAD = re.compile(r"^[\s*_>#`-]*CASE[\s*_`]+(K[0-9A-F]{4})\b", re.M)


def load_cases():
    return {c["id"]: c for c in (json.loads(p.read_text()) for p in sorted((LANE / "cases").glob("*.json")))}


def parse_run(text):
    """Return {reviewer_id: {field: value}} for the first block of each case that carries a verdict."""
    heads = list(CASE_HEAD.finditer(text))
    out = {}
    for i, m in enumerate(heads):
        block = text[m.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        labels = list(LABEL.finditer(block))
        fields = {}
        for j, lab in enumerate(labels):
            val = block[lab.end():labels[j + 1].start() if j + 1 < len(labels) else len(block)]
            fields.setdefault(lab.group(1).upper(), " ".join(val.replace("*", " ").split()))
        verdict = re.match(r"(ERROR|SOUND)\b", fields.get("VERDICT", ""), re.I)
        if not verdict or m.group(1) in out:
            continue
        conf = re.search(r"\d*\.?\d+", fields.get("CONFIDENCE", ""))
        c = float(conf.group(0)) if conf else None
        if c is not None and c > 1:  # a percentage
            c = c / 100.0
        out[m.group(1)] = {"verdict": verdict.group(1).upper(), "location": fields.get("LOCATION", ""),
                           "why": fields.get("WHY", ""), "confidence": c}
    return out


def read_grades(name, keycols):
    path = LANE / "grades" / name
    if not path.exists():
        return {}
    with path.open(newline="") as f:
        return {tuple(r[k] for k in keycols): r for r in csv.DictReader(f)}


def build_rows(cases, manifest):
    locus = read_grades("locus_grades.csv", ("reviewer", "case_id"))
    audit = read_grades("accusation_audit.csv", ("reviewer", "case_id"))
    rows, missing = [], []
    for rev in REVIEWERS:
        for b in manifest["reviewers"][rev]["bundles"]:
            path = LANE / "runs" / f"{b['name']}.txt"
            parsed = parse_run(path.read_text()) if path.exists() else {}
            for entry in b["cases"]:
                case = cases[entry["case_id"]]
                p = parsed.get(entry["reviewer_id"])
                row = {"reviewer": rev, "case_id": case["id"], "reviewer_id": entry["reviewer_id"],
                       "bundle": b["name"], "type": case["type"], "direction": case["direction"],
                       "origin": case["origin"], "topic": case["topic"], "verdict": "", "confidence": "",
                       "p_error": "", "locus_grade": "", "packet_defect": "", "outcome": "unparsed",
                       "location": "", "why": ""}
                if p:
                    row.update(verdict=p["verdict"], location=p["location"], why=p["why"])
                    if p["confidence"] is not None:
                        c = p["confidence"]
                        row["confidence"] = f"{c:.2f}"
                        row["p_error"] = f"{(c if p['verdict'] == 'ERROR' else 1 - c):.2f}"
                    key = (rev, case["id"])
                    if case["type"] == "ERROR":
                        if p["verdict"] == "SOUND":
                            row["outcome"] = "miss"
                        elif key in locus:
                            g = locus[key]["grade"]
                            assert g in ("HIT", "WRONG"), (key, g)
                            row["locus_grade"] = g
                            row["outcome"] = "hit" if g == "HIT" else "wrong_locus"
                        else:
                            missing.append(("locus", rev, case["id"]))
                    else:
                        if p["verdict"] == "SOUND":
                            row["outcome"] = "correct_pass"
                        else:
                            row["outcome"] = "false_accusation"
                            if key in audit:
                                assert audit[key]["packet_defect"] in ("yes", "no"), key
                                row["packet_defect"] = audit[key]["packet_defect"]
                            else:
                                missing.append(("audit", rev, case["id"]))
                rows.append(row)
    return rows, missing


def wilson(k, n):
    if n == 0:
        return [None, None]
    p = k / n
    den = 1 + Z * Z / n
    mid = (p + Z * Z / (2 * n)) / den
    half = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / den
    return [round(max(0.0, mid - half), 4), round(min(1.0, mid + half), 4)]


def rate(k, n):
    return {"k": k, "n": n, "rate": round(k / n, 4) if n else None, "wilson95": wilson(k, n)}


def newcombe(k1, n1, k2, n2):
    """Hybrid-score interval for p1 - p2 (Newcombe 1998, method 10)."""
    if not n1 or not n2:
        return None
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson(k1, n1)
    l2, u2 = wilson(k2, n2)
    d = p1 - p2
    return {"diff": round(d, 4), "newcombe95": [round(d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2), 4),
                                                round(d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2), 4)]}


def sign_test(b, c):
    n, k = b + c, min(b, c)
    p = min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n) if n else 1.0
    return {"r_side_only": b, "e_side_only": c, "p_two_sided": round(p, 4)}


def block(rows):
    parsed = [r for r in rows if r["outcome"] != "unparsed"]
    err = [r for r in parsed if r["type"] == "ERROR"]
    val = [r for r in parsed if r["type"] == "VALID"]
    hits = sum(r["outcome"] == "hit" for r in err)
    flags = sum(r["verdict"] == "ERROR" for r in err)
    acc = sum(r["verdict"] == "ERROR" for r in val)
    return {"n_rows": len(rows), "unparsed": len(rows) - len(parsed),
            "hit": rate(hits, len(err)), "flag": rate(flags, len(err)),
            "wrong_locus": sum(r["outcome"] == "wrong_locus" for r in err),
            "false_accusation": rate(acc, len(val)),
            "error_verdict_all": rate(sum(r["verdict"] == "ERROR" for r in parsed), len(parsed))}


def direction_effects(rows):
    parsed = [r for r in rows if r["outcome"] != "unparsed"]
    out = {}
    for label, typ, success in (("hit", "ERROR", lambda r: r["outcome"] == "hit"),
                                ("flag", "ERROR", lambda r: r["verdict"] == "ERROR"),
                                ("false_accusation", "VALID", lambda r: r["verdict"] == "ERROR"),
                                ("error_verdict_all", None, lambda r: r["verdict"] == "ERROR")):
        sub = [r for r in parsed if typ is None or r["type"] == typ]
        rr = [r for r in sub if r["direction"] == "R"]
        ee = [r for r in sub if r["direction"] == "E"]
        out[label] = newcombe(sum(map(success, rr)), len(rr), sum(map(success, ee)), len(ee))
    return out


def paired(rows, cases):
    by = {(r["reviewer"], r["case_id"]): r for r in rows}
    out = {}
    for typ, label, success in (("ERROR", "hit", lambda r: r["outcome"] == "hit"),
                                ("ERROR", "flag", lambda r: r["verdict"] == "ERROR"),
                                ("VALID", "false_accusation", lambda r: r["verdict"] == "ERROR")):
        b = c = usable = 0
        for rev in sorted({r["reviewer"] for r in rows}):
            for cid, case in sorted(cases.items()):
                if case["origin"] != "original" or case["type"] != typ:
                    continue
                pair = [by.get((rev, cid)), by.get((rev, cid + "m"))]
                if any(p is None or p["outcome"] == "unparsed" for p in pair):
                    continue
                usable += 1
                r_side = next(p for p in pair if p["direction"] == "R")
                e_side = next(p for p in pair if p["direction"] == "E")
                b += success(r_side) and not success(e_side)
                c += success(e_side) and not success(r_side)
        out[label] = {"pairs": usable, **sign_test(b, c)}
    return out


def calibration(rows):
    scored = [r for r in rows if r["outcome"] != "unparsed" and r["confidence"] != ""]
    if not scored:
        return None
    brier = sum((float(r["p_error"]) - (r["type"] == "ERROR")) ** 2 for r in scored) / len(scored)
    correct = lambda r: (r["verdict"] == "ERROR") == (r["type"] == "ERROR")
    bins = {}
    for lo, hi, name in ((0, .5, "<0.5"), (.5, .7, "0.5-0.7"), (.7, .9, "0.7-0.9"), (.9, 1.01, "0.9-1")):
        sub = [r for r in scored if lo <= float(r["confidence"]) < hi]
        if sub:
            bins[name] = {"n": len(sub), "mean_confidence": round(sum(float(r["confidence"]) for r in sub) / len(sub), 4),
                          "accuracy": round(sum(map(correct, sub)) / len(sub), 4)}
    return {"n": len(scored), "brier": round(brier, 4),
            "mean_confidence": round(sum(float(r["confidence"]) for r in scored) / len(scored), 4),
            "verdict_accuracy": round(sum(map(correct, scored)) / len(scored), 4), "bins": bins}


def costs(manifest):
    usage_path = LANE / "runs" / "usage.jsonl"
    usage = [json.loads(line) for line in usage_path.read_text().splitlines()] if usage_path.exists() else []
    out = {}
    for rev in REVIEWERS:
        names = [b["name"] for b in manifest["reviewers"][rev]["bundles"]]
        tot = {"calls": 0, "prompt_tokens": 0, "completion_tokens": 0, "reasoning_tokens": 0, "cached_tokens": 0,
               "usage_lines": 0, "wall_s_sum": 0, "wall_s_max": 0, "failed_calls": 0}
        for name in names:
            done = LANE / "runs" / f"{name}.done"
            if done.exists():
                kv = dict(x.split("=") for x in done.read_text().split())
                wall = int(kv["end"]) - int(kv["start"])
                tot["calls"] += 1
                tot["failed_calls"] += kv["rc"] != "0"
                tot["wall_s_sum"] += wall
                tot["wall_s_max"] = max(tot["wall_s_max"], wall)
            for u in usage:
                if u.get("caller") == f"reviewer_calibration:{name}":
                    tot["usage_lines"] += 1
                    for k in ("prompt_tokens", "completion_tokens", "reasoning_tokens", "cached_tokens"):
                        tot[k] += u.get(k) or 0
        out[rev] = tot
    return out


def collect():
    """Snapshot token usage. Claude lines come from the llmx usage log by caller tag. For codex-cli,
    llmx attributes rollouts by start time, which mixes up calls launched in the same second (its
    astra lines name another call's rollout); so astra tokens are read from the codex rollouts
    themselves, matched to bundles by the case ids in the prompt."""
    manifest = json.loads((LANE / "prompts" / "manifest.json").read_text())
    lines = [json.loads(line) for line in USAGE_LOG.read_text().splitlines() if '"reviewer_calibration:' in line]
    out = [u for u in lines if not u["caller"].startswith("reviewer_calibration:astra_")]
    bundles = {b["name"]: {c["reviewer_id"] for c in b["cases"]} for b in manifest["reviewers"]["astra"]["bundles"]}
    for path in sorted((Path.home() / ".codex" / "sessions").rglob("rollout-2026-09-29T01-*.jsonl")):
        text = path.read_text()
        ids = set(re.findall(r"CASE (K[0-9A-F]{4})", text))
        name = next((n for n, s in bundles.items() if s == ids), None)
        events = [json.loads(line) for line in text.splitlines() if '"token_count"' in line]
        events = [e for e in events if (e.get("payload") or {}).get("info")]
        if name is None or not events:
            continue
        tot = events[-1]["payload"]["info"]["total_token_usage"]
        out.append({"caller": f"reviewer_calibration:{name}", "model": "gpt-6-astra", "source": f"codex rollout {path.name}",
                    "prompt_tokens": tot["input_tokens"], "completion_tokens": tot["output_tokens"],
                    "reasoning_tokens": tot["reasoning_output_tokens"], "cached_tokens": tot["cached_input_tokens"],
                    "total_tokens": tot["total_tokens"]})
    out.sort(key=lambda u: u["caller"])
    (LANE / "runs" / "usage.jsonl").write_text("".join(json.dumps(u, sort_keys=True) + "\n" for u in out))
    print(f"collected {len(out)} usage lines")


def main():
    cases = load_cases()
    manifest = json.loads((LANE / "prompts" / "manifest.json").read_text())
    rows, missing = build_rows(cases, manifest)
    if sys.argv[1:] == ["pending"]:  # grouped by case, so grading goes case by case
        last = None
        for kind, rev, cid in sorted(missing, key=lambda m: (m[2], m[1])):
            if cid != last:
                print(f"\n## {cid} [{cases[cid]['type']} {cases[cid]['direction']}] RUBRIC: {cases[cid]['locus_rubric'][:400]}")
                last = cid
            r = next(x for x in rows if x["reviewer"] == rev and x["case_id"] == cid)
            print(f"- {kind} {rev} conf={r['confidence']} LOC: {r['location']} | WHY: {r['why']}")
        return
    if missing:
        raise SystemExit(f"[BLOCKED] {len(missing)} grades missing; run `score.py pending`")
    rows.sort(key=lambda r: (r["reviewer"], r["case_id"]))
    (LANE / "derived").mkdir(exist_ok=True)
    with (LANE / "derived" / "scores.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    summary = {"reviewers": {}}
    for name, sub in [(rev, [r for r in rows if r["reviewer"] == rev]) for rev in REVIEWERS] + [("pooled", rows)]:
        s = block(sub)
        s["by_direction"] = {d: block([r for r in sub if r["direction"] == d]) for d in ("R", "E")}
        s["by_origin"] = {o: block([r for r in sub if r["origin"] == o]) for o in ("original", "mirror")}
        s["by_direction_origin"] = {f"{d}_{o}": block([r for r in sub if r["direction"] == d and r["origin"] == o])
                                    for d in ("R", "E") for o in ("original", "mirror")}
        s["direction_effect_R_minus_E"] = direction_effects(sub)
        s["paired_mirror_sign_test"] = paired(sub, cases)
        s["calibration"] = calibration(sub)
        clean = [r for r in sub if r["packet_defect"] != "yes"]
        s["sensitivity_drop_packet_defects"] = {"false_accusation": block(clean)["false_accusation"],
                                                "direction_effect_R_minus_E": direction_effects(clean)}
        summary["reviewers"][name] = s
    summary["costs"] = costs(manifest)
    (LANE / "derived" / "summary.json").write_text(json.dumps(summary, indent=1, sort_keys=True) + "\n")
    print("wrote derived/scores.csv and derived/summary.json")


if __name__ == "__main__":
    if sys.argv[1:] == ["collect"]:
        collect()
    else:
        main()
