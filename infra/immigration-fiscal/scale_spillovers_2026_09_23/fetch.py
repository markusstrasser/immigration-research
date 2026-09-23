"""Fetch the crosswalks and source files the scale-spillover arms need; record their hashes.

Downloads (all into the ignored _cache/):
  xwalk_puma22_cbsa23.csv   Geocorr 2022: 2022 PUMAs to July-2023 CBSAs, 2020 population weights.
                            The 2023 delineation is used because Connecticut's 2022 planning regions
                            are not in the 2020 CBSA layer (Geocorr returns "not in any CBSA" there).
  L3_czeffects.dta          Card, Rothstein & Yi (2023) public CZ place effects, 691 CZs.
  cw_cty_czone.zip          Autor-Dorn county -> 1990 commuting zone crosswalk.
  2023_Gaz_cbsa_national    Census 2023 gazetteer, CBSA land areas (caps the 5-25 mile ring).
  papers (PDF)              the primary sources quoted in RESULT.md (NBER, LSE, IZA, UC Davis).
and writes _cache/manifest.json with sha256 of every file in _cache/.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/scale_spillovers_2026_09_23/fetch.py
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "_cache"
BROKER = "https://mcdc.missouri.edu/cgi-bin/broker"
STATES = ['Al01', 'Ak02', 'Az04', 'Ar05', 'Ca06', 'Co08', 'Ct09', 'De10', 'Dc11', 'Fl12', 'Ga13',
          'Hi15', 'Id16', 'Il17', 'In18', 'Ia19', 'Ks20', 'Ky21', 'La22', 'Me23', 'Md24', 'Ma25',
          'Mi26', 'Mn27', 'Ms28', 'Mo29', 'Mt30', 'Ne31', 'Nv32', 'Nh33', 'Nj34', 'Nm35', 'Ny36',
          'Nc37', 'Nd38', 'Oh39', 'Ok40', 'Or41', 'Pa42', 'Ri44', 'Sc45', 'Sd46', 'Tn47', 'Tx48',
          'Ut49', 'Vt50', 'Va51', 'Wa53', 'Wv54', 'Wi55', 'Wy56']
BLANKS = ("title", "oropt", "counties", "metros", "uaucs", "places", "latitude", "longitude",
          "locname", "distance", "nrings", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9",
          "r10", "lathi", "latlo", "longhi", "longlo")
FILES = {
    "L3_czeffects.dta": "https://eml.berkeley.edu/~jrothst/data/L3_czeffects.dta",
    "cw_cty_czone.zip": "https://www.ddorn.net/data/cw_cty_czone.zip",
    "w27075.pdf": "https://www.nber.org/system/files/working_papers/w27075/w27075.pdf",
    "w31587.pdf": "https://www.nber.org/system/files/working_papers/w31587/w31587.pdf",
    "w9108.pdf": "https://www.nber.org/system/files/working_papers/w9108/w9108.pdf",
    "w9316.pdf": "https://www.nber.org/system/files/working_papers/w9316/w9316.pdf",
    "w9641.pdf": "https://www.nber.org/system/files/working_papers/w9641/w9641.pdf",
    "w7444.pdf": "https://www.nber.org/system/files/working_papers/w7444/w7444.pdf",
    "w12440.pdf": "https://www.nber.org/system/files/working_papers/w12440/w12440.pdf",
    "w15507.pdf": "https://www.nber.org/system/files/working_papers/w15507/w15507.pdf",
    "w15103.pdf": "https://www.nber.org/system/files/working_papers/w15103/w15103.pdf",
    "w4728.pdf": "https://www.nber.org/system/files/working_papers/w4728/w4728.pdf",
    "ap2019_jue_am.pdf": "https://researchonline.lse.ac.uk/id/eprint/100482/1/GA_EP_The_economic_effects_of_density.pdf",
    "combes_gobillon_iza8508.pdf": "https://docs.iza.org/dp8508.pdf",
    "ciccone_peri_2006.pdf": "https://giovanniperi.ucdavis.edu/uploads/5/6/8/2/56826033/ciccone_peri_identifying_human_capital_2006.pdf",
    "rs2008_jue.pdf": "https://hceconomics.uchicago.edu/sites/default/files/pdf/events/Rosenthal_Strange_2008_JUE_v64_attenuation-human.pdf",
    "2023_Gaz_cbsa_national.zip": "https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2023_Gazetteer/2023_Gaz_cbsa_national.zip",
}


def get(url, timeout=600):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read()


def geocorr_state(state, tries=3):
    q = {"_PROGRAM": "apps.geocorr2022.sas", "_SERVICE": "MCDC_long", "_debug": "0",
         "state": state, "g1_": "puma22", "g2_": "cbsa23", "wtvar": "pop20", "nozerob": "1",
         "csvout": "1", "fileout": "1", "filefmt": "csv", "lstfmt": "txt", "namoptf": "b",
         "namoptr": "b", "kiloms": "0"}
    q.update({k: "" for k in BLANKS})
    url = BROKER + "?" + urllib.parse.urlencode(q)
    for attempt in range(tries):
        try:
            html = get(url, 300).decode("utf-8", "replace")
            m = re.search(r'"\s*(/temp/geocorr\w*_[^"\s]+\.csv)\s*"', html)
            if not m:
                raise RuntimeError(f"no csv link for {state}")
            return get("https://mcdc.missouri.edu" + m.group(1), 300).decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001 - retried, then raised
            if attempt == tries - 1:
                raise
            sys.stderr.write(f"retry {state}: {exc}\n")
            time.sleep(5)


def fetch_geocorr():
    out = CACHE / "xwalk_puma22_cbsa23.csv"
    if out.exists():
        return
    rows, header = [], None
    for st in STATES:
        body = geocorr_state(st)
        reader = list(csv.reader(io.StringIO(body)))
        header = header or reader[0]
        rows.extend(r for r in reader[2:] if r)          # row 2 holds the variable labels
        print(st, len(reader) - 2, flush=True)
    with out.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


def main():
    CACHE.mkdir(exist_ok=True)
    for name, url in FILES.items():
        dest = CACHE / name
        if not dest.exists():
            dest.write_bytes(get(url))
            print("fetched", name, flush=True)
    fetch_geocorr()
    manifest = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(CACHE.iterdir()) if p.is_file() and p.suffix in
                {".csv", ".dta", ".zip", ".pdf", ".json"} and p.name != "manifest.json"}
    (CACHE / "manifest.json").write_text(json.dumps(manifest, indent=1))
    print(json.dumps({k: v[:12] for k, v in manifest.items()}, indent=1))


if __name__ == "__main__":
    main()
