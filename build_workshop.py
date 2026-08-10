#!/usr/bin/env python3
"""Script pour générer directement un mod Workshop."""
from pathlib import Path
from src.config.config import Config
from src.scanner.scanner import Scanner
from src.database.database import Database
from src.translator.google_translator import GoogleTranslatorService
from src.ui.console import ConsoleUI
from src.writer.json_writer import JsonWriter
from src.translation_manager import TranslationManager
from src.workshop.workshop import WorkshopGenerator

def build_workshop_mod():
    """Génère un mod Workshop complet."""
    print(f"{Config.GREEN}🚀 Début de la génération du mod Workshop... {Config.RESET}")

    # Initialiser les composants
    manager = TranslationManager(
        scanner=Scanner(),
        database=Database(Config.DATABASE_PATH),
        translator=GoogleTranslatorService(),
        console=ConsoleUI(),
        writer=JsonWriter(),
    )

    # Scanner et traduire
    print(f"📂 Scanne {Config.OSTRANAUTS_DATA_PATH}...")
    project = manager.run(Config.OSTRANAUTS_DATA_PATH, automatic=True, generate_workshop=False)

    # Afficher les statistiques
    print(f"\n📊 Statistiques:")
    print(f"   - Fichiers scannés: {project.scanned_files}")
    print(f"   - Traductions depuis la mémoire: {project.cached_count}")
    print(f"   - Nouvelles traductions: {project.translated_count}")
    print(f"   - Fichiers en échec: {len(project.failed_files)}")
    if project.failed_files:
        print(f"{Config.RED} ⚠️  Fichiers en échec: {', '.join(project.failed_files)} {Config.RESET}")

    # Générer le mod Workshop
    print("\n🏗️  Génération du mod Workshop...")
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

    print(f"\n{Config.GREEN} ✅ Mod généré dans: {mod_dir}{Config.RESET}")
    print(f"\n📦 Pour tester localement:")
    print(f"   1. Copiez le dossier '{Config.WORKSHOP_MOD_NAME}' dans:")
    mods_dir = Path(Config.OSTRANAUTS_DATA_PATH).parent.parent / "Mods"
    print(f"      {mods_dir}")
    print(f"   2. Copiez 'loading_order.json' dans:")
    data_dir = Path(Config.OSTRANAUTS_DATA_PATH).parent
    print(f"      {data_dir}")
    print(f"   3. Lancez Ostranauts et vérifiez que la traduction fonctionne.")

    print(f"\n🎮 Pour publier sur Steam Workshop:")
    print(f"   1. Ouvrez Steam → Workshop → Mes fichiers → Ajouter un élément")
    print(f"   2. Sélectionnez le dossier: {mod_dir}")
    print(f"   3. Remplissez les métadonnées et publiez! {Config.RESET}")

if __name__ == "__main__":
    build_workshop_mod()