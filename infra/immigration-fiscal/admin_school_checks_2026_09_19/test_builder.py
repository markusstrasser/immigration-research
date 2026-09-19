import unittest
import pandas as pd
from builder import area_mask, public_k12


class SchoolBoundary(unittest.TestCase):
    def test_2024_state_schema_not_legacy_st(self):
        frame = pd.DataFrame({"STATE": [6, 48, 36]})
        self.assertEqual(area_mask(frame, 48).tolist(), [False, True, False])
        self.assertEqual(area_mask(frame, 0).tolist(), [True, True, True])

    def test_excludes_private_preschool_and_college(self):
        frame = pd.DataFrame({"SCH": [2, 2, 2, 3, 2, 1],
                              "SCHG": [1, 2, 14, 8, 15, 8]})
        self.assertEqual(public_k12(frame).tolist(), [False, True, True, False, False, False])


if __name__ == "__main__":
    unittest.main()
