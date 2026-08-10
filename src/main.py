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
    try:
        scan_directory, selected_file, automatic, generate_workshop = start_menu.ask()
    except KeyboardInterrupt:
        print(f"\n\n {Config.RED} ⚠️ Arrêt demandé. {Config.RESET}")
        return

    manager = TranslationManager(
        scanner=Scanner(),
        database=Database(Config.DATABASE_PATH),
        translator=GoogleTranslatorService(),
        console=ConsoleUI(),
        writer=JsonWriter(),
    )

    project = None
    try:
        if scan_directory:
            project = manager.run(
                selected_file, automatic, generate_workshop
            )
        else:
            project = manager.run_file(
                selected_file, automatic, generate_workshop
            )
    except KeyboardInterrupt:
        print(f"\n\n {Config.RED} ⚠️ Arrêt demandé. {Config.RESET}")
        return

    if project is None:
        return

    print("\n" + "=" * 70)
    print("  Résumé de la traduction")
    print("=" * 70)
    print(f"{Config.GREEN}{Config.FILE_SCANNED} : {project.scanned_files}")
    print(f"{Config.FROM_MEMORY} : {project.cached_count}")
    print(f"{Config.NEW_TRANSLATIONS} : {project.translated_count}")
    print(f"{Config.TEXT_UNITS} : {sum(len(v) for v in project.files.values())}{Config.RESET}")

    if project.failed_files:
        print(f"\n{Config.RED}⚠️ Fichiers en échec: {len(project.failed_files)} {Config.RESET}")
        for failed_file in project.failed_files:
            print(f"   - {failed_file}")

    print("=" * 70 + f"{Config.RESET}\n")

if __name__ == "__main__":
    main()