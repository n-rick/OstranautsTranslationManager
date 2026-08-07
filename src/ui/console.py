"""Interface utilisateur en console pour la revue des traductions."""

from models.text_unit import TextUnit
from config.config import Config
from ui.review_action import ReviewAction


class ConsoleUI:
    """Affiche une unité de texte et propose des actions de revue."""

    def review(self, relative_path: str, unit: TextUnit) -> ReviewAction:
        """Affiche les détails d'une unité et retourne la décision utilisateur."""

        print("\n" + "=" * 70)
        print(f"File : {relative_path}")
        print(f"Path : {unit.json_path}")
        print("=" * 70)

        print("\nTexte source :")
        print(unit.source_text)

        print("\nTexte traduit :")
        print(unit.translated_text)

        print("\n[V] " + Config.VALIDATE + " (par défaut)")
        print("[E] " + Config.EDIT)
        print("[S] " + Config.SKIP)
        print("[N] " + Config.NEXT_FILE)
        print("[Q] " + Config.QUIT)

        choice = input("\nVotre choix : ").strip().upper()
        
        return ReviewAction(choice) if choice else ReviewAction.VALIDATE