"""Recent arrivals (within about 5 years) vs settled immigrant-background pupils, PISA 2015 and 2022 student files.

BRIEF_2 addendum, test 5: split the first generation by age at arrival (ST021Q01TA) into recent arrivals
(arrived at age >= 10, i.e. within roughly 5-6 years of the test at 15-16) and earlier arrivals; >= 12 is kept
as the stricter band that matches OECD Table I.B1.7.13's "after age 12". Shares are weighted (W_FSTUWT) among
pupils with a valid IMMIG code, as in OECD Tables I.B1.7.1/7.2; first-generation pupils with a missing arrival
age are allocated in proportion (recent share = first-generation share x recent fraction among valid ages).
Inputs: _cache/microdata/stu2015_spss.zip, stu2022_spss.zip (webfs.oecd.org). Output: derived/arrival_within5.csv.
Usage: python3 arrival_microdata.py [--meta]
"""
import csv, os, sys, zipfile
import pyreadstat

FILES = {2015: "_cache/microdata/stu2015_spss.zip", 2022: "_cache/microdata/stu2022_spss.zip"}
COLS = ["CNT", "IMMIG", "ST021Q01TA", "W_FSTUWT"]


def sav_path(zpath):
    with zipfile.ZipFile(zpath) as z:
        name = max((n for n in z.namelist() if n.lower().endswith(".sav")), key=lambda n: z.getinfo(n).file_size)
        out = os.path.join(os.path.dirname(zpath), os.path.basename(name))
        if not os.path.exists(out) or os.path.getsize(out) != z.getinfo(name).file_size:
            with z.open(name) as src, open(out, "wb") as dst:
                while chunk := src.read(1 << 24):
                    dst.write(chunk)
    return out


def arrival_age(code, labels):
    """ST021Q01TA code -> age in years, from the file's own value label (e.g. '12 years', 'Younger than 12 months')."""
    lab = str(labels.get(code, code)).lower()
    if "month" in lab or lab.startswith(("0", "less", "younger")):
        return 0
    digits = "".join(ch if ch.isdigit() else " " for ch in lab).split()
    return int(digits[0]) if digits else None


def main():
    meta_only = "--meta" in sys.argv
    rows = []
    for cyc, z in FILES.items():
        path = sav_path(z)
        _, meta = pyreadstat.read_sav(path, metadataonly=True)
        labels = meta.variable_value_labels.get("ST021Q01TA", {})
        if meta_only:
            print(cyc, path, meta.number_rows, "ST021Q01TA label:", meta.column_names_to_labels.get("ST021Q01TA"))
            print("   values:", labels)
            print("   IMMIG:", meta.variable_value_labels.get("IMMIG"))
            continue
        acc = {}
        for df, _ in pyreadstat.read_file_in_chunks(pyreadstat.read_sav, path, chunksize=200000, usecols=COLS,
                                                    apply_value_formats=False):
            for cnt, immig, arr, w in df[COLS].itertuples(index=False):
                if immig not in (1, 2, 3) or w != w:
                    continue
                a = acc.setdefault(cnt, [0.0] * 7)  # n, wvalid, wimm, wg1, wg1_age_valid, wg1_recent10, wg1_recent12
                a[0] += 1; a[1] += w
                if immig in (2, 3):
                    a[2] += w
                if immig == 3:
                    a[3] += w
                    age = arrival_age(arr, labels) if arr == arr else None
                    if age is not None:
                        a[4] += w
                        a[5] += w * (age >= 10)
                        a[6] += w * (age >= 12)
        for cnt, (n, wv, wi, wg1, wva, wr10, wr12) in sorted(acc.items()):
            frac10 = wr10 / wva if wva else float("nan")
            frac12 = wr12 / wva if wva else float("nan")
            g1, imm = 100 * wg1 / wv, 100 * wi / wv
            rows.append([cnt, cyc, int(n), round(imm, 4), round(g1, 4), round(g1 * frac10, 4), round(g1 * frac12, 4),
                         round(imm - g1 * frac10, 4), round(1 - wva / wg1, 4) if wg1 else ""])
    if not meta_only:
        with open("derived/arrival_within5.csv", "w", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["cnt", "cycle", "n_valid_immig", "imm_share", "g1_share", "recent10_share", "recent12_share",
                        "settled10_share", "g1_missing_arrival_frac"])
            w.writerows(rows)
        print("rows", len(rows))


if __name__ == "__main__":
    main()
