#!/usr/bin/env python3
from PyPDF2 import PdfReader, PdfWriter
import sys
source = sys.argv[1]
target = f"{source}-scrubbed.pdf"


# before replacement
# meta.creator:
#       LaTeX with acmart 2022/04/09 v1.84 Typesetting articles for the Association for Computing Machinery and hyperref 2022-02-21 v7.00n Hypertext links for LaTeX
# meta.producer:
#       pdfTeX, Version 3.141592653-2.6-1.40.24 (TeX Live 2022/Arch Linux) kpathsea version 6.3.4


# after replacement (using a hex editor)
#   XXXXX with acmart 2022/04/09 v1.84 Typesetting articles for the Association for Computing Machinery and hyperref 2022-02-21 v7.00n Hypertext links for XXXXX
#   xxxxxx, Version sssssssssssssssssssssss (xxx xxxx 2022/Arch Linux) xxxxxxxx version 6.3.4

# more aggressively: just remove metadta.creator and metadata.producer (works?)

reader = PdfReader(source)
writer = PdfWriter()

meta = reader.metadata

# Add all pages to the writer
for page in reader.pages:
    writer.add_page(page)

writer.add_metadata(
    {
        "/Creator": "",
        "/Producer": "",
    }
)

# All of the following could be None and nobody is hurt!
#print(meta.author)
print("Original metadata")
print(f"creator: {meta.creator}")
print(f"Producer: {meta.producer}")
#print(meta.subject)
#print(meta.title)

print(f"saving as: {target}")
with open(target, "wb") as fp:
    writer.write(fp)

print("changed md to:")


reader = PdfReader(target)
meta = reader.metadata

writer.add_metadata(
    {
        "/Creator": "",
        "/Producer": "",
    }
)

print("New metadata")
print(meta.creator)
print(meta.producer)
