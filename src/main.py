"""Point d'entrée principal de l'application de traduction."""
import argparse
from src.config.config import Config
from src.database.database import Database
from src.scanner.scanner import Scanner
from src.ui.console import ConsoleUI
from src.translator.google_translator import GoogleTranslatorService
from src.translation_manager import TranslationManager
from src.writer.json_writer import JsonWriter
from src.reports.reports import ReportGenerator
from src.ui.start_menu import StartMenu

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ostranauts Translation Manager"
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Relance la traduction en utilisant la mémoire et les fichiers déjà générés.",
    )
    parser.add_argument(
        "--path",
        type=str,
        help="Chemin vers le répertoire data ou le fichier JSON à reprendre.",
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Fichier JSON unique à traduire en mode reprise.",
    )
    parser.add_argument(
        "--generate-workshop",
        action="store_true",
        help="Générer le mod Workshop pendant la reprise.",
    )
    parser.add_argument(
        "--no-workshop",
        action="store_true",
        help="Ne pas générer le mod Workshop pendant la reprise.",
    )
    return parser.parse_args()


def main() -> None:
    """Initialise les composants et lance le processus de traduction."""
    args = parse_args()

    if args.resume:
        if args.file and args.path:
            print(f"{Config.RED}Erreur: utilisez --file ou --path, pas les deux.{Config.RESET}")
            return

        if args.file:
            scan_directory = False
            selected_file = args.file
        else:
            scan_directory = True
            selected_file = args.path or str(Config.OSTRANAUTS_DATA_PATH)

        automatic = True
        generate_workshop = args.generate_workshop or (
            Config.GENERATE_WORKSHOP and not args.no_workshop
        )
    else:
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
                selected_file, automatic, generate_workshop, args.resume
            )
        else:
            project = manager.run_file(
                selected_file, automatic, generate_workshop, args.resume
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

    try:
        report_gen = ReportGenerator()
        report_path = report_gen.generate(project, automatic, generate_workshop)
        print(f"\nRapport généré: {report_path}")
    except Exception as e:
        print(f"\n{Config.RED}Erreur lors de la génération du rapport: {e}{Config.RESET}")

    print("=" * 70 + f"{Config.RESET}\n")

if __name__ == "__main__":
    main()