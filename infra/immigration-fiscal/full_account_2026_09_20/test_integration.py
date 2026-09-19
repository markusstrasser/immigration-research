import json
from pathlib import Path
import tempfile
import unittest

import pandas as pd

from builder import read_allocations, sha, verify_export
from welfare import response_pools


class IntegrationTests(unittest.TestCase):
    def test_complete_national_sum_cannot_hide_offsetting_unknowns(self):
        rows = []
        for category, unknown in [("a", 5), ("b", -5)]:
            rows.append(dict(scenario_id="test", allocation="personal", category=category,
                national_bn=50, target_bn=10, other_bn=40-unknown, external_bn=0,
                unallocated_bn=unknown, allocation_key="declared", response_class="household_direct"))
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/"input.csv"
            pd.DataFrame(rows).to_csv(path, index=False)
            _, total = read_allocations(path, 100)
            self.assertEqual(total.unallocated_bn.iloc[0], 0)
            self.assertEqual(total.unallocated_absolute_bn.iloc[0], 10)
            rows.append(rows[0])
            pd.DataFrame(rows).to_csv(path, index=False)
            with self.assertRaisesRegex(ValueError, "duplicate"):
                read_allocations(path, 100)

    def test_source_drift_fails_despite_unchanged_output(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            source, output = base/"source.txt", base/"result.csv"
            source.write_text("old")
            output.write_text("value\n1\n")
            (base/"audit.json").write_text(json.dumps(dict(
                source_hashes={str(source): sha(source)}, outputs={"result": sha(output)})))
            verify_export(output)
            source.write_text("new")
            with self.assertRaisesRegex(ValueError, "dependency changed"):
                verify_export(output)

    def test_incidence_on_labor_is_not_an_extra_corporate_remittance(self):
        r = pd.DataFrame([dict(scenario_id="cbo_collective", allocation="personal",
            category=c, response_class="household_direct", target_bn=value, unallocated_bn=0)
            for c, value in [("employee_hi", 20), ("corporate_labor", 10), ("personal_property_tax", 5)]])
        s = pd.DataFrame([dict(scenario_id="complete_preferred_F_per_capita", allocation="personal",
            category=c, response_class=cl, target_bn=value, unallocated_bn=0)
            for c, cl, value in [("medicare", "household_transfer", 30),
                                 ("business", "subsidy", 7), ("education", "service", 40)]])
        result = response_pools(r, s).iloc[0]
        self.assertEqual(result.direct_receipts_bn, 20)
        self.assertEqual(result.excluded_incidence_receipts_bn, 15)
        self.assertEqual(result.transfers_bn, 30)
        self.assertEqual(result.fixed_business_subsidies_bn, 7)


if __name__ == "__main__":
    unittest.main()
