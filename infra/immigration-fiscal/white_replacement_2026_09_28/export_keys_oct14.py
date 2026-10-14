"""Export only v7 income-tax key shares. No pension pricing; rough comparator totals remain blocked on R9."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import rekey_sept29 as W  # noqa: E402
import check_dumps_oct14 as D  # noqa: E402


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def white_tax_residual():
    """Independent receipt-key movement, with pension terms absent from both sides."""
    R = W.R
    R.PI['leaf_white_g3_rate'] = W.np.asarray(W.LINEAGE['age_mix']['mixes']['g3_rate'], float)
    sc = R.scenario('w3', 'leaf_white_g3_rate')
    count = W.LINEAGE['members']['white']
    archived = json.loads((W.DER / 'engine_lines_sept29_cash.json').read_text())
    parts = {}
    for line, key in W.CASE_TAX_KEY.items():
        national = R.NATIONAL['receipts|' + line]
        old_national = next(x['national_bn'] for x in archived['low']['lines']
                            if x['side'] == 'receipts' and x['id'] == line)
        W.gate(f'raw W key leaf: {line} national matches the preserved source', national == old_national)
        old = national * R.line_share(sc, 'receipts', line, 'cps')
        new = national * sc['share'][key + '_personal']
        parts[line] = -(new - old) * count / sc['population']
    raw = sum(parts.values())
    residual, applied = {}, {}
    for basis, filename in (('accrual', 'corrections.json'), ('cash', 'corrections_cash.json')):
        payload = json.loads((W.CASE_LANE / 'derived' / filename).read_text())
        record = next(x for x in payload['meta']['items'] if x['id'] == 'white_end_tax_keys')
        if not record.get('applied'):
            raise SystemExit('[BLOCKED] raw W residual requires the adopted white_end_tax_keys item')
        amount = 0.0
        for name, part in record['parts'].items():
            if name.startswith('lineage_whites:'):
                edit = payload['edits'][record['edits']['first'] + part['edit']]
                if edit.get('scenario') in (None, 'cbo_collective') and edit['line'] in W.CASE_TAX_KEY:
                    amount -= part['by']['personal']
        applied[basis] = amount
        for end in W.ENDS:
            W.gate(f'raw W key leaf: {basis} {end} income-tax responses are one',
                   all(x['response'] == 1 for x in W.FULL[basis][end]['lines']
                       if x['side'] == 'receipts' and x['id'] in W.CASE_TAX_KEY))
        residual[basis] = {end: raw - amount for end in W.ENDS}
    W.stop_if_failed()
    return {'source_count': count, 'raw_move_bn': raw, 'parts_bn': parts,
            'applied_move_bn': applied, 'item_applied': True, 'residual_zero_tolerance_bn': 1e-9,
            'white_end_tax_keys_residual': residual,
            'measurement_scope': 'receipt-key arithmetic only; a nonzero residual is reported, never rounded to pass'}


def main():
    D.main()  # standalone key exports must reject stale engine leaves before deriving any keys
    W.use_case("oct14")
    if W.META.get("adopted") != "2026-10-14":
        raise SystemExit("[BLOCKED] the key leaf requires the adopted October 14 case")
    w4, n4 = W.row4_weights()
    W.set_frame(w4, n4, W.DUMP["cash"])
    keys, W.TAX_K["_fedtax_bc"] = W.case_tax_keys()
    W.TAX_K.update(keys)
    W.R.K.update(keys)
    W.set_frame(w4, n4, W.DUMP["cash"])  # rebuild key totals on the same row-4 frame
    W.lineage_setup()
    W.stop_if_failed()
    groups = W.scenarios()
    residual = white_tax_residual()
    W.write("income_tax_keys_oct14.csv", W.tax_key_rows(groups))
    black = W.tax_key_rows({g: groups[g] for g in ("mexican_origin_rough", "nh_black_rough")})
    black_path = W.BLACK_LANE / "derived/income_tax_keys_oct14.csv"
    with black_path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(black[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(black)
    files = [W.CASE_LANE / "derived" / name for name in ("corrections.json", "corrections_cash.json", "summary.json")]
    files += [Path(__file__), Path(W.__file__), Path(W.R.__file__),
              Path(D.__file__),
              W.DER / 'engine_lines_sept29_cash.json', Path(W.TK.__file__), Path(W.TK.benchmark_frame().__file__), W.R.ZIP,
              W.TK.HERE / "derived/bins.csv", W.TK.BENCH / "derived/cbo_group_shares.csv"]
    files += [W.DER / f'engine_lines_{case}.json' for case in ('oct14', 'oct14_cash', 'oct14_union', 'oct14_union_cash')]
    metadata = {"case": "oct14", "scope": "raw income-tax keys only; no pension pricing or validated rough totals",
                "allocation": W.TAX_ALLOC, "lineage_counts": W.LINEAGE["counts"],
                "inputs_sha256": {str(p.relative_to(W.FISCAL)) if p.is_relative_to(W.FISCAL) else str(p): digest(p) for p in files},
                "csv_sha256": {str(p.relative_to(W.FISCAL)): digest(p) for p in (W.DER / "income_tax_keys_oct14.csv", black_path)},
                **residual}
    for lane in (W.LANE, W.BLACK_LANE):
        (lane / "derived/income_tax_keys_oct14_meta.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print("[PASS] final raw key leaf exported; rough pricing is checked separately")


if __name__ == "__main__":
    main()
