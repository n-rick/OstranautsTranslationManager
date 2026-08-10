"""Scan des fichiers JSON du projet."""
from pathlib import Path
from src.config.config import Config
from src.models.text_unit import TextUnit
from src.models.translation_project import TranslationProject
from src.scanner.json_extractor import JsonExtractor

class Scanner:
    """Parcourt un répertoire pour trouver les fichiers JSON à traduire."""

        # Répertoires à scanner pour la traduction (contiennent du texte)
    TRANSLATABLE_DIRS = {
        "ads",           # Publicités
        "archived_content",
        "attackmodes",
        "careers",       # Création du personnages
        "conditions",    # Stats et variables pour décrire
        "conditions_simple", # Plus de stats
        "context",
        "cooverlays",    # Noms et descriptions des objets
        "headlines",     # Titres des actualités
        "interactions",  # Actions/interactions
        "items",         # Objets
        "jobitems",
        "ledgerdefs",
        "manpages",      # Pages du manuel
        "market",
        "pda_apps",
        "pledges",
        "plot_beat_overrides",
        "plots",
        "racing",
        "rooms",
        "slots",
        "strings",       # Chaînes de texte générales
        "tips",
        ""
    }

    # Répertoires à exclure (technique, pas de texte à traduire)
    EXCLUDED_DIRS = {
        "ai_training",    # Décision de l'IA
        "audioemitters", # Émetteurs sonores (technique)
        "colors",        # Couleurs (technique)
        "condowners",      # template des objets
        "condtrigs",
        "chargeprofiles",
        "crewskins",
        "crime",
        "explosions",
        "gasrespires",   # Consommation de gaz (technique)
        "guipropmaps",   # Mappings UI (technique)
        "jobs",
        "lifeevents",
        "lights",
        "loot",
        "music",
        "music_stations",
        "names_first",   # Prénoms (ne pas traduire)
        "names_full",    # Noms complets (ne pas traduire)
        "names_last",    # Noms de famille (ne pas traduire)
        "names_robots",
        "names_ship",    # Noms de vaisseaux (ne pas traduire)
        "names_ship_adjectives",
        "names_ship_nouns",
        "parallax",
        "personspecs",
        "plot_beats",
        "plot_manager",
        "powerinfos",    # Infos puissance (technique)
        "schemas",
        "ships",
        "shipspecs",
        "slot_effects",
        "starsystem",    # Système stellaire (technique)
        "tickers",       # Minutages (technique)
        "tokens",        # Dictionnaires techniques (verbes, noms)
        "traitscores",   # Scores de traits (technique)
        "transit",
        "tsv",
        "wounds",
        "zone_triggers",
    }

    EXCLUDED_FILE_NAMES = {
        "interactions_encounters.json",
    }

    def __init__(self) -> None:
        """Initialise l'extracteur et le compteur de fichiers scannés."""
        self.extractor = JsonExtractor()

    def scan(self, directory: str) -> TranslationProject:
        """Retourne toutes les unités de texte extraites des fichiers JSON du répertoire."""
        project = TranslationProject()
        files = sorted(
            Path(directory).rglob("*.json"),
            key=lambda file: str(file.relative_to(directory)).lower(),
        )

        for file in files:
            project.scanned_files += 1
            try:
                relative = str(file.relative_to(directory))

                if self._should_exclude_file(relative):
                    continue

                project.files[relative] = self.extractor.extract(
                    str(file), relative
                )
            except Exception as error:
                project.failed_files.append(str(file))
                print(f"{Config.RED} [ERROR] {file}{Config.RESET}")
                print(error)

        project.root_directory = directory
        return project

    def _should_exclude_file(self, relative_path: str) -> bool:
        """Vérifie si un fichier doit être exclu du scan."""
        # Extraire tous les segments de chemin
        parts = relative_path.split("/")

        # Exclure un fichier s'il correspond à un nom de fichier exclu
        if Path(relative_path).name in self.EXCLUDED_FILE_NAMES:
            return True

        # Exclure un fichier si un segment correspond à un dossier exclu
        if any(part in self.EXCLUDED_DIRS for part in parts):
            return True

        # Inclure uniquement si le premier niveau est dans TRANSLATABLE_DIRS (si la liste est non vide)
        if parts and self.TRANSLATABLE_DIRS and parts[0] not in self.TRANSLATABLE_DIRS:
            return True

        return False


    def scan_file(self, file_path: str, base_directory: str = None) -> TranslationProject:
        """Retourne toutes les unités de texte extraites d'un fichier JSON spécifique.

        Args:
            file_path: Chemin complet vers le fichier JSON
            base_directory: Répertoire de base pour calculer le chemin relatif.
                          Si None, utilise le parent du fichier.
        """
        project = TranslationProject()
        file = Path(file_path)
        try:
            project.scanned_files = 1

            # Déterminer le répertoire de base
            if base_directory:
                base_dir = Path(base_directory)
            else:
                # Par défaut, utiliser le parent du fichier comme base
                # mais essayer de remonter d'un niveau pour conserver la structure
                base_dir = file.parent.parent if len(file.parts) > 2 else file.parent

            # Calculer le chemin relatif
            try:
                relative_path = str(file.relative_to(base_dir))
            except ValueError:
                # Si le fichier n'est pas sous base_dir, utiliser juste le nom du fichier
                relative_path = file.name

            project.root_directory = str(base_dir)
            project.files[relative_path] = self.extractor.extract(
                str(file), relative_path
            )
            return project
        except Exception as error:
            project.failed_files.append(str(file))
            print(f"{Config.RED}[ERROR] {file}{Config.RESET}")
            print(error)
            project.root_directory = str(Path(file_path).parent)
            return project
