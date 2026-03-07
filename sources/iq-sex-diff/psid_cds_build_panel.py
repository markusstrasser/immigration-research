#!/usr/bin/env python3
"""Build a compact PSID CDS panel from the downloaded public-use bundles."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "psid"
UNPACKED = DATA_DIR / "unpacked"

OUT_PANEL = DATA_DIR / "psid_cds_panel.parquet"
OUT_DIAG = DATA_DIR / "psid_cds_build_diagnostics.json"

WAVE_CONFIG = {
    1997: {
        "score_file": UNPACKED / "CDS1997/1997/CHILD97.txt",
        "score_do": UNPACKED / "CDS1997/1997/CHILD97.do",
        "score_keep": {
            "CHLDID97": "core_fid",
            "CHLDSN97": "core_sn",
            "Q3AGE": "age_years_reported",
            "Q3A3": "grade_in_school",
            "Q3LW_SS": "letter_word_std",
            "Q3PC_SS": "passage_comp_std",
            "Q3BRE_SS": "broad_reading_std",
            "Q3CAL_SS": "calculation_std",
            "Q3AP_SS": "applied_problems_std",
            "Q3BMA_SS": "broad_math_std",
            "Q3LWPR": "letter_word_pr",
            "Q3PCPR": "passage_comp_pr",
            "Q3BRPR": "broad_reading_pr",
            "Q3CALPR": "calculation_pr",
            "Q3APPR": "applied_problems_pr",
            "Q3BMPR": "broad_math_pr",
        },
        "demog_file": UNPACKED / "CDS1997/1997/DEMOG1997.txt",
        "demog_do": UNPACKED / "CDS1997/1997/DEMOG1997.do",
        "demog_keep": {
            "DEMID97": "core_fid",
            "DEMSN97": "core_sn",
            "AGEATCH": "age_months",
            "CH97PRWT": "child_weight",
            "SBLNUM97": "bio_siblings_in_home",
            "BIOPR97": "bio_parents_in_home",
            "BIOGPR97": "bio_grandparents_in_home",
        },
        "idmap_file": UNPACKED / "CDS1997/1997/IDMAP97.txt",
        "idmap_do": UNPACKED / "CDS1997/1997/IDMAP97.do",
        "idmap_keep": {
            "CHILDID97": "core_fid",
            "CHILDSN97": "core_sn",
            "PCGID97": "pcg_fid",
            "PCGSN97": "pcg_sn",
        },
    },
    2002: {
        "score_file": UNPACKED / "CDS2002/2002/ASSESSMT.txt",
        "score_do": UNPACKED / "CDS2002/2002/ASSESSMT.do",
        "score_keep": {
            "ASMTID01": "core_fid",
            "ASMTSN01": "core_sn",
            "Q24B2": "grade_in_school",
            "Q24IWAGE": "age_months",
            "Q24LWSS": "letter_word_std",
            "Q24PCSS": "passage_comp_std",
            "Q24BRSS": "broad_reading_std",
            "Q24APSS": "applied_problems_std",
            "Q24LWPR": "letter_word_pr",
            "Q24PCPR": "passage_comp_pr",
            "Q24BRPR": "broad_reading_pr",
            "Q24APPR": "applied_problems_pr",
        },
        "demog_file": UNPACKED / "CDS2002/2002/DEMOG.txt",
        "demog_do": UNPACKED / "CDS2002/2002/DEMOG.do",
        "demog_keep": {
            "DEMID01": "core_fid",
            "DEMSN01": "core_sn",
            "CH02PRWT": "child_weight",
            "SBLNUM03": "bio_siblings_in_home",
            "BIOPR03": "bio_parents_in_home",
            "BIOGPR03": "bio_grandparents_in_home",
        },
        "idmap_file": UNPACKED / "CDS2002/2002/IDMAP02.txt",
        "idmap_do": UNPACKED / "CDS2002/2002/IDMAP02.do",
        "idmap_keep": {
            "CHLDID02": "core_fid",
            "CHLDSN02": "core_sn",
            "PCG68ID02": "pcg_id68",
            "PCGPN02": "pcg_pn68",
        },
    },
    2007: {
        "score_file": UNPACKED / "CDS2007/2007/ASSESS07.txt",
        "score_do": UNPACKED / "CDS2007/2007/ASSESS07.do",
        "score_keep": {
            "ASMID07": "core_fid",
            "ASMSN07": "core_sn",
            "Q34B3": "grade_in_school",
            "Q34IWAGE": "age_months",
            "Q34LWSS": "letter_word_std",
            "Q34PCSS": "passage_comp_std",
            "Q34BRSS": "broad_reading_std",
            "Q34APSS": "applied_problems_std",
            "Q34LWPR": "letter_word_pr",
            "Q34PCPR": "passage_comp_pr",
            "Q34BRPR": "broad_reading_pr",
            "Q34APPR": "applied_problems_pr",
        },
        "demog_file": UNPACKED / "CDS2007/2007/DEMOG07.txt",
        "demog_do": UNPACKED / "CDS2007/2007/DEMOG07.do",
        "demog_keep": {
            "DEMID07": "core_fid",
            "DEMSN07": "core_sn",
            "CH07WT": "child_weight",
            "SBLNUM07": "bio_siblings_in_home",
            "BIOPR07": "bio_parents_in_home",
            "BIOGPR07": "bio_grandparents_in_home",
        },
        "idmap_file": UNPACKED / "CDS2007/2007/IDMAP07.txt",
        "idmap_do": UNPACKED / "CDS2007/2007/IDMAP07.do",
        "idmap_keep": {
            "CHILDID07": "core_fid",
            "CHILDSN07": "core_sn",
            "PCG68ID07": "pcg_id68",
            "PCGPN07": "pcg_pn68",
        },
    },
}


def parse_infix_layout(path: Path) -> dict[str, tuple[int, int]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"\binfix\b(.*?)\busing\b", text, flags=re.S | re.I)
    if not match:
        raise ValueError(f"could not find infix block in {path}")

    layout: dict[str, tuple[int, int]] = {}
    for name, start, end in re.findall(r"([A-Za-z][A-Za-z0-9_]+)\s+(\d+)\s*-\s*(\d+)", match.group(1)):
        layout[name] = (int(start) - 1, int(end))
    return layout


def read_fixed_width(txt_path: Path, do_path: Path, rename_map: dict[str, str]) -> pd.DataFrame:
    layout = parse_infix_layout(do_path)
    missing = [name for name in rename_map if name not in layout]
    if missing:
        raise KeyError(f"{txt_path.name}: missing layout entries for {missing}")

    ordered = list(rename_map)
    colspecs = [layout[name] for name in ordered]
    frame = pd.read_fwf(
        txt_path,
        colspecs=colspecs,
        names=ordered,
        dtype=str,
        header=None,
    )
    for column in ordered:
        frame[column] = frame[column].astype(str).str.strip()
        frame[column] = frame[column].replace({"": pd.NA, ".": pd.NA})
    return frame.rename(columns=rename_map)


def to_numeric(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    return numeric.where(numeric >= 0)


def build_cumulative_map() -> pd.DataFrame:
    cum_file = UNPACKED / "cdsind2021/CDSIND2021.txt"
    cum_do = UNPACKED / "cdsind2021/CDSIND2021.do"
    keep = {
        "CDSCUMID68": "family_id68",
        "CDSCUMPN": "person_id68",
        "CRFID97": "core_fid_1997",
        "CRSN97": "core_sn_1997",
        "CRFID02": "core_fid_2002",
        "CRSN02": "core_sn_2002",
        "CRFID07": "core_fid_2007",
        "CRSN07": "core_sn_2007",
        "ID68PCG97": "pcg_id68_1997",
        "PNPCG97": "pcg_pn68_1997",
        "ID68PCG02": "pcg_id68_2002",
        "PNPCG02": "pcg_pn68_2002",
        "ID68PCG07": "pcg_id68_2007",
        "PNPCG07": "pcg_pn68_2007",
    }
    frame = read_fixed_width(cum_file, cum_do, keep)
    for column in frame.columns:
        frame[column] = to_numeric(frame[column])
    return frame.drop_duplicates(subset=["family_id68", "person_id68"])


def build_sex_map() -> pd.DataFrame:
    ind_file = UNPACKED / "ind2023er/IND2023ER.txt"
    ind_do = UNPACKED / "ind2023er/IND2023ER.do"
    keep = {
        "ER30001": "family_id68",
        "ER30002": "person_id68",
        "ER32000": "sex",
        "ER34504": "age_2017",
    }
    frame = read_fixed_width(ind_file, ind_do, keep)
    for column in frame.columns:
        frame[column] = to_numeric(frame[column])
    return frame.drop_duplicates(subset=["family_id68", "person_id68"])


def build_wave_frame(year: int, cumulative: pd.DataFrame) -> pd.DataFrame:
    cfg = WAVE_CONFIG[year]

    score = read_fixed_width(cfg["score_file"], cfg["score_do"], cfg["score_keep"])
    demog = read_fixed_width(cfg["demog_file"], cfg["demog_do"], cfg["demog_keep"])
    idmap = read_fixed_width(cfg["idmap_file"], cfg["idmap_do"], cfg["idmap_keep"])

    for frame in (score, demog, idmap):
        for column in frame.columns:
            frame[column] = to_numeric(frame[column])

    merged = score.merge(demog, on=["core_fid", "core_sn"], how="left", validate="one_to_one")
    merged = merged.merge(idmap, on=["core_fid", "core_sn"], how="left", validate="one_to_one")

    cum_subset = cumulative.rename(
        columns={
            f"core_fid_{year}": "core_fid",
            f"core_sn_{year}": "core_sn",
            f"pcg_id68_{year}": "cum_pcg_id68",
            f"pcg_pn68_{year}": "cum_pcg_pn68",
        }
    )[
        [
            "family_id68",
            "person_id68",
            "core_fid",
            "core_sn",
            "cum_pcg_id68",
            "cum_pcg_pn68",
        ]
    ]
    cum_subset = cum_subset[
        cum_subset["core_fid"].notna()
        & cum_subset["core_sn"].notna()
        & (cum_subset["core_fid"] > 0)
        & (cum_subset["core_sn"] > 0)
    ].drop_duplicates(subset=["core_fid", "core_sn"])

    merged = merged.merge(cum_subset, on=["core_fid", "core_sn"], how="left", validate="many_to_one")
    merged["wave"] = year

    if "pcg_id68" not in merged.columns:
        merged["pcg_id68"] = merged["cum_pcg_id68"]
    else:
        merged["pcg_id68"] = merged["pcg_id68"].fillna(merged["cum_pcg_id68"])

    if "pcg_pn68" not in merged.columns:
        merged["pcg_pn68"] = merged["cum_pcg_pn68"]
    else:
        merged["pcg_pn68"] = merged["pcg_pn68"].fillna(merged["cum_pcg_pn68"])

    merged.drop(columns=["cum_pcg_id68", "cum_pcg_pn68"], inplace=True)
    return merged


def build_panel() -> tuple[pd.DataFrame, dict[str, object]]:
    cumulative = build_cumulative_map()
    sex_map = build_sex_map()

    frames: list[pd.DataFrame] = []
    diagnostics: dict[str, object] = {
        "waves": {},
        "cumulative_rows": int(len(cumulative)),
        "sex_rows": int(len(sex_map)),
    }

    for year in sorted(WAVE_CONFIG):
        frame = build_wave_frame(year, cumulative)
        before_sex = int(frame["family_id68"].notna().sum())
        frame = frame.merge(sex_map, on=["family_id68", "person_id68"], how="left", validate="many_to_one")

        frame["female"] = frame["sex"].map({2: 1, 1: 0})
        if "age_months" not in frame.columns:
            frame["age_months"] = frame["age_years_reported"] * 12.0
        frame["age_years"] = frame["age_months"] / 12.0
        frame["pair_id68"] = frame["family_id68"] * 1000.0 + frame["person_id68"]

        frames.append(frame)
        diagnostics["waves"][str(year)] = {
            "rows": int(len(frame)),
            "with_cumulative_join": before_sex,
            "with_sex": int(frame["sex"].notna().sum()),
            "with_weight": int(frame["child_weight"].notna().sum()),
        }

    panel = pd.concat(frames, ignore_index=True)
    panel["source"] = "PSID_CDS"
    diagnostics["panel_rows"] = int(len(panel))
    diagnostics["panel_unique_children"] = int(panel["pair_id68"].nunique())
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
