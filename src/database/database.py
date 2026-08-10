"""Gestion de la base de données de mémoire de traduction."""
import json
from pathlib import Path
from typing import Optional

from src.config.config import Config

class Database:
    """Stocke et récupère les traductions déjà effectuées."""

    def __init__(self, db_path: str):
        """Initialise la base de données avec le chemin du fichier."""
        self.db_path = Path(db_path)
        self.translations = {}
        self._loaded = False

    def load(self) -> None:
        """Charge les traductions depuis le fichier."""
        if self._loaded:
            return

        try:
            if self.db_path.exists():
                with open(self.db_path, "r", encoding="utf-8") as f:
                    self.translations = json.load(f)
            else:
                # Créer le dossier parent si nécessaire
                self.db_path.parent.mkdir(parents=True, exist_ok=True)
                self.translations = {}
            self._loaded = True
        except Exception as e:
            print(f"[WARNING] Impossible de charger la base de données: {e}")
            self.translations = {}
            self._loaded = True

    def save(self) -> None:
        """Sauvegarde les traductions dans le fichier."""
        try:
            # S'assurer que le dossier parent existe
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(self.translations, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"{Config.RED} [ERROR] Impossible de sauvegarder la base de données: {e}\n{Config.RESET}")

    def get_translation(self, uid: str) -> Optional[str]:
        """Récupère une traduction depuis la base de données."""
        if not self._loaded:
            self.load()
        return self.translations.get(uid)

    def update(self, text_unit) -> None:
        """Met à jour une traduction dans la base de données."""
        if not self._loaded:
            self.load()

        if hasattr(text_unit, 'uid') and hasattr(text_unit, 'translated_text'):
            self.translations[text_unit.uid] = {
                "source": text_unit.source_text,
                "translation": text_unit.translated_text,
                "field": text_unit.field,
                "path": text_unit.json_path,
                "relative_path": text_unit.relative_path,
            }

    def get_all(self) -> dict:
        """Retourne toutes les traductions."""
        if not self._loaded:
            self.load()
        return self.translations