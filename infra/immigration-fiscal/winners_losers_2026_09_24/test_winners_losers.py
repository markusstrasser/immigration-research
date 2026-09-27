"""Positive controls for the sister-lane ingestion and the allocation helpers, on a synthetic frame.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/winners_losers_2026_09_24/ -q
"""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("winners_losers", HERE / "winners_losers.py")
wl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(wl)


def frame():
    """Eight persons: seven other residents in California, Texas and Florida, and one group member."""
    return pd.DataFrame(dict(
        pw=[100.0, 200, 150, 50, 300, 100, 250, 400],
        other=[True] * 7 + [False],
        st=[6, 6, 6, 48, 48, 48, 12, 6],
        A_AGE=[10, 35, 70, 15, 40, 8, 50, 30],
        INDUSTRY=[0, 8680, 0, 0, 770, 0, 8680, 770],
        semp=[0, 5000, 0, 0, 0, 0, 20000, 0.0],
        wsal=[0, 30000, 0, 0, 50000, 0, 0, 20000.0],
        earn=[0, 35000, 0, 0, 50000, 0, 20000, 20000.0],
        MIG_ST=[0, 0, 0, 6, 0, 0, 6, 0],
        MIGSAME=[1, 1, 1, 2, 1, 1, 2, 1],
        metro_worker=[False, True, False, False, True, False, False, True],
        H_TENURE=[2, 2, 1, 1, 2, 2, 1, 2],
        n_other_hh=[2, 2, 1, 1, 1, 1, 1, 1],
        hh_other_ref=[True] * 7 + [False],
        HRNTVAL=[0, 0, 12000, 0, 0, 0, -3000, 0],
        race5=["nh_white"] * 3 + ["hispanic_other_origin"] * 2 + ["nh_black", "nh_white", "other"],
        native=[True] * 7 + [False],
        PRIV=[1, 1, 2, 1, 2, 1, 1, 1]))


def context(d):
    tax = d.earn.to_numpy() * 0.2 + 100.0
    naics = pd.DataFrame(dict(census_code=[8680, 770], naics=["722", "23"], exclude=["", ""],
                              description=["Restaurants", "Construction"]))
    return dict(tax_fed=tax * 0.6, tax_sl=tax * 0.4, q5=np.array([0, 1, 2, 3, 4, 0, 1, -1]), naics=naics)


def weighted_total(d, x):
    return float((d.pw.to_numpy() * x).sum() / 1e9)


def write_rows(lane: Path, rows: list[dict], result="**Verdict:** pending (test)"):
    (lane / "derived").mkdir(parents=True)
    pd.DataFrame(rows).to_csv(lane / "derived" / "winners_losers_rows.csv", index=False, lineterminator="\n")
    (lane / "RESULT.md").write_text(result + "\n")


def row(group, channel, direction, c, relation="beside", basis="modelled", key=None, pop="", cf="without the group"):
    r = dict(group=group, channel=channel, direction=direction, bn_low=c / 2 if c != "" else "", bn_central=c,
             bn_high=c * 2 if c != "" else "", population_m=pop, per_person_usd="", basis=basis,
             relation_to_account=relation, counterfactual=cf, source="test")
    if key is not None:
        r["key"] = key
    return r


def test_absent_and_malformed_files_stay_pending(tmp_path):
    d = frame()
    bad = tmp_path / "bad_lane"
    (bad / "derived").mkdir(parents=True)
    pd.DataFrame(dict(group=["x"], channel=["y"])).to_csv(bad / "derived" / "winners_losers_rows.csv", index=False)
    tbl, amounts = wl.ingest_sisters(d, context(d), wl.load_key_map(),
                                     {str(tmp_path / "absent_lane"): "absent", str(bad): "bad"})
    assert list(tbl.status) == ["pending", "pending"]
    assert "absent" in tbl.note.iloc[0] and "missing columns" in tbl.note.iloc[1]
    assert amounts == {}


def test_rows_are_allocated_signed_and_closed(tmp_path):
    d = frame()
    lane = tmp_path / "lane"
    write_rows(lane, [
        row("renters in California", "rent relief", "gain", 1.0, key="renters@CA"),
        row("local taxpayers", "tax base", "loss", 0.5),
        row("budget", "receipts", "gain", 2.0, relation="inside"),
        row("neighbours", "litter", "loss", "", basis="unpriced"),
        row("future taxpayers", "later receipts", "loss", 0.3),
        row("restaurant workers", "wages", "loss", 0.2, key="industry_worker:7225@CA"),
        row("anyone", "something", "loss", 0.1, key="no_such_template"),
    ])
    tbl, amounts = wl.ingest_sisters(d, context(d), wl.load_key_map(), {str(lane): "t"})
    status = dict(zip(tbl.group, tbl.status))
    assert status == {"renters in California": "allocated", "local taxpayers": "allocated", "budget": "role_only",
                      "neighbours": "role_only", "future taxpayers": "role_only",
                      "restaurant workers": "allocated", "anyone": "role_only"}
    assert tbl.set_index("group").loc["future taxpayers", "note"].startswith("no defensible key")
    assert "rejected" in tbl.set_index("group").loc["anyone", "note"]
    by = tbl.set_index("group")
    rent = amounts[by.loc["renters in California", "channel_id"]]
    for lev, v in (("low", 0.5), ("central", 1.0), ("high", 2.0)):
        assert weighted_total(d, rent[lev]) == pytest.approx(v, rel=1e-12)
    # Only California renter households headed by an other resident receive it; the group member none.
    assert np.flatnonzero(rent["central"]).tolist() == [0, 1]
    tax = amounts[by.loc["local taxpayers", "channel_id"]]["central"]
    assert weighted_total(d, tax) == pytest.approx(-0.5, rel=1e-12)
    assert tax[7] == 0 and (tax[:7] < 0).all()
    rest = amounts[by.loc["restaurant workers", "channel_id"]]["central"]
    assert np.flatnonzero(rest).tolist() == [1]   # the Florida restaurant worker and the group member excluded
    assert weighted_total(d, rest) == pytest.approx(-0.2, rel=1e-12)


def test_signed_rows_bounds_and_contradictions(tmp_path):
    d = frame()
    lane = tmp_path / "lane"
    signed = row("licensed restaurant owners", "sales change", "loss", -0.2, key="industry_owner:7225@CA")
    signed.update(bn_low=-0.4, bn_high=0.1)                  # a measured range that crosses zero
    wrong = row("restaurant owners", "sales change", "gain", -0.2, key="industry_owner:7225@CA")
    along = row("pupils", "dilution", "loss", 1.0, key="public_school_pupils")
    along.update(bn_low=-0.5, bn_high=2.0)                   # a loss whose low end is a gain
    write_rows(lane, [signed, row("licensed restaurant owners", "bound: every dollar lost", "loss", 0.5,
                                  key="industry_owner:7225@CA"), wrong, along])
    tbl, amounts = wl.ingest_sisters(d, context(d), wl.load_key_map(), {str(lane): "t"})
    assert list(tbl.status) == ["allocated", "allocated", "role_only", "allocated"]
    assert "ambiguous" in tbl.note.iloc[2]
    got = {lev: weighted_total(d, amounts[tbl.channel_id.iloc[0]][lev]) for lev in wl.LEVELS}
    assert got == pytest.approx({"low": -0.4, "central": -0.2, "high": 0.1}, rel=1e-12)
    got = {lev: weighted_total(d, amounts[tbl.channel_id.iloc[3]][lev]) for lev in wl.LEVELS}
    assert got == pytest.approx({"low": 0.5, "central": -1.0, "high": -2.0}, rel=1e-12)
    # an explicit key wins over the bound rule; without one the bound stays in the role table
    lane2 = tmp_path / "lane2"
    write_rows(lane2, [row("licensed restaurant owners", "bound: every dollar lost", "loss", 0.5)])
    tbl2, _ = wl.ingest_sisters(d, context(d), wl.load_key_map(), {str(lane2): "t2"})
    assert tbl2.status.iloc[0] == "role_only" and "bound" in tbl2.note.iloc[0]


def test_regional_breakdown_spreads_the_total(tmp_path):
    d = frame()
    lane = tmp_path / "lane"
    write_rows(lane, [
        row("other_residents_pupils", "dilution", "loss", 1.0, key="public_school_pupils"),
        row("other_residents_pupils:region=West", "dilution", "loss", 0.75, relation="overlaps:dilution"),
        row("other_residents_pupils:region=South", "dilution", "loss", 0.25, relation="overlaps:dilution"),
    ])
    tbl, amounts = wl.ingest_sisters(d, context(d), wl.load_key_map(), {str(lane): "t"})
    cid = tbl.channel_id.dropna().iloc[0]
    x = amounts[cid]["central"]
    west = d.st.eq(6).to_numpy()
    assert weighted_total(d, np.where(west, x, 0)) == pytest.approx(-0.75, rel=1e-12)
    assert weighted_total(d, np.where(~west, x, 0)) == pytest.approx(-0.25, rel=1e-12)
    assert "regional breakdown" in tbl.set_index("channel_id").loc[cid, "note"]


def test_key_templates_resolve_and_refuse(tmp_path):
    d = frame()
    ctx = context(d)
    k, m, _ = wl.resolve_key("interstate_movers:CA", d, ctx)
    assert np.flatnonzero(m).tolist() == [3, 6]
    k, m, _ = wl.resolve_key("landlords", d, ctx)
    assert np.flatnonzero(m).tolist() == [2, 6]   # rental income or loss
    k, m, _ = wl.resolve_key("public_school_pupils:q1", d, ctx)
    assert np.flatnonzero(m).tolist() == [0, 5]
    for bad in ("renters@ZZ", "industry_owner:ABC", "interstate_movers:XX", "unknown"):
        with pytest.raises(ValueError):
            wl.resolve_key(bad, d, ctx)


def test_map_row_to_key_reads_naics_and_states():
    km = wl.load_key_map()
    key, how = wl.map_row_to_key("compliance_gap_2026_09_24",
                                 dict(group="compliant owners in construction (NAICS 23)", channel="profits"), km)
    assert key == "industry_owner:23"
    key, _ = wl.map_row_to_key("movers_reasons_2026_09_24", dict(group="US-born adults leaving Texas", channel="x"), km)
    assert key == "interstate_movers:TX"
    key, _ = wl.map_row_to_key("x", dict(group="g", channel="c", key="renters@NY"), km)
    assert key == "renters@NY"
    # "City of LA" is Los Angeles, not Louisiana
    key, _ = wl.map_row_to_key("vending_restaurants_2026_09_24",
                               dict(group="budget", channel="sales tax not remitted (City of LA, 9.5%)"), km)
    assert key == "state_local_taxes@CA"


def test_rake_hits_both_margins():
    rng = np.random.default_rng(0)
    cell = rng.integers(0, 5, 400)
    state = rng.integers(0, 4, 400)
    seed = rng.uniform(0.5, 2.0, 400)
    cell_t = np.array([10.0, 20, 30, 25, 15])
    state_t = np.array([40.0, 30, 20, 10])
    x, it, err = wl.rake(seed, cell, state, cell_t, state_t)
    assert np.allclose(np.bincount(cell, weights=x, minlength=5), cell_t, rtol=1e-8)
    assert np.allclose(np.bincount(state, weights=x, minlength=4), state_t, rtol=1e-8)


def test_alloc_states_falls_back_and_records():
    d = frame()
    notes = {}
    key = np.where(d.st.eq(48), 0.0, 1.0)          # empty key in Texas
    out = wl.alloc_states(d, key, {6: 1.0, 48: 0.5}, fallback=d.earn.to_numpy(), notes=notes, label="t")
    assert weighted_total(d, out) == pytest.approx(1.5, rel=1e-12)
    tx = d.st.eq(48).to_numpy()
    assert weighted_total(d, np.where(tx, out, 0)) == pytest.approx(0.5, rel=1e-12)
    assert out[4] > 0 and out[3] == 0 and out[5] == 0    # Texas: only the earner, by the fallback
    assert notes["state_fallbacks"] == ["t: TX step 1"]


def test_counterfactual_phrasings():
    """The sister lanes' own phrasings (rows of 2026-09-25): only the group's or its pupils' absence counts."""
    yes = ["group's pupils absent; school spending responds at the account's 0.63-0.66 (its linear rule)",
           "without the group", "the group's absence", "The Mexican-origin group absent"]
    no = ["group's pupils absent, enrollment held: within-district effect of Hispanic share",
          "spending that fully follows enrollment (not the account's counterfactual of absence)",
          "the net movers stay; a transfer to other states", "California before SB 946 (vending a misdemeanor)",
          "no street-food vending at all", "the same workers paid on the books at the same gross wage",
          "without the conditions they cite they stay", ""]
    assert all(wl.counterfactual_is_absence(t) for t in yes)
    assert not any(wl.counterfactual_is_absence(t) for t in no)


def test_rows_off_the_account_counterfactual_stay_in_the_role_table(tmp_path):
    d = frame()
    lane = tmp_path / "lane"
    write_rows(lane, [
        row("restaurant owners", "sales", "gain", 0.3, key="industry_owner:7225@CA", cf="California before SB 946"),
        row("California budgets", "taxes moved", "loss", 0.7, key="state_local_taxes@CA", cf="the net movers stay"),
        row("other_residents_pupils", "dilution", "loss", 1.0, key="public_school_pupils",
            cf="group's pupils absent; school spending responds at the account's 0.63-0.66"),
    ])
    tbl, amounts = wl.ingest_sisters(d, context(d), wl.load_key_map(), {str(lane): "t"})
    assert list(tbl.status) == ["role_only", "role_only", "allocated"]
    assert all("not the group's absence" in n for n in tbl.note.iloc[:2])
    assert list(amounts) == [tbl.channel_id.iloc[2]]
    other = wl.sister_other_counterfactuals(tbl)
    assert list(other.counterfactual) == ["California before SB 946", "the net movers stay"]


def test_gate_stops_on_an_allocated_row_off_the_counterfactual():
    ok = pd.DataFrame(dict(lane=["x"], row=[0], status=["allocated"], counterfactual=["without the group"]))
    wl.check_sister_counterfactuals(ok)
    bad = pd.DataFrame(dict(lane=["x", "y"], row=[0, 3], status=["allocated", "allocated"],
                            counterfactual=["without the group", "the net movers stay"]))
    with pytest.raises(SystemExit, match="y:3"):
        wl.check_sister_counterfactuals(bad)


def test_role_only_lane_keeps_its_allocatable_rows_out_of_the_nets(tmp_path):
    """Under a case with a school response of 1 the school dilution rows stay in the role table."""
    d = frame()
    lane = tmp_path / "school_lane"
    write_rows(lane, [
        row("other_residents_pupils", "dilution", "loss", 1.0, key="public_school_pupils",
            cf="group's pupils absent; school spending responds at the account's 0.63-0.66"),
        row("other_residents_pupils:region=West", "dilution", "loss", 1.0, relation="overlaps:dilution"),
        row("taxpayers", "unfunded instruction", "gain", 2.0, relation="inside"),
    ])
    lanes = {str(lane): "t"}
    tbl, amounts = wl.ingest_sisters(d, context(d), wl.load_key_map(), lanes)
    assert list(tbl.status) == ["allocated", "role_only", "role_only"]
    tbl, amounts = wl.ingest_sisters(d, context(d), wl.load_key_map(), lanes,
                                     role_only={str(lane): wl.SCHOOL_DILUTION_ROLE_ONLY})
    assert list(tbl.status) == ["role_only"] * 3 and amounts == {}
    assert tbl.note.iloc[0] == wl.SCHOOL_DILUTION_ROLE_ONLY
    assert "inside the account" in tbl.note.iloc[2]   # rows kept out for their own reason keep it


def test_role_only_lanes_follow_the_school_response():
    wl.configure("sept26_schools")
    at = lambda school: {wl.CASE["model"]: dict(specs=pd.DataFrame(dict(school=school)))}  # noqa: E731
    assert wl.role_only_lanes(at([1, 1, 1])) == {"school_dilution_2026_09_24": wl.SCHOOL_DILUTION_ROLE_ONLY}
    assert wl.role_only_lanes(at([0.6522, 0.6813])) == {}
    assert "lower-response scenarios only" in wl.SCHOOL_DILUTION_ROLE_ONLY


def test_cases_chain_and_configure(tmp_path):
    for case in wl.RUNNABLE:
        c = wl.CASES[case]
        assert c["prev"] in wl.CASES and wl.CASES[c["prev"]]["model"] != c["model"]
        assert c["consumption_proposal"] == (case == "sept24")   # inside the fiscal channel from Sept 26 on
    assert wl.DEFAULT_CASE == "sept27" and wl.CASES["sept27"]["prev"] == "sept26_schools"
    assert wl.CASES["sept26_schools"]["prev"] == "sept26"
    assert len({wl.CASES[c]["model"] for c in wl.CASES}) == len(wl.CASES)
    # sept24 reads the paths it committed with; a later case its own lane, published totals and out-dir.
    wl.configure("sept24")
    assert wl.PATHS["bands"] == wl.FISCAL / "main_case_2026_09_24/derived/main_case_bands.csv"
    assert wl.PATHS["real_costs"] == wl.FISCAL / "sept24_propagation_2026_09_24/derived/real_costs_totals.csv"
    assert wl.PATHS["specs"] == wl.HERE / "derived" / "fiscal_specs.csv"
    assert wl.PINNED == {"generations": wl.GEN24_COMMIT, "debt_corrections": wl.DEBT24_FILES_COMMIT}
    assert wl.CASE["prev"]["case"] == "sept23" and wl.CASE["prev"]["base"] == wl.SEPT23_COMMIT
    wl.configure("sept26_schools", tmp_path)
    assert wl.PATHS["bands"] == wl.FISCAL / "main_case_schools_full_2026_09_26/derived/main_case_bands.csv"
    assert wl.PATHS["real_costs"] == wl.FISCAL / "sept26_propagation_2026_09_26/derived/real_costs_totals.csv"
    assert wl.PATHS["specs"] == tmp_path.resolve() / "fiscal_specs.csv" and wl.DERIVED == tmp_path.resolve()
    assert wl.PINNED == {"generations": wl.GEN26S_COMMIT, "debt_corrections": wl.DEBT26S_COMMIT}
    assert wl.CASE["prev"]["debt"] == wl.DEBT26_COMMIT and wl.CASE["prev"]["base"] == wl.BASE26_COMMIT
    assert not any(k in wl.PATHS for k in wl.CASE_PATHS)   # an earlier case reads none of September 27's inputs
    # September 27: its pins, its main profile beside the earlier cases' one, and its own inputs.
    wl.configure("sept27", tmp_path)
    assert wl.PATHS["bands"] == wl.FISCAL / "main_case_long_run_2026_09_27/derived/main_case_bands.csv"
    assert wl.PATHS["real_costs"] == wl.FISCAL / "sept27_propagation_2026_09_27/derived/real_costs_totals.csv"
    assert wl.PINNED == {"generations": wl.GEN27_COMMIT, "debt_corrections": wl.DEBT27_COMMIT}
    assert (wl.CASE["base"], wl.CASE["debt"]) == (wl.BASE27_COMMIT, wl.DEBT27_COMMIT)
    assert wl.CASE["prev"]["debt"] == wl.DEBT26S_COMMIT and wl.CASE["prev"]["base"] == wl.BASE26S_COMMIT
    assert wl.CASE["profile"] == "long_run_non_school_full" and "profile" not in wl.CASE["prev"]
    assert all(k in wl.PATHS for k in wl.CASE_PATHS)
    wl.configure("sept26_schools")
    assert not any(k in wl.PATHS for k in wl.CASE_PATHS)


def test_page_rows_follow_the_case():
    wl.configure("sept26_schools")
    assert wl.page_rows() == wl.PAGE
    wl.configure("sept27")
    ids = [r[0] for r in wl.page_rows()]
    assert len(ids) == len(wl.PAGE) + 2 and len(set(ids)) == len(ids)
    assert ids[ids.index("fiscal_b") + 1] == "displaced_beneficiaries"
    assert ids[ids.index("preferences_group_part") + 1] == "preferences_group_part_others"


def test_spm_pooling_keeps_totals_and_leaves_group_members_out():
    d = frame()
    d["target"] = ~d.other
    d["SPM_ID"] = [1, 1, 2, 3, 3, 3, 4, 2]  # unit 2 mixes an other resident with the group member
    d["PH_SEQ"] = [1, 1, 2, 3, 3, 3, 4, 2]
    pool, info = wl.spm_pooler(d)
    x = np.array([-500.0, 1500, -200, -800, 2400, -800, 300, 999])
    y = pool(x)
    other = d.other.to_numpy()
    assert np.isclose((d.pw * y)[other].sum(), (d.pw * x)[other].sum())
    assert y[7] == x[7] and y[2] == x[2]  # the group member keeps its own amount; its unit's other resident too
    assert np.isclose(y[0], (100 * -500 + 200 * 1500) / 300) and y[0] == y[1]
    assert np.isclose(info["other_in_mixed_units_m"], 150 / 1e6)
    y_equal = wl.spm_pooler(d.assign(pw=100.0))[0](x)  # equal weights: the members' sum over their number
    assert np.isclose(y_equal[3], (-800 + 2400 - 800) / 3)
