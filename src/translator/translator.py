"""Interface de base pour les services de traduction."""

from src.models.text_unit import TextUnit


class Translator:
    """Définit le contrat attendu pour un traducteur."""

    def translate(self, unit: TextUnit) -> TextUnit:
        """Traduit une unité de texte et retourne l'objet mis à jour."""
        raise NotImplementedError