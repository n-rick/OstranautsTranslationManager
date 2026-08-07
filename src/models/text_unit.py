"""Modèle représentant une unité de texte à traduire."""

from dataclasses import dataclass

from src.models.translation_status import TranslationStatus
from src.models.unit_type import UnitType


@dataclass
class TextUnit:
    """Représente un texte extraits d'un fichier JSON à traduire."""

    uid: str
    relative_path: str
    json_path: str
    field: str
    source_text: str
    translated_text: str = ""
    comment: str = ""
    status: TranslationStatus = TranslationStatus.NEW
    type: UnitType = UnitType.NORMAL
