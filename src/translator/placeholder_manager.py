"""Gestion des placeholders lors de la traduction."""

import re


class PlaceholderManager:
    """Protège et restaure les placeholders pour éviter leur modification."""

    PATTERN = re.compile(r"\[[^\]]+\]")

    def __init__(self) -> None:
        """Initialise la structure de stockage des placeholders."""
        self.placeholders: dict[str, str] = {}

    def protect(self, text: str) -> str:
        """Remplace les placeholders par des tokens temporaires dans le texte."""
        self.placeholders.clear()

        def replace(match):
            placeholder = match.group(0)

            token = f"__PH_{len(self.placeholders):04d}__"

            self.placeholders[token] = placeholder

            return token

        return self.PATTERN.sub(replace, text)

    def restore(self, text: str) -> str:
        """Restaure les placeholders originaux dans un texte traduit."""
        for token, placeholder in self.placeholders.items():
            text = text.replace(token, placeholder)

        return text
    
