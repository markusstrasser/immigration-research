#!/usr/bin/env python3
"""Build a compact PSID TAS transition panel from public-use bundles."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from psid_cds_build_panel import read_fixed_width, to_numeric


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "psid"
UNPACKED = DATA_DIR / "unpacked"

OUT_PANEL = DATA_DIR / "psid_tas_panel.parquet"
OUT_DIAG = DATA_DIR / "psid_tas_build_diagnostics.json"

WAVE_CONFIG = {
    2017: {
        "txt": UNPACKED / "TA2017/TA2017.txt",
        "do": UNPACKED / "TA2017/TA2017.do",
        "keep": {
            "TA170003": "current_fid",
            "TA170004": "current_seq",
            "TA170781": "hs_grad",
            "TA170782": "hs_gpa",
            "TA170783": "hs_gpa_max",
            "TA170785": "took_sat_act",
            "TA170787": "sat_reading",
            "TA170788": "sat_math",
            "TA170789": "act_composite",
            "TA170805": "college_gpa_k",
            "TA170806": "college_gpa_max_m",
            "TA170814": "college_gpa_y",
            "TA170815": "college_gpa_max_z",
            "TA171987": "cross_weight",
            "TA171989": "prior_cds_tas_weight",
        },
    },
    2019: {
        "txt": UNPACKED / "TA2019/TA2019.txt",
        "do": UNPACKED / "TA2019/TA2019.do",
        "keep": {
            "TA190003": "current_fid",
            "TA190004": "current_seq",
            "TA190918": "hs_grad",
            "TA190919": "hs_gpa",
            "TA190920": "hs_gpa_max",
            "TA190922": "took_sat_act",
            "TA190924": "sat_reading",
            "TA190925": "sat_math",
            "TA190926": "act_composite",
            "TA190944": "college_gpa_k",
            "TA190945": "college_gpa_max_m",
            "TA190954": "college_gpa_y",
            "TA190955": "college_gpa_max_z",
            "TA192199": "cross_weight",
            "TA192201": "prior_cds_tas_weight",
        },
    },
    2021: {
        "txt": UNPACKED / "TA2021/TA2021.txt",
        "do": UNPACKED / "TA2021/TA2021.do",
        "keep": {
            "TA210003": "current_fid",
            "TA210004": "current_seq",
            "TA210955": "hs_grad",
            "TA210956": "hs_gpa",
            "TA210957": "hs_gpa_max",
            "TA210959": "took_sat_act",
            "TA210961": "sat_reading",
            "TA210962": "sat_math",
            "TA210963": "act_composite",
            "TA210982": "college_gpa_k",
            "TA210983": "college_gpa_max_m",
            "TA210992": "college_gpa_y",
            "TA210993": "college_gpa_max_z",
            "TA212394": "cross_weight",
            "TA212395": "prior_cds_tas_weight",
        },
    },
    2023: {
        "txt": UNPACKED / "TA2023/TA2023.txt",
        "do": UNPACKED / "TA2023/TA2023.do",
        "keep": {
            "TA230003": "current_fid",
            "TA230004": "current_seq",
            "TA230991": "hs_grad",
            "TA230992": "hs_gpa",
            "TA230993": "hs_gpa_max",
            "TA230995": "took_sat_act",
            "TA230997": "sat_reading",
            "TA230998": "sat_math",
            "TA230999": "act_composite",
            "TA231018": "college_gpa_k",
            "TA231019": "college_gpa_max_m",
            "TA231029": "college_gpa_y",
            "TA231030": "college_gpa_max_z",
            "TA232404": "cross_weight",
            "TA232405": "prior_cds_tas_weight",
        },
    },
}


def build_individual_map() -> pd.DataFrame:
    ind_file = UNPACKED / "ind2023er/IND2023ER.txt"
    ind_do = UNPACKED / "ind2023er/IND2023ER.do"
    keep = {
        "ER30001": "family_id68",
        "ER30002": "person_id68",
        "ER32000": "sex",
        "ER34501": "fid_2017",
        "ER34502": "seq_2017",
        "ER34504": "age_2017",
        "ER34701": "fid_2019",
        "ER34702": "seq_2019",
        "ER34704": "age_2019",
        "ER34901": "fid_2021",
        "ER34902": "seq_2021",
        "ER34904": "age_2021",
        "ER35101": "fid_2023",
        "ER35102": "seq_2023",
        "ER35104": "age_2023",
    }
    frame = read_fixed_width(ind_file, ind_do, keep)
    for column in frame.columns:
        frame[column] = to_numeric(frame[column])
    return frame.drop_duplicates(subset=["family_id68", "person_id68"])


def build_wave_frame(year: int, ind_map: pd.DataFrame) -> pd.DataFrame:
    cfg = WAVE_CONFIG[year]
    frame = read_fixed_width(cfg["txt"], cfg["do"], cfg["keep"])
    for column in frame.columns:
        frame[column] = to_numeric(frame[column])

    id_map = ind_map.rename(
        columns={
            f"fid_{year}": "current_fid",
            f"seq_{year}": "current_seq",
            f"age_{year}": "age_years",
        }
    )[
        ["family_id68", "person_id68", "sex", "current_fid", "current_seq", "age_years"]
    ]
    id_map = id_map[
        id_map["current_fid"].notna()
        & id_map["current_seq"].notna()
        & (id_map["current_fid"] > 0)
        & (id_map["current_seq"] > 0)
    ].drop_duplicates(subset=["current_fid", "current_seq"])

    frame = frame.merge(id_map, on=["current_fid", "current_seq"], how="left", validate="many_to_one")
    frame["wave"] = year
    frame["female"] = frame["sex"].map({2: 1, 1: 0})
    frame["pair_id68"] = frame["family_id68"] * 1000.0 + frame["person_id68"]
    frame["source"] = "PSID_TAS"
    return frame


def build_panel() -> tuple[pd.DataFrame, dict[str, object]]:
    ind_map = build_individual_map()
    diagnostics: dict[str, object] = {
        "waves": {},
        "ind_map_rows": int(len(ind_map)),
    }
    frames: list[pd.DataFrame] = []

    for year in sorted(WAVE_CONFIG):
        frame = build_wave_frame(year, ind_map)
        frames.append(frame)
        diagnostics["waves"][str(year)] = {
            "rows": int(len(frame)),
            "with_stable_id": int(frame["family_id68"].notna().sum()),
            "with_sex": int(frame["sex"].notna().sum()),
            "with_cross_weight": int(frame["cross_weight"].notna().sum()),
        }

    panel = pd.concat(frames, ignore_index=True)
    diagnostics["panel_rows"] = int(len(panel))
    diagnostics["panel_unique_people"] = int(panel["pair_id68"].nunique())
    diagnostics["panel_unique_families68"] = int(panel["family_id68"].nunique())
    return panel, diagnostics


def main() -> None:
    panel, diagnostics = build_panel()
    OUT_PANEL.parent.mkdir(parents=True, exist_ok=True)
    panel.to_parquet(OUT_PANEL, index=False)
    OUT_DIAG.write_text(json.dumps(diagnostics, indent=2), encoding="utf-8")
    print(f"wrote {OUT_PANEL}")
    print(f"wrote {OUT_DIAG}")
    print(json.dumps(diagnostics, indent=2))


if __name__ == "__main__":
    main()
