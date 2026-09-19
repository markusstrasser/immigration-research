import json, tempfile, unittest
from pathlib import Path
import numpy as np
import pandas as pd
from common import CW,PAYLOAD,check_sources,payroll,quantile,returns,sha,summary
from builder import band,source_tables

def person(unit,line,status,dependent=0,wage=0,agi=0,weight=1):
    d=dict(TAX_ID=unit,A_LINENO=line,FILESTAT=status,DEP_STAT=dependent,
           WSAL_VAL=wage,civilian=True,household=True)
    d.update({k:0 for k in PAYLOAD}); d['AGI']=agi
    d.update({k:weight for k in CW}); return d

class Boundaries(unittest.TestCase):
    def test_native_joint_payload_not_first_spouse_and_dependent(self):
        d=pd.DataFrame([person(11,1,1,wage=30),person(11,2,1,wage=70,agi=100),
                        person(11,3,5,dependent=2,wage=10,agi=10),person(12,1,6)])
        r,a=returns(d)
        self.assertEqual(r.A_LINENO.tolist(),[2,3])
        self.assertEqual(r.return_wages.tolist(),[100,10])
        self.assertEqual(r.AGI.sum(),110)
        self.assertEqual(a['zero_payload_nonfiling_core_units'],1)

    def test_zero_filer_weight_ambiguity_is_reported_not_tax_dollars(self):
        d=pd.DataFrame([person(1,1,3,weight=4),person(1,2,3,weight=7)])
        r,a=returns(d)
        self.assertEqual(a['zero_payload_count_weight_range'],dict(minimum=4,selected=4,maximum=7))
        self.assertEqual(a['zero_payload_ambiguous_head_weights'],1)
        self.assertEqual(r[PAYLOAD].to_numpy().sum(),0)

    def test_ambiguous_or_illegal_carriers_fail(self):
        with self.assertRaisesRegex(ValueError,'Multiple'):
            returns(pd.DataFrame([person(1,1,1,agi=100),person(1,2,1,agi=200)]))
        with self.assertRaisesRegex(ValueError,'Mixed'):
            returns(pd.DataFrame([person(1,1,1,agi=100),person(1,2,5)]))

    def test_zero_income_mixed_civilian_unit_count_bounds(self):
        d=pd.DataFrame([person(1,1,1,weight=4),person(1,2,1,weight=4)])
        d.loc[1,'civilian']=False
        r,a=returns(d)
        self.assertEqual(a['zero_payload_scoped_count_bounds']['civilian'],dict(minimum=0,maximum=4))
        self.assertEqual(a['zero_payload_ambiguous_scope_units'],1)

    def test_statutory_cap_and_self_employment_offset(self):
        d=pd.DataFrame(dict(WSAL_VAL=[0,160200,150000,0],SEMP_VAL=[0,10000,20000,10000],FRSE_VAL=[0,0,0,-10000]))
        p=payroll(d,160200)
        np.testing.assert_allclose(p['oasdi_se_base'],[0,0,10200,0])
        self.assertAlmostEqual(p['employee_self_payroll'][2],.062*150000+.0145*150000+.124*10200+.029*(.9235*20000))
        self.assertEqual(p['employer_payroll'][0],0)

    def test_agi_band_boundaries(self):
        np.testing.assert_array_equal(band([-1,0,1,4999,5000,9999,10000,9999999,10000000]),[0,0,1,1,2,2,3,17,18])

    def test_sdr_and_weighted_median(self):
        self.assertAlmostEqual(summary([10,9,11])['se_sampling'],2)
        self.assertEqual(quantile([30,10,20],[1,1,8],.5),20)
        self.assertEqual(quantile([10,20],[1,1],.5),10)
        with self.assertRaises(ValueError): quantile([1,2],[1,-1],.5)

    def test_fingerprint_drift_fails(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'raw'; p.write_bytes(b'first')
            lock={'raw':{'sha256':sha(p)}}; check_sources(t,lock)
            p.write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError,'fingerprint'): check_sources(t,lock)

    def test_pinned_irs_tables_and_year_error(self):
        raw=Path(__file__).parent/'_cache'
        if not raw.exists(): self.skipTest('Source acquisition required for integration check')
        bands,totals=source_tables(raw)
        self.assertEqual(totals['total_wages'],10204095705000)
        self.assertEqual(totals['income_tax_after_nonrefundable'],2108587001000)
        old=pd.read_excel(raw/'22in12ms.xls',header=None)
        self.assertEqual(old.iloc[8,10]*1000,2098923017000)

if __name__=='__main__': unittest.main()
