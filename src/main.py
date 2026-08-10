"""Point d'entrée principal de l'application de traduction."""

from src.config.config import Config
from src.database.database import Database
from src.scanner.scanner import Scanner
from src.ui.console import ConsoleUI
from src.translator.google_translator import GoogleTranslatorService
from src.translation_manager import TranslationManager
from src.writer.json_writer import JsonWriter
from src.ui.start_menu import StartMenu

def main() -> None:
    """Initialise les composants et lance le processus de traduction."""

    start_menu = StartMenu()
    
    scan_directory, selected_file, automatic = start_menu.ask()

    manager = TranslationManager(
        scanner=Scanner(),
        database=Database(Config.DATABASE_PATH),
        translator=GoogleTranslatorService(),
        console=ConsoleUI(),
        writer=JsonWriter()
    )

    project = None

    try:
        if scan_directory:
            project = manager.run(
                Config.OSTRANAUTS_DATA_PATH,
                automatic
            )
        else:
            project = manager.run_file(
                selected_file,
                automatic
            )

    except KeyboardInterrupt:
        print(f"{Config.RED} Arrêt demandé. {Config.RESET}")

    if project is None:
        return

    print(f"{Config.GREEN}{Config.FILE_SCANNED} : {project.scanned_files}")
    print(f"{Config.GREEN}{Config.FROM_MEMORY} : {project.cached_count}")
    print(f"{Config.GREEN}{Config.NEW_TRANSLATIONS} : {project.translated_count}")
    print(f"{Config.GREEN}{Config.TEXT_UNITS} : {sum(len(v) for v in project.files.values())} {Config.RESET}")


if __name__ == "__main__":
    main()