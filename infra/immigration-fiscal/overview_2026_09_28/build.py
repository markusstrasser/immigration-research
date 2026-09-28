"""Build the evidence overview page: ladder entries sorted into groups, two charts, one time map.

    uv run --no-project python3 infra/immigration-fiscal/overview_2026_09_28/build.py

Reads the confidence ladder, the September 27 main case (`summary.json`, `main_case_bands.csv`)
and the figures page's staircase. Refuses to write if a ladder entry is unassigned or assigned
twice, or if the staircase and the main case disagree. Writes `derived/overview.html`.
"""

import csv
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import evidence  # noqa: E402

LADDER = ROOT / "research/immigration-confidence-ladder.md"
MAIN = ROOT / "infra/immigration-fiscal/main_case_long_run_2026_09_27/derived"
SOCIAL = ROOT / "infra/immigration-fiscal/sept27_propagation_2026_09_27/derived/real_costs_totals.csv"
# the population the account prices (row 4 of the data audit), not the CPS's raw union count
HEADCOUNT = ROOT / "infra/immigration-fiscal/main_case_decomposition_2026_09_29/derived/headcount.csv"


def load_headcount():
    """Priced and raw group size. Per-member figures divide engine totals by the priced count."""
    row = next(r for r in csv.DictReader(HEADCOUNT.open()) if r["cut"] == "all" and r["group"] == "union")
    priced, raw = float(row["row4"]), float(row["published"])
    if not (39e6 < priced < 41e6 and priced <= raw):
        fail(f"headcount out of range: priced {priced:,.0f}, raw {raw:,.0f}")
    return priced, raw
STAIRS = ROOT / "infra/immigration-fiscal/figures_2026_09_22/src/generated/figures.json"



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
    "gg": ("General administration", "0.60–0.85% per 1% more residents"),
    "taxes": ("Taxes checked against records", "off-books work, survey fill-ins, top incomes"),
    "benefits": ("Benefits and services checked against records", "credits, medical care, schools, care"),
}


def load_social():
    """Fiscal plus social total at central values, the published pairing (RESULT_ledger.md):
    the mixed-group Hispanic footing at the low end, custody at the high end, every row on the
    39.71M people the account prices (population_basis_2026_09_29, ladder 274)."""
    rows = {(r["column"], r["item"]): float(r["sept27"]) for r in csv.DictReader(SOCIAL.open()) if r["section"] == "7" and r["sept27"]}
    return [rows[("pairing_on_priced_count", "published pairing (low)")],
            rows[("pairing_on_priced_count", "published pairing (high)")]]


def waterfall_rows(s, stairs, social):
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
    d26 = [a - b for a, b in zip(s["adopted_2026_09_26"], s["adopted_2026_09_24"])]
    sch = [a - b for a, b in zip(s["schools_case"], s["adopted_2026_09_26"])]
    ent = s["enterprises"]
    ent_surplus = ent["receipt_at_end_specifications"]["cost_bn"]
    capital_total = s["capital_at_end_specifications"]["total_bn"]
    ent_capital = [t - core - block for t, core, block in zip(capital_total, c["capital_core"], c["capital_block"])]
    rows += [
        dict(label="Consumption taxes on spending", note="net of saving and remittances", step=d26),
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
    # Other ways to count, typed from the research record (pension accrual, property-tax receipts, social rows).
    alt = [290.5, 355.8]
    rows += [
        dict(label="Property taxes follow people, with smaller tax fixes", alt=True, prev=list(tot), value=alt),
        dict(label="Pensions counted when earned", alt=True, prev=alt, value=[368.0, 429.0]),
        dict(label="Costs outside public budgets", beside=True, prev=list(tot), value=list(social)),
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
        ("Schools, long run: full cost per pupil", "Schools, full cost per pupil", None),
        ("Colleges and other education", "Colleges and other education", ""),
    ]),
    ("Other public services", [
        ("Police, courts and prisons", "Police, courts and prisons", "charged by use"),
        ("General administration", "General administration", "0.60–0.85% per 1% more residents"),
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


def num(x, signed=True):
    """Whole $bn with a true minus sign; '0' when it rounds to zero."""
    r = round(x)
    if r == 0:
        return "0"
    return (("+" if r > 0 else "−") if signed else ("" if r > 0 else "−")) + f"{abs(r)}"


def cells(v, signed=True, cls=""):
    tone = lambda x: "gain" if round(x) < 0 else ("cost" if round(x) > 0 else "")
    return "".join(f'<td class="n {tone(x) if signed else ""} {cls}">{num(x, signed)}</td>' for x in v)


def ledger_html(rows):
    """Two-level ledger: category subtotals, items ranked by size, columns that sum to the main estimate."""
    steps = {r["label"]: r["step"] for r in rows if "step" in r}
    used = set()
    body, total = [], [0.0, 0.0]
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
        sub = [sum(m["v"][i] for m in merged.values()) for i in (0, 1)]
        total = [total[i] + sub[i] for i in (0, 1)]
        body.append(f'<tbody><tr class="cat"><th scope="rowgroup">{html.escape(cat)}</th>{cells(sub)}</tr>')
        for label, m in sorted(merged.items(), key=lambda kv: -max(abs(kv[1]["v"][0]), abs(kv[1]["v"][1]))):
            note = f'<span class="note">{html.escape(m["note"])}</span>' if m["note"] else ""
            body.append(f'<tr class="item"><td>{html.escape(label)}{note}</td>{cells(m["v"])}</tr>')
        body.append("</tbody>")
    missing = set(steps) - used
    if missing:
        fail(f"staircase steps missing from the ledger: {sorted(missing)}")
    main = next(r for r in rows if r.get("main"))["value"]
    if any(abs(a - b) > 1e-3 for a, b in zip(total, main)):
        fail(f"ledger sums to {total}, main estimate is {main}")
    head = ('<thead><tr><th></th><th class="n">Low end</th><th class="n">High end</th></tr></thead>')
    foot = f'<tfoot><tr class="total"><th>Main estimate</th>{cells(main, signed=False)}</tr></tfoot>'
    return f'<table class="ledger">{head}{"".join(body)}{foot}</table>'


def alternatives_html(rows):
    """Other ways to count, as running sums from the main estimate."""
    main = next(r for r in rows if r.get("main"))["value"]
    out = [f'<tr class="cat"><th>Main estimate</th>{cells(main, signed=False)}</tr>']
    for r in rows:
        if r.get("alt") or r.get("beside"):
            step = [r["value"][i] - r["prev"][i] for i in (0, 1)]
            if r.get("beside"):
                out.append('<tr class="cat"><th colspan="3">Separately, outside public budgets</th></tr>'
                           f'<tr class="item"><td>Main estimate</td>{cells(main, signed=False)}</tr>')
            out.append(f'<tr class="item"><td>{html.escape(r["label"])}</td>{cells(step)}</tr>')
            out.append(f'<tr class="sub"><td>= total</td>{cells(r["value"], signed=False)}</tr>')
    head = '<thead><tr><th></th><th class="n">Low end</th><th class="n">High end</th></tr></thead>'
    return f'<table class="ledger alt">{head}<tbody>{"".join(out)}</tbody></table>'


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
        (resp, "General administration held fixed", -28.5, -40.6, "approximate", "211"),
        (resp, "Schools respond at the within-district 0.836", *d("school_within_district"), "", "230"),
        (resp, "Every service grows fully with population", *d("proportional_reference:adopted"), "", "§services"),
        (resp, "Rental assistance held fixed", *d("rental_assistance_at_0"), "", "§services"),
        (count, "Public capital earns 7%, not 2–3%", *d("capital_return_at_7pct"), "", "238"),
        (count, "No return on public capital", *d("without_capital_return"), "", "238"),
        (count, "Government enterprises left out", *d("enterprises_out_option_a"), "", "§conventions"),
        (data, "Sampling noise, 95% interval", 20.8, 20.8, "noise", "184"),
        (data, "Survey answers left uncorrected", *d("uncorrected_at_adopted_responses"), "", "§data"),
        (data, "Census income fill-ins left in", *d("no_fill_in_correction"), "", "208"),
        (econ, "Natives and immigrants are poor substitutes (ε = 3)", -13.8, -9.1, "", "176"),
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
            vals = (f'<td class="n noise" colspan="2">± {round(lo)}</td>' if kind == "noise" else cells([lo, hi]))
            note = f'<span class="note">{kind}</span>' if kind in ("approximate",) else ""
            body.append(f'<tr class="item"><td>{html.escape(label)}{note}</td>{vals}'
                        f'<td class="ref"><a href="#{fid}">{flabel}</a></td></tr>')
        body.append("</tbody>")
    head = ('<thead><tr><th>Assumption changed</th><th class="n">Low end</th><th class="n">High end</th>'
            '<th class="ref">Finding</th></tr></thead>')
    return f'<table class="ledger assume">{head}{"".join(body)}</table>'




def main():
    entries = parse_ladder()
    s, bands, stairs = load_numbers()
    social = load_social()
    r = evidence.render(entries, fail)
    wrows = waterfall_rows(s, stairs, social)
    page = (HERE / "template.html").read_text()
    subs = {
        "{{LEDGER}}": ledger_html(wrows),
        "{{ALTERNATIVES}}": alternatives_html(wrows),
        "{{ASSUMPTIONS}}": assumptions_html(assumption_rows(s, bands), r["labels"], r["sections"]),
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
    add = [social[0] - s["main_case"][0], social[1] - s["main_case"][1]]
    mid = lambda v: round((v[0] + v[1]) / 2 / 5) * 5
    priced, _raw = load_headcount()
    pm = [x * 1e9 / priced / 1e3 for x in s["main_case"]]
    for k, v in {"{{PER_MEMBER}}": f"${(pm[0] + pm[1]) / 2:.1f}k ({pm[0]:.1f}–{pm[1]:.1f})",
                 "{{GROUP_SIZE}}": f"{priced / 1e6:.1f}M","{{SOCIAL_TOTAL}}": f"about ${mid(social)}bn ({social[0]:.0f}–{social[1]:.0f})",
                 "{{SOCIAL_ADD_WORDS}}": f"about ${mid(add)}bn",
                 "{{SOCIAL_ADD}}": f"about ${mid(add)}bn ({add[0]:.0f}–{add[1]:.0f})"}.items():
        page = page.replace(k, v)
    if "{{" in page:
        fail("unfilled placeholder: " + page[page.index("{{"):page.index("{{") + 30])
    out = HERE / "derived/overview.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page)
    print(f"wrote {out.relative_to(ROOT)}: {len(entries)} entries, {r['n_find']} findings, "
          f"{r['n_retired']} retired, {r['n_bib']} sources")

if __name__ == "__main__":
    main()
