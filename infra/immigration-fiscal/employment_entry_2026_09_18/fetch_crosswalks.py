"""Fetch PUMA->county allocation factors (MCDC Geocorr) for the three PUMA vintages
used by ACS 1-year PUMS 2005-2023, plus the fixed OMB 2013 county->CBSA delineation.

Vintages: puma2k (ACS 2005-2011), puma12 (ACS 2012-2021), puma22 (ACS 2022-2023).
Output: _cache/xwalk_<vintage>.csv with county allocation factors (afact = share of the
PUMA's population living in that county).
"""
import io, sys, time, csv, re, pathlib, urllib.request, urllib.parse

HERE = pathlib.Path(__file__).parent
CACHE = HERE / "_cache"
CACHE.mkdir(exist_ok=True)
BROKER = "https://mcdc.missouri.edu/cgi-bin/broker"

STATES = ['Al01','Ak02','Az04','Ar05','Ca06','Co08','Ct09','De10','Dc11','Fl12','Ga13','Hi15',
          'Id16','Il17','In18','Ia19','Ks20','Ky21','La22','Me23','Md24','Ma25','Mi26','Mn27',
          'Ms28','Mo29','Mt30','Ne31','Nv32','Nh33','Nj34','Nm35','Ny36','Nc37','Nd38','Oh39',
          'Ok40','Or41','Pa42','Ri44','Sc45','Sd46','Tn47','Tx48','Ut49','Vt50','Va51','Wa53',
          'Wv54','Wi55','Wy56']

SPECS = {
    # vintage -> (geocorr app, source geo, weight var)
    "puma2k": ("apps.geocorr2014.sas", "puma2k", "pop2k"),
    "puma12": ("apps.geocorr2014.sas", "puma12", "pop10"),
    "puma22": ("apps.geocorr2022.sas", "puma22", "pop20"),
}

BLANKS = ("title","oropt","counties","metros","uaucs","places","latitude","longitude",
          "locname","distance","nrings","r1","r2","r3","r4","r5","r6","r7","r8","r9","r10",
          "lathi","latlo","longhi","longlo")


def fetch_state(program, g1, wtvar, state, tries=3):
    q = {"_PROGRAM": program, "_SERVICE": "MCDC_long", "_debug": "0", "state": state,
         "g1_": g1, "g2_": "county", "wtvar": wtvar, "nozerob": "1", "csvout": "1",
         "fileout": "1", "filefmt": "csv",
         "lstfmt": "txt", "namoptf": "b", "namoptr": "b", "kiloms": "0"}
    q.update({k: "" for k in BLANKS})
    url = BROKER + "?" + urllib.parse.urlencode(q)
    for t in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=300) as r:
                html = r.read().decode("utf-8", "replace")
            m = re.search(r'"\s*(/temp/geocorr\w*_[^"\s]+\.csv)\s*"', html)
            if not m:
                raise RuntimeError("no csv link for %s %s" % (g1, state))
            with urllib.request.urlopen("https://mcdc.missouri.edu" + m.group(1), timeout=300) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            if t == tries - 1:
                raise
            sys.stderr.write("retry %s %s: %s\n" % (g1, state, e))
            time.sleep(5)


def main():
    for vintage, (program, g1, wtvar) in SPECS.items():
        out = CACHE / ("xwalk_%s.csv" % vintage)
        if out.exists():
            print("skip", out.name); continue
        rows = []
        for st in STATES:
            txt = fetch_state(program, g1, wtvar, st)
            rdr = csv.DictReader(io.StringIO(txt))
            hdr = rdr.fieldnames
            next(rdr)  # geocorr row 2 is a second header line of labels
            for r in rdr:
                rows.append(r)
            print(vintage, st, len(rows), flush=True)
            time.sleep(1)
        with out.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)
        print("wrote", out, len(rows))


if __name__ == "__main__":
    main()
