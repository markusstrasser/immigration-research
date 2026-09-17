"""Independent arithmetic checks using emitted aggregates, no harmonize import."""
from pathlib import Path
import argparse
import json
import numpy as np
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    root = args.output_dir
    values = pd.read_csv(root / 'generation_outcomes.csv')
    audit = pd.read_csv(root / 'denominator_audit.csv')
    residual = pd.read_csv(root / 'party_residuals.csv')
    provenance = json.loads((root / 'verification.json').read_text())
    assert provenance['status'] == 'PASS' and sum(s['n'] for s in provenance['sources']) == 14116
    assert len(provenance['sources']) == 7
    assert (values.valid_n + values.missing_n == values.cell_n).all()
    key = ['year', 'construction', 'population', 'generation']
    political = values[values.outcome.isin(['dem_all', 'rep_all', 'no_major_party'])].pivot(index=key, columns='outcome', values='weighted_pct')
    assert np.allclose(political.sum(axis=1), 100)
    for _, c in values.groupby(['year', 'construction', 'population', 'outcome']):
        total = c[c.generation.eq('all')].iloc[0]
        pieces = c[~c.generation.eq('all')]
        assert pieces.cell_n.sum() == total.cell_n
        assert pieces.valid_n.sum() == total.valid_n
        assert np.isclose(pieces.sum_weight.sum(), total.sum_weight)
        numerator = (pieces.weighted_pct * pieces.sum_weight).sum()
        assert np.isclose(numerator / total.sum_weight, total.weighted_pct)
    assert (audit.dem_n + audit.rep_n + audit.residual_n == audit.base_n).all()
    assert np.allclose(audit.dem_weight / audit.weight_total * 100, audit.reported_dem_all_pct)
    assert np.allclose(audit.dem_weight / (audit.dem_weight + audit.rep_weight) * 100, audit.dem_among_major_partisans_pct)
    residual_sum = residual.groupby(['construction', 'population', 'wording_scope', 'year', 'generation']).agg(n=('n', 'sum'), pct=('pct', 'sum'))
    indexed = audit.set_index(['construction', 'population', 'wording_scope', 'year', 'generation'])
    assert residual_sum.n.equals(indexed.base_n.reindex(residual_sum.index))
    assert np.allclose(residual_sum.pct, 100)
    c = audit[(audit.construction == 'gen_PR_native') & (audit.population == 'all_self_identified_latinos') & (audit.wording_scope == '2013plus') & (audit.year == 'pooled')].set_index('generation')
    assert c.loc['all', 'base_n'] == 10759
    assert c.loc['all', 'dem_n'] + c.loc['all', 'rep_n'] == 8639
    raw_all_gap = c.loc['G2', 'reported_dem_all_pct'] - c.loc['G1', 'reported_dem_all_pct']
    raw_partisan_gap = c.loc['G2', 'dem_among_major_partisans_pct'] - c.loc['G1', 'dem_among_major_partisans_pct']
    assert raw_all_gap > 0 and raw_partisan_gap < 0
    print(f'PASS: partitions, numerators/denominators, residual categories, seven primary benchmarks; same-base raw G2-G1 gaps {raw_all_gap:.6f} pp and {raw_partisan_gap:.6f} pp.')


if __name__ == '__main__':
    main()
