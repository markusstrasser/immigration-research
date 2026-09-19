import unittest
import numpy as np
import pandas as pd
from cohorts import education3
from sensitivities import npv, retention_after_exit, age_vector


class ProjectionTests(unittest.TestCase):
    def setUp(self):
        self.life=pd.DataFrame({"Lx":np.ones(101),"lx":np.ones(101)})

    def test_education_missing_is_not_dropout(self):
        x=education3(pd.Series([0,11,12,13,20,21,np.nan,-9]))
        self.assertEqual(x.iloc[:5].tolist(),[0,0,1,2,2])
        self.assertTrue(x.iloc[5:].isna().all())

    def test_exit_does_not_erase_pre_exit_flows(self):
        retain=retention_after_exit(25,10,.3)
        self.assertTrue(np.array_equal(retain[:10],np.ones(10)))
        self.assertTrue(np.array_equal(retain[10:],np.full(66,.7)))
        self.assertAlmostEqual(npv(np.ones(101),self.life,25,0,retain),10+66*.7)

    def test_zero_exit_exact_oracle(self):
        p=np.arange(101,dtype=float)-25
        self.assertEqual(npv(p,self.life),npv(p,self.life,resident=retention_after_exit(25,10,0)))

    def test_discount_clock_starts_at_valuation_age(self):
        p=np.zeros(101); p[25]=1.; p[26]=1.
        self.assertAlmostEqual(npv(p,self.life,25,.03),1+1/1.03)

    def test_invalid_retention_fails(self):
        with self.assertRaises(ValueError):
            retention_after_exit(25,10,1.1)
        with self.assertRaises(ValueError):
            npv(np.ones(101),self.life,resident=np.linspace(0,1,76))

    def test_age_band_boundaries_and_missing_profile(self):
        p=pd.DataFrame({"group":["a"]*8,"band":range(8),"net_per_person":range(8)})
        a=age_vector(p,"a")
        self.assertEqual([a[x] for x in [0,17,18,24,25,34,35,64,65,74,75,100]],[0,0,1,1,2,2,3,5,6,6,7,7])
        with self.assertRaises(ValueError):
            age_vector(p.iloc[:-1],"a")


if __name__=="__main__":
    unittest.main()
