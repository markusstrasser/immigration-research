"""Gates for the Pew 2017 U.S. Muslims lane. Every assertion is loud by design."""
import json
from pathlib import Path

import numpy as np
import pytest

import analysis as A

LANE = Path(__file__).resolve().parent


@pytest.fixture(scope='module')
def loaded():
    return A.load()


def test_g1_source_bytes():
    """G1: the archive is the manifest-registered one."""
    assert A.ZIP.exists(), f'missing {A.ZIP}'
    assert A.ZIP.stat().st_size == A.ZIP_BYTES
    assert A.sha256(A.ZIP) == A.ZIP_SHA256


def test_g2_shape_and_weights(loaded):
    """G2: 1,001 rows, weight positive and finite, 100 replicate weights."""
    d, meta, reps = loaded
    assert len(d) == 1001
    assert len(d.columns) == 222
    w = d['weight'].to_numpy(dtype=float)
    assert np.isfinite(w).all()
    assert (w > 0).all()
    assert len(reps) == 100


def test_replicate_weights_are_jackknife_shaped(loaded):
    """Delete-a-group jackknife: every replicate weight is 0, 1x or 2x the main weight."""
    d, meta, reps = loaded
    ratios = d[reps].div(d['weight'], axis=0).round(6)
    assert set(np.unique(ratios.to_numpy())) == {0.0, 1.0, 2.0}
    assert (ratios == 0).any(axis=1).sum() == 501
    assert int((ratios == 0).sum(axis=1).max()) == 1


def test_codebook_lookup_rejects_unknown_labels(loaded):
    """A code is only ever resolved from exact label text."""
    d, meta, reps = loaded
    book = A.Book(meta)
    assert book.code('educrec', 'Four year college or university degree') == 5.0
    assert book.code('respondent_birthregion2', 'U.S. (native born)') == 1.0
    with pytest.raises(AssertionError):
        book.code('educrec', 'Bachelors degree')


def test_g3_published_rows_reproduce(loaded):
    """G3: every published B-row lands within 1 percentage point."""
    d, meta, reps = loaded
    book = A.Book(meta)
    measure, _ = A.estimator(d, reps)
    misses = []
    for rid, name, var, base, values, published in A.reproduction_specs(d, book):
        if rid.endswith('-alt'):
            continue
        theta, se, _, n_base, _ = measure(values)
        if abs(100 * theta - published) > 1.0:
            misses.append((rid, name, round(100 * theta, 2), published))
    assert not misses, f'reproduction misses over 1 point: {misses}'


def test_percentages_within_a_question_sum_to_one(loaded):
    """Income and education bands partition their own base."""
    d, meta, reps = loaded
    book = A.Book(meta)
    measure, _ = A.estimator(d, reps)
    specs = {s[0]: s[3] for s in A.outcome_specs(d, book)}
    for family in (['income_lt_30k', 'income_30_75k', 'income_75_100k', 'income_ge_100k'],
                   ['edu_lt_hs', 'edu_hs', 'edu_some_college', 'edu_ba_plus'],
                   ['employed_full_time', 'employed_part_time', 'not_employed'],
                   ['civilians_often_sometimes', 'civilians_rarely_never']):
        total = sum(measure(specs[k])[0] for k in family)
        expected = 1.0 if family[0] != 'civilians_often_sometimes' else None
        if expected is not None:
            assert abs(total - 1.0) < 1e-9, f'{family} sums to {total}'
        else:
            assert total < 1.0, 'DK is in the qf3 denominator, so the two shares sum below 1'


def test_origin_groups_partition_their_universe(loaded):
    """Foreign-born region cells and U.S.-born parent cells each cover their universe once."""
    d, meta, reps = loaded
    book = A.Book(meta)
    groups = dict(A.origin_groups(d, book))
    fb = np.vstack([groups['Foreign born: ' + r] for r in A.REGIONS])
    assert fb.sum(axis=0).max() <= 1, 'a respondent fell in two birth regions'
    assert int(fb.any(axis=0).sum()) == 631
    usb = np.vstack([groups['U.S. born, parent from: ' + r] for r in A.REGIONS])
    assert usb.sum(axis=0).max() <= 1, 'a U.S.-born respondent fell in two parent regions'
    assert int(usb.any(axis=0).sum()) == int(groups['U.S. born: at least one foreign-born parent'].sum())
    both = groups['U.S. born: both parents U.S. born']
    assert not (both & groups['U.S. born: at least one foreign-born parent']).any()


def test_jrr_se_exceeds_srs_se(loaded):
    """The complex design loses precision: the JRR SE must beat the SRS approximation."""
    d, meta, reps = loaded
    book = A.Book(meta)
    measure, _ = A.estimator(d, reps)
    for _, _, _, _, values, _ in A.reproduction_specs(d, book)[:6]:
        theta, se, _, n, _ = measure(values)
        srs = np.sqrt(theta * (1 - theta) / n)
        assert se > srs, 'JRR SE below the SRS SE means the multiplier is wrong'
        assert (se / srs) ** 2 < 12, 'implausible design effect'


def test_outputs_and_audit_written():
    """G4: every variable used carries its codebook label in audit.json."""
    A.main()
    for name in ['report_reproduction.csv', 'cuts_by_nativity.csv', 'cuts_by_origin.csv', 'audit.json']:
        assert (A.OUT / name).exists(), name
    audit = json.loads((A.OUT / 'audit.json').read_text())
    assert audit['n_rows'] == 1001
    assert audit['variance']['multiplier'] == 1.0
    used = {v['variable'] for v in audit['variables_used']}
    for required in ['income', 'educrec', 'citizen', 'party', 'partyln', 'fertREC', 'qa2', 'qf3',
                     'qb2c', 'employ', 'respondent_birthregion2', 'father_birthregion2',
                     'mother_birthregion2']:
        assert required in used, required
    for v in audit['variables_used']:
        assert v['variable_label'], f"{v['variable']} has no label"
