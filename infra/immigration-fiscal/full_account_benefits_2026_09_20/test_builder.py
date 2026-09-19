"""Economic accounting identities and interface guards, not golden-output tests."""
import unittest
import numpy as np
import pandas as pd
from builder import accounting, integrate, RESPONSE_COLUMNS


class AccountingTests(unittest.TestCase):
    def test_included_tax_transfer_not_free_income(self):
        a = accounting(80, 20, 0, 40, 50, 0, 1)
        b = accounting(40, 60, 0, 40, 50, 0, 1)
        self.assertEqual(a['conditional_net_benefit_bn'], 90)
        self.assertEqual(a['conditional_net_benefit_bn'], b['conditional_net_benefit_bn'])

    def test_transfer_phaseout_cancels_only_with_full_recycling(self):
        for saving in (-9., 0., 12.):
            full = accounting(40, 10, saving, 80, 100, 0, 1)
            self.assertEqual(full['conditional_net_benefit_bn'], 30)
            private = accounting(40, 10, saving, 80, 100, 0, 0)
            self.assertEqual(private['conditional_net_benefit_bn'], 40-saving)

    def test_overlap_deducted_once_and_break_even(self):
        base = accounting(40, 10, 3, 80, 100, 7, 1)
        self.assertEqual(base['budget_change_bn'], -14)
        self.assertEqual(base['private_after_transfers_bn'], 37)
        self.assertEqual(base['conditional_net_benefit_bn'], 23)
        close = accounting(40, 10, 3, 80, 100, 30, 1)
        self.assertEqual(close['conditional_net_benefit_bn'], 0)
        self.assertIsNone(accounting(40, 10, 0, 0, 0, 0, 0)['maximum_additional_overlap_before_zero_bn'])

    def test_symmetric_fee_grossup_does_not_change_welfare(self):
        for fee in (0., 30., 100.):
            result = accounting(5, 4, 0, 20+fee, 50+fee, 0, 1)
            self.assertEqual(result['conditional_net_benefit_bn'], -21)

    def test_interface_refuses_defaults_duplicates_and_invalid_conventions(self):
        benefit = pd.DataFrame([dict(scenario_id='test', private_after_tax_wtp_bn=5.,
                                    induced_current_receipts_bn=4., source_transfer_saving_bn=-3.)])
        response = pd.DataFrame([['test', 'direct', 20., 50., 2., 1., 'source_2017', 'declared counterfactual']],
                                columns=RESPONSE_COLUMNS)
        out = integrate(benefit, response)
        self.assertEqual(out.conditional_net_benefit_bn.iloc[0], -23)
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            integrate(benefit, pd.concat([response, response]))
        for field, value in [('source_rule', np.nan), ('transfer_phaseout', 'unknown'),
                             ('receipt_change_bn', np.inf), ('fiscal_recycling_weight', .5),
                             ('tax_overlap_bn', -1.)]:
            bad = response.copy()
            bad.loc[0, field] = value
            with self.assertRaises(ValueError):
                integrate(benefit, bad)


if __name__ == '__main__':
    unittest.main()
