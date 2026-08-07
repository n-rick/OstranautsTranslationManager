from dataclasses import dataclass, field

from src.models.text_unit import TextUnit


@dataclass
class TranslationProject:

    files: dict[str, list[TextUnit]] = field(default_factory=dict)

    scanned_files: int = 0
    translated_count: int = 0
    cached_count: int = 0
    root_directory: str = ""
    failed_files: list[str] = field(default_factory=list)
