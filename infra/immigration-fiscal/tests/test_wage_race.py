"""Disjoint race/ethnicity, income windows and weighted-denominator regressions."""
from collections import defaultdict
from pathlib import Path
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'build'))
from analyze_wage_race import COLUMNS, WEIGHTS, add_chunk, check_partitions, group_masks, outcome_matrix, race_codes, selected_frame
from analyze_arrival_cohorts import ratios, sdr_estimate


def frame(rows):
    defaults = dict(AGEP=30,SEX=1,NATIVITY=1,POBP=1,HISP=1,RAC1P=1,RACBLK=0,
                    SCHL=16,ESR=1,RELSHIPP=20,WAGP=0,PERNP=0,ADJINC=1_000_000)
    data = pd.DataFrame([{**defaults,**r} for r in rows])
    return pd.concat([data,pd.DataFrame(np.ones((len(rows),81)),columns=WEIGHTS)],axis=1)


class WageRaceTests(unittest.TestCase):
    def test_hispanic_priority_and_black_multiracial_sensitivity(self):
        d = frame([dict(HISP=2,RAC1P=2,RACBLK=1),dict(RAC1P=2,RACBLK=1),
                   dict(RAC1P=9,RACBLK=1),dict(RAC1P=6),dict(RAC1P=9),dict()])
        np.testing.assert_array_equal(race_codes(d),[0,1,4,3,4,2])
        np.testing.assert_array_equal(race_codes(d,True),[0,1,1,3,4,2])
        d.loc[0,'RACBLK']=0
        with self.assertRaisesRegex(ValueError,'Inconsistent'):
            race_codes(d)

    def test_current_employment_and_annual_wages_are_different_denominators(self):
        d = frame([dict(ESR=1,WAGP=0,PERNP=-100),dict(ESR=3,WAGP=100,PERNP=100),
                   dict(ESR=2,WAGP=200,PERNP=250)])
        d['PWGTP']= [1,2,1]
        matrix=outcome_matrix(d,2)
        weighted=d.PWGTP.to_numpy()@matrix
        self.assertEqual(weighted[COLUMNS.index('wages')]/weighted[0],200)
        self.assertEqual(weighted[COLUMNS.index('earnings')]/weighted[0],175)
        self.assertEqual(weighted[COLUMNS.index('employed_wages')]/weighted[1],200)
        self.assertEqual(weighted[COLUMNS.index('employed_earnings')]/weighted[1],150)
        self.assertAlmostEqual(weighted[COLUMNS.index('positive_wages')]/weighted[2],800/3)
        self.assertEqual(weighted[COLUMNS.index('negative_earnings')],1)

    def test_civilian_noninstitutional_selection_retains_noninstitutional_gq(self):
        d=frame([dict(),dict(RELSHIPP=37),dict(RELSHIPP=38),dict(ESR=4),dict(ESR=5),dict(AGEP=65)])
        self.assertEqual(selected_frame(d).index.tolist(),[0,2])
        d.loc[0,'WAGP']=np.nan
        with self.assertRaisesRegex(ValueError,'Missing adult'):
            selected_frame(d)

    def test_partitions_conserve_every_replicate_without_summing_aggregates(self):
        d=frame([dict(NATIVITY=n,HISP=h,RAC1P=r,RACBLK=b,WAGP=100,PERNP=120)
                 for n in (1,2) for h,r,b in [(2,2,1),(1,2,1),(1,1,0),(1,6,0),(1,9,1)]])
        d.loc[0,'PWGTP1']=-1
        sums=defaultdict(lambda:np.zeros((81,len(COLUMNS))))
        counts=defaultdict(lambda:np.zeros(3,dtype=int))
        add_chunk(d,1,sums,counts)
        check_partitions(sums)
        self.assertEqual(sums[('aggregate','native','all')][1,0],3)
        groups=group_masks(d)
        self.assertEqual(groups[('black_alone','native','nonhisp_black')].sum(),1)
        self.assertEqual(groups[('black_any_race','native','nonhisp_black')].sum(),2)

    def test_sdr_difference_preserves_nested_group_covariance(self):
        a=np.ones(81)*10
        a[1:]=np.tile([9,11],40)
        b=a-3
        self.assertEqual(sdr_estimate(a-b)['acs_sdr_se'],0)
        self.assertEqual(sdr_estimate(a)['acs_sdr_se'],2)
        with self.assertRaises(ValueError):
            ratios(a,np.zeros(81))


if __name__=='__main__':
    unittest.main()
