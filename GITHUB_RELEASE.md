# Release Draft for v1.0.0

## Title
Ostranauts Translation Manager v1.0.0

## Description
Première version stable du projet.

### Highlights
- Traduction automatique des fichiers JSON d'Ostranauts
- Mémoire de traduction persistante dans `database/translation_memory.json`
- Reprise incrémentale (`--resume`) pour éviter de tout refaire après un crash
- Génération de mod Workshop compatible Steam avec `loading_order.json`
- Barre de progression terminale propre et message de sauvegarde des fichiers traduits
- Exclusion des fichiers techniques et des dossiers non traduisibles

### How to use
- Utilisateur final : `python main.py`
- Menu interactif : `python src/main.py`
- Reprise : `python src/main.py --resume --path /chemin/vers/Ostranauts_Data/StreamingAssets/data --generate-workshop`
- Fichier unique : `python src/main.py --resume --file /chemin/vers/ads/ads.json`
- Générer un mod : `python build_workshop.py`

### Notes
- Le dossier `output/` contient les fichiers JSON traduits.
- Le dossier `workshop_output/` contient le mod Workshop prêt à être publié.
