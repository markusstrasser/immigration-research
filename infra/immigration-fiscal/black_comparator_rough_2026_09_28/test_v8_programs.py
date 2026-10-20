"""Economic carrier accounting: receipt storage and resource terms cannot leak."""
import rekey_sept29 as B


def test_signed_receipt_and_resource_carriers(monkeypatch):
    monkeypatch.setattr(B.W, 'CASE', 'oct16')
    monkeypatch.setattr(B.W, 'META', {'union_completion': {'carriers': {
        'receipt_carrier': {'kind': 'line', 'side': 'receipt', 'parent_line': 'corporate_capital'},
        'capital_carrier': {'kind': 'capital', 'parent_line': 'capital'},
        'production_carrier': {'kind': 'production', 'parent_line': 'production'}}}})
    rows = [('spending', 'receipt_carrier', 0., -3., 1.),
            ('spending', 'capital_carrier', 0., 6., 1.),
            ('spending', 'production_carrier', 0., -2., 1.),
            ('spending', 'education_services', 0., 2., 1.)]
    costs, gaps = B.by_program(rows, 0.)
    assert costs['capital, property, production taxes'] == -3.
    assert costs['schools and colleges'] == 2.
    assert sum(costs.values()) == -1.
    assert sum(gaps.values()) == 1.
    assert B.PER_HEAD not in costs
