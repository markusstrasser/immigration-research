"""LA County: fetch 2024 roll (SFR, base year 2022-2024) + parcel areas, compute $/acre.

Sources
-------
Roll:  LA County "Parcel Data 2021-2025" table service
       https://services.arcgis.com/RmCCgQtiZLDCtblq/arcgis/rest/services/Parcel_Data_2021_Table/FeatureServer/0
       fields RollYear, AIN, UseType, Roll_LandValue, Roll_LandBaseYear, RecordingDate, UseCode
Area:  LA County "LA County Residential Parcels" (DPH GIS, snapshot 2024-01-09)
       https://services.arcgis.com/RmCCgQtiZLDCtblq/arcgis/rest/services/ResidentialParcels_LACounty_010924download_allCB20_HD22_attributes/FeatureServer/1
       field Shape__Area, units esriFeet (spatial ref 2229 = CA State Plane Zone 5, US feet)
"""
import json, os, sys, time
import requests
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", "_cache")
ROLL = "https://services.arcgis.com/RmCCgQtiZLDCtblq/arcgis/rest/services/Parcel_Data_2021_Table/FeatureServer/0/query"
AREA = ("https://services.arcgis.com/RmCCgQtiZLDCtblq/arcgis/rest/services/"
        "ResidentialParcels_LACounty_010924download_allCB20_HD22_attributes/FeatureServer/1/query")

WHERE = ("RollYear='2024' AND UseType='SFR' AND "
         "(Roll_LandBaseYear='2022' OR Roll_LandBaseYear='2023' OR Roll_LandBaseYear='2024')")
FIELDS = "AIN,UseCode,Roll_LandValue,Roll_LandBaseYear,Roll_ImpValue,RecordingDate,SQFTmain,YearBuilt,SitusZIP"


def page(url, where, out_fields, page_size=2000, extra=None):
    offset = 0
    rows = []
    while True:
        params = {
            "where": where, "outFields": out_fields, "returnGeometry": "false",
            "resultOffset": offset, "resultRecordCount": page_size,
            "orderByFields": "OBJECTID", "f": "json",
        }
        if extra:
            params.update(extra)
        for attempt in range(5):
            try:
                r = requests.post(url, data=params, timeout=120)
                j = r.json()
                break
            except Exception as e:
                print("retry", attempt, e, file=sys.stderr)
                time.sleep(2 * (attempt + 1))
        else:
            raise RuntimeError("failed page at offset %d" % offset)
        if "error" in j:
            raise RuntimeError(j["error"])
        feats = j.get("features", [])
        rows.extend(f["attributes"] for f in feats)
        print("  offset %d -> %d rows (total %d)" % (offset, len(feats), len(rows)), file=sys.stderr)
        if len(feats) < page_size:
            break
        offset += page_size
    return pd.DataFrame(rows)


def fetch_areas(ains, batch=700):
    out = []
    ains = list(ains)
    for i in range(0, len(ains), batch):
        chunk = ains[i:i + batch]
        w = "AIN IN (" + ",".join("'%s'" % a for a in chunk) + ")"
        params = {"where": w, "outFields": "AIN,UseCode,Shape__Area",
                  "returnGeometry": "false", "f": "json"}
        for attempt in range(5):
            try:
                j = requests.post(AREA, data=params, timeout=180).json()
                break
            except Exception as e:
                print("retry area", attempt, e, file=sys.stderr)
                time.sleep(2 * (attempt + 1))
        else:
            raise RuntimeError("area batch failed at %d" % i)
        if "error" in j:
            raise RuntimeError(j["error"])
        out.extend(f["attributes"] for f in j.get("features", []))
        if i % (batch * 20) == 0:
            print("  areas %d/%d" % (i, len(ains)), file=sys.stderr)
    return pd.DataFrame(out)


if __name__ == "__main__":
    roll_path = os.path.join(CACHE, "la_roll_2024_sfr.csv")
    if os.path.exists(roll_path):
        roll = pd.read_csv(roll_path, dtype={"AIN": str, "UseCode": str, "Roll_LandBaseYear": str})
    else:
        print("fetching roll ...", file=sys.stderr)
        roll = page(ROLL, WHERE, FIELDS)
        roll.to_csv(roll_path, index=False)
    print("roll rows", len(roll))

    area_path = os.path.join(CACHE, "la_area_sfr.csv")
    if os.path.exists(area_path):
        area = pd.read_csv(area_path, dtype={"AIN": str, "UseCode": str})
    else:
        print("fetching areas ...", file=sys.stderr)
        area = fetch_areas(roll.AIN.astype(str).unique())
        area.to_csv(area_path, index=False)
    print("area rows", len(area))

    df = roll.merge(area[["AIN", "Shape__Area"]], on="AIN", how="left")
    df["acres"] = df.Shape__Area / 43560.0
    print("matched area:", df.Shape__Area.notna().mean())
    df.to_csv(os.path.join(CACHE, "la_joined.csv"), index=False)
    print(df.head())
