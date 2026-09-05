#!/usr/bin/env python3
"""Generate the research-program sites.

    python3 generators/generate_sites.py            # all
    python3 generators/generate_sites.py mage       # one

Page grammar lives in generators/site_template.py (model/research-site-design-style.md).
Prose lives here, written to model/research-site-writing-style.md: plain academic
English, concrete subject, active verbs, no commentary on its own importance.

Bibliographic and funding facts come from data/*.yaml and are never paraphrased
into prose (model/ssot-records.md). Authored prose explains relationships among
those facts.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import site_template as T  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Per-site authored prose. Each `intro` states the problem mechanically; no
# sentence claims the work is important. Section prose explains relationships
# between the concepts rather than listing them.
COPY: dict[str, dict] = {
    "mage": {
        "question": "How should we engineer software when implementation becomes abundant "
                    "but engineering judgment remains scarce?",
        "intro": [
            "Capable agents have made it much cheaper to produce working code. They have not "
            "made it cheaper to decide what should be built, which obligations govern it, how "
            "to read the resulting evidence, or whether the system is acceptable to ship.",
            "MAGE studies the engineering structures that make delegated implementation "
            "governable: making consequential knowledge explicit as models, giving selected "
            "obligations authority over what agents produce, validating realizations against "
            "those models, and turning recurring human judgment into structures that later "
            "work can reuse.",
        ],
        "sections": [("research", "Research"), ("writings", "Writings"),
                     ("support", "Funding and support")],
        "extra": ('<h2 id="resources">The MAGE book and course</h2>\n'
                  '<p>The book, the course mirror, the detailed framework, and adoption '
                  'guidance are maintained separately.</p>\n'
                  '<p><a href="{canonical}">Explore MAGE &rarr;</a></p>'),
    },
    "embedded-swe": {
        "question": "How can analysis and assurance become practical for embedded software?",
        "intro": [
            "Embedded software runs where failures are expensive, and in conditions that defeat "
            "the assumptions most analysis tools are built on: no operating system to speak of, "
            "hardware that the analysis cannot reach, and code that cannot simply be run in a "
            "test harness.",
            "Our work has attacked that gap in stages. We studied defects in real embedded "
            "network stacks, built rehosting infrastructure so firmware can execute away from "
            "its target hardware, and applied static analysis at a scale where it finds "
            "hundreds of defects across many projects. A current thrust, Unit Proofing, asks "
            "whether component-level formal verification can be made cheap enough to use as an "
            "ordinary engineering step rather than a special occasion.",
        ],
        "sections": [("research", "Research"), ("publications", "Publications"),
                     ("support", "Funding and support")],
    },
    "failure-aware-sdlc": {
        "question": "What can engineering organizations learn from the ways software fails?",
        "intro": [
            "Software failures are investigated, patched, and filed away. The engineering "
            "knowledge they contain rarely survives the incident that produced it, so "
            "organizations meet the same class of failure again in the next system.",
            "We study failures empirically and ask what would have to change for that knowledge "
            "to persist. Some of our work characterizes how failures recur across systems and "
            "domains; other work examines whether evidence from past failures actually changes "
            "engineering decisions, and how organizations might structure requirements, design, "
            "and validation so that it does.",
        ],
        "sections": [("research", "Research"), ("publications", "Publications")],
    },
    "ptm-se": {
        "question": "What changes about software engineering when the reused component is a "
                    "learned model?",
        "intro": [
            "Developers increasingly build systems on models they did not train, obtained from "
            "public registries. A pre-trained model behaves like a dependency in some respects "
            "and unlike one in others: its interface is underspecified, its provenance is often "
            "unclear, its behaviour changes when it is retrained, and the file itself may "
            "execute code when loaded.",
            "We study models as software artifacts. Our work examines how developers find and "
            "select models, what happens when a model is integrated into a larger system, "
            "whether interoperability claims hold in practice, how model naming and "
            "documentation mislead, and what security properties a reused model brings with it.",
        ],
        "sections": [("research", "Research"), ("publications", "Publications"),
                     ("support", "Funding and support")],
    },
    "software-supply-chain": {
        "question": "How can software reuse remain trustworthy at ecosystem scale?",
        "intro": [
            "Modern software systems depend on artifacts produced by people and organizations "
            "their developers may never meet. Package registries and build systems make reuse "
            "inexpensive, but they separate the act of using software from direct knowledge of "
            "who produced it, how it reached the consumer, and what authority it should receive "
            "once incorporated into a system.",
            "We study the evidence and engineering mechanisms that make trust possible across "
            "those boundaries: establishing identity and provenance, protecting the distribution "
            "process, and making trust decisions sensitive to the context in which a dependency "
            "is actually used. Across these problems, the recurring question is not simply "
            "whether software is trusted, but what evidence justifies what trust, for what use.",
        ],
        "sections": [("research", "Research"), ("applications", "Applications"),
                     ("publications", "Publications"), ("support", "Funding and support")],
        "foundations_prose": [
            "Signing can establish who vouched for an artifact. A valid signature does not tell "
            "a developer whether that producer is trustworthy, or whether the dependency is "
            "appropriate in a particular system. We therefore study both the mechanisms that "
            "carry evidence and the decisions developers make from it.",
            "On the mechanism side, we have measured signing across public package registries "
            "and examined what identity-based signing establishes in practice. On the decision "
            "side, we have interviewed practitioners about why signing is or is not adopted, "
            "studied how developers choose dependencies, and shown how naming and metadata "
            "become an attack surface when an ecosystem assumes that a familiar package name "
            "identifies a familiar producer.",
        ],
        "applications_prose": [
            "The same questions recur wherever software is assembled from artifacts produced "
            "elsewhere, and the newer ecosystems inherit the problem before they inherit the "
            "defences.",
            "Pre-trained models are distributed through registries much like packages, and a "
            "model file can execute code when it is loaded. Research software has supply chains "
            "of its own, with different incentives and less tooling. Agent ecosystems are "
            "beginning to distribute executable capability in the same way.",
        ],
    },
    "saferegex": {
        "question": "What do small, heavily reused program fragments reveal about software "
                    "engineering?",
        "intro": [
            "A regular expression is a few characters long and is copied between languages, "
            "libraries, and projects with little thought. That makes it a useful subject: the "
            "same artifact is reused across many contexts, so its behaviour exposes assumptions "
            "that larger components hide.",
            "We have examined regexes along three lines that ran concurrently for most of a "
            "decade. One asks whether a regex means the same thing when it moves between "
            "languages. One asks what developers actually understand about the expressions they "
            "write. The third asks what a matching engine does with them, including the "
            "conditions under which matching becomes a denial-of-service vector, and what can "
            "be done about it.",
        ],
        "sections": [("research", "Research"), ("publications", "Publications"),
                     ("support", "Funding and support")],
    },
}


def load():
    import yaml
    r = lambda p: yaml.safe_load((ROOT / p).read_text())
    return r("model/sites.yaml"), r("data/publications.yaml"), r("data/funding.yaml")


def build(site: dict, pubs: list, fund: dict, canonical: str) -> str:
    pid = site["project_id"]
    c = COPY[pid]

    mine = [p for p in pubs if pid in (p.get("projects") or [])]
    by_role: dict[str, list] = {}
    for p in mine:
        by_role.setdefault((p.get("role_in_project") or {}).get(pid, "core"), []).append(p)

    grants = [g for g in fund["grants"] if pid in (g.get("projects") or [])]
    sections = [(sid, lbl) for sid, lbl in c["sections"]
                if sid != "support" or grants]

    intro = "\n".join(f"<p>{T.esc(p)}</p>" for p in c["intro"])

    fig = site.get("figure") or {}
    fig_file = f"figures/{fig['id']}.svg" if fig.get("id") else None
    has_fig = fig_file and (ROOT / site["path"] / fig_file).exists()

    b: list[str] = []

    # Research: prose beside the figure -- a good use of width.
    b.append('<h2 id="research">Research</h2>')
    research_prose = c.get("foundations_prose") or []
    if has_fig:
        left = "\n".join(f"<p>{T.esc(p)}</p>" for p in research_prose) or ""
        # caption is the READER-facing sentence; claim is the internal test the
        # figure had to pass. Never render claim -- it is design rationale.
        caption = " ".join((fig.get("caption") or fig.get("claim") or "").split())
        b.append(f'''<div class="split">
  <div>{left}</div>
  <figure>
    <img src="{T.esc(fig_file)}" alt="{T.esc(caption[:220])}">
    <figcaption>{T.esc(caption)}</figcaption>
  </figure>
</div>''')
    elif research_prose:
        b.extend(f"<p>{T.esc(p)}</p>" for p in research_prose)

    if c.get("applications_prose"):
        b.append('<h2 id="applications">Applications</h2>')
        b.extend(f"<p>{T.esc(p)}</p>" for p in c["applications_prose"])
        if by_role.get("application"):
            b.append(T.bibliography(by_role["application"], pid))

    if c.get("extra"):
        b.append(c["extra"].format(canonical=canonical))

    core = by_role.get("core", []) + by_role.get("precursor", [])
    if core:
        label = "Writings" if pid == "mage" else "Publications"
        anchor = "writings" if pid == "mage" else "publications"
        b.append(f'<h2 id="{anchor}">{label}</h2>')
        b.append(T.bibliography(core, pid))

    if grants:
        b.append('<h2 id="support">Funding and support</h2>')
        b.append("<p>This work has been supported by:</p>")
        b.append(T.funding(grants))

    return T.page(site["title"], " ".join(c["question"].split()), intro,
                  site["url"], "\n".join(b), sections,
                  site.get("short_name") or site["title"])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("site", nargs="*")
    args = ap.parse_args(argv)

    sites_doc, pubs_doc, fund = load()
    pubs = pubs_doc["publications"]
    canonical = next(s["url"] for s in sites_doc["sites"]
                     if s["id"] == "model-based-agentic-software-engineering")

    targets = [s for s in sites_doc["sites"] if s.get("profile") == "research-program"]
    if args.site:
        targets = [s for s in targets if s["project_id"] in args.site]

    for s in targets:
        out = ROOT / s["path"]
        (out / "assets").mkdir(parents=True, exist_ok=True)
        (out / "assets/site.css").write_text(T.CSS.format(**T.TOKENS))
        # logo + headshot are materialized by scripts/sync-site
        (out / "index.html").write_text(build(s, pubs, fund, canonical))
        (out / ".nojekyll").write_text("")
        n = sum(1 for p in pubs if s["project_id"] in (p.get("projects") or []))
        g = sum(1 for x in fund["grants"] if s["project_id"] in (x.get("projects") or []))
        print(f"  {s['project_id']:<24} {n:>2} pubs, {g} grants -> {s['url']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
