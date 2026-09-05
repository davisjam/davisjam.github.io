#!/usr/bin/env python3
"""Generate the umbrella site's Research, Teaching, and Service pages.

    python3 generators/generate_umbrella_pages.py [research|teaching|service]

Implements the SSOT rule (model/ssot-records.md):

    Narrative prose is hand-authored. Enumerative facts are generated.

Narrative lives in this file, close to the structure it argues for. Enumerative
records -- publications, patents, grants, awards, courses, service -- are
projected from data/*.yaml and never transcribed into page prose. That is why
the previous Service page went stale: it was a hand-maintained list, so it
silently stopped tracking the record in about 2024.

Writes Jekyll markdown into repos/davisjam.github.io/_pages/.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

def yq(v: str) -> str:
    return '"' + str(v).replace("\\", "\\\\").replace('"', '\\"') + '"'


import _paths
import yaml

# Resolved from whichever layout this copy sits in -- see _paths.py.
ROOT = _paths.DATA.parent
PAGES = _paths.PAGES

BANNER = ("<!-- Enumerative sections on this page are GENERATED from the davis-web\n"
          "     canonical records by generators/generate_umbrella_pages.py.\n"
          "     Edit the narrative in that generator, or the facts in data/*.yaml.\n"
          "     Hand edits here will be overwritten. -->")


def load():
    import yaml
    r = lambda p: yaml.safe_load(pathlib.Path(p).read_text())
    return (r(_paths.MODEL / "sites.yaml"), r(_paths.DATA / "publications.yaml"),
            r(_paths.DATA / "awards.yaml"), r(_paths.DATA / "service.yaml"), r(_paths.DATA / "courses.yaml"),
            r(_paths.DATA / "teaching.yaml"), r(_paths.DATA / "people.yaml"))


# --------------------------------------------------------------------------- research

PROGRAM_COPY = {
    "mage": ("How should we engineer software when implementation becomes abundant "
             "but engineering judgment remains scarce?",
             "Model-Based Agentic Software Engineering (MAGE) studies software engineering for "
             "increasingly capable AI agents. The central move is to externalize engineering "
             "knowledge into models, align delegated work with authoritative obligations, validate "
             "realizations against those models, and turn recurring human reasoning into reusable "
             "engineering capital."),
    "embedded-swe": ("Making analysis and assurance practical for embedded software.",
             "Embedded systems combine high consequences with environments that make conventional "
             "software analysis unusually difficult. Our work has developed techniques for "
             "rehosting, dynamic analysis, static analysis, testing, and verification of embedded "
             "software. A current thrust is Unit Proofing: making component-level formal "
             "verification practical enough to use as an ordinary engineering tool."),
    "failure-aware-sdlc": ("Learning systematically from the ways software systems fail.",
             "Software failures contain engineering knowledge, but organizations and research "
             "communities often treat them as isolated events. This research studies failures "
             "empirically and asks how evidence from past failures can improve requirements, "
             "design, testing, processes, and engineering decisions before the next system fails "
             "in the same way."),
    "ptm-se": ("What changes about software engineering when the reused component is a learned model?",
             "Pre-trained models are increasingly reused as software dependencies, but their "
             "behavior, interfaces, provenance, compatibility, and failure modes differ "
             "substantially from conventional libraries. We study how models are discovered, "
             "selected, integrated, tested, secured, reproduced, and evolved as components of "
             "larger software systems."),
    "software-supply-chain": ("How can software reuse remain trustworthy at ecosystem scale?",
             "Modern software is assembled from components produced by many actors across package "
             "registries, repositories, build systems, and increasingly model and agent "
             "ecosystems. We study the foundations and applications of trustworthy software "
             "supply chains, including provenance and signing, dependency risk, package "
             "confusion, adoption and usability, and mechanisms for making reuse safer."),
    "saferegex": ("Small programs expose surprisingly large software-engineering problems.",
             "Regular expressions are reused across languages, libraries, and ecosystems, yet "
             "developers struggle to understand their behavior, portability, performance, and "
             "security consequences. This body of work studies regexes as software artifacts, "
             "from reuse and developer comprehension to catastrophic backtracking, analysis, "
             "mitigation, and the semantics of modern regex engines."),
}

# Ordered deliberately: security/reliability first (the broadest historical
# range), then efficient systems, then education. Each cluster names 2-3
# EXPLICIT examples rather than picking heuristically -- the trio is chosen to
# show breadth, not recency. The security trio runs human-facing security ->
# platform governance -> software/system analysis.
CLUSTER_COPY = {
    "reliability-security-systems": (
        "Software security, reliability, and systems",
        "I have studied software security and reliability across areas including GraphQL, "
        "provenance, privacy, trust and safety, anti-phishing interventions, and software "
        "testing. Examples include:",
        ["C-7", "J-5", "C-37"]),
    "efficient-ml-systems": (
        "Efficient computing systems",
        "My work on efficient computing systems includes adaptive models, inference "
        "optimization, edge computing, and energy efficiency:",
        ["C-5", "C-19", "C-43"]),
    "engineering-education": (
        "Engineering education",
        "I study how software engineering and systems thinking can be taught through "
        "project-based learning and increasingly capable AI tools:",
        ["W-13", "W-14"]),
}

# Venue strings without a parenthesised abbreviation need one for the compact
# "(ABBREV 'YY)" form. Only genuine gaps belong here.
VENUE_ABBREV = {"USENIX Annual Technical Conference": "USENIX ATC"}


def cite(p: dict) -> str:
    """Title as a link, then venue abbreviation and two-digit year. Nothing else:
    the full bibliographic apparatus is what the Publications page is for."""
    import re as _re
    v = p.get("venue") or ""
    m = _re.search(r"\(([A-Za-z][A-Za-z0-9/&-]{1,14})\)", v)
    abb = m.group(1) if m else next(
        (a for k, a in VENUE_ABBREV.items() if k.lower() in v.lower()), "")
    yr = p.get("year")
    where = f"{abb} \u2019{str(yr)[2:]}" if abb and yr else (abb or str(yr or ""))
    # Emit HTML, not Markdown: kramdown does not process Markdown inside a
    # block-level <div>, so [text](url) would render literally.
    import html as _h
    link = p.get("paper_url")
    t = _h.escape(p["title"])
    title = f'<a href="{_h.escape(str(link), quote=True)}">{t}</a>' if link else t
    return f'{title} <span class="venue">({where})</span>' if where else title


CARD_CSS = """<style>
/* The width system lives in _sass/_research.scss, keyed on :has(), so the
   landing and the programme pages share one definition.

   USE A GRID, DO NOT DRAW THE GRID (same rule as the People page).

   These were bordered cards with a rule under the title and another above the
   footer. None of those lines encoded anything: each programme already has its
   own figure, a large title and generous space around it. Removing them lets
   the signature figures -- which ARE the visual thesis of each programme --
   become the first thing the eye lands on.

   Column count emerges from available width; it is not decreed as 3x2. */
/* minmax(min(340px,100%),...) not minmax(340px,...): a bare 340px floor cannot
   shrink below itself, so the grid overflowed a 375px viewport. */
.research-programs{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(340px,100%),1fr));
  column-gap:2.5rem;row-gap:3.25rem;margin:2em 0 2.5em}
.research-program{min-width:0}          /* long titles must not blow the track */
/* HIERARCHY: title, question, THEN figure. The figure used to come first,
   which asked a visitor to decipher a diagram before knowing which programme
   it belonged to -- and these drawings cannot be read at this size anyway.
   Here the thumbnail is a visual signature for recognition and
   differentiation; the title and question carry the meaning.

   UNIFORM VIEWPORT: all six get the same height whatever their native aspect
   ratio, so MAGE's tall figure does not tower over the others. object-fit
   contain, never cover -- cropping a diagram to make rectangles match would
   destroy it. The image is aria-hidden and untabbable: it is decorative here,
   its content lives on the programme page, and the title link already carries
   the accessible name. */
.research-program__figure{display:block;border:1px solid #e4e0d8;background:#fff;
  padding:.4rem;margin:0 0 .6rem;height:190px}
.research-program__figure img{width:100%;height:100%;object-fit:contain;display:block}
.research-program h2{margin:0 0 .3rem;font-size:1.15rem;line-height:1.3}
.research-program h2 a{color:inherit;text-decoration:none}
.research-program h2 a:hover{color:#8E6F3E;text-decoration:underline}
.research-program__q{margin:0 0 .85rem;font-size:.98rem;color:#44403c}
/* No rule above it, no CTA beside it: the title is the link. */
.research-program__foot{margin:0;font-size:.85rem;color:#57534e}
</style>
"""


def research(sites, pubs, *_):
    order = ["mage", "embedded-swe", "failure-aware-sdlc", "ptm-se",
             "software-supply-chain", "saferegex"]
    by_pid = {s["project_id"]: s for s in sites["sites"] if s.get("project_id")}

    # SSOT for the cards. The page renders this; nothing about a programme is
    # typed into page source, so title, question, count, and figure cannot drift
    # from model/sites.yaml and data/publications.yaml.
    data = ["# GENERATED by davis-web generators/generate_umbrella_pages.py.",
            "# Source: model/sites.yaml + data/publications.yaml. Do not hand-edit.", ""]
    import yaml as _y
    import xml.etree.ElementTree as _ET
    copy = _y.safe_load((_paths.DATA / "program-copy.yaml").read_text())["programs"]
    for pid in order:
        site = by_pid[pid]
        n = sum(1 for x in pubs["publications"] if pid in (x.get("projects") or []))
        fig = (site.get("figure") or {})

        # SIGNATURE FIGURE IS ONE ARTIFACT. This used to emit
        # /images/research/<pid>.svg -- a hand-copied duplicate of the real
        # drawing. Four of the six had drifted, and the regex card was still
        # showing the chronological arc months after the page moved to the
        # microscope figure. The landing and the programme page now resolve the
        # SAME path, so changing a figure necessarily changes both.
        source = f"/assets/research/{pid}/{fig.get('id')}.svg"
        svg = PAGES.parent / source.lstrip("/")
        if not svg.exists():
            raise SystemExit(f"{pid}: signature figure {source} does not exist")
        root = _ET.parse(svg).getroot()
        title_el = root.find("{http://www.w3.org/2000/svg}title")
        alt = " ".join((title_el.text or "").split()) if title_el is not None else ""

        # The landing question may be deliberately shorter than the page's --
        # regex trades precision for intrigue here -- but it is still declared
        # in the same record, never retyped into page source.
        q = copy[pid].get("landing_question") or copy[pid]["question"]
        data += [f"- title: {yq(site['title'])}",
                 f"  short_title: {yq(site.get('short_name') or site['title'])}",
                 f"  slug: {pid}",
                 f"  question: {yq(' '.join(q.split()))}",
                 # Consolidated: the entry links to the page in THIS site, not
                 # to a standalone project site.
                 f"  url: /research/{pid}/",
                 f"  figure: {source}",
                 f"  figure_alt: {yq(alt)}",
                 f"  publications: {n}", ""]
    (PAGES.parent / "_data").mkdir(exist_ok=True)
    (PAGES.parent / "_data/research.yml").write_text("\n".join(data))

    o = [f'''---
layout: single
title: "Research"
permalink: /research/
author_profile: true
---

{BANNER}

I study how to make software-intensive systems reliable and secure. My research begins
with engineering practice: I study how software is built and used, identify where existing
assumptions and engineering methods break down, and turn those findings into new methods,
tools, and ways of engineering software.

I pursue this problem from several directions: understanding how software fails in
practice; developing analysis and assurance methods that prevent failures; making
dependencies and reused components easier to understand and govern; and studying how
emerging technologies, including AI, change the way software is built and engineered.

My current research is organized around six programs.
''']

    o.append(CARD_CSS)
    o.append("""
<div class="research-programs">
{% for program in site.data.research %}
  <div class="research-program">
    <h2><a href="{{ program.url }}">{{ program.title }}</a></h2>
    <p class="research-program__q">{{ program.question }}</p>
    <a class="research-program__figure" href="{{ program.url }}" tabindex="-1" aria-hidden="true">
      <img src="{{ program.figure | relative_url }}" alt="" loading="lazy">
    </a>
    <p class="research-program__foot">{{ program.publications }} publications</p>
  </div>
{% endfor %}
</div>
""")
    by_id = {x["id"]: x for x in pubs["publications"]}
    o.append("\n## Other research\n\n"
             "My research also extends beyond these six programs, often through collaborations "
             "in which software-engineering questions intersect with other areas.\n")

    for heading, copy, picks in CLUSTER_COPY.values():
        o.append(f"\n**{heading}.** {copy}\n")
        o.append('<div class="other-works">')
        for pid in picks:
            p = by_id.get(pid)
            if p is None:
                raise SystemExit(f"other-research example {pid} not in the record")
            o.append(cite(p) + "<br>")
        o.append("</div>")
    o.append("\nThe complete record is on the [Publications](/publications/) page.\n")

    pats = [p for p in pubs["publications"] if p.get("type") == "patent"]
    pats.sort(key=lambda p: -(p.get("year") or 0))
    # Ordinary-weight linked title, unlinked year. Bolding eight titles made the
    # patents visually outweigh everything else on the page.
    o.append("\n## Patents\n")
    for p in pats:
        rec = (p.get("links") or {}).get("record")
        title = f"[{p['title']}]({rec})" if rec else p["title"]
        note = " — provisional application" if p["id"] == "Pa-1" else ""
        o.append(f"- {title} ({p.get('year', 'n.d.')}){note}")
    o.append("")
    return "\n".join(o)


# --------------------------------------------------------------------------- teaching

def teaching(sites, pubs, awards, service, courses, teach, ppl=None):
    """The Teaching page.

    The page's protagonist is the teaching programme. MAGE is rendered as an
    INSET inside the ECE 30861 section rather than as a heading of its own:
    making it an h3 sibling of the course titles would assert, typographically,
    that it is a third course. It is course infrastructure.

    Recognition is generated from data/awards.yaml (`teaching` + `mentoring`)
    so the page cannot drift from the award record. Student outcomes come from
    data/teaching.yaml because they are awards to STUDENTS, which awards.yaml
    does not model.
    """
    def para(xs):
        return [" ".join(str(x).split()) + "\n" for x in xs]

    def stats(rows):
        out = ['<div class="teaching-stats" markdown="0">']
        for r in rows:
            out.append(f'  <div class="teaching-stat"><span class="teaching-stat__value">'
                       f'{r["value"]}</span><span class="teaching-stat__label">'
                       f'{r["label"]}</span></div>')
        out.append("</div>\n")
        return out

    by_id = {c["id"]: c for c in courses["courses"]}

    o = [f"""---
layout: single
title: "Teaching"
permalink: /teaching/
author_profile: true
---

{BANNER}
"""]
    o += para(teach["opener"])

    cl = teach["curricular_leadership"]
    o.append(f"## {cl['heading']}\n")
    o += para(cl["paragraphs"])

    cs = teach["courses"]
    o.append(f"## {cs['heading']}\n")
    for entry in cs["entries"]:
        c = by_id[entry["id"]]
        head = f"{c['number']} — {c['title']}"
        if entry.get("catalog_url"):
            head = f"[{head}]({entry['catalog_url']})"
        o.append(f"### {head}\n")
        o += para(entry["paragraphs"])
        ins = entry.get("inset")
        if ins:
            # Subordinate to the course, and quiet: a thin accent rule, no
            # eyebrow, no panel, no trailing link row. Links live in the prose.
            o.append('<aside class="course-inset" markdown="1">')
            o.append(f'#### {ins["title"]}\n')
            o += para(ins["paragraphs"])
            o.append("</aside>\n")

    ur = teach["undergraduate_research"]
    o.append(f"## {ur['heading']}\n")
    o += para(ur["paragraphs"])
    o += stats(ur["stats"])
    o += para(ur["closing"])

    vip = teach["vip"]
    o.append(f"### {vip['heading']}\n")
    o += para(vip["paragraphs"])
    for t in vip["teams"]:
        o.append(f"**{t['title']}**  \n{' '.join(t['blurb'].split())}\n")

    so = teach["student_outcomes"]
    o.append(f"## {so['heading']}\n")
    o += para([so["lead"]])
    for it in so["items"]:
        when = f"**{it['when']}** · " if it.get("when") else ""
        o.append(f"- {when}**{it['title']}**"
                 + (f"  \n  {' '.join(it['detail'].split())}" if it.get("detail") else ""))
    o.append("")
    o += para(so["closing"])

    rec = teach["recognition"]
    o.append(f"## {rec['heading']}\n")
    for a in sorted(awards["awards"]["teaching"] + awards["awards"]["mentoring"],
                    key=lambda a: -a["year"]):
        note = f"  \n  {a['note']}" if a.get("note") else ""
        o.append(f"- **{a['year']}** · {a['title']}{note}")
    o.append("")
    o += para(rec["closing"])

    sot = teach["sotl"]
    o.append(f"## {sot['heading']}\n")
    o += para(sot["paragraphs"])
    if sot.get("stats"):
        o += stats(sot["stats"])
    o += para(sot["closing"])
    return "\n".join(o)


# --------------------------------------------------------------------------- service

def service_page(sites, pubs, awards, service, courses, teach=None, ppl=None):
    """The Service page.

    One claim, four manifestations: I help run the institutions through which
    software-engineering research and education happen.

    Two deliberate omissions (James, 260905). There is no program-committee
    table and no journal list -- an educated reader who sees ICSE / FSE / USENIX
    Security / ISSTA / ASE already knows the level and breadth, and the years
    turn it into a CV transcription. And there is no "Recognition for service"
    section at the bottom: the reviewer awards render beside the reviewing they
    recognize, which is where they mean something.

    `purdue.additional` is intentionally not rendered -- see service.yaml.
    """
    L, RC, NP, PU = (service["leadership"], service["research_community"],
                     service["national_professional"], service["purdue"])

    o = [f"""---
layout: single
title: "Service"
permalink: /service/
author_profile: true
---

{BANNER}

I help run the institutions through which software-engineering research and education happen.

## Research leadership and community building
"""]
    for e in L["conference"]:
        o.append(f"- **{e['role']}**, {e['venue']} ({e['years']})")
    for e in L["sustained"]:
        prog = "; ".join(f"{x['role']} ({x['years']})" for x in e["progression"])
        o.append(f"- **{e['venue']}** — {prog}")
    o.append("")
    o.append("I also build research community locally, organizing peer mentoring and "
             "writing groups for junior faculty, a reading group, and visits by "
             "researchers whose work my group learns from.\n")

    o.append("## Research community service\n")
    venues = [c.get("short", c["venue"]) for c in RC["major_program_committees"]]
    listed = ", ".join(venues[:-1]) + f", and {venues[-1]}"
    o.append("Peer review is part of the infrastructure of research. I regularly serve on "
             f"program committees in software engineering and security, including {listed}, "
             "as well as related venues.\n")

    rev = [a for a in awards["awards"]["service"] if a.get("reviewer")]
    o.append(f"My reviewing has been recognized with {_num(len(rev))} reviewer awards:\n")
    for a in sorted(rev, key=lambda a: -a["year"]):
        o.append(f"- {a['title']} · {a['year']}")
    o.append("")

    o.append("## National and professional service\n")
    for e in NP:
        yrs = ", ".join(str(y) for y in e["years"])
        what = f" — {e['what']}" if e.get("what") else ""
        note = f"  \n  {e['note']}" if e.get("note") else ""
        o.append(f"- **{e['role']}**, {e['body']}{what} ({yrs}){note}")
    for e in RC.get("editorial", []):
        o.append(f"- **{e['role']}**, {e['venue']}")
    o.append("")

    o.append("## Institutional service at Purdue\n")
    o.append("At Purdue, I contribute primarily where software engineering intersects with "
             "program development, institutional assessment, and emerging changes in "
             "engineering practice.\n")
    for e in PU["institutional"]:
        o.append(f"**{e['what']}** ({e['years']})  ")
        o.append(" ".join(e["detail"].split()) + "\n")
    return "\n".join(o)


def _num(n: int) -> str:
    return {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}.get(n, str(n))


def people(sites, pubs, awards, service, courses, teach=None, ppl=None):
    """The People page.

    Current researchers are people; graduate alumni are mentorship outcomes;
    undergraduate participation is a programme at scale. Those three things want
    three different visual grammars, and the page gives them three.

    USE A GRID, DO NOT DRAW THE GRID. An earlier version wrapped every person in
    a bordered cell, which turned a roster into a visible database table: the
    borders encoded nothing -- not programme, not cohort, not advising -- they
    merely revealed where the CSS boxes were. Every visible rule here has to
    name what it communicates, and a cell boundary communicates nothing.

    So: no card borders, no vertical rules, no shadows. Section headings and
    whitespace carry the structure. Alumni are denser than current members
    because they are a historical record rather than an introduction.

    A person's NAME is their only link, and only when a verified LinkedIn URL
    exists in the record -- never one constructed from a name.
    """
    P = ppl
    areas = P["area_phrases"]
    # Deposited theses live in their own record; People links to them rather
    # than restating the title. thesis_author is the explicit join key.
    theses = {t["author"]: t for t in
              yaml.safe_load((_paths.DATA / "theses.yaml").read_text())["theses"]}

    def named(e, fallback_url=None):
        url = e.get("linkedin") or e.get("name_url") or fallback_url
        return f'<a href="{url}">{e["name"]}</a>' if url else e["name"]

    def researcher(e):
        out = ['<div class="person">']
        if e.get("photo"):
            out.append(f'  <img class="person__photo" src="{e["photo"]}" '
                       f'alt="Portrait of {e["name"]}">')
        out.append('  <div class="person__text">')
        out.append(f'    <p class="person__name">{named(e)}</p>')
        meta = [e["degree"]] if e.get("degree") else []
        if e.get("co_advisor"):
            meta.append(f'co-advised with {e["co_advisor"]}')
        if meta:
            out.append(f'    <p class="person__meta">{" &middot; ".join(meta)}</p>')
        if e.get("affiliation"):
            out.append(f'    <p class="person__meta">{e["affiliation"]}</p>')
        #  is free text for work outside the six programmes; 
        # is a programme id resolved through area_phrases.
        area = e.get("research") or (areas[e["area"]] if e.get("area") else None)
        if area:
            out.append(f'    <p class="person__area">{area}</p>')
        out.append("  </div>")
        out.append("</div>")
        return "\n".join(out)

    o = [f"""---
layout: single
title: "People"
permalink: /people/
author_profile: true
---

{BANNER}

Duality Lab is a software-engineering research group at Purdue University. Our work is
carried out by graduate and undergraduate researchers working across the lab's research
programs.

Mentorship is a central part of the lab. Graduate researchers develop independent research
programs, while undergraduate researchers participate through sustained research teams,
senior design, independent study, SURF, REU, and related programs.
"""]

    if P.get("faculty"):
        o.append("## Faculty\n")
        for e in P["faculty"]:
            o.append('<div class="person person--solo">')
            o.append(f'  <p class="person__name">{named(e)}</p>')
            o.append(f'  <p class="person__meta">{" ".join(e["role"].split())}</p>')
            if e.get("links"):
                o.append('  <p class="person__links">'
                         + " &middot; ".join(f'<a href="{l["url"]}">{l["label"]}</a>'
                                             for l in e["links"]) + "</p>")
            o.append("</div>\n")

    if P.get("graduate"):
        o.append("## Graduate researchers\n")
        o.append('<div class="people-current">')
        o += [researcher(e) for e in P["graduate"]]
        o.append("</div>\n")

    ug = P.get("undergraduate")
    if ug:
        by_label = {s["label"]: s["value"] for s in teach["undergraduate_research"]["stats"]}
        counts = {"mentored": by_label["undergraduate researchers mentored"],
                  "authors": by_label["undergraduate research authors"],
                  "senior_design": by_label["senior-design projects"]}
        o.append(f"## {ug['heading']}\n")
        o += [" ".join(x.split()).format(**counts) + "\n" for x in ug["paragraphs"]]
        if ug.get("link"):
            o.append(f"[{ug['link']['label']} →]({ug['link']['url']})\n")
        teams = ug.get("current_teams") or []
        if teams:
            o.append(f"### Current VIP team{'s' if len(teams) > 1 else ''}\n")
            for t in teams:
                title = (f'[{t["title"]}]({t["url"]})' if t.get("url") else t["title"])
                o.append(f"**{title}**  \n{' '.join(t['blurb'].split())}\n")

    if P.get("alumni_graduate"):
        # No lead sentence: "Alumni" explains itself.
        o.append("## Alumni\n")
        o.append('<ul class="alumni">')
        for e in sorted(P["alumni_graduate"], key=lambda a: (-a["year"], a["name"])):
            bits = [f'<span class="alumni__name">{named(e)}</span>'
                    f' — {e["degree"]}, {e["year"]}']
            th = theses.get(e.get("thesis_author") or "")
            if th:
                title = " ".join(th["title"].split())
                url = th.get("pdf_url")
                shown = f'<a href="{url}">{title}</a>' if url else title
                bits.append(f'<br><span class="alumni__detail">&ldquo;{shown}&rdquo;</span>')
            elif e.get("thesis"):
                bits.append('<br><span class="alumni__detail">&ldquo;'
                            + " ".join(e["thesis"].split()) + "&rdquo;</span>")
            elif e.get("area"):
                bits.append(f'<br><span class="alumni__detail">{areas[e["area"]]}</span>')
            if e.get("next_position"):
                bits.append('<br><span class="alumni__next">Next position: '
                            f'{e["next_position"]}</span>')
            o.append("  <li>" + "".join(bits) + "</li>")
        o.append("</ul>\n")
    return "\n".join(o)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page", nargs="*",
                    choices=["research", "teaching", "service", "people"], default=None)
    args = ap.parse_args(argv)
    data = load()
    want = args.page or ["research", "teaching", "service", "people"]
    fns = {"research": research, "teaching": teaching, "service": service_page,
           "people": people}
    for name in want:
        out = PAGES / f"{name}.md"
        out.write_text(fns[name](*data))
        print(f"  wrote {out.relative_to(_paths.SITE)}  ({len(out.read_text().splitlines())} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
