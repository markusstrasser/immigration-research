"""San Bernardino County (06071): SFR parcels with base year 2022-2024.

Source: County of San Bernardino "Parcels with Redacted Owner Name" (SBCountyDPW / County_Of_San_Bernardino)
  https://services.arcgis.com/aA3snZwJfFkVyDuP/arcgis/rest/services/Parcels_for_San_Bernardino_County/FeatureServer/0
Fields: ParcelNumber, LandValue (text, comma formatted), ImprovementValue, Acreage (assessor acres),
        BaseYear (Prop 13 base year), AssessClass ('SINGLE FAMILY RESIDENTIAL').
Roll year of the values = 2026 (BaseYear=2026 parcels are present).
"""
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import CACHE, arcgis_page  # noqa: E402

URL = "https://services.arcgis.com/aA3snZwJfFkVyDuP/arcgis/rest/services/Parcels_for_San_Bernardino_County/FeatureServer/0/query"
FIELDS = "ParcelNumber,LandValue,ImprovementValue,Acreage,BaseYear,AssessDescription,TaxStatus"
WHERE = ("AssessClass='SINGLE FAMILY RESIDENTIAL' AND "
         "(BaseYear='2022' OR BaseYear='2023' OR BaseYear='2024')")

if __name__ == "__main__":
    df = arcgis_page(URL, WHERE, FIELDS, page_size=1000)
    df.to_csv(os.path.join(CACHE, "sb_sfr_base2022_24.csv"), index=False)
    print("rows", len(df))
    print(df.head())
