"""Translate the pooled cell ratios into the ledger's and the complete account's dollars.

Both accounts key public medical cost on MEPS 2024 all-donor means in the ten
transport cells (age band x US birth), applied to CPS ASEC 2025 records with
`exposure` (every record except infants the CPS leaves out of universe):

* ledger (`ledger_absolute_2026_09_17/absolute_ledger.py`): component `medical`
  = cell mean of the six public payers; item `M` = cell Medicaid mean x
  (1.5432 - 1) + cell Medicare mean x (1.2804 - 1), the NHEA-to-MEPS scaling;
* complete account (`full_account_spending_2026_09_20/builder.py`): national
  totals allocated by expected-dollar keys, Medicaid/CHIP/other medical by the
  TOTMCD24 cell mean, Medicare by TOTMCR24, health services by
  VA+TRICARE+other federal+state/local, military medical by TRICARE, veterans
  other by VA.

The union's key or charge is rebuilt cell by cell and gated against both
accounts' own outputs before any ratio touches it. The translation then scales
each cell by its Mexican-origin / all-donor ratio. For the account the national
key total is held fixed (the cell mean is the donor average, so people outside
the union in the same cell absorb the complement); a renormalized variant that
leaves everyone else's key unchanged is reported beside it.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
      infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/translate.py
"""
from __future__ import annotations

import hashlib
import json
import pickle
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
sys.path.insert(0, str(LANE))
from design import Z95, Est, combo  # noqa: E402

CACHE = LANE / "_cache"
DERIVED = LANE / "derived"
REPO = LANE.parents[2]
FISCAL = REPO / "infra/immigration-fiscal"
CPS_ZIP = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
CPS_SHA = "318845a2b5e0034eb2973898de1738f4df0025727de38499e7669cb9c0deef0b"  # builder.py CPS_SHA
LEDGER = FISCAL / "ledger_absolute_2026_09_17"
ACCOUNT = FISCAL / "full_account_spending_2026_09_20"
TARGET_POP = 40896574.15235156  # builder.py canonical target drift check

TRANSPORT_LABELS = ["0-17", "18-34", "35-49", "50-64", "65+"]
LEDGER_LABELS = ["0-17", "18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+"]
NAT = {1: "us_born", 2: "foreign_born"}
# account line -> (key name in incidence_keys.csv, MEPS columns of the key, ratio measure)
ACCOUNT_LINES = {
    "medicaid_and_chip_other_medical": ("medicaid", ["TOTMCD"], "medicaid"),
    "medicare": ("medicare", ["TOTMCR"], "medicare"),
    "health_services": ("health_other", ["TOTVA", "TOTTRI", "TOTOFD", "TOTSTL"], "other_public"),
    "military_medical": ("tricare", ["TOTTRI"], "tricare"),
    "veterans_other": ("va_medical", ["TOTVA"], "va"),
}
SPECS = ["plain", "winsor_p995", "winsor_p999", "two_part_lognormal",
         "pooled_excl_2020_2021", "pooled_cpi_all_items", "pooled_year_normalized"]
AGE_GROUPS = {"0-17": [0], "18-64": [1, 2, 3], "65+": [4], "all ages": [0, 1, 2, 3, 4]}


def _ok(msg):
    print(f"  ✓ {msg}", flush=True)


def _header(s):
    print(f"\n[{s}]", flush=True)


def fail(msg):
    print(f"  ✗ [BLOCKED] {msg}", file=sys.stderr, flush=True)
    raise SystemExit(2)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_cps() -> pd.DataFrame:
    """Same read, weight merge and group construction as `builder.py::build_keys`
    and `gen_ledger_extension_2026_09_16/extend_ledger.py::build`."""
    if sha256(CPS_ZIP) != CPS_SHA:
        fail("CPS ASEC archive changed since the account was built")
    fields = ["PH_SEQ", "PPPOS", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY",
              "PEMNTVTY", "PRDTHSP", "PUB", "PRIV"]
    with zipfile.ZipFile(CPS_ZIP) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=fields)
        w = pd.read_csv(z.open("asec_csv_repwgt_2025.csv"), usecols=["h_seq", "PPPOS", "pwwgt0"]
                        ).rename(columns={"h_seq": "PH_SEQ"})
    d = d.merge(w, on=["PH_SEQ", "PPPOS"], validate="one_to_one", how="left")
    if d.isna().any().any():
        fail("missing CPS keys after the replicate-weight merge")
    civilian = d.PRPERTYP.eq(2) | d.A_AGE.lt(15)
    native = d.PRCITSHP.isin([1, 2, 3])
    us = [57, 60, 66, 69, 73, 78]
    target = ((d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303))
              | (native & (d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)))
              | (native & d.PEFNTVTY.isin(us) & d.PEMNTVTY.isin(us) & d.PRDTHSP.eq(1)))
    d["civilian"] = civilian
    d["target"] = target & civilian
    d["exposure"] = ~(d.PUB.eq(0) & d.PRIV.eq(0))
    if d.loc[~d.exposure, "A_AGE"].gt(0).any():
        fail("reference exclusion includes a non-infant")
    d["tband"] = np.digitize(d.A_AGE, [18, 35, 50, 65])
    d["lband"] = np.digitize(d.A_AGE, [18, 25, 35, 45, 55, 65, 75])
    d["born"] = np.where(d.PENATVTY.eq(57), 1, 2)  # donor_model's CPS nativity rule
    nt = float(d.loc[d.target, "pwwgt0"].sum())
    if abs(nt - TARGET_POP) > 0.01:
        fail(f"canonical target population {nt} != {TARGET_POP}")
    return d


def meps_2024_cell_means(pool: pd.DataFrame) -> pd.DataFrame:
    m = pool[pool.year.eq(2024) & pool.PERWT.gt(0) & pool.AGE.ge(0) & pool.BORNUSA.isin([1, 2])].copy()
    m["tband"] = np.digitize(m.AGE, [18, 35, 50, 65])
    m["born"] = m.BORNUSA.astype(int)
    m["health_other"] = m[["TOTVA", "TOTTRI", "TOTOFD", "TOTSTL"]].sum(axis=1)
    cols = ["public_transport", "TOTMCR", "TOTMCD", "TOTVA", "TOTTRI", "health_other"]
    g = m.groupby(["tband", "born"])
    out = pd.DataFrame({c: g.apply(lambda x, c=c: (x[c] * x.PERWT).sum() / x.PERWT.sum(),
                                   include_groups=False) for c in cols})
    return out


def main():
    DERIVED.mkdir(exist_ok=True)
    audit = {}
    pool = pd.read_parquet(CACHE / "pooled.parquet")
    means = meps_2024_cell_means(pool)

    _header("rebuild the union's keys and charges from CPS ASEC 2025")
    d = read_cps()
    _ok(f"CPS read; canonical union {d.loc[d.target, 'pwwgt0'].sum():,.2f} people (builder's check)")
    w = d.pwwgt0.to_numpy(float)
    exp_ = d.exposure.to_numpy()
    civ = d.civilian.to_numpy()
    tgt = d.target.to_numpy()
    cell_of = list(zip(d.tband, d.born))
    key = {c: means[c].reindex(pd.MultiIndex.from_tuples(cell_of)).to_numpy() for c in means.columns}
    if any(np.isnan(v).any() for v in key.values()):
        fail("a CPS record fell outside the MEPS donor cells")

    # gate A: the account's incidence keys
    ik = pd.read_csv(ACCOUNT / "derived/incidence_keys.csv")
    ik = ik[ik.allocation.eq("personal")].set_index("key")
    gates_a = {}
    for line, (kname, cols, _) in ACCOUNT_LINES.items():
        col = "health_other" if kname == "health_other" else cols[0]
        v = key[col] * exp_
        nat_total, tgt_total = float((v * w)[civ].sum()), float((v * w)[tgt].sum())
        for lab, got, want in [("national", nat_total, ik.loc[kname, "national_key_total"]),
                               ("target", tgt_total, ik.loc[kname, "target_key_total"])]:
            if abs(got / want - 1) > 1e-9:
                fail(f"account key {kname} {lab}: {got:,.0f} vs incidence_keys.csv {want:,.0f}")
        gates_a[kname] = {"national": nat_total, "target": tgt_total}
    _ok("account keys reproduce incidence_keys.csv to 1e-9 for all five medical keys "
        f"(Medicaid target {gates_a['medicaid']['target']/1e9:.3f}bn of {gates_a['medicaid']['national']/1e9:.3f}bn)")

    # gate B: the ledger's union medical and M by ledger band
    params = json.loads((LEDGER / "params/params.json").read_text())["meps_coverage"]
    r_mcd = params["nhea_to_meps_ratio_medicaid"]["value"]
    r_mcr = params["nhea_to_meps_ratio_medicare"]["value"]
    comp = pd.read_csv(LEDGER / "derived/age_profile_components.csv")
    comp = comp[(comp.allocation == "personal") & (comp.account == "expanded")
                & (comp.group == "mexican_observed_total")]
    med_led = comp[comp.component == "medical"].set_index("band").signed_total
    m_led = comp[comp.component == "M"].set_index("band").signed_total
    med_rec = key["public_transport"] * exp_
    m_rec = (key["TOTMCD"] * (r_mcd - 1) + key["TOTMCR"] * (r_mcr - 1)) * exp_
    worst = 0.0
    for b in range(8):
        sel = tgt & (d.lband.to_numpy() == b)
        got_med, got_m = -float((w * med_rec)[sel].sum()), -float((w * m_rec)[sel].sum())
        worst = max(worst, abs(got_med - med_led.loc[b]), abs(got_m - m_led.loc[b]))
    if worst > 1.0:
        fail(f"ledger union medical/M by band not reproduced; worst residual ${worst:,.2f}")
    audit["gates"] = {"account_keys": gates_a, "ledger_band_worst_abs_residual_usd": worst,
                      "ledger_medical_total_bn": float(med_led.sum()) / 1e9,
                      "ledger_M_total_bn": float(m_led.sum()) / 1e9,
                      "nhea_ratios": {"medicaid": r_mcd, "medicare": r_mcr}}
    _ok(f"ledger union medical ({med_led.sum()/1e9:+.3f}bn) and M ({m_led.sum()/1e9:+.3f}bn) reproduce "
        f"in all eight bands (worst residual ${worst:.2f})")

    # cell-level dollar weights for the union
    rows = []
    for b in range(5):
        for born in (1, 2):
            sel = tgt & (d.tband.to_numpy() == b) & (d.born.to_numpy() == born)
            n = float((w * exp_)[sel].sum())
            mc = means.loc[(b, born)]
            rows.append(dict(band=TRANSPORT_LABELS[b], nativity=NAT[born], union_persons=float(w[sel].sum()),
                             union_exposed=n, meps2024_public=mc.public_transport, meps2024_medicaid=mc.TOTMCD,
                             meps2024_medicare=mc.TOTMCR, meps2024_va=mc.TOTVA, meps2024_tricare=mc.TOTTRI,
                             meps2024_health_other=mc.health_other,
                             ledger_medical_cost=n * mc.public_transport,
                             ledger_M_cost=n * (mc.TOTMCD * (r_mcd - 1) + mc.TOTMCR * (r_mcr - 1)),
                             key_medicaid=n * mc.TOTMCD, key_medicare=n * mc.TOTMCR,
                             key_health_other=n * mc.health_other, key_tricare=n * mc.TOTTRI,
                             key_va_medical=n * mc.TOTVA))
    cells = pd.DataFrame(rows)
    if abs(cells.ledger_medical_cost.sum() + med_led.sum()) > 1 or abs(cells.ledger_M_cost.sum() + m_led.sum()) > 1:
        fail("transport-cell charges do not sum to the ledger totals")
    cells.to_csv(DERIVED / "cps_cells.csv", index=False)

    alloc = pd.read_csv(ACCOUNT / "derived/allocations.csv")
    alloc = alloc[(alloc.scenario_id == "complete_preferred_F_per_capita") & (alloc.allocation == "personal")
                  ].set_index("category")
    line_bn = {line: float(alloc.loc[line, "target_bn"]) for line in ACCOUNT_LINES}
    if abs(line_bn["medicaid_and_chip_other_medical"] - 116.91) > 0.005:
        fail(f"preferred Medicaid/CHIP/other medical line is {line_bn['medicaid_and_chip_other_medical']}, not 116.91")
    audit["account_lines_bn"] = line_bn

    ests = pickle.load(open(CACHE / "cell_ests.pkl", "rb"))
    design = ests["pooled_design"]
    store = ests["pooled"]

    def get(spec, measure, b, nat):
        k = (spec, measure, TRANSPORT_LABELS[b], nat)
        if k not in store:
            fail(f"missing cell estimate {k}")
        return store[k]

    line_store = {}  # label -> design and each account line's (target $bn, key-weighted ratio, influence)

    def sums(spec_get, design_, label):
        """Ledger and account deltas for one set of cell ratios."""
        out_led, out_acc = [], []
        combos = [(grp, bands, (1, 2), "both") for grp, bands in AGE_GROUPS.items()]
        combos += [("all ages", AGE_GROUPS["all ages"], (1,), "us_born"),
                   ("all ages", AGE_GROUPS["all ages"], (2,), "foreign_born")]
        for grp, bands, borns, natlab in combos:
            parts_med, parts_mcd, parts_mcr, parts_tr = [], [], [], []
            for b in bands:
                for born in borns:
                    c = cells[(cells.band == TRANSPORT_LABELS[b]) & (cells.nativity == NAT[born])].iloc[0]
                    rp = spec_get("public", b, NAT[born])
                    rt = spec_get("public_transport", b, NAT[born])
                    rd = spec_get("medicaid", b, NAT[born])
                    rr = spec_get("medicare", b, NAT[born])
                    parts_med.append((c.ledger_medical_cost, rp))
                    parts_tr.append((c.ledger_medical_cost, rt))
                    parts_mcd.append((c.union_exposed * c.meps2024_medicaid * (r_mcd - 1), rd))
                    parts_mcr.append((c.union_exposed * c.meps2024_medicare * (r_mcr - 1), rr))

            def delta(parts):
                live = [(a, e) for a, e in parts if a != 0]
                if any(not np.isfinite(e.value) for _, e in live):
                    return Est(float("nan"), np.zeros(design_.n_psu))
                return combo([(a, e) for a, e in live]) if live else Est(0.0, np.zeros(design_.n_psu))
            base_med = sum(a for a, _ in parts_med)
            base_m = sum(a for a, _ in parts_mcd) + sum(a for a, _ in parts_mcr)
            e_med = delta(parts_med)
            e_tr = delta(parts_tr)
            e_m = delta(parts_mcd + parts_mcr)
            dm = Est(e_med.value - base_med, e_med.T)
            dt = Est(e_tr.value - base_med, e_tr.T)
            dM = Est(e_m.value - base_m, e_m.T)
            dtot = Est(dm.value + dM.value, dm.T + dM.T)
            for comp_, e, base in [("medical", dm, base_med), ("medical_transport_payers", dt, base_med),
                                   ("M", dM, base_m), ("medical+M", dtot, base_med + base_m)]:
                se = float(np.sqrt(design_.var(e.T))) if np.isfinite(e.value) else np.nan
                out_led.append(dict(spec=label, age_group=grp, nativity=natlab, component=comp_,
                                    ledger_cost_bn=base / 1e9,
                                    delta_cost_bn=e.value / 1e9, se_bn=se / 1e9,
                                    ci_lo_bn=(e.value - Z95 * se) / 1e9, ci_hi_bn=(e.value + Z95 * se) / 1e9,
                                    implied_ratio=(base + e.value) / base if base else np.nan))
        acc_terms = []
        for line, (kname, cols, measure) in ACCOUNT_LINES.items():
            kcol = f"key_{kname}"
            total_key = cells[kcol].sum()
            parts = []
            for b in range(5):
                for born in (1, 2):
                    c = cells[(cells.band == TRANSPORT_LABELS[b]) & (cells.nativity == NAT[born])].iloc[0]
                    parts.append((c[kcol] / total_key, spec_get(measure, b, NAT[born])))
            live = [(a, e) for a, e in parts if a > 0]
            if any(not np.isfinite(e.value) for _, e in live):
                continue
            e = combo(live)                       # key-weighted mean ratio
            factor = e.value
            se_f = float(np.sqrt(design_.var(e.T)))
            tb = line_bn[line]
            other = float(ik.loc[kname, "other_key_total"])
            renorm_share = factor * total_key / (factor * total_key + other)
            base_share = total_key / (total_key + other)
            out_acc.append(dict(spec=label, line=line, key=kname, meps_payer_ratio=measure,
                                account_target_bn=tb, key_weighted_ratio=factor, se_ratio=se_f,
                                delta_bn=tb * (factor - 1), se_bn=tb * se_f,
                                ci_lo_bn=tb * (factor - 1 - Z95 * se_f), ci_hi_bn=tb * (factor - 1 + Z95 * se_f),
                                delta_bn_renormalized=tb * (renorm_share / base_share - 1)))
            acc_terms.append((tb, e))
            line_store.setdefault(label, {"design": design_, "lines": {}})["lines"][line] = (tb, e.value, e.T)
        if len(acc_terms) == len(ACCOUNT_LINES):
            tot_v = sum(tb * (e.value - 1) for tb, e in acc_terms)
            tot_T = sum(tb * e.T for tb, e in acc_terms)
            se_t = float(np.sqrt(design_.var(tot_T)))
            out_acc.append(dict(spec=label, line="all five medical lines", key="", meps_payer_ratio="",
                                account_target_bn=sum(tb for tb, _ in acc_terms), key_weighted_ratio=np.nan,
                                se_ratio=np.nan, delta_bn=tot_v, se_bn=se_t, ci_lo_bn=tot_v - Z95 * se_t,
                                ci_hi_bn=tot_v + Z95 * se_t, delta_bn_renormalized=np.nan))
        return out_led, out_acc

    _header("translate")
    led_rows, acc_rows = [], []
    for spec in SPECS:
        if spec in ("plain", "winsor_p995", "winsor_p999", "two_part_lognormal"):
            def spec_get(measure, b, nat, spec=spec):
                if spec == "two_part_lognormal" and measure not in ("public", "medicare", "medicaid", "other_public"):
                    return get("plain", measure, b, nat)
                if spec.startswith("winsor") and measure not in ("public", "public_transport", "medicare",
                                                                 "medicaid", "other_public", "va", "tricare"):
                    return get("plain", measure, b, nat)
                if spec == "two_part_lognormal" and measure == "public_transport":
                    return get("plain", measure, b, nat)
                return get(spec, measure, b, nat)
        else:
            def spec_get(measure, b, nat, spec=spec):
                return get(spec, measure, b, nat)
        lr, ar = sums(spec_get, ests["sample_designs"].get(spec, design), spec)
        led_rows += lr
        acc_rows += ar
        tot = [r for r in lr if r["age_group"] == "all ages" and r["nativity"] == "both"
               and r["component"] == "medical+M"][0]
        mcd = [r for r in ar if r["line"] == "medicaid_and_chip_other_medical"][0]
        mcr = [r for r in ar if r["line"] == "medicare"][0]
        _ok(f"{spec}: ledger medical+M {tot['delta_cost_bn']:+.2f}bn (SE {tot['se_bn']:.2f}); account Medicaid "
            f"{mcd['delta_bn']:+.2f}bn (SE {mcd['se_bn']:.2f}), Medicare {mcr['delta_bn']:+.2f}bn (SE {mcr['se_bn']:.2f})")

    _header("translate year by year (each year's own design)")
    yr_rows = []
    for yspec in ("plain", "winsor_p995"):
        for yv in range(2016, 2025):
            ydes = ests["year_designs"][yv]
            ystore = ests["by_year"]

            def year_get(measure, b, nat, yv=yv, yspec=yspec):
                m = "public" if measure == "public_transport" else measure
                return ystore[(yspec, yv, m, TRANSPORT_LABELS[b], nat)]
            lr, ar = sums(year_get, ydes, f"{yspec}_year_{yv}")
            for r in lr + ar:
                r["year"], r["year_spec"] = yv, yspec
            yr_rows += [r for r in lr if r["component"] in ("medical", "M", "medical+M")] + ar
            tot = [r for r in lr if r["age_group"] == "all ages" and r["nativity"] == "both"
                   and r["component"] == "medical+M"][0]
            mcd = [r for r in ar if r["line"] == "medicaid_and_chip_other_medical"]
            mcr = [r for r in ar if r["line"] == "medicare"]
            _ok(f"{yspec} {yv}: ledger medical+M {tot['delta_cost_bn']:+.2f}bn (SE {tot['se_bn']:.2f})"
                + (f"; account Medicaid {mcd[0]['delta_bn']:+.2f}bn" if mcd else "")
                + (f", Medicare {mcr[0]['delta_bn']:+.2f}bn" if mcr else ""))

    pd.DataFrame(led_rows).to_csv(DERIVED / "translation_ledger.csv", index=False)
    pd.DataFrame(acc_rows).to_csv(DERIVED / "translation_account.csv", index=False)
    pd.DataFrame(yr_rows).to_csv(DERIVED / "translation_by_year.csv", index=False)
    with open(CACHE / "account_line_ests.pkl", "wb") as fh:   # bounds.py combines lines with exact SEs
        pickle.dump(line_store, fh)
    audit["inputs"] = {p.name: {"path": str(p), "sha256": sha256(p)} for p in [
        CPS_ZIP, LEDGER / "params/params.json", LEDGER / "derived/age_profile_components.csv",
        ACCOUNT / "derived/incidence_keys.csv", ACCOUNT / "derived/allocations.csv", CACHE / "pooled.parquet"]}
    audit["sign_convention"] = ("delta_cost_bn / delta_bn = corrected cost minus current cost; negative means "
                                "the account charges the union more than Mexican-origin donors in the same "
                                "cells draw")
    (DERIVED / "translation_audit.json").write_text(json.dumps(audit, indent=2, default=float) + "\n")
    _ok("translation_ledger.csv, translation_account.csv, translation_by_year.csv, cps_cells.csv written")


if __name__ == "__main__":
    main()
