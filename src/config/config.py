from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
load_dotenv(".env.local", override=True)


class Config:
    OSTRANAUTS_DATA_PATH = Path(os.getenv("OSTRANAUTS_DATA_PATH", ""))
    OUTPUT_PATH = Path(os.getenv("OUTPUT_PATH", "./output"))
    REPORT_PATH = Path(os.getenv("REPORT_PATH", "./reports"))
    DATABASE_PATH = Path(os.getenv("DATABASE_PATH", "./database/translation_memory.json"))
    SOURCE_LANGUAGE = os.getenv("SOURCE_LANGUAGE", "en")
    TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE", "")
