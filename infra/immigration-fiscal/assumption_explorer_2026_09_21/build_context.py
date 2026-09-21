"""Turn an agent-made inventory of executed results into context.json, keeping only what re-verifies.

Usage: build_context.py <ledger_map.json>. A value survives only if its digits are found within two
lines of the file:line the inventory cites; an item survives only with a memo and one surviving value.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def numbers(text):
    """Unsigned number tokens as printed, thousands separators removed."""
    return re.findall(r"\d+(?:\.\d+)?", str(text).replace(",", ""))


def confirmed(value, ref):
    """Every number in the recorded value equals, at its own printed precision, a number printed
    within two lines of the cited file:line (a range `a-b` or list `a,b` of lines widens the window).
    A range, pair or before/after string is therefore checked number by number, and a CSV cell with
    more decimals than the memo confirms the memo's rounding. Signs are not compared."""
    match = re.match(r"(.+?):(\d+)((?:\s*[-,]\s*\d+)*)", str(ref or ""))
    if not match or not (ROOT/match.group(1)).is_file():
        return False
    cited = [int(match.group(2))]+[int(n) for n in re.findall(r"\d+", match.group(3))]
    lines = (ROOT/match.group(1)).read_text(errors="replace").splitlines()
    window = " ".join(lines[max(0, min(cited)-3):max(cited)+2])
    if match.group(1).endswith(".csv"):
        window = window.replace(",", " ")  # field separators here, never thousands separators
    printed = [float(n) for n in numbers(window)]
    wanted = numbers(repr(abs(value)) if isinstance(value, (int, float)) else value)
    if not wanted:
        return str(value)[:12] in window
    for token in wanted:
        places = len(token.split(".")[1]) if "." in token else 0
        if not any(abs(round(x, places)-float(token)) < 0.5*10**-places for x in printed):
            return False
    return True


def main():
    source = json.loads(Path(sys.argv[1]).read_text())
    items, dropped_values, dropped_items = [], 0, []
    for item in source["items"]:
        values = []
        for v in item.get("values") or []:
            if confirmed(v.get("value"), v.get("file_line")):
                values.append({k: v.get(k) for k in ["label", "value", "unit", "se", "file_line"]})
            else:
                dropped_values += 1
        if not values or not item.get("memo"):
            dropped_items.append(item["id"])
            continue
        items.append(dict(id=item["id"], faq_entry=item.get("faq_entry"), objection=item.get("objection"),
                          finding=item.get("finding"), values=values[:5], relation_to_headline=item["relation_to_headline"],
                          combining_rule=item.get("combining_rule"), memo=item.get("memo"), population=item.get("population"),
                          comparator=item.get("comparator"), horizon=item.get("horizon"), evidence_level=item.get("evidence_level")))
    items.sort(key=lambda i: (i["faq_entry"] is None, i["faq_entry"] or 0, i["id"]))
    (HERE/"context.json").write_text(json.dumps(dict(items=items, combining_rules=source.get("combining_rules", [])), indent=1, ensure_ascii=False)+"\n")
    print(f"context.json: {len(items)} items kept, {len(dropped_items)} dropped {dropped_items}, {dropped_values} unconfirmed values removed")


if __name__ == "__main__":
    main()
