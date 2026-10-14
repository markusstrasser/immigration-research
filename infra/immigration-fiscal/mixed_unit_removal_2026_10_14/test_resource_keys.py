"""Independent weighted-pool fixtures, including a known unweighted failure."""
import importlib.util
from pathlib import Path
import numpy as np
import pytest

spec=importlib.util.spec_from_file_location('tested_resource_keys',Path(__file__).with_name('resource_keys.py'))
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)


def test_unweighted_sharing_fails_and_weighted_sharing_repairs_it():
    old=np.array([100.,0.]);w=np.array([2.,1.]);unit=np.array([0,0])
    assert old@w!=np.full(2,old.sum()/2)@w
    new,gap=M.weighted_split(old,np.ones(2),unit,w,np.array([True]))
    assert new@w==pytest.approx(old@w,abs=1e-9)
    assert gap<1e-15


def test_signed_weights_and_zero_income_conserve_original_pool():
    old=np.array([30.,50.,20.,20.]);w=np.array([-1.,3.,2.,4.]);unit=np.array([0,0,1,1])
    new,_=M.weighted_split(old,np.array([10.,40.,0.,0.]),unit,w,np.ones(2,bool))
    np.testing.assert_array_equal(new[2:],old[2:])
    np.testing.assert_allclose(np.bincount(unit,weights=w*new),np.bincount(unit,weights=w*old),rtol=0,atol=1e-9)


def test_zero_signed_income_moment_blocks_nonzero_pool():
    with pytest.raises(ValueError,match='zero signed'):
        M.weighted_split(np.array([10.,20.]),np.ones(2),np.array([0,0]),np.array([-1.,1.]),np.array([True]))
