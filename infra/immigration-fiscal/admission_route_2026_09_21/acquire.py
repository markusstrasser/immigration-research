"""Download the DHS Yearbook lawful-permanent-resident workbooks, FY2004-FY2023.

Each yearbook page (ohss.dhs.gov/topics/immigration/yearbook/<year>) links one main LPR file
(a zip of per-table workbooks in older years, a single xlsx later) beside a supplement and a
new-arrival/adjustment split. Only the main file is taken. Everything lands in `_cache/`
(ignored); `_cache/acquire_manifest.json` records the URL, size and SHA-256 of each file.
"""
import hashlib
import json
import re
import subprocess
import sys
import urllib.parse
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
BASE = "https://ohss.dhs.gov"
YEARS = range(2004, 2024)
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/126 Safari/537.36")
LINK = re.compile(r'href="([^"]+\.(?:xlsx|xls|zip))"', re.I)
MAIN = re.compile(r"lpr|lawful|permanent", re.I)
NOT_MAIN = re.compile(r"supp|tables?8|newadj|naturaliz|nonimmigrant|refugee|asylee|enforcement", re.I)


def get(url):
    # ohss.dhs.gov answers 403 to urllib with the same headers; curl is accepted.
    result = subprocess.run(["curl", "-sS", "-L", "--fail", "--max-time", "120", "-A", UA, url],
                            capture_output=True, check=False)
    if result.returncode != 0:
        raise SystemExit(f"  ✗ curl rc={result.returncode} for {url}: {result.stderr.decode()[:200]}")
    return result.stdout


# The FY2012 page links only the supplement; the main file sits at the FY2013 naming pattern
# (found by probing on 2026-09-21).
OVERRIDES = {2012: "/sites/default/files/2023-12/LPR%25202012.zip"}


def main_link(page, year):
    if year in OVERRIDES:
        return OVERRIDES[year]
    links = sorted({m for m in LINK.findall(page) if MAIN.search(m) and not NOT_MAIN.search(m)})
    if len(links) != 1:
        raise SystemExit(f"  ✗ FY{year}: expected one main LPR link, found {links}")
    return links[0]


def main():
    CACHE.mkdir(exist_ok=True)
    manifest = {}
    for year in YEARS:
        page_path = CACHE / f"yearbook_{year}.html"
        if not page_path.exists():
            page_path.write_bytes(get(f"{BASE}/topics/immigration/yearbook/{year}"))
        href = main_link(page_path.read_text(errors="replace"), year)
        url = urllib.parse.urljoin(BASE, href)
        suffix = Path(urllib.parse.unquote(urllib.parse.unquote(href))).suffix.lower()
        target = CACHE / f"lpr_fy{year}{suffix}"
        if not target.exists():
            target.write_bytes(get(url))
        data = target.read_bytes()
        members = []
        if suffix == ".zip":
            out = CACHE / f"lpr_fy{year}"
            with zipfile.ZipFile(target) as archive:
                archive.extractall(out)
                members = sorted(archive.namelist())
        manifest[str(year)] = {"url": url, "file": target.name, "bytes": len(data),
                               "sha256": hashlib.sha256(data).hexdigest(), "members": members}
        print(f"  ✓ FY{year}: {target.name} {len(data):,} bytes"
              + (f", {len(members)} members" if members else ""))
    (CACHE / "acquire_manifest.json").write_text(json.dumps(manifest, indent=1))


if __name__ == "__main__":
    sys.exit(main())
