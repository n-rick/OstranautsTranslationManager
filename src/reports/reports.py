"""Génération de rapports pour le projet."""
from datetime import datetime
from pathlib import Path
from typing import Any

from src.config.config import Config


class ReportGenerator:
    """Service responsable de la création des rapports.

    La méthode `generate` écrit un fichier texte dans le répertoire
    défini par `Config.REPORT_PATH`. Elle attend un objet `project`
    contenant au minimum les attributs suivants :
      - scanned_files
      - cached_count
      - translated_count
      - files (mapping vers listes de unités de texte)
      - failed_files (itérable des chemins en échec)

    Paramètres supplémentaires : `automatic` indique si le traitement
    était automatique, `generated_workshop` indique si le mod Workshop
    a été généré.
    """

    def generate(self, project: Any, automatic: bool, generated_workshop: bool) -> Path:
        """Génère le fichier de rapport et renvoie son chemin.

        Args:
            project: objet projet contenant les statistiques.
            automatic: True si le traitement était automatique.
            generated_workshop: True si le mod Workshop a été créé.

        Returns:
            Path vers le fichier rapport généré.
        """
        report_dir = Path(Config.REPORT_PATH)
        report_dir.mkdir(parents=True, exist_ok=True)

        now = datetime.now()
        filename = f"report_{now.strftime('%Y%m%d_%H%M%S')}.txt"
        report_path = report_dir / filename

        total_text_units = sum(len(v) for v in getattr(project, "files", {}).values())

        lines = []
        lines.append(now.isoformat())
        lines.append(f"Traitement automatique: {'Oui' if automatic else 'Non'}")
        lines.append(f"Mod Workshop généré: {'Oui' if generated_workshop else 'Non'}")
        lines.append("")

        files = list(getattr(project, "files", {}).keys())
        root_dir = getattr(project, "root_directory", None)
        if len(files) == 1:
            lines.append("Périmètre traité: Fichier unique")
            lines.append(f" - {files[0]}")
        else:
            lines.append("Périmètre traité: Tout le répertoire data")
            if root_dir:
                lines.append(f" - Racine: {root_dir}")
            lines.append(f" - Nombre de fichiers traités: {len(files)}")
            for file_path in sorted(files):
                lines.append(f"   - {file_path}")

        lines.append("")
        lines.append(f"{Config.FILE_SCANNED} : {getattr(project, 'scanned_files', 0)}")
        lines.append(f"{Config.FROM_MEMORY} : {getattr(project, 'cached_count', 0)}")
        lines.append(f"{Config.NEW_TRANSLATIONS} : {getattr(project, 'translated_count', 0)}")
        lines.append(f"{Config.TEXT_UNITS} : {total_text_units}")

        failed = list(getattr(project, "failed_files", []) or [])
        if failed:
            lines.append("")
            lines.append(f"Fichiers en échec: {len(failed)}")
            for f in failed:
                lines.append(f" - {f}")

        content = "\n".join(lines) + "\n"

        with report_path.open("w", encoding="utf-8") as fh:
            fh.write(content)

        return report_path
