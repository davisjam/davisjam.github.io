---
layout: single
title: "Research"
permalink: /research/
author_profile: true
redirect_from: 
  - /lab/
  - /lab.html
---

{% include base_path %}

## Joining the lab

**I welcome *graduate* and *undergraduate* researchers passionate about improving the quality of computing systems.**
Please review the lab description and the active projects to understand whether you are interested in joining our work.
If so, follow [these instructions](/join-lab) to check your qualifications and submit your application.
{: .notice--info}

## Introduction

This page describes the lab's general directions (first section), as well as some details about the lab (second section)
For a full list of publications, see [here](/publications).

Our lab conducts software engineering research with an eye to practical impact.
We understand two modes of impact:
- *Empirical*: Our tools have found plenty of defects and security vulnerabilities. Our research results have been adopted by major companies (Microsoft, IBM, Google) and major software systems (Node.js, Python, Ruby).
- *Theoretical*: Software engineering is always changing. Part of software engineering theory is to articulate and organize concepts so that practicing engineers can make sense of them (ontology). We write papers about this, and convey key ideas to practitioners through a Medium blog (65,000 views and counting).

## Research directions

### Web security, or, Software engineering for domain-specific languages

This research topic is about domain-specific languages, with applications to web security.
Domain-specific languages (DSLs) simplify the engineering of complex computing systems.
DSLs allow engineers to express domain-specific information fluently, rather than staggering through an articulation in a general-purpose language.

Regular expressions (regexes) are a widely used, hard to master DSL for string-matching problems.
They often cause software defects.
Regexes gone awry have caused [Internet-scale outages](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/) and are a [potent denial of service vector](https://www.usenix.org/conference/usenixsecurity18/presentation/staicu).

In our regex investigations, we have measured the difficulties that practitioners experience, and guided programming language designers toward regex engines that reflect the needs of practitioners.

*Here are some of the questions we have explored*:

1. How widespread of a problem is Regex Denial of Service? ([ESEC/FSE'18](/files/publications/DavisCoghlanServantLee-EcosystemREDOS-ESECFSE18.pdf), [ICSE'22](/files/publications/BarlasDuDavis-WebREDOS-ICSE22.pdf)).
3. How hard are regexes to work with? ([ESEC/FSE'19](/files/publications/DavisMichaelCoghlanServantLee-LinguaFranca-ESECFSE19.pdf), [ASE'19](/files/publications/MichaelDonohueDavisLeeServant-RegexesAreHard-ASE19.pdf))
4. How generalizable is regex research? ([ASE'19](/files/publications/DavisMoyerKazerouniLee-RegexGeneralizability-ASE19.pdf))
5. How might we address Regex Denial of Service? ([IEEE S&P'21](/files/publications/DavisServantLee-SelectiveMemo-IEEE-SP21.pdf), [IEEE S&P'23](/files/publications/HassanAamirLeeDavisServant-ReDoSUsability-SP23.pdf))

This work is supported by NSF [SaTC-2135156](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2135156).

### Software engineering for data-centric computing (SE4ML, pre-trained models)

Complex computing systems incorporate machine learning models -- data-centric computing components that predict the future based on the past (e.g. data science, ML, deep learning).
Correct machine learning models requires the development of the models themselves, and the use of analysis pipelines to automatically and repeatedly process batches of data.
Engineering these models is a critical aspect of modern computing.

Some problems in this domain are traditional, e.g. documenting one's code, promoting modularity, and porting concepts from one programming language (or ML framework) to another.
Other problems are new, e.g. understanding the nature of software re-use in this context (pre-trained models).

*Here are some of the questions we have explored*:

1. How might provenance be applied to assist data scientists? ([SIGMOD'19 demo](/files/publications/RupprechtDavisetal-SIGMOD-Demo-19.pdf), [VLDB'20](/files/publications/RupprechtDavisArnoldGurBhagwat-Ursprung-VLDB20.pdf))
2. What should high-quality machine learning software look like? (CSE'20 poster, [arXiv'21](https://arxiv.org/abs/2107.00821))
3. What are the challenges and practices for the reuse of machine learning models? ([ESEC/FSE-IVR'22](/files/publications/MontesPeerapatanapokinSchultzGuoJiangDavis-ModelZoo-FSE22IVR.pdf), [ICSE'23](/files/publications/JiangSynovicHyattSchorlemmerSethiLuThiruvathukalDavis-ICSE23-PTMReuseInHuggingFace.pdf), [MSR-Dataset'23](https://arxiv.org/abs/2303.08934))

This research is supported financially by Google, Cisco, and NSF [OAC-2107230](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2107230).

### Software engineering in cyber-physical systems (IoT)

Software influences the physical world one way or another.
Unlike traditional business software, in which physical-world effects are mediated by humans, Internet of Things (IoT) systems allow software to directly interact with the physical world through interconnected devices.

Embedded systems are some of the oldest computing systems (e.g. avionics), and there are well established engineering methods to reduce catastrophic failure.
However, these methods are not being applied in many safety-sensitive contexts such as medical devices.

*Here are some of the questions we have explored*:

1. How do software engineers think about machine learning and cybersecurity for IoT products? ([SERP4IoT'22](/files/publications/GopalakrishnaAnandayuvarajDettiBlandRahamanDavis-SWEngSecurityMLOnIoT.pdf))
2. What are the characteristics of failures in IoT systems? ([ASE-NIER'22](/files/publications/AnandayuvarajDavis-RecurringFailuresInIoT-ASE22NIER.pdf)) 
3. Are software engineering researchers consistent and coherent in their analysis of failures? ([ESEC/FSE-IVR'22](/files/publications/AmusuoSharmaRaoVincentDavis-SoftwareFailureAnalysis-FSE22IVR.pdf))
4. How do engineering students respond to lessons about failures? ([SERP4IoT'23](/files/publications/AnandayuvarajDavis-RecurringFailuresInIoT-ASE22NIER.pdf))
5. Can we apply traditional program analyses to embedded software applications? ([DSN-Disrupt'23](/files/publications/SrinivasanTanksalkarAmusuoDavisMachiry-Rehosting-DSN23.pdf), [LCTES-WIP'23](/files/publications/ShenDavisMachiry-NCMAs-LCTES23.pdf)).
6. How do we achieve good performance in resource-constrained environments? ([HotMobile'22](/files/publications/VeselskyWestAhlgrenGoelJiangLeeKimDavisThiruvathukalKlingensmith-V2VTrust-HotMobile.pdf), [ISLPED'21](/files/publications/GoelTungHuWangDavisThiruvathukalLu-HNN-ISLPED21.pdf), [ASP-DAC'22](/files/publications/GoelTungHuThiruvathukalDavisLu-ASPDAC2022.pdf), [ISLPED'22](/files/publications/GoelTungEliopoulosHuThiruvathukalDavisLu-DAGHNNs-ISLPED2022.pdf), [Computer'23](/files/publications/HuJiaoKocherWuLiuDavisThiruvathukalLu-LPCVC-Computer2023)).

This research is supported financially by Cisco and Rolls Royce.

### Software supply chains

*Here are some of the questions we have explored*:

1. What are general principles of secure software supply chains? ([SCORED'22](/files/publications/OkaforSchorlemmerTorresAriasDavis-SOKSecureSupplyChainProperties-SCORED22.pdf))
2. What are the characteristics of software supply chains in machine learning? ([SCORED'22](/files/publications/JiangSynovicSethiIndarapuHyattSchorlemmerThiruvathukal-PTMSupplyChain-SCORED22.pdf))

Some papers from other areas (notably my work on pre-trained models) also fall into this category.

This research is supported financially by Cisco and NSF [POSE-22297403](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2229703&HistoricalAwards=false).

## About the Duality Lab

### Overview

*The vision of the Duality Lab is to improve the quality of complex computing systems.*

We believe that computing systems will eventually mediate many human interactions with other humans and with the surrounding world.
We therefore seek to improve the human experience by improving the quality of computing systems.
Two factors are foundational to our success:

1. Our **diverse team** helps us understand the ways that computing systems are used and perceived by many kinds of humans. Computing systems will touch all of humanity, and so all of humanity is needed to develop them.
2. Our **data-driven and systems** approach grounds our work in real-world computing systems, ensuring that our findings and proposals impact the quality of computing systems in the here-and-now, not in the what-might-be.

In order to improve the quality of software-intensive computing systems, we take a scientific engineering approach.
   - We empirically study engineering failures to drive the development of tools and systems that reflect practitioners' needs and address their misconceptions.
   - We blend techniques from software engineering, systems, and security in order to understand, measure, and ameliorate the issues that computing practitioners face.
   - We apply methodologies appropriate to the task at hand: static and dynamic program analysis, pattern recognition and machine learning, algorithm development, and plenty of system building and hacking.

### What's in a name?

The Duality Lab is an abbreviation of the **D**avis Q**uality** Lab.

**"Quality"**

What do we mean by "quality"? Some of our projects focus on functional properties like **correctness** and **security**, while others consider **engineering process** and **human perspectives**.

Since we must understand engineering practice before we can improve it, our research often has an **empirical** bent &mdash; examining engineering artifacts (e.g. mining software repositories) and engineers themselves (e.g. surveys and interviews).

**"Duality"**

Quality is often approached dualistically &mdash; technical or social, but not both.
We aim to unite these perspectives.

- We believe that designing a high-quality system requires technical sophistication.
- We also believe that designing a high-quality system requires considering how humans will use it.

Call this what you will: human-in-the-loop, a socio-technical perspective, etc.
We believe it is the only way to achieve truly high-quality computing systems.
