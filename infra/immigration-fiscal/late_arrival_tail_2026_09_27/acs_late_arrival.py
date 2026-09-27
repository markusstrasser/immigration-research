"""Late-arrival tail, task 2: ACS 1-year PUMS 2019, 2021, 2022, 2023 via the Census API.

2020 1-year PUMS is not on the API (the /data/2020/acs/acs1/pums endpoint returns 404; the Census
Bureau released 2020 only as experimental-weight files), so the pool is four years.

Groups (all restricted to the person records the API returns for these predicates):
  mexico  foreign-born (NATIVITY=2) with POBP=303, all ages
  india   foreign-born (NATIVITY=2) with POBP=210, all ages
  white   NATIVITY=1, HISP=01, RAC1P=1, AGEP 65+ (US-born non-Hispanic white alone)
POBP=303/210 also returns natives born abroad to US-citizen parents (CIT=3); they are dropped so the
group matches B05006's foreign-born count (the gate) and the immigrant question.

Age at arrival = AGEP - (survey year - YOEP), floored at 0. Bands <50, 50-54, 55-59, 60-64, 65+.
Pooled estimates use PWGTP/4 over the pooled sample; SE = sqrt(4/80 * sum_r (theta_r - theta)^2)
with theta_r computed on PWGTPr/4 pooled (replicate r of each year pooled together).
Dollar amounts: SSP/SSIP * ADJINC (the API serves the factor, e.g. 1.010145; survey-year dollars), then CPI-U (BLS CUUR0000SA0, annual
mean of the 12 monthly values) to 2023 dollars.

Outputs: derived/late_arrival_65plus.csv, derived/acs_arrivals.csv, derived/acs_gate.csv,
derived/late_arrival_tenure.csv (years since arrival; earnings and employment at ages 50-79).
Raw API responses are cached under _cache/acs/ so reruns are offline.
"""
import csv
import json
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import acs_census as api  # noqa: E402

YEARS = [2019, 2021, 2022, 2023]
NREP = 80
DERIVED = HERE / "derived"
GROUP_PRED = {
    "mexico": "POBP=303",
    "india": "POBP=210",
    "white": "NATIVITY=1&HISP=01&RAC1P=1&AGEP=65:99",
}
# The API caps get= at 50 variables; predicate variables are appended to the response without
# counting. Two chunks joined on SERIALNO+SPORDER carry the 80 replicate weights.
BASE = ["SERIALNO", "SPORDER", "PWGTP", "AGEP", "YOEP", "CIT", "HINS3", "HINS4", "SSP", "SSIP",
        "ADJINC", "POVPIP", "RELSHIPP", "SEX", "SCHL", "NATIVITY"]
CHUNK_A = BASE + [f"PWGTP{i}" for i in range(1, 35)]
CHUNK_B = ["SERIALNO", "SPORDER"] + [f"PWGTP{i}" for i in range(35, NREP + 1)]
assert len(CHUNK_A) <= 50 and len(CHUNK_B) <= 50
# Earnings chunk (tenure follow-up): Mexico and India only, ages 50-79, joined 1:1 onto chunks A+B
# (which already carry ADJINC and all 80 replicate weights). Codes from each year's dictionary
# (identical 2019-2023): ESR 1,2 civilian employed, 4,5 armed forces employed, 3 unemployed,
# 6 not in labor force, 0 N/A (<16); PERNP -10000 = loss >= $10k (bottom code), -10001 N/A (<16).
CHUNK_E = ["SERIALNO", "SPORDER", "PERNP", "WAGP", "ESR", "WKHP"]
EARN_PRED = "AGEP=50:79"
EARN_GROUPS = ("mexico", "india")
YSA_BANDS = [("0-4", 0, 4), ("5-9", 5, 9), ("10-14", 10, 14), ("15-19", 15, 19), ("20plus", 20, 999)]
AGE_BANDS = [("50-54", 50, 54), ("55-59", 55, 59), ("60-64", 60, 64), ("65-69", 65, 69),
             ("70-74", 70, 74), ("75-79", 75, 79)]
# RELSHIPP codes from each year's dictionary (2019, 2021, 2022, 2023 identical):
# 29 "Father or mother", 31 "Parent-in-law" (of the reference person).
PARENT_CODES = (29, 31)
BANDS = [("lt50", 0, 49), ("50-54", 50, 54), ("55-59", 55, 59), ("60-64", 60, 64), ("65plus", 65, 200)]
B05006_LABEL = {"mexico": "Mexico", "india": "India"}


# National calls for large groups were reset by the server mid-transfer (2026-09-27: 19 of 24
# national chunks failed after six tries), so every call is partitioned by state (50 + DC).
STATES = [f"{i:02d}" for i in range(1, 57) if i not in (3, 7, 14, 43, 52)]
assert len(STATES) == 51


def fetch_chunk(year, group, name, cols, state):
    pred = GROUP_PRED[group] + (f"&{EARN_PRED}" if name == "E" else "")
    path = f"{year}/acs/acs1/pums?get={','.join(cols)}&{pred}&for=state:{state}"
    return api.get(path, f"pums/{year}_{group}_{name}_{state}.json")


def fetch_all(year, group, name, cols):
    rows = []
    for st in STATES:
        part = fetch_chunk(year, group, name, cols, st)
        if part:
            if rows:
                assert part[0] == rows[0], (year, group, name, st)
                rows.extend(part[1:])
            else:
                rows = list(part)
    return rows


def to_frame(rows):
    hdr = rows[0]
    first = {}
    for i, h in enumerate(hdr):
        first.setdefault(h, i)
    df = pd.DataFrame(rows[1:], columns=list(range(len(hdr))))
    df = df[[first[h] for h in first]]
    df.columns = list(first)
    return df


def load(year, group):
    a = to_frame(fetch_all(year, group, "A", CHUNK_A))
    b = to_frame(fetch_all(year, group, "B", CHUNK_B))
    for d in (a, b):
        d["key"] = d["SERIALNO"] + "_" + d["SPORDER"]
        assert d["key"].is_unique, (year, group)
    assert len(a) == len(b), (year, group, len(a), len(b))
    wb = [c for c in CHUNK_B if c.startswith("PWGTP")]
    df = a.merge(b[["key"] + wb], on="key", how="inner", validate="1:1")
    assert len(df) == len(a), (year, group)
    for c in df.columns:
        if c not in ("SERIALNO", "key"):
            df[c] = pd.to_numeric(df[c], errors="raise")
    # The API serves ADJINC as the factor itself (e.g. "1.010145"), not the file's 1010145 x 1e-6.
    assert df["ADJINC"].between(0.95, 1.10).all(), (year, group, df["ADJINC"].unique()[:5])
    return df


def load_earnings(year, group, df):
    """Join the ages 50-79 earnings chunk onto the (foreign-born) frame; rows outside 50-79 get NaN."""
    e = to_frame(fetch_all(year, group, "E", CHUNK_E))
    e["key"] = e["SERIALNO"] + "_" + e["SPORDER"]
    assert e["key"].is_unique, (year, group)
    for c in CHUNK_E[2:]:
        e[c] = pd.to_numeric(e[c], errors="raise")
    out = df.merge(e[["key"] + CHUNK_E[2:]], on="key", how="left", validate="1:1")
    in_age = out["AGEP"].between(50, 79)
    assert out.loc[in_age, "ESR"].notna().all(), (year, group, "earnings rows missing")
    # every earnings record is either in the frame or a dropped native (NATIVITY=1)
    assert int(in_age.sum()) <= len(e), (year, group)
    assert out.loc[in_age, "PERNP"].ge(-10000).all()
    return out


def cpi_factors():
    d = json.loads((api.CACHE / "bls_cpiu_CUUR0000SA0_2019_2023.json").read_text())
    assert d["status"] == "REQUEST_SUCCEEDED"
    vals = defaultdict(list)
    for r in d["Results"]["series"][0]["data"]:
        if r["period"].startswith("M") and r["period"] != "M13":
            vals[int(r["year"])].append(float(r["value"]))
    mean = {y: sum(v) / len(v) for y, v in vals.items() if len(v) == 12}
    return {y: mean[2023] / mean[y] for y in YEARS}


class Acc:
    """Accumulates weighted numerators and denominators (81 columns: full weight + 80 replicates)."""

    def __init__(self):
        self.num = defaultdict(lambda: np.zeros(NREP + 1))
        self.den = defaultdict(lambda: np.zeros(NREP + 1))
        self.n = defaultdict(int)

    def add(self, key, W, y, valid):
        vf = valid.astype(float)
        self.num[key] += (np.where(valid, y, 0.0)) @ W
        self.den[key] += vf @ W
        self.n[key] += int(valid.sum())


def se_of(theta):
    return float(np.sqrt(4.0 / NREP * np.sum((theta[1:] - theta[0]) ** 2)))


def arrival_age(df, year):
    return np.maximum(df["AGEP"].to_numpy() - (year - df["YOEP"].to_numpy()), 0)


def stats_65(df, year, cpi, foreign):
    """Indicator/value arrays and validity masks for the 65+ outcomes."""
    ssp = df["SSP"].to_numpy().astype(float)
    ssip = df["SSIP"].to_numpy().astype(float)
    adj = df["ADJINC"].to_numpy() * cpi[year]
    pov = df["POVPIP"].to_numpy()
    cit = df["CIT"].to_numpy()
    schl = df["SCHL"].to_numpy()
    rel = df["RELSHIPP"].to_numpy()
    true = np.ones(len(df), bool)
    out = {
        "medicaid": (df["HINS4"].to_numpy() == 1, true),
        "medicare": (df["HINS3"].to_numpy() == 1, true),
        "ssi_receipt": (ssip > 0, ssip >= 0),
        "ss_receipt": (ssp > 0, ssp >= 0),
        "mean_ssp_2023usd": (ssp * adj, ssp >= 0),
        "mean_ssip_2023usd": (ssip * adj, ssip >= 0),
        "mean_ssp_recipients_2023usd": (ssp * adj, ssp > 0),
        "mean_ssip_recipients_2023usd": (ssip * adj, ssip > 0),
        "naturalized": (cit == 4, true),
        "noncitizen": (cit == 5, true),
        "poverty_lt100": ((pov >= 0) & (pov < 100), pov >= 0),
        "parent_of_householder": (np.isin(rel, PARENT_CODES), true),
        "less_than_hs": ((schl >= 1) & (schl <= 15), schl >= 1),
        "mean_age": (df["AGEP"].to_numpy().astype(float), true),
    }
    if foreign:
        out["mean_years_since_arrival"] = ((year - df["YOEP"].to_numpy()).astype(float), true)
    return {k: (np.asarray(v, float), m) for k, (v, m) in out.items()}


def main():
    cpi = cpi_factors()
    # Fetch every raw response first (parallel; cached files make this a no-op on rerun).
    jobs = [(y, g, n, c, st) for y in YEARS for g in GROUP_PRED
            for n, c in (("A", CHUNK_A), ("B", CHUNK_B)) for st in STATES]
    jobs += [(y, g, "E", CHUNK_E, st) for y in YEARS for g in EARN_GROUPS for st in STATES]
    todo = [j for j in jobs if not (api.CACHE / f"pums/{j[0]}_{j[1]}_{j[2]}_{j[4]}.json").exists()]
    print(f"fetch: {len(jobs) - len(todo)}/{len(jobs)} cached, {len(todo)} to fetch", flush=True)
    failed = []

    def run(j):
        try:
            fetch_chunk(*j)
        except RuntimeError as e:
            failed.append(str(e))
            print(f"  ✗ {e}", flush=True)

    with ThreadPoolExecutor(max_workers=8) as ex:
        for i, _ in enumerate(ex.map(run, todo), 1):
            if i % 50 == 0 or i == len(todo):
                print(f"  [{i}/{len(todo)}] fetched", flush=True)
    if failed:
        raise SystemExit(f"[FAILED] {len(failed)} partitions; rerun to resume from the cache")
    for y in YEARS:
        api.get(f"{y}/acs/acs1/groups/B05006.json", f"b05006_groups_{y}.json")

    pooled = Acc()                      # pooled, weights /4
    yearly = {y: Acc() for y in YEARS}  # per-year, full weights
    arrivals = defaultdict(lambda: np.zeros(NREP + 1))
    arrivals_n = defaultdict(int)
    gate_rows, dropped = [], {}
    kept = {}  # (year, group) -> (frame with earnings, W) for the tenure tabulation

    for y in YEARS:
        for g in GROUP_PRED:
            df = load(y, g)
            if g in ("mexico", "india"):
                native = df["NATIVITY"].to_numpy() == 1
                dropped[(y, g)] = (int(native.sum()), float(df.loc[native, "PWGTP"].sum()))
                df = df[~native].reset_index(drop=True)
                assert (df["YOEP"] > 1900).all()
            W = df[["PWGTP"] + [f"PWGTP{i}" for i in range(1, NREP + 1)]].to_numpy(float)
            age = df["AGEP"].to_numpy()
            ones = np.ones(len(df))
            if g in ("mexico", "india"):
                aa = arrival_age(df, y)
                gate_rows.append((y, g, float(W[:, 0].sum()), len(df)))
                # arrivals by band, all current ages, per year (full weights)
                for band, lo, hi in BANDS + [("all", 0, 200)]:
                    m = (aa >= lo) & (aa <= hi)
                    arrivals[(g, y, "stock", band)] += W[m].sum(axis=0)
                    arrivals_n[(g, y, "stock", band)] += int(m.sum())
                recent = (y - df["YOEP"].to_numpy()) <= 1
                for band, m in (("lt50", aa < 50), ("50plus", aa >= 50), ("all", aa >= 0)):
                    arrivals[(g, y, "recent_le1", band)] += W[recent & m].sum(axis=0)
                    arrivals_n[(g, y, "recent_le1", band)] += int((recent & m).sum())
                kept[(y, g)] = (load_earnings(y, g, df), W)
                cells = [("all65", ones.astype(bool)), ("lt50", aa < 50), ("50plus", aa >= 50)]
                # the <50 band is the lt50 split cell; add only the four 50+ bands
                cells += [(b, (aa >= lo) & (aa <= hi)) for b, lo, hi in BANDS if b != "lt50"]
            else:
                cells = [("all65", ones.astype(bool))]
            old = age >= 65
            st = stats_65(df, y, cpi, foreign=g != "white")
            for cell, cm in cells:
                m = old & cm
                for acc, w in ((pooled, W / 4.0), (yearly[y], W)):
                    acc.add((g, cell, "pop"), w, ones, m)
                    for s, (v, valid) in st.items():
                        acc.add((g, cell, s), w, v, m & valid)
            print(f"{y} {g}: {len(df)} records, {int(old.sum())} aged 65+", flush=True)

    DERIVED.mkdir(exist_ok=True)
    gate_ok = True
    with open(DERIVED / "acs_gate.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["year", "group", "pums_weighted_foreign_born", "pums_records", "b05006_var",
                    "b05006_estimate", "b05006_moe", "pct_diff", "pass_within_1pct",
                    "dropped_native_records", "dropped_native_weighted"])
        for y, g, tot, n in gate_rows:
            meta = api.get(f"{y}/acs/acs1/groups/B05006.json", f"b05006_groups_{y}.json")["variables"]
            lab = B05006_LABEL[g]
            var = [k for k, v in meta.items()
                   if k.endswith("E") and v["label"].rstrip(":").split("!!")[-1] == lab]
            assert len(var) == 1, (y, g, var)
            var = var[0]
            moe = var[:-1] + "M"
            d = api.get(f"{y}/acs/acs1?get=NAME,{var},{moe}&for=us:1", f"b05006_{y}_{g}.json")
            est, m = float(d[1][1]), float(d[1][2])
            pct = 100.0 * (tot - est) / est
            ok = abs(pct) <= 1.0
            gate_ok &= ok
            dn, dw = dropped[(y, g)]
            w.writerow([y, g, f"{tot:.0f}", n, var, f"{est:.0f}", f"{m:.0f}", f"{pct:.3f}", int(ok),
                        dn, f"{dw:.0f}"])
            print(f"gate {y} {g}: PUMS {tot:,.0f} vs B05006 {var} {est:,.0f} ({pct:+.2f}%) "
                  f"{'PASS' if ok else 'FAIL'}", flush=True)
    if not gate_ok:
        print("[GATE FAIL] PUMS foreign-born total outside 1% of B05006; no other derived "
              "file written", flush=True)
        sys.exit(2)

    rows = []

    def emit(acc, g, cell, s, period):
        key = (g, cell, s)
        n = acc.n[key]
        if s == "pop":
            th = acc.den[key]
            est, se, dy = th[0], se_of(th), ""
        elif s == "share_of_group65":
            th = acc.den[(g, cell, "pop")] / acc.den[(g, "all65", "pop")]
            n = acc.n[(g, cell, "pop")]
            est, se, dy = th[0], se_of(th), ""
        else:
            th = acc.num[key] / acc.den[key] if acc.den[key][0] > 0 else np.full(NREP + 1, np.nan)
            est, se = th[0], se_of(th)
            dy = "2023" if "usd" in s else ""
        rows.append([g, cell, s, period, f"{est:.6f}", f"{se:.6f}", n, dy, int(n < 50)])

    stat_names = ["pop", "share_of_group65"] + sorted({k[2] for k in pooled.n if k[2] != "pop"})
    for g in GROUP_PRED:
        for cell in ["all65", "lt50", "50plus"] + [b for b, _, _ in BANDS if b != "lt50"]:
            if (g, cell, "pop") not in pooled.n:
                continue
            for s in stat_names:
                if s != "share_of_group65" and (g, cell, s) not in pooled.n:
                    continue
                emit(pooled, g, cell, s, "pooled_2019_2021_2022_2023")
    for g in ("mexico", "india"):
        for y in YEARS:
            for cell in ("lt50", "50plus"):
                for s in ("pop", "share_of_group65", "medicaid", "ssi_receipt", "ss_receipt"):
                    emit(yearly[y], g, cell, s, str(y))
    with open(DERIVED / "late_arrival_65plus.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["group", "arrival_cell", "stat", "period", "estimate", "se", "n_unweighted",
                    "dollar_year", "flag_n_lt_50"])
        w.writerows(rows)

    with open(DERIVED / "acs_arrivals.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["group", "measure", "arrival_age_band", "period", "weighted_count", "se",
                    "n_unweighted", "share_of_measure_total", "share_se"])
        for g in ("mexico", "india"):
            for measure, bands in (("stock", [b for b, _, _ in BANDS] + ["all"]),
                                   ("recent_le1", ["lt50", "50plus", "all"])):
                for band in bands:
                    for period in YEARS + ["pooled_mean"]:
                        if period == "pooled_mean":
                            th = sum(arrivals[(g, y, measure, band)] for y in YEARS) / len(YEARS)
                            tot = sum(arrivals[(g, y, measure, "all")] for y in YEARS) / len(YEARS)
                            n = sum(arrivals_n[(g, y, measure, band)] for y in YEARS)
                        else:
                            th = arrivals[(g, period, measure, band)]
                            tot = arrivals[(g, period, measure, "all")]
                            n = arrivals_n[(g, period, measure, band)]
                        sh = th / tot
                        w.writerow([g, measure, band, period, f"{th[0]:.1f}", f"{se_of(th):.1f}", n,
                                    f"{sh[0]:.6f}", f"{se_of(sh):.6f}"])

    tenure(kept, cpi)


def tenure(kept, cpi):
    """derived/late_arrival_tenure.csv: late arrivals by years since arrival, and earnings/employment
    at ages 50-79 by arrival <50 vs 50+. Pooled over the four years (weights and replicates / 4)."""
    acc = Acc()
    acc2 = Acc()  # follow-up cells, written after the original rows so those stay byte-identical
    six = ["medicaid", "medicare", "ssi_receipt", "ss_receipt", "mean_ssp_2023usd", "mean_ssip_2023usd"]
    for (y, g), (df, W) in kept.items():
        w = W / 4.0
        age = df["AGEP"].to_numpy()
        aa = arrival_age(df, y)
        ysa = y - df["YOEP"].to_numpy()
        ones = np.ones(len(df))
        st = stats_65(df, y, cpi, foreign=True)
        # (1) current age 65+, arrived 50+ / 55+, by years since arrival
        s1 = ["medicaid", "medicare", "ssi_receipt", "ss_receipt", "mean_ssp_2023usd",
              "mean_ssip_2023usd", "naturalized"]
        # (1b) arrived 50+, current age 55-64, by years since arrival
        s1b = ["medicaid", "ssi_receipt", "ss_receipt", "naturalized"]
        spec = [("arr50plus", aa >= 50, "65plus", age >= 65, s1),
                ("arr55plus", aa >= 55, "65plus", age >= 65, s1),
                ("arr50plus", aa >= 50, "55-64", (age >= 55) & (age <= 64), s1b)]
        for arr, am, agec, agem, stats in spec:
            for yb, lo, hi in YSA_BANDS + [("all", 0, 999)]:
                m = am & agem & (ysa >= lo) & (ysa <= hi)
                k = (g, arr, agec, yb)
                acc.add(k + ("pop",), w, ones, m)
                for s in stats:
                    v, valid = st[s]
                    acc.add(k + (s,), w, v, m & valid)
        # (1c) follow-up: age 55-64 arrived <50 and all arrivals; age 65+ all arrivals; and for
        # arrived 50+ at 55-64 the three stats (1b) lacked, in every tenure band
        a5564 = (age >= 55) & (age <= 64)
        spec2 = [("arr_lt50", aa < 50, "55-64", a5564, [("all", 0, 999)], six),
                 ("arr50plus", aa >= 50, "55-64", a5564, YSA_BANDS + [("all", 0, 999)],
                  ["medicare", "mean_ssp_2023usd", "mean_ssip_2023usd"]),
                 ("all", aa >= 0, "55-64", a5564, [("all", 0, 999)], six),
                 ("all", aa >= 0, "65plus", age >= 65, [("all", 0, 999)], six)]
        for arr, am, agec, agem, ybands, stats in spec2:
            for yb, lo, hi in ybands:
                m = am & agem & (ysa >= lo) & (ysa <= hi)
                k = (g, arr, agec, yb)
                if arr != "arr50plus":
                    acc2.add(k + ("pop",), w, ones, m)
                for s in stats:
                    v, valid = st[s]
                    acc2.add(k + (s,), w, v, m & valid)
        # (2) earnings and employment, ages 50-79 by band x arrival
        adj = df["ADJINC"].to_numpy() * cpi[y]
        esr = df["ESR"].to_numpy()
        pernp = df["PERNP"].to_numpy().astype(float) * adj
        wagp = df["WAGP"].to_numpy().astype(float) * adj
        employed = np.isin(esr, (1, 2, 4, 5)).astype(float)
        for arr, am in (("arr_lt50", aa < 50), ("arr50plus", aa >= 50)):
            for ab, lo, hi in AGE_BANDS:
                m = am & (age >= lo) & (age <= hi)
                k = (g, arr, ab, "all")
                acc.add(k + ("pop",), w, ones, m)
                acc.add(k + ("employment_rate",), w, employed, m)
                acc.add(k + ("mean_pernp_2023usd",), w, np.nan_to_num(pernp), m)
                acc.add(k + ("mean_wagp_2023usd",), w, np.nan_to_num(wagp), m)

    rows = []
    period = "pooled_2019_2021_2022_2023"

    def put(key, th, n, stat_dollar):
        g, arr, agec, yb, s = key
        dy = "2023" if stat_dollar else ""
        rows.append([g, arr, agec, yb, s, period, f"{th[0]:.6f}", f"{se_of(th):.6f}", n, dy,
                     int(n < 50)])

    for key in sorted(acc.n, key=lambda k: (k[0], k[1], k[2], k[3], k[4] != "pop", k[4])):
        n = acc.n[key]
        if key[4] == "pop":
            th = acc.den[key]
        elif acc.den[key][0] > 0:
            th = acc.num[key] / acc.den[key]
        else:
            th = np.full(NREP + 1, np.nan)
        put(key, th, n, "usd" in key[4])
    # replicated ratio of mean PERNP, arrived 50+ over arrived <50, same group and age band
    for g in EARN_GROUPS:
        for ab, _, _ in AGE_BANDS:
            a = (g, "arr50plus", ab, "all", "mean_pernp_2023usd")
            b = (g, "arr_lt50", ab, "all", "mean_pernp_2023usd")
            th = (acc.num[a] / acc.den[a]) / (acc.num[b] / acc.den[b])
            put((g, "arr50plus_over_arr_lt50", ab, "all", "ratio_mean_pernp"), th,
                min(acc.n[a], acc.n[b]), False)
    for key in acc2.n:  # insertion order: group-year loop order, then spec2 order
        n = acc2.n[key]
        if key[4] == "pop":
            th = acc2.den[key]
        elif acc2.den[key][0] > 0:
            th = acc2.num[key] / acc2.den[key]
        else:
            th = np.full(NREP + 1, np.nan)
        put(key, th, n, "usd" in key[4])
    with open(DERIVED / "late_arrival_tenure.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["group", "arrival", "current_age", "years_since_arrival", "stat", "period",
                    "estimate", "se", "n_unweighted", "dollar_year", "flag_n_lt_50"])
        w.writerows(rows)


if __name__ == "__main__":
    main()
