"""Native-immigrant nest inside each skill cell of the stationary CES account.

Generalizes `matched_benefits_2026_09_19/model.py:equilibrium()` by replacing the
scalar cell quantity ``x[j]`` with a CES aggregate over branches. Everything above
the cell (``q``, output, capital, the tax partition) keeps its present form, so
`fiscal_and_private()` is reused verbatim.

Conditional model assumptions under a stationary comparison, never identified
policy effects. The elasticity between branches is transported, not estimated on
this population.
"""
from __future__ import annotations

import numpy as np

TOLERANCE = 1e-12
ITERATIONS = 5000
DAMPING = (.75, .9)


class Nest:
    """One CES node. ``weights`` carries the child axis first, then skill.

    ``children`` holds either an integer leaf index or a nested ``Nest``.
    """

    __slots__ = ("kappa", "weights", "children")

    def __init__(self, kappa, weights, children):
        weights = np.asarray(weights, float)
        if len(children) != weights.shape[0] or not len(children):
            raise ValueError("Nest weights must match the child count")
        if not np.isfinite(weights).all() or np.any(weights <= 0):
            raise ValueError("Nest weights must be finite and strictly positive")
        if not np.isfinite(kappa) and kappa != 1.:
            raise ValueError("Nest exponent must be finite; use kappa=1 for perfect substitution")
        self.kappa, self.weights, self.children = float(kappa), weights, tuple(children)


def kappa_of(elasticity):
    """CES exponent for a substitution elasticity; exact 1 at infinity."""
    elasticity = float(elasticity)
    if np.isnan(elasticity) or elasticity <= 0:
        raise ValueError("Substitution elasticity must be positive")
    return 1. if np.isinf(elasticity) else 1 - 1 / elasticity


def leaves_of(node):
    out = []
    for child in node.children:
        out.extend([int(child)] if isinstance(child, (int, np.integer)) else leaves_of(child))
    return out


def aggregate(node, quantities):
    """Return the node value and d(value)/d(leaf) for every leaf beneath it."""
    values, grads = [], []
    for child in node.children:
        if isinstance(child, (int, np.integer)):
            values.append(quantities[int(child)])
            grads.append({int(child): 1.})
        else:
            value, grad = aggregate(child, quantities)
            values.append(value)
            grads.append(grad)
    stack, weights = np.stack(values), node.weights
    if abs(node.kappa) < TOLERANCE:
        total = np.exp((weights * np.log(stack)).sum(axis=0))
        partial = total * weights / stack
    else:
        powered = (weights * stack**node.kappa).sum(axis=0)
        total = powered**(1 / node.kappa)
        partial = weights * stack**(node.kappa - 1) * powered**(1 / node.kappa - 1)
    out = {}
    for part, grad in zip(partial, grads):
        for leaf, inner in grad.items():
            out[leaf] = out.get(leaf, 0.) + part * inner
    return total, out


def prune(node, dropped):
    """Drop leaves exactly: remove their term from the aggregate, not a floor."""
    weights, children = [], []
    for weight, child in zip(node.weights, node.children):
        if isinstance(child, (int, np.integer)):
            if int(child) in dropped:
                continue
        else:
            child = prune(child, dropped)
            if child is None:
                continue
        weights.append(weight)
        children.append(child)
    if not children:
        return None
    return Nest(node.kappa, np.stack(weights), children)


def two_level(branch_shares, sigma_ni):
    """Cell CES over branches. Leaves are numbered in branch order."""
    branch_shares = np.asarray(branch_shares, float)
    return Nest(kappa_of(sigma_ni), branch_shares, tuple(range(branch_shares.shape[0])))


def three_level(branch_shares, sigma_ni, parent, sub_shares, sub_sigma):
    """Branch ``parent`` becomes a CES sub-nest at ``sub_sigma``.

    Leaves are numbered depth-first: branches before ``parent`` keep their index,
    the sub-branches occupy ``parent .. parent + S - 1``, later branches shift up.
    """
    branch_shares, sub_shares = np.asarray(branch_shares, float), np.asarray(sub_shares, float)
    count, inner = branch_shares.shape[0], sub_shares.shape[0]
    if not 0 <= parent < count:
        raise ValueError("Sub-nest parent is not a branch")
    children, cursor = [], 0
    for index in range(count):
        if index == parent:
            children.append(Nest(kappa_of(sub_sigma), sub_shares,
                                 tuple(range(cursor, cursor + inner))))
            cursor += inner
        else:
            children.append(cursor)
            cursor += 1
    return Nest(kappa_of(sigma_ni), branch_shares, children)


def _check_inputs(shares, removed, sigma, labor_share, adjustment, elasticity, dropped, alive):
    if shares.shape[0] != 2:
        raise ValueError("Require a two-skill compensation share array")
    if not np.isfinite(shares).all() or not np.isfinite(removed).all():
        raise ValueError("Nonfinite calibration")
    if np.any(shares <= 0) or not np.allclose(shares.sum(axis=0), 1):
        raise ValueError("Skill compensation shares must sum to one")
    if np.any((removed < 0) | (removed > 1)):
        raise ValueError("Branch removal share outside [0,1]")
    if np.any(removed[alive] >= 1):
        raise ValueError("An undropped branch cannot be fully removed")
    if dropped and not np.allclose(removed[sorted(dropped)], 1):
        raise ValueError("A dropped branch must carry removal share one")
    if not (sigma > 0 and 0 < labor_share < 1 and 0 <= adjustment <= 1 and 0 <= elasticity <= 1):
        raise ValueError("Invalid model parameter")


def solve(shares, tree, removed, sigma=2., labor_share=.65, adjustment=1.,
          elasticity=0., dropped=()):
    """Remove branch labor from a nested cell aggregate; sign is with minus without.

    ``removed[i]`` is branch ``i``'s removed share of its own current earnings.
    Dropped branches leave the counterfactual aggregate entirely (exact removal)
    and earn nothing; their removal share must be one.
    """
    shares, removed = np.asarray(shares, float), np.asarray(removed, float)
    order = leaves_of(tree)
    if sorted(order) != list(range(len(order))) or removed.shape[0] != len(order):
        raise ValueError("Leaf indices must be a dense range matching removed")
    dropped = tuple(sorted(int(index) for index in dropped))
    alive = np.array([index not in dropped for index in range(len(order))])
    _check_inputs(shares, removed, sigma, labor_share, adjustment, elasticity, dropped, alive)
    base = aggregate(tree, np.ones_like(removed))[1]
    base_weights = np.stack([base[index] for index in range(len(order))])
    if not np.allclose(base_weights.sum(axis=0), 1, rtol=0, atol=1e-12):
        raise ValueError("Branch shares of a cell must sum to one")
    cut = prune(tree, set(dropped))
    if cut is None:
        raise ValueError("Every branch dropped; no counterfactual economy remains")
    rho = 1. if np.isinf(sigma) else 1 - 1 / sigma
    power = labor_share + adjustment * (1 - labor_share)
    live = alive.reshape((-1,) + (1,) * (removed.ndim - 1))
    surviving = np.where(live, 1 - removed, 1.)

    def evaluate(log_hours):
        quantities = surviving * np.exp(log_hours)
        cell, grad = aggregate(cut, quantities)
        log_q = ((shares * np.log(cell)).sum(axis=0) if abs(rho) < TOLERANCE
                 else np.log((shares * cell**rho).sum(axis=0)) / rho)
        marginal = np.stack([grad.get(index, np.ones_like(cell)) for index in range(len(order))])
        # A dropped branch has no counterfactual marginal product; report it inert
        # (wage ratio one) so it can never enter the fixed point or a total.
        log_wage = np.where(live, (power - rho) * log_q + (rho - 1) * np.log(cell)
                            + np.log(marginal) - np.log(base_weights), 0.)
        return cell, log_q, log_wage

    for weight in DAMPING:
        log_hours = np.zeros_like(removed)
        for iteration in range(ITERATIONS):
            cell, log_q, log_wage = evaluate(log_hours)
            desired = elasticity * log_wage
            error = float(np.max(np.abs(desired - log_hours)))
            if error < TOLERANCE:
                break
            log_hours = weight * log_hours + (1 - weight) * desired
        else:
            continue
        break
    else:
        raise ValueError("Labor-supply fixed point did not converge")
    hours, wage, q = np.exp(log_hours), np.exp(log_wage), np.exp(log_q)
    output, capital = q**power, q**adjustment
    current_pay = labor_share * shares * base_weights * (1 - removed)
    counterfactual_pay = np.where(live, current_pay * hours * wage, 0.)
    labor_gain = current_pay - counterfactual_pay
    domestic_capital_gain = (1 - labor_share) * (1 - output)
    opportunity_income = (1 - labor_share) * (1 - capital)
    capital_gain = domestic_capital_gain - opportunity_income
    # Euler exhaustion on domestic output; opportunity income sits outside the
    # modeled production sector, exactly as in the unnested model.
    cell_pay = labor_share * shares * q**(power - rho) * cell**rho
    if not np.allclose(counterfactual_pay.sum(axis=0), cell_pay, rtol=1e-10, atol=1e-12):
        raise ValueError("Counterfactual branch Euler conservation failed within a skill cell")
    if not np.allclose(counterfactual_pay.sum(axis=(0, 1)), labor_share * output,
                       rtol=1e-10, atol=1e-12):
        raise ValueError("Counterfactual Euler conservation failed")
    disutility_difference = np.zeros_like(current_pay)
    if elasticity:
        disutility_difference = current_pay * elasticity / (1 + elasticity) * (
            1 - hours**(1 + 1 / elasticity))
    return dict(labor_gain=labor_gain.sum(axis=0), capital_gain=capital_gain,
                domestic_capital_gain=domestic_capital_gain,
                opportunity_income=opportunity_income,
                gross_income_gain=labor_gain.sum(axis=(0, 1)) + capital_gain,
                disutility_difference=disutility_difference.sum(axis=0),
                labor_gain_by_branch=labor_gain, current_pay_by_branch=current_pay,
                counterfactual_pay_by_branch=counterfactual_pay,
                disutility_by_branch=disutility_difference,
                branch_share_of_cell=base_weights,
                wage_without_over_with=wage, hours_without_over_with=hours,
                cell_quantity_without_over_with=cell,
                output_without_over_with=output, capital_without_over_with=capital,
                iterations=iteration, fixed_point_error=error, damping=weight)


def nested_equilibrium(shares, branch_shares, removed, sigma=2., sigma_ni=np.inf,
                       labor_share=.65, adjustment=1., elasticity=0., dropped=()):
    """Two-level entry point: skill cells over a single CES nest of branches."""
    tree = two_level(branch_shares, sigma_ni)
    return solve(shares, tree, removed, sigma, labor_share, adjustment, elasticity, dropped)


def linearized_wage_response(shares, branch_shares, cell, sigma, sigma_ni, log_shock,
                             shocked=1):
    """First-order branch wage response to a log shock in one branch of one cell.

    Holds only at full capital adjustment (adjustment = 1, power = 1) and fixed
    labor supply. Reproduces the same-group and cross-group coefficients recorded
    in `research/immigration-marginal-revolution-leads-read-2026-09-21.md` section 3
    and adds the shocked branch's own counterpart.
    """
    shares, branch_shares = np.asarray(shares, float), np.asarray(branch_shares, float)
    if shares.shape != (2,) or branch_shares.ndim != 2 or branch_shares.shape[1] != 2:
        raise ValueError("Linearization takes point estimates with two skill cells")
    inverse_sigma = 0. if np.isinf(sigma) else 1 / sigma
    inverse_epsilon = 0. if np.isinf(sigma_ni) else 1 / sigma_ni
    removed_share = branch_shares[shocked, cell]
    same = removed_share * (inverse_epsilon - (1 - shares[cell]) * inverse_sigma) * log_shock
    other = removed_share * shares[cell] * inverse_sigma * log_shock
    out = np.zeros_like(branch_shares)
    for branch in range(branch_shares.shape[0]):
        out[branch, cell] = same
        out[branch, 1 - cell] = other
    out[shocked, cell] = same - inverse_epsilon * log_shock
    return out
