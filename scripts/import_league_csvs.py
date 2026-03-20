import csv
import json
import sys
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

REQUIRED_HEADERS = {
    "SiteConfig.csv": [
        "LeagueID",
        "LeagueName",
        "SeasonLabel",
        "SiteTitle",
    ],
    "Content.csv": ["ContentID", "Type", "Active"],
}

DATA_DIR = Path("data/csv")
SUMMARY_FILE = Path("data/derived/csv-file-summary.json")
OUTPUT_FILE = Path("data/derived/league-data.json")


def read_csv_rows(file_path):
    with file_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"CSV file {file_path} has no headers")

        rows = []

        for row_no, row in enumerate(reader, start=2):
            clean_row = {
                key: value.strip() if isinstance(value, str) else value
                for key, value in row.items()
            }

            if any(value not in ("", None) for value in clean_row.values()):
                rows.append(clean_row)
            elif any(value is not None for value in row.values()):
                # Row contains empty values only; keep it out but keep schema checks below
                pass

        return reader.fieldnames, rows


def validate_header(file_name, fieldnames):
    required = REQUIRED_HEADERS.get(file_name)
    if not required:
        return []

    missing = [h for h in required if h not in fieldnames]
    if missing:
        return missing
    return []


def main():
    print("Building league data from data/csv/")
    print()

    found_files = []
    missing_files = []
    row_counts = {}
    headers = {}
    tables = {}
    errors = []

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

            header_errors = validate_header(file_name, fieldnames)
            if header_errors:
                errors.append(
                    f"{file_name} is missing required headers: {', '.join(header_errors)}"
                )

            if file_name == "SiteConfig.csv" and len(rows) < 1:
                errors.append("SiteConfig.csv must contain at least one config row")

            if file_name == "Content.csv" and len(rows) < 1:
                errors.append("Content.csv must contain at least one content row")

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
        errors.append("Some required CSV files are missing.")

    if errors:
        print("\nERRORS detected during CSV ingest:")
        for err in errors:
            print(f"- {err}")

        print("\nImport failed. Fix CSV data and rerun.")
        sys.exit(1)

    print("All required CSV files are present and valid.")


if __name__ == "__main__":
    main()
