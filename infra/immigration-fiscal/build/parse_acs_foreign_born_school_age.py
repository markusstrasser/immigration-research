#!/usr/bin/env python3
"""ACS 2023 foreign-born school-age children by state (EL fiscal pressure proxy)."""
from __future__ import annotations

from pathlib import Path

from paths import derived_root

OUT = derived_root() / "stage5"


def build_acs_foreign_born_school_age_panel(out_dir: Path | None = None) -> int:
    from parse_acs_stage5_panels import build_acs_stage5_panels

    _, school_n = build_acs_stage5_panels(out_dir)
    return school_n


if __name__ == "__main__":
    build_acs_foreign_born_school_age_panel()
