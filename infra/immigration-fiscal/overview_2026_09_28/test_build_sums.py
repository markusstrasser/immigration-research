"""The build's gates: in every ledger block the printed lines add to the printed total, a claim the prose makes in
words holds on its record, and the template's build fragment is cut out exactly once.

    uv run --no-project python3 -m pytest infra/immigration-fiscal/overview_2026_09_28/test_build_sums.py -q
"""

import sys
from decimal import Decimal
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402


def row(kind, label, low, high, signed=True):
    return f'<tr class="item" data-sum="{kind}"><td>{label}</td>{B.cells([Decimal(low), Decimal(high)], signed)}</tr>'


def test_a_running_total_that_reads_as_bad_arithmetic_fails():
    # the operator's example at whole billions: 295 + 77 is printed as 371
    table = (row("start", "Main estimate", "295", "362", False) + row("step", "Pensions", "77", "73")
             + row("running", "= total", "371", "435", False))
    assert B.displayed_sum_errors(table) == ["'Pensions', low end: the parts add to 372, the table prints 371"]
    table = (row("start", "Main estimate", "294.7", "361.8", False) + row("step", "Pensions", "76.7", "73.0")
             + row("running", "= total", "371.4", "434.8", False))
    assert B.displayed_sum_errors(table) == []


def test_ledger_lines_must_add_to_their_subtotal_and_subtotals_to_the_total():
    parts = [("-70.1", "-60.3"), ("-51.0", "-53.6"), ("48.7", "50.3"), ("-13.3", "-8.8"), ("-4.1", "-4.1")]
    table = (row("subtotal", "Own taxes and benefits", "-89.8", "-76.4") + "".join(row("part", "x", *p) for p in parts)
             + row("total", "Main estimate", "-89.8", "-76.4", False))
    assert B.displayed_sum_errors(table) == [
        "'Own taxes and benefits', high end: the parts add to -76.5, the table prints -76.4"]


def test_a_table_with_no_marked_sums_fails():
    assert B.displayed_sum_errors("<table></table>") == [
        "no printed sums found (the rows lost their data-sum marks?)"]


def test_the_built_tables_add_and_rounding_each_line_alone_breaks_them():
    s, _bands, stairs, _arms = B.load_numbers()
    rows = B.waterfall_rows(s, stairs)
    tables = lambda: [B.ledger_html(rows)[0], B.alternatives_html(rows)[0]]  # noqa: E731
    assert [B.displayed_sum_errors(t) for t in tables()] == [[], []]
    try:
        B.ROUND_EACH = True
        # on v9 the alternatives' whole-billion steps add even when each is rounded alone, so only the ledger can
        # serve as the positive control (the synthetic running sum above covers the alternatives' check)
        ledger, _alternatives = tables()
        assert B.displayed_sum_errors(ledger)
    finally:
        B.ROUND_EACH = False


def test_the_prose_sums_add_as_printed_and_break_when_a_part_moves():
    recs = B.Q.load_registry()
    assert B.prose_sum_errors(recs) == []
    moved = {k: dict(v) for k, v in recs.items()}
    moved["social.items"]["expr"] = "(l - 10, h)"
    assert B.prose_sum_errors(moved) == [
        "the main estimate plus the costs outside the budget, low end: the parts print as 470, pairing.total as 480"]
    moved = {k: dict(v) for k, v in recs.items()}
    moved["cash.unplaced"]["expr"] = "(u1 + p1 + 2, u2 + p2)"
    assert B.prose_sum_errors(moved) == [
        "the time map's plain entries, low end: the parts print as 370, case.main as 368"]


def test_a_claim_in_words_holds_on_the_page_and_fails_when_its_record_moves():
    import groups as G
    recs = B.Q.load_registry()
    sites = B.text_sites((B.HERE / "template.html").read_text(), G.GROUPS)
    assert B.prose_claim_errors(sites, recs) == []
    moved = {k: dict(v) for k, v in recs.items()}
    moved["world.other_us_residents"]["expr"] = "(max(l1, l2, l3), 1.0)"
    assert B.prose_claim_errors(sites, moved) == [
        "'Other US residents lose at any weight' needs other US residents' line below zero at both ends in every "
        "reading; world.other_us_residents is (-306.536379285804, 1.0)"]
    assert B.prose_claim_errors({}, recs) == [
        "'Other US residents lose at any weight' stands on no text site: drop its claim or restore the sentence"]


def test_the_capital_return_total_must_say_the_enterprises_are_in():
    [(rid, _view, _sentence, errs)] = B.Q.lint_unit("Return on public capital: about "
                                                     "{{q:capital_return.total|mid_range}}. In the total.")
    assert (rid, errs) == ("capital_return.total", ["names none of /enterprise/"])


def test_the_build_fragment_is_cut_once_and_its_headings_open_the_contents():
    frag = '\n<h3 id="build">How the total is built</h3>\n<p>{{LEDGER}}</p>\n<h3 id="objects">One <b>year</b></h3>\n'
    page = f"<h2>a</h2>{{{{GROUPS}}}}{B.BUILD_START}{frag}{B.BUILD_END}<h2>b</h2>"
    rest, cut = B.cut_build_block(page)
    assert (rest, cut) == ("<h2>a</h2>{{GROUPS}}<h2>b</h2>", frag)
    assert B.build_toc(cut) == [("build", "How the total is built"), ("objects", "One year")]
    assert B.cut_build_block("<h2>a</h2>") == ("<h2>a</h2>", None)  # a template from before the build part
    for broken in (page + B.BUILD_START + B.BUILD_END, page.replace(B.BUILD_END, ""),
                   f"{B.BUILD_END}{frag}{B.BUILD_START}"):
        with pytest.raises(SystemExit, match="needs one"):
            B.cut_build_block(broken)
    with pytest.raises(SystemExit, match="no <h3 id"):
        B.build_toc("<h3>No anchor</h3>")
