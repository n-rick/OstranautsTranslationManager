import json
from pathlib import Path

from src.database.database import Database
from src.translation_manager import TranslationManager
from src.scanner.scanner import Scanner
from src.translator.translator import Translator
from src.ui.console import ConsoleUI
from src.writer.json_writer import JsonWriter


class DummyTranslator(Translator):
    def translate(self, unit):
        unit.translated_text = f"translated:{unit.source_text}"
        return unit.translated_text


class DummyScanner(Scanner):
    def __init__(self, project):
        self.project = project

    def scan(self, directory: str):
        return self.project

    def scan_file(self, file_path: str):
        return self.project


class DummyConsole(ConsoleUI):
    def review(self, relative_path, unit):
        return None


class DummyWriter(JsonWriter):
    def write(self, project, output_directory: str):
        pass

    def write_file(self, project, relative_path: str, output_directory: str):
        pass


class DummyProject:
    def __init__(self, root_directory, files):
        self.root_directory = root_directory
        self.scanned_files = len(files)
        self.files = files
        self.failed_files = []


def test_database_get_last_entry(tmp_path):
    db_path = tmp_path / "translation_memory.json"
    db = Database(str(db_path))
    db.translations = {
        "uid1": {"relative_path": "a.json", "path": "$.x", "translation": "A"},
        "uid2": {"relative_path": "b.json", "path": "$.y", "translation": "B"},
    }
    db._loaded = True

    last_uid, last_entry = db.get_last_entry()

    assert last_uid == "uid2"
    assert last_entry["relative_path"] == "b.json"


def test_resume_file_determination(tmp_path):
    db_path = tmp_path / "translation_memory.json"
    db = Database(str(db_path))
    db.translations = {
        "uid1": {"relative_path": "a.json", "path": "$.x", "translation": "A"},
        "uid2": {"relative_path": "b.json", "path": "$.y", "translation": "B"},
    }
    db._loaded = True

    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True)
    output_file = output_dir / "b.json"
    with output_file.open("w", encoding="utf-8") as f:
        json.dump({"y": "B"}, f)

    manager = TranslationManager(
        scanner=DummyScanner(DummyProject(str(tmp_path), {})),
        database=db,
        translator=DummyTranslator(),
        console=DummyConsole(),
        writer=DummyWriter(),
    )

    # for this test, temporarily override Config.OUTPUT_PATH
    from src.config.config import Config
    old_output_path = Config.OUTPUT_PATH
    Config.OUTPUT_PATH = output_dir

    resume_file = manager._determine_resume_file()

    Config.OUTPUT_PATH = old_output_path

    assert resume_file == "b.json"


def test_resume_skips_until_last_file(tmp_path):
    project_files = {
        "a.json": [],
        "b.json": [],
        "c.json": [],
    }
    project = DummyProject(str(tmp_path), project_files)

    db_path = tmp_path / "translation_memory.json"
    db = Database(str(db_path))
    db.translations = {
        "uid1": {"relative_path": "a.json", "path": "$.x", "translation": "A"},
        "uid2": {"relative_path": "b.json", "path": "$.y", "translation": "B"},
    }
    db._loaded = True

    manager = TranslationManager(
        scanner=DummyScanner(project),
        database=db,
        translator=DummyTranslator(),
        console=DummyConsole(),
        writer=DummyWriter(),
    )

    project = manager._process_project(project, automatic=True, generate_workshop=False, resume=True)

    assert project.scanned_files == 3
    assert manager.cached_count == 0
    assert manager.translated_count == 0


def test_recover_corrupt_database(tmp_path):
    db_path = tmp_path / "translation_memory.json"
    corrupted = '{"uid1": {"relative_path": "a.json", "path": "$.x", "translation": "A"}, "uid2": {"relative_path": "b.json", "path": "$.y", "translation": "B"'  # missing closing braces
    db_path.write_text(corrupted, encoding="utf-8")

    db = Database(str(db_path))
    db.load()

    assert "uid1" in db.translations
    assert db.translations["uid1"]["relative_path"] == "a.json"
    assert "uid2" not in db.translations or db.translations["uid2"]["relative_path"] == "b.json"
    assert db_path.exists()
    assert db_path.with_suffix(".json.corrupt.bak").exists()
