"""Gestion du flux principal de traduction des unités de texte."""
from pathlib import Path
from src.database.database import Database
from src.models.translation_project import TranslationProject
from src.models.translation_status import TranslationStatus
from src.scanner.scanner import Scanner
from src.config.config import Config
from src.ui.review_action import ReviewAction
from src.ui.console import ConsoleUI
from src.translator.translator import Translator
from src.models.text_unit import TextUnit
from src.writer.json_writer import JsonWriter

class TranslationManager:
    """Orchestre l'analyse, la traduction et la sauvegarde des textes."""

    def __init__(
        self,
        scanner: Scanner,
        database: Database,
        translator: Translator,
        console: ConsoleUI,
        writer: JsonWriter,
    ) -> None:
        """Initialise les dépendances du gestionnaire et ses compteurs."""
        self.scanner = scanner
        self.database = database
        self.translator = translator
        self.console = console
        self.writer = writer
        self.cached_count = 0
        self.translated_count = 0
        self._last_progress_length = 0

    def run(
        self, directory: str, automatic: bool, generate_workshop: bool = False
    ) -> TranslationProject:
        """Traduit les fichiers JSON d'un répertoire."""
        project = self.scanner.scan(directory)
        return self._process_project(project, automatic, generate_workshop)

    def run_file(
        self, file_path: str, automatic: bool, generate_workshop: bool = False
    ) -> TranslationProject:
        """Traduit un fichier JSON unique."""
        project = self.scanner.scan_file(file_path)
        return self._process_project(project, automatic, generate_workshop)

    def _process_project(
        self,
        project: TranslationProject,
        automatic: bool,
        generate_workshop: bool = False,
    ) -> TranslationProject:
        """Traite les unités du projet selon le mode choisi."""
        # Charger la base de données au début
        self.database.load()


        total_units = sum(len(units) for units in project.files.values())
        processed_units = 0

        for relative_path, units in project.files.items():
            skip_file = False
            for unit in units:
                processed_units += 1
                self._print_progress(processed_units, total_units, relative_path)

                # Vérifier si l'unité a déjà une traduction en mémoire
                translation = self.database.get_translation(unit.uid)
                if translation is not None:
                    unit.translated_text = translation.get("translation", translation)
                    self.cached_count += 1
                    continue

                # Traduire automatiquement
                self.translator.translate(unit)
                unit.status = TranslationStatus.AUTO_TRANSLATED

                # Mode manuel : demander une revue
                if not automatic:
                    action = self.console.review(relative_path, unit)
                    if action == ReviewAction.EDIT:
                        self.console.edit(unit)
                    elif action == ReviewAction.SKIP:
                        continue
                    elif action == ReviewAction.NEXT_FILE:
                        skip_file = True
                        break
                    elif action == ReviewAction.QUIT:
                        self.database.save()
                        project.cached_count = self.cached_count
                        project.translated_count = self.translated_count
                        return project

                # Mettre à jour la base de données avec la nouvelle traduction
                self.database.update(unit)
                self.translated_count += 1

            if skip_file:
                continue
        print()

        # Sauvegarder la base de données à la fin
        self.database.save()

        # Écrire les fichiers traduits
        self.writer.write(project, Config.OUTPUT_PATH)

        # Générer le mod Workshop si demandé
        if generate_workshop:
            self._generate_workshop(project)

        project.cached_count = self.cached_count
        project.translated_count = self.translated_count
        return project

    def _generate_workshop(self, project: TranslationProject) -> None:
        """Génère un mod Workshop à partir du projet traduit."""
        from src.workshop.workshop import WorkshopGenerator

        workshop_gen = WorkshopGenerator(
            mod_name=Config.WORKSHOP_MOD_NAME,
            author=Config.WORKSHOP_AUTHOR,
            mod_version=Config.WORKSHOP_MOD_VERSION,
            game_version=Config.WORKSHOP_GAME_VERSION,
            mod_url=Config.WORKSHOP_MOD_URL,
            notes=Config.WORKSHOP_NOTES,
        )

        mod_dir = workshop_gen.build(project, Config.WORKSHOP_OUTPUT_PATH)
        workshop_gen.generate_loading_order(
            str(Path(Config.WORKSHOP_OUTPUT_PATH) / Config.WORKSHOP_MOD_NAME),
            [Config.WORKSHOP_MOD_NAME],
        )
        print(f"\n{Config.GREEN} ✅ Mod Workshop généré dans: {mod_dir} {Config.RESET}\n")


    def _print_progress(self, current: int, total: int, filename: str) -> None:
        """Affiche une barre de progression ASCII."""
        import sys
        percent = current / total if total else 0
        bar_length = 40
        filled_length = int(bar_length * percent)
        bar = "█" * filled_length + "-" * (bar_length - filled_length)
        message = f"[{bar}] {current}/{total} ({percent:.1%}) - {filename}"

        if len(message) < self._last_progress_length:
            message += " " * (self._last_progress_length - len(message))

        sys.stdout.write(f"\r{message}")
        sys.stdout.flush()
        self._last_progress_length = len(message)