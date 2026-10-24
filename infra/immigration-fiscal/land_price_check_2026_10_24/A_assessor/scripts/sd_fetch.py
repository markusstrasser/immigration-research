"""San Diego County (06073): SFR parcels transferred 2022-2024, assessor land value.

Source: SANDAG/SanGIS "Parcels" hosted feature service
  https://geo.sandag.org/server/rest/services/Hosted/Parcels/FeatureServer/0
Fields: apn, asr_land (assessor land value), asr_impr, acreage (assessor acres),
        docdate (MMDDYY of last recorded document), SHAPE__Area (sq ft, CA SP Zone 6 feet),
        asr_landuse (11 = single family residential), unitqty, total_lvg_area.
"""
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import CACHE, arcgis_page  # noqa: E402

URL = "https://geo.sandag.org/server/rest/services/Hosted/Parcels/FeatureServer/0/query"
FIELDS = "apn,asr_land,asr_impr,acreage,docdate,SHAPE__Area,situs_zip,total_lvg_area,year_effective,unitqty"

if __name__ == "__main__":
    out = os.path.join(CACHE, "sd_sfr_transfers.csv")
    frames = []
    for yy in ("22", "23", "24"):
        where = "asr_landuse=11 AND docdate LIKE '%%%s'" % yy
        print("year 20%s" % yy, file=sys.stderr)
        frames.append(arcgis_page(URL, where, FIELDS, page_size=2000, order="objectid"))
    df = pd.concat(frames, ignore_index=True)
    df.to_csv(out, index=False)
    print("rows", len(df))
    print(df.head())
