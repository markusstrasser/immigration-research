"""Extract the 2007 local-finance rows from the Government Finance Database inside Modal.

The archive holds one 2.9 GB CSV (Pierson, Hand and Thompson's recoding of the Census
individual unit files, 1967 onward). Streaming and filtering it in the container costs
seconds and brings back a few megabytes instead of gigabytes.

  modal run modal_gfd_2007.py::peek      # header and first rows
  modal run modal_gfd_2007.py            # write /data/gfd_2007.csv, report shape
then
  modal volume get gfd gfd_2007.csv _cache/gfd_2007.csv
"""
import modal

app = modal.App("gfd-2007")
image = modal.Image.debian_slim().apt_install("p7zip-full")
vol = modal.Volume.from_name("gfd", create_if_missing=True)

ZIP = "/data/gfd_entire.zip"
MEMBER = "The Government Finance Database_All Data.csv"


def _stream():
    import subprocess

    return subprocess.Popen(["7z", "x", "-so", ZIP, MEMBER],
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)


@app.function(image=image, volumes={"/data": vol}, timeout=3600)
def peek():
    proc = _stream()
    out = []
    for i, line in enumerate(proc.stdout):
        if i >= 3:
            break
        out.append(line.decode("latin-1").rstrip()[:4000])
    proc.kill()
    return "\n".join(out)


@app.function(image=image, volumes={"/data": vol}, timeout=3600)
def extract(years=(2007, 2012, 2017)):
    """Keep only the requested survey years; write them to the volume."""
    import csv
    import io

    want = {str(y) for y in years}
    proc = _stream()
    reader = csv.reader(io.TextIOWrapper(proc.stdout, encoding="latin-1", newline=""))
    header = next(reader)
    lower = [h.strip().lower() for h in header]
    yi = next((i for i, h in enumerate(lower) if h in ("year4", "year", "yr")), None)
    if yi is None:
        proc.kill()
        return {"error": "no year column", "header": header[:40]}
    kept = 0
    seen = 0
    with open("/data/gfd_2007.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        for row in reader:
            seen += 1
            if len(row) > yi and row[yi].strip() in want:
                w.writerow(row)
                kept += 1
            if seen % 5_000_000 == 0:
                print(f"  {seen:,} rows scanned, {kept:,} kept", flush=True)
    proc.wait()
    vol.commit()
    import os
    return {"year_col": header[yi], "scanned": seen, "kept": kept,
            "bytes": os.path.getsize("/data/gfd_2007.csv"), "header": header}


# GFD column -> lane outcome. These are the database's own "direct expenditure"
# aggregates, so no item-code arithmetic is needed on this side.
GFD_COLS = {
    "total_direct": "Direct_General_Expend",
    "education": "Total_Educ_Direct_Exp",
    "educ_elemsec": "Elem_Educ_Direct_Exp",
    "police": "Police_Prot_Direct_Exp",
    "corrections": "Correct_Direct_Exp",
    "judicial": "Judicial_Direct_Expend",
    "welfare": "Public_Welf_Direct_Exp",
    "health": "Health_Direct_Expend",
    "hospital": "Total_Hospital_Dir_Exp",
    "highways": "Total_Highways_Dir_Exp",
}


@app.function(image=image, volumes={"/data": vol}, timeout=3600)
def aggregate(years=(2007, 2012, 2017, 2022)):
    """Sum local units to counties for the requested years; return a small CSV."""
    import csv
    import io
    from collections import defaultdict

    want = {str(y) for y in years}
    proc = _stream()
    reader = csv.reader(io.TextIOWrapper(proc.stdout, encoding="latin-1", newline=""))
    header = next(reader)
    ix = {h.strip(): i for i, h in enumerate(header)}
    missing = [c for c in GFD_COLS.values() if c not in ix]
    if missing:
        proc.kill()
        return {"error": "missing columns", "missing": missing}
    iy, it = ix["Year4"], ix["Type_Code"]
    ist, ico = ix["FIPS_Code_State"], ix["FIPS_County"]
    tot = defaultdict(lambda: defaultdict(float))
    units = defaultdict(int)
    scanned = 0
    for row in reader:
        scanned += 1
        if scanned % 5_000_000 == 0:
            print(f"  {scanned:,} rows scanned", flush=True)
        if len(row) <= ix["FIPS_County"]:
            continue
        if row[iy].strip() not in want:
            continue
        if row[it].strip() not in ("1", "2", "3", "4", "5"):   # local units only
            continue
        st, co = row[ist].strip(), row[ico].strip()
        if not st.isdigit() or not co.isdigit():
            continue
        key = (f"{int(st):02d}{int(co):03d}", row[iy].strip())
        units[key] += 1
        for label, col in GFD_COLS.items():
            v = row[ix[col]].strip()
            if v:
                try:
                    tot[key][label] += float(v)
                except ValueError:
                    pass
    proc.wait()
    out = "/data/gfd_county_waves.csv"
    cols = ["fips", "year", "n_units"] + list(GFD_COLS)
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for (fips, yr) in sorted(tot):
            rec = tot[(fips, yr)]
            w.writerow([fips, yr, units[(fips, yr)]]
                       + [f"{rec.get(c, 0.0):.1f}" for c in GFD_COLS])
    vol.commit()
    import os
    return {"scanned": scanned, "county_years": len(tot),
            "bytes": os.path.getsize(out)}


@app.local_entrypoint()
def main():
    print(aggregate.remote())
