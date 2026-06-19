#!/usr/bin/env python3
"""ACS 2023 PUMS state health coverage by nativity/citizenship (KFF chart substitute)."""
from __future__ import annotations

from pathlib import Path

from paths import derived_root

OUT = derived_root() / "stage5"


def build_acs_immigrant_health_state_panel(out_dir: Path | None = None) -> int:
    from parse_acs_stage5_panels import build_acs_stage5_panels

    health_n, _ = build_acs_stage5_panels(out_dir)
    return health_n


if __name__ == "__main__":
    build_acs_immigrant_health_state_panel()
