"""Validate delivered comparator inputs without publishing withheld C1-C9 tables."""
import json
from pathlib import Path
import tables_oct15 as T


def main():
    white = T.F / 'white_replacement_2026_09_28/derived'
    records = T.rows(white / 'symmetric_results_oct15.csv')
    values = T.comparator_values(records)
    bridges = T.bridge_values(T.rows(white / 'lineage_engine_bridge_oct15.csv'), values)
    mixed = T.COMPARISON.load_mixed_unit()
    checked, gaps = 0, []
    for row in records:
        if row['arm'] != 'combined_rules_only' or row['group'] != 'A1_third_plus_nh_white':
            continue
        correction = T.COMPARISON.comparator_removal(mixed, row['group'], row['basis'], row['end'], float(row['population']))
        T.check('C8 principal measured own-mask item11', float(row['comparator_item11_bn']), correction['bn'], 1e-9)
        T.check('C8 principal signed-vector paired SE', float(row['item11_paired_se_bn']), correction['paired_se_bn'], 1e-9)
        checked += 1
    for mortality, bound in T.MORTALITY_READINGS:
        for basis in ('accrual', 'cash'):
            for group in ('A1_third_plus_nh_white', 'A3_third_plus_nh_white_at_union_ages'):
                gaps.append(dict(mortality=mortality, bound=bound, basis=basis, group=group,
                                 lineage_minus_comparator_bn=T.comparator_gap(values, mortality, bound, basis, group)))
    report = dict(case='oct15', source_only=True, tables_withheld=True, bridges_checked=len(bridges),
                  measured_item11_rows_checked=checked, source_sha256=mixed['sha256'], comparisons=gaps)
    path = Path(__file__).resolve().parent / 'derived/c8_source_checks_oct15.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(f'[PASS] C8 delivered sources: {len(bridges)} bridge closures, {checked} measured own-mask rows; tables withheld')


if __name__ == '__main__':
    main()
