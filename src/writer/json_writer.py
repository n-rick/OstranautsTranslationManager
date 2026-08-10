"""Écriture des fichiers JSON traduits."""
import json
from pathlib import Path
from src.models.text_unit import TextUnit
from src.models.translation_project import TranslationProject
from src.rules.ostranauts_rules import OstranautsRules

class JsonWriter:
    """Écrit les fichiers JSON traduits dans le répertoire de sortie."""

    def __init__(self):
        self.rules = OstranautsRules()

    def write(
        self, project: TranslationProject, output_directory: str
    ) -> None:
        """Écrit tous les fichiers du projet en conservant leur chemin relatif."""
        output_path = Path(output_directory)

        for relative_path, units in project.files.items():
            # Vérifier si le fichier doit être exclu
            if self.rules.should_exclude_file(relative_path):
                print(f"[SKIP] Exclusion du fichier: {relative_path}")
                continue

            input_file = Path(project.root_directory) / relative_path
            output_file = output_path / relative_path

            # S'assurer que le dossier parent existe
            output_file.parent.mkdir(parents=True, exist_ok=True)

            self._write_file(input_file, output_file, units)

    def _write_file(
        self, input_file: Path, output_file: Path, units: list[TextUnit]
    ) -> None:
        """Charge, modifie et écrit un fichier JSON."""
        # Lire le fichier source
        with open(input_file, "r", encoding="utf-8-sig") as file:
            content = file.read()

        lines = []
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("//"):
                continue
            lines.append(line)

        data = json.loads("\n".join(lines))

        # Appliquer les traductions
        for unit in units:
            self._set_value(data, unit)

        # Écrire le fichier de sortie
        with open(output_file, "w", encoding="utf-8-sig") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def _set_value(self, data, unit: TextUnit) -> None:
        """Remplace la valeur correspondant au chemin JSON de l'unité."""
        clean_path = (
            unit.json_path.removeprefix("$")
            .replace("[", ".")
            .replace("]", "")
        )
        tokens = [token for token in clean_path.split(".") if token]
        if not tokens:
            return

        current = data
        # Navigation jusqu'au parent
        for token in tokens[:-1]:
            if token.isdigit():
                current = current[int(token)]
            else:
                current = current[token]

        last_token = tokens[-1]
        # Valeur actuelle
        if last_token.isdigit():
            old_value = current[int(last_token)]
        else:
            old_value = current[last_token]

        new_value = self._build_value(old_value, unit)

        if last_token.isdigit():
            current[int(last_token)] = new_value
        else:
            current[last_token] = new_value

    def _build_value(self, old_value, unit: TextUnit) -> str:
        """Construit la valeur finale à écrire."""
        # Pour les champs avec | (format spécial pour les overrides)
        if (
            unit.field in {"strTitle", "strDesc"}
            and isinstance(old_value, str)
            and "|" in old_value
        ):
            key = old_value.split("|", 1)[0]
            return f"{key}|{unit.translated_text}"
        return unit.translated_text
