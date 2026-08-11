"""Gestion du flux principal de traduction des unités de texte."""
import json
from pathlib import Path
from src.database.database import Database
from src.models.translation_project import TranslationProject
from src.models.translation_status import TranslationStatus
from src.scanner.scanner import Scanner
from src.config.config import Config
from src.ui.review_action import ReviewAction
from src.ui.console import ConsoleUI
from src.translator.translator import Translator
from src.models.text_unit import TextUnit
from src.writer.json_writer import JsonWriter
from src.workshop.workshop import WorkshopGenerator

class TranslationManager:
    """Orchestre l'analyse, la traduction et la sauvegarde des textes."""

    def __init__(
        self,
        scanner: Scanner,
        database: Database,
        translator: Translator,
        console: ConsoleUI,
        writer: JsonWriter,
    ) -> None:
        """Initialise les dépendances du gestionnaire et ses compteurs."""
        self.scanner = scanner
        self.database = database
        self.translator = translator
        self.console = console
        self.writer = writer
        self.cached_count = 0
        self.translated_count = 0
        self._last_progress_length = 0

    def run(
        self,
        directory: str,
        automatic: bool,
        generate_workshop: bool = False,
        resume: bool = False,
    ) -> TranslationProject:
        """Traduit les fichiers JSON d'un répertoire."""
        project = self.scanner.scan(directory)
        return self._process_project(project, automatic, generate_workshop, resume)

    def run_file(
        self,
        file_path: str,
        automatic: bool,
        generate_workshop: bool = False,
        resume: bool = False,
    ) -> TranslationProject:
        """Traduit un fichier JSON unique."""
        project = self.scanner.scan_file(file_path)
        return self._process_project(project, automatic, generate_workshop, resume)

    def _process_project(
        self,
        project: TranslationProject,
        automatic: bool,
        generate_workshop: bool = False,
        resume: bool = False,
    ) -> TranslationProject:
        """Traite les unités du projet selon le mode choisi."""
        # Charger la base de données au début
        self.database.load()

        total_units = sum(len(units) for units in project.files.values())
        processed_units = 0
        current_file = ""
        workshop_gen = None
        workshop_mod_dir = None

        if generate_workshop and automatic:
            project_path = Path(project.root_directory).resolve()
            data_path = Path(Config.OSTRANAUTS_DATA_PATH).resolve()
            if project_path == data_path:
                workshop_gen = WorkshopGenerator(
                    mod_name=Config.WORKSHOP_MOD_NAME,
                    author=Config.WORKSHOP_AUTHOR,
                    mod_version=Config.WORKSHOP_MOD_VERSION,
                    game_version=Config.WORKSHOP_GAME_VERSION,
                    mod_url=Config.WORKSHOP_MOD_URL,
                    notes=Config.WORKSHOP_NOTES,
                )
                workshop_mod_dir = workshop_gen.build(project, Config.WORKSHOP_OUTPUT_PATH)
                workshop_gen.generate_loading_order(
                    str(workshop_mod_dir),
                    [Config.WORKSHOP_MOD_NAME],
                )

        resume_file = None
        resume_started = True
        if resume:
            resume_file = self._determine_resume_file()
            if resume_file:
                resume_started = False
                print(
                    f"{Config.GREEN}Reprise détectée à partir de la dernière entrée de la BDD : {resume_file}{Config.RESET}"
                )

        try:
            for relative_path, units in project.files.items():
                if not resume_started:
                    if relative_path != resume_file:
                        continue
                    resume_started = True

                current_file = relative_path
                skip_file = False
                file_has_error = False

                for unit in units:
                    processed_units += 1
                    self._print_progress(processed_units, total_units, relative_path)

                    # Vérifier si l'unité a déjà une traduction en mémoire
                    translation = self.database.get_translation(unit.uid)
                    if translation is not None:
                        unit.translated_text = translation.get("translation", translation)
                        self.cached_count += 1
                        continue

                    # Traduire automatiquement
                    try:
                        self.translator.translate(unit)
                        unit.status = TranslationStatus.AUTO_TRANSLATED
                    except KeyboardInterrupt:
                        self._handle_unexpected_error(project, current_file)
                        raise
                    except Exception as error:
                        print(
                            f"{Config.RED}Erreur de traduction : {unit.source_text}"
                            f" -> {error}{Config.RESET}"
                        )
                        file_has_error = True
                        continue

                    # Mode manuel : demander une revue
                    if not automatic:
                        action = self.console.review(relative_path, unit)
                        if action == ReviewAction.EDIT:
                            self.console.edit(unit)
                        elif action == ReviewAction.SKIP:
                            continue
                        elif action == ReviewAction.NEXT_FILE:
                            skip_file = True
                            break
                        elif action == ReviewAction.QUIT:
                            self._handle_unexpected_error(project, current_file)
                            project.cached_count = self.cached_count
                            project.translated_count = self.translated_count
                            return project

                    # Mettre à jour la base de données avec la nouvelle traduction
                    self.database.update(unit)
                    self.database.save()
                    self.translated_count += 1

                if not skip_file:
                    self._persist_file_progress(project, relative_path)
                    if workshop_gen and workshop_mod_dir:
                        workshop_gen.copy_translated_file(relative_path)
                        workshop_gen.generate_loading_order(
                            str(workshop_mod_dir),
                            [Config.WORKSHOP_MOD_NAME],
                        )

                if file_has_error and relative_path not in project.failed_files:
                    project.failed_files.append(relative_path)

                if skip_file:
                    continue
        except Exception:
            self._handle_unexpected_error(project, current_file)
            raise

        print()

        # Sauvegarder la base de données finale
        self.database.save()

        # Écrire les fichiers traduits finaux
        self.writer.write(project, Config.OUTPUT_PATH)

        # Générer le mod Workshop si demandé and not already built for incremental auto/data
        if generate_workshop and not workshop_gen:
            self._generate_workshop(project)

        project.cached_count = self.cached_count
        project.translated_count = self.translated_count
        return project

    def _determine_resume_file(self) -> str | None:
        """Détermine le fichier à partir duquel reprendre en utilisant la dernière entrée BDD."""
        last_uid, last_entry = self.database.get_last_entry()
        if not last_entry:
            return None

        relative_path = last_entry.get("relative_path")
        json_path = last_entry.get("path")
        translation = last_entry.get("translation")
        if not relative_path or not json_path:
            return None

        output_file = Path(Config.OUTPUT_PATH) / relative_path
        if output_file.exists():
            try:
                if self._output_contains_translation(output_file, json_path, translation):
                    return relative_path
                print(
                    f"{Config.RED}La dernière entrée de la BDD n'a pas été retrouvée dans le fichier de sortie {output_file}."
                    f" Reprise depuis le fichier source {relative_path}.{Config.RESET}"
                )
            except Exception:
                pass

        return relative_path

    def _output_contains_translation(
        self, output_file: Path, json_path: str, translation: str
    ) -> bool:
        with open(output_file, "r", encoding="utf-8-sig") as file:
            data = json.load(file)

        value = self._extract_value_from_json_path(data, json_path)
        return value == translation

    def _extract_value_from_json_path(self, data, json_path: str):
        clean_path = json_path.removeprefix("$")
        clean_path = clean_path.replace("[", ".").replace("]", "")
        tokens = [token for token in clean_path.split(".") if token]
        current = data
        for token in tokens:
            current = current[int(token)] if token.isdigit() else current[token]
        return current

    def _persist_file_progress(self, project: TranslationProject, relative_path: str) -> None:
        """Sauvegarde les progrès pour un fichier partiellement ou totalement traité."""
        try:
            self.writer.write_file(project, relative_path, Config.OUTPUT_PATH)
            print()
            print(
                f"{Config.GREEN}[INCR] Fichier sauvegardé : {relative_path}{Config.RESET}"
            )
        except Exception:
            pass

    def _handle_unexpected_error(
        self, project: TranslationProject, current_file: str
    ) -> None:
        """Sauvegarde le projet en cas d'erreur imprévue."""
        self.database.save()
        if current_file:
            self._persist_file_progress(project, current_file)

    def _generate_workshop(self, project: TranslationProject) -> None:
        """Génère un mod Workshop à partir du projet traduit."""
        from src.workshop.workshop import WorkshopGenerator

        workshop_gen = WorkshopGenerator(
            mod_name=Config.WORKSHOP_MOD_NAME,
            author=Config.WORKSHOP_AUTHOR,
            mod_version=Config.WORKSHOP_MOD_VERSION,
            game_version=Config.WORKSHOP_GAME_VERSION,
            mod_url=Config.WORKSHOP_MOD_URL,
            notes=Config.WORKSHOP_NOTES,
        )

        mod_dir = workshop_gen.build(project, Config.WORKSHOP_OUTPUT_PATH)
        workshop_gen.generate_loading_order(
            str(Path(Config.WORKSHOP_OUTPUT_PATH) / Config.WORKSHOP_MOD_NAME),
            [Config.WORKSHOP_MOD_NAME],
        )
        print(f"\n{Config.GREEN} ✅ Mod Workshop généré dans: {mod_dir} {Config.RESET}\n")


    def _print_progress(self, current: int, total: int, filename: str) -> None:
        """Affiche une barre de progression ASCII."""
        import sys
        from pathlib import Path

        display_name = Path(filename).name
        max_name_length = 20
        if len(display_name) > max_name_length:
            display_name = f"...{display_name[-(max_name_length - 3):]}"

        percent = current / total if total else 0
        bar_length = 30
        filled_length = int(bar_length * percent)
        bar = "█" * filled_length + "-" * (bar_length - filled_length)
        message = f"[{bar}] {current}/{total} ({percent:.1%}) - {display_name}"

        if len(message) < self._last_progress_length:
            message += " " * (self._last_progress_length - len(message))

        if sys.stdout.isatty():
            sys.stdout.write(f"\033[2K\r{message}")
        else:
            sys.stdout.write(f"\r{message}")

        sys.stdout.flush()
        self._last_progress_length = len(message)