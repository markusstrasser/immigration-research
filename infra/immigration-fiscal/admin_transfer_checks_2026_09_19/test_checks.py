import unittest
import numpy as np
from pathlib import Path
from comparators import snap_months, bea_rows, rake_shift, read_comparators
from builder import distribute

class TransferChecks(unittest.TestCase):
    def test_real_pinned_admin_workbooks(self):
        here=Path(__file__).resolve().parent
        official,months,arms,_=read_comparators(here,Path("/Users/alien/research-data/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx"))
        self.assertAlmostEqual(months.amount_dollars.sum()/1e9,95.115241680)
        self.assertAlmostEqual(arms["SNAP_OASDI_only"]["social_security"],1449.964)
        self.assertAlmostEqual(arms["plus_SSI_BEA_persons"]["ssi"],65.134)
        self.assertEqual(len(official),9)
    def test_calendar_month_selection_rejects_fiscal_total_and_neighbors(self):
        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        rows = [("FY 2024",None,None,9999),("Dec 2023",None,None,9999)]
        rows += [(f"{m} 2024",None,None,i+1) for i,m in enumerate(months)]
        rows += [("Jan 2025",None,None,9999)]
        selected = snap_months(rows)
        self.assertEqual(selected.amount_dollars.sum(),78)
        with self.assertRaises(ValueError):
            snap_months(rows+[("Jan 2024",None,None,10)])
        with self.assertRaises(ValueError):
            snap_months(rows[:-2])

    def test_raking_replaces_old_adjustment_not_adds_whole_new_total(self):
        ratio, change = rake_shift(10,100,1.5,120)
        self.assertEqual(ratio,1.2)
        self.assertAlmostEqual(change,3)
        self.assertAlmostEqual(-15+change,-12)
        with self.assertRaises(ValueError):
            rake_shift(10,0,1.5,120)

    def test_snap_unit_amount_distributed_once(self):
        def allocate(values,index,eligible,n):
            return values[index]/np.bincount(index,minlength=n)[index]
        amounts=np.array([90.,40.])
        index=np.array([0,0,0,1])
        for arm in ["shared","personal"]:
            got=distribute(amounts,"unit",arm,index,2,allocate)
            np.testing.assert_allclose(np.bincount(index,weights=got),amounts)
            self.assertEqual(got.sum(),130)

    def test_bea_selects_declared_year_not_value_equal_to_year(self):
        rows=[("Title",None,None,None),("[Millions of dollars]",None,None,None),
              ("Line",None,"2023","2024"),("7","UI",2024,36468)]
        self.assertEqual(bea_rows(rows)[7]["amount_bn"],36.468)
        with self.assertRaises(ValueError):
            bea_rows(rows+[rows[2]])

if __name__=="__main__":
    unittest.main()
