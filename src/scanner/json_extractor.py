"""Extraction des unités de texte depuis des fichiers JSON."""

import json
import hashlib
from pathlib import Path
from src.models.text_unit import TextUnit
from src.rules.ostranauts_rules import OstranautsRules


class JsonExtractor:
    """Parcourt un fichier JSON et crée des unités de texte traduisibles."""
    
    def __init__(self):
        self.rules = OstranautsRules()

    def extract(self,
                file_path: str,
                relative_path: str,
                ) -> list[TextUnit]:
        """Lit un fichier JSON et retourne la liste des unités de texte extraites."""
        if self.rules.should_exclude_file(relative_path):
            return []

        with open(file_path, "r", encoding="utf-8-sig") as file:
            content = file.read()

            lines = []

            for line in content.splitlines():
                stripped = line.strip()

                if stripped.startswith("//"):
                    continue

                lines.append(line)

            joined = "\n".join(lines)
            try:
                data = json.loads(joined)
            except Exception as e:
                # Tentative de nettoyage: remplacer les caractères de contrôle
                # non autorisés par un espace, puis réessayer.
                cleaned = []
                for ch in joined:
                    # Autoriser tab, LF, CR (\t, \n, \r) et les caractères >= espace
                    if ch in ("\t", "\n", "\r") or ord(ch) >= 0x20:
                        cleaned.append(ch)
                    else:
                        cleaned.append(" ")
                try:
                    data = json.loads("".join(cleaned))
                except Exception:
                    # Propager l'erreur initiale si l'analyse échoue toujours
                    raise e

        units: list[TextUnit] = []

        self._process_value(
            value=data,
            path="$",
            relative_path=relative_path,
            units=units,
        )

        return units

    def _process_value(
        self,
        value,
        path: str,
        relative_path: str,
        units: list[TextUnit],
    ) -> None:
        """Traite récursivement une valeur JSON selon son type."""
        if isinstance(value, dict):
            self._process_dict(value, path, relative_path, units)

        elif isinstance(value, list):
            self._process_list(value, path, relative_path, units)

        elif isinstance(value, str):
            self._process_string(value, path, relative_path, units)

    def _process_dict(
        self,
        value: dict,
        path: str,
        relative_path: str,
        units: list[TextUnit],
    ) -> None:
        """Parcourt un dictionnaire JSON."""

        for key, item in value.items():

            # Structure spéciale Ostranauts
            special_units = self.rules.extract_special_units(
                key,
                item,
                f"{path}.{key}",
                relative_path,
            )

            if special_units:
                units.extend(special_units)
                continue

            # Champ texte classique
            if self.rules.is_translatable(key, item):
                self._process_string(
                    item,
                    f"{path}.{key}",
                    relative_path,
                    units,
                )
                continue

            # Pour les primitives non traduisibles, ne pas créer d'unité
            if isinstance(item, (dict, list)):
                self._process_value(
                    item,
                    f"{path}.{key}",
                    relative_path,
                    units,
                )

    def _process_list(
        self,
        value: list,
        path: str,
        relative_path: str,
        units: list[TextUnit],
    ) -> None:
        """Parcourt une liste JSON et transmet chaque élément."""
        for index, item in enumerate(value):
            self._process_value(
                item,
                f"{path}[{index}]",
                relative_path,
                units,
            )

    def _process_string(
        self,
        value: str,
        path: str,
        relative_path: str,
        units: list[TextUnit],
    ) -> None:
        """Crée une unité de texte."""

        if not value.strip():
            return

        uid = hashlib.sha1(f"{relative_path}:{path}".encode("utf-8")).hexdigest()

        field = path.split(".")[-1].split("[")[0]

        units.append(
            TextUnit(
                uid=uid,
                relative_path=relative_path,
                json_path=path,
                field=field,
                source_text=value,
            )
        )
