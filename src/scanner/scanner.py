from pathlib import Path

from models.text_unit import TextUnit
from scanner.json_extractor import JsonExtractor


class Scanner:
    def __init__(self) -> None:
        self.extractor = JsonExtractor()
        self.scanned_files = 0

    def scan(self, directory: str) -> list[TextUnit]:
        units: list[TextUnit] = []

        for file in Path(directory).rglob("*.json"):
            self.scanned_files += 1
            try:
              units.extend(self.extractor.extract(str(file)))
            except Exception as error:
              print(f"[ERROR] {file}")
              print(error)

        return units