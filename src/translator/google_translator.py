from deep_translator import GoogleTranslator
from config.config import Config
from models.text_unit import TextUnit
from translator.translator import Translator


class GoogleTranslatorService(Translator):

    def translate(self, unit: TextUnit) -> TextUnit:
        translated = GoogleTranslator(
            source=Config.SOURCE_LANGUAGE,
            target=Config.TARGET_LANGUAGE
        ).translate(unit.source_text)

        unit.translated_text = translated

        return unit