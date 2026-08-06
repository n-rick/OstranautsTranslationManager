from models.text_unit import TextUnit
from config.config import Config


class ConsoleUI:

    def review(self, unit: TextUnit) -> str:

        print("\n" + "=" * 70)
        print(f"File : {unit.source_file}")
        print(f"Path : {unit.json_path}")
        print("=" * 70)

        print("\nSource :")
        print(unit.source_text)

        print("\nTranslation :")
        print(unit.translated_text)

        print("\n[V] " + Config.VALIDATE)
        print("[E] " + Config.EDIT)
        print("[S] " + Config.SKIP)
        print("[Q] " + Config.QUIT)

        return input("\nChoice : ").strip().upper()