from enum import Enum
from config.config import Config


class ReviewAction(Enum):
    VALIDATE = "V"
    EDIT = "E"
    SKIP = "S"
    QUIT = "Q"