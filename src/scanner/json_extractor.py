import json
import hashlib
from pathlib import Path
from models.text_unit import TextUnit


class JsonExtractor:
    def extract(self, file_path: str) -> list[TextUnit]:
        with open(file_path, "r", encoding="utf-8-sig") as file:
            data = json.load(file)

        units: list[TextUnit] = []

        self._process_value(
            value=data,
            path="$",
            source_file=Path(file_path).name,
            units=units,
        )

        return units

    def _process_value(
        self,
        value,
        path: str,
        source_file: str,
        units: list[TextUnit],
    ) -> None:
        if isinstance(value, dict):
            self._process_dict(value, path, source_file, units)

        elif isinstance(value, list):
            self._process_list(value, path, source_file, units)

        elif isinstance(value, str):
            self._process_string(value, path, source_file, units)

    def _process_dict(
        self,
        value: dict,
        path: str,
        source_file: str,
        units: list[TextUnit],
    ) -> None:
        for key, item in value.items():
            self._process_value(
                item,
                f"{path}.{key}",
                source_file,
                units,
            )

    def _process_list(
        self,
        value: list,
        path: str,
        source_file: str,
        units: list[TextUnit],
    ) -> None:
        for index, item in enumerate(value):
            self._process_value(
                item,
                f"{path}[{index}]",
                source_file,
                units,
            )

    def _process_string(
        self,
        value: str,
        path: str,
        source_file: str,
        units: list[TextUnit],
    ) -> None:
        if not value.strip():
            return

        uid = hashlib.sha1(f"{source_file}:{path}".encode("utf-8")).hexdigest()

        field = path.split(".")[-1]

        units.append(
            TextUnit(
                uid=uid,
                source_file=source_file,
                json_path=path,
                field=field,
                source_text=value,
            )
        )
