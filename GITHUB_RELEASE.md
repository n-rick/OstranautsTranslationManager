# Release Draft for v1.3.0

## Title
Ostranauts Translation Manager v1.3.0

## Description
Cette version adopte l’API officielle DeepL et améliore la compatibilité avec les fichiers de données Ostranauts contenant des chaînes multilignes.

### Highlights
- Traduction automatique via le SDK officiel DeepL, avec clé configurée dans `.env` (`DEEPL_AUTH_KEY`).
- Protection et restauration des placeholders pendant la traduction.
- Lecture des chaînes JSON contenant des retours à la ligne bruts dans les fichiers du jeu.
- Arrêt propre et signalement du fichier en échec en cas d’erreur persistante du fournisseur.
- Couverture de tests hors ligne pour le service DeepL et les JSON multilignes.

### How to use
- Utilisateur final : `python main.py`
- Menu interactif : `python src/main.py`
- Reprise : `python src/main.py --resume --path /chemin/vers/Ostranauts_Data/StreamingAssets/data --generate-workshop`
- Fichier unique : `python src/main.py --resume --file /chemin/vers/ads/ads.json`
- Générer un mod : `python build_workshop.py`

### Notes
- Une clé API DeepL valide est requise pour les nouvelles traductions.
- Le dossier `output/` contient les fichiers JSON traduits.
- Le dossier `workshop/` contient le mod Workshop prêt à être publié.
