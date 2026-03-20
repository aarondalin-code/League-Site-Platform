import csv
import json
from pathlib import Path

EXPECTED_FILES = [
    "SiteConfig.csv",
    "Teams.csv",
    "Players.csv",
    "Games.csv",
    "Practices.csv",
    "Drills.csv",
    "Trivia.csv",
    "Content.csv",
]

DATA_DIR = Path("data/csv")
SUMMARY_FILE = Path("data/derived/csv-file-summary.json")
OUTPUT_FILE = Path("data/derived/league-data.json")


def read_csv_rows(file_path):
    with file_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = []

        for row in reader:
            clean_row = {
                key: value.strip() if isinstance(value, str) else value
                for key, value in row.items()
            }

            if any(value not in ("", None) for value in clean_row.values()):
                rows.append(clean_row)

        return reader.fieldnames or [], rows


def main():
    print("Building league data from data/csv/")
    print()

    found_files = []
    missing_files = []
    row_counts = {}
    headers = {}
    tables = {}

    for file_name in EXPECTED_FILES:
        file_path = DATA_DIR / file_name
        table_name = file_name.replace(".csv", "")

        if file_path.exists():
            print(f"FOUND: {file_name}")
            found_files.append(file_name)

            fieldnames, rows = read_csv_rows(file_path)
            headers[file_name] = fieldnames
            row_counts[file_name] = len(rows)
            tables[table_name] = rows
        else:
            print(f"MISSING: {file_name}")
            missing_files.append(file_name)

    print()

    summary = {
        "dataDirectory": str(DATA_DIR),
        "foundFiles": found_files,
        "missingFiles": missing_files,
        "rowCounts": row_counts,
        "headers": headers,
    }

    league_data = {
        "meta": summary,
        "tables": tables,
    }

    SUMMARY_FILE.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_FILE.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    OUTPUT_FILE.write_text(json.dumps(league_data, indent=2), encoding="utf-8")

    print(f"Wrote summary to {SUMMARY_FILE}")
    print(f"Wrote combined data to {OUTPUT_FILE}")

    if missing_files:
        print("Some required CSV files are missing.")
    else:
        print("All required CSV files are present.")


if __name__ == "__main__":
    main()
