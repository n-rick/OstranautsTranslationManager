from dataclasses import dataclass

from models.translation_status import TranslationStatus


@dataclass
class TextUnit:
    """
    Represents a translatable text extracted from a game file.
    """

    uid: str
    source_file: str
    json_path: str
    field: str
    source_text: str
    translated_text: str = ""
    status: TranslationStatus = TranslationStatus.NEW
    comment: str = ""
