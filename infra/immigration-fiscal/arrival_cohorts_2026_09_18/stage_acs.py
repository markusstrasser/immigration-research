"""Stream-extract the needed columns from ACS 1-year PUMS person zips into parquet.

Usage: uv run --no-project --with pandas --with pyarrow python3 stage_acs.py <year> <zip> [member...]
Writes _cache/acs_<year>.parquet with ages 25-54 only (all birthplaces; group filtering happens
downstream).
"""
import sys, os, subprocess, io
import pandas as pd

WANT = ["STATE", "PWGTP", "AGEP", "CIT", "ENG", "SCHL", "SEX", "WAGP", "WKHP",
        "WKWN", "WKW", "YOEP", "ESR", "HISP", "NATIVITY", "POBP", "RAC1P", "ST", "DECADE"]
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_cache")
os.makedirs(CACHE, exist_ok=True)


def read_member(zpath, member, cols_present):
    p = subprocess.Popen(["unzip", "-p", zpath, member], stdout=subprocess.PIPE)
    chunks = []
    for ch in pd.read_csv(p.stdout, usecols=cols_present, low_memory=False, chunksize=500_000):
        ch = ch[(ch.AGEP >= 25) & (ch.AGEP <= 54)]
        chunks.append(ch)
    p.stdout.close()
    p.wait()
    return pd.concat(chunks, ignore_index=True)


def main():
    year = int(sys.argv[1])
    zpath = sys.argv[2]
    members = sys.argv[3:] or ["psam_pusa.csv", "psam_pusb.csv"]
    if len(members) == 1 and " " in members[0]:
        members = members[0].split()
    hp = subprocess.Popen(["unzip", "-p", zpath, members[0]], stdout=subprocess.PIPE)
    header = hp.stdout.readline().decode().replace('"', '').strip().split(",")
    hp.stdout.close()
    hp.kill()
    cols = [c for c in WANT if c in header]
    print(year, "cols:", cols)
    missing = [c for c in ["PWGTP", "AGEP", "SEX", "SCHL", "POBP", "YOEP", "WAGP"] if c not in cols]
    if missing:
        print("MISSING CRITICAL", missing)
    parts = [read_member(zpath, m, cols) for m in members]
    df = pd.concat(parts, ignore_index=True)
    df["YEAR"] = year
    out = os.path.join(CACHE, f"acs_{year}.parquet")
    df.to_parquet(out, index=False)
    print("wrote", out, len(df))


if __name__ == "__main__":
    main()
