"""Gestion du flux principal de traduction des unités de texte."""

from database.database import Database
from models.translation_project import TranslationProject
from scanner.scanner import Scanner
from config.config import Config
from ui.review_action import ReviewAction
from ui.console import ConsoleUI
from translator.translator import Translator
from models.text_unit import TextUnit
from writer.json_writer import JsonWriter


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

    def run(self, directory: str) -> TranslationProject:
        """Exécute le processus complet de traduction pour un répertoire donné."""

        project = self.scanner.scan(directory)

        self.database.load()

        for relative_path, units in project.files.items():
            
            skip_file = False
            
            for unit in units:

                translation = self.database.get_translation(unit.uid)

                if translation is not None:
                    unit.translated_text = translation
                    self.cached_count += 1
                    
                else:
                    self.translator.translate(unit)
                    
                    action = self.console.review(relative_path, unit)
                    
                    if action == ReviewAction.EDIT:
                        self.console.edit(unit)
                        
                    if action == ReviewAction.NEXT_FILE:
                        skip_file = True
                        break
                    
                    if action == ReviewAction.QUIT:
                        self.database.save()
                        project.cached_count = self.cached_count
                        project.translated_count = self.translated_count
                        return project
                    
                    if action == "" or isinstance(action, KeyboardInterrupt):
                        action = ReviewAction.QUIT

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
    