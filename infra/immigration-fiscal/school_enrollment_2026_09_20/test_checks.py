import tempfile
import unittest
from pathlib import Path
import zipfile

import numpy as np
import pandas as pd

from measurement import FIELDS, public_k12, origin_masks, fixed_records, field, sdr, missing_replicate_guard
from builder import coefficients, apply_rates

def people(n):
    d=pd.DataFrame(-1,index=range(n),columns=list(FIELDS))
    d['PRCITSHP']=1
    d['PENATVTY']=57
    d['PEMNTVTY']=57
    d['PEFNTVTY']=57
    d['PRDTHSP']=0
    return d

class Boundaries(unittest.TestCase):
    def test_only_zero_weight_nonperson_can_lack_replicates(self):
        d=pd.DataFrame(dict(row=[np.nan,0],PRTAGE=[-1,8],PRPERTYP=[-1,1],PWSUPWGT=[0,100]))
        self.assertEqual(missing_replicate_guard(d).tolist(),[False,True])
        d.loc[0,'PWSUPWGT']=1
        with self.assertRaises(ValueError):
            missing_replicate_guard(d)

    def test_child_adult_grade_and_age_branches(self):
        d=people(10)
        d['PRTAGE']=[4,5,14,15,18,27,13,8,21,4]
        d['PRPERTYP']=[1,1,1,2,2,2,1,1,2,1]
        d['PESCH35']=1
        d['PESCH614']=1
        d['PECHPUB']=1
        d['PECHGRDE']=[3,4,16,-1,-1,-1,2,8,-1,2]
        d['PESSCHOL']=1
        d['PEPUBLIC']=1
        d['PRGRADE']=[-1,-1,-1,7,12,12,-1,-1,13,-1]
        d.loc[7,'PECHPUB']=2
        self.assertEqual(public_k12(d).tolist(),[True,True,True,True,True,True,False,False,False,False])
        # A positive grade cannot override a no-enrollment answer.
        d.loc[4,'PESSCHOL']=2
        self.assertFalse(public_k12(d)[4])

    def test_canonical_union_is_not_unqualified_selfid_or(self):
        d=people(4)
        d.loc[0,['PRCITSHP','PENATVTY']]=[5,303]
        d.loc[1,'PEMNTVTY']=303
        d.loc[2,'PRDTHSP']=1
        d.loc[3,['PRDTHSP','PEMNTVTY']]=[1,301]
        masks=origin_masks(d)
        self.assertEqual(masks['target'].tolist(),[True,True,True,False])
        self.assertTrue(masks['broad_or'].all())

    def test_sharing_keeps_unequal_receiver_weights_and_cost_once(self):
        d=people(2)
        weights=np.repeat(np.array([[2.],[5.]]),161,axis=1)
        # One $100 pupil cost shared equally; target contains the second person.
        b=coefficients(d,weights,np.array([0,0]),1,np.array([False,True]),np.array([100.,0.]),np.array(['p','p']),'shared')
        self.assertAlmostEqual(b['p'][0]*1e9,-250)
        personal=coefficients(d,weights,np.array([0,0]),1,np.ones(2,bool),np.array([100.,0.]),np.array(['p','p']),'personal')
        self.assertAlmostEqual(personal['p'][0]*1e9,-200)

    def test_replacement_is_delta_not_double_add(self):
        b={'c':np.full(161,-100.)}
        r={'c':np.full(161,.9)}
        result=apply_rates(b,r,np.full(161,-80.))
        self.assertAlmostEqual(result['balance_change_bn'],-10.)
        self.assertAlmostEqual(result['updated_signed_bn'],-90.)
        self.assertEqual(result['se_october_bn'],0)

    def test_fixed_width_fail_loud_and_positions(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'bad.zip'
            with zipfile.ZipFile(path,'w') as archive:
                archive.writestr('records.dat','00123\n123\n')
            with self.assertRaises(ValueError):
                fixed_records(path,5)
        records=np.array([b'0123407890'],dtype='S10')
        self.assertEqual(field(records,6,7).tolist(),[7])

    def test_variance_and_covariance_envelope(self):
        values=np.ones(161)
        values[1:]=2
        self.assertAlmostEqual(float(sdr(values)),2.)
        with self.assertRaises(ValueError):
            sdr(np.ones(80))

if __name__=='__main__':
    unittest.main()
