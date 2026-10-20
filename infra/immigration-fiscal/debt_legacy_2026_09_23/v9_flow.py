"""Oct16 signed payer/timing bridge over the preserved, audited oct15 source rows.

Native-First: native package evaluations and producer typed parts; unresolved
economic payer or timing is exported, never guessed as Treasury borrowing.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pandas as pd

from v8_flow import coalesce_coverage, separate_timing

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
sys.path.insert(0, str(FISCAL / "scripts"))
from memory_budget import require_within_budget


def require(ok, message):
    if not ok:
        raise ValueError("[BLOCKED] oct16 current-flow contract: " + message)


def clean(row):
    return {k: (None if pd.isna(v) else v) for k, v in row.items()}


def load_native_frame(out=None):
    """Verify the tracked receipt before consuming the rebuildable native cache."""
    out = Path(out) if out is not None else HERE / "derived/oct16"
    manifest = out / "native_frame_manifest.json"
    require(manifest.is_file(), "native frame manifest missing; run debt oct16 first")
    receipt = json.loads(manifest.read_text())
    artifact = receipt["artifact"]
    require(artifact["path"] == "_cache/oct16/native_frame.json", "unexpected native frame cache path")
    frame = HERE / artifact["path"]
    require(frame.is_file(), "native frame cache missing; run debt oct16 first")
    data = frame.read_bytes()
    require(len(data) == artifact["bytes"] and hashlib.sha256(data).hexdigest() == artifact["sha256"],
            "native frame cache hash/size mismatch; rebuild debt oct16")
    for path, digest in receipt["source_pins"].items():
        require(hashlib.sha256((FISCAL / path).read_bytes()).hexdigest() == digest,
                "stale native frame source " + path)
    return json.loads(data)


def write_native_frame_manifest(frame, out):
    """Record actual cache bytes; freshness is separately checked by every reader."""
    data = frame.read_bytes()
    snapshot = json.loads(data)
    receipt = dict(case="oct16", artifact=dict(path=frame.relative_to(HERE).as_posix(),
                   sha256=hashlib.sha256(data).hexdigest(), bytes=len(data)), source_pins=snapshot["pins"],
                   rebuild="sh infra/immigration-fiscal/debt_legacy_2026_09_23/run_oct16.sh")
    (out / "native_frame_manifest.json").write_text(json.dumps(receipt, indent=2)+"\n")


def residual_health_payer(full_fraction, national, military):
    require(0<military<national, 'military health national subblock')
    fraction=(full_fraction*national-military)/(national-military)
    require(0<=fraction<=1, 'residual health economic payer')
    return fraction


def require_capital_rate(row, rate):
    require("capital_stock_delta_bn" in row, "item21 capital source lacks its stock delta")
    require(abs(row["delta_bn"]-row["capital_stock_delta_bn"]*rate)<1e-9,
            "item21 direct capital is not priced at the selected Trustees rate")


def classify(rows, value, source_line, side, item, *, force=None, reason=None, level=None):
    """Route a signed cost by its economic source, not its carrier's storage side."""
    out = dict(side="v9_item", id=f"{item}:{side}:{source_line}", source_line=source_line,
               source_side=side, item=item, responsive_bn=float(value))
    if abs(value) < 1e-16:
        return None
    if force is not None:
        fraction, financing = force
    elif side == "capital":
        if level not in ("federal", "state_local"):
            out.update(financing="resource_cost", federal_bn=None, state_local_bn=None,
                       reason="capital source lacks a located government; never assigned to borrowing")
            return out
        fraction, financing = float(level == "federal"), "resource_cost"
    else:
        candidates = [r for r in rows if r["side"] == side and r["id"] == source_line
                      and r.get("financing") != "pension_accrual"]
        total = sum(r["responsive_bn"] for r in candidates)
        if not candidates or abs(total) < 1e-14 or any(r.get("federal_bn") is None for r in candidates):
            out.update(financing="unlocated", federal_bn=None, state_local_bn=None,
                       reason=reason or "no independently located economic source payer/timing")
            return out
        kinds = {r["financing"] for r in candidates}
        require(len(kinds) == 1, "ambiguous source financing " + source_line)
        fraction = sum(r["federal_bn"] for r in candidates) / total
        financing = next(iter(kinds))
    out.update(financing=financing, federal_bn=value*fraction, state_local_bn=value*(1-fraction))
    return out


def count_parts(payload, item, end):
    meta = payload["meta"][item]
    frame = pd.read_csv(FISCAL / meta["parts_file"])
    selected = frame[(frame.scenario == meta["parts_scenario"]) & (frame.end == end)].copy()
    if meta.get("subtract_parts_scenario"):
        before = frame[(frame.scenario == meta["subtract_parts_scenario"]) & (frame.end == end)]
        keys = [c for c in frame.columns if c not in ("scenario", "observed_change_bn", "coverage_change_bn", "change_bn")]
        # Producer rows can share the same source key; aggregate by economic source.
        keys = [c for c in keys if c not in ("complete_use_excluded",)]
        a = selected.groupby(keys, dropna=False)["change_bn"].sum()
        b = before.groupby(keys, dropna=False)["change_bn"].sum()
        selected = a.subtract(b, fill_value=0).rename("change_bn").reset_index()
    return selected.to_dict("records")


def build_rows(snapshot, old_rows):
    output, checks = [], []
    selected = snapshot["sets"]["set"]["payload"]["meta"]["v9"]["selected_items"]
    require("passthrough_source_tax" not in selected, "item19 unexpectedly central")
    for basis, block in snapshot["sets"].items():
        payload, meta = block["payload"], block["payload"]["meta"]
        previous_ids={r['id'] for r in block['old_payload']['meta']['items']}
        edit_owners=[r['id'] for r in meta['items'] if r['id'] not in previous_ids and r['edits']['count']]
        require(edit_owners==['consumption_tax_bases'], 'new engine edits lack their unique source18 owner')
        levels = {r["id"]: r["level"] for r in meta["capital_return"]["components"]}
        carriers = meta["union_completion"]["carriers"]
        for end, point in block["endpoints"].items():
            new, old = point["r"], point["old"]
            for convention in ("low", "central", "high"):
                base = [dict(r) for r in old_rows if (r["basis"], r["end"], r["convention"]) == (basis, end, convention)]
                require(abs(sum(r["responsive_bn"] for r in base)-old["cost_bn"]) < 1e-9,
                        f"preserved oct15 source total {basis}/{end}/{convention}")
                # Undo the previous set/cash split, then apply it again after all new terms.
                for row in base:
                    row["item"] = "inherited_v8"
                    if row["financing"] == "pension_accrual":
                        row["financing"] = "cash"
                        row["id"] = row["id"].removesuffix(":set_minus_cash")
                delta = []
                health_base = [r for r in base if r['side']=='spending' and r['id']=='health_services']
                health_amount = sum(r['responsive_bn'] for r in health_base)
                health_fraction = sum(r['federal_bn'] for r in health_base)/health_amount
                national_health = next(r['national_bn'] for r in new['evaluation']['spending'] if r['id']=='health_services')
                military_health = next(r['national_component_bn'] for r in meta['veterans_compensation']['by_end'][end]['parts']
                                       if r.get('part')=='va_medical' and r.get('population')=='engine')
                residual_health_fraction = residual_health_payer(health_fraction,national_health,military_health)
                def add(value, line, side, item, **kwargs):
                    if line=='health_services' and side=='spending' and kwargs.get('force') is None:
                        kwargs['force'] = (residual_health_fraction,'cash')
                    row = classify(base, value, line, side, item, **kwargs)
                    if row:
                        delta.append(row)
                for side, field in (("spending", "spending"), ("receipt", "receipts")):
                    prior = {r["id"]: r for r in old["evaluation"][field]}
                    for row in new["evaluation"][field]:
                        change = -row["effect_bn"] + prior[row["id"]]["effect_bn"]
                        source = carriers.get(row["id"], {})
                        parent = source.get("parent_line", row["id"])
                        add(change, parent, source.get("side", side), "consumption_tax_bases")
                old_cap = {r["id"]: r["return_bn"] for r in old["capital"]["components"]}
                for row in new["capital"]["components"]:
                    add(row["return_bn"]-old_cap[row["id"]], row["id"], "capital", "engine_capital", level=row["level"])
                for item, value in new["v9_post_engine"]["amounts"].items():
                    start = len(delta)
                    parts = new["v9_post_engine"]["parts"].get(item, [])
                    if item in ("veterans_compensation", "income_security_administration"):
                        for row in parts:
                            add(row["delta_bn"], row["source_line"], "spending", item, force=(1.0, "cash"))
                    elif item == "public_college_response":
                        for row in parts:
                            capital = row["kind"] == "college_capital"
                            add(row["delta_bn"], row["source_line"], "capital" if capital else "spending", item,
                                level=levels.get(row["source_line"]) if capital else None)
                    elif item == "one_rate":
                        for row in parts:
                            parent = row.get("source_line", row["line"])
                            level = levels.get(parent)
                            if parent in carriers:
                                level = levels.get(carriers[parent]["parent_line"])
                            add(row["delta_bn"], parent, "capital", item, level=level)
                    elif item == "health_residual_key":
                        for row in parts:
                            side = 'capital' if row.get('side')=='capital' or row.get('source_side')=='capital' else 'spending'
                            if side == 'capital':
                                require_capital_rate(row,meta['one_rate']['flat_real_equivalent'])
                            parent = row.get('source_line',row['line'])
                            add(row['delta_bn'],parent,side,item,level=levels.get(parent))
                    elif item in ("native_minor_calibration", "coverage_tenure"):
                        for row in count_parts(payload, item, end):
                            parent, side = row["source_line"], row["source_side"]
                            # The source's net production carrier combines P/F;
                            # its signed total alone cannot identify private income.
                            add(row["change_bn"], parent, side, item, level=row.get("level"))
                    elif item == "coverage_repricing":
                        prior = block["old_payload"]["meta"]["coverage"]["by_end"][end]["decomposition"]["line_parts"]
                        current = meta["coverage"]["by_end"][end]["decomposition"]["line_parts"]
                        for sign, pieces in ((-1, prior), (1, current)):
                            for row in pieces:
                                if row["economic_class"] == "production" and "P_bn" in row and "F_bn" in row:
                                    add(-sign*row["P_bn"], "private_P", "production", item, force=(0.,"private_production"))
                                    add(-sign*row["F_bn"], "induced_receipts_F", "production", item)
                                else:
                                    force = (health_fraction,'cash') if sign<0 and row.get('source_line')=='health_services' else None
                                    add(sign*row["coverage_bn"], row.get("source_line", row["line"]),
                                        row.get("source_side", "unknown"), item, level=row.get("level"),force=force)
                    known = sum(r["responsive_bn"] for r in delta[start:])
                    residual = value-known
                    if abs(residual) > 1e-12:
                        add(residual, "unlocated_remainder", "unknown", item,
                            reason="selected native item minus its exported located source pieces; no payer or timing invented")
                    require(abs(sum(r["responsive_bn"] for r in delta[start:])-value) < 1e-9,
                            f"selected item closure {item}")
                rows = base + delta
                # The retirement-only administration re-key moves a federal
                # block inside a mixed-payer line. Coverage's new-minus-old
                # aggregate needs the same economic payer adjustment.
                for piece in meta['income_security_administration']['by_end'][end].get('parts',[]):
                    if piece.get('population')!='coverage':
                        continue
                    parent=piece['source_line']
                    ordinary=classify(base,piece['delta_bn'],parent,'spending','administration_payer_probe')
                    if ordinary and ordinary['financing']=='cash':
                        adjustment=piece['delta_bn']-ordinary['federal_bn']
                        rows.append(dict(side='v9_item',id='administration_coverage_payer:'+parent,
                            source_line=parent,source_side='spending',item='income_security_administration',
                            responsive_bn=0.,federal_bn=adjustment,state_local_bn=-adjustment,financing='cash',
                            reason='retirement administration is federal; zero-total payer reclassification of its coverage piece'))
                require(abs(sum(r["responsive_bn"] for r in rows)-point["cost_bn"]) < 1e-9,
                        f"complete source closure {basis}/{end}/{convention}")
                output += [dict(r, basis=basis, end=end, convention=convention) for r in rows]
                checks.append(dict(basis=basis, end=end, convention=convention,
                                   source_closure_bn=sum(r["responsive_bn"] for r in rows)-point["cost_bn"], passed=True))
    # Aggregate all same economic source pieces before matching the two timing bases.
    grouped = {}
    for row in output:
        key = tuple(row.get(k) for k in ("basis", "end", "convention", "side", "id", "item", "generation", "source_line", "source_side", "financing"))
        if key not in grouped:
            grouped[key] = dict(row)
        else:
            for field in ("responsive_bn", "federal_bn", "state_local_bn", "union_bn", "lineage_bn"):
                a, b = grouped[key].get(field), row.get(field)
                grouped[key][field] = a+b if a is not None and b is not None else None
    # Item identity is in the row id, and generation/source fields retain source keys.
    timed = separate_timing(list(grouped.values()))
    return timed, checks


def main(d, args):
    live = json.loads((FISCAL / "live_case.json").read_text())
    require(live.get("key") == "oct16", "authoritative live case is not oct16")
    out = args.out_dir or HERE / "derived/oct16"
    out.mkdir(parents=True, exist_ok=True)
    frame = HERE / "_cache/oct16/native_frame.json"
    frame.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["node", str(HERE / "v9_frame.cjs"), str(frame)], check=True)
    snapshot = json.loads(frame.read_text())
    write_native_frame_manifest(frame, out)
    rows = [clean(r) for r in pd.read_csv(HERE / "derived/oct15/current_flow_source_parts_2024.csv").to_dict("records")]
    timed, checks = build_rows(snapshot, rows)
    table = pd.DataFrame(timed)
    bands = {b: x["band_bn"] for b, x in snapshot["sets"].items()}
    v9 = snapshot["summary"]["v9"]
    for basis, expected in (("set", v9["band_bn"]), ("cash", v9["cash_set_bn"])):
        require(max(abs(a-b) for a, b in zip(bands[basis], expected)) < 1e-9, basis + " native/summary band")
    printed = pd.read_csv(FISCAL / "main_case_2026_10_16/derived/main_case_bands.csv")
    for basis, variant in (("set", "adopted"), ("cash", "cash_set")):
        matched = printed[(printed.variant == variant) & (printed.profile == "long_run_non_school_full")]
        require(len(matched) == 1, basis + " unique adopted profile row")
        row = matched.iloc[0]
        require(max(abs(a-b) for a,b in zip(bands[basis], (row.cost_low_bn, row.cost_high_bn))) < 1e-4,
                basis + " printed band")
    federal = table[table.financing == "cash"].groupby(["basis", "end", "convention"]).federal_bn.sum()
    summary = dict(case="oct16", status="current flows only; historical financing remains unidentified",
                   financing_complete=False, historical_stock_identified=False, bands_bn=bands,
                   population=snapshot["sets"]["set"]["payload"]["meta"]["population_v9"],
                   selected_items=snapshot["sets"]["set"]["payload"]["meta"]["v9"]["selected_items"],
                   source_pins=snapshot["pins"], gates=checks, closure_tolerance_bn=1e-9,
                   federal_current_cash_bn={"|".join(k): v for k, v in federal.to_dict().items()},
                   federal_sign_scope="identified source cash only; unlocated remainder is not observed Treasury borrowing",
                   health_payer_rule="Inherited full-health federal payer mass less the explicitly federal VA subblock, over residual national health consumption; source21 and count-key changes use this residual mix. Retirement-administration coverage corrections retain their federal source payer.",
                   historical_military_scope="source-line-only historical delta is separately exported where national histories identify a source; full historical payer/timing remains blocked")
    summary["financing_totals_bn"] = {"|".join(k):v for k,v in table.groupby(["basis", "end", "convention", "financing"]).responsive_bn.sum().to_dict().items()}
    summary['item_timing_totals_bn'] = {'|'.join(k):v for k,v in table.groupby(['basis','end','convention','item','financing']).responsive_bn.sum().to_dict().items()}
    summary['item_export_scope'] = 'Selected v9 additions are individually routed; earlier selected items remain the audited inherited-v8 source-line base, including its explicit mixed-unit/coverage classifications. No arbitrary factor allocation of an inherited source line is invented.'
    summary["per_member_usd"] = {b: [x*1e9/summary["population"]["with_coverage"] for x in band] for b,band in bands.items()}
    require_within_budget("oct16 current-flow export")
    table.to_csv(out / "current_flow_source_parts_2024.csv", index=False, lineterminator="\n")
    (out / "current_flow_contract.json").write_text(json.dumps(summary, indent=2, allow_nan=False)+"\n")
    print("PASS oct16 source/timing closure", bands, "federal identified cash", summary["federal_current_cash_bn"])
    if not args.current_flow_only:
        raise ValueError("[BLOCKED] oct16 historical stocks need the unlocated payer/timing bridge; use --current-flow-only")
