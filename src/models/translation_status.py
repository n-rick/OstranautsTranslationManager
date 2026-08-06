from enum import Enum
from config.config import Config


class TranslationStatus(Enum):
    NEW = Config.NEW
    AUTO_TRANSLATED = Config.AUTO_TRANSLATED
    VALIDATED = Config.VALIDATED
    MODIFIED = Config.MODIFIED
    SKIPPED = Config.SKIPPED