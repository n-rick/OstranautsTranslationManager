"""Point d'entrée principal de l'application de traduction."""

from config.config import Config
from database.database import Database
from scanner.scanner import Scanner
from ui.console import ConsoleUI
from translator.google_translator import GoogleTranslatorService
from translation_manager import TranslationManager
from writer.json_writer import JsonWriter
from ui.start_menu import StartMenu

def main() -> None:
    """Initialise les composants et lance le processus de traduction."""

    start_menu = StartMenu()
    
    scan_directory, selected_file = start_menu.ask()

    manager = TranslationManager(
        scanner=Scanner(),
        database=Database(Config.DATABASE_PATH),
        translator=GoogleTranslatorService(),
        console=ConsoleUI(),
        writer=JsonWriter()
    )

    try:
        if scan_directory:
            project = manager.run(Config.OSTRANAUTS_DATA_PATH)
        else:
            project = manager.run_file(selected_file)

    except KeyboardInterrupt:
        print("\n\nArrêt demandé.")

    print(f"{Config.FILE_SCANNED} : {project.scanned_files}")
    print(f"{Config.FROM_MEMORY} : {project.cached_count}")
    print(f"{Config.NEW_TRANSLATIONS} : {project.translated_count}")
    print(f"{Config.TEXT_UNITS} : {sum(len(v) for v in project.files.values())}")


if __name__ == "__main__":
    main()