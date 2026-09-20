#!/usr/bin/env python3
"""Institutional group-quarters share of men 18-39 by origin x nativity, ACS 1-year PUMS via the Census API.

Extends the origin/nativity comparison of Rumbaut et al. 2006, but DOES NOT replicate its
correctional-only outcome. TYPE/TYPEHUGQ=2 covers all institutional GQ (correctional,
nursing, mental, juvenile) and can include ICE detention. Public PUMS cannot split them.
These are institutional-residence shares, not detention-adjusted incarceration or crime rates.
NATIVITY=1 pools second and later generations: ACS has no parental birthplace.
HISP identifies self-reported origin, not country of birth. The adjusted Mexican rate
reallocates excess HISP=24 ("all other Hispanic") by population share; this is a sensitivity
scenario, not observed recovery of misclassified individuals. See README.md for scope.

Run:  uv run python3 pull_and_compute.py          (uses CENSUS_API_KEY from env or ../acquire/config.local.env;
                                                   skips fetching when the JSON tabulations are already here)
Out:  acs_institutional_rates.csv
"""
import csv, json, os, pathlib, re, urllib.request
HERE = pathlib.Path(__file__).parent
YEARS = {"2010": "TYPE", "2019": "TYPE", "2023": "TYPEHUGQ", "2024": "TYPEHUGQ"}
HISP = {"01": "Not Hispanic", "02": "Mexican", "03": "Puerto Rican", "04": "Cuban", "05": "Dominican",
        "07": "Guatemalan", "08": "Honduran", "11": "Salvadoran", "16": "Colombian", "24": "All other Hispanic"}
RAC1 = {"1": "NH White", "2": "NH Black", "3": "NH AIAN", "6": "NH Asian"}
ASIAN = ("Chinese", "Hmong", "Korean", "Cambodian", "Filipino", "Laotian", "Vietnamese", "Asian Indian", "Thai")

def key():
    k = os.environ.get("CENSUS_API_KEY")
    if not k:
        m = re.search(r"CENSUS_API_KEY=\"?([A-Za-z0-9]+)", (HERE.parent / "acquire/config.local.env").read_text())
        k = m.group(1)
    return k

def fetch(yr, gq, rows, extra, out):
    if out.exists():
        return
    url = (f"https://api.census.gov/data/{yr}/acs/acs1/pums?tabulate=weight(PWGTP)&col+{gq}"
           + "".join(f"&row+{r}" for r in rows) + f"&SEX=1&AGEP=18:39{extra}&key={key()}")
    out.write_bytes(urllib.request.urlopen(url, timeout=120).read())

def load(fn):
    d = json.load(open(HERE / fn)); hdr = d[0]
    tc = {list(h.values())[0]: i for i, h in enumerate(hdr) if isinstance(h, dict)}
    return {tuple(str(x) for x in r[len(tc):]): (r[tc["2"]], sum(r[i] for i in tc.values())) for r in d[1:]}

rows_out = []
for yr, gq in YEARS.items():
    fetch(yr, gq, ["NATIVITY", "HISP"], "", HERE / f"h{yr}.json")
    fetch(yr, gq, ["NATIVITY", "RAC1P"], "&HISP=01", HERE / f"r{yr}.json")
    h, r = load(f"h{yr}.json"), load(f"r{yr}.json")
    groups = [(h, HISP, "hispanic_origin"), (r, RAC1, "nh_race")]
    if yr != "2010":
        fetch(yr, gq, ["NATIVITY", "RAC2P"], "&HISP=01&RAC1P=6", HERE / f"a{yr}.json")
        vj = HERE / f"rac2p_{yr}.json"
        if not vj.exists():
            vj.write_bytes(urllib.request.urlopen(f"https://api.census.gov/data/{yr}/acs/acs1/pums/variables/RAC2P.json").read())
        labels = json.load(open(vj))["values"]["item"]
        codes = {c: l.replace(" alone", "").replace(", except Taiwanese", "") for c, l in labels.items()
                 if l.startswith(ASIAN) and "alone" in l}
        groups.append((load(f"a{yr}.json"), codes, "nh_asian_detail"))
    nat = {k[1]: v for k, v in h.items() if k[0] == "1"}
    inst_all, tot_all = (sum(v[i] for v in nat.values()) for i in (0, 1))
    base = inst_all / tot_all
    oth_i, oth_n = nat["24"]; hisp_named_n = sum(v[1] for k, v in nat.items() if k not in ("01", "24"))
    excess = max(0.0, oth_i - base * oth_n)
    for t, codes, block in groups:
        for code, name in codes.items():
            for natv, lab in (("1", "native"), ("2", "foreign_born")):
                inst, tot = t.get((natv, code), (0, 0))
                adj = inst
                if block == "hispanic_origin" and natv == "1" and code not in ("01", "24"):
                    adj = inst + excess * tot / hisp_named_n
                rows_out.append(dict(year=yr, block=block, group=name, nativity=lab, institutional=inst, population=tot,
                                     pct=round(100 * inst / tot, 3) if tot else None,
                                     pct_adj_generic_hispanic=round(100 * adj / tot, 3) if tot else None))
    rows_out.append(dict(year=yr, block="total", group="All", nativity="native", institutional=inst_all, population=tot_all,
                         pct=round(100 * base, 3), pct_adj_generic_hispanic=round(100 * base, 3)))
    fb = [v for k, v in h.items() if k[0] == "2"]
    rows_out.append(dict(year=yr, block="total", group="All", nativity="foreign_born", institutional=sum(v[0] for v in fb),
                         population=sum(v[1] for v in fb), pct=round(100 * sum(v[0] for v in fb) / sum(v[1] for v in fb), 3),
                         pct_adj_generic_hispanic=None))
with open(HERE / "acs_institutional_rates.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows_out[0])); w.writeheader(); w.writerows(rows_out)
for row in rows_out:
    if row["group"] in ("Mexican", "NH White", "All", "Salvadoran", "Vietnamese", "Cambodian") :
        print(row)
