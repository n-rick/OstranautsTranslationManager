import re
from pathlib import Path

from src.reports.reports import ReportGenerator
from src.config.config import Config


class FakeProject:
    def __init__(self, scanned_files, cached_count, translated_count, files, failed_files=None):
        self.scanned_files = scanned_files
        self.cached_count = cached_count
        self.translated_count = translated_count
        self.files = files
        self.failed_files = failed_files or []


def _read_report(path: Path) -> str:
    with path.open("r", encoding="utf-8") as fh:
        return fh.read()


def test_generate_report_single_file(tmp_path):
    Config.REPORT_PATH = tmp_path

    project = FakeProject(
        scanned_files=1,
        cached_count=0,
        translated_count=1,
        files={"file.json": ["unit1"]},
    )

    gen = ReportGenerator()
    report_path = gen.generate(project, automatic=False, generated_workshop=False)

    assert report_path.exists()
    content = _read_report(report_path)

    assert "Traitement automatique: Non" in content
    assert "Mod Workshop généré: Non" in content
    assert f"{Config.FILE_SCANNED} : 1" in content
    assert f"{Config.FROM_MEMORY} : 0" in content
    assert f"{Config.NEW_TRANSLATIONS} : 1" in content


def test_generate_report_with_mod(tmp_path):
    Config.REPORT_PATH = tmp_path

    project = FakeProject(
        scanned_files=2,
        cached_count=1,
        translated_count=3,
        files={"a.json": ["u1", "u2"], "b.json": ["u3"]},
    )

    gen = ReportGenerator()
    report_path = gen.generate(project, automatic=False, generated_workshop=True)

    assert report_path.exists()
    content = _read_report(report_path)

    assert "Traitement automatique: Non" in content
    assert "Mod Workshop généré: Oui" in content
    assert f"{Config.FILE_SCANNED} : 2" in content
    assert f"{Config.FROM_MEMORY} : 1" in content
    assert f"{Config.NEW_TRANSLATIONS} : 3" in content


def test_generate_report_auto_directory_with_mod(tmp_path):
    Config.REPORT_PATH = tmp_path

    # Simule un répertoire contenant deux sous-dossiers
    files = {
        "dir1/file1.json": ["t1", "t2"],
        "dir2/file2.json": ["t3"],
        "dir2/file3.json": ["t4", "t5", "t6"],
    }

    project = FakeProject(
        scanned_files=6,
        cached_count=2,
        translated_count=4,
        files=files,
        failed_files=["dir2/file2.json"],
    )

    gen = ReportGenerator()
    report_path = gen.generate(project, automatic=True, generated_workshop=True)

    assert report_path.exists()
    content = _read_report(report_path)

    assert "Traitement automatique: Oui" in content
    assert "Mod Workshop généré: Oui" in content

    # Vérifie le nombre total d'unités de texte
    total_units = sum(len(v) for v in files.values())
    assert f"{Config.TEXT_UNITS} : {total_units}" in content

    # Vérifie que les fichiers en échec sont listés
    assert "Fichiers en échec: 1" in content
    assert "dir2/file2.json" in content
