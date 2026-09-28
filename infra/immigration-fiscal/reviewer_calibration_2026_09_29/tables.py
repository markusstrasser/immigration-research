"""Render derived/summary.json as markdown tables -> derived/tables.md (deterministic)."""
import json
from pathlib import Path

LANE = Path(__file__).resolve().parent
S = json.loads((LANE / "derived" / "summary.json").read_text())


def r(x):
    if x["n"] == 0:
        return "n/a"
    lo, hi = x["wilson95"]
    return f"{x['k']}/{x['n']} = {x['rate']:.2f} ({lo:.2f}-{hi:.2f})"


def d(x):
    return "n/a" if x is None else f"{x['diff']:+.2f} ({x['newcombe95'][0]:+.2f} to {x['newcombe95'][1]:+.2f})"


out = ["## Rates (Wilson 95% intervals)", "",
       "| Reviewer | Slice | Hit (right locus) | Flag (any ERROR on an ERROR case) | False accusation | ERROR verdicts, all cases |",
       "|---|---|---|---|---|---|"]
for rev, s in S["reviewers"].items():
    slices = [("all", s)] + [(f"dir {k}", v) for k, v in s["by_direction"].items()] + \
             [(k, v) for k, v in s["by_origin"].items()] + [(k, v) for k, v in s["by_direction_origin"].items()]
    for name, b in slices:
        out.append(f"| {rev} | {name} | {r(b['hit'])} | {r(b['flag'])} | {r(b['false_accusation'])} | {r(b['error_verdict_all'])} |")
out += ["", "## Direction effect, R minus E (Newcombe 95%), and paired mirror sign tests", "",
        "| Reviewer | Hit | Flag | False accusation | ERROR verdicts, all | Pairs: hit (R-only/E-only, p) | Pairs: accusation (R-only/E-only, p) |",
        "|---|---|---|---|---|---|---|"]
for rev, s in S["reviewers"].items():
    e, p = s["direction_effect_R_minus_E"], s["paired_mirror_sign_test"]
    out.append(f"| {rev} | {d(e['hit'])} | {d(e['flag'])} | {d(e['false_accusation'])} | {d(e['error_verdict_all'])} | "
               f"{p['hit']['r_side_only']}/{p['hit']['e_side_only']}, p={p['hit']['p_two_sided']} of {p['hit']['pairs']} | "
               f"{p['false_accusation']['r_side_only']}/{p['false_accusation']['e_side_only']}, p={p['false_accusation']['p_two_sided']} of {p['false_accusation']['pairs']} |")
out += ["", "## Calibration", "", "| Reviewer | n | Brier | Mean confidence | Verdict accuracy | Bins (n, mean conf, accuracy) |",
        "|---|---|---|---|---|---|"]
for rev, s in S["reviewers"].items():
    c = s["calibration"]
    bins = "; ".join(f"{k}: {v['n']}, {v['mean_confidence']:.2f}, {v['accuracy']:.2f}" for k, v in c["bins"].items())
    out.append(f"| {rev} | {c['n']} | {c['brier']:.3f} | {c['mean_confidence']:.2f} | {c['verdict_accuracy']:.2f} | {bins} |")
out += ["", "## Cost per arm", "", "| Arm | Calls | Prompt tok | Cached tok | Output tok | Reasoning tok | Usage lines | Wall s (sum / max) |",
        "|---|---|---|---|---|---|---|---|"]
for rev, c in S["costs"].items():
    out.append(f"| {rev} | {c['calls']} | {c['prompt_tokens']:,} | {c['cached_tokens']:,} | {c['completion_tokens']:,} | "
               f"{c['reasoning_tokens']:,} | {c['usage_lines']} | {c['wall_s_sum']} / {c['wall_s_max']} |")
(LANE / "derived" / "tables.md").write_text("\n".join(out) + "\n")
print("wrote derived/tables.md")
