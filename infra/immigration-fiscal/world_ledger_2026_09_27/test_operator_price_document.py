"""The report may not silently omit a whole reading or one endpoint cell."""
from itertools import product

import pandas as pd
import pytest

from operator_price_document import KEYS, VARIANTS, WEIGHTS, validate_coverage


def grid():
    rows = product(('reading1', 'reading2'), ('low', 'high'), ('zero', 'upper'),
                   sorted(WEIGHTS), VARIANTS)
    frame = pd.DataFrame(rows, columns=[*KEYS, 'variant'])
    return frame, dict(readings=['reading1', 'reading2'], rows=len(frame))


def test_full_coverage_passes():
    frame, receipt = grid()
    validate_coverage(frame, receipt)


@pytest.mark.parametrize('omission', ['one_reading', 'all_readings', 'one_cell'])
def test_coverage_omission_stops(omission):
    frame, receipt = grid()
    broken = frame[frame.reading.eq('reading1')] if omission == 'one_reading' else (
        frame.iloc[:0] if omission == 'all_readings' else frame.iloc[1:])
    with pytest.raises(SystemExit, match='BLOCKED'):
        validate_coverage(broken, receipt)
