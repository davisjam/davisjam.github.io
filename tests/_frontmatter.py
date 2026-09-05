"""Read a Jekyll page's YAML front matter.

Extracted 260905 because three checkers had grown their own copy of this parse
in one session, and the copies did not agree on failure:

    syntax.py     guarded a missing/unclosed block and reported it
    layout.py     guarded and skipped
    alignment.py  `text.split("---", 2)[1]`, which raises IndexError on any
                  page that has no front matter at all

So the same eight lines had three behaviours, one of which crashes the run. That
is the DRY-drift hazard in miniature: nobody chose those differences, they just
accumulated. One parse, one failure mode.

Returns None when there is no front matter, and raises yaml.YAMLError when there
IS a block and it will not parse -- the caller decides whether an unparseable
page is a finding or a crash, but never has to wonder which case it is looking
at.
"""

from __future__ import annotations

import pathlib

import yaml


def load(path: pathlib.Path | str, *, text: str | None = None) -> dict | None:
    """The page's front matter as a dict, or None if it has none.

    `text` lets a caller that has already read the file avoid a second read.
    """
    if text is None:
        text = pathlib.Path(path).read_text(errors="replace")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None                      # opened but never closed
    parsed = yaml.safe_load(text[3:end])
    return parsed if isinstance(parsed, dict) else None


def is_unclosed(text: str) -> bool:
    """True when a block opens and never closes -- worth reporting separately,
    since `load` cannot distinguish it from "no front matter" in its return."""
    return text.startswith("---") and text.find("\n---", 3) == -1
