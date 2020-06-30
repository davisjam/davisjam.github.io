#!/usr/bin/env python3
# Publications markdown generator for academicpages
# Data format: JSON, see publications.json for examples
# Caution: Overwrites ../auto-publications.md

import json

JOURNAL_PUB = "journal"
CONFERENCE_PUB = "conference"
SHORT_PUB = "short"
PATENT_PUB = "patent"

def writeOutPrefix(handle):
    handle.write("""---
layout: single
title: "Publications"
permalink: /publications/
author_profile: true
---

Here are the peer-reviewed publications to which I have contributed.
To see them organized by project, see [here](/research).
""")

FILE_PATH = "{{ site.url }}/{{ site.baseurl }}/{{ site.filesurl }}/publications"

def pub2md(pub):
    links = []
    if 'paperBasename' in pub and pub['paperBasename']:
        links.append('<a href="{}/{}"><i class="fas fa-file-pdf"></i></a>'.format(
            FILE_PATH, pub['paperBasename']
        ))
    if 'slidesBasename' in pub and pub['slidesBasename']:
        links.append('<a href="{}/{}"><i class="fas fa-file-powerpoint"></i></a>'.format(
            FILE_PATH, pub['slidesBasename']
        ))
    if 'artifactURL' in pub and pub['artifactURL']:
        links.append('<a href="{}"><i class="fas fa-truck"></i></a>'.format(
            pub['artifactURL']
        ))
    if 'videoURL' in pub and pub['videoURL']:
        links.append('<a href="{}"><i class="fas fa-video-camera"></i></a>'.format(
            pub['videoURL']
        ))
    if 'blogURL' in pub and pub['blogURL']:
        links.append('<a href="{}"><i class="fab fa-medium"></i></a>'.format(
            pub['blogURL']
        ))
    if 'bestPaperAward' in pub and pub['bestPaperAward']:
        links.append('[Best Paper Award](){: .btn}')
    
    authList = ', '.join(pub['authors'][:-1])
    if len(pub['authors']) > 1:
        authList += ", and " + pub['authors'][-1]

    cite = "*{}*.  \n {}.  \n {} {}.  ".format(
        pub['title'],
        authList,
        pub['venue'], pub['year'],
    )
    return cite + "\n " + ' '.join(links)

def writeConfPubs(handle, pubs):
    handle.write('\n## Conference papers\n\n')
    for i, pub in enumerate(pubs):
        handle.write("{}. {}\n".format(i+1, pub2md(pub)))

def writeJournalPubs(handle, pubs):
    handle.write('\n## Journal papers\n\n')
    for i, pub in enumerate(pubs):
        handle.write("{}. {}\n".format(i+1, pub2md(pub)))

def writeShortPubs(handle, pubs):
    handle.write('\n## Short papers\n\n')
    for i, pub in enumerate(pubs):
        handle.write("{}. {}\n".format(i+1, pub2md(pub)))

def writePatents(handle, pubs):
    if False:
        handle.write('\n## Patents\n\n')
        for i, pub in enumerate(pubs):
            handle.write("{}. {}\n".format(i+1, pub2md(pub)))

with open('publications.json', 'r') as infile, open('../auto-publications.md', 'w') as outfile:
    writeOutPrefix(outfile)
    pubs = json.load(infile)['publications']
    pubs = sorted(pubs, key=lambda p: p['year'], reverse=True)

    confPubs = [ pub for pub in pubs if pub['type'] == CONFERENCE_PUB ]
    journalPubs = [ pub for pub in pubs if pub['type'] == JOURNAL_PUB ]
    shortPubs = [ pub for pub in pubs if pub['type'] == SHORT_PUB ]
    patentPubs = [ pub for pub in pubs if pub['type'] == PATENT_PUB ]

    if confPubs:
        print("Writing the {} conference pubs".format(len(confPubs)))
        writeConfPubs(outfile, confPubs)
    if journalPubs:
        print("Writing the {} journal pubs".format(len(journalPubs)))
        writeJournalPubs(outfile, journalPubs)
    if shortPubs:
        print("Writing the {} short pubs".format(len(shortPubs)))
        writeShortPubs(outfile, shortPubs)
    if patentPubs:
        print("Writing the {} patents".format(len(patentPubs)))
        writePatentPubs(outfile, patentPubs)
    outfile.write('\n')