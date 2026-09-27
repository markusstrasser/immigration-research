"""Old -> new for every number W1's four lanes publish (back-cast, debt legacy, distribution, uncertainty).

Old values are the files committed at OLD, the September 24 runs of all four lanes. New values are the
case given by --case (default sept26_schools), with --middle (default sept26; "none" drops it) as a
column between. Nothing is typed in: every value is selected from the lane file named in its row.

Every later column is read from commits, never from the working tree: since 2026-09-27 the lanes' working
trees hold the September 27 case. TABLE is the commit at which this table was last written, when the
lanes' committed files held the schools case.

  back-cast     backcast_windows.csv at TABLE holds every case's concepts; a case's concept tag comes
                from backcast.py's LATER_CASES at TABLE (parsed, not imported).
  uncertainty   derived/<case>/summary.json at TABLE.
  distribution, debt legacy
                rebuilt with `--case X --out-dir <tmp>`. Each rebuilt file must equal the lane's file at
                its commit of that case (PINS; gate), so the table shows the committed runs.
  main case     each case lane's derived/summary.json at TABLE.

Writes derived/old_new_lanes.csv (LF) and prints the table as Markdown. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/sept26_propagation_2026_09_26/old_new_lanes.py
"""
from __future__ import annotations

import argparse
import ast
import csv
import io
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OLD = "e5e23ec"                       # the four lanes' September 24 runs, before any September 26 change
TABLE = "90c4b23"                     # this table's last write; the lanes' committed files held the schools case
F = "infra/immigration-fiscal/"
BC, DEBT, DIST, UNC = (F + "historical_backcast_2026_09_20/", F + "debt_legacy_2026_09_23/",
                       F + "distribution_weights_2026_09_23/", F + "uncertainty_propagation_2026_09_22/")
# The debt and distribution lanes' commits of each later case: a rebuild must equal these files.
PINS = {"sept26": {DEBT: "e62fccb", DIST: "f697514"}, "sept26_schools": {DEBT: "90c4b23", DIST: "39b854b"}}
LABELS = {"sept24": "Sept 24", "sept26": "Sept 26, CBO's one-year school response (0.63–0.66)",
          "sept26_schools": "Sept 26, schools at full cost"}
MAIN = "cbo_category_lag_non_school_full"
ROWS: list[dict] = []


def git_bytes(rel: str, commit: str = OLD, missing_ok: bool = False) -> bytes | None:
    out = subprocess.run(["git", "show", f"{commit}:{rel}"], cwd=ROOT, capture_output=True)
    if out.returncode:
        if missing_ok:
            return None
        raise SystemExit(f"[BLOCKED] {rel} not at {commit}")
    return out.stdout


def backcast_cases() -> dict:
    """backcast.py's LATER_CASES at TABLE, parsed as a literal rather than imported."""
    for node in ast.parse(git_bytes(BC + "backcast.py", TABLE).decode()).body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "LATER_CASES" for t in node.targets):
            return ast.literal_eval(node.value)
    raise SystemExit(f"[BLOCKED] no LATER_CASES in {BC}backcast.py at {TABLE}")


LATER = backcast_cases()               # case -> (main-case lane, concept tag, base variant, base tag)
if set(LATER) != set(PINS):
    raise SystemExit(f"[BLOCKED] LATER_CASES at {TABLE} ({sorted(LATER)}) and PINS ({sorted(PINS)}) differ")


class View:
    """One column: the lane files that hold one case."""

    def __init__(self, case: str, tmp: Path):
        self.case = case
        if case == "sept24":
            self.read = git_bytes
            self.tag, self.main_lane = "corrected", "main_case_2026_09_24"
            self.unc = json.loads(git_bytes(UNC + "derived/sept24/summary.json"))["sept24"]
            self.source = f"git {OLD}"
            return
        self.main_lane, tag = LATER[case][0], LATER[case][1]
        self.tag = tag.strip("_")
        self.unc = json.loads(git_bytes(UNC + f"derived/{case}/summary.json", TABLE))
        built = {DEBT: rebuild(DEBT + "debt_legacy.py", case, tmp / f"debt_{case}", PINS[case][DEBT]),
                 DIST: rebuild(DIST + "distribute.py", case, tmp / f"dist_{case}", PINS[case][DIST])}

        def read(rel: str) -> bytes:
            for lane, d in built.items():
                if rel.startswith(lane + "derived/"):
                    return (d / rel[len(lane + "derived/"):]).read_bytes()
            return git_bytes(rel, TABLE)
        self.read = read
        self.source = f"--case {case}"

    def csv(self, rel: str) -> pd.DataFrame:
        return pd.read_csv(io.BytesIO(self.read(rel)))

    def json(self, rel: str) -> dict:
        return json.loads(self.read(rel))

    def summary(self) -> dict:
        return json.loads(git_bytes(F + self.main_lane + "/derived/summary.json", TABLE))


def rebuild(script: str, case: str, out: Path, commit: str) -> Path:
    """The lane's files on one case, in `out`. Gate: each equals the lane's file at `commit`, its run of the case."""
    run = subprocess.run([sys.executable, str(ROOT / script), "--case", case, "--out-dir", str(out)], cwd=ROOT,
                         env={**os.environ, "OPENBLAS_NUM_THREADS": "1"}, capture_output=True, text=True)
    if run.returncode:
        raise SystemExit(f"[BLOCKED] {script} --case {case} failed:\n{run.stderr[-2000:]}")
    derived = str(Path(script).parent) + "/derived/"
    files = sorted(out.iterdir())
    differ = [f.name for f in files if git_bytes(derived + f.name, commit, missing_ok=True) != f.read_bytes()]
    if differ:
        raise SystemExit(f"[BLOCKED] {script} --case {case} differs from {commit} in {differ}")
    print(f"  ✓ {script} --case {case}: {len(files)} files, equal to {commit}")
    return out


def add(group, quantity, unit, file, getter, scale=1.0):
    """getter(view) -> value, (low, high) or None; one row with every view's values."""
    row = dict(group=group, quantity=quantity, unit=unit, file=file)
    for name, view in VIEWS.items():
        v = getter(view)
        lo, hi = (v if isinstance(v, tuple) else (v, None))
        f = lambda x: None if x is None else float(x) * scale  # noqa: E731
        row[f"{name}_low"], row[f"{name}_high"] = f(lo), f(hi)
    ROWS.append(row)


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
    if r.empty:
        raise SystemExit(f"[BLOCKED] no rows for {kw}")
    return float(r[col].min()), float(r[col].max())


def main_case():
    g = "main case (reference)"
    add(g, "fiscal main case", "$bn", "<case lane>/derived/summary.json", lambda v: tuple(v.summary()["main_case"]))
    add(g, "group receipts, reference incidence rule (shared allocation)", "$bn", "<case lane>/derived/summary.json",
        lambda v: v.summary()["group_receipts_bn"]["adopted"]["shared"])


def backcast():
    g = "back-cast (ladder 162, 219)"
    src = BC + "derived/backcast_windows.csv"
    for prefix, label in (("net_cost_cbo_informed", "main case"), ("net_cost_full_proportional", "proportional benchmark")):
        def family(v):
            w = v.csv(src)
            rows = w[w.concept.str.startswith(f"{prefix}_{v.tag}_")]
            if len(rows) != 6:
                raise SystemExit(f"[BLOCKED] expected six rows for {prefix}_{v.tag}")
            return rows
        for col, w in (("10y_2015_2024", "2015-2024"), ("15y_2010_2024", "2010-2024"), ("20y_2005_2024", "2005-2024")):
            add(g, f"{label}, whole-budget rules, {w}", "$tn", src,
                lambda v, col=col: (family(v)[col].min(), family(v)[col].max()))
        for rule in ("flat", "ratio", "income"):
            def by_rule(v, rule=rule):
                r = family(v).query("rule == @rule").set_index("concept")["10y_2015_2024"]
                return r[f"{prefix}_{v.tag}_low"], r[f"{prefix}_{v.tag}_high"]
            add(g, f"{label}, {rule} rule, 2015-2024", "$tn", src, by_rule)


def debt():
    g = "debt legacy (ladder 207)"
    split, stocks = DEBT + "derived/federal_split_2024.csv", DEBT + "derived/stocks.csv"
    main = dict(profile=MAIN)
    add(g, "federal part of the 2024 fiscal gap, central convention", "$bn", split,
        lambda v: ends(v.csv(split), "federal_bn", convention="central", **main))
    add(g, "2024 fiscal gap (cost + P)", "$bn", split,
        lambda v: ends(v.csv(split), "fiscal_gap_bn", convention="central", **main))
    for conv in ("central", "low", "high"):
        add(g, f"federal share of the 2024 gap, {conv} convention", "%", split,
            lambda v, conv=conv: ends(v.csv(split), "federal_share", convention=conv, **main), scale=100)
    c = dict(benchmark="main", rule="programme_income_pandemic_per_head", convention="central", rate_path="effective",
             window_start=2005, financing="all_borrowed")
    for col, label, unit, sc in (("stock_entering_2024_bn", "legacy stock entering 2024", "$bn", 1),
                                 ("stock_share_of_debt_end_fy2023", "stock, share of debt at end FY2023", "%", 100),
                                 ("legacy_interest_2024_bn", "legacy interest, 2024", "$bn", 1),
                                 ("interest_per_member_usd", "interest per group member", "$", 1),
                                 ("interest_per_other_resident_usd", "interest per other resident", "$", 1),
                                 ("interest_share_of_fy2024_net_interest", "interest, share of FY2024 net interest", "%", 100),
                                 ("interest_share_of_account_interest_allocation",
                                  "interest over the account's interest row allocation", "ratio", 1),
                                 ("stock_end_2024_brief_bn", "the brief's D, stock at the end of FY2024", "$bn", 1),
                                 ("sum_flows_nominal_bn", "nominal sum of the 2005-2023 federal gaps", "$bn", 1),
                                 ("flow_2024_part_year_interest_bn", "the 2024 gap's own part-year interest", "$bn", 1)):
        add(g, label + " (central rule)", unit, stocks, lambda v, col=col: ends(v.csv(stocks), col, **c), scale=sc)
    rules = {k: v for k, v in c.items() if k != "rule"}
    add(g, "legacy interest across back-cast rules, central convention", "$bn", stocks,
        lambda v: span(v.csv(stocks), "legacy_interest_2024_bn", **rules))
    add(g, "legacy stock across back-cast rules, central convention", "$tn", stocks,
        lambda v: span(v.csv(stocks), "stock_entering_2024_bn", **rules), scale=1e-3)
    conv = {k: v for k, v in rules.items() if k != "convention"}
    add(g, "legacy interest across rules and payer conventions", "$bn", stocks,
        lambda v: span(v.csv(stocks), "legacy_interest_2024_bn", **conv))
    add(g, "legacy interest, every specification", "$bn", stocks,
        lambda v: span(v.csv(stocks), "legacy_interest_2024_bn", benchmark="main"))
    add(g, "legacy interest, central rule, every specification", "$bn", stocks,
        lambda v: span(v.csv(stocks), "legacy_interest_2024_bn", benchmark="main", rule=c["rule"]))
    for k, val, label in (("convention", "low", "low payer convention"), ("convention", "high", "high payer convention"),
                          ("rate_path", "constant_3_22", "constant 3.22% rate"),
                          ("rate_path", "treasury_10y", "10-year Treasury rate"),
                          ("rate_path", "gross_public_securities", "public securities rate"),
                          ("window_start", 2010, "window from 2010"), ("window_start", 2015, "window from 2015"),
                          ("financing", "half_borrowed", "half borrowed"),
                          ("benchmark", "proportional", "proportional benchmark")):
        add(g, f"legacy interest, {label}", "$bn", stocks,
            lambda v, spec={**c, k: val}: ends(v.csv(stocks), "legacy_interest_2024_bn", **spec))
    benefits = DEBT + "derived/benefit_sensitivity.csv"
    for name in ("mobility", "mobility_and_scale"):
        for col, label in (("federal_2024_bn", "federal 2024"), ("stock_reduction_bn", "stock reduction"),
                           ("interest_reduction_2024_bn", "interest reduction 2024")):
            add(g, f"omitted benefits {name}: {label}", "$bn", benefits,
                lambda v, name=name, col=col: pick(v.csv(benefits), benefit_set=name, window_start=2005).iloc[0][col])
    forward = DEBT + "derived/forward_path.csv"
    for years in (10, 20, 30):
        add(g, f"forward federal debt from the 2024 gap, {years} years", "$bn", forward,
            lambda v, years=years: ends(v.csv(forward), "debt_bn", part="federal", convention="central",
                                        financing="all_borrowed", years=years))
    add(g, "forward debt if the whole gap were borrowed, 10 years", "$tn", forward,
        lambda v: ends(v.csv(forward), "debt_bn", part="whole_gap", convention="none", financing="all_borrowed",
                       years=10), scale=1e-3)
    windows = DEBT + "derived/adopted_backcast_windows.csv"
    for rule in ("programme", "programme_income"):
        for w in (2015, 2010, 2005):
            add(g, f"back-cast net cost, {rule}, {w}-2024", "$tn", windows,
                lambda v, rule=rule, w=w: ends(v.csv(windows), "net_cost_tn", benchmark="main", rule=rule,
                                               receipts_method="own_series", window_start=w))
    comp = DEBT + "derived/corrections_federal_by_component_2024.csv"
    for name in ("tax_stack", "medical_ethnicity_and_ltss", "audit_row1_premium_credits",
                 "education_row6_and_school_price", "lane_constants", "finite_removal", "consumption_key"):
        def component(v, name=name):
            k = pick(v.csv(comp), convention="central", component=name)
            return None if k.empty else ends(k, "federal_bn")
        add(g, f"per-correction federal part, {name}, central convention", "$bn", comp, component)
    for step, label in (("school_response_on_education_lines", "school response on the education lines"),
                        ("constant_line_federal_share", "constant line's federal share")):
        for conv in ("central", "low", "high"):
            def school_step(v, conv=conv, step=step):
                if v.case == "sept24" or v.case == next(iter(LATER)):
                    return None
                b = pick(v.csv(DEBT + f"derived/{v.case}_bridge_2024.csv"), convention=conv, step=step)
                return ends(b, "federal_bn")
            add(g, f"bridge from the previous case at matched specifications: federal part, {label}, "
                   f"{conv} convention", "$bn", DEBT + "derived/<case>_bridge_2024.csv", school_step)


def distribution():
    g = "distribution (ladder 194)"
    q, w, inputs = DIST + "derived/channel_by_quintile.csv", DIST + "derived/weighted_totals.csv", DIST + "derived/inputs.json"

    def val(v, ch, k, col="bn"):
        d = v.csv(q)
        d = d[d.measure == "spm"]
        return float(d[(d.channel == ch) & (d.quintile == k)][col].iloc[0])
    add(g, "fiscal cost channel, A_mid + F_c (negative = cost)", "$bn", q, lambda v: val(v, "fiscal_a", 0))
    for k in range(1, 6):
        add(g, f"fiscal cost, tax-share financing, fifth {k}", "$bn", q, lambda v, k=k: val(v, "fiscal_a", k))
    add(g, "fiscal cost, per-person cuts, each fifth", "$bn", q, lambda v: val(v, "fiscal_b", 1))
    add(g, "fiscal cost, top fifth's part under tax-share financing", "%", q,
        lambda v: val(v, "fiscal_a", 5) / val(v, "fiscal_a", 0), scale=100)
    add(g, "fiscal cost under per-person cuts, share of resources, bottom and top fifth", "%", q,
        lambda v: (val(v, "fiscal_b", 1, "pct_of_resources"), val(v, "fiscal_b", 5, "pct_of_resources")))
    add(g, "central total with the social items (TOTAL)", "$bn", q, lambda v: val(v, "TOTAL_a", 0))
    for conv, label in (("a", "tax-share"), ("b", "per-person")):
        add(g, f"central total, share of resources, bottom and top fifth, {label}", "%", q,
            lambda v, conv=conv: (val(v, f"TOTAL_{conv}", 1, "pct_of_resources"),
                                  val(v, f"TOTAL_{conv}", 5, "pct_of_resources")))

    def wv(v, ch, col):
        d = v.csv(w)
        d = d[d.measure == "spm"]
        return float(d[(d.channel == ch) & (d.eta == 1.3)][col].iloc[0])
    for conv, label in (("a", "tax-share"), ("b", "per-person")):
        add(g, f"central total at eta 1.3, equal-split equivalent, {label}", "$bn", w,
            lambda v, conv=conv: wv(v, f"TOTAL_{conv}", "equal_split_p5"))
        add(g, f"central total at eta 1.3, mean-normalized, {label}", "$bn", w,
            lambda v, conv=conv: wv(v, f"TOTAL_{conv}", "person_p5"))
    outside = ["wages", "housing_net", "crime", "unreimbursed_care"]
    add(g, "outside the budget: bottom four fifths, top fifth", "$bn", q,
        lambda v: (sum(val(v, ch, k) for ch in outside for k in (1, 2, 3, 4)), sum(val(v, ch, 5) for ch in outside)))
    add(g, "direct fiscal response A at the band ends (negative = cost)", "$bn", inputs,
        lambda v: (v.json(inputs)["fiscal"]["adopted"]["A_low_cost"], v.json(inputs)["fiscal"]["adopted"]["A_high_cost"]))


def uncertainty():
    g = "uncertainty (ladder 184)"
    src = UNC + "derived/<case>/summary.json"
    main = lambda v: v.unc if v.case == "sept24" else v.unc[v.case]  # noqa: E731
    for key, label in (("se_independent_bn", "per-case SE, sources independent"),
                       ("se_positive_correlation_bn", "per-case SE, all positively correlated"),
                       ("se_cps_bn", "per-case SE, CPS keys only"),
                       ("ci95_union_bn", "95% intervals of the main band's cases, union"),
                       ("ci95_envelope_union_bn", "95% intervals at the correlated upper bound, union"),
                       ("ci95_with_benefit_keys_union_bn", "95% intervals with the benefit keys' SE, union")):
        add(g, label, "$bn", src, lambda v, key=key: tuple(main(v)[key]))
    add(g, "per-case SE, uncorrected model at the adopted responses (control)", "$bn", src,
        lambda v: None if v.case == "sept24" else tuple(v.unc["uncorrected_at_adopted_responses"]["se_independent_bn"]))


def fmt(lo, hi, unit):
    if lo is None or pd.isna(lo):
        return "—"
    d = 0 if unit == "$" or abs(lo) >= 1000 else (2 if unit in ("ratio", "$tn") or abs(lo) < 10 else 1)
    if max(abs(lo), abs(hi) if hi is not None and not pd.isna(hi) else 0) < 0.1:
        d = 4
    if hi is not None and not pd.isna(hi) and hi != lo and f"{lo:.{d}f}" == f"{hi:.{d}f}":
        d += 1
    s = f"{lo:,.{d}f}"
    return s if hi is None or pd.isna(hi) else f"{s} to {hi:,.{d}f}"


VIEWS: dict[str, View] = {}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--case", choices=list(LATER), default="sept26_schools", help="the new column's case")
    ap.add_argument("--middle", choices=[*LATER, "none"], default="sept26",
                    help="a case shown between old and new, or none")
    ap.add_argument("--out", type=Path, default=HERE / "derived/old_new_lanes.csv")
    args = ap.parse_args()
    cases = ["sept24"] + ([args.middle] if args.middle not in ("none", args.case) else []) + [args.case]
    with tempfile.TemporaryDirectory() as tmp:
        for case in cases:
            VIEWS[case] = View(case, Path(tmp))
        main_case()
        backcast()
        debt()
        distribution()
        uncertainty()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(ROWS[0]), lineterminator="\n")
        w.writeheader()
        for r in ROWS:
            w.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in r.items()})
    head = " | ".join(LABELS.get(c, c) for c in cases)
    group = None
    for r in ROWS:
        if r["group"] != group:
            group = r["group"]
            print(f"\n**{group}**\n\n| Quantity | Unit | {head} | File |\n|---|---|{'---:|' * len(cases)}---|")
        cells = " | ".join(fmt(r[f"{c}_low"], r[f"{c}_high"], r["unit"]) for c in cases)
        print(f"| {r['quantity']} | {r['unit']} | {cells} | `{r['file'].replace(F, '')}` |")
    out = args.out.resolve()
    print(f"\n{len(ROWS)} rows -> {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")


if __name__ == "__main__":
    main()
