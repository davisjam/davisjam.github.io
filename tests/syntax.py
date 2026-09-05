#!/usr/bin/env python3
"""Every syntax check we can run without a Ruby toolchain, as a pre-push gate.

    python3 tests/syntax.py

WHY THIS EXISTS (260905). A regex edit to `_includes/masthead.html` removed an
`{% if %}` opener but left its `{% else %}{% endif %}` behind. Three block opens
against five closes is a Liquid syntax error, so GitHub Pages failed to build --
and kept serving the previous site. Several pushes in a row silently did
nothing. The alignment engine stayed green the whole time because it reads the
REPOSITORY, so it was measuring files that had never become a website.

Nothing in the toolchain compared what was pushed against what could be built.
This does, before the push rather than after.

A real `jekyll build` would be strictly better and should replace the Liquid
section here the moment a Ruby toolchain is available. Until then these checks
cover the failure modes that actually break a Pages build: unbalanced Liquid,
malformed front matter, unparseable data, and malformed SVG.

Exit 1 blocks the push. `git push --no-verify` overrides, which should be rare
enough to be memorable.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {".git", "_site", ".jekyll-cache", "node_modules", ".sass-cache", "vendor"}

# Liquid tags that open a block and require a matching {% endX %}. `else`,
# `elsif`, `when`, `break` and `continue` appear INSIDE a block and open nothing
# -- mistaking one for an opener is how a checker gets this wrong.
BLOCK_TAGS = {
    "if", "unless", "for", "case", "capture", "raw", "comment", "tablerow",
    "form", "paginate", "highlight", "block", "schema", "javascript",
    "stylesheet", "style", "liquid",
}
TAG = re.compile(r"\{%-?\s*(\w+)")


def files(*suffixes: str):
    for p in sorted(ROOT.rglob("*")):
        if p.is_file() and p.suffix in suffixes and not (set(p.parts) & SKIP):
            yield p


def check_liquid(bad: list[str]) -> None:
    """Balance {% block %} ... {% endblock %} with a stack, reporting the line."""
    for p in files(".html", ".md", ".markdown", ".xml"):
        stack: list[tuple[str, int]] = []
        for n, line in enumerate(p.read_text(errors="replace").splitlines(), 1):
            for m in TAG.finditer(line):
                tag = m.group(1)
                if tag in BLOCK_TAGS:
                    stack.append((tag, n))
                elif tag.startswith("end"):
                    want = tag[3:]
                    if not stack:
                        bad.append(f"{p.relative_to(ROOT)}:{n}: "
                                   f"{{% {tag} %}} with no matching {{% {want} %}}")
                    elif stack[-1][0] != want:
                        got, at = stack.pop()
                        bad.append(f"{p.relative_to(ROOT)}:{n}: {{% {tag} %}} closes "
                                   f"{{% {got} %}} opened on line {at}")
                    else:
                        stack.pop()
        for tag, n in stack:
            bad.append(f"{p.relative_to(ROOT)}:{n}: {{% {tag} %}} is never closed "
                       f"-- Pages will fail to build and keep serving the old site")


def check_front_matter(bad: list[str]) -> None:
    """A page whose front matter will not parse is a page Jekyll drops."""
    import yaml
    import _frontmatter
    for p in files(".md", ".markdown", ".html"):
        text = p.read_text(errors="replace")
        if _frontmatter.is_unclosed(text):
            bad.append(f"{p.relative_to(ROOT)}: front matter is never closed")
            continue
        try:
            fm = _frontmatter.load(p, text=text)
        except yaml.YAMLError as e:
            bad.append(f"{p.relative_to(ROOT)}: front matter is not valid YAML -- "
                       f"{str(e).splitlines()[0]}")
            continue
        if fm and "permalink" in fm:
            link = str(fm["permalink"])
            if not link.startswith("/"):
                bad.append(f"{p.relative_to(ROOT)}: permalink {link!r} is relative; "
                           f"it must start with /")


def check_data(bad: list[str]) -> None:
    import yaml
    for p in files(".yml", ".yaml"):
        try:
            yaml.safe_load(p.read_text())
        except yaml.YAMLError as e:
            bad.append(f"{p.relative_to(ROOT)}: {str(e).splitlines()[0]}")
    for p in files(".json"):
        text = p.read_text()
        # markdown_generator/publications.json declares on its own first line
        # that it supports comment lines and that `#` lines are deleted before
        # parsing. Honour the file's stated contract rather than calling a file
        # broken for being what it says it is.
        if text.lstrip().startswith("#"):
            text = "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("#"))
        try:
            json.loads(text)
        except json.JSONDecodeError as e:
            bad.append(f"{p.relative_to(ROOT)}: {e}")


def check_svg(bad: list[str]) -> None:
    """Figures are XML. `--` inside a comment is illegal and has bitten twice."""
    for p in files(".svg"):
        try:
            ET.parse(p)
        except ET.ParseError as e:
            bad.append(f"{p.relative_to(ROOT)}: malformed SVG -- {e}")


# Strings that only ever appear in the academicpages demo content. This exists
# because /cv/ served the template's fictional degrees, numbered placeholder
# skills and invented talks -- publicly, on a tenure-case site, linked from the
# sidebar -- and nothing noticed. Grep is enough; the phrases are distinctive.
TEMPLATE_TEXT = [
    "GitHub University", "Version Control Theory", "Professor Git",
    "Professor Hub", "Sub-skill", "Relevant Topic in Your Field",
    "Teaching experience 1", "Duties included: Tagging issues",
    "Duties included: Merging pull requests", "43 different slack teams",
    "Institute for Testing Science", "London School of Testing",
]


def check_template_text(bad: list[str]) -> None:
    """No page may ship the theme's placeholder content."""
    for p in files(".md", ".markdown", ".html"):
        if "_dev" in p.parts or "tests" in p.parts:
            continue
        text = p.read_text(errors="replace")
        for phrase in TEMPLATE_TEXT:
            if phrase in text:
                bad.append(f"{p.relative_to(ROOT)}: academicpages placeholder text "
                           f"still present -- {phrase!r}")


def check_python(bad: list[str]) -> None:
    for p in files(".py"):
        try:
            compile(p.read_text(), str(p), "exec")
        except SyntaxError as e:
            bad.append(f"{p.relative_to(ROOT)}:{e.lineno}: {e.msg}")


def main() -> int:
    bad: list[str] = []
    for name, fn in [("liquid", check_liquid), ("front matter", check_front_matter),
                     ("data", check_data), ("svg", check_svg),
                     ("template text", check_template_text), ("python", check_python)]:
        before = len(bad)
        fn(bad)
        n = len(bad) - before
        print(f"  {name:14} {'FAIL' if n else 'ok'}{f'  ({n})' if n else ''}")
    if bad:
        print(f"\n{len(bad)} problem(s) -- push blocked:\n")
        for b in bad:
            print(f"  {b}")
        print("\nThese break the Pages build. A failed build does not take the site "
              "down;\nit leaves the PREVIOUS site published, so the error is silent.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
