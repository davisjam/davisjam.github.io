#!/usr/bin/env bash

set -e
set -x

PUBFILE=publications.json
TMPFILE=publications-tmp.json

pushd markdown_generator/
  grep -v '#' $PUBFILE > $TMPFILE # Remove comment lines
  python3 publications.py $TMPFILE
  rm $TMPFILE
popd
