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
OUTPUT_FILE = Path("data/derived/csv-file-summary.json")


def count_data_rows(file_path):
    with file_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        next(reader, None)
        return sum(1 for row in reader if any(cell.strip() for cell in row))


def main():
    print("Checking league CSV files in data/csv/")
    print()

    found_files = []
    missing_files = []
    row_counts = {}

    for file_name in EXPECTED_FILES:
        file_path = DATA_DIR / file_name
        if file_path.exists():
            print(f"FOUND: {file_name}")
            found_files.append(file_name)
            row_counts[file_name] = count_data_rows(file_path)
        else:
            print(f"MISSING: {file_name}")
            missing_files.append(file_name)

    print()

    summary = {
        "dataDirectory": str(DATA_DIR),
        "foundFiles": found_files,
        "missingFiles": missing_files,
        "rowCounts": row_counts,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"Wrote summary to {OUTPUT_FILE}")

    if missing_files:
        print("Some required CSV files are missing.")
    else:
        print("All required CSV files are present.")


if __name__ == "__main__":
    main()
