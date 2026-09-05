#!/usr/bin/env python3
"""Generate the six research-program pages inside davisjam.github.io.

    python3 generators/generate_research_pages.py

Consolidation phase 3. These replace the standalone project sites: same prose,
same figures, same publication data, rendered as pages of the canonical site
under `research/<slug>/` and inheriting its shell from the theme.

Publication entries resolve from _data/publications.yml by ID. A page never
carries a copy of a title, venue, year, or URL -- and the title is always the
link, per the site-wide paper-link invariant.

URL note: while a project repo of the same name still has Pages enabled, GitHub
serves THAT repo at davisjam.github.io/<repo>/ and shadows any same-named path
here. These pages therefore live at /research/<slug>/, which collides with
nothing, and redirects from the old paths are added only after those repos are
deleted.
"""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
UMBRELLA = ROOT / "repos/davisjam.github.io"
OUT = UMBRELLA / "_pages"

sys.path.insert(0, str(ROOT / "generators"))
from generate_sites import COPY  # noqa: E402  the authored program prose


def yfm(v: str) -> str:
    return '"' + str(v).replace("\\", "\\\\").replace('"', '\\"') + '"'


def short_venue(v: str) -> str:
    import re
    m = re.search(r"\(([A-Za-z][A-Za-z0-9/&-]{1,14})\)", v or "")
    if m:
        return m.group(1)
    return re.sub(r"^Proceedings of the \d+\w*\s*", "", v or "").strip()[:48]


def pub_li(p: dict, project: str) -> str:
    url = p.get("paper_url")
    title = f'<a href="{url}">{p["title"]}</a>' if url else p["title"]
    venue = short_venue(p.get("venue") or "")
    yr = p.get("year")
    where = " &middot; ".join(x for x in [venue, str(yr) if yr else ""] if x)
    note = (p.get("program_notes") or {}).get(project)
    awards = "".join(f' <span class="award">{a.replace("-", " ")}</span>'
                     for a in (p.get("awards") or []))
    out = [f'  <li><span class="pub-title">{title}</span>{awards}']
    if where:
        out.append(f'<br><span class="venue">{where}</span>')
    if note:
        out.append(f'<br><span class="note">{note}</span>')
    out.append("</li>")
    return "".join(out)


def main() -> int:
    import yaml
    sites = yaml.safe_load((ROOT / "model/sites.yaml").read_text())["sites"]
    struct = yaml.safe_load((ROOT / "data/program-structure.yaml").read_text())["programs"]
    pubs = yaml.safe_load((ROOT / "data/publications.yaml").read_text())["publications"]
    fund = yaml.safe_load((ROOT / "data/funding.yaml").read_text())["grants"]
    canonical = next(s for s in sites
                     if s["id"] == "model-based-agentic-software-engineering")

    OUT.mkdir(parents=True, exist_ok=True)
    for s in sites:
        if s.get("profile") != "research-program":
            continue
        pid = s["project_id"]
        c = COPY[pid]
        fig = s.get("figure") or {}
        mine = [p for p in pubs if pid in (p.get("projects") or [])]
        by_role: dict[str, list] = {}
        for p in mine:
            by_role.setdefault((p.get("role_in_project") or {}).get(pid, "core"), []).append(p)
        for v in by_role.values():
            v.sort(key=lambda p: -(p.get("year") or 0))
        grants = [g for g in fund if pid in (g.get("projects") or [])]

        o = ["---",
             "layout: research-project",
             f"title: {yfm(s['title'])}",
             f"permalink: /research/{pid}/",
             "author_profile: true",
             f"research_slug: {yfm(s.get('short_name') or s['title'])}",
             f"question: {yfm(' '.join(c['question'].split()))}",
             f"figure: /assets/research/{pid}/{fig.get('id')}.svg",
             f"figure_alt: {yfm(' '.join((fig.get('caption') or '').split()))}",
             f"figure_caption: {yfm(' '.join((fig.get('caption') or '').split()))}"]
        if pid == "mage":
            o += [f"external_site: {canonical['url']}",
                  'external_label: "Explore the MAGE book, course, and framework"']
        o += ["---", ""]

        o += [" ".join(p.split()) + "\n" for p in c["intro"]]

        # The body is organized by CLAIM, not by year. Publications hang beneath
        # a claim as evidence for it; chronology is an artifact of the record,
        # and the Publications page already answers "when".
        by_id = {p["id"]: p for p in pubs}
        for sec in struct[pid]["sections"]:
            o.append(f"## {sec['title']}\n")
            o.append(" ".join(sec["prose"].split()) + "\n")
            o.append('<ul class="pub-list">')
            for rid in sec["publications"]:
                rec = by_id.get(rid)
                if rec is None:
                    raise SystemExit(f"{pid}: {rid} is not in the publication record")
                o.append(pub_li(rec, pid))
            o.append("</ul>\n")

        if grants:
            o.append("## Funding and support\n")
            o.append("This work has been supported by:\n")
            for g in grants:
                num = f" (#{g['number']})" if g.get("number") else ""
                t = f"[{g['title']}]({g['url']})" if g.get("url") else g["title"]
                o.append(f"- **{g['sponsor']}** — {t}{num}")
            o.append("")

        (OUT / f"research-{pid}.md").write_text("\n".join(o))
        print(f"  research/{pid}/  {len(mine)} publications, {len(grants)} grants")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
