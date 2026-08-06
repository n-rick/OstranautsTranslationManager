from config.config import Config
from database.database import Database
from scanner.scanner import Scanner
from translator.google_translator import GoogleTranslatorService
from translation_manager import TranslationManager


def main() -> None:

    manager = TranslationManager(
        scanner=Scanner(),
        database=Database(Config.DATABASE_PATH),
        translator=GoogleTranslatorService(),
    )

    units = manager.run(Config.OSTRANAUTS_DATA_PATH)

    print(f"Files scanned     : {manager.scanner.scanned_files}")
    print(f"Text units        : {len(units)}")
    print(f"From memory       : {manager.cached_count}")
    print(f"New translations  : {manager.translated_count}")


if __name__ == "__main__":
    main()