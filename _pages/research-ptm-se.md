---
layout: research-project
title: "Software Engineering for Pre-Trained Models"
permalink: /research/ptm-se/
author_profile: true
research_slug: "Pre-Trained Models"
question: "What changes about software engineering when the reused component is a learned model?"
figure: /assets/research/ptm-se/ptm-reuse-lifecycle.svg
figure_alt: "Reusing a model introduces new engineering obligations"
figure_desc: "A familiar reuse lifecycle runs across the top: model registry, select, integrate, validate, evolve. Beneath it are five claims the programme established. Reuse is familiar but the artifact is not. The ecosystem keeps moving. Identity and interoperability are not guaranteed. Reuse requires reengineering. Risk travels with the artifact."
---

Developers have been reusing software components for decades; pre-trained models inherit many of the same engineering problems, but also introduce new ones, because their identity, behavior, provenance, and interfaces are less explicit than those of conventional software packages.

We study pre-trained model reuse as a software-engineering practice. Our work asks which lessons from conventional component reuse still apply, where learned artifacts break those assumptions, and what new engineering methods are needed for selecting, integrating, validating, securing, and evolving models obtained from public registries.

## Pre-trained models are a distinct kind of software dependency

Early work in this programme established that reusing a pre-trained model is not simply a machine-learning convenience. Engineers must discover, interpret, adapt, validate, and maintain artifacts whose interfaces and provenance are less explicit than those of conventional software packages.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/DavisJajalJiangSchorlemmerSynovicThiruvathukal-DNNReuse-JVA23.pdf">Reusing Deep Learning Models: Challenges and Directions in Software Engineering</a></span><br><span class="venue">Proceedings of the IEEE John Vincent Atanasoff S &middot; 2023</span><br><span class="note">Framed model reuse as a software-engineering problem with its own challenges, rather than a machine-learning convenience.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2303.02552">An Empirical Study of Pre-Trained Model Reuse in the Hugging Face Deep Learning Model Registry</a></span><br><span class="venue">ICSE &middot; 2023</span><br><span class="note">The empirical study of Hugging Face reuse that established how engineers select and adapt pre-trained models at ecosystem scale.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2509.06085">Software Dependencies 2.0: An Empirical Study of Reuse and Integration of Pre-Trained Models in Open-Source Projects</a></span><br><span class="venue">arXiv &middot; 2025</span><br><span class="note">Generalizes dependency thinking to model artifacts: what a dependency is, when the dependency learns.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2310.01642">'I see models being a whole other thing': An Empirical Study of Pre-Trained Model Naming Conventions and A Tool for Enhancing Naming Consistency</a></span><br><span class="venue">EMSE &middot; 2025</span><br><span class="note">Interview study of how engineers reason about pre-trained models as components, including where model naming misleads them.</span></li>
</ul>

## The model ecosystem must be measured

Pre-trained model ecosystems change quickly: registries grow, conventions shift, new model families and formats appear, and downstream reuse practices evolve with them. Engineering guidance therefore cannot rest on a static picture of how models are produced or reused. We build datasets and conduct ecosystem-scale studies so that emerging practices, failure modes, and developer needs can be measured as they change.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2303.08934">PTMTorrent: A Dataset for Mining Open-source Pre-trained Model Packages</a></span><br><span class="venue">Annual Conference on Mining Software Repositorie &middot; 2023</span><br><span class="note">PTMTorrent made the model ecosystem minable, so claims about it could be measured instead of asserted.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2402.00699">PeaTMOSS: A Dataset and Initial Analysis of Pre-Trained Models in Open-Source Software</a></span><br><span class="venue">MSR &middot; 2024</span><br><span class="note">PeaTMOSS extends that to models as they appear inside open-source projects, linking the registry to the systems that depend on it.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2406.08205">What do we know about Hugging Face? A systematic literature review and quantitative validation of qualitative claims</a></span><br><span class="venue">ESEM &middot; 2024</span><br><span class="note">A systematic review and quantitative study of what is known about Hugging Face, consolidating a fast-moving literature.</span></li>
  <li><span class="pub-title">An Empirical Investigation of Pre-Trained Deep Learning Model Reuse in the Scientific Process</span><br><span class="note">An early empirical look at pre-trained model reuse in the wild.</span></li>
</ul>

## Model identity and interoperability cannot be assumed

Conventional dependency management assumes a named artifact can be identified, and that declared interfaces delimit how it composes with the rest of a system. Pre-trained models weaken both assumptions. Nominally equivalent models can differ, names can be inconsistent, and supposedly portable representations can fail when moved across tools and frameworks.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1181&context=ecepubs">Discrepancies among Pre-trained Deep Neural Networks: A New Threat to Model Zoo Reliability</a></span><br><span class="venue">ESEC/FSE-IVR &middot; 2022</span><br><span class="note">Found that nominally identical pre-trained models from model zoos differ, which makes a model zoo a supply chain rather than a catalogue.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2303.17708">Interoperability in Deep Learning: A User Survey and Failure Analysis of ONNX Model Converters</a></span><br><span class="venue">ISSTA &middot; 2024</span><br><span class="note">Tested whether ONNX interoperability holds. Conversion failures show that a portability claim is an engineering obligation, not a property.</span></li>
  <li><span class="pub-title">A method for identifying naming mismatches in neural networks based on their architectural properties</span><br><span class="venue">US provisional patent application, held by Purdu &middot; 2025</span><br><span class="note">Identifies naming mismatches from a network's architecture, making the naming problem detectable rather than only observable.</span></li>
</ul>

## Reuse shifts substantial engineering work downstream

Reusing a trained model does not eliminate engineering work; it relocates it. Downstream developers often have to reproduce results, adapt artifacts across frameworks and hardware, reconstruct missing assumptions, and determine whether the model remains valid for a new use.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://link.springer.com/article/10.1007/s10664-024-10521-0">Challenges and Practices of Deep Learning Model Reengineering: A Case Study on Computer Vision</a></span><br><span class="venue">EMSE &middot; 2024</span><br><span class="note">Model reengineering — reimplementing and extending published models — is a distinct and costly engineering activity; this documents what it involves.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2107.00821">An Experience Report on Machine Learning Reproducibility: Guidance for Practitioners and TensorFlow Model Garden Contributors</a></span><br><span class="venue">arXiv &middot; 2021</span><br><span class="note">Turned the reproducibility problem into guidance practitioners could apply.</span></li>
  <li><span class="pub-title">Improving the Reproducibility of Deep Learning Software: An Initial Investigation through a Case Study Analysis. https://arxiv.org/pdf/2505.03165. 2025</span><br><span class="venue">2025</span><br><span class="note">An early look at why deep-learning results are hard to reproduce, before reuse became the dominant mode.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2404.18801">A Partial Replication of MaskFormer in TensorFlow on TPUs for the TensorFlow Model Garden</a></span><br><span class="venue">arXiv &middot; 2024</span><br><span class="note">A partial replication across frameworks, which is where interoperability claims are tested rather than stated.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2412.18972">Recommending Pre-Trained Models for IoT Devices</a></span><br><span class="venue">SERP4IoT &middot; 2025</span><br><span class="note">Recommending models for constrained devices, where the reuse decision is bounded by the hardware it has to run on.</span></li>
</ul>

## Security is part of the reuse contract

A reused model is not only a learned function. It arrives as a software artifact with provenance, serialization formats, dependencies, and assumptions about how it will be loaded and executed. Those properties make security part of the reuse contract.

<ul class="pub-list">
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/JiangSynovicSethiIndarapuHyattSchorlemmerThiruvathukalDavis-PTMSupplyChain-SCORED22.pdf">An Empirical Study of Artifacts and Security Practices in the Pre-trained Model Supply Chain</a></span><br><span class="venue">SCORED &middot; 2022</span><br><span class="note">Characterized what is actually published alongside pre-trained models and what security practices accompany them.</span></li>
  <li><span class="pub-title"><a href="https://davisjam.github.io/files/publications/GopalakrishnaAnandayuvarajDettiBlandRahamanDavis-SWEngSecurityMLOnIoT.pdf">“If security is required”: Engineering and Security Practices for Machine Learning-based IoT Devices</a></span><br><span class="venue">SERP4IoT &middot; 2022</span><br><span class="note">Asks what security practices ML-based IoT engineering uses in practice, and finds them conditional on someone requiring them.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2508.15987">PickleBall: Secure Deserialization of Pickle-based Machine Learning Models</a></span> <span class="award">best artifact</span><br><span class="venue">CCS &middot; 2025</span><br><span class="note">Model serialization is an integration property. A format that executes code when loaded makes deserialization part of the reuse contract.</span></li>
  <li><span class="pub-title"><a href="https://arxiv.org/pdf/2503.19444">AI Safety in the Eyes of the Downstream Developer: A First Look at Concerns, Practices, and Challenges</a></span><br><span class="venue">arXiv &middot; 2025</span><br><span class="note">Looks at AI safety from the downstream developer's position — the engineer integrating a model, not the organization training it.</span></li>
</ul>

## Funding and support

This work has been supported by:

- **US National Science Foundation** — [CAREER: PTM-SEER: Software Engineering Foundations for Re-Using Pre-Trained Neural Models](https://www.nsf.gov/awardsearch/show-award/?AWD_ID=2541917) (#2541917)
- **US National Science Foundation** — [Collaborative Research: SaTC 2.0: RES: AIGIS: Securing the Deep Learning Model Supply Chain](https://www.nsf.gov/awardsearch/show-award/?AWD_ID=2526621) (#2526621)
- **Cisco** — Trustworthy Re-use of Pre-Trained Neural Networks
- **Google, LLC** — Unrestricted Gift: Machine Learning Reproducibility
- **Google, LLC** — Unrestricted Gift: Research on Machine Learning Reproducibility
