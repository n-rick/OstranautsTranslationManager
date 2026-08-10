"""Chargement de la configuration de l'application à partir des variables d'environnement."""
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
load_dotenv(".env.local", override=True)

class Config:
    """Contient les paramètres globaux utilisés par l'application."""

    # Couleurs
    RED = "\033[91m"
    GREEN = "\033[92m"
    RESET = "\033[0m"

    # Chemins principaux
    OSTRANAUTS_DATA_PATH = Path(
        os.getenv(
            "OSTRANAUTS_DATA_PATH",
            "/home/user/Ostranauts/Ostranauts_Data/StreamingAssets/data",
        )
    )
    OUTPUT_PATH = Path(os.getenv("OUTPUT_PATH", "./output"))
    REPORT_PATH = Path(os.getenv("REPORT_PATH", "./reports"))
    DATABASE_PATH = Path(
        os.getenv("DATABASE_PATH", "./database/translation_memory.json")
    )

    # Configuration Workshop
    WORKSHOP_MOD_NAME = os.getenv(
        "WORKSHOP_MOD_NAME", "Ostranauts - Traduction Française"
    )
    WORKSHOP_AUTHOR = os.getenv("WORKSHOP_AUTHOR", "RicoRama")
    WORKSHOP_MOD_VERSION = os.getenv("WORKSHOP_MOD_VERSION", "1.0.0")
    WORKSHOP_GAME_VERSION = os.getenv("WORKSHOP_GAME_VERSION", "1.0.0")
    WORKSHOP_MOD_URL = os.getenv(
        "WORKSHOP_MOD_URL",
        "https://github.com/n-rick/OstranautsTranslationManager",
    )
    WORKSHOP_NOTES = os.getenv(
        "WORKSHOP_NOTES",
        "Traduction complète en français pour Ostranauts v1.0. Inclut tous les textes du jeu, interfaces, descriptions et dialogues.",
    )
    WORKSHOP_OUTPUT_PATH = Path(
        os.getenv("WORKSHOP_OUTPUT_PATH", "./workshop")
    )
    GENERATE_WORKSHOP = os.getenv("GENERATE_WORKSHOP", "false").lower() == "true"

    # Langues
    SOURCE_LANGUAGE = os.getenv("SOURCE_LANGUAGE", "en")
    TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE", "fr")

    # Messages UI
    FILE_SCANNED = os.getenv(
        "FILE_SCANNED", "Fichiers scannés"
    )
    TEXT_UNITS = os.getenv("TEXT_UNITS", "Unités de texte")
    FROM_MEMORY = os.getenv("FROM_MEMORY", "Depuis la mémoire")
    NEW_TRANSLATIONS = os.getenv("NEW_TRANSLATIONS", "Nouvelles traductions")
    NEW = os.getenv("NEW", "NOUVEAU")
    AUTO_TRANSLATED = os.getenv("AUTO_TRANSLATED", "TRADUCTION AUTOMATIQUE")
    VALIDATED = os.getenv("VALIDATED", "VALIDÉ")
    MODIFIED = os.getenv("MODIFIED", "MODIFIÉ")
    SKIPPED = os.getenv("SKIP", "IGNORÉ")
    VALIDATE = os.getenv("VALIDATE", "Valider")
    EDIT = os.getenv("EDIT", "Éditer")
    SKIP = os.getenv("SKIP", "Ignorer")
    NEXT_FILE = os.getenv("NEXT_FILE", "Fichier suivant")
    QUIT = os.getenv("QUIT", "Quitter")
    TRANSLATE_ALL = os.getenv(
        "TRANSLATE_ALL", "Traduire tous les fichiers"
    )
    TRANSLATE_SINGLE = os.getenv(
        "TRANSLATE_SINGLE", "Traduire un fichier spécifique"
    )
    CHOICE = os.getenv("CHOICE", "Choix : ")
    FILE_NOT_EXISTS = os.getenv(
        "FILE_NOT_EXISTS", "Le fichier n'existe pas"
    )
    GENERATE_WORKSHOP_QUESTION = os.getenv(
        "GENERATE_WORKSHOP_QUESTION", "Générer un mod Workshop ? (o/n): "
    )