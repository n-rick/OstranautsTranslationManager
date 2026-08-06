"""Scan des fichiers JSON du projet."""

from pathlib import Path

from models.text_unit import TextUnit
from scanner.json_extractor import JsonExtractor


class Scanner:
    """Parcourt un répertoire pour trouver les fichiers JSON à traduire."""

    def __init__(self) -> None:
        """Initialise l'extracteur et le compteur de fichiers scannés."""
        self.extractor = JsonExtractor()
        self.scanned_files = 0

    def scan(self, directory: str) -> list[TextUnit]:
        """Retourne toutes les unités de texte extraites des fichiers JSON du répertoire."""
        units: list[TextUnit] = []

        for file in Path(directory).rglob("*.json"):
            self.scanned_files += 1
            try:
                units.extend(self.extractor.extract(str(file)))
            except Exception as error:
                print(f"[ERROR] {file}")
                print(error)

        return units