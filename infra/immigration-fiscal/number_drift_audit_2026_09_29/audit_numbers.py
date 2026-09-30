"""Audit the numbers a reader sees against their authoritative sources.

    uv run --no-project --offline python3 infra/immigration-fiscal/number_drift_audit_2026_09_29/audit_numbers.py

Reads the reader-facing texts (the evidence map's groups.py, template.html and build.py's hand-typed
table rows and notes; chosen spans of the topic INDEX, the objections FAQ, CLAUDE.md and three research memos
restated on the adopted case), extracts every number token, and matches each one to its source. A number the
map quotes through a placeholder,
`{{q:<id>|<view>}}`, is rendered by the map's `quantities.py` exactly as the build renders it and is
checked against its registry record: the rendering against the value, and the sentence against the
record's must_name and forbid. Every other number is matched to the source that `source_map.csv` names
for it. Writes `derived/number_audit.csv` (one row per audited number), `derived/extracted_numbers.csv`
(every token found, with its map key) and `derived/inputs.json` (the hash of every file read). Never
writes outside this lane.

Status of a number:
    MATCH          equal to its source after the display's rounding (for a placeholder: its record's
                   value, and the sentence passes the record's lint)
    STALE          unequal to its source, equal to the superseded value the map names
    MISMATCH       equal to neither (both values shown)
    UNSOURCEABLE   no source located; the map's note says what was searched
    CONTEXT-SHIFT  equal to its source, but the text gives it another population, year,
                   comparison or accounting treatment (the map's `context` says which; for a
                   placeholder, the sentence fails the record's lint)

A map row is keyed by (file, locator, ordinal): a structural locator for groups.py and build.py
("account/f239/text"), an anchor string for the line of any other file, and the token's position
within that unit (digits "0", "1", …; curated word numbers "w0", …). The number as shown is never
part of the key, so an edited number is compared with the same source and fails. When numbers were
inserted into a unit or deleted from it since mapping, its tokens pair with its rows by an alignment
on the number as shown (`_align`): an unchanged number keeps its row wherever it moved, an edited
one keeps the row of the number it replaced, and an inserted one has no row (UNSOURCEABLE).

`source_field` holds selectors ("a=<selector> ;; b=<selector>"), read by `quantities.resolve` in
the evidence map's directory (its docstring lists them). `expr` combines the variables (a, b, …; a regex match binds a, b, … in group order) into the
shown value: a scalar, or a (low, high) pair for a range. A single shown number checked against
a tuple must match every element (a figure said to hold at both ends). Rounding rules: dp
(within half a unit of the last digit shown; an exact half passes either way, since the source's
own rounding is unknown), int (to a whole number, for chart values the page prints as
whole numbers), n5 / n10 / n100 (nearest 5, 10, 100), sigN (N significant figures), via1 (to one decimal,
then to the decimals shown), alloc (within one unit of the last digit shown: a part the text says it printed by
controlled rounding, so that the printed parts add to the printed total), relNN (within NN% of the source; word
numbers), skip (not a quantity: listed in extracted_numbers.csv, not audited).

Options (for the positive control): --groups PATH reads another copy of groups.py; --out DIR
writes the outputs there instead of derived/.
"""

import argparse
import ast
import csv
import hashlib
import html
import importlib.util
import io
import json
import re
import subprocess
import sys
import tokenize
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MAP_PATH = HERE / "source_map.csv"
OVERVIEW = "infra/immigration-fiscal/overview_2026_09_28"
sys.path.insert(0, str(ROOT / OVERVIEW))
import quantities as Q  # noqa: E402

LADDER = Q.LADDER
INDEX = "research/immigration-INDEX.md"
FAQ = "research/immigration-objections-faq-2026-09-21.md"
CLAUDE = "CLAUDE.md"
REAL_COSTS = "research/immigration-real-fiscal-and-social-costs-2026-09-23.md"
BY_GENERATION = "research/immigration-adopted-account-by-generation-2026-09-25.md"
WINNERS = "research/immigration-winners-and-losers-2026-09-25.md"

# ---------------------------------------------------------------- number tokens

_N = r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?"
_PART = rf"[+\-−±~]?\$?(?:{_N})(?:bn|tn|k|M|m|pp|%|×)?"
NUM_RE = re.compile(
    rf"(?<![\w.$/])(?<![A-Za-z][-–])(?P<a>{_PART})"
    rf"(?:(?P<sep>\s?–\s?|-(?=\$?\d)|\s+to\s+)(?P<b>{_PART}))?"
    r"(?![\w.]*\d)(?!\w)"
)
_PARSE = re.compile(rf"^(?P<sign>[+\-−±~]?)\$?(?P<num>{_N})(?P<suf>bn|tn|k|M|m|pp|%|×)?$")

# Curated word numbers that carry a quantity (counts of sections and list items are left out).
WORDS = {"one resident in six": 1 / 6, "one other resident in six": 1 / 6, "about twice": 2,
         "About half": 0.5, "would double": 2, "Eight versions": 8, "Nine pooled": 9,
         "about a tenth": 0.1, "ten years": 10, "Two tests": 2, "top tenth": 0.1, "recent doubling": 2,
         "one in nine": 1 / 9, "one in four": 1 / 4, "one in six": 1 / 6, "one in seven": 1 / 7,
         "about a quarter": 0.25,
         "a quarter of the sound claims": 0.25, "costs what it costs: half": 0.5}
WORD_RE = re.compile(r"\b(?:" + "|".join(sorted(map(re.escape, WORDS), key=len, reverse=True)) + r")\b")

# Text that holds digits but no quantity: dates, ladder and item references, commit hashes.
MASKS = [
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),
    re.compile(r"\b(?:January|February|March|April|May|June|July|August|September|October|November|"
               r"December)\s+\d{1,2}(?:[–-]\d{1,2})?\b"),
    re.compile(r"^#+ \d+\.", re.M),
    re.compile(r"(?:\b(?:[Ll]adders?|[Ee]ntry|[Ee]ntries|[Ii]tems?|[Rr]ows?|Part|option|[Dd]ecision)|§) ?"
               r"\d+(?:[–-]\d+)?(?:(?:, | and | or |/| / )\d+(?:[–-]\d+)?)*\b"),
    re.compile(r"\((?:\d{2,3})(?:, \d{2,3})*\)"),
    re.compile(r"\b(?=[0-9a-f]*[a-f])(?=[0-9a-f]*\d)[0-9a-f]{7}\b"),
]


YEAR_RE = re.compile(r"(?:19|20)\d\d(?:\s?[–-]\s?(?:(?:19|20)\d\d|\d\d)|\s+to\s+(?:19|20)\d\d)?")


def mask(text):
    """Blank every masked span, keeping its line breaks so masked lines stay aligned with the text."""
    for m in MASKS:
        text = m.sub(lambda x: re.sub(r"[^\n]", " ", x.group(0)), text)
    return text


def parse_part(s):
    m = _PARSE.match(s)
    if not m:
        raise ValueError(f"unparsable number part {s!r}")
    v = Decimal(m.group("num").replace(",", ""))
    if m.group("sign") in ("-", "−"):
        v = -v
    return v, m.group("suf") or ""


def tokens(text, clean=None):
    """Number tokens in `text`: (start, end, raw, lo, hi, suffix, ordinal). A single number has lo == hi.
    `clean` is the text already masked (a line masked in its file's context), if any."""
    out, clean = [], mask(text) if clean is None else clean
    for k, m in enumerate(NUM_RE.finditer(clean)):
        a = parse_part(m.group("a"))
        b = parse_part(m.group("b")) if m.group("b") else a
        # "−$43–77bn" shares one sign and unit across the dash: both ends are negative
        if m.group("b") and a[0] < 0 and not a[1] and m.group("sep").strip() in ("–", "-") \
                and m.group("b")[0] not in "+-−±~":
            b = (-b[0], b[1])
        out.append((m.start(), m.end(), m.group(0), a[0], b[0], b[1] or a[1], str(k)))
    for k, m in enumerate(WORD_RE.finditer(clean)):
        v = Decimal(repr(WORDS[m.group(0)]))
        out.append((m.start(), m.end(), m.group(0), v, v, "word", f"w{k}"))
    return out


# ---------------------------------------------------------------- reader-facing texts

def _string_pieces(src):
    """Every string literal token in `src` by start position, plus the source lines."""
    out = {"__lines__": src.splitlines()}
    for t in tokenize.generate_tokens(io.StringIO(src).readline):
        if t.type == tokenize.STRING:
            out[t.start] = (t.end, ast.literal_eval(t.string))
    return out


def _pieces_in(node, pieces):
    """The literal pieces an (implicitly concatenated) string node is made of, with their lines.
    AST columns count UTF-8 bytes and tokenize columns count characters, so both are compared
    in characters."""
    lines = pieces["__lines__"]

    def chars(line, col):
        return len(lines[line - 1].encode()[:col].decode())

    lo = (node.lineno, chars(node.lineno, node.col_offset))
    hi = (node.end_lineno, chars(node.end_lineno, node.end_col_offset))
    got = [(start[0], val) for start, (end, val) in sorted((k, v) for k, v in pieces.items() if k != "__lines__")
           if lo <= start and end <= hi]
    if "".join(v for _, v in got) != node.value:
        raise SystemExit(f"[BLOCKED] string pieces at line {node.lineno} do not rebuild the literal")
    return got


def _kw(call):
    return {k.arg: k.value for k in call.keywords}


def groups_units(path):
    """(locator, pieces) for every claim, range, why, term and finding text in GROUPS."""
    src = path.read_text()
    pieces = _string_pieces(src)
    tree = ast.parse(src)
    groups = next(n.value for n in tree.body if isinstance(n, ast.Assign) and
                  any(isinstance(t, ast.Name) and t.id == "GROUPS" for t in n.targets))
    for g in groups.elts:
        kw = _kw(g)
        gid = kw["id"].value
        for field in ("claim", "range", "why"):
            if field in kw and isinstance(kw[field], ast.Constant) and kw[field].value:
                yield f"{gid}/{field}", _pieces_in(kw[field], pieces)
        for t in kw.get("terms", ast.List(elts=[])).elts:
            name, gloss = t.elts
            yield f"{gid}/term:{name.value}", _pieces_in(name, pieces) + [(gloss.lineno, ": ")] + \
                _pieces_in(gloss, pieces)
        for f in kw["findings"].elts:
            fk = _kw(f)
            ref0 = fk["refs"].elts[0].value
            for field in ("text", "why"):
                node = fk.get(field)
                if isinstance(node, ast.Constant) and node.value:
                    yield f"{gid}/f{ref0}/{field}", _pieces_in(node, pieces)


def _num_const(n):
    if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and not isinstance(n.value, bool):
        return n.value
    if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):
        v = _num_const(n.operand)
        return None if v is None else -v
    return None


def _num_list(n):
    if isinstance(n, ast.List) and n.elts:
        vals = [_num_const(e) for e in n.elts]
        if all(v is not None for v in vals):
            return vals
    return None


def build_units(path):
    """Hand-typed text and values in build.py that reach the page, as (locator, pieces, values): the
    ledger's category names, reader labels and notes (LEDGER), the rows of "Other ways to count"
    (the alt and beside rows of waterfall_rows) and the assumption rows (assumption_rows).
    RELABEL and the other waterfall rows only name staircase steps; the page shows LEDGER's text."""
    src = path.read_text()
    pieces = _string_pieces(src)
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "LEDGER" for t in node.targets):
            for cat in node.value.elts:
                name, items = cat.elts
                yield f"ledger/{name.value}", _pieces_in(name, pieces), None
                for item in items.elts:
                    step, label, note = item.elts
                    yield f"ledger/{step.value}/label", _pieces_in(label, pieces), None
                    if isinstance(note, ast.Constant) and note.value:
                        yield f"ledger/{step.value}/note", _pieces_in(note, pieces), None
        if isinstance(node, ast.FunctionDef) and node.name == "waterfall_rows":
            # a value list may be typed once and named ("alt = [290.5, 355.8]")
            named = {t.id: _num_list(a.value) for a in ast.walk(node) if isinstance(a, ast.Assign)
                     for t in a.targets if isinstance(t, ast.Name) and _num_list(a.value) is not None}
            for call in ast.walk(node):
                if not (isinstance(call, ast.Call) and getattr(call.func, "id", "") == "dict"):
                    continue
                kw = _kw(call)
                if not ("alt" in kw or "beside" in kw) or not isinstance(kw.get("label"), ast.Constant):
                    continue
                label = kw["label"].value
                yield f"alternatives/{label}/label", _pieces_in(kw["label"], pieces), None
                for field in ("value", "prev"):
                    n = kw.get(field)
                    vals = named.get(n.id) if isinstance(n, ast.Name) else _num_list(n)
                    if vals is not None:
                        yield f"alternatives/{label}/{field}", [(n.lineno, "")], vals
        if isinstance(node, ast.FunctionDef) and node.name == "assumption_rows":
            for tup in ast.walk(node):
                if isinstance(tup, ast.Tuple) and len(tup.elts) >= 4 and isinstance(tup.elts[0], ast.Name) \
                        and isinstance(tup.elts[1], ast.Constant) and isinstance(tup.elts[1].value, str):
                    label = tup.elts[1].value
                    yield f"assumptions/{label}/label", _pieces_in(tup.elts[1], pieces), None
                    vals = [_num_const(e) for e in tup.elts[2:4]]
                    if all(v is not None for v in vals):
                        yield f"assumptions/{label}/value", [(tup.elts[2].lineno, "")], vals


TAG = re.compile(r"<[^>]*>")
# the template's block placeholders ({{LEDGER}}, {{N_FINDINGS}}, …): whole generated tables and counts of entries
PLACEHOLDER = re.compile(r"\{\{[A-Z_]+\}\}")


def html_text(line):
    return re.sub(r"\s+", " ", html.unescape(TAG.sub(" ", line))).strip()


def html_lines(path, start_marker="<body>"):
    lines = path.read_text().splitlines()
    begin = next(i for i, l in enumerate(lines) if start_marker in l)
    for i in range(begin, len(lines)):
        text = html_text(PLACEHOLDER.sub(lambda m: " " * len(m.group(0)), lines[i]))
        if text:
            yield i + 1, text


def span_lines(path, spans):
    """(line, text) for a markdown file's in-scope spans. A span is (start anchor, end anchor): it
    runs from the start of the first to the end of the second, each unique in the file; text on
    the boundary lines outside the span is blanked, so its numbers are not read."""
    text = path.read_text()
    masked = mask(text)
    keep = [" " if c != "\n" else "\n" for c in text]
    for start, end in spans:
        for anchor in (start, end):
            if text.count(anchor) != 1:
                raise SystemExit(f"[BLOCKED] anchor {anchor!r} occurs {text.count(anchor)} times in {path.name}")
        a = text.index(start)
        b = text.index(end, a) + len(end)
        keep[a:b] = list(text[a:b])
    out = "".join(keep).split("\n")
    clean = "".join(m if k != " " else " " for m, k in zip(masked, keep)).split("\n")
    return [(i + 1, l, clean[i]) for i, l in enumerate(out) if l.strip()]


# Markdown spans in scope: current results only (coverage and reasons in RESULT.md).
INDEX_SPANS = [
    ("**Adopted main case (September 29): $371–435bn/year", "Treat an Astra accusation as a lead to verify"),
    ("**Earlier cases.** Each main case replaced the one before.", "too (−$51.0 / −$53.6bn)."),
    ("[By generation](immigration-adopted-account-by-generation-2026-09-25.md) (ladder 224,",
     "([scope memo](immigration-education-administration-scope-2026-09-20.md))."),
    ("[Real fiscal and social costs](immigration-real-fiscal-and-social-costs-2026-09-23.md) (ladder 188–193)",
     "[decision](../decisions/2026-09-28-social-items-more-benefits.md))."),
    ("Wages move **$66–166bn**", "charged nationally, the share ahead falls to 7.9%."),
    ("The [world ledger]", "premium over being raised in Mexico. [FRAMING-SENSITIVE]"),
    ("Benefits are priced to the same standard as the costs", "so both figures stand (ladder 199)."),
    ("The [debt legacy lane]", "nor the stock to an annual figure."),
    ("**Legacy comparisons, stated separately (September 30).**",
     "[decision](../decisions/2026-09-30-legacy-comparisons-separate.md); FRAMING-SENSITIVE]"),
    ("[Cumulative 2005–2024 back-cast]", "Not comparable with ladder 137's forward debt path."),
    # the rough Black comparison, restated on the adopted case (d6a5a2f)
    ("For comparison, a rough re-key of the main case to non-Hispanic Black residents costs",
     "group. This is not an engine run (ladder 259,"),
]
FAQ_SPANS = [
    ("Anchors: the [complete annual account]", "−$8k. [SOURCE: [CA–TX geography]"),
    ("- **Roads, parks and economic administration** take their long-run responses.",
     "−0.72 to 1.66, which cannot tell zero from one"),
    ("Steel-man: cheaper services, complementary labour and capital returns never appear in a",
     "The 1970–2000 college-share studies"),
    ("Finding: only income-year 2024 is a complete account.", "of other programmes before 2024 is unmeasured."),
    ("No. The account describes a resident stock in a stationary comparison.",
     "neither is cash that a removal would free in the year."),
    ("figures are not the $371–435bn complete account. [SOURCE:", "figures are not the $371–435bn complete account. [SOURCE:"),
    ("Two later corrections also nearly cancel:", "No combination changes the sign."),
    ("Steel-man: one year of a price surge, pandemic programmes and a migration wave", "which flatters the year."),
    # entry 5's split of the adopted account by generation (in scope since the v4 restatement, 5e9112e)
    ("On the adopted account itself, with no reference group", "on the US-born generations counted"),
    # entry 4's income split of the transfers (6157bb1) and entry 6's gap (1572b90), restated on the adopted case
    ("the renters' payments cancel in dollars but not by income",
     "fifths of other residents lose $79.4bn a year and the top fifth gains $44.5bn (ladder 194)."),
    ("many average residents, the main case's gap counting benefits when paid", "has no national total to share out."),
    ("**What about obligations left by past years?**",
     "[decision](../decisions/2026-09-30-legacy-comparisons-separate.md); FRAMING-SENSITIVE]"),
]
CLAUDE_SPANS = [
    ("Since\n  2026-09-23 the main case lets general public services", "business subsidies stay at **zero response by assumption**"),
]
# Memo passages restated on the adopted case (6157bb1, ebc15cc, 05312de). The real-costs memo's §4 bullets on
# housing, wages, crime and prices are left out: they did not move with the case.
MEMO_SPANS = {
    REAL_COSTS: [
        ("| Channel | Bottom fifth | 2nd | 3rd | 4th | Top fifth | Total |",
         "fifths lose $79.4bn a year and the top fifth gains $44.5bn."),
        ("**The fiscal cost's incidence is a financing convention.**", "and 19.0% and 0.64% under"),
        ("**Weighted by income.**", "weight (2.24), not a larger harm."),
    ],
    BY_GENERATION: [
        ("**Verdict (2026-09-29, the main case of that date):** On the main case of $371.4–434.8bn a year",
         "generation's own state mix are not computed."),
    ],
    WINNERS: [
        ("**Verdict (2026-09-29, the main case of that date, $371.4–434.8bn;",
         "whose pooled net under tax shares is −$524 a year."),
    ],
}
# Every markdown file in scope with its spans. A year in any of them needs no map row.
MARKDOWN = {INDEX: INDEX_SPANS, FAQ: FAQ_SPANS, CLAUDE: CLAUDE_SPANS, **MEMO_SPANS}


def check_sites(g, groups_path):
    """The build finds a groups.py site by quantities.groups_sites; this audit keys the same units by AST.
    Refuse when the two disagree on any locator or text."""
    spec = importlib.util.spec_from_file_location("_audited_groups", groups_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ours = {loc: "".join(v for _, v in pieces) for loc, pieces in g}
    theirs = Q.groups_sites(mod.GROUPS)
    if ours != theirs:
        diff = sorted(k for k in set(ours) | set(theirs) if ours.get(k) != theirs.get(k))
        raise SystemExit(f"[BLOCKED] groups.py units differ between the AST and quantities.groups_sites: {diff[:5]}")


def units(groups_path):
    """Every reader-facing text unit: (file, locator, pieces, values, masked text or None). Placeholders
    stay in the pieces; `extract` renders them."""
    g = list(groups_units(groups_path))
    check_sites(g, groups_path)
    for loc, pieces in g:
        yield f"{OVERVIEW}/groups.py", loc, pieces, None, None
    for loc, pieces, vals in build_units(ROOT / OVERVIEW / "build.py"):
        yield f"{OVERVIEW}/build.py", loc, pieces, vals, None
    tpl = ROOT / OVERVIEW / "template.html"
    for line, text in html_lines(tpl):
        yield f"{OVERVIEW}/template.html", f"L{line}", [(line, text)], None, None
    for rel, spans in MARKDOWN.items():
        if spans:
            for line, text, clean in span_lines(ROOT / rel, spans):
                yield rel, f"L{line}", [(line, text)], None, clean


def _quote(text, s, e):
    a = text.rfind(". ", 0, s)
    a = a + 2 if a >= 0 else 0
    b = text.find(". ", e)
    q = re.sub(r"\s+", " ", text[a:(b + 1 if b >= 0 else len(text))]).strip()
    if len(q) > 120:
        q = re.sub(r"\s+", " ", text[max(0, s - 55):e + 55]).strip()
    return q[:120]


def render_pieces(pieces):
    """The pieces with their placeholders rendered, and each rendering's (start, end, id, view) in the joined
    text. A placeholder split across two string pieces is refused."""
    out, spans, pos = [], [], 0
    for line, v in pieces:
        if v.count("{{q:") != len(Q.PLACEHOLDER.findall(v)):
            raise SystemExit(f"[BLOCKED] a placeholder at line {line} is split or malformed: {v[:80]!r}")
        r, sp = Q.fill(v)
        spans += [(pos + a, pos + b, rid, view) for a, b, rid, view in sp]
        out.append((line, r))
        pos += len(r)
    return out, spans


def bind_tokens(found, spans, text, where):
    """Map each token inside a rendered placeholder to (id, view, one-number view, sentence); others to None.
    A rendering must hold one token per number its view prints."""
    bound, inside = [None] * len(found), {i: [] for i in range(len(spans))}
    for j, (s, e, *_rest) in enumerate(found):
        hit = [i for i, (a, b, _r, _v) in enumerate(spans) if s < b and a < e]
        if not hit:
            continue
        a, b = spans[hit[0]][:2]
        # the text around a placeholder may add a sign before it or a unit after it ("{{q:…|range}}%")
        if len(hit) > 1 or not re.fullmatch(r"[+\-−±~$]?", text[s:a] if s < a else "") \
                or not re.fullmatch(r"(?:bn|tn|k|M|m|pp|%|×)?", text[b:e] if e > b else ""):
            raise SystemExit(f"[BLOCKED] {where}: token {text[s:e]!r} straddles a rendered placeholder")
        inside[hit[0]].append(j)
    for i, js in inside.items():
        a, b, rid, view = spans[i]
        subs = Q.subviews(view)
        if len(js) != len(subs):
            raise SystemExit(f"[BLOCKED] {where}: {{{{q:{rid}|{view}}}}} renders {text[a:b]!r}, "
                             f"{len(js)} tokens for {len(subs)} numbers")
        for j, sub in zip(js, subs):
            bound[j] = (rid, view, sub, Q.sentence(text, a, b))
    return bound


def extract(groups_path):
    """Every number token as a dict: file, line, locator, ordinal, raw, lo, hi, unit, text, line_text, and
    `bound` (id, view, one-number view, sentence) when a placeholder rendered it."""
    out = []
    for file, loc, pieces, vals, clean in units(groups_path):
        text = "".join(v for _, v in pieces)
        if vals is not None:
            for k, v in enumerate(vals):
                d = Decimal(repr(v))
                out.append(dict(file=file, line=pieces[0][0], locator=loc, ordinal=str(k), raw=repr(v), lo=d, hi=d,
                                unit="$bn", text=f"{loc.split('/')[1]} = {vals}"[:120], line_text=text, bound=None))
            continue
        pieces, spans = render_pieces(pieces)
        text = "".join(v for _, v in pieces)
        starts, pos = [], 0
        for line, v in pieces:
            starts.append((pos, line))
            pos += len(v)
        found = tokens(text, clean)
        bound = bind_tokens(found, spans, text, f"{file} {loc}")
        for (s, e, raw, lo, hi, suf, k), b in zip(found, bound):
            line = max(l for p, l in starts if p <= s)
            unit = "word" if suf == "word" else ("$" if "$" in raw else "") + suf
            out.append(dict(file=file, line=line, locator=loc, ordinal=k, raw=raw.strip(), lo=lo, hi=hi,
                            unit=unit, text=_quote(text, s, e), line_text=text, bound=b))
    return out


# ---------------------------------------------------------------- sources
# The selectors and their resolver live in the evidence map's quantities.py, which the build uses too.

resolve = Q.resolve


def _fmt(v):
    if isinstance(v, tuple):
        return " / ".join(_fmt(x) for x in v)
    return f"{v:.6g}" if abs(v) < 1e6 else f"{v:.0f}"


# ---------------------------------------------------------------- rounding and status

def _dec(x):
    return Decimal(repr(float(x)))


def rounds_to(value, shown, rule):
    """Whether source `value` displays as `shown` under `rule`."""
    v, d = _dec(value), shown
    places = max(0, -d.as_tuple().exponent)
    q = Decimal(1).scaleb(-places)
    if rule == "dp":
        # within half a unit of the last digit shown; an exact half may be shown either way
        return abs(v - d) <= q / 2
    if rule == "via1":
        return v.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP).quantize(q, rounding=ROUND_HALF_UP) == d
    if rule == "alloc":
        # controlled rounding moves a part by less than one unit of its last digit ("$2.27bn shows as $2.2bn")
        return abs(v - d) < q
    if rule == "int":
        # a hand-typed chart value the page prints as a whole number ("368.0" shows as 368)
        return v.quantize(Decimal(1), rounding=ROUND_HALF_UP) == d.quantize(Decimal(1), rounding=ROUND_HALF_UP)
    if re.fullmatch(r"n\d+", rule):
        step = Decimal(rule[1:])
        return (v / step).quantize(Decimal(1), rounding=ROUND_HALF_UP) * step == d
    if re.fullmatch(r"sig\d", rule):
        n = int(rule[3:])
        if v == 0:
            return d == 0
        exp = v.copy_abs().adjusted() - n + 1
        step = Decimal(1).scaleb(exp)
        return (v / step).quantize(Decimal(1), rounding=ROUND_HALF_UP) * step == d
    if rule.startswith("rel"):
        return abs(v - d) <= abs(v) * Decimal(rule[3:]) / 100
    raise SystemExit(f"[BLOCKED] unknown rounding rule {rule!r}")


def matches(value, tok, rule):
    """A range (lo–hi) matches a (low, high) source pair end by end. A single number matches a
    scalar source, or every element of a tuple source (a figure said to hold at both ends)."""
    vals = value if isinstance(value, tuple) else (value,)
    if tok["lo"] == tok["hi"]:
        return all(rounds_to(v, tok["lo"], rule) for v in vals)
    if len(vals) != 2:
        return False
    return all(rounds_to(v, d, rule) for v, d in zip(vals, (tok["lo"], tok["hi"])))


def load_map():
    rows = list(csv.DictReader(MAP_PATH.open()))
    keys = {}
    for r in rows:
        k = (r["file"], r["locator"], r["ordinal"])
        if k in keys:
            raise SystemExit(f"[BLOCKED] source_map.csv has two rows for {k}")
        keys[k] = r
    return keys


anchored = Q.anchored


def map_key(tok, anchors):
    """The map key of a token: the structural locator, or the anchor string whose line holds it."""
    if tok["file"].endswith(("groups.py", "build.py")):
        return (tok["file"], tok["locator"], tok["ordinal"])
    hits = [a for a in anchors.get(tok["file"], []) if anchored(a, tok["line_text"])]
    if len(hits) > 1:
        hits = [max(hits, key=len)]
    return (tok["file"], hits[0] if hits else tok["locator"], tok["ordinal"])


def map_anchors(cmap):
    anchors = {}
    for f, loc, _ in cmap:
        if not f.endswith(("groups.py", "build.py")):
            anchors.setdefault(f, set()).add(loc)
    return anchors


_YEAR = "<year>"


def _align(a, b):
    """Pairs (i, j) aligning the numbers a unit held when mapped (`a`) with the numbers it holds now (`b`).
    An equal number scores 2 and an edited one 1, so a number inserted or deleted since mapping does not
    shift its neighbours onto each other's rows. A year pairs only with a year. Ties keep the positional
    pairing."""
    def score(x, y):
        if x == y:
            return 2
        return None if (x == _YEAR) != (y == _YEAR) else 1
    n, m = len(a), len(b)
    best = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s = score(a[i - 1], b[j - 1])
            best[i][j] = max(best[i - 1][j], best[i][j - 1], best[i - 1][j - 1] + s if s is not None else -1)
    pairs, i, j = [], n, m
    while i and j:
        s = score(a[i - 1], b[j - 1])
        if s is not None and best[i][j] == best[i - 1][j - 1] + s:
            pairs.append((i - 1, j - 1))
            i, j = i - 1, j - 1
        elif best[i][j] == best[i - 1][j]:
            i -= 1
        else:
            j -= 1
    return pairs[::-1]


def pair_tokens(toks, cmap, anchors):
    """Each token's map key (None when it has no row) and a note when its number moved within its unit
    since mapping. A unit is one structural locator or one anchored line, and one kind of token (digits,
    words). A markdown file's unmapped years fill the gaps between its rows' positions."""
    keys = [map_key(t, anchors) for t in toks]
    rows, units = {}, {}
    for f, loc, o in cmap:
        rows.setdefault((f, loc, o.startswith("w")), set()).add(o)
    for j, (f, loc, o) in enumerate(keys):
        units.setdefault((f, loc, o.startswith("w")), []).append(j)
    out = [(k if k in cmap else None, "") for k in keys]
    for (f, loc, word), idx in units.items():
        have = rows.get((f, loc, word))
        if not have:
            continue
        pre = "w" if word else ""
        markdown = f in MARKDOWN

        def norm(raw):
            return _YEAR if markdown and YEAR_RE.fullmatch(raw) else raw
        n = max(int(o[len(pre):]) for o in have) + 1
        a = [norm(cmap[(f, loc, f"{pre}{i}")]["shown"]) if f"{pre}{i}" in have else _YEAR for i in range(n)]
        b = [norm(toks[j]["raw"]) for j in idx]
        if a == b:
            continue
        for j in idx:
            out[j] = (None, "")
        for i, jj in _align(a, b):
            o = f"{pre}{i}"
            if o in have:
                t = toks[idx[jj]]
                moved = "" if o == t["ordinal"] else f"moved within its unit since mapping (token {o}, now {t['ordinal']})"
                out[idx[jj]] = ((f, loc, o), moved)
    return out


def current_ordinals(groups_path):
    """Map key → the position its number holds now, for every row whose number moved within its unit."""
    toks, cmap = [t for t in extract(groups_path) if not t["bound"]], load_map()
    return {k: t["ordinal"] for t, (k, moved) in zip(toks, pair_tokens(toks, cmap, map_anchors(cmap))) if moved}


def audit(groups_path):
    toks = extract(groups_path)
    cmap = load_map()
    anchors = map_anchors(cmap)
    # an anchor must pick out exactly one scanned line of its file
    scanned = {}
    for t in toks:
        scanned.setdefault(t["file"], {})[t["line"]] = t["line_text"]
    bad = []  # every broken anchor at once, in a fixed order
    for f, locs in sorted(anchors.items()):
        for a in sorted(locs):
            n = sum(anchored(a, l) for l in scanned.get(f, {}).values())
            if n != 1:
                bad.append(f"anchor {a!r} picks {n} scanned lines of {f}")
    if bad:
        raise SystemExit(f"[BLOCKED] {len(bad)} anchor(s): " + "; ".join(bad))
    seen, audited, extracted = set(), [], []
    free = [t for t in toks if not t["bound"]]
    paired = {id(t): p for t, p in zip(free, pair_tokens(free, cmap, anchors))}
    recs = Q.load_registry()
    for t in toks:
        if t["bound"]:
            row, ext = bound_row(t, recs)
            audited.append(row)
            extracted.append(ext)
            continue
        key, moved = paired[id(t)]
        r = cmap.get(key) if key else None
        if key:
            seen.add(key)
        else:
            key = map_key(t, anchors)
        rule = r["rounding_rule"] if r else ""
        year = not r and t["file"] in MARKDOWN and YEAR_RE.fullmatch(t["raw"])
        extracted.append([t["file"], t["line"], key[1], key[2], t["raw"], t["unit"], t["text"],
                          "mapped" if r else ("year in a markdown file, not audited" if year else "UNMAPPED"), rule])
        if (r and rule == "skip") or year:
            continue
        row = dict(file=t["file"], line=t["line"], quoted_text=t["text"], number_as_shown=t["raw"],
                   unit=t["unit"], source_path="", source_field_or_line="", source_value="",
                   rounding_rule=rule, status="", note="")
        if not r:
            row.update(status="UNSOURCEABLE", note="no source_map.csv row for this token")
        elif not r["source_path"]:
            row.update(status="UNSOURCEABLE", note=r["note"])
        else:
            v = resolve(r["source_path"], r["source_field"], r["expr"])
            src = r["source_field"] + (f" ;; expr {r['expr']}" if r["expr"] else "")
            row.update(source_path=r["source_path"], source_field_or_line=src, source_value=_fmt(v))
            notes = [r["note"]] if r["note"] else []
            # a prose source (the ladder, a RESULT or memo) stands in for a missing machine-readable file
            if r["source_path"].endswith(".md") and "-sourced" not in r["note"]:
                notes.append("ladder-sourced" if r["source_path"] == LADDER else "text-sourced")
            if r["shown"] and r["shown"] != t["raw"]:
                notes.append(f"shown changed since mapping (was {r['shown']})")
            if moved:
                notes.append(moved)
            if matches(v, t, rule):
                row["status"] = "CONTEXT-SHIFT" if r["context"] else "MATCH"
                if r["context"]:
                    notes.insert(0, r["context"])
            else:
                stale = None
                if r["stale_field"]:
                    stale = resolve(r["stale_path"] or r["source_path"], r["stale_field"], r["stale_expr"])
                if stale is not None and matches(stale, t, rule):
                    row["status"] = "STALE"
                    notes.insert(0, f"equals {r['stale_label']}: {_fmt(stale)}")
                else:
                    row["status"] = "MISMATCH"
                    notes.insert(0, f"shown {t['raw']}, source {_fmt(v)}")
            row["note"] = "; ".join(notes)
        audited.append(row)
    unused = sorted(set(cmap) - seen)
    return audited, extracted, unused


def bound_row(t, recs):
    """The audit row of a number a placeholder rendered: its record's value and the record's lint."""
    rid, view, sub, sent = t["bound"]
    rec = recs[rid]
    target, rule = Q.view_value(rec, Q.record_value(rid, recs), sub), Q.rule_for(rec, sub)
    errs = Q.lint(sent, rec)
    notes = [f"bound to {{{{q:{rid}|{view}}}}}"]
    if Q.is_approximate(rec):
        notes.append(f"approximate ({rec['status']}): the page marks it")
    if not matches(target, t, rule):
        status = "MISMATCH"
        notes.insert(0, f"rendered {t['raw']}, record {_fmt(target)}")
    elif errs:
        status = "CONTEXT-SHIFT"
        notes.insert(0, f"the sentence {'; '.join(errs)}")
    else:
        status = "MATCH"
    row = dict(file=t["file"], line=t["line"], quoted_text=t["text"], number_as_shown=t["raw"], unit=t["unit"],
               source_path=rec["source_path"], source_field_or_line=f"q:{rid}|{sub}", source_value=_fmt(target),
               rounding_rule=rule, status=status, note="; ".join(notes))
    ext = [t["file"], t["line"], t["locator"], t["ordinal"], t["raw"], t["unit"], t["text"], f"bound: q:{rid}|{sub}",
           rule]
    return row, ext


def file_hashes(groups_path):
    files = {f"{OVERVIEW}/groups.py": groups_path, f"{OVERVIEW}/build.py": ROOT / OVERVIEW / "build.py",
             f"{OVERVIEW}/template.html": ROOT / OVERVIEW / "template.html",
             f"{OVERVIEW}/quantity_registry.csv": Q.REGISTRY,
             **{rel: ROOT / rel for rel in MARKDOWN}, LADDER: ROOT / LADDER,
             "source_map.csv": MAP_PATH}
    rows = list(csv.DictReader(MAP_PATH.open())) + [
        dict(source_path=r["source_path"], source_field=r["field"]) for r in Q.load_registry().values()]
    for p in sorted({r["source_path"] for r in rows if r["source_path"]} |
                    {m for r in rows for m in re.findall(r"@([^@]+)@", r["source_field"])}):
        files[p] = ROOT / p
    return {k: hashlib.sha256(Path(v).read_bytes()).hexdigest() for k, v in sorted(files.items())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--groups", type=Path, default=ROOT / OVERVIEW / "groups.py")
    ap.add_argument("--out", type=Path, default=HERE / "derived")
    args = ap.parse_args()
    audited, extracted, unused = audit(args.groups.resolve())
    args.out.mkdir(parents=True, exist_ok=True)
    cols = ["file", "line", "quoted_text", "number_as_shown", "unit", "source_path", "source_field_or_line",
            "source_value", "rounding_rule", "status", "note"]
    with (args.out / "number_audit.csv").open("w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(cols)
        for r in audited:
            w.writerow([r[c] for c in cols])
    with (args.out / "extracted_numbers.csv").open("w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["file", "line", "locator", "ordinal", "raw", "unit", "quoted_text", "map", "rounding_rule"])
        w.writerows(extracted)
    head = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    (args.out / "inputs.json").write_text(json.dumps(dict(head=head, sha256=file_hashes(args.groups.resolve())),
                                                     indent=1) + "\n")
    counts = {}
    for r in audited:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print(f"audited {len(audited)} numbers ({len(extracted)} tokens): " +
          ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    if unused:
        print(f"! {len(unused)} map rows match no token (text moved or changed): " +
              "; ".join("|".join(k) for k in unused[:8]))


if __name__ == "__main__":
    main()
