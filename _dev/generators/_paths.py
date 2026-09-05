"""Where the authored records and the site live, from either checkout layout.

The generators were written to run from the private davis-web orchestrator,
which holds the site as `repos/davisjam.github.io/`. That repo is scheduled for
deletion once the consolidation is finished -- but it still holds the AUTHORED
source (`data/*.yaml` and these generators), while the site carries only their
generated output. Deleting it in that state would leave the site unable to
regenerate itself: every page would still render, and nothing could be changed
at the source again.

So the same generators now run from either place:

    davis-web/generators/...          data at davis-web/data/,   site at repos/…
    <site>/_dev/generators/...        data at <site>/_dev/data/, site at <site>

Both layouts are detected rather than configured, so no environment variable or
flag has to be threaded through, and a copy in either location just works.
"""

from __future__ import annotations

import pathlib


def _resolve() -> tuple[pathlib.Path, pathlib.Path]:
    here = pathlib.Path(__file__).resolve().parent          # .../generators
    orchestrator = here.parent                              # davis-web  OR  <site>/_dev

    site = orchestrator / "repos/davisjam.github.io"
    if site.is_dir():
        return orchestrator / "data", site                  # davis-web layout

    site = orchestrator.parent                              # <site>
    if (site / "_pages").is_dir():
        return orchestrator / "data", site                  # in-site layout

    raise SystemExit(
        f"cannot locate the site from {here}: expected either "
        f"<root>/repos/davisjam.github.io/ or <site>/_dev/generators/")


DATA, SITE = _resolve()
PAGES = SITE / "_pages"
MODEL = DATA.parent / "model"
