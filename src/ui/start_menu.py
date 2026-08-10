"""Menu de démarrage pour choisir le mode de fonctionnement."""
from pathlib import Path
from src.config.config import Config

class StartMenu:
    """Affiche le menu de démarrage et gère les choix de l'utilisateur."""

    def ask(self) -> tuple[bool, str, bool, bool]:
        """Demande à l'utilisateur le mode de fonctionnement.

        Returns:
            tuple: (scan_directory, file_path, automatic, generate_workshop)
        """
        print("\n" + "=" * 70)
        print("  Ostranauts Translation Manager")
        print("=" * 70)
        print(Config.CHOICE)
        print("  <> 1. " + Config.TRANSLATE_ALL)
        print("  <> 2. " + Config.TRANSLATE_SINGLE)
        print("  <> 3. " + Config.QUIT)
        print("=" * 70)

        choice = input("> ").strip()

        if choice == "1":
            return self._handle_scan_directory()
        elif choice == "2":
            return self._handle_single_file()
        elif choice == "3":
            exit(0)
        else:
            print("Choix invalide. Veuillez réessayer.")
            return self.ask()

    def _handle_scan_directory(self) -> tuple[bool, str, bool, bool]:
        """Gère le choix de scanner un répertoire."""
        scan_dir = input("Entrée pour utiliser OSTRANAUTS_DATA_PATH"
        ).strip()
        if not scan_dir:
            scan_dir = Config.OSTRANAUTS_DATA_PATH

        # Vérifier que le répertoire existe
        if not Path(scan_dir).exists():
            print(f"{Config.RED}[ERROR] ⚠️ Le répertoire n'existe pas: {scan_dir} {Config.RESET}")
            return self.ask()

        automatic = input(f"{Config.GREEN} <> Mode automatique ? (o/n): {Config.RESET}").strip().lower() == "o"
        generate_workshop = (
            input(Config.GENERATE_WORKSHOP_QUESTION).strip().lower() == "o"
        )
        return True, scan_dir, automatic, generate_workshop

    def _handle_single_file(self) -> tuple[bool, str, bool, bool]:
        """Gère le choix de scanner un fichier unique."""
        file_path = input(f"{Config.GREEN}<> Saisir le chemin du fichier .json à traduire : \n(ex: steamapps/common/Ostranauts/Ostranauts_Data/StreamingAssets/data/info/infoNodes.json) {Config.RESET} \n").strip()

        if not Path(file_path).exists():
            print(Config.FILE_NOT_EXISTS)
            return self.ask()

        automatic = input(" <> Mode automatique ? (o/n): ").strip().lower() == "o"
        generate_workshop = (
            input(Config.GENERATE_WORKSHOP_QUESTION).strip().lower() == "o"
        )
        return False, file_path, automatic, generate_workshop
