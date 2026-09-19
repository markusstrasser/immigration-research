"""The incidence amount follows the live annual release, including arm changes."""
import json
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from incidence import live_annual_anchor


class AnnualAnchorTests(unittest.TestCase):
    def test_live_value_and_selected_arm_replace_historical_constant(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            arms = {"F": "zero", "G": "central"}
            (root / "audit.json").write_text(json.dumps({"central_arms": arms,
                                                         "params_sha256": "current"}))
            water = pd.DataFrame([dict(group="union", step=0, cumulative_bn=50.),
                                  dict(group="union", step=1, cumulative_bn=-100.)])
            water.to_csv(root / "waterfall.csv", index=False)
            pd.DataFrame([dict(group="union", item="F", arm="zero", total_bn=0.),
                          dict(group="union", item="F", arm="per_capita", total_bn=-20.)]
                         ).to_csv(root / "items_by_group.csv", index=False)
            self.assertEqual(live_annual_anchor(root, "union", "zero", arms, "current"), -100.)
            self.assertEqual(live_annual_anchor(root, "union", "per_capita", arms, "current"), -120.)
            water.loc[1, "cumulative_bn"] = -200.
            water.to_csv(root / "waterfall.csv", index=False)
            self.assertEqual(live_annual_anchor(root, "union", "per_capita", arms, "current"), -220.)
            with self.assertRaisesRegex(ValueError, "different parameters"):
                live_annual_anchor(root, "union", "zero", arms, "stale")
            with self.assertRaisesRegex(ValueError, "arm selection"):
                live_annual_anchor(root, "union", "zero", {"F": "zero"}, "current")


if __name__ == "__main__":
    unittest.main()
