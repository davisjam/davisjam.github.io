# model/ssot-records.md — enumerative records have one canonical source

> **Do not hand-maintain enumerative professional records in page prose.**
>
> **Narrative prose is hand-authored. Enumerative facts are generated.**

## 1. Why this is a rule and not a preference

The previous Service page is the worked example. It was a hand-maintained list,
so it silently stopped tracking the record around 2024 — omitting flagship
program committees, a USENIX Security vice chairship, NSF panels, ABET
self-study leadership, and workshop organization. Nothing failed. The page just
quietly became misleading by omission, which is the worst failure mode for a
page a reviewer reads to judge a career.

A list transcribed into prose has no source. It cannot be checked, cannot be
regenerated, and decays at exactly the rate the underlying record grows.

## 2. The split

```text
                         davis-web
                            │
              ┌─────────────┴─────────────┐
              │                           │
       HAND-AUTHORED                CANONICAL RECORDS
       generators/*.py              data/*.yaml
              │                           │
       research thesis              publications · patents
       teaching philosophy          grants · awards
       project narratives           courses · service
       explanatory prose            people
              │                           │
              └─────────────┬─────────────┘
                            ▼
                     PAGE REALIZATIONS
         ┌──────────────────┼──────────────────┐
         ▼                  ▼                  ▼
      Research           Teaching            Service
```

| Enumerative — generated | Narrative — authored |
|---|---|
| publications, patents | the research thesis |
| grants and funding | each program's framing |
| awards and recognition | teaching philosophy |
| courses taught | why a body of work matters |
| professional service | section framing and transitions |

The test: **if adding one more item to the list would require editing a page,
the list is in the wrong place.**

## 3. Canonical records

| File | Holds |
|---|---|
| `data/publications.yaml` | 129 works incl. patents and posters, with program membership |
| `data/funding.yaml` | 23 grants, explicit-only project edges |
| `data/awards.yaml` | research, teaching, service, mentoring, other |
| `data/service.yaml` | leadership, PCs, journals, national, Purdue |
| `data/courses.yaml` | courses taught, with terms |

## 4. The website taxonomy is not the CV taxonomy

A CV needs exhaustive reporting categories. A page needs to communicate the
*kind and trajectory* of the work. `data/service.yaml` is therefore shaped for
the page — leadership, research-community, national, Purdue — while staying
exhaustive underneath.

Two consequences worth stating, because both are easy to undo by "tidying":

- **Repeat selection is the signal.** Program committees render as venue-then-years
  (`ICSE 2025 · 2026 · 2027`), not as a reverse-chronological list, because
  repeat invitation by a flagship venue is the thing worth seeing.
- **A progression is one contribution, not three lines.** ICSE-SMeW renders as
  mentor → panelist → co-chair, because that shape is the point.

## 5. Confirmed versus planned

A record is published only when it is current or confirmed. Forthcoming roles
stay in `needs_confirmation` with the reason. Publishing a future editorship as
current would be an overclaim in an award-review context — the same discipline
as never inferring a funding edge (`content-model.md` §1 P2).

Currently held back: an NSF 2026 panel appearing in one source but not the CV
extract, and a forthcoming IEEE Computer co-editorship described as upcoming.

## 6. What is not service

Tools, practitioner writings, software impact, and download counts left the
Service page. They are research translation, and they now have better homes on
the research-program sites. Service means scholarly, professional, and
institutional service.
