---
layout: research-project
title: "Regular Expression Engineering"
permalink: /research/saferegex/
author_profile: true
research_slug: "Regular Expressions"
question: "What can regular expressions, viewed through a software-engineering microscope, teach us about building software?"
figure: /assets/research/saferegex/regex-microscope.svg
figure_alt: "A software-engineering microscope"
figure_desc: "A regular expression, described as one line of software, sits at the centre of three radial spokes with no enclosing triangle. The spokes are three perspectives on the same artifact: regex theory asks what it should mean; human factors asks how people reason about it; regex engines ask what happens when it runs. The research results sit in the open sectors between the spokes. Between theory and human factors, portability and composition asks whether meaning survives movement and reuse. Between theory and engines, realization asks whether the engine realizes the intended semantics safely. Between human factors and engines, security in practice asks whether developers can recognize and control pathological behavior."
---

Regular expressions are a niche topic, and that is part of why they are useful to study. A regex may be only one line of code, yet it is an unusually compact meeting point between formal semantics, human programming behavior, and the implementation choices of the engine that executes it. Many of the problems of software engineering become visible here at a scale where we can study them closely.

That perspective is personal as well as methodological. At IBM, I maintained hundreds of regular expressions used to parse the unstable and largely unspecified output of dozens of command-line tools and their many operating modes. Small expressions became critical infrastructure: reused constantly, difficult to reason about, and dependent on assumptions scattered across languages, runtimes, and evolving interfaces.

We study regular expressions as software artifacts. Across this program, we have asked what their formal semantics promise, how developers understand and reuse them, and how matching engines realize them in practice. Bringing those perspectives together exposes gaps that are easy to miss when any one layer is studied alone.

## A small artifact can become critical infrastructure

The programme began with a runtime failure: a single expensive input could stall an entire event-driven server, because one regular expression sat on the path every request took. That framing — performance as a security property — set up everything that followed, and measuring the ecosystem rather than the example turned a known theoretical hazard into a demonstrated and widespread one.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/DavisKildowLee-EHP-EuroSec17.pdf">The case of the poisoned event handler: Weaknesses in the Node.js event-driven architecture</a></span><br><span class="venue">EuroSec &middot; 2017</span><br><span class="note">The event-handler poisoning weakness in Node.js, which is where the performance-as-a-security-property line of work began.</span></li>
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/DavisWilliamsonLee-SenseOfTime-USENIXSecurity18.pdf">A Sense of Time for JavaScript and Node.js: First-Class Timeouts as a Cure for Event Handler Poisoning</a></span><br><span class="venue">SECURITY &middot; 2018</span><br><span class="note">First-class timeouts as a defence against event-handler poisoning. The runtime-side answer that preceded the regex-specific work.</span></li>
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/DavisCoghlanServantLee-EcosystemREDOS-ESECFSE18.pdf">The Impact of Regular Expression Denial of Service (REDOS) in Practice: an Empirical Study at the Ecosystem Scale</a></span> <span class="award">best paper</span><br><span class="venue">ESEC/FSE &middot; 2018</span><br><span class="note">Measured ReDoS across an ecosystem and found super-linear regexes widespread in deployed modules. The result that made the problem concrete.</span></li>
</ul>

## Shared syntax does not guarantee shared meaning

Regular expression syntax looks portable, and developers reuse it as though it were. It is not. Dialects disagree about what an expression matches, behaviour learned in one language does not transfer intact to another, and composing expressions introduces assumptions that neither part carried alone.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/DavisMoyerKazerouniLee-RegexGeneralizability-ASE19.pdf">Testing Regex Generalizability And Its Implications: A Large-Scale Many-Language Measurement Study</a></span><br><span class="venue">ASE &middot; 2019</span><br><span class="note">Tested whether regex behaviour generalizes across languages at scale. It does not, which turns portability into an engineering problem.</span></li>
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/DavisMichaelCoghlanServantLee-LinguaFranca-ESECFSE19.pdf">Why Aren't Regular Expressions a Lingua Franca? An Empirical Study on the Re-use and Portability of Regular Expressions</a></span><br><span class="venue">ESEC/FSE &middot; 2019</span><br><span class="note">Asked why regexes are not portable in practice despite a shared surface syntax, examining reuse across languages directly.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2503.20579">Is Reuse All You Need? A Systematic Comparison of Regular Expression Composition Strategies</a></span><br><span class="venue">arXiv &middot; 2025</span><br><span class="note">Compares strategies for composing regexes, asking whether reuse is the right default at the level of the expression itself.</span></li>
</ul>

## Compact notation does not make reasoning easy

If a one-line artifact is hard to reason about, that is a software-engineering finding rather than a user error. We study what developers actually understand about the expressions they write and reuse, and what an analysis tool has to explain before its findings can be acted on.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/MichaelDonohueDavisLeeServant-RegexesAreHard-ASE19.pdf">Regexes are Hard: Decision-making, Difficulties, and Risks in Programming Regular Expressions</a></span> <span class="award">best paper</span><br><span class="venue">ASE &middot; 2019</span><br><span class="note">Studied what developers understand when they write regexes, and found the difficulties are in comprehension and decision-making, not syntax.</span></li>
  <li><span class="pub-title"><a href="https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1178&context=ecepubs">Improving Developers' Understanding of Regex Denial of Service Tools through Anti-Patterns and Fix Strategies</a></span><br><span class="venue">S&P &middot; 2023</span><br><span class="note">ReDoS tools exist but developers misread their output; this studies how to present findings so they can be acted on.</span></li>
</ul>

## Execution is part of the semantics that matter

What an expression means in practice includes what the engine does to produce that meaning. Backtracking implementations turn ordinary expressions into pathological ones on some inputs, so the questions of which semantics to preserve, and at what cost, belong to engine design — not solely to the programmer writing the expression.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/Davis-RethinkingRegexEngines-FSE19-SRC-paper.pdf">Rethinking Regex Engines to Address ReDoS</a></span><br><span class="venue">ACM Joint Meeting on European Software Engineeri &middot; 2019</span><br><span class="note">Argued the problem is in the engines: worst-case-exponential matching is an implementation choice, not a property of regular expressions.</span></li>
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/DavisServantLee-SelectiveMemo-IEEE-SP21.pdf">Using Selective Memoization to Defeat Regular Expression Denial of Service (ReDoS)</a></span><br><span class="venue">S&P &middot; 2021</span><br><span class="note">Selective memoization defeats ReDoS without abandoning the expressive features that made backtracking engines popular.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2602.21459">Regular Expression Denial of Service Induced by Backreferences</a></span><br><span class="venue">arXiv &middot; 2026</span><br><span class="note">Backreferences reintroduce the vulnerability under different conditions, marking the current boundary of the security result.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2603.00311">Towards the Systematic Testing of Regular Expression Engines</a></span><br><span class="venue">JAWs &middot; 2026</span><br><span class="note">Regex engines themselves are largely untested against their own semantics; this proposes testing them systematically.</span></li>
</ul>

## Security failures cross the layers

ReDoS is not a defect in any single layer. It appears when a formal property, a developer's expectation, and an implementation's cost model disagree, so a defense has to hold at whichever layer is reachable. Sanitization intended to make input safe can itself introduce the vulnerability — and the ecosystem study, the anti-pattern work, and the backreference results above each show, from a different direction, that addressing one view alone leaves the others open.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1179&context=ecepubs">Exploiting Input Sanitization for Regex Denial of Service</a></span><br><span class="venue">ICSE &middot; 2022</span><br><span class="note">Published sanitization logic tells an attacker which inputs reach the matcher, turning a usability feature into an exploitation aid.</span></li>
  <li><span class="pub-title">On the Impact and Defeat of Regex DoS</span><br><span class="note">The Student Research Competition statement of the ReDoS problem and its defences.</span></li>
</ul>

## What the regex microscope revealed

Across these studies, the recurring lesson is that even very small software artifacts cross boundaries between specification, human understanding, and implementation. Reuse carries assumptions across those boundaries; failures appear when the assumptions do not travel with the artifact.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2406.11618">SoK: A Literature and Engineering Review of Regular Expression Denial of Service</a></span><br><span class="venue">AsiaCCS &middot; 2025</span><br><span class="note">Consolidates a decade of ReDoS literature and engineering practice into one account of what is known and what is still open.</span></li>
</ul>

## Funding and support

This work has been supported by:

- **US National Science Foundation** — [Collaborative Research: SaTC: CORE: Small: Improving Sanitization and Avoiding Denial of Service Through Correct and Safe Regexes](https://www.nsf.gov/awardsearch/show-award/?AWD_ID=2135156) (#2135156)
