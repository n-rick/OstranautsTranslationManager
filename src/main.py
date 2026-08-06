from scanner.scanner import Scanner
from config.config import Config
from database.database import Database
from translator.google_translator import GoogleTranslatorService


def main() -> None:
    scanner = Scanner()

    units = scanner.scan(Config.OSTRANAUTS_DATA_PATH)

    print(f"Files scanned : {scanner.scanned_files}")
    print(f"Text units    : {len(units)}")

    database = Database(Config.DATABASE_PATH)
    database.load()

    translator = GoogleTranslatorService()

    for unit in units:
        translation = database.get_translation(unit.uid)

        if translation is not None:
            unit.translated_text = translation
        else:
            translator.translate(unit)
            database.update(unit)

    database.save()


if __name__ == "__main__":
    main()