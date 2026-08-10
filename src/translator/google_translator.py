from deep_translator import GoogleTranslator
from deep_translator.exceptions import TranslationNotFound

from src.config.config import Config
from src.models.text_unit import TextUnit
from src.models.translation_status import TranslationStatus
from src.translator.placeholder_manager import PlaceholderManager


class GoogleTranslatorService:
    """Service de traduction basé sur l'API Google Translator."""

    def __init__(self) -> None:
        self.translator = GoogleTranslator(
            source=Config.SOURCE_LANGUAGE,
            target=Config.TARGET_LANGUAGE
        )
        self.placeholder_manager = PlaceholderManager()
    

    def translate(self, unit: TextUnit) -> TextUnit:
        """Traduit un texte en protégeant les placeholders avant la traduction."""

        protected = self.placeholder_manager.protect(
            unit.source_text
        )

        try:
            # Traduire le texte protégé.
            translated = self.translator.translate(protected)

        except TranslationNotFound:
            # Google ne trouve pas de traduction.
            # On conserve le texte original et on laisse le statut NEW.
            unit.translated_text = unit.source_text
            unit.status = TranslationStatus.NEW

            return unit

        except Exception as error:
            print(
                f"{Config.RED}"
                f"Erreur de traduction : {unit.source_text}"
                f" -> {error}"
                f"{Config.RESET}"
            )

        # Restaurer les placeholders dans le texte traduit.
        unit.translated_text = self.placeholder_manager.restore(
            translated
        )

        return unit
