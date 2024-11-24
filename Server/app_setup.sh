#!/usr/bin/bash
set -e

# Ensure working in project directory
cd $(dirname ${0})

test -d .venv || { 
  python3 -m venv --system-site-packages .venv \
  && source .venv/bin/activate \
  && pip3 install -r requirements.txt
}

