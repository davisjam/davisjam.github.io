#!/usr/bin/env python3
# Publications markdown generator for academicpages
# Data format: JSON, see publications.json for examples
# Caution: Overwrites ../auto-publications.md

import json

JOURNAL_PUB = "journal"
CONFERENCE_PUB = "conference"
SHORT_PUB = "short"

def writeOutPrefix(handle):
    handle.write("""---
layout: single
title: "Publications"
permalink: /publications/
author_profile: true
---
""")

FILE_PATH = "{{ site.url }}/{{ site.baseurl }}/{{ site.filesurl }}/publications"

def pub2md(pub):
    links = []
    if pub['wonAward']:
        links.append('<i class="fas fa-trophy fa-lg">Award</i>')
    if pub['paperBasename']:
        links.append('<a href="{}/{}"><i class="fa fa-file-text-o fa-lg"></i>Paper</a>'.format(
            FILE_PATH, pub['paperBasename']
        ))
    if pub['slidesBasename']:
        links.append('<a href="{}/{}"><i class="fa fa-file-powerpoint-o fa-lg"></i>Slides</a>'.format(
            FILE_PATH, pub['slidesBasename']
        ))
    if pub['artifactURL']:
        links.append('<a href="{}"><i class="fa fa-certificate fa-lg"></i>Artifact</a>'.format(
            pub['artifactURL']
        ))
    if pub['videoURL']:
        links.append('<a href="{}"><i class="fa fa-video-camera fa-lg"></i>Video</a>'.format(
            pub['videoURL']
        ))

    cite = "{}. *{}*. ({} {}).".format(
        ', '.join(pub['authors']),
        pub['title'],
        pub['venue'],
        pub['year']
    )
    return '\n '.join(links) + " " + cite

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

with open('publications.json', 'r') as infile, open('../auto-publications.md', 'w') as outfile:
    writeOutPrefix(outfile)
    pubs = json.load(infile)['publications']
    pubs = sorted(pubs, key=lambda p: p['year'], reverse=True)

    confPubs = [ pub for pub in pubs if pub['type'] == CONFERENCE_PUB ]
    journalPubs = [ pub for pub in pubs if pub['type'] == JOURNAL_PUB ]
    shortPubs = [ pub for pub in pubs if pub['type'] == SHORT_PUB ]

    if confPubs:
        print("Writing the {} conference pubs".format(len(confPubs)))
        writeConfPubs(outfile, confPubs)
    if journalPubs:
        print("Writing the {} journal pubs".format(len(journalPubs)))
        writeJournalPubs(outfile, journalPubs)
    if shortPubs:
        print("Writing the {} short pubs".format(len(shortPubs)))
        writeShortPubs(outfile, shortPubs)
    outfile.write('\n')