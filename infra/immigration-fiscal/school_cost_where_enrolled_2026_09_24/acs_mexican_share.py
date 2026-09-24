"""Mexican share of Hispanic public K-12 pupils by state, ACS 2024 one-year PUMS (local, read-only).

Public K-12 pupil: SCH=2 (public school) and SCHG 02-14 (kindergarten to grade 12). Hispanic:
HISP != 01; Mexican-origin: HISP = 02 (self-identified), and a broad variant adding the Mexico-born
(POBP = 303) who do not report Mexican origin. Also written: the all-ages Mexican share of Hispanics
(to carry district B03001 all-age shares over to pupils) and English ability (ENG) of pupils, the
survey's closest item to English-learner status. Standard errors use the 80 replicate weights
(successive difference, 4/80). Writes derived/acs_state_pupils.csv.

    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy \
      python3 infra/immigration-fiscal/school_cost_where_enrolled_2026_09_24/acs_mexican_share.py
"""
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PUMS = ROOT / "sources/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip"
REPS = [f"PWGTP{i}" for i in range(1, 81)]
COLS = ["STATE", "AGEP", "SCH", "SCHG", "HISP", "POBP", "ENG", "PWGTP"] + REPS
# Published 2024 ACS one-year US resident population (PUMS weights sum to it).
EXPECTED_TOTAL = (334_000_000, 342_000_000)


def load():
    parts, total_weight = [], 0.0
    with zipfile.ZipFile(PUMS) as z:
        for member in ["psam_pusa.csv", "psam_pusb.csv"]:
            for chunk in pd.read_csv(z.open(member), usecols=COLS, chunksize=500_000, dtype={"STATE": int}):
                total_weight += chunk.PWGTP.sum()
                chunk["pupil"] = chunk.SCH.eq(2) & chunk.SCHG.between(2, 14)
                chunk["hisp"] = chunk.HISP.ne(1)
                chunk["mex"] = chunk.HISP.eq(2)
                chunk["mex_broad"] = chunk.HISP.eq(2) | chunk.POBP.eq(303)
                chunk["eng_lt_very_well"] = chunk.ENG.isin([2, 3, 4])
                parts.append(chunk[chunk.hisp | chunk.pupil | chunk.mex_broad])
    if not EXPECTED_TOTAL[0] < total_weight < EXPECTED_TOTAL[1]:
        raise SystemExit(f"[BLOCKED] PUMS weights sum to {total_weight:,.0f}; expected the 2024 resident population")
    return pd.concat(parts, ignore_index=True), total_weight


def sdr_se(full, reps):
    return np.sqrt(4 / 80 * np.square(reps - full[..., None]).sum(axis=-1))


def main():
    d, total = load()
    print(f"[pums] {len(d):,} relevant person rows; weights sum {total:,.0f}")
    W = d[["PWGTP"] + REPS].to_numpy(float)
    measures = {
        "pupils": d.pupil, "hisp_pupils": d.pupil & d.hisp, "mex_pupils": d.pupil & d.mex,
        "mex_broad_pupils": d.pupil & d.mex_broad,
        "mex_pupils_eng_lt_very_well": d.pupil & d.mex & d.eng_lt_very_well,
        "hisp_pupils_eng_lt_very_well": d.pupil & d.hisp & d.eng_lt_very_well,
        "pupils_eng_lt_very_well": d.pupil & d.eng_lt_very_well,
        "hisp_all_ages": d.hisp, "mex_all_ages": d.mex,
    }
    rows = []
    for st, idx in list(d.groupby("STATE").indices.items()) + [(0, np.arange(len(d)))]:
        sums = {k: W[idx][m.to_numpy()[idx]].sum(axis=0) for k, m in measures.items()}
        row = {"state_fips": st}
        for k, v in sums.items():
            row[k] = v[0]
        for num, den, name in [("mex_pupils", "hisp_pupils", "mex_share_of_hisp_pupils"),
                               ("mex_broad_pupils", "hisp_pupils", "mex_broad_share_of_hisp_pupils"),
                               ("mex_all_ages", "hisp_all_ages", "mex_share_of_hisp_all_ages"),
                               ("mex_pupils_eng_lt_very_well", "mex_pupils", "mex_pupil_eng_lt_very_well_rate"),
                               ("hisp_pupils_eng_lt_very_well", "hisp_pupils", "hisp_pupil_eng_lt_very_well_rate"),
                               ("pupils_eng_lt_very_well", "pupils", "pupil_eng_lt_very_well_rate")]:
            full = sums[num] / np.where(sums[den] > 0, sums[den], np.nan)
            row[name] = full[0]
            row[name + "_se"] = float(sdr_se(full[:1], full[1:][None, :])[0]) if sums[den][0] > 0 else np.nan
        row["child_to_all_age_ratio"] = row["mex_share_of_hisp_pupils"] / row["mex_share_of_hisp_all_ages"]
        rows.append(row)
    out = pd.DataFrame(rows).sort_values("state_fips")
    nat = out[out.state_fips == 0].iloc[0]
    # Content gates: national public K-12 near 47m (school_enrollment README: ACS 46.981m all-age);
    # Mexican share of Hispanics near 0.58-0.62 in recent ACS releases.
    if not 45e6 < nat.pupils < 49e6:
        raise SystemExit(f"[BLOCKED] national public K-12 pupils {nat.pupils:,.0f} outside 45-49m")
    if not 0.5 < nat.mex_share_of_hisp_all_ages < 0.65:
        raise SystemExit(f"[BLOCKED] national Mexican share of Hispanics {nat.mex_share_of_hisp_all_ages:.3f}")
    if len(out) != 52:
        raise SystemExit(f"[BLOCKED] expected 51 jurisdictions + US, got {len(out) - 1}")
    (HERE / "derived").mkdir(exist_ok=True)
    out.to_csv(HERE / "derived/acs_state_pupils.csv", index=False, lineterminator="\n", float_format="%.6f")
    print(f"[us] public K-12 {nat.pupils/1e6:.3f}m, Hispanic {nat.hisp_pupils/1e6:.3f}m, Mexican {nat.mex_pupils/1e6:.3f}m "
          f"(broad {nat.mex_broad_pupils/1e6:.3f}m); Mexican share of Hispanic pupils {nat.mex_share_of_hisp_pupils:.4f} "
          f"(SE {nat.mex_share_of_hisp_pupils_se:.4f}); all ages {nat.mex_share_of_hisp_all_ages:.4f}")
    print(out[["state_fips", "hisp_pupils", "mex_pupils", "mex_share_of_hisp_pupils", "mex_share_of_hisp_pupils_se",
               "child_to_all_age_ratio"]].sort_values("mex_pupils", ascending=False).head(12).to_string(index=False))


if __name__ == "__main__":
    main()
