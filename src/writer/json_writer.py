import json
import re

from pathlib import Path

from src.models.text_unit import TextUnit
from src.models.translation_project import TranslationProject
from src.models.unit_type import UnitType


class JsonWriter:

    def write(
        self,
        project: TranslationProject,
        output_directory: str,
    ) -> None:

        for relative_path, units in project.files.items():

            input_file = Path(project.root_directory) / relative_path
            output_file = Path(output_directory) / relative_path

            self._write_file(
                input_file,
                output_file,
                units,
            )
    
    
    def _write_file(
        self,
        input_file: Path,
        output_file: Path,
        units: list[TextUnit],
    ) -> None:

        with open(input_file, "r", encoding="utf-8-sig") as file:
            data = json.load(file)

        for unit in units:
            self._set_value(
                data,
                unit
            )

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(output_file, "w", encoding="utf-8-sig") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4,
            )

    def _set_value(
        self,
        data,
        unit: TextUnit,
    ) -> None:
        clean_path = (
            unit.json_path
            .removeprefix("$")
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

        # Nouvelle valeur
        new_value = self._build_value(old_value, unit)

        # Écriture
        if last_token.isdigit():
            current[int(last_token)] = new_value
        else:
            current[last_token] = new_value

    def _build_value(
        self,
        old_value,
        unit: TextUnit,
    ) -> str:

        if unit.type == UnitType.NORMAL:
            return unit.translated_text

        if unit.type == UnitType.A_OVERRIDE_VALUES:
            key = old_value.split("|", 1)[0]
            return f"{key}|{unit.translated_text}"

        if unit.type == UnitType.A_OVERRIDE_TRIGGER_IA_VALUES:
            key = old_value.split("|", 1)[0]
            return f"{key}|{unit.translated_text}"

        if unit.type == UnitType.A_PHASE_TITLES:
            return unit.translated_text

        if unit.type == UnitType.A_VALUES:
            return unit.translated_text

        return unit.translated_text