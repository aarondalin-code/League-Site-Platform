import json
from pathlib import Path

DERIVED_PATH = Path("data/derived/league-data.json")
OUTPUT_DIR = Path("site/output")


def safe(value, fallback=""):
    return (value or "").strip() if value is not None else fallback


def render_html(page_title, site_config, body_html):
    primary_color = safe(site_config.get("PrimaryColor"), "#0052cc")
    secondary_color = safe(site_config.get("SecondaryColor"), "#ffa500")
    logo_url = safe(site_config.get("LogoURL"))
    site_title = safe(site_config.get("SiteTitle"), site_config.get("LeagueName", "League Site"))

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{page_title}</title>
  <style>
    :root {{ --primary: {primary_color}; --secondary: {secondary_color}; }}
    body {{ margin: 0; font-family: Arial, Helvetica, sans-serif; background: #f8f9fb; color: #222; }}
    .topbar {{ background: var(--primary); color: white; padding: 10px 16px; display: flex; align-items: center; gap: 12px; }}
    .topbar img {{ max-height: 40px; border-radius: 6px; }}
    .nav {{ background: #ffffff; border-bottom: 1px solid #dbe0e9; padding: 8px 16px; }}
    .nav a {{ color: var(--primary); margin-right: 14px; text-decoration: none; font-weight: bold; }}
    .nav a.current {{ color: var(--secondary); }}
    .content {{ padding: 16px; max-width: 960px; margin: auto; }}
    .card {{ background: white; border: 1px solid #dde4ef; border-radius: 8px; margin-bottom: 14px; padding: 12px; box-shadow: 0 1px 2px rgba(30, 40, 70, 0.08); }}
    footer {{ text-align: center; font-size: 13px; padding: 10px 0; color: #65738a; }}
  </style>
</head>
<body>
  <header class="topbar">
    {f'<img src="{logo_url}" alt="Logo" />' if logo_url else ''}
    <div>
      <div style="font-size: 1.25rem; font-weight: 700;">{site_title}</div>
      <div style="font-size: .9rem;">{safe(site_config.get('LeagueName'))} - {safe(site_config.get('SeasonLabel'))}</div>
    </div>
  </header>
  <nav class="nav">
    <a href="index.html" class="{ 'current' if page_title.lower().startswith('home') else '' }">Home</a>
    <a href="teams.html" class="{ 'current' if page_title.lower().startswith('teams') else '' }">Teams</a>
    <a href="players.html" class="{ 'current' if page_title.lower().startswith('players') else '' }">Players</a>
    <a href="schedule.html" class="{ 'current' if page_title.lower().startswith('schedule') else '' }">Schedule</a>
  </nav>
  <main class="content">
    {body_html}
  </main>
  <footer>Built from data in data/csv; update CSV and rerun scripts.</footer>
</body>
</html>
"""


def build_site():
    if not DERIVED_PATH.exists():
        raise FileNotFoundError(f"Derived data file not found: {DERIVED_PATH}. Run scripts/import_league_csvs.py first.")

    data = json.loads(DERIVED_PATH.read_text(encoding="utf-8"))
    tables = data.get("tables", {})
    site_config_rows = tables.get("SiteConfig", [])
    content_rows = tables.get("Content", [])

    if not site_config_rows:
        raise ValueError("SiteConfig table is empty. Fill data/csv/SiteConfig.csv and rerun.")

    config = site_config_rows[0]

    # home
    active_content = [row for row in content_rows if str(row.get("Active", "")).strip().upper() in ("TRUE", "1", "YES")]
    recent_lines = []
    if active_content:
        for row in active_content[:6]:
            title = safe(row.get("Title"), safe(row.get("Type"), "Untitled"))
            snippet = safe(row.get("Body"), "No detail provided.")
            recent_lines.append(f"<div class='card'><h3>{title}</h3><p>{snippet}</p></div>")
    else:
        recent_lines.append("<div class='card'>No active content yet. Add entries in Content.csv.</div>")

    home_html = f"""
    <h1>Welcome to {safe(config.get('LeagueName'), 'the League')}</h1>
    <p>{safe(config.get('SeasonLabel'), '')}</p>
    <div>
      <h2>Featured content</h2>
      {''.join(recent_lines)}
    </div>
    """

    # teams
    teams = tables.get("Teams", [])
    teams_html = """
    <h1>Teams</h1>
    <div>
    """
    if teams:
        for team in teams:
            teams_html += f"<div class='card'><h3>{safe(team.get('TeamName', team.get('Name', 'Unnamed Team')))}</h3><p>{safe(team.get('Coach'))}</p></div>"
    else:
        teams_html += "<div class='card'>No team data found in Teams.csv.</div>"
    teams_html += "</div>"

    # players
    players = tables.get("Players", [])
    players_html = """
    <h1>Players</h1>
    <div>
    """
    if players:
        for player in players[:30]:
            players_html += f"<div class='card'><strong>{safe(player.get('PlayerName', 'Unnamed Player'))}</strong> {safe(player.get('Team'))}</div>"
    else:
        players_html += "<div class='card'>No player data found in Players.csv.</div>"
    players_html += "</div>"

    # schedule
    games = tables.get("Games", [])
    schedule_html = """
    <h1>Schedule</h1>
    <div>
    """
    if games:
        for game in games[:30]:
            schedule_html += f"<div class='card'><strong>{safe(game.get('Date'))}</strong> {safe(game.get('HomeTeam'))} vs {safe(game.get('AwayTeam'))}</div>"
    else:
        schedule_html += "<div class='card'>No schedule games found in Games.csv.</div>"
    schedule_html += "</div>"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "index.html").write_text(render_html("Home", config, home_html), encoding="utf-8")
    (OUTPUT_DIR / "teams.html").write_text(render_html("Teams", config, teams_html), encoding="utf-8")
    (OUTPUT_DIR / "players.html").write_text(render_html("Players", config, players_html), encoding="utf-8")
    (OUTPUT_DIR / "schedule.html").write_text(render_html("Schedule", config, schedule_html), encoding="utf-8")

    print(f"Built HTML site in {OUTPUT_DIR}. Open index.html in browser.")


if __name__ == "__main__":
    build_site()
