

# League-Site-Platform

This repository contains the first data files for the league site platform.

## Current project state

The data files are in `data/csv/` and the platform can generate a preview website.

## CSV files

- SiteConfig.csv
- Teams.csv
- Players.csv
- Games.csv
- Practices.csv
- Drills.csv
- Trivia.csv
- Content.csv

## Quick preview (no manual HTML editing)

1. In terminal, run:
   - `./scripts/preview.sh`
2. Open browser at:
   - `http://localhost:8000`
3. Stop server with Ctrl+C

## Custom league branding

In `data/csv/SiteConfig.csv`, edit:
- `SiteTitle`, `LeagueName`, `SeasonLabel`
- `PrimaryColor`, `SecondaryColor`, `TextColor`
- `HeaderText`, `Tagline`, `BackgroundImageURL`

Then rerun `./scripts/preview.sh`.

## Current scaffold progress

- CSV files have been organized into `data/csv/`
- `START-HERE.md` has been added
- `scripts/import_league_csvs.py` now validates required data and fails loudly
- `scripts/build_homepage.py` generates `site/pages/home.md` from CSV-derived data
- `scripts/build_site.py` and `scripts/preview.sh` now build and serve HTML output
