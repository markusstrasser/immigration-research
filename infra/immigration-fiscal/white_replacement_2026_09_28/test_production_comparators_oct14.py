"""Streaming replicate joins must preserve IDs across chunk boundaries."""
import io
import zipfile

import numpy as np
import pandas as pd
import pytest

from production_comparators_oct14 import Production, read_replicates


def archive(rows):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as z:
        z.writestr('asec_csv_repwgt_2025.csv', pd.DataFrame(rows).to_csv(index=False))
    return zipfile.ZipFile(io.BytesIO(buf.getvalue()))


def test_streaming_reorder_preserves_person_weights():
    ids = pd.DataFrame({'PH_SEQ': [1, 1, 2], 'PPPOS': [1, 2, 1]})
    rows = [{'h_seq': 2, 'PPPOS': 1, 'pwwgt0': 30, 'pwwgt1': 31},
            {'h_seq': 1, 'PPPOS': 2, 'pwwgt0': 20, 'pwwgt1': 21},
            {'h_seq': 1, 'PPPOS': 1, 'pwwgt0': 10, 'pwwgt1': 11}]
    with archive(rows) as z:
        got = read_replicates(z, ids, ['pwwgt0', 'pwwgt1'], chunk_size=2)
    np.testing.assert_array_equal(got, [[10, 11], [20, 21], [30, 31]])


def test_negative_sdr_weight_is_retained():
    ids = pd.DataFrame({'PH_SEQ': [1], 'PPPOS': [1]})
    with archive([{'h_seq': 1, 'PPPOS': 1, 'pwwgt0': 10, 'pwwgt1': -.5}]) as z:
        np.testing.assert_array_equal(read_replicates(z, ids, ['pwwgt0', 'pwwgt1']), [[10, -.5]])


@pytest.mark.parametrize('kind', ['missing', 'duplicate_across_chunks', 'unknown', 'nonfinite'])
def test_invalid_replicate_joins_stop(kind):
    ids = pd.DataFrame({'PH_SEQ': [1, 2], 'PPPOS': [1, 1]})
    rows = [{'h_seq': 1, 'PPPOS': 1, 'pwwgt0': 10}, {'h_seq': 2, 'PPPOS': 1, 'pwwgt0': 20}]
    if kind == 'missing':
        rows.pop()
    elif kind == 'duplicate_across_chunks':
        rows.append(rows[0])
    elif kind == 'unknown':
        rows[1]['h_seq'] = 99
    else:
        rows[1]['pwwgt0'] = float('nan')
    with archive(rows) as z, pytest.raises(ValueError, match='BLOCKED'):
        read_replicates(z, ids, ['pwwgt0'], chunk_size=1)


@pytest.mark.parametrize('ages', ['own', 'target'])
def test_blockwise_weights_preserve_all_replicates_and_requested_counts(ages):
    from types import SimpleNamespace
    model = Production.__new__(Production)
    r = SimpleNamespace(w=np.array([1., 2., 3.]), cage=np.array([20, 20, 40]), BANDS=[20, 40])
    model.W = SimpleNamespace(R=r)
    model.weights = r.w[:, None] * np.linspace(.5, 1.5, 161)[None, :]
    sc = {'cps_w': np.array([1., 1., 1.]), 'ages': ages}
    got = np.concatenate([model.scenario_weights(sc, columns=slice(k, min(k + 16, 161)))
                          for k in range(0, 161, 16)], axis=1)
    whole = model.scenario_weights(sc)
    np.testing.assert_allclose(got, whole, rtol=1e-13, atol=1e-13)
    np.testing.assert_allclose(got.sum(axis=0), 3., rtol=1e-13, atol=1e-13)
    if ages == 'target':
        np.testing.assert_allclose(got[r.cage == 20].sum(axis=0), 2., rtol=1e-13, atol=1e-13)
