# `_dev/` — how this site is generated

Most pages here are **generated**, not hand-written. The narrative prose is
authored in `_dev/data/*.yaml`; the enumerative facts (publication counts,
award lists, course numbers, figure paths) are derived. A page carrying the
generated banner will be overwritten — edit the record, not the page.

```
python3 _dev/generators/generate_umbrella_pages.py   # research, teaching, service, people
python3 _dev/generators/generate_research_pages.py   # the six research/<slug>/ pages
```

Everything needed to do that lives in this directory:

| | |
|---|---|
| `data/` | the authored records — the single source of truth |
| `model/` | site model: `sites.yaml`, URL architecture, design and writing style |
| `generators/` | the generators and `_paths.py`, which locates the two above |
| `figure-toolkit/` | the SVG sensors (`check_figures.py`) |

Checks live one level up in `tests/`: `syntax.py` (also the pre-push hook),
`alignment.py` (the obligation engine), `layout.py` and `interaction.py`
(Playwright, against the deployed site).

## Why this directory exists

These files used to live only in a private orchestrator repo, `davis-web`,
which held this site as a submodule. That repo is to be deleted once the
consolidation finishes — and while it held the authoring source, deleting it
would have left this site able to *render* but not to *regenerate*: every page
would still serve, and no page could ever be changed at its source again.

`_paths.py` detects either layout, so the generators run correctly from here or
from the old orchestrator. `OBL-SELF-001` asserts that every record the
generators read is present in this directory, so the guarantee cannot quietly
regress.
