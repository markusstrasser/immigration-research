"""Re-evaluate on the account's priced count the air and crash figures that the evidence map printed as
approximations: the PM2.5 span, deaths among others and normalized figure, and the crash span and fault-based row.

The account prices 39,712,493 group members (data audit row 4). population_basis_2026_09_29/reeval.py restated each
pairing row's central value on that count by evaluating the lane's own function with every CPS count it reads
replaced by its row-4 value. The map then scaled the rest of each row (span ends, deaths, the normalized and
fault-based figures) by the central's factor. Here the same substitution runs through each lane's full grid, so
every end is the grid's own minimum or maximum on the priced count. Both lanes are imported read-only: their
main() never runs and nothing is written beside them.

  pm25_consumption    air_pollution_2026_09_28/air_items.py pm_grid (3^7 cells): the union n and the CPS civilian
                      frame at row 4. Row 4 alone, as in the pairing: the item is keyed to consumption, not to
                      travel per person.
  road_crash_*        road_crash_externality_2026_09_28/crash_model.py evaluate_split over its main()'s 3^9 grid,
                      composition term on: the union and civilian counts, the union's share of Hispanic residents
                      and the self-exposure q at row 4 (q from the congestion lane's exposures at the row-4 scale),
                      and the NHTS per-person ratios on persons aged 5+ (reeval.py's _5plus arm, the pairing_5plus
                      basis): P = p(1 - u_g) / [p(1 - u_g) + (1 - p)(1 - u_o)].

The frame counts and the under-5 shares come from reeval.py's own counts() and under5_shares().

Gates (exit 1, nothing written): each lane on its own counts reproduces its published files; q at the lane's scale
reproduces crash_model.py's; each central on the priced count reproduces reeval.csv's row4_bn, and its factor and
restated figure reproduce restated_pairing.csv (section row for PM2.5, row_5plus for crashes); every span holds its
central. Writes derived/priced_spans.csv, derived/end_factors.csv and derived/gates.csv. Run from the repository
root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --offline python3 \\
      infra/immigration-fiscal/social_spans_priced_count_2026_09_29/priced_spans.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import csv  # noqa: E402
import importlib.util  # noqa: E402
import itertools  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
BASIS = FISCAL / "population_basis_2026_09_29"
AIR = FISCAL / "air_pollution_2026_09_28"
CRASH = FISCAL / "road_crash_externality_2026_09_28"
OUT = HERE / "derived"
STATS = ("low", "central", "high")
ROW4 = "row 4"
ROW4_5PLUS = "row 4; NHTS ratios per person aged 5+"
FAILS: list[str] = []
GATES: list[dict] = []


def gate(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}", flush=True)
    GATES.append(dict(gate=label, result="PASS" if ok else "FAIL", detail=detail))
    if not ok:
        FAILS.append(label)


def load(name, path):
    """A lane's script as a module; its main() is guarded, so nothing runs or writes."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def one_row(path, **match):
    rows = [r for r in csv.DictReader(path.open()) if all(r[k] == v for k, v in match.items())]
    if len(rows) != 1:
        raise SystemExit(f"[BLOCKED] {path.relative_to(FISCAL)}: {len(rows)} rows for {match}")
    return rows[0]


def label(cell):
    return " ".join(f"{k}={v}" for k, v in cell.items())


def share_5plus(p, u_g, u_o):
    """The union's share of persons aged 5+ (reeval.py's _5plus arm). crash_model.py's traffic share
    s = P r / (P r + 1 - P) then applies the NHTS per-person ratio r to the persons it is measured on."""
    return p * (1 - u_g) / (p * (1 - u_g) + (1 - p) * (1 - u_o))


def air_grid(air):
    """pm_grid's cost to others and normalized cost ($bn) per cell, as air_items.py main() values them, the central
    cell's index, and the population share s."""
    grid, s = air.pm_grid("mexican_origin")
    icols = [c for c in grid.columns if c.startswith("i_")]
    for measure, col in (("absolute", "others"), ("normalized", "normalized")):
        grid[measure] = grid[col] * grid.morb * air.VSL_DOT_2024 / 1e9
    return grid, int(grid.index[(grid[icols] == 1).all(axis=1)][0]), icols, s


def air_cells(grid, central):
    """(measure, statistic) -> the grid cell: the minimum, the central cell and the maximum, first match on ties."""
    cells = {(m, st): i for m in ("absolute", "normalized")
             for st, i in zip(STATS, (int(grid[m].idxmin()), central, int(grid[m].idxmax())))}
    cells["deaths_among_others", "central"] = central
    return cells


def air_value(grid, measure, i):
    return float(grid.others[i]) if measure == "deaths_among_others" else float(grid[measure][i])


def crash_grid(crash):
    """evaluate_split over crash_model.py main()'s grid, in its order, and the central cell's position."""
    keys = list(crash.FACTORS)
    nf_or = crash.ccrs_nonfatal_or()
    levels = {**crash.FACTORS, **crash.x_levels_evidence(), "r_nf": nf_or}

    def run(idx, composition=True):
        return crash.evaluate_split(*[levels[k][idx[k]] for k in keys], r_nf=nf_or[idx["r_nf"]],
                                    composition=composition)
    cells = [dict(zip(levels, c)) for c in itertools.product(range(3), repeat=len(levels))]
    mid = cells.index({k: 1 for k in levels})
    return cells, [run(c) for c in cells], mid, run


CRASH_COLS = {"absolute": "total", "fault_based": "fault_total"}


def crash_cells(results, mid):
    """(measure, statistic) -> grid position: the lane's span() takes min() and max() of the column."""
    out = {}
    for measure, col in CRASH_COLS.items():
        vals = [r[col] for r in results]
        out.update({(measure, "low"): vals.index(min(vals)), (measure, "central"): mid,
                    (measure, "high"): vals.index(max(vals))})
    return out


def self_exposure(cong, target):
    """crash_model.py's Q_METRO from the congestion lane's 2017 southwest exposures at the group scale `target`
    (reeval.py's derivation): the group-traffic-weighted group share of commute-route traffic."""
    A = cong.A
    lane_target, A.TARGET = A.TARGET, target
    try:
        e = cong.setup()[4]["2017 southwest"]
    finally:
        A.TARGET = lane_target
    ok = e.phi_commute_route.notna() & e.acs_group_vehicle_minutes.notna()
    return float((e.acs_group_vehicle_minutes * e.phi_commute_route)[ok].sum() / e.acs_group_vehicle_minutes[ok].sum())


def main():
    rv = load("reeval", BASIS / "reeval.py")
    k = rv.counts()
    n0, n4 = k["union|all"]
    civ0, civ4 = k["cps_all_civilian|all"]
    mex4 = k["union_hispanic|all"][1] / k["cps_hispanic_civilian|all"][1]
    u_g, u_o, u_union, u_national = rv.under5_shares()
    roads = next(csv.DictReader(rv.ROADS_KEYS.open()))
    gate("age bins are on the row-4 union and frame", abs(u_union - n4) < 1e-3 and abs(u_national - civ4) < 1e-3,
         f"{u_union:,.2f}, {u_national:,.2f}")
    gate("under-5 shares equal the roads lane's keys.csv", abs(u_g - float(roads["under5_group"])) < 1e-6
         and abs(u_o - float(roads["under5_others"])) < 1e-6, f"u_g {u_g:.6f}, u_o {u_o:.6f}")
    reeval = {r["row"]: float(r["row4_bn"]) for r in csv.DictReader((BASIS / "derived" / "reeval.csv").open())}
    restated = BASIS / "derived" / "restated_pairing.csv"
    rows, parts = [], []

    def restates(name, section, item, published, priced):
        """The central reproduces reeval.csv (printed to 9 dp) and restated_pairing.csv, whose restated figure is
        the lane's printed central times the exact factor."""
        gate(f"{name} central on the priced count reproduces reeval.csv", abs(priced - reeval[item if section == "row"
             else f"{item}_5plus"]) < 5e-10, f"{priced:.9f}")
        r = one_row(restated, section=section, item=item, end="both")
        f = priced / published
        again = float(r["published"]) * f
        gate(f"{name} factor and restated figure reproduce restated_pairing.csv ({section})",
             f"{f:.6f}" == r["factor"] and f"{again:.6f}" == r["restated"],
             f"x{f:.9f}; {r['published']} x factor = {again:.6f} vs {r['restated']}")

    print("[pm25_consumption: air_items.py pm_grid]", flush=True)
    air = load("air_items", AIR / "air_items.py")
    gate("air lane's union and frame are the published CPS counts",
         abs(air.GROUPS["mexican_origin"]["n"] - n0) < 0.5 and abs(air.POP_ALL - civ0) < 0.5)
    grid0, mid, icols, s0 = air_grid(air)
    cells0 = air_cells(grid0, mid)
    items = AIR / "derived" / "items.csv"
    detail = AIR / "derived" / "items_detail.csv"
    for measure in ("absolute", "normalized"):
        row = one_row(items, item="pm25_consumption", group="mexican_origin", measure=measure)
        got = [f"{air_value(grid0, measure, cells0[measure, st]):.4f}" for st in STATS]
        want = [row[f"{st}_bn"] for st in STATS]
        gate(f"pm25 {measure} low / central / high reproduce items.csv", got == want, " / ".join(got))
    deaths = air_value(grid0, "deaths_among_others", mid)
    want = one_row(detail, item="pm25_consumption", group="mexican_origin", measure="absolute")["deaths_central"]
    gate("pm25 deaths among others reproduce items_detail.csv", f"{deaths:.6g}" == want, f"{deaths:.6f}")
    air.GROUPS["mexican_origin"]["n"], air.POP_ALL = n4, civ4
    grid4, mid4, _, s4 = air_grid(air)
    cells4 = air_cells(grid4, mid4)
    gate("pm25 grid keeps its cells in order", mid4 == mid and (grid4[icols] == grid0[icols]).all().all())
    for (measure, st), i in cells4.items():
        p, n = air_value(grid0, measure, cells0[measure, st]), air_value(grid4, measure, i)
        printed = (one_row(detail, item="pm25_consumption", group="mexican_origin", measure="absolute")["deaths_central"]
                   if measure == "deaths_among_others" else
                   one_row(items, item="pm25_consumption", group="mexican_origin", measure=measure)[f"{st}_bn"])
        cell = {c: int(grid4[c][i]) for c in icols}
        moved = cells0[measure, st] != i
        rows.append(dict(item="pm25_consumption", measure=measure, statistic=st, basis=ROW4, lane_printed=printed,
                         published=p, priced=n, factor=n / p, cell=label(cell),
                         cell_on_published_count="moved" if moved else "same"))
        # the factor's parts, same cell on both counts: value = D theta s r (1 - sigma) x morb x VSL (absolute,
        # deaths) or D theta s [r (1 - sigma) - (1 - s)] x morb x VSL (normalized); D, theta, r, morb, VSL fixed
        g0, g4 = grid0.loc[i], grid4.loc[i]
        split = [("population share s", s0, s4)]
        if measure == "normalized":
            r = air.ARMS["r"]["mexican_origin"][int(g0.i_r)]
            split.append(("r (1 - sigma) - (1 - s)", r * (1 - g0.sigma) - (1 - s0), r * (1 - g4.sigma) - (1 - s4)))
        else:
            split.append(("1 - sigma (others' share of the deaths)", 1 - g0.sigma, 1 - g4.sigma))
        for name, a, b in split:
            parts.append(dict(item="pm25_consumption", measure=measure, statistic=st, part=name, published=a,
                              priced=b, factor=b / a))
    restates("pm25", "row", "pm25_consumption", air_value(grid0, "absolute", mid), air_value(grid4, "absolute", mid4))

    print("[road crashes: crash_model.py evaluate_split]", flush=True)
    crash = load("crash_model", CRASH / "crash_model.py")
    cong = load("long_run_congestion", FISCAL / "service_response_long_run_2026_09_27" / "congestion.py")
    gate("crash lane's union and frame are the published CPS counts",
         abs(crash.N_GROUP - n0) < 0.5 and abs(crash.N_ALL - civ0) < 0.5)
    gate("congestion lane's TARGET is the published CPS union", abs(cong.A.TARGET - n0) < 0.5)
    q0 = self_exposure(cong, cong.A.TARGET)
    gate("congestion exposures at the lane's scale reproduce crash_model.py's q", abs(q0 - crash.Q_METRO) < 1e-12,
         f"{q0:.9f}")
    q4 = self_exposure(cong, n4)
    h0 = crash.HISP_PED * crash.MEX_OF_HISP
    cells, res0, mid, run = crash_grid(crash)  # run() reads the module's counts when called
    pos0 = crash_cells(res0, mid)
    model = json.loads((CRASH / "derived" / "model.json").read_text())
    items = CRASH / "derived" / "items.csv"
    item_of = {"absolute": "road_crash_externality", "fault_based": "road_crash_externality_fault_based"}
    for measure, col in CRASH_COLS.items():
        got = [res0[pos0[measure, st]][col] for st in STATS]
        row = one_row(items, item=item_of[measure], group="mexican_origin", measure="absolute")
        gate(f"crash {measure} span reproduces model.json spans.{col} and items.csv",
             got == model["spans"][col] and [f"{v:.2f}" for v in got] == [row[f"{st}_bn"] for st in STATS],
             " / ".join(f"{v:.6f}" for v in got))
    p4 = n4 / civ4
    crash.N_GROUP, crash.N_ALL, crash.P_SHARE, crash.MEX_OF_HISP, crash.Q_METRO = n4, civ4, p4, mex4, q4
    alone = run(cells[mid])["total"]
    gate("crash central on row 4 alone reproduces reeval.csv", abs(alone - reeval["road_crash_externality"]) < 5e-10,
         f"{alone:.9f}; q {q0:.6f} -> {q4:.6f}")
    crash.P_SHARE = share_5plus(p4, u_g, u_o)
    h4 = crash.HISP_PED * crash.MEX_OF_HISP
    res4 = [run(c) for c in cells]
    pos4 = crash_cells(res4, mid)
    restates("crash", "row_5plus", "road_crash_externality", res0[mid]["total"], res4[mid]["total"])
    gate("fault-based central uses neither x nor the composition term (crash_model.py main()'s check)",
         res4[mid]["fault_total"] == run(cells[mid], composition=False)["fault_total"])
    for (measure, st), i in pos4.items():
        col = CRASH_COLS[measure]
        p, n = res0[pos0[measure, st]][col], res4[i][col]
        printed = one_row(items, item=item_of[measure], group="mexican_origin", measure="absolute")[f"{st}_bn"]
        rows.append(dict(item=item_of[measure], measure="absolute", statistic=st, basis=ROW4_5PLUS,
                         lane_printed=printed, published=p, priced=n, factor=n / p, cell=label(cells[i]),
                         cell_on_published_count="moved" if pos0[measure, st] != i else "same"))
        a, b = res0[i], res4[i]
        split = [("traffic share s", a["s"], b["s"]),
                 ("1 - q (other traffic in the areas the group drives)", 1 - a["q"], 1 - b["q"]),
                 ("1 - h (non-motorist victims outside the group)", 1 - h0, 1 - h4)]
        if measure == "absolute":  # the four components add to the total; each carries its composition term
            split += [(f"component {c}", a[c], b[c]) for c in ("mv_nonfatal", "mv_fatal", "nonmotorist",
                                                               "single_vehicle")]
        for name, x, y in split:
            parts.append(dict(item=item_of[measure], measure="absolute", statistic=st, part=name, published=x,
                              priced=y, factor=y / x if x else ""))
    priced = {(r["item"], r["measure"], r["statistic"]): r["priced"] for r in rows}
    for item, measure in dict.fromkeys((r["item"], r["measure"]) for r in rows if r["statistic"] == "low"):
        lo, c, hi = (priced[item, measure, st] for st in STATS)
        gate(f"{item} {measure} span holds its central on the priced count", lo <= c <= hi,
             f"{lo:.6f} <= {c:.6f} <= {hi:.6f}")

    if FAILS:
        print(f"FAIL: {len(FAILS)} gate(s): {FAILS}")
        sys.exit(1)
    OUT.mkdir(exist_ok=True)
    for name, table in (("priced_spans.csv", rows), ("end_factors.csv", parts), ("gates.csv", GATES)):
        with (OUT / name).open("w", newline="") as handle:
            out = csv.DictWriter(handle, fieldnames=list(table[0]), lineterminator="\n")
            out.writeheader()
            for r in table:
                out.writerow({c: (f"{v:.9f}" if isinstance(v, float) else v) for c, v in r.items()})
    for r in rows:
        print(f"  {r['item']:36s} {r['measure']:20s} {r['statistic']:8s} {r['published']:>12.6f} -> "
              f"{r['priced']:>12.6f}  x{r['factor']:.6f}  cell {r['cell_on_published_count']}")
    print(f"  wrote {len(rows)} rows, {len(parts)} factor parts, {len(GATES)} gates -> {OUT.relative_to(FISCAL)}")


if __name__ == "__main__":
    main()
