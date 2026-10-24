"""Shared helpers: ArcGIS REST paging, Case-Shiller factors, robust stats."""
import os
import sys
import time

import numpy as np
import pandas as pd
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.normpath(os.path.join(HERE, "..", "_cache"))


def arcgis_page(url, where, out_fields, page_size=2000, order="OBJECTID",
                extra=None, verbose=True, max_pages=None):
    """Page a feature/table service query endpoint; returns DataFrame of attributes."""
    offset, rows, pages = 0, [], 0
    while True:
        params = {
            "where": where, "outFields": out_fields, "returnGeometry": "false",
            "resultOffset": offset, "resultRecordCount": page_size,
            "orderByFields": order, "f": "json",
        }
        if extra:
            params.update(extra)
        j = None
        for attempt in range(5):
            try:
                r = requests.post(url, data=params, timeout=180)
                j = r.json()
                if "error" not in j:
                    break
                print("svc error", j["error"], file=sys.stderr)
            except Exception as e:  # noqa: BLE001
                print("retry", attempt, e, file=sys.stderr)
            time.sleep(2 * (attempt + 1))
        if j is None or "error" in j:
            raise RuntimeError("query failed at offset %d" % offset)
        feats = j.get("features", [])
        rows.extend(f["attributes"] for f in feats)
        pages += 1
        if verbose:
            print("  page %d offset %d rows %d" % (pages, offset, len(rows)), file=sys.stderr)
        if len(feats) < page_size:
            break
        if max_pages and pages >= max_pages:
            break
        offset += page_size
    return pd.DataFrame(rows)


def case_shiller_factors(series_id, years):
    """Annual-average S&P CoreLogic Case-Shiller index -> ratio to `years['base']`."""
    path = os.path.join(CACHE, "cs_%s.csv" % series_id)
    if not os.path.exists(path):
        r = requests.get("https://fred.stlouisfed.org/graph/fredgraph.csv?id=%s" % series_id,
                         timeout=60)
        r.raise_for_status()
        with open(path, "w") as fh:
            fh.write(r.text)
    df = pd.read_csv(path)
    df.columns = ["date", "value"]
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df.date.dt.year
    df["value"] = pd.to_numeric(df.value, errors="coerce")
    ann = df.dropna().groupby("year").value.mean()
    return {y: ann.get(y) for y in years}


def iqr_stats(s, lo_q=0.25, hi_q=0.75):
    s = pd.Series(s).dropna()
    return {
        "n": int(len(s)),
        "median": float(np.median(s)),
        "p25": float(np.percentile(s, 25)),
        "p75": float(np.percentile(s, 75)),
        "mean": float(np.mean(s)),
    }
