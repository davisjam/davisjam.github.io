---
layout: research-project
title: "Embedded Software Engineering"
permalink: /research/embedded-swe/
author_profile: true
research_slug: "Embedded SWE"
question: "How can analysis and assurance become practical for embedded software?"
figure: /assets/research/embedded-swe/research-lineage.svg
figure_alt: "Four lines of attack on reliable embedded software"
figure_desc: "Four complementary lines of work meet at practical assurance. Understanding failure asks what goes wrong in real embedded software, through packet validation and layering violations. Making code reachable asks how firmware can be analyzed away from its hardware, through rehosting, LEMIX and bottom-up testing. Analyzing at scale asks whether useful analyses can become cheap enough to apply broadly, using CodeQL and OSS-Fuzz-Gen. Establishing guarantees asks whether verification can become an ordinary engineering step, through Unit Proofing, compositional bounded model checking and AutoSOUP."
---

Embedded software runs where failures are expensive, and in conditions that defeat the assumptions most analysis tools are built on: no operating system to speak of, hardware that the analysis cannot reach, and code that cannot simply be run in a test harness.

Our work has attacked that gap in stages. We studied defects in real embedded network stacks, built rehosting infrastructure so firmware can execute away from its target hardware, and applied static analysis at a scale where it finds hundreds of defects across many projects. A current thrust, Unit Proofing, asks whether component-level formal verification can be made cheap enough to use as an ordinary engineering step rather than a special occasion.

## Understanding embedded failures

Embedded software runs where failures are expensive, under conditions that defeat the assumptions most analysis tools are built on. This work establishes what actually goes wrong, and why the usual techniques do not reach it.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2308.10965">Systematically Detecting Packet Validation Vulnerabilities in Embedded Network Stacks</a></span><br><span class="venue">ASE &middot; 2023</span><br><span class="note">Found high-severity defects in the network stacks that low-resource devices depend on, and showed the defects were systematic enough to look for deliberately. The empirical start of the line.</span></li>
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/ShenDavisMachiry-NCMAs-LCTES23.pdf">Towards Automated Identification of Layering Violations in Embedded Applications (WIP)</a></span><br><span class="venue">LCTES &middot; 2023</span><br><span class="note">Layered design is what makes embedded software portable, so violations of the layering are a defect class worth detecting automatically.</span></li>
</ul>

## Making the code reachable

Analysis cannot begin until the software can be executed and inspected away from the hardware it was written for. Rehosting turns embedded applications into something ordinary tools can work on.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/SrinivasanTanksalkarAmusuoDavisMachiry-Rehosting-DSN2023.pdf">Towards Rehosting Embedded Applications as Linux Applications</a></span><br><span class="venue">DSN-Disrupt &middot; 2023</span><br><span class="note">First statement of rehosting embedded applications as ordinary Linux programs, so dynamic analysis no longer waits on hardware emulation.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2503.17588">LEMIX: Enabling Testing of Embedded Applications as Linux Applications</a></span><br><span class="venue">SECURITY &middot; 2025</span><br><span class="note">LEMIX made that rehosting practical: embedded applications become testable as Linux applications, removing the fidelity-versus-effort tradeoff earlier approaches were stuck with.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2509.03711">Reactive Bottom-Up Testing</a></span><br><span class="venue">arXiv &middot; 2025</span><br><span class="note">Reactive bottom-up testing: reaching deep code by building tests upward from the units rather than driving from the top.</span></li>
</ul>

## Analysis at ecosystem scale

Once analysis is affordable, the question becomes what it finds when pointed at many real projects rather than one.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2310.00205">Usage and Effectiveness of Static Analysis in Open-Source Embedded Software: CodeQL Finds Hundreds of Defects</a></span><br><span class="venue">ISSTA &middot; 2025</span><br><span class="note">Applied static analysis across many open-source embedded projects and found hundreds of defects, showing that analysis at ecosystem scale is affordable and that projects were not already doing it.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2510.02185">Lessons from Mitigating False Positives in Google's OSS-Fuzz-Gen</a></span><br><span class="venue">FSE-Industry &middot; 2026</span><br><span class="note">False positives are what make automated fuzz-driver generation unusable in practice; this reports what reducing them took inside Google's OSS-Fuzz-Gen.</span></li>
</ul>

## From defect detection to guarantees

A found defect is weaker than a guaranteed absence. The current thrust asks whether component-level verification can be made cheap enough to use as an ordinary engineering step.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2410.14818">A Unit Proofing Framework for Code-level Verification: A Research Agenda</a></span><br><span class="venue">ICSE-NIER &middot; 2025</span><br><span class="note">Sets out the Unit Proofing agenda: design-level verification does not expose implementation defects, so verification has to reach the code.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2503.13762">Do Unit Proofs Work? An Empirical Study of Compositional Bounded Model Checking for Memory Safety Verification</a></span><br><span class="venue">ICSE &middot; 2026</span><br><span class="note">Asked whether unit proofs work rather than assuming they do, and measured compositional bounded model checking for memory safety on real code.</span></li>
  <li><span class="pub-title">AutoSOUP: Safety-Oriented Unit Proof Generation for Component-level Memory-Safety Verification</span><br><span class="note">AutoSOUP generates the proofs. Automating construction is what moves unit proofing from a technique that works to one a team can afford to use.</span></li>
</ul>

## Funding and support

This work has been supported by:

- **Rolls-Royce** — Securing Software Implementations through System Fuzz Testing and Modular Formal Methods
- **Qualcomm, Inc.** — Qualcomm Innovation Fellowship
- **OpenAI — Cybersecurity Grant Program** — AutoUP: Automated Unit Proofing
- **Rolls-Royce** — Facilitating Effective Dynamic Analysis of Embedded Software
- **Rolls-Royce** — Dynamic Security Analysis of Embedded Software Systems
- **Rolls-Royce** — Dynamic Analysis of Embedded Firmware
