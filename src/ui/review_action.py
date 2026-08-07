"""Actions possibles lors de la revue d'une traduction."""

from enum import Enum
from src.config.config import Config


class ReviewAction(Enum):
    """Représente les choix disponibles dans l'interface de revue."""

    VALIDATE = "V"
    EDIT = "E"
    SKIP = "S"
    NEXT_FILE = "N"
    QUIT = "Q"