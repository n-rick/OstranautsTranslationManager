"""Modèle représentant une unité de texte à traduire."""

from dataclasses import dataclass

from models.translation_status import TranslationStatus


@dataclass
class TextUnit:
    """Représente un texte extraits d'un fichier JSON à traduire."""

    uid: str
    source_file: str
    json_path: str
    field: str
    source_text: str
    translated_text: str = ""
    status: TranslationStatus = TranslationStatus.NEW
    comment: str = ""
