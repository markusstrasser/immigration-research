"""Regression checks for the audit's masks (audit_numbers.mask).

    uv run --no-project --offline python3 -m pytest infra/immigration-fiscal/number_drift_audit_2026_09_29/ -q
"""
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_numbers as A  # noqa: E402


def raws(text):
    return [t[2] for t in A.tokens(text)]


def test_index_headline_boundary_survives_case_and_number_changes(tmp_path):
    path = tmp_path / 'index.md'
    start, end = A.INDEX_SPANS[0]
    path.write_text('Outside $1bn\n**Adopted main case (October 15): $366–456bn/year**\n'
                    f'{end} outside $2bn\n')
    scanned = '\n'.join(text for _, text, _ in A.span_lines(path, [(start, end)]))
    assert raws(scanned) == ['$366–456bn']


def test_faq_complete_account_boundary_survives_number_change(tmp_path):
    path = tmp_path / 'faq.md'
    span = next(span for span in A.FAQ_SPANS if span[0] == 'figures are not the $')
    path.write_text('Outside $1bn; figures are not the $366–456bn complete account. [SOURCE: outside $2bn\n')
    scanned = '\n'.join(text for _, text, _ in A.span_lines(path, [span]))
    assert raws(scanned) == ['$366–456bn']


def test_index_history_and_social_boundaries_read_the_v9_and_pending_consumer_rows(tmp_path):
    assert '2026-10-16-main-case-v9.md' in A.INDEX_SPANS[1][1]
    for span, label in [(A.INDEX_SPANS[1], '$368.0–436.6bn'), (A.INDEX_SPANS[3], '$477.7–573.4bn')]:
        path = tmp_path / 'index.md'
        path.write_text(f'{span[0]}\n{label}\n{span[1]}\nOutside $1bn\n')
        scanned = '\n'.join(text for _, text, _ in A.span_lines(path, [span]))
        assert label in raws(scanned)
        assert '$1bn' not in raws(scanned)


def test_closed_budget_span_reads_the_qualified_current_law_text(tmp_path):
    span = next(s for s in A.FAQ_SPANS if s[0].startswith('Finding: the headline uses income-year'))
    path = tmp_path / 'faq.md'
    path.write_text(f'Outside $1bn\n{span[0]}\n$368–437bn\n{span[1]}\nOutside $2bn\n')
    scanned = '\n'.join(text for _, text, _ in A.span_lines(path, [span]))
    assert raws(scanned) == ['2024', '$368–437bn']


def test_fill_in_boundary_does_not_require_the_removed_historical_price(tmp_path):
    span = next(s for s in A.INDEX_SPANS if s[0].startswith('the fill-in-off companion'))
    path = tmp_path / 'index.md'
    path.write_text(f'Outside $9.6–9.9bn\n{span[0]}\n{span[1]} outside $422bn\n')
    scanned = '\n'.join(text for _, text, _ in A.span_lines(path, [span]))
    assert raws(scanned) == []


def test_faq_coverage_prices_and_da_constructions_are_in_scope(tmp_path):
    span = next(s for s in A.FAQ_SPANS if s[0].startswith("The surveys' count discrepancy"))
    path = tmp_path / 'faq.md'
    path.write_text(f'Outside $1bn\n{span[0]}\n+$12.7 / $15.6bn and $365.4–433.8bn\n{span[1]} outside $2bn\n')
    scanned = '\n'.join(text for _, text, _ in A.span_lines(path, [span]))
    assert raws(scanned) == ['+$12.7', '$15.6bn', '$365.4–433.8bn']


def test_faq_defense_screen_has_its_own_scan_boundary(tmp_path):
    span = next(s for s in A.FAQ_SPANS if s[0].startswith('A held-fixed screen'))
    path = tmp_path / 'faq.md'
    path.write_text(f'Outside $1bn\n{span[0]} of $47.5–72.0bn and $18.9bn\n$66.4–90.9bn\n{span[1]} outside $2bn\n')
    scanned = '\n'.join(text for _, text, _ in A.span_lines(path, [span]))
    assert raws(scanned) == ['$47.5–72.0bn', '$18.9bn', '$66.4–90.9bn']


def test_revised_generation_crime_and_incidence_spans_read_the_live_text(tmp_path):
    spans = [A.MEMO_SPANS[A.BY_GENERATION][0],
             next(s for s in A.FAQ_SPANS if s[0] == 'The main case does not isolate'),
             next(s for s in A.INDEX_SPANS if s[0] == 'The [debt legacy lane]'),
             A.MEMO_SPANS[A.REAL_COSTS][1]]
    for start, end in spans:
        path = tmp_path / 'memo.md'
        path.write_text(f'{start}\n$365.8–456.0bn\n{end}\nOutside $1bn\n')
        scanned = '\n'.join(text for _, text, _ in A.span_lines(path, [(start, end)]))
        assert '$365.8–456.0bn' in raws(scanned)
        assert '$1bn' not in raws(scanned)


def test_v9_consumer_spans_read_their_restated_text(tmp_path):
    # the docs pass on the v9 consumer lanes (2026-10-21) moved or added these boundaries
    starts = {
        A.INDEX: ["In the account's calibrated production model, not a measured wage effect, wages move",
                  "The [world ledger]"],
        A.FAQ: ["all ages and generations in income-year 2024, state and local services included"],
        A.REAL_COSTS: ["**The fiscal cost's incidence is a financing convention.**",
                       "Fiscal and social costs together come to **", "| Fiscal main case |",
                       "¹ Valuing deaths by remaining life-years"],
        A.WINNERS: ["**Verdict ("],
        A.INDIAN: ["**Verdict:** On main case", "Per member a year, low / high end of main case"],
    }
    for file, names in starts.items():
        for name in names:
            start, end = next(s for s in A.MARKDOWN[file] if s[0] == name)
            path = tmp_path / 'doc.md'
            path.write_text(f'Outside $1bn\n{start}\n$479.6–553.7bn\n{end} outside $2bn\nOutside $3bn\n')
            scanned = '\n'.join(text for _, text, _ in A.span_lines(path, [(start, end)]))
            assert '$479.6–553.7bn' in raws(scanned), name
            assert not {'$1bn', '$2bn', '$3bn'} & set(raws(scanned)), name


def test_world_ledger_bindings_use_the_renamed_other_resident_column():
    rows = [r for r in A.load_map().values() if 'world_ledger' in r['source_path']
            and 'other_us_residents_bn' in r['source_field']]
    assert len(rows) == 2
    assert all('|us_residents_bn' not in r['source_field'] for r in A.load_map().values()
               if 'world_ledger' in r['source_path'])
    assert all(A.resolve(r['source_path'], r['source_field'], r['expr']) for r in rows)


def test_an_all_digit_hash_is_masked_only_when_it_names_a_commit():
    # After 9e316341 the INDEX cited 73934145 and "audit 4827413"; both met the audit as unsourced quantities.
    hashes = subprocess.run(["git", "-C", str(A.ROOT), "rev-list", "--all"], capture_output=True, text=True,
                            check=True).stdout.split()
    commit = next(h[:8] for h in hashes if h[:8].isdigit())
    other = next(str(n) for n in range(10_000_000, 10_001_000) if not any(h.startswith(str(n)) for h in hashes))
    assert raws(f"audit {commit} §A, {other} people") == [other]
    # digits inside a decimal or a comma-grouped number are never read as a hash
    assert raws(f"0.{commit[:7]}") == [f"0.{commit[:7]}"]
    assert raws("39,712,493 people") == ["39,712,493"]
