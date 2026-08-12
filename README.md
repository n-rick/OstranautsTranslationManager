# Ostranauts Translation Manager

**Application Python pour maintenir la traduction française d'Ostranauts.**

📌 **Version actuelle** : V1.2.0
🟢 **Statut** : En développement actif
🎮 **Compatibilité** : Ostranauts v1.0.0

---

## 🎯 **Fonctionnalités**

✅ **Scan intelligent** des fichiers JSON du jeu
✅ **Détection automatique** des champs traduisibles (strDesc, strTitle, strTooltip, etc.)
✅ **Traduction automatique** via Google Translate
✅ **Mémoire de traduction** pour éviter de re-traduire
✅ **Interface console** pour valider/éditer les traductions
✅ **Génération de mod Workshop** pour Steam
✅ **Exclusion des fichiers techniques** (tokens, noms, etc.)

---

## 📦 **Structure du projet**

```text
OstranautsTranslationManager/
├── src/
│   ├── config/          # Configuration (variables d'environnement)
│   ├── database/        # Base de données de mémoire de traduction
│   ├── models/          # Modèles (TextUnit, TranslationProject, etc.)
│   ├── rules/           # Règles de détection des textes traduisibles
│   ├── scanner/         # Scan des fichiers JSON
│   ├── translator/      # Services de traduction (Google Translate)
│   ├── ui/             # Interface utilisateur (console)
│   ├── workshop/        # Génération des mods Workshop
│   └── writer/          # Écriture des fichiers traduits
├── output/              # 📂 Fichiers JSON traduits (généré)
├── workshop_output/     # 📦 Mod Workshop prêt à publier (généré)
├── database/           # 💾 Base de données (translation_memory.json)
├── .env                # Configuration locale
├── .env.example        # Exemple de configuration
├── build_workshop.py   # Script pour générer un mod Workshop
└── README.md           # Ce fichier
```

## **Installation**

### 1. Prérequis

Python 3.8+
pip
Un jeu Ostranauts installé (version 1.0.0)

### 2. Cloner le dépôt

```bash
git clone https://github.com/n-rick/OstranautsTranslationManager.git
cd OstranautsTranslationManager
```


### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```


### 4. Configurer l’environnement
```bash
# Copier l'exemple de configuration
cp .env.example .env
```

### Éditer .env avec tes chemins (exemple pour Windows)

OSTRANAUTS_DATA_PATH=C:\\Steam\\steamapps\\common\\Ostranauts\\Ostranauts_Data\\StreamingAssets\\data




## 🎮 **Utilisation**
Option 1 : Menu interactif
```bash
python src/main.py
```

Option 2 : Mode commande
```bash
python src/main.py --resume --path /chemin/vers/Ostranauts_Data/StreamingAssets/data --generate-workshop
```

Option 3 : Reprendre un fichier unique
```bash
python src/main.py --resume --file /chemin/vers/ads/ads.json
```

## **Fonctionnalités :**

Choisir entre traduire tous les fichiers ou un fichier spécifique
Mode automatique (traduction sans validation) ou manuel (validation interactive)
Génération optionnelle d’un mod Workshop
Reprise automatique à partir de la mémoire de traduction et des fichiers déjà générés
Sauvegarde incrémentale après chaque fichier traité

Option 4 : Générer un mod Workshop directement

```bash
python build_workshop.py
```

Ce que ça fait :

Scanne tous les fichiers JSON dans OSTRANAUTS_DATA_PATH
Traduit automatiquement tous les textes
Génère un mod Workshop dans workshop_output/
Affiche les instructions pour tester et publier

### 📁 **Structure d’un mod Workshop pour Ostranauts**

Un mod Workshop valide a cette structure :
text
Copier

Ostranauts_Data/
├── Mods/
│   └── [NomDuMod]/          # Ex: "Ostranauts - Traduction Française"
│       ├── mod_info.json     # ⭐ Métadonnées du mod (obligatoire)
│       └── data/             # ✅ Données du mod (même structure que StreamingAssets/data/)
│           ├── ads/
│           ├── cooverlays/
│           ├── interactions/
│           └── ... (autres dossiers traduits)
└── loading_order.json       # ⭐ Ordre de chargement des mods (obligatoire)



Fichier mod_info.json (exemple)
```json
[{
  "strName": "Ostranauts - Traduction Française",
  "strAuthor": "N'rick FiKDiR",
  "strModURL": "https://github.com/n-rick/OstranautsTranslationManager",
  "strGameVersion": "1.0.0",
  "strModVersion": "1.0.0",
  "strNotes": "Traduction complète en français pour Ostranauts v1.0. Inclut tous les textes du jeu, interfaces, descriptions et dialogues."
}]
```



Fichier loading_order.json (exemple)
```json
[{
  "strName": "Mod Loading Order",
  "strNotes": "To mod Ostranauts, place this loading_order.json file in your Mods/ folder...",
  "aLoadOrder": ["core", "Ostranauts - Traduction Française"],
  "aIgnorePatterns": ["StreamingAssets/data/names_full"]
}]
```


## 🔧 **Configuration**
  
    
      Variable
      Description
      Exemple
    
  
  
    
      OSTRANAUTS_DATA_PATH
      Chemin vers StreamingAssets/data/
      /home/user/Ostranauts/Ostranauts_Data/StreamingAssets/data
    
    
      OUTPUT_PATH
      Dossier de sortie des fichiers traduits
      ./output
    
    
      DATABASE_PATH
      Chemin vers la base de données
      ./database/translation_memory.json
    
    
      WORKSHOP_MOD_NAME
      Nom du mod Workshop
      "Ostranauts - Traduction Française"
    
    
      WORKSHOP_AUTHOR
      Auteur du mod
      "N'rick FiKDiR"
    
    
      WORKSHOP_MOD_VERSION
      Version du mod
      "1.0.0"
    
    
      WORKSHOP_GAME_VERSION
      Version du jeu cible
      "1.0.0"
    
    
      WORKSHOP_OUTPUT_PATH
      Dossier de sortie du mod Workshop
      ./workshop_output
    
  


## 📊 **Quels fichiers sont traduits ?**
### ✅ Répertoires traduits (contiennent du texte)

    
      Répertoire
      Description
      Exemple de contenu
    
  
  
    
      ads/
      Publicités dans le jeu
      Noms et descriptions des pubs
    
    
      cooverlays/
      Noms et descriptions des objets
      strFriendlyName, strDesc
    
    
      headlines/
      Titres des actualités
      strTitle, strBody
    
    
      interactions/
      Actions et interactions
      strText, strDesc
    
    
      items/
      Objets du jeu
      strFriendlyName, strDesc
    
    
      manpages/
      Pages du manuel
      Texte d’aide
    
    
      strings/
      Chaînes de texte générales
      Divers textes UI
    
  


### ❌ Répertoires exclus (technique, pas de texte à traduire)
  
    
      Répertoire
      Raison
    
  
  
    
      tokens/
      Dictionnaires de verbes/noms (technique)
    
    
      names_*/
      Noms des PNJ (ne pas traduire)
    
    
      colors/
      Définitions de couleurs
    
    
      audioemitters/
      Paramètres sonores
    
    
      guipropmaps/
      Mappings UI
    
    
      powerinfos/
      Infos de consommation électrique
    
    
      tickers/
      Minutages
    
    
      traitscores/
      Scores de traits

## 🤝 Contribuer

Les contributions sont les bienvenues ! Ouvre une Issue ou un Pull Request pour :

- Signaler un bug
- Proposer une amélioration
- Ajouter une nouvelle fonctionnalité

## 📜 Licence

Ce projet est sous licence MIT. Tu es libre de l’utiliser, le modifier et le distribuer.

## ✨ Bonnes traductions !

Pour toute question, n’hésite pas à me contacter.
