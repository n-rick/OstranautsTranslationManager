import deepl

from src.config.config import Config
from src.models.text_unit import TextUnit
from src.models.translation_status import TranslationStatus
from src.translator.placeholder_manager import PlaceholderManager
from src.translator.translator import (
    TranslationRateLimitError,
    TranslationServiceError,
)


class DeepLTranslatorService:
    """Service de traduction basé sur l'API officielle DeepL."""

    def __init__(self) -> None:
        auth_key = Config.DEEPL_AUTH_KEY.strip()
        if not auth_key:
            raise ValueError(
                "La clé DeepL manque : ajoutez DEEPL_AUTH_KEY dans votre fichier .env."
            )

        self.translator = deepl.Translator(auth_key)
        self.placeholder_manager = PlaceholderManager()

    def translate(self, unit: TextUnit) -> TextUnit:
        protected = self.placeholder_manager.protect(unit.source_text)
        source_language = Config.SOURCE_LANGUAGE.upper()
        if source_language == "AUTO":
            source_language = None

        try:
            result = self.translator.translate_text(
                protected,
                source_lang=source_language,
                target_lang=Config.TARGET_LANGUAGE.upper(),
                preserve_formatting=True,
            )
        except (deepl.TooManyRequestsException, deepl.QuotaExceededException) as error:
            raise TranslationRateLimitError(str(error)) from error
        except deepl.DeepLException as error:
            raise TranslationServiceError(str(error)) from error

        unit.translated_text = self.placeholder_manager.restore(result.text)
        unit.status = TranslationStatus.AUTO_TRANSLATED
        return unit