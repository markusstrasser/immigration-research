"""Public college students by state, level and origin from ACS 2024 1-year PUMS (persons).

The tuition share needs, for each state, the share of Hispanic public college students who are of Mexican origin
(IPEDS reports Hispanic, not Mexican, students by institution). It also writes the group's population share in the
ACS, which carries an ACS-frame share to the account's frame.

Group: Mexican origin in the ACS = HISP 02 (Mexican, Mexican American, Chicano) or born in Mexico (POBP 303). The
account's union also counts natives with a Mexico-born parent who do not report Mexican origin; the ACS cannot see
parents' birthplaces, so they are missing here [ASSUMPTION: ratios, not levels, leave this lane].
Public college: SCH 2 (public school or college) and SCHG 15 (undergraduate) or 16 (graduate or professional).

Writes derived/acs_public_college_by_state.csv and derived/acs_population.json. Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/user_fee_allocation_2026_10_07/acs_college.py
"""
import hashlib
import json
import zipfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PUMS = REPO / "sources/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip"
PUMS_SHA = "afdc6d90c6e2f0bab365ed32d95ba4c4d8ac651162f46ac7861295b2dc469894"
COLS = ["STATE", "PWGTP", "SCH", "SCHG", "HISP", "POBP"]
OUT = HERE / "derived"


def sha(path):
    with open(path, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def main():
    if sha(PUMS) != PUMS_SHA:
        raise SystemExit(f"[BLOCKED] {PUMS} is not the pinned ACS 2024 person file")
    OUT.mkdir(exist_ok=True)
    cells, pop = [], {"persons": 0.0, "mexican_origin": 0.0, "hispanic": 0.0}
    with zipfile.ZipFile(PUMS) as z:
        members = sorted(n for n in z.namelist() if n.startswith("psam_pus") and n.endswith(".csv"))
        if members != ["psam_pusa.csv", "psam_pusb.csv"]:
            raise SystemExit(f"[BLOCKED] unexpected PUMS members {members}")
        for name in members:
            for d in pd.read_csv(z.open(name), usecols=COLS, chunksize=500_000):
                if d[["STATE", "PWGTP", "HISP", "POBP"]].isna().any().any():
                    raise SystemExit("[BLOCKED] missing state, weight, origin or birthplace")
                mex = d.HISP.eq(2) | d.POBP.eq(303)
                hisp = d.HISP.ne(1)
                pop["persons"] += float(d.PWGTP.sum())
                pop["mexican_origin"] += float(d.PWGTP[mex].sum())
                pop["hispanic"] += float(d.PWGTP[hisp].sum())
                c = d[d.SCH.eq(2) & d.SCHG.isin([15, 16])].copy()
                c["level"] = c.SCHG.map({15: "undergraduate", 16: "graduate"})
                c["mexican"] = (c.HISP.eq(2) | c.POBP.eq(303)).astype(float) * c.PWGTP
                c["hispanic"] = c.HISP.ne(1).astype(float) * c.PWGTP
                c["hispanic_mexican"] = (c.HISP.eq(2)).astype(float) * c.PWGTP
                cells.append(c.groupby(["STATE", "level"]).agg(students=("PWGTP", "sum"), records=("PWGTP", "size"),
                    hispanic=("hispanic", "sum"), mexican=("mexican", "sum"),
                    hispanic_mexican=("hispanic_mexican", "sum")))
    t = pd.concat(cells).groupby(level=[0, 1]).sum().reset_index()
    # The Mexican share of Hispanic students: Hispanic Mexicans over Hispanics (both self-reported), the ratio applied
    # to IPEDS Hispanic counts; mexican (HISP 02 or born in Mexico) over students is the direct share, kept as a check.
    t["mexican_share_of_hispanic"] = t.hispanic_mexican / t.hispanic
    t["mexican_share_of_students"] = t.mexican / t.students
    t["hispanic_share_of_students"] = t.hispanic / t.students
    t = t.sort_values(["STATE", "level"])
    t.to_csv(OUT / "acs_public_college_by_state.csv", index=False, lineterminator="\n", float_format="%.6f")
    pop["mexican_origin_share"] = pop["mexican_origin"] / pop["persons"]
    pop["source"] = {"file": str(PUMS.relative_to(REPO)), "sha256": PUMS_SHA,
                     "group": "HISP 02 or POBP 303", "public_college": "SCH 2 and SCHG 15 or 16"}
    nat = t.groupby("level")[["students", "hispanic", "mexican", "hispanic_mexican"]].sum()
    pop["public_college_national"] = {lv: {k: float(v) for k, v in row.items()} for lv, row in nat.iterrows()}
    (OUT / "acs_population.json").write_text(json.dumps(pop, indent=1, sort_keys=True) + "\n")
    print(nat.assign(mex_share=nat.mexican / nat.students, hisp_share=nat.hispanic / nat.students).to_string())
    print({k: v for k, v in pop.items() if not isinstance(v, dict)})


if __name__ == "__main__":
    main()
