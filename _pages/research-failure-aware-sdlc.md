---
layout: research-project
title: "Failure-Aware Software Development"
permalink: /research/failure-aware-sdlc/
author_profile: true
research_slug: "FA-SDLC"
question: "What can engineering organizations learn from the ways software fails?"
figure: /assets/research/failure-aware-sdlc/failure-learning-loop.svg
figure_alt: "Learning from failure means changing the next system"
figure_desc: "An assumption fails in a real system. What happened is preserved as evidence: reports, artifacts, decisions and consequences. Comparing incidents identifies the failure mechanism — which assumption failed and under what conditions. Generalizing beyond the incident yields a reusable claim about how systems fail. Institutionalizing that claim changes requirements, design, analysis, validation, process and governance, which in turn changes the conditions under which the next system is built."
---

Software failures are investigated, patched, and filed away. The engineering knowledge they contain rarely survives the incident that produced it, so organizations meet the same class of failure again in the next system.

We study failures empirically and ask what would have to change for that knowledge to persist. Some of our work characterizes how failures recur across systems and domains; other work examines whether evidence from past failures actually changes engineering decisions, and how organizations might structure requirements, design, and validation so that it does.

## Characterizing how software fails

Before failures can teach anything, we have to know what recurs. This work asks what failure studies actually establish, and whether the same engineering problems appear across systems and domains.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1183&context=ecepubs">Reflections on Software Failure Analysis</a></span><br><span class="venue">ESEC/FSE-IVR &middot; 2022</span><br><span class="note">Surveyed how failure studies are actually conducted and found the methods inconsistent, which is the problem the rest of this program addresses.</span></li>
  <li><span class="pub-title"><a href="https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1180&context=ecepubs">Reflecting on Recurring Failures in IoT Development</a></span><br><span class="venue">ASE-NIER &middot; 2022</span><br><span class="note">Showed that IoT failures recur through a small number of design flaws, so the knowledge to prevent them existed before the failures happened.</span></li>
</ul>

## Building evidence from failures

Individual failures are useful evidence only if they can be accumulated and analyzed. We study how to turn incident reports and other records of failure into evidence about recurring engineering problems.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2406.08221">FAIL: Analyzing Software Failures from the News Using LLMs</a></span><br><span class="venue">ASE &middot; 2024</span><br><span class="note">FAIL scales failure analysis by extracting incidents from news reports, so the evidence base stops being limited to what one team can read.</span></li>
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/SinglaAnandayuvarajKaluSchorlemmerDavis-LLMsForSupplyChainFailureAnalysis-SCORED2023.pdf">An Empirical Study on Using Large Language Models to Analyze Software Supply Chain Security Failures</a></span><br><span class="venue">SCORED &middot; 2023</span><br><span class="note">Tests whether language models can do the reading that failure analysis requires, which is the bottleneck on doing it at scale.</span></li>
</ul>

## Turning failure into engineering knowledge

Finding patterns is not enough. We study what can actually be learned from failures, and how that knowledge can be represented so it survives the incident that produced it.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2509.06301">Learning From Software Failures: A Case Study at a National Space Research Center</a></span><br><span class="venue">ICSE &middot; 2026</span><br><span class="note">A case study inside a national space research center: what an organization with strong incentives to learn from failure actually does.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2310.01653">On the Contents and Utility of IoT Cybersecurity Guidelines</a></span><br><span class="venue">PACMSE &middot; 2024</span><br><span class="note">IoT security guidelines are a written form of failure knowledge; this asks what they contain and whether they are usable by the engineers they target.</span></li>
</ul>

## Getting knowledge back into engineering decisions

The final problem is closing the loop. Even good evidence has little value if it does not reach the people making decisions, or alter the structures through which engineering proceeds.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/AnandayuvarajThulluriFigueroaShandilyaDavis-FailureKnowledgeAndDesignDecisions-SERP4IoT2023.pdf">Incorporating Failure Knowledge into Design Decisions for IoT Systems: A Controlled Experiment on Novices</a></span><br><span class="venue">SERP4IoT &middot; 2023</span><br><span class="note">A controlled study of whether failure knowledge changes design decisions. Moves the claim from plausible to tested.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2508.14796">A Guide to Stakeholder Analysis for Cybersecurity Researchers</a></span><br><span class="venue">arXiv &middot; 2025</span><br><span class="note">Failure knowledge only changes engineering if it reaches the people who decide; stakeholder analysis is the missing step in most such work.</span></li>
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/KaluSchorlemmerChenRobinsonKocinareDavis-PPPTheory-FSEIVR2023.pdf">Reflecting on the use of the Policy-Process-Product Theory in Empirical Software Engineering</a></span><br><span class="venue">ESEC/FSE-IVR &middot; 2023</span><br><span class="note">Examines the assumption underlying most of empirical software engineering — that policy and process shape product quality — and asks how often it is actually established rather than assumed.</span></li>
</ul>
