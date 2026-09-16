"""Regression check: the World Bank GDP pull reads its pinned cache and never touches the network
when the cache exists, and a live pull writes the cache.

Catalogued failure (2026-09-16 rebuild): ``imf_gdp_per_capita_panel`` went from 1,409 to 1,430 rows
between two builds because ``_fetch_wb_gdp`` pulled the World Bank API live every time, with no
input on disk to diff against.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "build"))


class WorldBankCache(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        (d / "data").mkdir()
        (d / "derived").mkdir()
        self.env = mock.patch.dict(
            os.environ, {"PNY_DATA_ROOT": str(d / "data"), "DERIVED_ROOT": str(d / "derived")}
        )
        self.env.start()
        sys.modules.pop("build_tier_a_context_panels", None)
        import build_tier_a_context_panels as m  # noqa: E402

        self.m = m
        m.OUT.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def test_pinned_cache_is_used_without_network(self):
        m = self.m
        m.WB_CACHE.parent.mkdir(parents=True)
        m.WB_CACHE.write_text(json.dumps({
            "MEX": [{"date": "2020", "value": 8000.0}, {"date": "2021", "value": None}],
            "USA": [{"date": "2020", "value": 60000.0}],
        }))
        with mock.patch("requests.get", side_effect=AssertionError("network call with cache present")):
            m._fetch_wb_gdp()
        import pandas as pd

        df = pd.read_csv(m.OUT / "imf_gdp_per_capita_panel.csv")
        self.assertEqual(len(df), 2, "null value dropped, two rows kept")
        self.assertEqual(set(df["iso3"]), {"MEX", "USA"})

    def test_live_pull_writes_cache(self):
        m = self.m
        payload = [{"page": 1}, [{"date": "2020", "value": 1.0}]]
        fake = mock.Mock()
        fake.json.return_value = payload
        with mock.patch("requests.get", return_value=fake) as get:
            m._fetch_wb_gdp()
        self.assertTrue(m.WB_CACHE.exists())
        self.assertEqual(get.call_count, len(("MEX", "USA") + m.HANSON_ORIGINS))
        self.assertEqual(json.loads(m.WB_CACHE.read_text())["MEX"], payload[1])

    def test_partial_failure_does_not_pin_a_broken_vintage(self):
        m = self.m
        good = mock.Mock()
        good.json.return_value = [{"page": 1}, [{"date": "2020", "value": 1.0}]]
        bad = mock.Mock()
        bad.json.side_effect = ValueError("not json")
        with mock.patch("requests.get", side_effect=[good, bad] + [good] * 50):
            m._fetch_wb_gdp()
        self.assertFalse(m.WB_CACHE.exists(), "cache must not be written when a country failed")


if __name__ == "__main__":
    unittest.main()
