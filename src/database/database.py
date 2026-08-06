"""Persistance des traductions dans un fichier JSON."""

import json
from pathlib import Path
from models.text_unit import TextUnit


class Database:
    """Gère la lecture et l'écriture de la mémoire de traduction."""

    def __init__(self, database_path: Path) -> None:
        """Initialise le chemin du fichier de base de données."""
        self.database_path = database_path
        self.memory: dict = {"translations": {}}

    def load(self) -> None:
        """Charge les traductions depuis le fichier JSON s'il existe."""
        if not self.database_path.exists():
            return

        try:
            with open(self.database_path, "r", encoding="utf-8") as file:
                self.memory = json.load(file)
        except (json.JSONDecodeError, OSError):
            self.memory = {"translations": {}}

    def save(self) -> None:
        """Sauvegarde la mémoire de traduction dans le fichier JSON."""
        with open(self.database_path, "w", encoding="utf-8") as file:
            json.dump(
                self.memory,
                file,
                ensure_ascii=False,
                indent=4,
            )

    def update(self, unit: TextUnit) -> None:
        """Met à jour la traduction associée à une unité de texte."""
        self.memory["translations"][unit.uid] = {
            "source_text": unit.source_text,
            "translated_text": unit.translated_text,
        }

    def contains(self, uid: str) -> bool:
        """Vérifie si une traduction existe déjà pour un identifiant donné."""
        return uid in self.memory["translations"]

    def get_translation(self, uid: str) -> str | None:
        """Retourne la traduction stockée pour un identifiant, si elle existe."""
        translation = self.memory["translations"].get(uid)

        if translation is None:
            return None

        return translation["translated_text"]