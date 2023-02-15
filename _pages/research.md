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

## Actively recruiting

**I welcome *graduate* and *undergraduate* researchers passionate about improving the quality of computing systems.**
Please review the lab description and the active projects to understand whether you are interested in joining our work.
If so, follow [these instructions](/join-lab) to check your qualifications and submit your application.
{: .notice--info}

This page describes some of my lab's broad directions.
For a full list of publications, see [here](/publications).

- Software engineering for domain-specific languages (regexes)
- "[Software 2.0](https://medium.com/@karpathy/software-2-0-a64152b37c35)" &mdash; Software engineering and its intersection with AI + Machine Learning
- Software engineering in cyber-physical systems
- Software supply chains

## Research projects

### Software engineering for domain-specific languages

Domain-specific languages (DSLs) are a technique used to simplify the engineering of complex computing systems.
DSLs allow engineers to express domain-specific information fluently, rather than staggering through an articulation in a general-purpose language.

Regular expressions (regexes) are a widely used, hard to master DSL for string-matching problems.
They often cause software defects.
Regexes gone awry have caused [Internet-scale outages](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/) and are a [potent denial of service vector](https://www.usenix.org/conference/usenixsecurity18/presentation/staicu).

In our regex investigations, we have measured the difficulties that practitioners experience, and guided programming language designers toward regex engines that reflect the needs of practitioners.

1. How widespread of a problem is Regex Denial of Service? ([ESEC/FSE'18](/files/publications/DavisCoghlanServantLee-EcosystemREDOS-ESECFSE18.pdf)).
2. How portable are regexes? ([ESEC/FSE'19](/files/publications/DavisMichaelCoghlanServantLee-LinguaFranca-ESECFSE19.pdf))
3. How hard are regexes to work with? ([ASE'19](/files/publications/MichaelDonohueDavisLeeServant-RegexesAreHard-ASE19.pdf))
4. How generalizable is regex research? ([ASE'19](/files/publications/DavisMoyerKazerouniLee-RegexGeneralizability-ASE19.pdf))
5. How can we address Regex Denial of Service in a backwards-compatible way? ([IEEE S&P'21](/files/publications/DavisServantLee-SelectiveMemo-IEEE-SP21.pdf))
6. Does sharing valid input formats with clients expose web services to Regex Denial of Service? ([ICSE'22](/files/publications/BarlasDuDavis-WebREDOS-ICSE22.pdf))

This work is supported by NSF [SaTC-2135156](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2135156).

### Software engineering for data-centric computing

Complex computing systems increasingly rely on components derived from data-centric computing, variously referred to as "machine learning" and "data science".
These techniques have been adopted across most enterprise businesses.
These techniques include the development of machine learning models, and the use of analysis pipelines to automatically and repeatedly process batches of data.
Correctly engineering these models, and reproducing and extending analysis pipelines, are critical aspects of modern computing.
The implications are broad, including business success and national defense.

*Here are some of the questions we have explored*:

1. How might provenance be applied to assist data scientists? ([VLDB'20](/files/publications/RupprechtDavisArnoldGurBhagwat-Ursprung-VLDB20.pdf), [SIGMOD'19 demo](/files/publications/RupprechtDavisetal-SIGMOD-Demo-19.pdf))
2. What should high-quality machine learning software look like? ([CSE'20 poster](), [arXiv'21 report](https://arxiv.org/abs/2107.00821))
3. What are the challenges and practices for the reuse of machine learning models? ([ESEC/FSE-IVR'22](/files/publications/MontesPeerapatanapokinSchultzGuoJiangDavis-ModelZoo-FSE22IVR.pdf), [ICSE'23](/files/publications/JiangSynovicHyattSchorlemmerSethiLuThiruvathukalDavis-ICSE23-PTMReuseInHuggingFace.pdf))

This research involves a collaboration with Drs. Yung-Hsiang Lu, George K. Thiruvathukal, and Neil Klingensmith, and is supported financially by:
- NSF [OAC-2107230](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2107230)
- Google
- Cisco

### Software engineering in cyber-physical systems

*Here are some of the questions we have explored*:

1. How do software engineers think about machine learning and cybersecurity for IoT products? ([SERP4IOT'22](/files/publications/GopalakrishnaAnandayuvarajDettiBlandRahamanDavis-SWEngSecurityMLOnIoT.pdf))
2. What are the characteristics of failures in IoT systems? ([ASE-NIER'22](/files/publications/AnandayuvarajDavis-RecurringFailuresInIoT-ASE22NIER.pdf)) 
3. Are software engineering researchers consistent and coherent in their analysis of failures? ([ESEC/FSE-IVR'22](/files/publications/AmusuoSharmaRaoVincentDavis-SoftwareFailureAnalysis-FSE22IVR.pdf))

This research is supported financially by:
- Cisco
- Rolls Royce

### Software supply chains

1. What are general principles of secure software supply chains? ([SCORED'22](/files/publications/OkaforSchorlemmerTorresAriasDavis-SOKSecureSupplyChainProperties-SCORED22.pdf))
2. What are the characteristics of software supply chains in machine learning? ([SCORED'22](/files/publications/JiangSynovicSethiIndarapuHyattSchorlemmerThiruvathukal-PTMSupplyChain-SCORED22.pdf))

This research is supported financially by:
- Cisco
- NSF [POSE-22297403](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2229703&HistoricalAwards=false)

## About the Duality Lab

Computing systems will transform the human experience during this century,
  for individuals (I sure like my robotic vacuum)
  and for society (Can computer vision safely support policing and national defense?).
Achieving this transformation requires high-quality software.
This is an increasingly-difficult challenge as computing systems become more complex.

### Vision

*The vision of the Duality Lab is to improve the quality of complex computing systems.*

We believe that computing systems will eventually mediate many human interactions with other humans and with the surrounding world.
We therefore seek to improve the human experience by improving the quality of computing systems.
Three factors are foundational to our success:

1. Our **diverse team** helps us understand the ways that computing systems are used and perceived by many kinds of humans. Computing systems will touch all of humanity, and so all of humanity is needed to develop them.
2. Our **data-driven** approach grounds our work in real-world computing systems, ensuring that our findings and proposals impact the quality of computing systems in the here-and-now, not in the what-might-be.
3. Our **readiness to re-imagine** enables us to propose, design, and implement new paradigms.

In order to improve the quality of software-intensive computing systems, we take a scientific engineering approach.
   - We empirically study engineering failures in order to drive the development of tools and systems that reflect practitioners' needs and address their misconceptions.
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

### Philosophy of training

Learning how to "do research" is a long journey. To help you understand what life will be like in my lab, let me tell you about my philosophy of training.

A research laboratory has two responsibilities.
  First, we create *new knowledge*.
  Second, we create *new researchers*.

Every lab member will contribute to the creation and sharing of new knowledge. This typically takes the form of understanding the state of the art (research literature) and of the practice (existing tools and systems), and then designing studies, implementing systems or studying humans, and writing up results.

Research is learned through apprenticeship.
  My lab members will become
    **disciplined thinkers**,
    **thoughtful researchers**,
    and
    **exemplary communicators**.
  I will provide you with
    one-on-one mentoring in these areas,
    feedback to help you understand your strengths and weaknesses,
    and
    resources to help you improve.
  In addition, senior lab members will be given opportunities to help train more junior lab members.

My complete *Advisor-Advisee Compact* is available on request.

### Impact

Our lab conducts research with an eye to practical impact.
Our research results have been adopted by major companies (Microsoft, IBM, Google) and major software systems (Node.js, Python, Ruby).
