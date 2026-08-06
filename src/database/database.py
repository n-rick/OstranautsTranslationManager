import json
from pathlib import Path
from models.text_unit import TextUnit


class Database:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.memory: dict = {"translations": {}}

    def load(self) -> None:
        if not self.database_path.exists():
            return

        try:
            with open(self.database_path, "r", encoding="utf-8") as file:
                self.memory = json.load(file)
        except (json.JSONDecodeError, OSError):
            self.memory = {"translations": {}}

    def save(self) -> None:
        with open(self.database_path, "w", encoding="utf-8") as file:
            json.dump(
                self.memory,
                file,
                ensure_ascii=False,
                indent=4,
            )
    
    def add(self, unit: TextUnit) -> None:
        self.memory["translations"][unit.uid] = {
            "source_text": unit.source_text,
            "translated_text": unit.translated_text,
        }
    
    def contains(self, uid: str) -> bool:
        return uid in self.memory["translations"]
    
    def get_translation(self, uid: str) -> str | None:
        translation = self.memory["translations"].get(uid)

        if translation is None:
            return None

        return translation["translated_text"]