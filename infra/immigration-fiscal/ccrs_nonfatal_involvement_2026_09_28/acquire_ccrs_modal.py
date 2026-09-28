"""Fetch CHP CCRS crash tables from data.ca.gov through a US Modal container.

data.ca.gov answers requests from this machine's region with Cloudflare error 1009 (country or
region banned), so the CKAN API and the CSV downloads run on Modal and the files come back
through a Modal Volume.

    modal run acquire_ccrs_modal.py::probe            # CKAN metadata + HEAD sizes -> _cache/ckan_ccrs.json
    modal run acquire_ccrs_modal.py::fetch --names "Crashes_2023,Parties_2023"
    modal volume get ccrs-2026-09-28 / _cache/ccrs/  # relay to the lane cache

fetch() stores each file gzip-compressed beside a <file>.json record of its byte count and sha256.
"""
import json

import modal

app = modal.App("ccrs-acquire-2026-09-28")
image = modal.Image.debian_slim().pip_install("requests")
vol = modal.Volume.from_name("ccrs-2026-09-28", create_if_missing=True)
CKAN = "https://data.ca.gov/api/3/action"
UA = {"User-Agent": "immigration-research ccrs lane (curl-compatible)"}


@app.function(image=image, timeout=600)
def probe_remote(query: str = "ccrs") -> dict:
    import requests

    out = {"search": [], "packages": {}}
    r = requests.get(f"{CKAN}/package_search", params={"q": query, "rows": 50}, headers=UA, timeout=60)
    r.raise_for_status()
    for p in r.json()["result"]["results"]:
        out["search"].append({"name": p["name"], "title": p["title"], "n_res": len(p["resources"]),
                              "org": (p.get("organization") or {}).get("name")})
        res = []
        for x in p["resources"]:
            size = x.get("size")
            try:
                h = requests.head(x["url"], headers=UA, timeout=30, allow_redirects=True)
                size = h.headers.get("content-length", size)
            except Exception as e:  # report, do not hide
                size = f"HEAD failed: {e!r}"
            res.append({"name": x.get("name"), "format": x.get("format"), "url": x.get("url"),
                        "size": size, "id": x.get("id"), "datastore_active": x.get("datastore_active"),
                        "last_modified": x.get("last_modified")})
        out["packages"][p["name"]] = {"notes": (p.get("notes") or "")[:4000], "resources": res}
    return out


@app.function(image=image, timeout=3000, volumes={"/vol": vol}, max_containers=12)
def fetch_one(name: str, url: str) -> dict:
    """Streams one resource to /vol/<url basename>.gz with a sidecar <basename>.json record."""
    import gzip
    import hashlib
    import os

    import requests

    base = url.rsplit("/", 1)[-1]
    h = hashlib.sha256()
    n = 0
    tmp = f"/vol/{base}.gz.part"
    with requests.get(url, headers=UA, stream=True, timeout=120) as r:
        r.raise_for_status()
        with gzip.open(tmp, "wb", compresslevel=6) as f:
            for chunk in r.iter_content(1 << 20):
                h.update(chunk)
                n += len(chunk)
                f.write(chunk)
    os.replace(tmp, f"/vol/{base}.gz")
    rec = {"name": name, "url": url, "file": f"{base}.gz", "bytes": n, "sha256": h.hexdigest(),
           "gz_bytes": os.path.getsize(f"/vol/{base}.gz")}
    json.dump(rec, open(f"/vol/{base}.json", "w"), indent=1)
    vol.commit()
    print(f"done {name}: {n} bytes", flush=True)
    return rec


@app.local_entrypoint()
def probe(query: str = "ccrs", out: str = "_cache/ckan_ccrs.json"):
    meta = probe_remote.remote(query)
    with open(out, "w") as f:
        json.dump(meta, f, indent=1)
    print(json.dumps(meta, indent=1))


@app.local_entrypoint()
def fetch(names: str, meta: str = "_cache/ckan_ccrs.json"):
    """names: comma-separated resource names from the probe output saved at `meta`."""
    pk = json.load(open(meta))["packages"]
    by_name = {r["name"]: r["url"] for p in pk.values() for r in p["resources"]}
    want = [(n, by_name[n]) for n in names.split(",")]
    print(json.dumps(list(fetch_one.starmap(want)), indent=1))
