"""Scan des fichiers JSON du projet."""
from pathlib import Path
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
                    str(file), relative
                )
            except Exception as error:
                project.failed_files.append(str(file))
                print(f"[ERROR] {file}")
                print(error)
        project.root_directory = directory
        return project

    def scan_file(self, file_path: str, base_directory: str = None) -> TranslationProject:
        """Retourne toutes les unités de texte extraites d'un fichier JSON spécifique.

        Args:
            file_path: Chemin complet vers le fichier JSON
            base_directory: Répertoire de base pour calculer le chemin relatif.
                          Si None, utilise le parent du fichier.
        """
        project = TranslationProject()
        file = Path(file_path)
        try:
            project.scanned_files = 1

            # Déterminer le répertoire de base
            if base_directory:
                base_dir = Path(base_directory)
            else:
                # Par défaut, utiliser le parent du fichier comme base
                # mais essayer de remonter d'un niveau pour conserver la structure
                base_dir = file.parent.parent if len(file.parts) > 2 else file.parent

            # Calculer le chemin relatif
            try:
                relative_path = str(file.relative_to(base_dir))
            except ValueError:
                # Si le fichier n'est pas sous base_dir, utiliser juste le nom du fichier
                relative_path = file.name

            project.root_directory = str(base_dir)
            project.files[relative_path] = self.extractor.extract(
                str(file), relative_path
            )
            return project
        except Exception as error:
            project.failed_files.append(str(file))
            print(f"[ERROR] {file}")
            print(error)
            project.root_directory = str(Path(file_path).parent)
            return project
