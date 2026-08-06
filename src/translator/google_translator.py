from deep_translator import GoogleTranslator
from config.config import Config
from models.text_unit import TextUnit
from translator.placeholder_manager import PlaceholderManager
from translator.translator import Translator


class GoogleTranslatorService(Translator):
    """Service de traduction basé sur l'API Google Translator."""

    def translate(self, unit: TextUnit) -> TextUnit:
        """Traduit un texte en protégeant les placeholders avant la traduction."""
        manager = PlaceholderManager()

        # Protéger les placeholders pour éviter qu'ils soient altérés pendant la traduction.
        protected = manager.protect(unit.source_text)

        # Traduire le texte protégé avec la configuration de langue définie.
        translated = GoogleTranslator(
            source=Config.SOURCE_LANGUAGE,
            target=Config.TARGET_LANGUAGE
        ).translate(protected)

        # Restaurer les placeholders dans le texte traduit.
        unit.translated_text = manager.restore(translated)

        return unit