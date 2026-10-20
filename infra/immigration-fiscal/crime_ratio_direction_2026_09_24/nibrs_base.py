"""Shared loader for the NIBRS lane's staged cells, and the positive control this lane must pass
before any new method: the murder ratios of `offender_ethnicity_nibrs_2026_09_23` (Hispanic ÷
non-Hispanic white 2.30 central, 1.53 with every unknown offender non-Hispanic, 3.93 with every
unknown Hispanic).

    uv run --no-project python3 infra/immigration-fiscal/crime_ratio_direction_2026_09_24/nibrs_base.py

The NIBRS lane's code is imported read-only from its directory; nothing there is written.
"""
from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
NIBRS = FISCAL / "offender_ethnicity_nibrs_2026_09_23"
sys.path.insert(0, str(NIBRS))

import nibrs_rates as nr  # noqa: E402  (the NIBRS lane's module)

# The NIBRS lane's published murder ratios (RESULT.md, "Offending rates", Murder row)
PUBLISHED = {("central", "Murder"): 2.30, ("alloc=b", "Murder"): 1.53, ("alloc=c", "Murder"): 3.93,
             ("central", "Robbery"): 4.22, ("alloc=b", "Robbery"): 2.36, ("alloc=c", "Robbery"): 9.75}


@lru_cache(maxsize=1)
def load() -> tuple[dict, dict]:
    """Stages with agency compositions merged, exactly as nibrs_rates.main() builds them."""
    acs = pd.read_csv(nr.OUT / "acs5_place_county_groups.csv")
    stages = {}
    for st, yr in nr.STATE_YEARS:
        d = pd.read_pickle(nr.STAGE / f"{st}-{yr}.pkl")
        comp = nr.compositions(st, yr, d["agencies"], acs)
        d["agencies"] = d["agencies"].merge(comp, on="agency_id", how="left")
        stages[(st, yr)] = d
    return stages, nr.national_pops()


def lane_specs() -> dict[str, dict]:
    return dict(nr.specs())


def reproduce(names=("central", "alloc=b", "alloc=c", "alloc=a0", "alloc=k")) -> pd.DataFrame:
    stages, natpop = load()
    sp = lane_specs()
    return pd.concat([nr.results(stages, sp[n], natpop, n)[0] for n in names], ignore_index=True)


def published_rows() -> pd.DataFrame:
    return pd.read_csv(nr.OUT / "rates_by_spec.csv")


def main() -> None:
    r = reproduce()
    pub = published_rows()
    m = r.merge(pub, on=["spec", "offence"], suffixes=("", "_pub"))
    worst = float((m.RR_H_NHW - m.RR_H_NHW_pub).abs().max())
    print(f"[gate] reproduction of the NIBRS lane's rates_by_spec.csv, 5 specs x 5 offences: max |dRR| = {worst:.2e}")
    for (spec, off), v in PUBLISHED.items():
        got = float(r[(r.spec == spec) & (r.offence == off)].RR_H_NHW.iloc[0])
        print(f"[gate] {spec:8s} {off:8s} Hispanic/NH-white {got:.4f} (published {v:.2f}) "
              f"{'PASS' if round(got, 2) == v else 'FAIL'}")
    print(r[["spec", "offence", "RR_H_NHW", "RR_H_all", "national_share_H"]].to_string(index=False))


if __name__ == "__main__":
    main()
