"""Pull ACS 1-year PUMS interstate-migration records, one request per state-year.

Notes learned while building this (2026-09-18):
  * a national (`for=state:*`) request is reset by the server;
  * large states (CA, TX, NY, FL) are reset too, so a failing state is retried in
    MIGSP chunks and the chunks are concatenated;
  * the MIGSP predicate must be the explicit OR list MIGSP=001..056. The range form
    `MIGSP=1:56` is silently wrong: it returns foreign-country codes and drops
    own-state movers (checked against the 2023 California pull).

Validation: 2023 California weighted domestic in-migrants = 423,980, which matches the
published ACS 2023 state-to-state flow for California.

Output: _cache/pums_mig_<year>.csv, one row per PUMS mover record with the residence
state appended. MIGSP == ST rows are intrastate movers, kept here and dropped later.
"""
import os, sys, time, csv, json, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_cache")
os.makedirs(CACHE, exist_ok=True)
KEY = os.environ["CENSUS_API_KEY"]
VARS = ["PWGTP", "MIGSP", "NATIVITY", "PINCP", "ADJINC", "AGEP", "SCHL"]
CODES = ["%03d" % i for i in range(1, 57)]
YEARS = [y for y in range(2010, 2025) if y != 2020]
if os.environ.get("PUMS_YEARS"):
    YEARS = [int(x) for x in os.environ["PUMS_YEARS"].split(",")]
STATES = ["%02d" % i for i in range(1, 57) if i not in (3, 7, 14, 43, 52)]


def _req(year, st, codes, timeout):
    url = ("https://api.census.gov/data/%d/acs/acs1/pums?get=%s&%s&for=state:%s&key=%s"
           % (year, ",".join(VARS), "&".join("MIGSP=" + c for c in codes), st, KEY))
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.loads(r.read().decode())


def fetch(year, st):
    """Whole state first; on repeated failure, four MIGSP chunks."""
    for a in range(3):
        try:
            d = _req(year, st, CODES, 240)
            return [] if d is None else d[1:], d[0]
        except urllib.error.HTTPError as e:
            if e.code in (204, 404):
                return [], None
            sys.stderr.write("y%d s%s whole try%d http %s\n" % (year, st, a, e.code))
        except Exception as e:
            sys.stderr.write("y%d s%s whole try%d %s\n" % (year, st, a, e))
        time.sleep(8 * (a + 1))
    rows, hdr = [], None
    for i in range(0, len(CODES), 14):
        chunk = CODES[i:i + 14]
        for a in range(5):
            try:
                d = _req(year, st, chunk, 240)
                if d:
                    hdr = d[0]
                    rows.extend(d[1:])
                break
            except urllib.error.HTTPError as e:
                if e.code in (204, 404):
                    break
                sys.stderr.write("y%d s%s chunk%d try%d http %s\n" % (year, st, i, a, e.code))
            except Exception as e:
                sys.stderr.write("y%d s%s chunk%d try%d %s\n" % (year, st, i, a, e))
            time.sleep(8 * (a + 1))
        else:
            raise RuntimeError("year %d state %s chunk %d failed" % (year, st, i))
    return rows, hdr


def main():
    for y in YEARS:
        out = os.path.join(CACHE, "pums_mig_%d.csv" % y)
        if os.path.exists(out) and os.path.getsize(out) > 100000:
            print("skip", y, flush=True)
            continue
        t0, n = time.time(), 0
        with open(out + ".tmp", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(VARS + ["ST"])
            for st in STATES:
                rows, hdr = fetch(y, st)
                if not rows:
                    print("  y%d s%s empty" % (y, st), flush=True)
                    continue
                idx = [hdr.index(v) for v in VARS]
                for r in rows:
                    w.writerow([r[i] for i in idx] + [st])
                    n += 1
        os.replace(out + ".tmp", out)
        print("year %d rows=%d %.0fs" % (y, n, time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
