"""Boundary and conservation checks for exhaustive conditional receipt allocation."""
import unittest
import numpy as np
import pandas as pd
from builder import partition, residual_property, ratio_replicates, validate, required_share


class ReceiptTests(unittest.TestCase):
    def test_missing_proxy_cannot_move_all_receipts_to_other(self):
        with self.assertRaisesRegex(ValueError, 'Missing required incidence key'):
            required_share({}, 'federal_liability')
        self.assertEqual(required_share({}, 'foreign', external=1), 0)
        self.assertEqual(required_share({}, 'explicit', target_override=10), 0)
        self.assertEqual(required_share({'federal_liability': .12}, 'federal_liability'), .12)

    def test_signed_amounts_and_external_endpoints(self):
        for amount in [-47.460,0,663.685]:
            for share in [0,.12,1]:
                for external in [0,.5,1]:
                    target,other,outside=partition(amount,share,external)
                    self.assertAlmostEqual(target+other+outside,amount)
                    if external==1:self.assertEqual(target+other,0)
                    if amount<0:self.assertLessEqual(target,0)

    def test_known_independent_partition(self):
        # $200, one-quarter outside; target owns one-fifth of domestic pool.
        self.assertEqual(partition(200,.2,.25),(30,120,50))
        self.assertEqual(partition(-40,.25,.5),(-5,-15,-20))

    def test_reject_invalid_shares(self):
        for args in [(1,-.01,0),(1,1.01,0),(1,.2,1.1),(float('nan'),.2,0)]:
            with self.assertRaises(ValueError):partition(*args)

    def test_property_residual_is_not_full_pool_twice(self):
        self.assertEqual(residual_property(750,400),350)
        self.assertEqual(residual_property(750,750),0)
        with self.assertRaises(ValueError):residual_property(750,751)

    def test_share_denominator_and_zero_target(self):
        np.testing.assert_equal(ratio_replicates(np.zeros(161),np.ones(161)),0)
        for target,total in [(np.ones(2),np.zeros(2)),(np.ones(2)*2,np.ones(2))]:
            with self.assertRaises(ValueError):ratio_replicates(target,total)

    def test_duplicate_and_nonconservation_fail_loud(self):
        frame=pd.DataFrame([dict(scenario_id='complete',allocation='shared',category='asset',national_bn=-40,
                                 target_bn=-5,other_bn=-15,external_bn=-20,unallocated_bn=0,
                                 response_class='public_asset',causal_response_fixed=0)])
        validate(frame,-40)
        with self.assertRaises(ValueError):validate(pd.concat([frame,frame]),-80)
        altered=frame.copy();altered.loc[0,'target_bn']=0
        with self.assertRaises(AssertionError):validate(altered,-40)
        altered=frame.copy();altered.loc[0,'causal_response_fixed']=1
        with self.assertRaises(ValueError):validate(altered,-40)


if __name__=='__main__':unittest.main()
