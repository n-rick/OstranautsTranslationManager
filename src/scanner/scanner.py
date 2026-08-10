"""Scan des fichiers JSON du projet."""

from pathlib import Path

from src.config.config import Config
from src.models.text_unit import TextUnit
from src.models.translation_project import TranslationProject
from src.scanner.json_extractor import JsonExtractor


class Scanner:
    """Parcourt un répertoire pour trouver les fichiers JSON à traduire."""

    def __init__(self) -> None:
        """Initialise l'extracteur et le compteur de fichiers scannés."""
        self.extractor = JsonExtractor()

    def scan(self, directory: str) -> TranslationProject:
        """Retourne toutes les unités de texte extraites des fichiers JSON du répertoire."""
        project = TranslationProject()

        files = sorted(Path(directory).rglob("*.json"))

        for file in files:
            project.scanned_files += 1
            try:
                relative = str(file.relative_to(directory))
                project.files[relative] = self.extractor.extract(
                    str(file),
                    relative,
                    )
            except Exception as error:
                project.failed_files.append(str(file))
                print(f"{Config.RED}[ERROR] {file}")
                print(error)

        project.root_directory = directory
        return project
    
    def scan_file(self, file_path: str) -> TranslationProject:
        """Retourne toutes les unités de texte extraites d'un fichier JSON spécifique."""
        project = TranslationProject()
        file = Path(file_path)
        
        try:
            project.scanned_files = 1
            project.root_directory = str(file.parent)
            
            relative_path= file.name
            project.files[relative_path] = self.extractor.extract(
                str(file),
                relative_path,
            )
            
            return project

        except Exception as error:
            project.failed_files.append(str(file))
            print(f"{Config.RED}[ERROR] {file}")
            print(error)

        project.root_directory = str(Path(file_path).parent)
        return project