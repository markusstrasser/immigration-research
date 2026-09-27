from pathlib import Path
import subprocess
import sys
import zipfile

import numpy as np
import pytest
import pandas as pd
from analysis import FIELDS, REPS, irs_diagnostic, load, predict, se, sha, validate_credit_identity, run


def test_composition_transport_exact_when_rates_stay_fixed():
    exposure = np.ones((32, 161)) * 100
    rate = np.arange(1, 33)[:, None]
    later = exposure.copy()
    later[:8] *= 2
    predicted = predict(exposure, exposure * rate, later, 'composition_transport')
    actual = (later * rate).reshape(4, 8, 161).sum(axis=1)
    np.testing.assert_allclose(predicted, actual / actual.sum(axis=0))
    assert abs(predicted[0, 0] - predict(exposure, exposure * rate, later, 'frozen_share')[0, 0]) > .01


def test_changed_rates_can_falsify_frozen_composition_model():
    exposure = np.ones((32, 161)) * 100
    old = np.ones((32, 161))
    later = old.copy()
    later[:8] *= 2
    predicted = predict(exposure, old * exposure, exposure, 'composition_transport')
    actual = (later * exposure).reshape(4, 8, 161).sum(axis=1)
    actual /= actual.sum(axis=0)
    assert abs(predicted[0, 0] - actual[0, 0]) > .1


def test_missing_training_support_rejected():
    exposure = np.ones((32, 161))
    exposure[0, 0] = 0
    with pytest.raises(ValueError, match='training support'):
        predict(exposure, np.ones_like(exposure), np.ones_like(exposure), 'composition_transport')


def test_negative_net_tax_cells_retained():
    exposure = np.ones((32, 161))
    outcomes = np.ones((32, 161))
    outcomes[:8] = -.1
    pred = predict(exposure, outcomes, exposure, 'composition_transport')
    assert pred[0, 0] < 0
    np.testing.assert_allclose(pred.sum(axis=0), 1)


def test_sdr_constant_and_perturbed_replicates():
    x = np.ones(161)
    assert se(x) == 0
    x[1:] += 1
    assert se(x) == 2


def test_pandemic_year_credit_identity_and_wrong_year_rejected():
    d = pd.DataFrame({'FEDTAX_BC': [2000], 'ACTC_CRD': [300], 'EIT_CRED': [100],
                      'CDC_CRD': [200], 'EIP_CRD': [1400], 'FEDTAX_AC': [0]})
    validate_credit_identity(d, 2022)
    with pytest.raises(AssertionError):
        validate_credit_identity(d, 2023)
    d.loc[0, 'FEDTAX_AC'] = 2
    with pytest.raises(AssertionError):
        validate_credit_identity(d, 2022)


def test_missing_xls_reader_fails_before_source_work(monkeypatch):
    monkeypatch.setattr('analysis.importlib.util.find_spec', lambda name: None)
    with pytest.raises(RuntimeError, match='--with xlrd'):
        run(None)


def malformed_cps_zip(path, mutation):
    """Two-member unit; alter one source invariant before exercising the real loader."""
    d = pd.DataFrame(0, index=range(2), columns=sorted(set(FIELDS)))
    d['PH_SEQ'], d['PPPOS'] = 1, [1, 2]
    d['A_AGE'], d['A_SEX'], d['PRPERTYP'] = [40, 41], [1, 2], 2
    d['PRCITSHP'], d['PENATVTY'], d['PEFNTVTY'], d['PEMNTVTY'] = 1, 57, 57, 57
    d['MARSUPWT'], d['SPM_WEIGHT'] = 10000, 10000
    d['SPM_ID'], d['SPM_HEAD'], d['SPM_NUMPER'] = 99, [1, 0], 2
    if mutation == 'head':
        d['SPM_HEAD'] = 0
    elif mutation == 'size':
        d['SPM_NUMPER'] = 3
    elif mutation == 'repeated':
        d.loc[1, 'SPM_WEIGHT'] = 20000
    elif mutation == 'sex':
        d.loc[1, 'A_SEX'] = 3
    else:
        raise ValueError(mutation)
    weights = pd.DataFrame(100, index=range(2), columns=REPS)
    weights['h_seq'], weights['PPPOS'] = 1, [1, 2]
    with zipfile.ZipFile(path, 'w') as z:
        z.writestr('pppub24.csv', d.to_csv(index=False))
        z.writestr('asec_csv_repwgt_2024.csv', weights.to_csv(index=False))


@pytest.mark.parametrize('optimized', [False, True])
@pytest.mark.parametrize('mutation,message', [
    ('head', 'SPM head mismatch'), ('size', 'SPM size mismatch'),
    ('repeated', 'Repeated SPM unit fields disagree'), ('sex', 'Invalid sex code'),
])
def test_malformed_source_rejected_with_and_without_optimization(tmp_path, mutation, message, optimized):
    path = tmp_path / 'malformed.zip'
    malformed_cps_zip(path, mutation)
    if not optimized:
        with pytest.raises(ValueError, match=message):
            load(2024, path)
        return
    code = ('import sys\nfrom pathlib import Path\nfrom analysis import load\n'
            'try:\n    load(2024, Path(sys.argv[1]))\n'
            'except ValueError as e:\n    print(e); sys.exit(0)\n'
            'raise SystemExit("Malformed source accepted under optimization")\n')
    result = subprocess.run([sys.executable, '-O', '-c', code, str(path)],
                            cwd=Path(__file__).parent, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    assert message in result.stdout


@pytest.mark.parametrize('optimized', [False, True])
def test_changed_irs_source_rejected_before_excel_read(tmp_path, optimized):
    raw = tmp_path / 'infra/immigration-fiscal/same_year_tax_2026_09_20/_cache'
    raw.mkdir(parents=True)
    (raw / '22in12ms.xls').write_bytes(b'changed source')
    lock = {'22in12ms.xls': {'sha256': 'not-the-hash'}}
    if not optimized:
        with pytest.raises(ValueError, match='IRS source drift'):
            irs_diagnostic(tmp_path, lock, {})
        return
    code = ('import sys\nfrom pathlib import Path\nfrom analysis import irs_diagnostic\n'
            'try:\n    irs_diagnostic(Path(sys.argv[1]), {"22in12ms.xls": {"sha256": "bad"}}, {})\n'
            'except ValueError as e:\n    print(e); sys.exit(0)\n'
            'raise SystemExit("Changed IRS source accepted under optimization")\n')
    result = subprocess.run([sys.executable, '-O', '-c', code, str(tmp_path)],
                            cwd=Path(__file__).parent, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    assert 'IRS source drift' in result.stdout


@pytest.mark.parametrize('changed_header,message', [
    ('year', 'does not declare Tax Year'), ('column', 'column header changed'),
])
def test_changed_irs_table_layout_rejected(tmp_path, monkeypatch, changed_header, message):
    raw = tmp_path / 'infra/immigration-fiscal/same_year_tax_2026_09_20/_cache'
    raw.mkdir(parents=True)
    path = raw / '22in12ms.xls'
    path.write_bytes(b'fixture')
    frame = pd.DataFrame('', index=range(28), columns=range(11))
    frame.iloc[0, 0] = 'Tax Year 2022'
    frame.iloc[3, 9] = 'Income tax after credits'
    frame.iloc[(0 if changed_header == 'year' else 3), (0 if changed_header == 'year' else 9)] = 'changed'
    monkeypatch.setattr('analysis.pd.read_excel', lambda *args, **kwargs: frame)
    with pytest.raises(ValueError, match=message):
        irs_diagnostic(tmp_path, {'22in12ms.xls': {'sha256': sha(path)}}, {})
