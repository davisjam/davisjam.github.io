# Patent grant dates — verification status

Two grant years disagreed between James's CV-derived list and
`publications.json`. Checked against Google Patents on 2026-09-04.

| Id | Title | CV list | publications.json | Google Patents |
|---|---|---|---|---|
| Pa-8 | Detection of file corruption in a distributed file system | granted 2018 | 2018 | **US10229121B2 — filed 2016-03-15, granted 2019-03-12** |
| Pa-3 | Verification of the integrity of data files stored in CoW | granted 2021 | 2021 | US11176090B2 — filed 2019-01-28, granted 2021-11-16 ✓ |
| Pa-2 | Determining a validity of an event emitter based on a rule | granted 2024 | 2021 | US20220374265A1 (application) — filed 2021-05-19, published 2022-11-24 |
| Pa-4..Pa-7 | — | — | — | not yet retrieved (rate-limited) |

## What this suggests

`publications.json` appears to carry **filing** or application-publication years
in at least some rows, while the CV list carries **grant** years. Pa-2 is the
clearest case: filed 2021 (publications.json's value), application published
2022, and a 2024 grant is entirely consistent with that timeline — so James's
"granted 2024" is likely right and 2021 is the filing year.

Pa-8 is the interesting one: **both** sources say 2018, but Google Patents has
the grant at 2019-03-12 (filed 2016). Neither source matches.

## Status

Google Patents rate-limited (HTTP captcha page) after ~6 queries; PatentsView
now requires an API key. Pa-4 through Pa-7 are unresolved.

Do NOT edit the years in data/publications.yaml from this table alone. Pa-8 in
particular needs James to confirm which date the CV should carry -- grant date
(2019-03-12) or something else. Re-run the lookup once the rate limit clears:

    python3 generators/verify_patents.py     # (to be written; see git log)

Quoted exact-phrase queries work; unquoted ones get captcha'd faster:

    curl -s -G https://patents.google.com/xhr/query \
      --data-urlencode 'url=q="Detection of file corruption in a distributed file system"'

---

## Resolved 2026-09-04 — exact Google Patents records

Resolved by NUMBER, not title search: several IBM inventions have near-identical
titles, so a generated search link could point at the wrong grant.

| Id | Number | Filed | Granted | Prior sources |
|---|---|---|---|---|
| Pa-2 | US11875185B2 | 2021-05-19 | **2024-01-16** | list said 2024 ✓, json said 2021 (the filing year) |
| Pa-3 | US11176090B2 | 2019-01-28 | 2021-11-16 | both said 2021 ✓ |
| Pa-5 | US10891174B1 | 2019-09-19 | **2021-01-12** | both said 2021 ✓ |
| Pa-6 | US10642796B2 | 2017-07-18 | **2020-05-05** | both said 2020 ✓ |
| Pa-7 | US10614039B2 | 2017-04-04 | **2020-04-07** | list said 2018 ✗, json said 2020 ✓ |
| Pa-8 | US10229121B2 | 2016-03-15 | **2019-03-12** | both said 2018 ✗ |

Two corrections to the CV-derived list: Pa-7 granted 2020, not 2018; Pa-8 granted
2019, not 2018. Both now take the record.

**Pa-4 remains unresolved.** Four query phrasings returned nothing from Google
Patents. It is rendered with no link rather than pointed at a guess.

**Pa-1 is a Purdue provisional** (63/813,549). Provisionals have no public Google
Patents record, so it is labelled and carries no link.
