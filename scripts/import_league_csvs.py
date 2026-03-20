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


def main():
    print("League CSV import script")
    print()
    print("Expected CSV files in data/csv/:")
    for file_name in EXPECTED_FILES:
        print(f"- {file_name}")


if __name__ == "__main__":
    main()
