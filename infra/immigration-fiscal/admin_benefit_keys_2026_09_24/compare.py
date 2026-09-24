"""Survey keys against administrative Hispanic shares, and the union's dollars re-keyed.

Reads this lane's outputs: derived/cps_keys_national.csv and _cache/cps_state_replicates.npz
(cps_keys.py), derived/admin_snap_qc.csv (snap_qc.py), admin_wic_pc.csv (admin_wic.py),
admin_tanf.csv (admin_tanf.py), admin_ui_eta203.csv (admin_ui.py), admin_hud_psh.csv (admin_hud.py),
admin_medicaid_taf.csv (admin_medicaid.py) and acs_recipients_2024.csv (acs_check.py); the account's
allocations (full_account_spending_2026_09_20/derived/allocations.csv, preferred keys, F per capita);
BEA Table 3.12 lines 35, 37, 39 (pinned workbook) and FNS WIC monthly food costs.

Relative reporting. For a Hispanic share h in the survey and a share a in the administrative data
under the same definition, rho = odds(h) / odds(a) is the survey's reporting rate for Hispanic
receipt relative to other receipt (rho < 1: Hispanic receipt under-reported). It transports
between populations with different Hispanic shares; a ratio of shares does not.

Specifications (derived/program_keys.csv, one row per programme x spec x allocation):
  B   national: rho from the national admin share and the CPS measure that matches it, applied
      to every Hispanic dollar of the account key (assumes Mexicans report like other Hispanics).
  A   route-A states (TX, CA, AZ, NM, NV where the admin ethnicity is usable), pooled with admin
      weights on both sides; rho applied to the union's key dollars only.
  G   geography only: admin state totals with CPS state Hispanic shares.
  BS  admin state totals and admin state Hispanic shares (the full administrative key).
  GA  G with each state's CPS share corrected by route A's rho.
  BV  BS where the state's administrative ethnicity passes the validity screen, GA where it fails
      (the central specification).
  B_screened  B computed over the states that pass the screen, both sides weighted by admin totals.
G, BS, GA and BV rebuild the union's share as sum_s A_s [h_s m_s + (1 - h_s) n] / sum_s A_s, with
m_s the union's share of Hispanic recipients in state s (ACS 2024: SNAP persons, public-assistance
persons, Medicaid persons, low-income or all persons as noted), n the union's share of non-Hispanic
recipients (CPS, national), and divide it by the same construction on CPS state totals and shares;
the account key's union share is scaled by that factor.

State weights A_s are dollars wherever an administrative source gives them by state: SNAP QC
benefits, HUD federal spending, ETA 5159 state UI benefits paid, ACF TANF basic assistance (federal
and MOE) and FNS WIC food costs (admin_state_dollars.py). Where the comparable CPS measure counts
people (WIC, TANF), the CPS side is weighted by the CPS key's own dollars by state, so both sides
compare dollar geography with within-state shares of people. The earlier people-weighted versions
are kept as variants (_participants, _recipients, _claims).

Validity screen (derived/admin_validity.csv): a state's administrative ethnicity fails when at least
half of the records lack it, or when its known Hispanic share is below half the ACS 2024 Hispanic
share of the matching population (SNAP: persons in SNAP households; UI: all persons; others:
persons below 200% of poverty). The route-A states used for rho are the five that pass.

Every CPS quantity is recomputed on the 160 successive-difference replicates, so each re-keyed
dollar figure carries a replicate SE (administrative shares held fixed; their own sampling error
is reported where the source gives it).

Writes derived/program_keys.csv, derived/share_comparisons.csv, derived/admin_validity.csv,
derived/package_se.csv and derived/line_deltas.json.
Run from the repo root after the scripts above:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with openpyxl python3 \
      infra/immigration-fiscal/admin_benefit_keys_2026_09_24/compare.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd

HERE = Path(__file__).resolve().parent
D = HERE / "derived"
FISCAL = HERE.parent
ALLOC = FISCAL / "full_account_spending_2026_09_20/derived/allocations.csv"
BEA = Path("/Users/alien/research-data/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx")
BEA_SHA = "69b5c7aefb38675324887ce31d6feb4fcde7c903ab952db7328da0813096615e"
WIC_MONTHLY = HERE / "_cache/wic_cost/37wic-monthly-9.xlsx"
SCREEN_UNKNOWN, SCREEN_RATIO = 0.5, 0.5
ROUTE_A = ["TX", "CA", "AZ", "NM", "NV"]
NAMES = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
         "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC",
         "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN",
         "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
         "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
         "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
         "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
         "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI",
         "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
         "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI",
         "Wyoming": "WY"}
REP = np.load(HERE / "_cache/cps_state_replicates.npz")
STATES = [str(s) for s in REP["states"]]
if len(STATES) != 51 or set(STATES) != set(NAMES.values()):
    raise SystemExit("[BLOCKED] CPS replicate file does not cover 50 states and DC")


def sha(path: Path) -> str:
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def odds(p):
    p = np.asarray(p, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        return p / (1 - p)


def rep_se(x):
    x = np.asarray(x, float)
    return float(np.sqrt(4 / 160 * np.square(x[1:] - x[0]).sum()))


def cps(programme, measure, allocation):
    """State x replicate sums for one CPS measure: total, hisp, union, union_hisp, union_nonhisp."""
    parts = ["total", "hisp", "union", "union_hisp", "mex_hisp", "union_nonhisp"]
    out = {p: REP[f"{programme}|{measure}|{allocation}|{p}"] for p in parts}
    return out


def by_state(series: pd.Series) -> np.ndarray:
    s = series.reindex(STATES)
    if s.isna().any():
        raise SystemExit(f"[BLOCKED] admin input lacks states {list(s[s.isna()].index)}")
    return s.to_numpy(float)


# ---------------------------------------------------------------- administrative inputs
def state_dollars(programme):
    s = pd.read_csv(D / "admin_state_dollars.csv")
    return by_state(s[s.programme == programme].set_index("state").dollars_bn)


def admin_snap():
    q = pd.read_csv(D / "admin_snap_qc.csv")
    q = q[q.measure == "dollars"].copy()
    q = q[q.geography.isin(NAMES)].assign(st=lambda x: x.geography.map(NAMES)).set_index("st")
    return dict(total=by_state(q.total), central=by_state(q.hisp_share_imputed), known=by_state(q.hisp_share_known),
                low=by_state(q.hisp_share_lower), high=by_state(q.hisp_share_upper), unknown=by_state(q.unknown_share),
                year="FY2024", source="SNAP QC FY2024 public-use file (FSBEN x FYWGT)",
                unit="benefit dollars split over participants")


def admin_wic(weights="dollars"):
    w = pd.read_csv(D / "admin_wic_pc.csv")
    w = w[(w.source_year == 2022) & (w.category == "all") & (w.geography_type == "state")].set_index("state_postal")
    w = w[w.index.isin(STATES)]
    h = by_state(w.hispanic_share_all)
    unknown = by_state((w.ethnicity_unknown.fillna(0) / w.participants))
    total = state_dollars("wic") if weights == "dollars" else by_state(w.participants)
    return dict(total=total, central=h, known=by_state(w.hispanic_share_known.fillna(w.hispanic_share_all)),
                low=h, high=h + unknown, unknown=unknown, year="April 2022 shares; FY2024 food costs" if weights == "dollars"
                else "April 2022", source="FNS WIC Participant and Program Characteristics 2022, Table B.8"
                + ("; state weights FNS WIC food costs FY2024" if weights == "dollars" else ""),
                unit="participants' Hispanic share, weighted by " + ("food dollars" if weights == "dollars" else "participants"))


def admin_tanf(with_moe=True, weights="dollars"):
    t = pd.read_csv(D / "admin_tanf.csv")
    t = t[(t.fiscal_year == 2024) & (t.geography_type == "state")]
    rows = {}
    for st in STATES:
        parts = t[(t.state_postal == st) & (t.program.isin(["TANF", "SSP-MOE"] if with_moe else ["TANF"]))]
        parts = parts[parts.recipient_hispanic_pct.notna() & (parts.recipients > 0)]
        if parts.empty:
            raise SystemExit(f"[BLOCKED] TANF row missing for {st}")
        n = parts.recipients
        hp, un = parts.recipient_hispanic_pct / 100, parts.recipient_eth_unknown_pct.fillna(0) / 100
        rows[st] = dict(total=n.sum(), low=(n * hp).sum() / n.sum(), high=(n * (hp + un)).sum() / n.sum(),
                        known=(n * hp).sum() / (n * (1 - un)).sum(), unknown=(n * un).sum() / n.sum())
    f = pd.DataFrame(rows).T
    total = state_dollars("tanf") if weights == "dollars" else by_state(f.total)
    return dict(total=total, central=by_state(f.known), known=by_state(f.known), low=by_state(f.low),
                high=by_state(f.high), unknown=by_state(f.unknown), year="FY2024",
                source="ACF Characteristics and Financial Circumstances of TANF Recipients FY2024, Tables 10, 59"
                       + ("" if with_moe else " (TANF only)")
                       + ("; state weights ACF TANF and MOE Financial Data FY2024, Table B, basic assistance"
                          if weights == "dollars" else ""),
                unit="recipients' Hispanic share, TANF" + (" + SSP-MOE" if with_moe else "") + ", weighted by "
                     + ("basic-assistance dollars" if weights == "dollars" else "recipients"))


def admin_ui(weights="dollars"):
    u = pd.read_csv(D / "admin_ui_eta203.csv").set_index("geography")
    total = by_state(u.benefits_paid_bn) if weights == "dollars" else by_state(u.total)
    return dict(total=total, central=by_state(u.hisp_share_known), known=by_state(u.hisp_share_known),
                low=by_state(u.hisp_share_all), high=by_state((u.hispanic + u.ethnicity_na) / u.total),
                unknown=by_state(u.na_share), year="CY2024",
                source="DOL ETA 203, 2024 monthly reports" + ("; state weights ETA 5159 state UI benefits paid 2024"
                                                              if weights == "dollars" else ""),
                unit="claimants' Hispanic share, weighted by " + ("benefits paid" if weights == "dollars" else "claimant-weeks"))


def admin_hud():
    h = pd.read_csv(D / "admin_hud_psh.csv")
    h = h[h.year == 2024].set_index("geography")
    d = by_state(h.hisp_share_dollars)
    return dict(total=by_state(h.federal_spending_bn), central=d, known=d, low=d, high=d, unknown=np.zeros(51),
                year="2024", source="HUD Picture of Subsidized Households 2024", unit="federal spending, by head's ethnicity")


def admin_medicaid():
    m = pd.read_csv(D / "admin_medicaid_taf.csv")
    s = m[(m.year == 2023) & m.source.str.startswith("CMS DQ Atlas, Race") & m.state_postal.isin(STATES)]
    s = s.set_index("state_postal")
    known = s.hispanic_share_known / 100
    # Arizona does not code Hispanic ethnicity in T-MSIS (DQ Atlas: 16.0% vs ACS 45.5%); use the ACS share.
    known = known.where(s.index != "AZ", s.acs_hispanic_share / 100)
    unk = s.unknown_share / 100
    low = known * (1 - unk)
    high = low + unk
    nat = m[(m.year == 2022) & m.geography.astype(str).str.contains("REI national minus Puerto")]
    return dict(total=by_state(s.total), central=by_state(known), known=by_state(known), low=by_state(low),
                high=by_state(high), national_rei=float(nat.hispanic_share_known.iloc[0]) / 100, year="2023 (states), 2022 (national REI)",
                source="CMS DQ Atlas TAF 2023 (state self-report); CMS REI 2022 national", unit="enrollees ever enrolled")


def validity(prog, admin, acs_measure, ratio=SCREEN_RATIO):
    """Screen each state's administrative ethnicity against the ACS; returns a boolean array (51,) and rows."""
    a = pd.read_csv(D / "acs_recipients_2024.csv").set_index(["measure", "geography"]).hisp_share
    ref = a[acs_measure].reindex(STATES).fillna(a["low_income_persons"].reindex(STATES)).to_numpy(float)
    known, unknown, w = admin["known"], admin["unknown"], admin["total"]
    fail_unknown = unknown >= SCREEN_UNKNOWN
    fail_ratio = known < ratio * ref
    invalid = fail_unknown | fail_ratio
    rows = [dict(programme=prog, state=st, weight_share=w[i] / w.sum(), admin_known=known[i], admin_unknown=unknown[i],
                 acs_measure=acs_measure, acs_hisp_share=ref[i], known_to_acs=known[i] / ref[i] if ref[i] > 0 else np.nan,
                 invalid=bool(invalid[i]),
                 reason=("unknown >= 50%" if fail_unknown[i] else "") + (" known < half the ACS share" if fail_ratio[i] else ""))
            for i, st in enumerate(STATES)]
    return invalid, rows


def acs_m(measure):
    """Union share of Hispanic recipients by state; a state with no Hispanic recipient records takes
    its low-income value, then the national value."""
    a = pd.read_csv(D / "acs_recipients_2024.csv").set_index(["measure", "geography"]).union_in_hisp
    s = a[measure].reindex(STATES)
    s = s.fillna(a["low_income_persons"].reindex(STATES)).fillna(a[(measure, "US")])
    return by_state(s)


# ---------------------------------------------------------------- line amounts
def partial_shares():
    if sha(BEA) != BEA_SHA:
        raise SystemExit("[BLOCKED] BEA workbook changed")
    book = openpyxl.load_workbook(BEA, read_only=True, data_only=True)
    rows = list(book["T31200-A"].values)
    head = [r for r in rows if r[0] == "Line"][0]
    j = [i for i, x in enumerate(head) if str(x) == "2024"][0]
    line = {int(r[0]): (str(r[1]).strip(), r[j]) for r in rows if str(r[0]).isdigit()}
    if not (line[35][0].startswith("Family assistance") and line[37][0] == "General assistance"
            and line[39][0].startswith("Other")):
        raise SystemExit("[BLOCKED] BEA Table 3.12 labels changed")
    tanf_share = line[35][1] / (line[35][1] + line[37][1])
    pins = json.loads((WIC_MONTHLY.parent / "SOURCE_PINS.json").read_text())
    if sha(WIC_MONTHLY) != pins[WIC_MONTHLY.name]["sha256"]:
        raise SystemExit("[BLOCKED] WIC monthly workbook changed since admin_state_dollars.py pinned it")
    w = pd.read_excel(WIC_MONTHLY, header=None)
    lab = w[0].astype(str).str.strip()
    months = [f"{m} 2024" for m in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]]
    sel = w[lab.isin(months)]
    if len(sel) != 12:
        raise SystemExit("[BLOCKED] WIC monthly workbook lacks calendar 2024")
    food = float(sel[5].sum())
    wic_share = food / (line[39][1] * 1e6)
    return dict(tanf_share=tanf_share, tanf_bn=line[35][1] / 1000, ga_bn=line[37][1] / 1000,
                wic_food_cy2024_bn=food / 1e9, line39_bn=line[39][1] / 1000, wic_share=wic_share)


# ---------------------------------------------------------------- engine
def key_parts(programme, measure, allocation):
    k = cps(programme, measure, allocation)
    tot = k["total"].sum(0)
    return dict(h=k["hisp"].sum(0) / tot, U=k["union"].sum(0) / tot, UH=k["union_hisp"].sum(0) / tot,
                UN=k["union_nonhisp"].sum(0) / tot)


def state_shares(c):
    tot = c["total"]
    nat = c["hisp"].sum(0) / tot.sum(0)
    with np.errstate(invalid="ignore", divide="ignore"):
        h = np.where(tot > 0, c["hisp"] / np.where(tot > 0, tot, 1), nat[None, :])
    return h, tot


def rebuild(weights, h, m, n):
    """Union share sum_s w_s [h_s m_s + (1 - h_s) n] / sum_s w_s; w (51,) or (51, 161), h (51, 161)."""
    w = weights if weights.ndim == 2 else weights[:, None]
    return (w * (h * m[:, None] + (1 - h) * n[None, :])).sum(0) / w.sum(0)


def specs_for(name, admin, comp, m, a_states, admin_variant="central", base=None, invalid=None):
    """Return dict spec -> (ratio arrays and factor on the key's union share) for one comparable pair.
    base: a CPS dollar measure whose state totals weight the CPS side (when comp counts people);
    invalid: states whose administrative ethnicity fails the screen (for BV)."""
    c = cps(*comp)
    hc, ctot = state_shares(c)
    bw = cps(*base)["total"] if base else ctot
    nat_h = (bw * hc).sum(0) / bw.sum(0)
    n = c["union_nonhisp"].sum(0) / (ctot.sum(0) - c["hisp"].sum(0))
    A = admin["total"]
    ha = admin[admin_variant]
    a_nat = (A * ha).sum() / A.sum()
    out = {}
    rho_b = odds(nat_h) / odds(a_nat)
    out["B"] = dict(admin_share=a_nat, survey_share=nat_h, rho=rho_b, kind="all_hispanic")
    idx = [STATES.index(s) for s in a_states]
    if idx:
        wa = A[idx]
        a_A = (wa * ha[idx]).sum() / wa.sum()
        c_A = (wa[:, None] * hc[idx]).sum(0) / wa.sum()
        rho_a = odds(c_A) / odds(a_A)
        out["A"] = dict(admin_share=a_A, survey_share=c_A, rho=rho_a, kind="union_only", states=",".join(a_states))
    base_u = rebuild(bw, hc, m, n)
    g = rebuild(A, hc, m, n)
    out["G"] = dict(admin_share=a_nat, survey_share=(A[:, None] * hc).sum(0) / A.sum(), factor=g / base_u, kind="factor")
    bs = rebuild(A, np.repeat(ha[:, None], 161, axis=1), m, n)
    out["BS"] = dict(admin_share=a_nat, survey_share=nat_h, factor=bs / base_u, kind="factor")
    if idx:
        hadj = (hc / rho_a) / (hc / rho_a + 1 - hc)
        ga = rebuild(A, hadj, m, n)
        out["GA"] = dict(admin_share=a_nat, survey_share=nat_h, factor=ga / base_u, kind="factor", rho=rho_a,
                         states=",".join(a_states))
        if invalid is not None:
            ok = ~invalid
            a_v = (A[ok] * ha[ok]).sum() / A[ok].sum()
            c_v = (A[ok][:, None] * hc[ok]).sum(0) / A[ok].sum()
            out["B_screened"] = dict(admin_share=a_v, survey_share=c_v, rho=odds(c_v) / odds(a_v), kind="all_hispanic",
                                     states=f"{int(ok.sum())} states passing the screen")
            hv = np.where(invalid[:, None], hadj, ha[:, None])
            bv = rebuild(A, hv, m, n)
            out["BV"] = dict(admin_share=float((A * hv[:, 0]).sum() / A.sum()), survey_share=nat_h, factor=bv / base_u,
                             kind="factor", rho=rho_a, states=",".join(a_states),
                             replaced=",".join(np.array(STATES)[invalid]))
    return out


def rekey(spec, kp):
    """New union share of the key (161,) under a spec."""
    if spec["kind"] == "all_hispanic":
        r = spec["rho"]
        return (kp["UH"] / r + kp["UN"]) / (kp["h"] / r + 1 - kp["h"])
    if spec["kind"] == "union_only":
        r = spec["rho"]
        return (kp["U"] / r) / (kp["U"] / r + 1 - kp["U"])
    return kp["U"] * spec["factor"]


def share_comparisons():
    """Long table: admin, CPS and ACS Hispanic shares under matching definitions, US and route-A states."""
    cn = pd.read_csv(D / "cps_keys_national.csv")
    cs = pd.read_csv(D / "cps_keys_state.csv")
    acs = pd.read_csv(D / "acs_recipients_2024.csv")
    q = pd.read_csv(D / "admin_snap_qc.csv")
    q["st"] = q.geography.map(NAMES).fillna(q.geography)
    t = pd.read_csv(D / "admin_tanf.csv")
    t = t[t.fiscal_year == 2024]
    w = pd.read_csv(D / "admin_wic_pc.csv")
    w = w[(w.source_year == 2022) & (w.category == "all")]
    u = pd.read_csv(D / "admin_ui_eta203.csv").set_index("geography")
    h = pd.read_csv(D / "admin_hud_psh.csv")
    h = h[h.year == 2024].set_index("geography")
    med = pd.read_csv(D / "admin_medicaid_taf.csv")
    geos = ["US"] + ROUTE_A

    def cps_val(prog, meas, alloc, geo):
        src = cn if geo == "US" else cs[cs.geography == geo]
        r = src[(src.programme == prog) & (src.measure == meas) & (src.allocation == alloc)]
        return (float(r.hisp_share.iloc[0]), float(r.hisp_share_se.iloc[0]), int(r.records.iloc[0])) if len(r) else (np.nan,) * 3

    def acs_val(meas, geo):
        r = acs[(acs.measure == meas) & (acs.geography == geo)]
        return (float(r.hisp_share.iloc[0]), float(r.hisp_share_se.iloc[0])) if len(r) and meas else (np.nan, np.nan)

    def qc(meas, geo):
        r = q[(q.measure == meas) & (q.st == geo)]
        if not len(r):
            return {}
        r = r.iloc[0]
        return dict(admin=r.hisp_share_imputed, known=r.hisp_share_known, low=r.hisp_share_lower,
                    high=r.hisp_share_upper, unknown=r.unknown_share)

    def qc_us(meas):
        # 50 states + DC only (the file's US row includes Guam and the Virgin Islands)
        r = q[(q.measure == meas) & q.geography.isin(NAMES)]
        tot = r.total.sum()
        known_w = (r.total * (1 - r.unknown_share))
        return dict(admin=(r.total * r.hisp_share_imputed).sum() / tot,
                    known=(known_w * r.hisp_share_known.fillna(0)).sum() / known_w.sum(),
                    low=(r.total * r.hisp_share_lower).sum() / tot, high=(r.total * r.hisp_share_upper).sum() / tot,
                    unknown=(r.total * r.unknown_share).sum() / tot)

    def tanf(geo, col, programs=("TANF", "SSP-MOE")):
        if geo == "US":
            r = t[(t.geography_type == "state") & t.program.isin(programs)]
        else:
            r = t[(t.state_postal == geo) & t.program.isin(programs)]
        n = {"recipient": "recipients", "adult": "adults", "child": "children"}[col]
        r = r[r[f"{col}_hispanic_pct"].notna() & (r[n] > 0)]
        if not len(r):
            return {}
        hp, un = r[f"{col}_hispanic_pct"] / 100, r[f"{col}_eth_unknown_pct"].fillna(0) / 100
        return dict(admin=(r[n] * hp).sum() / (r[n] * (1 - un)).sum(), known=(r[n] * hp).sum() / (r[n] * (1 - un)).sum(),
                    low=(r[n] * hp).sum() / r[n].sum(), high=(r[n] * (hp + un)).sum() / r[n].sum(),
                    unknown=(r[n] * un).sum() / r[n].sum())

    def wic(geo):
        if geo == "US":
            r = w[(w.geography_type == "state") & w.state_postal.isin(STATES)]
            a = (r.participants * r.hispanic_share_all).sum() / r.participants.sum()
        else:
            a = float(w[(w.state_postal == geo) & (w.geography_type == "state")].hispanic_share_all.iloc[0])
        return dict(admin=a, known=a, low=a, high=a, unknown=0.0)

    def ui(geo):
        if geo == "US":
            r = u.loc[STATES].sum()
            r["hisp_share_known"] = r.hispanic / (r.hispanic + r.not_hispanic)
            r["hisp_share_all"] = r.hispanic / r.total
            r["na_share"] = r.ethnicity_na / r.total
        else:
            r = u.loc[geo]
        return dict(admin=r.hisp_share_known, known=r.hisp_share_known, low=r.hisp_share_all,
                    high=r.hisp_share_all + r.na_share, unknown=r.na_share)

    def hud(geo, col):
        a = float(h.loc[geo, col])
        return dict(admin=a, known=a, low=a, high=a, unknown=np.nan)

    def medicaid(geo):
        if geo == "US":
            nat = med[(med.year == 2022) & med.geography.astype(str).str.contains("REI national minus Puerto")]
            a = float(nat.hispanic_share_known.iloc[0]) / 100
            dq = med[(med.year == 2023) & med.geography.astype(str).str.contains("sum of DQ Atlas states")]
            return dict(admin=a, known=float(dq.hispanic_share_known.iloc[0]) / 100,
                        low=float(dq.hispanic_share_all.iloc[0]) / 100,
                        high=float(dq.hispanic_share_all.iloc[0] + dq.unknown_share.iloc[0]) / 100,
                        unknown=float(dq.unknown_share.iloc[0]) / 100,
                        dq_acs=float(dq.acs_hispanic_share.iloc[0]) / 100)
        r = med[(med.year == 2023) & med.source.str.startswith("CMS DQ Atlas, Race") & (med.state_postal == geo)].iloc[0]
        return dict(admin=r.hispanic_share_known / 100, known=r.hispanic_share_known / 100,
                    low=r.hispanic_share_all / 100, high=(r.hispanic_share_all + r.unknown_share) / 100,
                    unknown=r.unknown_share / 100, dq_acs=r.acs_hispanic_share / 100, grade=r.dq_grade)

    defs = [
        ("snap", "benefit dollars split over participants", lambda g: qc_us("dollars") if g == "US" else qc("dollars", g),
         ("snap", "key", "both"), None),
        ("snap", "benefit dollars by unit head", lambda g: qc_us("head_dollars") if g == "US" else qc("head_dollars", g),
         ("snap", "head_dollars", "both"), None),
        ("snap", "participants (CPS: persons in receiving units)",
         lambda g: qc_us("participants") if g == "US" else qc("participants", g), ("snap", "persons_in_units", "both"), None),
        ("snap", "everyone listed in the home (ACS: persons in SNAP households)",
         lambda g: qc_us("listed_persons") if g == "US" else qc("listed_persons", g), ("snap", "persons_in_units", "both"),
         "snap_persons"),
        ("snap", "units by head (CPS, ACS: households by householder)",
         lambda g: qc_us("units_by_head") if g == "US" else qc("units_by_head", g), ("snap", "households", "both"),
         "snap_households"),
        ("wic", "participants (CPS: under-5s and women reporting WIC in WIC households)", wic,
         ("wic", "women_children_in_wic_households", "both"), None),
        ("wic", "participants (CPS: household WIC count by householder)", wic,
         ("wic", "participants_by_householder", "both"), None),
        ("wic", "participants (CPS: the key's dollars)", wic, ("wic", "key", "both"), None),
        ("tanf", "recipients, TANF + SSP-MOE (CPS: persons in TANF-type units)", lambda g: tanf(g, "recipient"),
         ("cash", "persons_in_tanf_units", "both"), None),
        ("tanf", "recipients, TANF only (CPS: persons in TANF-type units)",
         lambda g: tanf(g, "recipient", ("TANF",)), ("cash", "persons_in_tanf_units", "both"), None),
        ("tanf", "adult recipients, TANF (CPS: TANF-type reporters; ACS: public-assistance income)",
         lambda g: tanf(g, "adult", ("TANF",)), ("cash", "adult_recipients_tanf", "both"), "pap_persons"),
        ("tanf", "child recipients, TANF (CPS: children in TANF-type units)", lambda g: tanf(g, "child", ("TANF",)),
         ("cash", "children_in_tanf_units", "both"), None),
        ("ui", "claimant-weeks (CPS: benefit dollars)", ui, ("ui", "key", "personal"), None),
        ("ui", "claimant-weeks (CPS: recipients)", ui, ("ui", "recipients", "both"), None),
        ("housing", "federal spending by head (CPS: subsidy dollars at the SPM head)",
         lambda g: hud(g, "hisp_share_dollars"), ("housing", "head_dollars", "both"), None),
        ("housing", "households by head (CPS: SPM units with a subsidy)", lambda g: hud(g, "hisp_share_households"),
         ("housing", "subsidized_households", "both"), None),
        ("housing", "households by head (CPS: households reporting public or reduced-rent housing)",
         lambda g: hud(g, "hisp_share_households"), ("housing", "households_reporting", "both"), None),
        ("medicaid", "enrollees (US: REI 2022 imputed; states: 2023 self-report, known) vs CPS coverage",
         medicaid, ("medicaid", "covered", "both"), "medicaid_persons"),
    ]
    rows = []
    for prog, label, admin_fn, cmeas, ameas in defs:
        for g in geos:
            a = admin_fn(g)
            if not a:
                continue
            c, cse, crec = cps_val(*cmeas, g)
            s, sse = acs_val(ameas, g)
            rows.append(dict(programme=prog, definition=label, geography=g, admin_share=a["admin"],
                             admin_share_known=a["known"], admin_low=a["low"], admin_high=a["high"],
                             admin_unknown=a.get("unknown", np.nan), cps_measure="|".join(cmeas), cps_share=c,
                             cps_se=cse, cps_records=crec, acs_measure=ameas or "", acs_share=s, acs_se=sse,
                             dq_atlas_acs5=a.get("dq_acs", np.nan), dq_grade=a.get("grade", ""),
                             rho_cps=odds(c) / odds(a["admin"]) if np.isfinite(c) else np.nan,
                             rho_acs=odds(s) / odds(a["admin"]) if np.isfinite(s) else np.nan))
    out = pd.DataFrame(rows)
    out.to_csv(D / "share_comparisons.csv", index=False, lineterminator="\n")
    return out


ROUTE_LABEL = {"B": "B: national admin share; rho on every Hispanic dollar",
               "A": "A: route-A states; rho on the union's dollars",
               "G": "admin state totals, CPS state shares",
               "BS": "admin state totals and shares, unscreened",
               "GA": "admin state totals, CPS shares corrected by route-A rho",
               "BV": "admin state totals and shares where the screen passes, GA elsewhere",
               "none": ""}


def main():
    share_comparisons()
    alloc = pd.read_csv(ALLOC)
    alloc = alloc[alloc.scenario_id == "complete_preferred_F_per_capita"].set_index(["category", "allocation"])
    ps = partial_shares()
    progs = [
        # name, admin loader result (dollar weights), comparable CPS measure, CPS dollar measure weighting the CPS
        # side (None: the comparable is already dollars), key per allocation, account line, share of line,
        # ACS measure for m_s, ACS measure for the screen, note
        ("snap", admin_snap(), ("snap", "key", "both"), None,
         {"personal": ("snap", "key", "both"), "shared": ("snap", "key", "both")},
         "snap", 1.0, "snap_persons", "snap_persons", "QC benefits by state"),
        ("wic", admin_wic(), ("wic", "women_children_in_wic_households", "both"), ("wic", "key", "both"),
         {"personal": ("wic", "key", "both"), "shared": ("wic", "key", "both")},
         "other_state_welfare", ps["wic_share"], "low_income_persons", "low_income_persons",
         "WIC food is this share of BEA line 39; the rest (foster care, adoption, nonprofits) is audit row 10"),
        ("tanf", admin_tanf(True), ("cash", "persons_in_tanf_units", "both"), ("cash", "tanf_key", "personal"),
         {"personal": ("cash", "key", "personal"), "shared": ("cash", "key", "shared")},
         "family_and_general_assistance", ps["tanf_share"], "pap_persons", "pap_persons",
         "TANF (line 35) share of lines 35+37; general assistance has no administrative ethnicity"),
        ("ui", admin_ui(), ("ui", "key", "personal"), None,
         {"personal": ("ui", "key", "personal"), "shared": ("ui", "key", "shared")},
         "unemployment", 1.0, "all_persons", "all_persons", "ETA 203 shares are of claimant-weeks"),
        ("housing", admin_hud(), ("housing", "head_dollars", "both"), None,
         {"personal": ("housing", "key", "both"), "shared": ("housing", "key", "both")},
         "housing_subsidies", 1.0, "low_income_persons", "low_income_persons", "subsidy line, response 0 in every profile"),
    ]
    rows, deltas, reps, screen = [], {}, {}, []

    def record(prog, spec_id, spec, line, share, keys, admin, note, extra=""):
        for allocation, keym in keys.items():
            kp = key_parts(*keym)
            new_u = rekey(spec, kp)
            now = float(alloc.loc[(line, allocation), "target_bn"]) * share
            rek = now * new_u / kp["U"]
            chg = rek - now
            rows.append(dict(
                programme=prog, spec=spec_id, route=ROUTE_LABEL[spec_id.split("_")[0]], allocation=allocation,
                year=admin["year"], admin_source=admin["source"], admin_unit=admin["unit"], line=line, line_share=share,
                admin_hisp_share=float(spec["admin_share"]),
                survey_hisp_share=float(np.atleast_1d(spec["survey_share"])[0]),
                survey_hisp_share_se=rep_se(spec["survey_share"]) if np.ndim(spec["survey_share"]) else np.nan,
                ratio=float(spec["admin_share"] / np.atleast_1d(spec["survey_share"])[0]),
                rho=float(np.atleast_1d(spec.get("rho", np.nan))[0]),
                rho_se=rep_se(spec["rho"]) if np.ndim(spec.get("rho", 0)) else np.nan,
                factor=float(np.atleast_1d(new_u / kp["U"])[0]),
                key_union_share=float(kp["U"][0]), rekeyed_union_share=float(new_u[0]),
                group_bn_now=now, group_bn_rekeyed=float(rek[0]), change_bn=float(chg[0]),
                change_se_bn=rep_se(chg), route_states=spec.get("states", ""),
                screened_out_states=spec.get("replaced", ""), note=(note + (" " + extra if extra else "")).strip()))
            deltas.setdefault(f"{prog}_{spec_id}", {}).setdefault(line, {})[allocation] = float(chg[0])
            reps.setdefault(f"{prog}_{spec_id}", {}).setdefault(line, {})[allocation] = chg

    for prog, admin, comp, base, keys, line, share, acs, acs_screen, note in progs:
        m = acs_m(acs)
        invalid, srows = validity(prog, admin, acs_screen)
        screen += srows
        a_states = [x for x in ROUTE_A if not invalid[STATES.index(x)]]
        specs = specs_for(prog, admin, comp, m, a_states, base=base, invalid=invalid)
        for spec_id, spec in specs.items():
            record(prog, spec_id, spec, line, share, keys, admin, note)
        for which in {"snap": ["known", "low", "high"], "tanf": ["low", "high"], "ui": ["low", "high"]}.get(prog, []):
            sv = specs_for(prog, admin, comp, m, a_states, admin_variant=which, base=base, invalid=invalid)
            for sid in ["B", "BS", "BV"]:
                record(prog, f"{sid}_{which}", sv[sid], line, share, keys, admin, note, f"admin unknown ethnicity: {which}")
        strict, _ = validity(prog, admin, acs_screen, ratio=0.75)
        ss = specs_for(prog, admin, comp, m, [x for x in ROUTE_A if not strict[STATES.index(x)]], base=base,
                       invalid=strict)
        if "BV" in ss:
            record(prog, "BV_strict", ss["BV"], line, share, keys, admin, note,
                   "screen at three quarters of the ACS share instead of half")
        if prog == "snap":
            noaz = invalid.copy()
            noaz[STATES.index("AZ")] = True
            sn = specs_for(prog, admin, comp, m, ["CA", "NV"], base=base, invalid=noaz)
            for sid in ["A", "GA", "BV"]:
                record(prog, sid + "_noAZ", sn[sid], line, share, keys, admin, note,
                       "Arizona treated as failing the screen (its T-MSIS lacks Hispanic codes; its QC share sits "
                       "furthest below both surveys)")
        if prog == "tanf":
            record(prog, "BV_fullline", specs["BV"], line, 1.0, keys, admin, note,
                   "TANF factor applied to the whole line, general assistance included")
            record(prog, "BV_income_security_services", specs["BV"], "income_security_services", 1.0, keys, admin,
                   "key-choice variant: the consumption line keyed by the same cash key (audit row 12)")
            t2 = admin_tanf(False)
            i2, _ = validity(prog, t2, acs_screen)
            s2 = specs_for(prog, t2, comp, m, [x for x in ROUTE_A if not i2[STATES.index(x)]], base=base, invalid=i2)
            for sid in ["B", "BS", "A", "BV"]:
                record(prog, sid + "_tanf_only", s2[sid], line, share, keys, t2, note, "TANF only, without SSP-MOE")
            s3 = specs_for(prog, admin, ("cash", "persons_in_units", "both"), m, a_states, base=("cash", "key", "personal"),
                           invalid=invalid)
            for sid in ["B", "BS", "BV"]:
                record(prog, sid + "_all_paw", s3[sid], line, share, keys, admin, note,
                       "CPS side: persons in units with any cash assistance")
            t4 = admin_tanf(True, weights="recipients")
            s4 = specs_for(prog, t4, comp, m, a_states, invalid=invalid)
            for sid in ["B", "BS", "A", "BV"]:
                record(prog, sid + "_recipients", s4[sid], line, share, keys, t4, note, "states weighted by recipients")
        if prog == "ui":
            s2 = specs_for(prog, admin, ("ui", "recipients", "both"), m, a_states, base=("ui", "key", "personal"),
                           invalid=invalid)
            for sid in ["B", "BS", "A", "BV"]:
                record(prog, sid + "_cpsrecipients", s2[sid], line, share, keys, admin, note, "CPS side: recipients")
            u3 = admin_ui(weights="claims")
            s3 = specs_for(prog, u3, comp, m, a_states, invalid=invalid)
            for sid in ["B", "BS", "A", "BV"]:
                record(prog, sid + "_claims", s3[sid], line, share, keys, u3, note, "states weighted by claimant-weeks")
        if prog == "wic":
            s2 = specs_for(prog, admin, ("wic", "key", "both"), m, a_states, invalid=invalid)
            for sid in ["B", "BS", "A", "BV"]:
                record(prog, sid + "_keydollars", s2[sid], line, share, keys, admin, note, "CPS side: the key's dollars")
            w3 = admin_wic(weights="participants")
            s3 = specs_for(prog, w3, comp, m, a_states, invalid=invalid)
            for sid in ["B", "BS", "A", "BV"]:
                record(prog, sid + "_participants", s3[sid], line, share, keys, w3, note, "states weighted by participants")
        if prog == "housing":
            s2 = specs_for(prog, admin, ("housing", "subsidized_households", "both"), m, a_states, invalid=invalid)
            for sid in ["B", "BS"]:
                record(prog, sid + "_households", s2[sid], line, share, keys, admin, note,
                       "admin dollars vs CPS subsidized households")
    # The first-pass central (people weights; SNAP route A from California and Nevada), kept for comparison.
    snap = [x for x in progs if x[0] == "snap"][0]
    s_fp = specs_for("snap", snap[1], snap[2], acs_m(snap[7]), ["CA", "NV"])
    record("snap", "GA_firstpass", s_fp["GA"], snap[5], snap[6], snap[4], snap[1], snap[9],
           "route-A rho from California and Nevada, no screen (first pass)")

    # Medicaid: the preferred key is MEPS dollars transported by age x US birth, not a self-report of
    # receipt, so it is not re-keyed; the rows test CPS-reported coverage against TAF enrollment.
    madm = admin_medicaid()
    mspec = specs_for("medicaid", madm, ("medicaid", "covered", "both"), acs_m("medicaid_persons"),
                      ["TX", "CA", "NM", "NV"])
    nat_h = key_parts("medicaid", "covered", "both")["h"]
    mspec["B_rei"] = dict(admin_share=madm["national_rei"], survey_share=nat_h,
                          rho=odds(nat_h) / odds(madm["national_rei"]))
    for sid in ["B_rei", "B", "A", "BS"]:
        s = mspec[sid]
        for allocation in ["personal", "shared"]:
            rows.append(dict(
                programme="medicaid", spec=sid if sid != "B" else "B_dq_self_report",
                route=ROUTE_LABEL[sid.split("_")[0]], allocation=allocation,
                year=madm["year"], admin_source=madm["source"], admin_unit=madm["unit"],
                line="medicaid_and_chip_other_medical", line_share=1.0, admin_hisp_share=float(s["admin_share"]),
                survey_hisp_share=float(np.atleast_1d(s["survey_share"])[0]),
                survey_hisp_share_se=rep_se(s["survey_share"]),
                ratio=float(s["admin_share"] / np.atleast_1d(s["survey_share"])[0]),
                rho=float(np.atleast_1d(s.get("rho", np.nan))[0]),
                rho_se=rep_se(s["rho"]) if np.ndim(s.get("rho", 0)) else np.nan,
                factor=float(np.atleast_1d(s.get("factor", np.nan))[0]),
                key_union_share=np.nan, rekeyed_union_share=np.nan,
                group_bn_now=float(alloc.loc[("medicaid_and_chip_other_medical", allocation), "target_bn"]),
                group_bn_rekeyed=np.nan, change_bn=np.nan, change_se_bn=np.nan,
                route_states=s.get("states", ""),
                note="MEPS key (not a self-report of receipt): not re-keyed; CPS-reported coverage vs TAF enrollment"
                     + ("; Arizona uses the ACS share (T-MSIS lacks Hispanic codes)" if sid in ("B", "BS") else "")))
    for allocation in ["personal", "shared"]:
        rows.append(dict(programme="ssi", spec="none", route="", allocation=allocation, year="", admin_source="none",
                         admin_unit="", line="ssi", line_share=1.0,
                         group_bn_now=float(alloc.loc[("ssi", allocation), "target_bn"]),
                         note="[BLOCKED] SSA publishes noncitizen counts, not ethnicity; no administrative key"))
    out = pd.DataFrame(rows)
    out.to_csv(D / "program_keys.csv", index=False, lineterminator="\n")
    pd.DataFrame(screen).to_csv(D / "admin_validity.csv", index=False, lineterminator="\n")
    central = ["snap_BV", "wic_BV", "tanf_BV", "ui_BV", "housing_BV"]
    packages = {
        "central": central,
        "route_A": ["snap_A", "wic_A", "tanf_A", "ui_A", "housing_A"],
        "route_B": ["snap_B", "wic_B", "tanf_B", "ui_B", "housing_B"],
        "route_B_screened": ["snap_B_screened", "wic_B_screened", "tanf_B_screened", "ui_B_screened", "housing_B_screened"],
        "admin_state_keys_unscreened": ["snap_BS", "wic_BS", "tanf_BS", "ui_BS", "housing_BS"],
        "geography_only": ["snap_G", "wic_G", "tanf_G", "ui_G", "housing_G"],
        "survey_shares_route_A_rho": ["snap_GA", "wic_GA", "tanf_GA", "ui_GA", "housing_GA"],
        "central_strict_screen": ["snap_BV_strict", "wic_BV_strict", "tanf_BV_strict", "ui_BV_strict", "housing_BV_strict"],
        "central_snap_noAZ": ["snap_BV_noAZ", "wic_BV", "tanf_BV", "ui_BV", "housing_BV"],
        "central_people_weights": ["snap_BV", "wic_BV_participants", "tanf_BV_recipients", "ui_BV_claims", "housing_BV"],
        "central_tanf_only": ["snap_BV", "wic_BV", "tanf_BV_tanf_only", "ui_BV", "housing_BV"],
        "central_tanf_full_line": ["snap_BV", "wic_BV", "tanf_BV_fullline", "ui_BV", "housing_BV"],
        "central_plus_income_security_services": central + ["tanf_BV_income_security_services"],
        "central_unknown_low": ["snap_BV_low", "wic_BV", "tanf_BV_low", "ui_BV_low", "housing_BV"],
        "central_unknown_high": ["snap_BV_high", "wic_BV", "tanf_BV_high", "ui_BV_high", "housing_BV"],
        "first_pass_central": ["snap_GA_firstpass", "wic_BS_participants", "tanf_BS_recipients", "ui_BS_claims",
                               "housing_BS"],
    }
    se_rows = []
    for name, members in packages.items():
        combo = {}
        for spec_id in members:
            for line, by_alloc in deltas[spec_id].items():
                for a, v in by_alloc.items():
                    combo.setdefault(line, {}).setdefault(a, 0.0)
                    combo[line][a] += v
        deltas[f"package_{name}"] = combo
        for a in ["personal", "shared"]:
            vec = sum(reps[spec_id][line][a] for spec_id in members for line in reps[spec_id]
                      if line != "housing_subsidies")
            se_rows.append(dict(package=name, allocation=a, change_bn_transfer_lines=float(vec[0]), se_bn=rep_se(vec),
                                members=" ".join(members)))
    se = pd.DataFrame(se_rows)
    se.to_csv(D / "package_se.csv", index=False, lineterminator="\n")
    (D / "line_deltas.json").write_text(json.dumps(dict(partial_shares=ps, packages=packages, deltas=deltas),
                                                   indent=1) + "\n")
    pd.set_option("display.width", 250)
    pd.set_option("display.max_rows", 400)
    cols = ["programme", "spec", "allocation", "admin_hisp_share", "survey_hisp_share", "rho", "rho_se", "factor",
            "group_bn_now", "group_bn_rekeyed", "change_bn", "change_se_bn", "screened_out_states"]
    print(out[out.allocation != "shared"][cols].round(4).to_string(index=False))
    print(se[se.allocation == "personal"].drop(columns="members").round(3).to_string(index=False))
    print(json.dumps(ps, indent=1))


if __name__ == "__main__":
    main()
