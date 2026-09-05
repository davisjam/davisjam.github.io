#!/usr/bin/env python3
"""The alignment engine: does the realization still follow from the models?

    python3 checks/alignment.py                 # all obligations
    python3 checks/alignment.py --family FUND   # one family
    python3 checks/alignment.py --errors-only
    python3 checks/alignment.py --json report.json
    python3 checks/alignment.py --list          # the obligation register

This is deliberately NOT "a collection of tests." Each check declares the
OBLIGATION it establishes, the EVIDENCE it reads, and a RESULT. The point is not
that the site builds; it is that the built site still follows from the models it
is supposed to derive from.

    MODEL -> OBLIGATIONS -> REALIZATION -> EVIDENCE -> ALIGNMENT RESULT

Severity decides what blocks:

    ERROR     the realization CONTRADICTS the authority. Wrong publication
              facts, an unmodeled funding claim, a missing required project, a
              broken canonical URL. Blocks.
    WARNING   the realization likely violates the design or writing model.
              Puffery, a banned component, prose too wide. Does not block.
    ADVISORY  worth a human look. A page grown very long, two sections that
              look semantically repetitive.

Keeping WARNING non-blocking is what stops this becoming a lint bureaucracy
agents learn to game.

Degrees of freedom this removes: an agent may freely redesign a page, but may
not silently reinterpret which projects exist, who funded them, which papers
belong to them, where they live, or what shared academic identity they
instantiate.
"""

from __future__ import annotations

import argparse
import html
import json
import pathlib
import re
import sys
from dataclasses import dataclass, field

ROOT = pathlib.Path(__file__).resolve().parent.parent
ORIGIN = "https://davisjam.github.io"

ERROR, WARNING, ADVISORY = "ERROR", "WARNING", "ADVISORY"


@dataclass
class Finding:
    obligation: str
    severity: str
    detail: str
    where: str = ""


@dataclass
class Obligation:
    id: str
    statement: str
    evidence: list[str]
    severity: str = ERROR
    findings: list[Finding] = field(default_factory=list)

    def fail(self, detail: str, where: str = "", severity: str | None = None) -> None:
        self.findings.append(Finding(self.id, severity or self.severity, detail, where))


class Engine:
    def __init__(self) -> None:
        self.obligations: list[Obligation] = []

    def obl(self, oid: str, statement: str, evidence: list[str],
            severity: str = ERROR) -> Obligation:
        o = Obligation(oid, statement, evidence, severity)
        self.obligations.append(o)
        return o


# --------------------------------------------------------------------------- helpers

def load():
    import yaml
    r = lambda p: yaml.safe_load((ROOT / p).read_text())
    return {"sites": r("model/sites.yaml"), "pubs": r("data/publications.yaml"),
            "fund": r("data/funding.yaml"), "service": r("data/service.yaml"),
            "awards": r("data/awards.yaml"), "courses": r("data/courses.yaml")}


def text_of(h: str) -> str:
    h = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)))


def rendered(fragment: str) -> str:
    """Normalize a rendered HTML fragment for comparison against source data.

    Every comparison between what a page RENDERS and what the model SAYS goes
    through here. Writing the unescape ad hoc at each site produced false
    positives twice: an href carries &amp; where the record has &, so a raw
    comparison flagged every query-string URL as a mismatch; and stray tags and
    whitespace made titles differ that were in fact identical.

    A checker that cries wolf on correct content is worse than no checker --
    people learn to skip its output, and then the true findings go unread.
    """
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", fragment)).split())


def program_sites(m) -> list[dict]:
    return [s for s in m["sites"]["sites"] if s.get("profile") == "research-program"]


def built(site: dict) -> pathlib.Path:
    return ROOT / site["path"] / "index.html"


# --------------------------------------------------------------------------- families

def scholarly(e: Engine, m) -> None:
    o = e.obl("OBL-SCHOLARLY-001",
              "Every publication modeled for a project appears on that project's site.",
              ["data/publications.yaml", "repos/*/index.html"])
    o2 = e.obl("OBL-SCHOLARLY-002",
               "A project site claims no publication that is not modeled for it.",
               ["data/publications.yaml", "repos/*/index.html"])
    o3 = e.obl("OBL-SCHOLARLY-003",
               "Rendered publication titles match the canonical record exactly.",
               ["data/publications.yaml", "repos/*/index.html"])
    for s in program_sites(m):
        f = built(s)
        if not f.exists():
            o.fail("site not built", s["id"]); continue
        page = text_of(f.read_text())
        pid = s["project_id"]
        modeled = [p for p in m["pubs"]["publications"] if pid in (p.get("projects") or [])]
        for p in modeled:
            key = " ".join(p["title"].split())[:60]
            if key.lower() not in page.lower():
                o.fail(f"{p['id']} modeled for {pid} but absent from the page", s["id"])
        titles = re.findall(r'<div class="ti">(.*?)(?:<span|</div>)',
                            f.read_text(), re.S)
        rendered_titles = {rendered(t) for t in titles}
        canon = {" ".join(p["title"].split()) for p in modeled}
        for t in rendered_titles - canon:
            o2.fail(f"page renders {t[:60]!r}, not modeled for {pid}", s["id"])
        for t in canon - rendered_titles:
            o3.fail(f"{t[:60]!r} rendered differently or missing", s["id"])


def funding(e: Engine, m) -> None:
    o = e.obl("OBL-FUND-001",
              "A site displays a funding relationship only where the model asserts it.",
              ["data/funding.yaml", "repos/*/index.html"])
    o2 = e.obl("OBL-FUND-002",
               "Every modeled grant edge appears in its project's Funding section.",
               ["data/funding.yaml", "repos/*/index.html"])
    o3 = e.obl("OBL-FUND-003",
               "No site names a sponsor absent from its modeled grant edges.",
               ["data/funding.yaml", "repos/*/index.html"])
    for s in program_sites(m):
        f = built(s)
        if not f.exists():
            continue
        pid, h = s["project_id"], f.read_text()
        modeled = [g for g in m["fund"]["grants"] if pid in (g.get("projects") or [])]
        block = re.search(r'<h2 id="support">.*?(?=<h2|<footer)', h, re.S)
        rendered = text_of(block.group(0)) if block else ""
        for g in modeled:
            if g["title"][:40].lower() not in rendered.lower():
                o2.fail(f"{g['id']} ({g['sponsor']}) modeled for {pid} but not rendered", s["id"])
        if rendered:
            allowed = {g["sponsor"].lower() for g in modeled}
            for sponsor in {"national science foundation", "google", "cisco", "socket",
                            "openai", "qualcomm", "rolls-royce", "ibm", "meta", "amazon"}:
                if sponsor in rendered.lower() and not any(sponsor in a for a in allowed):
                    o3.fail(f"names sponsor {sponsor!r} with no modeled edge", s["id"])
        elif modeled:
            o.fail(f"{len(modeled)} modeled grants but no Funding section", s["id"])


def portfolio(e: Engine, m) -> None:
    o = e.obl("OBL-PORTFOLIO-001",
              "Every active research project has exactly one entry on the root Research page.",
              ["model/sites.yaml", "repos/davisjam.github.io/_pages/research.md"])
    o2 = e.obl("OBL-PORTFOLIO-002",
               "The Research page names no project absent from the model.",
               ["model/sites.yaml", "repos/davisjam.github.io/_pages/research.md"])
    o3 = e.obl("OBL-PORTFOLIO-003",
               "Project titles on the Research page match the model exactly.",
               ["model/sites.yaml", "repos/davisjam.github.io/_pages/research.md"])
    page = ROOT / "repos/davisjam.github.io/_pages/research.md"
    cards = ROOT / "repos/davisjam.github.io/_data/research.yml"
    if not page.exists():
        o.fail("Research page missing"); return
    src = page.read_text()
    if not cards.exists():
        o.fail("_data/research.yml missing; the card grid has no source"); return

    import yaml as _y
    entries = _y.safe_load(cards.read_text()) or []
    by_slug = {e["slug"]: e for e in entries}
    if "site.data.research" not in src:
        o.fail("Research page does not render the card data")

    for s in program_sites(m):
        pid = s["project_id"]
        e = by_slug.get(pid)
        if e is None:
            o.fail(f"{pid} has no Research-page card"); continue
        if sum(1 for x in entries if x["slug"] == pid) > 1:
            o.fail(f"{pid} has more than one card")
        if e.get("title") != s["title"]:
            o3.fail(f"{pid} card title {e.get('title')!r} != model {s['title']!r}")
        if e.get("url") != s["url"]:
            o.fail(f"{pid} card URL {e.get('url')} != canonical {s['url']}")
        n = sum(1 for x in m["pubs"]["publications"] if pid in (x.get("projects") or []))
        if e.get("publications") != n:
            o.fail(f"{pid} card claims {e.get('publications')} publications, model has {n}")
        fig = ROOT / "repos/davisjam.github.io" / str(e.get("figure", "")).lstrip("/")
        if not fig.exists():
            o.fail(f"{pid} card thumbnail missing: {e.get('figure')}")
        if len((e.get("figure_alt") or "").strip()) < 20:
            o.fail(f"{pid} card thumbnail has inadequate alt text")

    modeled = {s["project_id"] for s in program_sites(m)}
    for e in entries:
        if e["slug"] not in modeled:
            o2.fail(f"card for unmodeled project {e['slug']!r}")


def routes(e: Engine, m) -> None:
    o = e.obl("OBL-ROUTE-001", "Canonical metadata uses the modeled production URL.",
              ["model/sites.yaml", "repos/*/index.html"])
    o2 = e.obl("OBL-ROUTE-002",
               "Site navigation never sends the reader to a repo or preview origin.",
               ["repos/*/index.html"])
    o3 = e.obl("OBL-ROUTE-003", "Internal links and assets resolve under the site base path.",
               ["repos/*/index.html"])
    o4 = e.obl("OBL-ROUTE-004", "No internal asset uses a root-relative path.",
               ["repos/*/index.html"])
    o5 = e.obl("OBL-ROUTE-005", "Every jump-navigation fragment resolves to a section id.",
               ["repos/*/index.html"])
    for s in program_sites(m):
        f = built(s)
        if not f.exists():
            continue
        h, base = f.read_text(), f.parent
        canon = re.search(r'<link rel="canonical" href="([^"]+)"', h)
        if not canon or canon.group(1) != s["url"]:
            o.fail(f"canonical is {canon.group(1) if canon else 'absent'}, "
                   f"expected {s['url']}", s["id"])
        # Artifact and repository links on a PAPER are correct -- an artifact
        # lives on GitHub. What this obligation guards is the reader being sent
        # off-origin by NAVIGATION: a masthead, a jump link, or a canonical URL
        # pointing at a repo page or a preview deployment.
        # From <header>, not from index 0: starting at the top swept in <head>,
        # so every stylesheet CDN read as "navigation leaving the origin".
        # The obligation is about where a READER can be sent, not where assets
        # are fetched from.
        hs, he = h.find("<header"), h.find("</header>")
        nav_zone = (h[hs:he] if hs >= 0 and he > hs else "") + h[h.find("<footer"):]
        for href in re.findall(r'href="(https?://[^"]+)"', nav_zone):
            if href.startswith(ORIGIN):
                continue
            if href.startswith(f"https://github.com/{s['repository']}"):
                continue          # the "Repository" footer link is deliberate
            o2.fail(f"navigation leaves the canonical origin: {href}", s["id"])
        for href in re.findall(r'href="(https://[a-z0-9-]+\.github\.io[^"]*)"', h):
            if not href.startswith(ORIGIN):
                o2.fail(f"foreign github.io origin: {href}", s["id"])
        for ref in re.findall(r'(?:href|src)="([^"#?]+)"', h):
            if ref.startswith(("http", "mailto:", "data:", "//", "#")):
                continue
            if ref.startswith("/"):
                o4.fail(f"root-relative path {ref!r} breaks under a base path", s["id"])
                continue
            if not (base / ref).exists():
                o3.fail(f"unresolved {ref!r}", s["id"])
        ids = set(re.findall(r'id="([^"]+)"', h))
        for frag in re.findall(r'href="#([^"]+)"', h):
            if frag not in ids:
                o5.fail(f"jump link #{frag} has no target", s["id"])


def shell(e: Engine, m) -> None:
    o = e.obl("OBL-SHELL-001",
              "Every research site instantiates the common Davis academic header.",
              ["generators/site_template.py", "repos/*/index.html"])
    o2 = e.obl("OBL-SHELL-002", "Every research site offers an obvious return to Research.",
               ["repos/*/index.html"])
    want = ["Home", "Publications", "Teaching", "Service", "About"]
    for s in program_sites(m):
        f = built(s)
        if not f.exists():
            continue
        h = f.read_text()
        if "masthead" not in h:
            o.fail("no common masthead; a project-specific shell replaced it", s["id"]); continue
        head = h[h.find("masthead"):h.find("</header>")]
        for w in want:
            if f">{w}<" not in head:
                o.fail(f"masthead missing nav item {w!r}", s["id"])
        if "masthead__logo" not in head or "logo-v2" not in head:
            o.fail("masthead does not carry the Duality Lab logo", s["id"])
        # The breadcrumb occupies the Research slot: Research > <short name>.
        if 'class="crumb"' not in head or ">Research</a>" not in head:
            o.fail("masthead lacks the Research breadcrumb", s["id"])
        if f'>{s.get("short_name", "")}<' not in head:
            o.fail(f"breadcrumb does not name this project ({s.get('short_name')})", s["id"])
        # Identity now lives in the persistent rail, not a horizontal masthead --
        # repeating it at the top is what made these read as separate sites.
        if 'class="rail"' not in h or "James Davis" not in h:
            o.fail("no identity rail carrying James Davis", s["id"])
        if "JamesDavis.jpg" not in h:
            o.fail("identity rail has no headshot", s["id"])
        if "All research" not in h and ">Research<" not in h:
            o2.fail("no return path to Research", s["id"])


def sections(e: Engine, m) -> None:
    o = e.obl("OBL-SECTION-001", "Every required section exists with a unique id.",
              ["model/sites.yaml", "repos/*/index.html"])
    o2 = e.obl("OBL-SECTION-002", "Every required section appears in the jump navigation.",
               ["repos/*/index.html"])
    o3 = e.obl("OBL-SECTION-003", "No section is rendered empty.",
               ["repos/*/index.html"], WARNING)
    for s in program_sites(m):
        f = built(s)
        if not f.exists():
            continue
        h = f.read_text()
        jump = re.search(r'<nav class="jump">(.*?)</nav>', h, re.S)
        jump_txt = jump.group(1) if jump else ""
        for sec in s.get("required_sections") or []:
            hits = h.count(f'id="{sec}"')
            if hits == 0:
                o.fail(f"required section {sec!r} missing", s["id"]); continue
            if hits > 1:
                o.fail(f"section id {sec!r} appears {hits} times", s["id"])
            if f"#{sec}" not in jump_txt:
                o2.fail(f"section {sec!r} absent from jump navigation", s["id"])
            seg = h.split(f'id="{sec}"', 1)[1]
            seg = re.split(r"<h2 ", seg)[0]
            if len(text_of(seg).strip()) < 80:
                o3.fail(f"section {sec!r} looks empty", s["id"])


def design(e: Engine, m) -> None:
    o = e.obl("OBL-DESIGN-001", "Exactly one H1 per page.", ["repos/*/index.html"])
    o2 = e.obl("OBL-DESIGN-002",
               "No institutional eyebrow above the H1 (banned component).",
               ["model/research-site-design-style.md", "repos/*/index.html"])
    o3 = e.obl("OBL-DESIGN-003",
               "The page does not close by re-announcing authorship.",
               ["repos/*/index.html"])
    EYEBROW = [r"a research programme of", r"a research project of james",
               r"a duality lab initiative", r"research initiative"]
    for s in program_sites(m):
        f = built(s)
        if not f.exists():
            continue
        h = f.read_text()
        n = len(re.findall(r"<h1[ >]", h))
        if n != 1:
            o.fail(f"{n} H1 elements", s["id"])
        low = text_of(h).lower()
        for pat in EYEBROW:
            if re.search(pat, low):
                o2.fail(f"banned institutional label matching {pat!r}", s["id"])
        foot = h[h.find('<footer'):] if "<footer" in h else ""
        if re.search(r"a research project of", text_of(foot), re.I):
            o3.fail("footer re-announces authorship", s["id"])


def prose(e: Engine, m) -> None:
    o = e.obl("OBL-PROSE-001", "No portfolio-banned institutional language.",
              ["model/research-site-writing-style.md", "repos/*/index.html"])
    o2 = e.obl("OBL-PROSE-002", "House-style discouraged vocabulary is flagged for review.",
               ["model/research-site-writing-style.md"], WARNING)
    o3 = e.obl("OBL-PROSE-003", "No self-narrating page prose.",
               ["model/research-site-writing-style.md"], WARNING)
    HARD = ["research programme", "research initiative", "at the forefront",
            "our mission", "cutting-edge", "rapidly evolving landscape"]
    SOFT = ["comprehensive", "transformative", "holistic", "pioneering", "leverages",
            "real-world impact", "innovative", "crucial", "seeks to", "aims to"]
    NARRATE = ["this page explores", "below we highlight", "in this section",
               "together, these", "this work demonstrates"]
    for s in program_sites(m):
        f = built(s)
        if not f.exists():
            continue
        low = text_of(f.read_text()).lower()
        for p in HARD:
            if p in low:
                o.fail(f"banned phrase {p!r}", s["id"])
        for p in SOFT:
            if re.search(rf"\b{re.escape(p)}\b", low):
                o2.fail(f"discouraged {p!r}", s["id"])
        for p in NARRATE:
            if p in low:
                o3.fail(f"self-narration {p!r}", s["id"])


def accessibility(e: Engine, m) -> None:
    o = e.obl("OBL-A11Y-001", "Every page declares a language.", ["repos/*/index.html"])
    o2 = e.obl("OBL-A11Y-002", "Every image carries meaningful alt text.",
               ["repos/*/index.html"])
    o3 = e.obl("OBL-A11Y-003", "Heading hierarchy does not skip levels.",
               ["repos/*/index.html"], WARNING)
    o4 = e.obl("OBL-A11Y-004", "Every figure has a caption or adjacent explanation.",
               ["repos/*/index.html"])
    o5 = e.obl("OBL-A11Y-005", "Embedded SVG figures expose a title and description.",
               ["repos/*/figures/*.svg"])
    for s in program_sites(m):
        f = built(s)
        if not f.exists():
            continue
        h = f.read_text()
        if not re.search(r"<html[^>]+lang=", h):
            o.fail("no lang attribute", s["id"])
        for img in re.findall(r"<img[^>]*>", h):
            alt = re.search(r'alt="([^"]*)"', img)
            if not alt:
                o2.fail("image without alt", s["id"]); continue
            txt = alt.group(1).strip()
            # A logo or headshot is correctly named, not described. The
            # length rule applies to CONTENT images -- figures.
            is_identity = any(k in img for k in ("logo-v2", "JamesDavis.jpg"))
            if not txt:
                o2.fail("image with empty alt", s["id"])
            elif not is_identity and len(txt) < 15:
                o2.fail(f"content image alt too short: {txt!r}", s["id"])
        levels = [int(x) for x in re.findall(r"<h([1-6])[ >]", h)]
        for a, b in zip(levels, levels[1:]):
            if b > a + 1:
                o3.fail(f"heading jumps h{a} -> h{b}", s["id"])
        if "<figure" in h and "<figcaption" not in h:
            o4.fail("figure without a caption", s["id"])
        for svg in (ROOT / s["path"] / "figures").glob("*.svg"):
            t = svg.read_text()
            if "<title" not in t or "<desc" not in t:
                o5.fail(f"{svg.name} lacks <title>/<desc>", s["id"])


def seo(e: Engine, m) -> None:
    o = e.obl("OBL-SEO-001", "Every page has a unique, descriptive title naming the site.",
              ["repos/*/index.html"])
    o2 = e.obl("OBL-SEO-002", "Every page declares description and OpenGraph metadata.",
               ["repos/*/index.html"])
    o3 = e.obl("OBL-SEO-003", "No page is accidentally noindexed.", ["repos/*/index.html"])
    seen: dict[str, str] = {}
    for s in program_sites(m):
        f = built(s)
        if not f.exists():
            continue
        h = f.read_text()
        t = re.search(r"<title>(.*?)</title>", h, re.S)
        if not t:
            o.fail("no <title>", s["id"])
        else:
            title = rendered(t.group(1))
            if title in seen:
                o.fail(f"title collides with {seen[title]}: {title!r}", s["id"])
            seen[title] = s["id"]
            author = re.search(r'<meta name="author" content="([^"]*)"', h)
            if "Davis" not in title and not (author and "Davis" in author.group(1)):
                o.fail("neither title nor author metadata carries the author name",
                       s["id"], WARNING)
        for tag in ['name="description"', 'property="og:title"',
                    'property="og:url"', 'property="og:description"']:
            if tag not in h:
                o2.fail(f"missing {tag}", s["id"])
        if "noindex" in h:
            o3.fail("page declares noindex", s["id"])


def provenance(e: Engine, m) -> None:
    o = e.obl("OBL-PROV-001",
              "Generated collections originate from the generator, not hand-typed markup.",
              ["generators/", "repos/*/index.html"])
    o2 = e.obl("OBL-PROV-002", "Generated assets declare their provenance.",
               ["repos/*/assets/site.css"])
    for s in program_sites(m):
        css = ROOT / s["path"] / "assets/site.css"
        if css.exists() and "GENERATED" not in css.read_text()[:400]:
            o2.fail("site.css carries no provenance header", s["id"])
        f = built(s)
        if f.exists() and '<div class="bib">' not in f.read_text():
            o.fail("no generated bibliography block; list may be hand-typed", s["id"])


def crosssite(e: Engine, m) -> None:
    o = e.obl("OBL-CROSS-001",
              "A cross-listed work renders identical bibliographic facts on every site.",
              ["data/publications.yaml", "repos/*/index.html"])
    o2 = e.obl("OBL-CROSS-002",
               "A cross-listed work carries a DIFFERENT program note on each site.",
               ["data/program-notes.yaml"], WARNING)
    multi = [p for p in m["pubs"]["publications"] if len(p.get("projects") or []) > 1]
    for p in multi:
        notes = p.get("program_notes") or {}
        vals = [notes.get(pr) for pr in p["projects"]]
        if all(vals) and len(set(vals)) == 1:
            o2.fail(f"{p['id']} repeats one note across {p['projects']}")
        for pr in p["projects"]:
            site = next((s for s in program_sites(m) if s["project_id"] == pr), None)
            if not site:
                continue
            f = built(site)
            if f.exists() and " ".join(p["title"].split())[:50].lower() not in text_of(f.read_text()).lower():
                o.fail(f"{p['id']} missing from {pr}", site["id"])


def records(e: Engine, m) -> None:
    o = e.obl("OBL-RECORD-001",
              "Umbrella pages render enumerative records, never hand-maintained lists.",
              ["model/ssot-records.md", "repos/davisjam.github.io/_pages/*.md"])
    o2 = e.obl("OBL-RECORD-002", "Every canonical service record reaches the Service page.",
               ["data/service.yaml", "repos/davisjam.github.io/_pages/service.md"])
    o3 = e.obl("OBL-RECORD-003", "Course numbers on the Teaching page match the model.",
               ["data/courses.yaml", "repos/davisjam.github.io/_pages/teaching.md"])
    pages = ROOT / "repos/davisjam.github.io/_pages"
    for name in ("research", "teaching", "service"):
        f = pages / f"{name}.md"
        if not f.exists():
            o.fail(f"{name}.md missing"); continue
        if "GENERATED" not in f.read_text():
            o.fail(f"{name}.md carries no generated-content banner")
    svc = pages / "service.md"
    if svc.exists():
        t = svc.read_text()
        for pc in m["service"]["research_community"]["major_program_committees"]:
            if pc["venue"] not in t:
                o2.fail(f"program committee {pc['venue']!r} not rendered")
        for j in m["service"]["research_community"]["journals"]:
            if j.split("(")[0].strip() not in t:
                o2.fail(f"journal {j!r} not rendered")
    tch = pages / "teaching.md"
    if tch.exists():
        t = tch.read_text()
        for c in m["courses"]["courses"]:
            if c.get("featured") and c.get("number") and c["number"] not in t:
                o3.fail(f"featured course {c['number']} absent from Teaching")
            if c.get("legacy_number") and c.get("featured") and c["legacy_number"] in t:
                o3.fail(f"obsolete course number {c['legacy_number']} still published")


def links(e: Engine, m) -> None:
    """Whenever a specific paper is NAMED, its title links to a readable copy."""
    o = e.obl("OBL-LINK-001",
              "Every rendered publication title with a known paper_url is a link.",
              ["data/publications.yaml", "repos/*/index.html"])
    o2 = e.obl("OBL-LINK-002",
               "No page constructs its own paper link; all resolve from paper_url.",
               ["data/publications.yaml", "repos/*/index.html"])
    o3 = e.obl("OBL-LINK-003", "Every author-hosted paper PDF exists.",
               ["data/publications.yaml", "repos/davisjam.github.io/files/"])
    o4 = e.obl("OBL-LINK-004", "Every peer-reviewed publication has a paper_url.",
               ["data/publications.yaml"], WARNING)
    o5 = e.obl("OBL-LINK-005", "No malformed paper_url.", ["data/publications.yaml"])

    pubs = m["pubs"]["publications"]
    by_title = {" ".join(p["title"].split()): p for p in pubs}
    umbrella = ROOT / "repos/davisjam.github.io"

    for s in program_sites(m):
        f = built(s)
        if not f.exists():
            continue
        h = f.read_text()
        for block in re.findall(r'<div class="ti">(.*?)</div>', h, re.S):
            title = rendered(block)
            title = re.sub(r"\s*(Best Paper|Best Artifact|Distinguished.*)$", "", title).strip()
            rec = by_title.get(title)
            if rec and rec.get("paper_url") and "<a href" not in block:
                o.fail(f"{rec['id']} title rendered unlinked despite a known url", s["id"])
            if rec and "<a href" in block:
                href = re.search(r'href="([^"]+)"', block)
                # Unescape first: a rendered href carries &amp; where the record
                # has &, so a raw comparison flags every query-string URL.
                got = html.unescape(href.group(1)) if href else None  # href: entities only
                if got and rec.get("paper_url") and got != rec["paper_url"]:
                    o2.fail(f"{rec['id']} links {got}, canonical is {rec['paper_url']}",
                            s["id"])

    for p in pubs:
        u = p.get("paper_url")
        if not u:
            if p.get("type") in ("conference", "journal", "workshop", "magazine"):
                o4.fail(f"{p['id']} ({p.get('type')}) has no paper_url: {p['title'][:52]}")
            continue
        local = str(u).replace("https://davisjam.github.io/", "")
        if local.startswith("files/"):
            if not (umbrella / local).exists():
                o3.fail(f"{p['id']} points at a missing hosted PDF: {u}")
        elif not str(u).startswith(("http://", "https://")):
            o5.fail(f"{p['id']} paper_url is neither absolute nor site-rooted: {u}")
        elif " " in str(u) or str(u).count("http") > 1:
            o5.fail(f"{p['id']} malformed paper_url: {u[:60]}")


FAMILIES = {
    "LINK": links,
    "SCHOLARLY": scholarly, "FUND": funding, "PORTFOLIO": portfolio, "ROUTE": routes,
    "SHELL": shell, "SECTION": sections, "DESIGN": design, "PROSE": prose,
    "A11Y": accessibility, "SEO": seo, "PROV": provenance, "CROSS": crosssite,
    "RECORD": records,
}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--family", action="append", choices=sorted(FAMILIES))
    ap.add_argument("--errors-only", action="store_true")
    ap.add_argument("--json", metavar="PATH")
    ap.add_argument("--list", action="store_true", help="print the obligation register")
    args = ap.parse_args(argv)

    m = load()
    e = Engine()
    for name, fn in FAMILIES.items():
        if args.family and name not in args.family:
            continue
        fn(e, m)

    if args.list:
        for o in e.obligations:
            print(f"  {o.id:<22} [{o.severity:<8}] {o.statement}")
            print(f"  {'':<22} evidence: {', '.join(o.evidence)}")
        return 0

    all_f = [f for o in e.obligations for f in o.findings]
    errs = [f for f in all_f if f.severity == ERROR]
    warns = [f for f in all_f if f.severity == WARNING]
    advs = [f for f in all_f if f.severity == ADVISORY]

    print("== alignment: does the realization follow from the models? ==\n")
    for o in e.obligations:
        if not o.findings:
            print(f"  PASS   {o.id:<22} {o.statement[:66]}")
    print()
    for group, label in ((errs, ERROR), (warns, WARNING), (advs, ADVISORY)):
        if args.errors_only and label != ERROR:
            continue
        if not group:
            continue
        print(f"  ---- {label} ({len(group)}) ----")
        for f in group:
            loc = f" [{f.where}]" if f.where else ""
            print(f"  {f.obligation}{loc}: {f.detail}")
        print()

    print(f"  {len(e.obligations)} obligations · "
          f"{len(e.obligations) - len({f.obligation for f in all_f})} passing · "
          f"{len(errs)} ERROR · {len(warns)} WARNING · {len(advs)} ADVISORY")

    if args.json:
        pathlib.Path(args.json).write_text(json.dumps(
            {"obligations": [{"id": o.id, "statement": o.statement, "severity": o.severity,
                              "evidence": o.evidence,
                              "findings": [f.__dict__ for f in o.findings]}
                             for o in e.obligations]}, indent=1))
        print(f"  report -> {args.json}")

    return 1 if errs else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
