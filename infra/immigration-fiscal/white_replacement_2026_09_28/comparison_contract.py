"""One-engine contrasts and the separately itemized case-to-rough bridge."""
from __future__ import annotations


def engine_for(group):
    return 'case' if group == 'mexican_origin_engine' else 'rough'


def require_same_engine(left, right):
    if not left.get('engine') or left.get('engine') != right.get('engine'):
        raise SystemExit('[BLOCKED] comparison sides have missing or different engine tags')


def gap_fields(lineage, white, black, item11):
    require_same_engine(lineage, white)
    require_same_engine(lineage, black)
    if abs(lineage['population'] - white['population']) > 1e-6:
        raise SystemExit('[BLOCKED] white comparison does not match lineage population (1e-6 persons)')
    white_gap = lineage['cost_bn'] - white['cost_bn']
    black_gap = black['cost_bn'] - lineage['cost_bn']
    factor = lineage['population'] / black['population']
    equal = black['cost_bn'] * factor - lineage['cost_bn']
    return dict(lineage_engine=lineage['engine'], comparator_engine=white['engine'],
                white_gap_rough_lineage_bn=white_gap,
                black_minus_rough_lineage_bn=black_gap,
                black_minus_rough_lineage_equal_population_bn=equal,
                white_gap_without_item11_bn=white_gap - item11,
                black_minus_lineage_without_item11_bn=black_gap + item11,
                black_minus_lineage_equal_population_without_item11_bn=equal + item11,
                lineage_population=lineage['population'], black_own_population=black['population'],
                mixed_unit_removal_bn=item11,
                mixed_unit_asymmetry='item11 measured for lineage only; comparator counterpart unmeasured')


def bridge_parts(case_run, rough_run, carriers=None):
    """All evaluated line responses plus resource and post-engine components."""
    carriers = carriers or {}
    case, case_lines = case_run[:2]
    rough, rough_lines = rough_run[:2]
    def components(result, lines, buckets):
        out = {(side, lid): (1 if side == 'spending' else -1) * amount * response
               for side, lid, _, amount, response in lines
               if carriers.get(lid, {}).get('kind') not in ('capital', 'production')}
        out[('resource', 'capital_return')] = result['capital']
        out[('resource', 'production_gain')] = -result['production_gain']
        for key, value in buckets.items():
            if key.startswith('lineage post-engine '):
                out[('post_engine', key.removeprefix('lineage post-engine '))] = value
        if abs(sum(out.values()) - result['cost']) > 1e-9:
            raise SystemExit('[BLOCKED] bridge side decomposition does not close (1e-9bn)')
        return out
    a, b = components(case, case_lines, case_run[2]), components(rough, rough_lines, rough_run[2])
    parts = [dict(side=side, line=lid, case_bn=a.get((side, lid), 0.),
                  rough_bn=b.get((side, lid), 0.),
                  case_minus_rough_bn=a.get((side, lid), 0.) - b.get((side, lid), 0.))
             for side, lid in sorted(a.keys() | b.keys())]
    target = case['cost'] - rough['cost']
    if abs(sum(x['case_minus_rough_bn'] for x in parts) - target) > 1e-9:
        raise SystemExit('[BLOCKED] itemized case-to-rough bridge does not close (1e-9bn)')
    return parts
