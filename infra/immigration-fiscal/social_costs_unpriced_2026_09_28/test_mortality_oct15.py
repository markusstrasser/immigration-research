import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('live_crime_mortality',HERE/'mortality_oct15.py')
producer=importlib.util.module_from_spec(spec)
spec.loader.exec_module(producer)


def test_source_prices_close_current_P7_and_every_basis_rate():
    tables,receipt=producer.build()
    rows=pd.DataFrame(tables['mortality_pairing_rows.csv'])
    uniform=rows[rows.valuation=='dot_uniform']
    np.testing.assert_allclose(uniform.lineage_victim_delta_bn,0,rtol=0,atol=1e-9)
    assert len(rows)==6 and rows.groupby(['valuation','real_discount_rate']).size().eq(2).all()
    assert rows.groupby('end').held_lineage_fear_bn.nunique().eq(1).all()
    assert rows.groupby('end').held_lineage_security_bn.nunique().eq(1).all()
    assert all(receipt['gates'].values())


def test_partial_native_publication_fails_closed(monkeypatch,tmp_path):
    path=producer.VICTIM/'derived/oct15/mortality_receipt.json'
    original=producer.digest
    def changed(p):
        return 'changed' if p == producer.VICTIM/'derived/oct15/mortality_arms.csv' else original(p)
    monkeypatch.setattr(producer,'digest',changed)
    with pytest.raises(ValueError,match='partial/stale live mortality publication'):
        producer.validated_inputs()


def test_unknown_registry_basis_fails_before_output(monkeypatch):
    original=producer.validated_inputs()
    old,receipt,arms,p7_path,receipt_path=original
    receipt=dict(receipt,valuation_choices=[{'valuation':'dot_uniform','real_discount_rate':0}])
    monkeypatch.setattr(producer,'validated_inputs',lambda:(old,receipt,arms,p7_path,receipt_path))
    with pytest.raises(ValueError,match='wrong mortality basis/rate'):
        producer.build()
