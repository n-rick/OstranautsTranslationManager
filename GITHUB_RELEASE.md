# Release Draft for v1.2.0

## Title
Ostranauts Translation Manager v1.2.0

## Description
Version de correctifs et d’ergonomie utilisateur après la première release v1.0.0.

### Highlights
- Lancement simplifié via `python main.py`
- Menu console guidé pour choisir le traitement complet ou un fichier unique
- Mémoire de traduction persistante dans `database/translation_memory.json`
- Reprise incrémentale (`--resume`) sans réappliquer les traductions protégées de façon invalide
- Protection des phrases et tokens réservés comme `STARTING` et `Return to`
- Rapport détaillé indiquant le périmètre traité (fichier unique ou répertoire complet)
- Génération de mod Workshop compatible Steam avec `loading_order.json`
- Exclusion des fichiers techniques et des dossiers non traduisibles

### How to use
- Utilisateur final : `python main.py`
- Menu interactif : `python src/main.py`
- Reprise : `python src/main.py --resume --path /chemin/vers/Ostranauts_Data/StreamingAssets/data --generate-workshop`
- Fichier unique : `python src/main.py --resume --file /chemin/vers/ads/ads.json`
- Générer un mod : `python build_workshop.py`

### Notes
- Le dossier `output/` contient les fichiers JSON traduits.
- Le dossier `workshop/` contient le mod Workshop prêt à être publié.
