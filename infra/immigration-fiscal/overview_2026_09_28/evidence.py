"""Render the ladder groups: numbered findings, evidence tags, per-finding notes, bibliography.

Method symbols and dataset names are detected from each entry's own text, so they say what the
entry reports using, not what the page claims.
"""

import html
import re

from groups import GROUPS, INTERNAL_ENTRIES, RETIRED

# (symbol, label, description, patterns). Acronyms match case-sensitively on word boundaries.
KINDS = [
    ("S", "survey", "survey microdata (people's answers, person by person)", [
        ("CPS", r"\bCPS\b|\bASEC\b"), ("ACS", r"\bACS\b|\bPUMS\b"), ("MEPS", r"\bMEPS\b"),
        ("NHTS", r"\bNHTS\b"), ("GSS", r"\bGSS\b"), ("ANES", r"\bANES\b"), ("NLSY", r"\bNLSY"),
        ("NCVS", r"\bNCVS\b"), ("Consumer Expenditure Survey", r"Consumer Expenditure|\bCE 20\d\d"),
        ("New Immigrant Survey", r"New Immigrant Survey"), ("IIMMLA", r"\bIIMMLA\b"), ("CILS", r"\bCILS\b"),
        ("Pew surveys", r"\bPew\b"), ("American Housing Survey", r"American Housing Survey|\bAHS\b"),
        ("SCF", r"\bSCF\b"), ("ENIGH", r"\bENIGH\b"), ("NAEP", r"\bNAEP\b"), ("PISA", r"\bPISA\b"),
        ("SIPP", r"\bSIPP\b"), ("ECLS-K", r"\bECLS"), ("IPUMS", r"\bIPUMS\b"), ("SPI", r"\bSPI\b")]),
    ("A", "records", "administrative records (tax, benefit, police, birth, school records)", [
        ("IRS", r"\bIRS\b"), ("SSA", r"\bSSA\b"), ("T-MSIS", r"T-MSIS"), ("CMS", r"\bCMS\b"),
        ("NVSS births", r"\bNVSS\b"), ("NIBRS", r"\bNIBRS\b"), ("BJS", r"\bBJS\b"), ("SHR", r"\bSHR\b"),
        ("FBI UCR", r"\bUCR\b|\bFBI\b"), ("USCIS / OHSS", r"\bUSCIS\b|\bOHSS\b"),
        ("Census of Governments", r"Census of Governments"), ("CMS S-10", r"\bS-10\b"), ("CRDC", r"\bCRDC\b"),
        ("Opportunity Atlas", r"Opportunity Atlas|Opportunity Insights"),
        ("Social Capital Atlas", r"Social Capital Atlas"), ("INEGI", r"\bINEGI\b"),
        ("CDC WONDER", r"\bWONDER\b"), ("Sentencing Commission", r"Sentencing Commission|\bUSSC\b"),
        ("Texas DPS", r"Texas DPS|\bDPS\b"), ("NCES", r"\bNCES\b"), ("HMDA / FHFA", r"\bFHFA\b|\bHMDA\b"),
        ("FARS / CCRS crash records", r"\bFARS\b|\bCCRS\b"), ("CDC TB surveillance", r"\bCDC\b"),
        ("register data", r"\bregister")]),
    ("N", "accounts", "national accounts and budget totals", [
        ("BEA NIPA", r"\bBEA\b|\bNIPA\b"), ("Trustees / SOSI", r"Trustees|Statement of Social Insurance"),
        ("Treasury", r"\bTreasury\b"), ("CBO baseline", r"\bCBO\b")]),
    ("M", "model", "the account's engine or another model run here", [
        ("account engine", r"\bengine\b|main_case|main case"), ("CES production", r"\bCES\b"),
        ("back-cast", r"back-cast"), ("lineage model", r"\blineage\b")]),
    ("C", "causal", "a design aimed at cause (instrument, panel, placebo, lottery)", [
        ("instrument", r"instrument|\bIV\b|shift-share|Bartik"), ("fixed effects", r"fixed effects|fixed-effects"),
        ("placebo", r"placebo"), ("lottery", r"lottery"), ("synthetic control", r"synthetic control")]),
    ("T", "test", "a test fixed before looking, against data the account never used", [
        ("held-out test", r"before looking|held-out|which no step of it used|never used")]),
]


def strip_md(s):
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = s.replace("**", "").replace("`", "")
    return re.sub(r"\s+", " ", s).strip()


def tag_blocks(text, tag):
    """Balanced [TAG: ...] blocks."""
    out = []
    for m in re.finditer(r"\[" + tag + r":", text):
        depth, j = 0, m.start()
        while j < len(text):
            depth += {"[": 1, "]": -1}.get(text[j], 0)
            if depth == 0:
                break
            j += 1
        out.append(strip_md(text[m.end():j]))
    return out


def keep_links(s):
    s = re.sub(r"\[([^\]]*)\]\((https?://[^)\s]+)\)", r"\1 <\2>", s)
    return strip_md(s)


def source_spans(text):
    """Every 'SOURCE:' span, inside any tag block, up to its closing bracket or the next tag."""
    out = []
    for m in re.finditer(r"SOURCE:", text):
        depth, j = 0, m.end()
        while j < len(text):
            c = text[j]
            if c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
                if depth < 0:
                    break
            elif depth == 0 and text.startswith(("; CALCULATION", "; DATA", "; INFERENCE"), j):
                break
            j += 1
        out.append(keep_links(text[m.end():j]))
    return out


MONTHS = ("January February March April May June July August September October November December "
          "Census Table Note Figure Section Prisoners Survey Wave Round Law Fiscal Budget Report Rating "
          "Revisions Decision Brief Profile Statement Tables Update Release Vintage Summer Spring Fall Winter").split()
NOT_AUTHORS = set((
    "The In Across Over Since From After Before Between By For At On Of To With Within Without During Until "
    "Executed Corrected Updated Revised Added Measured Published Reported Adjusted Pooled Recovered Supplied "
    "Jan Feb Mar Apr Jun Jul Aug Sep Sept Oct Nov Dec Notes Note Bureau Hispanic White Black Asian Mexican "
    "Mexico America American Angeles California Texas Florida Illinois Arizona Nevada Colorado York Chicago Denver "
    "Houston Dallas Rochester Germany Denmark Sweden Norway Europe Italy Spain Austria Canada Cuba India China "
    "Congress Medicare Medicaid Social Security Federal State States Current Central Only Each Every All Both "
    "Scored Charged Pricing Priced Tested Weighted Translated Counted Carried Read Run Rerun Moving Removing "
    "Cohort Cohorts Class Classes Wave Year Years Age Ages Men Women Children Pupils Adults Residents Arrivals "
    "Legal Unauthorized Immigrants Natives Model Case Cases Lane Entry Entries Ladder Memo Page Chart Basics City Economy Institute Narrowed Nationally Qualified Reports Select Sensitivity Supplement Under Victimization"
).split())
AUTHOR_YEAR = re.compile(
    r"\b((?:[A-Z][a-zà-ÿ'’]+)(?:(?: (?:&|and) |[–-])[A-Z][a-zà-ÿ'’]+)*(?: et al\.?)?),? \(?((?:19[5-9]|20[0-2])\d)[a-z]?\b")


def citations(text):
    """Author-year citations named in the entry's own text."""
    out = []
    for m in AUTHOR_YEAR.finditer(strip_md(text)):
        a = m.group(1)
        head = a.split()[0].split("–")[0]
        if head in MONTHS or head in NOT_AUTHORS or head.endswith(("'s", "’s")):
            continue
        out.append(f"{a.replace(' and ', ' & ')} {m.group(2)}")
    return list(dict.fromkeys(out))


def detect(text):
    kinds, names = [], []
    for sym, _label, _desc, pats in KINDS:
        hit = [name for name, pat in pats if re.search(pat, text)]
        if hit:
            kinds.append(sym)
            if sym in ("S", "A", "N"):  # datasets only; methods are shown by the evidence level
                names += [n for n in hit if n not in names]
    return kinds, names


def cut(s, n=260):
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0] + "…"


def rating(text):
    m = re.search(r"Rating: \*\*(.+?)\*\*", text)
    return strip_md(m.group(1)) if m else ""


PUBLICATION = re.compile(r"https?://|doi|NBER|\bet al\b|[A-Z][a-z]+(?:[–-][A-Z][a-z]+)* \(?(?:19|20)\d\d\b|Journal|JPE|QJE|AER")
INTERNAL = re.compile(r"^(memo|research/|infra/|\.\./|immigration-)|\.md\b|\.csv\b|\.py\b|RESULT")


def chips(kinds):
    return "".join(f'<abbr class="chip k{k}" title="{html.escape(next(d for s, _, d, _ in KINDS if s == k))}">{k}</abbr>'
                   for k in kinds)


def check_coverage(entries, fail):
    seen = {}

    def put(key, where):
        key = str(key)
        if key in seen:
            fail(f"entry {key} is in both {seen[key]} and {where}")
        seen[key] = where

    for g in GROUPS:
        for i, f in enumerate(g["findings"]):
            for r in f["refs"]:
                put(r, f"{g['id']}#{i + 1}")
        for r in g["minor"]:
            put(r, f"{g['id']} minor")
    for r in RETIRED:
        put(r, "retired")
    for r in INTERNAL_ENTRIES:
        put(r, "internal")
    missing = sorted(set(entries) - set(seen), key=lambda k: (k[0] == "o", int(k.lstrip("o"))))
    unknown = sorted(set(seen) - set(entries))
    if missing or unknown:
        fail(f"unplaced ladder entries {missing}; placed but not in the ladder {unknown}. Place new entries in groups.py")


from evidence_class import CLASS, INPUTS, STEPS


def level_tag(f, fail):
    key = f["refs"][0]
    if key not in CLASS:
        fail(f"finding starting with ladder {key} has no entry in evidence_class.py")
    inp, step, bias = CLASS[key]
    tag = (f'<span class="lvl" title="{html.escape(INPUTS[inp][1])}">{INPUTS[inp][0]}</span>'
           f' <span class="arrow">→</span> '
           f'<span class="lvl" title="{html.escape(STEPS[step][1])}">{STEPS[step][0]}</span>')
    if bias:
        tag += f'<br><span class="soft">Known bias: {html.escape(bias)}</span>'
    return tag


BUILD_PART = "build"  # the part that opens with the template's build fragment (ledger, alternatives, assumptions)
BUILD_MARKER = "{{BUILD_BLOCK}}"  # where the fragment goes; build.py substitutes it


def render(entries, fail, build_toc=()):
    """The page's parts. `build_toc` lists (anchor, title HTML) for the build fragment's headings: the build part's
    contents list them before its groups, and its heading is followed by BUILD_MARKER."""
    from groups import PARTS
    check_coverage(entries, fail)
    stray = sorted({g["part"] for g in GROUPS} - {pid for pid, _ in PARTS})
    if stray:
        fail(f"groups in parts that PARTS lacks, so the page would drop them: {stray}")
    bib = {}
    toc, blocks = [], []
    n_find = 0
    gi = 0
    # Readers see section.finding numbers ("4.2"). Ladder numbers stay in data-ladder attributes and
    # HTML comments, for maintainers only.
    labels = {}  # ladder ref -> (label, anchor)
    sections = {}  # group id -> section number
    for pid, ptitle in PARTS:
        groups = [g for g in GROUPS if g["part"] == pid]
        if not groups and pid != BUILD_PART:
            continue
        toc.append(f'<li><a href="#part-{pid}">{html.escape(ptitle)}</a><ol>')
        blocks.append(f'<h2 id="part-{pid}">{html.escape(ptitle)}</h2>')
        if pid == BUILD_PART:
            toc += [f'<li><a href="#{a}">{t}</a></li>' for a, t in build_toc]
            blocks.append(BUILD_MARKER)
        for g in groups:
            gi += 1
            sections[g["id"]] = gi
            toc.append(f'<li><a href="#{g["id"]}">{html.escape(g["claim"])}</a></li>')
            items = []
            for fi, f in enumerate(g["findings"], 1):
                n_find += 1
                fid = f"{g['id']}-{fi}"
                flabel = f"{gi}.{fi}"
                for r in f["refs"]:
                    labels[str(r)] = (flabel, fid)
                text_all = " ".join(entries[str(r)]["body"] for r in f["refs"])
                _kinds, names = detect(text_all)
                fsrc = []
                for r in f["refs"]:
                    e = entries[str(r)]
                    for s_ in source_spans(e["body"]):
                        for part in re.split(r";\s+|,\s+(?=https?://)", s_):
                            part = part.strip(" .,")
                            if re.search(r"https?://", part) and not INTERNAL.search(part):
                                k = re.sub(r"\W+", " ", part.lower())[:90]
                                bib.setdefault(k, [cut(part, 220), []])[1].append(fid)
                                fsrc.append(bib[k][0])
                    for c in citations(e["body"]):
                        k = re.sub(r"\W+", " ", c.lower())
                        bib.setdefault(k, [c, []])[1].append(fid)
                        fsrc.append(c)
                fsrc = list(dict.fromkeys(fsrc))
                rows = []
                if f.get("why"):
                    rows.append(f'<p>{html.escape(f["why"])}</p>')
                if names:
                    rows.append(f'<p class="how">Data: {html.escape(", ".join(names))}.</p>')
                if fsrc:
                    rows.append(f'<p class="how">Sources: {html.escape(" · ".join(fsrc))}.</p>')
                ladder = " ".join(str(r) for r in f["refs"])
                items.append(
                    f'<li id="{fid}" data-ladder="{ladder}"><p class="ftext">'
                    f'<a class="fnum" href="#{fid}">{flabel}</a> {html.escape(f["text"])}</p>'
                    f'<p class="fmeta">{level_tag(f, fail)}</p>'
                    f'<details><summary>Evidence</summary>{"".join(rows)}</details></li>')
            terms = "".join(f"<dt>{html.escape(t)}</dt><dd>{html.escape(m)}</dd>" for t, m in g["terms"])
            minor = (f'<!-- narrower ladder entries, not summarised: {" ".join(str(r) for r in g["minor"])} -->'
                     if g["minor"] else "")
            blocks.append(f"""
<section id="{g['id']}" class="group">
  <h3><span class="gnum">{gi}</span> {html.escape(g['claim'])}</h3>
  {f'<p class="size">{html.escape(g["range"])}</p>' if g["range"] else ''}
  <p>{html.escape(g['why'])}</p>
  <ul class="findings">{''.join(items)}</ul>
  {f'<details><summary>Terms</summary><dl class="terms">{terms}</dl></details>' if terms else ''}
  {minor}
</section>""")
        toc.append("</ol></li>")
    legend = ('<table class="levels"><thead><tr><th>Input</th><th>Meaning</th></tr></thead><tbody>'
              + "".join(f"<tr><td class=lvl>{n}</td><td>{html.escape(d)}</td></tr>" for n, d in INPUTS.values())
              + '</tbody></table><table class="levels"><thead><tr><th>Step</th><th>Meaning</th></tr></thead><tbody>'
              + "".join(f"<tr><td class=lvl>{n}</td><td>{html.escape(d)}</td></tr>" for n, d in STEPS.values())
              + "</tbody></table>")
    bib_items = sorted(bib.values(), key=lambda v: v[0].lower())
    fid_label = {fid: lab for lab, fid in labels.values()}
    bibl = "".join(
        f'<li>{html.escape(t)} <span class="ref">'
        f'{" ".join(f"<a href=#{x}>{fid_label[x]}</a>" for x in dict.fromkeys(ids))}</span></li>'
        for t, ids in bib_items)
    return dict(toc="".join(toc), groups="\n".join(blocks), legend=legend, biblio=bibl, labels=labels, sections=sections,
                n_find=n_find, n_bib=len(bib_items), n_retired=len(RETIRED))
