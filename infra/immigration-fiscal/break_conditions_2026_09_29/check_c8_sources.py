"""Validate delivered comparator inputs without publishing withheld C1-C9 tables."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', choices=('oct15', 'oct16'), default='oct16')
    case = parser.parse_args().case
    if case == 'oct16':
        import tables_oct16 as T
    else:
        import tables_oct15 as T
    white = T.F / 'white_replacement_2026_09_28/derived'
    records = T.rows(white / f'symmetric_results_{case}.csv')
    values = T.comparator_values(records)
    bridges = T.bridge_values(T.rows(white / f'lineage_engine_bridge_{case}.csv'), values)
    mixed = T.COMPARISON.load_mixed_unit(case=case)
    checked, gaps = 0, []
    for row in records:
        if row['arm'] != 'combined_rules_only' or row['group'] != 'A1_third_plus_nh_white':
            continue
        correction = T.COMPARISON.comparator_removal(mixed, row['group'], row['basis'], row['end'], float(row['population']))
        T.check('C8 principal measured own-mask item11', float(row['comparator_item11_bn']), correction['bn'], 1e-9)
        if case == 'oct16':
            T.validate_item11_uncertainty(row)
            if correction['paired_se_bn'] is not None:
                raise SystemExit('[BLOCKED] oct16 source claims an unmeasured paired SE')
            T.check('C8 principal comparator-only SDR', float(row['item11_comparator_se_bn']), correction['comparator_se_bn'], 1e-9)
        else:
            T.check('C8 principal signed-vector paired SE', float(row['item11_paired_se_bn']), correction['paired_se_bn'], 1e-9)
        checked += 1
    for mortality, bound in T.MORTALITY_READINGS:
        for basis in ('accrual', 'cash'):
            for group in ('A1_third_plus_nh_white', 'A3_third_plus_nh_white_at_union_ages'):
                gaps.append(dict(mortality=mortality, bound=bound, basis=basis, group=group,
                                 lineage_minus_comparator_bn=T.comparator_gap(values, mortality, bound, basis, group)))
    report = dict(case=case, source_only=True, tables_withheld=True, bridges_checked=len(bridges),
                  measured_item11_rows_checked=checked, source_sha256=mixed['sha256'], comparisons=gaps)
    path = Path(__file__).resolve().parent / f'derived/c8_source_checks_{case}.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(f'[PASS] C8 delivered sources: {len(bridges)} bridge closures, {checked} measured own-mask rows; tables withheld')


if __name__ == '__main__':
    main()
