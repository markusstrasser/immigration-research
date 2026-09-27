"""Old -> new for every number this lane publishes, one propagation round at a time.

  --round 2 (default)  the schools case -> the September 27 case (2026-09-28,
                       sept27_propagation_2026_09_27/RESULT_ledger.md). Old: the schools-case files committed
                       at SCHOOLS. New: sept27 from derived/ (or --sept27-dir), gated to hold that case.
                       Writes sept27_propagation_2026_09_27/derived/old_new_ledger.csv.
  --round 1            the September 24 case -> the September 26 cases (2026-09-26,
                       sept26_propagation_2026_09_26/RESULT_ledger.md). September 24: the files committed at OLD.
                       The one-year scenario (sept26) is rebuilt with `specs.cjs --case sept26` and
                       `winners_losers.py --case sept26` into a temporary directory, or read from --sept26-dir.
                       The schools case: its files at SCHOOLS (derived/ held it until September 28).
                       Writes sept26_propagation_2026_09_26/derived/old_new_ledger.csv, byte for byte as committed.

Nothing is typed in: every value is selected from the ledger file named in its row, and a number that the memo
(research/immigration-winners-and-losers-2026-09-25.md) or the lane's RESULT.md quotes is one of these rows.
Round 2 adds the September 27 case's own quantities: the fiscal channel's three financing parts, the capped
programs, the long-run congestion by band end and the preferences attribution; the schools case has none of
them, so its cells are empty.

Run from the repository root, after the default run:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/winners_losers_2026_09_24/old_new.py [--round 1]
"""
from __future__ import annotations

import argparse
import io
import json
import os
import subprocess
import tempfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REL = "infra/immigration-fiscal/winners_losers_2026_09_24/derived"
OLD = "8a762fe"       # the September 24 files (the only commit that wrote derived/ before 2026-09-26)
SCHOOLS = "fa1bd3a"   # the schools-case files (derived/ from 2026-09-26 until the September 27 case)
ROUNDS = {
    1: dict(cases=("sept24", "sept26", "sept26_schools"), change=("change_sept24_to_schools", "sept24", "sept26_schools"),
            out=ROOT / "infra/immigration-fiscal/sept26_propagation_2026_09_26/derived/old_new_ledger.csv"),
    2: dict(cases=("sept26_schools", "sept27"), change=("change_schools_to_sept27", "sept26_schools", "sept27"),
            out=ROOT / "infra/immigration-fiscal/sept27_propagation_2026_09_27/derived/old_new_ledger.csv"),
}
MAIN_NETS = [f"net_{n}_{c}" for n in ("account", "social", "with_proposed") for c in ("a", "b")]
SENSITIVITY_NETS = [f"net_social_{c}_{t}" for c in ("a", "b")
                    for t in ("pooled_national_fiscal", "housing_national_uniform", "crime_custody_footing")]
MEMO_CUTS = ("state3", "edu_nativity", "tenure", "age3", "industry5", "race5", "sex", "decile")


def run_sept26(out: Path):
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1")
    for cmd in (["node", str(HERE / "specs.cjs"), "--case", "sept26", "--out-dir", str(out)],
                ["uv", "run", "--no-project", "python3", str(HERE / "winners_losers.py"), "--case", "sept26",
                 "--out-dir", str(out)]):
        r = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True)
        if r.returncode:
            raise SystemExit(f"[BLOCKED] {' '.join(cmd[:4])} exited {r.returncode}:\n{r.stdout[-2000:]}{r.stderr[-2000:]}")


def loaders(sept26_dir: Path | None, sept27_dir: Path) -> dict:
    def at(commit):
        return lambda name: subprocess.run(["git", "-C", str(ROOT), "show", f"{commit}:{REL}/{name}"], check=True,
                                           capture_output=True).stdout
    return {"sept24": at(OLD), "sept26": lambda name: (sept26_dir / name).read_bytes(), "sept26_schools": at(SCHOOLS),
            "sept27": lambda name: (sept27_dir / name).read_bytes()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", type=int, choices=tuple(ROUNDS), default=2)
    ap.add_argument("--sept26-dir", type=Path, default=None,
                    help="round 1: a finished `--case sept26 --out-dir` run (default: rebuild into a temporary directory)")
    ap.add_argument("--sept27-dir", type=Path, default=HERE / "derived",
                    help="round 2: a finished September 27 run (default: derived/)")
    args = ap.parse_args()
    rnd = ROUNDS[args.round]
    cases = rnd["cases"]
    with tempfile.TemporaryDirectory() as tmp:
        d26 = None
        if "sept26" in cases:
            d26 = args.sept26_dir.resolve() if args.sept26_dir else Path(tmp)
            if not args.sept26_dir:
                print("[sept26] rebuilding the one-year scenario into a temporary directory")
                run_sept26(d26)
        load = loaders(d26, args.sept27_dir.resolve())
        js = {c: json.loads(load[c]("inputs.json")) for c in cases}
        for c in cases:
            if c == "sept24":
                if "case" in js[c]:
                    raise SystemExit("[BLOCKED] the September 24 files carry a later case")
            elif js[c].get("case", {}).get("case") != c:
                raise SystemExit(f"[BLOCKED] the {c} files hold case {js[c].get('case', {}).get('case')}")
        csv = {c: {} for c in cases}

        def table(c, name):
            if name not in csv[c]:
                csv[c][name] = pd.read_csv(io.BytesIO(load[c](name)))
            return csv[c][name]
        rows = build_rows(table, js, cases, sept27=args.round == 2)
    out = pd.DataFrame(rows)
    col, old, new = rnd["change"]
    out[col] = out[new] - out[old]
    rnd["out"].parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(rnd["out"], index=False, lineterminator="\n", float_format="%.6f")
    print(f"wrote {rnd['out'].relative_to(ROOT)} ({len(out)} rows)")


def build_rows(table, js, cases, sept27=False) -> list[dict]:
    rows = []

    def add(group, quantity, unit, file, get):
        vals = {}
        for c in cases:
            try:
                v = get(c)
            except (KeyError, IndexError):
                v = None
            vals[c] = None if v is None else float(v)
        rows.append(dict(group=group, quantity=quantity, unit=unit, file=f"derived/{file}", **vals))

    def one(df, **match):
        m = df
        for k, v in match.items():
            m = m[m[k] == v]
        if len(m) > 1:
            raise SystemExit(f"[BLOCKED] {match} matches {len(m)} rows")
        return m.iloc[0] if len(m) else None

    # 1. The share ahead and the nets' totals (memo verdict, sensitivities; RESULT headline).
    for net in MAIN_NETS + SENSITIVITY_NETS:
        for unit in ("spm_unit_pooled", "person"):
            for stack in ("central", "least_costly", "most_costly"):
                def get(c, net=net, unit=unit, stack=stack):
                    r = one(table(c, "net_shares.csv"), net=net, unit=unit, stack=stack)
                    return None if r is None else 100 * r.winners_share
                if all(get(c) is None for c in cases):
                    continue
                add("share ahead", f"{net}, {stack}, {unit}", "%", "net_shares.csv", get)
            for col, unit_ in (("total_bn", "$bn"), ("mean_usd", "$"), ("median_usd", "$")):
                def get(c, net=net, unit=unit, col=col):
                    r = one(table(c, "net_shares.csv"), net=net, unit=unit, stack="central")
                    return None if r is None else r[col]
                if all(get(c) is None for c in cases) or (col == "total_bn" and unit == "person"
                                                          and net in MAIN_NETS):
                    continue   # totals do not depend on the unit; listed once, pooled
                add("net totals", f"{net}, central, {unit}: {col}", unit_, "net_shares.csv", get)
    # 2. Who gains and who loses, by channel (memo section 2).
    keys = ["who", "gain_or_loss", "channel"]
    all_keys = pd.concat([table(c, "winners_losers_table.csv")[keys] for c in cases]).drop_duplicates()
    for k in all_keys.itertuples(index=False):
        for col, unit_ in (("bn_per_year", "$bn"), ("persons_m", "m"), ("usd_per_person", "$")):
            def get(c, k=k, col=col):
                r = one(table(c, "winners_losers_table.csv"), who=k.who, gain_or_loss=k.gain_or_loss, channel=k.channel)
                return None if r is None or pd.isna(r[col]) else r[col]
            if all(get(c) is None for c in cases):
                continue
            add("channel table", f"{k.who} | {k.gain_or_loss} | {k.channel}: {col}", unit_,
                "winners_losers_table.csv", get)
    # 3. Person nets by cut (memo section 3), pooled and person count.
    cols = [f"net_social_{c}_spm_pooled_usd_per_person" for c in ("a", "b")] + \
           [f"net_social_{c}_spm_pooled_winners_share" for c in ("a", "b")] + \
           [f"net_social_{c}_winners_share" for c in ("a", "b")]
    groups = table(cases[0], "person_nets_by_cut.csv")
    for g in groups[groups.cut.isin(MEMO_CUTS)].itertuples(index=False):
        for col in cols:
            share = col.endswith("winners_share")
            def get(c, g=g, col=col, share=share):
                r = one(table(c, "person_nets_by_cut.csv"), cut=g.cut, group=g.group)
                return None if r is None else (100 * r[col] if share else r[col])
            add("person nets by cut", f"{g.cut}={g.group}: {col}", "%" if share else "$ per person",
                "person_nets_by_cut.csv", get)
    # 4. Geography and quintile burden (memo section 4; RESULT): cuts.csv, person count.
    for cut, grp in (("state3", "CA"), ("state3", "TX"), ("state3", "rest"), ("top10_states", "AZ")):
        for chan in ("net_social_a", "net_social_b", "net_social_a_pooled_national_fiscal",
                     "net_social_b_pooled_national_fiscal"):
            for col, unit_ in (("usd_per_person", "$ per person"), ("winners_share", "%")):
                def get(c, cut=cut, grp=grp, chan=chan, col=col):
                    r = one(table(c, "cuts.csv"), cut=cut, group=grp, channel=chan, level="central")
                    return None if r is None else (100 * r[col] if col == "winners_share" else r[col])
                add("geography", f"{cut}={grp}: {chan}, central, person: {col}", unit_, "cuts.csv", get)
    for q in ("Q1", "Q2", "Q3", "Q4", "Q5"):
        for chan in ("net_social_a", "net_social_b"):
            def get(c, q=q, chan=chan):
                r = one(table(c, "cuts.csv"), cut="quintile", group=q, channel=chan, level="central")
                return None if r is None else r.pct_of_resources
            add("quintile burden", f"quintile={q}: {chan}, central: % of SPM resources", "%", "cuts.csv", get)
    for cells, cell in (("edu_nativity x tenure", "ba_plus|us_born & landlord"),
                        ("edu_nativity x state3", "high_school|us_born & CA"),
                        ("edu_nativity x state3", "high_school|us_born & TX")):
        for net in ("net_social_a", "net_social_b"):
            for col, unit_ in (("winners_share", "%"), ("mean_net_usd", "$ per person"), ("persons_m", "m")):
                def get(c, cells=cells, cell=cell, net=net, col=col):
                    r = one(table(c, "winner_cells.csv"), cuts=cells, cell=cell, net=net)
                    return None if r is None else (100 * r[col] if col == "winners_share" else r[col])
                add("winner cells", f"{cells}: {cell}: {net}, central, person: {col}", unit_, "winner_cells.csv", get)
    # 5. Pooling moves (memo section 1).
    for net in ("net_social_a", "net_social_b"):
        for col, unit_ in (("up_m", "m"), ("down_m", "m")):
            def get(c, net=net, col=col):
                return one(table(c, "pooling_moves.csv"), net=net, role="all", unit="all")[col]
            add("pooling", f"{net}, all persons: {col}", unit_, "pooling_moves.csv", get)
    # 6. The registry, every row at low, central and high.
    reg_ids = pd.concat([table(c, "channels.csv")[["id"]] for c in cases]).drop_duplicates().id
    for id_ in reg_ids:
        for lev in ("low", "central", "high"):
            def get(c, id_=id_, lev=lev):
                r = one(table(c, "channels.csv"), id=id_)
                return None if r is None or pd.isna(r[f"bn_{lev}"]) else r[f"bn_{lev}"]
            if all(get(c) is None for c in cases):
                continue
            add("registry", f"{id_}: {lev}", "$bn", "channels.csv", get)
    # 7. The group's own frame.
    items = pd.concat([table(c, "group_frame.csv")[["item"]] for c in cases]).drop_duplicates().item
    for item in items:
        for col in ("bn_low", "bn_central", "bn_high"):
            def get(c, item=item, col=col):
                r = one(table(c, "group_frame.csv"), item=item)
                return None if r is None or pd.isna(r[col]) else r[col]
            if all(get(c) is None for c in cases):
                continue
            add("group frame", f"{item}: {col}", "$bn", "group_frame.csv", get)
    # 8. The fiscal channel's federal and state-local parts (the case's own rows). From September 27 the
    # debt lane's federal_bn and state_local_bn are the cash part; the other two parts are listed after them.
    model = {c: (js[c].get("case") or {}).get("model", "adopted_2026_09_24") for c in cases}
    cash = " (cash part from September 27)" if sept27 else ""
    parts = ("resource_cost_bn", "resource_cost_federal_bn", "displaced_bn", "displaced_federal_bn") if sept27 else ()
    for end in ("low", "high"):
        for conv in ("low", "central", "high"):
            for col in ("federal_bn", "state_local_bn") + parts:
                def get(c, end=end, conv=conv, col=col):
                    return one(table(c, "fiscal_federal_split.csv"), case=model[c], end=end, convention=conv)[col]
                add("federal split", f"{end} end, {conv} payer convention: {col}"
                    + (cash if col in ("federal_bn", "state_local_bn") else ""), "$bn", "fiscal_federal_split.csv", get)
    for col, unit_ in (("cost_bn", "$bn"), ("federal_bn", "$bn"), ("state_local_bn", "$bn"), ("federal_share", "share"),
                       ("future_taxpayers_bn", "$bn"), ("federal_today_bn", "$bn")) + tuple((p, "$bn") for p in parts):
        def get(c, col=col):
            return one(table(c, "fiscal_federal_split.csv"), case=model[c], end="central", convention="central")[col]
        add("federal split", f"central: {col}" + (cash if col in ("federal_bn", "state_local_bn", "federal_share") else ""),
            unit_, "fiscal_federal_split.csv", get)
    # 9. Totals held in inputs.json: the allocation base, the published totals, interest.
    for k in ("items_central", "least_costly", "most_costly"):
        add("totals", f"social_totals.{k}", "$bn", "inputs.json", lambda c, k=k: js[c]["social_totals"][k])
    for k, n in (("equal", 2), ("custody", 2), ("range", 2), ("span", 2), ("equal_victims", 0), ("custody_victims", 0)):
        for i in range(max(n, 1)):
            add("totals", f"published_totals.{k}" + (f"[{('low', 'high')[i]}]" if n else ""), "$bn", "inputs.json",
                lambda c, k=k, i=i, n=n: js[c]["published_totals"][k][i] if n else js[c]["published_totals"][k])
    for k in ("low", "central", "high"):
        add("totals", f"debt legacy interest: {k}", "$bn", "inputs.json", lambda c, k=k: js[c]["debt"][k])
    if sept27:
        sept27_rows(add, js)
    return rows


def sept27_rows(add, js):
    """10. The September 27 case's own quantities in inputs.json (the schools case has none of them)."""
    for prog in ("housing_subsidies", "energy_assistance"):
        add("capped programs", f"{prog}: amount, central", "$bn", "inputs.json",
            lambda c, p=prog: js[c]["capped_programs"]["amounts_bn"][p]["central"])
        add("capped programs", f"{prog}: eligible non-recipient households", "m", "inputs.json",
            lambda c, p=prog: js[c]["capped_programs"]["keys"][p]["eligible_non_recipient_households_m"])
    for end in ("low", "high"):
        for k in ("central_bn", "lane_cut"):
            add("congestion", f"{end} band end: {k}", "$bn" if k.endswith("bn") else "share", "inputs.json",
                lambda c, e=end, k=k: js[c]["congestion"]["by_band_end"][e][k])
        for i, lim in enumerate(("min", "max")):
            add("congestion", f"{end} band end: factorial {lim}", "$bn", "inputs.json",
                lambda c, e=end, i=i: js[c]["congestion"]["by_band_end"][e]["range_bn"][i])
        add("congestion", f"{end} band end: states where other residents gain", "states", "inputs.json",
            lambda c, e=end: len(js[c]["congestion"]["by_band_end"][e]["states_with_a_gain"]))
    add("congestion", "B1, lanes fixed", "$bn", "inputs.json", lambda c: js[c]["congestion"]["b1_lanes_fixed_bn"])
    pa = lambda c: js[c]["preferences_attribution"]  # noqa: E731
    for k in ("dbe_premium_part_bn", "dbe_netted_bn"):
        add("preferences attribution", k, "$bn", "inputs.json", lambda c, k=k: pa(c)[k])
    add("preferences attribution", "DBE share in the fiscal channel (key share x highway response, mean)", "share",
        "inputs.json", lambda c: pa(c)["dbe_in_fiscal_channel_share"]["used"])
    for p in ("admissions", "contractor_hiring", "lost_profits", "taxpayer_premium"):
        add("preferences attribution", f"{p}: white natives' share of the pool", "share", "inputs.json",
            lambda c, p=p: pa(c)["white_share_of_pool"][p])
        for side in ("white_parts", "other_parts"):
            add("preferences attribution", f"{p}: {side} before scaling to the logged total", "$bn", "inputs.json",
                lambda c, p=p, s=side: pa(c)[s][p])


if __name__ == "__main__":
    main()
