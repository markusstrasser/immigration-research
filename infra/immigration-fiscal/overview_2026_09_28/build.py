"""Build the evidence overview page: ladder entries sorted into groups, two charts, one time map.

    uv run --no-project python3 infra/immigration-fiscal/overview_2026_09_28/build.py

Reads the confidence ladder, the September 27 main case (`summary.json`, `main_case_bands.csv`)
and the figures page's staircase. Refuses to write if a ladder entry is unassigned or assigned
twice, or if the staircase and the main case disagree. Writes `derived/overview.html`.

Numbers that the text quotes from a file come from `quantity_registry.csv` through placeholders,
`{{q:<id>|<view>}}`, which `quantities.py` renders. The build lints every sentence that quotes a
record, runs the binding tests in `quantity_bindings.csv`, and refuses to write on any failure.
`--groups PATH` reads another copy of groups.py and `--out PATH` writes elsewhere (the positive
controls use both).
"""

import argparse
import csv
import html
import importlib
import importlib.util
import json
import re
import sys
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import quantities as Q  # noqa: E402

evidence = None  # imported in main(), after --groups has picked the groups module it reads

LADDER = ROOT / "research/immigration-confidence-ladder.md"
MAIN = ROOT / "infra/immigration-fiscal/main_case_long_run_2026_09_27/derived"
STAIRS = ROOT / "infra/immigration-fiscal/figures_2026_09_22/src/generated/figures.json"
OV = "infra/immigration-fiscal/overview_2026_09_28"


def q(rid):
    """A registry record's value, unrounded: a list for a pair of ends, else a number."""
    v = Q.record_value(rid)
    return list(v) if isinstance(v, tuple) else v


def load_headcount():
    """Priced and raw group size. Per-member figures divide engine totals by the priced count, the
    population the account prices (row 4 of the data audit), not the CPS's raw union count."""
    priced, raw = q("headcount.priced") * 1e6, q("headcount.raw") * 1e6
    if not (39e6 < priced < 41e6 and priced <= raw):
        fail(f"headcount out of range: priced {priced:,.0f}, raw {raw:,.0f}")
    return priced, raw



def fail(msg):
    sys.exit(f"[BLOCKED] {msg}")


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
    stairs = json.loads(STAIRS.read_text())["staircase"]
    main = s["main_case"]
    sept24 = s["adopted_2026_09_24"]
    last = next(r for r in stairs if r["id"] == "benefits")
    if any(abs(a - b) > 1e-3 for a, b in zip(last["total"], sept24)):
        fail(f"staircase ends at {last['total']}, summary.json September 24 case is {sept24}")
    if any(abs(a - b) > 1e-3 for a, b in zip(bands["adopted"], main)):
        fail("main_case_bands.csv and summary.json disagree on the adopted case")
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
    ent = s["enterprises"]
    ent_surplus = ent["receipt_at_end_specifications"]["cost_bn"]
    capital_total = s["capital_at_end_specifications"]["total_bn"]
    ent_capital = [t - core - block for t, core, block in zip(capital_total, c["capital_core"], c["capital_block"])]
    rows += [
        dict(label="Consumption taxes on spending", note="net of saving and remittances", step=key26),
        dict(label="Schools, finite removal", note="", step=sch26),
        dict(label="General administration, finite removal", note="", step=gg26),
        dict(label="Schools, long run: full cost per pupil", note="spending rises ~1% per 1% more pupils", step=sch),
        dict(label="September 26 schools case", total=True),
        dict(label="Roads, parks: long-run response", note="0.73 and 0.95 across states", step=c["long_run_responses"]),
        dict(label="Rental assistance at 1", note="", step=c["rental_assistance"]),
        dict(label="Return on public capital", note="2% real low end, 3% high end", step=[a + b for a, b in zip(c["capital_core"], c["capital_block"])]),
        dict(label="Government enterprises", note="operating loss and capital return", step=[ent_surplus[0] + ent_capital[0], ent_surplus[1] + ent_capital[1]]),
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
    for label, key in [("September 23 case", None), ("September 24 case", "adopted_2026_09_24"),
                       ("September 26 schools case", "schools_case")]:
        if key:
            v = next(r for r in rows if r["label"] == label)["value"]
            if any(abs(a - b) > 1e-3 for a, b in zip(v, s[key])):
                fail(f"{label} subtotal {v} != summary {s[key]}")
    rows = [r for r in rows if not r.get("total") or r.get("main")]
    # Other ways to count, from the registry: the pending set run as one (candidate v4), pension accrual on top,
    # the social pairing. The pairing's low end prices offending at the Hispanic average, so its fiscal case
    # moves first and the social step is the social items alone.
    alt, fisc = q("candidate_v4.set_cash"), q("pairing.fiscal_footing")
    if abs(fisc[1] - s["main_case"][1]) > 1e-6:  # the totals file keeps six decimals
        fail(f"the pairing's high-end fiscal case {fisc[1]} is not the main case's {s['main_case'][1]}")
    if any(abs(p - f - x) > 1e-9 for p, f, x in zip(q("pairing.total"), fisc, q("social.items"))):
        fail("the pairing less its fiscal case is not social.items")
    rows += [
        dict(label="Property taxes follow people, with smaller corrections", alt=True, prev=list(tot), value=alt),
        dict(label="Pensions counted when earned", alt=True, prev=alt, value=q("candidate_v4.set_accrual_payable")),
        dict(label="Offending at the Hispanic average, low end", beside=True, prev=list(tot), value=fisc),
        dict(label="Costs outside public budgets", beside=True, prev=fisc, value=q("pairing.total")),
    ]
    return rows


# Ledger categories: (category, [(step label on the staircase, reader label, note)]). Items inside a category
# are ranked by size at render time. Two staircase steps can share one reader label; they are summed.
LEDGER = [
    ("The group's own taxes and benefits", [
        ("Taxes paid minus benefits received", "Taxes paid minus benefits received", "survey values"),
        ("Taxes checked against records", "Taxes corrected with records", "off-books work, survey fill-ins, top incomes"),
        ("Benefits and services checked against records", "Benefits and services corrected with records",
         "tax credits, medical care, schools, care"),
        ("Gain from their work", "Taxes on the gain from their work", "wages and profits of others"),
        ("Consumption taxes on spending", "Sales and excise taxes", "net of saving and remittances"),
    ]),
    ("Schools and colleges", [
        ("Schools, first-year budget response", "Schools, full cost per pupil",
         "spending rises about 1% per 1% more pupils"),
        ("Schools, finite removal", "Schools, full cost per pupil", None),
        ("Schools, long run: full cost per pupil", "Schools, full cost per pupil", None),
        ("Colleges and other education", "Colleges and other education", ""),
    ]),
    ("Other public services", [
        ("Police, courts and prisons", "Police, courts and prisons", "charged by use"),
        ("General administration", "General administration", "{{q:gg.growth_elasticity|range}}% per 1% more residents"),
        ("General administration, finite removal", "General administration", None),
        ("Welfare administration, housing, community", "Welfare administration, housing, community", ""),
        ("Public health services", "Public health", ""),
        ("Roads, parks: long-run response", "Roads and parks", "0.73% and 0.95% per 1% more residents"),
        ("Rental assistance at 1", "Rental assistance", ""),
        ("Unpaid hospital care", "Unpaid hospital care", "charged by uninsured use"),
    ]),
    ("Public capital and enterprises", [
        ("Return on public capital", "Return on public capital", "2% real at the low end, 3% at the high end"),
        ("Government enterprises", "Government enterprises", "operating loss and capital return"),
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
    """Other ways to count, as running sums from the main estimate: the alternative rules, then the costs
    outside public budgets. Returns the table and its caption."""
    main = next(r for r in rows if r.get("main"))["value"]
    blocks = [[r for r in rows if r.get(k)] for k in ("alt", "beside")]
    places = 0 if running_shown(main, blocks, 0)[1] == 0 else 1
    shown, moved = running_shown(main, blocks, places, each=ROUND_EACH)
    out = []
    for k, (start, steps) in enumerate(shown):
        if k == 0:
            out.append(f'<tr class="cat" data-sum="start"><th>Main estimate</th>{cells(start, signed=False)}</tr>')
        else:
            out.append('<tr class="cat"><th colspan="3">Separately, outside public budgets</th></tr>'
                       f'<tr class="item" data-sum="start"><td>Main estimate</td>{cells(start, signed=False)}</tr>')
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


def assumption_rows(s, bands):
    """(category, label, change at low end, change at high end, kind, link target). Link target: a finding's
    ladder ref, or "§<group id>" when no single finding covers the assumption."""
    m = bands["adopted"]

    def d(key):
        return [bands[key][0] - m[0], bands[key][1] - m[1]]

    resp, count, data, econ = ("How budgets respond to more people", "What the account counts",
                               "Data corrections and noise", "How the economy responds")
    return [
        (resp, "Services other than schools held fixed", *d("long_run_non_school_fixed:adopted"), "", "§services"),
        (resp, "Roads and parks respond only after years, as CBO assumes",
         *d("cbo_category_lag_non_school_full:with_rental_assistance_capital_and_enterprises"), "", "237"),
        (resp, "General administration held fixed", *q("gg.fixed_change"), "", "211"),
        (resp, "Schools respond at the within-district 0.836", *d("school_within_district"), "", "230"),
        (resp, "Every service grows fully with population", *d("proportional_reference:adopted"), "", "§services"),
        (resp, "Rental assistance held fixed", *d("rental_assistance_at_0"), "", "§services"),
        (count, "Public capital earns 7%, not 2–3%", *d("capital_return_at_7pct"), "", "238"),
        (count, "No return on public capital", *d("without_capital_return"), "", "238"),
        (count, "Government enterprises left out", *d("enterprises_out_option_a"), "", "§conventions"),
        (data, "Sampling noise, 95% interval", q("noise.sampling_95"), q("noise.sampling_95"), "noise", "184"),
        (data, "Survey answers left uncorrected", *d("uncorrected_at_adopted_responses"), "", "§data"),
        (data, "Census income fill-ins left in", *d("no_fill_in_correction"), "", "208"),
        (econ, "Natives and immigrants are poor substitutes (ε = 3)", *q("production.eps3_change"), "", "176"),
    ]


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
            vals = (f'<td class="n noise" colspan="2">± {Q.rounded(lo, 0)}</td>' if kind == "noise" else
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


def check_quantities(template, groups, wrows, arows):
    """Refuse the page when a sentence quoting a record fails its lint, or a binding's site no longer
    quotes its record."""
    errs = []
    sites = text_sites(template, groups)
    for (file, loc), text in sorted(sites.items()):
        for rid, view, sent, e in Q.lint_unit(text):
            errs.append(f"{file} {loc}: {rid}|{view} in {sent!r} {'; '.join(e)}")
    rows = value_sites(wrows, arows)
    bindings = Q.load_bindings()
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


def main():
    global evidence, ROUND_EACH
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--groups", type=Path, default=HERE / "groups.py", help="another copy of groups.py")
    ap.add_argument("--out", type=Path, default=HERE / "derived/overview.html", help="where to write the page")
    ap.add_argument("--round-each", action="store_true",
                    help="round every table number on its own (the positive control for the printed-sum gate)")
    args = ap.parse_args()
    ROUND_EACH = args.round_each
    evidence = load_evidence(args.groups.resolve())
    entries = parse_ladder()
    s, bands, stairs = load_numbers()
    load_headcount()
    r = evidence.render(entries, fail)
    wrows = waterfall_rows(s, stairs)
    arows = assumption_rows(s, bands)
    page = (HERE / "template.html").read_text()
    n_bind = check_quantities(page, sys.modules["groups"].GROUPS, wrows, arows)
    (ledger, ledger_note), (alts, alts_note) = ledger_html(wrows), alternatives_html(wrows)
    errs = [f"ledger: {e}" for e in displayed_sum_errors(ledger)] + \
        [f"other ways to count: {e}" for e in displayed_sum_errors(alts)]
    if errs:
        fail(f"{len(errs)} printed sum(s) do not add up:\n  " + "\n  ".join(errs))
    subs = {
        "{{LEDGER}}": ledger,
        "{{LEDGER_NOTE}}": ledger_note,
        "{{ALTERNATIVES}}": alts,
        "{{ALTERNATIVES_NOTE}}": alts_note,
        "{{ASSUMPTIONS}}": assumptions_html(arows, r["labels"], r["sections"]),
        "{{TOC}}": r["toc"],
        "{{GROUPS}}": r["groups"],
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
    if "{{" in page:
        fail("unfilled placeholder: " + page[page.index("{{"):page.index("{{") + 30])
    out = args.out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    print(f"wrote {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}: {len(entries)} entries, "
          f"{r['n_find']} findings, {r['n_retired']} retired, {r['n_bib']} sources; {n_bind} bindings pass")


if __name__ == "__main__":
    main()
