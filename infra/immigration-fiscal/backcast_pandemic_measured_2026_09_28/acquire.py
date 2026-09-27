#!/usr/bin/env python3
"""Fetch and pin this lane's raw sources into _cache/, and extract the PDFs' text for quote checks.

Every file is checked against the sha256 recorded here; a missing file is downloaded with a generic
User-Agent. ASEC 2020 and 2021 (income years 2019 and 2020) were not local (dataset register; no
asecpub20/21 file under the repository or ~/research-data on 2026-09-28), so they are pulled here.
ASEC 2022-2025 are read in place from the lanes that pinned them (measure_shares.py).
"""
from __future__ import annotations

import hashlib
import urllib.request
from pathlib import Path

from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
AGENT = "Mozilla/5.0 (research data fetch)"
CENSUS = "https://www2.census.gov/programs-surveys/cps/datasets"
GOVINFO = "https://www.govinfo.gov/content/pkg"
SOURCES = {
    "asecpub20csv.zip": (f"{CENSUS}/2020/march/asecpub20csv.zip",
                         "f79430c5664745a2ae1c0f7fef615d93fa6b1933d0fe1dabb932ec52c73be591"),
    "asecpub21csv.zip": (f"{CENSUS}/2021/march/asecpub21csv.zip",
                         "7196ff49c52f833f65c537d66a0c8cc1540a8e31711a09c3730c218b4486c1f4"),
    "ddl2020.pdf": (f"{CENSUS}/2020/march/ASEC2020ddl_pub_full.pdf",
                    "c255850c37edefcc1c72b92c3a47949aa7292fe20adff85b5150daeb7bed12fc"),
    "ddl2021.pdf": (f"{CENSUS}/2021/march/asec2021_ddl_pub_full.pdf",
                    "5a3511e7945fe10e9c9177093665a659ab8b843d557075c7065d29c04b56b045"),
    "ddl2022.pdf": (f"{CENSUS}/2022/march/asec2022_ddl_pub_full.pdf",
                    "77622b19e77a24e8f5f6145fcb171ab856a2d438fda0ba1e04e7ce345b9f2428"),
    # Census working paper SEHSD-WP2021-18 (census.gov's own PDF path returned 404; IPUMS mirrors it).
    "wp2021_18.pdf": ("https://cps.ipums.org/cps/resources/spm/sehsd-wp2021-18.pdf",
                      "3f76213882d4b34f67664b9deaa440a07fd8e547f854ffc4583b1f397285bad2"),
    "bea_pandemic_2022q4_3rd.pdf": (
        "https://www.bea.gov/sites/default/files/2023-03/"
        "effects-of-selected-federal-pandemic-response-programs-on-personal-income-2022q4-3rd.pdf",
        "c0d92a9c6e6bfbcd8d22cc12af4f49675d95f4d9e0fa74e793a3b1b0058490fd"),
    "PLAW-116publ136.htm": (f"{GOVINFO}/PLAW-116publ136/html/PLAW-116publ136.htm",
                            "f8faea1a163304a7ad20c8540eb6d204e192a6e8a5901e3f38d84ab053a34d5d"),
    "PLAW-116publ260.htm": (f"{GOVINFO}/PLAW-116publ260/html/PLAW-116publ260.htm",
                            "c5d5b08013295d9a28c6857ef75ddf791cbf28906e9c72d53c222d5c83ea1156"),
    "PLAW-117publ2.htm": (f"{GOVINFO}/PLAW-117publ2/html/PLAW-117publ2.htm",
                          "fa3e20cfd6186b75f6dd84aa798734ac8448e9e2bd954eb0a5f6ed7b43c450cd"),
    "PLAW-115publ97.htm": (f"{GOVINFO}/PLAW-115publ97/html/PLAW-115publ97.htm",
                           "ff67e79aff30ec09b589027898ad702318e6074020fb644cc07e1fea6dbadfb1"),
}


def sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def fetch(name: str, url: str) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(request, timeout=600) as response:
        (CACHE / name).write_bytes(response.read())


def main() -> dict[str, str]:
    CACHE.mkdir(exist_ok=True)
    digests = {}
    for name, (url, pin) in SOURCES.items():
        path = CACHE / name
        if not path.exists():
            fetch(name, url)
        digest = sha(path)
        if digest != pin:
            raise SystemExit(f"[BLOCKED] {name} changed: {digest}")
        digests[name] = digest
        if path.suffix == ".pdf":
            text = "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
            path.with_suffix(".txt").write_text(text, encoding="utf-8")
    for name, digest in digests.items():
        print(f"{digest[:12]}  {name}")
    return digests


if __name__ == "__main__":
    main()
