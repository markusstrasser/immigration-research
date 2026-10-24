"""San Diego: full SFR population (for cohort/roll-year diagnostics)."""
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import CACHE, arcgis_page  # noqa: E402

URL = "https://geo.sandag.org/server/rest/services/Hosted/Parcels/FeatureServer/0/query"

if __name__ == "__main__":
    out = os.path.join(CACHE, "sd_sfr_all.csv")
    df = arcgis_page(URL, "asr_landuse=11",
                     "apn,asr_land,acreage,SHAPE__Area,docdate", page_size=2000,
                     order="objectid")
    df.to_csv(out, index=False)
    print("rows", len(df))
