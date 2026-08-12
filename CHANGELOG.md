# Changelog

Toutes les modifications notables apportées à ce projet doivent être documentées dans ce fichier.

## [1.2.0] - 2026-08-12
### Added
- Point d'entrée unique via `python main.py` pour un lancement utilisateur simple.
- Support du lancement console de l'application sans commandes Python avancées.
- Amélioration du rapport avec indication du périmètre traité (fichier unique ou répertoire complet).
- Protection renforcée des titres de phase et placeholders réservés comme `STARTING` et `Return to`.

### Fixed
- Correction du comportement de reprise mémoire pour ne pas réutiliser des traductions invalides sur des textes protégés.
- Correction des fichiers JSON de sortie pour les cas `aValues` et autres champs spéciaux.
- Stabilisation du traitement de la traduction et des rapports sur les scannings ciblés.

### Release
- Nouvelle version majeure de correctifs et ergonomie utilisateur après `v1.0.0`.

## [1.0.0] - 2026-08-10
### Added
- Première version stable du gestionnaire de traduction Ostranauts.
- Barre de progression de traduction affichée proprement en ligne unique.
- Exclusion des dossiers et fichiers techniques non translatables pendant le scan JSON.
- Support du nom de fichier tronqué dans l'affichage de progression pour éviter le débordement.

### Fixed
- Correction de l'affichage de la barre de progression pour effacer les anciennes lignes plus longues.
- Amélioration du rendu terminal en mode TTY.
- Correction des erreurs de sortie console sur les fichiers non-traduisibles.

### Release
- Tag Git `v1.0.0` créé.
