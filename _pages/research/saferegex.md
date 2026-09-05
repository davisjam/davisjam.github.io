---
layout: research-project
title: "Regular Expression Engineering"
permalink: /research/saferegex/
author_profile: true
research_slug: "Regex"
question: "What do small, heavily reused program fragments reveal about software engineering?"
figure: /assets/research/saferegex/research-arc.svg
figure_alt: "Three lines of inquiry running concurrently rather than in succession. Together they showed that small reused artifacts carry hidden assumptions across languages, developers, and runtimes."
figure_caption: "Three lines of inquiry running concurrently rather than in succession. Together they showed that small reused artifacts carry hidden assumptions across languages, developers, and runtimes."
---

A regular expression is a few characters long and is copied between languages, libraries, and projects with little thought. That makes it a useful subject: the same artifact is reused across many contexts, so its behaviour exposes assumptions that larger components hide.

We have examined regexes along three lines that ran concurrently for most of a decade. One asks whether a regex means the same thing when it moves between languages. One asks what developers actually understand about the expressions they write. The third asks what a matching engine does with them, including the conditions under which matching becomes a denial-of-service vector, and what can be done about it.

## Where the program began

The work started with a runtime problem: a single expensive input could stall an entire event-driven server. That framing — performance as a security property — set up everything that followed.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/DavisKildowLee-EHP-EuroSec17.pdf">The case of the poisoned event handler: Weaknesses in the Node.js event-driven architecture</a></span><br><span class="venue">EuroSec &middot; 2017</span><br><span class="note">The event-handler poisoning weakness in Node.js, which is where the performance-as-a-security-property line of work began.</span></li>
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/DavisWilliamsonLee-SenseOfTime-USENIXSecurity18.pdf">A Sense of Time for JavaScript and Node.js: First-Class Timeouts as a Cure for Event Handler Poisoning</a></span><br><span class="venue">SECURITY &middot; 2018</span><br><span class="note">First-class timeouts as a defence against event-handler poisoning. The runtime-side answer that preceded the regex-specific work.</span></li>
</ul>

## The scale of the problem

Measuring an ecosystem rather than an example turned a known theoretical hazard into a demonstrated, widespread one.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/DavisCoghlanServantLee-EcosystemREDOS-ESECFSE18.pdf">The Impact of Regular Expression Denial of Service (REDOS) in Practice: an Empirical Study at the Ecosystem Scale</a></span> <span class="award">best paper</span><br><span class="venue">ESEC/FSE &middot; 2018</span><br><span class="note">Measured ReDoS across an ecosystem and found super-linear regexes widespread in deployed modules. The result that made the problem concrete.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2406.11618">SoK: A Literature and Engineering Review of Regular Expression Denial of Service</a></span><br><span class="venue">AsiaCCS &middot; 2025</span><br><span class="note">Consolidates a decade of ReDoS literature and engineering practice into one account of what is known and what is still open.</span></li>
</ul>

## What developers actually do

If regexes are hard to reason about, the difficulty is a software-engineering finding, not a user error.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/MichaelDonohueDavisLeeServant-RegexesAreHard-ASE19.pdf">Regexes are Hard: Decision-making, Difficulties, and Risks in Programming Regular Expressions</a></span> <span class="award">best paper</span><br><span class="venue">ASE &middot; 2019</span><br><span class="note">Studied what developers understand when they write regexes, and found the difficulties are in comprehension and decision-making, not syntax.</span></li>
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/DavisMoyerKazerouniLee-RegexGeneralizability-ASE19.pdf">Testing Regex Generalizability And Its Implications: A Large-Scale Many-Language Measurement Study</a></span><br><span class="venue">ASE &middot; 2019</span><br><span class="note">Tested whether regex behaviour generalizes across languages at scale. It does not, which turns portability into an engineering problem.</span></li>
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/DavisMichaelCoghlanServantLee-LinguaFranca-ESECFSE19.pdf">Why Aren't Regular Expressions a Lingua Franca? An Empirical Study on the Re-use and Portability of Regular Expressions</a></span><br><span class="venue">ESEC/FSE &middot; 2019</span><br><span class="note">Asked why regexes are not portable in practice despite a shared surface syntax, examining reuse across languages directly.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2503.20579">Is Reuse All You Need? A Systematic Comparison of Regular Expression Composition Strategies</a></span><br><span class="venue">arXiv &middot; 2025</span><br><span class="note">Compares strategies for composing regexes, asking whether reuse is the right default at the level of the expression itself.</span></li>
</ul>

## Defences and engine design

The final line of work asks what to change: the expression, the sanitizer, or the engine itself.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/Davis-RethinkingRegexEngines-FSE19-SRC-paper.pdf">Rethinking Regex Engines to Address ReDoS</a></span><br><span class="venue">ACM Joint Meeting on European Software Engineeri &middot; 2019</span><br><span class="note">Argued the problem is in the engines: worst-case-exponential matching is an implementation choice, not a property of regular expressions.</span></li>
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/DavisServantLee-SelectiveMemo-IEEE-SP21.pdf">Using Selective Memoization to Defeat Regular Expression Denial of Service (ReDoS)</a></span><br><span class="venue">S&P &middot; 2021</span><br><span class="note">Selective memoization defeats ReDoS without abandoning the expressive features that made backtracking engines popular.</span></li>
  <li><span class="pub-title"><a href="https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1179&context=ecepubs">Exploiting Input Sanitization for Regex Denial of Service</a></span><br><span class="venue">ICSE &middot; 2022</span><br><span class="note">Published sanitization logic tells an attacker which inputs reach the matcher, turning a usability feature into an exploitation aid.</span></li>
  <li><span class="pub-title"><a href="https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1178&context=ecepubs">Improving Developers' Understanding of Regex Denial of Service Tools through Anti-Patterns and Fix Strategies</a></span><br><span class="venue">S&P &middot; 2023</span><br><span class="note">ReDoS tools exist but developers misread their output; this studies how to present findings so they can be acted on.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2602.21459">Regular Expression Denial of Service Induced by Backreferences</a></span><br><span class="venue">arXiv &middot; 2026</span><br><span class="note">Backreferences reintroduce the vulnerability under different conditions, marking the current boundary of the security result.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2603.00311">Towards the Systematic Testing of Regular Expression Engines</a></span><br><span class="venue">JAWs &middot; 2026</span><br><span class="note">Regex engines themselves are largely untested against their own semantics; this proposes testing them systematically.</span></li>
  <li><span class="pub-title">On the Impact and Defeat of Regex DoS</span><br><span class="note">The Student Research Competition statement of the ReDoS problem and its defences.</span></li>
</ul>

## Funding and support

This work has been supported by:

- **US National Science Foundation** — [Collaborative Research: SaTC: CORE: Small: Improving Sanitization and Avoiding Denial of Service Through Correct and Safe Regexes](https://www.nsf.gov/awardsearch/show-award/?AWD_ID=2135156) (#2135156)
