"""Gestion du flux principal de traduction des unités de texte."""

from database.database import Database
from scanner.scanner import Scanner
from config.config import Config
from ui.review_action import ReviewAction
from ui.console import ConsoleUI
from translator.translator import Translator
from models.text_unit import TextUnit


class TranslationManager:
    """Orchestre l'analyse, la traduction et la sauvegarde des textes."""

    def __init__(
        self,
        scanner: Scanner,
        database: Database,
        translator: Translator,
        console: ConsoleUI
    ) -> None:
        """Initialise les dépendances du gestionnaire et ses compteurs."""
        self.scanner = scanner
        self.database = database
        self.translator = translator
        self.console = console
        self.cached_count = 0
        self.translated_count = 0

    def run(self, directory: str) -> list[TextUnit]:
        """Exécute le processus complet de traduction pour un répertoire donné."""

        units = self.scanner.scan(directory)

        self.database.load()

        for unit in units:

            translation = self.database.get_translation(unit.uid)

            if translation is not None:
                unit.translated_text = translation
                self.cached_count += 1
            else:
                self.translator.translate(unit)
                choice = self.console.review(unit)
                if choice == ReviewAction.EDIT:
                    unit.translated_text = input(f"\n {Config.NEW_TRANSLATION} : ")
                elif choice == ReviewAction.QUIT:
                    break

                self.database.update(unit)
                self.translated_count += 1

        self.database.save()

        return units
    