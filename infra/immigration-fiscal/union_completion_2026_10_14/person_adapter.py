"""Reuse the member pricing kernel without writing its lane or copying its code.

AST adapter stops main() immediately after construction of its priced pieces.
It retains each unmasked key at omitted rows before the kernel restricts it to
member rows. Pension receipts_of() retains the same member denominator but
also evaluates the numerator on omitted persons. All original gates execute.
Cash bypasses only the three accrual-specific line splits, using engine cash
rows. No gate, tolerance, weight, amount or member key is changed.
"""
from __future__ import annotations

import ast
import importlib.util
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "within_group_distribution_2026_09_29/households.py"


class Adapter(ast.NodeTransformer):
    def __init__(self):
        self.adds = self.receipts = self.stops = self.cash_splits = 0

    def visit_FunctionDef(self, node):
        if node.name == "main":
            # Locate the structural boundary; fail loudly if the upstream kernel changes.
            cut = [i for i, n in enumerate(node.body) if isinstance(n, ast.Delete)
                   and any(isinstance(t, ast.Name) and t.id == "prod_parts" for t in n.targets)]
            assert len(cut) == 1, "[BLOCKED] upstream piece boundary changed"
            node.body = node.body[:cut[0]] + ast.parse("return locals()").body
            self.stops += 1
        if node.name == "add":
            # Capture precisely the vectors the kernel receives, before its member mask.
            node.body = ast.parse("outside = x[EXTRA_ROWS].copy()").body + node.body
            at = next(i for i, n in enumerate(node.body) if isinstance(n, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == "piece" for t in n.targets))
            node.body[at+1:at+1] = ast.parse("""
piece['outside_x'] = outside
if alt is not None and cat == PENSION:
    part = {'social_security': 'oasdi', 'medicare': 'part_a'}[pid]
    piece['outside_alt'] = alt['person'][part][a][EXTRA_ROWS].copy()
if pid in payroll:
    key = row_of('receipt', pid)['key']
    piece['outside_tax'] = onbooks_key[key][a][EXTRA_ROWS].copy()
""").body
            self.adds += 1
        if node.name == "receipts_of":
            assign = [n for n in node.body if isinstance(n, ast.For)][0]
            v = [n for n in assign.body if isinstance(n, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id == "v" for t in n.targets)][0]
            assert isinstance(v.value, ast.Call) and len(v.value.args) == 3
            v.value = v.value.args[1]  # vector over all records
            aug = [n for n in assign.body if isinstance(n, ast.AugAssign)][0]
            den = [n for n in ast.walk(aug) if isinstance(n, ast.BinOp) and isinstance(n.op, ast.MatMult)]
            assert len(den) == 1
            den[0].left = ast.parse("v[m]", mode="eval").body
            den[0].right = ast.parse("w0[m]", mode="eval").body
            self.receipts += 1
        if node.name == "v4_split":
            # Cash SS is keyed to recorded benefits; Medicare to its payer cells;
            # FIT to recorded income tax, with no accrual benefit-tax subtraction.
            node.body[2:2] = ast.parse("""
if CASH_MODE and i in {'social_security', 'medicare', 'federal_income_tax'}:
    return None
""").body
            self.cash_splits += 1
        return self.generic_visit(node)


def kernel(extra_rows, basis, gate):
    spec = importlib.util.spec_from_file_location("union_member_kernel", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    tree = ast.parse(SOURCE.read_text())
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main")
    adapter = Adapter()
    fn = adapter.visit(fn)
    assert (adapter.adds, adapter.receipts, adapter.stops, adapter.cash_splits) == (1, 1, 1, 1)
    module.EXTRA_ROWS = extra_rows
    module.CASH_MODE = basis == "cash"
    module.CACHE = HERE / "_cache" / basis
    module.OUT = HERE / "derived"  # never used before the return boundary
    # Person-accrual cache remains read-only in the source lane.
    original_person = module.person_vectors
    def person_vectors(*args):
        own_cache, own_out = module.CACHE, module.OUT
        module.CACHE, module.OUT = SOURCE.parent / "_cache", SOURCE.parent / "derived"
        try:
            return original_person(*args)
        finally:
            module.CACHE, module.OUT = own_cache, own_out
    module.person_vectors = person_vectors
    def kernel_gate(label, ok, detail=""):
        gate("member_kernel: " + label, ok, detail=detail)
    module.gate = kernel_gate
    # Its tenant key is defined only on union records. Preserve that vector and
    # explicitly use age-band fallback for omitted records, rather than silently zero.
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn], type_ignores=[])), str(SOURCE), "exec"),
         module.__dict__)
    return module.main("row4", "oct14", "person", "onbooks")
