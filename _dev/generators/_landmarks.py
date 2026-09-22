"""Resolve {{landmark:NAME}} references against model/sites.yaml.

WHY THIS EXISTS. The MAGE book URL was written literally into three records and
drifted to two different values, one of which pointed at a redirect stub titled
"Moved" -- so the Publications page linked the book to a placeholder. A status
check could not see it: a stub returns a healthy 200.

The first fix was a parity check: keep the three copies, fail when they
disagree. That is the weakest rung. It still permits N copies, it only reports
after the fact, and it needs updating every time a new surface appears.

This is the unification instead. The URL exists ONCE, in the sites.yaml landmark
block. Every other record names the landmark and gets the value substituted at
generation time, so disagreement is not detected -- it is unrepresentable.

Usage, in prose or in a structured field:

    "...openly available through [Teach with MAGE]({{landmark:course_mirror}})."
    url: "{{landmark:book}}"

An unknown name raises rather than silently emitting an empty href: a link to
nowhere is worse than a failed build.
"""

from __future__ import annotations

import re

import yaml

import _paths

_TOKEN = re.compile(r"\{\{landmark:([a-z_]+)\}\}")


def landmarks() -> dict[str, str]:
    """The landmark block, flattened across sites. Names are unique by
    construction -- the check that enforces that is OBL-LINK-007."""
    sites = yaml.safe_load((_paths.DATA.parent / "model" / "sites.yaml").read_text())
    out: dict[str, str] = {}
    for s in sites.get("sites", []):
        for k, v in (s.get("landmarks") or {}).items():
            out[k] = v
    return out


def resolve(text: str, known: dict[str, str] | None = None) -> str:
    """Substitute every {{landmark:NAME}} in a string."""
    known = known if known is not None else landmarks()

    def sub(m: re.Match[str]) -> str:
        name = m.group(1)
        if name not in known:
            raise KeyError(
                f"unknown landmark {name!r} -- model/sites.yaml defines "
                f"{sorted(known)}. Add it there rather than inlining a URL.")
        return known[name]

    return _TOKEN.sub(sub, text)
