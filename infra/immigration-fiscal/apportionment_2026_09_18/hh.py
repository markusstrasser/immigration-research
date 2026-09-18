"""Huntington-Hill (method of equal proportions) apportionment + official-count verification.

Usage: uv run --no-project --with "pandas>=2" --with numpy --with xlrd --with openpyxl python3 hh.py
"""
import math
import heapq
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
DERIVED.mkdir(exist_ok=True)

HOUSE_SIZE = 435


def apportion(pops: dict, house_size: int = HOUSE_SIZE) -> dict:
    """Method of equal proportions. pops: {state: apportionment population}."""
    seats = {s: 1 for s in pops}
    n_states = len(pops)
    if house_size < n_states:
        raise ValueError("house smaller than number of states")
    # priority value for the (n+1)-th seat currently held at n seats: P / sqrt(n(n+1))
    heap = []
    for s, p in pops.items():
        pv = p / math.sqrt(1 * 2)
        # negate for max-heap; tie-break deterministically by state name
        heapq.heappush(heap, (-pv, s, 1))
    for _ in range(house_size - n_states):
        negpv, s, n = heapq.heappop(heap)
        seats[s] = n + 1
        nn = n + 1
        pv = pops[s] / math.sqrt(nn * (nn + 1))
        heapq.heappush(heap, (-pv, s, nn))
    return seats


def priority_table(pops: dict, house_size: int = HOUSE_SIZE):
    """Return the ordered list of (rank, state, seat_number, priority_value) for seats 51..house_size."""
    heap = []
    for s, p in pops.items():
        heapq.heappush(heap, (-p / math.sqrt(2), s, 1))
    out = []
    for rank in range(len(pops) + 1, house_size + 1):
        negpv, s, n = heapq.heappop(heap)
        out.append((rank, s, n + 1, -negpv))
        nn = n + 1
        heapq.heappush(heap, (-pops[s] / math.sqrt(nn * (nn + 1)), s, nn))
    return out


def load_2020():
    d = pd.read_excel(CACHE / "apportionment-2020-table01.xlsx", header=None)
    hdr = d.index[d[0].astype(str).str.strip() == "STATE"][0]
    body = d.loc[hdr + 1:, [0, 1, 2]].dropna(subset=[0])
    body.columns = ["state", "pop", "seats"]
    body["state"] = body["state"].astype(str).str.strip()
    body = body[~body["state"].str.upper().str.startswith(("TOTAL", "1", "2", "NOTE"))]
    body = body[body["pop"].notna()]
    body["pop"] = body["pop"].astype("int64")
    body["seats"] = body["seats"].astype("int64")
    return body.reset_index(drop=True)


def load_2010():
    d = pd.read_excel(CACHE / "apport2010-table1.xls", header=None)
    hdr = d.index[d[0].astype(str).str.strip() == "STATE"][0]
    body = d.loc[hdr + 1:, [0, 1, 3]].dropna(subset=[0])
    body.columns = ["state", "pop", "seats"]
    body["state"] = body["state"].astype(str).str.strip()
    body = body[body["pop"].notna() & body["seats"].notna()]
    body = body[~body["state"].str.upper().str.startswith("TOTAL")]
    body["pop"] = body["pop"].astype("int64")
    body["seats"] = body["seats"].astype("int64")
    return body.reset_index(drop=True)


def verify(df, year):
    pops = dict(zip(df["state"], df["pop"]))
    official = dict(zip(df["state"], df["seats"]))
    got = apportion(pops)
    diffs = {s: (official[s], got[s]) for s in pops if official[s] != got[s]}
    ok = not diffs
    print(f"[{year}] states={len(pops)} total_pop={sum(pops.values()):,} "
          f"official_seats={sum(official.values())} computed_seats={sum(got.values())}")
    print(f"[{year}] EXACT MATCH: {ok}" + ("" if ok else f"  diffs={diffs}"))
    return ok, got


if __name__ == "__main__":
    d20 = load_2020()
    d10 = load_2010()
    d20.to_csv(DERIVED / "apportionment_pop_2020.csv", index=False)
    d10.to_csv(DERIVED / "apportionment_pop_2010.csv", index=False)
    ok20, _ = verify(d20, 2020)
    ok10, _ = verify(d10, 2010)
    # last seat / first seat missed, 2020 (sanity vs published: MN got the 435th seat, NY missed the 436th by 89 people)
    pops20 = dict(zip(d20["state"], d20["pop"]))
    pt = priority_table(pops20, 436)
    print("[2020] seat 435 ->", pt[-2][1], "seat 436 (first missed) ->", pt[-1][1])
    # published anchor: New York missed the 436th seat by 89 people
    import math as _m
    pv435 = pt[-2][3]
    s436, n436 = pt[-1][1], pt[-1][2]
    need = pv435 * _m.sqrt(n436 * (n436 - 1)) - pops20[s436]
    print(f"[2020] {s436} needed {need:,.1f} more people to take the 435th seat "
          f"(published figure: 89)")
    assert ok20 and ok10, "official apportionment not reproduced"
