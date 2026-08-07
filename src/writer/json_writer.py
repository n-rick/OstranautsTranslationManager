from pathlib import Path
from models.text_unit import TextUnit
from models.translation_project import TranslationProject


class JsonWriter:

    def write(
        self,
        input_directory: str,
        output_directory: str,
        project: TranslationProject,
    ) -> None:

        for relative_path, units in project.files.items():

            input_file = Path(input_directory) / relative_path
            output_file = Path(output_directory) / relative_path

            self._write_file(
                input_file,
                output_file,
                units,
            )