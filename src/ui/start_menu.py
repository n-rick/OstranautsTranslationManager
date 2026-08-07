from pathlib import Path
from config.config import Config


class StartMenu:

    def ask(self) -> tuple[bool, Path | None]:
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
                return True, None

            if choice == "2":
                path = Path(input(Config.FILE_PATH_TO_TRANSLATE).strip())

                if path.exists():
                    return False, path

                print(Config.FILE_NOT_EXISTS)