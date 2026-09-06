"""Locate the site and the authored records, from either checkout layout.

The generators got this treatment already (`generators/_paths.py`); the checks
did not, and the omission was invisible because of how they fail. Each check
computed `SITE = ROOT / "repos/davisjam.github.io"`, which is correct when run
from the davis-web orchestrator and wrong when run from the copy inside the
site, where it resolves to `<site>/repos/davisjam.github.io` -- a path that
does not exist.

That mattered more than a stack trace, because a11y.py treats a missing
axe-core as "tool absent, skip rather than fail" so a fresh clone can still
push. With the wrong SITE it looked for axe under the non-existent path, took
the skip branch, and the pre-push accessibility gate reported success while
scanning nothing. A silent pass on a legal-obligation gate.

Both layouts are detected rather than configured:

    davis-web/checks/...     site at repos/davisjam.github.io, data at davis-web/data
    <site>/tests/...         site at <site>,                   data at <site>/_dev/data
"""

from __future__ import annotations

import pathlib


def _resolve() -> tuple[pathlib.Path, pathlib.Path, pathlib.Path]:
    here = pathlib.Path(__file__).resolve().parent          # checks/ or tests/
    root = here.parent                                      # davis-web  or  <site>

    site = root / "repos/davisjam.github.io"
    if site.is_dir():
        return root, site, root / "data"                    # orchestrator layout

    if (root / "_pages").is_dir():
        return root, root, root / "_dev/data"                # in-site layout

    raise SystemExit(
        f"cannot locate the site from {here}: expected either "
        f"<root>/repos/davisjam.github.io/ or <site>/tests/")


ROOT, SITE, DATA = _resolve()
MODEL = DATA.parent / "model" if DATA.name == "data" else DATA.parent / "model"
