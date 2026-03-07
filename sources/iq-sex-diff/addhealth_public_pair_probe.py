#!/usr/bin/env python3
"""Probe whether public Add Health files expose usable within-family linkage."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "addhealth"
OUT = DATA / "addhealth_public_pair_probe.json"


def main() -> None:
    w1 = pd.read_csv(DATA / "wave1" / "w1inhome_dvn.tab", sep="\t", nrows=6504, low_memory=False)
    w2 = pd.read_csv(DATA / "wave2" / "w2inhome_dvn.tab", sep="\t", nrows=4834, low_memory=False)

    sib_cols_w1 = [c for c in w1.columns if "studsib" in c.lower() or "twin" in c.lower()]
    sib_cols_w2 = [c for c in w2.columns if "h2sib" in c.lower() or "h2twin" in c.lower()]
    idish_w1 = [c for c in w1.columns if any(k in c.lower() for k in ["aid", "hh", "house", "family", "pair"])]
    idish_w2 = [c for c in w2.columns if any(k in c.lower() for k in ["aid", "hh", "house", "family", "pair"])]

    value_counts = {}
    for col in ["STUDSIBA", "TWINA", "STUDSIBB", "TWINB"]:
        s = pd.to_numeric(w1[col], errors="coerce")
        value_counts[col] = {str(k): int(v) for k, v in s.value_counts(dropna=False).head(10).items()}

    result = {
        "wave1_sibling_columns": sib_cols_w1,
        "wave2_sibling_columns": sib_cols_w2,
        "wave1_id_like_columns": idish_w1,
        "wave2_id_like_columns": idish_w2,
        "wave1_sibling_flag_value_counts": value_counts,
        "inference": (
            "Public wave I/II in-home files expose sibling/twin indicator slots "
            "but no obvious pair identifier or household/family linkage field usable "
            "for a clean within-family design."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
