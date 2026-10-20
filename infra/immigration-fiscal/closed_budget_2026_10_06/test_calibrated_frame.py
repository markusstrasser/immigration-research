"""Scientific count/eligibility regressions for the shared oct16 frame."""
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0,str(Path(__file__).resolve().parent))
import calibrated_frame as C


def test_own_calibration_preserves_latent_addition_and_unlocated_coverage(monkeypatch):
    d=pd.DataFrame({'PH_SEQ':[1,2,3], 'PPPOS':[1,1,1], 'civ':[True]*3,
        'pw_row4':[10.,20.,30.], 'PRCITSHP':[1,1,1], 'PEFNTVTY':[303,0,0], 'PEMNTVTY':[0,0,0]})
    monkeypatch.setattr(C,'calibration_factors',lambda d:np.array([.8,1.5,1.]))
    meta={'union_completion':{'observed_records':[{'PH_SEQ':2,'PPPOS':1,'people':20.}]},
        'population_v9':{'without_coverage':43.,'with_coverage':47.},
        'coverage':{'counts_by_generation_folded':{'G1':0.,'G2':2.,'G3plus':3.}},
        'native_minor_calibration':{'coverage_people_change_by_generation':{'G2':-1.}}}
    def gate(name,ok,**detail):
        assert ok,(name,detail)
    # Original10 observed +5 latent; only10 receives factor0.8.
    located,target,record=C.complete_calibrated(d,np.array([15.,20.,30.]),np.array([True,False,False]),{'meta':meta},gate)
    np.testing.assert_array_equal(target,[True,True,False])
    np.testing.assert_allclose(located,[13.,30.,30.])
    assert record['coverage_in_weights'] is False
    assert record['coverage_people']=={'G1':0.,'G2':1.,'G3plus':3.}
    complete,_,record=C.complete_calibrated(d,np.array([15.,20.,30.]),np.array([True,False,False]),{'meta':meta},gate,coverage=True)
    assert complete[target].sum()==47.
    assert complete[2]==30.
    # A positive omitted mass still needs observed recipients in its generation.
    meta['coverage']['counts_by_generation_folded']['G1']=1.
    meta['population_v9']['with_coverage']=48.
    with pytest.raises(AssertionError,match='coverage_G1_has_placement'):
        C.complete_calibrated(d,np.array([15.,20.,30.]),np.array([True,False,False]),{'meta':meta},gate,coverage=True)
