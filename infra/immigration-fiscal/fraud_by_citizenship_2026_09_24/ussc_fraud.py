"""Federal fraud sentences by offender citizenship, FY2015-FY2024.

Source: US Sentencing Commission individual offender datafiles (CSV, one zip per fiscal year,
about 27,000 columns, streamed with pyarrow) joined on USSCIDN to the Commission's
economic-crime offense-type files, which assign every individual sentenced under USSG §2B1.1 to
one type (health care, government benefits, ...). Denominators: ACS 1-year B05003 (adults by
nativity and citizenship) and B05003I (the same for Hispanic or Latino adults).

Two fraud definitions, because they differ in who they catch:
- primary sentencing guideline GDLINEHI == "2B1.1" (FY2015-2024). This is the universe of the
  economic-crime files and of the loss variable; it excludes cases sentenced without guideline
  data and fraud schemes sentenced under the laundering guideline §2S1.1.
- the Commission's offense type OFFGUIDE == 16, "Fraud/Theft/Embezzlement" (FY2018-2024), the
  Sourcebook definition. It adds cases without guideline data, most of them short identity-
  document cases (18 USC 1028, 42 USC 408, 18 USC 1001) against noncitizens.
Sensitivities: §2B1.1 cases with positive recorded loss, and §2B1.1 plus §2S1.1 cases with a
fraud statute of conviction (fraud schemes sentenced as laundering).

Loss: LOSSHI, "the dollar amount of loss for which the sentenced individual is held
responsible" (codebook PDF p.37), for the primary guideline computation. Under USSG §2B1.1
comment. n.3(A) that is the greater of actual or intended loss; in government health care cases
the amount billed is prima facie intended loss (n.3(F)(viii)). Co-defendants are each held
responsible for the scheme's foreseeable loss (§1B1.3(a)(1)(B)), so sums over offenders
overstate scheme totals. Rows with LOSSPROB == 1 and the "some loss, amount not specified" code
are excluded from loss dollars.

Unauthorized and legal noncitizen adults: UNAUTH_SHARE (0.50, band 0.45-0.55) times ACS
noncitizen adults; derived/unauth_share_check.csv shows where the share comes from (Pew
Research Center, August 21 2025; the repo's ACS 2024 residual).

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3 \
      infra/immigration-fiscal/fraud_by_citizenship_2026_09_24/ussc_fraud.py [--fetch]
--fetch downloads missing inputs into _cache/ with curl (ACS needs CENSUS_API_KEY in the
environment; the key is never printed).
"""
from pathlib import Path
import argparse
import csv
import hashlib
import io
import json
import os
import re
import subprocess
import zipfile

import pandas as pd
import pyarrow as pa
import pyarrow.csv as pc

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
USSC = CACHE / "ussc"
ACS = CACHE / "acs"
OUT = HERE / "derived"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
USSC_ZIP = "https://www.ussc.gov/sites/default/files/zip/"
USSC_PDF = "https://www.ussc.gov/sites/default/files/pdf/research-and-publications/datafiles/"
CODEBOOKS = ["USSC_Public_Release_Codebook_FY99_FY25.pdf", "USSC_Economic_Crime_Codebook_FY13_FY25.pdf"]

FYS = list(range(2015, 2025))
COMM_FYS = list(range(2018, 2025))  # OFFGUIDE exists from FY2018
MN_EXTRA_FYS = [2025]  # Minnesota district check only; used when the file is present
ACS_YEARS = [2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023, 2024]  # no standard 2020 1-year
POOLED = "pooled_2015_2024"
POOLED_COMM = "pooled_2018_2024"

COLS = ["USSCIDN", "AGE", "CITIZEN", "CITWHERE", "HISPORIG", "DISTRICT", "OFFGUIDE",
        "GDLINEHI", "LOSSHI", "LOSSPROB", "AMTREST"]
CITIZEN = {"1": "us_citizen", "2": "legal_alien", "3": "illegal_alien",
           "4": "noncitizen_unknown", "5": "extradited_alien"}
STATUSES = list(CITIZEN.values())
RESIDENT_NONCIT = ["legal_alien", "illegal_alien", "noncitizen_unknown"]
NONCIT = RESIDENT_NONCIT + ["extradited_alien"]
LOSS_UNSPECIFIED = 9_999_999_997
MN_DISTRICT = "64"
# Commission offense types (codebook Appendix A, OFFGUIDE).
OFFGUIDE = {"16": "comm_fraud_theft_embezzlement", "10": "comm_drug_trafficking",
            "13": "comm_firearms", "17": "comm_immigration", "21": "comm_money_laundering",
            "7": "comm_child_pornography"}
# Statutes of conviction that mark a fraud scheme (NWSTAT is title + section + subsection,
# e.g. "181343" = 18 USC 1343): mail, wire, bank, health care fraud and fraud conspiracy,
# access devices, theft of public money, federal-program theft, false claims, health care
# false statements, the Medicare/Medicaid kickback statute, SNAP fraud.
FRAUD_STATUTE = re.compile(r"^(?:18(?:1341|1343|1344|1347|1349|1029|1035|641|666|287)|421320A7B|72024)")

# Economic-crime types. FY2013-19 ECON_COMBINED is folded into the FY2020+ ECON_OFF_TYPE
# categories as the codebook instructs (p.3): credit card + financial institution combine;
# disaster, immigration, retirement/unemployment, campaign finance, contract, education
# funds and weapons join all other.
ECON_OLD = {1: "securities", 2: "health_care", 3: "mortgage", 4: "credit_card_financial",
            5: "credit_card_financial", 6: "gov_procurement", 7: "gov_benefits",
            8: "identity_theft", 9: "counterfeit_forgery", 10: "mail", 11: "computer",
            12: "intellectual_property", 13: "embezzlement_theft", 14: "tax", 15: "insurance",
            17: "advance_fee", 18: "false_advertising", 20: "bankruptcy", 22: "antitrust",
            24: "false_statements", 29: "money_laundering"}
ECON_NEW = {1: "securities", 2: "health_care", 3: "mortgage", 4: "credit_card_financial",
            5: "gov_procurement", 6: "gov_benefits", 7: "identity_theft",
            8: "counterfeit_forgery", 9: "mail", 10: "computer", 11: "intellectual_property",
            12: "embezzlement_theft", 13: "tax", 14: "insurance", 15: "advance_fee",
            16: "false_advertising", 17: "bankruptcy", 18: "antitrust", 19: "false_statements",
            20: "money_laundering", 21: "all_other"}
GOV_VICTIM = ["health_care", "gov_benefits", "gov_procurement"]

# Unauthorized share of noncitizens [CALCULATION, see unauth_share_check()]; band 0.45-0.55.
UNAUTH_SHARE = {"low": 0.45, "central": 0.50, "high": 0.55}
# Pew Research Center, "U.S. Unauthorized Immigrant Population Reached a Record 14 Million in
# 2023", August 21 2025 (sources/immigration-fiscal/data/pew/pew-unauthorized-immigrants-2025.pdf):
# p.5 chart labels (all ages, coverage-adjusted) and p.10 lawful immigrants 37.8M of whom
# naturalized 23.8M.
PEW_UNAUTH = {2015: 11.0e6, 2019: 10.2e6, 2021: 10.5e6, 2022: 11.8e6, 2023: 14.0e6}
PEW_2023_LAWFUL_NONCIT = 37.8e6 - 23.8e6
# ../unauthorized_population_size_2026_09_19/RESULT.md §3: ACS 2024 1-year PUMS residual,
# Borjas rules, no coverage adjustment.
REPO_ACS2024_RESIDUAL = 12_973_901

# GAO-24-105833 (April 2024), PDF p.24: direct annual federal fraud losses, FY2018-2022.
GAO_FRAUD_BN = (233.0, 521.0)
GAO_FYS = list(range(2018, 2023))

# Sourcebook Table 9, Fraud/Theft/Embezzlement (_cache/ussc/sourcebook/table9_2019.pdf,
# table9_2022.pdf; ../detention_evidence_2026_09_20/_cache/ussc_2024_table9.pdf).
SOURCEBOOK_T9 = {2019: {"records": 76538, "known": 76110, "fraud": 6328, "citizen": 5116, "non": 1212},
                 2022: {"records": 64142, "known": 63841, "fraud": 5489, "citizen": 4645, "non": 844},
                 2024: {"records": 61678, "known": 61342, "fraud": 5287, "citizen": 4569, "non": 718}}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def curl(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["curl", "-sS", "-L", "-f", "-A", UA, "-o", str(dest), url],
                       capture_output=True, text=True)
    if r.returncode != 0:
        msg = re.sub(r"key=[A-Za-z0-9]+", "key=<KEY>", r.stderr + " " + url)
        dest.unlink(missing_ok=True)
        raise SystemExit(f"[BLOCKED] download failed: {msg.strip()}")


def fetch() -> None:
    for fy in FYS + MN_EXTRA_FYS:
        yy = f"{fy % 100:02d}"
        for name in (f"opafy{yy}nid_csv.zip", f"econ{yy}_csv.zip"):
            if not (USSC / name).exists():
                print(f"[fetch] {name}")
                curl(USSC_ZIP + name, USSC / name)
    for name in CODEBOOKS:
        if not (USSC / name).exists():
            curl(USSC_PDF + name, USSC / name)
    key = os.environ.get("CENSUS_API_KEY", "")
    for year in ACS_YEARS:
        for group in ("B05003", "B05003I"):
            dest = ACS / f"{group}_{year}.json"
            if dest.exists():
                continue
            if not key:
                raise SystemExit("[BLOCKED] CENSUS_API_KEY not set; source "
                                 "infra/immigration-fiscal/acquire/config.local.env")
            print(f"[fetch] ACS {group} {year}")
            curl(f"https://api.census.gov/data/{year}/acs/acs1?get=group({group})"
                 f"&for=us:1&key={key}", dest)


def require_inputs() -> None:
    missing = [p for p in
               [USSC / f"opafy{fy % 100:02d}nid_csv.zip" for fy in FYS]
               + [USSC / f"econ{fy % 100:02d}_csv.zip" for fy in FYS]
               + [ACS / f"{g}_{y}.json" for y in ACS_YEARS for g in ("B05003", "B05003I")]
               + [USSC / CODEBOOKS[0]]
               if not p.exists()]
    if missing:
        raise SystemExit("[BLOCKED] missing inputs (run with --fetch):\n  "
                         + "\n  ".join(str(p.relative_to(HERE)) for p in missing))


def read_year(fy: int) -> pd.DataFrame:
    """One fiscal year of sentenced individuals, selected columns, econ type joined."""
    path = USSC / f"opafy{fy % 100:02d}nid_csv.zip"
    with zipfile.ZipFile(path) as z:
        member = z.namelist()[0]
        with z.open(member) as f:
            header = next(csv.reader(io.TextIOWrapper(f, encoding="latin-1")))
        actual = {h.upper(): h for h in header}
        stat_cols = sorted((h for h in actual if re.fullmatch(r"NWSTAT\d+", h)),
                           key=lambda h: int(h[6:]))
        want = [actual[c] for c in COLS + stat_cols if c in actual]
        with z.open(member) as f:
            tbl = pc.read_csv(f, read_options=pc.ReadOptions(block_size=64 << 20),
                              convert_options=pc.ConvertOptions(
                                  include_columns=want,
                                  column_types={c: pa.string() for c in want},
                                  strings_can_be_null=True))
    df = tbl.to_pandas()
    df.columns = [c.upper() for c in df.columns]
    for c in COLS:
        if c not in df.columns:
            df[c] = None
    statutes = df[stat_cols]
    df = df[COLS].copy()
    df["FY"] = fy
    df["status"] = df.CITIZEN.map(CITIZEN).fillna("missing")
    df["hisp"] = df.HISPORIG.map({"2": "hispanic", "1": "non_hispanic"}).fillna("unknown")
    df["fraud"] = df.GDLINEHI.eq("2B1.1")
    df["comm"] = df.OFFGUIDE.map(OFFGUIDE).where(df.OFFGUIDE.notna(), None)
    df.loc[df.OFFGUIDE.notna() & df.comm.isna(), "comm"] = "comm_other"
    fraud_stat = statutes.apply(lambda col: col.str.contains(FRAUD_STATUTE, na=False)).any(axis=1)
    df["fraud_laundering"] = df.GDLINEHI.str.startswith("2S1.", na=False) & fraud_stat
    keep = df.fraud | df.OFFGUIDE.eq("16")
    joined = statutes[keep].stack().dropna().groupby(level=0).agg(lambda v: " ".join(sorted(set(v))))
    df["statutes"] = joined.reindex(df.index)
    raw_loss = pd.to_numeric(df.LOSSHI, errors="coerce")
    df["loss_positive"] = raw_loss.gt(0)
    df["loss_unspecified"] = raw_loss.eq(LOSS_UNSPECIFIED)
    df["loss"] = raw_loss.where(raw_loss.lt(LOSS_UNSPECIFIED) & df.LOSSPROB.ne("1"))
    rest = pd.to_numeric(df.AMTREST, errors="coerce")
    df["restitution"] = rest.where(rest.lt(9_999_999_990))

    epath = USSC / f"econ{fy % 100:02d}_csv.zip"
    with zipfile.ZipFile(epath) as z, z.open(z.namelist()[0]) as f:
        econ = pd.read_csv(f, dtype=str)
    econ.columns = [c.upper() for c in econ.columns]
    if "ECON_OFF_TYPE" in econ.columns:
        econ["subtype"] = pd.to_numeric(econ.ECON_OFF_TYPE).map(ECON_NEW)
    else:
        econ["subtype"] = pd.to_numeric(econ.ECON_COMBINED).map(ECON_OLD).fillna("all_other")
    dup = econ.USSCIDN.duplicated().sum()
    if dup:
        raise SystemExit(f"[BLOCKED] FY{fy} econ file has {dup} duplicate USSCIDN")
    orphan = (~econ.USSCIDN.isin(df.USSCIDN)).sum()
    if orphan:
        raise SystemExit(f"[BLOCKED] FY{fy}: {orphan} econ records not in the individual file")
    df = df.merge(econ[["USSCIDN", "subtype"]], on="USSCIDN", how="left", validate="1:1")
    stray = df.subtype.notna() & ~df.fraud
    if stray.any():
        raise SystemExit(f"[BLOCKED] FY{fy}: {stray.sum()} econ records outside GDLINEHI 2B1.1")
    df.loc[df.fraud & df.subtype.isna(), "subtype"] = "unclassified"
    return df


def acs_denominators() -> pd.DataFrame:
    rows = []
    for year in ACS_YEARS:
        rec = {"acs_year": year}
        for group, tag in (("B05003", "all"), ("B05003I", "hisp")):
            header, values = json.loads((ACS / f"{group}_{year}.json").read_text())
            d = dict(zip(header, values))

            def v(n: int) -> int:
                return int(d[f"{group}_{n:03d}E"])
            rec[f"{tag}_citizen_adults"] = v(9) + v(20) + v(11) + v(22)
            rec[f"{tag}_naturalized_adults"] = v(11) + v(22)
            rec[f"{tag}_noncit_adults"] = v(12) + v(23)
            rec[f"{tag}_noncit_all_ages"] = v(7) + v(18) + v(12) + v(23)
        rows.append(rec)
    acs = pd.DataFrame(rows).set_index("acs_year")
    acs.loc[2020] = (acs.loc[2019] + acs.loc[2021]) / 2  # [CALCULATION] no standard 2020 1-year
    acs = acs.sort_index().round().astype("int64")
    for base in ("citizen_adults", "naturalized_adults", "noncit_adults", "noncit_all_ages"):
        acs[f"nonhisp_{base}"] = acs[f"all_{base}"] - acs[f"hisp_{base}"]
    for k, s in UNAUTH_SHARE.items():
        acs[f"unauth_adults_{k}"] = (acs.all_noncit_adults * s).round().astype("int64")
        acs[f"legal_noncit_adults_{k}"] = (acs.all_noncit_adults * (1 - s)).round().astype("int64")
    acs.index.name = "FY"
    return acs


def unauth_share_check(acs: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for year, u in PEW_UNAUTH.items():
        if year >= 2022:
            continue  # Pew's 2022-23 figures sit on the Vintage-2024 augmented base, not ACS
        base = int(acs.loc[year, "all_noncit_all_ages"])
        rows.append({"source": f"Pew {year} unauthorized / ACS {year} noncitizens (all ages)",
                     "unauthorized": u, "noncitizens": base, "share": u / base})
    rows.append({"source": "Pew 2023 unauthorized / Pew 2023 noncitizens (own base)",
                 "unauthorized": PEW_UNAUTH[2023],
                 "noncitizens": PEW_UNAUTH[2023] + PEW_2023_LAWFUL_NONCIT,
                 "share": PEW_UNAUTH[2023] / (PEW_UNAUTH[2023] + PEW_2023_LAWFUL_NONCIT)})
    base = int(acs.loc[2024, "all_noncit_all_ages"])
    rows.append({"source": "Repo ACS 2024 residual (Borjas rules, uncorrected) / ACS 2024 noncitizens",
                 "unauthorized": REPO_ACS2024_RESIDUAL, "noncitizens": base,
                 "share": REPO_ACS2024_RESIDUAL / base})
    out = pd.DataFrame(rows)
    out["share"] = out.share.round(4)
    return out


def loss_stats(g: pd.DataFrame) -> dict:
    loss = g.loss.dropna()
    rest = g.restitution.dropna()
    return {"offenders": len(g),
            "loss_positive_n": int(g.loss_positive.sum()),
            "loss_n": len(loss),
            "loss_unspecified_n": int(g.loss_unspecified.sum()),
            "loss_sum_musd": round(loss.sum() / 1e6, 3),
            "loss_median_usd": round(float(loss.median()), 0) if len(loss) else None,
            "loss_mean_usd": round(float(loss.mean()), 0) if len(loss) else None,
            "loss_n_ge_100m": int(loss.ge(1e8).sum()),
            "loss_share_from_ge_100m": round(loss[loss.ge(1e8)].sum() / loss.sum(), 4) if loss.sum() else None,
            "restitution_n_positive": int(rest.gt(0).sum()),
            "restitution_sum_musd": round(rest.sum() / 1e6, 3)}


def per100k(n: float, d: float) -> float:
    return round(n / d * 1e5, 4) if d else None


def status_rates(counts: dict, acs_row: pd.Series, prefix: str = "all") -> list[dict]:
    """Rates per 100,000 adults of the same status; code 4 and the share band give ranges."""
    n = {s: counts.get(s, 0) for s in STATUSES}
    noncit = acs_row[f"{prefix}_noncit_adults"]
    out = [{"status": "us_citizen", "offenders": n["us_citizen"],
            "denominator": int(acs_row[f"{prefix}_citizen_adults"]),
            "rate": per100k(n["us_citizen"], acs_row[f"{prefix}_citizen_adults"]),
            "rate_low": None, "rate_high": None},
           {"status": "noncitizen_resident", "offenders": sum(n[s] for s in RESIDENT_NONCIT),
            "denominator": int(noncit),
            "rate": per100k(sum(n[s] for s in RESIDENT_NONCIT), noncit),
            "rate_low": None, "rate_high": None}]
    if prefix == "all":
        lo, mid, hi = UNAUTH_SHARE["low"], UNAUTH_SHARE["central"], UNAUTH_SHARE["high"]
        out.append({"status": "legal_alien", "offenders": n["legal_alien"],
                    "denominator": int(round(noncit * (1 - mid))),
                    "rate": per100k(n["legal_alien"], noncit * (1 - mid)),
                    "rate_low": per100k(n["legal_alien"], noncit * (1 - lo)),
                    "rate_high": per100k(n["legal_alien"] + n["noncitizen_unknown"], noncit * (1 - hi))})
        out.append({"status": "illegal_alien", "offenders": n["illegal_alien"],
                    "denominator": int(round(noncit * mid)),
                    "rate": per100k(n["illegal_alien"], noncit * mid),
                    "rate_low": per100k(n["illegal_alien"], noncit * hi),
                    "rate_high": per100k(n["illegal_alien"] + n["noncitizen_unknown"], noncit * lo)})
        for s in ("noncitizen_unknown", "extradited_alien"):
            out.append({"status": s, "offenders": n[s], "denominator": None, "rate": None,
                        "rate_low": None, "rate_high": None})
    return out


def rate_block(sel: pd.DataFrame, offense: str, acs: pd.DataFrame, fys: list[int],
               pooled: str, pooled_only: bool = False) -> list[dict]:
    """Per-year and pooled status rates for one offense selection."""
    rows = []
    if not pooled_only:
        for fy in fys:
            counts = sel[sel.FY == fy].status.value_counts().to_dict()
            rows += [{"FY": str(fy), "offense": offense, **r} for r in status_rates(counts, acs.loc[fy])]
    counts = sel[sel.FY.isin(fys)].status.value_counts().to_dict()
    rows += [{"FY": pooled, "offense": offense, **r} for r in status_rates(counts, acs.loc[fys].sum())]
    return rows


def codebook_labels() -> tuple[dict, dict]:
    """CITWHERE (country) and DISTRICT labels from codebook Appendix A."""
    txt = subprocess.run(["pdftotext", "-layout", str(USSC / CODEBOOKS[0]), "-"],
                         capture_output=True, text=True, check=True).stdout
    start = txt.index("\nCITWHERE\n")
    mid = txt.index("\nDISTRICT\n", start)
    end = txt.index("\nDRUGTYP1-DRUGTYPX\n", mid)
    countries, districts = {}, {}
    for line in txt[start:mid].splitlines():
        for code, name in re.findall(r"(\d{2,3}) = (.+?)(?=\s{2,}\d{2,3} = |\s*$)", line):
            countries[code] = name.strip()
    for line in txt[mid:end].splitlines():
        for code, name in re.findall(r"(\d{2}) = '([^']+)'", line):
            districts[str(int(code))] = name
    return countries, districts


def top_statutes(sel: pd.DataFrame, label: str, k: int = 10) -> list[dict]:
    """Most frequent statutes of conviction (NWSTAT) by citizenship status."""
    rows = []
    for status in ("us_citizen", "legal_alien", "illegal_alien"):
        g = sel[sel.status == status]
        counts = g.statutes.dropna().str.split().explode().value_counts()
        counts = counts.sort_index().sort_values(ascending=False, kind="stable").head(k)
        rows += [{"selection": label, "status": status, "cases": len(g), "statute": st,
                  "cases_with_statute": int(n)} for st, n in counts.items()]
    return rows


def status_counts(g: pd.DataFrame) -> dict:
    return {s: int((g.status == s).sum()) for s in STATUSES + ["missing"]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true", help="download missing inputs first")
    args = ap.parse_args()
    if args.fetch:
        fetch()
    require_inputs()
    OUT.mkdir(exist_ok=True)

    years = {fy: read_year(fy) for fy in FYS}
    mn_years = [fy for fy in MN_EXTRA_FYS
                if (USSC / f"opafy{fy % 100:02d}nid_csv.zip").exists()
                and (USSC / f"econ{fy % 100:02d}_csv.zip").exists()]
    extra = {fy: read_year(fy) for fy in mn_years}
    allx = pd.concat(years.values(), ignore_index=True)
    acs = acs_denominators()
    labels, districts = codebook_labels()
    fraud = allx[allx.fraud]

    # 1. §2B1.1 by citizenship status and year: offenders, loss, restitution.
    rows = []
    for fy, g in fraud.groupby("FY"):
        rows += [{"FY": str(fy), "status": s, **loss_stats(g[g.status == s])} for s in STATUSES + ["missing"]]
        rows.append({"FY": str(fy), "status": "all", **loss_stats(g)})
    rows += [{"FY": POOLED, "status": s, **loss_stats(fraud[fraud.status == s])} for s in STATUSES + ["missing"]]
    rows.append({"FY": POOLED, "status": "all", **loss_stats(fraud)})
    pd.DataFrame(rows).to_csv(OUT / "fraud_by_citizenship_year.csv", index=False)

    # 2. Economic-crime subtypes by citizenship status.
    sub_rows = []
    for (fy, sub), g in fraud.groupby(["FY", "subtype"]):
        sub_rows += [{"FY": str(fy), "subtype": sub, "status": s, **loss_stats(g[g.status == s])}
                     for s in STATUSES + ["missing"]]
    for sub, g in fraud.groupby("subtype"):
        sub_rows += [{"FY": POOLED, "subtype": sub, "status": s, **loss_stats(g[g.status == s])}
                     for s in STATUSES + ["missing"]]
    pd.DataFrame(sub_rows).to_csv(OUT / "fraud_subtypes_by_citizenship.csv", index=False)
    stat_rows = top_statutes(fraud[fraud.subtype == "gov_benefits"], "2B1.1_gov_benefits_fy2015_2024")
    stat_rows += top_statutes(allx[allx.FY.isin(COMM_FYS) & allx.OFFGUIDE.eq("16") & ~allx.fraud],
                              "offguide16_not_2B1.1_fy2018_2024")
    stat_rows += top_statutes(fraud, "2B1.1_all_fy2015_2024")
    pd.DataFrame(stat_rows).to_csv(OUT / "top_statutes.csv", index=False)

    # 3. Rates per 100,000 adults of the same status.
    loss_pos = fraud[fraud.loss_positive]
    plus_laundering = allx[allx.fraud | allx.fraud_laundering]
    rate_rows = rate_block(fraud, "fraud_2B1.1", acs, FYS, POOLED)
    rate_rows += rate_block(loss_pos, "fraud_2B1.1_loss_positive", acs, FYS, POOLED)
    rate_rows += rate_block(plus_laundering, "fraud_2B1.1_plus_fraud_laundering", acs, FYS, POOLED)
    for sub in GOV_VICTIM:
        rate_rows += rate_block(fraud[fraud.subtype == sub], sub, acs, FYS, POOLED)
    gb = fraud[(fraud.subtype == "gov_benefits") & fraud.loss_positive]
    rate_rows += rate_block(gb, "gov_benefits_loss_positive", acs, FYS, POOLED)
    comm = allx[allx.FY.isin(COMM_FYS) & allx.comm.notna()]
    for name in sorted(set(OFFGUIDE.values())):
        rate_rows += rate_block(comm[comm.comm == name], name, acs, COMM_FYS, POOLED_COMM)
    rate_rows += rate_block(comm[comm.comm != "comm_immigration"], "comm_all_except_immigration",
                            acs, COMM_FYS, POOLED_COMM)
    rate_rows += rate_block(comm, "comm_all_offenses", acs, COMM_FYS, POOLED_COMM)
    # The §2B1.1 definitions again over FY2018-2024, so ratios compare like with like.
    for sel, name in ((fraud, "fraud_2B1.1"), (loss_pos, "fraud_2B1.1_loss_positive"),
                      (plus_laundering, "fraud_2B1.1_plus_fraud_laundering")):
        rate_rows += rate_block(sel, name, acs, COMM_FYS, POOLED_COMM, pooled_only=True)
    rates = pd.DataFrame(rate_rows)
    rates.to_csv(OUT / "rates_per_100k.csv", index=False)

    # 4. Ratio of the resident-noncitizen rate to the citizen rate, by offense definition.
    wide = rates[rates.status.isin(["us_citizen", "noncitizen_resident"])].pivot_table(
        index=["FY", "offense"], columns="status", values=["rate", "offenders"], aggfunc="first")
    wide.columns = [f"{a}_{b}" for a, b in wide.columns]
    wide = wide.reset_index()
    wide["noncit_to_citizen_ratio"] = (wide.rate_noncitizen_resident / wide.rate_us_citizen).round(3)
    wide.sort_values(["offense", "FY"]).to_csv(OUT / "ratio_by_offense.csv", index=False)

    # 5. Hispanic origin by citizenship (citizen vs resident noncitizen), §2B1.1.
    h_rows = []
    for fy in FYS + [POOLED]:
        g = fraud if fy == POOLED else fraud[fraud.FY == fy]
        acs_row = acs.loc[FYS].sum() if fy == POOLED else acs.loc[fy]
        for hisp, prefix in (("hispanic", "hisp"), ("non_hispanic", "nonhisp")):
            counts = g[g.hisp == hisp].status.value_counts().to_dict()
            h_rows += [{"FY": str(fy), "hisp": hisp, "status": r["status"], "offenders": r["offenders"],
                        "denominator": r["denominator"], "rate": r["rate"]}
                       for r in status_rates(counts, acs_row, prefix=prefix)]
        h_rows.append({"FY": str(fy), "hisp": "unknown", "status": "all_statuses",
                       "offenders": int((g.hisp == "unknown").sum()), "denominator": None, "rate": None})
    pd.DataFrame(h_rows).to_csv(OUT / "fraud_by_hispanic_citizenship.csv", index=False)

    # 6. Country of citizenship of noncitizen offenders, pooled FY2015-2024.
    nc = allx[allx.status.isin(NONCIT)]
    ncf = nc[nc.fraud]
    ncc = nc[nc.comm.eq("comm_fraud_theft_embezzlement")]
    ctab = pd.DataFrame({
        "fraud_2B1.1": ncf.CITWHERE.value_counts(),
        "fraud_legal_alien": ncf[ncf.status == "legal_alien"].CITWHERE.value_counts(),
        "fraud_illegal_alien": ncf[ncf.status == "illegal_alien"].CITWHERE.value_counts(),
        "fraud_unknown_or_extradited": ncf[ncf.status.isin(["noncitizen_unknown", "extradited_alien"])].CITWHERE.value_counts(),
        "fraud_loss_positive": ncf[ncf.loss_positive].CITWHERE.value_counts(),
        "fraud_loss_musd": ncf.groupby("CITWHERE").loss.sum() / 1e6,
        "health_care": ncf[ncf.subtype == "health_care"].CITWHERE.value_counts(),
        "gov_benefits": ncf[ncf.subtype == "gov_benefits"].CITWHERE.value_counts(),
        "credit_card_financial": ncf[ncf.subtype == "credit_card_financial"].CITWHERE.value_counts(),
        "identity_theft": ncf[ncf.subtype == "identity_theft"].CITWHERE.value_counts(),
        "comm_fraud_fy2018_2024": ncc.CITWHERE.value_counts(),
        "all_offenses_noncitizen": nc.CITWHERE.value_counts(),
        "non_immigration_fy2018_2024": nc[nc.comm.notna() & nc.comm.ne("comm_immigration")].CITWHERE.value_counts(),
    }).fillna(0)
    ctab["fraud_loss_musd"] = ctab.fraud_loss_musd.round(3)
    int_cols = [c for c in ctab.columns if c != "fraud_loss_musd"]
    ctab[int_cols] = ctab[int_cols].astype("int64")
    ctab.index.name = "CITWHERE"
    ctab = ctab.reset_index()
    ctab.insert(1, "country", ctab.CITWHERE.map(labels).fillna("missing/unlisted"))
    ctab.sort_values(["fraud_2B1.1", "CITWHERE"], ascending=[False, True]).to_csv(
        OUT / "fraud_by_country_pooled.csv", index=False)

    # 6b. Where government-victim fraud is sentenced: districts, pooled FY2015-2024.
    gvd = fraud[fraud.subtype.isin(GOV_VICTIM)]
    drows = []
    for dist, g in gvd.groupby("DISTRICT"):
        noncit = g[g.status.isin(NONCIT)]
        top = noncit.CITWHERE.value_counts()
        top = top[top.index.sort_values()].sort_values(ascending=False, kind="stable")
        drows.append({"DISTRICT": dist, "district": districts.get(dist, "unlisted"),
                      "offenders": len(g), "health_care": int(g.subtype.eq("health_care").sum()),
                      "gov_benefits": int(g.subtype.eq("gov_benefits").sum()),
                      "gov_procurement": int(g.subtype.eq("gov_procurement").sum()),
                      "loss_sum_musd": round(g.loss.sum() / 1e6, 3),
                      "noncitizen_share": round(len(noncit) / len(g), 4),
                      "noncitizen_loss_share": round(noncit.loss.sum() / g.loss.sum(), 4) if g.loss.sum() else None,
                      "hispanic_share": round(g.hisp.eq("hispanic").mean(), 4),
                      "top_noncitizen_country": labels.get(top.index[0], "missing") if len(top) else None,
                      "top_noncitizen_country_n": int(top.iloc[0]) if len(top) else 0})
    pd.DataFrame(drows).sort_values(["loss_sum_musd", "DISTRICT"], ascending=[False, True]).to_csv(
        OUT / "gov_victim_fraud_by_district.csv", index=False)

    # 7. District of Minnesota, FY2015-2024 plus FY2025 when present: §2B1.1 by subtype, and
    #    fraud schemes sentenced under the laundering guideline.
    mn = pd.concat([allx] + list(extra.values()), ignore_index=True)
    mn = mn[mn.DISTRICT == MN_DISTRICT]
    fy_all = sorted(mn.FY.unique())
    span_all = f"pooled_{fy_all[0]}_{fy_all[-1]}"
    mn_rows = []
    for (fy, sub), g in mn[mn.fraud].groupby(["FY", "subtype"]):
        mn_rows.append({"FY": str(fy), "selection": "2B1.1", "subtype": sub, "offenders": len(g),
                        **status_counts(g), "loss_sum_musd": round(g.loss.sum() / 1e6, 3)})
    for fy, g in mn[mn.fraud_laundering].groupby("FY"):
        mn_rows.append({"FY": str(fy), "selection": "2S1_fraud_statute", "subtype": "laundering",
                        "offenders": len(g), **status_counts(g), "loss_sum_musd": round(g.loss.sum() / 1e6, 3)})
    for fy, g in mn.groupby("FY"):
        mn_rows.append({"FY": str(fy), "selection": "all_offenses", "subtype": "all", "offenders": len(g),
                        **status_counts(g), "loss_sum_musd": None})
    for label, sel in (("2B1.1", mn.fraud), ("2S1_fraud_statute", mn.fraud_laundering)):
        for span, fys in ((span_all, fy_all), ("pooled_2022_2025", [2022, 2023, 2024, 2025])):
            g = mn[sel & mn.FY.isin(fys)]
            mn_rows.append({"FY": span, "selection": label, "subtype": "all", "offenders": len(g),
                            **status_counts(g), "loss_sum_musd": round(g.loss.sum() / 1e6, 3)})
    for sub in ("gov_benefits", "health_care"):
        g = mn[mn.fraud & mn.subtype.eq(sub)]
        mn_rows.append({"FY": span_all, "selection": "2B1.1", "subtype": sub, "offenders": len(g),
                        **status_counts(g), "loss_sum_musd": round(g.loss.sum() / 1e6, 3)})
    pd.DataFrame(mn_rows).to_csv(OUT / "minnesota_district.csv", index=False)
    mnc = mn[mn.status.isin(NONCIT)]
    mn_country = pd.DataFrame({
        "fraud_2B1.1": mnc[mnc.fraud].CITWHERE.value_counts(),
        "fraud_laundering_2S1": mnc[mnc.fraud_laundering].CITWHERE.value_counts(),
        "gov_benefits": mnc[mnc.subtype == "gov_benefits"].CITWHERE.value_counts(),
        "health_care": mnc[mnc.subtype == "health_care"].CITWHERE.value_counts(),
        "all_offenses": mnc.CITWHERE.value_counts()}).fillna(0).astype("int64")
    mn_country.index.name = "CITWHERE"
    mn_country = mn_country.reset_index()
    mn_country.insert(1, "country", mn_country.CITWHERE.map(labels).fillna("missing/unlisted"))
    mn_country.sort_values(["fraud_2B1.1", "all_offenses", "CITWHERE"],
                           ascending=[False, False, True]).to_csv(
        OUT / "minnesota_noncitizen_country.csv", index=False)

    # 8. Implied annual federal fraud by citizenship group [CALCULATION]: shares of the
    #    government-victim §2B1.1 cases sentenced FY2018-2022 (GAO's window) times GAO's range.
    gv = fraud[fraud.subtype.isin(GOV_VICTIM) & fraud.FY.isin(GAO_FYS) & fraud.status.ne("missing")]
    grp = gv.status.where(gv.status.isin(["us_citizen", "legal_alien", "illegal_alien"]),
                          "unknown_or_extradited")
    pop = acs.loc[GAO_FYS].sum()
    total_pop = pop.all_citizen_adults + pop.all_noncit_adults
    pop_share = {"us_citizen": pop.all_citizen_adults / total_pop,
                 "legal_alien": pop.all_noncit_adults * (1 - UNAUTH_SHARE["central"]) / total_pop,
                 "illegal_alien": pop.all_noncit_adults * UNAUTH_SHARE["central"] / total_pop,
                 "unknown_or_extradited": 0.0}
    imp = []
    for k in ["us_citizen", "legal_alien", "illegal_alien", "unknown_or_extradited"]:
        s_n = (grp == k).mean()
        s_p = (gv.loss_positive & (grp == k)).sum() / gv.loss_positive.sum()
        s_l = gv.loss[grp == k].sum() / gv.loss.sum()
        imp.append({"group": k, "offenders": int((grp == k).sum()),
                    "offenders_loss_positive": int((gv.loss_positive & (grp == k)).sum()),
                    "loss_musd": round(gv.loss[grp == k].sum() / 1e6, 3),
                    "share_offenders": round(s_n, 4), "share_loss_positive_offenders": round(s_p, 4),
                    "share_loss": round(s_l, 4), "adult_pop_share": round(pop_share[k], 4),
                    "implied_bn_loss_share_low": round(s_l * GAO_FRAUD_BN[0], 1),
                    "implied_bn_loss_share_high": round(s_l * GAO_FRAUD_BN[1], 1),
                    "implied_bn_offender_share_low": round(s_p * GAO_FRAUD_BN[0], 1),
                    "implied_bn_offender_share_high": round(s_p * GAO_FRAUD_BN[1], 1)})
    pd.DataFrame(imp).to_csv(OUT / "implied_fraud_by_group.csv", index=False)

    # 8b. The same government-victim cases by Hispanic origin, and Mexican citizens: the closest
    #     USSC proxies for the Mexican-origin union (the file has no birthplace or ancestry).
    hisp_adults = pop.hisp_citizen_adults + pop.hisp_noncit_adults
    origin = []
    outside_sdfl = gv[gv.DISTRICT.ne("31")]  # 31 = Southern District of Florida (codebook A-3)
    for scope, base, label, mask, pop_share_k in (
            ("all_districts", gv, "hispanic", gv.hisp.eq("hispanic"), hisp_adults / total_pop),
            ("all_districts", gv, "non_hispanic", gv.hisp.eq("non_hispanic"), 1 - hisp_adults / total_pop),
            ("all_districts", gv, "hispanic_unknown", gv.hisp.eq("unknown"), None),
            ("all_districts", gv, "mexican_citizen_noncitizen",
             gv.CITWHERE.eq("49") & gv.status.isin(NONCIT), None),
            ("all_districts", gv, "southern_district_florida", gv.DISTRICT.eq("31"), None),
            ("excluding_southern_district_florida", outside_sdfl, "hispanic",
             outside_sdfl.hisp.eq("hispanic"), None)):
        origin.append({"scope": scope, "group": label, "offenders": int(mask.sum()),
                       "share_offenders": round(mask.mean(), 4),
                       "share_loss_positive_offenders": round((base.loss_positive & mask).sum()
                                                              / base.loss_positive.sum(), 4),
                       "share_loss": round(base.loss[mask].sum() / base.loss.sum(), 4),
                       "adult_pop_share": None if pop_share_k is None else round(pop_share_k, 4)})
    pd.DataFrame(origin).to_csv(OUT / "gov_victim_fraud_by_origin.csv", index=False)

    # 9. Denominators, share check, validation, manifest.
    acs.reset_index().to_csv(OUT / "denominators.csv", index=False)
    unauth_share_check(acs).to_csv(OUT / "unauth_share_check.csv", index=False)
    checks = {}
    for fy, want in SOURCEBOOK_T9.items():
        y = years[fy]
        known = y[y.status != "missing"]
        t9 = known[known.OFFGUIDE == "16"]
        got = {"records": len(y), "known": len(known), "fraud": len(t9),
               "citizen": int((t9.status == "us_citizen").sum()),
               "non": int((t9.status != "us_citizen").sum())}
        checks[str(fy)] = {k: {"got": got[k], "want": want[k], "pass": got[k] == want[k]} for k in want}
    coverage = {}
    for fy, g in years.items():
        f = g[g.fraud]
        coverage[str(fy)] = {"records": int(len(g)), "gdlinehi_2B1.1": int(len(f)),
                             "econ_classified": int(f.subtype.ne("unclassified").sum()),
                             "no_guideline": int(g.GDLINEHI.isna().sum()),
                             "offguide_16": int(g.OFFGUIDE.eq("16").sum()),
                             "offguide_16_not_2B1.1": int((g.OFFGUIDE.eq("16") & ~g.fraud).sum()),
                             "fraud_laundering_2S1": int(g.fraud_laundering.sum())}
    all_pass = all(c["pass"] for fy in checks.values() for c in fy.values())
    validation = {"sourcebook_table9": checks, "coverage": coverage, "all_pass": all_pass}
    (OUT / "validation.json").write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n")
    inputs = sorted([p for p in USSC.glob("*.zip")] + [USSC / CODEBOOKS[0]]
                    + [p for p in ACS.glob("B05003*_*.json")])
    manifest = {"script_sha256": sha256(Path(__file__)),
                "inputs": {str(p.relative_to(HERE)): {"bytes": p.stat().st_size,
                                                      "sha256": sha256(p)} for p in inputs}}
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    if not all_pass:
        raise SystemExit("[BLOCKED] Sourcebook check failed: " + json.dumps(checks))
    print("[ok] Sourcebook Table 9 reproduced for FY2019, FY2022, FY2024; outputs in",
          OUT.relative_to(HERE.parents[2]))


if __name__ == "__main__":
    main()
