#!/usr/bin/env python3
"""One-time migration: CV + publications.json -> data/publications.yaml.

After this runs, ``data/publications.yaml`` is the canonical, hand-maintained
source. This script is kept for provenance -- so the derivation is auditable --
not as a step in a recurring pipeline. Re-running it would overwrite hand edits.

Reconciliation rule (per James, 260904): where the CV and publications.json both
describe a work, **publications.json wins** on bibliographic fields; the CV
supplies the stable id and anything publications.json lacks. OpenAlex enrichment
is a separate pass (generators/enrich_openalex.py) that only ever ADDS
identifiers -- DOI, OA link, citation count -- and never overwrites a title.

Inputs:
    data/cv-extract.json     parsed CV entries, keyed on CV ids
    repos/davisjam.github.io/markdown_generator/publications.json

Output:
    data/publications.yaml
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PJ = ROOT / "repos/davisjam.github.io/markdown_generator/publications.json"
CV = ROOT / "data/cv-extract.json"
OUT = ROOT / "data/publications.yaml"

# --- program membership ------------------------------------------------------
# Authoritative source: James's six-program directive (260904, second message),
# which supersedes the earlier five-program message where they differ.
# MANY-TO-MANY by design -- see model/content-model.md §1 P1. A publication in
# two lists is correct, not a bug to clean up.

CORE = {
    "mage":                  ["B-1", "J-3", "W-2", "W-5", "W-9", "W-10"],
    "ptm-se":                ["C-12", "C-22", "C-23", "C-28", "C-29",
                              "J-1", "J-2", "J-4", "J-7",
                              "W-1", "W-12", "W-15", "W-19", "W-22", "W-25", "W-29",
                              "R-5", "R-7", "R-8", "Pa-1"],
    "software-supply-chain": ["C-2", "C-3", "C-8", "C-13", "C-16", "C-26", "M-1",
                              "W-6", "W-7", "W-8", "W-20", "W-27", "R-1"],
    "embedded-swe":          ["C-1", "C-10", "C-15", "C-17", "C-30",
                              "W-3", "W-11", "W-16", "W-17", "R-2"],
    "failure-aware-sdlc":    ["C-9", "C-21", "C-25",
                              "W-21", "W-24", "W-26", "R-3", "W-18", "W-20"],
    "saferegex":             ["C-4", "C-18", "C-31", "C-33", "C-36", "C-39", "C-40",
                              "C-41", "C-44", "C-45", "W-4", "W-33", "W-34", "W-36", "R-4"],
}

# Non-core roles, asserted explicitly. Everything else defaults to `core`.
ROLE_OVERRIDE = {
    ("software-supply-chain", "C-12"): "application",   # PickleBall: PTM-SE core, SSC application
    ("software-supply-chain", "W-5"):  "application",   # AgentHub: agent ecosystem
    # C-45 and W-36 are the Node.js event-handler-poisoning lineage the ReDoS
    # work grew out of -- program history, not current thrust (James, 260904).
    ("saferegex", "C-45"):             "precursor",
    ("saferegex", "W-36"):             "precursor",
}

# Cross-listings beyond the CORE lists above (James, 260904).
ALSO = {
    "W-5":  ["software-supply-chain"],   # AgentHub -> MAGE + supply chain
    "C-12": ["software-supply-chain"],   # PickleBall -> PTM-SE + supply chain
}

# Breadth clusters on the umbrella Research page. NOT project sites.
CLUSTERS = {
    "efficient-ml-systems": ["C-5", "C-6", "C-11", "C-14", "C-19", "C-20",
                             "C-32", "C-34", "C-35", "C-43", "M-2", "M-3", "W-23", "R-6"],
    "reliability-security-systems": ["C-7", "C-24", "C-27", "C-37", "C-38", "C-42",
                                     "C-46", "J-5", "J-9", "W-28", "W-31", "W-32", "W-35"],
    "engineering-education": ["B-2", "J-6", "J-8", "J-10", "J-11", "W-13", "W-14", "W-30"],
}

# All earlier-message candidates have since been adjudicated (James, 260904):
# C-45 and W-36 -> saferegex as precursors; R-6 -> efficient-ml-systems (not
# recognizably MAGE); Ps-4/Ps-5 remain posters, which are unassigned by design.
CANDIDATES: dict[str, list[str]] = {}

# Patent grant years. Google Patents is authoritative where a GRANT record was
# retrieved; James's CV-derived list otherwise (James, 260904). publications.json
# appears to carry filing or application-publication years in places.
#   Pa-8  US10229121B2  filed 2016-03-15, GRANTED 2019-03-12  (both sources said 2018)
#   Pa-3  US11176090B2  filed 2019-01-28, GRANTED 2021-11-16  (agrees with 2021)
#   Pa-2  only the application (US20220374265A1, filed 2021) was retrievable before
#         Google Patents rate-limited; James's list gives the grant as 2024.
# Pa-4..Pa-7 remain unverified against Google Patents; see data/patents-verification.md.
# Resolved to EXACT Google Patents records, not title searches: several IBM
# inventions have near-identical titles, so a generated search link would be
# sloppy and could point at the wrong grant. Grant years come from the record.
#
# Pa-4 is unresolved -- four query phrasings returned nothing. Left without a
# number rather than linked to a guess.
# Pa-1 is a Purdue PROVISIONAL application (63/813,549); provisionals have no
# public Google Patents record, so it carries no link.
PATENTS = {
    "Pa-2": ("US11875185B2", 2024),   # granted 2024-01-16, filed 2021-05-19
    "Pa-3": ("US11176090B2", 2021),   # granted 2021-11-16
    "Pa-5": ("US10891174B1", 2021),   # granted 2021-01-12
    "Pa-6": ("US10642796B2", 2020),   # granted 2020-05-05
    "Pa-7": ("US10614039B2", 2020),   # granted 2020-04-07 -- NOT 2018
    "Pa-8": ("US10229121B2", 2019),   # granted 2019-03-12 -- neither source had this
}
PATENT_YEAR = {k: v[1] for k, v in PATENTS.items()}

TYPE_OF = {"B": "book", "C": "conference", "J": "journal", "W": "workshop",
           "M": "magazine", "R": "report", "Ps": "poster", "Pa": "patent"}

# Titles the CV parser could not recover (author lists with bare surnames or
# particles). Hand-extracted from the CV; verified against the raw entry.
MANUAL_TITLE = {
    "B-1": "Model-Based Agentic Software Engineering",
    "B-2": "Epilogue: The Computer Engineer as Tool-User",
    "C-35": "Low-Power Multi-Camera Object Re-Identification using Hierarchical Neural Networks",
    "J-8": ("Applying Experiential Learning Theory to Understand Study Abroad Leaders' "
            "Experiences Using Real-Time Perspectives"),
    "Ps-3": "Is Reuse All You Need? A Systematic Comparison of Regular Expression Composition Strategies",
    "Ps-4": "Towards Scalable and Performance-Aware Code Optimization with LLMs",
}


# The single place a paper's readable destination is decided. Every renderer
# resolves from here; none constructs its own link (James, 260904).
#
# Preference is about the READER, not about citation formality: prefer a page
# they can actually obtain the paper from. A DOI that lands on a paywall is
# worse than an arXiv preprint of the same work.
BOOK_URL = {"B-1": "https://davisjam.github.io/model-based-agentic-software-engineering/book/index.html"}


def paper_url(pub: dict) -> str | None:
    if pub["id"] in BOOK_URL:
        return BOOK_URL[pub["id"]]
    links = pub.get("links") or {}
    vals = [v for v in links.values() if v]
    arxiv = next((v for v in vals if "arxiv.org" in str(v)), None)
    if arxiv:
        return arxiv                      # 1. stable public preprint
    paper = links.get("paper")
    if paper and str(paper).startswith("/files/"):
        # ABSOLUTE, not root-relative. These PDFs live at the umbrella root, so
        # from a project site "/files/..." is a cross-site link written as a
        # relative guess -- it happens to resolve only because the sites share an
        # origin. url-architecture.md §7: cross-project links use the canonical
        # namespace explicitly.
        return f"https://davisjam.github.io{paper}"
    if paper and str(paper).startswith("http"):
        return paper                      # 3. publisher page
    return links.get("record") or links.get("blog") or None


def key_sort(k: str) -> tuple[int, int]:
    pre, num = k.rsplit("-", 1)
    return (["B", "C", "J", "M", "W", "R", "Pa", "Ps"].index(pre), int(num))


def yaml_str(s: str) -> str:
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


def load_notes() -> dict:
    """program_notes, keyed `<pub-id>.<project-id>` in data/program-notes.yaml.

    Kept in a separate file from publications.yaml because they are authored
    prose over a generated record: a regeneration of the bibliography must not
    be able to lose them.
    """
    import yaml
    f = ROOT / "data/program-notes.yaml"
    if not f.exists():
        return {}
    raw = yaml.safe_load(f.read_text()).get("notes") or {}
    out: dict[str, dict[str, str]] = {}
    for key, text in raw.items():
        pid, _, proj = key.partition(".")
        clean = re.sub(r"\s*#\s*inferred.*$", "", str(text)).strip()
        # Guard: an authoring marker must never reach a page. The same class of
        # defect put design rationale in a figure caption -- a "#" annotation
        # inside a YAML folded scalar is TEXT, not a comment.
        assert "#" not in clean, f"authoring marker leaked into {key}: {clean!r}"
        out.setdefault(pid, {})[proj] = " ".join(clean.split())
    return out


def main() -> int:
    if not CV.exists():
        print(f"missing {CV}; run the CV extraction first", file=sys.stderr)
        return 1
    cv = json.loads(CV.read_text())
    notes = load_notes()
    # publications.json records are carried inline on each CV entry by the
    # extraction step, already reconciled. publications.json wins on conflict.

    membership: dict[str, list[str]] = {}
    roles: dict[str, dict[str, str]] = {}
    for proj, ids in CORE.items():
        for k in ids:
            membership.setdefault(k, []).append(proj)
            roles.setdefault(k, {})[proj] = ROLE_OVERRIDE.get((proj, k), "core")
    for k, projs in ALSO.items():
        for proj in projs:
            if proj not in membership.setdefault(k, []):
                membership[k].append(proj)
                roles.setdefault(k, {})[proj] = ROLE_OVERRIDE.get((proj, k), "application")
    cluster_of = {k: c for c, ids in CLUSTERS.items() for k in ids}

    out = [
        "# data/publications.yaml -- CANONICAL scholarly record.",
        "#",
        "# Keyed on the CV's own identifiers so the two stay mutually checkable.",
        "# Generated once by generators/build_publications.py; hand-maintained since.",
        "#",
        "# `projects` is MANY-TO-MANY (model/content-model.md P1). A publication on two",
        "# sites is reuse of one canonical record in two legitimate narratives -- do NOT",
        "# 'clean up' overlaps by forcing each work into a single project.",
        "#",
        "# `role_in_project`: core | application | precursor | context",
        "# Posters are carried here but are NOT surfaced on project sites (presentation",
        "# decision, not a data one).",
        "",
        "schema_version: 1",
        "publications:",
    ]

    counts: dict[str, int] = {}
    for k in sorted(cv, key=key_sort):
        e = cv[k]
        pjrec = e.get("pj")
        title = (pjrec or {}).get("title") or MANUAL_TITLE.get(k) or e.get("title") or ""
        if not title:
            print(f"  WARNING {k}: no title recovered", file=sys.stderr)
        projs = membership.get(k, [])
        for p in projs:
            counts[p] = counts.get(p, 0) + 1

        out.append(f"  - id: {k}")
        out.append(f"    type: {TYPE_OF[k.rsplit('-',1)[0]]}")
        out.append(f"    title: {yaml_str(title)}")
        if e.get("authors"):
            out.append(f"    authors: {yaml_str(e['authors'])}")
        if pjrec:
            for fld in ("venue", "year"):
                if pjrec.get(fld):
                    v = PATENT_YEAR.get(k) if fld == "year" and k in PATENT_YEAR else pjrec[fld]
                    out.append(f"    {fld}: {v if isinstance(v, int) else yaml_str(str(v))}")
            links = {n: pjrec.get(u) for n, u in
                     (("artifact", "artifactURL"), ("video", "videoURL"), ("blog", "blogURL"))
                     if pjrec.get(u)}
            if pjrec.get("paperBasename"):
                base = pjrec["paperBasename"]
                # Some entries carry a full URL rather than a filename.
                links["paper"] = (base if base.startswith(("http://", "https://"))
                                  else f"/files/publications/{base}")
            resolved = paper_url({"id": k, "links": links})
            if resolved:
                out.append(f"    paper_url: {yaml_str(resolved)}")
            if links:
                out.append("    links:")
                for n, u in links.items():
                    out.append(f"      {n}: {yaml_str(u)}")
            awards = [a for a, f in (("best-paper", "bestPaperAward"),
                                     ("best-artifact", "bestArtifactAward")) if pjrec.get(f)]
            if awards:
                out.append(f"    awards: [{', '.join(awards)}]")
        mine = notes.get(k) or {}
        if mine:
            out.append("    program_notes:")
            for proj in projs or sorted(mine):
                if proj in mine:
                    out.append(f"      {proj}: {yaml_str(mine[proj])}")
        if k in BOOK_URL and not (pjrec or {}).get("paperBasename"):
            out.append(f"    paper_url: {yaml_str(BOOK_URL[k])}")
        if k in PATENTS:
            num = PATENTS[k][0]
            out.append(f"    patent_number: {num}")
            out.append(f"    links:\n      record: \"https://patents.google.com/patent/{num}/en\"")
        if projs:
            out.append(f"    projects: [{', '.join(projs)}]")
            out.append("    role_in_project:")
            for p in projs:
                out.append(f"      {p}: {roles[k][p]}")
        elif k in cluster_of:
            out.append(f"    cluster: {cluster_of[k]}")
        out.append("")

    out += ["# Candidates from the earlier five-program message that the authoritative",
            "# six-program directive did not repeat. Left UNASSIGNED pending a decision.",
            "candidates:"]
    for proj, ids in CANDIDATES.items():
        out.append(f"  {proj}: [{', '.join(ids)}]")

    OUT.write_text("\n".join(out) + "\n")
    print(f"wrote {OUT}  ({len(cv)} records)")
    for p in sorted(counts):
        print(f"   {p:<24} {counts[p]}")
    unassigned = [k for k in cv if k not in membership and k not in cluster_of]
    print(f"   {'unassigned':<24} {len(unassigned)}: {' '.join(sorted(unassigned, key=key_sort))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
