"""Fetch the IRS SOI tables this lane scores against, and record whether SOI has published tax year 2024.

Downloads Table 1.2 (all returns by size of AGI) for tax years 2022 and 2023 into _cache/, and probes the
file names SOI uses for tax year 2024 and for preliminary data, and reads the Summer 2026 SOI Bulletin, where SOI
printed preliminary individual data in past years. Writes _cache/acquisition.json. Run once;
heldout.py reads only the cached files, so its reruns do not depend on the network.

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/tax_key_heldout_2026_09_28/acquire.py
"""
from __future__ import annotations

import datetime as dt
import hashlib
import html as htmllib
import json
import re
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
UA = {"User-Agent": "research-script/1.0"}
SOI = "https://www.irs.gov/pub/irs-soi/"
TABLES = ["22in12ms.xls", "23in12ms.xls"]
# Tax year 2024 under SOI's names for Table 1.2, 1.1 and 1.4, and the preliminary Table 1 name SOI used
# through tax year 2022 (22in01pl.xls exists), for tax years 2023 and 2024.
PROBES = ["24in12ms.xls", "24in12ms.xlsx", "24in11si.xls", "24in14ar.xls", "22in01pl.xls", "23in01pl.xls",
          "24in01pl.xls", "24in01pl.xlsx"]
PAGE = "https://www.irs.gov/statistics/soi-tax-stats-individual-statistical-tables-by-size-of-adjusted-gross-income"
# The summer issue is where SOI printed individual preliminary data in past years.
BULLETIN = "https://www.irs.gov/statistics/soi-tax-stats-soi-bulletin-summer-2026"


def get(url: str, method: str = "GET") -> tuple[int, bytes, dict]:
    req = urllib.request.Request(url, headers=UA, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, (r.read() if method == "GET" else b""), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, b"", dict(e.headers or {})


def main() -> None:
    CACHE.mkdir(exist_ok=True)
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out = {"fetched_utc": now, "user_agent": UA["User-Agent"], "tables": {}, "probes": {}, "page": {}}
    for name in TABLES:
        status, body, head = get(SOI + name)
        if status != 200 or not body:
            raise SystemExit(f"[BLOCKED] {SOI + name} returned {status}")
        (CACHE / name).write_bytes(body)
        out["tables"][name] = {"url": SOI + name, "status": status, "bytes": len(body),
                               "sha256": hashlib.sha256(body).hexdigest(), "last_modified": head.get("Last-Modified")}
    for name in PROBES:
        status, _, head = get(SOI + name, "HEAD")
        out["probes"][name] = {"url": SOI + name, "status": status, "last_modified": head.get("Last-Modified")}
    status, body, _ = get(PAGE)
    html = body.decode("utf-8", "replace")
    years = sorted({int(m) for m in re.findall(r"/pub/irs-soi/(\d\d)in\d\d[a-z]*\.xlsx?", html)})
    (CACHE / "soi_tables_by_agi_page.html").write_text(html)
    out["page"] = {"url": PAGE, "status": status, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(),
                   "two_digit_tax_years_linked": years}
    status, body, _ = get(BULLETIN)
    page = body.decode("utf-8", "replace")
    (CACHE / "soi_bulletin_summer_2026.html").write_text(page)
    text = " ".join(htmllib.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", "", page, flags=re.S))).split())
    notice = re.search(r"Typically, all issues of this quarterly publication.*?may be found at:", text)
    if status != 200 or not notice:
        raise SystemExit(f"[BLOCKED] {BULLETIN} returned {status} or no notice")
    out["bulletin"] = {"url": BULLETIN, "status": status, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(),
                       "notice": notice.group(0)}
    (CACHE / "acquisition.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
