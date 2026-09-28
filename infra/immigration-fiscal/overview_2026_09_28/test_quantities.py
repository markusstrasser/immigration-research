"""Rendering and binding rules the evidence map's build relies on.

    uv run --no-project python3 -m pytest infra/immigration-fiscal/overview_2026_09_28/test_quantities.py -q
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import quantities as Q  # noqa: E402


def rec(rid="t", shape="ends", unit="$bn", mid="n5", ends="0", field="a=num:321.82 ;; b=num:387.37", expr="(a, b)",
        status="file", must_name="", forbid="", reader_note=""):
    return dict(id=rid, shape=shape, unit=unit, mid_round=mid, ends_round=ends, field=field, expr=expr,
                source_path="", status=status, must_name=must_name, forbid=forbid, reader_note=reader_note)


def test_mid_range_rounds_the_unrounded_ends_once():
    assert Q.render(rec(), (321.82, 387.37), "mid_range") == "$355bn (322–387)"


def test_range_across_zero_gives_each_end_its_sign():
    r = rec(shape="interval")
    assert Q.render(r, (-55.14, 71.06), "range") == "−55 to +71"
    assert Q.render(r, (-55.14, 71.06), "range_unit") == "−$55bn to +$71bn"


def test_range_below_zero_shares_one_sign_with_magnitudes_ascending():
    assert Q.render(rec(ends="1"), (-3.2005, -3.0966), "range_unit") == "−$3.1–3.2bn"


def test_thousands_comma_for_every_unit_but_years():
    assert Q.render(rec(shape="scalar", unit="x", mid="n100"), 4825.5, "value") == "4,800"
    assert Q.render(rec(shape="scalar", unit="year", mid="0"), 2005.0, "value") == "2005"


def test_fill_returns_the_span_of_each_rendering():
    recs = {"t": rec()}
    text, spans = Q.fill("It costs about {{q:t|mid_range}} a year.", recs=recs)
    assert text == "It costs about $355bn (322–387) a year."
    assert [(text[a:b], rid, view) for a, b, rid, view in spans] == [("$355bn (322–387)", "t", "mid_range")]


def test_approximate_record_needs_a_reader_note_and_is_marked():
    recs = {"t": rec(status="needs_file", reader_note="Scaled from {{q:u|value}}."),
            "u": rec("u", shape="scalar", unit="M", mid="1", field="a=num:39.7125", expr="a")}
    text, _ = Q.fill("{{q:t|mid}}", markup=True, recs=recs)
    assert text == '<span class="approx" title="Approximate. Scaled from 39.7M.">$355bn</span>'


def test_lint_reads_the_sentence_that_quotes_the_record():
    recs = {"t": rec(must_name="white")}
    assert Q.lint_unit("Against whites the gap is {{q:t|mid}}. Other text.", recs) == []
    [(rid, view, sentence, errs)] = Q.lint_unit("Whites differ. The gap is {{q:t|mid}}.", recs)
    assert (rid, sentence) == ("t", "The gap is $355bn.") and errs == ["names none of /white/"]


def test_a_typed_number_at_a_bound_site_fails():
    b = dict(file="groups.py", locator="social/f189/text", quantity_id="t", view="mid")
    assert Q.binding_errors(b, "Victims lose about {{q:t|mid}} a year.") == []
    assert "not at its site" in Q.binding_errors(b, "Victims lose about $355bn a year.")[0]


def test_a_table_row_must_carry_the_record_unrounded():
    recs = {"t": rec()}
    b = dict(file="build.py", locator="alternatives/x/value", quantity_id="t", view="pair")
    assert Q.value_binding_errors(b, (321.82, 387.37), "x", recs) == []
    assert "a typed number" in Q.value_binding_errors(b, (321.8, 387.4), "x", recs)[0]
