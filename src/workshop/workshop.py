"""Génération de données pour le workshop."""
import json
from pathlib import Path
from src.models.translation_project import TranslationProject

class WorkshopGenerator:
    """Service de génération des données de workshop."""

    def __init__(
        self,
        mod_name: str,
        author: str,
        mod_version: str,
        game_version: str = "1.0.0",
        mod_url: str = "",
        notes: str = "",
    ):
        self.mod_name = mod_name
        self.author = author
        self.mod_version = mod_version
        self.game_version = game_version
        self.mod_url = mod_url
        self.notes = notes

    def build(self, project: TranslationProject, output_dir: str) -> Path:
        """Construit la structure complète du mod pour le Workshop.

        Args:
            project: Projet de traduction contenant les fichiers traduits
            output_dir: Répertoire de sortie (ex: ./workshop_output)

        Returns:
            Path: Chemin vers le dossier du mod généré
        """
        # Créer la structure de sortie
        mod_dir = Path(output_dir) / self.mod_name
        data_dir = mod_dir / "data"

        # Créer les dossiers
        data_dir.mkdir(parents=True, exist_ok=True)

        # Copier les fichiers traduits depuis le projet
        # Les fichiers sont déjà écrits dans OUTPUT_PATH par JsonWriter
        output_path = Path(project.root_directory).parent / "output"

        for relative_path, units in project.files.items():
            source_file = output_path / relative_path
            dest_file = data_dir / relative_path

            # S'assurer que le chemin parent existe
            dest_file.parent.mkdir(parents=True, exist_ok=True)

            # Copier le fichier traduit
            if source_file.exists():
                import shutil
                shutil.copy2(source_file, dest_file)

        # Générer mod_info.json
        self._generate_mod_info(mod_dir)

        return mod_dir

    def _generate_mod_info(self, mod_dir: Path) -> None:
        """Génère le fichier mod_info.json."""
        mod_info = [{
            "strName": self.mod_name,
            "strAuthor": self.author,
            "strModURL": self.mod_url,
            "strGameVersion": self.game_version,
            "strModVersion": self.mod_version,
            "strNotes": self.notes
        }]

        mod_info_path = mod_dir / "mod_info.json"
        with open(mod_info_path, "w", encoding="utf-8") as f:
            json.dump(mod_info, f, ensure_ascii=False, indent=4)

    def generate_loading_order(self, mods_dir: str, mod_names: list[str]) -> None:
        """Génère le fichier loading_order.json pour Ostranauts_Data/."""
        loading_order = {"aLoadOrder": mod_names}

        loading_order_path = Path(mods_dir).parent / "loading_order.json"
        with open(loading_order_path, "w", encoding="utf-8") as f:
            json.dump(loading_order, f, ensure_ascii=False, indent=4)