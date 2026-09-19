import unittest
import numpy as np
from builder import payroll_proxy


class PayrollTests(unittest.TestCase):
    def test_zero_and_negative_income(self):
        x=payroll_proxy([0,-10],[0,-100],[0,0])
        np.testing.assert_array_equal(x['both_sides_payroll_proxy'],[0,0])

    def test_shared_cap_prevents_double_taxable_base(self):
        x=payroll_proxy([160000,200000],[100000,100000],[0,0])
        np.testing.assert_array_equal(x['oasdi_base_proxy'],[168600,168600])
        np.testing.assert_array_equal(x['self_employment_oasdi_base_proxy'],[8600,0])
        self.assertAlmostEqual(x['employer_hi_proxy'][1],2900)

    def test_business_and_farm_losses_offset_before_tax(self):
        x=payroll_proxy([0],[1000],[-900])
        self.assertEqual(x['self_employment_net_proxy'][0],0)

    def test_self_employment_has_both_sides_not_extra_employer(self):
        x=payroll_proxy([0],[100000],[0])
        self.assertEqual(x['employer_oasdi_proxy'][0],0)
        self.assertAlmostEqual(x['both_sides_payroll_proxy'][0],92350*.153)
        self.assertEqual(x['employee_and_self_payroll_proxy'][0],x['both_sides_payroll_proxy'][0])


if __name__=='__main__':
    unittest.main()
