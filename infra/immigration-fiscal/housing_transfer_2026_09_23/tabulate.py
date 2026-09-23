"""ACS 2024 one-year PUMS: tenure, rent and home value of Mexican-origin and all other households.

Reads only the needed columns of the zipped national PUMS files in chunks.

Group person (P1): Hispanic origin Mexican (HISP=02) or born in Mexico (POBP=303). The CPS
account's union uses own or parent Mexican birthplace plus Mexican identification with US-born
parents; ACS has no parental birthplace, so P1 is the closest person rule available here.
Household rules:
  householder  the reference person is a group person (primary)
  any_member   at least one member is a group person (alternative the brief asks for)
  person_share rent and value apportioned by the share of members who are group persons
Dollars are 2024 dollars (ADJHSG = 1.000000 for the 2024 one-year file); rents are annualised
(monthly x 12). Standard errors use the 80 successive-difference replicate weights.

Outputs (derived/):
  pums_tabulation.csv   rule x group x tenure: households, persons, gross and contract rent, value
  pums_persons.csv      national person counts under each person rule
  pums_puma_cells.csv   PUMA x householder-rule group x tenure totals, input to arms.py
  pums_ownership_proxies.csv  capital-income, Hispanic-householder and small-landlord proxies
  pums_checks.json      person/household linkage and ADJHSG checks
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/housing_transfer_2026_09_23/tabulate.py
"""
from __future__ import annotations

import io
import json
import pathlib
import zipfile

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PUMS = ROOT / "sources/immigration-fiscal/data/external/acs_pums_2024_1yr"
DERIVED = HERE / "derived"
REPS = [f"WGTP{i}" for i in range(1, 81)]
PREPS = [f"PWGTP{i}" for i in range(1, 81)]
CHUNK = 150_000
MEXICO = 303


def read_zip(name, members, usecols, dtype):
    with zipfile.ZipFile(PUMS / name) as z:
        for member in members:
            with z.open(member) as fh:
                yield from pd.read_csv(io.TextIOWrapper(fh), usecols=usecols, dtype=dtype,
                                       chunksize=CHUNK)


def person_pass():
    cols = (["SERIALNO", "STATE", "PUMA", "PWGTP", "RELSHIPP", "HISP", "POBP", "NATIVITY",
             "INTP", "ADJINC"] + PREPS)
    dtype = {"SERIALNO": str, "STATE": str, "PUMA": str}
    households, pumas, national, capital = [], [], [], []
    for chunk in read_zip("csv_pus.zip", ["psam_pusa.csv", "psam_pusb.csv"], cols, dtype):
        hisp_mx = chunk["HISP"].eq(2)
        mx_born = chunk["POBP"].eq(MEXICO)
        grp = hisp_mx | mx_born
        head = chunk["RELSHIPP"].eq(20)
        # Interest, dividends and net rental income: the only ACS capital-income item. A
        # broad ownership proxy for the group's share of property income, not rental income.
        intp = chunk["INTP"].fillna(0).to_numpy(float) * chunk["ADJINC"].to_numpy(float) / 1e6
        w = chunk["PWGTP"].to_numpy(float)
        capital.append(pd.Series({
            "intp_all": (w * intp).sum(), "intp_grp_p1": (w * intp)[grp.to_numpy()].sum(),
            "intp_hispanic": (w * intp)[chunk["HISP"].ge(2).to_numpy()].sum(),
            "intp_positive_all": (w * (intp > 0)).sum(),
            "intp_positive_grp_p1": (w * (intp > 0))[grp.to_numpy()].sum()}))
        frame = pd.DataFrame({
            "SERIALNO": chunk["SERIALNO"],
            "n": 1, "n_grp": grp.astype(int), "n_hisp_mx": hisp_mx.astype(int),
            "head_grp": (head & grp).astype(int), "head_hisp_mx": (head & hisp_mx).astype(int),
            "head_native": (head & chunk["NATIVITY"].eq(1)).astype(int),
            "head_mx_born": (head & mx_born).astype(int)})
        households.append(frame.groupby("SERIALNO").sum())
        weights = chunk[["PWGTP"] + PREPS].to_numpy(float)
        flags = {"all": np.ones(len(chunk), bool), "grp_p1": grp.to_numpy(),
                 "hisp_mx": hisp_mx.to_numpy(), "mx_born": mx_born.to_numpy(),
                 "gq": chunk["RELSHIPP"].isin([37, 38]).to_numpy(),
                 "grp_gq": (grp & chunk["RELSHIPP"].isin([37, 38])).to_numpy()}
        national.append(pd.DataFrame({k: weights[v].sum(axis=0) for k, v in flags.items()}))
        puma = pd.DataFrame({"STATE": chunk["STATE"], "PUMA": chunk["PUMA"],
                             "persons": chunk["PWGTP"], "grp_persons": chunk["PWGTP"] * grp})
        pumas.append(puma.groupby(["STATE", "PUMA"]).sum())
    hh = pd.concat(households).groupby(level=0).sum()
    puma = pd.concat(pumas).groupby(level=[0, 1]).sum().reset_index()
    nat = sum(national)
    return hh, puma, nat, sum(capital)


def replicate_se(full, reps):
    return np.sqrt(4 / 80 * ((reps - full[:, None]) ** 2).sum(axis=1))


def household_pass(hh):
    cols = (["SERIALNO", "STATE", "PUMA", "WGTP", "NP", "TYPEHUGQ", "TEN", "GRNTP", "RNTP",
             "VALP", "ADJHSG", "HHLDRHISP", "BLD"] + REPS)
    dtype = {"SERIALNO": str, "STATE": str, "PUMA": str, "HHLDRHISP": str}
    cells, pumas, extras = [], [], []
    checks = {"occupied_rows": 0, "unmatched_rows": 0, "head_mismatch_rows": 0,
              "adjhsg_values": set()}
    for chunk in read_zip("csv_hus.zip", ["psam_husa.csv", "psam_husb.csv"], cols, dtype):
        chunk = chunk[chunk["TYPEHUGQ"].eq(1) & chunk["NP"].gt(0)].copy()
        checks["occupied_rows"] += len(chunk)
        checks["adjhsg_values"].update(chunk["ADJHSG"].unique().tolist())
        chunk = chunk.join(hh, on="SERIALNO")
        checks["unmatched_rows"] += int(chunk["n"].isna().sum())
        if chunk["n"].isna().any():
            raise ValueError("household without person records")
        # The household file's own householder recode must agree with the person file.
        checks["head_mismatch_rows"] += int((chunk["HHLDRHISP"].astype(int).eq(2)
                                             != chunk["head_hisp_mx"].eq(1)).sum())
        adj = chunk["ADJHSG"].to_numpy(float) / 1e6
        renter = chunk["TEN"].eq(3).to_numpy()
        tenure = np.select([chunk["TEN"].isin([1, 2]), chunk["TEN"].eq(3), chunk["TEN"].eq(4)],
                           ["owner", "renter", "no_cash_rent"], "unknown")
        values = {
            "households": np.ones(len(chunk)),
            "persons": chunk["NP"].to_numpy(float),
            "gross_rent_annual": np.where(renter, chunk["GRNTP"].fillna(0).to_numpy(float), 0) * 12 * adj,
            "contract_rent_annual": np.where(renter, chunk["RNTP"].fillna(0).to_numpy(float), 0) * 12 * adj,
            "owner_value": np.where(chunk["TEN"].isin([1, 2]).to_numpy(),
                                    chunk["VALP"].fillna(0).to_numpy(float), 0) * adj,
            "paying_cash_rent": (renter & chunk["GRNTP"].fillna(0).gt(0).to_numpy()).astype(float)}
        share = (chunk["n_grp"] / chunk["n"]).to_numpy(float)
        rules = {"householder": chunk["head_grp"].eq(1).to_numpy(),
                 "any_member": chunk["n_grp"].gt(0).to_numpy(),
                 "householder_hisp02": chunk["HHLDRHISP"].astype(int).eq(2).to_numpy()}
        weights = chunk[["WGTP"] + REPS].to_numpy(float)
        # Ownership proxies: Hispanic householders (to scale the SCF's Hispanic category to
        # the Mexican-origin group) and owner-occupants of 2-4 unit buildings, who own the
        # other units they live beside.
        wgt = chunk["WGTP"].to_numpy(float)
        hisp_head = chunk["HHLDRHISP"].astype(int).ge(2).to_numpy()
        small_owner = chunk["TEN"].isin([1, 2]).to_numpy() & chunk["BLD"].isin([4, 5]).to_numpy()
        grp_head = rules["householder"]
        extras.append(pd.Series({
            "households_all": wgt.sum(), "households_hispanic_head": wgt[hisp_head].sum(),
            "households_grp_head": wgt[grp_head].sum(),
            "households_hisp02_head": wgt[rules["householder_hisp02"]].sum(),
            "owners_2to4_all": wgt[small_owner].sum(),
            "owners_2to4_grp_head": wgt[small_owner & grp_head].sum(),
            "owners_2to4_hispanic_head": wgt[small_owner & hisp_head].sum(),
            "owners_all": wgt[chunk["TEN"].isin([1, 2]).to_numpy()].sum(),
            "owners_grp_head": wgt[chunk["TEN"].isin([1, 2]).to_numpy() & grp_head].sum(),
            "renters_in_2to4_all": wgt[renter & chunk["BLD"].isin([4, 5]).to_numpy()].sum(),
            "renters_in_2to4_grp_head": wgt[renter & chunk["BLD"].isin([4, 5]).to_numpy() & grp_head].sum()}))
        for rule, flag in rules.items():
            for group, mask in (("group", flag), ("other", ~flag)):
                for ten in ("owner", "renter", "no_cash_rent"):
                    m = mask & (tenure == ten)
                    for var, x in values.items():
                        tot = (weights[m] * x[m, None]).sum(axis=0)
                        cells.append((rule, group, ten, var, tot))
        # Person-share apportionment: each household split by the share of group members.
        for group, part in (("group", share), ("other", 1 - share)):
            for ten in ("owner", "renter", "no_cash_rent"):
                m = tenure == ten
                for var, x in values.items():
                    tot = (weights[m] * (x[m] * part[m])[:, None]).sum(axis=0)
                    cells.append(("person_share", group, ten, var, tot))
        # Native-born householder among other households, householder rule, for per-household figures.
        native_other = ~rules["householder"] & chunk["head_native"].eq(1).to_numpy()
        for ten in ("owner", "renter"):
            m = native_other & (tenure == ten)
            for var, x in values.items():
                tot = (weights[m] * x[m, None]).sum(axis=0)
                cells.append(("householder", "other_native_head", ten, var, tot))
        pumas.append(pd.DataFrame({
            "STATE": chunk["STATE"], "PUMA": chunk["PUMA"],
            "group": np.where(rules["householder"], "group", "other"), "tenure": tenure,
            **{var: chunk["WGTP"].to_numpy(float) * x for var, x in values.items()}})
            .groupby(["STATE", "PUMA", "group", "tenure"]).sum())
    table = {}
    for rule, group, ten, var, tot in cells:
        key = (rule, group, ten, var)
        table[key] = table.get(key, 0) + tot
    rows = []
    for (rule, group, ten, var), tot in table.items():
        se = replicate_se(tot[:1], tot[None, 1:])[0]
        rows.append({"rule": rule, "group": group, "tenure": ten, "variable": var,
                     "estimate": tot[0], "se": se})
    puma = pd.concat(pumas).groupby(level=[0, 1, 2, 3]).sum().reset_index()
    checks["adjhsg_values"] = sorted(checks["adjhsg_values"])
    return pd.DataFrame(rows), puma, checks, sum(extras)


def main():
    DERIVED.mkdir(exist_ok=True)
    hh, puma_persons, nat, capital = person_pass()
    persons = pd.DataFrame({"estimate": nat.iloc[0], "se": replicate_se(
        nat.iloc[0].to_numpy(), nat.iloc[1:].to_numpy().T)}).rename_axis("person_rule").reset_index()
    persons.to_csv(DERIVED / "pums_persons.csv", index=False)
    table, puma_hh, checks, extras = household_pass(hh)
    table.sort_values(["rule", "group", "tenure", "variable"]).to_csv(
        DERIVED / "pums_tabulation.csv", index=False)
    pd.concat([capital, extras]).rename("estimate").rename_axis("item").reset_index().to_csv(
        DERIVED / "pums_ownership_proxies.csv", index=False)
    wide = puma_hh.pivot_table(index=["STATE", "PUMA"], columns=["group", "tenure"],
                               values=["households", "gross_rent_annual", "contract_rent_annual",
                                       "owner_value", "persons"], aggfunc="sum", fill_value=0)
    wide.columns = [f"{g}_{t}_{v}" for v, g, t in wide.columns]
    wide = wide.reset_index().merge(puma_persons, on=["STATE", "PUMA"], how="outer",
                                    validate="one_to_one")
    wide.to_csv(DERIVED / "pums_puma_cells.csv", index=False)
    (DERIVED / "pums_checks.json").write_text(json.dumps(checks, indent=2, default=str))
    print(persons.to_string(index=False))
    print(json.dumps(checks, default=str))


if __name__ == "__main__":
    main()
