"""Chargement de la configuration de l'application à partir des variables d'environnement."""

from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
load_dotenv(".env.local", override=True)


class Config:
    """Contient les paramètres globaux utilisés par l'application."""

    OSTRANAUTS_DATA_PATH = Path(os.getenv("OSTRANAUTS_DATA_PATH", ""))
    OUTPUT_PATH = Path(os.getenv("OUTPUT_PATH", "./output"))
    REPORT_PATH = Path(os.getenv("REPORT_PATH", "./reports"))
    DATABASE_PATH = Path(os.getenv("DATABASE_PATH", "./database/translation_memory.json"))
    SOURCE_LANGUAGE = os.getenv("SOURCE_LANGUAGE", "en")
    TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE", "")
    FILE_SCANNED = os.getenv("FILE_SCANNED", "")
    TEXT_UNITS = os.getenv("TEXT_UNITS", "")
    FROM_MEMORY = os.getenv("FROM_MEMORY", "")
    NEW_TRANSLATIONS = os.getenv("NEW_TRANSLATIONS", "")
    NEW = os.getenv("NEW", "")
    AUTO_TRANSLATED = os.getenv("AUTO_TRANSLATED", "")
    VALIDATED = os.getenv("VALIDATED", "")
    MODIFIED = os.getenv("MODIFIED", "")
    SKIPPED = os.getenv("SKIP", "")
    VALIDATE = os.getenv("VALIDATE", "")
    EDIT = os.getenv("EDIT", "")
    SKIP = os.getenv("SKIP", "")
    NEXT_FILE = os.getenv("NEXT_FILE", "")
    QUIT = os.getenv("QUIT", "")
