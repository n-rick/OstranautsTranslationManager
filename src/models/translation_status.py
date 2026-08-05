from enum import Enum


class TranslationStatus(Enum):
    NEW = "NEW"
    VALIDATED = "VALIDATED"
    MODIFIED = "MODIFIED"
    SKIPPED = "SKIPPED"