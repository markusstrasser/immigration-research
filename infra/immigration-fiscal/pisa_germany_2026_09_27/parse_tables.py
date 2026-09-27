"""Parse PISA 2022 Vol I annex workbooks (StatLinks qmuad8 = ch.7 immigrant background, wh9d4z = ch.5 trends)
into a long CSV: table, country, group (OECD/Partners), column path, value.

Header rows sit between the table title and the first country row; labels of merged cells appear once and are
forward-filled to the right. Values 'm' (missing) and 'c' (too few observations) are kept as text.
"""
import csv, sys
import openpyxl

SRC = {"qmuad8": "_cache/statlink_qmuad8.xlsx", "wh9d4z": "_cache/statlink_wh9d4z.xlsx"}


def parse_sheet(ws):
    rows = [list(r) for r in ws.iter_rows(values_only=True)]
    # first data row = row whose first non-empty cell is 'OECD' (section label)
    start = next(i for i, r in enumerate(rows) if r and r[0] is not None and str(r[0]).strip() == "OECD")
    hdr_rows = [r for r in rows[2:start] if any(v is not None for v in r[1:])]
    ncol = max(len(r) for r in rows)
    paths = [[] for _ in range(ncol)]
    boundary = set()  # columns where a higher header row starts a new label: lower-row fill resets there
    for k, hr in enumerate(hdr_rows):
        last = None
        starts = set()
        for j in range(1, ncol):
            v = hr[j] if j < len(hr) else None
            if v is not None and str(v).strip() != "":
                last = str(v).replace("\n", " ").strip()
                starts.add(j)
            elif j in boundary or k == len(hdr_rows) - 1:
                last = None  # unit row (% / S.E.) and new parent spans are never forward-filled
            if last is not None:
                paths[j].append(last)
        boundary |= starts
    section, out = None, []
    for r in rows[start:]:
        if not r or r[0] is None:
            continue
        name = str(r[0]).strip()
        if name in ("OECD", "Partners"):
            section = name
            continue
        if name.startswith(("Note", "Source", "*", "1.", "2.", "3.")) and all(v is None for v in r[1:]):
            continue
        for j in range(1, min(len(r), ncol)):
            v = r[j]
            if v is None or (isinstance(v, str) and v.strip() == ""):
                continue
            p = [x for x in paths[j] if x]
            out.append((name, section, " / ".join(p), v))
    return out


def main(out_csv, wanted):
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["workbook", "table", "country", "section", "column", "value"])
        for key, path in SRC.items():
            wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
            for sh in wb.sheetnames:
                if not sh.startswith("Table") or sh not in wanted:
                    continue
                for name, sec, col, v in parse_sheet(wb[sh]):
                    w.writerow([key, sh, name, sec, col, v])


if __name__ == "__main__":
    wanted = set()
    for t in ["1", "2", "3", "4", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "13", "14", "9", "10"]:
        wanted.add(f"Table I.B1.7.{t}")
    for t in ["4", "5", "6"]:
        wanted.add(f"Table I.B1.5.{t}")
    main("derived/pisa2022_annex_long.csv", wanted)
