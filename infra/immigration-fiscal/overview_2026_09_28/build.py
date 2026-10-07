"""Build the evidence overview page: ladder entries sorted into groups, the account's ledgers, one time map.

    uv run --no-project python3 infra/immigration-fiscal/overview_2026_09_28/build.py

Reads the confidence ladder, main case v6 (`main_case_2026_10_07/derived/`: `summary.json`,
`main_case_bands.csv`, `lineage_addition.json`), the figures page's staircase (the steps up to the
September 24 case, read at its commit in `PINS`) and, through `quantity_registry.csv`, the lanes the
tables quote. The ledger runs the staircase, the September 26 and 27 changes and v4's items from
`summary.json`'s `change_at_fixed_specifications`; it splits v4's state-price item with the September 29 lane's
state-price lines. The added descendants come from `lineage_addition.json`, by count part, on v5 and
then with v6's items; v6's items on the identified members come from `summary.json`'s item parts,
with retiree health as the rest of the union-only case's change. Refuses to write if a ladder entry
is unassigned or assigned twice, or if the ledger misses a case's subtotal (September 23, 24, 26,
27, 29, October 5, and the main estimate). Writes `derived/overview.html`.

The ledger sections sit in `template.html` between `<!-- BUILD_BLOCK:START -->` and
`<!-- BUILD_BLOCK:END -->`. When groups.py has a "build" part, the build moves them to just after
that part's heading and lists their `<h3 id>` headings first in its contents. Without the part
they stay where the template has them.

Numbers that the text quotes from a file come from `quantity_registry.csv` through placeholders,
`{{q:<id>|<view>}}`, which `quantities.py` renders. The build lints every sentence that quotes a
record, runs the binding tests in `quantity_bindings.csv`, tests the claims the prose makes in words
against their records (`PROSE_CLAIMS`), and refuses to write on any failure.
`--groups PATH`, `--template PATH` and `--bindings PATH` read other copies of groups.py,
template.html and quantity_bindings.csv, `--out PATH` writes elsewhere, and `--round-each` rounds
every table number on its own (the positive controls use these).
"""

import argparse
import csv
import html
import importlib
import importlib.util
import json
import re
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import quantities as Q  # noqa: E402

evidence = None  # imported in main(), after --groups has picked the groups module it reads

LADDER = ROOT / "research/immigration-confidence-ladder.md"
MAIN = ROOT / "infra/immigration-fiscal/main_case_2026_10_07/derived"
STAIRS = ROOT / "infra/immigration-fiscal/figures_2026_09_22/src/generated/figures.json"
# Files read at a commit, not from the working tree, as account.cjs's PINS does: the figures page moves to newer cases,
# and the ledger takes from it only the steps up to the September 24 case.
PINS = {STAIRS: "57b48186"}  # figures.json's last commit on the September 24 case
OV = "infra/immigration-fiscal/overview_2026_09_28"
# how to read the dotted underline that quantities.fill puts on an approximate number; the page carries it only
# when some number does
APPROX_NOTE = (' A number with a dotted underline is <span class="approx" title="Approximate. Each such number '
               'carries its reason here.">approximate</span>. Its tooltip gives the reason.')


def q(rid):
    """A registry record's value, unrounded: a list for a pair of ends, else a number."""
    v = Q.record_value(rid)
    return list(v) if isinstance(v, tuple) else v


def load_headcount():
    """The lineage the account prices, its identified members (row 4 of the data audit) and the added
    descendants, and the CPS's raw union count. Per-member figures divide engine totals by the lineage."""
    lineage, identified, added, raw = (q(k) * 1e6 for k in ("headcount.lineage", "headcount.identified",
                                                            "headcount.added", "headcount.raw"))
    if q("headcount.priced") * 1e6 != lineage:
        fail(f"the priced count {q('headcount.priced') * 1e6:,.0f} is not the lineage {lineage:,.0f}")
    if not (42e6 < lineage < 44e6 and 39e6 < identified < 41e6 and identified <= raw
            and abs(identified + added - lineage) < 1):
        fail(f"headcount out of range: lineage {lineage:,.0f}, identified {identified:,.0f} + added {added:,.0f}, "
             f"raw {raw:,.0f}")
    return lineage, identified, added, raw



def fail(msg):
    sys.exit(f"[BLOCKED] {msg}")


def pinned(path):
    """A file's text at its commit in `PINS`, through `git show`; refuses when git cannot read it there."""
    rel = path.relative_to(ROOT).as_posix()
    try:
        r = subprocess.run(["git", "-C", str(ROOT), "show", f"{PINS[path]}:{rel}"], capture_output=True,
                           encoding="utf-8")
    except OSError as e:
        fail(f"git show {PINS[path]}:{rel}: {e}")
    if r.returncode:
        fail(f"git show {PINS[path]}:{rel} exited {r.returncode}: {r.stderr.strip()}")
    return r.stdout


# ---------------------------------------------------------------- ladder parsing

def strip_md(s):
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = s.replace("**", "").replace("`", "")
    return re.sub(r"\s+", " ", s).strip()


def leading_brackets(text):
    """Split off leading [dated revision] blocks, matching nested brackets."""
    notes, i = [], 0
    while i < len(text) and text[i] == "[":
        depth, j = 0, i
        while j < len(text):
            depth += {"[": 1, "]": -1}.get(text[j], 0)
            if depth == 0:
                break
            j += 1
        notes.append(text[i + 1:j])
        i = j + 1
        while i < len(text) and text[i] == " ":
            i += 1
    return notes, text[i:]


def first_sentence(s, cap=240):
    m = re.search(r"(?<=[a-z0-9%)\]’'\"”])[.;] (?=[A-Z\"“])", s)
    s = s[: m.start() + 1] if m else s
    return s if len(s) <= cap else s[: cap - 1].rsplit(" ", 1)[0] + "…"


def parse_ladder():
    lines = LADDER.read_text().splitlines()
    old_start = next(i for i, l in enumerate(lines) if l.startswith("# Immigration confidence ladder") and "current" not in l)
    old_end = next(i for i, l in enumerate(lines) if l.startswith("## Two weakest assumptions"))
    first_strong = next(i for i in range(old_start, old_end) if lines[i].startswith("## Strong"))
    entries = {}
    for line in lines[:old_start]:
        m = re.match(r"^(\d+)\. (.*)", line)
        if not m:
            continue
        n, body = int(m.group(1)), m.group(2)
        notes, rest = leading_brackets(body)
        b = re.search(r"\*\*(.+?)\*\*", rest)
        claim = strip_md(b.group(1) if b else rest)
        head = (" ".join(notes) + " " + claim[:400]).lower()
        status = "superseded" if re.search(r"supersed|withdrawn", head) else ("revised" if notes else "")
        entries[str(n)] = dict(key=str(n), claim=first_sentence(claim), status=status, body=body,
                               rating=evidence.rating(rest))
    for line in lines[first_strong:old_end]:
        m = re.match(r"^(\d+)\. `([^`]+)`(.*)", line)
        if not m:
            continue
        tail = m.group(3).upper()
        status = "superseded" if re.search(r"INVALIDATED|SUPERSEDED", tail) else ("revised" if "QUALIFIED" in tail or "CORRECTED" in tail else "old")
        entries[f"o{m.group(1)}"] = dict(key=f"o{m.group(1)}", claim=strip_md(m.group(2)), status=status,
                                         body=line, rating="")
    return entries


# ---------------------------------------------------------------- numbers and gates

def load_numbers():
    s = json.loads((MAIN / "summary.json").read_text())
    bands = {r["variant"] if r["profile"] == "long_run_non_school_full" else r["profile"] + ":" + r["variant"]:
             (float(r["cost_low_bn"]), float(r["cost_high_bn"]))
             for r in csv.DictReader((MAIN / "main_case_bands.csv").open())}
    stairs = json.loads(pinned(STAIRS))["staircase"]
    sept24 = s["adopted_2026_09_24"]
    last = next(r for r in stairs if r["id"] == "benefits")
    if any(abs(a - b) > 1e-3 for a, b in zip(last["total"], sept24)):
        fail(f"staircase ends at {last['total']}, summary.json September 24 case is {sept24}")
    for variant, key in [("adopted", "main_case"), ("oct05_case", "adopted_2026_10_05"),
                         ("sept29_case", "adopted_2026_09_29"), ("sept27_case", "adopted_2026_09_27"),
                         ("schools_case", "schools_case")]:
        if any(abs(a - b) > 1e-3 for a, b in zip(bands[variant], s[key])):
            fail(f"main_case_bands.csv {variant} {bands[variant]} and summary.json {key} {s[key]} disagree")
    return s, bands, stairs


# Reader-facing labels for the figures page's staircase rows: concepts, not the history of the analysis.
RELABEL = {
    "schools": ("Schools, first-year budget response", "63–66% of cost per pupil (CBO)"),
    "gg": ("General administration", "{{q:gg.growth_elasticity|range}}% per 1% more residents"),
    "taxes": ("Taxes checked against records", "off-books work, survey fill-ins, top incomes"),
    "benefits": ("Benefits and services checked against records", "credits, medical care, schools, care"),
}


def waterfall_rows(s, stairs):
    c = s["change_at_fixed_specifications"]
    # The staircase's `step` pairs are sorted by size, not by end, so steps come from the running totals.
    rows, prev = [], [0.0, 0.0]
    for r in stairs:
        if r["beyond"]:
            continue
        label, note = RELABEL.get(r["id"], (r["label"], r["note"] or ""))
        rows.append(dict(label=label, note=note, step=[r["total"][0] - prev[0], r["total"][1] - prev[1]]))
        prev = r["total"]
        if r["id"] == "gg":
            rows.append(dict(label="September 23 case", total=True))
        if r["id"] == "benefits":
            rows.append(dict(label="September 24 case", total=True))
    # The September 26 step holds two changes: consumption taxes keyed on spending (run L) and service responses
    # read as a finite removal, which belong to schools (run F) and to general government (the rest, run I).
    d26 = [a - b for a, b in zip(s["adopted_2026_09_26"], s["adopted_2026_09_24"])]
    key26, sch26 = q("consumption_key.effect"), q("finite_removal.schools")
    gg26 = [d - k - f for d, k, f in zip(d26, key26, sch26)]
    if any(abs(a - b) > 1e-3 for a, b in zip(gg26, q("finite_removal.general_government_and_row8"))):
        fail(f"the September 26 step less runs L and F is {gg26}, not run I (general government)")
    sch = [a - b for a, b in zip(s["schools_case"], s["adopted_2026_09_26"])]
    # Each later case's changes at fixed specifications, nested: v6's items hold v5's lineage, which holds v4's items,
    # which hold September 27's changes.
    c05 = c["oct05_case"]
    c29 = c05["sept29_case"]
    c27 = c29["sept27_case"]
    add = lambda *vs: [sum(v[i] for v in vs) for i in (0, 1)]  # noqa: E731
    sub = lambda a, b: [a[i] - b[i] for i in (0, 1)]  # noqa: E731
    far = lambda a, b, tol: any(abs(x - y) > tol for x, y in zip(a, b))  # noqa: E731
    # The added descendants by count part, on v5 and with v6's items (lineage_addition.json, the case lane's split of
    # v6 into the union-only case and the lineage's addition). Its v5 parts are v5's lineage block.
    la = json.loads((MAIN / "lineage_addition.json").read_text())["set"]
    parts, resp, resp5 = la["parts"], la["union_response_bn"], la["union_response_on_v5_bn"]
    if far(add(parts["g3_rate"]["on_v5_cost_bn"], parts["later"]["on_v5_cost_bn"], resp5), c05["total"], 1e-9) \
            or far(resp5, c05["union_response_move"], 1e-9) or far(la["case_bn"], s["main_case"], 1e-9) \
            or far(la["union_only"]["on_v5_cost_bn"], s["adopted_2026_09_29"], 1e-6) \
            or far(add(la["union_only"]["cost_bn"], la["lineage_addition_bn"]), s["main_case"], 1e-9):
        fail("lineage_addition.json does not split v5's lineage block and v6 as summary.json has them")
    # v6's items on the identified members: the pension item's union parts, every part of the fee item, and retiree
    # health as the rest of the union-only case's change. summary.json splits retiree health at the case's responses,
    # the union-only case at the union's own; the two differ by under $0.001bn.
    items = c["items"]
    fees = items["user_fees"]["parts"]
    if set(fees) != set(FEE_PARTS):
        fail(f"the fee item's parts are {sorted(fees)}; FEE_PARTS labels {sorted(FEE_PARTS)}")
    union_change = sub(la["union_only"]["cost_bn"], la["union_only"]["on_v5_cost_bn"])
    retiree = sub(sub(union_change, items["pension_tr2026"]["union"]), items["user_fees"]["total"])
    if far(retiree, add(items["retiree_health"]["union"], items["retiree_health"]["capital_return"]), 1e-3):
        fail(f"retiree health on the union-only case is {retiree}, summary.json's union part "
             f"{add(items['retiree_health']['union'], items['retiree_health']['capital_return'])}")
    lineage_items = add(*(parts[k]["items_change_bn"] for k in ("g3_rate", "later")), sub(resp, resp5))
    item_lineage = add(items["added_age_mix"]["total"], items["pension_tr2026"]["lineage"],
                       items["retiree_health"]["lineage"], *(v for k, v in c["interactions"].items()
                                                              if "added_age_mix" in k))
    if far(lineage_items, sub(la["lineage_addition_bn"], la["lineage_addition_on_v5_bn"]), 1e-9) \
            or far(lineage_items, item_lineage, 1e-3):
        fail(f"v6's items on the added descendants are {lineage_items}, summary.json's lineage parts {item_lineage}")
    # v4's state-price item prices three services at the states where the group lives and re-rates its sales and
    # vehicle taxes; the service lines move with this item alone, so the rest of the item is the taxes.
    services = [q(f"state_prices.{k}") for k in ("public_order", "health", "recreation")]
    state_tax = [a - b for a, b in zip(c29["item_state"], add(*services))]
    if any(abs(a + b) > 1e-9 for a, b in zip(state_tax, q("state_prices.taxes"))):
        fail(f"the state item less its service lines is {state_tax}, not the registry's state_prices.taxes")
    rows += [
        dict(label="Consumption taxes on spending", note="net of saving and remittances", step=key26),
        dict(label="Schools, finite removal", note="", step=sch26),
        dict(label="General administration, finite removal", note="", step=gg26),
        dict(label="Schools, long run: full cost per pupil", note="spending rises ~1% per 1% more pupils", step=sch),
        dict(label="September 26 schools case", total=True),
        dict(label="Roads, parks: long-run response", step=c27["long_run_responses"]),
        dict(label="Rental assistance at 1", step=c27["rental_assistance"]),
        dict(label="Return on public capital", step=add(c27["capital_core"], c27["capital_block"])),
        dict(label="Government enterprises",
             step=add(c27["enterprise_rekey"], c27["enterprise_surplus_receipt"], c27["capital_enterprise"])),
        dict(label="September 27 case", total=True),
        dict(label="Pension accrual", step=c29["item_pension"]),
        dict(label="Property taxes, long run", step=c29["item_5"]),
        dict(label="Income tax keyed to IRS totals", step=c29["item_3"]),
        dict(label="Payroll tax compliance", step=c29["item_6a"]),
        dict(label="Workers' compensation", step=c29["item_7"]),
        dict(label="Production gain rekeyed", step=c29["item_2"]),
        dict(label="Enterprise and housing receipts", step=c29["item_1"]),
        dict(label="Enterprise housing capital", step=c29["item_4"]),
        dict(label="State prices: public order and safety", step=services[0]),
        dict(label="State prices: health services", step=services[1]),
        dict(label="State prices: recreation and culture", step=services[2]),
        dict(label="State prices: sales and vehicle taxes", step=state_tax),
        dict(label="Roads by miles driven", step=c29["item_roads"]),
        dict(label="September 29 case", total=True),
        dict(label="Added descendants lost at the third generation's rate", step=parts["g3_rate"]["on_v5_cost_bn"]),
        dict(label="Added descendants lost a generation later", step=parts["later"]["on_v5_cost_bn"]),
        dict(label="Service responses at the larger group size", step=resp5),
        dict(label="October 5 case", total=True),
        dict(label="Pension accrual on the 2026 Trustees, each fund apart", step=items["pension_tr2026"]["union"]),
        dict(label="Retiree health on accrual", step=retiree),
        *(dict(label=FEE_PARTS[k], step=v) for k, v in fees.items()),
        dict(label="Added descendants lost at the third generation's rate, v6's items",
             step=parts["g3_rate"]["items_change_bn"]),
        dict(label="Added descendants lost a generation later, v6's items", step=parts["later"]["items_change_bn"]),
        dict(label="Service responses at the larger group size, v6's items", step=sub(resp, resp5)),
        dict(label="Main estimate", total=True, main=True),
    ]
    tot = [0.0, 0.0]
    for r in rows:
        if r.get("total"):
            r["value"] = list(tot)
        else:
            r["prev"] = list(tot)
            tot = [tot[0] + r["step"][0], tot[1] + r["step"][1]]
            r["value"] = list(tot)
    if any(abs(a - b) > 1e-3 for a, b in zip(tot, s["main_case"])):
        fail(f"waterfall sums to {tot}, main case is {s['main_case']}")
    # every case's subtotal; the September 29 case also against its own lane
    for label, want in [("September 23 case", s["adopted_2026_09_23"]), ("September 24 case", s["adopted_2026_09_24"]),
                        ("September 26 schools case", s["schools_case"]),
                        ("September 27 case", s["adopted_2026_09_27"]), ("September 29 case", s["adopted_2026_09_29"]),
                        ("September 29 case", q("case.sept29")), ("October 5 case", s["adopted_2026_10_05"])]:
        v = next(r for r in rows if r["label"] == label)["value"]
        if any(abs(a - b) > 1e-3 for a, b in zip(v, want)):
            fail(f"{label} subtotal {v} != {want}")
    v6_items = {**{k: v["total"] for k, v in items.items()}, **c["interactions"]}
    for what, parts_, total in [("September 27's changes", c27, c27["total"]), ("v4's items", c29, c29["total"]),
                                ("the lineage", c05, c05["total"]), ("v6's items", v6_items, c["total"]),
                                ("the fee item's parts", fees, items["user_fees"]["total"]),
                                ("the pension item's parts", items["pension_tr2026"], items["pension_tr2026"]["total"]),
                                ("the retiree-health item's parts", items["retiree_health"],
                                 items["retiree_health"]["total"])]:
        got = add(*(v for k, v in parts_.items() if k in ITEMS[what]))
        if any(abs(a - b) > 1e-3 for a, b in zip(got, total)):
            fail(f"{what} add to {got}, summary.json's total is {total}")
    rows = [r for r in rows if not r.get("total") or r.get("main")]
    # Other ways to count, each from the main estimate: pensions counted when paid, budgets at their first-year
    # responses, the descendants counted by ancestry share. Beside them the social pairing, whose low end prices
    # offending at the Hispanic average, so its fiscal case moves first and the social step is the social items alone.
    main, fisc = list(tot), q("pairing.fiscal_footing")
    if abs(fisc[1] - s["main_case"][1]) > 1e-6:  # the totals file keeps six decimals
        fail(f"the pairing's high-end fiscal case {fisc[1]} is not the main case's {s['main_case'][1]}")
    if any(abs(p - f - x) > 1e-9 for p, f, x in zip(q("pairing.total"), fisc, q("social.items"))):
        fail("the pairing less its fiscal case is not social.items")
    if any(abs(a - b) > 1e-6 for a, b in zip(q("case.cash_set"), s["cash_set"]["band_bn"])):
        fail("the registry's cash set is not summary.json's")
    rows += [
        dict(label="Pensions counted when paid", alt=True, block=0, prev=main, value=q("case.cash_set")),
        dict(label="Budgets respond within the first year", alt=True, block=1, prev=main, value=q("case.first_year")),
        dict(label="Descendants counted by share of Mexican ancestry", alt=True, block=2, prev=main,
             value=q("case.ancestry_share")),
        dict(label="Offending at the Hispanic average, low end", beside=True, block=3, prev=main, value=fisc),
        dict(label="Costs outside public budgets", beside=True, block=3, prev=fisc, value=q("pairing.total")),
    ]
    return rows


# The parts of each nested change in summary.json's change_at_fixed_specifications that its total adds. The
# September 27 block's other keys are memo amounts outside the sum (its note says so).
ITEMS = {
    "September 27's changes": ("long_run_responses", "rental_assistance", "capital_core", "capital_block",
                               "enterprise_rekey", "enterprise_surplus_receipt", "capital_enterprise"),
    "v4's items": ("item_1", "item_2", "item_3", "item_4", "item_5", "item_6a", "item_7", "item_pension",
                   "item_state", "item_roads"),
    "the lineage": ("union_response_move", "g3plus_members", "whites"),
    "v6's items": ("pension_tr2026", "retiree_health", "added_age_mix", "user_fees", "pension_tr2026_x_retiree_health",
                   "pension_tr2026_x_added_age_mix", "pension_tr2026_x_user_fees", "retiree_health_x_added_age_mix",
                   "retiree_health_x_user_fees", "added_age_mix_x_user_fees", "remainder"),
    "the fee item's parts": ("union_fee_tuition", "union_key_higher_ed", "union_k12_weight_school",
                             "union_k12_weight_other", "union_fee_health", "union_key_health", "union_key_pell",
                             "union_capital_k12", "union_capital_college", "union_capital_health_sl",
                             "union_capital_health_fed"),
    "the pension item's parts": ("union", "lineage"),
    "the retiree-health item's parts": ("union", "lineage", "capital_return"),
}

# v6's fee item, part by part (summary.json's user_fees parts): the staircase label of each. The ledger puts each
# with the line it edits.
FEE_PARTS = {
    "union_fee_tuition": "College tuition by who pays it",
    "union_key_higher_ed": "Public colleges keyed by use",
    "union_k12_weight_school": "BEA's K-12 weight: schools",
    "union_k12_weight_other": "BEA's K-12 weight: other education",
    "union_fee_health": "Hospital charges by who pays them",
    "union_key_health": "Public hospitals keyed by use",
    "union_key_pell": "Pell grants keyed by use",
    "union_capital_k12": "K-12 capital at its own key",
    "union_capital_college": "College capital keyed by use",
    "union_capital_health_sl": "Health capital, state and local",
    "union_capital_health_fed": "Health capital, federal",
}


# Ledger categories: (category, [(step label on the staircase, reader label, note)]). Items inside a category
# are ranked by size at render time. Two staircase steps can share one reader label; they are summed, and the
# label keeps the note of its first step (a later step's note is None).
LEDGER = [
    ("The group's own taxes and benefits", [
        ("Taxes paid minus benefits received", "Taxes paid minus benefits received", "survey values"),
        ("Taxes checked against records", "Taxes corrected with records",
         "off-books work, survey fill-ins, top incomes, IRS income totals, payroll taxes"),
        ("Income tax keyed to IRS totals", "Taxes corrected with records", None),
        ("Payroll tax compliance", "Taxes corrected with records", None),
        ("Benefits and services checked against records", "Benefits and services corrected with records",
         "tax credits, medical care, schools, care, workers' compensation, Pell grants"),
        ("Workers' compensation", "Benefits and services corrected with records", None),
        ("Pell grants keyed by use", "Benefits and services corrected with records", None),
        ("BEA's K-12 weight: schools", "Benefits and services corrected with records", None),
        ("BEA's K-12 weight: other education", "Benefits and services corrected with records", None),
        ("Pension accrual", "Pension promises earned",
         "Social Security and Medicare Part A, at the benefits current law can pay from each trust fund"),
        ("Pension accrual on the 2026 Trustees, each fund apart", "Pension promises earned", None),
        ("Gain from their work", "Taxes on the gain from their work", "wages and profits of others"),
        ("Production gain rekeyed", "Taxes on the gain from their work", None),
        ("Property taxes, long run", "Property taxes", "they follow people in the long run"),
        ("Consumption taxes on spending", "Sales and excise taxes", "net of saving and remittances"),
        ("State prices: sales and vehicle taxes", "Sales and vehicle taxes at local rates",
         "the states where the group lives"),
    ]),
    ("Schools and colleges", [
        ("Schools, first-year budget response", "Schools, full cost per pupil",
         "spending rises about 1% per 1% more pupils"),
        ("Schools, finite removal", "Schools, full cost per pupil", None),
        ("Schools, long run: full cost per pupil", "Schools, full cost per pupil", None),
        ("Colleges and other education", "Colleges and other education",
         "public colleges by measured use, tuition by who pays it"),
        ("Public colleges keyed by use", "Colleges and other education", None),
        ("College tuition by who pays it", "Colleges and other education", None),
    ]),
    ("Other public services", [
        ("Police, courts and prisons", "Police, courts and prisons", "charged by use, at state prices"),
        ("State prices: public order and safety", "Police, courts and prisons", None),
        ("General administration", "General administration", "{{q:gg.growth_elasticity|range}}% per 1% more residents"),
        ("General administration, finite removal", "General administration", None),
        ("Welfare administration, housing, community", "Welfare administration, housing, community", ""),
        ("Public health services", "Public health", "at state prices, hospitals by use, fees by who pays them"),
        ("State prices: health services", "Public health", None),
        ("Public hospitals keyed by use", "Public health", None),
        ("Hospital charges by who pays them", "Public health", None),
        ("Roads, parks: long-run response", "Roads and parks",
         "0.73% and 0.95% per 1% more residents, roads by miles driven"),
        ("Roads by miles driven", "Roads and parks", None),
        ("State prices: recreation and culture", "Roads and parks", None),
        ("Rental assistance at 1", "Rental assistance", ""),
        ("Unpaid hospital care", "Unpaid hospital care", "charged by uninsured use"),
        ("Retiree health on accrual", "Retiree health of public workers", "counted when earned, like public pensions"),
    ]),
    ("Public capital and enterprises", [
        ("Return on public capital", "Return on public capital", "2% real at the low end, 3% at the high end"),
        ("K-12 capital at its own key", "Return on public capital", None),
        ("College capital keyed by use", "Return on public capital", None),
        ("Health capital, state and local", "Return on public capital", None),
        ("Health capital, federal", "Return on public capital", None),
        ("Government enterprises", "Government enterprises", "operating loss and capital return"),
        ("Enterprise and housing receipts", "Government enterprises", None),
        ("Enterprise housing capital", "Government enterprises", None),
    ]),
    ("Descendants who no longer report Mexican origin", [
        ("Added descendants lost at the third generation's rate", "Lost at the third generation's rate",
         "{{q:lineage.lost_at_g3_rate|value}} people with their descendants, priced partly like white residents of "
         "the same ages"),
        ("Added descendants lost at the third generation's rate, v6's items", "Lost at the third generation's rate",
         None),
        ("Added descendants lost a generation later", "Lost a generation later",
         "{{q:lineage.lost_later|value}} people, priced like third-generation members of the same ages"),
        ("Added descendants lost a generation later, v6's items", "Lost a generation later", None),
        ("Service responses at the larger group size", "Service responses at the larger group size",
         "for the members who report Mexican origin"),
        ("Service responses at the larger group size, v6's items", "Service responses at the larger group size", None),
    ]),
]


def num(d, signed=True):
    """A printed Decimal with a true minus sign, and a plus when `signed`; zero has no sign."""
    return ("−" if d < 0 else ("+" if d > 0 and signed else "")) + f"{abs(d):f}"


def cells(shown, signed=True):
    """Table cells for printed Decimals, coloured by sign when `signed`."""
    tone = lambda d: "gain" if d < 0 else ("cost" if d > 0 else "")  # noqa: E731
    return "".join(f'<td class="n {tone(d) if signed else ""} ">{num(d, signed)}</td>' for d in shown)


def whole(v):
    return [Q.rounded(x, 0) for x in v]


# Rounding in the ledger and the running sums. The operator's rule: printed lines must add to the printed total.
# A table prints whole billions when every line's own rounding adds up; otherwise it prints one decimal, and where
# a sum still breaks, the lines nearest a rounding boundary are rounded the other way (Q.allocate). `ROUND_EACH`
# rounds every number on its own instead: the positive control for the gate in displayed_sum_errors.
ROUND_EACH = False


def rounding_note(places, moved):
    """The caption under a table: its precision, and how many lines are rounded the other way."""
    unit = "0.1" if places == 1 else "1"
    note = f"Lines show {'one decimal' if places == 1 else 'whole billions'}, and each column adds up as printed."
    if moved:
        note += (f" For that, {moved} line{'s' if moved > 1 else ''} near a rounding boundary "
                 f"{'are' if moved > 1 else 'is'} rounded the other way. "
                 f"{'Each stays' if moved > 1 else 'It stays'} within {unit} of its exact value.")
    return note


def ledger_shown(lines, main, places, each=False):
    """Printed values: (main, category subtotals, lines per category). The main estimate is rounded; the
    subtotals are allocated to it and each category's lines to its subtotal. `each` rounds every number on
    its own."""
    rnd = lambda x: Q.rounded(x, places)  # noqa: E731

    def fit(vals, target):
        if each:
            return [[rnd(x) for x in v] for v in vals]
        same = {k for k, v in enumerate(vals) if rnd(v[0]) == rnd(v[1])}  # printed equal at both ends
        cols = [Q.allocate([v[i] for v in vals], target[i], places, last=same) for i in (0, 1)]
        return [[cols[0][k], cols[1][k]] for k in range(len(vals))]
    tot = [rnd(x) for x in main]
    subs = fit([[sum(m["v"][i] for m in merged.values()) for i in (0, 1)] for _c, merged in lines], tot)
    return tot, subs, [fit([m["v"] for m in merged.values()], sub) for (_c, merged), sub in zip(lines, subs)]


def moved_lines(lines, shown, places):
    """How many printed subtotals and lines differ from their own rounding."""
    _tot, subs, items = shown
    n = 0
    for (_c, merged), sub, its in zip(lines, subs, items):
        true_sub = [sum(m["v"][i] for m in merged.values()) for i in (0, 1)]
        n += sum(1 for i in (0, 1) if sub[i] != Q.rounded(true_sub[i], places))
        n += sum(1 for m, s in zip(merged.values(), its) for i in (0, 1) if s[i] != Q.rounded(m["v"][i], places))
    return n


def ledger_lines(rows):
    """[(category, {reader label: dict(v=[low, high], note)})]: staircase steps summed under their reader labels."""
    steps = {r["label"]: r["step"] for r in rows if "step" in r}
    used, out = set(), []
    for cat, items in LEDGER:
        merged = {}
        for step_label, label, note in items:
            if step_label not in steps:
                fail(f"ledger item {step_label!r} is not a staircase step")
            used.add(step_label)
            m = merged.setdefault(label, dict(v=[0.0, 0.0], note=note))
            m["v"] = [a + b for a, b in zip(m["v"], steps[step_label])]
            if note is not None:
                m["note"] = note
        out.append((cat, merged))
    missing = set(steps) - used
    if missing:
        fail(f"staircase steps missing from the ledger: {sorted(missing)}")
    return out


def ledger_html(rows):
    """Two-level ledger: category subtotals, items ranked by size, columns that sum to the main estimate.
    Returns the table and its caption."""
    lines = ledger_lines(rows)
    total = [sum(sum(m["v"][i] for m in merged.values()) for _c, merged in lines) for i in (0, 1)]
    main = next(r for r in rows if r.get("main"))["value"]
    if any(abs(a - b) > 1e-3 for a, b in zip(total, main)):
        fail(f"ledger sums to {total}, main estimate is {main}")
    places = 0 if moved_lines(lines, ledger_shown(lines, main, 0), 0) == 0 else 1
    shown = ledger_shown(lines, main, places, each=ROUND_EACH)
    tot, subs, items = shown
    body = []
    for (cat, merged), sub, its in zip(lines, subs, items):
        body.append(f'<tbody><tr class="cat" data-sum="subtotal"><th scope="rowgroup">{html.escape(cat)}</th>'
                    f'{cells(sub)}</tr>')
        ranked = sorted(zip(merged.items(), its), key=lambda p: -max(abs(p[0][1]["v"][0]), abs(p[0][1]["v"][1])))
        for (label, m), s in ranked:
            note = f'<span class="note">{html.escape(m["note"])}</span>' if m["note"] else ""
            body.append(f'<tr class="item" data-sum="part"><td>{html.escape(label)}{note}</td>{cells(s)}</tr>')
        body.append("</tbody>")
    head = ('<thead><tr><th></th><th class="n">Low end</th><th class="n">High end</th></tr></thead>')
    foot = f'<tfoot><tr class="total" data-sum="total"><th>Main estimate</th>{cells(tot, signed=False)}</tr></tfoot>'
    note = rounding_note(places, moved_lines(lines, shown, places))
    return f'<table class="ledger">{head}{"".join(body)}{foot}</table>', note


def running_shown(main, blocks, places, each=False):
    """Printed running sums: per block, the rounded start, then (step, total) per row. Each total is rounded;
    each step is the difference of the printed totals around it (`each`: rounded on its own). Also the
    number of steps that differ from their own rounding. The build stops if a step moves by more than a unit."""
    unit = Decimal(1).scaleb(-places)
    out, moved = [], 0
    for block in blocks:
        prev_true, prev = main, [Q.rounded(x, places) for x in main]
        start, steps = prev, []
        for r in block:
            if any(abs(a - b) > 1e-9 for a, b in zip(r["prev"], prev_true)):
                fail(f"{r['label']!r} does not continue the running sum above it")
            step = [r["value"][i] - r["prev"][i] for i in (0, 1)]
            total = [Q.rounded(x, places) for x in r["value"]]
            shown = [Q.rounded(x, places) for x in step] if each else [total[i] - prev[i] for i in (0, 1)]
            if any(abs(shown[i] - Decimal(repr(step[i]))) > unit for i in (0, 1)):
                fail(f"{r['label']!r}: printing {shown} for {step} moves it by more than {unit}")
            moved += sum(1 for i in (0, 1) if shown[i] != Q.rounded(step[i], places))
            steps.append((r, shown, total))
            prev_true, prev = r["value"], total
        out.append((start, steps))
    return out, moved


def alternatives_html(rows):
    """Other ways to count, as running sums from the main estimate: one block per alternative rule, then the costs
    outside public budgets. Returns the table and its caption."""
    main = next(r for r in rows if r.get("main"))["value"]
    keys = sorted({r["block"] for r in rows if "block" in r})
    blocks = [[r for r in rows if r.get("block") == k] for k in keys]
    places = 0 if running_shown(main, blocks, 0)[1] == 0 else 1
    shown, moved = running_shown(main, blocks, places, each=ROUND_EACH)
    out = []
    for k, (block, (start, steps)) in enumerate(zip(blocks, shown)):
        if k == 0:
            out.append(f'<tr class="cat" data-sum="start"><th>Main estimate</th>{cells(start, signed=False)}</tr>')
        else:
            if block[0].get("beside"):
                out.append('<tr class="cat"><th colspan="3">Separately, outside public budgets</th></tr>')
            out.append(f'<tr class="item" data-sum="start"><td>Main estimate</td>{cells(start, signed=False)}</tr>')
        for r, step, total in steps:
            out.append(f'<tr class="item" data-sum="step"><td>{html.escape(r["label"])}</td>{cells(step)}</tr>')
            out.append(f'<tr class="sub" data-sum="running"><td>= total</td>{cells(total, signed=False)}</tr>')
    head = '<thead><tr><th></th><th class="n">Low end</th><th class="n">High end</th></tr></thead>'
    note = rounding_note(places, moved)
    return f'<table class="ledger alt">{head}<tbody>{"".join(out)}</tbody></table>', note


SUM_ROW = re.compile(r'<tr [^>]*data-sum="(\w+)"[^>]*>(.*?)</tr>', re.S)
SUM_CELL = re.compile(r'<td class="n[^"]*">([^<]*)</td>')


def displayed_sum_errors(table):
    """The arithmetic of a rendered table, read from the printed numbers. In a ledger each category's lines
    add to its subtotal and the subtotals to the total; in running sums each total is the one before it plus
    the step between them. A table with no sums to check is an error too."""
    def printed(row):
        vals = [Decimal(c.replace("−", "-").replace("+", "")) for c in SUM_CELL.findall(row)]
        if len(vals) != 2:
            raise SystemExit(f"[BLOCKED] a summed row prints {len(vals)} numbers: {row[:80]!r}")
        return vals

    def label(row):
        return html.unescape(re.sub(r"<[^>]+>", " ", row.split("</t", 1)[0])).strip()

    def check(what, got, want):
        nonlocal n
        n += 1
        for i, end in enumerate(("low", "high")):
            if got[i] != want[i]:
                errs.append(f"{what}, {end} end: the parts add to {got[i]}, the table prints {want[i]}")
    errs, n = [], 0
    sub = parts = run = step = None
    subs = []
    for kind, row in SUM_ROW.findall(table):
        v = printed(row)
        if kind in ("subtotal", "total") and sub is not None:
            check(f"{sub[0]!r}", [sum(p[i] for p in parts) for i in (0, 1)], sub[1])
        if kind == "subtotal":
            sub, parts = (label(row), v), []
            subs.append(v)
        elif kind == "part":
            parts.append(v)
        elif kind == "total":
            check("the category subtotals", [sum(s[i] for s in subs) for i in (0, 1)], v)
            sub = None
        elif kind == "start":
            run, step = v, None
        elif kind == "step":
            step = (label(row), v)
        elif kind == "running":
            if run is None or step is None:
                errs.append("a running total with no start or step above it")
                continue
            check(f"{step[0]!r}", [run[i] + step[1][i] for i in (0, 1)], v)
            run, step = v, None
    if sub is not None:
        errs.append(f"{sub[0]!r} has no total row below it")
    if n == 0:
        errs.append("no printed sums found (the rows lost their data-sum marks?)")
    return errs


# Sums the prose states in words: (what, [(record, sign)], total record). At each end, the parts as printed must
# add to the total as printed. The bindings keep every sentence that states the sum quoting its records.
PROSE_SUMS = [
    ("the main estimate, less the low end's offending at the Hispanic average, plus the costs outside the budget",
     [("case.main", 1), ("pairing.footing_reduction", -1), ("social.items", 1)], "pairing.total"),
]


def prose_sum_errors(recs=None):
    """The prose sums at each end, on the values the page prints (each record's ends rounding)."""
    recs = recs if recs is not None else Q.load_registry()

    def end(rid, view):
        p = Q.parts(Q.record_value(rid, recs), recs[rid]["shape"])
        return Q.printed_value(p[view], recs[rid]["ends_round"])
    errs = []
    for what, parts, total in PROSE_SUMS:
        for view in ("at_low_end", "at_high_end"):
            got, want = sum(sign * end(rid, view) for rid, sign in parts), end(total, view)
            if got != want:
                errs.append(f"{what}, {view.replace('at_', '').replace('_', ' ')}: the parts print as {got}, "
                            f"{total} as {want}")
    return errs


# Claims the prose makes in words, with no number of their own: (phrase, record, test, what the test needs). The phrase
# must stand in some text site, and the record's unrounded value must pass the test.
PROSE_CLAIMS = [
    ("behind even at equal weight", "world.reading2_breakeven_us", lambda v: v > 1,
     "the US-only break-even weight above 1"),
]


def prose_claim_errors(sites, recs=None):
    """The claims the prose makes in words, on `sites` ((file, locator) → text, as `text_sites` gives them)."""
    recs = recs if recs is not None else Q.load_registry()
    errs = []
    for phrase, rid, test, needs in PROSE_CLAIMS:
        if not any(phrase in text for text in sites.values()):
            errs.append(f"{phrase!r} stands on no text site: drop its claim or restore the sentence")
        v = Q.record_value(rid, recs)
        if not test(v):
            errs.append(f"{phrase!r} needs {needs}; {rid} is {v}")
    return errs


def assumption_rows(s, bands):
    """(category, label, change at low end, change at high end, kind, link target). Link target: a finding's
    ladder ref, or "§<group id>" when no single finding covers the assumption."""
    m = bands["adopted"]

    def d(key):
        return [bands[key][0] - m[0], bands[key][1] - m[1]]

    def vs_main(rid):
        v = q(rid)
        return [v[0] - m[0], v[1] - m[1]]

    def approx(rid):
        """A row whose record the page would mark approximate says so."""
        return "approximate" if Q.is_approximate(Q.load_registry()[rid]) else ""

    resp, count, data, econ = ("How budgets respond to more people", "What the account counts",
                               "Data corrections and noise", "How the economy responds")
    return [
        (resp, "Services other than schools held fixed", *d("long_run_non_school_fixed:adopted"), "", "§services"),
        (resp, "Roads and parks respond only after years, as CBO assumes",
         *d("cbo_category_lag_non_school_full:with_rental_assistance_capital_and_enterprises"), "", "237"),
        (resp, "Every budget at its first-year response", *vs_main("case.first_year"), "", "270"),
        (resp, "General administration held fixed", *q("gg.fixed_change"), "", "211"),
        (resp, "Schools respond at the within-district 0.836", *d("school_within_district"), "", "230"),
        (resp, "Every service grows fully with population", *d("proportional_reference:adopted"), "", "§services"),
        (resp, "Rental assistance held fixed", *d("rental_assistance_at_0"), "", "§services"),
        (count, "Public capital earns 7%, not 2–3%", *d("capital_return_at_7pct"), "", "238"),
        (count, "No return on public capital", *d("without_capital_return"), "", "238"),
        (count, "Government enterprises left out", *d("enterprises_out_option_a"), "", "§conventions"),
        (count, "Pensions counted when paid", *d("cash_set"), "", "257"),
        # an additive arm: the accrual at scheduled benefits less the case's, outside the engine
        (count, "Pensions at the benefits scheduled, not those payable", *q("pension.scheduled_change"),
         "approximate", "257"),
        (count, "Pensions on one combined trust fund, as if the law changed",
         *d("pension_tr2026_combined_funds"), "", "286"),
        (count, "Retiree health promises equal what governments pay in a year", *d("retiree_health_rho_one"), "",
         "288"),
        (count, "Fewer descendants stopped reporting Mexican origin", *vs_main("case.arm_a"), "", "295"),
        (count, "More descendants stopped reporting Mexican origin", *vs_main("case.arm_c"), "", "295"),
        (count, "Added descendants' ages if childhood reports of origin persisted",
         *d("added_age_mix_cohort_at_birth"), "", "292"),
        (data, "Sampling noise, 95% interval", q("noise.sampling_95"), q("noise.sampling_95"), "noise", "184"),
        (data, "Share of the college gap that non-identifiers close, one standard error",
         *q("lineage.c3_se_change"), "pm", "295"),
        (data, "Survey answers left uncorrected", *q("corrections.uncorrected_change"), "", "§data"),
        (data, "Census income fill-ins left in", *d("no_fill_in_correction"), "", "208"),
        (econ, "Natives and immigrants are poor substitutes (ε = 3)", *q("production.eps3_change"),
         approx("production.eps3_change"), "176"),
    ]


def check_tornado_record(arows):
    """The registry's summary of the table (assumptions.move_range_above_noise) is the table's: the smallest and the
    largest move among the rows larger than the noise."""
    noise = next(r for r in arows if r[4] == "noise")[2]
    sizes = [max(abs(r[2]), abs(r[3])) for r in arows if r[4] != "noise"]
    want = (min(x for x in sizes if x > noise), max(sizes))
    got = q("assumptions.move_range_above_noise")
    if any(abs(a - b) > 1e-9 for a, b in zip(got, want)):
        fail(f"assumptions.move_range_above_noise is {got}, the table's rows give {want}")


def assumptions_html(rows, labels, sections):
    size = lambda r: max(abs(r[2]), abs(r[3]))
    cats = {}
    for r in rows:
        cats.setdefault(r[0], []).append(r)
    body = []
    for cat, items in sorted(cats.items(), key=lambda kv: -max(size(r) for r in kv[1])):
        body.append(f'<tbody><tr class="cat"><th colspan="4" scope="rowgroup">{html.escape(cat)}</th></tr>')
        for _c, label, lo, hi, kind, ref in sorted(items, key=lambda r: -size(r)):
            if ref.startswith("§") and ref[1:] in sections:
                flabel, fid = f"§{sections[ref[1:]]}", ref[1:]
            elif ref in labels:
                flabel, fid = labels[ref]
            else:
                fail(f"assumption {label!r} targets {ref}, which is neither a finding's ladder ref nor a section")
            # noise: one half-width for both ends; pm: a half-width at each end
            vals = (f'<td class="n noise" colspan="2">± {Q.rounded(lo, 0)}</td>' if kind == "noise" else
                    "".join(f'<td class="n noise">± {Q.rounded(x, 0)}</td>' for x in (lo, hi)) if kind == "pm" else
                    cells(whole([lo, hi])))
            note = f'<span class="note">{kind}</span>' if kind in ("approximate",) else ""
            body.append(f'<tr class="item"><td>{html.escape(label)}{note}</td>{vals}'
                        f'<td class="ref"><a href="#{fid}">{flabel}</a></td></tr>')
        body.append("</tbody>")
    head = ('<thead><tr><th>Assumption changed</th><th class="n">Low end</th><th class="n">High end</th>'
            '<th class="ref">Finding</th></tr></thead>')
    return f'<table class="ledger assume">{head}{"".join(body)}</table>'



# ---------------------------------------------------------------- quantities: lint and binding tests

def text_sites(template, groups):
    """(file, locator) → text of every unit that may quote a record: groups.py fields, template lines
    (tags removed) and ledger notes. A template binding names an anchor that must pick one line."""
    sites = {(f"{OV}/groups.py", loc): text for loc, text in Q.groups_sites(groups).items()}
    for n, line in enumerate(template.splitlines(), 1):
        sites[(f"{OV}/template.html", f"L{n}")] = Q.plain(line)
    for _cat, items in LEDGER:
        for step_label, _label, note in items:
            if note:
                sites[(f"{OV}/build.py", f"ledger/{step_label}/note")] = note
    return sites


def value_sites(wrows, arows):
    """(file, locator) → (values, label) of every table row whose numbers a binding may name."""
    out = {}
    for _c, label, lo, hi, _kind, _ref in arows:
        out[(f"{OV}/build.py", f"assumptions/{label}/value")] = ((lo, hi), label)
    for r in wrows:
        if r.get("alt") or r.get("beside"):
            out[(f"{OV}/build.py", f"alternatives/{r['label']}/value")] = (tuple(r["value"]), r["label"])
    for _cat, merged in ledger_lines(wrows):
        for label, m in merged.items():
            out[(f"{OV}/build.py", f"ledger/{label}/value")] = (tuple(m["v"]), label)
    return out


def check_quantities(template, groups, wrows, arows, bindings_path=None):
    """Refuse the page when a sentence quoting a record fails its lint, or a binding's site no longer
    quotes its record."""
    errs = []
    sites = text_sites(template, groups)
    for (file, loc), text in sorted(sites.items()):
        for rid, view, sent, e in Q.lint_unit(text):
            errs.append(f"{file} {loc}: {rid}|{view} in {sent!r} {'; '.join(e)}")
    rows = value_sites(wrows, arows)
    bindings = Q.load_bindings(bindings_path)
    for b in bindings:
        if (b["file"], b["locator"]) in rows:
            vals, label = rows[(b["file"], b["locator"])]
            errs += Q.value_binding_errors(b, vals, label)
        elif b["file"].endswith("template.html"):
            hits = [t for (f, loc), t in sites.items() if f == b["file"] and Q.anchored(b["locator"], t)]
            errs += (Q.binding_errors(b, hits[0]) if len(hits) == 1 else
                     [f"{b['file']} {b['locator']!r}: the anchor picks {len(hits)} lines"])
        else:
            errs += Q.binding_errors(b, sites.get((b["file"], b["locator"])))
    if errs:
        fail(f"{len(errs)} quantity test(s) failed:\n  " + "\n  ".join(errs))
    return len(bindings)


def load_evidence(groups_path):
    """The evidence module, reading GROUPS from `groups_path` (a copy, for the positive control)."""
    spec = importlib.util.spec_from_file_location("groups", groups_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.modules["groups"] = mod
    return importlib.import_module("evidence")


BUILD_START, BUILD_END = "<!-- BUILD_BLOCK:START -->", "<!-- BUILD_BLOCK:END -->"


def cut_build_block(template):
    """The template without its build fragment (the ledger sections between BUILD_START and BUILD_END), and the
    fragment. A template without the two comments gives (template, None)."""
    n = (template.count(BUILD_START), template.count(BUILD_END))
    if n == (0, 0):
        return template, None
    if n != (1, 1) or template.index(BUILD_END) < template.index(BUILD_START):
        fail(f"the template needs one {BUILD_START} before one {BUILD_END}; it has {n[0]} and {n[1]}")
    head, rest = template.split(BUILD_START)
    fragment, tail = rest.split(BUILD_END)
    return head + tail, fragment


def build_toc(fragment):
    """(anchor, title) for each <h3 id> in the build fragment: the first items of the build part's contents."""
    items = [(a, re.sub(r"<[^>]+>", "", t).strip())
             for a, t in re.findall(r'<h3\b[^>]*\bid="([^"]+)"[^>]*>(.*?)</h3>', fragment, flags=re.S)]
    if not items:
        fail("the build fragment has no <h3 id=...> heading for the contents to link to")
    return items


def main():
    global evidence, ROUND_EACH
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--groups", type=Path, default=HERE / "groups.py", help="another copy of groups.py")
    ap.add_argument("--template", type=Path, default=HERE / "template.html", help="another copy of template.html")
    ap.add_argument("--bindings", type=Path, default=Q.BINDINGS, help="another copy of quantity_bindings.csv")
    ap.add_argument("--out", type=Path, default=HERE / "derived/overview.html", help="where to write the page")
    ap.add_argument("--round-each", action="store_true",
                    help="round every table number on its own (the positive control for the printed-sum gate)")
    args = ap.parse_args()
    ROUND_EACH = args.round_each
    evidence = load_evidence(args.groups.resolve())
    entries = parse_ladder()
    s, bands, stairs = load_numbers()
    load_headcount()
    template = args.template.read_text()
    # With a build part in groups.py the template's build fragment moves to the marker after that part's heading.
    # Without one it stays where the template has it.
    rest, fragment = cut_build_block(template)
    has_part = any(pid == evidence.BUILD_PART for pid, _ in sys.modules["groups"].PARTS)
    if has_part and fragment is None:
        fail(f"groups.py has a '{evidence.BUILD_PART}' part, but the template has no {BUILD_START} … {BUILD_END} "
             "fragment to put in it")
    r = evidence.render(entries, fail, build_toc(fragment) if has_part else ())
    n_marker = (r["groups"].count(evidence.BUILD_MARKER), template.count(evidence.BUILD_MARKER))
    if n_marker != ((1 if has_part else 0), 0):
        fail(f"{evidence.BUILD_MARKER} appears {n_marker[0]} time(s) in the rendered parts and {n_marker[1]} in the "
             f"template; it belongs once in the '{evidence.BUILD_PART}' part and never in the template")
    page, groups_html = ((rest, r["groups"].replace(evidence.BUILD_MARKER, fragment)) if has_part
                         else (template, r["groups"]))
    wrows = waterfall_rows(s, stairs)
    arows = assumption_rows(s, bands)
    check_tornado_record(arows)
    # the text sites are the template's lines, wherever the fragment ends up
    n_bind = check_quantities(template, sys.modules["groups"].GROUPS, wrows, arows, args.bindings.resolve())
    (ledger, ledger_note), (alts, alts_note) = ledger_html(wrows), alternatives_html(wrows)
    errs = [f"ledger: {e}" for e in displayed_sum_errors(ledger)] + \
        [f"other ways to count: {e}" for e in displayed_sum_errors(alts)] + \
        [f"prose: {e}" for e in prose_sum_errors()]
    if errs:
        fail(f"{len(errs)} printed sum(s) do not add up:\n  " + "\n  ".join(errs))
    claims = prose_claim_errors(text_sites(template, sys.modules["groups"].GROUPS))
    if claims:
        fail(f"{len(claims)} claim(s) in words no longer hold:\n  " + "\n  ".join(claims))
    subs = {
        "{{GROUPS}}": groups_html,  # first: with a build part it carries the placeholders of the ledger sections
        "{{LEDGER}}": ledger,
        "{{LEDGER_NOTE}}": ledger_note,
        "{{ALTERNATIVES}}": alts,
        "{{ALTERNATIVES_NOTE}}": alts_note,
        "{{ASSUMPTIONS}}": assumptions_html(arows, r["labels"], r["sections"]),
        "{{TOC}}": r["toc"],
        "{{LEGEND}}": r["legend"],
        "{{BIBLIO}}": r["biblio"],
        "{{N_ENTRIES}}": str(len(entries)),
        "{{N_FINDINGS}}": str(r["n_find"]),
        "{{N_BIB}}": str(r["n_bib"]),
        "{{N_RETIRED}}": str(r["n_retired"]),
    }
    for k, v in subs.items():
        if k not in page:
            fail(f"template lacks {k}")
        page = page.replace(k, v)
    page, _ = Q.fill(page, markup=True)
    page = page.replace("{{APPROX_NOTE}}", APPROX_NOTE if 'class="approx"' in page else "")
    if "{{" in page:
        fail("unfilled placeholder: " + page[page.index("{{"):page.index("{{") + 30])
    out = args.out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    print(f"wrote {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}: {len(entries)} entries, "
          f"{r['n_find']} findings, {r['n_retired']} retired, {r['n_bib']} sources; {n_bind} bindings pass")


if __name__ == "__main__":
    main()
