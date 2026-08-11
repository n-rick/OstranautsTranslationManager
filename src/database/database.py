"""Gestion de la base de données de mémoire de traduction."""
import json
from pathlib import Path
from typing import Any, Optional, Tuple

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
                    content = f.read()
                try:
                    self.translations = json.loads(content)
                except json.JSONDecodeError as e:
                    backup_path = self._backup_corrupt_file()
                    print(
                        f"[WARNING] Base corrompue détectée : {self.db_path}."
                        f" Copie de sauvegarde : {backup_path}"
                    )
                    self.translations = self._recover_translations(content)
                    if self.translations is None:
                        self.translations = {}
                    else:
                        self.save()
            else:
                # Créer le dossier parent si nécessaire
                self.db_path.parent.mkdir(parents=True, exist_ok=True)
                self.translations = {}
            self._loaded = True
        except Exception as e:
            print(f"[WARNING] Impossible de charger la base de données: {e}")
            self.translations = {}
            self._loaded = True

    def _backup_corrupt_file(self) -> Path:
        backup_path = self.db_path.with_suffix(self.db_path.suffix + ".corrupt.bak")
        self.db_path.rename(backup_path)
        return backup_path

    def _recover_translations(self, content: str) -> Optional[dict]:
        """Tente de récupérer les traductions à partir d'une base JSON partiellement valide."""
        decoder = json.JSONDecoder()
        text = content.strip()
        if not text.startswith("{"):
            return None

        idx = 1
        recovered = {}
        length = len(text)

        def _skip_whitespace(i: int) -> int:
            while i < length and text[i].isspace():
                i += 1
            return i

        while True:
            idx = _skip_whitespace(idx)
            if idx >= length or text[idx] == "}":
                break

            try:
                key, key_len = decoder.raw_decode(text[idx:])
            except json.JSONDecodeError:
                break
            idx += key_len
            idx = _skip_whitespace(idx)
            if idx >= length or text[idx] != ":":
                break
            idx += 1
            idx = _skip_whitespace(idx)

            try:
                value, value_len = decoder.raw_decode(text[idx:])
            except json.JSONDecodeError:
                break
            idx += value_len

            recovered[key] = value
            idx = _skip_whitespace(idx)
            if idx >= length:
                break
            if text[idx] == ",":
                idx += 1
                continue
            if text[idx] == "}":
                break
            break

        if recovered:
            return recovered
        return None

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

    def get_last_entry(self) -> Tuple[Optional[str], Optional[dict]]:
        """Retourne la dernière entrée enregistrée dans la base de données.

        Renvoie un tuple `(uid, entry)` ou `(None, None)` si la base est vide.
        """
        if not self._loaded:
            self.load()

        if not self.translations:
            return None, None

        last_uid, last_entry = next(reversed(self.translations.items()))
        return last_uid, last_entry

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