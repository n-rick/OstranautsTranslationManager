from database.database import Database
from scanner.scanner import Scanner
from translator.translator import Translator
from models.text_unit import TextUnit


class TranslationManager:
    
    def __init__(
        self,
        scanner: Scanner,
        database: Database,
        translator: Translator,
    ) -> None:
        self.scanner = scanner
        self.database = database
        self.translator = translator
        self.cached_count = 0
        self.translated_count = 0

    def run(self, directory: str) -> list[TextUnit]:

        units = self.scanner.scan(directory)

        self.database.load()

        for unit in units:

            translation = self.database.get_translation(unit.uid)

            if translation is not None:
                unit.translated_text = translation
                self.cached_count += 1
            else:
                self.translator.translate(unit)
                self.database.update(unit)
                self.translated_count += 1

        self.database.save()

        return units
    