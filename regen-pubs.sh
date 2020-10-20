#!/usr/bin/env bash

set -e
set -x

pushd markdown_generator/
  python3 publications.py
popd
