#!/bin/bash
set -e
python scripts/import_league_csvs.py
python scripts/build_site.py
cd site/output
python -m http.server 8000
