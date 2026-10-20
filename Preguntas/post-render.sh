#!/bin/sh
set -eu

rm -rf ../docs/*
cp -a _site/. ../docs/

rm -rf _site/