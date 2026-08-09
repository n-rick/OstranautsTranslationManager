"""Gestion du flux principal de traduction des unités de texte."""

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

    def run(self,
            directory: str,
            automatic: bool,
        ) -> TranslationProject:
        """Traduit les fichiers JSON d'un répertoire."""

        project = self.scanner.scan(directory)

        return self._process_project(
            project,
            automatic
        )

    
    def run_file(self,
                 file_path: str,
                 automatic: bool,
        ) -> TranslationProject:
        """Traduit un fichier JSON unique."""

        project = self.scanner.scan_file(file_path)

        return self._process_project(
            project,
            automatic,
        )
    
    
    def _process_project(
        self,
        project: TranslationProject,
        automatic: bool,
    ) -> TranslationProject:
        """Traite les unités du projet selon le mode choisi."""

        self.database.load()

        for relative_path, units in project.files.items():

            skip_file = False

            for unit in units:

                translation = self.database.get_translation(unit.uid)

                if translation is not None:
                    unit.translated_text = translation
                    self.cached_count += 1
                    continue

                self.translator.translate(unit)

                unit.status = TranslationStatus.AUTO_TRANSLATED

                if not automatic:
                    action = self.console.review(
                        relative_path,
                        unit,
                    )

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

                self.database.update(unit)
                self.translated_count += 1

            if skip_file:
                continue

        self.database.save()

        self.writer.write(
            project,
            Config.OUTPUT_PATH,
        )

        project.cached_count = self.cached_count
        project.translated_count = self.translated_count

        return project
    