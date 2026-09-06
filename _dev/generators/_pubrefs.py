"""Where a publication record's link comes from -- one answer, four consumers.

Patents used to store patent_number AND paper_url AND links.record: three
surfaces for one fact, which disagreed. Collapsing them to the number alone and
deriving the URL fixed that -- but only in generate_publications_page.py, the
generator I happened to be looking at. Three others read paper_url directly, so
the research landing and the programme pages silently lost every patent link.
Fixing the record exposed the duplication the record had been hiding.

So the resolution lives here and every consumer calls it. A new link kind is
added once.
"""

from __future__ import annotations


def paper_link(p: dict) -> str | None:
    """The best URL for a record, or None when there genuinely isn't one.

    Order matters: an explicit paper_url is authored intent and always wins. A
    derived patent URL is a fallback, not an override, so a record that needs to
    point somewhere unusual still can.
    """
    url = p.get("paper_url") or (p.get("links") or {}).get("record")
    if url:
        return url

    # Patents identify by grant number and the URL is a function of it.
    # Provisional applications have no published page, so they resolve to None
    # rather than to a link that 404s.
    num = p.get("patent_number")
    return f"https://patents.google.com/patent/{num}/en" if num else None
