"""Menu de démarrage de l'application."""

from pathlib import Path
from src.config.config import Config


class StartMenu:
    """Gère les choix initiaux de l'utilisateur."""

    def ask(self) -> tuple[bool, Path | None, bool]:
        """Demande le périmètre et le mode de traduction.

        Returns:
            tuple:
                - True si tout le répertoire Data doit être traité.
                - Le chemin du fichier si un seul fichier est sélectionné.
                - True pour le mode automatique, False pour le mode avec validation.
        """
        print()
        print("=" * 40)
        print(" Ostranauts Translation Manager")
        print("=" * 40)
        print()
        print("1 - " + Config.TRANSLATE_ALL)
        print("2 - " + Config.TRANSLATE_SINGLE)
        print()

        while True:
            choice = input(Config.CHOICE).strip()

            if choice == "1":
                scan_directory = True
                selected_file = None
                break

            if choice == "2":
                path = Path(
                    input(Config.FILE_PATH_TO_TRANSLATE).strip()
                )

                if path.is_file() and path.suffix.lower() == ".json":
                    scan_directory = False
                    selected_file = path
                    break

                print(Config.FILE_NOT_EXISTS)

        print()
        print("1 - Traduction automatique")
        print("2 - Traduction avec validation")
        print()

        while True:
            mode = input(Config.CHOICE).strip()

            if mode == "1":
                return scan_directory, selected_file, True

            if mode == "2":
                return scan_directory, selected_file, False
