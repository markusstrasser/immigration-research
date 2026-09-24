"""Old -> new for every number this lane moved (BRIEF.md task 5).

Old values come from the committed files (git HEAD) of the lanes this lane re-ran, or from the
September 23 column of this lane's own outputs; new values from the working tree. Nothing is typed
in: every value is selected from a file named in the row. Writes derived/old_new.csv and prints the
table as Markdown for RESULT.md.

Run from the repository root, after the lanes and real_costs_totals.py have run:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/sept24_propagation_2026_09_24/old_new.py
"""
from __future__ import annotations

import csv
import io
import json
import subprocess
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
F = "infra/immigration-fiscal/"
DEBT, DIST, UNC = F + "debt_legacy_2026_09_23/derived/", F + "distribution_weights_2026_09_23/derived/", \
    F + "uncertainty_propagation_2026_09_22/derived/"
ROWS: list[dict] = []


def head(rel: str) -> bytes:
    out = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ROOT, capture_output=True)
    if out.returncode:
        raise SystemExit(f"[BLOCKED] {rel} not at HEAD")
    return out.stdout


def both_csv(rel):
    return pd.read_csv(io.BytesIO(head(rel))), pd.read_csv(ROOT / rel)


def add(group, quantity, unit, old, new, new_file, old_source="git HEAD", scale=1.0):
    old = old if isinstance(old, tuple) else (old, None)
    new = new if isinstance(new, tuple) else (new, None)
    f = lambda x: None if x is None else float(x) * scale  # noqa: E731
    ROWS.append(dict(group=group, quantity=quantity, unit=unit, old_low=f(old[0]), old_high=f(old[1]),
                     new_low=f(new[0]), new_high=f(new[1]), new_file=new_file, old_source=old_source))


def pick(df, **kw):
    m = pd.Series(True, index=df.index)
    for k, v in kw.items():
        m &= df[k] == v
    return df[m]


def ends(df, col, **kw):
    r = pick(df, **kw).set_index("end")
    if len(r) != 2:
        raise SystemExit(f"[BLOCKED] expected two band ends for {kw}, got {len(r)}")
    return float(r.loc["low", col]), float(r.loc["high", col])


def span(df, col, **kw):
    r = pick(df, **kw)
    return float(r[col].min()), float(r[col].max())


def main_case():
    """The case itself, for the lines that quote it beside the numbers below (moved by main_case_2026_09_24)."""
    g = "main case (reference)"
    b23 = pd.read_csv(ROOT / (F + "main_case_2026_09_23/derived/main_case_bands.csv"))
    b23 = b23[(b23.profile == "cbo_category_lag_non_school_full") & (b23.variant == "adopted")].iloc[0]
    s24 = json.loads((ROOT / (F + "main_case_2026_09_24/derived/summary.json")).read_text())
    pop = json.loads((HERE / "derived" / "band_variants.json").read_text())["target_population"]
    src = F + "main_case_2026_09_24/derived/summary.json"
    add(g, "fiscal main case", "$bn", (b23.cost_low_bn, b23.cost_high_bn), tuple(s24["main_case"]), src,
        "main_case_2026_09_23/derived/main_case_bands.csv")
    add(g, "fiscal main case per group member", "$", (b23.per_member_low, b23.per_member_high),
        tuple(x * 1e9 / pop for x in s24["main_case"]), src, "main_case_2026_09_23/derived/main_case_bands.csv")


def debt():
    g = "debt legacy"
    so, sn = both_csv(DEBT + "stocks.csv")
    fo, fn = both_csv(DEBT + "federal_split_2024.csv")
    po, pn = both_csv(DEBT + "forward_path.csv")
    bo, bn = both_csv(DEBT + "benefit_sensitivity.csv")
    wo, wn = both_csv(DEBT + "adopted_backcast_windows.csv")
    main = dict(profile="cbo_category_lag_non_school_full")
    add(g, "federal part of the 2024 fiscal gap, central convention", "$bn", ends(fo, "federal_bn", convention="central", **main),
        ends(fn, "federal_bn", convention="central", **main), DEBT + "federal_split_2024.csv")
    for conv in ("central", "low", "high"):
        add(g, f"federal share of the 2024 gap, {conv} convention", "%", ends(fo, "federal_share", convention=conv, **main),
            ends(fn, "federal_share", convention=conv, **main), DEBT + "federal_split_2024.csv", scale=100)
    c = dict(benchmark="main", rule="programme_income_pandemic_per_head", convention="central", rate_path="effective",
             window_start=2005, financing="all_borrowed")
    for col, label, unit, sc in (("stock_entering_2024_bn", "legacy stock entering 2024", "$bn", 1),
                                 ("stock_share_of_debt_end_fy2023", "stock, share of debt at end FY2023", "%", 100),
                                 ("legacy_interest_2024_bn", "legacy interest, 2024", "$bn", 1),
                                 ("interest_per_member_usd", "interest per group member", "$", 1),
                                 ("interest_per_other_resident_usd", "interest per other resident", "$", 1),
                                 ("interest_share_of_fy2024_net_interest", "interest, share of FY2024 net interest", "%", 100),
                                 ("interest_share_of_account_interest_allocation", "interest over the account's interest row allocation", "ratio", 1)):
        add(g, label + " (central rule)", unit, ends(so, col, **c), ends(sn, col, **c), DEBT + "stocks.csv", scale=sc)
    rules = {k: v for k, v in c.items() if k != "rule"}
    add(g, "legacy interest across back-cast rules, central convention", "$bn", span(so, "legacy_interest_2024_bn", **rules),
        span(sn, "legacy_interest_2024_bn", **rules), DEBT + "stocks.csv")
    add(g, "legacy stock across back-cast rules, central convention", "$tn", span(so, "stock_entering_2024_bn", **rules),
        span(sn, "stock_entering_2024_bn", **rules), DEBT + "stocks.csv", scale=1e-3)
    conv = {k: v for k, v in rules.items() if k != "convention"}
    add(g, "legacy interest across rules and payer conventions", "$bn", span(so, "legacy_interest_2024_bn", **conv),
        span(sn, "legacy_interest_2024_bn", **conv), DEBT + "stocks.csv")
    add(g, "legacy interest, every specification", "$bn", span(so, "legacy_interest_2024_bn", benchmark="main"),
        span(sn, "legacy_interest_2024_bn", benchmark="main"), DEBT + "stocks.csv")
    add(g, "legacy interest, central rule, every specification", "$bn",
        span(so, "legacy_interest_2024_bn", benchmark="main", rule=c["rule"]),
        span(sn, "legacy_interest_2024_bn", benchmark="main", rule=c["rule"]), DEBT + "stocks.csv")
    for k, v, label in (("convention", "low", "low payer convention"), ("convention", "high", "high payer convention"),
                        ("rate_path", "constant_3_22", "constant 3.22% rate"), ("rate_path", "treasury_10y", "10-year Treasury rate"),
                        ("rate_path", "gross_public_securities", "public securities rate"), ("window_start", 2010, "window from 2010"),
                        ("window_start", 2015, "window from 2015"), ("financing", "half_borrowed", "half borrowed"),
                        ("benchmark", "proportional", "proportional benchmark")):
        spec = {**c, k: v}
        add(g, f"legacy interest, {label}", "$bn", ends(so, "legacy_interest_2024_bn", **spec),
            ends(sn, "legacy_interest_2024_bn", **spec), DEBT + "stocks.csv")
    for old_set, new_set in (("care_and_mobility", "mobility"), ("care_mobility_and_scale", "mobility_and_scale")):
        o, n = pick(bo, benefit_set=old_set, window_start=2005).iloc[0], pick(bn, benefit_set=new_set, window_start=2005).iloc[0]
        for col, label in (("federal_2024_bn", "federal 2024"), ("stock_reduction_bn", "stock reduction"),
                           ("interest_reduction_2024_bn", "interest reduction 2024")):
            add(g, f"omitted benefits {old_set} -> {new_set}: {label}", "$bn", o[col], n[col], DEBT + "benefit_sensitivity.csv")
    for years in (10, 20, 30):
        spec = dict(part="federal", convention="central", financing="all_borrowed", years=years)
        add(g, f"forward federal debt from the 2024 gap, {years} years", "$bn", ends(po, "debt_bn", **spec),
            ends(pn, "debt_bn", **spec), DEBT + "forward_path.csv")
    spec = dict(part="whole_gap", convention="none", financing="all_borrowed", years=10)
    add(g, "forward debt if the whole gap were borrowed, 10 years", "$tn", ends(po, "debt_bn", **spec),
        ends(pn, "debt_bn", **spec), DEBT + "forward_path.csv", scale=1e-3)
    for rule in ("programme", "programme_income"):
        for w in (2015, 2010, 2005):
            spec = dict(benchmark="main", rule=rule, receipts_method="own_series", window_start=w)
            add(g, f"back-cast net cost, {rule}, {w}-2024", "$tn", ends(wo, "net_cost_tn", **spec),
                ends(wn, "net_cost_tn", **spec), DEBT + "adopted_backcast_windows.csv")


def distribution():
    g = "distribution (ladder 194)"
    qo, qn = both_csv(DIST + "channel_by_quintile.csv")
    wo, wn = both_csv(DIST + "weighted_totals.csv")
    qo, qn = qo[qo.measure == "spm"], qn[qn.measure == "spm"]
    wo, wn = wo[wo.measure == "spm"], wn[wn.measure == "spm"]
    val = lambda q, ch, k, col="bn": float(q[(q.channel == ch) & (q.quintile == k)][col].iloc[0])  # noqa: E731
    src = DIST + "channel_by_quintile.csv"
    add(g, "fiscal cost channel, A_mid + F_c (negative = cost)", "$bn", val(qo, "fiscal_a", 0), val(qn, "fiscal_a", 0), src)
    for k in range(1, 6):
        add(g, f"fiscal cost, tax-share financing, fifth {k}", "$bn", val(qo, "fiscal_a", k), val(qn, "fiscal_a", k), src)
    add(g, "fiscal cost, per-person cuts, each fifth", "$bn", val(qo, "fiscal_b", 1), val(qn, "fiscal_b", 1), src)
    add(g, "fiscal cost, top fifth's part under tax-share financing", "%", val(qo, "fiscal_a", 5) / val(qo, "fiscal_a", 0),
        val(qn, "fiscal_a", 5) / val(qn, "fiscal_a", 0), src, scale=100)
    add(g, "fiscal cost under per-person cuts, share of resources, bottom and top fifth", "%",
        (val(qo, "fiscal_b", 1, "pct_of_resources"), val(qo, "fiscal_b", 5, "pct_of_resources")),
        (val(qn, "fiscal_b", 1, "pct_of_resources"), val(qn, "fiscal_b", 5, "pct_of_resources")), src)
    add(g, "central total with the social items (TOTAL)", "$bn", val(qo, "TOTAL_a", 0), val(qn, "TOTAL_a", 0), src)
    for conv, label in (("a", "tax-share"), ("b", "per-person")):
        add(g, f"central total, share of resources, bottom and top fifth, {label}", "%",
            (val(qo, f"TOTAL_{conv}", 1, "pct_of_resources"), val(qo, f"TOTAL_{conv}", 5, "pct_of_resources")),
            (val(qn, f"TOTAL_{conv}", 1, "pct_of_resources"), val(qn, f"TOTAL_{conv}", 5, "pct_of_resources")), src)
    wv = lambda w, ch, col: float(w[(w.channel == ch) & (w.eta == 1.3)][col].iloc[0])  # noqa: E731
    for conv, label in (("a", "tax-share"), ("b", "per-person")):
        add(g, f"central total at eta 1.3, equal-split equivalent, {label}", "$bn", wv(wo, f"TOTAL_{conv}", "equal_split_p5"),
            wv(wn, f"TOTAL_{conv}", "equal_split_p5"), DIST + "weighted_totals.csv")
        add(g, f"central total at eta 1.3, mean-normalized, {label}", "$bn", wv(wo, f"TOTAL_{conv}", "person_p5"),
            wv(wn, f"TOTAL_{conv}", "person_p5"), DIST + "weighted_totals.csv")
    outside = ["wages", "housing_net", "crime", "unreimbursed_care"]
    s = lambda q, ks: sum(val(q, ch, k) for ch in outside for k in ks)  # noqa: E731
    add(g, "outside the budget: bottom four fifths, top fifth (unchanged)", "$bn", (s(qo, [1, 2, 3, 4]), s(qo, [5])),
        (s(qn, [1, 2, 3, 4]), s(qn, [5])), src)


def real_costs():
    g = "real-costs totals (memo §7, §7b)"
    r = pd.read_csv(HERE / "derived" / "real_costs_totals.csv")
    src = F + "sept24_propagation_2026_09_24/derived/real_costs_totals.csv"
    for (section, column), part in r.groupby(["section", "column"], sort=False):
        items = part.item.str.replace(r" \((low|high)\)$", "", regex=True)
        for item in dict.fromkeys(items):
            rows = part[items == item]
            lo = rows[rows.item.str.endswith("(low)") | ~rows.item.str.contains(r"\((?:low|high)\)$")]
            hi = rows[rows.item.str.endswith("(high)")]
            o = (lo.sept23.iloc[0], hi.sept23.iloc[0] if len(hi) else None)
            n = (lo.sept24.iloc[0], hi.sept24.iloc[0] if len(hi) else None)
            unit = {"bn": "$bn"}.get(rows.unit.iloc[0], rows.unit.iloc[0])
            add(g, f"§{section} {column}: {item}", unit, o, n, src,
                old_source="this lane, Sept 23 column (memo arithmetic reproduced)")


def uncertainty():
    g = "uncertainty (ladder 184)"
    cu = pd.read_csv(ROOT / (UNC + "case_uncertainty.csv"))
    main = cu[cu.profile == "cbo_category_lag_non_school_full"]
    s = json.loads((ROOT / (UNC + "sept24/summary.json")).read_text())
    src = UNC + "sept24/summary.json"
    old = "Sept 20 main band, case_uncertainty.csv"
    add(g, "per-case SE, sources independent", "$bn",
        (main.se_combined_independent_bn.min(), main.se_combined_independent_bn.max()), tuple(s["sept24"]["se_independent_bn"]), src, old)
    add(g, "per-case SE, all positively correlated", "$bn",
        (main.se_all_positive_correlation_bn.min(), main.se_all_positive_correlation_bn.max()),
        tuple(s["sept24"]["se_positive_correlation_bn"]), src, old)
    add(g, "95% intervals of the main band's cases, union", "$bn", (main.ci95_low_bn.min(), main.ci95_high_bn.max()),
        tuple(s["sept24"]["ci95_union_bn"]), src, old)
    add(g, "95% intervals at the correlated upper bound, union", "$bn",
        (main.ci95_envelope_low_bn.min(), main.ci95_envelope_high_bn.max()), tuple(s["sept24"]["ci95_envelope_union_bn"]), src, old)
    add(g, "95% intervals with the benefit keys' SE, union", "$bn", None, tuple(s["sept24"]["ci95_with_benefit_keys_union_bn"]), src,
        "not computed before")
    add(g, "per-case SE on the Sept 23 case (never published) -> Sept 24", "$bn", tuple(s["sept23"]["se_independent_bn"]),
        tuple(s["sept24"]["se_independent_bn"]), src, "sept24/summary.json, sept23 block")
    add(g, "95% union on the Sept 23 case (never published) -> Sept 24", "$bn", tuple(s["sept23"]["ci95_union_bn"]),
        tuple(s["sept24"]["ci95_union_bn"]), src, "sept24/summary.json, sept23 block")


def fmt(lo, hi, unit):
    if lo is None or pd.isna(lo):
        return "—"
    d = 0 if unit == "$" or abs(lo) >= 1000 else (2 if unit in ("ratio",) or abs(lo) < 10 else 1)
    if hi is not None and not pd.isna(hi) and hi != lo and f"{lo:.{d}f}" == f"{hi:.{d}f}":
        d += 1                        # a range that rounds to one value shows one more decimal
    s = f"{lo:,.{d}f}"
    return s if hi is None or pd.isna(hi) else f"{s} to {hi:,.{d}f}"


def main():
    main_case()
    debt()
    distribution()
    real_costs()
    uncertainty()
    out = HERE / "derived" / "old_new.csv"
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(ROWS[0]), lineterminator="\n")
        w.writeheader()
        for r in ROWS:
            w.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in r.items()})
    group = None
    for r in ROWS:
        if r["group"] != group:
            group = r["group"]
            print(f"\n**{group}**\n\n| Quantity | Unit | Old | New | File |\n|---|---|---:|---:|---|")
        print(f"| {r['quantity']} | {r['unit']} | {fmt(r['old_low'], r['old_high'], r['unit'])} | "
              f"{fmt(r['new_low'], r['new_high'], r['unit'])} | `{r['new_file'].replace(F, '')}` |")
    print(f"\n{len(ROWS)} rows -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
