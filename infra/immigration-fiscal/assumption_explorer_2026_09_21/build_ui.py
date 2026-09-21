"""Assemble the self-contained explorer page: template + model + presets + evidence + ladder + sources + engine + UI.

The page loads nothing from the network and opens from file://. Links out are citations only.
Build-time checks, so a typo cannot silently do nothing:
- every preset path exists in the engine's state, and a value marked `value_from` is read from
  derived/scaling_check.json rather than typed;
- every id a source claims to support exists on the page (a setting, a card, a convention, an author
  statement), and every source carries a link and a short label;
- a file named in a reference becomes a local link only when it exists in this checkout;
- every allocation rule in the model has a plain name in ui.js.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

import ladder

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LANES = ROOT/"infra/immigration-fiscal"
OUT = HERE/"derived"
STATE_PATHS = re.compile(r"^(production\.[a-z_]+|[a-z_]+)$")
FILE_TOKEN = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_./-]*\.(?:md|py|csv|json|js|sql|html)\b")  # same pattern as ui.js repoLinks
FIXED_PLACES = {"ledger", "production", "standing"}


def strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for value in node.values():
            yield from strings(value)
    elif isinstance(node, list):
        for value in node:
            yield from strings(value)


def existing_paths(*documents):
    """Map every file token found in the page's text to its repo-relative path, when the file exists."""
    found = {}
    for document in documents:
        for text in strings(document):
            for token in FILE_TOKEN.findall(text):
                for candidate in (ROOT/token, LANES/token):
                    if candidate.is_file():
                        found[token] = str(candidate.relative_to(ROOT))
                        break
    return found


def check_sources(sources, presets, context, control_ids):
    places = set(FIXED_PLACES)
    places |= {f"control:{c}" for c in control_ids}
    places |= {f"card:{item['id']}" for item in context["items"]}
    places |= {f"preset:{p['id']}" for p in presets["presets"]}
    for author in presets["authors"]:
        places.add(f"author:{author['id']}")
        places |= {f"argue:{author['id']}:{i}" for i in range(len(author["argues"]))}
    keys = set()
    for source in sources["sources"]:
        missing = {"key", "short", "authors", "year", "title", "url", "supports"}-set(source)
        if missing:
            raise ValueError(f"Source {source.get('key')} lacks {sorted(missing)}")
        if source["key"] in keys:
            raise ValueError(f"Duplicate source key {source['key']}")
        keys.add(source["key"])
        if not re.match(r"^https?://", source["url"]):
            raise ValueError(f"Source {source['key']} has no http(s) link")
        if not source.get("repo_ref") and not source.get("resolved"):
            raise ValueError(f"Source {source['key']} names neither where the repo cites it nor when its link was resolved")
        unknown = set(source["supports"])-places
        if unknown:
            raise ValueError(f"Source {source['key']} supports places that are not on the page: {sorted(unknown)}")
    cited = {place for source in sources["sources"] for place in source["supports"]}
    return sorted(places-cited-FIXED_PLACES)


def check_key_names(model, ui):
    """Every allocation rule in the model needs a plain name in ui.js, or the ledger would show a column name."""
    block = re.search(r"var KEY = \{\s*spending: \{(.*?)\},\s*receipts: \{(.*?)\}\s*\};", ui, flags=re.S)
    if not block:
        raise ValueError("ui.js no longer defines the KEY display map")
    named = [set(re.findall(r"([A-Za-z0-9_]+): \"", part)) for part in block.groups()]
    used = [{key for line in model["spending"]["lines"] for key in line["keys"]},
            {cell["key"] for line in model["receipts"]["lines"] for by_allocation in line["cells"].values() for cell in by_allocation.values()}]
    for side, have, need in zip(("spending", "receipts"), named, used):
        if need-have:
            raise ValueError(f"No display name for {side} allocation rules: {sorted(need-have)}")


def main():
    model = json.loads((OUT/"model.json").read_text())
    presets = json.loads((HERE/"presets.json").read_text())
    evidence = json.loads((OUT/"scaling_check.json").read_text())  # scaling_check.py
    context_path = HERE/"context.json"
    context = json.loads(context_path.read_text()) if context_path.exists() else {"items": []}
    sources = json.loads((HERE/"sources.json").read_text())
    checks_path = HERE/"sources_check.json"                        # check_sources.py
    checks = json.loads(checks_path.read_text()) if checks_path.exists() else {}
    engine = (HERE/"engine.js").read_text()
    ui = (HERE/"ui.js").read_text()
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
    control_ids = re.findall(r"\{ group: \"[^\"]+\", id: \"([^\"]+)\"", ui)
    check_key_names(model, ui)
    uncited = check_sources(sources, presets, context, control_ids)
    for source in sources["sources"]:
        if source["key"] in checks:
            source["checked"] = checks[source["key"]]
    parsed_ladder = ladder.parse()
    template = (HERE/"template.html").read_text()
    if not template.lower().startswith("<!doctype html>"):
        raise ValueError("template.html must open with <!doctype html>: in quirks mode tables stop inheriting the text colour")
    sources_block = dict(sources=sources["sources"], repo_prefix=os.path.relpath(ROOT, OUT),
                         paths=existing_paths(presets, context, sources, parsed_ladder["source"], template))
    blocks = {"/*MODEL*/": json.dumps(model, separators=(",", ":")), "/*PRESETS*/": json.dumps(presets, separators=(",", ":")),
              "/*CONTEXT*/": json.dumps(context, separators=(",", ":")), "/*EVIDENCE*/": json.dumps(evidence, separators=(",", ":")),
              "/*LADDER*/": json.dumps(parsed_ladder, separators=(",", ":")), "/*SOURCES*/": json.dumps(sources_block, separators=(",", ":")),
              "/*ENGINE*/": engine, "/*UI*/": ui}
    page = template
    for marker, body in blocks.items():
        if page.count(marker) != 1:
            raise ValueError(f"Template marker missing or repeated: {marker}")
        page = page.replace(marker, body.replace("</script", "<\\/script"))
    if re.search(r"<(?:script|img|link|iframe|video|audio|source)\b[^>]*\b(?:src|href)=\"https?://", template+ui):
        raise ValueError("The page must not load network resources")
    (OUT/"explorer.html").write_text(page)
    answered = sum(1 for s in sources["sources"] if s.get("checked", {}).get("ok"))
    print(f"explorer.html: {len(page)/1e6:.2f} MB, {len(presets['presets'])} conventions, {len(presets['authors'])} authors, "
          f"{len(context['items'])} objection cards, {len(parsed_ladder['cards'])} ladder entries, "
          f"{len(sources['sources'])} sources ({answered} links answered), {len(sources_block['paths'])} local file links")
    if uncited:
        print(f"  ! {len(uncited)} places carry no external source: {', '.join(uncited[:12])}{' ...' if len(uncited) > 12 else ''}")


if __name__ == "__main__":
    main()
