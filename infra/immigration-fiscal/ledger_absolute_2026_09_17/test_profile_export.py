"""Small deterministic checks for the annual/lifetime boundary."""
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np
import pandas as pd

import profile_export as P


class ExportTests(unittest.TestCase):
    def fixture(self):
        ages = np.tile([5, 20, 30, 40, 50, 60, 70, 80], 3)
        d = pd.DataFrame({"A_AGE": ages})
        matrix = np.zeros((24, 8))
        matrix[:, 0], matrix[:, 1] = 100, 10
        personal = matrix.copy()
        personal[:, 0] = np.tile(np.arange(8) * 10, 3)
        masks = {g: np.arange(24) // 8 == i for i, g in enumerate(P.TARGETS)}
        state = dict(d=d, group=masks)
        weights = np.ones((24, 1))
        ctx = dict(weights=weights, civilian=np.ones(24, bool))
        charges = SimpleNamespace(columns=["G|central"], data=[np.full(24, -5.)])
        all_masks = dict(masks, **{P.UNION: np.ones(24, bool)})
        stats, inst = {}, {}
        for group, mask in all_masks.items():
            count = int(mask.sum() / 8)
            y = np.column_stack([matrix[:8] * count, np.full(8, -5. * count)])
            stats[group] = dict(n=np.full((8, 1), count), y=y[:, :, None],
                                h=np.full((8, 1, 1), count))
            inst[group] = np.full(8, count)
        def rebuild(c):
            self.assertEqual(c["allocation"], "personal")
            return charges, [], {"G": "central"}, {}, []
        return state, ctx, charges, stats, inst, matrix, personal, rebuild

    def test_export_preserves_shared_totals_and_rebuilds_personal(self):
        state, ctx, charges, stats, inst, matrix, personal, rebuild = self.fixture()
        with tempfile.TemporaryDirectory() as directory, patch.object(P, "_matrices", return_value=(matrix, personal, None)):
            audit = P.export_profiles(state, ctx, charges, {"G": "central"}, stats,
                                      np.array([3.]), inst, directory, personal_builder=rebuild)
            profiles = pd.read_csv(Path(directory) / "age_profiles.csv")
            components = pd.read_csv(Path(directory) / "age_profile_components.csv")
            P.validate_profiles(profiles, components)
            group = profiles[profiles.group.eq(P.UNION)]
            shared = group[group.allocation.eq("shared") & group.account.eq("expanded")]
            self.assertAlmostEqual(shared.net_total.sum(), (100 - 10 - 3 - 5 - 1) * 24)
            personal_rows = group[group.allocation.eq("personal") & group.account.eq("expanded")]
            self.assertNotEqual(shared.net_total.sum(), personal_rows.net_total.sum())
            self.assertEqual(set(audit["files"]), {"age_profiles.csv", "age_profile_components.csv"})
            self.assertEqual(audit["primary_allocation"], "personal")
            json.dumps(audit, allow_nan=False)
            invalid = pd.concat([profiles, profiles.iloc[:1]], ignore_index=True)
            with self.assertRaisesRegex(ValueError, "duplicate"):
                P.validate_profiles(invalid, components)
            corrupt = components.copy()
            corrupt.loc[0, "signed_total"] += 100
            with self.assertRaisesRegex(ValueError, "sum differs"):
                P.validate_profiles(profiles, corrupt)

    def test_refuses_shared_source_drift(self):
        state, ctx, charges, stats, inst, matrix, personal, rebuild = self.fixture()
        stats[P.TARGETS[0]]["y"][0, 0, 0] += 1
        with tempfile.TemporaryDirectory() as directory, patch.object(P, "_matrices", return_value=(matrix, personal, None)):
            with self.assertRaisesRegex(ValueError, "Shared base age schedule drift"):
                P.export_profiles(state, ctx, charges, {"G": "central"}, stats,
                                  np.array([3.]), inst, directory, personal_builder=rebuild)


if __name__ == "__main__":
    unittest.main()
