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


def digits(value):
    text = f"{value}"
    return re.sub(r"[^\d.]", "", text.replace(",", "")).rstrip("0").rstrip(".") if isinstance(value, (int, float)) else None


def confirmed(value, ref):
    match = re.match(r"(.+?):(\d+)", str(ref or ""))
    if not match or not (ROOT/match.group(1)).is_file():
        return False
    lines = (ROOT/match.group(1)).read_text(errors="replace").splitlines()
    n = int(match.group(2))
    window = " ".join(lines[max(0, n-3):n+2]).replace(",", "").replace("−", "-")
    want = digits(abs(value)) if isinstance(value, (int, float)) else None
    if want is None:
        return str(value)[:12] in window
    return want in window or want.split(".")[0] in re.findall(r"\d+", window)


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
