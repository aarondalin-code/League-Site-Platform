import json
from pathlib import Path

DERIVED_PATH = Path("data/derived/league-data.json")
OUTPUT_PAGE = Path("site/pages/home.md")


def build_homepage():
    if not DERIVED_PATH.exists():
        raise FileNotFoundError(
            f"Derived league data not found at {DERIVED_PATH}. Run scripts/import_league_csvs.py first."
        )

    league_data = json.loads(DERIVED_PATH.read_text(encoding="utf-8"))
    site_config_rows = league_data.get("tables", {}).get("SiteConfig", [])
    content_rows = league_data.get("tables", {}).get("Content", [])

    if not site_config_rows:
        raise ValueError("SiteConfig data is empty. Add data to data/csv/SiteConfig.csv and rebuild.")

    config = site_config_rows[0]

    league_name = config.get("LeagueName", "League")
    season_label = config.get("SeasonLabel", "Season")
    site_title = config.get("SiteTitle", f"{league_name} Website")

    active_content = [
        row for row in content_rows if str(row.get("Active", "")).strip().upper() in ("TRUE", "1", "YES")
    ]

    intro_text = config.get("WelcomeText", "Welcome to the league!")

    lines = [
        f"# {site_title}",
        "",
        f"## {league_name} - {season_label}",
        "",
        f"{intro_text}",
        "",
        "### Quick Links",
        "",
        "- [Teams](teams.md)",
        "- [Players](players.md)",
        "- [Schedule](schedule.md)",
        "",
        "### Featured Content",
        "",
    ]

    if not active_content:
        lines.append("No featured content available yet. Add rows to Content.csv and rebuild.")
    else:
        rows_to_show = active_content[:5]
        for row in rows_to_show:
            title = row.get("Title") or row.get("Type") or "Untitled"
            body = row.get("Body", "")
            lines.append(f"- **{title}**: {body}")

    OUTPUT_PAGE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PAGE.write_text("\n".join(lines), encoding="utf-8")

    print(f"Built {OUTPUT_PAGE} with {len(rows_to_show) if active_content else 0} featured items.")


if __name__ == "__main__":
    build_homepage()
