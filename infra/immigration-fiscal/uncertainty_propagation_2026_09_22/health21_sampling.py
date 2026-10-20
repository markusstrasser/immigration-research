"""Read-only adapter of item21's own fiscal builder, stopped before all writes.

The AST boundary is deliberately unique and fail-loud. The producer remains
authoritative for dollar blocks, native-child prices and raw donor support.
Native-First: execute the immutable producer prefix and its own price callback.
"""
from __future__ import annotations

import ast
import copy
import importlib.util
import os
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "spending_keys_r5_2026_10_15"
sys.path.insert(0, str(SOURCE))


def readonly_producer_tree(path):
    tree = ast.parse(path.read_text(), filename=str(path))
    main = next(q for q in tree.body if isinstance(q, ast.FunctionDef) and q.name == "main")
    hits = sorted((node for node in ast.walk(main) if isinstance(node, ast.Assign)
                   and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name)
                   and node.value.func.id == "coverage_build"), key=lambda q: q.lineno)
    # Final source emits both source-rate and selected-common-rate coverage.
    names = [q.targets[0].id if len(q.targets) == 1 and isinstance(q.targets[0], ast.Name) else None for q in hits]
    if names != ["cov", "cov_v9"]:
        raise ValueError("[BLOCKED] item21 read-only boundary changed")
    boundary = hits[0]

    class StopBeforeCoverage(ast.NodeTransformer):
        def visit_Assign(self, node):
            if node is boundary:
                return ast.copy_location(ast.Return(ast.Call(ast.Name("locals", ast.Load()), [], [])), node)
            return self.generic_visit(node)

    tree = StopBeforeCoverage().visit(tree)
    # Remove only the script entry point; retain producer conditional declarations.
    tree.body = [q for q in tree.body if not (isinstance(q, ast.If)
                 and isinstance(q.test, ast.Compare) and isinstance(q.test.left, ast.Name)
                 and q.test.left.id == "__name__" and len(q.test.ops) == 1
                 and isinstance(q.test.ops[0], ast.Eq) and len(q.test.comparators) == 1
                 and isinstance(q.test.comparators[0], ast.Constant)
                 and q.test.comparators[0].value == "__main__")]
    return ast.fix_missing_locations(tree)


class Builder:
    def __init__(self):
        self.guard = {"active": False}
        def deny_writer(event, args):
            if not self.guard["active"]:
                return
            writing = event == "open" and (args[2] or 0) & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)
            if writing or event in {"os.mkdir", "os.remove", "os.rename", "os.rmdir"}:
                raise ValueError("[BLOCKED] item21 read-only source reached a writer: "+event)
        sys.addaudithook(deny_writer)
        path = SOURCE / "health_residual.py"
        tree = readonly_producer_tree(path)
        self.ns = {"__file__": str(path), "__name__": "uncertainty_readonly_item21"}
        exec(compile(tree, str(path), "exec"), self.ns)
        self.guard["active"] = True
        try:
            self.original = self.ns["inputs"]()
        finally:
            self.guard["active"] = False
        self.ns["ARMS"] = ("central",)
        self.guard["active"] = True
        try:
            weights = self.ns["source_weights"](*self.original[:5])
        finally:
            self.guard["active"] = False
        self.ns["source_weights"] = lambda *args: weights
        self.central = self.evaluate()

    def evaluate(self, ratio_cell=None, donor_cell=None, increment=0.):
        values = list(self.original)
        d = values[0]
        bands = np.digitize(d.A_AGE.to_numpy(), [18, 35, 50, 65])
        born = np.where(d.PENATVTY.eq(57), 1, 2)
        if ratio_cell is not None:
            band, nativity = ratio_cell
            ratios = dict(values[7])
            ratios["central"] = ratios["central"].copy()
            ratios["central"][(bands == band) & (born == nativity)] += increment
            values[7] = ratios
        if donor_cell is not None:
            band, nativity = donor_cell
            keys = dict(values[5])
            keys["new"] = keys["new"].copy()
            exposure = ~(d.PUB.eq(0) & d.PRIV.eq(0)).to_numpy()
            keys["new"][(bands == band) & (born == nativity) & exposure] += increment
            values[5] = keys
        self.ns["inputs"] = lambda: tuple(values)
        self.guard["active"] = True
        try:
            return self.ns["main"]()
        finally:
            self.guard["active"] = False

    @staticmethod
    def vectors(local, data, audit, basis, reading, rate):
        observed = np.zeros(len(data["weights"]))
        constructed = observed.copy()
        added = observed.copy()
        pieces = local["prices"](data, audit, basis, "oct15_final_routing")
        count = 0
        for piece in pieces:
            if piece["end"] != reading:
                continue
            multiplier = rate/(.02 if reading == "low" else .03) if piece["source_side"] == "capital" else 1.
            a = multiplier*piece["base_price"]
            b = multiplier*piece["constructed_price"]
            scope = piece["population"]
            if scope in ("identified", "both"):
                observed += a
                constructed += b
            if scope in ("added", "both"):
                added += a
            count += 1
        if count != len(local["blocks"]["a"]):
            raise ValueError("[BLOCKED] item21 actual dollar-block coverage differs")
        raw_expected = sum(q.get("delta_bn", q.get("capital_stock_delta_bn", 0.)*rate)
                           for q in local["blocks"]["a"])
        actual = observed @ data["weights"][:, 0] + added @ data["added_weights"][:, 0]
        if abs(actual-raw_expected) > 1e-9:
            raise ValueError(f"[BLOCKED] item21 aggregate no-duplication closure: {actual} vs {raw_expected}")
        return observed, constructed, added

    def gradients(self, data, audit, basis, reading, rate, weights, missing, added_weights, cells, donor=False):
        """Dollar gradients of the full own-source term, holding fiscal coefficients."""
        central = self.vectors(self.central, data, audit, basis, reading, rate)
        baseline = central[0]@weights+central[1]@missing+central[2]@added_weights
        result = []
        # The ratios enter linearly. Donor means enter normalized shares; use
        # central differences and verify a tenfold step refinement.
        for cell in cells:
            band = self.ns["BANDS"].index(cell["band"])
            nativity = 1 if cell["nativity"] == "us_born" else 2
            if not donor:
                local = self.evaluate(ratio_cell=(band, nativity), increment=1.)
                price = self.vectors(local, data, audit, basis, reading, rate)
                result.append(float(price[0]@weights+price[1]@missing+price[2]@added_weights-baseline))
            else:
                estimates = []
                for h in (.01, .001):
                    endpoints = []
                    for sign in (-1, 1):
                        local = self.evaluate(donor_cell=(band, nativity), increment=sign*h)
                        price = self.vectors(local, data, audit, basis, reading, rate)
                        endpoints.append(price[0]@weights+price[1]@missing+price[2]@added_weights)
                    estimates.append((endpoints[1]-endpoints[0])/(2*h))
                if abs(estimates[0]-estimates[1]) > max(1e-7, abs(estimates[1])*1e-5):
                    raise ValueError("[BLOCKED] item21 donor gradient step convergence")
                result.append(float(estimates[1]))
        return result

    def donor_covariance(self):
        import propagate as P
        M = self.ns["M"]
        root = self.ns["ROOT"]
        md, _ = M.read_meps(root/"sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip",
                            root/"sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256su.txt")
        donor = md.copy()
        donor["public_paid"] = donor.TOTOFD24+donor.TOTSTL24
        cells, _, expected = M.donor_model(donor, self.original[0], False)
        payers = {**P.MEDICAL, "residual_ofd_stl": ["TOTOFD24", "TOTSTL24"]}
        cov = P.payer_covariance(md, cells, payers)
        if np.linalg.eigvalsh(cov).min() < -1e-10*np.diag(cov).max():
            raise ValueError("[BLOCKED] item21 joint payer covariance is not PSD")
        if not np.allclose(cov[-10:, -10:], expected, rtol=1e-10, atol=1e-12):
            raise ValueError("[BLOCKED] item21 joint donor covariance oracle")
        return cov.tolist(), [q for q in self.original[8] if q["key"] == "new"]
