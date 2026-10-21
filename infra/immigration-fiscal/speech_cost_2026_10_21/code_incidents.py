"""Code FIRE Scholars Under Fire (SUF) and Campus Deplatforming records by topic, outcome and direction.

Inputs (ignored `_cache/`, pulled 2026-10-21 through a headless browser session on fire.org, because the
site serves a JavaScript challenge to plain HTTP clients):
  fetch('/api/knack-data?type=scholars&page=0&range=2500&orderby=year&orderdir=desc')
  fetch('/api/knack-data?type=deplatforming&page=0&range=2500&orderby=year&orderdir=desc')
The response is a JSON document; agent-browser `eval` wraps it in one more JSON string layer.
SHA-256 of the pulled files is checked below so a re-pull that changed the records stops loudly.

Topic rules were pre-registered in RESULT.md (2026-10-21 15:10 JST) before any count was seen:
  IMM regex, GRP regex, RACE regex over name + controversy_explanation + FIRE's topic tags.
FIRE's own "Immigration" and "Race" tags are reported beside the regex (FIRE's methodology, Aug 2026 PDF:
"Immigration: Views on immigration, immigration policy, or immigrants."; "Race: ... racial differences,
accusations of racism, antisemitism, etc.").
Direction is FIRE's: "relative to the controversial expression", inferred from the source of the attempt.

    uv run --no-project python3 infra/immigration-fiscal/speech_cost_2026_10_21/code_incidents.py
"""

import collections
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parent
CACHE = LANE / "_cache"
OUT = LANE / "derived"

FILES = {
    "scholars": ("fire_scholars_under_fire_2026-10-21.json",
                 "95f56c63f3afb710d8bdd0a201c634cb0bea929715c0ecd076eac175eb9d1490"),
    "deplatforming": ("fire_campus_deplatforming_2026-10-21.json",
                      "6f58e50bb7630790addef124e49f275d280d67cac68f5515e1080a4cb2a0fc27"),
}

# Pre-registered patterns (RESULT.md, Pre-registration, Q1). Do not edit without a dated RESULT note.
IMM = re.compile(r"immigra|migrant|emigra|refugee|asylum|border|deport|\bICE\b|DACA|undocumented|illegal alien"
                 r"|xenophob|nativis|great replacement|sanctuary|citizenship", re.I)
GRP = re.compile(r"\bIQ\b|intelligence|hereditar|bell curve|eugenic|race science|racial differences"
                 r"|genetic.*(race|group)", re.I)
RACE = re.compile(r"\brac(e|ial|is[mt])|white supremac|black lives|BLM|anti-?black|DEI|diversity", re.I)
# \bICE\b must stay case-sensitive in intent; re.I would match "ice". Apply it separately.
IMM_NO_ICE = re.compile(IMM.pattern.replace(r"|\bICE\b", ""), re.I)
ICE = re.compile(r"\bICE\b")

# Outcomes FIRE codes that are an institutional or outside penalty on the scholar (this lane's grouping,
# not FIRE's). "No sanction", "Reinstatement", "Lawsuit", "Unknown" are not penalties; Resignation is
# reported separately because FIRE's code mixes forced and voluntary exits.
PENALTY = {"Termination", "Suspension", "Demotion", "Censorship", "Investigation", "Scholarship suppression",
           "Training", "Retraction/withdrawal", "Outside sanction"}
SCHOLAR_OUTCOMES = ["Termination", "Suspension", "Demotion", "Investigation", "Censorship",
                    "Scholarship suppression", "Training", "Outside sanction", "Resignation", "Reinstatement",
                    "Lawsuit", "No sanction", "Unknown"]


def load(kind):
    name, sha = FILES[kind]
    raw = (CACHE / name).read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    if got != sha:
        sys.exit(f"[BLOCKED] {name} sha256 {got} != pinned {sha}")
    doc = json.loads(raw)
    if isinstance(doc, str):
        doc = json.loads(doc)
    recs = doc["records"]
    if len(recs) != doc["total"]:
        sys.exit(f"[BLOCKED] {kind}: {len(recs)} records but total {doc['total']}")
    return recs


def flags(r):
    topics = r.get("controversy_topics") or []
    text = " ".join([r.get("name") or "", r.get("controversy_explanation") or "", " ".join(topics)])
    return {
        "imm_tag": "Immigration" in topics,
        "race_tag": "Race" in topics,
        "imm_regex": bool(IMM_NO_ICE.search(text) or ICE.search(text)),
        "grp_regex": bool(GRP.search(text)),
        "race_regex": bool(RACE.search(text)),
    }


def outcomes(r):
    return {o.strip() for o in (r.get("outcome") or "").split(";") if o.strip()}


def write(path, header, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def main():
    OUT.mkdir(exist_ok=True)
    sets = {
        "all": lambda f: True,
        "imm_tag": lambda f: f["imm_tag"],
        "imm_regex": lambda f: f["imm_regex"],
        "imm_tag_and_race_tag": lambda f: f["imm_tag"] and f["race_tag"],
        "race_tag": lambda f: f["race_tag"],
        "grp_regex": lambda f: f["grp_regex"],
        "race_regex": lambda f: f["race_regex"],
    }
    for kind in FILES:
        recs = load(kind)
        coded = [(r, flags(r)) for r in recs]
        # Topic set x direction x outcome (each incident counted once per outcome it carries).
        rows = []
        for sname, pred in sets.items():
            sub = [(r, f) for r, f in coded if pred(f)]
            dirs = collections.Counter(r.get("political_direction") or "" for r, _ in sub)
            for d in ["(any)"] + sorted(dirs):
                dsub = [r for r, _ in sub if d == "(any)" or (r.get("political_direction") or "") == d]
                oc = collections.Counter(o for r in dsub for o in outcomes(r))
                pen = sum(1 for r in dsub if outcomes(r) & PENALTY)
                row = [sname, d, len(dsub), len(recs)]
                if kind == "scholars":
                    row += [pen] + [oc.get(o, 0) for o in SCHOLAR_OUTCOMES]
                else:
                    row += [""] + [oc.get(o, 0) for o in ("Revoked", "Canceled", "Removed", "Withdrew",
                                                         "Postponed", "Substantial Event Disruption",
                                                         "Rejected", "Disinvitation Attempt",
                                                         "Cancellation Attempt", "Attempted Disruption")]
                rows.append(row)
        ohead = (SCHOLAR_OUTCOMES if kind == "scholars" else
                 ["Revoked", "Canceled", "Removed", "Withdrew", "Postponed", "Substantial Event Disruption",
                  "Rejected", "Disinvitation Attempt", "Cancellation Attempt", "Attempted Disruption"])
        write(OUT / f"{kind}_topic_direction_outcome.csv",
              ["topic_set", "direction", "n_incidents", "n_all_incidents", "n_any_penalty"] + ohead, rows)

        # By year: all incidents vs each topic set.
        years = sorted({r["year"] for r in recs})
        yrows = []
        for y in years:
            ys = [(r, f) for r, f in coded if r["year"] == y]
            yrows.append([y] + [sum(1 for _, f in ys if pred(f)) for pred in sets.values()])
        write(OUT / f"{kind}_topic_by_year.csv", ["year"] + [f"n_{s}" for s in sets], yrows)

        # Incident list for the immigration sets, for audit (no reclassification is applied from it).
        irows = []
        for r, f in coded:
            if f["imm_tag"] or f["imm_regex"]:
                irows.append([r["id"], r["year"], r.get("name"), r.get("school_type"),
                              ";".join(r.get("controversy_topics") or []), r.get("political_direction"),
                              r.get("outcome"), int(f["imm_tag"]), int(f["imm_regex"]), int(f["race_tag"]),
                              (r.get("controversy_explanation") or "").replace("\n", " ")[:400]])
        irows.sort(key=lambda x: (-x[1], x[0]))
        write(OUT / f"{kind}_immigration_incidents.csv",
              ["id", "year", "name", "school_type", "fire_topics", "direction", "outcome", "imm_tag",
               "imm_regex", "race_tag", "explanation_400"], irows)
        n_imm = sum(1 for _, f in coded if f["imm_tag"])
        print(f"{kind}: {len(recs)} incidents; FIRE Immigration tag {n_imm}; regex {sum(f['imm_regex'] for _, f in coded)}")


if __name__ == "__main__":
    main()
