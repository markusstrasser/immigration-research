"""Strict extension of the v7 payload contract for v8 consumers.

The existing lineage/item gate remains the principal for the v7 prefix. New
carriers, edit ranges, post-engine parts and responses require their own gates.
"""
from __future__ import annotations

import copy
import math


def parts(d, payload, which="set"):
    previous = d.case_payload("oct14", which)
    result = copy.deepcopy(d.v6_parts("oct14", previous, which))
    n = len(previous["edits"])
    old_lines = previous["lines"]
    old_items = previous["meta"]["items"]
    if payload["edits"][:n] != previous["edits"] or payload["lines"][:len(old_lines)] != old_lines \
            or payload.get("receipt_lines") != previous.get("receipt_lines") \
            or payload["meta"]["items"][:len(old_items)] != old_items:
        raise SystemExit("[BLOCKED] v8 payload does not preserve its complete v7 prefix")
    additions = payload["meta"]["items"][len(old_items):]
    if [x["id"] for x in additions] != ["foreign_source_tax", "union_completion", "mixed_unit_removal", "coverage"]:
        raise SystemExit("[BLOCKED] v8 items are not exactly items 9–12 in order")
    child = next(x for x in additions if x["id"] == "union_completion")
    delta = child.get("production_delta")
    if not delta or child.get("production_generation") != "G3plus" or delta["dims"] != previous["production"]["dims"]:
        raise SystemExit("[BLOCKED] v8 native child production lacks its declared additive G3plus grid")
    for field in ("private_wtp_bn", "induced_receipts_bn"):
        want = [x + y for x, y in zip(previous["production"][field], delta[field])]
        if len(want) != len(payload["production"][field]) or any(abs(a - b) > 1e-12 for a, b in zip(want, payload["production"][field])):
            raise SystemExit(f"[BLOCKED] v8 {field} is not the v7 grid plus its child delta exactly once")
    if payload["production"]["sampling_se_bn"] != previous["production"]["sampling_se_bn"]:
        raise SystemExit("[BLOCKED] v8 changed production sampling SE without a declared source")
    carriers = payload["meta"]["union_completion"]["carriers"]
    if [x["id"] for x in payload["lines"][len(old_lines):]] != list(carriers):
        raise SystemExit("[BLOCKED] v8's synthetic lines are not its declared union-completion carriers")
    for it in additions:
        first, count = it["edits"]["first"], it["edits"]["count"]
        if first != n or count < 0:
            raise SystemExit(f"[BLOCKED] v8 {it['id']} edits are not contiguous")
        mine = payload["edits"][first:first + count]
        if len(mine) != count or any("by" not in edit or "national_bn" in edit for edit in mine):
            raise SystemExit(f"[BLOCKED] v8 {it['id']} is not a fixed cell edit set")
        if it["kind"] == "post_engine":
            if count or it.get("parts"):
                raise SystemExit(f"[BLOCKED] v8 {it['id']} post-engine amount also carries edits")
            z = payload["meta"][it["id"]]
            for end in ("low", "high"):
                row = z["by_end"][end]
                gens = row.get("by_generation_bn", row.get("by_generation"))
                if not gens or any(not math.isfinite(x) for x in gens.values()) \
                        or abs(sum(gens.values()) - row["total_bn"]) > 1e-9:
                    raise SystemExit(f"[BLOCKED] v8 {it['id']}/{end} generation parts do not close")
            if it["id"] == "coverage" and z.get("stub"):
                raise SystemExit("[BLOCKED] v8 coverage remains STUB")
        elif it["kind"] == "edit_set":
            for j, edit in enumerate(mine):
                ps = [p for tag, p in it["parts"].items() if p["edit"] == j and tag.startswith(("union_", "lineage_"))]
                if not ps or any(abs(sum(p["by"][a] for p in ps) - edit["by"][a]) > 1e-12 for a in ("personal", "shared")):
                    raise SystemExit(f"[BLOCKED] v8 {it['id']}/{j} union/lineage parts do not close")
            result["items"].append(dict(record=it, first=first, edits=mine, union_only=False))
        else:
            raise SystemExit(f"[BLOCKED] unknown v8 item kind {it['kind']}")
        n += count
    if n != len(payload["edits"]):
        raise SystemExit("[BLOCKED] v8 items do not close the payload")
    responses = copy.deepcopy(previous["meta"]["responses"])
    fixed = {cid for cid, src in carriers.items() if src["kind"] != "line"}
    extras = set(payload["meta"]["responses"]) - set(responses)
    if extras != fixed:
        raise SystemExit(f"[BLOCKED] v8 response additions differ from endpoint carriers: {sorted(extras ^ fixed)}")
    for cid in fixed:
        z = payload["meta"]["responses"][cid]
        end = carriers[cid]["end"]
        if z != dict(receipt=False, override=cid, low=int(end == "low"), high=int(end == "high")):
            raise SystemExit(f"[BLOCKED] v8 {cid} is not its declared endpoint response")
        responses[cid] = z
    if payload["meta"]["responses"] != responses:
        raise SystemExit("[BLOCKED] v8 changed a prior response")
    # The exact carrier-only response extension was independently gated above.
    allowed = set(d.OCT15["stamps"]) | {"items", "population_v8", "responses"} | {key for it in additions for key in it["meta_changed"]}
    changed = {key for key in payload["meta"] | previous["meta"] if payload["meta"].get(key) != previous["meta"].get(key)}
    if changed - allowed:
        raise SystemExit(f"[BLOCKED] v8 changed undeclared meta blocks: {sorted(changed - allowed)}")
    if payload["meta"]["adopted"] != d.OCT15["adopted"]:
        raise SystemExit("[BLOCKED] v8 is not adopted")
    result["post_engine"] = {it["id"]: payload["meta"][it["id"]] for it in additions if it["kind"] == "post_engine"}
    return result
