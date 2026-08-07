import json
import re

from pathlib import Path

from models.text_unit import TextUnit
from models.translation_project import TranslationProject


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
                unit.json_path,
                unit.translated_text,
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
        json_path: str,
        value: str,
    ) -> None:
        # Supprime le '$' initial et les points/crochets superflus pour le découpage
        clean_path = (
            json_path
            .removeprefix("$")
            .replace("[", ".")
            .replace("]", "")
        )
        
        tokens = [t for t in clean_path.split(".") if t]
        
        if not tokens:
            return
            
        current = data

        # On navigue jusqu'à l'avant-dernier élément
        for token in tokens[:-1]:
            if token.isdigit():
                current = current[int(token)]  
            else:
                current = current[token]
                
        last_token = tokens[-1]
        
        # On applique la traduction sur le dernier élément
        if last_token.isdigit():
            current[int(last_token)] = value
        else:
            current[last_token] = value
