from deep_translator import GoogleTranslator
from src.config.config import Config
from src.models.text_unit import TextUnit
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

        # Traduire le texte protégé avec la configuration de langue définie.
        translated = self.translator.translate(protected)

        # Restaurer les placeholders dans le texte traduit.
        unit.translated_text = self.placeholder_manager.restore(
            translated
        )

        return unit
