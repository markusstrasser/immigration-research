"""Reject wrong customs vintages and preserve filer eligibility semantics."""
from pathlib import Path
import sys

import pandas as pd
import pytest

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import policy_scope
from tax_side import filer_has_ssn


def test_current_bea_selector_never_uses_older_vintage():
    rows=[dict(part=part,which='set',end=end,delta_net_cost_bn=value)
          for part,value in [('customs_historical_pinned_bea',-16.60),
                             ('customs_historical_current_bea',-16.93)]
          for end in ['low','high']]
    assert policy_scope.customs_current_vintage(dict(rows=rows))==-16.93
    with pytest.raises(ValueError,match='unique named ends'):
        policy_scope.customs_current_vintage(dict(rows=rows[:2]))
    rows[-1]['end']='low'
    with pytest.raises(ValueError,match='unique named ends'):
        policy_scope.customs_current_vintage(dict(rows=rows))


def test_ssn_grouping_matches_filer_rule_with_mixed_units():
    d=pd.DataFrame(dict(TAX_ID=[1,1,1,2,2,3,3],DEP_STAT=[0,0,1,0,1,0,0],
                        unauth=[True,False,True,True,False,False,False]))
    ids=[3,1,2]
    reference=(~d.groupby('TAX_ID').apply(
        lambda g:g.loc[~g.DEP_STAT.gt(0),'unauth'].astype(bool).all(),
        include_groups=False)).reindex(ids).to_numpy()
    assert filer_has_ssn(d,ids).tolist()==reference.tolist()==[True,True,False]
    with pytest.raises(ValueError,match='nondependent filer'):
        filer_has_ssn(d,[4])
