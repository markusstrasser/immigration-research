#!/usr/bin/env python3
"""Download Census individual-unit local government finance files into _cache/.

Sources (probed 2026-09-18):
  2012, 2017 : .../gov-finances/datasets/<y>/public-use-datasets/<y>_Individual_Unit_File.zip
  2018-2023  : .../gov-finances/tables/<y>/<y>_Individual_Unit_File(s).zip
No individual-unit file exists on census.gov for 2007 or for 2013-2016.
"""
import os
import shutil
import sys
import time
import urllib.request

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_cache")

URLS = {
    2012: "https://www2.census.gov/programs-surveys/gov-finances/datasets/2012/public-use-datasets/2012_Individual_Unit_File.zip",
    2017: "https://www2.census.gov/programs-surveys/gov-finances/datasets/2017/public-use-datasets/2017_Individual_Unit_File.zip",
    2018: "https://www2.census.gov/programs-surveys/gov-finances/tables/2018/2018_Individual_Unit_File.zip",
    2019: "https://www2.census.gov/programs-surveys/gov-finances/tables/2019/2019_Individual_Unit_File.zip",
    2020: "https://www2.census.gov/programs-surveys/gov-finances/tables/2020/2020_Individual_Unit_File.zip",
    2021: "https://www2.census.gov/programs-surveys/gov-finances/tables/2021/2021_Individual_Unit_File.zip",
    2022: "https://www2.census.gov/programs-surveys/gov-finances/tables/2022/2022_Individual_Unit_File.zip",
    2023: "https://www2.census.gov/programs-surveys/gov-finances/tables/2023/2023_Individual_Unit_Files.zip",
}

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}


def main():
    os.makedirs(CACHE, exist_ok=True)
    for year, url in sorted(URLS.items()):
        dest = os.path.join(CACHE, f"indunit_{year}.zip")
        if os.path.exists(dest) and os.path.getsize(dest) > 100_000:
            print(f"[skip] {year} {os.path.getsize(dest):,} bytes", flush=True)
            continue
        for attempt in range(1, 6):
            print(f"[get ] {year} attempt {attempt} {url}", flush=True)
            try:
                req = urllib.request.Request(url, headers=UA)
                with urllib.request.urlopen(req, timeout=120) as r:
                    with open(dest + ".part", "wb") as f:
                        shutil.copyfileobj(r, f, 1 << 20)
                shutil.move(dest + ".part", dest)
                break
            except Exception as exc:  # noqa: BLE001
                print(f"[warn] {year} attempt {attempt}: {exc}", flush=True)
                if os.path.exists(dest + ".part"):
                    os.remove(dest + ".part")
                if attempt == 5:
                    raise
                time.sleep(5 * attempt)
        print(f"[ok  ] {year} {os.path.getsize(dest):,} bytes", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
