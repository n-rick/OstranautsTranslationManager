from scanner.scanner import Scanner
from config.config import Config
from database.database import Database


def main() -> None:
    scanner = Scanner()

    units = scanner.scan(Config.OSTRANAUTS_DATA_PATH)

    print(f"Files scanned : {scanner.scanned_files}")
    print(f"Text units    : {len(units)}")

    database = Database(Config.DATABASE_PATH)
    print(f"Database path : {Config.DATABASE_PATH}")
    database.load()

    for unit in units:
        if not database.contains(unit.uid):
            unit.translated_text = unit.source_text  # Temporaire
            database.add(unit)

    database.save()

    print(f"Database entries : {len(database.memory['translations'])}")


if __name__ == "__main__":
    main()