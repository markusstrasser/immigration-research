"""Principal tests for the annual-to-period-profile boundary."""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

SPEC = importlib.util.spec_from_file_location("fiscal_lifetime", Path(__file__).with_name("lifetime.py"))
L = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(L)


def fixture_profiles():
    rows, components = [], []
    for allocation in ("personal", "shared"):
        for account in ("partial", "expanded"):
            for group in L.GROUPS:
                for band in range(8):
                    pop = 300.0 if group == "mexican_observed_total" else 100.0
                    balance = (band - 3) * 100.0 - (50 if account == "expanded" else 0)
                    row = dict(allocation=allocation, account=account, group=group, band=band,
                               population=pop, net_total=pop * balance, net_per_person=balance)
                    rows.append(row)
                    components.append({**row, "component": "cash", "signed_total": row["net_total"]})
    return pd.DataFrame(rows), pd.DataFrame(components)


def table():
    ages = np.arange(101)
    lx = 100000 * 0.98 ** ages
    return pd.DataFrame(dict(age=ages, lx=lx, Lx=lx * .99, qx=np.full(101, .02)))


def write_source(root):
    output = root / L.LANE / "derived"
    output.mkdir(parents=True)
    profiles, components = fixture_profiles()
    profiles.to_csv(output / "age_profiles.csv", index=False)
    components.to_csv(output / "age_profile_components.csv", index=False)
    source = root / "source.txt"
    source.write_text("authoritative source v1")
    audit = dict(inputs=[dict(path=str(source), sha256=L.sha256(source))],
                 item_metadata={"F|per_capita": {"national_dollars": 100.0}}, us_resident_population=10.0,
                 age_profile_export=dict(files={name: L.sha256(output / name)
                     for name in ("age_profiles.csv", "age_profile_components.csv")}))
    (output / "audit.json").write_text(json.dumps(audit))
    return output


def test_zero_rate_unit_balance_equals_remaining_person_years():
    t = table()
    for start in (0, 25, 65):
        value, years = L.survival_npv(np.ones(101), t, start, 0)
        assert value == pytest.approx(t.Lx.iloc[start:].sum() / t.lx.iloc[start])
        assert years == pytest.approx(value)


def test_finite_annuity_and_start_age_have_common_time_zero():
    t = pd.DataFrame(dict(lx=np.ones(101), Lx=np.ones(101)))
    values = np.full(101, 17.0)
    start, last, rate = 25, 82, .03
    expected = 17 * (1 - (1 + rate) ** -(last - start + 1)) / (1 - (1 + rate) ** -1)
    assert L.survival_npv(values, t, start, rate, last)[0] == pytest.approx(expected)
    values[:start] = 1e20
    assert L.survival_npv(values, t, start, rate, last)[0] == pytest.approx(expected)


def test_profiles_preserve_components_and_union():
    profiles, components = fixture_profiles()
    L.validate_profiles(profiles, components)
    components.loc[0, "signed_total"] += 10
    with pytest.raises(ValueError, match="reconstruct"):
        L.validate_profiles(profiles, components)


def test_missing_band_and_duplicate_are_refused():
    profiles, components = fixture_profiles()
    with pytest.raises(ValueError, match="age band"):
        L.validate_profiles(profiles.iloc[1:], components)
    with pytest.raises(ValueError, match="duplicate"):
        L.validate_profiles(pd.concat([profiles, profiles.iloc[:1]]), components)


def test_age_components_drive_lifetime_not_average_shift():
    profiles, _ = fixture_profiles()
    partial = L.age_vector(profiles, "mexico_born", "partial")
    mask = ((profiles.group == "mexico_born") & (profiles.account == "expanded")
            & (profiles.allocation == "personal"))
    profiles.loc[mask, "net_per_person"] = np.arange(8) ** 2
    expanded = L.age_vector(profiles, "mexico_born", "expanded")
    assert (expanded[0], expanded[25], expanded[100]) == (0, 4, 49)
    assert len(np.unique(expanded - partial)) > 1


def test_stale_annual_source_and_legacy_export_are_refused(tmp_path):
    output = write_source(tmp_path)
    L.load_age_profiles(tmp_path)
    (tmp_path / "source.txt").write_text("changed upstream")
    with pytest.raises(ValueError, match="stale source"):
        L.load_age_profiles(tmp_path)
    (output / "audit.json").write_text("{}")
    with pytest.raises(ValueError, match="predates"):
        L.load_age_profiles(tmp_path)


def test_revised_profile_file_is_refused(tmp_path):
    output = write_source(tmp_path)
    with (output / "age_profiles.csv").open("a") as stream:
        stream.write("\n")
    with pytest.raises(ValueError, match="stale annual"):
        L.load_age_profiles(tmp_path)


def test_full_grid_has_same_start_reference_and_proxy_metadata():
    profiles, _ = fixture_profiles()
    t = table()
    result = L.calculate(profiles, {key: t for key in L.TABLES})
    assert len(result) == 768
    assert result[result.group == "all_native"].mortality_table.eq("total").all()
    assert result[result.group == "third_plus_nh_white"].npv_difference_vs_white_same_start.eq(0).all()
    assert set(result[result.primary].allocation) == {"personal"}
    assert set(result[result.primary].account) == {"expanded"}


def test_generate_roundtrip_and_modified_output_refused(tmp_path):
    write_source(tmp_path)
    cache = tmp_path / L.LIFE_LANE / "_cache"
    cache.mkdir(parents=True)
    t = table()
    for number in L.TABLES.values():
        frame = pd.DataFrame({0: [f"{a}-{a+1}" for a in range(100)] + ["100 and over"],
                              1: t.qx, 2: t.lx, 3: np.zeros(101), 4: t.Lx})
        frame.to_excel(cache / f"lt2024_Table{number}.xlsx", index=False, header=False)
    output = tmp_path / "result"
    result = L.generate(tmp_path, output)
    assert len(L.load_period_profiles(output, tmp_path)) == len(result)
    with (output / "period_profiles.csv").open("a") as stream:
        stream.write("\n")
    with pytest.raises(ValueError, match="altered/stale"):
        L.load_period_profiles(output, tmp_path)


def test_debt_year_end_annuity_and_real_zero_interest():
    sys.path.insert(0, str(Path(__file__).parent))
    path = Path(__file__).parent.parent / "gap_interest_2026_09_18/interest_on_gap.py"
    spec = importlib.util.spec_from_file_location("debt_probe", path)
    debt = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(debt)
    result = debt.financing_path(-100, .03, 10, .5)
    assert result["debt_bn"] == pytest.approx(50 * ((1.03) ** 10 - 1) / .03)
    assert result["principal_bn"] == 500
    assert debt.financing_path(-100, 0, 10, .5)["interest_component_bn"] == 0
    assert debt.financing_path(-100, .03, 10, 0)["debt_bn"] == 0


def test_homicide_uses_age_components_and_mixes_sentence_npvs(tmp_path):
    sys.path.insert(0, str(Path(__file__).parent))
    path = Path(__file__).parent.parent / "homicide_cost_2026_09_18/cost_model.py"
    spec = importlib.util.spec_from_file_location("homicide_probe", path)
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    profiles, _ = fixture_profiles()
    t = table()
    partial = model.by_age(profiles, "all_native", "partial")
    expanded = model.by_age(profiles, "all_native", "expanded")
    assert model.remaining(partial, 25, .03, t) != model.remaining(expanded, 25, .03, t)
    finite = model.offender_cost(25, "nh_black", profiles, t, 0, .03, "expanded")
    life = model.offender_cost(25, "nh_black", profiles, t, 1, .03, "expanded")
    mixed = model.offender_cost(25, "nh_black", profiles, t, .2, .03, "expanded")
    assert mixed["total"] == pytest.approx(.8 * finite["total"] + .2 * life["total"])
    with pytest.raises(ValueError, match="audit is missing"):
        model.load_current_results(tmp_path)
