"""Assemble the self-contained explorer page: template + model + presets + evidence + ladder + engine + UI.

No network resource is referenced; the page opens from file:// and meets the Artifact page contract.
Every preset path must exist in the engine's state, so a typo cannot silently do nothing, and a
preset value marked `value_from` is read from derived/scaling_check.json rather than typed.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import ladder

HERE = Path(__file__).resolve().parent
OUT = HERE/"derived"
STATE_PATHS = re.compile(r"^(production\.[a-z_]+|[a-z_]+)$")


def main():
    model = json.loads((OUT/"model.json").read_text())
    presets = json.loads((HERE/"presets.json").read_text())
    evidence = json.loads((OUT/"scaling_check.json").read_text())  # scaling_check.py
    context_path = HERE/"context.json"
    context = json.loads(context_path.read_text()) if context_path.exists() else {"items": []}
    engine = (HERE/"engine.js").read_text()
    known = set(re.findall(r"^\s{6}([a-z_]+):", engine, flags=re.M)) | {"school_response_band"}
    ids = {p["id"] for p in presets["presets"]}
    for preset in presets["presets"]:
        for setting in preset.get("settings", []):
            path = setting.get("path")
            if path is None:
                continue
            if "value_from" in setting:
                setting["value"] = evidence[setting.pop("value_from")]
            head = path.split(".")[0]
            if not STATE_PATHS.match(path) or head not in known:
                raise ValueError(f"Preset {preset['id']} sets an unknown state path: {path}")
            if head == "production" and setting["value"] not in model["production"]["dims"][path.split(".")[1]]:
                raise ValueError(f"Preset {preset['id']} uses a production level that was never executed: {path}")
    for author in presets["authors"]:
        if author["closest"]["preset"] not in ids | {None}:
            raise ValueError(f"Author {author['id']} points at an unknown convention")
    page = (HERE/"template.html").read_text()
    blocks = {"/*MODEL*/": json.dumps(model, separators=(",", ":")), "/*PRESETS*/": json.dumps(presets, separators=(",", ":")),
              "/*CONTEXT*/": json.dumps(context, separators=(",", ":")), "/*EVIDENCE*/": json.dumps(evidence, separators=(",", ":")),
              "/*LADDER*/": json.dumps(ladder.parse(), separators=(",", ":")),
              "/*ENGINE*/": engine, "/*UI*/": (HERE/"ui.js").read_text()}
    for marker, body in blocks.items():
        if page.count(marker) != 1:
            raise ValueError(f"Template marker missing or repeated: {marker}")
        page = page.replace(marker, body.replace("</script", "<\\/script"))
    if re.search(r"(src|href)=\"https?://", page):
        raise ValueError("The page must not load network resources")
    (OUT/"explorer.html").write_text(page)
    print(f"explorer.html: {len(page)/1e6:.2f} MB, {len(presets['presets'])} conventions, {len(presets['authors'])} authors, "
          f"{len(context['items'])} objection cards, {len(json.loads(blocks['/*LADDER*/'])['cards'])} ladder entries")


if __name__ == "__main__":
    main()
