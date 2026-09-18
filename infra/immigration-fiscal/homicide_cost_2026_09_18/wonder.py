"""CDC WONDER XML API helper (Underlying Cause of Death, D158 = 2018-2024 single race).

The XML API is fussy: every cause-of-death select must be explicitly set to *All*
except the one being filtered on, group-by values for hierarchical variables need a
`-levelN` suffix, finder variables use `F_`, plain selects use `V_`, and `O_aar_pop`
is mandatory even when age adjustment is off.  Documented 15-second minimum spacing
between requests is respected.
"""
from __future__ import annotations

import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
CACHE.mkdir(exist_ok=True)
URL = "https://wonder.cdc.gov/controller/datarequest/{db}"
_last = [0.0]

FINDERS = ["V1", "V2", "V9", "V10", "V25", "V27", "V30", "V31"]
# every plain select in D158; anything not explicitly filtered must be *All*
SELECTS = ["V4", "V5", "V6", "V7", "V11", "V12", "V17", "V18", "V19", "V20", "V21",
           "V22", "V23", "V24", "V42", "V43", "V44", "V45", "V51", "V52"]


def _param(name: str, values) -> str:
    if not isinstance(values, (list, tuple)):
        values = [values]
    return "<parameter><name>%s</name>%s</parameter>" % (
        name, "".join(f"<value>{v}</value>" for v in values))


def request(byvars, filters: dict, measures=("M1",), db: str = "D158",
            o_age: str = "V51", tag: str = "q") -> ET.Element:
    """byvars: list of variable ids (with -levelN where hierarchical).
    filters: {var_id: value_or_list}; every other variable defaults to *All*."""
    cache = CACHE / f"wonder_{db}_{tag}.xml"
    if cache.exists() and cache.stat().st_size > 1000:
        return ET.fromstring(cache.read_text())
    parts = [_param("accept_datause_restrictions", "true")]
    bv = list(byvars) + ["*None*"] * (5 - len(byvars))
    for i, b in enumerate(bv, 1):
        parts.append(_param(f"B_{i}", b if b == "*None*" else f"{db}.{b}"))
    for i, m in enumerate(measures, 1):
        parts.append(_param(f"M_{i}", f"{db}.{m}"))
    for v in FINDERS:
        parts.append(_param(f"F_{db}.{v}", filters.get(v, "*All*")))
    for v in SELECTS:
        parts.append(_param(f"V_{db}.{v}", filters.get(v, "*All*")))
    opts = {"O_javascript": "on", "O_precision": "1", "O_show_totals": "true",
            "O_show_zeros": "true", "O_show_suppressed": "true", "O_timeout": "600",
            "O_aar": "aar_none", "O_aar_pop": "0000", "O_rate_per": "100000",
            "O_age": f"{db}.{o_age}", "O_ucd": f"{db}.V2", "O_location": f"{db}.V9",
            "O_urban": f"{db}.V19", "O_race": f"{db}.V42", "O_title": "homicide lane"}
    for v in FINDERS:
        opts[f"O_{v}_fmode"] = "freg"
    if "V4" in filters:
        opts["O_ucd"] = f"{db}.V4"
    for k, v in opts.items():
        parts.append(_param(k, v))
    xml = "<request-parameters>" + "".join(parts) + "</request-parameters>"
    wait = 16 - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    r = requests.post(URL.format(db=db), timeout=600,
                      data={"request_xml": xml, "accept_datause_restrictions": "true"})
    _last[0] = time.time()
    root = ET.fromstring(r.text)
    if root.find(".//data-table") is None:
        msgs = " | ".join(m.text or "" for m in root.findall(".//message"))
        raise RuntimeError(f"WONDER {db} {tag}: {msgs}")
    cache.write_text(r.text)
    return root


def rows(root: ET.Element, nby: int, nmeas: int = 1):
    """Flatten the data-table.  WONDER omits leading labels that repeat (rowspan) and
    emits subtotal rows as <c c="n"/><c dt="..."/>; those are dropped."""
    out, carry = [], [None] * nby
    for r in root.findall(".//data-table/r"):
        cells = r.findall("c")
        if any(c.get("dt") is not None or c.get("c") is not None for c in cells):
            continue
        labels = [c.get("l") for c in cells if c.get("l") is not None]
        vals = [c.get("v") for c in cells if c.get("v") is not None]
        start = nby - len(labels)
        row = carry[:start] + labels
        carry = row[:]
        out.append(row + vals[:nmeas])
    return out
