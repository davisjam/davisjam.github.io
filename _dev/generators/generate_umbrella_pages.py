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


ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ROOT / "repos/davisjam.github.io/_pages"

BANNER = ("<!-- Enumerative sections on this page are GENERATED from the davis-web\n"
          "     canonical records by generators/generate_umbrella_pages.py.\n"
          "     Edit the narrative in that generator, or the facts in data/*.yaml.\n"
          "     Hand edits here will be overwritten. -->")


def load():
    import yaml
    r = lambda p: yaml.safe_load((ROOT / p).read_text())
    return (r("model/sites.yaml"), r("data/publications.yaml"),
            r("data/awards.yaml"), r("data/service.yaml"), r("data/courses.yaml"),
            r("data/teaching.yaml"))


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
/* Two ancestors cap this page, measured rather than guessed (checks/layout.py
   --measure). At 1920 the grid was 770px wide at every viewport >= 1280:
     #main          max-width 1280px, auto-margins 320px a side
     article.page   padding-right 210.8px -- the Susy suffix(2 of 12), an empty
                    column reserved for a right sidebar this site does not use
   .page__inner-wrap / .page__content / .research-grid added nothing; they were
   all exactly page-width minus that padding.

   The fix widens the ANCESTORS and keeps prose narrow, rather than shrinking
   cards to fit a cap that should not apply to a full-width section. Scoped with
   :has() so only this page is affected -- no layout or theme edits. */
body:has(.research-grid) #main{max-width:min(1600px,calc(100vw - 3rem))}
body:has(.research-grid) .page{padding-right:1em}
/* Only the grid breaks out. Everything else stays at a reading measure -- prose
   at 1500px would be unreadable, which is why the cap exists in the first place. */
body:has(.research-grid) .page__content > *:not(.research-grid){max-width:48rem}
/* Generated with the page. Restrained and academic on purpose: a thin rule, no
   shadow, no rounded corners, no icons. The figures are diagrams, so the
   thumbnail uses object-fit: contain -- cropping one would destroy it. */
.research-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));
  gap:1.5rem;margin:2rem 0}
.research-card{position:relative;border:1px solid #ddd6cc;background:#fff;
  display:flex;flex-direction:column}
.research-card .thumb{background:#f6f4ef;border-bottom:1px solid #e4e0d8;
  aspect-ratio:3/2;display:block;padding:.6rem}
.research-card .thumb img{width:100%;height:100%;object-fit:contain;display:block}
.research-card .body{padding:1.25rem;display:flex;flex-direction:column;flex:1}
.research-card h2{margin:0 0 .5rem;font-size:1.2rem;line-height:1.25}
.research-card h2 a{color:inherit;text-decoration:none}
.research-question{font-style:italic;color:#57534e;margin:0 0 .6rem}
.research-card p{margin:0 0 .75rem;font-size:.95rem}
.research-card-footer{display:flex;justify-content:space-between;gap:1rem;
  align-items:baseline;margin-top:auto;padding-top:.75rem;font-size:.9rem;
  border-top:1px solid #e4e0d8}
.research-card-footer .count{color:#57534e}
/* Whole card clickable, without nesting interactive elements: the title anchor
   is stretched over the card, so the accessible name and tab order stay
   exactly one link per card. */
.research-card h2 a::after{content:"";position:absolute;inset:0}
.research-card:hover{border-color:#9a3f12}
.research-card-footer a{position:relative;z-index:1}
/* Compact example lines: indented, no bullets. Three headings each followed by
   a sentence and 2-3 lines should not read as a second bibliography. */
.other-works{margin:.4rem 0 1.4rem 1.5rem;line-height:1.75}
.other-works .venue{color:#57534e;font-size:.92rem;white-space:nowrap}
@media (max-width:760px){.research-grid{grid-template-columns:1fr}}
</style>"""


def research(sites, pubs, *_):
    order = ["mage", "embedded-swe", "failure-aware-sdlc", "ptm-se",
             "software-supply-chain", "saferegex"]
    by_pid = {s["project_id"]: s for s in sites["sites"] if s.get("project_id")}

    # SSOT for the cards. The page renders this; nothing about a programme is
    # typed into page source, so title, question, count, and figure cannot drift
    # from model/sites.yaml and data/publications.yaml.
    data = ["# GENERATED by davis-web generators/generate_umbrella_pages.py.",
            "# Source: model/sites.yaml + data/publications.yaml. Do not hand-edit.", ""]
    for pid in order:
        site = by_pid[pid]
        thesis, body = PROGRAM_COPY[pid]
        n = sum(1 for x in pubs["publications"] if pid in (x.get("projects") or []))
        fig = (site.get("figure") or {})
        cap = " ".join((fig.get("caption") or "").split())
        data += [f"- title: {yq(site['title'])}",
                 f"  short_title: {yq(site.get('short_name') or site['title'])}",
                 f"  slug: {pid}",
                 f"  question: {yq(' '.join(thesis.split()))}",
                 f"  description: {yq(' '.join(body.split()))}",
                 # Consolidated: the card links to the page in THIS site, not
                 # to a standalone project site.
                 f"  url: /research/{pid}/",
                 f"  figure: /images/research/{pid}.svg",
                 f"  figure_alt: {yq(cap)}",
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
<div class="research-grid">
{% for program in site.data.research %}
  <article class="research-card">
    <span class="thumb"><img src="{{ program.figure | relative_url }}"
         alt="{{ program.figure_alt }}" loading="lazy"></span>
    <div class="body">
      <h2><a href="{{ program.url }}">{{ program.title }}</a></h2>
      <p class="research-question">{{ program.question }}</p>
      <p>{{ program.description }}</p>
      <div class="research-card-footer">
        <a href="{{ program.url }}">Explore {{ program.short_title }} &rarr;</a>
        <span class="count">{{ program.publications }} publications</span>
      </div>
    </div>
  </article>
{% endfor %}
</div>
""")

    by_id = {p["id"]: p for p in pubs["publications"]}
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

    o.append("\n## The lab\n\n"
             "I welcome graduate and undergraduate researchers interested in software engineering, "
             "systems, security, and the engineering of AI-enabled systems.\n\n"
             "[How to join the lab →](/join-lab/)\n")
    return "\n".join(o)


# --------------------------------------------------------------------------- teaching

def teaching(sites, pubs, awards, service, courses, teach):
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
        o.append(f"### {c['number']} — {c['title']}\n")
        o += para(entry["paragraphs"])
        if entry.get("catalog_url"):
            o.append(f"[Purdue course catalog →]({entry['catalog_url']})\n")
        ins = entry.get("inset")
        if ins:
            o.append('<aside class="course-inset" markdown="1">')
            o.append(f'<p class="course-inset__eyebrow">{ins["eyebrow"]}</p>')
            o.append(f'#### {ins["title"]}\n')
            o += para(ins["paragraphs"])
            o.append(" ".join(f"[{l['label']} →]({l['url']})" for l in ins["links"]))
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
    o += stats(sot["stats"])
    o += para(sot["closing"])
    return "\n".join(o)


# --------------------------------------------------------------------------- service

def service_page(sites, pubs, awards, service, courses, teach=None):
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


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page", nargs="*", choices=["research", "teaching", "service"], default=None)
    args = ap.parse_args(argv)
    data = load()
    want = args.page or ["research", "teaching", "service"]
    fns = {"research": research, "teaching": teaching, "service": service_page}
    for name in want:
        out = PAGES / f"{name}.md"
        out.write_text(fns[name](*data))
        print(f"  wrote {out.relative_to(ROOT)}  ({len(out.read_text().splitlines())} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
