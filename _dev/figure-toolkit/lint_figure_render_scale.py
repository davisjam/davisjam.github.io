#!/usr/bin/env python3
"""Figure text must be legible at the width a reader actually meets it.

A figure on the website is part of the page's typography. It does not get its
own universe of font sizes. `font-size="13"` inside a 1240-wide viewBox is not
13px to anybody: rendered in a 940px column it is 9.9px, and in a 503px landing
column it is 5.3px. That is how a signature figure ends up looking like a
slide printed four-up.

WHAT THIS MEASURES. Not the SVG's nominal font-size, which is meaningless on
its own, but the APPARENT size once the drawing is scaled into its column:

    apparent_px = font_size * render_width / viewBox_width

The scale-invariant form of the same thing is `font_size / viewBox_width`, which
is the number worth comparing between figures.

THE REFERENCE IS mage-method.svg, and it was not chosen arbitrarily -- it came
from the book's figure spec and is the one figure already in scale: a 1000-wide
viewBox with 20px minimum text, so 0.020, rendering at 18.8px. The other five
sit at 13/1240 = 0.0105, about half that, which is why their explanatory text
disappears.

Getting a figure from 0.0105 to the target is not a font-size edit. Type nearly
twice as large needs roughly twice the room, so the drawing has to lose about
half its words. That is a redraw, and it is the correct fix -- enlarging the
type in place would just collide, which the overflow and collision sensors
would then report.

AUDIT-ONLY. It finds five of six figures today, and a blocking check that is
red on arrival breaks every unrelated push (repo rule: audit-only first, drain,
then promote).
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _figure_scan_root  # noqa: E402

ASSETS = _figure_scan_root.scan_root()

# The two widths a reader actually meets these drawings at, measured from the
# live site rather than assumed: the programme page caps the figure at 940px,
# and the research landing gives each entry ~503px in its two-column grid.
RENDER_WIDTHS = {"programme page": 940, "research landing": 503}

# Site metadata/caption text is ~14px. A figure's smallest SUBSTANTIVE text
# should not read materially smaller than that on the programme page. Tertiary
# annotations need not be comfortable in the landing thumbnail, which is a
# visual identifier rather than a miniature document.
TARGET_PX = 13.0
GATE = "programme page"

# Titles and decks are not the concern; the explanatory text is.
SUBSTANTIVE_BELOW = 20.0


def findings() -> list[str]:
    out: list[str] = []
    for svg in _figure_scan_root.figures(ASSETS):
        text = svg.read_text(encoding="utf-8")
        vb = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', text)
        if not vb:
            continue
        width = float(vb.group(1))
        sizes = sorted({float(x) for x in re.findall(r'font-size="([\d.]+)"', text)})
        if not sizes:
            continue
        substantive = [s for s in sizes if s < SUBSTANTIVE_BELOW] or sizes
        smallest = min(substantive)
        apparent = smallest * RENDER_WIDTHS[GATE] / width
        if apparent + 0.05 < TARGET_PX:
            ratio = smallest / width
            need = TARGET_PX * width / RENDER_WIDTHS[GATE]
            out.append(
                f"TOO-SMALL {svg.name} — smallest substantive text is "
                f"font-size={smallest:g} in a {width:g}-wide viewBox, i.e. "
                f"{apparent:.1f}px on the {GATE} (target {TARGET_PX:g}px). "
                f"scale={ratio:.4f} vs 0.0200 for mage-method. Needs "
                f"font-size≈{need:.0f}, which means roughly half the words.")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.parse_args(argv)
    fs = findings()
    print(f"== figure-render-scale — apparent text size at {RENDER_WIDTHS[GATE]}px "
          f"[AUDIT-ONLY (prints, exits 0)] ==")
    if not fs:
        print("  clean — every figure's explanatory text is legible where it is read")
    else:
        print(f"  {len(fs)} finding(s):")
        for f in fs:
            print(f"    {f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
