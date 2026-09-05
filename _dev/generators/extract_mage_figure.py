#!/usr/bin/env python3
"""Extract a canonical MAGE book figure into a portfolio site, without drift.

The /mage research-program site reuses the book's opening conceptual figure
(Figure 0.3-1, "The MAGE method") rather than commissioning a novel hero figure.
Reuse is the asset here: a reader who sees the figure on the research landing
page and follows through to the book recognizes it as the same thing.

The problem this script solves: that figure is an **inline <svg> inside
book/0.3-the-mage-method-at-a-glance.html**, not a standalone file. Copy-pasting
it would create a second artifact free to diverge -- and the canonical site is
under active development by another agent, so divergence is a matter of time,
not chance.

So the copy is GENERATED and its provenance is CHECKED:

    extract   canonical inline <svg>  ->  repos/mage/figures/mage-method.svg
              with a provenance header recording the source file and a hash
              of the extracted SVG

    verify    re-extract, re-hash, compare. A changed hash means the book's
              figure moved on; the site copy is stale and must be regenerated
              deliberately, not silently.

    python3 generators/extract_mage_figure.py            # extract / refresh
    python3 generators/extract_mage_figure.py --check    # verify freshness only

--check is what scripts/check-portfolio calls. It exits 1 on drift.

This is the general portfolio pattern -- canonical source upstream, materialized
copy committed in the child, freshness held by a check -- applied to a figure.
"""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / ("repos/model-based-agentic-software-engineering/book/"
                 "0.3-the-mage-method-at-a-glance.html")
DEST = ROOT / "repos/mage/figures/mage-method.svg"
FIGURE_LABEL = "Figure 0.3-1"

# XML forbids "--" inside a comment, so this header must avoid it entirely --
# including in the flag name, which is written as "check" rather than "--check".
PROVENANCE = """<!-- GENERATED FILE. Do not hand-edit; edits will be overwritten.
     Source:  model-based-agentic-software-engineering/book/0.3-the-mage-method-at-a-glance.html
     Figure:  {label}. {caption}
     Extract: davis-web/generators/extract_mage_figure.py
     Verify:  python3 generators/extract_mage_figure.py (with the "check" flag)
     sha256:  {digest}

     This is the canonical MAGE conceptual figure, reused on the /mage research
     site so the research front door and the book show the same visual thesis.
     Do NOT redraw it here. Edit it in the MAGE book and re-extract, or the two
     will diverge. -->
"""


def extract() -> tuple[str, str]:
    """Return (svg_markup, caption_text) from the canonical chapter."""
    if not SOURCE.exists():
        raise SystemExit(f"canonical source missing: {SOURCE}\n"
                         "Is the model-based-agentic-software-engineering submodule checked out?")
    html = SOURCE.read_text()
    fig = re.search(r"<figure.*?</figure>", html, re.S)
    if not fig:
        raise SystemExit(f"no <figure> found in {SOURCE.name}; the book's structure changed")
    block = fig.group(0)

    svg = re.search(r"<svg.*?</svg>", block, re.S)
    if not svg:
        raise SystemExit(f"{FIGURE_LABEL} is no longer an inline <svg>; "
                         "if the book now emits a file, link that instead of extracting")

    cap = re.search(r"<figcaption.*?>(.*?)</figcaption>", block, re.S)
    caption = ""
    if cap:
        caption = re.sub(r"<[^>]+>", " ", cap.group(1))
        caption = re.sub(r"\s+", " ", caption).strip()
        caption = caption.split(". ", 1)[1] if caption.startswith(FIGURE_LABEL) else caption
    return svg.group(0), caption


def render(svg: str, caption: str) -> str:
    digest = hashlib.sha256(svg.encode()).hexdigest()[:16]
    safe_caption = caption[:300].replace("--", "\u2014")  # XML comments cannot contain "--"
    header = PROVENANCE.format(label=FIGURE_LABEL, caption=safe_caption, digest=digest)
    if not svg.lstrip().startswith("<?xml"):
        svg = '<?xml version="1.0" encoding="UTF-8"?>\n' + svg
    first, rest = svg.split("\n", 1) if "\n" in svg else (svg, "")
    return f"{first}\n{header}{rest}\n"


def current_digest(text: str) -> str | None:
    m = re.search(r"sha256:\s*([0-9a-f]{16})", text)
    return m.group(1) if m else None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="verify the committed copy matches the canonical source; exit 1 on drift")
    args = ap.parse_args(argv)

    svg, caption = extract()
    digest = hashlib.sha256(svg.encode()).hexdigest()[:16]

    if args.check:
        if not DEST.exists():
            print(f"FAIL  {DEST.relative_to(ROOT)} missing -- run without --check to extract")
            return 1
        have = current_digest(DEST.read_text())
        if have != digest:
            print(f"FAIL  {FIGURE_LABEL} has drifted from the canonical book figure")
            print(f"        committed: {have}")
            print(f"        canonical: {digest}")
            print("      The book's figure changed. Re-extract deliberately:")
            print("        python3 generators/extract_mage_figure.py")
            return 1
        print(f"ok    {FIGURE_LABEL} matches the canonical source ({digest})")
        return 0

    DEST.parent.mkdir(parents=True, exist_ok=True)
    prior = current_digest(DEST.read_text()) if DEST.exists() else None
    DEST.write_text(render(svg, caption))
    verb = "unchanged" if prior == digest else ("updated" if prior else "created")
    print(f"{verb}: {DEST.relative_to(ROOT)}  ({len(svg)} bytes, sha256 {digest})")
    if caption:
        print(f"  caption: {caption[:110]}...")
    if prior and prior != digest:
        print(f"  NOTE: the canonical figure changed ({prior} -> {digest}). "
              "Re-render the page and look at it before committing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
