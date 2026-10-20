"""Household statistics from person balances and person survey weights.

Native-First: NumPy reductions retain the lane's distinct balance/rank measures.
"""
import numpy as np


def require(ok, message):
    if not ok:
        raise ValueError("[BLOCKED] oct16 statistics: " + message)


def top_share(balance, dollars, rank_weight, fraction):
    order = np.argsort(-balance, kind="stable")
    ordered_weight = rank_weight[order]
    target = fraction * ordered_weight.sum()
    previous = np.r_[0., np.cumsum(ordered_weight)[:-1]]
    inclusion = np.clip((target-previous)/ordered_weight, 0., 1.)
    return float(inclusion @ dollars[order])


def summarize(person, weight, household, labels):
    """Signs use unweighted household dollars; aggregates use person dollars."""
    ids, code = np.unique(household, return_inverse=True)
    members = np.bincount(code).astype(float)
    rank = np.bincount(code, weights=weight)/members
    balance = np.bincount(code, weights=person)
    dollars = np.bincount(code, weights=person*weight)
    member_weight = np.bincount(code, weights=weight)
    require(np.all(weight > 0) and np.isfinite(person).all(), "invalid balances or weights")
    require(abs(dollars.sum()-person@weight) < max(1e-3, abs(person@weight)*1e-12), "person/household weighted closure")
    npos = balance[code] < 0
    shares = []
    for breakdown, values in labels.items():
        for cell in sorted(set(values)):
            selected = values == cell
            hs = np.unique(code[selected])
            shares.append(dict(breakdown=breakdown, cell=cell, records=int(selected.sum()),
                households=len(hs), members_m=float(weight[selected].sum()/1e6),
                share_members_net_positive=float(weight[selected]@npos[selected]/weight[selected].sum()),
                share_households_net_positive=float(rank[hs]@(balance[hs]<0)/rank[hs].sum()),
                net_cost_per_member_usd=float(person[selected]@weight[selected]/weight[selected].sum()),
                cell_net_cost_bn=float(person[selected]@weight[selected]/1e9)))
    concentration = []
    for fraction, name in ((.1,"10"),(.2,"20")):
        top = top_share(balance,dollars,rank,fraction)
        gross = np.maximum(dollars,0)
        concentration += [dict(statistic=f"top{name}_share_of_total",value=top/dollars.sum()),
            dict(statistic=f"top{name}_gross_positive_share",value=top_share(balance,gross,rank,fraction)/gross.sum()),
            dict(statistic=f"top{name}_members_share",value=top_share(balance,member_weight,rank,fraction)/member_weight.sum())]
    concentration += [dict(statistic="total_bn",value=float(dollars.sum()/1e9)),
        dict(statistic="net_cost_households_bn",value=float(dollars[balance>0].sum()/1e9)),
        dict(statistic="net_contributor_households_bn",value=float(dollars[balance<0].sum()/1e9)),
        dict(statistic="share_households_net_positive",value=float(rank@(balance<0)/rank.sum()))]
    quantiles = []
    for unit, values, weights in (("per_member",(balance/members)[code],weight),("household",balance,rank)):
        order=np.argsort(values,kind="stable")
        cdf=np.cumsum(weights[order])/weights.sum()
        for q in (.1,.25,.5,.75,.9):
            j=min(np.searchsorted(cdf,q),len(order)-1)
            quantiles.append(dict(unit=unit,quantile=q,net_cost_usd=float(values[order[j]])))
    return dict(shares=shares,concentration=concentration,quantiles=quantiles,
        household_ids=ids,balance=balance,weighted_dollars=dollars,weight=rank,member_weight=member_weight,
        net_positive=npos,code=code,members=members)
