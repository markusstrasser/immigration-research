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
STAIRS = ROOT / "infra/immigration-fiscal/figures_2026_09_22/src/generated/figures.json"

ORANGE, ORANGE_FILL = "#ca7a5e", "#f2cabc"
BLUE, BLUE_FILL = "#5c97d2", "#bbd4ee"
INK, GREY, GREY_FILL = "#111111", "#8d897e", "#e4e1d6"


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
    the mixed-group Hispanic footing at the low end, custody at the high end."""
    rows = {(r["column"], r["item"]): float(r["sept27"]) for r in csv.DictReader(SOCIAL.open()) if r["section"] == "7" and r["sept27"]}
    return [rows[("hispanic_mixed_group", "total at central values (low)")],
            rows[("custody", "total at central values (high)")]]


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
    # Alternative and beside rows, typed from the ladder (entries 257, 195, 253, candidate v3 RESULT).
    rows += [
        dict(label="Alternative: property taxes follow people", note="with smaller tax-key fixes (253, 249)", pending=True,
             prev=list(tot), value=[290.5, 355.8]),
        dict(label="+ pensions counted when earned", note="current-law benefits (257)", pending=True,
             prev=[290.5, 355.8], value=[368.0, 429.0]),
        dict(label="Main estimate + costs outside budgets", note="victims, traffic, housing, fear (195, 258)", beside=True,
             prev=list(tot), value=list(social)),
    ]
    return rows


def tornado_rows(s, bands, social):
    m = bands["adopted"]

    def d(key):
        return [bands[key][0] - m[0], bands[key][1] - m[1]]

    rows = [
        ("Capital return at 7%, not 2–3%", d("capital_return_at_7pct"), "beside", "238"),
        ("Pensions counted when earned", [77.3, 73.6], "waiting", "257"),
        ("Services other than schools held fixed", [bands["long_run_non_school_fixed:adopted"][i] - m[i] for i in (0, 1)], "arm", "§services"),
        ("Costs outside budgets added", [social[0] - m[0], social[1] - m[1]], "beside", "§social"),
        ("No return on public capital", d("without_capital_return"), "arm", "238"),
        ("Roads and parks at CBO's lag of 0", [bands["cbo_category_lag_non_school_full:with_rental_assistance_capital_and_enterprises"][i] - m[i] for i in (0, 1)], "arm", "237"),
        ("General administration fixed (earlier version)", [-28.5, -40.6], "arm", "211"),
        ("Property taxes follow people", [-27.19, -27.19], "candidate", "253"),
        ("Schools at within-district 0.836", d("school_within_district"), "arm", "230"),
        ("Every service fully proportional", [bands["proportional_reference:adopted"][i] - m[i] for i in (0, 1)], "arm", "§services"),
        ("Enterprises left out", d("enterprises_out_option_a"), "arm", "§conventions"),
        ("Sampling noise (95%)", [20.8, 20.8], "noise", "184"),
        ("Natives and immigrants poor substitutes, ε = 3", [-13.8, -9.1], "arm", "176"),
        ("Survey data left uncorrected", d("uncorrected_at_adopted_responses"), "arm", "§data"),
        ("Census income fill-ins left in", d("no_fill_in_correction"), "arm", "208"),
        ("Rental assistance at 0", d("rental_assistance_at_0"), "arm", "§services"),
        ("Income-tax shares matched to IRS", [-3.2, -3.1], "candidate", "249"),
    ]
    return sorted(rows, key=lambda r: -max(abs(r[1][0]), abs(r[1][1])))


# ---------------------------------------------------------------- rendering

def fmt(x):
    return f"{abs(x):.0f}"


def rng(a, b):
    lo, hi = sorted((abs(a), abs(b)))
    return fmt(lo) if round(lo) == round(hi) else f"{fmt(lo)}–{fmt(hi)}"


def words(a, b):
    if a >= 0 and b >= 0:
        return f"worse off by {rng(a, b)}"
    if a <= 0 and b <= 0:
        return f"better off by {rng(a, b)}"
    if max(abs(a), abs(b)) < 1:
        return "about 0"
    return f"{fmt(a)} / {fmt(b)}"


def svg_waterfall(rows):
    x0, x1 = -100.0, 540.0
    lw, W, rh = 290, 800, 30
    pw = W - lw - 20

    def X(v):
        return lw + (v - x0) / (x1 - x0) * pw

    H = 40 + rh * len(rows) + 30
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Waterfall from taxes minus benefits to the main case" class="chart">']
    for t in range(-100, 501, 100):
        if t > x1:
            break
        out.append(f'<line x1="{X(t):.1f}" x2="{X(t):.1f}" y1="28" y2="{H - 26}" class="grid{" zero" if t == 0 else ""}"/>')
        out.append(f'<text x="{X(t):.1f}" y="{H - 10}" class="tick" text-anchor="middle">{abs(t)}</text>')
    out.append(f'<text x="{X(0) - 6:.1f}" y="18" class="axis" text-anchor="end">← everyone else better off</text>')
    out.append(f'<text x="{X(0) + 6:.1f}" y="18" class="axis">everyone else worse off, $bn a year →</text>')
    y = 36
    for r in rows:
        cls = "main" if r.get("main") else ("total" if r.get("total") else "")
        out.append(f'<text x="{lw - 10}" y="{y + 13}" class="lab {cls}" text-anchor="end">{html.escape(r["label"])}</text>')
        if r.get("note"):
            out.append(f'<text x="{lw - 10}" y="{y + 25}" class="note" text-anchor="end">{html.escape(r["note"])}</text>')
        v = r["value"]
        if r.get("total"):
            a, b = sorted(v)
            out.append(f'<rect x="{X(0):.1f}" y="{y + 3}" width="{X(a) - X(0):.1f}" height="16" fill="{GREY_FILL}"/>')
            out.append(f'<rect x="{X(a):.1f}" y="{y + 3}" width="{X(b) - X(a):.1f}" height="16" fill="{"#57544c" if r.get("main") else GREY}"/>')
            out.append(f'<text x="{X(b) + 6:.1f}" y="{y + 15}" class="val {cls}">{fmt(a)}–{fmt(b)}</text>')
        else:
            p = r["prev"]
            dash = ' stroke-dasharray="3 2"' if r.get("pending") or r.get("beside") else ""
            for k, dy in ((0, 3), (1, 12)):
                lo, hi = sorted((p[k], v[k]))
                worse = v[k] >= p[k]
                fill = "none" if dash else (ORANGE_FILL if worse else BLUE_FILL)
                line = ORANGE if worse else BLUE
                out.append(f'<rect x="{X(lo):.1f}" y="{y + dy}" width="{max(X(hi) - X(lo), 1):.1f}" height="8" fill="{fill}" stroke="{line}" stroke-width="1"{dash}/>')
            steps = [v[0] - p[0], v[1] - p[1]]
            txt = words(*steps)
            if r.get("pending") or r.get("beside"):
                txt = f"{fmt(v[0])}–{fmt(v[1])}"
            xr = X(max(p[0], p[1], v[0], v[1])) + 6
            out.append(f'<text x="{xr:.1f}" y="{y + 15}" class="val">{txt}</text>')
        y += rh
    out.append("</svg>")
    return "\n".join(out)


def svg_tornado(rows, labels, sections):
    """Each row links to the finding that holds its ladder ref, or to a section ("§<id>") when no single
    finding covers the assumption. An unknown target fails."""
    x0, x1 = -70.0, 110.0
    lw, W, rh = 330, 760, 24
    pw = W - lw - 90

    def X(v):
        return lw + (v - x0) / (x1 - x0) * pw

    H = 40 + rh * len(rows) + 26
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="How far each choice moves the main case" class="chart">']
    for t in range(-60, 101, 20):
        out.append(f'<line x1="{X(t):.1f}" x2="{X(t):.1f}" y1="28" y2="{H - 24}" class="grid{" zero" if t == 0 else ""}"/>')
        out.append(f'<text x="{X(t):.1f}" y="{H - 8}" class="tick" text-anchor="middle">{abs(t)}</text>')
    out.append(f'<text x="{X(0) - 6:.1f}" y="18" class="axis" text-anchor="end">← lower cost</text>')
    out.append(f'<text x="{X(0) + 6:.1f}" y="18" class="axis">higher cost, $bn a year →</text>')
    tag = {"waiting": "alternative", "candidate": "alternative", "beside": "beside", "arm": "", "noise": "noise"}
    y = 34
    for label, (a, b), status, ref in rows:
        if ref.startswith("§") and ref[1:] in sections:
            flabel, fid = f"§{sections[ref[1:]]}", ref[1:]
        elif ref in labels:
            flabel, fid = labels[ref]
        else:
            fail(f"tornado row {label!r} targets {ref}, which is neither a finding's ladder ref nor a section")
        out.append(f'<a href="#{fid}"><text x="{lw - 10}" y="{y + 13}" class="lab" text-anchor="end">'
                   f'{html.escape(label)}<tspan class="ref"> · {flabel}</tspan></text></a>')
        for k, dy, v in ((0, 3, a), (1, 11, b)):
            if status == "noise":
                lo, hi = -v, v
                col, fill = GREY, GREY_FILL
            else:
                lo, hi = sorted((0, v))
                col, fill = (ORANGE, ORANGE_FILL) if v > 0 else (BLUE, BLUE_FILL)
            dash = ' stroke-dasharray="3 2"' if status in ("waiting", "candidate", "beside") else ""
            if dash:
                fill = "none"
            out.append(f'<rect x="{X(lo):.1f}" y="{y + dy}" width="{max(X(hi) - X(lo), 1):.1f}" height="7" fill="{fill}" stroke="{col}"{dash}/>')
        val = f"± {fmt(a)}" if status == "noise" else rng(a, b)
        xr = X(max(0, a, b, (a if status == "noise" else 0))) + 6
        out.append(f'<text x="{xr:.1f}" y="{y + 14}" class="val">{val}<tspan class="ref"> {tag[status]}</tspan></text>')
        y += rh
    out.append("</svg>")
    return "\n".join(out)




def main():
    entries = parse_ladder()
    s, bands, stairs = load_numbers()
    social = load_social()
    r = evidence.render(entries, fail)
    page = (HERE / "template.html").read_text()
    subs = {
        "{{WATERFALL}}": svg_waterfall(waterfall_rows(s, stairs, social)),
        "{{TORNADO}}": svg_tornado(tornado_rows(s, bands, social), r["labels"], r["sections"]),
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
    for k, v in {"{{SOCIAL_TOTAL}}": f"about ${mid(social)}bn ({social[0]:.0f}–{social[1]:.0f})",
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
