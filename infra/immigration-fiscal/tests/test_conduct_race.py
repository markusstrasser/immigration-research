"""Protect source-measured race, ethnicity and birthplace distinctions."""
import sys
from pathlib import Path
import unittest

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "build"))
from analyze_conduct_race import COLUMNS, classify, composition, ethnicity_bounds


def fixture():
    frame = pd.DataFrame(2, index=range(5), columns=COLUMNS)
    frame["RV0001"] = 30
    frame["RV0003"] = [2, 1, 3, 2, 6]
    frame["RV0004"] = [1, 2, 1, 1, 8]
    frame["V0945"] = [1, 2, 2, 1, -1]
    frame["V1951"] = [2, 2, 1, -1, 2]
    frame["V1952"] = [2, 1, 1, 2, 1]
    frame["V1953"] = [1, 2, 1, 1, 1]
    frame["V1585"] = [10., 20., 30., 40., 50.]
    return frame


class ConductRaceTests(unittest.TestCase):
    def test_hispanic_white_and_black_are_not_disjoint_raw_indicators(self):
        df = classify(fixture())
        self.assertEqual(df.loc[2, "race_official"], "hispanic_any_race")
        self.assertEqual(df.loc[4, "race_official"], "non_hispanic_multiracial")
        self.assertEqual(df.loc[2, "citizenship"], "us_citizen")
        self.assertEqual(df.loc[2, "birthplace"], "reported_other_country")

    def test_unknown_ethnicity_is_not_silently_observed_nonhispanic(self):
        df = classify(fixture())
        self.assertEqual(df.loc[3, "race_official"], "non_hispanic_black")
        self.assertEqual(df.loc[3, "race_explicit_ethnicity"], "ethnicity_unresolved")
        bounds = ethnicity_bounds(df).set_index("group")
        self.assertEqual(bounds.loc["hispanic_any_race", "weighted_lower"], 30.)
        self.assertEqual(bounds.loc["hispanic_any_race", "weighted_upper"], 70.)
        self.assertEqual(bounds.loc["non_hispanic_black_official_single_race", "weighted_lower"], 10.)
        self.assertEqual(bounds.loc["non_hispanic_black_official_single_race", "weighted_upper"], 50.)

    def test_disjoint_groups_conserve_each_prisoner_universe(self):
        table = composition(classify(fixture()))
        sums = table.groupby(["classification_basis", "prisoner_universe"]).share_of_prisoner_universe_pct.sum()
        self.assertTrue(sums.round(9).eq(100).all())
        total = table.loc[table.prisoner_universe.eq("all_prisoners")]
        self.assertTrue(total.groupby("classification_basis").sample_n.sum().eq(5).all())

    def test_unknown_status_and_birthplace_remain_unknown(self):
        df = classify(fixture())
        self.assertEqual(df.loc[4, "birthplace"], "birthplace_unresolved")
        self.assertEqual(df.loc[4, "citizenship"], "citizenship_unresolved")

    def test_changed_schema_or_invalid_weights_fail(self):
        frame = fixture()
        frame.loc[0, "RV0003"] = 44
        with self.assertRaises(ValueError):
            classify(frame)
        frame = fixture()
        frame.loc[0, "V1585"] = -1
        with self.assertRaises(ValueError):
            classify(frame)

    def test_official_race_matches_source_reconstruction(self):
        frame = fixture()
        frame.loc[0, "RV0003"] = 1
        with self.assertRaises(ValueError):
            classify(frame)
        frame = fixture()
        frame.loc[0, "V1957"] = 1
        frame.loc[0, "RV0003"] = 6
        self.assertEqual(classify(frame).loc[0, "race_official"], "non_hispanic_multiracial")


if __name__ == "__main__":
    unittest.main()
