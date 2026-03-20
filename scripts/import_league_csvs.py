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


def main():
    print("Checking league CSV files in data/csv/")
    print()

    missing_files = []

    for file_name in EXPECTED_FILES:
        file_path = DATA_DIR / file_name
        if file_path.exists():
            print(f"FOUND: {file_name}")
        else:
            print(f"MISSING: {file_name}")
            missing_files.append(file_name)

    print()

    if missing_files:
        print("Some required CSV files are missing.")
    else:
        print("All required CSV files are present.")


if __name__ == "__main__":
    main()
