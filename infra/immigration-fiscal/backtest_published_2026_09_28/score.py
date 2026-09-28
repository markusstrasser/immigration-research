"""Phase 2 of the pre-registered back-test: score the frozen predictions against the published figures.

The predictions and tolerances were frozen in commit 0f9eea7; PREDICTIONS.md states them in words. This script
refuses to run unless derived/predictions.csv and derived/tolerances.json are identical to that commit, and it
never writes them. Every source is read from the lane's _cache/ (or the repository's sources/ tree) and checked
against its pinned sha256. derived/sources.json lists each source with its URL and access date, and reads/ quotes
the cells used.

Checks:
  1. NAE 2021, a shared-method comparison. Three items can yield a finding: income per Mexican undocumented
     immigrant (the report states no household count), the payroll share and the state distribution. The tax
     ratios are reported against the directions their conventions predict.
  2. NAS 2017 Table 8-1: a disclosed comparison, not a pre-registered test, because its tolerance was written
     down after the run.
  3. CMS HCRIS Worksheet S-10 line 30 by state: the year rule, the cleaning, the level test, the slope test with
     KFF's expansion dates, and the national total.
Post-hoc material goes to derived/notes.csv, labelled, beside the frozen verdicts; it never replaces one.

Outputs: derived/scores.csv, derived/notes.csv, derived/hcris_s10_states.csv, derived/hcris_fits.csv,
derived/nae_targets.csv, derived/sources.json.
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/backtest_published_2026_09_28/score.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import html  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "derived"
CACHE = HERE / "_cache"
sys.path.insert(0, str(HERE))
import predict as P  # noqa: E402  read-only: the lane's frozen builders (state codes)

FREEZE = "0f9eea7"
FROZEN = [OUT / "predictions.csv", OUT / "tolerances.json"]
ACCESSED = "2026-09-28"
Z95 = 1.959963984540054
PANEL = Path("/Users/alien/research-data/immigration-fiscal/derived/immigration_microdata.duckdb")
CMS = "https://data.cms.gov/sites/default/files/"
SOURCES = {
    "nae_2021": dict(
        path=CACHE / "aic/wb_nae_undoc_by_country_2021.html",
        sha256="ff404e07f325526c92b24411ff64e6416ebb2061de179921ee95e255e428b14a",
        url="https://web.archive.org/web/20211227214554id_/https://research.newamericaneconomy.org/report/"
            "contributions-of-undocumented-immigrants-by-country/",
        title="New American Economy, Examining the Economic Contributions of Undocumented Immigrants by Country "
              "of Origin (8 March 2021), Tables 4 and 5"),
    "nas_2017": dict(
        path=ROOT / "sources/immigration-fiscal/data/external/nas_2016/23550.pdf",
        sha256="c6fffc8f764e257b6a19794171e61e6b1bfc7e29f36187db0aaef532b475d68f",
        url="https://doi.org/10.17226/23550",
        title="National Academies, The Economic and Fiscal Consequences of Immigration (2017), Table 8-1, "
              "printed p. 389 (PDF page 414)"),
    **{f"hcris_{y}": dict(path=CACHE / f"hcris/CostReport_{y}_Final.csv", sha256=h, url=CMS + u,
                          title=f"CMS Hospital Provider Cost Report, {y} (data.cms.gov)")
       for y, h, u in [
           (2020, "d485aad82c62cd391118045f8c45c5ff18af0fcb315ef3935803343f1b88fb58",
            "2025-11/bd432d70-3689-4e8e-a8a5-5e7bf5232cb6/CostReport_2020_Final.csv"),
           (2021, "95c97a48cdd3cb52ed27c4f9e988c0c28e8f8a0796cf42588ead67d0e367c3ed",
            "2025-11/7e94fd9d-9ef2-4275-b993-299e30f5b371/CostReport_2021_Final.csv"),
           (2022, "a661e206201a405f57548f6705e66269f740e6694540e9645529f2591d839b89",
            "2025-11/c298e529-8bee-401a-bbd8-a38e74e19ab2/CostReport_2022_Final.csv"),
           (2023, "614f3d94dfeb84092ca775f90913ab4f843233a4fa90c3df3013efeb5221a757",
            "2026-01/3c39f483-c7e0-4025-8396-4df76942e10f/CostReport_2023_Final.csv")]},
    "hcris_dictionary": dict(
        path=CACHE / "hcris/dictionary_update_2024-03.pdf",
        sha256="40342bb506d4c39ad6a3306d188f414e97e683c8c7241aa5e0975bdc59c87b81",
        url=CMS + "2024-03/9756088d-5280-4090-80b9-449d31ef25a3/Cost%20Report%20Data%20Dictionary%20Update.pdf",
        title="CMS, Hospital Provider Cost Report Data Dictionary (update, March 2024)"),
    "prm2_ch40": dict(
        path=CACHE / "hcris/prm2_ch40_r18.pdf",
        sha256="bcd279d6c175a9ee26dee9648725c3b8ffdba823bdf0f03cb5ec9e76e449842f",
        url="https://www.cms.gov/files/document/r18p240ipdf.pdf",
        title="CMS, Provider Reimbursement Manual Part 2, chapter 40, Transmittal 18 (12-22), section 4012"),
    "s10_qa": dict(
        path=CACHE / "hcris/s10_ucc_qandas.pdf",
        sha256="fbd0127a92aaeec8cc7cc2fef346fb5e6e3e6fc504284d44525306b009ee9d35",
        url="https://www.cms.gov/medicare/medicare-fee-for-service-payment/acuteinpatientpps/downloads/"
            "worksheet-s-10-ucc-qandas.pdf",
        title="CMS, Worksheet S-10 questions and answers following the 2018 IPPS final rule"),
    "kff_dates": dict(
        path=CACHE / "kff/dw_ZJUAA_5_dataset.csv",
        sha256="0ac75d1cbb38913b3ff6648086d1ef2d84b1428963d0b788f758a1474a0f90b0",
        url="https://datawrapper.dwcdn.net/ZJUAA/5/dataset.csv",
        title="KFF, Status of State Medicaid Expansion Decisions, map data (Datawrapper ZJUAA v5)"),
    "kff_page": dict(
        path=CACHE / "kff/status_of_expansion.html",
        sha256="31fe12f4b5f180029ad7bb1c1e407afe16efcc3d2f854972c419b9cbdd3d3690",
        url="https://www.kff.org/affordable-care-act/issue-brief/status-of-state-medicaid-expansion-decisions/",
        title="KFF, Status of State Medicaid Expansion Decisions (published 21 August 2026), embedding ZJUAA"),
    **{f"acs_b06011_{y}": dict(path=CACHE / f"census/B06011_us_{y}.json", sha256=h,
                               url=f"https://api.census.gov/data/{y}/acs/acs1?get=NAME,B06011_001E,B06011_004E,"
                                   "B06011_005E&for=us:1 (key omitted)",
                               title=f"ACS {y} 1-year, B06011 median income by place of birth, United States")
       for y, h in [(2013, "9253ed8abef9d85754e698b155288cb7f3d3e7750ca9bf5bcc466c393debf97f"),
                    (2024, "8168defb53ce6843ac1ee09fd8892e84930f82f836f0378693638a4f2567b381")]},
}
# Census Bureau regions, for one post-hoc robustness fit only.
REGIONS = {"Northeast": "CT ME MA NH RI VT NJ NY PA", "Midwest": "IL IN MI OH WI IA KS MN MO NE ND SD",
           "South": "DE DC FL GA MD NC SC VA WV AL KY MS TN AR LA OK TX", "West": "AZ CO ID MT NV NM UT WY AK CA HI OR WA"}
NAE_STATES = {"California": "CA", "Texas": "TX", "Illinois": "IL", "Arizona": "AZ", "Georgia": "GA",
              "North Carolina": "NC", "Washington": "WA", "Florida": "FL", "New York": "NY", "Nevada": "NV"}
NAE_COLUMNS = ["household_income", "federal_income_taxes", "state_local_taxes", "spending_power",
               "social_security", "medicare"]


def frozen_guard():
    for path in FROZEN:
        rel = str(path.relative_to(ROOT))
        in_commit = subprocess.run(["git", "cat-file", "-e", f"{FREEZE}:{rel}"], cwd=ROOT).returncode == 0
        same = subprocess.run(["git", "diff", "--quiet", FREEZE, "--", rel], cwd=ROOT).returncode == 0
        if not (in_commit and same):
            raise SystemExit(f"[BLOCKED] {rel} differs from the freeze commit {FREEZE}; scoring refused")
    print(f"  ✓ predictions.csv and tolerances.json match the freeze commit {FREEZE}")


def check_sources():
    out = {}
    for name, s in SOURCES.items():
        if not s["path"].exists():
            raise SystemExit(f"[BLOCKED] missing source {name}: {s['path']}")
        got = P.sha(s["path"])
        if got != s["sha256"]:
            raise SystemExit(f"[BLOCKED] {name} changed: sha256 {got} != pinned {s['sha256']}")
        path = s["path"].relative_to(ROOT) if s["path"].is_relative_to(ROOT) else s["path"]
        out[name] = dict(title=s["title"], url=s["url"], path=str(path), sha256=got, accessed=ACCESSED)
    print(f"  ✓ {len(out)} sources match their pinned sha256")
    return out


def tvd(a, b):
    return 0.5 * float(np.abs(np.asarray(a, float) - np.asarray(b, float)).sum())


# ------------------------------------------------------------------------------------------------------
# Check 1: NAE 2021
# ------------------------------------------------------------------------------------------------------
def nae_targets():
    raw = SOURCES["nae_2021"]["path"].read_text(encoding="utf-8", errors="replace")
    body = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    text = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", body)).split())
    t4 = text[text.index("Table 4: Economic Contributions of Mexican Undocumented Immigrants by State, 2019"):
              text.index("Table 5:")]
    row = re.compile(r"(United States|" + "|".join(NAE_STATES) + r") " + " ".join([r"\$([\d,]+)"] * 6))
    rows = {m.group(1): [float(v.replace(",", "")) for v in m.groups()[1:]] for m in row.finditer(t4)}
    if set(rows) != {*NAE_STATES, "United States"}:
        raise SystemExit(f"[BLOCKED] NAE Table 4 rows parsed: {sorted(rows)}")
    t5 = re.search(r"Mexico " + " ".join([r"\$([\d,]+)"] * 4), text[text.index("Table 5:"):])
    if [float(v.replace(",", "")) for v in t5.groups()] != rows["United States"][:4]:
        raise SystemExit("[BLOCKED] NAE Table 5's Mexico row differs from Table 4's United States row")
    count = re.search(r"we find that there were more than ([\d.]+) million immigrants from Mexico who lack legal "
                      r"status in 2019", text)
    share = re.search(r"they make up more than ([\d.]+) percent of the ([\d.]+) million undocumented", text)
    household_count = re.search(r"\d[\d.,]* (million )?(Mexican )?(undocumented )?(households|household heads)", text)
    for name, v in rows.items():
        if abs(v[0] - v[1] - v[2] - v[3]) > 1.5:
            raise SystemExit(f"[BLOCKED] NAE spending-power identity fails for {name}")
    targets = pd.DataFrame([dict(row=name, **dict(zip(NAE_COLUMNS, v))) for name, v in rows.items()])
    return targets, dict(count_m=float(count.group(1)), share_pct=float(share.group(1)),
                         all_undocumented_m=float(share.group(2)), household_count_stated=household_count is not None)


def score_check1(pred, tol, targets, meta, scores, notes):
    t = tol["check1"]
    us = targets.set_index("row").loc["United States"]
    hi = us.household_income
    label = "shared-method comparison"

    def acc(item, construction="account", allocation=None):
        q = pred[(pred.check == 1) & (pred.item == item) & (pred.construction == construction)]
        if allocation is not None:
            q = q[q.allocation == allocation]
        return q.value.to_numpy(float)

    # Income per household: no household count is stated, so per Mexican undocumented immigrant.
    if meta["household_count_stated"]:
        raise SystemExit("[BLOCKED] NAE states a household count; score per household as declared")
    per_person = hi * 1e6 / (meta["count_m"] * 1e6)
    band = t["income_per_household"]["per_unauthorized_person"]
    central = acc("income_per_unauthorized_person_2019", "account_bridged_central")[0]
    low, high = (acc("income_per_unauthorized_person_2019", f"account_bridged_{k}")[0] for k in ("low", "high"))
    inside = band["low"] <= per_person <= band["high"]
    scores.append(dict(check=1, item="income_per_unauthorized_person_2019", label=label, target=per_person,
                       prediction=central, band_low=band["low"], band_high=band["high"],
                       verdict="no finding" if inside else "finding", gap=per_person / central - 1,
                       explanation=f"NAE ${hi:,.0f}M over its 'more than {meta['count_m']} million'; the account's "
                                   f"${acc('income_per_unauthorized_person')[0]:,.0f} in 2024 x the central bridge. "
                                   f"NAE is {per_person / low:.3f} x the bridge's low end (ACS/CPS 0.90, the group's "
                                   f"wages 5% above the AWI's growth; high end ${high:,.0f}), so the declared year and "
                                   f"survey gap covers it"))
    # 'More than 4.2 million': 40.8% of 10.3 million bounds the rounding of NAE's count.
    upper_count = max(meta["share_pct"] / 100 * meta["all_undocumented_m"], meta["count_m"])
    notes.append(dict(check=1, item="income_per_unauthorized_person_2019", kind="rounding",
                      value=hi / upper_count,
                      note=f"NAE's count, {meta['share_pct']}% of {meta['all_undocumented_m']} million = "
                           f"{upper_count:.3f} million, gives ${hi / upper_count:,.0f} per person; the verdict does "
                           "not change"))
    # Payroll share against the statutory rule on the frame, not halved and halved.
    pay = (us.social_security + us.medicare) / hi
    p = t["payroll_share"]
    in_stat = p["band_statutory"][0] <= pay <= p["band_statutory"][1]
    in_half = p["band_halved"][0] <= pay <= p["band_halved"][1]
    scores.append(dict(check=1, item="payroll_share", label=label, target=pay, prediction=p["S"],
                       band_low=p["band_statutory"][0], band_high=p["band_statutory"][1],
                       verdict="no finding" if (in_stat or in_half) else "finding", gap=pay / p["S"] - 1,
                       explanation=("inside the statutory band: NAE did not halve payroll" if in_stat else
                                    "inside the halved band" if in_half else "outside both declared conventions")))
    mc_base = us.medicare / 0.029 / hi
    notes.append(dict(check=1, item="payroll_share", kind="post-hoc explanation", value=mc_base,
                      note="NAE's Medicare column at 2.9% implies earnings of this multiple of its household "
                           "income; above 1, the payroll base must include Mexican undocumented earners outside the "
                           "counted households (reads Q1: 'all individual wage earners'; 'made by or on behalf of "
                           "employers of Mexican undocumented immigrants'). The frame's members earn 0.949 of "
                           "their household income"))
    notes.append(dict(check=1, item="payroll_share", kind="context", value=pay / acc("payroll_over_income").mean(),
                      note="NAE's statutory payroll over the account's own on-books payroll share (0.087 / 0.089): "
                           "the account credits the group with this much less payroll by design (audit row 2)"))
    # State distribution: NAE's listed states plus one rest cell.
    listed = list(NAE_STATES.values())
    nae_share = np.array([targets.set_index("row").loc[n].household_income for n in NAE_STATES]) / hi
    a = np.array([acc(f"income_share_{s}")[0] for s in listed])
    b = np.array([acc(f"income_share_{s}", "baseline_mexico_born_population")[0] for s in listed])
    d_acc = tvd(np.append(nae_share, 1 - nae_share.sum()), np.append(a, 1 - a.sum()))
    d_base = tvd(np.append(nae_share, 1 - nae_share.sum()), np.append(b, 1 - b.sum()))
    rule = t["state_shares"]
    verdict = ("no finding" if d_acc <= rule["agree_max"] and d_acc < d_base
               else "finding" if d_acc > rule["finding_min"] or d_acc >= d_base else "partial")
    worst = sorted(zip(listed, nae_share - a), key=lambda x: -abs(x[1]))[:3]
    scores.append(dict(check=1, item="state_shares_tvd", label=label, target=d_acc, prediction=np.nan,
                       band_low=0.0, band_high=rule["agree_max"], verdict=verdict, gap=d_acc - d_base,
                       explanation=f"D = {d_acc:.3f} against the baseline's {d_base:.3f}; largest gaps (NAE - account): "
                                   + ", ".join(f"{s} {g:+.3f}" for s, g in worst)))
    # Convention-driven ratios: a finding only if the gap runs against the expected direction beyond the bound.
    conv = t["convention_ratios"]
    for item, target in (("federal_A_cbo_scope_over_income", us.federal_income_taxes / hi),
                         ("state_local_over_income", us.state_local_taxes / hi),
                         ("spending_power_A_over_income", us.spending_power / hi),
                         ("federal_B_income_tax_over_income", us.federal_income_taxes / hi)):
        c = conv[item]
        v = acc(item)
        if c.get("finding_if_above") is not None:
            verdict, bound = ("finding" if target > c["finding_if_above"] else "no finding"), c["finding_if_above"]
        elif c.get("finding_if_below") is not None:
            verdict, bound = ("finding" if target < c["finding_if_below"] else "no finding"), c["finding_if_below"]
        else:
            verdict, bound = "reported only", np.nan
        direction = "lower" if target < v.min() else "higher" if target > v.max() else "inside"
        scores.append(dict(check=1, item=item, label=label + ", convention-driven", target=target,
                           prediction=v.mean(), band_low=bound, band_high=bound, verdict=verdict,
                           gap=target - v.mean(),
                           explanation=f"NAE {direction} than the account; expected {c['expected']}"))
    notes.append(dict(check=1, item="federal_income_taxes", kind="post-hoc explanation",
                      value=us.federal_income_taxes / hi,
                      note="NAE's federal column is 0.059 of household income: about half of CBO's all-federal "
                           "rate for low-to-middle quintiles (reading A, halved) and far above CBO's individual "
                           "income-tax rates there (reading B), so reading A fits [INFERENCE]"))


# ------------------------------------------------------------------------------------------------------
# Check 2: NAS 2017 Table 8-1
# ------------------------------------------------------------------------------------------------------
def nas_table():
    txt = subprocess.run(["pdftotext", "-layout", "-f", "414", "-l", "414", str(SOURCES["nas_2017"]["path"]), "-"],
                         capture_output=True, text=True, check=True).stdout
    pops = [float(x) for x in re.findall(r"\(population: ([\d.]+) million\)", txt)]
    totals = re.findall(r"Total\s+" + r"\s+".join([r"([\d,]+)\s+([\d,]+)\s+([\d.]+)"] * 3), txt)
    if len(pops) != 6 or len(totals) != 2:
        raise SystemExit(f"[BLOCKED] NAS Table 8-1 parse: {len(pops)} populations, {len(totals)} total rows")
    out = {}
    for i, year in enumerate((1994, 2013)):
        n = np.array(pops[3 * i:3 * i + 3])
        vals = np.array([float(v.replace(",", "")) for v in totals[i]]).reshape(3, 3)
        outlays, receipts = vals[:, 0], vals[:, 1]
        out[year] = dict(population_m=n.tolist(), receipts=receipts.tolist(), outlays=outlays.tolist(),
                         receipts_ratio=float(receipts[0] / (n @ receipts / n.sum())),
                         outlays_ratio=float(outlays[0] / (n @ outlays / n.sum())))
    return out


def score_check2(pred, tol, nas, scores, notes):
    label = "disclosed comparison, not a pre-registered test"
    for m in ("receipts_ratio", "outlays_ratio"):
        t = tol["check2"][f"nas_first_generation_{m}"]
        v = pred[(pred.check == 2) & (pred.item == f"nas_first_generation_{m}")
                 & (pred.construction == "A5_schools_flat")].value.to_numpy(float)
        target = nas[2013][m]
        hit = t["low"] <= target <= t["high"]
        if hit != (t["low"] <= t["nas_2013"] <= t["high"]):
            raise SystemExit("[BLOCKED] the rounded and unrounded NAS values score differently")
        scores.append(dict(check=2, item=f"nas_first_generation_{m}", label=label, target=target,
                           prediction=v.mean(), band_low=t["low"], band_high=t["high"],
                           verdict="hit" if hit else "miss", gap=v.mean() - target,
                           explanation=f"account {v.min():.3f}-{v.max():.3f} against NAS 2013 {target:.3f} "
                                       f"(1994: {nas[1994][m]:.3f})"))
    notes.append(dict(check=2, item="nas_first_generation_receipts_ratio", kind="post-hoc explanation",
                      value=nas[2013]["receipts_ratio"] - nas[1994]["receipts_ratio"],
                      note="NAS's own first-generation receipts ratio barely moved from 1994 to 2013, so the "
                           "report's trend cannot carry the gap; what changed after 2013 is the foreign-born's "
                           "relative income (next notes)"))
    med = {}
    for y in (2013, 2024):
        rows = json.loads(SOURCES[f"acs_b06011_{y}"]["path"].read_text())
        rec = dict(zip(rows[0], rows[1]))
        med[y] = float(rec["B06011_005E"]) / float(rec["B06011_001E"])
    notes.append(dict(check=2, item="nas_first_generation_receipts_ratio", kind="post-hoc explanation",
                      value=med[2024] / med[2013],
                      note=f"ACS median income, foreign-born over all: {med[2013]:.4f} in 2013, {med[2024]:.4f} in "
                           f"2024 (B06011); NAS's 2013 receipts ratio scaled by this change is "
                           f"{nas[2013]['receipts_ratio'] * med[2024] / med[2013]:.3f} [INFERENCE: taxes move at "
                           "least in proportion to income]"))
    if PANEL.exists():
        import duckdb
        con = duckdb.connect(str(PANEL), read_only=True)
        r = dict(con.execute(
            "select YEAR, sum(PERWT * inc * fb) / sum(PERWT * fb) / (sum(PERWT * inc) / sum(PERWT)) from ("
            " select YEAR, PERWT, case when INCTOT in (9999999, 9999998) then 0 else INCTOT end as inc,"
            " (BPL >= 150 and coalesce(CITIZEN, 0) <> 1)::int as fb from ipums_usa_borjas_panel"
            " where YEAR in (2010, 2023) and AGE >= 18) group by 1 order by 1").fetchall())
        notes.append(dict(check=2, item="nas_first_generation_receipts_ratio", kind="post-hoc explanation",
                          value=r[2023] / r[2010],
                          note=f"ACS mean total income of foreign-born adults over all adults: {r[2010]:.4f} in 2010, "
                               f"{r[2023]:.4f} in 2023 (local IPUMS panel, households and group quarters)"))
    else:
        print(f"[DEGRADED] {PANEL} missing: the ACS 2010/2023 mean-income note is skipped")
    notes.append(dict(check=2, item="nas_first_generation_outlays_ratio", kind="context",
                      value=nas[1994]["outlays_ratio"],
                      note="NAS's 1994 outlays ratio; 2013 is 0.902"))


# ------------------------------------------------------------------------------------------------------
# Check 3: HCRIS Worksheet S-10
# ------------------------------------------------------------------------------------------------------
def kff_not_expanded(year):
    """States that had not implemented expansion by 1 July of the year, from KFF's dates."""
    d = pd.read_csv(SOURCES["kff_dates"]["path"], dtype=str).fillna("")
    out = set()
    for _, r in d.iterrows():
        code = r["State Abbrev."].strip().rstrip("*")
        if r["Expansion Status"].strip() == "Not adopted":
            out.add(code)
            continue
        dates = re.findall(r"(\d{1,2})/(\d{1,2})/(\d{4})", r["Expansion Implementation Date"])
        m, day, y = (int(x) for x in dates[0])  # the first date: implementation or processing start
        if (y, m, day) > (year, 7, 1):
            out.add(code)
    return out


def wls_hc1(y, X, w):
    sw = np.sqrt(w)
    Xs, ys = X * sw[:, None], y * sw
    xtx_inv = np.linalg.inv(Xs.T @ Xs)
    beta = xtx_inv @ Xs.T @ ys
    e = ys - Xs @ beta
    n, k = Xs.shape
    meat = (Xs * e[:, None] ** 2).T @ Xs
    cov = xtx_inv @ meat @ xtx_inv * n / (n - k)
    resid_sd = float(np.sqrt(np.sum(w * (y - X @ beta) ** 2) / np.sum(w) * n / (n - k)))
    return beta, np.sqrt(np.diag(cov)), resid_sd


def slope_verdict(lo, hi, alt):
    has0, has_alt = lo <= 0 <= hi, lo <= alt <= hi
    return ("no power" if has0 and has_alt else "consistent with the adopted key" if has0
            else "favors r = 0.7" if has_alt else "miss")


def hcris(pred, tol, scores, notes):
    counts = {}
    for y in (2020, 2021, 2022, 2023):  # the year rule reads the counts before any state total is formed
        counts[y] = int(pd.read_csv(SOURCES[f"hcris_{y}"]["path"], usecols=["rpt_rec_num"], dtype=str)
                        .rpt_rec_num.nunique())
    year = next(y for y in sorted(counts, reverse=True) if y - 1 in counts and counts[y] >= 0.95 * counts[y - 1])
    print(f"[check 3] report counts {counts}; year rule selects {year}", flush=True)
    cols = ["rpt_rec_num", "Provider CCN", "State Code", "Fiscal Year Begin Date", "Cost of Uncompensated Care",
            "Total Costs"]
    d = pd.read_csv(SOURCES[f"hcris_{year}"]["path"], usecols=cols, dtype={"Provider CCN": str, "rpt_rec_num": str})
    begin = pd.to_datetime(d["Fiscal Year Begin Date"])
    states = set(P.STATES.values())
    d = d[d["State Code"].isin(states)]
    line30, costs = d["Cost of Uncompensated Care"], d["Total Costs"]
    negative = line30 < 0
    above = line30.notna() & costs.notna() & (line30 > costs)
    kept = d[line30.notna() & ~negative & ~above]
    by_provider = kept.groupby(["Provider CCN", "State Code"], as_index=False)["Cost of Uncompensated Care"].sum()
    tally = dict(year=year, begin_min=str(begin.min().date()), begin_max=str(begin.max().date()),
                 reports_in_file=int(len(begin)), reports_50_states_dc=int(len(d)),
                 reports_with_line30=int(line30.notna().sum()), dropped_negative=int(negative.sum()),
                 dropped_above_total_costs=int(above.sum()), reports_kept=int(len(kept)),
                 providers_kept=int(len(by_provider)), providers_in_two_states=int(
                     by_provider["Provider CCN"].duplicated().sum()),
                 missing_total_costs=int(costs.isna().sum()), counts_by_year=counts)
    total = by_provider.groupby("State Code")["Cost of Uncompensated Care"].sum()
    st = pd.read_csv(OUT / "hcris_states.csv")
    st["line30_bn"] = st.state.map(total).fillna(0.0).to_numpy() / 1e9
    st["reports_kept"] = st.state.map(kept.groupby("State Code").size()).fillna(0).astype(int)
    st["s10_share"] = st.line30_bn / st.line30_bn.sum()
    kff = kff_not_expanded(year)
    st[f"not_expanded_{year}_kff"] = st.state.isin(kff).astype(int)
    frozen_list = set(st.loc[st[f"not_expanded_{year}"] == 1, "state"])
    if frozen_list != kff:
        notes.append(dict(check=3, item="expansion", kind="KFF governs", value=len(kff ^ frozen_list),
                          note=f"KFF differs from the frozen list: {sorted(kff ^ frozen_list)}"))
    print(f"  KFF not expanded by 1 July {year}: {sorted(kff)} (frozen list {'matches' if frozen_list == kff else 'differs'})")
    national = st.line30_bn.sum()
    # Level test.
    lvl = tol["check3"]["level"]
    tv = {k: tvd(st.s10_share, st[k]) for k in ("account_r1", "account_r07", "baseline_uninsured_count",
                                                 "baseline_population", "account_r1_row4",
                                                 f"acs{year}_uninsured_share")}
    level = ("hit" if tv["account_r1"] <= lvl["hit_max"] and tv["account_r1"] <= lvl["beat_population_factor"]
             * tv["baseline_population"] else "miss" if tv["account_r1"] > lvl["miss_min"]
             or tv["account_r1"] >= tv["baseline_population"] else "partial")
    scores.append(dict(check=3, item="level_tvd", label="pre-registered", target=tv["account_r1"],
                       prediction=np.nan, band_low=0.0, band_high=lvl["hit_max"], verdict=level,
                       gap=tv["account_r1"] - tv["baseline_population"],
                       explanation="TVD against the S-10 shares: " + ", ".join(f"{k} {v:.3f}" for k, v in tv.items())))
    # Slope test: the frozen specification first, then the variants PREDICTIONS.md lists, then post-hoc checks.
    sl = tol["check3"]["slope"]
    expansion = st[f"not_expanded_{year}_kff"].to_numpy(float)
    regions = np.column_stack([st.state.isin(REGIONS[r].split()).to_numpy(float) for r in ("Midwest", "South", "West")])
    fits = []
    specs = [("primary: weighted, expansion", "account_r1", "group_share_of_uninsured", True, [expansion], False),
             ("weighted, no expansion", "account_r1", "group_share_of_uninsured", True, [], False),
             ("unweighted, expansion", "account_r1", "group_share_of_uninsured", False, [expansion], False),
             ("unweighted, no expansion", "account_r1", "group_share_of_uninsured", False, [], False),
             ("row 4 weights, weighted, expansion", "account_r1_row4", "group_share_of_uninsured_row4", True,
              [expansion], False),
             (f"ACS {year}, weighted, expansion", f"acs{year}_uninsured_share", f"acs{year}_group_share_of_uninsured",
              True, [expansion], False),
             # Post hoc: the CPS sample puts the same sampling error into the regressor and the prediction; an
             # ACS regressor has independent error. Region dummies test for a regional confounder.
             (f"post hoc: CPS shares, ACS {year} regressor, weighted, expansion", "account_r1",
              f"acs{year}_group_share_of_uninsured", True, [expansion], True),
             ("post hoc: weighted, expansion, Census regions", "account_r1", "group_share_of_uninsured", True,
              [expansion, *regions.T], True)]
    for name, share, x, weighted, extra, post_hoc in specs:
        yv = np.log(st.s10_share / st[share]).to_numpy()
        X = np.column_stack([np.ones(len(st)), st[x].to_numpy(), *extra])
        w = st[share].to_numpy() if weighted else np.ones(len(st))
        beta, se, resid = wls_hc1(yv, X, w)
        lo, hi = beta[1] - Z95 * se[1], beta[1] + Z95 * se[1]
        alt = sl["alternative_weighted"] if weighted else sl["alternative_unweighted"]
        fits.append(dict(fit=name, post_hoc=post_hoc, slope=beta[1], se=se[1], ci_low=lo, ci_high=hi,
                         alternative=alt, expansion_coef=beta[2] if extra else np.nan,
                         expansion_se=se[2] if extra else np.nan, residual_sd=resid,
                         verdict=slope_verdict(lo, hi, alt)))
    fits = pd.DataFrame(fits)
    prim = fits.iloc[0]
    scores.append(dict(check=3, item="slope_on_group_share", label="pre-registered", target=prim.slope,
                       prediction=0.0, band_low=prim.ci_low, band_high=prim.ci_high, verdict=prim.verdict,
                       gap=prim.slope, explanation=f"95% interval {prim.ci_low:.2f} to {prim.ci_high:.2f} (SE "
                                                   f"{prim.se:.2f}); r = 0.7 implies {prim.alternative:.3f}; weighted "
                                                   f"residual SD {prim.residual_sd:.2f}"))
    # Post hoc: the use ratio r whose key would produce the fitted slope under the primary specification.
    x_cps = st.group_share_of_uninsured.to_numpy()
    X0 = np.column_stack([np.ones(len(st)), x_cps, expansion])
    w0 = st.account_r1.to_numpy()

    def implied_slope(r):
        share_r = (r * st.py_group + st.py_other) / (r * st.py_group + st.py_other).sum()
        e = np.log(share_r / st.account_r1).to_numpy()
        return float(np.linalg.lstsq(X0 * np.sqrt(w0)[:, None], e * np.sqrt(w0), rcond=None)[0][1])

    def implied_r(target):  # the implied slope rises with r
        lo, hi = 1e-3, 1.5
        if not implied_slope(lo) <= target <= implied_slope(hi):
            return np.nan
        for _ in range(80):
            mid = (lo + hi) / 2
            lo, hi = (lo, mid) if implied_slope(mid) > target else (mid, hi)
        return (lo + hi) / 2

    if not np.isclose(implied_slope(0.7), sl["alternative_weighted"], atol=2e-3):
        raise SystemExit("[BLOCKED] the implied-slope map does not reproduce the frozen r = 0.7 alternative")
    r_hat = [implied_r(v) for v in (prim.slope, prim.ci_low, prim.ci_high)]
    notes.append(dict(check=3, item="slope_on_group_share", kind="post-hoc explanation", value=r_hat[0],
                      note=f"the use ratio r whose key would produce the fitted slope: {r_hat[0]:.2f} (interval "
                           f"{r_hat[1]:.2f}-{r_hat[2]:.2f}), read off the frozen person-years with the expansion "
                           "indicator held in"))
    for _, f in fits[fits.post_hoc].iterrows():
        notes.append(dict(check=3, item="slope_on_group_share", kind="post-hoc robustness", value=f.slope,
                          note=f"{f.fit}: slope {f.slope:.2f} (95% {f.ci_low:.2f} to {f.ci_high:.2f}), {f.verdict}"))
    notes.append(dict(check=3, item="slope_on_group_share", kind="context", value=prim.expansion_coef,
                      note=f"expansion coefficient {prim.expansion_coef:.3f} (SE {prim.expansion_se:.3f}): states "
                           f"without expansion in {year} report {np.exp(prim.expansion_coef) - 1:.0%} more S-10 "
                           "uncompensated care per uninsured person-year"))
    resid = pd.Series(np.log(st.s10_share / st.account_r1).to_numpy() - X0 @ np.linalg.lstsq(
        X0 * np.sqrt(w0)[:, None], np.log(st.s10_share / st.account_r1).to_numpy() * np.sqrt(w0), rcond=None)[0],
                      index=st.state)
    big = resid[st.set_index("state").account_r1 >= 0.015].sort_values()
    notes.append(dict(check=3, item="slope_on_group_share", kind="context", value=resid["MD"],
                      note="primary-fit residuals, states with at least 1.5% of the prediction: "
                           + ", ".join(f"{k} {v:+.2f}" for k, v in big.items()) + f"; MD (all-payer rates) "
                           f"{resid['MD']:+.2f}"))
    # National total.
    nat = tol["check3"]["national"]
    n_acc = nat["account_N"][str(year)]
    ratio = national / n_acc
    scores.append(dict(check=3, item=f"national_line30_{year}", label="pre-registered", target=national,
                       prediction=n_acc, band_low=nat["low"] * n_acc, band_high=nat["high"] * n_acc,
                       verdict="hit" if nat["low"] <= ratio <= nat["high"] else "miss", gap=ratio - 1,
                       explanation=f"S-10 line 30, 50 states and DC after cleaning, ${national:.2f}bn against the "
                                   f"account's ${n_acc:.2f}bn"))
    return st, fits, tally


# ------------------------------------------------------------------------------------------------------
def main():
    print("[guard]", flush=True)
    frozen_guard()
    sources = check_sources()
    pred = pd.read_csv(OUT / "predictions.csv", keep_default_na=False, na_values=[""])
    pred["allocation"] = pred.allocation.fillna("")
    tol = json.loads((OUT / "tolerances.json").read_text())
    scores, notes = [], []
    print("[check 1: NAE 2021]", flush=True)
    targets, meta = nae_targets()
    score_check1(pred, tol, targets, meta, scores, notes)
    print("[check 2: NAS 2017 Table 8-1]", flush=True)
    nas = nas_table()
    score_check2(pred, tol, nas, scores, notes)
    print("[check 3: HCRIS S-10]", flush=True)
    st, fits, tally = hcris(pred, tol, scores, notes)

    OUT.mkdir(exist_ok=True)
    pd.DataFrame(scores).to_csv(OUT / "scores.csv", index=False, lineterminator="\n")
    pd.DataFrame(notes).to_csv(OUT / "notes.csv", index=False, lineterminator="\n")
    targets.to_csv(OUT / "nae_targets.csv", index=False, lineterminator="\n")
    keep = ["fips", "state", "line30_bn", "reports_kept", "s10_share", "account_r1", "account_r07",
            "baseline_uninsured_count", "baseline_population", "group_share_of_uninsured",
            f"not_expanded_{tally['year']}_kff", "account_r1_row4", f"acs{tally['year']}_uninsured_share"]
    st[keep].to_csv(OUT / "hcris_s10_states.csv", index=False, lineterminator="\n")
    fits.to_csv(OUT / "hcris_fits.csv", index=False, lineterminator="\n")
    extra = dict(nae_meta=meta, nas_table_8_1=nas, hcris_tally=tally)
    (OUT / "sources.json").write_text(json.dumps(dict(sources=sources, parsed=extra), indent=1, sort_keys=True,
                                                 default=float) + "\n")
    for s in scores:
        print(f"  {s['check']} {s['item']}: {s['verdict']} — target {s['target']:.4g}, gap {s['gap']:+.4g}")
    print(f"  ✓ {len(scores)} verdicts and {len(notes)} notes written")


if __name__ == "__main__":
    main()
