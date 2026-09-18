"""Run the AHS 2023 national household test on Modal (the local link is saturated).

Downloads the AHS 2023 National PUF flat CSV in the cloud, discovers the relevant
variable names from the file header, and reports value distributions so the
regression pass can be written against the real codes.

Run:  modal run infra/immigration-fiscal/enclave_quality_2026_09_18/modal_ahs.py
"""
import modal

app = modal.App("ahs-enclave-quality")
image = (modal.Image.debian_slim(python_version="3.12")
         .pip_install("pandas>=2", "numpy>=2", "statsmodels", "requests"))

URL = ("https://www2.census.gov/programs-surveys/ahs/2023/"
       "AHS%202023%20National%20PUF%20v1.0%20Flat%20CSV.zip")


@app.function(image=image, timeout=3600, memory=16384, cpu=4)
def discover():
    import io, re, zipfile, requests, json
    import numpy as np, pandas as pd
    pd.set_option("display.width", 250, "display.max_columns", 80)

    print("downloading", URL, flush=True)
    r = requests.get(URL, timeout=1800)
    r.raise_for_status()
    print("bytes", len(r.content), flush=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    names = z.namelist()
    print("ZIP CONTENTS:", names, flush=True)
    csvs = [n for n in names if n.lower().endswith(".csv")]
    target = max(csvs, key=lambda n: z.getinfo(n).file_size)
    print("using", target, z.getinfo(target).file_size, flush=True)

    head = pd.read_csv(z.open(target), nrows=5, dtype=str, low_memory=False)
    cols = list(head.columns)
    print("n columns:", len(cols), flush=True)
    pat = re.compile(r"SPAN|RACE|HINC|FINC|TENURE|ADEQ|RATING|^NHQ|^NEAR|"
                     r"WEIGHT|WGT|CBSA|YRBUILT|BLD|CROWD|UNITSIZE|PERPOVLVL|"
                     r"NUMPEOPLE|TOTROOMS|HUDSUB|MOVFORCE|DIVISION|METRO", re.I)
    cand = [c for c in cols if pat.search(c)]
    print("CANDIDATE COLUMNS:", cand, flush=True)

    df = pd.read_csv(z.open(target), usecols=cand, dtype=str, low_memory=False)
    print("rows:", len(df), flush=True)

    def clean(s):
        return (s.astype(str).str.strip().str.strip("'").str.strip('"')
                 .replace({"": np.nan, "-6": np.nan, "-9": np.nan, "M": np.nan,
                           "N": np.nan, "B": np.nan, ".": np.nan}))
    for c in df.columns:
        df[c] = clean(df[c])

    print("\n=== value counts ===", flush=True)
    for c in cand:
        vc = df[c].value_counts(dropna=False).head(12)
        print("--- %s (nuniq=%d) ---" % (c, df[c].nunique()), flush=True)
        print(vc.to_string(), flush=True)

    return json.dumps({"columns": cols, "candidates": cand})[:400000]


@app.local_entrypoint()
def main():
    s = discover.remote()
    open("/tmp/ahs_discovery.json", "w").write(s)
    print("wrote /tmp/ahs_discovery.json", len(s))
