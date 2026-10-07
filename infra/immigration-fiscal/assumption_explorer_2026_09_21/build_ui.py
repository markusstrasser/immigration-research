"""Assemble the self-contained explorer page: template + model + case payloads + presets + evidence + ladder + sources +
engine + case + UI.

The page loads nothing from the network and opens from file://. Links out are citations only.
Build-time checks, so a typo cannot silently do nothing:
- the main case's two payloads (main_case_2026_10_07/derived/corrections.json and corrections_cash.json) are inlined
  for case.js; the build refuses when either is missing, lacks its stamps, responses or capital components, or carries
  a line with a class the engine does not answer or with no plain name in ui.js;
- every preset path exists in the case's state, a value marked `value_from` is read rather than typed (a name from
  derived/scaling_check.json, or `responses.<path>` from the payload's meta.responses), a case field takes one of its
  values, a per-line allocation rule names a line and rule the model holds, a band contains its point value, an
  `extends` names a preset that extends nothing, and exactly one preset is the central case;
- {response:<id>}, {share:<id>}, {elasticity:<id>}, {people:<field>} and {rate:<name>} tokens in preset text become the
  payload's numbers; an {assigned:<name>} token stays in the text and the page fills it from the ledger when it draws,
  so it must name an amount ui.js defines;
- a lane reading names a field of the case lane's summary.json, or a row of its bands CSV, that holds a band; a readout
  reads its band from the lane file it names, and a CSV readout's file must carry this case's band;
- every id a source claims to support exists on the page (a setting, a card, a convention, a readout, an author
  statement), and every source carries a short label and either a link or a file in this checkout;
- a setting's `cite` names ids in sources.json, each of which lists that convention among its places;
- a file named in a reference becomes a local link only when it exists in this checkout;
- every allocation rule in the model and the payloads has a plain name in ui.js.
"""
from __future__ import annotations

import csv
import json
import os
import re
from pathlib import Path

import ladder

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LANES = ROOT/"infra/immigration-fiscal"
OUT = HERE/"derived"
CASE_LANE = LANES/"main_case_2026_10_07"
PAYLOADS = {"accrual": CASE_LANE/"derived/corrections.json", "cash": CASE_LANE/"derived/corrections_cash.json"}  # written by main_case.cjs
STATE_PATHS = re.compile(r"^((production|key_override|key_band|response_override)\.[a-z_:]+|[a-z_]+)$")
BANDS = {"school_response_band": "school_response", "general_government_response_band": "general_government_response",
         "reading_band": "reading"}
READINGS = ("low", "high")
CASE_VALUES = {"benefits": ("accrual", "cash"), "long_run": ("case", 0, 1), "capital": ("case", 0, "private"), "reading": READINGS}
TOKEN = re.compile(r"\{(response|share|elasticity|people|rate):([a-z_]+)\}")
ASSIGNED = re.compile(r"\{assigned:([a-z_]+)\}")
FILE_TOKEN = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_./-]*\.(?:md|py|csv|json|js|cjs|sql|html)\b")  # same pattern as ui.js repoLinks
FIXED_PLACES = {"ledger", "capital", "production", "standing"}


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
    places |= {f"readout:{r['id']}" for r in presets["readouts"]}
    for author in presets["authors"]:
        places.add(f"author:{author['id']}")
        places |= {f"argue:{author['id']}:{i}" for i in range(len(author["argues"]))}
    keys = set()
    for source in sources["sources"]:
        # A document of this repo (a decision record, an analysis lane) links to its file in the checkout.
        repo = source.get("kind") == "repo"
        missing = {"key", "short", "authors", "year", "title", "supports", "path" if repo else "url"}-set(source)
        if missing:
            raise ValueError(f"Source {source.get('key')} lacks {sorted(missing)}")
        if source["key"] in keys:
            raise ValueError(f"Duplicate source key {source['key']}")
        keys.add(source["key"])
        if repo:
            if not (ROOT/source["path"]).is_file():
                raise ValueError(f"Source {source['key']} names no file in this checkout: {source['path']}")
        elif not re.match(r"^https?://", source["url"]):
            raise ValueError(f"Source {source['key']} has no http(s) link")
        elif not source.get("repo_ref") and not source.get("resolved"):
            raise ValueError(f"Source {source['key']} names neither where the repo cites it nor when its link was resolved")
        if not source["supports"]:
            raise ValueError(f"Source {source['key']} supports no place on the page: drop it from the registry")
        unknown = set(source["supports"])-places
        if unknown:
            raise ValueError(f"Source {source['key']} supports places that are not on the page: {sorted(unknown)}")
    cited = {place for source in sources["sources"] for place in source["supports"]}
    return sorted(places-cited-FIXED_PLACES)


def read_value(numbers, name, where="value_from"):
    """A number `value_from` names: a scaling_check.json field, or a dotted path such as responses.school.growth."""
    node = numbers
    for part in name.split("."):
        if not isinstance(node, dict) or part not in node:
            raise ValueError(f"{where} names no number: {name}")
        node = node[part]
    if isinstance(node, bool) or not isinstance(node, (int, float)):
        raise ValueError(f"{where} does not name a number: {name}")
    return node


def check_setting(preset, path, value, model, known, enterprises):
    """Refuse a setting the engine, the case or the model cannot honour."""
    lines = {line["id"]: line for line in model["spending"]["lines"]}
    head, _, tail = path.partition(".")
    if not STATE_PATHS.match(path) or head not in known:
        raise ValueError(f"Preset {preset} sets an unknown state path: {path}")
    if head == "production" and value not in model["production"]["dims"][tail]:
        raise ValueError(f"Preset {preset} uses a production level that was never executed: {path}")
    if head in ("key_override", "key_band"):
        rules = value if head == "key_band" else [value]
        if tail not in lines or not all(r in lines[tail]["keys"] for r in rules) or (head == "key_band" and len(rules) < 2):
            raise ValueError(f"Preset {preset} names an allocation rule the model does not hold: {path}")
    allowed = dict(CASE_VALUES, enterprises=tuple(enterprises)).get(path)
    if allowed is not None and value not in allowed:
        raise ValueError(f"Preset {preset} sets {path} to {value!r}, not one of {allowed}")
    if path == "reading_band" and value is not None and list(value) != list(READINGS):
        raise ValueError(f"Preset {preset}: reading_band must be {list(READINGS)}")


def preset_values(preset, by_id):
    """A preset's settings by path: its base's (`extends`), then its own."""
    values = {}
    if preset.get("extends"):
        base = by_id.get(preset["extends"])
        if not base or base.get("extends"):
            raise ValueError(f"Preset {preset['id']} extends {preset['extends']}, which is not a preset that extends nothing")
        values.update(preset_values(base, by_id))
    for setting in preset.get("settings", []):
        if setting.get("path") is not None:
            values[setting["path"]] = setting["value"]
    return values


def check_presets(presets, model, numbers, known, enterprises):
    """Resolve `value_from` in place and refuse a setting the engine, the case or the model cannot honour."""
    if sum(1 for p in presets["presets"] if p.get("central")) != 1:
        raise ValueError("Exactly one preset must be marked central")
    by_id = {p["id"]: p for p in presets["presets"]}
    for preset in presets["presets"]:
        for setting in preset.get("settings", []):
            if setting.get("path") is None:
                continue
            if "value_from" in setting:
                names = setting.pop("value_from")
                setting["value"] = [read_value(numbers, n) for n in names] if isinstance(names, list) else read_value(numbers, names)
            check_setting(preset["id"], setting["path"], setting["value"], model, known, enterprises)
    for preset in presets["presets"]:
        values = preset_values(preset, by_id)
        # A band is reported as a range; the preset's point value must be one of its ends, as for schools.
        pairs = list(BANDS.items())+[(p, "key_override."+p.partition(".")[2]) for p in values if p.startswith("key_band.")]
        for band, point in pairs:
            if values.get(band) is not None and values.get(point) not in values[band]:
                raise ValueError(f"Preset {preset['id']} declares {band} but sets {point} to none of its values")
    return by_id


def check_lane_readings(readings, by_id, summary, bands, model, known, enterprises):
    """Each lane reading is the central preset with stated changes, and names a band the case lane wrote."""
    if not readings.get("rows"):
        raise ValueError("presets.json lane_readings has no rows")
    for row in readings["rows"]:
        for path, value in row["changes"].items():
            check_setting(f"lane reading {row['label']!r}", path, value, model, known, enterprises)
        if "field" in row:
            node = summary
            for part in row["field"].split("."):
                node = node.get(part) if isinstance(node, dict) else None
            if not (isinstance(node, list) and len(node) == 2 and all(isinstance(x, (int, float)) for x in node)):
                raise ValueError(f"Lane reading {row['label']!r}: {readings['file']} has no band at {row['field']}")
        elif row.get("csv_variant") not in bands:
            raise ValueError(f"Lane reading {row['label']!r}: {readings['bands']} has no variant {row.get('csv_variant')}")


def read_bands(path, profile="long_run_non_school_full"):
    with open(path, newline="") as f:
        return {r["variant"]: (float(r["cost_low_bn"]), float(r["cost_high_bn"])) for r in csv.DictReader(f) if r["profile"] == profile}


def resolve_readouts(readouts, adopted_band):
    """Attach each readout's band (cost, $bn) from the lane file it names; a CSV must carry this case's own band."""
    for r in readouts:
        src = r["source"]
        if "csv" in src:
            with open(LANES/src["csv"], newline="") as f:
                arms = {row["arm"]: row for row in csv.DictReader(f)}
            band = lambda arm: [float(arms[arm]["cost_low_bn"]), float(arms[arm]["cost_high_bn"])]  # noqa: E731
            for arm in (src["arm"], src["cash_arm"], src["adopted_arm"]):
                if arm not in arms:
                    raise ValueError(f"Readout {r['id']}: {src['csv']} has no arm {arm}")
            if any(abs(x-y) > 5e-5+1e-9 for x, y in zip(band(src["adopted_arm"]), adopted_band)):
                raise ValueError(f"Readout {r['id']}: {src['csv']} is not on this case (its {src['adopted_arm']} row is {band(src['adopted_arm'])})")
            r["band"], r["cash_band"] = band(src["arm"]), band(src["cash_arm"])
        else:
            node = json.loads((LANES/src["json"]).read_text())
            rule = node
            for part in src["path"].split("."):
                node = node[part]
            for part in src["rule_path"].split("."):
                rule = rule[part]
            if not (isinstance(node, list) and len(node) == 2) or not isinstance(rule, str):
                raise ValueError(f"Readout {r['id']}: {src['json']} has no band at {src['path']} or rule at {src['rule_path']}")
            r["band"], r["rule"] = node, rule


def resolve_tokens(node, meta):
    """Replace the payload tokens: {response:<id>} (low-high responses), {share:<id>} (the population share a finite
    response is read at), {elasticity:<id>} (the marginal rates it is read from), {people:<field>} (millions) and
    {rate:<name>} (a capital-return rate)."""
    if isinstance(node, dict):
        return {k: resolve_tokens(v, meta) for k, v in node.items()}
    if isinstance(node, list):
        return [resolve_tokens(v, meta) for v in node]
    if not isinstance(node, str):
        return node
    R, counts, rates = meta["responses"], meta["lineage"]["counts"], meta["capital_return"]["rates"]

    def pair(lo, hi):
        return f"{lo:.2f}" if f"{lo:.2f}" == f"{hi:.2f}" else f"{lo:.2f}–{hi:.2f}"

    def token(match):
        kind, name = match.groups()
        try:
            if kind == "response":
                return pair(read_value(R, f"{name}.low"), read_value(R, f"{name}.high"))
            if kind == "share":
                return f"{read_value(R, f'{name}.s')*100:.1f}%"
            if kind == "elasticity":
                lo, hi = R[name]["elasticity"]
                return pair(lo, hi)
            if kind == "people":
                return f"{read_value(counts, name)/1e6:.2f} million"
            return f"{read_value(rates, name)*100:.0f}%"
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(f"Unresolved token {match.group(0)}: {error}") from error
    text = TOKEN.sub(token, node)
    if re.search(r"\{(?!assigned:)[a-z_]+:[^}]*\}", text):  # {assigned:...} is filled when the page draws
        raise ValueError(f"Unresolved token in preset text: {text[:100]}")
    return text


def check_cites(presets, sources):
    """A setting's `cite` names sources by key; each must be in the registry and list the convention it is cited in."""
    by_key = {source["key"]: source for source in sources["sources"]}
    for preset in presets["presets"]:
        for setting in preset.get("settings", []):
            keys = setting.get("cite", [])
            if not isinstance(keys, list) or not all(isinstance(k, str) for k in keys):
                raise ValueError(f"Preset {preset['id']}: cite must be a list of source keys")
            for key in keys:
                if key not in by_key:
                    raise ValueError(f"Preset {preset['id']} cites {key}, which sources.json does not hold")
                if f"preset:{preset['id']}" not in by_key[key]["supports"]:
                    raise ValueError(f"Source {key} is cited in preset {preset['id']} but does not list preset:{preset['id']}")


def check_assigned(presets, ui):
    """Every {assigned:<name>} token names an amount the page computes (ui.js ASSIGNED)."""
    block = re.search(r"var ASSIGNED = \{(.*?)\n  \};", ui, flags=re.S)
    if not block:
        raise ValueError("ui.js no longer defines the ASSIGNED amounts")
    named = set(re.findall(r"^\s+([a-z_]+): function", block.group(1), flags=re.M))
    for text in strings(presets):
        unknown = set(ASSIGNED.findall(text))-named
        if unknown:
            raise ValueError(f"Preset text names amounts the page does not compute: {sorted(unknown)} in {text[:80]}")


def check_payloads(payloads, engine, ui):
    """The case's payloads: stamped as one adopted case, with responses and capital components, and correction lines
    with a class engine.js answers and a plain name in ui.js (the payload's own labels are the builders')."""
    classes = set(re.findall(r'case "([a-z_]+)":', engine))
    label_block = re.search(r"var LABEL = \{(.*?)\n  \};", ui, flags=re.S)
    if not label_block:
        raise ValueError("ui.js no longer defines the LABEL names")
    labelled = set(re.findall(r"([a-z_0-9]+): \"", label_block.group(1)))
    for name, payload in payloads.items():
        meta = payload.get("meta", {})
        if not payload.get("edits") or not payload.get("lines") or not meta.get("adopted"):
            raise ValueError(f"{PAYLOADS[name]} lacks edits, lines or meta.adopted")
        if not (meta.get("capital_return") or {}).get("components"):
            raise ValueError(f"{PAYLOADS[name]} is stamped as adopted on {meta['adopted']} but has no capital components")
        for line in payload["lines"]:
            if line.get("response_class") not in classes:
                raise ValueError(f"Correction line {line.get('id')} has a response class engine.js does not answer")
        unnamed = {line["id"] for line in payload["lines"]+payload.get("receipt_lines", [])}-labelled
        if unnamed:
            raise ValueError(f"No plain name in ui.js LABEL for the payload's lines: {sorted(unnamed)}")
        R = meta.get("responses", {})
        for end in ("low", "high", "s"):
            read_value(R, f"general_government.{end}", where=f"{PAYLOADS[name].name} meta.responses")
        for end in ("growth", "decline"):
            read_value(R, f"school.{end}", where=f"{PAYLOADS[name].name} meta.responses")
        elasticity = R["general_government"].get("elasticity")
        if not isinstance(elasticity, list) or len(elasticity) != 2 or not all(isinstance(x, (int, float)) for x in elasticity):
            raise ValueError(f"{PAYLOADS[name]} meta.responses.general_government lacks the two marginal rates its ends replace")
    if payloads["cash"]["meta"]["adopted"] != payloads["accrual"]["meta"]["adopted"]:
        raise ValueError("The cash set's payload is not stamped with the case's adoption")


def check_key_names(model, payloads, ui):
    """Every allocation rule in the model and the payloads needs a plain name in ui.js, or the ledger would show a column name."""
    block = re.search(r"var KEY = \{\s*spending: \{(.*?)\},\s*receipts: \{(.*?)\}\s*\};", ui, flags=re.S)
    if not block:
        raise ValueError("ui.js no longer defines the KEY display map")
    named = [set(re.findall(r"([A-Za-z0-9_]+): \"", part)) for part in block.groups()]
    receipt_lines = model["receipts"]["lines"]+[line for p in payloads.values() for line in p.get("receipt_lines", [])]
    used = [{key for line in model["spending"]["lines"] for key in line["keys"]},
            {cell["key"] for line in receipt_lines for by_allocation in line["cells"].values() for cell in by_allocation.values()}]
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
    case = (HERE/"case.js").read_text()
    ui = (HERE/"ui.js").read_text()
    for name, path in PAYLOADS.items():
        if not path.is_file():
            raise ValueError(f"Missing {path}: run node ../main_case_2026_10_07/main_case.cjs first")
    payloads = {name: json.loads(path.read_text()) for name, path in PAYLOADS.items()}
    check_payloads(payloads, engine, ui)
    meta = payloads["accrual"]["meta"]
    summary = json.loads((CASE_LANE/"derived/summary.json").read_text())
    if "responses" in evidence:
        raise ValueError("scaling_check.json has a field named responses, which value_from reserves for meta.responses")
    known = set(re.findall(r"^\s{6}([a-z_]+):", engine, flags=re.M)) | set(BANDS) | set(CASE_VALUES) | {"enterprises", "reading_band"}
    enterprises = meta["capital_return"]["enterprise_option"]["allowed_by_file"]
    by_id = check_presets(presets, model, dict(evidence, responses=meta["responses"]), known, enterprises)
    check_lane_readings(presets["lane_readings"], by_id, summary, read_bands(LANES/presets["lane_readings"]["bands"]), model, known, enterprises)
    resolve_readouts(presets["readouts"], summary["main_case"])
    check_cites(presets, sources)
    presets = {k: v if k == "note" else resolve_tokens(v, meta) for k, v in presets.items()}  # the note documents the tokens
    ids = {p["id"] for p in presets["presets"]}
    for author in presets["authors"]:
        if author["closest"]["preset"] not in ids | {None}:
            raise ValueError(f"Author {author['id']} points at an unknown convention")
    control_ids = re.findall(r"\{ group: \"[^\"]+\", id: \"([^\"]+)\"", ui)
    check_key_names(model, payloads, ui)
    check_assigned(presets, ui)
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
    blocks = {"/*MODEL*/": json.dumps(model, separators=(",", ":")), "/*CASE_PAYLOADS*/": json.dumps(payloads, separators=(",", ":")),
              "/*PRESETS*/": json.dumps(presets, separators=(",", ":")),
              "/*CONTEXT*/": json.dumps(context, separators=(",", ":")), "/*EVIDENCE*/": json.dumps(evidence, separators=(",", ":")),
              "/*LADDER*/": json.dumps(parsed_ladder, separators=(",", ":")), "/*SOURCES*/": json.dumps(sources_block, separators=(",", ":")),
              "/*ENGINE*/": engine, "/*CASE*/": case, "/*UI*/": ui}
    page = template
    for marker, body in blocks.items():
        if page.count(marker) != 1:
            raise ValueError(f"Template marker missing or repeated: {marker}")
        page = page.replace(marker, body.replace("</script", "<\\/script"))
    if re.search(r"<(?:script|img|link|iframe|video|audio|source)\b[^>]*\b(?:src|href)=\"https?://", template+ui):
        raise ValueError("The page must not load network resources")
    (OUT/"explorer.html").write_text(page)
    answered = sum(1 for s in sources["sources"] if s.get("checked", {}).get("ok"))
    repo_docs = sum(1 for s in sources["sources"] if s.get("kind") == "repo")
    R = meta["responses"]
    print(f"explorer.html: {len(page)/1e6:.2f} MB, {len(presets['presets'])} conventions, {len(presets['readouts'])} readouts, "
          f"{len(presets['lane_readings']['rows'])} lane readings, {len(presets['authors'])} authors, "
          f"{len(context['items'])} objection cards, {len(parsed_ladder['cards'])} ladder entries, "
          f"{len(sources['sources'])-repo_docs} sources ({answered} links answered) and {repo_docs} repo documents, "
          f"{len(sources_block['paths'])} local file links; main case adopted {meta['adopted']} "
          f"({len(payloads['accrual']['edits'])} cell edits, cash set {len(payloads['cash']['edits'])}, {len(payloads['accrual']['lines'])} lines of its own, "
          f"{len(meta['capital_return']['components'])} capital components), general government "
          f"{R['general_government']['low']:.4f}/{R['general_government']['high']:.4f}, schools {R['school']['growth']:.4f}")
    if uncited:
        print(f"  ! {len(uncited)} places carry no external source: {', '.join(uncited[:12])}{' ...' if len(uncited) > 12 else ''}")


if __name__ == "__main__":
    main()
