"""Numbers on the evidence map and the files they come from.

One module for the build and for the number audit (`infra/immigration-fiscal/number_drift_audit_2026_09_29/`),
so that both read, round and check a quantity the same way.

`quantity_registry.csv` holds one record per quantity:
    id              stable key, never reused; a page names this, not a file
    label           what the number is, in plain words
    source_path     the file the selectors read (repository-relative)
    field           selectors, ";;"-separated (below); "x=q:<id>" reuses another record's value
    expr            combines the bound names (Python with SAFE_BUILTINS only)
    unit            $bn, $tn, $k, $, %, x (a ratio or count), year, M
    shape           scalar; ends (low end, high end); interval (min, max); central_interval (central, min, max)
    mid_round, ends_round
                    display rounding of the central and of the ends: decimals "0"–"2", or a step "n5", "n10", "n100"
    case, period, population, comparison, treatment
                    what the number measures
    status          file (machine fields only), file+text (plus a constant stated only in prose), text,
                    inference (combined here under a stated assumption), needs_file (no file measures it in the
                    page's frame, so the value is interim). The page marks inference and needs_file values
                    approximate.
    must_name, forbid
                    regular expressions, matched case-insensitively, that the sentence quoting the record must
                    match, or must not match
    supersedes, note
    reader_note     for an approximate record (inference, needs_file), what the page's tooltip tells the reader;
                    it may quote other records through placeholders

A page quotes a record with a placeholder, `{{q:<id>|<view>}}`. Views: mid, value, min, max, at_low_end,
at_high_end (one number); range ("49–62"), range_unit ("$49–62bn"), mid_range ("$55bn (49–62)"), pair
("$77.3 / $73.6bn", in end order). The central of an `ends` record is the midpoint of the unrounded ends,
and rounding happens once, when the view is rendered.

`quantity_bindings.csv` names the sites on the page that must quote a record: (file, locator, id, view). A text
site (a groups.py field, a template line found by an anchor, a ledger note) must hold the placeholder
(`binding_errors`); the build lints every sentence that quotes a record, bound or not (`lint_unit`). A row of the build's tables must carry the
record's values, and its label must pass the lint (`value_binding_errors`). The build refuses on any failure.

Selectors:
    json:<key.path[0]>            a value in a JSON file; a glob key ("ent_*") returns every match
    csv:<col=v&col=v>|<column>    one cell of the single CSV row matching every filter
    csvcol:<column>               a whole CSV column, in file order (for sums over years)
    re:<regex>                    capture groups of the first match in the file's text
    re:L<n>:<regex>               the same, inside confidence-ladder entry n only
    num:<value>                   a literal (for a count the text states, e.g. 1/6)
A selector may start with "@<path>@" to read another file than `source_path`. "a,b=<selector>" names its
values; a bare selector binds them to a, b, … in order.
"""

import csv
import fnmatch
import html
import io
import json
import math
import re
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REGISTRY = HERE / "quantity_registry.csv"
BINDINGS = HERE / "quantity_bindings.csv"
LADDER = "research/immigration-confidence-ladder.md"

# ---------------------------------------------------------------- sources

_cache = {}


def _read(path):
    if path not in _cache:
        p = ROOT / path
        if not p.exists():
            raise SystemExit(f"[BLOCKED] source {path} does not exist")
        _cache[path] = p.read_text()
    return _cache[path]


def ladder_entry(n):
    key = ("ladder", n)
    if key not in _cache:
        lines = _read(LADDER).splitlines()
        old = next(i for i, l in enumerate(lines) if l.startswith("# Immigration confidence ladder") and "current" not in l)
        hits = [l for l in lines[:old] if l.startswith(f"{n}. ")]
        if len(hits) != 1:
            raise SystemExit(f"[BLOCKED] ladder entry {n} found {len(hits)} times")
        _cache[key] = hits[0]
    return _cache[key]


WORD_VALUES = {"half": 0.5, "tenth": 0.1, "quarter": 0.25, "two": 2, "eight": 8, "nine": 9}


def _num(s):
    s = s.strip().replace("−", "-").replace(",", "").replace("$", "")
    if s.lower() in WORD_VALUES:
        return float(WORD_VALUES[s.lower()])
    return float(re.sub(r"(bn|tn|k|M|m|%|×)$", "", s))


def select(path, selector):
    """Values (a list of floats) that one selector reads."""
    if selector.startswith("@"):
        path, selector = selector[1:].split("@", 1)
    kind, _, arg = selector.partition(":")
    if kind == "json":
        # a key may be a glob ("by_component.ent_*.stock_charged_bn"); a glob returns every match
        vals, glob = [json.loads(_read(path))], False
        for part in re.findall(r"[^.\[\]]+|\[\d+\]", arg):
            if part.startswith("["):
                vals = [v[int(part[1:-1])] for v in vals]
            elif any(c in part for c in "*?["):
                glob = True
                vals = [v[k] for v in vals for k in sorted(v) if fnmatch.fnmatchcase(k, part)]
            else:
                vals = [v[part] for v in vals]
        if glob:
            return [float(x) for x in vals]
        v = vals[0]
        return [float(x) for x in v] if isinstance(v, list) else [float(v)]
    if kind == "csv":
        filt, _, col = arg.rpartition("|")
        conds = [c.split("=", 1) for c in filt.split("&")] if filt else []
        rows = [r for r in csv.DictReader(io.StringIO(_read(path)))
                if all(r.get(k) == v for k, v in conds)]
        if len(rows) != 1:
            raise SystemExit(f"[BLOCKED] {path} {filt!r} matches {len(rows)} rows")
        return [float(rows[0][col])]
    if kind == "csvcol":
        return [float(r[arg]) for r in csv.DictReader(io.StringIO(_read(path)))]
    if kind == "re":
        m = re.match(r"L(\d+):(.*)", arg, re.S)
        text, rx = (ladder_entry(int(m.group(1))), m.group(2)) if m else (_read(path), arg)
        hit = re.search(rx, text)
        if not hit:
            raise SystemExit(f"[BLOCKED] {selector!r} finds nothing in {path}")
        return [_num(g) for g in hit.groups()]
    if kind == "num":
        return [float(eval(arg, {"__builtins__": {}}, {}))]
    raise SystemExit(f"[BLOCKED] unknown selector {selector!r}")


_BIND = re.compile(r"\s*([A-Za-z_]\w*(?:\s*,\s*[A-Za-z_]\w*)*)\s*=\s*(?=@|json:|csv:|csvcol:|re:|num:)")
# the only functions an `expr` may call
SAFE_BUILTINS = {"abs": abs, "min": min, "max": max, "sum": sum, "round": round, "len": len, "zip": zip,
                 "range": range, "exp": math.exp}


def resolve(path, field, expr):
    """One value, or a tuple, from `field`'s selectors combined by `expr` (the audit's source-map rows)."""
    env = {}
    for part in [p.strip() for p in field.split(";;") if p.strip()]:
        bind = _BIND.match(part)
        vals = select(path, part[bind.end():] if bind else part)
        names = [n.strip() for n in bind.group(1).split(",")] if bind else [chr(97 + i) for i in range(len(vals))]
        if len(names) == 1 and len(vals) > 1:
            env[names[0]] = vals
        else:
            if len(names) != len(vals):
                raise SystemExit(f"[BLOCKED] {part!r} yields {len(vals)} values for {len(names)} names")
            env.update(zip(names, vals))
    if not expr:
        if len(env) != 1:
            raise SystemExit(f"[BLOCKED] {field!r} binds {sorted(env)} and has no expr to combine them")
        v = next(iter(env.values()))
    else:
        # the variables go in the globals, so a generator expression in `expr` can see them
        v = eval(expr, {"__builtins__": SAFE_BUILTINS, **env})
    if isinstance(v, list):
        v = tuple(v)
    return v


# ---------------------------------------------------------------- records

SHAPES = {"scalar": 1, "ends": 2, "interval": 2, "central_interval": 3}
# prefix and suffix of a rendered number
UNITS = {"$bn": ("$", "bn"), "$tn": ("$", "tn"), "$k": ("$", "k"), "$": ("$", ""), "%": ("", "%"),
         "x": ("", ""), "year": ("", ""), "M": ("", "M")}
STATUSES = ("file", "file+text", "text", "inference", "needs_file")
# the page marks these approximate, with the record's reader_note as the reason
APPROXIMATE = ("inference", "needs_file")
_Q = re.compile(r"\s*([A-Za-z_]\w*(?:\s*,\s*[A-Za-z_]\w*)*)\s*=\s*q:([\w.]+)\s*$")
_RECS = {}
_VALUES = {}


def load_registry(path=None):
    path = Path(path or REGISTRY)
    if path not in _RECS:
        recs = {}
        for r in csv.DictReader(path.open()):
            if r["id"] in recs:
                raise SystemExit(f"[BLOCKED] {path.name} has two records {r['id']!r}")
            if r["shape"] not in SHAPES or r["unit"] not in UNITS or r["status"] not in STATUSES:
                raise SystemExit(f"[BLOCKED] {r['id']}: unknown shape {r['shape']!r}, unit {r['unit']!r} "
                                 f"or status {r['status']!r}")
            recs[r["id"]] = r
        _RECS[path] = recs
    return _RECS[path]


def record_value(rid, recs=None, _open=()):
    """A record's value: a number, or a tuple in the order its shape names ((low end, high end);
    (min, max); (central, min, max))."""
    recs = recs if recs is not None else load_registry()
    done = _VALUES.setdefault(id(recs), {})
    if rid in done:
        return done[rid]
    if rid not in recs:
        raise SystemExit(f"[BLOCKED] no record {rid!r}")
    if rid in _open:
        raise SystemExit(f"[BLOCKED] records refer to each other in a cycle: {' → '.join(_open + (rid,))}")
    rec, env = recs[rid], {}
    for part in (p.strip() for p in rec["field"].split(";;") if p.strip()):
        q = _Q.match(part)
        if q:
            v = record_value(q.group(2), recs, _open + (rid,))
            vals, names = (list(v) if isinstance(v, tuple) else [v]), q.group(1)
        else:
            bind = _BIND.match(part)
            vals = select(rec["source_path"], part[bind.end():] if bind else part)
            names = bind.group(1) if bind else None
        names = [n.strip() for n in names.split(",")] if names else [chr(97 + i) for i in range(len(vals))]
        if len(names) == 1 and len(vals) > 1:
            env[names[0]] = vals
        elif len(names) == len(vals):
            env.update(zip(names, vals))
        else:
            raise SystemExit(f"[BLOCKED] {rid}: {part!r} yields {len(vals)} values for {len(names)} names")
    if rec["expr"]:
        v = eval(rec["expr"], {"__builtins__": SAFE_BUILTINS, **env})
    elif len(env) == 1:
        v = next(iter(env.values()))
    else:
        raise SystemExit(f"[BLOCKED] {rid} binds {sorted(env)} and has no expr to combine them")
    v = tuple(float(x) for x in v) if isinstance(v, (list, tuple)) else float(v)
    if (len(v) if isinstance(v, tuple) else 1) != SHAPES[rec["shape"]]:
        raise SystemExit(f"[BLOCKED] {rid} resolves to {v}, not the {rec['shape']} its shape names")
    done[rid] = v
    return v


def parts(v, shape):
    if shape == "scalar":
        return dict(mid=v, value=v, min=v, max=v)
    if shape == "central_interval":
        c, lo, hi = v
        return dict(mid=c, value=c, min=lo, max=hi)
    a, b = v
    return dict(mid=(a + b) / 2, min=min(a, b), max=max(a, b), at_low_end=a, at_high_end=b)


# ---------------------------------------------------------------- rendering

VIEWS = ("mid", "value", "min", "max", "at_low_end", "at_high_end", "range", "range_unit", "mid_range", "pair")


def _step(rnd):
    return re.fullmatch(r"n\d+", rnd) is not None


def _digits(x, rnd, unit):
    """(sign, digits) of x rounded by `rnd`: decimals ("0", "1", "2") or a step ("n5", "n10", "n100")."""
    d = Decimal(repr(float(x)))
    if _step(rnd):
        step = Decimal(rnd[1:])
        v, places = (d / step).quantize(Decimal(1), rounding=ROUND_HALF_UP) * step, 0
    else:
        places = int(rnd)
        v = d.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)
    body = f"{abs(v):.{places}f}" if unit == "year" else f"{abs(v):,.{places}f}"
    return ("−" if v < 0 else ""), body


def _one(x, rnd, unit):
    sign, body = _digits(x, rnd, unit)
    pre, suf = UNITS[unit]
    return f"{sign}{pre}{body}{suf}"


def render(rec, v, view):
    """A record's value as the page prints it."""
    p, unit, mr, er = parts(v, rec["shape"]), rec["unit"], rec["mid_round"], rec["ends_round"]
    if view in ("mid", "value"):
        return _one(p["mid"], mr, unit)
    if view in ("min", "max", "at_low_end", "at_high_end"):
        if view not in p:
            raise SystemExit(f"[BLOCKED] view {view!r} does not apply to {rec['id']}'s shape {rec['shape']!r}")
        return _one(p[view], er, unit)
    if view == "mid_range":
        return f"{render(rec, v, 'mid')} ({render(rec, v, 'range')})"
    if view == "pair":
        if "at_low_end" not in p:
            raise SystemExit(f"[BLOCKED] view 'pair' does not apply to {rec['id']}'s shape {rec['shape']!r}")
        pre, suf = UNITS[unit]
        (s1, b1), (s2, b2) = _digits(p["at_low_end"], er, unit), _digits(p["at_high_end"], er, unit)
        return f"{s1}{pre}{b1} / {s2}{pre}{b2}{suf}"
    if view in ("range", "range_unit"):
        lo, hi = p["min"], p["max"]
        (s1, b1), (s2, b2) = _digits(lo, er, unit), _digits(hi, er, unit)
        pre, suf = UNITS[unit] if view == "range_unit" else ("", "")
        if s1 and not s2:
            # a range across zero: "−58 to +74" (a dash would give both ends the minus sign)
            return f"{s1}{pre}{b1}{suf} to +{pre}{b2}{suf}"
        if s1:
            # both below zero: one sign, magnitudes ascending ("−$3.1–3.2bn"), as the pages write them
            return f"−{pre}{b2}–{b1}{suf}"
        return f"{pre}{b1}–{b2}{suf}"
    raise SystemExit(f"[BLOCKED] unknown view {view!r}")


def subviews(view):
    """The one-number or range view of each number a view prints, in order."""
    return {"mid_range": ["mid", "range"], "pair": ["at_low_end", "at_high_end"]}.get(view, [view])


def view_value(rec, v, view):
    """What a printed number is compared with: one number, or (min, max) for a range view."""
    p = parts(v, rec["shape"])
    if view in ("range", "range_unit"):
        # in the order the range is written: magnitudes ascending when both ends are below zero
        return (p["max"], p["min"]) if p["max"] < 0 else (p["min"], p["max"])
    if view not in p:
        raise SystemExit(f"[BLOCKED] view {view!r} does not apply to shape {rec['shape']!r}")
    return p[view]


def rule_for(rec, view, override=""):
    """The rounding rule a printed number of this view is checked with."""
    if override:
        return override
    rnd = rec["mid_round"] if view in ("mid", "value") else rec["ends_round"]
    return rnd if _step(rnd) else "dp"


def is_approximate(rec):
    return rec["status"] in APPROXIMATE


# ---------------------------------------------------------------- placeholders and lint

PLACEHOLDER = re.compile(r"\{\{q:([A-Za-z0-9_.]+)\|([a-z_]+)\}\}")


def fill(text, markup=False, recs=None):
    """`text` with every {{q:<id>|<view>}} rendered, and the (start, end, id, view) span of each rendering
    in the returned text. With `markup` (HTML), an approximate record's rendering is wrapped in a span
    that the page styles and explains; the spans are then not returned."""
    recs = recs if recs is not None else load_registry()
    out, spans, pos = [], [], 0
    for m in PLACEHOLDER.finditer(text):
        rid, view = m.groups()
        if rid not in recs:
            raise SystemExit(f"[BLOCKED] placeholder {m.group(0)} names no record")
        if view not in VIEWS:
            raise SystemExit(f"[BLOCKED] placeholder {m.group(0)} names no view")
        rec = recs[rid]
        s = render(rec, record_value(rid, recs), view)
        if markup and is_approximate(rec):
            if not rec["reader_note"]:
                raise SystemExit(f"[BLOCKED] the page quotes {rid}, which is approximate ({rec['status']}) and has "
                                 f"no reader_note to say why")
            note, _ = fill(rec["reader_note"], recs=recs)
            s = f'<span class="approx" title="Approximate. {html.escape(note)}">{s}</span>'
        out.append(text[pos:m.start()])
        start = sum(len(x) for x in out)
        out.append(s)
        spans.append((start, start + len(s), rid, view))
        pos = m.end()
    out.append(text[pos:])
    return "".join(out), ([] if markup else spans)


def sentence(text, s, e):
    """The sentence of `text` holding [s, e)."""
    a = max(text.rfind(". ", 0, s), text.rfind("\n", 0, s))
    b = [i for i in (text.find(". ", e), text.find("\n", e)) if i >= 0]
    return re.sub(r"\s+", " ", text[a + 1 if a >= 0 else 0:(min(b) + 1 if b else len(text))]).strip()


def lint(text, rec):
    errs = []
    if rec["must_name"] and not re.search(rec["must_name"], text, re.I):
        errs.append(f"names none of /{rec['must_name']}/")
    if rec["forbid"] and re.search(rec["forbid"], text, re.I):
        errs.append(f"says /{rec['forbid']}/")
    return errs


def lint_unit(text, recs=None):
    """Lint every placeholder in one text unit against its record: [(id, view, sentence, errors)]."""
    recs = recs if recs is not None else load_registry()
    rendered, spans = fill(text, recs=recs)
    out = []
    for s, e, rid, view in spans:
        sent = sentence(rendered, s, e)
        errs = lint(sent, recs[rid])
        if errs:
            out.append((rid, view, sent, errs))
    return out


# ---------------------------------------------------------------- sites and bindings

TAG = re.compile(r"<[^>]*>")


def plain(line):
    """A template line's text, tags removed, so that sentences split where the reader sees them."""
    return re.sub(r"\s+", " ", TAG.sub(" ", line)).strip()


def anchored(anchor, line):
    """Whether an anchor picks a line: it occurs in the line, or with a leading "^" the line starts with it
    (for a short line whose text also occurs inside a longer one)."""
    if anchor.startswith("^"):
        return line.lstrip().startswith(anchor[1:])
    return anchor in line


def groups_sites(groups):
    """groups.py's text units by locator: "<section id>/claim|range|why", "<section id>/term:<name>" and
    "<section id>/f<first ladder ref>/text|why". The drift audit keys its source map the same way."""
    out = {}
    for g in groups:
        for field in ("claim", "range", "why"):
            if g.get(field):
                out[f"{g['id']}/{field}"] = g[field]
        for name, gloss in g.get("terms", []):
            out[f"{g['id']}/term:{name}"] = f"{name}: {gloss}"
        for f in g["findings"]:
            for field in ("text", "why"):
                if f.get(field):
                    out[f"{g['id']}/f{f['refs'][0]}/{field}"] = f[field]
    return out


def load_bindings(path=None):
    rows = list(csv.DictReader(Path(path or BINDINGS).open()))
    seen = set()
    for b in rows:
        k = (b["file"], b["locator"], b["quantity_id"], b["view"])
        if k in seen:
            raise SystemExit(f"[BLOCKED] quantity_bindings.csv lists {k} twice")
        seen.add(k)
    return rows


def value_binding_errors(b, values, label, recs=None):
    """The build's test of a table row: it carries the record's values (a scalar at both ends) and its label passes
    the record's lint."""
    recs = recs if recs is not None else load_registry()
    where = f"{b['file']} {b['locator']!r}"
    if values is None:
        return [f"{where}: no such row"]
    v = record_value(b["quantity_id"], recs)
    want = tuple(v) if isinstance(v, tuple) else (v, v)
    if len(want) != len(values) or any(abs(a - c) > 1e-9 for a, c in zip(want, values)):
        return [f"{where}: row shows {tuple(values)}, record {b['quantity_id']} is {want} (a typed number?)"]
    return [f"{where}: label {label!r} {'; '.join(errs)}" for errs in [lint(label, recs[b["quantity_id"]])] if errs]


def binding_errors(b, unit_text):
    """The build's test of one text binding: its site still quotes the record through a placeholder. The
    sentence around it is tested by the lint the build runs on every unit (`lint_unit`)."""
    if unit_text is None:
        return [f"{b['file']} {b['locator']!r}: the site is gone"]
    ph = f"{{{{q:{b['quantity_id']}|{b['view']}}}}}"
    if ph not in unit_text:
        return [f"{b['file']} {b['locator']!r}: {ph} is not at its site (a typed number replaced it?)"]
    return []
