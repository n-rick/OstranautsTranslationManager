"""Énumération des statuts possibles d'une unité de texte."""

from enum import Enum
from src.config.config import Config


class TranslationStatus(Enum):
    """Décrit l'état de progression d'une traduction."""

    NEW = Config.NEW
    AUTO_TRANSLATED = Config.AUTO_TRANSLATED
    VALIDATED = Config.VALIDATED
    MODIFIED = Config.MODIFIED
    SKIPPED = Config.SKIPPED