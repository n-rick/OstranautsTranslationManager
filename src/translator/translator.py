"""Interface de base pour les services de traduction."""

from src.models.text_unit import TextUnit


class TranslationServiceError(Exception):
    """Indique que le service de traduction ne peut pas traiter la requête."""


class TranslationRateLimitError(TranslationServiceError):
    """Indique que le service distant limite toujours les traductions."""


class Translator:
    """Définit le contrat attendu pour un traducteur."""

    def translate(self, unit: TextUnit) -> TextUnit:
        """Traduit une unité de texte et retourne l'objet mis à jour."""
        raise NotImplementedError