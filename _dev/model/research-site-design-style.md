# Davis Research Site Design Style

The research project sites are **academic research pages within
davisjam.github.io**. They are not independent brands, labs, centers,
initiatives, or book sites.

A visitor should experience:

> James Davis's academic website → Research → a particular body of Davis's research.

## 1. Inheritance

```text
davisjam.github.io
├── identity · global navigation · typography
├── page geometry · accessibility · academic register
        ▼
   research-site template  →  /mage/ /software-supply-chains/ /embedded-.../ ...
```

**Not** `model-based-agentic-software-engineering → research sites`. The full
MAGE site is a book/course/resource environment. It may contribute figures,
concepts, and drawing methods. It does **not** contribute the page architecture.

## 2. Visual target

> A conventional academic research page, unusually well typeset and illustrated.

Not a branded microsite for a "research programme." The page should look
credible printed, read by a tenure evaluator, opened by a prospective PhD
student, or linked from a grant application.

Prefer **document** structure over **interface** structure: headings, prose,
figures, bibliographic entries, ordinary lists, rules and whitespace, restrained
links. Cards, pills, badges, coloured panels, oversized quotations, and
dashboard layouts only when the content genuinely requires them.

## 3. Global header — never strand the reader

Every research site carries the common Davis academic header:

```text
James Davis, PhD
Assistant Professor, ECE @ Purdue
Home   Research   Publications   Teaching   Service   About me
```

Returning to the parent site must not require reaching the bottom of a
multi-page document. Mark Research current.

## 4. Page header — begin plainly

```text
Software Supply Chains
How can software reuse remain trustworthy at ecosystem scale?
[2-3 sentence introduction]
```

**BANNED**: the eyebrow `A RESEARCH PROGRAMME OF THE DUALITY LAB`, and every
analogue — *A Davis Research Programme · A Duality Lab Initiative · Research
Initiative · Research Program · Research Area*. The H1 already tells the reader
what the page concerns. A page does not announce its own institutional category.

## 5. Local jump navigation

After the introduction, a restrained same-page anchor row over sections that
actually exist: `Overview  Research  Publications  People  Support`. Never add an
empty section to satisfy a template. This is not a second global nav.

## 6. Use the page width

Composition may use the full desktop width; running prose stays at a readable
measure. A figure beside prose is a good use of width. Five cards beside one
another is not. Layout must not turn two pages of scholarly material into five
pages of branded whitespace.

## 7. Figures explain; they do not brand

Original figures are encouraged where they make the research easier to
understand — as a **research figure within the document**, not a giant identity
device that turns the top of the page into a manifesto. Good drawings, not
illustrated books.

## 8. Section architecture

Headings come from the research, not a shared template. `Foundations` is
acceptable only if it leads to actual explanation; a compact taxonomy of nouns is
information architecture, not an academic account of the work.

## 9. Cards — default is no card

Before creating one, ask: *does the border encode a meaningful object boundary?*

Good: a person; a tool with several metadata fields; a dataset; a discrete
callout. **Bad**: a paragraph; a research topic; "Foundations"; "Applications";
a rhetorical claim; each publication; every grant.

## 10. Publications — a bibliography, not content cards

Year-grouped, restrained venue emphasis, small links. A formal award may appear
as factual metadata, rendered quietly. No promotional badges on routine papers.
Data comes from the SSOT.

## 11. Funding — academic acknowledgment, not sponsor marketing

Sponsor, title, award number. No logo wall. Relationships come from explicit
SSOT mappings, never inferred.

## 12. Footer

Common Davis footer with an obvious `← Research`. Do **not** end by announcing
"A research project of James C. Davis · Duality Lab · Purdue University" — the
surrounding website already establishes authorship, and saying it compounds the
independent-brand impression.

## 13. Responsive and print

One column on narrow screens; legible figures; wrapping jump nav; bibliographic
hierarchy preserved; no horizontal scrolling. Print/PDF stays intelligible.

## 14. Acceptance test

> If all colours and illustrations disappeared, would this still be an excellent,
> navigable academic research page?

If not, the page leans on visual packaging.

> If the H1 changed from "Software Supply Chains" to "Regular Expression
> Engineering," would the shell still work without pretending these are two
> independent organizations?

If not, the template is over-branded.

---

**Do not optimize for "designed." Optimize for "read."** The research supplies
the sophistication; the site makes it easy to understand, navigate, and verify.
