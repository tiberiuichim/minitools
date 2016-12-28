#!/bin/sh
type virtualenv >/dev/null 2>&1 || { echo >&2 "Needs virtualenv in PATH."; exit 1; }
virtualenv .
bin/pip install -r requirements.txt
