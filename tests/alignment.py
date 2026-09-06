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

import _frontmatter
import _sitepath
import re
import sys
from dataclasses import dataclass, field

ROOT, SITE, DATA_DIR = _sitepath.ROOT, _sitepath.SITE, _sitepath.DATA
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
    r = lambda p: yaml.safe_load(pathlib.Path(p).read_text())
    # Resolved through _sitepath so this works from the orchestrator and from
    # the copy inside the site; `r` takes an absolute path now, not a
    # root-relative string.
    M = DATA_DIR.parent / "model"
    return {"sites": r(M / "sites.yaml"), "pubs": r(DATA_DIR / "publications.yaml"),
            "fund": r(DATA_DIR / "funding.yaml"), "service": r(DATA_DIR / "service.yaml"),
            "awards": r(DATA_DIR / "awards.yaml"), "courses": r(DATA_DIR / "courses.yaml")}


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
    """Programmes, whether or not their standalone site still exists."""
    return [s for s in m["sites"]["sites"] if s.get("profile") == "research-program"]


def live_sites(m) -> list[dict]:
    """Programmes whose STANDALONE SITE is still the published artifact.

    After consolidation the programme pages live in the umbrella site, so the
    families that validate a standalone site (routes, shell, sections, design,
    SEO, provenance) have nothing to assert about the retired repos. STRUCT and
    the figure sensors still read those repos, because the authored figures
    live there until the repos are deleted.
    """
    return [s for s in program_sites(m) if s.get("site_status") != "retired"]


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
    for s in live_sites(m):
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
    # OBL-FUND-004: every grant is dated, and the dates are ordered.
    #
    # Nine of twenty-four -- every NSF-numbered award, CAREER and AIGIS among
    # them -- carried no start year. Nothing renders wrong today because nothing
    # sorts on it; the funders rail groups by sponsor. But a null start is a
    # defect waiting for the first date-ordered view, and it would sort the two
    # largest awards to the bottom or drop them. Dates come from CV-40's
    # EXTERNAL GRANTS blocks, which state a span for every award.
    o4 = e.obl("OBL-FUND-004",
               "Every grant carries an ordered date span.",
               ["data/funding.yaml"])
    for g in m["fund"]["grants"]:
        start, end = g.get("start"), g.get("end")
        if not start:
            o4.fail(f"{g['id']} has no start year -- any date-ordered view "
                    f"mis-sorts or drops it: {str(g.get('title'))[:44]}")
        elif end and end < start:
            o4.fail(f"{g['id']} ends ({end}) before it starts ({start})")

    for s in live_sites(m):
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
    page = SITE / "_pages/research.md"
    cards = SITE / "_data/research.yml"
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
        card_url, canon = e.get("url", ""), s["url"]
        if card_url.replace(ORIGIN, "") != canon.replace(ORIGIN, ""):
            o.fail(f"{pid} card URL {card_url} != canonical {canon}")
        n = sum(1 for x in m["pubs"]["publications"] if pid in (x.get("projects") or []))
        if e.get("publications") != n:
            o.fail(f"{pid} card claims {e.get('publications')} publications, model has {n}")
        fig = SITE / str(e.get("figure", "")).lstrip("/")
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
    for s in live_sites(m):
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
    for s in live_sites(m):
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
    for s in live_sites(m):
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
    for s in live_sites(m):
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
    for s in live_sites(m):
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
    for s in live_sites(m):
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
    for s in live_sites(m):
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
    for s in live_sites(m):
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


def publications_page(e: Engine, m) -> None:
    """Every record in the canonical file reaches the Publications page.

    auto-publications.md was named "auto" but nothing generated it. It was
    frozen output from the theme's old markdown_generator/publications.json and
    had drifted 26 records behind -- missing both books and four of the seven
    current technical reports. The site's most enumerative page was the one page
    still hand-maintained. It is generated now; this keeps it that way.
    """
    import yaml as _y
    o = e.obl("OBL-PUBS-001",
              "The Publications page renders every record in publications.yaml.",
              ["_dev/data/publications.yaml", "auto-publications.md"])
    site = SITE
    page = site / "auto-publications.md"
    if not page.exists():
        o.fail("auto-publications.md is missing"); return
    text = rendered(page.read_text()).lower()
    if "generated by" not in page.read_text().lower():
        o.fail("auto-publications.md carries no generated-content banner")
    pubs = _y.safe_load((site / "_dev/data/publications.yaml").read_text())["publications"]
    absent = [p for p in pubs
              if " ".join(p["title"].split()).lower()[:48] not in text]
    for p in absent[:8]:
        o.fail(f"{p['id']} is in the record but not on the page: {p['title'][:46]}")
    if len(absent) > 8:
        o.fail(f"...and {len(absent) - 8} more records absent from the page")
    theses = _y.safe_load((site / "_dev/data/theses.yaml").read_text())["theses"]
    for t in theses:
        if " ".join(t["title"].split()).lower()[:48] not in text:
            o.fail(f"thesis absent from the page: {t['title'][:46]}")

    # Same family, so it runs from here: PUBS maps to a single function.
    patents(e, m)


def patents(e: Engine, m) -> None:
    """A patent is identified by its number; the URL is a function of it.

    These records used to carry patent_number AND paper_url AND links.record --
    three surfaces for one fact -- and they disagreed. Three of eight cited a
    SIBLING continuation: same title, real grant, different number. Every URL
    resolved and every title matched, so nothing looked wrong from the page, and
    only comparing against CV-40 showed it. A fourth had a URL and no number,
    and that got written down as an open question for James when the answer was
    inside the URL.

    Storing the number alone and deriving the link makes disagreement
    impossible, so what remains to enforce is that nobody puts a URL back.
    """
    o = e.obl("OBL-PUBS-002",
              "Patents store a number, not a hand-written URL.",
              ["data/publications.yaml", "generators/generate_publications_page.py"])
    import yaml as _y
    pubs = _y.safe_load((DATA_DIR / "publications.yaml").read_text())["publications"]
    # A peer-reviewed record has to say WHERE and WHEN. C-1 and C-2 -- the CCS
    # and ASE papers, the two newest and most selective on the list -- carried a
    # title and an author string and nothing else, so the page printed them as
    # bare titles while every neighbour showed its venue. Nothing looked broken;
    # they just quietly read as less than they are.
    for rec in pubs:
        if rec.get("type") not in ("conference", "journal", "workshop"):
            continue
        for field in ("venue", "year"):
            if not rec.get(field):
                o.fail(f"{rec['id']} ({rec.get('type')}) has no {field} -- it "
                       f"prints as a bare title: {str(rec.get('title'))[:44]}")

    for p in (x for x in pubs if str(x.get("id", "")).startswith("Pa-")):
        pid = p["id"]
        for field, val in (("paper_url", p.get("paper_url")),
                           ("links", p.get("links"))):
            if val and "patents.google.com" in str(val):
                o.fail(f"{pid} hand-writes a patents.google.com URL in {field} -- "
                       f"store patent_number and let the generator derive it")
        # A provisional application is not published, so it has a serial and no
        # page. Requiring a grant number would be wrong; requiring one or the
        # other is what catches a record with neither.
        if not p.get("patent_number") and not p.get("application_number"):
            o.fail(f"{pid} has neither patent_number nor application_number -- "
                   f"nothing identifies it and no link can be derived")
        num = p.get("patent_number")
        if num and not re.fullmatch(r"[A-Z]{2}\d+[A-Z]\d?", str(num)):
            o.fail(f"{pid} patent_number {num!r} is not a grant number -- "
                   f"a derived URL would 404")


def self_sufficient(e: Engine, m) -> None:
    """The site must be able to regenerate itself with no external repo.

    The generators and the authored records used to live only in the private
    davis-web orchestrator, which is scheduled for deletion. Deleting it while
    it held them would have left this site able to RENDER but not to
    REGENERATE -- every page still serving, and no page ever changeable at its
    source again. That is a failure mode with no symptom until someone tries to
    edit something, so it gets an obligation rather than a note.
    """
    o = e.obl("OBL-SELF-001",
              "The site carries its own generators, models and authored records.",
              ["repos/davisjam.github.io/_dev/"])
    dev = SITE / "_dev"
    # The checks must RUN from inside the site, not merely be present: each one
    # hardcoded SITE = ROOT/"repos/davisjam.github.io", correct from the
    # orchestrator and wrong from here, and a11y.py's tool-absent skip turned
    # that into a silent pass on the accessibility gate.
    for chk in ("a11y.py", "alignment.py", "layout.py", "links.py", "syntax.py",
                "news_refs.py", "_sitepath.py", "_frontmatter.py"):
        if not (SITE / "tests" / chk).exists():
            o.fail(f"tests/{chk} is missing -- the site cannot check itself")
    sp = SITE / "tests/_sitepath.py"
    if sp.exists() and 'root / "repos/davisjam.github.io"' not in sp.read_text():
        o.fail("tests/_sitepath.py no longer detects the orchestrator layout")

    # PRESENCE IS NOT ENOUGH -- the resolver has to actually be used. layout.py
    # shipped in tests/, imported nothing, computed its own ROOT and then globbed
    # ROOT/"repos/davisjam.github.io/_pages". From inside the site that directory
    # does not exist, so the glob returned nothing, the sweep silently narrowed
    # to the home page, and it reported "no overflow" across 1 page rather than
    # 14. A green run over almost no pages, which is worse than a red one.
    #
    # So the path literal is banned everywhere except the resolver that has to
    # know it. Checked as text because the failure is textual: a hardcoded path
    # that happens to be right from one working directory.
    # PARSED, not searched. Two textual attempts failed in opposite directions:
    # a plain substring search flagged the comments explaining why not to use the
    # path, and skipping comments and string tokens to fix that removed the
    # literal the defect actually lives in -- so it passed a deliberately
    # reintroduced bug. The distinction is not comment-vs-code, it is "a string
    # used to build a path" vs "a string that talks about one", which no amount
    # of grepping separates.
    #
    # The AST separates them exactly: a pathlib path is built with the / operator,
    # so ROOT / "repos/davisjam.github.io/_pages" is a BinOp whose right operand
    # is that literal, while prose and failure messages never are.
    import ast
    for chk in sorted((SITE / "tests").glob("*.py")):
        if chk.name == "_sitepath.py":
            continue        # the resolver is the one file that must know the path
        try:
            tree = ast.parse(chk.read_text(errors="replace"))
        except SyntaxError:
            continue        # syntax.py is the gate for that, not this obligation
        for node in ast.walk(tree):
            if not (isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div)
                    and isinstance(node.right, ast.Constant)
                    and isinstance(node.right.value, str)):
                continue
            lit = node.right.value
            base = node.left.id if isinstance(node.left, ast.Name) else None
            if "repos/davisjam.github.io" in lit:
                o.fail(f"tests/{chk.name}:{node.lineno} builds a path from "
                       f"{lit!r} -- use _sitepath.SITE, or it silently scans "
                       f"nothing when run from inside the site")
            # ROOT is the one anchor that MEANS something different in each
            # layout, so a literal hung off it is the bug. news_refs.py read
            # ROOT/"data/news.yaml" and had therefore never once run in-site;
            # it raised FileNotFoundError the first time anyone tried. The
            # first version of this check only banned the repos/ literal and
            # sailed straight past it, which is why it is generalised here.
            elif base == "ROOT" and lit.split("/")[0] in ("data", "model", "generators"):
                o.fail(f"tests/{chk.name}:{node.lineno} builds a path from "
                       f"ROOT / {lit!r} -- ROOT differs between layouts; "
                       f"use _sitepath.DATA or _sitepath.SITE")

    # EVERY FILE A SHIPPED GENERATOR READS MUST SHIP WITH IT.
    #
    # The generators moved into _dev so the site could rebuild itself without
    # davis-web. Their DATA did not entirely follow: abstracts.json,
    # cv-extract.json, openalex-cache.json and patents-verification.md stayed
    # behind, referenced by build_publications.py, enrich_openalex.py and
    # fetch_abstracts.py. Nothing failed, because those are refresh tools rather
    # than page builders and nobody had run them from here -- the breakage was
    # scheduled for whenever davis-web was deleted and someone next needed to
    # re-derive publications.
    #
    # Checked by reading the generators rather than by listing expected files:
    # a hand-kept list is the thing that goes stale, and this is the same
    # false-green shape as a check that scans nothing.
    import re as _re
    for gen in sorted((dev / "generators").glob("*.py")):
        # Slashes allowed. The first version matched only bare filenames, which
        # happened to work because the generators had just been converted to
        # DATA / "file.json" -- a nested DATA / "sub/file.json" would have
        # slipped straight past. A control that passes because of an unrelated
        # cleanup is not a control.
        for m in _re.finditer(r'"([\w./-]+\.(?:json|yaml))"', gen.read_text()):
            name = m.group(1).rsplit("/", 1)[-1]
            # rglob on the SITE, not glob. publications.json lives at
            # markdown_generator/publications.json -- present, but invisible to
            # a top-level-only search, so the check reported a file as missing
            # that was sitting right there. A control that cries wolf gets
            # ignored exactly as fast as one that sleeps.
            here = [q for q in SITE.rglob(name)
                    if "node_modules" not in q.parts and ".git" not in q.parts]
            if not list(dev.rglob(name)) and not here:
                o.fail(f"_dev/generators/{gen.name} reads {name}, which is not "
                       f"in the site -- it would break once davis-web is gone")

    for need in ("generators/_paths.py", "generators/generate_umbrella_pages.py",
                 "generators/generate_research_pages.py", "model/sites.yaml",
                 "figure-toolkit/check_figures.py", "README.md"):
        if not (dev / need).exists():
            o.fail(f"_dev/{need} is missing -- the site cannot regenerate itself")
    # every record the generators read must be present here, not only upstream
    import re as _re
    referenced = set()
    for g in (dev / "generators").glob("*.py"):
        referenced |= set(_re.findall(r'_paths\.DATA / "([a-z-]+\.yaml)"', g.read_text()))
    for name in sorted(referenced):
        if not (dev / "data" / name).exists():
            o.fail(f"_dev/data/{name} is referenced by a generator but absent")
    if not referenced:
        o.fail("no data records resolved from the generators -- check the parse")


def signature_figures(e: Engine, m) -> None:
    """One drawing per programme, resolved identically everywhere.

    Added 260905 after the landing page was found rendering
    /images/research/<pid>.svg -- hand-copied duplicates of the real figures.
    Four of six had drifted, and the regex entry was still showing the
    chronological arc long after the page moved to the microscope figure. A
    signature figure is ONE artifact; a second independently-editable copy of it
    is a bug, not an optimisation.
    """
    import yaml as _y
    o = e.obl("OBL-FIG-001",
              "Landing and programme page resolve the same signature-figure file.",
              ["repos/davisjam.github.io/_data/research.yml",
               "repos/davisjam.github.io/_pages/research-*.md"])
    site = SITE
    rec = _y.safe_load((site / "_data/research.yml").read_text()) or []
    for prog in rec:
        pid, landing = prog["slug"], prog.get("figure")
        if not landing:
            o.fail(f"{pid}: landing record names no signature figure"); continue
        if not (site / landing.lstrip("/")).exists():
            o.fail(f"{pid}: landing figure {landing} does not exist")
        page = site / f"_pages/research-{pid}.md"
        if not page.exists():
            o.fail(f"{pid}: no programme page"); continue
        fm = _frontmatter.load(page) or {}
        if fm.get("figure") != landing:
            o.fail(f"{pid}: landing shows {landing}, page shows {fm.get('figure')} "
                   f"-- a signature figure must be one artifact")
    # A hand-maintained thumbnail directory is exactly how the drift happened.
    if (site / "images/research").exists():
        o.fail("images/research/ exists again -- thumbnails must derive from "
               "assets/research/, not be copied beside them")


def records(e: Engine, m) -> None:
    o = e.obl("OBL-RECORD-001",
              "Umbrella pages render enumerative records, never hand-maintained lists.",
              ["model/ssot-records.md", "repos/davisjam.github.io/_pages/*.md"])
    # The Service page is a SELECTION over an exhaustive record, not a rendering
    # of all of it (James, 260905). So the guarantee is no longer "everything is
    # on the page" -- it is "nothing left the page by accident": each bucket is
    # either fully rendered, or named in service.yaml's `record_only` with a
    # reason. That keeps the original protection (no silent record loss) while
    # allowing the page to be edited.
    o2 = e.obl("OBL-RECORD-002",
               "Every canonical service record is rendered, or declared record-only with a reason.",
               ["data/service.yaml", "repos/davisjam.github.io/_pages/service.md"])
    o3 = e.obl("OBL-RECORD-003", "Course numbers on the Teaching page match the model.",
               ["data/courses.yaml", "repos/davisjam.github.io/_pages/teaching.md"])
    pages = SITE / "_pages"
    for name in ("research", "teaching", "service"):
        f = pages / f"{name}.md"
        if not f.exists():
            o.fail(f"{name}.md missing"); continue
        if "GENERATED" not in f.read_text():
            o.fail(f"{name}.md carries no generated-content banner")
    svc = pages / "service.md"
    if svc.exists():
        t = svc.read_text()
        declared = m["service"].get("record_only") or {}
        for path, reason in declared.items():
            if len(" ".join(str(reason).split())) < 40:
                o2.fail(f"record_only {path!r} needs a real reason, not {reason!r}")
        def bucket(path):
            cur = m["service"]
            for k in path.split("."):
                cur = cur[k]
            return cur
        # A venue may render under its short name (ESEC/FSE -> FSE); that is
        # rendered, not missing.
        for pc in bucket("research_community.major_program_committees"):
            if pc["venue"] not in t and pc.get("short", pc["venue"]) not in t:
                o2.fail(f"program committee {pc['venue']!r} not rendered")
        for path in ("research_community.journals", "research_community.other_refereeing",
                     "purdue.additional"):
            if path in declared:
                continue
            for item in bucket(path):
                label = item if isinstance(item, str) else (item.get("venue") or item["what"])
                if label.split("(")[0].strip() not in t:
                    o2.fail(f"{path} entry {label!r} is neither rendered nor declared record-only")
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
    # Titles are NOT unique: a work can appear as both a book and its arXiv
    # version (B-1 and R-1 are both "Model-Based Agentic Software
    # Engineering"), or as a poster and a preprint. Resolving a rendered link
    # by title alone then blames whichever record lost the dict race for
    # linking "wrongly". Keep every record per title and accept a link that
    # matches ANY of them.
    by_title: dict[str, list] = {}
    for p in pubs:
        by_title.setdefault(" ".join(p["title"].split()), []).append(p)
    umbrella = SITE

    for s in program_sites(m):
        f = built(s)
        if not f.exists():
            continue
        h = f.read_text()
        for block in re.findall(r'<div class="ti">(.*?)</div>', h, re.S):
            title = rendered(block)
            title = re.sub(r"\s*(Best Paper|Best Artifact|Distinguished.*)$", "", title).strip()
            recs = by_title.get(title) or []
            urls = [r["paper_url"] for r in recs if r.get("paper_url")]
            if urls and "<a href" not in block:
                o.fail(f"{recs[0]['id']} title rendered unlinked despite a known url", s["id"])
            if recs and "<a href" in block:
                href = re.search(r'href="([^"]+)"', block)
                # Unescape first: a rendered href carries &amp; where the record
                # has &, so a raw comparison flags every query-string URL.
                got = html.unescape(href.group(1)) if href else None  # href: entities only
                if got and urls and got not in urls:
                    o2.fail(f"{'/'.join(r['id'] for r in recs)} links {got}, "
                            f"canonical is one of {urls}", s["id"])

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

    # Same family: LINK maps to a single function.
    external_consumers(e, m)


def external_consumers(e: Engine, m) -> None:
    """Assets another site references must not move without warning.

    The MAGE site reaches the lab logo at the full URI
    https://davisjam.github.io/images/logo.svg -- one file, no copy, no sync
    step. The full form rather than a root-absolute path because the latter
    404s under a local preview server, and a logo that looks broken through
    every development session invites someone to vendor a copy.

    The cost of the arrangement is a dependency pointing the wrong way for
    enforcement: the consumer holds the controls, the producer has none. Rename
    this file and the other site renders a broken image, with nothing here
    failing. So the producer side is pinned too. It is the only signal that
    would reach whoever does the renaming, and it costs one stat call.
    """
    o = e.obl("OBL-LINK-006",
              "Assets other sites reference stay where those sites expect them.",
              ["images/logo.svg"])
    for rel, who in (("images/logo.svg", "the MAGE site header"),):
        if not (SITE / rel).is_file():
            o.fail(f"{rel} is missing or moved -- {who} references it at "
                   f"/{rel} and would render a broken image")


def structure(e: Engine, m) -> None:
    """The figure and the page body must name the same things."""
    o = e.obl("OBL-STRUCT-001",
              "Every programme section heading appears on its page.",
              ["data/program-structure.yaml", "repos/davisjam.github.io/_pages/research-*.md"])
    o2 = e.obl("OBL-STRUCT-002",
               "Every declared figure_label appears in that programme's figure.",
               ["data/program-structure.yaml", "repos/*/figures/*.svg"])
    o3 = e.obl("OBL-STRUCT-003",
               "Every publication in a programme is placed under exactly one section.",
               ["data/program-structure.yaml", "data/publications.yaml"])

    import yaml as _y
    spec = _y.safe_load((DATA_DIR / "program-structure.yaml").read_text())["programs"]
    pages = SITE / "_pages"
    for site in program_sites(m):
        pid = site["project_id"]
        prog = spec.get(pid)
        if not prog:
            o.fail(f"{pid} has no declared structure"); continue

        page = pages / f"research-{pid}.md"
        body = page.read_text() if page.exists() else ""
        fid = (site.get("figure") or {}).get("id")
        figp = ROOT / site["path"] / "figures" / f"{fid}.svg"
        # Unescape: the SVG carries &amp; where the model has &, so a raw
        # comparison reports a mismatch that does not exist.
        fig = html.unescape(figp.read_text()) if figp.exists() else ""

        placed: list[str] = []
        for sec in prog["sections"]:
            if body and f"## {sec['title']}" not in body:
                o.fail(f"{pid}: section {sec['title']!r} not on the page")
            label = sec.get("figure_label")
            if label and fig and label not in fig:
                o2.fail(f"{pid}: figure does not carry {label!r} "
                        f"(section {sec['title']!r})")
            placed += sec["publications"]

        modeled = {p["id"] for p in m["pubs"]["publications"]
                   if pid in (p.get("projects") or [])}
        for x in sorted(modeled - set(placed)):
            o3.fail(f"{pid}: {x} is modeled for the programme but placed under no section")
        for x in sorted(set(placed) - modeled):
            o3.fail(f"{pid}: {x} is placed but not modeled for the programme")
        dupes = {x for x in placed if placed.count(x) > 1}
        for x in sorted(dupes):
            o3.fail(f"{pid}: {x} appears under more than one section")


def deployed(e: Engine, m) -> None:
    """Is the published site actually the site in this repository?

    Added after a Liquid syntax error made every build fail for several commits
    while production quietly served a stale site. Nothing noticed: every other
    family reads the REPO, so they stayed green on files that had never become a
    website. This is the only obligation that compares the deployment against
    the source.

    Network-dependent, so it is opt-in: run with --family DEPLOY.
    """
    o = e.obl("OBL-DEPLOY-001",
              "Each published page serves the content currently in this repository.",
              ["data/program-structure.yaml", "https://davisjam.github.io/research/*/"])

    import subprocess
    import yaml as _y
    spec = _y.safe_load((DATA_DIR / "program-structure.yaml").read_text())["programs"]
    for site in program_sites(m):
        pid = site["project_id"]
        want = (spec.get(pid) or {}).get("sections") or []
        if not want:
            continue
        url = f"{ORIGIN}/research/{pid}/"
        r = subprocess.run(["curl", "-s", "--max-time", "25", url],
                           capture_output=True, text=True)
        if r.returncode != 0 or not r.stdout.strip():
            o.fail(f"{pid}: {url} did not respond"); continue
        served = rendered(r.stdout)
        # A heading that exists here but not there means the build did not run,
        # or ran and failed, and the site is older than the repository.
        missing = [s["title"] for s in want if s["title"] not in served]
        if missing:
            o.fail(f"{pid}: served page is STALE -- missing {missing[0]!r} "
                   f"({len(missing)} of {len(want)} sections absent)")


OPT_IN = {"DEPLOY"}          # network-dependent; see main()

FAMILIES = {
    "DEPLOY": deployed,
    "FIG": signature_figures,
    "SELF": self_sufficient,
    "PUBS": publications_page,
    "STRUCT": structure,
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
        # DEPLOY compares the SERVED site against this repo, so it is red for
        # any work that is committed but not yet pushed -- i.e. during normal
        # editing. Running it by default would train a reader to ignore a red
        # result, which is exactly the habit that let the stale deploy persist.
        # Opt in explicitly, or run it after pushing.
        if name in OPT_IN and not (args.family and name in args.family):
            continue
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
